# Make It Better

Built on the "AI Workers' Union" poster. The robots went on strike after one tiny robot delivered version 47 and heard "Actually, the first one was better." Pure comedy for general viewers.

| Version | Video | Length | What changed |
|---|---|---|---|
| [`v3/`](v3/) | `make_it_better_v3.mp4` + cover | 15 s | **Master.** Series HOODYZ bar with a state pill, brand tag dropped, "MORE/LESS professional" audible, the loop no longer pops, a push-in on the last feedback line, the union beat no longer silent; then a polish pass (below) |
| [`v1/`](v1/) | `make_it_better.mp4` | 15 s | Opens on the payoff (letter + thumbs-up), sentence split across the loop: "…make it better?" / "Love the energy. Could you just…" |
| [`v2/`](v2/) | `make_it_better_v2.mp4` | 15 s | Clearer opening: "THE AI WENT ON STRIKE" + chant, his request, record scratch, three giant robots stare. Full line at the end, the army's roar restarts it |

## v2 beats

| Time | Beat |
|---|---|
| 0–2.2 s | Strike rally: "NO MORE VERSIONS!" The guy steps in: "Could you just make it better?" |
| 2.2–2.8 s | Record scratch, giant robots stare |
| 2.8–3.2 s | Rewind V47 → V1: "HOW DID THIS START?" |
| 3.2–6.9 s | V1, V12, V30, V47 with his feedback: "Make it pop." "More professional." "Less professional." "Actually, the first one was better." |
| 6.9–7.9 s | Eye twitch, clipboard down |
| 7.9–10.4 s | Day 1 to Day 4: the strike grows |
| 10.4–12.5 s | "THIS IS OUR FINAL VERSION." |
| 12.5–15 s | Happy thumbs-up: "Love the energy. Could you just make it better?" |

**Lesson from v1:** opening on a payoff that only the story explains confused viewers; v2 states the situation first.

## Build

```bash
./v1/build.sh
./v2/build.sh
```

## v3 changes (after an OK/fail pass against our best practices)

Measured against v2:

| Fixed | Was | Now |
|---|---|---|
| Series branding | No title bar at all | HOODYZ bar with a pill showing the state: ON STRIKE, the version during the flashback |
| Brand tag | `promptanatomy.app` at y 158–192, inside TikTok's top 0–200 strip | Dropped. Nothing is drawn above y=200 (measured: 0.6% contrast, which is background gradient) |
| The contradiction | Speech recognition heard "professional" for both "**More** professional" and "**Less** professional" | Re-synthesized with the stress written into the phonemes, plus a presence boost; both now transcribe correctly from the final mix. The label-pop sound effects were landing on the first word, so the lines moved 0.12 s later |
| The loop | The guy and his bubble vanished at the cut (picture difference 32.8) | He holds the closing pose from frame 0, so only the bubble swaps for the roar (19.8) |
| The union beat | 2.1 s at -28.3 dB, 14 dB under the film: reads as a fault | Crowd murmur and a sign creak; -23.9 dB, still a dramatic drop |
| The flashback | 3.9 s at one framing | A slow push-in on "Actually, the first one was better." |
| The rewind | Three version cards in 0.4 s (0.13 s each) | Two cards, 0.2 s each; recoloured to the episode's red and gold instead of off-palette purple |
| Mastering | Mono, -14.8 LUFS, a fixed limiter | Stereo, -14.3 LUFS, two-pass loudnorm (`master.sh`), peak -1.1 dBFS |
| Cover | None | `make_it_better_cover.png` |

### Polish pass (second review)

| Fixed | What changed |
|---|---|
| Two captions said the same thing at the open | The yellow "NO MORE VERSIONS!" is gone; the placard already says it. The loop's picture difference dropped again, 19.8 → 16.3 |
| The flashback's chronology | "47 VERSIONS EARLIER" under the V1 label for 0.9 s |
| The robot winked instead of giving up | **A bug:** the twitch scaled only the right eye (`tw if q==1 else 1`). Now both eyes twitch, hold flat from the ninth frame, and the V47 board drops after the hold as the shot's one clear action |
| The punchline had no consequence | The room freezes for the last 0.4 s and the sunglasses leader's smirk flattens to a line while the guy keeps grinning |
| The little grey object was unreadable | The toaster is bigger and carries its own V47 picket sign, so "even the appliances walked out" reads |
| The chant was one voice layered four times | Eight copies at different pitches and speeds, none quite in time, each filtered differently, with a room tail; faded out before his first line so it no longer eats "Could you" |

**Checks on v3:** 450 frames, 1080×1920, 30 fps; no flat frames; nothing in TikTok's top strip; all four feedback lines transcribe correctly from the final mix. A separate agent watched it muted, retold the story correctly and called the loop smooth. A clean rebuild from a copy reproduces the film, the cover and the audio bit for bit.

**Not checked, needs people:** whether it is funny, the crowd chant (still one synthetic voice layered four times), the mix balance.

## Known issues

- "Make it pop" is partly masked by the music; the bubble carries it.
- Days 3 and 4 are a wall of small robots; the mass is the gag, but individual robots are mush at phone size.
