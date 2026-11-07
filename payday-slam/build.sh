#!/usr/bin/env bash
# Renders Payday_Slam.mp4 (1080x1920, 30 fps, 17 s). Needs python3 (pillow, numpy, scipy) and ffmpeg.
set -euo pipefail
cd "$(dirname "$0")"
python3 audio.py
ffmpeg -y -v error -i audio.wav -af "loudnorm=I=-14:TP=-1.5:LRA=11:linear=true,aresample=44100" -c:a aac -b:a 192k audio.m4a
seq 0 6 | xargs -P"${JOBS:-2}" -I{} python3 render.py scene {}
printf "file '%02d.mp4'\n" 0 1 2 3 4 5 6 > scenes/list.txt
ffmpeg -y -v error -f concat -safe 0 -i scenes/list.txt -c copy v.mp4
ffmpeg -y -v error -i v.mp4 -i audio.m4a -map 0:v -map 1:a -c copy -movflags +faststart -shortest Payday_Slam.tmp.mp4
mv Payday_Slam.tmp.mp4 Payday_Slam.mp4
rm -f v.mp4
echo "Wrote $(pwd)/Payday_Slam.mp4"
