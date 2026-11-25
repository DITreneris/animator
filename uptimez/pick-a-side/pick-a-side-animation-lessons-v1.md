# Pick a Side: lessons for the animation (stage 7), v1

UptimeZ Inc. · episode 14 · 25 Nov. CLAUDE.md rule 1: every lesson that applies to animating this episode, collected from `docs/lessons.md` (on main) before any film code is written. The numbers are the lessons' own. The shots are this episode's (script v8). The plan that uses these is [`pick-a-side-animation-plan-v1.md`](pick-a-side-animation-plan-v1.md).

## How the film is built

| # | Lesson | Here |
|---|---|---|
| 109 | A later entry in a drawing map silently undoes a fix | `ps_film.py` has one map: shot id → function. Assert it on every build, and print what changed |
| 180 | Check the delivered file, not the frames you meant to put in it | The cut reads its frames only from the current version's folder. G5 runs on the encoded mp4 |
| 122 | Delete old render frames | Keep only the current version's frame folder |
| 195 | Trim before you animate | Timing v3 (66.3 s) is the length. Any trim is decided before a scene is drawn, not after |
| 201 (last line) | Start the renders only after the sound has finished | Build the sound, read its exit code, then render |
| 236 | A bubble keeps one place relative to its speaker across a cut inside a line | `BUBBLE_AT` per camera for the split shots (2.10, 3.1, 4.3) |

## Motion and acting

| # | Lesson | Here |
|---|---|---|
| 131 | A still frame cannot carry motion | All the board's stills that move are listed in the plan's exposure sheets; the hard ones already have tests (A–K) |
| 136, 187 | A beat the story turns on is held 0.5–0.6 s; the reaction that carries the turn gets the time | The heel over the tape (2.9), COO? (5.3), Pam's hand across (5.6), the smug pause before the bump (2.11). H v4's viewers: the hit is "rushed" (2 drawings) |
| 200 | A held beat needs one visible change, on the thing held | The shots the script calls still (1.3 "he doesn't move", 2.6, 2.8, 2.9b, 3.2, 5.5) each get one visible change: a blink and lips are not enough |
| 100, 117 | The change happens on screen | The tape torn off the roll (2.1), COO? written stroke by stroke (5.3), the throne spun (2.2) |
| 101, 102 | A glance is not a turn; cut the ambiguous face | Turns go to hands and props, not eyes |
| 114 | No white impact flash | Impacts get the yellow burst (H v4) and lines. A flash only from the robot's camera (3.1) |
| 39, 89, 93 | Feet stay put in a walk; fixed from the knees down; test as silhouettes first | Sofía's crossing (5.5, `k_gait`) and any new walk |
| 178, 184 | After three misreads, change the gesture; replace a move that can't be reached, and say so | The haul in 2.11 is gone (H v4) |
| 183, 143 | A loop is a state: everything the film changes is changed back on screen | 6.2 → 1.1: the blind, the tape, Sofía's side. The loop check masks the people |
| 112, 113 | Hold frame 0 before the camera moves; the sound runs through the seam | 1.1 held ≥ 0.4 s; a fade of ≤ 0.3 s at the seam |
| 197, 198 | A long line on one frozen frame needs a cut inside it; a listener points to the speaker | 1.3, 1.4, 3.3 (2.6 s each, one frame each on the board); 3.1 and 6.1 (3.0 s) |

## Faces, mouths, hands

| # | Lesson | Here |
|---|---|---|
| 196 | A shared part drawn at a fixed size breaks at another scale | Lips at Don's 0.60 and in close-ups: check the mouth on the face at both |
| 147, 149, 199, rule 4 | One hand for the cast; reuse the series' hands | `hands_ps`, `kit.HAND`; any hand or pose change goes through `docs/rules-hands-and-phones.md` section 0 |
| 115, 116, 186 | A held sign needs arms you can follow; an arm is not a tube; every held prop gets the same arm | Sofía's CV (5.3–6.1), Pam's phone and cup |
| 128 | Wide eyes and raised brows read as fear | Smug and calm faces: heavy lids, level brows |
| Hands page §0 | The rig returns hand points without the lean or tilt | Fix it once, opt-in, before scene 2 (motion tests H and J corrected it by hand) |

## Sound (stage 8, planned now)

| # | Lesson | Here |
|---|---|---|
| 105, 230 | Check room tone with the recognizer; voices dry | Whisper per line in the final mix, three windows |
| 107, 202 | Music cut by the story's silences; check the music as a map | The sparse vibes, cut dead on the blinds, the DING and the bump |
| 202 | Every new action gets a sound, or is decided silent | Tape screech, blind clatter, flash, DING, the roll, the bump |

## Cold viewers

| # | Lesson | Here |
|---|---|---|
| 106, 190 | Ask direct questions too | The plan's eight questions (plan v1 §4) |
| 119 | Trimming finds a floor | Ask "what felt rushed or slow" |
| 139 | Stop polishing a beat when its meaning lands | I (6.1b) and J (4.2) were accepted on this basis |
| 188, 191 | What three viewers guess, the film hasn't shown; two threads need one prop that names the join | The office and Father's booth: the #TeamDon photo is the join |
