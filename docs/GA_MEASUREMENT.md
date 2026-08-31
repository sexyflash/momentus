# GA4 계측 — 전 제품 정본

> 2026-08-30~31 작업. **모든 제품의 GA 는 계정 하나(`Momentus Official` / `accounts/1843518`)** 아래 있다.
> 새 제품·새 도구를 붙이기 전에 이 문서를 먼저 읽어라.

---

## 1. 제품별 속성 지도

| 제품 | 도메인 | 측정 ID | 속성 |
|---|---|---|---|
| the-moment.us (본진) | the-moment.us | `G-1T66ZV28MB` | 551281263 |
| 헤이레시 | heyreci.com | `G-Q960PRWMPJ` | 552134198 |
| 마크 | mark.the-moment.us | `G-0MZD2HR8Y3` | 541668714 |
| 큐 | cue.the-moment.us | `G-QSHEQZ8V9C` | 544010203 |
| 컨텍스트 | kontext.the-moment.us | `G-77XK1Y1900` | 525400922 |
| 더플랜(notes) | notes.the-moment.us | `G-S9H8HFXBWJ` | 551977129 |
| 빈방 | bb.the-moment.us | `G-J2TEB2NG5Z` | 552088876 |
| 팀AI | teamai.the-moment.us | `G-KM7ZH2V3K8` | 552103172 |
| **무료 도구 (북마크릿)** | the-moment.us/tools/ | `G-T8Y89D206F` | 460766131 |
| ChatPage (확장) | — | `G-XHRMGX26LK` | 464251612 |

**원칙**: 자기 도메인이 있으면 자기 속성. 북마크릿처럼 자기 도메인이 없는 것은
`무료 도구` 속성 **하나**에 모은다 — 도구가 늘어도 속성은 안 는다.

더플랜·Flipper·무료도구 **소개 페이지**는 the-moment.us 하위 경로라 본진 속성이 그대로 잡는다.

---

## 2. 태그를 어디에 심나 (저장소별)

| 저장소 | 자리 | 배포 |
|---|---|---|
| `momentus` | `scripts/gen_site.py` 의 `ANALYTICS` + 드래그 추적기 | `npx wrangler deploy` (워커 `momentus`, 정적 자산) |
| `teamai` | `site/app/layout.tsx` | Pages `teamai-web` → 워커 `teamai-domain` 프록시 |
| `binbang` | `site/{index,status,archive/index}.html` | Pages `binbang-samples` |
| `notes` | `web/src/ga.js` → `shop_ui.js`·`posts.js` | `web/` 에서 `npx wrangler deploy` |
| `Reci` | `components/analytics/GoogleAnalytics.tsx` | Vercel (apex 별칭 수동) |

### 함정
- **apex(the-moment.us)는 Pages 가 아니라 Worker `momentus`** 다. 정적 자산 서빙 + `/naver*`·`/px.gif`.
  Pages 프로젝트 `the-moment`(=`the-moment.pages.dev`)는 **마크 사이트**다. 헷갈리지 마라.
- **`binbang` 라이브는 `site/`** 다. `public/` 은 옛 프로젝트 잔재고 CLAUDE.md 의 S3 안내는 낡았다.
- **`notes` 는 호스트 가드 필수** — `web/src/index.js` 가 notes 워커와 `pay.the-moment.us` 워커의
  공용 진입점이라, 가드가 없으면 결제층 방문이 더플랜 트래픽으로 섞인다. 어드민에는 아예 안 넣었다.

---

## 3. 무료 도구(북마크릿) 계측

### 3-1. 이벤트 이름에 도구를 박는다 ★

    quickpang_run          youtube_rank_run        pinterest_grab_run
    quickpang_install      youtube_rank_install    insta_rank_install

- 규칙: **`<도구이름>_run`** · **`<도구이름>_install`**. 새 도구는 등록 없이 자동으로 생긴다.
- ⚠️ 이벤트 이름은 영문·숫자·밑줄만 — **하이픈을 밑줄로** (`youtube-rank` → `youtube_rank`).
- `tool`·`method` 매개변수도 함께 보낸다(표준 보고서 교차 분석용, 맞춤 측정기준 등록돼 있음).

**왜 매개변수가 아니라 이름인가** — `tool_run` + 매개변수로 갈랐더니 실시간에서 도구가 안 보였다.
**GA4 실시간 API 는 이벤트 범위 맞춤 측정기준을 아예 안 받는다**
(`customEvent:tool` → `not a valid dimension`). 표준 보고서를 몇 시간 기다려야 갈려서 실무에 못 쓴다.
이름에 박으면 기본 "이벤트 이름별 이벤트 수" 화면에 즉시 뜬다.

### 3-2. 어디서 잡히나

