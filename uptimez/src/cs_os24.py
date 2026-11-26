"""ONE STAR v24 (26 Nov, Tomas picked 1-6 of "more variety, the camera, more animation"):
1 slow push-ins on the punch lines (1.4 "Approved.", 3.4 the 99 % plan, 6.5 "Still one star."), about the speaker's head
  so the locked bubble's tail stays on the mouth;
2 the frame shakes on the hits (1.1 the phone on its head, 3.5b the ball on Don, 1.2 48K, 3.4b the crumple);
3 a whip pan from the throw (3.5's last drawings) to the hit (3.5b's first): the frame slides and smears;
4 1.4's last drawings: a close-up of the robot's visor, its tick, after his line (not inside it);
5 3.4's last drawings: the robot's visor, close: "99%" ... "98%";
6 secondary animation: the desk plant sways; the robot's antenna wobbles after it stops.
Shot lengths do not change (the mix and its speech check stay as v23). Opt-in through install()."""
import math
import numpy as np
import importlib
import cs_scene1 as s1

# shot -> (pivot in the frame, zoom at the end)
PUSH = {"1.4": ((397, 300), 1.10), "3.4": ((270, 520), 1.08), "6.5": ((300, 390), 1.10)}
# shot -> drawings with a hit (the shake decays over 4 drawings)
HITS = {"1.1": [7], "3.5b": [2], "1.2": [40], "3.4b": [3]}
SHAKE_A = {}                                                # shot -> the shake's first amplitude (px)
WHIP_OUT, WHIP_IN = ("3.5", 3), ("3.5b", 2)                 # the last 3 drawings of 3.5, the first 2 of 3.5b
WHIPPX, WHIP_IN_ON = [60.0], [True]
CU14 = (44, 49)                                             # 1.4 drawings drawn as the visor close-up
CU34 = 6                                                    # 3.4's last drawings: the robot's verdict
N = {}
ORIG = {}
VISOR14 = (243.0, 495.0)
POP14 = [False]


def _ease(u):
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


def _shake(sh, d):
    for h in HITS.get(sh, []):
        k = d - h
        if 0 <= k < 5:
            a = SHAKE_A.get(sh, 9.0) * (0.55 ** k)
            return (a * (1 if k % 2 == 0 else -1), a * 0.5 * (1 if k % 3 == 0 else -1))
    return None


