# SEO / GEO 지침 — 모멘터스 전 도메인 정본

> **이 문서가 정본이다.** 페이지를 새로 만들거나 `<head>` 를 건드리기 전에 여기부터 읽어라.
> 여기에 없는 SEO 규칙을 개별 저장소에 따로 적지 마라 — 폴리레포라 금방 갈라진다.
> 적용 범위: `the-moment.us`(apex) · `notes.` · `cue.` · `mark.` · `pay.` · `heyreci.com` **전부**.
>
> 실측 기준일: **2026-08-07**. 숫자를 인용할 땐 이 날짜를 같이 적어라.
> 관련: [PRODUCT_SYSTEM.md](PRODUCT_SYSTEM.md) §5(전시 두 층) · [INFORMATION_ARCHITECTURE.md](INFORMATION_ARCHITECTURE.md) · [PLAN_SHELL.md](PLAN_SHELL.md) §44

---

## §0. 먼저 — 흔한 오해 하나를 정정한다

> "우리 페이지가 JSON을 fetch 해서 그리니까 크롤러가 못 읽는다"

**apex(`the-moment.us`)에는 해당하지 않는다.** 2026-08-07 실측으로 apex 32개 생성 페이지 전부
`fetch()` 호출 **0건**이고, 본문이 초기 HTML 에 서버 렌더로 박혀 있다. `data/products.json` 은
**빌드 타임에 Python 이 읽는다**(`scripts/gen_site.py:20`) — 런타임 fetch 가 아니다.

단, **정확히는 "본문을 그리는 fetch 가 0건"**이다. `/tools/quickpang/` 에는 `fetch(` 문자열이 2건
잡히는데(`tools/quickpang/index.html:77,103`) 그건 `href="javascript:…"` 안의 **북마클릿 페이로드**라
페이지 렌더와 무관하다. 문자열 grep 으로 판정하지 말고 §5 의 방법을 써라.

이 오해가 생긴 진짜 출처는 **notes/pay 쪽 SPA** 다. 거기는 실제로 `fetch("/api/shop")` →
`innerHTML` 패턴이었고, 봇이 보는 텍스트가 **356자**였다. 2026-08-04 에
`~/Projects/notes/web/src/seo.js` 로 서버 프리렌더를 붙였지만 — **절반만 고쳐졌다.**
2026-08-07 실측으로 `notes/p/orbit-planner` 는 아직 **753자(본문 344자)**다. §5 표를 봐라.

**그래도 "JS 렌더 때문에 구글에 안 잡힌다"는 지금의 주된 원인이 아니다.**
안 잡히는 1순위 원인은 **§11 — GSC 속성이 아예 등록된 적이 없다**는 것이고,
페이지 쪽 결함은 §1 이다. 원인을 잘못 짚으면 안 고쳐도 될 걸 고치게 된다.

---

## §1. 상태판 (2026-08-07)

✅ 는 오늘 고쳐 **로컬에 반영**된 것이다. **아직 배포 전이라 라이브는 옛 상태다**(§12-2).

| # | 빠진 것 | 영향 범위 | 무슨 손해 | 심각도 |
|---|---|---|---|---|
| 1 | ✅ **해결(2026-08-07)** — `og:image` | apex 33페이지 전부 + notes 전 페이지 | 카톡·슬랙·X 에 링크를 붙이면 **썸네일 없는 회색 카드**. 클릭률이 직접 깎인다 | 🔴 |
| 2 | ✅ **해결** — `twitter:card` | 같은 범위 | X·디스코드에서 큰 카드로 안 펼쳐짐 | 🔴 |
| 3 | ✅ **해결** — 페이지 유형별 JSON-LD(`_schema_for()`) | apex 33페이지 전부(블록 md5 동일) | 제품에 `Product`/`SoftwareApplication`, 글에 `Article`, 리스트에 `ItemList` 가 없음 → 리치 결과·AI 인용 자격 상실 | 🔴 |
| 4 | ✅ **해결** — 빈 태그 `noindex`+sitemap 제외(자동) | 태그 7개 중 **4개가 글 0건**(`kontext`·`heyreci`·`cue`·`theplan`), `tools`·`mark` 1건, `people` 3건 | 빈 페이지가 sitemap 에 올라가 있음. 크롤 예산 낭비 + 사이트 품질 신호 하락 | 🟠 |
| 5 | **sitemap 에 `lastmod` 없음** | apex·cue·heyreci | 재크롤 우선순위 신호를 못 줌. notes(`seo.js:192,195`)는 이미 냄 | 🟠 |
| 6 | **`makesOffer` 4개 하드코딩** | `gen_site.py:1276-1281` | `products.json` 파생이 아님 → 새 제품 추가해도 스키마에 안 들어감. "한 줄 추가" 원칙 위반 | 🟠 |
| 7 | **`/apps/legal.html` 이 `/legal/terms/` 와 동일 콘텐츠인데 각자 자기참조 canonical** | apex 2페이지 | 중복 콘텐츠 신호가 갈림 | 🟠 |
| 8 | **`stories/rss.xml` 이 어디에도 선언 안 됨** | apex | `<link rel="alternate">` 0건 + sitemap 미등록 → 사실상 없는 파일 | 🟡 |
| 9 | ✅ **해결** — `apps/timer/support-page.html` | 1페이지 | `lang="en"`, description·canonical·JSON-LD 전무 (손관리 레거시) | 🟡 |
| 10 | **`products.json` 공개 엔드포인트 미구현** | 사이트 전체 | `.assetsignore` 가 `data/` 를 배포 제외 중. 에이전트가 읽을 기계용 카탈로그가 없음 | 🟡 |
| 11 | **`h1` 중복** | notes **전 페이지 7~8개**, cue 4개, apex 랜딩 3개 | 문서 주제가 흐려짐 | 🟡 |
| 12 | ✅ **해결** — `description` 자동 생성(`_re_desc()`) | 무료 도구 6개 전부 **15~22자**, `/apps/legal.html` 10자 | 구글이 무시하고 본문에서 임의 발췌한다 | 🟠 |
| 13 | ✅ **해결** — `og:type`·`og:site_name`·`og:locale` | apex 33페이지 전부 | 글이 `article` 로 안 잡힘 | 🟡 |
| 14 | **구글 소유확인 수단 자체가 없다** | 저장소·`<head>` 양쪽 모두 | 네이버 파일만 있다. **§11 참조 — 이게 "안 잡히는" 1순위 원인이다** | 🔴 |

**이미 잘 돼 있는 것 (건드리지 마라)**

- apex 전 페이지 완전 정적 서버 렌더 — 본문을 그리는 `fetch()` 0건. `PLAN_SHELL.md:44` 결정이 지켜지고 있다
- `canonical`/`og:url` 후처리 일괄 주입(`gen_site.py:3057-3092`) — 새 페이지가 자동으로 받는 구조. **개별 페이지에 canonical 을 손으로 넣지 마라, 덮어써진다**
- `robots.txt` 가 AI 봇 5종을 명시 허용 + `Sitemap:` 선언. **이 파일을 지우면 Cloudflare 가 자기 안내문을 자동 주입한다**(2026-08-04 실측: 지시문 0줄, Sitemap 선언 0줄)
- `pay.the-moment.us` 는 `noindex,nofollow` + `Disallow: /` — notes 와 내용이 같아 의도적 차단. **색인시키지 마라**
- `/l/*` 는 302 + `Cache-Control: no-store`, sitemap 의도적 제외 — 내용 없는 이정표다

---

## §2. SEO 와 GEO 는 다른 게임이다 — 섞지 마라

| | **SEO** (구글·네이버) | **GEO/AEO** (ChatGPT·Claude·Perplexity·AI 개요) |
|---|---|---|
| 누가 읽나 | 크롤러 → 색인 → 랭킹 | LLM 이 **그 자리에서 읽고 요약·인용** |
| 이기는 법 | 백링크·권위·체류시간 누적 | **답이 페이지에 그대로 박혀 있는가** |
| 순위 개념 | 있다(1~10위) | 없다. **인용되거나 안 되거나** |
| 반응 속도 | 수 주~수 개월 | 크롤 즉시 |
| 결정적 요소 | 도메인 권위 | **원자 단위 답변 + 구조화 데이터 + 다출처 반복 언급** |

**우리 현실:** 신생 도메인이라 SEO 권위 싸움은 당장 못 이긴다.
**GEO 가 우리가 실제로 이길 수 있는 판이다.** 그래서 `robots.txt` 에서 AI 봇을 막지 않고
**의도적으로 허용**하고 있다. 이 결정을 뒤집지 마라.

⚠️ **단, 과투자 금지선** (`PRODUCT_SYSTEM.md:166` 재확인):
`llms.txt` 에 올인하거나 거대 스키마를 짜는 데 시간을 쓰지 마라.
GEO 의 진짜 동력은 **페이지 밖 다출처 반복 언급**이다. 페이지 안에서 할 일은 §3~§6 이 전부다.

---

## §3. 모든 페이지가 반드시 갖춰야 할 것 — 필수 9종

새 페이지를 배포하기 전 **9개 전부** 있어야 한다. 하나라도 없으면 배포하지 마라.

