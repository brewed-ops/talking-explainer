"""Slice a NEW mascot's sheets (flat white ground, from references/mascot-sheet-prompt.md) into 4x sprites.

usage: <py> <skill>/scripts/cut-sheet.py --poses <png> --faces <png> --fx <png> <out_dir> [--only poses,faces] [--model <esrgan.pth>]

Finds every sprite itself: anything that is not flat white ground is ink, ink blobs are grouped per cell and read in grid order (rows, then left to right).
Counts must match the prompt (9 poses, 16 faces = 10 expressions + 6 mouths, 5 fx) or it stops.
Then run <engine>/scripts/blink-fit.py <out_dir> --band 0.36,0.57 and <skill>/scripts/mouth-fit.py <out_dir> --band 0.36,0.57.
Sprites are upscaled 4x: with torch + spandrel and a Real-ESRGAN anime model (--model, default
~/.cache/upscalers/RealESRGAN_x4plus_anime_6B.pth, from the xinntao/Real-ESRGAN v0.2.2.4 release) the lines stay
crisp; without them it falls back to Lanczos 4x (softer, fine for a first film).
"""
import sys, json
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage

args = sys.argv[1:]
def opt(k):
    i = args.index(k); v = args[i + 1]; del args[i:i + 2]; return v
only = opt("--only").split(",") if "--only" in args else ["poses", "faces", "fx"]
GAP_LO, GAP_HI = map(float, opt("--gap-band").split(",")) if "--gap-band" in args else (0.35, 0.8)  # half-body: 0.55,0.98
sheets = {g: Path(opt(f"--{g}")) for g in ("poses", "faces", "fx") if f"--{g}" in args}
sheets = {g: p for g, p in sheets.items() if g in only}
model_path = opt("--model") if "--model" in args else str(Path.home() / ".cache/upscalers/RealESRGAN_x4plus_anime_6B.pth")
out_dir = Path(args[0]); out_dir.mkdir(parents=True, exist_ok=True)

NAMES = {
    "poses": ["idle", "wave", "point", "thumbs-up", "celebrate", "walk", "think", "sit", "present"],
    "faces": ["neutral", "blink", "happy", "wide", "thinking", "focused", "wink", "concerned", "sleepy", "sparkle",
              "mouth-closed", "mouth-small", "mouth-open", "mouth-wide", "mouth-round", "mouth-fv"],
    "fx": ["steam", "sparkle-burst", "coffee-ring", "question", "confetti"],
}
MERGE = {"poses": 8, "faces": 8, "fx": 40}  # px dilation that joins one sprite's pieces (confetti, steam curls)
PAD = 10


def ground(a):
    a = a.astype(np.int16)
    return ((a.max(-1) - a.min(-1)) <= 10) & (a.mean(-1) >= 240)


def find_boxes(rgb, group):
    ink = ~ground(rgb)
    ink = ndimage.binary_opening(ink, iterations=1)  # drop JPEG-ish specks in the ground
    lab, n = ndimage.label(ndimage.binary_dilation(ink, iterations=MERGE[group]))
    objs = [sl for sl in ndimage.find_objects(lab)]
    areas = [((sl[0].stop - sl[0].start) * (sl[1].stop - sl[1].start)) for sl in objs]
    big = max(areas)
    boxes = [(sl[0].start, sl[0].stop, sl[1].start, sl[1].stop) for sl, a in zip(objs, areas) if a > 0.08 * big]
    boxes = [(y0 + MERGE[group], y1 - MERGE[group], x0 + MERGE[group], x1 - MERGE[group]) for y0, y1, x0, x1 in boxes]
    # grid order: cluster rows by vertical centre, then left to right
    boxes.sort(key=lambda b: (b[0] + b[1]) / 2)
    h = np.median([b[1] - b[0] for b in boxes])
    rows, cur = [], [boxes[0]]
    for b in boxes[1:]:
        if (b[0] + b[1]) / 2 - (cur[-1][0] + cur[-1][1]) / 2 > 0.5 * h:
            rows.append(cur); cur = [b]
        else:
            cur.append(b)
    rows.append(cur)
    ordered = [b for r in rows for b in sorted(r, key=lambda b: b[2])]
    assert len(ordered) == len(NAMES[group]), f"{group}: found {len(ordered)} sprites, expected {len(NAMES[group])}"
    return ordered


try:
    import torch, spandrel
    model = spandrel.ModelLoader().load_from_file(model_path).eval()
except Exception as e:  # no torch / spandrel / model file
    model = None
    print(f"AI upscaler unavailable ({type(e).__name__}) - using Lanczos 4x", flush=True)


