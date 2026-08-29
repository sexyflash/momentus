#!/usr/bin/env python3
"""
SEO/GEO 점검기 — docs/SEO_GEO.md §3(필수 9종)·§5(초기 HTML)·§7(사이트 자산) 을 기계로 검사한다.

지침이 문서로만 있으면 안 지켜진다. 이 스크립트가 그 문서의 집행부다.
규칙을 바꿀 땐 docs/SEO_GEO.md 를 먼저 고치고 여기를 맞춰라 (문서가 정본).

사용법:
    python3 scripts/seo_check.py                  # 저장소 생성물(로컬 HTML) 검사
    python3 scripts/seo_check.py --live           # 라이브 전 도메인 검사
    python3 scripts/seo_check.py --live --domain heyreci.com
    python3 scripts/seo_check.py --live --sitemap # sitemap 의 전 URL 이 200 인지까지

종료코드: 0 = 통과, 1 = 🔴 실패 있음. CI·배포 전 게이트로 쓸 수 있다.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path

# 로컬 검사 대상 = **현재 작업 디렉토리**다. 스킬 문서가 "어느 저장소에서든 cd 해서
# 돌리면 된다"고 약속한 동작이 이거다.
# ⚠️ 예전엔 스크립트 위치 기준(`__file__/../..`)이었다. 그래서 ~/bin/seo_check.py 로 돌리면
#    ROOT 가 홈 디렉토리가 돼 8,294개 파일(.cache/chrome-mcp 까지)을 훑고 FAIL 26,342 를 뱉었다
#    (2026-08-28). 저장소 사본으로 돌릴 때만 우연히 맞던 것이다.
ROOT = Path.cwd()

# 라이브 검사 대상. docs/SEO_GEO.md §7 의 표와 같은 목록을 유지해라.
DOMAINS = [
    "https://the-moment.us",
    "https://notes.the-moment.us",
    "https://cue.the-moment.us",
    "https://mark.the-moment.us",
    "https://heyreci.com",
]

# 검사에서 뺄 로컬 파일. 생성물이 아니거나 의도적 예외인 것만 넣어라 — 늘리지 마라.
SKIP = re.compile(
    r"""
    ^naver\w+\.html$          # 네이버 소유확인 파일 (내용이 토큰 한 줄)
  | ^google\w+\.html$         # 구글 소유확인 파일(생기면)
  | ^content/                 # 이야기 소스. .assetsignore 로 배포 제외
  | ^docs/                    # 배포 제외
  | ^design-review/           # 배포 제외
  | ^404\.html$               # 404 페이지는 색인 대상이 아니다
  | ^_                        # `_` 로 시작하는 실험용 로컬 산출물 (배포 안 됨)
  | (^|/)node_modules/        # 의존성. 우리 산출물이 아니다
  | (^|/)dist/                # 빌드 중간물 (배포본은 라이브로 본다)
  | (^|/)carousel/            # cue — 인스타 카드 렌더용. 웹페이지가 아니다
  | (^|/)distill/             # cue — 증류 작업물
  | (^|/)bridge/              # cue — 브릿지 작업물
  | (^|/)logs?/               # 로그·리포트
  | ^public/naver\w+\.html$   # 네이버 소유확인 파일이 public/ 아래 있는 저장소(cue)
