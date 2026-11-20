"""OFFICE NOIR 3: the whole film as one moving rough (20 Nov), v3 (v1, v2: film_on3_v1.py, _v2.py). v3 (Tomas,
/grill-me): Don comes into the ring as a fighter does, through the FIGHTERS door, crossed lights, fountains of sparks,
fireworks (6.2b); the folder goes into the hoodie's pocket (4.2); the Referee's sleeves reach his wrists; one close
shot each for what a phone loses: the bill (2.0), the matches (3.2b, closer), the ring girl's face (5.1a2), the
garage wall (8.2b). v2: v2, Tomas's notes on v1: the
fight bill HUMAN vs ROBOT; a long limousine; her picture is a plain identity photograph and on the street she is a
woman under an umbrella; the matches in three stages; the shadows turn on Don and his hands go up; in 5.1c the bell
rings while Pam has the robe half off him; in 6.3 Don's glass goes from the photograph to the ring girl: the same face.
v1: No sound, no text. 30 fps, 540x960.
Beats 01 to 04 and 08 move here for the first time (parameters of the staged frames, run through time); beats 05 to 07
are the ring roughs' own shots (ring_rough_on3 v9, ring_rough2_on3 v3), with the button's insert cut in after 5.4 and
inside 7.4. The last frame is the first frame: 8.5 ends on 1.1's first drawing.
render(out) -> the film. sheets(d) -> contact sheets at 2 fps, numbered, and one small sheet."""
import math
import os
import cairo
import ring_rough_on3 as rr
import ring_rough2_on3 as rr2
import street_on3 as st
import street_casts_on3 as stc
import alley_on3 as al
import door_on3 as dr
import office_on3 as of
import garage_on3 as ga
import client_on3 as b
from ring_rough_on3 import lerp

R5, F5 = tuple(rr.SHOTS), dict(rr.FN)
st.V5[0] = True
import robot_on3 as r
import noir2_cast as n2
import ring_on3 as rg
import cast_on3 as ca
import sofia_on3 as so3
import client_sheet_on3 as csh
from kit import Ctx, rect
ca.LONG[0] = True
K = dict(cards="deck", v4=True, v6=True)
T0 = 0.45                                                   # ring_rough2's 7.5 at this time is the film's first drawing: the glove an inch away


def ramp(t, a, d):
    """0 before a, 1 after a + d, smooth between."""
    return lerp(0.0, 1.0, (t - a) / d)


def bob(t, n=3.2, h=3.0):
    return abs(math.sin(t * math.pi * n)) * h


# ---- 01 the punch -------------------------------------------------------------------------------------------------
def s11(t):
    return rr2.shot_75(T0 + t)                               # lands at 0.3 s, white by 0.5


# ---- 02 the street ------------------------------------------------------------------------------------------------
def _rain(t):
    return 1 + int(t * 10) % 4


def s20(t):
    """The bill, as large as the frame, rain on it: TONIGHT, HUMAN vs ROBOT."""
    s_ = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(s_); k = Ctx(c, 0)
    c.set_source_rgb(0.20, 0.20, 0.23); c.paint()
    c.set_source_rgb(0.12, 0.12, 0.14); c.set_line_width(4)
    for i in range(12):
        y = i * 84 - 10
        c.move_to(0, y); c.line_to(540, y); c.stroke()
        for j in range(-1, 5):
            x = j * 150 + (75 if i % 2 else 0); c.move_to(x, y); c.line_to(x, y + 84); c.stroke()
    z = 3.25 + 0.12 * ramp(t, 0.0, 0.9)
    c.save(); c.translate(270, 470); c.scale(z, z); c.rotate(-0.03); c.translate(-(48 * 1.3 - 14), -(68 * 1.3 - 34))
    st.poster2(k, 0, 0, 1.0, 7)
    c.restore()
    c.set_source_rgba(1, 1, 1, 0.35); c.set_line_width(2.4)
    for i in range(14):
        x = (i * 137 + int(t * 10) * 61) % 560; y = (i * 251 + int(t * 10) * 173) % 980
        c.move_to(x, y); c.line_to(x - 12, y + 70); c.stroke()
    csh.noir(s_)
    return s_


