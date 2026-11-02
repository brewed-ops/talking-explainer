// Final render from the CLI with the hardware GPU path, logged to a file, then verified with ffprobe.
// Run from the film project root:  node <skill>/scripts/render-final.mjs <name> [extra render args, e.g. --resolution 4k]
// Launch it with run_in_background and read renders/<name>.log for progress (never pipe through | tail).
// If you stop it, kill the node process tree (Windows: taskkill /T /F /PID <pid>; macOS/Linux: pkill -f "hyperframes.*render")
// - stopping only this wrapper leaves the render running.
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import fs from 'node:fs';
import path from 'node:path';

const [name = 'film-1080p60', ...extra] = process.argv.slice(2);
if (!fs.existsSync('film.json')) { console.error('run from the film project root'); process.exit(1); }
const film = JSON.parse(fs.readFileSync('film.json', 'utf8'));
fs.mkdirSync('renders', { recursive: true });
const log = path.join('renders', `${name}.log`);
const mp4 = path.join('renders', `${name}.mp4`);
const fd = fs.openSync(log, 'w');
const start = Date.now();
// npx is a .cmd shim on Windows, so it needs a shell there; nowhere else
const r = spawnSync('npx', ['--yes', `hyperframes@${film.hyperframes}`, 'render', '--fps', String(film.fps), '--browser-gpu',
  '--workers', '6', '-o', mp4, ...extra], { stdio: ['ignore', fd, fd], shell: process.platform === 'win32' });
fs.closeSync(fd);
const code = r.status ?? 1;
console.log(`exit ${code} after ${Math.round((Date.now() - start) / 1000)}s - log ${log}`);
const mode = (/"browserGpuMode":"([a-z]*)"/.exec(fs.readFileSync(log, 'utf8')) || [])[1];
console.log(mode === 'hardware' ? 'gpu mode: hardware'
  : `WARNING: gpu mode '${mode || 'unknown'}' - expected hardware (software is ~15x slower)`);
if (fs.existsSync(mp4)) {
  const p = spawnSync('ffprobe', ['-v', 'error', '-select_streams', 'v:0', '-show_entries',
    'stream=width,height,r_frame_rate,nb_frames:format=duration,size', '-of', 'default=nw=1', mp4], { encoding: 'utf8' });
  process.stdout.write(p.stdout || String(p.error || ''));
  // a 1/60 s flash is invisible on contact sheets and seam checks but obvious when watching; scan every frame
  try {
    const { python } = await import('../../explainer-kit/scripts/lib/python.mjs');
    const [py, ...pyArgs] = python();
    const scan = path.join(path.dirname(fileURLToPath(import.meta.url)), 'flash-scan.py');
    const f = spawnSync(py, [...pyArgs, scan, mp4], { encoding: 'utf8' });
    process.stdout.write((f.stdout || '') + (f.stderr || ''));
  } catch (e) { console.log('flash-scan skipped: ' + e.message); }
}
process.exit(code);
