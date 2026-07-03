# ref07 repro_gen — 재료 생성 노트 (M9)

원본 픽셀 미사용. chair.png / badge.png는 Read(비전)로만 판독.
- chair → t2i 재생성 (사진 재료)
- badge → SVG 직접 드로잉 (그래픽 재료, t2i 금지)

## 슬롯 1: chair (2205×1046, top:2112)

- 모델: fal nano-banana-2 (t2i), aspect_ratio 21:9, 4K → PIL 센터크롭(2.108:1) 후 2205×1046 리사이즈
- 트라이: 2회 (1차 결과에 커튼·선반 등 주변 소품이 들어와 재생성)

### 프롬프트 전문 (1차)
> Wide cinematic furniture advertisement scene: a single mid-century modern round armchair centered in frame, three-quarter view angled toward the left. The chair has a curved molded shell of glossy dark walnut bentwood wrapping around the outside, plush light greige woven boucle fabric upholstery inside with a thick round seat cushion and curved padded arms, and four splayed tapered solid walnut legs. Setting: a warm taupe-brown studio backdrop wall softly lit by a warm spotlight glow directly behind the chair, a slightly darker muted brown floor, a clean horizontal seam line where wall meets floor, gentle soft shadow and faint reflection beneath the chair. Moody premium showroom lighting, warm brown monochrome palette, luxury furniture campaign photography. Absolutely no text, letters, logos, or watermarks.

1차 결과: 의자·조명은 좋았으나 좌측 커튼, 우측 가구/선반 등 배경 소품 유입 → 슬롯이 매우 와이드해 노출됨. 탈락.

### 프롬프트 전문 (2차, 채택 — gen_chair_raw2.png)
> Wide cinematic furniture advertisement scene: a single mid-century modern round armchair centered in an otherwise completely empty seamless studio set, three-quarter view angled toward the left. The chair has a curved molded shell of glossy dark walnut bentwood wrapping around the outside, plush light greige woven boucle fabric upholstery inside with a thick round seat cushion and curved padded arms, and four splayed tapered solid walnut legs. Setting: a flat, plain, seamless warm taupe-brown studio backdrop wall filling the entire frame edge to edge, softly lit by one warm spotlight glow directly behind the chair, a slightly darker muted brown seamless floor, and a single clean horizontal seam line where wall meets floor. Gentle soft shadow and faint reflection beneath the chair. The chair is the only object in the scene: no windows, no curtains, no plants, no shelves, no other furniture, no props, no wall panels. Moody premium showroom lighting, warm brown monochrome palette, luxury furniture campaign photography. Absolutely no text, letters, logos, or watermarks.

### 평가 (구도/무드 재현도)
- 구도: 상. 중앙 단독 의자, 좌향 3/4 뷰, 월넛 벤트우드 셸+그레이지 부클레 내장+스플레이드 다리, 벽-바닥 수평 심 모두 재현. 생성 의자는 원본보다 등받이가 높고 셸 노출이 적은 편(원본은 라운드 볼 형태가 더 강함).
- 무드: 최상. 웜 타우프 브라운 배경 + 의자 뒤 스포트라이트 글로우 + 어두운 바닥이 원본 무드와 거의 동일. 상단 타이포 존(#a3917d 계열)·하단 존(#8d7c6a)과의 색 연결 자연스러움.

### 한계
- 의자 프로포션(원본: 낮고 둥근 포드형 / 생성: 표준 라운지체어형) 차이.
- 생성 배경이 원본 크롭보다 약간 어둡고 붉은기가 있어, bg-top 그라데이션과의 경계에서 미세한 톤 점프 가능.

## 슬롯 2: badge (274×297) — SVG 직접 드로잉

repro_gen.html 내 인라인 SVG로 재작성 (원본 badge.png 미사용):
- 회전(-2deg) 라운드 사각 카드 + 옐로→오렌지 radial 그라데이션 + 안쪽 라이트 옐로 보더
- 우측·좌하단 오렌지 할프톤 도트 필드 (pattern)
- 좌상단 퍼플 우산: 스캘럽 캐노피 + 립 라인 + 연두 에지 도트 + 옐로 폴/훅
- "AISWARYA / —FURNITURE—" 다크퍼플 브랜드 라인
- FURNITURE / FESTIVAL / SALE: 이탤릭 볼드, 골드 그라데이션(SALE은 화이트) + 화이트 스트로크 + 다크레드 오프셋 섀도(유사 3D)
- 하단 레드 리본(접힌 귀 포함) "15th AUG - 30th SEP"

평가: 원본의 정보 구조·색 체계(퍼플/골드/레드)·레이아웃은 재현. 원본의 입체 압출 렌더링과 도트 블롭의 유기적 형태는 단순화됨.

## 렌더
- gen_trim.png 2205×3922, gen_layer.png(텍스트 투명+svg 숨김 → chair 재료만 남음) 동일 크기.
- 트림: 알고리즘(우하단 bg diff>30, 마지막 행+2) 결과 3922 — 원본 trim과 정확히 일치, 그대로 사용.
