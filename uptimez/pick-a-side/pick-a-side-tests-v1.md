# Pick a Side: checks, board v3 and motion tests (24 Nov)

UptimeZ Inc. · episode 14 · stage 5–6 results. Tomas's /grill-me picks (24 Nov): all the series' checks, each proven on a planted fault; board cold test with 3 new viewers and the script's direct questions; motion tests D–G; hide the door confetti; the robot's sun with an up-arrow.

## The checks (`src/ps_checks.py`, run by `python3 ps_scenes.py check`)

| Check | Rule | Planted fault (must fail) | Result on 38 shots |
|---|---|---|---|
| limbs | at most 2 arms per character (one per shoulder, frame surface only) | Don drawn twice: 4 arms | pass |
| tails | tip at mouth height beside the cheek (uz_check MOUTH); the robot's onto its antenna ("T"); ≤ 48 px past the box | tip on the crown; tail 180 px long | pass (1.4: known exception, Tomas 24 Nov) |
| strays | effect marks declared with an owner, near the owner | a crash line far from Don | pass (no marks in the board) |
| map | every shot id once; restaged shots drawn by the expected function (`EXPECT`) | 2.1 defined twice | pass |
| don | Don the tallest; the widest within 10 % (Sofía's jacket: 87 vs 82 px) | The Offer's Client at 0.52 beside Don | pass |
| zones | story props (phones, CV, the robot's card, the tape roll) out of y > 720 and the buttons | the CV moved under the buttons | pass |

What they found, fixed in v4 (opt-in `FIX_V4`; board v2 and layout v3 rebuild md5-identical):
- **11 long tails** in board v2 → board v3 uses `bc_sb.bubble` (beside the face, short tail onto the cheek, measured on each speaker's silhouette).
- **Pam's phone lit in 5.4–5.6** (the continuity row: dark until 5.7) and **two lit phones in 6.1** → dark until 5.7; one phone in 6.1.
- **Phone inserts 3.5, 4.2, 5.7** dipped into the bottom quarter → raised 34 / 54 / 12 px.
- Reframed for a wall beside the speaker: 2.5, 2.10, 6.1. One key frame per line: 3.1, 4.3 (Client 24 px right). 6.1: Sofía's CV lower (off her face), Pam's phone bigger.
- **1.4** stays a known exception: Don holds the roll beside his face, so the tail crosses it (58 px against 48).

## Board v3 cold test (3 new viewers, neutral sheets at 400 px and 270 px)

| Beat | A | B | C |
|---|---|---|---|
| 1 Blinds tug (Don vs robot) | missed: "the blinds fall on Don" | missed | half: "robot pulls up so it's visible" |
| 2 The line, Pam with Don, Mom on it, Sofía's heel | read | read | read |
| 3 Selfie, approval, Don approves | read | read | read |
| 4 Booth: "That one", "Invite her", COO? | read (Client and Father swapped) | read | read |
| 5 Sofía behind Don with the CV, "Everyone's with me" | read | read | read |

**G4 pass: 4 of 5 for each viewer; the loop read by all three.** Shared misreads (to the shot list, not fixed yet):
- Why the robot pulls the blinds up: not in the stills; carried by motion test A (passed 2 of 2, 23 Nov).
- The silhouette behind the glass (3.6, 5.1): who, and what happened to his phone (3 of 3 can't tell).
- "INVITATION · DAD" (5.7): read as Don's phone (2 of 3).
- Which side of the line Don's door is on (2 of 3 can't tell).

## Motion tests (15 drawings/s on 30 fps; strips at 8 fps; two cold viewers each)

| Test | Shot | v1 | v2 | Status |
|---|---|---|---|---|
| D | 2.1 the tape rips toward the camera; Pam hops left, Sofía right, Mom stays | Don made it 2/2; Sofía's hop weak; Mom read as "a man in teal" | hops read 2/2 (left / right / stays); Mom's gender unclear at 216 px | pass |
| E | 3.1–3.2 the arm telescopes, Don poses, FLASH, the photo | read 2/2 | — | pass |
| F | 5.6 Pam frozen in front, Sofía crosses the line | crossing read 2/2; the DON arrow "points at no one" | — | pass |
| G | 6.1 Don sincere, nobody looks; Pam reaches to her phone | nobody looks 2/2; Sofía's face covered by COO? 2/2; the reach read as "a purple cord" | face clear 2/2; nobody looks 2/2; the phone read as "a blue glow" / "the chair" | partial: the phone |

The checks ran on every drawing of D–G: all pass.

## What the tests can't tell

Whether it's funny, the voice timing and the mix: those need people with sound on.

## Second round (24 Nov, after "darom"): the four shared misreads, and G v3

Fixes (all opt-in under `FIX_V4`; the approved sheets still rebuild md5-identical): the guard behind the glass gets his canon sunglasses and earpiece coil (`ps_set.GUARD_CUES`); 5.4 framed wide (0.8) with DON's door and a readable DON · CEO plate across the tape (`ps_set.PLATE_BIG`); Pam's blue mug beside the phone in 5.7; Pam's phone upright in her hand in 6.1 and in G v3. Checks: 38 shots, 0 faults.

Three new viewers, the same board plus five direct questions:

| Question | A | B | C | Verdict |
|---|---|---|---|---|
| Who's behind the glass? | "the red room's agent", hands over the CV | sunglasses; works for the red room | sunglasses; "Dad's man or Dad" | better: 3 of 3 link him to the booth |
| Whose phone says INVITATION · DAD? | the blonde's (the DAD card beside her in 6.1) | the blonde's, unsure | **Pam's (the blue mug)** | 1 of 3: 6.1's upright phone beside Sofía's CV now reads as hers |
| Whose door, which side? | DON · CEO, right, not his side, unsure | DON · CEO, can't tell the side | DON · CEO, not the ← DON side, unsure | the door reads; the side half-reads |
| Why does he lift his foot? | can't tell | can't tell | can't tell (the heel in 2.8 is the blonde's) | 0 of 3: at 0.8 zoom the foot gag is too small (motion test C read it 2 of 2) |
| What ties the office to the red room? | the post, the portrait | the post, the portrait | the post, the portrait | 3 of 3 |

New: 1.4's bubble (the known exception) read as the blonde's line (A) / "can't tell who speaks" (B).

G v3: the phone is seen ("DAD") but 2 of 2 read Pam's reach as toward the throne. Third version: by the mute test's rule the thread is carried by another shot (5.7, the mug).

## Tomas's three decisions (24 Nov) and what was built

- **5.4: two key frames.** 5.4a wide (his door, DON · CEO, across the tape), 5.4b the medium (the foot over the line); in the film the camera pushes in (`KEYS_V4`).
- **6.1: Pam's phone small and flat under her fingers**, away from Sofía's CV; Pam's ownership is carried by 5.7 (the blue mug).
- **1.4: the roll in Don's other hand** (frame left, the pose mirrored), so his bubble sits on his right with a short tail; the known exception is lifted (`KNOWN_V4` empty).

Checks: 38 shots (41 key frames), 0 faults. Layout v3 and board v2 still rebuild md5-identical. Not yet re-tested on cold viewers.
