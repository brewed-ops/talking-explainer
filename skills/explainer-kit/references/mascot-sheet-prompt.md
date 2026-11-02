# Making a TALKING mascot (3 image prompts -> cut -> blink + mouth fit)

Use when the user wants their own character to present and talk. Generate THREE sheets in the SAME image chat
(ChatGPT image generation works well) with the reference image of the character attached to the first message -
one giant sheet (24+ cells) drops quality and drifts the face.

Why each rule exists (all hit cutting real sheets):
- Solid flat white background, never a "transparent" checkerboard - the model paints the checker as pixels.
- No labels or text - labels sit inside the face boxes and break the cut.
- Same character height + head size in every cell - pose swaps pop if scale changes between sprites.
- Gutters between cells - touching sprites merge during auto-detection.
- The slot ORDER matches `NAMES` in `cut-sheet.py` (9 poses, 16 faces = 10 expressions + 6 mouths, 5 fx), so the
  presenter track keeps working. Rows 3-4 of the face sheet are the mouth shapes the lip sync is built from.

Before sending, replace the KEEP IDENTICAL paragraph with the user's character (style, line, colours, hair,
glasses, clothes, build, personality). The text below is the bundled deadpan demo's description - an example.

After generating (proven on the deadpan demo - all 3 sheets came out right first try):
```
<py> <skill>/scripts/cut-sheet.py --poses poses.png --faces faces.png --fx fx.png <home>/profile/mascot-talking
<py> <engine>/scripts/blink-fit.py <home>/profile/mascot-talking --band 0.36,0.57
<py> <skill>/scripts/mouth-fit.py <home>/profile/mascot-talking --band 0.36,0.57
```
Read `_review.png`, `_blink-review.png`, `_mouth-review.png` before using it: every sprite clean on both grounds,
eyes closed on blinks, mouths sitting on the face with matching skin. A different face shape may need another
`--band` (eye band as fractions of the face height) - re-run blink-fit AND mouth-fit with the same value.

## Prompt 1 - pose sheet (attach the reference image)

```
Using the attached character as the exact reference, create a character pose sheet for an animated explainer video.

KEEP IDENTICAL TO THE REFERENCE: hand-drawn cartoon style, slightly rough black ink outlines with the same line weight, flat colors with one soft shadow tone, messy dark brown-black hair, clear thin-frame round glasses, warm tan skin, small dot nose, half-lidded deadpan eyes, beige crew-neck t-shirt, chubby rounded build. Same proportions, same face, same colors in every cell. He is calm and dry-humored, never hyper or cartoon-excited.

Full body. Add plain dark charcoal pants and simple white sneakers in the same flat style.

LAYOUT: a 3x3 grid, 9 poses, square image. Every pose the same scale: same character height and same head size in every cell, feet on the same baseline. Wide empty gutters between cells, nothing touching or overlapping. Front-facing or slight three-quarter.

POSES (left to right, top to bottom):
1. Idle - standing relaxed, arms at sides, neutral deadpan face
2. Wave - one hand raised, small friendly wave, slight smile
3. Point - arm extended pointing to the side, explaining something
4. Thumbs up - one thumbs up, small satisfied smirk
5. Celebrate - both fists up, mild proud grin (understated, not screaming)
6. Walk - mid-stride walking to the side
7. Think - hand on chin, eyes looking up, pondering
8. Sit - sitting on an invisible seat, relaxed, legs bent
9. Present - one open palm held out to the side like presenting a slide, other hand relaxed

BACKGROUND: solid flat pure white (#FFFFFF) across the whole image. No checkerboard, no transparency pattern, no floor, no cast shadows, no gradient.

NO text, labels, numbers, titles, borders, or frames anywhere in the image.
```

## Prompt 2 - faces + mouths (same chat)

```
Same character, same style. Now a head-and-shoulders expression sheet: a 4x4 grid, 16 heads, square image. Every head the same size and same angle (front-facing), same position in its cell, wide gutters, nothing touching.

Keep his deadpan personality - expressions are subtle and dry, not exaggerated anime.

Row 1-2, expressions with mouth closed or natural:
1. Neutral (half-lidded deadpan, like the reference)
2. Blink (eyes fully closed, otherwise identical to Neutral)
3. Happy (small closed-mouth smile)
4. Wide (eyes open wider, surprised)
5. Thinking (eyes looking up and to the side)
6. Focused (eyes narrowed, determined)
7. Wink (one eye closed, slight smirk)
8. Concerned (brows tilted up, small frown)
9. Sleepy (eyes almost shut, droopy)
10. Sparkle (eyes bright, impressed, small open smile)

Row 3-4, talking mouth shapes - all with the Neutral face, ONLY the mouth changes:
11. Mouth closed (M, B, P)
12. Mouth slightly open (rest between words)
13. Mouth open (A)
14. Mouth wide (E, teeth showing)
15. Mouth round (O, U)
16. Top teeth on lower lip (F, V)

Solid flat pure white (#FFFFFF) background, no checkerboard, no shadows. NO text or labels anywhere.
```

## Prompt 3 - effects (same chat)

```
Same hand-drawn ink style and line weight. A row of 5 small effect stickers, landscape image, evenly spaced with wide gaps, nothing touching:
1. Steam - three wavy steam curls (like rising from coffee)
2. Sparkle burst - a small cluster of 4-point sparkles
3. Coffee ring - a loose brown coffee-cup stain ring
4. Question mark - a hand-drawn question mark in a small thought bubble
5. Confetti - a small burst of paper confetti in warm browns, orange and cream

Solid flat pure white (#FFFFFF) background, no checkerboard, no shadows. NO text or labels.
```
