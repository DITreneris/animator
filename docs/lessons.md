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
