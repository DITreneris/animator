#!/usr/bin/env bash
# Renders says_here_v3.mp4 (1080x1920, 30 fps, 562 frames) and its cover. Needs python3 (pycairo, numpy, soundfile, pillow) and ffmpeg.
# Voices are already in vo/ (HARV: python3 voices.py regenerates them; Hoody: Tomas's recordings).
set -euo pipefail
cd "$(dirname "$0")"
ROOT=../..
if ! fc-list | grep -qi "Lilita One"; then
  mkdir -p ~/.fonts && cp "$ROOT/fonts/LilitaOne-Regular.ttf" ~/.fonts/ && fc-cache -f >/dev/null
fi
python3 render.py video
python3 audio.py
./master.sh mix.wav fin.wav      # stereo, two-pass loudnorm, limiter
ffmpeg -y -v error -i video.mp4 -i fin.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -movflags +faststart says_here_v3.tmp.mp4
mv says_here_v3.tmp.mp4 says_here_v3.mp4
python3 cover.py
python3 chars.py                 # character_sheet.png
rm -f video.mp4 fin.wav mix.wav chk_*.png
echo "Wrote $(pwd)/says_here_v3.mp4"