```html
<!-- 1. 언어 — ko 고정. 영어 페이지가 아니면 lang="en" 금지 -->
<html lang="ko">

<!-- 2. title — 60자 이내. "핵심어 — 맥락 | 브랜드" 꼴. 페이지마다 반드시 달라야 한다 -->
<title>네이버 채용 공고 39건 — 네이버 면접 예상질문 | Cue</title>

<!-- 3. description — 70~120자. 이 페이지에서만 얻을 수 있는 것을 적어라 -->
<meta name="description" content="NAVER 진행 중 채용공고 39건과 면접 예상질문. 공고만 보지 말고, 그 공고로 바로 AI 모의면접까지.">

<!-- 4. canonical — apex 는 빌드 후처리가 자동 주입한다(손대지 마라).
     다른 저장소는 직접 넣되 절대 URL + 배포 URL 과 정확히 일치해야 한다 -->
<link rel="canonical" href="https://cue.the-moment.us/company/naver">

<!-- 5. Open Graph 6종 — og:image 가 핵심이다 -->
<meta property="og:type"      content="website">      <!-- 글이면 article -->
<meta property="og:site_name" content="MOMENTUS">
<meta property="og:locale"    content="ko_KR">
<meta property="og:title"     content="(title 과 같게)">
<meta property="og:description" content="(description 과 같게)">
<meta property="og:url"       content="(canonical 과 같게)">
<meta property="og:image"     content="https://…/og/naver.png">  <!-- 절대 URL 필수 -->

<!-- 6. Twitter Card 2종 (X·디스코드·슬랙이 읽는다) -->
<meta name="twitter:card"  content="summary_large_image">
<meta name="twitter:image" content="(og:image 와 같게, 절대 URL)">

<!-- 7. JSON-LD — 페이지 유형에 맞는 스키마. §4 표 참조 -->
<script type="application/ld+json">{"@context":"https://schema.org","@graph":[…]}</script>

<!-- 8. viewport (모바일 우선 색인의 전제) -->
<meta name="viewport" content="width=device-width, initial-scale=1">

<!-- 9. 문자셋 — head 최상단 1024바이트 안에 -->
<meta charset="utf-8">
```

### og:image 규격

| 항목 | 값 |
|---|---|
| 크기 | **1200 × 630 px** (1.91:1). 이보다 작으면 카톡이 작은 카드로 떨어뜨린다 |
| 최소 | 600 × 315 px |
| 용량 | 300KB 이하 (카톡 파서가 큰 파일에서 타임아웃) |
| 포맷 | PNG 또는 JPG. **WebP·SVG 금지** — 카톡·네이버가 못 읽는다 |
| URL | **반드시 절대 URL**(`https://`). 상대경로면 대부분의 파서가 무시한다 |
| 글자 | 넣어도 되지만 **핵심 정보를 이미지에만 두지 마라** — 에이전트가 못 읽는다 |
| 위치 | `/og/<slug>.png`. 페이지별 고유가 원칙, 최소한 도메인 기본값 1장은 있어야 한다 |

