# Just For Now

Based on the "Temporary fix. Permanent problem." poster. A taped-up "temporary" fix ends up holding up the whole company. Developed over two rounds of review with a tester before building.

| Version | Video | Length | Purpose |
|---|---|---|---|
| [`test/`](test/) | `just_for_now_test_back.mp4`, `just_for_now_test_passed.mp4` | 6.9 s each | Rough test of the reveal + collapse only, identical pictures, two Tester lines to A/B |
| [`rough/`](rough/) | `just_for_now_rough.mp4` | 24.5 s | Whole story, rough: the tester's 23–25 s structure |
| [`v2/`](v2/) | `just_for_now_v2.mp4` | 28.5 s | Polish: dynamic opening and a bigger twist |
| [`v3/`](v3/) | `just_for_now_v3.mp4`, `just_for_now_v3_notag.mp4` | 25.3 s | Series pass: title bar, character polish, the Day 1 smiley as a readable plant, push-ins, trimmed, stereo master; no-tag version ends on the boss |

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

## v3 changes

- **Series title bar** "ME + MY AI" with a DAY pill (DAY 900 → DAY 1 → DAY 14 → DAY 60 → DAY 200 → DAY 500 → DAY 900) and TODAY on day 900, replacing the old captions in TikTok's top area. Bubbles and banners moved below it.
- **Character polish layer** (`jchars.py`, adapted from the series): expressions per beat, blinks, talking mouths on his lines, robot screen faces.
- **The Day 1 smiley is a readable plant:** drawn larger, with a 1.6× close-up as he draws it; his hand moves away so it shows. Both later jokes (hiding it, the boss's sunglasses smiley) pay it off.
- **Push-ins** on the creak, on "Who made this garbage?!" and on the giant smiley with sunglasses before the boss covers it.
- **28.5 s → 25.3 s:** calendars 4 s → 2.5 s, trophy 3 s → 2 s, pull-back 4.5 s → 3.8 s. The audio is the v2 mix re-placed on the new timeline (`MAP` in `audio.py`), mastered to stereo −14 LUFS.
- The tester robot moved out of the right-hand button area; the close-up of him hiding the smiley sits clear of the title bar.
- `just_for_now_v3_notag.mp4`: no chip; instead of looping it ends on the boss's trophy over his own smiley with "WHO MADE THIS GARBAGE?!" back on screen.

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
./v3/build.sh
```

`rough/` and `v2/` import `v6.py`, a copy of the test scene module, for the Tester, tower pieces and speech bubbles.

## Still to test with viewers

- Do people laugh at the smiley being hidden and at "FRIDAY."? Target: two real laughs.
- Is the tape rule clear without words? Does the POP read as a surprise, not another rewind?
- Do viewers notice the boss's sunglasses on the giant smiley in ~1.8 s? Does the 28.5 s length drag (shorten the trophy and calendars first)?
- "So… should we fix it?" was generated with a full stop after "So".
