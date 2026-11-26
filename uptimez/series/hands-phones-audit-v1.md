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
