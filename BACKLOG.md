# 모멘터스 백로그

> 지금 안 해도 되지만 잊으면 안 되는 것.

## Flipper — 앱 안 링크를 새 경로로 (2026-08-24)

Flipper 를 `/apps/` → `/products/` 로 승격하면서 앱 안에 박힌 링크가 옛 주소로 남았다.
지금은 **301 리다이렉트**가 받아 주고 있어 깨지지 않는다.

- 앱: `the-moment.us/apps/flipper*` → `the-moment.us/products/flipper*` 로 치환
  (특히 메인 하단 '잘 안 넘어가나요? 도움받기' → support)
- 앱이 새 주소로 나가면 `scripts/gen_site.py` 의 `/apps/<slug>/*` 301 블록을 지운다.

**급하지 않다.** 다운로드가 아직 0건이라, 며칠 안에 앱이 업데이트되면
구버전을 쓰는 사람이 사실상 없다. 리다이렉트를 오래 들고 갈 이유가 없어질 뿐이다.

요청서: `flipper_app_spec.md` (서고 발행분)
