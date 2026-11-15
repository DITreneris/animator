"""ANIMATION v1 of the Christmas special "Happy Compliance" (540 rough of the release), 28.9 s.
Built on storyboard v2 (xmas_sb_v2.py, kept as is) with the approved mix (xmas_mix_v1.wav). Adds the acting
and polish, by hooking the drawing functions for this render only (every module and earlier render unchanged):
- lip-sync from the real takes (xmas_visemes.json): Don, Sofía (red lips), Pam, and the robot's screen mouth;
- blinks for Don and Sofía (eyelids over open eyes only);
- camera punches: a push on "DETECTED", a jolt on Sofía's two slaps, a shake on the THUD;
- the robot's wheel spins when it moves;
- anticipation: Don dips before the razor goes up on "Nice balls";
- the razor payoff: bigger and closer, it spins in and stops against the robot's wheel;
- lighting: a soft warm glow on the string lights and the tree, and a light warm vignette."""
import json
import math
import os
import cairo
import kit
from kit import clamp, ease, lerp, INK
import anim
import xmas_set as xs
import sofia_xmas as sx
import pam_xmas as px
import don_xmas as dx
import santa_robot as sr
import waiter_kit as w
import iwry_mouths as mo
import xmas_sb_v2 as sb

DURATION = sb.DURATION
RAW_T = 0.0
_HERE = os.path.dirname(os.path.abspath(__file__))
VIS = json.load(open(os.path.join(_HERE, "xmas_visemes.json")))
OPEN = mo.OPEN
ACT = {"t": 0.0}
DON_BLINKS = (1.0, 8.75, 21.05)
SOF_BLINKS = (3.0, 6.35, 11.4, 22.9, 24.85)
MOVING = ((11.8, 12.7), (16.3, 16.42), (16.7, 16.82), (17.1, 17.22), (18.1, 18.3), (18.9, 19.25))


def vis(who, t):
    i = int(round(t * 12))
    v = VIS[who]
    return v[i] if 0 <= i < len(v) else ""


def blinking(t, times, d=0.14):
    return any(0 <= t - b < d for b in times)


def lids(k, x, y, skin, r, seed):
    c = k.c
    for ex in (-17, 17):
        kit.ellipse(k, x + ex, y, r, r, skin, seed + ex, shadow=False, outline=False)
        c.set_source_rgb(*INK); c.set_line_width(4); c.set_line_cap(1)
        c.move_to(x + ex - r + 1.5, y + 1); c.curve_to(x + ex - 4, y + 5, x + ex + 4, y + 5, x + ex + r - 1.5, y + 1)
        c.stroke()


# ------------------------------------------------------------------ Don: mouth and blinks, under the foam
_don_hook0 = dx._face_hook
_don0 = dx.don


def _don_hook(orig, foam):
    def face_draw(k, x, y, face, look, glasses=False, seed=0):
        orig(k, x, y, face, look, glasses=glasses, seed=seed)
        if seed == dx.FACE_SEED[0]:
            chin = ACT.get("don_chin", 0)
            if blinking(ACT["t"], DON_BLINKS) and face not in ("smug", "happy", "pleased", "grin"):
                lids(k, x, y - 7 * chin, kit.PEOPLE["DON"]["skin"], 12, seed + 60)
            code = vis("DON", ACT["t"])
            if code:
                mo.mouth(k, x, y - 7 * chin + 28, code, kit.PEOPLE["DON"]["skin"], erase=(20, 15), seed=seed)
            if foam:
                dx.foam_patch(k, x, y, seed)
    return face_draw


def _don(k, *a, **kw):
    ACT["don_chin"] = kw.get("chin", 0)
    kw = dict(kw)
    return _don0(k, *a, **kw)


# ------------------------------------------------------------------ Sofía: red-lip mouth and blinks
_sface0 = sx.face


def _sface(k, x, y, kind="neutral", look=(0, 0), seed=0):
    _sface0(k, x, y, kind, look, seed)
    if blinking(ACT["t"], SOF_BLINKS) and kind in ("neutral", "unimpressed", "knowing", "smile"):
        lids(k, x, y, sx.SKIN, 13, seed + 70)
    code = vis("SOF", ACT["t"])
    if code and ACT.get("sof_mouth", True):
        mo.mouth(k, x, y + 29, code, sx.SKIN, lip_col=sx.RED, inner=(0.45, 0.06, 0.08), erase=(19, 11), seed=seed)


# ------------------------------------------------------------------ Pam: mouth (the mask covers only the eyes)
_pam_hook0 = px._face_hook
_pam0 = px.pam


