# UptimeZ Inc.

**99.9% uptime. 0% findability.**

An AI office sitcom: short vertical cartoons about ridiculous people using AI, posted as if from the corporate account of a polished SaaS company. The brand is the straight man; the people inside it are the joke. Formerly *Uptime Inc.*

Most videos here are **540×960 animatics** (30 fps, mostly 15 s): rough cuts for audience tests. The exceptions are the *Saved to Cloud*, *Downloads Expedition* and *How Sofía Survived Day One* releases, rendered at 1080×1920.

## Cast

| Badge | Role | In one line | Voice (Kokoro) |
|---|---|---|---|
| **DON** | CEO | Shouts in capitals, understands nothing, softens only when it's about him. Bald. | `am_fenrir` |
| **PAM** | Project manager | "Improves" every instruction on the way down | `bf_emma` |
| **RUSH** | Sales | Panics first, types before he reads | `am_adam` |
| **MAX** | Developer | The only sensible one; asks the fair question, watches it burn | `am_michael` |
| **LAPTOP** | The AI | Two dots and a flat line. Does exactly what it's told and gets overruled | none |
| **CACHE** | Office cat | Always asleep on whatever the humans threw away | none |
| **SOFÍA** | New hire (*Day One*) | Blonde, playful, unimpressed; learns the office's one rule by 17:00 | `af_bella` |
| **DON 2.0** | Don's desk robot (*Day One*) | Waist-high, red tie, copies everything Don does, including delegating to PAM | Don's take, +4 semitones, light metal |

In *How Sofía Survived Day One*, DON is the team lead who approves everything blind, voiced by `am_onyx`; PAM never speaks.

Model sheets and the height line-up are in [`characters/`](characters/). They're drawn by the same kit as the episodes (`src/charsheets.py`), so a sheet always matches the video.

## Brand

Logo files are in [`brand/`](brand/): an uptime pulse line whose last spike becomes a **Z**, in green `#2BB673` on navy `#1F2A44`, plus light, dark and tagline lockups. Type is Lilita One (display) and Inter (UI and post cards). The full system (tokens, voice, post-card rules, character notes) is kept as the *UptimeZ Inc.* Design System artifact on claude.ai; `src/brand.py` regenerates the logo files.

The professional-network post in v04.2+ evokes LinkedIn through its culture only (company page, corporate-speak, reactions), never its logo or exact interface. No trademark search has been done on the name.

## Episodes

### Prompt Telephone — [`prompt-telephone/`](prompt-telephone/)

DON says "Make it bold!", each layer of the company passes it on, and the AI ends up publishing a post about DON's **bald** head.

| File | Version | Notes | Loudness |
|---|---|---|---|
| `uptime_PT_A_bold.mp4` | v03 A | "Bold?" ending | −18.1 LUFS |
| `uptime_PT_B_bald.mp4` | v03 B | "Bald." ending, DON bald | −18.1 LUFS |
| `uptime_PT_v04_1.mp4` | v04.1 | 6 shots, visible cause before effect | −18.0 LUFS |
| `uptimez_PT_v04_2.mp4` | v04.2 | **First UptimeZ-branded cut**: wall sign, badge marks, company post card, DON's portrait, chime | −18.3 LUFS |
| `uptimez_PT_v04_3.mp4` | v04.3 | Bigger opening speaker, lip-sync, blinks, breathing, louder mix | −14.5 LUFS |

Scenario notes: `scenario_v01.md`, `scenario_v03.md`, `scenario_v04_1.md`, `scenario_v04_2.md` (v04.3 is v04.2 plus the polish pass above). Contact sheets: `panels_*.png`.

### Saved to Cloud — [`saved-to-cloud/`](saved-to-cloud/)

PAM backs up everything to the cloud outside the window until it sneezes the office's files everywhere. "Nice. Shared." Then her private doodle of DON (horns, tail, pitchfork) lands on his desk, and he says it back.

