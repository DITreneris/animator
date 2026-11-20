"""OFFICE NOIR 3: the whole film as one moving rough (20 Nov), v7 (v1 to v6 pinned). v7 (Tomas): Don wears his hat
(a fedora over the headset: bald, he was taken for the machine); Sofia on the street is there: she comes after the CV
(2.5 photograph, 2.7 CV, 2.6 her), looks at him as she passes, and he lifts a glove to her. v6: v6 (Tomas, /grill-me): Pam in a
dark sweater's sleeves, hands with fingers; Don's face when he sees the gun's shadow (3.4c), then his hands up and
his knees going; Sofia walks past him under the lamp and he turns after her; the bell is three cuts, the top view is
out; the count is one, two, three, four; more time for Don's glass and CASE CLOSED and for the thumb on the red
button, less for the alley and the desk. v5: v5
(Tomas, /grill-me): Pam in sleeves to the wrist, her stopwatch on a plain cord; the robe in three held pictures (she
pulls, it sticks at the gloves; the bell, large; she waves it off and shoves it back); the hand-over at the car in
1.8 s; her hand pushes the ticket; the first punch is seen landing; his hand turns the ringing phone face down on the
CV (8.3b). v4: v4 (Tomas,
/grill-me): Don's entrance is three cuts (his outline in the white door, the aisle, over the ropes); in the alley the
gun's shadow comes down beside his head before he looks up; her one hand does everything at the desk; Pam's arms
as the Referee's; one great match for a phone (3.2c); shorter: the street, the alley, the split screen, the count and
the plaster. v3: v3 (Tomas,
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
ca.SLEEVES[0] = True
ca.DARK[0] = True
import inspect


def _hatted(orig, back=False):
    """Don with his hat on, wherever this film draws him: a grey fedora over the head the cast module returns."""
    def f(k, x, feet, s_=1.0, *a, **kw):
        o = orig(k, x, feet, s_, *a, **kw)
        hx, hy = o["head"]; c = k.c
        c.save(); c.translate(hx, hy); c.scale(s_, s_)
        felt, band = (0.34, 0.34, 0.38), (0.08, 0.08, 0.10)
        c.new_path(); c.move_to(-34, -30); c.curve_to(-36, -78, -10, -84, -2, -70); c.curve_to(8, -86, 36, -78, 34, -30); c.close_path()
        c.set_source_rgb(*felt); c.fill_preserve(); c.set_source_rgb(0.05, 0.05, 0.06); c.set_line_width(2.6); c.stroke()
        c.set_source_rgb(*band); c.rectangle(-34, -42, 68, 11); c.fill()
        c.new_path(); c.move_to(-58, -30); c.curve_to(-40, -40, 40, -40, 58, -30); c.curve_to(40, -20, -40, -20, -58, -30); c.close_path()
        c.set_source_rgb(*felt); c.fill_preserve(); c.set_source_rgb(0.05, 0.05, 0.06); c.set_line_width(2.6); c.stroke()
        c.restore()
        return o
    return f


n2.detective = _hatted(n2.detective)
n2.detective_back = _hatted(n2.detective_back, True)
K = dict(cards="deck", v4=True, v6=True)


def quick(fn, k_):
    """The same shot, k_ times faster."""
    return lambda t: fn(t * k_)
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
    """She is there. She comes along the wall under her umbrella and stops beside him; they look at each other; he knows
    the face from the photograph and lifts a glove; she nods and walks on behind him, out to the street. The camera is
    wide enough to see her go."""
    if t < 0.7:
        sx = lerp(790.0, 575.0, t / 0.7)
    elif t < 1.5:
        sx = 575.0
    else:
        sx = lerp(575.0, 250.0, (t - 1.5) / 0.9)
    stopped = 0.7 <= t < 1.5
    wave = 0.95 <= t < 1.75

    def him(k):
        stc.client(450, "b_fist" if wave else "b_pay", (0.9 if sx > 460 else -0.9, 0.0))(k)
        st.folder(k, 452 - (30 if wave else 0), stc.G - 30 - 176 * stc.Q, 0.62 * stc.SC, -0.06)

    def her(k):
        k.c.save(); k.c.translate(0, 6 * math.sin((t - 1.1) * math.pi / 0.3) if 1.1 <= t < 1.4 else 0)       # her nod
        stc.sofia(sx, (-0.9, 0.2) if (stopped or sx > 575) else (-1, 0.1))(k)
        k.c.restore()
    return st.frame((470, 1190, 1.12), [her, him], rain=_rain(t))


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
    else:
        f = al.fumble(130, stage=1, shake=(t - 0.45) / 0.5)
    return al.frame2(cam, [f], al.gang("aim", 1))


def s32c(t):
    return al.great_match(ramp(t, 0.0, 0.42) * 0.55 if t < 0.45 else 0.55 + 0.45 * ramp(t, 0.45, 0.35))


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
    """Don, bent over the cigarette end. On the wall beside his head the gun's shadow comes down and stops."""
    if t < 0.5:
        return al.frame2("A3w", [al.don_caught(lerp(60.0, 215.0, t / 0.45), 0.0)], al.gang("down", 0, True), cig=300)
    return al.frame2("A3w", [al.barrel(ramp(t, 0.5, 0.45)), al.don_caught(215, 0.0)], al.gang("down", 0, True), cig=300)


