"""OFFICE NOIR 3: the walkers turned to the side, v2 (v1 pinned: drawn from nothing, and Tomas: "very bad profiles, the
proportions are not kept, bad graphics, 1/10").

v2 is not a new drawing of anyone. Each figure is its OWN front drawing (the same head, face, clothes, colours and line),
turned three quarters: the head and body are the front drawing narrowed (Q), its eyes to where it goes; only what has to
change to walk is new, and it is built from the front drawing's own parts and measures: two legs seen from the side with
a knee (the front's trousers, tights, shoes), and two arms from one shoulder, the far one behind the body, the near one
over it (the front's own sleeve, glove and hand code).

  client(k, x, feet, s, dir_, cig, folder, face)
  don(k, x, feet, s, dir_, bent)
  her(k, x, feet, s, dir_)
x is where they are on the ground: the step is taken from it (no sliding). Each returns {"head": (x, y)}; the Client
also "tip" (the end of his cigarette)."""
import math
import contextlib
import cairo
import kit
from kit import cut, ellipse, INK
import client_on3 as b
import noir2_cast as n2
import motion_on3 as mo
import sofia_ob as sob
import sofia_v4 as sf
import sofia_bc as sbc

TAU = 2 * math.pi
Q = 0.70                                                     # how narrow the front drawing is when it is turned
d = n2.d


def stride(u, a, up):
    """One foot through a step: on the ground it goes back under him; in the air it swings forward, heel first down."""
    u = u % 1.0
    if u < 0.5:
        return a * (1 - 4 * u), 0.0, -0.22 + 1.2 * u          # (ahead, lift, pitch): heel strike to toe-off
    q = (u - 0.5) / 0.5
    return -a + 2 * a * q, up * math.sin(math.pi * q) ** 0.8, 0.38 - 0.6 * q


def _walk(x, s, dir_, a, up, rise):
    u = x / (4.0 * a * s) * dir_
    return u, stride(u, a, up), stride(u + 0.5, a, up), -rise * abs(math.sin(TAU * u)), math.sin(TAU * u)


def _knee(hip, foot, l1, l2):
    dx, dy = foot[0] - hip[0], foot[1] - hip[1]
    dd = max(1.0, min(math.hypot(dx, dy), l1 + l2 - 0.5))
    a0 = math.atan2(dy, dx)
    a1 = math.acos(max(-1.0, min(1.0, (l1 * l1 + dd * dd - l2 * l2) / (2 * l1 * dd))))
    return hip[0] + l1 * math.cos(a0 - a1), hip[1] + l1 * math.sin(a0 - a1)      # the knee, bent forward


def _board(k, p0, p1, w0, w1, col, lw=2.2):
    """A cut-out limb: a paper board from p0 to p1, as the front drawings' trouser legs are."""
    g = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
    nx, ny = -math.sin(g), math.cos(g)
    cut(k, [(p0[0] + nx * w0 / 2, p0[1] + ny * w0 / 2), (p1[0] + nx * w1 / 2, p1[1] + ny * w1 / 2),
            (p1[0] - nx * w1 / 2, p1[1] - ny * w1 / 2), (p0[0] - nx * w0 / 2, p0[1] - ny * w0 / 2)], col, shadow=False, lw=lw)


def _leg(k, hip, f, w, col, seam=None, joint=True):
    """hip to knee to ankle; returns the ankle. The knee is a round of the same cloth, so the two boards read as one leg."""
    c = k.c
    ank = (hip[0] + f[0], -f[1] - 20)
    ll = (-20 - hip[1]) * 0.515
    kn = _knee(hip, ank, ll, ll)
    _board(k, hip, kn, w, w * 0.92, col)
    _board(k, kn, ank, w * 0.92, w * 0.84, col)
    if joint:
        c.new_path(); c.arc(kn[0], kn[1], w * 0.43, 0, TAU); c.set_source_rgb(*col); c.fill()
    if seam:
        c.set_source_rgb(*seam); c.set_line_width(2.0); c.set_line_cap(1)
        c.new_path(); c.move_to(*hip); c.line_to(*kn); c.line_to(*ank); c.stroke(); c.set_line_cap(0)
    return ank


@contextlib.contextmanager
def _swap(*triples):
    old = [(o, n, getattr(o, n)) for o, n, _ in triples]
    for o, n, v in triples:
        setattr(o, n, v)
    try:
        yield
    finally:
        for o, n, v in old:
            setattr(o, n, v)


