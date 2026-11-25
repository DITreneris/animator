# Pick a Side: lessons that apply to the round 1 review fixes (24 Nov)

These rules were collected from `docs/lessons.md` (line numbers given) and `docs/rules-hands-and-phones.md` before any code was written, following `CLAUDE.md` "Before writing any code". They cover Tomas's picks: 6.1 re-staged for phone size, 4.2 as the Client's finger on the heel, "BOTH." on the arms frame, the scene 2 cuts, the small actions (2.4, 2.6, 5.3, 5.5, the portrait), and the loop with Pam's phone buzzing in 6.1 and 6.2 matching 1.1.

## 6.1 at phone size

- **266.** One obvious object beats five small ones at phone size. The CV with COO? is the object.
- **593.** A payoff frame needs one thing to read. Use a tight insert or push in, not a wide shot carrying eleven texts.
- **191, 528.** Push in 1.3–1.6× on punchlines and on the turns only.
- **829 (193).** A deep audit finds what no gate measures: the thing the meaning rests on is too small, cut off or not drawn. That describes 6.1 now: the CV is about 8–20 px.
- **711 (98).** The biggest face is r 78–80 (540 space), near y 400. Nothing that carries the story goes below y 720 or into the button rail.
- **253.** In a tight two-shot the bubble goes into clear wall, not beside the mouth where the other face is.

## 4.2: the Client's finger on the heel

- **753 (134).** An insert needs an owner. A hand alone was read as "a dial", or as someone else's hand.
- **909–911 (222).** Insert arms failed 3 of 3 at every length. Draw the hand and a wrist stub only (`insert_cuff`); the owner is known by his hand.
- **925 (224).** A hand-only insert works only at the frame's edge. Mid-frame, the hand needs its owner visible. For 4.2 that means the Client's finger comes in from the frame's edge onto the phone, with his oily print and dirty nail (the Client's hand, canon).
- **`rules-hands-and-phones.md`.** Use the series' hand (`kit.HAND`, the "point" shape), one hand for the whole cast. The phone UI is drawn once, with nothing under ~9 units.
- **573 (38).** An insert must not float. A limb comes out of something: here, the frame's edge.

## BOTH. and the scene 2 turns

- **524 (20), 714 (101).** A story turn is an action, not a glance. Keep the eyes still and give the turn to a hand and a prop.
- **517–518 (17).** Adding reaction shots costs time; don't pay for it by cutting the setup. That is why 2.1b, the card going on, is re-staged rather than cut.
- **620 (53).** Reactions face their target.
- **922 (222).** A joke read by 0 of 3 is cut, not repaired. 2.12 is cut because it repeats a framing.
- **931 (195).** Trim before you animate, and test a reversed decision on the shot itself.

## The small actions

- **655 (70).** A held prop takes its position from the hands, not the other way round. This applies to Pam's cup in 2.4 and Sofía's CV in 5.5.
- **399.** Every held prop needs an arm, and the prop is drawn at the hand the pose returns.
- **726 (110).** One prop, one place. This applies to the portrait when it is lowered.
- **529 (25).** Signs and plants must read at 270 px.

## The loop

- **19.** Loop through a character's action, never by repeating words at the join.
- **257, 819 (183).** A matched loop rewinds state, not just the picture. Every object the film changed must be changed back on screen. The blinds have to be whole and down in 6.2 as in 1.1, and only Pam's re-hanging in 5.3/5.6 can explain why.
- **659 (74).** A strong loop ends on frame 0's exact shot.
- **624 (57).** Frame 0 is drawn by the same code as frame 1. 6.2 has to be drawn by 1.1's own function.
- **271.** A narrative loop can beat a seamless one: "he learned nothing".
- **762 (143).** A loop of actions is checked against the set, not the frame.
- **827 (191).** Two plot threads read as two cartoons until one prop names the join. Here that prop is the INVITATION · DAD phone, and it is also the loop's trigger.

## After building

- **889 (213).** A new check finds old faults, so run it on the approved board too.
- **618 (51).** Cold-test the whole board, not just the hook. After these changes, test the changed frames on 3 new viewers, then the whole board.
