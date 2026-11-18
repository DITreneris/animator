"""ANIMATION v10 of "Happy Compliance" (18 Nov): v9 (xmas_anim9.py, kept) after Tomas's /grill-me picks, same length.

- the loop closes with the bar itself: the CENSORED bar that dropped onto Don stays stuck across his chest as he gets up,
  then peels off while he shuffles left and whips out of the frame to the left; the cold open's bar comes in from the
  right (one continuous leftward flight) and slaps onto the door bauble. The bar now has an origin;
- shot 7 ("INAPPROPRIATE BALLS DETECTED."): the robot's pointing arm is a scanner: a red beam sweeps Don head to toe
  twice, then a green tick pops beside him: checked, fine. So it censors the ornaments, not him;
- Pam's throw: a real wind-up (arm pulled back and held two frames), a smear on the whip, an arc trail on the bauble;
- the robot's talking mouth is a round "O" on its screen, not a square (read as a medical mask);
- everyone breathes: Don, Sofía and Pam, a slow 1 % rise and fall about their feet (ten breaths per loop, so the last
  frame still is frame 0).
Sound: sound_xmas10.py (v8's mix + the scan's hum and tick, and the bar's whoosh off). Module protocol: PANELS, DURATION,
RAW_T, shake."""
import inspect
import math
import kit
from kit import ease, clamp
import xmas_anim9 as M9
import xmas_anim8 as M8
import xmas_anim7 as M7
import xmas_anim6 as M6
import xmas_anim5 as M5
import xmas_anim4 as M4
import xmas_anim3 as M3
import xmas_anim2 as A2
import xmas_set as xs
import xmas_sb_v2 as sb
import xmas_test_a as ta
import santa_robot as sr
import waiter_kit as w
import don_xmas as dx
import sofia_xmas as sxm
import pam_xmas as pm
import pam_xmas3 as pm3

PRE, BEAT, LAND, UP = M8.PRE, M8.BEAT, M8.LAND, M8.UP
DURATION = M9.DURATION
RAW_T = 0.0
CLOCK = {"t": 0.0}

# ---------------------------------------------------------------- breathing
BREATH_T = DURATION / 10                               # ten whole breaths per loop
BREATH_A = 0.010


def _breathing(fn, phase, still_until=-1.0):
    def g(k, x, feet, s=1.0, *a, **kw):
        if CLOCK["t"] < still_until:                    # shot 1: his foam beard is an overlay at a fixed spot
            return fn(k, x, feet, s, *a, **kw)
        v = BREATH_A * 0.5 * (1 - math.cos(2 * math.pi * CLOCK["t"] / BREATH_T + phase))
        c = k.c
        c.save(); c.translate(x, feet); c.scale(1 - v * 0.3, 1 + v); c.translate(-x, -feet)
        try:
            return fn(k, x, feet, s, *a, **kw)
        finally:
            c.restore()
    return g


dx.don = _breathing(dx.don, 0.0, still_until=PRE + A2.PANELS[0][1])
sxm.sofia = _breathing(sxm.sofia, 2.1)
pm.pam = _breathing(pm.pam, 4.0)
pm3.pam = _breathing(pm3.pam, 4.0)

# ---------------------------------------------------------------- the robot's round talking mouth
_src = inspect.getsource(w.screen_face)
_old = "            c.rectangle(-w / 2, 13, w, h); c.fill()"
assert _old in _src
_src = _src.replace(_old, "            c.save(); c.translate(0, 13 + h / 2); c.scale(w * 0.36, h / 2 + 1.5)\n"
                          "            c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()")
_ns = dict(w.__dict__)
exec(compile(_src, "screen_face_v10", "exec"), _ns)
w.screen_face = _ns["screen_face"]
_src = inspect.getsource(sr._screen_face_v2)
_old = "            c.rectangle(-6, 15, 14, 3 + 10 * talk); c.fill()"
assert _old in _src
_src = _src.replace(_old, "            c.save(); c.translate(1, 16 + 5 * talk); c.scale(5.5, 2.5 + 5 * talk)\n"
                          "            c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()")
_ns = dict(sr.__dict__)
exec(compile(_src, "screen_face_v2_v10", "exec"), _ns)
sr._screen_face_v2 = _ns["_screen_face_v2"]


# ---------------------------------------------------------------- shot 7: the scan and the tick
SCAN0, SCAN1, TICK = 13.85, 15.15, 15.2
ARM = (642, 572)                                        # world: the tip of the pointing arm
DON_TOP, DON_X, DON_L, DON_R = 415, 650, 588, 710


