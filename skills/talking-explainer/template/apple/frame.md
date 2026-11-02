# frame.md - "{{FILM_NAME}}" talking explainer (design truth)

<!-- FILM-SPECIFIC parts are marked [FILM]. They still hold the worked example's values (REA - "Reverse Engineer
     Anything", 129.0s). Rewrite every [FILM] part for this film (SKILL.md phase 4) before any worker starts. -->

1920x1080 LANDSCAPE (16:9), rendered at **60fps**, [FILM] 129.0s (126.2s voice + 2.8s held end card),
[FILM] 12 scenes + two full-film overlays ({{PRESENTER}}, the lip-synced presenter, LEFT third; the {{BRAND_NAME}}
corner logo). **The look is Apple:** white light, near-black ink, Geist display type with tight tracking, glass
cards with hairlines and long soft shadows, critically damped springs, restraint - one idea on screen, lots of air.
Content per scene lives in each storyboard block; this file is the LOOK and the shared rules. Obey it to the letter.

## Style - Apple, applied to the four motion languages + emphasis/zoom

- **Restraint first:** one idea per frame, one hero object, big type, generous space. Every element earns its
  place. No decoration, no clutter, no shapes for their own sake.
- **Brand idents** - s01 opens on the {{BRAND_NAME}} logo; the last scene is the end card (logo + "{{CTA}}").
  Markup: `references/brand-snippet.html`. The m-brand corner logo overlay is not yours.
- **Kinetic typography ("materialize"):** the TOP BAND headline of every scene. Each word is its own span:
  it rises from y +26 with opacity 0 -> 1 AND `filter: blur(10px) -> blur(0px)` on the word span (a leaf), with
  the critically damped spring `sp(0.5)`, ~0.05s stagger, landing on its narration word. A replaced headline
  leaves the way it came (y -18, opacity 0, blur 8px, power2.in 0.3s) BEFORE the next arrives. Highlight words
  carry their meaning colour from the start (no colour flash). Line wrapper never animates.
- **Springs, not back.out:** every arrival uses `sp(response)` from the scene-starter (damping 1.0, response
  0.45-0.7) - NO overshoot on panels, cards, windows, text. A small overshoot (`sp(0.45, 0.75)`) only on a POP that
  carries momentum: the lens landing, a badge, a stamp, a counter's final value. `back.out` is banned in this film.
- **Spatial consistency:** things leave along the path they came in; a card that rose from below sinks back down.
  Things that open from a trigger grow from it (set `transformOrigin` to the trigger side).
- **UI/UX animation** - [FILM] s06-s08: the agent terminal types (one `tl.set` per character or per word), a cursor
  on arcs (keyframe arrays, power2.inOut), presses (scale 0.96 -> 1), a search field filtering a list.
- **Explainer animation** - lines that draw (strokeDashoffset), cards that deal out, counters that tick (one
  `tl.set` per step), the lens gliding over things.
- **Emphasis + zoom** - every scene carries at least two, marked **ZOOM** / **EMPH** in its block:
  - **ZOOM (camera push-in):** on the cue word the camera glides toward the named object - tween `#<id>-cam` z
    +100..+180 with a matching x/y so the object moves toward frame centre-right (NEVER left of x 640),
    `sine.inOut` or `power2.inOut` 1.0-1.3s (slow and smooth = premium), then eases back to identity (>= 0.9s)
    before the next beat or the seam. One camera leg at a time per property.
  - **EMPH pulse:** scale 1 -> 1.06..1.1 -> 1 with `sp(0.4, 0.7)` up and `sp(0.5)` back (restraint: never > 1.1).
  - **EMPH marker sweep:** `.ap-mark` bar behind a word (meaning colour at ~14%), scaleX 0 -> 1 from the left,
    power3.out 0.4s, stays.
  - **EMPH underline draw:** an SVG line (4-5px, round caps) under a word, strokeDashoffset to 0, power2.out 0.45s.
  - **EMPH focus pull:** everything else dims (opacity -> 0.3..0.45 and blur 4px on LEAVES only, never a 3D
    parent) while the subject stays sharp or lifts toward the camera (z +60); restore before exits.
  - **EMPH number punch-in:** a counter ticks (one `tl.set` per step) then pulses once.
  - **EMPH shake:** rotationZ -2 -> 2 -> 0 (sine.inOut 0.4s) - ONLY on red "not allowed" moments.
  Never stack two emphasis effects on one element at once; never emphasise a word before it is spoken.
