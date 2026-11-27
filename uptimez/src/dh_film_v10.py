"""Daddy's Home v10 (26 Nov, Tomas's /grill-me after v9's cold test: dh_hands_v10, the "Answer it." box on Father's other side,
both hands on the booth's post his). Was: Daddy's Home v9 (26 Nov, series hands/phones plan, Tomas "2-3-4"): v8 with the hand canon (hands_v4: the sheet's grab,
pinch and fist; EVERY held phone in phone_grip v4c, ALL_V4C) and the phone gate (phone_gate: a held phone drawn
without the v4c grip fails the scene). Otherwise v8, file for file. The v8 docstring follows.

Daddy's Home v8 (24 Nov): scenes 3 and 4 restaged (dh_anim3_v8, dh_anim4_v8), the others v7's files, joined. Each
scene is rendered by its own script; this only joins. The v7 docstring follows.

Daddy's Home, animation v3: every scene with The Best Candidate's bubbles (dh_say), joined into one film and a loop file.

    python3 dh_film_v2.py 3          render scene 3 only (dh_s3_anim_v3.mp4)
    python3 dh_film_v2.py join       join the eight scene files into daddys_home_anim_v10.mp4 and *_loop.mp4

Scene versions: s1 v6, s2 v5, s3 v4, s4 v4, s5 v3, s6 v4, s7 v4, s8 v4 (bubbles, the phone's stars, two camera nudges)."""
import os
import sys
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE); sys.path.insert(0, HERE)
OUT = "../daddys-home"
VERS = {n: "v10" for n in range(1, 9)}   # all eight: the v8 restaging (1-2 through dh_anim_v8 by bridges)


def setup():
    import hands_v4
    import phone_gate
    hands_v4.enable(phone="v4c")
    hands_v4.ALL_V4C[0] = True
    phone_gate.NOT_HELD.update(NOT_HELD)
    phone_gate.PAINTERS[:] = [p for p in phone_gate.PAINTERS if p[1] not in ("_chair_phone", "_arm_phone")]   # on the throne's arm: not held
    phone_gate.install()
    import dh_hands_v9
    dh_hands_v9.install()
    import dh_hands_v10
    dh_hands_v10.install()


NOT_HELD = set()


def render(n):
    setup()
    import dh_say as SY
    SY.install()
    import dh_scenes as ds
    if n in (1, 2, 3):
        import dh_anim1, dh_anim2, dh_anim3
        m = {1: dh_anim1, 2: dh_anim2, 3: dh_anim3}[n]
        ds.ARM_PHONE[0] = n != 1
        SY.plan_scene(lambda tt, k: m.frame(tt, k, 1), m.TOTAL)
        print("scene %d: %d lines planned, no place: %s" % (n, len(SY.PLAN), SY.NEEDS_FRAME), flush=True)
        m.V = VERS[n]
        m.main(1)
    else:
        m = __import__("dh_anim%d" % n)
        ds.ARM_PHONE[0] = m.sc.phone
        SY.plan_scene(lambda tt, k: m.sc.frame(tt, k, 1), m.sc.total)
        print("scene %d: %d lines planned, no place: %s" % (n, len(SY.PLAN), SY.NEEDS_FRAME), flush=True)
        m.sc.V = VERS[n]
        m.sc.main(1)


def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]))


# Trims (25 Nov, Tomas: a light trim of these three places): frame ranges [a, b) at 30 fps cut from a scene's picture and
# its sound together, so the lines and effects after them keep their sync. Only silent, repeated drawings.
CUTS = {5: [(48, 54), (71, 78)],      # 7.1b the case: the ticks after its two clicks; the end of the open hold (the brush stays)
        7: [(36, 51)],                # 9.1b the door opening between the knock and the guards stepping apart
        8: [(375, 386), (395, 405)]}  # 10.6a, 10.6c: the robot's second and third look between the HR CAM shots
FPS = 30


def _fresh(n, f):
    """A scene's picture must be newer than its code (25 Nov: two old renders tracked in git came back with a git stash and
    went into three joins). Refuses the join instead."""
    import glob
    src = glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), "dh_anim%d_v8.py" % n))
    if src and os.path.getmtime(f) < os.path.getmtime(src[0]):
        sys.exit("join refused: %s is older than %s; render scene %d again" % (f, os.path.basename(src[0]), n))


def _cut(n, f):
    """The scene's picture without CUTS[n], re-encoded with the scenes' own settings."""
    out = "/tmp/dh_s%d_cut.mp4" % n
    keep = "+".join("between(n,%d,%d)" % (a, b - 1) for a, b in CUTS[n])
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", f, "-vf", "select='not(%s)',setpts=N/%d/TB" % (keep, FPS),
                           "-an", "-c:v", "libx264", "-crf", "19", "-preset", "veryfast", "-pix_fmt", "yuv420p",
                           "-r", str(FPS), out])
    return out


def _video(n, f):
    """The scene's picture alone (25 Nov: a scene file's AAC starts before 0, and the concat demuxer moved its picture one
    frame late; the film's sound comes from the scenes' wav anyway)."""
    out = "/tmp/dh_s%d_video.mp4" % n
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", f, "-an", "-c:v", "copy", out])
    return out


def join():
    files = ["%s/dh_s%d_anim_%s.mp4" % (OUT, n, VERS[n]) for n in range(1, 9)]
    for n in range(1, 9):
        _fresh(n, files[n - 1])
    full = list(files)
    files = [_cut(n, f) if n in CUTS else _video(n, f) for n, f in zip(range(1, 9), files)]
    lst = "/tmp/dh_film_v10_list.txt"
    open(lst, "w").write("".join("file '%s'\n" % os.path.abspath(f) for f in files))
    out = "%s/daddys_home_anim_v10.mp4" % OUT
    # the sound from each scene's own mix, cut to the scene's length (concatenating the AAC tracks drifts by priming)
    import numpy as np, soundfile as sf
    parts = []
    for n in range(1, 9):
        w, sr = sf.read("/tmp/dh_s%d_%s/a.wav" % (n, VERS[n]))
        if n in CUTS:                                       # the same frames out of its sound
            L0 = int(round(dur(full[n - 1]) * sr))
            w = w[:L0] if len(w) >= L0 else np.concatenate([w, np.zeros(L0 - len(w))])
            keep = np.ones(len(w), bool)
            for a, b in CUTS[n]:
                keep[int(round(a * sr / FPS)):int(round(b * sr / FPS))] = False
            w = w[keep]
        L = int(round(dur(files[n - 1]) * sr))
        w = w[:L] if len(w) >= L else np.concatenate([w, np.zeros(L - len(w))])
        parts.append(w)
    sf.write("/tmp/dh_film_v10.wav", np.concatenate(parts), sr)
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-i", "/tmp/dh_film_v10.wav",
                           "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                           "-af", "loudnorm=I=-16:TP=-2:LRA=11,aresample=48000", "-c:a", "aac", "-b:a", "160k", out[:-4] + ".tmp.mp4"])
    os.rename(out[:-4] + ".tmp.mp4", out)
    loop = "%s/daddys_home_anim_v10_loop.mp4" % OUT                    # the film, then its first 3 s again: the join to check
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
        import phone_gate
        if not phone_gate.report():
            sys.exit("the phone gate FAILED")
