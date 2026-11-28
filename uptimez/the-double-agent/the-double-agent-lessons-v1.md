# The Double Agent: lessons for stage 4 (the scene file and the layouts), v1

UptimeZ Inc. · episode 15 · 27 Nov. CLAUDE.md rule 1: every lesson that applies to stage 4, collected from `docs/lessons.md` **as it is on main** (f031c29) before `da_scenes.py` is written. **# is the lesson's own number, Line its line in that file.** "Here" is this episode (script v4 with the 27 Nov amendments: the two spaces at every cut, the lines inside/outside, the pull-back 8.1, Pam's 6.2). Hands: `docs/rules-hands-and-phones.md` §0 and the library (`hand_lib_v4`), as in stage 3.

**New from this episode (27 Nov), added to `docs/lessons.md` as 249–253:** the destination behind the glass (249), the dolly as planes by depth with the glass's look tied to the glass (250), two spaces at every place change (251), J- and L-cuts between the spaces (252), lines paired across the glass (253). Also in `series/production-process.md` (working rules).

## 0. Three lessons that change something already decided (for Tomas)

| # | Line | Lesson | What it touches | Proposal |
|---|---|---|---|---|
| 22 | 526 | **Stage one idea at a time**: one thing moves, everything else waits | The two spaces (27 Nov): 3.4's background reads "Pam **setting** her mug" during Mom's wall and the feint | Background = a **state**, not an action: in 3.4 the mug is already on Father's table, Pam's hand on it, still. Same for 4.1, 7.2, 7.4 (the rule "still on every peak and line" already says so; the script's verbs should too) |
| 42 | 577 | **Let a line run on across a cut** instead of stretching the shot | Pam's new 6.2 line made 6.2 0.96 s longer (2.16 s); 8.1 +0.24 s; the film 69.4 s | "I took notes." starts on 6.2 and runs into 6.3's insert (the page itself), so 6.2 stays near 1.2 s; the film ~68.4 s |
| 83 | 678 | **A louder bed can mask a line** | 7.3: the casters start outside between "Don't lose it." and "Let him play." | The casters ducked under Father's line (held envelope), the speech check rerun after the mix |

## 1. The scene file and its map

| # | Line | Lesson | Here |
|---|---|---|---|
| 97 | 710 | Lay the scene out before animating it | `da_scenes.py` holds every shot: setup, camera, cast and poses, props, lines (`da_timing_v3.json`), sounds, the robot's pile, the two spaces |
| 109 | 725 | A later entry in a drawing map silently undoes a fix | One map, shot → function; printed and asserted on every build |
| 61 | 628 | Split the set map from the camera map | Three sheets: clean set (front desk v4 + the office glass), the top-down shot plan (S1, S3–S9, S8r), blocking for 3.4 and 7.4 |
| 167 | 795 | A floor plan is not a frame | Every setup checked as a real camera frame, not on the plan |
| 108 | 721 | Check the script against the set before writing poses | `set_gate`: marks, floor lines, the same person after a cut |
| 219 | 895 | A motion test's id must not be a board shot's id | The push/pull tests keep their own ids (`9.1`, `8.1-pull`) |

## 2. Shots and cuts (the 8 floor ↔ office changes)

| # | Line | Lesson | Here |
|---|---|---|---|
| 13 | 511 | A shot list before any key poses | G2: action and reaction per beat, sizes, eyelines |
| 15 | 513 | The camera changes sides | S8 / S8r are the reverse of S7; the mirror rule (Don's side screen right in S8) checked per cut |
| 54 | 621 | The same cast on both sides of a cut | Each of the 6 office cuts: who is where, inside and out |
| 55 | 622 | Catch an entrance mid-step | 4.1 (Pam out of the door), 4.3, 6.1 |
| 148 | 767 | A change of place needs its own shot | 2.1 shows the office from outside before the first cut in |
| 185 | 821 | An arrival needs its own held picture | Father's arrival (1.3) and the 8.1 pull-back's end (held 2.5 s) |
| 24 | 528 | Push in only on the turns | Two moves only: the 8.1 pull, the 9.1 push (the loop pair) |
| 155 | 780 | What fits in the still can be cut by the camera's move | Signs and limbs checked at both ends of 8.1 and 9.1 |
| 6 | 491 | Three motivated camera changes beat uniform framing | Sizes vary by beat: W for the space, M for the action, MC for the face |
| 18 | 519 | Compose every shot for 9:16; never crop one wide set | Each setup composed, not a crop of S7 |
| 191 | 827 | Two plot threads read as two cartoons until one prop names the join | The joins on screen: the glass, Pam's mustard mug, MY GARAGES, the throne |

## 3. Beats, reactions, holds

| # | Line | Lesson | Here |
|---|---|---|---|
| 20, 101, 102 | 524, 714, 715 | A turn is an action, not a glance; cut the ambiguous face | 6.7 (Pam closes her mouth), 5.2 (the pinky), 3.4 (the feint is the body) |
| 21, 23 | 525, 527 | Every reaction is a take; it comes after the gag, with a hold | 1.2 → Don's shin; 3.4 → the hold on Mom 0.5 s before her line |
| 53 | 620 | Reactions face their target | Don faces the glass in 2.1, 5.2; Pam faces the Client in 6.6 |
| 136, 187 | 755, 823 | A turning beat is held; the reaction that carries it gets the time | 6.5–6.7 (her silence), 7.3 (Father doesn't turn) |
| 132 | 751 | A decision needs its cause and its effect in one frame | 7.3: the casters (cause, by sound) and Father not turning (effect) |
| 100, 131 | 713, 750 | The change happens on screen; a still can't carry motion | The layouts list every shot that moves (the push, the tug, the peel) |

## 4. Lines and bubbles (12 lines; 7.3 has two)

| # | Line | Lesson | Here |
|---|---|---|---|
| 217 | 893 | Two lines in turn, or a camera move, get one key frame each | 7.3 (two), 8.1 (the pull, then Pam's line), 9.1 |
| 197, 198 | 833, 834 | A long line on one frozen frame needs a cut inside it; a listener points to the speaker | 8.1's 2.5 s line on the held final image: the inside is still, so the pen moves (her act) |
| 159, 171, 215 | 784, 804, 891 | A bubble stays put while spoken; a tail is measured; reuse a measured bubble | `speech.draw` + `speech_gate`, tails 10–20 px |
| 216 | 892 | A bubble's clash list includes signs and story props | MY GARAGES, the minutes, the mug, the hands |
| 169 | 802 | Never assign a line to a speaker yourself | Every line's speaker is in the script; 3.3's Client "from the door" gets a tail into the door gap |
| 165 | 793 | Pam's remark: "Some [what the others do]. Others [what Pam does]." | 8.1 passes ("take notes" is her act, shown in 6.2); 6.2 "I took notes." is a fact, not a remark, so the rule does not apply |
| 175, 121 | 808, 737 | Typed is not spoken; a short line beside a short line fails a windowed check | 6.2 (1.2 s) next to 6.4: Whisper with context (done: 3/3) |
| 33, 79 | 568, 674 | Narration and cards at the top; the bottom belongs to the app | Bubbles above y 720 |

## 5. Props, signs, sizes

| # | Line | Lesson | Here |
|---|---|---|---|
| 25, 111 | 529, 727 | Signs read at 270 px | Only MC and inserts read (sign-size note, plan v2); REVIEW · TOMORROW in 1.3 (S1 · W) does not: an MC or drop it |
| 220 | 896 | Strips at 216 px can't carry small props | The background deal steps (3.4, 4.1, 7.2, 7.4) are judged at 270 px, not on strips |
| 78, 110, 104 | 673, 726, 717 | Every prop gets a timeline; one prop, one place, one drawing | A prop table in `da_scenes.py`: the mug(s), the cup and saucer, the minutes, MY GARAGES, the clips' pile, the roll, the strip, the tag |
| 125, 170 | 744, 803 | Protect story props; dead zones on every frame | `of_set.protect()` for every story prop |
| 38, 134 | 573, 753 | An insert must not float and needs an owner | 5.1, 6.3, 6.6 |
| 124, 98, 69, 96 | 743, 711, 654, 700 | Faces from the drawing; scale measured; one size rule | Character sizes from the series lineup |
| 126 | 745 | Look at the board under the app | Every layout under the mock overlay |

## 6. The loop

| # | Line | Lesson | Here |
|---|---|---|---|
| 57, 74 | 624, 659 | Frame 0 by the same code; end on frame 0's exact shot | Done: 9.1's last drawing is frame 0's file; S8r start = end byte for byte |
| 183, 143 | 819, 762 | A loop is a state; check the set | Script v4's loop-state table (tags, gap, last clip, roll) |
| 112, 113 | 728, 729 | Hold frame 0; the sound runs through the seam | Frame 0 held ≥ 0.4 s (9.1 settles into it); room tone and the tug's squeak through the seam |

## 7. Sound

| # | Line | Lesson | Here |
|---|---|---|---|
| 107, 41 | 720, 576 | Music is cut by the story's silences; silence is a choice | 5.1 and 6.6 "music stops"; 6.7's held silence |
| 212 | 885 | No room reverb on dialogue | Dry voices; inside lines heard from outside (none now) would be muffled, not reverbed |

## 8. Testing the layouts

| # | Line | Lesson | Here |
|---|---|---|---|
| 62 | 629 | The blocking test | 7.4 (the clip tug) as real frames, two cold viewers, before the layouts are redrawn |
| 51, 106, 188, 190 | 618, 719, 824, 826 | Cold-test the whole board; ask direct questions | Stage 5; a direct question on the two spaces ("what happens inside while…") |
| 52 | 619 | Three fixes that don't land mean cut | Per shot |
| 141 | 760 | The 0:01 joke is a gate | 1.1, 0:00.4 the shoe on the roll |
| 213, 123 | 889, 742 | A new check finds old faults; a passing check is not a working one | Every new check planted with a known failure first |

## 9. Hands (stage 3's rules carry over)

147 (766), 179 (815), 199 (835), 181 (817), 178 (814), 70 (655), 186 (822), 208 (881), 214 (890), 194 (830): one hand for the cast, the series' solved hands first, staged before drawn, three misreads change the gesture, the prop from the hands, one-piece arms, the hand picked by the person, arms counted per shoulder, a fault becomes a gate. In stage 4: `hands_lr` set up for every layout, `da_hand_gate` on every frame.
