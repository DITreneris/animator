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

Checks: 38 shots (41 key frames), 0 faults. Layout v3 and board v2 still rebuild md5-identical. Re-tested below (third round).

## Third round (24 Nov): the three newest fixes on 3 new viewers

Same 41 frames (board v3, rebuilt md5-identical), neutral sheets at 400 px and 270 px, the generic prompt plus five direct questions (hands at the door, the foot gag, the phone, the loop, what ties the two places).

| Beat | Intended | A | B | C | Verdict |
|---|---|---|---|---|---|
| 1 | Don and the robot tug the blinds; he wants them down, the robot up | Don pulls the cord, blind falls on him; robot only smiles | same | same | partial 3 of 3: the blind gag reads, the tug-of-war does not |
| 2 | tape line, "pick a side", Pam crosses, Mom neutral, Sofía's heel | read | read | read | read 3 of 3 |
| 3 | selfie, human approval, Don approves | read ("group photo") | read (guessed a selfie stick) | read | read 3 of 3 |
| 4 | booth: "That one." "Invite her." the guard's COO? CV | read | read | read | read 3 of 3 |
| 5 | Sofía takes the CV; the invitation phone; "Everyone's with me"; loop | read, loop read | read, loop read | read, loop read | read 3 of 3 |

Pass: 4 of 5 beats for every viewer, loop read 3 of 3.

