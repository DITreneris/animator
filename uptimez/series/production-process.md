# UptimeZ Inc.: from script to final film (production process v1)

22 Nov. How an UptimeZ episode is made, from the first script to the master. It is built from lessons 1–122 (`docs/lessons.md`), the gates in [`../CLAUDE.md`](../CLAUDE.md), the episode 12 plan, and what episodes 9–12 cost in practice. Tomas decided its five shape-giving choices on 22 Nov (marked **decided**). The first episode to follow it is 13, *The Offer*.

## Why this process

Episodes 9–12 taught us five things:

1. **Fixes that were reported but never reached the screen.** A later entry in a drawing map overrode Mom's lips and Pam's payoff for ten film versions (lesson 109).
2. **Faults found by Tomas instead of by our checks.** Pam's third arm, tails on hair and crowns, cut-off SHRE, DO and R FIR, stray dashes. We had looked at contact sheets; nothing measured them.
3. **Problems that belong to layout turning up in the film.** Small characters, a calendar in three places, signs cut by the frame.
4. **Versions without a budget.** First Search took 35 film versions, and most of them fixed one or two things Tomas had spotted.
5. **What worked.** The gates, laying out each scene before animating it, voices before drawings, motion tests of the hard moments, the scale checker, and never breaking earlier work.

The process answers with four rules:

- **One source** (decided). From layout on, a single scene file per episode generates everything.
- **Checks that fail the build** (decided).
- **Five stops for Tomas** (decided).
- **A version budget per stage** (decided).

## The four rules

### 1. One source: the scene file (decided)

From stage 4 on, `src/<ep>_scenes.py` is the episode. It holds every shot:

- id, scene, duration, and the line with its take;
- camera setup and size;
- who is in frame, where they stand and how big;
- props and signs (whole or out);
- the action and the reaction;
- the effects.

Everything else is generated from it and never edited by hand:

- the script (`<ep>-script-vN.md`, marked "generated", as `daddys-home-script-v2.md` is);
- the layout sheets, the shot plan and the board;
- the animatic and the film's shot list and timing.

A change is made in the scene file and regenerated. A script written by hand (stages 1–3) is the plan the scene file starts from, and it is kept.

### 2. Checks that fail the build (decided)

`src/uz_check.py` runs on every render: the board, the motion tests, every scene and every film. A failed check stops the build with the shot, the frame and the reason. **No check counts until it has caught a known failure** (right column).

| Check | What it measures | Must catch (known failure) |
|---|---|---|
| **Drawing map** | Prints which function draws each shot; asserts that every shot changed in this version points at the new function | First Search v26–v34: `show` and `momdesk` overridden by film 4's drawings |
| **Scale** | Biggest face r 78–80 at 540 px near y 400; nothing story-critical below y 720 or under the right rail (x > 470, y 380–860); characters at the film's own scale (`cs_frame.py`). **Faces are where the rig drew them** (the robot's visor, not its antenna) | One Star's small characters under the buttons; The Offer's robot visor at y 650 (planted: y 790) |
| **Proportions** | Every character at its scene scale on one floor line, against the set's home table (`fs_set4.HOME`); **DON is the tallest and widest in any frame he shares** (`of_scenes.don_rule`, `python3 of_scenes.py don-validate`) | The Offer: the robot at the storyboard's 0.40 read as a gnome, "a rat", beside the throne; now 0.66 (the storyboard forces `SC` inside set shots: set it there); the Client is 111% of Don's height and 152% of his width (never in a frame with him in episode 13) |
| **Zones** | Every story prop a beat depends on is declared in the scene (`of_set.protect()`: phones with a screen, the lighter, the lamp in hand, a card, a button) and stays out of the dead zones | The Offer layout v4: 22 frames (lighter, lamp, DELETE, ACCEPT, DAD) |
| **Signs** | Every sign (text drawn by the set or a prop) is fully inside the frame or fully outside, after the camera | First Search v35: SHRE at 0:06, DO at 0:27, R FIR at 0:29, T CLIENT at 0:43 |
| **Tails** | Every tail ends beside the mouth drawn in that frame; never from above onto hair, a curl or a crown; no tail for an off-screen speaker | First Search v35: 15 tails on hair, curls and crowns |
| **Limbs** | Counts the arms drawn per character per frame from the rig calls; more than two stops the build. Drawing over or clipping an arm away must also go through the counter | First Search v36: Pam's third arm at 0:42; her crossed arms at 0:41 |
| **Strays** | Marks (dashes, speed lines, puffs, stars) with no character or prop within reach in that frame | First Search v36: the step dashes at 0:36; the furious puffs read as a thought bubble |
| **Text** | Every bubble and card inside the safe area (18, 96, 522, 820); narration under the top bar; no bubble over a face | Office Noir's cards under the top bar |
| **Loop** | Frame 0 and the last frame drawn by the same code; difference only where the script says (a date, a mark) | First Search's frame 0 drawn from the set's old master |
| **Sound** | Per line, three Whisper windows inside the final mix; −14 to −16 LUFS; true peak ≤ −1 dBTP on the final AAC; no dead stop at the seam | One Star's room tone (7 of 14 lines lost) |
| **Format** | 1080×1920, 30 fps, expected frame count, BT.709 converted and tagged | Flat colours from BT.601 tagged as BT.709 |

