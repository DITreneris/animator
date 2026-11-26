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

## 5.5: HR? off her mouth, variant C (25 Nov)

The CV word covered Sofía's mouth in 5.5. Tomas had three variants drawn (`ps_55_abc.png`):
- **A:** the word smaller in 5.5. Still over her mouth.
- **B:** her CV hand lower (pose `chest_low`). Her mouth is clear, but the word sits on her chin.
- **C:** HR? at the sheet's foot in every shot. Her face is clear in all three shots.

An outside review rated C 9/10, B 7.5, A 5.5 (fail). Tomas: proceed with C plus the review's three fixes:
- **P0:** 5.2's nib now sits just under the ?, not over it (`PEN_C`).
- **P1:** HR? 12 % bigger in 6.1.
- **P2:** a gap between the word and the sheet's edge.

C is the default with `GAGS_V5`. `check v5`: 0 faults. Board v3 is md5-identical. Script v9 regenerated. Frames: `ps_55_c_final.png`.

## Section 0, step 2: the silhouette test (25 Nov)

Three black variants per gesture at 270 px, two cold viewers (BO, BP), neutral prompt:
- **Booth** (`ps_sil_booth_v1.png`, 1 is the board's): 1 the nose pinch, 2 a flat hand over the face with the other fanning, 3 leaning away with palms out.
- **Oil can** (`ps_sil_can_v1.png`, 1 is the board's): 1 held up by its handle, 2 still in the guard's hand, 3 hugged in both arms.
- **Don's arm** (`ps_sil_pose_v1.png`, 1 is the gag's): 1 the arm dropped halfway, 2 hanging at his knee, 3 the other hand propping the elbow.

| Gesture | Variant | BO | BP | Verdict |
|---|---|---|---|---|
| Booth | 1 (board) | "no gesture, a blob" | "nothing happening" | **0 of 2** |
| Booth | 2 | "a raised fist" | "a fist, a punch or a cheer" | The clearest shape, but the wrong meaning |
| Booth | 3 | "phone or covering the mouth, muddy" | "hand to chin, a phone or a face-cover" | Muddy |
| Oil can | 1 (board) | "reaches to its shoulder" | "hands it something" | The can is lost in the merge |
| Oil can | 3 | "the robot spreads its arms" | "pushing it; the robot recoils" | Clearest, but read as a push |
| Don | 1 (the gag) | "two thumbs up" | "hands up, wait" | The pose reads; the drop does not show |

**All three gestures fail the silhouette test.** Each one happens in front of a body (a hand at the face, a can against a torso, an arm across a chest), so in black it merges into the figure. In colour, the nose pinch with the stink lines and the oil can each read 2 of 2 (round 4). The rules page asks for negative space around a gesture that must read in silhouette.

## Board v4: whole-board cold test (25 Nov)

All 43 key frames with bubbles, numbered with time stamps: two sheets at 200 px and one at phone size (135 px). Three new viewers (BQ, BR, BS), the whole-board prompt with the loop question, plus direct questions on HR?, the booth and the oil can.

| Beat / question | BQ | BR | BS | Verdict |
|---|---|---|---|---|
| Don's situation: shut out of Dad's meeting, sure everyone is with him, played | yes | yes | yes | 3 of 3 |
| Sides: Pam his, Mom neutral, Sofía switching, the robot "both" | yes | yes | yes | 3 of 3 |
| The loop leads back into the start | yes | yes | yes | 3 of 3 |
| **HR? on the CV: the robot's job, a threat to it** | yes | yes | yes ("it doesn't notice, it just got oil") | **3 of 3** |
| **The oil can: a bribe, the robot delighted** | yes | yes | yes | **3 of 3** |
| **The booth: the bodyguards pinch their noses at the smell** | "just stand guard"; the green lines "smell or tension" | "a stink or smoke gag, a hand near his face" | "a hand to his ear or chest"; the lines "smell, smoke or tension" | **1 of 3** (the stills test was 2 of 2). At board size the pinch is too small; the lines alone carry it |

Shared notes (not beats):
- **The red room is rushed and reads as a new subplot**, "a different movie": 3 of 3. This was already the case on board v3.
- **Who the Dad invitation is for** is unclear: 2 of 3. One viewer thought it was Pam's.
- Funniest: "BOTH." 3 of 3, the one heel 3 of 3, "SMILE. RECORDING." 2 of 3, the oil 2 of 3.
- Slow: Don's standing shots in frames 8–10 and his walk along the line (36–37): 3 of 3.

## The booth's close and the #TeamDon bridge (25 Nov, Tomas: "tvarkom")

- **4.3b:** a new close on both bodyguards, noses pinched, between the Client's "That one." (4.3a) and Father's "Invite her." (now 4.3c). No line. The shot keeps its length and its timing for now (`CLOSE_43`). Board v4 now has 44 key frames.
- **4.1:** the #TeamDon post just seen in the office (3.5), on the phone the silhouette lifted at the door (3.6), now in bodyguard 1's black-sleeved hand under the neon. Episode 13's approved phone hand (`of_cast.phone_grip`), declared to the hand gate with its thumb toward his body. The office and the booth now share one visible prop.
- `check v5`: 0 faults, hand gate included. Board v3 md5-identical. Sheet: `ps_booth_bridge_v1.png`. Not cold-tested.

**Not built: the invitation in Sofía's hand.** Picked from my option, but the script and concept v3.2 say the invitation is **Pam's**: her phone lies on the counter from 1.2, lights up INVITATION · DAD in 5.7, and in 6.1 Pam's hand reaches across the line for it (the Client's condition for Father is Pam). The viewer who read "it's Pam's" was right. My option assumed Sofía; it would undo canon. Put back to Tomas.

