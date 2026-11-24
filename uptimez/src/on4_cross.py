"""OFFICE NOIR 4: the crossing after the bump, restaged (24 Nov, after Tomas's frame-by-frame complaint: figures on top of
each other, no one scale). His picks: four shots instead of one wide take; Don wipes the bonnet from behind the car;
the two who take the money are Dad's bodyguards (dh_cast.guard, Daddy's Home), not street silhouettes; the car at the
people's scale.

ONE SCALE LAW for this set (on4_motion.c_side: far kerb y 584, near kerb y 790): a figure's size comes from where its feet
are. dscale(y) is Don's rig; Pam-Cat = 1.203 x that (as she stood at the bump); a bodyguard = 0.903 x that (Daddy's
Home's own ratio, guard 0.56 to Father 0.62); the limousine 1.65 (its roof at 0.82 of a man standing beside it).

  W  3.3   Don comes round behind the bonnet, wipes it, holds his glove up: clean. She lies in front, her palm still up.
  R  3.3b  the rear window: Don comes round the tail; the ringed hand, his bill; the rest go up over the roof.
  B  3.4   her: the bills come down on her; the car backs out of frame.
  G  3.5   the two bodyguards walk in behind her, take the bills, lift her, carry her off left.
Nobody stands in front of anybody: in W Don is behind the car, in R she is out of frame, in B and G Don is."""
import math
import cairo
import on4_motion as m
import on4_scenes as sc
import on4_cast as oc
import on4_street as st
import on4_car as car
import on4_lying as ly
import client_ob as co
import dh_cast as dc
import kit

P = sc.P
FWD = [False]                                                # (24 Nov, Tomas: "after the crash the car leaves backwards") it drives on, forward: out onto the far side of the road, round her, and off to the left
S_CAR = 1.65
PAM_K, GUARD_K = 1.203, 0.903
NOSE = 345.0                                                 # the bumper, where it stopped (T3: STOPX + 5 - 170 S)
CX = NOSE + 170 * S_CAR
LX, LY_, LS, LEAN = 345.0, 702.0, 0.62, -1.5                 # her, lying as she fell: the same rig, on its heels' spot


def dscale(y):
    return 0.42 + 0.14 * (y - 596.0) / 176.0


def bob(i, a=3.0):
    return -a if i % 2 else 0.0


def pam(face="doubt", look=(0.9, -0.6), arm=(50, -128), dx=0.0, dy=0.0):
    arms = oc.pm.ik(-1, -30, oc.BT - 30) + oc.pm.ik(1, arm[0], arm[1])
    return P("pam_cat", LX + dx, LY_ + dy, LS, m.pose(arms, ("relax_s", "palm")), face, look, lean=LEAN)


def shadow(k, x, y, rx, ry=7, a=0.45):
    c = k.c
    c.save(); c.translate(x, y); c.scale(rx, ry); c.new_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
    c.set_source_rgba(0, 0, 0, a); c.fill()


def bill(k, x, y, ang, s=2.0):
    c = k.c
    ly.bill(k, x, y, ang, s, seed=0)
    c.save(); c.translate(x, y); c.rotate(ang); c.set_source_rgb(0.12, 0.16, 0.10)
    c.select_font_face("sans-serif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10 * s)
    c.move_to(-3 * s, 3.5 * s); c.show_text("$"); c.restore()


def don(x, y, pose="stand", face="neutral", look=(0.9, 0.2), **kw):
    kw.setdefault("paddle_side", "GO"); kw.setdefault("paddle_ang", 0.9)
    return P("don", x, y, dscale(y), pose, face, look, **kw)


def plen(pts):
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:]))


def draw_don(k, d, dist=None, dirn=1):
    """Don; with dist (how far he has walked, px) he walks: a step every 0.30 of his height (on4_scenes.stepped,
    Office Noir 3's walk facing the camera). v2's side legs under his front-on body crossed (lesson 90): dropped."""
    if dist is None:
        sc.draw_cast(k, [d]); return
    who, a, kw = d
    kw = dict(kw); kw["step"] = math.pi * dist / (0.30 * 392 * a[2])
    kw.setdefault("lean", 0.035 * math.sin(kw["step"]))      # his weight over the standing foot
    sc.draw_cast(k, [(who, a, kw)])


