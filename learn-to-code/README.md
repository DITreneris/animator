# Learn to Code

He learned to code. His robot got the job, then the robots promoted each other. Built from a Reddit research file and a concept doc revised after a tester's review. 25 s, 2024 → 2026, opens and ends "today" under Tower Bridge.

| Video | Ending | Notes |
|---|---|---|
| `learn_to_code_A.mp4` | "They fired you too?" / "Worse. Our AIs promoted each other." | Ending A for the A/B test |
| `learn_to_code_B_v2.mp4` | "Any news on my application?" / "My AI is still talking with your AI." | Ending B with a setup line it can answer, and the robots shown still talking |
| `learn_to_code_B_v3.mp4` | as B v2 | Polish: camera push-ins on the reaction beats, big chat bubbles in 2025, a visible charger, the cable coil after the stamp, a slower tent reveal |
| `learn_to_code_B_v3_notag.mp4` | as B v2 | No burned-in chip, TODAY clear of the right edge, and it ends on the board meeting with the punch line on screen instead of looping |
| `learn_to_code_B_v4.mp4` / `_notag.mp4` | as B v2 | Rewatch twist: the job site that rejects him has his own robot's face as its logo (JOBS), the app his robot launched in 2024. Motion pass (wind-up and overshoot, the robot hops onto the pad, the pigeon lands, a white flash on each stamp), a hard cut-in on "You're hired!" |

## Story

| Time | Year | Beat |
|---|---|---|
| 0–3 s | 2026 · TODAY | Under Tower Bridge, application #847: REJECTED. A pigeon lands. "I learned to code for THIS?" |
| 3–3.5 s | | Rewind |
| 3.5–7 s | 2024 | He types "Hello Wor…" while his robot finishes a whole app. "Done!" |
| 7–14 s | 2025 | Interview with the head of hiring: "My AI will answer." The robots chat. "You're hired!" "And me?" "You're the charger guy." |
| 14–18 s | 2026 | He trails his robot holding the cable; it steps onto a wireless pad. POSITION ELIMINATED |
| 18–25 s | 2026 · TODAY | The next tent opens: the former head of hiring. Ending A or B, then a tilt up to the two robots' board meeting on top of the bridge |

Planted for rewatches: the "HEAD OF HIRING" sign on the next tent is visible from the first frame, and in v4 the job site's logo is his own robot's face.

## How it's built

`ltc.py` draws every scene and reuses the series' characters and title bar (`chars.py`, `titles.py`, `v*.py`). Variants are environment switches, so the scenes a version doesn't change are rendered once and shared:

- `ENDING=A` or `ENDING=B2`: which ending (the old B, "They fired you too?" / "My AI is still talking…", is `ENDING=B`)
- `POLISH=1`: push-ins and the other polish
- `NOTAG=1`: no chip, TODAY inside the frame, ends on the board meeting
- `V4=1`: the JOBS logo twist, motion pass and interview cut-in

`audio.py` synthesizes the music and effects and places the voice lines; `master.sh` masters to −14 LUFS stereo. Voices are Kokoro (`am_puck` for him, `bf_emma` for her); `vo/voices.py` regenerates them.

```bash
./build.sh
```
