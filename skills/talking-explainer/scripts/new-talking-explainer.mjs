// Scaffold a TALKING explainer film: the explainer-kit scaffold (engine skeleton, brand, SFX, audio) plus this
// skill's Apple look (Geist, glass, sp() springs, the lens spine), the Solar icon sheet, the src helpers and the
// lip-synced presenter. Landscape 16:9 only - a portrait cut is a PORT of the finished film (port-portrait.py).
// Usage: node <skill>/scripts/new-talking-explainer.mjs [path/to/film] --name <slug> [--mp3 <narration.mp3>] [--mascot <dir>]
//   path omitted -> <films_dir from brand.json>/<name>. The folder may already hold SCRIPT.md - nothing there is
//   overwritten. Mascot: --mascot <dir>, else <home>/profile/mascot-talking (when it has mouth-fit.json), else the
//   bundled talking demo. A mascot needs mouth-fit.json to talk (explainer-kit/references/mascot-sheet-prompt.md).
import { execFileSync, spawnSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const SKILL = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const KIT = path.resolve(SKILL, '..', 'explainer-kit');
const ENGINE = path.resolve(SKILL, '..', 'spatial-film');
const { loadBrand, expandHome, profileDir } = await import(pathToFileURL(path.join(KIT, 'scripts', 'lib', 'brand.mjs')).href);
const { python } = await import(pathToFileURL(path.join(KIT, 'scripts', 'lib', 'python.mjs')).href);

const args = process.argv.slice(2);
const flag = (k) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : null; };
const die = (m) => { console.error(m); process.exit(1); };
const fwd = (p) => p.replace(/\\/g, '/').replace(/\/+$/, '');
const target = args.find((a, i) => !a.startsWith('--') && !(i > 0 && args[i - 1].startsWith('--')));
const name = flag('--name');
const mp3 = flag('--mp3');
if (!name) die('usage: new-talking-explainer.mjs [path] --name <slug> [--mp3 <file>] [--mascot <dir>]');
if (!fs.existsSync(path.join(KIT, 'scripts', 'new-explainer.mjs'))) die('explainer-kit not found next to this skill at ' + KIT);

let brand;
try { brand = loadBrand(); } catch (e) { die(e.message + '\n(run explainer-kit setup first: setup-check.mjs, then profile.mjs init)'); }
let py;
try { py = python(); } catch (e) { die(e.message); }
const dir = path.resolve(target || path.join(expandHome(brand.films_dir), name));

// the talking mascot: --mascot, then the profile's talking character, then the bundled demo
const own = path.join(profileDir(), 'mascot-talking');
const mascot = flag('--mascot') ? path.resolve(flag('--mascot'))
  : fs.existsSync(path.join(own, 'mouth-fit.json')) ? own : path.join(SKILL, 'assets', 'mascot');
for (const f of ['manifest.json', 'mouth-fit.json']) {
  if (!fs.existsSync(path.join(mascot, f))) die(`${mascot} has no ${f} - it cannot talk yet. Run cut-sheet / blink-fit / mouth-fit (explainer-kit/references/mascot-sheet-prompt.md) or drop --mascot to use the demo.`);
}
if (fs.existsSync(path.join(profileDir(), 'mascot')) && mascot === path.join(SKILL, 'assets', 'mascot')) {
  console.warn('note: your profile mascot has no mouth shapes, so the bundled talking demo presents this film.');
}

// 1. explainer-kit scaffold into a TEMP folder (it wants an empty folder), then merge without overwriting
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'talking-'));
const tdir = path.join(tmp, name);
const a = [path.join(KIT, 'scripts', 'new-explainer.mjs'), tdir, '--name', name];
if (mp3) a.push('--mp3', path.resolve(mp3));
execFileSync(process.execPath, a, { stdio: ['ignore', 'ignore', 'inherit'] });
fs.mkdirSync(dir, { recursive: true });
fs.cpSync(tdir, dir, { recursive: true, force: false, errorOnExist: false });
fs.rmSync(tmp, { recursive: true, force: true });