def s21(t):
    return st.frame("S1", [stc.client(lerp(250.0, 400.0, t / 1.1))], rain=_rain(t))


def s22(t):
    return st.frame("S1", [stc.client(400)], car=(lerp(980.0, 250.0, t / 1.1), 0.0), rain=_rain(t))


def s24(t):
    return st.window_pov(ramp(t, 0.2, 0.4) - ramp(t, 2.4, 0.3), ramp(t, 0.7, 0.5), ramp(t, 1.4, 0.8), door=True)


def s24b(t):
    return st.frame("S2", [stc.with_folder(400)], car=(lerp(250.0, -700.0, (t - 0.2) / 1.0), 0.0), rain=_rain(t))


def s25(t):
    return st.cv_insert(0.0)


def s26(t):
    return st.frame("S3", [stc.sofia(lerp(900.0, 690.0, t / 0.9)), stc.with_folder(450)], rain=_rain(t))


def s27(t):
    return st.cv_insert(0.0 if t < 0.35 else 1.0)


# ---- 03 the alley -------------------------------------------------------------------------------------------------
def s31(t):
    return al.frame2("A1", [al.client(lerp(-30.0, 70.0, t / 1.0))], al.gang("aim", ramp(t, 0.5, 0.8) * 0.5))


def s32(t):
    return al.frame2("A2w", [al.fumble(130, stage=0, shake=math.sin(t * 26) * 1.5)], al.gang("aim", 0.5 + 0.5 * ramp(t, 0.0, 1.0)))


def s32b(t):
    """The matches, close, in three stages: the box whole and squeezed; crushed, they spill; the last one snaps."""
    (lx, ly), (rx, ry) = al._probe(130)["hands"]
    cam = ((lx + rx) / 2 + 4, (ly + ry) / 2 + 14, 5.4)        # v3: closer: two gloves and what is between them, nothing else
    if t < 0.45:
        f = al.fumble(130, stage=0, shake=math.sin(t * 40) * 2.0)
    elif t < 1.05:
        f = al.fumble(130, stage=1, shake=(t - 0.45) / 0.5)
    else:
        f = al.fumble(130, stage=2, shake=(t - 1.05) / 0.6)
    return al.frame2(cam, [f], al.gang("aim", 1))


def s33(t):
    return al.frame2("A3w", [al.fumble(150, stage=2, shake=1.0)], al.gang("aim" if t < 0.45 else "down", 1))


def s33b(t):
    tx, ty = al._tip(130)
    lit = t > 0.75
    return al.frame2("A2", [al.fumble(130, lit=lit), al.lighter_hand(tx + 13 + lerp(230.0, 0.0, t / 0.45), ty + 46, 0.9, flame=t > 0.5)], al.gang("down", 1))


def s34(t):
    x = lerp(180.0, 700.0, t / 1.3)
    return al.frame2("A1", [al.client(x, "b_walk", (0.9, 0), cig=x < 300)], al.gang("down", 0, True), cig=300 if x >= 300 else None)


def s34b(t):
    """Don, bent over the cigarette end. Behind him the three turn back and everything comes up at him. His hands go up."""
    if t < 0.9:
        return al.frame2("A3w", [al.don_caught(lerp(60.0, 215.0, t / 0.7), 0.0)], al.gang("down", 0, True), cig=300)
    return al.frame2("A3w", [al.don_caught(215, 0.0 if t < 1.35 else 1.0)], al.gang("aim", ramp(t, 0.9, 0.5)), cig=300)


# ---- 04 the price -------------------------------------------------------------------------------------------------
def s41(t):
    return dr.behind(ramp(t, 0.5, 0.6))


def s42(t):
    if t < 0.5:
        return dr.face((0.2, -0.9), pocket=0.0)              # up at the roll
    if t < 1.0:
        return dr.face((-0.7, 0.9), pocket=0.0)              # down at the folder
    if t < 1.6:
        return dr.face((-0.7, 0.9), pocket=ramp(t, 1.0, 0.5))    # into the pocket with it
    return dr.face((0.2, -0.9), pocket=1.0)                  # and up again


