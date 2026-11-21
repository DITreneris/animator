# Office Noir 3: the lines, proposal v2 (20 Nov)

After an outside review of proposal v1 ("OK, not yet LOCK", 7.5/10) and Tomas: "the voice we are now using, lowered a bit, a real noir sound; think about the pauses between sentences and the intonation before generating." Nothing is in the film until he approves.

## The review, point by point

| Point | Verdict | Evidence |
|---|---|---|
| 2.0 "Word is, I know how business works." | OK, taken | shorter by one word; heard word for word in the new voice |
| 2.2 keep Mom's "Where are you going, skunk?" and then "My manager. Also my mother." | OK, but it undoes Tomas's note | Tomas marked Mom's car lines as out of place ("a voice from nowhere"). Since then her bubble has a tail to the car's window. The two lines take about 4.5 s on a shot of 1.2 s: the car shot is held about 3 s longer |
| 2.4b "One folder." | OK | |
| 2.7 "One number I never called." | OK, taken | makes four: one fight, one folder, one woman, one number |
| 3.1 "I've never been afraid of anything." | disagree | seven words on a shot of 0.8 s; and he is not afraid in the picture: he does not see the guns. "Nothing scares me." says it in three |
| 3.2 "I make my own fire." | OK, taken | |
| 4.4a "Your ticket. You're fighting." | OK, taken | the ticket reads FIGHT TONIGHT on the screen; all cold viewers since the ticket was drawn got "a ticket to his own fight" from the picture |
| 5.1c "Too late. The bell." | OK, taken; it shortens Tomas's line | "Ah" was heard as "are"; without it the line passes |
| 6.2 "It was a fair fight." only if the cheat is seen | OK | both viewers of test 40: "the boss in the office, not the robot… presses the desk button… only then does the punch land"; test 39: "they are in on it together" |
| 6.3 Don: "The woman in the photo…" pause "Recognize her?" | OK, taken | both viewers of tests 39 and 40 matched the photograph to the ring girl from the picture alone |
| 6.2b "Nobody move." only if he stops something | partial: cut | nobody is moving when he comes in: the Client sits on his stool, the robot waits. Don keeps three lines |
| 7.4 "Human approval still pending." | OK, taken | |
| 7.4 "better if approval cannot be had" | disagree | the film's joke is that approval is always given, at once, by her; that is on the protect list |
| 8.3 "I'll call her back tomorrow." | OK, taken | he declines her call in the picture |
| 8.4 "Tomorrow." the last word | OK | it is |
| Risk: N and Don sound alike | OK, real | both are low men's voices. N is now slow and dark; Don is to be quicker, drier and higher |
| Risk: Sofía's arc needs her reaction | partial | not a matter of lines; her face on the street is one nod |

**What correlates.** One: say less than the picture (6.3, 4.4a, 5.1c). Two: a repeat has to grow (the robot). Three: Mom's one sentence against his boast (2.2).

## The list, v2 (31 lines)

| Shot | Who | Line |
|---|---|---|
| 2.0 | N | Word is, I know how business works. |
| 2.1 | N | One fight. |
| 2.2 | MOM | Where are you going, skunk? |
| 2.2 | N | My manager. Also my mother. |
| 2.4 | MOM | Everything you need is in there. |
| 2.4b | N | One folder. |
| 2.5 | N | One woman. |
| 2.7 | N | One number I never called. |
| 2.6 | SOFÍA | Call me. |
| 3.1 | N | Nothing scares me. |
| 3.2 | N | I make my own fire. |
| 3.4d | DON | Just looking. |
| 4.3 | CLIENT, MOM | How much? / One hundred bucks. |
| 4.4 | N | I name my price. |
| 4.4a | MOM | Your ticket. You're fighting. |
| 4.4t | N | I don't believe in signs. |
| 5.1a | SOFÍA | Round one. |
| 5.1c | PAM | I'll help you undress. / Too late. The bell. |
| 5.3 | ROBOT | Human approval required. |
| 5.4 | MOM | Approved. |
| 5.6 | N | I don't break. I break even. |
| 6.1 | PAM | Some punch. Others patch. |
| 6.2 | N | It was a fair fight. |
| 6.3 | DON | The woman in the photo… / Recognize her? |
| 6.4 | DON | Case closed. |
| 7.1 | N | But I didn't quit. |
| 7.2b | REFEREE | Break! |
| 7.3 | N | Ten garages. That was the plan. |
| 7.4 | ROBOT, MOM | Human approval still pending. / Approved. |
| 8.3 | N | I'll call her back tomorrow. |
| 8.4 | N | Tomorrow. |

## The narrator: `on3_narration_audition_v2.mp4` (`src/on3_narr_noir.py`)

The film's own voice (am_fenrir), all 16 narration lines of this list.

| | Was | Now |
|---|---|---|
| Lowered | 4 semitones | 5 |
| Pace | the model's own | the speech itself 10% slower |
| Pauses | whatever the model left | written: 0.30 s at a comma, 0.50 s between sentences, 0.60 s before a line's turn ("My manager. / Also my mother.", "I don't break. / I break even.") |
| Intonation | not checked | every phrase ends on a full stop and its pitch is measured: all 21 phrases fall from their first third to their last |
| Sound | plain | closer and darker: more chest, no top above 6.5 kHz, a little tape, level held even, a small dark room very low |

Speech check: 15 of 16 heard word for word. Not passed at any pace: "I name my price." is heard as "I need my price."