""",
    re.X,
)

# ⚠️ 속성값의 따옴표는 **선택**이다(HTML5). `<html lang=ko>` 도 유효하다.
#    2026-08-28: 따옴표를 필수로 본 정규식 때문에 notes 의 /insights 가
#    lang·description·canonical·viewport **전부 없음**으로 찍혔다 — 넷 다 실제로는 있었다.
#    오탐이 정본 백로그에 '고칠 것'으로 적혔다. 아래 Q(...) 로 세 형태를 모두 받는다.
def Q(name: str, val: str) -> str:
    """attr="값" / attr='값' / attr=값 세 형태를 받는 조각. 캡처 그룹 없음.

    ⚠️ 따옴표 안쪽도 **그 값이어야** 한다. `"[^"]*"` 로 두면 name="아무거나" 가
       전부 매치돼 모든 페이지가 통과해 버린다(2026-08-28 실측: FAIL 1 → 20,964 로 폭증).
    """
    v = re.escape(val)
    return rf'{name}=(?:"{v}"|\'{v}\'|{v}(?=[\s>/]))'


def QV(name: str) -> str:
    """값을 캡처하는 형태. group(1) 이 값이다."""
    return rf'{name}=(?:"([^"]*)"|\'([^\']*)\'|([^\s">]+))'


def attr_val(m) -> str:
    """QV 매치에서 실제 값을 꺼낸다(따옴표 종류에 따라 그룹이 다르다)."""
    if not m:
        return ""
    for g in m.groups():
        if g is not None:
            return g
    return ""


TAG = {
    "title": re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I),
    "desc": re.compile(rf'<meta[^>]+{Q("name", "description")}[^>]*>', re.I),
    # 값 안에 작은따옴표가 있어도 안 끊기게 여는 따옴표 종류별로 갈라 받는다(2026-08-07 사고).
    "desc_val": re.compile(
        rf'<meta[^>]+name=(?:"description"|\'description\'|description)[^>]+{QV("content")}',
        re.S | re.I,
    ),
    "canonical": re.compile(rf'<link[^>]+{Q("rel", "canonical")}', re.I),
    "og_image": re.compile(rf'{Q("property", "og:image")}[^>]+{QV("content")}', re.I),
    "og_type": re.compile(rf'{Q("property", "og:type")}', re.I),
    "og_title": re.compile(rf'{Q("property", "og:title")}', re.I),
    "og_url": re.compile(rf'{Q("property", "og:url")}', re.I),
    "tw_card": re.compile(rf'{Q("name", "twitter:card")}', re.I),
    "jsonld": re.compile(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', re.S | re.I),
    "h1": re.compile(r"<h1[\s>]", re.I),
    "lang": re.compile(rf'<html[^>]+{QV("lang")}', re.I),
    "charset": re.compile(r'<meta[^>]+charset', re.I),
    "viewport": re.compile(rf'{Q("name", "viewport")}', re.I),
    "noindex": re.compile(rf'{Q("name", "robots")}[^>]+content=[^>]*noindex', re.I),
}

# §20 — 전 도메인이 같은 블록을 갖는다. Allow: / 로 기술적으로는 통과하지만,
# 명시하지 않으면 다음에 누가 Disallow 를 넣을 때 막을 근거가 없다.
AI_BOTS = ["GPTBot", "OAI-SearchBot", "ClaudeBot", "PerplexityBot", "Google-Extended"]

STRIP_SCRIPT = re.compile(r"<(script|style)\b[^>]*>.*?</\1>", re.S | re.I)
STRIP_TAGS = re.compile(r"<[^>]+>")

# §5 통과 기준. 경로 패턴 → 최소 가시 텍스트(자)
MIN_TEXT = [
    (re.compile(r"/(products|p)/"), 1000),   # 제품 상세 — notes /p/<slug> 포함
    (re.compile(r"/stories/[^/]+/index\.html$|/stories/[^/]+$"), 1000),
    (re.compile(r"/legal/"), 1000),
    (re.compile(r"/tools/[^/]+/"), 1000),
]
MIN_TEXT_DEFAULT = 600


def visible_text(html: str) -> str:
    """봇이 보는 것과 같은 텍스트. 브라우저 DOM 이 아니라 초기 HTML 기준이다."""
    return " ".join(STRIP_TAGS.sub(" ", STRIP_SCRIPT.sub(" ", html)).split())


def min_text_for(name: str) -> int:
    for pat, n in MIN_TEXT:
        if pat.search(name):
            return n
    return MIN_TEXT_DEFAULT


def _iter_ld(blocks: list[str]):
    """JSON-LD 블록에서 dict 를 전부 훑는다 (@graph·배열·중첩 포함)."""
    def walk(o):
        if isinstance(o, dict):
            yield o
            for v in o.values():
                yield from walk(v)
        elif isinstance(o, list):
            for v in o:
                yield from walk(v)

    for b in blocks:
        try:
            yield from walk(json.loads(b))
        except json.JSONDecodeError:
            continue


ARTICLE_TYPES = {"Article", "BlogPosting", "NewsArticle", "TechArticle"}


def check_article(blocks: list[str]) -> list[tuple[str, str]]:
    """§15 필자 = 사람 · §16 신선도. 글 스키마가 있는 페이지에만 적용된다."""
    out: list[tuple[str, str]] = []
    for it in _iter_ld(blocks):
        t = it.get("@type")
        t = t if isinstance(t, str) else (t[0] if isinstance(t, list) and t else None)
        if t not in ARTICLE_TYPES:
            continue

        # §16 — 날짜가 없으면 '언제 쓴 글인지 아무도 모르는' 상태다
        if not it.get("datePublished"):
            out.append(("FAIL", f"{t}.datePublished 없음 — 신선도 신호가 0이다 (§16)"))
        if not it.get("dateModified"):
            out.append(("WARN", f"{t}.dateModified 없음 — 갱신을 해도 아무도 모른다 (§16)"))

        # §15 — author 는 Person 이어야 한다. Organization 이면 필자가 없는 것과 같다
        a = it.get("author")
        a0 = a[0] if isinstance(a, list) and a else a
        atype = a0.get("@type") if isinstance(a0, dict) else None
        if a0 is None:
            out.append(("FAIL", f"{t}.author 없음 — 구글 Who/How/Why 의 Who 가 비었다 (§15)"))
        elif atype != "Person":
            out.append((
                "WARN",
                f"{t}.author 가 {atype or type(a0).__name__} — Person 이어야 한다. "
                "우리 유일한 차별점(20년 채용 경력)이 스키마에 없는 상태다 (§15)",
            ))
        elif not a0.get("sameAs"):
            out.append(("WARN", f"{t}.author.sameAs 없음 — 밖의 언급을 한 엔티티로 못 묶는다 (§15-4)"))
        break  # 페이지당 글 스키마는 하나면 충분하다
    return out


def check_page(name: str, html: str) -> list[tuple[str, str]]:
    """(심각도, 메시지) 목록을 낸다. 심각도: FAIL=배포 막음, WARN=고칠 것."""
    out: list[tuple[str, str]] = []
    F = lambda m: out.append(("FAIL", m))
    W = lambda m: out.append(("WARN", m))

    # 의도적 noindex 페이지는 검사 대상이 아니다 (pay 등)
    if TAG["noindex"].search(html):
        return [("SKIP", "noindex 선언됨 — 의도적 색인 제외")]

    # 1. lang
    lang = attr_val(TAG["lang"].search(html))
    if not lang:
        F("<html lang> 없음")
    elif not lang.lower().startswith("ko"):
        W(f'lang="{lang}" — 한국어 페이지면 ko 여야 한다')

    # 2. title
    t = TAG["title"].search(html)
    if not t or not t.group(1).strip():
        F("<title> 없음/빈값")
    elif len(t.group(1).strip()) > 60:
        W(f"title {len(t.group(1).strip())}자 — 60자 넘으면 검색결과에서 잘린다")

    # 3. description
    if not TAG["desc"].search(html):
        F("meta description 없음")
    else:
        n = len(attr_val(TAG["desc_val"].search(html)).strip())
        if n == 0:
            F("meta description 이 빈값")
        elif n < 50:
            W(f"description {n}자 — 70~120자 권장")
        elif n > 160:
            W(f"description {n}자 — 160자 넘으면 잘린다")

    # 4. canonical
    if not TAG["canonical"].search(html):
        F("canonical 없음")

    # 5. Open Graph
    if not TAG["og_title"].search(html):
        F("og:title 없음")
    if not TAG["og_url"].search(html):
        W("og:url 없음")
    if not TAG["og_type"].search(html):
        W("og:type 없음")
    og_img = TAG["og_image"].search(html)
    if not og_img:
        F("og:image 없음 — 카톡·슬랙 공유 시 썸네일이 안 뜬다")
    else:
        u = attr_val(og_img).strip()
        if not u.startswith("http"):
            F(f"og:image 가 상대경로({u[:40]}) — 절대 URL 이어야 한다")
        if u.lower().endswith((".webp", ".svg")):
            F(f"og:image 가 {u.rsplit('.', 1)[-1]} — 카톡·네이버가 못 읽는다. PNG/JPG 로")

    # 6. Twitter Card
    if not TAG["tw_card"].search(html):
        F("twitter:card 없음")

    # 7. JSON-LD
    blocks = TAG["jsonld"].findall(html)
    if not blocks:
        F("JSON-LD 없음")
    else:
        types: list[str] = []
        for b in blocks:
            try:
                data = json.loads(b)
            except json.JSONDecodeError as e:
                F(f"JSON-LD 파싱 실패: {e}")
                continue
            items = data.get("@graph") if isinstance(data, dict) and "@graph" in data else data
            for it in items if isinstance(items, list) else [items]:
                if isinstance(it, dict) and it.get("@type"):
                    types.append(it["@type"])
                if isinstance(it, dict) and "aggregateRating" in it:
                    W("aggregateRating 있음 — 화면에 실제 리뷰가 없으면 리치결과 영구 박탈 사유다")
        if types and set(types) <= {"Organization"}:
            W("JSON-LD 가 Organization 뿐 — SEO_GEO.md §4 표를 보고 이 페이지 유형의 스키마를 추가해라")
        out += check_article(blocks)

    # 8. charset / viewport
    if not TAG["charset"].search(html):
        F("meta charset 없음")
    if not TAG["viewport"].search(html):
        W("meta viewport 없음 — 모바일 우선 색인의 전제다")

    # 9. h1 — 정확히 1개
    # ⚠️ <script> 안을 빼고 센다. 인라인 JS 가 마크업 문자열을 들고 있으면 그게 h1 으로 잡힌다
    #    (2026-08-28: notes 는 shop_ui 를 셸에 인라인해서 DOM h1 1개인 페이지가 **8개**로 찍혔다).
    #    visible_text() 는 원래 script 를 걷어내는데 이 검사만 원본 html 을 보고 있었다.
    n_h1 = len(TAG["h1"].findall(STRIP_SCRIPT.sub(" ", html)))
    if n_h1 == 0:
        F("<h1> 없음")
    elif n_h1 > 1:
        W(f"<h1> {n_h1}개 — 페이지당 정확히 1개여야 한다")

    # §5. 초기 HTML 가시 텍스트
    n_text = len(visible_text(html))
    need = min_text_for(name)
    if n_text < need:
        W(f"가시 텍스트 {n_text}자 (기준 {need}자) — thin content")

    # §5. 본문을 그리는 fetch 흔적.
    # 북마클릿 페이로드(href="javascript:…")의 fetch 는 렌더와 무관하므로 먼저 지운다
    # (2026-08-07: /tools/quickpang/ 가 이 오탐에 걸렸다).
    body_js = re.sub(r'href="javascript:.*?"', "", html, flags=re.S)
    # ⚠️ 결함 #9 (2026-08-29): fetch 흔적만 보고 경고하면 **정답 구조를 오답으로 찍는다.**
    #    권장 패턴은 "서버가 구워 넣고 → 클라이언트가 갱신"이다(cue 홈 bakeHome: 공고 851건·카드 12장).
    #    그 페이지엔 당연히 fetch 가 남아 있다. 문제는 fetch 가 있는 것이 아니라
    #    **fetch 말고는 본문이 없는 것**이다. 그래서 가시 텍스트가 기준 미달일 때만 경고한다.
    #    (cue 홈은 6,269자인데 이 경고를 계속 달고 있었다 — 자가 틀리면 고칠 게 없는데 고치려 든다.)
    if n_text < need and (
        re.search(r"fetch\([\"'][^\"']*\.json", body_js)
        or re.search(r"innerHTML\s*=\s*[^;]{0,80}await", body_js)
    ):
        W("런타임 fetch→innerHTML 흔적 + 본문 부족 — 봇은 JS 를 안 돌린다. 서버 프리렌더가 필요하다")

    # §5. SPA 프리렌더가 껍데기만 있는 경우 (notes 사례: 장치는 있는데 본문 344자)
    # ⚠️ 기준을 §5 표(min_text_for)와 **같은 숫자**로 맞춘다.
    #    2026-08-28 까지 여기만 800자로 따로 박혀 있어서, §5 허브 기준(600자)을 넘긴
    #    601자 페이지가 같은 도구 안에서 통과이면서 동시에 FAIL 이었다.
    #    한 도구가 두 기준을 들면 어느 쪽을 고쳐도 다른 쪽에 걸린다 — 규칙은 한 벌이어야 한다.
    #    이 검사의 목적은 "프리렌더 장치만 있고 내용이 없는 것"을 잡는 것이지
    #    §5 를 넘긴 페이지를 다시 떨어뜨리는 게 아니다.
    app = re.search(r'<main\b[^>]*id="app"[^>]*>(.*?)</main>', html, re.S | re.I)
    if app:
        n_app = len(visible_text(app.group(1)))
        if n_app < min_text_for(name):
            F(
                f"SPA 컨테이너 본문이 {n_app}자 (기준 {min_text_for(name)}자) — "
                "프리렌더 장치만 있고 내용이 없다. seoBody() 를 늘려라"
            )

    return out


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """리다이렉트를 따라가지 않는다. sitemap 검사용 — §18 참조."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: D102
        raise urllib.error.HTTPError(req.full_url, code, newurl, headers, fp)


