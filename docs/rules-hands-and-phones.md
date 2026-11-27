# Rules: hands, arms and phones (synced copy)

**The canon is [DITreneris/uptimez `docs/rules-hands-and-phones.md`](https://github.com/DITreneris/uptimez/blob/main/docs/rules-hands-and-phones.md)** (Tomas, 26 Nov). This is a copy of it from 26 Nov (with the `board_two` and `tap_insert` rows of branch `hands-v4-rows`). If the two differ, the uptimez page wins: update this copy, never the other way round. Lessons 147–264 and §0 below stay true where they do not contradict it.


Copied from [DITreneris/animator](https://github.com/DITreneris/animator) `docs/` on 26 Nov 2026, where it covers UptimeZ and Hoodyz. `docs/lessons.md` and the episode folders it names are in that repo. This page wins when `docs/lessons.md` disagrees. A new job is a new row here, written before any episode draws it. An episode does not get its own hands file.

## Read this

- **One hand for the whole cast.** `hands_ps`, through `kit.HAND` inside a rig or `of_cast.ps_hand` outside one.
- **One hand per wrist.** The prop sits at the hand the pose returns. A second hand, a sleeve stroke, an oval finger, or a phone rectangle on top of that hand is a second hand.
- **The arm is two bones of fixed length** (`of_scenes.ik2`). Move the shoulder or shorten the travel. A stroke of one width is not an arm.
- **A phone is `of_cast.phone_grip`**, upright, thumb off the words. A rectangle with words on it is a slide.
- **A still comes before motion.** Full size, and again at 270 px wide. The same misread three times changes the gesture.

A film that cannot import these modules still uses these shapes. It does not invent another hand.

## Jobs

Name the job, then draw that row. If the job is not here, stop and add the row before code.

| Job | Shape | Function |
|---|---|---|
| At rest | `quiet` | `hands_ps` |
| Fingertip, level | `point` | `hands_ps` |
| Fingertip, down or in an insert | `point_t` | `hands_ps` |
| Holding a thing | `grab` | `hands_ps` |
| Holding an edge (sheet, card, lid) | `clutch` | `of_cast.clutch` |
| Pen, or thumb and index meeting | `pinch` | `hands_ps` |
| Empty closed hand | `fist` | `hands_ps` |
| Open hand | `palm` | `hands_ps` |
| Thumbs-up | `thumb` | `hands_ps` |
| Phone | `phone_grip` | `of_cast.phone_grip` |
| Handle (lamp, tool) | `handle_grip` | `of_cast.handle_grip` |
| A board, tablet, card or printout in two hands | `board_two` | `hands_v4.board_two`: the board first, then one `clutch` at each upper corner (silhouette test 26 Nov: 2/2 over grab-at-the-sides and palms-under) |
| A tap on a screen in an insert | `tap_insert` | `hands_v4.tap_insert`: `point_t`, the forearm and a cuffed wrist stub from the bottom edge (test 26 Nov: 2/2; no stub reads as a floating hand, from the side reads as pointing, not tapping) |

**The sheet in films (26 Nov):** `hands_v4.py` (animator `uptimez/src`) draws the sheet's `grab`, `pinch` and `fist` (v2) after a film calls `hands_v4.enable()`. The phone: the sheet's row is v4c (the thumb off the words); `hands_v4.enable(phone="v4c")` draws it, checked in One Star v27 at 1:04. Without that argument a film keeps the old `of_cast.phone_grip` (v3). A film that does not call it draws as before. The two new rows came from the series hands and phones audit v1 (animator `uptimez/series/hands-phones-audit-v1.md`), where each film had improvised its own.

The picture of this table is the class sheet, `the-blueprint/rough_work/pic_hands/bp_hand_classes_v4.png`: male width 17, female 15, the same shapes, no nail. It is the target. Its `grab`, `pinch`, `fist` and `phone_grip` are drawn by the sheet scripts, so a film that calls the function in this table still gets the older drawing until a separate opt-in module exists. How a row changes: [`CANON.md`](../CANON.md).

`hands_ps` also contains `point_s`, `two`, `two_s`, `salute`, `tuck`, `beckon`, `relax`, `relax_s`. Those stay for shots that already shipped them. A new shot uses the table.

## 0. Before drawing

A review or a cold test that names a hand is not a request to patch that hand. In this order, before code:

1. **Name the job.** Reply with the row from the table. Do not grep `docs/lessons.md` for a shape, and do not copy this page into an episode file.
2. **A job that is not in the table is a new gesture.** Three solid black silhouettes, side by side, 270 px wide, two cold viewers. Keep the one both read as meant. Then add the row.
3. **Measure the gap.** Finger to screen, finger to hair, hand to the other hand: pixels on the frame, then the same gap on the 270 px tile. A 15 px gap at 540 is about 7 px in the feed.
4. **One still, as a PNG, before any render.** The hand sheet is this film's jobs at one scale.
5. **The check reads the picture.** It fails a second hand on the wrist, a phone with no `phone_grip`, and a sleeve drawn as one stroke. A check that measures boxes the drawing function just built does not count. `bp_draw_audit.py --hands` is that check. `uz_check` limbs is an arm count. On 16:9 the hand command is `--grips`, and its plant must exit 1. A cold viewer who names the action has not passed the hand. Plant the faults first; a check that always passes is worse than none.
6. **A 10 fps strip of the encoded file** for every shot whose hand or arm code changed, looked at before the cold test.
7. **The same misread three times changes the gesture.** After one hour, or two full checks, with the faults not falling, stop and report.

## 1. Hands and arms

### Gestures

- **A hand at the ear or the cheek reads as a phone call,** with or without a phone. A counting or warning finger goes in front of the chest, or toward the thing counted.
- **A pointing finger that stops near a sign reads as holding it.** When the arm drops, the sign floats. Point from a measured gap, or do not point at a wall sign.
- **Two hands near each other read as a handshake,** whatever the props. Keep a clear gap, or use another gesture.
- **`point` aimed down, or large in an insert, grows a second finger** from the thumb across the knuckles. Use `point_t` there (index out, no thumb). Pointing level reads. Pointing down reads as pointing at the floor.

### The hand itself

- **One shape per state.** Rest is `quiet`. A fingertip is `point` or `point_t`. A hold is `grab`, `clutch`, `pinch`, or `handle_grip`. One closed fist for every job reads as toes.
- **A face beats a gesture.** No hand or prop over an eye in a reaction shot.

### The arm

- **Two bones, fixed length.** Out of reach, the arm goes straight and reads as a pole from the neck. Shorten the travel.
- **A target near the shoulder folds the arm** into a V, or lays it across the head, and the drawing jumps. Catch the arm already up, and drop it straight down out of the frame.
- **The wrist is narrower than the forearm. The upper arm is wider. The elbow is a real joint.** Equal widths read as a rubber tube.
- **A sleeve is no wider than the arm in it.**
- **An elbow under about 20° that does not hang is a pole. A fold over about 140° is a lump.** Square shoulder patches, a wrist past the prop, and crossed forearms are drawing faults of the same kind: one round cap, the target on the prop, elbows out and the hands meeting at the prop.

### Close-ups

What fails, in the order viewers say it: one stroke from the edge is a pole; an elbow and a sleeve with no person is a tube; a hand alone in the middle is a hand walking in space.

- **At the frame's edge:** a hand and a short wrist stub (`of_scenes.insert_cuff`). The stub runs out of the nearest edge.
- **In the middle:** the owner is in the shot. Body (the back is enough: his hair, ears, shoulders) and both arms from the shoulders.
- **Both elbows inside the frame.** An elbow outside it splits into a forearm from the edge and a sleeve lying apart. Pull the camera back before cutting the elbow.
- **After pulling back, cut down the biggest flat light area.**
- **What he wears sits on the wrist,** along the forearm. A watch drawn in the old place floats once the arm is gone.

### Poses before motion

- **The target has to match the arm.** Much closer than the bones are long, the arm folds into a lump. Move the target until shoulder, elbow, forearm and hand are one line.
- **One static pose approved before any motion.**
- **One target path per hand per shot.** Blend between places. A switch of target inside one drawing pops.
- **In-betweens are drawings.** If a move pops, list the key poses that do not exist yet and draw them. A change of view of 90 degrees is a cut.
- **Chain the parts:** hips, trunk, head, then shoulder, elbow, wrist. Each a drawing or two after the one before.

### Holding and moving things

- **Draw the object, then the fingers over it.** A handle comes out past the fist.
- **A prop in a rig's hand is drawn in that hand's coordinates.** Record the matrix at the hand call, draw the prop under it, call the same hand again on top. One hand, two passes. Drawn in scene coordinates, the prop sits off the hand and at the wrong size.
- **Hold the object where its shape shows.**
- **A hand that changes job moves in order:** reach (about 0.3 s), grip, then lift, the object locked to the hand. Rest the hand near the next action, so the reach is short.
- **A tool leaves by the wrist.** The arm stays.
- **Contact all the way.** A lid keeps the hand on it through the slam and after. A hand beside it reads as a wave.
- **Each person handles his own prop.** A reach toward someone else's clasped hands reads as holding hands.
- **A handover is close, both hands in frame:** out, taken, carried, at least 1.0 s. The camera comes close. Slowing the wide shot does not make the pass readable.
- **A held prop drops over 0.4 s or more.** The body turns back after the drop. A drop and a turn in the same tenth of a second jump.
- **One prop, one shape, one place.** The same rag, tool or card, drawn the same way, in the hand only. No second copy in a pocket or an insert.
- **A shared rig is patched from the episode**, the way `client_of` patches its source. The shared file stays, because another film's build reads it as text.

### A phone in a hand

- **`of_cast.phone_grip` for every phone.** Palm behind, thumb over the edge toward the body (`body_x`), fingertips round the other edge. At the ear, the back of the phone is against the head.
- **Upright, when the screen must be read.**
- **The holder is in the shot, or the arm implies him.** A phone held from above belongs to someone standing over it. An arm along the floor from the edge has no owner.
- **The thumb stays off the words.** A press starts below the word and travels to the button.

### The screen

- **One UI kit per film.** Status bar, app bar, cards with a soft shadow, pill buttons, avatars. Every screen is 100 units wide, through `ui.hand` (inside a grip) or `ui.full` (a full-frame insert). A film without `of_ui.py` still follows the rest of this list.
- **One word carries the story, and it is the biggest thing on the screen.** A real-app detail that shrinks that word comes off.
- **Light screens.** The call is light green, the name in white, clear of the fingers.
- **Nothing smaller than about 9 units** on a 100-unit screen. Helper text is dropped, not shrunk.
- **Shadows and gradients stay weak.**
- **The word on the screen is the word someone says.**
- **No real brands, apps or logos.**
- **Colour tells the state** (green ringing, grey declined), because the small text may not be read.

### A lamp

A lamp has its parts: grey ribbed handle, orange shield, cage, bulb lit or dead, hook, and a cable from the handle to the floor. The beam follows the lamp's angle. A dead lamp darkens the frame a shade (`of_set.lamp`, `lamp_cable`).

## 2. Speech bubbles

- **A line's box stands still for the whole line.** Placed once, pasted after the frame. Only the tail follows the mouth drawn in that frame.
- **No cut inside a line when the box cannot keep its place.** One picture, and a slow push-in that holds the speaker's head. Where two pictures share a free area, both get the same box.
- **An off-screen speaker is shown.** The card's tail points at that speaker's own small head, peeking in at the frame's edge on its side. A card alone beside the listener reads as the listener's line.
- **A long line goes over the head, two rows,** when the tail would cross the chin.

Bubble measure, tail length and the safe rect live in `speech.py` and `speech_gate.py`. This section is only the placement.

## Where this was learned

Lessons 147, 149, 163, 178, 179, 200, 201, 206–208, 221–226, 231, 263, 264, 417, from *The Offer*, One Star, Daddy's Home and Pick a Side. The numbers are the history. The rows above are the rule. When a new film teaches a hand or a screen something this page does not say, add the row here.

## Superseded

- **200.** "An insert's arm is a hand, an elbow and the frame edge." The owner is in the shot, and both elbows are inside the frame.
- **201.** "A short forearm as wide as the hand, cropped tighter." True only at the frame's edge, and there it is a wrist stub.
- **221.** "An insert arm with a shoulder and a torso disc." The disc read as a dome. The owner's body is in the shot.
- **222.** "Hand and wrist stub only." True at the frame's edge only.

---

## Earlier version (animator, before 26 Nov), kept for its §0 and lessons

The rules that hold now, gathered from lessons 147, 149, 163, 178, 179, 200, 201, 206–208, 221–226, 231 (episode 13 *The Offer* v26–v39, One Star v7–v9). Read this before drawing any hand, close-up arm or phone screen. When a lesson below disagrees with this page, this page wins; the superseded ones are listed at the end.

## 0. Before changing any hand, arm, gesture or pose (Daddy's Home v8, 24 Nov)

A review or a cold test that names a hand is not a request to patch that hand. In this order, before code:

1. **List the rules that apply.** Read this page and grep `docs/lessons.md` (finger, thumb, point, gesture, silhouette, ear, phone, grip). Write the applicable ones, with their numbers, in the reply to Tomas, before any drawing. (v8 round 7 skipped this: lessons 263 and 417 were not read, and the fix made a new misread.)
2. **A gesture that carries meaning gets its own test first** (417): three variants as solid black silhouettes side by side, at feed size (270 px wide), shown to two cold viewers. Keep the one both read as meant (264: a pose must read as a black shape).
3. **Measure, don't eyeball** (263): a gap (finger to screen, finger to hair) is measured in pixels on the frame, and checked again on the 270 px tile. A 15 px gap at 540 is about 7 px in the feed: it doesn't exist there.
4. **Hand sheet in the film's poses** (`of_hands.py`) for any new or changed shape, and `of_scenes.py hand-validate` and `hand_gate.py` passing.
5. **A 10 fps strip of the encoded file** for every shot whose hand code changed, looked at before the cold test.
6. **The same misread three times: change the gesture, not its position** (178, extended from grips to every gesture). "The hand holds the sign" and "a handshake" came back 3 and 4 tests running while the hand was moved a few pixels each time.

## 1. Hands and arms

### Gestures

- **A hand raised to the ear or cheek reads as a phone call,** with or without a phone (it is the phone grip's place). Pam's "one" finger beside her ear was read as "taking a call" by both cold viewers. A counting or warning finger goes in front of the chest or toward the thing counted.
- **A pointing finger that stops near a sign reads as holding it.** When the arm drops, the sign "floats". Point from clearly apart (measured at feed size), or don't point at a wall sign at all.
- **Two people's hands near each other read as a handshake,** whatever the props. Keep a clear gap between their hands, or give the moment another gesture.
- **Big or turned hands:** `point`'s thumb across the knuckles reads as a second, bent finger in an insert or pointing down; use `point_t` (index out, no thumb: the back of the hand) there. Pointing level reads; pointing down reads as "at the floor" and the hand as deformed.

### The hand itself

- **One hand for the whole cast.** Use the series' hand (`kit.HAND`, `hands_ps` shapes `fist`, `point`, `palm`, `grab`, `thumb`, `quiet`; `of_cast.ps_hand` outside a rig). Don't draw a new hand system; merge main and look first (147, 179, 206).
- **One hand per wrist.** A prop is drawn at the hand the pose returns, never on a separate hand. `of_scenes.py hand-validate` must pass (179, 208).
- **A shape per state.** A resting hand is `quiet`, a press is `point` (a fingertip), a grip is `fist` or `grab`. One closed fist for everything reads as "toes" (207, 200).
- **A face beats a gesture.** No hand or prop over an eye in a reaction shot (163).

### The arm

- **Two bones of fixed length** (`of_scenes.ik2`). The arm's reach is set by the bones: move the shoulder or shorten the travel, never stretch the arm. A fixed elbow offset stretched an arm 33 % between two frames (224).
- **Keep the target in reach.** Out of reach, the arm goes straight and reads as "a pole from the neck" (179).
- **Never route a moving hand past the shoulder.** With fixed bones a target near the shoulder folds the arm into a V or lays it across the head; a raise or a drop that starts or ends there jumps between drawings. Catch the arm already up, and drop it straight down out of the frame (Daddy's Home v8, 3A, 10 fps strip).
- **A wrist narrower than the forearm, the upper arm wider, a real elbow.** Equal widths read as "a rubber tube" (149, 224).
- **A sleeve is no wider than the arm in it.** A wide light sleeve becomes the biggest shape in the frame (225).

### Close-ups (inserts)

Read by cold viewers, in this order of what failed: one stroke from the edge = "a pole"; elbow and sleeve but no person = "a tube"; hand alone mid-frame = "a hand walking in space".

- **At the frame's edge:** a hand with a short wrist stub (`insert_cuff`) passes. The stub runs out of the nearest edge (222).
- **Mid-frame:** the owner is in the shot. Show his body (from behind is fine: back, head with his own hair, ears, shoulders) and both arms from the shoulders (224).
- **Both elbows inside the frame.** An elbow outside it splits the arm into "a forearm from the edge" and "a sleeve lying apart", and it jumps when it folds in. Pull the camera back before cutting the elbow (225).
- **After pulling back, find the biggest flat light area** and cut it down; here a white back became shoulders only over navy overalls (225).
- **What he wears goes on his wrist,** along the forearm's direction (a watch floated when the arm was taken away) (223).

### Poses before motion

- **Check the hand target against the arm's length.** A target much closer to the shoulder than the arm is long folds the whole arm into a lump (a "bulge", a "stuck-on fist"). Move the target until shoulder, elbow, forearm and hand read as one line (231).
- **One static pose approved before any motion.** More frames of a broken pose multiply the fault (231).
- **One target path per hand per shot.** Blend between places; never switch targets in one drawing (231).
- **In-betweens are drawings.** If a move pops, list the key poses that do not exist yet (an exposure sheet) and draw them; a change of view of 90 degrees is a cut (231).
- **Chain the parts:** hips, trunk, head; shoulder, elbow, wrist. Each a drawing or two after the one before (231).

### Holding and moving things

- **Draw the object, then the fingers over it.** A tool's handle comes out past the fist (224).
- **A prop held by a rig's hand is drawn in that hand's coordinates.** The hand hook is called inside the rig's own transform: record the matrix at the call, draw the prop under it, then call the same hand again on top (one hand, two passes). Drawn in the scene's coordinates, a mug sat off the hand and at a fraction of its size (Daddy's Home v8, 4D'').
- **Hold an object where its shape shows.** A spark plug held by its thread showed only white and read as "paper" in three audits; held by the top, the metal shows (224).
- **A hand that changes job moves in order:** reach (about 0.3 s), grip, then lift, with the object locked to the fist. Rest the hand near the next action, so the reach is short (223, 225).
- **A tool is withdrawn by the wrist,** the arm still (224).
- **Contact all the way:** a lid that shuts has the hand on it down to the slam and after; a hand beside it reads as a wave (225).
- **Nobody reaches toward someone else's clasped hands** ("holding hands"). Each person handles his own prop (221).
- **When a grip fails three times, change the gesture, not the grip** (178).

### A phone in a hand

- **`of_cast.phone_grip` for every phone:** palm behind, thumb over the edge toward the body (`body_x`), fingertips round the other edge. At the ear, the BACK of the phone is against his head (179).
- **Held upright** for anything that must be read (200).
- **The holder is visible or implied:** a phone held from above belongs to someone standing over it; an arm along the floor from the edge has no owner (225).
- **The thumb stays off the screen's words.** If it must press, it starts below the word and travels to the button (the DONNIE decline).

### Checking

- **Hand sheet in the film's own poses, at one scale** (`of_hands.py N`), not random poses (149).
- **Stills to Tomas as PNG before any render.**
- **A 10 fps strip of the encoded file** for every shot whose hand or arm code changed. Stills at three times missed a jump (223).
- **After two audit rounds on the same stills, render and test the motion.**

### A rule is a gate (One Star v15–v16, 25 Nov)

- **Every held prop goes through the series' grips** (`of_cast.phone_grip`, `clutch`, `handle_grip`, `ps_hand`), never an
  episode's own ovals: One Star kept `s1.fist` / `grip_rect` / `sb.thumb` for months because nothing checked them, and every
  close-up hand read as "capsules". `cs_grips.py` routes them all through one switch.
- **The hand gate runs in the build, not only in The Offer:** a rig hand under a grip, a thumb on the outer side, an old
  grip drawer: the render stops (`cs_grips.gate`, self-test with planted faults first).
- **The elbow gate:** every rig arm is logged as drawn; an arm bent under 20° that does not hang fails (the "pole"), and a
  fold over ~140° is a lump (231). Measured faults were few; the "breaks" people see are mostly drawing: square shoulder
  patches (the Client: one round cap), a wrist over a counter's edge (keep the target on the prop), crossed forearms at
  the chest (elbows out, hands meet at the prop).
- **Two more gates (One Star v20, 26 Nov)**, because the geometric ones passed a film full of misreads: the **insert
  gate** (an `insert_cuff` sleeve with more than 200 frame units inside the frame and no owner: 224/225) and the
  **flat-band gate** (a run of one-colour rows over 40 % of the frame: v17's 5.2 shipped an empty dark lower half
  because the fix was checked on a crop). Both were tried on the planted v17 5.2 first. Check every change on the
  WHOLE frame, not a crop.
- **A prop that is held is held**: a robot's phone sits in its claw (two prongs over the phone), not on the end of
  its stick; a phone or card does not appear in a hand between two drawings: it is in the hand from the shot's start.
- **A phone's back on a dark costume** needs a rim and its camera lenses, or phone and hands become one black blob.
- **A gate on words is not a gate on hearing**: Whisper's context window lost "Still one star." whenever the mix
  moved by a fraction of a second, at any level; alone it was heard every time. People with sound decide.
- **Paint on a rig's part only inside that part** (One Star v26): capture the part's own shape as the rig draws it and
  clip to it; never a second guessed shape over it (a double contour in a close-up).
- **A phone shown to us is held by its owner's arm** (`phone_grip` at the rig's hand), never a hand drawn at a prop's
  edge; check the elbow gate after (a straight arm out is "a pole").
- **A shared rig is patched from its source in the episode** (as `client_of` does), never edited in place: another film's
  build reads that source as text.

### Lamps, rags and held props in a gag (The Offer v45–v51, 24–25 Nov)

- **A lamp has its parts:** grey ribbed handle, orange shield, cage, bulb lit or dead, hook, and a cable that hangs from the handle to the floor. Its beam goes along its own angle; a dead lamp darkens the frame a shade (`of_set.lamp`, `lamp_cable`).
- **A handover is shown close, both hands in frame:** out, taken, carried, at least 1.0 s. In a wide shot the same move read as "suddenly in the suit's hand" (3 of 3 twice). The camera comes close, not the move slower (v51, `HANDOVER_CAM`).
- **A held prop drops over 0.4 s or more,** and the body turns back AFTER the drop, not with it. A drop and a turn in the same 0.1 s read as a jump (2.8f, v51).
- **One prop, one shape, one place.** The red rag is in his hand only, drawn the same everywhere (`client_of.shop_rag`); no pocket rag, no second rag in an insert (v48, decided).

### Inserts and the loop (The Offer v53–v55, 25–26 Nov)

- **An insert's object carries its own signs.** A black band with a grey panel read as "seat backs or a counter" (2 of 2); with a windscreen, a pillar, side windows, handles, an aerial and a mirror it read as a car at once.
- **A match cut needs the first action finished.** A phone stopped a hand above the roof read as "a jump"; landed in the last two drawings (burst, thud, the car dips), the next shot's fist read as the second blow (2 of 2: "a match cut, intended").
- **Land the two actions in the same part of the frame,** so the eye doesn't travel across the cut.
- **A new last shot is the film's own set and rigs** (v54 was drawn from nothing and rejected; v55: the garage, Father's rig, scene 2's palm, frame 0's SLAM lines; only the camera is new). Storyboard PNG to Tomas first; cold viewers say whether it reads, not whether it belongs.
- **A hit is a hand, not a prop:** a phone slapped on a car read as "a wallet, a block" three times; the phone goes to the pocket and the palm slams (the guard's own gesture at frame 0).
- **A loop that is an echo gets its own gate** (`of_cut.slap_ok`: the last frame IS the declared picture), and the planted faults move with the picture: a fault outside the checked band was "caught by: NOTHING".
- **An end card that explains is read as a glitch.** The fresh plan pinned over the burnt one failed 3 of 3 from v30 to v52; an action replaced it.

## 2. Speech bubbles (The Offer v47–v51)

- **A line's box stands still for the whole line.** It is placed once and pasted as a layer after the frame; only the tail follows the mouth drawn in each frame (`lock_bubble`, `BUBBLE_AT`).
- **No cut inside a line when the box can't keep its place across the cut.** Cuts at 0:19 and 0:28 made the box jump between two places (3 of 3). Use one picture and a slow push-in that holds the speaker's head on screen (`push_in`, `BUBBLE_AT` key `"*"`). Where two pictures share a free area, give both the same box.
- **An off-screen speaker shows who it is:** the card's tail points to that speaker's own small head, peeking in at the frame's edge on its side. A card alone beside the listener reads as the listener's line (3 of 3; `robot_peek`).
- **A long line goes over the head, two rows, when the tail would cross the chin** (`bubble_top`, `speech.TOP_FIRST`).

## 3. Phone screens

- **One UI kit per film** (`of_ui.py` in ep. 13): status bar, app bar, cards with a soft shadow, pill buttons, avatars. Draw every screen at 100 units wide through `ui.hand` (in a grip) or `ui.full` (a full-frame insert). A rectangle with two words reads as a slide (226).
- **The look serves the read.** Each screen has one word that carries the story (DELETE, PAM, DAD, DONNIE) and it is the biggest thing on it. A real-app detail that makes that word smaller is removed (226).
- **Light screens.** A dark call screen read worse than the old flat green one; the call is light green, the name in white, clear of the fingers on the grip's edge (226).
- **Nothing smaller than about 9 units** on a 100-unit screen. Helper text and placeholder lines are dropped, not shrunk (226).
- **Soft shadows, light gradients.** They lift the screen off the flat cartoon, but stay weak (the audit cut them 40 %) (226).
- **The same word everywhere.** The name on a screen is the name someone says aloud: DAD on the invitation because Don calls DAD (lesson 163 in *The Offer*'s notes).
- **No real brands, apps or logos.**
- **Status:** each screen tells its state by colour as well as text (green ringing, grey DECLINED), because the small text may not be read.

## Superseded

- **200** "an insert's arm is an arm: hand, elbow, frame edge": superseded by the owner rule (224) and the elbow rule (225).
- **201** "a SHORT forearm as wide as the hand, crop tighter": failed 3 of 3 at v30; only true at the frame's edge.
- **221** "`insert_arm` with shoulder and torso disc": the disc read as "a dome"; replaced by the owner's real body (224).
- **222** "hand + wrist stub only": true at the frame's edge only (224).
