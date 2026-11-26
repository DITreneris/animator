---
name: quality-assurance-agent
description: Detailed drawing audit for scene stills. Measures who is inside the camera, then looks at the frame.
---

# Drawing audit

The hub QA skill checks a pull request. This skill checks a drawing. A still that looks fine at thumbnail size is not a pass. Measure first, then open the picture at full size.

## 1. Name the frame

| Picture | Logical frame | Checker | Set |
|---|---|---|---|
| UptimeZ 9:16 | 540×960, rendered 1080×1920 | `uptimez/src/uz_check.py` | `uptimez/series/front-desk-set.md`, `src/fs_set4.py` |
| Blueprint 16:9 | 960×540, centre (480, 270), rendered 1920×1080 | `uptimez/src/bp_draw_audit.py` | `uptimez/the-blueprint/set-16x9.md` |
| Hoodyz | 1080×1920 | `hoodyz/qa.py` plus the episode gates skill | `hoodyz/CLAUDE.md` |

`kit.W, kit.H` stay 540×960 even while a 16:9 still is drawn. `uz_check.py` reads that size. It is the wrong checker for `bp_frame.py`.

GV face bands (CU r ≥ 120 at 540 px) are the 9:16 bands. S0 at zoom 1.0 is a wide of a 960-wide room, so a face reads smaller. Do not fail it on the 540 bands.

## 2. Read before looking

1. The set source of truth for that frame.
2. `docs/lessons.md` for the thing this still touches (tails, signs, mouths, scale, hands).
3. This skill's `lessons.md`.
4. The scene file's shot row: camera name, line, motion.

If the set file and the scene file disagree, the set file wins for where things stand. The scene file wins for which shot is which. Report the disagreement. Do not edit the set to match the scene.

## 3. Measure the camera

`bp_frame.view` is: translate to the frame centre, scale by zoom, translate by minus the camera point.

Visible world of `(cx, cy, z)` on a `W×H` frame:

- `x` from `cx - (W/2)/z` to `cx + (W/2)/z`
- `y` from `cy - (H/2)/z` to `cy + (H/2)/z`

A head is in frame only when both numbers land inside that rect. Feet below the frame are a crop. A head past the side is a miss.

On 16:9, from `uptimez/src`:

```
python bp_draw_audit.py
```

The interpreter on the build machine is the one named in `set-16x9.md`. Exit 1 is a fail. Do not weaken a row so the script exits 0.

Live cameras are in the scene file. Shot 05 is NIGHT. Shot 11 is PUSH. `--plant` puts back the 25 Nov misses and must exit 1:

- Shot 05 was `SHRED`. Pam's head is outside that camera.
- Shot 11 was `COUNTER`. The Client and both pocket points are outside it.
- The old shred sheet, the finger, and the stamp page sit below y 540. The floor line is y 400.

`frame_fall` is the motion mark that does land inside S0. A check that fails that one is wrong.

## 4. Look at the still

Open the PNG at full size. Crop the detail the change touches. Six frames when the shot moves. A passing script is not a reason to skip this.

On every frame, in this order:

| Check | Fail |
|---|---|
| Speaker | The person who says the line, and the person they say it to, have a head inside the camera |
| Cast across a cut | Someone in the outgoing frame is gone in the next frame with no exit |
| Signs | A word is cut by the frame. Whole in, or whole out. The locked exception is written in `set-16x9.md`: COUNTER crops the top of OUR FIRST CLIENT |
| Type in its plate | A second line falls out of the nameplate, the door plate, or the bin window |
| Props | Paper outside the shredder window, the mug off the desk top, a label off its holder |
| Shadows | Contact shadows disagree about direction. On this 16:9 room they go down and to the right |
| Scale | UptimeZ: Don is the tallest person in a frame he shares. Hoodyz: Hoody and Eva match, MY AI is 0.6 of them. Distance scales a whole plane together |
| Limbs | More than two arms. A held prop whose hand cannot reach it. A tail on hair, a crown, an eye, or the mouth. New UptimeZ tails are 10–20 px past the box, tip on the cheek |
| Text | 9:16 bubbles inside `speech_gate.SAFE` `(18, 96, 522, 820)`. 16:9 bubbles inside `SAFE_16X9` `(24, 24, 936, 516)`. A bubble covers a face |
| Old room | A 16:9 overlay still uses the 9:16 floor (world y around 800). This room's floor is y 400 |
| Lock | A new poster, plant, or moved door, desk, or person, done so the shot would frame |

Hoodyz adds the gates in `hoodyz/.claude/skills/animation-episode-gates/SKILL.md`: full size at 432 px or wider, prop timeline, dead zones x 60–960 and y 210–1600 at 1080×1920. Those numbers are not the UptimeZ numbers.

## 5. Report

One table. A row needs a file, a shot id, and a number.

| Check | Result | Evidence |
|---|---|---|
| Shot 05 Pam | fail | head world (694, 338) on SHRED, visible x ends 631, screen x 1051 |

Result is `ok`, `partial`, `fail`, or `disagree`.

Under the table, two or three causes that explain more than one row. Then say which rows would undo a lock Tomas already made. Do not move the set. The next still, when the geometry is the fault, is a camera or a mark coordinate, measured again before it is written into `set-16x9.md`.

## References

- Agent: `.cursor/agents/quality-assurance-agent.md`
- Hub original (do not run it on these drawings): `C:\059_home_page\.cursor\skills\quality-assurance-agent\SKILL.md`
- Process: `uptimez/series/production-process.md` rule 2. A check counts after it has caught a known failure