def guard(k, x, y, pose, flip, seed, lean=0.0, step=None, turn=0.0):
    """Dad's bodyguard. step: he walks (on4_scenes.stepped). turn: his head turned, -1..1 (The Offer's of_cast._turn_head)."""
    import of_cast as oca
    c = k.c
    c.save(); c.translate(x, y); c.rotate(lean + (0.03 * math.sin(step) if step is not None else 0.0)); c.translate(-x, -y)
    def one(f_):
        o = dc.guard(k, x, f_, GS, pose=pose, flip=flip, seed=seed)
        if turn:
            oca._turn_head(k, x, f_, GS, flip, turn, seed)
        return o
    if step is not None:
        sc.stepped(one, k, x, y, GS, -co.HIP, step, 14.0)
    else:
        one(y)
    c.restore()


def fist(k, x, y, s_=1.0):
    """a bodyguard's hand under her: a cuff and a fist"""
    c = k.c
    c.set_source_rgb(0.97, 0.97, 0.94); c.rectangle(x - 7 * s_, y + 5 * s_, 14 * s_, 5 * s_); c.fill()
    kit.ellipse(k, x, y, 9 * s_, 7.5 * s_, dc.SKIN_F, 7900 + int(x) % 50, shadow=False, lw=1.6)


def path(pts, t):
    """along a polyline, t 0..1 by length"""
    L = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:])]
    d = t * sum(L)
    for (a, b), l in zip(zip(pts, pts[1:]), L):
        if d <= l or (a, b) == (pts[-2], pts[-1]):
            u = min(1.0, d / max(l, 1e-6)); return (a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u)
        d -= l


# ---- W: the wipe ---------------------------------------------------------------------------------------------------------
CAM_W = (300, 640, 1.45)
D_W = (398.0, 694.0)                                         # behind the bonnet, the car between him and us


WALK_W = [(170, 596), (330, 604), (420, 640), D_W]
NW = 18                                                      # drawings he walks for (12 a second): about four steps


def tw():
    def f(i):
        dist = None
        if i < NW:                                           # off the kerb, along the far side of the road, in behind the bonnet
            t = i / float(NW - 1)
            x, y = path(WALK_W, t); dist = plen(WALK_W) * t
            d = don(x, y, "stand", "neutral", (0.9, 0.3))
        elif i < NW + 18:                                    # his glove along the bonnet, out and back, the elbow working
            u = 0.5 - 0.5 * math.cos(2 * math.pi * (i - NW) / 6.0)
            d = don(D_W[0], D_W[1], (-56 - 18 * u, 40 - 14 * u, 8, 0), "neutral", (-0.8, 0.7), lean=-0.06 - 0.04 * u)
        elif i < NW + 21:                                    # he straightens, the glove up to his eye
            u = (i - NW - 18) / 3.0
            d = don(D_W[0], D_W[1], (-56 + 36 * u, 40 - 190 * u, 8, 0), "neutral", (-0.6, -0.3), lean=-0.06 * (1 - u))
        else:                                                # clean
            d = don(D_W[0], D_W[1], (-20, -150, 8, 0), "pleased", (-0.6, -0.3))
        wv = 0.5 - 0.5 * math.cos(2 * math.pi * (i - NW - 4) / 6.0) if NW + 4 <= i < NW + 16 else 0.0     # her small wave: the palm that was up
        pm_ = pam("doubt", (0.9, -0.7), (50 + 12 * wv, -128 - 22 * wv))
        def after(k):
            shadow(k, LX - 105, LY_ + 44, 125, 8)
            if d[1][1] < 650:
                shadow(k, d[1][0], d[1][1] + 2, 70 * d[1][2], 11 * d[1][2])
            draw_don(k, d, dist, 1)                          # Don first: the car hides him below the bonnet
            shadow(k, CX, 728, 160 * S_CAR, 8, 0.5)
            car.side(k, CX, 724, S_CAR)
            sc.draw_cast(k, [pm_])
        return m.draw(m.shot("3.1", loc="C_side", cam=CAM_W, cast=[], protect=(), after=after))
    f = m.lazy(f)
    return [f(i) for i in range(NW + 26)]              # 44: 3.3 and 3.3b share their time in halves (on4_scenes._timing)


# ---- R: the rear window --------------------------------------------------------------------------------------------------
CAM_R = (772, 640, 1.45)
D_R = (866.0, 772.0)                                         # on our side, by the boot, right of the window
WX, WY = CX + 74 * S_CAR, 724 - 86 * S_CAR                   # the rear window's middle


WALK_R = [(948, 640), (930, 720), D_R]
NR = 12


