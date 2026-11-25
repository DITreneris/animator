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

## Fifth round (24 Nov, after main moved the board's bubbles to `speech.draw`): whole board, 3 new viewers

Built on branch `uptimez-pick-a-side-speech` (from main c4cf7a9), Tomas's /grill-me picks: the robot's bubble tinted and bold through an opt-in `speech.ROBOT` (off: `speech.draw` byte-identical to main, so Office Noir 4 is untouched); its tip just over the antenna's ball (1.48 r); `speech_gate.check(fill=)` so the gate sees a tinted tail, with two planted-fault selftest cases. Checks 38 shots, 0 faults; `speech_gate` selftest ok.

| | S | T | U | Verdict |
|---|---|---|---|---|
| 4 of 5 beats | yes | yes | yes | pass |
| Loop | yes | yes | yes | 3 of 3 |
| The robot talks differently (caps, pale blue, tail to the antenna, screen face) | yes | yes | yes | 3 of 3 |
| The phone is Pam's | 80 % | 75 % | 75 % | 3 of 3 (sleeve and mug) |
| Speaker a guess or tail not seen | 20, 21, 27, 30, 31, 34, 38 | 5, 20, 21, 30, 31, 38 | 5, 20, 30, 31, 38 | shared: **20, 30, 31, 38** |

Shared staging faults (3 of 3, so the staging's, not the viewers'):
- **#20 (3.1a) "SMILE. RECORDING."**: the robot's box is placed beside its visor, at Don's shoulder, not over its antenna: read as Don's. `speech.draw` takes the side wall before the overhead one.
- **#30–31 (4.3a/b) "That one." / "Invite her."**: the box sits between the Client and Father; the 10–20 px tail is not seen at 270 px.
- **#38 (5.6) Pam's line**: the box is on Sofía's side of Pam, over the gap between them.
- Under all of them: with the short tail the rule demands, the box's side is the only cue, and when a second face is within a box-width on that side the speaker is a guess.

