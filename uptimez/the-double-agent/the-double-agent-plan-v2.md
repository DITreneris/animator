# The Double Agent: the production plan, v2 (stages 3–12)

UptimeZ Inc. · episode 15 · *Civil War* 3 of 5 · 26 Nov · for Tomas's decision. Follows plan v1 (its §1–§3 lessons still hold, its §6 decisions stand) and [`series/production-process.md`](../series/production-process.md). Starts from **script v3** (amended, 34 shots, 11 lines) and **voices v1** (`src/da_voices.py`, 44 takes, picks, `da_timing_v1.json`, 65.4 s). **Character canon:** DITreneris/uptimez `CANON.md` → `characters/README.md` (read 26 Nov at 8ae83f2).

## Status

| Stage | State |
|---|---|
| 1 Script | **v4** (`the-double-agent-script-v4.md`): 35 shots, 11 lines, ~65.2 s (~68.2 s with the voices); 2.4 the gift; 5.2 changed 27 Nov to the cup sip, little finger out (the saucer sip read 0/2 in silhouette) |
| 2 Voices | v2 against script v4 (`src/da_voices.py`, `da_timing_v2.json`); Whisper word-for-word; the Client's "Don't lose it." allowed by name |
| Sheets | Father v6, the Civil War line-up v4, Don (episode) v2, Pam (episode) v3 with the canon's rose lips, no brooch; Sofía's interview look v4 (`sofia_da.py`). Canon proposals in `canon-proposal/`, not sent |
| S8 (8.1) | **Locked v7** (`da_s8.py frame7`, `da_s8_final_v7.png`, md5 53a1ac37…; local tags s8-v5, s8-v7) |
| S8r (1.1, 9.1 end) | **Locked v4, 27 Nov** (`da_s8r.py`, `da_s8r_frame0_v4.png`, md5 851120fe…, loop seam PASS) |
| Hands | **The gate** `src/da_hand_gate.py` (13 rules incl. SEEN on the frame and THUMB by `hands_lr`; 10 planted faults fail, S8r v4 passes). **The job list** `the-double-agent-hand-jobs-v1.md` (every hand of script v4, its canon row). **Hand library v3 locked** (sandbox, `src/hand_lib_v3.py`; 3 poses; to the canon after 15). **`hands_lr`** copied from the canon (PR #11) for all new drawing. **5.2 still** (`da_s52.py`, gate and hands_lr clean) |
| 3 Look and set | 3.1 S8r ✔, 3.3 the loop state ✔, 3.6 job list ✔ + library v4 ✔ + **the hand sheet ✔** (`da_hand_sheet_v1.png`, 28 jobs), **3.4 props ✔** (`da_props_v1.png`, `src/da_props.py`); **left: 3.2 the 9.1 push strip** |
| 4–12 | Not started. Per plan v1 §6.2: **in parallel up to the board; animation only after 14's master** |

## 1. The cast against the character canon (re-analysed 26 Nov, canon main 47fd6d3)

**Where the canon is.** Two places, both in DITreneris/uptimez: `characters/` (episode looks, the old team line-up) and **`the-blueprint/sheets/bp_sheet_*.png`**, the newest office sheets (Don, Pam, Mom, Sofía, the Client, the robot, each against a DON 0.60 mark). Their scales are exactly **front desk v4's `fs_set4.HOME`** (Don 0.60, Pam 0.50, Mom 0.50, Sofía 0.47, the Client 0.52, the robot 0.48), so the 9:16 set and the canon agree. Comparison: `da_cast_vs_canon_v1.png` (the canon above, the episode's rigs below at HOME scales on one floor line).

