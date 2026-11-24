"""OFFICE NOIR 4: the final animation of the shots the rough held still (24 Nov, Tomas: "max quality"). Each shot is a
function of time in seconds, so it draws at any rate: 24 drawings a second here (the rough's motion tests drew 12).
Built on on4_motion's helpers (draw, shot, pose, lerp, ease, _pam with knees). Nothing earlier changes.

  python3 on4_anim.py 1.3 1.4 2.1        -> /tmp/anim/<shot>/NNN.png and a stills sheet per group"""
import math
import os
import sys
import cairo
import on4_motion as m
import on4_scenes as sc
import on4_cast as oc
import on4_street as st
from on4_scenes import P

DPS = 24
draw, shot, pose, lerp, ease = m.draw, m.shot, m.pose, m.lerp, m.ease
HERO = m.HERO


def seg(t, a, b):
    """0..1 across [a, b], clamped"""
    return max(0.0, min(1.0, (t - a) / float(b - a)))


def breath(t, rate=0.28):
    """a body's breathing as _pam's vertical scale: a slow rise of the chest, never still (not the knees: a few units
    of knee bend bowed her legs)"""
    return 1.0 + 0.007 * math.sin(2 * math.pi * rate * t)


def weight(drop, d=1.0):
    """the body over bent knees (review of the stills: "a squat in place"): the hips down, the trunk tipped forward a
    little with them, about the feet. Returns _pam's rot for a knee drop."""
    return d * 0.0045 * drop


def asym(arms, a=6):
    """the same pose, not mirrored: the screen-left arm a little higher, the right a little out"""
    return (arms[0] + a, arms[1] - a * 0.5, arms[2] + a * 0.7, arms[3] + a)


def kneel(drop, **kw):
    """_pam's knee dict, or None when the knees are straight"""
    return dict(drop=drop, **kw) if drop > 2.5 or kw else None


# ---- 1.3: the pose holds; her eyes follow Sofia out; the pose sags; she pulls her coat straight ------------------------
def a13(t):
    TUG = oc.pm.ik(-1, -34, oc.BT + 150) + oc.pm.ik(1, 34, oc.BT + 150)       # both hands at the coat's hem
    SAG = (-6, 0, 6, 0)
    look_x = 0.2 + 0.7 * ease(seg(t, 0.0, 0.7))                                # Sofia goes out at screen right
    if t < 0.9:                                                                # held: the hero pose, waiting to be thanked
        arms, face, look, rot, kn = HERO, "proud", (look_x, 0.1), 0.0, None
    elif t < 1.6:                                                              # it sags
        u = ease(seg(t, 0.9, 1.6))
        arms, face, look, rot, kn = asym(lerp(HERO, SAG, u), 8 * u), "fade", (0.9, 0.2 + 0.4 * u), 0.05 * u + weight(14 * u), kneel(14 * u)
    elif t < 2.3:                                                              # the coat pulled straight: two tugs, a lift
        u = seg(t, 1.6, 2.3)
        tug = abs(math.sin(u * 2 * math.pi))
        arms, face, look = asym(lerp(SAG, TUG, min(1.0, u * 3)), 5), "peer", (0.0, 0.8)
        kn = kneel(14 * (1 - u) + 8 * tug); rot = weight(14 * (1 - u) + 8 * tug) - 0.03 * tug
    else:                                                                      # and the pose again, as if
        u = ease(seg(t, 2.3, 2.6))
        arms, face, look, rot, kn = lerp(TUG, HERO, u), "proud", (-0.4, -0.2), 0.0, None
    p = P("pam_cat", 220, 730, 0.84, pose(arms, ("fist", "fist")), face, look, rim=True)
    return draw(shot("1.3", cast=[], after=lambda k: m._pam(k, p, 1.0, breath(t), rot, kn), protect=()))


