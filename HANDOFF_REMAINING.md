# 핸드오프 — 모멘터스 웹 남은 일 (2026-08-25)

> 인사이트 정비 5단계는 끝났다(보고서: shelf-mx7.pages.dev/d/insights-unify-20260825/).
> 이 문서는 **그 뒤에 남은 것 전부**다. 항목마다 *지금 상태 · 왜 남았나 · 하는 법 · 안 해도 되는 이유*를
> 적었다. 급한 순서가 아니라 **결정이 필요한 것 → 손만 대면 되는 것 → 안 해도 되는 것** 순이다.
>
> 큐 글 표지 30장은 분량이 커서 따로 뺐다 → `~/Projects/cue/HANDOFF_COVERS.md`

---

## A. 대표 결정이 먼저 필요한 것

### A-1. 헤이레시에 패밀리바를 달 것인가 ⛳ **결정 필요**

**지금**: `heyreci.com` 에 모멘터스 공용 바가 **없다**(실측 `id="mmt-bar"` 0개).
자체 도메인이라 다른 스포크(`*.the-moment.us`)와 처지가 다르다.

**왜 남았나**: 붙일지 말지가 기술이 아니라 **판단**이다.
- 붙이면 — 헤이레시 유입이 다른 제품으로 흐른다. 패밀리 인식이 생긴다.
- 안 붙이면 — 헤이레시가 독립 브랜드로 선다. 상품사진 서비스라 모멘터스와 결이 다를 수 있다.

**하는 법**(붙이기로 하면): `momentus/scripts/sync_shell.py` 의 `TARGETS` 에 heyreci 를 추가하고,
그 저장소 레이아웃에 `<!-- MMT:BEGIN -->` 마커를 넣으면 끝. 나머지는 자동이다.

### A-2. 컨텍스트에 패밀리바를 달 것인가 ⛳ **결정 필요**

**지금**: 없다. 영문 사이트(Features/Pricing/Docs)에 베타 딱지가 붙어 있다.

**왜 남았나**: 한글 바(제품 전체·인사이트·소개)를 영문 사이트 위에 얹으면 어색하다.
영문 바를 따로 만들면 그때부터 바가 두 벌이 된다 — 이 문서 전체가 경계하는 그 상태다.

**추천**: **지금은 달지 마라.** 컨텍스트가 정식 출시하고 한글을 지원할 때 같이 판단하는 게 맞다.

---

## B. 손만 대면 되는 것

### B-1. 컨텍스트 RSS 없음 — 본진이 손목록으로 버티는 중

**지금**: `kontext.the-moment.us` 에 `/rss.xml`·`/feed.xml` 전부 404(실측).
그래서 본진은 글 3편을 `momentus/data/products.json` 의 `posts` 배열에 **손으로 적어** 쓰고 있다.

**안전망은 이미 있다**: 빌드할 때마다 컨텍스트 목록 페이지를 세어 개수가 다르면 경고가 뜬다
(`gen_site.py` 의 `posts_index`). 조용히 낡지는 않는다.

**하는 법**: 컨텍스트에 `/rss.xml` 라우트를 추가(`src/data/blog/posts.json` 이 이미 있어 5분짜리다)
→ `products.json` 의 kontext 항목에서 `posts`·`posts_index` 를 지우고 `feed` 를 채운다.

**안 해도 되는 이유**: 글이 3편이라 손목록이 안 무겁다. **글이 5편을 넘으면 그때 해라.**

### B-2. 플리퍼 옛 `/apps/` 301 정리

**지금**: `/l/flipper*` 는 `/products/*` 로 **한 번에** 간다(302, 실측). 앱 재배포 필요 없음 — 끝난 일이다.
남은 건 `/apps/flipper*` → `/products/flipper*` 301 뿐인데, 이건 **옛 외부 링크·검색결과용**이다.

**하는 법**: `gen_site.py` 의 `/apps/<slug>/*` 301 블록을 지운다.

**안 해도 되는 이유**: 301 은 비용이 0이고, 지우면 옛 링크가 죽는다. **지울 이유가 생길 때까지 두는 게 맞다.**
(⚠️ 지운다면 `apps/<slug>/` 산출물이 남아 있지 않은지 확인해라 — 파일이 남으면 리다이렉트를 이긴다.)

### B-3. 중복 클래스 4건 — 뒤엣것이 이기고 있다

빌드가 매번 경고한다. **오늘 만든 게 아니라 예전부터 있던 것**이고, 오늘 2건은 오히려 줄었다.

| 클래스 | 위치(gen_site.py) |
|---|---|
| `.ap-qa` | 875 / 976 |
| `.fl-card` | 1793 / 1853 |
| `.gnb` | 87 / 102 |
| `.vc-thumb--g` | 521 / 846 |

**왜 위험한가**: 지금은 뒤엣것이 이겨서 화면이 멀쩡하다. 하지만 **앞엣것을 고치는 사람은
"왜 안 바뀌지"** 로 시간을 태운다. 이 가드를 만든 이유가 그거다.

