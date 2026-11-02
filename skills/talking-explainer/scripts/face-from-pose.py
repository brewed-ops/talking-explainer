"""Blinks + lip-sync mouth patches built from each POSE's own face (flat 2D mascots). Replaces blink-fit + mouth-fit.

usage: <py> <skill>/scripts/face-from-pose.py <mascot_dir> [--mouth-scale 1.0] [--only idle,point] [--review out.png]
Why: blink-fit / mouth-fit paste features from the separate faces sheet. When that sheet draws the face at other
proportions than the pose sheet (a half-body client mascot), every blink smeared the open eyes under the lids and cut
a hard edge in the hair, and every talking mouth sat 10-20 px off the drawn smile - so the mouth jumped on each word.
1. Per pose: the resting mouth = the red lip blob (+ its dark smile line and curled corners); the eyes = the two big
   solid dark blobs above it (eyebrows are thin arcs, so the fill-ratio test drops them).
2. Blink: paint each eye out with the skin around it, draw a closed lid arc + one lash. poses/<pose>-blink.png.
3. Mouths: the 6 sheet mouths (faces/mouth-*.png) as INK ONLY, scaled by pose smile width / sheet smile width,
   placed with the sheet's own offset from its smile (eye-band aligned), over a cover of the pose's skin.
   closed = the pose's own mouth (transparent patch) so short dips never swap to a different-looking mouth.
   Paint only lands on the FACE's skin + the resting mouth: a finger or hand in front of the mouth (think pose)
   keeps its pixels, so it stays in front.
Writes mouths/<pose>/*.png + mouth-fit.json + poses/*-blink.png (originals backed up once to <dir>/_backup-face/),
and _face-review.png (every pose: base, blink, each mouth) - read it before rendering.
"""
import sys, json, shutil
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

D = Path(sys.argv[1])
MS = float(sys.argv[sys.argv.index("--mouth-scale") + 1]) if "--mouth-scale" in sys.argv else 1.0
ONLY = sys.argv[sys.argv.index("--only") + 1].split(",") if "--only" in sys.argv else None
REVIEW = Path(sys.argv[sys.argv.index("--review") + 1]) if "--review" in sys.argv else D / "_face-review.png"
MOUTHS = ["closed", "small", "open", "wide", "round", "fv"]


def rgba(p): return np.asarray(Image.open(p).convert("RGBA")).astype(np.float32)
def lum(a): return a[..., :3] @ np.array([0.299, 0.587, 0.114])
def red(a): return (a[..., 0] - a[..., 1] > 110) & (a[..., 1] < 110) & (a[..., 0] > 140) & (a[..., 3] > 200)  # lips ~(205,50,83); tan skin (221,150,89) has R-G 71


def biggest(mask):
    lab, n = ndimage.label(mask)
    if not n:
        return mask
    return lab == int(np.argmax(np.bincount(lab.ravel())[1:])) + 1


def face_skin(a, near):
    """Median of the light, opaque pixels in a ring around `near` = this face's skin."""
    ring = ndimage.binary_dilation(near, iterations=30) & ~ndimage.binary_dilation(near, iterations=8)
    px = a[..., :3][ring & (a[..., 3] > 250) & (lum(a) > 120)]
    return np.median(px, 0)


def rest_mouth(a):
    """(mask, skin) of the resting mouth: the biggest red blob in the lower-middle face + nearby dark line/corners."""
    H, W = a.shape[:2]
    r = red(a)
    r[: int(H * 0.15)] = False; r[int(H * 0.6):] = False  # the face sits in the top of a half-body sprite
    lips = biggest(r)
    if lips.sum() < 50:
        return None, None
    skin = face_skin(a, lips)
    ys, xs = np.nonzero(lips)
    k = max(6, int((xs.max() - xs.min()) * 0.12))
    near = ndimage.binary_dilation(lips, iterations=k)
    nonskin = (np.abs(a[..., :3] - skin).max(-1) > 28) & (a[..., 3] > 200)
    lab, n = ndimage.label(nonskin & ndimage.binary_dilation(lips, iterations=3 * k))
    keep = np.zeros_like(lips)
    for j in range(1, n + 1):
        c = lab == j
        if (c & near).any() and (c & ~near).sum() < 0.15 * c.sum():  # mostly inside the mouth zone = smile, not a finger
            keep |= c
    return keep | lips, skin


