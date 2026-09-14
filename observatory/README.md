# 관측소 — 전 사이트 선행 지표 주간 표

정본 기획: [`docs/OBSERVATORY.md`](../docs/OBSERVATORY.md). 이 파일은 **돌리는 법**만 적는다.

## 한 줄

월요일 08:00 크론이 `run.sh` 하나를 돌린다 → 기존 주간 점검(그대로) + 사이트 10개 × 지표 6개를
재서 원장에 붙이고 → 전주 대비 ± 를 붙인 표 한 장을 #운영실에 올린다. **전부 0원짜리 계기다.**

## 파일

| 파일 | 하는 일 |
|---|---|
| `sites.json` | **대상 목록 단일 소스.** `collect.mjs`·`seo_weekly.sh`·`seo_check.py` 가 전부 이걸 읽는다 |
| `collect.mjs` | 기존 계기들을 **불러** 표를 만들고 원장에 붙이고 경보를 판정한다 |
| `bing.mjs` | 빙(BWT) 계기. 키는 `~/.config/observatory/bing.json` |
| `notify.py` | 원장을 읽어 표를 슬랙으로 |
| `drill.mjs` | **경보가 실제로 우는지** 확인하고 되돌린다 |
| `run.sh` | 크론 진입점 하나 |
| `data/ledger.jsonl` | append-only 원장. 한 줄 = 한 회차 한 사이트 |

## 자주 쓰는 것

```bash
cd ~/Projects/momentus
node observatory/collect.mjs                 # 수집 → 원장 → 표      (10사이트 ≈ 12분)
node observatory/collect.mjs --site cue      # 한 사이트만
node observatory/collect.mjs --no-collect    # 측정 없이 원장만 읽어 표
node observatory/collect.mjs --force         # 같은 주 재측정(덮어쓰는 행을 붙인다)
python3 observatory/notify.py --dry          # 슬랙에 **나갈 모양 그대로** 출력
node observatory/drill.mjs                   # 경보 드릴(끝나면 원장 원상복구, 실패면 rc=1)
node observatory/bing.mjs                    # 빙 등록 현황·키 상태
```

## 원장 규칙

- **append-only.** 과거 행을 고치지 마라. 틀렸으면 `--force` 로 새 행을 붙여라.
- 읽을 땐 `(주차, 사이트)` 로 묶어 **마지막 행이 이긴다**.
- 같은 주를 그냥 다시 돌리면 **행이 안 늘어난다**(skip). 늘리려면 `--force` 를 명시해야 한다.

## 지금 비어 있는 칸과 그 이유 (2026-09-14)

| 칸 | 누가 비었나 | 왜 · 뭘 하면 채워지나 |
|---|---|---|
| ① 크롤 | cue 빼고 전부 | 봇 방문 로그는 **워커가 있어야** 남는다. cue 워커에만 그 블록이 있다. 나머지는 정적 Pages 라 워커를 새로 붙여야 한다 |
| ③ 구글 | 헤이레시 | GSC 속성이 없다. 서비스계정 `gindex@sexyflash-mcp-2026.iam.gserviceaccount.com` 을 속성에 추가하면 바로 채워진다 |
| ④ 빙 | 전부 | 2026-09-14 등록 직후라 BWT 가 아직 데이터를 안 준다(고지: 최대 48시간). **2026-09-16 이후 재확인** |
| ①~④ | 북마크릿 · ChatPage | 자기 웹 호스트가 없는 제품이다. 원천적으로 못 잰다 |

🚫 빈 칸을 0 으로 채우지 마라. `—` 는 "못 잰다", `?` 는 "이번 회차에 실패", 숫자는 "실측"이다.

## 알아둘 함정

- **GSC 숫자 두 가지.** 사이트별 숫자는 `--host` 페이지 필터로 뽑는다. 필터를 걸면 GSC 가
  **페이지 단위**로 세고, 필터 없는 전체 합계는 **질의 단위**로 센다 — 그래서 사이트별 합이
  전체보다 클 수 있다(2026-09-14 실측: 전체 5 vs momentus 4 + mark 4). 버그가 아니다.
  주 대비 추세를 보는 게 목적이므로 **한 가지 방식을 계속 쓰는 것**이 중요하다.
- **크론엔 PATH 가 없다.** 새 실행 파일을 부르면 절대경로로 써라.
- **`~/bin/seo_check.py` 는 저장소 사본이다.** `scripts/seo_check.py` 를 고쳤으면 `cp` 로 맞춰라
  (둘 다 `sites.json` 을 읽으니 목록은 안 갈라진다).
- **AI Performance(BETA)는 공개 API 가 없다.** BWT UI 에만 있다 — `bing.mjs` 머리말 참조.
