# -*- coding: utf-8 -*-
"""공용 셸(1단 바 + 디자인 토큰)을 제품 저장소 '소스에 직접' 써넣는다.

왜 런타임(shell.js)이 아니라 소스에 박나 — 2026-07-27 전환:
  JS가 나중에 토큰을 덮어쓰면 첫 페인트는 제품 원래 값으로 그려진 뒤 바뀌어 '깜빡'이 보이고,
  바를 나중에 끼워 넣으면 페이지가 40px 밀린다(레이아웃 시프트).
  → 정본은 momentus 한 곳, 반영은 빌드 타임에 소스로. 런타임 보정 0.

실행: python3 scripts/sync_shell.py   (momentus 저장소 루트에서)
      제품 저장소는 각자 커밋·배포해야 반영된다.
"""
import os
import re
import sys

os.chdir(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, "scripts")

# gen_site.py 는 실행 시 사이트 전체를 생성하므로, 필요한 정의만 재사용하기 위해 exec 한다.
_src = open("scripts/gen_site.py", encoding="utf-8").read()
_ns = {"__name__": "gen_site_partial", "__file__": os.path.abspath("scripts/gen_site.py")}
exec(compile(_src, "scripts/gen_site.py", "exec"), _ns)
shell_css_block = _ns["shell_css_block"]
shell_bar_markup = _ns["shell_bar_markup"]

HOME = os.path.expanduser("~/Projects")

# (저장소, CSS 파일들, HTML 파일들, 그 제품의 도메인)
TARGETS = [
    ("notes", ["web/src/shop_ui.js"], ["web/src/shop_ui.js"], "notes.the-moment.us"),   # 구 planner-factory (2026-07-31 리네임)
    ("cue", ["public/landing.css", "public/jobs.css"],
     ["public/landing.html", "public/jobs.html", "public/privacy.html"], "cue.the-moment.us"),
    ("mark", ["src/styles/global.css"], ["src/layouts/Base.astro"], "mark.the-moment.us"),
]

CSS_RE = re.compile(r"/\* MMT:BEGIN.*?/\* MMT:END \*/", re.S)
HTML_RE = re.compile(r"<!-- MMT:BEGIN.*?<!-- MMT:END -->", re.S)


def put(path, block, pattern, anchor_re, anchor_fmt):
    """마커가 있으면 교체, 없으면 앵커 뒤에 삽입."""
    if not os.path.exists(path):
        print(f"  ⚠️ 없음: {path}")
        return False
    s = open(path, encoding="utf-8").read()
    if pattern.search(s):
        s2 = pattern.sub(lambda _: block, s, count=1)
    else:
        m = anchor_re.search(s)
        if not m:
            print(f"  ⚠️ 앵커 못 찾음: {path}")
            return False
        s2 = s[:m.end()] + anchor_fmt.format(block=block) + s[m.end():]
    if s2 != s:
        open(path, "w", encoding="utf-8").write(s2)
        print(f"  ✓ {path}")
        return True
    print(f"  = {path} (변경 없음)")
    return False


def main():
    css = shell_css_block()
    changed = 0
    for repo, css_files, html_files, host in TARGETS:
        print(f"[{repo}]")
        bar = shell_bar_markup(host)
        for rel in css_files:
            # .css 는 파일 맨 앞, HTML/JS 템플릿 안의 CSS 는 <style> 바로 뒤에 넣는다.
            #   (⚠️ shop_ui.js 는 JS 파일이라 맨 앞에 넣으면 파일이 깨진다 — 2026-07-27 실수 기록)
            anchor = re.compile(r"\A") if rel.endswith(".css") else re.compile(r"<style>")
            changed += put(os.path.join(HOME, repo, rel), css, CSS_RE, anchor, "\n{block}\n")
        for rel in html_files:
            changed += put(os.path.join(HOME, repo, rel), bar, HTML_RE,
                           re.compile(r"<body[^>]*>"), "\n{block}")
    print(f"\n반영 {changed}건 — 각 제품 저장소에서 커밋·배포하세요.")


if __name__ == "__main__":
    main()
