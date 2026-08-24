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
shell_legal_markup = _ns["shell_legal_markup"]

HOME = os.path.expanduser("~/Projects")

# (저장소, CSS 파일들, 바 HTML 파일들, 도메인, 법적표기 파일들)
#   법적표기 = 전자상거래 6종. 종전엔 제품 저장소가 손으로 베꼈다(notes 2곳·cue 4곳·mark 1곳).
#   틀리면 PG 심사에서 잡히는 문장이라 손복사로 두면 안 된다 — 2026-08-08 부터 여기서 밀어 넣는다.
#   ⬜ cue·mark 는 아직 마커가 없다. 각 저장소 푸터를 MMT:LEGAL 마커로 감싸면 목록에 넣는다.
TARGETS = [
    ("notes", ["web/src/shop_ui.js"], ["web/src/shop_ui.js"], "notes.the-moment.us",
     ["web/src/legal.js"], "<br>"),   # 구 planner-factory (2026-07-31 리네임)
    ("cue", ["public/landing.css", "public/jobs.css"],
     ["public/landing.html", "public/jobs.html", "public/privacy.html"], "cue.the-moment.us",
     ["public/landing.html", "public/jobs.html", "public/privacy.html", "src/index.js"], " · "),  # cue 푸터는 한 줄
    ("mark", ["src/styles/global.css"], ["src/layouts/Base.astro"], "mark.the-moment.us",
     ["src/components/Footer.astro"], "<br />"),
    # 빈방은 정적 HTML 2장 — 종전엔 바를 손으로 베껴 다른 제품과 어긋났다(2026-08-23).
    ("binbang", ["site/index.html", "site/status.html"],
     ["site/index.html", "site/status.html"], "bb.the-moment.us", [], "<br>"),
]

CSS_RE = re.compile(r"/\* MMT:BEGIN.*?/\* MMT:END \*/", re.S)
HTML_RE = re.compile(r"<!-- MMT:BEGIN.*?<!-- MMT:END -->", re.S)
# 법적 표기 — 제품 저장소가 손으로 베끼던 것을 여기서 갈아 끼운다(2026-08-08).
LEGAL_RE = re.compile(r"<!-- MMT:LEGAL:BEGIN.*?<!-- MMT:LEGAL:END -->", re.S)


#   ⚠️ .js 대상은 셸을 **템플릿 리터럴 안에** 담는다(notes/web/src/shop_ui.js, cue/src/index.js).
#     그래서 셸 안의 백틱 하나가 리터럴을 끊어 **빌드를 통째로 죽인다**.
#     2026-08-24 실사고: CSS 주석에 쓴 `calc(...)` 백틱 때문에 notes 배포가
#     "Expected ; but found calc" 로 실패했다. 원본만 고치면 다음에 또 들어온다.
#     순수 문자 검사라 자연어 판단이 아니다(룰 #1 무관). 걸리면 넣지 않고 멈춘다 —
#     깨진 셸을 밀어 넣는 것보다 안 넣는 게 낫다.
_JS_FORBIDDEN = ("`", "${")


def guard_js(path, block):
    """js 파일에 넣기 전, 템플릿 리터럴을 깨뜨릴 문자가 있는지 본다."""
    if not path.endswith(".js"):
        return True
    bad = [c for c in _JS_FORBIDDEN if c in block]
    if bad:
        print(f"  ⛔ {path}: 셸에 {bad} 가 있어 넣지 않는다 "
              f"(템플릿 리터럴이 깨진다). gen_site.py 의 셸 블록에서 지워라.")
        return False
    return True


def put(path, block, pattern, anchor_re, anchor_fmt, count=1):
    """마커가 있으면 교체, 없으면 앵커 뒤에 삽입."""
    if not os.path.exists(path):
        print(f"  ⚠️ 없음: {path}")
        return False
    if not guard_js(path, block):
        return False
    s = open(path, encoding="utf-8").read()
    if pattern.search(s):
        # ⚠️ count=1 이면 **한 파일에 마커가 여럿일 때 첫 개만 갈리고 나머지는 조용히 남는다.**
        #   cue/src/index.js 에 전자상거래 표기가 10곳 있었다(2026-08-08). 법적 표기는 전부여야 한다.
        s2 = pattern.sub(lambda _: block, s, count=count)
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
    for repo, css_files, html_files, host, legal_files, legal_sep in TARGETS:
        legal = shell_legal_markup(legal_sep)
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
        for rel in legal_files:
            # 마커가 반드시 있어야 한다 — 앵커를 못 찾으면 put 이 경고만 하고 지나간다.
            changed += put(os.path.join(HOME, repo, rel), legal, LEGAL_RE,
                           re.compile(r"\A"), "{block}", count=0)   # 0 = 그 파일의 **모든** 마커
    print(f"\n반영 {changed}건 — 각 제품 저장소에서 커밋·배포하세요.")


if __name__ == "__main__":
    main()
