# Approved.: the hand jobs, v1 (stage 1, rules §0 step 0)

28 Nov. Every hand in script v1, its job and its row in the canon table (DITreneris/uptimez `docs/rules-hands-and-phones.md` "Jobs", PR #12 for §0 step 0). This table is written before any hand is drawn. From stage 4, each shot's scene code declares these rows to the hand gate (E15's `src/da_hand_gate.py` pattern), and the gate fails a hand that is not on its shot's list. Misreads are counted, and 3 changes the gesture.

**Drawn in** E15's hand library v4 (`src/hand_lib_v4.py`, sandbox, one closed outline per hand) through `hands_lr` for left and right. The robot keeps its locked gripper and rest. **New:** a `point` pose for the library (H5, H6); every other row reuses a cold-tested pose.

## Story jobs (plan §5)

| # | Shot | Who | Job | Row / library pose | State |
|---|---|---|---|---|---|
| H1 | 1.2 | Don | raises the empty cup straight up, on his back | `handle_grip` = CUP_GRIP | Reuse (v3, 2/2). Catch the arm already up |
| H2 | 1.5 | Client | the washer under the chair leg; the other hand lifts the leg | `pinch` = PINCH + `clutch` = CLUTCH | Reuse (v4, 2/2 each) |
| H3 | 3.7 | Client | catches the mug without looking, **by the handle** | `handle_grip` = CUP_GRIP | Reuse. Never `grab` round the mug's body (0/2) |
| H4 | 5.3 | robot → Father | the invoice across a clear gap | gripper → Father's tag `pinch` (sheet v6 `redraw_at`) | Reuse. A gap, or it reads as a handshake |
| H5 | 6.2 | Father | finger reaches toward the screen and stops, clearly apart | `point` (`point_t` if large) | **New library pose.** Measure the gap at feed size |
| H6 | 3.4, 6.5–6.7 | Don | press without looking; later the hover, freeze, pull back | `point`, fingertip | **New library pose** (as H5): one job, two states |

## Every hand, shot by shot

| Shot | Who | Hand | Job | Row |
|---|---|---|---|---|
| 1.1 | Don | both | asleep: L on the armrest, R hanging | `clutch` / `quiet` (S8r v4, locked) |
| 1.1 | robot | front | pulls the card | gripper |
| 1.2 | Don | one | the cup raised (H1) | `handle_grip` |
| 1.2 | Don | other | flat on the floor | `quiet` |
| 1.3 | Pam | both | the blueprint open; turns a page | `board_two` → `pinch` (the page corner) |
| 1.4 | Father | both | unfolds the folding chair | `grab` ×2 (on its frame: narrower than the fist) |
| 1.4 | Don | one | the cup still up | `handle_grip` |
| 1.5 | Father | one | on the chair's back as it wobbles | `clutch` (an edge) |
| 1.5 | Client | both | washer and leg (H2) | `pinch` + `clutch` |
| 1.6 | Father | both | seated, on his knees | `quiet` (sheet v6 `seated_rest`) |
| 1.7 | Father | ringed hand | turns the tag | `pinch` (the tag pinch) |
| 2.1 | Sofía | both | sitting: on the armrests | `quiet` |
| 2.1 | Don | both | scrambling up, pushing off the floor | `palm` ×2 |
| 2.2 | Sofía | one | smooths her skirt | `palm` |
| 2.3 | robot | front | holds the report out, then retracts it | gripper |
| 2.3 | Father | one | raised palm: "stop" | `palm` (lib PALM 2/2 "stop") |
| 2.5 | Sofía | both | unpins the card; pins it; checks it | `pinch` ×2 → `pinch` |
| 2.5 | Sofía | one | points to the corner | `point` (level, from a gap) |
| 2.7 | robot | front | the report in its gripper | gripper |
| 3.1 | Don | both | at his sides, walking | `quiet` |
| 3.2 | Don | one | the filter in upside down | `grab` (the filter basket's handle: `handle_grip` if it shows) |
| 3.4 | Don | one | the blind jab (H6, state 1) | `point` |
| 3.7 | Client | one | the mug catch (H3) | `handle_grip` |
| 3.8 | — | — | the spoon stands by itself (no hand) | — |
| 3.9 | Don | one | carries the cup; sets it on the armrest | `handle_grip` |
| 4.1 | Father | one | props the name card | `pinch` |
| 4.2 | Client | one | the mug still held, lying flat | `handle_grip` |
| 4.2 | Father | both | hands on his knees, leaning | `quiet` |
| 4.3 | Don | both | looks at his own hands: palms up at his waist | `palm` ×2 (**a gesture to test**: palms up at the waist, three silhouettes, two viewers; rules §0.2) |
| 4.4 | Pam | both | the blueprint lowered | `board_two` |
| 5.2 | Don | both | stepping back from the paper | `quiet` |
| 5.3 | robot → Father | — | the invoice (H4) | gripper → `pinch` |
| 5.5 | Father | one, then both | pockets the invoice; holds the report | `pinch` → `clutch` (the report's edge) |
| 5.7 | Don | both | at his sides (no chin on a fist: the chin-slip is parked for E17) | `quiet` |
| 5.9 | Father | both | straightening: on his knees | `quiet` |
| 5.10 | Don | one | **tilts the throne's back to show it reclines** (script v3) | `clutch` (the back's top edge) |
| 5.11 | Father | both | the card in one, the report in the other | `pinch` / `clutch` |
| 6.1 | robot | both | seated: on the armrests | rest |
| 6.2 | Father | one | the reaching finger (H5) | `point` |
| 6.5–6.6 | Don | one | the hover (H6, state 2) | `point` |
| 6.7 | Don | both | **fists on his hips, elbows out** (no crossed forearms) | `fist` ×2 |
| 6.8 | Sofía | one | adjusts the HR card | `pinch` |
| 6.9 | robot | both | pushes up from the armrests | gripper ×2 |
| 6.10 | Father | ringed hand, then both | turns the tag; folds the chair | `pinch` → `grab` ×2 |
| 7.1 | Don | both | unhooks and folds the tag; wedges it | `pinch` ×2 |
| 7.1 | Don | both | then L on the armrest, R hanging | `clutch` / `quiet` (= 1.1) |
| 7.2 | robot | front | reaches for the card | gripper (= 1.1) |

## New gestures (rules §0.2: three silhouettes at 270 px, two cold viewers, then a row)

1. **`point` in the library** (H5, H6): one pose, the canon function as the fallback.
2. **Palms up at the waist, looking down at them** (4.3, Don): not in the table. If it misreads, the fallback is **Don's eyes going down to his hands hanging at his sides** (`quiet`, no new gesture).

## Count

47 entries (46 with a hand; +1 in script v3, 5.10; the spoon in 3.8 has none): 41 reuse a cold-tested row or a locked drawing, 4 use the new `point` pose (3.4, 6.2, 6.5–6.6, and Sofía's 2.5 point, which can fall back to the canon `point`), and 1 gesture is to be tested (4.3).
