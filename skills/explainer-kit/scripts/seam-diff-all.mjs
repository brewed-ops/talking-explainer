// Seam diff for a narrated film: every seam seam-check.py wrote to snapshots/seams/, with the presenter box
// masked (he moves across every cut, so a raw diff FAILs on him alone). 0.00% outside-presenter on every seam = pass.
// Usage (film root): node <skill>/scripts/seam-diff-all.mjs [x0,y0,x1,y1]
// The default box follows film.json: landscape 20,300,640,1080 (a talking mascot's hair on a bob and its fx bubbles above the head);
// portrait 0,980,580,1720 (covers the 9x16 Presenter zone and the talking-explainer portrait presenter, feet y 1640).
// Frames are grouped by time (one cluster per seam, 2 OR 3 frames: before / at / after) and the FIRST vs LAST frame
// of each cluster is diffed - the same pair seam-check compares. The loop frame (t = 0) stays alone and is skipped:
// a narrated film ends on a held end card, not a loop.
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { python } from './lib/python.mjs';

let portrait = false;
try { const f = JSON.parse(fs.readFileSync('film.json', 'utf8')); portrait = f.height > f.width; } catch {}
const box = process.argv[2] || (portrait ? '0,980,580,1720' : '20,300,640,1080');
const diff = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..', 'spatial-film', 'scripts', 'seam-diff.py');
const seams = path.resolve('snapshots', 'seams');
if (!fs.existsSync(seams)) { console.error('snapshots/seams not found - run from the film root after seam-check.py'); process.exit(1); }
const out = path.resolve('snapshots', 'seamdiff');
fs.mkdirSync(out, { recursive: true });
const [py, ...pyArgs] = python();
const at = (f) => parseFloat((/at-([0-9.]+)s/.exec(f) || [])[1]);
const files = fs.readdirSync(seams).filter((f) => /^frame-.*\.png$/.test(f)).sort();
const groups = [];
for (const f of files) {
  const g = groups[groups.length - 1];
  if (g && at(f) - at(g[g.length - 1]) >= 0 && at(f) - at(g[g.length - 1]) < 0.1) g.push(f); else groups.push([f]);
}
let i = 0;
for (const g of groups) {
  if (g.length < 2) continue;
  const [a, b] = [g[0], g[g.length - 1]];
  const r = spawnSync(py, [...pyArgs, diff, path.join(seams, a), path.join(seams, b), path.join(out, `pair-${i++}.png`), box], { encoding: 'utf8' });
  const last = (r.stdout || r.stderr || String(r.error || '')).trim().split('\n').pop();
  console.log(`${a} -> ${b}: ${last}`);
}
