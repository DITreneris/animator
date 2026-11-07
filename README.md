# animator

Code-generated vertical videos (9:16, 1080×1920) for TikTok, Reels and Shorts: memes about AI and vibe coding, turned into short animated loops. By [promptanatomy.app](https://promptanatomy.app).

Every frame is drawn from code and every sound is synthesized, so a video can be rebuilt exactly from this repo, with no stock footage, samples or AI video generators.

## Videos

| Folder | Video | Length | Status |
|---|---|---|---|
| [`payday-slam/`](payday-slam/) | **Payday Slam**: who gets paid? Employee, Freelancer, Founder… and the vibe coder who pays to work | 17 s | ✅ Source + render |
| `the-list/` | **The List**: the same joke on one screen, with recorded voices | 17 s | ⏳ Not added yet |
| `uptime-inc/` | **Uptime Inc.**: AI office sitcom with MAX, RUSH and PAM (*Prompt Telephone* v04.1, 6 shots) | 15 s | ⏳ Not added yet |
| `choose-career/` | **Choose Your Career**: sound effects added to the four-panel pay GIF | ~4 panels | ⏳ Not added yet |
| `chat-gifs/` | Chat GIFs re-timed to 13–15 s, reframed to 9:16 and given sound | 13–15 s | ⏳ Not added yet |

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

## How a video is built

1. **`plan.json`**: frame-accurate timing for every beat (30 fps), so visuals and sounds share one clock.
2. **`render.py`**: draws each frame with Pillow, then pipes the scenes to ffmpeg (H.264, BT.709, yuv420p).
3. **`audio.py`**: synthesizes the music and sound effects with NumPy/SciPy, cued to the same frame numbers.
4. **`build.sh`**: renders the scenes in parallel, normalizes the audio to about −14 LUFS and muxes the final MP4.

## Fonts and licensing

- `fonts/Anton-Regular.ttf` is the Anton typeface, © The Anton Project Authors, under the SIL Open Font License 1.1 (`fonts/Anton-OFL.txt`).
- No license has been chosen yet for the code and videos, so all rights are reserved by default.
