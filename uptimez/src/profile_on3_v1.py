"""OFFICE NOIR 3: the cast in profile, walking, v1 (21 Nov). Tomas: "walking from the side: we do it." The film's figures
face us, so a walk across the frame was a shuffle ("waddle", "close to a slide", five cold tests). Here each walker has a
side drawing made for walking: legs with a knee, a foot that lands on its heel and leaves on its toe, arms that swing
against the legs, a body that rises as one foot passes the other and leans the way it goes.
  client(k, x, feet, s, dir_, cig=False, folder=False)   the hooded man, street clothes, red gloves
  don(k, x, feet, s, dir_, bent=0.0)                      trench coat, fedora, his glass held out ahead
  her(k, x, feet, s, dir_)                                the woman under the umbrella
x is where they are on the ground: the step is taken from it (no sliding). Each returns {"head": (x, y)}.
turn(c, x, p)  the paper figure's turn between a side drawing and a front one: squeezed to an edge and out again."""
import math
import cairo
import kit
from kit import cut, ellipse, INK
import client_on3 as b
import client_ob as co
import noir2_cast as n2
import sofia_ob as sob

d = n2.d
TAU = 2 * math.pi


def stride(u, a, up):
    """One foot through a step: on the ground it goes back under him; in the air it swings forward, heel first down."""
    u = u % 1.0
    if u < 0.5:
        return a * (1 - 4 * u), 0.0, -0.25 + 1.4 * u          # (ahead, lift, pitch): heel strike to toe-off
    q = (u - 0.5) / 0.5
    return -a + 2 * a * q, up * math.sin(math.pi * q) ** 0.8, 0.45 - 0.7 * q


def _limb(c, p0, p1, w, col, lw=2.2):
    for ww, cc in ((w + 2 * lw, INK), (w, col)):
        c.set_source_rgb(*cc); c.set_line_width(ww); c.set_line_cap(1)
        c.new_path(); c.move_to(*p0); c.line_to(*p1); c.stroke()
    c.set_line_cap(0)


def _knee(hip, foot, l1, l2):
    dx, dy = foot[0] - hip[0], foot[1] - hip[1]
    dd = min(math.hypot(dx, dy), l1 + l2 - 0.5)
    a0 = math.atan2(dy, dx)
    a1 = math.acos(max(-1.0, min(1.0, (l1 * l1 + dd * dd - l2 * l2) / (2 * l1 * dd))))
    return hip[0] + l1 * math.cos(a0 - a1), hip[1] + l1 * math.sin(a0 - a1)      # the knee, bent forward


def _leg(k, hip, f, l1, l2, w, col, shoe, sole=None, heel=0.0):
    c = k.c
    ank = (hip[0] + f[0], -f[1] - 9)
    kn = _knee(hip, ank, l1, l2)
    _limb(c, hip, kn, w, col); _limb(c, kn, ank, w * 0.86, col)
    c.save(); c.translate(ank[0], ank[1] + 9); c.rotate(f[2])
    if sole:
        cut(k, [(-13, -3), (27, -3), (29, 3), (-14, 3)], sole, shadow=False, lw=1.6)
    cut(k, [(-14, -16), (6, -17), (26, -9), (29, -2), (-14, -2)], shoe, shadow=False, lw=2)
    if heel:
        cut(k, [(-13, -2), (-7, -2), (-9, heel), (-12, heel)], shoe, shadow=False, lw=1.4)
    c.restore()


def _arm(c, sh, a1, a2, l1, l2, w, col):
    e = (sh[0] + l1 * math.sin(a1), sh[1] + l1 * math.cos(a1))
    h = (e[0] + l2 * math.sin(a1 + a2), e[1] + l2 * math.cos(a1 + a2))
    _limb(c, sh, e, w, col); _limb(c, e, h, w * 0.9, col)
    return e, h


