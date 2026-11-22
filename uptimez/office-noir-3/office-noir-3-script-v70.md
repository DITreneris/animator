# Office Noir 3: The Last Round. Script note v70 (22 Nov): release_v3, drawn at 1080

Film v35 (87.37 s, 2621 frames). No line is changed. Tomas: fade straight to black; a native 1080; commit and push.

## Changed

1. **The end** (8.5) goes in on his sleeping face and straight to black; out of the black, the first drawing. No red.
2. **Native 1080** (`src/on3_native.py`): every surface the film makes is twice as large with a device scale of 2, so all drawing stays in 540x960 units; the noir pass and the grain take their size from the surface (the grain is the 540 grain, each grain two pixels wide). The 540 build is untouched: `on3_master.py` draws it as before.

## G5 on office_noir_3_release_v3_1080.mp4

| Check | Result |
|---|---|
| Format | PASS: 1080x1920, 30 fps, 2621 frames, BT.709 |
| Loudness, final AAC | PASS: -15.5 LUFS, true peak -1.4 dBTP |
| Speech | PASS: 37 of 37 (backwards: 0 of 37) |
| Frame 0 against the last | PASS (0.63 of 255 after encoding; 0 on the drawings) |
| 1080 against the 540 build, per frame | **FAIL by the worker's mark**: PSNR mean 34.4 dB, 252 of 2621 frames under 30 dB, lowest 25.8 dB |

What the dips are: all in shots that are text on a flat ground (the poster 2.0, the CV 2.7, the ticket 4.4a, HUMAN APPROVAL REQUIRED 7.4) or carry a bubble. Measured on the worst one (7.4): the lettering spans the same 49 to 436 px in both, and the frame's mean and its eighteen block means agree within 1 of 255. The same drawings rendered straight from the film at both sizes differ by 0.15 to 1.45 of 255 on average. So: type is rendered a fraction of a pixel differently at twice the size, and the 540 copy is compressed hard (crf 27); not a different picture. The mark was not lowered to make it pass.

## Seen while checking, not fixed

- 5.1c: a hairline runs down his face and chest where the half-off robe is clipped; it is in the 540 too and is plainer at 1080.
- No worker for text boxes, tails and bubbles on faces. Not rebuilt from a clean checkout. No cold test of 4.3b or of the new end.
