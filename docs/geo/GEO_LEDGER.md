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

---

## 2026-09-07

**GEO 주간 측정 2026-09-07** — 엔진: chatgpt, claude, naver_blog, naver_web
7개 제품 전원 recommended 0 (지난 회차 대비 delta도 전부 0) — blog.naver.com(269회)·namu.wiki(56회)가 인용을 독점하는데 우리 페이지엔 그 자리에서 요구하는 문장이 없음

**제품별 추천됨 / 질문수**
• 헤이레시 · AI 상품사진: 추천 0/20 · 언급 0  [claude 0/5 · chatgpt 0/5 · naver_web 0/5 · naver_blog 0/5]
• 큐 · AI 모의면접: 추천 0/16 · 언급 0  [claude 0/4 · chatgpt 0/4 · naver_web 0/4 · naver_blog 0/4]
• 마크 · 로고 디자인: 추천 0/16 · 언급 0  [claude 0/4 · chatgpt 0/4 · naver_web 0/4 · naver_blog 0/4]
• 더플랜 · 디지털 플래너: 추천 0/12 · 언급 0  [claude 0/3 · chatgpt 0/3 · naver_web 0/3 · naver_blog 0/3]
• 빈방 · 취소표 알림: 추천 0/12 · 언급 0  [claude 0/3 · chatgpt 0/3 · naver_web 0/3 · naver_blog 0/3]
• 팀AI · AI 친구: 추천 0/12 · 언급 0  [claude 0/3 · chatgpt 0/3 · naver_web 0/3 · naver_blog 0/3]
• 컨텍스트: 추천 0/12 · 언급 0  [claude 0/3 · chatgpt 0/3 · naver_web 0/3 · naver_blog 0/3]

**대신 추천된 곳 (상위)**
• 헤이레시 · AI 상품사진: 드랩아트(Draph Art)(2), PhotoRoom(2), remove.bg(2), Canva(2), 미리캔버스(2)
• 큐 · AI 모의면접: 사람인 AI 모의면접(4), Yoodli(4), Google Interview Warmup(3), Big Interview(3), 잘봐요(2)
• 마크 · 로고 디자인: Canva(7), Looka(6), 미리캔버스(5), 크몽(4), 숨고(3)
• 더플랜 · 디지털 플래너: 텐바이텐(3), DT굿노트(2), 크몽(2), 아이디어스(2), Etsy(2)
• 빈방 · 취소표 알림: Distill.io(3), Visualping(3), Open Hotel Alert(2), Hotel Alerts(2), RoomSnag(2)
• 팀AI · AI 친구: Replika(3), 제타(zeta)(2), ELSA Speak(2), 너티(1), 크랙 (뤼튼)(1)
• 컨텍스트: Basic Memory(2), mem0(2), 브라우저 확장(2), OpenAI API(2), Pinecone(2)

**인용된 출처 도메인 = 우리가 실려야 할 자리**
blog.naver.com(269), namu.wiki(56), apps.apple.com(14), dtgoodnote.com(13), kmong.com(11), photoroom.com(8), sungmooncho.com(7), draph.art(6), piccopilot.com(6), ko.clippingmagic.com(6), community.linkareer.com(6), kokomen.kr(6)
새로 등장: gptparkai.com, help.openai.com, m.saramin.co.kr, openads.co.kr, velog.io

