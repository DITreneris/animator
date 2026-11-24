"""OFFICE NOIR 4: the motion tests, v1 (24 Nov; series/production-process.md, after the board's G4). The beats a still
could not carry, each drawn at 8 drawings a second from the scene file's own shots (on4_scenes.py, its MOT parameters):

  T1  1.1-1.2   the hat shadow's threat, Pam's punch (wind-up, strike, a held hit, the shadow squashing down the wall),
                Sofia walking past on her phone
  T2  2.2-2.3   the envelope: on the Client's knee, his two taps, Dad's ringed hand flat (agreed), into the Client's OWN coat
  T3  3.1-3.2   STOP at Pam's side, the flip, GO to the car; she stops in its path; the car rolls in; the bump, held
  T4  6.3-7.1   the envelope held up; nobody; the arm comes down; the match cut to the arm asleep on the counter
  T5  8.1-1.1   the rota over the cups, the push to the lamp, the room dark, the streetlamp: the loop

  python3 on4_motion.py [T1 T2 ..]  ->  office-noir-4/on4_motion_<t>_v1.mp4 (540x960, 8 drawings/s, encoded at 24 fps)
                                        office-noir-4/on4_motion_<t>_v1.png (the contact sheet at 8 fps, numbered)
  Neutral copies of the sheets for the cold viewers: /tmp/on4_mot/<n>.png"""
import copy
import math
import os
import subprocess
import sys
import cairo
import on4_scenes as sc
import on4_cast as oc

BY = {x["id"]: x for _, ss in sc.SCENES for x in ss}
FPS = 12
OUT = sc.OUT
P = sc.P
_n = [0]


def pose(arms, gest=("relax_s", "relax_s")):
    """registers an arm pose with its hands; returns its name"""
    _n[0] += 1
    name = "_m%d" % _n[0]
    oc.CAT_POSES[name] = (tuple(arms), gest)
    return name


def lerp(a, b, t):
    if isinstance(a, (tuple, list)):
        return tuple(lerp(x, y, t) for x, y in zip(a, b))
    return a + (b - a) * t


def ease(t):
    return t * t * (3 - 2 * t)


def shot(id_, **over):
    sh = copy.copy(BY[id_]); sh.update(over)
    return sh


def draw(sh, mot=None):
    sc.MOT.clear(); sc.MOT.update(mot or {})
    try:
        s, _ = sc.render(sh, 1)
    finally:
        sc.MOT.clear()
    return s


def dark(s, a, cx=None, cy=None):
    c = cairo.Context(s)
    if cx is None:
        c.set_source_rgba(0.01, 0.01, 0.02, a); c.paint()
    else:
        g = cairo.RadialGradient(cx, cy, 70, cx, cy, 320)
        g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0.01, 0.01, 0.02, a)
        c.set_source(g); c.paint()
    return s


# ================================ v2 (24 Nov, Tomas's picks: "tvarkom animacija") ================================
# T1: Pam looks at the shadow; hit, a held drawing, then the shadow squashes, stretches and RUNS down the wall into a puddle.
# T2: a car, not "space": the rear door from outside (roof line, pillar, wheel arch, the lane's wall over it), a dark
#     cabin, a seat his size, no starlit roof; one shot: his own hand taps the envelope twice on his knee, lifts it and
#     puts it under his own lapel; Dad's ringed hand lies down on the seat.
# T3: STOP and GO from the front, then the bump from the side: the car drives in, she faces it, tips, folds and lies.
# T4: the arm comes down; the drawing with the arm up again is gone.  T5: the lamp stays put; the room darkens, rain,
#     a dissolve to the street.
FPS = 12
import alley_on3 as al
import on4_street as st
import on4_car as car
import on4_lying as ly
import client_ob as co
import dh_cast as dc
import hands_ps as hp
import kit
from kit import INK

HERO = oc.CAT_POSES["hero"][0]
WIND = oc.pm.ik(-1, -30, oc.BT - 30) + oc.pm.ik(1, 50, -128)
PUNCH = oc.CAT_POSES["punch"][0]
_loc0 = sc._loc


def shadow2(k, w=1.0, h=1.0, drip=0.0, state="aim", lean=0.0):
    """the projected hat shadow (sc.wall_shadow's geometry) with its deformation: w, h scale it on the wall; drip 0..1
    runs it down the wall into a puddle at the wall's foot."""
    c = k.c
    bx, by = 96, 742
    c.set_source_rgba(0.02, 0.02, 0.03, 0.80 * (1 - drip))
    c.new_path(); c.move_to(bx - 34, by + 34); c.line_to(bx + 40, by - 40); c.line_to(250, 960); c.line_to(70, 960); c.close_path(); c.fill()
    c.save(); c.new_path(); c.move_to(-20, 40); c.line_to(196, 300); c.line_to(196, 640); c.line_to(-20, 860); c.close_path(); c.clip()
    g = cairo.RadialGradient(110, 470, 20, 110, 470, 240)
    g.add_color_stop_rgba(0, 1, 1, 0.95, 0.55); g.add_color_stop_rgba(1, 1, 1, 0.95, 0)
    c.set_source(g); c.paint()
    hh = h * (1 - 0.93 * drip)
    if hh > 0.05:
        c.save(); c.translate(bx, by)
        c.transform(cairo.Matrix(0.74 * w * (1 + 0.9 * drip), -0.74 * w, 0, hh, 0, 0)); c.rotate(lean)
        al.shadow_man(k, 0, 0, 0.98, "knife", state, flip=True)
        c.restore()
    if drip > 0:                                            # streaks running down the wall
        c.set_source_rgba(0.02, 0.02, 0.03, 0.85)
        for i, dx in enumerate((-50, -20, 10, 40, 64)):
            x0 = bx + dx; y0 = by - dx - 250 * (1 - drip) * (0.6 + 0.1 * i)
            c.rectangle(x0 - 5, y0, 10, (by - dx) - y0 + 6); c.fill()
    c.restore()
    if drip > 0:                                            # the puddle at the wall's foot
        c.save(); c.translate(bx + 30, by + 20); c.rotate(-0.78); c.scale(110 * drip, 26 * drip)
        c.new_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.set_source_rgba(0.02, 0.02, 0.03, 0.9); c.fill()


