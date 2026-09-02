"""제품 상세 6컷 공통 빌더 — 장면(i2i, 마젠타) + 실제 캡처(픽셀 그대로).
   ⚠️ 캡처 위쪽 모멘터스 검은 GNB 는 반드시 잘라낸다.
   ⚠️ 컷마다 다른 화면을 쓴다."""
import sys, os, json
sys.path.insert(0, "/private/tmp/claude-501/-Users-sexyflash-slack-bot/b010fcfe-946f-48c3-aa30-abd72ceee43c/scratchpad/cap")
from PIL import Image
import screen
from build2 import hero_crop

D   = "/private/tmp/claude-501/-Users-sexyflash-slack-bot/b010fcfe-946f-48c3-aa30-abd72ceee43c/scratchpad/prod/"
OUT = D + "out/"; os.makedirs(OUT, exist_ok=True)
G   = "/Users/sexyflash/slack-bot/.tmp/creagen/"

CFG = json.load(open(sys.argv[1], encoding="utf-8"))

def shot(name, nav):
    """캡처 → (경로, 크롭). 가로 캡처는 GNB 를 자르고 16:9 로 맞춘다.
       ⚠️ 세로(모바일) 캡처에 16:9 크롭을 걸면 상단 띠만 남아 폰 화면에 확대돼 박힌다
          — 세로면 크롭하지 않고 fit_aspect 에 맡긴다(2026-09-02)."""
    p = D + name + ".png"
    im = Image.open(p)
    w, h = im.size
    top = int(nav)
    if h > w:                                   # 세로 캡처(모바일)
        return (p, (0, top, w, h) if top else None)
    return (p, (0, top, w, min(h, top + int(w * 9 / 16))))

for slug, c in CFG.items():
    HS, ZS, DS = G + c["hero_scene"], G + c["zoom_scene"], G + c["duo_scene"]
    def one(scene, sh, name, ratio, w):
        t = OUT + f"_{slug}_{name}.jpg"
        screen.fit(scene, sh[0], t, glow=0.10, dim=1.0, crop=sh[1])
        hero_crop(scene, t, OUT + f"{slug}-{name}.jpg", ratio=ratio, target_w=w)

    S = {k: shot(v, c.get("nav", 88)) for k, v in c["shots"].items()}
    one(HS, S["hero"], "hero", 2.37, 2560)
    one(ZS, S["d1"],   "d1",   1.39, 1500)
    one(ZS, S["d2"],   "d2",   1.39, 1500)
    one(ZS, S["d3"],   "d3",   1.90, 2560)

    t2 = OUT + f"_{slug}_c.jpg"
    screen.fit_multi(DS, [S["cmp_l"][0], S["cmp_r"][0]], t2, crops=[S["cmp_l"][1], S["cmp_r"][1]])
    hero_crop(DS, t2, OUT + f"{slug}-compare.jpg", ratio=2.28, target_w=2560)

    t3 = OUT + f"_{slug}_w.jpg"
    screen.fit_multi(DS, [S["wide_l"][0], S["wide_r"][0]], t3, crops=[S["wide_l"][1], S["wide_r"][1]])
    hero_crop(DS, t3, OUT + f"{slug}-wide.jpg", ratio=2.84, target_w=2560)
    print(slug, "ok", [f"{slug}-{n}.jpg" for n in ("hero","compare","d1","d2","wide","d3")])
