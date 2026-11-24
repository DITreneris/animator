"""DADDY'S HOME v8, scene 3 "The Green Star", animated from shot list v2 (daddys-home-s3-shot-list-v2.md) and the frames
Tomas approved on 24 Nov ("animuojam 3 scena, gates, patikra"). Same clock, same takes, same sound as v7 (dh_anim3):
only the pictures change. v7 is untouched; this file reuses its timing, mouths and mix.
  3A (3.1 + 3.2)  over Don's shoulder: his arm goes up to the screen; the robot answers; a small push; his hand drops
                  toward the pad
  3B, 3B'         the inserts: the thumb (the series hand, pressing), then the green star
  3C (3.4)        Pam, MCU, behind the counter, the green in her lenses
  3D (3.5)        Don, CU, the fist goes up and pumps again on "sees"; the robot's head beside him
  3E (4.1-4.2)    one held frame: Mom thumps the arm, Sofía sits, then explodes out; the throne rolls on its casters
  3F (4.3)        Mom MCU scrubbing; Sofía frozen behind her, her eyes go to the tag, then to Mom
  python3 dh_anim3_v8.py [nobub]  ->  ../daddys-home/dh_s3_anim_v8.mp4 and dh_s3_anim_v8_strip.png
  (nobub: no bubbles, no sound, for the cold mute test -> /tmp/dh_s3_v8_mute.mp4)"""
import math
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
import dh_anim1 as A
import dh_anim3 as V7
import dh_back as db
import dh_s3_v8 as S
from kit import Ctx, INK

V = "v8"
DPS, F, CH = V7.DPS, sb.F, dp.CHAIR
OUT = "../daddys-home"
ROWS, T0, TOTAL = V7.ROWS, V7.T0, V7.TOTAL
seq, loud, code, speaking = V7.seq, V7.loud, V7.code, V7.speaking
SKIN = kit.PEOPLE["DON"]["skin"]
# 24 Nov (Tomas: "Don sako GRUN"): "Make it green." from dh_voices/film_v8/3.1.wav: the v1 take's "Make it" and a clean
# "green" cut from the front of "Green ones." (a phrase-final "green" comes out "groan" in this voice: F2 1219 Hz;
# the new one 1979 Hz, Whisper "Make it green." 3/3). The v7 take is left as it is.
import numpy as _np, soundfile as _sf
V7.WAV["3.1"] = _np.asarray(_sf.read("dh_voices/film_v8/3.1.wav")[0], dtype=_np.float64)
NOBUB = [False]


def lerp(a, b, u):
    return tuple(x + (y - x) * u for x, y in zip(a, b))


def ease(u):
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


# ------------------------------------------------------------------ 3A: over Don's shoulder (3.1 + 3.2)
DONB = (404, 720)                                           # round 3: higher (his crown out of the bottom quarter), the tail beside the screen
def cam_3a(tt):
    return lerp(S.CAM_3A, S.CAM_3Az, ease((tt - T0["3.2"]) / 1.0))


ARM = [None]                                                # the hand's (x, y, shape) for this drawing


def r_3a(k, o, t, tt, n):
    rx, ry = o["robot"]["screen"]
    S.SCREEN[0] = (rx + 60, ry - 92, 80)          # round 3: narrower, so both tails pass beside it
    dp.star_screen(k, *S.SCREEN[0], green=False)
    dp._T(k.c, "1 / 5", S.SCREEN[0][0], ry - 92 + 80 * 0.62 * 0.40, 7.0, col=(1, 1, 1))
    o["robot_head"] = (rx, ry)
    i = int(tt * DPS + 1e-6)                                # drawings since the scene began
    j = i - int(T0["3.2"] * DPS)
    if j < 0:                                               # 3.1: up to the screen in four drawings, then held
        ARM[0] = seq(t, [(238, 492, "point_s"), (236, 500, "point_s")])     # caught already pointing at the screen, left of his box
    elif j < 8:
        ARM[0] = (236, 500, "point_s")
    else:                                                   # his hand drops toward the robot's pad before it has finished
        ARM[0] = seq((j - 8) / float(DPS), [(294, 1240, "relax")])   # dropped: straight down, out of the frame (a swing crossed his head or the robot)


