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

## v7 final

- **A bubble tail points at the speaker,** and should end beside the face, not on the hair; a long tail across a doorway reads as the door talking. Put the bubble next to the speaker's head with a short tail, and turn off name tags before the first line so tails never cross them.
- **Faded smear copies read as a second character** in a still or a pause. Use speed lines and a stretch along the motion instead.
- **A character's own arm is a prop too.** A straight arm from shoulder to hat crossed his face; bend it at an elbow outside the face, and register each arm segment for the eye check.
- **Brand cards behind a switch** (`TAG=1`): deliver a clean final and a tagged one, and keep effect words (RUMBLE) off the brand's building.
- **Escalate the loop object:** the tower spits out FINAL (29), not a blank sheet, so the last image extends the count instead of ending on nothing.

## v8

- **A tail that ends near the hair reads as pointing at the hair.** Put the speaker's bubble beside the face at mouth height with a short horizontal tail; move the character if that's what makes room.
- **A squashed character's shoulders sit at chin height,** so any arm reaching up crosses the face. Draw the reaching arm behind the body and only the hand in front.
- **Tag the colour space** (`scale=out_color_matrix=bt709`, `-colorspace/-color_primaries/-color_trc bt709`); platforms guess otherwise.

## v9–v10

- **Whose mouth is open decides who speaks,** for the viewer. A tail on the open mouth reads; a tail on hair or on top of a head reads as pointing at the hair. When the speaker changes, change the voice and the lip-sync with it, and close the listener's mouth (a static "panic" O-mouth reads as talking).
- **Side tails beat long tails:** a bubble level with the mouth and a tail of 10–20 px is unmistakable; a bubble above a head with a downward tail gets read as pointing at whatever is behind it.
- **Check the exact flagged frame at full size before arguing.** Twice a reviewer flagged a tail I thought was right; each time the full-size crop showed something real (tail on the hair, tail above the head). When the person then chose a different reading of who speaks, the fix had to go through voice, lip-sync and the listener's face, not just the tail.

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

## Series pass: Just for Now v3 (9 Nov)

- **Bring older films up to the series standard in one pass:** title bar, polish layer, push-ins, no-tag version, stereo −14 LUFS. Old captions in TikTok's top area had to go anyway.
- **Moving a title bar in moves everything near the top:** bubbles, banners, calendars and a close-up's head all needed new heights.
- **Trimming without redrawing:** shorten scenes by changing their internal timings or by remapping old frames, and re-place every sound with the same old→new time map. Keep music on a regular beat grid and map only section edges.
- **The plant decides the twist.** The smiley drawn on Day 1 was about 40 px; both later jokes depend on it, so it got a close-up and his hand had to move out of the way.
- **Validate detectors, again:** a pixel-pattern chip detector "found" the chip in the no-tag file (dark bubble outlines). Differencing the two versions frame by frame was exact: identical up to 23.7 s, then only the chip's rectangle.

## Review fixes: Just for Now v3.1, Who's a Good Boy v3.5 (9 Nov)

- **Inherited faults still count.** The blank dust frames and the navy "hand" were in the earlier cuts too; a new version is judged as a whole, so check old shots as hard as new ones.
- **Never fade to a flat colour mid-story.** A whiteout reads as an empty field. Cap overlays (dust at 60%) and dissolve the next shot in underneath; flag any frame whose picture is nearly one flat colour.
- **Cuts must match what was on screen.** The falling pieces started 17 px lower and with a bigger top block than the standing stack, and the trophy vanished; that read as a second building appearing.
- **Measure clearances on rendered frames, not by eye.** The first 120 px shift still left hair touching the bar; measuring found 362 → 384. The first measurement also caught the bar's own grey text edges, so limit the search to the area that matters.
- **Push-ins must wait for entrances.** Zooming while a character runs in from the edge crops him; start the push once he's fully inside the zoomed frame.
- **Small props need a silhouette.** The lying dog read as a scribble; an outline, a lighter muzzle, an ear, an eye and a red collar fixed it. Check that a moved prop doesn't land under someone's feet.
- **A pat is a hand resting on top of the head,** not a disc covering the hair.

## Second review: Just for Now v3.2, Learn to Code v4 hold (9 Nov)

