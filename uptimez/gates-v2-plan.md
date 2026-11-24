# Four new gates: hands, depth and volume, proportions, shot variety — plan v1 (23 Nov)

Tomas, 23 Nov: "we need new gates: a hands pass, a scene depth and volume pass, a proportions pass, a shot variety pass". The hands took two outside audits and three rounds in One Star alone, and episode 13 spent three more before that (lessons 147, 149, 172, 178, 179). Proportions failed in ep 12 ("the robot a gnome", lesson 137) and One Star ("too small", lesson 98). Flat, cast-portrait staging and same-size shot runs come back in review after review (lessons 18, 131, 191, 277, 491, 511, 519). Each was caught by a person, late. These gates catch them by measurement, early.

Every gate follows the house pattern (G5): **a tool that measures, a sheet a person looks at, a pass mark, and a planted fault that proves the check can fail.** A failed gate goes back one stage, not to the start.

## Where they sit

| Gate | Stage | Replaces / extends |
|---|---|---|
| **GV Shot variety** | the shot list (G2), before key poses; again on the rough cut | extends G2 |
| **GP Proportions** | the cast line-up, before the board; then every render | extends G3 "sizes consistent", generalises `of_scenes.don_rule` and `cs_frame.py` |
| **GD Depth and volume** | the layout sheet (G2b), before animation; then every render | extends G3 "a foreground layer" |
| **GH Hands** | key poses (the hand states written in the shot list); every render; a motion strip for every hand action | new |

Order in a new episode: GV → GP → GD → GH → G4 cold test → G5.

## GV Shot variety

**The shot list gets five columns:** size (ECU, CU, MCU, MS, WS, INS insert, OTS), angle (eye, low, high, top), move (static, push, pan, whip), length, screen direction (who faces where).

**Measured from the render, not typed:** each shot's size class comes from the biggest face radius the rig drew (`sb.HEADS`, as `cs_frame.py` reads it). The face radius bands are calibrated once on the series (CU r ≥ 120, MCU 95–120, MS 70–95, WS < 70 at 540; an insert has no face). If the measured class disagrees with the list, the list is wrong or the camera is.

**Pass:**
1. No more than **two cuts in a row of the same size and angle**.
2. **Every scene uses at least three size classes.**
3. **Every location has a wide shot** within its first 3 s on screen.
4. **Every story prop** (the protect list) gets an insert.
5. **Every beat** gets an action shot and a reaction close-up (G2, now measured).
6. **No jump cut:** two consecutive shots from the same camera whose framing differs by less than 20 % of its width fail. Cut further, or don't cut.
7. **Length:** no shot over 4 s without a camera move; mean shot length 1.2–3 s.
8. **Screen direction:** within a scene, each character keeps the side and facing they had in the previous shot unless a shot shows them cross. Measured from the look vectors and x positions the rig logs.

**Sheet:** the first frame of every shot in a row, labelled with size, angle and length, plus a timeline bar coloured by size class. A run of one colour is the fault you see at a glance.

**Planted fault:** duplicate one medium shot three times in the list; the gate must fail on rules 1 and 6.

## GP Proportions

**One table for the series:** `uptimez/src/cast_scale.json`, every character's canonical scale per set, height and width in units, and hand size (lessons 137, 149, 164). Props too: phone ≈ 0.9 of a hand's length, a lighter narrower than the fist (lesson 178), door height, desk height, the robot at 0.48 on the front-desk set.

**Pass:**
1. **Pairs:** in every drawing, every pair of characters on one floor line keeps the table's height ratio within ±3 %. This is `don_rule` generalised to everyone, with the planted Client at 0.52 kept.
2. **Across a cut:** the same character in two consecutive shots of the same size class keeps its face radius within ±8 %.
3. **Face for the shot size:** a medium shot's biggest face at r 78–80 near y 400 (`cs_frame.py`, lesson 98); a close-up at least 1.5× that.
4. **Hands:** hand width ÷ head radius inside the rig's band (heavy rigs 20 % smaller, light rigs 15 % bigger, lesson 149).
5. **Props:** each held prop's size ÷ its holder's hand length inside the table's band.
6. **No rescaling to fit a shot** (lesson 604): any character drawn at a scale that is not the table's × the camera's zoom fails.

**Sheet:** the line-up. Every character of the episode on one floor line at the table's scale, with their props, beside the previous episode's line-up. Then one frame per shot with each character's measured height ticked against the table.

**Planted fault:** the Client at 0.52 beside Don (fails rule 1); a phone at 1.5 × hand length (fails rule 5).

## GD Depth and volume

**Each draw call says which plane it is on:**
- **fg:** desk edges, a shoulder, a hand, a plant in front;
- **mid:** the characters;
- **bg:** the set.

