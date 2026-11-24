# Daddy's Home, scene 3 (The Green Star): shot list v2, the pilot

24 Nov. For approval before any drawing. Built from script v2 (scene 3, 0:22.4, 11.4 s), the v7 audit and `daddys-home-restaging-lessons-v1.md` (numbers in brackets point to its lessons). v7 stays as it is; this becomes `dh_film_v8` behind a flag.

## What stays fixed

- **Every line at its v7 time and every take unchanged**, so the mix, the lip-sync and the Whisper checks stay valid [4, 5].
- **Scene length 11.4 s**, the cut into scene 4 at 0:33.9.
- **Protect list (scene 3):**
  1. "Make it green." with Don pointing at the screen with one red star, 1/5.
  2. "Human approval required.": the robot's same polite face.
  3. "Approved.": his thumb on the pad before the robot's last word, the ketchup cuff, and he isn't looking.
  4. The huge green star, the happy chime, the four grey stars, still 1/5, the robot's small nod. The v7 drawing is kept.
  5. "It's still one.": Pam flat, looking at the screen.
  6. "Green is all he sees.": Don's fist up, meant kindly.
  7. Mom's thump on the gold arm (PFFT, the seat comes back up) and "He once fired a man... for sitting in that chair."
  8. Sofía sits, smooths her skirt, then explodes out: the clipboard one way, the throne the other.
  9. "Different chair.": Mom still scrubbing, Sofía frozen behind her.
  10. The $49,999 tag and the phone on the throne's arm: whole or out of frame, never cut.

## The shots: 10 in v7, 7 in v2

Sizes are measured as the biggest face radius at 540 wide: CU ≥ 120, MCU ≥ 95, MS ≥ 64 [10]. Bubbles stay at the top, over clear wall above the heads [13].

| v2 | v7 | At | s | Setup and size | Picture | Foreground | Hands | Lines |
|---|---|---|---|---|---|---|---|---|
| **3A** | 3.1 + 3.2 | 0:22.4 | 2.60 | A, at the robot's height, over Don's shoulder. MS, pushing in to MCU on the robot from 0:23.7 | Don, seen from behind, points up at the screen. The robot under the screen turns its face to him. The push ends with the screen whole at the top left and the bubbles over the wall at the top right [11, 12, 16]. | Don's back and shoulder, cut by the left edge [8] | Don: point, then relax as the robot answers | DON "Make it green." · ROBOT "Human approval required." |
| **3B** | 3.3 | 0:25.0 | 0.50 | Insert (kept) | His thumb on the pad, the ketchup cuff behind it. | His sleeve coming in from the right | The series hand pressing with the thumb, not a pale block | DON "Approved." |
| **3B'** | 3.3' | 0:25.5 | 0.80 | Insert (the v7 drawing kept) | The green star, the chime, 1/5, the robot's nod. | The robot's head, cut by the bottom edge | — | — |
| **3C** | 3.4 | 0:26.3 | 1.20 | S6, the counter's end, a little low. MCU, r ≥ 95 (v7: 64) | Pam behind the counter, looking up and left, flat. **A small green glow on her glasses**, so the star is in her frame [16]. | The counter top and the coffee machine's side, cut by the right edge | Pam: quiet, both hands on the counter | PAM "It's still one." |
| **3D** | 3.5 | 0:27.5 | 1.75 | Don where 3A left him, low, under him. CU, r ≥ 120 (v7: 84) | Don's fist up, his eyes going right to Pam, beaming. The green light on him. The first close-up in the film is the turn: he believes it [2]. | The robot's antenna and head, cut by the left edge: the same people as in 3A | Don: fist | DON "Green is all he sees." |
| **3E** | 4.1 + 4.1' + 4.2 | 0:29.3 | 3.10 | S3, B front. One held frame with three drawings; the camera does not move between them (v7 moved it 366→400). MS, Mom r ≥ 75 (v7: 61) | (a) Mom comes in, thumps the arm: PFFT. (b) Sofía walks in and sits, smoothing her skirt; Mom scrubs without looking. (c) Sofía explodes up, the clipboard flies left, the throne rolls right. | The shredder's body, cut by the left edge (its sign out of frame) | Mom: grab on her cloth; Sofía: palm on her skirt, then both palms up | MOM "He once fired a man..." · "...for sitting in that chair." |
| **3F** | 4.3 | 0:32.4 | 1.50 | B, closer. MCU on Mom, r ≥ 95 | Mom has followed the throne and scrubs on, eyes on the arm. Sofía behind her, frozen, looking at Mom [15]. | The throne's gold arm, cut by the bottom-right corner, tag and phone out of frame | Mom: grab on the cloth, scrubbing | MOM "Different chair." |

