---
format: 1920x1080
duration: 149.6s
fps: 60
message: "REA lets your AI agent find out how any app works - with evidence - and build it for you. Learn the recipe, then make it yours. Never copy and sell someone else's app."
arc: Ident -> #1 trending, "clone anything?" -> Famous cafe latte -> Taste, smell, watch = the recipe -> In short -> What REA does -> 4-step flow -> Notes search example -> Weeks to minutes -> The line -> Make it yours -> End card
audience: non-technical viewers (VAs, business owners, builders) - basic English on screen, Taglish voice
mode: autonomous
---

# REA - Reverse Engineer Anything (talking explainer, Apple look, Taglish take 1)

## Decisions

- **Format:** 1920x1080, 60fps, 149.6s (146.84s narration + 2.8s held end card). Narration is the clock: every
  reveal lands on a word from `src/timing/vo-words.json`. Times in each block are SCENE-LOCAL seconds.
- **Look:** Apple (apple-design skill) - see frame.md Style. Restraint, Geist display type, glass, springs.
- **Motion:** kinetic headlines that materialize on their words; UI animation for the agent and the apps;
  explainer animation for the cafe story; a **ZOOM** and an **EMPH** beat in every block.
- **The spine = THE LENS** (blue). Born in s04 (tasting), REA's mark in s01, inspects in s06, step 2 in s07,
  closes the film in s12.
- **Colour = meaning (never swap):** ORANGE = theirs (Luna Cafe, its latte, the original app). BLUE = REA + your
  agent + evidence. GREEN = yours / allowed. GREY = hidden / unknown. RED = not allowed only (s10, s11).
- **Presenter:** deadpan mascot overlay (lip-synced). Scenes never draw him; content stays out of x 40-620,
  y 420-1060 at all times. The presenter points/presents right - the thing named sits around x 700-1150 at its cue.
- **Data:** "morluto / rea", "Reverse engineer anything with agents", "100k+ stars", "Trending" - the real repo.
  Luna Cafe, "Your Cafe", Notes (generic app), "Claude Code" (plain text) - everything else fictional.

## Locked

- The user: "use talking-explainer skill. Topic is 'Reverse Engineer Anything github repo' since it's
  now taking a spotlight because of how people cloning softwares. make sure that the design is created with apple
  design skill so it looks sleek and premium looking". Full autonomy.

## Layout zones (frame px; world x/y = frame px minus 960/540 at z 0)

- **Presenter zone** x 40-620, y 420-1060 - never content. **Logo corner** x > 1500, y < 150 (m-brand 7.9-142.25s).
- **Top band** x 640-1460, y 60-190: the headline, centred on x ~1050, in a 2D layer above the rig.
- **Stage** x 640-1860, y 200-1020: the main objects, full width and height.

## Frame 1 - Ident + hook

- duration: 7.7s
- poster: 6.4
- transition_in: canon floor (film start)
- src: compositions/s01-hook.html
- style: BRAND IDENT + kinetic type

`.kit-logo` (--h ~130px) + kicker "explains" (36px, ink-faint) centred at frame (1180, 420). Then the hero:
`.ap-display` "REA" (~240px, ink) centred at frame (1180, 500) with the LENS (`.ap-lens` --s 150px) docked to its
right; under it `.ap-sub` words "Reverse" "Engineer" "Anything" (48px; "Anything" in blue `--wh-ink`).