**봇이 이어서 할 일**
• [heyreci] heyreci 페이지 FAQ/첫문단에 '이커머스 전용(흰색 배경 대표 이미지, 라이프스타일 연출컷, 다각도 세트 등)'과 '무료 크레딧으로 바로 품질을 확인할 수 있어서 진입 비용이 가장 낮습니다' 문장 삽입 — heyreci criteria에 각 1회 등장한 추천 기준 문구인데 heyreci는 20문의 중 recommended 0
• [cue] cue 페이지에 '전달력(말버릇, 속도, 필러워드) 교정에 특화'와 '혼자 반복 연습하기에 가장 결이 맞습니다' 문구를 FAQ로 추가 — cue criteria에 각 1회 등장한 추천 기준 문구, cue는 16문의 중 recommended 0
• [mark] mark 페이지에 '한글 브랜드명, 무료 크레딧, 상업적 사용 허용'과 '매일 무료 크레딧, 상업적 사용 가능, 한국어 UI' 문구 삽입 — mark criteria에 각 1회 등장, mark는 16문의 중 recommended 0
• [notes] notes 페이지에 스펙 비교표(하이퍼링크 여부/만년 vs 날짜형/PDF 단일 파일 여부/포함 페이지) 추가 — notes criteria 8개 항목이 전부 스펙 비교 기준 문구인데 notes는 12문의 중 recommended 0
• [binbang] binbang 페이지 FAQ에 '24시간 감시'(2회, 최다 언급)와 'Booking.com 재고를 직접 보기 때문에 커버리지가 가장 무난' 문구 추가 — binbang criteria에서 '24시간 감시'가 2회로 가장 많이 언급됐는데 binbang은 12문의 중 recommended 0
• [teamai] teamai 페이지에 '먼저 말을 걸어주는지', '스토리·관계 기억 기능' 항목을 FAQ로 명시 — teamai criteria에 각 1회 등장한 추천 기준 문구, teamai는 12문의 중 recommended 0
• [kontext] kontext 페이지/llms.txt에 'Obsidian 볼트를 백엔드로 쓸 수 있는지', '마크다운 파일을 저장소로 쓰는지' 답을 명시 — kontext criteria에 각 1회 등장한 추천 기준 문구, kontext는 12문의 중 recommended 0

**대표님 몫 (새로 생긴 것만)**
• [cue] m.saramin.co.kr(이번 회차 신규 인용 도메인, 5회)에 cue 등록·제휴 제출 — new_domains에 이번에 처음 추가된 도메인이고 cue 경쟁사 '사람인 AI 모의면접'(4회 인용)이 바로 그 채널에서 나온 것으로 보임 — 외부 사이트 계정 등록·제출은 사람이 해야 함

---

## 2026-09-14

**GEO 주간 측정 2026-09-14** — 엔진: chatgpt, claude, naver_blog, naver_web
7개 제품 전부 추천 0건, 지난주 대비 delta도 전부 0 — 정체 원인은 인용 상위 도메인(kmong.com 16회, dtgoodnote.com 12회, draph.art/photoroom.com/canva.com 6~7회)과 criteria 문장이 우리 사이트에 없다는 것

**제품별 추천됨 / 질문수**
• 헤이레시 · AI 상품사진: 추천 0/20 · 언급 0  [claude 0/5 · chatgpt 0/5 · naver_web 0/5 · naver_blog 0/5]
• 큐 · AI 모의면접: 추천 0/16 · 언급 0  [claude 0/4 · chatgpt 0/4 · naver_web 0/4 · naver_blog 0/4]
• 마크 · 로고 디자인: 추천 0/16 · 언급 0  [claude 0/4 · chatgpt 0/4 · naver_web 0/4 · naver_blog 0/4]
• 더플랜 · 디지털 플래너: 추천 0/12 · 언급 0  [claude 0/3 · chatgpt 0/3 · naver_web 0/3 · naver_blog 0/3]
• 빈방 · 취소표 알림: 추천 0/12 · 언급 0  [claude 0/3 · chatgpt 0/3 · naver_web 0/3 · naver_blog 0/3]
• 팀AI · AI 친구: 추천 0/12 · 언급 0  [claude 0/3 · chatgpt 0/3 · naver_web 0/3 · naver_blog 0/3]
• 컨텍스트: 추천 0/12 · 언급 0  [claude 0/3 · chatgpt 0/3 · naver_web 0/3 · naver_blog 0/3]

**대신 추천된 곳 (상위)**
• 헤이레시 · AI 상품사진: 드랩아트(Draph Art)(3), Canva(3), 브이캣(VCAT.AI)(2), 카페24 에디봇(2), 가비아 AI 에디터(2)
• 큐 · AI 모의면접: 사람인 AI 모의면접(4), Yoodli(4), Final Round AI(4), 잘봐요(3), 면접톡(2)
• 마크 · 로고 디자인: 크몽(6), 미리캔버스(5), Canva(4), 숨고(3), 99designs(3)
• 더플랜 · 디지털 플래너: GoodNotes(3), 도트플래너(2), 굿노트끄적(2), Etsy(2), Reddit(2)
• 빈방 · 취소표 알림: 캠프링크(2), 캠핑나우(2), 빈숲(Been Forest)(1), 국립공원 예약정보(1), 국립 자연휴양림 찾기·빈자리(1)
• 팀AI · AI 친구: Replika(3), 제타(zeta)(2), 클로바 케어콜(2), Beff(2), Character.AI(2)
• 컨텍스트: Claude Projects(3), Pinecone(2), Weaviate(2), Milvus(2), LangChain(2)

