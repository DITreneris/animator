"""Renders the animatic to tmp_video.mp4 (1080x1920, 30 fps, BT.709)."""
import os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); os.chdir(HERE)
import animatic as AN
p = subprocess.Popen(f'ffmpeg -y -v error -f rawvideo -pix_fmt bgra -s 1080x1920 -r 30 -i - -vf format=yuv420p -c:v libx264 -crf 18 -preset veryfast -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709 tmp_video.mp4'.split(), stdin=subprocess.PIPE)
for f in range(AN.NF): p.stdin.write(bytes(AN.draw(f).get_data()))
p.stdin.close(); assert p.wait() == 0; print('video ok', AN.NF)
