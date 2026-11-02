"""Fork a finished 16:9 talking explainer into a 1080x1920 portrait (TikTok / Reels / Shorts) project.

usage (any cwd): <py> <skill>/scripts/port-portrait.py <src film dir> <new film dir>
  e.g. port-portrait.py ~/TalkingExplainer/films/rea ~/TalkingExplainer/films/rea-9x16

Copies the source/audio (no renders, snapshots, harness output or work dirs), moves the shipped 16:9 scenes to
references/src-16x9/ (the workers' spec), rewrites the contract for portrait (frame.md layout = TikTok zones,
worker brief "port, don't reinvent", scene-starter 1080x1920, set-film.py width/height/name), moves the presenter
bottom-left (scale x0.9, feet y 1640) and points every project path at the new folder. Then, from the new film
root: src/set-film.py, build-presenter.py, build-brand.py (vertical = top centre at y 150), make-harness.py - and
dispatch the port workers (SKILL.md "Portrait / TikTok cut"). The 16:9 film is never touched.
"""
import json, re, shutil, sys
from pathlib import Path

src, dst = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
ref = dst / "references/src-16x9"
# resume: an earlier run copied + moved the scenes, then died on a contract patch
resume = dst.exists() and ref.exists() and not list((dst / "compositions").glob("s*.html"))
if dst.exists() and not resume:
    sys.exit(f"{dst} exists - pick a new folder")
if not (src / "film.json").exists():
    sys.exit(f"{src} has no film.json - point at a finished film's root")


def sub1(path, pairs):
    """Each film words its contract a little differently: apply what matches, list what did not (port those by hand)."""
    p = Path(path)
    if not p.exists():
        print(f"  skip {p.name}: missing"); return
    t = p.read_text(encoding="utf-8")
    for old, new in pairs:
        if t.count(old) == 1:
            t = t.replace(old, new)
        else:
            print(f"  {p.name}: phrase not found, rewrite by hand -> {old[:70]!r}")
    p.write_text(t, encoding="utf-8")


if resume:
    print(f"{dst}: resuming - copy + scene move already done")
else:
    skip = shutil.ignore_patterns("renders", "snapshots", "test", "work", "node_modules", ".media")
    shutil.copytree(src, dst, ignore=skip)
    ref.mkdir(parents=True)
    for f in list((dst / "compositions").glob("s*.html")) + list((dst / "compositions").glob("s*.motion.json")):
        shutil.move(str(f), ref / f.name)

# every project path and the film's name follow the new folder (case-insensitive: Windows resolve() may return
# a lower-case folder name for one the scaffold wrote in mixed case)
fwd = lambda p: str(p).replace("\\", "/")
src_rx = re.compile(re.escape(fwd(src)), re.I if sys.platform == "win32" else 0)
for f in dst.rglob("*"):
    if f.is_file() and f.suffix in (".md", ".html", ".json", ".py") and not any(
            part in ("assets", ".hyperframes", "src-16x9", "node_modules") for part in f.relative_to(dst).parts):
        t = f.read_text(encoding="utf-8")
        u = src_rx.sub(lambda m: fwd(dst), t)
        if f.name in ("meta.json", "package.json"):
            u = u.replace(f'"{src.name}"', f'"{dst.name}"')
        if u != t:
            f.write_text(u, encoding="utf-8")

