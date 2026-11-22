# Office Noir 3: the boxing scene as it stands (animatic v15), for review

Nothing in the film is changed by this folder. Scene: 0:38.2 to 1:21.3, 43.1 s, 26 shots, four blocks.

| File | What it is |
|---|---|
| `1_timeline.png` | Shots by size, what happens, who speaks, the four blows, motion in the frame, cuts per second, loudness |
| `2_plan.png` | The ring from above (a scheme: the set is drawn from the front), home positions, camera set-ups and their shots |
| `3_continuity.png` | Who is where on screen in every shot; robe, plaster, the robot's face, the plan |
| `block_A..D_frames.png` | The animatic's frames, 3 per second, with shot number and time (yellow = first frame of a shot) |
| `mute_A..D.png`, `mute_blows_10fps.png` | What the cold viewers saw: the film without cards and bubbles, numbered 1 to 171 |

Made by `src/on3_ring_analysis.py` (the three schemes) from `on3_animatic_timing_v15.json` and the animatic's frames.

## Measured

- Blocks: A the opening 7.2 s; B round one 9.7 s; C the corner and the detective 13.8 s; D the last round 12.4 s.
- The two fighters act on each other for 7.3 s of 43.1 s (17 %). Four blows in the scene: his jab that stops in the air (0:47.7), the robot's punch (0:52.5), his flurry of three (1:10.5 to 1:11.2), the robot's last punch (1:20.8).
- Block C has no blow at all for 13.8 s.
- 47 cuts, one every 0.9 s on average; the densest stretch (3 a second) is 0:51 to 0:53, round the first punch.
- The approval run (badge, Mom, button, tick) takes 3.5 s the first time and 3.4 s the second.
- Every camera looks from the same side: the Client is always on the left, the robot on the right.

## Cold test 53 (two fresh viewers, mute, 171 frames at 4 a second and the blows at 10)

Intended beats, written before the test: (1) round one is called, his cutman cannot get the robe off over the gloves, the bell; (2) he swings first, the punch hangs, the robot needs approval, an old woman elsewhere presses a button, the robot floors him; (3) the corner: patched; a detective walks in, takes his folder with the card girl's photo, case closed; (4) the last round: he gets up and hits the robot, the referee parts them, he reaches for the plan over the ring; (5) approval again, the punch.

| Beat | Viewer 1 | Viewer 2 | Verdict |
|---|---|---|---|
| 1 the opening | card girl, the sheet, the bell read; the robe: "I took it for his robe coming off, but it does not" | "corner fiddling… suddenly robeless… a glitch" | partly: the robe gag is not read by either |
| 2 the approved punch | "He never loses to the robot itself; he loses to her button" | "she approves without looking, and he gets flattened" | read |
| 3 corner, detective | patched: read; detective: "He changes nothing… a link that I could not decode" | "I could not tell what case he was on or what he concluded" | partly: what happens is read, why is not; the woman in the photo is not known as the card girl's other self |
| 4 the last round | flurry and the reach read: "the gloves on the prize" is the peak | "This is the best moment" | read |
| 5 approval, the punch | read; "a full repeat… that we already know" | "a 3.5-second near-repeat" | read, and long |

4 of 5 read by both (pass), 1 and 3 partly.

Both viewers, in the same words or nearly:
- **It is not a fight:** "Barely. The only real exchange is 130–134, about a second" / "It mostly does not feel like a fight… the hits arriving as cutaways".
- **Slack:** the corner before the bell (twice the same picture), the count ("the same image six times"), the split screen ("six identical frames"), the detective ("about seven seconds with nothing at stake" / "about 9 seconds… changes nothing"), the wide after the flurry, the second approval run.
- **The robot is too small in the wide shots:** "reads as a toy rather than an opponent" / "does not look like a threat"; it matches him only in the close shots.
- **Sizes:** the detective "towers over" the Client in 6.3 and is his height in 6.4; the card girl is "about one and a half times everyone else"; the referee "huge" at the bell.
- **Continuity:** the cutman changes side of him (right in the opening, left in round one) and is gone in the last round; the referee "pops in between the fighters… with no entrance"; the robot is missing in the last wide shot (1:13) "although it was lying tilted there a moment before", and is never seen getting up before its last punch; the detective fades out "half-transparent"; the knockdown lands him at the left ropes, then he lies centred from above; the card girl enters and never leaves; the plan hangs out of reach in the wides and at head height behind the referee at the bell.
- **Misreads:** the stretched red sleeve ("a punch at her?"), the count's hand ("a cursor" / "someone reaching down to help"), the thing over the smiling robot (the oil can), the white arc as the detective steps over the rope, the black frame before the first punch.
- **Loop:** both expect the end to return to the first knockdown or the opening wide; neither can know it returns to the film's first frame (not in the sheets).

The test cannot tell: whether it is funny, the voices and narration (they explain the detective and "Case closed"), the mix.