def _turned(c, x, dir_, q=None):
    """The front drawing standing at x, narrowed about x (and mirrored when it goes left)."""
    c.save(); c.translate(x, 0); c.scale((q or Q) * dir_, 1); c.translate(-x, 0)


# ---- the Client -------------------------------------------------------------------------------------------------------
def _trainer(k, ank, pitch):
    c = k.c
    c.save(); c.translate(ank[0], ank[1] + 20); c.rotate(pitch)
    ellipse(k, 9, -3, 33, 7, b.SOLE, 31, shadow=False, lw=2)
    ellipse(k, 7, -11, 31, 12, b.TRAINER, 32, shadow=False, lw=2)
    c.restore()


def _client_leg(k, hip, f, col):
    ank = _leg(k, hip, f, 50, col, seam=b.CHAR_LINE)
    c = k.c
    g = 0.0
    cut(k, [(ank[0] - 22, ank[1] - 8), (ank[0] + 22, ank[1] - 8), (ank[0] + 21, ank[1] + 7), (ank[0] - 21, ank[1] + 7)], b.CHAR_DARK, shadow=False, lw=1.8)   # the cuff
    _trainer(k, ank, f[2])


def _client_arm(k, u, f, seed):
    """The front drawing's own arm (the same limb, shoulder and glove), hung from one shoulder seen from the side."""
    sx, sy = -12, b.BT + 44
    hx, hy = b.limb(k, sx, sy, u, f, b.LN1, b.LN2, 50, 43, b.CHAR, b.CHAR, b.CHAR, 4, seed)
    ellipse(k, sx, sy - 1, 24, 21, b.CHAR, seed + 4, shadow=False, lw=2)
    ex, ey = sx + b._d(u)[0] * b.LN1, sy + b._d(u)[1] * b.LN1
    ux, uy = (hx - ex) / b.LN2, (hy - ey) / b.LN2
    b._glove(k, hx, hy, ux, uy, 1, seed + 60)
    return hx, hy


def client(k, x, feet, s=1.0, dir_=1, cig=False, folder=False, face="hard"):
    u, f0, f1, yb, sw = _walk(x, s, dir_, 46.0, 30.0, 9.0)
    c = k.c
    hip = (0, b.HIP - 8 + yb)

    def unit():
        c.save(); c.translate(x, feet); c.scale(s * dir_, s)

    unit()
    c.save(); c.translate(0, yb)
    _client_arm(k, -24 * sw + 4, 24, 911)                                                   # the far arm, behind him
    c.restore()
    _client_leg(k, (hip[0] + 3, hip[1]), f1, tuple(v * 0.86 for v in b.CHAR))               # the far leg
    _client_leg(k, hip, f0, b.CHAR)
    c.restore()
    _turned(c, x, dir_)                                                                     # his own front drawing: head, hood, hoodie
    with _swap((b, "limb", lambda k_, sx, sy, a1, a2, *a, **kw: (sx, sy + 150)), (b, "_glove", lambda *a, **kw: None),
               (b, "_lower_street", lambda *a, **kw: None), (b, "ellipse", _no_shoulder(b.ellipse))):
        o = b.boxer(k, x, feet + yb * s, s, "b_walk", face, (0.9, 0.0), outfit="street", cig=cig)
    head = c.user_to_device(*o["head"])
    tip = c.user_to_device(x + 47 * s, feet + (yb + b.HY + 50) * s)
    c.restore()
    unit(); c.translate(0, yb)
    if folder:                                                                              # the folder, clamped under his near arm
        c.save(); c.translate(6, b.BT + 96); c.rotate(-0.14); cut(k, [(-34, -24), (36, -24), (36, 26), (-34, 26)], b.IVORY, shadow=False, lw=2); c.restore()
        _client_arm(k, 4, 78, 913)
    else:
        _client_arm(k, 24 * sw + 4, 24, 913)                                                # the near arm, over him
    c.restore()
    return {"head": c.device_to_user(*head), "tip": c.device_to_user(*tip)}


def _no_shoulder(orig):
    def e(k, x, y, rx, ry, *a, **kw):
        if (rx, ry) == (24, 21):
            return None
        return orig(k, x, y, rx, ry, *a, **kw)
    return e


