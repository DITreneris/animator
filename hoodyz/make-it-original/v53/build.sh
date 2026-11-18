#!/usr/bin/env bash
# Make It Original v5.3: v5.2 plus the visible punchline (his tap on play, MY AI's SOURCE stamp). v5.2, v5 and v4 are imported, not touched.
set -euo pipefail
cd "$(dirname "$0")"
python3 mix53.py
../master.sh mix.wav fin.wav
python3 film.py keys
python3 film.py seam
python3 film.py
rm -f mix.wav