**Measured** (ink height and width against Don's, same floor line):

| Who | Canon sheet (16:9) | Episode rig | Rig h / Don | Look check | Verdict |
|---|---|---|---|---|---|
| **Don** | `bp_sheet_don` 0.60: open navy vest, white shirt with ketchup, khakis, headset, curl | `don_ps.don` | 1.00 | Same look | **OK**. Tallest of the cast except the Client (below) |
| **Pam** | `bp_sheet_pam` 0.50: purple cardigan, flower brooch, glasses, beige trousers, white shoes (16:9 adds a small nose: that film only) | `pm_ps.pam` | 0.72 (canon 0.72) | Same look. **Her rig's mug is the blue mug of 12–14** | **OK, one conflict:** the mustard mug decided for 15 changes her mug. Blue is also the Client's colour (the blueprint is "the only blue paper in the show"), so mustard keeps the two apart; continuity says a new day, a new mug. Decision below |
| **Mom** | **`bp_sheet_mom` 0.50: the office look exists** (teal jacket, gold lapels, brooch, grey curls, the curler, glasses, teal skirt) | `pm_ps.mom` | 0.83 (canon 0.83) | Same look; the jacket's square shoulders carry 3.4's wall | **OK.** (Plan v2's first draft said Mom had no office sheet: wrong, it is in `the-blueprint/sheets`) |
| **Sofía** | `bp_sheet_sofia` 0.47: pink dress, blonde high ponytail, gold earrings, clipboard | `sofia_ps.sofia` | 0.67 (canon 0.72) | **Different look:** 14's (12's cream power suit, low bun, gold shield earrings, gold-heel stilettos) | **Partial:** 14's costume, not the office canon. Right if 15 is the same war day as 14. Decision below |
| **The Client** | `bp_sheet_client` 0.52: office look (green jacket, white shirt), drawn at **1.03 of Don's height**, plus a small QUIET variant | `client_ps.client` (garage overalls, oily handprints, red rag: `client-of-v2`) | **1.03, width 1.65** | Garage look (he comes from the garage in 13–14) | **Fails the canon's own rule** (Don tallest and widest). Known since 13 (111% / 152%); the canon sheet repeats it. Staging rule below |
| **Father** | **None anywhere** (only a figure in `client-of-v2`'s scale row) | `dh_cast.father` at 0.52 × 1.19 (as `da_set`) | 0.98, width 0.96 | Burgundy coat, black, grey hair | **Gap:** the only person in 15 with no sheet. Under Don by 2%: reads as "a threatening version of Don" (bible) |
| **The robot** | `bp_sheet_robot` 0.48: HR badge, bow tie, antenna, remote up | `robot_ps.robot` | 0.65 (canon 0.65) | Same | **OK.** The pincer and a clip are new (hand sheet: the robot's gripper row exists) |

**What correlates:** (1) the 9:16 rigs already match the canon's scales and looks where a canon sheet exists; (2) the two real problems are **people the canon never settled**: Father (no sheet) and the Client's size (the canon itself breaks the Don rule); (3) two **episode-continuity** choices are open: Pam's mug colour and Sofía's costume.

**Staging rule (the Client's size):** in any frame with Don, the Client stands on a further floor line (feet higher) or is cut to a hand or arm (3.3, the door). 8.1 (S8) passes: Don is behind the glass at 0.36. The proportions check in `uz_check` names this exception per shot, never silenced in general.

**Sheets to make in stage 3** (animator `src/da_sheets.py`, with the film's own rigs; proposed to the canon repo only when Tomas asks: this session can read it, not push):

| Sheet | Why |
|---|---|
| **`father-v1-sheet`** (required) | No canon at all: turnaround at series scale beside Don, faces (calm, the nod, hard), the poses of 15 (the walk over the tape, hanging the tag, seated in Don's chair, a foot on the desk) |
| **`lineup-civil-war-v1`** (required) | The canon line-up shows Don, Pam, Rush and Max; the Civil War cast has none. From `da_cast_vs_canon_v1.png`, with the measured ratios and the Client's exception written on it |
| `don-da-v1` (episode faces) | Cold test F1 (Don read as a robot 0/3): offended, the little finger, suspicion → delight, the whisper, "Approved.", the dive |
| `pam-da-v1` (props and beats) | The mug (whichever colour is decided), the closed mouth, the duck, the plan grip |
| Props rows only | Mom's knitting; Sofía's paperclip box; the robot's crouch, pick and freeze |

## 2. Stage 3: look and set

Everything opt-in (a flag or a keyword whose default draws as before). After each shared-module change: episodes 9–14, the establishing frame and the S8 lock rebuild **md5-identical**.

| # | Piece | Built from (reuse first, CLAUDE.md rule 2) | Pass |
|---|---|---|---|
| 3.1 | **S8r, the floor seen from the office side** (new background, decided at stop 1): the tape line, the throne seen **from behind** (the tags hang on its front), Mom's desk, the counter backs, the street door far left; the glass's jambs out of frame | `da_s8.far_room` scaled to full frame; `ps_set.room` pieces; front desk v4 marks | Props on their marks (`set_gate`); the camera that 9.1 pushes into and 1.1 starts from; frame 0 held 0.4 s; signs whole or out |
| 3.2 | The push 9.1 (S8 → S8r): the blinds' rail and the glass's sheen sliding off, the far room handing over to S8r | `da_s8.glass`, `blinds_tidy` | A 10 fps strip; the seam into 1.1 by the same code (lesson 57) |
| 3.3 | **The loop state** (script v3 table): tags out of sight, the gap and the last clip under the seat, the roll behind Don's back foot | — | md5 of 9.1's last frame against 1.1's frame 0 at 540 |
| 3.4 | Props: Pam's mustard mug; Don's cup and saucer; Don's white office mug (the oily print); the gold desk photo DON · CEO; the robot's minutes AGENDA: WITHOUT HIM; the blueprint MY GARAGES (rolled and flat); REVIEW · TOMORROW tag; the peeled strip; Sofía's folder and the clear paperclip box; the clips (pile, single, in the pincer); Mom's knitting | `da_set.pam_mug`; `acts_ob.plan_open` (GARAGES + TITLE); 13's `of_ui` printout; 14's tag; `dh_props.ceo_chair` | Every sign reads at 270 px; one prop, one silhouette (lesson 110); every story prop declared with `of_set.protect()` |
| 3.5 | The sheets of §1 (Father and the line-up first) | The rigs listed in §1 | Faces read at phone size; the Don rule on every sheet |
| 3.6 | **The hand sheet** (rules-hands §0) for this episode's jobs, named from the job table; jobs not in the table get a row and a comparison sheet first | `hands_v4.enable()` (grab, pinch, fist from the canon sheet; no phone in this film) | Section 0 followed and listed in the reply; measured gaps at feed size |

**The hand jobs in script v3 (14):** Father hangs the tag (1.3); Sofía carries the box (1.4); the Client takes the mug at the door (3.3); Mom knits with one hand (3.4); Pam wipes the mug (3.5); the cup and saucer handed over (4.1); the saucer sip with the little finger (5.2); the minutes handed over (6.1–6.2); the mic pulled to the mouth (6.8); the tape peeled (7.1); the strip held high (7.2); the blueprint slid and taken with both hands (7.3); Don's grab on the armrest (7.4, 8.1); the robot's pincer on a clip (1.4–7.4). **New rows likely:** knitting, the saucer sip, the mic, the pincer.

## 3. Stage 4: the scene file and the layouts (Tomas's stop 3; budget 3)

| Step | What | Pass |
|---|---|---|
| 4.1 | **Collect the lessons** (CLAUDE.md rule 1): `the-double-agent-lessons-v1.md` with line numbers from `docs/lessons.md`, from plan v1 §3 plus the new beats (the clip tug, two bubbles in 7.3, the J-cut, the pinky, the knitting) | Sent before building |
| 4.2 | `src/da_scenes.py` modelled on `ps_scenes.py`: every shot with its setup, camera, cast and poses, props, lines (from `da_timing_v1.json`), sounds, the robot's b-business per shot (pile size, frozen or working), and the inside/outside timing for every S7 shot | Generates the script; the drawing map printed and asserted (lesson 109) |
| 4.3 | Generated: **a layout sheet per act**, the **top-down shot plan**, **blocking sheets for 3.4 (the wall and the feint) and 7.4 (the clip tug)** | G2: action and reaction per beat, sizes, eyelines; every turn an action |
| 4.4 | Checks on every layout frame: `uz_check` (scale, signs, tails, limbs, text, zones), `set_gate`, `speech_gate` (11 bubbles; 7.3 has two in 3.4 s, each ≥ 1.5 s, neither over the plan or the hands), the Don rule (the Client's exception named per shot) | All pass, no silenced check |
| 4.5 | **The blocking test** (lesson 62): the hardest shot (7.4) as real camera frames, two cold viewers, before the layouts are redrawn | 2 of 2 read: "the robot wants the clip, the man wants the chair" |

## 4. Stage 5: the board and the story test (hard gate)

| Step | What | Pass |
|---|---|---|
| 5.1 | One key frame per shot and per line (lesson 217), at 540, under the mock app overlay | G3 |
| 5.2 | **Whole-board cold test** (skill: cold-viewer-mute-test): 3 fresh viewers, two sheets at ~400 px tiles plus one at phone size, the open prompt, the story chain (script v3, 10 points) and the 10 direct questions, the loop question | Every viewer 8 of 10 chain points; two viewers making the same mistake is a staging fault. **No animation before this passes** (plan v1 §1, the lesson of 14) |
| 5.3 | One outside review on the board (G6's last round but one), triaged | OK / partial / fail table; what correlates |

## 5. Stage 6: motion tests (budget 3 each)

At film rate, 540, 8 fps strips, two cold viewers each; a beat that fails three fixes is cut and its thread carried by another shot (lesson 52).

| Test | Moment | Must read on mute |
|---|---|---|
| **A (first)** | 1.1–1.2 the roll on the shoe, the whack | A joke by 0:01 |
| B | 3.4 the wall, the feint, Mom knitting on | She blocks without effort; he is beaten |
| C | 5.2 the saucer sip and the little finger | Hurt, then fake dignity |
| D | 5.3 the stop at his own line | He can't cross his own line |
| E | 7.1–7.2 the peel, the barrier, Pam ducking, "Approved." | He lets her in, proud |
| **F** | 7.4 the clip under the caster, the two pulls | Each pulls for something else |
| G | 9.1 → 1.1 the push and the seam | The end is the start |

## 6. Stages 7–12

| Stage | What | Pass | Stop / budget |
|---|---|---|---|
| 7 Animation | `src/da_film.py` modelled on `ps_film.py`; native 1080 (2×), 15 drawings/s acting, 30 fps camera; scene by scene; stills to Tomas before any changed render (lesson 244) | `uz_check` on every frame; before/after strip per change | after 14's master |
| 8 Rough cut | The 11 takes, effects (script v3's sound column), room tone (the office muffled through the glass, the J-cut in 7.3), music cut by the story's silences (5.1, 6.6) | **G5** in full (Whisper per line in the mix, −14 to −16 LUFS, ≤ −1 dBTP, the seam); **G4** with 3 viewers and "what felt rushed or slow" | **Stop 4**; 4 |
| 9 Polish | Numbered fix lists | Every fix seen in the render; every instance checked (lesson 56) | 5 film versions, then frozen |
| 10 Reviews | Triage tables | G6, the last round | — |
| 11 Master and cover | 1080 master (not committed), 540 copy, the cover from the S8 lock | G5 on the final AAC; a clean-checkout rebuild; the cover at 120 px | **Stop 5** |
| 12 Close | `the-double-agent-film-v1.md` as built; lessons; README, INDEX, STORYLINE v3.5 row for 15 (as built) and the note for 16 (the robot's badge, the tear); the sheets proposed for the canon repo | — | commit, push and PR when Tomas asks |

## 7. Risks and fallbacks

| Risk | Fallback |
|---|---|
| The paperclips pull the eye in the S7 wides | Fewer, larger clips; the robot only in the shots that need it (1.4, 2.1, 5.4, 7.2, 7.4) |
| The clip under the caster doesn't read (motion test F, three fails) | An insert: the clip under the caster, 0.6 s, before Don's dive |
| 7.3's two bubbles crowd the plan | "Let him play." moves to the start of 7.4, off-screen, as a quoted card with Father's name |
| The Client's size beside Don | He stays inside the office in every shot with Don on the floor; at the door only his arm |
| Length past 66 s | The trims: 4.3 into 4.2, 6.2 into 6.1 (about 2.4 s) |
| Mom still reads "rules" in the mix | The take with a stop after "rule" (A) is picked; recheck word by word in the final mix |

## 8. Decisions for Tomas (multiple choice when asked)

**Closed (26–27 Nov):** Pam's mug mustard, the old blue one shatters (2.4); Sofía in a new interview suit; Mom's
5.4 hands on hips (the script's folded arms are a canon fault); 5.2 the cup sip, little finger out; the hand library
goes to the canon after episode 15, through its row process; no nose for Sofía (her sheet v4 as it is).
**For stage 4's layouts (from the props sheet, 27 Nov):** a sign's capitals at 270 px are about 2-4 px in a wide shot
(z 0.9 x the cast's 0.6), 6-10 px in a medium close, 12-20 px in an insert. Only MC and inserts read: REVIEW · TOMORROW
in 1.3 (S1 · W) cannot be read there; it must be framed closer, or the shot must not need it read.
**Still open:** Pam's calm lid as her default (canon tg-v2)? The Client's look in 15: the office (`client_ob`) or the
garage coveralls (`client-of-v2`)?

Asked in v2:

1. **The new sheets:** Father and the Civil War line-up (required), plus Don's and Pam's episode sheets, or only the two required?
2. **Pam's mug in 15:** mustard (decided in plan v1: apart from the Client's blue) or her blue mug of 12–14 (continuity)?
3. **Sofía's look in 15:** 14's war costume (same war day) or the canon office look?
4. **Canon repo:** propose the new sheets for `characters/` at stage 12, or as soon as they pass in stage 3?
5. **Voices:** approve the picks (stop 2), or name takes to swap.
