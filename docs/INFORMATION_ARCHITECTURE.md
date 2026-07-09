# the-moment.us — 정보 설계(IA) · CMS · 정적/AEO 전략

> 2026-07-09. 비주얼 이전에 잡는 뼈대. 사이트맵 · 페이지 위계 · 제품 등록(CMS) · LLM이 읽는 정적 전략.
> 원칙 출처: [`APEX_STRATEGY.md`](./APEX_STRATEGY.md), [`SITE_STRUCTURE.md`](./SITE_STRUCTURE.md)

---

## A. 사이트맵 (페이지 계층 + 목적)

> **URL은 SEO용(검색어), 화면 라벨은 갤러리 voice("소장품/작품").** 둘을 분리한다.

```
the-moment.us
├── /                     [홈/전시장]        방문자 욕망→1클릭 도구→컬렉션→팬. AEO 앵커.
├── /tools                [컬렉션 인덱스]     전 제품 목록·필터. 카탈로그. "무료 도구" 검색 착지.
│   ├── /tools/[slug]      [작품 상세]        ★ 제품당 1페이지 = AEO/SEO 유닛. manifest가 생성.
│   │     예) /tools/instagram-sort, /tools/her ...
│   └── (필터: 북마크릿 / 크롬확장 / 하려는 일별)   — 별도 페이지 아닌 쿼리 필터로
├── /about                [소개]             강형모 사람 층·AI 생산방식·타임라인. "팬 되기" 페이지.
├── /log                  [만든 것]          누적 changelog(levels.io식). 신선도·정량 = AEO 무기.
├── /legal                [이용약관]         재사용(이미 legal.html 있음)
├── /privacy              [개인정보처리방침]   재사용(이미 privacy-policy.html 있음)
└── /contact 또는 mailto   [문의]            hello@the-moment.us
```

**페이지 수:** 고정 6~7 + 제품당 1(`/tools/[slug]`). 지금 6개 → 약 12페이지.
**핵심:** 새 제품 = `/tools/[slug]` **한 장 자동 증가** + 홈 카드 + /tools 행 + sitemap + JSON-LD 자동. (지그)

---

## B. 페이지별 세로 위계 (위→아래)

### 홈 `/`
1. 헤더 — 워드마크 MOMENTUS + 최소 내비(작품·소개·문의)
2. **히어로** — 방문자 욕망 한 줄 + **1클릭 무료도구**(즉시 체험) ← B안 히어로
3. **現在 전시중** — 컬렉션 인덱스(6점, 카테고리/욕망별)
4. 작가의 말(teaser) → /about
5. **만든 것 / shipped** — 누적 changelog(신선도)
6. 푸터 — 법정·문의 + **정량 문구**("2026-07 기준 6개 도구·1만+ 사용")=AEO 앵커

### 작품 상세 `/tools/[slug]` ★ (AEO의 심장)
1. 작품명 + 매체 + `무료`
2. **한 줄 큐레이터 캡션 = 40~60단어 원자 답변**(사람이 LLM에 묻는 그대로)
3. 설치/드래그 CTA
4. mono 스펙 표(무엇·어디서·단축키·언어·가격)
5. 사용법 / 어디서 되나
6. **FAQ — 질문형 헤딩**(AEO 추출 블록)
7. 귀환 갈고리(다른 작품)
8. 푸터(법정·문의)

### 소개 `/about`
사람(강형모) → AI 생산방식 → 만든 것 타임라인 → 정직한 목소리 → 소셜/GitHub

---

## C. CMS — "제품 등록", 오버스펙 없이

### 원칙: **DB·헤드리스 SaaS·관리자 앱 만들지 않는다.**
제품 몇 개짜리 1인 스튜디오에 DB 백엔드 admin = 오버스펙. 게다가 그건 정적·LLM-readable·무료호스팅을 깬다.

