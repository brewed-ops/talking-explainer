"""Pull frames from a RENDERED film into one contact sheet - the checks the per-scene harness cannot do.

usage: <py> <skill>/scripts/frames.py <film.mp4> <out.jpg> --at 5.2,12.9,25.0 [--zone]
  default : full frames, 3 per row (portrait: 6 per row) - one per scene (pick a mid-beat time per scene).
  --zone  : landscape - the LEFT 1100px only with a red line at x 620 (the presenter's right edge), 5 per row.
            portrait (1080x1920, TikTok) - the full frame with the presenter box in red (x < 560, y > 1060) and
            TikTok's UI in orange (top y 150, right rail x 930 from y 680-1540, bottom y 1540), 6 per row.
            Pick every ZOOM peak. Any scene content inside a red/orange area is a zone violation (the harness has
            no presenter, so workers cannot see this).
"""
import subprocess, sys, tempfile
from pathlib import Path
from PIL import Image, ImageDraw

src, out = sys.argv[1], sys.argv[2]
times = [float(t) for t in sys.argv[sys.argv.index("--at") + 1].split(",")]
zone = "--zone" in sys.argv
W, H = (int(v) for v in subprocess.run(
    ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", src],
    capture_output=True, text=True, check=True).stdout.strip().split(","))
portrait = H > W
tmp = Path(tempfile.mkdtemp())
ims = []
for i, t in enumerate(times):
    p = tmp / f"{i:03d}.png"
    if portrait:
        vf = "scale=360:-1"
    else:
        vf = "crop=1100:1080:0:0,scale=352:-1" if zone else "scale=640:-1"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", src, "-frames:v", "1", "-vf", vf, str(p)], check=True)
    ims.append((t, Image.open(p).convert("RGB")))
cols = 6 if portrait else (5 if zone else 3)
w, h = ims[0][1].size
rows = (len(ims) + cols - 1) // cols
sheet = Image.new("RGB", (w * cols, h * rows), (0, 0, 0))
d = ImageDraw.Draw(sheet)
for i, (t, im) in enumerate(ims):
    x, y = (i % cols) * w, (i // cols) * h
    sheet.paste(im, (x, y))
    if zone and portrait:
        k = w / W
        d.rectangle([(x, y + 1060 * k), (x + 560 * k, y + 1660 * k)], outline=(255, 0, 0), width=2)
        d.line([(x, y + 150 * k), (x + w, y + 150 * k)], fill=(255, 140, 0), width=1)
        d.line([(x, y + 1540 * k), (x + w, y + 1540 * k)], fill=(255, 140, 0), width=1)
        d.line([(x + 930 * k, y + 680 * k), (x + 930 * k, y + 1540 * k)], fill=(255, 140, 0), width=1)
    elif zone:
        X = x + int(620 * w / 1100)
        d.line([(X, y), (X, y + h)], fill=(255, 0, 0), width=2)
    d.text((x + 5, y + 5), f"{t:g}s", fill=(255, 0, 0))
sheet.save(out, quality=88)
print(out, f"({len(ims)} frames{', zone check' if zone else ''}{', portrait' if portrait else ''})")
