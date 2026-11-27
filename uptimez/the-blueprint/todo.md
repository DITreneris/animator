# The Blueprint 16:9 — checklist

The order and the reason for it are in [`16-9-developing.md`](16-9-developing.md).

The room stays the lock in [`set-16x9.md`](set-16x9.md). A box is done when the evidence on that line exists. Do not tick a box because a camera was named.

## Done

- [x] Room locked 25 Nov 2026. Three stills: `stills/bp_still_s0.png`, `bp_still_shred.png`, `bp_still_counter.png`.
- [x] Paper cut v1, 400 s (6:40). Shot list, line ledger, script, cut-down.
- [x] Drawing audit. Live `bp_draw_audit.py` exits 0. `--plant` exits 1 with the eight old fails. Shot 01 still passes. Command: `/quality-assurance-agent`.

## 1. Put the existing shots on the picture

The audit's eight fails. A new rough before this films gags that are off the frame.

- [x] Shot 03. Shred sheet on the slot, (561, 397) to (561, 420).
- [x] Shot 03. The finger is not drawn. Pam is outside SHRED, and a finger with no arm would be a stray. The audit prints that as OPEN.
- [x] Shot 13. The page is in front of the wheel, `ROBOT` + (−8, +28). The stamp comes down onto it. His head and the HR badge stay clear.
- [x] Shot 11. Pocket from the Client (162, 312) to Pam (756, 290).
- [x] Shot 11. Halfway along, the slip passes above Don's head. The bend is (459, 150). Both heads stay inside PUSH.
- [x] Shot 11. Camera is PUSH.
- [x] Shot 05. NIGHT (560, 360, 1.85), and the night scene points at it.
- [x] `bp_draw_audit.py` exits 0. `--plant` exits 1 with the eight old fails. Shot 01 still passes.

## 2. One still, then the number may be written down

- [x] Render the NIGHT still. Open it at full size. Both heads are inside the frame. `stills/bp_still_night.png`.
- [x] Tomas approved the still 25 Nov 2026. Visible: Sofía, Don, Pam, Mom. The lines stay Sofía and Pam.
- [x] NIGHT (560, 360, 1.85) is in `set-16x9.md`.

## 3. Silent rough on this room

- [x] A rough rendered from the locked room. `bp_rough_v2.mp4` and `bp_rough_v2_nonight.mp4`. `bp_rough_v1.mp4` is the old room and was not rewritten.
- [x] Watched. `rough/bp_rough_v2_note.md` lists what reads and what the front wall cannot tell.

## 4. Walk paths

Only the two walks the cut already has. Homes, the desk, and both doors stay.

- [x] Arrival, shot 01, in from the glass door. Feet from x 48 to the home x 132 for the first 3 seconds, while the frame falls. Then the hold. `bp_rough_v3.mp4`.
- [x] The walk back at 1:20. Feet from 132 to about x 80 for the first 3 seconds of shot 04. The hold puts him back on the mark, so shot 06 still has him. That return is a cut, not a second walk.
- [x] Each path caught mid-step, in `rough_work/v3/`. He stays inside S0. He does not cover the robot or the plant.

## 5. Crops the rough asks for

Same drawing. A still before the constant is added to the set file. These three are in `bp_frame.py` and in rough v4. They are not in `set-16x9.md`.

- [x] The zero. ZERO (357, 108, 2.27), the first 3 seconds of shots 07 and 12. The poster is whole, and it still says 0. The screen, the lockup and OUR FIRST CLIENT are whole in that frame too.
- [ ] SCREEN. The word `blueprint` in UPTIMEZ FIND, alone. The rough did not ask for a frame with nothing else in it.
- [ ] BIN. ARCHIVE, the paper inside the window. The rough did not ask.
- [x] STAMP (246, 430, 2.8). After the stamp lands, 3 seconds of CUSTOMER SUCCESS. The robot's head is in that frame. Then S0.
- [x] PLAN (715, 329, 19). The first 3 seconds of shot 05, the taped strips, bay 7 a hole. The night hold hides them again.
- [ ] VOID. The dark CEO slot, only if the rough needs "the office is empty." It does not.

## 6. New drawings

The rough did not name a beat the front wall cannot tell by turning the camera. None of these were drawn. One still each, if a later rough asks. Furniture does not move to make the shot.

- [ ] WIN-L. Left wall, upstage of the light, looking across. Glass door and the Client nearest.
- [ ] WIN-R. Same wall, downstage of the light, looking toward the desk.
- [ ] Iš galo pro duris. Outside the glass door, looking in. For 1:20.
- [ ] Įeina, first person. Stile, mat, ficus, robot, Don, desk. The Client is not also in the room.
- [ ] Išeina, first person. Stop on the door frame. This is not the ending.
- [ ] Bird's view. Straight down, three feet lines. Once. `bp_ground_plan.png` is a label sheet, not this shot.

## 7. Pictures the rough named

Not a new camera. Rough v5 carries them. They stay out of `set-16x9.md` until a still is approved.

