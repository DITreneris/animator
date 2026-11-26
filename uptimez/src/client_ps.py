"""THE CLIENT in "Pick a Side" (episode 14): his garage look from 13 (client_of), in Father's velvet booth, filthy with oil.
Tomas, 23 Nov, /grill-me: arms, face and shirt; leans in to point at the phone, then sits back and leaves a black
handprint on the velvet; bored, then the watch; the red rag over his shoulder, never used.
Nothing in client_of / client_ob changes: the oil goes in through client_of's own globals (its `limb`, for the forearm
and the hand) for the length of one call, and the rest is drawn over him.
  client(k, x, feet, s, pose="open", face="bored", look=(0, 0), turn=0.0)       client_of.client, oily
  cast_client(k, x, feet, s, look, targets, clip_hip, face)                     of_cast.client (IK arms), oily
  overlay(k, x, feet, s, turn=0.0)                                              the cheek, the shirt, the rag
  python3 client_ps.py [out_dir]  ->  ps_client_v2.png (sheet), ps_client_phone_v2.png (phone check); v1: client_ps_v1.py"""
import math
import os
import sys
from contextlib import contextmanager
import cairo
import kit
import client_ob as co
import client_of as cof
from kit import Ctx, INK, cut, rect, ellipse

OIL = (0.17, 0.13, 0.11)
OIL_SHINE = (0.42, 0.36, 0.32)
POINT_V2 = [False]                                 # opt-in (Pick a Side 4.3a, review 26 Nov: "a brown fist, no index"): the pointing hand
POINT_SKIN = [(0.66, 0.46, 0.34)]                  # the film sets its own (below in ps_film)
POINT_LEN = [1.30]
POINT_W = [1.0]                    # in dirty skin, not oil, its index long and clear, the others one curled block
HAND_OIL = (0.21, 0.12, 0.07)                      # the hands: oil, warm enough that of_cast.cartoon_hand doesn't take them for the robot's grey
VELVET, VELVET_D = (0.42, 0.06, 0.12), (0.26, 0.03, 0.07)
TABLE, TABLE_D = (0.20, 0.12, 0.08), (0.12, 0.07, 0.05)


_STYLE = {}                                                                # side (-1 screen-left, 1 screen-right) -> hand


@contextmanager
def oily(hands=None, aim=None, k=None):
    """client_of draws its forearm and hand with SKIN through `limb`; for this call they are oil, and each hand is
    drawn by hand() in the style asked for that side ("point", "palm", "fist"; v2, the review: the rig's ball hand
    could not act)."""
    import of_cast as oc
    g = cof.client.__globals__
    old = g["limb"]
    old_hand = kit.HAND[0]

    def limb(k, sx, sy, a1, a2, ln1, ln2, w1, w2, col1, col2, skin, hand_r, seed, *a, **kw):
        side = -1 if sx < 0 else 1
        _STYLE["now"] = (hands or {}).get(side, "fist")
        if col2 == co.SKIN:
            col2 = OIL
        if skin == co.SKIN:
            skin = OIL
        r = old(k, sx, sy, a1, a2, ln1, ln2, w1, w2, col1, col2, skin, hand_r, seed, *a, **kw)
        dx, dy = math.sin(math.radians(a1)), math.cos(math.radians(a1))      # grease along the sleeve's hem
        mx, my = sx + dx * 40, sy + dy * 40
        c = k.c
        c.set_source_rgba(*OIL, 0.55); c.set_line_width(7); c.set_line_cap(1)
        c.move_to(mx - dy * 16, my + dx * 16); c.curve_to(mx - dy * 4, my + dx * 4 + 3, mx + dy * 6, my - dx * 6, mx + dy * 18, my - dx * 18)
        c.stroke()
        return r
    g["limb"] = limb
    kit.HAND[0] = hand
    if aim and k is not None:
        _STYLE["aim_dev"] = k.c.user_to_device(*aim)
    try:
        yield
    finally:
        g["limb"] = old
        kit.HAND[0] = old_hand
        _STYLE.pop("aim_dev", None)


