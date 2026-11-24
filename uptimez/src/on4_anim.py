"""OFFICE NOIR 4: the final animation of the shots the rough held still (24 Nov, Tomas: "max quality"). Each shot is a
function of time in seconds, so it draws at any rate: 24 drawings a second here (the rough's motion tests drew 12).
Built on on4_motion's helpers (draw, shot, pose, lerp, ease, _pam with knees). Nothing earlier changes.

  python3 on4_anim.py 1.3 1.4 2.1        -> /tmp/anim/<shot>/NNN.png and a stills sheet per group"""
import math
import os
import sys
import cairo
import kit
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


KNEE_K = 0.6                                               # (review: "the knees bend into an X") every knee bend 40 % less


def kneel(drop, **kw):
    """_pam's knee dict, or None when the knees are straight"""
    if m.LAW[0] and not kw and drop <= 20:                 # (24 Nov) no squat with both knees out (a diamond); and (Tomas: "she sways like a drunk") no shifting about either:
        return None                                        # standing, she stands; she moves when she walks (catwalk)
    kw = {k_: (v[0], v[1] * KNEE_K, v[2]) for k_, v in kw.items()}
    drop = drop * KNEE_K * (0.5 if m.LAW[0] else 1.0)
    return dict(drop=drop, **kw) if drop > 2.5 or kw else None


def relax(u):
    """(24 Nov, the review of 1.4: both knees bent, the trunk not answering) her weight on her screen-left leg, straight;
    the other loose: its heel up a little, its knee out, the foot a little aside. u 0..1. No squat."""
    return dict(drop=2.0 * u, r=(9.0 * u, 10.0 * u, 1)) if u > 0.05 else None


def catwalk(ph, away=False):
    """(24 Nov, Tomas: "her walk lacks a cat's manners"; v2 after the review) one stride, ph 0..1 (two steps), from the
    front. Each foot set down on one line under her middle, the free foot low and round (a glide, not a march); the
    hips swing out over the standing leg; the shoulders turn the other way (the figure cut at the belt); the head tips
    back again and stays level; one glove on her hip, the other arm loose with a limp wrist; a held beat as each foot
    lands; the hunting face. Returns (arms, gest, knee, rot, dx, kw) for pam_ and P (kw: tilt, twist, hunt)."""
    h = (ph % 1.0) * 2.0
    left_stands = h < 1.0
    u0 = h % 1.0
    u = 0.5 - 0.5 * math.cos(math.pi * min(1.0, max(0.0, (u0 - 0.12) / 0.76)))   # held at each contact, quick through the pass
    sw = math.sin(math.pi * u)
    side = -1 if left_stands else 1
    s_ = side * math.sin(math.pi * min(1.0, u * 1.1 + 0.08))                    # the hips out over the standing leg
    LINE = 14
    free_dx = (-side) * (-LINE) * (0.2 + 0.8 * u) + (-side) * 14 * (1 - u) * sw
    stand = (side * -LINE, 0.0, side)
    free = (free_dx, 7.0 * sw, -side)                        # low: it slides
    kn = dict(drop=0.5 + 1.2 * abs(math.cos(math.pi * u)), l=stand if left_stands else free, r=free if left_stands else stand)
    a = math.cos(math.pi * h)
    if away:                                               # the second walk (Tomas: she may walk twice, the walk a little different): leaving, her back to us: both arms loose, the hips wider, no tilt of the head
        arms = oc.pm.ik(-1, -34 + 9 * a, oc.BT + 134 - 3 * abs(a)) + oc.pm.ik(1, 34 + 9 * a, oc.BT + 134 - 3 * abs(a))
        return arms, ("relax_s", "relax_s"), kn, 0.085 * s_, 19.0 * s_, dict(twist=-0.12 * s_, behind=True)
    arms = tuple(HERO[:2]) + oc.pm.ik(1, 34 + 9 * a, oc.BT + 132 - 3 * abs(a))   # screen-left glove on her hip; the other swings, loose
    return arms, ("fist", "relax_s"), kn, 0.075 * s_, 16.0 * s_, dict(tilt=-0.03 * s_, twist=-0.10 * s_, hunt=0.5)


def pam_(k, p, sy=1.0, rot=0.0, kn=None):
    """her figure over a contact shadow on the ground under her boots (review: she floats)"""
    who, a, kw = p
    c = k.c
    c.save(); c.translate(a[0], a[1] + 2 * a[2]); c.scale(64 * a[2], 9 * a[2]); c.new_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
    c.set_source_rgba(0, 0, 0, 0.5); c.fill()
    return m._pam(k, p, 1.0, sy, rot, kn)


