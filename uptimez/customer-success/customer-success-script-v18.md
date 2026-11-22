# One Star — script v18 (line by line, with the shot list)

**Title (20 Nov, Tomas): "One Star"**, after the post at 0:01 and the last line, "Still one star." The working title "Customer Success" survives as Don's line at the handshake; the folder and file names keep it (`customer-success/`, `cs_*`) so nothing built breaks.

UptimeZ Inc. · episode 11 · 20 Nov · for review · scripts v1–v17 are kept

**v18, 21 Nov: one wall calendar in the series** (Tomas, /grill-me, after comparing with First Search film v30 on main):

| Change | In the film |
|---|---|
| **First Search's calendar, as it is** | The same drawing (`fs_film30.calendar`, called from `cs_cal.wall`), the same place: right of the portrait (was my own redraw, by the door, NOV · FRI · 20) |
| **THU 11, then FRI 12** | First Search ends on MON 8. One Star's post and call are Thursday the 11th; **3.2a (new, 0.8 s)**: the page tears off and falls, FRI 12; then he walks in at 9:00. The last wide (6.6) shows FRI 12, the first (1.1) THU 11: the loop's cut also turns the day back |
| 2.1 | Still opens on the calendar (now just up and right of Don), a shorter pan |
| main merged | The branch was already in main; main's newer set code is in (the wall logo is gone, as in First Search) |

**v17, 21 Nov: after the whole film's cold test** (`cs_cold_test_film_v1.md`; Tomas):

| Change | In the film |
|---|---|
| **5.4b is cut** (Pam straightens Don's mic) | Three cold rounds read the gesture but not its aim (lesson 52). 5.3 cuts straight to Don's "Customer success."; in 3.5b the boom only shakes and settles (no set-up left hanging) |
| **6.6a, new** | Don alone, big: he reads his phone, grins, swells, a thumb in his vest. In the wide nobody saw him react |
| **Trims** | 1.2 a second shorter (his read of the post 12% faster, `film_v5`); 3.1 and 4.2 a third of a second each. The film: 61.1 s |
| **Sound** | Episode 9's sparse vibes (bed A), cut by the buzz / on "Is this a joke?" / for "Still one star.", back on "Approved." / as the 7 goes in / for the loop. 99 effects, a faint room tone, the voices in the room (short reverb) |
| Small | "dialing…" on Don's phone; the note "finds things" bigger, in Pam's purple; FOUND BY: larger |

**v16, 20 Nov: the post and the reply read aloud** (Tomas: "Garage message should be said in the Client's voice. Robot answers Shut off!"):

| Change | In the script |
|---|---|
| **1.2: the Client reads his post** | CLIENT (voice-over, his post): "Paid $999. They lost my blueprint. My lawyer will call." It starts under 1.1 (0.5 s), as the heads turn; the phone pushes in on the red line as he says it. Read "nine hundred ninety-nine" ("nine ninety-nine" was heard as 9.99) |
| **1.4b: the robot reads its reply as it posts** | ROBOT: "Shut off! Our AI does not lose files!", flat and polite, as the reply lands under the post |
| Takes | `cs_voices/film_v4` = film_v3 unchanged + 1.2 (5.4 s) and 1.4b (2.2 s), Whisper 3/3 in the mix. Lines: 14. Scene 1 runs 13.1 s (was 9.0) |

**v15, 20 Nov: the reply swears, in a robot's words** (Tomas: "F*ck off! Our AI is not losing files!", then "Robotic: Shut off"; the AI matches the Client's tone):

| Change | In the script |
|---|---|
| **The reply: "Shut off! Our AI does not lose files!"** | Three lines: "Shut off!" big, the claim under it. The robot mirrored his angry post's tone, in its own vocabulary (it shuts things off; it never says "up"). Don approves it unread. Platform-safe; the censored swear version ("F\*ck off!") is kept as `cs_props.REPLY_V15_SWEAR` if we ever want it |

