# The Blueprint — 16:9 progress

The picture is locked. The film is not. The set source of truth is [`set-16x9.md`](set-16x9.md). The 9:16 series is not in this log.

## Now

| | |
|---|---|
| Set | Locked 25 Nov 2026. Sheet `stills/bp_still_s0.png` |
| Close views | `stills/bp_still_shred.png`, `stills/bp_still_counter.png` |
| Paper cut | Shot list, line ledger, script, and cut-down, all v1. 6:40 |
| Rough | `bp_rough_v5.mp4` is the current silent cut of this room, 400 s. `bp_rough_v1.mp4` is the **old** room. v2, v3 and v4 were not rewritten |
| Layouts and motion | `layouts/` and `motion/*_v2.mp4` are on this room. The other `motion/` files are the old coordinates |
| Night | Approved 25 Nov 2026. `stills/bp_still_night.png` `31e044d813fe94ead453458d7b71d5fe`. NIGHT (560, 360, 1.85) is in `set-16x9.md` |
| Drawing audit | `/quality-assurance-agent`. Live `bp_draw_audit.py` exits 0. `--plant` exits 1 with the eight old fails |
| Series code | Branch `uptimez-blueprint` is `d14139b` (26 Nov). `speech.draw` takes `safe=`. A caller that omits it stays on the 9:16 rect |
| Next | Watch `bp_rough_v5.mp4`. SCREEN, BIN, VOID, and the new axes stay unasked |

## Log

### 2026-11-26 — shared files

`origin/main` of `DITreneris/animator` moved from `63888e3` to `d14139b` (One Star v18, Pick a Side). This branch had no commits of its own, so it was fast-forwarded. Nothing was pushed.

The pilot's own files (`bp_*.py`, `the-blueprint/`) are not on `main`, so the fast-forward did not touch them. Six shared files had been edited on both sides. `main`'s versions were kept, and the 16:9 lines were put back on top:

- `speech.py`. `draw` still has `ROBOT`, `pin`, `CLEAR`, `SIGNS_FIRST` and `TOP_FIRST`. It also takes `safe=`. `SAFE_16X9` is (24, 24, 936, 516).
- `speech_gate.py`. `RAIL`, `avoid` and `fill` stay. The button rail is checked only when `safe` is omitted. Selftest passes.
- `pam_mf.py`. `NOSE` stays off by default. `GCHAIN_DX` stays.
- `CLAUDE.md`, `INDEX.md`, `series/front-desk-set.md`. The Blueprint rows stay. So do the hands rule, the set gate, and the Pick a Side v9 line.

`client_ob.py`, `don_v4.py`, `sofia_fs.py`, `uz_check.py`, `series/production-process.md` and `tools/stage5_pack.py` were not on that `main` diff. They were left as they were. `bp_draw_audit.py` still exits 0.

### 2026-11-26 — rough v5

The four stills are in the cut. `bp_rough_v5.mp4` is 400 s, 12000 frames, −15.3 LUFS, peak −1.3 dBTP. `bp_rough_v5_nonight.mp4` is 360 s, 10800 frames, −15.3 LUFS, peak −1.5 dBTP. The first no-night join peaked at −0.9, so those parts were joined again with the limiter at 0.80. v1, v2, v3 and v4 were not rewritten. The four locked stills kept their md5. The note is `rough/bp_rough_v5_note.md`.

### 2026-11-25 — mute week stills

Shot 08 is 30 seconds on COUNTER. On v5 the four reads fill it, 7.5 seconds each, in shot-list order. No new talk. The cards sit on the wall above Pam and Mom. Their heads stay in the frame. OUR FIRST CLIENT keeps the crop already written in the set file.

