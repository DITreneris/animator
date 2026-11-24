"""DADDY'S HOME (episode 12): the animation pass, scene 2 "Good News" (scene sheet v4, 10.45 s), on the sheet's own clock
and in the sheet's own camera frames. 12 drawings a second, out at 30 fps. Between and inside the key drawings: Don's
arms flying open, his mouth on the takes' loudness, the grin dying, the sleeve, Sofía's folder coming up, his jump and
landing, the hand on the throne, the shove and the throne rolling out, Pam's three looks, the throne rolling back and
bumping his hip. Lines in speech bubbles, only while spoken, the tail at the speaker's cheek, level with the mouth.
  KOKORO_DIR=/tmp/kokoro python3 dh_anim2.py [hi]  ->  ../daddys-home/dh_s2_anim_v1.mp4, dh_s2_anim_v1_strip.png"""
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
import dh_layout as dl
import dh_voices as dv
import dh_scenes as ds
import dh_anim1 as A
import cs_sfx as fx
from kit import Ctx, INK

V = "v3"                                                   # v2 (22 Nov, after the scene 2 review): he steps out of the throne on screen; the grin
                                                           # cracks on "Dad"; the folder stops at her chest; the end is a man caught, not startled;
                                                           # the price tag swings. v1: dh_anim2_v1.py
DPS, SR, F, CH = 12, 48000, sb.F, dp.CHAIR
OUT = "../daddys-home"
DONX, DONX2, DS_ = 452, 486, 0.60
SOF, PAM, SS, PS = ds.SOF, ds.PAM, ds.SS, ds.PS
scs, pb = ds.scs, ds.pb

ROWS = [(r[0], r[1]) for r in ds.S2]
SHOT = {r[0]: r[2] for r in ds.S2}
T0 = {}
_t = 0.0
for _sid, _d in ROWS:
    T0[_sid] = _t; _t += _d
TOTAL = _t
TAKES = [("1.2", T0["1.2"] + 0.10), ("1.3", T0["1.3"] + 0.10), ("2.2", T0["2.2"] + 0.10), ("2.3", T0["2.3a"] + 0.10), ("2.4", T0["2.4"] + 0.04)]
AT = dict(TAKES)
WAV = {}
for _k, _ in TAKES:
    _a, _sr = sf.read("%s/%s.wav" % (dv.FILM_OUT, _k)); WAV[_k] = np.asarray(_a, dtype=np.float64)
