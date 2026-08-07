#!/usr/bin/env python3
"""
PostToolUse 훅 — 페이지에 영향을 주는 파일을 고치면 SEO 점검 결과를 알려준다.

왜 필요한가: docs/SEO_GEO.md 가 있어도 사람도 에이전트도 매번 읽지 않는다.
og:image 가 33개 페이지에서 통째로 빠져 있던 걸 몇 달 뒤에야 발견했다(2026-08-07).
그래서 "고치면 바로 알려주는" 자리를 만든다.

**절대 작업을 막지 않는다.** 항상 exit 0 이고 decision:block 을 내지 않는다.
전역 원칙: deterministic 게이트는 오발동해도 손해 0 인 자리에만 둔다.
진짜 게이트는 사람이 보는 `python3 scripts/seo_check.py` 다.

stdin 으로 훅 입력 JSON 을 받는다. 출력은 systemMessage(사용자용) + additionalContext(모델용).
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 이 파일들을 고치면 페이지 <head>·구조화데이터·OG이미지가 바뀔 수 있다.
WATCH = re.compile(
    r"(scripts/gen_site\.py|scripts/gen_og\.py|data/products\.json|\.html)$"
)


def out(payload: dict) -> None:
    print(json.dumps(payload, ensure_ascii=False))
    sys.exit(0)


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)  # 입력이 이상해도 조용히 통과 — 작업을 방해하지 않는다

    ti = data.get("tool_input") or {}
    tr = data.get("tool_response") or {}
    path = tr.get("filePath") or ti.get("file_path") or ""
    if not path or not WATCH.search(path):
        sys.exit(0)

    # 생성물(og/, docs/)만 건드린 경우는 점검할 게 없다
    if "/og/" in path or "/docs/" in path:
        sys.exit(0)

    try:
        r = subprocess.run(
            [sys.executable, os.path.join(ROOT, "scripts", "seo_check.py")],
            cwd=ROOT, capture_output=True, text=True, timeout=60,
        )
    except Exception:
        sys.exit(0)

    tail = [ln for ln in r.stdout.strip().split("\n") if "FAIL" in ln and "건" in ln]
    summary = tail[-1].strip() if tail else "SEO 점검 결과를 읽지 못했습니다"

    if r.returncode == 0:
        out({"systemMessage": f"✅ SEO 점검 통과 — {summary}", "suppressOutput": True})

    # 개별 항목은 "       FAIL  <메시지>" 꼴. 마지막 요약 줄("FAIL N건 · warn M건")은 뺀다.
    fails = [ln.strip() for ln in r.stdout.split("\n") if "FAIL  " in ln][:8]
    detail = "\n".join(fails)
    out({
        "systemMessage": f"🔴 SEO 점검 미달 — {summary} (docs/SEO_GEO.md §3)",
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": (
                f"SEO/GEO 점검기가 배포 기준 미달을 보고했습니다 ({summary}).\n"
                f"{detail}\n\n"
                "정본은 docs/SEO_GEO.md §3(필수 9종)·§4(페이지별 JSON-LD)입니다.\n"
                "`python3 scripts/seo_check.py` 로 전체를 보고 고치세요. "
                "이 훅은 작업을 막지 않으니, 지금 작업과 무관하면 그대로 진행해도 됩니다."
            ),
        },
    })


if __name__ == "__main__":
    main()
