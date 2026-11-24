# Rules: hands, arms and phones

The rules that hold now, gathered from lessons 147, 149, 163, 178, 179, 200, 201, 206–208, 221–226, 231 (episode 13 *The Offer* v26–v39, One Star v7–v9). Read this before drawing any hand, close-up arm or phone screen. When a lesson below disagrees with this page, this page wins; the superseded ones are listed at the end.

## 1. Hands and arms

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

## 2. Phone screens

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
