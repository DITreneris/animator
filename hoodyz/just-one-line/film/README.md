# Just One Line (ME + MY AI)

16.8 s, 505 frames, 1080x1920, 30 fps. Hoody hands MY AI a one-line task; it shoves him aside and the fight runs six hits
while FILES CHANGED climbs to 47. HARV looks only at the tick, stamps the card APPROVED and hands MY AI Hoody's briefcase.
MY AI ends in Hoody's chair handing him the same card. It is a nightmare: the background sinks into the dark as it goes,
his eyes close on the last frames and open on frame 0, where he says "Just one line." again.

- `film.py`: the shots (A, F = ../fight.py v12, G, H, J, K), bubbles, the nightmare tint, the eyelids. `python3 film.py sheet 4`.
- `audio.py`: voices, synthesized effects on the picture's events, the fight bed, the nightmare drone; ducks under speech.
- `lines.json` (checked by speech recognition) and `reactions.json` (Tomas's wordless takes).
- `vo/`: Hoody `h_*.wav` = Tomas's takes (recordings 40-52, 23 Nov; `h_swing` and `h_grunts` are recorded but unused);
  MY AI and HARV from `vo/voices.py` (Kokoro: am_puck 1.35x, bm_george).
- `master.sh`: limits at 0.60 with oversampling (the recorded scream overshot -1 dBTP at the series' 0.70).
- `build.sh`: everything, ending in `qa.py`. Last run: GATE PASS, -14.7 LUFS, -3.6 dBTP, all 7 lines recognised.
- Cover: `cover.png` (HARV's stamp); frame 0 is the eyes opening, so pick the cover by hand when posting.