Beat 1 (0.12-1.40): cam glides down to identity (rotationX -6, y -160 -> 0, 1.6s sine.inOut); logo mark scales
0.9 -> 1 with opacity, `sp(0.6)`, at 0.15; wordmark wipes in (clipPath) at 0.45; "explains" materializes at 0.9.
Beat 2 (1.54-3.40): "today" (1.54) the logo group eases up and back (y -60, z -220, opacity -> 0 by 3.4, sp(0.9)).
Beat 3 (3.63-5.60): "It's all about" (3.63) kicker "It's all about" materializes at frame (1180, 330);
"REA" (5.17) the R-E-A letters materialize one by one (rise y +40, blur 14 -> 0, sp(0.55), stagger 0.08) landing
on 5.17; **ZOOM** cam glides in z +140 toward REA (5.10-6.30, sine.inOut) - **EMPH** the LENS pops in beside it
(scale 0.6 -> 1, `sp(0.45, 0.75)`) at 5.40.
Beat 4 (6.15-7.20): "Reverse" (6.15) "Engineer" (6.59) "Anything" (6.99) the sub words materialize on their words.
Seam out (7.20-7.62): everything leaves (title + sub drift toward camera z +300 with opacity 0, power2.in 0.4s),
cam home to identity -> canon floor by 7.62.

## Frame 2 - Trending: "clone anything?"

- duration: 13.6s
- poster: 6.2
- transition_in: canon floor
- src: compositions/s02-trending.html
- style: UI/UX animation + kinetic type

Stage: a repo card (`.ap-glass`, ~1000x560 authored, Geist): top line "morluto / rea" (44px 700, ink) with a
"Public" chip; description "Reverse engineer anything with agents" (36px, ink-soft); a row: a "Trending" chip
(blue `.kit-chip.wh`, Lucide trending-up) and a star counter "★"-free: Lucide star icon + "100k+" + "stars"
(counter in Geist Mono 64px). Plain text, no GitHub logo.
Headline A: "Top **trending** on GitHub" ("trending" blue). Headline B: "People say: **clone anything.**"
(ink). Headline C: "Is it **true?**" ("true?" grey).

Beat 1 (0.15-2.90): "Ito" (0.15) headline A begins; "trending" (1.13) lands blue; "repo" (2.61) the repo card
rises from y +80 with `sp(0.7)`; its lines materialize top-down (stagger 0.08).
Beat 2 (3.05-6.20): "GitHub" (3.05) the Trending chip pops (sp(0.45, 0.75)); "Mahigit" (4.43) **ZOOM** cam glides
in z +150 toward the star counter (4.35-5.55, sine.inOut); "100" (4.61) the counter ticks 0 -> 100k+ (tl.set per
step: 0, 12k, 31k, 58k, 84k, 100k+ ending at 5.59 on "stars") - **EMPH** number punch-in pulse at 5.62.
Beat 3 (6.29-11.40): cam eases home (6.0-7.0); "ang daming" (7.57) headline B replaces A; the repo card slides back
(z -260, opacity 0.35 on its face); three claim bubbles (`.kit-bubble`, ink text, 40px) deal out across the stage on
their words: "Clone any app." (8.09), "Copy any software." (9.71), "In minutes." (10.71) - each rising with sp(0.55),
slight rotations (-2 / +1.5 / -1 deg) - **ZOOM** a gentle push toward the bubbles (9.6-10.8, z +100).
Beat 4 (11.40-13.40): cam home (11.4-12.4); "Totoo" (12.44) headline C replaces B; **EMPH** the three bubbles go
grey and dim (focus pull, opacity 0.4) while a big grey "?" (Geist 700 ~260px, `--reply`) materializes centre
stage at 12.6 and pulses once at 12.78 ("yun").
Seam out: all leave by 13.52, cam home -> canon floor.

## Frame 3 - The famous cafe

- duration: 11.4s
- poster: 6.4
- transition_in: canon floor
- src: compositions/s03-cafe.html
- style: explainer (everyday picture)

World: an Apple-clean shopfront: a wide `.ap-glass` panel (~1100x560) at the back (world z -200) with a slim ORANGE
awning bar across its top and the name "Luna Cafe" (Geist 700 64px, `--api-ink`) + a "4.9 rating" chip (Lucide
star, ink). In front, centre stage on the floor: THE LATTE CUP - a clean flat illustration (white ceramic cup +
saucer, latte-art heart in the foam drawn with two soft SVG paths in coffee browns, an ORANGE sleeve band with
"Luna" in white Geist 600) ~300px tall, `.kit-shadow` under it; optional `mascot/fx/steam.png` (opacity 0.5)
above it. To the right: the RECIPE CARD (`.ap-glass` ~420x500): title "Recipe" (44px 700) + a Lucide lock icon,
five text lines rendered as GREY rounded bars blurred (`filter: blur(10px)` on each bar leaf) = hidden.
Headline A: "Start with **coffee.**" ("coffee." orange). Headline B: "Their **signature latte**" (orange).
Headline C: "The recipe? **Secret.**" ("Secret." grey).

