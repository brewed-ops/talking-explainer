# Worked example - "REA: Reverse Engineer Anything" (129.0s, 12 scenes, Apple look)

The film this skill was built from. Read it for SHAPE, not content:

| File | What it shows |
|---|---|
| `SCRIPT.md` | A hook-first script: the surprising claim as a question, "<host> here, from <brand>... let's break it down", the topic's NAME in paragraph 2, ONE everyday analogy told literally (a cafe's secret latte recipe), the closer. 12 paragraphs = 12 frames. It is in Taglish (Tagalog + English) because that is how its speaker talks - write in the profile's language. |
| `STORYBOARD.md` | 12 blocks with scene-local cue times, a **ZOOM** and an **EMPH** beat in every block, colour = meaning, one STAGE POSE seam ("LATTE", s03 -> s04), real facts + fictional extras. Written before the icon swap: where it says Lucide, the film now uses Solar (RETIME.md). |
| `RETIME.md` | A NEW take of the same script (the speaker's own recording, ~20% faster) + a new opener + the Solar icon swap, sent to the same workers as per-scene timing notes - a retime, not a rebuild. "This file wins over STORYBOARD.md times." |

For a new film, write `STORYBOARD.src.md` with GLOBAL times (`- start: <global>` per frame, cue words as
`"word"@g<global>`) and let `src/storyboard-local.py` write STORYBOARD.md - see SKILL.md phase 3.
