# The Blueprint set (16:9) — source of truth

Locked 25 Nov 2026. This is the 16:9 room. [`../series/front-desk-set.md`](../series/front-desk-set.md) and `src/fs_set4.py` stay the 9:16 set. They are not this picture.

Drawn by `src/bp_set.py`. Framed by `src/bp_frame.py`: logical 960×540, centre (480, 270), rendered at 2× to 1920×1080. `kit.W, kit.H` stay 540×960. Nothing here is imported by a shipped episode.

The sheet is [`stills/bp_still_s0.png`](stills/bp_still_s0.png). The two close views are [`stills/bp_still_shred.png`](stills/bp_still_shred.png) and [`stills/bp_still_counter.png`](stills/bp_still_counter.png). Progress is [`changelog.md`](changelog.md).

## What the lock is

The three stills, and the numbers in `bp_set.py` and `bp_frame.py`, are the set. Do not add posters, plants, or props. Do not move the logo, the comic labels, the cabinet, the shredder, the doors, or the people in order to restage. A later pass may animate. It does not redesign the room.

`bp_rough_v1.mp4` and `bp_rough_v1_nonight.mp4` are the **old** room and are not this set. `layouts/` and `motion/` from before the lock are the old coordinates. `bp_rough_v2.mp4` through `bp_rough_v5.mp4` are silent cuts of this room. `bp_pic_v1.mp4` and `bp_pic_v2.mp4` are the picture pass on the same room: bubbles, an overlay on the poster zero, and two hands. None of these is a new lock. `bp_pic_v3.mp4` is the same room with the falling portrait, the cannon firing, and Pam matching the strips. `bp_pic_v5.mp4` is the current picture (sheet look plus clutch hands, watched 27 Nov 2026). Tag `uptimez-blueprint-pic-v4` pins the watched sheet-look cut. The current mix is `bp_sound_v4.mp4` on `bp_pic_v5`.

## Planes

Floor line F = 400. Depth is the feet line, not a new scale. Don stays 0.60 and the tallest.

| Plane | Feet y | Who |
|---|---:|---|
| Back | 418 | Pam, Mom, behind the desk |
| Cabinet | 408 | Against the wall, not in the room |
| Mid | 458 | Client, robot, Sofía |
| Front | 500 | Don. Shredder feet 504 |

## Homes (x, feet, scale)

Client 132, 458, 0.52 · robot 248, 458, 0.48 · Sofía 348, 458, 0.47 · Don 476, 500, 0.60 · Pam 694, 418, 0.50 · Mom 778, 418, 0.50.

Zones stay the 9:16 jobs: A 0–280 arrivals, B 280–570 the irony, C 570–960 the counter and the boss.

## Furniture

| Piece | Where | What stays |
|---|---|---|
| Glass door | (18, 186, 116×214), open 0.85 | Cool reflection on the remaining pane. The open hole stays the street |
| Mat | (4, 402), 164×46 | Darker than the floor, wider than the opening |
| Ficus | x 188, feet on F | One plant. Terracotta pot, ochre rim, three greens, one brown leaf hanging |
| Desk | x 658–846, top front y 340, feet 448 | Light top, darker front face (22px) and lip, open underneath, two legs clear of Pam and Mom |
| On the desk | monitor 676, plan 708, nameplate 752, mug 832 | Both nameplate lines inside the plate. The mug sits on the top |
| Cabinet | x 540, feet 408 | FILES, LOST FILES |
| Shredder | (556, 504, 0.72) | ARCHIVE. Paper stays inside the bin window |
| CEO door | (888, 204, 44×196) | One leaf, hinged right. Plate DON · CEO / VISIONARY. A passage between the desk and the frame |

## Wall, left to right

Screen UPTIMEZ FIND (148, 48, 136×72). Lockup UPTIMEZ INC. (330, 18, height 40). Poster NOTHING GETS LOST / 0 FOUND (300, 78, 100×118). Portrait OUR FIRST CLIENT (508, 128, 0.72). Clock (612, 118). Board (668, 88). CCTV (756, 100) on a wall plate. BEST BOSS (796, 96).

## Light and colour

Window off the left. Six blind bars, softer toward the right, onto the floor. Contact shadows down and to the right, `#817463`.

Wall `#E6D9BE`. Floor `#B9A17F`, four seams that spread toward the camera. Ficus `#46674E` / `#527B59`. Cool glass and the monitor streak `#8CAAB9`. Pot `#9B5945`, rim `#C48B45`.

## Cameras (cx, cy, zoom)

S0 (480, 270, 1.0) the wide. SHRED (300, 386, 1.45) the action, cabinet whole, desk out. COUNTER (730, 320, 1.58) the desk and the passage. PUSH (420, 360, 1.35) is named and not a still. NIGHT (560, 360, 1.85) the night two-shot, approved 25 Nov 2026. Still `stills/bp_still_night.png`. Sofía, Don, Pam and Mom are in it. The night grade is that still. The day colours above do not change.

The counter close-up still crops the top of OUR FIRST CLIENT. The portrait and the CEO plate share a height. Do not add a poster to fill that.

ZERO (357, 108, 2.27), STAMP (246, 430, 2.8) and PLAN (715, 329, 19) are rough crops in `bp_frame.py`, looked at in rough v4. They are not part of this lock.

## Rebuild

From `uptimez/src`: `python3 bp_scenes.py stills`. On this machine the interpreter is `~/bpvenv/bin/python` in WSL (26 Nov 2026). `/tmp/bpvenv` is gone after a WSL restart.

`~/bpvenv` holds numpy 2.3.5, pillow 13.0.0, pycairo 1.29.2, soundfile 0.14.0, scipy 1.18.1, kokoro-onnx 0.4.7, onnxruntime 1.32.0, sherpa-onnx 2.0.3. numpy and pillow are pinned to the versions that drew the locked stills. With them the four stills re-render md5-identical.