def _walk(x, s, dir_, a, up, rise):
    u = x / (4.0 * a * s) * dir_
    return u, stride(u, a, up), stride(u + 0.5, a, up), -rise * abs(math.sin(TAU * u)), math.sin(TAU * u)


def _open(k, x, feet, s, dir_, yb, lean):
    c = k.c
    c.save(); c.translate(x, feet); c.scale(s * dir_, s); c.translate(0, yb); c.rotate(lean)
    return c


# ---- the Client -------------------------------------------------------------------------------------------------------
def client(k, x, feet, s=1.0, dir_=1, cig=False, folder=False, face="hard"):
    u, f0, f1, yb, sw = _walk(x, s, dir_, 46.0, 30.0, 9.0)
    c = k.c
    hood, trou = co.GREY, b.CHAR
    c.save(); c.translate(x, feet); c.scale(s * dir_, s)
    hip = (0, -178 + yb)
    far, near = (f1, f0)
    c.save(); c.translate(0, yb); c.rotate(0.05)                                           # the far arm, behind him
    e, h = _arm(c, (2, -292), -0.5 * sw + 0.10, 0.5, 66, 56, 34, tuple(v * 0.8 for v in hood))
    _glove(k, h, -0.5 * sw - 0.4, 0.86)
    c.restore()
    _leg(k, (hip[0] + 2, hip[1]), far, 92, 92, 44, tuple(v * 0.8 for v in trou), b.TRAINER, b.SOLE)
    c.save(); c.translate(0, yb); c.rotate(0.05)
    cut(k, [(-52, -300), (-8, -324), (44, -306), (58, -230), (50, -166), (-48, -164), (-58, -236)], hood, shadow=False, lw=2.6)      # the hoodie
    cut(k, [(10, -214), (50, -212), (50, -180), (12, -180)], tuple(v * 0.86 for v in hood), shadow=False, lw=1.8)                     # its pocket
    c.restore()
    _leg(k, hip, near, 92, 92, 46, trou, b.TRAINER, b.SOLE)
    c.save(); c.translate(0, yb); c.rotate(0.05)
    R, hy = 58.0, -372.0
    cut(k, [(16, hy - 30), (46, hy - 22), (62, hy + 4), (50, hy + 12), (54, hy + 24), (46, hy + 28), (48, hy + 44), (30, hy + 56), (0, hy + 50), (0, hy - 30)], co.SKIN, shadow=False, lw=2.2)   # brow, nose, lips, chin
    c.set_source_rgba(0.25, 0.20, 0.18, 0.30); c.new_path(); c.move_to(4, hy + 22); c.line_to(46, hy + 30); c.line_to(46, hy + 46); c.line_to(30, hy + 55); c.line_to(4, hy + 50); c.close_path(); c.fill()   # stubble
    c.set_source_rgb(*INK); c.set_line_cap(1)
    c.set_line_width(5.5); c.move_to(22, hy - 16); c.line_to(48, hy - 9); c.stroke()         # the brow, down
    c.arc(38, hy + 1, 3.4, 0, TAU); c.fill()                                                # the eye
    c.set_line_width(2.6); c.move_to(34, hy + 32); c.line_to(50, hy + 31); c.stroke(); c.set_line_cap(0)
    if cig:
        cut(k, [(48, hy + 28), (80, hy + 34), (79, hy + 40), (47, hy + 34)], (0.96, 0.95, 0.90), shadow=False, lw=1.4)
    c.new_path(); c.move_to(26, hy - 64); c.curve_to(-40, hy - 80, -78, hy - 20, -66, hy + 30)       # the hood, up: crown, back, nape, and the edge round his face
    c.curve_to(-60, hy + 70, -30, hy + 80, 12, hy + 76); c.curve_to(22, hy + 66, 6, hy + 40, 8, hy + 4)
    c.curve_to(10, hy - 30, 22, hy - 46, 26, hy - 64); c.close_path()
    c.set_source_rgb(*hood); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.6); c.stroke()
    c.set_source_rgb(*[v * 0.72 for v in hood]); c.set_line_width(3); c.new_path(); c.move_to(20, hy - 52); c.curve_to(2, hy - 30, 0, hy + 30, 12, hy + 66); c.stroke()
    tip = c.user_to_device(79, hy + 36)
    head = c.user_to_device(0, hy)
    if folder:                                                                              # the folder, under his near arm
        c.save(); c.translate(-2, -238); c.rotate(-0.16); cut(k, [(-32, -22), (34, -22), (34, 24), (-32, 24)], b.IVORY, shadow=False, lw=2); c.restore()
    e, h = _arm(c, (0, -294), (0.5 * sw + 0.06) if not folder else 0.10, 0.55 if not folder else 1.15, 66, 56, 36, hood)
    _glove(k, h, 0.5 * sw - 0.5, 1.0)
    c.restore()
    c.restore()
    return {"head": c.device_to_user(*head), "tip": c.device_to_user(*tip)}


