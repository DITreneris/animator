"""PICK A SIDE (episode 14): the text of every shot and the script's standing sections. From v8 on THIS is where
the words live (lifted once from script v7, 24 Nov); ps_scenes.py reads it and generates the script. Edit here, then
run `python3 ps_scenes.py script`; never edit the generated script."""

ORDER = ['1.1',
 '1.2a',
 '1.2b',
 '1.3',
 '1.4',
 '2.1',
 '2.1b',
 '2.2',
 '2.3',
 '2.4',
 '2.5',
 '2.6',
 '2.7',
 '2.8',
 '2.9',
 '2.9b',
 '2.10',
 '2.11',
 '3.1',
 '3.2',
 '3.3',
 '3.4',
 '3.5',
 '3.6',
 '3.7',
 '4.1',
 '4.2',
 '4.3',
 '5.1',
 '5.2',
 '5.3',
 '5.4',
 '5.5',
 '5.6',
 '5.7',
 '6.1',
 '6.1b',
 '6.2']

SHOTS = {'1.1': {'scene': 'Scene 1 · The Blind',
         'script': 1.8,
         'size': 'MEDIUM · S2, knees up (no floor)',
         'picture': '**FRAME 0.** The glass door, the blind **up**. Don at the left cord, facing us, his eyes up to '
                    "it, the robot at the right cord. Don's hand pulls: the slats rattle down, the room darkens; "
                    "**☀** lights on the robot's visor and its hand pulls them up. Down, up, down, up, each faster",
         'action': 'the tug of war → the ☀ each time it goes dark',
         'line': '',
         'fx': 'rattle ×4, rising'},
 '1.2a': {'scene': 'Scene 1 · The Blind',
          'script': 0.5,
          'size': 'MEDIUM · S2',
          'picture': 'The whole blind tears off its rail and drops over Don; the robot beside him, ☀ on its visor',
          'action': 'the blind falls → CRASH',
          'line': '',
          'fx': 'CRASH of slats'},
 '1.2b': {'scene': 'Scene 1 · The Blind',
          'script': 0.5,
          'size': 'MEDIUM · S3',
          'picture': "Pam, Mom and Sofía mid-room by the counter's end, where the tape will run",
          'action': "the crash → Pam's cup stops halfway",
          'line': '',
          'fx': '—'},
 '1.3': {'scene': 'Scene 1 · The Blind',
         'script': 2.2,
         'size': 'MEDIUM · S2',
         'picture': "Don under the blind, only his face out. The bare glass behind him. The robot's ☀ fades to a "
                    'smile',
         'action': "he doesn't move",
         'line': 'DON (whisper): "This meeting does not exist."',
         'fx': '—'},
 '1.4': {'scene': 'Scene 1 · The Blind',
         'script': 2.6,
         'size': 'MEDIUM · S3',
         'picture': 'Don, the blind over his shoulders like a cape, the tape roll on his wrist. Pam, Mom and Sofía '
                    'behind him',
         'action': 'he lifts the roll → they look at each other',
         'line': 'DON: "My father has a meeting. Without me."',
         'fx': '—'},
 '2.1': {'scene': 'Scene 2 · The Line',
         'script': 1.6,
         'size': 'LOW · S4',
         'picture': 'Floor level. **The tape rips across the floor toward the camera, straight through the group**: '
                    "three pairs of feet hop apart (Pam's flats left, Sofía's heels right, Mom's shoes stay on it)",
         'action': 'the tape → the feet hop',
         'line': '',
         'fx': 'the long tape SCREECH'},
 '2.1b': {'scene': 'Scene 2 · The Line',
          'script': 0.8,
          'size': 'MEDIUM · S3',
          'picture': 'The robot rolls up behind the throne; **a cyan barcode** on its visor, a beep; its claw clips '
                     "a white card on the throne's back: **OWNER: INVESTOR**. It rolls off, pleased",
          'action': 'the clip → the beep',
          'line': '',
          'fx': 'a beep, a clip'},
 '2.2': {'scene': 'Scene 2 · The Line',
         'script': 1.4,
         'size': 'MEDIUM · S3',
         'picture': 'Don passes the throne; its **$49,999** price tag (from 12) swings at the crown. He sees it, and '
                    "spins the throne so the tag faces the wall: **the robot's card turns to the room, OWNER: "
                    'INVESTOR**',
         'action': "the spin → he doesn't look back",
         'line': '',
         'fx': 'the casters spin'},
 '2.3': {'scene': 'Scene 2 · The Line',
         'script': 1.6,
         'size': 'MEDIUM · S3',
         'picture': 'Don stamps on his half, the roll pointed at each of them in turn like a weapon. On the tape: '
                    '**DON** and an arrow',
         'action': 'the roll points → they stiffen',
         'line': 'DON: "Pick a side."',
         'fx': '—'},
 '2.4': {'scene': 'Scene 2 · The Line',
         'script': 1.4,
         'size': 'WIDE · S1',
         'picture': '**Pam** steps over to Don first, quickly. **Her phone stays on the counter, across the line** '
                    '(face up, dark)',
         'action': 'Pam crosses → her phone stays',
         'line': '',
         'fx': '—'},
 '2.5': {'scene': 'Scene 2 · The Line',
         'script': 1.6,
         'size': 'TWO-SHOT · S3',
         'picture': 'Don and Pam. He **salutes** her, solemn; she half returns it with her cup hand, then hides a '
                    'small smile in the cup',
         'action': 'the salute → her half salute, the smile',
         'line': 'DON: "Pam. My general."',
         'fx': '—'},
 '2.6': {'scene': 'Scene 2 · The Line',
         'script': 2.2,
         'size': 'MEDIUM · S6',
         'picture': '**Mom** plants both feet on the tape; arms folded; she looks at Don',
         'action': "she doesn't move",
         'line': 'MOM: "I don\'t pick sides, Donnie."',
         'fx': '—'},
 '2.7': {'scene': 'Scene 2 · The Line',
         'script': 1.0,
         'size': 'MEDIUM · S6',
         'picture': '**Sofía** steps toward Don and stops mid-step',
         'action': 'she stops → her eyes go to the door',
         'line': '',
         'fx': 'a heel click'},
 '2.8': {'scene': 'Scene 2 · The Line',
         'script': 1.0,
         'size': 'INSERT',
         'picture': "**The heel:** her black shoe, heel planted behind the tape, toe on Don's side. Held",
         'action': 'held 0.6 s',
         'line': '',
         'fx': '—'},
 '2.9': {'scene': 'Scene 2 · The Line',
         'script': 1.6,
         'size': 'CLOSE',
         'picture': 'The robot, at its station. Its visor: a small **barrier with a red light**',
         'action': 'it reports',
         'line': 'ROBOT: "Border breach. One heel."',
         'fx': 'a soft two-tone beep'},
 '2.9b': {'scene': 'Scene 2 · The Line',
          'script': 1.2,
          'size': 'CLOSE · S6',
          'picture': "Sofía, the heel still back behind the line, arms loose; she doesn't move it",
          'action': 'flat, not moving',
          'line': 'SOFÍA: "Diplomatic heel."',
          'fx': '—'},
 '2.10': {'scene': 'Scene 2 · The Line',
          'script': 2.6,
          'size': 'TWO-SHOT · S6',
          'picture': 'Don admiring his line, not listening. The robot rolls onto the tape and **balances on it**, '
                     'its one wheel on the line, arms out like a tightrope walker (Tomas, robot sheet /grill-me). '
                     'After "Both.", **0.4 s on Don\'s face**',
          'action': "the wheel on the line → Don's face",
          'line': 'DON: "And you?" · ROBOT: "Both."',
          'fx': 'the wheels squeak'},
 '2.11': {'scene': 'Scene 2 · The Line',
          'script': 3.6,
          'size': 'MEDIUM · S6',
          'picture': 'Review round 1 (Tomas, 24 Nov): one push, not three. Don shoves it off onto his side; it rolls '
                     'straight back, arms still out across the tape, and **bumps Don**, who staggers (1.6 s)',
          'action': 'push, return → Don staggers',
          'line': '',
          'fx': 'squeak, squeak, BONK'},
 '2.12': {'scene': 'Scene 2 · The Line',
          'script': 1.1,
          'size': 'CLOSE · S6',
          'picture': 'Sofía, the heel still back: she **folds her arms** and gives Don one flat look',
          'action': 'arms fold',
          'line': '',
          'fx': '—'},
 '3.1': {'scene': 'Scene 3 · The Selfie',
         'script': 0.8,
         'size': 'MEDIUM · S6',
         'picture': 'Its arm **telescopes** up out of its side, a phone clamped at the tip. Don swings into his big '
                    'pose; Mom on the tape beside him, in frame',
         'action': "the arm → Don poses → Mom's word",
         'line': 'ROBOT: "Smile. Recording." · MOM: "Chin up, Donnie."',
         'fx': 'a servo whir'},
 '3.2': {'scene': 'Scene 3 · The Selfie',
         'script': 2.0,
         'size': 'INSERT (the photo)',
         'picture': 'A camera FLASH (a real flash, lesson 114), then **the photo fills the screen**, rendered from '
                    "this beat's own wide: Don beaming, Pam beside him, Mom on the tape, the robot balancing on the "
                    "tape, **Sofía's heel behind the line**, and **a big silhouette behind the door's glass**",
         'action': 'the photo → held',
         'line': '',
         'fx': 'shutter click'},
 '3.3': {'scene': 'Scene 3 · The Selfie',
         'script': 2.4,
         'size': 'CLOSE',
         'picture': 'The robot turns the phone at the tip of its arm to Don: the photo with **PUBLIC POST?** over it '
                    '(and on its visor)',
         'action': 'it asks',
         'line': 'ROBOT: "Public post? Human approval required."',
         'fx': '—'},
 '3.4': {'scene': 'Scene 3 · The Selfie',
         'script': 1.0,
         'size': 'CLOSE · S3',
         'picture': "Don, still posing, eyes on his own reflection, thumb on the robot's pad without looking",
         'action': 'the thumb',
         'line': 'DON: "Approved."',
         'fx': 'a chime'},
 '3.5': {'scene': 'Scene 3 · The Selfie',
         'script': 1.0,
         'size': 'INSERT (the screen)',
         'picture': 'PUBLIC POST? slides up and away; **#TeamDon 🤝** comes in under it, posted',
         'action': 'posted',
         'line': '',
         'fx': 'whoosh'},
 '3.6': {'scene': 'Scene 3 · The Selfie',
         'script': 1.6,
         'size': 'WIDE · S2',
         'picture': '**DING** behind the glass: the silhouette lifts a glowing phone to its face. In the foreground '
                    'Don still smiles',
         'action': 'the glow → Don smiles on',
         'line': '',
         'fx': 'DING (outside, muffled)'},
 '3.7': {'scene': 'Scene 3 · The Selfie',
         'script': 2.4,
         'size': 'CLOSE · S6',
         'picture': 'Pam sees the glow. Her mouth opens to warn him; she looks at Don posing; her cup comes up to '
                    "her chin (her mouth stays visible for the bubble's tail)",
         'action': 'the cup → silence',
         'line': 'PAM (under her breath, into her cup): "Some pose. Others notice."',
         'fx': '—'},
 '4.1': {'scene': 'Scene 4 · The Booth',
         'script': 0.6,
         'size': 'WIDE',
         'picture': "Red neon over the velvet booth: **THE HOUSE ALWAYS COLLECTS** (12's motto; lesson 148)",
         'action': '—',
         'line': '',
         'fx': 'club bass, low'},
 '4.2': {'scene': 'Scene 4 · The Booth',
         'script': 2.2,
         'size': "INSERT (bodyguard 1's phone)",
         'picture': 'The #TeamDon photo. **A black, oily finger stops on Pam first** and leaves a print on her; then '
                    'it slides across and spreads to zoom on **the heel** (a crop of 3.2: the same shoe, the same '
                    'angle), **a second print right over the heel**',
         'action': 'Pam, then the heel → two smudges',
         'line': '',
         'fx': '—'},
 '4.3': {'scene': 'Scene 4 · The Booth',
         'script': 1.8,
         'size': 'TWO-SHOT',
         'picture': '**The Client** in the velvet booth in his garage coveralls from 13, **filthy with oil**: oil to '
                    'the elbows, a black smear on his cheek, the rag over his shoulder. He points at the phone: '
                    '"That one." **Father** looks at it, then **nods once**: "Invite her."; he doesn\'t look at the '
                    'dirt. Bodyguard 1 does, wipes the phone on his sleeve, and sends. The Client sits back: **a '
                    'black handprint on the velvet**; he checks his watch',
         'action': "the finger → the nod (one frame, lesson 132); the handprint → the bodyguard's look",
         'line': 'CLIENT: "That one." · FATHER: "Invite her."',
         'fx': 'a send whoosh'},
 '5.1': {'scene': 'Scene 5 · The Door',
         'script': 1.4,
         'size': 'MEDIUM · S2',
         'picture': "Outside the glass: bodyguard 2's phone buzzes; he takes Sofía's CV from his breast pocket (from "
                    '12)',
         'action': 'the buzz → the CV',
         'line': '',
         'fx': 'buzz'},
 '5.2': {'scene': 'Scene 5 · The Door',
         'script': 1.6,
         'size': 'INSERT',
         'picture': 'Her CV (the circled number, the lipstick phone); **a gold pen writes C-O-O-?** across the top, '
                    'stroke by stroke (lesson 100)',
         'action': 'written on screen',
         'line': '',
         'fx': 'pen scratch'},
 '5.3': {'scene': 'Scene 5 · The Door',
         'script': 2.4,
         'size': 'WIDE · S1',
         'picture': 'A knock. The robot opens the door. Pam, on a step stool, is re-hanging the blind beside it. '
                    'Sofía walks upstage to the door. Don in the right foreground, at the line, his back to all of '
                    'it',
         'action': 'the door opens → Sofía goes to it',
         'line': 'ROBOT: "Welcome."',
         'fx': 'three knocks; the door'},
 '5.4': {'scene': 'Scene 5 · The Door',
         'script': 2.8,
         'size': 'MEDIUM · S6',
         'picture': '**The office gag.** Don looks right at his own office door, DON · CEO, **across the tape**. A '
                    'foot lifts and hovers over the line (held 0.6 s); he puts it back; he straightens his vest as '
                    'if nothing happened',
         'action': 'the foot → back',
         'line': '',
         'fx': '—'},
 '5.5': {'scene': 'Scene 5 · The Door',
         'script': 1.2,
         'size': 'INSERT',
         'picture': "At the door: the CV into Sofía's hand, **COO?** up. Held",
         'action': 'held 0.6 s',
         'line': '',
         'fx': '—'},
 '5.6': {'scene': 'Scene 5 · The Door',
         'script': 2.4,
         'size': 'MEDIUM · S2, over Pam',
         'picture': 'Pam on the stool in the foreground, the blind in her hands: **she saw COO?**. Beyond her, '
                    "**Sofía steps across the tape** to Father's side",
         'action': "her hands stop → Sofía's step over the line",
         'line': 'PAM (under her breath): "Some draw lines. Others cross them."',
         'fx': '—'},
 '5.7': {'scene': 'Scene 5 · The Door',
         'script': 1.4,
         'size': 'CLOSE · S6',
         'picture': "Sofía, back across the line at the counter. Pam's phone lights up beside her hand: **INVITATION "
                    '· DAD** (0.6 s on the screen inside the shot). She looks up, across the room, at Pam',
         'action': 'the screen → the look',
         'line': '',
         'fx': 'buzz'},
 '6.1': {'scene': 'Scene 6 · Everyone',
         'script': 3.0,
         'size': 'TWO-PLANE, closer than S1: Don big in front, Sofía readable behind (her face and COO? at phone '
                 'size; set at the layouts, after the Sofía sheet review)',
         'picture': "Don alone in front, facing the camera, sincere. Behind him: **Pam's hand reaching across the "
                    "line to her lit phone**, Mom turned away on the tape, **Sofía on Father's side, COO? in hand**, "
                    'the robot at the cord. No glance, no realisation',
         'action': 'his smile → nobody looks at him',
         'line': 'DON: "Everyone\'s with me."',
         'fx': '—'},
 '6.1b': {'scene': 'Scene 6 · Everyone',
          'script': 0.6,
          'size': 'MEDIUM · as 6.1',
          'picture': "Review round 1 (Tomas, 24 Nov, from Office Noir 1's startle): the phone behind him buzzes. Don's "
                     'eyes go round, **his one hair springs straight up**, his eyes snap back over his shoulder to it',
          'action': 'the buzz → the startle, the look to the phone',
          'line': '',
          'fx': 'BZZT, a spring boing'},
 '6.2': {'scene': 'Scene 6 · Everyone',
         'script': 1.0,
         'size': "MEDIUM · S2 (1.1's framing, knees up: the tape out of frame)",
         'picture': "The robot's hand yanks the cord: **the blinds shoot up**; **Don's hand comes in on the left "
                    'cord** and grabs it (he is back at his cord, as in frame 0). Cut to 1.1',
         'action': 'up → his hand on the cord → frame 0',
         'line': '',
         'fx': "rattle up, into 1.1's rattle down"}}

