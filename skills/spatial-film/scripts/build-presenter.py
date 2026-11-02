"""Build compositions/m-presenter.html - the presenter overlay for a narrated film.

usage (from the film project root):  python <skill>/scripts/build-presenter.py
Reads src/presenter-track.json (poses on cue words, fx, bob, blink, and optional
"marks" = per-shot spot/size changes + "hide" = [[from, to]] windows out of shot), assets/mascot/manifest.json +
blink-fit.json (sprite sizes, head anchors, blink variants), film.json (total length) and the narration audio
(film.json "audio"[0]) for the talking bob. Deterministic: same inputs -> same file. Never hand-edit the output.
A mascot with no faces/ dir and no -blink variants builds fine (every pose blink=false, head anchor from the pose).
Lip sync: when assets/mascot/mouth-fit.json exists (explainer-kit/scripts/mouth-fit.py), the 6 mouth patches of the
current pose are driven from the voice at track "mouth".rate (default 15/s): silence = the pose's own drawn mouth,
short dips = closed, fricatives = fv, quiet = small, louder = round / open / wide by spectral centroid.
No mouth-fit.json = no lip sync (the talking demo), everything else unchanged.
"""
import json, subprocess
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path.cwd()
film = json.loads((ROOT / "film.json").read_text(encoding="utf-8"))
TRACK = next(p for p in (ROOT / "src/presenter-track.json",) if p.exists())
T = json.loads(TRACK.read_text(encoding="utf-8"))
M = ROOT / "assets/mascot"
fit = json.loads((M / "blink-fit.json").read_text(encoding="utf-8")) if (M / "blink-fit.json").exists() else {}
TOTAL = round(sum(s[1] for s in film["scenes"]) * 60 / film["bpm"] * film.get("beats_per_bar", 4), 4)
S = T["scale"]
HAS_FACES = (M / "faces/neutral.png").exists()
if HAS_FACES:
    NEUTRAL_W = Image.open(M / "faces/neutral.png").width
    BAND_W = int(NEUTRAL_W * 0.94) - int(NEUTRAL_W * 0.08)  # same band as blink-fit.py