def tr():
    def f(i):
        j = i - NR + 10                                      # the old count, from where he stands
        cx = CX + (0 if j < 31 else ((j - 31) / 5.0) ** 2 * 260)                      # at the end it starts to back away
        cb = 724.0
        if FWD[0]:                                           # it pulls out to the far side and forward (to the left)
            q = max(0.0, (j - 28) / 13.0)
            cx = CX - 360 * q * q; cb = 724 - 30 * m.ease(min(1.0, q * 1.6))
        dist = None
        if i < NR:                                           # round the tail to our side, on his legs
            t = i / float(NR - 1)
            x, y = path(WALK_R, t); dist = plen(WALK_R) * t
            d = don(x, y, "stand", "neutral", (-0.9, 0.2))
        elif j < 28:                                         # his hand out for it; a look; into his vest
            u = min(1.0, max(0.0, (j - 15) / 3.0))
            d = don(D_R[0], D_R[1], (-70 + 30 * u, -10 + 40 * u, 8, 0), "pleased", (-0.6, -0.5) if j < 22 else (-0.3, 0.6))
        else:                                                # GO: the whistle
            d = don(D_R[0], D_R[1], "wave", "pleased", (-0.8, -0.2), paddle_ang=0.20 + 0.10 * math.sin(i * math.pi), whistle_in=True)
        def after(k):
            c = k.c
            shadow(k, cx, cb + 4, 160 * S_CAR, 8, 0.5)
            car.side(k, cx, cb, S_CAR)
            wx = WX + (cx - CX)
            if j >= 7:                                       # the glass down
                c.set_source_rgb(0.02, 0.02, 0.03); c.rectangle(wx - 36 * S_CAR, cb - 96 * S_CAR, 72 * S_CAR, 22 * S_CAR); c.fill()
            ox = 10 * max(0.0, 1 - abs(j - 13) / 3.0)        # the hand: out to him with his bill; a flick up on each of hers
            oy = 0.0
            for q in range(6):
                oy -= 9 * max(0.0, 1 - abs(j - (17 + q * 1.5)) / 0.8)
            if 9 <= j < 27:                                  # the cuff and the ringed hand, toward him
                c.save(); c.translate(wx + ox, WY + 4 + oy); c.scale(-1.5, 1.5); c.translate(-wx, -WY - 4)
                st.poly(k, [(wx + 30, WY - 6), (wx - 8, WY - 2), (wx - 6, WY + 12), (wx + 30, WY + 10)], dc.VELVET, 1.6)
                kit.ellipse(k, wx - 16, WY + 8, 11, 8, dc.SKIN_F, 7801, shadow=False, lw=1.6)
                c.set_source_rgb(*st.GOLD); c.rectangle(wx - 20, WY + 3, 6, 6); c.fill()
                c.restore()
            shadow(k, d[1][0], d[1][1] + 2, 70 * d[1][2], 11 * d[1][2])
            draw_don(k, d, dist, -1)
            hx, hy = wx + 26 + ox, WY + 16 + oy              # the ringed hand's fingers
            dx_, dy_ = d[1][0] - 62, d[1][1] - 150           # his glove
            if 11 <= j < 27:                                 # his: across, a look, into the vest
                if j < 15:
                    t = (j - 11) / 4.0; bill(k, hx + (dx_ - hx) * t, hy + (dy_ - hy) * t, 0.2, 1.5)
                elif j < 22:
                    bill(k, dx_, dy_, -0.2, 1.5)
                else:
                    t = (j - 22) / 5.0; bill(k, dx_ + 40 * t, dy_ + 46 * t, -0.2 - t, 1.5 - 0.6 * t)
            for q in range(6):                               # hers: up over the roof, away to the left
                t0 = 17 + q * 1.5
                if j < t0:
                    continue
                t = (j - t0) / 8.0
                x = hx - 12 - 330 * t; y = WY + 16 - 40 - 230 * math.sin(min(1.0, t) * math.pi * 0.62) + 40 * t * t
                if x > 560:
                    bill(k, x, y, 0.4 + q + t * 4, 1.3)
        m.POOL[0] = (700, 630)                              # the light where this shot is: the car's tail, under the lit window
        try:
            return m.draw(m.shot("3.1", loc="C_side", cam=CAM_R, cast=[], protect=(), after=after))
        finally:
            m.POOL[0] = (250, 610)
    f = m.lazy(f)
    return [f(i) for i in range(NR + 32)]              # 44


# ---- B: the bills on her -------------------------------------------------------------------------------------------------
CAM_B = (236, 648, 1.6)
LAND = [(206, 694), (232, 710), (258, 692), (284, 708), (308, 692), (330, 708)]     # on her coat and her legs; her face stays clear


