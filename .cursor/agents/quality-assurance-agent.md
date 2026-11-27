---
name: quality-assurance-agent
description: Drawing audit for UptimeZ and Hoodyz scene stills, layouts, and cameras. Use before locking a still, after a prop or camera change, and when a shot list names a person the frame may not hold.
---

# Quality assurance agent

Invoke with `/quality-assurance-agent`.

**Skill (workflow SOT):** `.cursor/skills/quality-assurance-agent/SKILL.md`
**Lessons:** `.cursor/skills/quality-assurance-agent/lessons.md`

Sister of the hub agent at `C:\059_home_page\.cursor\agents\quality-assurance-agent.md`. That agent reviews the landing page, tiers, and GEO. This one reviews scene drawings. Do not import its CI checks.

## When to use

A still, a layout, a camera constant, or a motion mark in `uptimez/` or `hoodyz/`. Before a still is called locked. After a prop pass. When a shot list names a speaker.

## Do not

- Apply the 9:16 gates (`uz_check` at 540×960, face bands at 540, dead zone y > 720) to the 16:9 room
- Apply the Hoodyz size rule (Hoody = Eva, MY AI at 0.6) to UptimeZ, or Don-is-tallest to Hoodyz
- Treat `bp_rough_v1.mp4`, `the-blueprint/layouts/`, or `the-blueprint/motion/` as the locked 16:9 set
- Pass a check that has not failed on a known fault
- Move furniture, doors, or people so a shot fits
- Call a camera good because its name exists. Compute the visible world

## Docs

- UptimeZ: `uptimez/CLAUDE.md`, `uptimez/series/production-process.md`, `uptimez/gates-v2-plan.md`, `uptimez/the-blueprint/set-16x9.md`
- Hoodyz: `hoodyz/CLAUDE.md`, `hoodyz/.claude/skills/animation-episode-gates/SKILL.md`
- 16:9 measurement: `uptimez/src/bp_draw_audit.py`