- [x] Cannon. Shot 04, after the 90-frame walk, 3 seconds on S0. `set_ob.cannon` at (619, 504, 0.72), between the shredder and the desk. `stills/bp_still_cannon.png`.
- [x] One star. Shot 12, after the ZERO crop, 3 seconds on S0. The phone is in front of Sofía. The poster stays 0. `stills/bp_still_star.png`.
- [x] The mute week. Shot 08, COUNTER, 7.5 seconds each: retries, STUPID in lipstick, MON 1 and THU 4, one deleted message. `stills/bp_still_retry.png`, `bp_still_lipstick.png`, `bp_still_calendar.png`, `bp_still_deleted.png`.
- [x] Watch `bp_rough_v5.mp4` with the sound off. The note is `rough/bp_rough_v5_note.md`. Two cold viewers, 26 Nov 2026: **fail**, 2 of 5 beats each. The week, the zero and the lost plan read. The shred, the pocket and the stamp do not, because no hand does them. Not redrawn: the rough budget is spent.

## 8. Shared files this pilot imports

26 Nov 2026. `origin/main` had moved to `d14139b`. The copies on this branch were still the 24 Nov versions. The Blueprint files themselves were not on `main`.

- [x] `uptimez-blueprint` is `d14139b`. Not pushed.
- [x] `speech.draw(..., safe=SAFE_16X9)` still places a 16:9 bubble. A caller that omits `safe` keeps the 9:16 rect and the button rail. `speech_gate.py` selftest passes.
- [x] `pam_mf.NOSE` stays off unless a sheet turns it on. `GCHAIN_DX` from `main` stays.
- [x] `bp_draw_audit.py` exits 0 after that.

## 8b. main on 27 Nov

`origin/main` `2205945` is in this branch at `2ce3e7e`, 27 Nov 2026. Not pushed. The 26 Nov boxes above stay as they were.

- [x] Read. Of the imported modules, only `hands_ps.py`, `of_cast.py` and `of_scenes.py` differ. Pinch flags and `PHONE_RIM` default off. The `of_scenes` edits are The Offer. `ik2` is unchanged. `bp_frame.py`, `bp_set.py` and `the-blueprint/` are not in the diff. A re-render of v4 would not move a pixel from these three files.
- [x] Merge `origin/main` `2205945` at `2ce3e7e`, 27 Nov 2026. Pinch flags and `PHONE_RIM` default off. `bp_picture.py look` exits 0. `bp_draw_audit.py` exits 0 and `--plant` exits 1 with the eight old fails. `speech_gate` selftest passes. Locked stills and `bp_pic_v4.mp4` (`fd263e1e`) kept their md5. Not pushed. The v4 watch did not wait on it.

## 9. Rough with sound

Budget `bp_sound_v1` to `v5`. v1 copies the silent v5 picture. v2 copies `bp_pic_v2`.