def card(k, t, x0=300, x1=372, y=630, period=0.9):
    """the game goes on: a card dealt across the table, again and again"""
    u = (t % period) / period
    if u > 0.6:
        return
    v = ease(u / 0.6)
    c = k.c
    c.save(); c.translate(x0 + (x1 - x0) * v, y - 10 * math.sin(v * math.pi)); c.rotate(0.3 * v)
    c.rectangle(-9, -6, 18, 12); c.set_source_rgb(0.96, 0.96, 0.94); c.fill_preserve(); c.set_source_rgb(0.1, 0.1, 0.1); c.set_line_width(1); c.stroke()
    c.restore()


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
        if m.LAW[0]:
            rot, kn = 0.0, None                            # she stands firm: only her arms and face let down
    elif t < 2.3:                                                              # the coat pulled straight: two tugs, a lift
        u = seg(t, 1.6, 2.3)
        tug = abs(math.sin(u * 2 * math.pi))
        arms, face, look = asym(lerp(SAG, TUG, min(1.0, u * 3)), 5), "peer", (0.0, 0.8)
        kn = kneel(14 * (1 - u) + 8 * tug); rot = weight(14 * (1 - u) + 8 * tug) - 0.03 * tug
        if m.LAW[0]:
            kn = None; rot = 0.0
    else:                                                                      # and the pose again, as if
        u = ease(seg(t, 2.3, 2.6))
        arms, face, look, rot, kn = lerp(TUG, HERO, u), "proud", (-0.4, -0.2), 0.0, None
    p = P("pam_cat", 220, 730, 0.84, pose(arms, ("fist", "fist")), face, look, rim=True)
    return draw(shot("1.3", cast=[], after=lambda k: pam_(k, p, breath(t), rot, kn), protect=()))