CAT = [True]                                                 # v6 (Tomas): Office Noir 1's black cat leaps across the lens at 0:00.25


def cat_over(s, frames):
    """the cat, drawn after the grade so its eyes keep their colour (as on_film does): frames = [(x, y, scale, flip)] or "full" """
    import cat_on as ct
    c = cairo.Context(s); kk = sc.Ctx(c, 0)
    if frames == "in":
        ct.black_cat(kk, 70, 1010, 4.2, "fall", flip=False)
    elif frames in ("full", "full2"):
        big = frames == "full2"
        ct.black_cat(kk, 300, 1040, 9.5, "fall", flip=False)
        c.set_source_rgba(0.02, 0.02, 0.03, 0.97 if big else 0.9); c.paint()      # the lens is fur
        dx = 14 if big else 0
        for ex in (176 + dx, 368 + dx):
            ct._eye(c, ex, 400, 50 if big else 42, "open")
        c.set_source_rgb(*ct.MOUTH); c.new_path(); c.save(); c.translate(272 + dx, 590); c.scale(1.0, 0.72 if big else 0.5)
        c.arc(0, 0, 84, 0, 2 * math.pi); c.restore(); c.fill()
        c.set_source_rgb(0.96, 0.95, 0.9)                                           # four fangs
        for fx_, up in ((-46, 1), (46, 1), (-34, -1), (34, -1)):
            yb = 590 - up * (60 if big else 42) * 0.9
            c.move_to(272 + dx + fx_ - 11, yb); c.line_to(272 + dx + fx_ + 11, yb); c.line_to(272 + dx + fx_, yb + up * 34); c.close_path(); c.fill()
    elif frames == "out":
        ct.black_cat(kk, 470, 330, 3.4, "fall", flip=False)
    elif frames == "gone":
        ct.black_cat(kk, 560, 150, 1.6, "fall", flip=False)
    return s


def t1():
    fr = []
    N = 42 if CAT[0] else 34
    FL = oc.pm.ik(-1, -64, -150) + oc.pm.ik(1, 64, -150)     # both hands up by her ears
    def sof(i):
        t = i / float(N)
        return (330 + 70 * t + (5 if i % 4 < 2 else -5), 650 + 560 * t * t + 80 * t - (7 if i % 2 else 0), 0.50 + 0.5 * t)   # v3: steps
    def f(i, arms, lean, face, look, sh, burst=False, hop=0):
        sx, sy, ss = sof(i)
        sofia = [P("sofia", sx, sy, ss, "hold", "appraise", (0.2, 1.0))] if sy < 1180 else []
        pam = [P("pam_cat", 220, 730 - hop, 0.84, pose(arms, ("fist", "fist")), face, look, lean=lean)]
        flat = []
        cast = flat + (sofia + pam if sy < 735 else pam + sofia)
        return draw(shot("1.1", cast=cast, before=lambda k: shadow2(k, **sh),
                         after=(lambda k: sc._burst(k, 98, 544, 36)) if burst else None))
    i = 0
    if CAT[0]:
        for _ in range(3):                                   # 0.25 s: frame 0, held
            fr.append(f(i, HERO, 0, "peer", (-1.0, -0.5), dict())); i += 1
        FL2 = oc.pm.ik(-1, -84, -176) + oc.pm.ik(1, 84, -176)                 # v7: hands flung wide over her head
        for step, hop, t in (("in", 0, 0.2), ("full", 0, 0.5), ("full2", 0, 0.8)):
            fr.append(cat_over(f(i, lerp(HERO, FL2, t), 0, "doubt", (0.9, -0.8), dict(), hop=hop), step)); i += 1       # the cat fills the lens
        fr.append(cat_over(f(i, FL2, 0.20, "doubt", (0.9, -0.9), dict(), hop=46), "out")); i += 1                       # v7: the flinch after it, where we can see it:
        fr.append(cat_over(f(i, FL2, 0.24, "doubt", (0.9, -0.9), dict(), hop=58), "gone")); i += 1                      # off the ground, bent back, arms up
        for hop, lean in ((58, 0.24), (40, 0.20), (14, 0.12)):
            fr.append(f(i, FL2, lean, "doubt", (0.9, -0.9), dict(), hop=hop)); i += 1
        for t in (0.5, 0.0):                                 # collects herself; her eyes back on the shadow
            fr.append(f(i, lerp(HERO, FL2, t), 0, "peer", (-1.0, -0.5), dict())); i += 1
        fr.append(f(i, HERO, 0, "peer", (-1.0, -0.5), dict())); i += 1
    else:
        for _ in range(6):                                   # 0.5 s: the threat, held; her eyes already on it
            fr.append(f(i, HERO, 0, "peer", (-1.0, -0.5), dict())); i += 1
    for t in (0.4, 0.8, 1.0):                                # the wind-up: the fist back, the weight back
        fr.append(f(i, lerp(HERO, WIND, t), 0.07 * t, "peer", (-1.0, -0.4), dict())); i += 1
    fr.append(f(i, lerp(WIND, PUNCH, 0.6), -0.04, "peer", (-1.0, -0.3), dict())); i += 1          # the strike
    fr.append(f(i, PUNCH, -0.13, "peer", (-1.0, -0.3), dict(w=1.0, h=1.0), burst=True)); i += 1   # contact
    fr.append(fr[-1]); i += 1                                # the held drawing
    for sh in (dict(w=1.25, h=0.8, lean=-0.08), dict(w=1.45, h=0.64, lean=-0.14), dict(w=1.5, h=0.6, lean=-0.16),
               dict(w=1.5, h=0.6, lean=-0.16, drip=0.3), dict(w=1.5, h=0.6, lean=-0.16, drip=0.6),
               dict(w=1.5, h=0.6, lean=-0.16, drip=0.85)):                     # v3: squash and run, no stretch back up
        fr.append(f(i, PUNCH, -0.12, "peer", (-1.0, 0.2), sh)); i += 1                            # squash, stretch, run
    for t in (0.5, 1.0):                                     # she turns to be thanked
        fr.append(f(i, lerp(PUNCH, HERO, t), -0.06 * (1 - t), "proud", (0.7, 0.3), dict(drip=1.0, state="down"))); i += 1
    while i < N:                                             # Sofia walks past and out; the pose held at nobody
        fr.append(f(i, HERO, 0, "proud" if i < N - 6 else "fade", (0.7, 0.6), dict(drip=1.0, state="down"))); i += 1
    return fr


