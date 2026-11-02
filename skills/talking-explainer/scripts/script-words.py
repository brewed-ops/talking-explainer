"""Words per paragraph of SCRIPT.md's "## Script" section, with seconds at the narration pace, the total, and an em-dash check.

usage (film root): <py> <skill>/scripts/script-words.py [SCRIPT.md] [--wps 2.67]

A typical narrated take runs ~160 wpm = 2.67 words/s; measure yours on the first take. Use it for
the STORYBOARD-draft "~sec" column and to check a length ask before the take is recorded.
"""
import sys
from pathlib import Path

wps = float(sys.argv[sys.argv.index("--wps") + 1]) if "--wps" in sys.argv else 2.67
skip = {sys.argv.index("--wps") + 1} if "--wps" in sys.argv else set()
args = [a for i, a in enumerate(sys.argv[1:], 1) if not a.startswith("--") and i not in skip]
src = Path(args[0] if args else "SCRIPT.md").read_text(encoding="utf-8")
body = src.split("## Script", 1)[1].split("\n## ", 1)[0]
paras = [p.strip() for p in body.strip().split("\n\n") if p.strip()]
total = 0
for i, p in enumerate(paras, 1):
    n = len(p.split()); total += n
    print(f"{i:2d}  {n:3d} words  ~{n / wps:5.1f}s  {p[:60]}")
print(f"total {total} words, ~{total / wps / 60:.2f} min, {len(paras)} paragraphs")
if chr(0x2014) in src:
    print("WARNING: em dash found - replace with a hyphen or '...'")
