"""DADDY'S HOME v8, scene 4 "The Wrong Man", animated from shot list v2 (daddys-home-s4-shot-list-v2.md) and the
frames of dh_s4_v8.py (round 3, on the set gate). Same clock, same takes, same sound as v7 (dh_anim4.sc): only the
pictures change. v7 is untouched. Bubbles, the dead zones and the set gate are scene 3 v8's (dh_anim3_v8), shared.
  4A (5.1)        the visitor already in, mid-step, the robot's back near: "I'm here to inspect the machine."
  4B (5.2)        the line: Mom, Don rubbing his hands, Sofía
  4C (5.3)        Don's arm sweeps the room open: "Of course. We've been expecting you."
  4D (5.4)        Pam at the counter, her eyes go down to his case
  4D' (5.4')      the insert: the pass, COFFEE SERVICE
  4D'' (5.4'')    her mug, nothing in it
  4E (6.1-6.1'')  the shredder running ("Complete..."), Don steps in front of it ("...transparency."), the sticker slapped
                  on ("Premium. On us.")
  4F (6.2)        the robot over the visitor's shoulder: "Premium search is non-functional." (cut by the next line)
  4G (6.3)        Don, close, the smile fixed: "Then make it lifetime."
  4H (6.4)        the visitor looks down at the sticker and up at Don, over Don's shoulder. HOLD.
  python3 dh_anim4_v8.py [nobub|gate]  ->  ../daddys-home/dh_s4_anim_v8.mp4"""
import os
import subprocess
import sys
import cairo
import kit
import hands_ps as hp
import fs_storyboard as sb
import dh_props as dp
import dh_layout as dl
import dh_scenes as ds
import dh_cast as dc
import dh_back as db
import dh_anim1 as A
import dh_anim4 as V7
import dh_anim3_v8 as A3                                    # say(), the zones, the speech install: shared with scene 3 v8
import dh_s4_v8 as S
from dh_anim import don_at, DS_
from kit import Ctx

V = "v8"
sc = V7.sc
DPS, F, CH = A3.DPS, sb.F, dp.CHAIR
OUT = "../daddys-home"
ROWS, T0, TOTAL = sc.rows, sc.T0, sc.total
seq = V7.seq
NOBUB = A3.NOBUB
THR = dl.CH[0]                                              # the throne on its set mark in every shot (S.THR4 448 is within 4)
VX = S.VX - 8                                               # the visitor in 4E and 4H (round 2: -16, his head clear of the tag; round 4: 8 back, so Don reaches him)
DONX = 466                                                  # Don in 4E and 4G


def say(k, text, cam, head, n):
    if NOBUB[0]:
        return
    hx, hy, _ = S.to_screen(cam, *head)
    A3.say(k, text, (hx, hy), n)


# ------------------------------------------------------------------ 4A
def r_a(k, o, t, tt, n):
    x = seq(t, [84, 98, 112, 122, 128])                     # caught mid-step, already in (v7's walk)
    bob = seq(t, [0, -5, 0, -4, 0])
    if 1.05 <= t < 1.40:                                    # round 4 (cold test: 2 s and nothing moves): a half step in
        bob = (-4, 0, -3, 0)[min(3, int((t - 1.05) * DPS))]; x += 6 * min(1.0, (t - 1.05) / 0.3)
    elif t >= 1.40:
        x += 6
    look = (0.6, 0) if t < 0.5 else ((-0.7, 0.1) if t < 0.95 else ((0.8, -0.1) if t < 1.45 else (0.2, 0.2)))   # round the room
    hp.reset("relax", "grab")
    with A.About(k.c, x, F + 8, 1.0, 1.0, bob):
        q = dc.repairman(k, x, F + 8, S.GS, case=True, look=look)
    o["head"] = q["head"]


def fg_a(k, cam, tt, n, box):
    A3.AVOID_EXTRA[:] = []
    S.a_fg(k, cam)
    if sc.speaking("5.2", tt):
        say(k, "I'm here to inspect the machine.", cam, box["head"], n)