def fg_3a(k, cam, tt, n, box):
    dy = -2 if (speaking("3.1", tt) and n % 2) else 0
    hd = db.don_back(k, DONB[0], DONB[1] + dy, 1.0, side=-1)
    db.don_arm(k, DONB[0], DONB[1] + dy, 1.0, ARM[0], side=-1)
    if not NOBUB[0]:
        if speaking("3.1", tt):
            A.bubble(k.c, "Make it green.", DONB)
        if speaking("3.2", tt):
            hx, hy, _ = S.to_screen(cam, *box["robot_head"])
            A.bubble(k.c, "Human approval required.", (hx, hy))


# ------------------------------------------------------------------ 3B: the thumb, the series hand pressing
def r_thumb(k, c, t, tt, n):
    dx = seq(t, [150, 40, -6, 0])
    c.set_source_rgb(0.86, 0.88, 0.90); c.paint()                                           # the robot's chest plate
    kit.rect(k, 110, 300, 320, 380, (0.10, 0.13, 0.18), 3501, lw=4)
    for r_ in (40, 62, 84, 106):
        c.set_source_rgb(0.30, 0.75, 0.95); c.set_line_width(5); c.new_path(); c.arc(270, 470, r_, 0.4, 2.74); c.stroke()
    dp._T(c, "APPROVE", 270, 640, 34, col=(0.80, 0.88, 0.95))
    if dx <= 0:
        c.set_source_rgb(0.30, 0.95, 0.55); c.set_line_width(7)
        for r_ in (126, 150):
            c.new_path(); c.arc(270, 470, r_ + (8 if n % 2 else 0), 0, 2 * math.pi); c.stroke()
    c.save(); c.translate(dx, 0)
    # rules page (24 Nov): a press is a fingertip (point); at the frame's edge, the hand and a short cuff stub
    # (of_scenes.insert_cuff) running out of the nearest edge, the sleeve no wider than the arm
    import of_scenes as osc
    hand, w = (452, 500), 128
    d = osc.insert_cuff(c, hand, (640, 560), w * 0.62, SKIN, (0.98, 0.98, 0.96), cuff=(0.98, 0.98, 0.96), stub=70)
    for ex, ey in ((506, 518), (526, 534), (498, 540)):      # the ketchup on his cuff
        kit.ellipse(k, ex, ey, 9, 7, (0.85, 0.16, 0.10), 3510 + ex, shadow=False, lw=1.4)
    hp.draw(k, "point", hand[0], hand[1], w, SKIN, d, 1)   # the index on the pad
    c.restore()
    return ("Approved.", (468, 452), 1, False, 0) if speaking("3.3", tt) else None


# ------------------------------------------------------------------ 3C: Pam
def r_pam(k, o, t, tt, n):
    hp.reset("quiet", "quiet")
    look = (-1, -0.35) if (speaking("3.4", tt) or t < 0.2) else (-0.2, -0.1)   # the line, then one flat glance off it
    q = ds.pb.pam(k, S.PAM[0], S.PAM[1], dl.PS, "stand", "neutral", look=look, glasses="up", mouth=code("3.4", tt))
    o["head"] = q["head"]


def fg_3c(k, cam, tt, n, box):
    S.c_fg(k, cam)
    if not NOBUB[0] and speaking("3.4", tt):
        hx, hy, _ = S.to_screen(cam, *box["head"])
        A.bubble(k.c, "It's still one.", (hx, hy))


# ------------------------------------------------------------------ 3D: Don, the fist
def r_don(k, o, t, tt, n):
    pose = (-8, 0, 170, -30)                                # up from the first drawing: a rising arm crossed his crown
    if 1.05 <= t < 1.22:                                    # up again on "sees"
        pose = (-8, 0, 182, -44)
    hp.reset("relax", "fist")
    d = V7.don_at(k, S.DON3[0], S.DON3[1], pose, "smug", (1, 0), tt, still=True)
    A.mouth(k, d["head"], V7.DS_, loud("3.5", tt))
    o["head"] = d["head"]


def fg_3d(k, cam, tt, n, box):
    S.ROBOT_NEAR[0] = (10, 780, 110)                        # round 3: lower, clear of the bubble on Don's left
    S.d_fg(k, cam)
    if not NOBUB[0] and speaking("3.5", tt):
        hx, hy, _ = S.to_screen(cam, *box["head"])
        A.bubble(k.c, "Green is all he sees.", (hx, hy))


