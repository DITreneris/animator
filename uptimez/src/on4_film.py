"""OFFICE NOIR 4: the whole film, every shot moving, 24 drawings a second (24 Nov). No text yet (cards, bubbles, lips
come on the approved motion). The motion tests at sub=2 (on4_motion), the held shots' final animation (on4_anim), the
rough's sound moved onto the new times (on4_rough.sound). Renders are not committed (.gitignore, 24 Nov).

  python3 on4_film.py  ->  ../office-noir-4/on4_film_v1.mp4 (540x960, 24 fps, AAC, -15 LUFS)"""
import os
import shutil
import subprocess
import numpy as np
import soundfile as sf
import on4_scenes as sc
import on4_motion as m
import on4_anim as an
import on4_rough as r

DPS = 24
SR = r.SR
VER = "v1"
OUT = os.path.join(sc.OUT, "on4_film_%s.mp4" % VER)
MOT = {("1.1", "1.2"): ("T1", 0, 78), ("2.2", "2.3"): ("T2", 0, None), ("2.4",): ("T7", 0, None),
       ("3.1", "3.2"): ("T3", 0, None), ("3.3", "3.3b", "3.4", "3.5"): ("T6", 0, None), ("3.6",): ("T8", 0, None),
       ("4.4",): ("T12", 0, None), ("6.0",): ("T9", 0, None), ("6.05",): ("T10", 0, None), ("6.07",): ("T11", 0, None),
       ("6.3", "6.6"): ("T4", 0, -16), ("8.1", "8.2"): ("T5", 0, -14)}


def frames(tmp):
    tm, d = sc._timing()
    ids = [x["id"] for _, ss in sc.SCENES for x in ss]
    n = 0; cuts = []
    i = 0
    while i < len(ids):
        grp = next((g for g in MOT if g[0] == ids[i]), None)
        span = grp if grp else (ids[i],)
        end = tm[span[-1]]["start"] + tm[span[-1]]["dur"]
        count = int(round(end * DPS)) - n
        cuts.append((ids[i], n))
        if grp:
            t, a, b = MOT[grp]
            fr = m.TESTS[t](sub=2)[a:b]
            pick = fr[:count] if len(fr) >= count else [fr[min(len(fr) - 1, int(j * len(fr) / count))] for j in range(count)]
            last = None
            for s in pick:
                p = "%s/%05d.png" % (tmp, n)
                if s is last:
                    os.symlink("%05d.png" % (n - 1), p)
                else:
                    s.write_to_png(p)
                last = s; n += 1
        else:
            f, dur = an.SHOTS[ids[i]]
            for j in range(count):
                f(j / float(DPS)).write_to_png("%s/%05d.png" % (tmp, n)); n += 1
        print(span, n, flush=True)
        i += len(span)
    return tm, d, n, cuts


def master(mix, tmp):
    mix = mix / max(1e-6, np.abs(mix).max()) * 0.5
    def lufs(a):
        sf.write(tmp + "/a.wav", a.astype(np.float32), SR)
        q = subprocess.run(["ffmpeg", "-hide_banner", "-i", tmp + "/a.wav", "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True)
        return float([l for l in q.stderr.splitlines() if "I:" in l][-1].split("I:")[1].split("LUFS")[0])
    g = 10 ** ((-15.0 - lufs(mix)) / 20.0)
    for _ in range(5):
        out = np.tanh(mix * g / 0.56) * 0.56
        I = lufs(out)
        if abs(I + 15.0) < 0.3:
            break
        g *= 10 ** ((-15.0 - I) / 20.0)
    return out


def main():
    tmp = "/tmp/on4_film"; shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    tm, d, n, cuts = frames(tmp)
    total = n / float(DPS)
    mix, marks, ev = r.sound(tm, d, total)
    out = master(mix, tmp)
    np.save(tmp + "/marks.npy", np.array(marks, dtype=object), allow_pickle=True)
    t_ = OUT[:-4] + "_tmp.mp4"
    q = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(DPS), "-i", tmp + "/%05d.png", "-i", tmp + "/a.wav",
                        "-vf", "format=yuv420p", "-c:v", "libx264", "-crf", "18", "-preset", "veryfast",
                        "-c:a", "aac", "-b:a", "160k", "-t", "%.3f" % total, t_])
    if q.returncode == 0:
        os.replace(t_, OUT)
    print(OUT, n, "drawings", round(total, 2), "s", "cuts", cuts, "marks", marks, ev)


if __name__ == "__main__":
    main()
