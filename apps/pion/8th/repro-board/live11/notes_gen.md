# ref11 재료 생성 노트 (repro_gen)

원본 픽셀 미사용. 크롭(photo_hero/a/b/c/d)을 비전으로만 판독 → nano-banana-2 t2i 1K → PIL 센터크롭/리사이즈로 슬롯 정확 크기.

## 슬롯별 프롬프트

### gen_hero (225×157, AR 3:2→크롭, raw 1264×848)
> Close-up product photography of a modern designer sofa, plush cream-white linen seat and back cushions, one rounded cylindrical bolster armrest cushion on the left, smooth caramel-tan leather wrapped wooden frame visible along the armrest and base, warm beige seamless studio background, soft diffused light, premium furniture catalogue style, photorealistic. Absolutely no text, letters, logos, or watermarks.

### gen_a (254×136, AR 16:9, raw 1376×768)
> Product photography of a three-seat modern sofa, cream off-white fabric upholstery with two wide seat cushions and two small round bolster cushions at each side, slim exposed warm wood frame accents and light tapered wooden legs, straight-on front view, plain warm ivory seamless studio background, soft even lighting, furniture catalogue style, photorealistic. Absolutely no text, letters, logos, or watermarks.

### gen_b (127×136, AR 1:1→크롭, raw 1024×1024)
> Product photography of a mid-century modern armchair, cream white upholstered seat and angled backrest, dark walnut wooden frame with slanted armrests and tapered legs, three-quarter view, plain light warm-gray seamless studio background, soft shadow under the chair, vintage Scandinavian design, photorealistic. Absolutely no text, letters, logos, or watermarks.

### gen_c (127×78, AR 3:2→크롭, raw 1264×848)
> Product photography of a low lounge armchair with thick soft cream boucle cushions and a light oak wooden frame with wide flat armrests, side three-quarter view, plain warm beige seamless studio background, soft diffused lighting, Scandinavian furniture catalogue style, photorealistic. Absolutely no text, letters, logos, or watermarks.

### gen_d (124×139, AR 1:1→크롭, raw 1024×1024)
> Product photography of two walnut wood dining chairs with vertical slat backrests and pale gray upholstered seats, one chair standing slightly behind the other, three-quarter view, plain cool light-gray seamless studio background, soft even light, minimalist furniture catalogue, photorealistic. Absolutely no text, letters, logos, or watermarks.

## 평가 (1트라이 통과, 재생성 없음)

- **hero**: 재현도 높음. 크림 리넨 쿠션 + 원통 볼스터 + 캐러멜 가죽 프레임 클로즈업 — 원본의 핵심 아이덴티티(가죽 랩 프레임 소파 디테일컷) 그대로. 원본 대비 볼스터가 조금 더 둥근 공 형태.
- **a**: 재현도 높음. 3인 크림 소파 + 양측 볼스터 + 우드 프레임/레그 정면 제품컷 성립. 원본보다 우드 프레임 노출이 약간 더 많음.
- **b**: 재현도 높음. 다크 월넛 프레임 + 크림 좌판의 미드센추리 암체어 3/4뷰 — 원본과 같은 유형·톤. 팔걸이 각도 디테일만 상이.
- **c**: 재현도 높음. 라이트 오크 프레임 + 크림 부클 라운지체어. 127×78 가로 크롭에서 체어가 중앙에 온전히 들어옴.
- **d**: 재현도 높음. 월넛 슬랫 등받이 다이닝체어 2개 전후 배치 + 쿨그레이 배경 — 원본 구도 매치.

## 한계
- 콜라주 5컷의 배경톤이 원본은 한 세트(같은 스튜디오 촬영)처럼 통일돼 있으나, 생성물은 컷별로 미세하게 다른 베이지/그레이 — 세트 일관성은 t2i 개별 생성의 구조적 한계.
- 제품 동일성(같은 소파의 클로즈업=hero, 전신=a) 보장 불가 — hero와 a는 유사 계열이지만 동일 제품은 아님.