# ---- T2 -----------------------------------------------------------------------------------------------------------------
WIN = [(70, 372), (410, 372), (470, 450), (470, 610), (70, 610)]


def seat3(k):
    """2.2 v2: the rear door from outside, in the lane."""
    c = k.c
    c.set_source_rgb(0.34, 0.33, 0.32); c.paint()                                                 # the lane's wall over the car
    for row in range(0, 12):
        for col in range(-1, 10):
            c.set_source_rgb(0.26, 0.25, 0.24); c.set_line_width(1.6); c.rectangle(col * 64 + (32 if row % 2 else 0), row * 28, 64, 28); c.stroke()
    st.poly(k, [(330, 60), (470, 60), (470, 250), (330, 250)], (0.05, 0.05, 0.06), 2.2)
    st.poly(k, [(-10, 330), (380, 322), (520, 400), (560, 430), (560, 960), (-10, 960)], car.BODY, 2.6)   # the body: roof, pillar
    c.set_source_rgb(*car.BODY_HI); c.set_line_width(3); c.move_to(-10, 336); c.line_to(378, 328); c.line_to(516, 404); c.stroke()
    car._p(c, WIN); c.set_source_rgb(0.07, 0.07, 0.09); c.fill()                                   # the cabin: dark
    c.save(); car._p(c, WIN); c.clip()
    st.poly(k, [(150, 470), (430, 470), (446, 620), (136, 620)], car.CREAM, 2.0)                  # the seat back, his size
    for x in (220, 290, 360):
        c.set_source_rgb(0.70, 0.66, 0.56); c.set_line_width(1.6); c.move_to(x, 478); c.line_to(x, 612); c.stroke()
    for x in (196, 356):
        car._rr(c, x - 38, 428, 76, 44, 12); car._fs(c, car.CREAM, 1.8)                           # two headrests
    c.restore()


def seat3_people(k, hand, env, dad):
    """his hand at `hand` (body units, co._ik target), the envelope at his hand (env: "hand") or under his lapel ("coat")."""
    c = k.c
    c.save(); car._p(c, WIN); c.clip()
    arms = (-10, 5) + co._ik(1, *hand)
    c.push_group(); o = co.client(k, 200, 728, 0.74, arms, "plain", look=(0.25, 0.9), roll=False, badge=False); c.pop_group()
    hx, hy = o["hands"][1]
    cx_, cy_ = o["head"][0] + 14, o["head"][1] + 104       # his chest, under the left lapel
    o = co.client(k, 200, 728, 0.74, arms, "plain", look=(0.25, 0.9), roll=False, badge=False)
    if env == "hand":
        oc.envelope(k, hx + 4, hy - 12, 1.15)
        kit.ellipse(k, hx, hy + 4, 15, 12, (0.87, 0.70, 0.58), 7700, shadow=False, lw=2.0)        # his thumb over its edge
    if env == "coat":
        oc.envelope(k, cx_ + 6, cy_ - 8, 1.0)
        st.poly(k, [(cx_ - 22, cy_ + 12), (cx_ + 36, cy_ + 2), (cx_ + 40, cy_ + 40), (cx_ - 18, cy_ + 44)], (0.30, 0.36, 0.26), 2.2)   # his jacket over its lower half
    dx = (1 - dad) * 160                                                                           # Dad's ringed hand on the seat
    st.poly(k, [(560 + dx, 560), (420 + dx, 566), (422 + dx, 606), (560 + dx, 612)], dc.VELVET, 2.2)
    kit.ellipse(k, 392 + dx, 590, 34, 15, dc.SKIN_F, 7702, shadow=False, lw=2.2)                  # v3: palm down, flat on the seat
    for i_ in range(4):
        kit.ellipse(k, 362 + dx - i_ * 2, 580 + i_ * 6, 14, 5, dc.SKIN_F, 7703 + i_, shadow=False, lw=1.6)
    c.set_source_rgb(*INK); c.rectangle(372 + dx, 576, 11, 14); c.fill(); c.set_source_rgb(*st.GOLD); c.rectangle(374 + dx, 578, 7, 10); c.fill()
    c.set_source_rgb(*st.NEON); c.rectangle(374 + dx, 580, 7, 6); c.fill()
    c.restore()
    car._p(c, WIN); c.set_source_rgb(*car.CHROME); c.set_line_width(4); c.stroke()                 # the window's chrome
    c.set_source_rgb(*INK); c.set_line_width(2.4); c.move_to(40, 340); c.line_to(40, 900); c.stroke()   # the door's shut lines
    c.move_to(500, 430); c.line_to(500, 780); c.stroke()
    car._rr(c, 90, 668, 70, 12, 5); car._fs(c, car.CHROME, 1.4)                                    # the handle
    c.set_source_rgb(*car.CHROME); c.set_line_width(4); c.move_to(-10, 800); c.line_to(430, 800); c.stroke()   # the sill strip
    c.set_source_rgb(0.02, 0.02, 0.03); c.new_path(); c.arc(520, 900, 120, math.pi, 2 * math.pi); c.fill()     # the wheel arch
    car._wheel(c, 520, 900, 96)
    c.save(); c.translate(486, 300); c.scale(-1, 1)                                                # her ears over the roof's edge:
    kit.ellipse(k, 0, 40, 60, 54, (0.36, 0.30, 0.27), 7501, shadow=False, lw=2.2); oc.ears(k, 0, 36, 0.85); c.restore()   # watching


