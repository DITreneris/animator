# The Double Agent: the hand jobs, v1 (stage 3.6, step 0.1)

27 Nov. Every hand in script v4, its job and the row of the canon table (DITreneris/uptimez
`docs/rules-hands-and-phones.md` "Jobs", read at 566aeb8). Written before any hand is drawn; each shot's scene code
declares these rows to `src/da_hand_gate.py` (`jobs()`), and the gate fails a hand that is not on its shot's list.
A job with no row is a new gesture: three silhouettes, two cold viewers, then a row (rules §0.2). **One job here had no
row: 5.2.** The silhouette tests (27 Nov, `src/da_sil_saucer.py`, two fresh viewers each, neutral prompts):
- **Drinking from the saucer** (`da_sil_saucer_v3.png`): 0 of 2. Front on, the saucer vanishes into the face; the
  raised hand read as "hmm", a wave, a phone call; the cup as a blob or keys. (A third viewer was primed by my prompt:
  set aside; even so, no saucer.) Tomas: change the gesture, "pinky on the cup".
- **The cup, the little finger out** (`da_sil_cup_v1.png`): A 2/2 "sipping tea or coffee"; **B 2/2 sipping, one
  viewer: "a bit posh and fussy, like a proper tea party, maybe a little showy"**: the meant read; C 0/2 (the cup low
  by his chest read as a box or a phone on a tray). Kept: **B**. Neither viewer named the finger itself: its lift is
  the beat, so it is checked in motion (a 10 fps strip, rules 0.6), not on a still. Misreads: the saucer sip 1 (dropped).
- **The cup v2** (outside audit of the cup sheet, "tobulinam": `src/da_hands.py`, `da_sil_cup_v2_review.png`; the
  gate passes both): B 2/2 "drinking from a mug, the other hand holds a flat thing out"; one viewer, unprompted: "a bit
  dainty and posh, like a fancy tea party ... a pinky-up, refined sip". **Both viewers, the same two doubts** (a
  staging fault, not a viewer fault): the hand at the handle reads as a pen, a stick, a crooked finger (the pinch, the
  handle and the little finger merge in silhouette); the saucer as a tray, a pan, a flat phone. In colour both read
  (the china, the coffee, the C handle); in the shot they come with the rattle and the slop on the saucer.
- The row for the canon table (proposed to DITreneris/uptimez only when Tomas asks): *A sip with manners: the cup
  in `pinch` at the cheek, held out past the head's outline, the little finger out; the saucer on a `grab` held out
  low on the other side.*