def s43(t):
    return of.over(ramp(t, 0.2, 0.5), show=True, cards="deck", v4=True)


def s44(t):
    pay = 0.0 if t < 0.5 else 0.3 + 0.7 * ramp(t, 0.5, 0.45)
    take = 1.0 if t >= 1.2 else 0.0
    tk = ramp(t, 1.6, 0.5) if t >= 1.6 else None
    return of.reverse(pay, take, turn=0 if take else None, ticket=tk, **K)


def s44a(t):
    return of.ticket_insert(ramp(t, 0.0, 0.35))


def s44t(t):
    return of.reverse(1.0, 1.0, turn=ramp(t, 0.1, 1.0), ticket=1.0, eyes=(0.3, 0.9) if t > 0.9 else None, **K)


def s44b(t):
    return of.tower_insert(ramp(t, 0.3, 0.5), v5=True)


def s44c(t):
    return dr.react(t >= 0.8)


# ---- 05 to 07 the ring: the roughs' own shots, with the button ----------------------------------------------------
def s51c(t):
    """Pam: "I'll help you undress." She has the robe off his shoulders and is pulling at the sleeve when the bell goes
    (the Referee's arm comes down). "Ah. Too late. The bell." She shoves it back up over him."""
    if t < 2.0:
        return F5["5.1c"](t)
    if t < 2.5:
        u = (t - 2.0) / 0.5

        def ref(k):
            c = k.c                                          # the ring's bell on its board, beside him; his hand comes down on it
            bx, by = 400, rg.F - 236
            rect(k, bx - 30, by - 34, 60, 76, (0.30, 0.26, 0.22), 3, shadow=False, lw=2.4)
            c.set_source_rgb(0.86, 0.86, 0.82); c.arc(bx, by, 24, 0, 2 * math.pi); c.fill_preserve(); c.set_source_rgb(0.08, 0.08, 0.09); c.set_line_width(2.6); c.stroke()
            c.arc(bx, by, 6, 0, 2 * math.pi); c.fill()
            if u >= 0.4:
                c.set_source_rgb(0.08, 0.08, 0.09); c.set_line_width(5); c.move_to(bx - 40, by + 44); c.line_to(bx - 14, by + 12); c.stroke()
            ca.referee(k, 336, rg.F - 96, rg.SC * ca.REL_REF, "ref_bell" if u < 0.4 else "ref_stand", look=(-0.8, 0), waistcoat=True)
            if u >= 0.4:                                     # the bell: rings out from his hand
                c = k.c; c.set_source_rgb(0.96, 0.96, 0.92); c.set_line_width(2.4)
                for r_ in (26, 40, 54):
                    c.new_path(); c.arc(400, rg.F - 236, 14 + r_ * (0.6 + 0.8 * (u - 0.4) / 0.6), -2.6, -0.5); c.stroke()
        return rg.frame((336, rg.F - 230, 2.3), [ref], [], near=False, hats=False)
    return F5["5.1c"](2.3 + (t - 2.5))