def t2():
    KNEE, UP, CHEST = (62, co.BT + 150), (62, co.BT + 128), (12, co.BT + 62)
    seq = [(KNEE, "hand", 0)] * 5 + [(UP, "hand", 0), (KNEE, "hand", 0), (KNEE, "hand", 0), (UP, "hand", 0), (KNEE, "hand", 0)]   # two taps
    seq += [(KNEE, "hand", d) for d in (0.3, 0.7, 1, 1, 1, 1)]                                     # Dad's hand lies down: agreed
    seq += [(lerp(KNEE, CHEST, ease(t)), "hand", 1) for t in (0.25, 0.5, 0.75, 1.0)]               # he lifts it to his coat
    seq += [(CHEST, "coat", 1)] * 2 + [(lerp(CHEST, KNEE, t), "coat", 1) for t in (0.5, 1.0)] + [(KNEE, "coat", 1)] * 6   # under his lapel
    return [draw(shot("2.2", loc="seat3", cam=sc.WIDE, cast=(), protect=(),
                      after=lambda k, a=a: seat3_people(k, *a))) for a in seq]


# ---- T3 -----------------------------------------------------------------------------------------------------------------
def c_side(k):
    """3.2 from the side of the road: the far houses, the road, the crossing's bars, the lamp."""
    c = k.c
    c.set_source_rgb(0.03, 0.03, 0.04); c.paint()
    st.poly(k, [(-300, 360), (300, 360), (300, 300), (420, 300), (420, 380), (1000, 380), (1000, 568), (-300, 568)], (0.90, 0.89, 0.86), 2.2)
    for x in (-120, -40, 40, 110, 200, 340, 460, 560, 640, 720, 800):
        st.poly(k, [(x, 430), (x + 34, 430), (x + 34, 500), (x, 500)], (0.06, 0.06, 0.07), 1.6)
    st.poly(k, [(-300, 568), (1000, 568), (1000, 584), (-300, 584)], (0.62, 0.61, 0.58), 1.6)        # the far kerb
    st.poly(k, [(-300, 584), (1000, 584), (1000, 790), (-300, 790)], st.ROAD, 1.6)
    c.set_source_rgba(0, 0, 0, 0.25); c.set_line_width(1.2)
    for y in range(596, 790, 16):
        c.move_to(-300, y); c.line_to(1000, y); c.stroke()
    for y, hh, x0, x1 in ((606, 10, 150, 430), (634, 14, 135, 440), (668, 20, 118, 452), (712, 28, 96, 466)):
        st.poly(k, [(x0, y), (x1, y), (x1 + 6, y + hh), (x0 - 6, y + hh)], (0.93, 0.92, 0.88), 1.2)
    st.poly(k, [(-300, 790), (1000, 790), (1000, 960), (-300, 960)], (0.20, 0.20, 0.21), 1.6)        # the near kerb, ours
    c.set_source_rgb(0.62, 0.62, 0.64); c.set_line_width(8); c.move_to(60, 584); c.line_to(60, 250); c.stroke()
    c.set_source_rgb(*INK); c.set_line_width(5); c.move_to(60, 584); c.line_to(60, 250); c.stroke()
    st.lamp_head(k, 60, 250, 0.8)


def _loc2(k, name):
    if name == "seat3":
        seat3(k); return None
    if name == "C_side":
        c_side(k); return lambda c_: sc.ons.vignette(c_, 0.5)
    return _loc0(k, name)


sc._loc = _loc2
PX, PF = 300, 716                                            # where she stands on the crossing (side view)


def t3():
    """v3: the whole beat from the side, one car. She comes over the crossing toward us; Don, on the far kerb, holds STOP
    out at her side; she stops; he flips it, GO to the car, the toot; the car drives in from the right; the bump."""
    fr = []
    STOPP = oc.pm.ik(-1, -30, oc.BT + 60) + oc.pm.ik(1, 96, oc.HY + 30)
    RUN = (-50, 30, 50, -40); RUN2 = (40, -30, -40, 30)
    D_STOP = ("stop", "confused", dict(paddle_side="STOP", chin=1))
    D_EDGE = ((-8, 0, 92, -40), "confused", dict(paddle_side="EDGE", chin=1))
    D_GO = ("wave", "pleased", dict(paddle_side="GO", paddle_ang=0.10, whistle_in=True))
    STOPX = PX + 40 + 170
    def side(cx, don, pam, burst=False):
        kind, px, pf, ps, arms, gest, lean, face, look = pam
        dpose, dface, dkw = don
        def after(k):
            c = k.c
            if cx < 900:
                g = cairo.LinearGradient(cx - 170, 0, cx - 420, 0)
                g.add_color_stop_rgba(0, 1, 1, 0.92, 0.5); g.add_color_stop_rgba(1, 1, 1, 0.92, 0)
                c.set_source(g); c.move_to(cx - 168, 652); c.line_to(cx - 430, 600); c.line_to(cx - 430, 720); c.line_to(cx - 168, 672); c.close_path(); c.fill()
            if kind == "down":
                c.save(); c.translate(PX, PF - 6); c.scale(0.6, 0.6); c.translate(-330, -690); ly.body(k); ly.head(k, *ly.HEAD, ly.ANG); c.restore()
            car.side(k, cx, 724, 1.0)
            if burst:
                sc._burst(k, PX + 34, PF - 60, 40)
        cast = [P("don", 170, 596, 0.42, dpose, dface, (0.9, -0.2), **dkw)]
        if kind == "up":
            cast.append(P("pam_cat", px, pf, ps, pose(arms, gest), face, look, lean=lean))
        return draw(shot("3.1", loc="C_side", cam=(300, 610, 1.45), cast=cast, protect=(), after=after))
    OFF = 1200
    for i in range(6):                                       # she comes over the crossing, after the car
        t = i / 5.0
        fr.append(side(OFF, D_STOP, ("up", PX, 610 + (PF - 610) * t, 0.44 + 0.18 * t, RUN if i % 2 == 0 else RUN2,
                                     ("fist", "fist"), 0.0, "peer", (0.8, -0.2))))
    STAND = ("up", PX, PF, 0.62, HERO, ("fist", "fist"), 0.0, "approve", (-0.9, -0.3))               # she sees STOP: stops dead
    fr += [side(OFF, D_STOP, STAND)] * 5
    fr.append(side(OFF, D_EDGE, STAND))                      # the flip
    fr += [side(OFF, D_GO, STAND)] * 3                       # GO, the toot, to the car
    FACE = lambda lean, dy, face: ("up", PX + lean * 60, PF + dy, 0.62, STOPP, ("relax_s", "palm"), -lean, face, (1.0, -0.1))
    for cx in (STOPX + 330, STOPX + 230, STOPX + 140, STOPX + 70, STOPX + 24):                     # the car drives in; she turns her palm to it
        fr.append(side(cx, D_GO, FACE(0, 0, "approve")))
    fr.append(side(STOPX + 6, D_GO, FACE(0, 0, "approve")))
    hit = side(STOPX, D_GO, FACE(0.16, 0, "approve"), burst=True)
    fr += [hit, hit]
    fr.append(side(STOPX, D_GO, FACE(0.45, 6, "doubt")))
    fr.append(side(STOPX, D_GO, FACE(0.8, 14, "doubt")))
    fr.append(side(STOPX, D_GO, FACE(1.15, 26, "doubt")))
    fr += [side(STOPX, D_GO, ("down", 0, 0, 0, HERO, ("fist", "fist"), 0, "", (0, 0)))] * 8          # she lies; he still waves GO
    return fr


