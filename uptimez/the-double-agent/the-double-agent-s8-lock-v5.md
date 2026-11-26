# The Double Agent: the S8 frame, LOCKED at v5 (26 Nov)

Tomas, 26 Nov: "Užrakinam" (lock it). **`da_s8_final_v5.png` replaces v4 as the final image (8.1) and the episode's likely cover.** Built by `python3 src/da_s8.py frame5` (1080×1920, frame units 540×960 at 2×); md5 `b62ed8b40151006d61bdc536b10848f5`. v4 still rebuilds byte for byte with `python3 src/da_s8.py frame` (md5 `3a220a5d561912819bf16685a7935192`): v5 is the opt-in `da_s8.V5`.

## What changed from v4, and why

| Change | Why |
|---|---|
| **Sofía in her episode 15 outfit** (`sofia_da`: the job-interview suit, charcoal, pearls, the series' high ponytail) | Script v4: the next day after 14, a new outfit (Tomas); charcoal, not navy, so she does not read as Don's vest (character audit) |
| **Sofía reads her binder in both hands** (`sofia_da.with_board`: the row `board_two`, the binder then a clutch at each upper corner), above the desk | The hands canon: a board, card or printout in two hands is `board_two`; her hands go through `hands_ps` for the first time (female width 15, no nail) |
| **Father leans back, the ring hand on the armrest of Don's chair, the other on his belly** (`da_s8._father_rest`), his sleeves in the dark velvet, the armrest drawn under the hand (two passes) | The folded arms misread three times ("holding the lapels", "one band", "checking a watch" 2/2): the rule changes the gesture. The new one read 2/2 as "a boss in his office" |
| **Both hands through `hands_ps`** (`kit.HAND`, `hands_v4.enable()`; `quiet` at rest) | The hands canon: one hand for the cast; no legacy ball hands in a new shot |
| Pam's mug is the mustard mug (already in v4) | Script v4: Don's gift (2.4) |

## Decisions carried from v4

The fight behind the glass (Don and the robot over the $49,999 throne on the tape line); the plan MY GARAGES with Pam's hands on it and the Client's finger; the $49,999 tag at canon size; Don's curl and headset; Mom not at her desk; the plain far wall; the hand-over carried by 7.3.

## Known and accepted

- The plan's direction (to Pam) does not read in the still: 7.3 carries it.
- The fight is small at phone size (a shape, not faces).
- Father's ring reads as "a red object" at full size and is lost at phone size.
- The Client and Pam keep v4's hands (unchanged drawings from the locked v4; their rigs already draw through `hands_ps`).

## Reopening

Under the freeze rule this frame is reopened only for a fault Tomas sees himself. Its code (`src/da_s8.py`, `src/da_set.py`, `src/sofia_da.py`, `src/dh_cast.py`'s opt-ins, `src/hands_v4.py`) is to be pinned with a tag (`uptimez-double-agent-s8-v5`) when committed.
