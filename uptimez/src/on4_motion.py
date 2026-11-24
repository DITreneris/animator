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
FPS = 8
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


# ---- T1: the punch ----------------------------------------------------------------------------------------------------------
HERO = oc.CAT_POSES["hero"][0]
WIND = oc.pm.ik(-1, -30, oc.BT - 30) + oc.pm.ik(1, 50, -128)
PUNCH = oc.CAT_POSES["punch"][0]


def t1():
    fr = []
    def f(arms, lean, face, look, sof, shadow, burst=False, sof_face="appraise"):
        sx, sy, ss = sof
        cast = sc.A_SHADOW() + [P("sofia", sx, sy, ss, "hold", sof_face, (0.2, 1.0))] * (sy < 1150) + \
            [P("pam_cat", 220, 730, 0.84, pose(arms, ("fist", "fist")), face, look, lean=lean)]
        if sy > 760:                                         # past Pam: nearer than her, drawn over her
            cast = [cast[-1]] + cast[:-1][2:] if False else sc.A_SHADOW() + [cast[-1]] + [c_ for c_ in cast if c_[0] == "sofia"]
        st_, sl = shadow
        return draw(shot("1.1", cast=cast, before=lambda k: sc.wall_shadow(k, st_, sl),
                         after=(lambda k: sc._burst(k, 98, 544, 34)) if burst else None))
    S0 = (330, 650, 0.50)
    def sof(i):                                              # she never stops: a step every drawing
        t = i / 20.0
        return (330 + 60 * t, 650 + 520 * t * t + 60 * t, 0.50 + 0.45 * t)
    i = 0
    for _ in range(4):                                       # 0.5 s: the threat, held (frame 0)
        fr.append(f(HERO, 0, "proud", (-0.6, -0.4), sof(i), ("aim", 0))); i += 1
    for t in (0.5, 1.0):                                     # the wind-up: her fist back, her weight back
        fr.append(f(lerp(HERO, WIND, t), 0.06 * t, "peer", (-0.8, -0.3), sof(i), ("aim", 0))); i += 1
    fr.append(f(PUNCH, -0.10, "peer", (-0.8, -0.3), sof(i), ("aim", 0), burst=True)); i += 1     # the strike
    fr.append(fr[-1]); i += 1                                # the hit, held
    for sl in (0.3, 0.6, 0.85, 1.0):                         # the shadow squashes and slides down the wall
        fr.append(f(PUNCH, -0.10 + 0.04 * sl, "peer", (-0.8, -0.1), sof(i), ("down", sl))); i += 1
    for t in (0.5, 1.0):                                     # back to the hero pose: she turns to be thanked
        fr.append(f(lerp(PUNCH, HERO, t), -0.06 * (1 - t), "proud", (0.6, 0.2), sof(i), ("down", 1.0))); i += 1
    for _ in range(6):                                       # Sofia walks past her and out; the pose held at nobody
        fr.append(f(HERO, 0, "proud" if _ < 3 else "fade", (0.7, 0.5), sof(i), ("down", 1.0))); i += 1
    return fr


# ---- T2: the envelope ---------------------------------------------------------------------------------------------------------
def t2():
    fr = []
    wide = lambda coat: draw(shot("2.2"), {"coat": coat})
    for _ in range(4):
        fr.append(wide(0.0))                                 # on his knee; her ears at the window
    for tap, dad in ((1, 0), (0, 0), (1, 0), (0, 0), (0, 0.5), (0, 1), (0, 1), (0, 1)):   # two taps; Dad's hand comes flat
        fr.append(draw(shot("2.3"), {"tap": tap, "dad": dad}))
    for t in (0.0, 0.3, 0.6, 0.85, 1.0, 1.0, 1.0, 1.0):      # into his own coat, under the lapel
        fr.append(wide(t))
    return fr