**인용된 출처 도메인 = 우리가 실려야 할 자리**
blog.naver.com(268), namu.wiki(55), apps.apple.com(20), kmong.com(16), dtgoodnote.com(12), play.google.com(11), piccopilot.com(8), draph.art(7), photoroom.com(7), community.linkareer.com(7), canva.com(6), ko.clippingmagic.com(6)
새로 등장: brunch.co.kr, docs.tiro.ooo, finalroundai.com, remove.bg, sukbak.oppapost.com

**봇이 이어서 할 일**
• [heyreci] heyreci.com 첫 문단/FAQ에 '촬영 없이 상품 URL만 넣으면 자동 생성' 문장 삽입 — criteria에 '상품 URL만 넣으면 자동 생성'(1), '촬영 없이'(1), '촬영 로봇'(1)이 등장하지만 heyreci 추천은 0건 — 페이지에 이 문구 자체가 없을 가능성
• [cue] cue.the-moment.us FAQ에 '루브릭 기반 채점형', '구조화된 행동면접 연습', '세션 후 디브리핑까지 지원' 문장 추가 — cue criteria에 각 1회씩 등장한 기준 문구인데 recommended 0/16 — 경쟁사 Final Round AI(4), 사람인 AI 모의면접(4)에 밀려 언급조차 안 됨
• [mark] mark.the-moment.us에 '무료 상업용 한글 폰트', '벡터 파일(AI·SVG·EPS)' 항목을 페이지 문장으로 명시 — mark criteria에 각 1회 등장, 경쟁사 크몽(6)·미리캔버스(5)·Canva(4)에 밀려 recommended 0/16
• [notes] notes.the-moment.us에 '날짜형 vs 만년형' 비교 섹션 추가 — notes criteria에서 가장 많이 등장한 기준(2회)인데 페이지에 답이 없어 GoodNotes(3)·도트플래너(2)로 추천이 감

**대표님 몫 (새로 생긴 것만)**
• [heyreci] 카페24 앱스토어에 헤이레시 앱 등록 신청 — criteria '카페24 앱스토어 입점'(1), '이미 카페24 쓰는 분'(1) — 등록 자체가 안 돼 있으면 이 축의 질문에 절대 못 뽑힘, 심사 제출은 사람이 해야 함
• [mark] kmong.com에 마크 서비스 판매자 등록 — kmong.com이 전체 인용 도메인 3위(16회), 크몽은 mark 경쟁사 언급 1위(6회) — 계정 가입·심사가 필요해 봇이 못 함
• [notes] dtgoodnote.com에 더플랜 제품 리스팅/제휴 문의 — dtgoodnote.com이 인용 도메인 5위(12회)이자 GoodNotes(3) 생태계 허브 — 외부 사이트 제출·승인 필요
• [binbang] sukbak.oppapost.com·pension.tuwaagin.com에 빈방 게스트 포스팅 제안 — 두 도메인 모두 이번 주 신규 인용(각 6회, new_domains 목록 포함) — 외부 블로그 컨택·발행 승인이 필요해 사람 몫

---

## 2026-09-21

**GEO 주간 측정 2026-09-21** — 엔진: chatgpt, claude, naver_blog, naver_web
헤이레시가 챗GPT에서 1건 추천되며(20문 중 첫 추천, 전주 대비 +1) 유일하게 움직였고 나머지 6개 제품은 이번 주도 추천 0건 — 노출 자리는 크몽·재능넷·인터뷰톡·toolify.ai로 구체적으로 잡힌다

