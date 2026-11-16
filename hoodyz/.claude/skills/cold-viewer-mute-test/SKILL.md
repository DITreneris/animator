---
name: "cold-viewer-mute-test"
description: "Use when checking whether a Hoodyz (ME + MY AI) rough cut or storyboard reads without sound, by sending frame grids to fresh subagents acting as cold viewers."
---

# Cold-viewer mute test

The test only works if the viewer has never seen the script, the concept or the earlier versions.

## Prepare

1. Render the cut without captions, bubbles or sound, or extract frames from it.
2. Make contact sheets at 4 fps, numbered in reading order, with a time stamp per tile. Add an 8 fps sheet for any beat under 0.5 s: a 4 fps grid misses impacts.
3. Add one sheet at feed size (about 270 px wide tiles) to test what can be read on a phone.
4. Write the intended reading yourself first: 5 beats, one line each. Don't show it to the viewer.

## Run

Start two fresh general-purpose agents, each given only the sheet paths and this prompt:

> These are frames from a short silent cartoon, in order. Describe what happens, beat by beat, as if telling a friend. Then answer: Whose situation is it? What changes between the start and the end? Who sides with whom, and how could you tell? What is the last image? Which moment would you screenshot? Which frames were confusing, and what did you think they meant?

Don't name the characters, the series or the joke.

## Score

- Compare each viewer's beats with your intended reading, line by line: read / misread (say how) / missed.
- Pass: both viewers read at least 4 of 5 beats.
- A beat both viewers misread the same way is a staging fault, not a viewer fault. Typical causes: the turn was a glance, not an action; the sign was too small; two things moved at once; the cut came before the reaction.
- Report a table of beat, intended, viewer A, viewer B, verdict and fix. Fixes go into the shot list, not straight into the code.

## Limits

Say what the test can't tell: whether it is funny, voice timing and the mix. Those need people with sound on.