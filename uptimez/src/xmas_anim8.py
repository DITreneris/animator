"""ANIMATION v8 of "Happy Compliance" (18 Nov): v7 (xmas_anim7.py, kept) after Tomas's notes:
- no "Eww." bubbles or emoji (the voices stay);
- the door gets its decoration: a fir garland along the top of the door frame, the red bauble hanging from its end;
- clean colours: no brown vignette, no warm glows (and the build encodes BT.709 properly);
- the fall, then the line: a new 0.7 s beat in the robot's shot (LAND) where Don drops in flat and lands on the THUD;
  only then does the robot say "Happy compliance!" over him (v2's own THUD in shot 11 is taken out);
- the loop: after the alarm, a new 1.2 s beat (UP): dazed Don gets up and shuffles off left, towards the door; the
  tail then shows him back in the doorway, frame 0.
Sound: sound_xmas8.py. Module protocol for engine_v / engine_hd: PANELS, DURATION, RAW_T, shake."""
import math
import kit
from kit import INK, ease, clamp, Ctx
import xmas_anim7 as M7
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
AT, BEAT, LAND, UP = 26.9, M7.EXTRA, 0.7, 1.2
D2 = A2.DURATION
DURATION = round(PRE + D2 + BEAT + LAND + UP + TAIL, 3)
RAW_T = 0.0

# ---------------------------------------------------------------- no Eww bubbles, clean colours
A2.V4["Eww."] = []
M7.eww = lambda k, t2: None
xa.vignette = lambda c: None
xa._glow = lambda *a, **kw: None
_punch0 = xa.punch


def punch(t):                                         # v2's THUD shake (27.2) goes: the THUD is now in LAND
    if 27.2 <= t < 27.45:
        return 1.0, 0.0, 0.0
    return _punch0(t)


xa.punch = punch

# ---------------------------------------------------------------- the fir garland over the door
_door2 = A2.door2
GREEN, GREEN_D = (0.20, 0.50, 0.30), (0.12, 0.36, 0.20)


def garland(k):
    c = k.c
    x0, x1, y = 596, 772, xs.FLOOR_Y - 252
    pts = [(x0 + (x1 - x0) * i / 22, y + 9 * math.sin(math.pi * ((i / 22 * 2) % 1.0))) for i in range(23)]
    for j, (x, yy) in enumerate(pts):                 # tufts of needles along a sagging rope
        for a in (-1.0, -0.4, 0.3, 0.9):
            c.save(); c.translate(x, yy); c.rotate(a + 0.2 * math.sin(j * 1.7))
            c.move_to(0, 0); c.line_to(14, -3); c.line_to(14, 3); c.close_path()
            c.set_source_rgb(*(GREEN if (j + int(a * 10)) % 2 else GREEN_D)); c.fill()
            c.restore()
    for j in range(2, 22, 5):                         # a few red berries
        x, yy = pts[j]
        kit.ellipse(k, x, yy + 4, 3.2, 3.2, (0.80, 0.14, 0.16), 1500 + j, shadow=False, lw=1.0)


def door2(k, x=None, open_amt=0.0):
    out = _door2(k, x, open_amt)
    garland(k)
    return out


A2.door2 = door2
M3.HOOK = (604, xs.FLOOR_Y - 250)                     # the bauble now hangs from the garland's left end
M3.BALL = (604, xs.FLOOR_Y - 196, 15)


# ---------------------------------------------------------------- Don lying, getting up, going
# Don at his true size (v7 drew him at 0.62 to fit him lying in the close robot shot, which made the robot a giant);
# the robot's shot is widened instead, for the whole of shot 11 and the new beats, so both are at the scale of the
# rest of the film.
S_DON, FEET_X = 1.0, 560
sb.CAM11 = (410, 616, 1.3)


def don_at(k, ang, dx_=0.0, lift=0.0, bob=0.0):
    """Don in the robot's shot, rotated about his feet by ang (-pi/2 = flat on his back, head to the left)."""
    c = k.c
    c.save(); xs.with_cam(c, sb.CAM11)
    px, py = FEET_X + dx_, xs.FEET - 40 * S_DON * (abs(ang) / (math.pi / 2)) - lift - bob
    c.save(); c.translate(px, py); c.rotate(ang); c.translate(-px, -py)
    dx.don(k, px, py, S_DON, "stand", "neutral", look=(-0.6, 0.2))
    c.restore(); c.restore()
    return px, py