# ---- 1.4: the shadows peel off the cobbles and run up the street to a pair of taillights; she turns to follow -------
def a14(t):
    RUN = ((-38, 30, 38, -30), (-10, 8, 10, -8), (38, -30, -38, 30), (10, -8, -10, 8))   # four drawings a stride
    YV, YE = 452, 540                                                          # the street's vanishing line; where they reach
    def contact(k, x, y, s_):
        c = k.c
        c.save(); c.translate(x, y + 2); c.scale(62 * s_ / 0.26, 7 * s_ / 0.26); c.new_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        c.set_source_rgba(0, 0, 0, 0.45); c.fill()
    def thug(j, x0, y0, s0, seed):
        u = seg(t, 0.15 + (0.30 if m.LAW[0] else 0.12) * j, 2.2 + (0.30 if m.LAW[0] else 0.12) * j)   # (review) the second man a good step behind: in file, not one double shape
        if u <= 0:                                                             # still flat on the cobbles: a shadow
            return ("flat", (x0 - 10, y0 + 12, 0.20), dict(seed=seed))
        rise = seg(u, 0.0, 0.14)
        if rise < 1 and m.LAW[0]:                                              # up off the cobbles, already the man he is
            return ("guard_sil", (x0, y0, (s0 / 0.26) * 0.30 * (0.35 + 0.65 * rise)), dict(seed=1600 + j * 40, flip=(j == 1), step=0.0, dark=0.90))
        if rise < 1:                                                           # peeling up off them
            return ("thug%d" % (j + 1), (x0, y0, s0 * (0.3 + 0.7 * rise)), dict(pose=(-40, 40, 40, -40), seed=seed))
        if m.LAW[0]:                                                           # (24 Nov, Tomas: "where do they go? they miss the lane") the two are Dad's bodyguards, dark;
            v = ease(seg(u, 0.14, 0.86)); w = seg(u, 0.86, 1.0)                # up the street INTO the arch at the bend (the taillights are in it),
            y = y0 + (566 - y0) * v                                            # then round it to the left, behind the wall's edge: gone, not popped
            sg = (s0 / 0.26) * 0.30 * (y - YV) / float(y0 - YV)                # a guard's size by the same distance: her 0.84 at y 760 is 0.40 at y 600; x 0.903 / 1.203 = 0.30
            x = x0 + (226 - x0) * v - 78 * w
            import on4_cross as xc
            ph_ = u * 30.0 + j * 1.3                                           # a step you can see at this size: the leg well up, the arms swinging against the legs, the body rising on each
            sw = 22 * math.sin(ph_)
            return ("guard_sil", (x, y - 3.0 * abs(math.sin(ph_)) * sg / 0.30, sg),
                    dict(seed=1600 + j * 40, flip=(j == 1), step=ph_, lift=44.0, dark=0.88 - 0.20 * v,
                         pose=xc.garm((-78, xc.co.HIP + 40 + sw), (78, xc.co.HIP + 40 - sw)), clip_x=st.A_BEND_X + 1 if v > 0.8 else None))
        v = ease(seg(u, 0.14, 1.0))                                            # running up the street: feet on the cobbles,
        y = y0 + (YE - y0) * v                                                 # the size from the distance (the feet's height
        sc_ = s0 * (y - YV) / float(y0 - YV)                                   # over the vanishing line)
        x = x0 + (262 - x0) * (y0 - y) / float(y0 - YE)
        ph = int(t * 12 + j * 2) % 4
        return ("thug%d" % (j + 1), (x, y - (4 * sc_ / s0 if ph in (1, 3) else 0), sc_), dict(pose=RUN[ph], seed=seed))
    cast = []; shadows = []
    for j, (x0, y0, s0, seed) in enumerate(((300, 600, 0.26, 4111), (340, 590, 0.24, 4112))):
        who, a, kw = thug(j, x0, y0, s0, seed)
        if who == "guard_sil":
            cast.append(P(who, *a, **kw)); shadows.append((a[0], a[1], a[2] * 0.6) if kw.get("clip_x") is None else (-999, 0, 0.01))
        elif t < 2.3 + 0.12 * j:
            if who == "flat":
                cast.append(P("flat", *a, **kw))
            else:
                cast.append(P(who, a[0], a[1], a[2], kw["pose"], seed=kw["seed"])); shadows.append((a[0], a[1], a[2]))
    u = ease(seg(t, 1.0, 1.8))                                                 # she turns to the taillights, then goes
    step = seg(t, 2.0, 2.8)
    arms = asym(lerp(HERO, (-30, 40, 40, -40), u), 6 * u)
    p = P("pam_cat", (150 if m.LAW[0] else 200) + 30 * step, 760 - 6 * math.sin(step * math.pi * 2), 0.84, pose(arms, ("fist", "fist")),
          "approve" if t < 1.0 else "peer", (0.6 * (1 - u) + 0.1 * u, -0.6 - 0.3 * u), rim=True)
    d = 8 * u
    kn = kneel(d, r=(10 * step, 8 * math.sin(step * math.pi * 2) ** 2, 1)) if step > 0 else kneel(d)
    rot_ = 0.04 * u + weight(d)
    if m.LAW[0]:                                                               # (Tomas: "where does she go?"; the review) she does not walk on the spot: she stays, her weight goes onto one leg, she turns to the arch and leans after them
        if t < 1.15:                                       # she stands firm and watches them go: only her eyes move
            p = P("pam_cat", 128, 760, 0.84, pose(HERO, ("fist", "fist")), "approve" if t < 0.9 else "peer", (0.6 + 0.3 * seg(t, 0.3, 0.9), -0.6), rim=True,
                  hunt=0.5 * seg(t, 0.9, 1.1))
            kn = None; rot_ = 0.0
        else:                                              # (Tomas: "she must come from far, nearer, to the camera") and she walks: toward us down the lane, her cat's walk,
            w = ease((t - 1.15) / 1.65)                    # bigger with every step, while they go into the arch behind her
            yy = 760 + 180 * w; ss = 0.84 * (yy - YV) / float(760 - YV)
            ar_, ge_, kn, rot_, dx_, kw_ = catwalk((t - 1.15) / 0.92)
            p = P("pam_cat", 128 + 130 * w + dx_ * ss, yy, ss, pose(ar_, ge_), "peer", (0.0, 0.1), rim=True, **kw_)
    def before(k):
        for x, y, s_ in shadows:
            contact(k, x, y, s_)
    def after(k):
        pam_(k, p, breath(t), rot_, kn)
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
        pam_(k, p, breath(t), lean + weight(10), kneel(10))
        sc.railing(k, 380)
    z = 1.0 + 0.22 * ease(seg(t, 0.0, 2.2))                                    # a slow push in, down onto the car
    if m.LAW[0]:                                           # (24 Nov, Tomas: "what does the car do? should it not come nearer?") the limousine drives up the lane to her wall and
        z = max(z, 1.002)                                  # never the exact wide camera: its light (with the parked car's red tail glow) came on for the first drawing only
        import on4_car as car_                             # stops under her; Dad's two men walk beside it; she drops behind the rail and her eyes follow it in
        import on4_cross as xc
        u = 0.06 + 0.94 * (1 - (1 - seg(t, 0.0, 1.7)) ** 2)   # it slows as it comes (already moving on the first drawing)
        cy = 576 + (735 - 576) * u
        cs = 0.36 * (105 + 285 * (cy - 576) / 384.0) / 105.0
        cx = 302 + 23 * (cy - 576) / 384.0 - 14 * u
        nose = -0.02 * math.sin(math.pi * seg(t, 1.5, 1.9))                    # it stops: the nose dips and comes back
        duck = ease(seg(t, 0.3, 0.75))                       # v2 (the review): down on her haunches: hips down and back, the trunk forward
        turn = ease(seg(t, 0.7, 1.0))                        # her head comes round to it last
        hunt = 0.6 * ease(seg(t, 1.8, 2.1))                  # and at the end her eyes narrow; a small smile
        D = 44 * duck
        look = (0.3 + 0.6 * turn - 0.2 * u * turn, 0.5 + 0.45 * turn)
        ARMS = oc.pm.ik(-1, -58, -126 - D) + lerp(oc.pm.ik(1, 62, -126), oc.pm.ik(1, 40, -84 - D), duck)   # one glove stays on the rail, the other comes down to her knee
        p = P("pam_cat", 186, 420, 0.64, pose(ARMS, ("grab", "relax_s" if duck > 0.5 else "grab")), "peer", look, rim=True, tilt=0.10 * turn, hunt=hunt)
        gd = [(-1, 10.0, 11.0, 1.70), (1, -16.0, 9.2, 1.86)]                    # each of Dad's men: side, how far ahead of the car's nose, his own pace, when he stops
        gp = []
        for j, (sgn, ahead, pace, stop) in enumerate(gd):
            gu = 0.06 + 0.94 * (1 - (1 - seg(t, 0.0, stop)) ** 2)              # his own walk, not the car's
            gy = 576 + (735 - 576) * gu + ahead * cs
            gs_ = 0.27 * 0.36 * (105 + 285 * (gy - 576) / 384.0) / 105.0
            gx = 302 + 23 * (gy - 576) / 384.0 - 14 * gu + sgn * (104 * cs + 16)
            tn = math.sin((t - 1.9) * 9.0) * seg(t, 1.9, 2.0) if j == 0 else 0.0     # stopped, the first looks up the street and down it (never up at her)
            gp.append((gx, gy, gs_, j == 1, (t * pace + j * 1.6) if t < stop else None, tn))
        def before(k):
            c = k.c
            for x0, x1 in ((0, 250), (540, 330)):            # night: the lane's walls darker toward the frame's edges
                g = cairo.LinearGradient(x0, 0, x1, 0)
                g.add_color_stop_rgba(0, 0, 0, 0, 0.62); g.add_color_stop_rgba(1, 0, 0, 0, 0.0)
                c.set_source(g); c.rectangle(min(x0, x1), 420, abs(x1 - x0), 540); c.fill()
            g = cairo.LinearGradient(0, 760, 0, 960); g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, 0.55)
            c.set_source(g); c.rectangle(0, 760, 540, 200); c.fill()
            for sgn in (-1, 1):                              # the headlights: two beams down the cobbles
                lx = cx + sgn * 62 * cs; ly_ = cy - 44 * cs; L = 190 * cs + 60
                g = cairo.LinearGradient(0, ly_, 0, ly_ + L)
                g.add_color_stop_rgba(0, 1, 1, 0.94, 0.50); g.add_color_stop_rgba(1, 1, 1, 0.94, 0.0)
                c.new_path(); c.move_to(lx - 10 * cs, ly_ + 30 * cs); c.line_to(lx + 10 * cs, ly_ + 30 * cs)
                c.line_to(lx + sgn * 30 * cs + 46 * cs, ly_ + L); c.line_to(lx + sgn * 30 * cs - 46 * cs, ly_ + L); c.close_path(); c.set_source(g); c.fill()
            for gx, gy, gs_, fl, st__, tn in gp:             # their long shadows down the lane toward us, from the lit house behind them
                L = 420 * gs_; out = (gx - cx) * 0.22
                g = cairo.LinearGradient(0, gy, 0, gy + L); g.add_color_stop_rgba(0, 0, 0, 0, 0.55); g.add_color_stop_rgba(1, 0, 0, 0, 0.0)
                c.new_path(); c.move_to(gx - 70 * gs_, gy + 2); c.line_to(gx + 70 * gs_, gy + 2)
                c.line_to(gx + out + 110 * gs_, gy + L); c.line_to(gx + out - 110 * gs_, gy + L); c.close_path(); c.set_source(g); c.fill()
            c.save(); c.translate(cx, cy); c.rotate(nose); c.translate(-cx, -cy)
            car_.reflect(k, lambda: car_.front(k, cx, cy, cs), cy, 0.25, 20)
            c.restore()
            gs0 = xc.GS
            try:
                for j, (gx, gy, gs_, fl, st__, tn) in sorted(enumerate(gp), key=lambda q: q[1][1]):
                    xc.GS = gs_
                    xc.guard(k, gx, gy + 4, xc.G_WALK, fl, 1600 + j * 40, 0.0, st__, tn)
            finally:
                xc.GS = gs0
        def after2(k):
            was = sc.RIM_A[0]; sc.RIM_A[0] = 0.35             # a thinner rim: she read as a sticker
            try:
                pam_(k, p, breath(t), 0.05 + 0.13 * duck, dict(drop=D, l=(-10 * duck, 0, 1), r=(4 * duck, 0, 1)) if duck > 0.03 else None)
            finally:
                sc.RIM_A[0] = was
            sc.railing(k, 380)
            c = k.c                                          # the frame's corners
            g = cairo.RadialGradient(270, 500, 300, 270, 500, 620); g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, 0.4)
            c.set_source(g); c.rectangle(-100, -100, 800, 1200); c.fill()
        car_.B_END_OFF[0] = True
        try:
            return draw(shot("2.1", cam=(270 - 40 * (z - 1) / 0.22, 480 + 60 * (z - 1) / 0.22, z), cast=[], before=before, after=after2, protect=()))
        finally:
            car_.B_END_OFF[0] = False
    return draw(shot("2.1", cam=(270 - 40 * (z - 1) / 0.22, 480 + 60 * (z - 1) / 0.22, z), cast=cast, after=after, protect=()))