# ------------------------------------------------------------------ 4B: the line (no line spoken)
def r_b(k, o, t, tt, n):
    S.D4B_POSE[0] = (-22, 62 + (6 if n % 2 else 0), 22, -62 - (6 if n % 2 else 0))   # he rubs his hands
    S.b_people(k, o)


def fg_none(k, cam, tt, n, box):
    A3.AVOID_EXTRA[:] = []


# ------------------------------------------------------------------ 4C: the sweep
def r_c(k, o, t, tt, n):
    dp.ceo_chair(k, S.THR4, CH[1], CH[2])
    hp.reset("palm", "relax")
    u = min(1.0, t / 0.25)
    pose = (-40 - 64 * u, 20 - 44 * u, 30, 10)              # the arm swings out and open in three drawings
    d = don_at(k, S.LINE[1][0], S.LINE[1][1], pose, "happy", (-1, 0), tt)
    A.mouth(k, d["head"], DS_, sc.loud("5.3", tt))
    o["head"] = d["head"]


def fg_c(k, cam, tt, n, box):
    A3.AVOID_EXTRA[:] = []
    if sc.speaking("5.3", tt):
        say(k, "Of course." if sc.since("5.3", tt) < 0.72 else "We've been expecting you.", cam, box["head"], n)


# ------------------------------------------------------------------ 4D, 4D'': Pam (no line)
def r_d(k, o, t, tt, n):
    hp.reset("quiet", "quiet")
    look = (-0.7, -0.1) if t < 0.17 else (-0.7, 0.8)        # at him, then down at his case
    ds.pb.pam(k, S.PAM[0], S.PAM[1], dl.PS, "stand", "neutral", look=look, glasses="up")


def fg_d(k, cam, tt, n, box):
    A3.AVOID_EXTRA[:] = []
    S.d_fg(k, cam)


def r_d2(k, o, t, tt, n):
    """5.4'' (round 4): the mug goes over in three drawings, its empty mouth to us; she looks in; her mouth opens, shuts."""
    S.MUG_TIP[0] = seq(t, [0.0, 0.0, 0.35, 0.75, 1.0])
    S.d2_people(k, o)
    S.MUG_TIP[0] = 0.0


def fg_d2(k, cam, tt, n, box):
    A3.AVOID_EXTRA[:] = []
    S.COUNTER[0] = 925; S.d_fg(k, cam); S.COUNTER[0] = 745


def i_pass(k, c, t, tt, n):
    S.d1_insert(k, c)


# ------------------------------------------------------------------ 4E: one held frame, three beats
def visitor(k, o, look):
    hp.reset("relax", "grab")
    q = dc.repairman(k, VX, S.VF, S.GS, case=True, look=look)
    o["vhead"] = q["head"]
    return q


