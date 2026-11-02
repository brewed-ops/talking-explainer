"""Write a paste-ready Solar icon sheet (inline SVG, colour = currentColor) for scene workers.

Icon set for these films = Solar (480 Design), https://solar-icons.vercel.app/icons.
Package @solar-icons/static (MIT code); the ARTWORK is CC BY 4.0 - every published video credits it in the
description: "Icons: Solar by 480 Design (CC BY 4.0)".
usage: <py> <skill>/scripts/solar-snippets.py <out.html> [--styles bold-duotone,linear] [name ...]
  Fetches @solar-icons/static with `npm pack` into a temp dir (no install). No names = the default explainer set.
  Unknown names are listed, never guessed - browse `dist/icons/linear/*.svg` names or the site for others.
Styles: bold-duotone = hero icons (step cards, chips, badges, the lens glyph) - the Apple-like two-tone; set the
second tone with `--solar-secondary-color` / `--solar-secondary-opacity` (default currentColor at 0.5).
linear = UI chrome (search fields, window rows, small marks), stroke 1.5 on a 24 grid - fine >= 40px.
"""
import argparse, pathlib, re, subprocess, tarfile, tempfile

DEFAULT = ["magnifier", "minimalistic-magnifier", "check-circle", "close-circle", "graph-up", "star",
           "lock-keyhole-minimalistic", "lock-keyhole-minimalistic-unlocked", "cup-hot", "wind", "eye",
           "chat-round-dots", "file-search", "card-search", "widget-add", "sledgehammer", "book-minimalistic",
           "copy", "calendar", "stopwatch", "window-frame", "programming", "code", "arrow-right", "danger-triangle",
           "shop", "users-group-rounded", "cpu", "shield-check", "hand-shake", "star-shine", "magnifier-bug"]

ap = argparse.ArgumentParser()
ap.add_argument("out"); ap.add_argument("names", nargs="*")
ap.add_argument("--styles", default="bold-duotone,linear")
a = ap.parse_args()
names, styles = a.names or DEFAULT, a.styles.split(",")

tmp = pathlib.Path(tempfile.mkdtemp())
subprocess.run("npm pack @solar-icons/static", cwd=tmp, shell=True, check=True, capture_output=True)
tgz = next(tmp.glob("solar-icons-static-*.tgz"))
with tarfile.open(tgz) as t:
    t.extractall(tmp, filter="data")
icons = tmp / "package" / "dist" / "icons"

rows, missing = [], []
for style in styles:
    rows.append(f"\n<!-- ===================== {style} ===================== -->")
    for n in names:
        f = icons / style / f"{n}.svg"
        if not f.exists():
            missing.append(f"{style}/{n}"); continue
        svg = f.read_text(encoding="utf-8").strip()
        svg = re.sub(r'\s(width|height)="24"', "", svg, count=2)
        svg = re.sub(r'class="[^"]*"', f'class="solar" width="64" height="64" aria-hidden="true"', svg, count=1)
        rows.append(f"<!-- {n} ({style}) -->\n{svg}")

ver = tgz.stem.split("-")[-1]
head = (f"<!-- Solar icons (480 Design, artwork CC BY 4.0 - credit it in the video description), "
        f"@solar-icons/static {ver}. Copy the <svg> inline; size with width/height, colour with `color:`. "
        "bold-duotone for hero icons, linear for UI chrome. Never Lucide/Phosphor in this film. -->")
pathlib.Path(a.out).write_text(head + "\n".join(rows) + "\n", encoding="utf-8")
print(f"{a.out}: {len(rows) - len(styles)} icons ({', '.join(styles)})" + (f"; NOT FOUND: {', '.join(missing)}" if missing else ""))