def scan7(fn):
    def g(k, t2, tl):
        fn(k, t2, tl)
        c = k.c
        if SCAN0 <= t2 < SCAN1:
            u = (t2 - SCAN0) / (SCAN1 - SCAN0)
            ph = (u * 2) % 1.0
            y = DON_TOP + (xs.FEET - DON_TOP) * (0.5 - 0.5 * math.cos(2 * math.pi * ph))
            c.save(); xs.with_cam(c, sb.CAM7)
            c.set_source_rgba(1.0, 0.22, 0.2, 0.22)
            c.move_to(*ARM); c.line_to(DON_L, y); c.line_to(DON_R, y); c.close_path(); c.fill()
            c.set_source_rgba(1.0, 0.25, 0.22, 0.9); c.set_line_width(3.2); c.set_line_cap(1)
            c.move_to(DON_L, y); c.line_to(DON_R, y); c.stroke()
            c.restore()
        if TICK <= t2:
            v = clamp((t2 - TICK) / 0.12)
            pop = 1 + 0.35 * math.sin(math.pi * v) if v < 1 else 1.0
            c.save(); xs.with_cam(c, sb.CAM7)
            cx, cy = 714, 505
            c.translate(cx, cy); c.scale(pop * v + 0.02, pop * v + 0.02)
            kit.ellipse(k, 0, 0, 30, 30, (0.22, 0.70, 0.36), 1700, shadow=False, lw=3)
            c.set_source_rgb(1, 1, 1); c.set_line_width(7); c.set_line_cap(1); c.set_line_join(1)
            c.move_to(-13, 1); c.line_to(-3, 12); c.line_to(15, -11); c.stroke()
            c.restore()
    g.__name__ = getattr(fn, "__name__", "panel")
    return g


# ---------------------------------------------------------------- Pam's throw, with a wind-up
SLEEVE = (0.36, 0.22, 0.52)


def _arm(k, hx, hy, alpha=1.0):
    c = k.c
    if alpha < 1:
        c.push_group()
    kit.cut(k, [(-40, 700), (hx - 46, hy - 26), (hx - 6, hy + 26), (-40, 810)], SLEEVE, shadow=False, lw=2.4)
    kit.ellipse(k, hx, hy, 34, 30, (0.97, 0.94, 0.90), 1400, shadow=False, lw=2.2)
    if alpha < 1:
        c.pop_group_to_source(); c.paint_with_alpha(alpha)


def throw10(k, te):
    """0-0.09 s pulled back and held; 0.09-0.13 the whip (smear); then the bauble flies off right on an arc."""
    c = k.c
    c.set_source_rgb(*M5.WALL); c.paint()
    back, fwd = (190, 420), (330, 600)
    if te < 0.09:
        j = 3 * math.sin(te * 90)                       # a tremble of effort
        _arm(k, back[0] + j, back[1])
        M6.bauble(k, back[0] + 22, back[1] - 30, 46, 0.3, seed=1410)
        c.set_source_rgba(0.1, 0.1, 0.1, 0.4); c.set_line_width(4); c.set_line_cap(1)
        for a_ in (-0.5, 0.0, 0.5):                     # effort ticks
            x0, y0 = back[0] - 40, back[1] - 80
            c.move_to(x0 + 18 * math.cos(a_ + 3.6), y0 + 18 * math.sin(a_ + 3.6))
            c.line_to(x0 + 38 * math.cos(a_ + 3.6), y0 + 38 * math.sin(a_ + 3.6)); c.stroke()
        return
    v = ease(clamp((te - 0.09) / 0.04))
    hx, hy = back[0] + (fwd[0] - back[0]) * v, back[1] + (fwd[1] - back[1]) * v
    for g_ in (0.25, 0.5, 0.75):                        # the smear of the whip
        if v > g_:
            _arm(k, back[0] + (fwd[0] - back[0]) * g_, back[1] + (fwd[1] - back[1]) * g_, 0.25)
    _arm(k, hx, hy)
    if te < 0.13:
        M6.bauble(k, hx + 26, hy - 28, 46, 0.3 - v, seed=1410)
        return
    f = clamp((te - 0.13) / 0.12)
    p0 = (fwd[0] + 26, fwd[1] - 28)
    pt = lambda q: (p0[0] + (660 - p0[0]) * q, p0[1] - 210 * math.sin(math.pi * q * 0.75))
    c.set_source_rgba(0.1, 0.1, 0.1, 0.35); c.set_line_width(4); c.set_line_cap(1)
    for i in range(8):                                  # the arc it has flown, dotted
        q = f * i / 8
        x, y = pt(q)
        c.arc(x, y, 4, 0, 2 * math.pi); c.fill()
    bx, by = pt(f)
    for d in (-20, 0, 20):
        c.move_to(bx - 42, by + d); c.line_to(bx - 120, by + d + 14); c.stroke()
    M6.bauble(k, bx, by, 46, 0.3 + 8 * f, seed=1410)