**v14, 20 Nov: the company's reply fights back** (Tomas, watching scene 1 animated: "Correct. We will recover." doesn't work; UptimeZ must run into a fight. /grill-me):

| Change | In the script |
|---|---|
| **The reply: "Our AI does not lose files."** (was "Correct. We will recover.") | Don approves it unread (1.4). It denies the accusation, which escalates the crisis and is why Don has to call (2.1). At the end (6.2) it sits right above "UPDATE: Pam found it.": the AI never lost it, and a human found it. Changed everywhere: 1.4b, 6.2, the props (`cs_props.REPLY_TXT`, opt-in) and episode 12's thread (the denial is on record when he decides whether to sue) |

**v13, 20 Nov: from the motion test** (`cs_motion_test_v1.md`, `src/cs_anim.py`; Tomas chose):

| Change | In the script |
|---|---|
| **The handshake is cut** | It failed four of four cold viewers in two animated versions ("an arm reaching", "pushing a phone at him"). After the contact is saved (5.3), cut straight to Don's close |
| **The order: the mic, then the line** | 5.4b Pam straightens Don's crooked mic, he never looks; 5.4c he says "Customer success." into the mic she fixed. She sets him up to take the credit. Passed in motion at feed size: "she quietly fixes it without fuss ... he doesn't notice" |
| **The set-up: the boom goes loose at 3.5b** | Don's flash of panic jerks his head; the boom swings loose and hangs crooked in every Don shot until Pam fixes it |
| Don talks with his eyes shut | His "grin" face popped his eyes ("surprised"); his mouth opens on the happy face instead |

**v12, 20 Nov: from five cold viewers of board v5** (`cs_board_mute_test_v5.md`; Tomas chose, /grill-me). Storyboard v6, animatic v2 (50.3 s with the takes).

| Tomas picked | In the script |
|---|---|
| Pam points at his pocket | **4.2b (new):** at the hole, Pam looks up and points at the blue strip sticking out of his jacket pocket; he looks down. 4.3a: his hand at the pocket, the strip coming out; he freezes. She notices; he had it; he lays it in himself |
| Don's mic in two frames | **5.4b:** the boom hangs crooked, her fingers on it. **5.4c (new):** straight, her hand leaving. Don smiles past her throughout |
| FOUND BY: HUMAN, an arrow at Pam | 4.4: the robot's sign |
| Her phone turned to us | 6.5: Sofía holds the phone up to camera: ★☆☆☆☆ under "Pam found it." |

Also: Pam's roll is held on her far side in 4.1; the robot's blue sheet is big in 3.1; the hands meet in 5.4a.

**v11, 20 Nov: tighter, one ending** (the storyboard v3 review and the v2 cold test; Tomas chose the two cuts). Storyboard v5, props v4. About 43 s, 30 shots, 12 lines.

| Change | In the script |
|---|---|
| Don's three faces | **Smug** when he approves the reply unread (1.4); **a flash of panic** at "Is this a joke?" (3.5b, new, 0.6 s); **proud** the moment Pam has fixed it (5.4a). Before, he grinned all through |
| The pocket, held | 4.3a his freeze, then **4.3c (new)**: close on the strip in his own oily hand, its 7 ringed in red; then he lays it in. Every outside viewer so far gave the 7 to Pam |
| The call, shorter | 2.1a 0.5 s, 2.1 1.5 s, 2.2 1.5 s (was 4.6 s in all) |
| Cut (Tomas): Sofía's "He's not looking at you." | Her thread stays silent: the lapel, walked past twice. She has one line, the last |
| Cut (Tomas): Mom's nod to Pam | Nobody who hadn't seen ep 10 knew who she was. Mom stays at her desk in the wides; her matchmaking waits for an episode that sets it up |
| One ending | Pam's line, then "Still one star.", then the wide (every phone buzzing = frame 0). Nothing after the sting |