_M = sorted(im.SIZES, key=lambda q: im.SIZES[q][0] * im.SIZES[q][1])
M_SMALL, M_BIG = _M[len(_M) // 3], _M[-1]


def loud(key, t):
    a = WAV[key]; i0 = int((t - AT[key]) * SR); n = SR // DPS
    if i0 < 0 or i0 >= len(a):
        return 0.0
    r = float(np.sqrt(np.mean(a[i0:i0 + n] ** 2))) / (float(np.sqrt(np.mean(a ** 2))) + 1e-9)
    return 0.0 if r < 0.35 else min(1.0, 0.35 + 0.5 * r)


def code(key, t):                                          # a mouth shape for Sofía and Pam, from the loudness
    op = loud(key, t)
    return None if op <= 0 else (M_SMALL if op < 0.75 else M_BIG)


def speaking(key, t):
    return AT[key] <= t < AT[key] + len(WAV[key]) / float(SR)


def seq(t, vals):                                          # one value per drawing, the last one held
    return vals[min(len(vals) - 1, int(t * DPS + 1e-6))]


def lerp4(a, b, u):
    return tuple(a[i] + (b[i] - a[i]) * u for i in range(4))


WIDE = (-104, -36, 94, 24)                                  # v2: not a mirror image: one arm a little higher
SAG = (-66, -6, 94, 24)                                    # on "Dad": the arm on the door's side sags


def don_at(k, x, feet, pose, face, look, tt, still=False):
    with A.About(k.c, x, feet, 1.0, 1.0 if still else A.breath(tt, 0.2)):
        return sb.don(k, x, feet, DS_, pose, face, look=look)


def grin(k, head, s):
    """v2: a grin that has stopped being a smile: a band of teeth, held."""
    x, y = head[0], head[1] + 27 * s
    kit.ellipse(k, x, y, 19 * s, 12 * s, A.SKIN, 4120, shadow=False, lw=0)
    kit.cut(k, [(x - 15 * s, y - 5 * s), (x + 15 * s, y - 5 * s), (x + 12 * s, y + 6 * s), (x - 12 * s, y + 6 * s)], (1, 1, 1), shadow=False, lw=2)
    c = k.c
    c.set_source_rgb(*INK); c.set_line_width(1.2)
    for i in (-2, -1, 0, 1, 2):
        c.move_to(x + i * 5.5 * s, y - 5 * s); c.line_to(x + i * 5.2 * s, y + 6 * s); c.stroke()


def cheek(d, s=DS_, side=-1):
    return (d["head"][0] + side * 27, d["head"][1] + 27 * s)


# ------------------------------------------------------------------ the shots
def r_news(k, o, t, tt, n):                                # 1.2: the arms fly open on "Brace"
    dp.ceo_chair(k, CH[0], CH[1], CH[2], seat_drop=1.0)
    pose = seq(t, [(-30, -10, 30, 10), (-70, -20, 70, 20), (-116, -40, 116, 40), (-96, -26, 96, 26), WIDE])
    dad = tt - AT["1.2"] - 0.95                              # v2: the mask cracks on "Dad": eyes to the door, one arm sags; the grin holds
    if dad >= 0:
        pose = lerp4(WIDE, SAG, A.ease(dad / 0.25))
    d = don_at(k, DONX, F + 26, pose, "happy" if dad < 0.1 or dad > 0.55 else "neutral", (0.6, 0) if dad < 0 else (-1, 0), tt)
    if 0.1 <= dad <= 0.55:
        grin(k, d["head"], DS_)
    A.mouth(k, d["head"], DS_, loud("1.2", tt))
    ds._sweat(k, d, 1 if t < 0.9 else 2)
    if speaking("1.2", tt):
        o["say"] = ("Brace yourselves." if tt - AT["1.2"] < 0.95 else "Dad is coming.", cheek(d, side=1), 1, False, 74)


def r_stare(k, o, t, tt, n):                               # 1.1: nobody moves; one of them blinks
    scs.sofia(k, SOF[0], SOF[1], SS, "hold", "interested", look=(-1, 0))
    pb.pam(k, PAM[0], PAM[1], PS, "stand", "neutral", look=(-1, 0), glasses="up")


def r_alone(k, o, t, tt, n):                               # 1.3
    q = scs.sofia(k, SOF[0], SOF[1], SS, "hold", "interested", look=(-0.8, -0.35), mouth=code("1.3", tt))
    if speaking("1.3", tt):
        o["say"] = ("Is he coming alone?", (q["head"][0] - 46 * SS, q["head"][1] + 30 * SS), -1, False)


def r_dead(k, o, t, tt, n):                                # 1.3b: the grin gone in one drawing, the arms still out
    dp.ceo_chair(k, CH[0], CH[1], CH[2], seat_drop=1.0)
    d = don_at(k, DONX, F + 26, WIDE, "neutral", (0.6, 0), tt, still=True)
    ds._sweat(k, d, 3)


def r_wipe(k, o, t, tt, n):                                # 1.3b': the arms drop, the sleeve goes over his head
    dp.ceo_chair(k, CH[0], CH[1], CH[2], seat_drop=1.0)
    pose = seq(t, [(-50, -14, 96, 50), (-8, 0, 140, 84), (-8, 0, 156, 100), (-8, 0, 148, 92)])
    d = don_at(k, DONX, F + 26, pose, "neutral", (0.4, 0.5), tt, still=True)
    A.fear(k, d["head"], DS_, "hope")
    ds._sweat(k, d, 1)


def r_reports(k, o, t, tt, n):                             # 2.1: the folder comes up to her chest
    q = scs.sofia(k, SOF[0], SOF[1], SS, "chest", "deadpan", look=(-1, 0))
    c = k.c
    hx, hy = min(q["hands"], key=lambda h_: h_[1])
    dy = seq(t, [46, 16, -5, 0])
    c.save(); c.translate(hx, hy + 16 + dy); c.rotate(-0.06 - 0.004 * dy)     # v2: it stops at her chest; her face stays clear
    kit.rect(k, -36, -32, 72, 50, (0.86, 0.72, 0.36), 3301, lw=2)
    kit.text(k, "EXPENSES", 0, -3, 11.5, INK)
    c.restore()


def r_jump(k, o, t, tt, n):                                # 2.2: off the floor before she has said a word; he lands on "anything"
    dp.ceo_chair(k, CH[0], CH[1], CH[2], seat_drop=1.0)
    up = seq(t, [-4, 26, 30, 28, 24, 18, 14, 14, 14, 14, 14, 8, -3, 0])
    sy = seq(t, [0.95, 1.05, 1.02, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0.95, 1.0])
    c = k.c
    c.set_source_rgba(0, 0, 0, 0.18); c.save(); c.translate(DONX, F + 30); c.scale(1, 0.22); c.arc(0, 0, 34 - up * 0.3, 0, 6.2832); c.fill(); c.restore()
    with A.About(c, DONX, F + 26 - up, 2.0 - sy, sy):
        d = sb.don(k, DONX, F + 26 - up, DS_, kit.ARM_POSES["shock"], "shock", look=(1, 0.3))
        A.fear(k, d["head"], DS_, "hope", loud("2.2", tt))
    if up > 6:
        ds._lines(k, [(424, F + 22, 414, F + 30), (452, F + 24, 452, F + 34), (480, F + 22, 490, F + 30)])
    if speaking("2.2", tt):
        o["say"] = ("I didn't steal anything!", cheek(d, side=1), 1, False, 74)


def r_hand(k, o, t, tt, n):                                # 2.3a: chin up; the hand lands on the throne's arm
    dp.ceo_chair(k, 400, CH[1], CH[2], seat_drop=1.0)
    x = seq(t, [424, 452, 476, DONX2])                      # v2: he steps out from in front of it, on screen
    pose = seq(t, [(-8, 0, 8, 0), (-14, 0, 12, 0), (-30, -6, 8, 0), (-64, -12, 8, 0), (-82, -18, 8, 0), (-78, -16, 8, 0)])
    if x < DONX2:
        ds._lines(k, [(x - 34, F + 14, x - 50, F + 14), (x - 34, F + 24, x - 54, F + 24)])
    d = don_at(k, x, F + 26, pose, "smug", (1, -0.3), tt)
    A.mouth(k, d["head"], DS_, loud("2.3", tt))
    if speaking("2.3", tt):
        o["say"] = ("The money...", cheek(d, side=1), 1, False)


ROLL = [400, 386, 330, 268, 214, 170, 140, 120]             # the throne's x, a drawing at a time: a wind-up, then gone


def r_push(k, o, t, tt, n):                                # 2.3b: the shove; it rolls out of the frame on a squeaking wheel
    x = seq(t, ROLL)
    i = min(len(ROLL) - 1, int(t * DPS + 1e-6))
    dp.TAG_ANG[0] = seq(t, [0, -0.25, -0.6, -0.7, -0.5, -0.3, -0.1, 0])     # the tag trails behind
    dp.ceo_chair(k, x, CH[1], CH[2], lean=-0.10 if 1 <= i <= 4 else -0.03, seat_drop=1.0)
    if 2 <= i <= 5:
        ds._lines(k, [(x + 74, F - 170, x + 108, F - 170), (x + 80, F - 130, x + 114, F - 130), (x + 74, F - 90, x + 108, F - 90), (x + 78, F - 20, x + 102, F - 20)])
    pose = seq(t, [(-70, -20, 8, 0), (-92, 0, 8, 0), (-96, 0, 8, 0), (-92, 0, 8, 0), (-80, -4, 8, 0), (-50, -4, 8, 0), (-20, 0, 8, 0), (-8, 0, 8, 0)])
    d = don_at(k, DONX2, F + 26, pose, "smug", (1, 0), tt)
    A.mouth(k, d["head"], DS_, loud("2.3", tt))
    if speaking("2.3", tt):
        o["say"] = ("...was invested.", cheek(d, side=1), 1, False)


def r_what(k, o, t, tt, n):                                # 2.4: three looks: at Don, at where the throne went, back at Don
    look = (-0.7, 0.1) if t < 0.30 else ((-1, 0.75) if t < 0.62 else (-0.7, 0.1))
    q = pb.pam(k, PAM[0], PAM[1], PS, "stand", "neutral", look=look, glasses="up", mouth=code("2.4", tt))
    if speaking("2.4", tt):
        o["say"] = ("Into what?", (q["head"][0] - 44 * PS, q["head"][1] + 30 * PS), -1, False)


def r_peek(k, o, t, tt, n):                                # 2.5: he smiles at Pam; behind him the crown rolls back into the frame
    x = seq(t, [150, 176, 214, 252, 286, 308, 318])
    dp.TAG_ANG[0] = seq(t, [0.5, 0.6, 0.6, 0.5, 0.4, 0.3, 0.2])
    dp.ceo_chair(k, x, CH[1], CH[2], lean=0.06, seat_drop=1.0)
    ds._lines(k, [(x - 78, F - 150, x - 56, F - 150), (x - 82, F - 110, x - 60, F - 110)])
    don_at(k, DONX2, F + 26, "vest", "happy", (1, 0), tt)


def r_caught(k, o, t, tt, n):
    """2.5' (v2): all of it, beside him; it bumps his hip. He is caught, not startled: the grin stays on as teeth, his
    eyes slide to it, a drop of sweat, and he steps in front of it with his arms half out, as if it could be hidden."""
    i = min(9, int(t * DPS + 1e-6))
    x = seq(t, [352, 396, 410, 404])
    dp.TAG_ANG[0] = seq(t, [0.3, 0.1, -0.35, 0.25, -0.12, 0.06, 0])
    dp.ceo_chair(k, x, CH[1], CH[2], lean=0.05 if i < 2 else 0.0, seat_drop=1.0)
    if i < 3:
        ds._lines(k, [(x - 104, F - 150, x - 82, F - 150), (x - 108, F - 110, x - 86, F - 110), (x - 104, F - 30, x - 82, F - 30)])
    hit = i >= 2
    dx = seq(t, [0, 0, 7, 3, 0, -22, -44, -58])             # the bump, then one step in front of it
    pose = "vest" if i < 5 else seq(t - 5.0 / DPS, [(-40, -10, 40, 10), (-66, -18, 66, 18), (-74, -22, 70, 20)])
    d = don_at(k, DONX2 + dx, F + 26, pose, "neutral" if hit else "happy", (-1, 0.15) if hit else (1, 0), tt, still=hit)
    if hit:
        grin(k, d["head"], DS_)
        A.sweat(k, d["head"], DS_, min(1.0, (t - 2.0 / DPS) / 0.5), side=1)
    if i == 2:
        ds._lines(k, [(DONX2 - 34, F - 96, DONX2 - 44, F - 106), (DONX2 - 36, F - 82, DONX2 - 50, F - 82), (DONX2 - 34, F - 68, DONX2 - 44, F - 58)])


DRAW = {"1.2": r_news, "1.1": r_stare, "1.3": r_alone, "1.3b": r_dead, "1.3b'": r_wipe, "2.1": r_reports, "2.2": r_jump, "2.3a": r_hand,
        "2.3b": r_push, "2.4": r_what, "2.5": r_peek, "2.5'": r_caught}


SPEECH_SHIFT = [False]                                      # opt-in (dh_say.install turns it on)
SHIFT2 = {}


def frame(tt, n, hi=1):
    sid = [s for s, _ in ROWS if T0[s] <= tt + 1e-6][-1]
    t = tt - T0[sid]
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540 * hi, 960 * hi); c = cairo.Context(surf); c.scale(hi, hi)
    k = Ctx(c, 0); box = {}
    sh = dict(SHOT[sid])

    def fn(k_, o_):
        DRAW[sid](k_, box, t, tt, n)
    sh["draw"] = fn
    dp.TAG_ANG[0] = 0.0
    if SPEECH_SHIFT[0] and sid in SHIFT2:                     # v-next: the camera moved for a side bubble's wall (lessons 358)
        if sh.get("cam") is None:
            sc_ = Ctx(cairo.Context(cairo.ImageSurface(cairo.FORMAT_ARGB32, 54, 96)), 0)
            sh["cam"] = dl.draw(dict(sh, draw=lambda k_, o_: None), sc_)
        cx_, cy_, cz_ = sh["cam"]; sh["cam"] = (cx_ + SHIFT2[sid][0], cy_ + SHIFT2[sid][1], cz_)
    cam = dl.draw(sh, k)
    c.identity_matrix(); c.scale(hi, hi)
    if "say" in box:
        txt, w, side, dark = box["say"][:4]
        shift = box["say"][4] if len(box["say"]) > 4 else 0      # the box off the crown, the tail still to his cheek
        tip = (270 + (w[0] - cam[0]) * cam[2], 480 + (w[1] - cam[1]) * cam[2])
        y = max(110, min(150, tip[1] - 190))
        A.bubble(c, txt, tip, y=y, side=side, maxw=190, dark=dark, shift=shift)
    return surf, sid


