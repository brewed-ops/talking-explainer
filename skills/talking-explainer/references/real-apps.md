# Real apps + real logos (a "how your setup works" film)

When the topic is a tool or system the user runs themselves ("how my note-taking setup works", "my content pipeline",
"how I use VS Code + Claude Code"), the film is a WALKTHROUGH of the real thing, not an analogy: folders as seen in
a file explorer, a real file opened, the real pipeline stages, the user's real numbers. One paragraph per step,
15-20 frames, 5 minutes is fine - length follows what the viewer needs. The one-analogy rule stays for concept topics.

## Logos - from the source, never redrawn

| Need | Where it comes from |
|---|---|
| A product's mark | the official SVG on the product's own site (press / brand page, or the site header's `<img>`) |
| A desktop app's icon | the icon inside the local install (Windows: `<install>/resources/app/resources/win32/*.ico`; macOS: `<App>.app/Contents/Resources/*.icns`) -> `ffmpeg -i in.ico -vf scale=256:-1 out.png` |
| Simple monochrome marks | the simple-icons package (`npm pack simple-icons`, `icons/<name>.svg`), filled with the brand colour |
| OS folders / files | Microsoft Fluent UI emoji (`fluentui-emoji` repo, "File folder" 3D/flat) or the OS's own icon, never a generic folder |

Save them in the film's `assets/logos/` and list every file in frame.md's Assets table, with the per-film line that
lifts the "no third-party logos" ban. Logos are trademarks: show them as the real product the narration names,
never as the film's brand and never altered.

## App look - from the app itself

- Electron apps carry their real theme in CSS: extract it (`npx @electron/asar extract-file <app>.asar app.css`)
  and run `<py> <skill>/scripts/app-tokens.py app.css references/apps/<app>-tokens.md --scope body --scope .theme-dark`.
- Native apps (File Explorer, Finder): screenshot the real window once at 100% scale and measure row height,
  icon size, fonts and colours from it.
- Write `references/apps/README.md` - per app: colours (token -> hex), fonts, chrome (title bar, tabs, sidebar
  widths), icon style, and the user's REAL content to show (folder names, file names, counts). Workers build the
  windows from this file, not from memory.

## Privacy list (in that README, before any worker starts)

Name exactly which folders, files and numbers may appear. Client names, people, emails, keys and private paths
never go on screen - collapse those folders or leave them out. Workers get only the safe list.

## Real data as pictures

Turn the user's real data into the picture (a graph export, a folder tree, a word count) with a small script in
the film's `src/` rather than letting a worker draw a "graph" - real structure reads as real, and the numbers are
already right. Count every number from the source BEFORE writing the storyboard; a placeholder you type into a
block is an invented number the worker will faithfully render.
