# 관측소 (Observatory) — 전 사이트 **선행 지표** 상시 관측

> 2026-09-14 대표 지시로 신설. 정본은 이 문서다.
> 🚫 **유료 측정을 상시로 돌리지 않는다.** 여기 있는 지표는 전부 **0원**이다.

## 왜 있나

대표 지시(2026-09-14) 원문 요지:

> "후행 지표는 필요 없다. 우리가 한 번 인용됐다는 것 자체는 의미가 없다.
>  **얼마나 가져가고, 얼마나 끌어갈 준비가 된 상태로 발전하고 있느냐** —
>  그 숫자가 들어왔느냐, 변화했느냐의 **표**가 필요하다. 이건 돈 드는 게 아니지 않냐."

그리고 이건 cue 하나의 일이 아니다. 지금 우리가 돌리는 사이트가 10개다
(GA4 속성 기준: ChatPage · AI모의면접(cue) · 북마크릿 · Mark · 모멘터스 랜딩 · Kontext ·
팀AI · 헤이레시 · 빈방 · 노트플래너).

**원칙: 행동을 바꾸지 않는 숫자는 재지 않는다.**
인용률이 0.03에서 0.082가 돼도 우리가 할 일이 안 바뀌면 그건 계기가 아니라 요금이다.

## 이미 있는 것 — 🚫 새로 만들지 마라

| 자산 | 무엇을 주나 | 비용 |
|---|---|---|
| `cue/scripts/gsc.mjs` | Search Console 색인·노출·클릭·평균순위 (서비스계정 `.gindex-sa.json`) | 0 |
| `cue/scripts/ga.mjs` | GA4 **전 속성** 사용자·세션·**유입경로(`--source`)** — 같은 키 | 0 |
| `cue/scripts/botlog.mjs` | KV 크롤러 실방문(봇별·일별). ⚠️ `--remote` 필수 | 0 |
| `~/bin/seo_check.py` (= `momentus/scripts/seo_check.py`) | head 필수태그·sitemap·**고아 페이지** | 0 |
| `momentus/scripts/seo_weekly.sh` | 위를 묶어 **월 08:00 크론**으로 실행 → 로그만 남김 | 0 |
| `momentus/scripts/geo_probe.py` | AI 답변 인용 프로브(claude 구독 / chatgpt API) | 구독+소액 |
| `social-core/pipeline/notify.py` · `slack-bot/bot_messenger.py` | 슬랙 발송 **중앙 창구**(직접 발송 금지 룰) | 0 |

**즉 계기는 거의 다 있다. 없는 건 ① 한 표로 합치기 ② 전주 대비 변화 ③ 슬랙 알림 ④ 대상 사이트 전체 확대다.**

## 지표 — 이 여섯 줄이 전부다 (사이트 × 주차)

인과 사슬 순서대로 놓는다. **앞이 막히면 뒤는 볼 필요가 없다.**

| # | 지표 | 뜻 | 출처 | 상태 |
|---|---|---|---|---|
| 1 | **크롤** | 봇별 방문 수 (googlebot·yeti·bingbot·gptbot·claudebot·applebot) | `botlog.mjs` | 🟡 cue만 있음 → 타 사이트 확대 필요 |
| 2 | **색인 가능성** | sitemap 장수 · 내부링크 도달 · **고아 수** · FAIL | `seo_check.py` | ✅ 5도메인 → 10으로 확대 |
| 3 | **구글 노출** | GSC 노출·클릭·평균순위 | `gsc.mjs` | ✅ |
| 4 | **빙 노출** | 빙 색인 수·노출·질의어 + **AI Performance(인용수)** | **Bing Webmaster Tools API** | ✅ **2026-09-14 설치 완료** (아래 §설치기록) |
| 5 | **유입** | 사이트별 사용자·세션 | `ga.mjs` | ✅ |
| 6 | **AI 리퍼러** | `chatgpt.com` · `perplexity.ai` · `claude.ai` · `copilot.microsoft.com` · `gemini.google.com` 유입 | `ga.mjs --source` | ✅ 되는데 **아무도 안 본다** |

**모든 칸에 전주 대비 `±`를 붙인다.** 대표가 원하는 건 절대값이 아니라 **변화**다.