def s63(t):
    """Don's tweezers lift the folder away. In his glass: her photograph, the one from the CV. The glass leaves the
    photograph and finds the ring girl herself: the same face. (6.4: CASE CLOSED.)"""
    if t < 1.2:
        return rr2.shot_63(t)
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(s); k = Ctx(c, 0)
    c.set_source_rgb(0.08, 0.08, 0.09); c.paint()
    grow = lerp(0.86, 1.0, (t - 1.2) / 0.3)
    slide = 620 * ramp(t, 2.0, 0.45)
    c.save(); c.translate(270, 440); c.scale(grow, grow); c.translate(-270, -440)
    c.set_source_rgb(0.10, 0.10, 0.11); c.set_line_width(40); c.set_line_cap(1); c.move_to(420, 640); c.line_to(540, 900); c.stroke()
    c.save(); c.arc(270, 440, 232, 0, 2 * math.pi); c.clip()
    c.set_source_rgb(0.72, 0.72, 0.74); c.paint()                                                 # the ring's light, behind her
    c.save(); c.translate(-slide, 0)
    c.set_source_rgb(0.86, 0.80, 0.62); c.rectangle(-200, 0, 640, 960); c.fill()                  # the folder's inside
    rect(k, 110, 250, 320, 400, (0.96, 0.96, 0.93), 3, shadow=False, lw=3)                        # her photograph, as on the CV
    c.save(); c.rectangle(112, 252, 316, 396); c.clip(); c.set_source_rgb(0.62, 0.62, 0.64); c.paint()
    st.her(k, 270, 380 + 272 * 2.2, 2.2); c.restore()
    rect(k, 248, 236, 44, 30, (0.70, 0.70, 0.74), 9, shadow=False, lw=2)                          # its clip
    so3.sofia(k, 270 + 620, 470 + 272 * 2.3, 2.3, "r_hips", "spotted", (0, 0))                    # the ring girl, herself
    c.restore(); c.restore()
    c.set_source_rgb(0.10, 0.10, 0.11); c.set_line_width(22); c.arc(270, 440, 236, 0, 2 * math.pi); c.stroke()
    c.set_source_rgba(1, 1, 1, 0.5); c.set_line_width(10); c.arc(270, 440, 200, 3.6, 4.5); c.stroke()
    c.restore()
    csh.noir(s)
    return s


def s51a2(t):
    """The ring girl, close, as the card goes by: the face from the photograph, a feather on it now."""
    s_ = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(s_); k = Ctx(c, 0)
    g = cairo.RadialGradient(270, 200, 40, 270, 300, 900); g.add_color_stop_rgba(0, 0.86, 0.86, 0.88, 1); g.add_color_stop_rgba(1, 0.22, 0.22, 0.25, 1); c.set_source(g); c.paint()
    x = lerp(330.0, 250.0, t / 0.9)
    so3.sofia(k, x, 520 + 272 * 3.4, 3.4, "r_card", "smile" if t < 0.5 else "spotted", (-0.6, 0.0), card_="ROUND 1")
    csh.noir(s_)
    return s_


