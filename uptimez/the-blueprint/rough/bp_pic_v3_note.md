# Picture v3

`bp_pic_v3.mp4` is 400 s, 12000 frames, 1920×1080, bt709, −15.3 LUFS, peak −1.5 dBTP.
`bp_pic_v3_nonight.mp4` is 360 s, 10800 frames, the same bed, −15.3 LUFS, peak −1.2 dBTP.
v1 and v2 stay. The silent roughs, `bp_sound_v1`, `bp_sound_v2`, and the four locked stills were not rewritten.

The bed is pink noise, as on v1 and v2. Those numbers measure the noise. The mix is `bp_sound_v3.mp4`.

## What changed from v2

Same 400 s, same shot lengths, same line times as `bp_pic_v2_timing.json`. `write_timing()` was not called. `bp_sound_v1_timing.json` is still `74f55afb586fcbb0f5b643063b0279bf`.

Shot 01 hides the wall portrait and drops `fs.portrait` from the peg (508, 128) to the floor beside Don's feet. The olive rectangle is gone. The locked s0 still still has the portrait on the wall.

Shot 04 runs the fuse across the 90-frame insert. Confetti leaves the muzzle toward the ARCHIVE bin. The hold after is that same cannon, spent, with a few pieces on the floor.

On "I'm matching them." only, `plan_patched` is on the desk and Pam's hand, the series `point`, sits on a tape seam. The sleeve is her purple and starts at the fist the room already draws (705, 341). Earlier night lines keep the plan hidden. Shots 06–13 keep the desk sheet at 0.15. The stamp was not redrawn.

`bp_picture.py beats` exits 0. `beats --plant` exits 1: an olive board is caught, a fuse at 0 with no confetti is caught, a sheet with no hand is caught, and a hand with no arm is caught.

## Watched cold, 26 Nov 2026

Two fresh viewers, [I](0f3375b4-fdc7-4442-8a3b-ac458a3f13ef) and [J](c775c735-83e1-48fc-a6db-cf321cc6c07d). Frames of the three beats, the shred, the zero, the pocket and the stamp, slate cropped, plus the five questions.

Pass: both say the falling thing is a framed face, the cannon fires, and the woman at the desk is matching the strips. Both at 4 of 5 or better. **Pass. 5 of 5 and 4 of 5.**

| Question | Viewer I | Viewer J |
|---|---|---|
| What falls? | A framed picture, a man with a bandage on his forehead | A framed picture, a portrait of a man with a bandage |
| What does the cannon do? | Fires blue confetti, then sits spent | Fires a burst of blue confetti, then sits spent |
| What is she doing with the strips? | Matching them. Numbered garages | Matching them. Numbered garages |
| 1. What did the Client lose? | His blueprint | His blueprint |
| 2. What does Don do with it? | Pushes a sheet into the slot labelled ARCHIVE | Pushes a sheet into the machine labelled ARCHIVE |
| 3. Does the search find it? | No. The poster shows 0 found | No. The poster shows 0 found |
| 4. Who finds it in the end? | Brown bob, headset, purple top, holds the card up at the desk | The older woman: grey hair, glasses, pearls, green jacket. She finds it in his pocket |
| 5. What does the robot stamp? | CUSTOMER SUCCESS | CUSTOMER SUCCESS |

## Beats that read

- The thing that falls is a framed face. The wall copy is gone for that shot. On the hold it is on the floor beside Don.
- The cannon fires. Both said so. On v2 it read as a striped cone that had fallen over.
- Pam joins the strips. Both said she is matching them. Her name is not printed.
- Don shreds. The search stays at 0. Viewer I names the finder as the woman in the purple top. That is Pam's body.

## The one miss

Question 4, Viewer J only. The finder is the woman with the brown bob, glasses, purple top and headset. J named the older woman beside her. I did not. It is not a miss from both, so it does not spend v4.

The stamp drew CUSTOMER SUCCESS, and this time both read the two words. v3 was not spent on redrawing it.
