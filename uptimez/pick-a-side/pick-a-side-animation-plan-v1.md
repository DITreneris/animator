# Pick a Side: the animation plan (stage 7), v1

UptimeZ Inc. · episode 14 · 25 Nov · for Tomas's decision. Follows [`series/production-process.md`](../series/production-process.md) stage 7 and the stage plan [`pick-a-side-plan-v1.md`](pick-a-side-plan-v1.md). The lessons it applies: [`pick-a-side-animation-lessons-v1.md`](pick-a-side-animation-lessons-v1.md). **Nothing is animated yet.** Stage 7 is held by the release-order rule (plan §2, 0.5: animate 14 only after episode 12's fix plan) until Tomas lifts it.

## 1. Where the episode stands (audit, 25 Nov)

| Stage | State | Open |
|---|---|---|
| 1 Script | v8, generated (38 shots, 66.3 s, 19 lines) | — |
| 2 Voices | 19 takes, Whisper 3/3, `ps_timing_v3.json` | — |
| 3–4 Set, scene file, layouts | `ps_scenes.py` is the one source; `check`: 38 shots, 0 faults | — |
| 5 Board | v3, 42 key frames; cold test passed 3 of 3; outside review round 1 built | Outside round 2 is saved for the rough cut (G6) |
| 6 Motion tests | A–K (below); animatic `ps_animatic_v1.mp4` (540, board + takes) | The throne spin (2.2) has no test |

### What the motion tests cover

| Test | Shot | State | Into the film as |
|---|---|---|---|
| A | 1.1 the blinds tug of war (the 0:01 joke) | v3 approved | Redrawn on board v3's staging (A was drawn before the set fixes) |
| B | 2.10–2.11 the robot ×3 | v3 approved, **superseded**: 2.11 is one push now | Replaced by H |
| C | 5.4 Don's foot over the line | v3 approved | Redrawn on board v3's staging |
| D | 2.1 the tape rips toward the camera | v2 | As tested |
| E | 3.1–3.2 the selfie arm, FLASH, the photo | v1, read 2/2 | As tested |
| F | 5.6 Sofía crosses, Pam frozen | v1, read 2/2 | As tested |
| G | 6.1 nobody looks; Pam's reach | v3; the reach moved to 5.7 | As tested |
| H | 2.10b–2.11 smug, the bump, the fall | v4, 3 of 3 | With the viewers' two notes: the hit one drawing longer, the fall lands or cuts |
| I | 6.1b the startle | v1, accepted | Checked in the rough cut |
| J | 4.2 the finger to the heel | v1, accepted | Checked in the rough cut |
| K | 5.5 Sofía's three steps onto the tape | v3, 2 of 3, accepted | As tested |

About 20 of the 66 seconds are covered by tests. Not yet tested but moving on the board:
- 1.2a, the blind falls;
- 2.2, the throne spin (the stage plan named it as test 3);
- 2.4, Pam crosses;
- 4.3, the Client's finger and Father's nod;
- 5.2, COO? written;
- 5.3, the door opens and Sofía goes to it;
- 6.2, the loop's hand on the cord.

## 2. The risks, and what the plan does about each

| Risk | Evidence | Answer |
|---|---|---|
| **Two sources.** The tests re-stage their shots in `ps_motion.py` and steer the scene file through switches (`STEP_55`, `FINGER_42`, `SPRING_61B`, `NO_SHIFT`) | Lesson 109: a later map entry undid two fixes for ten versions | One map in `ps_film.py`; the tests become thin callers of the film's shot functions (§3.2) |
| **Version runaway** | The Offer's film reached v49 against a budget of 5; most overruns were motion and staging found in the film (plan v1 §1) | Stills of every key pose before any video (Tomas's rule, 24 Nov); scene by scene; untested moves get a still sheet first |
| **Frozen shots** | The Offer at 67.6 s had half its 41 shots frozen (lesson 195); "nothing happens" 3 of 3 (200) | Every shot gets at least one visible change; the script's "still" shots are listed in the lessons doc |
| **Short shots** | Nine shots of 1.0 s or less; H v4's hit read "rushed" 3 of 3 | Hold the story beats 0.5–0.6 s (136). Any time added is taken from a named shot, so 66.3 s stays the length |
| **Contact by hand** | The rigs return hand points without the lean or tilt; H and J corrected it in the test | Fixed once, opt-in, before scene 2 (§3.5) |
| **Sound comes last and breaks the mix** | Lessons 105, 202, 230 | The sound map (§4) is written with the exposure sheets, not after the picture |