def _blur(c, px, direction):
    """A horizontal smear of the drawn frame by px pixels (device), and a shift: the whip."""
    sf = c.get_target(); sf.flush()
    w, h, st = sf.get_width(), sf.get_height(), sf.get_stride()
    a = np.ndarray((h, st // 4, 4), np.uint8, sf.get_data())[:, :w].astype(np.float32)
    n = max(2, int(px))
    acc = np.zeros_like(a)
    for i in range(n):
        acc += np.roll(a, direction * i, axis=1)
    acc /= n
    a2 = np.roll(acc, direction * n // 2, axis=1)
    np.ndarray((h, st // 4, 4), np.uint8, sf.get_data())[:, :w] = a2.clip(0, 255).astype(np.uint8)
    sf.mark_dirty()


def wrap(sh, fn):
    def f(k, d):
        c = k.c
        n = N[sh]
        c.save()
        z = 1.0
        cu = (sh == "1.4" and CU14[0] <= d < CU14[1]) or (sh == "3.4" and d >= n - CU34)
        if sh in PUSH and not cu:
            (px, py), zz = PUSH[sh]
            z = 1.0 + (zz - 1.0) * _ease(d / float(max(1, n - 1)))
            c.translate(px, py); c.scale(z, z); c.translate(-px, -py)
        s = _shake(sh, d)
        if s:
            c.translate(270, 480); c.scale(1.04, 1.04); c.translate(-270, -480)
            c.translate(*s)
        try:
            if sh == "1.4" and CU14[0] <= d < CU14[1]:
                visor_cu(k, d, "tick")
            elif sh == "3.4" and d >= n - CU34:
                visor_cu(k, d - (n - CU34), "pct")
            else:
                fn(k, d)
        finally:
            c.restore()
        ds = c.get_target().get_device_scale()[0]
        if sh == WHIP_OUT[0] and d >= n - WHIP_OUT[1]:
            u = (d - (n - WHIP_OUT[1]) + 1) / float(WHIP_OUT[1])
            _blur(c, WHIPPX[0] * u * ds, -1)
        if sh == WHIP_IN[0] and d < WHIP_IN[1] and WHIP_IN_ON[0]:
            _blur(c, WHIPPX[0] * (1 - d / float(WHIP_IN[1])) * ds, -1)
    return f


VC = [(300.0, 392.0, 138.0, 128.0)]                                                 # the visor in the close-up (measured)


def visor_cu(k, d, kind):
    """The robot's head, close: 1.4's frame drawn 3.4 x about its visor. v26: anything put on the visor is clipped to
    the visor's own patch (captured as 1.4 draws it), a smooth ellipse 6 % inside it with no outline: no second
    contour, no overflow, the head's shape the same in every drawing."""
    import cs_props as cp
    import cs_v14 as V
    c = k.c
    sx, sy = VISOR14
    Z = 3.4
    got = []
    oe = V.ellipse

    def ell(k_, x, y, rx, ry, col, seed=0, *a, **kw):
        if seed == 990:
            got.append((k_.c.get_matrix(), x, y, rx, ry))
        return oe(k_, x, y, rx, ry, col, seed, *a, **kw)
    import cs_v14c as VC_
    oe2 = VC_.ellipse
    V.ellipse = VC_.ellipse = ell
    c.save(); c.translate(270, 470); c.scale(Z, Z); c.translate(-sx, -sy)
    try:
        ORIG["1.4"](k, 44 if kind == "tick" else 0)
    finally:
        V.ellipse, VC_.ellipse = oe, oe2
        c.restore()
    if not got or (kind == "tick" and not POP14[0]):
        return
    m, x, y, rx, ry = got[-1]
    c.save(); c.set_matrix(m)
    c.save(); c.translate(x, y); c.scale(rx * 0.94, ry * 0.94); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
    c.clip()
    c.set_source_rgb(0.06, 0.08, 0.12); c.paint()
    c.translate(x, y)
    if kind == "tick":
        sc = (0.0, 1.10, 1.0, 1.0, 1.0)[min(d - CU14[0], 4)]
        if sc:
            c.scale(sc, sc)
            c.set_source_rgba(*cp.GRN, 0.25); c.arc(0, 0, 0.75 * ry, 0, 2 * math.pi); c.fill()
            c.set_source_rgb(*cp.GRN); c.set_line_width(0.16 * ry); c.set_line_cap(1); c.set_line_join(1)
            c.move_to(-0.45 * ry, 0); c.line_to(-0.12 * ry, 0.33 * ry); c.line_to(0.50 * ry, -0.38 * ry); c.stroke()
    else:
        txt = ("99%", "99%", "...", "...", "98%", "98%")[min(d, 5)]
        cp.T(c, txt, 0, 0.26 * ry, 0.70 * ry, col=(0.55, 0.85, 1.0))
    c.restore()


def plant_sway():
    import cs_os20 as g20
    import cs_v19
    base = g20.plant

    def plant(k, side, dx=0):
        t = s1.CUR_T[0] if hasattr(s1, "CUR_T") else 0.0
        c = k.c
        a = 0.025 * math.sin(2 * math.pi * PH[0] / 30.0)
        px = 20 if side == "left" else 520
        c.save(); c.translate(px, 925); c.rotate(a if side == "left" else -a); c.translate(-px, -925)
        base(k, side, dx)
        c.restore()
    cs_v19.PIECES["plant"] = plant


PH = [0]


def install():
    if N:
        return
    for i in range(1, 7):
        m = importlib.import_module("cs_scene%d" % i)
        out = []
        for sh, nd, fn in m.SHOTS:
            N[sh] = nd
            ORIG[sh] = fn
            if sh in PUSH or sh in HITS or sh in (WHIP_OUT[0], WHIP_IN[0]):
                fn = wrap(sh, fn)
            out.append((sh, nd, fn))
        m.SHOTS[:] = out
    od = s1.draw

    def draw(fn, d):
        PH[0] = d
        return od(fn, d)
    s1.draw = draw
    plant_sway()
    import cs_film
    import cs_sfx as fx
    cs_film.FX[:] = cs_film.FX + [("1.4", CU14[0], fx.chime(), 0.10), ("3.4", N["3.4"] - CU34, fx.beep(880, 0.08), 0.08),
                                  ("3.4", N["3.4"] - CU34 + 4, fx.beep(620, 0.10), 0.08), ("3.5", N["3.5"] - 3, fx.whoosh(0.3), 0.18)]
