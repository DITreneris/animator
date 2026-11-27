# UptimeZ canon: scenes, characters, hands

Where the current scenes, character looks and hands are, for a person or an agent about to draw. This page only points. If it disagrees with a page it links, the linked page wins. The story's canon is [`STORYLINE.md`](STORYLINE.md) (premise, cast, canon locks).

## Scenes

| Format | Set | Source of truth | Stills |
|---|---|---|---|
| 16:9 | The office, *The Blueprint* | [`the-blueprint/set-16x9.md`](the-blueprint/set-16x9.md), locked 25 Nov 2026 | `the-blueprint/stills/bp_still_s0.png`, `bp_still_shred.png`, `bp_still_counter.png`, `bp_still_night.png` (locked: they must rebuild byte for byte) |
| 9:16 | The front desk, from episode 10 on | [`series/front-desk-set.md`](series/front-desk-set.md) v4: zones, depth, home positions, camera setups S1–S6 | in that page |
| 9:16 | The Client's garage, *The Offer* | [`the-offer/the-offer-set-v2.md`](the-offer/the-offer-set-v2.md) | in that page |
| 9:16 | The ring, *Office Noir 3* | [`office-noir-3/ring-set.md`](office-noir-3/ring-set.md) | in that page |

A shot is staged on the set's own page, not re-measured from an old film.

## Characters

- **Who they are:** the cast table in [`README.md`](README.md) and the four leads in [`STORYLINE.md`](STORYLINE.md).
- **How they look:** [`characters/README.md`](characters/README.md) names every sheet in [`characters/`](characters/). Heights are in `characters/uptimez-team-lineup.png`.
- **Office look and episode looks.** A sheet tagged with an episode (`-tg-`, `-mf-`, `-ss-`, `-xmas-`, `-on-`, `-on3-`, `-cs-`, `-of-`) is that episode's costume. The office look stays as it is. Within one look, the highest version is current.
- **Drawing rules every sheet keeps** are at the top of [`characters/README.md`](characters/README.md): Don tallest and widest, heads about a third of the body, no noses, no prop over a face, the mini mark on every badge.

## Hands

- **Rules and the job table:** [`../docs/rules-hands-and-phones.md`](../docs/rules-hands-and-phones.md). Name the job from the table before drawing. A new job is a new row on that page.
- **The picture of the table:** [`the-blueprint/rough_work/pic_hands/bp_hand_classes_v4.png`](the-blueprint/rough_work/pic_hands/bp_hand_classes_v4.png). Male hand width 17, female 15, the same shapes, no nail. The robot has two: at rest and the gripper.
- **Which drawing each row uses:** `ACCEPTED` in [`src/bp_hand_sheet_v4.py`](src/bp_hand_sheet_v4.py). Today `grab` and `pinch` are v2, `phone_grip` is v4b (one silhouette: forearm, palm, the side of the hand, three fingers over the far edge, the thumb on the near edge). Every other row is as on the v2 sheet.

### The sheet is the target; films still call the functions

On the sheet, `grab`, `pinch`, `fist` and `phone_grip` are drawn by the sheet scripts. A film draws with the function the job table names (`hands_ps`, `of_cast`). Until a separate opt-in hand module exists, a film that calls `hands_ps` `grab` gets the older grab, not the one on the sheet. Do not edit `hands_ps` or `of_cast` to match the sheet: films that already shipped use them.

### Changing a row

1. Draw the attempt as a new version in `DRAWERS` in `src/bp_hand_sheet_v4.py`.
2. `python3 bp_hand_compare.py <row> <old> <new>` (from `src/`) writes `pic_hands/compare_<row>_<old>_vs_<new>.png`: old and new, male and female, left and right hand, 100 %, 50 %, 25 % and the flat silhouette.
3. Tomas picks. A tie keeps the old drawing. Each row gets at most two attempts. A fix must look better than the version before, not only follow the review.
4. Change that row's entry in `ACCEPTED` and run `python3 bp_hand_sheet_v4.py`. It refuses to write unless every other row matches its source sheet pixel for pixel, the earlier sheets are unchanged, the locked stills keep their checksums, and there is no nail red.

The earlier sheets stay as history: `bp_hand_classes.png` (v1), `_v2.png`, and `_v3.png` (a regression: thin fingers on `grab`, small stubs on `pinch`; rolled back).