# ------------------------------------------------------------------ 3E: one held frame (4.1, 4.1', 4.2)
THR = S.THR                                                 # (+30 tried: still no wall between the faces; the box goes on Mom's left)
MOMX = 300                                                  # 24 Nov (Tomas, /grill-me): 3E and 3F back to round 2's staging;
                                                            # the camera moves for a bubble, the people don't (lessons 358)


import mom_bc as _mb
WIPE_FAR = _mb.POSES["wipe"]                                # her own reach (the throne is back where she can reach it)


def mom_e(k, o, tt, n, look=(0.6, 0.8), dy=0):
    hp.reset("quiet", "fist")
    with A.About(k.c, MOMX, F + 8, 1.0, 1.0, dy):
        m = sb.mfs.mom(k, MOMX, F + 8, dl.MS, WIPE_FAR, "sweet", look=look, mouth=code("4.1", tt))
    o["head"] = m["head"]
    return m


def r_thump(k, o, t, tt, n):
    i = min(20, int(t * DPS + 1e-6))
    sd = seq(t, [1.0, 1.0, 0.45, -0.08, 0.04, 0.0])
    dp.ceo_chair(k, THR, CH[1], CH[2], seat_drop=sd, puff=(i == 2))
    if i in (2, 3):                                        # PFFT: two short marks off the seat, no more
        ds._lines(k, [(THR - 34, CH[1] - 128 * CH[2], THR - 34, CH[1] - 146 * CH[2]), (THR + 34, CH[1] - 128 * CH[2], THR + 34, CH[1] - 146 * CH[2])])
    m = mom_e(k, o, tt, n, (0.6, 0.6), 0)               # (her thump bob moved her cheek off the held tail)
    if i >= 4:
        V7.scrub(k, m["hands"][1][0], m["hands"][1][1], n)


def r_sits(k, o, t, tt, n):
    i = min(30, int(t * DPS + 1e-6))
    dp.ceo_chair(k, THR, CH[1], CH[2])
    hp.reset("palm", "palm")
    if i < 2:                                               # arriving, from the right, mid-step
        ds.scs.sofia(k, THR + (70, 34)[i], F + 4, dl.SS, "hold", "smile", look=(-0.6, 0.2))
    else:
        with A.About(k.c, THR, CH[1], 1.0, 1.0, (7, -3, 0)[min(2, i - 2)]):
            V7.sofia_throned(k, THR, CH[1], CH[2], "smile", (-0.6, 0))
    m = mom_e(k, o, tt, n)
    V7.scrub(k, m["hands"][1][0], m["hands"][1][1], n)


def r_up(k, o, t, tt, n):
    """4.2 (round 2): four drawings of held fright in the throne, then she goes up and to the left, the clipboard the
    same way, the throne right on its casters (three short lines behind it, gone when it stops). Mom scrubs on."""
    i = min(20, int(t * DPS + 1e-6))
    j = max(0, i - V7.HOLD); tj = j / float(DPS)
    cx = seq(tj, [THR, THR + 5, THR + 8, THR + 10, THR + 10, THR + 10])   # a jolt, not a roll: the tag stays whole in frame
    dp.TAG_ANG[0] = seq(tj, [0, 0.5, 0.6, 0.3, -0.2, 0.1, 0])
    dp.ceo_chair(k, cx, CH[1], CH[2])
    if i < V7.HOLD:
        V7.sofia_throned(k, THR, CH[1], CH[2], "horrified", (-1, 0) if i else (-0.6, 0))
    else:
        if 1 <= j <= 3:
            tx = cx - 78
            ds._lines(k, [(tx - 22, F - 120, tx - 2, F - 120), (tx - 30, F - 86, tx - 4, F - 86), (tx - 22, F - 52, tx - 2, F - 52)])
        up = seq(tj, [34, 60, 66, 62, 58, 58, 58])
        sx_ = THR + (352 - THR) * min(1.0, (j + 1) / 4.0)
        sy = seq(tj, [1.08, 1.04, 1, 1, 1, 1, 1])
        hp.reset("palm", "palm")
        with A.About(k.c, sx_, F + 4 - up, 2.0 - sy, sy):
            ds.scs.sofia(k, sx_, F + 4 - up, dl.SS, "show", "horrified", look=(0.4, -0.6), lean=-0.2, tablet_kind="none")
        u = min(1.0, (j + 1) / 7.0)
        ds._clip(k, 372 - 72 * u, F - 150 - 150 * math.sin(u * 2.4) + 28 * u, -0.3 - 2.4 * u)
        if j <= 2:
            ds._lines(k, [(sx_ - 14, F - 30, sx_ - 20, F - 18), (sx_ + 14, F - 30, sx_ + 20, F - 18)])
    m = mom_e(k, o, tt, n)
    V7.scrub(k, m["hands"][1][0], m["hands"][1][1], n)


