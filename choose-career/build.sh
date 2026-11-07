#!/usr/bin/env bash
# Builds both cuts of Choose Your Career from src/choose_career_reveal.gif.
# Needs python3 (pillow, numpy, scipy) and ffmpeg.
#   choose_career_reveal_sfx.mp4   original 900x1066 frame (one black row added for an even height)
#   choose_career_reveal_9x16.mp4  1080x1920 for Reels/Shorts/TikTok, meme raised 100 px above centre
set -euo pipefail
cd "$(dirname "$0")"
B=build
python3 sfx.py "$B"
ffmpeg -y -v error -i "$B/audio.wav" -c:a aac -b:a 192k "$B/audio.m4a"

encode() { # name video_filter
  ffmpeg -y -v error -f concat -safe 0 -i "$B/list.txt" -i "$B/audio.m4a" \
    -vf "fps=30,$2,scale=out_color_matrix=bt709:out_range=tv,format=yuv420p" \
    -colorspace bt709 -color_primaries bt709 -color_trc bt709 \
    -c:v libx264 -crf 16 -preset slow -tune stillimage -c:a copy -t 10.2 -movflags +faststart "$1.tmp.mp4"
  mv "$1.tmp.mp4" "$1.mp4"
  echo "Wrote $(pwd)/$1.mp4"
}

encode choose_career_reveal_sfx  "pad=900:1066:0:0:black"
# 900x1065 -> 1080x1278; centred top would be 321 px, raised 100 px clears most of the app's caption area
encode choose_career_reveal_9x16 "scale=1080:1278:flags=lanczos,pad=1080:1920:0:221:0x040404"