- **Similar colour plus similar pattern reads as "the same object".** A navy block with a window grid under the OFFICE block read as a second HEADQUARTERS. Give every block in a stack its own colour and texture.
- **An arm must come from a body the viewer can see.** Once a push-in cropped the boss's body, his arm became a white bar across the trophy. Start arms at the near shoulder, pass them behind held props and end them in a gripping hand.
- **Brand tags belong in the title bar,** not over the picture: a chip under the bar sat on the little office in the pushed ending.
- **A polish pass must not make any beat worse than the shipped cut.** Compare the new version beat by beat with the master: Learn to Code v4's cut-in put the HIRED stamp on his face and swept the robot's arm across HEAD OF HIRING, so the whole cut was held although everything else improved.
- **Stamps and props placed in screen space must be checked in every framing,** especially close-ups, where faces move to new places.

## Make It Original: auditions, sheet, rough (11 Nov)

- **Screen every melody, not only the hero riff.** The AI's first tune shared three intervals with Smoke on the Water; the interval screen caught it before anyone heard it. It's a quick aid, not a guarantee.
- **Measure synthesized notes against the written ones.** A single-note lead whose notes ring into each other turns into wrong low tones through distortion (up to an octave and a half off). Stop each note when the next starts, then check pitch per note.
- **Kokoro ignores capitals for stress.** "Now THAT'S original" came out flat; writing the phonemes with a stress mark (`ðˈˈæts`) and `is_phonemes=True` put the loudest point on THAT'S.
- **A gesture that carries the callback needs its own test.** The first wave-off read as "hi". Drawing three silhouettes side by side picked the one that reads as "go away" (a backhand brush outward).
- **Keep the gesture inside the frame and away from the buttons.** A world zoom pushed the flick off the left edge; the cat first played under TikTok's right-hand buttons. Check the key action, not just text, against the safe zones.
- **Make a looping riff fill whole bars.** With the riff on a 2 s bar, the robot plays it twice and the film cuts where a third pass would start, which lands on frame 0's riff.
- **Copy helpers into the new episode's own kit.** The series modules load their own voice files on import; a self-contained `kit.py` rebuilt cleanly from the repo.

## Make It Original: from rough to master (11 Nov)

- **A rough that explains the joke isn't a rough that performs it.** The slideshow passed every layout check and still failed on mute: one framing per era, half-bodies, decorative motion. Test the acting, not only the layout: tell the story from body positions alone.
- **Build matched shots from one function.** The 1986 rejection and the 2026 rejection, and the two stadium poses, share the same framing code and arm path, so a 50% overlay of the pair shows one figure. Prove each callback with an overlay.
- **Lock what the joke is before adding gags.** The cat was funny and still gave the ending two meanings. It came back only once the ending played them in order: his joy, then the cat on the monitor, then the robot's look.
- **Let a running image carry the structure.** The stadium appears three times (his fantasy, the cat on his stage, his fantasy again) and gives a hook at frame 0, a reveal and a payoff.
- **Sound can tell the joke too.** The speaker plays the cat's version, his fantasy turns it into his own guitar, the snap back returns the cat's. Cut arena reverb and crowd dead on the cut to reality.
- **Measure voices against the music around them.** The first mix had the lines 6-8 dB under the riff; raise the lines and check per-section levels, not just the overall loudness.
- **Check the key action against the frame edge after every camera change.** A zoom pushed his face off the left edge and exposed the set's right edge as a black strip.
- **A reported defect you can't reproduce still needs an answer.** "Stepped" floor edges did not exist in the frames; they were compression in the half-size preview. Say so, measure the edge on the final encode, and never send a low-quality preview for a finish review.
- **Use a fresh-eyes agent on muted frames before delivery.** It retold the story, confirmed both callbacks and found a cropped face, a too-subtle glance and dead space that the maker's eye had stopped seeing.
- **Reuse a finished cut by time-shifting it.** v4 imports version A's shot functions and calls the 2026 ones with `t - D`, so the two cuts can't drift apart and version A stays byte-identical.
- **Make the audio exactly the video's length** (`frames * 48000 / 30` samples), or `-shortest` drops the last frame.
- **Sort recorded takes by transcribing them.** A small Whisper model from the `k2-fsa/sherpa-onnx` GitHub releases (with `pip install sherpa-onnx`) runs offline when Hugging Face is blocked; split each file on silence and transcribe every take to find which line it is. Cut takes by time with short fades: a silence trimmer set for loud audio ate the first word of a quiet take. Then transcribe each line again from the final mix to check it's still intelligible over the music.
- **Noise reduction makes voices dull; measure it.** `afftdn=nf=-30` cost these takes 10 dB of 2-6 kHz presence (the band that carries consonants) against their 200-1000 Hz body. Use a gentler `nf=-45:tn=1`, then add about +5 dB at 3.2 kHz and a 6 kHz shelf and light compression, and compare the presence ratio with the raw take. Apply any pitch shift *before* the boost, or the shift drags the boost down with it.
