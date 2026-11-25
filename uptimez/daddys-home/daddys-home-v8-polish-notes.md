# Daddy's Home v8: polish and master (25 Nov)

## What went wrong in the film sent on 25 Nov at 05:05

- Two old renders were tracked in git: `dh_s1_anim_v8.mp4` and `dh_s2_anim_v8.mp4`, from commit 008a4ad.
- On 24 Nov at 20:47, a `git stash` of those two files (made to start a clean branch) put the old renders back over the new ones.
- Three joins then used them: v8c, v8d and the file sent. That is why the film had scene 1 with the phone at Don's ear, and Father's "I arrive at five." box beside Don's head, so it read as Don's line.

Fixes:
- The two files are out of git (`git rm --cached`).
- `dh_film_v8.join` refuses a scene whose picture is older than its `dh_anim{n}_v8.py` (`_fresh`).

## Trims (Tomas: light, three places)

`dh_film_v8.CUTS`: frame ranges at 30 fps, cut from a scene's picture and its sound together, so everything after them keeps its sync.

- **Scene 5, 7.1b (the case):** the ticks after its two clicks, and the end of the open hold. The brush stays.
- **Scene 7, 9.1b:** the door opening, between the knock and the guards stepping apart.
- **Scene 8, 10.6a and 10.6c:** the robot's second and third look between the HR CAM shots.

The film goes from 96.8 s to 95.1 s. The estimate was 6–8 s; these three places only hold 1.6 s of repeated silent drawings.

## The one-frame shift in the joins

- A scene file's AAC starts before 0 (priming), and the concat demuxer moved the picture one frame late at every scene join. The films still had 2853 frames.
- The join now takes each scene's picture alone (`_video`). The film's sound comes from the scenes' wav, as before.

## Speech

- `dh_film_v8_timing` counts the cuts, and two lines are updated to their takes:
  - 2:1.2 "Brace yourselves. Dad is coming.";
  - 5:7.3b "CEO responsible.".
- Result: 34/36 heard.
  - 1:0.3 "Donnie." is as loud as the other lines (−15.8 LUFS); the recogniser hears "D".
  - 2:2.4 "Into what?" is heard as "into water", with the line before it inside its window.

## Master

`dh_master_v8.py`: each scene drawn again at 1080x1920 by its own v8 module (the same drawings, the same bubbles in the same order), picture only. It is joined with the same CUTS and sound.

- **Every scene, 1080 scaled down against 540:** mean 32–37 dB, no frame below 25 dB.
- **The films, 540 against 1080:** 2853 frames, mean 33.9 dB, minimum 25.8.
- **Master:** 1080x1920, 30 fps, 95.1 s, −16.6 LUFS, −1.6 dBTP. Whisper 34/36, as at 540.
