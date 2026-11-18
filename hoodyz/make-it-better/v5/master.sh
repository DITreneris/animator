#!/usr/bin/env bash
# Masters a mono mix to stereo, -14 LUFS, true peak under -1 dBTP (limiter 0.5 + 15 kHz low-pass: the v3 setting overshot to -0.3 after AAC on rough 3) after AAC. Usage: master.sh mix.wav fin.wav
set -euo pipefail
J=$(ffmpeg -hide_banner -i "$1" -af 'pan=stereo|c0=c0|c1=c0,loudnorm=I=-14:TP=-2:LRA=11:print_format=json' -f null - 2>&1 | sed -n '/^{/,/^}/p')
g(){ echo "$J" | python3 -c "import json,sys;print(json.load(sys.stdin)['$1'])"; }
ffmpeg -v error -y -i "$1" -af "pan=stereo|c0=c0|c1=c0,loudnorm=I=-14:TP=-2:LRA=11:measured_I=$(g input_i):measured_TP=$(g input_tp):measured_LRA=$(g input_lra):measured_thresh=$(g input_thresh):offset=$(g target_offset):linear=true,aresample=48000,lowpass=f=15000,alimiter=limit=0.5:attack=2:release=40:level=false" -ar 48000 "$2"
