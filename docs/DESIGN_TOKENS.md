# 디자인 토큰 — 모멘터스 전 서비스 공통

> 정본 파일: [`assets/momentus.css`](../assets/momentus.css) · 배포 주소 `https://the-moment.us/assets/momentus.css`
> 이 문서는 **왜·어디까지**를 적는다. 값 자체는 위 파일이 유일한 소스다.

## 왜 만들었나

2026-08-07 사장님: *"할 때마다 페이지를 만들 때마다 수정할 때마다 틀어지지 않으려면 공통으로
쉐어하는 글로벌 css 같은 게 있어야 ... 어떻게 하면 좀 일관성 있게 할 것이냐"*

그날 실측한 "기본 버튼"의 상태:

| 저장소 | 반경 | 크기/굵기 | 패딩 |
|---|---|---|---|
| apex | 99px | 14 / 600 | 12·22 |
| mark | 999px | ~14 / 700 | 13·24 |
| notes | 999px | 15 / 700 | 17·44 |
| pay | **10px** | 15 / 700 | 13·22 |
| 문의 폼(그날 신규) | **10px** | 15 / 700 | 14·30 |

같은 회색선이 `#e6e8ec` / `#e9e9e9` / `#e9ecef` 로 셋이었다.
**단일 소스가 없어서 페이지를 만들 때마다 손으로 다시 정했다 — 드리프트는 사고가 아니라 구조의 결과였다.**

같은 날 `/inquiry/` 사고가 그 증거다: apex 에 이미 `.lg-head`(고정 헤더 56px 보정 포함)가 있는데
찾지 않고 새 컨테이너를 짜서 제목이 헤더에 달라붙었다.

## 무엇을 공유하나 (셋)

| # | 범위 | 토큰 |
|---|---|---|
| ① | **버튼** | `--mmt-r-ctrl` `--mmt-fs-ctrl` `--mmt-fw-ctrl` `--mmt-ctrl-pad(-lg/-sm)` `--mmt-ctrl-gap` |
| ② | **입력칸** | `--mmt-r-field` `--mmt-field-pad` `--mmt-fs-field` `--mmt-field-bw` |
| ③ | **문서형 페이지 제목** | `--mmt-fs-page-title` `--mmt-fw-page-title` `--mmt-ls-page-title` `--mmt-fs-section` |

그 밖에 값이 미세하게 갈리던 중립색 둘(`--mmt-line` `--mmt-muted`)만 포함한다.

### 🚫 공유하지 않는 것 — 의도적으로

- **레이아웃** (컨테이너 폭·그리드·섹션 여백) — 제품마다 다른 게 정상이다. 넣는 순간 이 파일이 모든 화면을 지배한다.
- **강조색(accent)** — 제품의 얼굴이다. cue 파랑, mark 주황은 그대로.
- **히어로 제목 크기** — notes 56px, mark 초대형 타이포는 개성이다.
  `--mmt-fs-page-title` 은 **읽는 페이지**(약관·환불·결제안내·문의)용이지 랜딩 히어로용이 아니다.
- **앱 UI 컨트롤** — cue 퀴즈 화면의 전체폭·56px 버튼은 페이지 CTA 와 다른 species 다. 손대지 않는다.

## 기준값을 어떻게 골랐나

**측정해서 골랐다. 다수결이 아니라 "이미 이 집 스타일인 것"을 찾았다.**
버튼 반경은 5개 중 3개(apex·mark·notes)가 이미 pill 이었고, 튀는 건 pay 와 그날 새로 만든 문의 폼이었다.
그래서 **pill(999px)이 기준**이고 그 둘을 맞췄다. 반대로 10px 로 통일했으면 멀쩡한 셋을 망가뜨렸다.

## 쓰는 법

각 사이트가 셸 `<head>` 에 한 줄:

```html
<link rel="stylesheet" href="https://the-moment.us/assets/momentus.css">
```

그리고 자기 셀렉터에서 토큰을 참조한다. **폴백값을 반드시 같이 적는다** — 파일이 못 실려도 안 무너진다.

```css
.btn{
  border-radius: var(--mmt-r-ctrl, 999px);
  padding:       var(--mmt-ctrl-pad, 14px 28px);
  font-size:     var(--mmt-fs-ctrl, 15px);
  font-weight:   var(--mmt-fw-ctrl, 700);
}
```

제품이 다른 값을 원하면 **자기 `:root` 에서 한 줄만 덮는다.** 그러면 그게 "의도한 예외"로 남는다.

```css
:root{ --mmt-r-ctrl: 10px; }   /* 이 제품은 사각 버튼 */
```

## 배선 현황 (2026-08-07)

| 사이트 | 링크 | 버튼 | 입력 | 문서 제목 |
|---|---|---|---|---|
| apex (the-moment.us) | ✅ | ✅ `.btn` | ✅ 문의 폼 | ✅ `.lg-head h1` |
| pay | ✅ | ✅ `.btn` | ✅ `input,textarea` | — (체크아웃 전용 크기 유지) |
| notes | ✅ | ✅ `.btn-dark` | — | — |
| cue | ✅ | ✅ `.buy-cta`(신설) | — | — |
| mark | ✅ | ✅ `.btn` | ✅ `.field input` | — |

미배선은 "빠뜨린 것"이 아니라 **아직 그 species 가 그 사이트에 없거나, 손대면 개성이 깨지는 자리**다.
새로 만들 때 토큰을 쓰면 자연히 채워진다.

## 별도 계약: `--mmt-cta-*` (상단 공통 바)

`--mmt-cta-r` `--mmt-fs-cta` `--mmt-cta-pad` 는 **상단 공통 바(`#mmt-bar`) 전용**으로 그 전부터 있던 것이다.
페이지 버튼(`--mmt-*-ctrl`)과 species 가 다르니 **섞지 마라.** 바 버튼은 작고 촘촘해야 한다.