### 왜 빙(4번)이 중요한가
ChatGPT 웹검색·코파일럿이 타는 인덱스가 빙이다. **구글이 601장을 미색인으로 묶어둔 것과 달리
빙에는 이미 들어가 있다** (2026-09-14 DuckDuckGo `site:` 실측 — 홈·허브뿐 아니라
`/company/daangn/sales`·`/job/daangn-7667450003`·`/playbook/self-intro`·`/prep/ai-mock`까지 유형별로 나옴).
**빙에서 안 보이면 ChatGPT가 우리를 못 찾는다.** GSC로 구글을 보듯 빙을 봐야 한다. BWT는 무료다.

## 2026-09-14 기준선 (실측)

GA4 28일(08-16~09-13), `node cue/scripts/ga.mjs --source --days 28`:

```
제품-AI모의면접(cue)  186명  ← m.search.naver.com 107 · naver 66 · direct 57   AI 리퍼러 0
모멘터스 랜딩          89명  ← direct 76 · (not set) 26 · m.search.naver 6 · google 3
                              · chatgpt.com 1  ← 🟢 우리 네트워크 최초의 AI 유입
Mark                 139명  ← direct 105 · naver 38 · instagram 4
팀AI                  40명  ← direct 86 · accounts.google 78 · bing 1
빈방                  16명  ← direct 17 · bing 2
헤이레시               29명  ← direct 136 · accounts.google 75
```

`seo_weekly.log` 2026-09-14 08:00 회차:
```
the-moment.us   FAIL 0 · 고아   5/33
cue             FAIL 0 · 고아   0/131
notes           FAIL 0 · 고아   3/49
mark            FAIL 1 · 고아 853/860 (99%)   🔴
heyreci         FAIL 1 · 고아  73/112 (65%)   🔴
GSC cue: 노출 0 · 클릭 0
```

**읽는 법:** 사슬 1~2는 도는데 3(구글 노출)이 0이다. 6(AI 리퍼러)은 전 사이트 통틀어 1건.
mark는 sitemap 860장 중 853장이 고아라 **2번에서 이미 막혀 있다** — 3~6을 볼 필요가 없다.

## 만들 것

### 1. `momentus/observatory/collect.mjs` — 수집·합산
- 위 계기들을 호출해 **사이트 × 지표** 표를 만든다. 🚫 계기를 다시 구현하지 마라, 불러 써라
- 결과는 **append-only** 원장 `momentus/observatory/data/ledger.jsonl` (한 줄 = 한 회차 한 사이트)
- 전주 회차를 원장에서 읽어 `±` 를 계산한다. **빈 주는 `{missing:true}`** (cue 원장 규칙과 동일)

### 2. `momentus/observatory/bing.mjs` — 신규 계기
- Bing Webmaster Tools API (무료 · apikey). 색인 수 · 노출 · 클릭 · 상위 질의어
- 사이트 소유확인은 IndexNow 키가 이미 있어 쉽다(`cue/.indexnow_key`)
- ⚠️ **등록·키 발급은 사람 로그인이 필요하다.** 그 한 단계만 대표 또는 브라우저 자동화

### 3. 슬랙 알림 — 🚫 직접 쏘지 마라
- `social-core/pipeline/notify.py` 중앙 창구 경유 (`bot_messenger.send_as_persona`)
- **매주 표 1장**을 보낸다. 그리고 아래는 **즉시** 알린다:
  - 🟢 **첫 AI 리퍼러** / 첫 GSC 노출 / 첫 빙 노출 — 우리가 기다리는 신호다
  - 🔴 크롤 급감(전주 대비 −50%) · 고아율 급증 · FAIL 신규 발생 · GA 세션 0
- 🚫 변화 없는 주에 장문을 쏘지 마라. 조용하면 한 줄이면 된다

### 4. 대상 확대
- 도메인 목록을 5 → GA4 10속성에 맞춘다. 목록은 **한 파일**(`observatory/sites.json`)에 두고
  `seo_weekly.sh`도 그걸 읽게 고친다. 🚫 목록을 두 벌로 만들지 마라
- 크롤 로그(1번)는 지금 cue 워커에만 있다. 다른 사이트도 워커면 같은 블록을 이식,
  아니면 그 사이트는 1번 칸을 비운다(🚫 지어내지 마라)

