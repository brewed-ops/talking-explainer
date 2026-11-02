"""Turn Unicode Block Element art (a mascot drawn in U+2580-U+259F, e.g. Clawd) into a pixel bitmap.

usage: py -3.12 blocks_to_sprite.py <poses.json> <out_dir> [--cell 12x22] [--color #D97757] [--eye #1A1410]

poses.json = {"color": "#D97757", "poses": {"default": [" ▐▛███▜▌", "▝▜█████▛▘", "  ▘▘ ▝▝"], ...}}
Each character is a 2x2 quadrant cell. Rows are centred like the terminal draws them (a row one char shorter
shifts half a char = one quadrant column). Writes <out_dir>/<pose>.png (crisp, transparent, eyes filled dark)
and <out_dir>/bitmap.json ({pose: [[0/1/2,...], ...]} with 1 = body, 2 = eye) for voxel builds in Three.js.
--cell WxH = pixels per quadrant; terminal glyphs are ~1:1.8, so 12x22 keeps the real proportions.
"""
import sys, json
from pathlib import Path
from PIL import Image

# quadrant bits per glyph: (TL, TR, BL, BR)
Q = {
    " ": (0, 0, 0, 0), "█": (1, 1, 1, 1), "▀": (1, 1, 0, 0), "▄": (0, 0, 1, 1), "▌": (1, 0, 1, 0), "▐": (0, 1, 0, 1),
    "▘": (1, 0, 0, 0), "▝": (0, 1, 0, 0), "▖": (0, 0, 1, 0), "▗": (0, 0, 0, 1),
    "▛": (1, 1, 1, 0), "▜": (1, 1, 0, 1), "▙": (1, 0, 1, 1), "▟": (0, 1, 1, 1), "▚": (1, 0, 0, 1), "▞": (0, 1, 1, 0),
}


def to_bitmap(rows):
    width = max(len(r) for r in rows)
    grid = []
    for r in rows:
        off = width - len(r)  # centred: shift by half the missing chars, in quadrant columns
        line_t, line_b = [0] * (width * 2), [0] * (width * 2)
        for i, ch in enumerate(r):
            if ch not in Q:
                raise SystemExit(f"glyph {ch!r} (U+{ord(ch):04X}) is not a Block Element quadrant")
            tl, tr, bl, br = Q[ch]
            x = i * 2 + off
            line_t[x], line_t[x + 1], line_b[x], line_b[x + 1] = tl, tr, bl, br
        grid += [line_t, line_b]
    # eyes = empty cells walled in left and right inside a body row
    for row in grid:
        filled = [x for x, v in enumerate(row) if v]
        if filled:
            for x in range(filled[0], filled[-1] + 1):
                if not row[x] and any(row[:x]) and any(row[x + 1:]) and sum(row) >= len(row) // 2:
                    row[x] = 2
    return grid


def main():
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    cw, ch = (int(v) for v in (sys.argv[sys.argv.index("--cell") + 1] if "--cell" in sys.argv else "12x22").split("x"))
    data = json.loads(src.read_text(encoding="utf-8"))
    color = sys.argv[sys.argv.index("--color") + 1] if "--color" in sys.argv else data.get("color", "#D97757")
    eye = sys.argv[sys.argv.index("--eye") + 1] if "--eye" in sys.argv else "#1A1410"
    hexrgb = lambda h: tuple(int(h.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)) + (255,)
    out.mkdir(parents=True, exist_ok=True)
    maps = {}
    for name, rows in data["poses"].items():
        g = to_bitmap(rows)
        maps[name] = g
        im = Image.new("RGBA", (len(g[0]) * cw, len(g) * ch), (0, 0, 0, 0))
        for y, row in enumerate(g):
            for x, v in enumerate(row):
                if v:
                    im.paste(hexrgb(color if v == 1 else eye), (x * cw, y * ch, (x + 1) * cw, (y + 1) * ch))
        im.save(out / f"{name}.png")
        print(name, f"{len(g[0])}x{len(g)} cells ->", out / f"{name}.png")
    (out / "bitmap.json").write_text(json.dumps(maps), encoding="utf-8")


if __name__ == "__main__":
    main()