**하는 법**: 각 쌍을 열어 **뒤엣것이 의도인지** 확인하고, 앞엣것을 지우거나 이름을 갈라라.
`.gnb` 는 102행이 `@media` 안일 수 있으니(의도된 재정의) 먼저 확인.

### B-4. 플리퍼 설정 스크린샷 2장 — 아래가 비어 보인다

`hisense-4-flipper-detail.png` 는 화면 아래쪽이 실제로 빈 설정 화면이고 맨 아래는 시스템 내비바다.
**자동으로 자를 수 없다**(단색 줄이 1줄뿐이라 검사에 안 걸린다).

**하는 법**: 기기에서 다시 찍거나, 손으로 아래를 잘라라.
**안 해도 되는 이유**: 잘린 게 아니라 원래 그런 화면이다. 내용 전달에는 문제 없다.

---

## C. 안 하기로 한 것 (재론 방지)

| 항목 | 판단 | 근거 |
|---|---|---|
| 무료 도구 카드의 서비스 로고 6종 | **그대로 둔다** | 대표: *"서비스 로고 쪽은 신경 쓰지 마"*(8/25) |
| 컨텍스트 배너 해상도(유튜브 1280×720 천장) | **그대로 둔다** | 대표: *"그냥 냅둬"*(8/25) |
| 큐 목록 카드를 본진 규격으로 | **안 맞춘다** | 큐 목록은 글 카드가 아니라 상황별(`준비 중`·`면접 후`) 필터가 붙은 다른 물건. 억지로 맞추면 쓰기 나빠진다 |
| 플래너 인사이트를 메뉴에 걸기 | **글 5편 전엔 안 건다** | 1편짜리 메뉴는 "관리 안 하는 사이트"라고 광고하는 것 |
| 큐 글 주소 `/playbook/` → `/insights/` | **안 옮긴다** | 31편이 이미 색인. 방문자에겐 차이 0인데 301 사슬만 는다 |

---

## D. 계속 지킬 규칙 (8/25 합의)

- **글 5편 미만이면 메뉴에 걸지 않는다.** 페이지는 남기되 링크는 숨긴다. 새 제품도 동일.
- **목록 주소만 맞추고 글 주소는 옮기지 않는다.**
- **각 저장소에서 카드 CSS 를 다시 쓰지 않는다.** 쓰는 순간 다시 두 벌이 된다.
  모양의 단일 소스는 `gen_site.py` 의 `NEWS_CSS` 하나이고, `sync_shell.py` 가 밀어 넣는다.
- **공용 셸에 백틱(`` ` ``)이나 `${` 를 넣지 마라.** 플래너·큐는 셸을 JS 템플릿 리터럴 안에 담아서
  한 글자에 배포가 죽는다. `sync_shell.py` 가 이제 결정론으로 막지만, 걸리면 셸이 **안 나간다**.
- **2주 뒤(≈9/8) GA 숫자를 보고** 인사이트에 더 투자할지 정한다. 지금 새 블로그는 만들지 않는다.
  속성: `the-moment.us` · 측정 ID `G-1T66ZV28MB` (마크·큐 것과 섞지 마라).

---

## E. 검증 명령 (뭘 하든 마지막에)

```bash
# 전 사이트 패밀리바·목록·넘침 한 번에
cd ~/Projects/momentus && ~/slack-bot/.venv/bin/python - <<'EOF'
from playwright.sync_api import sync_playwright
import time
T=[("본진","https://the-moment.us/insights/"),("마크","https://mark.the-moment.us/insights/"),
   ("큐","https://cue.the-moment.us/insights"),("플래너","https://notes.the-moment.us/insights/"),
   ("컨텍스트","https://kontext.the-moment.us/insights"),("빈방","https://bb.the-moment.us/")]
with sync_playwright() as pw:
    b=pw.chromium.launch(); p=b.new_context(viewport={'width':1440,'height':1000},
        extra_http_headers={'Cache-Control':'no-cache'}).new_page()
    for n,u in T:
        r=p.goto(u+('?z=%d'%time.time()), wait_until='networkidle'); p.wait_for_timeout(1200)
        d=p.evaluate("""()=>({bar:!!document.querySelector('#mmt-bar'),
          card:document.querySelectorAll('.nws-card').length,
          ovf:document.documentElement.scrollWidth-document.documentElement.clientWidth,
          broken:[...document.querySelectorAll('img')].filter(i=>i.complete&&!i.naturalWidth).length})""")
        print(f"{n:8} {r.status} bar={d['bar']} card={d['card']:>3} 넘침={d['ovf']} 깨짐={d['broken']}")
    b.close()
EOF
```

**⚠️ 확인은 반드시 `Cache-Control: no-cache` + 고유 쿼리로.** 클라우드플레어가 301 과 HTML 을
캐시해서, 고친 게 안 고쳐진 것처럼 보이는 사고가 이 작업에서만 세 번 났다.
