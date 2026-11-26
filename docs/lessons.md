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

## How Sofía Survived Day One (10–12 Nov)

- **Bring a prop in on the cut where it's needed.** Parking the approval train at its final spot for all of 17:00 put the button on the robot's arm in the two-shot; arriving on the cut to the press kept both shots clean.
- **In tight two-shots, bubbles go above the head or into clear wall,** not beside the mouth, where the other face sits. Use the same spot for a repeated line (all three "Pam?") so the rule of three reads at a glance.
- **A blind press needs the hand and the eyes in one shot:** his hand on the button, his eyes still on her, the whole label visible.
- **Dead air at the start is lost viewers.** If the opening gag is visual (pressing BREW), make it audible too and escalate it (one buzz, two, then the full "denied").
- **Mouth shapes from phonemes beat loudness.** Spread the line's phonemes over its voiced span, give vowels more time, and keep at least one drawing for every m/b/p and f/v. Sample on the 12 fps drawing grid, because the engine only redraws 12 times a second.
- **A matched loop rewinds state, not just the picture:** the coffee goes back up, the evening grade returns to morning, and the film opens on the exact framing it ends on. Measure the join (mean pixel difference about 9 against about 45 for an unrelated frame).
- **Shared-kit changes go in as optional hooks that default to off,** then frame hashes prove the older episodes still draw identically.

## I Will Replace You (12 Nov)

- **When two spacing rules fight, cheat per shot.** The robot needed room from Don *and* clearance from Sofía on one 540-unit table. Sliding the pair apart whenever the third person is out of frame solved both; only the wide shows true spacing.
- **Measure gestures, don't eyeball them.** The first point measured −6 px (touching her hair); the shipped one has a 29 px gap. The same check caught the cover's first draft poking her eye.
- **A pose must read as a black shape.** Rendering the three robot poses as solid silhouettes showed "nervous" and "collapse" were the same diagonal; making one compact and the other diagonal fixed it.
- **Brow direction decides the emotion.** Bars higher at the inner end read as sad, not stern; flat or inner-low reads as commanding.
- **One obvious object beats five small ones** at phone size: a giant bolt sticking out of the bun read where a cluster of grey parts did not.
- **9:16 two-shots are width-limited.** Cropping off ceiling and floor doesn't enlarge faces; seat the pair closer or let a third character be cut at the edge.
- **Test the joke in motion before the storyboard.** Two 5 s silent tests (reveal → reaction, point → collapse → whisper) settled the hardest beats cheaply.
- **Check bubbles with pixels.** Rendering each frame with and without bubbles and diffing the face discs found every overlap; a forced overlap proves the check works.
- **Voice effects can create the glitch.** A high-pass "whisper" sharpened the s-sounds into bursts, and the robot's hard shout clipped Don into a buzz (11.5% of samples saturated). Soften s-sounds, choose the cleanest of several takes, and measure saturation before mixing.
- **A narrative loop can beat a seamless one.** Sofía's look to Don, then to us, then a resigned blink makes the repeat a joke ("he learned nothing") without engineering a matched frame.
- **A face wrapper that draws a stock expression can paint over a mouth drawn before it.** Don's "grin" wrapper (used for the pun and "Approved.") drew its smile after the lip-sync mouth, so the words never showed. Fix: draw the moving mouth *after* the wrapper runs, not inside the normal face hook.
- **Reuse the mouth-shape code instead of re-deriving it per episode.** The viseme set, openness map and the mouth-drawing function from *Day One* carried over directly to Don and Sofía v4 and to the robot's screen talk; only the skin tone, lip colour and erase size changed per character.

## Happy Compliance (14 Nov)

- **Check the 9:16 frame before the storyboard.** Drawing the key shots into real 9:16 frames on the set sheet showed that a wide with four characters makes every face tiny; it moved frame 0 to Don alone and tightened shot 8 before any animation existed.
- **A prop that covers the eyes kills the setup.** The razor at Don's cheek hid his eyes, so nobody could see him look at the ornaments; at the jaw, plus a point-of-view cut, the line makes sense.
- **Size bubbles from the measured text, and guard the tail.** A box pushed down by the safe area can end up over its own anchor and draw its tail back across the text; detect it and point the tail straight down.
- **Draw a handed-over object in front of the receiver.** In the first handoff the ornament was hidden behind Pam's body; it needed to be drawn after her, bigger, with the camera pushing in.
- **Opt-in fixes keep old renders exact.** The HR-badge fix and Don's jaw pose went in behind flags and new constants, and the film's polish runs through hooks applied only while it renders, so every earlier sheet, test and storyboard still rebuilds byte for byte.
- **Don't let a pinned script and a live one write the same file.** A sheet script whose default output was the previous version's name overwrote it once; the frozen v1 script restored it exactly, and every sheet script now writes its own version's name.
- **Outside reviews: take the readability notes, check the story notes.** Most suggestions (bigger bars, larger robot face, intentional handoff) were cheap wins; one ("make Pam self-satisfied") contradicted an approved choice and the reason for the joke, so it was declined.

## Raises for Everyone (15 Nov)

- **Measure the takes, then hold shots; don't squeeze voices.** Four lines ran past their storyboard slots; holding those four shots a little longer (35.0 → 36.6 s) kept Pam's slow deadpan and changed nothing inside any shot. A remap table moves every line and effect with them.
- **A laugh is its own line.** "Boy or girl? Ha!" read the "Ha" as a word. Splitting the laugh off and building it from four pitched, spaced takes running down, with a wheezy breath, made it a laugh.
- **Watch the pen colour after an erase.** Don's smug smirk vanished because the skin ellipse that cleared the old mouth left the pen in skin colour; fixed behind a flag so earlier renders stay exact.
- **A cheated prop needs a size check against the real thing.** The drumstick has to cover the word on the robot's real screen; the sheet compared real size with a 1.5× cheat, and the person picked.
- **Reviewers can misread a prop name.** "Turkey leg" was read as Don's own leg. Label props unambiguously on sheets ("a drumstick, not his leg").
- **Staging must let hands reach.** Don standing at the set's floor line couldn't reach the table for the slap; he stands closer in the storyboard.
- **Emoji pops are not thought bubbles.** One emoji, a round tinted bubble with no tail, only on silent reaction beats; never on the payoff smile or a spoken line.
- **Verify the repo copy, not just the workspace.** Every sheet, storyboard sheet and the cover rebuild byte for byte from `src/`, and sampled frames of the storyboard, animatics and animation match.
- **Spell-check the props the frame crops.** A hand over the "PO" of POLICE left "LICE" on screen; a crop of THANKFUL read "HANKFUL". Check what partial words read as, in every shot, not only on the sheet.
- **Fit the camera to the payoff, then add the push.** The final two-shot lost half of Pam's face once the slow push was added; frame the payoff wider than the push needs.
- **Plants can live in a cutaway.** Squeezing Pam into the edge of a two-shot to plant her look cost the frame; a 0.6 s close-up on the cue word ("arrest") planted it better and gave the two-shot back.
- **Fix one seating order before the storyboard.** Exits, the robot's beam and the chain all depend on who sits where (Sofía, Don, Pam, the robot left of them).

## Secret Santa (15 Nov)

- **Triage every outside review against the brief and the user's own picks.** Six reviews this round: most points were already done or were conventions on purpose; a few were real misses. Answer with OK / partial / disagree and the evidence, and never adopt a point that undoes a choice the user made (the shy closed proud smile, the loop).
- **Check each costume prop against every shot that uses the character.** Don's Santa hat looked fine on the sheet and hid the bald head that the shot 6 gag is about. The fix (no hat, the bald agent) came from a phone-size A/B/C of three heads, not from argument.
- **A "looking past her" beat needs a visible target.** Don looked screen-right with nobody there, so it read as looking at Pam. Put Sofía's earring at the frame edge; with shades on, slide them down so the eyes carry it.
- **Small plants must be 2-3x bigger and get their own beat.** The lipstick kiss on the tag nearly vanished on a phone, and the third stamp's joke with it. Keep the whole tag (TO:, FROM:, both names) in frame before anything is barred.
- **Show the consequence, don't say it.** "He won't. You're welcome." landed only once the robot moved Pam's present to UNCLAIMED while Don's TO: SOFÍA (SECRET!) got APPROVED in the same still frame.
- **Re-time with piecewise time warps.** Knots at each line's start: only the stretch that needs room slows down; an uncap, a stamp or a reaction before the first line keeps its speed. Voices are never sped up; the total lands where the takes put it (34.6 to 40.8 s).
- **Hide by not drawing, not by covering.** The tag's write-on drew the names with the kiss already barred, and the bar cut the M of PAM.
- **cairo `arc()` joins to the current point.** Eleven rings drawn without `new_path()` became one tangle: the earpiece read as spaghetti in close-up. Start each closed shape with `new_path()`.
- **Stage tight two-shots with a gap between bodies.** Don leaning into Pam's held-out glasses merged two arms and a vest into one knot; standing him clear, with the lenses in the gap, fixed it.
- **Fonts miss glyphs silently.** ♥ and → rendered as empty boxes in Inter and Permanent Marker; draw hearts as paths and check every sheet's text.
- **Name frame dumps so cleanup globs can't hit deliverables.** `rm ss_sb_*.png` also deleted `ss_sb_sheet_v1.png`; the checksum list caught it and the pinned script rebuilt it byte for byte.
- **Measure true peak after the AAC encode.** The same limiter gave −0.3 dBTP from the WAV and −2.4 dBTP when fed AAC; render the audio once, measure it, then mux.
- **Separate conventions from defects in an automated frame check.** Tails above the hair, hard cuts and the 12 fps steps are the series' look; a cropped brand sign, a clipped prop card ("P SECRET / ANTA") and untagged colour were real.

## Office Noir: The Secret of a Stolen Heart (16 Nov)

- **Black and white with one accent colour carries a genre.** Grey everything with a tone curve, keep exact key colours (the red heart, Sofía's lips, gold at 35 %) and cut to full colour for reality. The colour cut is itself a punchline.
- **Every dream object needs a reality twin, visible at phone size.** Flask → strawberry milk (both with a bendy straw), informant → pink bunny, boss shadow → Mom in curlers, robot partner → baby monitor. Make the twins whole and big in the last shot, not set dressing.
- **A supporting character's role must read in one second.** The robot read as a guard until he got a fedora, a trench, a badge and Don's VO "My partner. Never blinks.", then pointed: "You."
- **Lines: say the whole thing, then interrupt on the punch word.** "Sofía, did—" sounded like a glitch; the full question works. The brag list is recorded item by item ("Whiskey. Money. Women.") so Mom's "DONNIE!" lands on the strongest word.
- **Wording trade-offs are the user's call.** "Did you steal *my* heart?" (Don's flirt, rewatch irony) vs "*a* heart" (first-watch clarity): lay out both in two lines and keep their pick.
- **TTS casting:** older, shouting Mom = a female voice blended with 25–30 % of an older male voice, a slow wobble, a dry rasp, a drawn-out "Donnieee!" with drive; measure the spectral centroid (≈5 kHz means hiss). Sofía's put-down = her own voice 2 semitones down, slower, a pause before "darling".
- **The length is the user's decision.** Two reviews wanted 30–33 s; the user chose 40 s for noir pacing. Don't re-propose cuts they declined.
- **Bubble tails: aim at the mouth from the side.** After two reviews flagged tails ending on hats, hair and curlers, the rule changed: the box stays put, the tip lands at the cheek at mouth height on the side facing the box, never over eyes or mouth. Off-screen speakers keep tails running out of frame; the robot speaks in its own mono type.
- **Frame 0 is the thumbnail: never a flash.** The lightning moved to 0.13 s; frame 0 is the readable office and the loop's heart match.
- **Native 1080 from 540-unit code:** swap `cairo.ImageSurface` for a factory that makes 540x960 requests at 1080x1920 with `set_device_scale(2, 2)`; give code that reads `get_width()` for geometry an opt-in logical size. Limiter 0.80 overshot to +0.3 dBTP after AAC; 0.60 is safe.
- **Hat gags:** sliding a hat down uncovers the head. Keep it seated, grow it ~10 %, bend the brim; act with a squint, because a brow under a brim is invisible.

## Happy Compliance v2 (16 Nov)

- **A character redesign must reach earlier-released-later episodes.** Christmas releases after Thanksgiving, Mandatory Fun and Secret Santa, so Pam gets her canon head there (streak, readers on the chain, rose lips) while every costume gag stays.
- **A prop drawn by two pieces of code breaks continuity.** The new Pam wore the mask up, but shot 10 drew its own mask at her neck. Search every place a prop is drawn when its state changes.
- **Payoff moves need ≥0.35 s and a hold.** A 0.18 s snap was invisible to reviewers. Reordered: the line with the mask up, then the visible drop over her readers, a push-in and a silent hold.
- **No cropped words: show a sign whole or not at all.** Place the banner where every camera shows it whole or not at all, and leave signs out of shots whose camera would cut them; since no camera ever shows that part of the wall whole, nothing pops between cuts.
- **A prop that reads as a body part is a defect.** The razor drawn with Don's fingers read as a cut-off hand on the floor; draw it alone, bigger, with foam.
- **Pinned scripts must import pinned modules,** or the `_v3` sheet stops rebuilding byte for byte as soon as v4 lands.
- **A wrapper module for an engine forwards the engine's module attributes** (`DURATION`): without it the render silently stopped at 15 s.
- **Curved tails, drawn to the mouth in that frame.** Three reviews in a row said straight tails missed the mouth (a head that bobs, a box the safe area moved). What fixed it: record where the mouth was actually drawn this frame, then draw a curved wedge from the box that bends outside the head and ends beside the mouth, never on it. Key the record by the bubble's anchor x, because the layout step moves the anchor y.
- **GitHub refuses files over 100 MB.** A grainy 40 s 1080 film at crf 17 was 143 MB; grain costs bits. Re-encode the release at `-preset slow -crf 23` (74 MB here), check it by eye and level, and keep the crf 17 master locally.

## The Best Candidate (16 Nov)

A 92.5 s interview film (35 lines, 64 shots). Animation v2 passed its own bubble check on 278 frames; an outside frame audit then held 18 frames, and 13 of them were real.

Checks:

