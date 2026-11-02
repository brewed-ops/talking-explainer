// Lint + check + snapshot ONE scene in its isolated harness (never touches the shared index.html).
// Run from the film project root:  node <skill>/scripts/test-scene.mjs <scene_id> "<t1,t2,...>"
// Snapshots: .hyperframes/test/<id>/snaps/frame-NN-at-Xs.png + contact-sheet.jpg (read the sheet first).
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

const [id, times] = process.argv.slice(2);
if (!id || !times) { console.error('usage: test-scene.mjs <scene_id> "<t1,t2,...>"'); process.exit(1); }
if (!fs.existsSync('film.json')) { console.error('run from the film project root (film.json not found)'); process.exit(1); }
const V = JSON.parse(fs.readFileSync('film.json', 'utf8')).hyperframes;
const T = path.join('.hyperframes', 'test', id);
if (!fs.existsSync(T)) { console.error(`no harness for ${id} - run: <py> <skill>/scripts/make-harness.py`); process.exit(1); }
const comp = path.join('compositions', `${id}.html`);
if (!fs.existsSync(comp)) { console.error(`${comp} not written yet`); process.exit(1); }
fs.copyFileSync(comp, path.join(T, 'compositions', `${id}.html`));
// keep the shared stylesheets + logos current: kits grow while workers build, and the harness copy is only
// made at make-harness time (every worker on the premium rebuild hit a stale kit, 2026-10-14)
for (const f of fs.readdirSync('assets').filter((n) => n.endsWith('.css'))) fs.copyFileSync(path.join('assets', f), path.join(T, 'assets', f));
if (fs.existsSync(path.join('assets', 'logos'))) fs.cpSync(path.join('assets', 'logos'), path.join(T, 'assets', 'logos'), { recursive: true });
// npx is a .cmd shim on Windows, so it needs a shell there; nowhere else
const hf = (a) => {
  const r = spawnSync('npx', ['--yes', `hyperframes@${V}`, ...a], { encoding: 'utf8', shell: process.platform === 'win32', maxBuffer: 1 << 26 });
  return (r.stdout || '') + (r.stderr || '') + (r.error ? String(r.error) : '');
};
const tail = (s, n) => s.replace(/\s+$/, '').split('\n').slice(-n).join('\n');
console.log(`== lint ${id}`);
let lint = hf(['lint', T]);
// a cold npx cache can race on first use (ECOMPROMISED); one retry clears it
if (lint.includes('ECOMPROMISED')) lint = hf(['lint', T]);
console.log(tail(lint, 40));
// lint alone misses the browser audits (WCAG contrast, text overlap) that gate the final `check`: a portrait port
// shipped 2 contrast + 4 overlap errors past lint-clean workers. Run check on the harness too.
console.log(`== check ${id} (layout + contrast)`);
console.log(hf(['check', T]).split('\n').filter((l) => /✗|⚠|Fix:|Try |error\(s\)|Check (passed|failed)/.test(l)).slice(0, 30).join('\n'));
// contract traps lint does not catch (each one shipped once): an inline visibility:visible escapes the scene's
// host and leaks into other scenes on seek; an element with the bare scene id collides with the harness host.
const src = fs.readFileSync(comp, 'utf8').split('\n');
src.forEach((l, i) => {
  if (/visibility: *['"]visible['"]/.test(l)) console.log(`${i + 1}: TRAP: use visibility 'inherit' (or opacity), never 'visible' - fix before reporting`);
  if (l.includes(`id="${id}"`) && !l.includes('data-composition-id')) console.log(`${i + 1}: TRAP: an element carries the bare scene id - prefix it (${id}-...)`);
});
console.log(`== snapshot ${id} at ${times}`);
fs.rmSync(path.join(T, 'snaps'), { recursive: true, force: true });
console.log(tail(hf(['snapshot', T, '--at', times, '--no-end', '--describe', 'false', '-o', path.join(T, 'snaps')]), 6));