## What the gates should say afterwards

| Gate | v7, scene 3 | v2 target |
|---|---|---|
| Shots | 10, mean 1.14 s | 7, mean 1.64 s, none under 0.5 s |
| Sizes | MS 6, insert 2, WS 2 (nothing at MCU or CU) | CU 1, MCU 3, MS 1, insert 2 |
| Lone small figures | robot (3.2), Pam (3.4) | none: the robot shares 3A with Don, and Pam is at MCU |
| Foreground | 1 of 8 people shots | 5 of 5 |
| Bubble tails | pass | pass (`dh_tailcheck` on every new shot) |
| `dh_baseline check` | — | "same" for scenes 1–8 (v7 untouched) |

## Two decisions before drawing

1. **Don from behind (3A).** No rig of his back exists yet; only the Client's (`sb._client_back`) and the robot's. Recommended: draw a small new piece for Don's back (bald head, headset band, vest), opt-in, used only for over-the-shoulder shots. Fallback: Don in three-quarter view, cut by the left edge, with his pointing arm reaching to the screen.
2. **3E to 3F: a cut or a pan.** Recommended: a cut in to Mom for "Different chair." (the punchline gets the closer shot). Alternative: one 4.6 s shot that pans after the rolling throne and ends on the two of them.

## Then

After approval: six full-size frames (3A start and end, 3C, 3D, 3E c, 3F) for your look before any animation; then the scene animated, the gates and `dh_baseline check`, then a cold mute test on v7's and v8's scene 3.

## Frames, round 2 (24 Nov): what changed against the table above

Drawn by `src/dh_s3_v8.py` (with `src/dh_back.py`, Don from behind, and the new opt-in hand shape `point_s` in `hands_ps.py`; v3 pinned as `hands_ps_v3.py`).

- **The screen hangs to the robot's right**, not over it: over the robot, both bubbles' tails had to cross the screen.
- **3A ends at MS** (robot r 60 → 64), not MCU: any closer and the screen is cut.
- **3E** is MS (Mom r 61) and has no foreground: Mom, Sofía in the air and the whole $49,999 tag only fit at this size. The throne rolls a shorter way, on its casters, with three short lines behind it.
- **3F** Mom r 89 (MCU is 95); Sofía stands further back, her face clear above Mom's shoulder. The bubble sits at mouth height over Sofía's jacket.
- Measured: 3C Pam r 100 (MCU), 3D Don r 120 (CU).
- Bubbles are placed by hand; `dh_say` places the real ones.
- `dh_baseline check`, each scene run on its own: all eight "same". A single run over all eight shows 7|9.3 as different with the old hand file as well, so state carries between scenes in one process; the check is run per scene.

## Round 3 (24 Nov): the voice, the tails, the cold test

