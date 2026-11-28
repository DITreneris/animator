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

VER = "v23"                                                   # v2: the pauses in the sound only; v3 (24 Nov): the town's bills and chalk, the sky, the old-town finish
po.ON[0] = True; st.TOWN[0] = True
import on4_cross as xc
m.CRASH[0] = True; m.LAW[0] = True; m.CAR_S = xc.S_CAR      # v4: the bump as a tap; v5: one scale law on the crossing, the plank bounces
m.TESTS.update(xc.TESTS)                                     # v5: the crossing after the bump in four shots (W, R, B, G), not one wide take
sc.DUR.update({"3.2": 2.8, "3.3": 88 / 12.0, "3.4": 36 / 12.0, "3.5": 52 / 12.0})   # 3.3 is halved between 3.3 and 3.3b: 44 drawings each
CEIL = 0.50                                                  # v4: 0.56 gave -0.9 dBFS after AAC with the new effects (the limit is -1)
sc.DUR["2.3"] = 2.75; r.NEW["c1"] = ("2.2", 2.95, "CLIENT", "Mine until it's done.")   # v11: the handover has its beats (52 keys); his line as it goes under his lapel
r.CLEAR += ["f1", "p2", "p3", "c1"]; r.RETAKE.update(f1=os.path.join(r.vo.OUT, "takes_v5", "f1.wav"), p2=os.path.join(r.vo.OUT, "takes_v5", "p2.wav"))   # takes chosen through the master's own chain (knee, AAC)   # v12: the lines the recognizer lost in the mix stand alone
xc.FWD[0] = True; import on4_club as _cl; _cl.TUBE[0] = True   # v13: the car drives on forward past her; the motto as neon tubing
m.GIVE[0] = True                                             # v11: Dad's hand gives the envelope, the Client takes it
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
r.RETAKE.update(f1=os.path.join(r.vo.OUT, "takes_v5", "f1.wav"), p2=os.path.join(r.vo.OUT, "takes_v5", "p2.wav"))   # v12 (after the v4 takes above, which were overriding these)
m.HIT[0] = True; m.TEETER[0] = True; xc.FAR[0] = True   # v15 (cold test of v14): the punch as a blow; the second after the tap acted; the car in the far lane, the bills in the air as it leaves
an.BIG53[0] = True; sc.BURN[0] = True; sc.CV_SOFIA[0] = True; an.ARCH14[0] = True; m.OTS44[0] = True; an.LIFT2[0] = True; m.SIGN_OUT[0] = True   # v16 (cold test of v14, second round)
an.END2[0] = True; r.END2[0] = True; m.END_HOLD[0] = 6     # v16 (Tomas: the ending too long, Sofia too small): the rota once, Sofia from the waist up
sc.DUR.update({"7.1": 1.2, "7.2": 2.6, "7.3": 1.2, "7.4": 0.0, "7.5": 1.8, "8.1": 3.6 - 8 / 12.0})
an.LOW21[0] = True                                          # the words: her head under the card in 2.1
r.NEW["p3"] = (r.NEW["p3"][0], r.NEW["p3"][1], r.NEW["p3"][2], "Anyone?"); r.RETAKE["p3"] = os.path.join(r.vo.OUT, "takes_v6", "p3_any.wav")   # v17 (Tomas): "Well?" was never heard in the mix (1 of 3; four new takes 0 of 3); "Anyone?" is heard 3 of 3 and is the fourth "nobody"
import on4_cast as _oc
m.CAT_SOFT[0] = True; m.TUCK[0] = True; m.RING_GOLD[0] = True; m.WALK12[0] = True; an.THUMB62[0] = True; _oc.TAIL[0] = True   # v17: the cat whole with two eyes, the envelope behind his lapel, a gold ring, two strides on the crossing, a hand on the CV, her tail
import on4_weather as _wx; _wx.ON[0] = True; _wx.LIGHT[0] = True   # v18: Office Noir 3's light on the dream (light_on3.auto), Office Noir 2's rain on the street, wet cobbles, grain
_wx.SIDE[0] = True                                          # v19: side light (frame and figures), one fainter rain layer, grain halved, the light at 0.5 (Tomas: "a little too dark")
m.LOOP2[0] = True; _wx.SEAM[0] = True; sc.DUR.update({"8.1": 2.2, "8.2": 1.3})   # v20 (the loop, Tomas's picks): the dark 1 s, the lane up through it over 1.2 s, the eyes where the cat leaps from, one rain and one light through the seam, the opening three keys shorter
m.CAT3[0] = True; m.CAT4[0] = True; m.CAT5[0] = True       # v21: the cat leaps straight at the camera again, one detailed cat on all seven drawings, over the camera and away; a shake on the lens drawing
_wx.SHAKE[0] = True; import on4_club as _cl; _cl.CHASE[0] = True   # v22: the camera jolts on the blows; the theatre's bulbs run, the dealers deal (steam and the tail's follow left off: they did not read)
V23 = os.environ.get("V23", "1") == "1"
if V23:                                                      # v23 (cold test of v22; Tomas's picks)
    r.NEW["e1"] = ("3.2", 0.97, "PAM", "Excuse me?")         # on the bumper, to the car, still standing
    r.NARR["n8"] = ("3.2", 2.15, "Nobody stops for me.")     # on the fall itself, not after it (after her "Excuse me?")
    m.CARRY2[0] = True; m.PEEL2[0] = True; xc.MONEY2[0] = True; xc.DEPTH_R[0] = True; an.SOF2[0] = True
    sc.DUR.update({"3.4": 24 / 12.0, "6.05": 0.0})           # the bills in 1 s; the cut to the Client in her act is out (0.9 s)
