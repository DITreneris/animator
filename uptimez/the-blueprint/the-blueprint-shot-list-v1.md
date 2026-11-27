# The Blueprint — paper cut v1

Phase 1 shot list. This is the plan. `src/bp_scenes.py` repeats these durations and generates the script from them. It does not overwrite this file.

Target **6:40 (400 s)**. Inherited coverage plus the 40 s night scene plus the 30 s mute week. Usable inherited blocks sum to 330 s, which is over the 3:00 floor, so this cut does not collapse to 5:00 and does not invent a second plot.

Block times are long-form holds: reaction coverage from the built films, restaged for 16:9. They are longer than the dry-take lengths. Take lengths are in `the-blueprint-line-ledger-v1.md`.

Sources: onboarding script v11 and animation v19 (76.8 s), First Search film v35 (62.9 s, `fs_timing_film35.json`), One Star shot list v19 / master v13 (61.3 s).

Setups: **S0** full desk. **SHRED** two-shot on the shredder. **COUNTER** Pam's end of the counter. **PUSH** a closer two-shot on the same set. **NIGHT** (560, 360, 1.85), approved 25 Nov 2026.

| Time | Dur | Source | Line | Take | Decision | 16:9 |
|---|---:|---|---|---|---|---|
| 0:00 | 18 s | ep 9 v19 open: frame and leaf | — | — | KEEP. Motion test A, the falling frame | S0 |
| 0:18 | 32 s | ob 3.1, 3.2, 3.3, 3.7, 3.12 | Ten garages. Missus. I live alone. Oh… Can it find this when I lose it? | `ob_voices/film` keys 3.1, 3.2, 3.3, 3.7, 3.12 | KEEP | S0 then PUSH |
| 0:50 | 30 s | ob 4.1, 4.3, the shred, 5.4, 5.5 | Here, you will never lose anything again. We'll take care of it. One month. I ask, you find it. Approved. | `ob_voices/film` 4.1, 4.3, 5.4, 5.5 | KEEP. The shred and the finger are silent. Motion tests B and C | SHRED |
| 1:20 | 20 s | ob 8.1, 8.3, 9.1, 10.4 | FIRST CUSTOMER. SOFÍA! WE HAVE A CUSTOMER! Some shit, others scoop. ONBOARDING COMPLETE. | `ob_voices/film` 8.1, 8.3, 10.4. Scoop is **not** in `ob_voices/film/takes.json`. Inherit `ob_voices/film_v10` key 9.1 | KEEP. The walk back to the door is the loop. CUT | S0 |
| 1:40 | 40 s | new | Put recovered on it. Recovered from what? He needs a page by Friday. He needs the bays. I won't draw one. I'm matching them. | none. New | KEEP. The only new talk | NIGHT |
| 2:20 | 30 s | fs film v35 A–D paid | Friday, the bank. Garage eleven. Guaranteed by Friday. Friday. Or I sue. | `fs_voices/film_v13` 1.2, 2.2, 3.3's neighbour D paid is key for the sue line: see ledger | KEEP. The portrait bonk on Don is CUT. The morning frame-drop already happened | S0 |
| 2:50 | 35 s | fs E–G, E2 | It found nothing. Can you make the zero green? Interface change. Approved. | `fs_voices/film_v13` 3.3, F's two lines, the Approved key | KEEP. Sofía's closed mouth on the green sweep is a silent reaction, not a new line | PUSH |
| 3:25 | 30 s | fs T week, T2 | — | — | KEEP as mute pictures: retries, STUPID in lipstick, calendar MON 1 to THU, one deleted message. No new talk | COUNTER |
| 3:55 | 30 s | fs H, X, young man, R2 | Where's my blueprint? Where is his blueprint? Ask the machine. Zero results. Young man. See you in court. | `fs_voices/film_v13` | KEEP. Mom is this one thumb and nothing else | S0 |
| 4:25 | 20 s | cs 1.1–1.4, Stupid human | Paid $999… Reply drafted. Approved. Stupid human. | `cs_voices/film_v9` | KEEP | COUNTER |
| 4:45 | 50 s | cs 3.3–4.4 | Is this a joke? Check your pocket. The result was obtained by a h-human. | `cs_voices/film_v9` | KEEP. Motion test D, the pocket | COUNTER |
| 5:35 | 40 s | cs 5–6 | Your number. Customer success. Some post. Others find. Still one star. | `cs_voices/film_v9` | KEEP. The new picture is Sofía's look at Pam, silent | S0 |
| 6:15 | 25 s | new button | — | — | KEEP. Motion test E. Robot stamps CUSTOMER SUCCESS on the one-star page. No loop | S0 |

**Sum: 400 s. 6:40.**

## Cut, and why

| Source line | Why it is out |
|---|---|
| ob 1.3 "Hi. I'd like to sign up." | The frame drop already says a customer arrived |
| ob 2.1–2.3 Don. CEO. / Founder. And CEO. / CONTACT NOT VERIFIED. | Title run. He sells again at 0:50 |
| ob 6.x Tap here. That worked. Everything you need is in there. | Product re-explanation |
| ob 7.3 CONTACT APPROVED. | The cannon is the celebration |
| ob 10 loop, Client back at the door | Closed-loop ending |
| fs opening bonk onto Don | Second bonk. The morning drop is the only one |
| fs "The zero's green." "Machines." "That hussy." "Eww." "Pam has a plan." "Some post. Others tape." | Mom beyond one thumb, and lines that restate the surface-clean joke |
| fs heal / MON 8 loop | Closed-loop ending |
| cs "Let's fix this together." "Nine o'clock. Your office." "Recovered." "Blueprint generated…" "He's not looking at you." | Phone errand and a line that states Sofía's status out loud |
| cs 6.6 loop | Closed-loop ending |
| Office Noir 3, Father, the throne, the tape | Other episodes |

## Night scene, protect list

Sofía will not draw a fake bay. Pam does not stop matching strips. Nobody names the theme.

1. SOFÍA: "Put recovered on it."
2. PAM: "Recovered from what?"
3. SOFÍA: "He needs a page by Friday."
4. PAM: "He needs the bays."
5. SOFÍA: "I won't draw one."
6. PAM: "I'm matching them."

## Acceptance

330 s of kept blocks from episodes 9–11, plus 40 s night, plus 30 s mute week. Removing the night scene leaves **360 s (6:00)**. That cut-down is `bp_rough_v1_nonight.mp4`, produced so the cut can be watched. This paper cut does not claim the night scene fails.
