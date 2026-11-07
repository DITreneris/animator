# Payday Slot Machine

A 19-second vertical video (1080×1920, 30 fps) based on the "Choose your career" pay meme. Each career gets a slot machine whose four reels spin out four months of income.

| Time | Beat |
|---|---|
| 0–1.25 s | "CHOOSE / YOUR / CAREER" slams in word by word, then moves to the top |
| 1.25–4.3 s | **Employee**, "same. every. month.": reels stop evenly on $3k ×4 to identical beeps |
| 4.3–7.4 s | **Freelancer**, "invoice is 'in process'": reels stop unevenly on $900, $1.5k, $500, $2k |
| 7.4–12.2 s | **Founder**, "trust the vision": $0, $0, $0, a heartbeat, then a $600k jackpot with rays, falling coins, screen shake and sunglasses |
| 12.2–16.2 s | **Vibe Coder**, "this is the one": −$200 ×4 in red, each with confetti while he keeps cheering |
| 16.2–19 s | "ONE PROMPT AWAY FROM REVENUE." over the cheering coder, with −$200 scrolling across the bottom; party horn, then a sad trombone |

Each finished machine folds into a summary row, so all four results stay visible. The characters are original drawings in a similar crude style, not the meme's artwork. The figures are the meme's joke numbers, not real earnings data.

## Build

```bash
./build.sh            # set JOBS=4 to render more scenes in parallel
```

Output: `Payday_Slot_Machine.mp4`, 570 frames, about −14.3 LUFS integrated, true peak about −2.1 dBTP. The encoder thread count is fixed, so rebuilds are byte-identical whatever `JOBS` is.

Check single frames (times in seconds) before a full render:

```bash
python3 render.py check 3.8 10.7 14.8     # writes check/t03.80.png …
```

## Files

- `plan.json`: scene times, each career's reel values, stop times and colors, and the end line
- `render.py`: Pillow frame renderer and NumPy sound synthesis (`check T…`, `scene ID…`, `audio`)
- `build.sh`: soundtrack, loudness normalization, parallel scene renders and mux

## Known issues

- The founder's final reel shows "$600k" about 0.2 s before the jackpot hits at 10.9 s, so the reveal is slightly spoiled. Holding it out of view until it lands would fix it.
- Coins briefly cover the title during the jackpot.
- Comedic timing and the synthesized sound haven't been reviewed by a viewer yet.
- This version uses the repo's copy of Anton, which differs from the font the first render used, so text is fitted to the frame width and sizes differ by a few pixels from that render.
