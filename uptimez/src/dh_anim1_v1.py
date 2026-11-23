"""DADDY'S HOME (episode 12): the animation pass, scene 1 "The Call" (scene sheet v3, 12.0 s), on the sheet's own clock.
12 drawings a second, out at 30 fps. The key drawings are the sheet's; this adds what happens between and inside them:
the phone buzzing, Don's eyes, the seat's drop and its shake, him springing up, the breath in every hold, mouths moving
on the takes' own loudness, the finger's tap on "first", the phone turned face down, the arm coming down from his ear.
Lines are in speech bubbles, on screen only while they are spoken, the tail to the mouth (or to the phone for a voice
heard through it).
  KOKORO_DIR=/tmp/kokoro python3 dh_anim1.py [lo|hi]  ->  ../daddys-home/dh_s1_anim_v1.mp4, dh_s1_anim_v1_strip.png"""
import math
import os
import subprocess
import sys
import cairo
import numpy as np
import soundfile as sf
import kit
import fs_storyboard as sb
import dh_props as dp
import dh_poses as dq
import dh_layout as dl
import dh_voices as dv
import dh_scenes as ds
import cs_sfx as fx
from kit import Ctx, INK

V = "v1"
DPS = 12
SR = 48000
F = sb.F
CH = dp.CHAIR
DON = (452, F + 26, 0.60)
SKIN = kit.PEOPLE["DON"]["skin"]
OUT = "../daddys-home"

# the sheet's rows give the clock
ROWS = [(r[0], r[1]) for r in ds.S1]
T0 = {}
_t = 0.0
for _sid, _d in ROWS:
    T0[_sid] = _t; _t += _d
TOTAL = _t
TAKES = [("0.3", T0["0.3"] + 0.10), ("0.4", T0["0.4"] + 0.10), ("0.5", T0["0.5a"] + 0.10), ("0.6", T0["0.6"] + 0.10), ("0.7", T0["0.7a"] + 0.10)]


def _take(key):
    a, sr = sf.read("%s/%s.wav" % (dv.FILM_OUT, key))
    assert sr == SR
    return np.asarray(a, dtype=np.float64)


WAV = {k: _take(k) for k, _ in TAKES}
AT = dict(TAKES)


def loud(key, t):
    """How open a mouth is at film time t while take `key` plays: 0, or 0.35..1 from the take's own loudness."""
    a = WAV[key]; i0 = int((t - AT[key]) * SR); n = SR // DPS
    if i0 < 0 or i0 >= len(a):
        return 0.0
    r = float(np.sqrt(np.mean(a[i0:i0 + n] ** 2))) / (float(np.sqrt(np.mean(a ** 2))) + 1e-9)
    return 0.0 if r < 0.35 else min(1.0, 0.35 + 0.5 * r)


def speaking(key, t):
    return AT[key] <= t < AT[key] + len(WAV[key]) / float(SR)


def ease(t):
    t = min(1.0, max(0.0, t)); return t * t * (3 - 2 * t)


class About:
    """Scale the drawing about a point (breath, stretch): with About(c, x, y, sx, sy): ..."""
    def __init__(self, c, x, y, sx=1.0, sy=1.0, dy=0.0):
        self.c, self.a = c, (x, y, sx, sy, dy)

    def __enter__(self):
        x, y, sx, sy, dy = self.a
        self.c.save(); self.c.translate(x, y + dy); self.c.scale(sx, sy); self.c.translate(-x, -y)

    def __exit__(self, *a):
        self.c.restore()


def breath(t, phase=0.0):
    return 1.0 + 0.009 * math.sin(2 * math.pi * (t / 1.5 + phase))


def mouth(k, head, s, op):
    """Over the drawn mouth: skin, then an open mouth as tall as the sound is loud."""
    if op <= 0:
        return
    x, y = head[0], head[1] + 28 * s
    kit.ellipse(k, x, y - 1.5 * s, 17 * s, 10 * s, SKIN, 4100, shadow=False, lw=0)
    kit.ellipse(k, x, y, (9 + 3 * op) * s, (3 + 8 * op) * s, (0.35, 0.08, 0.08), 4101, shadow=False, lw=2)


