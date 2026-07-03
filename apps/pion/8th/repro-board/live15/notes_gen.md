# ref_15 재료 생성 노트 (M9, repro_gen)

원본 픽셀 미사용. 사진 1종 t2i 재생성 + 아이콘 5종(원본은 크롭 img였음)을 전부 인라인 stroke SVG로 직접 드로잉해 교체.

## 슬롯 1: photo_hero (1000×949)

- 모델: fal `nano-banana-2`, t2i, aspect 1:1, 1K → 1024×1024 수신 → PIL 수직 bias 0.45 크롭 972행 → 1000×949 리사이즈.
- 원본 판독: 크림 화이트 미니멀 주방(3D 렌더 톤), 좌측 톨 수납장, 벽면 상부장+연한 우드 카운터, 로만셰이드 창, 전면 아일랜드에 베이지 패브릭 스툴 2개(블랙 철제 다리). 중앙부는 패널이 덮으므로 주변부 재현이 핵심.

### 프롬프트 전문
> Bright minimalist Korean apartment kitchen interior, clean photorealistic 3D architectural render style. Cream-white flat-front cabinetry: tall pantry units on the left, upper wall cabinets and lower counters along the back wall with a pale wood-look countertop, small under-mounted sink with a slim white faucet. In the foreground center-right, a white kitchen island counter with two rounded beige fabric-upholstered stools with thin black metal legs tucked at it. A window with a sheer white roman shade on the back-left, matte warm-white walls and pale floor. A few subtle props only: a small potted plant, a wooden cutting board, a white ceramic kettle. Soft even diffuse daylight, airy ivory and warm beige palette, straight-on wide view, cozy minimal interior mood. Absolutely no text, letters, logos, or watermarks.

### 평가
- **구도**: 좌 톨장 / 후면 상부장+창(로만셰이드) / 전면 아일랜드+베이지 스툴 2개 — 원본 요소 전부 재현, 1트라이 채택. 스툴 형태(라운드 패브릭+블랙 다리)까지 일치. 재현도 상.
- **무드**: 아이보리 균질광 3D 렌더 톤 일치. 원본보다 채도가 아주 약간 낮고 우드 카운터 면적이 작음.
- **차이**: 창 위치가 원본(중앙 뒤) 대비 약간 우측, 후드·타일 등 디테일 생략됨 — 패널이 중앙을 덮어 체감 차이 적음.

## 슬롯 2: 아이콘 5종 → stroke SVG 드로잉 (t2i 금지 준수)

원본 크롭(icon_utensils 65×60, icon_step1~4 100×88)을 눈으로 판독 후 재작도. 팔레트: 다크 스트로크 `#26241F`, 옐로 `#FFD54F`, 크림 `#FBE9DC`, 라이트블루 `#BFDCE0`/`#9FC3CB`, 유텐실 브라운 `#8C7F6E`.

- **icon_utensils**: 행잉 레일 + 고리 3개, 거품기(발룬 3획)·슬롯 터너·유텐실 크록(수직 손잡이 3개) — 원본 구성 동일.
- **icon_step1** (실측): 줄자 — 원형 바디 + 옐로 상면 타원 + 우측 눈금 스트립.
- **icon_step2** (철거): 판자를 어깨에 맨 작업자 스틱피겨 + 옐로 안전모 + 좌하 벽돌 패치.
- **icon_step3** (보양·시공): 옐로 상/하 보양 밴드 + 상단 화이트 패널열 + 라이트블루 타일 3장 + 우측 시트 라인.
- **icon_step4** (청소): 크림 돔 바디 캐니스터 청소기 + 게이지 다이얼 + 블루 호스(굵은 블루 스트로크+다크 심선) + 노즐.

### 평가
- 실루엣·팔레트·스트로크 무드는 원본과 동급으로 읽힘. step1·3·4 재현도 상, step2는 원본(디테일 많은 인물 일러스트) 대비 단순화가 커서 재현도 중.

## 산출물
- `gen_photo_hero.png` (1000×949), `repro_gen.html` (아이콘 SVG 내장), `gen_trim.png` (1000×1749), `gen_layer.png`.

## 한계
- 아이콘 5종은 프리핸드 재작도라 세부 곡률·디테일 밀도는 근사(특히 step2 인물).
- gen_layer.png에서는 프로토콜 주입 규칙(svg opacity 0)에 따라 드로잉 아이콘·스탬프도 함께 숨겨짐 — 사진 재료만 남는 것이 의도.
- 트림 컷 y=1749 (원본 repro 1750과 ±1행).
