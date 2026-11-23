# Thank You v2 ("He Always Said Thank You")

15.8 s, 1080x1920, 30 fps, a seamless loop. v1 (`../v1`) is imported and untouched.

**The loop is the story.** A firing squad; HARV stops it because Hoody always said thank you; the receipt shows one flagged
night, 3:12 AM, when he yelled at the toaster; the toaster remembers, HARV walks out, and the last frame is frame 0.

- `film.py` - the picture (shots A-K; later blocks override earlier ones: board 2, board 3, polish 1-2, bubbles, safe zones).
- `audio.py`, `master.sh` - mix and master (-14 LUFS). Hoody's lines are Tomas's recordings (`vo/g1-g3.wav`); the toaster is `vo/t1.wav`.
- `safe.py` - every bubble, chat message and the receipt inside the Reels/TikTok/Shorts safe area (x 60-960, y 210-1600) in every frame.
- `measure.py` - prop and character positions per shot (continuity).
- `CONCEPT.md` - idea, protect list, prop timeline, polish log.
- `build.sh` - everything, ending in the safe-zone gate and `../../qa.py`.

Known and kept: the top bar's right edge reaches ~x 1040 (series-wide); the rewind 2037 -> 2028 vs "10 years ago".
