# Daddy's Home, scene 7 v8 "The Arrival" (24 Nov)

`src/dh_anim7_v8.py`: v7's scene (`dh_anim7.sc`: clock, takes, mix) through `dh_anim_v8` (v8 bubbles, dead zones, set gate). Round 1 of 2.

Lessons applied: rules §0 and Gestures ("a finger near a sign = holding it"; "a hand at the ear = a phone"); 245 (an arm without a body); 207 (a shape per state); 179 (reach); 263 (feed size); 417/264 (variants, 2 cold viewers); 178 (change the gesture after three misreads).

## What changed

- **Set:** as scene 6 v8 left it. The throne is on its mark (452), Don is in front of it, and the line-up moved +34.
  - 9.1r is reframed, so Don and the price tag are no longer cut at the left edge (zone gate).
- **9.4, 9.4', 9.5'' (hands audit #6):** v7 had his arm straight up along the price tag ("holding the tag"), and the two-shot cut his body ("an arm without a body").
  - Now: a two-shot with both men whole (`CAM2`, 1.8), the tag, the crown and the shredder's SHRED whole.
  - Father ends his walk at 376 (v7 330). That leaves room on his left for his "Approved." box, which he says to the robot, off the frame on that side. In v8's first pass the box sat over Don's head.
- **The thumb:**
  - v7 drew a rectangle on a fist, which read "a raised index finger" and "a phone" (2/2), with white "(( ))" shake marks ("a ringing phone", 2/2).
  - Now it is the series' thumbs-up hand (`hands_ps` "thumb") at 1.3x, on his far hand at shoulder height against the wall: clear of his ear, the tag and Father.
  - The shake is now real movement (±2°).
- `dq.don_zipped` is wrapped (`THUMB`, keeps `_v7`). `r_offer`, `r_approved` and `r_react` are redrawn here.

## Checks

speech_gate 60 / 0, dead zones 0, set 0. v7 baseline: same. Film rejoined with scene 7 v8: 96.8 s, −16.6 LUFS, −1.7 dBTP.

## Cold tests

- **Thumb, round 1** (3 heights, near hand, stills): no phone 2/2; chest height "clearest" 2/2. When Father stood near, it touched his arm, so it moved to the far hand.
- **Whole scene, mute** (4 fps sheet plus a 5 fps strip of the thumb):
  - The story reads 2/2: his throne taken over, the robot and the guards side with the visitor, and he ends sweating.
  - No phone 0/2. Nothing touches the tag.

## Open (stopped at 2 rounds)

- **The thumb still reads as "an index finger" 2/2**, the third such misread (rule 178: change the gesture, not the grip). His far arm, upper arm down and forearm up, reads as "a white V, a checkmark, a pole" 2/2.
- **Seen in v7's shots, both viewers the same way:**
  - the fist on the glass (9.1) reads as "a microphone";
  - a black blob at Father's foot (9.2', his step);
  - floating dashes under the robot (9.5', its hop marks).
  - Also "who says Approved." (1/2): Father's mouth is small at feed size.
