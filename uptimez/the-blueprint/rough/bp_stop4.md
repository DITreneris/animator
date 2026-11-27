# The Blueprint — Stop 4: rough with sound (26 Nov 2026)

Tomas's stop for the rough with sound, on the picture that passed.

- File: `bp_sound_v2.mp4` (400 s, 12000 frames). No-night: `bp_sound_v2_nonight.mp4` (360 s, 10800 frames).
- Picture: `bp_pic_v2.mp4`. Notes `rough/bp_pic_v1_note.md` and `rough/bp_pic_v2_note.md`.
- Local only. The six night lines are Kokoro, and that licence is still open.

What changed: the same dry takes now sit on a picture with a bubble on the speaker, a dull zero until shot 07's Approved, Don's hand putting the page in the shredder after the promise, and Pam's hand on the card after "Check your pocket." Shot 10 is on PUSH. `bp_sound_v1` stays the v5 picture.

## Gates

| Gate | Result | Proven on a known failure |
|---|---|---|
| `speech_gate` on every bubble, `SAFE_16X9` | 43 of 43, and 37 of 37 on the no-night picture | Sofía's line drawn on Pam is caught as the nearer head. A bubble on a silent frame is caught |
| Zero overlay | Dull (140, 143, 148) until `fs_4.3` ends, then poster green (51, 158, 87) | A green disc with the overlay left off is caught. The sample is beside the digit, because the centre is the white 0 |
| `bp_draw_audit.py --hands`, `--hands --plant` | exit 0, exit 1 | A sheet with no hand is caught. A hand with no arm is caught |
| `bp_draw_audit.py` live, `--plant` | exit 0, exit 1 (the eight old fails) | The finger stays OPEN: Pam is outside SHRED |
| `--lines`, `--lines --picture` | exit 0 with two OPEN rows, exit 0 | Shot 10's two speakers are OPEN on `SHOTS` (COUNTER) and inside the frame on PUSH |
| Four locked stills | md5 unchanged (`25111ff3…`, `da34775d…`, `0a25fcc6…`, `31e044d8…`) | — |
| `uz_check.check_film`, 16:9, no loop seam | no faults. Sound v2: 12000 frames, −15.2 LUFS, −4.4 dBTP; no-night 10800, −15.2, −1.2 | The picture files' −15.3 is pink noise. The mix replaced it |
| Whisper inside the mix, 2 of 3 | 43 of 43, 37 of 37. "Oh..." is a vowel and is not scored | The no-night mix with `fs_4.1` and `cs_6.5` muted loses exactly those two |
| A bare mix still rebuilds v1 | `bp_sound_v1_nonight` again is md5 `ce8403457c981d5f1d05cd8c01e5cd5e`. `bp_sound_v1.mp4` is still `9762e9991976878bf9ff07339208188b`. The v1 timing file is still `74f55afb586fcbb0f5b643063b0279bf` | The v2 mix writes `bp_pic_v2_timing.json` and refuses a `bp_sound_v1` output name |

Loudness is on the AAC. The limiter ends at 0.80. At 0.85 the full cut peaked at −0.3 dBTP and the no-night cut at −0.2. Gain on the shipped mix is +9.40 dB. Room tone is `cs_film.py` at 0.3. No reflections, no music.

## The watch

Both viewers, 4 of 5. [G](32a0b079-1046-43bf-b18a-0f6f3a057a46) and [H](a18e20df-b1c0-4991-8ded-c1a5d677e872). Don feeds the page into the shredder. The finder is the woman with the brown bob, glasses, purple top and headset at the desk. Her name is not printed.

Both missed the same question, with different wrong answers. On the silent rough both had answered "cannot tell", so this is not a fall. v3 was not spent.

What does the robot stamp?

1. **CUSTOMER SUCCESS.** The two words `bp_scenes.stamp` draws. This is the line in the film.
2. The zero, turned green. Viewer G. That colour change is Don's "Approved." on shot 07.
3. A blank yellow circle on the clipboard. Viewer H.

## Decided, 26 Nov 2026

**1. Leave the stamp.** Tomas watched `bp_sound_v2.mp4`. The stamp stays CUSTOMER SUCCESS in the note. It is not redrawn.

`bp_pic_v3` is not that redraw. It is three beats the wide still cannot tell: the portrait falling off the wall, the cannon firing, and Pam matching the strips. 400 s, the shot lengths, and the v2 line times stay.

2 and 3 were not taken. A stamp redraw was the other offer, and it was declined.