def hand(k, hx, hy, w, skin, seed, d, side):
    """The Client's oily hands (v2): episode 13's cartoon hand (of_cast.cartoon_hand) for a fist; "point": the index
    finger out along the forearm, the others curled; "palm": an open hand, fingers spread, flat to the surface."""
    import of_cast as oc
    style = _STYLE.get("now", "fist")
    if skin == OIL:
        skin = HAND_OIL
    if style == "fist":
        return oc.cartoon_hand(k, hx, hy, w, skin, seed, d, side)
    c = k.c
    w = w * 1.25
    a = math.atan2(d[1], d[0])
    if style == "palm":                                       # pressed flat on a wall: fingers up, whatever the forearm does
        ux_, uy_ = c.user_to_device(0, 0); vx_, vy_ = c.user_to_device(0, -1)
        a = math.atan2(vy_ - uy_, vx_ - ux_) - math.atan2(c.user_to_device(1, 0)[1] - uy_, c.user_to_device(1, 0)[0] - ux_) + 0.0
        a = -math.pi / 2
    aim = _STYLE.get("aim_dev") if style == "point" else None
    if aim:                                                   # the hand turns at the wrist so the finger aims at the target
        ax_, ay_ = c.device_to_user(*aim)                     # (the rig draws in its own scaled units)
        a = math.atan2(ay_ - hy, ax_ - hx)
    c.save(); c.translate(hx, hy); c.rotate(a)

    def blob(x, y, rx, ry, rot=0.0):
        c.save(); c.translate(x, y); c.rotate(rot); c.scale(rx, ry); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        c.set_source_rgb(*skin); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.0); c.stroke()

    def finger(x0, y0, ln, wd, ang):
        c.save(); c.translate(x0, y0); c.rotate(ang)
        c.new_path(); c.move_to(0, -wd / 2); c.line_to(ln, -wd / 2.4); c.arc(ln, 0, wd / 2.4, -math.pi / 2, math.pi / 2)
        c.line_to(0, wd / 2); c.close_path()
        c.set_source_rgb(*skin); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.0); c.stroke()
        c.restore()
    c.new_path()                                                                             # the wrist
    c.move_to(-0.55 * w, -0.30 * w); c.line_to(0.05 * w, -0.34 * w); c.line_to(0.05 * w, 0.34 * w)
    c.line_to(-0.55 * w, 0.30 * w); c.close_path()
    c.set_source_rgb(*skin); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.0); c.stroke()
    if style == "point" and POINT_V2[0]:
        skin = POINT_SKIN[0]
        w = w * POINT_W[0]
        c.new_path(); c.move_to(-0.55 * w, -0.30 * w); c.line_to(0.05 * w, -0.34 * w); c.line_to(0.05 * w, 0.34 * w)
        c.line_to(-0.55 * w, 0.30 * w); c.close_path()                                       # the wrist again, in skin
        c.set_source_rgb(*skin); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.4); c.stroke()
        blob(0.20 * w, 0.06 * w, 0.46 * w, 0.40 * w)                                         # the back of the hand
        c.new_path(); c.save(); c.translate(0.50 * w, 0.18 * w); c.scale(0.26 * w, 0.26 * w)  # the three fingers: one curled block
        c.arc(0, 0, 1, -math.pi / 2, math.pi / 2); c.line_to(-0.6, 1); c.line_to(-0.6, -1); c.close_path(); c.restore()
        c.set_source_rgb(*skin); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.4); c.stroke()
        c.set_line_width(1.6)
        for fy in (0.10, 0.26):
            c.move_to(0.48 * w, fy * w); c.line_to(0.70 * w, fy * w); c.stroke()
        finger(0.36 * w, -0.20 * w, POINT_LEN[0] * w, 0.32 * w, -0.04)                               # the index, long and straight
        blob(0.24 * w, side * 0.36 * w, 0.30 * w, 0.14 * w, side * 0.5)                     # the thumb, over the curled ones
        c.set_source_rgba(*OIL, 0.55)                                                        # his oil, on the back and the knuckle
        c.save(); c.translate(0.08 * w, 0.02 * w); c.scale(0.20 * w, 0.14 * w); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
        c.save(); c.translate((POINT_LEN[0] - 0.35) * w, -0.20 * w); c.scale(0.12 * w, 0.09 * w); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
    elif style == "point":
        for fy in (0.06, 0.30):                                                              # two fingers curled under
            blob(0.52 * w, fy * w + side * 0.0, 0.22 * w, 0.15 * w)
        blob(0.18 * w, 0.0, 0.48 * w, 0.42 * w)                                              # the palm
        finger(0.40 * w, -0.24 * w, 1.05 * w, 0.30 * w, -0.06)                               # the index, straight out
        blob(0.16 * w, side * 0.44 * w, 0.30 * w, 0.16 * w, side * 0.7)                     # the thumb, tucked
        c.set_source_rgba(1, 1, 1, 0.35); c.set_line_width(2)                                # oil shine on the finger
        c.move_to(0.6 * w, -0.32 * w); c.line_to(1.25 * w, -0.32 * w); c.stroke()
    else:                                                                                    # "palm": open, spread, flat
        c.set_source_rgba(*OIL, 0.55)                                                        # the oil squeezed out round it
        c.save(); c.translate(0.45 * w, 0); c.scale(1.25 * w, 0.95 * w); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
        blob(0.25 * w, 0.0, 0.52 * w, 0.48 * w)
        for fy, ln, an in ((-0.36, 0.78, -0.30), (-0.12, 0.92, -0.08), (0.12, 0.90, 0.08), (0.34, 0.72, 0.28)):
            finger(0.55 * w, fy * w, ln * w, 0.24 * w, an)
        finger(0.05 * w, side * 0.40 * w, 0.62 * w, 0.26 * w, side * 1.05)                  # the thumb, out
    c.restore()


