# ref08 재료 생성 노트 (repro_gen)

원본 픽셀 미사용. 크롭(photo1/photo2)을 비전으로만 판독 → nano-banana-2 t2i 1K → PIL 센터크롭/리사이즈로 슬롯 정확 크기.

## 슬롯별 프롬프트

### gen_photo1 (275×156, AR 16:9, raw 1376×768)
> Architectural photography of a modern minimalist house exterior at dusk, facade clad in dark walnut-brown vertical wood slats, a wide smooth off-white concrete horizontal band running across the upper facade receding in perspective to the right, large dark tinted floor-to-ceiling windows below, a bare slender tree with tiny pale blossoms in the left foreground, moody overcast evening light, muted palette of warm browns and cream, cinematic, photorealistic. Absolutely no text, letters, logos, or watermarks.

### gen_photo2 (275×155, AR 16:9, raw 1376×768)
> Interior photography of a serene minimalist modern office, pale warm-gray plaster walls, two tall narrow vertical backlit window panels glowing softly white on the left wall, delicate airy indoor trees with fine green foliage in low planters, long white minimal tables with slim olive-green chairs, smooth light gray floor, soft diffused daylight, japandi zen atmosphere, muted sage and greige palette, photorealistic. Absolutely no text, letters, logos, or watermarks.

## 평가 (1트라이 통과, 재생성 없음)

- **photo1**: 재현도 높음. 다크 우드 수직 슬랫 + 백색 수평 밴드 + 좌측 꽃나무 + 황혼 무드 전부 성립. 원본은 파사드 클로즈업(벽면이 프레임을 채움)인데 생성물은 건물 전체가 보이는 조금 더 물러난 앵글 — 구도 거리감만 차이. 팔레트·조명 무드는 근접.
- **photo2**: 재현도 높음. 좌측 세로 발광 창 2개, 연녹 잎의 가는 실내수, 백색 테이블 + 올리브 체어, 그레이지 팔레트 모두 재현. 원본보다 우측에 창/선반이 추가되어 약간 더 밝고 개방적. 원본의 스파 같은 어두운 차분함 대비 채도 약간 높음.

## 한계
- t2i는 원본과 동일 구도를 보장 못함 — 요소·팔레트·무드 단위 재현이며 픽셀 유사도는 목표가 아님.
- 슬롯이 16:9와 정확히 일치하지 않아(275:156≈1.763) 센터크롭에서 상하 수 px 손실.
