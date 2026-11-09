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

# Lessons from UptimeZ Inc.

What came out of *Saved Locally*, *Where Files Live* and *Prompt Telephone* (6–7 Nov 2026), after four tester reviews.

## Comedy

- **Recognition isn't laughter.** "So true" reactions meant the idea was relatable but not funny. The fix was people being ridiculous about AI, not AI being clever.
- **Don't invent a stand-in.** Testers didn't know what "SAVI" was; real, familiar things (Downloads, the cloud, a LinkedIn-style post) need no explaining.
- **Take jargon literally.** "Make it bold" → a post about a bald head works because every viewer knows both words.
- **Show the cause before the effect.** Each person's mistake must be visible as it happens, and each must be worse than the last.
- **Turn the punchline on the smug one.** DON's "Finally. A post about me." beat any ending where the AI or the junior loses.
- **The brand is the straight man.** A polished, earnest company page makes the chaos inside it funnier; it never jokes itself.

## Testing

- Don't test a visual gag with audio only, and don't loop a clip three times before asking for the first reaction.
- Five viewers against five can't prove a winner; use tests to find what confuses people.
- Measure confusion (where people got lost), not the number of gags.

## Technical

- Wrap earlier modules at runtime (`pt43` patches the kit's face drawing for lip-sync) instead of editing them, then check old cuts still match by checksum.
- Drive lip-sync and word cues from the measured voice timings (`pt43_sync.json`), not from hand-typed times.
- Chain a speaker's TTS clips with a small gap; overlapping clips from one voice sound broken.
- `loudnorm` left these mixes around −18 LUFS. A compressor, fixed gain and a limiter set below the target reached −14.5 LUFS with a −1.5 dBFS peak.
- Faces must never sit behind monitors or props; check every reacting face in the contact sheet.

# Lessons from "Saved to Cloud" (S1v2 → S1v3.5)

Seven versions in one session, plus one outside review (6.8/10 for S1v3). Files: `uptimez_S131_*` (A/B test), `S133`–`S135` (cold open, name tags, doodle payoff).

## Comedy

- **A picture beats a sentence for the payoff.** "CAN MY BOSS SEE THIS?" made viewers read; PAM's horned doodle of DON reads in under a second, with sound off, in any language. Put it beside his gilded portrait and the contrast is the punchline.
- **A repeated line needs new meaning.** DON repeating "Nice. Shared." only works once the page is about him.
- **Never make a button do the opposite.** SAVE that leaks (S1v2) and DELETE that saves (S1v3) both confused people; the outside review caught the second one, after I had criticised the first.
- **Cut a character whose line adds nothing.** MAX's "Where's the file?" was already shown by the flying file.
- **Extend only with beats that earn a laugh.** 15 s → 25 s worked by adding a mid-film gag (the cloud hiccups a file, PAM shoves it back), not by slowing shots.

## Openings and intros

- **Cold open on the climax, then rewind.** Frame 0 is the ACHOO; the page slaps the lens; "15 SECONDS EARLIER…". The page in the first second doubles as the planted detail.
- **Introduce the cast with freeze-frame tags, not speeches.** Spoken "Hi, I'm Don…" costs 2 s each before anything happens. A 1.0 s freeze with a comic bubble (name + three emoji) is a joke in itself.
- **Tags in the film's own style.** Navy corporate lower-thirds looked pasted on; white comic bubbles with a tail to the character fit.

## Process

- **Over-specifying again.** S1v3 specced blinks, a cat, BPM and file labels before the joke was proven; the review was right to cut them. Same lesson as the robot-office episodes.
- **One test variable at a time.** The A/B renders differed only in the page.
- **A comic pause is not dead air.** Keep "no gap over 0.5 s" for the mix, but hold 0.6–0.8 s before the punchline.

## Technical

- `engine_v.py` renders any length (`DURATION` in the module) and exposes the unquantised time for smooth camera moves.
- A **time map** wrapper (`s133.py`) adds a cold open, a rewind and freeze frames around an existing film without touching it; `sound_s133.py` splices the old mix with the same map. Re-measure loudness after splicing: it came out at −18 LUFS until the gain was raised.
- Pose tweening: register tweened arm angles in the kit's pose table at runtime (`anim.py`), so the kit draws in-between poses unchanged.
- Colour emoji in cairo: draw them with PIL (`NotoColorEmoji`, size 109, `embedded_color=True`), convert to premultiplied BGRA and paint as a surface.
- A doodle style (wobbly blue pen, Permanent Marker labels) separates "drawn by a character" from the paper-cutout world.

# Lessons from "Downloads Expedition" (v1 → v5)

Five versions and four outside reviews. The fourth review put v4 on HOLD: the joke read, the drawings didn't.

## Drawing

- **Parent every prop to a body.** Hats, lamps, badges and held files were separate stickers placed in canvas coordinates, so they drifted off heads and hands between shots. In v5 each is drawn inside the body's transform (`rush()` returns the lamp position; files follow `p["hands"]`; badges are redrawn last in the same transform).
- **Fix draw order, not just positions.** A file drawn before the hand that holds it reads "TNAL (27)"; a desk drawn after a face cuts the eyes. Decide per shot what is in front, and check it.
- **A light beam has one source.** Cut the beam out of a darkness layer with its tip on the lamp; a triangle placed in the frame never lines up.
- **Don't hold the camera on the weakest drawing.** The 4 s face close-up was the worst composite in the film. A wide shot with clear staging (MAX enters on the door side, never crossing PAM) told the same beat better.
- **Fewer, bigger things.** Six sheets that leave the frame read as an avalanche; thirty became grey discs. Impact lines read better than dust.
- **A door is open or closed.** Animate it in 0.1–0.15 s; a half-open door looks like a broken slab.

## Checks

- **Register props, not only text.** v4's checks covered labels and faces but missed desks, hat brims and sheets crossing eyes. `qa_dlx.py` now registers an eye band for every face and a box for every prop drawn after it, and checks that each bubble tail ends at its speaker's head.
- **Run A/B identity checks in separate processes.** Both wrappers set the same module global, so a single process rendered B twice.
- **Look at the 1080 frame too.** PAM's badge sat half under the desk; only the full-resolution still showed it.

## Process

- **Make each episode stand alone.** `dlx.py` imported the emoji drawer from `s134.py`, which pulled in the whole Saved to Cloud chain and its sync files; a standalone `emoji.py` fixed the clean build.

## v6 polish pass

- **Cut dead holds with the time map, not by re-timing beats.** A second entry in `dlx.CUTS` removed 0.6 s of a hold where only a lamp flickered; picture, mix and lip-sync stayed in sync because all three read the same cut list.
- **A listener needs a reaction.** MAX standing still after "Downloads." killed the joke; eyes to the door, a gulp and eyes back cost no screen time.
- **Show the hand that does the action.** The helmet sliding out by itself read as a glitch; a hand on the brim and two yanks read as a tug.
- **Smear with ghosts, not tilt.** Two faded copies along the path and a stretch along the motion sold the blast better than rotating the cutout.

## Thumbnail and delivery

- **Draw the cover with the film's own kit,** so the characters match, and keep the title and every face inside the centre 1080×1440 that profile grids crop to. Put the title above the set so the signs that set up the joke (DOWNLOADS, the plaque) stay visible; check it at grid size.
- **Rebuild from the repo before calling it shipped.** The workspace render can hide missing files or sync data; comparing the repo build with the delivered video (PSNR inf / identical streams) caught an import chain that needed another episode's data.
