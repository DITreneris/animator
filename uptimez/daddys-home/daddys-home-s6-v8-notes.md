# Daddy's Home v8, scene 6 "Stand Like One" (24 Nov)

`uptimez/src/dh_anim6_v8.py`: v7's scene through `dh_anim_v8.py` (v8 bubbles, dead zones, set_gate), the failing shots redrawn.

## What changed

- **Set:** the throne on its mark (452; v7 418); Don, Mom and the line-up move with it (+34); the cameras on them follow and step back so each speaker has wall for the box (the two-shots had no wall between the faces: lesson 253, reframe).
- **8.3, the zip:** Mom is in the shot (a two-shot) and zips him with her own arm, IK to the pull, over 0.85 s (v7: Don's close shot and a teal sleeve from the bottom-left corner, "a tube" in the hands audit). Her line has her own bubble now (v7: from off the frame).
- **8.4a, 8.4c:** Sofía holds her CV at her side, her fingertips on its edge (v7: the sheet beside her hand, "the CV floats").
- **8.2', 8.2'':** the filter she holds low 22 nearer her, whole in the frame.
- `set_gate` logs `sofia_dh` too. `dh_anim_v8` shows a named card for an off-screen speaker (`sc.CARD8`), and lets an entrance pass under the app buttons for its first 2 drawings.

## Checks

speech_gate 38 / 0, dead zones 0, set 0; v7 baseline same.

## Cold tests (2 rounds, 2 viewers each)

- The CV: "holds a CV" 2 of 2 (v7: floating). No arm "from the corner" any more.
- The zip, round 1: "snaps shut, whose hand?" 2 of 2; round 2 (0.85 s pull): "closes bit by bit" 2 of 2, whose hand "probably hers" 1, "his own" 1.
- Open (v7's, not changed): Don's hands up at his head on "Mom! I'm..." read "on a phone" 2 of 2 (rules: a hand at the ear is a phone); the filter on his head reads "a toupee"; the HAND OF THE CEO beat has no setup in this scene.