# ---- 4.1: at the club's door, where they dropped her: dust off, "There you are." to the car, the sign flickers, she looks up
def a41(t):
    BRUSH = (oc.pm.ik(-1, -30, oc.BT + 60) + oc.pm.ik(1, 20, -190), oc.pm.ik(-1, -30, oc.BT + 60) + oc.pm.ik(1, 40, -150))
    CHEST = oc.pm.ik(-1, -30, oc.BT + 60) + oc.pm.ik(1, -6, oc.BT + 50)
    if t < 0.6:                                                                # dust off the coat, twice
        arms = BRUSH[int(t * 7) % 2]; face, look, gest = "peer", (0.4, 0.8), ("relax_s", "flat")
    elif t < 1.4:                                                              # to the car: There you are.
        u = ease(seg(t, 0.6, 0.85))
        arms = lerp(BRUSH[0], HERO, u); face, look, gest = "approve", (-0.9, 0.1), ("fist", "fist")
    else:                                                                      # the sign flickers; her eyes go up; a hand to her heart
        u = ease(seg(t, 1.7, 2.1))
        arms = lerp(HERO, CHEST, u); face, look, gest = ("hopeful" if t > 1.9 else "approve"), (0.0, -1.0), ("fist", "flat")
    p = P("pam_cat", 400, 714, 0.50, pose(asym(arms, 4), gest), face, look, rim=True)
    flick = 1.45 <= t < 1.55 or 1.65 <= t < 1.72                               # ONLY FOR YOU goes out twice, then holds
    def after(k):
        pam_(k, p, breath(t), 0.0, None)
        if flick:
            k.c.set_source_rgb(0.03, 0.03, 0.04); k.c.rectangle(96, 392, 348, 34); k.c.fill()
    if m.LAW[0]:                                           # (24 Nov) from where 3.6 left her, at its size; the camera pulls back to the marquee, landing on its flicker
        cam = lerp((300.0, 640.0, 1.8), (270.0, 462.0, 1.05), ease(seg(t, 0.6, 1.45)))     # ends on the shot's own camera
        return draw(shot("4.1", cam=cam, cast=[], after=after, protect=()))
    return draw(shot("4.1", cast=[], after=after, protect=()))