def r_e(k, o, t, tt, n):
    dp.ceo_chair(k, THR, CH[1], CH[2])
    sid = [s for s, _ in ROWS if T0[s] <= tt + 1e-6][-1]
    if sid == "6.1":                                        # (a) the shredder eats a page; the visitor's eyes on it
        V7.shredding(k, n)
        visitor(k, o, (0.8, 0.4))
        x, pose = DONX, (-8, 0, 8, 0)
    elif sid == "6.1'":                                     # (b) Don steps sideways in front of it, arms a little out
        V7.shredding(k, n)
        visitor(k, o, (0.8, 0.2))
        x, pose = DONX + 40 * min(1.0, t / 0.25), (-30, 0, 30, 0)
    else:                                                   # (c) round 4 (cold test: "the sticker just appears"; rules 223, 225):
        i = int(t * DPS + 1e-6)                             # he comes back with it in his hand (shown), presses it on with
        on = i >= 3                                         # his palm (the burst), keeps the palm on it, then lets go
        visitor(k, o, (0.2, 1) if i >= 5 else (0.6, 0.2))
        x = DONX + 40 - 52 * min(1.0, t / 0.083)          # he steps in (his head stays clear of the tag) and reaches him at full arm
        if i >= 8:
            x = DONX - 12 + 12 * min(1.0, (t - 8.0 / DPS) / 0.25)   # and back
        stick = stuck_at()
        if on:
            draw_sticker(k, *stick)
        if i < 3:                                           # the sticker in his hand, held up toward the visitor
            pose = (-60 - 15 * i, -20 - 4 * i, 8, 0)           # his other arm down: his right is the box's wall
        elif i < 8:                                         # the palm flat on it, contact all the way
            pose = reach(x, stick)
        else:                                               # let go: the hand drops to his side, the sticker stays
            pose = (-30, 0, 8, 0)
        if 3 <= i <= 4:
            ds._lines(k, [(stick[0] - 50, stick[1] - 40, stick[0] - 62, stick[1] - 52), (stick[0] + 30, stick[1] - 44, stick[0] + 40, stick[1] - 58),
                          (stick[0] - 56, stick[1] + 18, stick[0] - 70, stick[1] + 22)])
        hp.reset("palm", "relax")
        if i < 3:                                           # the object first, at his hand; his fingers drawn over it
            scratch = Ctx(cairo.Context(cairo.ImageSurface(cairo.FORMAT_ARGB32, 4, 4)), 0)
            hx, hy = _don_real()(scratch, x, F + 26, DS_, pose, "happy")["hands"][0]
            draw_sticker(k, hx - 14, hy - 6, S.GS * 0.85)
        d = don_at(k, x, F + 26, pose, "happy", (-1, 0), tt, still=True)
        A.mouth(k, d["head"], DS_, max(sc.loud("6.1a", tt), sc.loud("6.1b", tt)))
        o["head"] = d["head"]
        return
    hp.reset("palm", "relax")
    d = don_at(k, x, F + 26, pose, "happy", (-1, 0), tt)
    A.mouth(k, d["head"], DS_, max(sc.loud("6.1a", tt), sc.loud("6.1b", tt)))
    o["head"] = d["head"]


def fg_e(k, cam, tt, n, box):
    A3.AVOID_EXTRA[:] = []
    if tt >= T0["6.1''"]:                                   # the sticker is the point of this line: no box on it
        sx, sy = sticker_at(VX, S.VF)
        x0, y0, _ = S.to_screen(cam, sx - 50 * S.GS, sy - 50 * S.GS)
        x1, y1, _ = S.to_screen(cam, sx + 50 * S.GS, sy + 50 * S.GS)
        A3.AVOID_EXTRA.append((x0, y0, x1, y1))
    if sc.speaking("6.1a", tt):
        say(k, "Complete..." if tt < T0["6.1'"] else "...transparency.", cam, box["head"], n)
    for t_ in ("Premium.", "On us."):                       # his right (the throne side): his left is the sticker and his palm
        A3.HELD.setdefault(t_, (None, 1))
    if sc.speaking("6.1b", tt):
        say(k, "Premium." if sc.since("6.1b", tt) < 0.62 else "On us.", cam, box["head"], n)


def sticker_at(x, feet):
    """Where ds._sticker puts the PREMIUM sticker on the visitor (its centre), in world units."""
    return (x - 10 * S.GS, feet + (ds.co_BT + 80) * S.GS)


def draw_sticker(k, cx, cy, s_=None):
    import math as m_
    s_ = s_ or S.GS
    pts = [(cx + m_.cos(2 * m_.pi * i / 24) * (46 if i % 2 else 39) * s_, cy + m_.sin(2 * m_.pi * i / 24) * (46 if i % 2 else 39) * s_) for i in range(24)]
    kit.cut(k, pts, dp.GOLD, lw=2)
    kit.text(k, "PREMIUM", cx, cy + 5 * s_, 16.5 * s_, kit.INK)


_REACH = {}


def _don_real():
    return getattr(sb.don, "_real", sb.don)                 # a measuring pass is not a drawing: the set gate must not log it
STUCK = [None]                                              # where his palm put the sticker (set once; 4H draws it there too)