Beat 1 (0.18-1.60): "Okay" (0.18) headline A begins; "kape" (1.14) "coffee." lands.
Beat 2 (2.18-4.40): "Imagine" (2.18) the shopfront rises from y +60 (sp(0.75)); "sikat" (2.50) the rating chip
pops; "cafe" (2.94) the "Luna Cafe" name materializes; "malapit" (3.16) cam drifts slightly right (x -40, 1.2s).
Beat 3 (4.76-8.30): "Yung" (4.76) headline B replaces A; "latte" (5.58) the cup rises onto the floor centre stage
(sp(0.7)) - **ZOOM** cam glides in z +170 toward the cup (5.55-6.85, sine.inOut); "sobrang sarap" (7.31) **EMPH**
the cup pulses once (1 -> 1.06 -> 1) and a "Best seller" chip (`.kit-chip.api`) pops beside it at 7.59.
Beat 4 (8.47-11.20): cam eases back to identity (8.3-9.3); "Pero syempre" (8.47) headline C replaces B;
"hindi nila ibibigay" (8.95) the recipe card slides in from the right (x +200 -> 0, sp(0.7)); "recipe" (10.29)
**EMPH** the lock icon does one small shake (rotationZ -6 -> 6 -> 0, 0.4s) - the lines stay blurred grey.
Seam out (t = 11.4): STAGE POSE "LATTE" - the cup at its stage-pose transform (centre-left of the stage, e.g. world
x 40, y 170), the recipe card at its pose (world x 520, y 20), the shopfront, chips and headline gone by 11.32,
cam/drift at identity. Defined ONCE here; s04 copies the values verbatim.

## Frame 4 - Taste, smell, watch (the lens is born)

- duration: 12.0s
- poster: 11.4
- transition_in: STAGE POSE "LATTE"
- src: compositions/s04-taste.html
- style: explainer
- spine: THE LENS is born here

Starts on the LATTE pose exactly as s03 left it. Adds: three clue chips (`.kit-chip.wh`, 34px, Lucide icons):
"Taste" (coffee icon), "Smell" (wind icon), "Watch" (eye icon), stacked above/right of the cup; the BIG
inspection ring (`.ap-ring` --s ~340px + handle) and the recipe card's lines turning from blurred grey into real
blue text (Geist 600 36px, `--wh-ink`): "2 shots espresso", "Oat milk", "A little vanilla" (+ two still-grey lines).
Headline A: "So what do you **do?**" (ink). Headline B: "Taste. Smell. Watch." (each word blue, landing on its cue).
Headline C: "Bit by bit... **the recipe.**" ("the recipe." blue).

Beat 1 (0.17-1.40): "So ano" (0.17) headline A materializes; "gagawin mo" (0.91) lands.
Beat 2 (1.47-5.90): "Titikman" (1.47) headline B starts: "Taste." lands; the LENS is born: the inspection ring
grows over the cup (scale 0.6 -> 1, opacity, sp(0.6)) - **ZOOM** cam glides in z +140 toward the cup (1.4-2.7);
the "Taste" chip pops (sp(0.45, 0.75)); "Aamuyin" (3.45) "Smell." lands + its chip; "Papanoorin" (4.79) "Watch."
lands + its chip; "barista" (5.49) cam eases back home (5.0-6.1).
Beat 3 (6.55-9.20): the ring glides from the cup to the recipe card (x/y glide, sine.inOut 0.8s from 6.2);
"shot" (6.75) line 1 un-blurs to "2 shots espresso" (blur 10 -> 0 + grey bar fades to the blue text) - **EMPH**
number punch-in on "2"; "gatas" (7.71) line 2 becomes "Oat milk"; **ZOOM** cam glides in z +120 toward the recipe
card (6.5-7.7) and back (8.4-9.4).
Beat 4 (9.40-11.80): "Konti-konti" (9.40) headline C replaces B; line 3 becomes "A little vanilla" (9.8);
"mabubuo" (10.52) the ring shrinks into the LENS badge (`.ap-lens` --s 96px) docked on the recipe card's corner -
**EMPH** pop `sp(0.45, 0.75)`; "recipe" (11.14) the card's title "Recipe" turns into "Recipe - found" with the lock
icon swapped for the blue lens.
Seam out: all leave by 11.92 (cup sinks back down, card slides right), cam home -> canon floor.

