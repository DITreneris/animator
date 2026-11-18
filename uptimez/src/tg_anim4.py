"""ANIMATION v4 of "Raises for Everyone" (18 Nov): the reframe and camera polish, on top of v3 (tg_anim3.py, unchanged).
The v3 review found cut-off UPTIMEZ INC. signs and banner fragments at the frame edges, a second form insert that
repeated the cold open, and a camera locked off in every shot. v4 wraps each v3 panel in a screen-space move:
  s1   the wide table: a slow creep-in
  s2   the form insert: a push down to the empty Signature line (it sets up the ending)
  s3   Sofia and Pam: a slow creep
  s4   "Boy or girl? HA!": reframed (sign strip out of frame), then a creep
  s5   POLICY VIOLATION: reframed (sign corner out), then a creep (on top of v2's hit)
  s6   Don sweating: tighter (the cut UPTIMEZ sign out of frame), then a creep
  s7   "A raise for saying...": reframed (dark sign out of frame), then a creep
  s8a  "You failed.": a crash zoom on Don
  s8b  "She refused...": a slow push;  s8c the bite: a slow push
  s9   "walking policy violation": the logo sign brought fully into frame, then a creep
  s10a "HR. Back me up." and s10b ACCURATE: the standoff, handheld; signs brought fully into frame
  s11  the signing: reframed on the robot's hand and the pen, the banner and sign fragments out of frame
Speech bubbles are drawn in screen space, with their tails following the move, so they stay sharp and in the safe
area. The paper boil is calmer (half the wobble). The cold open, the reaction inserts, the signed form and the loop
tail stay locked, so the last frame is still frame 0.
Module protocol for engine_v / engine_hd: PANELS, DURATION, RAW_T, shake."""
import math
import cairo
import kit
from kit import Ctx, clamp, ease
import tg_anim3 as m3
import tg_anim as ta
import tg_sb as sb
import tg_set as ts

DURATION = m3.DURATION
RAW_T = 0.0
NAMES = ["cold", "s1", "s2", "s3", "s4", "s4b", "s5", "s6", "s7", "s8a", "s8b", "s8c", "s8d", "s9",
         "s10a", "s10b", "s10c", "s11", "s11b", "tail"]
assert len(NAMES) == len(m3.PANELS)

# ---------------------------------------------------------------- a calmer boil: half the wobble between drawings
_rr0, _re0 = kit.rough_rect_pts, kit.rough_ellipse_pts
_speech0 = sb.xb.speech
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
    dx = amp * (math.sin(t * 1.7) * 0.6 + math.sin(t * 5.3 + 1.0) * 0.3 + math.sin(t * 11.0 + 2.0) * 0.15)
    dy = amp * (math.sin(t * 1.3 + 0.5) * 0.6 + math.sin(t * 6.1) * 0.3 + math.sin(t * 13.0 + 1.0) * 0.12)
    return dx, dy, 0.004 * math.sin(t * 2.1)


SIG = (282.0, 650.0)                       # the Signature line of the form insert, on screen


