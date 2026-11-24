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


def tw():
    def f(i):
        if i < 10:                                           # off the kerb, along the far side of the road, in behind the bonnet
            x, y = path([(170, 596), (330, 604), (420, 640), D_W], m.ease(i / 9.0))
            d = don(x, y + bob(i), "stand", "neutral", (0.9, 0.3), lean=0.03 if i % 2 else -0.03)
        elif i < 28:                                         # his glove along the bonnet, out and back
            out = (i // 3) % 2 == 0
            d = don(D_W[0], D_W[1], (-74, 26, 8, 0) if out else (-56, 40, 8, 0), "neutral", (-0.8, 0.7), lean=-0.10 if out else -0.06)
        elif i < 31:                                         # he straightens, the glove up to his eye
            d = don(D_W[0], D_W[1], (-20, -150, 8, 0), "neutral", (-0.6, -0.3))
        else:                                                # clean
            d = don(D_W[0], D_W[1], (-20, -150, 8, 0), "pleased", (-0.6, -0.3))
        wave = 14 <= i < 28 and (i // 3) % 2 == 0            # her small wave: the palm that was up
        pm_ = pam("doubt", (0.9, -0.7), (62, -150) if wave else (50, -128))
        def after(k):
            shadow(k, LX - 105, LY_ + 44, 125, 8)
            if d[1][1] < 640:
                shadow(k, d[1][0], d[1][1] + 2, 70 * d[1][2], 11 * d[1][2])
            sc.draw_cast(k, [d])                             # Don first: the car hides him below the bonnet
            shadow(k, CX, 728, 160 * S_CAR, 8, 0.5)
            car.side(k, CX, 724, S_CAR)
            sc.draw_cast(k, [pm_])
        return m.draw(m.shot("3.1", loc="C_side", cam=CAM_W, cast=[], protect=(), after=after))
    f = m.lazy(f)
    return [f(i) for i in range(38)]


# ---- R: the rear window --------------------------------------------------------------------------------------------------
CAM_R = (772, 640, 1.45)
D_R = (866.0, 772.0)                                         # on our side, by the boot, right of the window
WX, WY = CX + 74 * S_CAR, 724 - 86 * S_CAR                   # the rear window's middle


def tr():
    def f(i):
        cx = CX + (0 if i < 31 else ((i - 31) / 5.0) ** 2 * 260)                      # at the end it starts to back away
        if i < 10:                                           # round the tail to our side
            x, y = path([(948, 640), (930, 720), D_R], m.ease(i / 9.0))
            d = don(x, y + bob(i), "stand", "neutral", (-0.9, 0.2), lean=0.03 if i % 2 else -0.03)
        elif i < 28:                                         # his hand out for it; a look; into his vest
            d = don(D_R[0], D_R[1], (-70, -10, 8, 0) if i < 16 else (-40, 30, 8, 0), "pleased", (-0.6, -0.5) if i < 22 else (-0.3, 0.6))
        else:                                                # GO: the whistle
            d = don(D_R[0], D_R[1], "wave", "pleased", (-0.8, -0.2), paddle_ang=0.10 if i % 2 else 0.30, whistle_in=True)
        def after(k):
            c = k.c
            shadow(k, cx, 728, 160 * S_CAR, 8, 0.5)
            car.side(k, cx, 724, S_CAR)
            wx = WX + (cx - CX)
            if i >= 7:                                       # the glass down
                c.set_source_rgb(0.02, 0.02, 0.03); c.rectangle(wx - 36 * S_CAR, 724 - 96 * S_CAR, 72 * S_CAR, 22 * S_CAR); c.fill()
            if 9 <= i < 27:                                  # the cuff and the ringed hand, toward him
                c.save(); c.translate(wx, WY + 4); c.scale(-1.5, 1.5); c.translate(-wx, -WY - 4)
                st.poly(k, [(wx + 30, WY - 6), (wx - 8, WY - 2), (wx - 6, WY + 12), (wx + 30, WY + 10)], dc.VELVET, 1.6)
                kit.ellipse(k, wx - 16, WY + 8, 11, 8, dc.SKIN_F, 7801, shadow=False, lw=1.6)
                c.set_source_rgb(*st.GOLD); c.rectangle(wx - 20, WY + 3, 6, 6); c.fill()
                c.restore()
            shadow(k, d[1][0], d[1][1] + 2, 70 * d[1][2], 11 * d[1][2])
            sc.draw_cast(k, [d])
            hx, hy = wx + 26, WY + 16                        # the ringed hand's fingers
            dx_, dy_ = d[1][0] - 62, d[1][1] - 150           # his glove
            if 11 <= i < 27:                                 # his: across, a look, into the vest
                if i < 15:
                    t = (i - 11) / 4.0; bill(k, hx + (dx_ - hx) * t, hy + (dy_ - hy) * t, 0.2, 1.5)
                elif i < 22:
                    bill(k, dx_, dy_, -0.2, 1.5)
                else:
                    t = (i - 22) / 5.0; bill(k, dx_ + 40 * t, dy_ + 46 * t, -0.2 - t, 1.5 - 0.6 * t)
            for j in range(6):                               # hers: up over the roof, away to the left
                t0 = 17 + j * 1.5
                if i < t0:
                    continue
                t = (i - t0) / 8.0
                x = hx - 12 - 330 * t; y = hy - 40 - 230 * math.sin(min(1.0, t) * math.pi * 0.62) + 40 * t * t
                if x > 520:
                    bill(k, x, y, 0.4 + j + t * 4, 1.3)
        m.POOL[0] = (700, 630)                              # the light where this shot is: the car's tail, under the lit window
        try:
            return m.draw(m.shot("3.1", loc="C_side", cam=CAM_R, cast=[], protect=(), after=after))
        finally:
            m.POOL[0] = (250, 610)
    f = m.lazy(f)
    return [f(i) for i in range(36)]


# ---- B: the bills on her -------------------------------------------------------------------------------------------------
CAM_B = (236, 648, 1.6)
LAND = [(206, 694), (232, 710), (258, 692), (284, 708), (308, 692), (330, 708)]     # on her coat and her legs; her face stays clear


def tb():
    def f(i):
        cx = CX + 260 + (i / 6.0) ** 2 * 300                 # the car going, out of frame by the eighth drawing
        look = (0.9, -0.9) if i < 8 else (0.3, -0.2)
        pm_ = pam("doubt" if i < 14 else "fade", look, (50, -128))
        def after(k):
            shadow(k, LX - 105, LY_ + 44, 125, 8)
            if cx - 170 * S_CAR < 420:
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
TAKE, LIFT, GO = 10, 22, 27


def tg():
    def f(i):
        go = max(0, i - GO)
        cdx = -30.0 * go
        lift = -46.0 * m.ease(min(1.0, max(0.0, (i - LIFT) / 4.0))) + (4 if (go and i % 2) else 0)
        gs = []
        for j in (0, 1):
            side = -1 if j == 0 else 1                       # which hand works: the one toward her middle
            if i < TAKE:                                     # in from the right, one after the other
                t = m.ease(min(1.0, max(0.0, (i - j * 1.5) / 7.5)))
                x = 520 + j * 90 + (GX[j] - 520 - j * 90) * t
                gs.append((x, GY + (bob(i, 2.5) if t < 1 else 0), G_WALK))
            elif i < LIFT:                                   # down for the bills, up with them
                gs.append((GX[j], GY, G_DOWN(-side) if (i - TAKE) < 4 + j * 2 else G_HOLD(-side)))
            else:                                            # under her, up, and away
                gs.append((GX[j] + cdx, GY + (bob(i, 2.5) if go else 0), G_CARRY))
        pm_ = pam("fade" if i < LIFT else "doubt", (0.3, -0.2) if i < LIFT else (0.9, -0.6), (50, -128), dx=cdx, dy=lift)
        def after(k):
            for j, (x, y, a) in enumerate(gs):
                shadow(k, x, GY + 3, 62 * GS, 8 * GS + 3)
            if lift > -30:
                shadow(k, LX - 105 + cdx, LY_ + 44, 125, 8, 0.45 * (1 + lift / 46.0) + 0.1)
            for j, (x, y, a) in enumerate(gs):
                dc.guard(k, x, y, GS, pose=a, flip=(j == 1), seed=1600 + j * 40)
            sc.draw_cast(k, [pm_])
            for j, (bx, by) in enumerate(LAND):              # the bills: on her; then three to each fist, a fan beside his head
                own = j % 2
                t = min(1.0, max(0.0, (i - TAKE - 3 - own * 2 - (j // 2) * 1.2) / 3.0))
                gx_, gy_, _ = gs[own]
                sd = 1 if own == 0 else -1                   # the fist toward her middle
                fx_, fy_ = gx_ + sd * 112 * GS, gy_ + (co.BT + 20) * GS - 8 - (j // 2) * 9
                if i >= LIFT:
                    continue                                 # into their pockets before they take her
                x, y, ang = bx + (fx_ - bx) * t, by + (fy_ - by) * t, (0.4 + j) * (1 - t) + (0.4 - 0.3 * (j // 2)) * sd * t
                bill(k, x, y, ang, 1.3 - 0.2 * t)
        return m.draw(m.shot("3.1", loc="C_side", cam=CAM_G, cast=[], protect=(), after=after))
    f = m.lazy(f)
    return [f(i) for i in range(43)]


TESTS = {"W": m.keys(tw), "R": m.keys(tr), "B": m.keys(tb), "G": m.keys(tg)}