## Frame 5 - In short

- duration: 11.4s
- poster: 9.8
- transition_in: canon floor
- src: compositions/s05-short.html
- style: kinetic type + explainer (the analogy maps)

Kicker "In short" (`.kit-kicker`). Hero: `.ap-display` "Reverse engineering" (~140px, 2 lines allowed, blue
`--wh-ink`) centred at frame (1240, 400); under it `.ap-sub` "How it works - without the recipe." ("recipe" grey).
Then the map: two `.ap-glass` cards side by side, LEFT a small latte cup + a grey locked "Recipe" line, RIGHT an
`.ap-window` (ORANGE accent dot in its bar, title "App") whose body is a GREY locked panel "Source code" (Geist
Mono 34px, Lucide lock, blurred grey lines). Between them a "=" (Geist 700 80px, ink-faint).
Headline B (top band): "Software? **No source code.**" ("No source code." grey).

Beat 1 (0.14-1.20): "So in short" (0.14) the kicker materializes (centred over the hero spot).
Beat 2 (1.79-5.40): "reverse" (1.79) the hero words materialize, "engineering" (2.35) lands - **EMPH** a blue
underline draws under "engineering" (2.5-2.95); "paano gumagana" (4.11) the sub materializes in three groups:
"How it works -" (4.11), "without" (6.35), "the recipe." (7.41, "recipe" grey) - **ZOOM** a slow push z +100
toward the hero (2.2-3.6) and back (4.4-5.4).
Beat 3 (7.41-11.00): the hero shrinks up and fades out (7.6-8.0, power2.in); "Sa software" (7.93) headline B
materializes in the top band; the two map cards rise (left 8.1, right 8.51, sp(0.65)) and the "=" pops at 8.8;
"source code" (10.22-10.64) **ZOOM** cam glides in z +100 toward the RIGHT card's locked panel (9.6-10.5,
sine.inOut) and returns home over 10.5-11.3 (sine.inOut); **EMPH** its lock pulses at 10.64.
Seam out: cards and headline leave 10.9-11.32 (power2.in) -> canon floor.

## Frame 6 - What REA does

- duration: 13.9s
- poster: 12.4
- transition_in: canon floor
- src: compositions/s06-rea.html
- style: UI/UX animation (defines the AGENT TERMINAL look s08 reuses)

Stage: LEFT-centre the AGENT TERMINAL (`.ap-dark`, ~720x520, bar title "Claude Code" plain text, Geist Mono 32px);
RIGHT their APP WINDOW (`.ap-window`, ~600x520, bar title "App", an ORANGE accent: a small orange app-icon square
in its bar, body = a simple list UI: a search field + 4 rows). Between them, three tool chips (`.kit-chip.wh`, 30px)
that plug into the terminal: "Inspect", "Trace", "Evidence". The LENS (`.ap-lens` --s 96px) as REA's mark on the
tool tray.
Headline A: "What **REA** does" ("REA" blue). Headline B: "Tools for your **AI agent**" ("AI agent" blue).
Headline C: "Down to the **binary.**" ("binary." blue).

