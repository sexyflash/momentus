# ref05 repro_gen — 재료 생성 노트 (M9)

원본 픽셀 미사용. photo.png는 Read(비전)로만 판독, t2i로 재생성.

## 슬롯: photo (570×332)

- 모델: fal nano-banana-2 (t2i), aspect_ratio 16:9, 1K → PIL 센터크롭(1.717:1) 후 570×332 리사이즈
- 트라이: 1회 (재생성 불필요)

### 프롬프트 전문
> Minimal e-commerce product photograph of a man's two feet wearing plain white ribbed crew socks, side view, both feet pointing to the left. The far foot rests flat on the floor; the near foot is slightly forward with the heel lifted, toes touching the ground. Bare lower legs with subtle natural leg hair visible above the ribbed sock cuffs, frame cropped at mid-shin. Seamless light cool gray-white studio background, glossy pale off-white floor with a very soft reflection and diffused soft shadows under the feet. Clean, airy, neutral cool-white palette, soft even studio lighting, commercial sock product photography. Absolutely no text, letters, logos, or watermarks.

### 평가 (구도/무드 재현도)
- 구도: 상. 두 발 좌향 측면, 흰 크루삭스+골지 커프, 정강이 중간 크롭, 다리털 디테일까지 재현. 원본은 앞발이 뒤꿈치 들림/뒷발 평면인데, 생성본은 앞발 평면·뒷발이 스텝 동작으로 걸린 형태 — 포즈 디테일만 상이.
- 무드: 상. 밝은 회백 심리스 배경 + 살짝 반사되는 바닥, 쿨톤 화이트 팔레트가 원본과 거의 동일. 페이지 배경(#fcfcfd)과의 연결도 자연스러움.

### 한계
- 발 앞뒤 배치·뒤꿈치 들림 포즈가 좌우 반전에 가깝게 나옴(전체 실루엣 인상은 유지).
- 원본 대비 배경 그라데이션이 약간 더 균일(원본은 우상단이 살짝 어두움).

## 렌더
- gen_trim.png 570×940, gen_layer.png(텍스트 투명+svg 숨김) 동일 크기.
- 트림: 알고리즘(우하단 bg diff>30)은 766을 반환 — tail 블록(#e8e9ee)이 흰 bg 대비 diff 23으로 임계(30) 미달이라 tail 앞에서 잘림. 레이아웃이 원본 repro와 동일하므로 원본 trim 경계 940으로 크롭.
