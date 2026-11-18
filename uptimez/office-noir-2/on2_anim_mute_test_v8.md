# Office Noir 2 — cold mute test of the animation (v8)

18 Nov · motion test v8 (85.7 s, 42 set-ups, script v3) · two new viewers (E and F) · gate G4

## How it was run

- **What they saw.** 343 frames of the film at 4 a second, with no narration line, no bubbles and no sound, on 17 sheets of 21 tiles, each tile 270 px wide with its number and time. Four strips showed quick moments drawing by drawing: the coin, the stamp, the dive under the desk, the pop. `src/on2_mute_anim.py` makes the sheets.
- **Round 1, cold.** The skill's prompt, unchanged: tell it beat by beat, then the six questions. This round gives the score.
- **Round 2, asked.** Ten questions about particular frames, sent to the same two viewers afterwards. They could look again. This round shows whether something is in the picture when you look for it; it does not count toward the score.
- **Not perfectly blind.** Both viewers reported a list of your projects and some character names in their context and said they did not use it. Viewer E had seen the names Pam and Don before reaching the badges; both names are printed on badges in the frames.

## The intended reading, written before the test

The same five beats as the storyboard tests. Beat 1 has the new mirror: she smiles at herself, then sees the hat.

1. **The street.** A glamorous woman in red gets out of a taxi at night. A man in a hat follows. She smiles at herself in her compact, sees his hat in it and stops smiling. His hand goes for the thing she carries; she drops the compact and runs, losing her wrap.
2. **The trail, and the coin.** She leaves white footprints. A sweeper sees a detective coming and sweeps them away; he loses the trail and goes the wrong way. At a door a robot hands her coin back: it needs approval.
3. **The bar.** Men push money at her; she hides from the detective behind it. A man's hand sends her a drawing of a building and a question mark. She answers with a phone number in lipstick; nobody takes it. The detective finds the number, sees her, and closes the case.
4. **The office.** She finds the same drawing rolled in a drawer and uses it to bait the man in the hat. Someone comes; she hides under the desk. Two shadows on the wall: a small one raises its arm, a bang, his hat flies off.
5. **Awake.** It was a dream. The same picture in colour is a party: an older woman has popped champagne and a paper hat lands on the man. She wakes at a table with sugar on her cheek and a party blower in her hands. A man in a paper crown gives a thumbs-up, a woman sweeps confetti, she shuts her eyes; the lamp in the window.

Pass: both viewers tell back at least 4 of the 5.

## Result: pass, five of five for both

The storyboard passed at the threshold (four of five each). The animation is read whole by both viewers, cold.

| Beat | Viewer E | Viewer F | Board v4 | Animation v8 |
|---|---|---|---|---|
| 1 The street | Read: "She checks herself in a compact mirror, smiling. A fedora silhouette appears in the mirror and her smile drops" | Read: the same, and "a grey hand with a white cuff reaches toward the roll" | Read by both | **Read by both** |
| 2 The trail, and the coin | Read: "The sweeper brushes the footprints into her dustpan… He walks off behind her, the opposite way". The coin: "hands the coin back with a tag reading PENDING APPROVAL" | Read. The coin: "a tip or bribe being bounced by bureaucracy" | C half, D read | **Read by both** |
| 3 The bar | Read: "She hides her face behind the banknotes until he passes". The card: "a drawing of a building and a big question mark". The eye and CASE CLOSED read | Read: the same. "The lipstick card is in his breast pocket" | C read, D half | **Read by both** |
| 4 The office | Read, less the beckon, which was first taken for "counting on her fingers" | Read: "She gives a sly smile and beckons him with one finger" | Read by both | **Read by both** |
| 5 Awake | Read: "The 'shot' was a champagne cork… A striped party hat drops onto his head". The crown man's hand first read as "one finger raised" | Read, with the thumbs-up | Read by both | **Read by both** |

Both chose the same frame to screenshot: 189, the detective's giant eye in the glass behind her as her face falls. Both gave the hat in the air and the cut to colour as the runner-up.

## What the changes since the storyboard did

