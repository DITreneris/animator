"""PICK A SIDE (episode 14): the series' checks wired into the scene file (Tomas, /grill-me 24 Nov: "all the series'
checks, each proven on a planted fault"). ps_scenes.py v4 calls them on every layout and board frame; the motion tests
call them on every drawing. Each must catch its planted fault before it counts (validate()).

  limbs   at most two arms per character in a frame (the rigs' kit.arm calls, counted per owner; lesson: Pam's third arm)
  tails   every bubble's tail tip beside the mouth drawn in that frame (uz_check's rule, MOUTH band); the robot's beside
          the robot's too, its face point the visor's centre (its eyes); never down from above
  strays  every effect mark (speed, impact, crash lines) declared with its owner and drawn within reach of that owner
  map     every shot id once; the shots changed in this version drawn by the function named (lesson 109)
  don     Don the tallest in any frame he shares, and the widest (10 % allowed: Sofía's flared jacket, 87 vs 82 px)
  zones   every story prop declared (phones with a screen, the CV, the robot's card, the tape roll) and out of the
          apps' dead zones: the bottom quarter (y > 720) and the buttons (x > 470, y 380-860)

  python3 ps_checks.py validate   -> each check on its planted fault (must FAIL) and on the real shot (must pass)"""
import math
import types
import cairo
import kit
import acts_ob as ac
import uz_check as uz
from kit import Ctx

W, H = 540, 960
# standing height and width at scale 1.0 (measured 24 Nov from each rig, ARGB alpha bbox; The Offer's for the robot)
UNIT_H = {"don": 384, "sofia": 330, "pam": 332, "mom": 384, "robot": 310}
UNIT_W = {"don": 137, "sofia": 156, "pam": 133, "mom": 149, "robot": 132}
WIDE_OK = 1.10

OWNER = []                                                   # the character being drawn (a stack)
ARMS = {}                                                    # owner -> arms drawn this frame
MARKS = []                                                   # (owner, (x, y) in frame units)
PROTECT = []                                                 # (name, x0, y0, x1, y1) in frame units


def reset():
    ARMS.clear(); del MARKS[:]; del PROTECT[:]


# --- limbs: count the rigs' arms per owner ------------------------------------------------------------------------------
_depth = [0]


def _arm_wrap(f0):
    def arm(k, *a, **kw):
        _depth[0] += 1
        try:
            return f0(k, *a, **kw)
        finally:
            _depth[0] -= 1
            tg = k.c.get_target()                            # (the framing pass draws on a 4x4 scratch: not the frame)
            if _depth[0] == 0 and OWNER and getattr(tg, "get_width", lambda: 0)() == W:   # one arm per shoulder: a redraw (Pam's late hand) is the same arm
                sx, sy = k.c.user_to_device(a[0], a[1])
                ARMS.setdefault(OWNER[-1], set()).add((round(sx / 4), round(sy / 4)))
    arm._ps = True
    return arm


class _Kit(types.ModuleType):                                # an arm swapped into kit later (acts_ob.arms) is wrapped too
    def __setattr__(self, n, v):
        if n == "arm" and callable(v) and not getattr(v, "_ps", False):
            v = _arm_wrap(v)
        types.ModuleType.__setattr__(self, n, v)


def install():
    if type(kit) is types.ModuleType:
        kit.__class__ = _Kit
    for mod in (kit, ac):
        if not getattr(mod.arm, "_ps", False):
            mod.arm = _arm_wrap(mod.arm)


class owner:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        OWNER.append(self.name)

    def __exit__(self, *a):
        OWNER.pop()


def check_limbs():
    return ["LIMBS: %s has %d arms" % (o, len(n)) for o, n in ARMS.items() if len(n) > 2]


# --- strays: effect marks with their owner ------------------------------------------------------------------------------
def mark(c, who, x, y):
    MARKS.append((who, c.user_to_device(x, y)))


def check_strays(faces, reach=2.4):
    out = []
    for who, (x, y) in MARKS:
        if not (0 <= x <= W and 0 <= y <= H):
            continue
        f = faces.get(who)
        if f is None or not (abs(x - f[0]) <= reach * 2 * f[2] + 60 and f[1] - 3 * f[2] <= y <= f[1] + 9 * f[2]):
            out.append("STRAY: a mark of %s at (%d, %d) with %s not near" % (who, x, y, who))
    return out


