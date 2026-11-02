"""Fit the sheet's 6 talking mouths onto every front-facing pose, as small overlay patches (lip sync).

usage: <py> <skill>/scripts/mouth-fit.py <mascot_dir> [--band 0.36,0.57] [--min-score 0.5] [--pixel [--mouth-scale 0.75]] [--chin 0.74]   (--chin: lower it below the open mouths' bottom; --pixel: pixel-art mascots, see pixel_mode; --mouth-scale shrinks the talking mouths)
Needs faces/neutral.png + faces/mouth-{closed,small,open,wide,round,fv}.png (references/mascot-sheet-prompt.md
prompt 2, rows 3-4) and blink-fit.json from <engine>/scripts/blink-fit.py run with the SAME --band.

1. Align each mouth face to neutral by its eye band (translation only - same sheet, same scale).
2. The mouth window = where the six mouth faces differ from neutral, padded; feathered ellipse mask.
3. Per pose with a good head fit: map the window into pose pixels with blink-fit's scale + offset, colour-match
   the patch skin to the pose skin (ring around the window), write mouths/<pose>/<mouth>.png + mouth-fit.json.
build-presenter.py picks mouth-fit.json up and drives the patches from the voice (rest = the pose's own mouth).
--ink-only (flat 2D mascots): copy ONLY the mouth ink (lips, teeth, inside) onto a flat
  plate of the pose's own skin, and never paint over a pose line that crosses the window edge (chin, neck shadow,
  hair). The default whole-oval blend pasted the faces sheet's cheek dimple + a second chin line on every word.
  --mouth-scale works here too (0.85 when the open/wide mouths stand taller than the eye).
"""
import sys, json
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage

D = Path(sys.argv[1])
BY = [float(v) for v in sys.argv[sys.argv.index("--band") + 1].split(",")] if "--band" in sys.argv else [0.40, 0.66]
MIN = float(sys.argv[sys.argv.index("--min-score") + 1]) if "--min-score" in sys.argv else 0.5
MS = float(sys.argv[sys.argv.index("--mouth-scale") + 1]) if "--mouth-scale" in sys.argv else 1.0
# chin line (fraction of faces/neutral.png height) - a low mouth needs more (a pixel sloth: mouth at 0.72-0.80 -> 0.84)
CHIN = float(sys.argv[sys.argv.index("--chin") + 1]) if "--chin" in sys.argv else 0.74
MOUTHS = ["closed", "small", "open", "wide", "round", "fv"]
INK = "--ink-only" in sys.argv


def rgba(p): return np.asarray(Image.open(p).convert("RGBA")).astype(np.float32)


def on_white(a): return a[..., :3] * (a[..., 3:] / 255) + 255 * (1 - a[..., 3:] / 255)


N = rgba(D / "faces/neutral.png")
H, W = N.shape[:2]
bx0, by0, bx1, by1 = int(W * 0.08), int(H * BY[0]), int(W * 0.94), int(H * BY[1])
ng = on_white(N).mean(-1)
band = ng[by0:by1, bx0:bx1]


def align(img):
    """(dy, dx) so that img[y+dy, x+dx] ~ N[y, x] - brute force on a 2px grid over the eye band."""
    g = on_white(img).mean(-1)
    best = (1e18, 0, 0)
    for dy in range(-40, 41, 2):
        for dx in range(-30, 31, 2):
            y0, x0 = by0 + dy, bx0 + dx
            if y0 < 0 or x0 < 0 or y0 + band.shape[0] > g.shape[0] or x0 + band.shape[1] > g.shape[1]:
                continue
            e = np.abs(g[y0:y0 + band.shape[0], x0:x0 + band.shape[1]] - band)[::3, ::3].mean()
            if e < best[0]:
                best = (e, dy, dx)
    return best[1], best[2]


faces = {}
for m in MOUTHS:
    im = rgba(D / f"faces/mouth-{m}.png")
    dy, dx = align(im)
    # paste into neutral's frame
    out = np.zeros_like(N); out[..., :3] = 255
    ys, xs = slice(max(0, -dy), min(H, im.shape[0] - dy)), slice(max(0, -dx), min(W, im.shape[1] - dx))
    out[ys, xs] = im[ys.start + dy:ys.stop + dy, xs.start + dx:xs.stop + dx]
    faces[m] = out
    print(f"mouth-{m:<6} aligned dy {dy:+d} dx {dx:+d}")