- Retries. `0 RESULTS` and `RETRY UNTIL FRIDAY`, in the colours of the retry screen in `fs_film35.py`.
- Lipstick. `STUPID`, the letters from `fs_film35.lipstick_word`, and the lipstick from `fs_film35.lipstick`. The robot is outside COUNTER, so the word is on the sheet, not on his back.
- Calendar. MON 1 and THU 4, the page from `fs_film35.calendar`. The shot list stops at Thursday.
- Deleted. One struck line and the word DELETED. First Search has no separate drawing for this card.

Stills: `bp_still_retry.png`, `bp_still_lipstick.png`, `bp_still_calendar.png`, `bp_still_deleted.png`. `bp_draw_audit.py` exits 0. `--plant` exits 1 with the eight old fails. The four locked stills were not rewritten. None of these cards are in `set-16x9.md`.

### 2026-11-25 — one star still

Shot 12 still opens on ZERO for 90 frames. The next 90 frames, on v5 only, are S0 with Sofía's phone in front of her body. One gold star and four empty ones, then 1/5. The mark is `cs_scene6.star`. The poster still says 0. Her head and Don's head stay above the phone.

`stills/bp_still_star.png`. The crop is `stills/bp_still_star_crop.png`. `bp_draw_audit.py` exits 0. `--plant` exits 1 with the eight old fails. The four locked stills were not rewritten. The phone is not in `set-16x9.md`.

### 2026-11-25 — cannon still

Shot 04 already walks for the first 90 frames. The next 90 frames, on v5 only, are the hold with a cannon between the shredder and the desk. `set_ob.cannon`, scale 0.72, feet at the shredder's floor, label CONFETTI. The muzzle points at the bin. Homes, the desk, and both doors stay.

`stills/bp_still_cannon.png`. The crop is `stills/bp_still_cannon_crop.png`. `bp_draw_audit.py` exits 0. `--plant` exits 1 with the eight old fails. The four locked stills kept their md5. The cannon is not in `set-16x9.md`. Rough v5 is not rendered.

### 2026-11-25 — word crops, rough v4

Three words that were already on the wall, each for the first 3 seconds of its shot, then the shot's own camera. No new prop. The poster still says 0.

- ZERO (357, 108, 2.27). Shots 07 and 12. NOTHING, GETS LOST, the green 0, FOUND. The screen, the lockup and OUR FIRST CLIENT are whole in the same frame.
- STAMP (246, 430, 2.8). Shot 13, after the 60-frame stamp on S0. CUSTOMER SUCCESS reads. The robot's head is in the frame.
- PLAN (715, 329, 19). Shot 05. The taped strips, bay 7 a hole. The night hold hides them again, so the approved night still is the hold.

`bp_rough_v4.mp4` is 400 s, 12000 frames, −15.3 LUFS, peak −1.0 dBTP. `bp_rough_v4_nonight.mp4` is 360 s, 10800 frames, the same loudness. v1, v2 and v3 were not rewritten. The four locked stills were not rewritten. The note is `rough/bp_rough_v4_note.md`.

These triples are in `bp_frame.py`. They are not in `set-16x9.md`.

Not drawn: the mute week, STUPID in lipstick, a cannon, a star. SCREEN alone, BIN, and the empty CEO slot were not asked for by the rough.

### 2026-11-25 — Client walks, rough v3

The Client's home stays (132, 458, 0.52). Pose stays stand. `SKIP_CLIENT` defaults off, so a locked still does not move.

- Shot 01. Feet from x 48, inside the glass door, to x 132, the first 90 frames, while the frame falls. The hold is the home.
- Shot 04. Feet from 132 back to about x 80, the first 90 frames. He stays inside S0 and does not cover the robot or the plant. The hold puts him back on the mark. That return is a cut, not a second walk. Shot 06 still has him for Friday.

`bp_rough_v3.mp4` is 400 s, 12000 frames, −15.3 LUFS, peak −1.1 dBTP. `bp_rough_v3_nonight.mp4` is 360 s, 10800 frames, peak −1.1. v1 and v2 were not rewritten. The note is `rough/bp_rough_v3_note.md`. Mid-step stills are in `rough_work/v3/`.

### 2026-11-25 — silent rough v2

