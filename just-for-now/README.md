# Just For Now

Based on the "Temporary fix. Permanent problem." poster. A taped-up "temporary" fix ends up holding up the whole company. Developed over two rounds of review with a tester before building.

| Version | Video | Length | Purpose |
|---|---|---|---|
| [`test/`](test/) | `just_for_now_test_back.mp4`, `just_for_now_test_passed.mp4` | 6.9 s each | Rough test of the reveal + collapse only, identical pictures, two Tester lines to A/B |
| [`rough/`](rough/) | `just_for_now_rough.mp4` | 24.5 s | Whole story, rough: the tester's 23–25 s structure |
| [`v2/`](v2/) | `just_for_now_v2.mp4` | 28.5 s | Polish: dynamic opening and a bigger twist |

## v2 beats

| Time | Beat |
|---|---|
| 0–2.5 s | Day 900. The Tester tiptoes in, crash zoom on the tape, smash cut to the guy sprinting: "DON'T TOUCH THAT!" |
| 2.5–3 s | Rewind |
| 3–6 s | Day 1: he tapes a cracked pillar and draws a smiley: "Just for now." |
| 6–10 s | "I'll fix it Friday." Calendars: Friday, Next Friday… The tower grows, he turns gray |
| 10–13 s | Day 500: "MOST RELIABLE SYSTEM" trophy. Creak |
| 13–17 s | Day 900: "Who made this garbage?!" He sees his smiley and hides it behind the trophy. *cough* |
| 17–21 s | The Tester peels the tape. Collapse. "Should I put it back?" POP: everything is back |
| 21–24 s | "So… should we fix it?" "FRIDAY." |
| 24–28.5 s | Pull back: the whole world sits on a giant taped pillar. The giant boss robot: "WHO MADE THIS GARBAGE?!", sees its own smiley (with gold sunglasses) and covers it with a giant trophy. A big Tester reaches for the tape → loop |

## How the story got here

1. **Concept 1** (15 s): Tester touches a box, "Test passed.", collapse. Verdict from review: relatable, but the collapse is predictable.
2. **Tester review 1 (6.5/10):** the best joke is the guy hiding his own mark; the collapse needs a visible cause (tape, not a sticky note); "Should I put it back?" beats "Test passed."; cut callbacks.
3. **Concept 2** (~30 s): adds "Friday", the award, and the tower restoring itself.
4. **Tester review 2 (7/10):** escalation isn't more scenes; one physical rule; end on "Friday." to finish the character's arc; 23–25 s.
5. **Rough** built from review 2, then **v2** polished the opening and added the pull-back twist.

## Build

```bash
./test/build.sh
./rough/build.sh
./v2/build.sh
```

`rough/` and `v2/` import `v6.py`, a copy of the test scene module, for the Tester, tower pieces and speech bubbles.

## Still to test with viewers

- Do people laugh at the smiley being hidden and at "FRIDAY."? Target: two real laughs.
- Is the tape rule clear without words? Does the POP read as a surprise, not another rewind?
- Do viewers notice the boss's sunglasses on the giant smiley in ~1.8 s? Does the 28.5 s length drag (shorten the trophy and calendars first)?
- "So… should we fix it?" was generated with a full stop after "So".
