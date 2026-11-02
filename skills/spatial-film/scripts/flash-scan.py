"""Find single-frame flashes in a final render: a frame that differs from BOTH neighbours while the neighbours
match (an element shown for 1/60s). Usage: <py> <engine>/scripts/flash-scan.py <video.mp4> [threshold]
render-final.mjs runs it after every render; any FLASH line is a bug (first found: 44.000s in an intro film)."""
import subprocess, sys
import numpy as np

src = sys.argv[1]
thr = float(sys.argv[2]) if len(sys.argv) > 2 else 4.0
W, H = 96, 96
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', src, '-vf', f'scale={W}:{H}', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'],
                     capture_output=True, check=True).stdout
f = np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.int16)
hits = 0
for i in range(1, len(f) - 1):
    a = np.abs(f[i] - f[i - 1]).mean()
    b = np.abs(f[i] - f[i + 1]).mean()
    n = np.abs(f[i + 1] - f[i - 1]).mean()
    if a > thr and b > thr and n < a / 3:
        hits += 1
        print(f'FLASH frame {i} ({i / 60:.3f}s): vs prev {a:.1f}, vs next {b:.1f}, prev vs next {n:.1f}')
print(f'{len(f)} frames scanned, {hits} flash(es)')
