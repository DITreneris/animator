#!/usr/bin/env bash
# Renders whos_a_good_boy_v3_3.mp4 (with the promptanatomy.app chip) and whos_a_good_boy_v3_3_notag.mp4
# (no chip, TODAY clear of the right edge). 1080x1920, 30 fps, 24 s. Needs python3 (pycairo, numpy, pillow) and ffmpeg.
# fin14.wav is the mastered mix (-14 LUFS, stereo) used for both; `python3 audio.py` rebuilds the raw mix as mix.wav.
set -euo pipefail
cd "$(dirname "$0")"
ROOT=../..
if ! fc-list | grep -qi "Lilita One"; then
  mkdir -p ~/.fonts && cp "$ROOT/fonts/LilitaOne-Regular.ttf" ~/.fonts/ && fc-cache -f >/dev/null
fi
printf "file '%s.mp4'\n" A B C D E F G > list.txt
for MODE in tag notag; do
  if [ "$MODE" = notag ]; then export NOTAG=1; OUT=whos_a_good_boy_v3_3_notag; else unset NOTAG; OUT=whos_a_good_boy_v3_3; fi
  python3 v10.py render
  ffmpeg -y -v error -f concat -i list.txt -c copy video.mp4
  ffmpeg -y -v error -i video.mp4 -i fin14.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart "$OUT.tmp.mp4"
  mv "$OUT.tmp.mp4" "$OUT.mp4"; echo "Wrote $(pwd)/$OUT.mp4"
done
rm -f {A,B,C,D,E,F,G}.mp4 list.txt video.mp4 chk_*.png sheet.png
