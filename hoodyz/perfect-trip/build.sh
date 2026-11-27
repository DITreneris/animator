#!/usr/bin/env bash
# Perfect Trip: render the final, mix, master, mux, cover.
set -euo pipefail
cd "$(dirname "$0")"
python3 seam.py
python3 safe.py /tmp/safe_trip.json
python3 render.py final
python3 audio.py
bash master.sh mix.wav fin.wav
ffmpeg -v error -y -i video.mp4 -i fin.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest -movflags +faststart perfect_trip_v2.mp4
python3 cover.py
rm -f video.mp4 mix.wav fin.wav
echo "perfect_trip_v2.mp4 + cover_v2.png"
