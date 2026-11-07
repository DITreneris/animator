# Choose Your Career

The four-panel *Choose Your Career* GIF (Employee, Freelancer, Founder, Vibe Coder) with synthesized sound effects. The picture and panel timing are unchanged from the GIF; the sound tells each panel's joke.

| Video | Size | Length | Loudness (measured) |
|---|---|---|---|
| `choose_career_reveal_sfx.mp4` | 900×1066 (source frame plus one black row for an even height) | 10.2 s, 306 frames at 30 fps | −14.4 LUFS, true peak −2.2 dBFS |
| `choose_career_reveal_9x16.mp4` | 1080×1920, meme scaled to 1080×1278 and raised 100 px above centre | 10.2 s, 306 frames at 30 fps | −14.4 LUFS, true peak −2.2 dBFS |

## Sound design

Every panel lands with a low thud and a crack. The four amounts in each row pan slightly left to right, following their place on screen.

| Panel (appears at) | Sound | Joke |
|---|---|---|
| **Employee** (0.0 s) | Four identical rubber stamps, evenly spaced | Same pay, same rhythm |
| **Freelancer** (1.7 s) | Four coin pings at uneven intervals; bigger amounts ring higher and louder | Unpredictable income |
| **Founder** (3.7 s) | Three hollow knocks, then a heavy hit, a register ding and a coin shower on $600k | Nothing, nothing, nothing, then the payout |
| **Vibe Coder** (6.0 s) | Four error buzzes falling in pitch, two party-horn toots, then a long deflating slide | Celebrating while the money drains away |

All sounds are synthesized with NumPy/SciPy: no samples, no music.

## Build

```bash
./build.sh
```

`sfx.py` unpacks the GIF into `build/frames/`, reads each frame's duration to get the panel start times, writes the concat list and synthesizes `build/audio.wav` (48 kHz stereo) cued to those times. Cue times are written to `build/events.json`. `build.sh` encodes the audio to AAC and renders both cuts (H.264, BT.709, yuv420p, `+faststart`).

## Files

- `src/choose_career_reveal.gif`: the original 900×1065 GIF (4 frames: 1.7, 2.0, 2.3, 4.2 s)
- `sfx.py`: frame unpacking, timing and soundtrack
- `build.sh`: encodes both cuts

## Known issues

- The mix and comedy timing were checked by measurement only (cue onsets, loudness, peak); they still need a listen on a phone, especially the party horn's level.
- In the 9:16 cut, the app's like and comment buttons may still overlap the right edge of the lower panels, including part of the Vibe Coder's raised fist. The labels and amounts on the left stay clear.
- The 9:16 cut was added with this repo commit and has not been reviewed on a phone yet.
