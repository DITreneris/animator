E=$1
J=$(ffmpeg -hide_banner -i mix_$E.wav -af 'pan=stereo|c0=c0|c1=c0,loudnorm=I=-14:TP=-2:LRA=11:print_format=json' -f null - 2>&1 | sed -n '/^{/,/^}/p')
g(){ echo "$J" | python3 -c "import json,sys;print(json.load(sys.stdin)['$1'])"; }
ffmpeg -v error -y -i mix_$E.wav -af "pan=stereo|c0=c0|c1=c0,loudnorm=I=-14:TP=-2:LRA=11:measured_I=$(g input_i):measured_TP=$(g input_tp):measured_LRA=$(g input_lra):measured_thresh=$(g input_thresh):offset=$(g target_offset):linear=true,aresample=48000,alimiter=limit=0.66:level=false" -ar 48000 fin_$E.wav
