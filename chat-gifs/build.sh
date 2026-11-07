#!/usr/bin/env bash
# Rebuilds both chat videos at 1080x1920, 30 fps, from the source GIFs in src/.
# Needs python3 (pillow, numpy) and ffmpeg.
set -euo pipefail
cd "$(dirname "$0")"

# GIF clean-up: light denoise for dither, gentle tone curve that keeps light-grey
# bubbles visible, mild saturation, light sharpen. Stronger eq/curves erase or darken bubbles.
CLEAN="hqdn3d=1.5:1.5:0:0,curves=all='0/0 0.5/0.44 0.92/0.895 0.985/0.985 1/1',eq=saturation=1.08,unsharp=5:5:0.6:5:5:0.0"

render() { # name crop pad_colour limiter_ceiling
  local name=$1 crop=$2 pad=$3 lim=$4 dir="build/$1"
  python3 "$name.py" "$dir"
  ffmpeg -y -v error -i "$dir/audio.wav" \
    -af "alimiter=limit=$lim:attack=2:release=60:level=disabled,loudnorm=I=-14:TP=-2.5:LRA=11:linear=true,aresample=44100" -c:a aac -b:a 192k "$dir/audio.m4a"
  ffmpeg -y -v error -f concat -safe 0 -i "$dir/list.txt" -i "$dir/audio.m4a" \
    -vf "fps=30,crop=$crop,scale=1080:-2:flags=lanczos,$CLEAN,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=$pad,format=yuv420p" \
    -c:v libx264 -preset veryfast -crf 16 -colorspace bt709 -color_primaries bt709 -color_trc bt709 \
    -c:a copy -shortest -movflags +faststart "$name.tmp.mp4"
  mv "$name.tmp.mp4" "$name.mp4"
  echo "Wrote $(pwd)/$name.mp4"
}

# crop = w:h:x:y in source pixels: drop side margins (and the Messenger GIF's black bars)
render emma_blocked     696:1000:12:0  0xfcfcfc 0.2
render babe_voice_agent 692:788:14:32  0x060504 0.3