| File | Version | Notes |
|---|---|---|
| `uptimez_S136_saved_to_cloud_tag_1080.mp4` | **S1v3.6 release** | **1080×1920**, 25.7 s, −15.3 LUFS. Cold open on the ACHOO, rewind, emoji name tags, three laughs; the last sniff loops into the opening |
| `uptimez_S136_saved_to_cloud_notag_1080.mp4` | S1v3.6 | Same, ending on DON (24.7 s) |
| `uptimez_S135_saved_to_cloud_tag.mp4` | S1v3.5 | 540×960 animatic, first cut with the doodle payoff |
| `uptimez_S131_saved_to_cloud_a.mp4`, `_b.mp4` | S1v3.1 A/B | 15 s test: three search lines vs "CAN MY BOSS SEE THIS?" |

How the versions build on each other (each wraps the last at runtime, none edits it): `s131` A/B → `s132` 21.5 s extension with `anim.py` (pose tweening, walk, squash and stretch, camera) and `engine_v.py` (any length) → `s133` cold open + rewind + freeze frames via a time map → `s134` emoji name tags → `s135` doodle payoff → `s136` final polish, rendered at 2× by `engine_hd.py`. The emoji tags need the Noto Color Emoji font (`/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf`).

### Downloads Expedition — [`downloads-expedition/`](downloads-expedition/)

PAM asks "Where's the final?" without looking up from her keyboard, and points at DOWNLOADS. Behind the door is a cave. RUSH abseils past KEVIN (an intern skeleton still holding FINAL (3)), pulls FINAL (27) from the bottom of the pile, and is blasted back out by the avalanche, bearded. "Got it!" Then PAM saves FINAL (28), which lands on his hard hat. MAX: "Got the original?" RUSH: "Downloads." and hands him the helmet. The tower shakes; a window spits out a page that loops into frame 0.

| File | Version | Notes |
|---|---|---|
| `uptimez_DLX10_expedition_1080.mp4` | **v10 (current)** | **1080×1920**, 21.8 s, BT.709, no branding. Over v9: PAM asks "Where's the final?" (her voice, her mouth, tail beside it) while RUSH listens with his mouth shut; MAX's "Got the original?" sits beside his mouth with a short side tail |
| `uptimez_DLX10_expedition.mp4`, `DLX10_stills_phone.png` | v10 | 540×960 preview, 22 stills |
| `uptimez_DLX9_expedition_1080.mp4` | v9 | 1080×1920, 21.8 s, BT.709, no branding. Over v8: MAX's tail ends beside his mouth, no RUMBLE word on the exterior |
| `uptimez_DLX9_expedition.mp4`, `DLX9_stills_phone.png` | v9 | 540×960 preview, 22 stills |
| `uptimez_DLX8_expedition_1080.mp4` | v8 | 1080×1920, 21.8 s, −15.4 LUFS, −2.2 dBFS peak, tagged BT.709, no branding. Over v7: RUSH's first line in a bubble beside his mouth, his arm reaches behind his head on the handover so only the hand shows on the brim |
| `uptimez_DLX8_expedition.mp4`, `DLX8_stills_phone.png` | v8 | 540×960 preview, 22 stills (cover unchanged: `uptimez_DLX7_thumbnail.png`) |
| `uptimez_DLX7_expedition_final_1080.mp4` | v7 | 1080×1920, 21.8 s, −15.4 LUFS, −2.2 dBFS peak, no branding. Over v6: bubble tails at their speakers (RUSH's at his cheek, MAX's short tail from just above his head), the blast starts below the DOWNLOADS sign with no ghost copies, RUSH's arm bends around his face on the handover, RUMBLE in the sky, the tower spits out FINAL (29) |
| `uptimez_DLX7_expedition_final_tag_1080.mp4` | v7 final, tagged | Same, plus a "Name the exact file. / promptanatomy.app" card over the building in the last 0.6 s (`TAG=1`) |
| `uptimez_DLX7_expedition_final.mp4`, `uptimez_DLX7_thumbnail.png`, `DLX7_stills_phone.png` | v7 | 540×960 preview, cover, 22 stills |
| `uptimez_DLX6_expedition_b_1080.mp4` | v6 (ending B) | 1080×1920, 21.8 s, −15.4 LUFS, −2.2 dBFS peak. Over v5: 0.6 s less wide hold before MAX, MAX reacts to "Downloads." (looks at the door, gulps), shorter beard, RUSH visibly tugs the hard hat out, smear frames on the blast, the pile sheds sheets before the RUMBLE |
| `uptimez_DLX6_expedition_b.mp4`, `uptimez_DLX6_thumbnail.png`, `DLX6_stills_phone.png` | v6 | 540×960 preview, cover, 22 stills |
| `uptimez_DLX5_expedition_b_1080.mp4` | v5 (ending B) | 1080×1920, 22.4 s, −15.5 LUFS, −2.2 dBFS peak |
| `uptimez_DLX5_expedition_b.mp4` | v5 | 540×960 preview of the same cut |
| `uptimez_DLX5_thumbnail.png` | v5 | 1080×1920 cover; title and faces inside the centre 1080×1440 that profile grids crop to (`src/thumb_dlx.py`) |
| `DLX5_stills_phone.png`, `DLX_character_sheet.png` | | 18 stills at phone size; RUSH (office / expedition / after), KEVIN |

