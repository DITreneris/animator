# Daddy's Home: review and production plan v1

UptimeZ Inc. · episode 12 · 21 Nov · for Tomas's decision. Nothing here is built. It reviews concept v3, the repo, the lessons and the skills, then sets out how episode 12 gets made.

## 1. Ambition, goals, horizons

**Ambition:** episode 12 is the first one where the series changes genre for 20 seconds. Sixty seconds of office panic, then a gangster film walks in and nobody is joking any more. If it works, Father is a character people wait for, and Act C has a villain.

**Goals for the episode (measurable):**

| Goal | Measure |
|---|---|
| It reads on mute | Two cold viewers answer all of: who is coming, who the man with the case really is, what lands on Don's head, what the robot looks at, who is calling at the end |
| Father is frightening, not funny | Both cold viewers describe him with a fear word, unprompted; nobody calls him "the dad" only |
| The first joke by 0:02 | The DAD phone and Don's drop, in frame 0–2 s |
| Length | Rough cut at most 90 s; target after trim **75–80 s** |
| Lines | At most 32 after trim (v3 has about 38; One Star had 14 in 62 s, The Best Candidate 35 in 92 s) |
| Scale | `cs_frame`-style check passes on every shot: biggest face r 78–80 at 540, nothing story-critical under y 720 or the right rail |
| Sound | −14 to −16 LUFS, peak ≤ −1 dBTP, Whisper on every line |

**Horizons:**

| Horizon | What | Done when |
|---|---|---|
| H0, now | Close One Star: Tomas's listen, lessons written, README/INDEX rows, branch to main | Episode 11 is on main and documented |
| H1, episode 12 | Daddy's Home from script to master | Tomas approves the master |
| H2, Act C | 13 The Demonstration, 14 The Refund, 15 Permission to Succeed, 16 Renewal Day, the finale | Each has a one-page concept before 12's animation ends, so 12 plants what they need |
| H3, the series | Release order (10 before 11 before 12), covers, platform checks, and learning from real viewers instead of only cold agents | The first three Act B episodes are out and their numbers are read |

## 2. Review of concept v3

**Gate G0, the series check:**

| Check | Verdict | Note |
|---|---|---|
| Two wants collide | PASS | Don wants to look like a CEO; Father wants his money |
| One comic mechanism | PASS | Fear makes them show everything to the wrong man |
| One iconic image | PASS, pick one | The wet filter on Don's bald head (the cover), or the robot staring at the chair (the ending) |
| The image loops, the story advances | PASS with a fix | See fault 6 |
| Status moves | PASS | Don: boss → salesman → child → suspect |
| Works on mute | **AT RISK** | 38 lines in 90 s. The physical beats from the review help; the tour and beat 2 are still talk |

**Faults found in v3 (to fix in the script, not by rewriting the concept):**

| # | Fault | Evidence | Fix |
|---|---|---|---|
| 1 | **Don has no desk on this set.** Frame 0 says "feet up", but on the front desk set Don stands under his portrait in zone B; the counter belongs to Pam and Mom | `series/front-desk-set.md` | Don sits **in the CEO chair** in zone B, feet up on the shredder, phone on the chair's arm. That plants the chair in frame 0 as the thing he loves |
| 2 | **The coffee machine has no place** | Same doc | On the counter beside Pam (zone C). It gives her motive a location and keeps it in her shots |
| 3 | **"Human approval required." has no object** | Canon: the robot needs approval for money, access, commitments, system changes | "Unregistered visitor. Human approval required." → Father: "Approved." He approves his own entry. Then "Welcome, majority shareholder." |
| 4 | **The green star needs Don's "Approved."** | Canon, and episode 10's green zero | DON: "Make it green." ROBOT: "Human approval required." DON: "Approved." This also sets up Father taking the word from him 50 s later |
| 5 | **Nine characters, one vertical frame.** Don, Sofía, Pam, Mom, the robot, the repairman, Father, two bodyguards. At series face scale, three fit in a shot | `cs_frame` rule, One Star's scale failures | No group shot at the arrival or the freeze. The freeze is **five held singles or pairs, 0.3 s each**, or one slow pan along the line. Decide at layout (G2b) |
| 6 | **The loop's two phones don't match.** The last shot has the phone buzzing in his vest pocket; frame 0 has it on a desk | Lesson: frame 0 and the last frame are diffed | Both are the same insert: the phone face, DAD, lit. At the end Don pulls it from his pocket and we cut on the screen |
| 7 | **Father "is parking" in episode 8** | `README.md`, The Best Candidate | No conflict if nobody mentions it. Don't add a line about it |
| 8 | **The robot "rolls forward"** | The HR robot has a station in zone A, by the door | It doesn't roll. It is already at the door, which is where a visitor check belongs |
| 9 | **No protect list** | Gate G1 | Below |