# ------------------------------------------------------------------ the shots, each drawn for a time inside it
def d_phone(t, n):
    return lambda k, c: dp.dad_phone(k, True, buzz=(1.0 if n % 2 else -1.0))


def d_seat(t, n, kind):
    def f(k, o):
        import acts_ob as ac
        c = k.c
        if kind == "a":                                     # his eyes go to the phone over three drawings
            u = ease(t / 0.2)
            with About(c, CH[0], dl.FLOOR, 1.0, breath(t)):
                dq.don_seated(k, CH[0], dl.FLOOR, CH[2], phone="ring" if n % 2 == 0 else None, look=(u, 0.2 * u))
            ac.shredder(k, CH[0] + 190 * CH[2], dl.FLOOR, 0.62, fill=0.4)
        elif kind == "freeze":                              # nothing moves: that is the joke
            dq.don_seated(k, CH[0], dl.FLOOR, CH[2], phone="ring", look=(1, 0.2), freeze=True)
            ac.shredder(k, CH[0] + 190 * CH[2], dl.FLOOR, 0.62, fill=0.4)
        else:                                               # the seat goes: down hard, a bounce, still
            dy = (-16, 7, -3, 0)[min(3, int(t * DPS))]
            with About(c, CH[0], dl.FLOOR, 1.0, 1.0, dy):
                dq.don_seated(k, CH[0], dl.FLOOR, CH[2], phone="ring" if n % 2 == 0 else None, sunk=True, hang=True, puff=t < 0.45)
    return f


def d_up(t, n):
    def f(k, o):
        sy = (1.08, 0.96, 1.01, 1.0)[min(3, int(t * DPS))]
        dp.ceo_chair(k, CH[0], CH[1], CH[2], seat_drop=1.0)
        if n % 2 == 0:
            ds._ring_on_arm(k)
        with About(k.c, DON[0], DON[1], 2.0 - sy, sy):
            sb.don(k, DON[0], DON[1], DON[2], "vest", "smug", look=(0.4, 0))
    return f


def d_call(t, tt, face, key=None, lower=0.0, lit=True, face2=None, at2=9.0, look=(0.3, 0)):
    """Close on Don with the phone. key: the take that moves his mouth. lower: 0 at his ear .. 1 lowered."""
    def f(k, o):
        dp.ceo_chair(k, CH[0], CH[1], CH[2], seat_drop=1.0)
        u = ease(lower)
        pose = (-8, 0, 128 + (40 - 128) * u, 124 + (70 - 124) * u)
        fc = face2 if (face2 and t >= at2) else face
        with About(k.c, DON[0], DON[1], 1.0, breath(tt, 0.3)):
            d = sb.don(k, DON[0], DON[1], DON[2], pose, fc, look=(look[0] + (0.6 - look[0]) * u, look[1] + (0.6 - look[1]) * u))
            ds._phone_in_hand(k, d, lit, at_ear=u < 0.5)
            if key:
                mouth(k, d["head"], DON[2], loud(key, tt))
        o["mouth"] = (d["head"][0] - 27, d["head"][1] + 27 * DON[2])      # the edge of his cheek, level with his mouth, on the side away from the phone
        o["phone"] = (d["head"][0] + 44, d["head"][1] - 2)                # the phone's outer edge
    return f


def d_booth(t, tap=0.0, down=False, jolt=0.0):
    def f(k, c):
        z = 1.0 + 0.035 * ease(t / 1.6)                     # the camera leans in a little, every time we come back
        c.save(); c.translate(270, 430 + jolt); c.scale(z, z); c.translate(-270, -430)
        dp.booth(k, tap=tap, face_down=down)
        c.restore()
    return f


SH = {}


CLOSE = (DON[0] + 6, 636, 2.7)                             # the film's close on Don: his face at the series' size (r about 80), the crown whole


def shot(name, heads, fn, cam=None):
    sh = SH.get(name) or SH.setdefault(name, dl.shot(name, heads, None, "", chair=False, cam=cam, ymin=150))
    sh["draw"] = fn
    return sh