- **The spine = THE LENS** (`.ap-lens` blue round badge with a magnifier glyph, and `.ap-ring` - the big
  inspection ring it becomes when it hovers over a thing). It means "look inside / find out how it works".
  [FILM] Born in s04, it is the topic's mark in s01, inspects the app in s06, is step 2 in s07, closes the film in
  s12. Same look everywhere - copy the markup from `references/snippets.html` (APPLE LAYER section). A film may
  pick a different spine object; then rewrite this bullet and keep it one look everywhere.

## Tokens (`assets/kit.css` :root, APPLE LAYER at the end of the file - never invent colours)

| Role | Value |
|---|---|
| ground | `.kit-ground` = white radial light -> `#F5F5F7` -> `#E6E6EB`; floor = fine ink dots (kit-floor) |
| card / glass / well | `#FFFFFF`, `.ap-glass` (faked glass: white gradient + top edge + hairline + long shadow), `#F2F2F5` |
| ink / ink-soft / ink-faint | `#1D1D1F` / `#424245` / `#6E6E73` |
| dark pane (agent terminal, binary) | `.ap-dark` `#2C2C2E -> #1C1C1E`, text `#F5F5F7`, dim text `#A1A1A6`, prompt glyph `#2997FF` |
| [FILM] ORANGE = THEIRS (`--api` / `--api-ink`, kit class `.api`) | `#F56300` / `#B64400` - the famous cafe + its latte, the original app, someone else's software |
| [FILM] BLUE = the topic + your AI agent + evidence (`--wh` / `--wh-ink`, kit class `.wh`) | `#0071E3` / `#0066CC` - the lens, the agent, findings, evidence |
| [FILM] GREEN = YOURS / allowed (`--ok` / `--ok-ink`, class `.ok`) | `#34C759` / `#1E8A3C` - learning, your own version, permission |
| [FILM] GREY = hidden / unknown (`--reply`, class `.reply`) | `#86868B` / `#6E6E73` - the secret recipe, closed source code |
| RED = NOT allowed / the problem (`--bad` / `--bad-ink`, class `.bad`) | `#FF3B30` / `#D70015` - only the "never do this" moments |
| hairline | `rgba(0,0,0,.08)` |

