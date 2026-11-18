"""ANIMATION v3 of "Happy Compliance" (18 Nov): the joke at 0:01 and a true loop. Wraps animation v2 (xmas_anim2.py,
kept and unchanged) with:
- a cold open of PRE s in front: Don in the doorway (v2's frame 0) beside a red bauble hanging on the door frame.
  0.10 s: a black CENSORED bar flies in from the right, straight at his open robe... swerves round him at the last
  moment and slaps onto the bauble (THUNK at 0.55 s). The episode's joke before a word: it censors the ornament, not
  the boss. The bauble stays barred while he says his line;
- v2 after it, PRE s later (voices, lips, blinks and camera punches keep v2's clock);
- a loop tail of TAIL s after v2's last drawing (the alarm starting again): back to the doorway, Don and the bauble
  bare again, exactly frame 0. The next violation the robot will not see is already in the door.
Sound: sound_xmas3.py (v2's mix PRE s later, the whoosh and the THUNK in front).
Module protocol for engine_v / engine_hd: PANELS, DURATION, RAW_T, shake."""
import math
import kit
from kit import Ctx, ease, clamp
import xmas_anim2 as A2
import xmas_anim as xa
import xmas_set as xs
import xmas_sb_v2 as sb
import sofia_xmas as sx
import santa_robot as sr

PRE, TAIL = 0.8, 0.4
DURATION = round(A2.DURATION + PRE + TAIL, 3)
RAW_T = 0.0
BALL = (612, xs.FLOOR_Y - 196, 15)                 # world: hanging on the left of the door frame, at his chest height
HOOK = (612, xs.FLOOR_Y - 252)
T0, T_HIT = 0.10, 0.55
CHEST = (700, xs.FLOOR_Y - 150)


def ball(k, barred, bar_xy=None, bar_rot=0.0):
    c = k.c
    bx, by, r = BALL
    c.set_source_rgb(0.75, 0.15, 0.17); c.set_line_width(1.6)
    c.move_to(*HOOK); c.line_to(bx, by - r - 4); c.stroke()
    sx.ornament(k, bx, by, r, 7, col=sx.ORN_RED)
    if barred:
        sr.censor_bar(k, bx, by, r * 3.0 * xs.BAR_SCALE, r * 0.95 * xs.BAR_SCALE, rot=0.08, seed=77, label=True)
    elif bar_xy is not None:
        sr.censor_bar(k, bar_xy[0], bar_xy[1], r * 3.0 * xs.BAR_SCALE, r * 0.95 * xs.BAR_SCALE, rot=bar_rot,
                      seed=77, label=True)


def _bez(p0, p1, p2, u):
    return ((1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * p1[0] + u * u * p2[0],
            (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * p1[1] + u * u * p2[1])


def bar_flight(tl):
    """The bar from off the right edge, at his chest, round him, onto the bauble."""
    u = clamp((tl - T0) / (T_HIT - T0))
    if u < 0.55:                                    # straight in at his robe
        v = ease(u / 0.55)
        p = (900 + (CHEST[0] + 60 - 900) * v, CHEST[1] - 10 + 10 * v)
        return p, 0.4 * (1 - v)
    v = (u - 0.55) / 0.45                            # the swerve: down in front of him and up onto the bauble
    p = _bez((CHEST[0] + 60, CHEST[1]), (CHEST[0] - 20, CHEST[1] + 120), (BALL[0], BALL[1]), ease(v))
    return p, -0.6 * math.sin(math.pi * v) + 0.08 * v


_P0 = A2.PANELS[0][2]


def _first(k, t, tl):
    """v2's first drawing (t = 0), as it was."""
    A2.RAW_T = 0.0
    _P0(k, 0.0, 0.0)


def _overlay(k, draw):
    c = k.c
    c.save(); xs.with_cam(c, sb.CAM1); draw(); c.restore()


def cold(k, t, tl):
    c = k.c
    sh = (0.0, 0.0)
    if T_HIT <= tl < T_HIT + 0.2:
        f = int((tl - T_HIT) * 30)
        sh = ((4, -3, 2, -1, 1, 0)[f % 6], (3, -4, 2, -1, 0, 0)[f % 6])
    c.save(); c.translate(*sh)
    _first(k, t, tl)
    if tl < T0:
        _overlay(k, lambda: ball(k, False))
    elif tl < T_HIT:
        p, rot = bar_flight(tl)
        _overlay(k, lambda: ball(k, False, p, rot))
    else:
        _overlay(k, lambda: ball(k, True))
        if tl < T_HIT + 0.18:                        # impact lines
            sx_, sy_ = xs.to_screen(sb.CAM1, BALL[0], BALL[1])
            c.set_source_rgb(*kit.INK); c.set_line_width(3); c.set_line_cap(1)
            for a in range(0, 360, 45):
                r0, r1 = 34, 52
                c.move_to(sx_ + r0 * math.cos(math.radians(a)), sy_ + r0 * math.sin(math.radians(a)))
                c.line_to(sx_ + r1 * math.cos(math.radians(a)), sy_ + r1 * math.sin(math.radians(a)))
                c.stroke()
    c.restore()


def shifted(i, fn):
    def g(k, t, tl):
        A2.RAW_T = RAW_T - PRE
        fn(k, max(0.0, t - PRE), tl)
        if i == 0:                                   # his line: the bauble stays barred beside him
            _overlay(k, lambda: ball(k, True))
    g.__name__ = getattr(fn, "__name__", "panel")
    return g


def tail(k, t, tl):
    """Frame 0, unboiled, with the engine's push undone."""
    c = k.c
    pe = 1 + 0.03 * (tl / TAIL)
    c.save(); c.translate(270, 480); c.scale(1 / pe, 1 / pe); c.translate(-270, -480)
    k0 = Ctx(c, 0)
    _first(k0, 0.0, 0.0)
    _overlay(k0, lambda: ball(k0, False))
    c.restore()


D2 = A2.DURATION
PANELS = ([(0.0, PRE, cold)] + [(t0 + PRE, t1 + PRE, shifted(i, fn)) for i, (t0, t1, fn) in enumerate(A2.PANELS)] +
          [(D2 + PRE, DURATION, tail)])


def shake(t):
    return xa.shake(t - PRE) if hasattr(xa, "shake") and PRE <= t < D2 + PRE else 0
