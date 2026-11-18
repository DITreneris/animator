---
name: "animation-episode-gates"
description: "Use when planning, building or reviewing a Hoodyz (ME + MY AI) episode in this folder, to run the stage gates (series check, protect list, shot list, composition, mute test, QA, audit triage) in order."
---

# Episode gates

Each gate has a pass mark and runs before the next stage. A failed gate goes back one stage, not to the start. Report each gate as PASS / FAIL with evidence; never mark a gate passed by judgement alone when it can be measured.

| Gate | Stage | Pass |
|---|---|---|
| G0 Series check | concept | all yes: what the hero wants, the helper takes it, ironic surface, one iconic image, someone who matters sees him fail |
| G1 Protect list | concept | five things that make this episode, written in the concept doc |
| G2 Shot list | before key poses | every beat has an action shot and a reaction shot with size and eyelines; every story turn is a physical action |
| G3 Composition | key poses, and every new or changed shot | at full size: nothing covers a face or body, nobody cut by the frame edge, one size rule, held props in the hands, no floating limbs; signs legible at 270 px |
| G3b Motion | each rough | `hoodyz/motion.py`: no shot under ~0.8 unless it is a named deliberate hold; reactions are takes |
| G4 Cold mute test | each rough | two cold viewers (see `cold-viewer-mute-test`), both tell back at least 4 of 5 beats |
| G5 QA | each render | measured, and the build fails on any miss |
| G6 Audit triage | after any review | table done, protect list checked, at most two rounds |
| G7 Tomas's review | before any merge | he has watched the film and said yes; the PR stays open until then |

## G3 at full size

Thumbnails hide what matters. Perfect Date v2.2 passed a 216 px check with Hoody's head over MY AI and MY AI behind the bench. For every shot, render the start, middle and end at 432 px wide or more and check:

1. **Overlaps:** does any character or prop cover a face or a body that should read? Is anyone cut in half by the frame edge?
2. **Sizes:** measure the characters' heights and keep one rule for the series. For Hoodyz: Hoody and Eva are the same height, and MY AI is 0.6 of it. Only distance from the camera scales everyone in that plane together.
3. **Props in hands:** is everything a character uses (a handle, a guitar, a rose, a card) placed from the hand positions? If the pose can't reach, change the pose, not the prop.
4. **Anatomy:** no floating limbs; arms on anything held in a close-up; a hand comes out of a sleeve, and the sleeve out of the body or the frame edge.

Re-check after every change, including small polish passes: breathing or a shift can push a character into the edge or behind something.

## G5 QA worker

A script that exits non-zero on any failure:

- ffprobe: 1080x1920, 30 fps, expected frame count, BT.709 tags.
- ffmpeg ebur128 on the final AAC file: true peak at or below -1 dBTP, integrated -14 to -16 LUFS.
- Speech recognition on every voice line inside the final mix, windowed with its tail, compared word by word.
- Text boxes outside the app-control zones and at least 30 px from the edges.
- Frame 0 is complete (no flash, nothing scaling in from 0); the last frame leads back into it.
- A thumbnail grid at 270 px wide for legibility of signs and plants.

Validate each check on a known failure first, so a check that always passes is caught.

## G6 Audit triage

For every outside review (another AI, a person, a mute viewer):

1. Table each point as OK / partial / fail / disagree, with evidence from the frames (sizes, durations, levels).
2. Write "what correlates": the two or three causes behind several points.
3. Check every suggested cut against the protect list. A cut that removes a protected item is refused or replaced by a version that keeps it.
4. Say which points were already done and which undo a choice the person made.
5. After two rounds without the laugh arriving, stop polishing and go back to premises.
6. **Agent viewers inform, the person decides.** Never let a viewer's suggestion replace an opening, an ending or a loop the person chose. Put it to them as an option, and keep one structural change per round.
7. When a version comes back worse, return to the last good one and fix it there.

## Asking

When the person wants to decide ("/grill-me"), ask numbered decisions with lettered options, recommended option first, then build exactly what was picked.