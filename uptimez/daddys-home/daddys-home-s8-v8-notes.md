# Daddy's Home, scene 8 v8 "Find My Money" (24 Nov)

`src/dh_anim8_v8.py`: v7's scene (`dh_anim8.sc`: clock, takes, mix) through `dh_anim_v8`, on the set as scene 7 v8 left it (`dh_anim7_v8`). 2 rounds.

Lessons applied: rules §0 and Gestures ("two people's hands near = a handshake"; "a hand at the ear = a phone"); 245 (an arm without a body); 179 (reach: the guard's IK is clamped to 98 % of his arm); 224 (the sheet first, then the fingers over it); 263; 417/264; 178.

## What changed

- **Set:** the throne on its mark (452), Father at 376 and Don in front of the throne, as at the end of scene 7. The values scene 8 computes at import are recomputed: ARM8, POV8, the FOUND box on the tag, Father's head, and the heads `clear_signs` frames on.
- **Father's lines (10.2, 10.4a, 10.4a', 11.1)** are in 9.4''s two-shot, so Don is whole.
  - v7 framed Father close, with Don's raised arm in the frame's edge behind the price tag and his body cut ("an arm without a body, holding the tag", hands audit #6).
  - His boxes are on his left. The portrait sign is pushed out of the top.
- **Don's hand:**
  - scene 7's raised palm comes down slowly over Father's first line (1.4 s), the elbow bent all the way (a straight in-between read "a pole");
  - then his hands are at his sides;
  - v7's rectangle thumb and "(( ))" marks are gone.
- **9.6, 9.6' (the CV):**
  - she holds her CV up in front of her on his side, her fingers on its lower edge;
  - his hand comes to its top edge and draws it away;
  - then it goes into his pocket and her hands are down;
  - v7 had her arm straight out to his hand on the CV, "a handshake".
- **Smaller fixes:**
  - 10.1's card now names FATHER (the adapter named it DON).
  - 11.4 is closer on Pam: her sign is whole and big, and the shredder's "SHRE" behind her leg is out of the frame.
  - 10.4b: her startle jump is a SET_AIR exception.

## Checks

- **Gate:** speech_gate 113 / 0, dead zones 0, set 0. v7 baseline: same.
- **Film v8 with scenes 3–8 v8:** 96.8 s, 2902 frames, 540x960 at 30 fps, −16.6 LUFS, −1.7 dBTP.
- **Whisper:** 32/36, the same 4 misses as before, all in other scenes (two are the script file's outdated text). Scene 7 and 8 lines are all heard.

## Cold tests (mute, 2 viewers, the whole scene)

- **Round 1:**
  - the story reads 2/2 (his situation, FOUND, the call); no handshake; the only phones read are Father's and the DAD screen;
  - but the CV "jumps" into the guard's hand 2/2;
  - Don's held palm reads "a wave or an oath, not an action" and "a pole" 2/2.
- **Round 2:**
  - the handoff reads 2/2 ("he takes it from her, her hands end up empty");
  - Don's hands are "mostly down", the lowering reads "a small wave".

## Open (stopped at 2 rounds)

- The guard's reaching arm, in one drawing (0.6 s), reads "a floating fist over her head" (1/2) or "stiff, a pole" (1/2), and the handoff "for a moment a handshake" (1/2).
- Don's lowering hand near Father reads "a wave, almost a handshake" (1/2).
- The freeze cutaways (Mom, Pam, the visitor) confuse cold viewers who see this scene alone. They are callbacks to scenes 4–6.