def bubble(c, text, tip, y=128, up=False, side=0):
    """A speech bubble in the 540 frame: the box at y, the tail's tip 10 px short of the mouth (or the phone)."""
    c.select_font_face(kit.FONT); c.set_font_size(31)
    lines = [""]
    for w_ in text.split():
        cand = (lines[-1] + " " + w_).strip()
        if c.text_extents(cand).x_advance > 372 and lines[-1]:
            lines.append(w_)
        else:
            lines[-1] = cand
    bw = max(c.text_extents(l).x_advance for l in lines) + 44; bh = 26 + 37 * len(lines)
    bx = min(max(tip[0] + side * (bw / 2 - 26) - bw / 2, 24), 462 - bw)
    tx = min(max(tip[0], bx + 30), bx + bw - 30)
    c.set_line_join(1)
    for fill in (False, True):
        c.new_path()
        r = 16
        c.arc(bx + r, y + r, r, math.pi, 1.5 * math.pi); c.arc(bx + bw - r, y + r, r, 1.5 * math.pi, 0)
        c.arc(bx + bw - r, y + bh - r, r, 0, 0.5 * math.pi); c.arc(bx + r, y + bh - r, r, 0.5 * math.pi, math.pi); c.close_path()
        if up:
            c.move_to(tx - 14, y + 2); c.line_to(tip[0], tip[1] + 10); c.line_to(tx + 14, y + 2); c.close_path()
        else:
            c.move_to(tx - 14, y + bh - 2); c.line_to(tip[0] + side * 4, tip[1] - 3); c.line_to(tx + 14, y + bh - 2); c.close_path()
        if fill:
            c.set_source_rgb(1, 1, 1); c.fill()
        else:
            c.set_source_rgb(*INK); c.set_line_width(7); c.stroke()
    c.set_source_rgb(*INK)
    for i, l in enumerate(lines):
        c.move_to(bx + (bw - c.text_extents(l).x_advance) / 2, y + 42 + 37 * i); c.show_text(l)


def frame(tt, n, hi=1):
    """One drawing at film time tt (drawing n)."""
    sid = [s for s, _ in ROWS if T0[s] <= tt + 1e-6][-1]
    t = tt - T0[sid]
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540 * hi, 960 * hi); c = cairo.Context(surf); c.scale(hi, hi)
    k = Ctx(c, 0); o = {}; cam = None; say = None
    HS, H = ds.HS, ds.H
    if sid == "0.1":
        d_phone(t, n)(k, c)
    elif sid == "0.2a":
        cam = dl.draw(shot("0.2", [HS], d_seat(t, n, "a")), k)
    elif sid == "0.2a'":
        cam = dl.draw(shot("0.2", [HS], d_seat(t, n, "freeze")), k)
    elif sid == "0.2b":
        cam = dl.draw(shot("0.2", [HS], d_seat(t, n, "drop")), k)
    elif sid == "0.2c":
        cam = dl.draw(shot("0.2c", [H], d_up(t, n)), k)
    elif sid == "0.3":
        d_booth(t)(k, c)
        if speaking("0.3", tt):
            say = ("Donnie.", (270, 178), True)
    elif sid == "0.5a":
        w = t - 0.95                                        # "first"
        tp = 0.0 if w < 0 else (1.0 if w < 0.17 else max(0.0, 1.0 - (w - 0.17) / 0.17))
        d_booth(t, tap=tp, jolt=2.0 if 0 <= w < 0.09 else 0.0)(k, c)
        if speaking("0.5", tt):
            say = ("My men go in first.", (270, 178), True)
    elif sid == "0.7a":
        d_booth(t, down=t >= 0.75, jolt=3.0 if 0.75 <= t < 0.84 else 0.0)(k, c)
        if speaking("0.7", tt):
            say = ("Today.", (270, 178), True)
    else:
        fn = {"0.4": lambda: d_call(t, tt, "happy", key="0.4"),
              "0.5b": lambda: d_call(t, tt, "happy", face2="neutral", at2=0.75),
              "0.6": lambda: d_call(t, tt, "confused", key="0.6"),
              "0.7b": lambda: d_call(t, tt, "panic", lower=t / 0.25, lit=False)}[sid]()
        box = {}

        def wrap(k_, o_):
            fn(k_, o_); box.update(o_)
        cam = dl.draw(shot("close", [H], wrap, CLOSE), k)
        P = lambda w: (270 + (w[0] - cam[0]) * cam[2], 480 + (w[1] - cam[1]) * cam[2])
        if sid == "0.4" and speaking("0.4", tt):
            say = ("Dad! Great timing!", P(box["mouth"]), -1)
        elif sid == "0.6" and speaking("0.6", tt):
            say = ("Tomorrow?", P(box["mouth"]), -1)
        elif sid == "0.5b" and speaking("0.5", tt):
            say = ("I arrive at five.", P(box["phone"]), 1)
    c.identity_matrix(); c.scale(hi, hi)
    if say:
        txt, tip, up = say
        if up is True:
            bubble(c, txt, (tip[0], tip[1] - 14), y=200, up=True)
        else:
            bubble(c, txt, tip, y=128, side=up)
    return surf, sid


