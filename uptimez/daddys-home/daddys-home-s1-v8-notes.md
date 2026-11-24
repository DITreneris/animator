# Daddy's Home, scene 1 v8 "The Call" (24 Nov)

`src/dh_anim1_v8.py`: v10's scene (`dh_anim1`: its own clock, drawings and mix) through `dh_anim_v8`, via `Bridge1`. The bridge turns `dh_anim1.frame`'s branches into shots and inserts. The scene now has v8 bubbles, dead zones, set_gate and a mode without bubbles. 2 rounds.

Lessons applied:
- rules §0;
- "A phone in a hand": `of_cast.phone_grip` for every phone; upright when it must be read (200); the holder visible;
- 179 (the phone at the ear on an arm with the elbow out);
- 178 (change the gesture after the grip fails);
- 263, 417/264.

## What changed

- **The call (0.4, 0.5b, 0.6, 0.7b):** the phone is in his hand, in `phone_grip`, held up in front of him on speaker with DAD on its screen. The arm comes from his own shoulder with the elbow bent (searched).
  - v10 had his hand behind his head and the phone by his cheek, not in it (hands audit #1).
  - At his ear, in the series grip, the phone "is stuck to his cheek" 2/2: his head is wider than his arm is long, so the hand cannot reach round it with the elbow out.
  - In 0.7b the call ends: the screen goes dark and the phone tips as his hand drops.
- **Father's lines** (the booth, his face above the frame, and "I arrive at five." through the phone) are on named cards (FATHER), as an off-screen speaker.
- **0.2b** (the seat's drop): `ymin` 320, so `clear_signs` does not push the camera so far that the price tag goes under the title bar on the first lift.

## Checks

- **Gate:** speech_gate 94 / 0, dead zones 0, set 0.
- **Film v8, all eight scenes now v8:** 96.8 s, 2902 frames, −16.6 LUFS, −1.7 dBTP.
- **Whisper:** 32/36, the same 4 misses as before; the mix is unchanged. "Good news, everyone!" is the script file's outdated text.

## Cold tests

- **Round 1** (stills: v10, the ear grip, two speaker holds): the speaker hold at his chest "clearly in his hand, on a visible arm", "his dad" 2/2. The ear grip is the weakest 2/2.
- **Round 2** (mute, the whole scene):
  - the story 2/2 (his dad, "Today.", he ends in shock);
  - the phone "clearly in his hand, on his arm" 2/2;
  - read as speakerphone 1/2.

## Open (stopped at 2 rounds)

- **Father holds a tablet, not a phone,** so "how is he on the call" 2/2. This is v10's booth.
- **The spring up from the seat (0.2c):** the arms straight out "like poles" (1/2), the legs "pillars" (1/2). This is v10's.
- **0.7b's dark, tipping phone:** "hung up or dropped it?" (1/2).