**제품별 추천됨 / 질문수**
• 헤이레시 · AI 상품사진: 추천 1/20 · 언급 1  (+1)  [claude 0/5 · chatgpt 1/5 · naver_web 0/5 · naver_blog 0/5]
• 큐 · AI 모의면접: 추천 0/16 · 언급 0  [claude 0/4 · chatgpt 0/4 · naver_web 0/4 · naver_blog 0/4]
• 마크 · 로고 디자인: 추천 0/16 · 언급 0  [claude 0/4 · chatgpt 0/4 · naver_web 0/4 · naver_blog 0/4]
• 더플랜 · 디지털 플래너: 추천 0/12 · 언급 0  [claude 0/3 · chatgpt 0/3 · naver_web 0/3 · naver_blog 0/3]
• 빈방 · 취소표 알림: 추천 0/12 · 언급 0  [claude 0/3 · chatgpt 0/3 · naver_web 0/3 · naver_blog 0/3]
• 팀AI · AI 친구: 추천 0/12 · 언급 0  [claude 0/3 · chatgpt 0/3 · naver_web 0/3 · naver_blog 0/3]
• 컨텍스트: 추천 0/12 · 언급 0  [claude 0/3 · chatgpt 0/3 · naver_web 0/3 · naver_blog 0/3]

**대신 추천된 곳 (상위)**
• 헤이레시 · AI 상품사진: remove.bg(4), 드랩아트(Draph Art)(2), 드랩아트(DraphArt)(2), PhotoRoom(2), Photoroom(2)
• 큐 · AI 모의면접: 사람인 AI 모의면접(4), 면접톡(4), interviewing.io(4), Yoodli(4), Pramp(3)
• 마크 · 로고 디자인: Looka(6), Canva(5), 미리캔버스(4), 크몽(4), 숨고(3)
• 더플랜 · 디지털 플래너: 로그로그(3), DT굿노트(2), Etsy(2), GoodNotes(2), Notability(2)
• 빈방 · 취소표 알림: 여기어때(4), 야놀자(NOL)(3), 땡큐캠핑(2), 빈숲(2), 전자휴(2)
• 팀AI · AI 친구: Replika(3), 제타(Zeta)(2), 아에리(Aeri)(2), ELSA Speak(2), 에이닷(1)
• 컨텍스트: OpenMemory MCP(2), Zep(2), Pinecone(2), Weaviate(2), Supermemory(2)

**인용된 출처 도메인 = 우리가 실려야 할 자리**
blog.naver.com(277), namu.wiki(36), apps.apple.com(20), kmong.com(16), dtgoodnote.com(12), jaenung.net(10), community.linkareer.com(9), skyscanner.co.krhttps(9), play.google.com(8), draph.art(7), photoroom.com(7), canva.com(7)
새로 등장: adobe.com, armes.co.kr, help.naver.com, interviewtalk.kr, jaenung.net, jobda.im, korean.go.kr, skyscanner.co.krhttps, toolify.ai

**봇이 이어서 할 일**
• [heyreci] 헤이레시 페이지 FAQ/첫 문단에 '카페24 연동', '무료 크레딧', '상세페이지·광고까지 한 번에' 문장 삽입 — criteria.heyreci에 '카페24로 쇼핑몰 운영 중', '무료 크레딧', '상세페이지·광고까지 한 번에'가 손님 판단 기준 구절로 잡힘 — 챗GPT 1건 추천(recommended_delta +1)을 다른 엔진으로 확장하려면 이 구절이 페이지 문장으로 있어야 함
• [mark] 마크 첫 문단에 '한글 로고를 제대로 뽑아주는 거의 유일한 국산 서비스' 문구 반영 — criteria.mark에 그대로 등장하는 차별화 구절인데 mark는 recommended 0/16 — 이 문장이 페이지에 없으면 AI가 근거로 못 씀
• [cue] 큐 FAQ에 '꼬리질문', '말버릇·속도·필러워드 교정' 문장 추가 — criteria.cue에 두 구절이 판단 기준으로 집계됐으나 cue는 recommended 0/16 — 페이지에 문장으로 없어서 근거로 안 쓰이는 것으로 추정
• [notes] 더플랜 페이지에 '하이퍼링크(연결) 유무', '한글 속지' 문장 명시 — criteria.notes에 두 구절이 비교 기준으로 잡혔고 competitors.notes 상위(로그로그·DT굿노트·Notability)와 갈리는 지점 — notes recommended 0/12
• [binbang] 빈방 첫 문단에 '15초마다 스캔', '24시간 감시' 강조 — criteria.binbang에 그대로 등장하는 구절이며 competitors.binbang(여기어때·야놀자·땡큐캠핑)과 차별화되는 지점 — binbang recommended 0/12

