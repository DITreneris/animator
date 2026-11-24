# UptimeZ Inc.

**99.9% uptime. 0% findability.**

An AI office sitcom: short vertical cartoons about ridiculous people using AI, presented in the style of a polished SaaS company's corporate posts. The brand is the straight man; the people inside it are the joke. Formerly *Uptime Inc.*

The prequel shorts here are mostly **540×960 animatics** (30 fps, about 15 s): rough cuts for audience tests. The main-series episodes (from *How Sofía Survived Day One*) are released at **1080×1920** and run 15–90 s; *Saved to Cloud* and *Downloads Expedition* also have 1080 releases.

## Cast

**Series canon lives in [`STORYLINE.md`](STORYLINE.md)**: each character's want, private lie, contradiction and moral line, the relationships, and Season 1. [`INDEX.md`](INDEX.md) maps every document; [`CLAUDE.md`](CLAUDE.md) has the working rules for agents.

### Main series (from *How Sofía Survived Day One*)

| Badge | Role | In one line | Voice (Kokoro) |
|---|---|---|---|
| **DON** | CEO (and whatever title he gives himself) | Sells anything, examines nothing, believes his own pitch. Bald, fleece vest with a ketchup stain | `am_onyx` |
| **SOFÍA** | New hire, then the office's sharpest player | Wants authority independent of Don; rejects him; never fakes a record | `af_bella` |
| **PAM** | Project manager | Can't stop fixing things; loves Don, unrequited; strategic silence | British, picked per episode by audition |
| **THE ROBOT** | One machine, reassigned: Don's desk robot (*Day One*) → cafeteria waiter (*I Will Replace You*) → HR (from *Raises for Everyone*) | Every statement and stamp technically true; needs human approval for money, access and commitments | Pitched and filtered per episode |
| **MOM** | Don's mother; Assistant to Don since *The Best Candidate* | Curlers, an old shouting voice; Don shrinks when she enters | Voice F: `bf_alice` + `bm_lewis`, aged |
| **THE CLIENT** | Owner of ten garages (from *The Onboarding*) | The first real customer; not an idiot. Olive work jacket, VISITOR badge, a head taller than Don | `am_fenrir` −4 semitones |
| **FATHER** | The investor, a nightclub kingpin (from episode 12, *Daddy's Home*) | Holds the majority share; can replace the CEO | not cast yet |

### Prequel shorts (*Prompt Telephone*, *Saved to Cloud*, *Downloads Expedition*)

Same office, before Sofía. These shorts set the tone ("0% findability") but sit outside the main storyline.

| Badge | Role | In one line | Voice (Kokoro) |
|---|---|---|---|
| **DON** | CEO | Shouts in capitals, understands nothing, softens only when it's about him | `am_fenrir` |
| **PAM** | Project manager | "Improves" every instruction on the way down | `bf_emma` |
| **RUSH** | Sales | Panics first, types before he reads | `am_adam` |
| **MAX** | Developer | The only sensible one; asks the fair question, watches it burn | `am_michael` |
| **LAPTOP** | The AI | Two dots and a flat line. Does exactly what it's told and gets overruled | none |
| **CACHE** | Office cat | Always asleep on whatever the humans threw away | none |

In *How Sofía Survived Day One*, DON acts as the team lead who approves everything blind, and PAM never speaks. Don's desk robot is DON 2.0 (waist-high, red tie, copies Don, voiced from Don's take +4 semitones). In *I Will Replace You*, the same robot works as TRAINEE, the cafeteria waiter (`am_echo` +2 semitones, small-speaker tone).

Model sheets and the height line-up are in [`characters/`](characters/). They're drawn by the same kit as the episodes (`src/charsheets.py`), so a sheet always matches the video.

## Brand

Logo files are in [`brand/`](brand/): an uptime pulse line whose last spike becomes a **Z**, in green `#2BB673` on navy `#1F2A44`, plus light, dark and tagline lockups. Type is Lilita One (display) and Inter (UI and post cards). The full system (tokens, voice, post-card rules, character notes) is kept as the *UptimeZ Inc.* Design System artifact on claude.ai; `src/brand.py` regenerates the logo files.

The professional-network post in v04.2+ evokes LinkedIn through its culture only (company page, corporate-speak, reactions), never its logo or exact interface. No trademark search has been done on the name.

## Episodes

