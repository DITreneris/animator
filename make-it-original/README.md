# Make It Original (Hoodyz ep. 4)

In 1986 his drummer rejects Hoodyz's garage riff: "Play something we know." In 2016 his upload gets 3 views, while his cat walking across the strings plays the same riff and gets 10M. In 2026 he asks his AI for something completely original, rejects it with the drummer's exact line and gesture, and smugly approves the viral cat version: "Now THAT'S original!"

Concept, locked decisions and the viewer test: the "Hoodyz Ep. 4 — Make It Original (concept)" doc in Claude Docs.

## Status (11 Nov)

**Rough, waiting for the viewer test.** Production (camera, full animation, final voices) starts only once the rough passes the test in the concept doc.

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
