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
        arms, face, look, rot, kn = lerp(HERO, SAG, u), "fade", (0.9, 0.2 + 0.4 * u), 0.05 * u, kneel(12 * u)
    elif t < 2.3:                                                              # the coat pulled straight: two tugs, a lift
        u = seg(t, 1.6, 2.3)
        tug = abs(math.sin(u * 2 * math.pi))
        arms, face, look, rot = lerp(SAG, TUG, min(1.0, u * 3)), "peer", (0.0, 0.8), 0.0
        kn = kneel(12 * (1 - u) + 6 * tug)
    else:                                                                      # and the pose again, as if
        u = ease(seg(t, 2.3, 2.6))
        arms, face, look, rot, kn = lerp(TUG, HERO, u), "proud", (-0.4, -0.2), 0.0, None
    p = P("pam_cat", 220, 730, 0.84, pose(arms, ("fist", "fist")), face, look)
    return draw(shot("1.3", cast=[], after=lambda k: m._pam(k, p, 1.0, breath(t), rot, kn), protect=()))


# ---- 1.4: the shadows peel off the cobbles and run up the street to a pair of taillights; she turns to follow -------
def a14(t):
    RUN = ((-34, 28, 34, -28), (34, -28, -34, 28))
    def thug(j, x0, y0, s0, seed):
        u = seg(t, 0.15 + 0.12 * j, 2.2 + 0.12 * j)
        if u <= 0:                                                             # still flat on the cobbles: a shadow
            return ("flat", (x0 - 10, y0 + 12, 0.20), dict(seed=seed))
        rise = seg(u, 0.0, 0.14)
        if rise < 1:                                                           # peeling up off them
            return ("thug%d" % (j + 1), (x0, y0, s0 * (0.3 + 0.7 * rise)), dict(pose=(-40, 40, 40, -40), seed=seed))
        v = ease(seg(u, 0.14, 1.0))                                            # running up the street, smaller and smaller
        step = RUN[int(t * 8) % 2]
        return ("thug%d" % (j + 1), (x0 + (262 - x0) * v, y0 - 150 * v - (5 if int(t * 8) % 2 else 0), s0 * (1 - 0.62 * v)),
                dict(pose=step, seed=seed))
    cast = []
    for j, (x0, y0, s0, seed) in enumerate(((300, 600, 0.26, 4111), (340, 590, 0.24, 4112))):
        who, a, kw = thug(j, x0, y0, s0, seed)
        if t < 2.3 + 0.12 * j:
            if who == "flat":
                cast.append(P("flat", *a, **kw))
            else:
                cast.append(P(who, a[0], a[1], a[2], kw["pose"], seed=kw["seed"]))
    u = ease(seg(t, 1.0, 1.8))                                                 # she turns to the taillights, then goes
    step = seg(t, 2.0, 2.8)
    arms = lerp(HERO, (-30, 40, 40, -40), u)
    p = P("pam_cat", 200 + 30 * step, 760 - 6 * math.sin(step * math.pi * 2), 0.84, pose(arms, ("fist", "fist")),
          "approve" if t < 1.0 else "peer", (0.6 * (1 - u) + 0.1 * u, -0.6 - 0.3 * u), rim=False)
    kn = kneel(6 * u, r=(10 * step, 8 * math.sin(step * math.pi * 2) ** 2, 1)) if step > 0 else kneel(6 * u)
    def after(k):
        m._pam(k, p, 1.0, breath(t), 0.04 * u, kn)
    return draw(shot("1.4", cast=cast, after=after, protect=()))


# ---- 2.1: on the fire escape, looking down; the car; the shadow at its rear window points back down the lane ---------
def a21(t):
    lean = 0.06 + 0.04 * ease(seg(t, 0.2, 1.0))                               # she leans over, further
    point = seg(t, 0.8, 1.2)                                                   # the shadow's arm comes up, points down the lane
    tp = (-30, 20, 30, -20) if point < 1 else (-30, 20, 110, 70)
    cast = [P("thug1", 262, 578, 0.20, tp, seed=4121)]
    look = (0.7, 0.9) if t < 1.2 else ((0.7 - 1.4 * seg(t, 1.2, 1.6)), 0.9)     # her eyes go where he points
    p = P("pam_cat", 130, 420, 0.64, pose(HERO, ("fist", "fist")), "peer", look)
    def after(k):
        m._pam(k, p, 1.0, breath(t), lean, kneel(8))
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
