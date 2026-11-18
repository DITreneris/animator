"""ANIMATION v7 of "Happy Compliance" (18 Nov): v6 (xmas_anim6.py, kept) with Tomas's three notes:
- 0:05 "Eww.": the two bubbles sit in the gap between Sofia's and Pam's heads, each with a short straight tail to
  beside its speaker's mouth (the long curved tails ran through the emoji and over Sofia's cap); the emoji are small
  badges on the boxes' outer top corners;
- the throw comes after "Merry Christmas, Don." and the hit is on screen: a 0.25 s throw insert, then in Don's shot
  the bauble hits his head (BONK, stars), he stiffens and tips back out of the frame like a plank;
- the fall lands: in the robot's shot Don drops in flat on his back in front of it on the THUD, stars circling his
  head, the bauble rolling away; the robot does not notice him (it goes red only over the bar slipping off).
  The feet sticking up ("pretzels on the floor") are gone.
Sound: sound_xmas7.py. Module protocol for engine_v / engine_hd: PANELS, DURATION, RAW_T, shake."""
import math
import kit
from kit import INK, ease, clamp, Ctx
import xmas_anim6 as M6
import xmas_anim5 as M5
import xmas_anim4 as M4
import xmas_anim3 as M3
import xmas_anim2 as A2
import xmas_anim as xa
import xmas_set as xs
import xmas_sb_v2 as sb
import xmas_bubbles as xb
import don_xmas as dx

PRE, TAIL = M3.PRE, M3.TAIL
EXTRA_AT, EXTRA = 26.9, 0.9                           # v2 clock: a new 0.9 s beat after "Merry Christmas, Don."
DURATION = round(M3.DURATION + EXTRA, 3)
RAW_T = 0.0

M4.feet_up = lambda k, t: None                        # no more feet in the air
A2.V4["Eww."] = []                                    # drawn below instead


# ---------------------------------------------------------------- "Eww." x 2, between the heads
EWW = (dict(t0=3.62, at=(262, 250), tip=(196, 348), icon="roll", badge=(212, 228)),
       dict(t0=3.87, at=(290, 318), tip=(350, 336), icon="queasy", badge=(338, 296)))


def eww(k, t2):
    for e in EWW:
        if t2 >= e["t0"]:
            xb.speech(k, "Eww.", [e["tip"]], t2, e["t0"], size=30, at=e["at"])
            p = xb._pop(t2, e["t0"])
            A2._emoticon(k.c, e["icon"], e["badge"][0], e["badge"][1], 16 * p)


# ---------------------------------------------------------------- the new beat: the throw, the BONK, the plank
E_IN, E_BONK, E_TIP, E_TIPD = 0.25, 0.40, 0.45, 0.40        # local time in the new beat
HEAD10B = (270, 258)                                  # Don's head on screen in shot 10b


def stars(c, cx, cy, t, rx, ry=None):
    ry = ry or rx * 0.32
    for j in range(3):
        a = t * 7 + j * 2.09
        x, y = cx + rx * math.cos(a), cy + ry * math.sin(a)
        c.save(); c.translate(x, y); c.rotate(a)
        c.move_to(0, -11)
        for i in range(1, 10):
            r = 11 if i % 2 == 0 else 4.5
            c.line_to(r * math.sin(i * math.pi / 5), -r * math.cos(i * math.pi / 5))
        c.close_path(); c.set_source_rgb(1.0, 0.84, 0.22); c.fill_preserve()
        c.set_source_rgb(*INK); c.set_line_width(1.6); c.stroke()
        c.restore()