def s34c(t):
    """Close: his eyes go to it. A drop of sweat."""
    return al.frame2((262, al.G - 250, 3.1), [al.barrel(1.0), al.don_sees(215, ramp(t, 0.0, 0.6))], al.gang("down", 0, True), cig=300)


def s34d(t):
    """His hands go up; his knees are going."""
    return al.frame2("A3w", [al.barrel(1.0), al.don_caught(215 + math.sin(t * 60) * 2.2, 1.0)], al.gang("down", 0, True), cig=300)


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
    if t < 1.2:
        pay = 0.0 if t < 0.5 else 0.3 + 0.7 * ramp(t, 0.5, 0.45)
        return of.reverse(pay, 0.0, **K)
    tk = ramp(t, 2.15, 0.6) if t >= 2.15 else None           # then the same hand pushes the ticket out to him
    return of.reverse(1.0, 0.0, one=ramp(t, 1.2, 0.35) + ramp(t, 1.6, 0.5), ticket=tk, **K)


def s44a(t):
    return of.ticket_insert(ramp(t, 0.0, 0.35))


def s44t(t):
    return of.reverse(1.0, 0.0, one=2.0 + ramp(t, 0.05, 0.6) + ramp(t, 0.7, 0.5), ticket=1.0, eyes=(0.3, 0.9) if t > 1.0 else None, **K)


def s44b(t):
    return of.tower_insert(ramp(t, 0.3, 0.5), v5=True, one=True)


def s44c(t):
    return dr.react(t >= 0.8)


# ---- 05 to 07 the ring: the roughs' own shots, with the button ----------------------------------------------------
def s51c(t):
    """Three pictures, each held. 1 (to 1.3): Pam has the robe off his shoulders; the sleeve comes with her and sticks at
    the glove. "I'll help you undress." 2 (1.3 to 2.2): the bell, large: the Referee's hand on it, the sound coming off
    it. 3 (2.2 to 3.4): she lets go, one hand thrown up at the bell, and shoves the robe back up over him. "Ah. Too late.
    The bell." (Pam)"""
    if t < 1.3:
        return F5["5.1c"](min(t * 1.25, 1.6))
    if t < 2.2:
        u = (t - 1.3) / 0.9

        def ref(k):
            c = k.c
            bx, by = 392, rg.F - 240
            rect(k, bx - 34, by - 40, 68, 88, (0.30, 0.26, 0.22), 3, shadow=False, lw=2.6)
            c.set_source_rgb(0.86, 0.86, 0.82); c.arc(bx, by, 28, 0, 2 * math.pi); c.fill_preserve(); c.set_source_rgb(0.08, 0.08, 0.09); c.set_line_width(3); c.stroke()
            c.arc(bx, by, 7, 0, 2 * math.pi); c.fill()
            ca.referee(k, 320, rg.F - 96, rg.SC * ca.REL_REF, "ref_bell" if u < 0.25 else (-11, 4) + ca.cb._m_ik(1, 96, ca.cb.M_BT + 30), look=(0.8, 0), waistcoat=True)
            if u >= 0.25:
                c.set_source_rgb(0.97, 0.97, 0.93); c.set_line_width(3.4); c.set_line_cap(1)
                for i_, r_ in enumerate((36, 52, 68, 84)):
                    ph = ((u - 0.25) * 2.2 + i_ * 0.25) % 1.0
                    for a0, a1 in ((-2.7, -1.9), (-1.25, -0.45), (0.45, 1.25)):
                        c.new_path(); c.arc(bx, by, 30 + 70 * ph, a0, a1); c.stroke()
                c.set_line_cap(0)
        return rg.frame((372, rg.F - 236, 2.9), [ref], [], near=False, hats=False)
    return F5["5.1c"](2.35 + (t - 2.2) * (0.85 / 1.2))


