"""ANIMATION v9 of "Happy Compliance" (xmas_anim8.py = v8, kept), same length and timing as v8.

v8 -> v9 (user + two cold viewers: the green striped close-up at 30.6 s could not be placed):
- the peel close-up is gone; instead the robot's shot pushes in on the bare-again bauble next to the robot's
  face, the bar visibly drops off it (in place, on the tree), the robot's eyes go red, and the camera eases back
  out to the wide shot before Don gets up. One space, one action: the alarm now has its cause in the same frame.
- the bar in the push is drawn bigger and falls further, so it reads on a phone.
"""
import math
import kit
from kit import ease, clamp
import xmas_anim8 as M8
import xmas_sb_v2 as sb
import xmas_set as xs
import xmas_test_a as ta
import xmas_bubbles as xb

PRE, BEAT, LAND = M8.PRE, M8.BEAT, M8.LAND
DURATION = M8.DURATION
RAW_T = 0.0

CAM0 = M8.sb.CAM11                       # v8's wide robot shot
PUSH = (362, 522, 2.1)                  # the gold bauble whose bar slips + the robot's face
T_IN, T_IN1 = 27.84, 27.98              # v2 clock: push in as the line ends
T_SLIP = 27.98                           # the bar lets go (lands on Don at 28.30, alarm 28.35)
LAND_Y = xs.FEET - 40                    # Don's chest, lying
T_OUT, T_OUT1 = 28.58, 28.88             # and back out before he gets up


def cam_at(t2):
    if t2 < T_IN:
        v = 0.0
    elif t2 < T_IN1:
        v = ease(clamp((t2 - T_IN) / (T_IN1 - T_IN)))
    elif t2 < T_OUT:
        v = 1.0
    else:
        v = 1 - ease(clamp((t2 - T_OUT) / (T_OUT1 - T_OUT)))
    return tuple(a + (b - a) * v for a, b in zip(CAM0, PUSH))


_bar0 = None


def s11_push(fn11):
    """Shot 11 at v2's own time, Don lying, no peel insert; camera pushes in on the bauble as its bar drops."""
    def g(k, t, tl):
        t2 = t - PRE - BEAT - LAND
        cam = cam_at(t2)
        sb.CAM11 = cam
        bar_mod = sb.sr
        bar0 = bar_mod.censor_bar

        def bigger(k_, x, y, w, h, rot=0.0, seed=0, **kw):
            if seed == 1200:                     # the one that slips: drawn by us, on top, below
                return None
            return bar0(k_, x, y, w, h, rot=rot, seed=seed, **kw)
        bar_mod.censor_bar = bigger
        try:
            M8.s11_frozen(fn11, t2)(k, t, tl)
            M8.lying(k, (t2 - 26.9) + LAND - 0.3)
            ox, oy = ta.ORN[2]
            if t2 < T_SLIP:                      # still on the bauble (drawn on top so it can't hide)
                bx, by, br = ox, oy, 0.08
            else:                                # slides off, drops in front of everything onto Don's chest
                p = clamp((t2 - T_SLIP) / 0.32)
                q = p * p
                bx, by, br = ox + 40 * p, oy + (LAND_Y - oy) * q, 0.08 + 1.3 * p
                if p >= 1:                       # a little bounce on landing
                    bt = t2 - T_SLIP - 0.32
                    by -= 14 * max(0.0, 1 - bt / 0.18) * abs(math.sin(bt * 30))
            c = k.c
            c.save(); xs.with_cam(c, cam)
            bar0(k, bx, by, 14 * 3.0 * xs.BAR_SCALE * 1.5, 14 * 0.95 * xs.BAR_SCALE * 1.5, rot=br, seed=1200)
            if T_SLIP <= t2 < T_SLIP + 0.32:     # speed lines above it
                c.set_source_rgba(0.1, 0.1, 0.1, 0.35); c.set_line_width(3); c.set_line_cap(1)
                for d in (-18, 0, 18):
                    c.move_to(bx + d, by - 30); c.line_to(bx + d - 4, by - 75); c.stroke()
            c.restore()
            if t2 >= T_SLIP + 0.08:              # bare again: a glint on the gold bauble
                gx, gy = xs.to_screen(cam, ox - 5, oy - 6)
                gv = min(1.0, (t2 - T_SLIP - 0.08) / 0.1)
                k.c.set_source_rgba(1, 1, 1, 0.85 * gv)
                k.c.arc(gx, gy, 5 * cam[2], 0, 6.2832); k.c.fill()
        finally:
            bar_mod.censor_bar = bar0
            sb.CAM11 = CAM0
    g.__name__ = "s11"
    return g


PANELS = list(M8.PANELS)
for _j, (_t0, _t1, _f) in enumerate(PANELS):
    if getattr(_f, "__name__", "") == "s11":
        PANELS[_j] = (_t0, _t1, s11_push(M8._f11))
assert any(getattr(f, "__name__", "") == "s11" and f.__code__.co_filename.endswith("xmas_anim9.py")
           for _, _, f in PANELS)


def shake(t):
    return M8.shake(t)