# ---- T3: STOP, GO, the bump ---------------------------------------------------------------------------------------------------
def t3():
    fr = []
    RUN = (-50, 30, 50, -40); RUN2 = (40, -30, -40, 30)
    STOPP = oc.CAT_POSES["stop_palm"][0]
    cam = (270, 610, 1.5)
    def f(car, don, pam, burst=False, loc="C_turn"):
        kind, px, arms, gest, lean, face = pam
        dpose, dface, dkw = don
        cast = [P("don", 140, 700, 0.56, dpose, dface, (0.4, -0.8), **dkw)]
        if kind == "front":
            cast.append(P("pam_cat", px, sc.ROAD_Y + 6, 0.62, pose(arms, gest), face, (-0.6, -0.3), lean=lean))
        else:
            cast.append(P("pam_from_behind", px, sc.ROAD_Y + 10, 0.66, pose(arms, gest), face, (0, -0.2), lean=lean))
        return draw(shot("3.1", loc=loc, cam=cam, cast=cast, protect=(),
                         after=(lambda k: sc._burst(k, 300, 664, 40)) if burst else None), {"car": car})
    D_STOP = ("stop", "confused", dict(paddle_side="STOP", chin=1))
    D_EDGE = ((-8, 0, 92, -40), "confused", dict(paddle_side="EDGE", chin=1))
    D_GO = ("wave", "pleased", dict(paddle_side="GO", paddle_ang=0.10, whistle_in=True))
    FAR = (640, 0.52)
    # she runs in from the right, after the car; the car waits at the junction; STOP held out at her side
    for i, px in enumerate((520, 470, 420, 372)):
        fr.append(f(FAR, D_STOP, ("front", px, RUN if i % 2 == 0 else RUN2, ("fist", "fist"), -0.14, "peer")))
    for px in (330, 300):                                    # she sees the paddle: she stops, dead centre of the car's path
        fr.append(f(FAR, D_STOP, ("front", px, oc.CAT_POSES["hero"][0], ("fist", "fist"), 0.0, "approve")))
    fr.append(f(FAR, D_EDGE, ("front", 300, oc.CAT_POSES["hero"][0], ("fist", "fist"), 0.0, "approve")))   # the flip
    for cy, cs in ((652, 0.62), (664, 0.76)):                # GO, the toot: the car rolls; she is still facing the paddle
        fr.append(f((cy, cs), D_GO, ("front", 300, oc.CAT_POSES["hero"][0], ("fist", "fist"), 0.0, "approve")))
    for cy, cs in ((676, 0.90), (688, 1.02)):                # she turns to the headlights: one palm out
        fr.append(f((cy, cs), D_GO, ("back", 294, STOPP, ("relax_s", "palm"), 0.0, "approve"), loc="C_bump"))
    fr.append(fr[-1])                                        # the pause before (lesson 158)
    hit = f((702, 1.15), D_GO, ("back", 292, STOPP, ("relax_s", "palm"), -0.22, "approve"), burst=True, loc="C_bump")
    fr += [hit, hit]                                         # the bump, held
    for lean in (-0.5, -0.9, -1.35):                         # over backwards onto the stripes
        fr.append(f((702, 1.15), D_GO, ("back", 292 - lean * 100, STOPP, ("relax_s", "palm"), lean, "approve"), loc="C_bump"))
    for _ in range(3):                                       # she is down; he is still waving GO
        fr.append(fr[-1])
    return fr


# ---- T4: the arm comes down; the match cut ---------------------------------------------------------------------------------------
def t4():
    fr = []
    UP = oc.CAT_POSES["triumph2"][0]; DOWN = (-8, 0, 8, 0)
    for _ in range(4):                                       # held up, in the light: Well?
        fr.append(draw(shot("6.3")))
    def close(t, face, look):
        arms = lerp(UP, DOWN, ease(t))
        cast = [P("pam_cat", 262, 950, 1.5, pose(arms, ("relax_s", "fist")), face, look, env=True, rim=True)]
        return dark(draw(shot("6.6", cast=cast)), 0.0)
    for _ in range(3):                                       # close: still up; her eyes go across the room: nobody
        fr.append(close(0.0, "proud" if _ == 0 else "hopeful", ((-0.8, 0), (0.8, 0), (0.8, 0))[_]))
    for t in (0.2, 0.45, 0.7, 0.9, 1.0):                     # the arm comes slowly down
        fr.append(close(t, "fade" if t > 0.3 else "doubt", (0.3, 0.6)))
    for _ in range(3):
        fr.append(close(1.0, "fade", (0.4, 0.9)))            # Of course.
    up_again = close(0.0, "fade", (0.4, 0.9))                # the dream's last picture: the arm up (the shape of the match)
    fr.append(up_again)
    for _ in range(5):                                       # the match: asleep on the counter, the arm up
        fr.append(draw(shot("7.1")))
    return fr


