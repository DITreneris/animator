#!/usr/bin/env bash
# Renders says_here_v2.mp4 (1080x1920, 30 fps). Needs python3 (pycairo, numpy, pillow) and ffmpeg.
set -euo pipefail
cd "$(dirname "$0")"
ROOT=../..
if ! fc-list | grep -qi "Lilita One"; then
  mkdir -p ~/.fonts && cp "$ROOT/fonts/LilitaOne-Regular.ttf" ~/.fonts/ && fc-cache -f >/dev/null
fi
python3 render.py render
printf "file '%s.mp4'\n" A B C D E F G H I J K > list.txt
ffmpeg -y -v error -f concat -i list.txt -c copy video.mp4
python3 audio.py
ffmpeg -y -v error -i mix.wav -af "lowpass=f=15000,alimiter=limit=0.72:level=false,aresample=48000" -c:a pcm_s16le fin.wav
ffmpeg -y -v error -i video.mp4 -i fin.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart says_here_v2.tmp.mp4
mv says_here_v2.tmp.mp4 says_here_v2.mp4
for s in A B C D E F G H I J K; do rm -f "$s.mp4"; done
rm -f list.txt video.mp4 fin.wav mix.wav chk_*.png sheet.png
echo "Wrote $(pwd)/says_here_v2.mp4"
