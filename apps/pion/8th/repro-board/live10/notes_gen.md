# ref10 재료 생성 노트 (repro_gen)

원본 픽셀 미사용. 크롭(photo1~3)을 비전으로만 판독 → nano-banana-2 t2i 1K → PIL 센터크롭/리사이즈로 슬롯 정확 크기.

## 슬롯별 프롬프트

### gen_photo1 (123×186, AR 2:3, raw 848×1264)
> Scandinavian interior photography, warm white minimalist room, a dark wood low console desk against the wall with one small framed botanical artwork hung above it, two light oak Windsor chairs with tall spindle backs standing on a smooth pale concrete floor, bright opening with sheer white daylight on the right side, soft natural light, calm beige and cream palette, photorealistic. Absolutely no text, letters, logos, or watermarks.

### gen_photo2 (64×96, AR 2:3, raw 848×1264)
> Narrow minimalist hallway interior, warm beige limestone travertine walls, a single Windsor spindle-back chair in smoked dark oak standing at the end of the corridor, smooth gray concrete floor, soft daylight falling from one side, quiet architectural mood, warm neutral palette, photorealistic. Absolutely no text, letters, logos, or watermarks.

### gen_photo3 (124×115, AR 1:1, raw 1024×1024)
> Studio photography of three light oak Windsor chairs with tall spindle backs arranged in a loose row against a plain light gray gallery wall, one wider armchair variant and two side chair variants, seamless pale floor, soft even diffused lighting, minimalist furniture catalogue aesthetic, photorealistic. Absolutely no text, letters, logos, or watermarks.

## 평가 (1트라이 통과, 재생성 없음)

- **photo1**: 재현도 높음. 다크 우드 콘솔 + 액자 + 라이트 오크 윈저 체어 2개 + 우측 채광 개구부 구도가 원본과 거의 동일한 배치. 3장 중 최고 매치.
- **photo2**: 재현도 높음. 트래버틴 복도 + 끝에 스모크드 오크 윈저 체어 1개 — 원본 구도 그대로. 64×96 축소에서도 실루엣 판독 양호.
- **photo3**: 재현도 높음. 라이트 오크 윈저 3개(암체어 1 + 사이드 2) 갤러리 컷 성립. 원본은 배경에 어두운 수평 오브젝트(벤치/작품)가 있었는데 생성물은 순수 무지 배경 — 소품 차이.

## 한계
- 원본 photo1의 체어는 벽 쪽으로 붙어 있으나 생성물은 방 중앙 쪽 — 미세 배치 차이.
- 윈저 체어의 스핀들 개수·등받이 곡률 같은 제품 디테일은 t2i 재량(동일 제품 재현은 불가, 동일 계열 재현까지).
