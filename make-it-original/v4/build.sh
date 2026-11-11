#!/usr/bin/env bash
# Make It Original v4 (the master): soundtrack, key poses and the final 1080x1920 film.
# Needs python3 (pycairo, numpy, soundfile, pillow), ffmpeg and the Lilita One font. Uses ../v3 (version A's shots), ../kit.py, ../sound.py, ../vo.
set -euo pipefail
cd "$(dirname "$0")"
python3 mix4.py
../master.sh mix.wav fin.wav
python3 film.py keys
python3 film.py
python3 cover.py
rm -f mix.wav
