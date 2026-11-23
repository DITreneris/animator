# The front desk set (v4)

The room where Act B happens (episodes 9–11) and the default room for the series from episode 10 on. Built for *First Search*: `src/fs_set4.py` (draws it), `first-search/fs_set_v4.png` (the sheet). Earlier versions are kept: `fs_set3.py` (v3), `fs_setmap.py` (the v1 map).

## Zones: each with one job

| Zone | World x | Job | What's there |
|---|---|---|---|
| A | 0–280 | Discovery and arrivals | The glass door, the UPTIMEZ FIND screen over it, the HR robot's station; blue confetti from episode 9 in the corner |
| B | 280–570 | The irony | OUR FIRST CLIENT over Don's spot; the sale, the bonk, the payoff; the shredder at its edge (SHRED, a sheet in the slot) |
| C | 570–960 | The counter and the boss's door | Pam at the counter's left end (monitor, the patched plan propped up); Mom at its right end (ASSISTANT TO DON, the baby photo, mug, candy, knitting); DON's office door with its gilt plate DON · CEO · VISIONARY |

## Depth

The counter and the doors are the back plane; the Client, the robot and Sofía the middle; Don stands forward under the portrait; the shredder is a foreground piece. Everyone gets a contact shadow.

## Home positions (world x, feet, scale)

Client 110, F−14, 0.52 · robot 232, F+4, 0.48 · Sofía 352, F−26, 0.47 · Don 440, F+26, 0.60 · Pam 692, F−72, 0.50 (behind the counter) · Mom 824, F−70, 0.50 (behind it, by DON's door; at home: fists, chin up, unimpressed). F = 800.

## Ways through the room

- **Out from behind the counter:** round its LEFT end only (the right end is DON's door), past the shredder, into B. Mom and Pam both use it.
- **In from the street:** the glass door in A.
- **Don's office:** the door in C, behind Mom. Nobody reaches it without passing her.

## Camera setups

S1 the master (far front, A+B) · S2 A front · S3 B front · S4 B low, close under Don · S5 C close (Mom at her desk) · S6 the counter's end (B+C). Inserts have no place. Each episode's shot plan gives every shot one setup.

## Staging rules learned on this set

- Reactions face their target, not the camera.
- The same cast on both sides of a cut; the camera moves, people don't vanish.
- Catch an entrance mid-step (a foot still behind the counter's end).
- The camera has to visit C early if Pam's or Mom's thread matters.

## v5: two props for episode 12 (*Daddy's Home*), opt-in

Nothing in `fs_set4.py` changed. The props are drawn through a shot's own hooks (`back`, `extra`), so episodes 10 and 11 draw as before. Positions are in `src/dh_props.py`.

| Prop | Where (world x, y, scale) | Zone | Its one job |
|---|---|---|---|
| **The CEO chair** (`dh_props.ceo_chair`) | 452, F+8, 0.60: on Don's mark, under OUR FIRST CLIENT | B | The money. Don sits in it in frame 0 with his feet on the shredder, stands in front of it, pushes it away, and the robot looks at it at the end. On casters, so it rolls back |
| **The coffee machine** (`dh_props.coffee_machine`) | 770, F−166, 0.62: on the counter top between Pam and Mom | C | What the visitor has really come for. Four states: broken (OUT OF ORDER), rattle, pop, ok |

**Why:** the concept had Don at a desk, and this set gives him none; the chair replaces it and plants the evidence in the first shot. The machine sits by Pam so that her motive (an empty cup) and its cause are in one frame.

The club booth (`dh_props.booth`) is a separate full-frame drawing, not part of this set.