def _glove(k, h, ang, sc):
    c = k.c
    c.save(); c.translate(*h); c.rotate(-ang); c.scale(sc, sc)
    cut(k, [(-13, -20), (13, -20), (14, -6), (-14, -6)], (0.95, 0.94, 0.90), shadow=False, lw=1.8)   # the cuff
    ellipse(k, 0, 14, 25, 27, b.KEY, 41, shadow=False, lw=2.4)
    ellipse(k, 17, 4, 10, 13, b.KEY, 42, shadow=False, lw=2)                                         # the thumb
    c.restore()


# ---- Don --------------------------------------------------------------------------------------------------------------
FELT = (0.34, 0.34, 0.38)
TROUSERS, SHOE = (0.30, 0.30, 0.34), (0.07, 0.07, 0.08)


def don(k, x, feet, s=1.0, dir_=1, bent=0.0):
    u, f0, f1, yb, sw = _walk(x, s, dir_, 30.0, 20.0, 6.0)
    c = k.c
    hem, hy = d.HEM, d.HY
    c.save(); c.translate(x, feet); c.scale(s * dir_, s)
    hip = (0, hem - 34 + yb)
    _leg(k, (hip[0] + 2, hip[1]), f1, 52, 54, 24, tuple(v * 0.8 for v in TROUSERS), SHOE)
    _leg(k, hip, f0, 52, 54, 26, TROUSERS, SHOE)
    c.save(); c.translate(0, hem + yb); c.rotate(0.06 + 0.22 * bent); c.translate(0, -hem)       # he leans from the hips, over his glass
    bt = d.BT
    e, h = _arm(c, (0, bt + 22), -0.4 * sw, 0.35, 46, 44, 21, d.TRENCH_SHADE)                    # the far arm
    ellipse(k, h[0], h[1], 10, 10, d.SKIN, 51, shadow=False, lw=2)
    cut(k, [(-34, bt + 6), (-4, bt - 6), (32, bt + 4), (42, bt + 90), (38, hem - 84), (56, hem - 6 + 5 * sw), (-52, hem - 2 - 5 * sw), (-40, hem - 84), (-42, bt + 80)],
        d.TRENCH, shadow=False, lw=2.6)                                                          # the coat: its skirts swing
    cut(k, [(-41, bt + 82), (41, bt + 82), (40, bt + 96), (-40, bt + 96)], d.TRENCH_SHADE, shadow=False, lw=1.8)   # the belt
    cut(k, [(-10, bt - 6), (24, bt + 2), (30, bt + 40), (8, bt + 16)], d.TRENCH_SHADE, shadow=False, lw=2)         # the collar, turned up
    R = 46.0
    ellipse(k, 4, hy, R * 0.86, R, d.SKIN, 52, shadow=False, lw=2.4)                              # his head
    cut(k, [(36, hy - 6), (56, hy + 8), (40, hy + 14)], d.SKIN, shadow=False, lw=2)               # the nose
    ellipse(k, -8, hy + 6, 7, 11, d.SKIN, 53, shadow=False, lw=1.8)                               # the ear
    c.set_source_rgb(0.55, 0.55, 0.57); c.set_line_width(7); c.set_line_cap(1); c.new_path(); c.arc(4, hy, 37, 2.2, 3.0); c.stroke(); c.set_line_cap(0)   # grey hair at the nape, a line of it under the brim
    c.set_source_rgb(*INK); c.set_line_cap(1); c.set_line_width(3.2)
    c.move_to(20, hy - 4); c.line_to(34, hy - 2); c.stroke()                                      # the eye, narrowed
    c.set_line_width(2.4); c.move_to(24, hy + 26); c.curve_to(30, hy + 30, 36, hy + 28, 40, hy + 24); c.stroke(); c.set_line_cap(0)
    c.new_path(); c.move_to(-58, hy - 30); c.curve_to(-30, hy - 42, 40, hy - 42, 74, hy - 24)     # the brim
    c.curve_to(40, hy - 20, -30, hy - 20, -58, hy - 30); c.close_path()
    c.set_source_rgb(*FELT); c.fill_preserve(); c.set_source_rgb(0.05, 0.05, 0.06); c.set_line_width(2.6); c.stroke()
    c.new_path(); c.move_to(-36, hy - 32); c.curve_to(-40, hy - 80, -12, hy - 86, 0, hy - 72); c.curve_to(12, hy - 88, 40, hy - 78, 38, hy - 32); c.close_path()
    c.set_source_rgb(*FELT); c.fill_preserve(); c.set_source_rgb(0.05, 0.05, 0.06); c.stroke()
    c.set_source_rgb(0.08, 0.08, 0.10); c.rectangle(-37, hy - 44, 76, 11); c.fill()               # the band
    head = c.user_to_device(4, hy)
    e, h = _arm(c, (2, bt + 24), 0.9 + 0.12 * sw + 0.25 * bent, 0.5, 46, 44, 23, d.TRENCH)         # the near arm, out ahead, with his glass
    ellipse(k, h[0], h[1], 11, 11, d.SKIN, 54, shadow=False, lw=2)
    gx, gy = h[0] + 22, h[1] + 18 * bent - 8
    c.set_source_rgb(0.10, 0.10, 0.12); c.set_line_width(6); c.set_line_cap(1); c.move_to(h[0] + 2, h[1]); c.line_to(gx - 12, gy - 4 + 10 * bent); c.stroke(); c.set_line_cap(0)
    c.set_source_rgba(0.92, 0.95, 1.0, 0.45); c.arc(gx + 10, gy, 24, 0, TAU); c.fill_preserve(); c.set_source_rgb(0.10, 0.10, 0.12); c.set_line_width(5); c.stroke()
    c.restore()
    c.restore()
    return {"head": c.device_to_user(*head)}


