# animator

Code-generated vertical videos (9:16, 1080×1920) for TikTok, Reels and Shorts: memes about AI and vibe coding, turned into short animated loops. By [promptanatomy.app](https://promptanatomy.app).

Every frame is drawn from code and every sound is synthesized, so a video can be rebuilt exactly from this repo, with no stock footage, samples or AI video generators.

## Videos

| Folder | Video | Length | Status |
|---|---|---|---|
| [`payday-slam/`](payday-slam/) | **Payday Slam**: who gets paid? Employee, Freelancer, Founder… and the vibe coder who pays to work | 17 s | ✅ Source + render |
| [`the-list/`](the-list/) | **The List**: the same joke on one screen, doodle style, with recorded voices | 17 s | ✅ Source + render |
| `uptime-inc/` | **Uptime Inc.**: AI office sitcom with MAX, RUSH and PAM (*Prompt Telephone* v04.1, 6 shots) | 15 s | ⏳ Not added yet |
| [`choose-career/`](choose-career/) | **Choose Your Career**: sound effects added to the four-panel pay GIF, plus a 9:16 cut | 10 s | ✅ Source + render |
| [`says-here-boss/`](says-here-boss/) | **Says Here You Were Our Boss**: 2024 prompt engineer → 2027 interviewed by his own agents (v1, v2 with voices) | 15–17 s | ✅ Source + render |
| [`thank-you/`](thank-you/) | **He Always Said Thank You**: the robots spare him… except for the toaster | 14.5 s | ✅ Source + render |
| [`make-it-better/`](make-it-better/) | **Make It Better**: the AI went on strike after version 47 (v1, v2 clearer opening) | 15 s | ✅ Source + render |
| [`just-for-now/`](just-for-now/) | **Just For Now**: a taped temporary fix holds up the whole company (test clips, rough, v2) | 7–28.5 s | ✅ Source + render |
| [`chat-gifs/`](chat-gifs/) | **Emma Blocked** and **Babe / Voice Agent**: chat GIFs re-timed, reframed to 9:16 and given synthesized sound | 13–15 s | ✅ Source + render |

The full history of the work, including concepts not yet built, is in [`docs/sessions.md`](docs/sessions.md).

## Quick start

Needs Python 3.10+, ffmpeg and a few Python packages:

```bash
pip install -r requirements.txt
./payday-slam/build.sh          # writes payday-slam/Payday_Slam.mp4
```

Check single frames before a full render:

```bash
python3 payday-slam/render.py check 0 228 420   # writes payday-slam/check/f000.jpg …
```

## Canvas-drawn doodle episode

`the-list/` is drawn on an HTML canvas in headless Chromium (Playwright) instead of Pillow or cairo, at 12 poses per second. Build it with `./the-list/build.sh`; it needs Node with `playwright` as well as the Python packages.

## Cairo-drawn episodes

`says-here-boss/`, `thank-you/`, `make-it-better/` and `just-for-now/` share one cartoon style (the hoodie guy, white robots, the rewind effect) drawn with pycairo instead of Pillow. Each version folder has:

- `v.py`: the character and prop library as it stood for that version
- `render.py`: the scenes (`python3 render.py frames 0 120` for check frames, `render` for all scenes)
- `audio.py`: synthesized music and effects, mixed with the voice lines in `vo/`
- `voices.py`: optional, regenerates raw voice takes with Kokoro
- `build.sh`: full render and mux

## How a video is built

1. **`plan.json`**: frame-accurate timing for every beat (30 fps), so visuals and sounds share one clock.
2. **`render.py`**: draws each frame with Pillow, then pipes the scenes to ffmpeg (H.264, BT.709, yuv420p).
3. **`audio.py`**: synthesizes the music and sound effects with NumPy/SciPy, cued to the same frame numbers.
4. **`build.sh`**: renders the scenes in parallel, normalizes the audio to about −14 LUFS and muxes the final MP4.

## Fonts and licensing

- `fonts/LilitaOne-Regular.ttf` is the Lilita One typeface, © Google Inc. / the Lilita One authors, under the SIL Open Font License 1.1 (`fonts/LilitaOne-OFL.txt`). Used by the cairo-drawn episodes.
- The episodes with spoken lines use voices made with Kokoro (`kokoro-onnx`); the model's license hasn't been confirmed for commercial use.

- `fonts/PermanentMarker-Regular.ttf` is the Permanent Marker typeface, © 2010 Font Diner, Inc., under the Apache License 2.0 (`fonts/PermanentMarker-LICENSE.txt`). Used by *The List*.
- `fonts/Anton-Regular.ttf` is the Anton typeface, © The Anton Project Authors, under the SIL Open Font License 1.1 (`fonts/Anton-OFL.txt`).
- No license has been chosen yet for the code and videos, so all rights are reserved by default.
