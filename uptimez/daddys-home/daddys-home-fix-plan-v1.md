# Daddy's Home: fix plan v1 (22 Nov)

Animation v1 of all eight scenes is joined (`daddys_home_anim_v1.mp4`, 96.8 s, 540). A check against the tails-to-the-mouth
lesson (PR #62, `docs/lessons.md`) found that only 3 of 49 bubbles pass, 6 pass in part and about 40 fail. This plan
fixes that, together with the open items saved after each scene, and ends with cold viewers.

## Decisions (Tomas, /grill-me, 22 Nov)

| Question | Choice |
|---|---|
| Rounds | **2 fix rounds, then the cold test, then 1 round.** Then stop. |
| Scope of round 1 | **Bubbles + the known leftovers** (below). The trim to 95 s, music, room tone and 1080 are not in this plan. |
| Off-screen lines | **A quoted card with the speaker's name, no tail** (Mom's "Then stand like one, Donnie.", Father's "I prefer green in cash."). |
| Cold test | **2 fresh viewers, mute, plus direct questions,** on the whole film. |

## Round 1: bubbles

### A. One bubble for the whole film

The cause of all ~40 failures is one function: `dh_anim1.bubble` draws a straight triangle from a box at the top of the
frame to a point by the head, so every tail whose box sits above the head crosses it. It is replaced (opt-in, the old
function pinned) by one `speech()` used by all eight scenes, built on PR #62's rule:

1. **The box goes beside the head, on the side with wall,** in the top band (y 96 and down), never in the bottom quarter
   (y ≥ 720), never in the right rail (x > 470, y 380–860), never on skin, on a sign or on the price tag. Measured once
   per shot and held still; only the tail follows the head.
2. **The tail ends on the cheek at mouth height, on the box's side,** and curves round the outside of the whole head
   (hair, headset, crown behind it included). It never comes down from above.
3. **Overhead only onto the robot's antenna, touching it.** No bubble comes down onto Don's bald head either: the throne
   and the crown stand behind it.
4. **Off screen: a quoted card.** No tail; the name above the line (MOM, FATHER).
5. **On from the first syllable, off one drawing after the last word** (as now).

The head, face radius, mouth and cheek come from the rig in that drawing (Don, Father, the bodyguards and the repairman
from their rigs' points; Sofía, Pam and Mom from theirs; the robot from `dq.robot_state`), not from typed offsets.

### B. The check, on every drawing

`dh_tailcheck.py` renders all ~1,160 drawings and fails on any miss:

- the tail's tip is on the speaker's skin;
- walking from the tip toward the mouth, the mouth begins within 0.4 of the face's radius and only skin is crossed;
- the tail crosses no hair, glasses, eyes, headset, hat, crown or price tag;
- the box is on no one's skin, no sign and no price tag, and inside the safe zone above;
- the robot's tail touches the antenna;
- no tail on an off-screen line.

Before it is trusted it must catch five faults planted on purpose: a tail down over the forehead, a tip on Pam's fringe,
a gap at the robot's antenna, a tail to the frame's edge, a box on the price tag.

### C. The known leftovers, scene by scene

| Scene | Fix |
|---|---|
| 1 The Call | Redraw the hanging drawing (0.2b) with his knees at his chin. Keep the price tag clear of the top of Don's head in his close shots. |
| 2 Good News | The bared-teeth grin reads as a grille: redraw it. The throne leaves the frame in ~0.3 s: more drawings on the same length. Sofía and Pam frozen for 0.4 s: one blink and a breath. |
| 3 The Green Star | Mom's mouth moves with her lines. Sofía's frightened face without the row of teeth. Don's single in front of bare wall: frame it with the screen's edge or the throne. |
| 4 The Wrong Man | The repairman's mouth moves with his lines (a mouth for his rig, as Don's). The cut corner of the coffee machine out of Pam's shots. |
| 5 The Filter | Don's close shots less crowded (tag, filter, crown, bubble). The flinch three-shot closer. Pam higher in her last shot. Repairman's mouth (from scene 4). |
| 6 Mom | Sofía's frozen smile held longer at the end (the shot keeps its length; the confident part gets shorter). One paper in her hands in 8.4a. The 8.2 two-shot closer. Mom's line becomes a quoted card. |
| 7 The Arrival | The knocking fist drawn as a fist. The step drawn as a step, not a straight leg. The 9.4 two-shot framed so both faces sit inside. |
| 8 Find My Money | The phone on the arm clear of Don's hand. The price tag clear of Don's hair in the robot's view. The shuffles held a drawing longer. Father's raised eyebrow bigger. Father's first line becomes a quoted card. |

Not in this plan: the trim to 95 s, music and room tone, the 1080 master, rebuilding the scene sheets and the animatic.

### Gate 1

- `dh_tailcheck.py` passes on every drawing, and its self-test catches all five planted faults.
- The speech check (Whisper, three windows) on the joined mix: every line heard at least 2 of 3.
- A thumbnail sheet at 270 px of one drawing per line.
- The joined film rebuilt (`daddys_home_anim_v2.mp4`) and the loop file; frames counted.
- **Tomas watches it.** His notes are round 2.

## Round 2: Tomas's notes

Only what Tomas raises on v2, plus anything the check catches after those changes. Same gate. Output:
`daddys_home_anim_v3.mp4`.

## Cold test

Two fresh agents who have seen nothing of the series, as in `cold-viewer-mute-test`:

- Contact sheets of the whole film at 4 fps, numbered, with time stamps; an 8 fps sheet for the beats under 0.5 s (the
  seat's drop, the BANG, the POP and SLAP, the zip, the knocks, FOUND); one sheet at feed size (270 px).
- No sound, no bubbles.
- My intended reading is written first, one beat per scene (8), and not shown to them.
- After the open prompt, direct questions on what the jokes depend on: who rings Don at the start and at the end; what the
  throne cost and why Don hides it; who the man with the metal case really is; who approves Father at the door; what the
  robot's camera finds; what Mom does to Pam and to Sofía.
- **Pass: both tell back at least 7 of the 8 beats.** A beat both misread the same way is a staging fault and goes into
  round 3.

## Round 3: the cold viewers' shared misreads

Only those. Then the film goes to Tomas, and the plan stops here (the two-review-round rule): the trim, music and 1080
are the next plan.

## Order of work

1. Pin the files that change (`_vN`), build `speech()` and `dh_tailcheck.py` with its self-test.
2. Scenes 1–8 one at a time: bubbles, then that scene's leftovers; the check on that scene before the next.
3. Gate 1 on the whole film → Tomas.
4. Round 2 → gate → Tomas.
5. Cold test → triage table (beat, intended, viewer A, viewer B, verdict, fix).
6. Round 3 → Tomas.

Nothing is committed until Tomas asks.