**v10, 20 Nov: the insult, the pocket, the one star** (Tomas, after two outside reviews and the v2 cold test, /grill-me):

| Tomas picked | In the script |
|---|---|
| The AI's plan is a phallic layout (no car wash) | The robot's **SITE PLAN · RECOVERED BY AI · 99% CONFIDENT**: twelve garages round a driveway whose outline, taken whole, reads as a phallus (two round courts at the foot, a long drive, a turning circle). Deniable: no anatomy, only the silhouette. Props v3 |
| "Is this a joke?" and he turns to go | The drama peak: he tilts his head, gets it, goes red: "Is this a joke?" He turns for the door; **Pam steps into his way with her roll**. Replaces "I have ten garages." |
| Sofía: "Still one star." | Her last line looks at the rating Don doesn't: the UPDATE names Pam, and the stars haven't moved. Replaces "Nobody noticed." (her dressed-for-him thread stays silent: the lapel, the earring, walked past twice) |
| He pulls it out and freezes | 4.3: his hand comes out of his own pocket with the 7; **he freezes; his face, embarrassed, held 0.5 s**; then he lays it in himself |

**From the v2 cold test and the reviews (staging, no new story):** 1.3 folded into 1.1 (the heads turn in the wide); the call opens on its insert (**10 GARAGES · calling…**); the robot's paddle reads **HUMAN ✓** and points at Pam, after a beat of defeat; Pam's hand on Don's mic gets its own close two-shot (Sofía's line moves to her own shot); Mom over her shoulder onto Pam's lit phone; no confetti on the floor; **the film ends on the wide with every phone buzzing (= frame 0)**, Sofía's line just before it. Props v3: the reply dominates its insert; the post and the UPDATE share one layout (only the strike-through and the UPDATE change, the one star stays put); the contact is a contact card (Pam · 555 0142 · SAVED); Pam's line with the rest dimmed.

