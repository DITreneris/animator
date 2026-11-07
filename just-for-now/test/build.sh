#!/usr/bin/env bash
# Renders the two rough-test clips (scenes 5-6 only), one per Tester line:
# just_for_now_test_back.mp4 ("Should I put it back?") and just_for_now_test_passed.mp4 ("Test passed.").
set -euo pipefail
cd "$(dirname "$0")"
if ! fc-list | grep -qi "Lilita One"; then
  mkdir -p ~/.fonts && cp ../../fonts/LilitaOne-Regular.ttf ~/.fonts/ && fc-cache -f >/dev/null
fi
VAR=back python3 render.py render
VAR=passed python3 render.py render g
python3 audio.py
for V in back passed; do
  printf "file '%s.mp4'\n" a b c d e f "g_$V" > list.txt
  ffmpeg -y -v error -f concat -i list.txt -c copy video.mp4
  ffmpeg -y -v error -i "mix_$V.wav" -af "lowpass=f=15000,volume=2dB,alimiter=limit=0.78:level=false,aresample=48000" -c:a pcm_s16le fin.wav
  ffmpeg -y -v error -i video.mp4 -i fin.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart "just_for_now_test_$V.tmp.mp4"
  mv "just_for_now_test_$V.tmp.mp4" "just_for_now_test_$V.mp4"
done
rm -f a.mp4 b.mp4 c.mp4 d.mp4 e.mp4 f.mp4 g_back.mp4 g_passed.mp4 list.txt video.mp4 fin.wav mix_back.wav mix_passed.wav chk_*.png sheet.png
echo "Wrote $(pwd)/just_for_now_test_back.mp4 and just_for_now_test_passed.mp4"
