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