def stuck_at():
    """Where the sticker goes: as near the pass as Don's palm reaches from DONX - 12."""
    if STUCK[0] is None:
        want = sticker_at(VX, S.VF)
        scratch = Ctx(cairo.Context(cairo.ImageSurface(cairo.FORMAT_ARGB32, 4, 4)), 0)
        h = _don_real()(scratch, DONX - 12, F + 26, DS_, reach(DONX - 12, want), "happy")["hands"][0]
        STUCK[0] = (h[0] - 10, want[1]) if h[0] - 10 > want[0] else want
    return STUCK[0]


def reach(x, target):
    """Don's arm angles putting his screen-left hand on target (world units), by search; cached."""
    key = (round(x), round(target[0]), round(target[1]))
    if key not in _REACH:
        scratch = Ctx(cairo.Context(cairo.ImageSurface(cairo.FORMAT_ARGB32, 4, 4)), 0)
        best = None
        for a0 in range(-130, -20, 4):
            for a1 in range(-90, 60, 4):
                h = _don_real()(scratch, x, F + 26, DS_, (a0, a1, 8, 0), "happy")["hands"][0]
                d2 = (h[0] - target[0]) ** 2 + (h[1] - target[1]) ** 2
                if best is None or d2 < best[0]:
                    best = (d2, (a0, a1, 8, 0))
        _REACH[key] = best[1]
    return _REACH[key]


# ------------------------------------------------------------------ 4F: the robot, over the visitor's shoulder
def r_f(k, o, t, tt, n):
    """6.2 (round 4: it held 2 s, nothing moving): the robot bobs on its words, as v7's r_robot."""
    import dh_animatic as da
    dy = robot_bob(tt, n)
    k.c.save(); k.c.translate(0, dy); da._rb("idle")(k, o); k.c.restore()
    o["robot_head"] = (da.RH[0], da.RH[1] + dy)


def fg_f(k, cam, tt, n, box):
    A3.AVOID_EXTRA[:] = []
    S.f_fg(k, cam)
    if sc.speaking("6.2", tt) and box.get("robot_head"):
        say(k, "Premium search is non-functional.", cam, box["robot_head"], n)


def r_f_robot(k, o, t, tt, n):
    if "robot" in o:
        o["robot_head"] = o["robot"]["screen"]


def robot_bob(tt, n):
    return -2 if (sc.speaking("6.2", tt) and n % 2) else 0   # small: its box follows the antenna (at -4 it jumped)


# ------------------------------------------------------------------ 4G: Don, close
CAM_4G = (440, 640, 3.6)                                   # the tag whole on his left (at 470 the frame cut it)


def r_g(k, o, t, tt, n):
    dp.ceo_chair(k, THR, CH[1], CH[2])
    hp.reset("fist", "fist")
    d = don_at(k, DONX, F + 26, (-14, 0, 14, 0), "happy", (1, 0), tt)   # eyes on the visitor (right); the smile fixed
    A.mouth(k, d["head"], DS_, sc.loud("6.3", tt))
    o["head"] = d["head"]


def fg_g(k, cam, tt, n, box):
    A3.AVOID_EXTRA[:] = []
    if sc.speaking("6.3", tt):
        say(k, "Then make it lifetime.", cam, box["head"], n)


# ------------------------------------------------------------------ 4H: down at the sticker, up at Don. HOLD
def r_h(k, o, t, tt, n):
    lean = seq(t, [0.0, 0.05, 0.09, 0.09, 0.09, 0.05, 0.0])
    c = k.c
    py = S.VF - 150 * S.GS
    c.save(); c.translate(VX, py); c.rotate(lean); c.translate(-VX, -py)
    hp.reset("relax", "grab")
    dc.repairman(k, VX, S.VF, S.GS, case=True, look=(0.15, 1) if lean > 0 else (-0.3, 0.2))
    draw_sticker(k, *stuck_at())                            # where his palm put it in 4E
    c.restore()


def fg_h(k, cam, tt, n, box):
    A3.AVOID_EXTRA[:] = []
    S.h_fg(k, cam)


