# ref_12 재료 생성 노트 (M9) — 하루끝베개

원본 픽셀 0% — 모든 사진 재료를 nano-banana-2 t2i로 재생성 (원본은 Read 비전 판독만).
베이크 텍스트(구조 태그·온도 뱃지·9cm 치수)는 t2i 금지 대상이므로 **PIL 직접 드로잉**으로 합성
(AppleSDGothicNeo Bold — 프로토콜 2항 "그래픽은 직접 드로잉" 준용).

## 슬롯별 t2i 프롬프트 (전부 1트라이 통과, 재생성 0회)

### gen_top.png (301×110 ← 21:9 1584×672 센터크롭)
> Top-down product photograph of an ergonomic pillow with a triangular lattice grid mesh texture surface, cream ivory colored TPE-style mesh material, gently curved contour edge at the front, soft even studio lighting, light warm beige-gray palette. On the right side of the frame, a circular magnified detail inset with a clean white ring border showing a close-up cross-section of the pillow's two stacked mesh layers (finer mesh on top, coarser mesh below). Wide panoramic crop, clean minimal background, Korean e-commerce product detail page photography style. Absolutely no text, letters, numbers, logos, or watermarks.

+ PIL: 다크 라운드 태그 "상단구조"(243,6) / "하단구조"(208,86), 흰 9px.

### gen_test_left.png (118×114 ← 1:1)
> Lifestyle photograph of a young Asian woman sleeping on her side on a plain fluffy white cotton pillow, eyes closed, peaceful expression, warm cozy bedroom with soft warm amber window light in the background. In the upper left corner of the frame, a square inset panel showing a thermal infrared camera view of a person's head resting on a pillow, rendered in hot red, orange and yellow heat-map colors indicating trapped body heat. Natural beauty lifestyle tone, soft focus background. Absolutely no text, letters, numbers, logos, or watermarks.

+ PIL: "32.4℃" 흰 13px bold (5,3), 그림자 1px.

### gen_test_right.png (118×114 ← 1:1)
> Lifestyle photograph of a young Asian woman lying on her back sleeping restfully on a low ergonomic contour pillow with a subtle grid mesh texture, lips slightly parted, bright clean bedroom with soft neutral daylight, white bedding, high-key airy tone. In the upper left corner of the frame, a square inset panel showing a thermal infrared camera view of a person's head resting on a pillow, rendered mostly in cool dark blue and purple heat-map colors indicating very low heat. Natural beauty lifestyle tone. Absolutely no text, letters, numbers, logos, or watermarks.

+ PIL: "23.7℃" 흰 13px bold (5,3).

### gen_9cm.png (301×220 ← 4:3 1200×896 센터크롭)
> Bright airy lifestyle photograph of a young Asian woman in a white sleeveless top sleeping comfortably on her side on a medium-height white pillow, lying toward the right of the frame with her face in gentle side profile, serene closed eyes, white bedding, high-key soft daylight, clean minimal bedroom. In the lower left corner of the frame, a rectangular inset panel showing a medical X-ray radiograph of a human cervical spine and neck in glowing blue-white tones on a black background, horizontal orientation with neatly aligned vertebrae. Korean bedding brand detail page style. Absolutely no text, letters, numbers, logos, or watermarks.

+ PIL: 파랑 점선 치수선 x276 (y118–200, 끝단 틱) + "9cm" 17px bold (239,146).

### gen_rack.png (301×168 ← 16:9)
> Product photograph of a single white ergonomic contour pillow with an embossed wavy grid texture, freshly washed and lying flat on a white metal wire laundry drying rack, viewed from a slightly elevated three-quarter angle, clean bright white studio background fading to very light gray, soft even diffused lighting, minimal composition. Absolutely no text, letters, numbers, logos, or watermarks.

## 결과 평가 (구도/무드 재현도)

| 슬롯 | 구도 | 무드 | 비고 |
|---|---|---|---|
| gen_top | ◎ | ◎ | 격자 베개+우측 서클 인서트(2층 단면) 한방에 재현. 원본보다 격자 팔레트가 골드톤(원본은 그레이지) |
| gen_test_left | ◎ | ◎ | 좌상단 열화상 인서트(적황)+측면 수면+웜톤 침실 — 원본 문법 그대로 |
| gen_test_right | ○ | ◎ | 쿨블루 인서트+등면 수면+하이키. 원본의 "입 벌리고 정면" 앵글이 측면-등면 절충으로 |
| gen_9cm | ◎ | ◎ | 옆으로 누운 여성+좌하 경추 엑스레이 인서트+9cm 치수 — 원본 정보 구조 완전 재현 |
| gen_rack | ◎ | ◎ | 흰 건조대 위 컨투어 베개, 화이트 배경. 원본과 거의 동일 문법 |

## 한계
- 원본의 베개 제품 아이덴티티(특정 격자 패턴·컬러)는 재현 불가 — 유사 카테고리 제품으로 대체됨 (gen_top 골드 격자 vs 원본 그레이지 격자, gen_rack 웨이브 엠보 vs 원본 도트 엠보).
- 인물이 원본과 다른 사람(당연) — 앵글·조명 문법만 일치.
- 열화상 인서트의 온도 스케일 바(원본 인서트 하단 컬러바)는 생성물에 없음.
- gen_top 서클 인서트가 우측 프레임에 살짝 클리핑(원본도 우측 에지 접함 — 허용).
- PIL 폰트가 AppleSDGothicNeo(원본은 불명 고딕) — 베이크 텍스트 서체 미세 차이.

## 자평
재료 재현도 **~88%**. 5슬롯 전부 1트라이 통과, 인서트(서클/열화상/엑스레이) 같은
합성 문법까지 t2i 단독으로 성립. 잔여 갭은 제품 아이덴티티(격자 패턴 색·형)와
열화상 컬러바 디테일.

## 생성 원본 (fal, 1K)
- top: v3b.fal.media/files/b/0aa0b2b6/DNohe47vPmJ827JBzLThR_3HN9nxyV.png
- test_left: …0aa0b2b7/36X9LfyKu3_Vm_LiEFNk7_lThbwNFx.png
- test_right: …0aa0b2b8/iIPJlrFlfhG39NTpuWVWF_tIxT8KAN.png
- 9cm: …0aa0b2b9/stDw2jgzk4tlH5BUj8S87_6UA0itRe.png
- rack: …0aa0b2ba/zC3IuVB8tOV_y_lX0GoEA_QJHGq4Pr.png

## 산출물
`gen_top/test_left/test_right/9cm/rack.png`, `repro_gen.html`(src만 교체),
`gen_trim.png`(301×1464), `gen_layer.png`(텍스트 투명 — 사진+베이크 주석만 잔존 확인).
