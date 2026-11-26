# The Double Agent: best practices and the production plan, v1

UptimeZ Inc. · episode 15 · *Civil War* 3 of 5 · 26 Nov · for Tomas's decision. Starts from concept v5 and the establishing frame v3, and follows [`series/production-process.md`](../series/production-process.md) (stages 0–12, five stops, version budgets), `CLAUDE.md`, `docs/rules-hands-and-phones.md` (canon copy: DITreneris/uptimez) and `docs/lessons.md` (245 lessons). Modelled on [`pick-a-side-plan-v1.md`](../pick-a-side/pick-a-side-plan-v1.md).

## Status

| Stage | State |
|---|---|
| 0 Start | Branch `uptimez-double-agent` (pushed, from main 4cdb790). Episode 14 is finished but its film work is on `uptimez-pick-a-side-gags`, not on main |
| Concept | v1 → v5. **Three outside reviews already** (6.0 → 7.4 → 8.1) plus one frame review. **G6 is spent at concept stage: the concept is closed.** The next outside review comes only at the board, then the rough cut |
| Set | The establishing frame v3 (`src/da_set.py`, the office glass on front desk v4 + 14's pieces); its cold test: the premise 3/3, Don read as a robot 0/3 (fixes F1–F5) |
| 1–12 | Not started |

## 1. What the last three episodes taught, applied here

| Lesson from | What happened | The rule for 15 |
|---|---|---|
| **14, story audit** | The film was animated before the board told the story: the chain broke at points 6–10 (the hand-over 0/3, the crossing 0/3), and scenes 5–6 were redone after animation. **The skipped whole-board cold test cost the most** | **The story chain test on the whole board is a hard gate before stage 7.** No skipping "because each change was tested alone" |
| **14, the CV → card** | HR? needed episode 12 to read; replaced late by an invitation card | **Every prop reads with no earlier episode** (the review's standalone 4/10). The mug, the minutes, the blueprint, the tag: each tested cold at 270 px |
| **14, the door** | I drew a new door instead of the one the series had solved (*The Onboarding*) | **Reuse what was approved first** (CLAUDE.md rule 2): name the file reused for every set piece and gesture |
| **13, v61** | The film budget is 5; The Offer reached v61, mostly hands, sleeves and endings found in the film | **Budgets are hard:** past the budget a version needs a written reason, or the work goes back a stage. **An approved film is frozen**: a rule written later applies from the next episode, not to it |
| **13, v54 (lesson 244)** | A last shot drawn from nothing and rendered before Tomas saw a still | **Section 0 under time pressure too:** the rules listed, a storyboard PNG, Tomas's word, then the render |
| **11, v16–v26 (lesson 245)** | The gates measured geometry, not reading: an ownerless sleeve, a finger over a word, all gates at 0 | Gates are necessary, not sufficient: **every changed frame looked at whole, at full size**, before it's sent |
| **11 → 14, the backlog** | Four episodes finished or nearly, none released; no audience data | **Release order decision (§6)** before 15's animation |

## 2. The rules this episode adds or enforces

1. **The 0:01 joke is proved first, in motion** (lesson 141): the roll on the shoe is motion test 1, before any other test.
2. **The glass is the engine:** every S7 shot is staged twice (what Don sees, what we see inside), and the inside action is timed against the floor action in the scene file, not added later.
3. **Hands are the biggest risk.** This episode has **nine hand jobs**, more than 14: the wrist grab (3.3), the mug wipe (3.5), the cup and saucer and the saucer sip (5.2), the minutes handed over (6.1–6.2), the mic pulled to the mouth (6.8), the tape peeled (7.1), the barrier held (7.2), the blueprint slid (7.3), the strip stuck on the palm (8.2). Each is **named from the job table** in `rules-hands-and-phones.md` before drawing; a job not in the table (the saucer sip, the strip on the palm, the mic) is **a new row on that page**, with its comparison sheet, before any shot uses it. Films keep the old phone grip (v3).
4. **Don must read as a person** (the cold test's 0/3): a readable face in every Don close-up (offended, delighted, shocked), never blank; the saucer sip is the strongest proof. Re-tested at the board with the direct question "who is the man in front?".
5. **One prop, one silhouette:** Pam's mug is the same shape and colour in every shot (lesson 110: one prop, one place).
6. **Cause and effect in one frame** (132): Father's heel and the photo; Mom's pads and Don's lean; Pam's glance and the Client's blueprint (a cut pair, 6.6 → 6.7).
7. **Hold every story beat 0.5–0.6 s** (136): Pam's closed mouth, the feint, the barrier, the sticky salute.
8. **The loop is a state** (183) or a story step (STORYLINE rule 1): decided before the scene file (§6).

## 3. Lessons that apply, shot by shot

Written in full into `the-double-agent-lessons-v1.md` (with line numbers) before stage 4, as CLAUDE.md rule 1 asks. The map:

| Shots | Lessons |
|---|---|
| 1.1–1.3 the roll, the whack, Father's shoes | 141 (0:01), 10 (one visible physical rule: the sticky tail must show), 23 / 912 (reaction with a hold), 999 (a different last picture), 201 (a gag at body size), 221 (a gag needs a shape) |
| 2.1, 3.3–3.4, 5.4, 7.2 (S7 through the glass) | 22 (one idea moving at a time: floor or office, not both), 188 / 191 (two threads need one visible join: the glass), 136 |
| 2.2 the heel and the photo | 132 (cause and effect in one frame), 135 (Father's gender from the drawing: the cold test read "a woman" 2/3) |
| 3.4 the feint | 101 / 102 (a glance is not a turn: the feint is the body), 200 (a held beat needs one visible change) |
| 3.3, 3.5, 5.2, 6.1–6.2, 6.8, 7.1–7.3, 8.2 the hand jobs | rules-hands §0, 147 / 149 (one hand for the cast), 178 (three misreads: change the gesture), 221 / 224 (an arm needs its owner in the frame), 231 / 245 (an elbow target too close folds the arm), 244 (section 0 under time pressure) |
| 4.2 Don at the street door | 38 / 573 (nothing floats), the street door as 14 drew it |
| 5.1, 6.3, 6.6 the inserts | 134 (an insert needs an owner), 266 / 593 (one obvious object at phone size), 111 / 80 (text at 270 px) |
| 5.3 the inertia stop | 39 / 89 / 93 (feet stay planted; test as silhouettes first), 128 (wide eyes read as fear) |
| 6.4–6.8 the lines | speech.draw + speech_gate (tails 10–20 px), 197 / 198 (a long line on one frozen frame needs a cut), 217 (two lines in turn get a key frame each), 216 (the bubble's clash list holds the signs and the story props) |
| 8.1 the final image (S8) | 211 (a face in a picture is not a person), the dead zones (124–126), the set gate (props on their marks) |
| 9.2 → 1.1 the loop | 57 (frame 0 by the same code), 112 / 113 (frame 0 held 0.4 s; sound through the seam), 183, 239 (the loop holds the cause) |
| Sound | 105 / 230 (room tone and Whisper in the final mix), 107 / 202 / 864 (every gag has a sound or is decided silent; the music cut by the story's silences), voices dry (212) |

## 4. The plan, stage by stage

| Stage | What gets made | Pass | Stop | Budget |
|---|---|---|---|---|
| **1 Script** | `the-double-agent-script-v1.md` from concept v5: 33 shots, sizes, setups (S1, S3–S9), action → reaction, the inside/outside timing for every S7 shot, line, sound; **the protect list**; the 0:01 joke named with its frame (1.1, 0.4 s); the story chain (§5) and the direct questions | G0, G1; 4 lines (line budget); every verbal joke has an action; checked against front desk v4 and the canon locks. **No outside review** (G6 spent) | **1** | 4 versions |
| **2 Voices** | Existing voices only: Don `am_onyx`, Pam's voice as in 14. Four takes. `da_timing_v1.json` | Whisper 3/3 on every dry take, and with silence after it; the real length 50–60 s | **2** | — |
| **3 Look and set** | Opt-in, md5-safe: **S8, the floor from behind the glass** (the new background: counter backs, Mom's back, the tape, the throne, Don outside); the office inside (desk, Don's chair, the gold desk photo DON · CEO); **Pam's mug** (one silhouette, one colour); Don's cup and saucer; the minutes (the robot's printout style from 13's `of_ui`); the blue blueprint (13's plan drawing); REVIEW · TOMORROW tag (14's tag drawing); the peeled strip; F1–F5 from the cold test. **Hand sheet** for the three new hand jobs | Episodes 9–14 and the establishing frame rebuild **md5-identical**; every sign and prop reads at 270 px; the Don rule (tallest and widest) | — | — |
| **4 Scene file and layouts** | `src/da_scenes.py` (modelled on `ps_scenes.py`): the one source. Generated: script vN, a layout sheet per act, the top-down shot plan, **blocking sheets for 3.4 (the feint) and 7.2 (the barrier)** | G2; `uz_check`, `set_gate`, `hand_gate`, `speech_gate` on every layout frame; the dead zones; no stand-in poses (each pose with its object) | **3** | 3 versions |
| **5 Board** | One key frame per shot (and per line, lesson 217), at 540, under the app overlay | G3; **G4 on the whole board: the story chain + direct questions, 3 viewers.** Hard gate: no animation before it passes (§1). Then **one outside review** on the board | — | — |
| **6 Motion tests** | Six, at film rate, 540, strips at 8 fps: **A the roll on the shoe (0:01, first)**, B the feint, C the saucer sip, D the inertia stop, E the barrier and the duck, F the sticky salute | G4: two cold viewers each; A must read as a joke on mute | — | 3 versions each; a beat failing three fixes is cut (52) |
| **7 Animation** | Native 1080 (2×), 15 drawings/s acting, 30 fps camera; `da_film.py` modelled on `ps_film.py`, one drawing map asserted (109) | All gates on every frame; every change seen in a before/after strip; stills to Tomas before any changed render | — | — |
| **8 Rough cut** | Voices, effects (the list in concept v5), room tone (the office through glass: muffled), the office vibes from *The Onboarding*, cut by the story's silences | **G5** in full; **G4** with three viewers, the direct questions and "what felt rushed or slow" | **4** | — |
| **9 Polish** | Numbered fix lists | Every fix seen in the render; every instance of a fixed drawing checked (56) | — | **5 film versions, then frozen** |
| **10 Reviews** | Triage tables | G6: the last outside round, on the rough cut | — | 1 left |
| **11 Master and cover** | 1080 master (not committed), 540 copy, the cover (the final image: the meeting inside, Don saluting outside, is the natural cover) | G5 on the final AAC; a clean rebuild; the cover at 120 px | **5** | — |
| **12 Close** | `the-double-agent-film-vN.md` as built; lessons; README, INDEX, STORYLINE (v3.5: 14 as built, 15, the badge and the tear moved to 16) from the built film; a PR when Tomas asks | — | — | — |

## 5. The story chain and the direct questions (fixed now)

**The chain** (what a cold viewer must know after each act; tested at the board and the rough cut):

1. The man in front is the boss, a person, and the line is his.
2. Others are holding a meeting in his own office, and the older man has taken his chair.
3. The woman with the mug is pulled into the meeting; the older woman hides it from him.
4. She goes back in on her own, behind his back.
5. He sees her mug inside and is jealous / furious.
6. He can't cross his own line; the older woman takes a side against him.
7. The woman brings him a paper; he decides she is spying **for him**.
8. She could tell him the truth and doesn't.
9. He opens his own line to let her back in, proud.
10. Inside they work without him and give her the plan; outside he salutes; the tape is stuck to him.

**Direct questions:** (1) Who is the man in front: a person or something else? (2) Whose office is the glass room, and who sits in whose chair? (3) Why can't the man in front just walk into his office? (4) Whose mug is on the table inside, and why does it matter? (5) What does the man in front think the woman is doing for him? Is he right? (6) Why does she say nothing? (7) Who gets the blue paper, and what does that mean for him? (8) The video loops: what happens next?

Pass: every viewer reads at least 8 of 10 chain points and answers every direct question; two viewers making the same mistake is a staging fault.

## 6. Tomas's decisions (26 Nov, /grill-me)

| # | Question | Decision |
|---|---|---|
| 1 | The loop | **A state, a tight opener** (lesson 183): 1.1–1.2 are close (the shoe, the roll); the gap in the line and the strip on his hand are not seen before the seam. The wide 1.3 is framed so the gap's place is out of shot or hidden by Don |
| 2 | Release order | **In parallel up to the board:** 15's script, voices, set and board now; its animation only after 14's master. Releasing 11–14 is handled alongside |
| 3 | The freeze rule | **Yes, for the whole series:** an approved film is not reopened for rules written later (hands, bubbles); they apply from the next episode. The only exception: a fault Tomas sees himself |
| 4 | S8 (the floor seen from inside the office) | **A still now, before the script:** the final image (8.1) as one frame and a cold test; if too costly or unreadable, the S7 fallback while the script is still unwritten |
| 5 | Pam's mug | **Mustard yellow** (the complement of her purple), one silhouette in every shot; checked at 270 px against the yellow tape (thickness and shape differ) |

## 7. Risks and their fallbacks (set now, lesson 95)

| Risk | Fallback |
|---|---|
| The roll doesn't read as sticky before the shoe lands (motion test A fails three times) | Open on 1.2 (the whack) with the roll already on the shoe; the sticky tail shown in the loop's last shot instead |
| Don still reads as a robot at the board | The saucer sip moves earlier (to 4.1, with Pam); his first close-up gets a big human face (an offended pout) at 2.3 |
| The feint (3.4) reads as nothing on a still pair | Mom's pads follow a third, bigger lean (a hop) instead of a feint |
| A hand job fails three misreads | Change the gesture (178): the saucer sip → he gulps from the cup and spills it on his vest; the strip on the palm → the strip on his vest |
| S8 too costly or unreadable | The final image in S7 from the floor (Don saluting in front, the meeting behind the glass), the original v3 composition |
| Length over 60 s | First trims: 4.3 (Pam past Mom) into 4.2; 6.2 into 6.1 |
