# One Star v14: physical action and the hands round (25 Nov)

Rough cut `one_star_rough_v14c.mp4` (1080×1920, 64.75 s, 1948 frames, not committed); preview `one_star_rough_v14c_540.mp4`.
Rebuild from `uptimez/src`: `python3 cs_film_v14.py ../customer-success` (scenes 1, 2, 3, 4, 6; 5 as v13), then the film
as `rough_v14c`.

## Tomas's picks (/grill-me)

| Beat | v14 |
|---|---|
| 0:00 first joke | The buzz throws Don's phone out of his hands, it bounces off the robot's head, the robot catches it, ★ 1/5 on its visor; then the wide, every head on Don (`cs_scene1_v14.py`) |
| 1.4 | Don presses without looking: the antenna first (it twangs), then the visor, "Approved."; then the robot tosses his phone back and he catches it without a look (+8 drawings) |
| 3.1 / 3.1b | The sheet shoots out faster than his hand, his fist shuts on air; new insert: the roll trundles to the glass door and bumps it |
| 3.5 / 3.5b | The Client's plan balled in his raised fist, "Is this a joke?", the throw; PLOK on Don's forehead, the ball drops, he freezes, an eye twitching |
| End | The phones buzz again; Don clamps his to his chest with both hands (the loop's answer to 0:00) |
| Screens | The post's rating is one big gold ★ and "1/5", the same mark as the flying phone, the visor and Sofía's tablet; the UPDATE keeps it |

## Hands (rules page, lessons 163, 178, 179, 224, 231)

- 2.1: the phone at the ear folded his arm over his head (ear 28 units from a 58-unit arm's shoulder). The phone is held in front (the 2.2 insert is that screen); the mic is down from the start, no flick, the free hand at his side.
- 4.1: one size for Pam's hand (1.3×); STOP palm, one finger at her temple for the glasses, back out and down folded (an angle blend swung the forearm level at him, and the drop crossed her eyes).
- 4.2b: her finger aims above his pocket, clear of his hand.
- 6.3: her arm from her own shoulder, the elbow out, a darker sleeve with an edge, the series' hand round the phone; her other hand on the counter.

## QA

-15.6 LUFS, -1.9 dBFS. Speech 14/16: "Still one star." misses as in v13; Don's 1.4 "Approved." (ep 10's take) is heard as "Approve." in all v14 mixes (v13: 2/3). Music back 0.75 s after it and the tick moved off it did not help: listen.

## v16: the last polish before the render (25 Nov, /grill-me "what is left to polish")

Rebuild: `python3 cs_film_v16.py ../customer-success 2` (1080 master `rough_v16`); `python3 cs_film_v16.py OUT 1` is the
540 film the gates ran on, compared with the master frame by frame (PSNR). Cover: `python3 cs_cover.py v2` →
`one_star_cover_v2.png` (the opening's frame, Don's shock and the visor's ★ 1/5; the title band with the film's mark).

| Pick | Done |
|---|---|
| "Still one star." re-recorded | Not a reading fault: alone in the mix 3/3; with Pam's line before it (the checker's context window) 1/3. Six new reads, pauses included, did worse ("Still in Star 1 Star"). The same take +3 dB (film_v10): 3/3 in both, -11 dB like "Nine o'clock." Tomas chose it by ear. |
| 0:19 Don's finger at the visor | POINT_AT (418, 706), GRAB_AT (410, 730): the point and the fist stop ~15 px clear of the visor (it touched on d2–d5) |
| 0:49 Pam's pen hand | Her purple sleeve with a cuff from the top edge to the hand (a bare stub read as nobody's); the pen shorter, its end over her hand |
| 0:49 at 1080 (found by the PSNR check) | The pen hand was placed at HALF its place in the master: `user_to_device / HI` on a scratch surface without the device scale. At 540 it wrote on the tape; at 1080 it hung above it (so the v15 master too). Now `device_to_user`, the same at both sizes |
| Open palm | Fingers of unequal length (index, middle, ring, pinky; the pinky thinner), `hands_ps.PALM_VAR`, on in One Star only |

Review of the stills: 8.5/10, GO; "no more hand redesign" (thumb root, sausage-like fingers, the pinch point: cosmetic at 9:16).

Lesson: when a line is lost in the mix, measure it alone and in its context window before re-recording; here the level
was the fault, not the read.