def get(url: str, timeout: int = 20, follow: bool = True) -> tuple[int, str]:
    """(상태코드, 본문). follow=False 면 3xx 를 그대로 돌려주고 본문에 목적지를 담는다.

    ⚠️ 기본값(follow=True)은 301 을 따라가 200 으로 보고한다. 2026-08-28 에
    cue sitemap 의 `/blog`(→`/insights` 301)를 25일간 '정상'으로 보고한 원인이었다.
    """
    req = urllib.request.Request(url, headers={"User-Agent": "momentus-seo-check/1.0"})
    opener = None if follow else urllib.request.build_opener(_NoRedirect)
    try:
        ctx = opener.open(req, timeout=timeout) if opener else urllib.request.urlopen(req, timeout=timeout)
        with ctx as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        # follow=False 일 때 3xx 는 e.reason 에 목적지가 실려 온다
        return e.code, str(e.reason) if 300 <= e.code < 400 else ""
    except Exception as e:  # noqa: BLE001 — 네트워크 실패를 그대로 보여준다
        return 0, str(e)


def report(label: str, issues: list[tuple[str, str]]) -> tuple[int, int]:
    fails = [m for s, m in issues if s == "FAIL"]
    warns = [m for s, m in issues if s == "WARN"]
    skips = [m for s, m in issues if s == "SKIP"]
    if skips:
        print(f"  ⏭  {label} — {skips[0]}")
        return 0, 0
    if not fails and not warns:
        print(f"  ✅ {label}")
        return 0, 0
    icon = "🔴" if fails else "🟠"
    print(f"  {icon} {label}")
    for m in fails:
        print(f"       FAIL  {m}")
    for m in warns:
        print(f"       warn  {m}")
    return len(fails), len(warns)


