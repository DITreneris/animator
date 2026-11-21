#!/usr/bin/env bash
# Untitled: voices -> mix -> master -> picture -> mux -> QA. Needs pycairo, numpy, soundfile, ffmpeg, the fonts Lilita One and
# Permanent Marker; for voices.py also kokoro-onnx (KOKORO_DIR) and Tomas's takes (REC); for QA sherpa-onnx Whisper (ASR_DIR).
set -euo pipefail
cd "$(dirname "$0")"
[ -n "${KOKORO_DIR:-}" ] && [ -n "${REC:-}" ] && (cd vo && python3 voices.py)
python3 mix.py && bash master.sh mix.wav fin.wav
python3 rough.py final
ffmpeg -v error -y -i rough_video.mp4 -i fin.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest untitled.mp4
python3 ../qa.py untitled.mp4 633 lines.json
