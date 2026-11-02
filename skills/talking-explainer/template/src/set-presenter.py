"""Write the poses + fx of src/presenter-track.json. GLOBAL seconds = the cue word's start minus ~0.1s.
Keeps scale/home/enter/bob/blink/mouth from the scaffolded track. Only use poses the mascot has
(assets/mascot/manifest.json). Talking poses = the ones in assets/mascot/mouth-fit.json (the demo: idle, point,
present, thumbs-up, wave, celebrate, sit). think/walk have NO mouths - never while the voice talks (use fx/question
for a thinking beat instead). Change pose every ~2-4s on a word that earns it: point/present when something on the
stage is named, thumbs-up on a win, wave on hello/goodbye, idle between.
usage (film root): <py> src/set-presenter.py"""
import json
from pathlib import Path

# worked example (REA, first 20 seconds) - replace with this film's poses
P = [(0.0, "present"), (3.8, "idle"), (4.7, "wave"), (6.6, "present"), (8.0, "idle"), (9.0, "point"),
     (10.6, "present"), (12.9, "idle"), (14.3, "point"), (15.9, "present"), (17.8, "idle"), (18.4, "present")]
FX = [{"sprite": "fx/question", "at": 3.85, "out": 4.75, "dx": 170, "dy": -650, "scale": 0.16},
      {"sprite": "fx/sparkle-burst", "at": 37.2, "out": 38.4, "dx": 200, "dy": -620, "scale": 0.17}]

p = Path("src/presenter-track.json")
tr = json.loads(p.read_text(encoding="utf-8"))
have = {k.split("/", 1)[1] for k in json.loads(Path("assets/mascot/manifest.json").read_text(encoding="utf-8")) if k.startswith("poses/")}
talk = set(json.loads(Path("assets/mascot/mouth-fit.json").read_text(encoding="utf-8"))) if Path("assets/mascot/mouth-fit.json").exists() else set()
assert all(a[0] < b[0] for a, b in zip(P, P[1:])), "poses out of order"
assert {n for _, n in P} <= have, f"unknown poses: {sorted({n for _, n in P} - have)}"
silent = sorted({n for _, n in P} - talk) if talk else []
if silent: print("note: no mouths on", silent, "- keep them off spoken lines")
tr["_doc"] = ("Presenter track for compositions/m-presenter.html (spatial-film/scripts/build-presenter.py). Written by "
              "src/set-presenter.py - edit there. GLOBAL seconds = cue word minus ~0.1s.")
tr["poses"] = [[t, n] for t, n in P]
tr["fx"] = FX
p.write_text(json.dumps(tr, indent=2), encoding="utf-8")
print(len(P), "poses,", len(FX), "fx")
