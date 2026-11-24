#!/usr/bin/env bash
# Just One Line: picture (with the safe-zone gate) -> mix -> master -> mux -> QA. Uses ../fight.py (v12), ../kp.py and the
# perfect-date cast. Needs pycairo, numpy, soundfile, ffmpeg, the font Lilita One; for QA sherpa-onnx Whisper (ASR_DIR).
set -euo pipefail
cd "$(dirname "$0")"
python3 film.py final                       # exits 1 if any text box leaves x 60-960, y 375-1600
python3 audio.py && ./master.sh mix.wav fin.wav
ffmpeg -y -v error -i video.mp4 -i fin.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -movflags +faststart just_one_line.mp4
python3 -c "import film as F; F.draw(F.START['H'] + 45).write_to_png('cover.png')"
rm -f video.mp4 fin.wav mix.wav boxes.json
python3 ../../qa.py just_one_line.mp4 505 lines.json
