#!/usr/bin/env bash
# Renders The_List.mp4 (1080x1920, 30 fps, 17 s). Needs node + playwright (with Chromium),
# python3 (numpy, scipy) and ffmpeg.
set -euo pipefail
cd "$(dirname "$0")"
python3 audio.py
node render.js video
ffmpeg -y -v error -i v.mp4 -i audio.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -movflags +faststart -shortest The_List.tmp.mp4
mv The_List.tmp.mp4 The_List.mp4
rm -f v.mp4 audio.wav
echo "Wrote $(pwd)/The_List.mp4"
