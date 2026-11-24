# One Star: the master, v13 (24 Nov)

UptimeZ Inc. · episode 11 · **approved by Tomas as the master (24 Nov).** The film is rough cut v13 unchanged.

| | |
|---|---|
| Film | `one_star_master_v13.mp4` (1080×1920, rebuilt, not committed) · `one_star_master_v13_540.mp4` (committed) |
| Length | 61.3 s, 736 drawings at 12 per second, 30 fps |
| Sound | −15.7 LUFS integrated, peak −2.4 dBFS; dry voices with the room tone under them |
| Lines | 16 of 16 word-exact in the final mix (speech recognition, three windows each) |
| Gates | GV, GP, GD, GH pass on every drawing of shot list v19 (`one-star-gates-v19-r2.md`) |
| Cold tests | 5 of 5 beats on v8 and on v11, two fresh viewers each |
| Cover | `one_star_cover_v1.png` (1080×1920): the post and the reply, "Stupid human." 🤡, under the title and the one-star rating; reads at 270 px. `src/cs_cover.py 1.4b 20` |

**Rebuild** (from `uptimez/src`): `python3 cs_film_v8.py ../customer-success 1 2 6`, `python3 cs_film_v9.py ../customer-success 4`, `python3 cs_film_v12.py ../customer-success 3 5`, then `python3 cs_film_v13.py ../customer-success`; copy `one_star_rough_v13.mp4` to the master's name.

**Known and left:** a viewer could not tell who dialled whom in the call (2.1); both viewers wondered why Don is happy at one star (the joke).
