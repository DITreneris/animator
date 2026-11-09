# Who's a Good Boy?

Built from six "Me and my AI agent" memes, turned into one story with the series' hoodie guy and robot. In 2024 he praises his robot like a puppy; by 2027 the robot is saying it to him. 24 s, opens on "today" (2026) and rewinds.

| Version | Video | What changed |
|---|---|---|
| [`v3/`](v3/) | `whos_a_good_boy_v3_3.mp4` | Final: character polish layer (expressions, robot screen faces, blinks, talking mouths, shadows), a readable title bar, the 2026 TODAY opening, QA fixes for TikTok's caption and button areas |
| [`v3/`](v3/) | `whos_a_good_boy_v3_3_notag.mp4` | Same film with no burned-in promptanatomy.app chip (the payoff stays uncovered) and TODAY moved clear of the right edge |
| [`v3/`](v3/) | `whos_a_good_boy_v3_4.mp4` / `_notag.mp4` | Picture polish (`V34=1`): camera push-ins on the opening, the office and the payoff; a bigger, readable APPROVE button in 2024 with a close-up on his first press; a close-up and white flash when the robot grabs the button; "WHO'S A GOOD BOY?" back on screen over the final image. Same timing and audio |

Earlier versions (rough, v2, v3–v3.2) were reviewed in the session but aren't in the repo; v3.3 contains all of their changes.

## Story

| Year | Beat | Line |
|---|---|---|
| 2026 · TODAY | Hook: his robot drags him along the path | "WAIT!" |
| 2024 | He praises his robot like a puppy | "Who's a good boy?" |
| 2025 | The robot does more and more of his work | |
| 2026 | He approves without reading | "Did you read it?" "Approve." / "…Approve." |
| 2027 | Roles reversed: the heart-eyed robot pats him, ball in his mouth, while the real dog lies on the path | "Who's a good boy?" |

## How it's built

The scenes are in `v9.py` (with shared drawing in `v.py`, `v6.py`, `v8.py`). Later versions are layers that replace drawing functions without touching the scenes, timing or audio:

- `chars.py`: expressions, robot screen faces, blinks, breathing, lip flap from the voice files, shadows
- `titles.py`: title bar and subtitle style
- `today.py`: the 2026 TODAY opening and the 2026 → 2025 → 2024 rewind
- `qafix.py`: per-scene subtitle positions and layout fixes clear of the app's controls
- `polish34.py`: the v3.4 layer (`V34=1`): wraps each scene in a camera move and keeps subtitles and the chip in screen space
- `v10.py`: applies the layers and renders. `NOTAG=1` removes the chip and moves TODAY inside the frame.

`fin14.wav` is the mastered soundtrack (−14 LUFS, stereo) used by both videos; `audio.py` rebuilds the raw mix.

```bash
./v3/build.sh
```
