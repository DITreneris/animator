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
| G3 Composition | key poses | faces in the band under the title bar, a foreground layer, eyelines meet, sizes consistent, signs legible at 270 px |
| G4 Cold mute test | each rough | two cold viewers (see `cold-viewer-mute-test`), both tell back at least 4 of 5 beats |
| G5 QA | each render | measured, and the build fails on any miss |
| G6 Audit triage | after any review | table done, protect list checked, at most two rounds |

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

## Asking

When the person wants to decide ("/grill-me"), ask numbered decisions with lettered options, recommended option first, then build exactly what was picked.