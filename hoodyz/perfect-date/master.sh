#!/usr/bin/env bash
# Masters a mono mix to stereo at -14 LUFS without touching its dynamics: one linear gain, then a peak limiter.
# (The series loudnorm master switches to dynamic mode when loudness range > 11 LU and flattens the punchline.)
# Usage: master.sh mix.wav fin.wav
set -euo pipefail
meas(){ ffmpeg -hide_banner -i "$1" -af ebur128 -f null - 2>&1 | awk '/Summary/{s=1} s&&/ I:/{print $2; exit}'; }
ffmpeg -v error -y -i "$1" -af 'pan=stereo|c0=c0|c1=c0' -ar 48000 _st.wav
G=$(python3 -c "print(-14-($(meas _st.wav)))")
for pass in 1 2; do
  ffmpeg -v error -y -i _st.wav -af "volume=${G}dB,alimiter=limit=0.70:attack=4:release=60:level=false" -ar 48000 "$2"
  G=$(python3 -c "print($G+(-14-($(meas "$2"))))")
done
rm -f _st.wav
