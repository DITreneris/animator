"""DADDY'S HOME (episode 12): the animation pass, scene 3 "The Green Star" (scene sheet v3, 11.45 s), on the sheet's clock
and in the sheet's camera frames. 12 drawings a second, out at 30 fps. Between and inside the key drawings: Don's arm
going up to the screen, the robot's bob, the thumb coming in and pressing, the green star popping, Pam's mouth, the fist
pump, Mom's thump and the seat coming back up, her scrubbing, Sofía sitting down and exploding out of the throne, the
clipboard's flight, the throne rolling away. Lines in speech bubbles, only while spoken.
  KOKORO_DIR=/tmp/kokoro python3 dh_anim3.py [hi]  ->  ../daddys-home/dh_s3_anim_v1.mp4, dh_s3_anim_v1_strip.png"""
import math
import os
import subprocess
import sys
import cairo
import numpy as np
import soundfile as sf
import kit
import fs_storyboard as sb
import iwry_mouths as im
import dh_props as dp
import dh_poses as dq
import dh_layout as dl
import dh_animatic as da
import dh_voices as dv
import dh_scenes as ds
import dh_anim1 as A
import cs_sfx as fx
from kit import Ctx, INK

V = "v2"                                                   # v2 (22 Nov, after the scene 3 review): Sofía plainly IN the throne (elbows on its arms,
                                                           # knees forward); a held fright before she goes up, and a frightened face, not an angry
                                                           # one; after "Different chair." her eyes slide to Mom; "1 / 5" on the screen, red and
                                                           # green; the two singles 12 % closer. v1: dh_anim3_v1.py
DPS, SR, F, CH = 12, 48000, sb.F, dp.CHAIR
OUT = "../daddys-home"
DS_ = 0.60
PAM, SS, PS, MS, THR, DON3 = ds.PAM, ds.SS, ds.PS, ds.MS, ds.THR, ds.DON3
scs, pb = ds.scs, ds.pb

ROWS = [(r[0], r[1]) for r in ds.S3]
SHOT = {r[0]: r[2] for r in ds.S3}
T0 = {}
_t = 0.0
for _sid, _d in ROWS:
    T0[_sid] = _t; _t += _d
TOTAL = _t
TAKES = [("3.1", T0["3.1"] + 0.10), ("3.2", T0["3.2"] + 0.04), ("3.3", T0["3.3"] + 0.06), ("3.4", T0["3.4"] + 0.10), ("3.5", T0["3.5"] + 0.10),
         ("4.1", T0["4.1"] + 0.10), ("4.3", T0["4.3"] + 0.15)]
AT = dict(TAKES)
WAV = {}
for _k, _ in TAKES:
    _a, _sr = sf.read("%s/%s.wav" % (dv.FILM_OUT, _k)); WAV[_k] = np.asarray(_a, dtype=np.float64).copy()
# the robot is talked over on purpose: "Human approval required." is cut off by Don's "Approved."
_n = int((AT["3.3"] - 0.02 - AT["3.2"]) * SR)
if _n < len(WAV["3.2"]):
    WAV["3.2"] = WAV["3.2"][:_n]; WAV["3.2"][-int(0.04 * SR):] *= np.linspace(1, 0, int(0.04 * SR))