def beat10(fn):
    def g(k, t, tl):
        te = t - (M7.EXTRA_AT + PRE)
        if te < M7.E_IN:
            return throw10(k, te)
        return fn(k, t, tl)
    g.__name__ = "beat"
    return g


# ---------------------------------------------------------------- UP: the bar rides on Don, then leaves for the door
BAR_W = 14 * 3.0 * xs.BAR_SCALE * 1.5
BAR_H = 14 * 0.95 * xs.BAR_SCALE * 1.5
_BX, _BY, _BR = ta.ORN[2][0] + 40, M9.LAND_Y, 0.08 + 1.3          # where it lies on him (v9)
_PIV = (M8.FEET_X, xs.FEET - 40 * M8.S_DON)                         # his pivot, flat
T_OFF, T_OFFD = 0.62, 0.38                                           # local time in UP


def _on_don(ang, dx_=0.0, bob=0.0):
    px = M8.FEET_X + dx_
    py = xs.FEET - 40 * M8.S_DON * (abs(ang) / (math.pi / 2)) - bob
    lx, ly = _BX - _PIV[0], _BY - _PIV[1]               # its offset from him while he lay flat (ang = -90 deg)
    r = ang + math.pi / 2
    cr, sr_ = math.cos(r), math.sin(r)
    return px + lx * cr - ly * sr_, py + lx * sr_ + ly * cr, _BR + r


_bar0 = sr.censor_bar


def _no_slip(k_, x, y, wd=60, ht=18, rot=0.0, label=True, seed=0):
    if seed == 1200:
        return None
    return _bar0(k_, x, y, wd, ht, rot=rot, label=label, seed=seed)


def up10(fn11):
    def g(k, t, tl):
        sb.sr.censor_bar = _no_slip
        try:
            M8.s11_frozen(fn11, 28.88)(k, t, tl)
        finally:
            sb.sr.censor_bar = _bar0
        te = t - (PRE + M8.D2 + BEAT + LAND)
        c = k.c
        if te < 0.5:
            ang = -math.pi / 2 * (1 - ease(te / 0.5))
            M8.don_at(k, ang)
            pos = _on_don(ang)
        else:
            wv = (te - 0.5) / 0.7
            ang, dxx, bob = 0.08 * math.sin(wv * 14), -260 * ease(wv), 6 * abs(math.sin(wv * 12))
            M8.don_at(k, ang, dx_=dxx, bob=bob)
            hx, hy = xs.to_screen(sb.CAM11, M8.FEET_X + dxx, xs.FEET - 300 * M8.S_DON - 30)
            M7.stars(c, hx, hy, te, 34)
            pos = _on_don(ang, dxx, bob)
        bx, by, br = pos
        c.save(); xs.with_cam(c, sb.CAM11)
        if te >= T_OFF:                                  # it peels up off his chest, then sails out left (to the door)
            pe = clamp((te - T_OFF) / 0.09)
            bx, by, br = bx - 10 * pe, by - 45 * ease(pe), br + 0.5 * pe   # a corner lifts, it comes away
            if te >= T_OFF + 0.09:
                f = clamp((te - T_OFF - 0.09) / (T_OFFD - 0.09))
                q = f * f
                bx, by, br = bx - 760 * q, by - 60 * math.sin(math.pi * f * 0.6), br + 0.6 * f
                c.set_source_rgba(0.1, 0.1, 0.1, 0.3); c.set_line_width(4); c.set_line_cap(1)
                for d in (-14, 14):                          # it leaves a trail back to him
                    c.move_to(bx + 55, by + d); c.line_to(bx + 55 + 200 * f, by + d + 30 * f); c.stroke()
        _bar0(k, bx, by, BAR_W, BAR_H, rot=br, seed=1200)
        c.restore()
    g.__name__ = "up"
    return g


# ---------------------------------------------------------------- the panels
def _clocked(fn, frozen=None):
    def g(k, t, tl):
        CLOCK["t"] = t if frozen is None else frozen
        return fn(k, t, tl)
    g.__name__ = getattr(fn, "__name__", "panel")
    return g


_P = list(M9.PANELS)
_P[9] = (_P[9][0], _P[9][1], M4.cam(8, M7.extra(8, M3.shifted(8, scan7(A2.PANELS[8][2])))))
_P[14] = (_P[14][0], _P[14][1], beat10(_P[14][2]))
_P[17] = (_P[17][0], _P[17][1], up10(M8._f11))
assert [getattr(f, "__name__", "") for _, _, f in _P[14:18]] == ["beat", "land", "s11", "up"], \
    [getattr(f, "__name__", "") for _, _, f in _P]
PANELS = [(t0, t1, _clocked(f, 0.0 if i == len(_P) - 1 else None)) for i, (t0, t1, f) in enumerate(_P)]  # tail = frame 0


def shake(t):
    return M9.shake(t)
