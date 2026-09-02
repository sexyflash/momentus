"""i2i 가 만든 장면의 '마젠타 스크린'을 찾아 실제 캡처를 원근 맞춰 끼워넣는다.

왜 이렇게 하나: 캡처를 i2i 에 그대로 넣으면 모델이 화면 안 한글·숫자를 다시 그려
없는 값을 지어낸다(실측). 그래서 i2i 는 *장면*만 만들고(화면은 순수 마젠타 판),
실제 화면은 여기서 픽셀 그대로 워프해 넣는다. 크로마키와 같은 원리."""
import sys
import numpy as np
from PIL import Image, ImageFilter, ImageDraw

def screen_quad(scene):
    a = np.asarray(scene.convert('RGB')).astype(np.int16)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mask = (r > 140) & (b > 140) & (g < 120) & (abs(r - b) < 90)
    ys, xs = np.nonzero(mask)
    if len(xs) < 5000:
        raise SystemExit('마젠타 스크린을 못 찾았다 (픽셀 %d)' % len(xs))
    s, d = xs + ys, xs - ys
    tl = (xs[s.argmin()], ys[s.argmin()]); br = (xs[s.argmax()], ys[s.argmax()])
    tr = (xs[d.argmax()], ys[d.argmax()]); bl = (xs[d.argmin()], ys[d.argmin()])
    return [tl, tr, br, bl], Image.fromarray((mask * 255).astype(np.uint8), 'L')

def coeffs(dst, src):
    """dst(장면 4점) -> src(캡처 4점) 매핑 계수. PIL PERSPECTIVE 는 역방향을 받는다."""
    A, B = [], []
    for (x, y), (u, v) in zip(dst, src):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); B.append(u)
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y]); B.append(v)
    return np.linalg.solve(np.asarray(A, float), np.asarray(B, float))


def quad_ratio(q):
    """쿼드의 가로/세로 비. 화면 비율을 맞춰 넣어 글자가 눌리는 걸 막는다."""
    w = (abs(q[1][0]-q[0][0]) + abs(q[2][0]-q[3][0])) / 2.0
    h = (abs(q[3][1]-q[0][1]) + abs(q[2][1]-q[1][1])) / 2.0
    return (w / h) if h else 1.0


def fit_aspect(shot, ratio):
    """캡처를 쿼드 비율에 맞춰 가운데 크롭. ⚠️ 비율을 안 맞추면 원근 워프가
       가로/세로를 눌러 글자가 찌그러진다(2026-09-02 대표 지적)."""
    w, h = shot.size
    if ratio <= 0:
        return shot
    if w / h > ratio:                       # 가로가 남는다 → 좌우를 자른다
        nw = int(round(h * ratio))
        x = (w - nw) // 2
        return shot.crop((x, 0, x + nw, h))
    nh = int(round(w / ratio))              # 세로가 남는다 → 위쪽을 살리고 아래를 자른다
    return shot.crop((0, 0, w, min(h, nh)))


def kill_fringe(out, rounds=3):
    """합성 뒤 남은 얇은 마젠타 테두리를 이웃 색으로 메운다.
       ⚠️ 예전엔 마스크를 MaxFilter(9)로 넓혀 덮었는데, 얇은 베젤(2~3px)까지
          같이 먹어 모니터 테두리가 끊겼다. 이제 마스크는 최소만 넓히고
          남은 fringe 는 여기서 지운다."""
    a = np.asarray(out).astype(np.int16)
    for _ in range(rounds):
        r, g, b = a[..., 0], a[..., 1], a[..., 2]
        mag = (r > 110) & (b > 110) & (g < 130) & (np.abs(r - b) < 110) & ((r - g) > 40) & ((b - g) > 40)
        if not mag.any():
            break
        good = (~mag).astype(np.float32)[..., None]
        src = a.astype(np.float32) * good
        acc = np.zeros_like(src); cnt = np.zeros_like(good)
        for dy, dx in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)):
            acc += np.roll(np.roll(src, dy, 0), dx, 1)
            cnt += np.roll(np.roll(good, dy, 0), dx, 1)
        fill = np.divide(acc, np.maximum(cnt, 1e-6))
        a = np.where(mag[..., None] & (cnt > 0), fill.astype(np.int16), a)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGB')


