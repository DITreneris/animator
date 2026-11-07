# Saved Locally (retired)

The first Uptime Inc. concept: an elevator-in-2077 sketch about SAVI, an assistant that "saved it locally". Testers didn't know what SAVI was, and the joke read as recognition rather than laughter, so the series moved on to *Where Files Live* and then *Prompt Telephone*.

Kept exactly as made, for reference:

| File | Version |
|---|---|
| `saved_locally_animatic_A.mp4`, `_B.mp4` | v1, two endings |
| `saved_locally_animatic_A_v2.mp4`, `_B_v2.mp4` | v2 |
| `uptime_inc_saved_locally_A_v3.mp4`, `_B_v3.mp4` | v3, with the Uptime Inc. badges |
| `uptime_inc_cast_card.png` | First cast card |

`src/` holds the scripts as they stood (`render_v1.py`, `render_v2.py`, `render.py` for v3, plus `timing.py`, `audio.py`, `voices.py`). They predate the shared kit and have no build script; `voices.py` reads the Kokoro model from `$KOKORO_DIR` (default `models/`).
