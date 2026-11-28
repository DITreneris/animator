# Approved.: best practices and the production plan, v1

UptimeZ Inc. · episode 16 · *Civil War* 4 of 5 · 28 Nov · working folder `the-review/`, branch `uptimez-the-review`.
It starts from concept v7.1 ([`the-review-concept-v7.1.md`](the-review-concept-v7.1.md)) and follows [`series/production-process.md`](../series/production-process.md) (stages 0–12, five stops, version budgets), [`CLAUDE.md`](../CLAUDE.md) (the gates), and the record of episodes 13–15. Nothing is built past the concept yet.

## Status

| Stage | State |
|---|---|
| 0 Before starting | Concept v7.1 closed. Branch `uptimez-the-review`. **STORYLINE v3.5 written** (only the sitting CEO can hand over the throne; row 16 *Approved.*; the Client's survival planted in 16) |
| 0.4 E15 as built | Done (28 Nov): the $49,999 tag hangs from the crown (not under the armrest); REVIEW is one two-sided tag on the throne's back; the Client is never on Don's floor line (h 1.03, w 1.69 of Don). In script v1 |
| 1 Script | **v3** (`the-review-script-v3.md`, 52 shots, 65.6 s, 11 lines; the dialogue punch-up, 28 Nov) with `the-review-hand-jobs-v1.md`. Stop 1 answered 28 Nov: one night (canon night grade), Sofía new outfit, panel voiced, 52 shots |
| 2 Voices | **Takes v1 done** (28 Nov): `src/rv_voices.py` (E15's method) with Kokoro and Whisper fetched from their GitHub releases. 11 lines, picks 1.2 B, 1.4 D, 2.5 A, 3.2 B, 3.3 B, 3.4 B (E15's take, reused), 4.2 B, 4.4 B, 5.1 B, 5.9 B, 5.10 A; Whisper heard 11 of 11 (2 of 3 windows or better). **Real length 74.3 s** (script 65.6; the bible allows 90). The robot's "Yes." was heard as "Yes, sir" 3 of 3 (its filter's tail): cut at 0.42 s (`TRIM`), now "Yes." 3 of 3, also with silence after it. Picks kept as the auto-pick (Tomas, "choose best"). `rv_timing_v1.json`; `rv_voices_v1.mp4` and the audition (not committed: rebuilt locally). **Stop 2 passed** (28 Nov) |
| 3 Look and set | **Night grade test still first** (decided 28 Nov): `src/rv_night.py` applies the canon night (bp_frame's palette) to the 9:16 front desk, opt-in, the throne with a warm rim only; cold checks, two fresh viewers a round: **v1** 0/2 sure of night ("no window, no dark sky, no lamp"); **v2** (+ street-light bands, vignette, stronger glows) 0/2, the bands read as rain or a glitch (removed); Tomas picked **night in the glass door**: **v3** (`rv_night_test_v3.png`: the shut door shows a navy sky, the moon, a lit window across the road, a streetlamp) **2/2 night**. Eye order throne → $49,999 tag in 6 of 6. Left: the room itself reads flat ("a dull afternoon" without the door), so every wide keeps the door in frame or a screen glow near a face; the moon made bigger (15). **Night with the cast, LOCKED at v5** (28 Nov, Tomas: "one stronger pass, then lock"): `rv_night_cast_N1/N2/N3_v5.png` (`src/rv_night_cast.py`, runs on a checkout with E15's modules until that branch is merged; md5 N1 f530ed31…, N2 77e5f887…, N3 d823bc73…). Six cold rounds: night reads with the door, the dark office glass or a screen in frame (N1 2/2, N3 2/2, N2 "probably" 2/2); HUMAN APPROVAL REQUIRED as the robot's face reads at 270 px; G3 clean. **Kept:** the light lands (monitor and machine pools on their sources, the cold patch from the door), the background falls off, contact shadows, the people darker away from the lights (shade 0.30). **Dropped:** the lit band and rim on the people (v4: "a ghost", "a hologram", "glassy" 2/2) and the big pools that ghosted the Client. The flat paper look of the people stays, as the series' style; motion (the screens' flicker) is checked at the motion tests. Rule for every shot: a night source in frame (the door, the dark office glass, or a screen near a face). **Lock moved to v6** (28 Nov, the third outside night review, Tomas "itraukiam, tvarkom"): the counter's front falls off away from Pam's monitor (to about 40 % at its far end) and the coffee machine is the warm source (a small warm pool at its front, its red lamp glowing): a hierarchy of sources, cold screens and one warm machine. `rv_night_cast_N1/N2/N3_v6.png` (md5 1192b831…, 53ff5b23…, 90cb5f75…). Not taken from that review, with reasons: the ambient −25 % (the canon palette), the cold rim on the people (failed 2/2 in v4), a dimmer throne gold (6 of 6 viewers read it first: the power prop). G6 is spent for the night look: the next outside review is at the board. Sofía's new outfit: **a CEO power suit** (black, sharp shoulders, a gold pin). E12's coffee machine (`dh_props.coffee_machine`) already has the gauge: it is the needle |
| 3 Props | **Props sheet v1** (`src/rv_props.py`, `rv_props_v1.png`): the grey steel folding chair (open, wobble, folded), the washer, REVIEW · TODAY/TOMORROW (E15's tag), the $80 invoice, the Client's name card, the report (held, unfurled), **one screen function** for the robot's face and the machine's panel, Sofía's CEO suit (E15's in black, a gold pin; shoulders not squared yet). All read at 270 px. Script **v4** retimed to the takes (74.3 s), the budget's last |
| 3b Key stills | **K2 v2 reads 2/2** (the robot in the throne, Don about to lose it, Father deciding); fixes: Don on HIS side of the tape (v1 stood him on Father's), the screen larger; APPROVER: CEO stays borderline at 270 (the 6.2 insert carries it). Father's reaching finger: to the pose sandbox. **K1 failed 2 rounds** (v1-v2: "abstract blocks", the arm "a trolley jack", empty floor): Tomas 28 Nov, redo **with the robot in frame at the same height** (its UPTIME face level with Don's lap, its arm down to the card). New poses (Don seated, Don on the floor, Sofía seated, the Client kneeling) go through a **pose sandbox** (Tomas 28 Nov), canon rigs untouched. v3 (robot at lap height) failed on the badge: its chest shows the HR badge it has at frame 0 but not at the end. **K1 v4** (Tomas "Go 1"): a medium on the whole throne with Don asleep (`src/rv_poses.py` v1, `don_seated`: don_ps's own rig clipped at the belt, new legs), the robot hidden behind the throne (only its screen's glow and its thin arm from behind the base), REVIEW · TOMORROW under the front-left caster. Cold round: Don asleep in a throne for sale 2/2; fixed after it: the card larger and moved left ("tiny", "the lever covers it"), away from the throne's red lever (read as part of the arm 2/2). Over the 3-version budget: at Tomas's lock. **Locked 28 Nov (Tomas): K1 v6, K2 v3.** K2 v3: no HR badge on the robot, Don's own head on the APPROVER: CEO screen, pushed in, Don and Father whole in frame, the floor arrow whole. K1: the front-on seated pose (v4-v5, then the report over the knees) read as "standing in front of the chair" four rounds running, so the premise changed (rule 5): Don asleep ACROSS the throne (`rv_poses.don_sprawl` "B": chin down, legs over the right armrest, the unread report on his belly, both hands `quiet`). Silhouette test §0.2, 3 variants: B "dozed" 2/2 (A "passed out", C "falling / dead"). K1 v6 cold: seated and asleep 2/2; joke told back unprompted ("bought a $49,999 throne to nap in; his only decision is TOMORROW"); the report also hides the ketchup stain (read as blood before). Legs thinned and drawn under the torso after it ("huge tube legs" 2/2), not re-tested. Confetti off in both (`rv_night_cast.NO_THRONE_CONFETTI`, opt-in; N1-N3 unchanged). Props sheet v2: the report one continuous strip with a second spill, the chair's one short leg, SALARY small over a big $0, the card's text centred. For the animatic: the robot arm ("a crane", "a lamp") reads once it moves the card; the red lever ("a joystick"). |
| 4–6 | **4.1 scene file v1 (28 Nov):** `src/rv_scenes.py`, the 52 shots moved from script v4 (generates `the-review-script-v5.md`). Amended there: 1.1/7.2 = K1 v6 (Don asleep across the throne, S4 · M); the blanket (Tomas /grill-me: the report's spilled tail stays when Father leaves, 6.10; Don folds it over himself, 7.1; frame 0's paper is last loop's tail); the robot hooks the tag back on the throne's back (1.4, behind). Four checks (Tomas: all four), each caught its planted fault: lines PASS, loop PASS (K1's hides listed: the HR card, the needle, Father's props), tape PASS (Don crosses at 3.1 and 3.9 only; the Client never on Don's line), props PASS (12 props, a state per shot, the needle still on lines and peaks). **4.3 Act I layouts (28 Nov):** v1 (`rv_layouts.py`, the night lock, a camera search for G3) cold 2 viewers + an outside review: 1.5, 1.6, 1.7 and Don's legs failed. E15's characters refreshed (branch `uptimez-double-agent` at 65ef23b: the Client CLEAN, Sofía v5 under the CEO suit as `rv_props.SOFIA_V5`, the cups canon); K1, K2, N3 rebuild identical, N1/N2 change with the Client. Poses reused (Tomas "Ieskom"): `rv_poses` v4 silhouettes: Don on his back knee up 2/2, Father on the folding chair 2/2 (B), the Client's side bend 0/2 ("back pain", "vomiting"). v2 (round 2 of 2): 1.6 seated 2/2, 1.7 two keys TOMORROW -> TODAY 2/2 with the crown, Don's cup 2/2; **1.5 still fails** (the Client's reaching arms read as "a huge limb", "legs" 2/2); the Client's red rag read as blood 1/2. G6: two rounds spent, back to premises for 1.5. **1.5 v3 (Tomas):** an insert at the short leg, the Client's hand from the edge (rolled sleeve, wrist stub) pinching the washer, two keys; **no rag on the Client in E16** (Tomas "1": `rv_layouts.CLIENT_NO_RAG`, the shoulder overlay skipped and client_of's own POCKET_RAG opt-out). Round 3 (new premise, 2 viewers): the hand at the chair's foot 2/2, its owner guessed as the Client 2/2, but the washer read as the chair's own foot 2/2 ("grips the foot", "drags the chair"); Father read as "a grey-haired woman" 2/2 at 270 in the wides (1.4, 1.6; rounds 1-2 said a man). **Act I layouts locked (Tomas 28 Nov), to the animatic:** the washer in motion (the hand never covers it, a silver glint, the tink, the chair stops wobbling); Father larger in 1.4 and 1.6 only if the animatic misreads him again; the cup arm of 1.2 ("fainted" 1/2) carried by the 1.1 slide. **Act II layouts (28 Nov), 2 rounds:** Sofía seated in the throne REUSED from dh_scenes._sofia_seated (in the CEO suit over v5); 2.6 as two keys (the oil tear on a flat face, then NOTED.). Round 2: the HR card robot -> Sofía 2/2, the oil tear read as hurt 2/2 ("oil, not crying" noted: the joke), Don pleased at the end 2/2; still open: Father's raised palm at 2.3 ("welcome / sit / go away" 2/2), POSITION VACANT the throne or the job (1/2), who rejects whom at 2.1 (Father's eyes past Sofía). **Act II locked (Tomas 28 Nov), to the animatic:** the palm in motion (report out -> palm -> the report slowly retracted), Father's head turning past Sofía as she sits. **Act III layouts (28 Nov), 2 rounds:** the episode's needle dial (`rv_props.gauge`, four zones, a new drawing over the machine's own gauge); the Client laid down REUSED from of_cast (The Offer), the mug at the hand the rig drew. Round 2: HUMAN APPROVAL REQUIRED 2/2, the spoon standing in the sludge 2/2, the mug caught 2/2. Open: Don's jab reads "raises a hand / waves" 2/2 (twice); why the Client is on the floor 2/2, and he reads as the failure while Don reads competent 2/2 (the anticipation is invisible in stills); 3.6 "nothing changes" 2/2; Don's step over the tape "a broken leg" 2/2. **Round 3 (Tomas: two new premises, then lock):** 3.4 a close, Don leaning over the counter's end, his fingertip on a green button beside the panel: "presses / approves" 2/2 (his face then 'smug' drew shut eyes; now 'grin', eyes open, not re-tested); 3.6 the Client leaning back from the tick, eyes on it ("something's coming" 1/2); 3.7 two keys, down BEFORE the steam, then the catch: the Client "the hero" 1/2, "dove or slipped" 1/2; Don "proud but reckless" 1/2. **Act III locked (Tomas 28 Nov), to the animatic:** the dive's timing (down on the tick, the steam after), the button larger, Don's step over the tape. **Lighting v3 (Tomas 28 Nov, the night-lighting review):** `rv_layouts.LIGHT_V3` on for the layouts (the locked K1/K2/N1-N3 untouched): a warm pool on the floor under the throne (no spotlight: "warm rim" kept), Pam's monitor on her face, the machine's halo and counter spill in its needle's colour (from `rv_scenes.states`), contact shadows +0.10; no cold rim on people (read as a ghost in the night lock). Five test frames reviewed (`rv_light_v3_test.png`): throne, Pam, gauge, Don on the floor OK; the robot's tear close FAIL with the pool and the darkening ("a gold fog, it levitates") -> back to v1 there. v3b: the pool -15 %, the gauge halo -30 % and tighter, the counter spill -20 %, the steam as ragged fading wisps ("soap bubbles"). **3.7 hand (the hand review, 28 Nov; canon: "a mug is held by its handle"):** CUP_GRIP on the lying rig, two attempts (handle hidden 2/2, "mitten", stray watch and knot); then a cut-in 3.7c, the hand alone from the frame's edge: CUP_GRIP's thumb pass at insert scale read "a glued pink bar" 2/2; Tomas: "another grip or the saucer hold": SAUCER_SUPPORT, the mug on his level palm (`rv_layouts.palm_mug`): "a waiter's tray, balancing" 2/2 (Don's cup on his palm at 1.2 is the callback), but the library hand at insert scale reads "a paddle / mitten" 2/2 and the mug "pasted on" 1/2: a canon row fix (the hand library's shapes at insert scale), not this episode's. The Client still reads lucky or worn out, not clever. **3.7 locked (Tomas 28 Nov, rule 5 after four attempts):** cheap fixes only (a long soft shadow under the lying Client, the mug's handle to screen left in every shot, 3.8's spoon shorter and the tar glossy). **Two tasks before animation:** (1) a lying-Client rig in the pose sandbox (the elbow on the floor, a knee bent, the knotted sleeves lying flat; the canon's lying pose is the creeper's, a standing figure turned 90°); (2) the canon hand rows at insert scale (SAUCER_SUPPORT, CUP_GRIP's thumb: "a paddle", "a glued bar"), in DITreneris/uptimez via `bp_hand_compare`, two attempts, Tomas picks. **Act IV layouts (28 Nov), 2 rounds:** the card on the throne's seat = "the throne is for the Client" 2/2, Don losing 2/2. Open: 4.2 Father reads contempt, not approval ("looks down on him", "doesn't help" 2/2): dh_cast.father has only 'hard' and 'talk' faces, no smile; 4.3 Don's look at his hands read "clasped, a waiter" (v1) then "clutching his cheeks, worried" (v2), 2/2 each; 4.4 "adds nothing" 2/2 (her eyes' move needs the robot or two keys). **Round 3 (Tomas: three targeted fixes, then lock):** 4.2 Father leaning toward the Client, his finger at the mug, a sly smile drawn over the rig's flat mouth: still "contempt, look at this loser" 2/2 (the heavy lids plus a smirk plus a point); 4.3 two keys, palms up then turned over: "identical", "worried" 2/2, his eyes on his hands don't show at this size; 4.4 two keys, the robot with its report in frame: "her attention goes to the robot" 1/2. **Act IV locked (Tomas 28 Nov), to the animatic / the sandbox:** Father's approval needs a face the rig doesn't have (eyes open, a small nod: a sandbox face, dh_cast untouched); 4.3 as an insert on his palms or a push-in to his eyes; Pam's look timed to the robot's head lift. **Act V layouts (28 Nov), 2 rounds:** the report's long strip, the $80 UNPAID insert on Father's velvet, UPTIME 100% / SALARY $0, Don's nod, Father's eyes to the crown's tag, "It reclines" (the throne tipped back under Don's palm; the room's own throne hidden for that shot), the card and the report in Father's two hands. Round 2: the invoice 2/2, "the robot works all the time and costs nothing" 2/2, "weighing the $80 against the $49,999" or "the robot against Don" 2/2. Open: 5.9 his realisation ("There it is.") has no face 2/2 (the same missing Father faces as 4.2); 5.10 "presenting / offering" 1-2/2 (the recline shows in motion); 5.7 "asleep or smug" (the nod is motion). **Act VI layouts (28 Nov), 2 rounds:** the robot set in the throne (K2's staging), HUMAN APPROVAL REQUIRED then APPROVER: CEO, everyone turned to Don, Don's close, the finger toward the screen and frozen, fists on the hips (`HIPS`, three trials on a sheet: don_ps "vest" read as "crossed arms / hugging himself"), Sofía's HR card, the robot out of the throne, Father leaving with the chair folded and the report's tail on the floor. Round 2: Don holds back 2/2, the fists "stubborn, 'fine, I won't'" 1/2. **Open, protect-list 1:** WHY he holds back (to keep his chair) reads in neither round ("noble" 1/2, "can't tell" 2/2), and the face on APPROVER: CEO is not read as Don's at 270 (1/2 "the robot"): stills can't carry it; it goes to the motion test of 6.4-6.7 (his eyes: the screen -> his own face on it -> the crown -> the hand back), the hardest beat. **Act VII (28 Nov), 1 round:** 7.1 two keys (the card wedged under the front-left caster as K1's, then across the throne, the report's tail as the blanket: don_sprawl "B"); 7.2 = K1 v6, the same file as 1.1 (the seam is one drawing). Cold: asleep on the throne, the TOMORROW card under the wheel, the robot's arm reaching 2/2; the seam into 1.2 "abrupt" 2/2: the fall is 1.1's motion (the gripper pulls the card, the throne rolls, he slides), not a still. **Stage 4 layouts done: all seven acts drawn; Tomas's stop 3. Hands by the canon (Tomas 28 Nov, after the audit against DITreneris/uptimez main 81c0ac7: "atrakinam ir sutvarkom pagal taisykles"):** `src/rv_hands.py`: hands_lr (E15's da_arms rule off for this process), hands_v4, `relax` -> `quiet`, Father on the canon hand, held things on the hand library through `without_hands` / `lib_hand` (the thing first, the fingers over it; `clutch`, `pinch`, saucer_hold), E15's `da_hand_gate` on every key frame against `rv_scenes.HANDS` (every hand's job declared). The gate: 178 faults at first, 0 now; four planted faults (JOB, LEGACY, AIR, WRIST) caught. **K1 v7 and K2 v4 replace v6 / v3:** K2 now has FATHER's finger toward the screen (script 6.2, hand-jobs H5), 25 px clear at 270, Don only looking. Not covered: the Client's own rig hand (client_ps), the robot's gripper (not logged), Pam's blueprint (not in her hands: `board_two` to do), 7.1a's stoop and the lying Client (sandbox). Not cold-tested since the change |
| 7–12 | **Held until episode 15's master** (decided 28 Nov) |

## 1. Our best practices, analysed (episodes 13–15)

| Practice | Evidence it works | Evidence it was missed or cost us |
|---|---|---|
| **One scene file generates everything** (stage 4) | The Offer and Pick a Side: script, layouts, board and animatic from `of_scenes.py` / `ps_scenes.py` | The generated script drifted when it was not regenerated after a film version (E14 plan §1). **Regenerate at every version** |
| **Checks that fail the build, each proved on a planted fault** | `uz_check`, 19 cases; E14's `ps_checks.py`, 38 shots, 0 faults | People and props floating in the air in E15's Act II layouts were caught by Tomas, not a check. That gave the **grounding gate** (feet on the floor or behind the counter, props on a surface or in a reaching hand) |
| **Five stops for Tomas** | Each stop sends the file, the gates passed and the open decisions as multiple choice | — |
| **Version budgets** | They exist because of First Search's 35 versions | E15 had **12 rounds of hand fixes** before the sandbox hand library |
| **Hands: one job table, one style** | E15's hand library v3 (approved 27 Nov) in one-outline style, kept out of canon until the episode is done | Each hand fixed shot by shot never converged |
| **Key stills before the board** | E15's S8 final image and S8r (frame 0) were locked first and anchored everything else | — |
| **Cold viewers** at the board, motion tests and rough cut, with direct questions | Shared misreads are cheap fixes. In E15 a reading was accepted instead of fought (the paperclip → the robot comes for the throne) | They measure reading, not laughs (lesson 141) |
| **Simplify a shot that is too hard** | E15: fewer characters and details where both spaces were hard to draw | — |
| **Outside reviews: two rounds, triaged (G6)** | Each triage found two or three causes behind many points | **E16 has already had five reviews at concept stage** (E14 had four). The concept is now closed |
| **The freeze rule** | An approved film is not reopened for later rules (26 Nov) | — |

## 2. The rules this episode adds or enforces

1. **The concept is closed.** v7.1 and its "closed decisions" list are the brief. Outside reviews come back only at the **board** (stage 5) and the **rough cut** (stage 8), one round each.
2. **Two key stills first** (decided 28 Nov), before layouts:
   - **K1 the loop seam:** a close shot of Don, the throne, the card under the front caster and the robot's hand. Frame 0 and the last frame are drawn by the same code.
   - **K2 the silence:** the robot in the throne, the screen showing **APPROVER: CEO** with Don's face, Father's finger stopped, Don's hand hovering.
   Each still passes `uz_check`, the hands page and Tomas before the scene file is laid out.
3. **One drawing for both approvals.** The machine panel and the robot's screen are drawn by **one function** in the same type (HUMAN APPROVAL REQUIRED). Don's press (gesture 1) and his hover (gesture 2) are one hand job with two states. The loop check covers the callback: the two screens differ only where the script says.
4. **Hands: E15's grab list and method, six story jobs** (decided 28 Nov). Every hand is listed with its row before drawing, the hand gate checks each shot, and hand library v4 is reused; only `point` is new. The canon (`hands_ps`, `of_cast`) is untouched until the episode is done. See §5.
5. **Grounding gate on every layout and board frame:** feet on the floor line or behind the counter; props on a surface or in a reaching hand. This covers the report paper, the folding chair, the mug and the card.
6. **The 0:01 joke is proved in motion first** (lesson 141, E14 rule 1). Motion test M1 is the throne rolling back off the pulled card, Don sliding, the cup raised. It is also the caster physics check.
7. **Hold every story beat 0.5–0.6 s** (lesson 136): the washer, POSITION VACANT, the needle, the tick, "Good hands." with Don's hands, the $80 invoice, SALARY $0 → $49,999, APPROVER: CEO. **The 2 s silence is fixed**, and nothing is trimmed from it.
8. **One dominant text per shot** (lesson 118): no shot carries two of POSITION VACANT, NOTED., UPTIME 100%, SALARY $0, $49,999, $80 UNPAID, APPROVER: CEO. Each reads at 270 px.
9. **Cause and effect in one frame** (lesson 132): the tick and the Client's head turn; Father's smile and Don's eyes; Father's stopped finger and Don's face on the screen.

## 3. Before starting (stage 0)

| # | Task | State |
|---|---|---|
| 0.1 | Concept v7.1 closed (five reviews triaged; G6 used) | Done |
| 0.2 | **STORYLINE v3.5**: the throne handover rule, row 16 rewritten as *Approved.*, the Client's survival marked as planted | Done (28 Nov) |
| 0.3 | Branch `uptimez-the-review` | Done |
| 0.4 | Read **episode 15 as built** (its latest frames, not its script): the throne and its back, the REVIEW · TOMORROW card, the tape, Sofía's outfit, Pam's mustard mug, Father's look | **Done late, 28 Nov** (after Tomas: "kodel tu nupaisei tokia nauja?"): against rough cut v4 (`e9e9894`). The price tag and the REVIEW card differed; the tape's state after episode 15 is still open |
| 0.5 | **Release order:** stages 1–6 run in parallel with episode 15; stage 7 waits for E15's master | Decided |

## 4. The plan, stage by stage

| Stage | What gets made | Pass | Stop | Budget |
|---|---|---|---|---|
| **1 Script** | `the-review-script-v1.md` from concept v7.1: every shot with size, setup (S1–S6 plus inserts), action → reaction, line, sound and hold; the protect list (§6); the 0:01 joke named with its frame; the cold viewers' direct questions (§7); **`the-review-hand-jobs-v1.md`: every hand with its row (§5)** | G0 (including the 0:01 joke), G1; **line budget 7** (the concept's); every spoken line has an action; checked against the front desk v4 and the canon locks; **no outside review** (the concept had five) | **1** | 4 versions |
| **2 Voices** | Existing voices: Don `am_onyx`, Pam (E15's audition pick), Father (his E12–15 voice), the robot (filtered, the source on screen), the machine panel (the robot's family, flat). The Client and Sofía are silent. `rv_timing_v1.json` | Whisper 3/3 on every dry take, checked with silence after each take; dry voices; the real length is known (target 64 s, at most 90 s) | **2** | — |
| **3 Look and set** | Opt-in props on the front desk v4 plus E14's tape: the **folding chair** (wobbling and fixed), the **washer**, the **coffee machine** panel and needle (creeps toward the counter edge in steps), the **steam jet**, the **report** (folded and accordion-unfurled), the **$80 invoice**, the Client's **name card**, the REVIEW · TODAY / TOMORROW card (E15's drawing), the **throne's front caster** and the **$49,999 tag under the armrest** (the back stays bare as in E15), the robot screens (one function, see rule 3), **APPROVER: CEO** with Don's face. **Sofía's outfit:** decided at this stage (the day after E15) | Episodes 13–15 rebuild **md5-identical**; every sign reads at 270 px | — | — |
| **3b Key stills** | **K1** the loop seam, **K2** the silence (rule 2) | `uz_check`, the grounding gate, the hands page, full-size crops of every hand; `/quality-assurance-agent` | Tomas picks (as E15's S8) | 3 versions each |
| **4 Scene file and layouts** | `src/rv_scenes.py`, the one source. Generated: the script, a layout sheet per scene, a top-down shot plan, a blocking sheet for the hardest beat (36–47 s: the report flood with Father reading) | G2 (action and reaction per beat, sizes, eyelines: Sofía → POSITION VACANT, Pam → the corner, Don → Father's smile); `uz_check`; grounding gate; `set_gate` (props on their marks, `SET_MOVES` for the creeping machine); the blocking test | **3** | 3 versions |
| **5 Board** | One key frame per shot at 540, generated | G3 (faces and protected props out of the dead zones; the board under the app overlay); **G4: two cold viewers** with the open prompt and the direct questions; then **outside review round 1** | — | — |
| **6 Motion tests** | **M1** the 0:01 throne roll (caster physics); **M2** the tick → head turn → drop → mug catch; **M3** the report following Don back; **M4** the press / hover / pull back (both states); **M5** the robot's slow, formal rise | G4: two cold viewers on 8 fps strips; `uz_check` | — | 3 versions each |
| **7 Animation** | Scene renders, native 1080 (at 2×), 15 drawings/s acting, 30 fps camera | `uz_check` on every frame including the drawing map; every change seen in a before/after strip | — | — |
| **8 Rough cut** | The full film: voices, effects (the tick, the hiss, the glug, the paper), room tone | G5 in full; G4 cold viewers (4 fps sheets plus 8 fps strips, the open prompt, the direct questions, "what felt rushed or slow"); then **outside review round 2** | **4** | — |
| **9 Polish** | Film versions | Each version is a numbered fix list, each fix seen in the render; three fixes that don't land on one beat cut the beat (lesson 52) | — | 5 versions |
| **11 Master and cover** | 1080 master, 540 preview (rebuilt locally, not committed), cover | G5 on the final AAC; a clean-checkout rebuild; cover read at 120 px | **5** | — |
| **12 Close** | `the-review-film-vN.md` (as built), lessons, README / INDEX / STORYLINE row 16 from the built film; the hand library to canon via CANON.md; a pull request | Pushed when Tomas asks | — | — |

Pin each approved stage with a tag: `uptimez-approved-vN`.

## 5. Hands: reuse E15's grab list and its method (decided 28 Nov)

E15 already built the method and most of the drawings, on branch `uptimez-double-agent`:
- `the-double-agent-hand-jobs-v1.md`: every hand in the script, its job and its canon row, written before drawing.
- `src/da_hand_gate.py`: each shot declares its rows, and the gate fails a hand that is not on its shot's list. Misreads are counted, and 3 is a fail.
- `src/hand_lib_v4.py`: the sandbox library, one closed outline per hand. Poses RELAXED, CUP_GRIP, SAUCER_SUPPORT, GRAB, CLUTCH, PINCH, PALM, FIST, all cold-tested.
- `src/hands_lr.py`: the canon's left/right.
- `src/da_hand_sheet.py`: the episode hand sheet, every job drawn with its prop.

E16 follows the same order and reuses those files. It writes no hands file of its own.

- **Stage 1:** the script comes with `the-review-hand-jobs-v1.md`, a table like E15's covering **every** hand (about 25, not only the story ones), each mapped to its row.
- **Stage 3:** `rv_hand_sheet_v1.png`, built the way `da_hand_sheet.py` builds E15's.
- **From stage 4:** each shot declares its rows to the hand gate.

### The six story jobs, mapped to what exists

| # | Job | Row / library pose | State | Rule it must keep (`docs/rules-hands-and-phones.md`) |
|---|---|---|---|---|
| H1 | Don, flat on his back, raises the cup straight up | `handle_grip` = lib **CUP_GRIP** (v3, 2/2) | **Reuse** | Catch the arm already up; never route the hand past the shoulder (Daddy's Home v8) |
| H2 | The Client fits a washer under the chair leg while his other hand lifts the leg | `pinch` = lib **PINCH** (v4, 2/2) + `clutch` = lib **CLUTCH** (2/2) | **Reuse** | One hand per wrist; the washer is drawn at the pinch the pose returns |
| H3 | The Client catches the mug without looking | **By the handle**: `handle_grip` = **CUP_GRIP** | **Reuse** | Lib GRAB read 0/2 on a mug's wide body ("a hammer"), so he catches it by the handle, never round the body |
| H4 | The robot hands over the $80 invoice; Father takes it | robot **gripper** (locked) → Father `pinch` (Father sheet v6, the tag pinch `redraw_at`) | **Reuse** | **Two hands near each other read as a handshake**: keep a clear gap and let the paper span it |
| H5 | Father's finger reaches toward the robot's screen and stops | `point` (canon; `point_t` if large in frame) | **New for the library** (there is no POINT pose): use the canon function first, add a library pose only if it misreads | **A finger that stops near a sign reads as holding it**: it stops clearly apart, measured at feed size |
| H6 | Don's press without looking, and later the hover, freeze and pull back | `point`, fingertip on the button | **New for the library** (same as H5): one job, two states | **A press is `point`** (a fingertip), not a palm slap, so the concept's "slaps" becomes a blind fingertip jab |

### Canon fault in v7.1, fixed at the script

- **"Don folds his arms"** at the climax and in the loop. E15 found that crossed forearms are a canon fault (in 5.4 Mom was changed to hands on hips). E16 uses:
  - **At the climax, standing:** fists on his hips (`fist` ×2, elbows out, the same pose Mom used in E15). It reads as defiance.
  - **In the loop, seated:** left hand on the armrest, right hanging (`clutch` / `quiet`). This is Don's pose in E15's locked S8r v4, so frame 0 matches an approved drawing.

### Cut from v7.1 into the script (no story weight, each a hand job)

The cup shaken twice; the spoon tilted to a diagonal (the spoon now stands upright on its own); the filter handoff to the Client; Don nudging the name card and Father straightening it. Don's pettiness moves to his face, and Father's straightening becomes a glance.

### The other hands (to list in full at stage 1), most of them reused

- Father unfolding the chair (`grab` ×2).
- Sofía unpinning and pinning the badge, then checking it (`pinch`).
- Pam holding the blueprint and turning a page (`board_two`, `pinch`).
- The robot pulling the card out (gripper).
- Father flipping the card (`pinch`, the tag pinch).
- Don folding the card and wedging it (`pinch`).
- Don putting the filter in (`grab`).
- Don setting the cup down (`handle_grip`).

**No new row is needed except a `point` pose in the library.** Any new gesture goes through rules §0.2: three silhouettes, two cold viewers, then a row.

## 6. Protect list (G1, draft for the script)

1. **The two HUMAN APPROVAL REQUIRED screens and Don's two gestures:** blind press, then hover and pull back.
2. **APPROVER: CEO with Don's face.** Father's finger stops.
3. **"Good hands." earned twice** (the washer, the mug), with **Don looking at his own hands.**
4. **The robot's arc:** the report refused → POSITION VACANT → the tear → NOTED. → "Yes." → the $80 invoice.
5. **The loop:** REVIEW · TOMORROW under the caster, the same close shot at both ends.

## 7. Cold viewers' direct questions (to be written into the script)

1. Why does Don make the coffee himself?
2. Whom does Father want, and why?
3. What does the robot show Father that nobody else could?
4. Why doesn't Father approve the robot himself?
5. What does Don do at the end, and why?

Pass: both viewers read at least 4 of 5 beats and answer every question.

## 8. /grill-me at every stop

Every stop sends the file, one line on what changed, the gates passed with evidence, and the open decisions as multiple choice (AskUserQuestion, recommended option first). Then it builds exactly what was picked. Known decisions waiting for their stage:

- Stage 1: the hold lengths against the 64 s target; whether the robot's "Yes." comes from out of frame (the corner) or on screen.
- Stage 2: the machine panel's voice (the robot's family, or none, as text only).
- Stage 3: Sofía's outfit; the throne's front caster and armrest tag drawings.
- Stage 3b: K1 and K2 framings (two options each).

## 9. Risks

| Risk | Guard |
|---|---|
| Hands again eat the schedule | E15's grab list, gate and library reused; only `point` is new; full-size crops; two attempts per row, a tie keeps the old drawing; misreads fail at 3 |
| The length grows past 64 s | The animatic decides; the bible allows 90 s; the 2 s silence is never trimmed |
| Too much text on mute | Rule 8, and the board's cold test asks what each screen said |
| The loop's state mismatches (the badge, the mug, the machine) | The close-shot seam (K1) and the loop check |
| More outside reviews at script stage | Rule 1: reviews only at the board and the rough cut |
| E15's animation slips | Stages 1–6 only; stage 7 waits |

#### Cold review after canon hands (28 Nov, 2 viewers, 270 strip + full size)
- K2 v4: Father's finger stops short of the screen 2/2 (one viewer read it as pointing at the price tag). Open: his other hand at the right edge reads as a cropped red blob 2/2.
- 5.5 (both hands on the bill in the lap): reads 2/2.
- Open: 5.10, Don's arm is a straight tube and his hand a mitten glued to the throne 2/2.
- Open: 5.11, the arms are splayed and stiff and the card and report hang pasted from the fingertips 2/2.
- Open: 5.3, the arm is a pole and it's unclear who holds the bill 1/2 each.
- Open: 5.1, the paper floats beside the gripper 1/2 (the robot gripper isn't logged by the gate).
- Open: 5.9, the hands on the knees are blobs with a red dot 1/2.
- Gate: 0 faults. The gate checks the canon rows, not how a hand reads: elbow bend, arm taper and a held-by-edge grip at full arm's length need pose work, not a gate fix.

#### Act V hands v5 (28 Nov, Tomas "darom", then "proceed")
- **Arms:** the three reworked shots draw through `tapered()` (E15's `da_arms.tapered`, opt-in per shot), with elbows bent. Every other frame is as it was.
- **A new sheet grip, by silhouette test.**
  - Round 1: the top-edge clutch, a fist on the side edge and palm-behind-thumb-in-front. No 2/2 winner, and thumb-in-front read as a pen 2/2.
  - Round 2: the clutch at the sheet's top corner nearest the body, the sheet tilted a little out, and the forearm drawn over the sheet. 2/2.
  - Finding: the sheet drawn over the wrist was what read as "pasted". `held_sheet(..., corner=True, sleeve=...)`.
  - Proposed for the canon's clutch row as a placement note, not yet written there.
- **5.3:** elbow bent, invoice in the corner grip. Round 3 read it as floating beside the hand 2/2, because its corner sat 8 px left of the fingers. Fixed after the round (corner under the fingers); not re-tested.
- **5.10:** Don beside the throne, his open palm (`palm`) on the back's gold edge, elbow bent (four trials). Round 3: "a salesman presenting it" 2/2.
- **5.11:** restaged. The card is held up in the corner grip (round 3: held 2/2). The report lies on his knee under his open palm (round 3: "a sticker", 2/2, open). Camera set by hand (G3: plaque and floor tape out). Hand jobs: clutch, palm.
- **K2 v5** (v4 kept): Father's other arm tucked in, camera 474, his ring off in this frame. It was "a red blob" 2/2 at 270. Round 3: the pointing finger is clear 2/2.
- **Still open:**
  - The report under the palm in 5.11.
  - The rig's hanging `quiet` hands read as mittens (Don, Father; 2/2, every frame). That is a series rig question, not this episode's.
  - The robot's arms read as poles with ball ends (2/2). Its gripper is not in the gate.
  - The ring at 270 is a blob wherever it shows (5.9, 5.11).
- **Rounds:** that is two rounds on these stills (rule 7, G6). Next is motion, or Tomas's call.

#### Held hands on the canon's functions (28 Nov, outside review "vis dar nesilaikom ranku canon", Tomas "tvarkom")
- **The cause.** Held hands were drawn by episode 15's `hand_lib_v4` (CLUTCH, PINCH, PALM, RELAXED), not by the functions the canon table names: `of_cast.clutch`, `hands_v4.board_two`, `hands_ps`.
  - The gate counted them by job name, so it reported 0 faults while viewers saw "pasted", "a sticker", "no fingers round it".
  - The corner-grip silhouette test above was run on the library hand. Void.
- **The gate.** New rule FUNC in `rv_hands.check`: a library hand is a fault unless its job is a pending row (`pinch_pinky`, `saucer_hold`). The planted fault must fail: `python3 rv_hands.py`.
  - First run: 14 FUNC faults. These included Pam's resting hands, which episode 15's `rig_hands` draws with the library's RELAXED; `rv_hands.setup` now hands them to `hands_ps` quiet.
  - Now 0, every act.
- **The shots.**
  - `held_sheet` uses `of_cast.clutch` (the back of the hand on the top edge, four fingers down over the front, the thumb under; object first) or `hands_ps` pinch: 1.4, 5.3, 5.11 card, 6.10 (the chair), 7.1a (pinch).
  - 5.5 uses `hands_v4.board_two`.
  - 5.10: Don's palm through his rig's `kit.HAND`.
  - 1.5a and 1.7a inserts: `hands_ps` pinch.
  - 3.6a: the Client's open hand is `hands_ps` palm.
  - 5.11: the report on his knee, held by its top edge from above (clutch). The palm-on-a-sheet is gone (no canon row).
  - Unchanged: 1.2 and 3.7 (`saucer_hold`, a pending row, Tomas's pick).
  - The corner/sleeve/inward hack is removed.

#### Props as episode 15 ends (28 Nov, Tomas /grill-me)
- **The audit.** Against episode 15 rough cut v4 (`e9e9894`; the worktree had been at 65ef23b; K1 and K2 rebuilt md5-identical).
  - The throne is the same (`dh_props.ceo_chair`).
  - The $49,999 tag was episode 14's (`ps_set.price_tag`, inherited from the night set).
  - The REVIEW card was episode 15's v1.
  - Cups, Sofía v5, the clean Client, the rigs and the confetti (off) already matched.
  - Open: the tape. Episode 15 ends with Don's strip peeled and the throne over the gap.
- **The price.** `dh_props` swing ticket v2, style **A** (the crown's left point), `TAG_FONT` 19, as episode 15's S8 and S8r.
  - Style B (under the left armrest, Tomas's first pick) was covered by Don's mark or the robot in 9 shots: 2.5, 2.7, 4.1, 4.5, 5.10, 6.1, 6.4, 6.7, 6.9.
  - The front of the episode 14 card is off.
- **The REVIEW card.** `da_layouts.review_tag "A"`; TODAY is the same lines (`rv_props._review_tag_word`, pixel-checked against TOMORROW).
- **Gates.**
  - `rv_props.props_selftest`, every planted fault failing first:
    - PROP: a retired function drawn (episode 14's tag, REVIEW v1, the price in style B).
    - COVER: a sign under 70 % visible.
    - EDGE: a card cut by the frame, even with no letters on it.
  - They run in every layout's checks, in the camera search, and on K1 and K2.
  - Hands and props: 0 faults, all acts.
- **Frames.**
  - K1 v8, K2 v6 (v7 and v5 kept). Don's antenna crosses the K1 tag; the letters read.
  - 5.9: Father's eyeline back to the crown's left point.
  - 5.7: camera set by hand.
  - 6.4 is now a medium close: Don, the $49,999 and APPROVER: CEO with his face in one frame. At 4.2 no camera kept the tag whole or out. This changes the shot, for Tomas.
- **Cold read at 270, 8 stills, 2 viewers.** The price read in every still that shows it (6/8); "large and clear" in 5.9. The robot's screen overlaps the card's corner in 6.1 (the letters stay whole).
- **Canon.** DITreneris/uptimez `hands-function-rule` 67192ac: CANON.md "Props". Lesson 251.
