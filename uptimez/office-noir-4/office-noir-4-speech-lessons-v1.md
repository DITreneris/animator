# Office Noir 4: narration, bubbles, lips and blinks. Lessons to apply (v1, 24 Nov)

Collected from `docs/lessons.md` (line numbers), `uptimez/CLAUDE.md` and the code of Office Noir 1 to 3, before any text is
built. Nothing below is built yet.

## Decided already for this film (Tomas, 24 Nov)

- Text goes on approved motion, not before.
- Lips move only for speakers seen on screen; the narrator (Pam-Cat's voice) stays off screen.
- Bubbles and cards follow the earlier Office Noir films.
- A 540 preview first, then the 1080 master.

## The narrator's words (Pam-Cat, off screen)

| Source | Rule | For Office Noir 4 |
|---|---|---|
| lessons 568 (rule 33), CLAUDE.md G5 Text | Narration and cards go at the top, under the app's bar (y 96); never in the bottom quarter | Every narrator line is a card at the top |
| `on3_animatic._card` (Office Noir 2 and 3) | Typewriter face (Special Elite 30) on cream cards with a black edge and a soft shadow, left at x 18, from y 100, two rows at most | Reuse `_card` as it is. The longest line ("I know where to see what others do not see.") must fit two rows: to be measured |
| lessons 569 (rule 34) | A white line with an outline reads better than a dark band | Office Noir 1's first look; Noir 2 and 3 moved to cream cards. The cards are the later, approved practice: use the cards |
| lessons 610 (rule 46) | One headline and a small series label; three stacked cards shrink the picture | The title is one card; no subtitle card |
| lessons 551 | A tail can only end on a mouth that is on screen; an off-screen line is a quoted card | The narrator never gets a tail. Father's "For the boys." (only his hand is seen) is a quoted card with his name, no tail |
| CLAUDE.md G5 Speech | A card is on screen only while its line is spoken | Cards come and go with the takes' times in `on4_rough` |
| lessons 216 | A bubble's or card's clash list includes the signs and story props | Cards over the sky will cover the moon and the stars in 1.1, 1.4 and at the crossing: accepted when the sky was drawn, to be checked per shot |

## Bubbles (speakers on screen: Don, the Client, Pam-Cat, Sofia)

| Source | Rule | For Office Noir 4 |
|---|---|---|
| CLAUDE.md (after Daddy's Home v2) | New bubbles call `speech.draw`; the check is `speech_gate.check`; no other tail length or table | All bubbles through `speech.draw`, every frame through `speech_gate.check` |
| lessons 325, CLAUDE.md Tails | The box beside the face at mouth height; the tail 10 to 20 px, its tip on the cheek's outline, never on the mouth, eyes or hair | As is |
| lessons 357, 398 | Aim at the head as drawn in that drawing; measure, do not type offsets | Don behind the bonnet, Don leaning, Pam-Cat lying: measured per drawing |
| lessons 358 | A side bubble needs wall beside the face; if there is none, reframe the shot | "Not a scratch." (Don at the right edge behind the bonnet) and "Traffic flows." (Don at the left edge) have little wall: to be tested on the stills first |
| lessons 784 (rule 159) | The box stays put while its line is spoken; only the tail follows the mouth | As is |
| lessons 555 | Measure the safe area (18, 96, 522, 820) against every box | By `speech_gate.check` |
| lessons 802 (rule 169) | Never give a line to a speaker yourself | The speakers are in `on4_rough.NEW`; none is guessed |

## Lips and blinks

| Source | Rule | For Office Noir 4 |
|---|---|---|
| `motion_on3.alive` | Breath 0.7 %, blinks, lips from the take (visemes), poses tweened; `FROZEN` for the loop's ends | Reuse for Don, the Client, Pam-Cat on screen, Sofia; frame 0 and the last frame frozen |
| lessons 352 | A fixed face can ignore the spoken mouth: check that every speaking face takes the mouth | Don's "pleased" and "smug" faces checked on the stills |
| lessons 588, 594 | A re-cut moves every blink and lip shape; key them to the shot's own time | Lips and blinks keyed to shot time, since the cut still changes |
| lessons 834 (rule 198) | A listener points to the speaker: with no moving mouth the only face in shot takes the line | "For the boys." over Don's face in 3.3b: the card must name FATHER |

## Order of work

1. This sheet to Tomas.
2. Stills: one frame per line with its card or bubble, under the mock app overlay, before any render.
3. `speech_gate.check` on every drawing; six frames opened at full size.
4. Lips and blinks on the approved stills; then the 540 preview.