def _smear(k, x, y, rx, ry, seed, alpha=0.85, drag=None):
    """An irregular oil stain: a ragged blob, and a drag tail (dx, dy) where it was wiped."""
    import random
    rnd = random.Random(seed)
    c = k.c
    pts = []
    n = 11
    for i in range(n):
        a = 2 * math.pi * i / n
        r = 1.0 + rnd.uniform(-0.28, 0.28)
        pts.append((x + math.cos(a) * rx * r, y + math.sin(a) * ry * r))
    c.set_source_rgba(*OIL, alpha)
    c.move_to(*pts[0])
    for i in range(n):
        p0, p1 = pts[i], pts[(i + 1) % n]
        mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
        c.curve_to(p0[0], p0[1], p0[0], p0[1], mx, my)
    c.close_path(); c.fill()
    if drag:
        dx, dy = drag
        c.set_source_rgba(*OIL, alpha * 0.45); c.set_line_width(min(rx, ry) * 1.3); c.set_line_cap(1)
        c.move_to(x, y); c.curve_to(x + dx * 0.3, y + dy * 0.3 + 2, x + dx * 0.7, y + dy * 0.7 - 2, x + dx, y + dy); c.stroke()


def overlay(k, x, feet, s, turn=0.0, seed=4400):
    """v2 (the review: "applied, not earned"): in his own units, the thumb-wipe up his screen-left cheek and a smudge at
    the right temple; on the T-shirt a smeared palm print, one ragged stain and a wiped streak across the stomach; the
    red rag draped over his screen-right shoulder, a folded top and a hanging tail, with grease on it."""
    c = k.c
    c.save(); c.translate(x, feet); c.scale(s * (1 - 0.18 * abs(turn)), s)
    hy, bt = co.HY, co.BT
    c.save(); c.translate(20 * turn, 0)
    c.set_source_rgba(*OIL, 0.80); c.set_line_cap(1)
    c.set_line_width(8); c.move_to(-50, hy - 2); c.curve_to(-46, hy + 8, -40, hy + 14, -32, hy + 20); c.stroke()
    c.set_line_width(4); c.move_to(-54, hy + 10); c.line_to(-46, hy + 22); c.stroke()
    _smear(k, 34, hy - 20, 7, 5, seed + 1, 0.55, drag=(6, -8))                            # the temple, where he pushed his hair back
    c.restore()
    _smear(k, 34, bt + 54, 13, 15, seed + 2, 0.75, drag=(4, 30))                         # the palm print on the chest, dragged down
    c.set_source_rgba(*OIL, 0.70); c.set_line_width(5.5); c.set_line_cap(1)
    for i, fx in enumerate((-10, -3, 5, 12)):
        c.move_to(34 + fx, bt + 44); c.line_to(34 + fx * 1.3 + 1, bt + 26 - (3 if i in (1, 2) else 0)); c.stroke()
    _smear(k, -30, bt + 76, 12, 9, seed + 3, 0.85, drag=(-6, 12))                        # one ragged stain
    c.set_source_rgba(*OIL, 0.50); c.set_line_width(9)                                    # the stomach: wiped across, left to right
    c.move_to(-46, bt + 128); c.curve_to(-20, bt + 120, 10, bt + 132, 44, bt + 122); c.stroke()
    c.set_source_rgba(*OIL, 0.28); c.set_line_width(4)
    c.move_to(-40, bt + 138); c.curve_to(-14, bt + 132, 14, bt + 140, 38, bt + 134); c.stroke()
    c.save(); c.translate(-co.SH[0] + 18, bt - 8)                                        # the rag, over his screen-left shoulder (the watch arm is free)
    cut(k, [(-16, -6), (24, -12), (30, -2), (26, 18), (30, 46), (24, 74), (14, 66), (8, 84), (-2, 70), (-10, 78),
            (-12, 50), (-16, 22)], co.RAG, lw=2.2)
    cut(k, [(-16, -6), (24, -12), (30, -2), (26, 10), (-14, 14)], (0.66, 0.16, 0.15), shadow=False, lw=1.8)   # the fold over the top
    c.set_source_rgba(0.40, 0.08, 0.08, 0.65); c.set_line_width(1.8); c.set_line_cap(1)
    for a_, b_ in (((-6, 24), (-2, 66)), ((10, 22), (14, 60))):                          # the folds hanging
        c.move_to(*a_); c.line_to(*b_); c.stroke()
    _smear(k, 16, 36, 6, 7, seed + 4, 0.70)
    _smear(k, -4, 58, 4, 5, seed + 5, 0.60)
    c.restore()
    c.restore()