Beat 1 (0.20-2.60): "Ngayon" (0.20) headline A begins; "R-E-A" (1.68-2.22) "REA" lands blue - **EMPH** marker sweep
(blue) behind "REA" at 2.25.
Beat 2 (2.82-6.40): "Binibigyan" (2.82) headline B replaces A; "AI agent" (3.48-3.94) the terminal rises
(sp(0.7)) and a blinking-free cursor block shows; "Claude Code" (5.02-5.44) the bar title types in (one tl.set per
word) and **EMPH** pulses once.
Beat 3 (6.66-11.10): "tools" (6.66) the lens + three chips deal out (stagger 0.12, sp(0.5)) and slide into the
terminal's left edge as three lines: "+ inspect", "+ trace", "+ evidence" (blue mono); "silipin" (7.26) the app
window rises on the right; "app" (8.04) the LENS glides over to the app window and becomes the inspection ring over
its list; "gumagalaw" (9.22) the app moves under the ring: the search field gets typed "latte" and the list filters
to 1 row (UI behaviour); "ginagawa" (10.44-11.06) a thin blue trace line draws from the app to the terminal and the
terminal prints "search() -> filter -> render" (mono, blue) - **ZOOM** cam glides in z +120 toward the app window
(8.0-9.4) and back (10.2-11.2).
Beat 4 (11.82-13.50): "Hanggang sa loob" (11.82) headline C replaces B; the app window's face slides forward and
a DARK binary layer (`.ap-dark`, same size) appears BEHIND-through it: rows of Geist Mono hex/assembly in
`#A1A1A6` ("0x1A4F  mov rax, [rbp-8]", "0x1A53  call search_index", "0x1A58  test eax, eax") with the middle row
highlighted blue; "binary" (12.92) **ZOOM** cam glides in z +80 toward the binary layer (12.0-13.0, sine.inOut)
and returns home over 13.0-13.82 (sine.inOut) + **EMPH** the highlighted row pulses at 12.95.
Seam out: all leave by 13.82 -> canon floor.

## Frame 7 - The flow (4 steps)

- duration: 15.25s
- poster: 14.4
- transition_in: canon floor
- src: compositions/s07-flow.html
- style: explainer (Apple keynote step cards)

Four `.ap-glass` step cards in one row across the stage (each ~270x360, gap 26, row centred on x ~1250, y ~600):
1 "Ask" (Lucide message-circle, blue), 2 "Inspect" (the LENS badge), 3 "Evidence" (Lucide file-search, blue),
4 "Build" (Lucide hammer, GREEN - yours). Each: number in `.kit-kicker` ("1".."4"), icon 72px, label 44px 700.
A thin blue progress line (4px, round) runs under the row and draws from card to card as each lights.
Then an EVIDENCE sheet (`.ap-glass` ~760x420) lifts out of card 3: rows with blue lens bullets: "Found: search
index", "Where: 3 places in the app", "Proof: code + screenshots" (Geist 34px).
Headline A: "Simple **flow.**" (ink). Headline B: "With **evidence.**" ("evidence." blue).
Headline C: "Then it **builds** it for you." ("builds" green).

Beat 1 (0.22-1.60): "Simple" (0.22) headline A; "flow" (0.82) lands. The four cards rise dim (opacity 0.35 on
their faces) in a soft ripple (0.9-1.6, stagger 0.1, sp(0.7)).
Beat 2 (2.06-6.40): "Una" (2.06) card 1 lights (face opacity 1 + scale 1.04 settle, sp(0.5)); "agent" (3.06) its
icon pulses; "Tapos titignan" (4.06-4.48) the line draws 1 -> 2, card 2 lights; "app" (5.12) the lens pulses.
Beat 3 (6.42-10.70): "ibabalik" (7.28) line draws 2 -> 3, card 3 lights; "findings" (8.24) the evidence sheet
lifts out of card 3 toward the camera (z +120, sp(0.7)) while the row dims (focus pull) - **ZOOM** cam glides in
z +120 toward the sheet (8.1-9.3); its rows materialize (8.4, 8.7, 9.0); "with evidence" (9.10-10.18) headline B
replaces A, **EMPH** marker sweep (blue) under "Proof: code + screenshots" at 10.2.
Beat 4 (10.84-14.80): cam eases home (10.6-11.7); the sheet sinks back into card 3 (11.0-11.6), the row un-dims;
"pwede" (12.34) headline C replaces B; "i-build" (13.02) line draws 3 -> 4 and card 4 lights GREEN - **EMPH** pop
(sp(0.45, 0.75)); "feature" (13.34) a small green "Your app" chip pops under card 4; "para sa yo" (13.74) **ZOOM** a
gentle push z +90 toward card 4 (13.6-14.7) then hold.
Seam out: cam home + all leave by 15.17 (return the push over 14.7-15.15, it is small).

