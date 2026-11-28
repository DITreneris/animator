# Approved.: best practices and the production plan, v1

UptimeZ Inc. · episode 16 · *Civil War* 4 of 5 · 28 Nov · working folder `the-review/`, branch `uptimez-the-review`.
It starts from concept v7.1 ([`the-review-concept-v7.1.md`](the-review-concept-v7.1.md)) and follows [`series/production-process.md`](../series/production-process.md) (stages 0–12, five stops, version budgets), [`CLAUDE.md`](../CLAUDE.md) (the gates), and the record of episodes 13–15. Nothing is built past the concept yet.

## Status

| Stage | State |
|---|---|
| 0 Before starting | Concept v7.1 closed. Branch `uptimez-the-review`. **STORYLINE v3.5 written** (only the sitting CEO can hand over the throne; row 16 *Approved.*; the Client's survival planted in 16) |
| 0.4 E15 as built | Done (28 Nov): the $49,999 tag hangs from the crown (not under the armrest); REVIEW is one two-sided tag on the throne's back; the Client is never on Don's floor line (h 1.03, w 1.69 of Don). In script v1 |
| 1 Script | **v3** (`the-review-script-v3.md`, 52 shots, 65.6 s, 11 lines; the dialogue punch-up, 28 Nov) with `the-review-hand-jobs-v1.md`. Stop 1 answered 28 Nov: one night (canon night grade), Sofía new outfit, panel voiced, 52 shots |
| 2 Voices | **Takes v1 done** (28 Nov): `src/rv_voices.py` (E15's method) with Kokoro and Whisper fetched from their GitHub releases. 11 lines, picks 1.2 B, 1.4 D, 2.5 A, 3.2 B, 3.3 B, 3.4 B (E15's take, reused), 4.2 B, 4.4 B, 5.1 B, 5.9 B, 5.10 A; Whisper heard 11 of 11 (2 of 3 windows or better). **Real length 74.3 s** (script 65.6; the bible allows 90). The robot's "Yes." was heard as "Yes, sir" 3 of 3 (its filter's tail): cut at 0.42 s (`TRIM`), now "Yes." 3 of 3, also with silence after it. Picks kept as the auto-pick (Tomas, "choose best"). `rv_timing_v1.json`; `rv_voices_v1.mp4` and the audition (not committed: rebuilt locally). **Stop 2 passed** (28 Nov) |
| 3 Look and set | **Night grade test still first** (decided 28 Nov): `src/rv_night.py` applies the canon night (bp_frame's palette) to the 9:16 front desk, opt-in, the throne with a warm rim only; cold checks, two fresh viewers a round: **v1** 0/2 sure of night ("no window, no dark sky, no lamp"); **v2** (+ street-light bands, vignette, stronger glows) 0/2, the bands read as rain or a glitch (removed); Tomas picked **night in the glass door**: **v3** (`rv_night_test_v3.png`: the shut door shows a navy sky, the moon, a lit window across the road, a streetlamp) **2/2 night**. Eye order throne → $49,999 tag in 6 of 6. Left: the room itself reads flat ("a dull afternoon" without the door), so every wide keeps the door in frame or a screen glow near a face; the moon made bigger (15). **Night with the cast, LOCKED at v5** (28 Nov, Tomas: "one stronger pass, then lock"): `rv_night_cast_N1/N2/N3_v5.png` (`src/rv_night_cast.py`, runs on a checkout with E15's modules until that branch is merged; md5 N1 f530ed31…, N2 77e5f887…, N3 d823bc73…). Six cold rounds: night reads with the door, the dark office glass or a screen in frame (N1 2/2, N3 2/2, N2 "probably" 2/2); HUMAN APPROVAL REQUIRED as the robot's face reads at 270 px; G3 clean. **Kept:** the light lands (monitor and machine pools on their sources, the cold patch from the door), the background falls off, contact shadows, the people darker away from the lights (shade 0.30). **Dropped:** the lit band and rim on the people (v4: "a ghost", "a hologram", "glassy" 2/2) and the big pools that ghosted the Client. The flat paper look of the people stays, as the series' style; motion (the screens' flicker) is checked at the motion tests. Rule for every shot: a night source in frame (the door, the dark office glass, or a screen near a face). **Lock moved to v6** (28 Nov, the third outside night review, Tomas "itraukiam, tvarkom"): the counter's front falls off away from Pam's monitor (to about 40 % at its far end) and the coffee machine is the warm source (a small warm pool at its front, its red lamp glowing): a hierarchy of sources, cold screens and one warm machine. `rv_night_cast_N1/N2/N3_v6.png` (md5 1192b831…, 53ff5b23…, 90cb5f75…). Not taken from that review, with reasons: the ambient −25 % (the canon palette), the cold rim on the people (failed 2/2 in v4), a dimmer throne gold (6 of 6 viewers read it first: the power prop). G6 is spent for the night look: the next outside review is at the board. Sofía's new outfit: **a CEO power suit** (black, sharp shoulders, a gold pin). E12's coffee machine (`dh_props.coffee_machine`) already has the gauge: it is the needle |
| 3 Props | **Props sheet v1** (`src/rv_props.py`, `rv_props_v1.png`): the grey steel folding chair (open, wobble, folded), the washer, REVIEW · TODAY/TOMORROW (E15's tag), the $80 invoice, the Client's name card, the report (held, unfurled), **one screen function** for the robot's face and the machine's panel, Sofía's CEO suit (E15's in black, a gold pin; shoulders not squared yet). All read at 270 px. Script **v4** retimed to the takes (74.3 s), the budget's last |
| 3b Key stills | **K2 v2 reads 2/2** (the robot in the throne, Don about to lose it, Father deciding); fixes: Don on HIS side of the tape (v1 stood him on Father's), the screen larger; APPROVER: CEO stays borderline at 270 (the 6.2 insert carries it). Father's reaching finger: to the pose sandbox. **K1 failed 2 rounds** (v1-v2: "abstract blocks", the arm "a trolley jack", empty floor): Tomas 28 Nov, redo **with the robot in frame at the same height** (its UPTIME face level with Don's lap, its arm down to the card). New poses (Don seated, Don on the floor, Sofía seated, the Client kneeling) go through a **pose sandbox** (Tomas 28 Nov), canon rigs untouched. v3 (robot at lap height) failed on the badge: its chest shows the HR badge it has at frame 0 but not at the end. **K1 v4** (Tomas "Go 1"): a medium on the whole throne with Don asleep (`src/rv_poses.py` v1, `don_seated`: don_ps's own rig clipped at the belt, new legs), the robot hidden behind the throne (only its screen's glow and its thin arm from behind the base), REVIEW · TOMORROW under the front-left caster. Cold round: Don asleep in a throne for sale 2/2; fixed after it: the card larger and moved left ("tiny", "the lever covers it"), away from the throne's red lever (read as part of the arm 2/2). Over the 3-version budget: at Tomas's lock. **Locked 28 Nov (Tomas): K1 v6, K2 v3.** K2 v3: no HR badge on the robot, Don's own head on the APPROVER: CEO screen, pushed in, Don and Father whole in frame, the floor arrow whole. K1: the front-on seated pose (v4-v5, then the report over the knees) read as "standing in front of the chair" four rounds running, so the premise changed (rule 5): Don asleep ACROSS the throne (`rv_poses.don_sprawl` "B": chin down, legs over the right armrest, the unread report on his belly, both hands `quiet`). Silhouette test §0.2, 3 variants: B "dozed" 2/2 (A "passed out", C "falling / dead"). K1 v6 cold: seated and asleep 2/2; joke told back unprompted ("bought a $49,999 throne to nap in; his only decision is TOMORROW"); the report also hides the ketchup stain (read as blood before). Legs thinned and drawn under the torso after it ("huge tube legs" 2/2), not re-tested. Confetti off in both (`rv_night_cast.NO_THRONE_CONFETTI`, opt-in; N1-N3 unchanged). Props sheet v2: the report one continuous strip with a second spill, the chair's one short leg, SALARY small over a big $0, the card's text centred. For the animatic: the robot arm ("a crane", "a lamp") reads once it moves the card; the red lever ("a joystick"). |
| 4–6 | Not started. Allowed in parallel with episode 15 |
| 7–12 | **Held until episode 15's master** (decided 28 Nov) |

## 1. Our best practices, analysed (episodes 13–15)

| Practice | Evidence it works | Evidence it was missed or cost us |
|---|---|---|
| **One scene file generates everything** (stage 4) | The Offer and Pick a Side: script, layouts, board and animatic from `of_scenes.py` / `ps_scenes.py` | The generated script drifted when it was not regenerated after a film version (E14 plan §1). **Regenerate at every version** |
| **Checks that fail the build, each proved on a planted fault** | `uz_check`, 19 cases; E14's `ps_checks.py`, 38 shots, 0 faults | People and props floating in the air in E15's Act II layouts were caught by Tomas, not a check. That gave the **grounding gate** (feet on the floor or behind the counter, props on a surface or in a reaching hand) |
| **Five stops for Tomas** | Each stop sends the file, the gates passed and the open decisions as multiple choice | — |
| **Version budgets** | They exist because of First Search's 35 versions | E15 had **12 rounds of hand fixes** before the sandbox hand library |
| **Hands: one job table, one style** | E15's hand library v3 (approved 27 Nov) in one-outline style, kept out of canon until the episode is done | Each hand fixed shot by shot never converged |
| **Key stills before the board** | E15's S8 final image and S8r (frame 0) were locked first and anchored everything else | — |
| **Cold viewers** at the board, motion tests and rough cut, with direct questions | Shared misreads are cheap fixes. In E15 a reading was accepted instead of fought (the paperclip → the robot comes for the throne) | They measure reading, not laughs (lesson 141) |
| **Simplify a shot that is too hard** | E15: fewer characters and details where both spaces were hard to draw | — |
| **Outside reviews: two rounds, triaged (G6)** | Each triage found two or three causes behind many points | **E16 has already had five reviews at concept stage** (E14 had four). The concept is now closed |
| **The freeze rule** | An approved film is not reopened for later rules (26 Nov) | — |

## 2. The rules this episode adds or enforces

1. **The concept is closed.** v7.1 and its "closed decisions" list are the brief. Outside reviews come back only at the **board** (stage 5) and the **rough cut** (stage 8), one round each.
2. **Two key stills first** (decided 28 Nov), before layouts:
   - **K1 the loop seam:** a close shot of Don, the throne, the card under the front caster and the robot's hand. Frame 0 and the last frame are drawn by the same code.
   - **K2 the silence:** the robot in the throne, the screen showing **APPROVER: CEO** with Don's face, Father's finger stopped, Don's hand hovering.
   Each still passes `uz_check`, the hands page and Tomas before the scene file is laid out.
3. **One drawing for both approvals.** The machine panel and the robot's screen are drawn by **one function** in the same type (HUMAN APPROVAL REQUIRED). Don's press (gesture 1) and his hover (gesture 2) are one hand job with two states. The loop check covers the callback: the two screens differ only where the script says.
4. **Hands: E15's grab list and method, six story jobs** (decided 28 Nov). Every hand is listed with its row before drawing, the hand gate checks each shot, and hand library v4 is reused; only `point` is new. The canon (`hands_ps`, `of_cast`) is untouched until the episode is done. See §5.
5. **Grounding gate on every layout and board frame:** feet on the floor line or behind the counter; props on a surface or in a reaching hand. This covers the report paper, the folding chair, the mug and the card.
6. **The 0:01 joke is proved in motion first** (lesson 141, E14 rule 1). Motion test M1 is the throne rolling back off the pulled card, Don sliding, the cup raised. It is also the caster physics check.
7. **Hold every story beat 0.5–0.6 s** (lesson 136): the washer, POSITION VACANT, the needle, the tick, "Good hands." with Don's hands, the $80 invoice, SALARY $0 → $49,999, APPROVER: CEO. **The 2 s silence is fixed**, and nothing is trimmed from it.
8. **One dominant text per shot** (lesson 118): no shot carries two of POSITION VACANT, NOTED., UPTIME 100%, SALARY $0, $49,999, $80 UNPAID, APPROVER: CEO. Each reads at 270 px.
9. **Cause and effect in one frame** (lesson 132): the tick and the Client's head turn; Father's smile and Don's eyes; Father's stopped finger and Don's face on the screen.

## 3. Before starting (stage 0)

| # | Task | State |
|---|---|---|
| 0.1 | Concept v7.1 closed (five reviews triaged; G6 used) | Done |
| 0.2 | **STORYLINE v3.5**: the throne handover rule, row 16 rewritten as *Approved.*, the Client's survival marked as planted | Done (28 Nov) |
| 0.3 | Branch `uptimez-the-review` | Done |
| 0.4 | Read **episode 15 as built** (its latest frames, not its script): the throne and its back, the REVIEW · TOMORROW card, the tape, Sofía's outfit, Pam's mustard mug, Father's look | To do |
| 0.5 | **Release order:** stages 1–6 run in parallel with episode 15; stage 7 waits for E15's master | Decided |

## 4. The plan, stage by stage

| Stage | What gets made | Pass | Stop | Budget |
|---|---|---|---|---|
| **1 Script** | `the-review-script-v1.md` from concept v7.1: every shot with size, setup (S1–S6 plus inserts), action → reaction, line, sound and hold; the protect list (§6); the 0:01 joke named with its frame; the cold viewers' direct questions (§7); **`the-review-hand-jobs-v1.md`: every hand with its row (§5)** | G0 (including the 0:01 joke), G1; **line budget 7** (the concept's); every spoken line has an action; checked against the front desk v4 and the canon locks; **no outside review** (the concept had five) | **1** | 4 versions |
| **2 Voices** | Existing voices: Don `am_onyx`, Pam (E15's audition pick), Father (his E12–15 voice), the robot (filtered, the source on screen), the machine panel (the robot's family, flat). The Client and Sofía are silent. `rv_timing_v1.json` | Whisper 3/3 on every dry take, checked with silence after each take; dry voices; the real length is known (target 64 s, at most 90 s) | **2** | — |
| **3 Look and set** | Opt-in props on the front desk v4 plus E14's tape: the **folding chair** (wobbling and fixed), the **washer**, the **coffee machine** panel and needle (creeps toward the counter edge in steps), the **steam jet**, the **report** (folded and accordion-unfurled), the **$80 invoice**, the Client's **name card**, the REVIEW · TODAY / TOMORROW card (E15's drawing), the **throne's front caster** and the **$49,999 tag under the armrest** (the back stays bare as in E15), the robot screens (one function, see rule 3), **APPROVER: CEO** with Don's face. **Sofía's outfit:** decided at this stage (the day after E15) | Episodes 13–15 rebuild **md5-identical**; every sign reads at 270 px | — | — |
| **3b Key stills** | **K1** the loop seam, **K2** the silence (rule 2) | `uz_check`, the grounding gate, the hands page, full-size crops of every hand; `/quality-assurance-agent` | Tomas picks (as E15's S8) | 3 versions each |
| **4 Scene file and layouts** | `src/rv_scenes.py`, the one source. Generated: the script, a layout sheet per scene, a top-down shot plan, a blocking sheet for the hardest beat (36–47 s: the report flood with Father reading) | G2 (action and reaction per beat, sizes, eyelines: Sofía → POSITION VACANT, Pam → the corner, Don → Father's smile); `uz_check`; grounding gate; `set_gate` (props on their marks, `SET_MOVES` for the creeping machine); the blocking test | **3** | 3 versions |
| **5 Board** | One key frame per shot at 540, generated | G3 (faces and protected props out of the dead zones; the board under the app overlay); **G4: two cold viewers** with the open prompt and the direct questions; then **outside review round 1** | — | — |
| **6 Motion tests** | **M1** the 0:01 throne roll (caster physics); **M2** the tick → head turn → drop → mug catch; **M3** the report following Don back; **M4** the press / hover / pull back (both states); **M5** the robot's slow, formal rise | G4: two cold viewers on 8 fps strips; `uz_check` | — | 3 versions each |
| **7 Animation** | Scene renders, native 1080 (at 2×), 15 drawings/s acting, 30 fps camera | `uz_check` on every frame including the drawing map; every change seen in a before/after strip | — | — |
| **8 Rough cut** | The full film: voices, effects (the tick, the hiss, the glug, the paper), room tone | G5 in full; G4 cold viewers (4 fps sheets plus 8 fps strips, the open prompt, the direct questions, "what felt rushed or slow"); then **outside review round 2** | **4** | — |
| **9 Polish** | Film versions | Each version is a numbered fix list, each fix seen in the render; three fixes that don't land on one beat cut the beat (lesson 52) | — | 5 versions |
| **11 Master and cover** | 1080 master, 540 preview (rebuilt locally, not committed), cover | G5 on the final AAC; a clean-checkout rebuild; cover read at 120 px | **5** | — |
| **12 Close** | `the-review-film-vN.md` (as built), lessons, README / INDEX / STORYLINE row 16 from the built film; the hand library to canon via CANON.md; a pull request | Pushed when Tomas asks | — | — |

Pin each approved stage with a tag: `uptimez-approved-vN`.

## 5. Hands: reuse E15's grab list and its method (decided 28 Nov)

E15 already built the method and most of the drawings, on branch `uptimez-double-agent`:
- `the-double-agent-hand-jobs-v1.md`: every hand in the script, its job and its canon row, written before drawing.
- `src/da_hand_gate.py`: each shot declares its rows, and the gate fails a hand that is not on its shot's list. Misreads are counted, and 3 is a fail.
- `src/hand_lib_v4.py`: the sandbox library, one closed outline per hand. Poses RELAXED, CUP_GRIP, SAUCER_SUPPORT, GRAB, CLUTCH, PINCH, PALM, FIST, all cold-tested.
- `src/hands_lr.py`: the canon's left/right.
- `src/da_hand_sheet.py`: the episode hand sheet, every job drawn with its prop.

E16 follows the same order and reuses those files. It writes no hands file of its own.

- **Stage 1:** the script comes with `the-review-hand-jobs-v1.md`, a table like E15's covering **every** hand (about 25, not only the story ones), each mapped to its row.
- **Stage 3:** `rv_hand_sheet_v1.png`, built the way `da_hand_sheet.py` builds E15's.
- **From stage 4:** each shot declares its rows to the hand gate.

### The six story jobs, mapped to what exists

| # | Job | Row / library pose | State | Rule it must keep (`docs/rules-hands-and-phones.md`) |
|---|---|---|---|---|
| H1 | Don, flat on his back, raises the cup straight up | `handle_grip` = lib **CUP_GRIP** (v3, 2/2) | **Reuse** | Catch the arm already up; never route the hand past the shoulder (Daddy's Home v8) |
| H2 | The Client fits a washer under the chair leg while his other hand lifts the leg | `pinch` = lib **PINCH** (v4, 2/2) + `clutch` = lib **CLUTCH** (2/2) | **Reuse** | One hand per wrist; the washer is drawn at the pinch the pose returns |
| H3 | The Client catches the mug without looking | **By the handle**: `handle_grip` = **CUP_GRIP** | **Reuse** | Lib GRAB read 0/2 on a mug's wide body ("a hammer"), so he catches it by the handle, never round the body |
| H4 | The robot hands over the $80 invoice; Father takes it | robot **gripper** (locked) → Father `pinch` (Father sheet v6, the tag pinch `redraw_at`) | **Reuse** | **Two hands near each other read as a handshake**: keep a clear gap and let the paper span it |
| H5 | Father's finger reaches toward the robot's screen and stops | `point` (canon; `point_t` if large in frame) | **New for the library** (there is no POINT pose): use the canon function first, add a library pose only if it misreads | **A finger that stops near a sign reads as holding it**: it stops clearly apart, measured at feed size |
| H6 | Don's press without looking, and later the hover, freeze and pull back | `point`, fingertip on the button | **New for the library** (same as H5): one job, two states | **A press is `point`** (a fingertip), not a palm slap, so the concept's "slaps" becomes a blind fingertip jab |

### Canon fault in v7.1, fixed at the script

- **"Don folds his arms"** at the climax and in the loop. E15 found that crossed forearms are a canon fault (in 5.4 Mom was changed to hands on hips). E16 uses:
  - **At the climax, standing:** fists on his hips (`fist` ×2, elbows out, the same pose Mom used in E15). It reads as defiance.
  - **In the loop, seated:** left hand on the armrest, right hanging (`clutch` / `quiet`). This is Don's pose in E15's locked S8r v4, so frame 0 matches an approved drawing.

### Cut from v7.1 into the script (no story weight, each a hand job)

The cup shaken twice; the spoon tilted to a diagonal (the spoon now stands upright on its own); the filter handoff to the Client; Don nudging the name card and Father straightening it. Don's pettiness moves to his face, and Father's straightening becomes a glance.

### The other hands (to list in full at stage 1), most of them reused

- Father unfolding the chair (`grab` ×2).
- Sofía unpinning and pinning the badge, then checking it (`pinch`).
- Pam holding the blueprint and turning a page (`board_two`, `pinch`).
- The robot pulling the card out (gripper).
- Father flipping the card (`pinch`, the tag pinch).
- Don folding the card and wedging it (`pinch`).
- Don putting the filter in (`grab`).
- Don setting the cup down (`handle_grip`).

**No new row is needed except a `point` pose in the library.** Any new gesture goes through rules §0.2: three silhouettes, two cold viewers, then a row.

## 6. Protect list (G1, draft for the script)

1. **The two HUMAN APPROVAL REQUIRED screens and Don's two gestures:** blind press, then hover and pull back.
2. **APPROVER: CEO with Don's face.** Father's finger stops.
3. **"Good hands." earned twice** (the washer, the mug), with **Don looking at his own hands.**
4. **The robot's arc:** the report refused → POSITION VACANT → the tear → NOTED. → "Yes." → the $80 invoice.
5. **The loop:** REVIEW · TOMORROW under the caster, the same close shot at both ends.

## 7. Cold viewers' direct questions (to be written into the script)

1. Why does Don make the coffee himself?
2. Whom does Father want, and why?
3. What does the robot show Father that nobody else could?
4. Why doesn't Father approve the robot himself?
5. What does Don do at the end, and why?

Pass: both viewers read at least 4 of 5 beats and answer every question.

## 8. /grill-me at every stop

Every stop sends the file, one line on what changed, the gates passed with evidence, and the open decisions as multiple choice (AskUserQuestion, recommended option first). Then it builds exactly what was picked. Known decisions waiting for their stage:

- Stage 1: the hold lengths against the 64 s target; whether the robot's "Yes." comes from out of frame (the corner) or on screen.
- Stage 2: the machine panel's voice (the robot's family, or none, as text only).
- Stage 3: Sofía's outfit; the throne's front caster and armrest tag drawings.
- Stage 3b: K1 and K2 framings (two options each).

## 9. Risks

| Risk | Guard |
|---|---|
| Hands again eat the schedule | E15's grab list, gate and library reused; only `point` is new; full-size crops; two attempts per row, a tie keeps the old drawing; misreads fail at 3 |
| The length grows past 64 s | The animatic decides; the bible allows 90 s; the 2 s silence is never trimmed |
| Too much text on mute | Rule 8, and the board's cold test asks what each screen said |
| The loop's state mismatches (the badge, the mug, the machine) | The close-shot seam (K1) and the loop check |
| More outside reviews at script stage | Rule 1: reviews only at the board and the rough cut |
| E15's animation slips | Stages 1–6 only; stage 7 waits |
