#!/usr/bin/env bash
# Every Failure: gates, render, mix, master, mux. Writes every_failure_v1.mp4 (rough, placeholder voices).
set -euo pipefail
cd "$(dirname "$0")"
python3 seam.py
python3 safe.py /tmp/ef_safe.json
python3 render.py
python3 audio.py
bash master.sh mix.wav fin.wav
ffmpeg -v error -y -i tmp_video.mp4 -i fin.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest every_failure_v1.mp4
rm -f tmp_video.mp4 mix.wav fin.wav
echo "every_failure_v1.mp4"