def s55(t):
    """5.5 with the punch seen: the tick; the glove through his eyes; black; then, from outside, the piston out and its
    glove on his jaw, held; then he goes over."""
    if t < 0.9:
        return F5["5.5"](t)
    if t < 1.25:                                             # close: the grey glove on his jaw, his face folding round it (the film's first picture, without the plaster yet)
        u = (t - 0.9) / 0.35
        s_ = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(s_); k = Ctx(c, 0)
        g = cairo.RadialGradient(230, 300, 40, 230, 300, 760)
        g.add_color_stop_rgba(0, 0.80, 0.80, 0.82, 1); g.add_color_stop_rgba(1, 0.14, 0.14, 0.16, 1); c.set_source(g); c.paint()
        sc = 3.3 * b.REL
        dx = -26 * ramp(u, 0.25, 0.5)
        b.boxer(k, 210 + dx, 520 - b.HY * sc + 20, sc, "b_walk", "hard" if u < 0.2 else "shock", (0.9, 0.0))
        b.robot_glove(k, lerp(470.0, 300.0, u / 0.2) + dx * 0.6, 500, 3.0)
        if 0.2 <= u < 0.75:
            c.set_source_rgb(1, 1, 1); c.set_line_width(9); c.set_line_cap(1)
            for i in range(7):
                an = -2.6 + i * 0.5
                c.move_to(250 + 90 * math.cos(an), 470 + 90 * math.sin(an)); c.line_to(250 + 150 * math.cos(an), 470 + 150 * math.sin(an)); c.stroke()
        csh.noir(s_)
        return s_
    return F5["5.5"](0.93 + (t - 1.25))


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


def _aisle(t):
    """Don comes in as a fighter does: the door at the back opens white, two lights cross on him, fountains of sparks
    go up either side of the aisle, fireworks over the hats. He walks it with his glass held up like a belt. The Client,
    on his stool, and the robot both turn to look."""
    dx0, dy0, dw, dh = rg.DOOR
    u = ramp(t, 0.0, 1.5)
    px, pf, ps = lerp(dx0 + dw / 2.0, 372.0, u), lerp(rg.FAR + 6.0, rg.FAR + 2.0, u) - bob(t, 3.4, 5.0), rg.SC * lerp(0.74, 0.86, u)
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
            n2.detective(k, px, pf, ps, "up", "squint", (-0.5, 0.2), lean=4 * math.sin(t * math.pi * 3.4))
        finally:
            n2.LOOK[0] = old

    def client(k):
        rr2._seated(k, True, look=(0.9, -0.2), face="tired")

    def robot(k):
        x, y, s_ = rg.HOME["robot_corner"]
        rg.shadow(k, x + 84, y, 40); r.robot(k, x + 84, y, s_, "r_wait", "ask", side=-1)
    return rg.frame((lerp(470.0, 372.0, u), lerp(rg.F - 300.0, rg.F - 250.0, u), lerp(1.5, 1.28, u)), [lights, fountains, don, client, robot], [], door=True)


