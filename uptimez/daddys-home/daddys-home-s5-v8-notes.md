# Daddy's Home v8, scene 5 "The Filter" (24 Nov)

`uptimez/src/dh_anim5_v8.py`: v7's scene (`dh_anim5.sc`: clock, takes, mix) run through `dh_anim_v8.py` (v8 bubbles via `dh_anim3_v8.say`, the dead-zone check and `set_gate` on every drawing), with only the shots that failed redrawn. `dh_anim_v8.py` is meant for scenes 6–8 too: a scene's v8 module patches `sc.DRAW[...]` and calls `frame`, `gate`, `run`.

## What changed

- **Set:** the throne on its mark (452; v7 418 in 7.1a', 7.3, 7.5, 7.7), Don in front of it with it, the close cameras on him following (+34, his face out of the app buttons). Mom and Sofía on two floor lines (F+22, F+2) and further apart (v7: overlapping on one line).
- **7.2a, 7.2a':** the brush hand from the left edge as a hand and cuff stub (`insert_cuff`), the brush drawn first, the fingers over it.
- **7.6:** the invoice drawn first at his hand, his fingers over its edge (v7: the sheet hid his hand).
- **7.8:** Pam's mug in her hand's coordinates (one hand, two passes), the sip at the middle of her mouth, tipped; her arm below her eyes (v7: the mug hung beside her hand, her sleeve crossed her glasses).
- Exceptions listed in the module: the flinch off the floor (7.1a'), the filter's flight out of the top (7.2a'', 7.2b, 7.3's first drawing), the invoice sliding in at the edge (7.6).

## Checks

speech_gate 72 / 0, dead zones 0, set 0; −17.7 LUFS; v7 baseline same. Film v8 (scenes 3, 4, 5 v8): −16.6 LUFS, −1.5 dBTP, speech 32 of 36 (the 4 misses are in scenes 1, 2, 5's "Incident logged." and two of them are the script file's old text).

## Cold tests (2 rounds, 2 viewers each)

- Read 2 of 2 both rounds: he fixes it with one touch, the POP, the filter on the CEO's head, REC, he laughs, the $80 invoice, the smile goes, Pam drinks.
- Round 1 → 2: Pam's mug "could pass for a phone" → not mentioned; Mom and Sofía "merged" → "borderline, touching at the shoulder".
- Tried and dropped: his hand on the case as it comes down (7.1a): at head height it read "on the phone" 2 of 2, worse than v7's case alone ("hangs in the air").
- Open: the brush hand "a floating fist" for one drawing as it comes in; the case insert (7.1b) "a random grey box"; the invoice arm "a stiff rod" (1 of 2).

## Round 3 (24 Nov, after the whole-film mute test): the brush

- **Fault:** 7.2a and 7.2a' read "a fist hits the machine", "a fist-bump / a handshake" (2/2, whole film). v7's 4 cm brush was hidden under the fist.
- **Lessons applied:** rules §0; holding ("a tool's handle comes out past the fist", "hold an object where its shape shows"); inserts 224/225 (a hand plus a cuff stub from the edge); 263; 417/264.
- **Fix:**
  - The brush is drawn at 2.0x (`BRUSH_S`), with the fist on the middle of its orange grip.
  - The tuft rests on the machine's light grey panel (`TIP_DX`, `TIP_DY`); on the dark group head it was lost 2/2.
  - The reach starts with the hand already in the frame.
- **Stills test** (4 sizes and positions, 2 viewers): "a fist holding a tool, not a handshake or a fist-bump" 2/2. The orange grip makes it a tool (2/2).
- **Checks:** gate speech 72/0, zones 0, set 0; baseline same; film rejoined.
