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
import on4_posters as po
import on4_street as st

VER = "v9"                                                   # v2: the pauses in the sound only; v3 (24 Nov): the town's bills and chalk, the sky, the old-town finish
po.ON[0] = True; st.TOWN[0] = True
import on4_cross as xc
m.CRASH[0] = True; m.LAW[0] = True; m.CAR_S = xc.S_CAR      # v4: the bump as a tap; v5: one scale law on the crossing, the plank bounces
m.TESTS.update(xc.TESTS)                                     # v5: the crossing after the bump in four shots (W, R, B, G), not one wide take
sc.DUR.update({"3.2": 2.8, "3.3": 88 / 12.0, "3.4": 22 / 12.0, "3.5": 52 / 12.0})   # 3.3 is halved between 3.3 and 3.3b: 44 drawings each
CEIL = 0.50                                                  # v4: 0.56 gave -0.9 dBFS after AAC with the new effects (the limit is -1)
m.CATWALK[0] = True                                          # v9: her cat's walk over the crossing and along the fire escape; the car drives up in 2.1; the hunting face
m.PEEK[0] = True                                             # v8: she watches from the window over the car
m.DENSE[0] = True                                            # v7: twelve different drawings a second in 2.2-2.3, 2.4's fall, 6.3-6.6, 8.1-8.2
r.SCENE3[0] = "cross"                                        # v4: the crossing's sound after the bump; v5: on the four shots
r.NARR["n8"] = ("3.3", 0.3, "Nobody stops for me.")          # v4 (Tomas): as she lies there and waves, and they all step over her
r.NEW["d1"] = ("3.1", 1.25, "DON", "Traffic flows.")         # clear of his whistle on the tap
r.NEW["d2"] = ("3.3", 2.9, "DON", "Not a scratch.")          # after her line; where he holds the glove up: clean
r.NEW["f1"] = ("3.3b", 1.0, "FATHER", "For the boys.")       # as the ringed hand lets the bills go
r.RETAKE["d2"] = os.path.join(r.vo.OUT, "takes_v4", "d2.wav")   # a slower take (0.82): the first was not heard in the mix
r.RETAKE["f1"] = os.path.join(r.vo.OUT, "takes_v4", "f1.wav")   # "For, the boys." at 0.8, -1 semitone: heard 3 of 3 alone
OUT = os.path.join(sc.OUT, "on4_film_%s.mp4" % VER)
MOT = {("1.1", "1.2"): ("T1", 0, 78), ("2.2", "2.3"): ("T2", 0, None), ("2.4",): ("T7", 0, None),
       ("3.1", "3.2"): ("T3", 0, None), ("3.3", "3.3b", "3.4", "3.5"): ("T6", 0, None), ("3.6",): ("T8", 0, None),
       ("4.4",): ("T12", 0, None), ("6.0",): ("T9", 0, None), ("6.05",): ("T10", 0, None), ("6.07",): ("T11", 0, None),
       ("6.3", "6.6"): ("T4", 0, -16), ("8.1", "8.2"): ("T5", 0, -14)}
del MOT[("3.3", "3.3b", "3.4", "3.5")]                       # v5
MOT[("6.3", "6.6")] = ("T4", 0, None); MOT[("8.1", "8.2")] = ("T5", 0, None)   # v7: DENSE's own counts (56 and 58 keys)
MOT.update({("3.3",): ("W", 0, None), ("3.3b",): ("R", 0, None), ("3.4",): ("B", 0, None), ("3.5",): ("G", 0, None)})


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
        out = np.tanh(mix * g / CEIL) * CEIL
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
                        "-c:a", "aac", "-b:a", "192k", "-t", "%.3f" % total, t_])
    if q.returncode == 0:
        os.replace(t_, OUT)
    print(OUT, n, "drawings", round(total, 2), "s", "cuts", cuts, "marks", marks, ev)


if __name__ == "__main__":
    main()
