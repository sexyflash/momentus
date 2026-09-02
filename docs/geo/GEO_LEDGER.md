# GEO 원장 — '뭐 쓰지?'에 우리가 후보로 뽑히는가

> 매주 `scripts/geo_probe.py weekly` 가 아래에 한 회차씩 쌓는다. 원본은 `runs/<날짜>.json`.
> 읽는 법: **인용 도메인 = 실려야 할 자리 · 추천 기준 = 페이지에 있어야 할 문장 · 질문 표현 = 글 제목.**
> 🚫 회차를 지우지 마라. 안 움직인 기록이 제일 값나간다(SEO_EXPERIMENTS.md 원칙).


---

## 2026-09-02

**GEO 주간 측정 2026-09-02** — 엔진: chatgpt, claude, naver_blog, naver_web
7개 제품 108개 질의 전부에서 추천 0건(첫 주 베이스라인) — 인용 도메인·기준 문구 기반으로 노출 작업 착수

**제품별 추천됨 / 질문수**
• 헤이레시 · AI 상품사진: 추천 0/20 · 언급 0  [claude 0/5 · chatgpt 0/5 · naver_web 0/5 · naver_blog 0/5]
• 큐 · AI 모의면접: 추천 0/16 · 언급 0  [claude 0/4 · chatgpt 0/4 · naver_web 0/4 · naver_blog 0/4]
• 마크 · 로고 디자인: 추천 0/16 · 언급 0  [claude 0/4 · chatgpt 0/4 · naver_web 0/4 · naver_blog 0/4]
• 더플랜 · 디지털 플래너: 추천 0/12 · 언급 0  [claude 0/3 · chatgpt 0/3 · naver_web 0/3 · naver_blog 0/3]
• 빈방 · 취소표 알림: 추천 0/12 · 언급 0  [claude 0/3 · chatgpt 0/3 · naver_web 0/3 · naver_blog 0/3]
• 팀AI · AI 친구: 추천 0/12 · 언급 0  [claude 0/3 · chatgpt 0/3 · naver_web 0/3 · naver_blog 0/3]
• 컨텍스트: 추천 0/12 · 언급 0  [claude 0/3 · chatgpt 0/3 · naver_web 0/3 · naver_blog 0/3]

**대신 추천된 곳 (상위)**
• 헤이레시 · AI 상품사진: remove.bg(3), 드랩아트(2), MixMemo(2), Canva(2), Crello(2)
• 큐 · AI 모의면접: 사람인 AI 모의면접(7), 면접톡(4), Yoodli(4), 잘봐요(3), Pramp(3)
• 마크 · 로고 디자인: 크몽(4), Canva(3), 미리캔버스(3), Looka(3), Tailor Brands(2)
• 더플랜 · 디지털 플래너: 네이버 스마트스토어(3), 크몽(3), Etsy(2), Notion(2), Todoist(2)
• 빈방 · 취소표 알림: 여기어때(3), Visualping(2), 야놀자(2), 네이버 예약(2), 캠퍼블 CAMPABLE(2)
• 팀AI · AI 친구: ChatGPT(4), Replika(4), Character.AI(3), ELSA Speak(2), 제타(zeta)(1)
• 컨텍스트: Supermemory(2), Zep(2), CLAUDE.md(2), Pinecone(2), Weaviate(2)

**인용된 출처 도메인 = 우리가 실려야 할 자리**
blog.naver.com(265), namu.wiki(55), apps.apple.com(22), kmong.com(16), dtgoodnote.com(11), community.linkareer.com(10), haijob.co.kr(10), piccopilot.com(9), play.google.com(9), sungmooncho.com(7), draph.art(6), vcat.ai(6)

**봇이 이어서 할 일**
• [heyreci] heyreci FAQ/llms.txt 첫 문단에 '카페24 앱스토어 입점', '5회 무료 체험' 문구 추가 — criteria.heyreci에 '카페24 앱스토어 입점'(1), '5회 무료 체험'(1)이 추천 근거 구절로 집계됐으나 recommended 0/20
• [cue] cue 페이지 첫 문단에 '이력서 기반 맞춤 질문' 문구 삽입 — criteria.cue에서 '이력서 기반 맞춤 질문'(2), '무료 체험'(2)이 최다 근거 구절, recommended 0/16
• [mark] mark 페이지에 '한국어 UI·한글 서체' 문구 추가 — criteria.mark에 등장, competitors.mark에서 크몽(4)이 최다 경쟁자로 잡힘
• [binbang] binbang 첫 문단에 '무료', '취소표 실시간 알림' 문구 강조 — criteria.binbang에서 '무료'(2), '취소표 실시간 알림'(2)이 공동 최다 근거 구절
• [kontext] kontext 블로그에 '여러 AI를 번갈아 쓰신다면' 등 질문형 제목으로 비교글 초안 작성 — criteria.kontext의 근거 구절들이 전부 손님 질문 프레이밍('~쓰신다면','~경우')이라 그대로 제목화 가능

**대표님 몫 (새로 생긴 것만)**
• [mark] kmong.com에 mark 로고 디자인 서비스 리스팅 제출 — cited_domains에서 kmong.com이 16회로 인용 도메인 3위이고 competitors.mark에서도 크몽이 4회로 최다 경쟁자 — 외부 플랫폼 계정 제출 필요
• [heyreci] 카페24 앱스토어에 heyreci 실제 입점 신청·승인 진행 — criteria.heyreci에 '카페24 앱스토어 입점'이 추천 근거로 집계됐으나 아직 미입점으로 추정 — 외부 플랫폼 심사·승인이라 사람 필요
• [cue] community.linkareer.com·haijob.co.kr 계정으로 로그인해 cue 소개글 게시 — cited_domains에서 두 도메인이 각각 10회로 공동 4위 인용 — 취업준비생 커뮤니티 계정 로그인·게시글 작성이 필요
