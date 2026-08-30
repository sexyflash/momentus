#!/bin/zsh
# 구글 서비스계정 키 발급 + 전 저장소 배치 — 한 번 돌리면 끝난다.
#
# ── 왜 있나 (2026-08-28)
# SEO/GEO 자동화(색인 API 푸시 · Search Console 읽기 · GA4 리포팅)는 전부
# **서비스계정 키 파일 하나**에 걸려 있다. 사이트가 5개라 매번 콘솔을 손으로 도는 건 낭비다.
#
# 이미 끝나 있는 것 (2026-08-28, 브라우저로 처리):
#   · GCP 프로젝트         sexyflash-mcp-2026 (기존 재사용)
#   · API 3종 사용 설정     indexing / searchconsole / analyticsdata
#   · 서비스계정            gindex@sexyflash-mcp-2026.iam.gserviceaccount.com
#   · GSC 소유자 등록       sc-domain:cue.the-moment.us  ✅
#
# 남은 것 = 이 스크립트가 하는 것: 키 발급 → 각 저장소에 배치 → 검증
#
# 🚫 키 파일을 커밋하지 마라. 각 저장소 .gitignore 에 .gindex-sa.json 이 있는지 확인한다.
# 🚫 키를 슬랙·문서·대화에 붙여넣지 마라. 파일로만 옮긴다.
set -e
export PATH="/opt/homebrew/share/google-cloud-sdk/bin:$PATH"

SA="gindex@sexyflash-mcp-2026.iam.gserviceaccount.com"
PROJECT="sexyflash-mcp-2026"
KEY="$HOME/.config/gindex-sa.json"          # 정본 1벌. 저장소에는 복사본이 간다.
REPOS=(cue mark notes momentus heyreci)

echo "── 1. 인증 확인"
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" 2>/dev/null | grep -q .; then
  echo "🔴 gcloud 로그인이 안 돼 있다.  gcloud auth login  을 먼저 돌려라."
  exit 1
fi
echo "   ✅ $(gcloud auth list --filter=status:ACTIVE --format='value(account)' 2>/dev/null | head -1)"

echo "── 2. 키 발급"
mkdir -p "$(dirname "$KEY")"
if [ -f "$KEY" ]; then
  echo "   ⏭  이미 있다: $KEY  (다시 만들려면 지우고 재실행)"
else
  gcloud iam service-accounts keys create "$KEY" \
    --iam-account="$SA" --project="$PROJECT" >/dev/null
  chmod 600 "$KEY"
  echo "   ✅ 발급: $KEY"
fi

echo "── 3. 저장소 배치"
for r in $REPOS; do
  d="$HOME/Projects/$r"
  [ -d "$d" ] || { echo "   ⏭  $r — 저장소 없음"; continue; }
  cp "$KEY" "$d/.gindex-sa.json"
  chmod 600 "$d/.gindex-sa.json"
  # gitignore 확인 — 없으면 추가한다. 키가 커밋되면 구글이 자동으로 무효화한다.
  if ! git -C "$d" check-ignore -q .gindex-sa.json 2>/dev/null; then
    echo ".gindex-sa.json" >> "$d/.gitignore"
    echo "   ⚠️  $r — .gitignore 에 추가했다"
  fi
  echo "   ✅ $r/.gindex-sa.json"
done

echo "── 4. 검증"
cd "$HOME/Projects/cue" 2>/dev/null && {
  echo -n "   Search Console 읽기: "; node scripts/gsc.mjs 2>&1 | grep -E "사이트맵|🔴" | head -2 || echo "실패"
  echo -n "   색인 API: "; node scripts/gindex.mjs "https://cue.the-moment.us/" 2>&1 | tail -1
}

cat <<'NOTE'

── 남은 수동 작업 (각 1분, 브라우저)
  1) GSC 다른 속성에도 같은 서비스계정을 **소유자**로 추가
     https://search.google.com/search-console/users?resource_id=sc-domain%3Athe-moment.us
     https://search.google.com/search-console/users?resource_id=sc-domain%3Aheyreci.com
     → 이메일: gindex@sexyflash-mcp-2026.iam.gserviceaccount.com

  2) GA4 속성에 같은 계정을 **뷰어**로 추가 (analytics.google.com → 관리 → 속성 액세스 관리)

  ⚠️ sc-domain:the-moment.us 하나가 cue·mark·notes·apex 를 전부 덮는다.
     heyreci.com 만 별도 속성이다.
NOTE