# ---- 4.3: she points at the sign, then at herself; turns to show someone: nobody; a small smile; ears up; in she goes
def a43(t):
    UP, ME = oc.CAT_POSES["point_up"][0], oc.CAT_POSES["point_me"][0]
    EARS = oc.pm.ik(-1, -40, oc.HY - 40) + oc.pm.ik(1, 40, oc.HY - 40)
    x, y, sc_, behind = 300, 712, 0.50, False
    kn = None; rot = 0.0
    if t < 0.75:
        u = ease(seg(t, 0.0, 0.25)); arms, gest, face, look = lerp(HERO, UP, u), ("fist", "point"), "proud", (0.5, -1.0)
        rot = -0.04 * u
    elif t < 1.25:
        u = ease(seg(t, 0.75, 0.95)); arms, gest, face, look = lerp(UP, ME, u), ("relax_s", "point"), "proud", (-0.2, -0.1)
    elif t < 2.0:                                                              # to the street: left, right: nobody
        arms, gest, face = HERO, ("fist", "fist"), "hopeful"
        look = (-1.0, 0.1) if t < 1.6 else (1.0, 0.1)                         # the eyes first, the head and body after them
        rot = (-0.06 * ease(seg(t, 1.33, 1.45))) if t < 1.6 else (-0.06 + 0.12 * ease(seg(t, 1.68, 1.82)))
        kn = kneel(4, l=(0, 6 if t < 1.6 else 0, -1), r=(0, 0 if t < 1.6 else 6, 1))   # the weight onto the other foot
    elif t < 2.35:                                                             # a small smile anyway; the ears patted up
        u = ease(seg(t, 2.0, 2.15)); arms, gest, face, look = lerp(HERO, EARS, u), ("flat", "flat"), "approve", (0.0, 0.0)
        kn = kneel(4 + 6 * abs(math.sin((t - 2.0) * 18)))
    else:                                                                      # and in: her back to us, smaller under the arch
        u = ease(seg(t, 2.35, 2.9)); behind = True
        x, y, sc_ = 300 + (270 - 300) * u, 712 - 52 * u, 0.50 * (1 - 0.28 * u)
        arms, gest, face, look = (-20, 20, 20, -20) if int(t * 10) % 2 else (20, -20, -20, 20), ("relax_s", "relax_s"), "proud", (0, 0)
    if behind:
        def shadow(k):
            c = k.c
            c.save(); c.translate(x, y + 2); c.scale(64 * sc_, 9 * sc_); c.new_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
            c.set_source_rgba(0, 0, 0, 0.5); c.fill()
        return draw(shot("4.3", cast=[P("pam_from_behind", x, y - (2 if int(t * 10) % 2 else 0), sc_, pose(arms, gest), face, look)], before=shadow, protect=()))
    p = P("pam_cat", x, y, sc_, pose(asym(arms, 3), gest), face, look, rim=True)
    return draw(shot("4.3", cast=[], after=lambda k: pam_(k, p, breath(t), rot, kn), protect=()))


# ---- 5.1: inside, from where the POV left off: the slow push goes on; the game goes on --------------------------------
def a51(t):
    u = ease(seg(t, 0.0, 1.2))
    return draw(shot("5.1", cam=(228 - 30 * u, 590 - 10 * u, 1.4 + 0.12 * u), after=lambda k: card(k, t), protect=()))