**Protect list (G1), proposed:**

1. Father never jokes, shouts, slips or hurries. Six short lines.
2. "Good. Find my money." and the robot's slow head turn to the chair.
3. The wet filter stays on Don's head until Mom takes it off.
4. "I'm here to inspect the machine." Nobody looks at the coffee machine.
5. The loop: DAD rings while Father stands in front of him. "Answer it."

Any later cut that removes one of these is refused or replaced.

## 3. Review of the repo

| Finding | Evidence | Action |
|---|---|---|
| **One Star isn't on main** | `uptimez-one-star-calendar` is not an ancestor of `origin/main` | Episode 12 builds on it. PR and merge first (when Tomas says), or branch 12 from it and say so |
| **Episode 11 is missing from the docs** | No One Star rows in `README.md` or `INDEX.md`; `STORYLINE.md` row 11 still describes the old plot (the Client saves Pam's number) | Write the rows from the built film |
| **`docs/lessons.md` stops at First Search (19 Nov)** | No One Star section | Write it (section 4) |
| **`src/` has 1,026 files** | Mostly `_vN` pins | Don't clean it now: the pins are what make md5 rebuilds possible. Add one index of which pins belong to which release, later |
| **One Star's helpers have `cs_` names** but are series tools | `cs_frame.py` (scale and dead zones), `cs_sfx.py`, `cs_cal.py`, `cs_layout.py` | Episode 12 imports them as they are. Renaming would break pins |
| **The set doc has no CEO chair, coffee machine or club booth** | `series/front-desk-set.md` | Front desk **v5**, opt-in: the chair in B, the machine on the counter in C. Written into the doc with the reason. The booth gets its own small module |
| **Uncommitted now** | `daddys-home/` (concepts v1–v3, this plan), and the Father edits in `STORYLINE.md`, `CLAUDE.md`, `README.md` | Commit when asked |

## 4. Lessons to write down (One Star, 19–21 Nov)

Not yet in `docs/lessons.md`:

1. **Lay the scene out before animating.** A layout sheet per scene (who, where, what size, which prop) caught what the board didn't.
2. **Scale is measured, not judged.** `cs_frame.py`: face radius, the bottom line, the right rail, signs whole or out. Run it on every shot before rendering.
3. **Arms move by IK from the shoulder**, not by blending pose angles.
4. **The change happens on screen.** The number being written, the star turning, the sheet torn off. A before/after cut reads as two different props.
5. **A glance is not a turn.** Reactions that were only a look were misread by both cold viewers; an action wasn't.
6. **One face per reaction.** A smug face read as tense. Remove the ambiguous one instead of tuning it.
7. **A prop in a hand** needs the hand drawn for that prop; one extra thumb gets seen.
8. **One calendar in the series.** A shared prop is drawn by the episode that made it.
9. **Room tone and reverb are checked by Whisper**, not by ear: 7 of 14 lines were lost before the tone came down.
10. **A line that doesn't work is a premise problem.** "Correct. We will recover." took three rewrites; the fix was a different stance ("Shut off!"), not better wording.
11. **Ask direct questions in the cold test** as well as the open prompt: six yes/no facts the episode depends on.
12. **Concept reviews:** every verbal joke gets a visible action that causes it or makes it worse (today's review).

## 5. Skills

| Skill | State | Change proposed |
|---|---|---|
| `animation-episode-gates` | Has G0–G6 and G2b | Add **G2c Layout and scale**: a layout sheet per scene and a measured scale check before any animation. Add the line budget to G0. Add the direct-question list to G4 |
| `cold-viewer-mute-test` | Works | Add: six direct factual questions after the open prompt; an 8 fps sheet is compulsory for any hit under 0.5 s |
| `video-making` | Fine | None |
| `../hoodyz/.claude/skills/` copies | Written for Hoodyz | Leave; `uptimez/CLAUDE.md` already says not to apply their series check here. Add G2c to `CLAUDE.md`'s gate table |

## 6. The process, stage by stage

Each stage ends at a gate. Tomas decides at the stages marked **T**. A failed gate goes back one stage.

| # | Stage | Output | Gate and pass mark |
|---|---|---|---|
| 0 | **Close episode 11** | Lessons section, README/INDEX/STORYLINE rows, the branch on main | Tomas has listened to rough v5 with sound. **T** |
| 1 | **Script v1** | `daddys-home-script-v1.md`: every line, every action, the protect list, section times. Faults 1–8 fixed | **G0 + G1.** Lines ≤ 36; every verbal joke has its action; canon checked against STORYLINE. **T** (/grill-me on the open choices, section 7) |
| 2 | **Voices** | Kokoro auditions: Father (3 candidates, low, slow, pitched down) and the repairman (2). A timing file from the takes | Whisper on every take. The real length is known before anything is drawn. **T** picks Father |
| 3 | **Look sheets** | Father, the bodyguard (one design, mirrored), the repairman, at series proportions beside Don and the Client; the CEO chair; the coffee machine (broken / pop / steaming); the filter; the phone DAD; the green-star post | Silhouette test: the repairman and a bodyguard look alike at 270 px, and different at full size. Father reads as Don aged. No real brands. **T** |
| 4 | **Set v5 and the booth** | The front desk with the chair and the machine, opt-in; the club booth; the set doc updated | Episodes 10 and 11 rebuild **md5-identical** |
| 5 | **Shot list** | Every beat: action shot, reaction shot, size, eyeline, camera setup S1–S6, duration | **G2.** Every story turn is a physical action. No shot holds more than three faces |
| 6 | **Layout** | A layout sheet per scene; top-down shot plan; a blocking sheet for the two hardest beats: **the arrival** (three knocks to "Approved.") and **the filter** | **G2b + G2c.** The scale checker passes on every shot. Two cold viewers on real camera frames of the arrival. **T** |
| 7 | **Board** | One key frame per shot, 540 | **G3**, then **G4 on the whole board** with the loop question |
| 8 | **Motion tests** | Four short tests before the full animation: the filter pop and landing; the chair rolling back; the robot's head turn with Don's sidestep; Father's entrance | Each read by two cold viewers on an 8 fps sheet. A test misread three times is cut and its thread carried elsewhere |
| 9 | **Scenes** | Six or seven scene files, native 1080, 12 drawings a second | Scale check and bubble checks on every drawing |
| 10 | **Rough cut** | Voices, effects, room tone, music. The music stops dead on the three knocks; a different, low bed for Father | **G4** (two cold viewers, the direct questions) and **G5** (format, loudness, Whisper). **T** watches |
| 11 | **Trim** | To 75–80 s. Candidates in order: beat 2's Pam exchange, beat 5, the tour | The protect list is intact. **T** |
| 12 | **Reviews** | Outside reviews triaged | **G6:** at most two rounds |
| 13 | **Master and cover** | 1080 master (not committed), 540 copy, the cover (the filter on Don's head, Father's shadow in the door) | G5 on the final AAC; frame count after muxing; a clean-checkout rebuild. **T** approves |
| 14 | **Close** | Lessons, README/INDEX rows, STORYLINE row 12 from the built film | Committed and pushed when asked |

**What can be reused:** Don, Sofía, Pam, Mom, the robot, the set, the calendar, the phone and post from One Star, the breathing and IK code, the effects library, the film assembler, the scale checker, the Whisper QA.

**What is new work, biggest first:** Father and the bodyguards (new rigs); the arrival and the freeze (nine characters); the coffee machine with the filter; the repairman; the booth; the CEO chair on casters.

## 7. Decisions for Tomas before script v1

1. **Frame 0:** Don in the CEO chair with his feet on the shredder (recommended), or a new desk for Don.
2. **The freeze:** five quick held shots (recommended, keeps faces big), or one pan along the line.
3. **Length target:** 75–80 s after trim (recommended), or keep 90 s.
4. **Episode 11 first:** merge One Star to main before starting 12 (recommended), or build 12 on the open branch.
5. **Father's face:** hidden until he walks in (recommended, as in the concept), or shown in the booth.

## 8. Risks

1. **Too many people.** Solved only by shots of two or three and a camera that visits each zone.
2. **Too many words.** The line budget is a gate, not a wish.
3. **Father comes out comic.** The voice audition and the entrance test decide this early, before the scenes are animated.
4. **The repairman takes over.** His chain is capped at 19 s.
5. **New rigs slow everything.** Look sheets and motion tests come before any scene, so a bad rig costs a day, not the episode.