- **"Make it green." approved** (Tomas, 24 Nov): `src/dh_voices/film_v8/3.1.wav`, used by v8 only. Don's voice says a phrase-final "green" as "groan" (vowel F2 1219 Hz in 22 spellings and phoneme strings); the new take keeps the old "Make it" and a "green" cut from the front of "Green ones." (F2 1979 Hz). Whisper hears "Make it green." 3/3, alone and in the mix.
- **"Green is all he sees."**: the take was fine; the fist's whoosh 0.05 s before it made Whisper hear "Brain". The whoosh now follows the line. Mix: all four checked lines 3/3, −16.5 LUFS, peak −2.0 dBFS.
- **Tails 8/8 lines, 108/108 drawings** (`DH8_BUBBLES=speech`: dh_speech places the bubbles, the placement the tail check was built on; dh_say passed 2/8). Don's back: head higher (crown out of the bottom quarter), the curl off the crown, the arm drawn apart from him. Pam back at v7's size (r 64): at 74 her bob blocks every tail. "...for sitting in that chair." shows as a MOM card.
- **Cold mute test, round 3: 2 of 5** (round 2: 3, v7: 2). Both viewers read Mom's cloth hand beside Sofía's as a handshake, and Sofía's jump as climbing into the throne, because the throne now rolls under her and she stands where it stood in 3F. Restaging 3E for the bubbles cost the read; round 2's 3E read better. Open.

## Round 4 (24 Nov): bubbles back on the repo's rules

- **Why round 3 was wrong:** it used dh_speech, the bubble system the repo dropped (`daddys-home-bubble-lessons-v1.md`, plan step 1), because `dh_tailcheck` passed it; that check did not test CLAUDE.md's "box beside the face, short tail". Round 3 had tails of 180–444 px from the top band, a MOM card for a speaker in frame, and a box with one word a line.
- **Now:** dh_say (the `bc_sb` port) for every line; no pinned boxes. `dh_tailcheck` gained qa_bc's rules: at most 20 px of tail over open wall (more over hair beside the cheek, lessons 360), no card for a speaker in frame, no squeezed box; the tip on the cheek's outline at mouth height (0.7 r instead of 0.4 r: Mom's and Pam's frontal faces put the outline 0.55–0.63 r from the mouth; Tomas, 24 Nov). Validated: round 3's bubbles (`dh_tailcheck_plant_r3.py`) fail on every line; the five old planted faults are still caught.
- **Staging:** 3E and 3F back to round 2 (Tomas). The camera moves for the boxes: 3E steps back and left (Mom's boxes on her left, the throne only jolts 10 so the tag stays whole); 3F steps back and right (Mom's box on her right). 3A: no push; Don's crown at x 404, his finger at the screen left of his box. 3D: the fist up from the first drawing, the head held still. Mom's thump bob removed.
- **Result:** 8 of 8 lines, 108 of 108 drawings. Frames: `dh_s3_v8_bubbles_r2.png`. Open: Sofía's jump passes in front of the tag; 3E is now WS (Mom r about 53) with a lot of floor. The film is rendered after Tomas's look.

## Round 5 (24 Nov): the series' shared bubble (`speech.draw`, `speech_gate.check`)

- main now says: new bubbles call `speech.draw`, checked by `speech_gate.check`; no other tail length or checker. v8 moves onto them (`dh_anim3_v8.say`): the face, the mouth and the cheek edges are measured on each drawing (dh_say.measure, the logged rigs); the box and the tail are `speech.draw`'s; every bubble drawing is checked (`python3 dh_anim3_v8.py gate`).
- What speech.draw is given: the robot and Don's bare crown as `above`; everyone else the cheek outline at mouth height (`aim`) on the side with more wall; to avoid: the logged signs (tag, screen), the app's right rail, other heads whole, Don's raised arm in 3A. A rig logged twice (the iso redraw) is not "another face".
- 3A: Don's crown at x 370 (his box over it, clear of the rail); his arm drops as the robot answers, so the robot's box goes over its antenna.
- `dh_tailcheck.py` is back to what v7 was checked with (my qa additions removed: one tail length, in speech_gate). `speech_gate.selftest` passes.
- Result: 108 bubble drawings, 0 faults. The frame sheet went to Tomas directly (sheets are not committed from 24 Nov).
