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

ROOT = Path(__file__).resolve().parent.parent

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
""",
    re.X,
)

TAG = {
    "title": re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I),
    "desc": re.compile(r'<meta[^>]+name=["\']description["\'][^>]*>', re.I),
    # ⚠️ 여는 따옴표를 (["\']) 로 잡고 \1 역참조로 닫는다. `["\']` 로 닫으면
    #    값 안에 작은따옴표가 있을 때 거기서 끊겨 길이를 오측한다(2026-08-07 사고).
    "desc_val": re.compile(
        r'<meta[^>]+name=["\']description["\'][^>]+content=(["\'])(.*?)\1', re.S | re.I
    ),
    "canonical": re.compile(r'<link[^>]+rel=["\']canonical["\']', re.I),
    "og_image": re.compile(r'property=["\']og:image["\'][^>]+content=(["\'])(.*?)\1', re.I),
    "og_type": re.compile(r'property=["\']og:type["\']', re.I),
    "og_title": re.compile(r'property=["\']og:title["\']', re.I),
    "og_url": re.compile(r'property=["\']og:url["\']', re.I),
    "tw_card": re.compile(r'name=["\']twitter:card["\']', re.I),
    "jsonld": re.compile(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', re.S | re.I),
    "h1": re.compile(r"<h1[\s>]", re.I),
    "lang": re.compile(r'<html[^>]+lang=["\']([^"\']+)["\']', re.I),
    "charset": re.compile(r'<meta[^>]+charset', re.I),
    "viewport": re.compile(r'name=["\']viewport["\']', re.I),
    "noindex": re.compile(r'name=["\']robots["\'][^>]+content=["\'][^"\']*noindex', re.I),
}

STRIP_SCRIPT = re.compile(r"<(script|style)\b[^>]*>.*?</\1>", re.S | re.I)
STRIP_TAGS = re.compile(r"<[^>]+>")

# §5 통과 기준. 경로 패턴 → 최소 가시 텍스트(자)
MIN_TEXT = [
    (re.compile(r"/(products|p)/"), 1000),
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


def check_page(name: str, html: str) -> list[tuple[str, str]]:
    """(심각도, 메시지) 목록을 낸다. 심각도: FAIL=배포 막음, WARN=고칠 것."""
    out: list[tuple[str, str]] = []
    F = lambda m: out.append(("FAIL", m))
    W = lambda m: out.append(("WARN", m))

    # 의도적 noindex 페이지는 검사 대상이 아니다 (pay 등)
    if TAG["noindex"].search(html):
        return [("SKIP", "noindex 선언됨 — 의도적 색인 제외")]

    # 1. lang
    lang = TAG["lang"].search(html)
    if not lang:
        F("<html lang> 없음")
    elif not lang.group(1).lower().startswith("ko"):
        W(f'lang="{lang.group(1)}" — 한국어 페이지면 ko 여야 한다')

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
        d = TAG["desc_val"].search(html)
        n = len(d.group(2).strip()) if d else 0
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
        u = og_img.group(2).strip()
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

    # 8. charset / viewport
    if not TAG["charset"].search(html):
        F("meta charset 없음")
    if not TAG["viewport"].search(html):
        W("meta viewport 없음 — 모바일 우선 색인의 전제다")

    # 9. h1 — 정확히 1개
    n_h1 = len(TAG["h1"].findall(html))
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
    if re.search(r"fetch\([\"'][^\"']*\.json", body_js) or re.search(
        r"innerHTML\s*=\s*[^;]{0,80}await", body_js
    ):
        W("런타임 fetch→innerHTML 흔적 — 봇은 JS 를 안 돌린다. 서버 프리렌더가 필요하다")

    # §5. SPA 프리렌더가 껍데기만 있는 경우 (notes 사례: 장치는 있는데 본문 344자)
    app = re.search(r'<main\b[^>]*id="app"[^>]*>(.*?)</main>', html, re.S | re.I)
    if app and len(visible_text(app.group(1))) < 800:
        F(
            f"SPA 컨테이너 본문이 {len(visible_text(app.group(1)))}자 — "
            "프리렌더 장치만 있고 내용이 없다. seoBody() 를 늘려라"
        )

    return out


def get(url: str, timeout: int = 20) -> tuple[int, str]:
    req = urllib.request.Request(url, headers={"User-Agent": "momentus-seo-check/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
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
            if path == "/sitemap.xml":
                n = body.count("<loc>")
                extra = f"  ({n} URL)" + ("  🟠 lastmod 없음" if "<lastmod>" not in body else "")
            print(f"  ✅ {path}{extra}")
        elif required:
            print(f"  🔴 {path} → {code}")
            fails += 1
        else:
            print(f"  🟠 {path} → {code} (권장)")
    return fails


def check_sitemap_urls(base: str) -> int:
    code, body = get(base + "/sitemap.xml")
    if code != 200:
        return 0
    urls = re.findall(r"<loc>(.*?)</loc>", body)
    print(f"\n── sitemap URL 상태: {base} ({len(urls)}건)")
    bad = 0
    for u in urls:
        c, h = get(u)
        if c != 200:
            print(f"  🔴 {c} {u}")
            bad += 1
        elif len(visible_text(h)) < 400:
            print(f"  🟠 {c} {u} — 가시 텍스트 {len(visible_text(h))}자, 빈 페이지를 sitemap 에 두지 마라")
    if bad == 0:
        print("  ✅ 전 URL 200")
    return bad


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", action="store_true", help="라이브 도메인 검사")
    ap.add_argument("--domain", action="append", help="특정 도메인만 (반복 가능)")
    ap.add_argument("--sitemap", action="store_true", help="sitemap 의 전 URL 상태까지 검사")
    args = ap.parse_args()

    total_fail = total_warn = 0

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
