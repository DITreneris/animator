# Payday Slam

A 17-second vertical video (1080×1920, 30 fps) based on the "Wait, you guys are getting paid?" meme.

| Time | Beat |
|---|---|
| 0–2 s | "WHO / GETS / PAID?" slams in on the beat while money rains down |
| 2–5 s | Employee $3k ×4 (cash register), Freelancer $900 / $1.5k / $500 / $2k (uneven coins) |
| 5–9 s | Music cuts for Founder $0, $0, $0, then a riser builds into a $600K jackpot |
| 9–12 s | Record scratch, the screen turns red, Vibe coder −$200 ×4 on a sad trombone |
| 12–15 s | Crickets, then the coder pops up: "WAIT, YOU GUYS ARE GETTING PAID?" |
| 15–17 s | "TOTAL: −$800" stamp, then "TAG A VIBE CODER" |

## Build

```bash
./build.sh            # set JOBS=4 to render more scenes in parallel
```

Output: `Payday_Slam.mp4`, 510 frames, about −14.6 LUFS integrated, peak about −2.9 dBFS.

## Files

- `plan.json`: rows, values and the frame number of every beat
- `render.py`: frame renderer (`check N…` for still frames, `scene N` for one scene)
- `audio.py`: synthesized soundtrack and sound effects
- `build.sh`: full render, loudness normalization and mux

## Known issues

- The "TOTAL: −$800" stamp covers the Freelancer row during the last 2 seconds.
- The original meme's photo of an actor is replaced with an original cartoon coder, so the meme image isn't needed.