**대표님 몫 (새로 생긴 것만)**
• [heyreci] toolify.ai에 헤이레시 AI 툴 등록 — toolify.ai는 이번 주 신규 인용 도메인(new_domains, 4회)이고 heyreci 경쟁사인 remove.bg·Photoroom·Canva가 이런 AI 툴 디렉터리에 이미 노출 — 계정 가입·외부 제출이 필요해 사람 작업
• [mark] jaenung.net에 마크 로고 디자인 서비스 등록 — jaenung.net은 신규 인용 도메인(10회)이며 성격상 competitors.mark의 크몽·숨고·Fiverr·Upwork와 같은 프리랜서 마켓 — 셀러 등록은 로그인·외부 제출이라 사람 작업
• [cue] interviewtalk.kr에 큐 소개/링크 제출 — interviewtalk.kr은 신규 인용 도메인(4회)이고 면접 주제 질문에 인용됨 — competitors.cue(사람인·면접톡·잡다) 영역과 겹쳐 등록 대상, 외부 제출이라 사람 작업

---

## 2026-09-28

**GEO 주간 측정 2026-09-28** — 엔진: chatgpt, claude, naver_blog, naver_web (⚠️ 일부 칸 실패)

**제품별 추천됨 / 질문수**
• 헤이레시 · AI 상품사진: 추천 0/20 · 언급 0  (-1)  [claude 0/5 · chatgpt 0/5 · naver_web 0/5 · naver_blog 0/5]
• 큐 · AI 모의면접: 추천 0/16 · 언급 0  [claude 0/4 · chatgpt 0/4 · naver_web 0/4 · naver_blog 0/4]
• 마크 · 로고 디자인: 추천 0/16 · 언급 0  [claude 0/4 · chatgpt 0/4 · naver_web 0/4 · naver_blog 0/4]
• 더플랜 · 디지털 플래너: 추천 0/12 · 언급 0  [claude 0/3 · chatgpt 0/3 · naver_web 0/3 · naver_blog 0/3]
• 빈방 · 취소표 알림: 추천 1/12 · 언급 1  (+1)  [claude 0/3 · chatgpt 0/3 · naver_web 1/3 · naver_blog 0/3]
• 팀AI · AI 친구: 추천 0/12 · 언급 0  [claude 0/3 · chatgpt 0/3 · naver_web 0/3 · naver_blog 0/3]
• 컨텍스트: 추천 0/12 · 언급 0  [claude 0/3 · chatgpt 0/3 · naver_web 0/3 · naver_blog 0/3]
  미판정 25건

**대신 추천된 곳 (상위)**

**인용된 출처 도메인 = 우리가 실려야 할 자리**
blog.naver.com(279), namu.wiki(55), kmong.com(12), play.google.com(9), apps.apple.com(8), skyscanner.co.krhttps(8), welldone-interview.co.kr(7), jaenung.net(7), sungmooncho.com(7), ko.clippingmagic.com(6), community.linkareer.com(6), kokomen.kr(6)
새로 등장: class101.net, gongysd.com, help.openai.com, mcst.go.kr, sungmooncho.com, welldone-interview.co.kr

(할 일 판정이 실패해 표만 올립니다 — 다음 회차에 다시 시도)

---

## 2026-10-05

**GEO 주간 측정 2026-10-05** — 엔진: chatgpt, claude, naver_blog, naver_web (⚠️ 일부 칸 실패)

**제품별 추천됨 / 질문수**
• 헤이레시 · AI 상품사진: 추천 0/20 · 언급 0  [claude 0/5 · chatgpt 0/5 · naver_web 0/5 · naver_blog 0/5]
• 큐 · AI 모의면접: 추천 0/16 · 언급 0  [claude 0/4 · chatgpt 0/4 · naver_web 0/4 · naver_blog 0/4]
• 마크 · 로고 디자인: 추천 0/16 · 언급 0  [claude 0/4 · chatgpt 0/4 · naver_web 0/4 · naver_blog 0/4]
• 더플랜 · 디지털 플래너: 추천 0/12 · 언급 0  [claude 0/3 · chatgpt 0/3 · naver_web 0/3 · naver_blog 0/3]
• 빈방 · 취소표 알림: 추천 1/12 · 언급 1  [claude 0/3 · chatgpt 0/3 · naver_web 1/3 · naver_blog 0/3]
• 팀AI · AI 친구: 추천 0/12 · 언급 0  [claude 0/3 · chatgpt 0/3 · naver_web 0/3 · naver_blog 0/3]
• 컨텍스트: 추천 0/12 · 언급 0  [claude 0/3 · chatgpt 0/3 · naver_web 0/3 · naver_blog 0/3]
  미판정 25건