# --- zones: declared story props ----------------------------------------------------------------------------------------
def protect(c, name, x0, y0, x1, y1):
    pts = [c.user_to_device(x, y) for x, y in ((x0, y0), (x1, y0), (x0, y1), (x1, y1))]
    PROTECT.append((name, min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts)))


def check_zones():
    out = []
    for name, x0, y0, x1, y1 in PROTECT:
        vx0, vy0, vx1, vy1 = max(x0, 0), max(y0, 0), min(x1, W), min(y1, H)
        if vx1 - vx0 < 4 or vy1 - vy0 < 4:
            continue
        if vy1 > uz.BOTTOM + 2:
            out.append("ZONE: %s in the bottom quarter (y %d-%d)" % (name, vy0, vy1))
        elif vx1 > uz.RAIL[0] + 2 and vy1 > uz.RAIL[1] and vy0 < uz.RAIL[2]:
            out.append("ZONE: %s under the right-hand buttons (x %d-%d, y %d-%d)" % (name, vx0, vx1, vy0, vy1))
    return out


# --- Don the tallest --------------------------------------------------------------------------------------------------
def check_don(cast):
    """cast: {name: scale} of everyone standing in one plane of the frame (a foreground layer is a plane of its own)."""
    if "don" not in cast:
        return []
    dh, dw = UNIT_H["don"] * cast["don"], UNIT_W["don"] * cast["don"]
    out = []
    for n, s_ in cast.items():
        if n == "don" or n not in UNIT_H:
            continue
        if UNIT_H[n] * s_ > dh + 1:
            out.append("DON RULE: %s taller than Don (%d vs %d)" % (n, UNIT_H[n] * s_, dh))
        if UNIT_W[n] * s_ > dw * WIDE_OK:
            out.append("DON RULE: %s wider than Don (%d vs %d)" % (n, UNIT_W[n] * s_, dw))
    return out


# --- tails --------------------------------------------------------------------------------------------------------------
class FillRec(cairo.Context):
    """keeps every filled path's points (device units) and every text box, for the tail check."""
    def __new__(cls, surf):
        return super().__new__(cls, surf)

    def __init__(self, surf):
        self.fills, self.texts = [], []

    def _keep(self):
        pts = []
        for kind, p in self.copy_path_flat():
            if p:
                pts.append(self.user_to_device(p[0], p[1]))
        if pts:
            self.fills.append(pts)

    def fill(self):
        self._keep(); return super().fill()

    def fill_preserve(self):
        self._keep(); return super().fill_preserve()

    def show_text(self, s):
        x, y = self.get_current_point(); e = self.text_extents(s)
        pts = [self.user_to_device(x + e.x_bearing + dx, y + e.y_bearing + dy) for dx in (0, e.width) for dy in (0, e.height)]
        self.texts.append((min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts)))
        return super().show_text(s)


LONG = 48                                                    # the tip at most this far past the bubble (lessons 174, 325: 10-20 px)


def tail_tip(fills, texts):
    """uz_check's way: the bubble's fill point farthest from its text box is the tail's tip (None: no tail)."""
    if not fills or not texts:
        return None
    box = (min(t[0] for t in texts) - 24, min(t[1] for t in texts) - 18, max(t[2] for t in texts) + 24, max(t[3] for t in texts) + 18)
    dist = lambda p: max(box[0] - p[0], 0, p[0] - box[2]) + max(box[1] - p[1], 0, p[1] - box[3])
    tip = max((p for f in fills for p in f), key=dist)
    if dist(tip) < 6:
        return None
    return tip