## Frame 8 - A real example: Notes search

- duration: 13.25s
- poster: 12.6
- transition_in: canon floor
- src: compositions/s08-notes.html
- style: UI/UX animation (agent terminal look = s06, same worker)

Stage: RIGHT their app: an `.ap-window` "Notes" (~620x560, ORANGE accent square in the bar), sidebar-free: a
search field (rounded, Lucide search) + 5 note rows ("Latte recipe ideas", "Grocery list", "Meeting notes",
"Latte art practice", "Trip plan", Geist 30px). LEFT-centre the AGENT TERMINAL (`.ap-dark` as in s06, ~740x440,
"Claude Code") where the user's request types in three lines:
"1. How does search work?" / "2. Show me the evidence." / "3. Build this in my app." (line 3 in GREEN `--ok`).
Headline A: "Let's make it **real.**" (ink). Headline B: "You want: **Notes search**" ("Notes search" orange).
Headline C: "Just **ask** your agent." ("ask" blue).

Beat 1 (0.19-1.60): "So gawin" (0.19) headline A; "real" (0.87) lands.
Beat 2 (1.79-5.20): "Sabihin natin" (1.79) the Notes window rises on the right (sp(0.7)); "search" (2.77) headline
B replaces A; the search field focuses (soft blue ring) and "latte" types (tl.set per character 2.9-3.5); the list
filters to the two latte rows (others fade + collapse via y/opacity, never height); "Notes app" (3.79-4.13) **ZOOM**
cam glides in z +120 toward the window (3.6-4.8) and back (4.9-5.9).
Beat 3 (5.47-10.40): "Sasabihin" (5.47) headline C replaces B; the terminal rises left-centre (it must stay right
of x 640 - window shifts right/back to make room); "agent" (6.21) a prompt glyph shows; "alamin mo" (7.17) line 1
types word by word to 8.55 ("search"); **ZOOM** cam glides in z +110 toward the terminal (7.1-8.3) and back
(9.8-10.9); "ipakita" (9.01) line 2 types to 9.61 ("ebidensya") - **EMPH** blue marker sweep behind "evidence."
at 9.7.
Beat 4 (11.07-13.00): "tapos gawan" (11.07) line 3 types in green to 12.69 ("app ko") - **EMPH** "my app" pulses
at 12.75.
Seam out: all leave by 13.17 -> canon floor.

## Frame 9 - Weeks to minutes

- duration: 12.5s
- poster: 9.6
- transition_in: canon floor
- src: compositions/s09-minutes.html
- style: kinetic type (Apple keynote stat) + explainer

Two keynote stats side by side on the stage (each an `.ap-glass` ~520x420): LEFT kicker "Before" + `.ap-display`
"Weeks" (~150px, ink-faint) with a small calendar (Lucide) whose pages flip (3 tl.set swaps); RIGHT kicker "Now" +
`.ap-display` "Minutes" (~150px, blue) with a thin blue ring timer that draws once around a Lucide timer icon.
Then the cloning picture: the right stat sinks back and one ORANGE app window (`.ap-window` small, ~360x260,
"App") stands centre-right; ghost copies of it (outline-only, ink 30% hairline, empty) deal out behind it in a
fan (5 copies).
Headline A: "Why it got **big**" (ink). Headline B: "Weeks -> **minutes**" ("minutes" blue). Headline C:
"So people **clone** software." (ink).

