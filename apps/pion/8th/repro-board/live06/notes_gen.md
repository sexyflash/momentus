# ref06 repro_gen — 재료 생성 노트 (M9)

원본 픽셀 미사용. photo.png는 Read(비전)로만 판독, t2i로 재생성.

## 슬롯: photo (455×550, left:245 top:425)

- 모델: fal nano-banana-2 (t2i), aspect_ratio 4:5, 2K → PIL 센터크롭(0.827:1) 후 455×550 리사이즈
- 트라이: 1회 (재생성 불필요)

### 프롬프트 전문
> Straight-on front view product photograph of a modern Scandinavian wardrobe made of light natural oak wood with warm honey grain. Layout: the left two-thirds has two tall hinged doors meeting in the middle with two small round wooden knobs side by side at mid height, and below them three stacked drawers each with two small round wooden knobs; the right third is one full-height tall door panel with a slim vertical brass-gold handle groove at its left edge. Slightly rounded top corners, short tapered wooden legs with small brass-gold feet caps. Evenly lit soft studio lighting, seamless very pale off-white background with a faint warm-lavender tint, subtle soft shadow under the legs, clean minimal furniture e-commerce product shot. Absolutely no text, letters, logos, or watermarks.

### 평가 (구도/무드 재현도)
- 구도: 최상. 좌측 2도어(중앙 원형 손잡이 2개)+하단 3단 서랍, 우측 통짜 도어+세로 황동 핸들, 테이퍼드 다리+황동 발캡, 정면 뷰까지 원본 구성要素를 거의 그대로 재현. 원본과 달리 서랍이 좌측 2/3 폭 전체를 차지하는 비례 차이 정도.
- 무드: 상. 밝은 오크 결, 연보라끼 도는 옅은 배경이 페이지 배경(#f8f6fb)과 자연스럽게 이어짐. 생성본이 원본보다 약간 밝고 노란기가 덜함.

### 한계
- 서랍 손잡이가 원본(칸당 2개, 지그재그 배치)과 달리 칸당 2개 정렬형.
- 원본의 우측 도어 이중 프레임 라인은 단순화됨.

## 렌더
- gen_trim.png 736×973, gen_layer.png(텍스트 투명+svg 숨김) 동일 크기.
- 트림: 알고리즘 결과 960(생성 사진 하단이 배경에 가깝게 페이드) — 레이아웃 동일하므로 원본 trim 경계 973으로 크롭.