# ---- T5: the loop ------------------------------------------------------------------------------------------------------------------
def t5():
    import on4_props as pr
    import on4_street as st
    fr = []
    a = BY["8.1"]["cam"]
    hx, hy = pr.LAMP[0] - 40, pr.LAMP[1] - 90
    ax, ay = st.A_LAMP
    b = (hx - (ax - 270) / 2.4, hy - (ay - 480) / 2.4, 2.4)   # the lamp's head on frame 0's streetlamp
    for _ in range(4):
        fr.append(draw(shot("8.1")))                         # the rota over the cups, the mask down, her head on her arm
    for t in (0.15, 0.35, 0.55, 0.75, 0.9, 1.0):             # the push to the lamp; the room goes dark round it
        e = ease(t)
        s = draw(shot("8.1", cam=lerp(a, b, e), protect=()))
        lx, ly = sc._to_screen(lerp(a, b, e), (hx, hy))
        fr.append(dark(s, 0.97 * e, lx, ly + 20))
    for _ in range(2):
        fr.append(draw(shot("8.2")))
    for _ in range(6):                                       # frame 0: the streetlamp where the lamp was
        fr.append(draw(shot("1.1")))
    return fr


TESTS = {"T1": t1, "T2": t2, "T3": t3, "T4": t4, "T5": t5}


def build(name):
    fr = TESTS[name]()
    d = "/tmp/on4_mot/%s" % name
    os.makedirs(d, exist_ok=True)
    for f_ in os.listdir(d):
        os.remove(os.path.join(d, f_))
    for i, s in enumerate(fr):
        s.write_to_png(os.path.join(d, "%03d.png" % i))
    mp4 = os.path.join(OUT, "on4_motion_%s_v1.mp4" % name.lower())
    tmp = mp4[:-4] + "_tmp.mp4"
    r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(d, "%03d.png"),
                        "-vf", "fps=24,format=yuv420p", "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", tmp])
    if r.returncode == 0:
        os.replace(tmp, mp4)
    cols = 8; rows = (len(fr) + cols - 1) // cols; w, h = 270, 480
    sh = cairo.ImageSurface(cairo.FORMAT_RGB24, cols * (w + 8) + 8, rows * (h + 26) + 8)
    c = cairo.Context(sh); c.set_source_rgb(0.96, 0.95, 0.92); c.paint()
    for i, s in enumerate(fr):
        x = 8 + (i % cols) * (w + 8); y = 8 + (i // cols) * (h + 26)
        c.save(); c.translate(x, y); c.scale(0.5, 0.5); c.set_source_surface(s, 0, 0); c.paint(); c.restore()
        c.set_source_rgb(0.1, 0.1, 0.1); c.select_font_face("Inter", 0, 1); c.set_font_size(13)
        c.move_to(x, y + h + 16); c.show_text("%d   %.2f s" % (i + 1, i / FPS))
    png = os.path.join(OUT, "on4_motion_%s_v1.png" % name.lower())
    sh.write_to_png(png)
    sh.write_to_png("/tmp/on4_mot/%d.png" % (list(TESTS).index(name) + 1))
    return mp4, png, len(fr)


if __name__ == "__main__":
    for n in (sys.argv[1:] or list(TESTS)):
        print(n, build(n))
