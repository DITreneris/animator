# The Double Agent: the layouts plan, v1 (stage 4.3–4.5, up to Tomas's stop 3)

UptimeZ Inc. · episode 15 · 27 Nov. Done before this plan: 4.1 the lessons (`the-double-agent-lessons-v1.md`), 4.2 the scene file (`src/da_scenes.py`: 35 shots, five data checks passing, generated `the-double-agent-script-v5.md`, 68.5 s). This plan covers what is left of stage 4. Budget: **3 layout versions**; the stop rule holds (two full check runs without the faults going down → stop and report).

## 0. What Tomas gets at stop 3

| # | Deliverable | File |
|---|---|---|
| 1 | Three layout sheets, one per act: every shot at 270 px as its key frame, the apps' zones in red, the line, the checks' verdict under each | `da_layout_act{1,2,3}_v1.png` (+ a feed-size copy) |
| 2 | The top-down shot plan: the set from above, the 9 camera setups, each shot's camera as a numbered wedge, the cast's marks per act | `da_shot_plan_v1.png` |
| 3 | Blocking sheets for the two hardest beats: 3.4 (the wall and the feint) and 7.4 (the clip tug) | `da_blocking_34_v1.png`, `da_blocking_74_v1.png` |
| 4 | The blocking test of 7.4: real camera frames, two cold viewers, their answers in a table | `the-double-agent-blocking-test-v1.md` |
| 5 | The check report: every frame, every check, PASS/FAIL, the known exceptions with their reasons | printed by `da_layouts.py`, pasted into the plan's status table |

## 1. How it is built (one source, reuse first)

- **New `src/da_layouts.py`** reads `da_scenes.STAGE` and `TEXT` (nothing about a shot is typed twice). One map, shot → draw function; printed and asserted on every build (lesson 109).
- **Per setup, the drawing it reuses:**

| Setup | Shots | Drawn by | Camera |
|---|---|---|---|
| S1 master (A+B) | 1.3, 1.4, 4.2, 5.3, 7.4 | `da_set.room` (front desk v4 + tape + throne + the office glass with `office_inside`) + the rigs at their marks | framed on the shot's story faces (`cs_frame.face_cam`, as `ps_scenes`), `da_set._floor_on` for low framings |
| S3 B front | 1.2, 1.5, 2.3, 2.4, 3.1, 5.2, 6.2, 6.4, 6.5, 6.7, 6.8 | the same world, closer | faces framed; MC and C sizes by the series' size rule (lesson 69) |
| S4 B low | 7.1 | the same world, low | fixed: under Don, the tape at the bottom |
| S5 C close | 4.3 | the same world | Mom at her desk |
| S6 counter's end | 3.2, 4.1, 6.1 | the same world | B+C; the glass in the back |
| S7 the episode's master | 2.1, 3.3, 3.4, 5.4, 7.2 | `da_set.establish`'s world | from (659, 700, 0.90), framed per shot |
| S8 inside the office | 2.2, 3.5, 7.3 | `da_s8`'s layers (v9 flags), per-shot cast states | frame units; MC as a crop of the S8 frame |
| S8r the floor from the office | 1.1 | `da_s8r_frame0_v4.png` (the file) | — |
| S9 a view through the glass | 5.1, 6.6 | `da_set.office_inside`, cropped to the glass, the tint kept | close on the object / the face |
| Insert | 6.3 | `da_props.minutes` | frame units |
| Moves | 8.1 pull, 9.1 push | `da_push91.py` | key frames at start, the glass passing, the end (lesson 217) |

- **The other space in the glass, per shot (the two spaces, lessons 249–253):** `da_set.office_inside` gets an opt-in `STATE` (default = establish v3, md5 unchanged): who is in the office and where, the mug on the table or not, the blueprint rolled / handed / held, Pam inside or not. Each floor shot that shows the glass sets it from `STAGE[...]["other"]`. All are still states.
- **The robot's pile** drawn from `STAGE[...]["robot"]` (count, working/frozen): the box, the clips on the floor (`sofia_da.paperclip`, CLIPS_V2), the pincer up when frozen.
- **Hands:** `hands_lr.setup()` and `hands_v4` for every floor and office frame; the library v4 poses for the new jobs (the cup and saucer, the minutes, the blueprint in two hands, the mic, the strip); `da_hand_gate` on every frame. Key poses only: motion is stage 6.

## 2. The marks (world units; F = 800, the tape at x 560 at F, splaying toward the camera)

Measured from `da_establish_v3` and `ps_scenes.P`, written into `da_scenes.py` as `MARKS` before any layout is drawn, then held by `set_gate` (`PROPS` + per-shot `SET_MOVES` with the reason):