# ---- 5.3: she comes in from the right on her toes, low; the hand into his coat; out with the envelope; back off ------
def a53(t):
    LIFT = oc.CAT_POSES["lift"][0]
    if t < 0.9:                                                                # tiptoe in, low
        u = seg(t, 0.0, 0.9); x = 360 - 110 * ease(u)
        st_ = int(t * 10) % 2
        arms, gest, env = (-20, 30, 30, -10), ("relax_s", "relax_s"), False
        kn = kneel(5, l=(-3, 10 if st_ else 0, -1), r=(3, 0 if st_ else 10, 1)); rot = 0.07
    elif t < 1.6:                                                              # the hand into the coat
        u = ease(seg(t, 0.9, 1.25)); x = 250
        arms, gest, env = lerp((-20, 30, 30, -10), LIFT, u), ("relax_s", "grab"), False
        kn = kneel(12); rot = 0.09
    elif t < 2.0:                                                              # and out, with it
        x = 250; arms, gest, env = LIFT, ("relax_s", "grab"), True
        kn = kneel(12); rot = 0.06
    else:                                                                      # backing off, the envelope to her chest
        u = ease(seg(t, 2.0, 2.3)); x = 250 + 40 * u
        arms, gest, env = lerp(LIFT, oc.pm.ik(-1, -30, oc.BT + 60) + oc.pm.ik(1, 10, oc.BT + 40), u), ("relax_s", "grab"), True
        kn = kneel(8); rot = 0.03
    if m.LAW[0]:                                           # sneaking: low, both knees the way she goes (not out to both sides)
        d_ = 10 if t < 0.9 else (14 if t < 2.0 else 8)
        st2 = int(t * 10) % 2 if t < 0.9 else 0
        kn = dict(drop=d_, l=(-3, 8 if st2 else 0, -1), r=(-3, 0 if (st2 or t >= 0.9) else 8, -1))
    p = P("pam_cat", x, 716, 0.46, pose(arms, gest), "peer", (-0.8, 0.4), rim=True, env=env, hunt=0.5 if m.LAW[0] else 0.0, rim_red=bool(m.LAW[0]))
    def after(k):
        card(k, t)
        if m.LAW[0]:                                       # her shadow thrown away from the booth's lamp, along the boards
            c = k.c
            g = cairo.LinearGradient(x, 0, x + 120, 0); g.add_color_stop_rgba(0, 0, 0, 0, 0.5); g.add_color_stop_rgba(1, 0, 0, 0, 0.0)
            c.new_path(); c.move_to(x - 16, 712); c.line_to(x + 16, 720); c.line_to(x + 130, 734); c.line_to(x + 120, 716); c.close_path(); c.set_source(g); c.fill()
        pam_(k, p, breath(t), rot, kn)
    z = 1.9 * (1 + 0.03 * ease(seg(t, 0.0, 2.3)))                             # a slow push in
    if m.LAW[0]:                                           # as the envelope comes out: THE HOUSE stutters twice and goes out; ALWAYS COLLECTS burns on
        import on4_club as cl_
        cl_.ROW0[0] = 0.0 if (1.60 <= t < 1.68 or 1.76 <= t < 1.84 or t >= 1.95) else 1.0
        try:
            return draw(shot("5.3", cam=(160, 610, z), cast=[], after=after, protect=()))
        finally:
            cl_.ROW0[0] = 1.0
    return draw(shot("5.3", cam=(160, 610, z), cast=[], after=after, protect=()))


# ---- 5.3b: her black glove draws the envelope out of his coat by its edge -----------------------------------------------
def a53b(t):
    """5.3b, v4 (review: "an amorphous fist"; the hands rules): the envelope first, then the fingers over it: her thumb on
    its face at the edge, the index and middle finger behind it (their tips show over the top), the back of the hand,
    the wrist narrower than the cuff, the sleeve out of the frame's right edge. It comes out slowly and is held 0.6 s."""
    u = ease(seg(t, 0.2, 1.6))
    GL = (0.22, 0.22, 0.25); RIM = (0.85, 0.85, 0.82)                          # the glove a shade off the coat, rim-lit
    def lift(k):
        c = k.c
        sc.knee_coat(k, env=False, hand=False)
        ex, ey = 360 - 34 * u, 378 - 74 * u                                    # the envelope: half in the pocket, then out by its corner
        oc.envelope(k, ex, ey, 2.4)                                            # v5 (the hand rules: three tries failed, so the series' own grab):
        if u < 0.75:                                                           # the object first, then the hand over it
            st.poly(k, [(296, 400), (444, 400), (440, 520), (300, 520)], (0.16, 0.17, 0.22), 2.0)   # the pocket over it while it is in
        import hands_ps as hp
        gx, gy = ex + 104, ey - 26                                             # on its right edge, fingers curled over it, the heart left clear
        st.poly(k, [(gx + 150, gy - 150), (gx + 20, gy - 40), (gx + 52, gy - 6), (gx + 170, gy - 100)], oc.COAT, 2.4)   # her sleeve, from the corner of the frame
        c.set_source_rgb(*RIM); c.set_line_width(2); c.move_to(gx + 150, gy - 150); c.line_to(gx + 20, gy - 40); c.stroke()
        c.push_group(); hp.draw(k, "grab", gx, gy, 104, GL, (-0.7, 0.7), 1); g_ = c.pop_group()
        for dx_, dy_ in ((-3, 0), (3, 0), (0, -3), (0, 3)):                   # rim-lit off the dark coat
            c.save(); c.translate(dx_, dy_); c.set_source_rgba(*RIM, 0.9); c.mask(g_); c.restore()
        hp.draw(k, "grab", gx, gy, 104, GL, (-0.7, 0.7), 1)
        oc.ears(k, 500, 120 - 20 * u, 1.3)
    old = sc.coat_lift
    sc.coat_lift = lift
    try:
        return draw(shot("5.3b", protect=()))
    finally:
        sc.coat_lift = old