def beat(fn10b):
    """After "Merry Christmas, Don.": Pam's throw (insert), then in his shot (v2's last drawing of 10b, held) the
    bauble hits his head (BONK, stars) and he tips back out of the frame like a plank."""
    _don0 = xa._don

    def g(k, t, tl):
        te = t - (EXTRA_AT + PRE)
        if te < E_IN:
            return M5.throw_insert(k, 24.9 + te * 2.0)
        c = k.c
        if te >= E_TIP:
            u = ease(clamp((te - E_TIP) / E_TIPD))

            def tipped(kk, x, feet, *a, **kw):
                cc = kk.c
                cc.save(); cc.translate(x, feet + 280 * u * u); cc.rotate(-1.5 * u); cc.translate(-x, -feet)
                try:
                    return _don0(kk, x, feet, *a, **kw)
                finally:
                    cc.restore()
            xa._don = tipped
        try:
            fn10b(k, 26.88 + PRE, tl)
        finally:
            xa._don = _don0
        if te < E_BONK:                                # the bauble, fast, from the left
            v = ease((te - E_IN) / (E_BONK - E_IN))
            x, y = -60 + (HEAD10B[0] - 70 + 60) * v, HEAD10B[1] - 10
            c.set_source_rgba(0.1, 0.1, 0.1, 0.3); c.set_line_width(5); c.set_line_cap(1)
            for d in (-16, 0, 16):
                c.move_to(x - 30, y + d); c.line_to(x - 120, y + d); c.stroke()
            M6.bauble(k, x, y, 46, 8 * v, seed=1420)
        else:                                          # it bounces off; BONK; stars round where his head was
            v = (te - E_BONK) / 0.4
            M6.bauble(k, HEAD10B[0] - 70 - 160 * v, HEAD10B[1] - 10 - 260 * v + 300 * v * v, 46, -6 * v, seed=1420)
            xb.burst(k, "BONK", HEAD10B[0] - 110, HEAD10B[1] - 90, te, E_BONK, size=44, rot=-0.2)
            if te < E_TIP + 0.1:
                stars(c, HEAD10B[0], HEAD10B[1] - 110, te, 70)
    g.__name__ = "beat"
    return g


# ---------------------------------------------------------------- shot 11: he lands flat in front of the robot
T_LAND = 27.2
S_DON = 0.62
FEET_X = 482


def lying(k, t2):
    c = k.c
    drop = 0.0 if t2 >= T_LAND else (1 - ease(clamp((t2 - 26.9) / (T_LAND - 26.9)))) * 600
    bounce = 10 * math.exp(-(t2 - T_LAND) * 12) * abs(math.sin((t2 - T_LAND) * 30)) if t2 >= T_LAND else 0
    c.save(); xs.with_cam(c, sb.CAM11)
    px, py = FEET_X, xs.FEET - 40 * S_DON - drop - bounce
    c.save(); c.translate(px, py); c.rotate(-math.pi / 2); c.translate(-px, -py)
    dx.don(k, px, py, S_DON, "stand", "neutral", look=(0, -1))
    c.restore()
    head = (px - 300 * S_DON * 0.86, py)                  # roughly where his head lies, to the left
    if t2 >= T_LAND:                                      # the bauble rolls away from his head
        v = clamp((t2 - T_LAND) / 0.8)
        M6.bauble(k, head[0] - 30 - 70 * ease(v), xs.FEET - 14, 14, -8 * v, seed=1440)
    c.restore()
    if t2 >= T_LAND + 0.05:
        hx, hy = xs.to_screen(sb.CAM11, head[0], head[1] - 60)
        stars(c, hx, hy, t2, 46)


def s11_new(fn):
    def g(k, t, tl):
        t2 = t - PRE
        fn(k, t, tl)
        if t2 >= 26.9 and not (28.05 <= t2 < 28.4):
            lying(k, t2)
    g.__name__ = getattr(fn, "__name__", "panel")
    return g


def extra(i, fn):
    if i == 13:
        def g(k, t, tl):
            t2 = t - PRE
            if 28.05 <= t2 < 28.4:
                return M5.peel_insert(k, t2)
            return s11_new(fn)(k, t, tl)
        g.__name__ = getattr(fn, "__name__", "panel")
        return g

    def h(k, t, tl):
        t2 = t - PRE
        fn(k, t, tl)
        if i == 0:
            x = 726 + (700 - 726) * ease(clamp(t2 / 0.35))
            M5.foam(k.c, M5.HEAD0[0] + (x - 726) * sb.CAM1[2], M5.HEAD0[1])
        if i == 2:
            eww(k, t2)
    h.__name__ = getattr(fn, "__name__", "panel")
    return h


D2 = A2.DURATION


def later(fn, d):
    def g(k, t, tl):
        return fn(k, t - d, tl)
    g.__name__ = getattr(fn, "__name__", "panel")
    return g


_P = [(t0, t1, M4.cam(i, extra(i, M3.shifted(i, fn)))) for i, (t0, t1, fn) in enumerate(A2.PANELS)]
_P10B = M4.cam(12, extra(12, M3.shifted(12, A2.PANELS[12][2])))
PANELS = ([(0.0, PRE, M3.cold)] +
          [(t0 + PRE, t1 + PRE, f) for (t0, t1, f) in _P[:13]] +
          [(EXTRA_AT + PRE, EXTRA_AT + PRE + EXTRA, beat(_P10B))] +
          [(t0 + PRE + EXTRA, t1 + PRE + EXTRA, later(f, EXTRA)) for (t0, t1, f) in _P[13:]] +
          [(D2 + PRE + EXTRA, DURATION, M3.tail)])


def shake(t):
    return M3.shake(t)
