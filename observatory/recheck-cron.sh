#!/bin/zsh
# 관측소 판정기 — 매일 09:30 돌면서 **판정이 나면 그때만** 비서실 인박스에 알린다.
#
# 왜 (2026-09-14): BWT 데이터가 48시간 뒤에 들어온다. 그걸 사람이 기억해서 다시 볼 리가 없다.
#   🟡(대기)면 조용히 로그만 남기고, 🔴/🟢(판정 남)이면 인박스에 한 줄 올린다.
#   판정이 한 번 나가면 STAMP 를 남겨 **같은 판정을 매일 반복해서 올리지 않는다.**
LOG=/Users/sexyflash/Projects/cue/crawler/data/observatory.log
INBOX=/Users/sexyflash/slack-bot/memory/secretary/inbox.md
STAMP=/Users/sexyflash/Projects/momentus/observatory/data/.verdict_sent
NODE=/opt/homebrew/bin/node
DAY=$(TZ=Asia/Seoul date '+%Y-%m-%d')

out=$($NODE /Users/sexyflash/Projects/momentus/observatory/recheck.mjs 2>&1)
echo "════════ $DAY $(TZ=Asia/Seoul date '+%H:%M') ════════" >> "$LOG"
echo "$out" >> "$LOG"

# 🔴 '첫 줄' 이 아니라 **대기(🟡·⏳)가 아닌 첫 줄** 을 판정으로 삼는다.
#   빙 노출은 아직 대기(🟡)인데 소유확인만 먼저 승격(🟢)되는 경우가 있다 —
#   head -1 로 잡으면 그 승격을 영영 못 알린다.
verdict=$(echo "$out" | grep -E '^  (🔴|🟢)' | head -1)
[ -z "$verdict" ] && exit 0            # 전부 대기 — 조용히 있는다
[ -f "$STAMP" ] && [ "$(cat $STAMP)" = "$verdict" ] && exit 0   # 같은 판정 반복 금지
echo "$verdict" > "$STAMP"
{
  echo ""
  echo "- [관측소] 빙/GEO 판정이 나왔습니다 ($DAY)"
  echo '```'
  echo "$out" | sed -n '/── 판정/,/── 손으로 볼 것/p' | head -12
  echo '```'
  echo "  전문: $LOG · 재실행: node ~/Projects/momentus/observatory/recheck.mjs"
} >> "$INBOX"