def t6():
    """3.3-3.5 in the same side camera (Tomas, rough v2), one long shot, 7 s: she lies under the bumper; Don comes off the
    kerb to the bonnet, lays his glove on it, holds it up to his eye: clean; her small wave; the rear window comes down,
    the ringed hand lets the bills go, they drift onto her; the car backs away; two shadows walk in, pluck the bills
    off her, step over her and go. Nobody looks down."""
    fr = []
    STOPX = PX + 40 + 170
    CA, CB = (300, 610, 1.45), (392, 600, 1.02)
    BILLS = [(196, 682), (262, 694), (322, 686)]              # v5: three big ones, the first onto her face
    DX, DY, DS = 352, 772, 0.56                                  # v5: Don on the road in front of the bonnet, nearer than the car
    def f(i):
        cam = CA if i < 36 else lerp(CA, CB, ease(min(1.0, (i - 36) / 6.0)))
        cx = STOPX + (0 if i < 57 else ((i - 57) / 7.0) ** 2 * 420)                # the car backs away
        if i < 9:                                                                    # Don comes to the bonnet
            t = i / 8.0; don = P("don", 170 + (DX - 170) * t, 596 + (DY - 596) * t, 0.42 + (DS - 0.42) * t, "stand", "neutral", (0.9, 0.2), paddle_side="GO", paddle_ang=0.9)
        elif i < 32:                                                                 # v5: his glove along the bonnet, back and forth; his back to her
            w = (72, -24) if (i // 3) % 2 else (58, -10)
            don = P("don", DX, DY, DS, (-8, 0) + w, "neutral", (0.9, 0.6), paddle_side="GO", paddle_ang=0.9, lean=0.10)
        elif i < 40:                                                                 # clean
            don = P("don", DX, DY, DS, "stand", "pleased", (0.9, 0.3), paddle_side="GO", paddle_ang=0.9)
        elif i < 62:
            don = P("don", DX, DY, DS, "wave", "pleased", (0.8, -0.2), paddle_side="GO", paddle_ang=0.10, whistle_in=(i % 6 < 3))
        else:
            t = min(1.0, (i - 62) / 8.0); don = P("don", DX - (DX - 170) * t, DY - (DY - 596) * t, DS - (DS - 0.42) * t, "stand", "neutral", (-0.8, 0), paddle_side="GO", paddle_ang=0.9)
        wave = 24 <= i < 38 and (i // 3) % 2 == 0
        TH = (PX - 96, PX + 92)                                                      # v8 (Tomas): one at her head, one at her feet
        LIFT, GO = 73, 76                                                           # they take the money, pick her up, carry her off
        cdx = -32.0 * max(0, i - GO)                                                # the carry: everything moves left together
        cdy = -34.0 * min(1.0, max(0.0, (i - LIFT) / 3.0)) + (4 if (i > GO and i % 2) else 0)
        def thug_at(j):
            t = (i - (60 + j * 2)) / 7.0
            if t < 0:
                return None
            if t < 1:
                return (660 - (660 - TH[j]) * t, t, "in")
            return (TH[j] + cdx, t, "take" if i < GO else "go")
        def after(k):
            c = k.c
            hands = {}
            for j in (0, 1):                                                         # the shadows first: they stand behind her, she stays whole
                th = thug_at(j)
                if th is None:
                    continue
                x, t, ph = th
                st.thug(k, x, 704, 0.40, "open" if (ph != "take" and int(t * 6) % 2) else (-30, 20, 30, -20), seed=4500 + j,
                        hands=("grab", "grab") if ph != "in" else ("relax", "relax"), lean=0.0)
                hands[j] = (x - 6, 704 - 150, ph, t)                                 # the bill held up over his head
            c.save(); c.translate(PX + cdx, PF - 6 + cdy); c.scale(0.6, 0.6); c.translate(-330, -690); ly.body(k); ly.head(k, *ly.HEAD, ly.ANG)
            if wave:
                sc._wave(k)
            c.restore()
            car.side(k, cx, 724, 1.0)
            sc.draw_cast(k, [don])                                                   # in front of the car, not on it
            wx, wy = cx + 74, 724 - 86                                               # the rear window
            if 44 <= i < 62:
                c.set_source_rgb(0.02, 0.02, 0.03); c.rectangle(cx + 38, 724 - 96, 72, 22); c.fill()   # the glass down
            if 46 <= i < 60:                                                         # the cuff and the ringed hand out of it
                st.poly(k, [(wx + 30, wy - 6), (wx - 8, wy - 2), (wx - 6, wy + 12), (wx + 30, wy + 10)], dc.VELVET, 1.6)
                kit.ellipse(k, wx - 16, wy + 8, 11, 8, dc.SKIN_F, 7801, shadow=False, lw=1.6)
                c.set_source_rgb(*st.GOLD); c.rectangle(wx - 20, wy + 3, 6, 6); c.fill()
            def bill(x, y, ang):
                ly.bill(k, x, y, ang, 2.0, seed=0)
                c.save(); c.translate(x, y); c.rotate(ang); c.set_source_rgb(0.12, 0.16, 0.10)
                c.select_font_face("sans-serif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(20)
                c.move_to(-6, 7); c.show_text("$"); c.restore()
            for j, (bx, by) in enumerate(BILLS):                                     # the bills: let go, drifting onto her; then up into a shadow's fist
                t0 = 48 + j * 2
                if i < t0:
                    continue
                t = min(1.0, (i - t0) / 9.0)
                x = wx - 16 + (bx - (wx - 16)) * t; y = wy + 14 + (by - (wy + 14)) * t * t + math.sin(t * 9 + j) * 8 * (1 - t)
                ang = 0.4 + j + t * 3
                own = hands.get(0 if j < 2 else 1)                                   # the first shadow takes two, the second one
                if own and own[2] != "in":
                    hx, hy, ph, tt_ = own
                    u = min(1.0, (tt_ - 1.0) / 0.5)
                    x, y, ang = x + (hx + (j % 2) * 22 - x) * u, y + (hy - (j % 2) * 10 - y) * u, ang * (1 - u) + (0.25 - 0.5 * (j % 2)) * u
                if x > -30:
                    bill(x, y, ang)
        return draw(shot("3.1", loc="C_side", cam=cam, cast=[], protect=(), after=after))
    return [f(i) for i in range(84)]


# ---- T4 -----------------------------------------------------------------------------------------------------------------
def t4():
    fr = []
    UP = oc.CAT_POSES["triumph2"][0]; DOWN = (-8, 0, 8, 0)
    for _ in range(6):
        fr.append(draw(shot("6.3")))                         # held up, in the light: Well?
    off = draw(shot("6.3", loc="stage_dark", after=None))    # v3: the light goes out while we still see all of her
    fr += [off, off, off]
    def close(t, face, look):
        arms = lerp(UP, DOWN, ease(t))
        cast = [P("pam_cat", 262, 950, 1.5, pose(arms, ("relax_s", "fist")), face, look, env=True, rim=True)]
        return draw(shot("6.6", cast=cast))
    for look in ((-0.9, 0), (-0.9, 0), (0.9, 0), (0.9, 0), (0, 0), (0, 0)):                        # her eyes cross the room: nobody
        fr.append(close(0.0, "hopeful", look))
    for t in (0.1, 0.25, 0.4, 0.55, 0.7, 0.82, 0.92, 1.0):                                         # the arm comes slowly down
        fr.append(close(t, "doubt" if t < 0.5 else "fade", (0.3, 0.3 + 0.5 * t)))
    for _ in range(6):
        fr.append(close(1.0, "fade", (0.4, 0.9)))            # Of course.
    for _ in range(8):
        fr.append(draw(shot("7.1")))                         # the cut: asleep on the counter, the arm up
    return fr


# ---- T5 -----------------------------------------------------------------------------------------------------------------
def blend(a, b, t):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960); c = cairo.Context(s)
    c.set_source_surface(a, 0, 0); c.paint(); c.set_source_surface(b, 0, 0); c.paint_with_alpha(t)
    return s


def t5():
    import on4_props as pr
    import random
    fr = []
    hx, hy = pr.LAMP[0] - 40, pr.LAMP[1] - 90
    ax, ay = st.A_LAMP
    b = (hx - (ax - 270) / 1.6, hy - (ay - 480) / 1.6, 1.6)   # v3: wider, the sleeper in frame; the lamp's head on frame 0's streetlamp
    for _ in range(6):
        fr.append(draw(shot("8.1")))                         # the rota over the cups, her head down
    r = random.Random(5)
    def close(d, rain):
        import sys
        held = [(m, m.shredder) for m in list(sys.modules.values()) if callable(getattr(m, "shredder", None))]
        for m, _f in held:                                   # v5: no shredder in the last shot (seen in the dark by both cold viewers)
            m.shredder = lambda *a, **kw: None
        try:
            s = draw(shot("8.1", cam=b, protect=()))
        finally:
            for m, f_ in held:
                m.shredder = f_
        s = dark(s, 0.88 * d, ax, ay + 20)
        c = cairo.Context(s); g = cairo.LinearGradient(0, ay + 180, 0, ay + 236)                    # v4: the floor (the shredder) goes first
        g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0.01, 0.01, 0.02, min(1.0, d * 1.6))
        c.set_source(g); c.paint()
        if rain and CAT[0]:                                  # v6: two eyes open in the dark; the loop, and the cat leaps
            import cat_on as ct
            c = cairo.Context(s)
            for ex in (118, 150):
                ct._eye(c, ex, 640, 9, "closed" if rain < 0.5 else "open", slit=rain >= 1.0)
        if rain:
            c = cairo.Context(s); c.set_source_rgba(1, 1, 1, 0.5 * rain); c.set_line_width(2)
            for _ in range(26):
                x = ax + r.uniform(-90, 90); y = ay + r.uniform(20, 260)
                c.move_to(x, y); c.line_to(x - 5, y + 22); c.stroke()
        return s
    for d in (0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.0, 1.0):                                    # the room goes dark round the lamp
        fr.append(close(d, 0))
    last = None
    for rn in (0.4, 0.7, 1.0, 1.0, 1.0, 1.0):                                                      # rain under it
        last = close(1.0, rn); fr.append(last)
    street = draw(shot("1.1"))
    for t in (0.17, 0.33, 0.5, 0.67, 0.83, 1.0):                                                   # the dissolve: the lamp is the streetlamp
        fr.append(blend(last, street, t))
    for _ in range(6):
        fr.append(street)
    return fr


# ---- T7 -----------------------------------------------------------------------------------------------------------------
def peel(c, x, y, s=1.0, ang=0.0):
    """a banana peel: three flaps off a stub. GOLD exactly, so the accent pass keeps a little of its colour."""
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    for a in (-1.15, 0.0, 1.15):
        c.save(); c.rotate(a)
        c.move_to(-7, 0); c.curve_to(-12, 14, -8, 30, 0, 40); c.curve_to(8, 30, 12, 14, 7, 0); c.close_path()
        c.set_source_rgb(*st.GOLD); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.0); c.stroke()
        c.restore()
    c.rectangle(-4, -12, 8, 13); c.set_source_rgb(0.25, 0.2, 0.12); c.fill()
    c.restore()


