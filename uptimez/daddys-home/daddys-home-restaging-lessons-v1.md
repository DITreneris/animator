# Daddy's Home: lessons for the restaging, v1

24 Nov. Collected before any drawing, as the series rule asks. Each lesson says where it was learned and what it means for Daddy's Home v8. Sources: `docs/lessons.md` (line numbers as of main 1222d77), One Star v19 (`src/cs_v19.py`, `customer-success/one-star-shot-list-v19.md`), and the v7 audit (`gates_dh.py`, 24 Nov).

## What the v7 audit says (the problem)

- 102 shots in 96.7 s; mean shot 0.95 s, 21 shots of 0.4 s or less.
- Sizes: 60 MS, 23 WS, 4 MCU, 15 inserts, **no close-up**. Median head top at y 278: the frames are built around bubble room, so the bottom half is floor.
- 76 of 87 people shots show whole figures; 20 lone small figures (the robot and Pam most of all).
- Foreground in 24 % of shots.
- Causes: (1) frames built for the bubble, not the actor; (2) one reaction per shot, so a cut per line; (3) one flat set seen from one height.

## Lessons that apply

### Shot list and cutting

1. **Shot list before key poses** (lessons 511). Each beat: an action shot and a reaction shot, with size, eyeline and foreground written down. v8 does this per scene, as a doc, before drawing.
2. **Three motivated camera changes beat uniform framing** (491): a close-up for the emotion, an insert for the key object, a low angle for power. More cuts are not more story.
3. **Hold a shot across two lines when both people are in it** (v7 audit; One Star 4.2b held 18 drawings). Merge an exchange into one over-the-shoulder instead of cutting per line. Target: about 60–65 shots for the film.
4. **Adding reactions costs time; don't pay for it with the setup** (518). The line schedule stays: no line moves, so the mix and lip-sync stay valid.
5. **Retime with the old clock** (594). If a shot is merged, the drawings inside it keep the old film time, so blinks and mouths stay on their lines.

### Composition in 9:16

6. **Compose every shot for 9:16; never crop one wide set** (519). Faces in the band under the title bar; heads big in close-ups; a foreground layer.
7. **Two-shots are width-limited** (267): cropping ceiling and floor doesn't enlarge faces. Bring the pair closer, or let one be cut by the frame edge (over the shoulder).
8. **Fake an over-the-shoulder with a foreground silhouette** (497). One Star does it with `sb._client_back` and the `cs_v19` foreground pieces; the same approach is reused here, not rewritten.
9. **Stage tight two-shots with a gap between bodies** (310): no merged arms.
10. **Sizes are measured, not named**: CU ≥ 120 face radius at 540 wide, MCU ≥ 95, MS ≥ 64 (`gates_dh.BANDS`, same as One Star). A shot called CLOSE in v7 at r 64–84 is an MS.
11. **Frame for the payoff, then add the push** (296). A push must not cut a face or a sign at its end.
12. **Signs whole or out, through a move as well as at its ends** (series rule). The CUSTOMER SATISFACTION screen and the $49,999 tag are signs.

### Bubbles (the cause of the empty floor)

13. **A side bubble needs wall, so frame for the bubble** (358) was right for v7 and is what pushed the actors down. v8 keeps bubbles at the top (series rule) and puts them **over clear wall above the heads** (253), so the actor can be big. A bubble never covers a face, a sign or a hand that acts.
14. **Bubbles ≥ 44/46** in the tail check stays the floor. Run `dh_tailcheck` on every new shot.

### Acting

15. **Reactions face their target, not the camera** (620). Pam looks at the screen, Don at Pam, Mom at the chair arm.
16. **The shout needs its object in the same frame** (466). "Make it green." has the screen in frame; "It's still one." has the star or its glow in frame.
17. **A plant must be readable the first time** (216): the one red star at 270 px wide.
18. **Hands are the series hand** (`kit.HAND`, `hands_ps`: point, fist, palm, grab, quiet). Don's disc hands go. Held objects use `grip_rect` (One Star scene 1).
19. **A lip-sync mouth scales with the figure** (554). Every new close-up checks the mouth at its new size.
20. **Show the consequence, not the comment** (512): Sofía's leap and the rolling throne carry the joke, not Mom's line.

### Regression

21. **v7 is not touched.** New code goes in new files behind flags (`dh_film_v8.py` and on). `python3 dh_baseline.py check` must say "same" for scenes 1–8 before every send.
22. **Run checks one at a time** (222): parallel renders broke the baseline once already.
23. **Gates before and after**: `gates_dh.py` on v7 and on the new scene; the new numbers go in the shot list.
24. **Cold mute test** on v7 and on v8 (two fresh viewers each), so we know whether the restaging reads better and not only measures better.
25. **At most two rounds per scene**; stop and report after 1 hour or 2 runs without convergence.

## Learned on the pilot (scene 3, 24 Nov)

26. **Measure the vowel, not only the words.** Whisper heard "green" in takes Tomas heard as "grun"; the vowel's F2 (about 2000 Hz for "ee", 1200 for "groan") showed it. Don's voice says a phrase-final "green" as "groan" in every spelling; a phrase-initial one is clean, so cut it from there.
27. **No effect on a line's first word** (lesson 443 again): the fist's whoosh 0.05 s before "Green" made it "Brain".
28. **Stage for the read first, then fit the bubbles.** Moving the throne and Sofía to make room for Mom's bubbles made two beats misread (a handshake, climbing in). When a bubble has no room, move the camera (v7's SHIFT) before moving the people.
29. **Bubble sides are set by the rigs:** Mom's mouth sits right of her face's middle, so her tail reaches only from her right; Pam's bob blocks tails above r 64; Don's curl is his crown top (frame him so a side box has wall).
30. **A back rig is one silhouette:** its raised arm must be drawn apart, or the tail finds the fingertip as the "top".
31. **The tail check tests dh_speech's placement**; render with the placement it tests.
