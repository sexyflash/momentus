#!/bin/zsh
# 관측소 주간 회차 — 크론 진입점 하나. 정본: docs/OBSERVATORY.md
#
# ⚠️ 기존 `seo_weekly.sh` 를 **대체하지 않는다. 감싼다.**
#    그쪽은 사람이 읽는 로그를 계속 남기고(가설·실험 원장 안내가 거기 붙어 있다),
#    이쪽은 같은 계기들을 기계용으로 다시 읽어 표·원장·슬랙을 만든다.
#    크론 줄은 **이 파일 하나**로 바뀐다 — 두 줄로 두면 한쪽만 고쳐진다.
#
# 🔴 크론 함정 3개 (전부 여기서 처리했다)
#   1. PATH 가 거의 없다 → 모든 실행 파일을 **절대경로**로 쓴다
#   2. `~/.local/bin` 이 PATH 에 없다 → 아래 PATH 에 직접 박는다
#   3. 헤드리스 `claude -p` 는 파일을 못 쓴다 → 이 경로엔 claude 를 쓰지 않는다(전부 결정론)

export PATH=/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$HOME/.local/bin
NODE=/opt/homebrew/bin/node
PY=/usr/bin/python3
OBS=$HOME/Projects/momentus/observatory
LOG=$HOME/Projects/cue/crawler/data/observatory.log

{
  echo "════════ $(TZ=Asia/Seoul date '+%Y-%m-%d %H:%M KST') 관측소 회차 시작 ════════"

  # ① 기존 주간 점검 — 그대로 돈다(로그 위치도 그대로)
  /bin/zsh "$HOME/Projects/momentus/scripts/seo_weekly.sh"
  echo "  seo_weekly.sh rc=$?"

  # ② 수집 → 원장 append → 표
  cd "$HOME/Projects/momentus" || exit 1
  "$NODE" "$OBS/collect.mjs"
  rc=$?
  echo "  collect.mjs rc=$rc"

  # ③ 슬랙 — 수집이 실패해도 보낸다. 침묵이 제일 나쁘다(룰 #6).
  #    표를 못 그리면 notify.py 가 "못 그렸다"를 대신 보낸다.
  "$PY" "$OBS/notify.py"
  echo "  notify.py rc=$?"
  echo
} >> "$LOG" 2>&1
