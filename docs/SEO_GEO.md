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

## §12. 우선순위 — 이 순서로 고쳐라

| 순위 | 할 일 | 근거 | 비용 |
|---|---|---|---|
| 1 | **GSC 도메인 속성 등록 + sitemap 제출** (the-moment.us · heyreci.com) | 이거 없이는 나머지가 무의미. 소유확인 수단이 아예 없다 | 30분 · **사람만 가능** |
| 2 | **배포** — apex 의 og:image·JSON-LD·description 개선이 아직 로컬에만 있다 | 고쳐 놓고 안 올리면 0 | 5분 |
| 3 | **`notes` 프리렌더 본문** — 344자로는 유료 상품이 봇에게 안 보인다. `seo.js` 의 `seoBody()` 확장 | 매출 도메인이 사실상 미색인 | 반나절 |
| 4 | **`heyreci.com` 에 canonical + JSON-LD** | 매출 도메인인데 둘 다 0건 | 반나절 |
| 5 | **`mark` 에 업종별 랜딩** — sitemap URL 이 1개뿐이라 검색에 낼 표면이 없다 | 색인 물량 자체가 없음 | 별건, 크다 |
| 6 | **제품 상세 본문 늘리기** — apex 제품 상세가 917~968자(기준 1,000). 질문형 헤딩+FAQ 추가 | GEO 인용 단위 | 반나절 |
| 7 | `cue` 의 `/jobs`·`/blog` JSON-LD 0건 보완 | 623 URL 중 큰 축이 비어 있음 | 2시간 |
| 8 | sitemap `lastmod`(전 도메인), RSS `<link rel="alternate">`, `h1` 1개 정리 | 마감 | 2시간 |
| 9 | `notes`·`heyreci` 에 `llms.txt` | GEO 보조 (기대치는 낮게) | 30분 |

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
