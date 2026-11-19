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

> These are frames from a short silent cartoon, in order. Describe what happens, beat by beat, as if telling a friend. Then answer: Whose situation is it? What changes between the start and the end? Who sides with whom, and how could you tell? What is the last image? Which moment would you screenshot? Which frames were confusing, and what did you think they meant? The video loops; does the end lead back into the beginning? On the phone-size sheet only: what can you still read or recognise, and what is lost?

Don't name the characters, the series or the joke. Give the sheet files and their folder neutral names; render with speech bubbles switched off.

## Score

- Compare each viewer's beats with your intended reading, line by line: read / misread (say how) / missed.
- Pass: both viewers read at least 4 of 5 beats.
- A beat both viewers misread the same way is a staging fault, not a viewer fault. Typical causes: the turn was a glance, not an action; the sign was too small; two things moved at once; the cut came before the reaction.
- Report a table of beat, intended, viewer A, viewer B, verdict and fix. Fixes go into the shot list, not straight into the code.
- List the details both viewers misread the same way even when every beat passed. They are usually cheap staging fixes: in Untitled, both read 5 of 5 beats and still shared eight misreads (a puff taken for blossom, a phone for "a blue rectangle", a squat for a fall, red X eyes for death, the card text lost at phone size).

## Limits

Say what the test can't tell: whether it is funny, voice timing and the mix. Those need people with sound on.

## Hook and loop variants

- **Hook test:** the first 3 s at 10 fps on one sheet. Ask: at 1 s, what do you know and is anything funny, surprising or moving? When do you first understand it? Would you keep watching at 1 s and at 2 s? What one change to the first second would stop you scrolling?
- **Loop test:** the final second, then the opening second, each frame labelled END or START. Ask whether the cut means something or feels like a restart.
- **Motion:** silent grids show poses, not movement. Pair the test with `hoodyz/motion.py`; a viewer can't tell a 0.2 shot from a 3.0 shot on a contact sheet.

## What the results are for

- They are a smoke test, not a verdict. Two viewers disagreed on the same footage (Make It Original v5.2 vs v5.3), so read a pair as a signal and confirm with a second pair before acting on a single report.
- They find faults inside the structure (who is speaking, what an object is, where someone went). They never replace a structure the person chose. If they keep pointing at the structure, put it to the person as an option.
- Ask what they would screenshot: it tells you which image is the episode's iconic one.