## 3. How it is built

### 3.1 `ps_film.py`, modelled on `of_film.py` (reused, not new)

- **Built from:** one function per shot taking `(t, L)`, `render_scene(n)`, `mouth_at` (lips from the take's loudness), `bubble_on` (a bubble lives as long as its line), and `held_only` (a dead-zone fault counts only when it lasts several drawings, so a prop passing through is a move). **New:** a check that fails a shot whose drawings never change (lesson 200), proved on a planted still shot first.
- **The picture:** 15 drawings a second on a 30 fps camera. Review copies at 540; only the master at native 1080 (rendered at 2×, `set_device_scale(2, 2)`).
- **Every drawing goes through** `ps_checks.frame_checks`, `speech_gate.check`, `set_gate`, `hand_gate`, and the loop check (1.1 against 6.2). A fault stops the build with the shot, the drawing and the reason.

### 3.2 One map, one source

- `ps_film.SHOT_FN = {shot id: function}`. A shot not in the map is a hold: the board's key frame, plus lips, blinks and its bubble.
- The approved test motion moves into the shot functions: `tug_state`, `d_state`, the selfie, the crossing, `h2_state`, the startle, the finger, `k_gait`. Each `ps_motion.shot_X` then calls the film's function, and its old renders must rebuild md5-identical (the tests are pinned as they stand).
- The build asserts and prints the map (lesson 109).

### 3.3 Exposure sheets first

Per scene, before any code: a table of shot × drawing (key poses, holds, the one visible change, the cut points), and the key poses rendered as **stills**, sent to Tomas. Video only after the stills are seen (Tomas, 24 Nov: "nerenderink kol nepadarai .png").

### 3.4 Scene by scene, with sound

1. **Scene 1 first** (1.1–1.4, 8.1 s, the 0:01 joke): the exposure sheet and stills; then the scene with its voices, the blind clatter and CRASH; the checks; then 2 cold viewers on a 4 fps sheet plus an 8 fps strip of 1.1–1.2b. Asked directly: "what are the two fighting over?"
2. **Scenes 2–6** in story order, each the same way: the sheet and stills, the scene, the checks, a look at full size. A cold test per scene only where a new move was not tested (2.2, 2.4, 4.3, 5.3, 6.2).
3. **Join:** the loop check, the whole film's 4 fps sheet, then the rough cut (stage 8, **stop 4**).

Version budget (process §4): 3 per scene before the rough cut, then 5 for the film. A move that fails three times is cut or changed (lessons 52, 178).

### 3.5 Before scene 2: the rig's hand points

`don_ps`, `sofia_ps` and `robot_ps` return hand points without the lean or tilt they then draw with. The fix: an opt-in flag that returns the drawn points, validated on a planted fault (a grip 20 px off must fail `hand_gate`). Earlier episodes rebuild md5-identical.

## 4. Sound map (written with the sheets, built at stage 8)

| Where | Sound |
|---|---|
| 1.1 the tug of war | The blind's rattle on each pull; no music until the crash |
| 1.2a–b | CRASH; the cup's clink stops |
| 2.1 | The tape screech toward the camera |
| 2.1b, 5.1 | The clip; the beep; the buzz |
| 2.2 | The throne's roll and creak |
| 2.11 | The roll back and the bump (a soft thud plus a spring); the music cut dead on the hit |
| 3.1 | The telescope arm, the FLASH (the only flash) |
| 3.5–3.6 | Posted; the DING from the bodyguard's phone outside the door |
| 5.3 | The door; "Welcome." |
| 6.1b | The buzz that startles him |
| Bed | The series' sparse vibes (chords only), cut by the story's silences (107); a low office tone under the dry voices |

## 5. Next, in order

1. **Tomas decides the release order:** keep 14's animation on hold until Daddy's Home is finished, or lift the rule.
2. **The throne spin (2.2):** test it now (test L) or let scene 2's stills decide.
3. Then `ps_film.py` with the map (§3.1–3.2), proved on scene 1 before anything else is drawn.
4. Scene 1's exposure sheet and stills go to Tomas.
