# ref_16 재료 생성 노트 (M9, repro_gen)

원본 픽셀 미사용. 사진 2종 t2i 재생성 + 보태니컬 리스 일러스트를 인라인 SVG로 직접 드로잉.

## 슬롯 1: photo_main (246×268)

- 모델: fal `nano-banana-2`, t2i, aspect 1:1, 1K → 1024×1024 수신 → PIL 중앙 폭크롭 940 → 246×268 리사이즈.
- 원본 판독: 베이지 석회암 덩어리 위/주변에 앰버 유리 에센셜오일 병(다크 라벨)과 매트 블랙 원형 틴(십자가 각인+금박 텍스트), 웜 크림 배경, 좌상단 사광, 클래식 아포테케리 무드.
- 원본의 십자가 각인·"LE TOV" 금박 텍스트는 **전부 blank 표면으로 대체**(텍스트·로고 금지).

### 프롬프트 전문
> Elegant classic apothecary product photography. Several small dark amber glass essential-oil bottles with matte black caps and completely blank unlabeled dark surfaces, standing in the foreground, together with a few small round matte black metal tins with smooth plain lids placed on top of and beside chunky rough-hewn beige limestone rocks stacked behind them. Warm cream-beige seamless studio background, soft directional warm light from the upper left casting gentle long shadows, muted earthy beige-brown palette, luxurious calm still-life mood, slightly elevated straight-on camera. Absolutely no text, letters, logos, engravings, or watermarks on any surface.

### 평가
- **구도**: 후면 석회암 스택 + 틴(돌 위) + 전면 앰버 병 열 — 원본 배치 문법 동일, 1트라이 채택. 재현도 상.
- **무드**: 웜 베이지·사광·롱섀도 일치. 병 수가 원본(4병)보다 많아 밀도가 약간 높음.
- **차이**: 라벨·십자가·금박 전부 무지 — 규칙상 의도된 차이.

## 슬롯 2: photo_caps (246×150)

- 모델: 동일, aspect 16:9, 1K → 1376×768 → 중앙 폭크롭 1260 → 246×150.
- 원본 판독: 매트 블랙 원형 틴 3개 매크로 클로즈업(눕고·서고·기운 배치), 금박 텍스트 라벨, 크림 배경 얕은 심도.

### 프롬프트 전문
> Macro close-up product photograph of three small round matte black metal tins with smooth completely blank lids, arranged casually on a warm cream-beige surface: one tin lying tilted on its edge on the left, one standing upright in the center facing the camera, one leaning at an angle on the right. Very shallow depth of field with soft focus falloff, warm soft beige gradient studio background, premium minimal cosmetic mood, warm gentle studio lighting. Absolutely no text, letters, logos, embossing, or watermarks.

### 평가
- **구도**: 3틴 좌눕/중정면/우기움 배치 그대로. 얕은 심도·크림 패브릭 표면까지 재현. 재현도 상.
- **차이**: 원본의 금박 타이포 라벨 부재(의도), 원본보다 틴이 화면에 크게 잡힘.

## 슬롯 3: wreath (140×78) → SVG 드로잉

- 원본 판독(5x 확대): 인그레이빙 스타일 보태니컬 카르투슈 — 이중 라운드 프레임, 상단 새 2마리+중앙 꽃, 좌우 로제트, 잎 덩굴, 내부 이탤릭 세리프 성구 3행("For I can do everything / through Christ, / who gives me strength.") + 하단 "LE TOV".
- 재현: viewBox 140×78 인라인 SVG. 이중 라운드 프레임 + 좌반부 덩굴·잎·새·로제트를 `<g id="halfL">`로 그리고 `scale(-1,1)` 미러로 대칭 완성. 텍스트는 Cormorant Garamond italic(성구)+Cinzel("LE TOV") SVG text. 스트로크 `#3b3b3b` 0.6–0.9.

### 평가
- 카르투슈 구조·성구 타이포·대칭 보태니컬 어휘(새·로제트·잎 덩굴) 재현. 원본의 조밀한 동판화 밀도(스크롤워크·세부 꽃송이)는 단순화 — 재현도 중상.

## 산출물
- `gen_photo_main.png` (246×268), `gen_photo_caps.png` (246×150), `repro_gen.html` (wreath SVG 내장), `gen_trim.png` (246×1351), `gen_layer.png`.

## 한계
- 246px 폭 슬롯이라 t2i 1K 결과를 강하게 다운스케일 — 디테일 손실은 원본 크롭과 동일 조건.
- wreath는 인그레이빙 밀도를 손드로잉 SVG로 완전 재현하기 어려워 요소 어휘 수준의 근사.
- 트림 컷 y=1351 (원본 repro와 동일).