A plane log per drawing (opt-in, like `kit.HAND`), and a render with each plane switched off to measure what it covers.

**Pass:**
1. **Three planes:** every shot has mid and bg; **a foreground layer in every two-shot and every medium shot of a conversation**, and in at least 40 % of all shots (lesson 519: a sofa back, a cake, a hand). Measured: switching fg off changes at least 2 % of the frame.
2. **No line-up:** a shot with three or more characters fails if all their feet sit within 6 px of one floor line and no body overlaps another. Stagger them in depth, the near one bigger (the staging rule: reactions face their target, not the camera).
3. **Contact:** every standing character and every set-down prop has a contact shadow (from the draw log).
4. **Parallax:** on a pan or push, fg moves at least 1.3× bg. A flat move over one picture reads as a slide, not a room.
5. **One light per set:** every shadow and shade offset points the same way within a set (lesson 50: "noir is light, not grey").
6. **Volume:** every character shows a shade side or rim, and no flat area of one colour covers more than 60 % of a body. This catches the "box" bodies and the flat walls reviewers call "placeholder" (lesson 191).

**Sheet:** each shot with its planes tinted (fg warm, bg cool) beside the plain frame, plus the feet line and overlap marks for shots with three or more people.

**Planted fault:** One Star's 4.4 with the fg layer removed (fails rule 1); three characters on one line, not touching (fails rule 2).

## GH Hands

The hand system is now one: `kit.HAND` and `hands_ps` (shapes fist, point, palm, thumb, salute, relax, quiet, grab, cup), with grips from ep 13 (`phone_grip`, `handle_grip`, `clutch`) and One Star's `grip_rect`. The robot keeps its grippers.

**The shot list gets a hands column:** each hand's state (quiet, fist, grip, point, palm, robot) and what it touches. Pam's STOP palm, the point at the pocket and the 7 held were each decided per shot today.

**Measured (a hand log per drawing, from the hook and the grip functions):**
1. **One system:** every hand drawn in the film comes through the hook or a grip. A legacy disc or oval hand at an arm's end fails. Measured: render with the hook off and on; every arm end must change, except the robot.
2. **Held means gripped:** every held prop (registered like `PH_DEV`) has a grip drawn on it in the same drawing, and no second hand of the rig under it.
3. **State matches the list:** the logged shape per hand equals the shot list's column.
4. **A point stops short:** the pointing fingertip ends 4–20 px from what it points at (lesson 172).
5. **No pop:** a hand never changes shape between two drawings without a drawing in between (closed → release → index out). Measured on the log.
6. **Every insert hand has its owner's sleeve** (lessons 58, 134).
7. **The read test:** two cold subagents, shown only the story hands (the P0 list) at 9:16 feed size, name each one: points, holds, grips, open, at rest. Pass is 2 of 2 for every story hand (the audits' 1-second test).

**Sheets:** every hand before and after, found by diffing hook-off and hook-on frames (today's method). A motion strip of every hand action, drawing by drawing. The hand log as a table.

**Planted fault:** a legacy disc hand in one shot (rule 1); a phone with no grip (rule 2); a finger touching its target (rule 4).

## How we build it

| Step | What | Time | Your check |
|---|---|---|---|
| 1 | Logs, opt-in in the shared modules: shot metadata (size, angle, move), plane per draw call, character scale, hand state. Earlier films rebuild byte for byte with the logs off | 3 h | none |
| 2 | `gates.py`: the four checks, each with its planted fault proven to fail, exit code ≠ 0 on any miss, and the four sheets | 3 h | none |
| 3 | Baselines: run all four on One Star v7 and Daddy's Home v7. Report as an OK/FAIL table per gate per shot | 1.5 h | **the four sheets** |
| 4 | Fixes, per gate, at most two rounds each; after two rounds a failing shot is restaged, not resized (lesson 132) | depends on step 3 | the fixed sheets, then a render |
| 5 | Into the rules: the gate table in `uptimez/CLAUDE.md`, the `animation-episode-gates` skill (an update you approve), lessons, and the shot list template with the new columns | 0.5 h | the text |

Total about 8 h before fixes. Fixes are sized after step 3, when we know how much fails.

## To decide

1. **Thresholds:** foreground in ≥ 40 % of shots; same-size runs ≤ 2; ±3 % pairs; ±8 % across a cut; shots ≤ 4 s. Keep these, or set your own?
2. **The cold hand read test (GH 7):** every episode, or only when hands changed?
3. **Baselines:** One Star and Daddy's Home both, or One Star first?
4. **Do the gates block a render** (as G5 does), or only report until they are calibrated on two episodes?
