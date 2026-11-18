"""ANIMATION v11 of "Happy Compliance" (18 Nov): v10 (xmas_anim10.py, kept) plus life in the background, same length
and sound. Everything runs on v10's clock (CLOCK), which the tail holds at 0, so the last frame is still frame 0.
- the tree twinkles: small fairy lights along its three tinsel ropes fade in and out, out of step;
- the bunting sways: each letter flag swings gently from the string, a ripple running along it;
- the robot's pompom (its antenna light) bobs: a slow idle bob, a wobble while it rolls, a damped bounce when it stops;
- Sofía's hair and ice-bauble earrings sway a little all the time (on top of the swing she already had);
- Don and Pam really breathe now (v10's breathing was bypassed for them by xmas_anim's per-frame swaps);
- the robot's screen blinks now and then (its eager face).
Module protocol for engine_v / engine_hd: PANELS, DURATION, RAW_T, shake."""
import inspect
import math
import kit
import xmas_anim10 as M10
import xmas_anim as xa
import xmas_set as xs
import santa_robot as sr
import waiter_kit as w
import sofia_xmas as sxm

PANELS, DURATION, RAW_T, PRE = M10.PANELS, M10.DURATION, 0.0, M10.PRE
CLOCK = M10.CLOCK


def shake(t):
    return M10.shake(t)


# ---------------------------------------------------------------- breathing, for real
# v10 wrapped dx.don and pam_xmas.pam, but xmas_anim swaps those per frame for its own lip-sync versions, which call
# the originals it captured at import (and restore them after each frame): so in v10 only Sofía breathed. Point its
# captured originals at v10's breathing versions.
import don_xmas as dx
import pam_xmas as pm
xa._don0 = dx.don
xa._pam0 = pm.pam

# ---------------------------------------------------------------- the tree twinkles
_tree0 = xs.tree
ROPES = ((-80, -78, 84, -110), (-62, -170, 64, -196), (-44, -246, 44, -262))   # xs.tree's tinsel, tree-local


def tree(k, x=xs.TREE_X, base=xs.TREE_BASE, s=xs.TREE_S, *a, **kw):
    out = _tree0(k, x, base, s, *a, **kw)
    c = k.c
    t = CLOCK["t"]
    c.save(); c.translate(x, base); c.scale(s, s)
    n = 0
    for (ax, ay, bx, by) in ROPES:
        for q in (0.1, 0.24, 0.38, 0.52, 0.66, 0.8, 0.94):
            p0, p1, p2, p3 = (ax, ay), (ax * 0.3, ay + 22), (bx * 0.3, by + 22), (bx, by)
            px_ = (1 - q) ** 3 * p0[0] + 3 * (1 - q) ** 2 * q * p1[0] + 3 * (1 - q) * q * q * p2[0] + q ** 3 * p3[0]
            py_ = (1 - q) ** 3 * p0[1] + 3 * (1 - q) ** 2 * q * p1[1] + 3 * (1 - q) * q * q * p2[1] + q ** 3 * p3[1]
            if any((px_ - ox) ** 2 + (py_ + 6 - oy) ** 2 < (r + 9) ** 2 for ox, oy, r, _ in xs.ORNAMENTS):
                n += 1
                continue                                # never on top of an ornament
            lv = 0.5 + 0.5 * math.sin(2 * math.pi * t * 0.9 + n * 2.3)
            col = xs.LIGHTS[n % 4]
            c.set_source_rgba(*col, 0.35 * lv); c.arc(px_, py_ + 6, 10, 0, 2 * math.pi); c.fill()
            c.set_source_rgb(*[0.55 * v + 0.45 * v * lv for v in col]); c.arc(px_, py_ + 6, 4.2, 0, 2 * math.pi)
            c.fill_preserve(); c.set_source_rgb(*kit.INK); c.set_line_width(1.2); c.stroke()
            if lv > 0.8:
                c.set_source_rgb(1, 1, 1); c.arc(px_ - 1.4, py_ + 4.6, 1.3, 0, 2 * math.pi); c.fill()
            n += 1
    c.restore()
    return out


xs.tree = tree
xa._tree0 = tree                                      # xmas_anim swaps xs.tree per frame and calls this

