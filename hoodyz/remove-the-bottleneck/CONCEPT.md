# Remove the Bottleneck: concept (ME + MY AI)

From Tomas's promptanatomy.app cartoon "Remove the bottleneck." (23 Nov, deep audit, then all a; set B).
No real brands: the cartoon's four branded AIs become MY AI and three copies of itself.

## The idea in one line

Hoody, coffee in hand, points at the PIPELINE board: "Remove the bottleneck." MY AI splits into four (DELEGATE), ticks
AUTOMATE, DELEGATE, OPTIMIZE, and all four heads turn to him. Four little tailors measure him; he thinks it is a new suit.
They tip him head first into the AI AUTOMATION crate, stamp it BOTTLENECK REMOVED and march it out on their heads, his
thumb up out of the hand slot: "Faster!" The crate comes back to its place, the lid pops: frame 0.

**The joke:** he was the bottleneck, and he gives his own removal a thumbs-up.
**New against Just One Line:** there MY AI pushes him out; here he agrees to it.

## Series check (G0)

| Check | Answer | Verdict |
|---|---|---|
| What Hoody wants | a faster team | yes |
| MY AI takes it | takes the order literally: removes him | yes |
| Ironic surface | BOTTLENECK REMOVED, with his own thumb up | yes |
| One iconic image | the crate carried out on four heads, a thumb up out of the slot | yes |
| Someone who matters sees him fail | HARV signs for the crate as it goes past | yes |

## Protect list (G1): Tomas's choices (all a)

1. **Four copies of MY AI** (DELEGATE as a visible pop), never four brands.
2. **Hoody is the bottleneck**; the PIPELINE board shows it from frame 0 (a tiny Hoody stuck in the neck, circled red).
3. **The loop:** the crate is set down where it stood; the lid pops; Hoody stands up in frame 0's pose.
4. **His thumb up out of the crate, and "Faster!"** (Tomas records it, muffled).
5. **A shipping crate, not a coffin:** plywood, arrows up, hazard stripes.
6. **The tailors:** each copy a different job (height, inside leg, waist with pins, the spec sheet - which shows a crate).
7. **Set B:** its own office - dark teal wall, wood floor, the board, the crate open from frame 0.
8. Release with another episode between this and Just One Line.

## Beats (G2): about 14 s

| # | Time | Action | Reaction / eyeline | Line |
|---|---|---|---|---|
| A | 0.0-1.5 | Frame 0: Hoody points at the board, coffee in hand; at 0.5 s POP POP POP: MY AI is four | Hoody at the board, then the copies | Hoody: "Remove the bottleneck." |
| B | 1.5-3.5 | Two copies hold up the list: AUTOMATE ✓ DELEGATE ✓ OPTIMIZE ✓ BOTTLENECK ☐; four heads turn to him | Hoody sips, smug | - |
| C | 3.5-6.0 | The tailors (k3): ruler, inside leg, waist tape, the spec sheet with a crate on it | Hoody arms out, flattered | Hoody: "New suit?" |
| D | 6.0-8.5 | The crate was rolled in behind him during C; the waist tape is yanked and he goes over backwards into it; a copy on the rim pushes his knees down in (k4) | the copies at each other: a nod | - |
| E | 8.5-10.5 | The lid slams; the copies lift it; only then the stencil: BOTTLENECK REMOVED. (a hold) | - | (stamp) |
| F | 10.0-14.5 | (see The loop, below) The carry (k5): HARV signs for it; a beat later his thumb pops up out of the slot; they set it down where it stood; the lid pops | - | Hoody (muffled): "Faster!" |

Audit round 1 (23 Nov): fixed the C -> D cause (the crate behind him, the tape yanks him over), the K2 empty box (circled
red), the carry (hands under the crate, a tilt), the bubble's tail into the slot, the reveal order (stencil, then the thumb).
Refused: making the hand a middle finger (the protect list: he gives his removal a **thumbs-up**; the hand was redrawn as a
clear thumbs-up), and "Hoody realises at the end" (he never does: that is the joke).

## The loop (Tomas, 24 Nov, all a) - `rough/film.py`, rough 3

The old ending hid the join behind a white flash (last frame against frame 0: 98.8/255). Now the last frame IS frame 0:
`python3 film.py seam` draws both (frame 0 without its bubble, which appears as he starts to speak) and fails unless the
difference is exactly 0.

1. **Out of the left, back in from the right.** The crate's own place is on the right, so they come in and it is there.
2. **His own "Faster!" does it.** The copies obey and sprint; he causes his removal and his return.
3. **The empty office (0.5 s).** The PIPELINE board goes green, the tasks flow, a big tick; it flashes red the moment the
   crate's nose comes back in. The colour change reads on a phone; the tiny Hoody does not.
4. **One bump resets everything.** They drop the crate at its place: the lid flies open, the sticker flies off (the plate
   AI AUTOMATION is under it), Hoody is thrown out in one somersault and lands on his feet at his mark, mug in hand, finger
   coming up; three copies pop away and the fourth trots to its mark. 0.7 s, no flash.
5. **RETURN TO SENDER** is stamped across the sticker when it comes back: nobody wants the bottleneck.

What this changed in the set (so every shot shares one layout): the board is top right in every shot (it used to move);
the crate's place is x 420, wholly in frame (it used to hang off the right edge, its plate under the app's buttons);
frame 0's Hoody points up right at the board, coffee in his left hand, and the copies pop up behind his back.
BOTTLENECK REMOVED is a paper sticker now, not a stencil. The hand slot is at the crate's left end (its front when they
run), so his thumb leads the charge. The mug never disappears: a copy holds it at the fitting and lobs it in after him.
`kp.py`'s k0-k5 still show the earlier layout.

