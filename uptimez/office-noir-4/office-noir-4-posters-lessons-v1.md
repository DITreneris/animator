# Office Noir 4: town bills and signs, lessons applied (v1, 24 Nov)

Rules taken from `docs/lessons.md` (line numbers) before drawing the bills in `src/on4_posters.py`.

| Line | Lesson | How it is applied |
|---|---|---|
| 335 | No cropped words: a sign whole or not at all | `on4_posters.whole()` checks the shot's camera; the club bill is left out of the close cameras (T8, 4.3, T12). The crossing and lane bills sit inside every camera that sees those walls |
| 590 | Reframe before you hide | The lane bills were shrunk to 0.76 so the third clears the right edge; nothing in the set moved |
| 529 | Signs read at 270 px | Checked on `on4_posters_stills_phone_v1.png`: THE CAT, HUMAN / ROBOT, UPTIMEZ INC., CABARET read in the close cameras; the small lines do not in the wide (3.4) |
| 626 (rule 59) | Props carry one job; no posters without a job | Pam-Cat's bill sets up the stage act. Human vs Robot and the TV show are series in-jokes with no job in this story: Tomas's pick, kept, flagged |
| 450 | A background gag that cannot be read is a distraction | Bills at 0.74-0.78 of 96 x 136, one big word each |
| 744 (rule 125) | Story props out of the dead zones | Her bill is left or centre in each place; only the fight bill in the lane enters x > 470 |
| 216 | A bubble's clash list includes the signs | Open: the CABARET board at the crossing is at y 57-103 px, where narration cards start (y 96). To settle when the text is built |
| reuse | Reuse approved work | The fight bill is Office Noir 3's `street_on3.poster2`, unchanged |

Protect rule kept: her bill shows a silhouette with ears, never her face. Red: only the heart on her bill (exact NEON).
Opt-in: `on4_posters.ON[0]`, default False.
