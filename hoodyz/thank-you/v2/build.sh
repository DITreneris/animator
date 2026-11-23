#!/usr/bin/env bash
# Thank You v2: mix -> master -> picture -> mux -> safe-zone gate -> QA. Imports v1 (../v1) untouched.
# Needs pycairo, numpy, soundfile, ffmpeg, the font Lilita One; for QA sherpa-onnx Whisper (ASR_DIR).
set -euo pipefail
cd "$(dirname "$0")"
python3 audio.py && ./master.sh mix.wav fin.wav
python3 - <<'PY'
import subprocess, sys
sys.argv = ['film.py']
import film as F
p = subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','bgra','-s','1080x1920','-r','30','-i','-',
    '-c:v','libx264','-crf','18','-preset','veryfast','-pix_fmt','yuv420p','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','video.mp4'], stdin=subprocess.PIPE)
for f in range(F.NF): p.stdin.write(bytes(F.draw(f).get_data()))
p.stdin.close(); sys.exit(p.wait())
PY
ffmpeg -y -v error -i video.mp4 -i fin.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -movflags +faststart thank_you_v2.mp4
python3 -c "import film as F; F.draw(F.START['G'] + 45).write_to_png('cover.png')"
rm -f video.mp4 fin.wav mix.wav
python3 safe.py
python3 ../../qa.py thank_you_v2.mp4 475 lines.json
