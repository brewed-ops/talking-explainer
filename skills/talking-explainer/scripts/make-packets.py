"""Write .hyperframes/frame-packets/<id>.md (one per STORYBOARD.md block) + the worker role _role.md.
Stand-in for general-video/scripts/frame-packets.mjs, which fails on current HyperFrames skills ("frame packets: ENOENT",
its frame-worker-core.md moved). The role defaults to <skill>/references/frame-role.md.
usage (film root, after storyboard-local.py + split-headers.py):
  <py> <skill>/scripts/make-packets.py [role.md]"""
import re
import shutil
import sys
from pathlib import Path

root = Path.cwd()
role = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "references/frame-role.md"
rules = Path.home() / ".claude/skills/hyperframes-animation/rules"
out = root / ".hyperframes/frame-packets"
out.mkdir(parents=True, exist_ok=True)
shutil.copy(role, out / "_role.md")
sb = (root / "STORYBOARD.md").read_text(encoding="utf-8")
blocks = re.split(r"(?m)^(?=## Frame \d+)", sb)[1:]
if not blocks:
    sys.exit("no '## Frame <n>' blocks in STORYBOARD.md - run src/storyboard-local.py first")
head = ("# Frame packet: {id}\n\n## Project inputs\n\n- Project: {proj}\n- Design truth: {frame}\n"
        "- RULES_DIR: {rules}\n\n## Assigned storyboard block\n\n")
for b in blocks:
    m = re.search(r"- src: compositions/([\w-]+)\.html", b)
    if not m:
        sys.exit("a block has no '- src: compositions/<id>.html' line - run src/split-headers.py")
    fid = m.group(1)
    (out / f"{fid}.md").write_text(head.format(id=fid, proj=root, frame=root / "frame.md", rules=rules) + b.rstrip() + "\n",
                                   encoding="utf-8")
    print(fid, len(b.splitlines()), "lines")
if not rules.exists():
    print(f"note: {rules} not found - run: npx hyperframes skills update general-video hyperframes-animation media-use")
