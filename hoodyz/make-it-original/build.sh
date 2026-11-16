#!/usr/bin/env bash
# Make It Original (Hoodyz ep. 4): audio auditions, character sheets and the rough.
# Needs: python3 with pycairo, numpy, soundfile, pillow; ffmpeg; the Lilita One font (fonts/ in this repo).
# The scratch voices in vo/ are committed; vo/voices.py regenerates them (needs kokoro-onnx model files).
set -euo pipefail
cd "$(dirname "$0")"
python3 riffs.py                    # originality screen of the riff candidates
python3 auditions.py                # aud/make_it_original_auditions.mp4 + WAVs
python3 sheet.py                    # sheet_cast.png, sheet_faces.png
python3 mix.py                      # mix.wav + lips.npy
./master.sh mix.wav fin.wav         # stereo, -14 LUFS
python3 rough.py                    # make_it_original_rough.mp4
rm -f mix.wav lips.npy sheet_*_phone.png aud/card_*.png aud/cards.txt aud/reel.wav
