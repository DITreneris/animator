#!/usr/bin/env bash
# Perfect Date v2.4 (v2.3 = render2_v23.py; finale eased, no jump): render, mix, master, mux. v1 (../) is imported, not touched.
set -euo pipefail
cd "$(dirname "$0")"
python3 render2.py final
python3 audio2.py
bash master2.sh mix.wav fin.wav
ffmpeg -v error -y -i video.mp4 -i fin.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest -movflags +faststart perfect_date_v2_4.mp4
rm -f video.mp4 mix.wav fin.wav
echo "perfect_date_v2_4.mp4"
