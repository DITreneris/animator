# Sound v4

`bp_sound_v4.mp4` is 400 s on `bp_pic_v5.mp4`, −15.2 LUFS, true peak −4.4 dBTP (AAC). md5 `3a0cd7cd3e6adcbc92c0512ece86238c`.
`bp_sound_v4_nonight.mp4` is 360 s on `bp_pic_v5_nonight.mp4`, −15.2 LUFS, −1.2 dBTP. md5 `b36d06e48f8d19884c02389922174cb4`.

Built with `bp_sound.py mix full|nonight 4 bp_pic_v5`, so timing is `bp_pic_v5_timing.json`. `bp_sound_v1`–`v3`, `bp_sound_v1_timing.json` (`74f55afb…`), and `bp_pic_v5` (`91889e7a…`) were not rewritten.

Same dry takes as v1–v3. Same line times as picture v2–v5. Room tone ×0.3. No music, no pink noise under the mix.

## Gates

| Check | Result |
|---|---|
| Whisper inside the mix, 3 windows | 43 of 43 (full), 37 of 37 (no-night). "Oh..." unscored vowel |
| Mute plant (`bp_sound.py plant 4`) | loses exactly `fs_4.1` and `cs_6.5` |
| `bp_sound_v1.mp4` | still `9762e9991976878bf9ff07339208188b` |
| `bp_sound_v3.mp4` | still `1dbeb577915e9f7067b2b2ca8f0ed71f` |

## Watch

Open `bp_sound_v4.mp4` (and `_nonight` if useful). Picture is the clutch v5 cut. Sound budget: four of five spent.
