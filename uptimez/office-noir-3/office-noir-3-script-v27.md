# Office Noir 3: The Last Round — script v27 (line by line, with the shot list)

UptimeZ Inc. · the Client's dream · between episode 10 (*First Search*) and episode 11 (*Customer Success*) · for review · nothing is drawn from this yet · scripts v1 to v26 and concept v1 are kept

**v27, 20 Nov:** the whole film is on one board (`src/board_on3.py`, 70 frames, `on3_board_v1.png`) and **passed the whole-board cold test with the loop question: 5 of 5 and 5 of 5, and the loop closes for both** (`cold_test_whole_board_v1/result.md`). Before it (Tomas: proceed; taken as option 1): **only the deck lies on her desk until he has paid; then her other hand deals the top card and turns it: the Tower** (redrawn: courses, windows, a door, the crown going over, a thick bolt). With that the hundred is the price of the fight again ("he paid for his own knockout, and the Tower card says as much"). In 8.4 the arm that hung to the phone lays it on the CV. Open, shared by both viewers: the hand that turns the card is taken for another person's; 10 GARAGES is read as his goal, not his own plan; her hand at the car window reads as "a monitor"; Don from behind is not known.

**v26, 20 Nov:** after two outside reviews (Tomas: improve). **Beat 04:** in 4.2 his glove shoves the folder down as his eyes go up to the roll (a look was not read); the hundred is drawn as money; her fingers bend over the note's far edge and it comes toward her; the door is beside him, ajar; 4.4c, his face over the card: one squint, then as before. **Beat 08:** he is drawn lying, one arm hanging to the phone on the floor; in 8.4 the gown is over his eyes and his other arm lays the phone on the CV; her photograph is clipped to the CV; the plan has left its ghost on the wall; the tube and the hook are out. Tests: `cold_test_garage_v2/result.md` passes (4 and 4); `cold_test_beat04_v2/result.md` fails (3 and 3) on one cause: **with the cards on her desk the hundred is read as the price of a reading, not of the fight.** Open, for Tomas. 46 set-ups.