## Phones against the repo's rules (25 Nov, Tomas: "kaip vaizduojame telefonus, kaip patobulinti?")

Rules checked: `docs/rules-hands-and-phones.md` §1 "A phone in a hand" and §2 "Phone screens", and lessons 225 (the holder visible or implied), 226 (one UI kit; the story's word the biggest; nothing under ~9 units; light screens) and 295 (a cropped word reads as another word).

Fixed, all behind `GAGS_V5`; with the switch off the screens are md5-identical and board v3 is unchanged:
- **One UI kit.** `ps_ui.py` draws episode 14's screens on episode 13's `of_ui` (status bar, app bar, card, pill, avatar):
  - 3.3–3.4: PUBLIC POST?, the biggest thing on the screen, then APPROVE turning green with a tick;
  - 3.5 and 4.1: the #TeamDon post;
  - 5.7 and 6.1: Pam's invitation is episode 13's own `of_ui.invite` (DAD).
- **4.2:** the push-in is a pinch-zoom into the photo with no caption, so the cut word "amDon" is gone (lesson 295). The heel point is re-measured for the new layout (`ps_ui.HEEL_PT`).
- **3.4:** the robot's phone is in the board frame, the gag's payoff pose, the green pad by his thumb (`PHONE_34`).
- `check v5`: 0 faults. Sheet: `ps_phones_v1.png`.

**Not fixed, 6.1: Pam's hand has no owner** (rule 225; this is why 2 of 3 couldn't tell whose invitation it is). I grid-searched 6.1's framing (x −150 to −60, y −240 to −180, zoom 1.28 and 1.33) to bring Pam's face in. Every framing that shows her cuts a sign (OUR FIRST CLIENT, the throne's INVESTOR card, DON on the floor, ASSISTANT TO DON). Moving Pam off her mark is not allowed (the set rule). Needs a decision from Tomas.

## Phone review fixes (25 Nov, board v4, all behind GAGS_V5)

| Item | Fix | Result |
|---|---|---|
| 4.2 grease dots read as eyes | `point_t`, no dots (rules §1 "big or turned hands") | clean index on Sofía's heel |
| 3.5 phone too small | scale 2.3 → 2.95 (+28 %), y 500 → 430; 3.1 broke the bottom-quarter zone | `check v5` 0 faults |
| DAD not the biggest word | `pss.phone_close` uses episode 13's own `of_ui.invite_small` (DAD 30, INVITATION 13.2); no new code | 5.7 and the counter phone in 6.1 |
| 3.3 PUBLIC POST? said twice | new visor kind "ask": one big "?" | bubble carries the words |
| 6.1 Don's two fists (lesson 207: "toes") | silhouette test, 3 variants (thumbs in vest / thumbs up / arm out), 2 cold viewers: both picked thumbs up, both found "arm out" hardest | `DON_61 = ("thumbs", None)` |

Lessons applied: 163, 207, 263, 264, 417, rules §0 and §1. Board v3 unchanged (git clean), `check` and `check v5` 0 faults. Stills: ps_phones_v2.png.

## Review 2 of the phone frames (25 Nov, 8.3/10, Tomas: B + hands → LOCK)

| Item | Fix | Result |
|---|---|---|
| Pam's phone not tied to her (B) | `pss.CASE`: muted purple case, 3 cream flowers on the rim (case 136×240, screen untouched); the flat counter phone in the same purple | 5.7, 6.1, 1.2 |
| 6.1 phone hangs in the air | `pss.phone_stand`: a dark desk stand, its lip over the phone's foot; the phone stays on its mark | reads as standing |
| 5.7 "crumpled paper" hand | 3 variants (grab / episode 13's `of_cast.phone_grip` held / fist), 2 cold viewers: both picked "held", both found the fingertips "floating beads" → the back of the fingers drawn behind the phone's left edge; the phone 20 px up (case out of the bottom quarter) | `H57 = "held"` |
| 4.2 finger too thick | w 84 → 72 (−15 %) | |
| 6.1 Pam reaches for her phone | tried `reach_up` / `reach_pt` (target 0.92 of reach along the line to the phone, lesson 179): the phone is 3 arm lengths behind and above her, Pam is hidden by Mom, the raised arm reads as Mom's hand. Not used; the case carries the ownership | kept "reach" |
| Bug | `hands_validate()` left gags_v5's UI kit, case and v55 switched on inside `check` v3; now restored | `check` 0, `check v5` 0 |

Board v3 unchanged (git clean). Stills: ps_phones_v3.png.

## Film, scene 1 v1 (25 Nov, `ps_film.py film 1`, 122 drawings, 8.06 s, −15.3 LUFS, AAC true peak −2.3 dB)

Built: `ps_film.py` (of_film's shape: one map, cameras locked to the board's key frames, lips from the take's loudness, bubbles as long as the take, sound from of_sound's synth: rattle ×4 rising, the slam and the slats, the cup's cut clink, room tone). Fixes found in the frames: the falling blind drew a second face (blind_over's gap) → plain slats in the air; board v4's ROOM_V4 froze 1.1's blind half down → `ROOM_OWN` (the film's room); the open mouth sat above the drawn one → on the line.

| Beat | Round 1 (2 viewers, blind frozen) | Round 2 (2 viewers, fixed; viewer D read the memory notes: half-contaminated) |
|---|---|---|
| Tug of war over the blind, the robot wins | 2/2 the blind; the dimming "a glitch" 2/2 | 2/2, the light explained by the blind 2/2 |
| The blind falls on Don | 2/2 | 2/2 |
| 1.2b the three hear the crash, Pam's cup stops | 0/2: "out of nowhere" | 0/2: "a cutaway with no setup" → **staging fault** (nothing moves in it at 4 or 8 fps) |
| "This meeting does not exist." (Don) | 2/2 | 2/2 |
| "My father has a meeting. Without me." (Don), the three react | 1/2 Don | 1/2 Don, 1/2 "can't tell" (Don small in the wide, the tail unreadable); reactions 2/2 |

Shared: the roll in 1.4 read as "a coin / a gold object" (3 of 4).

### Scene 1 v2 (`ps_film_s1_v2_540.mp4`)

Built: 1.2b the three chatting, the crash: heads snap to it, a startle hop, the cup jolts and stops (faces: frozen / stern / surprised, the rigs' own); 1.4a Don close while he speaks (his own camera, the roll in his frame-right hand so it rises clear of his box), then 1.4b the three; dead-zone faults counted only when a prop rests 5 drawings (of_film's held_only: the roll passes the rail in 4).

| Beat | v2 (2 fresh viewers, images only) |
|---|---|
| Tug of war, the robot wins | 2/2 |
| The blind falls on Don | 2/2 |
| 1.2b the three hear the crash | **0/2 a third time** ("a static cutaway"; the 4 fps sheet samples only after the hit) → rule: change the gesture, not its position |
| "This meeting does not exist." | 2/2 |
| "My father has a meeting." is Don's, the roll is tape | 2/2, roll 2/2 "a roll of tape, probably" |

4 of 5 beats: G4 passes. Shared, not a beat: the cut 1.3 → 1.4a read as "another room" 2/2.

### Scene 1 v3 (`ps_film_s1_v3_540.mp4`, Tomas: 1.2b cut, 1.4 opens wide)

Built: 1.2b out, its 0.5 s at the head of 1.3 (the take keeps its time); 1.4 opens on the board's wide (the door, the three, one room) and pushes in to Don (0.20–0.50 s); the box comes on after the push (it hopped three times riding it; 0.35 s late on the line); signs crossing the frame's edge during a camera move count as passing (fewer than 5 drawings).

| Beat | v3 (2 fresh viewers, images only) |
|---|---|
| Tug of war over the blind, the robot wins | 2/2 |
| The blind falls on Don | 2/2 |
| "This meeting does not exist." | 2/2 |
| Same room (the asked question) | 2/2 ("the window glass at the left edge, the floor carries on") |
| Don's line, the three react to it | 2/2 |

5 of 5. Shared, not beats: the roll 0/2 named ("a megaphone? a ring?"; v2 2/2 "tape, probably"); the bent slat across his eye read as "an eyepatch" 2/2 (and in v1).

## Scene 1 v4 and §3.5 (25 Nov, long session, Tomas's /grill-me picks)

- 1.3 "eyepatch" (6 viewers): not a slat. `blind_over` had no new sub-path before the face gap's arc, so it joined the rectangle's corner: a stroke across his eye. `don_ps.BLIND_GAP_FIX` (opt-in). 1.4: the roll's tongue longer, flat, a torn end (`ROLL_TAIL`), kept out of the bottom quarter. `ps_film_s1_v4_540.mp4`.
- §3.5: the rigs return hands unleaned (Don lean, robot tilt, Sofía lean: measured). `ps_scenes.HANDS_DRAWN` (opt-in) returns and logs them where drawn; `hands_drawn_validate()` plants a foreign hand on a leaned wrist: caught with the flag, missed without; wired into `check` ("handsD OK").
- Board v3 md5 checked against a worktree of 5e8bdd9 (the board PNGs are git-ignored, so `git status` can't show them): identical.

## Scene 2 (`ps_film.py film 2`, 310 drawings, 20.7 s, −15.6 LUFS)

Built: 2.1 test D; 2.1b the robot rolls in, SLAP, the card stays; 2.2 a cut-out spin (`ps_set.SPIN`, opt-in), the card on until the spin; 2.3 stamp + the roll pointing in turn; 2.4 Pam's hop over the line; 2.5 salute / half salute / the cup; 2.6 Mom's two stamps; 2.7 the stop mid-step; 2.8 held (HOLDS); 2.9 the robot bobs with its words; 2.10 split (Don, the robot on the line, Don's face close); 2.11 test H. Sound map: screech, beep, SLAP, casters, stamp, landing, heel click, two-tone beep, squeaks, BONK on H's hit. New checks: a shot whose drawings never change fails unless in HOLDS (validated: 2.8 without its entry is caught); signs crossing the edge in a camera move pass (< 5 drawings).

Found in the frames: inserts were redrawn as the room (the camera lock); the card vanished between 2.1b and 2.2.

| Beat | v1 (3 viewers) | v2 (3 fresh viewers) |
|---|---|---|
| Don lays the line, his roll | 2/3; "Pam holds the roll" 2/3 (the board's 2.3 had her beside him before she crosses: continuity fault) | 3/3, roll Don's 3/3 |
| The robot's card, Don spins the tag away | 3/3 spin; the card's author 2/3 | 3/3 |
| Pam sides with Don | 3/3 | 3/3 |
| Mom refuses; Sofía's heel, "border breach" | 3/3 | 3/3 |
| "And you?" / "Both."; the bump, Don worse | asker 1/3; "a blank wall" 3/3 (2.10b's robot at the frame's edge) | asker 3/3; Don worse 3/3 |

5 of 5 (G4). Shared, still open: the haul and the bump read as "the robot zaps him" 6 of 6 across both rounds (the impact strokes read as a spark; the 4 fps sheet misses the haul) — one more round and the rule changes the gesture.

### Scene 2 v3: the ending at 8 fps (2 fresh viewers, the strip 19.0–20.7 s only)

Both: "the robot rolls in and shoves him; the yellow burst is a comic impact flash; Don worse". At 8 fps the "zap" is gone (the 4 fps sheet caught only the burst). Test H v4 has no haul (Tomas, after three misread hauls), so "it rolls into him" is the intended reading. The squeaks and the BONK now follow H v4's timing (roll 0.40 s, hit 0.65 s): `ps_film_s2_v3_540.mp4`.

## Scene 3 (`ps_film.py film 3`, 207 drawings, 13.8 s, −15.7 LUFS)

Built: 3.1–3.2 test E (the arm, FLASH, the photo), 3.1 held on its two lines; 3.3 the robot bobs with "Public post?"; 3.4 his phone-side arm up, sinks onto the phone as it slides in, the pad goes green, back up; 3.5 the approved screen slides up, the post comes in; 3.6 the silhouette's phone lights at DING; 3.7 Pam's eyes to the glow, her mouth opens, the cup up to her chin. Sound: servo, shutter, chime, whoosh, DING (muffled).

| Beat | v1 (3 viewers) |
|---|---|
| The robot takes the photo | 3/3 |
| "Public post?" — Don approves without looking | 3/3 ("rubber-stamp") |
| It's posted, #TeamDon | 3/3 |
| The figure behind the glass sees it | 3/3 a watcher; its glow 2/3 |
| Pam notices, says it into her cup | notices 3/3; the cup as her answer weak ("she doesn't act") |

Shared: "Chin up, Donnie." 3/3 can't tell who says it (Mom, small, behind); 3.5 opened on two dark drawings 2/3 (the second insert painted over the first: fixed, v2).

### Scene 3 v3 (Tomas 25 Nov: "trumpai priartinam prie Mamos", "matomas gurkšnis")

Built: 3.1 cuts in to Mom for "Chin up, Donnie." (its own camera, nudged clear of INVESTOR and the robot's face); 3.7 after her line a sip: the cup up to her mouth, eyes shut, back down a little, a small slurp.

| Question (2 fresh viewers, 4 fps sheet) | v3 |
|---|---|
| Who says "Chin up, Donnie." | 2/2 Mom |
| What Pam does with the cup | 0/2: "a phone, a selfie / photographing the pose" |

The blue mug at her face reads as a phone (the episode's other prop), the sip falls on one 4 fps drawing. Steam off the rim was tried and dropped: from the drawn hand point it either crossed her eyes or floated off the mug (not converging, rule 5).

### Scene 3 v4 (Tomas: "1", the longer sip)

3.7 +0.40 s; the sip held 0.36 s at her mouth (two 4 fps drawings), eyes up into the cup, two slurps. 2 fresh viewers: 0/2, "she raises a phone, photographs / checks the post". Third round the cup reads as a phone → the rule changes the gesture or the prop (Tomas's call: Pam's mug is part of her look).
Tomas 25 Nov: the silence without the sip (`SIP_ON = False`, the board's cup at her chin); scene 3 v5 = v3 without the sip. 4.3: Father's take 0.4 s later (plan v2 §7).

## Scene 4 (`ps_film.py film 4`, 92 drawings, 6.1 s with Father's take +0.4 s, −15.5 LUFS)

Built (plan v2 §7): 4.1 the neon's flicker, the black sleeve lifts the #TeamDon phone (`BRIDGE_DROP`); 4.2 motion test J; 4.3 the board's three framings in turn: 4.3a "That one.", 4.3b the guards turn and pinch (`PINCH_43` 0→1 from the rig's GUARD_POSE to the board's pinch, in 0.20 s), the stink lines rise all through (`STINK_RISE`), 4.3c "Invite her." Sound: the club's bass, the neon's hum, the smudge, a sniff, the send.

| Beat (3 fresh viewers, scene 3's sheet before it for context) | v1 |
|---|---|
| A casino back room; the photo came by Don's public post | 3/3 |
| The finger picks the blonde in the white coat | 3/3 (whose finger: "the scruffy man's, probably" 3/3) |
| The guards hold their noses: the Client stinks | 3/3 |
| Father decides: "Invite her." | 3/3 |
| Father doesn't react to the smell | 3/3 |

5 of 5. Shared, not beats: the cut 4.3b → 4.3c "same room?" 3/3 unsure.

### Scene 4 v2–v3 (outside review 26 Nov, 7.5/10; Tomas "proceed"; rules §0 this time)

- **The pinch (§0):** `hands_ps` has no pinch. `dh_cast.FRONT_HAND` (opt-in) draws the series' hand on the guard's face arm, backed down its forearm (`FRONT_HAND_BACK`) so the fingertips, not the knuckles, land on the nose; a sheet of 8 shapes. Silhouettes don't work here (the hand is in front of a black suit: all black, as logged before), so the 3 variants (palm, beckon, the rig's ball) went to 2 viewers in colour at feed size: split (palm best 1, the ball best 1), "a boxing glove", "a paddle with lines", "pointing / shh". No existing shape reads as a pinch → a new shape is needed (asked Tomas). Unchanged in the film.
- **4.1:** 5.7's grip (palm under the phone's foot, the backs of the fingers behind its left edge), the phone +20 % (`BRIDGE_V2`): "a hand round the phone" 3/3.
- **4.2:** the photo 35 % closer (`ZOOM_42`). v2: the finger still landed on her coat 3/3 — the measured offsets (100 px, 46 px) didn't scale with the zoom; v3 scales them and moves the photo so her heels sit under the `point_t` tip: "her shoe / foot" 2/2.
- **4.3:** stink lines off the Client's head, each its own width and phase (`STINK_V2`); Father +12 % (`FATHER_V2`, framed left to keep the phone off the rail), 0.38 s of silence before "Invite her." (his take +0.25 s): "in charge" 3/3.
- Disagreed (logged in the reply): one guard turning instead of both (undoes Tomas's mirrored pick); filling the bottom quarter (the platforms' captions).
- Open: "That one." speaker 2/3 unclear (the table's clutter).
- **The pinch, v4 (Tomas: a new shape):** `hands_ps` "pinch" (opt-in, a new name: no other shape changes): the thumb and the index meet at the tips, the other three curled. 3 variants at feed size (the rig's ball, pinch backed 1.2, pinch backed 1.0), 2 viewers: both "the pinch reads, the ball is a mask / mitten"; best 1.2 and 1.0 one each, 1.0 "a clump" → 1.2. 10 fps strip of the encoded file (3.9–4.6 s): no jumps. `ps_film_s4_v4_540.mp4`.

## Audit 26 Nov: all sheets, hands and palms (scene 4 v7)

| # | Found | Cause | Fix | Check |
|---|---|---|---|---|
| E1 | Guards: a double hand on the pinching wrist | The pinch hand was drawn on top of the rig's own ball and backed down the forearm: two geometries at one wrist | `dh_cast.FRONT_HAND` hook through `limb` (kit.HAND): one hand per wrist, the cuff over the joint | 2/2 "normal hands"; hand_gate 0 |
| E2 | The pinch read as "pressing the earpiece" (2/2) | The hand sat at the cheek/ear side (rules §1: hand at the ear = a call) | PINCH_POSE (-80, -87), FRONT_HAND_S 0.9: the fingers on the nose under the glasses, forearm upright | 2/2 "pinches the bridge of the nose, under the glasses" |
| E2b | The in-between read as a stretched "noodle" arm (2/2) | Linear interpolation of both angles swung the straight arm out sideways | `PINCH_LEAD` 1.6 (opt-in): the forearm folds first, the hand rises up the chest | 2/2 gone; 10 fps strip of v7 clean |
| E2c | The other hand at the belt read as "an extra fist" (2/2) | Clasped, the front hand covered it; alone it was the rig's bare ball, the cuff apart from it | `dh_cast.BACK_HAND` "quiet" (opt-in while ARM_FRONT is set) | 2/2 count two hands, hanging |
| E3 | The Client's grey palm on his shirt read as "a floating hand" by some | Not a fault: the approved oily palm print (client_ps overlay, v2 review) | Not changed: Tomas's call | 4/6 viewers read it as a stain |
| E4 | Pam's mug: an extra thumb | The sip-era thumb capsule left on | pm_ps.MUG_THUMB off | rebuilt s1 v5, s3 v6 |

check / check v5: 38 shots, 0 faults each. Board defaults unchanged (PINCH_LEAD 1.0, BACK_HAND None).

## Scene 4 v8: review 7.8/10 (26 Nov), Tomas: different gestures, longer close

| Point | Fix (opt-in, film only) | Cold test |
|---|---|---|
| Client's hand "a brown fist, no index" | `client_ps.POINT_V2`: skin, index long, three curled as one block, thumb over; `POINT_SKIN` (0.86, 0.64, 0.50), `POINT_W` 1.3; the hand on the phone screen, index on the purple figure (`POINT_43`, `AIM43`) | 2/2 "a pointing index finger" (round 1: 2/2 "a stick/cigar"). Open: 2/2 "points vaguely up-left, no clear target"; 1/2 still "stick-like" |
| Guards' fingers tangled | `hands_ps.PINCH_V2`: index and thumb straight, the others in the palm | 2/2 nose pinch; at feed size still "blobby" 1/2 |
| Different gestures (Tomas) | `GUARD_B` / `dh_cast.GUARD_TURN` (new: face slid in the head, tilt): B turns his head away, palm over mouth and nose, 0.4 s after A | Variants (417): folded / palm up / palm at chest read 0/2 as smell (wave, stop, nervous); palm over mouth+nose 2/2 "different from the pinch" |
| Longer reaction | 4.3b 0.95 s (B_43 1.90), Father's take +0.45 s; a muffled huff for B | |
| #TeamDon photo small, cut | `SHOT43_V8`: phone 1.45, whole in the frame (x 244) | |
| Bubble over hand and photo | "That one." in two rows (`NARROW_43` 84), it fits on his right | 2/2 the Client says it (was 2/3 unclear) |
| 4.3a→4.3b a near-identical reframe | 4.3b in 4.3a's camera (no cut) | |
| Not done (disagree) | table lower 25–30 %, captions at the bottom: y > 720 is the app's UI | |

check / check v5: 38 / 0 each. Board v4 md5-identical (44 frames, against a315cc5).

## Scene 4 v9 stills: review 6.5/10 (26 Nov), "proceed"

- **The table phone shows the team photo** (`PHOTO_43`, `_phone_photo`: 3.1's `rp.team_photo`, as 4.1 and 4.2), not four bars. Phone 1.3 at x 240, whole in the frame.
- **The Client's index ends at Sofía** (`HAND_OFF43` (60, 38), `POINT_LEN` 0.85). Five other hand places folded the arm into a lump (his shoulder is beside the phone: rule "keep the target in reach"); from above, the sleeve drew over the finger.
- **4.3c**: the guard and the phone dimmed 35 % behind Father (`FATHER_SPOT`), Father lit.
- Hand sheet `ps_s4_hand_sheet_v1.png`: guard A's hand at the nose in five shapes, for Tomas's pick. Film v9 after it.
- Not done (Tomas has not answered): different guard faces, neon rim light. Disagreed: table lower, stink lines.
- check / check v5 38 / 0; board v4 md5-identical. No cold test on these stills yet.

## Scene 4 v9 film: the hand-sheet review (26 Nov), "proceed"

- **Cause of "lines across the hand" (all five variants):** `dh_cast` drew the clasped hand's three finger strokes at the wrist of side 1 whatever hand was there. Off when a hands_ps hand is hooked (`not hook`). 2/2 "no stray lines".
- **Pinch v3** (`hands_ps.PINCH_V3`): a C, the index round one side, the thumb's pad round the other, the three curled as one block with two lines, the nose's tip red between the tips, a contact shadow. Hand 0.8, PINCH_POSE (-73, -93). Not done: another skin colour for the hand (one skin for the cast).
- Cold test of the encoded v9 at feed size (2 viewers): the photo on the phone and his point at it 2/2; Father the most important 2/2; no stray lines, no extra hand, no call 2/2. **Open: the pinch reads as "a fist to the nose or mouth" 2/2, and the two guards as "the same gesture" 2/2**: a guard's face is about 45 px wide at feed size, the fingers cannot be told apart there. The smell reads from the stink lines.
- check / check v5 38 / 0; board v4 md5-identical.

## Scene 4 v10: review FAIL "a pink lump, the nose not squeezed" (26 Nov), "proceed"

- **`dh_cast.NOSE_PINCH`** (a face state, opt-in, guard A only via `ps.NOSE_43`): the nose's lower half redrawn a quarter narrower, nostrils as slits, a crease each side.
- **Pinch v4** (`hands_ps.PINCH_V4`): a clamp, index one side, thumb the other, the three curled as one block with one line; no red tip, no shadow blob.
- **`dh_cast.FRONT_HAND_AIM`**: the hand turns at the wrist to the nose point (rig units) and is sized so the clamp lands on it: measured, not nudged (three rounds of pose nudging never put it on the nose).
- Cold test of the encoded v10 (2 viewers, feed-size strip + one full-size frame): **"pinches his nose with index and thumb" 2/2** at both sizes (v9: 0/2 "a fist"); no stray lines, lump, extra hand or call 2/2. Open: **2/2 "could read as a horns / rock-on sign at a glance"**; the guards "the same action" 2/2 at feed size.
- Stopped here as planned (one sheet, one test). check / check v5 38 / 0; board v4 md5-identical.

## Scene 4 v11: the pinch's tips closed (Tomas 26 Nov: "1 padarom, 2 paliekam")

- `hands_ps.PINCH_CLOSE` 1.0: the index's and thumb's tips meet over the nose (a loop round it), no open V. 0 restores v10.
- Cold test of the encoded v11 (2 viewers, feed-size strip + one full frame): "pinches his nose with index and thumb, a bad smell" 2/2; "no horns, no OK sign, no call, no stray lines, no extra hand" 2/2 (v10: horns 2/2). Note 1/2: at feed size the hand "could be a fist or a lump at the nose", read right from the stink lines.
- Guards A / B left as they are (Tomas). check / check v5 38 / 0; board v4 md5-identical.

## Scene 4 LOCKED at v11 (Tomas, 26 Nov)

Tag `uptimez-pick-a-side-s4-v11` (local: the push of tags is refused by the session's proxy, 403). After scene 5's code, scene 4 v11 re-rendered from the tag's tree and from the branch: md5-identical (be72e2a2…).

## Scene 5 (26 Nov): v1 → v3

Shots: 5.1 the silhouette, his phone lights (3.6's) · 5.2 the gold pen writes H, R, ? a letter at a time (`sofia_ps.CV_N`, the hand moving on) · 5.3a the board, 5.3b the can comes up from his hand, then the heart (`HEART_53`) · 5.4a wide 0.85 s, then test C · 5.5 test K · 5.6 test F's staging · 5.7 the phone shakes with its buzz. Sound: buzz, a scratch per letter, three knocks, a clink and a chime, heels, buzz.

| Beat | v1 (2 viewers, 4 fps sheets) | v2 / v3 |
|---|---|---|
| The pen writes HR? on the CV, a black sleeve | 2/2 | |
| The oil can, the heart | 2/2 | |
| Don's foot over the line and back, the vest | 2/2 the foot; 1/2 "content to have crossed" | |
| Sofía holds HR? at the line (5.5) | 2/2 | |
| Sofía crosses the tape (5.6) | **0/2** (hidden by Pam's box) | v2: **2/2** "crosses left to right" |
| Pam's line is spoken | **0/2** ("a sign she holds": a six-row narrow box by her raised arms) | v2: 2/2 "she speaks" |
| Pam's phone, INVITATION · DAD | 2/2 | 2/2 |
| 5.1 who is outside | 2/2 "a figure in sunglasses", the phone's glow "a scan" 2/2 | not changed: 3.6 sets it up in the film |

- v2: 5.6's own camera (lower, wider), Sofía's walk above Pam's box, Pam 70 px lower (`PAM_DY_56`), the box in two rows on her right.
- v2 found: when the box went, the floor's "← DON" under it read as "signed - DON" 2/2. v3: the box stays to the cut (`BOX_TO_END`); her walk starts 72 left of the tape (5.5 ends on it: "a jump" 1/2 at 128). v3 not cold-tested (the scene's third version).
- Open: Sofía has no CV in 5.6's wide (test F's cast); 5.6's first drawing still shows the floor's DON before the box.
- check / check v5 38 / 0; board v4 md5-identical.

## Scene 5 v5: review 7.5/10 (26 Nov), "what correlates", "proceed"

Applies (rules-hands §0): 224 (the object, then the fingers over it), 208 (one hand per wrist), 149/224 (a real knee), 178 (three misreads: change the gesture), 163 (a face beats a gesture).

- **5.6** `STOOL_56` (the stool in frame, Pam 40 px up, the camera 86 lower so Sofía's walk stays above her box), `pm_ps.BLIND_W` 26 (the blind wider than her hands, darker slats, ladder strings, pull cord, a stack of slats under the rail). The shot's switches are set only while its near layer draws.
- **5.1** `ps_set.GLASS_PHONE_V2` (scene 5 only; 3.6 keeps its tested look): a phone's body and screen in his fist, the glow on his face.
- Cold test of v4 (2 viewers, feed size): the phone "a phone, he looks at it" **2/2** (v1: "a scan" 2/2); "stands on a step stool" **2/2**; Sofía left of the line → right of it 2/2; Pam speaks 2/2. **Open: "holds a grey bar or shelf" 2/2, the blind not named** (the stack of slats added after this test, v5, not tested).
- For Tomas's pick, not in the film: `ps_s5_leg_sheet_v1.png` (`don_ps.LEG`, four legs), `ps_s5_grip_sheet_v1.png` (`PEN_HAND` fist / pinch / grab; the can as it is; `CV_FINGERS`; `ps_set.ARC_K` 0.6).
- Scene 3 v6 and scene 4 v11 re-rendered from their commits and from the branch: md5-identical. check / check v5 38 / 0; board v4 md5-identical.