The first rough of the locked room. `bp_rough_v1.mp4` was left as the old room.

`bp_rough_v2.mp4` is 400 s, 12000 frames, −15.3 LUFS, peak −1.3 dBTP after the limiter. `bp_rough_v2_nonight.mp4` is 360 s, 10800 frames, peak −1.2. The first concat peaked at −0.9. An `alimiter` at 0.85 was added and the same parts were joined again. No cairo redraw for that fix.

Before this render, three picture faults were closed. The finger is not drawn. The stamp page sits in front of the wheel. The pocket slip passes above Don's head.

Watched with the sound off. What reads, and what the front wall cannot tell, is `rough/bp_rough_v2_note.md`. That note is the brief the walks and the crops were built from.

### 2026-11-25 — drawing audit command

`/quality-assurance-agent` is the command. The file is `.cursor/commands/quality-assurance-agent.md`. It follows `.cursor/skills/quality-assurance-agent/SKILL.md`: name the frame, run the checker, open the PNG at full size, report one table.

16:9 uses `bp_draw_audit.py`. Live exits 0. `--plant` exits 1 with the eight old fails. 9:16 stays on `uz_check.py`. Hoodyz stays on `hoodyz/qa.py`. GV, GP, GD and GH stay in `gates_os.py` for One Star. There is no color-contrast gate.

Written into `series/production-process.md` (stage 4 and the Drawing audit section), `CLAUDE.md`, and `INDEX.md`. The skill's planted misses now match the room: shot 05 is NIGHT, shot 11 is PUSH.

### 2026-11-25 — NIGHT approved

Tomas approved `stills/bp_still_night.png`. The triple NIGHT (560, 360, 1.85) is in `set-16x9.md`. The shot list's 1:40 row now says NIGHT. The six night lines are unchanged. No takes yet. The 7.5 notes (split pants, a second plant, a thinner desk, stronger blinds) were not built. The approved picture is the second light pass.

### 2026-11-25 — night light, second pass

The first night pass still read as a grey veil. The room is now a flat night wall `#596780` (measured rgb 89, 103, 128) and a darker floor `#3E4B63`. Sofía, Don, Pam, Mom, the desk, the cabinet and the shredder are put back from the day frame, so their colours are not in the veil.

Blind bars are `#131C2C`, about 40% quieter. The wall keeps the window slope. The floor bars are flatter and do not continue the wall angle. The monitor glass is `#9EDFFF`, with a short spill and a cyan touch on Pam's face and hands. One warm practical `#E5B36D` sits on the right desk front. A contact shadow sits under the cabinet only.

`bp_still_night.png` is `31e044d813fe94ead453458d7b71d5fe`. The three locked stills and `layouts/bp_layout_final.png` kept their md5. Nothing was added to the empty upper-left of this crop: the logo, the clock and the ficus are already on the wide, and this pass is light only.

### 2026-11-25 — night light

The night frame was a 45% near-black overlay, so it read as a dimmed day. `grade < 1` now runs `_night` in `bp_frame.py` and leaves the day paint alone.

Measured: 30% of `#252E48` over the day wall is still brown, rgb 172, 164, 152. A pale-blue multiply comes first, then the 30% layer. The wall lands at rgb 115, 123, 134.

On top of that, only where it belongs: the six blind bars cooler and carried onto the floor, a warm pool on the desk, the desk monitor glass lit with a spill onto Pam, and a 3-pixel cold rim on the window side of Sofía and Don.

Locked stills and `layouts/bp_layout_final.png` re-rendered with the same md5. `bp_still_night.png` is `41466fe188d6ebfbd4ba926bf5fdcb58`. Camera, homes, and furniture were not moved.
### 2026-11-25 — geometry

The motion marks now sit on the locked room. `bp_set.py` was not touched. Each mark is a constant in `bp_scenes.py`, offset from a prop or a home:

- Shred sheet, shot 03: on the bin's slot, `SHRED_AT` + (5, −123 × 0.72) = (561, 415). The sheet goes from y 397 to y 420.
- Pocket, shot 11: from the Client, `CLIENT` + (30, −146) = (162, 312), to Pam, `PAM` + (62, −128) = (756, 290). The counter dot uses the same end point.
- Stamp, shot 13: page at `ROBOT` + (−36, −56) = (212, 402). The stamp starts 228 above it.

Cameras. Shot 05 is now NIGHT and shot 11 is now PUSH. `layouts()` takes the night camera from the shot. S0, SHRED, COUNTER and PUSH are unchanged.

`bp_draw_audit.py` reads the marks from `bp_scenes.py`, and shot 13 now also requires the robot. `--plant` restores the 25 Nov coordinates and cameras.

```
bp_draw_audit.py          fails 0   exit 0
bp_draw_audit.py --plant  fails 8   exit 1   (03 ×3, 05 pam, 11 client, 11 ×2, 13)
```

The three locked stills re-rendered byte-identical to the `C:\uptimez` copy:

```
25111ff33a2338b32e7bdea584204c28  bp_still_s0.png
da34775d2ac9821b42f149abb8261149  bp_still_shred.png
0a25fcc6b5831f360f24eb79c312fb5f  bp_still_counter.png
1697943d76b767e6dc6f482cf5f94cca  bp_still_night.png        new
efaa3a1e4d7664514bc183d06e4c4c10  layouts/bp_layout_night.png
```

Motion v2: `bp_motion_shred_v2.mp4`, `bp_motion_pocket_v2.mp4`, `bp_motion_stamp_v2.mp4`, each with frames 00, 30 and 59 as PNG. The old `bp_motion_*.mp4` files and `bp_rough_v1.mp4` were not overwritten.

Seen at full size, still open:

- Night still. Sofía and Pam are both in. So are Don and Mom, with Don between the two speakers. Later the same day Tomas approved that occupancy. The lines stay Sofía and Pam.
- Pocket. Halfway along, the slip passes across Don's face, and it reads as a note stuck to his forehead.
- Stamp. The page covers the robot's body and his HR badge. His head stays clear.
- Finger, shot 03. In onboarding 5.1–5.3 it is Pam's raised finger. Pam is not inside SHRED, and a finger on the bin with no arm would be a stray. It was left at the 9:16 floor, and the audit lists it as OPEN, not as a pass.

### 2026-11-25 — set locked

Tomas locked the stills as the 16:9 source of truth after the prop pass. Indexed in `uptimez/INDEX.md`. `fs_set4.py` stays 9:16.

Last picture fixes, on the locked room: the mug sits on the desk, the CCTV has a wall plate, the shredder paper stays inside the bin, the brown ficus leaf hangs as a leaf.

### 2026-11-25 — picture

The room was rebuilt in 960×540 (floor at y 400). It is not a crop of the 9:16 set.

Audits, in order, stills only:

- Geometry. Own CEO door (the 330px door's lower panel hung past this floor). Desk open underneath. Three feet-lines. Contact shadows one direction.
- Type. Both nameplate lines inside the plate. White CEO off the door leaf. FOUND under the green 0. FILES in the holder. ARCHIVE on this shredder only.
- Passage. Desk 658–846, door at x 888, cabinet against the wall with LOST FILES. Shred camera moved so the desk is out and the cabinet is whole.
- Light. Six blind bars from a window off the left, one ficus, darker desk front, cooler glass, wider mat. Floor and wall painted past x 0 and x 960 so the close-ups have no cut edge.
- Colour. Blinds quieter, four floor seams, thicker top, three greens on the ficus, CEO wood lighter. Audit 8.3. Stop adding decoration.
- Logo. `UPTIMEZ INC.` lockup at (330, 18), between the screen and the portrait. Wide only.

`bp_rough_v1` was not re-rendered on any of these passes. Kokoro's commercial licence is still unconfirmed, so there is no public master.