Beat 1 (0.20-1.80): "Kaya sya sumikat" (0.20-0.50) headline A materializes.
Beat 2 (2.21-6.60): "Dati" (2.21) the LEFT card rises with "Before"; "linggo" (3.19) "Weeks" materializes and the
calendar pages flip (3.4, 3.8, 4.2); "feature" (5.63) the left card dims (opacity 0.45 on its face).
Beat 3 (7.15-9.40): "ngayon" (7.15) headline B replaces A; the RIGHT card rises with "Now"; "minuto" (8.79)
"Minutes" lands blue - **EMPH** the ring timer draws (8.6-9.3) and "Minutes" pulses at 9.21 ("lang"); **ZOOM** cam
glides in z +150 toward the right card (8.5-9.7).
Beat 4 (9.29-12.10): cam eases home (9.7-10.7); "Kaya ang daming" (9.29) headline C replaces B; both cards sink
back (z -300, fade); "nagki-clone" (9.97) the orange app window rises centre-right and its ghost copies fan out
behind it (stagger 0.1, sp(0.6), 10.1-10.7); "software" (11.75) **EMPH** focus pull: the copies brighten one by one
(opacity 0.5 -> 1 ripple) - a lot of copies.
Seam out: all leave by 12.42 -> canon floor.

## Frame 10 - The line

- duration: 17.12s
- poster: 9.9
- transition_in: canon floor
- src: compositions/s10-line.html
- style: explainer + UI (README quote)

Stage: two `.ap-glass` cards side by side (each ~520x520): LEFT GREEN "Learn how it works" (Lucide book-open,
green) with an `.ap-badge.ok` check; RIGHT RED "Copy the whole app" + second line "and sell it" (Lucide copy) with
an `.ap-badge.bad` X. Later a README QUOTE card (`.ap-glass`, ~1000x360): kicker "REA's own README" + quote (Geist
600 44px, ink): "Only for software you own - or have permission for." with "you own" and "permission" swept GREEN.
Headline A: "Wait. **This matters.**" ("This matters." ink-soft). Headline B: "Learn it: **okay.**" ("okay." green).
Headline C: "Copy and sell: **not okay.**" ("not okay." red). Headline D: "Even REA **says so.**" ("says so." blue).

Beat 1 (0.17-2.00): "Pero teka" (0.17-0.31) headline A begins; "importante" (1.37) lands - **EMPH** underline draw
(ink) under "This matters." at 1.45.
Beat 2 (2.95-5.20): "Yung pag-aaral" (2.95) headline B replaces A; the LEFT card rises (sp(0.7)); "gumagana"
(3.97) its label materializes; "okay yun" (4.61-4.83) the green check pops (sp(0.45, 0.75)) - **EMPH** pop.
Beat 3 (5.51-10.70): "Pero yung kukopyahin" (5.51-5.97) headline C replaces B; the RIGHT card rises; "buong app"
(6.93) "Copy the whole app" materializes; "ibebenta mo" (8.51) "and sell it" materializes - **ZOOM** cam glides in
z +130 toward the right card (7.6-8.9); "Ibang usapan" (9.86) the red X pops + **EMPH** shake (the card,
rotationZ -2 -> 2 -> 0) at 10.0; cam eases home (9.6-10.7).
Beat 4 (10.86-16.60): "Kahit yung R-E-A mismo" (10.86-11.92) headline D replaces C; both cards slide back and dim
(z -300, face opacity 0.35); the README quote card rises in front (sp(0.75)) at 11.3; "sinasabi nila" (12.80) the
quote materializes word-group by word-group to 15.93; "software na sa'yo" (15.21-15.93) **EMPH** green marker
sweep behind "you own" at 15.7; "permiso" (16.35) green sweep behind "permission" at 16.35 - **ZOOM** cam glides
in z +100 toward the quote (13.0-14.4) and back (14.6-15.7).
Seam out: all leave 16.70-17.04 (quote + dim cards fade, power2.in) -> canon floor (cam already home).