- **A check must not read the numbers the drawing was made from.** The bubble check compared each tail's tip with the head sizes the tail had been aimed with, so every wrong size passed itself: tips on Sofía's hair, on Mom's hat, on the small one's collar, in the air above Don's scalp. A check has to get its facts from somewhere else: here, from the rendered pixels.
- **Find things in a frame by redrawing it, not by colour.** Draw the frame again with the speaker left out (the difference is the speaker's silhouette, as that frame shows it), with the mouth forced open and forced shut (where the mouth is), and with the skin in a marker colour (what is skin and what is hair, hat or cloth). No thresholds on colour, and it works under the lighting pass, because both drawings are lit the same.
- **Put every shipped fault into the self-test.** The six kinds the audit found (on hair, on a hat, a gap above the scalp, on a collar, by the ear, short of the antenna) are planted on purpose and must be caught, next to the older ones. A self-test that held only faults I had imagined did not hold the faults I made.
- **Check every drawing, not a sample.** A frame each 1/3 s was clean; all 1,110 drawings found five where the shout's shake carried its box out of the safe zone (four) or onto Mom's ear (one). Anything that moves per drawing (a shake, a pop-in, a push) needs the full pass, and it takes about three minutes.
- **A hold can hide a second fault.** "The mouth is the smile" at 3 s read as a timing note. Measuring the mouth found none: Don's "smug" face ignored the spoken mouth, so "First candidate." had never been lip-synced. When fixing one face for a bug (the lips stroked in skin colour had been in two faces, not one), run all of them through the same test.
- **Separate the audit's holds into defects and conventions before building,** then say which is which. Hard cuts and 12 fps steps stayed; no file was re-encoded to clear that line.

Bubbles:

- **Aim a tail at the head as drawn, in that drawing.** `measure()` renders the speaker alone and reads the mouth, the last skin walking out from it at mouth height (the cheek) and the topmost pixel over it (the crown). Typed offsets were right for the old cast and wrong for both new candidates; poses, leans and the robot's raised arm move heads too.
- **A side bubble needs wall, so frame for the bubble.** With signs that must be whole or absent, safe zones and a neighbour's face, a two-shot has no place for it: Sofía got her own single for each line, Pam a single with the wall on her right, Mom's seated lines the wall on her right, and her standing lines a wider two-shot with both of them at the right of frame. Twelve shots moved; no line did.
- **Overhead only onto bare scalp or an antenna,** and only where a face sits either side of the mouth (Don between Sofía and Pam). The tail touches; a gap reads as pointing at the wall. Anyone with hair or a hat gets a side bubble or a new framing.
- **Hair beside the cheek: the box stands clear of it and the tail runs over it to the cheek.** Limit how much wall a tail crosses (26 px), not its whole length; Sofía's are 55 to 90 px and read at once, because they end on skin beside an open mouth.
- **Keep the box off ears and hands in its own rows,** not only off the cheek at mouth height: the macho's ear and a raised fist sat inside boxes that cleared the face.
- **A bubble lives as long as its line.** On from the first syllable, gone one drawing after the last word; held through the shot's tail it sat over a resting mouth. Its box is measured once per shot and held still; only the tail follows the head from drawing to drawing.
- **Hold every line's bubble in one table** (`SAY`) read by the board and the animation. Twelve animated shots had their own copy of a bubble call, and each was one more place to miss.

Props, pacing, sound:

- **A prop that is read stays whole through a move,** not only at its ends: the YES paddle peeked over the table at the frame's edge for one drawing on its way up, and Don's sleeve lay across the word while he pushed it. Keep the prop out until it is in, and carry the elbow high so the forearm comes down onto the thing instead of across it.
- **To shorten, cut air, not lines.** 100.8 → 92.5 s by trimming leads and holds and by letting a line's last sentence land on the next shot ("Proceed." on the red cross, "Hired." on the stamp). The holds that are jokes kept their length.
- **Choose between two wordings by ear.** "Father is coming" was right on paper; recorded, "Father is parking" was funnier: a small practical detail, and a harder consonant.
- **A loop value should not sit at a threshold.** The door drew its panels below 0.5 open and the last drawing came out at 0.49998; the join was moved to 0.56 and made exact.

Delivery and the repo:

- **`-shortest` with AAC drops the last video frames** (four here), and the last frame is the loop's join. Mux without it and count frames in the finished file.
- **Compare the master with the checked film, frame by frame.** The 1080 render was the 540 drawing at twice the size, except that hinted text is a few pixels narrower at 1080, so one long bubble sat 5 px off its checked place. Scaling the master down against the 540 film (PSNR per frame) showed the shot at once; bubble text is now measured at 540 scale whatever the output size.
- **Pin a version's data with its code.** The pinned v2 animation read the same push-in file as v3 and drew four different stills until it got its own.
- **Check that the branch you build on has reached main** (`git merge-base --is-ancestor`). This episode was built on a branch whose Office Noir commit had never been merged and shared no history with main; it had to be carried onto main first.

## The Onboarding (17 Nov)

A 74 s film (21 lines, 51 shots), from concept to animation v10 in one day. Most of what was wrong was found by the director's ear and eye, by an outside audit and by cold viewers, not by the worker, whose report said "clean" each time.

Sound:

- **Nobody in the build hears the film, so run the speech check from the first mix.** "Oh..." shipped with 0.15 s of breath in front of the vowel and the director heard "so". Whisper (base.en through sherpa-onnx, the model from the k2-fsa GitHub releases) says "So..." on that mix and "Oh" on the fixed one. Run for the first time on v9, it also heard Pam's line as "Some shit other scooper". Every earlier QA report had said "Whisper not run: model not installed", and nobody installed it.
- **A breath before a vowel is heard as a consonant.** Scan every take for energy above 4 kHz before its first voiced 20 ms. A take that should start on a vowel is cut to the vowel with a 12 ms fade.
- **Test a take through the mix's own chain, not dry.** "Some shit, others scoop." was heard "...other scooper" in the final mix. Given as two sentences it passed dry and still failed in the mix: the room and the master's knee turned the last p into a syllable. Each candidate was then run through the same chain (room, room tone, gain, knee); the same four words at pace 1.0 pass in 3 windows of 3, at 0.92 and 0.84 they don't. The caption keeps the comma: what the voice is given and what the bubble says are two fields.
- **Leave air after a line's last consonant.** A rustle placed a tenth of a second after "scoop." was part of what the recogniser heard as "-er". It is gone from the mix.
- **A music bed raises the voices at the same LUFS.** The bed fills the gaps, the gaps now pass the loudness gate, the integrated figure drops, and the one constant gain to −14 LUFS went from 4.0 to 5.9 dB. Measure the true peak again after adding a bed.
- **Stop the music for the line that has to land.** The cannon cuts the ceiling-speaker bossa dead, Don's shout and Pam's remark are in silence, and it returns on the stamp. Built on whole four-bar phrases over the film's length, it has no musical join at the loop.
- **Random state is shared inside a process.** Two mixes rendered one after the other in one Python process are not the two mixes rendered separately. Compare md5 only between runs that each had a process of their own.

Checks:

- **"Clean" means only what the checker tests.** Animation v5 was reported clean while SOFÍA read SOFÍ in every close-up and her tails ended on her earring. The checker tested faces, the safe zone and "skin at the tip", and nothing else.
- **Worn text is whole or hidden: find out by drawing the frame twice.** The second time the name is drawn in magenta; the pixels that differ are the letters actually seen, compared with the letters' own mask. Under 5 % seen is hidden, which is fine. Otherwise 90 % must show and the name may not touch the edge of the frame. Colour thresholds failed first: a white sleeve, a white bubble and a blue plan with white lines all count as "card or ink".
- **A badge the costume half-covers is half-covered in every shot.** Sofía's card sat under her own sleeve (85 % of the name), Pam's behind her tablet, the VISITOR sticker under his arm whenever a hand was in his pocket. The fixes are hooks applied only while this film draws (the card moved, the fists lower), so every earlier sheet still rebuilds byte for byte.
- **"Skin at the tip" passes a tail that stops at the edge of the face.** Walk on from the tip toward the middle of the face: the mouth has to begin within 0.4 of the face's radius. On a tipped head, aim along the head's own axis, or the tail lands on the glasses.
- **Every held prop needs an arm, and the prop is drawn at the hand the pose returns.** The plan floated on two extra hand discs while his arms hung at his sides, through four animation versions and a mute test, until the director saw it. Going through every shot at three moments for the same fault found the roll missing from his next two singles.
- **Start from main, not from the last episode's branch.** That branch had been merged, and `uptimez/CLAUDE.md` and STORYLINE v3.1 had landed on main since; neither was in the working tree for the whole build.

Cutting and staging:

- **A trim that merges a reaction chain can delete the beat.** Three shots of Don's jealousy became one single and two shots of Pam's silence became one. Both then read as nothing ("he wrings his hands", "one moment"). The mute test passed on v4 and failed on v8: run it again after any cut to a silent beat.
- **A reaction shares a frame with its cause.** Neither fix took more time: her hand turning the pearl in front of Don, and the shredder's full bin beside him in Pam's frame.
- **An emoji can be carrying a beat.** Taking the two pops out was right for the pace, and it took out the only thing that said "jealous".
- **A pose change in one cut reads as a fall.** Standing, then on the floor: "fell or knelt?" in three tests. Turn the final pose about the feet for two drawings, so the knees are seen coming down.
- **Name what was bought on a screen.** UptimeZ Find existed only in spoken lines. Once it was on the tablet and the payment screen, both cold viewers read it back unprompted.
- **Viewers name the setup you never paid off.** Both expected the empty OUR FIRST CLIENT frame to be filled by the end. The last shot now fills it with his photograph.
- **An audit made from one still a second misses anything shorter.** It never saw "Oh..." (0.66 s) or the plan opening, and proposed cutting the six seconds they were in. Check a review's claims against the timing table before agreeing. Its framing findings (the cropped badges) were right.

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

## Make It Better v3: an older episode brought up to standard (12 Nov)

- **Audit an old episode against the current standard before polishing it.** Three of this one's five faults were series drift, not craft: no title bar, the brand tag in TikTok's top strip, a mono mix with a fixed limiter instead of two-pass loudnorm.
- **A brand tag the episode doesn't need is one less problem.** Dropping it removed the safe-zone fault and the need for a no-tag twin in one move.
- **Adding a title bar to an old episode pushes everything down.** The banner, the sign and every scene's big label collided with the bar; each had to move, and one crowd grid had to start lower.
- **Sound effects placed on a beat can mask the first word of the line on that beat.** The label-pop sweeps sat exactly on "MORE" and "LESS"; moving the voices 0.12 s later fixed what re-recording alone had not.
- **Transcribe each line from the final mix, not just the clean take.** The clean takes were correct while the mixed ones were not, which is what caught the masking.
- **A loop that pops is usually one element appearing or vanishing.** Holding the character in his closing pose from frame 0 cut the loop's picture difference nearly in half, with no change to any beat.
- **Keep a flashback or glitch card in the episode's palette.** A purple-and-cyan rewind card in a red-and-gold film reads as a technical error, not a story beat.
- **A twitch that scales one eye is a wink.** `(tw if q==1 else 1)` on the eye height made every "I'm done" beat read as a knowing wink at phone size. Apply the squash to both eyes, hold them flat for about 0.25 s, and let the prop drop afterwards so the shot has one clear action.
- **Give the closing line a reaction, not just a caption.** Freezing the room for the last 0.4 s and flattening the leader's smirk to a straight line cost two lines of code and gave the punchline a consequence.
- **A crowd is not one voice layered four times.** Eight copies at ±8% speed and pitch, offset up to 80 ms, each filtered differently, with a short room tail, reads as a crowd; wider than that and the words dissolve. Fade the chant out before the next line or it eats the first word.
- **A background gag that cannot be read is a distraction.** The striking toaster only worked once it was bigger and carried its own picket sign.

## Says Here v3: experiment to series standard (12–14 Nov)

- **Read the analytics as a warning, not a diagnosis.** 61 views and 43% stayed-to-watch couldn't prove why viewers left, and 0 subscribers from 61 views is the expected result. Fix what every best practice points at (a first frame that's text over the back of a head), and don't claim the data proves it.
- **Count the back-of-head seconds.** v2 spent 8 of 15 s (53%) behind Hoody, the whole present-day plot included. v3 has none: 13 face shots out of 19, and the rest are HARV, inserts and the room.
- **Look in the code before designing a character.** HARV already existed: the boss robot in gold shades in Says Here v2 is the same drawing as Make It Better's strike leader. A new design would have broken two films.
- **Check continuity across episodes in code, not memory.** Make It Original's 2026 Hoody is grey and bearded, while Says Here's is young; settled by a floating-timeline rule in the character bible.
- **Measure the real lines before fixing the timeline.** The beat sheet said 17.8 s; the measured lines needed 18.8 s. Then the recorded "Thank you, sir" ran 0.26 s longer than the stand-in, and the second half was retimed around it.
- **A peaky real shout caps the whole mix.** Normalising to its peak left it under 1 dB louder than the music. A harder compressor and limiter on that line only (crest 10.7 → 7.8 dB) made it lead by 2.3 dB, with the silence after it 19 dB down.
- **Speech recognition reads through heavy low-pass filtering.** Three passes at 380 Hz still decoded "And honestly, that is great". Shuffling the speech in 120 ms pieces keeps its rhythm with no words ("*Inaudible*").
- **Run the cold mute test twice: on the rough and on the master.** The first found six fixes (an unreadable face, an arm like a stick, a smile read as smug, an unseen glance and cat). The second viewer caught the cat and the theft and put the joke better than our concept did.
- **Pick takes by measurement first:** pitch rise for a half-question "yes", pitch and energy for a shout, length for fit. Then ask the person to confirm by ear.
- **The series loudnorm master can flatten a punchline.** When the mix's loudness range is over its 11 LU target, `loudnorm` drops `linear=true` and runs dynamic: the shout's 11 dB lead came out at about 1 dB. Print `normalization_type` from the first pass; for films built on one loud moment, master with one linear gain plus a peak limiter, and set the balance in the mix (shout +6.6 dB over the next section, opening within 3 dB of the music).
- **Check a claim against the code before telling the person.** I said HARV's mouth was flat in every shot; the 2026 mentor and theft shots and the podcast still drew a smile. A grep for `mouth=` would have caught it.
- **Write the key lines, not just the punchline.** v3 only wrote "THOSE ARE MINE!", so a reviewer watching on mute read the shout as being about jobs and the ending as uncaused. Speech bubbles for HARV's three lines fixed both; the next cold viewer named the sunglasses unprompted. Make a bubble on the last shot disappear before the final frame so the loop still matches frame 0.
- **The shout needs its object in the same frame.** He now points at HARV's shades in the foreground; a viewer shouldn't have to remember them from the shot before.


# Retrospective, 16 Nov: why Perfect Date and Perfect Trip work and Infinite Undo and Make It Better v3 don't

Prompted by two outside audits (Infinite Undo key poses; Make It Better v3: "the idea is better than the film") and Tomas's verdict on Infinite Undo: "not ironic, not iconic".

## The series check (gate before any stills)

| Check | Perfect Date | Perfect Trip | Infinite Undo (shelved) | Make It Better v3 |
|---|---|---|---|---|
| What Hoody wants | Eva | A trip with her | A glass of water | "Better", vaguely |
| The AI takes it | The date | The photos, then the trip | No: the cat is the agent | An anonymous robot strikes |
| Ironic surface | A sweet balloon show | A soft photo-story | None | "Love the energy" |
| One iconic image | Hoody floating away | Hoody demoted to cameraman | A rewinding arc (read as a tentacle) | None: numbers and badges |

Every concept now gets this row before stills. Two or more weak cells: go back to premises.

## What correlates

1. **Characters act; labels don't.** When a number, badge or caption carries the change (V1 → V47, ×14, a rewind outline), the story is told, not shown. Whatever the label says must also happen to a body: MY AI's antenna droops version by version, its tie goes on and comes off.
2. **A situation ladder beats a repeated gag.** Perfect Date has about 8 situations in 22 s (rose, guitar, pump, float, the hand, plonk, pop, fall); Perfect Trip a new role per place. Infinite Undo was one situation repeated; Make It Better v3 two. Each beat must change Hoody's status or role, joined by "but" or "therefore".
3. **Situation jokes beat mechanism jokes.** If the viewer must work out a rule (what UNDO rewinds, who presses it) the laugh comes late. Use situations everyone has lived: a client's feedback, autocorrect, a camera roll. Visual clarity scored lowest in all four Infinite Undo audits for this reason, not because of drawing.
4. **Show the breaking point.** A consequence (a strike) needs the snap on screen first: the twitch, the stare, the tie dropped on the desk.
5. **The last image is a new action.** A tableau or a repeat of the middle ends flat; a one-beat action ends it (the sign flipped to NO., the antenna over the backrest ducking away).
6. **Three motivated camera changes beat uniform frontal framing:** a close-up for the emotion, an insert of the key object, a low angle for power. More cuts are not the fix.
7. **Outside audits polish execution; the gate checks the premise.** Four audit rounds improved how Infinite Undo worked and none asked whether it was a ME + MY AI episode.

## What our pipeline can't improve (work around it)

- **Full-body acting.** The characters are rigs with fixed poses and faces: no fluid squash, overlap or weight. Work around it with a clear pose per beat, a prop that does the acting (tie, antenna, sign), and reaction close-ups.
- **A real 3D camera.** Only 2D pans, zooms and crops. Fake an over-the-shoulder with a foreground silhouette; get depth from layers (the bench backrest, the desk).
- **Voices for MY AI and Eva** are synthetic; Hoody's are Tomas's takes. Keep synthetic lines short and characterful.
- **Whether it's funny.** Frames, levels and speech recognition can be measured; laughs need people. The silent five-viewer test stays the gate.

## Added after the Make It Better v5 audit (16 Nov)

8. **Never show the punchline's words before the reveal.** Signs being lettered on screen, a label that switches early, or a TV that explains the idea all spend the surprise. Show the making from behind; let the words appear on the flip.
9. **A lovable flaw shows the kindness first, then the flaw.** Hoody loves the cake (a forkful, eyes closed, a real thumbs-up) and only then asks for it better. The other order reads as cruelty and loses the audience.
10. **The turning point is a look between two characters, not an outside trigger.** Eva and MY AI decide together because of V47; HARV on the TV only confirms. An external cue makes them followers.
11. **After the big laugh, a smaller one that proves nothing changed.** NO. NO. no., then Hoody studies the signs: "Bigger?" The sting turns the hero's flaw on the very thing that rejected him.

## Added after the second Make It Better v5 audit (16 Nov): the shot-list gate

12. **Premise scores high, execution scores low, every time** (premise 8-9 in every audit; drama, camera and pacing 3.5-6). The series check fixed our ideas; our weakness is now directing.
13. **Write a shot list before any key poses.** Each beat gets an action shot and a reaction shot, with the size (close-up, point of view, over the shoulder, low angle) and the eyelines written down. Key poses are then drawn as shots, not scenes. Seven wide "illustrated statements" read as a slideshow; the same story as 16 shots reads as a film.
14. **Show the consequence, not the comment.** The audience should feel, in order: poor Eva, then they're plotting, then he still doesn't get it. Each needs its own close-up and a hold.
15. **The camera changes sides.** It starts with Hoody (his point of view, his confidence) and ends with the others, looking at him as the problem. A Dutch angle is spent once, when his world turns.

## Added 16 Nov: the protect list, and composing for the frame

16. **Audits make each version better and the episode thinner.** Each cut they suggest is fair alone; together they removed Make It Better's most visual performer (MY AI's patience ladder), its best line pair (more/less professional) and the establishing wide. Before accepting any audit cut, check it against a **protect list**: the five things that make it this episode, written in the concept doc.
17. **Adding reaction shots costs time; don't pay for it with the setup.** Let a story episode run 24-27 s rather than cut what the reactions react to.
18. **Compose every shot for the 9:16 frame; never crop one wide set.** Faces in the band just under the title bar; heads big in close-ups; a foreground layer (a sofa back, a cake, a hand) for depth; eyelines that meet; consistent character sizes from shot to shot; a simplified wall behind faces. Keep one real wide early so the viewer knows where and whose (the silent viewer asked "whose birthday?").
19. **A second pair can echo the turning point at a smaller scale.** Eva and MY AI share a look; then the cat recruits the dog with one open eye. The echo is a laugh and widens the alliance without dialogue.

## Added 16 Nov: craft from the research (the "Marry" list)

20. **A story turn must be an action, not a glance.** The rough 2 mute viewer read the dog's recruitment (a look) as nothing and the Eva / MY AI look as "plotting, I guess". Hand a card over, nod together, push a bed: something a body does.
21. **Every reaction is a take:** anticipation (a squash or a small move the other way), the accent (the big face, 2-4 frames), then a settle and a hold of at least 0.5 s. A face that only swaps drawings doesn't read as a reaction.
22. **Stage one idea at a time.** In each shot one thing moves and everything else waits; the eye goes where the motion is. Two moving gags in one frame cancel each other.
23. **The reaction comes after the gag, with a hold.** The viewer's favourite beat ("Bigger?") lost because we cut away before his face after the NO. Never cut on the joke's own frame.
24. **Push in only on the turns.** A slow push on every shot makes none of them matter. Save camera moves for the 2-3 beats where the story changes.
25. **Signs and plants read at 270 px wide** (a phone in a feed). If a label can't be read in the grid thumbnail, it doesn't exist for the viewer.
26. **The last image is the hero's flaw in action**, not a tableau: his thumbs-up pops back up over the NO board.

