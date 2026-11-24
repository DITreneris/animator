# Pick a Side: best practices and the production plan, v1

UptimeZ Inc. · episode 14 · *Civil War* 2 of 5 · 23 Nov · for Tomas's decision. Nothing is built past the floor plan. Starts from concept v3.2 and [`ps_plan_v2.png`](ps_plan_v2.png), and follows [`series/production-process.md`](../series/production-process.md) (stages 0–12, five stops, version budgets) and `docs/lessons.md` (148 lessons).

## Status (updated 24 Nov, after the board's third and fourth cold tests)

| Stage | State |
|---|---|
| 0 Before starting | Concept v3.2 approved; branch `uptimez-pick-a-side`; STORYLINE v3.4 written; release-order condition (12's fix plan before animation) **still open** |
| 1 Script | Done: v8, generated from the scene file (38 shots, 68.8 s; the plan said ≤ 14 lines, the board has 19 takes) |
| 2 Voices | Done: `ps_voices_v2.mp4`, `ps_timing_v3.json` |
| 3 Look and set | Done, opt-in: tape, blinds, DON · CEO plate, guard cues, phones, CV; earlier episodes rebuild md5-identical |
| 4 Scene file and layouts | Done: `ps_scenes.py` is the one source; layouts v3 approved; **all the series' checks wired and each proved on a planted fault** (`ps_checks.py`; 38 shots, 0 faults) |
| 5 Board | Board v3 done. Cold tests: round 1–2 (fixes), **round 3 passed** (3 viewers, 4 of 5 beats each, loop read), round 4 (the door pair): wants and light 3 of 3. Left: the robot's grip at 270 px half-reads (kept); the phone in 6.1 not seen, ownership carried by 5.7's mug; the Mom, Father and Client names not read by mute viewers. **Outside review round 1 of 2 not yet asked** |
| 6 Motion tests | A–C approved (v3); D tape rip, E selfie, F, G Pam's reach done (G's thread moved to 5.7 by the three-fix rule) |
| 7–12 | Not started: animation, rough cut, polish, reviews, master, close |

Not in the plan above and added during the work: the checks module, the bubble adapter (`bc_sb.bubble`) with key frames per spoken line (`SPLIT_V4`, `KEYS_V4`), and the cold-viewer staging pair. Lessons 213–220 in `docs/lessons.md`.

## 1. Our best practices, analysed

### What the record says

| Practice | Evidence it works | Evidence it was missed or cost us |
|---|---|---|
| **One scene file generates everything** (stage 4) | The Offer's script v6, layouts, board, animatic and film all came from `of_scenes.py`; no hand-written drift inside the film | The *generated* script was not regenerated after rough cut v4: script v6 still says 60.4 s / 13 lines, the cut is 63.5 s / 15 lines. **Regenerate the script at every film version** |
| **Checks that fail the build** (`uz_check`, 19 validated cases) | Caught dead-zone props, signs, tails, limbs in The Offer (lessons 123–125) | Checks only work once validated on a known failure (123). None measures *laughs*: 14 cold viewers read The Offer and nobody noticed it had no joke until 0:08 (141) |
| **Five stops for Tomas** | Every stop sends the file, the gates and the open decisions | Tomas still caught what no gate measures: the missing 0:01 joke, stand-in poses (129, 145), a "gnome" robot (137) |
| **Version budgets** (layouts 3, motion tests 3, film 5) | First Search's 35 film versions are why they exist | The Offer overran: scene 2 v12, scene 4 v10, rough cut v8. Most overruns were **motion and staging found in the film** (131, 132, 142, 144, 145) that a motion test would have found earlier |
| **Cold viewers** at board, motion tests and rough cut, with direct questions (106) | Their shared misreads are cheap fixes (84) | They measure reading, not comedy (141); some misreads don't matter, so stop after two rounds if the meaning lands (139) |
| **Lay out every scene first** (97, preferences) | One Star's wrong map and the hidden robot were found before animation | Layouts with stand-in poses passed and survived to the film (129, 145) |
| **Outside reviews: two rounds, triaged** (G6) | Episode 14's concept rose from "Consider" to 8–9/10 on story in three rounds | Episode 14 has already had **four** outside reviews at concept stage. **The concept is closed; reviews come back only at the board and the rough cut** |

### The five rules this episode adds or enforces