| Mark | Where | Who, when |
|---|---|---|
| `don_line` | his side, toes at the tape (x ≈ tape − 56, F + 150) | Don 2.1, 3.4, 5.3's stop, 7.2 |
| `don_counter` | his side, facing the counter end (≈ 520, F + 60) | Don 2.4, 3.1, 4.1, 6.2–6.8 |
| `don_street` | zone A, at the street door's glass | Don 4.2 |
| `throne` | `ps_set.THRONE` (452, F + 8), the tape behind it | 1.1–1.5, 7.4; rolled through the gap in 7.4 (SET_MOVES) |
| `pam_counter` | in front of the counter's left end (650, F + 34) | Pam 2.4, 3.2, 6.x |
| `mom_desk` | behind the counter at her desk (824, F − 70) | Mom 3.3 (stands), 4.3, 6.1 |
| `mom_wall` | the counter's left end, Father's side, between Don and the glass (≈ 600, F + 40) | Mom 3.4, 5.4, 7.2 |
| `office_door` | x 896, behind Mom's desk | Pam's crossings |
| `robot_pile` | the floor between the throne and Mom's desk (≈ 560–700, F + 60) | the robot 1.4–7.4 |
| inside: `father_chair`, `client_seat`, `sofia_seat`, `pam_inside` | `da_s8`'s meeting marks | S8 and the glass |

## 3. Shot by shot (key frame, what must read at 270 px, the risk)

| Shot | Setup · size | Key frame | Must read at 270 | Risk / check |
|---|---|---|---|---|
| 1.1 | S8r · M | frame 0 (the file) | the tug, the throne, the roll | done (locked) |
| 1.2 | S3 · M | the roll swinging into his shin | the roll on his foot, the whack | the 0:01 joke is 1.1; this is its payoff: hold |
| 1.3 | S1 · W | the shoes and hem stepping over; the tag hung | Father's shoes; the robot letting go | **REVIEW · TOMORROW unreadable in S1 · W** (2–4 px): move the hang to an MC or let it read as "a tag" only — Tomas |
| 1.4 | S1 · W | the box catching the armrest, clips spilling | the spill | the pile's first frame (30 clips) |
| 1.5 | S3 · M | roll off the sole, dropped by the throne | the roll's place (the loop needs it behind his back foot later) | set_gate: the roll's mark |
| 2.1 | S7 · W | Don toes at the line; inside, Father sitting | Father in Don's chair through the glass | the inside at 270: Father must be a figure, not a smudge |
| 2.2 | S8 · M | the heel on the face-down photo | DON · CEO before it turns; the heel on it | the photo's sign whole; outside: Don at the line, the robot frozen |
| 2.3 | S3 · MC | the vest snap, chin up | his face | — |
| 2.4 | S3 · M two-shot | the mug with the bow held out; the blue mug shattering | the bow, the shards (`shards_v2`) | two things move (the gift, the fall): the gift first, the fall after (lesson 22) |
| 3.1 | S3 · MC | one hand up, not turning | — | — |
| 3.2 | S6 · M | the pour into her mug and the cup | the mustard mug, the cup and saucer | the glass behind: Father and the Client waiting |
| 3.3 | S7 · W | the oily hand taking her mug at the door | the mug leaving her hand | the robot frozen on the Client's line |
| 3.4 | S7 · M | the feint (Don leaning one way, Mom not moving) | the shoulder pads, the knitting hand | **blocking sheet**; the glass: the mug on the table, Pam's hand on it, still |
| 3.5 | S8 · MC | Pam wiping the oily print | the print, the wipe | outside through the glass: Mom's back, Don's head |
| 4.1 | S6 · M | Pam handing over the cup and saucer across the tape | the hand-over | Pam caught mid-step out of the door; the glass: the deal seated |
| 4.2 | S1 · W | Don preening at the street door; Pam crossing back behind him | his back to the office, her going in | two people move: Don still at the door while she crosses |
| 4.3 | S5 · M | Pam passing Mom, Mom knitting | Mom not looking up | — |
| 5.1 | S9 · C | her mug on Father's table | the mustard mug, inside | the one silhouette (mug v2) |
| 5.2 | S3 · MC | the pinky out, the saucer held out | the pinky, the slop (`cup_and_saucer_v2`) | the library's PINCH (round 2) |
| 5.3 | S1 · W | the dead stop at his line, body going on | the feet stopped at the tape | the robot frozen |
| 5.4 | S7 · M | Mom planted between him and the glass | her arms folded, the robot frozen with a clip | — |
| 6.1 | S6 · M | Pam out of the door with the printout | the page | entrance mid-step |
| 6.2 | S3 · M two-shot | the page held out ("I took notes." starts) | the page, her face | the line runs on into 6.3 |
| 6.3 | I | AGENDA: WITHOUT HIM | the words whole | the insert's owner: her fingers at the edge (lesson 134) |
| 6.4 | S3 · MC | suspicion → delight | his face | — |
| 6.5 | C | her mouth opening | — | — |
| 6.6 | S9 · C | the Client looking at her, the roll in his hands | his look, the blue roll | — |
| 6.7 | C | her mouth closing, held 0.6 s | the change | one visible change on the held beat |
| 6.8 | S3 · MC | the mic at his mouth; Pam leaning in | the mic, the lean | the speech bubble's tail off the mic |
| 7.1 | S4 · C | the strip peeling up | the strip (`strip_v2`) | — |
| 7.2 | S7 · W | Pam under the strip; the robot frozen, one clip left | the strip as a barrier, her ducking | the glass: the Client seated with the roll, still |
| 7.3 | S8 · MC two-shot | the blueprint between them, Father not turning | MY GARAGES, both her hands | two bubbles in 3.4 s, each ≥ 1.5 s, neither on the plan or the hands |
| 7.4 | S1 · W | the dive: Don's grab on the armrest, the robot's pincer over the clip | "he wants the chair, it wants the clip" | **blocking sheet + the blocking test**; the glass: Pam holding MY GARAGES, still |
| 8.1 | move | three key frames: the tug, the glass passing, the deal held | the reveal | done (`da_push91.py pull`) |
| 9.1 | move | three key frames | the seam | done |

