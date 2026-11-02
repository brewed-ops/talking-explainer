"""List the real pauses in a take and the word that follows each one - pick scene cuts from this list.

usage (film root): <py> <skill>/scripts/find-cuts.py [assets/audio/vo.mp3] [src/timing/words.txt] [--min 0.25] [--db -40]

Whisper word times drift by up to ~0.4s around pauses (seen in practice: a word stamped at 81.06 sat inside a silence that
really ran 81.07-81.51), so cut in the MIDDLE of a measured silence, never at a word time. Each line prints the
silence, its length, the suggested cut (midpoint) and the first word after it; a paragraph start = a scene cut.
words.txt is the output of explainer-kit/scripts/words.py (one segment per line, "word@time").
"""
import re
import subprocess
import sys
from pathlib import Path

opts = dict(zip(sys.argv[1::1], sys.argv[2::1]))
args = [a for i, a in enumerate(sys.argv[1:], 1) if not a.startswith("--") and not sys.argv[i - 1].startswith("--")]
mp3 = args[0] if args else "assets/audio/vo.mp3"
words_txt = args[1] if len(args) > 1 else "src/timing/words.txt"
min_len = float(opts.get("--min", 0.25))
db = opts.get("--db", "-40")

out = subprocess.run(["ffmpeg", "-hide_banner", "-i", mp3, "-af", f"silencedetect=n={db}dB:d={min_len}", "-f", "null", "-"],
                     capture_output=True, text=True).stderr
starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", out)]
ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", out)]
words = []
if Path(words_txt).exists():
    for line in Path(words_txt).read_text(encoding="utf-8").splitlines():
        for w, t in re.findall(r"(\S+)@([\d.]+)", line):
            words.append((float(t), w))
else:  # no words.txt (words.py prints to stdout) - read the transcribe.py json directly
    import json
    for seg in json.loads(Path("src/timing/vo-words.json").read_text(encoding="utf-8")):
        words += [(w["s"], w["w"].strip()) for w in seg["words"]]
words.sort()
for s, e in zip(starts, ends):
    nxt = next((f"{w}@{t:.2f}" for t, w in words if t >= s - 0.05), "(end)")
    print(f"{s:8.2f}-{e:8.2f} ({e - s:.2f})  cut {(s + e) / 2:8.2f}  -> {nxt}")