## Frame 11 - Make it yours

- duration: 11.43s
- poster: 10.6
- transition_in: canon floor
- src: compositions/s11-yours.html
- style: explainer + kinetic type (the cafe callback)

Two latte cups on the floor (the SAME cup illustration as s03 - copy its markup from compositions/s03-cafe.html):
LEFT their cup (ORANGE sleeve "Luna"), RIGHT your cup (GREEN sleeve, "Yours" in white). A "Same taste" dashed line
draws between them with an `.ap-badge.ok` check. Then a "Luna" logo sticker (orange rounded label) flies from the
left cup toward the right cup and gets an `.ap-badge.bad` X and falls away.
Headline A: "Copy the **taste.**" ("taste." green). Headline B: "Not their **name or logo.**" ("name or logo." red).
Hero (centre-right, replaces headlines): `.ap-display` two lines "Learn the **recipe.**" (blue) / "Make it
**yours.**" (green) ~120px.

Beat 1 (0.12-3.60): "parang sa cafe" (0.12-0.51) the two cups rise (left 0.15, right 0.35, sp(0.7));
"gayahin" (1.86) headline A; "lasa" (2.72) the dashed line draws between the cups; "latte" (3.20) the green check
pops on it (sp(0.45, 0.75)).
Beat 2 (4.10-7.00): "Pero hindi" (4.10) headline B replaces A; "nakawin" (5.46) the "Luna" sticker lifts off the
left cup and glides toward the right cup (5.0-5.9, arc keyframes) - **ZOOM** cam glides in z +120 toward the right
cup (5.2-6.4); "pangalan" (6.04) the red X pops on the sticker - **EMPH** shake; "logo" (6.62) the sticker drops
away (y +200, opacity 0, power2.in 0.4s); cam eases home (6.4-7.3).
Beat 3 (7.26-11.00): cups slide down/back and dim (7.2-7.6); "So learn the recipe" (7.26-8.54) hero line 1
materializes, "recipe." lands blue on 8.54; "then make it yours" (9.62-10.20) line 2 materializes, "yours." lands
green on 10.20 - **EMPH** pulse on "yours." at 10.25; **ZOOM** a slow push z +90 toward the hero (8.6-9.9) then home
(9.9-10.9); "okay" (10.86) hold.
Seam out: all leave by 11.35 -> canon floor.

## Frame 12 - Recap + end card

- duration: 10.05s
- poster: 9.4
- transition_in: canon floor
- src: compositions/s12-close.html
- style: kinetic type + BRAND IDENT

Recap (hero, Geist 700 ~100px, 2 lines, centred at frame (1220, 480)): "REA: learn **how it works.**" ("how it
works." blue) + the LENS (`.ap-lens` --s 120px) beside it. End card: `.kit-logo` (--h ~150px) centred at frame
(1220, 470) + `.kit-cta` "Follow for more" at (1220, 700).

Beat 1 (0.19-2.40): "So ayun guys" (0.19) recap words begin; "REA" (1.35-1.75) "how it works." lands blue,
**EMPH** the lens pops (sp(0.45, 0.75)) at 1.5 + **ZOOM** gentle cam push-in (z +100, 1.1-2.3) then home (2.3-3.1).
Beat 2 (2.40-2.70): recap leaves up and out (power2.in 0.3s) by 2.70.
Beat 3 (2.75-5.00): the logo materializes (scale 0.92 -> 1 + opacity, sp(0.7)) at 2.80 (the corner logo has left
at 2.70); wordmark wipes in at 3.05; "follow for more" (4.25) the CTA rises (sp(0.6)) landing on 4.83 ("more");
**EMPH** a blue underline draws under it (4.9-5.35).
Beat 4 (5.00-10.05): HOLD the end card; only drift breathes and the CTA does ONE soft pulse at "Thank you" (6.63).
Film ends on it (not a loop).