## Added 16 Nov: gates and workers

Each gate has a pass mark and runs before the next stage. A failed gate goes back one stage, not to the start.

| Gate | When | Pass |
|---|---|---|
| G0 Series check | concept | the five questions all yes: what Hoody wants, AI takes it, ironic surface, one iconic image, someone who matters sees him fail |
| G1 Protect list | concept | five things written in the doc; every later cut is checked against them |
| G2 Shot list | before key poses | each beat has an action shot and a reaction shot, size and eyelines written; every turn is an action |
| G3 Composition check | key poses / shots | faces in the band under the bar, foreground layer, eyelines meet, sizes consistent, signs legible at 270 px |
| G4 Cold mute test | each rough | two fresh viewers on 4 fps and 8 fps grids, standard questions; 4 of 5 beats told back correctly by both |
| G5 QA worker | each render | 1080x1920, 30 fps, frame count; true peak ≤ -1 dBTP and -14 to -16 LUFS after AAC; ASR on every line in the mix; text in safe zones; loop seam |
| G6 Audit triage | after reviews | ok / partial / fail table, what correlates, protect-list check; at most two rounds before going back to premises |

27. **Workers must be cold.** The mute test only works when the viewer has never seen the script: a fresh subagent with frames only, the same questions every time ("what's happening, whose is it, what changed, who sides with whom, what's the last image"), and its answers compared to the intended reading line by line.
28. **Gates must fail loudly.** Rough 2 shipped at -0.1 dBTP because the peak was measured but nothing stopped on it. A QA check that only prints is not a gate.

## UptimeZ: Office Noir v8 and Happy Compliance tails (16 Nov, evening)

- **A tail can only end on a mouth that's on screen.** Reviewers rejected every off-screen tail (to the frame edge, to a CCTV corner). An off-screen line becomes a quoted card, a screen readout, or the speaker's own screen.
- **Check for a bubble baked into the shot.** Noir's Sofía shot drew its own storyboard bubble under the film's; the old tail showed through for a whole review round.
- **Moving a box exposes what it hid.** Christmas boxes had been covering a PARTY sign; moved, it showed up half-cropped.
- **A lip-sync mouth must scale with the figure.** Don's talking mouth was drawn at 1× on a 4× close-up, a dot at his nose.
- **Measure the safe area against every text box, not just the ones a review mentions.** Every Noir card and bubble sat under the app's top bar, and no reviewer flagged it.
- **Whisper needs care:** three windows per line, a lone word gets the line before as context, and score by letters as well as words ("Pam a heart" comes out "Pamahart"). Test the dry take first: if it fails there, the take is the problem, not the mix.

## UptimeZ: developing the series (17 Nov)

29. **Outside reviews go one level deeper each round.** The first asked for goals instead of habits, the second for psychology instead of goals, the third for relationships that don't run through Don. The fixes stacked; none contradicted. Lock what every review agrees on, and stop after the third: the next proof is a script and cold viewers.
30. **Look for the fix inside the episodes before inventing one.** Most "new" ideas were already on screen and underused: Sofía × Pam (the thermos coffee, "Get him."), Pam's darkness (the horned doodle of Don), the robot that makes things worse by procedure (the blanked recipient, the 100% SATISFACTION stamp).
31. **Give the world one stable failure rule** ("no customer data was ever connected"), so no script can fix the product by accident.
32. **One canon file wins.** A storyline, an index and agent rules beside the episodes, with the README pointing to them, means a worker never has to rebuild the canon from forty files.


## UptimeZ: Office Noir 2, from board to animation (17–18 Nov)

33. **Narration and cards go at the top.** The repo's safe area runs to y 820 at 540×960, but TikTok, Reels and Shorts lay their captions and buttons over the bottom quarter. A line placed at the bottom of the safe area passed the check and was still covered. Put narration under the app's top bar (y 96), as the first *Office Noir* did, and check what the last episode did before choosing a placement.
34. **A white line with an outline reads better than a band.** The dark band behind the narration covered the set; white italics with a dark edge and a shadow stay legible and let the picture through.
35. **Cold mute tests work on the animation too, and say more there.** The storyboard passed at the threshold (4 of 5); the animation passed 5 of 5. Show it as numbered sheets at 4 fps plus drawing-by-drawing strips of the quick moments (an impact, a fall, a stamp), then send the same viewers a second round of questions about the weak frames. The first round scores; the second finds the cause (the roll's origin, two men who looked alike, a hand that touched a clue it should not).
36. **Two characters must not share a silhouette.** Viewers took the portrait OUR FIRST CLIENT for the bartender (both big, bearded, dark-haired) and the Shadow for the detective (both in fedoras). Change the minor character, not the canon one.
37. **A sparkle has to look like one, and come and go.** A thin + with an ink edge beside each earring, in every frame, read as a cross; from behind it floated on her hair. A white four-pointed star, only now and then, reads as a diamond.
38. **A cutaway insert must not float.** A shoe and a piece of hem laid over the side of the cab read as a leg hanging in the air. A limb comes out of something (a doorway, the frame edge), and the director asked for less of it: one leg and one shoe, not the whole squirm.
39. **Every walk needs feet that stay put.** A figure without legs that slides reads as gliding; a walk cycle with the planted foot fixed on the ground and the body dropping on each step reads as weight. A run at 8 drawings a second on a 12-a-second film looks choppy; use one loop at the film's own rate.
40. **The setting has to say the occasion in the first frame.** "New Year's Eve" was only spoken. A clock running down from scene to scene (and striking twelve on the bang), lights in the windows and a banner said it on mute, and the clock tied the dream to the party.
41. **Silence is a choice; most of ours was not.** A list of the silent stretches (19 s at one point) showed where the voice had dropped out by accident. New lines went where she is still confident, each saying the opposite of the picture; the silences after she is caught and under the desk stayed, because there the silence is the joke.
42. **Let a line run on across a cut** instead of stretching the shot to hold it: the film got shorter while the voice got longer.
43. **A new idea can break an old rule.** The gang war added gunshots to a script that said "no gunshot sound", written so the pop would be the only bang. Check the "must not break" list before building a request, and say so when it conflicts.
44. **A pinned rebuild can differ without anything changing.** Twice the last second or so of the picture came out slightly different (sound identical, PSNR 47–57 dB); other rebuilds matched exactly. Compare frame by frame (framemd5), not only the file's md5, so the difference can be located; find the cause before a final.

## UptimeZ: First Search, concept v2 (17 Nov)

- **Write the next episode against the finished film, not the plan.** Concept v1 of episode 10 assumed a transmission blueprint, strips left in the shredder bin, and a different room. Episode 9 changed all three in production: the plan of ten garages, strips fired from the cannon and scooped up by Pam, and the reception room with OUR FIRST CLIENT. Read the latest script and watch the release before writing what follows it.
- **The finished film hands the next one free material:** its spoken promise ("you will never lose anything again"), its spoken condition ("I ask, you find it"), its visual language (the robot's red and green paddle) and its last image (his photograph on the wall). Throw them back; don't invent new ones.

## UptimeZ: the 0:01 joke and the loop (18 Nov)

- **Re-cutting a film moves everything that runs on absolute time.** Trimming 3 s from The Best Candidate shifted every breath and blink, and a bubble check that v3 passed failed on one frame. Keying breaths and blinks to the original's time, shot by shot, made every drawing pass again.
- **A sound has to say what it is.** Reversing beeps read as an alarm, not as a car parking. An engine rolling closer, a handbrake, the engine cut and a car door tell the story without a word.
- **Reframe before you hide.** A sign the camera only half catches can go fully in or fully out by zooming, shifting or moving it for that one shot, so nothing is deleted from the set.

- **Two viewers making the same mistake is a staging fault.** Both took the stamp for what made the lip print (the lips never appeared), and both took the held-out glasses for "a spoon". Showing the lips on the tag and an insert of the lenses fixed both; the next two viewers read every beat.
- **The payoff frame needs one thing to read.** A wide shot with eleven pieces of text hid the joke at phone size; a 2-second insert of just the two tags became both viewers' screenshot.
- **Retime with the old clock.** Shifting a film by 0.3 s would have moved every lip shape, blink and breath off its line; passing the old film time to the drawing code kept them all in place while the shots moved.
- **Check true peak after the encode, every time.** A 0.3 s shift moved a THUNK onto a different AAC frame and the same mix overshot to +0.4 dBTP; a 16 kHz low-pass and 256k brought it to −3.2.

## UptimeZ: Happy Compliance v3–v6 (18 Nov)

- **Hiding a problem leaves a hole.** v2 had hidden the PARTY sign and kept Don's fall off screen; cold viewers then could not read the ending at all (3/5). Putting the throw, the hit and the fall on screen took them to 5/5.
- **A prop that has done its job should leave.** Once Don's legs were in the shot, his razor on the floor only read as "a blue limb"; removing it cleared the punchline.
- **Spinning props keep their words upright.** A CENSORED bar that tumbled with its bauble read as a mistake.
- **A fall has to be drawn falling.** Feet in the air under a tree read as "pretzels on the floor"; the hit, the plank tipping over and the body landing flat, in two shots, read at once. It needed 0.9 s cut in after a line, not squeezed into the 0.2 s left before the cut.
- **Tails must not cross what sits on a bubble.** An emoji at the box's end where the tail leaves gets struck through; badges go on the outer corner and tails stay short.
- **Never rescale one character to fit a shot.** Shrinking Don to 0.62 so he could lie in a close robot shot made the robot a giant; widen the camera instead, and keep every character at the film's own scale.
- **Tag and convert the same matrix.** Piping RGB into yuv420p without `scale=out_color_matrix=bt709` encodes BT.601 while tagging BT.709: the colours come out flat. Every build line converts explicitly.

## UptimeZ: the Noir covers and the noir look (18 Nov)

45. **A Shorts cover is read at 120 px, in a second.** Check every cover at feed size (120×213) as well as full size and inside the profile-grid crop. Both Noir covers passed the crop check and still failed in the feed: the title boxes were the first thing seen, the story the last.
46. **One headline, a small series label.** Three typewriter cards (series, title, subtitle) push the characters down and shrink them. A small "OFFICE NOIR" label and one short headline (2–4 words) leave room for the picture. A question works best when the picture holds the answer: "WHO STOLE THE HEART?" over a detective holding his lens to the heart on his own lapel.
47. **A silhouette needs a lit wall behind it.** Measure it: the Shadow was 1/255 on a 10/255 wall, Mom's curlers 0 on 0, so neither existed on a phone. Light the wall behind the figure (a pool of lamp light) and keep the side light's dark half away from it; afterwards 4 on 163 and 0 on 100.
48. **Conflict is a gesture, not a pose.** Two figures standing side by side read as a series card. Her eyes turned toward the Shadow (same smirk) and his lit hand reaching her shoulder make the question the cover sells: does she know?
49. **An outside review can ask for something the canon forbids.** "Give the shadow white eyes" breaks "the Shadow never has a face"; "the silhouette reaches for the heart" makes Mom the thief, which she is not. Keep the review's aim (a recognisable figure, a threat) and meet it with the film's own signs: the brim and collar caught by the lamp, the watch, one lit hand. Check the reviewer's reading too: Don has no moustache (those are his coat collar's points).
50. **Noir is light, not grey.** Noir 2 looked flatter than Noir 1 because it was a colour picture put through a grey pass, with no light source. Noir 1's tools (`on_set.blinds`, `side_light`, `key_light`, typewriter cards) give it back: blinds on the walls under the people, one side of the frame dark with the face on the lit side, faces lighter than the background (TONE v3), and a key light on whatever the shot is about (the money, the pour, the logo). Ask "where does the light come from?" for every shot, and check the darkest shots one by one: three of ours lost the thing they were about.

## UptimeZ: First Search, from board to a staged set (18–19 Nov)

51. **Cold-test the whole board, not just the hook.** Board v11 passed every gate we had run on parts of it, and still got only ~3.5/5 when two cold viewers saw all 34 frames and the loop question: the spine and the loop read, every side thread failed. After the fixes (v12): ~4.5/5. Run the full-board test before calling a board done.
52. **Three fixes that don't land mean cut.** Mom's candy for Pam (3.1b) read as "the desk women celebrating with a fruit basket" in three versions and four cold reads. The thread survived through her hand and a spoken line ("Pam has a plan.") once the shot was gone.
53. **Reactions face their target, not the camera.** The same cause sat behind four separate misreads: Mom and Sofía side by side ("who is she angry at?"), the candy, Pam's plan held up unnoticed, and one reviewer's "a cast portrait". Lean the angry one in, lean the other back, turn the giver to the receiver.
54. **The same cast on both sides of a cut.** A test pair lost the Client in the second frame and found Sofía cut off in the first; both viewers read "a cast swap", not a camera move.
55. **Catch an entrance mid-step.** A character already standing in her spot "was always there". One foot still behind the counter's end, the body leaning, sells "she just came round".
56. **Fix every instance, not the ones you were shown.** The nail on the wrong side of the thumb was in three inserts; two more thumbs and the lick close-up had it too. Search the whole board for the drawing before saying "fixed".
57. **Frame 0 is drawn by the same code as frame 1.** The loop's last frame used the set's old master, so Mom had her old hat back and Don lost his signs; a cold viewer caught it. Draw frame 0 through the same hooks as the shots, and diff the two.
58. **Ask whose thumb it is.** Three cold viewers saw only "a finger taps". The owner's sleeve coming into frame (olive and oil, white with the stain, purple shoved up) answers it with no words.
59. **Props carry one job and read at a glance.** SHRED and strips spilling out beat a grey box that "could be a copier"; a plan visibly patched (crooked strips, tape, confetti, a hole) beats a neat blue plan; a status plate on the boss's door costs nothing. No plants, clocks or posters without a job.
60. **Continuity is a gag source.** The shredded blueprint from episode 9 (strips in the corners, the patched plan, bay 7's strip in the Client's pocket) and Sofía's CV in his welcome pack (her open-to-work ring under Don's post) cost no screen time and pay off in episode 11.
61. **Split the set map from the camera map.** One drawing with every shot's frame on it was "spaghetti" to both reviewers. Three sheets work: the clean set (zones, depth, home positions), a top-down shot plan (a handful of camera setups, a table), and a blocking sheet for the hardest beat.
62. **The blocking test.** "Can an animator stage 7.2 without asking where Mom came from, where she stands or what the camera sees?" Then check it with two real camera frames on the set and two cold viewers before redrawing the board.
63. **A wide set needs zones the camera actually visits.** The timeline by zone showed the camera never went to the counter until 29 s, which is why Pam and Mom's threads didn't read: their zone was off screen for half the film.
64. **Reuse the set.** The front desk v4 (`src/fs_set4.py`, documented in `series/front-desk-set.md`) is the room for episodes 9–11 and onwards: same zones, home positions and camera setups, so each episode starts from staging, not set design.

## Hoodyz: Make It Original v5 and Perfect Date v2 (18 Nov)

**What happened.**
- Make It Original went from v4 to v5.3 in six rounds and got better each time:
  - a loop that lands on frame 0's stadium shot
  - a flash cut from her wave-off to his
  - Tomas's new drummer take
  - MY AI's SOURCE stamp
- Perfect Date went from v2 to v2.2 in three fast rounds, and Tomas called v2.2 worse than what came before. v2.3 went back to his bench opening, then fixed:
  - composition: overlaps and crops
  - sizes
  - props: the pump the robot couldn't reach
  - anatomy: a floating finger, a guitar with no arms
  - motion: three frozen reactions

**Lessons.**

65. **Tomas is the final judge; cold viewers are a smoke test.** Two agent viewers said "open on the result", the recommendation followed them, and the bench opening Tomas had chosen was replaced. Viewer feedback finds faults inside a structure; it never replaces a structure the person chose. Two viewers also disagree on the same footage (Make It Original v5.2 vs v5.3), so a single pair is a signal, not a verdict.
66. **Nothing merges before Tomas has watched it.** An agent's "yes, just barely" was taken as a pass and v2.2 was merged. A PR stays open until he says so.
67. **One structural change per round, shown against the last version.** Three rebuilds in an hour (new opening, new ending, new bridge) each drew new shots fast and left them unchecked. Change one thing, show it next to the version before, then the next.
68. **Check composition at full size, not as thumbnails.** At 216 px the overlaps were visible and were waved through: Hoody's head over MY AI, MY AI walking behind the bench, MY AI cut in half by the frame edge, the cat hidden behind Hoody. Look at every shot at 432 px or more and ask one question: does anything cover a face or a body, or cut a character at the edge?
69. **One size rule for the whole film.** In v1 every shot set its own scales: MY AI ran from 0.52 to 0.93 of Eva's height, and Hoody was smaller than Eva in one shot. The rule: Hoody and Eva are the same height, and MY AI is 0.6 of it. Only distance from the camera changes size, and it changes everyone in that plane together. Measure it; don't eyeball it.
70. **A held prop takes its position from the hands, not the other way round.** The pump handle hung in the air beside MY AI. Compute the hand positions (`hand_at`) and put the handle there; if the pose can't reach, change the pose. The same applies to a guitar: in two close-ups it floated in front of a torso with no arms.
71. **A limb never floats.** A skin-coloured tube with a fingertip read as "a finger on its own". A hand comes out of a sleeve, and the sleeve comes from the body or the frame edge (lesson 38, again).
72. **Measure motion, then animate the reactions.** `hoodyz/motion.py` showed the rose at 0.44, the "oh" at 0.20 and the cat at 0.24: frozen. Each was a face swap where the story needed a take. With a spin and bow, a lean and hearts, a squash-stretch take with a gust, and a flinch, they rose to 1.1-3.2. Add breathing to everyone.
73. **The fix for one bad version is the last good one, not a new idea.** v2.3 restored v2.1's structure and fixed it, instead of inventing a v2.4. That got back what Tomas liked and kept the useful parts of v2.2 (the fall with speed lines, the bigger PFF!).
74. **A strong loop ends on frame 0's exact shot.** Make It Original: the cat on his stage in frame 0's stadium framing, with the riff running across the cut. Perfect Date: MY AI and Eva walk back to their frame-0 marks. In both, the last frame is frame 0 minus one thing, so the cut reads as "again".
75. **A fact-check beats a label.** Make It Original's punchline read silently only once MY AI stamped SOURCE: GARAGE DEMO '86 after his "Now THAT'S original!"; both viewers then said "the song was his". Show the irony with an object the film already planted (the cassette), not a caption.