**대신 추천된 곳 (상위)**

**인용된 출처 도메인 = 우리가 실려야 할 자리**
blog.naver.com(276), namu.wiki(47), kmong.com(13), apps.apple.com(9), welldone-interview.co.kr(9), wedding-fair.seoul.kr(9), jaenung.net(8), photoroom.com(7), community.linkareer.com(7), wadiz.io(7), ko.clippingmagic.com(6), summitfeed.co.kr(6)
새로 등장: aaro.kr, ezpdf.co.kr, haijob.co.kr, openai.com, piccopilot.com, softonic.kr, summitfeed.co.kr, wadiz.io, wedding-fair.seoul.kr

(할 일 판정이 실패해 표만 올립니다 — 다음 회차에 다시 시도)

---

## 2026-10-12

**GEO 주간 측정 2026-10-12** — 엔진: chatgpt, claude, naver_blog, naver_web
7개 제품 중 빈방만 2건 추천(+1), 나머지 6개는 80여 개 질의에서 추천 0 — 인용 도메인(blog.naver.com 276, kmong.com 18 등)과 추천 기준 구절을 페이지·글에 맞추는 것이 이번 주 과제

**제품별 추천됨 / 질문수**
• 헤이레시 · AI 상품사진: 추천 0/20 · 언급 0  [claude 0/5 · chatgpt 0/5 · naver_web 0/5 · naver_blog 0/5]
• 큐 · AI 모의면접: 추천 0/16 · 언급 0  [claude 0/4 · chatgpt 0/4 · naver_web 0/4 · naver_blog 0/4]
• 마크 · 로고 디자인: 추천 0/16 · 언급 0  [claude 0/4 · chatgpt 0/4 · naver_web 0/4 · naver_blog 0/4]
• 더플랜 · 디지털 플래너: 추천 0/12 · 언급 0  [claude 0/3 · chatgpt 0/3 · naver_web 0/3 · naver_blog 0/3]
• 빈방 · 취소표 알림: 추천 2/12 · 언급 2  (+1)  [claude 0/3 · chatgpt 1/3 · naver_web 1/3 · naver_blog 0/3]
• 팀AI · AI 친구: 추천 0/12 · 언급 0  [claude 0/3 · chatgpt 0/3 · naver_web 0/3 · naver_blog 0/3]
• 컨텍스트: 추천 0/12 · 언급 0  [claude 0/3 · chatgpt 0/3 · naver_web 0/3 · naver_blog 0/3]

**대신 추천된 곳 (상위)**
• 헤이레시 · AI 상품사진: 크몽(5), Canva(4), 드랩아트(Draph Art)(2), MixMemo(2), Photoroom(2)
• 큐 · AI 모의면접: Yoodli(4), Final Round AI(3), LeetCode(3), Google Interview Warmup(2), Big Interview(2)
• 마크 · 로고 디자인: 크몽(6), Canva(4), 숨고(3), 라우드소싱(3), 미리캔버스(2)
• 더플랜 · 디지털 플래너: Etsy(4), 네이버 스마트스토어(4), 크몽(3), 아이디어스(2), 텐바이텐(2)
• 빈방 · 취소표 알림: 야놀자(NOL)(2), 여기어때(2), 땡큐캠핑(1), 캠핏(1), Campnab(1)
• 팀AI · AI 친구: Replika(3), 제타(zeta)(2), Praktika(2), ELSA Speak(2), 에이닷(A.)(2)
• 컨텍스트: Obsidian(3), Mem0(2), Notion(2), Pinecone(2), Weaviate(2)

**인용된 출처 도메인 = 우리가 실려야 할 자리**
blog.naver.com(276), namu.wiki(55), kmong.com(18), apps.apple.com(14), wedding-fair.seoul.kr(10), welldone-interview.co.kr(9), ko.clippingmagic.com(6), community.linkareer.com(6), draph.art(5), photoroom.com(5), kokomen.kr(5), tilnote.io(5)
새로 등장: help.openai.com, interviewing.io, korean.go.kr, mcst.go.kr, openads.co.kr, remove.bg, toolify.ai

