# Perfect Date

ME + MY AI episode. 1080×1920, 30 fps, 670 frames (22.3 s), −14.1 LUFS, true peak −2.0 dBTP.

Hoody asks his AI to help him impress Eva. MY AI shows him how (a rose: "Watch!"), hands him the guitar ("Your turn!") and, as a proud stage tech, pumps up his heart balloon for the show. He floats up playing his old riff from *Make It Original* with his eyes shut, while Eva takes the robot's hand (HIS DATE → ITS DATE). He opens his eyes above an empty bench. *Plonk.* The cat covers her ears. The balloon pops, he falls, and he lands on the bench with a BOOM, dizzy. The loop cut to the calm opening face is the reset.

- `perfect_date.mp4`: the final (x264 crf 14 slow, AAC 256k, faststart)
- `cover.png`: the gap wide with the title (`cover.py`)

## v2 (18 Nov): the hook and the loop

**`v2/perfect_date_v2.mp4`** (17.5 s, 526 frames). `bash v2/build.sh` rebuilds it; v1 is imported, not touched.

**What changed:**
- Frame 0 is the ask: on the bench, "HELP ME IMPRESS HER!" already on screen, MY AI leaning in, Eva right there.
- The film ends in the same bench shot: he crashes down, dizzy and alone, held 0.8 s. The loop lands on him asking MY AI again, and the label resets ITS -> HIS.
- Cut: the opening close-up, the park wide, the cat-and-dog cutaway and the top-down shot. Shortened: "Your turn!" and the float.
- A real hand pump with PFF puffs, ITS DATE popped at twice the size and held 0.8 s, and the string snapping on PLONK.

**Checks:**

| Check | v1 | v2 |
|---|---|---|
| Premise readable | at 2.2 s | **at 0.0 s** (hook test: "I know the setup at tile 1") |
| Still at 1 s? | "I'd swipe" | "Probably swipe": the opening barely moves for 1.5 s |
| Loop | "more like a restart" | "reads as *he never learns*, a nice gag", but nothing bridges the cut |
| Biggest laugh | HIS -> ITS DATE (~12 s) | HIS -> ITS DATE (~9 s) |
| QA | pass | pass: -14.1 LUFS, -1.1 dBTP; "Your turn!" reads as "your time" in 2 of 3 recognition windows (the bubble carries it) |

**v2.1** (same file, 16.4 s, 493 frames):
- MY AI bounces and rubs its mitts while he fidgets.
- The ask runs 1.2 s, and the rose lands by ~2 s with Hoody in the shot.
- A head-shake bridge leads into the loop.
- The pink close-up and the rose shot are trimmed.
- The mix dips 4 dB under "Your turn!", which now passes the speech check.
- `v2/master2.sh` adds a 15 kHz low-pass and limiter 0.6, after the BOOM overshot to -0.5 dBTP.

QA passes: -14.4 LUFS, -3.6 dBTP. Both fresh testers still swipe at 1 s: the motion is too small in a wide shot. Both independently said to open on the result, the robot handing her the rose. The loop "half works": the dazed hold drags, and the robot and Eva pop in.

## Build

```bash
bash build.sh        # render.py final → audio.py → master.sh → perfect_date.mp4, then cover.py
```

A clean rebuild from `git archive` gives the same decoded video and audio (md5).

## Files

- `render.py`: 20 shots. `VO` holds where each line sits; the lip sync and `audio.py` both read it, so mouth and sound cannot drift
- `audio.py`: park and wind, the riff (`sound.py`, the 1986 take), pump hiss and squeaks, MY AI's alarm boops, plonk, three creaks, the pop, the falling whistle, the BOOM (its tail wraps the loop)
- `master.sh`: linear gain to −14 LUFS + a limiter (no loudnorm: it flattened the Says Here shout)
- `characters/eva.py`: Eva v2, now with a walk cycle (knees) and blinks
- `characters/myai.py`: MY AI v2: fixed two-segment arm rig, eight eye shapes, `talk` (eyes squash, antenna glows with the voice), a stepping walk with knees, the decorative rose
- `vo/`: Tomas's takes (whisper 3, oh 3, whoa 2; ooh, sigh, breath unused) and MY AI's two lines in its locked voice

## Checks on the final

| Check | Result |
|---|---|
| Frames, size, rate | 670, 1080×1920, 30 fps |
| Loudness | −14.1 LUFS, LRA 8.2, true peak −2.0 |
| The BOOM vs the pop | about 9 dB louder (RMS) |
| Phone-app zones | no text in the top strip, right rail or caption area |
| Speech recognition in the final mix | "Watch!", "Your turn.", "Oh", "Wow" ✓ · the whisper reads "Help me, Prescott" (borderline; the bubble carries it) |
| Clean rebuild | identical decoded md5 |
| Cold mute tests | five, one per rough; fixes from each are in the commit log |

## Lessons from this episode

1. **A helpful machine can read as a saboteur.** When MY AI pumped the balloon with no reaction, viewers read "gets him out of the way". One beat fixed it: wide eyes, a red "!", arms reaching up after him, *then* Eva takes its hand, *then* heart eyes. The reaction to the accident is what proves it was one.
2. **Plant every prop in every shot it belongs to.** The balloon vanished from the playing close-up and Tomas caught it. Check prop continuity shot by shot, not only where the prop matters.
3. **Lip sync from loudness needs a floor.** Normalising each take to its own peak kept the whisper's mouth open the whole line. Mapping the per-frame dB between the take's 35th and 97th percentiles makes the gaps between syllables close the mouth.
4. **A 4 fps mute test can miss a 0.2 s impact.** The BOOM fell between the sampled frames. Judge very short beats at full frame rate, and with sound.
5. **"Last frame = frame 0" isn't always right.** Here the loop cut itself is the reset joke (dizzy → calm), so the film ends on the dizzy face and the label resets on frame 0.
6. **Views straight down need two cues.** Legs hanging into the top of the frame read as "poles" until the soles faced the camera and his shadow sat on the grass below. A tiny couple in a high view read as strange; a side-on wide with him small in the sky read at once.
7. **A label change is the punchline, so make it move.** ITS DATE in a small pill was missed; popping it big for half a second made every viewer catch it.

## Caption (draft)

> He asked his AI for help impressing her. It helped. 🎸🎈 Watch the top bar.

Pinned comment: *Was MY AI being helpful or did it know exactly what it was doing? 👀*

Hashtags: #MEandMYAI #Hoodyz #AIcomedy #animation #wingman #fyp