def sound(out):
    mix = np.zeros(int((TOTAL + 0.3) * SR))

    def put(a, at_, g=1.0):
        i0 = int(at_ * SR); a = a[:max(0, len(mix) - i0)]; mix[i0:i0 + len(a)] += a * g
    for key, at_ in TAKES:
        put(WAV[key], at_)
    for at_ in (0.0, T0["0.2a"]):                           # the ring, until the freeze
        put(fx.ring(0.40), at_, 0.35)
    put(fx.whoosh(0.45), T0["0.2b"], 0.5)                   # PSSSH
    put(fx.step(), T0["0.2b"] + 0.10, 0.6)                  # the seat lands
    put(fx.ring(0.40), T0["0.2c"], 0.30)                    # still ringing
    put(fx.tap(), T0["0.5a"] + 0.95, 0.7)                   # the finger, on "first"
    put(fx.tap(140.0), T0["0.7a"] + 0.75, 0.6)              # the phone, face down
    sf.write(out, mix, SR)


def main(hi=1):
    tmp = "/tmp/dh_s1_%s" % V; os.makedirs(tmp, exist_ok=True)
    ds.ARM_PHONE[0] = False
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
    out = "%s/dh_s1_anim_%s%s.mp4" % (OUT, V, "" if hi == 1 else "_1080")
    part = out[:-4] + ".tmp.mp4"
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", tmp + "/list.txt", "-i", tmp + "/a.wav",
                           "-vf", "fps=30,format=yuv420p", "-af", "loudnorm=I=-16:TP=-2:LRA=11,aresample=48000", "-c:v", "libx264", "-crf", "19",
                           "-preset", "veryfast", "-c:a", "aac", "-b:a", "160k", "-t", "%.3f" % TOTAL, part])
    os.rename(part, out)
    cols = 12; tw, th = 180, 320; rows_ = (len(tiles) + cols - 1) // cols
    sheet = cairo.ImageSurface(cairo.FORMAT_RGB24, cols * tw, rows_ * (th + 18)); c = cairo.Context(sheet)
    c.set_source_rgb(1, 1, 1); c.paint()
    for i, (p, sid, tt) in enumerate(tiles):
        im = cairo.ImageSurface.create_from_png(p)
        x, y = (i % cols) * tw, (i // cols) * (th + 18)
        c.save(); c.translate(x, y + 18); c.scale(tw / float(im.get_width()), th / float(im.get_height())); c.set_source_surface(im, 0, 0); c.paint(); c.restore()
        c.set_source_rgb(0, 0, 0); c.select_font_face("Inter", 0, 1); c.set_font_size(12); c.move_to(x + 4, y + 13); c.show_text("%s  %.2f" % (sid, tt))
    sheet.write_to_png("%s/dh_s1_anim_%s_strip.png" % (OUT, V))
    print("wrote", out, "%.2f s, %d drawings" % (TOTAL, N))


if __name__ == "__main__":
    main(2 if (len(sys.argv) > 1 and sys.argv[1] == "hi") else 1)