- [x] Voices. `src/bp_voices/`, `bp_voices.py`. 37 shipped takes copied byte for byte (md5-checked), 6 night takes new and local only. Gate 43 of 43, plants 3 of 3, rebuild identical.
- [x] Stop 2 package. `voices/bp_stop2_voices.md`, audition `voices/bp_night_takes_v1.wav`.
- [x] Stop 2, night takes: Tomas keeps them for the local rough (26 Nov 2026).
- [x] Stop 2, shot 10: the two off-screen voices are accepted on `bp_sound_v1` only (26 Nov 2026). "Paid $999" stays. The picture pass puts shot 10 on PUSH.
- [x] Picture budget. `bp_pic_v1` to `v5`, because the silent budget was picture without talk and the sound budget is mixes on a frozen picture.
- [x] Times. `bp_sound_v1_timing.json` from `bp_scenes.timeline()`. `bp_draw_audit.py --lines` exits 0 with shot 10's two speakers as OPEN; `--lines --plant` exits 1.
- [x] Mix. `bp_sound.py`. `bp_sound_v1_nonight.mp4` −15.2 LUFS / −2.1 dBTP, `bp_sound_v1.mp4` −15.1 / −1.5, on the AAC. `uz_check` no faults on both.
- [x] Whisper inside the mix. 43 of 43 and 37 of 37. Two muted lines are lost exactly; room tone ×5 loses none.
- [x] Cold viewers on frames plus the transcript, 26 Nov 2026: **fail**, 3 of 5 beats each (silent v5: 2 of 5). The deal, the deadline, the search failing and the stamp read. Lines land on the wrong woman (no mouths move), and the shred and the pocket still have no author. Picture faults on v5, so no `bp_sound_v2` on that picture.
- [x] Picture v1. `bp_pic_v1.mp4` and `bp_pic_v1_nonight.mp4`. Bubbles, dull zero until `fs_4.3`, shot 10 on PUSH, inserts in the v5 order. `speech_gate` 43 of 43 and 37 of 37. The zero plant caught a green disc with no overlay. Locked stills unchanged. Note `rough/bp_pic_v1_note.md`.
- [x] Who speaks, third watch, 26 Nov 2026: **pass on the body**. Both put "I won't draw one" on the blonde and the other two lines on the woman in the purple top at the desk. Names are not printed. Watches 1 and 2 did not pass. The older-woman reading fell between them.
- [x] Picture v2. Don's hand on the shred after the promise. Pam's hand on the card after the joke; the card leaves on "Check your pocket." `bp_pic_v2_timing.json`. `--hands` exits 0; `--hands --plant` exits 1. Note `rough/bp_pic_v2_note.md`.
- [x] Five questions, 26 Nov 2026: **pass**, 4 of 5 each. Don shreds. The finder is that desk woman. Both missed the stamp, with different wrong answers. v3 stays unspent. The stamp draws CUSTOMER SUCCESS.
- [x] Sound v2. `bp_sound_v2.mp4` −15.2 LUFS / −4.4 dBTP, no-night −15.2 / −1.2. Whisper 43 of 43 and 37 of 37. The mute plant loses exactly `fs_4.1` and `cs_6.5`. A second `bp_sound_v1_nonight` build is md5 `ce8403457c981d5f1d05cd8c01e5cd5e`. The v1 timing file is still `74f55afb586fcbb0f5b643063b0279bf`. `uz_check` no faults.
- [x] Stop 4, 26 Nov 2026: answer 1. Leave the stamp. It stays CUSTOMER SUCCESS in the note and is not redrawn. `bp_pic_v3` is the falling portrait, the cannon firing, and Pam matching the strips. Package `rough/bp_stop4.md`.
- [x] Picture v3. The portrait falls, the cannon fires, Pam's hand is on the tape for "I'm matching them." `beats` exits 0; `beats --plant` exits 1. Note `rough/bp_pic_v3_note.md`.
- [x] Cold watch, 26 Nov 2026: **pass**. [I](0f3375b4-fdc7-4442-8a3b-ac458a3f13ef) 5 of 5, [J](c775c735-83e1-48fc-a6db-cf321cc6c07d) 4 of 5. Both read a framed face, a firing cannon, and the strips being matched. J gave the finder to the older woman. Both read the stamp as CUSTOMER SUCCESS. v4 stays unspent.
- [x] Sound v3. `bp_sound_v3.mp4` −15.2 LUFS / −4.4 dBTP, no-night −15.2 / −1.2. Whisper 43 of 43 and 37 of 37. The mute plant loses exactly `fs_4.1` and `cs_6.5`. A second `bp_sound_v1_nonight` build is md5 `ce8403457c981d5f1d05cd8c01e5cd5e`. The v1 timing file is still `74f55afb586fcbb0f5b643063b0279bf`. `bp_sound_v1.mp4` is still `9762e9991976878bf9ff07339208188b`. `uz_check` no faults.

## 10. The sheet look

The drawings that were already on the sheets, and not in the room. `bp_set.SHEET` stays off, so a locked still does not change. `wsl bash -lc "cd /mnt/c/04_animator/uptimez/src && ~/bpvenv/bin/python bp_picture.py use"` writes the new files. `QUIET` stays off. `of_cast.phone_grip` stays the old function.

- [x] Room. `rough_work/pic_use/bp_use_room.png` and `_270.png`. Sofia's nose and heel, Pam's nose, the Client's elbow, Don's cuffs.
- [x] Night. `bp_use_night.png` and `_270.png`. The same wide, the night light. The nose stays in that grade.
- [x] Phone. `bp_use_phone.png` and `_270.png`. Sheet `phone_grip` v4b, the star and `1/5`. The poster's 0 stays in the frame.
- [x] Mom. Her elbow differs from the room's two segments, so `bp_use_mom.png` and `_270.png` use the one sleeve.
- [x] Tomas approved these four, 26 Nov 2026. The next picture turns this look on.
- [x] `bp_pic_v4` rendered 27 Nov 2026. `bp_pic_v4.mp4` `fd263e1eee822917db682d15fe5ac2a8`, no-night `6bb05a079721c02bebe560afccdbe2a9`. The look from `rough_work/pic_use/`. Shred, the card and the tape stay `point`. The clutch stills in `rough_work/pic_hands/` were not part of this approval. `bp_picture.py look` exits 0. Locked stills unchanged. Note `rough/bp_pic_v4_note.md`.
- [x] Watch `bp_pic_v4.mp4` (400 s) and `bp_pic_v4_nonight.mp4`, 27 Nov 2026. Sheet look against `rough_work/pic_use/` signed off. Shred, the card and the tape staying `point` is this version. The clutch stills in `rough_work/pic_hands/` stay out of v4.
- [ ] `bp_pic_v5`: clutch on shred, card and tape (`of_cast.clutch`, job Holding an edge). `bp_pic_v5_timing.json`. `--grips` exits 0; `--grips --plant` exits 1. Locked stills unchanged. No `bp_sound_v4` until this picture is watched.

## Not this cut

- [ ] A public master. The Kokoro licence is still open. A silent rough does not need it.
- [ ] More furniture, a second plant, or a window painted on the back wall.
- [ ] A low angle. This camera only zooms.
- [ ] First person as the last shot. Shot 13 is the stamp, and the loop stays cut.
