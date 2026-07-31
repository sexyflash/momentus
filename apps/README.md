# `apps/` — 프로덕션 생명줄만 남긴 폴더 (2026-08-01 정리)

> 여기 남은 파일은 **전부 외부 스토어·설치된 확장이 실시간으로 참조하는 주소**다.
> 사이트 생성기(`scripts/gen_site.py`)가 만들지 않고, sitemap에도 없고, 1단 바에서도 안 보인다.
> **"안 쓰는 것 같다"고 옮기거나 지우면 프로덕션이 죽는다.** 옮기기 전 이 문서를 읽어라.

## 절대 건드리면 안 되는 것

| 경로 | 누가 부르나 | 옮기면 |
|---|---|---|
| `chatpage/remote-config/*.json` (3개) | **설치된 ChatPage 크롬 확장이 실행 중에 조회** | 확장이 설정을 못 읽음. 사용자 기기에서 즉시 고장 |
| `legal.html` | **크롬 웹스토어 등록 정보** | 스토어 정책 위반 → 등록 취소 위험 |
| `privacy-policy.html` | **크롬 웹스토어 + Flipper(Android) 개인정보처리방침** | 위와 같음. Flipper 조항(§1.4)도 여기 있다 |
| `timer/support-page.html` | **맥 App Store 「포모도로 타이머」 지원 URL** | 애플 심사 리젝 사유 |

⚠️ `wrangler.jsonc`의 `html_handling: "auto-trailing-slash"` 때문에 `.html` 직링크는 **307로 확장자 없는 주소에 보내진다**. 스토어가 참조하는 URL이라 배포 후 반드시 최종 200을 실측할 것 (`curl -sL`).

## 옮긴 것 (2026-08-01)

레거시 앱 랜딩 6종을 저장소 밖으로 뺐다. 작업트리 **1.4GB → 681MB**.

```
/Volumes/Seagate Backup/Projects/momentus-legacy/
    pion/ (724MB) · dokdo/ · kidup/ · naver-talk-hub/ · openspot/ · quickpang/
```

- 778개 파일 전부 크기·개수 대조 확인 후 이동.
- 옛 주소는 `_redirects`로 회수한다(`gen_site.py` 하단에서 생성). **손으로 `_redirects`를 고치지 마라.**
  - `/apps/quickpang/*` → `/tools/quickpang/` — 퀵팡만 외부 유입이 살아 있다(1만+).
    드래그 버튼 payload가 `/tools/quickpang/`와 바이트 동일(14,796자)임을 실측하고 넘겼다.
  - 나머지 5종 → `/` (대체재 없음. 방문자에게 404보다 홈이 낫다)
- ⚠️ **`/apps/*` 같은 광역 리다이렉트 규칙을 절대 쓰지 마라.** 위 생명줄 4개가 한 번에 죽는다.
  규칙은 반드시 슬러그별로 쓴다.

## 새 네이티브 앱 페이지를 만들 때

여기에 손으로 HTML을 놓지 마라. `data/products.json`에 한 줄 추가하고 `gen_site.py`를 돌린다
(카드·1단 바·푸터·sitemap·JSON-LD가 자동 생성된다). 근거: `docs/PLATFORM_TOPOLOGY.md` §9.
