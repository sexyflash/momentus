#!/bin/zsh
# 주간 SEO/GEO 전수 점검 (SEO_GEO.md §18-3).
#
# 왜 있나 (2026-08-28): SEO 결함은 배포 순간에 안 보이고 **다음에 누가 볼 때까지 그대로 산다.**
#   /blog→/insights 통합 후 sitemap 이 25일간 어긋나 있었는데 아무도 몰랐다.
#   cue 는 배포 직후 점검이 crawl.mjs 에 붙어 있고, 이건 **전 도메인**을 주 1회 훑는다.
#
# 🚫 아무것도 막지 마라 — 경고만 남긴다(§13). 사람이 로그를 보고 판단한다.
# 로그: ~/Projects/cue/crawler/data/seo_weekly.log

LOG=~/Projects/cue/crawler/data/seo_weekly.log
CHK=~/bin/seo_check.py

{
  echo "════════ $(TZ=Asia/Seoul date '+%Y-%m-%d %H:%M KST') ════════"
  for d in the-moment.us cue.the-moment.us notes.the-moment.us mark.the-moment.us heyreci.com; do
    cd ~/Projects/momentus || exit 1
    out=$(/usr/bin/python3 "$CHK" --live --domain "$d" --pages 1 --orphans 2>&1)
    echo "── $d"
    echo "$out" | grep -E "FAIL [0-9]+건" | sed 's/^/   /'
    echo "$out" | grep -E "^  🔴|FAIL  |고아 [0-9]+장" | head -20 | sed 's/^/   /'
  done
  # 색인이 실제로 어떻게 됐나 — 키(.gindex-sa.json)가 있으면 자동으로 나온다.
  # 없으면 한 줄만 남고 넘어간다. 사람이 GSC 화면을 열 필요가 없어지는 지점이다.
  echo "── 서치콘솔"
  cd ~/Projects/cue 2>/dev/null && /opt/homebrew/bin/node scripts/gsc.mjs --all 2>&1 | sed 's/^/   /'
  cd ~/Projects/momentus || exit 1

  # 프로그래매틱 묶음 고유도 — 40% 미만이면 템플릿을 손봐야 한다(§17)
  echo "── 원장 (증거를 안 적으면 남는 게 없다)"
  echo "   가설: ~/Projects/cue/SEO_HYPOTHESES.md — 확인일 지난 가설의 GSC 숫자를 표에 적어라"
  echo "   실험: ~/Projects/momentus/docs/SEO_EXPERIMENTS.md — 판정(✅/❌/🌫)을 갱신하고,"
  echo "         ❌·🌫 를 지우지 마라. '해봤는데 안 되더라'가 제일 값나가는 기록이다"
  grep -n "⏳" ~/Projects/momentus/docs/SEO_EXPERIMENTS.md 2>/dev/null | head -12 | sed "s/^/   관찰중 /"

  echo "── 고유도"
  /usr/bin/python3 "$CHK" --uniq "https://cue.the-moment.us/job/" 2>&1 | grep -E "평균|🔴|🟠" | sed 's/^/   /'
  echo
} >> "$LOG" 2>&1