SHOTS = {"5.1": ("4A", r_a, fg_a, False), "5.2": ("4B", r_b, fg_none, False), "5.3": ("4C", r_c, fg_c, False),
         "5.4": ("4D", r_d, fg_d, False), "5.4''": ("4D2", r_d2, fg_d2, False),
         "6.1": ("4E", r_e, fg_e, False), "6.1'": ("4E", r_e, fg_e, False), "6.1''": ("4E", r_e, fg_e, False),
         "6.2": ("4F", r_f, fg_f, False), "6.3": ("4G", r_g, fg_g, False), "6.4": ("4H", r_h, fg_h, False)}
def _m(cam, dx=0, dy=0):
    return (cam[0] + dx, cam[1] + dy, cam[2])


CAMS = {"4A": S.CAM_4A, "4B": (480, 712, 2.3), "4C": _m(S.CAM_4C, 0, -8), "4D": S.CAM_4D, "4D2": S.CAM_4D2,
        "4E": (426, 618, 1.72), "4F": _m(S.CAM_4F, 0, 14), "4G": CAM_4G, "4H": S.CAM_4H}
# (gate, 24 Nov) 4B up: Sofía's face out of the app buttons; 4C, 4E down: the tag's string under the title bar;
# 4F up: the robot's face out of the caption quarter
INS = {"5.4'": i_pass}
SHIFT_CAM = {}
SET_MOVES = {}
SET_AIR = set()
SET_BEHIND = set()
SET_WALKS = set()
ENTRANCES = {("5.1", "visitor")}
FOREGROUND = {("5.1", "robot"), ("6.4", "don_back")}         # over-the-shoulder pieces from behind: no face shows, the edge is the point


def frame(tt, n, hi=1):
    sid = [s for s, _ in ROWS if T0[s] <= tt + 1e-6][-1]
    t = tt - T0[sid]
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540 * hi, 960 * hi); c = cairo.Context(surf); c.scale(hi, hi)
    k = Ctx(c, 0)
    dp.TAG_ANG[0] = 0.0
    kit.HAND[0] = hp.hand
    try:
        if sid in INS:
            INS[sid](k, c, t, tt, n)
            return surf, sid
        name, draw, fg, robot = SHOTS[sid]
        cam = CAMS[name]
        if sid in SHIFT_CAM:                                # a cut in for one line (the camera only, lesson 358)
            cam = SHIFT_CAM[sid]
        box = {}

        def fn(k_, o_):
            box.update(o_)
            draw(k_, box, t, tt, n)
        sh = dl.shot(name, [], fn, "", rb=robot, chair=False, cam=cam, ymin=0)
        cam = dl.draw(sh, k)
        c.identity_matrix(); c.scale(hi, hi)
        fg(k, cam, tt, n, box)
    finally:
        kit.HAND[0] = None
    return surf, sid


def install_speech():
    import dh_speech as SP
    SY = A3.install_speech()
    SP._fresh(sys.modules[__name__], "frame")
    return SY


