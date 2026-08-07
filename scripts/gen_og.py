#!/usr/bin/env python3
"""
OG 이미지 생성기 — `/og/*.png` (1200×630) 을 매니페스트에서 자동으로 굽는다.

정본 지침: docs/SEO_GEO.md §3.
왜 생성물인가: 제품이 늘 때마다 손으로 이미지를 만들면 반드시 빠뜨린다.
`data/products.json` 에 한 줄 추가하면 OG 이미지도 같이 생긴다 — PRODUCT_SYSTEM.md §9 의 지그 원칙.

**빌드를 절대 깨뜨리지 않는다.** Pillow 나 폰트가 없으면 경고만 내고 건너뛴다.
그 경우 gen_site.py 후처리가 기존 이미지를 그대로 두거나 기본값으로 넘어간다.

사용법:
    python3 scripts/gen_og.py           # 없는 것만 생성
    python3 scripts/gen_og.py --force   # 전부 다시 생성 (디자인 바꿨을 때)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "og"

W, H = 1200, 630
INK, PAPER, GRAY = "#0b0c0e", "#ffffff", "#5b6270"
BLUE = "#3182f6"

# 폰트 후보 — 앞에서부터 있는 것을 쓴다. Pretendard 가 브랜드 정본이고,
# 없으면 맥 시스템 한글 폰트로 떨어진다(빌드가 죽는 것보다 낫다).
FONT_BOLD = [
    Path.home() / "Projects/notes/fonts/PretendardJP-Bold.ttf",
    Path("/System/Library/Fonts/AppleSDGothicNeo.ttc"),
    Path("/System/Library/Fonts/Supplemental/AppleGothic.ttf"),
]
FONT_REG = [
    Path.home() / "Projects/notes/fonts/PretendardJP-Regular.ttf",
    Path("/System/Library/Fonts/AppleSDGothicNeo.ttc"),
    Path("/System/Library/Fonts/Supplemental/AppleGothic.ttf"),
]


# products.json 의 color 는 CSS 변수일 수 있다(브랜드 색을 KB_CSS 토큰에 모아 두기 때문).
# Pillow 는 var() 를 모르므로 여기서 푼다. 값의 정본은 gen_site.py 의 KB_CSS `:root` 다 —
# 거기서 색을 바꾸면 이 표도 같이 고쳐라.
CSS_VARS = {
    "--coup": "#346aff",
    "--ig": "#e1306c",
    "--yt": "#ff0033",
    "--pin": "#e60023",
    "--ok": "#12b76a",
}


def _color(v: str | None) -> str:
    """'var(--ig)' · '#e1306c' · None 을 전부 유효한 hex 로 만든다."""
    if not v:
        return BLUE
    v = v.strip()
    if v.startswith("var("):
        return CSS_VARS.get(v[4:-1].strip(), BLUE)
    return v if v.startswith("#") else BLUE


def _font(cands, size):
    from PIL import ImageFont

    for p in cands:
        if p.exists():
            try:
                return ImageFont.truetype(str(p), size)
            except Exception:  # noqa: BLE001 — .ttc 인덱스 문제 등은 다음 후보로
                continue
    return ImageFont.load_default()


def _wrap(draw, text, font, max_w):
    """한글은 공백이 적어 단어 단위 줄바꿈이 안 먹는다. 글자 단위로 자른다."""
    lines, cur = [], ""
    for ch in text:
        if ch == "\n":
            lines.append(cur)
            cur = ""
            continue
        t = cur + ch
        if draw.textlength(t, font=font) > max_w and cur:
            lines.append(cur)
            cur = ch
        else:
            cur = t
    if cur:
        lines.append(cur)
    return lines


def render(path: Path, title: str, sub: str = "", accent: str = BLUE, kicker: str = "MOMENTUS"):
    from PIL import Image, ImageDraw

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # 왼쪽 세로 액센트 바 — 제품 색으로 구분되고, 브랜드 톤(미니멀)을 깨지 않는다
    d.rectangle([0, 0, 14, H], fill=accent)

    pad = 96
    f_kick = _font(FONT_REG, 30)
    f_title = _font(FONT_BOLD, 82)
    f_sub = _font(FONT_REG, 36)

    t_lines = _wrap(d, title, f_title, W - pad * 2)[:3]
    s_lines = _wrap(d, sub, f_sub, W - pad * 2)[:2] if sub else []

    # 블록 전체를 수직 중앙에 둔다 — 줄 수가 1~3줄로 달라져도 균형이 유지된다.
    block = 52 + len(t_lines) * 100 + (12 + len(s_lines) * 50 if s_lines else 0)
    y = (H - block) // 2

    d.text((pad, y), kicker, font=f_kick, fill=accent)
    y += 52
    for ln in t_lines:
        d.text((pad, y), ln, font=f_title, fill=INK)
        y += 100

    if s_lines:
        y += 12
        for ln in s_lines:
            d.text((pad, y), ln, font=f_sub, fill=GRAY)
            y += 50

    d.text((pad, H - 92), "the-moment.us", font=_font(FONT_REG, 30), fill=GRAY)

    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, "PNG", optimize=True)
    return path


def targets():
    """(출력경로, 제목, 부제, 액센트) 목록. 매니페스트에서 뽑으므로 제품이 늘면 자동으로 늘어난다."""
    d = json.loads((ROOT / "data" / "products.json").read_text(encoding="utf-8"))
    P = d["products"]
    out = [("default", "쓸모 있는 것만 만듭니다", "강형모 1인 AI 스튜디오", BLUE)]

    for slug in d["order"]:
        p = P.get(slug) or {}
        name = (p.get("name") or slug).split(" · ")[0]
        out.append((slug, name, p.get("desire") or p.get("tagline") or "", _color(p.get("color"))))

    # 고정 페이지 — 새 유형을 추가하면 여기 한 줄
    out += [
        ("about", "모멘터스 소개", "무엇을 만들고, 왜 만드는가", BLUE),
        ("tools", "무료 브라우저 도구", "설치 없이 지금 바로 쓰는 도구 6종", BLUE),
        ("stories", "모멘터스 이야기", "만들면서 배운 것을 적습니다", BLUE),
    ]
    return out


def main() -> int:
    force = "--force" in sys.argv
    try:
        import PIL  # noqa: F401
    except ImportError:
        print("  og: Pillow 없음 — 이미지 생성 건너뜀 (pip3 install Pillow)")
        return 0

    made = skipped = 0
    for slug, title, sub, accent in targets():
        p = OUT / f"{slug}.png"
        if p.exists() and not force:
            skipped += 1
            continue
        try:
            render(p, title, sub, accent)
            made += 1
        except Exception as e:  # noqa: BLE001 — OG 이미지 때문에 빌드를 죽이지 않는다
            print(f"  og: {slug} 생성 실패({e}) — 건너뜀")
    print(f"  og/: {made}개 생성, {skipped}개 유지 (1200×630)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