def s62a(t):
    """Cut 1: the FIGHTERS door, close, white. In it a black outline: a coat, a glass held up. Fireworks either side."""
    s_ = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(s_); k = Ctx(c, 0)
    c.set_source_rgb(0.04, 0.04, 0.05); c.paint()
    op = ramp(t, 0.0, 0.25)
    c.set_source_rgb(0.98, 0.98, 0.94); c.rectangle(270 - 150 * op, 170, 300 * op, 650); c.fill()
    rect(k, 150, 96, 240, 54, (0.86, 0.86, 0.82), 3, shadow=False, lw=3)
    import kit as _kit
    _kit.text(k, "FIGHTERS", 270, 124, 34, (0.07, 0.07, 0.08), bold=True)
    if op > 0.6:
        c.save(); c.rectangle(120, 170, 300, 650); c.clip()
        c.push_group()
        old = n2.LOOK[0]; n2.LOOK[0] = 9
        try:
            n2.detective(k, 270, 830 - bob(t, 3.0, 6.0), 2.1, "up", "squint", (0, 0))
        finally:
            n2.LOOK[0] = old
        pat = c.pop_group()
        c.set_source_rgb(0.03, 0.03, 0.04); c.mask(pat)                                              # only his outline
        c.restore()
    c.set_source_rgb(0.98, 0.98, 0.94); c.set_line_width(4); c.set_line_cap(1)
    for i, (fx, fy, t0) in enumerate(((70, 300, 0.15), (470, 260, 0.35), (60, 620, 0.5))):
        a = (t - t0) / 0.5
        if 0 < a < 1.2:
            for j in range(12):
                an = j * math.pi / 6 + i
                c.move_to(fx + math.cos(an) * 34 * a, fy + math.sin(an) * 34 * a); c.line_to(fx + math.cos(an) * (20 + 60 * a), fy + math.sin(an) * (20 + 60 * a)); c.stroke()
    c.set_line_cap(0)
    csh.noir(s_)
    return s_


def s62b(t):
    """Cut 2: the aisle. He walks it between the hats, the lights crossed on him, sparks either side."""
    return _aisle(t)


def s62c(t):
    """Cut 3: the ropes. One leg over, a duck under the top rope, and he is in the ring, his glass up."""
    u = ramp(t, 0.0, 0.7)
    px, pf = lerp(430.0, 340.0, u), rg.F - 14 - 26 * math.sin(math.pi * u)

    def don(k):
        rg.shadow(k, px, rg.F - 14, 36)
        old = n2.LOOK[0]; n2.LOOK[0] = 9
        try:
            n2.detective(k, px, pf, rg.SC, "up", "squint", (-0.6, 0.1), lean=-16 * math.sin(math.pi * u))
        finally:
            n2.LOOK[0] = old
        if u < 1:                                            # the rope he comes over, pressed down under him
            c = k.c; c.set_source_rgb(0.96, 0.96, 0.92); c.set_line_width(5)
            c.move_to(px - 150, rg.F - 150); c.curve_to(px - 40, rg.F - 150 + 60 * math.sin(math.pi * u), px + 40, rg.F - 150 + 60 * math.sin(math.pi * u), px + 150, rg.F - 150); c.stroke()

    def client(k):
        rr2._seated(k, True, look=(0.9, -0.1), face="tired")
    return rg.frame((300, rg.F - 210, 1.7), [client, don], [], near=False, hats=False)


def s64(t):
    """6.4 in 2.5 s, but the stamped words are held: the stamp at its own speed (to 0.55), CASE CLOSED held clear for
    0.6 s, then Don's walk out and the Referee's eyebrow, quicker."""
    if t < 0.55:
        return rr2.shot_64(t)
    if t < 1.35:
        return rr2.shot_64(0.7)
    return rr2.shot_64(0.8 + (t - 1.35) * (2.2 / 1.35))


def s52a(t):
    """The bell: three cuts, a quarter of a second each: from the front, his view of it, its view of him. The view from
    above is out (it read as blobs in four tests)."""
    return F5["5.2a"](min(int(t / 0.25), 2) * 0.25 + 0.01)


def _count_shot():
    src = inspect.getsource(rr.shot_56)
    for old_, new_ in (("    n = 1 if t < 0.6 else 2 if t < 1.2 else 3\n", "    n = min(4, 1 + int(t / 0.4))\n"),
                       ("    bob = 10 * abs(math.sin(t / 0.6 * math.pi))\n", "    bob = 16 * abs(math.sin(t / 0.4 * math.pi))\n"),
                       ("math.pi / 2 + 0.25, n, 51)", "math.pi / 2 + 0.25, n, 51, thumb=False)"),
                       ("c.set_source_rgba(0, 0, 0, 0.34)                         # the shadow of the plan", "c.set_source_rgba(0, 0, 0, 0.0)                          # the shadow of the plan (out: it read as a bar across him)")):
        assert src.count(old_) == 1, old_
        src = src.replace(old_, new_)
    ns = dict(vars(rr)); exec(src.replace("def shot_56(", "def shot_56b("), ns)
    return ns["shot_56b"]