**Validation so far** (`src/uz_check_validate.py`, results in `src/uz_check_validation.json`; 19 cases, all behave). Each case must fail on the faulty version and pass on the fixed one:

- On the real failures: drawing map (v33/v34), signs (v35/v36), tails (v35/v36), strays (v36/v37), limbs (v36/v37; the hand-drawn writing arm declared with `uz_check.limb`, as a scene file will do).
- On faults made from real drawings, because the old episodes named above are not in this format: text (v36 bubbles moved 140 px up), scale (v36 camera 330 px higher), sound level, loop and format (the v37 copy made 6 dB hot, cut at 0:40, left at 540, its colour tags removed).
- The dead-zone checks (`of_scenes.py zones-validate`): the robot lowered (visor y 790) and the DELETE phone under the buttons must fail; 3.2 as framed must pass.
- Not yet covered: per-line Whisper in the final mix (the takes are checked by `of_voices.py`), "no bubble over a face", and the loop's "same code" rule.
- One fault the checker found is still in First Search v37: the robot's HR-line tail ends at eye level. It is allowed by name in its case.

A known artefact of a check (for example, "Zero results." scoring 1/3 because its window holds the line before) is written into the episode's QA note once, with the evidence, and allowed by name. It is never silenced in general.

### 3. Five stops for Tomas (decided)

Work stops and waits for Tomas at:

1. **Script**
2. **Voices**, with the timing
3. **Scene layouts**
4. **Rough cut with sound**
5. **Master**

Between stops it goes on unless a gate fails. Every stop sends:

- the file, and one line on what changed;
- the gates passed, with evidence;
- the open decisions, as multiple choice.

### 4. A version budget per stage (decided)

| Stage | Budget |
|---|---|
| Script | 4 versions |
| Scene layouts | 3 versions |
| Motion test (each) | 3 versions |
| Film, from the rough cut | 5 versions |
| Outside reviews | 2 rounds (G6) |

When a stage runs out of budget, the next version needs a written reason, or the work goes back one stage. Three fixes that don't land on the same beat mean the beat is cut (lesson 52).

## The stages

Each row lists what goes in, what comes out, what must pass, and whether Tomas approves.