def fit(scene_path, shot_path, out_path, glow=0.55, dim=0.93, crop=None):
    scene = Image.open(scene_path).convert('RGB')
    shot = Image.open(shot_path).convert('RGB')
    if crop:
        shot = shot.crop(crop)
    quad, mask = screen_quad(scene)
    shot = fit_aspect(shot, quad_ratio(quad))
    # 워프도 화면 밖으로 살짝 넘치게 — 베젤 몇 픽셀을 덮는 게 마젠타가 남는 것보다 낫다
    cx = sum(p[0] for p in quad) / 4.0
    cy = sum(p[1] for p in quad) / 4.0
    quad = [(cx + (x - cx) * 1.02, cy + (y - cy) * 1.02) for x, y in quad]
    W, H = scene.size
    # ⚠️ 지글거림(모아레) 방지 — 2880px 캡처를 곧장 작은 사각형으로 워프하면 표본이 듬성해져
    #    글자가 떨린다. 목표 크기의 1.4배로 LANCZOS 로 먼저 줄인 뒤 워프한다(2026-09-01 대표 지적).
    qw = max(abs(quad[1][0] - quad[0][0]), abs(quad[2][0] - quad[3][0]))
    tgt = int(qw * 1.4)
    if 0 < tgt < shot.width:
        shot = shot.resize((tgt, max(1, int(shot.height * tgt / shot.width))), Image.LANCZOS)
    sw, sh = shot.size
    src = [(0, 0), (sw, 0), (sw, sh), (0, sh)]
    warped = shot.transform((W, H), Image.PERSPECTIVE, coeffs(quad, src), Image.BICUBIC)

    # 마젠타는 가장자리에서 안티에일리어싱으로 번진다. 마스크를 *깎으면* 그 번진 띠가
    # 그대로 드러나 보라 테두리가 남는다 — 반대로 **넓혀서** 덮어야 한다(2026-09-01 실측).
    m = mask.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(0.6))
    out = scene.copy()
    out.paste(Image.eval(warped, lambda v: int(v * dim)), (0, 0), m)

    # 화면이 방을 물들이는 빛 — 장면과 붙어 보이게
    if glow:
        halo = Image.new('RGB', (W, H), (0, 0, 0))
        halo.paste(warped, (0, 0), m)
        halo = halo.filter(ImageFilter.GaussianBlur(90))
        out = Image.blend(out, Image.fromarray(
            np.clip(np.asarray(out, np.int16) + np.asarray(halo, np.int16) * glow, 0, 255).astype(np.uint8)), 0.75)
    out = kill_fringe(out)
    out.save(out_path, quality=96, subsampling=0)
    return out_path, quad

if __name__ == '__main__':
    p, q = fit(sys.argv[1], sys.argv[2], sys.argv[3])
    print(p, '| quad', q)


def _quad_from_mask(mask_arr, x0, x1):
    ys, xs = np.nonzero(mask_arr[:, x0:x1])
    xs = xs + x0
    s, d = xs + ys, xs - ys
    return [(xs[s.argmin()], ys[s.argmin()]), (xs[d.argmax()], ys[d.argmax()]),
            (xs[s.argmax()], ys[s.argmax()]), (xs[d.argmin()], ys[d.argmin()])]


def screen_quads(scene, n=2):
    """마젠타 화면이 여러 개인 장면 — 열 히스토그램의 빈 구간으로 갈라 좌→우 순서로 돌려준다."""
    a = np.asarray(scene.convert('RGB')).astype(np.int16)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    m = (r > 140) & (b > 140) & (g < 120) & (abs(r - b) < 90)
    cols = m.sum(axis=0)
    on = np.nonzero(cols > 5)[0]
    if len(on) == 0:
        raise SystemExit('마젠타 없음')
    # 켜진 열 사이의 가장 큰 빈 구간을 경계로
    gaps = [(on[i + 1] - on[i], i) for i in range(len(on) - 1)]
    gaps.sort(reverse=True)
    cuts = sorted(on[i] + (on[i + 1] - on[i]) // 2 for _, i in gaps[:n - 1])
    bounds = [on[0]] + cuts + [on[-1] + 1]
    quads = [_quad_from_mask(m, bounds[i], bounds[i + 1]) for i in range(n)]
    return quads, Image.fromarray((m * 255).astype(np.uint8), 'L')


def fit_multi(scene_path, shot_paths, out_path, crops=None, glow=0.10, dim=1.0):
    scene = Image.open(scene_path).convert('RGB')
    quads, mask = screen_quads(scene, len(shot_paths))
    W, H = scene.size
    m = mask.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(0.6))
    out = scene.copy()
    for i, sp in enumerate(shot_paths):
        shot = Image.open(sp).convert('RGB')
        if crops and crops[i]:
            shot = shot.crop(crops[i])
        q = quads[i]
        shot = fit_aspect(shot, quad_ratio(q))
        cx = sum(p[0] for p in q) / 4.0
        cy = sum(p[1] for p in q) / 4.0
        q = [(cx + (x - cx) * 1.02, cy + (y - cy) * 1.02) for x, y in q]
        qw = max(abs(q[1][0] - q[0][0]), abs(q[2][0] - q[3][0]))
        tgt = int(qw * 1.4)
        if 0 < tgt < shot.width:
            shot = shot.resize((tgt, max(1, int(shot.height * tgt / shot.width))), Image.LANCZOS)
        sw, sh = shot.size
        warped = shot.transform((W, H), Image.PERSPECTIVE,
                                coeffs(q, [(0, 0), (sw, 0), (sw, sh), (0, sh)]), Image.BICUBIC)
        # 이 화면 영역만 잘라 붙인다
        box = Image.new('L', (W, H), 0)
        ImageDraw.Draw(box).polygon([tuple(map(int, p)) for p in q], fill=255)
        sub = Image.new('L', (W, H), 0)
        sub.paste(m, (0, 0), box)
        out.paste(Image.eval(warped, lambda v: int(v * dim)), (0, 0), sub)
    out = kill_fringe(out)
    out.save(out_path, quality=96, subsampling=0)
    return out_path, quads