def check_tail(who, tip, face, said, length=0.0, form=None):
    if tip is None or face is None:
        return []
    if length > LONG:
        return ["TAIL of %s too long: %r reaches %d px past its bubble" % (who, said, length)]
    x, y, r = face
    dy, dx = (tip[1] - y) / r, abs(tip[0] - x) / r
    if who == "robot" and form == "T":                       # canon (bc_sb "T"): down onto its antenna, nowhere else on top
        if not (-2.6 <= dy <= -0.8 and dx <= 0.6):
            return ["TAIL of the robot not on its antenna: %r tip %s, visor %s" % (said, tuple(round(q) for q in tip),
                                                                                 (round(x), round(y), round(r)))]
        return []
    if not (uz.MOUTH[0] <= dy <= uz.MOUTH[1] and dx <= uz.MOUTH[2]):
        where = "above the mouth (from above, hair)" if dy < uz.MOUTH[0] else ("below the mouth" if dy > uz.MOUTH[1] else "too far to the side")
        return ["TAIL %s of %s: %r tip %s, face %s" % (where, who, said, tuple(round(q) for q in tip), (round(x), round(y), round(r)))]
    return []


# --- the drawing map ----------------------------------------------------------------------------------------------------
def check_map(shots, expect):
    out, seen = [], {}
    for sh in shots:
        if sh["id"] in seen:
            out.append("MAP: shot %s is defined twice; the later entry would win (lesson 109)" % sh["id"])
        seen[sh["id"]] = sh
    for sid, fn in expect.items():
        sh = seen.get(sid)
        got = getattr(sh.get("cast") or sh.get("draw"), "__name__", "?") if sh else "missing"
        if got != fn:
            out.append("MAP: %s is drawn by %s, expected %s" % (sid, got, fn))
    return out


# --- wiring into ps_scenes (opt-in: only `ps_scenes.py check` and the motion tests call install_scene) ---------------
CAST = {}                                                    # name -> scale drawn this frame (one plane)
PROPS = [("sp", "cv_coo", "the CV"), ("rp", "phone_screen", "a phone screen"), ("pss", "pam_phone", "Pam's phone"),
         ("pss", "phone_close", "the phone close-up"), ("pm", "phone_lit", "the lit phone"), ("dp", "tape_roll", "the tape roll"),
         ("pss", "robot_card", "the robot's card"), ("cps", "phone_on_table", "the phone on the table")]


def _bbox_group(c, f, name):
    """draw f inside a group, paint it back, and declare its inked box (device units) as a story prop."""
    import numpy as np
    c.push_group()
    try:
        r = f()
    finally:
        pat = c.pop_group()
    m = c.get_matrix()
    tmp = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); t = cairo.Context(tmp); t.set_matrix(m)
    t.set_source(pat); t.paint(); tmp.flush()
    a = np.ndarray((H, W, 4), np.uint8, tmp.get_data())[..., 3]
    ys, xs = np.nonzero(a > 40)
    if len(xs) and (name, xs.min(), ys.min(), xs.max(), ys.max()) not in PROTECT:   # the bare pass (covered()) draws it again
        PROTECT.append((name, xs.min(), ys.min(), xs.max(), ys.max()))
    c.set_source(pat); c.paint()
    return r


NO_DECLARE = [False]


def install_scene(ps):
    install()
    if getattr(ps, "_checked", False):
        return
    ps._checked = True
    mods = dict(sp=ps.sp, rp=ps.rp, pss=ps.pss, pm=ps.pm, dp=ps.dp, cps=ps.cps)
    for m, fn, name in PROPS:
        f0 = getattr(mods[m], fn)
        def prop(k, *a, _f0=f0, _name=name, **kw):
            if NO_DECLARE[0]:                                 # a full-frame insert declares its own story rect instead
                return _f0(k, *a, **kw)
            if _name == "Pam's phone" and not kw.get("lit", a[3] if len(a) > 3 else False):
                return _f0(k, *a, **kw)                      # dark, face up on the counter: set dressing until it lights (5.7)
            return _bbox_group(k.c, lambda: _f0(k, *a, **kw), _name)
        setattr(mods[m], fn, prop)
    for who in ("don", "robot", "sofia", "pam", "mom"):
        f0 = getattr(ps, who)
        def person(k, *a, _f0=f0, _who=who, **kw):
            CAST[_who] = ps.SC[_who]
            with owner(_who):
                return _f0(k, *a, **kw)
        setattr(ps, who, person)
    import fs_animatic as an
    sp0 = an.speech
    def speech(c, k, text, head, others, *a, **kw):
        rc = FillRec(c.get_target()); rc.set_matrix(c.get_matrix())
        box = sp0(rc, Ctx(rc, k.boil), text, head, others, *a, **kw)
        who = min(ps.LAST[0], key=lambda n: abs(ps.LAST[0][n][0] - head[0]) + abs(ps.LAST[0][n][1] - head[1]))
        tip = tail_tip(rc.fills, rc.texts)
        ln = 0.0 if tip is None else math.hypot(max(box[0] - tip[0], 0, tip[0] - box[2]), max(box[1] - tip[1], 0, tip[1] - box[3]))
        TAILS.append((who, tip, ps.LAST[0][who], text, ln))   # ln: how far the tip reaches past the bubble's box
        return box
    an.speech = speech


