# Hoodyz (ME + MY AI): series rules

These rules apply to the episodes in this folder only, not to the rest of the repo.

## Cast

- **Hoody**: navy hoodie; his flaw grows into behaviour. His lines are Tomas's recordings (Kokoro am_puck only as a placeholder).
- **MY AI**: his cheerful companion robot, a perfectionist director with an irritable side in small doses; never a villain. Its antenna is its mood gauge.
- **Eva**: tech lover, charmed by competence, sharp and amused; walks the dog. Voice Kokoro af_heart.
- **The cat**: the recurring runner. **HARV**: strict, professorial, the AI Hoody trained; the recurring antagonist, not the bad guy.
- The series signature is the label switch in the title bar (HIS DATE → ITS DATE, HIS TRIP → ITS TRIP); pop it big for half a second.

## Gates (run them in order; use the `animation-episode-gates` skill)

1. **Series check before any stills:** what Hoody wants, MY AI takes it, an ironic surface, one iconic image, someone who matters watching him fail. Two weak answers: back to premises.
2. **Protect list:** the five things that make the episode, in the concept doc. Check every audit cut against it.
3. **Shot list before key poses:** an action shot and a reaction shot per beat, with size and eyelines. Every story turn is a physical action, never a glance. **Every prop gets a timeline** in the shot list: the shots it is in and its place ("card: shots 11-15, at 640/1714"). Re-derive it whenever the order of events or the loop changes.
4. **Compose for the 9:16 frame:** faces just under the title bar, a foreground layer, eyelines that meet, one real wide early, signs readable at 270 px. Check every shot **at full size (432 px wide or more), never as thumbnails**:
   - **Nothing covers a face or a body,** and nobody is cut in half by the frame edge.
   - **One size rule:** Hoody and Eva are the same height, and MY AI is 0.6 of it. Only distance from the camera changes size, for everyone in that plane together.
   - **Held props sit in the hands:** compute the hand positions (`hand_at`) and put the handle, guitar or rose there. If the pose can't reach, change the pose.
   - **No floating limbs:** a hand comes out of a sleeve, and the sleeve out of the body or the frame edge. A close-up holding a guitar shows the arms.
   - **Props measured on every frame, not looked at:** wrap the prop's draw call, render the whole film and print its position per shot; compare with the prop timeline. A shot that draws its own copy of a prop is how they drift.
   - **The bottom ~250 px belong to the app** (caption, likes, buttons): keep the story above ~1700 px; anchor a camera push-in at the ground line.
   - **Text is fitted by measuring** it against its card or plate, with 30 px margins; crop every label at full size to check nothing covers it.
5. **Motion check** (`python3 hoodyz/motion.py film.mp4 cuts.json`): no shot under ~0.8 unless it is a deliberate hold (a deadpan, a reaction held after the gag). A reaction is a take, not a face swap. Everyone breathes.
6. **Cold mute test on every rough** (`cold-viewer-mute-test` skill): two fresh viewers, both get 4 of 5 beats. They are a smoke test: they find faults inside the structure and never replace a structure Tomas chose.
7. **QA that fails the build** (`python3 hoodyz/qa.py film.mp4 FRAMES lines.json`, exits 1 on any miss): 1080×1920, 30 fps, true peak ≤ −1 dBTP after AAC, −14 to −16 LUFS, speech recognition on every line in the mix, BT.709 tags. Re-run it after **every** mix change: a louder bed can mask a line. Safe zones and the loop seam are still checked by eye.
8. **Audit triage:** ok / partial / fail table, what correlates, protect-list check, at most two rounds.
9. **Tomas watches before anything merges.** A PR stays open until he says so; no agent verdict counts as approval.

## Working with Tomas

- "/grill-me": ask numbered decisions with lettered options, recommended first; he answers like "all a". Then build exactly what was picked.
- **Say his idea back in one line** before writing a concept doc on it (who does what): the Untitled doc was first built on the wrong character.
- Critiques get an ok / fail table with evidence and "what correlates".
- No real brands or logos. Never break shipped renders: new versions in new folders, old ones rebuild byte for byte.
- **His choices are the protect list.** An opening, an ending or a loop he picked is not changed on a test's advice; propose it and let him decide.
- **One structural change per round,** shown next to the version before. When a version comes back worse, return to the last good one and fix that, instead of inventing a new one.
- **Polish has a limit:** agree the number of polish iterations with him up front (two worked for Untitled), then stop and hand over.