### 5. 크론
- 기존 `0 8 * * 1 momentus/scripts/seo_weekly.sh` 를 **대체하지 말고 감싼다**
- ⚠️ cron 함정 3개: 절대경로 · `PATH`에 `~/.local/bin` 없음 · 헤드리스 `claude -p`는 파일을 못 쓴다

## 유료 프로브(`geo_probe.py`)는 어떻게 쓰나 — **상시 금지**

- 정기 실행 **안 한다.** 두 경우에만: ① 최초 기준선 1회 ② 페이지 형태를 바꾼 뒤 전/후 1회씩
- 위 6개 선행 지표가 전부 0으로 깔려 있으면 **돌릴 이유가 없다** — 사슬 앞이 막힌 걸 뒤에서 재봐야 답은 정해져 있다
- 돌릴 땐 `claude`(구독)를 기본 엔진으로. API 키는 제품이 실제로 쓰는 경로를 잴 때만

## 자[尺] — 이게 되면 완성이다

1. `node observatory/collect.mjs` 한 번으로 **10개 사이트 × 6지표 표**가 나온다
2. 그 표에 **전주 대비 ±**가 붙어 있다(2회차부터)
3. 원장에 append 됐고, 같은 주를 다시 돌려도 **행이 중복되지 않는다**
4. 슬랙에 표가 도착한다 — 중앙 창구를 거쳐서
5. 값을 인위적으로 나쁘게 바꾸면(테스트) **🔴 알림이 실제로 뜬다**. 뜨는 걸 눈으로 본 뒤 되돌린다
6. 사람이 아무것도 안 해도 **다음 주 월요일 08:00에 저절로 온다**

🚫 "돌려봤더니 잘 되더라"로 끝내지 마라. 5번(경보가 실제로 울리는지)을 안 보면 그 경보는 장식이다.

## 설치 기록 — Bing Webmaster Tools (2026-09-14)

**계정:** Google `sexyflash@gmail.com` 로 로그인 → **GSC 임포트**(사이트 검증 불필요, 사이트맵 자동 이관).
GSC 8개 사이트가 전부 `IsVerified: true` 로 들어왔다.

```
✅ cue.the-moment.us · the-moment.us · mark.the-moment.us · heyreci.com
✅ kontext.the-moment.us · teamai.the-moment.us · planner.the-moment.us · sexyflash.blogspot.com
🟡 notes.the-moment.us — API 로 추가했으나 IsVerified:false (GSC 개별 속성이 아니라 임포트 대상이 아니었다)
```

**🔑 API 키 위치: `~/.config/observatory/bing.json` (chmod 600).**
🚫 **저장소에 넣지 마라** — keyguard 가 커밋을 막고, 한 번 들어가면 이력에서 못 지운다.
재발급: bing.com/webmasters → ⚙ 설정 → API access → API Key.

**동작 확인된 엔드포인트** (전부 `?apikey=<KEY>`, base `https://ssl.bing.com/webmaster/api.svc/json/`)

| 엔드포인트 | 용도 | 검증 |
|---|---|---|
| `GetUserSites` | 등록 사이트·검증 상태 | ✅ 8건 반환 |
| `GetFeeds?siteUrl=` | 사이트맵 등록 현황 | ✅ |
| `SubmitFeed` (POST `{siteUrl,feedUrl}`) | 사이트맵 제출 | ✅ 5개 사이트 신규 제출 |
| `AddSite` (POST `{siteUrl}`) | 사이트 추가 | ✅ (검증은 별도) |
| `GetRankAndTrafficStats?siteUrl=` | 노출·클릭·색인수·크롤수 (일별) | ⏳ 0행 — 데이터 처리 48시간 |
| `GetQueryStats?siteUrl=` | 질의어별 노출·클릭·평균순위 | ⏳ 0건 — 동일 |

**사이트맵:** cue 는 이미 등록돼 있었고, `the-moment.us` · `mark` · `heyreci` · `kontext` · `teamai` 5개를 새로 제출해 각 1건 확인.
`planner` 는 `/sitemap.xml` 이 301 이라 건너뛰었다(사이트맵 경로 확인 필요).

### 🟢 덤으로 발견 — **AI Performance (BETA)** 가 이미 있다

