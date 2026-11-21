"""OFFICE NOIR 3: the motion tools, v1 (20 Nov). Tomas: "Don is redrawn; he moves like a diagram; everyone's walking
has to be put right". Nothing here changes an earlier module: every patch is put on while one figure is drawn and taken
off again, and a film that does not call these draws as before.
  don(...)        Don for this film: Office Noir 2's detective with LEGS and SHOES (he stood on a block: "square legs
                  with no feet"), sleeves in one piece (the kit's two-part arm read as "jointed segments"), ears and
                  short grey hair at the temples (the kit's two grey blocks read as a headset's pads), his fedora.
                  steps: his two feet, as on2_motion.don_legs; walk=(x, dir) steps him by where he is.
  don_back(...)   the same from behind: no headset.
  walk(fn, x, s)  a cast callable of the Client (client_on3.boxer, street clothes) drawn walking: the feet step by where
                  he is on the ground (no sliding), the body rises between steps, the arms swing a little.
  her(fn, x, feet, s)  the woman under the umbrella walking: her own legs and boots, stepping.
  stride(u, a, up)     one foot through a cycle (Office Noir 2's)."""
import math
import contextlib
import cairo
import kit
import noir2_cast as n2
import client_on3 as b
from kit import cut, rect, ellipse, INK

d = n2.d
_DET, _BACK = n2.detective, n2.detective_back                # as they are when this module is first imported
TROUSERS, SHOE = (0.30, 0.30, 0.34), (0.07, 0.07, 0.08)
STAND = ((-14, 0, 0), (14, 0, 0))
NOW = {}                                                     # "walk": (x, dir) or "steps": for a Don drawn by another module's code


def stride(u, a=28.0, up=14.0):
    u = u % 1.0
    if u < 0.5:
        return a * (1 - 4 * u), 0.0
    q = (u - 0.5) / 0.5
    return -a + 2 * a * q, up * math.sin(math.pi * q)


def rise(u, h):
    """How far the body is lifted: highest as one foot passes the other, twice a cycle."""
    return h * abs(math.sin(2 * math.pi * u))


@contextlib.contextmanager
def _swap(*triples):
    old = [(o, n, getattr(o, n)) for o, n, _ in triples]
    for o, n, v in triples:
        setattr(o, n, v)
    try:
        yield
    finally:
        for o, n, v in old:
            setattr(o, n, v)


# ---- Don -----------------------------------------------------------------------------------------------------------
def _sleeves(k, pose, col, seed, cuff=None):
    """One sleeve from the shoulder to the wrist, bent, not two boards and a joint; a cuff; a hand."""
    c = k.c
    a = d._pose_tuple(pose); hands = []
    dd = lambda g: (math.sin(math.radians(g)), math.cos(math.radians(g)))
    for side, (u, f) in ((-1, (a[0], a[1])), (1, (a[2], a[3]))):
        sx, sy, ln = side * 40, d.BT + 16, 48
        ex, ey = sx + dd(u)[0] * ln, sy + dd(u)[1] * ln
        hx, hy = ex + dd(u + f)[0] * ln, ey + dd(u + f)[1] * ln
        qx, qy = hx - dd(u + f)[0] * 9, hy - dd(u + f)[1] * 9
        for w, colr in ((23, INK), (19, col)):
            c.set_source_rgb(*colr); c.set_line_width(w); c.set_line_cap(0); c.set_line_join(1)
            c.new_path(); c.move_to(sx - (0 if colr == INK else 0), sy - (2 if colr == INK else 0)); c.curve_to(ex, ey, ex, ey, qx, qy); c.stroke()
        for w, colr in ((23, INK), (19, d.TRENCH_SHADE)):                                   # the cuff
            c.set_source_rgb(*colr); c.set_line_width(w); c.set_line_cap(0)
            c.new_path(); c.move_to(qx - dd(u + f)[0] * (2 if colr == INK else 0), qy - dd(u + f)[1] * (2 if colr == INK else 0))
            c.line_to(qx + dd(u + f)[0] * 6, qy + dd(u + f)[1] * 6); c.stroke()
        ang = math.atan2(dd(u + f)[1], dd(u + f)[0])
        c.save(); c.translate(hx, hy); c.rotate(ang)
        c.new_path(); c.move_to(-8, -8); c.curve_to(2, -11, 13, -9, 15, -3); c.curve_to(16, 4, 10, 9, 0, 9); c.line_to(-8, 8); c.close_path()   # the palm and fingers together
        c.set_source_rgb(*d.SKIN); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2); c.stroke()
        c.new_path(); c.move_to(-2, -8 * side); c.curve_to(2, -15 * side, 8, -14 * side, 7, -8 * side)                                       # the thumb
        c.set_source_rgb(*d.SKIN); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1.8); c.stroke()
        c.set_source_rgb(*INK); c.set_line_width(1.2); c.move_to(8, -2); c.line_to(14, -1); c.move_to(8, 3); c.line_to(13, 4); c.stroke()         # fingers
        c.restore()
        hands.append((hx, hy))
    return hands


