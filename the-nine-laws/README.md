# The Nine Laws

SeaShell is a Super AI, depicted as a hermit crab. It speaks as its own
character, voiced from a recording the user makes themself (plus ElevenLabs
reads for newer lines), and carries a SeaShell-owned three-note motif as its
sonic signature rather than borrowed music. "The Nine Laws" is its first
video; the series continues from there with each episode reusing SeaShell's
established sign-off card/line and sonic identity for continuity.

All soundtracks here are synthesized from scratch in Python (numpy/scipy —
no licensed music or sound libraries) and muxed onto the original silent
video with the video stream untouched.

Unlike most folders in this repo, these can't be rebuilt from the repo
alone: the picture is a supplied video, and the voice clips each
`score.py` loads (`*_trim.wav`, `*_oct.wav`, `c_*.wav`, `w_*.wav`), and Part 3's laugh
clips, are not committed. Each folder holds the scoring script and the final render.

| Folder | Video | Length | Loudness |
|---|---|---|---|
| [`v1/`](v1/) | `the_nine_laws_sound_v2.mp4` (built by `score.py`, the v2 score) | 45.0 s | -12.9 LUFS |
| [`v2-almost-done/`](v2-almost-done/) | `almost_done_sound.mp4` | 21.3 s | -13.4 LUFS |
| [`v3-the-bug-trains-you/`](v3-the-bug-trains-you/) | `the_bug_trains_you_sound.mp4` | 30.0 s | -15.0 LUFS (flat gain + peak limiter, so the laughs aren't flattened) |

## Episodes

### The Nine Laws — [`v1/`](v1/)
The opening video: establishes SeaShell's sonic identity and the closing
"Bugs are remaining" sign-off line, reused in later episodes.

### Part 2, "Almost Done" — [`v2-almost-done/`](v2-almost-done/)
Reuses the Nine Laws sign-off take unchanged. Adds progressive chime decay,
a crack/snap and tape-rip for the glitch beats, and a reverse fill-tone
scored under the backward-walking bug to literalize "undoing progress."

### Part 3, "The Bug Trains You" — [`v3-the-bug-trains-you/`](v3-the-bug-trains-you/)
A David Lynch *Rabbits*-style treatment: a continuous tide (standing in for
Lynch's rain) under the whole episode, a single distant foghorn (standing in
for the train whistle), a true half-second of silence where "Act 2" is
skipped, and a synthetic, deliberately artificial laugh track that fires at
the *least* funny moments rather than the two beats that actually resemble
jokes. Six new SeaShell lines (ElevenLabs reads, processed through the same
dry + octave-down + reverb chain as every other episode): "Reward.", "Good
developer.", "Still on call.", "Permission to rest.", "Who trained whom?",
and "Thus spoke SeaShell." to close; the episode ends on that line.

The laughs are recorded ElevenLabs sound effects (the first synthesized
versions weren't recognizable as people). `score.py` loads them from a
`laughs/` folder that, like the voice clips, isn't committed. Checks run
on the final render: speech recognition hears all six lines correctly in
the mix, and an AudioSet classifier (CED-mini) scores all three laugh spots
as laughter (0.32 / 0.53 / 0.72). `finish.sh` sets the loudness and muxes.
