#!/usr/bin/env bash
# Rebuilds UptimeZ Inc. episodes (540x960 animatics, 30 fps, 15 s) from src/.
# Usage: ./build.sh pt43            one episode (15 s keys below)
#        ./build.sh s131a | s131b    Saved to Cloud A/B test (15 s, 540x960)
#        ./build.sh s136 | s136n     Saved to Cloud release, 1080x1920 (with / without the sniff tag)
#        ./build.sh dlx | dlx_tag    Downloads Expedition v10, 1080x1920, BT.709 (clean / with the promptanatomy.app card)
#        ./build.sh day1 | day1_thumb   How Sofía Survived Day One loop v3, 1080x1920, BT.709 / its cover
#        ./build.sh iwry | iwry_thumb   I Will Replace You animatic v3 (540x960) / its cover
#        ./build.sh all             every episode
#        ./build.sh sheets          brand marks + character sheets
# Needs: python3 (pycairo, numpy, soundfile, kokoro-onnx), ffmpeg,
#        Kokoro model files in $KOKORO_DIR (default: src/models/), Lilita One + Inter fonts.
set -euo pipefail
cd "$(dirname "$0")"
ROOT=../..
HERE=$(pwd)
export KOKORO_DIR=${KOKORO_DIR:-$HERE/src/models}

# fonts used by the kit (installed per-user if missing)
for f in LilitaOne-Regular.ttf Inter-400.ttf Inter-700.ttf Inter-800.ttf PermanentMarker-Regular.ttf; do
  if [ -f "$ROOT/fonts/$f" ] && ! fc-list | grep -qi "${f%%[-.]*}"; then
    mkdir -p ~/.fonts && cp "$ROOT/fonts/$f" ~/.fonts/ && fc-cache -f >/dev/null
  fi
done

# audio chains: v04.3 is louder (compress + limit); earlier cuts use loudnorm
LOUD_OLD="loudnorm=I=-15:TP=-2:LRA=11"
LOUD_43="acompressor=threshold=-24dB:ratio=4:attack=4:release=80:makeup=2,volume=14dB,alimiter=limit=0.60:attack=1:release=50:level=false"

# key | sound script | mix name | output folder | output file | audio chain
EPISODES="
s3|sound.py|s3|storyboards|uptime_S3_check_downloads_storyboard.mp4|OLD
s1|sound.py|s1|storyboards|uptime_S1_saved_to_cloud_storyboard.mp4|OLD
s3b|sound2.py|s3b|storyboards|uptime_S3B_downloads_shadow_ending.mp4|OLD
s3c|sound2.py|s3c|storyboards|uptime_S3C_downloads_role_reversal.mp4|OLD
s1v2|sound2.py|s1v2|storyboards|uptime_S1v2_saved_to_cloud_search_history.mp4|OLD
pta|sound_pt.py|pta|prompt-telephone|uptime_PT_A_bold.mp4|OLD
ptb|sound_pt.py|pta|prompt-telephone|uptime_PT_B_bald.mp4|OLD
pt4|sound_pt4.py|pt4|prompt-telephone|uptime_PT_v04_1.mp4|OLD
pt42|sound_pt42.py|pt42|prompt-telephone|uptimez_PT_v04_2.mp4|OLD
pt43|sound_pt43.py|pt43|prompt-telephone|uptimez_PT_v04_3.mp4|43
s131a|sound_s131.py|s131|saved-to-cloud|uptimez_S131_saved_to_cloud_a.mp4|43
s131b|sound_s131.py|s131|saved-to-cloud|uptimez_S131_saved_to_cloud_b.mp4|43
"

build_one() {
  local line; line=$(echo "$EPISODES" | grep "^$1|") || { echo "unknown episode: $1"; exit 1; }
  IFS='|' read -r key snd mix dir out chain <<<"$line"
  local outdir=${OUT_DIR:-$HERE/$dir}; mkdir -p "$outdir"
  local af=$LOUD_OLD; [ "$chain" = 43 ] && af=$LOUD_43
  ( cd src
    python3 "$snd" "$mix"
    python3 engine.py "$key" | ffmpeg -y -v error \
      -f rawvideo -pix_fmt bgra -s 540x960 -r 30 -i - -i "${mix}_mix.wav" \
      -af "$af" -c:v libx264 -crf 20 -pix_fmt yuv420p -c:a aac -b:a 192k \
      -shortest -movflags +faststart "$outdir/$out.tmp.mp4"
    mv "$outdir/$out.tmp.mp4" "$outdir/$out" )
  echo "Wrote $outdir/$out"
}

# Saved to Cloud release: S1v3.2 audio -> spliced, rebalanced mix; drawn at 2x (needs Noto Color Emoji)
build_release() {
  local m=$1 out; out=${OUT_DIR:-$HERE/saved-to-cloud}; mkdir -p "$out"
  local name=uptimez_S136_saved_to_cloud_$([ "$m" = s136n ] && echo notag || echo tag)_1080.mp4
  ( cd src
    python3 sound_s131.py s131 && python3 sound_s132.py s132 && python3 sound_s136.py "$m"
    python3 engine_hd.py "$m" | ffmpeg -y -v error \
      -f rawvideo -pix_fmt bgra -s 1080x1920 -r 30 -i - -i "${m}_mix.wav" \
      -af "acompressor=threshold=-24dB:ratio=4:attack=4:release=80:makeup=2,volume=18.5dB,alimiter=limit=0.55:attack=1:release=50:level=false" \
      -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k \
      -shortest -movflags +faststart "$out/$name.tmp.mp4"
    mv "$out/$name.tmp.mp4" "$out/$name" )
  echo "Wrote $out/$name"
}

