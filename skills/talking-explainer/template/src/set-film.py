"""Write the scene list + audio length into film.json. Cuts sit in the sentence pauses of src/timing/vo-words.json;
the scene durations add up to voice end + ~2.8s (the held end card). storyboard-local.py prints the list for you.
Cues (SFX) are set separately by src/set-cues.py. Edit the values below per film - they hold the worked example (REA).
usage (film root): <py> src/set-film.py"""
import json
from pathlib import Path

SCENES = [
    ["s01-hook", 7.9], ["s02-trending", 10.4], ["s03-cafe", 9.95], ["s04-taste", 10.3], ["s05-short", 10.1],
    ["s06-rea", 12.8], ["s07-flow", 11.75], ["s08-notes", 12.3], ["s09-minutes", 9.4], ["s10-line", 15.4],
    ["s11-yours", 9.75], ["s12-close", 8.95],
]
VOICE = 126.43  # ffprobe length of assets/audio/vo.mp3

p = Path("film.json")
f = json.loads(p.read_text(encoding="utf-8"))
f["scenes"] = SCENES
f["audio"][0]["dur"] = VOICE
f["ground"] = "#F5F5F7"
p.write_text(json.dumps(f, indent=2), encoding="utf-8")
t, starts = 0.0, []
for s, d in f["scenes"]:
    starts.append(f"{s} {t:.2f}"); t += d
print("total", round(t, 2), f"(voice {VOICE} + {t - VOICE:.2f}s end hold)")
print(" | ".join(starts))
