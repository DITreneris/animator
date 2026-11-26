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
- [ ] Watch `bp_rough_v5.mp4` with the sound off. The note is `rough/bp_rough_v5_note.md`.

## 8. Shared files this pilot imports

26 Nov 2026. `origin/main` had moved to `d14139b`. The copies on this branch were still the 24 Nov versions. The Blueprint files themselves were not on `main`.

- [x] `uptimez-blueprint` is `d14139b`. Not pushed.
- [x] `speech.draw(..., safe=SAFE_16X9)` still places a 16:9 bubble. A caller that omits `safe` keeps the 9:16 rect and the button rail. `speech_gate.py` selftest passes.
- [x] `pam_mf.NOSE` stays off unless a sheet turns it on. `GCHAIN_DX` from `main` stays.
- [x] `bp_draw_audit.py` exits 0 after that.

## Not this cut

- [ ] A public master. The Kokoro licence is still open. A silent rough does not need it.
- [ ] More furniture, a second plant, or a window painted on the back wall.
- [ ] A low angle. This camera only zooms.
- [ ] First person as the last shot. Shot 13 is the stamp, and the loop stays cut.