def eyes(a, mouth):
    ys, xs = np.nonzero(mouth)
    mw = xs.max() - xs.min(); mcx, mcy = (xs.min() + xs.max()) / 2, ys.min()
    y0, y1 = int(max(0, mcy - 2.0 * mw)), int(mcy - 0.2 * mw)  # flat 2D face: eyes end ~0.4 smile-widths above the smile
    x0, x1 = int(max(0, mcx - 1.3 * mw)), int(min(a.shape[1], mcx + 1.3 * mw))
    dark = np.zeros(a.shape[:2], bool)
    dark[y0:y1, x0:x1] = (lum(a[y0:y1, x0:x1]) < 70) & (a[y0:y1, x0:x1, 3] > 200)
    dark = ndimage.binary_fill_holes(dark)  # the white highlight is part of the eye
    lab, n = ndimage.label(dark)
    c = []
    for j, sl in enumerate(ndimage.find_objects(lab), 1):
        h, w = sl[0].stop - sl[0].start, sl[1].stop - sl[1].start
        fill = (lab[sl] == j).sum() / max(1, h * w)
        if fill > 0.6 and 0.9 < h / max(1, w) < 2.4 and 0.25 * mw < w < 0.8 * mw:
            c.append(((lab[sl] == j).sum(), j, sl))
    # the eyes = the pair most alike in size and height, one each side of the mouth (a hair clump can pass alone)
    best, pair = 1e18, []
    for i, (ai, ji, si) in enumerate(c):
        for ak, jk, sk in c[i + 1:]:
            l_, r_ = sorted([(si, ji), (sk, jk)], key=lambda t: t[0][1].start)
            if not (l_[0][1].stop < mcx < r_[0][1].start):
                continue
            cost = abs(ai - ak) / max(ai, ak) + abs(si[0].start - sk[0].start) / mw
            if cost < best:
                best, pair = cost, [(lab == l_[1], l_[0]), (lab == r_[1], r_[0])]
    return pair if best < 0.6 else []


