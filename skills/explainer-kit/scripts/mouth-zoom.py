"""Zoomed lip-sync review: every mouth patch composited on its pose, one row per pose (base, closed, small, open,
wide, round, fv), cropped to the face and blown up NEAREST - the small _mouth-review.png hides a doubled mouth.

usage: py -3.12 mouth-zoom.py <mascot_dir> <out.png> <pose,pose,...>     e.g. point,present,idle
Read it after mouth-fit.py: one mouth per cell, same height across the row, collar/chin untouched.
"""
import sys, json
from pathlib import Path
from PIL import Image
D = Path(sys.argv[1]); OUT = Path(sys.argv[2])
fit = json.loads((D / "mouth-fit.json").read_text())
poses = sys.argv[3].split(",")
M = ["closed", "small", "open", "wide", "round", "fv"]
rows = []
for p in poses:
    f = fit[p]; base = Image.open(D / f"poses/{p}.png").convert("RGBA")
    pad = 60; box = (f["x"] - pad, f["y"] - pad - 120, f["x"] + f["w"] + pad, f["y"] + f["h"] + pad)
    cells = [base.crop(box)]
    for m in M:
        im = base.copy(); im.alpha_composite(Image.open(D / f"mouths/{p}/{m}.png").convert("RGBA"), (f["x"], f["y"]))
        cells.append(im.crop(box))
    w, h = cells[0].size
    row = Image.new("RGB", (w * 7, h), (229, 146, 199))
    for i, c in enumerate(cells): row.paste(c, (i * w, 0), c)
    rows.append(row.resize((row.width // 2, row.height // 2), Image.NEAREST))
sheet = Image.new("RGB", (max(r.width for r in rows), sum(r.height for r in rows)), (20, 20, 20))
y = 0
for r in rows: sheet.paste(r, (0, y)); y += r.height
sheet.save(OUT); print(OUT, sheet.size)