**Platform note:** the site plan is a silhouette gag. TikTok, Reels and Shorts can limit reach for sexually suggestive content even in cartoons; keep it deniable (no anatomy, one beat, the Client's reaction carries it) and check the cut against each platform before posting.

**v9, 20 Nov: Pam's episode** (Tomas: "Duodam Pam, čia jos serija; tobulinam ją, kad žiūrovas pamiltų", /grill-me). The looks stay; Pam gets a sign, a kindness, a reaction and one written line:

| Tomas picked | In the script |
|---|---|
| Glasses up, sleeves up | When she starts on the plan (4.1) she pushes her reading glasses up into her hair and shoves her sleeves up; **they stay up to the end** (ep 10 had her tug the sleeves down at the loop). Pam at work, all episode |
| She fixes Don's mic | 5.4: as Don steps in for the handshake and the credit, **she reaches over and straightens his crooked headset mic**. He doesn't notice. She still loves him |
| Face down, then a peek | 6.3: when her name lights up in his UPDATE she turns the phone face down at once; then lifts one corner, peeks, and **almost smiles** |
| One written line | 6.3b: under his UPDATE, a reply from Pam: **"Some post. Others find."** (her pattern: "Some shit, others scoop.", "Some post. Others tape.", "Some dream. Others sweep."). Read, not spoken |

**v8, 20 Nov: the post is the crisis, not the payoff** (Tomas: "Firstly client needed to post, lost my blueprint, plan to sue. Communication crisis. Later phone call, meeting, he corrects his post: Pam found. Firstly AI tried to recover unsuccessfully, later Human AKA Pam did it." /grill-me):

| Tomas picked | In the script |
|---|---|
| The post lands at 0:01 | Every phone in the office buzzes at once; on every screen his post: **"Paid $999. They lost my blueprint. My lawyer will call."** Everyone looks at Don |
| The AI generates a fake plan | Asked to recover the blueprint, the robot **generates** one: glossy, confident, **twelve garages, number 7 a car wash**. Don approves it unseen. The Client counts and knows at once |
| Don calls; the Client comes in | Don, all charm on the phone: "Let's fix this together." The Client: "Nine o'clock. Your office." |
| An UPDATE line under the post | At the end the old line is struck through and under it: **"UPDATE: Pam found it."** Still one star. Don reads it as praise; the company's reply above it, "Shut off! Our AI does not lose files!" (v15; was "Correct. We will recover."), now looks absurd |

**What v8 drops from v7:** the portrait falling on the robot (and the robot's dent, REPAIR, REBOOT), the Customer Success Report with FOUND BY: AI, the robot's photo of Don and his FOUND BY AI post. Kept: the clean portrait on the wall (as ep 10 leaves it), the FRI calendar, the taped plan and the 7 from his pocket (the 9 turned back to a 6), Pam's number on the tape, PAM · FINDS THINGS, the three thumbs, Sofía walked past, Mom's look and nod, "Nobody noticed."

**What the change does:** the episode now runs on one question, *who recovers the blueprint*: the AI (fast, glossy, wrong) or the human (slow, taped, right). The crisis has a clock (the lawyer, nine o'clock) and the ending reverses the opening on the same screen: the post that threatened to sue now names Pam.

## The episode in one line

The Client posts that UptimeZ lost his blueprint and his lawyer will call. Don charms him into a meeting and has the robot "recover" it; the AI generates a beautiful plan of the wrong garages. Pam brings the real one, taped, with a hole at 7, and the Client fills it from his own pocket. He corrects his post: Pam found it. Don takes it as praise.

## The protect list (G1)

1. **The post at 0:01**: every phone buzzes, "My lawyer will call.", everyone looks at Don.
2. **The AI's site plan**: approved unseen; the silhouette; "Is this a joke?"; he turns to go.
3. **The human's blueprint**: Pam's taped plan, the hole at 7, the strip from his pocket (the 9 turned back to a 6).
4. **The number**: "Your number.", her pen on the tape, PAM · FINDS THINGS; Sofía walked past.
5. **The UPDATE**: the struck line, "UPDATE: Pam found it.", every phone buzzing again; Pam's phone face down, the peek, "Some post. Others find."; Don proud; "Nobody noticed."

And for Pam, across the episode: glasses up and sleeves up from 4.1; the mic she straightens for Don while he takes the credit (5.4).

## Props and signs (all legible at 270 px)

| Prop | Where | Reads |
|---|---|---|
| The post | 1.2, 6.2 | A feed card: his avatar, **10 GARAGES** · **UptimeZ Find ★☆☆☆☆** · **"Paid $999. They lost my blueprint. My lawyer will call."** · reactions climbing |
| The reply | 1.4, 6.2 | Under the post: **UptimeZ: "Shut off! Our AI does not lose files!"** (v15) (Sofía's polished draft greyed out under it, her avatar in the green open-to-work ring) |
| The UPDATE | 6.2, 6.3b | The post again: **"My lawyer will call."** struck through; under it **"UPDATE: Pam found it."**; still one star. In 6.3b, under it: **PAM: "Some post. Others find."** |
| Don's phone | 2.1, 2.2 | Calling **10 GARAGES**; then his calendar: **FRI · 9:00 · CLIENT** |
| The wall calendar | 1.1, 2.2 | Red **FRI**, beside the door |
| The AI site plan | 3.1–3.5 | **SITE PLAN · RECOVERED BY AI · 99% CONFIDENT** · twelve garages round a driveway whose outline reads as a phallus (props v3); deniable, no anatomy |
| The taped plan | 4.2–4.4 | As ep 10 left it: five strips taped back crooked, the first upside down (its 6 reads as a 9), blue confetti, **a hole at 7** |
| The strip | his shots to 4.3 | Garage 7, ringed in red; peeking from his jacket pocket |
| Her number | 5.2 | **PAM 555 0142** in pen on the tape across 7 |
| His phone | 5.3 | A contact card: **Pam · 555 0142 · note: finds things · ✓ SAVED** |
| Mom's desk | 1.1, 6.6 (the wides) | **ASSISTANT TO DON**, the baby photo, the WORLD'S BEST MOM mug, the candy dish, the DON scarf (longer than in ep 10) |

## Beat 01 · The post · 0:00–0:08

| Shot | Size | What we see | Says | Thinks · eyeline |
|---|---|---|---|---|
| 1.1 | Wide (frame 0) | The front desk as ep 10 leaves it: the clean portrait over Don, the FRI calendar, the robot by Don, Sofía, Pam at the counter, **Mom at her desk** (ASSISTANT TO DON). **0.3 s: every phone buzzes at once**: Don's, Sofía's, Pam's, Mom's; the robot's visor lights. Everyone looks down; **then every head turns to Don** (v10: 1.3 folded in). Don smiles | (all the phones) | All: *Don.* · at Don |
| 1.2 | Insert, a phone | The post: **10 GARAGES · UptimeZ Find ★☆☆☆☆ · "Paid $999. They lost my blueprint. My lawyer will call."** The reactions climbing; a push in on the red line (v16) | CLIENT (v.o., his post, from 1.1): "Paid $999. They lost my blueprint. My lawyer will call." | |
| 1.4 | Two-shot, Don and the robot, then insert | The robot's visor: a reply already drafted. Don, **smug**, thumbs its pad without reading (**thumb 1**, the stain on his cuff). Insert under the post: **UptimeZ: "Shut off! Our AI does not lose files!"** (v15), posted; Sofía's draft greyed out below it | ROBOT: "Reply drafted. Human approval required." · DON: "Approved." · (v16, as it posts) ROBOT: "Shut off! Our AI does not lose files!" | Sofía: *no...* · at her phone |

## Beat 02 · The call · 0:08–0:14

| Shot | Size | What we see | Says | Thinks · eyeline |
|---|---|---|---|---|
| 2.1 | Insert, then medium, Don | (v10) Insert: his phone, **10 GARAGES · calling…**. Then Don flicks his mic down (sales mode), the phone at his ear, the sales smile, a hand on his heart | DON: "Let's fix this together." | *Charm.* · at nobody |
| 2.2 | Insert, Don's phone, then the wall | The Client's voice, flat, from the phone (no bubble; a caption on the screen): his calendar fills **FRI · 9:00 · CLIENT**; the wall clock clicks to nine beside the red FRI | CLIENT (phone): "Nine o'clock. Your office." | |

## Beat 03 · The AI's blueprint · 0:14–0:24

| Shot | Size | What we see | Says | Thinks · eyeline |
|---|---|---|---|---|
| 3.1 | Two-shot, Don and the robot | Don points at the robot: recover it. The robot prints (its signature): a long glossy sheet rolls out | ROBOT: "Blueprint generated. Human approval required." · DON: "Approved." | Don: *done.* · at the door |
| 3.2 | Medium, the door | 9:00. The Client comes in; the 7 strip peeks from his pocket. **Sofía smooths a lapel, touches the earring and steps into his eyeline (KNOWING). He walks past her**, eyes on Don | | Sofía: *he'll notice.* · Client: at Don |
| 3.3 | Medium three, Don presenting | Don unrolls the AI's plan with a flourish | DON: "Recovered." | *Dazzle.* · at the Client |
| 3.4 | Insert, the AI's site plan | **SITE PLAN · RECOVERED BY AI · 99% CONFIDENT**: twelve neat garages round a pale driveway: two round courts, a long drive, a turning circle. Held long enough to take in the whole outline | | |
| 3.5 | Close, the Client | He tilts his head. Again. He gets it: red from the collar up. He looks at Don; then turns for the door | CLIENT: "Is this a joke?" | *That's me they're laughing at.* · at Don |
| 3.5b | Close, Don, 0.6 s | (v11) **A flash of panic**: eyes wide, mouth open; gone by the next cut; **his head jerks and the headset boom swings loose** (v13: it hangs crooked until 5.4) | | *Uh-oh.* · at the Client |

## Beat 04 · The human's blueprint · 0:24–0:33

| Shot | Size | What we see | Says | Thinks · eyeline |
|---|---|---|---|---|
| 4.1 | Medium, the door, then medium, Pam | **He is at the door. Pam steps into his way** with a blue roll under her arm (from her desk, where ep 10 left her taping). She pushes her glasses up into her hair and shoves her sleeves up (they stay up to the end) | | Pam: *wait.* · at the Client |
| 4.2 | Top shot, the desk | Her hands unroll it over the AI's sheet: **MY GARAGES**, five strips taped crooked, the first upside down, **a hole at 7** | | |
| 4.3 | Medium, the Client, then insert | He pats his pocket (ep 9's gesture); his hand comes out with the strip, **7** ringed in red. **He freezes. His face, embarrassed, held 0.5 s** (he had it all along). (v11) **Close: the strip in his own hand**, oil in the creases, its 7 ringed in red, 1 s. Insert: he turns the upside-down strip round (**the 9 becomes a 6**) and lays the 7 in the hole himself; **thumb 2**, Pam's (sleeve shoved up), tapes it | | *...oh.* · at the strip |
| 4.4 | Medium, the robot, the plan in the bottom of frame | The plan is whole. **A beat of defeat**: the robot's visor dims. Then its paddle flips: **HUMAN ✓**, pointed at Pam | ROBOT: "The result was obtained by a h-human." | · at Pam |

## Beat 05 · The number · 0:33–0:40

| Shot | Size | What we see | Says | Thinks · eyeline |
|---|---|---|---|---|
| 5.1 | Two-shot, the Client and Pam; Sofía in front, his back to her | Sofía steps into his path again, smiling; he turns his back on her, to Pam, phone up. Her smile, at his back: CAUGHT → RECOVER | CLIENT: "Your number." | Sofía: *me?* · Client: at Pam |
| 5.2 | Close, Pam, then insert | She freezes, eyes to Don and back; then, without a word, writes **PAM 555 0142** on the tape across 7 | | *Me?* · at Don |
| 5.3 | Insert, his phone | A contact card: **NEW CONTACT · Pam · 555 0142 · note: finds things · ✓ SAVED** (v10) | | |
| 5.4 | Close, Don's head and shoulder, Pam at the edge | (v13: no handshake.) Don beams after the Client, his mic hanging crooked since 3.5b. **Pam's hand comes in, lifts the boom, it overshoots, springs back, settles at his mouth; a tap; her hand leaves.** His eyes never open. Then, into the mic she fixed | DON: "Customer success." | Pam: *there.* · at Don |

## Beat 06 · The UPDATE · 0:40–0:50

| Shot | Size | What we see | Says | Thinks · eyeline |
|---|---|---|---|---|
| 6.1 | Medium, the Client at the door | The whole plan under his arm, **thumb 3** (his, oil in the creases) typing on his phone. He goes | | *Fair.* · at the phone |
| 6.2 | Insert, the phone | His post again: **"My lawyer will call."** struck through; under it **"UPDATE: Pam found it."**; still ★☆☆☆☆; above it, the company's **"Shut off! Our AI does not lose files!"** (v15) | | |
| 6.3 | Close, Pam | **Every phone buzzes again.** Pam's lights up on the counter with her name. **She turns it face down at once.** Then lifts one corner, peeks, and **almost smiles**; her thumb types | | *Me.* · at the phone |
| 6.3b | Insert, her phone | Under his UPDATE: **PAM: "Some post. Others find."** | | |
| 6.5 | Medium, Sofía, her phone | She looks at the rating on her phone, the one star unchanged under "Pam found it." Dry, no smile | SOFÍA: "Still one star." | *Nobody fixed that.* · at her phone |
| 6.6 | Wide (= frame 0) | Every phone still buzzing. Don reads his, puffs up, thumbs in his vest: praise. Hard cut to 1.1 | | Don: *they love us.* · at his phone |

**The loop:** 6.6 is frame 0's wide with every phone buzzing; the buzz carries over the seam into 1.1. Same room, same buzz; the story has moved: **the post that threatened to sue now names Pam, her number is on his phone, the rating is still one star, and Don thinks the feed is praising him.**

## Count

| | |
|---|---|
| Shots | 30 (inserts counted) |
| Lines | 12: the Client 3 (one by phone), Don 5, the robot 3, Sofía 1 (the last); Pam and Mom none. The post, the reply, the UPDATE and Pam's line are read |
| Length | about 43 s on storyboard v5 (beats 8 / 3.5 / 9 / 10 / 7.5 / 7 s); the takes set the real timing |
| Things to read | the post, the reply, FRI, FRI · 9:00 · CLIENT, the AI site plan (its silhouette), the taped plan and the hole, the 9 turned to a 6, the strip's 7, PAM 555 0142, PAM · FINDS THINGS, the UPDATE, "Some post. Others find." |
| Silent signatures | Don: the mic down and up (2.1, 5.4), the vest (6.3) · the Client: the watch, the pocket · Sofía: the lapel and the earring (3.2, 6.5), who noticed · Pam: fixing (4.3), glasses and sleeves up (4.1 to the end), Don's mic (5.4), face down and the peek (6.3) · the robot: prints (3.1) · three thumbs (1.4, 4.3, 6.1) |

## The takes

**v11:** no new takes; `film_v3` without Sofía's "He's not looking at you." (5.4s).

**v10 (20 Nov): `src/cs_voices/film_v3`** (`sound_cs.py takes_v3`): film_v2's eleven unchanged lines, and two new: the Client's "Is this a joke?" (2/3 with Whisper; the second window runs it together) and Sofía's "Still one star." (3/3). 17.7 s of speech.

**Recorded (20 Nov): `src/cs_voices/film_v2`** (`sound_cs.py takes_v2`), 18.3 s of speech, all 13 lines 3/3 with Whisper. Two reads changed so Whisper hears the words: the robot's "Blue print generated" (else "Luprent"), the Client's "I have ten garages." at normal speed (slowed, the end was lost). The Client's "Nine o'clock. Your office." is filtered as a phone. What follows is the plan they were made from.

From `cs_voices/film_v1` (all 3/3 with Whisper): Don's "Approved." (ep 10's take, twice), "Customer success.", the robot's "Reply drafted. Human approval required." and "The result was obtained by a h-human.", the Client's "Your number.", Sofía's two lines. **New to record:** DON "Let's fix this together.", "Recovered."; CLIENT "Nine o'clock. Your office." (through a phone), "I have ten garages."; ROBOT "Blueprint generated. Human approval required."

## Gates still to pass

- **G3** on the storyboard (v2, from this script): the post and the UPDATE legible at 270 px; the AI plan's 12 and CAR WASH readable; the shredder kept out of every shot not about it (the v1 cold test: it made Sofía and Don read as the shredders).
- **G4** a cold mute test of board v2. The v1 test's other fixes carry over: Mom established in frame 0; the 7 strip coming out of *his* pocket; Sofía walked past with his back to her.
- **Canon:** STORYLINE's 11 has the Client "furious" and 12 "The Escalation" (he threatens to cancel). The lawyer threat in 11 moves some of 12 forward; 12 opens on whether he still sues, and on the bank. (v14) The company's public "Shut off! Our AI does not lose files!" is still on record under his UPDATE: episode 12 can use it.