s56 = _count_shot()                                         # one, two, three, four: a finger more every 0.4 s, no thumb, the hand dipping on each


def s63b(t):
    """6.3 with room: the tweezers and the folder as before (to 1.2), then the glass: the photograph held, the slide, the
    ring girl held; a second more in all."""
    return s63(t) if t < 1.2 else s63(1.2 + (t - 1.2) * (1.9 / 2.7))


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
        ("2.0", 0.9, s20), ("2.1", 0.8, quick(s21, 1.35)), ("2.2", 1.2, quick(s22, 1.2)), ("2.4", 1.8, quick(s24, 2.8 / 1.8)), ("2.4b", 0.9, quick(s24b, 1.4)),
        ("2.5", 1.1, s25), ("2.7", 1.7, s27), ("2.6", 2.4, s26),
        ("3.1", 0.8, quick(s31, 1.6)), ("3.2", 0.6, s32), ("3.2b", 0.9, quick(s32b, 1.1)), ("3.2c", 0.8, quick(s32c, 1.1)), ("3.3", 0.7, quick(s33, 1.25)),
        ("3.3b", 1.1, quick(s33b, 1.45)), ("3.4", 0.7, quick(s34, 1.85)), ("3.4b", 1.2, s34b), ("3.4c", 0.7, s34c), ("3.4d", 0.8, s34d),
        ("4.1", 1.3, s41), ("4.2", 1.9, s42), ("4.3", 1.0, quick(s43, 1.4)), ("4.4", 2.4, quick(s44, 2.9 / 2.4)), ("4.4a", 0.9, s44a),
        ("4.4t", 1.2, quick(s44t, 1.25)), ("4.4b", 1.0, quick(s44b, 1.2)), ("4.4c", 1.0, quick(s44c, 1.4))]
for name, dur in R5:
    if name == "5.4":
        FILM += [("5.4", 1.3, F5["5.4"]), ("5.4b", 0.5, s54b)]
    elif name == "5.1c":
        FILM.append(("5.1c", 3.4, s51c))
    elif name == "5.1a":
        FILM += [("5.1a", dur, F5["5.1a"]), ("5.1a2", 0.9, s51a2)]
    elif name == "5.2a":
        FILM.append(("5.2a", 0.75, s52a))
    elif name == "5.5":
        FILM.append(("5.5", dur + 0.35, s55))
    elif name == "5.6":
        FILM.append(("5.6", 1.6, s56))
    else:
        FILM.append((name, dur, F5[name]))
for name, dur in rr2.SHOTS:
    if name == "7.4":
        FILM += [("7.4", 1.1, s74a), ("7.4b", 0.45, s54b), ("7.4c", 0.7, s74c)]
    elif name == "6.3":
        FILM += [("6.2a", 0.8, s62a), ("6.2b", 1.5, s62b), ("6.2c", 0.9, s62c), ("6.3", 3.9, s63b)]
    elif name == "6.1":
        FILM.append(("6.1", 2.2, quick(rr2.FN["6.1"], dur / 2.2)))
    elif name == "6.2":
        FILM.append(("6.2", 1.1, quick(rr2.FN["6.2"], dur / 1.1)))
    elif name == "6.4":
        FILM.append(("6.4", 2.7, s64))
    else:
        FILM.append((name, dur, rr2.FN[name]))
FILM += [("8.1", 1.6, s81), ("8.2", 1.3, s82), ("8.2b", 1.0, lambda t: ga.f82b()), ("8.3", 1.5, s83),
         ("8.3b", 1.3, lambda t: _buzzing(lambda: ga.f83b(0.2 if t < 0.6 else 0.5 + 0.5 * ramp(t, 0.6, 0.3)), t)), ("8.4", 1.7, s84), ("8.5", 1.0, s85)]


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
