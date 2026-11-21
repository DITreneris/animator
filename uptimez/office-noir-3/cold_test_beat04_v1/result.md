# Cold tests 18 and 19: beat 04, the arena door and her office, as stills (20 Nov)

New: `src/door_on3.py` (4.1 from behind him, 4.2 his face three times). Her office is `src/office_on3.py` (passed alone in `cold_test_office_v1`). Four fresh viewers.

Intended: 1 he comes to the arena's back door and sees the ring · 2 over the ring hangs the plan, 10 GARAGES, the prize, an angry robot boxer under it · 3 he looks at the roll, at the folder under his arm, at the roll: that, not this · 4 he pays a hundred for the fight · 5 she takes it without moving; the power is hers.

## Round 1 (eight frames): 4 and 3, fail

| # | Viewer G | Viewer H | Verdict |
|---|---|---|---|
| 1 | Read | Read | Read |
| 2 | Read ("the prize on the banner, 10 garages") | Read ("prize or sponsor") | Read |
| 3 | Half: "the paper shows only its blank back" | Half: "a blank sheet" | **The folder was drawn from its back: a blank slab** |
| 4 | Read ("entry fee or stake") | Misread ("to be paid… fee, stake or a bet", whose hundred?) | **The note was hidden behind his glove in 4.3 and "teleported" to the desk** |
| 5 | Read | Read | Read; the hand could be "pushing it at him" |

## Round 2 (nine frames): 4 and 4, pass, narrowly

Changed: her photograph sticks out of the folder (4.2); the hundred is held out whole past the glove (4.3, `over(show=True)`, opt-in; `office_on3_v1.py` is v1); 4.4 starts with the note still between his gloves.

| # | Viewer K | Viewer L | Verdict |
|---|---|---|---|
| 1 | Read | Read | Read |
| 2 | Read (prize) | Half ("a prize, a sponsor, the stakes?") | Read by one; in the film the plan is set up in beat 02, which these frames do not include |
| 3 | **Misread: he wants the prize "for the woman in the photo"** | Read ("one sour sideways glance… something he would rather not look at") | Split. A look is not an action (rule 1 in `ring-set.md`): this needs a gesture, e.g. the folder pushed down out of frame as the glove goes up |
| 4 | Read | Read ("the 100 is what it costs him") | Read |
| 5 | Read | Read ("mob-boss granny") | Read |

Open, named by both: frames 2 to 4 look like one frame at phone size (only the eyes move); the note still jumps from his chest to her end of the desk; the door behind him in her view could be "a mirror or a chair back"; HR on the robot's belt and the hats are lost at phone size; the button is "an ashtray"; who the woman in the photograph is (told in beat 02).

Limits: a fragment test. Whether 10 GARAGES reads as his own plan, and the folder as the contract he was given, is for the whole-board test.
