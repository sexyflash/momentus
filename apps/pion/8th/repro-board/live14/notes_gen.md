# ref_14 재료 생성 노트 (M9, repro_gen)

원본 픽셀 미사용. 사진 1종을 t2i로 재생성, 아이콘 4종은 기존 repro.html의 인라인 SVG 그대로(원래부터 드로잉).

## 슬롯: photo_top (816×411)

- 모델: fal `nano-banana-2`, t2i, aspect 16:9, 1K → 1376×768 수신 → PIL 중앙(수직 bias 0.55) 크롭 693행 → 816×411 리사이즈.
- 원본 판독: 우드 테이블 위 로제 와인병(크림 라벨)·리브드 유리컵·체리 유리볼(좌), 늘어진 그린 스프리그(중), 야생화 꽃병(우), 전면에 "Hour" 인쇄 화이트 파우치, 베이지 벽+의자 등받이, 따뜻한 창측광.
- "Hour" 텍스트는 프로토콜에 따라 **무지(blank) 파우치**로 대체.

### 프롬프트 전문
> Warm lifestyle photograph on a rustic natural wooden dining table. On the left: a tall bottle of rosé wine with a plain blank cream paper label, an empty ribbed glass tumbler beside it, and a small clear glass bowl filled with fresh red cherries at the front-left edge. In the middle: a loose sprig of trailing green leaves lying on the table. On the right: a clear glass vase holding a casual bouquet of small yellow, purple and white wildflowers with greenery. In the center-right foreground: a plain blank white cotton canvas pouch lying flat on the table, completely unprinted. Background: warm beige plaster wall, the back of a light wooden chair softly visible behind the table. Soft warm afternoon window light from the left, cozy natural film-photo tone, gentle shadows, muted warm palette. Absolutely no text, letters, logos, or watermarks.

## 평가 (구도/무드 재현도)

- **구도**: 좌 와인병+컵+체리볼 / 중 스프리그 / 우 꽃병 / 전면 파우치 — 오브젝트 배치·좌우 균형이 원본과 거의 동일. 1트라이 채택. 재현도 상.
- **무드**: 웜 베이지 벽, 좌측 창광, 필름톤 — 원본의 오후 라이프스타일 무드 일치. 꽃 색이 원본(옐로·퍼플)보다 퍼플 비중이 약간 높음.
- **차이**: 파우치가 원본보다 약간 작고 스트링 파우치 형태(원본은 납작한 대형 파우치+Hour 인쇄). 텍스트 금지 규칙상 의도된 차이. 와인 병 라벨은 blank 크림으로 클린함.
- 텍스트/로고 누출: 없음.

## 산출물
- `gen_photo_top.png` (816×411), `repro_gen.html`, `gen_trim.png` (816×1205), `gen_layer.png` (재료 레이어), 프롬프트 본 문서.

## 한계
- t2i 특성상 소품의 정확한 기물(리브드 컵 디테일, 체리 개수감)은 근사. 색온도는 원본보다 살짝 밝음.
- 트림 컷 y=1205 (원본 repro 1206과 ±1행).
