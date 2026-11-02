# Scene workers (12 scenes = 6 Sonnet workers x 2, at most 4 running at once - queue the rest)

Pair scenes so one worker owns what two scenes share:

| Worker | Scenes | Why together |
|---|---|---|
| w1 | s01 hook + the end card | brand idents mirror each other |
| w2 | the two scenes that share a STAGE pose (a hero object handed across a cut) | one worker defines the pose once |
| w3 | the everyday-picture pair (where the spine object is born) | the spine's look is set here |
| w4 | the definition + the diagram | |
| w5 | the UI scenes that share one window/terminal look | the look is defined once |
| w6 | the rest - queued LAST if they copy an object another pair defines | |

A ~5 minute film = ~20 scenes = 10 workers, same cap of 4.

**A fix round counts against the cap of 4.** SendMessage to a finished worker RESUMES it - with 4 builders running
that is 5. When a slot frees, choose: launch the next queued pair OR send a fix round - and batch each worker's
fixes into one message so its fix round is short. If you overshoot, TaskStop the newest worker and resume it with
SendMessage when a slot frees (it keeps its context). **Before EVERY SendMessage, write the running list (builders
+ fix rounds) and count it** - the rule alone does not hold; review finished scenes as they land, but queue their
fixes behind the cap like any other job.

Fix rounds and retimes go to the SAME worker via SendMessage (it keeps its generator scripts and context).

**Workers invent numbers when a block is vague** ("22 sessions" on a history card, made-up file dates, a label
the narration happened to say put on the wrong thing). Give every number in the block (count it from the real
source first), keep the brief's rule 11 ("never invent a number, name or relation"), and check every number and
label on screen against the source on review - not just the layout.

## Prompt template (hand PATHS, never paste files)

```
You are a HyperFrames scene worker building two scenes of a <N>s narrated 16:9 explainer, "<TITLE>" (<language>
narration, a cartoon presenter on its own lip-synced overlay in the LEFT third, branded <brand>, an APPLE
product-page look: sleek, premium, restraint).

PROJECT_DIR: <abs path>
Your frames: <id> (<dur>s) and <id> (<dur>s). <id> = <one line, start to end>. <id> = <one line>.

Start by reading PROJECT_DIR/references/worker-brief.md and follow it exactly. Then read
.hyperframes/frame-packets/_role.md, .hyperframes/frame-packets/<id>.md, .hyperframes/frame-packets/<id>.md,
frame.md (all of it - especially Style, Emphasis + zoom, the spine, Smoothness law),
references/scene-starter.html (copy its sp() spring helper verbatim), assets/kit.css (the APPLE LAYER at its end),
references/snippets.html (APPLE LAYER section at its end), references/icons-solar.html (the only icons allowed).

Hard facts (these win):
- SIZE + ZONE LAW: headlines 60-84px (top band x 640-1460, y 60-190, centred on x ~1050), body >= 36px, UI text
  >= 30px effective (Geist, .kit-zoom at its closest-shot size, never transform scale > 1). The presenter owns
  x 40-620, y 420-1060: NOTHING may enter x < 640 at ANY time, including the peak of a camera push - report the
  measured leftmost x at every push peak. Corner logo owns x > 1500, y < 150. Stage x 640-1860, y 200-1020: use
  its full width and height.
- Put headlines in their own 2D layer above the camera rig so pushes never move or crop them.
- Every ZOOM and EMPH beat in your blocks is required. One camera leg at a time per property; legs >= 0.8s; cam
  and drift at identity on the first and last frame.
- No arrival starts before 0.12 (a "0.1s early" start near t=0 goes negative and the timeline clamps it to 0 -
  the word shows in frame 1 and the seam fails). Exits done by dur - 0.08.
- Springs: sp(response, damping) from the scene-starter for every arrival - back.* / elastic are BANNED. Pulses
  never above scale 1.1.
- ICONS = SOLAR only (references/icons-solar.html: bold-duotone hero, linear chrome) - never Lucide/Phosphor.
- Colour = meaning: <the film's code>. Coloured TEXT uses the -ink token (contrast). Colour per WORD span, never a
  whole line. Exact strings from the blocks; basic English on screen.
- Never invent a number, name or relation. Use only what the blocks and references give; report what is missing.
- Quality bar: would this frame sit on an Apple product page? Big tight Geist type, air, glass, soft long shadows.
  UI windows sized to fill the stage and centred vertically (no dead band under the headline).
- NO EMPTY STAGE: from ~0.5s to the exit the stage holds a picture. If the block's first object lands late (a
  headline-only opening), bring a supporting picture forward on an earlier word. Content centred on stage y ~610 -
  never all in y 300-700 with the lower half bare.
- Text floors at contact-sheet scale: chips/labels 52px+, card titles 48px, sublines 34px+, tags 36px. Filled
  green chips use dark text (white on the green accent fails contrast).

Seams you must hit exactly (frame.md): <start/end per scene>.

Write compositions/<id>.html and compositions/<id>.html (+ .motion.json each). Test with
`node <ENGINE>/scripts/test-scene.mjs <id> "<t1,t2,...>"` at every beat midpoint plus 0 and dur, read the contact
sheet, iterate until lint has 0 errors, check shows no error or TRAP and the frames match the blocks. Run
`<PY> <ENGINE>/scripts/fromto-scan.py compositions/<id>.html ...` (0 hits). Report briefly: files, lint + check,
contact sheet paths, leftmost x at push peaks, anything not done.
```

For a PORTRAIT port the prompt says PORT (start from `references/src-16x9/<id>.html`, keep copy/beats/cues/colours/
icons/seam poses, re-author layout + camera only) and carries the portrait zone law instead (SKILL.md).

## Review (main session)

- Snapshot each scene's MIDDLES yourself (`test-scene.mjs <id> "<t...>"`, then read the sheet) - workers' last
  sheets often show only the seams. Judge readability at contact-sheet scale.
- First-pass misses seen so far: tiny text + empty stage (ask for sizes in px and lane x positions); UI windows
  small and low with dead stage space (ask for window size + vertical centre); an empty "tray" pill; a card
  sitting empty before its words; receding cards peeking over the new subject (fade them fully); a stamp drawn
  UNDER labels (z-order); an object cut by the frame edge during a push; an empty UI pushed into (fill the beat
  with real content before the push); a headline coloured as a whole line instead of one word; a bare stage
  between two beats (the old object exits fully before the new one starts - overlap them ~0.3s, the old one
  receding toward its own side); a blank phone or browser screen while the voice sets up (skeleton rows + shimmer +
  a status line); a phone screen slide that leaks the outgoing screen's text beside the bezel (clip the screen
  container and fade the outgoing screen).
- The harness has NO presenter: zone violations only show in the assembled film - run `frames.py --zone` on the
  render at every ZOOM peak before you call it done.
