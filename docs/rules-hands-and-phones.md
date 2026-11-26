# Rules: hands, arms and phones

One page for the whole repo, UptimeZ and Hoodyz. This page wins when `docs/lessons.md` disagrees. A new job is a new row here, written before any episode draws it. An episode does not get its own hands file.

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

The picture of this table is the class sheet, `uptimez/the-blueprint/rough_work/pic_hands/bp_hand_classes_v4.png`: male width 17, female 15, the same shapes, no nail. It is the target. Its `grab`, `pinch`, `fist` and `phone_grip` are drawn by the sheet scripts, so a film that calls the function in this table still gets the older drawing until a separate opt-in module exists. How a row changes: [`uptimez/CANON.md`](../uptimez/CANON.md).

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
