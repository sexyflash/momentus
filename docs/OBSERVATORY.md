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
| 4. 슬랙 도착 | ⏳ 발송 승인 대기 | 본문은 `notify.py --dry` 로 확정. 발송은 대표 승인 후 |
| 5. 🔴 가 실제로 운다 | ✅ | `node observatory/drill.mjs` rc=0 — 4종 발화 확인 후 원장 md5 동일 복원 |
| 6. 월 08:00 자동 | ⏳ 크론 등록 승인 대기 | `run.sh` 완성. 크론 줄 교체만 남음 |

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