# ---- per-pose geometry: head-centre anchor x, feet = sprite bottom ----
poses = sorted({p for _, p in T["poses"]})
geo = {}
for name in poses:
    im = Image.open(M / f"poses/{name}.png")
    w, h = im.size
    f = fit.get(name, {})
    a = np.asarray(im.convert("RGBA"))[..., 3]
    if HAS_FACES and f.get("score", 0) >= 0.70:
        ax = f["x"] + BAND_W * f["scale"] / 2
    else:  # head rows centroid (no raised arm in these poses)
        cols = np.nonzero(a[int(h * 0.04): int(h * 0.26)] > 128)[1]
        if cols.size:
            ax = float(cols.mean())
        else:  # no head match: top-centre of the silhouette
            top = np.nonzero((a > 128).any(1))[0]
            tc = np.nonzero(a[top[0]: top[0] + max(1, h // 50)] > 128)[1] if top.size else []
            ax = float(np.mean(tc)) if len(tc) else w / 2
    geo[name] = {"w": w, "h": h, "ax": ax, "blink": HAS_FACES and bool(f.get("blink")) and (M / f"poses/{name}-blink.png").exists()}

mfit = json.loads((M / "mouth-fit.json").read_text(encoding="utf-8")) if (M / "mouth-fit.json").exists() else {}
mfit = {k: v for k, v in mfit.items() if k in geo}

# ---- voice envelope for the talking bob ----
aud = film["audio"][0]["src"]
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(ROOT / aud), "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                     capture_output=True, check=True).stdout
x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
rate = T["bob"]["rate"]
hop = int(16000 / rate)
n = len(x) // hop
rms = np.sqrt((x[: n * hop].reshape(n, hop) ** 2).mean(1))
env = np.clip(rms / (np.percentile(rms, 95) + 1e-9), 0, 1)
env[env < 0.12] = 0
sm = np.zeros_like(env)  # fast attack, slower release
for i in range(1, n):
    k = 0.6 if env[i] > sm[i - 1] else 0.25
    sm[i] = sm[i - 1] + k * (env[i] - sm[i - 1])
env = np.round(sm, 3)

# ---- visemes for the mouth patches ----
MO = T.get("mouth", {})
mrate, mlead = MO.get("rate", 15), MO.get("lead", 0.03)
vis = []
if mfit:
    mh = int(16000 / mrate)
    mn = len(x) // mh
    win = np.hanning(1024).astype(np.float32)
    freqs = np.fft.rfftfreq(1024, 1 / 16000)
    m_rms, cen, hf = np.zeros(mn), np.zeros(mn), np.zeros(mn)
    for i in range(mn):
        c = i * mh + mh // 2
        seg = x[max(0, c - 512): c + 512]
        if len(seg) < 1024:
            seg = np.pad(seg, (0, 1024 - len(seg)))
        sp = np.abs(np.fft.rfft(seg * win)) ** 2
        tot = sp.sum() + 1e-12
        m_rms[i] = np.sqrt((x[i * mh:(i + 1) * mh] ** 2).mean())
        cen[i] = (sp * freqs).sum() / tot
        hf[i] = sp[freqs > 3500].sum() / tot
    lv = np.clip(m_rms / (np.percentile(m_rms, 95) + 1e-9), 0, 1)
    voiced = lv > 0.1
    vc, vh = cen[voiced], hf[voiced]
    c30, c70, h80 = np.percentile(vc, 30), np.percentile(vc, 70), np.percentile(vh, 80)
    for i in range(mn):
        if not voiced[i]:
            j = i
            while j < mn and not voiced[j]: j += 1
            k = i
            while k > 0 and not voiced[k - 1]: k -= 1
            vis.append("rest" if (j - k) >= 4 else "closed")
        elif hf[i] > h80 and lv[i] < 0.55: vis.append("fv")
        elif lv[i] < 0.3: vis.append("small")
        elif cen[i] < c30: vis.append("round")
        elif cen[i] > c70: vis.append("wide")
        else: vis.append("open")
    for i in range(1, mn - 1):  # one-frame islands read as flicker (closures excepted)
        if vis[i - 1] == vis[i + 1] != vis[i] and vis[i] != "closed":
            vis[i] = vis[i - 1]

# ---- markup ----
P = film.get("overlays", [{}])[0].get("id", "m-presenter")  # the overlay id in film.json
def px(v): return f"{v:.1f}px"
imgs = []
for name, g in geo.items():
    W, H, ax = g["w"] * S, g["h"] * S, g["ax"] * S
    flip = f" transform: scaleX(-1); transform-origin: {px(ax)} 50%;" if name in T["mirror"] else ""
    for suffix in ([""] + (["-blink"] if g["blink"] else [])):
        imgs.append(f'          <img id="{P}-p-{name}{suffix}" class="{P}-p" src="assets/mascot/poses/{name}{suffix}.png" alt="" '
                    f'style="width:{px(W)}; height:{px(H)}; left:{px(-ax)}; top:{px(-H)};{flip}">')
fx_html = []
for i, fx in enumerate(T.get("fx", [])):
    im = Image.open(M / f"{fx['sprite']}.png")
    w, h = im.width * fx["scale"], im.height * fx["scale"]
    fx_html.append(f'        <img id="{P}-fx{i}" class="{P}-p" src="assets/mascot/{fx["sprite"]}.png" alt="" '
                   f'style="width:{px(w)}; height:{px(h)}; left:{px(fx["dx"] - w / 2)}; top:{px(fx["dy"] - h / 2)};">')

mouth_html = []
for name, mf in mfit.items():
    g = geo[name]
    flip = " transform: scaleX(-1); transform-origin: 0 0;" if name in T["mirror"] else ""
    mouth_html.append(f'          <div class="{P}-mw" style="position:absolute; left:0; top:0;{flip}">')
    for m in ("closed", "small", "open", "wide", "round", "fv"):
        mouth_html.append(f'            <img id="{P}-m-{name}-{m}" class="{P}-m" src="assets/mascot/mouths/{name}/{m}.png" alt="" '
                          f'style="width:{px(mf["w"] * S)}; height:{px(mf["h"] * S)}; left:{px((mf["x"] - g["ax"]) * S)}; top:{px((mf["y"] - g["h"]) * S)};">')
    mouth_html.append("          </div>")
fx_html = []
for i, fx in enumerate(T.get("fx", [])):
    im = Image.open(M / f"{fx['sprite']}.png")
    w, h = im.width * fx["scale"], im.height * fx["scale"]
    fx_html.append(f'        <img id="{P}-fx{i}" class="{P}-p" src="assets/mascot/{fx["sprite"]}.png" alt="" '
                   f'style="width:{px(w)}; height:{px(h)}; left:{px(fx["dx"] - w / 2)}; top:{px(fx["dy"] - h / 2)};">')

# ---- timeline ----
js = []
home, ent = T["home"], T["enter"]
js.append(f"gsap.set(q('pos'), {{ x: {ent['from_x']}, y: {home['feet']}, force3D: true }});")
js.append(f"tl.fromTo(q('pos'), {{ x: {ent['from_x']} }}, {{ x: {home['x']}, duration: {ent['dur']}, ease: 'expo.out', force3D: true }}, {ent['at']});")
# optional "marks": the presenter changes spot/size per shot (films that cut between rooms).
# [{"at": t, "x": px, "feet": px, "scale": 1, "dur": 0}] - dur 0 = a hard cut on t, dur > 0 = a move ending at t + dur.
# optional "hide": [[from, to], ...] - out of the shot (opacity on the anchor child, never on the .clip).
cur = {"x": home["x"], "y": home["feet"], "scale": 1}
for mk in sorted(T.get("marks", []), key=lambda m: m["at"]):
    to = {"x": mk["x"], "y": mk["feet"], "scale": mk.get("scale", 1)}
    if mk.get("dur", 0) > 0:
        js.append(f"tl.fromTo(q('pos'), {json.dumps(cur)}, {{ ...{json.dumps(to)}, duration: {mk['dur']}, ease: '{mk.get('ease', 'expo.inOut')}', immediateRender: false, force3D: true }}, {mk['at']});")
    else:
        js.append(f"tl.set(q('pos'), {json.dumps(to)}, {mk['at']});")
    cur = to
for a, b in T.get("hide", []):
    js.append(f"tl.set(q('pos'), {{ opacity: 0 }}, {a}); tl.set(q('pos'), {{ opacity: 1 }}, {b});")
sched = T["poses"]
first = sched[0][1]
js.append(f"gsap.set('.{P}-p', {{ opacity: 0 }}); gsap.set(q('p-{first}'), {{ opacity: 1 }});")
for (t, name), prev in zip(sched[1:], sched):
    js.append(f"tl.set(q('p-{prev[1]}'), {{ opacity: 0 }}, {t}); tl.set(q('p-{name}'), {{ opacity: 1 }}, {t});")
    js.append(f"tl.fromTo(q('pop'), {{ scaleX: 1.04, scaleY: 0.95 }}, {{ scaleX: 1, scaleY: 1, duration: 0.42, ease: 'back.out(2.2)', immediateRender: false, force3D: true }}, {t});")
# blinks: only on poses that have a blink variant, never within 0.3s of a swap
swaps = [t for t, _ in sched]
def pose_at(t):
    cur = sched[0][1]
    for st, nm in sched:
        if st <= t: cur = nm
    return cur
tb, k, b = 1.9, 0, T["blink"]
while tb < TOTAL - 0.5:
    nm = pose_at(tb)
    if geo[nm]["blink"] and all(abs(tb - s) > 0.3 and abs(tb + b["dur"] - s) > 0.3 for s in swaps):
        js.append(f"tl.set(q('p-{nm}-blink'), {{ opacity: 1 }}, {tb:.2f}); tl.set(q('p-{nm}-blink'), {{ opacity: 0 }}, {tb + b['dur']:.2f});")
    tb += b["every"][k % len(b["every"])]; k += 1
# lip sync: one visible mouth patch at a time, for the pose on screen
if mfit:
    js.append(f"gsap.set('.{P}-m', {{ opacity: 0 }});")
    events = sorted({round(i / mrate - mlead, 3) for i in range(len(vis)) if i == 0 or vis[i] != vis[i - 1]} | set(swaps))
    shown, n_mouth = None, 0
    for t in events:
        if t < 0: continue
        vi = min(len(vis) - 1, max(0, int(round((t + mlead) * mrate))))
        nm, v = pose_at(t + 1e-6), vis[vi]
        want = f"m-{nm}-{v}" if (v != "rest" and nm in mfit) else None
        if want != shown:
            if shown: js.append(f"tl.set(q('{shown}'), {{ opacity: 0 }}, {t:.3f});")
            if want: js.append(f"tl.set(q('{want}'), {{ opacity: 1 }}, {t:.3f});"); n_mouth += 1
            shown = want
# breath (1.2% on the breath layer) and talking bob (voice envelope) - fromTo chains, explicit starts
cyc, t = 2.4, 0.0
while t + cyc <= TOTAL:
    js.append(f"tl.fromTo(q('breath'), {{ scaleY: 1 }}, {{ scaleY: 1.012, duration: {cyc / 2}, ease: 'sine.inOut', immediateRender: false, force3D: true }}, {t:.2f});")
    js.append(f"tl.fromTo(q('breath'), {{ scaleY: 1.012 }}, {{ scaleY: 1, duration: {cyc / 2}, ease: 'sine.inOut', immediateRender: false, force3D: true }}, {t + cyc / 2:.2f});")
    t += cyc
by, sq = T["bob"]["y"], T["bob"]["squash"]
js.append(f"var E = {json.dumps(env.tolist())};")
js.append(f"for (var i = 1; i < E.length; i++) {{ if (E[i] === 0 && E[i - 1] === 0) continue;"
          f" tl.fromTo(q('bob'), {{ y: {by} * E[i - 1], scaleY: 1 + {sq} * E[i - 1] }}, {{ y: {by} * E[i], scaleY: 1 + {sq} * E[i],"
          f" duration: {1 / rate:.4f}, ease: 'sine.inOut', immediateRender: false, force3D: true }}, (i - 1) / {rate}); }}")
for i, fx in enumerate(T.get("fx", [])):
    js.append(f"gsap.set(q('fx{i}'), {{ opacity: 0, scale: 0.3, transformOrigin: '50% 100%' }});")
    js.append(f"tl.fromTo(q('fx{i}'), {{ opacity: 0, scale: 0.3, y: 20 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.45, ease: 'back.out(2)', immediateRender: false, force3D: true }}, {fx['at']});")
    js.append(f"tl.fromTo(q('fx{i}'), {{ y: 0 }}, {{ y: -14, duration: {fx['out'] - fx['at'] - 0.7:.2f}, ease: 'sine.inOut', immediateRender: false, force3D: true }}, {fx['at'] + 0.45});")
    js.append(f"tl.fromTo(q('fx{i}'), {{ opacity: 1, scale: 1 }}, {{ opacity: 0, scale: 0.6, duration: 0.25, ease: 'power2.in', immediateRender: false, force3D: true }}, {fx['out'] - 0.25});")

html = f"""<!-- Generated by spatial-film/scripts/build-presenter.py from {TRACK.name} - edit the track, not this file. -->
<template>
<style>
#root {{ position: absolute; inset: 0; width: {film["width"]}px; height: {film["height"]}px; overflow: hidden; }}
.{P}-anchor {{ position: absolute; left: 0; top: 0; width: 0; height: 0; will-change: transform; transform-origin: 0 0; }}
.{P}-p, .{P}-m {{ position: absolute; display: block; will-change: opacity; }}
</style>
<div id="root" data-composition-id="{P}" data-width="{film["width"]}" data-height="{film["height"]}">
  <div id="{P}-layer" class="clip" data-start="0" data-duration="{TOTAL}" data-track-index="1" style="position:absolute; inset:0;">
    <div id="{P}-pos" class="{P}-anchor">
      <div id="{P}-shadow" style="position:absolute; left:-170px; top:-34px; width:340px; height:68px; border-radius:50%; background:radial-gradient(closest-side, rgba(11,30,63,.24), rgba(11,30,63,0));"></div>
      <div id="{P}-bob" class="{P}-anchor">
        <div id="{P}-breath" class="{P}-anchor">
          <div id="{P}-pop" class="{P}-anchor">
{chr(10).join(imgs)}
{chr(10).join(mouth_html)}
          </div>
        </div>
      </div>
{chr(10).join(fx_html)}
    </div>
  </div>
</div>
<script>
(function () {{
  var q = function (id) {{ return '#{P}-' + id; }};
  var tl = gsap.timeline({{ paused: true }});
  {(chr(10) + '  ').join(js)}
  window.__timelines = window.__timelines || {{}};
  window.__timelines['{P}'] = tl;
}})();
</script>
</template>
"""
(ROOT / "compositions").mkdir(exist_ok=True)
(ROOT / f"compositions/{P}.html").write_text(html, encoding="utf-8")
print(f"compositions/{P}.html: {len(sched)} poses, {sum(1 for j in js if 'blink' in j)} blinks, {len(env)} bob frames, total {TOTAL}s")
if mfit: print(f"lip sync: {len(mfit)} poses, {n_mouth} mouth shapes shown, visemes " + str({v: vis.count(v) for v in sorted(set(vis))}))
for name, g in geo.items():
    print(f"  {name:<10} {g['w'] * S:6.0f}x{g['h'] * S:4.0f}  anchor {g['ax'] * S:5.1f}  blink {g['blink']}")
