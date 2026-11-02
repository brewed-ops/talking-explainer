# Phase 0 - The script, in the speaker's own voice

Load before writing any script this skill narrates. **The speaker's own style lives in the profile's `voice.md`
(`<profile>/voice.md`) - read it before writing a line, and write in that voice.** It holds their language, pace,
opener and closer, the words they really use and the ones they never say. If it is still the unfilled template,
fill it first (interview, or `scripts/speech-profile.py` on a 5+ minute unscripted recording).
Opener and closer lines come from `voice.md`; the brand name and end-card line come from `brand.json`
(`opener`, `cta`). Never put a word in the speaker's mouth that `voice.md` does not support.

## Claims about AI must be true of TODAY's models

Viewers who use the latest assistants catch a stale claim at once ("every chat starts from zero", "your notes
won't fit"): assistants now have built-in memory and very long context windows. Before any line about what AI
can't do, check it against current models, concede what they now do, then give the reason that still holds -
measured, not assumed (the user's real file size vs the biggest window, built-in memory = short summaries, very
long context = less accurate and slower).

## Newbie-proof without an analogy

For a tech/tool walkthrough, define every jargon word in plain words the first time it is said, right after it
("API key... the secret code your app uses to get in", "provider... the company that runs the model on its
servers", "fallback... meaning a backup"). One short definition, then move on.

Fact-check every mechanism claim against the vendor's own doc page before handing over the script, not against a
summary of it - a plausible guess ("the auto router sends easy prompts to cheap models") is how wrong facts ship.
Log each check in SCRIPT.md's facts block.

## Numbers a viewer can picture

Never say tokens, bytes or exact big counts in the voice. Convert to a unit people know (pages at ~500 words a
page, minutes, "a whole book") and round the rest ("almost nine thousand", "over two hundred"). Keep the exact
figures in SCRIPT.md's facts block, not in the narration.

## Punctuation is direction (ElevenLabs reads it)

- `...` = a trailing pause before a reveal or while listing (~0.5-1s on Multilingual v2 / v3 / v4).
- `?` = questions and check-ins to the viewer.
- **Never `!`** - it makes the take sound excited and salesy. Periods everywhere else, including greetings,
  interjections and the closer.
- Short sentences. A sentence that needs a breath in the middle gets a comma where the speaker would pause.
- No `<break>` tags unless one beat truly needs it - punctuation already carries the pauses, and many breaks on
  Multilingual v2 cause artifacts.
- Spell things the way they should be SAID: "N-eight-N" not "n8n", "four-oh-four" not "404", "A-P-I" only if the
  speaker spells it. Keep terms the speaker says in English in English - the model reads them cleaner than a
  translated version.

## Shape for an explainer

1. Opener + topic (one line, the speaker's own opener). 2. The question people ask. 3. ONE everyday analogy a
non-technical viewer already lives (parcel tracking, a rider's text, a restaurant order) - told literally, because
every sentence becomes a picture. 4. "So in short..." one-line contrast. 5. The real-tool example. 6. The
takeaway (which one, when). 7. Closer (the speaker's own closer).
Each paragraph = one scene; write paragraphs so each NAMES the thing the scene will show.

## Word count -> length

Length = words / the speaker's pace (wpm in `voice.md`; assume ~140 if unmeasured) at speed 1.0. ~180-210 words
= ~85-90s at 140 wpm; ~100 words = ~45s. Save the script as `<film>/SCRIPT.md` (sections: Script / Scene map /
ElevenLabs settings) and count the Script section only (Node or Python one-liner: split on whitespace between the
`## Script` and `## Scene` headings). A first draft usually lands ~15% long - trim it. Hyphenated spoken numbers
("four-oh-four") count as 1 word but speak as 3, so aim low on number-heavy topics. For a shorter cut drop the
second example, not the analogy.

## ElevenLabs settings (starting point, not A/B-locked)

Model Multilingual v2 (v3 / v4 when the speaker's voice supports it), speed 1.0 (1.1 to fit a short cut),
stability 0.50, similarity 0.75-0.80, style 0.0-0.15, speaker boost on. Robotic -> stability -0.05;
mispronunciations or a question-lilt on statements -> stability +0.05 (max 0.6). Encode the settings in the take's
filename (e.g. `_sp100_s50_sb75`) so a good take can be reproduced.

## Chunking

Generate long scripts in 2-3 chunks split at paragraph breaks, or one take if the tone holds. Ask for ONE mp3 of
the whole script: join chunks before transcribing so the word timings are one continuous timeline. Re-listen to
the join points - the energy should not reset.

## Language

The speaker's language (English, Taglish, other) is set in `voice.md` and `brand.json` `language`. Pass the
matching `--lang` code to `transcribe.py`. Mixed-language speakers: write the mix exactly as they would say it,
and keep their English terms in English.