def _pam_hook(orig, mask, chin=0.0):
    def with_mouth(k, x, y, face, look, glasses=False, seed=0):
        orig(k, x, y, face, look, glasses=glasses, seed=seed)
        if seed == px.FACE_SEED[0]:
            code = vis("PAM", ACT["t"])
            if code:
                mo.mouth(k, x, y - 7 * ACT.get("pam_chin", 0) + 28, code, kit.PEOPLE["PAM"]["skin"], erase=(20, 13),
                         seed=seed)
    return _pam_hook0(with_mouth, mask, chin)


def _pam(k, *a, **kw):
    ACT["pam_chin"] = kw.get("chin", 0)
    return _pam0(k, *a, **kw)


# ------------------------------------------------------------------ the robot: screen mouth and a spinning wheel
_robot0 = sr.robot
_wheel0 = w._wheel


def _robot(k, x, feet, s=1.0, pose="stand", face="eager", look=(0, 0), wobble=0.0, side=1, talk=0.0, **kw):
    code = vis("ROB", ACT["t"])
    if code and face in ("stern", "proud", "smug", "eager"):
        talk = OPEN[code] * (1.0 if face == "stern" else 0.8) + (0.1 if code == "M" else 0.0)
    elif ACT.get("lipsync_robot", True):
        talk = 0.0
    return _robot0(k, x, feet, s, pose, face, look, wobble, side, talk, **kw)


def _wheel(k, locked, seed):
    _wheel0(k, locked, seed)
    c = k.c
    t = ACT["t"]
    ang = 0.0
    for a, b in MOVING:                                     # spin only while it travels
        ang += max(0.0, min(t, b) - a) * 16.0
    c.set_source_rgb(0.55, 0.57, 0.62); c.set_line_width(2.4); c.set_line_cap(1)
    for i in range(3):
        aa = ang + i * math.pi / 3
        c.move_to(math.cos(aa) * 10, -24 + math.sin(aa) * 10); c.line_to(math.cos(aa) * 21, -24 + math.sin(aa) * 21)
        c.stroke()


# ------------------------------------------------------------------ lighting: warm glow on the lights and the tree
_lights0 = xs.lights
_tree0 = xs.tree


def _glow(c, x, y, r, a, col=(1.0, 0.82, 0.45)):
    g = cairo.RadialGradient(x, y, 0, x, y, r)
    g.add_color_stop_rgba(0, *col, a); g.add_color_stop_rgba(1, *col, 0)
    c.set_source(g); c.arc(x, y, r, 0, 2 * math.pi); c.fill()


def _lights(k, x0, x1, y, sag=26, n=16, boil=0):
    c = k.c
    seg = (x1 - x0) / 3
    for j in range(3):
        a, b = x0 + j * seg, x0 + (j + 1) * seg
        for i in range(1, 6):
            t = i / 6
            px_ = (1 - t) ** 3 * a + 3 * (1 - t) ** 2 * t * (a + seg * 0.3) + 3 * (1 - t) * t * t * (b - seg * 0.3) + t ** 3 * b
            py_ = (1 - t) ** 3 * y + 3 * (1 - t) ** 2 * t * (y + sag) + 3 * (1 - t) * t * t * (y + sag) + t ** 3 * y
            col = xs.LIGHTS[(j * 5 + i - 1 + boil) % 4]
            _glow(c, px_, py_ + 8, 26, 0.35, col)
    _lights0(k, x0, x1, y, sag, n, boil)


def _tree(k, x=xs.TREE_X, base=xs.TREE_BASE, s=xs.TREE_S, censored=(), seed=950, boil=0):
    _glow(k.c, x, base - 170 * s, 230 * s, 0.22)
    return _tree0(k, x, base, s, censored, seed, boil)


def vignette(c):
    g = cairo.RadialGradient(270, 470, 260, 270, 470, 640)
    g.add_color_stop_rgba(0, 0.35, 0.18, 0.05, 0.0)
    g.add_color_stop_rgba(1, 0.35, 0.18, 0.05, 0.28)
    c.set_source(g); c.paint()


