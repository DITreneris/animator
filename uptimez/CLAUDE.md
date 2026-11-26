# UptimeZ Inc.: rules for agents and workers

These rules apply to the UptimeZ episodes in `uptimez/` only, not to Hoodyz (`../hoodyz/`, which has its own `CLAUDE.md`) or the repo's other videos. Start with [`INDEX.md`](INDEX.md) (where everything is), then [`STORYLINE.md`](STORYLINE.md) (canon).

## Canon in five lines (details in STORYLINE.md)

- **UptimeZ Find** returns 0 RESULTS because no customer data was ever connected. No script fixes it by accident.
- **Don**, CEO, sells for real and believes his own pitch; he approves instead of investigating. **Sofía** wants authority independent of Don, rejects him, and never fakes a record. **Pam** can't stop fixing things, loves Don unrequited, and uses strategic silence.
- **The robot** (desk robot → waiter → HR) is technically true in every statement and stamp. It acts alone only within its permissions, and needs human approval for money, access, commitments and system changes.
- **Mom** works at UptimeZ as Assistant to Don and is used sparingly. **The Client** owns ten garages and is not an idiot. **Father** is the investor and arrives in episode 12 (*Daddy's Home*): a nightclub kingpin, calm, never funny on purpose, with two silent bodyguards.
- **Every episode:** one comic mechanism from two competing desires; the image loops while the story advances; status moves in every scene; it works on mute; the first joke is physical and lands by 0:01.
- **Civil War (13–17):** power is the gold CEO throne with its $49,999 price tag (from 12); the two camps are a tape line on the office floor (from 14). Corporate words stay in the background; mechanisms are physical.

Prequel shorts (*Prompt Telephone*, *Saved to Cloud*, *Downloads Expedition*) use Rush, Max, the laptop AI and Cache, and are outside the main storyline.

## Before writing any code (after Daddy's Home v2, 22 Nov)

1. **Collect the lessons first.** Grep `../docs/lessons.md` for the topic (bubbles, tails, signs, mouths, scale...), write every rule that applies into the episode folder as `<episode>-<topic>-lessons-vN.md` with line numbers, and send it to Tomas before building.
2. **Reuse what was approved.** Search `src/` and `git log origin/main` for a film where the same problem was solved and reviewed (bubbles: `bc_sb.bubble` / `measure`, checks: `qa_bc.py`). Name the file being reused. Write new code only if nothing exists, and say so to Tomas first.
3. **Look before sending.** Open at least six frames at full size, with crops of the details the change touches (where a tail meets its box, the tip on the cheek). A checker that passes is not a reason to send; the frames are.
4. **Hands, arms, gestures, poses:** before any change, follow section 0 of `../docs/rules-hands-and-phones.md` (list the applicable lessons with numbers in the reply, silhouettes for a meaningful gesture, measured gaps at feed size, hand sheet, 10 fps strip, change the gesture after three misreads). This holds for every fix from a review or a cold test, not only for new shots (Daddy's Home v8 round 7 skipped it and made a new misread).
5. **Stop when it isn't converging.** After one hour or two full check runs without the faults going down, stop and report to Tomas instead of patching on.

## Working with Tomas

- **"/grill-me"** means ask the decisions as multiple choice before building (AskUserQuestion, recommended option first), then build exactly what was picked.
- **An outside review** (pasted text or an attachment) gets an OK / partial / fail / disagree table with evidence from frames, levels or files, then "what correlates": the two or three causes behind several points. Say which points undo a choice Tomas made. Build only after "improve" or "proceed".
- **Reply in Lithuanian when he writes Lithuanian**, otherwise English.
- **Commit and push only when asked**, on a branch, never straight to `main`.

## Gates

**How an episode is made, stage by stage** (scene file as the one source, checks that fail the build, Tomas's five stops, version budgets): [`series/production-process.md`](series/production-process.md).

The full gate list for UptimeZ is below. The skill copies in `../hoodyz/.claude/skills/` are written for Hoodyz; don't apply their series check here.

| Gate | Pass |
|---|---|
| G0 Series check | Two characters' wants collide; one comic mechanism; one iconic image; the image loops while the story advances; status moves. Check against STORYLINE.md. **The first joke lands by 0:01 and is physical** (decided 23 Nov): an action readable with no sound and no reading; name it and its frame. A verbal or sign joke may come second (lesson 141) |
| G1 Protect list | The five things that make the episode, written in the script doc |
| G2 Shot list | An action shot and a reaction shot per beat, with size and eyeline |
| G3 Composition | Faces under the title bar, signs whole or out of frame, signs legible at 270 px. Faces **and every story prop** (declared with `of_set.protect()`) out of the dead zones (y > 720; x > 470 between y 380 and 860), measured where the rig drew them, never from typed head points (lessons 124–126). The board is looked at under the mock app overlay |
| G4 Cold mute test | Fresh viewers who have never seen the script (people, or new subagents shown frames only) tell back at least 4 of 5 beats |
| G5 QA worker | Fails the build on any miss (below) |
| G6 Audit triage | At most two review rounds, then go back to premises or test on viewers |
| Drawing audit | `/quality-assurance-agent` before a still is called locked. 16:9 uses `bp_draw_audit.py`. 9:16 uses `uz_check.py`. GV, GP, GD, GH stay in `gates_os.py` for One Star. There is no color-contrast gate |

## Never break earlier work

- New behaviour is **opt-in**: a module flag or a keyword argument whose default draws exactly as before.
- Existing `_vN.py` files stay untouched and keep importing the pinned modules they were built with. **From 24 Nov on (decided), new episodes pin approved versions with immutable `git tag`s** (e.g., `uptimez-<ep>-vN`) instead of copying whole `_vN.py` files in `src/`.
- After any shared-module change, rebuild the approved sheets, covers and renders and **compare md5**. They must be byte-identical.
- New renders get new names; the release a README calls current is replaced only when it's approved.
- **A drawing map's later entry wins.** After replacing a shot's drawing, check that the map points at the new function (print it, or assert it) and look at that shot in the render: two fixes in First Search were overwritten for ten versions (lesson 109).

## Render and QA standard (G5)

| Check | Pass |
|---|---|
| Format | 1080×1920, 30 fps, the expected frame count, BT.709 tags. Native 1080: render at 2× with `set_device_scale(2,2)`, not an upscale |
| Loudness | True peak ≤ −1 dBTP and −14 to −16 LUFS, measured on the final AAC (limit around 0.60; AAC overshoots) |
| Speech | Whisper on every line inside the final mix, three windows per line; a lone word gets the previous line as context; score by words or letters (it runs "Pam a heart" together) |
| Text | Every bubble, card and shout inside the safe area (18, 96, 522, 820 at 540×960) and off the right-hand button rail. Speech bubbles never cover a face. Narration and cards go at the top, under the bar (y 96): the bottom quarter is where TikTok, Reels and Shorts put captions, even inside the safe area |
| Tails | The box beside the face, level with the mouth, and a **short** tail (10–20 px past the box, lessons 174, 325) whose tip lands on the cheek's outline at mouth height, never on the mouth, over the eyes or on hair; aimed at the mouth **drawn in that frame**. A tail may bend only to clear the head; never a long tail wrapped round it. No wall beside the face: reframe the shot (lesson 358). Off-screen speakers only get a quoted card with the name, no tail. New bubbles call `speech.draw`; `bc_sb.bubble` and `qa_bc.py` stay for films already shipped |
| Frame 0 | Complete (no flash, nothing scaling in), held at least 0.4 s before the camera moves, and the last frame leads back into it. The sound runs through the seam: no dead stop before frame 0 (a fade of 0.3 s at most) |
| Size | **From 24 Nov on, new `.mp4` renders and intermediate contact-sheet PNGs (`board`, `layout`, `storyboard`, `cold_test*`) are not committed** (`.gitignore` stops `.git` binary bloat; `./build.sh` and `<ep>_scenes.py` rebuild them locally). Code, scripts, timing JSON, kept dry voice takes and final covers stay tracked. Files committed before 24 Nov stay tracked |

New bubbles call `speech.draw` (`src/speech.py`). The check is `speech_gate.check` (`src/speech_gate.py`); both use the safe rect and the 10–20 px tail in `speech_gate`. The check also fails a box in the button rail (`speech_gate.RAIL`) and, given `avoid=` (the frame's signs, story props and hands, the same rects passed to `speech.draw`), a box over one of them (24 Nov; `speech.draw`'s second pass may cross a sign, so pass `RAIL` in its `avoid` too). Do not add another `TextRec`, another tail length, or another `TAIL_K` table. `kit.bubble` and `fs_animatic.speech` remain for films already shipped. A lesson in `docs/lessons.md` becomes a rule here only after `speech_gate.selftest` fails on that fault.

Validate every new check on a known failure first; a check that always passes is worse than none.

## The set

- **The front desk v4** (`src/fs_set4.py`, [`series/front-desk-set.md`](series/front-desk-set.md)) is the room from episode 10 on: zones A/B/C, home positions, the way out from behind the counter, camera setups S1–S6. Start an episode's staging from it; change it only with a reason written into that doc.
- **Plan in three sheets:** the clean set, a top-down shot plan (setups + table), a blocking sheet for the hardest beat. Before redrawing a board on a set, test the hardest shot as real camera frames with two cold viewers.
- **Reactions face their target; the same cast on both sides of a cut; entrances caught mid-step.**
- **The set is a gate, not a reference** (24 Nov, after Daddy's Home v8 scene 3 moved the throne 404 → 540 between shots and stood Sofía "behind" Mom on her own floor line). `src/set_gate.py` logs every rig and set prop as drawn and fails: a prop off its mark (`PROPS`, from `series/front-desk-set.md`), two overlapping people on one floor line (whoever is behind stands further back: feet higher), a person somewhere else after a cut. An episode lists its exceptions by shot (`SET_MOVES`, `SET_AIR`, `SET_WALKS`) with the reason beside each. A scene's `gate` runs it with the bubble and dead-zone checks; a fix for a bubble or a cold-test note never moves a prop or a person off the set without passing it. Changing the set itself: the doc first, then `PROPS`.

## Look and voices

- **Shared kit:** `src/kit.py`, paper cut-out style. Holiday looks are costumes on the existing characters, never redesigns.
- **Voices (Kokoro):** Don `am_onyx` (the prequel shorts used `am_fenrir`), Sofía `af_bella`, Pam a British voice picked per episode by audition, Mom voice F (`bf_alice` + `bm_lewis`, aged, shouting). The robot's voice is pitched and filtered per episode.
- **Voices are dry** (Tomas, 23 Nov, after One Star v9): no room reverb, reflections or echo on dialogue ("like from a well"); a quiet room tone under the film is fine. A voice effect goes only on a character the viewer sees as its source (the robot); a line over a phone screen or an insert is spoken in a clean voice ("Stupid human." read as "Don in a pipe" in the robot's effect).
- **Check each take with silence after it**, not only alone: Pam's "Check your pocket." passed alone and was heard as "pocketer" in the dry mix (a long released t). Trim the tail and recheck inside the final mix, word by word.
- **No real brands or logos** in the picture. LinkedIn is evoked by culture only.
