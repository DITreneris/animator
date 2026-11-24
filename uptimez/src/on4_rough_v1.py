"""OFFICE NOIR 4: the first moving rough, v1 (24 Nov). An animatic from the scene file (on4_scenes.py, timing v2): every
shot's key drawing held for its time; the five motion-tested beats (on4_motion.py v3: the punch, the envelope, STOP-GO and
the bump from the side, the arm coming down, the loop) moving at 12 drawings a second; the four voice takes of stage 2
(on4_voices/takes_v1) at their shots. No music, no effects, no bubbles yet: this is for timing and reading.

  python3 on4_motion.py && python3 on4_rough.py  ->  ../office-noir-4/on4_rough_v1.mp4 (540x960, 24 fps, AAC)"""
import os
import shutil
import subprocess
import numpy as np
import soundfile as sf
import on4_scenes as sc
import on4_voices as vo

FPS = 12
MOT = {("1.1", "1.2"): ("T1", 0, 31), ("2.2", "2.3"): ("T2", 0, None), ("3.1", "3.2"): ("T3", 0, None),
       ("6.3", "6.6"): ("T4", 0, -8), ("8.1", "8.2"): ("T5", 0, -7)}
OUT = os.path.join(sc.OUT, "on4_rough_v1.mp4")


def main():
    tm, d = sc._timing()
    shots = [x for _, ss in sc.SCENES for x in ss]
    ids = [x["id"] for x in shots]
    tmp = "/tmp/on4_rough"; shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    n = 0
    def put(path, count):
        nonlocal n
        for _ in range(count):
            os.symlink(path, "%s/%05d.png" % (tmp, n)); n += 1
    i = 0
    while i < len(ids):
        grp = next((g for g in MOT if g[0] == ids[i]), None)
        span = grp if grp else (ids[i],)
        end = tm[span[-1]]["start"] + tm[span[-1]]["dur"]
        count = int(round(end * FPS)) - n
        if grp:
            t, a, b = MOT[grp]
            files = sorted(os.listdir("/tmp/on4_mot/" + t))[a:b]
            if len(files) >= count:
                pick = files[:count]
            else:
                pick = [files[min(len(files) - 1, int(j * len(files) / count))] for j in range(count)]
            for f in pick:
                put("/tmp/on4_mot/%s/%s" % (t, f), 1)
        else:
            s, _ = sc.render(shots[i], 1)
            p = "%s/key_%s.png" % (tmp, ids[i]); s.write_to_png(p); put(p, count)
        i += len(span)
    total = n / FPS
    SR = 48000
    mix = np.zeros(int((total + 0.1) * SR), np.float32)
    for key, ln in d["lines"].items():
        a, sr = sf.read(os.path.join(vo.OUT, "takes_v1", key + ".wav"))
        if a.ndim > 1:
            a = a.mean(1)
        if sr != SR:
            a = np.interp(np.arange(0, len(a), sr / SR), np.arange(len(a)), a)
        t0 = tm[ln["shot"]]["start"] + vo.LEAD.get(ln["shot"], 0.3)
        j = int(t0 * SR); a = a[:len(mix) - j]
        mix[j:j + len(a)] += a.astype(np.float32)
        print("line", key, ln["shot"], round(t0, 2))
    mix *= 0.5 / max(1e-6, np.abs(mix).max())
    sf.write(tmp + "/a.wav", mix, SR)
    t_ = OUT[:-4] + "_tmp.mp4"
    r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", tmp + "/%05d.png", "-i", tmp + "/a.wav",
                        "-vf", "fps=24,format=yuv420p", "-c:v", "libx264", "-crf", "20", "-preset", "veryfast",
                        "-c:a", "aac", "-b:a", "128k", "-t", "%.3f" % total, t_])
    if r.returncode == 0:
        os.replace(t_, OUT)
    print(OUT, n, "drawings", round(total, 2), "s")


if __name__ == "__main__":
    main()