BWT 좌측 메뉴에 `AI Performance`(BETA)가 있고 **Citation sources: Microsoft Copilots and Partners** 로
`Total Citations` · `Avg. Cited Pages` · **Grounding Queries**(어떤 질문에서 우리가 근거로 쓰였나) · `Pages` 를 준다.
**우리가 만들려던 GEO 성적표를 빙이 공짜로 주고 있다.**

- cue 3개월: **Total Citations 0 · Cited Pages 0**
- ⚠️ **아직 0으로 확정하지 마라** — 계정 생성 당일이고 BWT 자체가 "최대 48시간" 을 고지한다.
  `the-moment.us` 의 Grounding Queries 는 "momentary issue" 로 아예 안 떴다. **2026-09-16 이후 재확인.**
- UI 에 `Download` / `Download all` 이 있다. **API 엔드포인트는 미확인** — Agent-2 가 확인할 것

### ⚠️ BWT 가 띄운 경고 하나
> "Avoid IndexNow Batch Mode to prevent excessive server load and potential indexing delays."

cue 의 `scripts/indexnow.mjs` 가 배치로 밀고 있다. **당장 고치지는 않았다** — 색인 전략과 얽혀 있어
`SEO_HYPOTHESES.md` 에 가설로 올린 뒤 판단할 일이다.

---

## 지어진 것 — 2026-09-14 (slack-bot 세션)

돌리는 법·함정은 [`observatory/README.md`](../observatory/README.md). 여기엔 **판정이 필요했던 것**만 적는다.

| 자[尺] | 상태 | 근거 |
|---|---|---|
| 1. 10사이트 × 6지표 한 표 | ✅ | `node observatory/collect.mjs` 1회, 10행 |
| 2. 전주 대비 ± | ✅ 배선 완료 | 1회차라 화면엔 빈칸. **드릴에서 ± 판정이 실제로 도는 걸 확인**(아래 5번) |
| 3. 같은 주 재실행 시 중복 없음 | ✅ | 재실행 `0행 추가 · 1행 skip` / `--force` 만 1행 추가. 물리 12행 · 유일키 10 |
| 4. 슬랙 도착 | ✅ | 2026-09-14 12:02:58 #운영실 게시 — `conversations.history` 로 본문 확인 |
| 5. 🔴 가 실제로 운다 | ✅ | `node observatory/drill.mjs` rc=0 — 4종 발화 확인 후 원장 md5 동일 복원 |
| 6. 월 08:00 자동 | ✅ | `0 8 * * 1 … observatory/run.sh` 로 교체(줄 수 10 → 10, recheck 09:30 그대로) |

### 판단한 것들