The three fixes:
- **1.4, the roll in the other hand:** nobody saw a roll at the door; all three say the other hand is a fist, and that the roll appears at #5 and #9. Harmless, but it carries nothing: the roll is not read before the tape scene.
- **5.4a/5.4b, two key frames:** landed. 3 of 3 read Don straddling the line (#35 wide, #36 close), call it "BOTH" in action, and pick #36 as the screenshot. The 0 of 3 of the second round is now 3 of 3.
- **6.1, the phone small and flat by Pam:** not seen. No viewer mentions a phone in Pam's hand in #40. The only phone read is the 5.7 insert (#39, "INVITATION / DAD" beside the blue mug): owner Pam by the mug A 40%, B 40%, C "Don's, 30%". Same picture as the second round (ownership carried by the mug, not by the hold), a little firmer than 1 of 3.

Shared misreads that are not beats:
- The robot's sun icon: 3 of 3 see "a sun/arrow", none reads "more light" (the tug of beat 1).
- The teal woman (Mom): 3 of 3 call her older, family-like ("Donnie"), none says mother.
- The two men behind the glass: 3 of 3 guess a portrait resemblance, none names Father and the Client.
- #22 and #29, the photo and its copy with dark figures: 3 of 3 half-read it ("someone shouldn't be in it").
- #18, who knocked Don over: C could not tell.

What would undo these: if Tomas wants the tug-of-war read, the robot's arm must visibly hold the other cord (not only a raised arm); if the phone ownership must read in 6.1 itself, the phone has to be in Pam's hand and bigger, which he declined in the 6.1 pick. Neither is changed without his word.

## Fourth round (24 Nov, /grill-me): the tug and the light, staging pair #1-#2 on 3 new viewers

Built (all under `FIX_V4`; checks 38 shots, 0 faults; approved v3 sheets untouched): 1.1 is motion test A's key frame (both hands on their cords, the cords taut, the blind half down, `_tug_11`, `ROOM_V4`); 1.2a gets three warm daylight bands through the bare glass onto Don (`light_in`); 1.4's roll stays in the other hand.

| Question | D | E | F | Verdict |
|---|---|---|---|---|
| Opposite wants (Don down, the robot up) | yes | yes | yes | 3 of 3 (was 0 of 3) |
| The robot holds its cord | "I think so, not certain" | "seems to grip it" | "can't see its hand" | 1.5 of 3: the grip is the weak point |
| The light and the icon | "let the light in" | "more light" | "brightness up" | 3 of 3 |
| Who won | the robot | the robot | the robot | 3 of 3 |

Shared misreads: the robot's hand is hidden against the door frame beside its screen (3 of 3 unsure); the two motion lines under its grip read as "tick marks near Don's hip" (E, F). The fix if wanted: the robot a step left so its arm is clear of the frame, the grip below its screen, the motion lines off.

Fix (Tomas "taisom ranka"): the robot a step left (`rx - 18`), its near arm straight up on the glass, the grip at its tip, the motion lines off. Three new viewers, the same pair and questions:

| Question | G | H | J | Verdict |
|---|---|---|---|---|
| Opposite wants | yes | yes (inferred) | yes | 3 of 3 |
| The robot holds its cord | "a raised claw, not sure" | "a grey gripper holds it" (big only) | "the cord runs to its head; no hand" | 1.5 of 3, unchanged; 0 of 3 at phone size |
| Light and icon | "brightness up" | "sunrise, raise the blinds" | "more sun, open up" | 3 of 3 |
| Who won | the robot | the robot | the robot | 3 of 3 |

The tick marks are gone. The grip itself is still a half-read after two fixes: at 270 px the robot's short arm and the knob merge with its screen. The beat no longer depends on it (the wants, the light and the winner read 3 of 3); in the film the pull is carried by motion test A, which read the tug in motion.

## Hands and phones audit (24 Nov, against `docs/rules-hands-and-phones.md` on main)

Found and fixed (opt-in under `FIX_V4`; checks 38 shots, 0 faults; the approved layouts v3 rebuild md5-identical from `ps_scenes_v3.py`):
- **The posted screen's ♥** (3.5, 4.2): Inter has no such glyph, a hex-code box was drawn. Now a drawn heart (`robot_ps.HEART`).
- **6.1, Pam's phone:** was a dark flat trapezoid with a blue glow and no owner. Now upright in her fist (hands_ps "cup", drawn under her fingers like the mug), small, lit, INVITATION · DAD on it (`pm_ps` pose `reach_ph`, `ps_set.phone_close(buzz=False)`).

Not changed, noted: the ep 14 screens are not drawn through `of_ui.py` (it exists only on main); Don's thumb on APPROVE (`phone_screen` "approved") is a polygon, not the series' hand; the Client's hand in 4.3 is dark brown (the oily handprint?); `hand-validate` and `phone_grip` belong to episode 13's rig. Not yet re-tested on cold viewers.

Cold test of the 6.1 fix (3 new viewers K, L, M; frames 5.6, 5.7, 6.1 and its follow-up, 400 px and 270 px):

| Question | K | L | M | Verdict |
|---|---|---|---|---|
| A phone in 6.1 | no | no | "a pink card or paper with a tiny hand on it" | 0 of 3 read Pam's fist as holding a phone |
| The phone in 5.7 | buzzing, "INVITATION / DAD", lying on a desk | same | same | 3 of 3 read the screen and that it buzzes |
| Whose | "possibly Pam, a guess" | can't tell | can't tell | 0 of 3 firm (K a guess) |
| Does anyone know about it | no | no | no | 0 of 3 |

The third version of 6.1's phone (flat by the CV, then dark, then upright in the fist, lit): 6.1 is a shot misread after three fixes, so by the cold-viewer rule it is cut or its thread moved. The screen text is read; the owner is not.

Tomas's pick: take the phone out of 6.1, carry the owner in 5.7. Built (`FIX_V4`): 6.1 has Pam's empty reach and no phone; 5.7 has Pam's purple cardigan sleeve in from the bottom-right corner and her fingertip on the phone below the words, her blue mug beside it. Checks: 38 shots, 0 faults; approved layouts v3 md5-identical.

Cold test (3 new viewers P, Q, R, frames 5.6, 5.7, 6.1 and the follow-up):

| Question | P | Q | R | Verdict |
|---|---|---|---|---|
| Whose phone | Pam's, ~70 % (the sleeve) | Pam's, fairly sure (the sleeve) | Pam's, fairly sure (the sleeve) | 3 of 3 (was 0 of 3 firm) |
| The screen | INVITATION / DAD, buzzing | same | same | 3 of 3 |
| The arm | Pam's, tapping | Pam's, pressing | Pam's, pointing | 3 of 3 |
| Anyone in the office knows | no | Pam "uneasy or flat" | no | 0 of 3: the knowing is not carried; the film's 5.7 beat and Don's "Everyone's with me" must carry the irony |

The ownership is read from the sleeve's colour only; the mug is not named as the link any more. Not yet re-tested: the whole board after the heart and 6.1 changes.
