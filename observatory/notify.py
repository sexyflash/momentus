#!/usr/bin/env python3
"""관측소 슬랙 발송 — 표를 **원장에서 읽어** 한 장 보낸다.

## 왜 이 파일이 따로 있나

수집(collect.mjs)과 발송을 한 프로세스에 두면, 발송이 실패할 때 수집까지 다시 돌아야 한다.
원장이 이미 진실이므로 발송은 **원장을 읽어 다시 그리기만** 하면 된다(`--no-collect`).

## 발송 경로 (slack-bot 룰 #3)

페르소나 발송은 `bot_messenger.send_as_persona()` 단일 진입점만 통과한다. 그런데 그 함수는
**봇 프로세스 안에서만** 동작한다(`register_bots()` 가 거기서 돈다). 관측소는 크론에서 도는
별도 프로세스라 등록된 봇이 없다 → 그대로 부르면 **예외 없이 조용히 drop** 된다.

그래서 `naver_keepalive.slack_alert` 와 **같은 모양**을 쓴다:
  ① 봇 안이면 `send_as_persona`  ② 밖이면 ops 봇 토큰으로 직접 발송(폴백).
폴백은 룰 #3 우회가 아니라 **침묵 방지**다(룰 #6: 조용히 못 보내면 알림이 증발한다).
폴백에서도 `username`·`icon_*` 을 박지 않는다 — ops 봇 자신의 프로필로 나가므로
페르소나 정체성이 어긋나지 않는다.

쓰는 법
    python3 observatory/notify.py            # 원장을 읽어 표를 #운영실로
    python3 observatory/notify.py --dry      # 보낼 본문만 출력(발송 안 함)
    python3 observatory/notify.py --week 2026-W38
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
NODE = "/opt/homebrew/bin/node"          # 🔴 크론엔 PATH 가 없다. 절대경로.
COLLECT = HERE / "collect.mjs"
CHANNEL = os.environ.get("OBSERVATORY_CHANNEL", "C0B4CQDHZCL")   # #운영실
PERSONA = "ops"
SLACK_BOT = Path.home() / "slack-bot"


def _env_token() -> str:
    """봇 밖 폴백용 토큰. slack-bot/.env 에서 직접 읽는다(그 프로세스가 아니라 파일이 진실)."""
    tok = os.environ.get("SLACK_OPS_BOT_TOKEN") or os.environ.get("SLACK_SECRETARY_BOT_TOKEN")
    if tok:
        return tok
    try:
        for line in (SLACK_BOT / ".env").read_text("utf-8", "replace").splitlines():
            line = line.strip()
            for key in ("SLACK_OPS_BOT_TOKEN=", "SLACK_SECRETARY_BOT_TOKEN="):
                if line.startswith(key):
                    return line[len(key):].strip().strip("'\"")
    except Exception:
        pass
    return ""


def build(week: str | None = None) -> str:
    """표 본문. **collect.mjs 의 렌더러 하나만** 쓴다 — 여기서 다시 그리면 두 벌이 된다."""
    args = [NODE, str(COLLECT), "--no-collect", "--message"]
    if week:
        args += ["--week", week]
    p = subprocess.run(args, capture_output=True, text=True, cwd=str(HERE.parent), timeout=300)
    if p.returncode != 0:
        raise RuntimeError((p.stderr or p.stdout or "collect.mjs 실패").strip()[:300])
    return p.stdout.strip()


def to_mrkdwn(text: str) -> str:
    """슬랙 표기로 변환. 🚫 변환 규칙을 여기서 새로 쓰지 마라 — slack_mrkdwn 이 단일 소스다."""
    sys.path.append(str(SLACK_BOT))
    try:
        import slack_mrkdwn  # type: ignore
        return slack_mrkdwn.to_slack_mrkdwn(text)
    except Exception as e:  # noqa: BLE001
        print(f"[observatory] mrkdwn 변환 불가(원문 그대로): {str(e)[:100]}", file=sys.stderr)
        return text


def send(text: str) -> bool:
    if not text:
        return False
    sys.path.append(str(SLACK_BOT))
    try:
        import bot_messenger  # type: ignore
        if bot_messenger.is_ready():
            if bot_messenger.send_as_persona(PERSONA, CHANNEL, text):
                return True
            print("[observatory] 단일 진입점 발송 실패 — 폴백 시도", file=sys.stderr)
    except Exception as e:  # noqa: BLE001
        print(f"[observatory] bot_messenger 경유 불가(폴백): {str(e)[:120]}", file=sys.stderr)

    tok = _env_token()
    if not tok:
        print("[observatory] 🔴 슬랙 토큰 없음 — 발송 포기(표는 원장에 남아 있다)", file=sys.stderr)
        return False
    # ⚠️ 폴백은 bot_messenger 를 안 타므로 **마크다운 변환도 안 탄다** — `**굵게**` 가 그대로
    #    나간다(슬랙은 `*굵게*` 다, 메모리 slack-mrkdwn-not-markdown). 변환기를 직접 부른다.
    text = to_mrkdwn(text)
    try:
        req = urllib.request.Request(
            "https://slack.com/api/chat.postMessage",
            data=json.dumps({"channel": CHANNEL, "text": text, "unfurl_links": False}).encode(),
            headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json; charset=utf-8"},
        )
        with urllib.request.urlopen(req, timeout=20) as r:
            res = json.loads(r.read().decode())
        if not res.get("ok"):
            print(f"[observatory] 🔴 슬랙 거부: {res.get('error')}", file=sys.stderr)
            return False
        return True
    except Exception as e:  # noqa: BLE001
        print(f"[observatory] 🔴 발송 실패: {str(e)[:160]}", file=sys.stderr)
        return False


def main() -> int:
    argv = sys.argv[1:]
    week = argv[argv.index("--week") + 1] if "--week" in argv else None
    try:
        text = build(week)
    except Exception as e:  # noqa: BLE001
        # 🚫 조용히 죽지 마라. 표를 못 그린 것도 알려야 할 사실이다.
        text = f"🔴 관측소 표를 그리지 못했습니다 — {str(e)[:300]}"
        if "--dry" in argv:
            print(to_mrkdwn(text))
            return 1
        send(text)
        return 1
    if "--dry" in argv:
        print(to_mrkdwn(text))     # 보이는 것 = 나가는 것
        return 0
    return 0 if send(text) else 1


if __name__ == "__main__":
    sys.exit(main())
