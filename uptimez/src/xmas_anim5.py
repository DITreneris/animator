"""ANIMATION v5 of "Happy Compliance" (18 Nov): v4 (xmas_anim4.py, kept) after two cold mute viewers, who got the main
joke (HR censors the tree and Sofia, not the boss) but not the ending, and saw the cold open's bar only as "a sticker":
- cold open: the CENSORED bar now flies in and STOPS in front of Don's robe (0.35-0.50 s, hovering, "looking" at him),
  then turns away and slaps onto the bauble (THUNK at 0.68 s); his shaving foam is a big white fluffy cloud on his jaw
  (it read as "a napkin" or "blowing his nose");
- the ending, made visible: after "Human in the loop." Pam's gloved hand throws Sofia's censored bauble off screen
  (an insert, 24.9-25.5 s of v2's clock); it comes in at Don's head at the end of "Merry Christmas, Don.", then THUD;
- Don's legs at the THUD come up out of his robe (no red block: it read as "a box" or "the tree pot"), and his razor
  is a plain razor, bigger, without the foam blob (it read as "a limb with a mitt");
- the bar coming off the bauble before the alarm gets its own close-up (28.05-28.4 s), so the alarm has a cause.
Sound: sound_xmas5.py. Module protocol for engine_v / engine_hd: PANELS, DURATION, RAW_T, shake."""
import math
import kit
from kit import INK, ease, clamp, Ctx
import xmas_anim4 as M4
import xmas_anim3 as M3
import xmas_anim2 as A2
import xmas_set as xs
import xmas_sb_v2 as sb
import sofia_xmas as sx
import santa_robot as sr
import don_xmas as dx
import props_ss  # noqa: F401  (props.soft lives in props_ss)
import props_ss as props

PRE, TAIL = M3.PRE, M3.TAIL
DURATION = M3.DURATION
RAW_T = 0.0
WALL = kit.WALL

# ---------------------------------------------------------------- cold open: the bar stops at his robe, then turns
M3.T0, M3.T_HIT = 0.08, 0.68
T_ARR, T_TURN = 0.35, 0.50


def bar_flight(tl):
    stop = (M3.CHEST[0] + 64, M3.CHEST[1] - 14)
    if tl < T_ARR:                                     # in from the right edge, at his robe
        v = ease(clamp((tl - M3.T0) / (T_ARR - M3.T0)))
        return (900 + (stop[0] - 900) * v, stop[1]), 0.5 * (1 - v)
    if tl < T_TURN:                                    # it stops and "looks" at him
        w = (tl - T_ARR) / (T_TURN - T_ARR)
        return (stop[0] + 3 * math.sin(w * 18), stop[1] - 4 * math.sin(w * 9)), 0.12 * math.sin(w * 12)
    v = ease(clamp((tl - T_TURN) / (M3.T_HIT - T_TURN)))   # and turns away, onto the bauble
    return M3._bez(stop, (M3.CHEST[0] - 30, M3.CHEST[1] + 110), (M3.BALL[0], M3.BALL[1]), v), -0.7 * math.sin(math.pi * v)


M3.bar_flight = bar_flight

# ---------------------------------------------------------------- the foam: a big fluffy cloud on his jaw
FOAM = ((-62, 52, 15), (-44, 66, 18), (-22, 78, 17), (0, 84, 15), (20, 78, 12), (-56, 80, 12), (-36, 92, 13),
        (-12, 96, 12), (-70, 34, 10))


def foam(c, hx, hy, s=1.0):
    k0 = Ctx(c, 0)
    for i, (fx, fy, r) in enumerate(FOAM):
        kit.ellipse(k0, hx + fx * s, hy + fy * s, r * s, r * 0.9 * s, (1, 1, 1), 1300 + i, shadow=False, lw=1.3)
    c.set_source_rgba(0.75, 0.85, 0.95, 0.6)
    for fx, fy, r in FOAM[::2]:
        c.arc(hx + (fx - r * 0.3) * s, hy + (fy - r * 0.3) * s, r * 0.25 * s, 0, 2 * math.pi); c.fill()


