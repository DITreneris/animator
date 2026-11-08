#!/usr/bin/env bash
# Renders the four Learn to Code versions (1080x1920, 30 fps, 25 s). Needs python3 (pycairo, numpy, pillow) and ffmpeg.
#   learn_to_code_A.mp4          ending A: "Worse. Our AIs promoted each other."  (ENDING=A)
#   learn_to_code_B_v2.mp4       ending B: "Any news on my application?" / "My AI is still talking with your AI."  (ENDING=B2)
#   learn_to_code_B_v3.mp4       B v2 + polish: push-ins, big bubbles, bigger charger, cable coil  (POLISH=1)
#   learn_to_code_B_v3_notag.mp4 B v3 with no chip, TODAY clear of the edge, ends on the board meeting  (NOTAG=1)
set -euo pipefail
cd "$(dirname "$0")"
ROOT=..
if ! fc-list | grep -qi "Lilita One"; then
  mkdir -p ~/.fonts && cp "$ROOT/fonts/LilitaOne-Regular.ttf" ~/.fonts/ && fc-cache -f >/dev/null
fi
build () {  # $1 output name, $2 audio master, then scene files
  local out=$1 wav=$2; shift 2
  printf "file '%s'\n" "$@" > list.txt
  ffmpeg -y -v error -f concat -i list.txt -c copy video.mp4
  ffmpeg -y -v error -i video.mp4 -i "$wav" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart "$out.tmp.mp4"
  mv "$out.tmp.mp4" "$out.mp4"; echo "Wrote $(pwd)/$out.mp4"
}
# audio: mix, then master to -14 LUFS stereo
python3 audio.py A;  bash master.sh A
python3 audio.py B2; bash master.sh B2
NOTAG=1 python3 audio.py B2; bash master.sh B2_notag
# pictures: only the scenes a version changes are rendered again
ENDING=A python3 ltc.py render                       # a b c d e A_f
ENDING=B2 python3 ltc.py render f                    # B2_f
POLISH=1 ENDING=B2 python3 ltc.py render a d e f     # pa pd pe pB2_f
NOTAG=1 POLISH=1 ENDING=B2 python3 ltc.py render a f # npa npB2_f
build learn_to_code_A           fin_A.wav        a.mp4 b.mp4 c.mp4 d.mp4 e.mp4 A_f.mp4
build learn_to_code_B_v2        fin_B2.wav       a.mp4 b.mp4 c.mp4 d.mp4 e.mp4 B2_f.mp4
build learn_to_code_B_v3        fin_B2.wav       pa.mp4 b.mp4 c.mp4 pd.mp4 pe.mp4 pB2_f.mp4
build learn_to_code_B_v3_notag  fin_B2_notag.wav npa.mp4 b.mp4 c.mp4 pd.mp4 pe.mp4 npB2_f.mp4
rm -f a.mp4 b.mp4 c.mp4 d.mp4 e.mp4 A_f.mp4 B2_f.mp4 pa.mp4 pd.mp4 pe.mp4 pB2_f.mp4 npa.mp4 npB2_f.mp4 \
      list.txt video.mp4 mix_*.wav fin_*.wav chk_*.png sheet.png
