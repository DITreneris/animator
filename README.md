# animator

Code-generated vertical videos (9:16, 1080×1920) for TikTok, Reels and Shorts: memes about AI and vibe coding, turned into short animated loops. By [promptanatomy.app](https://promptanatomy.app).

Every frame is drawn from code and every sound is synthesized, so a video can be rebuilt exactly from this repo, with no stock footage, samples or AI video generators.

## Videos

| Folder | Video | Length | Status |
|---|---|---|---|
| [`payday-slam/`](payday-slam/) | **Payday Slam**: who gets paid? Employee, Freelancer, Founder… and the vibe coder who pays to work | 17 s | ✅ Source + render |
| [`payday-slot-machine/`](payday-slot-machine/) | **Payday Slot Machine**: each career's slot machine spins out its monthly pay, ending on "One prompt away from revenue." | 19 s | ✅ Source + render |
| [`the-list/`](the-list/) | **The List**: the same joke on one screen, doodle style, with recorded voices | 17 s | ✅ Source + render |
| [`uptimez/`](uptimez/) | **UptimeZ Inc.** (formerly Uptime Inc.): AI office sitcom with DON, PAM, RUSH and MAX. *Prompt Telephone* v03–v04.3, *Where Files Live* storyboards, retired *Saved Locally*, logo files and character sheets (540×960 animatics) | 15 s | ✅ Source + render |
| [`choose-career/`](choose-career/) | **Choose Your Career**: sound effects added to the four-panel pay GIF, plus a 9:16 cut | 10 s | ✅ Source + render |
| [`hoodyz/`](hoodyz/) | **ME + MY AI** (Hoodyz): Hoody, his robot MY AI, Eva, the cat and HARV. *Just For Now*, *Who's a Good Boy?*, *Learn to Code*, *Says Here You Were Our Boss*, *He Always Said Thank You*, *Make It Better*, *Make It Original*, *Perfect Date*, *Perfect Trip*; *Infinite Undo* shelved. See [`hoodyz/README.md`](hoodyz/README.md) | 7–28.5 s | ✅ Source + render |
| [`chat-gifs/`](chat-gifs/) | **Emma Blocked**, **Babe / Voice Agent** and **Claude / Backups**: chat GIFs re-timed, reframed to 9:16 and given synthesized sound | 12–15 s | ✅ Source + render |
| [`the-nine-laws/`](the-nine-laws/) | **The Nine Laws** (SeaShell, the hermit-crab Super AI): *The Nine Laws*, Part 2 *Almost Done*, Part 3 *The Bug Trains You* (a David Lynch *Rabbits*-style score). Synthesized soundtracks on supplied video | 21–45 s | 🔊 Sound source + render (picture and voice clips not in repo) |

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

`uptimez/` uses its own paper-cutout kit and a single `build.sh` for all its episodes; see [`uptimez/README.md`](uptimez/README.md).

The older Hoodyz episodes (`hoodyz/says-here-boss/`, `hoodyz/thank-you/`, `hoodyz/make-it-better/` and `hoodyz/just-for-now/`) share one cartoon style (the hoodie guy, white robots, the rewind effect) drawn with pycairo instead of Pillow. Each version folder has:

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
- `fonts/Inter-400.ttf`, `Inter-700.ttf`, `Inter-800.ttf` are the Inter typeface, © The Inter Project Authors, under the SIL Open Font License 1.1 (`fonts/Inter-OFL.txt`). Used by *UptimeZ Inc.* post cards and character sheets.
- `fonts/ArchivoBlack-Regular.ttf` is the Archivo Black typeface, © 2017 The Archivo Black Project Authors, under the SIL Open Font License 1.1 (`fonts/ArchivoBlack-OFL.txt`). Used by *Payday Slot Machine*.
- No license has been chosen yet for the code and videos, so all rights are reserved by default.