# ---------------------------------------------------------------- the bunting sways
_src = inspect.getsource(xs.banner)
_old = "        cut(k, [(fx - step * 0.45, fy), (fx + step * 0.45, fy), (fx, fy + step * 1.15)], col, shadow=False, lw=1.6)\n"
_old2 = "        text(k, ch, fx, fy + step * 0.52, step * 0.6, (1, 1, 1), bold=True)\n"
assert _old in _src and _old2 in _src
_src = _src.replace(_old, "        c.save(); c.translate(fx, fy); c.rotate(SWAY(i)); c.translate(-fx, -fy)\n" + _old)
_src = _src.replace(_old2, _old2 + "        c.restore()\n")
_ns = dict(xs.__dict__)
_ns["SWAY"] = lambda i: 0.07 * math.sin(2 * math.pi * CLOCK["t"] / 2.6 - i * 0.45)
exec(compile(_src, "banner_v11", "exec"), _ns)
xs.banner = _ns["banner"]

# ---------------------------------------------------------------- the robot's pompom bobs
POM = {"dx": 0.0, "dy": 0.0}
_src = inspect.getsource(sr._hat)
for a_, b_ in (("70, -64", "PX, PY"), ("70 + math.cos", "PX + math.cos"), ("-64 + math.sin", "PY + math.sin"),
               ("66, -68", "PX - 4, PY - 4"), ("c.curve_to(48, -100, 64, -86, 68, -66)", "c.curve_to(48, -100, 64, -86, PX - 2, PY - 2)")):
    assert a_ in _src, a_
    _src = _src.replace(a_, b_)
_src = _src.replace('    c = k.c\n', '    c = k.c\n    PX, PY = 70 + POM["dx"], -64 + POM["dy"]\n', 1)
_ns = dict(sr.__dict__); _ns["POM"] = POM
exec(compile(_src, "hat_v11", "exec"), _ns)
sr._hat = _ns["_hat"]


def _pom(t2):
    """Pompom offset (head-local units) at v2 clock t2: idle bob, rolling wobble, a damped bounce after each stop."""
    dx, dy = 0.0, 1.6 * math.sin(2 * math.pi * CLOCK["t"] / 1.7)
    for a, b in xa.MOVING:
        if a <= t2 < b:
            dx += 5 * math.sin((t2 - a) * 26); dy += 2.5 * abs(math.sin((t2 - a) * 26))
        elif b <= t2 < b + 0.8:
            e = math.exp(-(t2 - b) * 6)
            dx += 6 * e * math.sin((t2 - b) * 30)
    return dx, dy


_robot_v11 = sr.robot


def robot(k, *a, **kw):
    POM["dx"], POM["dy"] = _pom(CLOCK["t"] - PRE)
    return _robot_v11(k, *a, **kw)


sr.robot = robot
xa._robot0 = robot                                    # (same: xmas_anim's per-frame robot calls this)

# ---------------------------------------------------------------- Sofía's hair and earrings sway
_sofia_v11 = sxm.sofia


def sofia(k, x, feet, s=1.0, pose="stand", face_kind="neutral", look=(0, 0), lag=(0, 0), *a, **kw):
    t = CLOCK["t"]
    lag = (lag[0] + 3.2 * math.sin(2 * math.pi * t / 2.2), lag[1] + 1.2 * math.sin(2 * math.pi * t / 1.1))
    return _sofia_v11(k, x, feet, s, pose, face_kind, look, lag, *a, **kw)


sxm.sofia = sofia

# ---------------------------------------------------------------- the robot's screen blinks
_face_v11 = w.screen_face
BLINKS = (1.3, 4.3, 7.1, 10.2, 13.0, 16.4, 19.6, 22.3, 25.4, 29.6, 31.9)        # CLOCK seconds


def screen_face(k, face, look=(0, 0), talk=0.0, side=1):
    t = CLOCK["t"]
    if face == "eager" and talk <= 0.05 and any(0 <= t - b < 0.1 for b in BLINKS):
        face = "blink"
    return _face_v11(k, face, look, talk, side)


w.screen_face = screen_face
