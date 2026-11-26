# The front desk set (v4)

The 9:16 room. The 16:9 pilot does not use this file. Its source of truth is [`../the-blueprint/set-16x9.md`](../the-blueprint/set-16x9.md).

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

## Episode 14 (*Pick a Side*): the set's additions (`src/ps_set.py`, 23 Nov)

All drawn on top of the front desk v4 by `ps_set.room()`; nothing in `fs_set4.py`, `set_ob.py` or `dh_props.py` changes, and earlier episodes rebuild as before.

- **The glass door is shut** for this episode (fs_set4 draws it 85 % open; `ps_set` passes `open_=0` for its own frames only).
- **Blinds** on the glass: white horizontal slats on a rail, a cord each side (Don's left at x 32, the robot's right at x 164); states up, down (0..1, the room dims), torn (the rail hangs from its left bracket, the slats are on Don), rehung.
- **The tape** at world x 560 from the back wall to the camera, "DON" and an arrow into his side in black marker. Left = Don's side (zones A, B), right = Father's (C). Never in S2's knees-up framing (1.1, 6.2).
- **The throne's $49,999 tag** on a string from the crown. Drawn here for the first time: episode 12's film has no tag.
- **The robot's card** (v2, from 2.1b): a white inventory card clipped on the throne's back, a cyan barcode, **OWNER: INVESTOR**. Spun (2.2 on), the throne is drawn from behind: the tag's blank back, the card to the room.
- **Pam's phone** face up at the counter's left end (640, 640): dark, or lit; its close (5.7) reads INVITATION · DAD.
- **The step stool** (5.3–5.6) and **Father's booth** as in 12 with the Client's oily handprint (4.3).
- **v3** (set audit, 23 Nov): every state change made bigger than the object: the tape 40 % wider with a dark edge; torn keeps 3 crooked slats on the broken rail and a short cord; rehung has one bent slat (Pam's repair); the price tag 1.5x; the cords shorter, Don's pull white, the robot's grey; Pam's phone is episode 13's invitation card exactly (cream, purple INVITATION, black DAD); the handprint 1.5x.

## The set gate (24 Nov)

`src/set_gate.py` checks every drawing against this page: the props on their marks (`PROPS`: the throne 452, F+8, 0.60), depth (two people who overlap on screen stand on different floor lines; the one behind has his feet higher), and continuity across cuts (nobody is somewhere else after a cut unless the episode lists the walk). Its self-test plants the faults that shipped in Daddy's Home v8 scene 3 (the throne at 540, Sofía and Mom on one line, Mom 300 → 446 at a cut). A change here is copied into `PROPS` in the same commit.