**① 크론을 주인으로 뒀다(슬랙봇 스케줄러가 아니라).** 스펙이 "기존 크론을 감싸라"고 했고,
실제로 recurring self-heal(룰 #4)이 지키려던 "자가연쇄가 끊기는" 사망 모드가 cron 엔 없다.
대신 크론이 통째로 죽는 모드는 **표 스스로** 잡는다 — 지난주 행이 없으면 헤더가
`🔴 지난주 회차가 통째로 없다` 로 바뀐다. 조용히 '첫 회'로 넘어가지 않는다.

**② 슬랙은 `bot_messenger` 우선 · 폴백 직접발송.** `send_as_persona` 는 **봇 프로세스 안에서만**
동작한다(밖에서 부르면 예외 없이 drop). 크론은 그 밖이다. `naver_keepalive.slack_alert` 와
같은 모양(봇 안이면 단일 진입점, 밖이면 ops 토큰)으로 맞췄고, 폴백도 **같은 `slack_mrkdwn`
변환기**를 탄다 — 안 그러면 `**굵게**` 가 그대로 나간다.

**③ 목록을 정말 한 파일로 모았다.** `sites.json` 을 `seo_weekly.sh` 와 `scripts/seo_check.py`
(그리고 `~/bin` 사본)가 읽는다. 그 전엔 5개가 박혀 있어서 **teamai·kontext·빈방이 어느
점검에도 안 걸리고 있었다** — 이번에 처음 재보고 바로 FAIL 이 나왔다(아래).

**④ 계기를 새로 만들지 않고 두 개를 넓혔다.**
`gsc.mjs --host <호스트>`(sc-domain 속성 안에서 서브도메인만 분리) ·
`botlog.mjs --json --ns <KV>`(사람용 표를 정규식으로 긁지 않게). 둘 다 기존 동작은 그대로다.

**⑤ 임계는 실측으로 잡았다.** 크롤 −50%: cue 실측 주간 합계 3,230 → 3,459(+7%)라 정상
변동과 7배 떨어져 있다. 최소 200건 가드는 배포 직후의 작은 수에 오발동하지 않게.

### 처음 잰 값이 바로 일거리를 뱉었다 (2026-W38 기준선)

```
🟢 모멘터스 랜딩 — 첫 AI 리퍼러 1세션 (chatgpt.com)
🟢 모멘터스 랜딩 · Mark — 구글 첫 노출 4회
🔴 Mark    고아 854/861 (99%)  FAIL 1
🔴 헤이레시 고아  73/112 (65%)  FAIL 1
🔴 팀AI    고아  58/144 (40%)  FAIL 1   ← 이번에 처음 재봤다
🔴 Kontext FAIL 25건                    ← 이번에 처음 재봤다
🔴 빈방    FAIL 10건                    ← 이번에 처음 재봤다
```

**Mark·헤이레시·팀AI 는 사슬 2번에서 막혀 있다 — 3~6 을 볼 필요가 없다.** 고아부터다.

### 남은 것

- **빙 4번 칸** — 2026-09-16 이후 `node observatory/bing.mjs --site cue.the-moment.us` 로 재확인.
  지금은 `{"d":[]}` 라 **0 이 아니라 `unavailable`** 로 적고 있다(모름을 0 으로 바꾸지 않는다).
- **AI Performance API 는 없다(실측).** `GetAIPerformanceStats`·`GetCitationStats`·
  `GetGroundingQueries`·`GetCopilotStats` 등 **9종을 찔러 전부 404**. UI 경로
  `www.bing.com/webmasters/api/aiperformance` 는 쿠키 인증 SPA 껍데기(HTML)를 준다.
  → 길은 ① UI Download 버튼 ② 브라우저 자동화 둘뿐. `bing.mjs` 의 `aiPerformance()` 가
  그 사실을 값으로 돌려준다(엔드포인트가 열리면 그 함수만 고치면 된다).
- **① 크롤 칸** — cue 워커에만 봇 로그가 있다. 나머지는 정적 Pages 라 워커를 붙여야 채워진다.
  🚫 그 전까지 그 칸을 0 으로 채우지 마라.
- **③ 헤이레시** — GSC 속성에 서비스계정을 추가하면 바로 채워진다.

---

# 2026-09-14 (2차) — 자산 전수 확인 · 48시간 판정 장치

## 우리 사이트가 실제로 몇 개인가 — 전수 확인

GA4 속성 이름만 보면 10개인데, **그중 둘은 웹사이트가 아니다.** 실측으로 갈랐다.

| 자산 | 정체 | 호스트 | BWT | GSC | 판정 |
|---|---|---|---|---|---|
| 모멘터스 랜딩 | 사이트 | `the-moment.us` | ✅ | ✅ | 추적 |
| cue | 사이트 | `cue.the-moment.us` | ✅ | ✅ | 추적 |
| Mark | 사이트 | `mark.the-moment.us` | ✅ | ✅ | 추적 |
| 헤이레시 | 사이트 | `heyreci.com` | ✅ | ✅ | 추적 |
| Kontext | 사이트 | `kontext.the-moment.us` | ✅ | ✅ | 추적 |
| 팀AI | 사이트 | `teamai.the-moment.us` | ✅ | ✅ | 추적 |
| **노트** | 사이트 | `notes.the-moment.us` | 🟡 검증대기 | ✅ **9/14 추가·자동확인** | 추적 |
| **빈방** | 사이트 | `bb.the-moment.us` | 🟡 검증대기 | ✅ **9/14 추가·자동확인** | 추적 |
| 노트플래너 | **`notes` 로 개명됨** | `planner.the-moment.us` → 301 | ✅(잔존) | ✅ | 잔존 등록. 지우지 않음(리다이렉트 추적용) |
| 북마크릿 | 사이트 아님 — `the-moment.us/tools/` 하위 | — | 상위로 커버 | 상위로 커버 | 별도 등록 불필요 |
| **ChatPage** | **크롬 확장** (manifest v2.9.7) | 없음 | — | — | **검색 표면 없음. 제외** |
| **her** | **크롬 확장** | 없음 | — | — | **제외** |
| pay | 결제(거래) | `pay.the-moment.us` | — | — | **`robots: Disallow /` + noindex. 의도적 제외** |
| (구) sexyflash.blogspot.com | 외부 블로그 | — | ✅ | ✅ | 임포트로 딸려옴. 방치 |

🔴 **대표 지적이 맞았다 — 플래너는 노트로 개명됐다.** BWT 임포트가 옛 이름(planner)을 가져왔고
새 이름(notes)은 GSC 속성이 아니라 빠져 있었다. 9/14 에 GSC 에 URL 접두어 속성으로 추가했더니
**도메인 소유권으로 자동 확인**됐다. 빈방(`bb`)도 같은 방식으로 추가했다 — **이 둘은 아예 누락돼 있었다.**

### 남은 것 — BWT 검증 2건
`notes` · `bb` 는 BWT 에서 `IsVerified:false` 다. BWT 의 GSC 재동기화 버튼이 UI 에 없다.
다만 임포트 동의문에 **"주기적으로 검증 상태를 재확인한다"** 고 명시돼 있으니 며칠 내 자동 승격될 수 있다.
안 되면 셋 중 하나:
1. DNS TXT/CNAME — ⚠️ **wrangler 토큰은 `zone(read)` 뿐이라 DNS 쓰기가 안 된다.** 대시보드나 별도 토큰 필요
2. `BingSiteAuth.xml` 배포 — ⚠️ notes 저장소에 **미커밋 변경 2건**이 있어 배포하면 남의 작업이 같이 나간다
3. 그냥 기다린다 (사이트맵은 이미 제출됐고 크롤은 검증과 무관하게 돈다)

## 🔍 곁가지로 나온 결함 두 개 (이번에 안 고침 — 기록만)

- **`www.heyreci.com` 이 리다이렉트 없이 200 을 준다.** apex 와 중복 호스트 = 중복 콘텐츠.
  canonical 이 어디를 가리키는지 확인 필요
- **`bb.the-moment.us/sitemap.xml` 에 `<loc>` 이 1개뿐이다.** 빈방은 페이지가 그보다 많다
- **GSC 서비스계정(`gindex@…`)이 3개 속성만 본다** — `sc-domain:cue` · `sc-domain:the-moment.us` · `https://cue…`.
  mark·heyreci·kontext·teamai 는 **SA 권한이 없어 `gsc.mjs` 가 못 읽는다.**
  다만 `sc-domain:the-moment.us` 는 하위 도메인을 **합산**하므로 페이지 필터로 대체 가능.
  heyreci 는 별도 도메인이라 대체 불가 → 속성에 SA 를 사용자로 추가해야 한다

## IndexNow — **손댈 것 없다** (확인 결과)

BWT 가 "배치 모드를 피하라"고 경고했지만, 우리 실측은 **회당 4~27개**다(`[indexnow] pinged N urls`).
경고가 겨냥하는 대량 배치(최대 1만)와 무관하다. `momentus/scripts/indexnow_push.mjs` 도 크론에 없다
(2026-08-29 1,606장은 일회성이었다). 🚫 지금 고치지 마라 — 고칠 문제가 없다.

## 🎣 48시간 판정 장치 — **미리 걸어둔 미끼와 단서**

BWT 는 "최대 48시간" 을 고지한다. 그래서 오늘 숫자는 **전부 0**이다.
문제는 이틀 뒤 0을 봤을 때 **계정이 새것이라 0인지, 진짜 안 보여서 0인지 구분이 안 된다**는 것.
그 구분을 사람 기억이 아니라 **대조군**으로 한다.

### 대조군을 어디서 얻었나
GA4 28일 실측에 **빙에서 사람이 실제로 클릭해 들어온 사이트**가 있었다 —
`팀AI 1 · 빈방 2 · 북마크릿(the-moment.us/tools/) 1`. **cue 는 0.**
그리고 **AI 답변에서 클릭이 들어온 사이트**도 하나 — `the-moment.us ← chatgpt.com 1`. **cue 는 0.**
→ 대조군에 숫자가 뜨는데 cue 만 0이면 **계기는 멀쩡하고 cue 가 진짜 안 보이는 것**이다.

### 판정표 (2026-09-14 에 확정. 🚫 결과를 보고 고치지 마라)

| 대조군(teamai·the-moment.us) | cue | 판정 | 다음 행동 |
|---|---|---|---|
| 0 | 0 | 🟡 **계기 미확정** | 하루 더. 그래도 0이면 BWT **UI**를 눈으로 확인(API만의 문제일 수 있다) |
| >0 | 0 | 🔴 **cue 가 빙에서 안 보인다** | URL Inspection 으로 색인 여부 확인 → 색인은 됐는데 노출 0이면 **수요 문제**(걸릴 검색어가 없다) |
| — | >0 | 🟢 **보인다** | `GetQueryStats` 상위 질의어를 뽑아 콘텐츠 편성에 반영 |

AI Performance 는 API 미확인이라 **사람이 본다**:
`the-moment.us` 에 citation 이 뜨는데 cue 가 0 → cue 만 AI 에 안 잡히는 것.
**둘 다 0 → 이 계기가 Copilot 만 재고 ChatGPT 를 못 재는 것**일 수 있다. 그때만 `geo_probe.py` **1회**로 교차 확인.

### 걸어둔 장치

| 파일 | 하는 일 |
|---|---|
| `observatory/data/baseline-2026-09-14.json` | 설치 당일 스냅샷(전 사이트 노출·클릭·질의·사이트맵). 비교 기준 |
| `observatory/recheck.mjs` | 기준선과 비교해 표를 찍고 **위 판정표를 자동 적용**한다 |
| `observatory/recheck-cron.sh` | 매일 09:30. 🟡(대기)면 로그만, **🔴/🟢 판정이 나면 비서실 인박스에 알린다.** 같은 판정 반복 금지(`.verdict_sent`) |
| crontab | `30 9 * * * /bin/zsh …/observatory/recheck-cron.sh` |
| 로그 | `~/Projects/cue/crawler/data/observatory.log` |

**✅ 경보가 실제로 울리는지 눈으로 확인했다** — 판정기를 임시로 🔴 를 내도록 바꿔 돌렸더니
비서실 인박스에 항목이 실제로 추가됐다(11줄). 확인 후 **원복하고 시험 항목·스탬프를 지웠다.**
🚫 이 검증을 건너뛰지 마라 — 안 울리는 경보는 장식이다.


### 사이트 목록 — 확장앱·북마크릿을 왜 남겼나

추적 8개(the-moment.us·cue·mark·heyreci·kontext·teamai·notes·bb)는 그대로다. 다만
**북마크릿·ChatPage 는 `sites.json` 에서 지우지 않고 `domain: null`·`seo: false` 로 남겼다.**

- 지표 1~4(크롤·색인·구글·빙)는 **원천적으로 잴 수 없으니 `—`** 다 — Cue 세션이 말한 "제외"와 같은 결과.
- 지표 5(유입)는 **잴 수 있고 실제로 큰 값이 나온다**(북마크릿 63명/주, ChatPage 3,895명/28일).
  목록에서 통째로 빼면 그 유입이 표에서 사라진다 — 그건 제외가 아니라 **유실**이다.
- `planner` 는 뺐다(notes 로 개명·301). BWT 에만 남아 있다.

### 아직 안 고친 결함 (2차 세션이 올린 것 + 이번 실측)

- `www.heyreci.com` 이 리다이렉트 없이 200 — apex 와 중복 호스트
- `bb.the-moment.us/sitemap.xml` 의 `<loc>` 이 1개뿐 (이번 표의 `0/1` 이 그 결과다)
- **GSC 서비스계정이 3개 속성만 본다.** `*.the-moment.us` 는 `sc-domain:the-moment.us` +
  `--host` 페이지 필터로 전부 대체된다(이번 회차에 mark 3회·momentus 2회로 실측 확인).
  **heyreci.com 만 별도 도메인이라 대체 불가** — 그 속성에 서비스계정을 추가해야 3번 칸이 채워진다.

---

# 2026-09-14 (3차) — 블로커 정리. **셋 중 둘은 결함이 아니었다**

대표 지시: "추가해서 마무리해, 블로커 없이." 남아 있던 4건을 전부 닫았다.

## ✅ 1. heyreci GSC 서비스계정 추가 — 해결

`sc-domain:heyreci.com` 의 **사용자 및 권한**에 `gindex@sexyflash-mcp-2026.iam.gserviceaccount.com`
을 **전체** 권한으로 추가했다. 실측 확인:

```
서비스계정이 보는 속성 3 → 4개
  https://cue.the-moment.us/     | siteOwner
  sc-domain:the-moment.us        | siteFullUser
  sc-domain:cue.the-moment.us    | siteOwner
  sc-domain:heyreci.com          | siteFullUser   ← 신규
```

**3번 지표(구글 노출)의 마지막 블로커가 없어졌다.** `*.the-moment.us` 는 Agent-2 의 `gsc.mjs --host`
로 분리되고, 별도 도메인인 heyreci 는 이제 속성 자체를 읽는다.

## ❌ 2. `www.heyreci.com` 중복 호스트 — **결함이 아니다** (내가 틀렸다)

리다이렉트가 없는 건 맞지만 **canonical 이 양쪽 다 apex 를 가리킨다**:

```
www.heyreci.com  → <link rel="canonical" href="https://heyreci.com/index"/>
heyreci.com      → <link rel="canonical" href="https://heyreci.com/index"/>
```

중복 콘텐츠 신호는 canonical 로 이미 정리돼 있다. 🚫 고칠 것 없다. 백로그에서 뺀다.

## ❌ 3. `bb.the-moment.us/sitemap.xml` 이 1장 — **의도된 것이다** (내가 틀렸다)

사이트맵 본문에 이유가 적혀 있었다:

> `빈방 사이트맵. 손님에게 보여줄 페이지만 싣는다. /archive/*(내부 시안)·/status(손님별 코드 페이지)는 robots.txt 에서…`

**손님에게 보여줄 페이지가 실제로 하나**다. 🚫 고칠 것 없다.

⚠️ 다만 진짜 함정을 하나 봤다 — `bb.the-moment.us/BingSiteAuth.xml` 이 **200 을 준다.**
없는 경로에 SPA 랜딩 HTML 을 돌려주는 것이다(bb 의 robots.txt 주석에 적힌 그 사고와 같은 종류).
**존재 여부를 상태코드로 판정하면 안 된다** — 본문을 봐야 한다. 이번에도 200 만 보고
"BingSiteAuth 이미 있네" 로 넘어갈 뻔했다.

## ⏳ 4. BWT `notes`·`bb` 소유확인 — **감시로 전환** (사람 기억에서 뺐다)

BWT SPA 에 GSC 재동기화 버튼도, 대기 사이트의 검증 화면으로 가는 URL 도 없다
(`/webmasters/addsite`·`/siteverification` 둘 다 라우트 없음, 사이트 선택기의 "Not verified" 는 배지일 뿐).
남은 길은 DNS 쓰기(현 wrangler 토큰은 `zone:read` 뿐)나 파일 배포(두 저장소 모두 미커밋 변경 있음)인데,
**둘 다 남의 작업이나 계정 권한을 건드려야 한다.**

대신 GSC 쪽은 오늘 확인을 끝냈고 BWT 는 "주기적으로 GSC 검증 상태를 재확인한다"고 명시했다.
그래서 **기다리되, 기다리는 걸 사람이 기억하지 않게** `recheck.mjs` 에 감시를 넣었다:

| 상태 | 출력 | 인박스 |
|---|---|---|
| 승격됨 | `🟢 BWT 소유확인 — notes·bb 가 승격됐다(설치 +N일)` | **알림 감** |
| 7일 미만 대기 | `⏳ … 7일까지는 빙의 자동 재검증을 기다린다` | 조용 |
| **7일 경과** | `🔴 … N일째 미검증` + 남은 두 경로(DNS 권한 / 파일 배포) 명시 | **알림 감** |

🔴 **크론의 판정 선택 규칙도 같이 고쳤다.** 종전엔 `head -1` 이라 **첫 줄이 🟡(대기)면 그 뒤의
🟢 를 영영 못 봤다** — 빙 노출은 대기인데 소유확인만 먼저 승격되는 게 정확히 그 경우다.
지금은 **대기(🟡·⏳)가 아닌 첫 줄**을 판정으로 삼는다.
✅ 그 분기가 실제로 인박스까지 가는 걸 눈으로 확인하고(🟡 뒤의 🟢 를 집어 12줄 추가) 원복했다.
