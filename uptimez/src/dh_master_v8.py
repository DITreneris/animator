"""Daddy's Home v8: the 1080x1920 master. Each scene is drawn again at twice the size by its own v8 module (the same drawings,
the same bubbles in the same order), picture only; the film is then joined with dh_film_v8's CUTS and the same sound as the
540 film, and compared with it frame by frame (the 1080 scaled down; PSNR per frame).
  python3 dh_master_v8.py [1-8 ...]   ->  ../daddys-home/dh_s{n}_anim_v8_1080.mp4   (no scenes given: all eight)
  python3 dh_master_v8.py join        ->  ../daddys-home/daddys_home_anim_v8_1080.mp4 and the PSNR check"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE); sys.path.insert(0, HERE)
import dh_film_v8 as fv
import dh_scenes as ds
import dh_anim_v8 as E
import dh_anim3_v8 as A3

DPS = 12


def _setup(n):
    """The scene's module and its frame function, with its speech installed and its held boxes cleared, as its own render."""
    m = __import__("dh_anim%d_v8" % n)
    if n in (3, 4):
        m.install_speech()
        fr = m.frame
        total = m.TOTAL if n == 3 else m.sc.total
        ds.ARM_PHONE[0] = True
    else:
        E.install_speech(m)
        fr = m.frame8
        total = m.sc.total
        ds.ARM_PHONE[0] = m.sc.phone
    A3.HELD.clear(); A3.R_HELD.clear(); del A3.CHECKS[:]
    return fr, total


def render(n):
    fr, total = _setup(n)
    tmp = "/tmp/dh_s%d_v8_1080" % n; os.makedirs(tmp, exist_ok=True)
    N = int(round(total * DPS)); lst = []
    for i in range(N):
        surf, sid = fr(i / float(DPS), i, 2)
        p = "%s/d_%04d.png" % (tmp, i); surf.write_to_png(p)
        lst.append("file '%s'\nduration %.5f\n" % (p, 1.0 / DPS))
    lst.append("file '%s'\n" % p)
    open(tmp + "/list.txt", "w").write("".join(lst))
    out = "%s/dh_s%d_anim_v8_1080.mp4" % (fv.OUT, n)
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", tmp + "/list.txt",
                           "-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-crf", "19", "-preset", "veryfast",
                           "-t", "%.3f" % total, out[:-4] + ".tmp.mp4"])
    os.rename(out[:-4] + ".tmp.mp4", out)
    print("wrote", out, "%d drawings, %d bubble checks with faults" % (N, len([c for c in A3.CHECKS if c[2]])))


def join():
    vers = dict(fv.VERS)
    fv.VERS.update({n: vers[n] + "_1080" for n in range(1, 9)})
    real_wav = {n: "/tmp/dh_s%d_%s/a.wav" % (n, vers[n]) for n in range(1, 9)}
    for n in range(1, 9):                                   # the same sound as the 540 film
        d = "/tmp/dh_s%d_%s" % (n, fv.VERS[n]); os.makedirs(d, exist_ok=True)
        if not os.path.exists(d + "/a.wav"):
            os.symlink(real_wav[n], d + "/a.wav")
    src = {n: "dh_anim%d_v8.py" % n for n in range(1, 9)}
    out = "%s/daddys_home_anim_v8.mp4" % fv.OUT
    keep = out + ".540.keep"
    os.rename(out, keep)                                    # fv.join writes the 540 name: keep the 540 film aside
    loop = "%s/daddys_home_anim_v8_loop.mp4" % fv.OUT; loop_keep = loop + ".540.keep"
    if os.path.exists(loop):
        os.rename(loop, loop_keep)
    try:
        fv.join()
        os.rename(out, "%s/daddys_home_anim_v8_1080.mp4" % fv.OUT)
        os.rename(loop, "%s/daddys_home_anim_v8_1080_loop.mp4" % fv.OUT)
    finally:
        os.rename(keep, out)
        if os.path.exists(loop_keep):
            os.rename(loop_keep, loop)
    m = "%s/daddys_home_anim_v8_1080.mp4" % fv.OUT
    psnr = subprocess.run(["ffmpeg", "-i", m, "-i", out, "-lavfi", "[0:v]scale=540:960:flags=area[a];[a][1:v]psnr=stats_file=/tmp/dh_psnr.txt",
                           "-f", "null", "-"], capture_output=True, text=True).stderr
    vals = [float(l.split("psnr_avg:")[1].split()[0]) for l in open("/tmp/dh_psnr.txt") if "psnr_avg:" in l and "inf" not in l.split("psnr_avg:")[1].split()[0]]
    low = sorted((v, i) for i, v in enumerate(vals))[:5]
    print("master:", m, "PSNR vs the 540 film: mean %.1f dB, lowest frames %s" % (sum(vals) / len(vals), [(i, round(v, 1)) for v, i in low]))


if __name__ == "__main__":
    a = sys.argv[1:]
    if a == ["join"]:
        join()
    else:
        for n in (map(int, a) if a else range(1, 9)):
            render(n)