def gate():
    """Every drawing: speech_gate per line, the apps' dead zones, the set gate. Exit 1 on any."""
    import collections, math
    import dh_speech as SP
    import set_gate
    SY = install_speech(); ds.ARM_PHONE[0] = True
    A3.HELD.clear(); A3.R_HELD.clear(); del A3.CHECKS[:]
    set_gate.install(); del set_gate.SEQ[:]
    me = sys.modules[__name__]
    zc = collections.Counter(); sc_ = collections.Counter()
    for n in range(int(round(TOTAL * DPS))):
        set_gate.begin(None)
        surf, sid = me.frame(n / float(DPS), n, 1)
        set_gate.SEQ[-1] = (sid, list(set_gate.LOG))
        for f_ in set_gate.faults(sid, moves=SET_MOVES, air=SET_AIR, behind=SET_BEHIND):
            sc_[(sid, f_)] += 1
        if sid in INS:
            continue
        seen = []
        for rec in SP.REG:
            try:
                ms = SY.measure(rec); hx, hy = SP._frame_matrix(rec).transform_point(*rec["head_u"])
            except Exception:
                continue
            if any(math.hypot(hx - a, hy - b) < 0.5 * ms["r"] for a, b in seen):
                continue
            seen.append((hx, hy)); r = ms["r"] * 0.8
            if -r < hx < 540 + r and -r < hy < 960 + r:
                for f_ in A3.zone_faults((hx - r, hy - r, hx + r, hy + r), "face"):
                    if f_ == "at the frame's edge" and (sid, rec.get("name")) in ENTRANCES and n - int(T0[sid] * DPS) < 2:
                        continue
                    if (sid, rec.get("name")) in FOREGROUND:
                        continue
                    zc[("face %s" % rec.get("name"), sid, f_)] += 1
        for a in A3._avoid(solid=True):
            for f_ in A3.zone_faults(a, "sign"):
                zc[("sign", sid, f_)] += 1
    by = collections.OrderedDict()
    for n, text, faults in A3.CHECKS:
        b = by.setdefault(text, [0, 0, collections.Counter()]); b[0] += 1
        if faults:
            b[1] += 1; b[2].update(faults)
    bad = 0
    for text, (nn, nf, cnt) in by.items():
        print("%-36s %3d drawings %3d with faults  %s" % (text, nn, nf, dict(cnt)))
        bad += nf
    print("speech_gate: %d bubble drawings, %d with faults" % (len(A3.CHECKS), bad))
    for (what, sid, f_), v in sorted(zc.items()):
        print("ZONE %-14s %-5s %-22s %d drawings" % (what, sid, f_, v))
    print("dead zones: %d drawings with a face or sign in them" % sum(zc.values()))
    for (sid, f_), v in sorted(sc_.items()):
        print("SET %-5s %s  %d drawings" % (sid, f_, v))
    cuts = set_gate.cut_faults(walks=SET_WALKS)
    for f_ in cuts:
        print(f_)
    print("set: %d drawings off the set, %d cuts that move someone" % (sum(sc_.values()), len(cuts)))
    return bad + sum(zc.values()) + sum(sc_.values()) + len(cuts)


def main(hi=1):
    tmp = "/tmp/dh_s4_%s%s" % (V, "_mute" if NOBUB[0] else ""); os.makedirs(tmp, exist_ok=True)
    ds.ARM_PHONE[0] = True
    me = sys.modules[__name__]
    N = int(round(TOTAL * DPS)); lst = []
    for n in range(N):
        surf, sid = me.frame(n / float(DPS), n, hi)
        p = "%s/d_%04d.png" % (tmp, n); surf.write_to_png(p)
        lst.append("file '%s'\nduration %.5f\n" % (p, 1.0 / DPS))
    lst.append("file '%s'\n" % p)
    open(tmp + "/list.txt", "w").write("".join(lst))
    if NOBUB[0]:
        out = "/tmp/dh_s4_v8_mute.mp4"
        subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", tmp + "/list.txt",
                               "-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-crf", "19", "-preset", "veryfast", "-t", "%.3f" % TOTAL, out])
        print("wrote", out); return
    sc.sound(tmp + "/a.wav")
    out = "%s/dh_s4_anim_%s.mp4" % (OUT, V)
    part = out[:-4] + ".tmp.mp4"
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", tmp + "/list.txt", "-i", tmp + "/a.wav",
                           "-vf", "fps=30,format=yuv420p", "-af", "loudnorm=I=-16:TP=-2:LRA=11,aresample=48000", "-c:v", "libx264", "-crf", "19",
                           "-preset", "veryfast", "-c:a", "aac", "-b:a", "160k", "-t", "%.3f" % TOTAL, part])
    os.rename(part, out)
    print("wrote", out, "%.2f s, %d drawings" % (TOTAL, N))


if __name__ == "__main__":
    if "gate" in sys.argv[1:]:
        sys.exit(1 if gate() else 0)
    if "nobub" in sys.argv[1:]:
        NOBUB[0] = True
        main(1)
    else:
        install_speech()
        A3.HELD.clear(); A3.R_HELD.clear(); del A3.CHECKS[:]
        main(1)
        bad = [c_ for c_ in A3.CHECKS if c_[2]]
        print("speech_gate on the render: %d bubble drawings, %d with faults" % (len(A3.CHECKS), len(bad)))