_M = sorted(im.SIZES, key=lambda q: im.SIZES[q][0] * im.SIZES[q][1])
M_SMALL, M_BIG = _M[len(_M) // 3], _M[-1]


def loud(key, t):
    a = WAV[key]; i0 = int((t - AT[key]) * SR); n = SR // DPS
    if i0 < 0 or i0 >= len(a):
        return 0.0
    r = float(np.sqrt(np.mean(a[i0:i0 + n] ** 2))) / (float(np.sqrt(np.mean(a ** 2))) + 1e-9)
    return 0.0 if r < 0.35 else min(1.0, 0.35 + 0.5 * r)


def code(key, t):
    op = loud(key, t)
    return None if op <= 0 else (M_SMALL if op < 0.75 else M_BIG)


def speaking(key, t):
    return AT[key] <= t < AT[key] + len(WAV[key]) / float(SR)


def seq(t, vals):
    return vals[min(len(vals) - 1, int(t * DPS + 1e-6))]


def don_at(k, x, feet, pose, face, look, tt, still=False):
    with A.About(k.c, x, feet, 1.0, 1.0 if still else A.breath(tt, 0.2)):
        return sb.don(k, x, feet, DS_, pose, face, look=look)


def cheek(d, side=-1):
    return (d["head"][0] + side * 27, d["head"][1] + 27 * DS_)


import sofia_ob as _sob
_sob.POSES.setdefault("throned", (-64, 14, 64, -14))        # her elbows out on the gold armrests (the table her rig reads)


def sofia_throned(k, x, floor, cs, face, look, clip=True):
    """v2: Sofía IN the throne. Her arms lie along its gold arms, her lap comes forward over the seat, her knees are in
    front of her and her shins come down to shoes bigger than they would be standing; the clipboard is on her lap."""
    c = k.c
    seat_y = floor - 110 * cs + 3
    feet = seat_y + 122 * SS
    c.save(); c.rectangle(x - 150, seat_y - 400, 300, 400 + 2); c.clip()
    q = scs.sofia(k, x, feet, SS, "throned", face, look=look, tablet_kind="none")
    c.restore()
    kit.cut(k, [(x - 32, seat_y - 6), (x + 32, seat_y - 6), (x + 42, seat_y + 30), (x - 42, seat_y + 30)], scs.WINE, shadow=False, lw=2.2)   # her lap
    c.set_source_rgb(*INK); c.set_line_width(1.6)
    for sx in (-1, 1):                                      # the knees, then the shins and the shoes
        c.new_path(); c.arc(x + sx * 21, seat_y + 24, 9, math.pi * 0.15, math.pi * 0.85); c.stroke()
        kit.cut(k, [(x + sx * 21 - 9, seat_y + 30), (x + sx * 21 + 9, seat_y + 30), (x + sx * 19 + 7, floor - 2), (x + sx * 19 - 7, floor - 2)],
                (0.16, 0.15, 0.18), shadow=False, lw=1.8)
        kit.cut(k, [(x + sx * 19 - 12, floor - 5), (x + sx * 19 + 14, floor - 5), (x + sx * 19 + 17, floor + 6), (x + sx * 19 - 12, floor + 6)],
                (0.08, 0.07, 0.08), shadow=False, lw=1.6)
    if clip:
        ds._clip(k, x + 4, seat_y - 4, -0.12)
    return q


def scrub(k, x, y, n):                                     # Mom's cloth going: two marks, swapping sides every drawing
    sg = 1 if n % 2 else -1
    ds._lines(k, [(x + sg * 10, y - 8, x + sg * 22, y - 12), (x + sg * 12, y + 4, x + sg * 26, y + 4)])


# ------------------------------------------------------------------ the shots
def r_point(k, o, t, tt, n):                               # 3.1: his arm goes up to the red star
    rx, ry = o["robot"]["screen"]
    dp.star_screen(k, rx + 6, ry - 92, 124, green=False)
    dp._T(k.c, "1 / 5", rx + 6, ry - 92 + 124 * 0.62 * 0.40, 9.5, col=(1, 1, 1))
    pose = seq(t, [(-40, -4, 8, 0), (-100, -10, 8, 0), (-156, -18, 8, 0), (-148, -14, 8, 0)])
    d = don_at(k, DON3[0], DON3[1], pose, "smug", (-1, -0.6), tt)
    A.mouth(k, d["head"], DS_, loud("3.1", tt))
    if speaking("3.1", tt):
        o["say"] = ("Make it green.", cheek(d, 1), 1, False, 40)


def r_robot(k, o, t, tt, n):                               # 3.2: the same polite face; it bobs as it talks
    dy = -3 if (speaking("3.2", tt) and n % 2) else 0
    c = k.c
    c.save(); c.translate(0, dy); da._rb("idle")(k, o); c.restore()
    if speaking("3.2", tt):
        o["say"] = ("Human approval required.", (da.RH[0] + 24, da.RH[1] + 4), 1, False, 20)


def r_thumb(k, c, t, tt, n):                               # 3.3: the thumb is on the pad before the robot's last word
    dx = seq(t, [150, 40, -6, 0])
    c.save(); c.translate(dx, 0); ds.s3_thumb(k, c); c.restore()
    if dx > 0:                                              # the pad stays put while the thumb travels
        c.set_source_rgb(0.86, 0.88, 0.90); c.rectangle(0, 0, dx, 960); c.fill()
    if dx <= 0:
        c.set_source_rgb(0.30, 0.95, 0.55); c.set_line_width(7)
        for r_ in (126, 150):
            c.new_path(); c.arc(270, 470, r_ + (8 if n % 2 else 0), 0, 2 * math.pi); c.stroke()
    return ("Approved.", (468, 452), 1, False, 0) if speaking("3.3", tt) else None


def r_green(k, c, t, tt, n):                               # 3.3': the green star pops, far too pleased with itself
    z = seq(t, [0.62, 1.10, 0.97, 1.0])
    c.set_source_rgb(0.05, 0.07, 0.10); c.paint()
    c.save(); c.translate(270, 400); c.scale(z, z); c.rotate(0.03 * math.sin(tt * 9) if z == 1.0 else 0.0); c.translate(-270, -400)
    ds.s3_green(k, c)
    c.restore()
    dp._T(c, "1 / 5", 270, 716, 58, col=(1, 1, 1))          # it doesn't pop: the number is the one thing that hasn't changed
    return None


def r_pam(k, o, t, tt, n):                                 # 3.4
    q = pb.pam(k, PAM[0], PAM[1], PS, "stand", "neutral", look=(-1, -0.35), glasses="up", mouth=code("3.4", tt))
    if speaking("3.4", tt):
        o["say"] = ("It's still one.", (q["head"][0] - 44 * PS, q["head"][1] + 30 * PS), -1, False, 0)


def r_proud(k, o, t, tt, n):                               # 3.5: one fist goes up, and up again on "sees"
    pose = seq(t, [(-8, 0, 110, 70), (-8, 0, 178, -4), (-8, 0, 168, 10), (-8, 0, 172, 6)])
    if 1.05 <= t < 1.22:
        pose = (-8, 0, 180, -8)
    d = don_at(k, DON3[0], DON3[1], pose, "smug", (1, 0), tt)
    A.mouth(k, d["head"], DS_, loud("3.5", tt))
    if speaking("3.5", tt):
        o["say"] = ("Green is all he sees.", cheek(d, -1), -1, False, -30)


def r_thump(k, o, t, tt, n):                               # 4.1: her fist comes down on the gold arm; PFFT, the seat is back up
    i = min(20, int(t * DPS + 1e-6))
    sd = seq(t, [1.0, 1.0, 0.45, -0.08, 0.04, 0.0])
    dp.ceo_chair(k, THR, CH[1], CH[2], seat_drop=sd, puff=(i == 2))
    if i in (2, 3):
        ds._lines(k, [(THR - 34, CH[1] - 128 * CH[2], THR - 34, CH[1] - 146 * CH[2]), (THR + 34, CH[1] - 128 * CH[2], THR + 34, CH[1] - 146 * CH[2]),
                      (THR - 70, CH[1] - 196 * CH[2], THR - 84, CH[1] - 208 * CH[2]), (THR - 58, CH[1] - 202 * CH[2], THR - 62, CH[1] - 218 * CH[2])])
    with A.About(k.c, 318, F + 8, 1.0, 1.0, -10 if i == 1 else 0):
        m = sb.mfs.mom(k, 318, F + 8, MS, "wipe", "sweet", look=(0.6, 0.6), mouth=code("4.1", tt))
    if i >= 4:
        scrub(k, m["hands"][1][0], m["hands"][1][1], n)
    if speaking("4.1", tt):
        o["say"] = ("He once fired a man...", (m["head"][0] - 40 * MS, m["head"][1] + 30 * MS), -1, False, -40, 132)


def r_sits(k, o, t, tt, n):                                # 4.1': Sofía walks in and sits down in it; Mom scrubs on
    i = min(30, int(t * DPS + 1e-6))
    dp.ceo_chair(k, THR, CH[1], CH[2])
    if i < 2:                                               # arriving, from the right
        scs.sofia(k, THR + (70, 34)[i], F + 4, SS, "hold", "smile", look=(-0.6, 0.2))
    else:
        with A.About(k.c, THR, CH[1], 1.0, 1.0, (7, -3, 0)[min(2, i - 2)]):
            sofia_throned(k, THR, CH[1], CH[2], "smile", (-0.6, 0))
    m = sb.mfs.mom(k, 318, F + 8, MS, "wipe", "sweet", look=(0.6, 0.8), mouth=code("4.1", tt))
    scrub(k, m["hands"][1][0], m["hands"][1][1], n)
    if speaking("4.1", tt):
        o["say"] = ("...for sitting in that chair.", (m["head"][0] - 40 * MS, m["head"][1] + 30 * MS), -1, False, -40, 132)


HOLD = 4                                                    # v2: drawings of held fright before she moves (0.33 s)


def r_up(k, o, t, tt, n):
    """4.2 (v2): Mom's "...that chair." is still ending. Sofía hears it: four drawings in the throne, eyes wide, not
    breathing. Then she goes: straight up, the clipboard one way, the throne the other. Terror, never anger."""
    i = min(20, int(t * DPS + 1e-6))
    j = max(0, i - HOLD)                                    # drawings since she moved
    tj = j / float(DPS)
    cx = seq(tj, [THR, THR + 26, THR + 52, THR + 62, THR + 66, THR + 68])
    dp.TAG_ANG[0] = seq(tj, [0, 0.5, 0.6, 0.3, -0.2, 0.1, 0])
    dp.ceo_chair(k, cx, CH[1], CH[2], lean=seq(tj, [0.0, 0.12, 0.10, 0.06, 0.02, 0.0]))
    if i < HOLD:
        sofia_throned(k, THR, CH[1], CH[2], "horrified", (-1, 0) if i else (-0.6, 0))
        if i == 1:
            ds._lines(k, [(THR - 22, CH[1] - 318 * CH[2], THR - 30, CH[1] - 334 * CH[2]), (THR + 22, CH[1] - 318 * CH[2], THR + 30, CH[1] - 334 * CH[2])])
        return
    if 1 <= j <= 3:
        ds._lines(k, [(cx - 60, F - 150, cx - 36, F - 150), (cx - 64, F - 100, cx - 40, F - 100), (cx - 60, F - 40, cx - 36, F - 40)])
    up = seq(tj, [34, 60, 66, 60, 46, 26, 6])
    sy = seq(tj, [1.08, 1.04, 1, 1, 1, 1, 0.95])
    with A.About(k.c, 392, F + 4 - up, 2.0 - sy, sy):
        scs.sofia(k, 392, F + 4 - up, SS, "show", "horrified", look=(0.4, -0.6), lean=-0.2, tablet_kind="none")
    u = min(1.0, (j + 1) / 7.0)                             # the clipboard: up and away to the left, turning
    ds._clip(k, 372 - 76 * u, F - 150 - 150 * math.sin(u * 2.4) + 40 * u, -0.3 - 2.4 * u)
    if up > 20:
        ds._lines(k, [(366, F - 8, 356, F + 4), (392, F - 6, 392, F + 8), (418, F - 8, 428, F + 4)])


def r_mom(k, o, t, tt, n):                                 # 4.3: Mom scrubs on; behind her Sofía is frozen where she landed
    dp.ceo_chair(k, 448, CH[1], CH[2])
    after = tt - (AT["4.3"] + len(WAV["4.3"]) / float(SR))    # v2: the line lands; then her face goes flat and her eyes slide to Mom
    if after < 0:
        scs.sofia(k, 524, F + 4, SS, "show", "horrified", look=(0.2, -0.2), lean=0.14, tablet_kind="none")
    else:
        scs.sofia(k, 524, F + 4, SS, "show", "deadpan", look=(-min(1.0, 0.3 + after / 0.17 * 0.35), 0), lean=0.14 - 0.10 * min(1.0, after / 0.17), tablet_kind="none")
    ds._clip(k, 300, F - 6, 1.35)
    m = sb.mfs.mom(k, 372, F + 8, MS, "wipe", "sweet", look=(0.5, 0.9), mouth=code("4.3", tt))
    scrub(k, m["hands"][1][0], m["hands"][1][1], n)
    if speaking("4.3", tt):
        o["say"] = ("Different chair.", (m["head"][0] - 40 * MS, m["head"][1] + 30 * MS), -1, False, -40, 132)


CLOSER = {"3.4": (1.12, dl.hp(PAM[0], PAM[1], PS)), "3.5": (1.12, dl.hd(DON3[0], DON3[1], DS_))}    # v2: (how much, the head it closes on)
CAM0 = {}
DRAW = {"3.1": r_point, "3.2": r_robot, "3.4": r_pam, "3.5": r_proud, "4.1": r_thump, "4.1'": r_sits, "4.2": r_up, "4.3": r_mom}
INS = {"3.3": r_thumb, "3.3'": r_green}


def frame(tt, n, hi=1):
    sid = [s for s, _ in ROWS if T0[s] <= tt + 1e-6][-1]
    t = tt - T0[sid]
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540 * hi, 960 * hi); c = cairo.Context(surf); c.scale(hi, hi)
    k = Ctx(c, 0); box = {}
    dp.TAG_ANG[0] = 0.0
    if sid in INS:
        say = INS[sid](k, c, t, tt, n)
        c.identity_matrix(); c.scale(hi, hi)
        if say:
            A.bubble(c, say[0], say[1], y=150, side=say[2], maxw=220)
        return surf, sid
    sh = dict(SHOT[sid])

    def fn(k_, o_):
        box.update(o_)
        DRAW[sid](k_, box, t, tt, n)
    sh["draw"] = fn
    if sid in CLOSER:
        if sid not in CAM0:                                 # the sheet's own camera, found once on a scratch surface
            sc = Ctx(cairo.Context(cairo.ImageSurface(cairo.FORMAT_ARGB32, 54, 96)), 0)
            c0 = dl.draw(dict(SHOT[sid], draw=lambda k_, o_: None), sc)
            f_, hd = CLOSER[sid]
            CAM0[sid] = (hd[0] - (hd[0] - c0[0]) / f_, hd[1] - (hd[1] - c0[1]) / f_, c0[2] * f_)
        sh["cam"] = CAM0[sid]; sh["ymin"] = 100
    cam = dl.draw(sh, k)
    c.identity_matrix(); c.scale(hi, hi)
    if "say" in box:
        txt, w, side, dark, shift = box["say"][:5]
        mw = box["say"][5] if len(box["say"]) > 5 else 200      # Mom's are narrow: they stay clear of the price tag
        tip = (270 + (w[0] - cam[0]) * cam[2], 480 + (w[1] - cam[1]) * cam[2])
        y = max(110, min(150, tip[1] - 190))
        A.bubble(c, txt, tip, y=y, side=side, maxw=mw, dark=dark, shift=shift)
    return surf, sid