def sitemap_locs(base: str) -> tuple[list[str], str]:
    """sitemap 의 전 URL. **sitemapindex 를 따라간다.**

    ⚠️ 2026-08-28: 이걸 안 따라가서 mark(Astro @astrojs/sitemap)의 URL 수를
       '1개'로 보고했다. 실제로는 색인 파일 1개 안에 수백 개가 들어 있었고,
       그 잘못된 숫자가 정본 §21 에 '검색에 낼 표면이 없다'로 적혔다.
       색인형 sitemap 은 흔하다 — 표준 동작으로 다뤄라.
    """
    for path in ("/sitemap.xml", "/sitemap-index.xml"):
        code, body = get(base + path)
        if code != 200:
            continue
        if "<sitemapindex" in body:
            child = re.findall(r"<loc>(.*?)</loc>", body)
            out: list[str] = []
            for c in child[:50]:  # 색인 안의 색인까지는 안 판다
                cc, cb = get(c)
                if cc == 200:
                    out += re.findall(r"<loc>(.*?)</loc>", cb)
            return out, f"{path} (색인 {len(child)}개)"
        return re.findall(r"<loc>(.*?)</loc>", body), path
    return [], ""


def check_site_assets(base: str) -> int:
    """§7 — robots.txt / sitemap.xml / llms.txt"""
    print(f"\n── 사이트 자산: {base}")
    fails = 0
    for path, required in (("/robots.txt", True), ("/sitemap.xml", True), ("/llms.txt", False)):
        code, body = get(base + path)
        if code == 200:
            extra = ""
            if path == "/robots.txt" and "Sitemap:" not in body:
                extra = "  🔴 Sitemap: 선언 없음"
                fails += 1
            if path == "/robots.txt" and re.search(r"Disallow:\s*/\s*$", body, re.M):
                extra += "  ⚠️ 전체 Disallow (의도한 것인지 확인)"
            if path == "/robots.txt":
                missing = [b for b in AI_BOTS if not re.search(rf"User-agent:\s*{re.escape(b)}", body, re.I)]
                if missing:
                    extra += f"  🟠 AI 봇 명시 없음: {', '.join(missing)} (§20)"
            if path == "/sitemap.xml":
                if "<sitemapindex" in body:
                    locs, how = sitemap_locs(base)
                    extra = f"  ({len(locs)} URL · {how})"
                else:
                    extra = f"  ({body.count('<loc>')} URL)" + ("  🟠 lastmod 없음" if "<lastmod>" not in body else "")
            print(f"  ✅ {path}{extra}")
        elif required:
            print(f"  🔴 {path} → {code}")
            fails += 1
        else:
            print(f"  🟠 {path} → {code} (권장)")
    return fails


