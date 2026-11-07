# UptimeZ Inc.

**99.9% uptime. 0% findability.**

An AI office sitcom: short vertical cartoons about ridiculous people using AI, posted as if from the corporate account of a polished SaaS company. The brand is the straight man; the people inside it are the joke. Formerly *Uptime Inc.*

All videos here are **540×960 animatics** (30 fps, 15 s, 450 frames): rough cuts for audience tests, not final 1080×1920 releases.

## Cast

| Badge | Role | In one line | Voice (Kokoro) |
|---|---|---|---|
| **DON** | CEO | Shouts in capitals, understands nothing, softens only when it's about him. Bald. | `am_fenrir` |
| **PAM** | Project manager | "Improves" every instruction on the way down | `bf_emma` |
| **RUSH** | Sales | Panics first, types before he reads | `am_adam` |
| **MAX** | Developer | The only sensible one; asks the fair question, watches it burn | `am_michael` |
| **LAPTOP** | The AI | Two dots and a flat line. Does exactly what it's told and gets overruled | none |
| **CACHE** | Office cat | Always asleep on whatever the humans threw away | none |

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
./uptimez/build.sh pt43      # one episode (keys: s3 s1 s3b s3c s1v2 pta ptb pt4 pt42 pt43)
./uptimez/build.sh all       # every episode
./uptimez/build.sh sheets    # logo files + character sheets
```

Stills for checking: `cd uptimez/src && python3 engine.py pt43 0 60 240` writes `pt43_000.png` etc.

How it works: `engine.py` draws each frame with pycairo (paper-cutout kit in `kit.py`, 12 fps boil, slow push-in per panel) and pipes raw frames to ffmpeg; each `sound*.py` voices the lines with Kokoro, synthesizes music and effects in NumPy and writes `<key>_mix.wav`. Newer episodes wrap older modules at runtime (`pt42` wraps `pt4`, `pt43` wraps `pt42` and the kit) instead of editing them, so every earlier cut still rebuilds unchanged. Rebuilding `pt43` and `ptb` from this folder gave frames and loudness identical to the committed files.

Kokoro's model licence hasn't been confirmed for commercial use.
