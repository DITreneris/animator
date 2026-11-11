# Make It Original (Hoodyz ep. 4)

In 1986 his drummer rejects Hoodyz's garage riff: "Play something we know." In 2016 his upload gets 3 views, while his cat walking across the strings plays the same riff and gets 10M. In 2026 he asks his AI for something completely original, rejects it with the drummer's exact line and gesture, and smugly approves the viral cat version: "Now THAT'S original!"

Concept, locked decisions and the viewer test: the "Hoodyz Ep. 4 — Make It Original (concept)" doc in Claude Docs.

## Status (11 Nov)

**Master: `v4/make_it_original_v4.mp4`** (19.9 s, 1080×1920, 30 fps, loops, scratch voices). Waiting for your sign-off, the muted viewer test and your recorded voices.

The story as built: his stadium is a fantasy; the drummer's "Play something we know." cuts to the real garage. In 2016 his post gets 3 views, his cat plays the riff with one lazy paw and gets 10M, and he pictures the cat on his own stage. In 2026 he asks his AI for something completely original, rejects it with the drummer's exact gesture and line, the robot glances at the old cat and plays the cat video, his stadium blooms back ("Now THAT'S original!"), the robot turns to us and the old cat yawns.

| Folder | What it is |
|---|---|
| [`v4/`](v4/) | **The master** (19 shots): `make_it_original_v4.mp4`, `make_it_original_cover.png`, key poses and matched-pair overlays in `keys/`. `./v4/build.sh` rebuilds it |
| [`v3/`](v3/) | Version A, no cat (13 shots, 14.1 s), as a half-resolution timing cut. v4 reuses its shot code for 1986 and 2026 |
| [`v2/`](v2/) | Key poses of the first 17-shot storyboard (history) |
| this folder | The first rough, audio auditions, character sheets, and the shared kit (`kit.py`, `sound.py`, `timeline.py`, `vo/`) |

**Checks on the master:** 598 frames; -14.5 LUFS, peak -3.0 dBFS; no flat frames; captions and key actions clear of TikTok's buttons; both matched pairs (the gesture, the stadium pose) overlay exactly; a clean rebuild from a copy matches the film, cover and key sheet exactly. A separate agent watched it muted and retold the story correctly ("he became the drummer who crushed him"); the defects it found in the recoil shot, the robot's glance and the cat-video insert were fixed. Not checked, needs people: whether it's funny, the sound of the stadium-to-garage cut, the voices.

**Your lines to record** (drop-in replacements for `vo/*.wav`): "Play something we know." (drummer, flat); "Make something completely original."; "Play something we know." (Hoodyz, the drummer's delivery); "Now THAT'S original!"

### Earlier files

| File | What it is |
|---|---|
| `make_it_original_rough.mp4` | The rough: a timed slideshow with light motion, 19.5 s, 1080×1920, loops. Scratch voices |
| `aud/make_it_original_auditions.mp4` | Audio auditions: riffs A–C (1986 guitar, 2016 fragment, cat version), AI tunes T1–T3, effects. WAVs beside it |
| `sheet_cast.png`, `sheet_faces.png` | Character sheets: the cast, the wave-off gesture, the cat, robot faces, props; Hoodyz's expressions by era |

**Picks** (made by Claude, open to override): riff **C** (D F C A G D'), AI tune **T3** (the T2 melody on electric piano), wave-off **B** (a backhand brush outward; the first version read as "hi").

## How it's built

| File | Job |
|---|---|
| `timeline.py` | One source of timing for picture and sound; the riff, the AI tune and every beat |
| `sound.py` | Synthesized instruments and effects: plucked-string guitar with soft clip, paw plucks, meow, electric piano, tape fast-forward, swipe, counter ticks |
| `riffs.py` | Riff candidates and the originality screen against 41 famous riffs and tunes (3+ shared consecutive intervals fails) |
| `kit.py` | The drawing kit: series helpers copied from `whos-a-good-boy/v3`, plus Hoodyz at three ages, the drummer, the cat, the guitar, the cassette, robot faces and the HOODYZ title bar |
| `sheet.py`, `auditions.py`, `mix.py`, `rough.py` | The sheets, the auditions, the soundtrack (with lip-flap envelopes) and the rough |
| `vo/` | Scratch voices (Kokoro: Hoodyz `am_puck`, 1.5 semitones lower in 2026; drummer `am_onyx`). The stress on "THAT'S" is written in phonemes |

```bash
./build.sh
```

A clean rebuild from a copy of the repo reproduces the rough, the auditions and both sheets exactly (decoded video and audio md5, PNG bytes).

## Checks run on the rough

- 584 frames, 30 fps, 1080×1920; -14.4 LUFS, true peak -2.2 dBTP; no flat frames.
- Subtitles, the cat's playing and the 2026 desk kept clear of TikTok's right-hand buttons and caption area; the wave-off hand stays inside the frame in both eras.
- Each guitar take measured against the written notes (within about 20–40 cents; 1986 is detuned on purpose).
- Not checked, needs people: whether it's funny, whether viewers recognise the riff, the voices.