def client(k, x, feet, s=1.0, pose="open", face="bored", look=(0, 0), seed=900, turn=0.0, hands=None):
    with oily(hands):
        o = cof.client(k, x, feet, s, pose, face, look=look, seed=seed, turn=turn)
    overlay(k, x, feet, s, turn)
    return o


def cast_client(k, x, feet, s, look=(-1, 0), targets=(), clip_hip=False, face="bored", hands=None, aim=None):
    """aim: (x, y) in the caller's units: where the pointing finger points (it turns at the wrist)."""
    import of_cast as oc
    with oily(hands, aim, k):
        o = oc.client(k, x, feet, s, look=look, targets=targets, clip_hip=clip_hip, face=face)
    overlay(k, x, feet, s)
    return o


# --- the booth (a wider version of 12's, for the two-shot 4.3) --------------------------------------------------------
def booth_room(k, w, h, seat_y, table_y, x0=0):
    """The velvet booth seen front on: the dark club, red neon, a buttoned burgundy bench back, a dark table in front."""
    import dh_props as dp
    c = k.c
    g = cairo.LinearGradient(0, 0, 0, h); g.add_color_stop_rgb(0, 0.10, 0.02, 0.05); g.add_color_stop_rgb(1, 0.03, 0.01, 0.03)
    c.set_source(g); c.rectangle(x0, 0, w, h); c.fill()
    for yy, a in ((seat_y - 520, 0.9), (seat_y - 480, 0.55)):
        for wd, al in ((26, 0.10), (14, 0.22), (5, a)):
            c.set_source_rgba(*dp.NEON, al); c.set_line_width(wd); c.set_line_cap(1)
            c.move_to(x0 + 20, yy); c.line_to(x0 + w - 20, yy); c.stroke()
    top = seat_y - 440                                                   # v2: the bench back rises above their heads
    c.set_source_rgb(*VELVET); c.rectangle(x0 + 10, top, w - 20, seat_y - top + 40); c.fill()
    c.set_source_rgb(*VELVET_D); c.set_line_width(3)
    for i in range(1, int(w / 90) + 1):                                  # the channel tufting
        xx = x0 + 10 + i * 90
        c.move_to(xx, top + 10); c.line_to(xx, seat_y + 30); c.stroke()
        for yy in range(int(top + 40), int(seat_y), 70):
            c.arc(xx, yy, 4, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(3); c.rectangle(x0 + 10, top, w - 20, seat_y - top + 40); c.stroke()


def table(k, w, table_y, x0=0, h=320):
    c = k.c
    rect(k, x0 - 10, table_y, w + 20, 26, TABLE, 4500, shadow=False, lw=2.4)
    c.set_source_rgb(*TABLE_D); c.rectangle(x0 - 10, table_y + 26, w + 20, h); c.fill()


def handprint(k, x, y, s=1.0, ang=0.2):
    """The black handprint he leaves on the velvet."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    c.set_source_rgba(*OIL, 0.92)
    c.save(); c.scale(1, 1.15); c.arc(0, 0, 14, 0, 2 * math.pi); c.restore(); c.fill()
    c.set_line_cap(1); c.set_line_width(7)
    for i, (fx, ln) in enumerate(((-12, 18), (-4, 24), (5, 24), (13, 18))):
        c.move_to(fx, -10); c.line_to(fx * 1.25, -10 - ln); c.stroke()
    c.move_to(-14, 4); c.line_to(-28, -6); c.stroke()
    c.restore()


def phone_on_table(k, x, y, s=1.0, prints=True):
    """Bodyguard 1's phone propped up on the table (its bottom edge at y + 76 s), its screen to us: the #TeamDon post,
    and his oily prints on it (on Pam, then on the heel)."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    rect(k, -46, -76, 92, 152, (0.08, 0.08, 0.09), 4510, shadow=False, lw=2.2)
    c.set_source_rgb(0.95, 0.95, 0.97); c.rectangle(-40, -68, 80, 136); c.fill()
    c.set_source_rgb(0.86, 0.80, 0.68); c.rectangle(-36, -48, 72, 70); c.fill()                # the photo
    for px_, col in ((-22, (0.15, 0.25, 0.55)), (-6, (0.45, 0.25, 0.60)), (10, (0.99, 0.97, 0.91)), (24, (0.6, 0.6, 0.62))):
        c.set_source_rgb(*col); c.rectangle(px_ - 5, -36, 10, 50); c.fill()
    c.set_source_rgb(0.95, 0.78, 0.15); c.rectangle(15, 6, 3, 16); c.fill()                   # the tape in it
    c.set_source_rgb(0.2, 0.2, 0.25); c.select_font_face("Inter", 0, 1); c.set_font_size(11)
    c.move_to(-34, 40); c.show_text("#TeamDon")
    if prints:
        for (fx, fy) in ((-6, -20), (12, 16)):
            c.set_source_rgba(*OIL, 0.55); c.save(); c.translate(fx, fy); c.scale(1, 1.3); c.arc(0, 0, 7, 0, 2 * math.pi)
            c.restore(); c.fill()
    c.restore()


def sheet(out):
    import dh_cast as dc
    import fs_storyboard as sb
    import of_cast as oc
    W, H = 2200, 1900
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W * 2, H * 2); surf.set_device_scale(2, 2)
    c = cairo.Context(surf); c.set_source_rgb(0.96, 0.95, 0.92); c.paint()
    k = Ctx(c, 0)
    cof._label(c, "PICK A SIDE · THE CLIENT · in Father's booth, filthy with oil · v2 · client_of's garage look, the same man", 40, 50, 30, center=False)
    cof._label(c, "v2 (the review): hands that act (point, palm, watch) · oil smeared, not printed · the rag draped · a booth, not a bar",
               40, 84, 18, col=(0.3, 0.3, 0.3), center=False)
    cof._label(c, "1  The look, at the series' scale", 40, 140, 22, center=False)
    F = 640
    sb.don(k, 150, F, 0.60 / 0.52, "stand", "neutral", look=(1, 0))
    cof.client(k, 360, F, 1.0, "open", "bored", look=(-1, 0))
    client(k, 580, F, 1.0, "open", "bored", look=(-1, 0))
    dc.father(k, 800, F, 0.62 / 0.52, face="hard", look=(-1, 0))
    for x, n in ((150, "Don"), (360, "13: clean"), (580, "14: oily"), (800, "Father")):
        cof._label(c, n, x, 680)
    cof._label(c, "2  Faces and hands", 1000, 140, 22, center=False)
    for i, (fc, lk, nm) in enumerate((("bored", (0, 0), "bored (rest)"), ("glance", cof.GLANCE, "eyes down: the watch"))):
        c.save(); c.rectangle(1000 + i * 300, 170, 280, 300); c.clip()
        c.translate(1140 + i * 300, 340); c.scale(2.2, 2.2); c.translate(0, -co.HY)
        client(k, 0, 0, 1.0, "open", fc, look=lk)
        c.restore()
        cof._label(c, nm, 1140 + i * 300, 500)
    for j, (st, nm) in enumerate((("point", "point"), ("palm", "palm, pressed"), ("fist", "fist (13's hand)"))):
        hx, hy = 1660 + j * 170, 330
        _STYLE["now"] = st
        hand(k, hx, hy, 46, OIL, 4600 + j, (0.0, 1.0) if st == "fist" else (0.0, -1.0) if st != "point" else (1.0, -0.15), 1)
        cof._label(c, nm, hx, 500)
    _STYLE.pop("now", None)
    cof._label(c, "3  The booth, 4.3: he points, Father nods; he presses his palm on the velvet; the print stays, the watch", 40, 780, 22, center=False)
    PW, PH = 690, 760
    for j, title in enumerate(("4.3a · the index finger on the photo", "4.3b · the palm pressed flat on the velvet",
                               "4.3c · the print stays; wrist up, eyes down")):
        x0 = 40 + j * (PW + 20)
        y0 = 820
        c.save(); c.rectangle(x0, y0, PW, PH); c.clip()
        seat = y0 + 640
        tbl = seat - 60
        booth_room(k, PW, y0 + PH, seat, tbl, x0)
        s = 1.15
        hip_feet = seat - co.HIP * s
        cx = x0 + 470
        if j == 2:
            handprint(k, cx + 150, seat - 130, 1.5, 0.15)
        phone_on_table(k, x0 + 245, tbl - 90, 1.2, prints=True)
        dc.father(k, x0 + 120, seat + 170, 0.62 / 0.52 * 1.15, face="hard", look=(0.6, 0.5))
        if j == 0:
            c.save(); c.translate(cx, seat); c.rotate(-0.16); c.translate(-cx, -seat)
            cast_client(k, cx, hip_feet, s, look=(-1.2, 1.4), targets=[(x0 + 335, tbl - 128), (cx + 40, tbl - 6)],
                        clip_hip=True, hands={-1: "point"}, aim=(x0 + 240, tbl - 122))
            c.restore()
        elif j == 1:
            cast_client(k, cx, hip_feet, s, look=(-0.4, 0.2), targets=[(cx - 80, tbl - 6), (cx + 150, seat - 130)],
                        clip_hip=True, hands={1: "palm"})
        else:
            wt = (cx + 30 * s, hip_feet + (co.HY + 70) * s)
            cast_client(k, cx, hip_feet, s, look=cof.GLANCE, targets=[(cx - 80, tbl - 6), wt], clip_hip=True, face="glance")
        table(k, PW, tbl, x0)
        c.restore()
        c.set_source_rgb(*INK); c.set_line_width(3); c.rectangle(x0, y0, PW, PH); c.stroke()
        cof._label(c, title, x0 + PW / 2, y0 + PH + 34, 17)
    surf.write_to_png(out); print("wrote", out)