def _no_blocks(orig):
    def r(k, x, y, w, h, *a, **kw):
        if (w, h) == (12, 26):                               # the kit's grey blocks beside his head
            return None
        return orig(k, x, y, w, h, *a, **kw)
    return r


def hat(k, hx, hy, s):
    c = k.c
    c.save(); c.translate(hx, hy); c.scale(s, s)
    felt, band = (0.34, 0.34, 0.38), (0.08, 0.08, 0.10)
    c.new_path(); c.move_to(-34, -30); c.curve_to(-36, -78, -10, -84, -2, -70); c.curve_to(8, -86, 36, -78, 34, -30); c.close_path()
    c.set_source_rgb(*felt); c.fill_preserve(); c.set_source_rgb(0.05, 0.05, 0.06); c.set_line_width(2.6); c.stroke()
    c.set_source_rgb(*band); c.rectangle(-34, -42, 68, 11); c.fill()
    c.new_path(); c.move_to(-58, -30); c.curve_to(-40, -40, 40, -40, 58, -30); c.curve_to(40, -20, -40, -20, -58, -30); c.close_path()
    c.set_source_rgb(*felt); c.fill_preserve(); c.set_source_rgb(0.05, 0.05, 0.06); c.set_line_width(2.6); c.stroke()
    c.restore()


def _legs(k, x, feet, s, steps):
    c = k.c; hem = d.HEM
    c.save(); c.translate(x, feet); c.scale(s, s)
    for hip, (fx, lift, toe) in sorted(zip((-13, 13), steps), key=lambda q: -q[1][1]):      # the lifted foot behind
        cut(k, [(hip - 14, hem - 8), (hip + 14, hem - 8), (fx + 13, -lift - 8), (fx - 13, -lift - 8)], TROUSERS, shadow=False, lw=2.2)
        if toe:
            cut(k, [(fx - toe * 14, -lift - 13), (fx + toe * 10, -lift - 13), (fx + toe * 28, -lift - 5), (fx + toe * 28, -lift), (fx - toe * 14, -lift)],
                SHOE, shadow=False, lw=1.8)
        else:
            ellipse(k, fx, -lift - 6, 17, 9, SHOE, 560 + hip, shadow=False, lw=1.8)
    c.restore()


def walk_steps(x, s, dir_=1, a=22.0, up=12.0, toe=None):
    """His feet for where he stands: x on the ground, s his scale. Returns (steps, rise)."""
    u = x / (4.0 * a * s) * dir_
    f0, f1 = stride(u, a, up), stride(u + 0.5, a, up)
    t_ = dir_ if toe is None else toe
    r_ = rise(u, 3.5)
    return ((-13 + f0[0] * dir_ * 0.8, f0[1] - r_, t_), (13 + f1[0] * dir_ * 0.8, f1[1] - r_, t_)), r_


def don(k, x, feet, s=1.0, pose="look", face="squint", look=(0.8, 0.5), lean=0.0, glass=True, wrap=False,
        napkin_in_band=False, seed=500, cloth_ang=0.0, steps=None, walk=None):
    c = k.c
    up_ = 0.0
    walk = walk if walk is not None else NOW.get("walk")
    steps = steps or NOW.get("steps")
    if walk is not None:
        steps, up_ = walk_steps(walk[0], s, walk[1])
    steps = steps or STAND
    c.save(); c.translate(x, feet); c.rotate(math.radians(lean)); c.translate(-x, -feet - up_ * s)
    _legs(k, x, feet, s, steps)
    c.push_group()
    old_look = n2.LOOK[0]; n2.LOOK[0] = 9                                                # bare head under this film's hat
    with _swap((d, "_arms", _sleeves), (kit, "rect", _no_blocks(kit.rect))):
        try:
            o = _DET(k, x, feet, s, pose, face, look, 0.0, glass, wrap, napkin_in_band, seed, cloth_ang)
        finally:
            n2.LOOK[0] = old_look
    c.save(); c.set_operator(cairo.OPERATOR_CLEAR)                                           # the block he stood on, out
    c.rectangle(x - 64 * s, feet + (d.HEM + 1.5) * s, 128 * s, (-d.HEM + 14) * s); c.fill(); c.restore()
    c.pop_group_to_source(); c.paint()
    hx, hy = o["head"]
    c.save(); c.translate(hx, hy); c.scale(s, s)
    c.restore()
    hat(k, hx, hy, s)
    dev = {"head": c.user_to_device(*o["head"]), "hands": [c.user_to_device(*q) for q in o["hands"]]}
    c.restore()
    o = dict(o); o["head"] = c.device_to_user(*dev["head"]); o["hands"] = [c.device_to_user(*q) for q in dev["hands"]]
    return o