def blink(a, mouth, skin):
    out = a.copy()
    E = eyes(a, mouth)
    if len(E) != 2:
        return None
    ink = np.median(a[..., :3][E[0][0] & (lum(a) < 50)], 0)
    S = 4
    layer = Image.new("RGBA", (a.shape[1] * S, a.shape[0] * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    face_cx = np.mean([(sl[1].start + sl[1].stop) / 2 for _, sl in E])
    for m, sl in E:
        # fill = mean of the row and column interpolations between the clean skin either side (the mask-region way).
        # A flat median fill left an oval; a normalized blur went dark mid-eye. 12 px takes in the art's line halo.
        cover = ndimage.binary_dilation(m, iterations=12)
        y0, y1, x0, x1 = sl[0].start - 30, sl[0].stop + 30, sl[1].start - 30, sl[1].stop + 30
        sub, cv = out[y0:y1, x0:x1], cover[y0:y1, x0:x1]
        acc, cnt = np.zeros(sub.shape[:2] + (3,)), np.zeros(sub.shape[:2])
        for axis in (0, 1):
            S_, C_ = (sub, cv) if axis == 1 else (sub.transpose(1, 0, 2), cv.T)
            A_, N_ = (acc, cnt) if axis == 1 else (acc.transpose(1, 0, 2), cnt.T)
            for i in range(C_.shape[0]):
                idx = np.nonzero(C_[i])[0]
                if not len(idx) or idx[0] == 0 or idx[-1] == C_.shape[1] - 1:
                    continue
                a0, b0 = S_[i, idx[0] - 1, :3], S_[i, idx[-1] + 1, :3]
                t = ((idx - idx[0] + 1) / (idx[-1] - idx[0] + 2))[:, None]
                A_[i, idx] += a0 * (1 - t) + b0 * t; N_[i, idx] += 1
        raw = np.where((cnt > 0)[..., None], acc / np.maximum(cnt, 1)[..., None], sub[..., :3])  # zeros outside bled in as a dark rim
        fill = ndimage.uniform_filter(raw, (5, 5, 1))
        feather = np.clip(ndimage.distance_transform_edt(cv) / 3, 0, 1)[..., None] * (cnt > 0)[..., None]
        sub[..., :3] = sub[..., :3] * (1 - feather) + fill * feather
        sub[cv, 3] = 255
        h, w = sl[0].stop - sl[0].start, sl[1].stop - sl[1].start
        cx, cy = (sl[1].start + sl[1].stop) / 2, sl[0].start + h * 0.55
        hw, sag, sw = w * 0.62, h * 0.16, max(3, w * 0.13)
        box = [(cx - hw) * S, (cy - sag * 2) * S, (cx + hw) * S, (cy + sag * 2) * S]
        d.arc(box, 15, 165, fill=tuple(int(v) for v in ink) + (255,), width=int(sw * S))  # closed lid, curving down
        side = 1 if cx > face_cx else -1  # one lash at the outer corner
        lx, ly = cx + side * hw * 0.92, cy + sag * 0.35
        d.line([lx * S, ly * S, (lx + side * w * 0.22) * S, (ly - h * 0.12) * S], fill=tuple(int(v) for v in ink) + (255,), width=int(sw * 0.8 * S))
    lay = np.asarray(layer.resize((a.shape[1], a.shape[0]), Image.LANCZOS)).astype(np.float32)
    al = lay[..., 3:] / 255
    out[..., :3] = out[..., :3] * (1 - al) + lay[..., :3] * al
    return out


# ---- the sheet's mouths: ink + offset from the sheet smile ----
N = rgba(D / "faces/neutral.png")
n_rest, n_skin = rest_mouth(N)
nys, nxs = np.nonzero(n_rest)
n_w, n_top, n_cx = nxs.max() - nxs.min(), nys.min(), (nxs.min() + nxs.max()) / 2
H0, W0 = N.shape[:2]
g0 = lum(N) * N[..., 3] / 255 + 255 * (1 - N[..., 3] / 255)
eb = g0[int(n_top - 2.4 * n_w):int(n_top - 0.6 * n_w), int(n_cx - 1.8 * n_w):int(n_cx + 1.8 * n_w)]  # eye band


def align(img):
    g = lum(img) * img[..., 3] / 255 + 255 * (1 - img[..., 3] / 255)
    y0, x0 = int(n_top - 2.4 * n_w), int(n_cx - 1.8 * n_w)
    def search(cands):
        best = (1e18, 0, 0)
        for dy, dx in cands:
            yy, xx = y0 + dy, x0 + dx
            if yy < 0 or xx < 0 or yy + eb.shape[0] > g.shape[0] or xx + eb.shape[1] > g.shape[1]:
                continue
            e = np.abs(g[yy:yy + eb.shape[0], xx:xx + eb.shape[1]] - eb)[::3, ::3].mean()
            if e < best[0]:
                best = (e, dy, dx)
        return best
    # the face cells are cut one by one, so their framing differs by up to ~100 px: coarse, then fine
    _, cy_, cx_ = search([(dy, dx) for dy in range(-120, 121, 6) for dx in range(-120, 121, 6)])
    e, dy, dx = search([(cy_ + a, cx_ + b) for a in range(-6, 7) for b in range(-6, 7)])
    return dy, dx


sheet = {}
for m in MOUTHS[1:]:
    F = rgba(D / f"faces/mouth-{m}.png")
    dy, dx = align(F)
    # the new mouth: everything not-skin around the red/teeth area under the nose, holes filled
    zone = np.zeros(F.shape[:2], bool)
    zy, zx = int(n_top + dy - 0.5 * n_w), int(n_cx + dx)
    zone[max(0, zy):int(zy + 1.3 * n_w), max(0, int(zx - 0.9 * n_w)):int(zx + 0.9 * n_w)] = True
    nonskin = (np.abs(F[..., :3] - n_skin).max(-1) > 40) & (F[..., 3] > 200) & zone
    core = biggest(nonskin)
    ys, xs = np.nonzero(core)
    box = (ys.min(), ys.max(), xs.min(), xs.max())
    # + the parts inside its box (teeth, tongue, inner lip)
    inside = np.zeros_like(core); inside[box[0]:box[1] + 1, box[2]:box[3] + 1] = True
    ink = ndimage.binary_fill_holes(core | (nonskin & inside))
    ink = ndimage.binary_dilation(ink, iterations=1) & (np.abs(F[..., :3] - n_skin).max(-1) > 8)
    ys, xs = np.nonzero(ink)
    crop = F[ys.min():ys.max() + 1, xs.min():xs.max() + 1].copy()
    cm = ink[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    crop[..., 3] = np.where(cm, crop[..., 3], 0)
    # offset of this mouth's top/centre from the sheet smile, in sheet px, eye-aligned
    sheet[m] = (crop, ys.min() - dy - n_top, (xs.min() + xs.max()) / 2 - dx - n_cx)
    print(f"sheet mouth-{m:<6} aligned dy {dy:+d} dx {dx:+d}  ink {crop.shape[1]}x{crop.shape[0]}  top {sheet[m][1]:+.0f}  cx {sheet[m][2]:+.0f}")

# ---- per pose ----
bk = D / "_backup-face"
if not bk.exists():
    shutil.copytree(D / "mouths", bk / "mouths")
    (bk / "poses").mkdir(parents=True)
    (bk / ".gitignore").write_text("*\n")  # old sprites git already has - keep the backup local
    for p in (D / "poses").glob("*-blink.png"):
        shutil.copy2(p, bk / "poses" / p.name)
    for f in ("mouth-fit.json", "blink-fit.json"):
        if (D / f).exists():
            shutil.copy2(D / f, bk / f)
    print("originals backed up to", bk)

fit = json.loads((D / "mouth-fit.json").read_text())
poses = [p for p in fit if not ONLY or p in ONLY]
out_fit, rows = dict(fit), []
for pose in poses:
    P = rgba(D / f"poses/{pose}.png")
    rest, skin = rest_mouth(P)
    if rest is None:
        print(f"{pose}: no resting mouth found, skipped"); continue
    ys, xs = np.nonzero(rest)
    p_w, p_top, p_cx = xs.max() - xs.min(), ys.min(), (xs.min() + xs.max()) / 2
    s = p_w / sheet["wide"][0].shape[1] * MS  # widest mouth = smile width (the sheet draws its smile narrower than its mouths)
    # the face's skin around the mouth = where paint may land (a finger's skin is a separate region)
    pad = int(p_w * 0.9)
    X0, Y0 = int(max(0, p_cx - pad)), int(max(0, p_top - pad * 0.45))
    X1, Y1 = int(min(P.shape[1], p_cx + pad)), int(min(P.shape[0], p_top + pad * 1.25))
    win = P[Y0:Y1, X0:X1]
    r_w = rest[Y0:Y1, X0:X1]
    skinish = (np.abs(win[..., :3] - skin).max(-1) <= 28) & (win[..., 3] > 200)
    lab, n = ndimage.label(skinish)
    touch = np.unique(lab[ndimage.binary_dilation(r_w, iterations=3) & skinish])
    face = np.isin(lab, touch[touch > 0])
    face = biggest(face) | r_w
    allowed = ndimage.binary_dilation(face, iterations=1) & ~(~face & ~r_w & (lum(win) < 90))  # never over a line that is not the mouth
    cover = ndimage.binary_dilation(r_w, iterations=3) & allowed
    (D / "mouths" / pose).mkdir(parents=True, exist_ok=True)
    Image.new("RGBA", (X1 - X0, Y1 - Y0), (0, 0, 0, 0)).save(D / "mouths" / pose / "closed.png")
    tiles = [win]
    for m, (crop, dtop, dcx) in sheet.items():
        w2, h2 = max(1, round(crop.shape[1] * s)), max(1, round(crop.shape[0] * s))
        cr = np.asarray(Image.fromarray(crop.round().astype(np.uint8), "RGBA").resize((w2, h2), Image.LANCZOS)).astype(np.float32)
        cr[..., :3] = np.where((np.abs(cr[..., :3] - n_skin).max(-1) < 30)[..., None], skin, cr[..., :3])
        oy = int(round(p_top + dtop * s)) - Y0
        ox = int(round(p_cx + dcx * s - w2 / 2)) - X0
        patch = np.zeros_like(win)
        patch[cover, :3] = skin; patch[cover, 3] = 255
        y0, x0 = max(0, oy), max(0, ox)
        y1, x1 = min(win.shape[0], oy + h2), min(win.shape[1], ox + w2)
        sub = cr[y0 - oy:y1 - oy, x0 - ox:x1 - ox]
        al = sub[..., 3:] / 255 * allowed[y0:y1, x0:x1, None]
        tgt = patch[y0:y1, x0:x1]
        base_rgb = np.where(tgt[..., 3:] > 0, tgt[..., :3], win[y0:y1, x0:x1, :3])
        tgt[..., :3] = base_rgb * (1 - al) + sub[..., :3] * al
        tgt[..., 3] = np.maximum(tgt[..., 3], al[..., 0] * 255)
        Image.fromarray(patch.round().astype(np.uint8), "RGBA").save(D / "mouths" / pose / f"{m}.png", optimize=True)
        t = win.copy(); a2 = patch[..., 3:] / 255
        t[..., :3] = t[..., :3] * (1 - a2) + patch[..., :3] * a2
        tiles.append(t)
    out_fit[pose] = {"x": X0, "y": Y0, "w": X1 - X0, "h": Y1 - Y0, "score": fit[pose].get("score", 1.0), "from": "pose"}
    b = blink(P, rest, skin)
    if b is not None:
        Image.fromarray(b.round().astype(np.uint8), "RGBA").save(D / f"poses/{pose}-blink.png", optimize=True)
    else:
        print(f"{pose}: eyes not found, blink left as it was")
    by = int(max(0, p_top - 2.6 * p_w)); bx0, bx1 = int(max(0, p_cx - 1.6 * p_w)), int(p_cx + 1.6 * p_w)
    eyesrc = b if b is not None else P
    row = [P[by:Y1, bx0:bx1], eyesrc[by:Y1, bx0:bx1]] + tiles[1:]
    rows.append((pose, row))
    print(f"{pose:<10} smile {p_w}px wide at {p_cx:.0f},{p_top}  scale {s:.3f}  patch {X0},{Y0} {X1 - X0}x{Y1 - Y0}  blink {'ok' if b is not None else 'NO'}")

(D / "mouth-fit.json").write_text(json.dumps(out_fit, indent=1))
T = 200
sheet_img = Image.new("RGB", (T * 7, T * len(rows)), "white")
for r, (pose, row) in enumerate(rows):
    for c, t in enumerate(row):
        im = Image.fromarray(t.round().astype(np.uint8), "RGBA"); im.thumbnail((T, T))
        bg = Image.new("RGBA", (T, T), "white"); bg.alpha_composite(im, ((T - im.width) // 2, (T - im.height) // 2))
        ImageDraw.Draw(bg).text((3, 3), pose if c == 0 else ["", "blink"] [c] if c < 2 else MOUTHS[c - 1], fill="red")
        sheet_img.paste(bg.convert("RGB"), (c * T, r * T))
sheet_img.save(REVIEW)
print("review:", REVIEW)
