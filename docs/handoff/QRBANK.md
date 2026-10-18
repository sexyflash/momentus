# QR Bank 편입 준비 (2026-10-18)

> QR Bank 세션(M4)이 개발 중인 서비스를 모멘터스 제품 목록에 올리기 위한 준비 문서다.
> **아직 공개하지 않았다.** `data/products.json`에는 넣지 않았다. 넣는 순간 매일 05:45 재빌드가 바로 공개한다.

## 1. 기존 사이트 구조 (실측)
- 저장소: `~/Projects/momentus` (GitHub `sexyflash/momentus`, apex `the-moment.us`). 정본 문서는 `docs/PRODUCT_SYSTEM.md`.
- 제품 하나 = `data/products.json`의 `products.<slug>` 한 항목 + `order` 배열의 slug 한 줄.
  - `scripts/gen_site.py`가 이 항목으로 아래를 전부 만든다.
    - 소개 페이지 `/products/<slug>/`
    - 제품 목록·랜딩 카드
    - 1단 바 '더보기'
    - 푸터·sitemap·JSON-LD
  - HTML을 손으로 만들지 않는다.
- 최신 사례는 팀AI(`teamai`)다. `type: service`·`cta: ext`이고, 자기 서브도메인(`teamai.the-moment.us`)으로 내보내는 CTA가 하나 있다. QR Bank도 같은 모양이다.

## 2. 추천 최종 URL
| 무엇 | 주소 |
|---|---|
| 소개 페이지 (apex, 생성물) | `https://the-moment.us/products/qrbank/` |
| 서비스 (QR Bank 워커) | `https://qr.the-moment.us` — 고객 `/` · 사장님 `/merchant` · 조사 `/research-report` |

- **서브도메인을 쓰는 이유:**
  - 인쇄한 QR은 한 번 붙이면 주소를 못 고친다. 그래서 그 주소를 QR Bank가 혼자 영구히 소유해야 한다.
  - 짧을수록 QR 모듈이 적어 작게 인쇄해도 잘 찍힌다.
- **도메인 이름에 `bank`를 넣지 않는 이유:** 아래 4번 참고.
- 지금 시험 주소 `qr-bank-test-1018.reci-cdn.workers.dev`는 다른 워커 계정(reci-cdn)이다. 편입할 때 모멘터스 Cloudflare 계정의 the-moment.us 존에 사용자 지정 도메인으로 붙인다. DNS를 손으로 만들지 않는다.

## 3. GA 연결 방식
- **소개 페이지(apex):** 생성기가 apex 속성 `G-1T66ZV28MB`를 자동으로 붙인다. 별도 작업은 없다.
  - '서비스 열기' 클릭은 기존 outbound 이벤트로 남는다(`link_kind=product`).
  - 2026-10-18부터 outbound의 `link_url`에서 `#` 뒤를 잘라 보낸다(`scripts/gen_site.py`).
- **서비스(qr.the-moment.us):** apex 속성과 섞지 않는다. 마크·큐처럼 **QR Bank 전용 속성**을 새로 만든다. 만드는 일은 GA 관리 화면에서 사람이 해야 한다.
- **보내면 안 되는 것:** 계좌번호, 예금주, 금액, URL fragment(`#…`). 서비스에서는 다음을 지킨다.
  1. **고객 화면 `/`에는 GA를 넣지 않는 것을 추천한다.** 계좌 정보가 주소에 실리는 화면이다.
     넣어야 한다면 아래 세 가지를 모두 지킨다.
     - `gtag('config', ID, {send_page_view:false})`로 설정한다.
     - `page_view`는 `page_location: location.origin + location.pathname`으로 직접 보낸다. 쿼리와 `#`는 빼고, `page_referrer`도 같은 식으로 자른다.
     - 해당 스트림의 '향상된 측정 → 브라우저 기록 이벤트 기반 페이지 변경'을 끈다.
  2. **사장님 화면 `/merchant`:** 입력값(계좌·예금주·금액)을 이벤트 매개변수에 넣지 않는다.
     - 허용 이벤트 예: `qr_issue`(매개변수 `amount_mode`: fixed/open/…), `template_pick`(`a4`/`a2`), `export`(`png`/`svg`/`print`).
     - 은행 코드처럼 개인을 식별하지 않는 값만 싣는다.
  3. **고객 화면에서 은행 앱 열기 시도**를 재고 싶다면 `bank_open`(`bank` = 은행 코드)만 보낸다. 성공 여부는 웹에서 알 수 없으니 '열기 시도'로만 이름 붙인다.

