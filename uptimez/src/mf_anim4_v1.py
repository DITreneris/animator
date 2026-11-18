"""ANIMATION v4 of "Mandatory Fun" (18 Nov): the camera polish, on top of v3 (mf_anim3.py, unchanged).
The camera audit found 20 shots with good size variety, but every one locked off and front-on. v4 adds motivated
moves per beat, a handheld feel only in the two chaos shots, a punch-in inside the long yank shot, and a calmer
paper boil. Each move is a screen-space layer around the shot's own camera:
  s1  the robot's line: a slow creep-in (the training drones on)
  s3  Don's entrance: a whip-pan in from the right
  s4c the arrest flirt: a slow push
  s5  "Officer? I confess." and the sulk: a creep-in on the sulk
  s6b the red verdict: a slow push (on top of v2's hit)
  s7  "You can't arrest a cop!": handheld
  s8a the cuffs: a crash zoom
  s10 the clicks: a slow push
  s11 the exit and the yank: handheld, then a punch-in on Pam for "So... dinner?"
The cold open and the loop tail stay locked, so the last frame is still frame 0.
Module protocol for engine_v / engine_hd: PANELS, DURATION, RAW_T, shake."""
import math
import kit
from kit import Ctx, clamp, ease
import mf_anim3 as m3
import mf_animatic as an
import mf_sb as sb
import mf_yank as yk
import pam_mf as pm

DURATION = m3.DURATION
RAW_T = 0.0
NAMES = ["cold"] + [fn.__name__ for _, _, fn in an.PANELS] + ["rewind"]


# ---------------------------------------------------------------- a calmer boil: half the wobble between drawings
_rr0, _re0 = kit.rough_rect_pts, kit.rough_ellipse_pts
CALM = 0.5


def _mix(p0, p1):
    return [(a[0] + (b[0] - a[0]) * CALM, a[1] + (b[1] - a[1]) * CALM) for a, b in zip(p0, p1)]


def _rr(k, *a, **kw):
    p1 = _rr0(k, *a, **kw)
    return p1 if k.boil == 0 else _mix(_rr0(Ctx(k.c, 0), *a, **kw), p1)


def _re(k, *a, **kw):
    p1 = _re0(k, *a, **kw)
    return p1 if k.boil == 0 else _mix(_re0(Ctx(k.c, 0), *a, **kw), p1)


# ---------------------------------------------------------------- the moves
def handheld(t, amp=3.0):
    """A slow drift plus a light shake: two sines and a little noise, deterministic in t."""
    dx = amp * (math.sin(t * 1.7) * 0.6 + math.sin(t * 5.3 + 1.0) * 0.3 + math.sin(t * 11.0 + 2.0) * 0.15)
    dy = amp * (math.sin(t * 1.3 + 0.5) * 0.6 + math.sin(t * 6.1) * 0.3 + math.sin(t * 13.0 + 1.0) * 0.12)
    return dx, dy, 0.004 * math.sin(t * 2.1)


def pam_s11():
    """Pam's head on screen in the yank shot (where her bubble is anchored)."""
    return sb.scr(yk.CAM, sb.X["pam"], sb.SEAT + pm.HY - 30)


def move(name, t, tl, d):
    """(cx, cy, z, dx, dy, rot): zoom z about the screen point (cx, cy), then a shift and a roll."""
    cx, cy, z, dx, dy, r = 270.0, 480.0, 1.0, 0.0, 0.0, 0.0
    if name == "s1":
        z = 1.0 + 0.06 * ease(tl / d)
    elif name == "s3":
        e = ease(clamp(tl / 0.22))
        dx = 220 * (1 - e)
    elif name in ("s4c", "s10"):
        z = 1.0 + 0.05 * ease(tl / d)
    elif name == "s5":
        z = 1.0 + 0.08 * ease(clamp((tl - (d - 1.6)) / 1.6))
    elif name == "s6b":
        z = 1.0 + 0.05 * ease(tl / d)
    elif name == "s7":
        dx, dy, r = handheld(t, 3.0)
    elif name == "s8a":
        z = 1.0 + 0.16 * ease(clamp(tl / 0.16))
    elif name == "s11":
        dx, dy, r = handheld(t, 2.2)
        if tl >= 3.3:                                          # "So... dinner?": punch in on Pam
            cx, cy = pam_s11()
            cy += 60                                           # her face, a little under the bubble anchor
            z = 1.0 + 0.32 * ease(clamp((tl - 3.3) / 0.12))
            dx *= 0.5; dy *= 0.5
    return cx, cy, z, dx, dy, r


def cam(name, fn):
    def panel(k, t, tl):
        t0 = next(a for a, b, f in m3.PANELS if f is fn)
        t1 = next(b for a, b, f in m3.PANELS if f is fn)
        cx, cy, z, dx, dy, r = move(name, t, tl, t1 - t0)
        c = k.c
        c.save()
        c.translate(cx + dx, cy + dy); c.rotate(r); c.scale(z, z); c.translate(-cx, -cy)
        kit.rough_rect_pts, kit.rough_ellipse_pts = _rr, _re
        m3.RAW_T = RAW_T
        try:
            fn(k, t, tl)
        finally:
            kit.rough_rect_pts, kit.rough_ellipse_pts = _rr0, _re0
            c.restore()
    panel.__name__ = name
    return panel


def shake(t):
    return m3.shake(t)


PANELS = [(t0, t1, cam(n, fn)) for (t0, t1, fn), n in zip(m3.PANELS, NAMES)]
