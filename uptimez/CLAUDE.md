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

## Render and QA standard (G5)

| Check | Pass |
|---|---|
| Format | 1080×1920, 30 fps, the expected frame count, BT.709 tags. Native 1080: render at 2× with `set_device_scale(2,2)`, not an upscale |
| Loudness | True peak ≤ −1 dBTP and −14 to −16 LUFS, measured on the final AAC (limit around 0.60; AAC overshoots) |
| Speech | Whisper on every line inside the final mix, three windows per line; a lone word gets the previous line as context; score by words or letters (it runs "Pam a heart" together) |
| Text | Every bubble, card and shout inside the safe area (18, 96, 522, 820 at 540×960) and off the right-hand button rail. Speech bubbles never cover a face |
| Tails | Each tail ends beside the mouth **drawn in that frame**, curving round outside the head. Off-screen speakers get no tail (a caption, a screen readout or a quoted card instead) |
| Frame 0 | Complete (no flash, nothing scaling in), and the last frame leads back into it |
| Size | Release files under GitHub's 100 MB limit: `-preset slow -crf 23` for grainy films; keep the high-quality master outside the repo |

Validate every new check on a known failure first; a check that always passes is worse than none.

## Look and voices

- **Shared kit:** `src/kit.py`, paper cut-out style. Holiday looks are costumes on the existing characters, never redesigns.
- **Voices (Kokoro):** Don `am_onyx` (the prequel shorts used `am_fenrir`), Sofía `af_bella`, Pam a British voice picked per episode by audition, Mom voice F (`bf_alice` + `bm_lewis`, aged, shouting). The robot's voice is pitched and filtered per episode.
- **No real brands or logos** in the picture. LinkedIn is evoked by culture only.
