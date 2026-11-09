# Lessons from the robot office episodes

What worked and what failed while making *Says Here You Were Our Boss*, *He Always Said Thank You*, *Make It Better* and *Just For Now* (3–6 Nov 2026). The same lessons were proposed for the `viral-loop-animation` skill.

## Comedy

- **Characters beat situations.** The guy hiding his own smiley got better reviews than the building collapsing.
- **An expected disaster isn't a punchline.** If the setup says it will fall, make the fall a false ending and put the surprise after it (Just For Now: collapse → "Should I put it back?" → POP).
- **Escalation means worse, not more.** Each scene must add a joke or make the character sillier; extra events alone don't.
- **One visible physical rule.** Viewers must see what holds what up. A sticky note can't cause a collapse; load-bearing tape can.
- **End on a word that finishes the arc,** set up out loud earlier ("I'll fix it Friday" → "FRIDAY.").
- **A bigger twist can repeat the joke at a larger scale** (the boss robot with the same secret).
- **Plain words for general viewers:** everyday feedback and excuses, not "scope" or "context windows".

## Openings and loops

- The first seconds must make sense with no context. *Make It Better* v1 opened on the payoff and confused people; v2 states the situation first.
- Use several quick shots (crash zoom, smash cut, sprint-in), not one static wide shot or a slow zoom on a bubble.
- Don't split a sentence across the loop point or repeat the same words at the join. Loop through a character's action (the Tester reaching for the tape again) or a reaction (the army's roar).
- Call a hard cut a hard cut.

## Process

- Generate and measure voices before fixing scene lengths.
- Build a rough version before polishing. A 2-scene test checks one joke but can't judge a story.
- For a line choice, render identical versions and show them to different people; ask what made them laugh.
- Treat reviewers' scores as opinions until real viewers test it. Separate agreements from disagreements and say plainly where the reviewer was right.
- Frames and loudness can be checked from code; comedy timing, voices and mix need a person.

## Technical

- Ease functions that return 0 at the start make cairo's scale invalid; clamp to 0.02.
- Draw props that carry the joke after the characters; check bubbles don't cover labels or heads.
- A navy hoodie disappears on dark backgrounds; lighten the background.
- Long digital silence sounds like a fault; add faint room tone.
- Set the limiter below the target peak (AAC overshoots), then re-measure the final file.

# Lessons from Payday Slam → The List

What worked and what failed while turning the "Wait, you guys are getting paid?" meme into *The List* (3–6 Nov 2026).

- **Copying the meme's table isn't a video.** *Payday Slam* was clear but had 16 numbers and no funny action; the reviewer's verdict was "too many numbers, no funny animation".
- **More shots lost the story.** Separate close-ups per character made each gag funnier, but without a shared setting or labels, viewers couldn't follow who was who or why the coder paid.
- **Go back to what worked and add only the best gags.** The fix was the original meme's one-screen comparison plus one gag and one number per row.
- **Test the joke with one still before animating.** A single image of the finished list confirmed the story was clear in seconds, before any animation time was spent.
- **Approve in stages:** style still → punchline clip with voice → storyboard → still → animated draft. The punchline clip is the stage that decides the rest.
- **Keep the caption identical to the voice line.** A reviewer suggested a shorter caption, but it would no longer match the recorded line.
- **Repetition can be funnier than clarity:** −$200 shown four times beat "−$200/month".
- **Fill an empty opening with the character.** Starting the coder huge and shrinking him as each row arrives fixed both the weak first frame and the empty middle of the screen (the author's idea).
- **Recorded voices beat synthesized ones for the punchline,** and their real lengths set the timing.

# Lessons from Payday Slot Machine

What came out of making and reviewing *Payday Slot Machine* (3–4 Nov 2026, added 7 Nov).

- **Ask for concepts, get concepts.** Five ranked ideas with hook, joke and payoff made choosing quick; the slot machine won because the meme was already a four-beat reveal.
- **Protect the reveal.** A slowing reel showed "$600k" 0.2 s before the jackpot. Check the frames just before each payoff, not only the payoff itself.
- **Measure the file you deliver.** Loudness was first reported from before a final level change; the delivered file was quieter. Repeat checks after every rebuild.
- **Leave headroom before AAC.** A −1 dBFS peak rose to about 0 dBFS after encoding; limit first, then normalize.
- **Pin the encoder for reproducible builds.** With automatic x264 threads, two builds differed in three frames; a fixed `-threads` value made rebuilds byte-identical.
- **Font files differ between copies.** The repo's Anton is a different build from the one first used; fitting text to the frame width keeps any build on screen.

# Lessons from Learn to Code

What *Learn to Code* (25 s, 2024 → 2026, ending under Tower Bridge) taught us (7–8 Nov 2026).

## Comedy

- **The punchline must answer the line before it.** "They fired you too?" → "My AI is still talking with your AI." didn't land, because a yes/no question wants a reversal ("Worse."). The stall line works once the question is one it can stall: "Any news on my application?".
- **A/B endings may need their own setup line.** Otherwise the test compares a working joke against a broken setup.
- **Show a callback as big the first time as at the payoff.** The robots "still talking" only reads if their 2025 chat bubbles are as large and clear as at the board meeting.
- **Plant the ending in the opening shot.** The next tent's "HEAD OF HIRING" sign is visible from frame 0 and only makes sense after the reveal.
- **Fill the beat after a big stamp.** He coils the useless cable while his robot floats hearts, instead of 1.5 s of nothing.

## Camera and readability

- In wide shots faces are about 10% of the frame height, too small on a phone. Push in 1.3–1.6× on reaction beats and during punchlines, then ease out before the next move.
- Keep subtitles, title bar and popups in screen space so push-ins don't move or crop them; move subtitles up while zoomed.
- A tilt from the hero up to the reveal above him (the robots' board meeting on the bridge) and back down to the opening composition makes a clean loop.

## Technical

- Check TTS pronunciation from phonemes first: "A.I.s" was spelled out, "AIs" was right. British voices need `lang='en-gb'`.
- Pan mono to stereo before measuring loudness, or the result is about 3 LU too loud.
- Sharp click clusters made AAC overshoot the limiter on one channel; low-pass the clicks.
- Scale-in animations that start at frame 0 are invisible on frame 0; start them a few frames earlier.
- Variants (ending B, polish pass) behind environment switches with new file names, verified by checksums and by comparing frame hashes against a saved copy of the old module.

## Delivery: the no-tag pass (8 Nov)

- **Don't burn the brand chip over the payoff.** On *Who's a Good Boy?* it covered the last 2 s (robot, ball, dog), so trimming it off would also cut the ending. Keep tags behind a switch and render a no-tag version.
- **Keep text off the frame edge.** TODAY ended at x 1079 of 1080 and read "TODA" in a full-width crop; it now ends at x 1045.
- **A loop's last frame isn't the punch line.** For deliveries that don't loop, hold the payoff to the end with the punch line on screen.
- **ffmpeg concat paths are relative to the list file.** A list pointing at the old build folder silently rebuilt the old video; check the changed area in the output.
- **Test a detector on a known positive** before trusting a "0 found".
- **Rebuild from a clean repo copy** and compare decoded video and audio with the delivered files; all six videos matched exactly.

## Polish passes: Learn to Code v4 and Who's a Good Boy v3.4 (8–9 Nov)

- **A rewatch twist beats a rewatch detail.** Making the job site's logo his own robot's face changes what the opening means on a second watch; the earlier plants (a sign, a pigeon) only reward noticing.
- **Check invented brand names before using them.** "JobBot" and "HireBeep" are real companies. A series character's face plus a plain word (JOBS) can't belong to anyone.
- **Plants must be readable the first time.** The 2024 APPROVE button was about 90 px with an unreadable label, so the robot taking it over in 2026 lost its callback; 1.45× and a close-up on the first press fixed it.
- **Hard cut-ins feel faster than glides** for a single beat ("You're hired!"); keep glides for reaction faces and reveals.
- **When a push-in moves props under the subtitles, move the subtitles,** per scene: the office subtitles had to go from under the desk to the wall once the button got bigger on screen.
- **A layered film can take a camera layer without touching its scenes:** wrap each scene function in a camera move and draw subtitles and the chip in screen space.
- **Small contact-sheet tiles hide a 1.3× push-in.** Compare the same moment side by side at a readable size before concluding something is missing.
- **A comparison where both sides error "matches".** Check the outputs aren't empty, and include a positive control that must differ.
- **Run rebuild checks one at a time.** Two builds encoding in parallel made x264 differ on 1–4 frames (404 edge pixels, at most 15 levels); rendered alone, the same scene matched the delivered file bit for bit.
