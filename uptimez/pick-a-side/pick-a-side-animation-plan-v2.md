# Pick a Side: the animation plan (stage 7), v2

v1 was written on board v3 while the film was on hold for Daddy's Home. v2 (25 Nov) follows board v4 (the gags, the phones), Daddy's Home being finished (PR #118, the hold is lifted), and Tomas's /grill-me answers of 25 Nov.

## 0. Decisions (Tomas, 25 Nov)

| Question | Answer |
|---|---|
| Enough gags? | **Yes.** No new gags. Every gag gets its reaction, a hold, and a last picture that differs from its first (lessons 23, 912, 999) |
| Order | **Scene 1 now.** This plan is updated scene by scene as the film is built |
| Whole-board mute test on v4 first? | **No.** Board v3 read 3 of 3; each v4 change was tested on its own; new moves are tested in their scene |
| Sound | **With the exposure sheets.** Every gag has a sound or is written down as silent (lessons 105, 202, 230, 864) |

Still holding: stills (.png) before any video; no re-render after every small fix; props and people stay on the set; bubbles as they are (no change without asking); branch `uptimez-pick-a-side-gags`, commit only when asked.

## 1. Where the episode stands

| Stage | State |
|---|---|
| Script | v9 (board v4 text: HR?, the treat, the booth), 38 shots, 66.3 s |
| Voices | 19 takes, Whisper 3/3, `ps_timing_v3.json`. The v9 text changes (3.4, 4.3, 5.2, 5.3) need their takes checked against the new split shots |
| Scene file | `ps_scenes.py`, `check v5` 38 shots 0 faults, hand gate wired in |
| Board | v4, 44 key frames; phones locked after two outside reviews (8.3/10, "B + hands → LOCK") |
| Motion tests | A, C, D, E, F, G, H, I, J, K approved or accepted (v1 §1); not tested: 2.2, 4.1 bridge, 4.3b, 5.3b, 5.7 held phone, 6.1 thumbs, 6.2 |

## 2. The gags and what each needs in motion

Density: one physical gag about every 3.3 s. The only long talk is 1.3–1.4 (5.2 s): it is carried by a visible change per shot, not a new gag.

| Time | Shot | Gag | Reaction, hold | Last picture differs by | Sound | Motion |
|---|---|---|---|---|---|---|
| 0:00 | 1.1–1.2a | The blinds tug of war, the blind falls on Don | 1.2b: Pam's cup stops halfway; 1.3 Don frozen under it, 0.4 s | the blind on him, bare glass | rattle ×4 rising, CRASH | A (approved) |
| 0:08 | 2.1 | The tape rips through the group's feet | the feet hop apart, Mom's stay | the tape across the floor | tape screech toward the camera | D |
| 0:09.7 | 2.1b | The robot's OWNER: INVESTOR card | it rolls off pleased | the card on the throne | clip, beep | in scene 2 stills |
| 0:10.5 | 2.2 | The throne spin: the tag away, the card to the room | Don's smile drops, 0.4 s | the card faces us | roll and creak | **new: stills, cold test** |
| 0:11.9 | 2.3 | The roll as a weapon | they stiffen | DON arrow on the tape | — | in scene 2 stills |
| 0:15.1 | 2.5 | The salute, the half salute | the smile in the cup | the cup up | — | board |
| 0:20.2 | 2.8–2.9b | The heel behind the line, "Border breach" | Sofía doesn't move | the barrier on the visor | heel click, two-tone beep | board |
| 0:24.6 | 2.10–2.11 | The robot on the tape, the push, the bump | Don staggers; the fall lands or cuts | Don off balance | thud and spring, the music cut on the hit | H (2 notes) |
| 0:28.8 | 3.1–3.2 | The telescope arm, FLASH | the photo fills the screen | the photo | arm, the one flash | E |
| 0:36.4 | 3.4 | The tired arm, the phone slides in | his thumb lands on APPROVE | APPROVED | — | in scene 3 stills |
| 0:38.6 | 3.6 | DING behind the glass | Don smiles on | the glow | DING, muffled | board |
| 0:40.2 | 3.7 | Pam's cup to her chin | silence | the cup at her chin | — (the silence is the joke) | board |
| 0:42.6 | 4.1 | #TeamDon under the neon | — | the phone in the black sleeve | club bass | **new: still** |
| 0:43.2 | 4.2 | The oily finger on Pam, then the heel | — | the print on Pam, the zoom | — | J |
| 0:45.4 | 4.3a–c | The oily Client; the guards pinch their noses | 4.3b close, no line | Father: "Invite her." | stink? (to decide on the sheet) | **new: stills, cold test** |
| 0:49.8 | 5.2 | The gold pen writes H-R-? | — | HR? on the CV | pen scratch per stroke | in scene 5 stills |
| 0:51.4 | 5.3a–b | The oil can given to the robot | heart on the visor | the can in its hand | door, "Welcome.", a clink | **new: stills, cold test** |
| 0:53.8 | 5.4 | The foot over the line, the vest straightened | held 0.6 s | foot back | — | C |
| 0:57.8 | 5.6 | Sofía crosses, Pam frozen | Pam's hands stop | Sofía on Father's side | heel clicks | F, K |
| 1:00.3 | 5.7 | Pam's phone: INVITATION · DAD in her hand | Sofía looks up at Pam | the phone held | buzz | **new: held grip in motion** |
| 1:01.7 | 6.1–6.1b | Don's thumb up, "Everyone's with me."; the buzz, the hair spring | eyes snap back | the hair up | buzz | I; **thumb new** |
| 1:05.3 | 6.2 | The blinds shoot up, the loop | Don's hand on the cord | 1.1's frame | rattle, into frame 0 | **new: loop check** |

## 3. How it is built (v1 §3 stands; the changes)

- **`ps_film.py`** modelled on `of_film.py` (reused): one function per shot `(t, L)`, `render_scene(n)`, `mouth_at`, `bubble_on`, `held_only`; the check that fails a shot whose drawings never change (lesson 200), proved on a planted still shot first.
- **One map:** `ps_film.SHOT_FN`, asserted and printed (lesson 109); the motion tests become thin callers and rebuild md5-identical.
- **Board v4 switches:** the film runs under `gags_v5()`; board v3 and every approved sheet stay md5-identical.
- **Every drawing** through `ps_checks.frame_checks`, `speech_gate`, `set_gate`, `hand_gate` (now with `hands_validate` restoring its switches), and the loop check.
- 15 drawings a second on 30 fps; review copies at 540, the master at native 1080 (2×).

## 4. Per scene, in order

Each scene: exposure sheet (shot × drawing, the visible change, the cut, the sound) → key-pose stills to Tomas → the scene with voices and sound → checks → a look at full size → a cold test only where the move is new. Budget: 3 versions a scene, then 5 for the film; a move that fails three times is changed (lessons 52, 178).

| Scene | Time | Shots | New in motion | Cold test asks |
|---|---|---|---|---|
| 1 | 0:00–0:08 | 1.1–1.4 | none (A approved) | "What are the two fighting over?" (4 fps sheet + 8 fps strip of 1.1–1.2b) |
| 2 | 0:08–0:28.8 | 2.1–2.11 | 2.2 throne spin | Who owns the throne now? Who is on whose side? |
| 3 | 0:28.8–0:42.6 | 3.1–3.7 | 3.4 tired arm | Who approved the post? Who saw it outside? |
| 4 | 0:42.6–0:48.4 | 4.1–4.3c | 4.1 bridge, 4.3b noses | Where is this, and how did the photo get there? |
| 5 | 0:48.4–1:01.7 | 5.1–5.7 | 5.3b oil can, 5.7 held phone | What is Sofía offered? Whose phone rings? |
| 6 | 1:01.7–1:06.3 | 6.1–6.2 | 6.1 thumb, 6.2 loop | What is Don missing? What happens next? |

**Before scene 2:** the rig hand points with lean and tilt (v1 §3.5), opt-in, validated on a planted 20 px fault.

**Join (stage 8, stop 4):** the loop check, the film's 4 fps sheet, the whole-film cold test (3 viewers, the loop question, plus "whose phone is it in 6.1?"), the sound mix to G5 (−14 to −16 LUFS, ≤ −1 dBTP, Whisper per line).

## 5. Scene 1: the exposure sheet (first draft)

15 drawings a second; times from script v9.

| Shot | Time | Drawings | Keys | The one visible change | Cut | Sound |
|---|---|---|---|---|---|---|
| 1.1 | 0:00.0–1.8 | 27 | frame 0 = blind up, held 0.4 s (6 drawings, G5); then test A's four pulls, each faster (down Don, up robot ☀) | the blind's height, the room's light | on the fourth pull down | rattle ×4 rising, no music |
| 1.2a | 1.8–2.3 | 8 | the rail gives; the blind drops over Don; daylight bands through the bare glass | blind on Don | on the landing + 2 drawings | CRASH |
| 1.2b | 2.3–2.8 | 7 | Pam, Mom, Sofía; Pam's cup stops halfway, held | the cup stops | after the hold | the cup's clink cut short |
| 1.3 | 2.8–5.4 | 39 | Don's face out of the slats, still; ☀ fades to a smile on the robot; one slat swings and settles | the visor ☀ → smile | after the line + 0.3 s | DON whisper |
| 1.4 | 5.4–8.1 | 40 | the blind as a cape; he lifts the roll on "Without me."; the three look at each other | the roll up, three heads turn | on the look | DON |

Stills to Tomas: 1.1 frame 0, 1.1 mid-pull, 1.2a landing, 1.2b cup, 1.3 ☀ and smile, 1.4 roll up and the look (8 stills).

## 6. Open items

- 6.1: the case and the stand carry Pam's ownership; ask the scene 6 and whole-film cold tests directly.
- The v9 lines (3.4, 4.3, 5.2, 5.3) against their takes: recheck timing per split shot when scenes 3–5 are built.
- The commit of the phone fixes (25 Nov) waits for Tomas.

## 7. Scene 4: the plan (25 Nov, before building)

0:42.6–0:48.4 (5.8 s in script v9), three shots, three new moves. Built under the rules that held for scenes 1–3: stills first (sent, not waited on), a camera locked to the board's key frame unless a shot asks for its own, the board's text unchanged, 3 cold viewers with a question per new move.

| Shot | s | Drawings | What moves | The one visible change | Reused | Sound | Cold-test question |
|---|---|---|---|---|---|---|---|
| 4.1 | 0.6 | 9 | the neon buzzes on (one flicker); bodyguard 1's black sleeve lifts the #TeamDon phone into the frame under it | the phone comes up | board v4's bridge (`_post_bridge`, of_cast.phone_grip) | club bass, low; the neon's hum | "Where is this, and how did the photo get there?" |
| 4.2 | 2.2 | 33 | the oily finger stops on Pam (print 1), slides to the heel, spreads to zoom, print 2 | prints, the zoom | motion test J (FINGER_42), the v4 `point_t` finger | two soft smudges | "Who is the finger interested in?" |
| 4.3a | ~0.95 | 14 | the Client leans in, points at the phone: "That one." | the lean, the point | the board's booth, BOOTH_PART_V4 part 0 | — | "Who wants whom invited?" |
| 4.3b | ≥0.4 | 6+ | both guards turn away, mirrored, pinch their noses; the green stink lines rise | the turn, the lines (wavy, rising) | `_booth_guards`, CLOSE_43 | a sniff, a gag (short) | "Why do the two men hold their noses?" |
| 4.3c | rest | ~22 | Father looks at the phone, nods once: "Invite her."; the Client sits back: a black handprint on the velvet | the nod (one drawing, lesson 132), the print | part 1 | a send whoosh on the nod | "Does the man in the middle react to the smell?" |

**Decided (Tomas 25 Nov): (a), Father's take 0.4 s later.** Was: in v3 timing Father's take starts at 1.13 s, so a 4.3b close between the two lines would last 0.18 s — below a readable hold (0.4 s, lessons 23, 999). Options: (a) Father's take 0.4 s later, 4.3 = 3.33 s, the film +0.4 s (recommended); (b) the noses inside 4.3a's frame, behind the Client while he talks (no close); (c) the close after "Invite her.", the handprint moves to it.

**Before building:** the hand sheet for the pinch (rules §0: both guards' hands at their noses, measured gaps at feed size), the stink lines as a moving path (not three static strokes), and the booth's dead zones (the rail at x > 470).