## 4. The checks on every frame (4.4); the build fails on a miss not listed with its reason

| Check | Tool | New? |
|---|---|---|
| Faces and story props out of the dead zones (y > 720; x > 470 at y 380–860), measured where the rigs drew them | `uz_check.check_scale` + `of_set.protect()` | reuse |
| Signs whole or out of frame; a sign partly covered (DON → ON) | `uz_check.check_signs`, `ps_scenes.covered` (copied, not imported) | reuse |
| The set: props on their marks, floor lines, the same people across a cut | `set_gate` + `SET_MOVES` / `SET_AIR` per shot | reuse |
| Bubbles: 12 lines, `speech.draw`, tails 10–20 px, the box off signs, props and hands | `speech_gate` | reuse |
| Hands: jobs, left/right, the thumb side, props seen | `da_hand_gate` + `hands_lr.check()` | reuse (ep15) |
| **The other space reads at 270 px**: the state in the glass covers enough pixels at feed size (the figure or the prop, not a smudge) | new: measured on the frame drawn with and without the inside | new: planted fault first |
| **The mirror rule on the drawn frame**: Don's x against the tape's x per setup | new: from the rig's head, not from `STAGE` | new: planted fault first |
| **The robot's pile reads and doesn't steal the eye** (script's open question 2): its pixels at 270 against the story faces' | new | new: planted fault first |
| The loop | `da_push91` (9.1's end = frame 0's file) | done |

## 5. The blocking sheets (4.3) and the blocking test (4.5)

- **3.4 the wall and the feint:** a top-down of the counter's left end (Don, Mom, the glass behind, the robot frozen) and three key frames: left, right, the feint + the hold on Mom (0.5 s) before her line.
- **7.4 the clip tug:** a top-down of the throne, the gap, the clip under the caster, the roll; key frames: the robot rolling off the clip toward Father's side, Don's dive and grab, the tug (each pulling for something else).
- **The test:** 7.4 as 4–6 real camera frames (not the plan) to two fresh viewers, the open prompt plus the direct question "what does each of them want?". Pass: 2 of 2 read "the robot wants the clip, the man wants the chair". A miss goes into the staging, then one retest; two misses go to Tomas (lesson 52: three means cut).

## 6. Order of work

1. `MARKS` into `da_scenes.py`; `set_gate` exceptions per shot. (short)
2. `da_set.office_inside(STATE)` opt-in; establish v3's md5 checked unchanged.
3. `da_layouts.py`: the map, the per-setup renderers, the sheet; **Act I first** (9 shots) → sent to Tomas as soon as it is clean, so a wrong direction costs one act, not three.
4. The three new checks, each with its planted fault.
5. Act II (12 shots), Act III (14 shots, 8.1 and 9.1 as key frames).
6. The shot plan, the two blocking sheets.
7. The 7.4 blocking test.
8. Stop 3: the package in §0, the status table in plan v2.

## 7. For Tomas now (can wait until Act I's sheet)

- **1.3's REVIEW · TOMORROW tag** cannot be read in S1 · W: (a) the hang gets its own MC, (b) it reads only as "a tag" here and its words come at the loop's insert, (c) drop the words from 1.3.
- **Length 68.5 s** with the voices: keep, or trim per script v4's open item (4.3 into 4.2, 6.2 into 6.1).

## 8. Decided after Act I's first sheet (Tomas 27 Nov, /grill-me: "too many badges and chairs")

| What | Decision | Where (all opt-in; earlier frames md5-identical) |
|---|---|---|
| The throne's back | bare: no OWNER: INVESTOR card (14's), no price tag's blank back; REVIEW · TOMORROW stays | `da_set.EP15_SET` |
| The floor set | no taped MY GARAGES plan on the counter (the blueprint is rolled until 7.3), no shredder | `da_set.EP15_SET` |
| Don's office chair | a plain low black office chair (variant L): one throne only | `da_s8.CHAIR_VARIANT = "L"`; the glass view low too |
| Name badges | off for the people; the robot's HR stays (its role here) | `da_set.no_badges()`, `NAME_BADGES` |
| Consequences | **S8 v10** (v9 + chair L + no badges), **S8r v5** (frame 0 without Don's badge; loop seam PASS, md5 bc18f8ef…), the push and the pull-back rebuilt on them (`da_push91_strip_v3.png`, `da_pull81_strip_v2.png`); S8 v7/v8/v9 and S8r v4 unchanged | `python3 da_s8.py frame10`, `python3 da_s8r.py v5` |

