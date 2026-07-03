# ref_13 재료 생성 노트 (M9) — 아우라홈 가습기

원본 픽셀 0% — 인테리어 3분할 peek + 가습기 2분할 전부 nano-banana-2 t2i 재생성
(원본 crop은 Read 비전 판독만, i2i·텍스트 지우기 없음).

## 슬롯별 t2i 프롬프트 (전부 1트라이 통과, 재생성 0회)

### gen_left.png (58×154 ← 9:16 768×1376 센터크롭)
> Bright natural interior photograph of a light oak wooden dresser with round knob drawers against a warm white wall, a few small wooden toy figures and a tiny potted plant on top, a small natural wood children's chair and table in the foreground, warm Scandinavian nursery style, soft diffused daylight, tall vertical composition. Absolutely no text, letters, numbers, logos, or watermarks.

### gen_center.png (164×198 ← 4:5 928×1152 센터크롭)
> Cozy bedroom at night: a small glowing mushroom-shaped table lamp with warm orange light sits on a wooden nightstand beside a bed, a small vase of flowers next to the lamp, white rumpled duvet and pillows filling the foreground with soft dappled leaf shadows cast across the bedding, warm beige walls, intimate dim ambient evening light, vertical composition. Absolutely no text, letters, numbers, logos, or watermarks.

### gen_right.png (58×154 ← 9:16 센터크롭)
> Bright warm interior photograph of a slim wooden console table against a soft beige wall, ceramic vases with dried flowers and small green plants arranged on top, a white fabric-shade floor lamp standing behind the table, soft natural daylight from the side, cozy neutral-toned living room, tall vertical composition. Absolutely no text, letters, numbers, logos, or watermarks.

### gen_humid.png (314×238 ← 4:3 1200×896 센터크롭)
> Split-screen product photograph divided into two equal panels by a thin white vertical line down the middle: each panel shows the identical white cylindrical ultrasonic humidifier with a small round dial on its base, standing on a white table against a plain light gray studio background. In the left panel the humidifier emits a thin faint wisp of mist; in the right panel the same humidifier emits a thick dense tall plume of mist. At the exact center of the image, overlapping both panels, a circular inset badge with a clean white ring border showing a macro close-up of a brushed stainless metal rotary control dial. Clean minimal Korean home appliance detail page style. Absolutely no text, letters, numbers, logos, or watermarks.

## 결과 평가 (구도/무드 재현도)

| 슬롯 | 구도 | 무드 | 비고 |
|---|---|---|---|
| gen_left | ◎ | ◎ | 원목 서랍장+토이+아이 의자/테이블 — 원본 키즈룸 문법 그대로. 58px 슬릿에서 판독 동등 |
| gen_center | ◎ | ◎ | 머시룸 램프 웜글로우+흰 이불 잎사귀 그림자+꽃병 — 원본 무드 거의 동일 |
| gen_right | ○ | ◎ | 콘솔+드라이플라워+흰 스탠드. 원본보다 소품 밀도 높고 스탠드가 프레임 우측(원본 좌측 뒤) |
| gen_humid | ◎ | ◎ | 2분할+흰 세로 디바이더+좌 약미스트/우 강미스트+중앙 다이얼 서클 — 5개 구성요소 전부 한방 재현 |

## 한계
- gen_humid 중앙 다이얼의 "MAX" 각인·포인터는 텍스트 금지 규칙으로 미재현(무문자 다이얼).
- 가습기 제품 아이덴티티가 원본(하단 노브·테이퍼 실루엣)과 유사 카테고리 대체 — 좌우 개체 동일성은 유지되나 원본 SKU와는 다름.
- gen_left/right는 9:16 → 0.377 초슬림 크롭이라 원본 대비 시야가 좁음(피사체는 유지).
- 원본 humid는 좌우 앵글이 미묘하게 달랐는데(카메라 고정 2컷) 생성물은 거의 대칭.

## 자평
재료 재현도 **~90%**. 특히 gen_humid는 분할 구도+미스트 강약 대비+센터 서클 오버랩이라는
합성 문법을 t2i 단독으로 성립시킴. 인테리어 3분할은 슬림 크롭 후에도 원본과 같은
"공간 peek" 역할 수행. 잔여 갭은 제품 SKU 동일성과 다이얼 각인.

## 생성 원본 (fal, 1K)
- left: v3b.fal.media/files/b/0aa0b2bc/J8NPU_YRycKJA0g8gg7Ad_iWqUA1se.png
- center: …0aa0b2bd/QaSNlCwFrPkqnt_BSpGBH_I0voP0jb.png
- right: …0aa0b2be/6sQ-CmyaiQI2bXJ4nC0YZ_lM9R2dT8.png
- humid: …0aa0b2bf/CmLXwVGn9LxW9LoFP4krx_UOl2ofbH.png

## 산출물
`gen_left/center/right/humid.png`, `repro_gen.html`(src만 교체),
`gen_trim.png`(354×1425 — 원본 트림 1426과 1px 차), `gen_layer.png`(텍스트 투명 검증 통과).