def tb():
    def f(i):
        cx = CX + 260 + (i / 6.0) ** 2 * 300                 # the car going, out of frame by the eighth drawing
        if FWD[0]:                                           # it passes behind her, right to left, and is gone by the eleventh drawing
            cx = CX - 360 - 62.0 * i - 3.0 * i * i
        look = (0.9, -0.9) if i < 8 else (0.3, -0.2)
        pm_ = pam("doubt" if i < 14 else "fade", look, (50, -128))
        def after(k):
            shadow(k, LX - 105, LY_ + 44, 125, 8)
            if FWD[0]:
                if cx + 175 * S_CAR > 40:
                    shadow(k, cx, 698, 160 * S_CAR, 8, 0.5); car.side(k, cx, 694, S_CAR)
            elif cx - 170 * S_CAR < 420:
                shadow(k, cx, 728, 160 * S_CAR, 8, 0.5); car.side(k, cx, 724, S_CAR)
            sc.draw_cast(k, [pm_])
            for j, (bx, by) in enumerate(LAND):              # down out of the dark, swinging, onto her
                t = min(1.0, max(0.0, (i - j * 1.6) / 9.0))
                if i < j * 1.6:
                    continue
                x = bx + 150 * (1 - t) + math.sin(t * 7 + j) * 16 * (1 - t); y = 330 + (by - 330) * (t ** 1.4)
                bill(k, x, y, 0.4 + j + (1 - t) * 3, 1.3)
        return m.draw(m.shot("3.1", loc="C_side", cam=CAM_B, cast=[], protect=(), after=after))
    f = m.lazy(f)
    return [f(i) for i in range(22)]


# ---- G: the bodyguards ---------------------------------------------------------------------------------------------------
CAM_G = (240, 640, 1.35)
GY = 690.0                                                   # behind her (she is drawn after them)
GS = dscale(GY) * GUARD_K
GX = (150.0, 332.0)                                          # one at her head, one at her heels


def garm(lt, rt):
    """a bodyguard's arms by where the hands go (his own units: x from his middle, y up from his feet negative)"""
    return dc.ik(-co.SH[0], co.BT + 26, lt[0], lt[1], co.LN1, co.LN2, -1) + dc.ik(co.SH[0], co.BT + 26, rt[0], rt[1], co.LN1, co.LN2, 1)


G_WALK = garm((-78, co.HIP + 40), (78, co.HIP + 40))
G_DOWN = lambda side: garm((-40, co.HIP + 96), (78, co.HIP + 40)) if side < 0 else garm((-78, co.HIP + 40), (40, co.HIP + 96))
G_HOLD = lambda side: garm((-112, co.BT + 20), (78, co.HIP + 40)) if side < 0 else garm((-78, co.HIP + 40), (112, co.BT + 20))
G_CARRY = garm((-46, co.HIP + 84), (46, co.HIP + 84))
G_WATCH = dc.GUARD_POSE                                      # his hands clasped in front of him: the one who keeps watch
TAKE, GIVE, POCKET, LIFT, GO = 10, 23, 28, 31, 36
G_REACH = lambda sd, dn: garm((-40 if sd < 0 else -78, co.HIP + (96 if (sd < 0 and dn) else 40) if sd < 0 else co.HIP + 40),
                              (40 if sd > 0 else 78, co.HIP + (96 if (sd > 0 and dn) else 40) if sd > 0 else co.HIP + 40))