# the window: union of what changes below the eyes
diff = np.zeros((H, W), bool)
for m, f in faces.items():
    d = np.abs(on_white(f) - on_white(N)).max(-1) > 60
    d[: by1] = False; d[int(H * CHIN):] = False  # below the eyes, above the chin line
    d[:, : int(W * 0.32)] = False; d[:, int(W * 0.68):] = False
    diff |= ndimage.binary_opening(d, iterations=2)
lab, n = ndimage.label(ndimage.binary_dilation(diff, iterations=6))
sizes = ndimage.sum(diff, lab, range(1, n + 1))
diff &= lab == int(np.argmax(sizes)) + 1  # the mouth is the biggest change; jaw-line wobble is not
ys, xs = np.nonzero(diff)
cy, cx = (ys.min() + ys.max()) / 2, (xs.min() + xs.max()) / 2
hh, hw = (ys.max() - ys.min()) / 2 * 1.45 + 14, (xs.max() - xs.min()) / 2 * 1.35 + 18
wy0, wy1, wx0, wx1 = int(cy - hh), int(cy + hh), int(cx - hw), int(cx + hw)
print(f"mouth window (neutral px): x {wx0}-{wx1}, y {wy0}-{wy1}")
yy, xx = np.mgrid[wy0:wy1, wx0:wx1]
r = np.sqrt(((yy - cy) / hh) ** 2 + ((xx - cx) / hw) ** 2)
mask = np.clip((1.0 - r) / 0.28, 0, 1)  # solid core, soft rim

fit = json.loads((D / "blink-fit.json").read_text())
ring = (r > 0.85) & (r < 1.0)


def lum(a): return a[..., :3] @ np.array([0.299, 0.587, 0.114])


def dark_parts(a, thr=110):
    """Labelled dark-ink components (outline, mouth line, collar) of an RGBA crop."""
    return ndimage.label((lum(a) < thr) & (a[..., 3] > 200))