> 카톡·슬랙은 og 를 **캐시한다.** 이미지를 바꿔도 즉시 반영 안 된다.
> 카톡은 [디버거](https://developers.kakao.com/tool/debugger/sharing) 에서 캐시를 밀어야 한다.

---

## §4. 페이지 유형별 JSON-LD — 정본 표

`@graph` 배열에 `Organization` + **그 페이지의 실제 타입**을 같이 넣는다.
**apex 는 `gen_site.py` 의 `_schema_for()` 가 경로로 유형을 판별해 자동 생성한다** — 참고 구현이다.
다른 저장소는 이 표를 보고 직접 넣어라.

| 페이지 유형 | `@type` | 필수 필드 | 현재 상태 |
|---|---|---|---|
| 랜딩 | `Organization` + `WebSite` | `name, url, email, inLanguage, publisher` | ✅ apex 자동 |
| 유료 제품 상세 | `Product`/`SoftwareApplication` + `Offer` | `name, description, image, brand, offers{availability, url, seller}` — **가격은 아는 것만** | ✅ apex·notes 자동 |
| 웹앱 / 무료 도구 | `SoftwareApplication` | `name, applicationCategory, operatingSystem, offers{price:"0", priceCurrency:"KRW"}` | ✅ apex 자동 |
| 네이티브 앱 | `MobileApplication` | `name, description, operatingSystem, image` | ✅ apex 자동 |
| 블로그 글 | `BlogPosting` | `headline, datePublished, dateModified, author, image, publisher, mainEntityOfPage` | ✅ apex 자동 |
| 리스트 / 허브 / 태그 | `CollectionPage` + `ItemList` | `mainEntity.itemListElement[{position, url, name}]` — **본문 링크에서 뽑는다** | ✅ apex 자동 |
| FAQ 가 있는 페이지 | `FAQPage` | `mainEntity[{Question, acceptedAnswer}]` | ✅ cue `/company/*` 만 |
| 하위 경로 전부 | `+ BreadcrumbList` | `itemListElement[{position, name, item}]` | ✅ apex·cue·mark |
| 소개 | `AboutPage` | `name, description, url, mainEntity` | ✅ apex 자동 |
| 법적 문서·기타 | `WebPage` | `name, description, url, inLanguage` | ✅ apex 자동 |

### 절대 규칙 4가지

1. **화면에 없는 걸 스키마에 적지 마라.** 구글 스팸 정책 위반이고, 걸리면 리치 결과가 **영구 박탈**된다. `aggregateRating` 을 리뷰 없이 넣는 게 가장 흔한 사고다 — 넣지 마라.
2. **가격은 실제 결제 금액과 일치해야 한다.** `pay.the-moment.us` 의 sku 가격이 정본이다. 다르면 구글이 상품 노출을 끊는다.
3. **`@graph` 로 묶어라.** `<script>` 를 여러 개 흩뿌리는 것보다 파싱이 안정적이다.
4. **하드코딩 금지.** 스키마는 `products.json` 파생이어야 한다. 지금 `gen_site.py:1276-1281` 의 `makesOffer` 4개가 손으로 적혀 있는데, 이게 §9 의 "제품 추가 = 한 줄" 원칙을 깨고 있다.

### 좋은 예 (notes 가 이미 하고 있는 것 — apex 가 따라가야 할 기준)

```json
{"@context":"https://schema.org","@graph":[
  {"@type":"Organization","name":"모멘터스","alternateName":"MOMENTUS",
   "url":"https://the-moment.us","email":"hello.momentus@gmail.com"},
  {"@type":"Product","name":"오르빗","description":"중학생을 위한 무료 학습 노트",
   "image":["https://notes.the-moment.us/img/…/draft_user_cover.png"],
   "brand":{"@type":"Brand","name":"notes"},
   "offers":{"@type":"Offer","price":"0","priceCurrency":"KRW",
     "availability":"https://schema.org/InStock",
     "url":"https://notes.the-moment.us/p/orbit-planner",
     "seller":{"@type":"Organization","name":"모멘터스"}}}
]}
```

---

## §5. 초기 HTML 규칙 — 봇은 JS 를 돌리지 않는다

이게 이 문서에서 제일 중요한 절이다.

> **크롤러와 LLM 은 초기 HTML 만 읽는다.**
> 구글은 JS 를 실행하긴 하지만 **렌더링 큐가 따로 돌아 수일~수주 지연**된다.
> **AI 봇(GPTBot·ClaudeBot·PerplexityBot)은 JS 를 아예 안 돌린다.**
> JS 로 그린 콘텐츠는 GEO 에서 **존재하지 않는 것과 같다.**
> — `INFORMATION_ARCHITECTURE.md:92` · `PLAN_SHELL.md:44`

### 판정하는 법 — `sed` 한 줄로 재지 마라 (2026-08-07 사고)

```bash
python3 scripts/seo_check.py --live --domain <도메인>     # ← 이걸 써라
```

브라우저 개발자도구의 Elements 탭을 보지 마라 — 그건 **JS 실행 후**다. 봇이 보는 건 `curl` 결과다.

⚠️ **한 줄 `sed` 로 재면 틀린 답이 나온다.** 이 문서가 처음에 아래 명령을 처방했다가 사고를 냈다:

```bash
# 🚫 쓰지 마라 — 여러 줄에 걸친 <script> 를 못 지운다
curl -sL "<URL>" | sed 's/<script[^>]*>.*<\/script>//g; s/<[^>]*>/ /g' | tr -s ' ' ' ' | wc -c
```

`sed` 는 **줄 단위**라 여는 `<script>` 와 닫는 `</script>` 가 다른 줄에 있으면 아무것도 안 지운다.
그러면 **JS 소스코드가 본문 글자수로 잡혀** 실제의 3~90배가 나온다.
실측: `/stories/tag/mark/` 가 sed 로는 2,590자, 실제로는 **589자**.
`notes/p/orbit-planner` 는 sed 로 40,052자, 실제로는 **753자** — 이 오측 때문에
"notes 는 넉넉하다"는 정반대 결론이 이 문서에 한 번 실렸다.

정확히 재려면 **비탐욕 정규식 + `re.S`** 여야 한다 (`scripts/seo_check.py` 의 `visible_text()`).

### 통과 기준

| 페이지 유형 | 최소 가시 텍스트 | 목표 |
|---|---|---|
| 제품 상세 · 글 | **1,000자** | 2,000자+ |
| 리스트 · 허브 | **600자** | 1,000자+ |
| 법적 문서 | 1,000자 | — |

**2026-08-07 실측 — 전 도메인이 기준 미달이다.** 이게 이 문서에서 가장 나쁜 발견이다.

| URL | 가시 텍스트 | 본문(`main`)만 | 판정 |
|---|---:|---:|---|
| `notes/p/orbit-planner` | **753** | **344** | 🔴 유료 플래너 상세가 344자 |
| `notes/products` | 881 | 476 | 🔴 |
| `cue/jobs` | 746 | — | 🔴 JSON-LD 도 0건 |
| `the-moment.us/stories/tag/cue/` | **485** | 43 | 🔴 apex 최저 |
| `the-moment.us/stories/tag/mark/` | 589 | 146 | 🔴 |
| `the-moment.us/tools/` | 735 | 293 | 🟠 |
| `the-moment.us/products/cue/` | 917 | 469 | 🟠 |
| `the-moment.us/products/heyreci/` | 968 | 517 | 🟠 |
| `the-moment.us/stories/why-free/` | 1,358 | 908 | ✅ |
| `cue/blog` | 2,806 | — | ✅ |
| `cue/company/naver` | 3,730 | — | ✅ 최고 |

**`notes` 의 프리렌더는 절반만 고쳐졌다.** `seo.js` 가 붙기 전 356자였는데 지금 344~476자다.
장치는 들어갔지만 **내보내는 본문이 여전히 거의 없다.** "고쳤다"고 적힌 채 방치돼 있었다 —
유료 상품을 파는 페이지가 봇에게는 문단 두 개짜리로 보인다. §12 우선순위 3번이다.

**`cue/company/naver` 가 유일하게 잘 된 예다.** 이 페이지 구조를 다른 상세 페이지에 복제해라.

### 반드시 서버 HTML 에 있어야 하는 것

- **`<h1>` 1개** — 페이지당 정확히 하나. `notes` 는 **전 페이지가 7~8개**다(`/p/*` 만의 문제가 아니다). apex 랜딩 3개, cue 4개
- 본문 전체와 소제목(`h2`/`h3`) 계층
- **내비게이션 링크** — 크롤러는 링크를 따라 발견한다. `shell.js` 가 그리는 바에만 의존하지 마라. apex 는 이미 서버 렌더로 박고 있다
- 가격·스펙·FAQ 같은 사실 정보
- 이미지 `alt` 텍스트

### JS 로 채워도 되는 것

- 상호작용 UI (탭 전환, 모달, 아코디언 **내용은 HTML 에 두고 접기만 JS**)
- 개인화·로그인 상태 표시
- 무한 스크롤의 **2페이지 이후** (1페이지는 HTML 에)

### SPA 저장소는 프리렌더가 의무다

`notes`/`pay` 처럼 SPA 인 곳은 `~/Projects/notes/web/src/seo.js` 방식을 따르되 **거기서 멈추지 마라** —
서버가 `<main id="app">` 에 본문 + JSON-LD 를 심고 클라이언트가 덮어쓰는 progressive enhancement 인데,
notes 는 장치만 넣고 **본문을 344자밖에 안 내보내서 사실상 미해결이다**(§5 표).
`noindex` 는 `seo.js` 가 아니라 `index.js:79`·`pay_app.js:33` 에 있다.
**새 SPA 를 이 장치 없이 배포하지 마라. 넣었으면 §5 기준을 넘는지 재라.**

---

## §6. 본문 작성 규칙 (GEO — AI 가 인용하게 만드는 법)

AI 는 **잘라서 인용할 수 있는 덩어리**를 찾는다. 문단이 길고 주어가 흐리면 인용이 안 된다.

1. **질문형 헤딩 + 40~60단어 답.** 사람이 검색창에 치는 말 그대로 `h2` 로 쓰고, 바로 아래에 그것만으로 완결되는 답을 놔라.
   ```html
   <h2>큐는 무료인가요?</h2>
   <p>큐의 모의면접 연습은 무료입니다. 회원가입 없이 바로 시작할 수 있고,
      질문 생성과 음성 답변 연습에 비용이 들지 않습니다. 2026년 8월 기준입니다.</p>
   ```
2. **정량·날짜를 박아라.** "많은 기업"이 아니라 "채용공고 39건(2026-08-07 기준)". 숫자가 있는 문장이 인용된다.
3. **첫 문단이 전부다.** 페이지 맨 위 2~3문장 안에 "이게 뭐고 누구를 위한 것인가"를 끝내라. AI 는 앞부분에 가중치를 준다.
4. **대명사 대신 고유명사.** "이 서비스는" → "큐는". AI 가 문단을 떼어내도 주어가 살아 있어야 한다.
5. **시맨틱 HTML.** `<article> <section> <h2> <ul> <table> <dl>`. `div` 범벅은 구조를 못 준다.
6. **이미지 안에 정보를 넣지 마라.** 가격표·비교표를 이미지로 만들면 에이전트가 못 읽는다. HTML `<table>` 로 써라. (`PRODUCT_SYSTEM.md:164`)
7. **FAQ 는 화면에도 보이게.** `FAQPage` 스키마만 넣고 화면에 없으면 §4 절대규칙 1 위반이다.

---

## §7. 사이트 단위 자산 — 도메인마다 4개

| 파일 | 필수 | 규칙 |
|---|---|---|
| `/robots.txt` | ✅ **전 도메인** | `Allow: /` + AI 봇 5종 명시 허용 + `Sitemap:` 절대 URL. **없으면 Cloudflare 가 쓸모없는 자동 안내문을 주입한다** |
| `/sitemap.xml` | ✅ **전 도메인** | 생성물이어야 한다. `<lastmod>` 를 넣어라. **200 이 아닌 URL·noindex·리다이렉트를 넣지 마라** |
| `/llms.txt` | 권장 | 제품·가격·정책 요약. 현재 apex·cue·mark 만 있음. notes·heyreci **404** |
| RSS | 글이 있는 도메인 | `<link rel="alternate" type="application/rss+xml">` 로 **선언까지** 해야 한다 |

### 도메인별 현황 (2026-08-07 실측)

`python3 scripts/seo_check.py --live` 로 언제든 다시 뽑을 수 있다. 아래는 2026-08-07 실행 결과.

| 도메인 | robots | sitemap | llms.txt | canonical | og:image | twitter | JSON-LD |
|---|:---:|---|:---:|:---:|:---:|:---:|---|
| `the-moment.us` | ✅ | 30 URL · lastmod ❌ | ✅ | ✅ | ❌ | ❌ | ⚠️ Organization 만 |
| `notes.the-moment.us` | ✅ | 10 URL · lastmod ✅ | ❌ **404** | ✅ | ❌ | ❌ | ✅ Product+Offer |
| `cue.the-moment.us` | ✅ | **623 URL** · lastmod ❌ | ✅ | ✅ | ✅ | ✅ | ⚠️ 페이지마다 다름. `/company/*` 는 4종, **`/jobs`·`/blog` 는 0건** |
| `mark.the-moment.us` | ✅ | 색인형 → `sitemap-0.xml` 에 **1 URL** | ✅ | ✅ | ✅ | ✅ | ✅ 하위는 VisualArtwork+Breadcrumb+CollectionPage (홈만 Organization) |
| `heyreci.com` | ✅ | 110 URL · lastmod ❌ | ❌ **404** | ❌ **없음** | ✅ | ✅ | ❌ **0건** |
| `pay.the-moment.us` | ✅ Disallow | — | — | — | — | — | — (의도적 noindex) |

**`cue/company/*` 가 현재 최고 수준이다** — 스키마 4종 + 본문 3,730자. 다만 같은 도메인의 `/jobs` 는
JSON-LD 0건에 746자다. **도메인이 아니라 페이지 단위로 봐라. 어느 도메인도 균일하지 않다.**
**`heyreci.com` 이 제일 나쁘다** — 매출 나는 도메인인데 canonical 과 JSON-LD 가 둘 다 0이다.
**`apex` 는 URL 30개로 제일 작다** — 색인될 물량 자체가 적다는 뜻이기도 하다.

**`mark` 는 sitemap 에 URL 이 1개뿐이다** — 색인될 페이지가 첫 화면 하나라는 뜻이다.
"업종별 로고를 가장 많이 만든 곳"이라는 포지션에 비해 검색에 낼 표면이 없다. 업종별 랜딩이 필요하다.

`h1` 중복은 apex 랜딩 3개, cue 4개, notes 8개로 전 도메인 공통 문제다.

`cue` 첫 페이지의 `fetch('/data/jobs.json')` 은 **본문 렌더가 아니다** — 초기 HTML 에 이미 10,341자가
있고 이건 채용공고 수치를 갱신하는 보조 호출이다. 다만 **그 JSON 안의 공고 목록은 AI 봇에게 안 보인다.**
공고 건수 같은 인용 가능한 숫자는 빌드 타임에 HTML 로 구워라 (§6-2).

---

## §8. 하면 안 되는 것

1. **개별 페이지에 `canonical` 을 손으로 넣지 마라 (apex 한정).** `gen_site.py:3057-3092` 후처리가 덮어쓴다. 예외를 넣어야 하면 그 후처리 함수를 고쳐라.
2. **`index.html` 을 직접 수정하지 마라.** 매일 05:45 재빌드가 지운다. `scripts/gen_site.py` 에서만 고쳐라.
3. **`robots.txt` 를 지우지 마라.** Cloudflare 자동 주입본이 그 자리를 먹는다 (Sitemap 선언 0줄).
4. **AI 봇을 차단하지 마라.** `Disallow: GPTBot` 을 추가하는 순간 GEO 전략이 끝난다.
5. **`pay.the-moment.us` 를 색인시키지 마라.** notes 와 중복 콘텐츠다. `noindex` 를 풀지 마라.
6. **`/l/*` 를 301 로 바꾸지 마라.** 브라우저가 영구 캐시해서 링크 대상 변경이 안 먹는다. 302 + `no-store` 가 의도다 (`workers/link-redirect/index.js` — 이유는 14-16행 주석, 구현은 34·38행).
7. **없는 리뷰로 `aggregateRating` 을 넣지 마라.** 리치 결과 영구 박탈 사유다.
8. **빈 페이지를 sitemap 에 넣지 마라.** 글 0건인 태그 페이지가 지금 **4개**(`kontext`·`heyreci`·`cue`·`theplan`) 올라가 있다.
9. **키워드를 반복해 박지 마라.** 지금 AI 검색은 반복 빈도가 아니라 **답의 명확성**을 본다.
10. **핵심 정보를 이미지로만 두지 마라.** 에이전트가 못 읽는다.
11. **`title`/`description` 을 페이지마다 복붙하지 마라.** 중복은 구글이 색인에서 접는 직접 사유다.
12. **손관리 HTML 의 주석에 `/assets/site.css?v=` 를 쓰지 마라.** `gen_site.py` 후처리의 생성물 판별이
    단순 substring 검색이라 **주석에 있어도 생성물로 오인해 그 파일을 덮어쓴다.**
    (2026-08-07 실측: `apps/timer/support-page.html` 에 "이 파일엔 그 서명이 없다"고 적었더니
    그 문장 때문에 서명이 생겨 후처리 대상이 됐다.)

---

## §9. 새 페이지를 만들 때 — 절차

### apex (`the-moment.us`)

1. **HTML 을 손으로 만들지 마라.** 제품이면 `data/products.json` 에 한 줄 추가 → 카드·바·푸터·sitemap·JSON-LD 가 자동으로 따라온다 (`PRODUCT_SYSTEM.md:230`).
2. 새 유형이면 `scripts/gen_site.py` 에 빌더를 추가하고, `page()` 를 통과시켜라 — `<head>` 9종이 자동으로 붙는다.
3. `sitemap.xml` 생성부(`gen_site.py:2975-2986`)에 등록.
4. §4 표를 보고 그 유형의 JSON-LD 를 `head_extra` 로 넣어라.
5. `og:image` 를 `/og/<slug>.png` 로 만들어 넣어라 (1200×630).
6. `bash scripts/rebuild.sh` → §10 검증 → 배포.

### 다른 저장소 (notes·cue·mark·heyreci)

1. §3 의 9종을 직접 넣는다. 템플릿 함수 하나를 통과시키고, 페이지마다 복붙하지 마라.
2. SPA 면 §5 마지막의 프리렌더 장치가 **먼저** 있어야 한다.
3. 해당 도메인 `sitemap.xml` 에 등록.

---

## §10. 검증 — 배포 전에 이걸 돌려라

### 자동 점검기 (권장)

이 문서의 §3·§5·§7 을 기계로 검사한다. **지침이 문서로만 있으면 안 지켜진다 — 이게 집행부다.**

```bash
python3 scripts/seo_check.py                    # 저장소 생성물 전수 검사
python3 scripts/seo_check.py --live             # 라이브 5개 도메인
python3 scripts/seo_check.py --live --sitemap   # sitemap 의 전 URL 상태까지
python3 scripts/seo_check.py --live --domain heyreci.com
```

`FAIL` = 배포 기준 미달(종료코드 1). `warn` = 고쳐야 하지만 배포를 막지는 않음.
**2026-08-07 최초 실행 결과: 로컬 33개 페이지에서 FAIL 70건 · warn 101건.**
FAIL 의 대부분이 `og:image`(33) + `twitter:card`(33) 이다 — §12 우선순위 2번이 여기서 나왔다.

규칙을 바꿀 땐 **이 문서를 먼저 고치고** `scripts/seo_check.py` 를 맞춰라. 문서가 정본이다.

### 수동 확인 (개별 URL 을 급히 볼 때)

```bash
# 페이지 하나 전수 점검. URL 만 바꿔서 쓴다.
U="https://the-moment.us/products/cue/"; H=$(curl -sL "$U")
echo "title      : $(echo "$H" | grep -o '<title>[^<]*' | head -1)"
echo "desc       : $(echo "$H" | grep -c 'name=\"description\"')  (1이어야 함)"
echo "canonical  : $(echo "$H" | grep -o 'rel=\"canonical\"[^>]*')"
echo "og:image   : $(echo "$H" | grep -c 'og:image')  (1 이상)"
echo "twitter    : $(echo "$H" | grep -c 'twitter:card')  (1 이상)"
echo "JSON-LD    : $(echo "$H" | grep -c 'application/ld+json')  (1 이상)"
echo "h1         : $(echo "$H" | grep -c '<h1')  (정확히 1)"
echo "fetch()    : $(echo "$H" | grep -c 'fetch(')  (본문을 그리는 fetch 면 실패)"
echo "가시텍스트 : $(echo "$H" | sed 's/<script[^>]*>.*<\/script>//g; s/<[^>]*>/ /g' | tr -s ' \n' ' ' | wc -c) 자"

# 사이트 자산 4종
for p in /robots.txt /sitemap.xml /llms.txt /; do
  printf "%-14s %s\n" "$p" "$(curl -s -o /dev/null -w '%{http_code}' "https://the-moment.us$p")"
done

# sitemap 의 전 URL 이 200 인지 (리다이렉트·404 가 섞이면 크롤 예산을 태운다)
curl -s https://the-moment.us/sitemap.xml | grep -o '<loc>[^<]*' | cut -d'>' -f2 | \
  while read u; do echo "$(curl -s -o /dev/null -w '%{http_code}' "$u") $u"; done | grep -v '^200'

# JSON-LD 파싱 검증
curl -sL "$U" | python3 -c "
import sys,re,json
for m in re.findall(r'<script type=\"application/ld\+json\">(.*?)</script>',sys.stdin.read(),re.S):
    d=json.loads(m); print('OK', [i.get('@type') for i in (d.get('@graph') or [d])])"
```

**외부 검증 도구** (배포 후 반드시 한 번씩)

| 확인할 것 | 도구 |
|---|---|
| 구조화 데이터 문법 | [Rich Results Test](https://search.google.com/test/rich-results) |
| 카톡 공유 카드 | [카카오 디버거](https://developers.kakao.com/tool/debugger/sharing) |
| 봇이 보는 렌더 결과 | Search Console → URL 검사 → **테스트한 페이지 보기** |
| 슬랙 카드 | 아무 채널에 링크를 붙여 본다 |

---

### 2026-08-28 추가된 3종 (§17·§18)

```bash
# 유형별 표본 전수 검사 — 첫 페이지 1장만 보던 구멍을 메운다. 이걸 먼저 돌려라
python3 ~/bin/seo_check.py --live --domain <도메인> --pages 1

# 프로그래매틱 묶음 고유도 (40% 미만 경고 / 30% 미만 발행 금지)
python3 ~/bin/seo_check.py --uniq "https://<도메인>/<묶음경로>/"

# sitemap 전 URL — 이제 리다이렉트를 200 으로 속이지 않는다
python3 ~/bin/seo_check.py --live --domain <도메인> --sitemap
```

---

## §11. 구글 서치 콘솔에 안 잡히는 진짜 이유

**"페이지가 잘못 만들어져서"가 아니다.** apex 페이지들은 위 결함(og:image·스키마)을 빼면
색인 가능한 상태다. 색인이 안 되는 건 대개 이 순서다 — 위에서부터 확인해라.

1. **소유권 확인 + sitemap 제출을 안 했다.** 2026-08-07 실측 — 저장소에 네이버 소유확인 파일
   (`naver3fe771ebb904433f0e91a9067ec07ec0.html`)은 있는데 **구글 소유확인 파일도, `<head>` 의
   `google-site-verification` 메타도 0건이다.** 즉 GSC 속성이 애초에 없다.
   속성 등록 → `sitemap.xml` 제출부터 해야 한다. 이걸 안 하면 아무리 잘 만들어도 안 잡힌다.
2. **도메인이 신생이고 외부 링크가 거의 없다.** 구글은 링크가 없는 새 도메인을 천천히 크롤한다.
   sitemap 제출 후에도 **수 주**가 걸린다.
3. **서브도메인은 각각 별도 속성이다.** `the-moment.us` 를 등록해도
   `notes.`·`cue.`·`mark.` 는 **안 잡힌다.** 도메인 속성(DNS 인증)으로 등록하면 한 번에 커버된다 —
   이 방식을 권장한다. `heyreci.com` 은 별도 도메인이라 어차피 따로 등록해야 한다.
4. **`pay.` 가 안 잡히는 건 정상이다.** 의도적으로 막았다.
5. 그다음이 페이지 품질 문제(thin content 태그 페이지 등)다.

> **§1 을 고쳐도 GSC 등록을 안 하면 색인은 안 된다.** 두 개는 별개 작업이고, 순서는 등록이 먼저다.

---

## §12. 백로그 — 남은 일

> 2026-08-07 apex 작업분은 배포 완료(커밋 `122b012`). 아래는 **아직 안 한 것**이다.
> 착수 전 `python3 ~/bin/seo_check.py --live` 로 현재 상태부터 다시 재라 — 숫자가 낡았을 수 있다.

### 🔴 사람만 할 수 있는 것

- [ ] **구글 서치 콘솔 등록 + sitemap 제출.** 소유확인 수단이 저장소·`<head>` 양쪽에 0건이라
      GSC 속성이 아예 없다. **이게 "검색에 안 잡힌다"의 1순위 원인이다**(§11).
      → **도메인 속성(DNS 인증)** 으로 등록하면 `notes.`·`cue.`·`mark.` 가 한 번에 커버된다.
      `heyreci.com` 은 별도 도메인이라 따로. sitemap: `https://the-moment.us/sitemap.xml`

### 🟠 매출 도메인 — 여기가 제일 아프다

- [ ] **`notes` 프리렌더 본문 늘리기.** `seo.js` 의 `seoBody()` 가 344자만 낸다.
      장치는 있는데 내용이 없어 유료 플래너가 봇에게 안 보인다. 점검기가 FAIL 로 잡는다.
      → `python3 ~/bin/seo_check.py --live --domain notes.the-moment.us`
- [ ] **`heyreci.com` 에 canonical + JSON-LD.** 둘 다 **0건**이다. 매출 도메인인데 기본이 없다.
- [ ] **`mark` 에 업종별 랜딩.** sitemap URL 이 **1개**뿐이라 검색에 낼 표면 자체가 없다.
      "업종별 로고를 가장 많이 만든 곳"이라는 포지션과 어긋난다. (별건, 크다)

### 🟡 마감 작업

- [ ] `cue` 의 `/jobs`·`/blog` JSON-LD 0건 보완 (623 URL 중 큰 축이 비어 있다)
- [ ] sitemap `lastmod` — apex·cue·heyreci 전부 없다 (notes 는 이미 냄)
- [ ] `stories/rss.xml` 을 `<link rel="alternate">` 로 선언 + sitemap 등록
- [ ] `h1` 1개로 정리 — apex 랜딩 3개(캐러셀 슬라이드), cue 4개, notes 7~8개
- [ ] `notes`·`heyreci` 에 `llms.txt` (GEO 보조. 기대치는 낮게 — §2 과투자 금지선)
- [ ] `products.json` 공개 엔드포인트 (`.assetsignore` 가 `data/` 를 막고 있다)
- [ ] `makesOffer` 하드코딩 4개를 `products.json` 파생으로 (`gen_site.py`)

### ✅ 2026-08-07 완료 (apex, 배포됨)

`og:image`(14장 자동생성) · `twitter:card` · `og:type/site_name/locale` ·
**페이지 유형별 JSON-LD**(`_schema_for()`, 35페이지) · **제품 FAQ 40개**(본문 + `FAQPage`) ·
`description` 자동생성(10~29자 → 70~120자) · 빈 태그 `noindex`+sitemap 제외 ·
별칭 canonical 통합 · 레거시 타이머 페이지 · 점검기·스킬·훅 ·
`rebuild.sh` 생성물 경로 단일화(`how-to-pay`·`i`·`inquiry` 가 커밋에서 누락돼 있었다)

결과: 점검기 **FAIL 70건 → 0건, warn 71건 → 4건**. 제품 상세 본문 917자 → 1,226~1,378자.

---

## §13. 어디서 어떻게 쓰는가 — 운영 모델

**한 곳에서 규칙을 관리하고, 각 저장소에서 그 도구를 부른다.** 폴리레포라 규칙을 복제하면 갈라진다.

| 자산 | 위치 | 역할 |
|---|---|---|
| **정본 문서** | `~/Projects/momentus/docs/SEO_GEO.md` (이 파일) | 규칙의 유일한 출처. 저장소마다 복붙 금지 |
| **점검기** | `~/bin/seo_check.py` | **모든 저장소에서 동작.** `cd` 해서 그냥 돌리면 된다 |
| **전역 스킬** | `~/.claude/skills/seo-page/` | 어느 프로젝트에서 페이지 작업을 하든 자동 발동 |
| **momentus 스킬** | `momentus/.claude/skills/seo-page/` | 전역의 momentus 전용 보충판(자동화 목록·금지사항) |
| **momentus 훅** | `momentus/.claude/settings.json` | `*.html`·`gen_site.py`·`products.json` 수정 시 자동 점검 |

### 쓰는 법 — 저장소별로 다르다

**momentus** — "제품 추가해줘" / "페이지 만들어줘" 라고만 하면 된다.
`products.json` 한 줄이면 페이지·OG이미지·JSON-LD·sitemap·llms.txt 가 전부 자동으로 따라온다.
`<head>` 는 손댈 일이 없다.

**notes·cue·mark·heyreci·kontext** — 아직 수동이다. 전역 스킬이 발동해 규칙을 읽어 오지만,
`<head>` 와 JSON-LD 는 그 저장소의 템플릿에 **직접 넣어야 한다.**
`python3 ~/bin/seo_check.py --live --domain <도메인>` 으로 검증해라.

> 각 저장소를 momentus 수준으로 올리려면 **템플릿 함수 하나 + 후처리 한 곳**을 만들어라.
> `gen_site.py` 의 `page()` + `_schema_for()` 가 참고 구현이다. 페이지마다 복붙하면 반드시 빠뜨린다.

### 왜 아무것도 막지 않나

전역 원칙대로 deterministic 게이트는 **오발동해도 손해 0** 인 자리에만 둔다.
SEO 결함으로 매일 도는 빌드를 죽이면 사이트가 통째로 낡는 게 더 큰 손해다.
훅과 `rebuild.sh` 는 경고만 하고, 판단은 사람이 `seo_check.py` 출력을 보고 한다.

### 점검기를 고칠 때

`momentus/scripts/seo_check.py` 가 원본이다. 고친 뒤 `cp scripts/seo_check.py ~/bin/` 로 동기화해라.
(두 벌이 갈라지면 저장소마다 다른 기준으로 검사하게 된다.)

---

## §14. 이 문서를 고칠 때

- 실측 없이 숫자를 바꾸지 마라. §10 의 명령을 돌리고 **날짜와 함께** 적어라.
- 사고가 나면 "사고 → 가드 룰"로 §8 에 한 줄 추가해라. 그게 이 저장소의 축적 방식이다.
- 개별 저장소에 SEO 규칙을 따로 적지 마라. 여기로 링크해라.

---

# 2부 — 2026-08-28 증축분 (§15~§20)

> 계기: `claude-seo`(⭐15.5k, MIT) 를 뜯어 **우리가 안 하고 있던 것만** 추려 정본으로 올렸다.
> 도구를 깔라는 얘기가 아니다. 우리 자산에 실제로 대보고 숫자가 나온 것만 규칙이 됐다.
> §1~§14 는 "페이지 한 장이 갖출 것"이다. **2부는 "사이트를 운영하는 법"이다.**

## §15. 필자를 사람으로 만들어라 — 우리가 제일 크게 흘리고 있는 것

**사고(2026-08-28 실측):** `cue/playbook/*` 의 `Article.author` 가 `{"@type":"Organization","name":"Cue"}` 였다.
우리 글의 유일한 차별점은 **"20년 넘게 사람을 뽑고 면접을 봐온 사람이 쓴다"** 인데,
구글에게도 LLM 에게도 그 사람은 **존재하지 않는 상태**로 39편이 나가 있었다.

구글의 1차 heuristic 은 `Who / How / Why` 세 질문이다
(developers.google.com/search/docs/fundamentals/creating-helpful-content).
`Who` 에 답이 없으면 E-E-A-T 의 **Experience·Expertise 두 칸이 통째로 비어 있는 것**과 같다.
그리고 Trust 가 넷 중 제일 무겁다는 것이 구글이 공개한 유일한 가중치 정보다.

### 규칙

1. **글이 있는 도메인은 `Person` 엔티티를 정확히 1개 갖는다.** 여러 명으로 늘리지 마라 — 실체가 없으면 들킨다.
2. `Article`·`BlogPosting` 의 `author` 는 **`Person`**, `publisher` 만 `Organization` 이다.
3. 그 `Person` 은 **실체 페이지**를 가진다(`/about` 안의 앵커라도 좋다). 스키마에만 있고 화면에 없으면 §4 절대규칙 1 위반이다.
4. `sameAs` 로 **밖의 우리**를 연결한다(브런치·링크드인·유튜브·X 중 실재하는 것만).
   AI 인용은 백링크(상관 0.266)보다 **브랜드 언급(유튜브 0.737)** 에 3배 더 붙는다(Ahrefs, 7.5만 브랜드).
   `sameAs` 는 흩어진 언급을 한 엔티티로 묶어주는 유일한 페이지 안 장치다.
5. 화면에는 **글당 한 번만** 드러낸다. 두 번 넘으면 권위 팔이로 읽힌다(`cue/CLAUDE.md` 와 같은 문장).

```json
"author": {
  "@type": "Person",
  "name": "<실명 또는 고정 필명>",
  "jobTitle": "채용·면접 20년",
  "description": "20년간 채용과 면접을 해온 사람. 지원자 편에서 쓴다.",
  "url": "https://cue.the-moment.us/about#writer",
  "sameAs": ["<링크드인>", "<유튜브>"]
}
```

🚫 **없는 자격을 지어내지 마라.** 우리 경험은 실재한다 — 그걸 그대로 적는 것으로 충분하다.
숫자·기관명을 보태는 순간 §9 금지선(경험을 통계로 위장) 위반이다.

**적용 대상:** cue(39편·즉시) · notes · heyreci · mark(작업 사례 글이 생기면). apex 는 제품 도메인이라 해당 없음.

---

## §16. 신선도는 태그가 아니라 프로그램이다

**사고(2026-08-28 실측):** cue 글의 `Article` 에 `datePublished` 도 `dateModified` 도 **둘 다 없다.**
sitemap 611 URL 에 `lastmod` 도 없다. 즉 **우리 사이트는 언제 쓴 글인지 아무도 모른다.**

3개월 미만 콘텐츠는 AI 답변에 인용될 확률이 약 3배, 6개월 방치되면 인용 자격을 잃는다
(SE Ranking, 130만 인용 분석). 우리는 **하루 두 번 크롤하고 4시간마다 발행하는** 사이트다.
신선도는 우리가 이미 갖고 있는 자산인데 **날짜를 안 적어서 못 쓰고 있었다.**

### 규칙

1. 글 스키마에 `datePublished` + `dateModified` **둘 다** 넣는다(ISO 8601, KST 오프셋 포함).
2. **화면에도 보이게** 한다. 스키마에만 있으면 안 된다.
3. sitemap `<lastmod>` 는 **실제 내용이 바뀐 시각**이다. 빌드 시각을 넣지 마라 —
   매 배포마다 611개가 전부 갱신됐다고 거짓말하면 크롤러가 lastmod 를 믿지 않게 된다.
4. **분기 1회 갱신 루프.** 유입 상위 10편을 다시 읽고, 사실이 바뀐 곳을 고치고, 고친 것만 `dateModified` 를 올린다.
5. 🚫 **날짜만 바꾸지 마라.** 내용 변경 없는 날짜 갱신은 구글이 `content churn` 으로 분류하는 패턴이다
   (helpful-content 가이드의 `Why` 실패 사례). 우리 §9 금지선과 같은 정신이다.

**우리 구조에서의 이점:** 공고 데이터가 매일 바뀐다 → `/job/*`·`/company/*` 는 **자동으로 신선하다.**
`lastmod` 를 원장의 `first_seen`/갱신 시각에 연결하면 496장이 공짜로 신선도 신호를 얻는다.

---

## §17. 프로그래매틱 페이지 — 자로 재고, 나눠서 내라

**사고(2026-08-28):** cue 는 `/job/*` **496장**을 사실상 한 번에 냈고,
**아무도 고유도를 재본 적이 없었다.** 배치 규칙(50~100장) 위반이다.

> ⚠️ **이 숫자는 하룻밤에 세 번 바뀌었다. 자를 못 믿으면 숫자도 못 믿는다.**
> ① 연속 6장 표본 → 최저 39.5% (표본을 붙은 것으로만 뽑아 과소평가)
> ② 균등 8장 표본 → 최저 48.8% (`--uniq` 로 교정)
> ③ **나브·푸터 제외 → 최저 59.2%** ← **이게 맞는 값이다.**
> §17 은 처음부터 "공유 헤더·푸터·나브는 계산에서 제외한다"고 적혀 있었는데
> **구현이 그걸 안 지키고 있었다**(§22-6). 크롬이 클수록 고유도가 실제보다 낮게 나와,
> 멀쩡한 묶음을 '발행 금지선 아래'로 오판한다. 실제로 `/company/*` 를 26.9% 로 잘못 찍었다.

구글의 `Scaled Content Abuse` 정책(2024-03 도입)은 2025-06 에 대량 수동조치로 집행됐다.
프로그래매틱 페이지는 **양이 아니라 고유도**로 죽는다.

### 게이트 — 숫자로 막는다

| 지표 | 기준 | 조치 |
|---|---|---|
| 페이지 간 고유도 | **≥ 40%** | 미만이면 WARN — 템플릿에 고유 섹션을 더해라 |
| 페이지 간 고유도 | **< 30%** | 🛑 **발행 금지.** 레코드를 묶어 상위 페이지 하나로 합쳐라 |
| 생성 페이지 수 | 100장 초과 | 표본 **5~10% 사람 검수** 후 발행 |
| 생성 페이지 수 | 500장 초과 | 🛑 명시적 승인 필요 |
| 배치 크기 | **50~100장씩** | 2~4주 색인·순위를 보고 다음 배치 |

**고유도 계산:** 나브·푸터를 제거한 가시 텍스트의 **5-gram 집합**을 만들고,
같은 묶음의 다른 페이지와 겹치는 비율을 뺀다. 템플릿 문구는 **고유도에 포함시키지 않는다**(그게 보일러플레이트다).
```bash
python3 ~/bin/seo_check.py --uniq "https://cue.the-moment.us/job/"    # 표본 자동 추출·측정
```

### 이 페이지 하나만 있어도 낼 만한가

프로그래매틱 페이지 한 장을 놓고 **"비슷한 페이지가 하나도 없었어도 이걸 발행했을까"** 를 물어라.
답이 "아니오"면 그건 페이지가 아니라 **목록의 행**이다. 목록으로 합쳐라.

### 우리 자산 적용

**2026-08-28 전수 실측 (크롬 제외 · 균등 표본). 전 묶음 게이트 통과.**

| 묶음 | 규모 | 평균 | 최저 | 판정 |
|---|---:|---:|---:|---|
| `cue/job/*` | 496 | 90.0% | 59.2% | ✅ 단 **496장 일괄 발행**은 배치 규칙 위반이었다 |
| `cue/company/*` | 49 | 93.0% | 63.4% | ✅ |
| `cue/role/*` | 8 | 91.1% | 77.9% | ✅ |
| `cue/prep/*` | 8 | 75.1% | 70.5% | ✅ 보일러플레이트 16.3% 로 이 중 제일 높다 |
| `mark/insights/*` | 174 | 93.9% | 64.3% | ✅ |
| `mark` 업종별 랜딩 | **22 (이미 있다)** | 79.9% | 65.1% | ✅ "업종명만 바꾼 페이지"가 아니다 — 실제 시안이 페이지마다 다르다 |
| `mark` 작업 상세 | 670 | 69.4% | 56.6% | ✅ |

> 🚫 **"mark 는 검색에 낼 표면이 없다"는 앞선 기술은 오독이었다**(§22-3).
> 실제로는 773 URL 이고 업종별 랜딩도 22장 이미 살아 있다.

---

## §18. 회귀를 감시해라 — 우리는 사람이 안 보는 사이에 배포된다

**사고(2026-08-28 실측):** 2026-08-03 에 `/blog` 를 `/insights` 로 통합했는데,
**sitemap 은 아직 `/blog` 를 싣고 있다.** `/blog` 는 301 이고 `/insights` 는 sitemap 에 없다.
25일간 아무도 몰랐다. `crawler/crawl.mjs` 가 매 실행 끝에 `wrangler deploy` 를 돌기 때문에
**사람이 안 보는 사이에 하루 두 번 배포된다.**

**더 나쁜 것은 점검기가 그걸 정상이라고 보고했다는 점이다.** `seo_check.py` 가
리다이렉트를 따라가서 `/blog` 를 **200 으로 보고**했고, 라이브 검사는 **첫 페이지 1장만** 봤다.
611장 중 1장. 그래서 글 39편은 한 번도 검사된 적이 없었다.
**둘 다 2026-08-28 에 고쳤다**(`--pages`, `follow=False`). 고친 직후 같은 사이트에서
**FAIL 0건 → FAIL 15건**이 나왔다.

> 🚨 **자가 못 재는 것은 없는 것이 아니라 안 보이는 것이다.**
> 점검기가 통과를 주면 통과의 범위를 먼저 의심해라.

SEO 결함은 배포 순간에 안 보인다. **다음에 누가 볼 때까지 그대로 산다.**

### 규칙

1. **URL 구조를 바꾼 커밋은 sitemap 생성기를 같이 고친 커밋이어야 한다.** 하나만 고치면 반드시 어긋난다.
2. sitemap 에 **리다이렉트·404·noindex 를 넣지 마라.** 크롤 예산을 태우고, 통합했다는 신호를 지운다.
3. **주 1회 전수 점검을 사람 없이 돌린다.**
   ```bash
   python3 ~/bin/seo_check.py --live --domain <도메인> --sitemap
   ```
4. 스냅샷 비교 대상 12종: `status` · `title` · `description` · `canonical` · `meta robots` ·
   `h1[]` · `h2[]` · JSON-LD `@type[]` · `og:*` · sitemap URL 집합 · sitemap `lastmod` · RSS 항목 수.
   **CRITICAL**(status·canonical·robots·JSON-LD 소실) / **WARN**(title·desc·h1 변경) / **INFO**(h2·og).
5. 🚫 **배포를 막지 마라.** §13 원칙대로 경고만 한다. 낡은 사이트가 더 큰 손해다.

---

## §19. 페이지 유형이 검색 의도와 맞는가 (SXO)

기술 점수 100점이어도 **유형이 틀리면 안 올라간다.**
어떤 키워드의 상위 10개가 전부 도구·비교표인데 우리만 에세이면, 아무리 잘 써도 못 뚫는다.

### 규칙 — 글을 쓰기 전에 30초만 쓴다

1. 노리는 검색어로 실제 검색해서 **상위 10개의 페이지 유형**을 센다
   (정보성 글 / 비교표 / 목록 / 도구·계산기 / 제품 / 커뮤니티 글).
2. 우세 유형이 60% 넘으면 **그 유형으로 쓴다.** 40~60% 면 섞인 판이라 각도로 이길 수 있다.
3. 우리 유형이 소수파면 **글을 잘 쓰는 게 아니라 형식을 바꾸는 게 답이다.**
4. `People Also Ask` 에 뜨는 질문들이 **그대로 우리 `h2`** 다(§6-1 과 같은 규칙).

**cue 적용:** '면접 예상질문' 계열은 상위가 목록·도구형이 많다.
우리는 에세이(`/playbook/*`)와 도구(`/job/*` 예상질문)를 **둘 다 갖고 있다** — 유형이 맞는 쪽으로 내부링크를 몰아라.

---

## §20. 1차 출처 정정 (2026-08-28) — 낡은 상식 5개를 버린다

| 버릴 것 | 실제 | 우리가 할 일 |
|---|---|---|
| `FAQPage` 를 넣으면 리치결과가 뜬다 | **2026-05-07 부로 전 사이트 FAQ 리치결과 종료.** SERP 이득 0 | 이미 있는 건 **두되**(`cue/company/*`·`/faq`), 리치결과 목적의 **신규 추가 금지**. 진짜 사용자 Q&A 는 `QAPage` |
| `llms.txt` 가 AI 인용을 늘린다 | 구글 공식(2026-05-15 도입, 06-15 명확화): **구글 검색에 도움도 해도 안 된다** | 비구글 봇용으로만 유지. §2 의 과투자 금지선이 옳았다 — 시간 더 쓰지 마라 |
| 단어 수가 랭킹 요소다 | 아니다. 커버리지 **바닥선**일 뿐 | §5 의 최소 글자수는 그대로 쓰되 "채우기" 하지 마라 |
| AI 노출을 막는 전용 파일이 있다 | 없다. `noindex`·`nosnippet`·`max-snippet`·`data-nosnippet` 로만 제어 | 특정 문단을 AI 요약에서 빼려면 `data-nosnippet` |
| `HowTo`·`SpecialAnnouncement`·`ClaimReview` 스키마 | 전부 폐기(2023-09 / 2025-07 / 등) | §4 표에 넣지 마라 |

### §2 표 정정 — "다른 게임"이 아니라 "같은 신호, 다른 표면"

구글 공식 입장은 **"AEO·GEO 는 SEO 를 다시 이름 붙인 것"** 이다.
AI 개요(AI Overviews)는 **기존 랭킹에 종속**된다 — 순위가 안 나오면 인용도 안 된다.
다만 **AI 모드·ChatGPT·Perplexity 는 별개 표면**이다(AI 모드와 AI 개요가 같은 URL 을 인용하는 비율 **13.7%**, Ahrefs 54만 쿼리쌍).
거기선 순위보다 **신선도·엔티티 권위·인용 가능한 문단**이 이긴다.

> **정정된 우리 전략:** "GEO 가 우리가 이길 판" 이라는 §2 의 결론은 **유효하다.**
> 단, 이유가 바뀐다 — 별개 학문이라서가 아니라, **AI 모드·ChatGPT 계열이 순위 약결합 표면이라
> 신생 도메인도 인용 풀에 들어갈 수 있기 때문**이다. 그래서 §15(사람)·§16(신선도)·§6(인용 가능한 문단)
> **셋이 우리 전부**다. 백링크 사냥에 시간 쓰지 마라 — 상관계수 0.266 이다.

### AI 봇 명시 허용은 전 도메인이다

apex `robots.txt` 에만 GPTBot·OAI-SearchBot·ClaudeBot·PerplexityBot·Google-Extended 5종 명시가 있고
**cue·mark 에는 없다**(2026-08-28 실측). `Allow: /` 로 기술적으로는 허용되지만,
정책을 명시하지 않으면 다음에 누가 `Disallow` 를 넣을 때 막을 근거가 없다.
**전 도메인 같은 블록을 넣어라.**

> ⚠️ `ChatGPT-User`·`Google-Agent`·`Google-NotebookLM` 은 **사용자 트리거라 robots.txt 를 무시한다.**
> 이들을 막으려면 서버단 접근제어뿐이다. 우리는 막을 이유가 없다.

---

## §21. 2026-08-28 전 도메인 실측 + 실행 결과

**새 자로 다시 쟀다.** 이전 표(§7)는 "첫 페이지 1장"만 본 숫자다. 아래가 유형별 표본 기준이다.

### 결과 (2026-08-28 야간 작업 후 · 전부 배포·라이브 재측정 완료)

| 도메인 | FAIL | warn | 무엇을 했나 |
|---|---|---|---|
| `the-moment.us` (apex) | **2 → 0** | 0 → **0** | 랜딩 `h1` 신설(sr-only) · sitemap `lastmod` · RSS 선언 |
| `cue.the-moment.us` | **15 → 0** | 16 → **4** | §15 필자 Person·§16 날짜(40편) · 목록 스키마 · sitemap `/insights`+lastmod 519 · AI봇 · h1 정리 · **홈 공고 섹션 프리렌더** |
| `mark.the-moment.us` | **3 → 0** | 4 → **2** | h1 3개 신설 · 페이지 유형별 스키마 5종 · AI봇 5종 · `twitter:description` · **sitemap lastmod 628** · 글 `updated` 지원 |
| `notes.the-moment.us` | **7 → 0** | 28 → **2** | SPA 4경로 서버 본문 · **유료 제품 40장 서버 본문**(344→1,681자) · `/orders` noindex · 경로별 고유 meta · 페이지 유형 스키마 |
| **합계 (이 머신 4개)** | **27 → 0** | 48 → **8** | |
| `heyreci.com` | 12 | 11 | 🛑 **고쳐뒀으나 미배포** — `~/Projects/heyreci`(2026-08-28 clone). Vercel 프로덕션이라 사람 승인 필요 |

> ⚠️ **앞 표(전 49건)의 mark 숫자는 틀렸다.** 점검기가 `sitemapindex` 를 안 따라가
> URL 773개를 "1개"로 읽었고, 그 오독이 "검색에 낼 표면이 없다"로 적혔다. 아래 §22 참조.

### 이번 작업에서 제일 컸던 것

**"카피는 이미 있는데 JS 로만 그려서 봇이 못 읽던 것"** 이 두 군데 있었다.
새로 쓴 글은 한 줄도 없다 — 있는 것을 서버 HTML 로 옮겼을 뿐이다.

| 어디 | 전 | 후 |
|---|---|---|
| `notes/p/*` (유료 제품 **40장**) | 344자 | **1,681자** |
| `cue` 홈 공고 섹션 | 공고 목록 **0** | 851건·10개사·카드 12장 |

§5 는 처음부터 "봇은 JS 를 안 돌린다"고 적혀 있었고, `cue/CLAUDE.md` 도
"공고 건수 같은 인용 가능한 숫자는 빌드 타임에 HTML 로 구워라"고 적어 두고 있었다.
**규칙이 없어서가 아니라 안 지켜서 생긴 손해였다.**

### 사이트 자산 4종 — 4개 도메인 전부 충족

| | robots(AI봇 5종) | sitemap `lastmod` | llms.txt | RSS 선언 |
|---|:--:|:--:|:--:|:--:|
| apex | ✅ | ✅ 4 | ✅ | ✅ |
| cue | ✅ | ✅ 519 | ✅ | ✅ |
| notes | ✅ | ✅ 41 | ✅ | ✅ |
| mark | ✅ | ✅ 628 | ✅ | ✅ |

`lastmod` 는 **0 → 1,192개**가 됐다. 전부 내용에서 나온 날짜다 — 🚫 빌드 시각 금지(§16-3).

**프로그래매틱 고유도는 전 묶음 통과다**(§17 표). 템플릿을 손볼 일은 없고,
남은 건 "한 번에 500장씩 내지 말 것"이라는 **발행 방식**뿐이다.

### 남은 warn 8건 — 전부 정체가 확인된 것

- cue 2 · notes 1 = `author.sameAs` 없음 / `author` 가 Person 이 아님 → **사람 결정 대기**
- cue 2 = 홈 공고 섹션의 **갱신용** fetch. 내용은 이미 서버에 구워져 있다(점검기는 스크립트 존재만 본다)
- mark 2 = `/explore`·`/find` 클라이언트 필터 (작업물은 각자 색인 페이지가 있다)
- notes 1 = `/insights` 목록 480자 (글이 아직 적다)

### 남은 일 — 사람이 정해야 진행되는 것

> 위 계획(cue → heyreci → mark → notes → apex)은 **2026-08-28 야간에 전부 실행됐다.**
> 아래가 그 뒤에 남은 것이다.

| # | 남은 것 | 왜 사람이 필요한가 |
|---|---|---|
| 1 | **heyreci 배포** | `~/Projects/heyreci` 에 canonical(`alternates.canonical:'./'` 한 줄로 전 페이지) · JSON-LD 3종 · AI봇 5종 · `llms.txt` 라우트를 넣어뒀다. 바뀐 파일 3개. **Vercel 이라 push 가 곧 프로덕션 배포**다 |
| 2 | **필자 `sameAs` URL** | 실재하는 링크드인·브런치·유튜브 주소가 필요하다. AI 인용은 백링크(0.266)보다 브랜드 언급(유튜브 0.737)에 3배 붙고, `sameAs` 가 그걸 한 엔티티로 묶는 **페이지 안의 유일한 장치**다. 🚫 없는 걸 지어내지 마라 |
| 3 | **notes 글의 필자** | 확정된 바가 없어 `Organization` 으로 뒀다. 사람으로 세울지 결정 필요(§15) |
| 4 | **notes 제품 카피** | `/insights` 목록이 480자다. 글이 쌓이면 자연히 해소된다 |

### 자동으로 도는 것 — 손 안 대도 유지된다

| 언제 | 무엇 | 어디 |
|---|---|---|
| 글이 새로 나올 때마다 | 필자·날짜·스키마·바이라인·sitemap `lastmod` 가 자동으로 붙는다 | 템플릿 단일 소스 |
| 배포 직전 (하루 2회 자동 포함) | 정적 페이지 머리부 + 홈 공고 섹션 프리렌더 주입 | `cue/scripts/sync-seo.mjs` |
| 배포 직후 (하루 2회) | `--pages 1` 자체 점검. **경고만 — 배포를 막지 않는다**(§13) | `cue/crawler/crawl.mjs` |
| 매주 월 08:00 | 5개 도메인 전수 + 프로그래매틱 고유도 | `momentus/scripts/seo_weekly.sh` → `cue/crawler/data/seo_weekly.log` |

> 2026-08-28 실증: 03:10 자동 발행된 새 글이 **사람 손 하나 없이** `Person 박진이` + 날짜 +
> 화면 바이라인 + sitemap `lastmod` 를 갖추고 나왔다.

### 사람만 할 수 있는 것 (여전히 1순위)

> ⚠️ **정정(2026-08-28):** 이 자리에 "GSC 등록이 1순위"라고 오래 적혀 있었는데 **틀렸다.**
> `cue.the-moment.us` 는 이미 **도메인 속성으로 등록돼 있고 사이트맵도 2026-07-19 에 제출**돼
> 정상 처리(성공, 619 URL 발견)되고 있었다. 2026-08-07 에 적힌 항목을 확인 없이 계속 옮겨
> 적으면서 남은 유령이다. §22-4("자를 고치면 그 자로 잰 과거 숫자를 전부 다시 재라")를
> 문서 항목에도 똑같이 적용해라 — **낡은 할 일은 낡은 숫자보다 더 오래 산다.**

- [ ] **구글 색인 API 서비스계정 키** (`cue/scripts/GINDEX_SETUP.md`, 10분)
      **이게 지금 진짜 1순위다.** 키 하나가 두 개를 연다:
      ① `/job/*` 495장을 매 크롤마다 구글에 **즉시 푸시**(IndexNow 는 구글에 안 간다)
      ② `scripts/gsc.mjs` 로 **색인 현황·노출·검색어를 사람 없이 읽는다**
      ②가 없으면 "뭐가 색인됐나"를 알려면 매번 사람이 GSC 화면을 열어야 한다 —
      그 왕복이 "결과만 기다리면 되는 상태"를 막는 마지막 병목이다.
- [ ] `notes`·`mark`·apex 도 GSC 속성 상태 확인 (cue 처럼 이미 돼 있을 수 있다 — **추측하지 말고 봐라**)

### 다시 재는 법

```bash
for d in the-moment.us cue.the-moment.us notes.the-moment.us mark.the-moment.us heyreci.com; do
  echo "### $d"; python3 ~/bin/seo_check.py --live --domain $d --pages 1 2>&1 | tail -3
done
```

---

## §22. 점검기를 믿기 전에 — 자가 틀린 적이 오늘만 여덟 번이다

2026-08-28 하룻밤에 `seo_check.py` 에서 **결함 8개**가 나왔다. 전부 "통과인데 통과가 아닌" 종류다.
**우리가 본 숫자는 사이트의 상태가 아니라 자의 상태였다.**

| # | 결함 | 무엇을 잘못 말했나 |
|---|---|---|
| 1 | 라이브 검사가 **첫 페이지 1장**만 봤다 | cue 611장 중 1장. 글 40편은 한 번도 검사된 적이 없었다 → `--pages` |
| 2 | 리다이렉트를 **따라가서 200 으로** 보고 | sitemap 의 `/blog`(301)를 25일간 '정상'이라고 했다 → `follow=False` |
| 3 | **sitemapindex 를 안 따라감** | mark 773 URL 을 "1개"로 읽었다. 그 오독이 정본에 "표면이 없다"로 적혔다 → `sitemap_locs()` |
| 4 | **따옴표 없는 속성**(`<html lang=ko>`)을 못 읽음 | notes `/insights` 를 lang·description·canonical·viewport **4종 전부 없음**으로 오판. 넷 다 있었다 → `Q()`/`QV()` |
| 5 | `ROOT` 가 **스크립트 위치** 기준 | `~/bin/seo_check.py` 로 돌리면 홈 전체(8,294 파일)를 훑어 FAIL 26,342 → `Path.cwd()` |
| 6 | `--uniq` 가 **나브·푸터를 포함**해서 쟀다 | §17 본문은 "제외한다"인데 구현이 안 지켰다. `/company/*` 를 **26.9%**(발행 금지선 아래)로 오판 — 실제 **63.4%** → `content_text()` |
| 7 | SPA 검사만 **800자가 따로** 박혀 있었다 | §5 표는 허브 600자다. **같은 도구가 601자 페이지를 통과이면서 동시에 FAIL** 로 판정했다 → `min_text_for()` 공유 |
| 8 | `h1` 을 **`<script>` 안까지** 셌다 | 인라인 JS 가 마크업 문자열을 들면 그게 h1 으로 잡힌다. notes 는 DOM h1 1개인 페이지가 **8개**로 찍혔다 → `STRIP_SCRIPT` 적용 |

### 그래서 규칙

1. 🚨 **통과를 받으면 통과의 범위를 먼저 의심해라.** "FAIL 0" 은 "결함이 없다"가 아니라
   "이 자가 본 범위에는 없다"는 뜻이다. cue 는 `--pages` 를 붙이는 순간 0 → 15 가 됐다.
2. **점검기가 이상하다고 하면 대상보다 점검기를 먼저 의심해라.** 오늘 오탐이 정탐보다 많았다.
   §21 백로그에 "mark 는 표면이 없다"가 적힌 것도, "notes 는 canonical 이 없다"가 적힌 것도 오탐이었다.
3. **정규식으로 HTML 을 읽을 땐 세 형태를 다 받아라** — `attr="값"` · `attr='값'` · `attr=값`.
   따옴표는 HTML5 에서 **선택**이다.
4. **점검기를 고치면 그 자로 잰 과거 숫자를 전부 다시 재라.** 낡은 숫자가 정본에 남으면
   그게 다음 사람의 작업 지시가 된다. 오늘 §21 을 두 번 고쳐 쓴 이유다.
5. 자를 고친 커밋은 **무엇이 어떻게 틀렸었는지**를 코드 주석에 남긴다. 이 표가 그 주석들의 목차다.
6. 🚩 **내 페이지가 걸린 기준을 내가 고칠 땐 밝혀라.** 7번이 그런 경우였다 —
   기준을 낮춘 게 아니라 §5 표의 숫자로 통일한 것이지만, 통일 뒤에도 걸린 페이지(`/business`)는
   **실제로 내용을 채워서** 통과시켰다. 자를 손대 통과시키는 것과 대상을 고쳐 통과시키는 것은 다르다.
7. **HTML 을 정규식으로 셀 땐 `<script>`·`<style>` 을 먼저 걷어라.** 8번이 그것이다.
   인라인 스크립트가 마크업 문자열을 들고 있는 SPA 에서는 모든 태그 개수 검사가 무의미해진다.


---

## §23. sitemap 은 발견만 시킨다 — 크롤 우선순위는 내부 링크가 정한다

**사고(2026-08-28, cue GSC 실측):** 점검기 FAIL 0 인 사이트의 **색인이 0개**였다.
620페이지 중 609개가 `발견됨 - 현재 색인이 생성되지 않음`, 11개가 `크롤링됨 - 색인 안 됨`,
클릭 0 · 노출 0. 구글의 마지막 크롤은 **40일 전**이었다.

URL 검사를 열어 보니 **기술적 장벽이 하나도 없었다** — 크롤 허용 예, 페이지 가져오기 성공,
색인 생성 허용 예. robots 도 리다이렉트도 오류도 아니었다.
그런데 `참조 사이트맵: 감지된 참조 사이트맵이 없습니다`, `참조 페이지: mark.the-moment.us/…` 였다.
**구글은 우리 사이트맵이 아니라 형제 사이트 링크를 타고 홈을 발견했다.**

재보니 원인은 하나였다:

```
/jobs (공고 허브)  → /job/ 링크 0개    ← 목록을 전부 JS 로 그려 봇에겐 빈 페이지
sitemap /job/ 495장 · 내부 링크 도달 112장
고아 383장 (77%)
```

> **"사이트맵에는 있는데 내부 링크가 0인 페이지가 Discovered 큐에 갇히는 1순위다."**
> 사이트맵은 **발견**만 보장하고, 크롤 **우선순위**는 내부 링크가 정한다.

### 규칙

1. 🔴 **sitemap 에 넣은 URL 은 내부 링크로도 도달해야 한다.** 하나라도 예외를 두지 마라.
2. **sitemap 기준과 목록 기준을 같은 코드에서 만들어라.** 갈리는 순간 그 차이가 곧 고아 수다.
   (cue: sitemap 은 `열림 && (질문 or JD)`, 목록은 상한 60 → 그 차이가 383장이었다)
3. **허브가 목록을 JS 로만 그리면 그 허브는 없는 것이다.** 봇은 빈 `<div>` 를 본다(§5).
   사용자 화면은 JS 가 덮어쓰므로 서버 렌더를 같이 내보내도 아무것도 달라지지 않는다.
4. **클릭 깊이 3 이내.** 홈에서 5클릭 넘게 떨어지면 크롤 효율이 급락한다.
5. 자동 검사: `python3 ~/bin/seo_check.py --live --domain <도메인> --orphans`
   (20% 넘으면 FAIL. cue `crawl.mjs` 가 배포마다 돌려 로그에 남긴다)

### 🚨 점검기 통과와 색인은 다른 문제다

`FAIL 0` 은 **"구글이 뺄 이유가 없다"** 는 뜻이지 **"구글이 온다"** 는 뜻이 아니다.
§3~§20 은 오면 안 빼이게 만드는 규칙이고, **오게 만드는 건 내부 링크(§23)와 색인 API 다.**
둘을 같은 것으로 착각하면, 다 고쳐놓고 색인 0인 채로 몇 달을 보낸다 — 실제로 그랬다.

### 🔴 규칙은 증거에서만 나온다 — `SEO_EXPERIMENTS.md`

**이 문서(§1~§23)는 "규칙"이고, `docs/SEO_EXPERIMENTS.md` 는 "증거"다.**
증거 없이 규칙을 추가하지 마라. 업계 통설을 그대로 옮겨 적는 건 규칙이 아니라 **인용**이고,
인용은 §20 처럼 1차 출처를 달아 구분해서 적는다.

실험 원장에는 **✅ 효과 확인 / ❌ 효과 없음 / 🌫 모름** 세 판정이 있고,
🚫 **❌ 와 🌫 를 지우지 마라 — 그게 제일 값나가는 기록이다.**
"이건 해봤는데 안 되더라"가 쌓여야 다음 사이트에서 시간을 안 버린다.

### 조치의 효과는 원장에 적는다

SEO 조치는 2~4주 뒤에 결과가 나온다. **무엇을 했고 뭐가 될 거라 봤고 언제 확인하는지**를
적어두지 않으면 그때 가서 아무도 모른다. cue 는 `cue/SEO_HYPOTHESES.md` 가 그 원장이다.
가설마다 **틀렸다고 볼 조건**을 같이 적는다 — 그게 없으면 영원히 "곧 될 거야"가 된다.

---

## §24. GEO 데스크 — "뭐 쓰지?"에 우리가 후보로 뽑히는지 매주 잰다 (2026-09-02)

**왜.** 대표: *"각 서비스가, 원하는 사람이 뭔가 하려고 할 때 추천이 되고 싶어."* 위 §들은 전부
**우리 페이지를 봇이 읽을 수 있게** 만드는 일이었고, 그게 됐는지는 아무도 안 재고 있었다.
월요일 크론 점검은 로그 파일에만 쌓였다.

**무엇.** 손님 말투 질문 세트(제품당 3~5개)를 매주 같은 엔진에 던져 **추천됐나 · 누가 대신
추천됐나 · 어떤 출처를 인용했나 · 어떤 기준으로 골랐나**를 적고, 그 세 목록을 할 일로 바꾼다.

| 읽는 것 | 뜻 | 바뀌는 할 일 |
|---|---|---|
| 인용 출처 도메인 | 우리가 실려야 할 자리 | 디렉터리 등록 · 비교글 기고 · 커뮤니티 |
| 추천 기준 구절 | 우리 페이지에 문장으로 있어야 할 것 | FAQ · 첫 문단 · llms.txt |
| 질문 표현 | 우리가 써야 할 글 제목 | 인사이트 글 · 네이버 블로그 |

**어디.**

| 것 | 경로 |
|---|---|
| 질문 세트 | `docs/geo/questions.json` — id 는 유지하고 문구만 고친다(주간 비교가 끊긴다) |
| 측정·판정·집계·보고 | `scripts/geo_probe.py` — `weekly` 한 방 = run→judge→actions→원장→커밋 |
| 회차 원본 | `docs/geo/runs/<날짜>.json` — (질문, 엔진) 키. 죽어도 빈 칸만 다시 채운다(룰 #12) |
| 주간 원장 | `docs/geo/GEO_LEDGER.md` — 회차를 지우지 마라 |
| 누적 출처 | `docs/geo/sources.json` — "실려야 할 자리" 목록. `listed` 를 사람이 갱신 |
| 실행·보고 | `~/slack-bot/geo_desk.py` — `__GEO_DESK__` 월 03:00, 보고는 #운영실 |

**엔진과 비용.** `claude`(claude -p + WebSearch, 구독, 질문당 60~120초) · `chatgpt`(OpenAI
Responses + web_search, 질문당 몇 원) · `naver_web`/`naver_blog`(검색 페이지 HTML — 검색 API 는
앱에 검색 scope 가 없어 401). 전부 **직렬**이고 새벽에 돈다. 제미나이·퍼플렉시티는 아직 없다.

**판정은 LLM, 집행은 코드.** "추천됐나·기준이 뭐냐·할 일이 뭐냐"는 `claude -p`(sonnet) 가
JSON 으로 답하고, 코드는 그 값을 **원문 (질문, 엔진) 키와 대조해 있는 항목만** 받는다.
지어낸 항목은 버려진다. 네이버는 도메인 등장 여부만 결정론으로 본다.

**측정 오염 주의.** `claude -p` 는 **이 저장소 밖(임시 디렉터리)** 에서 돈다. momentus 의
CLAUDE.md·메모리가 답변에 섞이면 "우리가 추천됐다"가 자기 자료를 읽은 결과가 된다.

**한 판 실측 (2026-09-02, heyreci-1 × 4엔진).** 아래 GEO_LEDGER.md 첫 회차 참조.

**알려진 한계.** `claude -p` 는 Claude Code 껍데기라 claude.ai 에서 손님이 받는 답과 같지 않다
(전역 `~/.claude/CLAUDE.md` 도 읽는다 — 거기에 the-moment.us 주소가 인프라 규칙으로 4줄 있다).
그래서 claude 열은 **추세**로만 읽고, 손님이 실제로 쓰는 답은 chatgpt·naver 열이 더 가깝다.
