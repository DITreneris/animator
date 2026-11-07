# The List

A 17-second vertical video (1080×1920, 30 fps) based on the "Wait, you guys are getting paid?" meme. One screen fills in row by row, and the vibe coder is the only one who pays to work. It reworks [`payday-slam/`](../payday-slam/) in a hand-drawn doodle style, with recorded voice lines.

| Time | Beat | Voice |
|---|---|---|
| 0–1.5 s | "WHO GETS PAID?" The coder fills most of the screen, grinning, laptop on fire | — |
| 1.5–3.5 s | **Employee +$3k**: a money bag lands, his face never changes | "mm." |
| 3.5–5.5 s | **Freelancer +$900**: coins bonk her head, the smile stays | "ow…" |
| 5.5–8 s | **Founder $0 → $0 → $0**: tears grow on three sad notes | — |
| 8–9 s | A money truck crashes into the row with **+$600k** | "I'm okay" |
| 9–10.5 s | **Vibe coder −$200 ×4** on sad trombone notes, then "on AI tools" | "Here's my money!" |
| 10.5–15.5 s | Silence, he looks up, eyes pop, jaw drops, caption word by word | "Wait… you guys are getting paid?" |
| 15.5–17 s | Grin returns, `promptanatomy.app` | "Thanks!" |

The coder starts huge and shrinks in quick steps as each row arrives, as if the list were pushing him down.

## Build

```bash
./build.sh                 # writes The_List.mp4
node render.js still       # writes The_List_Still.png (the one-image test)
node render.js check 0 130 152   # single poses → check/p000.jpg …
```

Needs Node with `playwright` (and its Chromium), Python 3 with NumPy and SciPy, and ffmpeg. A full build takes about 30 s and reproduces the released video exactly (frames and audio).

Output: `The_List.mp4`, 510 frames, −14.7 LUFS integrated, peak −1.9 dBFS.

## Files

- `page.html`: the 1080×1920 canvas and the Permanent Marker font (`../fonts/`)
- `lib.js`: drawing library: wobbly ink lines, paper texture, the coder with all his faces (grin, frozen, jaw drop), laptop
- `anim.js`: the animation, 204 poses at 12 poses per second (`window.vframe(n)`), output at 30 fps
- `still.js`: the single still image used to test the joke before animating
- `audio.py`: synthesized tune and effects, the voice clips placed and levelled, music ducked under the voices
- `vo/`: the six voice lines used, trimmed from the original recordings
- `render.js`, `build.sh`: rendering and muxing
- `history/`: earlier stages: the doodle style test, the voiced punchline test, and the storyboard of the multi-shot version that was dropped

## How it got here

1. *Payday Slam*: the meme's table animated. Clear, but 16 numbers and no funny action.
2. *The Payday Line*: a cartoon in one room. Funnier idea, but small faces and mechanical motion.
3. Doodle style with separate shots per character: each gag worked, but viewers lost the story.
4. *The List*: one screen like the original meme, one gag and one number per row, voiced punchline. A tester scored it concept 9/10, execution 7/10.

## Known issues

- The loop is a hard cut: the list resets to empty.
- Flying bills briefly cover "+$600k" when the truck hits.
- The −$200 row is small on a phone.
- The coder is fairly small at the punchline; scaling him back up at the jaw drop is untested.

## Rights

The voice lines are the author's own recordings. Permanent Marker is © Font Diner, under the Apache License 2.0 (`../fonts/PermanentMarker-LICENSE.txt`). All music and effects are synthesized in `audio.py`.