# ---- the woman under the umbrella --------------------------------------------------------------------------------------
HAIR = (0.93, 0.90, 0.80)
DRESS = (0.10, 0.10, 0.12)


def her(k, x, feet, s=1.0, dir_=-1):
    u, f0, f1, yb, sw = _walk(x, s, dir_, 30.0, 18.0, 5.0)
    c = k.c
    hy, top = sob.HY, sob.BODY_TOP
    c.save(); c.translate(x, feet); c.scale(s * dir_, s)
    hip = (0, -118 + yb)
    tights, boot = (0.13, 0.13, 0.15), (0.05, 0.05, 0.06)
    _leg(k, (hip[0] + 2, hip[1]), f1, 56, 58, 17, tights, boot, heel=10)
    _leg(k, hip, f0, 56, 58, 18, tights, boot, heel=10)
    c.save(); c.translate(0, yb); c.rotate(0.04)
    e, h = _arm(c, (0, top + 16), -0.45 * sw, 0.3, 42, 40, 15, tuple(v * 1.5 for v in DRESS))    # the far arm, swinging
    ellipse(k, h[0], h[1], 8, 8, sob.SKIN, 61, shadow=False, lw=1.8)
    cut(k, [(-26, top + 2), (-2, top - 8), (24, top + 4), (30, top + 70), (44 + 4 * sw, -96), (-40 - 4 * sw, -96), (-30, top + 70)], DRESS, shadow=False, lw=2.4)   # jacket and skirt
    c.set_source_rgb(0.92, 0.92, 0.90); c.set_line_width(3)                                        # her pearls
    c.new_path(); c.arc(8, top + 4, 15, 0.2, 2.6); c.stroke()
    R = 40.0
    c.new_path(); c.move_to(18, hy - 44); c.curve_to(-40, hy - 56, -62, hy - 6, -50, hy + 44)      # her hair, behind: a bob to the jaw
    c.curve_to(-40, hy + 60, -14, hy + 58, -6, hy + 40); c.line_to(0, hy - 10); c.close_path()
    c.set_source_rgb(*HAIR); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.2); c.stroke()
    ellipse(k, 6, hy, R * 0.82, R * 0.98, sob.SKIN, 62, shadow=False, lw=2.2)                      # her face
    cut(k, [(34, hy - 2), (46, hy + 8), (34, hy + 12)], sob.SKIN, shadow=False, lw=1.8)            # her nose
    c.new_path(); c.move_to(34, hy - 30); c.curve_to(10, hy - 52, -20, hy - 44, -22, hy - 8)       # her fringe
    c.curve_to(-6, hy - 22, 16, hy - 24, 36, hy - 18); c.close_path()
    c.set_source_rgb(*HAIR); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2); c.stroke()
    c.set_source_rgb(*INK); c.arc(22, hy - 4, 3.4, 0, TAU); c.fill()                               # her eye, and its lash
    c.set_line_width(2); c.set_line_cap(1); c.move_to(18, hy - 10); c.line_to(30, hy - 12); c.stroke(); c.set_line_cap(0)
    cut(k, [(26, hy + 20), (40, hy + 19), (38, hy + 25), (28, hy + 26)], sob.RED, shadow=False, lw=1.2)   # her lips
    ellipse(k, -12, hy + 22, 4.5, 4.5, (0.95, 0.95, 0.92), 63, shadow=False, lw=1.4)               # a pearl at her ear
    head = c.user_to_device(6, hy)
    e, h = _arm(c, (2, top + 18), 0.55, 2.0, 40, 40, 16, tuple(v * 1.7 for v in DRESS))           # the near arm, up: the umbrella
    ellipse(k, h[0], h[1], 8, 8, sob.SKIN, 64, shadow=False, lw=1.8)
    ux, uy = h[0], h[1]
    c.set_source_rgb(0.10, 0.10, 0.12); c.set_line_width(4 / 1.0); c.move_to(ux, uy + 8); c.line_to(ux - 2, uy - 250); c.stroke()
    c.new_path(); c.move_to(ux - 124, uy - 236); c.curve_to(ux - 98, uy - 330, ux + 90, uy - 330, ux + 116, uy - 236)
    for i in range(4):
        x0 = ux + 116 - 60 * i; c.curve_to(x0 - 10, uy - 250, x0 - 50, uy - 250, x0 - 60, uy - 236)
    c.close_path(); c.set_source_rgb(0.08, 0.08, 0.10); c.fill_preserve(); c.set_source_rgb(0.02, 0.02, 0.03); c.set_line_width(3); c.stroke()
    c.restore()
    c.restore()
    return {"head": c.device_to_user(*head)}


def turn(c, x, p):
    """Call before drawing a figure standing at x: it is squeezed toward an edge-on sheet (p 0 = full width, 1 = an edge)."""
    q = max(0.45, 1.0 - p)    # v19b: never an edge: at 8 pictures a second the figure vanished for one
    c.translate(x, 0); c.scale(q, 1); c.translate(-x, 0)
