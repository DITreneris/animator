# UptimeZ Inc.: rules for agents and workers

These rules apply to the UptimeZ episodes in `uptimez/` only, not to Hoodyz (`../hoodyz/`, which has its own `CLAUDE.md`) or the repo's other videos. Start with [`INDEX.md`](INDEX.md) (where everything is), then [`STORYLINE.md`](STORYLINE.md) (canon).

## Canon in five lines (details in STORYLINE.md)

- **UptimeZ Find** returns 0 RESULTS because no customer data was ever connected. No script fixes it by accident.
- **Don**, CEO, sells for real and believes his own pitch; he approves instead of investigating. **Sofía** wants authority independent of Don, rejects him, and never fakes a record. **Pam** can't stop fixing things, loves Don unrequited, and uses strategic silence.
- **The robot** (desk robot → waiter → HR) is technically true in every statement and stamp. It acts alone only within its permissions, and needs human approval for money, access, commitments and system changes.
- **Mom** works at UptimeZ as Assistant to Don and is used sparingly. **The Client** owns ten garages and is not an idiot. **Father** is the investor and arrives in episode 14.
- **Every episode:** one comic mechanism from two competing desires; the image loops while the story advances; status moves in every scene; it works on mute.

Prequel shorts (*Prompt Telephone*, *Saved to Cloud*, *Downloads Expedition*) use Rush, Max, the laptop AI and Cache, and are outside the main storyline.

## Working with Tomas

- **"/grill-me"** means ask the decisions as multiple choice before building (AskUserQuestion, recommended option first), then build exactly what was picked.
- **An outside review** (pasted text or an attachment) gets an OK / partial / fail / disagree table with evidence from frames, levels or files, then "what correlates": the two or three causes behind several points. Say which points undo a choice Tomas made. Build only after "improve" or "proceed".
- **Reply in Lithuanian when he writes Lithuanian**, otherwise English.
- **Commit and push only when asked**, on a branch, never straight to `main`.

## Gates

The full gate list for UptimeZ is below. The skill copies in `../hoodyz/.claude/skills/` are written for Hoodyz; don't apply their series check here.

| Gate | Pass |
|---|---|
| G0 Series check | Two characters' wants collide; one comic mechanism; one iconic image; the image loops while the story advances; status moves. Check against STORYLINE.md |
| G1 Protect list | The five things that make the episode, written in the script doc |
| G2 Shot list | An action shot and a reaction shot per beat, with size and eyeline |
| G3 Composition | Faces under the title bar, signs whole or out of frame, signs legible at 270 px |
| G4 Cold mute test | Fresh viewers who have never seen the script (people, or new subagents shown frames only) tell back at least 4 of 5 beats |
| G5 QA worker | Fails the build on any miss (below) |
| G6 Audit triage | At most two review rounds, then go back to premises or test on viewers |

## Never break earlier work

- New behaviour is **opt-in**: a module flag or a keyword argument whose default draws exactly as before.
- Pin the previous file as `_vN` before changing it. A pinned file imports the pinned modules it was built with.
- After any change, rebuild the approved sheets, covers and renders and **compare md5**. They must be byte-identical.
- New renders get new names; the release a README calls current is replaced only when it's approved.
- **A drawing map's later entry wins.** After replacing a shot's drawing, check that the map points at the new function (print it, or assert it) and look at that shot in the render: two fixes in First Search were overwritten for ten versions (lesson 86).

## Render and QA standard (G5)

| Check | Pass |
|---|---|
| Format | 1080×1920, 30 fps, the expected frame count, BT.709 tags. Native 1080: render at 2× with `set_device_scale(2,2)`, not an upscale |
| Loudness | True peak ≤ −1 dBTP and −14 to −16 LUFS, measured on the final AAC (limit around 0.60; AAC overshoots) |
| Speech | Whisper on every line inside the final mix, three windows per line; a lone word gets the previous line as context; score by words or letters (it runs "Pam a heart" together) |
| Text | Every bubble, card and shout inside the safe area (18, 96, 522, 820 at 540×960) and off the right-hand button rail. Speech bubbles never cover a face. Narration and cards go at the top, under the bar (y 96): the bottom quarter is where TikTok, Reels and Shorts put captions, even inside the safe area |
| Tails | Each tail ends beside the mouth **drawn in that frame**, curving round outside the head. Off-screen speakers get no tail (a caption, a screen readout or a quoted card instead) |
| Frame 0 | Complete (no flash, nothing scaling in), held at least 0.4 s before the camera moves, and the last frame leads back into it. The sound runs through the seam: no dead stop before frame 0 (a fade of 0.3 s at most) |
| Size | **1080 renders are not committed** (`uptimez/**/*_1080.mp4` is in `.gitignore`); `build.sh` rebuilds them and they're delivered directly. The 540 previews, covers and sheets are committed. The 1080 files committed before 17 Nov stay tracked |

Validate every new check on a known failure first; a check that always passes is worse than none.

## The set

- **The front desk v4** (`src/fs_set4.py`, [`series/front-desk-set.md`](series/front-desk-set.md)) is the room from episode 10 on: zones A/B/C, home positions, the way out from behind the counter, camera setups S1–S6. Start an episode's staging from it; change it only with a reason written into that doc.
- **Plan in three sheets:** the clean set, a top-down shot plan (setups + table), a blocking sheet for the hardest beat. Before redrawing a board on a set, test the hardest shot as real camera frames with two cold viewers.
- **Reactions face their target; the same cast on both sides of a cut; entrances caught mid-step.**

## Look and voices

- **Shared kit:** `src/kit.py`, paper cut-out style. Holiday looks are costumes on the existing characters, never redesigns.
- **Voices (Kokoro):** Don `am_onyx` (the prequel shorts used `am_fenrir`), Sofía `af_bella`, Pam a British voice picked per episode by audition, Mom voice F (`bf_alice` + `bm_lewis`, aged, shouting). The robot's voice is pitched and filtered per episode.
- **No real brands or logos** in the picture. LinkedIn is evoked by culture only.
