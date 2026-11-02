"""Pull a desktop app's REAL theme tokens (CSS custom properties) out of its stylesheet into a short sheet, so a
recreated app window looks like the app and not like a guess.

usage: <py> <skill>/scripts/app-tokens.py <app.css> <out.md> [--scope "body" --scope ".theme-dark"] [--grep background,text,accent]
  Electron apps (Obsidian, VS Code, Slack, Discord, Notion desktop...) ship their CSS inside an asar archive:
    npx @electron/asar list <app>.asar | grep -i "\\.css$"          (find the main stylesheet)
    npx @electron/asar extract-file <app>.asar app.css            (writes it to the current folder)
  Obsidian: <install>/resources/obsidian.asar (or obsidian-<version>.asar in the user's app data), file app.css,
  scopes "body" + ".theme-dark". Default --grep keeps colours, fonts and sizes; --grep all keeps every token.
"""
import argparse, re
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("css"); ap.add_argument("out")
ap.add_argument("--scope", action="append", default=[])
ap.add_argument("--grep", default="background,text,accent,color,font,size,border,interactive,icon,nav,tab,graph,link,tag")
a = ap.parse_args()
css = Path(a.css).read_text(encoding="utf-8", errors="replace")
scopes = a.scope or ["body", ":root", ".theme-dark", ".theme-light"]
keys = None if a.grep == "all" else a.grep.split(",")
out = [f"# Real theme tokens from {Path(a.css).name}", ""]
for scope in scopes:
    blocks = re.findall(r"(?:^|\})\s*" + re.escape(scope) + r"\s*\{([^{}]*)\}", css)
    if not blocks:
        continue
    seen = {}
    for blk in blocks:  # later blocks win, like the cascade
        for k, v in re.findall(r"(--[\w-]+)\s*:\s*([^;]+);", blk):
            if keys is None or any(w in k for w in keys):
                seen[k] = " ".join(v.split())
    out += [f"## {scope}  ({len(seen)} tokens)"] + [f"{k}: {v}" for k, v in seen.items()] + [""]
Path(a.out).write_text("\n".join(out), encoding="utf-8")
print(f"{a.out}: {sum(1 for l in out if l.startswith('--'))} tokens from {len([l for l in out if l.startswith('## ')])} scope(s)")
