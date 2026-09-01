#!/bin/bash
# the-moment.us 자동 재빌드 — 제품 피드(스트림)를 매일 다시 긁어 랜딩을 갱신한다.
#   호출: launchd(com.sexyflash.momentus-rebuild) 매일 05:45. 수동 실행도 가능.
#   안전장치
#     · 생성 실패하면 배포하지 않는다(깨진 사이트를 올리지 않는다).
#     · 변경이 없으면 커밋·배포를 건너뛴다(빈 배포 금지).
#     · 커밋만 하고 origin push 는 하지 않는다(푸시는 사장님 결정).
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1

# ⚠️ 생성물 경로는 **한 곳에만** 적는다. 두 군데(diff 검사 / git add)에 따로 적었더니
#    how-to-pay·i·inquiry 가 add 목록에서만 빠져 **생성은 되는데 커밋은 안 되는** 상태로
#    방치됐다(2026-08-07 발견). 새 최상위 생성 경로를 만들면 여기 한 줄만 추가해라.
GEN_PATHS="index.html stories insights tools products about legal apps og how-to-pay inquiry i sitemap.xml robots.txt llms.txt"

echo "───────── $(date '+%Y-%m-%d %H:%M:%S') 재빌드 시작"

# ⚠️ 2026-07-28 사고 재발 방지 — 옛 상태로 배포해 사이트가 통째로 되돌아갔다.
#    다른 곳(다른 세션·기기)에서 올린 커밋을 먼저 받고, 갈라져 있으면 배포하지 않는다.
git fetch -q origin || echo "  ⚠️ fetch 실패 — 로컬 기준으로 진행"
if ! git merge-base --is-ancestor origin/main HEAD 2>/dev/null; then
  echo "❌ origin/main 에 로컬에 없는 커밋이 있다 — 사람이 병합해야 한다. 배포 중단."
  echo "   해결: git pull --rebase origin main (또는 git merge origin/main) 후 다시 실행"
  exit 1
fi

if ! python3 scripts/gen_site.py; then
  echo "❌ 생성 실패 — 배포하지 않고 중단"
  exit 1
fi

if git diff --quiet -- $GEN_PATHS data/stream_cache.json 2>/dev/null; then
  echo "= 변경 없음 — 커밋·배포 건너뜀"
  exit 0
fi

# ⚠️ 생성물만 담고 소스(scripts/gen_site.py · data/products.json)를 빼면 안 된다.
#    소스가 커밋되지 않으면 다른 세션·기기의 재빌드가 옛 소스로 생성해 **조용히 회귀**한다
#    (2026-08-01 Flipper 교보 SAM 탭에서 발견). 생성물과 소스는 항상 같이 커밋한다.
git add -A $GEN_PATHS assets scripts data _redirects 2>/dev/null
git commit -q -m "chore(stream): 자동 재빌드 — 제품 피드 갱신 $(date '+%Y-%m-%d')" || echo "  (커밋할 것 없음)"

# SEO/GEO 점검 — docs/SEO_GEO.md 의 집행부.
# ⚠️ 배포를 막지 않는다(경고만). 매일 도는 자동 빌드를 SEO 결함으로 죽이면
#    사이트가 통째로 낡는 게 더 큰 손해다. 사람이 로그를 보고 고친다.
python3 scripts/seo_check.py || echo "  ⚠️ SEO 점검 미달 — docs/SEO_GEO.md §3 참조 (배포는 계속)"

if npx --yes wrangler deploy; then
  echo "✅ 배포 완료"
  # IndexNow — **6개 사이트 전체**의 바뀐 URL 을 네이버·빙에 통지한다(구글은 안 받는다).
  #   사이트마다 배포 방식이 달라(워커·Pages·Vercel·launchd) 각각 붙이면 갈라진다.
  #   여기 한 곳에서 매일 훑는다. 안 바뀐 건 안 보낸다 — 전량 재전송은 스팸이다.
  echo "───────── IndexNow"
  node scripts/indexnow_push.mjs || echo "  🟠 IndexNow 실패 — 배포는 이미 끝났다"
  # 로컬에만 남으면 다음에 다른 곳에서 옛 상태로 배포할 수 있다 → 올려서 항상 같게 유지.
  git push -q origin main 2>/dev/null && echo "  ↑ origin 동기화 완료" || echo "  ⚠️ push 실패 — 수동 확인 필요"
else
  echo "❌ 배포 실패 — 커밋은 남아 있음(다음 실행에서 재시도)"
  exit 1
fi
