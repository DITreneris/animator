# Daddy's Home, scene 2 v8 "Good News" (24 Nov)

`src/dh_anim2_v8.py`: v7's scene (`dh_anim2`: its own clock, shots and mix) through `dh_anim_v8`, via a small `Bridge` (the attributes `dh_anim_v8` reads from a `dh_anim.Scene`). It now has v8 bubbles, dead zones, set_gate and a mode without bubbles (`nobub`). 2 rounds.

Lessons applied:
- rules §0 and Gestures ("a hand at the ear = a phone"; "a finger near a sign = holding it"; "two people's hands near = a handshake");
- reach (179: the elbow bent at least 40° by a search over the arm's angles);
- "contact all the way";
- a shape per state (207: `palm` on the push and the oath);
- 263, 417/264, 178.

## What changed

- **Set:**
  - The throne is on its mark (452) from 2.3a on. v7 had it at 400 from 2.3a, a jump of 52 at the cut from 2.2.
  - The step out, the roll out and back, and the cameras move with it.
  - `SET_MOVES` covers the shove, the roll back and the bump; `FLYING` covers the throne leaving and re-entering the frame.
- **2.3a, 2.3b ("The money... was invested."):**
  - v7: a straight arm to the throne's arm ending in a mitten, "a pole" (2/2, whole-film test).
  - v8: his palm on the throne's arm with the elbow bent (≥40°), the poses searched to keep the hand on it while it is in reach; then a bent follow-through and down.
- **2.2 ("I didn't steal anything!"):**
  - v7's `shock` fists beside his ears read as "holding the price tag" (2/2, stills).
  - v8: both palms up (stills test: "hands up, not me", "don't shoot" 2/2); the near one at his shoulder, under his box and off the tag at the top of the jump.
- **2.5:** his hands down. v7's `vest` pose, hands clasped at his chest, read "a handshake" 2/2.
- **Cameras:**
  - 1.3 is moved up and left: Sofía's box clear of the button rail and the shredder's SHRED out of the frame.
  - 2.2 is wider: wall for his box.
  - 2.5' is a step right and down: the tag's swing out of the title bar.

## Checks

- **Gate:** speech_gate 77 / 0, dead zones 0, set 0.
- **Film rejoined:** 96.8 s, −16.6 LUFS, −1.7 dBTP.

## Cold tests (mute, 2 viewers, the whole scene)

- **Round 1:** the story and "hiding the spending" read 2/2. Still open after round 1:
  - the push "a pole" 2/2;
  - a one-palm oath "touching his ear / headset" 2/2;
  - 2.5's clasped hands "a handshake" 2/2.
- **Round 2:**
  - the story 2/2, the punchline ("the money went into the throne") 2/2;
  - the push reads "he points back at the throne with an open palm" 2/2, no pole.

## Open (stopped at 2 rounds)

- **The oath palm by his head** still reads "at his headset / ear" 2/2. It is the third ear read, so rule 178 says change the gesture: hands clutching his chest, or both hands up high.
- **His hand on the throne's arm** reads "shaking hands with the chair" 2/2.
- **The empty frames after the throne rolls out** (the coat stand and a red dot on the floor) confuse 2/2. This is v7's.
