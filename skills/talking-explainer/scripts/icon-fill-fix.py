"""One-off repair for scenes swapped by icon-swap.py before its inline-fill fix: add fill:currentColor;stroke:none
to every Phosphor <svg> (viewBox 0 0 256 256) that lacks it.  usage: <py> <skill>/scripts/icon-fill-fix.py <scene.html> ...
"""
import re, sys

for p in sys.argv[1:]:
    t = open(p, encoding="utf-8").read()
    n = 0

    def fix(m):
        global n
        tag = m.group(0)
        if "fill:currentColor" in tag:
            return tag
        n += 1
        if ' style="' in tag:
            return tag.replace(' style="', ' style="fill:currentColor;stroke:none;', 1)
        return tag[:-1] + ' style="fill:currentColor;stroke:none;">'

    t = re.sub(r'<svg\b[^>]*viewBox="0 0 256 256"[^>]*>', fix, t)
    open(p, "w", encoding="utf-8").write(t)
    print(p, n, "fixed")
