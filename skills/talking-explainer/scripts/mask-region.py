"""Paint a box out of a client image (a price, a "TWO WAYS TO ENROLL" block) with the panel's own colour:
each row in the box is interpolated between the smoothed clean row just above and the one just below, so a
flat or gently graded panel reads as untouched. Keeps the original as <work>/<name>-original.png first.
usage: py -3.12 <skill>/scripts/mask-region.py <image> x0,y0,x1,y1 [--work .hyperframes/work] [--smooth 61]
       then view the printed crop before a worker uses the image.
Saved from a client promo 2026-10-27 (a hand-written mask; a raw row copy left vertical streaks,
the uniform_filter1d smoothing fixed them)."""
import argparse
import shutil
from pathlib import Path

import numpy as np
from PIL import Image
from scipy.ndimage import uniform_filter1d

ap = argparse.ArgumentParser()
ap.add_argument("image")
ap.add_argument("box", help="x0,y0,x1,y1 in image pixels; y0/y1 must sit on clean panel rows")
ap.add_argument("--work", default=".hyperframes/work")
ap.add_argument("--smooth", type=int, default=61, help="horizontal smoothing window (px) for the edge rows")
a = ap.parse_args()

src = Path(a.image)
x0, y0, x1, y1 = (int(v) for v in a.box.split(","))
orig = Path(a.work) / f"{src.stem}-original{src.suffix}"
if not orig.exists():
    orig.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, orig)
img = np.asarray(Image.open(orig).convert("RGB")).astype(np.float32)
top = uniform_filter1d(img[max(0, y0 - 6):y0 + 1, x0:x1].mean(0), a.smooth, axis=0)
bot = uniform_filter1d(img[y1:y1 + 7, x0:x1].mean(0), a.smooth, axis=0)
for y in range(y0, y1 + 1):
    t = (y - y0) / max(1, y1 - y0)
    img[y, x0:x1] = top * (1 - t) + bot * t
out = Image.fromarray(img.clip(0, 255).astype(np.uint8))
out.save(src)
crop = Path(a.work) / f"{src.stem}-masked-check.png"
out.crop((max(0, x0 - 60), max(0, y0 - 60), min(out.width, x1 + 60), min(out.height, y1 + 60))).save(crop)
print(f"masked {src} box {a.box}; original kept at {orig}; check {crop}")