def sound(out):
    mix = np.zeros(int((TOTAL + 0.3) * SR))

    def put(a, at_, g=1.0):
        i0 = int(at_ * SR); a = a[:max(0, len(mix) - i0)]; mix[i0:i0 + len(a)] += a * g
    for key, at_ in TAKES:
        put(WAV[key], at_)
    put(fx.tap(220.0), T0["3.3"] + 0.17, 0.6)               # the thumb on the pad
    put(fx.chime(), T0["3.3'"] + 0.05, 0.6)                 # far too happy
    put(fx.whoosh(0.2), T0["3.5"] + 0.05, 0.3)              # the fist
    put(fx.step(), T0["4.1"] + 0.17, 0.7)                   # the thump
    put(fx.whoosh(0.3), T0["4.1"] + 0.19, 0.45)             # PFFT
    put(fx.rustle(0.3), T0["4.1'"] + 0.17, 0.4)             # she sits
    put(fx.whoosh(0.3), T0["4.2"] + 0.06 + 0.33, 0.6)              # she goes up
    put(fx.scratch(0.4), T0["4.2"] + 0.10 + 0.33, 0.3)             # the throne rolls
    put(fx.step(), T0["4.2"] + 0.84, 0.6)                   # she lands
    put(fx.tap(140.0), T0["4.2"] + 0.80, 0.5)               # the clipboard
    sf.write(out, mix, SR)


def main(hi=1):
    tmp = "/tmp/dh_s3_%s" % V; os.makedirs(tmp, exist_ok=True)
    ds.ARM_PHONE[0] = True
    N = int(round(TOTAL * DPS)); lst = []; tiles = []
    for n in range(N):
        surf, sid = frame(n / float(DPS), n, hi)
        p = "%s/d_%04d.png" % (tmp, n); surf.write_to_png(p)
        lst.append("file '%s'\nduration %.5f\n" % (p, 1.0 / DPS))
        if n % 3 == 0:
            tiles.append((p, sid, n / float(DPS)))
    lst.append("file '%s'\n" % p)
    open(tmp + "/list.txt", "w").write("".join(lst))
    sound(tmp + "/a.wav")
    out = "%s/dh_s3_anim_%s%s.mp4" % (OUT, V, "" if hi == 1 else "_1080")
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
    main(2 if (len(sys.argv) > 1 and sys.argv[1] == "hi") else 1)
