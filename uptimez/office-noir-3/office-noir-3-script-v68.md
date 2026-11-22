# Office Noir 3: The Last Round. Script note v68 (22 Nov): the release build

Film v33, the animatic v29's timing and lines, release_v1 (87.07 s, 2612 frames).

## G4, the whole film (cold_test_whole_v2/result.md): PASS

Two fresh viewers, 5 of 5 beats each, the loop read by both, the defeat "ironic, not confusing" for both.

## G5 (src/on3_qa.py, exit code 0)

| Check | Result |
|---|---|
| Format | PASS: 1080x1920, 30 fps, 2612 frames (expected 2612), BT.709 |
| Loudness, on the final AAC | PASS: -15.5 LUFS, true peak -1.7 dBTP |
| Speech (Whisper base.en, every line in the final mix) | PASS: 37 of 37; self-test, the mix backwards: 0 of 37 |
| Frame 0 against the last frame | PASS: mean difference 1.1 of 255 after encoding (0 on the drawings) |
| 1080 against the 540 master | PASS: PSNR mean 40.8 dB, lowest 36.7 dB |

## Not to the standard, said plainly

1. **The 1080 file is the 540 picture scaled up** (lanczos), not drawn at 1080: the noir pass, the light and the masks of this film work on 540x960 pixels, and the last versions' layers too. The file is named `_1080up`. A native 1080 needs those passes rewritten for a scale.
2. **No worker checks this film's text boxes, tails and bubbles on faces**; they were looked at on sheets and by the cold viewers only.
3. The speech check first failed 3 of 37 on its own scoring (digits: "100 bucks", "Round 1"; a short line's window eaten by the line before it); the scorer was changed, not the film. The backwards self-test still fails all 37.
4. Not rebuilt from a clean checkout; no md5 comparison of the earlier episodes' sheets was run for this film's changes (they are all inside film_on3.py and on3_animatic.py).

## Left open on purpose (Tomas)

The crowd, robe, belt, antenna and steps are built and not seen. Open and seen: the white drawing on a hit reads as an error to both whole-film viewers; nothing recoils after the first punch; the office shot 4.3 is the stillest stretch; the Referee's entrance (changed after test 67, not re-tested alone).
