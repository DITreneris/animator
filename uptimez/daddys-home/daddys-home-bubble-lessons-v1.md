# Daddy's Home: speech bubbles, every lesson that applies (collected 22 Nov, before redoing them)

Source: `docs/lessons.md` (line numbers), the Best Candidate code on `main` (`bc_sb.py`, `qa_bc.py`), PR #62, and Tomas's standing rules.
Animation v2's bubbles (`dh_speech.py`) broke most of the rules below. Next to each rule: **v2** says how v2 broke it.

## Where the box goes
1. **Beside the face, level with the mouth, on clear wall** (167, 174, 325). **v2:** kept the box in the top band and joined it to the mouth with a long tail.
2. **No wall beside the face? Reframe the shot, don't stretch the tail** (358, 167): Best Candidate moved twelve shots and no lines. **v2:** used long tails, then named cards.
3. **Tight two-shots:** above the head or into clear wall, not beside the mouth where the other face sits; a repeated line goes in the same spot (253).
4. **The box stays off ears and hands in its own rows,** not only off the cheek (361).
5. **The box is measured once per shot and held still;** only the tail follows the head (362). **v2:** the box jumped and the bubble type changed mid-line.
6. **Size the box from the measured text, at 540 scale** (279, 375). Don't squeeze lines into narrow 3–4 line boxes. **v2:** squeezed them.
7. **Safe zones:** not under the top bar (y 96), not in the bottom quarter (y ≥ 720), not under the right rail (x > 470, y 380–860) (555, 568, 691).
8. **No bubble on anyone's skin, on a sign or on the price tag; signs are whole or out** (33, 269, 335, 691).

## The tail
9. **Short tail from the side:** 10–20 px, level with the mouth, is unmistakable (174). Best Candidate draws a straight triangle from the box's edge: `[(ex, ty-11), tip, (ex, ty+11)]`.
10. **The tip lands on the outline of the cheek at mouth height, on the side facing the box; never over the eyes or into the mouth** (325, 339). **v2:** the tip went into the mouth corner and read as a straw.
11. **Aim at the head as drawn in that drawing:** `measure()` renders the speaker alone and reads the mouth (open vs shut), the cheek (the last skin walking out from it) and the crown (357).
12. **Walk from the tip toward the centre of the face: the mouth starts within 0.4 of the face radius;** on a tipped head, walk along the head's own axis (398).
13. **Hair beside the cheek (Sofía, Pam, Mom):** the box stands clear of the hair and the tail runs over it to the cheek; limit how much wall the tail crosses (26 px), not its whole length (360).
14. **From above only onto a bare scalp or the robot's antenna,** touching it, and only where faces sit either side (Don between two). Anyone with hair gets a side bubble or a new framing (359).
15. **A tail ending near the hair reads as pointing at the hair; a long tail across a doorway reads as the door talking** (159, 167). **v2:** its long "rope" tails are this fault.
16. **Off-screen speaker:** quoted card with the name, no tail (551). Only for someone actually off the frame. **v2:** used cards for on-screen speakers too.
17. **Nothing sits where the tail leaves the box** (603). **v2:** the tail was drawn in the same path as the box with the opposite winding, so where they overlap the fill dropped out and a cut-out showed at the tail's root.

## Timing and the mouth
18. **The bubble is on from the first syllable and gone one drawing after the last word** (362).
19. **Whose mouth is open decides who speaks:** close the listener's mouth (173).
20. **A face wrapper can paint over the talking mouth:** draw the mouth after it (272); scale the mouth with the figure (554).
21. **One table (`SAY`) for every line's bubble,** read by both the board and the animation (363).

## The check
22. **The check reads pixels, not the drawing's own numbers** (348). Redraw the frame with the speaker left out, with the mouth forced open and shut, and with skin in a marker colour (349). Use `qa_bc.py`'s tests as they are; extend them, don't rewrite them.
23. **Check every drawing,** not a sample (351).
24. **"Clean" means only what the checker tests** (395). Before sending, look at frames at full size, including the joint between box and tail. **v2:** never looked before sending.
25. **Check a claim against the code and the frames before telling Tomas** (175, 464).

## Code to reuse (approved in Tomas's reviews)
- `bc_sb.py`: `measure(name)`, and `bubble(k, lines, who, form="R"/"L"/"T"/"off", ...)` with `lock` to hold the box still, `hair=True` for hair beside the cheek, and `SAY`.
- `qa_bc.py`: `tail_checks()` and the rest of its tests, with a self-test of planted faults.
- The episode's own style stays the same: white rounded boxes, Father's in dark red, the robot in mono type.

## Plan
1. Port `bc_sb.bubble`, `measure` and `qa_bc` into Daddy's Home. `dh_speech.py` / `dh_tailcheck.py` are dropped; they stay unused files, not deleted.
2. Shots with no wall beside the face get a new framing:
   - Don under the price tag: scenes 1, 2, 4, 5;
   - Mom at the frame edge: scene 3, 4.1′ / 4.3;
   - Don with his hands up: 2.2.
3. Send six frames at full size first: a side tail, the joint between box and tail, Don from above, the robot, Sofía/Pam with hair, and a card for an off-screen speaker. The film is rendered only after Tomas's ok.
