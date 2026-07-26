#!/bin/bash
# the-moment.us 자동 재빌드 — 제품 피드(스트림)를 매일 다시 긁어 랜딩을 갱신한다.
#   호출: launchd(com.sexyflash.momentus-rebuild) 매일 05:45. 수동 실행도 가능.
#   안전장치
#     · 생성 실패하면 배포하지 않는다(깨진 사이트를 올리지 않는다).
#     · 변경이 없으면 커밋·배포를 건너뛴다(빈 배포 금지).
#     · 커밋만 하고 origin push 는 하지 않는다(푸시는 사장님 결정).
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1

echo "───────── $(date '+%Y-%m-%d %H:%M:%S') 재빌드 시작"

if ! python3 scripts/gen_site.py; then
  echo "❌ 생성 실패 — 배포하지 않고 중단"
  exit 1
fi

if git diff --quiet -- index.html stories tools products about legal apps sitemap.xml data/stream_cache.json 2>/dev/null; then
  echo "= 변경 없음 — 커밋·배포 건너뜀"
  exit 0
fi

git add -A index.html stories tools products about legal apps sitemap.xml assets data/stream_cache.json _redirects 2>/dev/null
git commit -q -m "chore(stream): 자동 재빌드 — 제품 피드 갱신 $(date '+%Y-%m-%d')" || echo "  (커밋할 것 없음)"

if npx --yes wrangler deploy; then
  echo "✅ 배포 완료"
else
  echo "❌ 배포 실패 — 커밋은 남아 있음(다음 실행에서 재시도)"
  exit 1
fi