TAILS = []


def frame_checks(ps, heads):
    """the frame just rendered: -> faults."""
    out = check_limbs() + check_zones() + check_don(dict(CAST)) + check_strays(heads)
    if getattr(ps, "FIX_V4", [False])[0]:                    # board v3: bc_sb's bubbles (their tips as drawn)
        for b in ps.BUBBLES_V4:
            tip, box = b["tip"], b["box"]
            ln = 0.0 if tip is None else math.hypot(max(box[0] - tip[0], 0, tip[0] - box[2]), max(box[1] - tip[1], 0, tip[1] - box[3]))
            out += check_tail(b["who"], tip, b["face"], b["text"], ln, b["form"])
        return out
    for who, tip, face, said, ln in TAILS:
        out += check_tail(who, tip, face, said, ln)
    return out


def begin():
    reset(); CAST.clear(); del TAILS[:]


# --- validation on planted faults ---------------------------------------------------------------------------------------
def validate():
    import ps_scenes as ps
    import don_ps as dp
    res = []

    def case(name, planted, real):
        ok = bool(planted) and not real
        res.append(ok)
        print("%-7s %s | planted: %s | real: %s" % (name, "OK " if ok else "BAD", (planted[:1] or ["(nothing caught)"])[0][:90],
                                                     real[:1] or "pass"))

    # limbs: Don drawn twice under one owner (Pam's third arm, in kind) vs Don once
    install()
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); k = kit.Ctx(cairo.Context(s), 0)
    reset()
    with owner("don"):
        dp.don(k, 200, 800, 0.6, "stand", "neutral", (0, 0)); dp.don(k, 210, 800, 0.6, "push", "neutral", (0, 0))
    planted = check_limbs()
    reset()
    with owner("don"):
        dp.don(k, 200, 800, 0.6, "stand", "neutral", (0, 0))
    case("limbs", planted, check_limbs())
    # tails: a tip on the crown (from above) vs beside the mouth; the robot's on its antenna vs beside the visor
    face = (270, 400, 70)
    case("tails", check_tail("don", (270, 320), face, "x") + check_tail("robot", (270, 320), face, "y") +
         check_tail("don", (340, 440), face, "x", length=180),
         check_tail("don", (340, 440), face, "x", length=18) + check_tail("robot", (350, 450), face, "y", length=18))
    # strays: a crash line far from Don vs beside him
    reset(); c = cairo.Context(s)
    mark(c, "don", 500, 100); planted = check_strays({"don": (150, 600, 40)})
    reset(); mark(c, "don", 190, 560)
    case("strays", planted, check_strays({"don": (150, 600, 40)}))
    # map: a duplicated shot vs the scene file as it is
    dup = list(ps.SHOTS) + [ps.S("2.1", ps.S2, {}, ps.cast_trio())]
    case("map", check_map(dup, ps.EXPECT), check_map(ps.SHOTS, ps.EXPECT))
    # don: The Offer's Client (458 high at scale 1) at 0.52 beside Don vs the office cast at its scales
    UNIT_H["client"], UNIT_W["client"] = 458, 150
    planted = check_don({"don": 0.60, "client": 0.52})
    del UNIT_H["client"], UNIT_W["client"]
    case("don", planted, check_don(dict(ps.SC)))
    # zones: Sofía's CV moved under the buttons vs 5.5 as staged
    reset(); c = cairo.Context(s)
    protect(c, "the CV", 480, 500, 530, 560); planted = check_zones()
    reset(); protect(c, "the CV", 200, 400, 300, 480)
    case("zones", planted, check_zones())
    return all(res)


if __name__ == "__main__":
    import sys
    if sys.argv[1:] == ["validate"]:
        sys.exit(0 if validate() else 1)
