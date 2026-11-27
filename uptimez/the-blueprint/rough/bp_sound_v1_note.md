# Rough with sound v1

`bp_sound_v1.mp4` is 400 s, 12000 frames, 1920×1080, bt709, **−15.1 LUFS, true peak −1.5 dBTP**, measured on the AAC.
`bp_sound_v1_nonight.mp4` is 360 s, 10800 frames, **−15.2 LUFS, −2.1 dBTP**. A second build of the no-night cut is md5-identical (`ce8403457c981d5f1d05cd8c01e5cd5e`).
Budget: `bp_sound_v1` to `v5`. This is version 1. The silent roughs v1 to v5 were not rewritten.

## What is in it

- **Picture.** `bp_rough_v5.mp4` and `bp_rough_v5_nonight.mp4`, stream-copied. The video packets of each file hash the same as v5's. No frame is redrawn, so every picture note in `bp_rough_v5_note.md` still stands.
- **Voices.** 43 dry takes from `src/bp_voices/` (`bp_voices.py`). 37 are the shipped takes, copied byte for byte from `ob_voices/film_v10`, `fs_voices/film_v13` and `cs_voices/film_v10`. The six night lines are new Kokoro takes, local only. The no-night cut has 37 lines.
- **Times.** `bp_sound_v1_timing.json`, from `bp_scenes.timeline()`: ledger order inside each shot, gaps from each line's source film (capped at 3 s where the source held lines this cut drops, stretched at most 1.5×), 1 s after the cut or after the last silent insert, at least 2 s of hold after the last line.
- **Room.** `cs_film.py`'s room tone at 0.3, about −57 dBFS in the mix. No reflections, no music, no pink noise.
- **Loudness.** Gain and `alimiter` on the AAC itself. The limiter ends at 0.85, about 1.5 dB over the plain gain. At 0.50 the voices (19.6 dB of peak over loudness) needed more than 10 dB of limiting and still fell short of −15.

## Gates

| Gate | Result | Proven on a known failure |
|---|---|---|
| `uz_check.check_film(..., format="16x9", loop_max=None)` | no faults on either file; 12000 and 10800 frames | — (the series checker) |
| Whisper inside the mix, 3 windows, letters ≥ 0.88 plus the key word; a one-word line heard with the line before | 43 of 43 (full), 37 of 37 (no-night). "Oh..." is a vowel and is not scored | The no-night mix with "Can you make the zero green?" and "Still one star." muted loses exactly those two lines |
| Room tone ×5 (the plan's plant) | loses no line | Not a failure: with no music the tone stays about 38 dB under the voices. The check is trusted on the muted plant, not on this one |
| `bp_draw_audit.py`, `--plant` | exit 0, exit 1 (the eight old misses) | — |
| `bp_draw_audit.py --lines`, `--lines --plant` | exit 0 with two named OPEN rows, exit 1 | "Can you make the zero green?" moved into shot 07's ZERO crop fails on the edge order, the silent insert and Don's head outside ZERO |
| The four locked stills | md5 unchanged | — |
| Cuts | every cut sits in room tone (−56 to −59 dBFS), no step larger than the room tone's own | — |
| Voice takes (`bp_voices.py gate`, `plant`, `rebuild`) | 43 of 43, plants 3 of 3, rebuild identical | in `voices/bp_stop2_voices.md` |

## Watched cold, 26 Nov 2026

Two fresh viewers ([viewer A](c3837bda-86a2-4412-9d4e-7a37736ed929), [viewer B](364f679d-7f89-4a9e-8b1f-0a2f935e9e03)) got the same 28 frame parts as the v5 watch (the picture is the same packets) and a transcript of every line with its start time and how the voice sounds, not who speaks. Open prompt first, then the five questions.

Pass mark: both read at least 4 of 5 beats. **Fail: 3 of 5 each** (v5 silent: 2 of 5).

| Direct question | Viewer A | Viewer B |
|---|---|---|
| 1. What did the Client lose? | The blueprint, hedged ("this" is never shown) | The MY GARAGES blueprint, for the bank |
| 2. What does Don do with it? | Guess: the archive shreds it | Guess: the archive shreds it. "Cannot tell for sure" |
| 3. Does the search find it? | No | No |
| 4. Who finds it in the end? | "The older assistant". Wrong woman | "The older Assistant to Don, matching the strips". Wrong woman |
| 5. What does the robot stamp? | CUSTOMER SUCCESS | CUSTOMER SUCCESS |

What the sound fixed: the deal ("One month. I ask, you find it."), the blueprint for the bank by Friday, the zero-results week, the review and "Stupid human", the robot's "obtained by a h-human", and the stamp's words. Both read the satire as intended: the company finds nothing, a human does the finding, and it still calls that customer success.

The same mistake from both, so staging, not viewers:

- **Nobody's mouth moves, so lines land on the wrong person.** Both gave Pam's British voice to Mom (the older woman behind ASSISTANT TO DON), and neither gave a single line to Sofía. The night was read as "the two desk women" arguing. Sofía's name is heard once ("SOFÍA!") and never attached to anyone.
- **The shred and the pocket still have no author.** Both guessed the shred from the taped strips in part 10, not from part 04. The pocket card flies before "Check your pocket", so neither knew what was found or where.
- **"Make the zero green" does not land:** the zero on the poster is green the whole film.
- **"Garage eleven" against ten garages, "Young man", "Your number"** were not understood by either.
- **Dead air:** both named the same tails after the last line: part 03 (about 15 s), 11 (about 20 s), 12, 14, 22 (about 30 s, at the payoff), 25 and the 20 s end. The talk is about 90 s of 400; spreading it across the holds would slow the dialogue rather than fill the picture.

None of these is a sound fault that a second mix of this picture could fix: they need mouths, hands or moved inserts. Per the stop rule, this file stayed the v5 picture. The picture pass did that work afterwards. `bp_sound_v2.mp4` is `bp_pic_v2` with these same takes.

## Open

- **Shot 10, on this file.** "Paid $999…" (the Client) and "Reply drafted…" (the robot) are spoken from outside COUNTER (world x 426 to 1034). Listed by name as OPEN in `bp_draw_audit.py`, because that check reads `SHOTS`. Stop 2 accepted them here. `bp_pic_v2` puts the shot on PUSH.
- **Shot 03 and shot 11, on this file, play their beat before the talk.** The v5 picture lays every insert at the start of its shot, so the shred lands before "Here, you will never lose anything again", and the pocket flies before "Is this a joke?" and "Check your pocket." `bp_pic_v2` moves both inserts to after the lines that name them.
- **The night lines are local only** (the Kokoro licence). Two of them are given to Kokoro differently from how they are written; see the ledger.
- The slate band still prints one line per shot. It is the rough's slate, not a caption.