def pixel_mode():
    """--pixel: pixel-art mascots. Never blend face crops: start from the POSE's own window, erase its resting mouth
    (the dark part right under the nose) with its own skin, then stamp only the new mouth's ink (outline + filled
    inside), resized NEAREST, its top on the resting mouth's top. One mouth, one height, the pose's own collar,
    hard pixels. Sheets often draw round/fv as resting mouth + new mouth below - the soft patch showed both."""
    # resting mouth in neutral: the topmost dark part in the window (the nose is pink, the collar sits lower)
    nl, nn = dark_parts(N[wy0:wy1, wx0:wx1])
    edge = set(np.unique(np.concatenate([nl[0], nl[-1], nl[:, 0], nl[:, -1]])))  # eye/cheek bits cut by the window
    tops = [(np.nonzero(nl == i)[0].min(), i) for i in range(1, nn + 1) if (nl == i).sum() > 40 and i not in edge]
    rest = nl == min(tops)[1]
    ry, rx = np.nonzero(rest)
    inks = {}
    for m, face in faces.items():
        if m == "closed":
            continue
        win = face[wy0:wy1, wx0:wx1]
        d = np.abs(on_white(win) - on_white(N[wy0:wy1, wx0:wx1])).max(-1) > 60
        lab, n = dark_parts(win)
        # the new mouth = the biggest dark part that is new (mostly not in neutral)
        best = max(((((lab == i) & d).sum(), i) for i in range(1, n + 1)), default=(0, 0))
        if best[0] < 40:
            print(f"mouth-{m}: no new mouth ink found, skipped"); continue
        line = lab == best[1]
        # + red/pink mouth pixels next to the outline (an open mouth's tongue often has no outline under it)
        ml, mn = ndimage.label((win[..., 0] - win[..., 1] > 60) & d)
        touch = np.unique(ml[ndimage.binary_dilation(line, iterations=3)])
        mouthy = np.isin(ml, touch[touch > 0])
        ink = ndimage.binary_fill_holes(ndimage.binary_closing(line | mouthy, iterations=3))
        ink &= ~(win[..., 2] > win[..., 0] + 20)  # never the sheet's own collar tag (teal) - the pose keeps its own
        lab2, n2 = ndimage.label(ink)
        ink = lab2 == int(np.argmax(np.bincount(lab2.ravel())[1:])) + 1 if n2 else ink
        ys, xs = np.nonzero(ink)
        inks[m] = (win[ys.min():ys.max() + 1, xs.min():xs.max() + 1].copy(), ink[ys.min():ys.max() + 1, xs.min():xs.max() + 1])
    out_fit, tiles = {}, []
    for pose, f in fit.items():
        if f["score"] < MIN:
            continue
        s = f["scale"]
        P = rgba(D / f"poses/{pose}.png")
        X0, Y0 = int(round(f["x"] + (wx0 - bx0) * s)), int(round(f["y"] + (wy0 - by0) * s))
        PW, PH = int(round((wx1 - wx0) * s)), int(round((wy1 - wy0) * s))
        if X0 < 0 or Y0 < 0 or X0 + PW > P.shape[1] or Y0 + PH > P.shape[0]:
            print(f"{pose}: window off-sprite, skipped"); continue
        # the pose's own resting mouth: the dark part overlapping neutral's, mapped. A weak head fit can land the
        # window low (a pixel mascot's "present", fit 0.59: its mouth sat ~40 px above) - slide it up before giving up
        exp = np.zeros((PH, PW), bool)
        exp[np.clip((ry * s).astype(int), 0, PH - 1), np.clip((rx * s).astype(int), 0, PW - 1)] = True
        for shift in (0, PH // 4, PH // 2):
            if Y0 - shift < 0:
                break
            pw_ = P[Y0 - shift:Y0 - shift + PH, X0:X0 + PW]
            pl, pn = dark_parts(pw_)
            hit = np.bincount(pl[ndimage.binary_dilation(exp, iterations=6)], minlength=pn + 1); hit[0] = 0
            if hit.max():
                Y0 -= shift
                if shift: print(f"{pose}: window slid up {shift}px to its resting mouth")
                break
        if hit.max() == 0:
            print(f"{pose}: resting mouth not found, skipped"); continue
        sizes = np.bincount(pl.ravel(), minlength=pn + 1)
        keep = [i for i in range(1, pn + 1) if hit[i] and sizes[i] < 3 * len(ry)]  # a "w" mouth can come in pieces
        prest = np.isin(pl, keep)
        py_, px_ = np.nonzero(prest)
        top, cx_ = py_.min(), (px_.min() + px_.max()) / 2
        skin = np.median(pw_[..., :3][(lum(pw_) > 180) & (pw_[..., 3] > 250) & ~ndimage.binary_dilation(prest, iterations=8)], 0)
        base = pw_.copy()
        base[ndimage.binary_dilation(prest, iterations=6) & (pw_[..., 3] > 200), :3] = skin  # 6: the soft rim of a curled mouth tip is lighter than the ink threshold
        (D / "mouths" / pose).mkdir(parents=True, exist_ok=True)
        Image.fromarray(pw_.round().astype(np.uint8), "RGBA").save(D / "mouths" / pose / "closed.png", optimize=True)
        for m, (rgb, ink) in inks.items():
            h2, w2 = max(1, round(ink.shape[0] * s * MS)), max(1, round(ink.shape[1] * s * MS))
            rgb2 = np.asarray(Image.fromarray(rgb.round().astype(np.uint8), "RGBA").resize((w2, h2), Image.NEAREST)).astype(np.float32)
            ink2 = np.asarray(Image.fromarray(ink.astype(np.uint8) * 255).resize((w2, h2), Image.NEAREST)) > 0
            out = base.copy()
            oy, ox = top, int(round(cx_ - w2 / 2))
            ys, xs = np.nonzero(ink2)
            ty, tx = ys + oy, xs + ox
            ok = (ty >= 0) & (ty < PH) & (tx >= 0) & (tx < PW)
            px = rgb2[ys[ok], xs[ok], :3]
            fskin = np.median(N[wy0:wy1, wx0:wx1][..., :3][lum(N[wy0:wy1, wx0:wx1]) > 180], 0)
            px[np.abs(px - fskin).max(-1) < 40] = skin  # skin caught inside the mouth fill -> this pose's skin
            out[ty[ok], tx[ok], :3] = px
            out[..., 3] = pw_[..., 3]
            a = out.round().astype(np.uint8)
            Image.fromarray(a, "RGBA").save(D / "mouths" / pose / f"{m}.png", optimize=True)
            if pose in ("idle", "present", "point"):
                t = Image.fromarray(P.astype(np.uint8), "RGBA").copy()
                t.alpha_composite(Image.fromarray(a, "RGBA"), (X0, Y0))
                hc = t.crop((max(0, X0 - PW // 3), max(0, Y0 - PH), X0 + PW + PW // 3, Y0 + PH + PH // 3))
                hc.thumbnail((240, 240), Image.NEAREST)
                tile = Image.new("RGB", (250, 250), (20, 26, 40)); tile.paste(hc, (5, 5), hc); tiles.append(tile)
        out_fit[pose] = {"x": X0, "y": Y0, "w": PW, "h": PH, "score": f["score"]}
        print(f"{pose:<10} mouth at {X0},{Y0} {PW}x{PH}  resting mouth top {top}  (head fit {f['score']})")
    (D / "mouth-fit.json").write_text(json.dumps(out_fit, indent=1))
    if tiles:
        cols = 5
        cs = Image.new("RGB", (cols * 250, ((len(tiles) + cols - 1) // cols) * 250), (90, 90, 90))
        for i, t in enumerate(tiles):
            cs.paste(t, ((i % cols) * 250, (i // cols) * 250))
        cs.save(D / "_mouth-review.png")
    print("lip-sync poses:", list(out_fit))
    sys.exit(0)


if "--pixel" in sys.argv:
    pixel_mode()
out_fit, tiles = {}, []
for pose, f in fit.items():
    if f["score"] < MIN:
        continue
    s = f["scale"]
    P = rgba(D / f"poses/{pose}.png")
    # window top-left in pose px
    px0, py0 = f["x"] + (wx0 - bx0) * s, f["y"] + (wy0 - by0) * s
    pw, ph = (wx1 - wx0) * s, (wy1 - wy0) * s
    X0, Y0 = int(round(px0)), int(round(py0))
    PW, PH = int(round(pw)), int(round(ph))
    if X0 < 0 or Y0 < 0 or X0 + PW > P.shape[1] or Y0 + PH > P.shape[0]:
        print(f"{pose}: window off-sprite, skipped"); continue
    pose_win = P[Y0:Y0 + PH, X0:X0 + PW]
    ring_p = np.asarray(Image.fromarray(ring.astype(np.uint8) * 255).resize((PW, PH), Image.NEAREST)) > 0
    pose_skin = np.median(pose_win[..., :3][ring_p & (pose_win[..., 3] > 250)], 0)
    if INK:  # pose pixels that are not skin and reach the window edge (chin line, neck shadow, hair) stay untouched
        nonskin = (np.abs(pose_win[..., :3] - pose_skin).max(-1) > 25) | (pose_win[..., 3] < 200)
        pl, _ = ndimage.label(nonskin)
        edge = set(np.unique(np.concatenate([pl[0], pl[-1], pl[:, 0], pl[:, -1]]))) - {0}
        keep_pose = ndimage.binary_dilation(np.isin(pl, list(edge)), iterations=3)  # 1 left a smudged half-tone chin edge
        # the pose's own resting mouth (interior non-skin: lips, smile line, the curled smile corner) gets a fully
        # opaque cover - under the soft rim its corner showed through as a dark cheek spot on every word
        rest_mouth = ndimage.binary_dilation((pl > 0) & ~np.isin(pl, list(edge)), iterations=4)
    (D / "mouths" / pose).mkdir(parents=True, exist_ok=True)
    for m, face in faces.items():
        win = face[wy0:wy1, wx0:wx1].copy()
        face_skin = np.median(win[..., :3][ring & (win[..., 3] > 250)], 0)
        win[..., :3] = np.clip(win[..., :3] * (pose_skin / np.maximum(face_skin, 1)), 0, 255)
        if INK:
            h_, w_ = win.shape[:2]
            dist = np.abs(win[..., :3] - pose_skin).max(-1)
            il, _ = ndimage.label((dist > 45) & (win[..., 3] > 200))
            cands = []
            for j, sl in enumerate(ndimage.find_objects(il), 1):
                if sl is None or sl[0].start == 0 or sl[1].start == 0 or sl[0].stop == h_ or sl[1].stop == w_:
                    continue  # touches the window edge = chin / cheek / hair, not the mouth
                if 0.15 < (sl[0].start + sl[0].stop) / 2 / h_ < 0.85 and 0.2 < (sl[1].start + sl[1].stop) / 2 / w_ < 0.8:
                    cands.append((int((il[sl] == j).sum()), j, sl))
            core = np.zeros((h_, w_), bool)
            if cands:  # the mouth = the biggest blob + whatever sits inside its box (teeth, tongue); a dimple beside it is out
                _, jm, bm = max(cands)
                for _, j, sl in cands:
                    if sl[0].start >= bm[0].start - 2 and sl[0].stop <= bm[0].stop + 2 and sl[1].start >= bm[1].start - 2 and sl[1].stop <= bm[1].stop + 2:
                        core |= il == j
            ink = ndimage.binary_dilation(core, iterations=2) & (dist > 10)
            layer = np.dstack([win[..., :3], ink * 255.0]).round().astype(np.uint8)
            plate = Image.new("RGBA", (w_, h_), tuple(int(v) for v in pose_skin) + (255,))
            li = Image.fromarray(layer, "RGBA")
            if MS != 1.0 and core.any():
                ys_, xs_ = np.nonzero(core)
                icy, icx = (ys_.min() + ys_.max()) / 2, (xs_.min() + xs_.max()) / 2
                li = li.resize((max(1, round(w_ * MS)), max(1, round(h_ * MS))), Image.LANCZOS)
                plate.alpha_composite(li, (int(round(icx - icx * MS)), int(round(icy - icy * MS))))
            else:
                plate.alpha_composite(li)
            win = np.asarray(plate).astype(np.float32).copy()
        win[..., 3] = win[..., 3] * mask
        im = Image.fromarray(win.round().astype(np.uint8), "RGBA").resize((PW, PH), Image.LANCZOS)
        a = np.asarray(im).copy()
        a[..., 3] = np.minimum(a[..., 3], pose_win[..., 3].astype(np.uint8))  # never paint outside the pose
        if INK:
            a[..., 3][rest_mouth & (pose_win[..., 3] > 0)] = 255
            a[..., 3][keep_pose] = 0
        Image.fromarray(a, "RGBA").save(D / "mouths" / pose / f"{m}.png", optimize=True)
        if pose in ("idle", "present", "sit"):
            t = Image.fromarray(P.astype(np.uint8), "RGBA").copy()
            t.alpha_composite(Image.fromarray(a, "RGBA"), (X0, Y0))
            hc = t.crop((max(0, X0 - PW), max(0, Y0 - PH * 2), X0 + PW * 2, Y0 + PH * 2))
            hc.thumbnail((240, 240))
            tile = Image.new("RGB", (250, 250), (20, 26, 40)); tile.paste(hc, (5, 5), hc); tiles.append(tile)
    out_fit[pose] = {"x": X0, "y": Y0, "w": PW, "h": PH, "score": f["score"]}
    print(f"{pose:<10} mouth at {X0},{Y0} {PW}x{PH}  (head fit {f['score']})")
(D / "mouth-fit.json").write_text(json.dumps(out_fit, indent=1))
if tiles:
    cols = 6
    cs = Image.new("RGB", (cols * 250, ((len(tiles) + cols - 1) // cols) * 250), (90, 90, 90))
    for i, t in enumerate(tiles):
        cs.paste(t, ((i % cols) * 250, (i // cols) * 250))
    cs.save(D / "_mouth-review.png")
print("lip-sync poses:", list(out_fit))
