"""Daddy's Home, animation v2: every scene with the PR #62 bubbles (dh_speech), joined into one film and a loop file.

    python3 dh_film_v2.py 3          render scene 3 only (dh_s3_anim_v3.mp4)
    python3 dh_film_v2.py join       join the eight scene files into daddys_home_anim_v2.mp4 and *_loop.mp4

Scene versions: s1 v5, s2 v4, s3 v3, s4 v3, s5 v2, s6 v3, s7 v3, s8 v3 (bubbles only; drawings unchanged)."""
import os
import sys
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE); sys.path.insert(0, HERE)
OUT = "../daddys-home"
VERS = {1: "v5", 2: "v4", 3: "v3", 4: "v3", 5: "v2", 6: "v3", 7: "v3", 8: "v3"}


def render(n):
    import dh_speech as SP
    SP.install()
    if n in (1, 2, 3):
        import dh_anim1, dh_anim2, dh_anim3
        m = {1: dh_anim1, 2: dh_anim2, 3: dh_anim3}[n]
        m.V = VERS[n]
        m.main(1)
    else:
        m = __import__("dh_anim%d" % n)
        m.sc.V = VERS[n]
        m.sc.main(1)


def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]))


def join():
    files = ["%s/dh_s%d_anim_%s.mp4" % (OUT, n, VERS[n]) for n in range(1, 9)]
    lst = "/tmp/dh_film_v2_list.txt"
    open(lst, "w").write("".join("file '%s'\n" % os.path.abspath(f) for f in files))
    out = "%s/daddys_home_anim_v2.mp4" % OUT
    # the sound from each scene's own mix, cut to the scene's length (concatenating the AAC tracks drifts by priming)
    import numpy as np, soundfile as sf
    parts = []
    for n in range(1, 9):
        w, sr = sf.read("/tmp/dh_s%d_%s/a.wav" % (n, VERS[n]))
        L = int(round(dur(files[n - 1]) * sr))
        w = w[:L] if len(w) >= L else np.concatenate([w, np.zeros(L - len(w))])
        parts.append(w)
    sf.write("/tmp/dh_film_v2.wav", np.concatenate(parts), sr)
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-i", "/tmp/dh_film_v2.wav",
                           "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                           "-af", "loudnorm=I=-16:TP=-2:LRA=11,aresample=48000", "-c:a", "aac", "-b:a", "160k", out[:-4] + ".tmp.mp4"])
    os.rename(out[:-4] + ".tmp.mp4", out)
    loop = "%s/daddys_home_anim_v2_loop.mp4" % OUT                    # the film, then its first 3 s again: the join to check
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", out, "-i", out, "-filter_complex",
                           "[1:v]trim=0:3,setpts=PTS-STARTPTS[v1];[1:a]atrim=0:3,asetpts=PTS-STARTPTS[a1];[0:v][0:a][v1][a1]concat=n=2:v=1:a=1[v][a]",
                           "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "19", "-preset", "veryfast", "-pix_fmt", "yuv420p",
                           "-c:a", "aac", "-b:a", "160k", loop[:-4] + ".tmp.mp4"])
    os.rename(loop[:-4] + ".tmp.mp4", loop)
    print("wrote", out, "%.2f s" % dur(out), "and", loop)


if __name__ == "__main__":
    if sys.argv[1:] == ["join"]:
        join()
    else:
        for a in sys.argv[1:]:
            render(int(a))