def t7():
    """2.4, v6 (Tomas): she climbs the fire escape, leans over the rail to see, goes over it into the bin below; the lid
    slams on the narrator's last word. A beat. The lid lifts: she comes up with a banana peel on her ear, sees it,
    flicks it off, hero pose, as if nothing happened. 55 drawings, 4.6 s."""
    PY, RY, GY = 330, 256, 716                               # the platform, the rail's top, the ground
    BX0, BX1, BY = 200, 420, 566                             # the bin: its mouth
    S_ = 0.50
    def bin_back(k, lid):
        c = k.c
        st.poly(k, [(BX0 + 8, BY - 6), (BX1 - 8, BY - 6), (BX1 - 8, BY + 30), (BX0 + 8, BY + 30)], (0.06, 0.06, 0.07), 2.0)   # the dark inside
        if lid > 0:                                          # the lid open: hinged at the back, standing up behind her
            h = 150 * lid
            st.poly(k, [(BX0 - 6, BY - 4), (BX1 + 6, BY - 4), (BX1 - 4, BY - 4 - h), (BX0 + 4, BY - 4 - h)], (0.30, 0.30, 0.32), 2.4)
    def bin_front(k, lid, shake=0):
        c = k.c
        c.save(); c.translate(shake, 0)
        st.poly(k, [(BX0, BY), (BX1, BY), (BX1 - 10, GY), (BX0 + 10, GY)], (0.24, 0.25, 0.26), 2.6)
        c.set_source_rgb(*INK); c.set_line_width(2)
        for x in (BX0 + 52, BX0 + 110, BX0 + 168):
            c.move_to(x, BY + 14); c.line_to(x, GY - 10); c.stroke()
        st.poly(k, [(BX0 - 8, BY - 8), (BX1 + 8, BY - 8), (BX1 + 8, BY + 8), (BX0 - 8, BY + 8)], (0.34, 0.34, 0.36), 2.4)        # the rim
        for x in (BX0 + 28, BX1 - 28):                                                                                          # wheels
            kit.ellipse(k, x, GY, 13, 13, (0.08, 0.08, 0.09), 7700 + x, shadow=False, lw=2)
        if lid == 0:
            st.poly(k, [(BX0 - 10, BY - 22), (BX1 + 10, BY - 22), (BX1 + 10, BY - 6), (BX0 - 10, BY - 6)], (0.30, 0.30, 0.32), 2.4)
        c.restore()
    def scene(k):                                            # the ground, a pavement line; the platform's shadow on the wall
        c = k.c
        st.poly(k, [(-10, GY), (550, GY), (550, 970), (-10, 970)], (0.20, 0.20, 0.21), 2.0)
        sc.platform(k, PY)
    def f(pam=None, lid=0, shake=0, fall=None, pl=None, burst=False, clip=False):
        def before(k):
            scene(k); bin_back(k, lid)
        def after(k):
            c = k.c
            sc.railing(k, RY)
            pts = None
            if fall:                                         # over the rail: drawn in front of it, turning
                x, y, ang = fall
                c.save(); c.translate(x, y); c.rotate(ang); c.translate(-x, -y)
                sc.draw_cast(k, [P("pam_cat", x, y + 60, S_, pose(lerp(HERO, oc.CAT_POSES["triumph2"][0], 0.8), ("relax_s", "relax_s")), "doubt", (0, 0.9), rim=True)])
                c.restore()
            if clip and pam:                                 # in the bin: only what shows above its rim
                pts = sc.draw_cast(k, [pam])
            bin_front(k, lid, shake)
            if burst:
                sc._burst(k, BX0 - 16, BY - 14, 26); sc._burst(k, BX1 + 16, BY - 14, 26)
            if pl:
                peel(c, *pl)
            return pts
        return draw(shot("2.4", cam=(270, 462, 1.45), cast=[pam] if (pam and not clip) else [], before=before, after=after, protect=()))
    fr = []
    for i in range(8):                                       # up the ladder
        t = i / 7.0
        fr.append(f(P("pam_cat", 105, PY + 150 * (1 - t) - (6 if i % 2 else 0), S_, "hero", "peer", (0.3, -0.6), rim=True)))
    for i in range(9):                                       # along the platform, her eyes on the street below
        t = i / 8.0
        fr.append(f(P("pam_cat", 105 + 205 * t, PY - (5 if i % 2 else 0), S_, "hero", "peer", (0.6, 0.7), rim=True)))
    for i in range(12):                                      # further over the rail, and further
        t = i / 11.0
        fr.append(f(P("pam_cat", 310, PY, S_, "hero", "peer" if t < 0.75 else "doubt", (0.4, 1.0), lean=0.62 * t * t + (0.03 if i % 2 else 0), rim=True)))
    for x, y, ang in ((330, 300, 1.7), (325, 400, 2.9), (318, 500, 3.3)):   # over she goes, head first
        fr.append(f(fall=(x, y, ang)))
    fr.append(f(lid=0, burst=True, shake=5))                 # the lid slams (the narrator's last word)
    fr.append(f(lid=0, shake=-4))
    for _ in range(5):
        fr.append(f(lid=0))                                  # a beat
    IN = lambda dy, face, look, arms="hero", lean=0.0: P("pam_cat", 310, BY + 150 - dy, S_, arms, face, look, clip_y=BY, lean=lean, rim=True)
    HEADY = lambda dy: BY + 150 - dy - 232 * S_ * 1.0
    def up(dy, lid, face, look, arms="hero", peel_on=True, pl=None):
        p = IN(dy, face, look, arms)
        return f(p, lid=lid, clip=True, pl=pl if pl else ((310 + 34, HEADY(dy) - 26, 0.9, 0.5) if peel_on else None))
    fr.append(up(20, 0.3, "fade", (0, 0)))                   # the lid lifts: ears, a peel
    fr.append(up(55, 0.7, "fade", (0, 0)))
    for dy in (90, 110, 112, 112):                           # up to the chest; the peel hangs on her ear
        fr.append(up(dy, 1.0, "fade", (0.2, 0.2)))
    for _ in range(3):                                       # her eyes go up to it
        fr.append(up(112, 1.0, "doubt", (0.8, -1.0)))
    FLICK = pose(oc.pm.ik(-1, -30, oc.BT - 30) + oc.pm.ik(1, 44, -150), ("relax_s", "fist"))
    fr.append(up(112, 1.0, "peer", (0.8, -1.0), arms=FLICK))                                        # a flick
    fr.append(up(112, 1.0, "peer", (0.6, -0.4), arms=FLICK, pl=(420, HEADY(112) - 70, 0.9, 1.9)))
    fr.append(up(112, 1.0, "proud", (0.3, 0), pl=(470, HEADY(112) + 10, 0.9, 3.2)))
    while len(fr) < 55:                                      # hero pose, in a bin: nothing happened
        fr.append(up(116, 1.0, "proud", (0.5, -0.2), peel_on=False, pl=(452, GY - 6, 0.9, 1.5)))
    return fr


