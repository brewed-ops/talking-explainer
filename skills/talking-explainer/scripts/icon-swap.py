"""Swap every inline Solar icon in a film's scenes for Phosphor (or a real logo <img>), keeping size/colour/class.

usage: <py> <skill>/scripts/icon-swap.py <film_dir> [--map map.json] [--dry]
For a film that must use Phosphor icons and REAL file-type logos (PDF, XLSX ...). Scenes hold Solar icons
as inline <svg> with no name, so each one is identified by its path data against references/icons-solar.html +
snippets.html; icons fetched outside that sheet are matched by the LABEL right after them (map key "label:<text>").
Map values: "<phosphor-name>" (weight follows the Solar style: bold-duotone -> duotone, linear -> regular,
bold -> fill), "<name>:<weight>", or "img:assets/logos/<file>" for a real file/brand logo.
Phosphor = @phosphor-icons/core 2.1.1 assets, cached in ~/.cache/phosphor/assets (npm pack it once if missing).
Anything unmatched is listed, never guessed. Edits compositions/s*.html in place (backup once in .hyperframes/work/).
"""
import json, re, shutil, subprocess, sys, tarfile, tempfile
from pathlib import Path

film = Path(sys.argv[1])
DRY = "--dry" in sys.argv
PH = Path.home() / ".cache/phosphor/assets"
if not PH.exists():
    tmp = Path(tempfile.mkdtemp())
    subprocess.run("npm pack @phosphor-icons/core@2.1.1", cwd=tmp, shell=True, check=True, capture_output=True)
    with tarfile.open(next(tmp.glob("*.tgz"))) as t:
        t.extractall(tmp)
    shutil.copytree(tmp / "package/assets", PH)

SOLAR_TO_PH = {"magnifier": "magnifying-glass", "minimalistic-magnifier": "magnifying-glass", "check-circle": "check-circle",
               "close-circle": "x-circle", "graph-up": "chart-line-up", "star": "star", "lock-keyhole-minimalistic": "lock-simple",
               "lock-keyhole-minimalistic-unlocked": "lock-simple-open", "cup-hot": "coffee", "wind": "wind", "eye": "eye",
               "chat-round-dots": "chat-circle-dots", "file-search": "file-magnifying-glass", "card-search": "magnifying-glass",
               "widget-add": "squares-four", "sledgehammer": "hammer", "book-minimalistic": "book", "copy": "copy",
               "calendar": "calendar-blank", "stopwatch": "timer", "window-frame": "browser", "programming": "code",
               "code": "code", "arrow-right": "arrow-right", "danger-triangle": "warning", "shop": "storefront",
               "users-group-rounded": "users-three", "cpu": "cpu", "shield-check": "shield-check", "hand-shake": "handshake",
               "star-shine": "sparkle", "magnifier-bug": "bug"}
WEIGHT = {"bold-duotone": "duotone", "linear": "regular", "bold": "fill", "outline": "regular", "broken": "regular"}
custom = json.loads(Path(sys.argv[sys.argv.index("--map") + 1]).read_text()) if "--map" in sys.argv else {}

lib = {}
for ref in ("references/icons-solar.html", "references/snippets.html"):
    p = film / ref
    if p.exists():
        for m in re.finditer(r"<!-- ([\w-]+) \(([\w-]+)\) -->\s*(<svg.*?</svg>)", p.read_text(encoding="utf-8"), re.S):
            lib.setdefault(tuple(re.findall(r' d="([^"]{0,60})', m.group(3))), (m.group(1), m.group(2)))


def phosphor(name, weight):
    f = PH / weight / (f"{name}.svg" if weight == "regular" else f"{name}-{weight}.svg")
    if not f.exists():
        raise SystemExit(f"no Phosphor icon {name} ({weight}) - check the name in {PH / weight}")
    return re.search(r"<svg[^>]*>(.*)</svg>", f.read_text(encoding="utf-8"), re.S).group(1).strip()


def keep_attrs(tag):
    """The outer <svg ...> attributes that carry size, colour, class, id, position - not the Solar geometry."""
    attrs = dict(re.findall(r'([\w:-]+)="([^"]*)"', tag))
    return {k: v for k, v in attrs.items() if k not in ("viewBox", "fill", "stroke-width", "xmlns")}


changed, missing = 0, []
for f in sorted((film / "compositions").glob("s*.html")):
    t = f.read_text(encoding="utf-8")
    out, pos, n = [], 0, 0
    for m in re.finditer(r"<svg\b[^>]*>.*?</svg>", t, re.S):
        svg = m.group(0)
        if svg.count("<svg") > 1:  # an unclosed <svg> upstream: the match ran to a later </svg> and swallowed a
            missing.append(f"{f.stem}: UNCLOSED <svg> before '{svg[:60]}' - fix by hand")  # whole screen (s06 2026-10-27)
            continue
        ds = tuple(re.findall(r' d="([^"]{0,60})', svg))
        if not ds:
            continue  # hand-drawn shapes (rings, bars, rules) - not icons
        hit = lib.get(ds) or next((v for k, v in lib.items() if k and k[0] == ds[0]), None)
        label = " ".join(re.sub(r"<[^>]+>", " ", t[m.end():m.end() + 300]).split())
        target, weight = None, None
        for k, v in custom.items():
            if k.startswith("label:") and label.startswith(k[6:]):
                target = v
                break
        if not target and hit:
            target = custom.get(hit[0], SOLAR_TO_PH.get(hit[0]))
            weight = WEIGHT.get(hit[1], "regular")
        if not target:
            if 'class="solar"' in svg or "solar-secondary" in svg or 'viewBox="0 0 24 24"' in svg:
                missing.append(f"{f.stem}: {ds[0][:24]} -> '{label[:40]}'")
            continue
        open_tag = re.match(r"<svg\b[^>]*>", svg).group(0)
        a = keep_attrs(open_tag)
        if target.startswith("img:"):
            style = a.get("style", "")
            w, h = a.get("width", "48"), a.get("height", "48")
            new = f'<img src="{target[4:]}" alt="" width="{w}" height="{h}" style="object-fit:contain;{style}"' + \
                  (f' class="{a["class"]}"' if "class" in a else "") + (f' id="{a["id"]}"' if "id" in a else "") + ">"
        else:
            name, _, w8 = target.partition(":")
            w8 = w8 or weight or ("duotone" if "solar-secondary" in svg else "regular")
            # inline fill: kit rules like `.kit-chip svg { fill:none; stroke:currentColor }` beat the fill ATTRIBUTE
            # and blanked every chip icon in a promo film - Solar survived only because it filled each path
            a["style"] = "fill:currentColor;stroke:none;" + a.get("style", "")
            attrs = " ".join(f'{k}="{v}"' for k, v in a.items())
            new = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" fill="currentColor" {attrs}>{phosphor(name, w8)}</svg>'
        out.append(t[pos:m.start()]); out.append(new); pos = m.end(); n += 1
    if n:
        out.append(t[pos:])
        if not DRY:
            bk = film / ".hyperframes/work/icon-swap-backup"
            bk.mkdir(parents=True, exist_ok=True)
            if not (bk / f.name).exists():
                shutil.copy2(f, bk / f.name)
            f.write_text("".join(out), encoding="utf-8")
        print(f"{f.stem:<12} {n} icons swapped")
        changed += n
print(f"total {changed} swapped{' (dry run)' if DRY else ''}")
if missing:
    print("UNMATCHED (add a label: entry to --map):", *missing, sep="\n  ")