QA v16 (1080 master, 1996 frames, 66.33 s): -15.6 LUFS, -2.3 dBFS; bubbles 12, 0 faults; hand and elbow gates 0 at 1080.
Speech 15/16: "Still one star." 3/3; Don's 1.4 "Approved." still "Approve." (Tomas listens). PSNR master vs 540 film:
average 35.0 dB; after the 5.2 fix the dips are text and line hinting only (phone posts ~29 dB, checked by difference images).
The 540 build reports 8 hand-gate faults on 6.6 d2/d8 ("a rig hand under the phone"), also in v15 at 540, none at 1080;
the two pictures are the same (the gate's scale, not the drawing): open.

## G4 cold mute test on rough_v16 (two fresh viewers, 4 fps sheets with the bubbles)

Both told back all five beats (the review and the robot's ★ 1/5; "Approved." unread → "Stupid human."; the AI plan →
"Is this a joke?" and the throw; Pam finds piece 7, "Your number."; still one star). PASS. Both would screenshot the
"99% CONFIDENT" plan. Both flagged, for the next episode (Tomas merged as is):
- 4.4 the green arrow from Pam to HUMAN✓ reads as a rope tying her to the sign;
- 1.4 Don's arm straight to the visor and 4.2b Pam's pointing arm across to his pocket read as poles;
- 3.1b the roll bumps "a post": the glass door does not read as a door;
- 5.2 the sleeve from the corner: A "pole-like", B "acceptable for an insert".

## v17: the cold test's notes (25 Nov, /grill-me)

Rebuild: `python3 cs_film_v17.py ../customer-success 2` (master `rough_v17`), `python3 cs_film_v17.py OUT 1` for the PSNR check.
All behind `cs_v17.install()`; v16 rebuilds as before.

| Pick | Done |
|---|---|
| 4.4 the green arrow | Gone; the HUMAN✓ paddle leans to Pam after it turns (`cs_v15e.NO_ARROW44`) |
| 1.4 Don's arm a pole | He leans in 8 and presses with the elbow up, out of his body's outline (the upper arm had been hidden on his white shirt, so only a level forearm showed). The swings from and back to rest blend the joint angles: an IK flip there jumped (`cs_v14.angles14`, ELBOW14, LEAN14) |
| 4.2b Pam's arm a pole | The elbow at her side, the forearm and finger up at his pocket (`cs_scene4.ELBOW42b` = 20°) |
| 3.1b "a post" | The glass door has a pull handle, a kick rail, glints and a PUSH sticker (`cs_v14.DOOR31b`) |
| 5.2 sleeve | The insert 120 higher, so her sleeve from the top edge is short (`cs_grips.SHIFT52`; the plan's floor carried on below) |
| 6.6 gate at 540 | The hand logs and the gate in frame units (540 wide) whatever surface draws: at 1080 half the passes draw on a 540 scratch surface, so 14 x HI was 28 units there and 14 at 540. Now 16 kept out, 13 the gate; 0 faults at both sizes |
| "Approved." | Not re-recorded: alone 3/3 for every take; after the robot's "...approval required." Whisper writes "Approve." for the old take, four new reads at 0 and +3 dB, and with the music back at 0.05, 0.9 or 1.6 s. Its language model, not the take: Tomas listens |

QA v17 master: 1996 frames, -15.6 LUFS, -2.3 dBFS, bubbles 12/0, hand and elbow gates 0 at 1080 and 540; PSNR vs the 540
film 35.0 average, no shot dips below v16; speech 15/16 ("Approved." as above).

## v18: the cold viewers' remaining notes (25 Nov evening, /grill-me)

Rebuild: `python3 cs_film_v18.py ../customer-success 2`; all behind `cs_v18.install()`.

| Pick | Done |
|---|---|
| 0:01 the phone jumped from his hands into the air | One in-between drawing: his hands rising (-100, -90, 100, 90), the phone just off his left fist, beside his head, not over it. The wide gives up its last drawing, so the film's clock is v17's |
| 0:32 the throw a pole | After the release the arm goes on down and bends (FOLLOW35 (-10, 5, 40, 70) over 0.25 s) |
| 0:55 a knot of arms, "a blue pole" | 6.1: one hand holds the phone at his chest, the other hangs; the roll is gone |
| 1:04 his hands changed every drawing | 6.6a clamped by d5 and still (no jitter); the buzz zigzags outside his hands |
| 0:13 a lone calendar | 2.1 opens on Don (no wall calendar first) |
| 0:36 an empty desk | 4.2 the plan already sliding in at d0 (LEAD42 5) |
| 0:43 a blank grey sign | 4.4 HUMAN✓ turned by d2 (FLIP44 (0, 2)) |
| 1:03 her phone jumped up | 6.5 up over 5 drawings |
| The 7 in his pocket | Left as is (the joke: he lost it himself) |

8 fps check of the toss, the throw and the hit, and the loop (the FRI wide → Don's buzzing phone): as intended.
Speech 15/16 ("Approved." as before). The check is fragile: moving the Client's 1.2 line by 1/12 s changed the mix
by about -32 dB around 15 s and Whisper lost "Nine o'clock." and "Still one star."; with LINE12 back at 1.42 both pass
at 2/3. Before release: two or three people with sound, on a phone.

## v19: the post goes viral (26 Nov, Tomas: "0:02 counts from 0.1K: not convincing, no speed or dynamics")

`python3 cs_film_v19.py ../customer-success 2` (only scene 1 changes; `cs_os19.install()`. Note: `cs_v19.py` is another
episode's module, hence `os19`). 1.2's reactions count now accelerates, 1.2K → 48K exponentially by 0:05.5, a new
number every drawing (v13 eased out, 0.3K → 2.4K, slowing). Past 10K it turns red and bold with a bump. Reaction dots
fly up out of the three dots, more and more of them. Speech 15/16 as in v18.

v19a (review 8/10, "polish and ship"): the dots read as confetti, so the row and the flying reactions are angry,
laughing and thumbs-down faces (drawn, no emoji font). Past 10K the number is red and bold and grows to 135% at 48K,
with a pulse at 10K and on 48K. The row sits 18 higher. Notification pops come closer and closer (16, accelerating),
with a low thud on 48K. Speech still 15/16; 1.2 is heard 3/3 under the pops.

## v20: the frame-by-frame hand audit (26 Nov; Tomas: not ready to publish, hands, elbows, fingers)

`python3 cs_film_v20.py ../customer-success 2`; all behind `cs_os20.install()`.

Why the lessons were not used: the gates only measured geometry (a rig hand under a grip, the thumb's side, an
elbow's bend), and the fixes were checked on crops. The rules that failed had no gate: an insert arm without its
owner (224/225), a phone that appears, a key word under a finger, an empty band in the frame.

| Shot | v19 | v20 |
|---|---|---|
| 4.3s 0:41 | a long olive sleeve from the bottom to mid-frame, a fist over half the 7 | over his shoulder (fs_film31's back of his head), his own arm with an elbow, thumb in front below the 7, fingertips round the far edge |
| 4.3a 0:40 | the strip in a fist with watch and badge, one lump | his three fingers across its back, the heel past its edge; brows up ("dawning") |
| 5.1 0:46 | the phone appears in his hand | in his hand from d0; Sofía's side-eye at Pam from d14 |
| 5.2 0:49-0:51 | an empty dark lower half (v17), a thick pen, a tiny ownerless NEW CONTACT phone | v16's plan filling the frame (1.6 on the tape), a thinner pen in a readable tripod, a short sleeve at the edge, a shadow under the paper, no phone |
| 5.3 0:52 | the finger over SAVE; "note: finds things" small; SAVED 0.6 s | the tap right of the word; "finds things" 35 % bigger under a small "note:"; SAVED 1.5 s (the shot 11 drawings longer) |
| 1.1, 1.4 | the robot's phone on the end of its stick | in its claw |
| 3.3, 3.4b, 4.1 | four equal capsules | unequal tapered fingers (clutch); a fist round Pam's tube (handle_grip) |
| 6.6a | phone and hands one black blob | the phone's rim and lenses |
| 4.2, 4.3w | every bay as loud as the 7 | the other bays toned down 38 %, the 7 and the title bright |
| 5.2a | a frozen face | a closed smile and a blush from d7 |
| plant | green spears over feet | 20 % smaller, round leaves, a pot's rim |
| bezels | thick | thinner on the full-frame phones |

Kept: the robot's line ("The result was obtained by a h-human.", recorded). Gates: hand 0, elbow 0, insert 0,
flat-band 0 (3.1b, 3.2a, 3.5, 6.3 at 30-40 %: a wall or a floor, looked at). Speech 14/16: "Approved." as before, and
"Still one star." heard alone every time but lost in its context window whatever its level or place (+1.5, +3 dB,
+0.15 s tried): Whisper, not the mix. Film 67.25 s.

## v21: the three last corrections (26 Nov; review of v20 8.7/10, "only these three, then QA and publish")

`python3 cs_film_v21.py ../customer-success 2` (`cs_os21.install()`).
- P0 5.2: the pen in a tripod: the index finger along its top to near the tip (with a nail), the thumb on its lower side,
  the middle finger under it; the tip ON the last stroke written (v20: "a fist round the pen").
- P1 5.3: SAVE blue and active before the tap (grey read "disabled"), a darker blue when pressed, green SAVED after.
- P1 4.2/4.3w: the other bays a further 25 % down, a soft light rim round bay 7.
QA: 2020 frames, -15.6 LUFS; bubbles 12/0; hand, elbow, insert and flat-band gates 0; PSNR 35.1; speech 14/16 as v20.

## v22: 0:11 the feed scrolls; Pam's "Wait." (26 Nov)

`python3 cs_film_v22.py ../customer-success 2` (`cs_os22.install()`, voices `cs_voices/film_v11`).
- 1.4b: the reply no longer slides up over the reactions: the feed scrolls up 96 (the header leaves whole) and the
  reply comes in under the 48K row. The row outside 1.2 now shows 1.2's end (48K, red); it showed 1.2K. The clown
  +18 %, "We value every client's journey..." 22 px at 80 % (was 20 px at 45 %).
- 4.1: Pam's "Wait." (voice A, take a, Tomas's pick) with her STOP palm, the bubble over her head. Heard 3/3.
- cs_scene4.schedule returns its lines in time order (the speech check segfaulted on 4.2p before 4.1p).
QA: 2020 frames, -15.6 LUFS; bubbles 13/0; hand, elbow, insert, flat-band gates 0; PSNR 35.1; speech 15/17
("Approved." and "Still one star." in its context window, as before).