def lying(k, t_since_land, drop=0.0):
    c = k.c
    bounce = 10 * math.exp(-t_since_land * 12) * abs(math.sin(t_since_land * 30)) if t_since_land >= 0 else 0
    px, py = don_at(k, -math.pi / 2, lift=drop + bounce)
    head = (px - 300 * S_DON * 0.86, py)
    if t_since_land >= 0:
        c.save(); xs.with_cam(c, sb.CAM11)
        v = clamp(t_since_land / 0.8)
        M6.bauble(k, head[0] - 30 - 70 * ease(v), xs.FEET - 14, 14, -8 * v, seed=1440)
        c.restore()
        hx, hy = xs.to_screen(sb.CAM11, head[0], head[1] - 60)
        M7.stars(c, hx, hy, t_since_land, 46)


_burst0 = xb.burst


def s11_frozen(fn11, t2):
    """Shot 11 drawn at v2 time t2, without v2's THUD burst."""
    def g(k, t, tl):
        xb.burst = lambda *a, **kw: None
        try:
            fn11(k, t2 + PRE, tl)
        finally:
            xb.burst = _burst0
    return g


def land_beat(fn11):
    """LAND: the robot, smiling (v2 shot 11 held at 26.9), Don drops in flat and lands on the THUD."""
    def g(k, t, tl):
        s11_frozen(fn11, 26.9)(k, t, tl)
        te = t - (AT + BEAT + PRE)
        tl0 = 0.3
        drop = (1 - ease(clamp(te / tl0))) * 600
        lying(k, te - tl0, drop if te < tl0 else 0.0)
        if te >= tl0:
            xb.burst(k, "THUD", 150, 640, te, tl0, size=48, rot=-0.15)
    g.__name__ = "land"
    return g


def s11_live(fn11):
    """Shot 11, v2's own time (shifted by BEAT + LAND), Don lying in front of the robot, no v2 THUD burst."""
    def g(k, t, tl):
        t2 = t - PRE - BEAT - LAND
        if 28.05 <= t2 < 28.4:
            return M5.peel_insert(k, t2)
        s11_frozen(fn11, t2)(k, t, tl)
        lying(k, (t2 - 26.9) + LAND - 0.3)
    g.__name__ = "s11"
    return g


def up_beat(fn11):
    """UP: the alarm (shot 11 held at 28.88); Don gets up, dazed, and shuffles off left towards the door."""
    def g(k, t, tl):
        s11_frozen(fn11, 28.88)(k, t, tl)
        te = t - (PRE + D2 + BEAT + LAND)
        c = k.c
        if te < 0.5:                                    # up, like a plank going the other way
            ang = -math.pi / 2 * (1 - ease(te / 0.5))
            don_at(k, ang)
            hx, hy = xs.to_screen(sb.CAM11, FEET_X - 300 * S_DON * 0.86 * math.cos(ang + math.pi / 2) * 0, xs.FEET - 260)
        else:                                           # and off to the left, wobbling
            w = (te - 0.5) / 0.7
            don_at(k, 0.08 * math.sin(w * 14), dx_=-260 * ease(w), bob=6 * abs(math.sin(w * 12)))
            hx, hy = xs.to_screen(sb.CAM11, FEET_X - 260 * ease(w), xs.FEET - 300 * S_DON - 30)
            M7.stars(c, hx, hy, te, 34)
    g.__name__ = "up"
    return g


# ---------------------------------------------------------------- the panels
_P = [(t0, t1, M4.cam(i, M7.extra(i, M3.shifted(i, fn)))) for i, (t0, t1, fn) in enumerate(A2.PANELS)]
_P10B = M4.cam(12, M7.extra(12, M3.shifted(12, A2.PANELS[12][2])))
_F11 = A2.PANELS[13][2]


def _f11(k, t, tl):                                     # v2's shot 11 at v2 time t - PRE (no extras, no feet)
    A2.RAW_T = t - PRE
    return _F11(k, t - PRE, tl)


T_BEAT = AT + PRE
T_LAND = T_BEAT + BEAT
T_11 = T_LAND + LAND
T_UP = PRE + D2 + BEAT + LAND
PANELS = ([(0.0, PRE, M3.cold)] +
          [(t0 + PRE, t1 + PRE, f) for (t0, t1, f) in _P[:13]] +
          [(T_BEAT, T_LAND, M7.beat(_P10B)),
           (T_LAND, T_11, land_beat(_f11)),
           (T_11, T_UP, s11_live(_f11)),
           (T_UP, T_UP + UP, up_beat(_f11)),
           (T_UP + UP, DURATION, M3.tail)])


def shake(t):
    if T_LAND + 0.3 <= t < T_LAND + 0.55:               # the THUD, now on the landing
        f = int((t - T_LAND - 0.3) * 30)
        return (5, -4, 3, -2, 1, 0, 0, 0)[f % 8]
    return 0
