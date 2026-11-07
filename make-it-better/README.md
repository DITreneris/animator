# Make It Better

Built on the "AI Workers' Union" poster. The robots went on strike after one tiny robot delivered version 47 and heard "Actually, the first one was better." Pure comedy for general viewers.

| Version | Video | Length | What changed |
|---|---|---|---|
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

## Known issues

- The rewind in v2 is 0.4 s, possibly too fast to read.
- The crowd chant is one synthetic voice layered four times.
