# Chat GIFs

Two fake-chat GIFs (about 20 s each) re-timed to 13–15 s, reframed to 9:16 (1080×1920, 30 fps), cleaned up for sharper text and given synthesized sound.

| Video | Source | Length | Sound |
|---|---|---|---|
| `emma_blocked.mp4` | `src/emma_blocked.gif` (iMessage, 19.9 s) | 13.2 s | Key taps, send whoosh, receive pops, typing-dot ticks, double "bonk" on *Emma blocked you.* |
| `babe_voice_agent.mp4` | `src/babe_voice_agent.gif` (Messenger, 19.9 s) | 14.9 s | 116 BPM plucked hook and beat, chat pops and swooshes, tape-stop on *Already training my voice agent.*, robot blip, riser and ticks under her endless typing, dun-dun-DUN ending |

## Story beats

**Emma Blocked**: "You cheated on me!" → "ChatGPT said I was wrong." → "And what did you do about it?" → "Asked Claude." → "You did WHAT?!" → "Anyway… what's your Gemini password?" → *Emma blocked you.*

**Babe / Voice Agent**: "Where are you?" → "Beers with the boys" → "Don't get drunk! You promised to read to the baby tonight." → "I'll play a bedtime story from my phone." → "He needs YOUR voice!" → "Already training my voice agent." → her "…" never ends.

## Build

```bash
./build.sh
```

Each `<name>.py` unpacks its GIF into `build/<name>/frames/`, writes an ffmpeg concat list with the new per-frame durations, and synthesizes `audio.wav` cued to the same frame start times. `build.sh` then normalizes the audio, crops and scales to 1080 wide, applies the clean-up filter, pads to 1080×1920 and muxes.

Output (measured): `emma_blocked.mp4` −15.3 LUFS, peak −2.1 dBFS; `babe_voice_agent.mp4` −14.8 LUFS, peak −1.8 dBFS.

## Re-timing rules used

- Typing steps 100–140 ms → 65 ms; typing dots → 80–100 ms; 70 ms send/arrive frames unchanged.
- Reading holds about 3 words per second, at least about 0.9 s.
- Punchline and the pause before the reveal keep 1–1.5 s; end card at most 2.6 s.
- The last hold is long enough for the closing sting, and the audio buffer is exactly the video length.

## Files

- `src/`: the original GIFs
- `common.py`: GIF unpacking, concat list, envelope and WAV helpers
- `emma_blocked.py`, `babe_voice_agent.py`: frame timings and soundtrack for each clip
- `build.sh`: loudness normalization, 9:16 reframe, clean-up filter and encode

## Known issues

- The sources are 720 px, 256-colour GIFs, so text sharpness is capped. Exporting future chat animations at 1080 px wide as MP4 or PNG frames would look much crisper.
- `emma_blocked` has no promptanatomy.app mark; the Messenger source carries it in the original frame.
- The mix balance and comedy timing have been checked by measurement only; they still need a listen on a phone.
