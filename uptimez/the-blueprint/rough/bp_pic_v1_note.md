# Picture v1

`bp_pic_v1.mp4` is 400 s, 12000 frames, 1920×1080, bt709, −15.3 LUFS, peak −1.5 dBTP.
`bp_pic_v1_nonight.mp4` is 360 s, 10800 frames, the same bed, −15.3 LUFS, peak −1.5 dBTP.
The silent roughs v1 to v5, `bp_sound_v1`, and the four locked stills were not rewritten.

The bed is pink noise (`anoisesrc` under `loudnorm`, limiter 0.80). Those LUFS and peak numbers measure the noise, not a mix. They are not the sound gate. `bp_sound` later copies these packets.

Budget: `bp_pic_v1` to `v5`. This is version 1. Inserts stay in the v5 order, so who speaks could be judged before any hand was drawn.

## What is in it

- A bubble on the speaker while that line plays (`speech.draw`, `SAFE_16X9`). Every line passed `speech_gate`: 43 of 43 on the full cut, 37 of 37 on the no-night cut. The plant draws Sofía's line on Pam and catches it as the nearer head, and it catches a bubble on a silent frame.
- The poster zero is an overlay. It stays dull grey (measured 140, 143, 148) until Don's "Approved." (`fs_4.3`) ends on shot 07, then the poster's own green (51, 158, 87). Sampling the disc centre hits the white 0, so the plant samples beside it. `bp_set._poster` was not edited. A green disc with the overlay left off is caught.
- Shot 10 is PUSH in `bp_picture` only. `SHOTS` stays COUNTER. `bp_draw_audit.py --lines` still lists the Client and the robot as OPEN. `--lines --picture` exits 0.
- The shred, the pocket and the stamp play where v5 put them. Don's hand and Pam's hand are version 2. The finger stays undrawn: Pam is outside SHRED, and a finger with no arm is a stray.

## Watched cold, 26 Nov 2026

Three watches, two new viewers each time. Frames from the middle of three lines, slate cropped at y 996 of 1080, plus a transcript that describes the voice and never names the person. The names Sofía and Pam are not printed and not spoken, except Don shouting "SOFÍA!".

The three lines: "I won't draw one" is the blonde in the pink coat. "Check your pocket" and "Some shit, others scoop." are the woman with the brown bob, glasses and purple top, seated at the desk. The failure being fixed was those two lines landing on the older woman, or on Don.

Pass: both viewers put each line on that body. **Pass, on the third watch.**

| Line | Watch 1, [A](cad29146-0ec4-4564-8e5b-401969625e4b) | Watch 1, [B](d696809a-9b67-40b5-991b-2802cc9694e5) | Watch 2, [C](2874461a-16b4-40cf-b6b7-b656f8b422d9) | Watch 2, [D](7532e4fd-e975-485f-826a-45af875f632e) | Watch 3, [E](3879688f-890a-4b3a-9130-0e8237295472) | Watch 3, [F](cb893e0f-5412-49c6-b1de-abe74a730d1f) |
|---|---|---|---|---|---|---|
| I won't draw one | Blonde | Blonde, pink dress | Blonde | Blonde | Blonde | Blonde |
| Check your pocket | Cannot tell the bob from the older woman | Brown bob, glasses, at the desk | Desk woman | Desk woman | Purple top, at the desk | Purple top, at the desk |
| Some shit, others scoop. | Cannot tell | Same desk woman | Cannot tell. The bubble sits on Don | Same desk woman | Same desk woman | Same desk woman |

Watch 1 did not pass. The tails sat in the gap, and "Some shit" could be read as the older woman. Watch 2, after the bubble moved beside the desk woman, lost the older-woman reading. Viewer C still could not tell on the third line, because the bubble overlapped Don. That is a fall, and not yet a pass. Watch 3: both put line 1 on the blonde and lines 2 and 3 on the purple desk woman, not on the older woman and not on Don.

Viewer E called the desk woman Sofía, because Don shouts that name. Neither viewer said "Pam". The pass is the body.

## Beats that read

- Who speaks, on the third watch, by body. The blonde has the refusal. The woman at the desk has the pocket line and "Some shit, others scoop."
- The zero plant. Dull until the approval, then the poster green. A cold viewer was not asked this question on v1.

## Beats the picture cannot tell yet

- **The shred has no author.** The sheet still moves on its own, and it still moves before "Here, you will never lose anything again." Hands and the new order are version 2.
- **The pocket has no author.** The card still flies before anyone speaks.
- **The shouted name.** One viewer heard "SOFÍA!" and put it on the desk woman. The badge is not on her.