| Still misread by both in board v4 | In the animation |
|---|---|
| A hand is coming for the card | **Fixed.** Asked, both were sure nobody takes it. One read the stool as "whoever she pushed the card toward is not there" |
| The drawing: drawers, a ledger, a floor plan | **Fixed.** Both: "a drawing of a building" |
| Mom's bottle: "a bottle or a party popper" | **Fixed.** Both: a champagne bottle, the cork gone |
| The short shadow could be the sweeper | **Fixed.** Both: a new person, "lumpy hair and a handbag" |
| The roll is pale on the street and dark in the office | **Not fixed.** See 1 below |

Also new in the animation: both saw two pursuers and told them apart; both tied the detective to the man in the crown and the sweeper to the woman with the broom at the party; both read the pop as a gunshot until the cut; both recognised the last window as the first street.

## What both still misread or could not tell

These are staging faults by the test's rule: the same reading from both viewers.

| # | Frames | What both said | Likely cause | Proposed fix (for the shot list) |
|---|---|---|---|---|
| 1 | 9-14, 214-229 | The thing she carries on the street is "a rolled paper". Cold, F took the office roll for the same one ("her paper") and E could not tell "whether she brought it, found it or is stealing it". Neither said "drawer" | Her clutch is a tube with bands, the shape of the roll. In 6.2 the drawer fills the frame, so it reads as a desk top | Open 6.2 a little wider: her glove pulls a drawer out of a desk, then the roll. And either give the clutch a clasp and a chain, or accept the echo |
| 2 | 206-213 | The portrait OUR FIRST CLIENT is "the bartender" | Two big bearded dark-haired men. The portrait is small | Change the bartender, not the Client: no beard, slicked hair. Or hold the portrait larger for half a second |
| 3 | 51-60, 68 | A dark-sleeved hand picks up the wrap and drops it; then the detective has it. "One pursuer or two?" | The Shadow touches the detective's clue | The Shadow's hand does not pick it up. The wrap falls and lies there; the detective arrives holding it |
| 4 | 177-183 | The dark round thing beyond the bar: "a stool seat, an ashtray or the top of a hat" | The stool is a disc seen from above | Give it a back and legs, or take it out: the card alone reads |
| 5 | 316-323 | The raised hand: "a thumbs-up; a raised index finger is possible" (E's cold reading was a finger) | The thumb is a long thin upright | A shorter, fatter thumb leaning back from a fist seen side-on |
| 6 | 96-101 | The low-battery sign on the robot: "I do not know what it is for" | The sign that makes it a beggar is not read | Minor: a hand-written "PLEASE CHARGE" card would say it, or leave it; the coin gag reads without it |
| 7 | 115-122 | "I do not know who is handing her money or why" (both guessed admirers) | Hands without owners | Leave it: both used the money correctly as her hiding place |
| 8 | 302-307 | She "pops up from behind a table". Both inferred a dream or a doze; E: "the film never says so outright" | She is asleep for one drawing | Hold her asleep, head on the table, for half a second before she jerks upright |

## Read by one viewer only

- **The beckon (238-242).** E's cold reading was counting; on a second look, "beckoning, not counting". F read it at once. After the cut it is one beckon, eight drawings.
- **The detective's direction (90-95).** E read "the opposite way from where the woman ran" cold. F first had him leaving "the way she came", and on a second look "wanders off the wrong way". Neither saw the sweeper send him; nothing shows why he chooses that way.
- **The powder (43-46).** First taken for "pearls or raindrops" (E) and "smoke or an explosion" (F); both worked it out from the footprints.

## What does not read without sound

- **What she is afraid of.** Asked for one sentence, both said: being followed and caught, by the man in the hat, then the detective, then whoever is at the door. Neither said she is afraid of being found out for giving her number. Both did guess why the case is closed: "he thinks he has got her number".
- **Who she fears at the door.** Both noticed the man in the hat standing calmly while she hides. That is as intended: the surprise is the small shadow.

## What read without help

The smile dropping in the mirror. The sweeper erasing the trail under his lens. The coin coming back with PENDING APPROVAL. Hiding behind the banknotes. The building on the card and the same building on the plan. The lipstick number ending up in his pocket. The giant eye. The pop as a gunshot, then a cork, with the fedora becoming a paper hat. The party blower in the place of the roll (asked, both linked it to the roll under the desk). The last window as the first street: "she chooses to drift back into the fantasy".

## What this test cannot tell

Whether it is funny, whether the narration and the lines land, anything about timing or the mix, and how it plays as movement: the viewers saw stills at four a second, and they are models, not people. Those need people with the sound on.
