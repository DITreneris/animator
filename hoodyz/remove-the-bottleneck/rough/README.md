# Remove the Bottleneck: rough 8 (ME + MY AI, HIS TEAM)

`rough8.mp4`: 470 frames, 15.67 s, 1080x1920, 30 fps. A rough for Tomas to judge with sound; not final.
Concept, decisions and audits: `../CONCEPT.md`.

Build (needs ../../perfect-date cast kit, pycairo, ffmpeg):

    python3 film.py final      # video.mp4; fails if any text is outside x 60-960, y 375-1600
    python3 film.py seam       # the last frame must equal frame 0 (without its bubble) exactly
    python3 audio.py && ./master.sh mix.wav fin.wav
    ffmpeg -y -i video.mp4 -i fin.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -movflags +faststart rough8.mp4
    ASR_DIR=... python3 ../../qa.py rough8.mp4 470 lines.json

Voices: Tomas's recordings 53-64 in `vo/` (`h_remove.wav` = recording 64, take 1, tempo 1.4).
Earlier versions are kept beside the current files (`film_r3/r4/r6.py`, `audio_r6.py`, `../setb_r3/r4.py`).
