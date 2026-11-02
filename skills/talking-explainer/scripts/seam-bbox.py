"""Where do two seam frames differ? Prints the bounding box of changed pixels per seam pair, presenter zone masked.

usage (film root, after seam-check.py wrote snapshots/seams/): <py> <skill>/scripts/seam-bbox.py [snapshots/seams]

seam-diff-all.sh reports "outside-presenter N%". A small non-zero value is often the mascot's head poking above the
presenter zone (seen: 0.03%, bbox x 240-370, y 386-400) - the overlay, not scene content. Check the
box before reopening a scene: a box in the stage (x > 640) is a real seam bug.
"""
import re
import sys
from pathlib import Path
from PIL import Image, ImageChops

d = Path(sys.argv[1] if len(sys.argv) > 1 else "snapshots/seams")
frames = sorted(d.glob("frame-*-at-*.png"), key=lambda p: int(re.search(r"frame-(\d+)", p.name).group(1)))
by_idx = {int(re.search(r"frame-(\d+)", p.name).group(1)): p for p in frames}
# seam-check writes three frames per seam (out, mid, in): compare index 3k with 3k+2
for k in range(0, max(by_idx) + 1, 3):
    a, b = by_idx.get(k), by_idx.get(k + 2)
    if not a or not b:
        continue
    A, B = Image.open(a).convert("RGB"), Image.open(b).convert("RGB")
    diff = ImageChops.difference(A, B).convert("L").point(lambda v: 255 if v > 24 else 0)
    s = diff.size[0] / 1920
    diff.paste(0, (0, int(420 * s), int(640 * s), diff.size[1]))   # presenter zone x 0-640, y 420-bottom
    box = diff.getbbox()
    verdict = "clean" if not box else ("stage!" if box[2] > 640 * s and box[3] > 200 * s else "edge/overlay")
    print(f"{a.name} -> {b.name}: {box}  {verdict}")