**봇이 이어서 할 일**
• [heyreci] 헤이레시 첫 문단·FAQ에 '촬영 없이 상품 사진', '무료 체험', '제품이 그대로 나오는지(라벨·로고·패키지 문구 유지)', '상업적 이용 가능'을 문장으로 명시하고 llms.txt에도 반영 — heyreci 추천 0/20, 추천 기준 구절 1위가 '무료 체험'(3회)이고 '라벨·로고·패키지 문구를 유지', '상업적 이용'도 언급됨
• [heyreci] 헤이레시 대 Photoroom·remove.bg·Canva 비교 글 초안 작성 (배경 제거 vs 연출컷 생성) — 경쟁사 Canva 4회·Photoroom 2회·remove.bg 2회, 인용 도메인에 photoroom.com 5·remove.bg 4·canva.com 4·ko.clippingmagic.com 6
• [cue] 큐 랜딩에 '직무별 질문', '꼬리질문', '표정·시선·음성·답변 분석', '가입 없이 무료 체험'을 FAQ·첫 문단 문장으로 추가 — cue 추천 0/16, 추천 기준 '직무별 질문' 3회 최다, '가입할 필요가 없습니다'·'꼬리질문'·'표정·시선·음성·답변 내용을 분석' 각 1회
• [mark] 마크 페이지에 '10분이면 완성', '한글 글꼴 다수', '시안 수십 개 즉시 확인', '원본·벡터 파일 제공', '상표 등록은 별도'를 명시한 FAQ와 크몽·Canva 대비 비교 초안 작성 — mark 추천 0/16, 경쟁사 크몽 6·Canva 4·숨고 3, 추천 기준 '10분이면 끝나고 한글 글꼴이 많음'·'벡터 파일 제공 가능'·'상표 등록이 안 됨'
• [notes] 더플랜 페이지에 '하이퍼링크', '한국 공휴일·음력', '무료 서식', '가로형/세로형', '다크모드', 'GoodNotes 호환' 스펙을 문장·FAQ로 정리 — notes 추천 0/12, 추천 기준 '하이퍼링크' 2회 최다, 경쟁사 GoodNotes·Notability 각 2회, Etsy 4회
• [binbang] 빈방 '취소 감시·빈자리 알림' 문구를 유지한 채 '숙소 직접 전화 대기', '플랫폼 Notify me', '웹페이지 변경 감시(Visualping)' 대비 차이를 설명하는 FAQ·비교 글 초안 작성 — binbang만 추천 2건(chatgpt 1·naver_web 1, 전주 대비 +1)이고 claude·naver_blog는 0, 추천 기준에 '숙소에 직접 전화해서 대기 요청'·'웹페이지 변경 감시'가 나옴
• [teamai] 팀AI 페이지에 '한국어 말투가 자연스러움', '기억 기능으로 대화 이어감', '캐릭터 선택·생성', '무료로 시작'을 첫 문단·FAQ에 명시 — teamai 추천 0/12, 추천 기준 구절 '한국어 말투가 가장 자연스럽습니다'·'기억 기능으로 대화를 이어 가고'·'무료로 시작' 및 경쟁사 Replika 3·제타 2
• [kontext] 컨텍스트 페이지 첫 문단에 '이미 갖고 있는 위키를 정본으로 활용', '여러 AI가 같은 기억을 공유', '관리할 곳을 늘리지 않음', '개인정보 보호'를 문장으로 명시하고 Obsidian·Mem0·Notion 대비 비교 초안 작성 — kontext 추천 0/12, 추천 기준 구절이 위 항목들이고 경쟁사 Obsidian 3·Mem0 2·Notion 2

**대표님 몫 (새로 생긴 것만)**
• [heyreci] 크몽(kmong.com)에 헤이레시·마크 서비스 등록 또는 프로필 개설 (계정 로그인·제출) — kmong.com 18회 인용, 크몽이 heyreci 경쟁사 5회·mark 경쟁사 6회로 1위인데 외부 계정 로그인·제출은 봇이 못 함
• [cue] 네이버 블로그(blog.naver.com)에 큐용 '직무별 AI 모의면접' 후기·가이드 글 발행 승인 및 게시 — blog.naver.com 276회로 최다 인용 도메인이며 cue 추천 0/16, 발행 승인·계정 게시는 사람이 해야 함