HEAD0 = (314.2, 255.6)                                 # his head on screen at t = 0 (CAM1)
_first0 = M3._first


def _first(k, t, tl):
    _first0(k, t, tl)
    foam(k.c, *HEAD0)


M3._first = _first


# ---------------------------------------------------------------- the razor, plain and bigger
def razor_floor(k, hand, s=1.0, ang=-0.9, seed=540):
    t = A2.xa.ACT.get("t", 0.0)
    if not (A2.SHOT11[0] <= t < A2.SHOT11[1]):
        return A2._saved["razor"](k, hand, s, ang, seed)
    c = k.c
    hx, hy = hand
    s *= 1.45
    c.save(); c.translate(hx, hy); c.scale(s, s); c.rotate(ang)
    kit.rect(k, -4.5, -26, 9, 44, dx.RAZOR, seed, shadow=False, lw=1.8)                  # the handle
    c.set_source_rgb(*INK); c.set_line_width(1.0)
    for g in range(4):
        c.move_to(-3, -2 + g * 5); c.line_to(3, -2 + g * 5); c.stroke()
    kit.rect(k, -16, -36, 32, 10, (0.86, 0.88, 0.91), seed + 1, shadow=False, lw=1.8)    # the head, wide
    c.set_source_rgb(0.55, 0.58, 0.62); c.set_line_width(1.6)
    c.move_to(-13, -31); c.line_to(13, -31); c.stroke()                                  # the blade
    c.restore()


A2.razor_floor = razor_floor


# ---------------------------------------------------------------- his legs out of his robe
def feet_up(k, t):
    if 28.05 <= t < 28.4:                              # not over the bauble close-up
        return
    c = k.c
    a = t - M4.T_THUD
    pop = 1 - math.exp(-a * 14) * math.cos(a * 30)
    lift = 240 * min(1.0, max(0.0, pop))
    skin = (0.96, 0.80, 0.66)
    for j, (x, lean) in enumerate(((78, -0.38), (170, 0.30))):
        wob = 0.12 * math.exp(-a * 5) * math.sin(a * 22 + j)
        c.save(); c.translate(x, 1000 - lift); c.rotate(lean + wob)
        kit.cut(k, [(-22, 160), (22, 160), (17, 8), (-17, 8)], skin, shadow=False, lw=2.4)
        c.set_source_rgb(0.30, 0.22, 0.18); c.set_line_width(1.4)
        for h in range(6):
            c.move_to(-10 + (h % 3) * 8, 34 + h * 18); c.line_to(-6 + (h % 3) * 8, 26 + h * 18); c.stroke()
        kit.ellipse(k, 0, -4, 30, 20, (0.12, 0.16, 0.34), 900 + j, shadow=False, lw=2.6)
        kit.ellipse(k, 0, -6, 22, 13, (0.82, 0.80, 0.76), 902 + j, shadow=False, lw=1.6)
        c.restore()
        c.save(); c.translate(x, 1000 - lift); c.rotate(lean + wob)            # the robe's sleeve-like hem round each
        kit.cut(k, [(-30, 175), (30, 175), (26, 120), (-26, 120)], dx.ROBE, shadow=False, lw=2.2)
        c.restore()


M4.feet_up = feet_up


# ---------------------------------------------------------------- the inserts
def bauble(k, x, y, r, rot, barred=True, seed=0):
    c = k.c
    c.save(); c.translate(x, y); c.rotate(rot)
    sx.ornament(k, 0, 0, r, seed, col=sx.ORN_RED)
    if barred:
        sr.censor_bar(k, 0, 0, r * 3.0, r * 0.95, rot=0.08, seed=seed + 5, label=True)
    c.restore()


