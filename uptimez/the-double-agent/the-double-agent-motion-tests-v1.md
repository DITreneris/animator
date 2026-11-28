# The Double Agent: motion tests v1 (stage 6, 27 Nov)

`src/da_motion.py` → `da_motion_{A,B,C,D}_v1.mp4` (15 drawings a second, 30 fps) and 8 fps strips. Two fresh viewers on the strips (neutral names, no context).

| Test | What reads | What fails (both viewers unless noted) | Fix |
|---|---|---|---|
| A 5.3 the slip | the launch with the cup flying (funniest, both); lying stunned, the coffee spill | **no cause**: the clips under his foot not seen; the take-off one drawing (too fast); the hang 5 drawings flat and stiff ("levitating", "an invisible table"); lying, his legs read as a box | a contact drawing: the foot on the clips, the clips spraying, 2 drawings before the launch; clips bigger; the hang 2–3 drawings and still rotating (an arc, not a hold); the legs on the floor drawn as legs; the end hold halved |
| B 3.4 Mom the goalkeeper | she stands her ground, no contact (both) | her steps not seen; overlapped behind her, his head stacked on hers ("totem pole"); her curler read as a purple phone at his ear; his moves pop (no in-betweens); the end shock has no cause | side by side with a gap (no overlap), each step with a lift and an in-between; his end face frustrated, not shocked |
| C 7.2 the tape gate | he lifts the tape himself, no contact (both); her quiet exit while he beams (funny, 1) | **two yellow lines**: the floor stripe stays while a second lifts; she slides with no legs moving; the lift one drawing (a whip); the ending empty | the strip peeled out of the floor line itself (its bare stripe on the floor); her walk framed from the knees up, or a step pose; the lift over 3 drawings; the end cut short |
| D 6.5–6.7 Pam's choice | the snap from shock to deadpan (funniest, both) | the shock hold 1.2–1.5 s too long; her start face already reads annoyed; the look up at the glass reads as "suspicion" | the shock hold to ~0.4 s; a softer start (pleased); keep the side-eye |

## Round 2 (v2) and round 3 (v3), two fresh viewers each, 27 Nov

| Test | v2 | v3 | Verdict |
|---|---|---|---|
| A the slip | the cause reads (2 of 2: "slips on the bits, nobody touches him"); the cup "from nowhere"; the take-off one drawing | the cause reads (2 of 2), the cup in his hand from the start; frame 9 upside down "a great silhouette"; still the take-off fast, the mug vanishes after landing, the end hold long | **pass**; polish: one more in-between, the mug lands in the puddle, the end hold halved |
| B Mom the goalkeeper | his raised knee read as a kick or an ankle hook (2 of 2); the throne's black back behind his head read as "another man with dark hair" | — | **fail** (her block: 4 layout rounds + 2 motion rounds); 3.4's tiptoe pose read in round 6 |
| C the doorman | the door opens "by itself" (her hand up high, read as a wave); everything tiny | the door is hers now, but his bow reads as pointing at the floor or dismissing her; intent unclear (2 of 2); both cut by the frame's edges | **fail** on mute; the line "Approved." and the sound not in the test |
| D Pam's choice | the snap from shock to deadpan "the best beat of the four" (2 of 2) | same; the end hold long | **pass**; polish: the end hold shorter |

## Round 4 (v4, 240 px tiles), two fresh viewers, 27 Nov

| Test | Result | Verdict |
|---|---|---|
| A the slip | the cause reads (2 of 2: "the foot on the pile, the bits spraying"); frame 9 the funniest (2 of 2); 6→7 still fast | **pass**; polish in the animation: one more drawing at the take-off |
| C the doorman (C2) | "a bow, a point, a sash or a dance?"; the door "opens behind her"; "no clear joke"; tiny at this size (2 of 2) | **fail**: the doorman's third version on mute (after the tape gate's four rounds) |
| D Pam's choice | gasp → eye-roll → flat, read (2 of 2); the eye-roll one drawing, easy to miss | **pass**; polish: the eye-roll 2–3 drawings |

## Round 5 (v5, 28 Nov): C the close bow (Tomas: 1), D polished; two fresh viewers

| Test | Result | Verdict |
|---|---|---|
| C the doorman, close | "presenting, like 'ta-da' or 'after you'", "a game-show host: behold!" (2 of 2); "nothing where he points" (the door is off screen: the door's sound and the cut to 7.3, Pam inside, pay it off); the hold long | **pass** on the gesture; the payoff is the cut and the sound (check in the rough cut) |
| D Pam's choice | gasp → eye-roll ("ugh, whatever") reads (2 of 2); the eye-roll still short (2 drawings), the gasp a little long; "only her face moves" | **pass**; in the animation: the eye-roll 4 drawings, a shoulder drop with it |

All four tests now read their action: A the slip (rounds 3–4), C the close bow, D Pam's choice; B (Mom the goalkeeper) cut (3.4b, Tomas). Board: 40 shots, 71.4 s; animatic v2.

## Stage 7 decisions (Tomas /grill-me, 28 Nov)

- Order: scene 1 (1.1–1.5) animated first, shown as a 540 preview plus a strip; the look agreed; then scenes 2–9 without stops, to the rough cut (stop 4).
- Music: the series theme, little: at the start and the end, quiet under the voices; one noir sting for 5.1's mug.
- Effects: better synthesis (no licences, rebuilt from code), replacing the animatic's drafts.
- Mouths: automatic phonemes from the takes' word timing (Whisper), with the key lines checked and fixed by hand ("NOT THE CHAIR!", "Your rule, sweetheart.", "Approved.").

## Round 6 (28 Nov, Tomas "aštrinam"): scene 1's physical gag

Two new tests in `da_motion.py`: **E** (1.2, the shin whack as a hit: the foot comes up, a kick, the roll swings out and round with a smear, contact on one drawing with hit marks and a jolt, eyes shut, then the layout's key pose held for "Oof") and **F** (1.3, the release: the robot lets go with its hands up, the throne lurches 50 to Don's side, Don goes back two hops on one leg and lands on his mark, and only then the shoes step in). v1 and v2 each (v2: a higher swing, longer hops). Two cold viewers on the 8 fps strips (clip names neutral):

| Beat | Intended | A | B | Verdict |
|---|---|---|---|---|
| E: the roll is stuck to his shoe | dangles off the sole | "something stuck to his shoe", object unknown | "hanging off his raised foot", tape only after clip 2 | read (what the object is: only from context) |
| E: the swing | kicks, it swings round | "springs up like a stepped-on rake" | "flips up and back" | read |
| E: the whack on his other shin | contact, wince | read, "best gag", F5 | read, "best gag", F5 | **read 2/2** |
| F: the robot lets go, so he flies back | release → hops | "angry lunge at the line" | "pain hop" | **missed 0/2** |
| F: frozen by the shoes over the line | freeze | read | read, "scale gag" | read 2/2 |

The whack works. The release doesn't read in the S1 wide: the robot is small, Don's hand is not on the throne before it lets go, and the hops read as pain. In the film it still plays as a pain hop into the freeze, which is fine; the release as its own gag would need his hand on the armrest in drawings 1–2 and a closer camera (the 1.3 layout is approved, so that is Tomas's choice).
