"""Proves every seam and the loop by pixels. Snapshots the assembled film one frame either side of each scene
boundary AND the exact boundary frame (the incoming scene's local 0), plus frame 0 vs the last frame. Every shot
of a seam must match its first one.
Why the boundary frame: a hide done only by a tl.set at 0 never renders on a scene's first frame, so a
film's intro flashed its finished end pose for one frame at 44.000s; the old start-1 / start+1 pair skipped that frame.
Run from the project root after assemble.py:  python <skill>/scripts/seam-check.py [--tol 0.5]
PASS = under --tol percent of pixels differ by more than 12 levels. Whip-pan or held-motion seams may need a
look by eye - the PNGs stay in snapshots/seams/."""
import glob, os, shutil, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from film import ROOT, load, hf
from PIL import Image, ImageChops

tol = float(sys.argv[sys.argv.index('--tol') + 1]) if '--tol' in sys.argv else 0.5
f = load()
fr = 1 / f['fps']
pairs = []  # (label, [times]) - every time must match the first
sl = f['scene_list']
for a, b in zip(sl, sl[1:]):
    pairs.append((f'{a["id"]} -> {b["id"]}', [round(b['start'] - fr, 4), round(b['start'], 4), round(b['start'] + fr, 4)]))
pairs.append((f'loop {sl[-1]["id"]} -> {sl[0]["id"]}', [round(f['total'] - fr, 4), 0.0]))
times = [t for _, ts in pairs for t in ts]
out = os.path.join(ROOT, 'snapshots', 'seams')
shutil.rmtree(out, ignore_errors=True)
# argument list, never a command string; npx is a .cmd shim on Windows, so only there it needs a shell
r = subprocess.run(['npx', '--yes', hf(f), 'snapshot', '--at', ','.join(map(str, times)), '--no-end',
                    '--describe', 'false', '-o', out], shell=os.name == 'nt', capture_output=True, text=True, cwd=ROOT)
shots = sorted(glob.glob(os.path.join(out, 'frame-*.png')), key=lambda p: int(os.path.basename(p).split('-')[1]))
if len(shots) != len(times):
    sys.exit(f'expected {len(times)} snapshots, got {len(shots)}\n{r.stdout[-800:]}{r.stderr[-800:]}')
bad, k = 0, 0
for label, ts in pairs:
    imgs = [Image.open(shots[k + j]).convert('RGB') for j in range(len(ts))]
    k += len(ts)
    pct, worst = 0.0, ts[1]
    for t, im in zip(ts[1:], imgs[1:]):
        diff = ImageChops.difference(imgs[0], im).convert('L').point(lambda v: 255 if v > 12 else 0)
        p = 100 * diff.histogram()[255] / (im.width * im.height)
        if p >= pct:
            pct, worst = p, t
    ok = pct <= tol
    bad += not ok
    print(f'{"PASS" if ok else "FAIL"}  {label:<34} {ts[0]:>8.4f} vs {worst:<8.4f} {pct:6.2f}% differ')
print(f'{len(pairs) - bad}/{len(pairs)} seams match - frames in snapshots/seams/')
sys.exit(1 if bad else 0)