# ------------------------------------------------------------------ shot overrides: anticipation, the razor
def s4b(k, t, tl):
    look = (-0.8, 0.9) if t < 8.2 else (-0.8, 0)
    DIP = (-48, 206, 8, 0)

    def draw():
        xs.set_dressing(k, boil=int(t * 4)); xs.door(k, open_amt=1.0)
        if t < 6.82:                                        # a small dip before the razor goes up
            pose = anim.tween(dx.POSE_JAW, DIP, u(t, 6.7, 0.1))
        else:
            pose = anim.tween(DIP, dx.POSE_LINE, u(t, 6.82, 0.25), overshoot=True)
        dx.don(k, 600, xs.FEET, 1.0, kit.ARM_POSES[pose], "neutral" if t < 8.2 else "smug", look=look,
               chin=0.6 if t >= 8.2 else 0.0)
    sb.world(k, sb.CAM4, draw)
    if 6.85 <= t < 9.45:
        sb.xb.speech(k, "Nice balls.\nI've got two for you.", sb.top(sb.CAM4, 600, xs.FEET, sb.DON_HY), t, 6.85)


def u(t, t0, d):
    return clamp((t - t0) / d)


def s11(k, t, tl):
    peel = u(t, 28.1, 0.4)

    def draw():
        xs.set_dressing(k, boil=int(t * 4))
        cen = tuple(i for i in range(8) if not (i == 2 and t >= 28.1))
        xs.tree(k, censored=cen)
        if t >= 28.1:
            import xmas_test_a as ta
            ox, oy = ta.ORN[2]
            sr.censor_bar(k, ox - 6 * peel, oy + 120 * peel ** 2, 14 * 3.0 * xs.BAR_SCALE, 14 * 0.95 * xs.BAR_SCALE,
                          rot=0.08 + 2.2 * peel, seed=1200)
        sr.robot(k, 420, xs.FEET, 1.0, "present", "proud" if t < 28.35 else "stern", side=-1, alarm=t >= 28.35)
        if t >= 27.3:                                       # bigger, closer: spins in and stops at the wheel
            v = ease(u(t, 27.3, 0.55))
            hit = u(t, 27.85, 0.12)
            bx = lerp(255, 382, v) - 6 * math.sin(math.pi * hit)
            dx.razor(k, (bx, xs.FEET - 7), 1.7, ang=1.57 + 0.35 + 9.0 * (1 - v), seed=1210)
    sb.world(k, sb.CAM11, draw)
    if 26.95 <= t < 28.1:
        sb.xb.speech(k, "Happy compliance!", sb.top(sb.CAM11, 420, xs.FEET, sb.ROB_HY, 115), t, 26.95, size=30)
    if 27.2 <= t < 27.6:
        sb.xb.burst(k, "THUD", 105, 470, t, 27.2)


OVERRIDE = {sb.s4b: s4b, sb.s11: s11}


# ------------------------------------------------------------------ camera punches and the per-frame wrapper
def punch(t):
    """Screen-space zoom and offset."""
    z, dx_, dy_ = 1.0, 0.0, 0.0
    if 13.75 <= t < 14.4:                                   # push on "DETECTED"
        z = 1 + 0.07 * ease(u(t, 13.75, 0.12)) * (1 - ease(u(t, 14.1, 0.3)))
    for th in (18.38, 18.68):                               # jolts on Sofía's two slaps
        if 0 <= t - th < 0.1:
            dx_ += (5, -4, 3)[int((t - th) * 30) % 3]; dy_ += (-3, 3, -2)[int((t - th) * 30) % 3]
    if 0 <= t - 27.2 < 0.25:                                # the THUD shake
        f = int((t - 27.2) * 30)
        dx_ += (8, -7, 6, -5, 4, -3, 2, -1)[f % 8]; dy_ += (-5, 5, -4, 3, -2, 2, -1, 1)[f % 8]
    return z, dx_, dy_


def wrap(fn):
    def panel(k, t, tl):
        c = k.c
        rt = RAW_T if abs(RAW_T - t) < 0.2 else t
        ACT["t"] = t
        z, ox, oy = punch(rt)
        c.save()
        c.translate(270 + ox, 480 + oy); c.scale(z, z); c.translate(-270, -480)
        dx.don, dx._face_hook, sx.face = _don, _don_hook, _sface
        px.pam, px._face_hook = _pam, _pam_hook
        sr.robot, w._wheel = _robot, _wheel
        xs.lights, xs.tree = _lights, _tree
        try:
            OVERRIDE.get(fn, fn)(k, t, tl)
        finally:
            dx.don, dx._face_hook, sx.face = _don0, _don_hook0, _sface0
            px.pam, px._face_hook = _pam0, _pam_hook0
            sr.robot, w._wheel = _robot0, _wheel0
            xs.lights, xs.tree = _lights0, _tree0
        c.restore()
        c.save(); c.identity_matrix(); vignette(c); c.restore()
    return panel


PANELS = [(t0, t1, wrap(fn)) for t0, t1, fn in sb.PANELS]
