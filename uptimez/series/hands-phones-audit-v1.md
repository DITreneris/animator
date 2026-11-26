# Hands and phones: series audit v1 (26 Nov)

Scope: the canon (DITreneris/uptimez `CANON.md`, `docs/rules-hands-and-phones.md`, the hand class sheet v4) against the films still open:
- 11 One Star: master v13 approved, not released;
- 12 Daddy's Home: anim v7;
- 13 The Offer: rough cut v39;
- 14 Pick a Side: master v8;
- Office Noir 4: rough v13.

Released films (1–10, Office Noir 1–3) are history. By the rules they are not rebuilt.

Method:
- a code scan of each film's own modules (`/tmp/hand_audit.py`: hand shapes, `phone_grip`, other phone draws, hand-drawn fingers);
- contact sheets at 1 fps;
- full-size frames at the hand and phone moments.

## A. The canon itself

| # | Finding | Effect |
|---|---|---|
| C1 | Two copies of the rules page. DITreneris/uptimez `docs/rules-hands-and-phones.md` (26 Nov) has the job table and "Read this". animator `docs/rules-hands-and-phones.md` (main) does not. Each says it wins over lessons.md, but neither says which copy wins. | An agent in animator follows the old page (no job table, no `point_t`, no `clutch` row) |
| C2 | The class sheet v4 is "the target", but films still draw the older `hands_ps` / `of_cast` (CANON.md: "until a separate opt-in hand module exists"). No such module exists. | Every film is off the sheet by design: `grab` (thin), `phone_grip` v3 (three loose finger ovals) |
| C3 | Shapes outside the job table in new shots: `relax_s` and `cup` (Pick a Side 4 and 2 calls), `relax` and `relax_s` (Office Noir 4, 84 calls) | The table says a new shot uses the table |
| C4 | There is no row for **a tablet or a board held in two hands** (Daddy's Home's tablet, One Star's site plan and printout, Sofía's card in 6.1) or for **a finger tapping a screen in an insert** (One Star, Pick a Side). Each film improvised one | The same job is drawn three ways |
| C5 | `phone_grip` is the only phone row, but the code scan finds `phone_grip` 13× (The Offer), 8× (Pick a Side), **0** (One Star, Daddy's Home, Best Candidate). Other phone draws: One Star `.phone(k` 13×; Pick a Side `phone_close` 10×, `phone_screen` 7× | A phone without the grip is the rules' "slide" |

## B. Films (frames: `of_pick.png`, `os_pick.png`, `dh_pick.png`)

| Film | Moment | Fault | Rule | Severity |
|---|---|---|---|---|
| The Offer | 0:04 DELETE, 0:33 PAM phone, 0:53 calendar | `phone_grip` v3: three finger ovals at the far edge, apart from the palm; a palm bigger than the phone at 0:33 | sheet v4b = one silhouette | Polish (the series reference, consistent) |
| The Offer | 0:58 Father with a green phone | a phone at the hip, no visible grip at 540 | phone_grip | Minor |
| One Star | 0:35 the Client with the blue printout or phone | a fist with stripes round it, no `phone_grip`; reads as "holds a bottle" | C5 | **Fail** |
| One Star | 0:47, 0:51 tapping SAVE and the review | a finger and blob from the bottom edge, no wrist stub; a "hand walking in space" | close-ups, at the edge: hand and wrist stub | **Fail** |
| One Star | 0:53 Pam at the desk, phone flat | a phone flat on the desk with a pointing hand: OK. Her arm is one stroke to the desk | two-bone arm | Polish |
| One Star | 0:58 Sofía with the printout | fingers as loose ovals over its edge | C4 (clutch) | Polish |
| One Star | 1:00 Don hugging the phone | both hands merged into one blob over the phone | one hand per wrist | **Fail** |
| Daddy's Home | 0:02 Father's tablet | two hands at the bottom corners, the left a plain blob | C4 | Polish |
| Daddy's Home | 0:13 "Dad is coming", 0:41 | Don's arms straight from the shoulder | "an elbow under 20° is a pole" | Polish |
| Daddy's Home | 0:41 the inspector and Don | two hands meeting reads as a handshake (intended?) | gestures | Check intent |
| Pick a Side | master v8 | fixed today: hand-over, oil can, 6.1 grip. Left: 5.2 pen pinch; 5.4 leg (Tomas's lock) | — | — |
| Office Noir 4 | rough v13 | noir silhouettes: hands read as shapes. `relax`/`relax_s` throughout (C3); the letter hands (0:41) OK | C3 | Low (the style hides it) |

## C. What correlates

1. **The canon has no single home or version.** Two rules pages, plus a sheet the code does not draw (C1, C2). Every film fixes hands locally, so the same fault comes back (Pick a Side's phone today, One Star's taps).
2. **Jobs with no row get improvised:** two-hand boards and tablets, insert taps (C4). These are exactly the moments the reviews flag.
3. **Phones bypass `phone_grip`** when the film draws a screen insert first and adds a hand after (C5).

## D. Fix path (proposed, not started)

1. One canon: DITreneris/uptimez `docs/rules-hands-and-phones.md` wins; animator's copy becomes a pointer (or a synced copy with its date).
2. Add rows: `board_two` (two `clutch` at the upper corners) and `tap_insert` (`point_t` plus `insert_cuff` from the nearest edge); each via the §0.2 silhouette test.
3. The opt-in module `hands_v4.py`: draws the sheet's v4 `grab`, `pinch`, `fist` and `phone_grip` behind a flag. Old films are untouched (md5 checks).
4. Per film, opt-in fixes on the failing moments only (One Star 0:35 / 0:47 / 0:51 / 1:00; Daddy's Home tablet and arms; The Offer to `phone_grip` v4b), each with a 270 px still, a 10 fps strip and the GH gate.
5. A gate in `gates_os` GH: fail a phone drawn without `phone_grip`, and an insert hand without a cuff. Plant first.

## E. Correction and progress (26 Nov, later)

- **The audit above used stale films for One Star and The Offer.** main had moved on: One Star v14–v26 (with its own frame-by-frame hand audit in v20, a hand gate `cs_grips` and an insert gate) and The Offer v57. I merged main into this branch (one conflict in `hands_ps`: both opt-in flag sets kept; Pick a Side frames md5-identical before and after).
- **One Star v26, re-rendered and looked at:** the v13 faults (taps with no wrist, the merged hands, the Client's phone) are already fixed there. Taps come from the bottom with a cuff, which is the `tap_insert` row. Its gates pass.
- **The canon:** DITreneris/uptimez is the canon (branch `hands-v4-rows`: the `board_two` and `tap_insert` rows, silhouette-tested 2/2; CANON.md names `hands_v4`). animator's page is now a dated synced copy that points there.
- **`hands_v4.py`** (opt-in): the sheet's grab, pinch and fist (v2) and phone_grip (v4b, small tilts turned with it), plus `board_two` and `tap_insert`. Its check sheet is `/tmp/hands_v4_check.png`.
- **One Star v27** = v26 + `hands_v4.enable()` (`cs_film_v27.py`): every gate passes (hand 0, insert 0, bubbles 0).
  - Changed drawings: 30.5 s (the Client's fist round the gem: sheet grab) and 64.5 s (Sofía's phone: v4b, one silhouette).
  - **A new fault at 64.5:** v4b's thumb lands on "1/5" and its fingers on "Pam". The rule is "the thumb off the words". The sheet's grip covers more of the screen's edge than v3 did. Decision needed before the other films.
- **Decision (Tomas, 26 Nov): films keep the old phone grip (v3).** `hands_v4.PHONE_V4B` is off by default. One Star v27 re-rendered: only 0:30 (the gem in the sheet's grab) differs from v26; 1:04 is v26's phone again. Gates pass.
- **The canon's phone row is now v4c** (DITreneris/uptimez f94fbf1: fingertips stop on the far bezel, the thumb up the near edge; `bp_phone_words.py` passes). `hands_v4` now carries it (`PHONE_ROW = "v4c"`; `enable(phone="v4c")`). One Star v27 uses it. At 1:04, "Pam found it" and "1/5" are clear at full size and at 270 px. Gates pass. Drawings changed from v26: 0:30 (the gem, grab) and 1:04 (the phone). Everything else is identical.

## F. The Offer v58 (26 Nov)

`of_film_v58.py` is v57's five scenes with `hands_v4.enable(phone="v4c")`. Every scene check gives 0 faults; of_cut G5 passes. `of_roughcut_v58_540.mp4`, 64.9 s.
- **Diff against v57, frame by frame:** scenes 1 and 2 are identical (the DELETE phone is tilted past 0.35 and keeps the old grip, as do the inserts' hands).
- Changed:
  - scene 3: the engine-bay tools (sheet grab), the Client's phone ×2, the ignition key (sheet pinch), the guard's calendar phone;
  - scene 4: Pam's phone ×2, Don's phone;
  - scene 5: Father's phone ×2.
- **First try failed:** the sheet's v4c draws its own forearm straight down. Where the rig's arm comes in from the side (the Client at 0:32), that made a second arm, a "U" under the phone. Fix: `hands_v4.FOREARM = False`: the rig's arm runs into the palm, as in the films' grip. Re-rendered: one arm per hand everywhere. One Star v27 re-rendered with it too: 1:04's words are clear, and no extra arm shows.
- **To look at:** the ignition key (3, f668). The sheet's pinch reads as a closed hand with the key in it, where v57 showed two fingertips on the key.

## G. Every held phone (26 Nov, Tomas after The Offer v62: "the phones are not fixed, every frame carefully")

v62 had left the old grip on every phone v4c did not draw upright: tilted (2.7), at the ear (3.7), the inserts drawn in two parts (0.4 DELETE, 2.8 PAM) and the pressing thumb (4.1 DONNIE).
- **`hands_v4.ALL_V4C`** (opt-in, off by default, so v62 and One Star v27 stay as they were) draws all of those in v4c: turned about the palm, the phone's back to us, palm-behind / fingers-in-front for inserts, the thumb to `thumb_tip`.
- **`phone_gate.py`**: a held phone painted without a v4c grip on the call stack fails the film. Its self-test plants the old grip first. On The Offer, v62 FAILS (27 drawings at 3 sites: 4.1, 2.7, 3.7) and v63 PASSES.
- **Limit:** a phone a scene paints itself (a rectangle, not `of_cast.phone`) is invisible to the gate. Daddy's Home 11.6 was one; the frames are still the check.

**The Offer v63** (PR #141): every phone v4c. 4.1's thumb lifts 0.15 s after DECLINED so the word reads.

**One Star v28** (`cs_film_v28.py`): v27 with ALL_V4C. Every gate passes, the phone gate included (840 phone drawings, 0 faults). Changed at 0:00, 0:02, 0:13-0:15, 0:46-0:48, 0:56, 1:06; every one is the phone's back held in v4c.

**Daddy's Home v9** (`dh_film_v9.py`, `dh_hands_v9.py`). v8's baseline was rendered fresh first. Changed against it: scene 1 drawings 27-142, scene 8 188-205; scene 7 54-69 only by a bubble's 12 px shift; the rest identical.
- 0.4-0.7b, Don's phone, at his ear and lowered, was a rectangle with a hands2 grip: now phone_grip v4c, with The Offer v58's pale rim on its back (cold viewers read the black back at his ear as "a hand on his ear").
- 11.6, Father's phone, was a rectangle with an oval thumb: now v4c, the thumb pressing the green button.
- 0.3-0.7, the booth, the guard's hand on the post: now of_cast.clutch on its left edge.
- Phone gate 0 faults.
- **Not done:** Don's straight arms ("Brace yourselves" with arms wide) are a pose, not a broken elbow, so they were left as they are.
- **Cold viewers (2), pre-existing points:**
  - 11.6 "Answer it.": the bubble covers Father's phone (as in v8);
  - the booth: the guard's grey sleeve reads as "someone else's arm", and Father's ring fist shows no fingers.

## H. Daddy's Home v10, One Star v29 (26 Nov, Tomas's /grill-me after the v9/v28 cold test)

**Daddy's Home v10** (`dh_film_v10.py`, `dh_hands_v10.py`; changed against v9 only in scene 1, drawings 27-134, and scene 8, 191-202):
- **The booth:** both hands on the post are now Father's. The left sleeve is his velvet. His ring hand clutches the right edge, four fingers over the front, the ring on them; in 0.5 the tap lifts the whole hand.
- **11.6 "Answer it.":** the box first went on Father's other side, as Tomas picked. There it covered Don's face, because Don's rig is not logged as a face. So the box is over Father's head (form T, dh_say.SAY), and the phone is logged so the box stays off it.

**One Star v29** (`cs_film_v29.py`; changed only at 65.6-65.9 s): in 6.6a the phone is clamped in both hands at one size from the first drawing. Every gate passes.

Phone gate 0 faults on both.

**Cold viewers (2):** the fixes read.
- The tablet is held by "his hands (red sleeves, white cuffs)".
- "No bubble covers a face, phone or hand."
- Neither viewer saw a size jump in 6.6a.

**Points both viewers raised that were already in earlier versions:**
- the booth's face-down post (0.7) reads as "a different object";
- One Star 6.5, Sofía's phone hand has no sleeve ("a hand without an arm");
- Daddy's Home, the invoice arm with no hand ("fused into the paper").
