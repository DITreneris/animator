# ME + MY AI — Untitled

21.1 s, 1080x1920, 30 fps, loops. `untitled.mp4`, cover `cover.png`. Built by `build.sh`.

Hoody and MY AI walk into the park; MY AI falls for a dog poop ("Be brutally honest." / "A masterpiece! 10/10").
20 minutes earlier, in a modern art museum, Hoody taught it "This is art" three times over brown bronze sculptures
(UNTITLED, TWO FRIENDS, PUDDLE (SELF-PORTRAIT)) on a 120 BPM beat. In the park MY AI matches the shape (MATCH 99% = ART)
and plants its own card, UNTITLED (2026). Eva bags the art. "VANDALISM!" Hoody kicks the card away and they walk on —
into frame 0, where the next one is waiting.

## Files
- `keys.py` — props, sets and the key frames (later sections override earlier ones; the last definition wins).
- `rough.py` — the timeline and the animation, on top of `keys.py` (`python3 rough.py frames F ...` / `video` / `final`).
- `mix.py`, `master.sh` — sound: voices, park, the museum beat, effects; -15 LUFS.
- `vo/` — Hoody: Tomas's takes. MY AI: the locked series voice (Kokoro am_puck, 1.35x). `vo/voices.py` rebuilds them.
- `lines.json`, `cuts.json` — for `../qa.py` (speech recognition per line) and the motion check.

## Checks (19 Nov 2026)
- QA gate: pass (size, 633 frames, BT.709, -15.3 LUFS, -3.1 dBTP, all 6 lines recognised in the mix).
- The poop and the card were measured on every frame: the poop at 904/1700 px in every park shot it is in, the card at
  640/1714 from the plant (shot 11) to the kick (shot 15), and in no frame before or after.
- Cold-viewer mute test (2 viewers, rough 7): 5 of 5 beats read by both. Their eight shared misreads were fixed in this cut.
- Speech tails (20 Nov): placed every frame from where the speaker is drawn. Hoody's curve down outside his hair to his cheek
  beside the mouth; MY AI's end on its antenna ball. Measured on all 240 bubble frames: 0 px from the speaker.
- Not machine-checkable: whether it is funny, the voice timing and the mix. Tomas judges those.