Built by `dlx.py` (one module, `ENDING = "A" | "B"`; `dlx_a.py` / `dlx_b.py` apply a 0.6 s trim as a time map) with props from `dlx_kit.py`, a voice-first mix from `sound_dlx.py`, and automatic layout checks in `qa_dlx.py` (faces and eyes never crossed by props, labels or other faces; bubble tails at their speaker; text size and app-button zones). `./build.sh dlx` runs all three (`dlx_tag` for the tagged cut).

### How Sofía Survived Day One — [`sofia-day-one/`](sofia-day-one/)

Sofía's first day. At 9:00 the coffee maker refuses her: WAITING FOR APPROVAL. DON approves everything without looking ("I approve everything."), his robot copies him, and every question ends the same way: "Pam?" First DON, then the robot, then at 17:00 Sofía herself. PAM hands her coffee from her own thermos with one look into the camera. Then DON blindly presses APPROVE, and the 9:00 coffee finally pours. The screen resets, the coffee rewinds back into the machine, and the loop starts again. Pure comedy, no brand card; it should work on mute (clock stamps, the rule of three on "Pam?").

| File | Version | Notes |
|---|---|---|
| `uptimez_day1_loop_v3_1080.mp4` | **loop v3 (current)** | **1080×1920**, 25 s, BT.709, −16.2 LUFS, −1.6 dBFS peak. Mouth shapes from each line's phonemes (lips close on m/b/p, teeth on f/v); matched loop frame: after the reset the coffee rewinds, the evening light returns to morning and the camera settles on the close-up the film opens on |
| `uptimez_day1_loop_v2_1080.mp4` | loop v2 | 1080×1920. Sound pass: the opening is the joke in sound (each BREW press gets an angrier denial over the machine hum), Sofía's heels, PAM's typing (dead stop for her look to camera) |
| `uptimez_day1_loop_v1.mp4` | loop v1 | 540×960. Full animation: eased poses, loudness lip-sync, blinks, hair and hoop lag, screen-reset loop ending |
| `uptimez_day1_animatic_v1.mp4` | animatic v1 | Storyboard v3 with voices and stings, 540×960 |
| `day1_storyboard_silent_v3.mp4`, `_sheet_v3.png` | storyboard v3 | Company badges (Sofía's paper DAY 1 sticker until 17:00, DON 2.0 on the robot), APPROVE plate, contact shadows, evening grade |
| `day1_storyboard_silent_v2.mp4`, `_sheet_v2.png` | storyboard v2 | Review fixes: DON's hand on the button, bubbles clear of faces, spaced 17:00 staging, tighter railway reveal, no white flash |
| `day1_storyboard_silent.mp4`, `day1_storyboard_sheet.png` | storyboard v1 | Silent, 17 shots, sitcom framing (one wide, mirror framing on the three "Pam?") |
| `day1_voice_auditions.mp4` | | Three voices each for DON and Sofía, two robot treatments (chosen: DON B, Sofía B, robot A) |
| `day1_thumbnail.png`, `day1_thumbnail_grid_crop.png` | | 1080×1920 cover (`src/thumb_day1.py`) and its centre 1080×1440 grid crop |
| `sofia_sheet_v1.png`, `sofia_sheet.png`, `sofia_sheet_v3.png` | | Sofía model sheets: first pass, v2 (blonde, shorter skirt, flirtier), v3 badges |
| `day1_props_sheet.png`, `day1_props_sheet_v3.png` | | Robot, coffee maker, railway and train, thermos and mug; v3 badges |

Built from `src/`: `sofia.py` (Sofía), `day1_kit.py` (robot, coffee maker, railway, props), `day1_sb.py` → `day1_sb_v2.py` → `day1_sb_v3.py` (storyboards), `day1_anim.py` → `day1_anim_v2.py` (animation; v2 reads `day1_visemes.json` from `day1_visemes.py`), `sound_day1.py` → `_v4.py` (voices, stings and foley; v2+ wrap every tail across the loop point). Every version is its own file, so each earlier cut still renders unchanged. `kit.py` gained an optional `BADGE_HOOK` (default off, so older episodes draw exactly as before). `./build.sh day1` rebuilds loop v3, `./build.sh day1_thumb` the cover.

### Where Files Live — [`storyboards/`](storyboards/)

Nobody understands what's cloud, local, disk or phone. Storyboard animatics with ending variants.

| File | Idea |
|---|---|
| `uptime_S3_check_downloads_storyboard.mp4` | "Check Downloads" |
| `uptime_S3B_downloads_shadow_ending.mp4` | S3 with the shadow ending |
| `uptime_S3C_downloads_role_reversal.mp4` | S3 with the role-reversal ending |
| `uptime_S1_saved_to_cloud_storyboard.mp4` | "Saved to the cloud" |
| `uptime_S1v2_saved_to_cloud_search_history.mp4` | S1 with the search-history ending |

### History — [`history/saved-locally/`](history/saved-locally/)

The retired first concept, *Saved Locally* (SAVI), v1–v3. Kept as made; see its README.

## Build

```bash
pip install pycairo numpy soundfile kokoro-onnx
# Kokoro model: kokoro-v1.0.int8.onnx + voices-v1.0.bin from the
# thewh1teagle/kokoro-onnx GitHub release, in src/models/ or $KOKORO_DIR
./uptimez/build.sh pt43      # one episode (keys: s3 s1 s3b s3c s1v2 pta ptb pt4 pt42 pt43 s131a s131b)
./uptimez/build.sh s136      # Saved to Cloud release at 1080x1920 (s136n = without the tag)
./uptimez/build.sh dlx       # Downloads Expedition final at 1080x1920 (dlx_tag = with the promptanatomy.app card)
./uptimez/build.sh day1      # How Sofía Survived Day One, loop v3 at 1080x1920 (day1_thumb = cover)
./uptimez/build.sh all       # every episode
./uptimez/build.sh sheets    # logo files + character sheets
```

Stills for checking: `cd uptimez/src && python3 engine.py pt43 0 60 240` writes `pt43_000.png` etc.

How it works: `engine.py` draws each frame with pycairo (paper-cutout kit in `kit.py`, 12 fps boil, slow push-in per panel) and pipes raw frames to ffmpeg; each `sound*.py` voices the lines with Kokoro, synthesizes music and effects in NumPy and writes `<key>_mix.wav`. Newer episodes wrap older modules at runtime (`pt42` wraps `pt4`, `pt43` wraps `pt42` and the kit) instead of editing them, so every earlier cut still rebuilds unchanged. Rebuilding `pt43` and `ptb` from this folder gave frames and loudness identical to the committed files.

Kokoro's model licence hasn't been confirmed for commercial use.
