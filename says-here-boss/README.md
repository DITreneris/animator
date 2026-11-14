# Says Here You Were Our Boss

Based on the four-panel "2024 Prompt Engineer → 2027 My Agents Are Hiring" meme. Cold open in 2027: a robot interviewer in gold sunglasses reads his CV, "Says here you used to be our boss?", then a rewind shows how he got there.

| Version | Video | Length | What changed |
|---|---|---|---|
| [`v1/`](v1/) | `says_here_you_were_our_boss.mp4` | 17 s | First build: interview, rewind, 2024 / 2025 / 2026, "HIRED: Prompt Engineer, 12 tokens/hour", "Thank you, sir", "One more thing…" |
| [`v2/`](v2/) | `says_here_v2.mp4` | 15 s | Voiced lines, moving opening (robot slides its shades down), close-up "...YES?", the stolen-sunglasses payoff ("Nice shades, by the way." → "MY SHADES?!"), badge only at the end |
| [`v3/`](v3/) | `says_here_v3.mp4` | 19 s | **Hoodyz episode.** Rebuilt from the concept up: HARV (the AI Hoody trained, now PROF. HARV, PhD, Head of Human Resources) has no record of him; faces carry every beat (no back-of-head shots); the dark-room podcast shot; 9.99 TOKENS / HOUR; HARV never smiles; "I've had these for years." → "THOSE ARE MINE!" → silence and a close-up of the cat's one eye; every key line also written, so it works on mute; Tomas's recorded voice; HOODYZ title bar; stereo master. See [`v3/README.md`](v3/README.md) |

**Planted detail:** in 2026 a tiny robot steals his gold-framed sunglasses; the interviewer is wearing them in the first shot.

## Build

```bash
./v1/build.sh
./v2/build.sh
./v3/build.sh
```

## Voices (v2)

Kokoro, via `kokoro-onnx`. The processed lines are in `v2/vo/`, so a rebuild doesn't need the model; `voices.py` regenerates the raw takes.

| File | Voice | Line |
|---|---|---|
| `v_r1` | bm_george | Says here, you used to be our boss? |
| `v_g1` | am_puck | Yes? |
| `v_g2b` | am_puck | Thank you, sir! (sped up ×1.12) |
| `v_r2b` | bm_george | Nice shades, by the way. (sped up ×1.1) |
| `v_r3` | bm_george | About your experience. |

Robot filter: `asetrate=24000*0.93,aresample=24000,aecho=0.8:0.6:14:0.35,tremolo=f=55:d=0.25,highpass=f=120,acompressor`. Guy: `asetrate=24000*1.1`. Both trimmed with `silenceremove`.

## Known issues (v2)

- Voices are synthetic and were never checked by ear in the session; "Thank you, sir!" is squeezed into 0.5 s.
- The Kokoro model's license hasn't been confirmed for commercial use.