### 정답: **콘텐츠 = 리포 안 플랫 파일 (단일 소스)**
- `src/content/tools/*.md` (frontmatter) **또는** 단일 `products.json` = 매니페스트 = 진실의 원천.
- **제품 등록 = 항목 1개 추가 → git push → CF Pages 자동 재빌드.** 관리자 UI 없음. "admin"은 파일 1개 편집.
- Astro **Content Collections + Zod 스키마**로 필드 검증 → 오타·누락 빌드 시 차단(오버스펙 없이 안전).
- **이 슬랙봇이 제품을 자동 등록 가능** — 새 도구 만들면 봇이 항목 append + 커밋. (지그 자동화)

### 최소 스키마(필드)
```yaml
slug, name, tagline          # 큐레이터 한 줄
category: bookmarklet|extension
medium, free: true
url                          # 스토어 링크 or 북마크릿 소스
atomic_answer                # 40~60단어 (AEO)
spec: {무엇, 어디서, 단축키, 언어, 가격}
faq: [{q, a}, ...]           # 질문형 (AEO)
date, proof?                 # "1만 팔로워" 등
hook: true                   # 귀환 갈고리
```

### 3단계 (필요할 때만 올림)
| 단계 | 무엇 | 언제 |
|---|---|---|
| **0 (MVP·권장)** | 플랫 파일(json/md) 직접 편집 | 지금. 인프라 0 |
| 1 (옵션) | git-기반 폼 UI(Decap/TinaCMS) — 여전히 같은 리포 파일 출력, 정적 유지 | JSON 편집이 귀찮아지면 |
| ✗ 금지 | Contentful 등 헤드리스 SaaS·DB·서버·admin 앱 | 오버스펙. 비용·정적·AEO 다 깸 |

---

## D. 정적 + AEO 전략 (Perplexity·GPT·Claude가 읽게)

### 왜 정적이어야 하나 = 두 목표가 하나로 통합
- **LLM은 초기 HTML만 읽는다.** JS로 그려지는 콘텐츠는 크롤러가 못 봄.
- **Astro + CF Pages** → 페이지마다 **사전 렌더 정적 HTML**(콘텐츠가 초기 HTML에, 클라 JS 0). mark와 동일 스택.
- 플랫 파일 → 정적 HTML로 빌드 = **"스태틱 파일처럼 관리"** + **"LLM이 읽음"**이 같은 시스템. 형 직관이 정확.

### 페이지에서 실제 효과 있는 것(과투자 금지)
- `/tools/[slug]`마다: **질문형 헤딩 + 40~60단어 원자 답변** + **정량·날짜 사실** + **비교표 1개**.
- 깨끗한 시맨틱 HTML(h1/h2·진짜 텍스트, canvas/이미지-only 금지).
- `robots.txt` — **AI 크롤러 허용**(GPTBot·ClaudeBot·PerplexityBot·Google-Extended).
- `sitemap.xml`(자동), JSON-LD `SoftwareApplication`(제품당), `llms.txt`(기대 낮지만 쌈).

### 미신·과투자 금지
llms.txt에 올인·대형 스키마·백링크 사재기 = 효과 미미. **AEO 진짜 동력은 페이지 밖 다출처 반복언급**(Reddit·디렉토리·네이버 4곳+). 사이트는 그것들이 가리키는 **앵커**.

---

## E. 한 장 요약

- **IA:** 홈 · /tools(+[slug]) · /about · /log · 법정 = 고정 6~7 + 제품당 1장 자동.
- **CMS:** 리포 플랫 파일 1개 = 등록. git push = 배포. DB·SaaS 금지.
- **정적/AEO:** Astro 정적 빌드 → 관리 쉬움 + LLM 읽힘(한 시스템). 상세페이지가 AEO 유닛. 진짜 트래픽은 페이지 밖.

### 결정 대기
- [ ] URL 라벨: `/tools` vs `/works` (SEO=tools 권장)
- [ ] CMS 단계 0(플랫파일)로 시작 확정?
- [ ] 콘텐츠 포맷: `products.json` 단일 vs `content/tools/*.md` 개별 (제품 늘면 md 권장)
