# The Double Agent: the S8 frame (the final image, 8.1), the plan v1

26 Nov, Tomas: "plan it in detail, a long session, this frame matters". The frame the episode ends on and its likely cover: **inside Don's office the meeting works on the Client's blueprint and hands it to Pam; through the glass, Don salutes at his line with his own tape stuck to his hand.** Builds on S8 v1 (`da_s8_final_v1.png`), its cold test (`da_coldtest_s8_v1.md`, 2.5 of 5) and the outside frame review (6.5/10). Lessons: [`the-double-agent-s8-lessons-v1.md`](the-double-agent-s8-lessons-v1.md).

## 1. What the frame must say (the pass mark)

Five beats, the same questions as v1's test, 3 cold viewers, **pass: every viewer 4 of 5, and beats 2 and 4 by all three**:

| # | Beat | v1 | Target |
|---|---|---|---|
| 1 | The man outside is proud, saluting, at his line | 3/3 (salute 2/3) | 3/3, salute 3/3 |
| 2 | **Inside, a meeting that works without him and ignores him** | "a judging panel" 3/3 | **"they're working / planning without him" 3/3** |
| 3 | The older man in red is in charge | 3/3 | 3/3 |
| 4 | **The dirty man gives the blue plan (his garages) to the woman in purple** | "a 1–10 scorecard" 3/3 | **"a plan / blueprint of garages, handed to her" 3/3** |
| 5 | He is losing and doesn't know; his own tape is stuck to his hand | 3/3; tape 1/3 | 3/3; tape 2/3 at full size |

Plus the review's four: the window reads as glass, not a screen; the chair as a chair; the desk as a desk; planes separated by light and shadow.

## 2. The frame, layer by layer (draw order, lesson 129)

Frame units 540 × 960, rendered at 2× (1080 × 1920). Back to front:

