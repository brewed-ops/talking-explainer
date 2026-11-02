"""Prove the presenter's lip sync against the voice: what the mouth shows INSIDE spoken words vs INSIDE silences.

usage (film root): py -3.12 <skill>/scripts/lipsync-check.py [compositions/m-presenter.html] [src/timing/words.txt] [--db -40]

Reads the mouth-patch timeline build-presenter.py wrote (tl.set opacity 1/0 on <P>-m-<pose>-<mouth>), samples the
middle of every spoken word (from words.txt) and the middle of every measured silence >= 0.3 s (ffmpeg silencedetect
on vo-master.wav), and prints: % of words with a talking mouth on screen (open/wide/round/small/fv), % of silences
with the resting mouth (no patch / closed). Pass mark: words >= 90% talking (the misses are mostly M/B/P words,
correctly closed), silences >= 90% at rest.
"""
import re, subprocess, sys, json
from pathlib import Path

args = [a for a in sys.argv[1:] if not a.startswith("--")]
DB = sys.argv[sys.argv.index("--db") + 1] if "--db" in sys.argv else "-40"
html = Path(args[0] if args else "compositions/m-presenter.html").read_text(encoding="utf-8")
words_txt = Path(args[1] if len(args) > 1 else "src/timing/words.txt").read_text(encoding="utf-8")

ev = []  # (t, id, on)
for m in re.finditer(r"tl\.set\(q\('((?:[^']*-)?m-[^']*)'\), \{ opacity: ([01]) \}, ([0-9.]+)\)", html):  # q('m-<pose>-<mouth>')
    ev.append((float(m.group(3)), m.group(1), m.group(2) == "1"))
ev.sort()
if not ev:
    sys.exit("no mouth-patch events in the presenter - is mouth-fit.json in assets/mascot/?")


def shown(t):
    on = set()
    for et, i, o in ev:
        if et > t:
            break
        (on.add if o else on.discard)(i)
    return [i.rsplit("-", 1)[-1] for i in on]


words = [(w, float(t)) for w, t in re.findall(r"(\S+)@([0-9.]+)", words_txt)]
TALK = {"open", "wide", "round", "small", "fv"}
hits = 0
for k, (w, t) in enumerate(words):
    nxt = words[k + 1][1] if k + 1 < len(words) else t + 0.4
    mid = t + min(0.35, (nxt - t)) / 2
    if TALK & set(shown(mid)):
        hits += 1
wav = "assets/audio/vo-master.wav" if Path("assets/audio/vo-master.wav").exists() else "assets/audio/vo.mp3"
log = subprocess.run(["ffmpeg", "-hide_banner", "-i", wav, "-af", f"silencedetect=noise={DB}dB:d=0.3", "-f", "null", "-"],
                     capture_output=True, text=True).stderr
st = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", log)]
en = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", log)]
sil = [(a, b) for a, b in zip(st, en) if b - a >= 0.3]
rest = sum(1 for a, b in sil if not (TALK & set(shown((a + b) / 2))))
print(f"words: {hits}/{len(words)} with a talking mouth ({100 * hits / max(1, len(words)):.1f}%)")
print(f"silences: {rest}/{len(sil)} at rest ({100 * rest / max(1, len(sil)):.1f}%)")
