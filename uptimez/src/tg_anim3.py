"""ANIMATION v3 of "Raises for Everyone" (18 Nov): the joke at frame 0 and a true loop. Wraps animation v2
(tg_anim.py, kept and unchanged) with:
- a cold open: the first CUT s of shot 1 become the form insert. The form, I AM HAPPY WITH MY CURRENT SALARY, is on
  the table at frame 0; Don's hand slaps it at 0.1 s (on v2's own slap sound) while his voice says "Raises for
  everyone! Sign here." The contradiction is the joke, readable on mute. Then shot 1 continues on Don, as in v2;
- a loop tail (LOOP s) after the stamped form: a fresh, blank form drops onto the stack and covers it; the last
  drawing is frame 0, ready for the next slap.
Timing and voices are v2's (the cold open plays over shot 1's first CUT s); the film is LOOP s longer.
Module protocol for engine_v / engine_hd: PANELS, DURATION, RAW_T, shake."""
import math
import kit
from kit import Ctx, INK, clamp, ease
import brand
import tg_anim as ta
import tg_sb as sb
import tg_set as ts
import don_tg as dt

CUT, LOOP = 1.25, 0.65
D0 = ta.DURATION
DURATION = round(D0 + LOOP, 3)
RAW_T = 0.0
SHIRT = (0.96, 0.96, 0.94)


def form_only(k, dx=0.0, dy=0.0, rot=0.0, seed=1300):
    """The blank form of shot 2 (no wood), offset and turned: for the drop in the loop tail."""
    c = k.c
    c.save(); c.translate(270 + dx, 470 + dy); c.rotate(-0.06 + rot)
    kit.rect(k, -200, -270, 400, 540, (1, 1, 1), seed, lw=3)
    c.set_source_rgb(*brand.GREEN); c.rectangle(-196, -266, 392, 52); c.fill()
    brand.mark(c, -184, -258, 36, zzz=False)
    kit.text(k, "UPTIMEZ INC.  ·  HR", 20, -232, 22, (1, 1, 1), font="Inter", bold=True)
    kit.text(k, "EMPLOYEE SATISFACTION", 0, -150, 26, INK, font="Inter", bold=True)
    kit.text(k, "FORM 11-B  ·  THANKSGIVING", 0, -118, 14, (0.45, 0.45, 0.45), font="Inter")
    for i, ln in enumerate(("I AM HAPPY WITH", "MY CURRENT", "SALARY.")):
        kit.text(k, ln, 0, -40 + i * 46, 38, INK, font="Inter", bold=True)
    c.set_source_rgb(*INK); c.set_line_width(2.4)
    c.move_to(-140, 196); c.line_to(140, 196); c.stroke()
    kit.text(k, "Signature", -100, 222, 14, (0.45, 0.45, 0.45), font="Inter")
    c.restore()


def hand(k, x, y):
    """Don's forearm in his white shirt sleeve, coming down from the top of the frame, the palm flat at (x, y)."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(1.7, 1.7); c.translate(-x, -y)
    kit.cut(k, [(x - 34, -40), (x + 46, -40), (x + 40, y - 70), (x - 30, y - 70)], SHIRT, lw=2.6)
    kit.rect(k, x - 34, y - 86, 76, 26, (1, 1, 1), 1401, lw=2.4)                       # the cuff
    kit.ellipse(k, x + 4, y - 20, 58, 50, dt.SKIN, 1402, lw=2.6)                       # the palm, flat
    for i, fx in enumerate((-36, -14, 10, 32)):                                         # fingers, spread
        kit.ellipse(k, x + fx, y + 28 - abs(fx) * 0.25, 11, 22, dt.SKIN, 1403 + i, shadow=False, lw=2.2)
    kit.ellipse(k, x + 58, y - 26, 20, 11, dt.SKIN, 1408, shadow=False, lw=2.2)        # the thumb
    c.restore()


def cold(k, t, tl):
    """0..CUT: the form; the hand slaps it at 0.1 s and lifts off by 0.7 s."""
    c = k.c
    pe = 1 + 0.03 * (tl / CUT)                                  # no engine push on this insert
    c.save(); c.translate(270, 480); c.scale(1 / pe, 1 / pe); c.translate(-270, -480)
    sb.form_insert(k, 0.0)
    if 0.0 < tl < 0.75:
        if tl < 0.10:
            y = -60 + (300 + 60) * ease(tl / 0.10)            # comes down fast
        elif tl < 0.45:
            y = 300                                           # pressed flat
        else:
            y = 300 - 420 * ease((tl - 0.45) / 0.30)          # lifts off
        hand(k, 300, y)
        if 0.10 <= tl < 0.42:
            sb.slap_lines(k, 300, 300, 5.0)
    c.restore()
    ta.vignette(c) if hasattr(ta, "vignette") else None


def tail(k, t, tl):
    """After the stamp: a blank form drops onto the stack; the last drawings are frame 0."""
    c = k.c
    pe = 1 + 0.03 * (tl / LOOP)
    if tl >= 0.42:                                            # frame 0, on unboiled paper
        c.save(); c.translate(270, 480); c.scale(1 / pe, 1 / pe); c.translate(-270, -480)
        cold(Ctx(c, 0), 0.0, 0.0)
        c.restore()
        return
    last = ta.PANELS[-1]
    last[2](k, D0 - 0.02, last[1] - last[0] - 0.02)          # the stamped form, as v2 ends
    e = ease(clamp(tl / 0.30))
    form_only(k, dx=40 * (1 - e), dy=-1100 * (1 - e), rot=0.25 * (1 - e) + 0.02 * math.sin(tl * 40) * (1 - e))


def from_v2(fn, t0):
    def panel(k, t, tl):
        ta.RAW_T = RAW_T
        fn(k, t, tl + t0)
    panel.__name__ = "s1_rest"
    return panel


def shake(t):
    return ta.shake(t) if t < D0 else 0


_p0 = ta.PANELS[0]
PANELS = ([(0.0, CUT, cold), (CUT, _p0[1], from_v2(_p0[2], CUT))] + list(ta.PANELS[1:]) +
          [(D0, DURATION, tail)])
