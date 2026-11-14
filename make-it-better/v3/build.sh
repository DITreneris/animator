#!/usr/bin/env bash
# Renders make_it_better_v3.mp4 (1080x1920, 30 fps) and its cover. Needs python3 (pycairo, numpy, pillow) and ffmpeg.
set -euo pipefail
cd "$(dirname "$0")"
ROOT=../..
if ! fc-list | grep -qi "Lilita One"; then
  mkdir -p ~/.fonts && cp "$ROOT/fonts/LilitaOne-Regular.ttf" ~/.fonts/ && fc-cache -f >/dev/null
fi
python3 render.py render
printf "file '%s.mp4'\n" A S B C E F G H > list.txt
ffmpeg -y -v error -f concat -i list.txt -c copy video.mp4
python3 audio.py
./master.sh mix.wav fin.wav      # stereo, -14 LUFS, true peak about -1.6 dBTP
ffmpeg -y -v error -i video.mp4 -i fin.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart make_it_better_v3.tmp.mp4
mv make_it_better_v3.tmp.mp4 make_it_better_v3.mp4
python3 cover.py
for s in A S B C E F G H; do rm -f "$s.mp4"; done
rm -f list.txt video.mp4 fin.wav mix.wav chk_*.png sheet.png
echo "Wrote $(pwd)/make_it_better_v3.mp4"
