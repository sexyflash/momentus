# 이미지 연출 정본 — 도구/제품 페이지

> 대표 지시(2026-09-01): *"이미지 생성을 위해 시도하고 사용하는 프롬프트들 좀 잘 저장해.
> 다른 페이지 할 때 어떤 식으로 연출을 요구했는지 기록을 해야 톤앤매너를 유지도 하고 운영하지."*
> **새 페이지 이미지를 만들기 전에 이 문서를 먼저 읽고, 만들고 나면 여기에 추가해라.**

## 0. 북극성 — 이 톤을 벗어나지 마라

기준 사진: 밝은 자연광 스칸디나비아 카페 인테리어 (대표 지정, 2026-09-01)
`https://i.pinimg.com/1200x/3d/bb/c9/3dbbc97c1cc61f5bc03058b4bd6488a3.jpg`
→ 로컬 사본 `assets/tools/_ref/mood.jpg`

- **밝고 따뜻하다.** 크림 벽 · 물푸레/오크 · 왼쪽에서 드는 햇빛 · 긴 부드러운 그림자
- 어두운 스튜디오, 검은 배경, 창고, 게이밍 룸 톤 → **폐기**(2026-09-01 반려)
- 소품은 적게. 화면 주변에 여백을 넉넉히.

## 1. 🔴 절대 규칙 — 스크린샷을 i2i 에 넣지 마라

캡처를 그대로 i2i 참조로 주면 모델이 **화면 안 한글·숫자를 다시 그린다.** 실측(2026-09-01):

| 실제 | i2i 결과 |
|---|---|
| 조회 380,000 | 조회 **280,000** |
| #3 | **#9** |
| 다시 정렬 | 다시 **정멸** |
| 45개 정렬 완료 | **48가 전점 전호** |

**제품 화면이 거짓말을 하는 이미지**가 된다. 그래서 방식은 항상 이것:

```
i2i        → 장면(방·책상·모니터). 화면은 순수 마젠타 판으로 비워 둔다.
코드(PIL)  → 마젠타를 찾아 실제 캡처를 원근 맞춰 워프해 끼운다. 픽셀 그대로.
```

스크립트: `scratchpad/cap/screen.py`(fit / fit_multi) · `build2.py`(6컷 생성)

## 2. 모델·파라미터

| 용도 | 모델 | 해상도 | 비고 |
|---|---|---|---|
| 히어로(헤더) | `gpt` (gpt-image-2) | **1K** | 대표 지시 — 지글거림이 덜하다 |
| 장면·배경 일반 | `nb-pro` | 2K | 질감이 풍부 |
| 시안 여러 장 | `nb2` | 1K | |

⚠️ `nb2-lite`(6크레딧)는 현재 배선이 끊겨 있다 — 부르면 조용히 `gpt`(25크레딧)로 간다.
자세한 건 대표 승인 대기 중.

## 3. 프롬프트 원본 (그대로 복사해 쓰고, 소품만 바꿔라)

### 3-1. 장면 — 모니터 1대 (히어로용)

```
Recreate the light and material palette of the reference photograph — bright natural
daylight through a large window, warm cream walls, pale oak and ash wood, soft long
shadows, airy Scandinavian minimalism, calm and premium — as <직업/상황>.

Composition: a wide pale oak desk seen straight on from a comfortable distance with
generous breathing room. ONE large widescreen monitor stands in the middle of the frame,
front-facing with only a very slight turn, its whole body visible including the stand,
not cropped, not tilted. Beside it: <소품 3~5개>. Tidy and sparse. Soft daylight from the
left, gentle shadows, high-key and warm, no darkness. Editorial interior photography,
35mm, natural colour.

CRITICAL: the monitor screen must be a perfectly FLAT, EVENLY LIT, PURE SATURATED MAGENTA
(#FF00FF) rectangle — completely empty. No content, no text, no icons, no reflections,
no glare, no gradient on the screen itself. Crisp straight edges. Nothing else in the
image may be magenta or pink.
```

### 3-2. 장면 — 모니터 2대 (전/후 비교용)

3-1 과 같되 이 문단으로 교체:

```
TWO identical widescreen monitors stand side by side in the middle of the frame, both
almost front-facing with only a very slight turn, both fully visible including their
stands, evenly lit, at the same size and height, with a small gap between them.
...
CRITICAL: BOTH monitor screens must be perfectly FLAT ... PURE SATURATED MAGENTA (#FF00FF)
```

### 3-3. 빈 배경 (카드/텍스트 얹을 때)

```
Recreate the light and material palette of the reference photograph as a completely EMPTY
backdrop: warm cream plaster wall bathed in soft natural daylight from the left, a pale oak
surface running across the lower third, gentle diagonal window light and long soft shadows,
faint dust in the light, calm Scandinavian minimalism, high-key and warm.

Absolutely nothing in the frame — no furniture, no objects, no plants, no devices, no
screens, no people, no text, no letters, no numbers, no logos. Just wall, light, shadow and
the wooden surface. The central area must stay clean and uncluttered so cards can be placed
on top later. Editorial interior photography, 35mm, natural colour.
```

### 3-4. 도구별 소품 (톤은 같게, 소품만 다르게)

| 도구 | 상황 | 소품 |
|---|---|---|
| 이미지 수집기 | 인테리어 디자이너 책상 | 무드보드 시트, 패브릭·스톤 스와치, 컬러칩, 세라믹 화병 |
| 유튜브 인기순 | 영상 작가의 책상 | 슬림 콘덴서 마이크, 밝은 회색 헤드폰, 노트와 펜 |
| 쿠팡 퀵보기 | 온라인 셀러 작업대 | 크라프트 택배 박스 2~3개, 라벨 프린터, 종이테이프, 리넨 머그 |

## 4. 함정 (다 실측으로 데인 것들)

- **마젠타 테두리** — 경계는 안티에일리어싱으로 번진다. 마스크를 *깎으면* 그 띠가 드러나
  보라 테두리가 남는다. **넓혀서(MaxFilter) 덮고**, 워프도 2% 오버스캔.
- **검은 여백** — 크롭 상자가 이미지 밖으로 나가면 PIL 이 검게 채운다. 세로가 모자라면
  가로를 잘라 비율을 맞춰라(`build2.hero_crop`).
- **밝은 장면에 halo 를 세게 주지 마라.** 어두운 장면 기준값(glow .55)을 그대로 쓰면 뜬다.
  밝은 장면은 `glow=0.10, dim=1.0`.
- **히어로 컨테이너는 2.4:1**(`.vd-hero{height:600px}` × 1440). 16:9 를 넣으면 위아래가 잘린다.
  히어로는 2560×1080 로 뽑아라.
- **캡처는 정사각 크롭을 못 견딘다.** `.vd-duo`/`.vd-wide` 기본값이 `aspect-ratio:1` 이라
  화면이 잘려 못 읽는다 — 실제 캡처 세트에는 `.sh` 변형(가로형 contain)을 붙인다.

## 5. 캡처 쪽 규칙

- 데모는 **기능이 실제로 보이는 상태**로 찍어라. 쿠팡은 '옵션·재고 보기'를 눌러
  재고 칩이 펼쳐진 화면이어야 비교가 된다(대표 지적). 검색어도 옵션이 있는 상품군으로
  (`무선마우스` ✗ 대부분 '옵션 없음' / `여아 신발` ✓ 사이즈 5/5·23/24·14/14).
- 전/후 두 장은 **같은 크롭·같은 높이**로 잘라야 나란히 놓았을 때 비교가 된다.