| # | Layer | What | Reused from | Fixes |
|---|---|---|---|---|
| L1 | **The office wall** | the office's own wall around the glass, one step darker than the floor's (`IN_WALL`) | `da_set.IN_WALL` | — |
| L2 | **The floor seen through the glass** (`_floor_through_glass` v2) | far wall (`kit.WALL`) with a skirting line; floor (`kit.FLOOR`); **the tape receding, with a gap beside Don where he peeled his strip**; **the throne's back** (`ps_set.throne_back`) on his side, behind him; **the counter's back** right outside the glass (top and back panel, the monitor's back, Mom's mug); a faint light veil (it is a brighter room) | `ps_set.throne_back`, `ps_set.TAPE`, `fs_set4.shadow` | window-or-screen (2/3); Don's scale gets depth cues |
| L3 | **Don outside** | at his line, facing the office, **eyes open, a big grin**, saluting; **the strip**: longer (about his forearm), wider, curled, stuck to his saluting palm, its end hanging; contact shadow | `don_ps.don` "salute" | the tape 1/3; curl stays (canon) |
| L4 | **The glass** | a cool tint (`#8CAAB9`, 0.12); **two reflections**: a soft diagonal and the faint reflection of the window frame; **jambs and sill with thickness** (the inner faces as trapezoids, lit on one side); **blinds**: a tidy opt-in variant for this wide glass (8 parallel slats, equal gaps, the rail, two cords) | `ps_set.blinds` (+ `TIDY` flag, default off) | blinds "like wires"; "a screen" |
| L5 | **Don's chair** | a black leather executive chair seen from the front: a rounded, tufted back with a lighter edge and a headrest, shorter than v1's slab; its shadow on the wall | new (no office chair in the repo fits; `cafe_kit.chair_back` is a café chair) | "a black hole" 3/3 |
| L6 | **The meeting** (`cafe_kit.seated`: drawn above the desk top only) | **the Client** (left), leaning over the desk, his oily finger on the plan (`client_ps.cast_client`, `hands={-1: "point"}`, `aim=` the plan: 14's booth pose); **Pam** (left-centre), seated, her hand on the plan's other edge, eyes on it; **Father** (centre, in Don's chair), leaning back, **arms folded**, eyes on the plan, the chain and stubble shadow big (lesson 135); **Sofía** (right-centre, out of the rail zone), standing, clipboard, eyes on the plan | `client_ps.cast_client`, `pm_ps.pam`, `dh_cast.father`, `sofia_ps.sofia`, `cafe_kit.seated` | "a judging panel" 3/3 |
| L7 | **The desk** | Don's desk: a visible **top plane** (lighter wood, its far edge and near edge) and a **shorter front** (about 10 % less than v1) | `cafe_kit.table` (front + top), `da_set.DESK` | "a brown wall" |
| L8 | **On the desk** | **the blueprint as garages** (`acts_ob.plan_open` with `GARAGES` and `TITLE`: "MY GARAGES", bay 7 ringed), bigger (about 1.6× v1), on the top plane between the Client's finger and Pam's hand; **Pam's mustard mug**; Don's white office mug; contact shadows under each | `acts_ob.plan_open` (`GARAGES`, `TITLE`) | "a 1–10 scorecard" 3/3; the photo removed ("a yellow stick" 3/3) |
| L9 | **Hands over props** | the Client's finger and Pam's fingers drawn again over the plan (lesson 224) | `hands_ps.redraw_at` | — |
| L10 | **The light** | the room's grade: the office darker at the top and corners, the near desk darker toward us, the glass the brightest area (a lit floor seen from a dim office) | `of_scenes.grade` (copied as a local, opt-in) | "everything equally flat" |
| L11 | **Pam's line (placeholder)** | the bubble's place reserved (not drawn yet): left of the glass top, clear of Don's head and every face (`speech.draw` with `avoid=`) | `speech.draw`, `speech_gate` | — |

## 3. The steps, with a stop after each sheet

Stills only (Tomas: no render before the .png). Each step ends with the sheet sent and a short note; the next step starts unless Tomas stops it.

| Step | Output | Check before sending |
|---|---|---|
| **A** | This plan + the lessons file | — |
| **B. The window** | `da_s8_window_v1.png`: L1–L4 with nobody inside; three blinds variants side by side (canon, tidy 8, tidy 6) | the glass reads as glass at 270 px (a still pair: v1's window vs B's) |
| **C. The furniture** | `da_s8_furniture_v1.png`: the chair (3 silhouettes), the desk top + front, the props at their size | silhouettes at 270 px: the chair named "a chair" by 2 cold viewers |
| **D. The blocking** | `da_s8_blocking_v1.png`: three layouts of the four at the desk as silhouettes (who leans, who sits, where the plan is) | 2 cold viewers: "what are they doing?" must be "working on / planning something", not "judging" |
| **E. The hands** | `da_s8_hands_v1.png`: the Client's point on the plan, Pam's grab on its edge, Father's folded arms, Don's salute with the strip; at 100 / 50 / 25 % (rules-hands §0) | named from the job table; the new rows (the strip on the palm, Father's folded arms) as comparison sheets |
| **F. The frame** | `da_s8_final_v2.png` + six crops at full size (the window frame, the plan and hands, Father, Don outside, the chair, the desk props) + the frame under the mock app overlay | faces and the plan out of the dead zones; signs whole; Don's tape visible at 540; the Don rule doesn't apply (he isn't sharing the plane) |
| **G. The cold test** | `da_coldtest_s8_v2.md`: 3 new viewers, the same 8 questions + "what is the blue paper?" + "where are we, and what is the man outside to the people inside?" | §1's pass mark |
| **H. Fixes** | `da_s8_final_v3.png` (only if G fails) | the same |

**Budget:** 3 versions of the frame (v2–v4), 3 per sheet. A misread that survives three fixes changes the gesture (178): the blueprint → the Client hands Pam the rolled blueprint (`client_ob.blueprint_roll`) across the desk; the salute → Don holds the strip up like a flag. **Stop rule:** one hour or two full rounds without the faults going down → stop and report.

## 4. Tomas's decisions (26 Nov, /grill-me)

| # | Question | Decision |
|---|---|---|
| 1 | Mom in this frame | **Not at her desk** (out of frame; nothing new drawn) |
| 2 | Father | **Leaning back, arms folded**, eyes on the plan |
| 3 | The blueprint | **"MY GARAGES" + garages, bay 7 ringed** (`acts_ob.TITLE` + `GARAGES`) |
| 4 | The far wall | **Plain, with a skirting** |
