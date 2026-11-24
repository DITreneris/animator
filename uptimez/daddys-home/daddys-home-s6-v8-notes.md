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
- Open (v7's, not changed): the filter on his head reads "a toupee"; the HAND OF THE CEO beat has no setup in this scene.

## Round 3 (24 Nov): Don's hands on "Mom! I'm..." (8.2')

v7 had both hands up at his head, which read "on a phone" 2 of 2 (rules: a hand at the ear is a phone). Lessons applied: rules §0 and Gestures; 417/264 (silhouettes, 2 cold viewers); 263 (feed size); 178 (change the gesture, not the grip).

- 12 gestures drawn at feed size, 3 sets, 2 cold viewers per set. Hands out to the side lost the near hand behind Mom ("a stub" 2/2). Winner: near arm down, far fist flung up in protest ("clearest" 2/2, no phone, both hands whole).
- With the bubble on, the fist sat under the box. `r_lick` now logs his hands (a `kit.HAND` spy) into `A3.AVOID_EXTRA` for this line only (cleared in `frame8`), so the gate also fails a box over the fist. The fist was raised above the box: `LICK_POSE = (-8, 0, 130, 25)`. More elbow bend (50–70) pushes the box onto his face (gate fail).
- Motion test (10 fps strip of the render, 2 viewers): protest fist 2/2, phone 0/2. Known: 1 of 2 calls the forearm from behind the box "a pole" (the box hides the elbow).
- Gate: speech 38/0, zones 0, set 0. Film rejoined: 96.8 s, −16.6 LUFS, −1.7 dBTP.
- Seen, not changed (v7's 8.2''): Mom wipes his forehead with a closed fist, which reads as "knocking" (1/2) or as his own hand (1/2).
