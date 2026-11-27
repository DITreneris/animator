---
description: Audit a scene still. Measure who is inside the camera, then look at the picture at full size.
---

# /quality-assurance-agent

Read `.cursor/skills/quality-assurance-agent/SKILL.md` and follow it. The agent file is `.cursor/agents/quality-assurance-agent.md`. Do not use the hub QA agent. That one reviews a landing page.

## Preflight

Name the frame before measuring. The user may pass a still path, a shot id, or both. If they pass nothing, use the still open in the editor. If none is open, ask which frame.

| Picture | Checker | Set |
|---|---|---|
| UptimeZ 9:16 | `uptimez/src/uz_check.py` | `uptimez/series/front-desk-set.md` |
| Blueprint 16:9 | `uptimez/src/bp_draw_audit.py` | `uptimez/the-blueprint/set-16x9.md` |
| Hoodyz | `hoodyz/qa.py` | `hoodyz/CLAUDE.md` |

`uz_check.py` is the wrong checker for a 16:9 still. GV face bands at 540 px are the wrong bands for S0. There is no color-contrast gate. Do not invent one in the report.

## Plan

1. Read the set file, the shot row, and this skill's `lessons.md`.
2. Run the checker for that picture. A Blueprint run is live, then `--plant`.
3. Open the PNG at full size. Crop the detail the change touches.
4. Report one table. Do not edit the set, the camera, or a character unless the user asked for a fix.

## Commands

Blueprint, from PowerShell. The interpreter is the one named in `set-16x9.md`. An inline `python -c` through `wsl` loses the script, so use the file.

```
wsl -e bash -lc 'cd /mnt/c/04_animator/uptimez/src && /tmp/bpvenv/bin/python bp_draw_audit.py; echo live=$?; /tmp/bpvenv/bin/python bp_draw_audit.py --plant; echo plant=$?'
```

Live exits 0 on the current room. `--plant` must exit 1. A check that fails shot 01, the falling frame, is a bad check. Do not weaken a row so the script exits 0.

9:16 uses `uz_check.py` on that episode's scene file. Hoodyz uses `hoodyz/qa.py`. Do not mix their numbers.

## Verification

Look at the still at full size after the script. A passing script is not a pass. Six frames when the shot moves.

## Summary

One table. A row needs a file, a shot id, and a number. Result is `ok`, `partial`, `fail`, or `disagree`.

| Check | Result | Evidence |
|---|---|---|
| Shot, what | ok | file, the number, the camera |

Under the table, two or three causes. Then name any row that would undo a lock Tomas already made. Do not move furniture, doors, or people so a shot fits.

## Next

A geometry miss is a camera or a mark, measured again before it is written into the set file. A 7-out-of-10 note about pants, a new plant, or a thinner desk is not this command's fix list.