def move(name, t, tl, d):
    """(cx, cy, z, dx, dy, rot): zoom z about the screen point (cx, cy), then a shift and a roll."""
    cx, cy, z, dx, dy, r = 270.0, 480.0, 1.0, 0.0, 0.0, 0.0
    e = ease(clamp(tl / d))
    if name == "s1":
        z = 1.0 + 0.05 * e
    elif name == "s2":
        cx, cy = SIG
        z = 1.0 + 0.30 * ease(clamp(tl / (d * 0.75)))
    elif name == "s3":
        cx, cy, z = 300.0, 560.0, 1.0 + 0.05 * e
    elif name == "s4":
        z = 1.04 + 0.04 * e
    elif name == "s5":
        cx, z = 330.0, 1.08 + 0.03 * e
    elif name == "s6":
        cx, cy, z = 270.0, 700.0, 1.10 + 0.05 * e
    elif name == "s7":
        cx, z = 240.0, 1.05 + 0.04 * e
    elif name == "s8a":
        cx, cy = 270.0, 150.0
        z = 1.12 + 0.12 * ease(clamp(tl / 0.16))
    elif name == "s8b":
        cx, cy, z = 230.0, 600.0, 1.0 + 0.06 * e
    elif name == "s8c":
        z = 1.0 + 0.04 * e
    elif name == "s9":
        cx, cy, z = 220.0, 560.0, 1.0 + 0.05 * e
    elif name == "s10a":
        dx, dy, r = handheld(t, 3.0)
        dx += 26; dy += 14
    elif name == "s10b":
        dx, dy, r = handheld(t, 3.0)
        cx, cy, z = 300.0, 700.0, 1.05
        dx += 32
    elif name == "s11":
        cx, cy, z = 300.0, 540.0, 1.0 + 0.04 * e              # a slow push on the robot's hand and the pen
        dx = 15
    return cx, cy, z, dx, dy, r


def _screen_speech(M0):
    """xb.speech in screen space: the anchors and the box centre go through the move, the box itself does not."""
    inv = cairo.Matrix(*M0); inv.invert()

    def sp(k, s, anchors, t, t0, *a, **kw):
        c = k.c
        Mc = c.get_matrix()

        def f(p):
            return inv.transform_point(*Mc.transform_point(*p))
        anchors = f(anchors) if isinstance(anchors, tuple) else [f(p) for p in anchors]
        if kw.get("at"):
            kw["at"] = f(kw["at"])
        c.save(); c.set_matrix(M0)
        try:
            _speech0(k, s, anchors, t, t0, *a, **kw)
        finally:
            c.restore()
    return sp


# set cheats, per shot, in world units: a sign the camera only half catches is moved fully in or fully out
CHEAT = {"s4": {"sign": (0, -30)}, "s5": {"sign": (-40, 0)}, "s10a": {"sign": (30, 0)}, "s10b": {"sign": (40, 0), "banner": (0, -30)}, "s7": {"sign": (40, 0)}, "s8a": {"sign": (0, -40)}, "s9": {"sign": (45, 0)},
         "s11": {"sign": (110, 0), "banner": (0, -70)}}
_sign0, _banner0 = ts.pt42.wall_sign, ts.banner


def _cheat(name):
    ch = CHEAT.get(name, {})
    if "sign" in ch:
        sx, sy = ch["sign"]
        ts.pt42.wall_sign = lambda k, x, y, *a, **kw: _sign0(k, x + sx, y + sy, *a, **kw)
    if "banner" in ch:
        bx, by = ch["banner"]
        ts.banner = lambda k, x, y, *a, **kw: _banner0(k, x + bx, y + by, *a, **kw)


LOCKED = {"cold", "s4b", "s8d", "s10c", "s11b", "tail"}


def cam(name, t0, t1, fn):
    def panel(k, t, tl):
        m3.RAW_T = RAW_T
        if name in LOCKED:
            fn(k, t, tl)
            return
        cx, cy, z, dx, dy, r = move(name, t, tl, t1 - t0)
        c = k.c
        M0 = c.get_matrix()
        c.save()
        c.translate(cx + dx, cy + dy); c.rotate(r); c.scale(z, z); c.translate(-cx, -cy)
        kit.rough_rect_pts, kit.rough_ellipse_pts = _rr, _re
        sb.xb.speech = _screen_speech(M0)
        _cheat(name)
        try:
            fn(k, t, tl)
        finally:
            kit.rough_rect_pts, kit.rough_ellipse_pts = _rr0, _re0
            sb.xb.speech = _speech0
            ts.pt42.wall_sign, ts.banner = _sign0, _banner0
            c.restore()
    panel.__name__ = name
    return panel


def shake(t):
    return m3.shake(t)


PANELS = [(t0, t1, cam(n, t0, t1, fn)) for (t0, t1, fn), n in zip(m3.PANELS, NAMES)]
