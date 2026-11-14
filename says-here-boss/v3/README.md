# Says Here You Were Our Boss: v3

Hoodyz episode, rebuilt from the v2 experiment to the series standard. 18.97 s, 20 shots, 569 frames, 1080×1920, 30 fps, stereo.

**Logline.** Hoody sits a job interview with HARV, the AI he trained. HARV is now a professor and Head of Human Resources. He's wearing Hoody's sunglasses, and the company has no record that Hoody ever existed.

**The joke in three beats:** the robot takes the sunglasses → the robot innocently claims them ("I've had these for years.") → Hoody explodes ("THOSE ARE MINE!"), nothing happens, and he has to smile again. The last frame matches frame 0, so the interview never ends.

## Shots

| # | Frames | Shot |
|---|---|---|
| 1 | 0–19 | Hoody, forced smile, sweat bead (no text in the first second) |
| 2 | 20–61 | HARV at the desk with Hoody's CV: "Says here you used to be our boss?" (HARV's mouth is flat in every shot: he never smiles) |
| 3 | 62–80 | Hoody: the smile cracks, "…yes." |
| 4–5 | 81–119 | His eyes flick to the shades; insert on the shades with a glint and a sparkle |
| 6 | 120–133 | REWIND |
| 7–9 | 134–235 | Triptych, one framing: 2024 PROMPT ENGINEER / 2025 PROMPT MANAGER / 2026 MENTOR (small HARV) |
| 10–11 | 236–275 | Small HARV takes the shades (YOINK!); Hoody's hand reaches for his empty head |
| 12 | 276–329 | The dark room: Hoody on the sofa with JOBS on his laptop, the cat beside him; on TV, *THE HUMAN TOUCH*, where HARV points at a line labelled HUMANS falling off a cliff |
| 13–15 | 330–399 | Offer letter (9.99 TOKENS / HOUR); eye twitch; crying "Thank you, sir." |
| 16 | 400–455 | HARV adjusts the shades, flat-faced: "I've had these for years." |
| 17 | 456–485 | "THOSE ARE MINE!", the loudest point in the film |
| 18 | 486–501 | Silence. HARV still; the panel turns to look at each other (one tiny beep) |
| 19 | 502–519 | Close on the cat on the desk: she opens one eye at him, the only one who heard |
| 20 | 520–568 | The forced smile returns: "About your experience." → loop |

## Files

- `render.py`: the shots and the timeline (`python3 render.py frames 0 329` for checks, `video` for the picture)
- `chars.py`: Hoody's new faces, HARV, the nameplate, the cat's one eye, the title bar, the dark room; run it to write `character_sheet.png`
- `kit.py`: a copy of the drawing kit from `make-it-original/` (this folder stands alone)
- `audio.py`: the mix (voices, a bed in the flashback only, effects, the silence after the shout)
- `master.sh`: stereo master by one linear gain plus a peak limiter. The series loudnorm master switched to dynamic mode on this film (loudness range 12.6 LU > 11) and flattened the shout's lead from 11 dB to about 1
- `voices.py`: regenerates HARV's lines (needs `kokoro-onnx`; set `KOKORO_DIR`)
- `cover.py`: `cover.png`, the dark-room frame
- `build.sh`: everything. The master is the build script's output; a second clean build matched it with identical audio and 3 video frames different at about 90 dB PSNR (invisible x264 nondeterminism)

## Voices

| File | Who | Line | Source |
|---|---|---|---|
| `h1` | HARV | Says here, you used to be our boss? | Kokoro |
| `g1` | Hoody | …yes. | Tomas, take 4 of 4 (strongest rise at the end) |
| `g2` | Hoody | Thank you, sir. | Tomas, take 4 of 4 complete takes (0.84 s) |
| `h2` | HARV | I've had these for years. | Kokoro |
| `g3` | Hoody | THOSE ARE MINE! | Tomas, take 1 of 5 (highest pitch and energy) |
| `h3` | HARV | About your experience. | Kokoro |
| `pod` | HARV on the podcast | (wordless) | Kokoro, chopped into shuffled 120 ms pieces and muffled |

**HARV's voice is locked for the series:** Kokoro `bm_george`, speed 1.05, `en-gb`, then `highpass=f=120,lowpass=f=7000,aecho=0.8:0.6:9:0.35` at the HR desk. As the Professor (on the podcast) it's clean George.

**Hoody's chain:** `highpass=f=85, afftdn=nf=-45:tn=1, equalizer=f=3200:t=q:w=1.0:g=5, treble=g=5:f=6000, acompressor`. The shout gets a lighter EQ plus a harder compressor and limiter: crest 10.7 → 7.8 dB, so it can lead the mix.

## Measured

| Check | Result |
|---|---|
| Every line, speech recognition on the final mix | All six correct; the podcast is wordless (shuffled speech) |
| Section levels | Shout −10.7 dB, next loudest −17.3, the silence after it −33.5, the opening interview −20.3 |
| Loudness | −14.7 LUFS, LRA 6.0 LU, true peak −1.8 dBTP |
| Loop, frame 0 vs last | Mean difference 0.3 / 255 |
| Flat frames | None (min std below the bar 24.1) |
| App zones | Clear |
| Fresh-eyes mute test (frames only) | Story, theft, loop and cat all read; "Of everything he lost, he's only angry about the sunglasses" |

## Not measured

Comedy timing, the voice blend and whether the shout feels earned need ears and real viewers. Next: a muted viewer test with five people (does the theft read? is the cat noticed?), then post as a **new upload**, not a replacement of v2.