# ---- 6.1: up from the fall; she pulls a knife out of the boards and slits the envelope with it; the sheet slides out ---
def a61(t):
    import on4_props as pr
    X = 225
    KX = sc.KNIFE_AT[2][0]                                     # the nearest, at her right
    ENVH = oc.pm.ik(-1, -84, -170)                             # the envelope out in her left hand, at her shoulder, clear of her face
    if t < 0.6:                                                # down to it: weight onto the right, the hand to the handle
        u = ease(seg(t, 0.0, 0.45))
        arms = ENVH + lerp(oc.pm.ik(1, 50, -128), oc.pm.ik(1, (KX - X) / 0.86, -40), u)
        kn = kneel(46 * u, l=(-8, 0, -1), r=(14 * u, 0, 1)); rot = 0.18 * u; held = False
        if m.LAW[0]:                                       # a lunge to the knife: the far leg out and long, the near knee bent; more from the waist
            kn = dict(drop=20 * u, l=(-30 * u, 0, -1), r=(8 * u, 0, 1)); rot = 0.27 * u
    elif t < 0.9:                                              # up with it
        u = ease(seg(t, 0.6, 0.9))
        arms = ENVH + lerp(oc.pm.ik(1, (KX - X) / 0.86, -40), oc.pm.ik(1, 30, -176), u)
        kn = kneel(46 * (1 - u)); rot = 0.18 * (1 - u); held = True
        if m.LAW[0]:
            kn = dict(drop=20 * (1 - u), l=(-30 * (1 - u), 0, -1), r=(8 * (1 - u), 0, 1)) if u < 0.97 else None; rot = 0.27 * (1 - u)
    else:                                                      # the slit: across the top of the envelope, then the sheet out
        u = ease(seg(t, 0.95, 1.2))
        arms = ENVH + lerp(oc.pm.ik(1, 30, -176), oc.pm.ik(1, -40, -176), u)        # at her chest: nothing over her eyes
        kn = None; rot = 0.0; held = True
    p = P("pam_cat", X, 700, 0.86, pose(asym(arms, 3), ("grab", "grab")), "peer" if t < 1.3 else "hopeful", (0.2, -0.6), rim=True)
    pulled = t >= 0.6
    def after(k):
        c = k.c
        sc.stage_marks(k, skip=(2,) if pulled else ())
        pts = pam_(k, p, breath(t), rot, kn)
        sc._spot_on(k)
        lx, ly = pts["hands"][0]; rx, ry = pts["hands"][1]
        oc.envelope(k, lx + 6, ly - 34, 1.4)                   # the dream envelope, its heart to us
        if t > 1.25:                                           # the sheet sliding up out of it
            v = ease(seg(t, 1.25, 1.8))
            c.save(); c.translate(lx + 6, ly - 50 - 60 * v); c.rotate(-0.06)
            c.rectangle(-30, -40, 60, 72); c.set_source_rgb(0.97, 0.97, 0.95); c.fill_preserve(); c.set_source_rgb(*m.INK); c.set_line_width(1.5); c.stroke()
            c.restore()
        if held:
            sc.knife(c, rx, ry - 10, -0.9 if t < 1.2 else -2.2, 1.5)
        if 0.95 <= t < 1.2:                                    # the slit's flash
            c.set_source_rgba(1, 1, 1, 0.8); c.set_line_width(3); c.move_to(lx - 30, ly - 58); c.line_to(lx + 42, ly - 58); c.stroke()
    sc.MARKS[0] = False
    try:
        return draw(shot("6.1", cam=(250, 560, 1.4), cast=[], after=after, protect=()))
    finally:
        sc.MARKS[0] = True


# ---- 6.2: her glove's thumb slides off the sheet: SOFIA, the photograph; the camera in on the circled number ---------
def a62(t):
    """v5 (review): her hand holds the sheet at its right edge: the palm off the paper, the thumb across its face (the
    fingers are behind it). The thumb lies over the end of SOFIA and slides down off it. The camera comes in a little,
    her face and the number both in frame, and holds 0.5 s."""
    u = ease(seg(t, 0.15, 0.7)); z = 1.0 + 0.14 * ease(seg(t, 0.4, 1.1))
    GL = (0.22, 0.22, 0.25); RIM = (0.85, 0.85, 0.82)
    def after(k):
        c = k.c
        ey = 492 + 74 * u                                                      # the thumb's height: on the name, then under it
        st.poly(k, [(620, ey - 60), (500, ey - 34), (506, ey + 44), (620, ey + 70)], oc.COAT, 2.4)   # her sleeve, from the right edge
        for col, grow in ((RIM, 3), (GL, 0)):                                  # the palm, off the paper's edge
            c.new_path(); c.save(); c.translate(506, ey + 10); c.scale(48 + grow, 58 + grow); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
            c.set_source_rgb(*col); c.fill()
        for col, w in ((RIM, 46), (GL, 40)):                                   # the thumb, short and thick, across the sheet's face
            c.set_source_rgb(*col); c.set_line_width(w); c.set_line_cap(1); c.move_to(480, ey); c.line_to(404, ey - 8); c.stroke()
        c.set_source_rgba(0, 0, 0, 0.35); c.set_line_width(2); c.new_path(); c.arc(410, ey - 8, 13, -1.2, 1.2); c.stroke()   # its nail's edge
    return draw(shot("6.2", cam=(270, 480 - 20 * (z - 1) / 0.14, z), after=after, protect=()))


# ---- office -------------------------------------------------------------------------------------------------------
def _desk_shot(sid, t, cast, after=None, loc=None, cam=None):
    kw = dict(cast=cast, protect=())
    if after:
        kw["after"] = after
    if loc:
        kw["loc"] = loc
    if cam:
        kw["cam"] = cam
    return draw(shot(sid, **kw))