1. **The 0:01 joke is proved first, in motion, before anything else is animated** (141). The blinds tug of war is motion test 1.
2. **Every beat that is motion gets a motion test before the board is approved** (131). Episode 14 is mostly physical: the blinds, the tape through the group, the throne spin, the robot ×3, the selfie and DING, the foot over the line. Six tests, a budget of 3 versions each.
3. **The photo is rendered from the scene itself.** The #TeamDon picture is the real wide frame of beat 8, rendered by the same code; the Client's zoom is a crop of that render. The heel, the tape and the silhouette then match **by construction**, not by care (the audit's P0).
4. **Cause and effect in one frame** (132): heel and tape; DING glow, silhouette and Don's smile; the Client's finger and Father's nod; Don's lifted foot and his own office door.
5. **Hold every story beat 0.5–0.6 s** (136): the heel, COO?, Pam's hand across the line, Don's foot hovering.

### Lessons that apply shot by shot

| Lesson | Where in episode 14 |
|---|---|
| 100 the change happens on screen | The tape is torn off the roll on screen; COO? is **written** in gold on screen; the throne **spins** |
| 101 a glance is not a turn | Sofía's "flat glance" at Don (beat 7) and Pam's choice (beat 9) go to hands and props: Sofía folds her arms; Pam's mouth opens and her cup comes up to cover it |
| 108 check the script against the set | Done: floor plan v2 on the front desk v4 |
| 111, 80 text at 270 px, fitted by measuring | DON on the tape, PUBLIC POST?, #TeamDon, COO?, INVITATION · FATHER, PAID BY DAD |
| 118 one text at a time on a screen | PUBLIC POST? slides up, then #TeamDon |
| 125, 126 protect story props; the board under the app | Declare: the tape roll, both cords, the robot's screen, the photo, Pam's phone, the CV, the heel, the bodyguard's phone |
| 127 a pose needs its object | The roll in Don's hand, the cords, the cup, the CV, the step stool for Pam |
| 135 gender from the drawing | Father keeps episode 13's stubble shadow in the booth |
| 137, 138 sizes against the set's canon, measured | The office home table: robot 0.66 (via `SC`), Don 0.60, Sofía 0.47, Pam 0.50, Mom 0.50; the Don rule; measure the drawn figure after any change |
| 143 a loop of actions checks the set | Loop check masks people; the declared set differences are the tape and the spun throne |
| 147 one hand | `kit.HAND` on, as in episode 13 |
| 148 a change of place needs its own shot | The booth opens on its red neon, THE HOUSE ALWAYS COLLECTS (from 12), for 0.5 s |
| 105, 83 room tone and the recognizer | Re-run Whisper after every mix change |
| 109 the drawing map | Assert every changed shot points at its new function |
| 119 trimming has a floor | Trim, then ask the cold viewers what felt rushed |
| 122 delete old frames | Keep only the current version's folder |

## 2. Before starting (stage 0)