MUG_END = os.environ.get("MUG_END", "0") == "1"
if MUG_END:                                                  # v24 (28 Nov, Tomas's /grill-me and two reviews): Don's empty mug, the kiss, the drawer
    VER = "v24"
    an.MUG_END[0] = True; an.mug_end(); sc.MUG_END[0] = True; r.MUG[0] = True
    import copy as _cp
    for _t, _ss in sc.SCENES:
        _ids = [x["id"] for x in _ss]
        if "7.5" in _ids and "7.6" not in _ids:
            _n = _cp.copy(_ss[_ids.index("7.5")]); _n["id"] = "7.6"; _n["size"] = "insert, the drawer from above"
            _n["picture"] = "The drawer: fifteen of his CEO mugs and one gap. Hers goes in; she turns its handle to line up."
            _n["cast"] = (); _n["after"] = None; _n["protect"] = ()
            _ss.insert(_ids.index("7.5") + 1, _n)
    sc.DUR.update({"7.1": 1.0, "7.2": 2.4, "7.3": 1.0, "7.4": 0.7, "7.5": 1.9, "7.6": 1.8, "8.1": 1.4, "8.2": 3.0})   # 8.2: T5 whole (the dark 1 s, the eyes, the lane up to frame 0): 1.5 s cut the loop off (found by the frame-0 check on v25)
    r.NEW["d3"] = ("7.2", 0.55, "DON", "Only for you.")     # he says it as the mug goes up into her hand; not a look; done before he walks out
    def _end81(cam):
        o = an._probe(692, 742, 0.50, "down", "happy", (0, 0.2), "arm_up_open")
        return m.draw(m.shot("8.1", cam=cam, cast=[an.P("pam_awake", 692, 742, 0.50, "down", "happy", (0, 0.2), "arm_up_open")],
                             after=lambda k: an._mark(k, o, 0.5), protect=()))
    m.END81[0] = _end81
    def _mug_heart(c, x, y):                                 # (Tomas) his CEO mug where the envelope stood; the loop's heart glows on its side
        import on4_props as _p
        _p.don_mug(sc.Ctx(c, 0), x, y + 66, 1.65)          # big and low: CEO under the heart, the heart where frame 0's neon heart is
    m.MUG_HEART[0] = _mug_heart
