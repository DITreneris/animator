"""OFFICE NOIR 3: the release build (iteration 4, 22 Nov). Film v33 with the animatic v29's timing, lines and mix, the
level set with a true-peak ceiling of -2 dBTP so that the AAC stays under -1. Writes the 540x960 master and, from it,
a 1080x1920 file. NOTE: the 1080 file is the 540 picture scaled up (lanczos), not drawn at 1080: this film's noir pass,
light and masks work on 540x960 pixels. It is named _1080up so nobody takes it for a native render.
  KOKORO_DIR=... python3 on3_master.py"""
import os
import subprocess
import sys
os.environ.setdefault("ON3_TP", "-2.0")  # release_v6: film v38
import on3_animatic as an

an.V = "release_v6"
D = "../office-noir-3/"
if __name__ == "__main__":
    total, held, lines = an.build(D + "office_noir_3_release_v6_540.mp4")
    print("%.2f s" % total)
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", D + "office_noir_3_release_v6_540.mp4", "-vf", "scale=1080:1920:flags=lanczos,format=yuv420p",
                           "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709",
                           "-color_trc", "bt709", "-movflags", "+faststart", "-c:a", "copy", D + "office_noir_3_release_v6_1080up.mp4"])