| # | Task | Why |
|---|---|---|
| 0.1 | **Tomas approves concept v3.2** (the plan stays on hold until then) | Stop 0: the concept is closed |
| 0.2 | Write the approved series changes: **STORYLINE v3.4** (power = the throne, camps = the tape, 15–17 physical), **CLAUDE.md** (the 0:01 joke is physical), and **PAID BY DAD in episode 13**'s office shots (rough cut v9) | Episode 14 opens on the tag; 13 must plant it |
| 0.3 | **Branch:** `uptimez-pick-a-side`, from `uptimez-civil-war-arc` (episode 13 isn't on main yet), and say so | Process stage 0 |
| 0.4 | Read episode 13 **as built** (rough cut v8 frames), not its script | The throne, the robot at 0.66, the hand, the doors |
| 0.5 | **Release order check:** 11 → 12 → 13 must come out before 14; animation of 14 doesn't start until 12's fix plan is done | Three unfinished episodes already |

## 3. The plan, stage by stage

| Stage | What gets made | Pass (gates and checks) | Stop | Budget |
|---|---|---|---|---|
| **1 Script** | `pick-a-side-script-v1.md` from concept v3.2: every shot with size, setup (S1–S6 + inserts), action → reaction, line, sound; the protect list; the **0:01 joke named with its frame**; the cold viewers' direct questions (§4); the spoken lines as .md | G0 (incl. the 0:01 joke), G1; a line budget of ≤ 14; every verbal joke has an action; checked against the floor plan and the canon locks. **No outside review at this stage** (the concept had four) | **1** | 4 versions |
| **2 Voices** | All existing voices: Don `am_onyx`, Pam `bf_emma`, Mom voice F aged, the robot's series voice B. No auditions. `ps_timing_v1.json` | Whisper 3/3 on every dry take; the real length within 60–90 s (target 60–64 s) | **2** | — |
| **3 Look and set** | Opt-in props on the front desk v4 (front desk **v6** in the set doc): the **tape** (floor perspective, a roll, tear on screen, DON and an arrow), the **blinds** on the door glass (up, down, torn; two cords), the **PAID BY DAD** tag (13's drawing), the robot's **selfie arm**, its **☀** and **PUBLIC POST?** screens, the **CV with COO?** (gold, written stroke by stroke), Pam's **phone** face up (dark, lit), Sofía's **heel close-up**, Pam's **step stool**. Reused: the booth (12), Father with stubble (13), bodyguards, the Client's look from 9 | Episodes 9–13 rebuild **md5-identical**; every sign reads at 270 px | — | — |
| **4 Scene file and layouts** | `src/ps_scenes.py` (modelled on `of_scenes.py`): every shot, its camera, cast, scales, props declared with `protect()`, signs, action, reaction, effects. Generated: script v(n), a layout sheet per scene, the top-down shot plan, **the blocking sheet for beat 8** (selfie, the photo as a real render, the DING) and **beat 11** (foot over the line + CV at the door) | G2; `uz_check` on every layout frame (scale, signs, tails, limbs, text, dead zones); the Don rule; **no stand-in poses** (each pose has its object); **the photo rendered from the beat's own frame** | **3** | 3 versions |
| **5 Board** | One key frame per shot at 540, generated, looked at under the app overlay | G3; **G4** with two cold viewers + the direct questions + the loop question. Then **one outside review round** (G6, 1 of 2) | — | — |
| **6 Motion tests** | Six, at film rate, 540: **(1) the blinds tug of war** (the 0:01 joke, first), (2) the tape through the group, (3) the throne spin, (4) the robot ×3 with the bump, (5) the selfie, FLASH and DING, (6) Don's foot over the line | G4 on 8 fps strips with two cold viewers each; test 1 must be read as a joke ("they fight over the blinds") with no sound and no text | — | 3 versions each; a beat that fails three fixes is cut (52) |
| **7 Animation** | Scenes rendered native 1080 (2×), 15 drawings/s acting, 30 fps camera; `ps_film.py` | `uz_check` on every frame incl. the drawing map; each change seen in a before/after strip at full size | — | — |
| **8 Rough cut** | `ps_cut.py`: voices, effects (tape screech, blind clatter, flash, DING, the roll), room tone, the series' sparse vibes cut by the story's silences (107) | **G5** in full; **G4** with two cold viewers (4 fps sheet + 8 fps strips + direct questions + "what felt rushed or slow") | **4** | — |
| **9 Polish** | Numbered fix lists | Every fix seen in the render; every instance of a fixed drawing checked (56) | — | 5 film versions |
| **10 Reviews** | Triage tables | G6: the second and last outside round, on the rough cut | — | 2 rounds total |
| **11 Master and cover** | 1080 master (delivered, not committed), 540 copy, the cover (the #TeamDon photo is the natural cover) | G5 on the final AAC; a clean-checkout rebuild; the cover read at 120 px | **5** | — |
| **12 Close** | `pick-a-side-film-vN.md` as built; lessons; README, INDEX, STORYLINE rows from the built film; old frames deleted; commit, push and a PR when Tomas asks | — | — | — |

## 4. Direct questions for the cold viewers (fixed now)

1. What are the two people at the window fighting over, and why does the robot pull the blinds up?
2. What does the yellow line on the floor mean, and whose side is the boss's own office door on?
3. Who in the photo isn't really on the boss's side? How can you tell?
4. Who approved putting the photo online?
5. Who is behind the glass door, and what happened to his phone?
6. Who decided to make Sofía an offer, and what made them decide?
7. What is written on the paper Sofía gets?
8. Where is Sofía standing at the end, and does the boss know?

Pass: both viewers read at least 4 of 5 beats and answer every question; two viewers making the same mistake is a staging fault.

## 5. Risks and their fallbacks (set before the first round, lesson 95)

| Risk | Fallback |
|---|---|
| The blinds tug of war doesn't read as a joke on mute after three motion-test versions | The tape screech through the group moves to 0:00 (the second-strongest physical gag) |
| The tape doesn't read as a floor line in a vertical frame | A low S4 angle on the tape for its first appearance; the DON arrow bigger |
| The heel is too small in the photo | The photo insert pushes in on the heel before the cut to the booth; the Client's zoom repeats that push |
| Don's foot hovering reads as a stumble (side legs are hard, 89–90) | Frontal staging, the knee up and the foot over the tape, no side view |
| The selfie lens can't hold Don, the heel and the silhouette at once | The photo is the S1 wide as the robot sees it (a "screenshot" look), not a true selfie angle |
| Length over 66 s | First trims: beat 2 into beat 1; Mom's line said off her action |

## 6. Decisions for Tomas

1. Approve concept v3.2 (closes the concept stage).
2. Write the series changes now: STORYLINE v3.4, the CLAUDE.md rule, and PAID BY DAD in episode 13 (rough cut v9)?
3. Branch `uptimez-pick-a-side` from the Civil War branch?
4. Start episode 14's script now, but its animation only after episode 12's fix plan is done?
