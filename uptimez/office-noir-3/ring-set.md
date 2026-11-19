# The ring (set v4)

The room of beats 05 to 07 of *Office Noir 3: The Last Round*. Built by `src/ring_on3.py` (draws it, holds the cameras) and `src/ring_sheets_on3.py` (the three planning sheets). Sheets: `on3_ring_set_v4.png`, `on3_ring_plan_v4.png`, `on3_ring_blocking_v4.png` (v1 to v3 kept; `src/ring_on3_v1.py` to `_v3.py` draw them). The frames' casts are in `src/ring_casts_on3.py`.

## Zones: each with one job

| Zone | World x | Job | What's there |
|---|---|---|---|
| A | 0–250 | His corner: repair and the glove gags | The post with a pale pad, the stool with the folder, the bucket; Pam |
| B | 250–480 | Centre: the fight, the ask, the punch | The lamp; under it his plan, level on two cords, one end let down; the Referee a step behind the line between them |
| C | 480–720 | Its corner: the machine, serviced | The post with a socket, the cable, the oil can; the lit doorway behind it is the way out |

## Depth, back to front

The hall and the doorway · the far crowd (one dark mass; cuffs with money in 5.1 only) · the far posts and ropes · the canvas and the cast · the near ropes and posts (the master only) · the apron, Sofía's lane · the ringside hats.

## Home positions (world x, feet, scale)

Pam 88, F−16, 0.70 · the Client on the stool 152, F−36 · the Client fighting 296, F−42, 0.49 · the Referee 368, F−88, 0.49 · the robot fighting 452, F−46, 0.57 · the robot in its corner 600, F−52 · Sofía on the apron, right to left, F+108, 0.92. F = 1400; the canvas runs from F−110 to F+30.

## Ways in and out

- **The Client:** through the ropes on A's side, once, in 5.1.
- **Don:** in from our side to the stool; out across B under the plan to the doorway behind C.
- **Sofía:** along the apron, never onto the canvas.
- **Mom:** never here. Her word arrives on the robot's screen.

## Camera setups

R1 the master (post to post, the lamp, the plan, the lane) · R7 his view of the plan from below (its own drawing, `ring_on3.plan_pov`) · R2 centre, the two of them with the plan's end over them · R3 his corner, square on · R4 its corner · R5 straight down (its own drawing) · R6 low, looking up at the plan. Inserts and the closes of 7.2 and 7.5 are their own drawings.

## What the first frames showed

- **5.1 does not work as one shot.** In the master the Client is about 140 px tall and the robe gag will not read. The plan sheet splits it: 5.1a (R1, the room and Sofía) and 5.1b (R3, the robe). Script v12 has the split.
- **In 5.2 the Referee stands behind the robot,** not between them: with him between, the stopped glove read as landing on his shirt. Script v12 has it so.
- **C is visited once** (6.2, half a frame). If 6.2 is cut, the socket and the oil can go with it.

## Cold tests (19 Nov)

Test 1 (set v1): 2 of 5 and 2 of 5. Test 2 (set v2): 4 of 5 and 3 of 5. Test 3 (set v3, four frames): 4 of 5 and 3 of 5. Pass is 4 of 5 for both, so the gate is not passed. Records: `cold_test_ring_v1/`, `_v2/`, `_v3/result.md`.

- **Test 3 fixed:** the plan (its own shot, 5.1b) and the Referee's neutrality (centred, at the far ropes).
- **Test 3 broke:** the punch. Lowered to clear the Referee, it read as an offered glove to both viewers.
- **Never read in three tests:** the Client arriving. Leave it to 4.1.

Test 4 (set v4, five frames): 3 of 5 and 2 of 5. The plan with its title, 10 GARAGES, is named by both. The punch is now read as aimed at the Referee, who stands between them; the waistcoat did not help. The robe's direction cannot be told from stills. Record: `cold_test_ring_v4/result.md`. Stills testing of beat 05 stops here; the next test is a moving rough.

- **Fixed:** the robe gag reads (the sleeve drawn stretched from his glove to Pam's hands); the robot's face is clear of Sofía's card.
- **Failed twice, the same way:** nobody sees him look at the plan. Eyes turned up read as weariness in this style. The plan needs a shot of its own or a reach.
- **Open:** the Referee behind the robot reads as the robot's man to one viewer in two; the stop marks at the glove read as a hit on nothing; the ropes across him do not read as arriving.

Test 5 (the moving rough `on3_beat05_rough_v1.mp4`, `src/ring_rough_on3.py`): 3 of 5 and 4 of 5, one short of a pass. The robe gag reads for both viewers for the first time; the plan reads; the swing is too soft for one viewer; the Referee behind the robot is still taken for its handler by some. Record: `cold_test_beat05_rough_v1/result.md`.

Test 6 (the whole beat, `on3_beat05_rough_v2.mp4`, 14.1 s): about 3 of 5 for both. The approval mechanism (5.3 to 5.5) is read in full by both, at phone size too. The robe's snag and the gap at the stopped glove were lost again; the watch gag in 5.6 is not read. Record: `cold_test_beat05_rough_v2/result.md`.

## Staging rules learned on this set

- A look is not an action here: what matters gets its own shot or a hand on it.
- A costume change inside a scene must be seen starting: show the robe on before it comes off.
- Marks in the air at a stopped glove read as an impact.
- A punch is thrown at shoulder height or it is not a punch.
- A stopped punch needs empty space behind the gap. A person standing there becomes the target.
- A change of clothes cannot be judged from stills.
- Fixing one reading can break another: retest the whole run of frames, not the one changed.

## Not done

5.6 (from above), 7.3 (low) and Don's walk out are not staged. The gate is open until the plan's thread reads.
