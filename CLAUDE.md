# momentus — Claude Code 작업 지침

> 모멘터스 스튜디오 자산 저장소. pion 상세페이지 t2i 파이프라인·chatpage 리모트설정·수집 북마크릿(인스타/핀터레스트/쿠팡/유튜브)·t2i 재현도 비교보드 등.

> 🔎 **새 기능 짜기 전 능력 인덱스부터.** 영상·이미지·TTS·캐러셀·크롤·발행·LLM호출을 새로 만들기 전 **`python3 ~/Projects/cap.py "<하려는 것>"`** 로 이미 있는지 물어라(의미검색, 있으면 재사용). 전체 지도 `~/Projects/CAPABILITIES.md`(capabilities_scan.py가 매일 05:30 자동생성, 표는 손대지 마). 같은 능력이 15개 저장소에 흩어져 재발명이 반복된다(2026-07-14 릴스 3회 재작성 사고).
> ⚠️ 브랜드 진실: 모멘터스=강형모 1인 AI 스튜디오(컨테이너), 팔레트 흰+블루 #3182f6+잉크 미니멀. 이미지 생성 정본=CREAGEN(`mcp__creagen__*`), fal은 벡터화 전용.

> 🏠 **랜딩(the-moment.us/)은 [docs/LANDING.md](docs/LANDING.md) 가 정본.**
> `index.html` 은 생성물이다 — 직접 고치면 매일 05:45 재빌드가 지운다.
> 랜딩 스타일·구조는 `scripts/gen_site.py` 의 `KB_CSS` + 랜딩 빌더에서만 고친다.
> 브랜드 색(§3)·타이포 척도(§4)는 `KB_CSS` 최상단 토큰에만 산다 — 개별 규칙에 색·px 를 박지 마라.
> 로컬 미리보기 포트 함정과 cloudflared 주의사항(§7)도 거기 있다.
> 🧭 **제품을 만들고·묶고·전시하는 규칙은 [docs/PRODUCT_SYSTEM.md](docs/PRODUCT_SYSTEM.md) 가 정본.**
> 새 제품 추가·리스트 개편·앱 페이지 작업 전에 먼저 읽어라. tools/apps/products 축 판단,
> 리스트 정렬축, 에이전트용 전시 층(층 2), `/l/` 영구 링크 규칙, 접는 절차가 거기 있다.
> 💳 **결제·계정(pay./id.) 구조는 [docs/PLAN_PAY_LAYER.md](docs/PLAN_PAY_LAYER.md) 가 정본.**
> 결제 버튼·주문·이행·문의·로그인을 건드리기 전에 먼저 읽어라. PG(포스타트) 서면 확인 사항,
> "sku만 넘긴다" 계약, 이메일=신원 결정, 하면 안 되는 것 목록(§8)이 거기 있다.
> `PLATFORM_TOPOLOGY.md` §6·§7과 충돌하면 **PLAN_PAY_LAYER 가 최신**.
> 🗣 **아직 안 정해진 큰 질문(모멘터스 정체성·퍼널 방향·리스트 축)은
> [docs/DISCUSSION_MOMENTUS_SHAPE.md](docs/DISCUSSION_MOMENTUS_SHAPE.md).**
> 대표가 "그 마크다운 읽고 얘기하자"고 하면 그 문서의 §0 사용법대로 진행한다.
> 잠정 입장에 동의부터 하지 말고 반박거리 편을 먼저 들어 볼 것.