def check_sitemap_urls(base: str) -> int:
    urls, _ = sitemap_locs(base)
    if not urls:
        return 0
    print(f"\n── sitemap URL 상태: {base} ({len(urls)}건)")
    bad = 0
    for u in urls:
        c, h = get(u, follow=False)
        if 300 <= c < 400:
            print(f"  🔴 {c} {u}  →  {h}")
            print("        sitemap 에 리다이렉트를 두지 마라 — 크롤 예산을 태우고 통합 신호를 지운다 (§18-2)")
            bad += 1
        elif c != 200:
            print(f"  🔴 {c} {u}")
            bad += 1
        elif len(visible_text(h)) < 400:
            print(f"  🟠 {c} {u} — 가시 텍스트 {len(visible_text(h))}자, 빈 페이지를 sitemap 에 두지 마라")
    if bad == 0:
        print("  ✅ 전 URL 200")
    return bad


# 공유 크롬(나브·푸터·헤더)은 고유도 계산에서 뺀다 — §17 이 그렇게 적혀 있는데
# 2026-08-28 첫 구현은 통째로 재고 있었다(점검기 결함 6번째). 크롬이 클수록 고유도가
# 실제보다 낮게 나와, 멀쩡한 묶음을 '발행 금지선 아래'로 오판한다.
# 🚫 템플릿 문구는 빼지 마라 — **그게 보일러플레이트다**(§17 계산법).
STRIP_CHROME = re.compile(
    r"<(header|footer|nav)\b[^>]*>.*?</\1>", re.S | re.I
)


