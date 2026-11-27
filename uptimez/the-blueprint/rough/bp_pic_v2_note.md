# Picture v2

`bp_pic_v2.mp4` is 400 s, 12000 frames, 1920×1080, bt709, −15.3 LUFS, peak −1.5 dBTP.
`bp_pic_v2_nonight.mp4` is 360 s, 10800 frames, the same bed, −15.3 LUFS, peak −1.5 dBTP.
v1 stays the attribution picture. The silent roughs, `bp_sound_v1`, and the four locked stills were not rewritten.

The bed is pink noise, as on v1. Those numbers measure the noise. The mix is `bp_sound_v2.mp4`.

## What changed from v1

Shot 03 holds the two promise lines with the sheet still on the desk, shreds for 60 frames with Don's hand on the page, then holds "One month…" and "Approved." The finger's empty frames are in the holds. Pam is outside SHRED, so the finger stays undrawn.

Shot 11 holds "Is this a joke?" with no card in the air, then the card leaves the Client's pocket across "Check your pocket.", and the hold after has Pam's hand on the card. The hand is drawn only once the card has reached her (the last tenth of the pocket). Earlier, a sleeve across the room read as an arm from off screen.

Both hands are `point` from `hands_ps`, chosen off the existing sheet. Don's sleeve is his shirt white and starts at the fist the room already draws (508, 411), index on the sheet, width 20. Pam's sleeve is her purple and starts at her fist (705, 341), the fingertip stopped on the card, width 16. `bp_draw_audit.py --hands` exits 0. `--hands --plant` exits 1: a sheet with no hand is caught, and a hand with no arm is caught.

Times for these seven lines are `bp_pic_v2_timing.json`. The other lines keep their v1 times. `bp_scenes.timeline()` is still the v5 order, and `write_timing()` was not called, so `bp_sound_v1_timing.json` stays `74f55afb586fcbb0f5b643063b0279bf`.

Bubbles: 43 of 43 and 37 of 37 still pass `speech_gate`. The zero overlay is the v1 overlay.

## Watched cold, 26 Nov 2026

Two fresh viewers, [G](32a0b079-1046-43bf-b18a-0f6f3a057a46) and [H](a18e20df-b1c0-4991-8ded-c1a5d677e872). Line frames, four shred frames, four pocket frames, slate cropped, transcript by voice. Open prompt first, then the five questions.

Pass: both at 4 of 5 or better, and both say Don puts the page in the shredder and the desk woman finds the card. **Pass. 4 of 5 each.**

| Direct question | Viewer G | Viewer H |
|---|---|---|
| 1. What did the Client lose? | The blueprint | The blueprint |
| 2. What does Don do with it? | Feeds a sheet into the ARCHIVE shredder | Shreds the page in the archive machine |
| 3. Does the search find it? | No. The search stays at 0 found | No. The search stays at zero found |
| 4. Who finds it in the end? | Brown bob, glasses, purple top, headset, at the computer on the right, holding the blank card. No name printed | Short brown hair, glasses, purple top, headset, seated at the desk, holding it up. No name printed |
| 5. What does the robot stamp? | The zero, turned green | A blank yellow circle on the clipboard |

## Beats that read

- The lost blueprint.
- Don puts the page in the shredder. Both said so. On v5 and on the sound rough, both could only guess.
- The search stays at 0.
- The finder is the woman at the desk: brown hair, glasses, purple top, headset. That is Pam's body. Her name is not printed, and neither viewer said it. On the sound rough both gave this beat to the older woman.

## Beats that do not

The same question from both, with different wrong answers, so it is not the shared staging miss that spends the next version. On silent v5 both answered "cannot tell", so this is not a fall on that beat. Questions 2 and 4 did fall: they now read. v3 stays unspent.

- **The stamp.** The robot stamps the words CUSTOMER SUCCESS (`bp_scenes.stamp`). Viewer G read Don's approval, the zero turning green. Viewer H read a blank yellow circle on the clipboard. Neither read the two words.