# ---- T8 -----------------------------------------------------------------------------------------------------------------
def t8():
    """3.6, v9 (Tomas): the two shadows carry her in from the right, the money up in their fists, and drop her at the
    club's door; they walk on and out. She lies there; then she comes up off the pavement stiff as a plank, puts her
    mask straight, and stands where 4.1 finds her. 57 drawings, 4.75 s, in 4.1's camera."""
    import on4_lying as ly
    CAM = (270, 462, 1.05)
    X0, GYp = 400, 714                                       # where 4.1 has her; the pavement
    def bill(k, x, y, ang):
        c = k.c
        ly.bill(k, x, y, ang, 1.8, seed=0)
        c.save(); c.translate(x, y); c.rotate(ang); c.set_source_rgb(0.12, 0.16, 0.10)
        c.select_font_face("sans-serif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(18)
        c.move_to(-5, 6); c.show_text("$"); c.restore()
    def f(i):
        carry = i < 15
        cx = X0 - 96 + (1 - i / 14.0) * 330 if carry else X0 - 96         # her middle while carried (she lies head to the left)
        lift = -40 + (4 if i % 2 else 0) if carry else min(0, -40 + (i - 14) * 22)
        cast = []
        if i >= 30:                                          # up off the pavement, stiff as a plank, about her heels
            t = ease(min(1.0, (i - 30) / 11.0))
            if i < 44:
                cast = [P("pam_cat", X0, GYp, 0.70, "hero", "doubt", (0.2, -0.4), lean=-1.45 * (1 - t), rim=True)]
            elif i < 51:
                cast = [P("pam_cat", X0, GYp, 0.70, "mask_fix", "doubt", (-0.4, -0.2), rim=True)]
            else:
                cast = [P("pam_cat", X0, GYp, 0.70, "hero", "approve", (-0.4, -1), rim=True)]
        def after(k):
            c = k.c
            for j, off in enumerate((-96, 92)):              # the shadows: one at her head, one at her feet; then on, and out to the left
                x = cx + off if carry else X0 - 96 + off - max(0, i - 18) * 30
                if x < -60:
                    continue
                st.thug(k, x, GYp - 12, 0.44, "open" if i % 2 else (-30, 20, 30, -20), seed=4500 + j,
                        hands=("grab", "grab") if carry or i < 18 else ("grab", "relax"), lean=0.0)
                bill(k, x - 6, GYp - 12 - 162, 0.25 - 0.5 * j)
                if j == 0:
                    bill(k, x + 16, GYp - 12 - 172, -0.2)
            if i < 30:
                c.save(); c.translate(cx, GYp - 6 + lift); c.scale(0.66, 0.66); c.translate(-330, -690); ly.body(k); ly.head(k, *ly.HEAD, ly.ANG); c.restore()
            if i in (16, 17):                                # dropped
                sc._burst(k, X0 - 200, GYp - 4, 22); sc._burst(k, X0 + 10, GYp - 4, 22)
        return draw(shot("4.1", cam=CAM, cast=cast, after=after, protect=()))
    return [f(i) for i in range(57)]


TESTS = {"T1": t1, "T2": t2, "T3": t3, "T4": t4, "T5": t5, "T6": t6, "T7": t7, "T8": t8}


def build(name):
    fr = TESTS[name]()
    d = "/tmp/on4_mot/%s" % name
    os.makedirs(d, exist_ok=True)
    for f_ in os.listdir(d):
        os.remove(os.path.join(d, f_))
    for i, s in enumerate(fr):
        s.write_to_png(os.path.join(d, "%03d.png" % i))
    mp4 = os.path.join(OUT, "on4_motion_%s_v4.mp4" % name.lower())
    tmp = mp4[:-4] + "_tmp.mp4"
    r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(d, "%03d.png"),
                        "-vf", "fps=24,format=yuv420p", "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", tmp])
    if r.returncode == 0:
        os.replace(tmp, mp4)
    cols = 10; rows = (len(fr) + cols - 1) // cols; w, h = 270, 480
    sh = cairo.ImageSurface(cairo.FORMAT_RGB24, cols * (w + 8) + 8, rows * (h + 26) + 8)
    c = cairo.Context(sh); c.set_source_rgb(0.96, 0.95, 0.92); c.paint()
    for i, s in enumerate(fr):
        x = 8 + (i % cols) * (w + 8); y = 8 + (i // cols) * (h + 26)
        c.save(); c.translate(x, y); c.scale(0.5, 0.5); c.set_source_surface(s, 0, 0); c.paint(); c.restore()
        c.set_source_rgb(0.1, 0.1, 0.1); c.select_font_face("Inter", 0, 1); c.set_font_size(13)
        c.move_to(x, y + h + 16); c.show_text("%d   %.2f s" % (i + 1, i / FPS))
    png = os.path.join(OUT, "on4_motion_%s_v4.png" % name.lower())
    sh.write_to_png(png)
    sh.write_to_png("/tmp/on4_mot/%d.png" % (list(TESTS).index(name) + 1))
    return mp4, png, len(fr)


if __name__ == "__main__":
    for n in (sys.argv[1:] or list(TESTS)):
        print(n, build(n))