# ---- 1.4: the shadows peel off the cobbles and run up the street to a pair of taillights; she turns to follow -------
def a14(t):
    RUN = ((-38, 30, 38, -30), (-10, 8, 10, -8), (38, -30, -38, 30), (10, -8, -10, 8))   # four drawings a stride
    YV, YE = 452, 540                                                          # the street's vanishing line; where they reach
    def contact(k, x, y, s_):
        c = k.c
        c.save(); c.translate(x, y + 2); c.scale(62 * s_ / 0.26, 7 * s_ / 0.26); c.new_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        c.set_source_rgba(0, 0, 0, 0.45); c.fill()
    def thug(j, x0, y0, s0, seed):
        u = seg(t, 0.15 + 0.12 * j, 2.2 + 0.12 * j)
        if u <= 0:                                                             # still flat on the cobbles: a shadow
            return ("flat", (x0 - 10, y0 + 12, 0.20), dict(seed=seed))
        rise = seg(u, 0.0, 0.14)
        if rise < 1:                                                           # peeling up off them
            return ("thug%d" % (j + 1), (x0, y0, s0 * (0.3 + 0.7 * rise)), dict(pose=(-40, 40, 40, -40), seed=seed))
        v = ease(seg(u, 0.14, 1.0))                                            # running up the street: feet on the cobbles,
        y = y0 + (YE - y0) * v                                                 # the size from the distance (the feet's height
        sc_ = s0 * (y - YV) / float(y0 - YV)                                   # over the vanishing line)
        x = x0 + (262 - x0) * (y0 - y) / float(y0 - YE)
        ph = int(t * 12 + j * 2) % 4
        return ("thug%d" % (j + 1), (x, y - (4 * sc_ / s0 if ph in (1, 3) else 0), sc_), dict(pose=RUN[ph], seed=seed))
    cast = []; shadows = []
    for j, (x0, y0, s0, seed) in enumerate(((300, 600, 0.26, 4111), (340, 590, 0.24, 4112))):
        who, a, kw = thug(j, x0, y0, s0, seed)
        if t < 2.3 + 0.12 * j:
            if who == "flat":
                cast.append(P("flat", *a, **kw))
            else:
                cast.append(P(who, a[0], a[1], a[2], kw["pose"], seed=kw["seed"])); shadows.append((a[0], a[1], a[2]))
    u = ease(seg(t, 1.0, 1.8))                                                 # she turns to the taillights, then goes
    step = seg(t, 2.0, 2.8)
    arms = asym(lerp(HERO, (-30, 40, 40, -40), u), 6 * u)
    p = P("pam_cat", 200 + 30 * step, 760 - 6 * math.sin(step * math.pi * 2), 0.84, pose(arms, ("fist", "fist")),
          "approve" if t < 1.0 else "peer", (0.6 * (1 - u) + 0.1 * u, -0.6 - 0.3 * u), rim=True)
    d = 8 * u
    kn = kneel(d, r=(10 * step, 8 * math.sin(step * math.pi * 2) ** 2, 1)) if step > 0 else kneel(d)
    def before(k):
        for x, y, s_ in shadows:
            contact(k, x, y, s_)
    def after(k):
        m._pam(k, p, 1.0, breath(t), 0.04 * u + weight(d), kn)
    return draw(shot("1.4", cast=cast, before=before, after=after, protect=()))


# ---- 2.1: on the fire escape, looking down; the car; the shadow at its rear window points back down the lane ---------
def a21(t):
    lean = 0.06 + 0.04 * ease(seg(t, 0.2, 1.0))                               # she leans over, further
    point = seg(t, 0.8, 1.2)                                                   # the shadow's arm comes up, points down the lane
    tp = (-30, 20, 30, -20) if point < 1 else (-30, 20, 110, 70)
    cast = [P("thug1", 262, 578, 0.20, tp, seed=4121)]
    look = (0.7, 0.9) if t < 1.2 else ((0.7 - 1.4 * seg(t, 1.2, 1.6)), 0.9)     # her eyes go where he points
    RAIL = oc.pm.ik(-1, -30, oc.BT + 60) + oc.pm.ik(1, 86, -70)               # her right hand on the rail, the left on her hip
    p = P("pam_cat", 186, 420, 0.64, pose(asym(RAIL, 4), ("fist", "grab")), "peer", look, rim=True)
    def after(k):
        m._pam(k, p, 1.0, breath(t), lean + weight(10), kneel(10))
        sc.railing(k, 380)
    z = 1.0 + 0.22 * ease(seg(t, 0.0, 2.2))                                    # a slow push in, down onto the car
    return draw(shot("2.1", cam=(270 - 40 * (z - 1) / 0.22, 480 + 60 * (z - 1) / 0.22, z), cast=cast, after=after, protect=()))


SHOTS = {"1.3": (a13, 2.91), "1.4": (a14, 2.8), "2.1": (a21, 2.2)}


def frames(sid):
    f, dur = SHOTS[sid]
    n = int(round(dur * DPS))
    return [f(i / float(DPS)) for i in range(n)]


def build(sid):
    d = "/tmp/anim/%s" % sid
    os.makedirs(d, exist_ok=True)
    for x in os.listdir(d):
        os.remove(os.path.join(d, x))
    fr = frames(sid)
    for i, s in enumerate(fr):
        s.write_to_png(os.path.join(d, "%03d.png" % i))
    return d, len(fr)


if __name__ == "__main__":
    for sid in sys.argv[1:]:
        print(sid, build(sid))
