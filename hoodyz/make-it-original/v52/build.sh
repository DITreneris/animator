#!/usr/bin/env bash
# Make It Original v5.2: v5.1 plus the visible rejection and the 18 Nov drummer take. v5 and v4 are imported, not touched.
set -euo pipefail
cd "$(dirname "$0")"
python3 mix52.py
../master.sh mix.wav fin.wav
python3 film.py keys
python3 film.py seam
python3 film.py
rm -f mix.wav