def s62b(t):
    """Don comes in as a fighter does: the door at the back opens white, two lights cross on him, fountains of sparks
    go up either side of the aisle, fireworks over the hats. He walks it with his glass held up like a belt. The Client,
    on his stool, and the robot both turn to look."""
    dx0, dy0, dw, dh = rg.DOOR
    u = ramp(t, 0.5, 1.7)
    px, pf, ps = lerp(dx0 + dw / 2.0, 330.0, u), lerp(rg.FAR + 6.0, rg.F - 8.0, u), rg.SC * lerp(0.74, 1.0, u)
    hy = pf - 330 * ps

    def lights(k):                                           # behind everything in the ring: the door, white; fireworks; the two beams
        c = k.c
        c.set_source_rgb(0.98, 0.98, 0.94); c.rectangle(dx0, dy0, dw, dh); c.fill()
        for i, (fx, fy, t0) in enumerate(((150, rg.FAR - 420, 0.3), (430, rg.FAR - 470, 0.7), (270, rg.FAR - 520, 1.1), (600, rg.FAR - 430, 1.5), (90, rg.FAR - 500, 1.8))):
            a = (t - t0) / 0.7
            if 0 < a < 1:
                c.set_source_rgba(1, 1, 1, 1 - a * 0.7); c.set_line_width(3.4); c.set_line_cap(1)
                for j in range(14):
                    an = j * math.pi / 7 + i
                    c.move_to(fx + math.cos(an) * 60 * a * 0.5, fy + math.sin(an) * 60 * a * 0.5); c.line_to(fx + math.cos(an) * (30 + 78 * a), fy + math.sin(an) * (30 + 78 * a) + 22 * a * a); c.stroke()
                c.set_line_cap(0)
        for sx in (-1, 1):
            c.set_source_rgba(1, 1, 1, 0.26 * ramp(t, 0.2, 0.3)); c.new_path()
            c.move_to(360 + sx * 420, rg.FAR - 640); c.line_to(px - 70 * ps, hy + 380 * ps); c.line_to(px + 70 * ps, hy + 380 * ps); c.close_path(); c.fill()

    def fountains(k):                                        # either side of his way in, at the ring's far edge
        c = k.c
        for sx in (-1, 1):
            bx, by = dx0 + dw / 2 + sx * 86, rg.FAR - 96
            c.set_source_rgb(0.99, 0.99, 0.95); c.set_line_width(2.6); c.set_line_cap(1)
            for j in range(18):
                ph = (t * 3.1 + j * 0.37) % 1.0
                an = -math.pi / 2 + (j - 8.5) * 0.085
                c.move_to(bx + math.cos(an) * 150 * ph, by + math.sin(an) * 150 * ph + 60 * ph * ph)
                c.line_to(bx + math.cos(an) * 150 * (ph + 0.08), by + math.sin(an) * 150 * (ph + 0.08) + 60 * (ph + 0.08) ** 2); c.stroke()
            c.set_line_cap(0)
            rect(k, bx - 8, by - 4, 16, 22, (0.10, 0.10, 0.12), 60 + sx, shadow=False, lw=2)

    def don(k):
        rg.shadow(k, px, pf, 36 * ps / rg.SC)
        old = n2.LOOK[0]; n2.LOOK[0] = 9
        try:
            n2.detective(k, px, pf, ps, "up", "squint", (-0.5, 0.2), lean=0)
        finally:
            n2.LOOK[0] = old

    def client(k):
        rr2._seated(k, True, look=(0.9, -0.2), face="tired")

    def robot(k):
        x, y, s_ = rg.HOME["robot_corner"]
        rg.shadow(k, x + 84, y, 40); r.robot(k, x + 84, y, s_, "r_wait", "ask", side=-1)
    return rg.frame((lerp(470.0, 372.0, u), lerp(rg.F - 300.0, rg.F - 250.0, u), lerp(1.5, 1.28, u)), [lights, fountains, don, client, robot], [], door=True)


def s54b(t):
    return of.button_insert(ramp(t, 0.0, 0.2))


def s74a(t):
    return rr2.shot_74(t)                                    # the cracked screen asks; her office (to 1.1)


def s74c(t):
    return rr2.shot_74(1.1 + t)                              # her mouth; the tick


# ---- 08 awake -----------------------------------------------------------------------------------------------------
def _buzzing(fn, t):
    real = ga.buzz
    if int(t * 8) % 2:
        ga.buzz = lambda *a, **k_: None
    try:
        return fn()
    finally:
        ga.buzz = real


def s81(t):
    return ga.f81(eye=t > 0.7)


def s82(t):
    return _buzzing(ga.f82, t)


def s83(t):
    return _buzzing(ga.f83, t)


def s84(t):
    return _buzzing(ga.f84, t)


def s85(t):
    """Into the red of the gown; the red goes dark; out of the dark, the first drawing."""
    first = rr2.shot_75(T0)
    if t >= 0.9:
        return first
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(s)
    if t < 0.4:
        src = ga.f84(); z = 1 + 9 * ramp(t, 0.0, 0.4)
        c.translate(270, 480); c.scale(z, z); c.translate(-353, -565); c.set_source_surface(src, 0, 0); c.paint()   # the gown over his head
        c.identity_matrix(); c.set_source_rgba(*b.GOWN, ramp(t, 0.15, 0.25)); c.paint()
    else:
        u = ramp(t, 0.4, 0.3)
        c.set_source_rgb(*[v * (1 - u) for v in b.GOWN]); c.paint()
        if t > 0.7:
            c.set_source_surface(first, 0, 0); c.paint_with_alpha(ramp(t, 0.7, 0.2))
    return s