def tg():
    """Tomas's picks after the review of the stills (24 Nov): two men, two jobs. The one at her head bends and picks the
    bills up one by one; the one at her heels keeps watch, hands clasped, looking up and down the street; the first
    hands him half; both pocket it; then both bend, hands under her, and she goes up and away, stiff, swaying."""
    def f(i):
        go = max(0.0, i - GO)
        cdx = -30.0 * go
        up = m.ease(min(1.0, max(0.0, (i - LIFT) / 4.0)))
        lift = -46.0 * up
        sway = 0.045 * math.sin(i * math.pi / 2.0 - 0.9) if go else 0.0             # she swings behind their steps
        step = 0.0                                           # (their bob is in the walk now)
        gs = []
        for j in (0, 1):
            if i < TAKE:                                     # in from the right, the collector first
                t = m.ease(min(1.0, max(0.0, (i - j * 2.0) / 7.5)))
                x = 520 + j * 90 + (GX[j] - 520 - j * 90) * t
                gs.append([x, GY, G_WALK, 0.0, j == 1, (math.pi * (520 + j * 90 - x) / (0.30 * 447 * GS)) if t < 1 else None, 0.0])
            elif i < LIFT:
                if j == 0:                                   # he bends for each bill, and comes up with it
                    ph = (i - TAKE) % 2.0
                    dn = i < GIVE - 1 and ph < 1.0
                    pose = garm((-84, co.HIP + 30), (44, co.HIP + 100)) if dn else garm((-84, co.HIP + 30), (-40, co.HIP + 30))   # down for one; across to the fan in his other hand
                    if i >= GIVE:                            # half of it across to the other
                        pose = garm((-84, co.HIP + 30), (118, co.BT + 70)) if i < POCKET else G_WALK
                    gs.append([GX[0], GY, pose, 0.16 if dn else 0.03, False, None, 0.0])
                else:                                        # the watch: hands clasped; he looks the other way now and then
                    tn = 0.0                                 # his head: up the street, back, down the street, back (The Offer's turn)
                    for t0, t1, v in ((TAKE + 2, TAKE + 5, 1.0), (TAKE + 8, TAKE + 11, -1.0)):
                        tn += v * max(0.0, min(1.0, (i - t0) / 1.0, (t1 + 1 - i) / 1.0))
                    pose = G_WATCH if i < GIVE else (garm((-118, co.BT + 70), (78, co.HIP + 40)) if i < POCKET else G_WALK)
                    gs.append([GX[1], GY, pose, 0.0, True, None, tn])
            else:                                            # both bend to her, hands under her, up, and away
                bend = 0.14 * (1 - up) * (1 if j == 0 else -1)
                gs.append([GX[j] + cdx, GY, G_CARRY, bend, j == 1, (math.pi * go * 30.0 / (0.30 * 447 * GS) + j * 0.5) if go else None, 0.0])
        arm = (50 + 5 * math.sin(i * math.pi / 2.0 - 1.6), -128 + 8 * math.cos(i * math.pi / 2.0 - 1.6)) if go else (50, -128)
        arms = oc.pm.ik(-1, -30, oc.BT - 30) + oc.pm.ik(1, arm[0], arm[1])
        pm_ = P("pam_cat", LX + cdx, LY_ + lift, LS, m.pose(arms, ("relax_s", "palm")), "fade" if i < LIFT else "doubt",
                (0.3, -0.2) if i < LIFT else (0.9, -0.6), lean=LEAN + sway, tilt=(0.09 * math.sin(i * math.pi / 2.0 - 2.2)) if go else 0.0)
        def after(k):
            for j, g in enumerate(gs):
                shadow(k, g[0], GY + 3, 62 * GS, 8 * GS + 3)
            if lift > -30:
                shadow(k, LX - 105 + cdx, LY_ + 44, 125, 8, 0.45 * (1 + lift / 46.0) + 0.1)
            for j, g in enumerate(gs):
                guard(k, g[0], g[1], g[2], g[4], 1600 + j * 40, g[3], g[5], g[6])
            if up > 0.25:                                    # their hands under her (drawn first: she lies on them): at her shoulders, at her ankles
                yb = LY_ + lift + 27
                for hx_ in (LX - 168 + cdx, LX - 128 + cdx, LX - 44 + cdx, LX - 8 + cdx):
                    fist(k, hx_, yb, 1.0)
            sc.draw_cast(k, [pm_])
            f0x, f0y = gs[0][0] - 84 * GS, gs[0][1] + (co.HIP + 30) * GS               # the collector's other hand, low at his side: the fan grows there, clear of his face
            f1x, f1y = gs[1][0] - 118 * GS, gs[1][1] + (co.BT + 70) * GS                # the watch's hand, out to take his half
            for j, (bx, by) in enumerate(LAND):              # six bills: off her one by one, a fan in his fist; three across; pocketed
                if i >= POCKET:
                    continue
                t = min(1.0, max(0.0, (i - TAKE - 0.6 - j * 2.0) / 1.2))
                x, y, ang = bx + (f0x - 6 - bx) * t, by + (f0y - by - j * 4) * t, (0.4 + j) * (1 - t) + (-1.2 + 0.10 * j) * t
                if i >= GIVE and j % 2:                      # every other one goes across
                    u = min(1.0, (i - GIVE) / 3.0)
                    x, y, ang = x + (f1x - x) * u, y + (f1y - (j // 2) * 6 - y) * u, ang * (1 - u) + (-0.4 + 0.12 * j) * u
                bill(k, x, y, ang, 1.3 - 0.2 * t)
        return m.draw(m.shot("3.1", loc="C_side", cam=CAM_G, cast=[], protect=(), after=after))
    f = m.lazy(f)
    return [f(i) for i in range(52)]


TESTS = {"W": m.keys(tw), "R": m.keys(tr), "B": m.keys(tb), "G": m.keys(tg)}
