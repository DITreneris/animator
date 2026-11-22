# Office Noir 3: The Last Round. Script note v69 (22 Nov): release_v2

Film v34 (87.37 s, 2621 frames). No line is changed. Tomas after the whole-film test: cut the office into two pictures; take the white drawing out; the CV photograph is locked.

## Changed

1. **4.3 is two pictures.** He asks "How much?" over his shoulder (4.3, 1.5 s on film); she names the price in her own close picture (4.3b): she looks up at him. No cards are up yet in that picture: she deals them in 4.4b.
2. **No white drawing on a hit** in 7.2 (the stop, the shake and the robot's recoil stay).

## G5 (src/on3_qa.py): PASS

1080x1920, 30 fps, 2621 frames, BT.709; -15.5 LUFS, true peak -1.4 dBTP; speech 37 of 37 (backwards: 0 of 37); frame 0 = the last frame; against the 540 master PSNR mean 40.2 dB, lowest 36.1 dB.

The speech check first failed one line ("I always hit first.": in three of five windows the recognizer looped, "I always I always I always"; in the others it heard the line whole). The worker now voids a looped window and hears a longer one. Second change to the scorer in this release; the film's sound was not changed for it.

## Not done, not tested

- 4.3b was looked at in frames only; no cold test after this change.
- The red wash before the loop: discussed, not decided, not touched.
- The 1080 file is still the 540 picture scaled up (`_1080up`).