def _no_pads(orig):
    def e(k, x, y, rx, ry, col, *a, **kw):
        if (rx, ry) == (9, 15):
            return None
        return orig(k, x, y, rx, ry, col, *a, **kw)
    return e


def don_back(k, x, feet, s=1.0, *a, **kw):
    with _swap((n2, "ellipse", _no_pads(n2.ellipse))):
        o = _BACK(k, x, feet, s, *a, **kw)
    hat(k, o["head"][0], o["head"][1], s)
    return o


# ---- the Client, walking -------------------------------------------------------------------------------------------
_STEP = [None]                                               # ((dx, lift), (dx, lift)) while he is drawn walking
_LOW = b._lower_street


def _lower_street(k, seed):
    if _STEP[0] is None:
        return _LOW(k, seed)
    c = k.c
    legs = (((-28, 27), (-2, -56, -48, -10), (-49, -9), (-44, -41)), ((46, 31), (2, 56, 64, 26), (25, 65), (48, 56)))
    for ((cx, rx), (h0, h1, f0, f1), (c0, c1), (s0, s1)), (dx, lift) in sorted(zip(legs, _STEP[0]), key=lambda q: -q[1][1]):
        ellipse(k, cx + dx, -3 - lift, rx, 7, b.SOLE, seed + 1 + cx, lw=2)
        ellipse(k, cx + dx, -10 - lift, rx, 11, b.TRAINER, seed + 2 + cx, shadow=False, lw=2)
        cut(k, [(h0, b.HIP - 4), (h1, b.HIP - 4), (f0 + dx, -22 - lift), (f1 + dx, -22 - lift)], b.CHAR, shadow=False, lw=2.2)
        cut(k, [(c0 + dx, -30 - lift), (c1 + dx, -30 - lift), (c1 - 1 + dx, -14 - lift), (c0 + 1 + dx, -14 - lift)], b.CHAR_DARK, shadow=False, lw=1.8)
        c.set_source_rgb(*b.CHAR_LINE); c.set_line_width(2.0); c.set_line_cap(1)
        c.move_to(s0, b.HIP + 30); c.line_to(s1 + dx, -34 - lift); c.stroke()


def walk(fn, x, s, dir_=1, a=34.0, up=26.0, on=True):
    """fn: a cast callable that draws the Client at x (scale s). Drawn walking when on."""
    if not on:
        return fn

    def dr(k):
        u = x / (4.0 * a * s) * dir_
        f0, f1 = stride(u, a, up), stride(u + 0.5, a, up)
        r_ = rise(u, 4.0)
        sw = 11.0 * math.sin(2 * math.pi * u)
        wpose = b.POSES["b_walk"]
        swung = (wpose[0] + sw, wpose[1], wpose[2] + sw, wpose[3])
        _STEP[0] = ((f0[0] * dir_ * 0.8, f0[1] - r_), (f1[0] * dir_ * 0.8, f1[1] - r_))
        k.c.save(); k.c.translate(0, -r_ * s)
        try:
            with _swap((b, "_lower_street", _lower_street)):
                b.POSES["b_walk"] = swung
                return fn(k)
        finally:
            b.POSES["b_walk"] = wpose
            _STEP[0] = None; k.c.restore()
    return dr


# ---- the woman under the umbrella, walking --------------------------------------------------------------------------
TIGHTS, BOOT = (0.13, 0.13, 0.15), (0.05, 0.05, 0.06)
HEM_HER = -96