This list is not in story order. For the story order (Season 1, episodes 1–8 and what's next), see [`STORYLINE.md`](STORYLINE.md) or [`INDEX.md`](INDEX.md).

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

### I Will Replace You — [`i-will-replace-you/`](i-will-replace-you/)

Cafeteria. DON: "Nice hoops. Can I get in your loop?" SOFÍA: "You're out of the loop." A robot waiter rolls up and she thinks: *Replace him.* It only talks to "sir", serves two cheeseburgers full of bolts, asks "Are you hiring, sir?", snaps upright, points at Sofía: "I WILL REPLACE YOU!", then collapses and whispers "If that's okay, sir?" DON: "Approved." Sofía looks at Don, then at us, a resigned blink; a bolt drops and Don's pun starts again. The joke: AI is coming for your job; it just needs your boss's approval first.

| File | Version | Notes |
|---|---|---|
| `uptimez_iwry_anim_v2_1080.mp4` | **release (current)** | **1080×1920**, 25 s, −16 LUFS. Full animation on storyboard v2: mouths from the real voice takes, blinks (Sofía, Don, Pam, the robot's screen), eased eye darts with hair/hoop lag, Don's lean-in overshoot and nod, Sofía's recoil on the shout, the thumbs-up pop, Pam typing |
| `uptimez_iwry_anim_v2.mp4` | release, 540 rough | Same animation, 540×960, for review before the 1080 render |
| `uptimez_iwry_animatic_v3.mp4` | animatic v3 | 540×960, 25 s, −16 LUFS. Storyboard v2 with voices: Don `am_onyx`, Sofía `af_bella`, robot B `am_echo`. Don's shout without hard clipping (v2 squared 11.5% of its samples into a buzz) |
| `uptimez_iwry_animatic_v2.mp4` | animatic v2 | Robot voice B; the whisper regenerated: de-essed, best of three takes (the v1 high-pass turned its "s" sounds into glitchy bursts) |
| `uptimez_iwry_animatic_v1.mp4` | animatic v1 | Robot voice A |
| `iwry_robot_auditions.mp4` | | Three robot voices (A `am_puck`, B `am_echo`, C `bm_fable`), each with all four lines |
| `iwry_storyboard_silent_v2.mp4`, `_sheet_v2.png` | **storyboard v2** | Review polish: hunched entrance below Don's face, eyes to Sofía before the point, tucked arms on the whisper, larger whisper text, metal separated from the buns, narrative-loop ending |
| `iwry_storyboard_silent.mp4`, `iwry_storyboard_sheet.png` | storyboard v1 | 12 shots, 25 s, silent |
| `iwry_test_a.mp4`, `iwry_test_b.mp4` (+ sheets) | motion tests | Reveal → proud robot → Don's reaction; point → collapse → whisper → "Approved." |
| `robot_sheet_v2.png`, `cafe_set_v2.png` | sheets v2 | Submissive collapse, firm shout face, one-object burgers, per-shot staging with measured gaps, new faces |
| `robot_sheet_v1.png`, `cafe_set_v1.png` | sheets v1 | First robot and set; the 12 cameras on the set |
| `iwry_thumbnail.png`, `iwry_thumbnail_grid_crop.png` | cover | 1080×1920; the shout is the title, the whisper the hook; key art inside the 1080×1440 grid crop |

Built from `src/`: `waiter_kit.py` (robot, pose blending, the screen `"blink"` face), `cafe_kit.py` (set, props, bubbles, per-shot staging `STAGE`, Pam's pose/face params), `iwry_common.py` (shared world and shots; gained `don_tilt`, mouth overlays, `sof_dx`, `don_thumb_scale`, Pam's pose/face — all optional, default off), `iwry_mouths.py` (viseme mouth shapes, shared by Don and Sofía v4), `iwry_visemes.py` (reads the mix's per-line timings into a 12 fps viseme string per character), `iwry_sb.py` / `iwry_sb_v2.py` (silent storyboards), `iwry_anim.py` (full animation: lip-sync, blinks, eased motion; `iwry_anim_v1.py` kept), `iwry_test_a.py` / `_b.py`, `qa_iwry.py` (renders each frame with and without bubbles and flags any bubble over a face), `sound_iwry.py` (voices, stings, mix; `LIPS=1` exports per-frame loudness for the visemes), `thumb_iwry.py`. Earlier versions are kept as `_v1` files. `./build.sh iwry` rebuilds animatic v3, `./build.sh iwry_anim` the release (540 rough + 1080), `./build.sh iwry_thumb` the cover.

### Secret Santa — [`secret-santa/`](secret-santa/)

Christmas at the office. PAM, uncapping a dusty-rose lipstick, whispers: "Sofía… do you think I could pull off nude?" SOFÍA: "On your lips, Pam." "Would Don notice?" "Don notices mirrors." The door bangs open: DON as Agent Secret Santa (cheap shades, an earpiece, a laminated TOP SECRET · SANTA card sealed with a ketchup thumbprint): "Secret Santa! HR-approved!" (the robot THUNKs APPROVED). Pam takes off her glasses and holds them out; Don leans in, catches his own reflection in her lenses and purrs: "Agent Santa. Licensed to gift." She melts. "Don… what would you like Santa to bring?" "Sofía." A smug hold. "Or a full-length mirror." Pam is hurt, then brightens anyway: she writes TO: DON ♥ FROM: PAM on her present's tag and kisses it. The HR robot: "Personal data detected. Anonymizing." It bars the sender (sensible), the recipient (absurd) and, after a considered hover, the kiss (THUNK.). Silence. Pam, glasses back on: "Will Don get it?" The robot moves her present to UNCLAIMED, Don's TO: SOFÍA ♥ FROM: DON (SECRET!) gets APPROVED: "He won't." … "You're welcome." Pam slides a fresh tag toward herself and uncaps the lipstick: frame 0. The joke: the robot does its job perfectly and is the only one who thinks Christmas went well.

| File | Version | Notes |
|---|---|---|
| `uptimez_ss_anim_v2_1080.mp4` | **release (current)** | **1080×1920**, v1 with Don's lips synced (v1 played his lines on his fixed face: his mouth is drawn on top with `iwry_mouths.don_mouth`, not through `mouth=`) |
| `uptimez_ss_anim_v2.mp4` | release, 540 rough | Same, 540×960 |
| `uptimez_ss_anim_v5.mp4` | **animation v5 (final, 18 Nov)**, 540 | 41.9 s, −15.9 LUFS, true peak −3.2 dB, 13/13 lines heard by Whisper, the last frame is frame 0. `ss_anim5.py` over v4: the cold open 1.3× slower; a SOFÍA name plate on her desk; a glint on Don's polished dome; the robot's arm drawn sharp; PERSONAL DATA DETECTED in light text; APPROVED under FROM: DON; a light camera (creeps on Pam's melt, hurt and stare and on the line-up, a small punch-in on each THUNK). Lips, blinks and breaths keep v4's clock. Sound `ss_sound_v5.py` (encoded through a 16 kHz low-pass at 256k: plain 192k AAC overshot to +0.4 dBTP on the kiss THUNK) |
| `uptimez_ss_anim_v4.mp4` | **animation v4 (final, 18 Nov)**, 540 | 41.6 s, −15.7 LUFS, the last frame is frame 0. `ss_anim4.py` after two rounds of cold mute viewers: Pam herself leans in and kisses the blank tag, then the robot's stamp bars the kiss (THUNK at 0.66 s); no UptimeZ sign behind the first bubbles, each bubble just above its speaker and one at a time; a full-screen insert of her half-moon glasses with Don's reflection in both lenses; the payoff as a 2.1 s insert (her barred tag over his TO: SOFÍA ♥ / FROM: DON, APPROVED stamped down), the wide shot without signs, UNCLAIMED or "(SECRET!)". Sound `ss_sound_v4.py`. 1080 rebuilt, not committed |
| `uptimez_ss_anim_v3.mp4` | animation v3, 540 | The joke at 0:01 (`ss_anim3.py`): the tag is kissed off-frame and the robot's stamp bars it; frame 0 holds the fresh tag, so the loop joins. Cold viewers took the stamp for the kisser, hence v4 |
| `uptimez_ss_anim_v1_1080.mp4` | release v1 | **1080×1920**, 40.8 s, −15.8 LUFS, −2.4 dBTP, BT.709. Animatic v3 plus blinks, an idle breathing sway, Sofía's crystal earrings swinging; Don's vest card and the UptimeZ sign always whole |
| `uptimez_ss_anim_v1.mp4` | release, 540 rough | Same animation, 540×960 |
| `ss_animatic_v3.mp4` (v1, v2 kept) | animatic | Storyboard v2 re-timed to the real takes with piecewise time warps (34.6 → 40.8 s; voices never sped up), Pam `bf_emma` (a soft whispered opening), Sofía `af_bella`, Don `am_onyx` (a slower purr), robot B (warmer "You're welcome."), an original jingle-bell bed that drops out with the kiss stamp; v2: shot 4 un-tangled, a tidy earpiece wire, Don's forearm to the dome; v3: the M of PAM no longer cut in the write-on |
| `ss_storyboard_silent_v2.mp4`, `_sheet_v2.png` | **storyboard v2** | Concept v5: the reflection flirt, "Sofía." / "Or a full-length mirror." split, Pam's denial, the whole tag and a bigger kiss, UNCLAIMED vs APPROVED, the matched loop |
| `ss_storyboard_silent_v1.mp4`, `_sheet_v1.png` | storyboard v1 | 16 shots, 36.5 s |
| `ss_motion_v2_A.mp4` (v1 A, B, AB kept) | motion test | Shots 11-14: three stamps (THUNK, THUNK!, take A's THUNK. after a hover), Pam's stare turning to hurt |
| `ss_set_sheet_v2.png` (v1 kept) | set | The office at Christmas (red/green chains, the hand-drawn SECRET SANTA sign with an HR-APPROVED stamp, Pam's present + 2, fairy lights over Sofía's desk), one 9:16 frame per shot; v2 after the cinematic audit |
| `ss_frame0_phone_v2.png`, `don_heads_phone_v2.png`, `robot_bars_phone_v2.png` | phone checks | Frame 0 at real size; Don's three heads (hat, beard, bald agent: C chosen); the stamp bars at real size |
| `ss_thumbnail.png` | cover | UNCLAIMED vs APPROVED in one frame; the hand-drawn sign as the title |

Character sheets are in [`characters/`](characters/) (`*-ss-*`). Built from `src/`: `sofia_ss.py`, `pam_ss.py`, `don_ss.py`, `robot_ss.py`, `props_ss.py`, `ss_set.py`, `ss_motion.py`, `ss_sb.py`, `ss_takes.py` (the kept takes in `ss_takes/`), `ss_timing.py`, `ss_sound.py`, `ss_visemes.py`, `ss_animatic.py`, `ss_anim.py`, `thumb_ss.py`, and the sheet scripts `*_sheet_ss.py`, `ss_set_sheet.py`, `ss_sb_sheet.py`; earlier versions kept as `_v1`/`_v2`, later fixes behind opt-in flags so they rebuild unchanged. `./build.sh ss` rebuilds the mix, both v2 renders and the cover (`./build.sh ss_v1`: v1).

### Mandatory Fun — [`mandatory-fun/`](mandatory-fun/)

The HR robot runs a compulsory AI policy training. The MANDATORY FUN slide slams on: "Attendance is mandatory. So is fun." DON bursts in as self-appointed AI Police (a toy cap a size too small, a giant gold star, yellow toy cuffs on his belt): "AI Police! Who's going to jail?" To SOFÍA: "Sofía, you're under arrest." "For what?" "Stealing my attention." She turns a page. PAM, over her reading glasses: "Officer? I confess." He never looks at her and sulks. The robot scans his sulk: INSUFFICIENT FUN. "Failure to enjoy training. Detention required." "You can't arrest a cop!" It lifts his own cuffs, freezes: HUMAN APPROVAL REQUIRED, and turns to Pam. "APPROVED!" It cuffs Don; Pam quietly snaps the other cuff onto her own wrist. Sofía walks out, Don lunges after her, the chain yanks him back. Pam: "So… dinner?" The scan passes over Don's panic to Pam's smile: FUN DETECTED. "Mandatory fun. Successful." The joke: human oversight works exactly as designed; the approving human just has a conflict of interest.

| File | Version | Notes |
|---|---|---|
| `uptimez_mf_anim_v2_1080.mp4` | **release (current)** | **1080×1920**, 37.3 s, −16 LUFS, BT.709. Lip-sync on Don, Sofía and Pam, blinks, Sofía's swinging hoops, red/amber/green verdict light spill, the robot's idle glow, camera punches (red verdict hit, "APPROVED!" jolt, DING push, the two clicks, a slow push on FUN DETECTED), cool vignette; v2 frames the final shot wider so Pam's and Don's faces stay whole |
| `uptimez_mf_anim_v2.mp4` | release, 540 rough | Same animation, 540×960 |
| `uptimez_mf_anim_v4.mp4` | **animation v4 (final, 18 Nov)**, 540 | 39.65 s, −15.9 LUFS. v3 plus the camera polish (`mf_anim4.py`): motivated creeps and pushes, a whip-pan, a crash zoom on the cuffs, handheld only in the two chaos shots, a punch-in on Pam, a calmer boil, cut signs pushed out of frame. The 1080 master is rebuilt, not committed |
| `uptimez_mf_anim_v3.mp4` | animation v3, 540 | The joke at 0:01 (`mf_anim3.py`): MANDATROY gets zapped to MANDATORY and a party cone lands on the robot; a rewind tail ends on frame 0 |
| `uptimez_mf_anim_v1.mp4` | animation v1, 540 | Before the payoff reframe |
| `mf_animatic_v2.mp4` (v1 kept) | animatic | Storyboard re-timed to the real takes (33.0 → 37.3 s: shots held, never voices sped up), Don `am_onyx`, Sofía `af_bella`, Pam `bf_emma` (her "APPROVED!" pitched up and driven), robot B; an original corporate-training jingle, ducked; v2: the slide whole at frame 0, the cuff insert framed below the star, the scroll never reads "LICE", the final beam aimed at Pam's smile |
| `mf_storyboard_silent_v2.mp4`, `_sheet_v2.png` | **storyboard v2** | Shot 4 from Sofía's side; Pam's 💗 as a cutaway on the word "arrest" |
| `mf_storyboard_silent_v1.mp4`, `_sheet_v1.png` | storyboard v1 | 16 panels, 33 s, the camera plan |
| `mf_yank_test_v2.mp4` (v1 kept) | motion test | Shot 11: taut 0.25 s, a 3-frame release, the cap's flight and landing tap |
| `mf_set_sheet_v2.png` (v1 kept) | set | Door far left, the projector screen with the slide, the table (Sofía, Don's empty chair, Pam); v2: the camera plan, one 9:16 frame per shot |
| `mf_thumbnail.png` | cover | The payoff: Don cuffed to Pam, panicking; Pam beaming in the green FUN DETECTED beam; the slide as the title |

Character sheets are in [`characters/`](characters/) (`*-mf-*`). Built from `src/`: `sofia_mf.py`, `pam_mf.py`, `don_mf.py`, `robot_mf.py`, `props_mf.py` (the toy cuffs and chain), `mf_set.py`, `mf_yank.py` (+ `sound_mf_yank.py`), `mf_sb.py` (storyboard; earlier versions kept as `_v1`..`_v4`), `mf_timing.py`, `sound_mf.py`, `mf_visemes.py`, `mf_animatic.py`, `mf_anim.py`, `thumb_mf.py`, and the sheet scripts `*_sheet_mf.py`, `mf_set_sheet.py`, `mf_sb_sheet.py`. `./build.sh mf` rebuilds the mix, both renders and the cover.

### Raises for Everyone (Thanksgiving) — [`raises-for-everyone/`](raises-for-everyone/)

Thanksgiving at the office. DON slaps down a form: "Raises for everyone! Sign here." It reads I AM HAPPY WITH MY CURRENT SALARY. SOFÍA: "Still hoping for a raise?" PAM: "I'm expecting." Don: "Boy or girl? HA!" The HR robot (paper pilgrim hat): POLICY VIOLATION. Pam: "A raise for saying we don't want one?" Don: "Now you're getting it." Pam: "No." Don tears off a turkey leg: "You failed." Sofía: "She refused. She didn't fail." Don, chewing: "Same thing here." Pam stands, pats her hair (she has a soft spot for him), then: "You're a walking policy violation." Don: "HR. Back me up." ACCURATE. Don covers the verdict with the turkey leg and slides the form to the robot: "Sign it." Muffled: "OK. Signed." The form, signed by the only employee without a salary, gets a 100% SATISFACTION stamp. The joke: the robot judges truth, not loyalty, and the company still gets its number.

| File | Version | Notes |
|---|---|---|
| `uptimez_tg_anim_v2_1080.mp4` | **release (current)** | **1080×1920**, 36.6 s. v1 plus framing fixes: the banner reads THANKFUL whole in shot 1, the whole turkey leg reads over the hidden verdict in shot 11, the pilgrim hat's brim clears the screen, "OK. SIGNED." points at the screen |
| `uptimez_tg_anim_v2.mp4` | release, 540 rough | Same, 540×960 |
| `uptimez_tg_anim_v4.mp4` | **animation v4 (final, 18 Nov)**, 540 | 37.25 s, −15.9 LUFS. v3 plus `tg_anim4.py`: every sign fully in or out of frame (per-shot reframes and set cheats), the second form insert pushes to the Signature line, creeps and pushes, a crash zoom on "You failed.", handheld only in the HR standoff, screen-space bubbles, a calmer boil |
| `uptimez_tg_anim_v3.mp4` | animation v3, 540 | The joke at 0:01 (`tg_anim3.py`): Don's hand slaps I AM HAPPY WITH MY CURRENT SALARY; a fresh blank form drops at the end, so the last frame is frame 0 |
| `uptimez_tg_anim_v1_1080.mp4` | release v1 | **1080×1920**, 36.6 s, −16 LUFS, BT.709. Lip-sync on Don, Sofía and Pam, blinks, Don's laughing bounce, swinging star earrings, red/green verdict light spill, turkey steam, camera punches (slap jolt, verdict hit, "No." push, ACCURATE push, stamp shake), warm vignette |
| `uptimez_tg_anim_v1.mp4` | release, 540 rough | Same animation, 540×960, for review |
| `tg_animatic_v2.mp4` (v1 kept) | animatic | Storyboard v3 re-timed to the real takes (four shots held longer, 35.0 → 36.6 s), voices Don `am_onyx`, Sofía `af_bella`, Pam `bf_emma`, robot B (muffled "OK. Signed."); v2: a real laugh for Don; an original plucked-guitar bed that stops dead on "No." |
| `tg_storyboard_silent_v3.mp4`, `_sheet_v3.png` | **storyboard v3** | Emoji reaction pops: Sofía 🙄 and 😮‍💨, Pam 💗 |
| `tg_storyboard_silent_v2.mp4`, `_sheet_v2.png` | storyboard v2 | New ending: the robot signs; the stamped form |
| `tg_storyboard_silent_v1.mp4`, `_sheet_v1.png` | storyboard v1 | 18 shots, 33 s; close-ups carry the jokes, two tilted shots |
| `tg_set_sheet_v1.png` | set | Day One wall, leaf garland, THANKFUL FOR OUR EMPLOYEES* banner, the long table; 9:16 frames for six key shots |
| `tg_thumbnail.png` | cover | Don's opening line as the title, the turkey leg over the verdict, Pam's stare |

Character sheets are in [`characters/`](characters/) (`*-tg-*`). Built from `src/`: `sofia_tg.py`, `don_tg.py`, `pam_tg.py`, `robot_tg.py` (Thanksgiving looks on the existing characters; v1s kept as `_v1`), `tg_set.py`, `tg_sb.py` (storyboard; `tg_sb_v1.py`, `_v2.py` kept), `sound_tg.py` (voices, laugh, effects, music, mix), `tg_timing.py` (re-timing to the takes), `tg_visemes.py`, `tg_animatic.py`, `tg_anim.py` (the polish, through hooks for this render only; v2, `tg_anim_v1.py` kept), `thumb_tg.py`, and the sheet scripts `*_sheet_tg.py`, `tg_set_sheet.py`, `tg_sb_sheet.py`. `./build.sh tg` rebuilds the mix, both v2 renders and the cover (`./build.sh tg_v1` the v1 renders).

### Office Noir: The Secret of a Stolen Heart — [`office-noir/`](office-noir/)

DON dreams he is a hard-boiled detective in a black-and-white rain-soaked office, the only colour a stolen red heart. His partner, the robot (fedora, trench, silver badge: "My partner. Never blinks."), "Suspect identified." Don's narration: "Nobody tells me what to do. Whiskey. Money. Women." MOM (curlers, an old shouting voice): "DONNIE!" Back in the dream, Don to SOFÍA: "Sofía… did you steal my heart?" SOFÍA, low and slow: "I sign my work… darling." The robot points: "You." Don to PAM: "I was framed!" Every dream object has a reality twin in his bedroom (flask → strawberry milk, informant → a pink bunny, the boss's shadow → Mom, the robot → a baby monitor). Hat gag C: the brim pulled down and a Bogart squint. 40 s, kept long for noir pacing.

| File | Version | Notes |
|---|---|---|
| `uptimez_on_anim_1080.mp4` | **release v8 (current, 17 Nov)** | **1080×1920**, native 1080, 40.1 s, −15.7 LUFS, −1.2 dBTP. Passes the G5 QA worker `src/on_qa.py` (report: `on_qa_report.txt`). v8 fixes after four frame reviews: curved tails ending beside the mouth drawn in that frame; off-screen speakers without tails (Don's line to Sofía as a quoted card, "> SUSPECT IDENTIFIED." as a CCTV readout, the robot's "YOU." on his screen); one Sofía bubble (an older one was hidden underneath); Don's lip-sync mouth scaled to his close-up; every card, bubble and the DONNIE! shout moved under the app's top bar; a clearer "Whiskey" and "Donnie!", and the two stings moved off "Unsigned" and "boss". Previous release (v5) in git history |
| `uptimez_on_anim.mp4` | release v8, 540 preview | Same film, 540×960 |
| `uptimez_on_anim_v9.mp4` | **v9 (final, 18 Nov)**, 540 preview | 43.0 s. A black cat crosses at 0:01 and Don's hat jumps (`cat_on.py`); the narration starts after it, with a pause before "Unsigned."; softer thunder; the cat curled on the bed leaps out; the tail desaturates and dissolves into frame 0. QA report `on_qa_report_v9.txt` |
| `on_tails_v8_check.png`, `on_qa_report.txt` | v8 checks | The ticketed moments; the G5 report |
| `on_cover_v3.png` (v1, v2 kept) | cover | v3 (18 Nov), for Shorts: a small OFFICE NOIR label and one headline, "WHO STOLE THE HEART?", over Don holding his lens to the heart on his own lapel; Mom's curlers on a lit wall. v2: the three title cards |
| `on_animatic_silent.mp4`, `on_animatic_voiced.mp4` | animatics | Storyboard timed to the takes |
| `on_auditions_v5.mp4`, `on_mom_auditions.mp4`, `_v2.mp4` | auditions | Voices; Mom F (`bf_alice` + `bm_lewis`, aged, shouting); Sofía A (−2 semitones, a pause) |
| `on_sb_sheet_v1..v5.png`, `on_sb_loop_v1..v5.png` | storyboard | v5: the partner robot, the brag list, hat C, the cheek tails |
| `on_set_sheet_v1..v3.png`, `on_set_phone_v1..v3.png`, `props_sheet_on_v1..v2.png`, `props_phone_on_v1..v2.png` | set and props | The noir office and its bedroom twin; phone-size checks |

Character sheets: `characters/uptimez-{don,mom,sofia}-on-*`, `uptimez-pam-on-v1..v3-*`. Built from `src/` (`on_*.py`, `*_on.py`, `sound_on*.py`, `thumb_on.py`); `./uptimez/build.sh on`.

### Office Noir 2: The Shadow of Fate — [`office-noir-2/`](office-noir-2/)

New Year special. SOFÍA dreams she is a femme fatale in a black-and-white city on New Year's Eve, red gown and red gloves the only colour. She steps out of a taxi while two gangs shoot it out behind her, and she doesn't blink. In a cabaret a bald detective in a headset hunts for her fingerprints; she slips him a stamp: CASE CLOSED. In the dark UptimeZ office she finds what she came for in Don's drawer, the Client's roll, and hides under the desk as his shoes come in: it was Don. At midnight she wakes up at the office party, asleep on a table with a party blower; Pam sweeps up the icing-sugar prints of her dream: "Some dream. Others sweep." She blows the blower, it gives up, and through the window behind her a taxi pulls up: the film loops.

| File | Version | Notes |
|---|---|---|
| `on2_film_v28_1080.mp4` | **release v28 (current, 20 Nov)**, not committed | 1080×1920, native 1080, 79.2 s, 30 fps, BT.709, −15.0 LUFS, −2.5 dBTP, 16/16 lines heard by Whisper, the last drawing is the first. Rebuild with `./uptimez/build.sh on2`. v27 (18 Nov) was the release before |
| `on2_motion_test_v28.mp4` | v28, 540 preview | v28: a joke by 0:01, the first gunshot at 1.0 s (1.1 is 0.75 s); v25: the first Noir's look (blinds on the walls under the people, a side light, lighter faces, typewriter narration cards at the top); v26: the money, the pour and the office lit; v27: the arms in the bar against smoke. v24 is the last before the new look |
| `office-noir-2-script-v6.md` | script (current) | Line by line with the shot list, as of v28 (the look of v25–v27, the new opening); v1–v5 and concepts v1–v4 kept |
| `on2_shotboard_v8.png` | shot board | One frame from each of the 48 set-ups of v24 |
| `on2_cover_v3.png` (v1, v2 kept) | cover | Her face close, her eyes on the Shadow, his lit hand on her shoulder; OFFICE NOIR 2 label, "The Shadow of Fate". Checked at feed size (120 px) |
| `on2_anim_mute_test_v8.md`, `on2_board_mute_test_v1.md`, `_v4.md`, `on2_pacing_test_v15.md` | tests | Cold mute tests of the board and the animation; the cold pacing test |
| `on1_vs_on2_*.png`, `on2_look_proto_v1.png`, `on2_look_v25_six.png`, `on2_v25_sixteen.png`, `on2_v26_fixed_frames.png` | look | Why the first Noir looked better, and the before/after of the new look |
| `on2_board_v1..v7.png`, `on2_board_mute_v*`, `on2_cast_v1..v5.png` (+ phone), `on2_don_back_v1.png`, `on2_shadow_hat_v1.png`, `on2_two_men_v1.png`, `on2_animatic_v1.mp4`, `on2_narration_*` | development | Board, cast, animatic, narration auditions (A2 chosen) |

Built from `src/`: `on2_motion.py` (timing, the picture, the release; `_v1`…`_v27` kept), `on2_motion_b5.py` and `on2_motion_b68.py` (beats 05 and 06–08), `on2_board.py` (sets), `noir2_cast.py` (the cast in noir), `on2_sound.py` (the takes in `src/on2_voices/`, the mixes), `engine_on.py` (the noir pass; TONE v3 is the new look, `engine_on_v2.py` keeps Office Noir unchanged), `thumb_on2.py` (the cover), `on2_mute_anim.py` (sheets for the cold tests).

### Office Noir 3: The Last Round — [`office-noir-3/`](office-noir-3/)

The Client's dream, between episodes 10 and 11, **release v6 (22 Nov), 540.** Black and white with one red: his gloves and robe. He is a boxer in a dark city, fighting the HR robot for his blueprint hanging over the ring; Mom is the queen of the underground fights, Pam his cutman, Sofía the round-card girl, Detective Don collecting evidence. He wakes on a sofa in one of his garages as Sofía calls.

| File | Notes |
|---|---|
| `office_noir_3_release_v6_540.mp4` | **release v6** (film v38): 87.2 s, −15.5 LUFS, −1.1 dBTP, speech 37 of 37; the 1080 master is rebuilt, not committed |
| `office-noir-3-script-v73.md` | The last script note (the man on the sofa drawn anew); notes v1–v72 kept |
| `office-noir-3-concept-v1.md`, `ring-set.md`, `on3_cover_v1.png` | Concept, the ring set, the cover |

### The Best Candidate — [`the-best-candidate/`](the-best-candidate/)

Three candidates for ASSISTANT TO DON, and an HR robot that rules on bias. DON opens each interview with the same question, "What if I made a mistake?", and marks the answers. The small one (three degrees, "and a half") would show him the data: "Too short." The robot: "Height is not protected. Proceed." The nice macho hands SOFÍA her dropped pen, tells Don "Everybody makes mistakes. It's okay.", and gets "Too distracting." ("For whom?"). Then MOM walks in ("Forty years. One very difficult client."), and to Don's question, asked very small this time: "I'd make you apologize." "Sorry." A two-second pause; his phone has 47 missed calls from a client; he answers it: "Sorry." "Good boy." The robot: "She made him answer the client. Hired." At the door she licks her thumb: "DONNIE! Your vest!" and scrubs it. "Donnie. Father is parking." "Why?" "He's applying for your job." It loops on the door. 92.5 s, 35 lines.

| File | Version | Notes |
|---|---|---|
| `uptimez_bc_anim_v3_1080.mp4` | **animation v3, 1080 master (current)** | **1080×1920**, drawn natively (not upscaled), 92.5 s, 46 MB, −14.0 LUFS, true peak −1.1 dB, BT.709. The same drawings as the 540 film below, frame for frame (bubble boxes included: their text is measured at 540 scale) |
| `uptimez_bc_anim_v3.mp4` | animation v3, 540 | 540×960, 92.5 s, −14.0 LUFS, true peak −1.1 dB. The bubble pass after a frame audit of v2: every tail ends where the drawing says the speaker's cheek or crown is; 18 of the 32 bubbles sit beside the face at mouth height (Sofía, Pam and Mom have framings with clear wall for it), Don at the table and the robot keep theirs overhead, down onto bare scalp or the antenna; a bubble is on screen only while its line is spoken; Don's "smug" face is lip-synced; the chair insert sits under the macho's badge and YES stays whole while Don pushes the paddle. Clean on all 1,110 drawings under `qa_bc.py` v2. Animations v1 (101 s) and v2 (the tightening to 92.5 s, Don's missing lips) are not in the repo; `src/bc_anim_v2.py` still draws v2 |
| `uptimez_bc_anim_v4.mp4` | **animation v4.1 (final, 18 Nov)**, 540 | 89.5 s, −14.1 LUFS. `bc_anim4.py` over v3: the CLIENT · 47 MISSED CALLS phone comes first and is turned face down at 1.0 s, then "First candidate." and one ignored buzz; 3 s off silent holds (breaths and blinks keep v3's phase, so the bubble checks pass on all 1,074 drawings). `sound_bc_mix4.py`: Father's car rolls in, handbrake, engine off and car door under the last shots, so the loop says he is the next candidate. The 1080 master is rebuilt, not committed |
| `the-best-candidate-interview-script-v1..v6.md` | script | v6 is cut: "Good boy.", "Donnie. Father is parking.", the measured section times |
| `bc_storyboard_v1..v3_1.png`, `_2.png`, `bc_storyboard_phone_v1..v3.png`, `bc_storyboard_silent_v1..v3.mp4` | storyboard | 64 panels. v3 is the first bubble pass (one speaker to a panel, signs whole or absent, inserts for what must be read). The animation's board has since moved on (`src/bc_sb.py`); no v4 pages have been drawn |
| `bc_set_sheet_v1..v4.png`, `bc_set_phone_v1..v4.png` | set | The interview room: the door, the notice, the BIAS MONITOR and its states; v3 hangs the signs higher to leave wall for bubbles, v4 adds the ficus, a dado and window light |
| `bc_cast_sheet_v1..v3.png`, `bc_cast_phone_v1..v3.png`, `mom_bc_*`, `sofia_bc_*`, `pam_bc_*`, `bc_tech_sheet_v3.png` | cast | The small one and the nice macho (new), Mom, Sofía and Pam dressed for the interview, the robot's rulings |

Built from `src/`: `bc_set.py` (set v4; `_v1`…`_v3` kept), `cand_bc.py`, `don_bc.py`, `mom_bc.py`, `sofia_bc.py`, `pam_bc.py`, `props_bc.py` (characters and props, earlier versions kept), `bc_sb.py` (the board: cameras, the `SAY` table of every bubble, `measure()`), `qa_bc.py` (the checks), `sound_bc.py` (the takes, kept in `src/bc_voices/`), `sound_bc_mix.py` (effects, the looping bed, the master), `bc_anim.py` (timing, lip-sync, actions, light, the render). `./uptimez/build.sh bc` checks and rebuilds the animation from the kept takes: no voice is re-recorded, but the Kokoro model files must be in `src/models` or `KOKORO_DIR`, because the older sound modules the mix borrows its effects from load them on import.

### The Onboarding — [`the-onboarding/`](the-onboarding/)

Episode 9. A garage owner with ten garages walks in to sign up, because he keeps losing the plan of his garages. Don promises "you will never lose anything again", takes the plan ("We'll take care of it.") and, with his eyes on Sofía, sets it in the shredder. Sofía falls for the Client ("Oh...", the pearl). Pam sees the shredder, raises a finger and lowers it. The robot celebrates the first customer by firing the strips from a confetti cannon, and stamps ONBOARDING COMPLETE on the glass. Pam scoops the strips off the floor: "Some shit, others scoop." His photograph now hangs in OUR FIRST CLIENT.

| File | Version | Notes |
|---|---|---|
| `uptimez_ob_anim_v19.mp4` (+ `_1080`, not committed) | **animation v19 (current, 18 Nov)** | 540 and native 1080, 76.8 s, −14.0 LUFS, −1.4 dBTP, 21/21 lines heard. The first joke at 1.7 s: the door slams, OUR FIRST CLIENT drops onto the Client and a ficus leaf onto his head; he signs up wearing it; Pam hangs it back, crooked. The plan is MY GARAGES (no. 7 ringed); the film loops (he has lost the strip again and comes back to the door). v12–v18 previews kept |
| `ob_cover_v1.png` | cover | THE FIRST CLIENT: him with the frame round his neck and the leaf, "Hi. I'd like to sign up." (`src/thumb_ob.py`) |
| `ob_v19_fixed_shots.png` | check | The Client's size and the dressed walls, v19 |
| `the-onboarding-script-v11.md` | script (current) | Line by line with the shot list, as of animation v11; v12–v19 changes are in the `ob_anim.py` notes; v1–v10 kept |
| `the-onboarding-concept-v1.md` … `v9.md` | concepts | The development |
| `ob_storyboard_v1..v3.png` (+ `_mute`), `ob_chain_v1..v2.png` | storyboard | The reaction chain and the mute versions |
| `ob_cast_v1..v6.png`, `ob_client_looks_v1..v3.png`, `ob_sofia_v1..v3.png`, `ob_set_v1..v5.png` (+ phone checks) | sheets | The Client's looks, Sofía's pearls, the set |
| `ob_animatic_v1..v2.mp4`, `ob_client_voices_v1.mp4`, `ob_sofia_oh_v1.mp4` | animatics, auditions | The Client's voice is B (`am_fenrir` −4 semitones); "Oh..." take A |
| `storyline-proposal-act-b.md` | proposal | Act B around the blueprint; STORYLINE v3.2 decides |

Built from `src/` (`*_ob`, `ob_anim.py`, `qa_ob*.py`); `./uptimez/build.sh ob`.

### First Search — [`first-search/`](first-search/)

Episode 10, **built: film v35 (21 Nov), 62.9 s.** The Client needs his blueprint by Friday. Don sells him a guarantee, takes his $999, posts the win, and has the robot paint the empty search result green. Sofía plasters the cracked portrait, Pam writes STUPID on the robot's back and tapes the plan, Mom scrubs the bump off Don's head with a licked thumb. On Friday the plan is shredded strips; "See you in court." On Monday the portrait is whole again.

| File | Notes |
|---|---|
| `first-search-film-v35.md` | **Current.** The film as built: every shot with its time and line, the running props, the hand-off to episode 11, the version history |
| `fs_film35_540.mp4` | **Film v35**, 540 (the 1080 is rebuilt, not committed). 62.9 s, −15.2 LUFS, peak −2.2 dBFS, the last frame leads into frame 0 (only the calendar differs: MON 1 / MON 8) |
| `fs_timing_film3..35.json` | Each film's shot timing (QA and Whisper read it) |
| `first-search-script-v10.md` | The production script the film started from; the film grew past it (the threat and the court, the post, the lipstick, the flashback, the huddle). Scripts v1–v9 kept |
| `first-search-concept-v1..v6.md`, `first-search-premise-v1..v3.md` | Kept |
| `fs_shot_design_v1.md`, `fs_shot_list_v2.md`, `cold_test_v11/`, `cold_test_v12/` | Board-stage staging and cold tests |

Built from `src/` (`fs_film35.py`, over `fs_film5.py` … `fs_film34.py`, all kept; `fs_storyboard.py`, `fs_set.py`, `fs_anim.py`, `fs_animatic.py`, voices in `src/fs_voices/film_v13`): `cd src && python3 fs_film35.py ../first-search 1080`. `FS_ONLY=C,U` renders only those shots.

### One Star — [`customer-success/`](customer-success/)

Episode 11, **master v13 (24 Nov), approved.** Thursday the 11th: every phone in the office buzzes with the Client's post, one star, "Paid $999. They lost my blueprint. My lawyer will call." The robot drafts a reply and Don approves it unread; Don reads it out: "Stupid human." 🤡. Don phones him: "Nine o'clock. Your office." Friday the 12th, Don presents a site plan "recovered" by the AI; the Client: "Is this a joke?" At the door Pam stops him with a raised palm; his own taped plan slides over the AI's, with a hole at bay 7. Pam: "Check your pocket." The 7 is in his own hand. Robot: "The result was obtained by a h-human." He saves her number: "finds things". Don: "Customer success." The post gets "UPDATE: Pam found it."; Pam answers it: "Some post. Others find."; Sofía: "Still one star." Don reads his phone and puffs up. The folder and file names keep the working title (`customer-success/`, `cs_*`).

| File | Notes |
|---|---|
| `one_star_master_v13_540.mp4`, `one_star_cover_v1.png` | **The master (24 Nov)** and its cover (`one-star-master-v13.md`); the film is rough cut v13 unchanged |
| `one_star_rough_v13_540.mp4` | **v13 (24 Nov)**, 540: 61.3 s, 16 lines, −15.7 LUFS, peak −2.4 dBFS; all 16 lines word-exact in the final mix. The 1080 file is rebuilt, not committed |
| `one_star_rough_v12_540.mp4` … `_v6_540.mp4` | v6–v12 of 23 Nov: phone texts inside the screen, layout B (Pam brings the plan), the series' one hand, shot list v19, dry voices, Don's clean "Stupid human." |
| `one-star-shot-list-v19.md` | **Current shot list:** size, foreground and hands for every shot (five close-ups, two over-the-shoulder shots, a foreground layer with parallax, the 7 insert 4.3s) |
| `one-star-gates-v1.md`, `one-star-gates-v19-r2.md` | The four new gates on v7 (GV, GD, GH fail) and on v19 (all pass) |
| `one-star-pam-lines-v1.md` | Pam's two spoken lines, approved before recording |
| `customer-success-script-v18.md` | The script ("Stupid human." 🤡, scene 4 before layout B); v14–v17 kept |
| `one-star-layout-v1.md`, `-v2.md`, `cs_layout_v*_scene3..6.png` | The layout pass: every scene laid out before it was animated |
| `cs_motion_test_v8.md`, `cs_cold_test_film_v1.md`, `-v2.md` | Motion tests and the earlier cold tests. Cold tests of v8 and v11 (two fresh viewers each): 5 of 5 beats |

Built from `src/`: `cs_scene1.py` … `cs_scene6.py`, `cs_film.py` (the mix), `cs_hands.py` (hand states), `cs_v19.py` (shot list v19), `cs_props.py`, `cs_frame.py`, `cs_sfx.py`, `cs_cal.py`; voices in `src/cs_voices/film_v9`. Each film version has a driver that switches its changes on (`cs_film_v7.py` … `cs_film_v13.py`; earlier versions draw as before). To rebuild v13 at 1080:

```bash
cd uptimez/src
python3 cs_film_v8.py ../customer-success 1 2 6
python3 cs_film_v9.py ../customer-success 4
python3 cs_film_v12.py ../customer-success 3 5
python3 cs_film_v13.py ../customer-success     # the mix and the film
python3 gates_os.py collect && python3 gates_os.py depth && python3 gates_os.py report   # with V19=1 for v19
```

**Left as is:** one note from the last cold test (who dials whom in the call).

### Daddy's Home — [`daddys-home/`](daddys-home/)

Episode 12, **animation v7 (23 Nov), 540; in the fix pass.** The one-star post goes viral and Don's father sees it: a nightclub kingpin and the company's majority investor, coming today at five, his people first. The office mistakes the coffee-machine repairman for Father's man and shows him everything; then the real Father walks in, and the robot looks at the chair. Frame 0 is Don in the gold CEO throne ($49,999 price tag), his phone ringing DAD; the loop ends on the same call.

| File | Notes |
|---|---|
| `daddys_home_anim_v7.mp4`, `_v7_loop.mp4` | **v7**, 540: 96.8 s, all eight scenes, speech bubbles in the Best Candidate style (`src/dh_say.py`), "Stupid human." 🤡 on Father's phone |
| `daddys-home-script-v2.md` | **Current script**, generated from the eight scene sheets (97.2 s, 37 lines) |
| `daddys-home-fix-plan-v1.md`, `daddys-home-bubble-lessons-v1.md` | The fix plan (two fix rounds, cold viewers, one more round; the trim to 95 s, music and 1080 come after it) and the 25 bubble rules |
| `daddys-home-concept-v1..v3.md`, `-plan-v1.md`, `-shot-list-v1.md`, `-spoken-lines-v1..v4.md` | Concept, plan, shot list, approved lines |

Built from `src/` (`dh_scenes.py`, `dh_anim1.py` … `dh_anim8.py`, `dh_say.py`, `dh_props.py`, `dh_film_v7.py`; voices in `src/dh_voices/film_v1`): `cd src && python3 dh_film_v7.py 1` … `8`, then `python3 dh_film_v7.py join`. **Still open:** the fix plan from cold viewers on, music, the 1080 master; Don's rig hands are not yet the series hand.

### The Offer — [`the-offer/`](the-offer/)

Episode 13, *Civil War* 1 of 5, **rough cut v30 (24 Nov), 540.** Father comes to the Client's garage to make him take down the post. Everything he brings to frighten him, the Client turns into garage work, until Father asks how he would run Don's company. "Without him." The Client's terms are Pam. Back at the office, the robot reads the new meeting out loud: AGENDA: WITHOUT HIM.

| File | Notes |
|---|---|
| `of_roughcut_v30_540.mp4` | **v30**: 64.5 s, 15 lines, sound v15 (the office bed, the lamp gag's tick, the garage theme back at the pin); G5 and the hand gate pass |
| `the-offer-script-v6.md` | **Current script**, generated from `src/of_scenes.py` (do not edit by hand); v1–v5 kept |
| `the-offer-set-v2.md`, `of_hands_v*_sheet.png` | The garage set; the hand sheets the series hand grew from |

Built from `src/` (`of_scenes.py`, `of_set.py`, `of_cast.py`, `client_of.py`). **Still open:** the master and the cover.

### Pick a Side — [`pick-a-side/`](pick-a-side/)

Episode 14, *Civil War* 2 of 5, **board and motion tests (23 Nov); not animated yet.** A secret loyalty meeting: Don tapes a line across the office floor, DON on the tape. The robot fights him over the blinds (the 0:01 joke), Father learns of it from a team photo post (#TeamDon), and the loop ends with Sofía on Father's side. Don, alone in front: "Everyone's with me." Pam: "Some draw lines. Others cross them."

| File | Notes |
|---|---|
| `pick-a-side-script-v7.md` | **Current script** (about 61 s), with the blocking of 1.1–1.3; v1–v6 kept |
| `pick-a-side-spoken-lines-v4.md`, `ps_voices_v2.mp4` | The 19 approved lines and their recorded voices |
| `pick-a-side-concept-v3.2.md`, `pick-a-side-plan-v1.md` | The approved concept and the production plan |
| `ps_motion_A/B/C_v*.mp4`, `ps_hands_v1.png` | Motion tests; the series hand (`src/hands_ps.py`) was first drawn here |

Built from `src/ps_scenes.py`. **Still open:** animation (waits for episode 12's fix plan).

### Office Noir: Seven Lives — [`office-noir-4/`](office-noir-4/)

Office Noir 4, Pam's dream (a Valentine's special), **first moving rough v1 (24 Nov).** Pam-Cat is the noir hero who sees everything and does everything right, and keeps trying to be noticed: not the woman she saves, not the cop who runs her over, not the casino with her name in lights. She wakes at her desk, and the only thanks she gets is for coffee.

| File | Notes |
|---|---|
| `on4_rough_v1.mp4` | **Rough v1**: the animatic with the four voice takes, 68.9 s |
| `office-noir-4-script-v16.md` | **Current script**, generated from `src/on4_scenes.py`; board v1–v9 changes listed in it |
| `office-noir-4-concept-v2.md`, `on4_coldtest_*.md`, `on4_motiontest_v*.md` | The concept and the cold and motion tests of the board |

### Happy Compliance (Christmas special) — [`happy-compliance/`](happy-compliance/)

Christmas Eve at the office. DON walks in mid-shave in an open bathrobe: "Sorry. Getting ready for the ball." SOFÍA (glamorous nurse) and PAM (a five-minute home-made superhero: bath-towel cape, cardboard mask, paper "P"): "Eww." Don's eyes drop to the two red ornaments in Sofía's hands: "Nice balls. I've got two for you." The office robot, now promoted to HR and in a Santa hat, rolls in: "Inappropriate balls detected." It points at Don, rolls straight past him, and censors every ornament on the tree, then the two in Sofía's hands. "Violation resolved." Don gives a relieved thumbs-up. Sofía hands Pam a censored ornament: "Get him." The mask goes on: "Human in the loop." Sofía, sweetly: "Merry Christmas, Don." THUD. "Happy compliance!" A bar falls off, the alarm starts again. The joke: AI governance protects the company from the tree, not from the boss.

| File | Version | Notes |
|---|---|---|
| `uptimez_xmas_anim_v8.mp4` | release v8 (superseded by v9), 540 | 32.9 s, −16.0 LUFS, −4.5 dBTP, the last frame is frame 0. `xmas_anim8.py` over v7 (kept): no "Eww." bubbles or emoji (voices only); a fir garland over the door with the bauble hanging from it; clean colours (no brown vignette or warm glows; encoded BT.709 properly); Don at his true size in the robot's shot (v7 shrank him to 0.62 and made the robot a giant; the shot is widened instead); he lands on the THUD before the robot's "Happy compliance!"; after the alarm he gets up dazed and shuffles off towards the door, and the tail shows him back in the doorway (frame 0). Sound `sound_xmas8.py` (v2's mix rebuilt without its off-screen THUD and the razor slide). |
| `uptimez_xmas_anim_v9.mp4` | release v9 (superseded by v10), 540 | 32.9 s, −16.0 LUFS, −4.9 dBTP, the last frame is frame 0. `xmas_anim9.py` over v8 (kept): the green striped close-up of the bar slipping (30.6 s) is gone. Two cold viewers and the author could not place it. The robot's shot instead pushes in on the gold bauble beside its face; the bar slips off it, drops in front of everything onto Don lying on the floor, the robot's eyes go red, and the camera eases back out before he gets up. Two fresh cold viewers (mute) both read the robot finally turning on Don, the cause in the same frame. Same timing and mix as v8. |
| `uptimez_xmas_anim_v10.mp4` | release v10 (superseded by v11), 540 | 32.9 s, −16.0 LUFS, −4.9 dBTP, the last frame is frame 0. `xmas_anim10.py` over v9 (kept): the bar that drops onto Don rides on his chest as he gets up, peels off and sails out left, and the cold open's bar comes in from the right (one leftward flight), so the bar has an origin. In shot 7 HR's pointing arm becomes a scanner: a red beam sweeps Don twice, then a green tick (checked, fine). Pam's throw gets a wind-up (arm up and back, held), a smear and an arc trail. The robot's talking mouth is a round O. Don, Sofía and Pam breathe (1 %, ten breaths per loop; Don is still in shot 1, where his foam is an overlay). Sound `sound_xmas10.py` (v8's mix + the scan hum and tick, the slap, the whoosh off). Cold viewers Q and R: 5/5 each, and the scan was Q's screenshot. |
| `uptimez_xmas_anim_v11.mp4` | **release v11 (final, 18 Nov)**, 540 | 32.9 s, −16.0 LUFS, −4.9 dBTP, the last frame is frame 0; v10's sound. `xmas_anim11.py` over v10 (kept): life in the background on v10's clock (held at 0 in the tail). Fairy lights twinkle along the tree's tinsel (never over an ornament), the bunting flags sway in a ripple, the robot's pompom bobs (idle, wobbling as it rolls, a damped bounce when it stops), Sofía's hair and earrings sway, the robot's eager face blinks now and then. Fixes v10's breathing for Don and Pam: xmas_anim swaps their drawing functions per frame and called the originals it had captured, so in v10 only Sofía breathed. `./build.sh xmas_final` |
| `uptimez_xmas_anim_v7.mp4` | v7, 540 | 31.0 s, −16.0 LUFS, −1.5 dBTP, the last frame is frame 0. `xmas_anim7.py` over v6 (kept): the two "Eww." bubbles sit between the heads with short tails, their emoji as badges outside the boxes (the long tails crossed the emoji); a new 0.9 s beat after "Merry Christmas, Don." (the throw, the bauble hits his head with a BONK and stars, he tips back like a plank); in the robot's shot he lands flat on his back in front of it on the THUD, stars circling, the bauble rolling away; the robot never looks (the feet-in-the-air read as "pretzels on the floor"). Sound `sound_xmas7.py`. `./build.sh xmas_final` |
| `uptimez_xmas_anim_v6.mp4` | v6, 540 | 30.1 s, −16.0 LUFS, −1.5 dBTP, Whisper 10/10 lines, the last frame is frame 0. `xmas_anim6.py` (over v5, v4, v3; each kept): **0:01** a CENSORED bar flies at Don's open robe, stops, "looks", and turns away onto a bauble on the door frame (THUNK at 0.68 s): it censors the ornament, not the boss; his shaving foam a big white cloud; the PARTY sign whole above him; **the ending made visible** (Pam's gloved hand throws the censored bauble, it hits Don at "Merry Christmas, Don.", his legs come up at the THUD, the bar slips off a bauble in close-up before the alarm); **the loop**: after the alarm, back to the doorway, bauble bare, exactly frame 0. A light camera (creeps on Don's lines, a push on "Human in the loop."). Sound `sound_xmas5.py`. Two pairs of cold mute viewers: v4 3/5 beats, v5 5/5. `./build.sh xmas_final`; the 1080 master is rebuilt, not committed |
| `uptimez_xmas_anim_v5.mp4`, `_v4.mp4`, `_v3.mp4` | v5, v4, v3, 540 | v3: the cold open and the loop; v4: PARTY above Don, his legs at the THUD, the light camera; v5: the cold viewers' fixes (the bar's pause, the foam, Pam's throw, the bar slipping off). `xmas_v3_open_check.png`, `xmas_v6_check.png` |
| `uptimez_xmas_anim_v2_1080.mp4` | release v2 (tails fixed 17 Nov) | **1080×1920**. Pam v4 (canon head, a fond side-eye, "over" for "Human in the loop.", the mask up, then a visible drop over her readers), a two-row banner, no cropped signs (shown whole or not at all), the razor drawn without fingers, Sofía's badge raised, curved tails ending beside the mouth actually drawn in each frame | **17 Nov (`xmas_anim2` v4):** every box placed clear of the speaker's head, hat, cap or mask, with the tail running outside the face to beside the mouth; "Eww." as two bubbles a beat apart with their own emoticons (Sofía's eye-roll, Pam's queasy green); "Merry Christmas, Don." beside him with its tail to the left edge; the PARTY sign also kept out of shots 1 and 4. Check grid: `xmas_tails_v4_check.png` |
| `uptimez_xmas_anim_v2.mp4` | release v2, 540 | Same, 540×960 |
| `xmas_thumbnail_v2.png`, `xmas_storyboard_sheet_v2.png`, `xmas_storyboard_silent_v2.mp4`, `xmas_set_sheet_v2.png`, `xmas_motion_test_b_v2.mp4`, `sofia_xmas_v1_vs_v2.png` | v2 extras | Cover v2: the badge fix only. `./uptimez/build.sh xmas2` |
| `uptimez_xmas_anim_v1_1080.mp4` | release v1 | **1080×1920**, 28.9 s, −16 LUFS. Lip-sync on all ten lines (Don, Sofía, Pam, the robot's screen), blinks, camera punches (DETECTED push, slap jolts, THUD shake), the robot's spinning wheel, Don's anticipation dip, a bigger razor payoff, warm light glow and vignette |
| `uptimez_xmas_anim_v1.mp4` | release, 540 rough | Same animation, 540×960, for review |
| `uptimez_xmas_animatic_v1.mp4` | animatic v1 | Storyboard v2 with the mix: Don `am_onyx`, Sofía `af_bella`, Pam `bf_emma`, robot B (`am_echo`, last episode's shout); an original sleigh-bell bed that stops dead on "Nice balls" |
| `xmas_pam_auditions.mp4` | | Pam's first voice: A `bf_emma` (picked), B `bf_alice`, C `bf_isabella` |
| `xmas_storyboard_silent_v2.mp4`, `_sheet_v2.png` | **storyboard v2** | Razor at Don's jaw (both eyes visible), his eyes drop and we cut to his point of view, "Eww." / "Get him." / "Merry Christmas, Don." added, HR fits its badge, bubbles sized from their text with pop-in and a shaking shout, THUD burst |
| `xmas_storyboard_silent_v1.mp4`, `_sheet_v1.png` | storyboard v1 | 11 shots, 27.5 s |
| `xmas_motion_test_a.mp4`, `_b_v1.mp4`, `_b_v2.mp4`, `xmas_motion_tests_contact.png` | motion tests | A: the censoring (three slaps, the flung cascade, Sofía's two). B: the handoff (v2: a close push-in, the bigger ornament) and the mask snap |
| `xmas_set_sheet_v2.png` (v1 kept) | set | The Day One office wall, decorated; 9:16 frames for the key shots; v2 bigger censor bars and the robot's v3 face |
| `sofia_xmas_earring_options.png`, `sofia_xmas_v1_vs_v2.png` | | Sofía's earring/braid options (B picked) and the figure change |
| `xmas_thumbnail.png`, `xmas_thumbnail_grid_crop.png` | cover | The censored tree, the smug robot, furious Sofía; its own line as the title |

Character sheets are in [`characters/`](characters/) (`*-xmas-*`, `uptimez-robot-hr-*`). Built from `src/`: `sofia_xmas.py`, `don_xmas.py`, `pam_xmas.py`, `santa_robot.py` (costumes on the existing characters; earlier versions kept as `_v1`…), `xmas_set.py` (set, tree, ornaments, censor bars), `xmas_test_a.py` / `xmas_test_b.py`, `xmas_sb.py` / `xmas_sb_v2.py`, `xmas_bubbles.py` (fitted, popping bubbles, shout, burst), `sound_xmas.py` (audition, voices, effects, music, mix), `xmas_visemes.py`, `xmas_anim.py` (the polish, applied through hooks for this render only), `thumb_xmas.py`. `./build.sh xmas` rebuilds the mix, both renders and the cover (needs the Kokoro model in `src/models` or `KOKORO_DIR`).

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

## Production rules

How every episode is made now; the details live in [`CLAUDE.md`](CLAUDE.md), [`series/production-process.md`](series/production-process.md) and [`../docs/lessons.md`](../docs/lessons.md).

- **Gates before each stage** (G0 series check … G6 audit triage) and four measured gates from 23 Nov ([`gates-v2-plan.md`](gates-v2-plan.md), `src/gates_os.py`): **GV** shot variety (sizes measured from the rendered faces), **GP** proportions, **GD** depth and volume (a foreground layer, no line-ups), **GH** hands. Each check fails on a planted fault before it is trusted.
- **One hand for the whole cast:** `kit.HAND` with `src/hands_ps.py` (quiet, fist, point, palm, grab, grips); the robot keeps its own grippers.
- **Voices are dry:** no room reverb on dialogue; an effect only on a character seen as its source. Every line is checked word by word inside the final mix.
- **One episode, one branch;** 1080 renders are rebuilt, not committed; earlier versions are pinned and new behaviour is opt-in.

## Build

```bash
pip install pycairo numpy soundfile kokoro-onnx
# Kokoro model: kokoro-v1.0.int8.onnx + voices-v1.0.bin from the
# thewh1teagle/kokoro-onnx GitHub release, in src/models/ or $KOKORO_DIR
./uptimez/build.sh pt43      # one episode (keys: s3 s1 s3b s3c s1v2 pta ptb pt4 pt42 pt43 s131a s131b)
./uptimez/build.sh s136      # Saved to Cloud release at 1080x1920 (s136n = without the tag)
./uptimez/build.sh dlx       # Downloads Expedition final at 1080x1920 (dlx_tag = with the promptanatomy.app card)
./uptimez/build.sh day1      # How Sofía Survived Day One, loop v3 at 1080x1920 (day1_thumb = cover)
./uptimez/build.sh iwry      # I Will Replace You, animatic v3 at 540x960 (iwry_thumb = cover)
./uptimez/build.sh bc        # The Best Candidate, animation v3 at 540x960 and 1080x1920 (its bubble checks run first and can stop it)
./uptimez/build.sh all       # every episode
./uptimez/build.sh sheets    # logo files + character sheets
```

Stills for checking: `cd uptimez/src && python3 engine.py pt43 0 60 240` writes `pt43_000.png` etc.

How it works: `engine.py` draws each frame with pycairo (paper-cutout kit in `kit.py`, 12 fps boil, slow push-in per panel) and pipes raw frames to ffmpeg; each `sound*.py` voices the lines with Kokoro, synthesizes music and effects in NumPy and writes `<key>_mix.wav`. Newer episodes wrap older modules at runtime (`pt42` wraps `pt4`, `pt43` wraps `pt42` and the kit) instead of editing them, so every earlier cut still rebuilds unchanged. Rebuilding `pt43` and `ptb` from this folder gave frames and loudness identical to the committed files.

Kokoro's model licence hasn't been confirmed for commercial use.