| Shot | Who | Hand | Job | Canon row |
|---|---|---|---|---|
| 1.1 | Don | L / R | the armrest / hanging | `clutch` / `quiet` (**locked**, S8r v4) |
| 1.1 | robot | front / back | the arm post / hanging | gripper / rest (**locked**) |
| 1.2 | Don | the hand he lets go with | flung open by the whack | `palm` |
| 1.3 | Father | ringed hand | hangs REVIEW · TOMORROW by its string | `pinch` (Father sheet v6: the tag pinch, `redraw_at`) |
| 1.3 | robot | front | lets go of the throne | gripper → rest |
| 1.4 | Sofía | both | the folder and the clear box | `board_two` (her sheet v4 carry) |
| 1.5 | Don | one | pulls the roll off his sole | `grab` |
| 2.1 | robot | front | picks up a clip | gripper |
| 2.2 | Father | both | on the armrests, seated | `quiet` (sheet v6 `seated_rest`) |
| 2.3 | Don | both | straightens his vest by its hem | `clutch` ×2 (an edge) |
| 2.4 | Don | one or two | presents the mustard mug | `grab` |
| 2.4 | Pam | both | the blue mug, then lets go | `grab` → `palm` |
| 3.1 | Don | one | raised, without turning | `palm` |
| 3.2 | Pam | both | the thermos; the mug | `grab` ×2 |
| 3.3 | Pam | both | the mug; the cup and saucer | `grab` ×2 |
| 3.3 | Client | one (oily) | takes her mug at the door | `grab` |
| 3.4 | Mom | one | knits while her body blocks: the needle held like a pen | `pinch` (the needle); her knitting from `mom_fs.knitting` |
| 3.5 | Pam | both | holds the white mug; wipes it with a cloth | `grab` ×2 |
| 4.1 | Pam → Don | one each | the cup and saucer handed over | `grab` |
| 4.2 | Don | one | the cup at his lips | `pinch` (the handle) |
| 4.2 | Pam | one | her notepad | `clutch` (an edge) |
| 5.2 | Don | both | **sips from the cup, little finger out; the saucer held out in the other hand** (Tomas 27 Nov; the saucer sip read 0/2) | **NEW row, tested:** `pinch` on the cup's handle + the little finger out; the saucer on a `grab` (`da_sil_saucer.py cup`, variant B) |
| 5.3 | Don | both | windmilling at his line | `palm` ×2 |
| 5.4 | Mom | both | **hands on hips** (Tomas 27 Nov; the script's "arms folded" is a canon fault: crossed forearms) | `fist` ×2 on the hips: `mom_fs` pose "fists" (elbows out), not `pm_ps.mom`'s legacy `tuck`/`relax_s` |
| 5.4 | robot | front | frozen with a clip | gripper |
| 6.1–6.2 | Pam | one | the minutes held out | `clutch` |
| 6.6 | Client | both | the rolled blueprint | `grab` ×2 |
| 6.8 | Don | one | pulls his headset mic to his mouth | `pinch` |
| 7.1 | Don | one | peels the strip up | `pinch` |
| 7.2 | Don | both | the strip held high | `pinch` ×2 |
| 7.3 | Client | one | slides the blueprint across | `palm` (flat on it) |
| 7.3 | Pam | both | takes it | `board_two` |
| 7.4 | Don | both | dives, grabs an armrest | `clutch` |
| 7.4 | robot | front | over the clip, then on the throne | gripper |
| 8.1 | all | — | locked (`da_s8_final_v7.png`) | — |
| 9.1 | — | — | ends on S8r v4 | — |

**Misreads carried** (`da_s8r.MISREADS`, the gate fails a job at 3): Don's armrest `clutch` 2, Don's hanging `fist` 2
(replaced by `quiet`), the robot's gripper 2.

**A gap in the canon:** rules §0.5 names `bp_draw_audit.py --hands` (and `--grips` on 16:9) as the check that reads
the picture. Neither exists on uptimez main or animator main (searched 27 Nov). `src/da_hand_gate.py` is this episode's
check (box rules + `SEEN`, which reads the finished frame). Propose it to the canon when Tomas asks.

## The hand library (sandbox, locked v3, Tomas 27 Nov: "library v3 tvirtinam")

After the outside audit of the cup sheets (the hands built of separate strokes: "tentacles stuck to the wrist"), and
Tomas: not the canon until it is fixed. `src/hand_lib_v3.py` (one closed outline per hand: the wrist, the back of the
hand, the knuckle line, tapering fingers, the thumb from the heel of the palm; left and right mirrored; contact points)
and `src/hand_lib_sheet_v3.py` (`hand_lib_v3_sheet.png`; `check`: PIECES, WRIST, CONTACT, MIRROR on the picture, each
first caught on its planted fault). Three poses: RELAXED, CUP_GRIP, SAUCER_SUPPORT. v1 and v2 kept as history.

| Round | Cold viewers (2 fresh each, neutral prompt, silhouettes) |
|---|---|
| v1 | rest read; cup read, the little finger "a tongue, a spoon, a blade"; the saucer hand "a wing, a fish, a paddle", 0/2 |
| v2 | all three actions 2/2; the mug "perched on the knuckles", the finger "a hitchhiker's thumb, a spike"; plate and hand one shape |
| v3 | **all three actions 2/2** ("an arm at rest", "holds a mug by its handle", "palm up under a plate, like a waiter"); left: fingers splay ("flame, claw"), the saucer's gap too wide (it floats), the rest hand a mitten |

Locked as it is; what is left is judged in colour in the shot and in motion (5.2, a 10 fps strip). The canon gets the
library only when Tomas asks.

## Against the canon's hands (checked 27 Nov, DITreneris/uptimez main bbf4cbb; Tomas: "taip darome")

- **Left and right: `hands_lr`.** PR #11 keeps `da_arms.setup()` for the frames locked with it (S8r v4, S8 v7) and
  sends everything drawn after to the canon's `hands_lr`. `src/hands_lr.py` is a verbatim copy (md5 616a285c…, the
  same as the canon's). `hand_lib_v3.draw_lr()` takes the thumb's side from `hands_lr.side()` and logs each hand for
  `hands_lr.check()`; `da_s52.py` runs `hands_lr.setup()` and the check (clean). `da_hand_gate` THUMB uses
  `hands_lr.check()` when it is set up, `da_arms` only for the locked frames; new plant `lr_old` (hands_lr in its old
  mode, a level mirror pair) fails "two right hands".
- **Rows, in the canon's names.** CUP_GRIP is a candidate for `handle_grip` ("Handle (lamp, tool)"); RELAXED for
  `quiet`; SAUCER_SUPPORT a new row (a flat thing on one palm: none in the table). The comparison sheets in the canon's
  format (`CANON.md` "Changing a row", step 2): `src/hand_lib_compare_v3.py` -> `compare_handle_grip_canon_vs_lib3.png`,
  `compare_quiet_canon_vs_lib3.png`, `compare_saucer_support_canon_vs_lib3.png` (old | new, male 17 / female 15, left |
  right, 100 / 50 / 25 %, silhouette). They go to the canon after episode 15 (Tomas, /grill-me), through its process
  (`DRAWERS` / `ACCEPTED` in `bp_hand_sheet_v4.py`, two attempts per row: the library's three rounds were the sandbox).
- **"An episode does not get its own hands file."** `src/da_hands.py` is marked SUPERSEDED (kept only so the 5.2
  silhouette tests rebuild); `da_s8r.clutch_v4` is recorded as an exception inside the locked S8r v4.

## Hand library v4 and the episode hand sheet (27 Nov, Tomas "darom 1-2")

`src/hand_lib_v4.py` keeps v3's three poses as they were and adds one per canon row, the same construction:
GRAB, CLUTCH (front view: the back of the hand on a bar, the fingers over its face, the thumb behind: the canon's
clutch as one outline), PINCH, PALM, FIST. `src/hand_lib_sheet_v4.py` (`hand_lib_v4_sheet.png`; `check`: all eight pass
PIECES, WRIST, CONTACT, MIRROR; hands_lr clean). Cold viewers, two fresh each, silhouettes, neutral prompt:

| Pose | Round 1 | Round 2 (the canon's limit: two attempts) |
|---|---|---|
| CLUTCH | 2/2 "a fist gripping a bar", "a believable overhand grip" | — |
| PALM | 2/2 "waving hi, stop" | — |
| FIST | 2/2 "a relaxed fist at the side" (one: "or a boot") | — |
| GRAB | 0/2 "a hammer, a dumbbell" (the mug's body as wide as the fist, one black block) | 2/2 "a fist round a pole" (a thermos narrower than the fist, the knuckles past its edge); both: no fingers to see |
| PINCH | 2/2 "dangling a tag"; the hand "a mitten, a duck's bill" | 2/2 "dangling a box on a string"; the string from the fingertip, no pinch seen |

**The episode hand sheet** `src/da_hand_sheet.py` -> `da_hand_sheet_v1.png` (28 jobs of script v4, each with its prop
from `da_props.py`, the cast's hand sizes, male 17 / female 15) and `_feed.png`; hands_lr clean. Looked at full size:
fixed there, the knitting drawn under Mom's fingers (it was over them) and clear of her hand (half covered, DON read
"ON"); the minutes held by their corner (the hand covered AGENDA).
