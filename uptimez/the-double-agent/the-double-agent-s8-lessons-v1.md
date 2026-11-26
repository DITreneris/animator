# The Double Agent: lessons for the S8 frame (the final image, 8.1), v1

26 Nov. CLAUDE.md rule 1: every lesson that applies to the S8 still, collected from `docs/lessons.md` (line numbers) and `docs/rules-hands-and-phones.md` before any code. The faults they answer are from `da_coldtest_s8_v1.md` (3 viewers) and the outside frame review (6.5/10) of the same still.

## Staging: "a judging panel" (3/3)

| Line | Lesson | Here |
|---|---|---|
| 620 | **53. Reactions face their target, not the camera.** | The four at the desk face the plan, not us: heads down, eyes on the paper |
| 612 | 48. Conflict is a gesture, not a pose: two figures side by side read as a series card | Each person does one thing to the plan (points, writes, leans back, reads) |
| 714 | **101. A glance is not a turn**: give the turn to a hand and a prop | The plan moves between two hands (the Client's to Pam's), not eyes |
| 751 | **132. A decision needs its cause and its effect in one frame** | The Client's hand on the plan and Pam's hand taking it, in the same frame |
| 817 | **181. Stage the hands before you draw them** | Everyone on the desk's near side, reaching to the plan on the desk top, no reaching through each other |
| 755 | 136. A beat the story turns on gets held | The hand-over is the still's centre, the frame's largest object after the faces |

## The blueprint: "a 1–10 scorecard" (3/3)

| Line | Lesson | Here |
|---|---|---|
| 679 | **84. Cold viewers' shared misreads are cheap fixes** | Draw it as what it is: garages (`acts_ob.GARAGES`), no numbers |
| 824 | 188. What three cold viewers guess, the film hasn't shown | Three said "scorecard": the drawing says scorecard. Change the drawing, not the test |
| 753 | 134. A close-up object needs an owner | The plan in two owners' hands |
| 239 (sec.) | Small props need a silhouette | Bigger, with its paper curl, on the desk's top plane |
| 744 | 125. Protect story props, not only faces | The plan out of the dead zones (y > 720; x > 470 between y 380 and 860) |

## The window: "a window or a projection screen?" (2/3), the review's "no depth"

| Line | Lesson | Here |
|---|---|---|
| 497 (sec.) | **No real 3D camera: get depth from layers** | Jambs and a sill with thickness; the counter's back right outside; the far room behind |
| 611 | 47. A silhouette needs a lit wall behind it | Don outside stands against the light far wall |
| 958–960 | **229. The room's light: a grade over the whole frame; contact shadows** | A darker office, the floor outside lighter (a lit room seen from a dimmer one); shadows under every prop, the chair, the window frame |
| 571 | 36. Two characters must not share a silhouette (the portrait read as a person) | Nothing behind the glass that reads as a second Don |
| 884 | 211. A face in a picture is not a person | No portrait in this frame (the desk photo is out) |

## Objects: the chair "a black hole", the desk "a brown wall", the photo "a yellow stick"

| Line | Lesson | Here |
|---|---|---|
| 239 (sec.) | Small props need a silhouette | A real executive chair: rounded, tufted, a lighter edge |
| 129 (sec.) | **Fix draw order**: a desk drawn after a face cuts the eyes | Order: wall → glass world → glass → chair → people → desk top → props → hands over props |
| 726 | **110. One prop, one place** | Don's photo is on the desk at 2.2; here it is out of frame, not a stick |
| 721 | 108. Check the script against the set before writing poses | Father's feet on the desk need a seated rig the series doesn't have: here he leans back, arms folded (feet up stays in 2.2's own shot) |

## People

| Line | Lesson | Here |
|---|---|---|
| 754 | **135. Mute viewers read gender from the drawing** (Father = "the woman") | Father's stubble shadow (13's) and his chain, big |
| 747 | 128. Wide eyes and raised inner brows read as fear | Calm: heavy lids, level brows |
| 756 | **137. Sizes against the set's canon, measured** | Father 1.19 × the Client; Pam, Sofía at their canon ratios to the Client; Don outside at his line, measured against the far floor |
| 743 | 124. Faces come from the drawing | Faces checked where the rigs drew them |
| 745 | 126. Look at the board under the app | The still checked under the mock app overlay |
| 692, 818 | 88 / 182. Turned heads need a drawn three-quarter | Nobody turns their head: eyes and hands do the work |

## Hands (rules-hands §0, canon: DITreneris/uptimez)

| Job (from the table) | Who | Note |
|---|---|---|
| `point` | The Client: his oily finger on the plan | existing row |
| `grab` (or `pinch`) | Pam: her fingers on the plan's other edge | existing row; the pen behind her ear, not in hand (one object per hand) |
| `folded` arms | Father | Mom's folded pose (`pm_ps.M_POSES["folded"]`) is the model; on Father's rig: a new pose → silhouette test |
| `hold` (clipboard) | Sofía | her canon pose |
| `salute` + **the strip stuck to the palm** | Don, outside | **a new row**: the strip as one object on the palm, drawn over the hand (lesson 224: draw the hand again over the object) |
| | | 814: **178. three misreads: change the gesture** · 817: 181 · 832: 196 (a shared part at a fixed size breaks at another scale: check the hands at Don's 0.34 outside) |

## Process

| Line | Lesson | Here |
|---|---|---|
| CLAUDE.md rule 2 | Reuse what was approved; name the file | `cafe_kit.seated` (people above the table top), `cafe_kit.table` (front panel + top), `of_scenes.grade` (the light), `ps_set.throne_back`, `acts_ob.plan_open` + `GARAGES`, `fs_set4.shadow`, `ps_set.blinds` (+ a tidy opt-in variant) |
| CLAUDE.md rule 3 | Look before sending: six frames at full size with crops | The still and six crops: the window frame, the plan and hands, Father, Don outside, the chair, the desk props |
| CLAUDE.md rule 5 | Stop when it isn't converging | One hour or two full check runs without the faults going down: stop and report |
| 1092 (244) | Section 0 under time pressure; a storyboard before a render | The still is the storyboard: stills only, no video |
