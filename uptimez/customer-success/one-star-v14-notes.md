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
