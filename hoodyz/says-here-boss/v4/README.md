# Says Here You Were Our Boss: v4

20.1 s, 20 shots, 603 frames, 1080x1920, 30 fps. `says_here_v4.mp4`, cover `cover.png` (the 9.99 offer). Built by `build.sh`.
v3 is untouched; v4 imports its cast, sets and voice takes from `../v3`.

**Why v4.** v3 looped by matching two still frames (a held smile), opened on 0.67 s of silent smile, and 7 of its 19 shots
measured as frozen.

**The loop is now the joke.** After "About your experience..." HARV's antenna pulses, a NEW CHAT chip pops, and he picks the
same CV up again. The cut lands mid-lift on frame 0, where he reads it: "Says here you used to be our boss?" He has no memory
of the interview either. The CV's rise, the chime's tail, the paper rustle and the room tone run through the cut.

## What changed against v3
- **Hook:** frame 0 is HARV in Hoody's gold shades with the CV coming up; the line starts at 0.1 s.
- **Desk shots reframed close:** HARV fills the frame, the desk is a strip, the nameplate sits above the app's bottom zone.
- **Speech tails touch the speaker.** "About your experience..." is on HARV (v3 had it on Hoody); "Thank you, sir." sits low
  beside Hoody, out of the app's button column.
- **Dark room recomposed:** the TV up top, a big Hoody on the sofa with the JOBS laptop.
- **Cat close-up redrawn** on this desk, plain wall behind.
- **Animation:** HARV's antenna glows with his voice and his head tilts per phrase (his mouth stays flat); the panel turns to
  him; Hoody's mouth moves on "...yes."; cut pops; the forced smile snaps back with a squash.
- **From two cold viewers' shared misreads:** a thick yoink arm with a hand, the reach as an arm from his shoulder, HARV's
  hand sliding the offer letter in, greyer tears, an eyes-only slit, bigger shades on his head in 2024-26, no chip at frame 0.

## Measured (21 Nov 2026)
| Check | Result |
|---|---|
| QA gate (`../../qa.py`) | pass: all six lines recognised in the mix, -14.8 LUFS, true peak -1.9 dBTP |
| Loop, last frame vs frame 0 | mean difference 0.84 / 255, the CV mid-lift in both |
| Sound across the cut | -22 dB before, -28 dB after (v3: a 12 dB jump) |
| Motion (`hoodyz/motion.py`) | 2 of 20 shots under 0.8, both deliberate: the silence after the shout, the cat |
| Cold-viewer mute test (2 viewers, rough 1, no bubbles) | 5 of 5 beats each; both read NEW CHAT as "he wipes it and restarts" |

## Not measured
Whether it is funny, the voice timing and the mix: Tomas judges those with sound on. The cold-viewer test ran on rough 1,
before the two polish passes.

## Open ideas (not done)
A 1.5 s text hook ("POV: the AI you trained interviews you"); a trim to about 17 s (cut the eyes insert, shorten the years).