FILM = [("1.1", 0.6, s11),
        ("2.0", 0.9, s20), ("2.1", 1.1, s21), ("2.2", 1.5, s22), ("2.4", 2.8, s24), ("2.4b", 1.3, s24b), ("2.5", 1.4, s25), ("2.6", 1.5, s26), ("2.7", 2.0, s27),
        ("3.1", 1.3, s31), ("3.2", 1.0, s32), ("3.2b", 1.8, s32b), ("3.3", 1.1, s33), ("3.3b", 1.6, s33b), ("3.4", 1.3, s34), ("3.4b", 2.3, s34b),
        ("4.1", 1.6, s41), ("4.2", 1.9, s42), ("4.3", 1.5, s43), ("4.4", 2.2, s44), ("4.4a", 0.9, s44a), ("4.4t", 1.4, s44t), ("4.4b", 1.3, s44b), ("4.4c", 1.4, s44c)]
for name, dur in R5:
    if name == "5.4":
        FILM += [("5.4", 1.3, F5["5.4"]), ("5.4b", 0.5, s54b)]
    elif name == "5.1c":
        FILM.append(("5.1c", 3.4, s51c))
    elif name == "5.1a":
        FILM += [("5.1a", dur, F5["5.1a"]), ("5.1a2", 0.9, s51a2)]
    else:
        FILM.append((name, dur, F5[name]))
for name, dur in rr2.SHOTS:
    if name == "7.4":
        FILM += [("7.4", 1.1, s74a), ("7.4b", 0.45, s54b), ("7.4c", 0.7, s74c)]
    elif name == "6.3":
        FILM += [("6.2b", 2.4, s62b), ("6.3", 3.1, s63)]
    else:
        FILM.append((name, dur, rr2.FN[name]))
FILM += [("8.1", 1.6, s81), ("8.2", 1.6, s82), ("8.2b", 1.0, lambda t: ga.f82b()), ("8.3", 2.2, s83), ("8.4", 2.2, s84), ("8.5", 1.0, s85)]


def _use():
    rr.SHOTS = tuple((n, d) for n, d, _ in FILM)
    rr.FN = {n: f for n, _, f in FILM}


def render(out):
    _use(); rr.render(out)


def frame_at(T):
    for n, d, f in FILM:
        if T < d - 1e-9:
            return n, f(round(T * 30) / 30)
        T -= d
    n, d, f = FILM[-1]
    return n, f(d - 1 / 30)


def total():
    return sum(d for _, d, _ in FILM)


def _sheet(tiles, out, w, cols):
    h = int(w * 960 / 540); rows = -(-len(tiles) // cols)
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, cols * (w + 6) + 6, rows * (h + 30) + 6); c = cairo.Context(s)
    c.set_source_rgb(0.13, 0.13, 0.15); c.paint()
    for i, (lab, f) in enumerate(tiles):
        x, y = 6 + (i % cols) * (w + 6), 26 + (i // cols) * (h + 30)
        c.save(); c.translate(x, y); c.scale(w / 540, w / 540); c.set_source_surface(f, 0, 0); c.paint(); c.restore()
        c.set_source_rgb(1, 1, 1); c.select_font_face("sans", 0, 1); c.set_font_size(15); c.move_to(x + 2, y - 7); c.show_text(lab)
    s.write_to_png(out)


def sheets(d, fps=2.0, per=16):
    """Numbered tiles with the time in seconds; shots under 0.7 s get a tile of their own so nothing is skipped."""
    os.makedirs(d, exist_ok=True)
    times, T = [], 0.0
    for n, dur, _ in FILM:
        k_ = max(1, round(dur * fps))
        times += [T + dur * (i + 0.5) / k_ for i in range(k_)]
        T += dur
    tiles = [("%d  %.1fs" % (i + 1, tt), frame_at(tt)[1]) for i, tt in enumerate(times)]
    for j in range(0, len(tiles), per):
        _sheet(tiles[j:j + per], os.path.join(d, "sheet_%02d.png" % (j // per + 1)), 240, 8)
    _sheet(tiles, os.path.join(d, "sheet_small.png"), 120, 16)
    return len(tiles)


if __name__ == "__main__":
    import sys
    print("%.1f s, %d shots" % (total(), len(FILM)))
    if len(sys.argv) > 2:
        print(sheets(sys.argv[2]))
    render(sys.argv[1])