// 2. this skill's contract (the scaffold's example contract is the look)
const T = path.join(SKILL, 'template');
const cp = (from, to) => { fs.mkdirSync(path.dirname(to), { recursive: true }); fs.cpSync(from, to, { recursive: true }); };
cp(path.join(T, 'apple', 'frame.md'), path.join(dir, 'frame.md'));
cp(path.join(T, 'apple', 'worker-brief.md'), path.join(dir, 'references', 'worker-brief.md'));
cp(path.join(T, 'apple', 'scene-starter.html'), path.join(dir, 'references', 'scene-starter.html'));
const kit = path.join(dir, 'assets', 'kit.css');
if (!fs.readFileSync(kit, 'utf8').includes('APPLE LAYER')) {
  fs.appendFileSync(kit, '\n' + fs.readFileSync(path.join(T, 'apple', 'kit-apple.css'), 'utf8'));
  fs.appendFileSync(path.join(dir, 'references', 'snippets.html'), '\n' + fs.readFileSync(path.join(T, 'apple', 'snippets-apple.html'), 'utf8'));
}
for (const f of fs.readdirSync(path.join(T, 'src'))) cp(path.join(T, 'src', f), path.join(dir, 'src', f));
// worked example = REA (the example storyboard/brief belong to the other look)
for (const f of ['STORYBOARD.md', 'BRIEF.md', 'references/STORYBOARD.example.md', 'references/BRIEF.example.md']) {
  fs.rmSync(path.join(dir, f), { force: true });
}
cp(path.join(SKILL, 'references', 'example'), path.join(dir, 'references', 'example'));

// 3. talking mascot (poses + blinks + faces + fx + mouths + 3 json) and Geist
fs.rmSync(path.join(dir, 'assets', 'mascot'), { recursive: true, force: true });
fs.cpSync(mascot, path.join(dir, 'assets', 'mascot'), { recursive: true, filter: (p) => !/[\\/]source$|[\\/]_[^\\/]*\.png$/.test(p) });
cp(path.join(SKILL, 'assets', 'fonts'), path.join(dir, 'assets', 'fonts'));

// 4. Solar icon sheet (needs npm; CC BY 4.0 - credit it in the video description)
const [pyBin, ...pyArgs] = py;
const sol = spawnSync(pyBin, [...pyArgs, path.join(SKILL, 'scripts', 'solar-snippets.py'), path.join(dir, 'references', 'icons-solar.html')], { encoding: 'utf8' });
console.log((sol.stdout || '').trim() || `warning: Solar icon sheet not written (${(sol.stderr || String(sol.error || '')).trim().split('\n').pop()}) - rerun solar-snippets.py`);

// 5. placeholders in this skill's files (+ the temp path the base scaffold wrote into its own)
const vars = {
  PROJECT_DIR: fwd(dir), SKILL: fwd(SKILL), ENGINE: fwd(ENGINE), FILM_NAME: name, BRAND_NAME: brand.name,
  OPENER: brand.opener, CTA: brand.cta, PRESENTER: brand.presenter, PY: py.join(' '),
};
const SKIP = new Set(['assets', 'node_modules', '.git', '.hyperframes', 'renders', 'snapshots']);
const walk = (d) => {
  for (const e of fs.readdirSync(d, { withFileTypes: true })) {
    const p = path.join(d, e.name);
    if (e.isDirectory()) { if (!SKIP.has(e.name)) walk(p); continue; }
    if (!/\.(md|html|json|py)$/i.test(e.name)) continue;
    const s = fs.readFileSync(p, 'utf8');
    const out = s.split(fwd(tdir)).join(fwd(dir))
      .replace(/\{\{(PROJECT_DIR|SKILL|ENGINE|FILM_NAME|BRAND_NAME|OPENER|CTA|PRESENTER|PY)\}\}/g, (_, k) => vars[k]);
    if (out !== s) fs.writeFileSync(p, out);
  }
};
walk(dir);
const film = JSON.parse(fs.readFileSync(path.join(dir, 'film.json'), 'utf8'));
film._doc = 'Talking explainer (16:9, Apple look). Scenes/audio from src/set-film.py, cues from src/set-cues.py.';
film.ground = '#F5F5F7';
fs.writeFileSync(path.join(dir, 'film.json'), JSON.stringify(film, null, 2) + '\n');

const talking = Object.keys(JSON.parse(fs.readFileSync(path.join(dir, 'assets', 'mascot', 'mouth-fit.json'), 'utf8')));
console.log(`\ntalking explainer ready: ${dir}\n  mascot: ${mascot === path.join(SKILL, 'assets', 'mascot') ? 'the bundled talking demo' : mascot} (talking poses: ${talking.join(', ')})\n` +
  `next: ${mp3 ? '' : 'drop the take at assets/audio/vo.mp3, then '}${py.join(' ')} "${fwd(KIT)}/scripts/transcribe.py" assets/audio/vo.mp3 src/timing --lang <code>`);