def sound(out):
    mix = np.zeros(int((TOTAL + 0.3) * SR))

    def put(a, at_, g=1.0):
        i0 = int(at_ * SR); a = a[:max(0, len(mix) - i0)]; mix[i0:i0 + len(a)] += a * g
    for key, at_ in TAKES:
        put(WAV[key], at_)
    put(fx.whoosh(0.25), T0["1.2"] + 0.08, 0.35)            # the arms
    put(fx.rustle(0.30), T0["1.3b'"] + 0.05, 0.45)          # the sleeve
    put(fx.rustle(0.35), T0["2.1"], 0.5)                    # the folder
    put(fx.whoosh(0.25), T0["2.2"], 0.4)                    # up
    put(fx.step(), T0["2.2"] + 1.0, 0.6)                    # and down
    put(fx.tap(160.0), T0["2.3a"] + 0.17, 0.5)              # the hand on the arm
    put(fx.whoosh(0.3), T0["2.3b"] + 0.08, 0.5)             # the shove
    put(fx.scratch(0.5), T0["2.3b"] + 0.2, 0.30)            # the wheel
    put(fx.scratch(0.55), T0["2.5"], 0.30)                  # the wheel, coming back
    put(fx.step(), T0["2.5'"] + 0.17, 0.7)                  # the bump
    sf.write(out, mix, SR)


def main(hi=1):
    tmp = "/tmp/dh_s2_%s" % V; os.makedirs(tmp, exist_ok=True)
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
    out = "%s/dh_s2_anim_%s%s.mp4" % (OUT, V, "" if hi == 1 else "_1080")
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
    sheet.write_to_png("%s/dh_s2_anim_%s_strip.png" % (OUT, V))
    print("wrote", out, "%.2f s, %d drawings" % (TOTAL, N))


if __name__ == "__main__":
    main(2 if (len(sys.argv) > 1 and sys.argv[1] == "hi") else 1)