Colour = meaning. Never use a meaning colour decoratively; never swap them. Bans: emoji, neon glow, purple-to-blue
gradient, coloured left-border cards, circular spinners (shimmer sweep instead), stock people, "John Doe", hard
cuts, empty frames, `backdrop-filter` (fake the glass with `.ap-glass`), third-party LOGOS (product names are plain
text) unless this film shows real apps (SKILL.md "Real apps + real logos" - then list each logo file under Assets).
[FILM] Data is fictional except the real subject: (list the exact real strings here). Use the exact strings in the
storyboard blocks. On-screen copy is BASIC ENGLISH, headline lines ~6 words max. [FILM] The NARRATION language:
(the profile's language) - the screen carries the short English key words on the narration's cue words.

## Type - Geist only

**Missing glyphs (e.g. the peso sign ₱) fall back to a system font** - Geist and Geist Mono have no ₱. Build it
from a "P" plus two bars (rename the prefix):
`.<id>-peso { position: relative; display: inline-block; }`
`.<id>-peso i { position: absolute; left: -.05em; width: .66em; height: .075em; background: currentColor; border-radius: .02em; }`
`.<id>-peso i:nth-child(1) { top: .33em; } .<id>-peso i:nth-child(2) { top: .5em; }`
markup: `<span class="<id>-peso">P<i></i><i></i></span>189`.

Every scene declares, inside its template (the scene-starter has them):

```css
@font-face { font-family: 'Geist'; font-weight: 100 900; src: url('assets/fonts/geist-var.woff2') format('woff2'); }
@font-face { font-family: 'Geist Mono'; font-weight: 100 900; src: url('assets/fonts/geist-mono-var.woff2') format('woff2'); }
```

Tracking is size-specific - display (>= 120px) `-0.05em`, headlines (60-84px) `-0.035em`, body (36-48px)
`-0.02em`, UI/mono (28-34px) `0`. Leading tight on big type (0.92-1.05), 1.3-1.5 on body. Hierarchy from weight
+ size together: display/headline 700, body 500-600, secondary in ink-faint. Geist Mono for code, binary,
terminal text and numbers in UI only.

Sizes: top-band headline `.kit-label` 84px or `.kit-label.sm` 60px (always a real headline, never a kicker alone);
hero display `.ap-display` 160-240px; body/labels >= 36px; UI text >= 30px effective (author at its closest-shot
size; `.kit-zoom` only if needed); captions 44px+. Main objects fill the STAGE (x 640-1860, y 200-1020) - use its
full width and height, never a small cluster in the middle.

## Shared kit - `assets/kit.css` + `references/snippets.html`

Every scene links it inside its template: `<link rel="stylesheet" href="assets/kit.css">`. Copy markup from the
snippets file (the APPLE LAYER section at its end first); never restyle a kit/ap class inside a scene (sizes via
inline style/vars are fine). Use: `.ap-glass`, `.ap-dark`, `.ap-window`, `.ap-bar`, `.ap-lens`, `.ap-ring`,
`.ap-badge(.ok/.bad/.wh)`, `.ap-display`, `.ap-sub`, `.ap-mono`, `.ap-mark(.wh/.ok/.bad/.api)`, `.kit-label(.sm)`,
`.kit-kicker`, `.kit-caption`, `.kit-chip(.api/.wh/.ok/.bad/.reply)`, `.kit-card`, `.kit-cursor`, `.kit-shadow`,
`.kit-shimmer`, `.kit-logo`, `.kit-cta`. **ICONS = SOLAR only:** inline SVGs from `references/icons-solar.html` -
bold-duotone for hero icons, linear for UI chrome; colour with `color:`. Never Lucide (`.kit-ico` paths) or
Phosphor. Artwork CC BY 4.0 (480 Design) - credited in the video description. Do NOT use `.kit-tile`,
`.kit-packet`, `.kit-parcel`, `.kit-ghl-form`, `.kit-n8n` (the chunky look).

## Layout - landscape frame zones (frame px, 1920x1080; world x/y = frame px minus 960/540 at z 0)

- **Presenter zone** x 40-620, y 420-1060: the lip-synced presenter overlay (`compositions/m-presenter.html`, not yours)
  in the LEFT third, feet at y 1030. Never put scene content there - at ANY time, including the peak of a camera
  push - and never draw a mascot or a person. The presenter points/presents to the RIGHT: the thing named sits
  around frame x 700-1150 at its cue.
- **Logo corner** x > 1500, y < 150: the corner logo overlay (`m-brand`, [FILM] 8.1s-122.75s - from build-brand.py).
  Keep it clear.
- **Top band** x 640-1460, y 60-190: the scene's headline, centred on x ~1050. Put the headline in its own 2D
  layer ABOVE the camera rig (outside `#<id>-stage`, track index 2) so pushes never move or crop it.
- **Stage** x 640-1860, y 200-1020: the main objects - the right two-thirds of the frame, full height.
- Title / lockup scenes (the open, the end card) may use the centre-right too, but still never the presenter zone.

## Assets (reference them ROOT-RELATIVE as `assets/...` - never `../assets/`, lint rejects it)

| File | What |
|---|---|
| `fonts/geist-var.woff2`, `fonts/geist-mono-var.woff2` | the only typefaces |
| `brand/logo.*` | the {{BRAND_NAME}} logo (s01 + the end card only, via `.kit-logo` - markup in `references/brand-snippet.html`) |
| `mascot/fx/steam.png`, `sparkle-burst.png` | optional accents (steam on a cup) |

Mascot poses are the overlay's - scenes never use `mascot/poses/`. Everything else is built in-scene from tokens:
cups, shop fronts, windows, terminal, cards, Solar icons.

## The camera (one rig per scene, same lens everywhere)

```html
<div id="<id>-stage" class="clip" data-start="0" data-duration="<dur>" data-track-index="1"
     style="position:absolute; inset:0; perspective:1866px; perspective-origin:50% 50%;">
  <div id="<id>-drift" class="<id>-layer">          <!-- constant breath only -->
    <div id="<id>-cam" class="<id>-layer">          <!-- authored camera legs -->
      <div class="kit-floor"></div>                 <!-- always first, never tweened -->
      <!-- world objects: position:absolute; left:50%; top:50%; then gsap.set(x,y,z,rotationX/Y) -->
    </div>
  </div>
</div>
```

- 1866px perspective. Never change it. World x/y 0 = frame centre (960, 540).
- Move the camera by tweening `#<id>-cam` (inverse transform: dolly in = tween `z` positive). Add a nested
  `#<id>-push` layer when an orbit and a dolly must overlap.
- **Flattening traps:** `opacity < 1`, `filter`, `overflow:hidden`, `clip-path`, `mix-blend-mode` on any ancestor
  that holds 3D children flattens the 3D. Only on leaves (a card face, a label, a word span).
- Depth of field: far layers get a static `filter: blur(4-8px)` on the leaf; a focus pull may tween blur on leaves.
- Constant life: `#<id>-drift` breathes (scale 1 -> 1.015 -> 1, rotationY 0 -> 0.8 -> 0, sine.inOut), at IDENTITY
  at t = 0 and t = dur. The presenter overlay is always moving too, so no frame is dead.
- Shadows: `.ap-glass` / `.ap-window` / `.ap-dark` carry their own; `.kit-shadow` under things standing on the floor.

## Smoothness law (60fps)

1. Animate only `x, y, z, rotationX/Y/Z, scale, opacity` (+ `filter` blur on word spans / leaves, `clipPath`
   reveal, `strokeDashoffset` draw). Never `width/height/top/left/margin/box-shadow/font-size/color`.
2. Eases: `sp(response[, damping])` springs for arrivals and settles; `power2.in` for exits; `sine.inOut` /
   `power2.inOut` for camera legs and glides; `power3.out` for draws/sweeps. **No `none`/linear, no `back.*`,
   no `elastic`, no `steps()`, no `snap`, no `roundProps`, no `Math.round` on animated values.**
3. A camera leg is never shorter than 0.8s; sequence legs on one property (no overlap on the same layer).
4. Seekable and deterministic: one paused timeline, `fromTo` with explicit start states, `immediateRender: false`
   on every later `fromTo` of the same property, no `Math.random`, no clocks, no CSS transitions/animations.
5. `will-change: transform` on every moving layer; `force3D: true` in tweens that move layers in 3D.
6. **Narration is the clock.** Every reveal lands on its cue word: the storyboard block gives scene-local seconds.
   A spring arrival STARTS ~0.15s before the word (it visibly lands ~0.3s after start). Nothing named appears
   before its word. No arrival starts before 0.12 (a negative start clamps to 0 and shows in frame 1).

## Seams - the exact frames both neighbours render

[FILM] One row per cut, from `src/set-film.py`'s printed starts.

| Seam | Time (global) | Shared frame |
|---|---|---|
| film start | 0.0 | canon floor |
| s01-hook -> s02-trending | 7.9 | canon floor |
| s02-trending -> s03-cafe | 18.3 | canon floor |
| s03-cafe -> s04-taste | 28.25 | STAGE POSE "LATTE" (defined once in s03, identical values in s04 - same worker) |
| s04-taste -> s05-short | 38.55 | canon floor |
| ... | ... | canon floor |
| s11-yours -> s12-close | 120.05 | canon floor |
| film end | 129.0 | the held end card (not a loop) |

- **Canon floor** = `.kit-ground` + `.kit-floor` with drift and cam at identity and NOTHING else visible. Exits
  finish by dur - 0.08; arrivals start at >= 0.12. The presenter overlay keeps the frame alive across it.
- **Stage pose seams** = both files gsap.set the same objects to the same values with cam/drift at identity; the
  outgoing scene's extras are gone by dur - 0.08 and the incoming scene adds nothing before 0.12.

`.kit-grain` sits on top of every scene for its whole duration (static).
