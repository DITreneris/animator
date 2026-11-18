"""ANIMATION v4 of "Happy Compliance" (18 Nov): v3 (xmas_anim3.py, kept and unchanged) with:
- the PARTY sign above the door shown whole over Don's head in the opening shot (v2 had taken it out of shot 1, where
  boxes once hid it), so also in the cold open and the loop tail (frame 0 is still the last frame); taken out of shot
  4a (0:06), where it was cut by the right edge;
- the THUD (0:28) made readable: Don's slippered feet shoot up from the bottom of the frame as he goes down off
  screen, wobble, and stay; his razor still skids in from his side (it read as "a leg with a slipper" on its own);
- a light camera, on v2's clock: a slow creep on Don's "Sorry. Getting ready for the ball.", "Nice balls..." and
  "Merry Christmas, Don.", a small punch-in on Sofia's "Get him." and a push on Pam's "Human in the loop.". v2's
  own punches (DETECTED, the slaps, the THUD) stay.
Sound: v3's (xmas_mix_v3.wav). Module protocol for engine_v / engine_hd: PANELS, DURATION, RAW_T, shake."""
import math
import kit
from kit import INK, ease, clamp
import xmas_anim3 as M3
import xmas_anim2 as A2
import don_xmas as dx

PRE, TAIL = M3.PRE, M3.TAIL
DURATION = M3.DURATION
RAW_T = 0.0
A2.NO_PARTY = ((5.2, 5.9), (6.7, 9.5), (13.4, 15.8), (19.8, 21.5), (25.5, 26.9))   # shot 1 shows it; 4a does not


def _u(t, t0, d):
    return clamp((t - t0) / d)


def move(i, t, tl, d):
    """(cx, cy, z) in 540 x 960 screen space, on v2's clock t."""
    e = ease(clamp(tl / d))
    if i == 0:                                            # "Sorry. Getting ready for the ball."
        return 270, 380, 1 + 0.04 * e
    if i == 3:                                            # 4a: a cut sign corner (top left) pushed out of frame
        return 540, 700, 1.12
    if i == 5:                                            # "Nice balls... I've got two for you."
        return 270, 330, 1 + 0.06 * e
    if i == 11:                                           # "Get him." / "Human in the loop."
        z = 1 + 0.05 * (1 - ease(_u(t, 22.1, 0.3))) * (t >= 21.95)
        z += 0.06 * ease(_u(t, 23.05, 1.4))
        return 380, 400, z
    if i == 12:                                           # "Merry Christmas, Don."
        return 270, 340, 1 + 0.05 * e
    return 270, 480, 1.0


T_THUD = 27.2


def feet_up(k, t):
    """Don, down behind the frame edge: his shins and slippers kicked up from the bottom left, soles to us."""
    c = k.c
    a = t - T_THUD
    pop = 1 - math.exp(-a * 14) * math.cos(a * 30)       # a springy shoot up, then a wobble that settles
    lift = 240 * min(1.0, max(0.0, pop))
    skin = (0.96, 0.80, 0.66)
    for j, (x, lean) in enumerate(((78, -0.38), (170, 0.30))):
        wob = 0.12 * math.exp(-a * 5) * math.sin(a * 22 + j)
        c.save(); c.translate(x, 1000 - lift); c.rotate(lean + wob)
        kit.cut(k, [(-22, 160), (22, 160), (17, 8), (-17, 8)], skin, shadow=False, lw=2.4)
        c.set_source_rgb(0.30, 0.22, 0.18); c.set_line_width(1.4)          # his hairy shins
        for h in range(6):
            c.move_to(-10 + (h % 3) * 8, 34 + h * 18); c.line_to(-6 + (h % 3) * 8, 26 + h * 18); c.stroke()
        kit.ellipse(k, 0, -4, 30, 20, (0.12, 0.16, 0.34), 900 + j, shadow=False, lw=2.6)   # the slipper
        kit.ellipse(k, 0, -6, 22, 13, (0.82, 0.80, 0.76), 902 + j, shadow=False, lw=1.6)    # its sole, to us
        c.restore()
    hem = 960 - max(0.0, lift - 150) * 0.5
    kit.cut(k, [(10, 990), (240, 990), (236, hem), (14, hem)], dx.BOXERS, shadow=False, lw=2.2)   # the boxers' edge


def cam(i, fn):
    def g(k, t, tl):
        t2 = t - PRE
        d = A2.PANELS[i][1] - A2.PANELS[i][0]
        cx, cy, z = move(i, t2, tl, d)
        c = k.c
        c.save(); c.translate(cx, cy); c.scale(z, z); c.translate(-cx, -cy)
        try:
            fn(k, t, tl)
        finally:
            c.restore()
        if i == 13 and t2 >= T_THUD:
            feet_up(k, t2)
    g.__name__ = getattr(fn, "__name__", "panel")
    return g


D2 = A2.DURATION
PANELS = ([(0.0, PRE, M3.cold)] +
          [(t0 + PRE, t1 + PRE, cam(i, M3.shifted(i, fn))) for i, (t0, t1, fn) in enumerate(A2.PANELS)] +
          [(D2 + PRE, DURATION, M3.tail)])


def shake(t):
    return M3.shake(t)
