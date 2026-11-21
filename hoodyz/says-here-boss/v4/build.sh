#!/usr/bin/env bash
# Says Here v4: mix -> master -> picture -> mux -> QA. Uses v3's cast, sets and voice takes (../v3), untouched.
# Needs pycairo, numpy, soundfile, ffmpeg, the font Lilita One; for QA sherpa-onnx Whisper (ASR_DIR).
set -euo pipefail
cd "$(dirname "$0")"
python3 audio.py && ./master.sh mix.wav fin.wav
python3 film.py final
ffmpeg -y -v error -i video.mp4 -i fin.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -movflags +faststart says_here_v4.mp4
python3 -c "import film as F; F.draw(F.START['a12'] + 30).write_to_png('cover.png')"
rm -f video.mp4 fin.wav mix.wav
python3 ../../qa.py says_here_v4.mp4 603 lines.json
