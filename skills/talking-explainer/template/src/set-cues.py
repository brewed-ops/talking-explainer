"""SFX cue sheet - written in GLOBAL seconds on the storyboard's cue words, converted to scene-local here (scene
starts from film.json, so run src/set-film.py first). Apple restraint: quiet (0.1-0.3), only on causal moments -
pop on arrivals, whoosh on push-ins, ping on counters/checks, click on UI presses, impact on the red moments.
Sound names = keys of film.json "sfx". usage (film root): <py> src/set-cues.py"""
import json
from pathlib import Path

# worked example (REA, first two scenes) - replace with this film's cues: scene -> [(global s, sound, volume)]
G = {
    "s01-hook": [(0.3, "pop", 0.16), (2.32, "whoosh", 0.08), (4.9, "pop", 0.2)],
    "s02-trending": [(8.2, "pop", 0.18), (11.4, "ping", 0.2), (15.6, "ping", 0.16)],
}

p = Path("film.json")
f = json.loads(p.read_text(encoding="utf-8"))
start, t = {}, 0.0
for s, d in f["scenes"]:
    start[s] = t; t += d
assert set(G) <= set(start), f"scenes not in film.json: {set(G) - set(start)}"
cues = []
for s, cs in G.items():
    for g, sfx, vol in cs:
        loc = round(g - start[s], 2)
        assert 0 <= loc <= dict(f["scenes"])[s], f"{s}: cue at global {g} falls outside the scene"
        cues.append([s, loc, sfx, vol])
f["cues"] = cues
p.write_text(json.dumps(f, indent=2), encoding="utf-8")
missing = [v[0] for v in f.get("sfx", {}).values()
           if not Path("assets/audio/sfx", v[0]).exists() and not Path("assets/audio", v[0]).exists()]
print(len(cues), "cues; missing sfx files:", missing)
