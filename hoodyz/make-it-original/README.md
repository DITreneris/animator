# Make It Original (Hoodyz ep. 4)

In 1986 his drummer rejects Hoodyz's garage riff: "Play something we know." In 2016 his upload gets 3 views, while his cat plays the same riff with one lazy paw and gets 10M. In 2026 he asks his AI for something completely original, rejects it with the drummer's exact line and gesture, and smugly approves the viral cat version: "Now THAT'S original!"

Concept, locked decisions and the viewer test: the "Hoodyz Ep. 4 — Make It Original (concept)" doc in Claude Docs.

## Status (18 Nov): v5.1

**v5.1** (same file, `v5/make_it_original_v5.mp4`) adds the fixes from the v5 mute test:
- A 6-frame flash cut to the 1986 drummer's wave-off inside his 2026 one, at the same arm phase, with 1986 in the bar and her cymbal under it.
- MY AI's tune drawn as strange glyphs on bright tiles: a spiral, a star, an eye, a zigzag.
- The drummer's take pitched 1.5 semitones down instead of 2.5.
- Years that jump straight to the next era instead of rolling through 2011.

**Checks:**
- QA: -14.1 LUFS, -2.2 dBTP.
- The drummer's line is still heard as "Play something with now". Recognition gives the same with no pitch shift, so it's the delivery of "we know": re-record it with a clear "we KNOW".
- Two new cold viewers both linked him to the drummer this time ("reminds me of the drummer from The Loud").
- Both read the wave as drumming, not as a rejection. Her wave is made with the drumsticks in her hand, so silently it looks like a flourish. Without the caption the rejection doesn't read yet.

## Status (18 Nov): v5, the loop

**New master candidate: `v5/make_it_original_v5.mp4`** (19.9 s, 598 frames, same voices). The office tail is gone. After "Now THAT'S original!" the film ends on frame 0's exact stadium shot. The cat now plays the riff on his stage with one lazy paw and yawns into a big meow, while old Hoody air-guitars in the crowd. The cut lands on young Hoody playing the same riff on the same stage, and the year flips from 2026 to 1986. The caption holds for 1.2 s. `v5/keys/seam.png` shows the last frame beside frame 0. v5 imports v4's shots, and v4's files are unchanged.

**Checks:**
- QA (`hoodyz/qa.py`): -14.1 LUFS, -2.1 dBTP, 598 frames, BT.709.
- Crowd level at the seam: -32.1 dB at the end, -32.8 dB at the start, so there is no gap. In v4 it was -46 dB at the end, then the crowd burst in.
- Speech recognition: the drummer's pitched-down "Play something we know." is heard as "Play something with now". v4 does this too.
- Two cold viewers watched without captions. Both read the loop: "the stage always belonged to the cat". Both missed the 2026 reversal: neither saw that his wave-off is the drummer's, and both asked what the robot made. That is v4 material and is listed for the next pass.

## Status (11 Nov)

**Master: `v4/make_it_original_v4.mp4`** (19.9 s, 1080×1920, 30 fps, loops, **Tomas's recorded voices**). Waiting for your sign-off and the muted viewer test.

Voices: the four recorded lines are in `vo_rec/` (trimmed, gently denoised, with a presence boost at 3.2 kHz and 6 kHz and light compression so they cut through the music; the drummer's line is pitched down 2.5 semitones before the boost, so he sounds like a different person without going dull). The scratch voices stay in `vo/` for the rough and version A.

The story as built: his stadium is a fantasy; the drummer's "Play something we know." cuts to the real garage. In 2016 his post gets 3 views, his cat plays the riff with one lazy paw and gets 10M, and he pictures the cat on his own stage. In 2026 he asks his AI for something completely original, rejects it with the drummer's exact gesture and line, the robot glances at the old cat and plays the cat video, his stadium blooms back ("Now THAT'S original!"), the robot turns to us and the old cat yawns.

| Folder | What it is |
|---|---|
| [`v4/`](v4/) | **The master** (19 shots): `make_it_original_v4.mp4`, `make_it_original_cover.png`, key poses and matched-pair overlays in `keys/`. `./v4/build.sh` rebuilds it |
| [`v3/`](v3/) | Version A, no cat (13 shots, 14.1 s), as a half-resolution timing cut. v4 reuses its shot code for 1986 and 2026 |
| [`v2/`](v2/) | Key poses of the first 17-shot storyboard (history) |
| this folder | The first rough, audio auditions, character sheets, and the shared kit (`kit.py`, `sound.py`, `timeline.py`, `vo/`) |

**Checks on the master:** 598 frames; -14.5 LUFS, peak -3.0 dBFS; no flat frames; captions and key actions clear of TikTok's buttons; both matched pairs (the gesture, the stadium pose) overlay exactly; a clean rebuild from a copy matches the film, cover and key sheet exactly. A separate agent watched it muted and retold the story correctly ("he became the drummer who crushed him"); the defects it found in the recoil shot, the robot's glance and the cat-video insert were fixed. Not checked, needs people: whether it's funny, the sound of the stadium-to-garage cut, the voices.

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
| `kit.py` | The drawing kit: series helpers copied from `whos-a-good-boy/v3`, plus Hoodyz at three ages, the drummer, the cat, the guitar, the cassette, robot faces and the original HOODYZ title bar. The films use `topbar_a` in `v3/cast.py`: ME + MY AI with the Hoodyz badge since 14 Nov |
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
