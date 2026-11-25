# One Star: bubbles and tails, the rules and the plan (v1, 25 Nov)

v13 and v14 have no bubbles: all 16 lines are voice only. Per `uptimez/CLAUDE.md` step 1, the rules first, then the
plan per line. Nothing is built until Tomas picks.

## The rules that apply (uptimez/CLAUDE.md, docs/lessons.md)

| Rule | Source |
|---|---|
| New bubbles call `speech.draw`; the check is `speech_gate.check` on every drawing (safe rect, 10-20 px tail, the button rail, `avoid=` signs, props and hands) | CLAUDE.md 62-67 |
| The box beside the face, level with the mouth, a short side tail whose tip lands on the cheek's outline at mouth height; never on the mouth, eyes or hair | CLAUDE.md 63; lessons 167, 174, 325 |
| Overhead only onto bare scalp (Don) or the robot's antenna, the tail touching; anyone with hair gets a side bubble or a new framing | lesson 359 |
| No wall beside the face: reframe the shot, never shrink the text | lessons 358, 1026 |
| Off-screen or on-a-screen speakers: no tail; what a screen shows is the line (typed is not spoken) | CLAUDE.md 63; lessons 175, 784 |
| A bubble lives as long as its line: on with the first syllable, gone one drawing after the last | lesson 362 |
| Placed once per picture (one camera, one text), laid over the frame after everything, so a jolt, a breath or a camera ease does not move it; only the tail follows the mouth | lessons 784, 1016-1017 (`of_scenes.lock_bubble`) |
| The clash list includes signs, story props and a gesture that carries the line (`protect`); a moving prop's whole path is protected | lessons 216, 988 |
| The robot speaks in its own tinted mono bubble, bold, over its visor, never across its card or paddle | lesson 954; `speech.ROBOT` |
| The Offer's settings: SIZE 30, MONO_SIZE 28, MAX_W 300, MONO_BOLD, SIGNS_FIRST; a line over 3 rows goes over the head | lesson 954 |
| Text under the bar (y 96), off the right rail and out of the bottom quarter | CLAUDE.md 62 |
| The last bubble is gone before the loop's last frame | lesson 465 |
| Check with pixels: draw each frame with and without the bubble; a check never reads the numbers the drawing was made from | lessons 269, 348 |

## The plan, line by line

| Time (v14c) | Line | On screen | Bubble | Why |
|---|---|---|---|---|
| 1.4-6.2 | CLIENT "Paid $999. They lost my blueprint. My lawyer will call." | the post | **none** | the screen is the line |
| 6.3-8.6 | ROBOT "Reply drafted. Human approval required." | Don and the robot; Don's hand goes to the antenna at 1.8-2.4 s into the shot | **decide** | an overhead tail onto the antenna meets Don's grabbing hand |
| 8.8-9.5 | DON "Approved." | the same two-shot, his finger on the visor | overhead, onto his crown | bald; the wall above both is clear |
| 11.0-12.2 | DON (the reply) "Stupid human." | the reply on the phone | **none** | the screen is the line |
| 13.5-15.0 | DON "Let's fix this together." | Don, the phone in front; the camera pans down from the calendar | side, the wall on his left | **decide**: the pan moves the face under the bubble |
| 15.5-17.2 | CLIENT (phone) "Nine o'clock. Your office." | the calendar filling | **none** | his voice through the phone; the calendar is the caption |
| 17.9-20.3 | ROBOT "Blueprint generated. Human approval required." | the sheet shooting out, Don's lunge | overhead onto the antenna, mono | the action is low (slot, floor, his arm): the wall above is free. Protect the sheet's path and his arm |
| 20.5-21.2 | DON "Approved." | Don looking at his empty fist | overhead onto his crown | the robot's head is beside his face |
| 25.5-26.3 | DON "Recovered." | over the Client's shoulder, the sheet | overhead onto his crown | the sheet fills his sides |
| 28.8-29.8 | CLIENT "Is this a joke?" | the Client, the ball in his raised fist | side, left of his face | hair: side only. Protect the fist and the ball, and the throw's path after |
| 36.6-37.7 | PAM "Check your pocket." | Pam by the door, pointing; the Client | side, left of her face | **reframe**: the door frame leaves no wall now |
| 41.8-43.9 | ROBOT "The result was obtained by a h-human." | the robot's FOUND BY: HUMAN paddle | **decide** | the paddle already says it; a bubble competes with the sign |
| 45.3-46.2 | CLIENT "Your number." | the Client with his phone, Pam, Sofía | side, left of his face over Pam's head | Sofía on his right |
| 52.1-53.4 | DON "Customer success." | Don and Pam | overhead onto his crown | Pam's face beside his |
| 59.2-60.9 | PAM "Some post. Others find." | her reply on the phone | **none** | the screen is the line |
| 61.4-62.3 | SOFIA "Still one star." | Sofía with the tablet, ★ 1/5 | side, left of her face | protect the tablet; gone before the loop's wide |

10 bubbles, 4 lines carried by screens, 2 robot lines and 1 pan to decide.

## No bubble during the gags

The opening (0-2.2 s), the antenna and the toss, the sheet's run and the roll at the door, the throw and PLOK carry no
line; no bubble may cover their paths (the flying phone, the arcs, the ball).

## Built (v15, 25 Nov, Tomas's picks)

`src/cs_say.py`, `src/cs_film_v15.py` -> `one_star_rough_v15.mp4` (sound identical to v14c). 12 bubbles placed,
`speech_gate.check` clean on every one at 1080. Decisions: the robot's first line beside its visor (it holds Don's phone
low in 1.4 so that wall is free); 4.4 a small box right of the sign, the tail onto the antenna; 2.1's pan lands before
the line. Reframed for the bubble (lesson 358): 1.4 (both 90 px right), 4.2b (zoomed out, Pam off the edge), 4.4 (60 px
left). Found on the way: at 1080 a half-size copy of the rigs is drawn on a scratch pass; the bubble keeps one head per
rig (the largest), or the check sees a face that is not in the frame.