def fg_3e(k, cam, tt, n, box):
    if not NOBUB[0] and speaking("4.1", tt):
        hx, hy, _ = S.to_screen(cam, *box["head"])
        line = "He once fired a man..." if tt < T0["4.1'"] else "...for sitting in that chair."
        A.bubble(k.c, line, (hx, hy))


# ------------------------------------------------------------------ 3F: "Different chair." (round 2's staging)
SOF3F = 400                                                 # 12 right of round 2: whole in the stepped-back frame
def r_mom(k, o, t, tt, n):
    dp.ceo_chair(k, 491, CH[1], CH[2])
    after = tt - (V7.AT["4.3"] + len(V7.WAV["4.3"]) / float(V7.SR))
    hp.reset("palm", "palm")
    if after < 0:                                           # frozen; her eyes go up to the price
        lk = (0.2, -0.2) if t < 0.35 else (0.55, -0.7)
        ds.scs.sofia(k, SOF3F, F - 50, dl.SS, "show", "horrified", look=lk, lean=0.14, tablet_kind="none")
    else:                                                   # after the line: flat, her eyes slide to Mom
        u = min(1.0, after / 0.17)
        ds.scs.sofia(k, SOF3F, F - 50, dl.SS, "show", "deadpan", look=(0.55 + 0.45 * u, -0.7 + 0.9 * u), lean=0.14 - 0.10 * u, tablet_kind="none")
    hp.reset("quiet", "fist")
    m = sb.mfs.mom(k, 446, F + 8, dl.MS, "wipe", "sweet", look=(0.5, 0.9), mouth=code("4.3", tt))
    V7.scrub(k, m["hands"][1][0], m["hands"][1][1], n)
    o["head"] = m["head"]


def fg_3f(k, cam, tt, n, box):
    if not NOBUB[0] and speaking("4.3", tt):
        hx, hy, _ = S.to_screen(cam, *box["head"])
        A.bubble(k.c, "Different chair.", (hx, hy))


# ------------------------------------------------------------------ the frame
SHOTS = {"3.1": ("3A", r_3a, fg_3a, True), "3.2": ("3A", r_3a, fg_3a, True),
         "3.4": ("3C", r_pam, fg_3c, False), "3.5": ("3D", r_don, fg_3d, False),
         "4.1": ("3E", r_thump, fg_3e, False), "4.1'": ("3E", r_sits, fg_3e, False), "4.2": ("3E", r_up, fg_3e, False),
         "4.3": ("3F", r_mom, fg_3f, False)}
SHIFT = {}                                                  # sid -> (dx, dy[, zoom factor]) in set units
CAMS = {"3C": S.CAM_3C, "3D": S.CAM_3D, "3E": S.CAM_3E, "3F": S.CAM_3F}
INS = {"3.3": r_thumb, "3.3'": V7.r_green}


def frame(tt, n, hi=1):
    sid = [s for s, _ in ROWS if T0[s] <= tt + 1e-6][-1]
    t = tt - T0[sid]
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540 * hi, 960 * hi); c = cairo.Context(surf); c.scale(hi, hi)
    k = Ctx(c, 0)
    dp.TAG_ANG[0] = 0.0
    kit.HAND[0] = hp.hand
    try:
        if sid in INS:
            say = INS[sid](k, c, t, tt, n)
            c.identity_matrix(); c.scale(hi, hi)
            if say and not NOBUB[0]:
                A.bubble(c, say[0], say[1], y=150, side=say[2], maxw=220)
            return surf, sid
        name, draw, fg, robot = SHOTS[sid]
        cam = cam_3a(tt) if name == "3A" else CAMS[name]
        if sid in SHIFT:                                    # the camera moved for this line's bubble (lessons 358), as v7's SHIFT3
            dx_, dy_, f_ = (SHIFT[sid] + (1.0,))[:3]
            cam = (cam[0] + dx_, cam[1] + dy_, cam[2] * f_)
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