| # | Stage | In | Out | Pass | Stop |
|---|---|---|---|---|---|
| 0 | **Start** | STORYLINE, the previous episode **as built** (its film doc, not its plan), the set doc, the lessons | A branch `uptimez-<episode>`; the episode folder | The previous episode is on main or its branch is named; canon read against the last film | — |
| 1 | **Script** | The concept or the storyline row | `<ep>-script-vN.md`: every shot, line and action; the protect list; section times; open decisions | **G0** series check, **G1** protect list; a line budget; every verbal joke has an action; checked against the set (lesson 108) and the canon locks; outside reviews triaged (**G6**) | **1** |
| 2 | **Voices** | The approved script | Auditions for new voices; every take; `<ep>_timing.json` | Whisper on every dry take; **the real length is known** and within 40–90 s (arc: 60–90 s) | **2** |
| 3 | **Look and set** | New characters, props and sets | Look sheets at series proportions beside the cast; set changes opt-in; the set doc updated | Earlier episodes rebuild **md5-identical**; signs on new props read at 270 px | — |
| 4 | **Scene file and layouts** | Script, timing, set | `src/<ep>_scenes.py`; generated: script, a layout sheet per scene, a top-down shot plan, a blocking sheet for the hardest beat | **G2**: action and reaction per beat, sizes and eyelines; every turn is an action. **`uz_check`** on each layout frame (scale, signs, tails, limbs, text). The blocking test (lesson 62) | **3** |
| 5 | **Board** | Scene file | One key frame per shot at 540, generated | **G3**; **G4 on the whole board** with two cold viewers and the loop question; two viewers making the same mistake is a staging fault | — |
| 6 | **Motion tests** | The hardest moments, named in the scene file (an entrance, an impact, a reach, a head turn) | A short test each, at film rate | **G4**: two cold viewers on 8 fps strips; `uz_check` | — |
| 7 | **Animation** | Scene file, tests | Scene renders, native 1080 (rendered at 2×), **15 drawings a second for acting, 30 fps camera** (decided) | `uz_check` on every frame, including the drawing map; every change seen in a before/after strip of that shot | — |
| 8 | **Rough cut** | Scenes, takes | The full film: voices, effects, room tone, music | **G5** in full; **G4**: two cold viewers on 4 fps sheets plus 8 fps strips of quick beats, the open prompt **and** direct questions (lesson 106), and "what felt rushed or slow" | **4** |
| 9 | **Polish** | Tomas's notes, cold viewers, reviews | Film versions, within the budget of 5 | Each version is a numbered fix list; each fix is shown in the render (full size, frame by frame), and every instance of that drawing is checked, not just the one reported (lesson 56) | — |
| 10 | **Reviews** | Outside reviews | A triage table: OK / partial / fail / disagree, what correlates, which points undo Tomas's choices | **G6**: two rounds at most; protect list intact | — |
| 11 | **Master and cover** | The approved film | 1080 master and 540 preview (rebuilt locally, not committed from 24 Nov per `.gitignore`), the cover (committed) | G5 on the final AAC; a clean-checkout rebuild; cover read at 120 px and in the profile crop | **5** |
| 12 | **Close** | The master | `<ep>-film-vN.md` (the film as built, shot by shot); lessons; README, INDEX and STORYLINE rows written from the built film; old render frames deleted | Committed and pushed when Tomas asks; a pull request per episode | — |

## Cold viewers (decided: board, motion tests, rough cut)

Cold viewers see the episode three times: the **board** (stage 5), each **motion test** (6), and the **rough cut** (8). Every time:

- Two fresh agents who have never seen the script, shown numbered frames only.
- The same open prompt each time: what happens; whose situation it is; what changes; who sides with whom; the last image; what was confusing; what felt rushed or slow.
- After the open prompt, the episode's direct questions, written into the script at stage 1 (for example, *The Offer*'s five).
- Pass mark: both viewers read at least 4 of 5 beats, and answer every direct question.

## Working rules at every stage

- **"Fixed" means seen in the render.** Look at the changed shot at full size, frame by frame, before saying it. A contact sheet is for finding faults, not for confirming fixes.
- **Never break earlier work.** New behaviour on shared modules is opt-in, existing `_vN` files stay untouched, and approved renders rebuild md5-identical (see `../CLAUDE.md`).
- **The freeze rule (decided 26 Nov, Tomas):** an approved film is not reopened for a rule written later (hands, bubbles, gates); the rule applies from the next episode. The only exception is a fault Tomas sees himself.
- **Pinning (decided 24 Nov):** for new episodes, pin each approved stage or cut with an immutable `git tag` (for example, `uptimez-<ep>-vN`) rather than copying whole `_vN.py` files in `src/`. Existing `_vN.py` files stay as built.
- **Disk:** the build keeps only the current version's frame folder. Old folders and test renders are deleted at each version (lesson 122).
- **Language and commits:** reply in Lithuanian when Tomas writes Lithuanian. Commit and push only when he asks, on the episode branch, never to main.

## Episode 13 from here

*The Offer* is at stage 1: script v3 is written and its open questions are answered. Next:

- **Stop 1:** Tomas approves script v3.
- **Stage 2:** auditions for the Client's garage voice if it changes, the bodyguards stay silent, the timing file.
- **Stage 3:** the garage set and its props.
- **Stage 4:** `src/of_scenes.py`, the first scene file under this process.
- **Before stage 4:** `uz_check.py` is built and validated on the known failures in the checks table.