SECTIONS = {'G0: the series check': '| Check | Verdict |\n'
                         '|---|---|\n'
                         '| Two wants collide | Don wants secret loyalty; the robot wants everything in the light '
                         "and on record. Under it: Sofía wants real authority, Father wants Don's people |\n"
                         '| One comic mechanism | The most secret meeting in the world, held with the most '
                         'transparent employee in the world |\n'
                         '| **The 0:01 joke, physical** | **Shot 1.1, frame 0 to 0:01.8:** Don yanks the blinds '
                         "down, the robot's ☀ yanks them up, faster and faster. No sound or reading needed |\n"
                         '| One iconic image | The #TeamDon photo: the team that proves there is no team (also the '
                         'cover) |\n'
                         "| The image loops, the story advances | The last shot (6.2) is 1.1's framing (knees up, "
                         'the tape out of frame): the robot yanks the blinds up and Don grabs his cord again, into '
                         "frame 0. Story: Sofía is on Father's side and Don doesn't know |\n"
                         '| Status moves | Don: boss → divider of the office → his own publicist → shut out of his '
                         'own office → sincerely alone |\n'
                         '| Works on mute | 8 direct questions below; text kept to four reads |',
 'G1: protect list': '1. **The blinds tug of war** at 0:00–0:01.8 (1.1).\n'
                     '2. **The tape through the group and "Pick a side."** (2.1–2.3).\n'
                     '3. **"Public post?" / "Approved." / DING behind the glass**: Don publishes his own secret '
                     '(3.3–3.6).\n'
                     "4. **The held heel**, the same pose in the photo and in the Client's zoom (2.8, 3.2, 4.2).\n"
                     '5. **"Everyone\'s with me."** over Sofía on Father\'s side with COO? (6.1).\n'
                     '\n'
                     'Any later cut that removes one of these is refused or replaced.',
 'Line budget': '19 lines (v5, Tomas: about 18). Don 7 · the robot 5 · Pam 2 · Mom 2 · Sofía 1 · the Client 1 · '
                'Father 1. Every verbal joke has an action: Don\'s whisper from under the fallen blind; "Pick a '
                'side." with the roll pointed like a weapon; "Pam. My general." with a salute; "Both." with the '
                'wheels astride; "Approved." with the thumb on the pad while posing; Pam\'s line into her cup; '
                '"Everyone\'s with me." over the picture that says otherwise.',
 'Props: where each is, shot by shot (lesson 78)': '| Prop | Shots | Where |\n'
                                                   '|---|---|---|\n'
                                                   '| The blinds | 1.1–1.3 (up/down, then torn onto Don), 1.4 '
                                                   '(cape), torn off until 5.3 (Pam re-hangs), 6.2 (hung, up) | The '
                                                   "door's glass, zone A |\n"
                                                   "| The tape | from 2.1 to the end; never in S2's knees-up framing "
                                                   "(1.1, 6.2), so the loop's join holds | World x 560, back wall to "
                                                   "the camera, DON and an arrow on Don's side |\n"
                                                   "| The throne | 2.1b the robot's card clipped on its back; 2.2 "
                                                   'spun (tag to the wall, the card OWNER: INVESTOR to the room), '
                                                   'then stays spun | Zone B, 452 |\n'
                                                   "| Pam's phone | face up and dark from 1.2; lit (INVITATION · "
                                                   "DAD) in 5.7 and 6.1; not in S2's framing, so 6.2 → 1.1 holds | "
                                                   "The counter's left end, Father's side |\n"
                                                   "| The CV | in bodyguard 2's pocket (5.1), COO? (5.2), to Sofía "
                                                   '(5.5), in her hand to the end | — |\n'
                                                   "| The robot's camera arm | 3.1–3.3 | Up, then down |\n"
                                                   '| The silhouette | behind the glass from 3.2 to 5.3, gone after '
                                                   'it | Outside the door |',
 'Hands and bubbles (lessons 169–192, for the layouts, the animatic and G5)': '**Hands.** Every character draws with '
                                                                              'the one hand (`hands_ps`, approved 23 '
                                                                              'Nov) for gestures; grips on props '
                                                                              'reuse what episode 13 solved before '
                                                                              'anything new is drawn (lesson 179):\n'
                                                                              '- **Phones** use '
                                                                              '`of_cast.phone_grip`, its `thumb` '
                                                                              'side checked against the arm it is on '
                                                                              'at every call site (lesson 192): the '
                                                                              "robot's selfie phone (3.1–3.4), Don's "
                                                                              'thumb on APPROVE (3.4: '
                                                                              '`fs_storyboard.thumb` in the insert), '
                                                                              "bodyguard 1's phone and the Client's "
                                                                              "finger (4.2–4.3), Pam's phone (5.7, "
                                                                              '6.1).\n'
                                                                              '- **Every held prop gets a one-piece '
                                                                              'arm from the shoulder** '
                                                                              "(`of_cast.guard_arm_front`, the rig's "
                                                                              'own IK; lessons 179, 186): the tape '
                                                                              "roll (1.4, 2.3), Pam's mug, the CV "
                                                                              '(5.1–5.5), the rag. The prop is drawn '
                                                                              'at the hand the pose returns, never '
                                                                              'on a hand drawn apart from the arm.\n'
                                                                              '- **A reaching arm that would cross a '
                                                                              'face stays behind; only the hand and '
                                                                              'the prop come in front** (lesson '
                                                                              "179): Pam's reach to her phone (6.1), "
                                                                              "the robot's telescopic arm (3.1).\n"
                                                                              '- **Stage the hands before drawing '
                                                                              'them** (lesson 181): each target '
                                                                              "within reach on the character's own "
                                                                              'floor line at the layouts (Mom on the '
                                                                              "tape, Pam at the counter's left end, "
                                                                              "the Client's finger on the phone).\n"
                                                                              '- **If a grip fails three cold '
                                                                              'readings, change the gesture, not the '
                                                                              'grip** (lesson 178). Watch first: '
                                                                              "Pam's half salute (2.5); the fallback "
                                                                              'is the mug lifted like a toast.\n'
                                                                              '\n'
                                                                              '**Bubbles and tails** (lessons '
                                                                              '169–171, 175, 189; G3/G5):\n'
                                                                              '- Every line has its speaker written '
                                                                              'in this script; none is assigned '
                                                                              'while drawing (lesson 169).\n'
                                                                              '- **One curved tail style for the '
                                                                              'film; each tail measured per frame** '
                                                                              '(base, tip, distance to the head '
                                                                              'drawn in that frame), head points in '
                                                                              "the frame's own units (lesson 189). "
                                                                              "Don's whisper in 1.3: the tail ends "
                                                                              "beside his face in the slats' gap. "
                                                                              "Pam's two remarks: beside her mouth, "
                                                                              'which stays clear of the mug. The '
                                                                              'robot: the tail comes in from the '
                                                                              'side to its visor at eye height, and '
                                                                              '**its visor glows while it speaks**, '
                                                                              'so the speaker reads on mute.\n'
                                                                              '- **Typed is not spoken** (lesson '
                                                                              '175): "Public post?", APPROVED, '
                                                                              '#TeamDon and INVITATION · DAD are '
                                                                              'screen text on the phone, never '
                                                                              'bubbles.\n'
                                                                              '- **Every bubble and screen text is '
                                                                              'boxed per frame, the pop included** '
                                                                              '(lesson 170): inside the safe area, '
                                                                              'off the right-hand rail, the '
                                                                              'narration and cards at the top.\n'
                                                                              '\n'
                                                                              '**After each cut:** pull the changed '
                                                                              'shots out of the encoded file, not '
                                                                              'the frames meant for it (lesson 180); '
                                                                              'read the guesses the cold viewers '
                                                                              "make as what the film hasn't shown "
                                                                              'yet (lessons 188, 190); choose a face '
                                                                              "from a sheet of all the rig's faces, "
                                                                              'never by name (lesson 187).',
 'Direct questions for the cold viewers': '1. What are the two people at the window fighting over, and why does the '
                                          'robot pull the blinds up?\n'
                                          '2. What does the yellow line on the floor mean, and whose side is the '
                                          "boss's own office door on?\n"
                                          "3. Who in the photo isn't really on the boss's side? How can you tell?\n"
                                          '4. Who approved putting the photo online?\n'
                                          '5. Who is behind the glass door, and what happened to his phone?\n'
                                          '6. Who decided to make Sofía an offer, and what made them decide?\n'
                                          '7. What is written on the paper Sofía gets?\n'
                                          '8. Where is Sofía standing at the end, and does the boss know?',
 'New to design (stage 3, from v2)': '- **The Client, booth version:** the coveralls from `client_of.py` v2 with an '
                                     'oil layer (opt-in): arms dark to the elbow, a smear on the cheek, dirty hands; '
                                     'must still read as the Client at booth scale.\n'
                                     '- **The oily fingerprint** on the phone glass (4.2) and **the handprint** on '
                                     'the velvet (4.3): both on screen as they happen (lesson 100).'}