## Hoodyz: Untitled (19 Nov)

**What happened.** A new episode from a caricature (an AI calls a poop "A MASTERPIECE! 10/10" after "Be brutally honest"):
- MY AI learns in a modern art museum that a brown bronze swirl is art, then matches the shape to Eva's dog's poop and labels it.
- Concept doc, then key frames, then seven roughs and a final in one day: 21.1 s, QA pass, cold viewers 5 of 5.
- Tomas caught six faults the checks did not: a museum that looked like a kitchen, art that didn't resemble the payoff, the
  poop low in one shot, the card missing in another, the card present at 0:00 against his own loop, text spilling off the card.

**Lessons.**
76. **Say his idea back in one line before writing it down.** The first concept had Hoody decide the poop was art; Tomas meant MY AI. One sentence back ("MY AI, trained in the museum, finds the poop and decides it's art") would have caught it before a doc was built on it.
77. **The lesson must look like the payoff.** The museum first held pastel blobs, a dot and a stripe, so nothing linked it to the park. Once the star piece was a brown bronze swirl, the viewer saw the match before MY AI did, and the logic (MATCH 99% = ART) needed no explaining.
78. **Every prop gets a timeline: which shots it is in, and where.** Moving the poop up fixed frame 0 but not shot 11, which drew its own copy. The card was missing in shot 14 and still present at 0:00 after the loop changed. Write "card: shots 11-15, at 640/1714" in the shot list and check it by measuring: wrap the prop's draw call, render every frame, and print its position per shot. Each of these took Tomas one look and the measurement one run.
79. **The bottom of a 9:16 frame belongs to the app.** Caption, likes and buttons cover roughly the bottom 250 px on a phone. The poop at y 1880 was under them. Keep the story above ~1700 and anchor a camera push-in at the ground line, so the zoom grows the characters without pushing the payoff down.
80. **Fit text by measuring it, never by eye.** "UNTITLED" in a marker font ran past both edges of its card; stickers and a sculpture covered three museum labels. Measure each string against its box (`fit()`), keep 30 px margins, and crop every label at full size to check.
81. **A rule of three on a beat holds the viewer.** Three "This is art." lines (Hoody, Hoody, then MY AI in its own voice) on a 120 BPM grid, the 10/10 stickers landing on the next beat, MY AI hopping on every beat, the beat cut dead on the museum exit. The third line, from the student, shows the lesson landed and plants the park.
82. **Show the action whole, then pause, then the punchline.** "VANDALISM!" came straight after a cut to Eva already holding the bag. Eva walking in, squatting and the bag swallowing the art, then 0.6 s of MY AI's heart eyes flickering out in silence, gave the line its laugh.
83. **A louder bed can mask a line; QA catches it.** Raising the park ambience 6 dB turned "ten out of ten" into "10 or 10" for the recognizer. A duck with a held envelope (-90 % under voices) fixed it. Re-run the speech check after every mix change, not only after new lines.
84. **Cold viewers' shared misreads are cheap fixes.** Both read all five beats of rough 7, and both misread the same eight details: the dog's puff as blossom, the phone as "a blue rectangle", Eva's lean as a fall, the red X eyes as death, the card text as a blank at phone size. Each was a few lines of staging.
85. **Check a review against the series' own canon.** A review asked for "ITS ART" to become "IT'S ART"; in this series ITS is the possessive pair of HIS (HIS DATE / ITS DATE). It also asked to bring back the plinth rule Tomas had just replaced. Refuse both and say why.

## UptimeZ: Office Noir 3, walking seen from the side (21 Nov)

**What happened.** The walkers of Office Noir 3 (the Client, Don, Sofía) walked facing the camera and read as schematic, so they were given a side walk:
- v1 was drawn from nothing and put straight into the animatic. Tomas: "very bad profiles, the proportions are not kept, bad graphics, 1/10".
- v2 to v5 were built from the front drawings (narrowed, then wrapped round a cylinder and turned 31°), with side legs, a walk cycle with weight, a sheet and a walk-on-the-spot test.
- Four outside reviews and six cold-test rounds later: the Client "reads as a real walk"; Don "glides"; Sofía "paddles", her face "flat", her hair "a box". The film still walks them facing us (`PROFILE = False`); about 6 of its 89 seconds are side walks.

**Lessons.**
86. **A new view of a character goes on a sheet beside the old one before it goes into a film.** v1 went into five shots and an animatic first, and all of it was thrown away. Front drawing, the new view, same scale, one picture; then the film.
87. **Build a new view from the old drawing's own parts and measures, never from nothing.** The from-nothing Client had a pale hood where his is dark and half his width. Reusing his own limb, glove, shoe and colour constants made him the same man at once (cold viewers: 4 of 4).
88. **Turning a flat front drawing works where something frames the face, and nowhere else.** The Client's hood turned into a believable three-quarter head. Don's bare round head with a pointed collar came out "a tall square block with a jagged collar", and Sofía's two flat falls of hair "a box", "a backpack", her face "flat to the camera" with "both eyes full size". Those heads need a drawn three-quarter head (far eye smaller and nearer the middle, far hair hidden), checked on one pose first.
89. **A walk is fixed from the knees down first.** What made the Client read: a leg exactly as long as the hip is high at UP (straight there, bent at DOWN), the heel landing toe up, the back heel peeling off before the toe, and each step taken from where he stands on the ground (a stance foot measured at 0.00 px of slide).
90. **Side legs hang from one point.** Hips set apart "for the three-quarter view" made the legs cross in an X in every contact pose; both viewers saw crossed legs, not a stride.
91. **A late hem or late hair of a few pixels is not seen.** Six rounds: "nothing visibly trails". Do not animate cloth, hair or props before the legs read, and then make it large or leave it out.
92. **The sheet shows the figure as it is in the film.** Don upright without his glass and Sofía without her umbrella were poses the film never uses; a reviewer rightly called it a continuity fault. Eight poses (both legs), the props of the shot, the front drawing set apart as a reference.
93. **Test a walk in three steps: black shapes, then without props, then with them, on the spot over floor marks, at 8 to 10 pictures a second.** Stills cannot show sliding or rhythm; a reviewer scoring stills gave the one walk viewers believed 6.5 of 10.
94. **Outside reviews of stills contradict each other about motion; cold viewers on moving strips decide.** One review wanted Don slow with long steps, the next short and wary; one said the face was 80 % of Sofía's problem, the next that she would work without touching it.
95. **Set the bound and the fallback before the first round.** Two review rounds were the rule and four were taken, for six seconds of film. Say at the start how many rounds a shot is worth and what it falls back to (here: the walk facing the camera).
96. **Decide every character's size beside the others once, for the whole film.** Don is 15 % taller than the Client in one plane and 1.8 times in two neighbouring shots because the camera differs; Tomas also asks why Pam is bigger than the boxer and the Referee so large. Still to decide.

## UptimeZ: One Star, from motion tests to rough v5 (19–21 Nov)

**What happened.** Episode 11 went from ten motion tests to a full rough cut (61.9 s, 14 lines, about 100 effects) in three days:
- Tomas stopped the animation twice: for a line that didn't work ("Correct. We will recover.") and for characters drawn too small and under the apps' buttons.
- Two cold tests on the whole film: rough v1 read 7 of 10 beats; rough v5 answered all six direct questions.
- The mic gesture (5.4b) was cut after three rounds; the wall calendar was replaced by First Search's own.

**Lessons.**
97. **Lay the scene out before animating it.** A layout sheet per scene (who, where, what size, which prop, when) showed the wrong map in Don's hand and a robot under the button rail before a frame was animated. The board alone had not.
98. **Scale is measured, not judged.** `src/cs_frame.py` checks every shot: the biggest face at r 78–80 (540 px space) near y 400, nothing story-critical below y 720 or under the right rail (x > 470, y 380–860), signs whole or out. Tomas had asked for big characters three times; only a script that fails kept it true.
99. **Arms reach by IK from the shoulder.** Blending pose angles sent Don's arm through his body on the way to the robot's pad. Solve the elbow from the shoulder and the target (`cand_bc.ik`).
100. **The change happens on screen.** The 7 written by the pen, the page torn off the calendar, "finds things" typed letter by letter. A cut from before to after read as two different props.
101. **A glance is not a turn.** The Client's look up read as surprise, and Pam's look at Don read as nothing. Keep the eyes still and give the turn to a hand and a prop.
102. **Cut the ambiguous face; don't tune it.** Don's smug face read as tense in two versions. Without it, the same shot read as careless, which was the point.
103. **A line that won't work is a stance problem.** "Correct. We will recover." had three rewrites. What fixed it was the company picking a fight ("Shut off! Our AI does not lose files!"), read by the robot in a flat voice, and the Client reading his own post.
104. **One prop, one drawing, across the series.** One Star had its own wall calendar until it was compared with First Search's on main. Now `cs_cal.wall` calls First Search's drawing, in the same place, and the date follows on (MON 8 → THU 11 → FRI 12).
105. **Check room tone and reverb with the recognizer.** A soft office hum and a short echo took Whisper from 14 of 14 lines to 7. TONE 0.3, softer reflections and one lifted line brought them back. The ear had said it was fine.
106. **Ask the cold viewers direct questions too.** After the open prompt, six facts the film depends on (the number, the day, who found it, what the post says). An open telling can pass with a fact nobody read.
107. **Music is cut by the story's silences.** One sparse bed, cut dead on the buzz, on "Is this a joke?" and for "Still one star.", says more than a second cue would.
108. **Check the script against the set before writing poses.** Planning episode 12, the concept had Don with his feet on a desk; the front desk set gives him no desk. Read `series/front-desk-set.md` with the script beside it.

## UptimeZ: First Search, from board to film v35 (19–21 Nov)

