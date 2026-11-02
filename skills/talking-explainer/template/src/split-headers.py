"""Split the storyboard's compact '- duration: X | poster: Y | ...' lines into one bullet per field (frame-packets.mjs needs that)."""
from pathlib import Path

p = Path("STORYBOARD.md")
out = []
for line in p.read_text(encoding="utf-8").splitlines():
    if line.startswith("- duration:") and " | " in line:
        out += ["- " + part.strip() for part in line[2:].split(" | ")]
    else:
        out.append(line)
p.write_text("\n".join(out) + "\n", encoding="utf-8")
print("split")