## Sizes and palette (audit, 24 Nov) - `rough/film.py`, rough 4

Measured: MY AI's height keeps the series rule (0.5 of Hoody to the top of its head, 0.61 with the antenna), but it is as
WIDE as he is (367 px against 372), and four side by side need 1468 px of a 1080 px frame: they piled into one white mass
and read as a mob, not as small and innocent. `size_mock.py` compares 1.0, 0.8 and 0.68.

- **The copies are 0.75** (`KC`): MY AI splits into four SMALLER ones (the pop in A shrinks it), and the last one pops back
  to full size at the end, so frame 0 and the series rule are untouched. **HARV stays 1.0**: the leader is bigger than the team.
- Palette (the cast's colours untouched): wall 649DA0 -> 48777E, floor B38960, crate DDB16E; the sticker is near white.
- Soft contact shadows (18 %) under everyone on the floor, and under the carried crate.
- More room between the copies: a neat row of four in B, the carriers 165 px apart under the crate.
- Before: they stand in a row, in step, eyes open. After: they march each on its own foot, eyes happy.
- Refused: cutting the empty floor at the bottom (the lowest 250 px are under the apps' caption and buttons: series rule).
- A change this forced: at 0.75 they cannot hold the list over their heads without hiding their faces, so **the list is a
  sheet taped to the wall** (B). It stays there: its last box is ticked when the sticker goes on (E), and the sprint's wind
  tears it off (F), so the wall is bare again for frame 0. At the fitting the waist tape is hauled DOWN to the small one's hand.

## Props

| Prop | Shots | Place |
|---|---|---|
| Crate (AI AUTOMATION) | A-F | right, x 600, lid up (A-D); shut, stamped (E-F); carried (F); back at x 600 (loop) |
| PIPELINE board | all | upper left, behind Hoody |
| Coffee mug | A-C | Hoody's right hand |
| The list | B | two copies' hands |
| Tapes, ruler, pins, glasses, spec sheet | C | the copies |

## Known gaps

- Title bar: **HIS TEAM** (Tomas). HARV signs for the crate in F (Tomas): drawn as the series draws him (Says Here,
  Make It Better): MY AI's size, gold-rimmed shades. Hoody: the young era (dark hair, no beard), as in every episode since Perfect Date.
- Voices to record: "Remove the bottleneck.", "New suit?", "Faster!" (muffled), maybe a sip.

## Files

`office.py` (the cast helpers, copied from just-one-line), `setb.py` (the set), `tailors.py` (C; v1 kept),
`kp.py` (k0-k5 -> key_poses.png), `set_mock.py` (the three set options).

## The poster (Tomas, 24 Nov) - `rough/film.py`, rough 5 (`film_r4.py`, `setb_r4.py` = before)

The PIPELINE board changed colour (green in the empty office, red on the return) and Tomas read it as flashing for no
reason; and the crate's AI AUTOMATION plate is hidden for half the film (behind Hoody, then under the sticker). So the board
is now a plain **AI AUTOMATION poster** (`setb.poster`): the same in every frame, top right, where he points in frame 0.
This replaces protect-list item 2's board (the tiny Hoody in the neck) and loop point 3 (green / red); the ding and the
buzzer are gone from the mix. The empty office is carried by the torn list fluttering down and out, and the dust.

Text audit (24 Nov), rough 6: the poster lost its three ticks (they doubled the list's) and is 190 px high, so Hoody's hair
no longer covers it; "New suit?" moved left off the poster; the first bubble's tail no longer crosses the poster when he
backs off; SLAM! moved from the crate (yellow on plywood) up onto the wall; RETURN TO SENDER is opaque (BOTTLENECK REMOVED
showed through it). Left: the list is half hidden in C (the stacked copies), by the lifted crate and by HARV in F.

## Sound accents and the new first line (24 Nov) - rough 7, rough 8 (`film_r6.py`, `audio_r6.py`, `lines_r6.json` = before)

Rough 7: a low two-note stab on the red circle (B) and on the sticker (E), a ding on the last tick; "huh" moved off the line.
Rough 8: recording 64 (take 1, tempo 1.4, 1.67 s): "Remove the bottle - NECK", every syllable heard (the old take, 0.9 s,
was heard as "Remove the bottle."; kept as `vo/h_remove_take53.wav`). The line is 0.8 s longer, so the pops wait for it:
`P0 = 51` (was 15), A is 81 frames, the film 470 frames (15.67 s); everything after A moved 1.2 s later.

## Final (24 Nov, all a) - `final/remove_the_bottleneck.mp4`, rough 9

Cold mute test (2 viewers, 5/5 beats each; their shared faults fixed): the fitting is 0.7 s shorter (C 54 frames, the still
stretch cut), the thumb is 1.5x bigger. 449 frames, 14.97 s. Cover: the carry with the thumb and "FASTER!" (both viewers'
screenshot moment). Posting text in `final/POST.md`.

## Cover audit (24 Nov): `final/cover_v2.png` (`final/cover2.py`; v1 `cover.png` kept)

Done: no AI AUTOMATION poster and no list in the cover (less text); the series bar 15 % smaller; HARV's ear was cut by the frame
edge in the film too, so he now stands at x 205 (was 165) in every shot (`film_r9.py` = before; the film is rough 10, QA passes).
Refused: removing the thumb ("it competes with the joke"): the thumb IS the joke (protect list 4), and the cold viewers
needed it bigger, not gone. Not done: cropping the empty floor (the bottom dead zone is the series rule), moving the leader further.