TRIM = MUG_END and os.environ.get("TRIM", "0") == "1"
HEAD = set()                                                 # trimmed shots that keep their speed and lose their end
ORIG = {}                                                    # shot -> its length before the trim (the source drawings a trimmed shot is resampled from)
if TRIM:                                                     # v25 (28 Nov, Tomas's /grill-me on the pace: "the tempo drops in the middle"): 20-52 s tightened, nothing redrawn
    VER = "v25"
    _tm0 = sc._timing()[0]
    K = 1.25                                                 # (Tomas, after the first segment at 1.5: "a touch slower, say 1.25")
    NEWDUR = {"3.3": _tm0["3.3"]["dur"] / K, "3.3b": _tm0["3.3b"]["dur"] / K, "3.4": _tm0["3.4"]["dur"] / K, "3.5": _tm0["3.5"]["dur"] / K, "3.6": 3.7, "4.3": 2.0, "4.4": _tm0["4.4"]["dur"] / K, "6.6": 1.5}
    for _k, _v in NEWDUR.items():
        ORIG[_k] = _tm0[_k]["dur"]; r.SPEED[_k] = _v / _tm0[_k]["dur"]
    sc.DUR.update({"3.3": NEWDUR["3.3"] * 2, "3.4": NEWDUR["3.4"], "3.5": NEWDUR["3.5"], "3.6": 3.7, "4.3": 2.0, "4.4": NEWDUR["4.4"], "6.6": 1.5})   # 3.3 is halved between 3.3 and 3.3b
    HEAD.add("3.6"); r.SPEED["3.6"] = 1.0                    # (Tomas, the segment at 0:17: "a cut shows") 3.6 at its own speed, its standing hold cut off the end:
                                                             # squeezed evenly, her plank rise took 0.3 s and jumped, and the band's entry (2.5 s in) fell on a still drawing
    r.NEW["d2"] = ("3.3", 2.1, "DON", "Not a scratch."); r.NEW["f1"] = ("3.3b", 0.8, "FATHER", "For the boys.")
    r.MOVE7["n3"] = ("3.5", 1.2)                             # "I am like a cat. I have seven lives." starts as they carry her: no 8 s without a word
    _a43 = an.SHOTS["4.3"][0]; _k43 = ORIG["4.3"] / 2.0
    an.SHOTS["4.3"] = ((lambda t: _a43(t * _k43)), 2.0)      # the same acting, faster: one point at the sign, one at herself


def pick(fr, span, tm, count):
    """the drawings of a motion group for the film. Untrimmed: the first count of them, as ever. Trimmed: each shot's
    own stretch of the source (its old length), spread evenly over its new length"""
    if not any(s in ORIG for s in span):
        return fr[:count] if len(fr) >= count else [fr[min(len(fr) - 1, int(j * len(fr) / count))] for j in range(count)]
    out = []; a = 0
    for q, s in enumerate(span):
        n0 = int(round(ORIG.get(s, tm[s]["dur"]) * DPS))
        src = fr[a:a + n0] if q < len(span) - 1 else fr[a:a + n0] or fr[-1:]
        a += n0
        n1 = count - len(out) if q == len(span) - 1 else int(round(tm[s]["dur"] * DPS))
        src = src or fr[-1:]
        if s in HEAD:
            out += [src[min(len(src) - 1, j)] for j in range(n1)]
        else:
            out += [src[min(len(src) - 1, int(j * len(src) / float(n1)))] for j in range(n1)]
    return out


OUT = os.path.join(sc.OUT, "on4_film_%s.mp4" % VER)
MOT = {("1.1", "1.2"): ("T1", 0, 78), ("2.2", "2.3"): ("T2", 0, None), ("2.4",): ("T7", 0, None),
       ("3.1", "3.2"): ("T3", 0, None), ("3.3", "3.3b", "3.4", "3.5"): ("T6", 0, None), ("3.6",): ("T8", 0, None),
       ("4.4",): ("T12", 0, None), ("6.0",): ("T9", 0, None), ("6.05",): ("T10", 0, None), ("6.07",): ("T11", 0, None),
       ("6.3", "6.6"): ("T4", 0, -16), ("8.1", "8.2"): ("T5", 0, -14)}
del MOT[("3.3", "3.3b", "3.4", "3.5")]                       # v5
MOT[("6.3", "6.6")] = ("T4", 0, None); MOT[("8.1", "8.2")] = ("T5", 0, None)   # v7: DENSE's own counts (56 and 58 keys)
MOT.update({("3.3",): ("W", 0, None), ("3.3b",): ("R", 0, None), ("3.4",): ("B", 0, None), ("3.5",): ("G", 0, None)})
if MUG_END:                                                  # v24: 8.1 is the mug ending's own (on4_anim.m81); T5's dark is 8.2 alone
    del MOT[("8.1", "8.2")]; MOT[("8.2",)] = ("T5", 0, None)
if V23:
    MOT.pop(("6.05",), None)                                 # v23: the cut to the Client in her act is out


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
            last = None
            for s in pick(fr, span, tm, count):
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
