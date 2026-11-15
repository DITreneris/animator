#!/bin/bash
# flat gain to -14 LUFS (capped by -1.5 dBTP), peak-safety limiter, mux onto untouched video
set -e
cd /home/claude/part3
M=$(ffmpeg -i snd/mix.wav -af "loudnorm=I=-14:TP=-2:print_format=json" -f null - 2>&1 | tail -n 13)
I=$(echo "$M" | grep -oP '"input_i"\s*:\s*"\K[-\d.]+'); TP=$(echo "$M" | grep -oP '"input_tp"\s*:\s*"\K[-\d.]+')
G=$(python3 -I -c "print(round(min(-14.0-$I, -1.5-$TP + 4.5), 2))")   # allow limiter to take up to 3 dB of peaks
echo "mix I=$I TP=$TP -> gain $G dB"
ffmpeg -y -v error -i snd/mix.wav -af "volume=${G}dB,alimiter=limit=0.84:attack=2:release=60:level=disabled" -ar 48000 snd/mix_norm.wav
ffmpeg -y -v error -i in/src.mp4 -i snd/mix_norm.wav -c:v copy -c:a aac -b:a 192k -map 0:v:0 -map 1:a:0 -shortest "$1"
ffmpeg -y -v error -i "$1" -ac 1 -ar 16000 /home/claude/tagger/final16k.wav
