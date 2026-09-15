#!/usr/bin/env python3
"""실험 판정일 알리미 — "해봤는데 어떻게 됐나"를 **때가 되면 다시 묻는** 자리.

왜 (2026-09-15): `docs/SEO_EXPERIMENTS.md` 는 잘 설계돼 있었는데 **굴러가지 않았다.**
  ⏳(관찰 중) 가 14건 쌓였고 확인일 9/4·9/11 이 지났는데 아무도 판정을 안 적었다.
  상기시키는 장치가 `seo_weekly.sh` 가 **로그 파일에 찍는 한 줄**뿐이었고, 그 로그는
  아무도 안 읽는다. 로그에만 있는 알림은 없는 것과 같다(slack-bot 룰 #9).

그래서 **확인일이 지난 실험**을 주간 표에 얹어 대표가 보는 자리로 끌어올린다.

무엇이 결정론인가 (slack-bot 룰 #1)
  이 스크립트는 자연어를 한 글자도 판단하지 않는다. **고정 칸 표를 파싱**해 날짜만 비교한다.
  "효과가 있었나"는 사람(또는 LLM)이 숫자를 보고 적는다 — 그건 코드가 할 일이 아니다.

표 형식 (SEO_EXPERIMENTS.md 의 `## ⏳ 판정 대기` 아래 표 하나가 단일 소스)
  | 실험 | 사이트 | 조치일 | 확인일 | 무엇을 재나 | 조치 전 값 |

쓰는 법
  python3 scripts/exp_due.py            # 확인일 지난 것만 사람이 읽는 줄로
  python3 scripts/exp_due.py --all      # 대기 전부
  python3 scripts/exp_due.py --json
"""
from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

LEDGER = Path(__file__).resolve().parent.parent / "docs" / "SEO_EXPERIMENTS.md"
HEAD = "## ⏳ 판정 대기"
DATE = re.compile(r"(\d{4})-(\d{2})-(\d{2})")


def rows(path: Path = LEDGER) -> list[dict]:
    """대기 표를 읽는다. 표가 없거나 깨져도 빈 목록 — 본 흐름을 막지 않는다(비파괴)."""
    try:
        text = path.read_text("utf-8")
    except Exception:
        return []
    if HEAD not in text:
        return []
    block = text.split(HEAD, 1)[1].split("\n## ", 1)[0]
    out = []
    for line in block.splitlines():
        line = line.strip()
        if not line.startswith("|") or line.startswith("|---") or "실험 |" in line:
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 6:
            continue
        m = DATE.search(cells[3])
        if not m:
            continue
        out.append({"exp": cells[0], "site": cells[1], "done": cells[2],
                    "due": "-".join(m.groups()), "measure": cells[4], "before": cells[5]})
    return out


def due(today: date | None = None, path: Path = LEDGER) -> list[dict]:
    t = (today or date.today()).isoformat()
    return [r for r in rows(path) if r["due"] <= t]


def lines(items: list[dict]) -> list[str]:
    return [f"{r['exp']} · {r['site']} — {r['measure']} (조치 {r['done']} · 확인일 {r['due']} · 조치 전 {r['before']})"
            for r in items]


def main() -> int:
    argv = sys.argv[1:]
    items = rows() if "--all" in argv else due()
    if "--json" in argv:
        print(json.dumps(items, ensure_ascii=False))
        return 0
    if not items:
        return 0
    print(f"확인일이 지난 실험 {len(items)}건 — 숫자를 재서 ✅/❌/🌫 를 원장에 적어라")
    for s in lines(items):
        print("  " + s)
    return 0


if __name__ == "__main__":
    sys.exit(main())