def phone(out):
    import dh_cast as dc
    frames = []
    for name, txt in (("two-shot", "4.3: Father and the Client in the booth"), ("medium", "4.3: the finger, the oil"),
                      ("close", "the cheek, the shirt, the rag")):
        f = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(f); k = Ctx(c, 0)
        if name == "two-shot":
            seat, tbl = 820, 760
            booth_room(k, 540, 960, seat, tbl)
            s = 1.55
            phone_on_table(k, 205, tbl - 110, 1.45)
            dc.father(k, 105, seat + 230, 0.62 / 0.52 * 1.55, face="hard", look=(0.8, 0.4))
            cast_client(k, 470, seat - co.HIP * s, s, look=(-1.2, 1.2), targets=[(292, tbl - 150), (480, tbl - 6)], clip_hip=True,
                        hands={-1: "point"}, aim=(200, tbl - 150))
            table(k, 540, tbl)
        elif name == "medium":
            seat, tbl = 920, 860
            booth_room(k, 540, 960, seat, tbl)
            s = 1.8
            phone_on_table(k, 95, tbl - 120, 1.6)
            cast_client(k, 380, seat - co.HIP * s, s, look=(-1.2, 1.4), targets=[(195, tbl - 170), (380, tbl - 6)], clip_hip=True,
                        hands={-1: "point"}, aim=(95, tbl - 170))
            table(k, 540, tbl)
        else:
            booth_room(k, 540, 960, 1400, 1500)
            s = 2.6
            client(k, 290, 420 - co.HY * s, s, "open", "bored", look=(-0.6, 0))
        frames.append((name, txt, f))
    W = 3 * 270 + 4 * 20
    s_ = cairo.ImageSurface(cairo.FORMAT_RGB24, W, 480 + 80); c = cairo.Context(s_); c.set_source_rgb(0.15, 0.15, 0.16); c.paint()
    for i, (name, txt, f) in enumerate(frames):
        c.save(); c.translate(20 + i * 290, 20); c.scale(0.5, 0.5); c.set_source_surface(f, 0, 0); c.paint(); c.restore()
        c.select_font_face("Inter", 0, 1); c.set_font_size(15); c.set_source_rgb(1, 1, 1)
        c.move_to(20 + i * 290, 522); c.show_text(name.upper() + " · at 270 px")
        c.select_font_face("Inter", 0, 0); c.set_font_size(12); c.move_to(20 + i * 290, 542); c.show_text(txt)
    s_.write_to_png(out); print("wrote", out)


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else "../pick-a-side"
    os.makedirs(d, exist_ok=True)
    sheet(os.path.join(d, "ps_client_v2.png"))
    phone(os.path.join(d, "ps_client_phone_v2.png"))