def upscale(rgb):
    if model is None:
        im = Image.fromarray(rgb)
        return np.asarray(im.resize((im.width * 4, im.height * 4), Image.LANCZOS))
    t = torch.from_numpy(rgb).permute(2, 0, 1).float().div(255).unsqueeze(0)
    with torch.no_grad():
        o = model(t).clamp(0, 1)
    return (o[0].permute(1, 2, 0).numpy() * 255).round().astype(np.uint8)


def cutout(rgb, group):
    g = ground(rgb)
    lab, _ = ndimage.label(g)
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    remove = np.isin(lab, list(border))
    a16 = rgb.astype(np.int16)
    lum, sat = a16.mean(-1), a16.max(-1) - a16.min(-1)
    if group == "poses":  # ground trapped between an arm and the body; eye whites live in the head - never touch those
        for i, sl in enumerate(ndimage.find_objects(lab), 1):
            if i in border or sl is None:
                continue
            m = lab[sl] == i
            cy = (sl[0].start + sl[0].stop) / 2 / rgb.shape[0]
            if m.sum() < 400 or not GAP_LO <= cy <= GAP_HI:  # full body: below 0.8 = white sneakers, read as ground
                continue
            if lum[sl][m].mean() >= 251 and sat[sl][m].mean() <= 3:  # pure ground white, not a sneaker
                remove[sl] |= m
                print(f"    gap erased: {int(m.sum())} px at height {cy:.2f}")
    alpha = (~remove).astype(np.float32)
    BG = 254.0
    rim = (~remove) & ndimage.binary_dilation(remove, iterations=2)
    a_rim = np.clip((BG - lum) / (BG - 40.0), 0, 1)
    alpha[rim] = np.minimum(1.0, a_rim[rim] * 1.15)
    out = rgb.astype(np.float32)
    a = alpha[..., None]
    out = np.where(a > 0, (out - (1 - a) * BG) / np.maximum(a, 1e-3), 0)
    out = np.clip(out, 0, 255)
    alpha = ndimage.gaussian_filter(alpha, 0.6) * (alpha > 0)
    rgba = np.dstack([out, alpha * 255]).round().astype(np.uint8)
    if group != "fx":  # keep the figure, drop stray specks
        clab, cn = ndimage.label(rgba[..., 3] > 8)
        sizes = ndimage.sum(np.ones_like(clab), clab, range(1, cn + 1))
        for j in range(1, cn + 1):
            if sizes[j - 1] < 0.01 * sizes.max():
                rgba[..., 3][clab == j] = 0
    ys, xs = np.nonzero(rgba[..., 3] > 8)
    return rgba[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


mf = out_dir / "manifest.json"
manifest = json.loads(mf.read_text()) if mf.exists() else {}
for group, path in sheets.items():
    sheet = np.array(Image.open(path).convert("RGB"))
    (out_dir / group).mkdir(exist_ok=True)
    for name, (y0, y1, x0, x1) in zip(NAMES[group], find_boxes(sheet, group)):
        y0, x0 = max(0, y0 - PAD), max(0, x0 - PAD)
        y1, x1 = min(sheet.shape[0], y1 + PAD), min(sheet.shape[1], x1 + PAD)
        rgba = cutout(upscale(np.ascontiguousarray(sheet[y0:y1, x0:x1])), group)
        Image.fromarray(rgba, "RGBA").save(out_dir / group / f"{name}.png", optimize=True)
        manifest[f"{group}/{name}"] = {"w": rgba.shape[1], "h": rgba.shape[0], "sheet": path.name,
                                       "sheet_box": [int(x0), int(y0), int(x1), int(y1)]}
        print(f"{group}/{name}", rgba.shape[1], "x", rgba.shape[0], flush=True)
(out_dir / "manifest.json").write_text(json.dumps(manifest, indent=1))

# review sheet: every sprite on dark + light ground
tiles = []
for k in manifest:
    im = Image.open(out_dir / f"{k}.png")
    im.thumbnail((260, 300))
    t = Image.new("RGB", (540, 310), (20, 26, 40))
    t.paste((246, 242, 234), (270, 0, 540, 310))
    for ox in (5, 275):
        t.paste(im, (ox + (260 - im.width) // 2, 5 + (300 - im.height) // 2), im)
    tiles.append(t)
cols = 5
rows = (len(tiles) + cols - 1) // cols
cs = Image.new("RGB", (cols * 540, rows * 310), (128, 128, 128))
for i, t in enumerate(tiles):
    cs.paste(t, ((i % cols) * 540, (i // cols) * 310))
cs.save(out_dir / "_review.png")
print("review:", out_dir / "_review.png")