| 자리 | 이벤트 | 4종 전부? |
|---|---|---|
| 랜딩 드래그 버튼 (우리 도메인) | `<도구>_install` (`method`: drag/click) | ✅ |
| 도구 실행 (남의 사이트) | `<도구>_run` (픽셀 → 워커 → MP) | ❌ **인스타 제외** |
| 귀환 갈고리 | UTM 유입 → apex | ✅ |

### 3-3. 인스타는 실행을 못 잰다 — 고장이 아니다

북마크릿은 **남의 페이지 안**에서 돌아 그 사이트 CSP 를 그대로 받는다. 2026-08-31 헤더 실측:

| 사이트 | gtag.js | fetch | 이미지 픽셀 |
|---|---|---|---|
| 인스타그램 | ❌ | ❌ | ❌ |
| 핀터레스트 | ❌ | ❌ | ✅ (`img-src *`) |
| 유튜브·쿠팡 | ✅ (CSP 헤더 없음) | ✅ | ✅ |

셋의 공통분모가 이미지뿐이라 픽셀로 간다. 인스타는 세 경로 다 막혀 **가져감만** 잡힌다.

### 3-4. 픽셀 경로

    도구 → https://the-moment.us/px.gif?t=<도구>&cid=<익명>&sid=<세션>
         → 워커 worker/naver.js → GA4 측정 프로토콜 → 무료 도구 속성

- **비밀키를 북마크릿에 넣지 마라.** 소스는 랜딩에 그대로 노출된다 — 키가 있으면 누구나
  가짜 이벤트를 넣을 수 있다. `GA_MP_SECRET` 은 워커 시크릿에만 있다.
- **보는 페이지 주소·제목·내용은 일절 안 보낸다** (`referrerPolicy='no-referrer'`).
  남의 사이트에서 도는 코드라 그걸 실으면 열람 기록 수집이 된다.
- 워커는 아는 도구 이름만 통과시키고, 무엇이 오든 200 으로 답한다 — 계측이 도구를 망가뜨리면 안 된다.

### 3-5. 북마크릿 `.txt` 를 고칠 때 금지 문자

- **`#`** — `javascript:` URL 에서 조각으로 잘린다. CSS 선택자 대신 `getElementById`.
- **`%`** — 파일이 퍼센트 인코딩돼 있어 디코드 때 깨진다.
- 한글은 `\uXXXX` 이스케이프. 고친 뒤 **디코드해서 문법 검사**: `urllib.parse.unquote` → `node --check`.

---

## 4. 확인하는 법

```bash
node ~/Projects/momentus/scripts/ga_tools_report.mjs --realtime   # 즉시 (29분 창)
node ~/Projects/momentus/scripts/ga_tools_report.mjs              # 최근 28일
```

GA 화면: **무료 도구 (북마크릿) → 보고서 → 참여도 → 이벤트**

### 측정 ID 가 실존하는지 판별 (★ 사고 방지)

```bash
curl -s "https://www.googletagmanager.com/gtag/js?id=<ID>" | wc -c
```

실존 속성은 ~506~517KB. **없는 ID 는 정확히 425,239 바이트** — 아무 ID나 넣어도 같은 값이다.

⚠️ **`/g/collect` 가 204 를 주는 것은 증거가 아니다.** GA 는 모르는 tid 에도 204 를 준다.
헤이레시가 이것 때문에 오랫동안 데이터 0 이었다(죽은 ID `G-GBBFS7ZDMX`).

⚠️ **헤드리스 크롬은 GA 봇 필터에 걸린다.** 실측은 실제 크롬으로.

### payload 가 맞는지 (MP)

```bash
curl -s -X POST "https://www.google-analytics.com/debug/mp/collect?measurement_id=<ID>&api_secret=<KEY>" \
  -d '{"client_id":"1.1","events":[{"name":"quickpang_run","params":{"tool":"quickpang"}}]}'
# validationMessages 가 [] 면 통과
```

---

## 5. 남은 일 / 안 한 것

- **표준 보고서 반영은 몇 시간 걸린다.** 실시간에서 확인하는 게 빠르다.
- 옛 `tool_run`·`tool_install` 이벤트는 2026-08-31 이전 데이터에만 있다. 새로 안 쌓인다.
- `Bomber Analytics`(247682761) 는 빈 계정이지만 **다른 회사 것으로 보여 남겼다.**
- 형 계정의 다른 GA 계정들(엔카·awards·Encar Dashboard·engaging·MixMax·Snap Shot·
  Chrome Web Store·2022 Town Hall)은 **남의 것**이다. 건드리지 마라.
- 서비스계정(`gindex@…`)은 **읽기 전용**이다. 속성·측정기준 생성은 GA 화면에서만 된다(API 403).

## 6. 지운 것 (2026-08-30~31, 휴지통 35일)

빈 계정 4개 — `MOMENTUS`(405789423) · `Mark`(398034148) · `Momentus`(29522033) · `AI포토그래퍼`(364298055).
전부 속성 0개짜리 껍데기였다. 속성은 하나도 지우지 않았다.