NEW_LAYOUT = """## Layout - PORTRAIT frame zones for TikTok (frame px, 1080x1920; world x/y = frame px minus 540/960 at z 0)

TikTok (and Reels / Shorts) draws its own UI over the video - nothing that matters may sit under it:
- **Top** y < 150 (Following / For You tabs, search) - empty.
- **Right rail** x > 930, y 680-1540 (avatar, like, comment, save, share) - no text, no key detail there; a window
  edge or a soft shadow may pass under it.
- **Bottom** y > 1540 (username, caption, sound, progress bar) - empty (only the presenter's legs).

Zones:
- **Logo** x 380-700, y 150-240: the corner logo overlay (`m-brand`, top centre). Keep it clear.
- **Top band** x 70-1010, y 260-500: the scene's headline, centred on x 540, max 2 lines at 84px (3 at 60px).
  Put the headline in its own 2D layer ABOVE the camera rig (outside `#<id>-stage`, track index 2) so pushes never
  move or crop it. Where the 16:9 headline was one long line, wrap it at a natural phrase break.
- **Stage** x 60-1020, y 520-1060 (below y 680 keep text and key details at x <= 920): the main objects, full width.
- **Lower right** x 580-920, y 1080-1520: secondary objects (a chip, a badge, a small card, a counter, the beat's
  evidence). Use it - it is the right half of the presenter's row and keeps the frame full.
- **Presenter zone** x 20-560, y 1060-1660: the lip-synced presenter overlay (`compositions/m-presenter.html`, not
  yours), feet at y 1640 (a HALF-BODY presenter sits waist-on-bottom-edge and bigger: MEASURE its box with
  `test-scene.sh m-presenter` and rewrite this line - e.g. x 0-680, y 1220-1920). Never put scene content there - at ANY time, including the peak of a camera push - and
  never draw a mascot or a person. The presenter presents UP and to the RIGHT: the thing named sits around frame
  x 560-920, y 700-1100 at its cue.
- Title / lockup scenes (the open, the end card) may use the whole frame from y 250 to 1060 plus the lower right,
  but still never the presenter zone, the logo zone or the platform UI lines.

**Porting from 16:9:** the 16:9 stage was 1220x820 to the right of the presenter; the portrait stage is 960x540
above it plus the 340x440 lower right. Re-stack side-by-side layouts vertically (A above B), turn 3-across rows
into 2 + 1 or a column, cut dead space before cutting type size. Windows: ~860-940 wide, ~480-540 tall in the
stage. A diagram that ran left -> right may run top -> bottom when it reads better. A camera push goes toward the
named object and keeps it inside the stage - pushes are smaller here (z +80..+140); a secondary object a push would
drag past the platform lines recedes/dims during that push.

"""
fm = dst / "frame.md"
t = fm.read_text(encoding="utf-8")
a = t.index("## Layout - landscape frame zones")
b = t.index("## Assets", a)  # the heading's tail differs per film ("(reference them", "(ROOT-RELATIVE", ...)
fm.write_text(t[:a] + NEW_LAYOUT + t[b:], encoding="utf-8")
sub1(fm, [
    ("1920x1080 LANDSCAPE (16:9), rendered at **60fps**,", "1080x1920 PORTRAIT (9:16) for TikTok, rendered at **60fps**,"),
    ("LEFT third; the", "BOTTOM-LEFT; the"),
    ("**The look is Apple:**",
     f"**This film is the PORTRAIT PORT of `{src.name}` (16:9, shipped).** Each scene's source is\n"
     "`references/src-16x9/<id>.html`: same copy, same beats, same cue times, same colours, same icons, same emphasis,\n"
     "same seam poses. Only the layout, sizes, positions and camera vectors change for the portrait zones below.\n"
     "**The look is Apple:**"),
    ("with a matching x/y so the object moves toward frame centre-right (NEVER left of x 640),",
     "with a matching x/y so the object moves toward the stage centre (NEVER into the presenter zone or past the platform lines),"),
    ("Main objects fill the STAGE (x 640-1860, y 200-1020) - use its\nfull width and height, never a small cluster in the middle.",
     "Main objects fill the STAGE (x 60-1020, y 520-1060) - use its\nfull width, never a small cluster in the middle. Body text >= 40px on the phone frame."),
    ("World x/y 0 = frame centre (960, 540).", "World x/y 0 = frame centre (540, 960)."),
])
sub1(dst / "references/worker-brief.md", [
    ("(1920x1080 landscape, narrated, Apple look)",
     "(1080x1920 PORTRAIT for TikTok, narrated, Apple look - a port of the shipped 16:9 film)"),
    ("Canvas 1920x1080 (LANDSCAPE 16:9), rendered at 60fps.", "Canvas 1080x1920 (PORTRAIT 9:16, TikTok), rendered at 60fps."),
    ("(compositions/m-presenter.html, LEFT third)", "(compositions/m-presenter.html, BOTTOM-LEFT)"),
    ("corner logo (m-brand, top-right) - not yours, keep out of their zones (frame.md Layout).",
     "logo (m-brand, top centre) - not yours, keep out of their zones. The platform's own UI covers the top, the right rail and the bottom (frame.md Layout)."),
    ("2. **No captions, landscape zones:** obey frame.md \"Layout - landscape frame zones\"; keep film labels 60px+ from edges.",
     "2. **No captions, portrait zones:** obey frame.md \"Layout - PORTRAIT frame zones for TikTok\"; keep film labels 60px+ from edges.\n"
     "   **Port, don't reinvent:** start from `references/src-16x9/<scene_id>.html` (the shipped 16:9 scene - copy it\n"
     "   to compositions/ and adapt). Keep its copy, beats, cue times, colours, icons, emphasis and seam poses exactly;\n"
     "   change only #root / data-width / data-height to 1080x1920 and re-author layout, sizes, positions and camera vectors."),
    ("- **Faithful copy:** on-screen words exactly as the storyboard block quotes them (basic English).",
     "- **Faithful copy:** on-screen words exactly as the 16:9 source scene shows them (basic English)."),
])
sub1(dst / "references/scene-starter.html", [
    ("Scene starter (1920x1080,", "Scene starter (1080x1920 portrait,"),
    ("width: 1920px; height: 1080px;", "width: 1080px; height: 1920px;"),
    ('data-width="1920" data-height="1080"', 'data-width="1080" data-height="1920"'),
])
sub1(dst / "src/set-film.py", [
    ('f["ground"] = "#F5F5F7"',
     f'f["ground"] = "#F5F5F7"\nf["width"], f["height"], f["name"] = 1080, 1920, "{dst.name}"  # portrait port of {src.name}'),
])
p = dst / "src/presenter-track.json"
tr = json.loads(p.read_text(encoding="utf-8"))
tr["_doc"] = "PORTRAIT 1080x1920, bottom-left, feet y 1640. " + tr.get("_doc", "")
src_h = json.loads((src / "film.json").read_text(encoding="utf-8")).get("height", 1080)
half = tr.get("home", {}).get("feet", 0) >= src_h  # sprite bottom pushed below the frame = a half-body cut
k = 1.243 if half else 0.9  # half body: x1.3 put the hair over stage cards at y ~1170
tr["scale"] = round(tr["scale"] * k, 3)
# full body: feet y 1640, above the platform caption line. HALF BODY: the waist cut must sit on the frame's bottom
# edge as in 16:9 - at 1640 the cut edge floats mid-frame. Bigger so the face carries the phone frame; the
# platform captions then pass over the torso, never the face.
tr["home"] = {"x": 300 if half else 270, "feet": 1990 if half else 1640}  # half body: hair top ~1270 in the tallest pose + pop
# measure on the RENDER (or every pose + its pop), not one pose still: a single still read 70 px low
for fx in tr.get("fx", []):
    fx["dx"], fx["dy"], fx["scale"] = round(fx["dx"] * k), round(fx["dy"] * k), round(fx["scale"] * k, 3)
print(f"presenter: {'HALF body, waist on the bottom edge' if half else 'full body'}, scale {tr['scale']}, home {tr['home']}"
      " - measure its real box with test-scene.sh m-presenter and write it into frame.md's Presenter zone line")
p.write_text(json.dumps(tr, indent=2), encoding="utf-8")
print(f"{dst}: portrait contract written, {len(list(ref.glob('s*.html')))} 16:9 scenes in references/src-16x9/")