**v25, 20 Nov:** tarot cards are back on her desk (Tomas: the desk looked empty; this undoes v19's "the button and the coupe, nothing else"), and she turns one (Tomas, /grill-me). **Three cards lie face down, the deck beside them. At the end of 4.4, one hand on the hundred, she turns the last card with the other: the Tower, struck. She does not look up.** The card has an insert of its own, 4.4b. Passed its cold test first time (`on3_office_tower_v1.png`, `cold_test_office_tower_v1/result.md`: 5 and 5). Both viewers now read the hundred as the price of a card reading: "One hundred bucks. For the fight." has to carry the rest. 45 set-ups.

**v24, 20 Nov:** the last two pieces are staged. **The arena door** (`src/door_on3.py`, `on3_beat04_frames_v1.png`, `cold_test_beat04_v1/result.md`: passed narrowly at the second round, 4 and 4): 4.1 from behind him, the ring small through the door; in 4.2 her photograph sticks out of the folder under his arm; in 4.3 the hundred is held out whole past his glove; 4.4 starts with the note still between his gloves. **His garage office, awake** (`src/garage_on3.py`, `on3_garage_frames_v1.png`, `cold_test_garage_v1/result.md`: passed at the second round, 4 and 4), the film's only colour. The phone says INCOMING CALL (CALLING was read as him dialling); in 8.4 his arm comes out from under the gown and lays the phone face down on the CV; where the plan was pinned, four torn corners are left; the hook is bare and the tube lies on the floor, PLAN on it. Open: 4.2 is still a look, not an action; the tube is taken for the plan itself.

**v23, 20 Nov:** the alley's shadows are redrawn after an outside review (set v2: `src/alley_on3.py`, `on3_alley_frames_v2.png`, `cold_test_alley_v2/result.md`; passed at the second round, 5 of 5 for both). **The three are men now, each different:** a lean one bent forward with a knife held low, the big one in the middle with the tommy gun, a fifth larger and darker, his head sunk between his shoulders, and an upright one with a bat on his shoulder; snapped brims, turned-up collars, bent arms, legs. **They close in** between 3.1 and 3.2, and turn to watch him go. **The matches get a shot of their own (3.2b):** once the men were a real threat, both viewers took his gloves for crossed arms and the lighter for a bribe he refuses. **The flame reaches the cigarette and it burns.** 44 set-ups.

**v22, 20 Nov:** the alley is built and staged (set v1: `src/alley_on3.py`, `on3_alley_frames_v1.png`; Tomas, /grill-me) and passed its cold test first time (`cold_test_alley_v1/result.md`). **It is the gap beside the arena,** off the street, with the arena's light at its far end. **The gunmen are shadows on the wall and nothing else:** three hats and coats, a tommy gun, a bat, a knife; the men are never seen. **One real hand, a white cuff, comes out of a shadow with a lighter; the weapons go down while it does.** The finger stays cut.

**v21, 20 Nov:** the street passed its cold test at v3 (`on3_street_frames_v3.png`, `cold_test_street_v3/result.md`: 5 of 5 for both). What it took: **Sofía on the street and in the photograph is the star of Office Noir 2, her gown black here** (his gloves stay the only red); in the ring she is the ring girl, as before. **The page is seen photograph first** (her picture alone, clipped over the heading: a contract), **then the photograph is lifted on its clip: The Onboarding's sheet,** CV, lines, her number circled. **The lipstick telephone is out.** **The finger is out** (2.3 is cut): a raised boxing glove read as a wave in two tests. Six glove gags remain. 43 set-ups.

**v20, 20 Nov:** the street is built (set v1: `src/street_on3.py`, `on3_street_frames_v1.png`; Tomas, /grill-me). It is **outside the arena, at night**: the arena's wall and fight posters, one lamp, the arena door at the far end, so beats 02 and 04 share a place. **Mom at the car is a ringed hand at the rear window and no more;** her face is first seen in her office. **2.4 is his view into the car.** **Sofía passes under the one lamp.** Its first cold test missed by one (`cold_test_street_v1/result.md`): the raised glove reads as a wave, and the CV reads as a come-on. Both are open.

**v19, 20 Nov:** Mom's office is built (set v1: `src/office_on3.py`, `on3_office_set_v1.png`; Tomas, /grill-me). It is **a back office over the arena**: blinds on a window that looks down on the ring's glow, which she never turns to; the light lies in stripes on the wall behind her. **On her desk: the button and the coupe, nothing else.** The cash box, the croupier's rake and the tarot cards are out of the film: in 4.4 her ringed hand covers the note; in 6.2 she holds the hundred up and counts it again; in 7.4 she presses the button without looking, and no card is turned. **4.3 is over his shoulder, 4.4 is her view of him.** The staging passed its cold test (`cold_test_office_v1/result.md`). The ring's rough is at v3 on the real office (`on3_ring_rough_v3.mp4`).

**v18, 19 Nov:** first-person views (Tomas, /grill-me). **5.2a, the bell: four fast cuts round the ring** (from the front, his view of it, its view of him, from above); a true orbit is not drawn: the ring is a flat cut-out seen from one side. **5.3 is the robot's own view:** his glove stopped a hand from the lens, and HUMAN / APPROVAL / REQUIRED comes up over his face. **In 5.5 the jab is seen through his eyes:** the grey glove fills the frame, black; then he is down. **In 7.3 he claps the plan's hung end between two gloves** and it slides up and out (this replaces the one-glove version). The film's first and last drawing, the glove landing on his face seen from outside, is unchanged. The ring's rough passed its cold tests at v2 (`on3_ring_rough_v2.mp4`, `cold_test_ring_rough_v2/result.md`). 44 set-ups.

**v17, 19 Nov:** /grill-me (Tomas). **The watch gag is cut from 5.6** (unread in three cold tests): seven glove gags remain. **In 7.3 the paper slides off the glove:** he gets the glove against the plan's hung end, it slips over the leather and swings away. **Don at the ring is Office Noir 2's detective, unchanged.** Beat 05's rough passed its cold test at v4 (4 and 4 of 5); beats 06 and 07 have a first rough (`on3_beat0607_rough_v1.mp4`, about 3 of 5: `cold_test_beat0607_rough_v1/result.md`); the whole ring plays as `on3_ring_rough_v1.mp4`.

**v16, 19 Nov:** **Mom sits** (Tomas). In every office shot (4.3, 4.4, 5.4, 6.2, 7.4) she is seated behind her desk in a high-backed chair and never gets up; he stands in front of it. Her office has a lit wall behind her: a black coat in a dark room did not read. The rough of beat 05 is at v5 (`on3_beat05_rough_v5.mp4`).

**v15, 19 Nov:** **in 5.2 the Referee stands behind the robot** (Tomas, after four cold tests: there, every viewer saw a punch that stops short; between them, none did). A moving rough of 5.1a to 5.2 exists (`on3_beat05_rough_v1.mp4`); its cold test read the robe gag for the first time and missed the pass mark by one (`cold_test_beat05_rough_v1/result.md`).

**v14, 19 Nov:** the second /grill-me (Tomas) and cold test 4 (`cold_test_ring_v4/result.md`). **The plan carries a title block: 10 GARAGES.** It stays his own plan, not a prize. **The Referee wears a black waistcoat.** **In 5.1a he is already in his corner:** his arrival is 4.1; three tests never saw him come through the ropes. **Open, for Tomas:** where the Referee stands in 5.2. Between them, every viewer of tests 3 and 4 took him for the punch's target; behind the robot (tests 1 and 2), every viewer saw a punch that stops short.

**v13, 19 Nov:** after two failed cold tests of the ring's first frames and /grill-me (Tomas). **The plan has a shot of its own:** 5.1b, his view of it from below, one second, his glove coming up toward it; a look at it was not read by any of four viewers. 5.1 is now three shots (the master, his view, the robe). **In 5.1a he is caught stepping through the ropes,** Pam holding them up. **In 5.2 the Referee stands at the far ropes, halfway between them.** 42 set-ups, about half a second longer. A third cold test (`cold_test_ring_v3/result.md`) read the plan and the Referee and misread the punch; that is open.

**v12, 19 Nov:** the ring is built (set v1: `ring-set.md`, `on3_ring_set_v1.png`, `on3_ring_plan_v1.png`, `on3_ring_blocking_v1.png`), and two things its first frames showed are decided (Tomas). **5.1 is two shots:** 5.1a, the master, for the room, the plan and Sofía; 5.1b, his corner, for the robe. In the master he is about 140 px tall and the robe gag did not read. **In 5.2 the Referee stands behind the robot,** not between them: between them, the stopped glove read as landing on his shirt. 41 set-ups; the length is unchanged.

**v11, 19 Nov:** Pam and the Referee, sheet v6 (Tomas, /grill-me): `characters/uptimez-corner-on3-v6-sheet.png`. Pam is a corner hand: sleeves rolled, a dark stained work apron, the towel round her neck; the cotton bud is out. The Referee's sleeves are rolled to the elbow. In 5.1 the robe comes off his shoulders and down to the belt before the sleeves stop at the gloves: he stands bare-chested for a moment, then she pulls it back on.

**v10, 19 Nov:** no change to the film. Pam and the Referee are at sheet v4 (`characters/uptimez-corner-on3-v4-sheet.png`): his hairline is higher in every drawing, so in 6.4 only the eyebrow moves; and the eyebrow is a close-up, never asked of a wide shot.

**v9, 19 Nov:** Pam and the Referee, sheet v2 (`characters/uptimez-corner-on3-v2-sheet.png`), after the outside review. One change to the film: **Pam's stopwatch has a job.** She clicks it on the bell (5.2) and holds it up through the count (5.6). On the sheet: the Referee's sleeves are shaded off his chest, his eyebrow is bolder (the other brow comes down), his idle hands are open; Pam's frames are dark. Her eyes, her cap and the cord are unchanged.

**v8, 19 Nov:** Pam and the Referee (Tomas, /grill-me), brought in line with their sheet, `characters/uptimez-corner-on3-v1-sheet.png`. The cast is complete.

| | v7 | v8 |
|---|---|---|
| **Pam** | "A towel and a roll of tape" | His cutman: the flat cap and apron of Office Noir 2, sleeves rolled, a dark stained work apron, a towel round her neck, a stopwatch on a cord. A bucket and a sponge by the post. In 6.1 she squeezes the sponge over his head, then tapes his brow |
| **The Referee** | "A white shirt, a bow tie, slicked hair, bare hands" | The Bartender of Office Noir 2 without his glass, as drawn: bare forearms, black bow tie. Checked beside the Client as black shapes: they do not share a silhouette |
| **Sofía and the Referee** | Not said | She does not notice him. Her eyes stay on the Client |

**v7, 19 Nov:** after the outside review of the robot's sheet, and Tomas's answers (1A 2A 3A).

| | v6 | v7 |
|---|---|---|
| **The plan over the ring** (1A) | A roll on a rope, turning | Hung level on two cords, one end let down so the drawing shows: the ten bays, the L-shaped one solid (`src/props_on3.py`). A vertical roll over a ring read as a microphone |
| **His face in frame 0** (2A) | Wide eyes from the first drawing | HARD in the first drawing, eyes on the glove. The glove lands, and only then the face folds and the eyes go wide. The same in 7.5, so the loop holds |
| **The fight's rule** | Implied | It asks, everything stops, the tick, one punch, it asks again. His swing in 5.2 stops a clear hand short of it: he never touches its screen before the words go |
| **Phone checks** (3A) | Three small staged shots per character | The figure alone at three sizes. Shots are staged once, at the board, on the set |
| **The robot** | Sheet v1 | Sheet v2: one grey value per part, and the crack along the screen's rim so the words stay whole |

**v6, 19 Nov:** the robot (Tomas, /grill-me), brought in line with its sheet, `characters/uptimez-robot-on3-v1-sheet.png`.

| | v5 | v6 |
|---|---|---|
| **Who it is** | "The robot, gloves on its claws" | The same small HR robot, drawn smaller than the Client. Big grey gloves on two piston arms; a steel yoke over its shoulders carries them; two outriggers with casters beside its wheel, so a punch does not tip it. A champion's belt under the HR badge |
| **Its face** | A proud face, and a separate chest screen for the words | One screen, its face: FURIOUS in the ring, the three words when it asks, the tick, PROUD between rounds. From 7.2 the screen is cracked, and it still asks through the crack |
| **Its corner** | It oils its own elbow | It cannot: it has gloves on too. A small service arm on the yoke tips the oil can; a cable runs from its back to a socket in the corner post |

**v5, 19 Nov:** Mom's place and Mom's things (Tomas, /grill-me).

| | v4 | v5 |
|---|---|---|
| **Where she is** (Tomas) | On a high chair inside the arena door, then at ringside | **In her own office,** never at the ring. A desk, a lamp, blinds; behind her, through the blinds, the ring's light. She does not turn to it once |
| **How her word reaches the ring** | She says "Approved." beside the ring | One ringed finger comes down on a button on her desk; the robot's screen flips to the tick. The cause is on screen, and she still has not looked |
| **Her hand on the note** | Her hand takes his hundred | Her ringed hand comes across the desk and covers the note where he has laid it (4.4). She never touches him. (v19: there is no rake) |
| ~~The tarot card~~ | None | Cut in v19: no cards on her desk. At the last "Approved." she presses the button without looking (7.4) |
| **The champagne** | None | A coupe at her elbow in every office shot. She does not drink it |
| **The table** | A high chair | Her desk |
| **Her look** | To be developed | `characters/uptimez-mom-on3-v2-sheet.png`; her car is `src/car_on3.py`, a 1940s limousine |

Sets go from five to six (her office). It can be built on the first Office Noir's office: the blinds and the side light are already there.

**v4, 19 Nov:** how he fights (Tomas): in the robe, because he cannot get it off.

| | v3 | v4 |
|---|---|---|
| **In the ring** | He boxes in the robe; no reason given | At the bell Pam tries to pull the robe off him and the sleeves stop at the gloves (5.1). He boxes in it because it will not come off |
| **Glove gags** | Eight, the first being the pocket on the street (2.1) | Still eight: the pocket is out, the sleeves are in |
| **The Client's look** | The robe everywhere | A charcoal tracksuit on the street, the robe from the ring on, a hard face (sheet v2); already written into v3's rules, and unchanged here |

**v3, 19 Nov:** script v2 with Tomas's two additions. What changed:

| | v2 | v3 |
|---|---|---|
| **Glove gags** (Tomas) | Four | All eight are back. The four returned ones sit inside shots that were already there (2.1, 2.5, 5.6, 6.4), so no set-up is added for them. No two are next to each other, and each costs him more than the last: comfort, face, money, the plan |
| **The Referee** (Tomas) | None | The Bartender of Noir 2, in a white shirt and a bow tie. Three jobs: he counts over the Client with bare fingers (5.6), he sees Don take the folder and raises one eyebrow (6.4), and he says the one word that stops the Client when he is winning (7.2b) |
| **"Break!"** (Tomas picked A) | The Client stops hitting the robot for no reason | The Referee steps in: "Break!" The Client obeys, steps back, looks up at the roll. Then "Approved." It also answers "I don't break." |
| **"One fight."** | Open | Stays, as Tomas wrote it |
| **Length** | About 69 s, 38 set-ups | About 73 s, 40 set-ups |
| **The Client's look** (outside review, Tomas 1A 2A 3A) | The red robe everywhere | `characters/uptimez-client-on3-v2-sheet.png`: a charcoal hooded tracksuit on the street, the red robe from the ring on, the gloves always; a hard face as his neutral in the dream; the garages' gear, never words |
| **Sofía's ring look** (Tomas, /grill-me) | To be developed | `characters/uptimez-sofia-on3-v1-sheet.png`: a short black satin leotard, bare arms, waves over one shoulder, one gold hoop, a feather, a ribbon at the neck, a beauty mark, seamed stockings, black patent heels. Her lips keep their red |

**v2, 19 Nov:** script v1 after the outside OK/FAIL review of 19 Nov and Tomas's idea of the folder as a contract. What changed:

| | v1 | v2 |
|---|---|---|
| **The folder** (Tomas) | He pays a hundred and gets the folder | The folder comes first, through the car window, in silence but for one line: it looks like a contract on a woman. He turns the page: it is her CV. He never receives money |
| **Why he fights** (review, P0) | He sees the plan after he has paid | He sees the plan over the ring (4.1, 4.2), asks "How much?", and pays for the fight |
| **The front** (review, P0–P1) | Street, car, alley, deal: 22 set-ups, the ring at 0:44 | The street, the car, the folder and Sofía are one scene; the alley is four set-ups with Don in one; the ring starts at about 0:34 |
| **The robot** (review) | First seen at 0:44 | Its piston arm is behind the glove in frame 0; it sits under the roll in 4.1, at about 0:25 |
| **The robe** (review, P0; my error) | Hung on the post in 6.1, against the rule | He boxes in it, hood down. The folder lies on his stool |
| **Glove gags** (review) | Eight | Four: the gesture at Mom, the cigarette, the payment, the plan. The pocket, the watch, the folder and the pointing are out |
| **The card** (review) | ROUND 2 | LAST ROUND |
| **The approval** (review) | Screen, "Approved.", jab | The screen is two rows filling the insert; after "Approved." it flips to a tick, then the jab: the cause is on screen |
| **Mom's place for the money** | The car window | A high chair and a cash box just inside the arena door. The car is for the folder only |
| **Length** | About 81 s, 46 set-ups | About 69 s, 38 set-ups. Nothing was cut to reach a number: this is what the merged scenes come to |

Not taken from the review: a fixed target of 65–70 s (the length is Tomas's call; it is decided on the animatic), and cutting Don's two set-ups at the ring (his walk under the roll is what points back at the plan).

## What the film is about

He handed over the plan of his ten garages and got a welcome pack with Sofía's CV in it. Then he paid $999 for Premium and his phone said 100% COMPLETE. The plan is still gone. That night he dreams he is a hard man in a hard city. He is handed a folder like a contract, and it is a CV. He pays for a fight to win his own plan back, and what he fights is the machine.

The dream runs in the order it happened to him: first the folder, then the bill, then the result.

## The protect list (gate G1)

1. **The first drawing is the last:** a glove landing on his face, close.
2. **Every hard line is answered by the picture:** a hit, a bill, or him asking.
3. **He never takes the red gloves off.** On the street he wears a charcoal hooded tracksuit and the gloves are the only red; from the ring on he wears the red robe. Eight things he cannot do, each costing more than the last: show a finger, open a folder, light his cigarette, hold his money, get out of his robe, read his watch, point, grip the roll. The last is the strongest.
4. **The folder looks like a contract and is a CV; then he pays for the fight.** His plan hangs over the ring all night, and he is the only one who looks up.
5. **"Human approval required." Mom: "Approved." The punch.** Awake, the punch is his phone: 100% COMPLETE.

## Rules of staging

- **Black and white with one red.** On the street (beats 02–04): his gloves. From the ring on (05–07): his gloves and his robe. And Sofía's lips. The change of clothes is the cut from 04 to 05 and is never shown.
- **His face in the dream is HARD:** low brows, narrow eyes, a pressed mouth. He shows almost nothing until a punch lands; the wide eyes are kept for those.
- **The tracksuit needs light behind it.** It is charcoal on a night street: a lit wall behind him in every street shot, down to his knees. Colour comes back only when he wakes.
- **Every shot names its light** (the last column). Shadows stand against a lit wall, never dark on dark.
- **The roll is in every ring shot,** above, in the lamp. Only he looks at it.
- **The fight has one rule:** it asks, everything stops, the tick, one punch, it asks again. Nobody touches its screen while the words are up.
- **The punch is framed the same three times:** 1.1 and 7.5 identical; 5.5 wider, so the loop is not given away.
- **The contract is only an image.** Nobody says what the folder is, and he holds no weapon. Money goes one way in this film: away from him.
- **Each character has a way of being filmed.** The Client: from a little below, the camera walking with him. Mom: through glass in the car; in her office, across her desk, the lit blinds behind her, and she never turns to them. Don: through his glass, with the thing he is missing in the same frame. Pam: square on, still. The robot: dead centre.
- **The Referee** is the Bartender of Noir 2: white shirt, bow tie, clean-shaven, slicked hair. He stands between the two, sees everything with his own eyes, and does nothing about it. He is the only one in the ring with bare hands.
- **Glove gags are never next to each other,** and the four small ones (folder, sleeves, watch, pointing) take a second inside a shot, never a shot of their own.
- **The robot never speaks.** Its screen is its face: furious, then the three words, then the tick. Mom approves without looking: a word to the money and one finger on a desk button, from her office.
- **Mom is never at the ring.** After the car she is only in her office. She sits in every shot. The hundred leads each shot of her: covered by her hand (4.4), held up and read (5.4, 6.2), still in her hand when she presses the button (7.4). The coupe stands at her elbow throughout.
- **Narration is typewriter cards at the top,** under the app's bar. Spoken lines are bubbles, with tails to a mouth that is on screen.
- **Series canon:** the series' proportions between characters, feet on the floor, walks with a planted foot.
- **Slapstick, not injury:** stars, a folded face, no blood.

## Beat 01 · The punch · about 0:00–0:04

| Shot | Size | What we see | Says | Thinks · eyeline | Light |
|---|---|---|---|---|---|
| 1.1 | Close, his face | Frame 0: his face, three-quarters, HARD, his eyes on a grey glove an inch from his cheek, large in the foreground. Behind the glove, a steel piston arm and, out of focus, a furious screen. The red collar of the robe at the bottom of the frame. It lands at 0.3 s: only now the face folds round the glove and the eyes go wide | N: "They say I know how business is done." | *Here it comes.* · at the glove | The ring lamp, straight above |
| 1.2 | The same | He drops out of the bottom of the frame. The lamp swings in the empty picture. A bell | | | The lamp, swinging |

## Beat 02 · The contract · about 0:04–0:17

| Shot | Size | What we see | Says | Thinks · eyeline | Light |
|---|---|---|---|---|---|
| 2.1 | Wide, low | Rain on wet stones, street lamps. He walks toward us: a charcoal hooded tracksuit, hood up, the red gloves swinging | N: "One fight." | | The lamps, pools on the stones |
| 2.2 | Wide | Headlights swing across the arena's wall; a long black car brakes at his knees, along the kerb. Its rear glass is black | MOM, from the dark: "Where are you going, skunk?" | Mom: *Oil. I can smell him from here.* | The headlights; the lamp |
| 2.4 | His view into the car | The rear glass comes down a hand's width. From the dark, her small ringed hand and a fur cuff hold out a folder. His two gloves come up from the foot of the frame and take it. The car pulls away | MOM: "Everything you need is in there." N: "A lot of money." | Client: *A job.* | The lamp, in the glass |
| 2.5 | Insert, from above | Under the lamp, his gloves get the folder open at the second try: one photograph, large, clipped over the top of the page. A woman in an evening gown. Nothing else to read | N: "One woman." | Client: *The job.* | The lamp, across the page |
| 2.6 | Two-shot | The woman herself comes the other way under the lamp: the gown, the wrap, the earrings, as in the photograph. Her eyes go down him and back up. He holds the folder to his chest and looks straight ahead | | Sofía: *Him.* · Client: *Her.* | The lamp between them |
| 2.7 | Insert | His glove pushes the photograph up on its clip. Under it: CV, four lines, and her number, circled, 555 0142 | | | The lamp |
| 2.8 | Close, the Client, 0.7 s | His face. Behind him, out of focus, she looks back over her shoulder once | | *She wants a job.* | The lamp, from behind |

## Beat 03 · The alley · about 0:17–0:25

| Shot | Size | What we see | Says | Thinks · eyeline | Light |
|---|---|---|---|---|---|
| 3.1 | Wide | The alley beside the arena: one long lit wall. On it, three huge shadows in hats and coats; a tommy gun, a bat and a knife swing round onto him together. He comes round the corner, a cigarette in his mouth, the folder under his arm. The men themselves are never seen | N: "I don't ask." | *Evening.* | The far end's light, along the wall |
| 3.2 | Close, the Client | He holds up both gloves. Between them, a crushed matchbox. He pushes his chin and the cigarette forward | N: "I'm the one who asks the questions." | *A light?* | The far wall, a rim on him |
| 3.2b | Insert, his gloves | Two red gloves and the crushed matchbox between them. Matches fall out, one after another. Above, his face: he does not look at the shadows | | *Come on.* | The gloves, the only red |
| 3.3 | Two-shot, him and the nearest shadow | The weapons' shadows go down. Out of the shadow comes one real hand, a white cuff, with a lighter. The flame, at his cigarette | | Shadows: *Is he serious?* | The flame, on his face |
| 3.4 | Wide, then closer | He walks on toward the arena's light; the cigarette falls from his mouth. Detective Don comes in behind him, bent over his glass, and takes it up with tweezers. On the wall behind Don every shadow has its hands up. He does not look round | | Don: *Evidence.* · Shadows: *Is that it?* | The lit wall; Don in front of it |

## Beat 04 · The price · about 0:25–0:34

| Shot | Size | What we see | Says | Thinks · eyeline | Light |
|---|---|---|---|---|---|
| 4.1 | Wide, from behind him | The arena's back door. He stops in it. Inside: one lamp over a ring; under the lamp, on two cords, his plan hung level, one end let down so the ten bays show; under the roll, the small robot on its wheel and outriggers, big grey gloves hanging, its screen furious. His head tips back | | | The ring lamp through the doorway |
| 4.2 | Close, the Client | His eyes on the roll. Down, to the folder under his arm. Up again, and one glove shoves the folder down out of the frame | | *That. Not this.* | The ring lamp on his face |
| 4.3 | Over his shoulder | Over his shoulder (M2). Her office, over the arena: blinds, the ring's light in stripes on the wall behind her, the button, a coupe of champagne and a deck of cards on the desk. She sits in a high-backed chair and does not look up. His hooded back is near; one red glove comes up with a banknote pinched against it | CLIENT: "How much?" MOM: "One hundred bucks. For the fight." | Client: *For my own plan.* · Mom: *They all pay.* | The desk lamp; the blinds, lit from the ring |
| 4.4 | Her view (M3) | He stands small in front of the desk, the door behind him, a banknote held between two red gloves. He lays it down; it crosses the desk. Her ringed hand comes in from the near edge and covers it. Her other hand takes the top card off the deck, lays it in the middle of the desk and turns it | N: "I name my price." | | The desk lamp |
| 4.4b | Insert, the card | The Tower, struck: its top going over, a bolt. Her fingers leave its edge. At the bottom of the frame her other hand is still on the hundred | | Mom: *They all fall.* | The desk lamp |
| 4.4c | Close, the Client | His eyes go down to the card: one long squint. Then up, the face he came in with | | *Cards.* | The desk lamp, from below |

## Beat 05 · Round one · about 0:34–0:46

| Shot | Size | What we see | Says | Thinks · eyeline | Light |
|---|---|---|---|---|---|
| 5.1a | Wide, the master (R1), 2.0 s | The ring under its lamp, smoke, hats and cuffs waving money. The roll above. He is in his corner in the robe, hood down, one glove half up toward the roll; Pam beside him. The robot waits at centre, and a step behind it the Referee: a white shirt with the sleeves rolled, a black waistcoat, a bow tie, slicked hair, bare hands. His corner: a stool with the folder on it, a bucket by the post. Across the front of the frame Sofía walks the card: ROUND 1. Her eyes are on him | | Sofía: *Look at me.* · Client: *Up there.* | The lamp cone; the smoke shows it |
| 5.1b | His view, from below (R7), 1.0 s | The plan, big: the lamp behind it, the two cords, the ten bays, the L-shaped one solid, and its title block: 10 GARAGES. One red glove comes up into the frame toward it and stops short | | Client: *Mine.* | The lamp, straight above |
| 5.1c | Medium, his corner (R3), 2.0 s | Pam, in her flat cap and work apron, a towel round her neck, a stopwatch on a cord, pulls the robe back off his shoulders and down to the belt; he stands bare-chested, and one sleeve stretches from his glove to her two hands and stops dead. She pulls once more, gives up, and pulls it back on. He has not looked down once | | Pam: *It won't come off.* · Client: *Up there.* | The lamp, from the side |
| 5.2 | Two-shot (R2) | The Referee, behind the robot, drops his raised arm. The bell. He winds up and swings, everything he has. His glove stops a clear hand short of it. The robot does not move; its gloves hang. At the edge of the frame Pam's thumb clicks the stopwatch | | *Now.* · Pam: *Time.* | The lamp |
| 5.2a | Four cuts, a quarter of a second each | The bell. From the front; his view of it; its view of him, in a frame of brackets; from above | | | The lamp |
| 5.3 | The robot's view | Through its screen: his face, hard, and his red glove stopped a hand from the lens, shaking. Three rows come up over him: HUMAN / APPROVAL / REQUIRED | | | The screen's own glow |
| 5.4 | Close, Mom, in her office | Seated, as in 4.3. She holds his hundred up beside her eyes and reads it. Her eyes go to it; her mouth opens a crack; her face is still again. One ringed finger comes down on a button on the desk. Behind her the blinds, and the ring she has not looked at | MOM: "Approved." | *One. Still one.* | The desk lamp; the blinds |
| 5.5 | Insert, 0.4 s; his view; then wide | The screen flips to a tick. Through his eyes: the grey glove comes straight at the lens and fills it. Black. Wide: he goes over backwards | | | The screen, then the lamp |
| 5.6 | From above | He lies flat on the canvas, arms out, the shadow of the roll across his chest. Over him the Referee's bare hand counts: one finger, two, three. At the edge of the ring Pam holds the stopwatch up, face to him | N: "I don't break. I break even." | Client: *How long have I got.* · Referee: *Four.* | The lamp, straight down |

## Beat 06 · The corner · about 0:46–0:56

| Shot | Size | What we see | Says | Thinks · eyeline | Light |
|---|---|---|---|---|---|
| 6.1 | Medium, square on | He is on the stool. Pam squeezes the sponge over his head, once. Then she tapes his brow and presses it down with her thumb | PAM: "Some punch. Others patch." | Pam: *Hold still.* | The lamp, from the side |
| 6.2 | One frame, split in two | Left: the robot in its corner, the proud face on its screen; an oil can tips over its elbow. Right: in her office, seated, Mom holds his hundred up beside her eyes and counts it again | N: "They beat me. They cheated me." | | The screen; the desk lamp |
| 6.3 | Over the Client's shoulder, then through the glass | Beside him, Don's tweezers lift the folder off the stool. In his glass, huge: Sofía's photograph | N: "They robbed me." | Don: *The woman.* | The lamp; the glass catches it |
| 6.4 | Medium, with one close, 0.5 s | The stamp comes down on the folder: CASE CLOSED. Don walks out under the roll; his hat sets it swinging; he does not look up. The Client points after him with a glove: a fist. Close: the Referee has seen all of it. One eyebrow goes up. He looks away. Pam turns the Client's head back to the front | | Client: *Up! Look up!* · Referee: *Not my ring.* · Pam: *Last round.* | The lamp |

## Beat 07 · The last round · about 0:56–1:05

| Shot | Size | What we see | Says | Thinks · eyeline | Light |
|---|---|---|---|---|---|
| 7.1 | Medium | The card goes past, fast: LAST ROUND. He stands up off the stool, tape on his brow | N: "But I didn't quit." | | The lamp |
| 7.2 | Three quick closes | His glove lands: a dent in the robot. Again: its screen cracks. It rocks back onto one outrigger | | *There.* | The lamp; the screen flickers |
| 7.2b | Three-shot | The Referee steps between them, a bare palm on the Client's chest. The Client stops at once, steps back, and lets his gloves hang. The robot rights itself | REFEREE: "Break!" | Client: *Yes, sir.* · Referee: *Rules.* | The lamp |
| 7.3 | Low, looking up | Pushed back under the roll, he looks up and reaches. He claps the plan's hung end between both gloves and has it for a moment; the paper slides up and out from between the leather and swings away on its cords. The gloves close on each other; they cannot grip | | *Mine.* | The lamp behind the roll |
| 7.4 | Insert, then her desk, then insert | The cracked screen: HUMAN APPROVAL / REQUIRED. Her office: she does not look up from the hundred; her arm comes down on the button. The screen: a tick | MOM: "Approved." | Mom: *His card.* | The screen; the desk lamp |
| 7.5 | Close, the framing of 1.1 | His face, HARD again, the grey glove an inch away, the piston arm behind it. It lands. White | | | The lamp, straight above |

## Beat 08 · Awake · about 1:05–1:13

| Shot | Size | What we see | Says | Thinks · eyeline | Light |
|---|---|---|---|---|---|
| 8.1 | The framing of 7.5, in colour | His face on a sofa cushion, and his phone lying on his cheek where the glove was. The screen: UptimeZ Find · PREMIUM · 100% COMPLETE, green. He opens one eye | (the cheerful chime of episode 10) | *Ow.* | The phone's green |
| 8.2 | Wide | The office of one of his garages, at night. He is on a low sofa in a red dressing gown. By his head, a side table: the phone has buzzed itself off its edge. On the table, his watch and the UptimeZ welcome pack, a CV sticking out. On the wall, a bare hook and a pale rectangle where a plan was pinned, four torn corners still under their pins; on the floor, the plan's tube, its cap off. Through the window, a car up on a lift | | | A desk lamp; the workshop light through the window |
| 8.3 | Insert, the phone, then the table | The phone rings in his hand: a number, 555 0142. The screen: INCOMING CALL, 555 0142. On the CV beside it: 555 0142, circled | (the ring) | | The phone |
| 8.4 | Medium | He looks at the phone, at the CV, at the empty tube. He puts the phone face down on the CV and pulls the gown over his head | | *Not tonight.* | The desk lamp |
| 8.5 | Push in | Into the red fold of the gown; the red goes dark; out of the dark, his face and the grey glove an inch from his cheek | (the bell, over the seam) | | The dark, then the ring lamp |
| Loop | | The last drawing of 8.5 is the first of 1.1, pixel for pixel | | | |

## Count

| | |
|---|---|
| Lines | 14: narration 7, Mom 4, the Client 1, Pam 1, the Referee 1. The robot's screen twice. Sofía, Don and the shadows have none. About 29 s of voice |
| Set-ups | 42 (v1: 46, v2: 38, v11: 40, v12: 41) |
| Length | About 73 s (v1: about 81 s, v2: about 69 s) |
| Things to read | 7: ROUND 1, LAST ROUND, the CV with 555 0142, HUMAN APPROVAL REQUIRED, CASE CLOSED, 100% COMPLETE, the ringing 555 0142 |
| Sets | 6: the street (from Noir 2), the alley, the arena door, her office (on Office Noir's office), the ring, his garage office |
| Holds to protect | The raised glove (2.3); the turned page (2.7); the hats looking at each other (3.3); his eyes on the roll (4.2); the counting fingers (5.6); his step back after "Break!" (7.2b) |
| Back in if there is room | Her look back as its own shot (v1 2.5); Don's cigarette end through the glass (v1 4.6) |
| First cuts if a cold viewer names a repeat | The second try at the folder (2.5), then the watch (5.6): the two cheapest glove gags |

## What it must not break

- **Nothing is said awake.** He is alone. He does not learn where the plan is.
- **Sofía's call is not answered,** and nobody says "CV". It stays for episode 12.
- **Episode 11 is untouched:** he arrives furious, as written. This is the night before.
- **The robot is technically true:** it never hits without approval.
- **He never receives money,** and nobody names the folder as a contract.
- **No gun is fired.** The punches and the bell are the only bangs.
- **Mom does not shout.** She is quiet and in charge.
- **Mom is never at the ring** and never looks at it. Her word reaches it through the button.
- **No cards.** (v19: the tarot cards are out of the film.)
- **The Client is cheated, not stupid.** He is the only one who sees the roll.
- **The red is his gloves, his robe (from the ring on) and her lips,** nothing else, until the cut to colour. Her heels are black patent.
- **The Referee is not the Client.** Noir 2's viewers took the Bartender for the man in OUR FIRST CLIENT. He stays clean-shaven and slick-haired, in white, and is checked beside the Client on the cast sheet.
- **The Referee says one word,** and takes no side.
- **No real person, brand or logo.**

## What the storyboard has to prove on mute

Two cold viewers, frames only. The review's four questions are 1, 4, 6 and 9.

1. What does the man in red want? Where is it?
2. What did you think the folder was when it came out of the car? And after he turned the page?
3. What do the armed men end up doing for him, and why couldn't he do it himself?
4. Why does he pay? What is he paying for?
5. Why doesn't the robot hit him straight away? Who lets it, where is she, and is she watching?
6. What does the man with the magnifying glass take, and what does he miss?
7. What does the woman in his corner do for him? And the man in the bow tie: what does he see, and what does he do about it?
7b. In the last round the boxer is winning. Why does he stop?
7c. Why does he box in his robe?
8. What hits him at the end, in the dream and awake?
9. The phone says 100% COMPLETE. Is it? What is still missing?
10. Who is ringing him, and how do you know? What does he do?
11. What is the last image, and does it lead back to the first?

**Pass:** both tell back at least 4 of the 5 beats (the contract; the alley; the price; the ring; awake), and both answer 1, 4, 5 and 7b.

**Also asked:** "Did anything repeat too often?" If either names the gloves, the two cheapest gags go first (see Count).

**If question 2 fails:** if either viewer still thinks at the end that he was hired to kill her, the contract goes: the CV becomes the first page and the photograph the second.

## Voices

- **The Client:** voice B from *The Onboarding*, lower and slower for the narration; his one spoken line in his own voice.
- **Mom:** voice F, quiet and dry, not shouting. Two or three takes of "Approved." to choose from.
- **The Referee:** the nice macho's voice from *The Best Candidate*, one word, flat and official.
- **Pam:** the British voice of *The Onboarding*, through the mix chain.
- **Sound:** rain; the bell; the piston jab; the chime of episode 10 for 100% COMPLETE; a phone's ring.

## Next

1. Your notes on this script.
2. **Sofía's ring look,** two or three options on a sheet, on its own.
3. The cast is drawn: Sofía (v2), the Client (v2), Mom (v2), the robot (v2), Pam and the Referee (v6); Don is unchanged from Noir 2. Next is the sets with their light, then the board.
4. Set sheets with the light drawn in, then the board and the cold mute test.