## 4. 브랜드 표기
- 회사 표기는 **모멘터스(MOMENTUS)**다. 「모멘텀스」가 아니다. 사이트 푸터·제목 모두 「모멘터스」·「MOMENTUS」를 쓴다.
- 한 줄 문구는 「순간순간을 소중하게」, 강조색은 `#3182f6`이다.
- 공용 토큰은 `https://the-moment.us/assets/momentus.css`다. 값을 복사하지 말고 링크로 참조한다.
- 제품명 초안은 「QR Bank · 계좌 QR」(짧은 이름 `QR Bank`)이다.
- **확인 필요(법률):** 은행법 제14조는 은행이 아닌 자가 상호에 '은행'을 쓰지 못하게 한다.
  - 영문 'Bank'·'뱅크'가 여기에 걸리는지는 확인하지 못했다.
  - 공개 전에 대표 결정 또는 자문을 받는다. 바뀔 수 있으므로 도메인에는 넣지 않았다.
- 문구 원칙: QR Bank는 송금을 실행하지 않는다. '송금 성공', '결제' 같은 말을 쓰지 않는다. 은행 앱 열림은 은행별 실기기 확인 전이라는 것을 그대로 적는다.

## 5. 준비된 것
- `data/handoff/qrbank_product_entry.json` — `products.json` 항목 초안(소개 문구·특징·사용법·FAQ).
  - `data/`는 배포 제외라 공개되지 않는다.
- 렌더 확인: 별도 작업 사본에서 항목을 넣고 `gen_site.py`를 돌렸다.
  - `/products/qrbank/`가 생성됐다. 제목은 「QR Bank · 계좌 QR — MOMENTUS」, canonical은 `https://the-moment.us/products/qrbank/`, GA는 apex 속성이다.
  - 390px와 1440px에서 가로 넘침과 스크립트 오류가 없었다(헤드리스 크롬).
  - **문제:** 제품 이미지(`shot`·`shots`)가 없으면 템플릿이 다른 제품(플래너) 사진으로 빈자리를 채운다. 실제 QR Bank 화면 이미지가 꼭 필요하다.
- `scripts/gen_site.py`의 outbound 이벤트가 `#` 뒤를 보내지 않게 고쳤다.

## 5-1. 2026-10-18 실측 (시험 주소 /merchant, 헤드리스 크롬)
- 고객 링크 형식: `/#r=<base64url JSON>`. JSON 키는 bankCode·bankName·account(숫자만)·owner·mode·amount·shop·item이다. **계좌·예금주·금액이 # 뒤에 있다.**
- 금액 3방식 × 디자인 3종 × A4/A2 × 390/1440 조합에서 오류 0건, 가로 넘침 0.
- PNG·SVG 저장이 되고, QR을 디코딩한 값이 고객 링크와 같다.
- 수정 배포 뒤 재확인: A4는 210×297, A2는 420×594로 각각 한 장이다. 인쇄 버튼과 Ctrl+P가 같은 인쇄물을 낸다.
- 브랜드 표기 「모멘터스」 반영, 공용 CSS 링크 반영, 외부 요청은 momentus.css 하나뿐.
- 화면 안내는 「입력한 계좌는 이 브라우저에 보관돼요. QR 링크를 가진 사람은 계좌 정보를 볼 수 있어요.」다. 이 문구로 FAQ 저장 답을 채웠다.

## 6. 개발 인계 때 받아야 할 것
1. GitHub 저장소 URL·커밋·실행법, 배포 대상(워커 이름·계정), 최종 경로(`/`·`/merchant`·`/research-report`)
2. ~~계좌·금액 위치~~ → `#r=`로 확인됨(5-1). 고객 화면 `/`에는 GA를 넣지 않는다.
3. ~~계좌 저장 위치~~ → 화면 안내와 실측으로 채웠다(5-1). 코드로 한 번 더 확인한다.
4. 우리 자산인 실제 화면 이미지 4~6장: 사장님 발행 화면, A4/A2 인쇄물, 고객 은행 선택 화면. 각각 `shot` 1장과 `shots`가 된다.
5. 가격(무료/유료). 지금 초안은 `free:false`(목록에 '제품'으로 표시)다.
6. 은행별 실기기 확인 현황(확인된 은행 수). FAQ 문구는 이 수치로만 고친다.

## 7. 공개 절차 (인계 받은 뒤)
1. 초안의 `__SERVICE_URL__`과 `__PRIVACY_ANSWER__`를 채운다.
2. `data/products.json`의 `products`에 `qrbank`를, `order`에 `"qrbank"`를 넣는다. 랜딩 카테고리 단어가 필요하면 `KB_WORD`에도 한 줄 넣는다.
3. `python3 scripts/gen_site.py`를 돌리고 로컬에서 `/products/qrbank/`를 390px·데스크톱으로 확인한다.
4. 서비스 도메인이 외부에서 200을 돌려주는지 먼저 확인한 다음 커밋·배포한다. 소개 페이지 CTA가 죽은 주소를 가리키면 안 된다.