# ---- Don --------------------------------------------------------------------------------------------------------------
def _don_arm(k, u, f, glass=False):
    """mo._sleeves' sleeve, cuff and hand, one arm from one shoulder."""
    c = k.c
    dd = lambda g: (math.sin(math.radians(g)), math.cos(math.radians(g)))
    sx, sy, ln = -10, d.BT + 26, 48
    ex, ey = sx + dd(u)[0] * ln, sy + dd(u)[1] * ln
    hx, hy = ex + dd(u + f)[0] * ln, ey + dd(u + f)[1] * ln
    qx, qy = hx - dd(u + f)[0] * 9, hy - dd(u + f)[1] * 9
    if glass:
        n2.magnifier(k, hx, hy, 1.0, math.radians(100 - (u + f) * 0.2))
    for w, colr in ((23, INK), (19, d.TRENCH)):
        c.set_source_rgb(*colr); c.set_line_width(w); c.set_line_cap(0); c.set_line_join(1)
        c.new_path(); c.move_to(sx, sy - (2 if colr == INK else 0)); c.curve_to(ex, ey, ex, ey, qx, qy); c.stroke()
    for w, colr in ((23, INK), (19, d.TRENCH_SHADE)):                                       # the cuff
        c.set_source_rgb(*colr); c.set_line_width(w)
        c.new_path(); c.move_to(qx - dd(u + f)[0] * (2 if colr == INK else 0), qy - dd(u + f)[1] * (2 if colr == INK else 0))
        c.line_to(qx + dd(u + f)[0] * 6, qy + dd(u + f)[1] * 6); c.stroke()
    ang = math.atan2(dd(u + f)[1], dd(u + f)[0])
    c.save(); c.translate(hx, hy); c.rotate(ang)
    c.new_path(); c.move_to(-8, -8); c.curve_to(2, -11, 13, -9, 15, -3); c.curve_to(16, 4, 10, 9, 0, 9); c.line_to(-8, 8); c.close_path()
    c.set_source_rgb(*d.SKIN); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2); c.stroke()
    c.restore()
    return hx, hy


def _don_leg(k, hip, f, col):
    c = k.c
    ank = (hip[0] + f[0], -f[1] - 10)
    ll = (-10 - hip[1]) * 0.515
    kn = _knee(hip, ank, ll, ll)
    _board(k, hip, kn, 28, 27, col); _board(k, kn, ank, 27, 26, col)
    c.new_path(); c.arc(kn[0], kn[1], 12, 0, TAU); c.set_source_rgb(*col); c.fill()
    c.save(); c.translate(ank[0], ank[1] + 10); c.rotate(f[2])
    cut(k, [(-14, -13), (10, -13), (28, -5), (28, 0), (-14, 0)], mo.SHOE, shadow=False, lw=1.8)      # the front drawing's walking shoe
    c.restore()


def don(k, x, feet, s=1.0, dir_=1, bent=0.0):
    u, f0, f1, yb, sw = _walk(x, s, dir_, 34.0, 22.0, 6.0)
    c = k.c
    hip = (0, d.HEM - 46 + yb)
    lean = 10.0 * bent

    def unit(tilt=True):
        c.save(); c.translate(x, feet); c.scale(s * dir_, s)
        if tilt:
            c.translate(0, yb); c.rotate(math.radians(lean))

    unit(False)
    _don_leg(k, (hip[0] + 2, hip[1]), f1, tuple(v * 0.86 for v in mo.TROUSERS))
    _don_leg(k, hip, f0, mo.TROUSERS)
    c.restore()
    unit(); _don_arm(k, -20 * sw * (1 - bent) + 6, 18); c.restore()                         # the far arm, behind his coat
    _turned(c, x, dir_, 0.76)
    c.save(); c.translate(x, feet + yb * s); c.rotate(math.radians(lean)); c.scale(s, s)     # only his coat's width below the collar: the shirt arms under the front drawing's sleeves stay out
    c.new_path(); c.rectangle(-300, -900, 600, 900 + d.BT - 2); c.move_to(-47, d.BT - 2); c.line_to(47, d.BT - 2); c.line_to(57, d.HEM + 2); c.line_to(-57, d.HEM + 2); c.close_path()
    c.restore(); c.clip()
    with _swap((mo, "_legs", lambda *a, **kw: None), (mo, "_sleeves", lambda k_, pose, col, seed, cuff=None: [(0, 0), (0, 0)])):
        o = mo.don(k, x, feet + yb * s, s, "look", "squint", (0.9, 0.5 * bent), lean=lean, glass=False)
    head = c.user_to_device(*o["head"])
    c.restore()
    unit()
    if bent > 0.5:
        _don_arm(k, 52, 30, glass=True)                                                     # his glass, held out low
    else:
        _don_arm(k, 20 * sw + 6, 18)
    c.restore()
    return {"head": c.device_to_user(*head)}


