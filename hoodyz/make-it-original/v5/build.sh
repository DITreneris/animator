#!/usr/bin/env bash
# Make It Original v5 (the loop): soundtrack, key poses, the seam check and the final 1080x1920 film.
# Reuses v4's shots by import; v4's own files are not touched.
set -euo pipefail
cd "$(dirname "$0")"
python3 mix5.py
../master.sh mix.wav fin.wav
python3 film.py keys
python3 film.py seam
python3 film.py
rm -f mix.wav
