"""STORYBOARD.src.md (cue words marked @g<GLOBAL seconds>) -> STORYBOARD.md (cues as @<scene-local seconds>).

Each "## Frame" block carries "- start: <global>"; every @gX.XX inside it becomes @L.LL = X - start. Also prints
the scene list (id, duration) for src/set-film.py and checks that starts chain (start + duration = next start).
"""
import re
from pathlib import Path

src = Path("STORYBOARD.src.md").read_text(encoding="utf-8")
parts = re.split(r"(?m)^(?=## Frame )", src)
out, scenes, prev_end = [parts[0]], [], None
for p in parts[1:]:
    start = float(re.search(r"(?m)^- start: ([\d.]+)", p).group(1))
    dur = float(re.search(r"(?m)^- duration: ([\d.]+)s", p).group(1))
    sid = re.search(r"compositions/(s\d+-[\w-]+)\.html", p).group(1)
    if prev_end is not None and abs(prev_end - start) > 0.001:
        raise SystemExit(f"{sid}: start {start} != previous end {prev_end}")
    prev_end = round(start + dur, 3)
    def loc(m):
        t = round(float(m.group(1)) - start, 2)
        if t < 0 or t > dur:
            raise SystemExit(f"{sid}: cue {m.group(1)} outside 0..{dur}")
        return f"@{t:.2f}"
    p = re.sub(r"@g(\d+(?:\.\d+)?)", loc, p)
    # bare global times (ZOOM ranges "87.4-88.9", "Exit by 92.67", "back by ...") -> local; a decimal is a time
    # when it falls inside this scene's global window (scales/confidences like 1.06 / 0.75 sit below any start > 0)
    if start > 0:
        def bare(m):
            v = float(m.group(1))
            return f"{v - start:.2f}" if start - 0.001 <= v <= start + dur + 0.01 else m.group(1)
        lines = p.split("\n")
        p = "\n".join(l if l.startswith(("- start:", "- duration:")) else re.sub(r"(?<![@\d.])(\d{1,3}\.\d{1,2})(?![\d])", bare, l)
                      for l in lines)
    p = re.sub(r"(?m)^- start: ([\d.]+)", r"- global start: \1", p)
    out.append(p)
    scenes.append((sid, dur))
Path("STORYBOARD.md").write_text("".join(out), encoding="utf-8")
print("STORYBOARD.md written,", len(scenes), "frames, total", prev_end)
print(scenes)