# ---- the woman under the umbrella --------------------------------------------------------------------------------------
def _her_leg(k, hip, f, col):
    c = k.c
    ank = (hip[0] + f[0], -f[1] - 22)
    ll = (-22 - hip[1]) * 0.512
    kn = _knee(hip, ank, ll, ll)
    _board(k, hip, kn, 17, 15, col, lw=1.8); _board(k, kn, ank, 15, 12, col, lw=1.8)
    c.new_path(); c.arc(kn[0], kn[1], 6.6, 0, TAU); c.set_source_rgb(*col); c.fill()
    c.save(); c.translate(ank[0], ank[1] + 22); c.rotate(f[2] * 0.7)
    cut(k, [(-8, -28), (8, -28), (17, -3), (17, 0), (-6, 0), (-8, -6)], mo.BOOT, shadow=False, lw=1.6)   # the front drawing's boot
    c.restore()


def her(k, x, feet, s=1.0, dir_=-1):
    u, f0, f1, yb, sw = _walk(x, s, dir_, 30.0, 18.0, 5.0)
    c = k.c
    hip = (0, mo.HEM_HER - 40 + yb)
    col = [sbc.BLAZER]

    def unit():
        c.save(); c.translate(x, feet); c.scale(s * dir_, s)

    def arm(a1, a2, seed):
        with _swap((sf, "BLOUSE", col[0])):
            return sf._arm(k, 0, sob.BODY_TOP + 14 + yb, a1, a2, seed, w=15)

    unit()
    arm(-18 * sw + 4, 14, 21)                                                               # the far arm, behind her
    _her_leg(k, (hip[0] + 2, hip[1]), f1, tuple(v * 0.8 for v in mo.TIGHTS))
    _her_leg(k, hip, f0, mo.TIGHTS)
    c.restore()

    def no_arm(k_, sx, sy, a1, a2, seed, ln=48, w=17):
        col[0] = sf.BLOUSE
        return sx, sy + 90

    _turned(c, x, dir_, 0.74)
    c.save(); c.rectangle(x - 400, feet - 4000, 800, 4000 + (mo.HEM_HER + 2 + yb) * s); c.clip()        # her own front drawing, down to her hem
    with _swap((sf, "_arm", no_arm)):
        o = sob.sofia(k, x, feet + yb * s, s, "low", "smile", (0.95, 0.15), badge=False, tablet_kind=None)
    c.restore()
    head = c.user_to_device(*o["head"])
    c.restore()
    unit()
    hx, hy = arm(34, 118, 23)                                                               # the near arm, up: the umbrella, the street's own
    c.set_source_rgb(0.10, 0.10, 0.12); c.set_line_width(4); c.move_to(hx, hy + 8); c.line_to(hx - 4, hy - 250); c.stroke()
    c.new_path(); c.move_to(hx - 124, hy - 236); c.curve_to(hx - 98, hy - 330, hx + 90, hy - 330, hx + 116, hy - 236)
    for i in range(4):
        x0 = hx + 116 - 60 * i; c.curve_to(x0 - 10, hy - 250, x0 - 50, hy - 250, x0 - 60, hy - 236)
    c.close_path(); c.set_source_rgb(0.08, 0.08, 0.10); c.fill_preserve(); c.set_source_rgb(0.02, 0.02, 0.03); c.set_line_width(3); c.stroke()
    ellipse(k, hx, hy, 9, 9, sob.SKIN, 64, shadow=False, lw=2)
    c.restore()
    return {"head": c.device_to_user(*head)}


def turn(c, x, p):
    """Call before drawing a figure standing at x: narrowed as it turns (p 0 = as drawn, 1 = at its narrowest)."""
    q = max(0.45, 1.0 - p)
    c.translate(x, 0); c.scale(q, 1); c.translate(-x, 0)