def content_text(html: str) -> str:
    return visible_text(STRIP_CHROME.sub(" ", html))


def _shingles(text: str, n: int = 5) -> set:
    toks = re.findall(r"[가-힣A-Za-z0-9]+", text)
    return {tuple(toks[i : i + n]) for i in range(len(toks) - n + 1)}


def check_uniqueness(prefix: str, sample: int = 8) -> int:
    """§17 — 프로그래매틱 페이지 묶음의 고유도를 잰다.

    같은 템플릿에서 나온 페이지들이 서로 얼마나 다른지를 5-gram 으로 잰다.
    40% 미만이면 WARN, 30% 미만이면 발행 금지다.
    """
    base = re.match(r"(https?://[^/]+)", prefix)
    if not base:
        print(f"  🔴 --uniq 는 절대 URL 이어야 한다: {prefix}")
        return 1
    allu, _ = sitemap_locs(base.group(1))
    if not allu:
        print("  🔴 sitemap 을 못 읽었다")
        return 1
    urls = [u for u in allu if u.startswith(prefix)]
    if len(urls) < 2:
        print(f"  🔴 '{prefix}' 로 시작하는 URL 이 {len(urls)}개 — 잴 게 없다")
        return 1

    step = max(1, len(urls) // sample)
    picked = urls[::step][:sample]
    print(f"\n── §17 고유도: {prefix}  (전체 {len(urls)}장 중 {len(picked)}장 표본)")

    docs = {}
    for u in picked:
        c, h = get(u)
        if c != 200:
            continue
        docs[u] = _shingles(content_text(h))
    if len(docs) < 2:
        print("  🔴 표본을 못 받았다")
        return 1

    keys = list(docs)
    worst, worst_pair = 100.0, ("", "")
    scores = []
    for i, a in enumerate(keys):
        for b in keys[i + 1 :]:
            if not docs[a]:
                continue
            uniq = 100 - len(docs[a] & docs[b]) / len(docs[a]) * 100
            scores.append(uniq)
            if uniq < worst:
                worst, worst_pair = uniq, (a, b)
    avg = sum(scores) / len(scores)

    # 전 표본이 공유하는 보일러플레이트
    common = set.intersection(*docs.values())
    boiler = sum(len(common) / len(v) * 100 for v in docs.values() if v) / len(docs)

    print(f"  평균 고유도 {avg:.1f}%  ·  최저 {worst:.1f}%  ·  공통 보일러플레이트 {boiler:.1f}%")
    print(f"  최저 쌍: {worst_pair[0].rsplit('/', 1)[-1]} ↔ {worst_pair[1].rsplit('/', 1)[-1]}")
    if worst < 30:
        print("  🔴 30% 미만 — 발행 금지선이다. 레코드를 묶어 상위 페이지 하나로 합쳐라 (§17)")
        return 1
    if worst < 40:
        print("  🟠 40% 미만 — 경고선. 템플릿 문장을 줄이고 원본 데이터 인용을 늘려라 (§17)")
    else:
        print("  ✅ 40% 이상")
    if len(urls) > 500:
        print(f"  🟠 {len(urls)}장 — 500장 초과 묶음은 명시적 승인 대상이다 (§17)")
    elif len(urls) > 100:
        print(f"  🟠 {len(urls)}장 — 100장 초과. 표본 5~10% 사람 검수가 필요하다 (§17)")
    return 0


def check_sample_pages(base: str, n: int) -> tuple[int, int]:
    """sitemap 에서 경로 유형별로 표본을 뽑아 전수 검사한다.

    첫 페이지 1장만 보던 탓에 cue 의 글 39편이 한 번도 검사된 적이 없었다 (2026-08-28).
    """
    urls, _ = sitemap_locs(base)
    if not urls:
        return 0, 0
    buckets: dict[str, list[str]] = {}
    for u in urls:
        seg = u[len(base) :].strip("/").split("/")[0] or "(홈)"
        buckets.setdefault(seg, []).append(u)
    print(f"\n── 유형별 표본 검사: {base}  ({len(buckets)}종)")
    f = w = 0
    for seg, us in sorted(buckets.items()):
        for u in us[: max(1, n)]:
            c, h = get(u)
            if c != 200:
                print(f"  🔴 HTTP {c} {u}")
                f += 1
                continue
            a, b = report(f"[{seg}] {u[len(base):] or '/'}", check_page(u, h))
            f += a
            w += b
    return f, w


def check_orphans(base: str, hubs: list[str] | None = None) -> int:
    """§23 — sitemap 에 있는데 **내부 링크가 하나도 없는** 페이지를 센다.

    ⚠️ 이게 "Discovered - currently not indexed" 의 교과서적 원인이다.
       sitemap 은 **발견**만 시킨다. 크롤 우선순위는 **내부 링크**가 정한다.
       2026-08-28 cue 실측: sitemap /job/ 495장 중 **383장(77%)이 고아**였고,
       GSC 에서 609장이 "발견됨 - 크롤 안 됨"에 갇혀 있었다(색인 0개).
       `/jobs` 허브가 목록을 전부 JS 로 그려서 봇에게는 빈 페이지였던 게 원인이다.

    🚫 <script> 안의 href 를 세지 마라 — 봇은 그걸 링크로 안 본다. 그게 정확히 이 사고의 본질이다.
    """
    urls, _ = sitemap_locs(base)
    if not urls:
        print("\n── 고아 페이지: sitemap 을 못 읽었다")
        return 0
    # 허브 = 홈 + sitemap 의 얕은 경로(깊이 1~2). 여기서 링크가 안 나가면 고아다.
    if hubs is None:
        seen, hubs = set(), []
        for u in urls:
            p = u[len(base):].strip("/")
            if p.count("/") <= 1 and p not in seen:
                seen.add(p)
                hubs.append(u)
        hubs = hubs[:40]

    linked: set[str] = set()
    for h in hubs:
        code, html = get(h)
        if code != 200:
            continue
        body = STRIP_SCRIPT.sub(" ", html)
        for m in re.findall(r'href="(/[^"#?\s]*)"', body):
            linked.add(base + m.rstrip("/"))
            linked.add(base + m)

    orphans = [u for u in urls if u.rstrip("/") not in linked and u not in linked]
    print(f"\n── 고아 페이지: {base}  (허브 {len(hubs)}장에서 링크 수집)")
    print(f"  sitemap {len(urls)}장 · 내부 링크 도달 {len(urls) - len(orphans)}장 · 고아 {len(orphans)}장")
    if not orphans:
        print("  ✅ 고아 0")
        return 0
    pct = len(orphans) / len(urls) * 100
    bucket: dict[str, int] = {}
    for u in orphans:
        seg = u[len(base):].strip("/").split("/")[0] or "(홈)"
        bucket[seg] = bucket.get(seg, 0) + 1
    for seg, n in sorted(bucket.items(), key=lambda x: -x[1])[:8]:
        print(f"     /{seg}: {n}장")
    if pct >= 20:
        print(f"  🔴 {pct:.0f}% 가 고아 — sitemap 에만 있고 링크가 없으면 크롤 큐에 갇힌다 (§23)")
        return 1
    print(f"  🟠 {pct:.0f}% 가 고아")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", action="store_true", help="라이브 도메인 검사")
    ap.add_argument("--domain", action="append", help="특정 도메인만 (반복 가능)")
    ap.add_argument("--sitemap", action="store_true", help="sitemap 의 전 URL 상태까지 검사")
    ap.add_argument("--pages", type=int, metavar="N", help="§18 — sitemap 경로 유형마다 N장씩 전수 검사")
    ap.add_argument("--uniq", metavar="URL_PREFIX", help="§17 — 프로그래매틱 묶음의 고유도 측정")
    ap.add_argument("--orphans", action="store_true", help="§23 — sitemap 에 있는데 내부 링크가 없는 페이지")
    args = ap.parse_args()

    total_fail = total_warn = 0

    if args.uniq:
        return check_uniqueness(args.uniq)

    if args.live:
        bases = [
            b if b.startswith("http") else f"https://{b}"
            for b in (args.domain or DOMAINS)
        ]
        for base in bases:
            total_fail += check_site_assets(base)
            print(f"── 첫 페이지: {base}/")
            code, html = get(base + "/")
            if code != 200:
                print(f"  🔴 HTTP {code}")
                total_fail += 1
            else:
                f, w = report(base + "/", check_page(base, html))
                total_fail += f
                total_warn += w
            if args.orphans:
                total_fail += check_orphans(base)
            if args.pages:
                f, w = check_sample_pages(base, args.pages)
                total_fail += f
                total_warn += w
            if args.sitemap:
                total_fail += check_sitemap_urls(base)
    else:
        files = sorted(
            p for p in ROOT.rglob("*.html") if not SKIP.search(str(p.relative_to(ROOT)))
        )
        print(f"── 로컬 생성물 {len(files)}개 검사 (기준: docs/SEO_GEO.md)")
        for p in files:
            rel = str(p.relative_to(ROOT))
            f, w = report(rel, check_page(rel, p.read_text("utf-8", "replace")))
            total_fail += f
            total_warn += w

    print(f"\n{'─' * 60}")
    print(f"FAIL {total_fail}건 · warn {total_warn}건")
    if total_fail:
        print("🔴 배포 기준 미달. ~/Projects/momentus/docs/SEO_GEO.md §3 을 보고 고쳐라.")
    return 1 if total_fail else 0


if __name__ == "__main__":
    sys.exit(main())