# Downloads Expedition: voice-first mix (sound_dlx.py), automatic layout checks, drawn at 2x
build_dlx() {
  local end=$1 out; out=${OUT_DIR:-$HERE/downloads-expedition}; mkdir -p "$out"
  local name=uptimez_DLX10_expedition${2:+_tag}_1080.mp4
  ( cd src
    python3 sound_dlx.py "$end"
    python3 qa_dlx.py "dlx_${end,,}"
    TAG=${2:+1} python3 engine_hd.py "dlx_${end,,}" | ffmpeg -y -v error \
      -f rawvideo -pix_fmt bgra -s 1080x1920 -r 30 -i - -i "dlx_${end,,}_mix.wav" \
      -af "acompressor=threshold=-24dB:ratio=3:attack=4:release=80:makeup=1,volume=17dB,alimiter=limit=0.6:attack=1:release=50:level=false" \
      -vf scale=out_color_matrix=bt709:out_range=tv -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv \
      -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 \
      -shortest -movflags +faststart "$out/$name.tmp.mp4"
    mv "$out/$name.tmp.mp4" "$out/$name" )
  echo "Wrote $out/$name"
}

# How Sofía Survived Day One: phoneme mouth shapes + looping mix (sound_day1_v4.py), drawn at 2x
build_day1() {
  local out=${OUT_DIR:-$HERE/sofia-day-one} name=uptimez_day1_loop_v3_1080.mp4; mkdir -p "$out"
  ( cd src
    python3 sound_day1_v4.py
    local I G
    I=$(ffmpeg -hide_banner -i day1_mix_v4.wav -af ebur128 -f null - 2>&1 | grep "I:" | tail -1 | awk '{print $2}')
    G=$(python3 -c "print(round(-15.3-($I),2))")
    python3 engine_hd.py day1_anim_v2 | ffmpeg -y -v error \
      -f rawvideo -pix_fmt bgra -s 1080x1920 -r 30 -i - -i day1_mix_v4.wav \
      -af "volume=${G}dB,alimiter=limit=0.5:attack=1:release=40:level=false" \
      -vf scale=out_color_matrix=bt709:out_range=tv,format=yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv \
      -c:v libx264 -preset veryfast -crf 18 -c:a aac -b:a 192k -ar 48000 -t 25 \
      -movflags +faststart "$out/$name.tmp.mp4"
    mv "$out/$name.tmp.mp4" "$out/$name" )
  echo "Wrote $out/$name"
}

# I Will Replace You: storyboard v2 + voiced mix (robot B, de-essed whisper, Don's soft shout)
build_iwry() {
  local out=${OUT_DIR:-$HERE/i-will-replace-you} name=uptimez_iwry_animatic_v3.mp4; mkdir -p "$out"
  ( cd src
    ROBOT=B WHISPER=2 DONSHOUT=2 python3 sound_iwry.py mix
    local I G
    I=$(ffmpeg -hide_banner -i iwry_mix_B_w2_d2.wav -af ebur128 -f null - 2>&1 | grep "I:" | tail -1 | awk '{print $2}')
    G=$(python3 -c "print(round(-15.6-($I),2))")
    python3 engine_v.py iwry_sb_v2 | ffmpeg -y -v error \
      -f rawvideo -pix_fmt bgra -s 540x960 -r 30 -i - -i iwry_mix_B_w2_d2.wav \
      -af "volume=${G}dB,alimiter=limit=0.5:attack=1:release=40:level=false" \
      -vf scale=out_color_matrix=bt709:out_range=tv,format=yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv \
      -c:v libx264 -preset veryfast -crf 18 -c:a aac -b:a 192k -ar 48000 -t 25 \
      -movflags +faststart "$out/$name.tmp.mp4"
    mv "$out/$name.tmp.mp4" "$out/$name" )
  echo "Wrote $out/$name"
}

case "${1:-}" in
  iwry)       build_iwry ;;
  iwry_thumb) ( cd src && python3 thumb_iwry.py "${OUT_DIR:-$HERE/i-will-replace-you}/iwry_thumbnail.png" ) ;;
  day1)       build_day1 ;;
  day1_thumb) ( cd src && python3 thumb_day1.py "${OUT_DIR:-$HERE/sofia-day-one}/day1_thumbnail.png" ) ;;
  dlx)     build_dlx B ;;
  dlx_tag) build_dlx B tag ;;
  s136|s136n) build_release "$1" ;;
  all)    for k in $(echo "$EPISODES" | cut -d'|' -f1); do build_one "$k"; done ;;
  sheets) ( cd src && python3 brand.py && python3 charsheets.py ) ;;
  "")     sed -n 2,6p "$0" ;;
  *)      build_one "$1" ;;
esac