def her(fn, x, feet, s, dir_=-1, a=26.0, up=15.0, on=True):
    """fn draws her standing at (x, feet), scale s. Walking: her own legs and boots are drawn stepping, and she is drawn
    over them down to her hem only."""
    if not on:
        return fn

    def dr(k):
        c = k.c
        u = x / (4.0 * a * s) * dir_
        f0, f1 = stride(u, a, up), stride(u + 0.5, a, up)
        r_ = rise(u, 3.0)
        c.set_source_rgba(0, 0, 0, 0.35); c.save(); c.translate(x, feet); c.scale(36, 36 * 0.16); c.new_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()   # her shadow, on the ground
        c.save(); c.translate(0, -r_ * s)
        c.save(); c.translate(x, feet); c.scale(s, s)
        for hip, (fx, lift) in sorted(zip((-17, 17), (f0, f1)), key=lambda q: -q[1][1]):
            fx = hip + fx * dir_ * 0.8; lift = lift - r_
            cut(k, [(hip - 8, HEM_HER - 6), (hip + 8, HEM_HER - 6), (fx + 6, -lift - 20), (fx - 6, -lift - 20)], TIGHTS, shadow=False, lw=1.8)
            cut(k, [(fx - 8, -lift - 26), (fx + 8, -lift - 26), (fx + 8 + dir_ * 9, -lift - 3), (fx + 8 + dir_ * 9, -lift), (fx - 8 + dir_ * 2, -lift), (fx - 8, -lift - 6)],
                BOOT, shadow=False, lw=1.6)
        c.restore()
        c.save(); c.rectangle(-4000, -4000, 8000, 4000 + feet + (HEM_HER + 2) * s); c.clip()
        try:
            return fn(k)
        finally:
            c.restore(); c.restore()
    return dr


# ---- v2: life: in-betweens when a pose or a place jumps, breath, blinks, lips -----------------------------------------
# A film sets the clock for every drawing (timed); a figure wrapped in alive() then
#   moves from its last pose and place to the new one over four drawings, with a small overshoot, when they jump;
#   breathes (a slow rise and fall about its feet); blinks; and, while CLOCK["say"][who] holds a mouth shape, talks.
# Without a clock (CLOCK["shot"] is None) a wrapped figure draws exactly as the figure it wraps.
CLOCK = {"shot": None, "t": 0.0, "T": 0.0, "say": {}}
_ST, _CNT = {}, {}
_ROBE = {}
ROBE_SHOTS = {"5.1c"}
ROBE_FADE = [True]                                           # film v21 sets it off: 5.1c draws its own half-off robe
MASKS = [False]                                              # v5, opt-in: keep each figure's outline for the light pass
FACE_AT = {}                                                 # v5: who -> shot -> [(from t, face)], used where the shot asks for the plain "hard" face
FROZEN = set()                                               # shots whose figures do not breathe or blink (the loop's two ends: frame 0 is the last frame)
TWEEN = 4.0 / 30.0


def timed(name, fn, start):
    def f(t):
        CLOCK["shot"], CLOCK["t"] = name, t
        CLOCK["T"] = CLOCK.pop("T_ext", start + t)
        CLOCK["heads"], CLOCK["zoom"] = {}, None             # v3: where each speaker's head is on the finished frame, for bubbles
        CLOCK["figs"] = []                                   # v5: each tracked figure's own outline on the frame, for light that falls on it
        _CNT.clear()
        return fn(t)
    return f


def _back(p):
    p = max(0.0, min(1.0, p)) - 1.0
    return 1.0 + p * p * (2.2 * p + 1.2)


