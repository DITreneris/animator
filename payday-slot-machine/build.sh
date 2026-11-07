#!/usr/bin/env bash
# Renders Payday_Slot_Machine.mp4 (1080x1920, 30 fps, 19 s). Needs python3 (pillow, numpy) and ffmpeg.
set -euo pipefail
cd "$(dirname "$0")"
python3 render.py audio
ffmpeg -y -v error -i audio.wav -af "alimiter=limit=0.4:attack=1:release=60:level=false,loudnorm=I=-14:TP=-2.5:LRA=11:linear=true,aresample=44100" -c:a aac -b:a 192k audio.m4a
ids="hook employee freelancer founder vibecoder endline"
mkdir -p scenes
printf '%s\n' $ids | xargs -P"${JOBS:-2}" -I{} python3 render.py scene {}
printf "file '%s.mp4'\n" $ids > scenes/list.txt
ffmpeg -y -v error -f concat -safe 0 -i scenes/list.txt -c copy v.mp4
ffmpeg -y -v error -i v.mp4 -i audio.m4a -map 0:v -map 1:a -c copy -movflags +faststart -t 19 Payday_Slot_Machine.tmp.mp4
mv Payday_Slot_Machine.tmp.mp4 Payday_Slot_Machine.mp4
rm -f v.mp4
echo "Wrote $(pwd)/Payday_Slot_Machine.mp4"
