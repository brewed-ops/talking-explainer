# RETIME - take 2 (the speaker's own ElevenLabs take) - this file WINS over STORYBOARD.md times

The speaker: "the tone and pacing of the voice is not really me... I'll generate the audio" - the new take is 126.43s (film
129.0s), ~20% tighter than take 1. Plus two changes they asked for:
1. **New opener (s01 + s02 rewritten):** "May repo sa GitHub ngayon na kaya daw i-clone kahit anong app. Totoo ba?
   <host> here, from <brand>... let's break it down." / "Ang tawag dito... R-E-A. Reverse Engineer Anything. Isa
   sya sa pinaka-trending na repo sa GitHub ngayon. Mahigit one hundred thousand stars."
2. **ICONS = SOLAR** (https://solar-icons.vercel.app), still the Apple look. Replace EVERY Lucide / hand-drawn icon
   in your scenes with the matching icon from `references/icons-solar.html` (inline SVG, colour via `color:`):
   **bold-duotone** for hero icons (step cards, chips, card icons, badges' glyph area), **linear** for UI chrome
   (search fields, window rows, small marks). The LENS glyph is now Solar's magnifier - copy the new `.ap-lens`
   markup from `references/snippets.html` (APPLE LAYER). Suggested map: search/lens = magnifier; trending =
   graph-up; star = star; lock = lock-keyhole-minimalistic; taste = cup-hot; smell = wind; watch = eye; ask =
   chat-round-dots; evidence = file-search; build = widget-add; learn = book-minimalistic; copy = copy; weeks =
   calendar; minutes = stopwatch. The plain check / X marks inside `.ap-badge` circles may stay as they are.

**Everything else stays as built** (pictures, copy, colours, layout, ZOOM/EMPH beats) - only the timing moves to
the cue words below. Rules unchanged: arrivals start ~0.15s before the cue (spring lands ~0.3s after start), never
before 0.12; exits finish by dur - 0.08; nothing in x < 640 at any time (incl. push peaks); camera legs >= 0.8s,
cam/drift at identity on the first and last frame; canon floor seams except s03 -> s04 (STAGE POSE "LATTE").
Scenes got SHORTER: where two beats now collide, shorten tweens (springs: lower response, e.g. sp(0.4)) rather
than dropping a beat - but if a beat cannot fit, drop the least important EMPH and say so.
Times are SCENE-LOCAL seconds (global word time minus the scene start).

## s01-hook - 7.90s (global 0.00) - NEW CONTENT (the hook)

The voice starts at 0.00, so frame 1 must already be moving (first arrival at 0.12). Stage: a glass pill
`.ap-glass` "GitHub · Trending repo" (graph-up icon, blue) materializes centre stage at ~(1240, 380) on
"repo sa github" @0.30-0.74 (start 0.12). Hero (`.ap-display` ~150px, 2 lines, centred x ~1240):
line 1 "Clone **any app?**" - "Clone" lands on "i-clone" @2.32, "any app?" (orange `--api`: someone else's app) on
"kahit anong app" @2.60-3.14; as "app" lands, a small orange app window (`.ap-window` ~300x200, "App") sits behind
the hero at the right and 3 ghost copies fan out of it (white glass, orange hairline - the s09 look) @3.14-3.5.
**ZOOM** cam glides z +110 toward the hero 2.2-3.4 and home 3.5-4.4.
line 2 "Is it true?" (grey `--reply-lo`, 96px) materializes on "Totoo ba?" @3.92; **EMPH** the "?" pulses @4.10.
Hero, pill and copies leave 4.40-4.80 (power2.in, along their entry path).
Ident: `.kit-logo` (--h ~130px) centred at (1180, 470) materializes on "<host> here" @4.86 (mark scale 0.92 -> 1 +
opacity, sp(0.6)); wordmark wipes in on "from <brand>" @5.52-5.76; under it a 44px line "Let's break it down."
(ink-faint, "break it down." in blue) materializes word by word on "Let's break it down" @6.78-7.40.
Exit 7.45-7.82 (logo group recedes z -200 + fades), cam/drift at identity -> canon floor. The m-brand corner logo
enters at global 8.1 (after this scene).

## s02-trending - 10.40s (global 7.90) - NEW CONTENT (the name, then the repo)

Part 1, the name (take the hero from the old s01: `.ap-display` "REA" ~240px + the LENS beside it + `.ap-sub`):
kicker "It's called" (44px, ink-faint) on "Ang tawag dito" @0.14 (start 0.12); "REA" letters materialize landing on
"R-E-A" @1.28; **EMPH** the lens pops (sp(0.45, 0.75)) @1.50; **ZOOM** cam glides z +120 toward REA 1.2-2.4, home
2.5-3.4; sub words "Reverse" @2.76, "Engineer" @3.30, "Anything" (blue) @3.80.
Hero leaves up/back 4.50-4.90.
Part 2, the repo (the existing repo card + chip + star counter, as built): headline "Top **trending** on GitHub"
on "Isa sya sa pinaka-trending" @5.06-5.50 ("trending" blue); the repo card rises on "repo" @6.56; Trending chip
pops on "github" @6.98; **ZOOM** cam glides z +120 toward the star counter 7.9-8.9; counter ticks 0 -> 100k+ from
"100" @8.46 to "stars" @9.60; **EMPH** number punch-in @9.62; cam home 9.0-9.95 must overlap nothing (start the
return at 9.0 as a separate leg after the push ends at 8.9). DROP the old claim bubbles + big "?" + headlines B/C
(the hook in s01 now says them). Exit 9.95-10.32.

## s03-cafe - 9.95s (global 18.30)
- headline A "Start with coffee." on "Okay" @0.16 (start 0.12); "coffee." on "kape" @1.38
- shopfront rises on "Imagine" @2.20; rating chip on "sikat" @2.82; "Luna Cafe" on "cafe" @3.36; cam drift right on "malapit" @3.58
- headline B on "Yung signature" @4.78-4.96; cup rises on "latte" @5.46 + ZOOM 5.4-6.6; cup pulse on "sobrang" @6.18; "Best seller" chip on "sarap" @6.88
- cam back 6.7-7.6; headline C "The recipe?" on "Pero syempre" @7.52, "Secret." @9.00 (ahead of "recipe" @9.60 - it must clear before the pose)
- recipe card slides in on "hindi nila ibibigay" @8.48; lock shake on "ibibigay" @8.95
- headline + extras gone by 9.87 -> STAGE POSE "LATTE" (unchanged values)

## s04-taste - 10.30s (global 28.25)
- starts on STAGE POSE "LATTE"; headline A "So what do you do?" from 0.12, "do?" on "mo?" @1.21
- "Taste." + ring born + ZOOM on "Titikman" @1.85 (push 1.8-2.8, home 2.9-3.8); "Taste" chip @1.95
- "Smell." + chip on "Aamuyin" @2.81; "Watch." + chip on "Papanoorin" @3.91; (barista @4.71)
- ring glides to the recipe card 4.8-5.5; "2 shots espresso" + punch on "shot" @5.89; "Oat milk" on "gatas" @6.63; ZOOM on the card 5.3-6.3, home 6.4-7.3
- headline C "Bit by bit..." on "Konti-konti" @7.61; "A little vanilla" @7.93; "the recipe." on "mabubuo" @8.73
- ring -> lens badge on the card @8.73; "Recipe - found" on "recipe" @9.51
- exit 9.80-10.22 -> canon floor

## s05-short - 10.10s (global 38.55)
- kicker "In short" on "So in short" from 0.12
- "Reverse" @1.43, "engineering" @1.87 + underline 2.0-2.45; ZOOM push 1.8-2.9, home 3.0-3.9
- sub "How it works -" on "paano gumagana" @3.75, "without" on "kahit" @5.57, "the recipe." on "recipe" @7.01
- hero leaves 7.20-7.60; headline B "Software? No source code." on "Sa software" @7.89
- cards rise 8.0 / 8.3, "=" @8.6; ZOOM on the locked panel 8.2-9.0, home 9.1-9.95; lock pulse on "code" @9.59
- exit 9.70-10.02

## s06-rea - 12.80s (global 48.65)
- headline A on "Ngayon" @0.13; "REA" + marker sweep on "R-E-A" @1.69
- headline B on "Binibigyan" @2.73; terminal rises on "AI agent" @3.55-3.97; "Claude Code" types on @5.05-5.41
- lens + chips on "tools" @6.03, plug in as lines; app window rises + terminal glides aside on "silipin" @6.79
- lens -> ring over the app on "app" @7.59; ZOOM toward the app 7.5-8.5, home 9.3-10.2
- list filters on "gumagalaw" @8.57; trace line + "search() -> filter -> render" on "ginagawa" @9.23-9.69
- headline C + binary layer on "Hanggang sa loob" @10.83-11.27; ZOOM z +80 11.0-11.8, home 11.9-12.70; row pulse on "binary" @12.07
- exit 12.40-12.72

## s07-flow - 11.75s (global 61.45)
- headline A on "Simple" @0.13, "flow." @0.71; dim cards ripple 0.3-0.9
- card 1 lights on "Una" @1.31, icon pulse on "agent" @2.65
- line 1 -> 2 + card 2 on "titignan" @3.25-3.91; lens pulse on "app" @4.47
- line 2 -> 3 + card 3 on "ibabalik" @5.65; evidence sheet lifts on "findings" @6.57 + ZOOM 6.4-7.4; rows 6.8 / 7.1 / 7.4
- headline B "With evidence." on "With evidence" @7.63-7.81; marker on "Proof" @7.95; cam home 7.6-8.5; sheet sinks 8.3-8.8
- headline C on "pwede" @9.55; card 4 green on "i-build" @10.23; "Your app" chip on "feature" @10.55
- ZOOM z +90 toward card 4 9.6-10.5, home 10.6-11.6 (on "para sa'yo" @10.95-11.39)
- exit 11.35-11.67

## s08-notes - 12.30s (global 73.20)
- headline A from 0.12, "real." on "real" @0.74
- Notes rises on "Sabihin" @1.36; headline B on "search" @2.66; "latte" types 2.75-3.25; list filters @3.3; ZOOM 3.3-4.2, home 4.3-5.2 ("Notes app" @3.48-3.80)
- headline C + terminal rises + Notes steps back on "Sasabihin" @4.44; prompt glyph on "agent" @5.30
- line 1 types on "alamin" @6.08 to "search" @7.62; ZOOM on the terminal 6.0-7.0, home 8.6-9.5
- line 2 types on "ipakita" @8.32 to "evidence" @9.02; blue marker on "evidence." @9.10
- line 3 (green) types on "tapos gawan" @9.84 to "app ko" @11.96 - put a green marker sweep on "my app" @11.70 as its EMPH (no pulse after - no room)
- exit 12.00-12.22 (fast power2.in)

## s09-minutes - 9.40s (global 85.50)
- headline A on "Kaya siya sumikat" @0.16-0.50
- "Before" card on "Dati" @1.00; "Weeks" on "linggo" @2.18; calendar flips 2.4 / 2.8 / 3.2; left card dims on "feature" @4.28
- headline B on "Ngayon" @5.06; "Now" card @5.06; "Minutes" on "minuto" @5.98; ring timer 5.8-6.4; pulse on "lang" @6.48; ZOOM 5.5-6.5, home 6.6-7.5
- headline C on "Kaya ang daming" @6.94; cards sink 6.9-7.3; window + clone fan on "nagki-clone" @7.68 (deal 7.7-8.3)
- ripple on "software" @8.58; fold + exit 8.90-9.32

## s10-line - 15.40s (global 94.90)
- headline A on "Pero teka" from 0.12; "This matters." + underline on "importante" @1.28
- headline B + LEFT card on "Yung pag-aaral" @2.32; label on "gumagana" @3.48; green check on "okay yun" @4.46
- headline C + RIGHT card on "kukopyahin" @5.14-5.52; "Copy the whole app" on "buong app" @6.46; "and sell it" on "ibebenta" @7.38-7.92; ZOOM 6.4-7.6
- red X + shake on "ibang usapan" @8.52; cam home 8.8-9.7
- headline D on "Kahit yung REA mismo" @9.76-10.78; cards recede + fade to 0 by 11.10; quote card lands ~11.30 (start 11.10)
- quote words from "sinasabi nila" @11.48 through "sa'yo" @13.86; green sweep "you own" @13.60; "permission" @14.56
- ZOOM toward the quote 11.6-12.6, home 12.7-13.6
- exit 14.95-15.32

## s11-yours - 9.75s (global 110.30)
- cups rise on "Parang sa cafe" from 0.12 (left 0.12, right 0.30)
- headline A on "gayahin" @1.08; dashed line on "lasa" @2.08; green check on "latte" @2.56
- headline B on "Pero hindi" @3.22; sticker lifts + glides on "nakawin" @3.9-4.6 (lands at your cup @4.18); ZOOM 3.9-5.0
- red X + shake on "pangalan" @4.78; sticker drops on "logo" @5.48; cam home 5.1-6.0
- cups dim 5.9-6.2; "Learn the recipe." on "So learn" @6.06, "recipe." blue on "recipe" @7.12
- "Make it yours." on "then make it" @7.84, "yours." green on "yours" @8.48 + pulse @8.52; hero push 7.2-8.1, home 8.3-9.2
- exit 9.35-9.67

## s12-close - 8.95s (global 120.05)
- recap "REA:" on "yan ang REA" landing @1.49 (start ~1.3); "learn how it works." 1.6-1.9; lens pop @2.00; gentle push 1.3-2.2, home 2.3-3.1
- recap leaves 2.40-2.70 (the corner logo leaves at local 2.70)
- big logo 2.80, wordmark 3.05; CTA lands on "follow for more" @3.59-4.07; CTA soft pulse @4.10
- CTA soft pulse on "Thank you" @5.77; HOLD to 8.95 (film end)