def throw_insert(k, t2):
    """Pam's gloved hand throws the censored bauble off to the right (v2 clock 24.9-25.5)."""
    c = k.c
    a = t2 - 24.9
    c.set_source_rgb(*WALL); c.paint()
    rel = 0.16
    sl = ease(clamp(a / rel))
    kit.cut(k, [(-40, 690), (150 + 60 * sl, 560 - 40 * sl), (190 + 60 * sl, 610 - 40 * sl), (-40, 790)],
            (0.36, 0.22, 0.52), shadow=False, lw=2.4)                                       # her purple sleeve
    hx, hy = 200 + 60 * sl, 570 - 40 * sl
    kit.ellipse(k, hx, hy, 34, 30, (0.97, 0.94, 0.90), 1400, shadow=False, lw=2.2)          # the glove
    if a < rel:
        bauble(k, hx + 30, hy - 26, 46, -0.2, seed=1410)
    else:
        v = ease(clamp((a - rel) / 0.34))
        bx, by = hx + 30 + (640 - hx) * v, hy - 26 - 180 * math.sin(math.pi * v * 0.8)
        c.set_source_rgba(0.1, 0.1, 0.1, 0.35); c.set_line_width(5); c.set_line_cap(1)
        for d in (-22, 0, 22):                                                               # speed lines
            c.move_to(bx - 40, by + d); c.line_to(bx - 130, by + d + 6); c.stroke()
        bauble(k, bx, by, 46, -0.2 + 9 * v, seed=1410)


def incoming(k, t2):
    """The bauble comes in at Don's head from the left (v2 clock 26.6-26.9)."""
    v = ease(clamp((t2 - 26.6) / 0.3))
    k.c.set_source_rgba(0.1, 0.1, 0.1, 0.3); k.c.set_line_width(5); k.c.set_line_cap(1)
    x, y = -70 + 285 * v, 300 - 35 * v
    for d in (-18, 0, 18):
        k.c.move_to(x - 30, y + d); k.c.line_to(x - 110, y + d - 4); k.c.stroke()
    bauble(k, x, y, 52, 6 * v, seed=1420)


def peel_insert(k, t2):
    """The bar slips off one bauble on the tree (v2 clock 28.05-28.4): the cause of the alarm."""
    c = k.c
    a = t2 - 28.05
    c.set_source_rgb(0.18, 0.42, 0.26); c.paint()                                            # needles, close
    c.set_source_rgb(0.12, 0.32, 0.20); c.set_line_width(6)
    for i in range(14):
        c.move_to(-20 + i * 45, 0); c.line_to(40 + i * 45, 960); c.stroke()
    sx.ornament(k, 270, 470, 110, 1430, col=sx.ORN_RED)
    v = ease(clamp(a / 0.28))
    c.save(); c.translate(270 - 30 * v, 470 + 330 * v * v); c.rotate(0.08 + 1.4 * v)
    sr.censor_bar(k, 0, 0, 330, 105, rot=0.0, seed=1431, label=True)
    c.restore()
    if a > 0.12:                                                                             # bare again: a glint
        g = min(1.0, (a - 0.12) / 0.1)
        c.set_source_rgba(1, 1, 1, 0.8 * g); c.arc(230, 420, 22, 0, 2 * math.pi); c.fill()


def extra(i, fn):
    def g(k, t, tl):
        t2 = t - PRE
        if i == 11 and 24.9 <= t2 < 25.5:
            return throw_insert(k, t2)
        if i == 13 and 28.05 <= t2 < 28.4:
            return peel_insert(k, t2)
        fn(k, t, tl)
        if i == 0:                                     # the foam follows him as he steps in
            x = 726 + (700 - 726) * ease(clamp(t2 / 0.35))
            foam(k.c, HEAD0[0] + (x - 726) * sb.CAM1[2], HEAD0[1])
        if i == 12 and t2 >= 26.6:
            incoming(k, t2)
    g.__name__ = getattr(fn, "__name__", "panel")
    return g


D2 = A2.DURATION
PANELS = ([(0.0, PRE, M3.cold)] +
          [(t0 + PRE, t1 + PRE, M4.cam(i, extra(i, M3.shifted(i, fn)))) for i, (t0, t1, fn) in enumerate(A2.PANELS)] +
          [(D2 + PRE, DURATION, M3.tail)])


def shake(t):
    return M3.shake(t)