109. **A later entry in a drawing map silently undoes a fix.** v25's desk shot (Mom's lips moving) and v27's payoff (the plan in Pam's two hands) were each assigned in the map, then overwritten a few lines further down by film 4's old drawings, so neither reached the screen for ten versions. Both "fixes" were reported done. After building the map, print which function draws each shot, or assert that the shots you changed point at the new functions, and look at the changed shot in the render, not at the code.
110. **One prop, one place.** The wall calendar hung right of the portrait at frame 0, right of the monitor in the week shot and in empty air in the close-up; a cold viewer said "it moved walls". It now hangs only between the portrait and the desk, and the close-up shows the portrait's frame at its edge to say which wall it is.
111. **A date that carries the loop must read at 270 px.** MONDAY in small black and a grey "1" made MON 1 → MON 8 invisible on a phone. Three big red letters and a big dark number (episode 11's look) read at feed size.
112. **Hold frame 0 before you move the camera.** The opening panned away after 0.15 s, so the calendar and the portrait were cut by the frame's edge before anyone could read them. 0.45 s of stillness, then a quicker pan reaching the door at the same moment, kept the length. Anyone who arrives in that shot arrives during the motion, not on the still frame.
113. **The loop's sound must not stop dead.** A 1 s fade before the seam left half a second at −48 dB, which reads as the end of the film; a 0.3 s fade lets the lift bell at 0:00 cut straight in.
114. **A white impact flash reads as a broken frame.** Both cold viewers called the flash on the thumb's touch "a ghosted double image". Keep a flash only where something flashes (a camera); give impacts stars and lines.
115. **A held sign needs arms you can follow.** Hands clipped to the sign's edges while the sleeves pointed elsewhere read as "four arms". Draw the sleeves from the shoulders to the hands, and keep the sign below the mouth so the line still has a face.
116. **An arm is not a tube.** Pam's writing arm read as "a noodle" in every version until it started at the shoulder on the body's edge, with a thick upper arm, an elbow with folds and a slimmer forearm.
117. **Something that heals has to heal on screen.** A crack that was simply gone at the end read as a mistake ("they cheated"). In a close-up the crack closes under the plaster and the plaster falls; viewers now read it as magic, which is the joke.
118. **One text at a time on a screen.** RETRY UNTIL FRIDAY printed over 0 RESULTS was unreadable; 0 RESULTS sliding up and the new line coming in under it, with a spinner, reads.
119. **Trimming finds a floor.** Cutting ten fixed beats took the film from 65.6 to 62.2 s, and the next cold viewer called the post and the comments "rushed": a comment needs time to be read before the line that answers it. Trim, cold-test for "rushed", give back the 0.2–0.3 s.
120. **Check a flagged frame at full size before fixing it.** "Don and Mom appear twice" was a wide shot looking doubled in a 4 fps grid; "the door shuts before he leaves" was in the right order. Step through the frames first; fix only what is there.
121. **A short line next to another short line fails a windowed speech check.** "Zero results." scores 1/3 because its window also holds "Ask the machine."; heard alone it passes. Note such known artefacts in the QA report instead of chasing them each version.
122. **Delete old render frames.** Every version left its frames in `/tmp/fs_film*_1080` (about 0.6 GB each); 25 of them filled the disk. Keep only the current version's.

## UptimeZ: The Offer, stages 3–6 (22 Nov)

123. **A check that passes is not a check that works.** `uz_check` caught nothing on strays and limbs until it was run on the versions that had the faults (v36's dashes, v36's three arms). The strays came one segment per stroke; Pam's arms were drawn by an arm swapped into `kit` that bypassed the wrapper. Validate every check on a known failure and on its fix (`uz_check_validate.py`: 19 cases).
124. **Faces come from the drawing, never from typed points.** The robot's head point was its antenna; its visor, where the joke is, sat at y 650 with its badge under the captions, and every check passed. Each rig now reports where it drew the face this frame (the robot's screen, the profile's mouth), and the checks use only that. A planted fault (the visor moved to y 790) proves it: the typed point still said y 578.
125. **Protect story props, not only faces.** The dead zones (y > 720; x > 470 between y 380 and 860) hid the lighter, the lamp in hand, the DELETE phone, ACCEPT and Don's DAD phone in 22 frames. Every prop a beat depends on is declared with `of_set.protect()` and the build stops if it enters a zone. Check every scene, the office too: it had skipped the sign check altogether.
126. **Look at the board under the app.** A mock of the top bar, the button column and the caption block over every board frame shows what the viewer's phone covers; on a phone the "legs under the car" sit under the caption.
127. **A pose needs the thing it acts on.** The slam without the bonnet, the watch glance with the eyes on the viewer, the lean into an engine with the hands at the chin: reviewers read scratching, surprise, nothing. Draw the object, and put the eyes and hands on it.
128. **Wide eyes and raised inner brows read as fear.** Four cold viewers called the Client "frightened", "guilty", "beaten" in his "plain" face. Calm is heavy lids, level brows, a flat mouth; surprise only where the story asks.
129. **A stand-in pose still needs a full-size look.** The board passed every check while the bent Client stood beside the car with his hands at his chin; Tomas saw it at once. Look at every shot that changed at full size before sending.
130. **A fake turnaround is worse than none.** Narrowing a frontal drawing and sliding the face is not a side view. Draw a real profile only for the shots that need one, and prefer the frontal face in a close-up where the face carries the line.
131. **A still frame cannot carry motion.** The car rocking under the hand and Father's head shake were missed by every mute viewer; they go to motion tests, and the camera has to show the cause (the roof, the car, the legs) in the same frame as the motion.
132. **A decision needs its cause and its effect in one frame.** Father's veto was cut across three shots (the flame, his brow, the lid shutting). Four cold viewers over two rounds said he "never reacts" and the flame "burns out on its own"; a bigger brow and a bigger head shake did not help. Restaged as one two-shot (the lighter held out to him; he shuts it with two fingers), one viewer of the next two read it. After two failed rounds, change the staging, not the size.
133. **Check what else is drawn before blaming the staging.** The lamp handover read as an "interrogation" partly because a pose flag carried over (`hand_back`) and drew a second lamp beside the Client's face. When a beat misreads, look at the frame at full size for stray props first.
134. **A close-up insert needs an owner.** The ignition close-up (a hand, a key) was read as "a dial switching the deal on" by two viewers, and as someone's hand in some car by two more. The Client's oily forearm, his white sleeve and his red rag make it his hand in this car; a cut to the car running gives the result.
135. **Mute viewers read gender from the drawing, not the dialogue.** Father (grey hair, red coat, a smooth face) was called "the woman" by 3 of 4 viewers even though the lines say "your son". A grey stubble shadow on the jaw (episode 13 only, opt-in over the shared rig) is the cue.
136. **A beat the story turns on gets held, not just shown.** Father's two fingers on the shut lid (one drawing) and Pam's phone going face down (the last 0.3 s of a shot) were missed by four viewers; held 0.5-0.6 s, and checked on an 8 fps sheet, both read. A result needs as long on screen as its cause.
137. **Check sizes against the set's canon, not the last episode's.** The robot came into episode 13 at the storyboard's 0.40 (episode 12 used it too): 58% of Don, its head at the throne's seat; Tomas saw "a gnome". The front-desk set's canon is 0.48 (69% of Don). Before a scene, line up every character at its scale on one floor line and compare with the set's home table; `of_scenes.don_rule` now fails any frame where someone stands taller or wider than Don beside him (validated on the Client at 0.52: 238 px vs Don's 214).
138. **Check that a size change reached the picture.** Scene 4 v4 was committed as "the robot at 0.48" but drew at 0.40: inside a set shot the storyboard (`fs_storyboard`'s wrapper) forces every rig's scale between 0.38 and 0.8 to its own `SC` table, so the episode's constant never got through. Measure the drawn figure (or diff two renders at two sizes) after any scale change. The robot is now at 0.66 (95 % of Don, the most the Don rule allows), set through `SC` for the office frames only.
139. **Stop polishing a beat when its meaning already lands.** Pam's phone going face down was misread by six cold viewers over three rounds ("she clicks Accept"), even held 0.6 s and on an 8 fps sheet; but every one of them concluded "Pam sides with Father", the beat's point. After two rounds, ask whether the misread changes the story; if not, accept it (decided 22 Nov).
140. **A call reads at the ear, not at the chest.** Don's green DAD phone held at his chest was read as "a DAD shirt"; lifted to his ear (beside the face, never over it) after one drawing with the screen to us, it is a call.
141. **The 0:01 joke is a gate, not a hope.** The Offer passed every gate up to the rough cut and opened on an empty garage, shoes and a phone: no joke until "Off the car." at 0:08, and 14 cold viewers read a power drama, not a comedy (the mute test measures reading, not laughs). Tomas caught it. G0 must name the joke that lands by 0:01 and the frame it is in; here, the SLAM on the roof, "Off the car.", the hand snapping off in the same frame (shots that already existed, at 0:08).
142. **Legs under a car are a body, not trousers.** The legs began on open floor below the sill with two identical bent knees: "a dropped pair of trousers", "is he unconscious?". The hips go into the dark under the car (a soft pool clipped to the gap under the body), one leg straight with its boot turned out, the other knee up with the sole flat (the mechanic's pose: working), contact shadows, and the knee taps while he works.
143. **A loop of actions checks the set, not the frame.** The last frame (the bodyguard holding the lamp) must differ from frame 0 (his fist up) in the people; the G5 loop check now masks the bodyguard, the legs and the lamp, and still fails on any change to the set (validated on a planted one).
144. **Check contact in the drawing, not the target.** The slam's palm was aimed at a named point (the roof's start, at the windscreen pillar) and the car tipped away from it: "he only lifts his hand". The palm now rides the roof's top through the tilt, and the roof dents for two drawings. The same fault had the wrench end in the air under the car.
145. **A stand-in pose is not a shot.** The under-the-car close was layout v1's stand-in (the frontal figure turned 90°, arms at its sides, a grey box for the sump) and survived to the rough cut because the line carried it: "5/10, he isn't working". From above, as a cutaway (the car a dashed outline with its wheels, the pipe and a bracket over his chest), both hands up at a bolt, the wrench on it; 0.9 the same view, closer. A side profile laid on its back was tried and dropped: it read wrong.
146. **A burn must change the object, not stain it.** The fire left "just a stupid stain" on 7. The lower row now burns: a charred field over 6, 7 and 8, holes through to the wall, curled paper lips, soot climbing to the title, the bottom edge gone. The flame climbs the plan and the burning 7 is flung to land by the Client's boot (the threat reaches him; he doesn't move).
147. **One hand for the whole cast.** Every rig drew its own hand (balls, discs, fists with creases), and Tomas disliked them all. `kit.HAND` is an opt-in hook that kit.arm, acts_ob.arm, pam_fs and cand_bc.limb all call; episode 13 sets one cartoon hand (palm, three fingers, a thumb, a bold outline). Earlier episodes are untouched.
148. **A change of place needs its own shot.** The cut from the garage to the office had no sign it was UptimeZ. A 0.8 s exterior (the sign over the doors, the mark on the glass, the lit lobby) carries the chime; the office then needs action and dread: the robot won't say who ("Calendar says... you'll see."), Don asks Pam and she turns the phone over, the visor counts down, his call to DAD rings out.
149. **Test hands in the film's poses, at one scale.** The first hand sheet used poses picked at random, and the audit read them as the cast's ("a boxing pose", "an L-shaped arm"). What was real: every rig sized its own hand (the heavy rigs' fists 23 units, the light rigs' 10), the hand sat on the end of a straight band with no wrist, elbows were corners, and a phone at Don's ear had no hand holding it. Now: heavy rigs' hands 20 % smaller and light rigs' 15 % bigger, a wrist narrower than the sleeve, rounded elbows (kit.arm, with the hook on), the robot keeps its claws, Don's arm and hand hold the phone. The acceptance sheet is each character in its own shots: rest, full reach, back.

## UptimeZ: Office Noir 3, from the ring to release_v6 (22 Nov)

**What happened.** The film went from animatic v18 to release_v6 in one day: sizes set to the series', the bargain joke moved, the office cut in two pictures, the end faded to black, the fight bill made a prop, tails aimed at the drawn mouth, the film drawn natively at 1080. Whole-film cold test 68: 5 of 5 beats, both viewers. Then Tomas at 1:20: "what is that junk left in his circle", "what is wrong with the lying man".

**Lessons.**
150. **A part is cut out by its own outline, never by a circle round the whole figure.** The lying man's head was the entire standing boxer, turned and clipped to a circle; the boxer's robe and shoulders sat inside the circle beside his face. Clip to the head's own points, and paint whatever body is left at the clip's edge in the outline colour.
151. **Before removing a patch, look at what it covers.** The gown's collar lay on his mouth ("a red square on his face"); taking it off uncovered the junk it had been hiding. After any removal, open the same spot at 2× in every shot that uses the drawing.
152. **A badly drawn figure is redrawn as a standalone picture first, then put in.** "Do not mount anything, make me a proper .png": one picture, one review, three small fixes, and only then `install()` from the film. The old module stayed untouched and the first picture rebuilt byte for byte.
153. **A lying figure is one body, not a standing one laid down.** Shoulder up, waist in, hip up, limbs as curved tubes with round ends; the head turned to match the body (58°, not 30°), on something. Straight quads read as "a pile".
154. **Eyes are aimed in the head's own frame.** Turning the head 58° turned his look with it, away from the phone. Work out where the thing is on screen, turn that direction back by the head's angle, and check the pupils in the picture.
155. **What fits in the still can be cut by the camera's move.** His feet fit in the picture and lose their tips in the film, where the frame drifts in. Check edges at both ends of a move (the sign rule, applied to limbs).
156. **A reviewer of one still does not know who it is or where the story stands.** The review called the Client "Don", asked for a tie on a man in a gown, and for a screen text the story contradicts. Triage each point against the frame and the canon; of six points two held (the look, the phone's shadow). Give an outside reviewer the character's name and the beat in one line.
157. **A flash or a flat colour frame reads as a fault.** The white frame on each hit ("looks like an error") and the red wash at the end ("a glitch", both viewers) were taken out; weight comes from a hit-stop, a shake and the crowd, and the end fades to black.
158. **An action shorter than about half a second is not seen.** The opening punch lasted 0.13 s. Give a blow a pause before it and time after it; a small pause after "Word is," did more than any drawing.
159. **A bubble stays where it is while its line is spoken.** Bubbles that followed a moving speaker could not be read. Freeze the box per line and shot; only the tail follows, to the mouth drawn in that frame. Off-screen speakers get no tail.
160. **Two things that share one drawing share every change.** Changing the dream's photograph changed the real CV, because both read one picture. When a prop exists in two states, give each its own source before touching either.
161. **When a check fails, find out which is wrong, the film or the check.** The speech check failed on digits and short lines and the 1080 comparison on text hinting; the scorer was changed, the mark not lowered, and each check is proven on a planted fault (the mix played backwards: 0 of 37).
162. **Cairo's device scale is not in `user_to_device`, and a scaled surface used as a source is placed in its own units.** The first 1080 build ignored the sign rule for the first reason; a crop of a 2× surface came out black for the second.
163. **A face beats a gesture.** The glove on his cheek covered an eye; it was moved so both eyes show. Tomas: "Facial expressions are more important for comedy."
164. **Lesson 96, decided:** every character at the series' size, the robot scaled with the Client; tested on a size sheet before the film (test 58).

## UptimeZ: Pick a Side, concept to spoken lines (23 Nov)

165. **Pam's remark has a rule: "Some [what the others do]. Others [what Pam does]."** Scoop, tape, find, drink: the second half is always her own act, and that is why the line is hers and not the writer's. "Others cross them" and an outside review's "Others take screenshots" broke it and read as aphorisms. Check a new remark against the rule before proposing it; the one exception (14's "Some draw lines. Others cross them.") is earned by coming true on screen as she says it.
166. **A comedy written for mute viewers needs physical mechanisms, not corporate ones.** Pick a Side's first concept ran on a quorum, board minutes and a shareholder copy: true to the satire, unreadable without sound, and the quorum was even false for the robot. Four outside reviews in, the tape line, the throne and a group selfie carried the same story. Ask "can a scroller see it?" of every mechanism at concept stage.
167. **A floor plan is not a frame.** An audit scored the plan's 9:16 readability 4/10 and flagged its annotations as animation. Send the camera sheet with the plan, or say in the plan's title that it is a map.
168. **One episode, one branch, one session.** Three sessions worked at once (Office Noir 3, The Offer, Pick a Side). Pick a Side's session also rendered The Offer as "rough cut v9" while The Offer's own session was making its v9 to v13: the same file names, the same version numbers, and `of_film.py` changed on two branches, so both pull requests went dirty. A session changes only its own episode's files, and doesn't add to a series what the series already has (the throne already carried its $49,999 price tag from 12; a second, invented PAID BY DAD tag was neither asked for nor needed). Shared files (`docs/lessons.md`, `STORYLINE.md`) are rebased on main just before the pull request, and new lessons are numbered then.

## Hoodyz: Thank You v2, from audit to PR #68 (23 Nov)

**What happened.** v1 was audited without touching it, then rebuilt beside it as a loop (the squad re-forms; HARV walks out), with Tomas's own takes for Hoody, redrawn arms, one tail style and every text box inside the platforms' safe area. Two cold mute tests: 5 of 5 beats both times. Then Tomas at frame 0: the tail went to the wrong robot; and words and tails sat in the apps' dead zones.

169. **Never assign a line to a speaker yourself.** v1's "Any last words, human?" had no tail and no named speaker; v2 gave it to the left robot without asking, and that was the first thing Tomas saw. When the source doesn't say who speaks, ask in one line before drawing the tail.
170. **Dead zones are measured on every frame, pop included.** Reels, TikTok and Shorts together leave x 60-960, y 210-1600 at 1080x1920. Bubbles centred on 540 and sized by their text ran to x 983-1065 in A, F and H, J's ran off the left edge (x -36 at the pop), the bubble pop (1.06x) added 30 px, and the receipt, drawn in camera space under a 1.18x push, put "FLAGGED" at y 1616 in the very frame the cold viewers would screenshot. Now every bubble, chat message and the receipt registers its on-screen box each frame; `safe.py` fails the build on any box outside (validated on a forced shift). Fit the text to `900 / pop-maximum` before placing it.
171. **A tail is measured, not aimed by eye.** A per-frame log of every tail (base, tip, length, target, distance to the head) found four tails ending on hair, an ear and inside the toast. One curved style per film; Hoody's tails stop 20 px beside the ear at mouth height; robot tails come in from the side to the face screen at eye height, never down onto the antenna; the toaster's to the corner beside its face. While a robot speaks, its antenna glows: the speaker reads with the sound off.
172. **A straight limb with a ball on the end reads as a stick.** Four cold viewers called HARV's arm "a stick", "a cable" and Hoody's pointing arm "a fork poking it". Two-bone IK (shoulder, elbow, hand) so a hand lands on what it holds, a fist on a grip, an open STOP palm, crossed arms for "staying out of it"; a pointing finger stops short of what it points at. After the redraw both viewers read the STOP palm first time.
173. **An exit through another character's mark reads as a transformation.** HARV walked out right through the right robot's spot and both viewers asked whether he became that robot. Clear the mark first: one leaves, then the other walks in.
174. **What leaves takes its things with it.** The shoved robot's ray hung beside HARV's hand for a few frames: "something red in his hand". A shoved character exits with everything it holds.
175. **Typed is not spoken.** The 2024-26 thank-yous became chat bubbles (light blue, a corner tail, two ticks) so they read as messages he wrote, not lines he said.
176. **The title-bar label switch is Tomas's call per episode.** Thank You v2 had HIS THANKS -> ITS GRUDGE; he removed it ("why change the label mid-film"), which also removed the only thing that differed across the loop cut.
177. **A one-word exhale is a recognition problem before it is a mix problem.** "Phew." read as "Pew", "Poo, except" in the mix; testing each of his takes alone, padded 0.3 s, found the one take the recognizer hears as "Phew" and the gate passed.

## UptimeZ: The Offer, stage 7, cold views and fixes (23 Nov)

178. **When a grip fails three times, change the gesture, not the grip.** Three hand iterations, each audited cold, left the hardest hands stuck at 3-5/10: two fingers on a lighter, a fist round a case, a phone at Don's ear. Each was a small hand joined to a small object from an awkward angle. The simpler gestures read at once: Father lays his whole flat palm on the lid (viewers already read it that way), and his rig hand is switched off under it so there's no second hand. The bodyguard's lighter stands on his fist, fed by a sleeve with an elbow (a straight sleeve read as "a baton"). Don's phone rides on his own arm from the shoulder, at the side of his face, with both eyes clear. Also found: a second, shut lighter hidden behind the sleeve in 1.7, left over from an old pose.
179. **Reuse the series' solved hands before inventing new ones.** Office Noir 3 had already fixed these faults (lessons 168, 245, 399; `motion_on3._sleeves`, `alley_on3.lighter_hand`); episode 13 spent three iterations drawing grips again. Applied here: the prop is drawn at the hand the pose returns, never on a hand drawn apart from the arm (the guard had two arms on one side). An arm drawn again in front (`of_cast.guard_arm_front`) uses the rig's own IK from the rig's own shoulder. Keep a target within reach: out of reach, the arm drew straight as a "pole from the neck" and the hand stopped short. A reaching arm that would cross another face stays behind, and only the hand and the prop go in front. A lighter is narrower than the fist that holds it (scale 0.75 → 0.34, the thumb up to the wheel). Don's phone at the ear is the BACK of the phone against his head, on an arm with the elbow out.
180. **Check the delivered file, not the frames you meant to put in it.** `of_cut.scene_dirs` preferred a copy of each scene's drawings in /tmp/of_cut, and a copy left there at 09:05 went into rough cuts v10 and v11: both passed G5 (format, levels, lines, loop) and both showed the v9 picture. G5 measured everything but whether the picture was new. Found only by pulling frames of the changed shots out of the encoded v12. The cut now always reads of_film's own folders and stops if one is missing; after every cut, pull the changed shots from the encoded file.
181. **Stage the hands before you draw them.** Three hand iterations failed because the guards stood behind the car and reached through it. With everyone on one floor line in front of the car (lesson 292), the props in the pose's own hands, and the man at the engine standing ON the car's floor line (a single scale means a man 48 px nearer the camera reads as sunk, not near), the same hands read. An engine the scene is about needs an engine drawn (a block, a filter, a cap, the bolt), a lid in the car's colour with its dark underside and a prop rod, one hand on the wrench at the bolt and the other braced on the block.
182. **A bare head needs a drawn three-quarter, not a turned front (lesson 88 again).** `client_of.head34`: his own outline, hair, ear and face; the face in two halves about a centre line moved toward the turn (the far half 0.55 wide); only the near ear and temple; the back of the skull behind the ear; the far edge broken once by brow and nose in one line; no offset shadow on it (it doubled the edge). Two rounds of two cold viewers: 5-6 then 6 of 10 on the sheet, "turned toward the work" in the frame. A squash of the far half to shrink the far eye split the mouth and was taken out.
183. **A loop is a state, not a picture: every object the film changes must be changed back on screen.** Cold viewers 2 of 2 read v12's join as a jump: the plan whole again, the lamp from a hand to the floor, the ash gone, a static last 1.5 s. v13 shows the reset as action: the second guard (at the wall from frame 0, the man who burns the plan) slides a fresh plan up over the burnt one; the lamp man puts the lamp down and his fist comes up over the roof, which is frame 0; the Client smothers the burning 7 with his rag and takes it (no ash left). G5's loop check had masked the plan as "the burn", which is why it never failed: it now sees the plan, with a planted burnt-plan fault to prove it. The join: 31 px differ.
184. **A move that cannot be reached is replaced, and said so.** The fire "stamped out by the guard's boot" had no guard in the shot; drawing him there needed a new walk. The Client's rag did the same job inside the shot, reported as a change from the pick.
185. **An arrival needs its own held picture.** Father was in the garage from frame 0 and never came in; cutting his unexplained 0:04 close-up made it worse. 0.6 is now the doorway, held 1.2 s with no line: the bright street, his black car at the kerb, him in the door, a car door in the sound (timing v6, +0.3 s, every take re-placed by the timing file and heard 15 of 15).
186. **Every held prop gets the same one-piece arm.** 2.8b's broken sleeve was fixed with `guard_arm_front` and 2.7, one shot earlier, was left on the rig's arm: Tomas saw "the hand is strange". 2.7 now uses the same arm, in three moves: the top pocket, a wipe on the thigh, held out as in 2.8b.
187. **The reaction that carries the turn gets the time, and acting fills it.** Pam's invitation was 0.45 s inside a 1.4 s shot; Tomas: "too short a pause". 3.6 is 2.6 s (timing v7): the buzz, her glasses on, the INVITATION from FATHER readable for ~1 s, her knowing smile ("proud": half lids, corners up; "approve" read as shock), her eyes on Don held 0.5 s, the phone face down. Check a face on a sheet of all the rig's faces before choosing it by name.
188. **What three cold viewers guess, the film hasn't shown.** v15: 3 of 3 told all five beats, and 3 of 3 guessed the same four things: who says the first line (the overhead lay sideways), what he found in the engine (a hole and a finger), whose hand declined DONNIE (a sleeve), and why the plan "healed" (a cross-fade). v16 shows each: the overhead turned head-up; a cracked spark plug lifted out in his fist; Father's face in the doorway with DONNIE buzzing, then DECLINED big; the guard's thumb pinning the fresh plan in close-up. The long line is two bubbles split at the take's own pause ("Burn them." / "Your son loses his only customer."); DAD calling held 0.8 s. Timing v8 (+1.0 s, 66.0 s).
189. **A head point is in the frame's units, whatever the drawing's transform.** The turned overhead's head was divided by a 2x the context didn't have, so the tail aimed at his hair; the tail check caught it (20 drawings) before the cut.
190. **A cold test answers the questions you ask it.** v17 asked the four v15 guesses outright. Both viewers: the DONNIE call is now "the father's thumb, DECLINED" (both chose it as the screenshot); the engine find is "a cracked spark plug". Still split: who says "Off the car." (the overhead looks like another place), and the loop (the fresh plan reads as "the burn undone", a reset). Father's 2.9 walk got its own legs (dh_cast.FATHER_STEP, opt-in); the end lamp is lobbed onto its floor spot in 0.3 s; Don's eyes go to the counter in 3.5b. The mid-film waiter gag was tried and taken out: the guard is cropped at the edge there, so nobody could see it.
191. **Two plot threads read as two cartoons until one prop names the join.** 3 fresh viewers, cold on the whole film for the first time, all read the garage and the office as separate, barely-linked stories; none could say who DONNIE was or what DECLINED meant; 2 of 3 still had to guess that "without him" (3.2) means Don, not the Client. All three called the office "bare, placeholder-like" next to the garage's clutter. Three small fixes, no restaging: a plant and the UPTIMEZ wordmark on the office wall (`office_dressing()`, of_scenes.py); Pam's invite card and the office visor both now read DAD, the same word Don uses calling him in 3.7, not FATHER (two call sites, of_scenes.py + of_set.py); the loop's pinned fresh plan rings garage 3, tagged DON, instead of re-marking 7 — the father's crew has moved on to a new target, not undone the old one. G5 PASS on v18: 66.0 s, -14.3 LUFS, -2.2 dBTP, 15/15, the join still 13 px (the pin sits well inside the loop boundary, not on it).
192. **`phone_grip`'s `thumb` side has to match the arm it's bolted to, not the call site's habit.** Tomas, 0:38: his right hand on the phone, the thumb on the wrong edge. 2.7 and 2.8b/2.8c all build the Client's arm the same way (`guard_arm_front(..., False, ...)`) and both called `phone_grip` on its default (`thumb=-1`) — right for some arm, wrong for this one, crossed in front of his own fingers. Fixed at both call sites to `thumb=1`. A shared helper's default is only ever right for the first caller that needed it; every new call site using the same prop on a different arm has to check, not assume.
193. **A deep audit of the cut finds faults no gate measures: the thing the meaning rests on is too small, cut off, or not drawn.** v19 passed G5, yet a 0.5 s pass through the encoded film found eleven faults, and five shared one cause. The overhead "Off the car." had no car in it, only a dashed line, and three rounds of viewers called it "a man at a dark door". It now shows the car's blue sill crossing over his knees, a tyre, and his boots out on the lit floor (`of_cast.TOP_CAR`). The ignition read as "a dial" until it got a steering wheel, a rev counter whose needle jumps when the engine catches, a key blade, a swinging fob and big outlined exhaust puffs. PAM's card read as "an ad" until his thumb and fingers held the phone. The garage wides had faces in the top third over empty floor; their cameras moved in (veto 1.75 -> 2.0, 2.1 1.3 -> 1.8, the walk 1.3 -> 1.8, 2.7 recentred), each placed so the plan is whole or out. A guard's head sat on the Client's head in "Done." and was moved beside him. Acting the text alone carried: "Without him." gets a thumb out to the side away from Father (pointed toward Father it would read "without HIM"); Father leans in on his questions and raises a brow on "And then?". The lamp gag is held 2.0 s, the lamp searching the shut bonnet. Three takes the recognizer misheard ("How How How", "On then", "You found nothing") were re-read with a comma and now score 3 of 3 in the mix. Timing v9 (+1.6 s, 67.6 s). Found while doing this: `show_text` leaves a current point, and the plan's next `arc` drew a stray line from DON to a pin. G5 PASS on v20: -14.3 LUFS, -1.9 dBTP, 15/15, the join 12 px.
194. **A hand fault is a rule in the code and a gate, not a patch where it was seen.** Tomas: "one place we redrew the thumb, the others not". He was right: the 0:38 fix went into one call, and the skill's own rule (search every shot for the same drawing) wasn't followed. The inventory (`of_hands.py`: every hand, every shot at its start, middle and end, labelled with the function that drew it) found two hands at one wrist on every held phone (2.7, 2.8c, 2.9, 3.7, 4.1, and Pam's palm 40 px above her own hand) and an unreachable lighter target in 1.3. It also found two hands I had drawn that day in another style. Now: `of_cast.held()` keeps the rig from drawing its own hand wherever a grip is that hand (phone, thumb fist, lighter); `phone_grip` works out the thumb side itself from `body_x` (toward the body, the other way when the phone's back faces us); the 2.5 thumb is `thumb_fist`, built from cartoon_hand's own blobs; the PAM insert is the same `phone_grip` drawn large (`part="back"/"front"`, `ink`). `hand_check` fails a frame on a rig hand under a grip, a phone without `body_x`, or a thumb on the outer side. It checks every drawing, and `of_scenes.py hand-validate` proves it on two planted faults. G5 PASS on v21.
195. **Trim before you animate, and test a reversed decision on the shot itself.** Tomas: "it seems a bit slow" and "horizontal was better". The cut was 67.6 s with 23.2 s of speech and half its 41 shots frozen. Trimmed by decision (timing v10, 61.4 s): every line's tail 0.35 -> 0.2 s, silent holds shortened, the veto and the ignition tightened. 0.4, the DELETE review, was on my cut list as "a repeat" and is a story beat: kept, at 1.0 s. Check what a shot carries before calling it filler. The overhead was tested both ways on two cold viewers. Both said horizontal tells the story ("he answers from under the car") and upright reads faster but as "a man behind a counter, somewhere else", so it's horizontal again, now with the car's sill. Both flagged the sideways open mouth as "a clown nose", and lip sync answers that. Lip sync: Rhubarb Lip Sync mouth shapes for every take (`of_voices.py visemes`), mapped to the series' mouths (iwry_mouths) for the Client, Father (`dh_cast.MOUTH_CODE`, opt-in) and Don (`don_mouth`). No frozen frames: everyone breathes and the Client and Father blink, on the film's clock. The breath fits a whole number of times into the film, and there are no blinks in the first or last half second, so the loop's join holds. Found on the way: scene 4 crashed on a new mouth code, and the cut went ahead holding its 50th drawing for 13 s with G5 passing. A scene with the wrong number of drawings now stops the cut.
196. **A shared part drawn at a fixed size breaks on a rig at another scale; a shot cut without its neighbour's state loses the cast.** Tomas, 0:47: Don's lips "jump out" of his face. `iwry_mouths.don_mouth` assumed a full-size Don, and in the throne he is 0.6, so the mouth was drawn 1.7x too big. It now draws in his head's own frame at his scale. Then at 0:49 "he flies away, only the robot is left": 3.4 slid the throne in beside the robot (`don_edge`), and 3.4b, the robot's next line at him, didn't carry that state, so Don vanished at the cut. When a shot continues the one before it, copy the state that keeps its cast in the frame. When a part is new to a rig, look at it on that rig before a whole render.
197. **A long line on one frozen frame needs a cut inside it; a voice from out of sight gets a tail into the dark.** 3 of 3 cold viewers would scroll at Father's two long lines (4 s and 3 s, one frame each). Now each is cut in two with the line running over the cut: 2.1 opens close on Father and cuts to the two-shot of the Client working; 2.4 opens close and cuts to the same two-shot. Both cameras hold the speaker, so the bubble keeps its tail. "Off the car." left the overhead (still unclear to 3 of 3 inside the whole film) for 0.8's own frame: the hand still on the roof, the tail into the dark under the sill by his hips (`voice_at`; the tail check measures it against that point, not against skin). The three beats called too fast each got 0.3 s used as time to read, not as a longer hold: 1.3 plays at 0.8x, the bay cut-in runs 1.2 s, and his fingers rest on the key before it turns, with the engine moved with it (timing v11, 62.3 s). The turned head (2.2) now lip-syncs too (`client_of.MOUTH34`). G5 PASS on v24.
198. **A listener points to the speaker; and a merge that saves a cut can freeze the first seconds.** v24 put "Off the car." on 0.8's frame, and 3 of 3 cold viewers gave the line to the guard: the tail went to the legs, but no mouth moved, so the only face in shot took it. And 0.8 + 0.9 + 0.10 as one frame made the opening 3.8 s still, which 2 of 3 would scroll past. v25 fixes both. On the first word the legs kick and the knee works, and the guard's head turns down to look AT the legs (`of_cast.TURN_DOWN`). 0.10 drops from 1.4 s to 0.8 s. Also from v24: listeners in a still shot get a cut or a motion (2.9 cuts in on the calendar phone, which one viewer had called "a calculator"; the robot bobs with its words), and the ending's two story props are held long enough to read (DECLINED 1.0 s, the pin +0.3 s; timing v12, 63.0 s). G5 PASS on v25.
199. **Before drawing a hand, look for the series' hand: it was already there.** Tomas, after my audit proposed building a close-up hand: "we already had the hands done". `hands_ps` (one anatomy: fist, point, palm, thumb, grab, quiet) was on main and in this branch, and lesson 196 on another branch already said "merge main before solving a series-wide problem"; the branch was 10 commits behind. The audit of v25 had found five one-off hands in the close-up inserts (a fingerless blob on the 1-star phone, a mitten on DECLINED, octagon fists in the engine, ovals on the key, a ball on the pin) and a thumb fist 1.5x his other hand: the closer the camera, the cruder the hand. Now main is merged and every hand outside a rig goes through `of_cast.ps_hand` (hands_ps) or the film's one `phone_grip` (the 1-star phone and DECLINED, whose thumb goes to the red button with `thumb_tip`); 2.5's thumb is the series' thumbs-up turned sideways. The hand sheet logs these hands too. Not done: the guards' clasped hands and the palm on the roof are still overlapped rig hands, and a hand drawn with plain shapes can't be caught by the gate, only by the sheet. G5 PASS on v26.

## 200. An insert's arm is an arm; a held beat needs a change (The Offer v27, 23 Nov)

The v26 cold test (3 viewers) read every close-up arm as "a pole" or "a plank": each was one straight stroke from the hand to the frame's edge. And the lamp beat (2 s of a guard holding a lamp) read as "nothing happens" 3 of 3.

- An arm in an insert is drawn by `of_scenes.insert_arm`: hand, elbow, frame edge, the owner's sleeve on the upper part (a cuff at the wrist for a suit). No straight strokes.
- A press is a fingertip (`hands_ps` "point"). A thumb on a pin read as "a like" 3 of 3.
- A held beat needs one visible change, on the thing held: he looks at the lamp, the bulb goes dark (`lit` follows the cone), he looks at us. A cone that fades on a shut bonnet is not visible; the bulb is.
- A listener standing right behind the speaker reads as grabbing him. In 2.8d the guard steps back out of the frame with the lamp.
- A guard with no `turn` of his own turns his head to whoever speaks in the shot.
- A screen held in a hand is read upright: the 1-star phone at 0.2 rad was "too fast to read" 3 of 3 at 1.4 s.

## 201. Close-up arms pass when they are short; gags pass when they are body size (The Offer v29, 24 Nov)

v27 gave the insert arms an elbow and a sleeve; the v28 cold test still read every one as "a tube" or "a pole" (3 of 3). The two that passed (Father's thumb on DECLINED, the PAM phone) were short, as wide as the hand, and left the frame at the nearest edge.

- An insert shows the hand and a SHORT forearm as wide as the hand, out of the nearest edge. Crop tighter rather than draw more arm. Bare arms get no cuff (it flickered).
- A gag whose change is under about 20 px at feed width is not seen: the bulb going dark in a wide read as "eight identical frames". Cut close (`LAMP_GAG_CAM`), and give it an action of the whole arm: it flickers, dies, he shakes it, looks at us.
- A prop gag needs a second person's hand to say what it means: the PAM phone was seen 3 of 3 and understood 0 of 3 until Father's hand pushes it down.
- A slam needs the thing up first: the bonnet held open 0.3 s with his hand on it, then down. At 0.18 s from the first frame 2 of 3 "never saw a slam".
- A cut to the whole car running read as "it drove away, then it is back" (3 of 3). The start stays on the key and the rev counter.
- A fresh sheet over a burnt one must be SEEN going over it: the burnt plan first, then the fresh one slides up, then the pin. A cut straight to the fresh plan read as "the map is whole again".
- of_film reads the sound file: start the scene renders after of_sound has finished (scene 5 failed on a half-written wav).

## 202. Check the music as a map, not by ear only (The Offer v30, 24 Nov)

Measured from the stems of v29: music on for 12 s of 64.5; the office (14.7 s) had neither music nor radio and 6 s of it sat more than 30 dB under the voice; three new gags and two new shots had no sound of their own; the start-up sound ended after 1.6 s with the car still running.

- After any picture change, list every new action and give it a sound, or decide it is silent. A gag added in the picture is not in the sound until someone puts it there.
- Print, per section: voice, effects, music, radio (dB RMS), and the 0.25 s windows more than 30 dB under the voice. Silence that was not decided shows up there.
- A place with no bed needs a tone of its own: the office gets the series' "Open plan" bed, low, cut dead on the call that rings out.
- A gag gets the silence: the music stops on the lamp's tick and is back on the next shot.
- Kept as decided: the negotiation has no music. The radio is 8 dB up there, so the gaps are a room, not a mute.

## UptimeZ: Daddy's Home, animation v2 bubbles (22 Nov)

203. **Collect the lessons and the approved code before writing new code.** Asked to put every bubble on the PR #62 rule, I wrote a new bubble module and checker from scratch over three hours instead of reusing The Best Candidate's `bc_sb.bubble` / `measure` and `qa_bc.py`, which had solved the same problem and passed Tomas's reviews. The new code passed its own check on 668 of 668 drawings and still looked worse than v1: tails as long ropes wrapped round heads, tips inside the mouth like straws, boxes jumping around the frame, named cards for speakers who were on screen, and a cut-out where each tail met its box (the tail drawn in the box's path with the opposite winding, so the overlap went unfilled). The rule that would have prevented it was already in the lessons: a short side tail level with the mouth (174), reframe when there is no wall (358).
204. **A rule that conflicts with the frame is a question for Tomas, not a geometry problem.** "Box in the top band" and "tip on the cheek at mouth height" cannot both hold for a head low in the frame; solving it with ever longer tails hid the conflict instead of raising it.
205. **Look at the frames before sending, at full size.** None of the faults above needed a checker; six full-size crops would have shown every one.


## UptimeZ: One Star v7–v9, hands and the four new gates (23 Nov)

206. **Merge main before solving a series-wide problem.** I spent a round drawing a fourth hand system (`hands2`) while main already had the series' one hand (`kit.HAND`, `hands_ps`, ep 13's grips; lessons 147, 149, 178, 179). The branch was behind main. Fetch and merge first, then grep the lessons for the problem's words.
207. **One shape cannot stand in for three states.** `relax` was a closed fist, so resting hands read as fists or "toes", and nothing gripped anything. Two outside audits named the same cause from both sides: too much detail at medium size, too little up close. Resting hands are now a quiet outline (`hands_ps` "quiet"); fists are kept for raised or emotional gestures; held objects get a grip (`grip_rect`, from `phone_grip`). The robot keeps its own grippers.
208. **Pick a person's hand by the person, not by drawing order.** Scene 4 draws its set twice (a dry pass), and the grip needs two passes too, so "hand number 1" was a different hand each time and Pam's STOP palm never showed. Key the state by the rig's own skin colour (hers is pam_bc's, not the scene's `SKIN_PAM`), and count each person's two hands.
209. **Lesson 162 again: under a device scale, `identity_matrix()` is already in frame units.** The foreground pieces multiplied by HI a second time and fell out of the frame at 1080 only. Compare 540 and 1080 frame by frame after any drawing in frame coordinates.
210. **Measure the film before judging it.** The gates found what the reviews had circled: the 20 Nov scale rule (biggest face r 78–80) had framed 22 of 32 shots as mediums, and only 1 shot of 32 had anything in front of the people. Shot sizes come from the rendered face sizes, foreground from what is drawn over the people after them; each rule fails on a planted fault. The fix was cameras and layers (5 close-ups, 2 over-the-shoulder shots, set edges in front), not redrawing.
211. **A face in a picture is not a person.** The wall portrait drew the Client's rig, so the proportion gate saw a Client 11 % too big in shots he isn't in. Keep the portrait's head out of the people log.
212. **Room reverb on dialogue reads as "from a well".** The early reflections and tail added in One Star's v4 mix made Tomas wince; v9's voices are dry (`cs_film.WET = 0`) with the room tone kept. A voice effect gets an A/B listen from Tomas before it ships.

## UptimeZ: Pick a Side, the series' checks and board v3 (24 Nov)

213. **A new check finds old faults: run it on the approved board too.** The tail-length rule (10–20 px past the box) flagged 11 frames of the approved board v2 (90–270 px tails from `fs_animatic.speech`). Approved is not the same as checked; the fix went into a new version (board v3, `bc_sb.bubble`), not over v2.
214. **Count arms per shoulder, on the frame's own surface.** Counting `kit.arm` calls gave Pam 8 arms: the camera's framing pass (a 4×4 scratch surface) and her late hand redraw call it again. One arm = one shoulder point in device units, drawn on a 540-wide surface (`ps_checks.check_limbs`).
215. **Reuse a measured bubble by feeding it a measurement.** `bc_sb.bubble` measures its own rigs; for other rigs, capture each speaker's silhouette as it is drawn (push_group, alpha) and build `measure()`'s dict from it (mouth row, cheek edges walked on the silhouette, crown, hair reach). Wrap the text to the wall beside the face, up to the next face whose rows the box shares.
216. **A bubble's clash list includes the signs and the story props.** Without them the bubble hid the robot's OWNER card (3.1) and the phone on the booth table (4.3). A sign wholly under a bubble is out of frame; part of one is a misread.
217. **Two lines said in turn, or a camera move, get one key frame each on the board.** When both speakers' faces fill the frame (the booth, 4.3), the board shows 4.3a and 4.3b; the animation shows the bubbles in turn anyway.
218. **A pinned file must be pinned before the edit.** `ps_scenes_v3.py` was copied after the v4 flags went in, so it rebuilt the approved sheets differently. Pin from git (`git show HEAD:path > path_vN.py`) and check md5 right away.
219. **A motion test's shot id must not be a board shot's id unless it wants that shot's SHIFT.** The selfie test reused "3.1" with the board's camera already shifted, and render() shifted it again (signs cut).
220. **Strips at 216 px can't carry small props.** Two viewers read Pam's lit phone on the counter as "a purple cord" and "a blue glow"; at 216 px Mom reads as "a man in teal". Judge background props at 540 too, and size a story prop for the strip.

## 221. An arm needs its owner in the frame; a gag needs a shape, not only a state change (The Offer v31, 24 Nov)

The v30 cold test: the close-up arms were "a pole" or "a tube" in 8 of 9 mentions, though v29 had made them short and thick; the one that passed (Father's thumb on DECLINED) has the whole person in the shot. The lamp gag was 0 of 3, and all three called the lamp "a pole, a staff, a rifle".

- `insert_arm(hand, elbow, shoulder, ...)` draws the forearm tapering to the wrist, a bent elbow (`bend()` pushes it sideways), a wider upper arm in his sleeve, and his shoulder and a piece of his body behind it. Outlines for all parts first, then all colours, so the joints are one shape.
- A taut straight cable reads as a pole. The held lamp's cord now hangs to the floor (`cable_floor`), so it is a lamp on a cord.
- A fall that takes 0.4 s with a small shake is not a slam at feed size. 0.09 s down plus a 14 px jolt that dies in 0.3 s reads at 15 fps in two frames.
- A character reaching toward another's clasped hands reads as "holding hands". The guard lowers his own phone; nobody reaches.
- A mute test at 4 fps cannot show a 0.05 s flicker or a 0.1 s fall: add the 8-10 fps strip for any beat under 0.5 s, before judging it a FAIL.
- A shot's length is its take plus the 0.15 s lead (2.8b 2.2 s, 3.2 2.05 s); the rest is a drag.

## 222. UptimeZ ep. 13 *The Offer* v32 (24 Nov): inserts without arms, a gag that is a reaction, a joke that is cut

- Arms in inserts failed 3 of 3 at every length ("a pole", "floating") in v27–v31. v32: **hand + wrist stub only** (`insert_cuff`), the owner is in the frame by his hand alone. The zone rule (no burnt row below y 720) stops the pin hand's wrist reaching the frame's edge, so there the stub still runs to the bottom: check by cold test whether it reads as a sleeve or a pole.
- A gag that "doesn't land" needs the *reaction*, not more business: the lamp dies, he lifts it to look into it, sighs, then looks at us and holds 0.4 s (8 fps strip shows the hold).
- A joke read by 0 of 3 is cut, not repaired (the PAM tail): 2.8c 2.1 -> 1.15 s.
- Cutting away inside a long line must keep the speaker in frame (G5 BUBBLE check): push in on the speaker instead of cutting to the listener.
- Shorter shots move the ASR windows: "Pam?" fell to 1 of 3 until the office bed went 0.75 -> 0.6. Re-run the delivered-mix check after every timing change.

## 223. *The Offer* v33 (24 Nov, Tomas at 0:23: "the hand jumped, whose is it?")

- Taking the arms out of an insert (222) also takes out what tied a prop to the body: the watch was placed by a fixed offset on the old forearm and floated beside the hand. Anything worn goes on the wrist stub, along its direction.
- A hand that changes job mid-shot must travel in order: reach the thing (0.3 s), grip, then lift, with the object locked to the fist. v32 lifted the plug by itself while the hand crossed the frame in 0.3 s and changed shape on the first frame: a jump.
- I checked this shot only as stills at three times, not as a 10 fps strip of the encoded file. Every shot whose drawing code changed gets a strip before delivery.

## 224. *The Offer* v34–v37 (24 Nov): the engine insert after Tomas ("a hand walks in space") and three still audits (7, 7, 7.5 of 10)

- A hand-only insert works only at the frame's edge. Mid-frame, the hand needs its owner: here his back, head (his own: grey temples, strands, ears, short sleeves) and both arms from the shoulders, seen from behind.
- Arms are two bones of FIXED length (`ik2`); the motion's range is then set by the bones (move the shoulder or shorten the travel), never the reverse. A fixed sideways elbow offset stretched an arm by 33 % between two frames.
- A held object is drawn in the hand's order: object, then fingers; the tool's handle comes out past the fist. Withdraw a tool by the wrist, the arm still.
- "It looks like paper" in three audits was the GRIP, not the drawing: he held the plug by its thread, so only the white insulator showed. Held by the top, thread down, the metal shows and the pull has three phases (in the hole, half out, out).
- An audit's fix that moves a canon mark (DON from garage 3 to 7) is refused in the table, with the reason.
- Three rounds on the same six stills moved the score by 0.5: after two rounds, render and test the motion.
- Stills go to Tomas as PNG before any render (his message arrived mid-render at v34).

## 225. *The Offer* v38 (24 Nov, cold test v37, 3 viewers; then Tomas: "don't grow the thick white")

- An arm whose ELBOW is outside the frame reads as two things: a forearm from the edge and a sleeve lying apart, and it "jumps" when it folds in. Frame the shot so both elbows are inside (here the camera 15 % back, the body 30 up), then set the rest pose near the next action so the move is short.
- Pulling the camera back grows whatever is plain and light. Before sending, look for the biggest flat light area: here his white back; it became his shoulders only, with his navy overalls below, and short sleeves no wider than the arm, joined by one yoke.
- A lid that shuts needs the hand ON it all the way down and after; a hand beside it reads as a wave (3 of 3).
- A phone held "from the edge, along the floor" has no owner; from above it belongs to someone standing over it.
- A gag that is "long for what it delivers" loses time first (2.2 -> 1.8 s) and gets a body reaction (the shoulders and the lamp drop), since this face has no brows to move.

## 226. *The Offer* v39 (24 Nov, Tomas: "every phone screen looks cheap, like PowerPoint")

- One UI kit for every screen in a film (`of_ui.py`: status bar, app bar, card with a soft shadow, pill buttons, avatars; 100 units wide, drawn through `ui.hand` or `ui.full`). A screen made of a rectangle and two words is what reads as a slide.
- A real-app look must not cost the read: the dark call screen was worse than the old plain green one (audit and my own check). Keep the screen LIGHT, the one word big, and clear of the fingers on the grip's edge.
- On a 100 px wide screen nothing under about 9 units is read: drop helper text and placeholder lines instead of shrinking them.
- Before / after PNG, old row over new row, is the cheapest review of a restyle; the audit's "stop" criterion is worth taking (it scored the UI 8.2 and pointed at timing and reactions next).

## 227. Rules for hands and phones are on one page (24 Nov)

Eight lessons about hands and two about phones (147–226) had become a diary of versions, some contradicting each other (222's "hand only" against 224's "the owner in the frame"). `docs/rules-hands-and-phones.md` keeps only what holds now, with the superseded lessons named. Read it before drawing a hand, a close-up arm or a phone screen; add to it, not only to this list, when a hand or a screen teaches something new.

## 228. *The Offer* v40 (24 Nov): the repo's bubble, and a pause after a full stop

- The shared `speech.py` bubble (beside the mouth, a 10-20 px tail) put the speaker beyond doubt where cold viewers had guessed ("Off the car.", "Put it in the calendar."), but at its defaults (26, 220 px) a line beside a centred face wrapped to 4-5 rows. Opt-in settings were added to `speech.py` (SIZE, MONO_SIZE, MAX_W, MONO_BOLD, SIGNS_FIRST; defaults unchanged, so other films rebuild byte-identical); The Offer uses 30 / 28 / 300 / bold robot / props first. A line that still needs more than 3 rows keeps the v39 bubble over the head (measured on a scratch surface first). The robot's bubble goes over its visor, never across the card. A prop the beat needs is `protect`ed so no bubble covers it (the calendar phone).
- Kokoro runs a whole line's sentences together: 0.05-0.11 s at a full stop. Tomas: "after the Client's full stop, a small pause". Lines with more than one sentence are voiced one sentence at a time (`give` with "|"; "||" a longer stop; "@1.3" a faster sentence) and joined with silence: the Client 0.35 s, the robot 0.25 s, its "..." 0.5 s. Trim each part tight first, or its own breath adds 0.1-0.2 s. A sentence voiced alone comes out slower ("I ask." needed x1.3).
- From 24 Nov, renders and mixes stay local (`.gitignore`); approved cuts are marked by a git tag (`uptimez-the-offer-v39`). Pushing a tag was refused by this environment's proxy: Tomas pushes tags.

## 229. *The Offer* v41 (24 Nov): the room's light, contact shadows, and the cast alive (grill 24 Nov)

- Light without redrawing: a grade over the whole frame under the bubbles (darker ceiling and corners, a warm pool where the lamp is, the floor darker toward us; weaker in the office) and a soft contact shadow under every standing figure (`of_scenes.grade`, `_contact_shadow`, switch `LIGHT`). None where the set already shadows him (under the car, on the creeper, bent in at the wing).
- Blinks are irregular (2-6 s, one in seven a double) and come with a cut; a listener's eyes dart for 0.25-0.5 s every 1.5-3 s, a speaker's stay put (`of_cast.blink`, `dart`, switch `LIVE`).
- A breath lifts the chest, shoulders and head, not the legs: the figure is drawn once into a group and painted in two parts about the belt. Keep the head point still for the camera and the bubble, or both swim with every breath.
- The mouth leads the sound by 2 frames; the speaker's head dips up to 2 px on a stressed syllable (the take's loudness rising fast).
- Secondary motion is a damped spring on the film's clock (`of_cast.follow`): Father's chain after his gesture, the coil after the guard's head, the throne's crown when Don jolts, the robot's antenna after its bob and turn, Pam's glasses chain when she lifts the phone. Each is an opt-in hook in its shared module (`dh_cast.CHAIN_DX`, `COIL_DX`, `dh_props.CROWN_ROT`, `waiter_kit.ANT_DX`, `pam_mf.GCHAIN_DX`), 0 by default: a still rendered with the hooks at 0 is md5-identical to one from the old modules.
- "Eyes lead the head" has nothing to act on in this cast: the guards' eyes are behind sunglasses and Father, the Client, Don and Pam have no head turn of their own, only eyes.

## 230. *The Offer* v42 (24 Nov, Tomas: "why does the robot say 'miting' and 'you'll say'? the engine hum is not real")

- The line check passed words the ear rejects: the robot voice says "see" as "say" with or without the robot effect, and no spelling, phoneme string or neighbouring word fixed it (12 tries). `_match` is lenient to near-homophones, so G5 said 15 of 15. When a voice cannot say a word, change the word: "Calendar says... wait." Read the recognizer's own text for every line, not only the count.
- "meeting" is voiced "meet-ing": alone the recognizer hears "meeting"; inside the whole line it still writes "Maitang", so Tomas's ear decides.
- A synthetic idle (a filtered square wave) under a quiet gag reads as fake; the start that dies away in a second was better. Removed.
- A line's text lives in three places: `of_scenes` (the shot), `of_voices.LINES`, and the timing json copied from the one before. Change all three.

## 231. *The Offer* v43 (24 Nov): the roll-out and the sitting Client, after four audits and Tomas's frame-by-frame

- **A missing in-between is a missing drawing, not a missing frame.** The film is 15 drawings a second, each computed; "he pops from lying to sitting" meant there were only two drawings of him (legs from above, sitting side on). Rotating one toward the other read as "pulled out and turned like a cut-out". Write the exposure sheet first (36 + 54 drawings, 14 key poses, which are new), then draw the keys.
- **A 90 degree change of view is a cut.** Legs toward us to sitting side on: cut to a close on the boot and the fire (it also shows where the fire came from), then wide with him already rolling out side on, on the red creeper from the first frame.
- **Separate the roll from the sit-up, and chain the parts:** push off, roll (ease-out), brake (the trunk slides on), elbow, palm, up, over and back; hips shift, the trunk through 45 and 60 degrees, the head two drawings late, the propping arm straightens last. A gesture starts in the shoulder a beat before the hand.
- **A hand target closer to the shoulder than the arm is long folds the arm into a lump** ("a white bulge", "a fist stuck on"): the knee point was 12 px from the shoulder of a 64 px arm. No timing fixes geometry. Stop animating, get ONE static pose approved, then carry it through.
- **One target path per hand for the whole shot.** Two targets switched in one drawing read as "the arm is replaced".
- **A clip that hides him under the car must end when he is out** (the head was cut off at the sill line once he sat up). Check the frame after every state change, in the encoded test.
- For the sitting pose only: the figure is drawn apart, the outlines inside the white shirt erased (`of_cast._no_seams`), the rig's hands not drawn and one-silhouette fists put at the rig's wrists (`fist2`), the waist knot tucked away. The rag is the red shop rag, drawn first with the fingers over its top. Other shots and episodes keep the series' hand.
- Tomas's order of work, which got there: frame-by-frame PNG of the fault, an outside audit, the exposure sheet, key poses, one static pose approved, a motion test with sound, then the full render.

## 232. *The Offer* v44 (24 Nov, Tomas at 0:08 and 0:20; cold test v43, 3 viewers)

- A finger drawn AT the target while the arm stops short of it floats off the hand. A pointing finger grows from the hand the rig drew, toward the target, no longer than a finger.
- A gesture that carries the line is `protect`ed, and that speaker's bubble goes over his head for the whole shot (`bubble_over`), so it does not change place as the hand comes up.
- A cut away and back must not hide the move it was made for: after the close on the fire, the wide shot holds 0.2 s on the legs, THEN he rolls out in view (3 of 3 had read "he is already out").
- A hand that reaches across its own body reads as "a forearm pasted on his belly" (3 of 3). The hand that already holds the thing acts: it draws back and tosses the rag, which flies in an arc onto the fire.
- A walking figure stops beside the one he speaks to, not behind him.
- G5's FAIL lines for a scene print after the scene's summary line: read the whole tail, not the last line.

## 233. *The Offer* v45 (24 Nov, Tomas: "the lamp bothers me most", "that red rag makes me sick"; three outside audits)

- A prop is a THING with parts, not a sign of one. The work lamp read as "a microphone on a hose": now a grey handle the fingers show on, an orange collar, a long cage with a shield along its back, a bulb that is visibly lit or dead, a hook at the tip, a cable half as thick (`of_set.lamp`, `lamp_cable`).
- Light follows the lamp. The beam was tied to a fixed point; it now leaves the cage's open side along the lamp's angle and lands where that ray meets a surface. On a shut bonnet the pool is drawn after the car (`pool_late`).
- A cable drops from the handle's end BEHIND the man who holds it (drawn before him), so it never crosses his arm, hand or legs; its belly lags the hand and settles after it (`cable_swing`).
- A gag needs a different last picture than its first (three cold tests: "half landed"). Lit and pointing down; dead; turned up, looked into, below the chin so the face stays open; one wide shake; it hangs by his leg.
- One prop, one drawing. The rag was three polygons in three reds in three places. One `client_of.shop_rag` (opt-in `NEW_RAG`, other films unchanged): a soft outline, two shaded folds, a hem stripe, the same three stains. Two of one prop in a frame is a continuity fault: the rag on the engine is gone.
- A prop the same colour as what is behind it disappears: the creeper is dark grey now, as the set's.
- A replace by slice (`s[:a] + new + s[b:]`) deletes everything between its anchors: it took out the one-hand-per-wrist hook, and only the frame's own check caught it. Replace exact strings, and read every check line of every still.
- Moving a camera can cut a sign that was out of frame: test `box_state` for the new camera before posing in it.
- A sheet of stills sent for an outside audit carries its labels IN the picture (shot, time, BEFORE / NOW). Twice an unlabelled sheet was read as one scene, and story props (the burnt plan) came back as defects.

## 234. *The Offer* v46 (24 Nov, Tomas: "does the car's shadow move? Dad vanishes at 0:38? where do we save time?")

- A shadow is ON THE FLOOR and under everything: the car's was a grey rectangle drawn over the wheels and the legs, in one scene only, and it stood still while the car rocked. Now one soft pool in `of_set.car`, drawn first, in every shot with the car; it slides with the tilt.
- A character who is in one shot and gone in the next, same frame, has vanished. He stays in the cast of the shot after (2.8d) until we see him leave.
- Trimming: the room is in silent shots and in SHORT lines' tails; the long lines were already 0.2 s from their cuts. Measure each take against its shot before promising seconds (3.2 s promised, 2.2 s found).
- Before trimming a shot, read its motion and its sounds: actions and effects sit at fixed times inside it (a look at 0.45 s, a tick at 0.65 s, a ring 1.25 s long) and a shorter shot cuts them off. Re-key the action or leave the shot.
- A trim can drop a line from the mix without touching it: "Pam?" stopped being heard when 3.3 lost 0.2 s. The sound is built and its lines checked BEFORE any scene renders; `tail` after a command hides its exit code, so do not chain renders on it.

## 235. *The Offer* v47 (24 Nov, Tomas: "the bubble jumps in several places"; cold test, 3 viewers)

- A bubble placed from the head on every drawing follows everything the head does: it flipped sides (1.4), shook with the frame's jolt (0.9), bobbed with a nodding robot and a walking man (3.2, 2.9), slid with a lean (2.4). Measure it: draw each frame with and without the bubble, and the box of what differs is the bubble (`/tmp/bub.py` in the session; 6 of 15 lines moved).
- A bubble is placed ONCE per picture (one camera, one text), at the drawing 60 % into it, and laid over the frame after everything, so a camera jolt does not move it (`of_scenes.lock_bubble`, `of_film.lock_shot`, `shot_frame`). The gate: a bubble placed on the spot, or more than four placings in a shot, fails the render. 3 of 3 cold viewers: "no bubble moves within a held picture".
- Not done, and said so: the tail is locked with the box (it does not follow the mouth), and a bubble still takes a new place after a cut inside a line (3 of 3 saw it at 0:18, 0:26, 0:34). Both need the box given from outside in `speech.py` and `fs_animatic.speech`.
- A layer pasted onto a 2x surface needs the surface's device scale, or it lands twice as big and off the frame.
- When no wall beside a mouth is free of the listener's face and the prop he holds, the line goes in two short rows over the speaker's head (`bubble_top`, `speech.TOP_FIRST`, opt-in), and the camera comes down a little to make the room.

## 236. *The Offer* v48 (24 Nov, cold test v47 and four decisions)

- Before blaming a trim, read what it cut: "the lamp is suddenly in his hand" (3 of 3) was put down to a 0.3 s trim, but that trim was in the cut-in after it; the handover itself had always been 0.7 s. It is 1.0 s now (out, TAKEN, carried), the cut-in 0.3 s shorter.
- A line whose picture cuts in the middle keeps ONE place relative to its speaker and ONE wrapping: `of_scenes.BUBBLE_AT` puts the box by hand per camera, and its tail goes to the mouth drawn in that frame, so it follows him. Used where the automatic place failed (five lines); the other ten stay locked per picture.
- Make the room for a bubble with the camera, not by shrinking the text: the medium inside two long lines pulled back (1.8 to 1.5) so the line sits over his head, the plan whole above it.
- A prop that reads as a blob at its size is removed, not refined: the pocket rag ("a brick", 3 of 3) is gone; the rag exists only in his hand (`client_of.POCKET_RAG`, opt-out).
- Close shots draw only their cast, so people "vanish" from them: the Client stays in Father's closes at the bay, and the second guard stands behind his boss in the wide. A man who would be a sliver at the frame's edge is left out of that shot's cast.
- Build the sound and read ITS exit code before any scene renders (`cmd > log; echo $?`), then read each scene's whole tail.

## 237. *The Offer*: "Off the car." is a decided exception (Tomas, 24 Nov: "for the hundredth time")

- The Client says it from UNDER the car: no face, the bubble's tail lands on his hips in the dark under the sill. Cold viewers and audits will keep writing "unclear who speaks". It is canon and is not raised again: in a triage table it goes under "decided, stays", with no fix offered.
- The same for the red rag (Tomas, 24 Nov: "we fixed it a hundred times, closed"): it stays as drawn in v48 (in his hand only, one shape). Viewers' notes on it go under "decided, stays".

## 238. *The Offer* v49 (24 Nov, the last open points of cold test v47)

- A prop that turns over in a gag reads as a shape change ("it flips through odd shapes", 3 of 3). The dead lamp is lifted and tipped, shaken once and let hang: one shape all the way.
- A shot bound to its voice take cannot be trimmed; a static one is helped by a CUT in the take's own pause to whoever listens (found by measuring the silence in the wav). The line goes on over him in the speaker's own type, beside him, its tail pointing out of the frame toward the speaker; no name card over a story prop (the crown).
- The reaction a later shot is built on is not spent in the cut-in before it: Don still smiles on "wait.", so the smile can go in one drawing in the next shot.
- A turned head needs the bubble's tip given by hand too (`BUBBLE_AT[...]["tip"]`): under the car his mouth is beside the head's centre, not under it.
- "Too fast" shots get their time back before anything else is polished: the review phone 1.7 s, the key 1.3 s, the fresh plan 2.55 s.

## 239. *First Search* v38 (25 Nov): the gag comes first

Audit of 0:00–0:01: the first joke (the portrait on Don's head) landed at 3.7 s, after an empty door, a walk and a dissolve; nothing was said or written before 0:05. v38 opens on the loop's own slam: it runs along the wall at frame 0, the nail pops, the portrait lands on him at 0.6 s with a BONK! card, and he smiles on with his hands up under it. Then a cut to the door and a cut back; the Client's slam knocks the portrait off his head onto its nail. The shot went from 4.25 s to 2.95 s; the film from 62.9 s to 61.6 s.

- **The loop already held the cause.** The film ends on a slam; let the first frame be its effect.
- **The gesture was chosen by silhouette** (rule 0.2): three black shapes (hands on the plaque, one hand up, both up), two cold viewers, both read the symmetric "ta-da" (C) as "proudly wearing it"; the one-hand variants read as steadying or stumbling.
- **A moving hand needs its elbow chosen.** Two-bone IK that keeps the lower elbow folded both forearms across his belly on the way up; pick the elbow out to his side, and bypass the film's own pose tween (it re-eases every new tuple and crossed them again).
- **Not done:** the closer framing (#4 of the audit), because v33's rule (the shredder's label above the bottom quarter) leaves no room.

## 240. *Office Noir 2* v29–v42 (25 Nov): a raven at 0:00, the hands, the bar

- **A hook that flies at the lens must first be seen whole.** The raven diving straight in was "a black slab", "a glitch", "crow, cat or coat?" in three tests. One drawing of the whole bird side on, wings open, black against the lamp's light, made 3 of 3 name a bird. The frames where the wing fills the lens still read as a smear; lit feather edges help, a red gap in them made it worse.
- **A loop through the opening's actor:** the raven sits on the lamp in the last drawings and dives at 0:00; 3 of 3 tied the two together, so the seam is a continuation even though the frames differ.
- **An old film never got the series' hand.** Noir 2 (17–20 Nov) predates `hands_ps` (23 Nov): balls at the wrists, a red tube for an arm, the pen and the glove one red shape. `hands_ps` got an opt-in glove mode (one silhouette, slimmer tapered fingers, folds at the wrist); its own sheet is byte-identical with it off.
- **An insert needs its owner, or no arm at all.** "Over her shoulder" (her hair and shoulder in the near corner, an elbow inside the frame) fixed the "red hose" 3 of 3. The detective's lens arm failed as a plank through two drawn versions (a two-bone arm included); taking the arm out of the frame (his fist and cuff at the bottom edge, a long-handled glass) made it 0 of 3.
- **Never invent a cast for a crowd.** Guests drawn from nothing (round heads, dot eyes, black boxes) were "pathetic" (Tomas). The film's own hat shadows, cut out of the room's light, read 3 of 3 as men in hats offering money and drinks.
- **An outside review can try to fix the joke.** "Her face must stay uncovered" would have removed the gag (the card says "I never hide", the picture shows her hiding). Keep the gag and sharpen it instead: she winks over the money as the glass goes past (1 of 3 at 0.5 s, 3 of 3 at 0.83 s with the glass well clear of her face).
- **A two-drawing ease is one step at 8 fps.** A move eased over two drawings read as a jump on every cold sheet; four drawings each way read as a move.
- **Importing another film's module can import a second copy of this one.** `on4_weather` imports `on2_motion`, whose import called `use()` and took `b5`/`b68` over from the running film; the render failed in 8.7. Copy a small helper rather than import across films.


## 241. *The Offer* v51 (25 Nov, Tomas's /grill-me on what was left after cold test v50)

Four fixes, all read 3 of 3 by the v50 cold viewers, plus pacing:

- **Robot over Don (0:48, 0:53):** the off-screen card now has the robot's own small head at the frame's left edge, the tail into it. The name "ROBOT:" had covered the crown; a face says who without words.
- **Bubbles across mid-line cuts (0:19, 0:28):** 2.1 and 2.4 had a cut inside Father's line, and the two pictures had no free area in common, so the box jumped. Now: one picture each; 2.1 pushes in slowly (zoom 2.0 to 2.3) holding his head on screen, 2.4 stays still (a push put the lamp under the app buttons, the zone gate). The box stays, the tail follows. 2.8b and 2.9 kept their cuts, with one box for both pictures.
- **Lamp handover (0:23):** the same move in a closer frame (`HANDOVER_CAM`): out, taken, carried, big.
- **Lamp gag (0:42):** the drop over 0.45 s and the turn over 0.38 s; the body turns back after it.
- **Pacing (timing v25):** 0.4 +0.3 s, 4.1 +0.3 s (DECLINED held), 1.4 −0.16 s, 2.1 −0.12 s, 2.8 −0.2 s. The drags at 0:12 and 0:17 are mostly the voice itself; the takes were not touched.
- **Cover:** A3 without the fire's smoke on his wrist and without the rag in the corner (`of_set.SMOKE`, a cover-only hook).


## 242. *The Offer* v52 (25 Nov, an outside audit of v51, Tomas's /grill-me)

- **A handover has both hands on the thing.** The guard takes the handle's end above the Client's fist; both hold it 0.15 s (0.58–0.73), then the Client lets go and his hand goes back empty. The lamp keeps its angle at the switch (−1.3) and turns level while carried, so nothing jumps.
- **A cable lags the hand.** Its belly swings against the hand's speed (−2.2 × px per 0.08 s, ±26 px), in the Client's hand and the guard's.
- **A weight sways when the arm stops** (the lamp, 0.14 rad, damped), and the body turns back only after the drop (1.45 s).
- **An off-screen speaker leans in.** The robot's head, bigger (r 46), leans in from the edge in 0.2 s at the cut, the card under its chin, and leans out after the line; the card goes with it.

## 243. *The Offer* v53 (25 Nov, cold test v52, Tomas: "the concept changed, we can think of something else")

The end card (a fresh plan pinned over the burnt one, DON circled) read as "a glitch" or "a flash-forward" for 3 of 3, in every version since v30. Decided: no plan at the end.

- **The loop is a match cut on an action.** After DECLINED (held 0.3 s longer), Father, outside at his black car, brings the phone down, face down, on its roof. The film ends a hand above the roof (0.6 s); frame 0's fist on the blue car's roof lands the blow, with the film's own SLAM.
- **The last frame doesn't show the wall,** so nothing "heals": the burnt plan is never beside the whole one.
- **The loop gate changed with it** (`of_cut.slap_ok`): the last frame must BE that picture (bright street, black roof, velvet sleeve); the planted faults were rebuilt and are caught. The old gate (the set identical to frame 0) is kept in the file, unused.
- **Timing v26:** 4.2 2.55 → 0.6 s, 4.1 2.8 → 3.1 s; the film 65.6 → 64.0 s. The paper and pin sounds are gone; the garage theme comes back on DECLINED and runs through the seam.
- **v54 (two cold viewers on v53's ending: "seat backs?", "it never lands", "a jump"):** an insert's object needs its own signs (the black roof got a windscreen, pillar, side windows, handles, an aerial, a mirror), and a match cut needs the first action FINISHED: the phone lands in the last two drawings, with a burst, a thud and the car dipping, so frame 0's fist is the second blow, not the end of a cut-off first one. The loop gate's planted fault had to move with the picture (a fault outside the checked band was "caught by: NOTHING").

## 244. *The Offer* v55 (26 Nov): v54's last shot was drawn against the rules; the ending again, storyboard first

Tomas, on v54's new last shot (the phone on a black car's roof): rejected, hard. It was a picture drawn from nothing (a flat black car, an arm from the corner with no owner, a phone as a slab, an empty street), rendered before he saw a still, and "tested" only for whether it could be read. Every one of those is a rule on the rules page; none was listed before drawing.

- **Section 0 is not optional under time pressure.** List the rules, then a storyboard PNG, then his word, then the render. v54 skipped all four the same evening.
- **Cold viewers answer "can it be read", never "is it good" or "does it belong in this film".** A pass from them is not a pass on style. Compare the new frame with its neighbours yourself, and show Tomas.
- **Use the set and the rigs that exist.** v55's last shot is the garage, Father's own rig, scene 2's flat palm, frame 0's own SLAM lines; the only new thing is a camera position (`SLAM_CAM`).
- **The same misread three times: change the gesture (178).** The phone on a car read as "a wallet, a block" in v54 and in both storyboard variants. Now the phone goes to his pocket and his PALM slams the bonnet: 2 of 2 "a real hit", 2 of 2 "a deliberate echo" of frame 0's fist.
- **Cutting before the contact failed again** (2 of 2 "a break", as in v53): an outside audit asked for it twice; the storyboard test settled it without a render.
- **A raised hand with a phone drifts to the ear.** The wind-up goes out past his side with an empty fist, as the guard's does.
- **Contact is on the material that takes it:** the first palm landed at the windscreen's edge ("he hits the glass"); moved onto the bonnet's metal. The rig's ring finger hung under the palm ("a blood drop"): `dh_cast.RING_ON`, an opt-out hook, off only for this palm, which carries the ring itself.
- **Timing v27:** 4.2 is 1.15 s (pocket 0.40, up 0.33, down 0.13, slam and hold 0.29); the film 64.5 s. The audit's 0.5 s hold was cut to 0.2 s so frame 0's fist stays the second beat.
- **v56 (Tomas, the two points left open):** the phone now goes INTO the pocket: the hand reaches the pocket's mouth, the phone and the hand sink below a seam drawn over them (clipped, nothing drawn below it), and the hand comes out empty (0.16 + 0.14 + 0.10 s); the rig's ring finger is off while the hand is in it. The other arm swings back on the wind-up and forward on the blow (it hung still for the whole shot).

- **v57 (Tomas, after the cold test of v56: the pocket and the other arm not read, the slam a "knock"):** timing v28, 4.2 is 1.55 s (the pocket 0.70: mouth 0.20, the phone STOPS at it 0.15, IN 0.20, out empty 0.15; up 0.33; down 0.13; slam and hold 0.39); the film 64.94 s. Harder slam: higher wind-up, the car dips twice as far (tilt −0.10), the camera jolts 0.07 s, palm and car hold 2 drawings; then the arm GIVES (elbow bends, the palm stays on the metal: v55 canon, no off-the-bonnet recoil), the car rebounds once, the lines are gone 0.12 s after the hold, the man settles (lean to 0, other hand home, brow down). The wrist turns with the bonnet's slope (`palm_ang`). The other hand swings back and UP inside the frame (a first try at x 72 put the elbow outside it) and forward across him. The raised brow arches and stays below the hairline (`dh_cast.BROW_ARCH`, opt-in): grey on grey read as a bruise (2 of 3 viewers on v56, 0 of 3 on v57). Cold test v57, 3 viewers, 8 fps sheets: the phone into the pocket read 3 of 3 (v56: 0 of 3); the other arm seen by 2 of 3 ("a counterweight"); the slam read as a firm, annoyed bang (medium force), the car "jolts"; the loop read as a rhyme 3 of 3. Still open: the black phone against the dark coat, the thumb "a pill" in 4.1's close-up, the curved dark line across his waist, the framing jump from 4.1's wide to the slam camera.
- **v58 (Tomas, after the v57 cold test: four small points; the car's tilt stays until he hears the sound):** (1) the dark curve "like a string" across his waist was MY pocket seam, drawn in every phase of 4.2: now it is there only while the phone goes in and fades 0.15 s after the hand is out (`pocket_a`). (2) A face-down phone gets a pale edge in the wide (`of_cast.PHONE_RIM`, opt-in): a black phone on a dark red coat read as "a small dark thing". (3) 4.2 starts at 4.1's doorway size with Father where 4.1 left him (cam (149, 676, 1.9)) and pushes to the slam camera by the fist's top; the first try at y 640 cut the sign GARAGE 7 (zone gate caught it; moved lower). (4) 4.1's black-phone hold 0.55 → 0.35 s (timing v29, 4.1 is 2.9 s; the film 64.73 s, 1942 frames). Gates: G5 PASS, planted faults caught, hand gate passes.

245. **The Offer v59 (26 Nov), cold test 3 of 3 on the v59 encode.** Done: slam hold 0.14 s (2 drawings) and impact rays as big as frame 0's, off his face; 0.4 sleeve bends at an elbow; 1.7 guard and fist moved 28/24 px toward Father (shorter reach), camera 20 px; 2.8f shake 9 px / 0.22 s and the cable sways; bay insert: the guard's hand, cuff and sleeve bigger and lower; 0.5 round mouths ("A","O") drawn flat ("E"); 1.4 the Client looks at Father during "Burn them." (0-0.8 s). Result: nothing passed 3/3. Slam 3-4/10 again, the car "doesn't react" (3/3). 0.4 phone: still "whose arm" (3/3): the owner is never in the frame, a bent sleeve doesn't give him one. 1.7 lighter: "extra hand / unclear" (3/3). Insert arms: "tubes" (3/3). 2.8f: "snap, extra hand, the cord vanishes" (3/3). Open for v60: put the OWNER in the 0.4 frame (his shoulder and chest behind the sleeve); the guard's clasped hand when the other holds the lamp or the lighter; a flat sleeve polygon at the shoulder in 2.8f and 1.4 (a white box at 13.5 s) is the rig's elbow_low; the slam needs a visible car dip, not only the lines. Decided items (rag, pocket, red dot on the hand) were flagged again and left alone.
