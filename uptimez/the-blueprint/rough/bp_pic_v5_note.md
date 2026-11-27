# Picture v5

`bp_pic_v5.mp4` is 400 s, 12000 frames, 1920×1080, bt709. md5 `91889e7a1ed4d8a62e42239fc14cc19a`.
`bp_pic_v5_nonight.mp4` is 360 s, 10800 frames. md5 `3fcec6b6bda3f4526913424c40ca0daf`.
v1–v4 stay. `bp_pic_v4.mp4` is still `fd263e1eee822917db682d15fe5ac2a8`. The silent roughs, `bp_sound_v1` to `bp_sound_v3`, and the four locked stills were not rewritten.

The bed is pink noise. There is no `bp_sound_v4`. The mix waits until this picture has been watched. Mix with `picture=bp_pic_v5` so timing follows `bp_pic_v5_timing.json`.

## What changed from v4

Same 400 s, same shot lengths, same line times as `bp_pic_v4_timing.json`, copied once into `bp_pic_v5_timing.json` (`91d3a3a23e5ef0675523f66724411b2d`). `write_timing()` was not called. Earlier timing files were only read.

Sheet look stays on (`SHEET`, `MOM_ARMS`) for version ≥ 4. Shot 12's star insert stays phone grip v4b.

**Job:** Holding an edge (sheet, card, lid) → `clutch` → `of_cast.clutch`.
Shred, the card and the tape draw clutch on version 5 only. v1–v4 keep `point` plus the sleeve stroke. `DON_HAND` / `PAM_HAND` stay `"point"` so `look` still locks v4.

## Gates

`bp_draw_audit.py --grips` exits 0. `--grips --plant` exits 1 (old stroke, second point, phone rectangle).
`bp_picture.py look` exits 0 (v4 path unchanged).
`bp_picture.py v5` exits 0: clutch on shred/pocket/match, no stroke, no point; bubbles 43 of 43 and 37 of 37.

## Watch

Open `bp_pic_v5.mp4` and `_nonight`. Check: Don shreds with a clutch on the sheet; Pam's clutch meets the card after the joke; Pam's clutch matches the tape on "I'm matching them."; sheet look vs `rough_work/pic_use/` still reads. No `bp_sound_v4` until that watch.
