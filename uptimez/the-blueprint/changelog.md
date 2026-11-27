# The Blueprint — 16:9 progress

The picture is locked. The film is not. The set source of truth is [`set-16x9.md`](set-16x9.md). The 9:16 series is not in this log.

## Now

| | |
|---|---|
| Set | Locked 25 Nov 2026. Sheet `stills/bp_still_s0.png` |
| Close views | `stills/bp_still_shred.png`, `stills/bp_still_counter.png` |
| Paper cut | Shot list, line ledger, script, and cut-down, all v1. 6:40 |
| Rough | `bp_rough_v5.mp4` is the last silent cut of this room, 400 s. `bp_rough_v1.mp4` is the **old** room. v2, v3 and v4 were not rewritten. The sound under v2 to v5 is pink noise |
| Rough with sound | `bp_sound_v3.mp4` (400 s, local only: the night lines are Kokoro) on `bp_pic_v3`, and `bp_sound_v3_nonight.mp4` (360 s). −15.2 LUFS on the AAC, true peak −4.4 / −1.2 dBTP. `bp_sound_v1` stays on v5's picture. `bp_sound_v2` stays on `bp_pic_v2`. Budget 5, three spent. Note `rough/bp_pic_v3_note.md` |
| Voices | `src/bp_voices/`: 37 shipped takes copied byte for byte, 6 new night takes (local only). Stop 2 package `voices/bp_stop2_voices.md` |
| Layouts and motion | `layouts/` and `motion/*_v2.mp4` are on this room. The other `motion/` files are the old coordinates |
| Night | Approved 25 Nov 2026. `stills/bp_still_night.png` `31e044d813fe94ead453458d7b71d5fe`. NIGHT (560, 360, 1.85) is in `set-16x9.md` |
| Drawing audit | `/quality-assurance-agent`. Live `bp_draw_audit.py` exits 0. `--plant` exits 1 with the eight old fails. `--lines` exits 0 with shot 10's two off-screen speakers as OPEN; `--lines --picture` exits 0. `--hands` exits 0; `--hands --plant` exits 1. That hands check measures the boxes `bp_picture.py` just built. `--grips` exits 0 on the hand stills; `--grips --plant` exits 1. A named action is not a hand pass. The still is opened beside the previous picture |
| Series code | Merged `origin/main` `2205945` (The Offer, PR #141) at `2ce3e7e`. Branch point stays `d14139b`. Pinch flags and `PHONE_RIM` default off. `ik2` is unchanged. `bp_picture.py look` exits 0 after the merge. `bp_pic_v4.mp4` md5 `fd263e1eee822917db682d15fe5ac2a8` and the no-night `6bb05a079721c02bebe560afccdbe2a9` did not move. Locked stills `25111ff3`, `da34775d`, `0a25fcc6`, `31e044d8` |
| Picture | `bp_pic_v5.mp4` (400 s) and `bp_pic_v5_nonight.mp4` (360 s), opened, not watched. md5 `91889e7a1ed4d8a62e42239fc14cc19a` / no-night `3fcec6b6bda3f4526913424c40ca0daf`. Clutch on shred, card and tape. Sheet look stays on. Budget `bp_pic_v1` to `v5`, five spent. Tag `uptimez-blueprint-pic-v4` pins watched v4. Note `rough/bp_pic_v5_note.md` |
| Hands | Four stills in `rough_work/pic_hands/`. v5 motion uses `clutch` on shred, card and tape. v4 motion stayed `point`. Pam's clutch is 0.70 of width 18. Don's clutch scale 0.72. The card in the air has no hand. The old phone drawing is `bp_hand_plant_phone.png` |
| Sheet look | Approved 26 Nov 2026. `rough_work/pic_use/`. Watched on v4 the same day as the safety lock. The four locked stills kept their md5 |
| Next | Watch `bp_pic_v5`. No `bp_sound_v4` until that watch (`picture=bp_pic_v5`). SCREEN, BIN, VOID, and the new axes stay unasked. No public master until the Kokoro licence is decided |

## Log

### 2026-11-27 — picture v5, clutch hands, not watched

`bp_pic_v5.mp4` and `bp_pic_v5_nonight.mp4`. Same times as v4. Sheet look stays on. Shred, card and tape use `of_cast.clutch` (job Holding an edge). v1–v4 keep `point`. `bp_picture.py look` and `v5` exit 0. `--grips` exits 0; `--grips --plant` exits 1. Locked stills and `bp_pic_v4` md5s held. Note `rough/bp_pic_v5_note.md`. No `bp_sound_v4`.

### 2026-11-27 — safety lock before clutch v5

`bp_picture.py` and `bp_sound.py` refuse to overwrite an existing `bp_pic_vN` / `bp_sound_vN`. `rows()` only loads timing JSON; `write_vN_timing` creates a missing file once. `look` no longer rewrites v4 timing. A named picture stem picks that stem's timing for a later mix. `look` exit 0; locked stills and `bp_pic_v4` md5s held. Not pushed.

### 2026-11-27 — origin/main merged

`2ce3e7e` merges `origin/main` `2205945` into `uptimez-blueprint`. The one content conflict was `docs/rules-hands-and-phones.md`: the synced copy from main, including `board_two` and `tap_insert`, plus the earlier-version archive. `PINCH_V2`, `PINCH_V3`, `PINCH_V4` and `PHONE_RIM` read false on import. `bp_picture.py look` exits 0. `bp_draw_audit.py` exits 0, fails 0, shot 01 included. `--plant` exits 1 with the eight old fails. `speech_gate.py` selftest passes. Locked stills stayed `25111ff3`, `da34775d`, `0a25fcc6`, `31e044d8`. `bp_pic_v4.mp4` stayed `fd263e1eee822917db682d15fe5ac2a8`, the no-night file `6bb05a079721c02bebe560afccdbe2a9`, the v4 timing `a108715b401f2c5855759ae6dcb1eedf`. No render. The Blueprint hand lesson sits after main's 243–248 as lesson 249. Not pushed. **v4 watch closed** 27 Nov 2026: sheet look vs `rough_work/pic_use/` signed off.

### 2026-11-27 — main since the branch point

`origin/main` is `2205945`, 86 commits after `d14139b`. Not merged. The diff against the modules this pilot imports is `hands_ps.py`, `of_cast.py` and `of_scenes.py`. `PINCH_V2`, `PINCH_V3`, `PINCH_V4` and `PHONE_RIM` default off, so `point` and a phone with no rim stay the drawing v4 already uses. The `of_scenes` edits are The Offer's pocket, slam and lamp. `ik2` is not in that diff. `bp_frame.py`, `bp_set.py` and `the-blueprint/` are not in it either. A merge is not required before the v4 watch.

### 2026-11-27 — picture v4, the signed look, not watched

`bp_pic_v4.mp4` and `bp_pic_v4_nonight.mp4`. Same times as v3. `SHEET` and `MOM_ARMS` are on for this version only: Sofia's nose and heel, Pam's nose, the Client's elbow, Don's cuffs, Mom's one sleeve. Shot 12's silent star frames are the phone grip v4b on the signed crop. "Your number." is that pose on S0, because the crop cannot hold the bubble. The rectangle stays on v3. Shred, the card and the tape stay `point`. The four locked stills kept `25111ff3`, `da34775d`, `0a25fcc6` and `31e044d8`. `bp_picture.py look` exits 0. Note `rough/bp_pic_v4_note.md`. Not watched. No `bp_sound_v4`.

### 2026-11-26 — sheet look approved

Tomas approved the four stills in `rough_work/pic_use/`. The room, the night light, the phone and Mom's sleeve are the drawing the next picture uses. Sofia's nose and heel, Pam's nose, the Client's elbow and Don's cuffs are in that look. `QUIET` stays off. The phone on `bp_use_phone.png` is sheet `phone_grip` v4b, not `of_cast.phone_grip`.

`python bp_picture.py use` wrote them, full size and 270 px. `bp_set.SHEET` stays off, so a rebuild of the locked room does not take the look. The class sheet v4 matched the file it replaced, pixel for pixel. v1, v2 and v3 of that sheet kept their md5. The four locked stills kept `25111ff3`, `da34775d`, `0a25fcc6` and `31e044d8`.

The clutch stills in `rough_work/pic_hands/` were not in this approval. `bp_pic_v4` was not opened. The checklist is section 10 of `todo.md`.

### 2026-11-26 — hand still polish

Pam's clutch on the card and on the tape is drawn at 0.70 of width 18. An 8 px sleeve runs from the desk slab into that palm. `pam_taping` skips its blue strip on those two stills only. Don's clutch is 0.72 of the arm width, and a skin stroke covers the shirt's end so the cuff and the palm are one shape. The sheet, the bone length, the phone crop and the flight frame were not moved. `bp_hand_reach.txt` now records the tape contact as 0. The 25 px bone shortfall stays in the note. `--grips` exits 0. `--grips --plant` exits 1. The four locked stills kept their md5. `bp_pic_v4` was not opened. No 10 fps strip.

The working crops named in the entry below were removed after this pass.

### 2026-11-26 — grip plants and crops

`python bp_picture.py grips --plant` writes the old drawing into `rough_work/pic_hands/`, full size and 270 px, and exits 1 when a sleeve stroke, a second `point`, and a phone rectangle are all caught. Those files are `bp_hand_plant_shred.png`, `bp_hand_plant_pocket.png`, `bp_hand_plant_tape.png` and `bp_hand_plant_phone.png`. The four live stills were not replaced.

Crops of the three `clutch` stills, same folder: `crop_shred.png` (the sheet at the slot), `crop_card.png` (the card on the hand), `crop_tape.png` (the fist on the seam). `bp_hand_reach.txt` is unchanged: shred elbow 89°, card and tape 99°, phone 110°, slot gap 19 px. `bp_pic_v4` was not opened. No 10 fps strip.

The drawing audit now says a named action is not a hand pass. The still is opened beside the previous picture. That line is in `.cursor/skills/quality-assurance-agent/lessons.md`. The 9:16 film is not in this log.

### 2026-11-26 — hand stills

`python bp_picture.py grips` paints the stills and exits 1 on a sleeve stroke, a second `point`, or a phone rectangle. `--plant` paints today's picture into the same folder and exits 1 when all three are caught. `bp_draw_audit.py --grips` is that command. `--hands` is unchanged: it still measures the pose boxes, and `--hands --plant` still exits 1.

Full 960×540 and 270 px, under `rough_work/pic_hands/`:

- `bp_hand_shred.png`. Don's returned hand, `of_cast.clutch`. The sheet's far side aims at the slot and stops 19 px short. The arm was shortened 46 px. Bone length stays 48. Elbow 89°.
- `bp_hand_flight.png`. One frame of the pocket flight. No hand.
- `bp_hand_card.png`. The card is on the hand `pam_taping` returns, `clutch`. That hand is 72 px from the pocket mark. The mark sits on Mom, so the card was not carried there. Elbow 99°.
- `bp_hand_tape.png`. The seam moved 44 px onto that same hand. It was 25 px past the two bones. `clutch` on the strip. Elbow 99°.
- `bp_hand_phone.png`. Sofía in this room, tablet off, `of_cast.phone_grip`. One gold star, `1/5` the largest word, her middle at `body_x`, the thumb below the word. Crop (350, 254, 1.99) is on this still only. At 270 px the word is 4.0 px wide and the poster's 0 is still in the frame. A crop that made the word readable would lose the 0.

`bp_hand_reach.txt` has the bends and the gaps. The four locked stills kept their md5. `bp_pic_v4` was not opened. No 10 fps strip.

### 2026-11-26 — main is past the shared-file pin

`origin/main` is `aaab657`. The shared-files entry below records the fast-forward to `d14139b` (One Star v18). This branch was not moved again. Nothing was merged and nothing was pushed.

`uptimez/customer-success/one-star-v14-notes.md` on `main` continues through v26. The copy on this branch ends at v18. The drawings are opt-in: `cs_os19.py` through `cs_os26.py`, plus later lines in `cs_grips.py` and `cs_scene5.py`. `of_cast.phone_grip` is the same function.

What those notes add, and this branch does not have:

- v20. Hand and elbow gates at 0 while an ownerless sleeve, a phone that appears, and a finger on a word still read. `main` added two gates and tried them on the planted v17 frame first: an insert cuff with no owner, and a one-colour band over 40% of the frame.
- v23. Sofía's phone is `phone_grip` on her own arm. A hand at the edge of a tablet has no arm. The first straight arm failed the elbow gate. The last wide keeps only Don's phone.
- v25. The Client's phone at 1.0× was smaller than his fingers. It is 1.8×.
- v26. `point` on the plan was left. The review called it a little unnatural.

Lesson 245 on `main` records the same pass: clip an overlay to the rig part as drawn, and a phone shown to us is in its owner's arm. This branch's rules page is the job table. It does not name v20–v26. The picture was not redrawn. v4 stays unspent.

### 2026-11-26 — hands page

[`docs/rules-hands-and-phones.md`](../../docs/rules-hands-and-phones.md) is the hand for every film. It opens with the job table (`quiet`, `point`, `point_t`, `grab`, `clutch`, `pinch`, `fist`, `palm`, `thumb`, `phone_grip`, `handle_grip`). A job that is not in the table is a new row on that page, written before code. An episode does not get its own hands file, and `docs/lessons.md` is not grepped for a hand shape. The lesson numbers sit at the bottom.

`uptimez/CLAUDE.md` point 4, [`INDEX.md`](../INDEX.md) and lesson 227 point at that table. The picture, the locked stills, `bp_pic_v3` and `bp_sound_v3` were not rewritten. v4 stays unspent.

The three hands on this cut are still the v2 and v3 drawing: a `point` and a sleeve stroke from a fixed fist, on top of the hand the room already draws. Shot 12's phone is still `star_overlay`, a rectangle, while Sofía's pose is `hold`. `--hands` still exits 0, because it measures those boxes. The next hand names its row first.

### 2026-11-26 — picture pass, sound v2

`bp_picture.py`. A bubble on the speaker (`speech.draw`, `SAFE_16X9`). The poster zero is an overlay: dull grey until Don's "Approved." (`fs_4.3`) ends on shot 07, then the poster's own green. `bp_set._poster` was left alone, and the four locked stills kept their md5. Shot 10 is PUSH in this module only. `SHOTS` stays COUNTER, so a rebuild of rough v5 is unchanged. The finger stays undrawn.

- **v1.** Inserts stay in the v5 order, so who speaks could be judged alone. Three cold watches. The third passed on the body: both viewers put "I won't draw one" on the blonde in the pink coat, and "Check your pocket" and "Some shit, others scoop." on the woman with the brown bob, glasses and purple top at the desk. Neither name is printed. One of them called that desk woman Sofía, because Don shouts the name. The note is `rough/bp_pic_v1_note.md`.
- **v2.** Shot 03 holds the promise, then Don's hand (the series `point`, sleeve from the fist the room already draws) puts the page in the shredder, then the hold. Shot 11 holds the joke, the card leaves the pocket with "Check your pocket.", and Pam's hand is on the card for the hold after. Times are `bp_pic_v2_timing.json`. `bp_scenes.timeline()` and `bp_sound_v1_timing.json` stay the v5 order (`74f55afb586fcbb0f5b643063b0279bf`). Both cold viewers read 4 of 5. Don shreds the page. The finder is that same desk woman. Both missed the stamp, and they missed it differently: the zero turned green, and a blank yellow circle. The stamp draws CUSTOMER SUCCESS. v3 was not spent. The note is `rough/bp_pic_v2_note.md`.
- **Sound.** `bp_sound.py` takes a picture. A bare mix still writes `bp_sound_v1` from v5, and a second no-night build is md5 `ce8403457c981d5f1d05cd8c01e5cd5e`. `bp_sound_v2.mp4` copies the v2 packets and uses the v2 times: the same dry takes, room tone at 0.3, no reflections. Loudness on the AAC, limiter 0.80 (0.85 peaked at −0.3 and −0.2): full −15.2 LUFS / −4.4 dBTP, no-night −15.2 / −1.2. Whisper 43 of 43 and 37 of 37. The mute plant loses exactly `fs_4.1` and `cs_6.5`. `uz_check` no faults on either file. `bp_sound_v1.mp4` is still `9762e9991976878bf9ff07339208188b`.

The picture files carry the silent roughs' pink-noise bed, so the loudness check has something to measure. That bed is not the mix. Stop 4 is `rough/bp_stop4.md`. [`INDEX.md`](../INDEX.md), the README episode list, [`set-16x9.md`](set-16x9.md) and [`docs/sessions.md`](../../docs/sessions.md) name `bp_sound_v2.mp4` as the current cut.

### 2026-11-26 — Stop 4, answer 1

Tomas watched `bp_sound_v2.mp4` and left it. The stamp stays CUSTOMER SUCCESS in the note. It is not redrawn, and v3 is not spent on it. `bp_pic_v3` is the three beats a wide still cannot tell: the portrait falling off the wall, the cannon firing, and Pam matching the strips. 400 s, the shot lengths, and the v2 line times stay.

### 2026-11-26 — picture v3, sound v3

`bp_picture.py`, version 3 only. `bp_scenes._motions(5)` and `SHOTS` stay. The wall portrait is skipped only while shot 01 is painted (`SKIP_PORTRAIT`, off by default, so the locked stills do not change).

- **Picture.** The portrait falls from the peg to the floor. The cannon's fuse runs and confetti leaves the muzzle toward the ARCHIVE bin. On "I'm matching them." the taped plan and Pam's hand are on a seam. Times are a copy of `bp_pic_v2_timing.json`. The picture bed is pink noise, −15.3 LUFS. `uz_check` no faults. 12000 and 10800 frames.
- **Watch.** [I](0f3375b4-fdc7-4442-8a3b-ac458a3f13ef) 5 of 5, [J](c775c735-83e1-48fc-a6db-cf321cc6c07d) 4 of 5. Both read a framed face, a cannon that fires, and the desk woman matching the strips. J gave the finder to the older woman. Both read the stamp as CUSTOMER SUCCESS. v4 was not opened. The note is `rough/bp_pic_v3_note.md`.
- **Sound.** `bp_sound_v3.mp4` copies the v3 packets and the v2 times. Same dry takes, room tone 0.3, limiter 0.80 (0.85 peaked at −0.3 and −0.2). Full −15.2 LUFS / −4.4 dBTP, no-night −15.2 / −1.2. Whisper 43 of 43 and 37 of 37. The mute plant loses exactly `fs_4.1` and `cs_6.5`. A bare mix still rebuilds `bp_sound_v1_nonight` at `ce8403457c981d5f1d05cd8c01e5cd5e`. `bp_sound_v1.mp4` is still `9762e9991976878bf9ff07339208188b`. The v1 timing file is still `74f55afb586fcbb0f5b643063b0279bf`.

[`INDEX.md`](../INDEX.md), the README episode list, [`set-16x9.md`](set-16x9.md) and [`docs/sessions.md`](../../docs/sessions.md) name `bp_sound_v3.mp4` as the current cut.

### 2026-11-26 — rough with sound v1

The silent roughs v2 to v5 carried pink noise, not a mix: `_concat` laid `anoisesrc` under `loudnorm`. Their −15.3 LUFS measured the noise. They were not rewritten.

- **Voices.** `bp_voices.py` writes `src/bp_voices/`. The 37 inherited lines are the shipped takes in git, copied byte for byte and checked by md5. They are not regenerated: this machine's Kokoro does not reproduce them ("Approved." 0.783 s against the shipped 0.718 s in kokoro-onnx 0.4.4 and 0.4.7; First Search 4.1 rebuilt is heard "make the zero grain"). An earlier ledger line said no WAVs were kept; it was wrong and is corrected. The six night lines are Sofía (`sound_bc.sofia`) and Pam voice A, local only. "Recovered from what?" and "He needs the bays." are given to Kokoro differently from how they are written, because Whisper misheard the written form 3 of 3. Gate 43 of 43, plants 3 of 3, a second build identical.
- **Times.** `bp_scenes.timeline()` and `bp_sound_v1_timing.json`. `bp_draw_audit.py --lines` checks each speaker's head inside the camera of the moment, and no line over a crop, the shred, the pocket or the stamp.
- **Mix.** `bp_sound.py`. v5's picture stream-copied (packets identical), dry takes, `cs_film.py` room tone at 0.3, no reflections. Loudness on the AAC with the limiter at 0.85: 0.50 needed more than 10 dB of limiting and fell short of −15.
- **Cold watch.** Frames plus a timestamped transcript: fail, 3 of 5 beats each (v5 silent: 2 of 5). Both gave Pam's lines to Mom and none to Sofía, because no mouth moves. The shred and the pocket still have no author. Not a sound fault; no v2.
- **Checks.** `uz_check` no faults on both files. Whisper inside the mix 43 of 43 and 37 of 37; the plant with two lines muted loses exactly those two. Room tone ×5 loses none (no music: the tone stays 38 dB under the voices). The four locked stills kept their md5.

The note is `rough/bp_sound_v1_note.md`.

### 2026-11-26 — decisions before the picture pass

- The six night takes stay in the local rough. The Kokoro licence is still open, so they are not a public master.
- "Paid $999" stays. It is the shipped One Star take, heard 3 of 3 in the mix. "A thousand dollars" and "1K" were asked and not used.
- Shot 10's two off-screen voices are accepted on `bp_sound_v1` only. The picture pass puts shot 10 on PUSH. `SHOTS` is not changed, so a rebuild of rough v5 is still COUNTER.
- The long silent tails after the last line are not filled by stretching the dialogue.

### 2026-11-26 — shared files

`origin/main` of `DITreneris/animator` moved from `63888e3` to `d14139b` (One Star v18, Pick a Side). This branch had no commits of its own, so it was fast-forwarded. Nothing was pushed.

The pilot's own files (`bp_*.py`, `the-blueprint/`) are not on `main`, so the fast-forward did not touch them. Six shared files had been edited on both sides. `main`'s versions were kept, and the 16:9 lines were put back on top:

- `speech.py`. `draw` still has `ROBOT`, `pin`, `CLEAR`, `SIGNS_FIRST` and `TOP_FIRST`. It also takes `safe=`. `SAFE_16X9` is (24, 24, 936, 516).
- `speech_gate.py`. `RAIL`, `avoid` and `fill` stay. The button rail is checked only when `safe` is omitted. Selftest passes.
- `pam_mf.py`. `NOSE` stays off by default. `GCHAIN_DX` stays.
- `CLAUDE.md`, `INDEX.md`, `series/front-desk-set.md`. The Blueprint rows stay. So do the hands rule, the set gate, and the Pick a Side v9 line.

`client_ob.py`, `don_v4.py`, `sofia_fs.py`, `uz_check.py`, `series/production-process.md` and `tools/stage5_pack.py` were not on that `main` diff. They were left as they were. `bp_draw_audit.py` still exits 0.

### 2026-11-26 — rough v5

The four stills are in the cut. `bp_rough_v5.mp4` is 400 s, 12000 frames, −15.3 LUFS, peak −1.3 dBTP. `bp_rough_v5_nonight.mp4` is 360 s, 10800 frames, −15.3 LUFS, peak −1.5 dBTP. The first no-night join peaked at −0.9, so those parts were joined again with the limiter at 0.80. v1, v2, v3 and v4 were not rewritten. The four locked stills kept their md5. The note is `rough/bp_rough_v5_note.md`.

### 2026-11-25 — mute week stills

Shot 08 is 30 seconds on COUNTER. On v5 the four reads fill it, 7.5 seconds each, in shot-list order. No new talk. The cards sit on the wall above Pam and Mom. Their heads stay in the frame. OUR FIRST CLIENT keeps the crop already written in the set file.

- Retries. `0 RESULTS` and `RETRY UNTIL FRIDAY`, in the colours of the retry screen in `fs_film35.py`.
- Lipstick. `STUPID`, the letters from `fs_film35.lipstick_word`, and the lipstick from `fs_film35.lipstick`. The robot is outside COUNTER, so the word is on the sheet, not on his back.
- Calendar. MON 1 and THU 4, the page from `fs_film35.calendar`. The shot list stops at Thursday.
- Deleted. One struck line and the word DELETED. First Search has no separate drawing for this card.

Stills: `bp_still_retry.png`, `bp_still_lipstick.png`, `bp_still_calendar.png`, `bp_still_deleted.png`. `bp_draw_audit.py` exits 0. `--plant` exits 1 with the eight old fails. The four locked stills were not rewritten. None of these cards are in `set-16x9.md`.

### 2026-11-25 — one star still

Shot 12 still opens on ZERO for 90 frames. The next 90 frames, on v5 only, are S0 with Sofía's phone in front of her body. One gold star and four empty ones, then 1/5. The mark is `cs_scene6.star`. The poster still says 0. Her head and Don's head stay above the phone.

`stills/bp_still_star.png`. The crop is `stills/bp_still_star_crop.png`. `bp_draw_audit.py` exits 0. `--plant` exits 1 with the eight old fails. The four locked stills were not rewritten. The phone is not in `set-16x9.md`.

### 2026-11-25 — cannon still

Shot 04 already walks for the first 90 frames. The next 90 frames, on v5 only, are the hold with a cannon between the shredder and the desk. `set_ob.cannon`, scale 0.72, feet at the shredder's floor, label CONFETTI. The muzzle points at the bin. Homes, the desk, and both doors stay.

`stills/bp_still_cannon.png`. The crop is `stills/bp_still_cannon_crop.png`. `bp_draw_audit.py` exits 0. `--plant` exits 1 with the eight old fails. The four locked stills kept their md5. The cannon is not in `set-16x9.md`. Rough v5 is not rendered.

### 2026-11-25 — word crops, rough v4

Three words that were already on the wall, each for the first 3 seconds of its shot, then the shot's own camera. No new prop. The poster still says 0.

- ZERO (357, 108, 2.27). Shots 07 and 12. NOTHING, GETS LOST, the green 0, FOUND. The screen, the lockup and OUR FIRST CLIENT are whole in the same frame.
- STAMP (246, 430, 2.8). Shot 13, after the 60-frame stamp on S0. CUSTOMER SUCCESS reads. The robot's head is in the frame.
- PLAN (715, 329, 19). Shot 05. The taped strips, bay 7 a hole. The night hold hides them again, so the approved night still is the hold.

`bp_rough_v4.mp4` is 400 s, 12000 frames, −15.3 LUFS, peak −1.0 dBTP. `bp_rough_v4_nonight.mp4` is 360 s, 10800 frames, the same loudness. v1, v2 and v3 were not rewritten. The four locked stills were not rewritten. The note is `rough/bp_rough_v4_note.md`.

These triples are in `bp_frame.py`. They are not in `set-16x9.md`.

Not drawn: the mute week, STUPID in lipstick, a cannon, a star. SCREEN alone, BIN, and the empty CEO slot were not asked for by the rough.

### 2026-11-25 — Client walks, rough v3

The Client's home stays (132, 458, 0.52). Pose stays stand. `SKIP_CLIENT` defaults off, so a locked still does not move.

- Shot 01. Feet from x 48, inside the glass door, to x 132, the first 90 frames, while the frame falls. The hold is the home.
- Shot 04. Feet from 132 back to about x 80, the first 90 frames. He stays inside S0 and does not cover the robot or the plant. The hold puts him back on the mark. That return is a cut, not a second walk. Shot 06 still has him for Friday.

`bp_rough_v3.mp4` is 400 s, 12000 frames, −15.3 LUFS, peak −1.1 dBTP. `bp_rough_v3_nonight.mp4` is 360 s, 10800 frames, peak −1.1. v1 and v2 were not rewritten. The note is `rough/bp_rough_v3_note.md`. Mid-step stills are in `rough_work/v3/`.

### 2026-11-25 — silent rough v2

The first rough of the locked room. `bp_rough_v1.mp4` was left as the old room.

`bp_rough_v2.mp4` is 400 s, 12000 frames, −15.3 LUFS, peak −1.3 dBTP after the limiter. `bp_rough_v2_nonight.mp4` is 360 s, 10800 frames, peak −1.2. The first concat peaked at −0.9. An `alimiter` at 0.85 was added and the same parts were joined again. No cairo redraw for that fix.

Before this render, three picture faults were closed. The finger is not drawn. The stamp page sits in front of the wheel. The pocket slip passes above Don's head.

Watched with the sound off. What reads, and what the front wall cannot tell, is `rough/bp_rough_v2_note.md`. That note is the brief the walks and the crops were built from.

### 2026-11-25 — drawing audit command

`/quality-assurance-agent` is the command. The file is `.cursor/commands/quality-assurance-agent.md`. It follows `.cursor/skills/quality-assurance-agent/SKILL.md`: name the frame, run the checker, open the PNG at full size, report one table.

16:9 uses `bp_draw_audit.py`. Live exits 0. `--plant` exits 1 with the eight old fails. 9:16 stays on `uz_check.py`. Hoodyz stays on `hoodyz/qa.py`. GV, GP, GD and GH stay in `gates_os.py` for One Star. There is no color-contrast gate.

Written into `series/production-process.md` (stage 4 and the Drawing audit section), `CLAUDE.md`, and `INDEX.md`. The skill's planted misses now match the room: shot 05 is NIGHT, shot 11 is PUSH.

### 2026-11-25 — NIGHT approved

Tomas approved `stills/bp_still_night.png`. The triple NIGHT (560, 360, 1.85) is in `set-16x9.md`. The shot list's 1:40 row now says NIGHT. The six night lines are unchanged. No takes yet. The 7.5 notes (split pants, a second plant, a thinner desk, stronger blinds) were not built. The approved picture is the second light pass.

### 2026-11-25 — night light, second pass

The first night pass still read as a grey veil. The room is now a flat night wall `#596780` (measured rgb 89, 103, 128) and a darker floor `#3E4B63`. Sofía, Don, Pam, Mom, the desk, the cabinet and the shredder are put back from the day frame, so their colours are not in the veil.

Blind bars are `#131C2C`, about 40% quieter. The wall keeps the window slope. The floor bars are flatter and do not continue the wall angle. The monitor glass is `#9EDFFF`, with a short spill and a cyan touch on Pam's face and hands. One warm practical `#E5B36D` sits on the right desk front. A contact shadow sits under the cabinet only.

`bp_still_night.png` is `31e044d813fe94ead453458d7b71d5fe`. The three locked stills and `layouts/bp_layout_final.png` kept their md5. Nothing was added to the empty upper-left of this crop: the logo, the clock and the ficus are already on the wide, and this pass is light only.

### 2026-11-25 — night light

The night frame was a 45% near-black overlay, so it read as a dimmed day. `grade < 1` now runs `_night` in `bp_frame.py` and leaves the day paint alone.

Measured: 30% of `#252E48` over the day wall is still brown, rgb 172, 164, 152. A pale-blue multiply comes first, then the 30% layer. The wall lands at rgb 115, 123, 134.

On top of that, only where it belongs: the six blind bars cooler and carried onto the floor, a warm pool on the desk, the desk monitor glass lit with a spill onto Pam, and a 3-pixel cold rim on the window side of Sofía and Don.

Locked stills and `layouts/bp_layout_final.png` re-rendered with the same md5. `bp_still_night.png` is `41466fe188d6ebfbd4ba926bf5fdcb58`. Camera, homes, and furniture were not moved.
### 2026-11-25 — geometry

The motion marks now sit on the locked room. `bp_set.py` was not touched. Each mark is a constant in `bp_scenes.py`, offset from a prop or a home:

- Shred sheet, shot 03: on the bin's slot, `SHRED_AT` + (5, −123 × 0.72) = (561, 415). The sheet goes from y 397 to y 420.
- Pocket, shot 11: from the Client, `CLIENT` + (30, −146) = (162, 312), to Pam, `PAM` + (62, −128) = (756, 290). The counter dot uses the same end point.
- Stamp, shot 13: page at `ROBOT` + (−36, −56) = (212, 402). The stamp starts 228 above it.

Cameras. Shot 05 is now NIGHT and shot 11 is now PUSH. `layouts()` takes the night camera from the shot. S0, SHRED, COUNTER and PUSH are unchanged.

`bp_draw_audit.py` reads the marks from `bp_scenes.py`, and shot 13 now also requires the robot. `--plant` restores the 25 Nov coordinates and cameras.

```
bp_draw_audit.py          fails 0   exit 0
bp_draw_audit.py --plant  fails 8   exit 1   (03 ×3, 05 pam, 11 client, 11 ×2, 13)
```

The three locked stills re-rendered byte-identical to the `C:\uptimez` copy:

```
25111ff33a2338b32e7bdea584204c28  bp_still_s0.png
da34775d2ac9821b42f149abb8261149  bp_still_shred.png
0a25fcc6b5831f360f24eb79c312fb5f  bp_still_counter.png
1697943d76b767e6dc6f482cf5f94cca  bp_still_night.png        new
efaa3a1e4d7664514bc183d06e4c4c10  layouts/bp_layout_night.png
```

Motion v2: `bp_motion_shred_v2.mp4`, `bp_motion_pocket_v2.mp4`, `bp_motion_stamp_v2.mp4`, each with frames 00, 30 and 59 as PNG. The old `bp_motion_*.mp4` files and `bp_rough_v1.mp4` were not overwritten.

Seen at full size, still open:

- Night still. Sofía and Pam are both in. So are Don and Mom, with Don between the two speakers. Later the same day Tomas approved that occupancy. The lines stay Sofía and Pam.
- Pocket. Halfway along, the slip passes across Don's face, and it reads as a note stuck to his forehead.
- Stamp. The page covers the robot's body and his HR badge. His head stays clear.
- Finger, shot 03. In onboarding 5.1–5.3 it is Pam's raised finger. Pam is not inside SHRED, and a finger on the bin with no arm would be a stray. It was left at the 9:16 floor, and the audit lists it as OPEN, not as a pass.

### 2026-11-25 — set locked

Tomas locked the stills as the 16:9 source of truth after the prop pass. Indexed in `uptimez/INDEX.md`. `fs_set4.py` stays 9:16.

Last picture fixes, on the locked room: the mug sits on the desk, the CCTV has a wall plate, the shredder paper stays inside the bin, the brown ficus leaf hangs as a leaf.

### 2026-11-25 — picture

The room was rebuilt in 960×540 (floor at y 400). It is not a crop of the 9:16 set.

Audits, in order, stills only:

- Geometry. Own CEO door (the 330px door's lower panel hung past this floor). Desk open underneath. Three feet-lines. Contact shadows one direction.
- Type. Both nameplate lines inside the plate. White CEO off the door leaf. FOUND under the green 0. FILES in the holder. ARCHIVE on this shredder only.
- Passage. Desk 658–846, door at x 888, cabinet against the wall with LOST FILES. Shred camera moved so the desk is out and the cabinet is whole.
- Light. Six blind bars from a window off the left, one ficus, darker desk front, cooler glass, wider mat. Floor and wall painted past x 0 and x 960 so the close-ups have no cut edge.
- Colour. Blinds quieter, four floor seams, thicker top, three greens on the ficus, CEO wood lighter. Audit 8.3. Stop adding decoration.
- Logo. `UPTIMEZ INC.` lockup at (330, 18), between the screen and the portrait. Wide only.

`bp_rough_v1` was not re-rendered on any of these passes. Kokoro's commercial licence is still unconfirmed, so there is no public master.
