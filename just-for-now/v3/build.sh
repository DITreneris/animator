#!/usr/bin/env bash
# Renders just_for_now_v3.mp4 (loop, with the promptanatomy.app chip) and just_for_now_v3_notag.mp4
# (no chip, ends on the boss covering his own smiley). 1080x1920, 30 fps, 25.27 s. Needs python3 (pycairo, numpy, pillow) and ffmpeg.
set -euo pipefail
cd "$(dirname "$0")"
ROOT=../..
if ! fc-list | grep -qi "Lilita One"; then
  mkdir -p ~/.fonts && cp "$ROOT/fonts/LilitaOne-Regular.ttf" ~/.fonts/ && fc-cache -f >/dev/null
fi
python3 audio.py;          bash master.sh mix.wav fin.wav
NOTAG=1 python3 audio.py;  bash master.sh mix_notag.wav fin_notag.wav
python3 render.py render                 # all scenes, loop version
NOTAG=1 python3 render.py render Zc Zd   # nZc nZd: the no-tag ending
L="A B C D E F Fb Ga Gb Gc Gd Ha Hb Hc Za Zb"
build () {  # $1 output, $2 audio, then the two last scenes
  local out=$1 wav=$2; shift 2
  printf "file '%s.mp4'\n" $L "$@" > list.txt
  ffmpeg -y -v error -f concat -i list.txt -c copy video.mp4
  ffmpeg -y -v error -i video.mp4 -i "$wav" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart "$out.tmp.mp4"
  mv "$out.tmp.mp4" "$out.mp4"; echo "Wrote $(pwd)/$out.mp4"
}
build just_for_now_v3       fin.wav       Zc Zd
build just_for_now_v3_notag fin_notag.wav nZc nZd
for n in $L Zc Zd nZc nZd; do rm -f "$n.mp4"; done
rm -f list.txt video.mp4 mix.wav mix_notag.wav fin.wav fin_notag.wav chk_*.png sheet.png