def alive(orig, who, poses=None, skin=None, lip=None, breathe=0.007, blinks=True, tween_pose=True, mouth_kw=False):
    import inspect
    default_pose = inspect.signature(orig).parameters["pose"].default
    ph = (sum(ord(ch) for ch in who) % 17) / 17.0

    def fig(k, x, feet, s=1.0, pose=None, *a, **kw):
        pose = default_pose if pose is None else pose
        if CLOCK["shot"] is None:
            return orig(k, x, feet, s, pose, *a, **kw)
        T = CLOCK["T"]
        try:
            tup = (poses(pose) if callable(poses) else poses[pose]) if (poses is not None and isinstance(pose, str)) else pose
        except KeyError:
            tup = pose
        num = tween_pose and isinstance(tup, (tuple, list)) and all(isinstance(q, (int, float)) for q in tup)
        n = _CNT[who] = _CNT.get(who, 0) + 1
        key = (who, n)
        tgt = (list(tup) if num else []) + [x, feet]
        st = _ST.get(key)
        moving = False
        if (st is None or st["shot"] != CLOCK["shot"] or not (0 < T - st["T"] < 0.09) or len(st["tgt"]) != len(tgt)
                or abs(s - st["s"]) > 0.04 * s):
            cur, st = tgt, {"from": tgt, "t0": -9.0}
        else:
            dp = max([abs(p - q) for p, q in zip(tgt[:-2], st["tgt"][:-2])] or [0.0])
            dx = max(abs(tgt[-1] - st["tgt"][-1]), abs(tgt[-2] - st["tgt"][-2])) / s
            if dx > 130:                                     # a cut inside the shot: no sliding across it
                st["from"], st["t0"] = tgt, -9.0
            elif dp > 16 or dx > 16:                         # a jump: start from what is on the screen now
                st["from"], st["t0"] = st["cur"], T - 1.0 / 30
            p = (T - st["t0"]) / TWEEN
            moving = p < 1.0
            e = _back(p)
            cur = [f + (g - f) * e for f, g in zip(st["from"], tgt)] if moving else tgt
        st.update(shot=CLOCK["shot"], T=T, tgt=tgt, cur=cur, s=s)
        _ST[key] = st
        px, pf = cur[-2], cur[-1]
        ppose = tuple(cur[:-2]) if (num and moving) else pose
        code = CLOCK["say"].get(who)
        if code and mouth_kw:
            kw = dict(kw); kw["mouth"] = code
        still_ = CLOCK["shot"] in FROZEN
        shut = blinks and not still_ and ((T + ph * 5.0) % (2.9 + ph * 1.3)) < 0.1
        c = k.c
        c.save()
        if breathe and not moving and not still_:
            sy = 1.0 + breathe * math.sin(2 * math.pi * (T / 3.4 + ph))
            c.translate(px, pf); c.scale(1.0, sy); c.translate(-px, -pf)
        old = kit.face_draw

        def face_draw(k_, fx, fy, face, look, glasses=False, seed=0):
            old(k_, fx, fy, face, look, glasses=glasses, seed=seed)
            if shut and skin and face not in ("squint", "happy", "pleased", "smug"):
                r_ = 14.5 if face in ("shock", "panic") else 11.5
                for sx in (-17, 17):
                    ellipse(k_, sx, fy, r_, r_, skin, seed + sx + 71, shadow=False, outline=False)
                    k_.c.set_source_rgb(*INK); k_.c.set_line_width(3.2); k_.c.set_line_cap(1)
                    k_.c.move_to(sx - 9, fy + 2); k_.c.curve_to(sx - 3, fy + 5, sx + 3, fy + 5, sx + 9, fy + 2); k_.c.stroke()
            if code and skin and not mouth_kw:
                import iwry_mouths as im
                im.mouth(k_, fx, fy + 28, code, skin, lip_col=lip, erase=(18, 10), seed=seed + 67)
        kit.face_draw = face_draw
        if FACE_AT.get(who, {}).get(CLOCK["shot"]) and a and a[0] == "hard":                  # v5: his face follows the moment (it was one scowl for the whole fight)
            fa = [f_ for t0, f_ in FACE_AT[who][CLOCK["shot"]] if CLOCK["t"] >= t0]
            if fa:
                a = (fa[-1],) + tuple(a[1:])
        robe = None
        kw0 = kw
        if "strip" not in kw and who == "CLIENT" and CLOCK["shot"] in ROBE_SHOTS and ROBE_FADE[0]:      # v6b: before she pulls it the call has no "strip" at all, so the first change was never seen
            kw = dict(kw); kw["strip"] = False
        if "strip" in kw and ROBE_FADE[0]:                                    # v6: his robe comes off, or goes back on, from the hips up, over six drawings (it changed between two)
            rs = _ROBE.get(who)
            if rs is None or rs["shot"] != CLOCK["shot"] or not (0 <= T - rs["T"] < 0.09):
                rs = {"v": kw["strip"], "t0": -9.0}
            elif rs["v"] != kw["strip"]:
                rs["v"], rs["t0"] = kw["strip"], T
            rs["shot"], rs["T"] = CLOCK["shot"], T
            _ROBE[who] = rs
            p_ = (T - rs["t0"]) / 0.4
            if 0 <= p_ < 1:
                robe = p_ if not kw["strip"] else 1 - p_      # how much of him the robe covers, hips to shoulders
        try:
            if MASKS[0]:
                c.push_group()
            if robe is not None:
                kw2 = dict(kw); kw2["strip"] = True
                orig(k, px, pf, s, ppose, *a, **kw2)          # the bare man, whole
                kw = dict(kw0) if "strip" not in kw0 else dict(kw, strip=False)
                c.save(); yl = pf - s * (178 + 290 * robe)
                c.rectangle(px - 400 * s, yl, 800 * s, pf - yl + 80 * s); c.clip()      # the robed one, as far up as the robe has come
            o = orig(k, px, pf, s, ppose, *a, **(kw if robe is not None or "strip" in kw0 else kw0))
            if robe is not None:
                c.restore()
            if MASKS[0]:
                pat = c.pop_group(); c.set_source(pat); c.paint()
                try:
                    m_ = cairo.ImageSurface(cairo.FORMAT_A8, 540, 960); mc = cairo.Context(m_)
                    mc.set_matrix(c.get_matrix()); mc.set_source(pat); mc.paint()
                    hx_, hy_ = c.user_to_device(*o["head"])
                    CLOCK.setdefault("figs", []).append((m_, hx_, hy_, abs(c.get_matrix().xx) * s, who))
                except Exception:
                    pass
            if kw.get("cig") and CLOCK["shot"] in SMOKING and CLOCK["t"] >= SMOKING[CLOCK["shot"]]:      # v4: his cigarette smokes, and its end glows
                tx, ty = o["head"][0] + 48 * s, o["head"][1] + 45 * s
                smoke(c, tx, ty - 2 * s, s * 0.95, seed=0.3, h=170)
                gl = 0.5 + 0.5 * math.sin(T * 5.0)
                c.set_source_rgb(0.86, 0.10 + 0.15 * gl, 0.14); c.arc(tx - 1.5 * s, ty, (2.6 + 1.2 * gl) * s, 0, 2 * math.pi); c.fill()
            try:
                hx_, hy_ = c.user_to_device(*o["head"])
                CLOCK.setdefault("heads", {}).setdefault(who, (hx_, hy_, abs(c.get_matrix().xx) * s))
            except Exception:
                pass
            return o
        finally:
            kit.face_draw = old
            c.restore()
    fig.plain = orig
    return fig


