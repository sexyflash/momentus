"""생성되는 셸 CSS 의 **조용히 죽는 선언**을 잡는다.

왜 필요한가 (2026-09-22 사고):
  `#mmt-bar .mmt-wm b{font:400 8px/1 inherit}` 가 6일간 **패밀리 8사이트 전부**에
  나가 있었다. CSS shorthand 에 CSS-wide 키워드(inherit/initial/unset/revert)를
  **부분값**으로 쓰면 선언 **전체가 무효**다 — 전체 값이 그 키워드일 때만 유효하다.
  브라우저는 에러를 내지 않고 조용히 버린다. 그래서 눈으로도, 기존 검사기(seo_check)
  로도 안 잡혔고, 로고 부제가 8px 대신 부모 16px·800 으로 렌더돼 로고가 뭉갰다.

  **조용히 실패하는 것은 기계가 잡아야 한다.** 사람이 "확인했다"로는 이 종류를 못 잡는다.
"""
import re

# 값이 여러 토큰으로 이뤄지는 단축 속성 — 여기에 CSS-wide 키워드가 섞이면 선언이 죽는다.
SHORTHANDS = {
    "font", "background", "border", "border-top", "border-right", "border-bottom",
    "border-left", "border-radius", "border-width", "border-style", "border-color",
    "margin", "padding", "flex", "flex-flow", "grid", "grid-area", "grid-template",
    "transition", "animation", "outline", "list-style", "overflow", "gap", "place-items",
    "place-content", "text-decoration", "columns", "inset",
}
CSS_WIDE = {"inherit", "initial", "unset", "revert", "revert-layer"}

_DECL = re.compile(r"(?:^|[;{])\s*([a-zA-Z-]+)\s*:\s*([^;{}]+)")


def find_invalid(css: str) -> list:
    """[(속성, 값, 이유)] — 비어 있으면 통과."""
    bad = []
    for m in _DECL.finditer(css):
        prop, val = m.group(1).lower(), m.group(2).strip()
        if prop not in SHORTHANDS:
            continue
        toks = [t for t in re.split(r"[\s/]+", val) if t]
        hit = [t for t in toks if t.lower() in CSS_WIDE]
        # 전체 값이 키워드 하나뿐이면 유효(font:inherit). 다른 토큰과 섞이면 무효.
        if hit and len(toks) > 1:
            bad.append((prop, val, f"단축 속성에 '{hit[0]}' 를 부분값으로 썼다 — 선언 전체가 무효다"))
    return bad


def assert_valid(css: str, where: str = "css") -> None:
    """무효 선언이 있으면 **막는다**. 조용히 나가는 것보다 생성이 실패하는 게 낫다."""
    bad = find_invalid(css)
    if not bad:
        return
    lines = "\n".join(f"    {p}: {v}\n      → {why}" for p, v, why in bad)
    raise SystemExit(
        f"\n🔴 [css_lint] {where} 에 브라우저가 **조용히 버릴** 선언이 {len(bad)}건 있다:\n"
        f"{lines}\n\n"
        "  단축 속성(font/background/border/…)에는 inherit·initial·unset 을 섞어 쓸 수 없다.\n"
        "  개별 속성으로 풀어라. 예: font:400 8px/1 inherit\n"
        "              → font-weight:400;font-size:8px;line-height:1  (family 는 어차피 상속된다)\n"
    )


if __name__ == "__main__":
    import sys
    for path in sys.argv[1:]:
        assert_valid(open(path, encoding="utf-8").read(), path)
        print(f"  ✓ {path}")
