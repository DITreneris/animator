# Picture v4

`bp_pic_v4.mp4` is 400 s, 12000 frames, 1920×1080, bt709, −15.3 LUFS, peak −1.6 dBTP.
`bp_pic_v4_nonight.mp4` is 360 s, 10800 frames, the same bed, −15.3 LUFS, peak −1.3 dBTP.
v1, v2 and v3 stay. The silent roughs, `bp_sound_v1` to `bp_sound_v3`, and the four locked stills were not rewritten.

The bed is pink noise, as on v1 to v3. Those numbers measure the noise. There is no `bp_sound_v4`. The mix waits until this picture has been watched.

## What changed from v3

Same 400 s, same shot lengths, same line times as `bp_pic_v3_timing.json`, copied into `bp_pic_v4_timing.json`. `write_timing()` was not called. v1, v2 and v3 timing files were only read.

`SHEET` and `MOM_ARMS` are on while version 4 paints, and off again after. The frames take the look Tomas signed on 26 Nov: Sofia's nose and heel, Pam's nose, the Client's elbow, Don's cuffs, Mom's one sleeve. `QUIET` stays off. `of_cast.phone_grip` was not called.

Shot 12's star insert, the silent parts, is the signed phone still: sheet grip v4b, the star and `1/5`, on the tight crop that still holds the poster's 0. The 108×120 rectangle is not drawn. v3 still paints that rectangle on S0.

"Your number." (`cs_5.1`, 4.0 s) falls inside that insert. The phone crop holds the Client's head and cannot hold the bubble. That one piece is the same wrist and pose on S0, with no rectangle. The lines after 6.0 s stay on the S0 hold, and Sofia is back on her room pose.

Shred, the card and the tape stay `point`. The clutch stills in `rough_work/pic_hands/` are not in this picture.

`bp_picture.py look` exits 0: `use` left `pic_use` and the locked md5s alone, `beats` exits 0, `beats --plant` exits 1, and `bubbles` is 43 of 43 and 37 of 37. Not watched.