def _scalp(SY):
    """v8 only: when dh_say's bare-scalp search (offsets to 0.3 r) finds the curl or the shine, look further out on the
    crown (0.35 to 0.55 r): the first outline pixel there, with skin or its shine under it and nothing above."""
    import numpy as np
    orig = SY.measure
    if getattr(orig, "_v8", False):
        return

    def measure(rec):
        fresh = "meas" not in rec
        out = orig(rec)
        if fresh and rec.get("name") == "don" and not out["bald"]:
            N, S_, (mx, my), r = out["N"], out["S"], out["m"], out["r"]
            light = (out["fc"]["a"].sum(-1) > 600)
            for off in (-0.35, -0.45, -0.55, 0.35, 0.45):
                x = int(mx + off * r)
                col = np.nonzero(N[:int(my), x])[0] if 0 <= x < 540 else []
                if not len(col):
                    continue
                y0 = int(col.min())
                if N[max(0, y0 - 30):max(0, y0 - 4), max(0, x - 8):x + 9].any():
                    continue
                below = S_[y0 + 4:y0 + 14, x - 3:x + 4] | light[y0 + 4:y0 + 14, x - 3:x + 4]
                if below.mean() > 0.6:
                    out["top"], out["bald"] = (float(x), y0 + 2), True
                    break
        return out
    measure._v8 = True
    SY.measure = measure


def install_speech():
    import dh_say as SY
    import dh_speech as SP
    SY.install()
    _scalp(SY)
    SP.CARD["Approved."] = "DON"                            # the insert: his hand only, his face off the frame (a card, lessons 551)
    SP._wrap(db, "don_back", "antenna", False)              # Don from behind: the tail comes down onto his bald crown
    SP._fresh(sys.modules[__name__], "frame")
    return SY


PINS = {"Make it green.": (300, 112, 220),               # over the wall above his crown, right of the screen
        "Human approval required.": (20, 112, 240),     # over the wall above the antenna, left of the screen
        "Green is all he sees.": (24, 112, 260)}        # above his crown, clear of the robot's face


def pin(SY):
    """The boxes for the three overhead lines, chosen by the shot (frames approved 24 Nov), not searched: the searched
    places sat on the screen and on the robot's face. Tails and checks are dh_say's own."""
    import dh_speech as SP
    c = cairo.Context(cairo.ImageSurface(cairo.FORMAT_ARGB32, 8, 8))
    for text, (bx, by, mw) in PINS.items():
        lines, bw, bh = SP._lines(c, text, mw)
        SY.PLAN[text] = ("T", bx, by, bw, bh, lines)


def sound(out):
    """v7's mix (dh_anim3.sound), with one change: the fist's whoosh sat 0.05 s before "Green is all he sees." and Whisper
    heard "Brain" in the mix (an effect on a line's first word masks it); it now comes after the line."""
    import numpy as np, soundfile as sf_
    import cs_sfx as fx
    SR = V7.SR
    mix = np.zeros(int((TOTAL + 0.3) * SR))

    def put(a, at_, g=1.0):
        i0 = int(at_ * SR); a = a[:max(0, len(mix) - i0)]; mix[i0:i0 + len(a)] += a * g
    for key, at_ in V7.TAKES:
        put(V7.WAV[key], at_)
    put(fx.tap(220.0), T0["3.3"] + 0.17, 0.6)
    put(fx.chime(), T0["3.3'"] + 0.05, 0.6)
    put(fx.whoosh(0.2), V7.AT["3.5"] + len(V7.WAV["3.5"]) / float(SR) + 0.05, 0.3)   # the fist, after the line
    put(fx.step(), T0["4.1"] + 0.17, 0.7)
    put(fx.whoosh(0.3), T0["4.1"] + 0.19, 0.45)
    put(fx.rustle(0.3), T0["4.1'"] + 0.17, 0.4)
    put(fx.whoosh(0.3), T0["4.2"] + 0.06 + 0.33, 0.6)
    put(fx.scratch(0.4), T0["4.2"] + 0.10 + 0.33, 0.3)
    put(fx.step(), T0["4.2"] + 0.84, 0.6)
    put(fx.tap(140.0), T0["4.2"] + 0.80, 0.5)
    sf_.write(out, mix, SR)