Fixes (Tomas's /grill-me picks: 3.1a an exception; the wall with no other face, reframing where both walls have one; the changed frames on 3 new viewers). All under `FIX_V4`; `speech.CLEAR` opt-in (off: `speech.draw` byte-identical to main); checks 38 shots, 0 faults:
- 3.1a: its own framing (`PART_SHIFT_V4`, grid-searched: no cut sign, tail 10–20 px): in on the robot, Don out of the frame.
- 4.3a/b: one speaker per key frame (`BOOTH_PART_V4`), the other off the edge.
- 5.6: Pam in from the edge (x 200), the background 40 px right: her box on her left, away from Sofía.

| Frame | V | W | X | Verdict |
|---|---|---|---|---|
| 3.1a the robot | fairly easy | easy | fairly easy | 3 of 3 (was 0 of 3 sure) |
| 3.1b Mom | easy | fairly easy | moderate guess (box over Don's head) | 2.5 of 3 |
| 4.3a the Client | easy | easy | easy | 3 of 3 (was 0) |
| 4.3b Father | easy | easy | easy | 3 of 3 (was 0) |
| 5.6 Pam | guess | mostly a guess | guess | 0 of 3 sure: the tail of the narrow box is not seen |

New shared misread (3 of 3): the throne's **blank price tag** (white, a round hole at its point) is read as "an empty speech bubble pointing at nobody". With `speech.draw`'s plain white boxes it now looks like one.

Tomas's picks: 5.6 a frame for Pam only (`SHIFT_V4["5.6"] = (480, -40, 1.0)`, Sofía out; her crossing stays in 5.4/5.5); the blank tag off the throne once it is spun (`ps_set.TAG_OFF`, opt-in). Checks 38 shots, 0 faults. Cold test, 3 new viewers (Y, Z, AA) on 5.4b, 5.5, 5.6, 5.7:

| | Y | Z | AA | Verdict |
|---|---|---|---|---|
| 5.6 who speaks | Pam, "fairly sure" (only person) | Pam, easy | Pam, fairly confident | 3 of 3 (was 0 of 3) |
| 5.6 tail seen | barely; at 270 px "a floating label" | tiny; not at 270 px | not at 270 px | 0 of 3 at phone size: the speaker is read by being alone in the frame |
| An empty bubble anywhere | none | none | none | the tag misread is gone |

Left, noted: `speech.draw`'s 10–20 px tail is not seen at 270 px by anyone in this round or the last; the board relies on the speaker being alone or the box sitting at their face. `COO?` (the CV's lettering) is read as a caption or Sofía's thought, not speech: fine.

Merge with main (24 Nov, PR #99 was "dirty"): The Offer v40 and Daddy's Home v8 had changed `speech.py` (opt-in SIZE, MONO_SIZE, MAX_W, MONO_BOLD, SIGNS_FIRST) and `speech_gate.py` (the button rail, `avoid=`). Both sides kept: `ROBOT` bolds through main's `_weight`; `check(..., avoid=(), fill=None)`; all four selftest cases kept. With ROBOT and CLEAR off, `speech.draw` is byte-identical to main's, with and without The Offer's settings. Main's new rail check found 3 ep 14 boxes in the rail (2.6, 4.3a, 5.6): the board now passes the rail to `speech.draw` as avoid, and Pam's own 5.6 frame has her at x 160. Checks 38 shots, 0 faults.

## Motion tests H–K (24 Nov, after outside review round 1; Tomas's /grill-me: all four, one push in 2.11, Office Noir 1's startle rhythm, checks + 3 new viewers)

Built in `ps_motion.py` (VER 1 each) on the board's own shots, cameras and shifts. Each drawing goes through `frame_checks`; all four pass. The board is md5-identical (the new parameters `SPRING_61B`, `FINGER_42`, `STEP_55` default to the board). Approved test B was rebuilt byte-identical after a stray edit was reverted. `ps.NO_SHIFT` keeps an already-shifted camera from being shifted twice.

- **H (2.4 s), 2.10b → 2.11.** The robot's arms open across the tape. Don hauls it past him onto his side, it rolls straight back into his back, he staggers. The 2.11 camera is the board's, moved 100 px left. The haul starts inside the frame, off the rail.
- **I (1.0 s), 6.1b → 1.1.** The buzz runs 2 drawings, his eyes go round, his hair springs (1.35, 0.80, 1.12), a hold, then the cut into frame 0.
- **J (1.2 s), 4.2.** His fingertip comes in along its own line from the edge and lands on her. The print appears after it lands.
- **K (1.2 s), 5.5.** Sofía comes in from the left onto the tape in her "chest" pose ("walk" put the CV in the caption zone).

Strips at 8 fps, 3 new viewers (AQ, AR, AS):

| | AQ | AR | AS | Verdict |
|---|---|---|---|---|
| H: the robot knocks Don over | yes, no contact seen | yes, no contact seen | yes, no contact seen | 3 of 3 read the bump; none saw a contact frame |
| H: Don hauls it first | read as "arms crossed, the robot rolls in" | the same | the same | **0 of 3**: the haul doesn't read |
| I: the startle | yes | yes | yes | 3 of 3 |
| I: what startles him | the CV ("likeliest") | the CV | the CV | **0 of 3 name the phone** when shown alone (the whole board read it 3 of 3) |
| J: the finger lands on Sofía | yes, near her | yes | yes | 3 of 3 |
| J: whose hand | can't tell | "a UI tap" | can't tell | **0 of 3** (alone; on the board 4.3a follows with the Client) |
| K: she steps onto the tape | a glide | a glide | a glide | **0 of 3**: no step cycle |

### K v2 (24 Nov): a real step cycle

Code: `sofia_ss.LEGS` (opt-in, v6) is a leg override. The leg pivots from the hip (shear plus shortening), so the shoe moves and the hip stays under the skirt. sofia_ss's own `step` is a sine, so the planted foot slid forward in the second half of each step (lesson 39), and it wasn't used. `ps_motion.k_gait`: three steps (lead, back, closing), each foot standing still on the floor between its swings, the body midway between the feet, and a rise at mid-swing with the standing leg straightening. Measured: each sole stays on the same pixels until its next step (79–85 → 124–132 → 139–145). The board's 42 frames are md5-identical. Lesson 93 order: a black silhouette strip, then without the CV, then the full shot. Checks: pass.

Three new viewers (AT, AU at 216 px, AV at 270 px):

| | AT | AU | AV | Verdict |
|---|---|---|---|---|
| K: she walks with steps | yes, a stride in frames 2–4 | "step poses on a gliding body" | "a step and a glide" | **1 of 3** (was 0 of 3) |
| K: feet planted | "can't tell from stills" | "mostly, some skating" | "may slide" | 0 of 3 sure |
| K: CV stays in hand at the chest | yes | yes | yes | 3 of 3 |
| K: ends on the tape | yes | yes | yes | 3 of 3 |

Shared note (not a beat): the shredder "slides in" from the left. In fact she uncovers it by walking right. All three say the legs alone carry the walk ("the upper body barely moves").

### K v3 (24 Nov, Tomas: "bring in the upper body")

Changes on top of v2:
- a lean into the walk (4°, settling to 0 by 1.05 s); the bun leans with her (`sofia_ps`, an identity transform at 0°);
- the free hand of the "chest" pose swings 18° against the moving leg, elbow kept (the pose `chest_step`, set per drawing);
- the bob goes from 3 to 5 px.

The board is md5-identical, test B is unchanged, and the checks pass.

Three new viewers (AW, AX at 216 px, AY at 270 px):

| | AW | AX | AY | Verdict |
|---|---|---|---|---|
| K: she walks with steps | "a mix: steps in 2–4, a glide in 5–8" | "a walk, with a small glide on top" | "a walk, but a very smooth one" | **2 of 3** walk (v1 0, v2 1) |
| K: feet planted | "skate a bit in 5–8" | "partly skate" | "planted in 2–4, maybe sliding in 5–7" | the middle step is the weak spot |
| K: CV at the chest | yes | yes | yes | 3 of 3 |
| K: ends on the tape | yes | yes | yes | 3 of 3 |

Shared misread (all three): frames 5–7 (0.50–0.75 s) are the long middle step, where the back leg passes the planted one. The feet "bunch or cross" there and read as a skate. In stills at 8 fps the lift there is small.

### H v2 (24 Nov, Tomas: "the robot passes in front")

Restaged 2.11 (`ps_motion.shot_H2`, VER H 2):
- **haul:** Don backs away, both hands on the robot's near hand, leaning back from −0.10 to −0.28, with effort strokes. The grip is solved per drawing, with the IK aimed in the leaned frame (lesson 263); each hand is within 4 px of the robot's hand.
- **release:** the robot sails past IN FRONT of him to his left, with speed lines drawn behind him.
- **roll back:** it rolls back behind him while he smiles smugly.
- **contact:** a contact frame of 2 drawings, a small yellow jagged burst under Don's layer with no flash (lesson 114).
- **end:** the board's bump.

The camera is the board's minus 70: at minus 100 the robot's face went under the rail at the start of the haul. Checks pass.

Before this, silhouettes (hands section 0) of three leans at 270 px, two viewers:
- the strongest lean (3) was clearest for both;
- viewer 1 (asked about a pull) read it as a pull;
- viewer 2 (neutral) read it as a **push**. In a still the direction can't be seen, so it was decided by the motion test.

Three new viewers on the strip (AZ, BA at 216 px, BB at 270 px):

| | AZ | BA | BB | Verdict |
|---|---|---|---|---|
| H: Don hauls the robot | "the robot shoves him" | "the robot's arm shoves him; he leans away" | "grabs its arm; maybe a tug-of-war" | **1 of 3, partly** (v1 0 of 3). Shared misread 2 of 3: the robot shoves Don |
| H: contact | frame 16, the burst | frame 16 | frame 16 | **3 of 3** (v1 0 of 3) |
| H: knocked over | yes | yes | yes | 3 of 3 |
| H: smug before the hit | "didn't see it coming" | "thought he'd won" | "thinks he has won" | 3 of 3 |
| H: whose fault | the robot | the robot | "partly Don, he grabbed first" | the cause (Don's haul) reads 1 of 3 |

Shared cause of the misread: the robot's arm runs straight into Don's hands in front of his belly. Its arm lies across his body, so it reads as the arm pushing him. Nothing shows the robot being dragged: no resisting tilt toward him, no trace on the floor.

### H v3 (24 Nov, Tomas: "another round: drag cues")

Changes on top of v2:
- **the grip:** the robot's near arm is raised (−125°), so Don's hands hold it at chest height, arms straight out from his body. The grip point is now the drawn hand: the rig returns it without the tilt, so `rob_hand` rotates it about the wheel.
- **the tilt:** the robot leans toward him (−0.22).
- **drag marks:** the wheel leaves two marks on the floor.
- **the start:** the haul starts 15 px closer, so its face stays out of the rail.

Checks pass at the board camera −70.

Three new viewers (BC, BD at 216 px, BE at 270 px):

| | BC | BD | BE | Verdict |
|---|---|---|---|---|
| H: Don hauls the robot | "the robot drags Don (an HR escort)" | "Don pulls its arm" | "Don shoves the robot" | **1 of 3** (v1 0, v2 1) |
| H: who starts it | the robot | Don | Don | Don 2 of 3 |
| H: contact | frame 16 | frame 16 ("small, partly hidden") | frame 16 | 3 of 3 |
| H: knocked over | yes | yes | yes | 3 of 3 |

**The third round misread the haul gesture** (arms crossed, then shoved, then shoved or dragged). Lesson 178: change the gesture, not its parameters. The contact frame, the smug pause and the fall are fixed and stay.

### H v4 (24 Nov, Tomas: "drop the haul")

The barge-hauler (Tomas's pick after the third misread) was tried as silhouettes first. It doesn't fit the rigs: the robot's arm is too short to go over Don's shoulder from any distance, so the robot ends up pressed against him and the two silhouettes merge into one blob. Making it work would need new rig code or a new prop (a rope), so Tomas dropped the haul.

2.11 v4:
- it opens with the robot already on Don's side and Don smiling smugly (0.40 s);
- it rolls back toward the tape, into him, with speed lines (0.25 s);
- the contact frame (2 drawings, the yellow burst under Don's layer, no flash);
- the board's bump.

The why is carried by 2.10 and the whole board. The camera is the board's −100 (at −85 the HR badge is cut at the left). Checks pass. Not yet re-tested on viewers: the contact, the smug pause and the fall each read 3 of 3 in v2 and v3.

H v4 cold test (25 Nov), three new viewers (BF, BG at 216 px, BH at 270 px):

| | BF | BG | BH | Verdict |
|---|---|---|---|---|
| Don smug, unaware | yes | yes | yes | 3 of 3 |
| The robot charges into him | yes ("a ram") | yes ("on purpose") | yes ("ran into him") | 3 of 3 |
| Contact (frame 13) | yes | yes | yes | 3 of 3 |
| He's knocked over, the robot's fault | yes | yes | yes | 3 of 3 |

**Pass; H is closed** (v4, one over the budget of 3, with the reason logged above).

Shared notes for the film (stage 7), not fixed in the test:
- **The hit is rushed** (3 of 3): the charge and the hit take two drawings. In the film, hold the contact one drawing longer and let the charge start a little earlier.
- **"Frozen mid-fall, never lands"** (3 of 3): that's the test's padding on the board's end pose. In the film he lands or the cut comes on the tilt (2.11 is 1.6 s, then 3.1).
- **The 2.10b arm hold drags** (0.6 s, 3 of 3), and the robot is half out of frame at the cut (2 of 3).

## Gag stills v2 (25 Nov): Tomas's picks and the outside review of draft v1

Tomas's picks (two /grill-me rounds):
- **HR?** on the CV in place of COO? ("COO not works for our audience").
- An **oil can** handed to the robot at the door; the stool wobble dropped.
- The robot doesn't notice that HR? is its own job (pays off in 15).
- Don's **pose strains** in 3.4.
- The **bodyguards lean away** in the booth.

Stills only, no video: `ps_gags_stills_v2.png`. All opt-in (`GAGS_V5`, `sofia_ps.CV_WORD`, the robot's `tele`, `phone_s` and `visor="heart"`, `ps_set.DOOR_OPEN`). With them off the board is md5-identical and `check` finds 0 faults. The oil can is Office Noir 3's (`robot_on3.oil_can`). The door, pose and booth stills are drawn by scripts outside the scene file; they are not ported into `ps_scenes.py` yet.

Two cold viewers on the three strips (BI, BJ; neutral folders, no names):

| Strip | Read | Not read | Verdict |
|---|---|---|---|
| The pose strains (5 stills) | hold, sweat, frown, the press, the green tick, the relief: 2 of 2 | **The joke:** both read "he is pressured into approving and panics", not "his arm tires holding the pose". The robot sliding the phone under his thumb: 0 of 2. The misses: 0 of 2. The phone is "a tablet" | **Partial.** Sweat and a frown read as fear of the post, not strain |
| The oil can (2 stills) | a gift from the stern guard, the robot delighted (the heart): 2 of 2 | **The object:** "a bucket, a mug, a bag", 0 of 2 | **Partial.** The gag reads, the can doesn't |
| The bodyguards lean away (2 stills) | — | The lean: 0 of 2 ("almost nothing changes"). Both read the guards as **holding the Client down: a hostage video** | **Fail, and it says the wrong thing:** the Client is Father's ally |

## Gag stills v3 (25 Nov, Tomas: "tobulinam", third /grill-me)

Picks:
- **Booth:** the guards pinch their noses (the Client smells of gas and oil, ep 9 canon).
- **Pose:** no misses; the tired arm sinks and the phone meets the thumb; no sweat, no worried face.
- **Oil can:** a classic brass oiler with a long spout and a drop (new drawing, `robot_ps.oil_can`).
- **The guard** stands one step inside the door.

`ps_gags_stills_v3.png`. Two new cold viewers (BK, BL):

| Strip | v2 | v3 | Verdict |
|---|---|---|---|
| The pose (3.4) | "pressured, he panics" 2 of 2 | **"He cheerfully, thoughtlessly approves a public post"** 2 of 2; smug at the end 2 of 2. The tired arm: 0 of 2 (read as a reach). The robot's part: 0 of 2. The phone is "a tablet standing on the floor" | The story beat now reads right (protect list 3). The strain gag itself doesn't read in stills |
| The oil can (5.3b) | a gift, the robot delighted 2 of 2; the object 0 of 2 | a gift, delighted 2 of 2; the object **"a golden basket, a handbag"** 0 of 2; still 2 read as "it tosses the bag up", not oiling | The gag reads; **the object failed twice.** The spout reads as a handle |
| The bodyguards (4.3) | "a hostage video" 2 of 2 | hostage 0 of 2; **a smell gag 1 of 2**; the other: "hands to their earpieces" | Partial. The wrong meaning is gone |

## Gags, round 4 (25 Nov, Tomas: "stiprinam")

Changes:
- **Oil can:** a paper label OIL on the can and big black drops; the robot holds it level, its spout over its own raised joint.
- **Booth:** big green stink lines; the pinching hand comes from the side away from the earpiece cord.
- **Pose:** a motion test in place of stills (`ps_gag_pose_v1.mp4`, 2.7 s, 15 drawings/s; checks pass; 10 fps strip `ps_gag_pose_strip_v1.png`): hold 0.45 s, the raised arm shakes and sinks (slow, then it gives way), the phone slides in under the thumb, the green tick, smug, the thumb back up.

Stills: `ps_gags_stills_v4.png`. The drawing scripts are kept in `src/ps_gags/` (not yet ported into the scene file). Two new cold viewers (BM, BN):

| Gag | Result | Verdict |
|---|---|---|
| The oil can | "a can labelled OIL" 2 of 2; a treat or bribe for the robot 2 of 2; the robot delighted 2 of 2. Unclear who holds the can in the second still 2 of 2 | **Pass** (the object was 0 of 2 twice before) |
| The bodyguards | stink lines 2 of 2; both pinch their noses 2 of 2; "he smells, they suffer, he doesn't react" 2 of 2 | **Pass** (v2 hostage 2 of 2, v3 1 of 2) |
| The pose (motion) | he approves the public post and ends smug 2 of 2; **the tablet moves to meet his hand 2 of 2** (was 0 of 2 in stills). The shaking arm: "nervous, hesitant" 2 of 2, not tired | **Partial.** The robot's part and the story beat read; the shake still says nerves |

Shared notes: the phone is "a tablet"; the #TeamDon photo on the booth's phone is cut by the frame ("#Teams"); the Client's oil reads as "scratches, bruises or dirt".

## Board v4 and the pose's new gesture (25 Nov, Tomas: "tvarkom, kas liko")

**Ported into the scene file** (all behind `GAGS_V5`; `python3 ps_scenes.py check v5`, `board v5`, `script v5`):
- **HR?** on the CV (5.2 with a real pen, 5.3a, 5.5, 5.6, 6.1); the CV 18 % smaller and lower, her face clear.
- **4.3:** the two bodyguards behind the bench, noses pinched, the stink lines; their heads are passed to the bubbles.
- **5.3:** a second key frame, 5.3b, close on bodyguard 2 and the robot with the oil can and the heart. "Welcome." stays on 5.3a. The robot rolls 30 px toward him from its 5.3a mark so the can stays left of the button rail.

Board v4: 38 shots, **43 key frames**, 66.3 s; `check v5`: 0 faults. With the switch off, board v3 is md5-identical and `check` finds 0 faults. Script v9 is generated (`script v5`); v8 and the timing file are byte-identical. Changed frames: `ps_board_v4_changed.png`.

**Not cold-tested:** board v4 as a whole board, and its 5.3b key frame as drawn in the scene file (the round-4 still had the can held level, dripping; the board frame holds it up beside the robot's head so nothing crosses its visor).

**The pose (3.4), a new gesture** (lesson 178: the shaking arm read as nerves three rounds running): the raised arm drops, he heaves it back up (two arcs under the elbow), it drops for good, the phone slides in under the thumb, the green tick, smug. No shake marks; he grins throughout. `ps_gag_pose_v2.mp4` (2.6 s), strip `ps_gag_pose_strip_v2.png`; checks pass. Not cold-tested (Tomas, 25 Nov: stills first, test when asked). It is still drawn by `src/ps_gags/L6.py`, not by the scene file: it goes in with the animation (stage 7).

## The hand gate and the hand sheet (25 Nov, Tomas: "ar mes praeinam gate?")

Before: `check` ran no hand gate for episode 14 (only "no more than two arms"). `hand_gate.check` run by hand on the new frames failed 4.3: "two at one wrist", a second hand drawn 4.5 px from the guard rig's own.

Fixed:
- **The gate is wired in.** `ps_scenes.grip()` declares a hand drawn outside a rig (5.2's pen hand, 4.2's finger); the rig wrappers log their hands; `check` runs `hand_gate.check` on every key frame. `hands_validate()` plants a foreign hand on the guard's own in 4.3 and must see it fail before any frame is checked (it does).
- **4.3, the noses:** the guard's OWN arm, drawn after his head (`dh_cast.ARM_FRONT`, opt-in). No second hand.
- **5.3b, the oil can:** held by its loop handle on the hand the rig returns, the robot's hand drawn again over it (`robot_ps.hand_again`, as `robot_mf` does for the cuffs). It is in the robot's near hand, over the guard's dark suit, so its visor and the heart are clear.
- **3.4, the thumb:** a thumb, not a fingertip (Tomas, 25 Nov: the series' "Approved"). The phone's own drawn-in thumb is off (`robot_ps.PAD_THUMB`), so there is one thumb; the pad is brought to where his arm puts the hand (0.1 px).
- **The hand sheet** `ps_hands_board_v4.png` (`src/ps_hands.py`; not `ps_hands_v1.png`, the cast sheet approved 23 Nov): eight hands cut from the film's own frames at 1:1. It found two faults the checks had passed: Sofía's CV hanging beside her hand (my lowering of it; back on her hand now, smaller) and the two thumbs on the pad.

Now: `check v5` 0 faults with the hand gate on; `check` (board v3) 0 faults; board v3 and Daddy's Home's cast sheet md5-identical. `ps_gag_pose_v3.mp4` and its strip replace v2.

Still open in section 0: the three-silhouette test with two cold viewers (step 2) and the gaps re-measured on the 270 px tile (step 3) are not done; nothing was shown to viewers this round. In 5.5 the word HR? sits just under her mouth, over her chin.