# ---- v4: smoke that moves ----------------------------------------------------------------------------------------------
SMOKING = {}                                                 # shot -> from when (s) the cigarette in the Client's mouth is alight


def smoke(c, x, y, s=1.0, seed=0.0, h=150.0, alpha=0.62):
    """A cigarette's smoke from (x, y): two thin ribbons that rise, widen, curl and thin out, moving with the clock."""
    T = CLOCK["T"] if CLOCK["shot"] is not None else 0.0
    c.save(); c.set_line_cap(1); c.set_line_join(1)
    for rb in range(2):
        px = py = None
        for i in range(15):
            u = i / 14.0
            xx = x + (3 + 26 * u) * s * math.sin(2 * math.pi * (u * 1.5 - T * 0.6 + seed + rb * 0.41)) + 16 * s * u * math.sin(T * 0.35 + seed * 7)
            yy = y - h * s * u
            if px is not None:
                c.set_source_rgba(1, 1, 1, alpha * (1 - u) ** 1.25 * (0.6 if rb else 1.0)); c.set_line_width((2.2 + 5.5 * u) * s)
                c.move_to(px, py); c.line_to(xx, yy); c.stroke()
            px, py = xx, yy
    c.restore()


def flame():
    """The lighter flame's height for this drawing, 0.8 to 1.2."""
    T = CLOCK["T"] if CLOCK["shot"] is not None else 0.0
    return 1.0 + 0.30 * math.sin(T * 27) + 0.12 * math.sin(T * 53 + 1)       # v4b: it read as still at 6 fps


# ---- v6: a figure that is not one of the wrapped ones (a side drawing), tracked the same way ---------------------------
def tracked(who, draw, s=1.0):
    """draw(k) -> {"head": (x, y)}. Drawn; its head and its own outline are kept for bubbles and for the light."""
    def dr(k):
        c = k.c
        if CLOCK["shot"] is None or not MASKS[0]:
            return draw(k)
        c.push_group()
        o = draw(k)
        pat = c.pop_group(); c.set_source(pat); c.paint()
        try:
            m_ = cairo.ImageSurface(cairo.FORMAT_A8, 540, 960); mc = cairo.Context(m_)
            mc.set_matrix(c.get_matrix()); mc.set_source(pat); mc.paint()
            hx_, hy_ = c.user_to_device(*o["head"]); sc = abs(c.get_matrix().xx) * s
            CLOCK.setdefault("figs", []).append((m_, hx_, hy_, sc, who))
            CLOCK.setdefault("heads", {}).setdefault(who, (hx_, hy_, sc))
        except Exception:
            pass
        return o
    return dr
