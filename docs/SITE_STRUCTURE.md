# the-moment.us — 사이트 골격 & 제품 정리 (마스터)

> 2026-07-08 정리. "전시장 아니라 나 대신 일하는 본체" 전략의 **실행 지도.**
> 전략 원문: [`docs/APEX_STRATEGY.md`](./APEX_STRATEGY.md) (v1 + v2, `apex-strategy-handoff` 브랜치)
> 디자인 리뷰(랜딩·소개·상세 A/B·벤치마킹): [`design-review/index.html`](../design-review/index.html) · 아티팩트 발행됨

---

## 1. 한 장 요약

- **본체 = 껍데기(storefront) + 지그(재사용 틀).** 제품 소스는 각자 별개, 사이트는 **랜딩·법정·FAQ·귀환갈고리**만.
- **방문자가 주인공.** 도착 → 무료도구 1클릭 체험 → "와 되네" → 누적 타임라인 → 팬.
- **디자인 방향: A안(THE CHANGELOG) 척추 + B안 히어로(1클릭 도구) 접목.** Toss 토큰 + Pretendard 셀프호스트.

## 2. 제품 인벤토리 (6종, 전부 무료)

| 제품 | 종류 | 소스 위치 | 사이트 랜딩 | 상태 |
|---|---|---|---|---|
| 인스타 인기순 정렬 | 북마크릿 | `bookmarklets/insta-rank.js` (캡처 대기) | `apps/insta-rank/` (미생성) | 소스 있음 |
| 유튜브 인기순 정렬 | 북마크릿 | `bookmarklets/youtube-rank.js` (캡처 대기) | 미생성 | 소스 있음 |
| 핀터레스트 원본 추출 | 북마크릿 | `bookmarklets/pinterest-grab.js` (캡처 대기) | 미생성 | 소스 있음 |
| 퀵팡 (쿠팡 퀵보기) | 북마크릿 | `apps/quickpang/` | `apps/quickpang/` (index+mobile) ✅ | 라이브·1만 팔로워 검증 |
| ChatPage | 크롬 확장 | `~/Projects/ChatPage` (별도 repo) | `apps/chatpage/` remote-config만, 랜딩 미생성 | 라이브 v2.9.7·별점5.0 |
| her | 크롬 확장 | `/Volumes/Seagate Backup/Projects/her` (별도 repo, 클론됨) | 미생성 | v1.0.9·브랜딩 다듬기 필요 |

**카테고리 2종:** 북마크릿(설치X, 드래그) 4 · 크롬 확장(스토어 설치) 2.

## 3. 리포 배치 규칙 (어디에 뭘 두나)

- **momentus repo(this) = 껍데기.** `apps/<제품>/`(랜딩) · `bookmarklets/`(북마크릿 소스) · `legal.html`·`privacy-policy.html`(공용 법정, 이미 있음) · `design-review/`(디자인 시안).
- **무거운 독립 앱 = Seagate `Projects/`** (Reci·nightwork·toonfactory·**her**). 소스는 여기, 사이트엔 랜딩만.
- **ChatPage = `~/Projects/ChatPage` 그대로 유지**(이동 X — 슬랙봇 self-heal 모니터가 경로 물고 있음). 사이트엔 랜딩만 추가.
- **연결 = 매니페스트 한 줄** (지그). 소스와 페이지는 의도적 분리, `products.json`이 잇는다.

## 4. 지금 있는 것 vs 만들 것

**있음(재사용):** legal·privacy 법정페이지 · quickpang 랜딩 · apps 쉘 · her·ChatPage 소스 · 디자인 시안
**없음(빌드):** ① 대문 홈페이지(apex `/`) ② 공용 스킨/지그(드래그버튼+FAQ+귀환갈고리 한 벌) ③ 북마크릿 3종 랜딩 ④ ChatPage·her 랜딩 ⑤ her 브랜딩 다듬기 ⑥ `products.json` 매니페스트

## 5. 다음 순서 (트래픽 0에서도 이득 나는 것부터)

1. **방향 확정** — 디자인 리뷰에서 A/B/C + 상세 A안/B안 중 선택
2. **지그 + `products.json`** — 제품 = 필드 채우기
3. **대문 홈** (선택된 방향) — Astro + CF Pages (mark와 동일 스택)
4. **북마크릿 소스 캡처 + 3종 랜딩** + 귀환 갈고리 규격
5. **her·ChatPage 랜딩** + her 브랜딩
6. AEO 앵커(정량+엔티티 한 줄) → 페이지 밖 시딩

## 6. 미결 (형 결정 필요)

- [ ] 디자인 방향 (A/B/C, 상세 A안 vs B안)
- [ ] `apex-strategy-handoff` 브랜치를 main에 합칠지 (그 브랜치엔 옛 8th 에셋 삭제도 포함 — 의도된 정리인지 확인 필요)
- [ ] her 최종 이름/포지션 ("바이브코딩 필수템" 유지?)