def main(hi=1):
    tmp = "/tmp/dh_s3_%s%s" % (V, "_mute" if NOBUB[0] else ""); os.makedirs(tmp, exist_ok=True)
    ds.ARM_PHONE[0] = True
    me = sys.modules[__name__]
    N = int(round(TOTAL * DPS)); lst = []; tiles = []
    for n in range(N):
        surf, sid = me.frame(n / float(DPS), n, hi)
        p = "%s/d_%04d.png" % (tmp, n); surf.write_to_png(p)
        lst.append("file '%s'\nduration %.5f\n" % (p, 1.0 / DPS))
        if n % 3 == 0:
            tiles.append((p, sid, n / float(DPS)))
    lst.append("file '%s'\n" % p)
    open(tmp + "/list.txt", "w").write("".join(lst))
    if NOBUB[0]:
        out = "/tmp/dh_s3_v8_mute.mp4"
        subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", tmp + "/list.txt",
                               "-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-crf", "19", "-preset", "veryfast", "-t", "%.3f" % TOTAL, out])
        print("wrote", out); return
    sound(tmp + "/a.wav")
    out = "%s/dh_s3_anim_%s.mp4" % (OUT, V)
    part = out[:-4] + ".tmp.mp4"
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", tmp + "/list.txt", "-i", tmp + "/a.wav",
                           "-vf", "fps=30,format=yuv420p", "-af", "loudnorm=I=-16:TP=-2:LRA=11,aresample=48000", "-c:v", "libx264", "-crf", "19",
                           "-preset", "veryfast", "-c:a", "aac", "-b:a", "160k", "-t", "%.3f" % TOTAL, part])
    os.rename(part, out)
    cols = 12; tw, th = 180, 320; rows_ = (len(tiles) + cols - 1) // cols
    sheet = cairo.ImageSurface(cairo.FORMAT_RGB24, cols * tw, rows_ * (th + 18)); c = cairo.Context(sheet)
    c.set_source_rgb(1, 1, 1); c.paint()
    for i, (p, sid, tt) in enumerate(tiles):
        im_ = cairo.ImageSurface.create_from_png(p)
        x, y = (i % cols) * tw, (i // cols) * (th + 18)
        c.save(); c.translate(x, y + 18); c.scale(tw / float(im_.get_width()), th / float(im_.get_height())); c.set_source_surface(im_, 0, 0); c.paint(); c.restore()
        c.set_source_rgb(0, 0, 0); c.select_font_face("Inter", 0, 1); c.set_font_size(12); c.move_to(x + 4, y + 13); c.show_text("%s  %.2f" % (sid, tt))
    sheet.write_to_png("%s/dh_s3_anim_%s_strip.png" % (OUT, V))
    print("wrote", out, "%.2f s, %d drawings" % (TOTAL, N))


if __name__ == "__main__":
    if "remux" in sys.argv[1:]:                             # new sound only: the pictures are copied
        tmp = "/tmp/dh_s3_%s" % V; sound(tmp + "/a.wav")
        out = "%s/dh_s3_anim_%s.mp4" % (OUT, V)
        subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", out, "-i", tmp + "/a.wav", "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                               "-af", "loudnorm=I=-16:TP=-2:LRA=11,aresample=48000", "-c:a", "aac", "-b:a", "160k", "-t", "%.3f" % TOTAL, out[:-4] + ".tmp.mp4"])
        os.rename(out[:-4] + ".tmp.mp4", out); print("remuxed", out); sys.exit()
    if "nobub" in sys.argv[1:]:
        NOBUB[0] = True
        main(1)
    else:
        SY = install_speech()
        me = sys.modules[__name__]
        if SY is not None:
            SY.plan_scene(lambda tt, k: me.frame(tt, k, 1), TOTAL)
            print("scene 3 v8: %d lines pinned, no place: %s" % (len(SY.PLAN), SY.NEEDS_FRAME), flush=True)
        main(1)