D_CAM = (668, 598, 2.75)                                    # v5 (review): the office 15 % closer: the actors, not the counter


def _pam_asleep(t, x=692, feet=760, look=(0, 0)):
    return P("pam_awake", x, feet - 1.5 * math.sin(2 * math.pi * 0.22 * t), 0.50, "down", "neutral", look, "arm_up_open")


def a71(t):                                                    # asleep on the counter, breathing
    return draw(shot("7.1", cam=D_CAM, cast=[_pam_asleep(t)], protect=()))


def a72(t):                                                    # Sofia in mid-step, eyes on her phone; the envelope into the hand; her mug; on
    import sofia_dh as sd
    import on4_props as pr
    import hands_ps as hp
    sd.so.POSES["post"] = (sd.so.POSES["hold"][0], sd.so.POSES["hold"][1], 160, 40)
    x = 560 + 85 * ease(seg(t, 0.0, 0.8)) + 160 * ease(seg(t, 2.5, 3.2))
    reach = 0.8 <= t < 1.6
    sof = P("sofia", x, 800 - (4 if int(t * 8) % 2 and (t < 0.8 or t > 2.5) else 0), 0.47, "post" if reach else "hold", "appraise", (0.2, 1.0))
    v = ease(seg(t, 0.8, 1.4))
    def post(k):
        hx, hy = sc.HANDS.get("pam_awake", (706, 510))
        if t >= 0.8:                                           # up from her hand into Pam's
            ex, ey = 650 + (hx + 2 - 650) * v, 640 + (hy - 20 - 640) * v
            pr.envelope(k, ex, ey, 0.26, 0.2 * v + 0.5 * math.sin(v * math.pi) * 0.3)
            if v >= 1:
                hp.draw(k, "grab", hx, hy, 15, (0.99, 0.86, 0.70), (0.0, -1.0), 1)
    loc = "desk8" if t > 2.3 else None                         # her mug at the end of the row
    return draw(shot("7.2", cam=D_CAM, cast=[_pam_asleep(t), sof], after=post, protect=(), **({"loc": loc} if loc else {})))


def a73(t):
    """the clink wakes her. Expectation: the mask up, a heart on an envelope in her hand: she smiles."""
    up = t > 0.35
    face = "neutral" if t < 0.5 else ("approve" if t < 0.85 else "hopeful")   # a gasp, then the smile: a heart, for her
    p = P("pam_awake", 692, (724 if up else 742) - (4 * math.sin(seg(t, 0.35, 0.6) * math.pi) if up else 0), 0.50, "up" if up else "down", face,
          (0.4, -0.7) if t > 0.5 else (0, 0), "arm_up_open")
    return draw(shot("7.3", cam=(696, 628, 3.0), cast=[p], after=sc._sofia_post, protect=()))


def a74(t):                                                    # the rota, big; the camera down the column to SUN, then still for 1 s
    u = ease(seg(t, 0.1, 1.0))
    return draw(shot("7.4", cam=(270, 440 + 40 * u, 1.0 + 0.10 * u), protect=()))


def a75(t):
    """Realization, then disappointment: the sheet under her chin, her fingertip down the rows to the seventh PAM; her
    eyes follow it; the brows go, the head sinks a little; held."""
    import on4_props as pr
    u = ease(seg(t, 0.2, 1.7))
    face = "hopeful" if t < 0.35 else ("approve" if t < 0.8 else ("doubt" if t < 1.8 else "fade"))   # smile, the gasp, the brows, gone
    sink = 5 * ease(seg(t, 1.8, 2.2))
    p = P("pam_awake", 692, 722 + sink, 0.50, "up", face, (-0.2, 0.7 + 0.3 * u), "stand")
    def after(k):
        pr.rota(k, 706, 694, 0.30, -0.05)                      # held under her chin, in both hands
        for fx in (676, 736):
            kit.ellipse(k, fx, 652 + (fx - 676) * 0.05, 8, 6, (0.99, 0.86, 0.70), 7600 + fx, shadow=False, lw=1.4)
        row = min(6, int(u * 7))
        fy = 673 + row * 9.4
        kit.ellipse(k, 728, fy, 6, 4.5, (0.99, 0.86, 0.70), 7690, shadow=False, lw=1.3)       # her fingertip on the row's PAM
        k.c.set_source_rgba(0, 0, 0, 0.25); k.c.set_line_width(1); k.c.move_to(722, fy + 5); k.c.line_to(734, fy + 5); k.c.stroke()
    return draw(shot("7.5", cam=(702, 648, 3.1), cast=[p], after=after, protect=()))


SHOTS = {"1.3": (a13, 2.91), "1.4": (a14, 2.8), "2.1": (a21, 2.2), "4.1": (a41, 2.6), "4.3": (a43, 2.9), "5.1": (a51, 1.2), "5.3": (a53, 2.3), "5.3b": (a53b, 2.3), "6.1": (a61, 2.0), "6.2": (a62, 1.6), "7.1": (a71, 1.4), "7.2": (a72, 3.2), "7.3": (a73, 1.4), "7.4": (a74, 2.0), "7.5": (a75, 2.8)}


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
