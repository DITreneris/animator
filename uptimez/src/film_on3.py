"""OFFICE NOIR 3: the whole film as one moving rough (20 Nov), v15 (v1 to v14 pinned). v15 (Tomas, /grill-me): he lies
on the sofa on his side, face to us; smoke, flame and the sponge's water move; the fight has a feint, footwork, a body
hook, a duck and an uppercut; a matchbox that reads, an edge of light at the door and round the alley's shadows. v14: the film is lit as Office
Noir 1 and 2 were (light_on3.auto, on the finished frame, round the tracked figures); the Client's back at her desk is
redrawn (office_on3.BACK2). v13: three things both cold
viewers took for mistakes: the doorway is a doorway (a frame, a FIGHTERS plate, a passage behind, dark or lit); the
smoke is soft and drifts; the hall behind the robot in his view of it has the same people. v12 (an outside review: FAIL,
"blobs and rectangles, not a crowd"): the spectators are people: three tiers behind the far ropes, paler and smaller
with distance, overlapping, each in his own place, with fists, clapping, waving, shouting; at the ringside, backs and
heads nearest us. Nothing else is touched. v11 (Tomas, on animatic v6):
the split frame is cut across, not down (6.2); the hall is alive: the crowd bobs and pumps fists, and throws tall waving
shadows on the back wall; the second approval's sign is held for the robot's line; Sofía's head is tracked for her
bubble. v10 (iteration 2 of 4, the
camera and the cutting): a slow push in on every shot whose drawing stands still; no piece of a shot under half a
second but a punch (the bell 3 x 0.5 s; after CASE CLOSED two pieces, not three; the tick without her face again);
Don comes down the aisle at the camera; shorter toward 80 s. v9 (Tomas, /grill-me: the jumps
in the ring and life first; about 80 s): the Client, Pam, Don, the Referee and the robot move from a pose or a place to
the next over four drawings; the people breathe and blink, and talk while their line is spoken (motion_on3.alive);
eleven still shots are shorter. v8 (Tomas: "Don is redrawn; everyone's
walking has to be put right"): Don has legs, shoes, sleeves in one piece, ears (motion_on3.don); the Client, the woman
under the umbrella and Don walk in steps that hold the ground (2.1, 2.6, 3.1, 3.4, 3.4b, 6.2b, 6.2c). v7 (Tomas): Don wears his hat
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


import motion_on3 as mo
n2.detective = mo.alive(mo.don, "DON", n2.d._pose_tuple, skin=n2.d.SKIN)      # v9: he moves between poses, breathes
n2.detective_back = mo.don_back
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
    x = lerp(250.0, 400.0, t / 1.1)
    return st.frame("S1", [mo.walk(stc.client(x), x, stc.Q, on=t < 1.1)], rain=_rain(t))


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
    if t < 1.0:                                              # v8: she walks, at a walk: steps, not a glide
        sx = 575.0 + 150.0 * (1 - t / 1.0) ** 1.4
    elif t < 1.8:
        sx = 575.0
    else:
        sx = 575.0 - 250.0 * min(1.0, (t - 1.8) / 1.2) ** 1.25
    stopped = 1.0 <= t < 1.8
    wave = 1.2 <= t < 2.1

    def him(k):
        stc.client(450, "b_fist" if wave else "b_pay", (0.9 if sx > 460 else -0.9, 0.0))(k)
        st.folder(k, 452 - (30 if wave else 0), stc.G - 30 - 176 * stc.Q, 0.62 * stc.SC, -0.06)

    def her(k):
        k.c.save(); k.c.translate(0, 6 * math.sin((t - 1.4) * math.pi / 0.3) if 1.4 <= t < 1.7 else 0)       # her nod
        mo.her(stc.sofia(sx, (-0.9, 0.2) if (stopped or sx > 575) else (-1, 0.1)), sx, stc.G - 30, stc.SC * 0.86, on=not stopped)(k)
        k.c.restore()
    return st.frame((470, 1190, 1.12), [her, him], rain=_rain(t))


def s27(t):
    return st.cv_insert(0.0 if t < 0.35 else 1.0)


# ---- 03 the alley -------------------------------------------------------------------------------------------------
def s31(t):
    x = lerp(-30.0, 70.0, t / 1.0)
    return al.frame2("A1", [mo.walk(al.client(x), x, al.Q, on=t < 1.0)], al.gang("aim", ramp(t, 0.5, 0.8) * 0.5))


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
    x = 210.0 + 200.0 * t                            # v8: a hurried walk, in steps; he is still in the frame at the cut
    return al.frame2("A1", [mo.walk(al.client(x, "b_walk", (0.9, 0), cig=x < 300), x, al.Q, a=30.0)], al.gang("down", 0, True), cig=300 if x >= 300 else None)


def s34b(t):
    """Don, bent over the cigarette end. On the wall beside his head the gun's shadow comes down and stops."""
    if t < 0.8:                                              # v8: he walks in on his own two feet
        x = 215.0 - 110.0 * (1 - t / 0.8) ** 1.3
        mo.NOW["walk"] = (x, 1)
        try:
            return al.frame2("A3w", [al.don_caught(x, 0.0)], al.gang("down", 0, True), cig=300)
        finally:
            mo.NOW.clear()
    return al.frame2("A3w", [al.barrel(ramp(t, 0.8, 0.45)), al.don_caught(215, 0.0)], al.gang("down", 0, True), cig=300)


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
    px, pf, ps = lerp(dx0 + dw / 2.0, 470.0, u), lerp(rg.FAR + 6.0, rg.FAR + 40.0, u), rg.SC * lerp(0.62, 1.04, u)   # v10: toward us, growing
    hy = pf - 330 * ps

    def lights(k):                                           # behind everything in the ring: the door, white; fireworks; the two beams
        c = k.c
        _doorway(c, True)
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
            w_ = t * 1.9 if u < 1 else 0.0                    # v8: steps toward us, one foot and then the other
            f0, f1 = mo.stride(w_, 0.0, 30.0), mo.stride(w_ + 0.5, 0.0, 30.0)
            up_ = mo.rise(w_, 7.0) if u < 1 else 0.0
            n2.detective(k, px, pf - up_ * ps, ps, "up", "squint", (-0.5, 0.2), lean=5 * math.sin(w_ * 2 * math.pi) if u < 1 else 0,
                         steps=((-16, f0[1] - up_, 0), (16, f1[1] - up_, 0)))
        finally:
            n2.LOOK[0] = old

    def client(k):
        rr2._seated(k, True, look=(0.9, -0.2), face="tired")

    def robot(k):
        x, y, s_ = rg.HOME["robot_corner"]
        rg.shadow(k, x + 84, y, 40); r.robot(k, x + 84, y, s_, "r_wait", "ask", side=-1)
    return rg.frame((lerp(dx0 + dw / 2.0 - 60, 440.0, u), lerp(rg.F - 300.0, rg.F - 262.0, u), lerp(1.5, 1.34, u)), [lights, fountains, don, client, robot], [], door=True)


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
            n2.detective(k, px, pf, rg.SC, "up", "squint", (-0.6, 0.1), lean=-16 * math.sin(math.pi * u),
                         steps=((-14 - 16 * math.sin(math.pi * u), 34 * math.sin(math.pi * u), -1 if 0 < u < 1 else 0), (14, 0, 0)))
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
    return rr2.shot_64(S64_REST(t - 1.35))                   # v10: no piece under half a second (see _s64_rest)


def _s64_rest():
    """After CASE CLOSED the ring rough has three pieces (wide, the Client's cheer, the Referee). v10: the wide one is
    out (0.43 s, and it said nothing the cheer does not); the cheer 0.65 s, the Referee 0.6 s."""
    a, b_, c_ = 0.8 + 0.43 * (2.2 / 1.35), 0.8 + 0.96 * (2.2 / 1.35), 0.8 + 1.33 * (2.2 / 1.35)
    return lambda u: (a + (b_ - a) * min(u / 0.65, 0.999)) if u < 0.65 else (b_ + (c_ - b_) * min((u - 0.65) / 0.6, 0.999))


S64_REST = _s64_rest()


def s52a(t):
    """The bell: three cuts, a quarter of a second each: from the front, his view of it, its view of him. The view from
    above is out (it read as blobs in four tests)."""
    return F5["5.2a"](min(int(t / 0.5), 2) * 0.25 + 0.01)      # v10: half a second each; a quarter was a flicker


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
    """v11: the cracked screen asks for 1.5 s (the robot now says it: "Human approval still pending."); then her office."""
    return rr2.shot_74(0.2) if t < 1.5 else rr2.shot_74(0.5 + (t - 1.5))


def s62h(t):
    """v11 (Tomas: "the split frame: not cut down the middle but across?"). Two wide halves, one over the other: the robot
    in its corner, proud, oiled; under it Mom at her desk with the hundred. In a tall frame a face needs width, and each
    half was a sliver 267 px wide."""
    def robot(k):
        x, f = 590, rg.F - 40
        rg.shadow(k, x, f, 40)
        r.robot(k, x, f, rg.SC * r.REL, "r_oil", "proud", side=-1, oil=True)
        r.oil_can(k, x - 58, f - 150 + 3 * math.sin(t * 5), 1.5, -0.7)
        c = k.c; c.set_source_rgb(0.05, 0.05, 0.06)
        for i in range(3):
            y = f - 122 + ((t * 70 + i * 16) % 46)
            c.save(); c.translate(x - 84, y); c.scale(3.2, 5); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
    top = rg.frame((560, rg.F - 150, 2.0), [robot], [], near=False, hats=False)
    low = rr2.mom_box(t)
    out = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); oc = cairo.Context(out)
    oc.save(); oc.rectangle(0, 0, 540, 477); oc.clip(); oc.set_source_surface(top, 0, -215); oc.paint(); oc.restore()
    oc.save(); oc.rectangle(0, 483, 540, 477); oc.clip(); oc.set_source_surface(low, 0, 180); oc.paint(); oc.restore()
    oc.set_source_rgb(0, 0, 0); oc.rectangle(0, 477, 540, 6); oc.fill()
    return out


def s74c(t):
    return rr2.shot_74(1.48 + t * (0.3 / 0.55))                # v10: the tick only, held 0.55 s; her face again is out


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
        ("2.5", 1.1, s25), ("2.7", 1.7, s27), ("2.6", 3.0, s26),
        ("3.1", 0.8, quick(s31, 1.6)), ("3.2", 0.6, s32), ("3.2b", 0.9, quick(s32b, 1.1)), ("3.2c", 0.8, quick(s32c, 1.1)), ("3.3", 0.7, quick(s33, 1.25)),
        ("3.3b", 1.1, quick(s33b, 1.45)), ("3.4", 1.0, s34), ("3.4b", 1.5, s34b), ("3.4c", 0.7, s34c), ("3.4d", 0.8, s34d),
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
        FILM += [("7.4", 2.1, s74a), ("7.4b", 0.45, s54b), ("7.4c", 0.7, s74c)]
    elif name == "6.3":
        FILM += [("6.2a", 0.8, s62a), ("6.2b", 1.5, s62b), ("6.2c", 0.9, s62c), ("6.3", 3.9, s63b)]
    elif name == "6.1":
        FILM.append(("6.1", 2.2, quick(rr2.FN["6.1"], dur / 2.2)))
    elif name == "6.2":
        FILM.append(("6.2", 1.3, s62h))
    elif name == "6.4":
        FILM.append(("6.4", 2.7, s64))
    else:
        FILM.append((name, dur, rr2.FN[name]))
FILM += [("8.1", 1.6, s81), ("8.2", 1.3, s82), ("8.2b", 1.0, lambda t: ga.f82b()), ("8.3", 1.5, s83),
         ("8.3b", 1.3, lambda t: _buzzing(lambda: ga.f83b(0.2 if t < 0.6 else 0.5 + 0.5 * ramp(t, 0.6, 0.3)), t)), ("8.4", 1.7, s84), ("8.5", 1.0, s85)]


# v9: the cast is alive: in-betweens when a pose or a place jumps, breath, blinks, lips while a line is spoken
import client_on3 as _b, cast_on3 as _ca, robot_on3 as _r, client_ob as _co
_b.boxer = mo.alive(_b.boxer, "CLIENT", _b.POSES, skin=_co.SKIN, mouth_kw=True)
_ca.pam_corner = mo.alive(_ca.pam_corner, "PAM", _ca.P_POSES, skin=_ca.pn.ps.SKIN, lip=(0.72, 0.10, 0.12))
_ca.referee = mo.alive(_ca.referee, "REFEREE", None, skin=_ca.cb.M_SKIN, tween_pose=False)
_r.robot = mo.alive(_r.robot, "ROBOT", None, breathe=0.0, blinks=False, tween_pose=False)
# v15 (Tomas, /grill-me): on the sofa he lies on his side, his face to us; cigarette smoke moves wherever there is a
# cigarette, the lighter's flame flickers, the end glows; Pam's sponge splashes; the fight has more than one punch:
# a feint and footwork before his first swing (5.2); in the last round a body hook, a duck under the robot's jab, an
# uppercut (7.2). And the three things cold test 43 left: a matchbox that reads, an edge of light on his back at the door,
# an edge round each shadow in the alley.
ga.SIDE[0] = True
al.RIM[0] = al.BOX2[0] = True
dr.RIM[0] = True
al.SMOKE[0] = lambda c, x, y, s_: mo.smoke(c, x, y, s_, seed=0.7, h=140)
al.FLAME[0] = mo.flame
mo.SMOKING.update({"3.3b": 0.55, "3.4": 0.0})
GUARD = (-40, -165, 40, 165)
JAB = (-40, -165, 92, 0)
UWIND = (-40, -165, 24, 70)                                   # the glove low, by his hip
UPPER = (-40, -165, 74, 84)                                   # and up under its chin


def _open52(t):
    """5.2, before he winds up: in his guard, on his toes, one jab at the air that the robot does not answer."""
    if t < 0.10:
        return GUARD
    if t < 0.17:
        return lerp(GUARD, JAB, (t - 0.10) / 0.07)
    if t < 0.24:
        return lerp(JAB, GUARD, (t - 0.17) / 0.07)
    return lerp(GUARD, rr.WALK, (t - 0.24) / 0.11)


def _bob52(t):
    return 7 * abs(math.sin(t * 20)) if t < 0.35 else 0.0


def _pose72(t):
    """7.2: a hook to its body lands (0.3); he ducks; its jab goes over him; he comes up with an uppercut (0.9)."""
    h1, h2 = 0.3, 0.9
    if t < h1:
        return lerp(rr.WIND, rr2.LOW, (t - h1 + 0.1) / 0.1)
    if t < 0.40:
        return rr2.LOW
    if t < 0.50:
        return lerp(rr2.LOW, GUARD, (t - 0.40) / 0.10)
    if t < 0.72:
        return GUARD
    if t < 0.80:
        return lerp(GUARD, UWIND, (t - 0.72) / 0.08)
    return lerp(UWIND, UPPER, (t - 0.80) / 0.10)


def _duck72(t):
    return ramp(t, 0.40, 0.10) * (1 - ramp(t, 0.78, 0.12))


def _draw72(k, t, x, f, draw):
    d = _duck72(t)
    c = k.c
    c.save(); c.translate(x, f); c.rotate(0.24 * d); c.scale(1.0, 1.0 - 0.11 * d); c.translate(-x, -f)
    try:
        return draw()
    finally:
        c.restore()


def _rpose72(t):
    return "r_jab" if 0.50 <= t < 0.74 else "r_wait"


def _splash(k, head, t):
    """6.1: the sponge is squeezed over his head: drops fly out in arcs, water runs down his face, drips fall from his
    chin, small rings where it lands on his shoulders."""
    c = k.c
    sx, sy = head[0] + 4, head[1] - 80
    water, edge = (0.93, 0.96, 1.0), (0.10, 0.10, 0.12)

    def drop(x, y, r_):
        c.new_path(); c.move_to(x, y - r_ * 1.9); c.curve_to(x + r_ * 1.2, y - r_ * 0.2, x + r_, y + r_, x, y + r_); c.curve_to(x - r_, y + r_, x - r_ * 1.2, y - r_ * 0.2, x, y - r_ * 1.9)
        c.set_source_rgb(*water); c.fill_preserve(); c.set_source_rgb(*edge); c.set_line_width(1.2); c.stroke()
    for i in range(12):                                      # the burst
        u = (t - 0.36 - 0.022 * (i % 5)) / 0.5
        if 0 < u < 1:
            an = -math.pi / 2 + (i - 5.5) * 0.30
            drop(sx + math.cos(an) * 96 * u, sy + math.sin(an) * 70 * u + 170 * u * u, 4.2 - 1.6 * u)
    c.set_line_cap(1)
    for j, dx in enumerate((-20, -6, 9, 21)):                # down his face
        u = (t - 0.5 - 0.05 * j) / 0.75
        if 0 < u < 1.5:
            y0, y1 = head[1] - 58, head[1] - 58 + 128 * min(u, 1.0)
            ya = y0 + (y1 - y0) * max(0.0, (u - 1.0) * 2)
            c.set_source_rgba(water[0], water[1], water[2], 0.85); c.set_line_width(2.6)
            c.new_path(); c.move_to(head[0] + dx, ya); c.curve_to(head[0] + dx + 4, (ya * 2 + y1) / 3, head[0] + dx - 4, (ya + y1 * 2) / 3, head[0] + dx + 1, y1); c.stroke()
    for j, dx in enumerate((-12, 4, 16)):                    # off his chin
        ph = (t - 1.0 - 0.21 * j)
        if 0 < ph < 1.1:
            v = (ph * 2.2) % 1.0
            drop(head[0] + dx, head[1] + 66 + 96 * v * v, 3.6)
    c.set_line_cap(0)


def _surgery():
    """The ring roughs' own shots, with these pieces put in (their pinned files draw as before)."""
    src = inspect.getsource(rr2.shot_61)
    a_ = src.index("        if 0.45 < t < 1.3:"); b_ = src.index("c.move_to(head[0] + dx, y0); c.line_to(head[0] + dx, y0 + 12); c.stroke()\n") + len("c.move_to(head[0] + dx, y0); c.line_to(head[0] + dx, y0 + 12); c.stroke()\n")
    ns = dict(rr2.__dict__); ns["_splash"] = _splash
    exec(src[:a_] + "        _splash(k, head, t)\n" + src[b_:], ns); rr2.shot_61 = ns["shot_61"]

    src = inspect.getsource(rr.shot_52)
    for old, new in (("            pose, dx, lean = WALK, 0, 0.0\n", "            pose, dx, lean = _open52(t), 0, 0.0\n"),
                     ("        x, f = 290 + dx, F - 40\n", "        x, f = 290 + dx, F - 40 - _bob52(t)\n")):
        assert old in src, old
        src = src.replace(old, new)
    ns = dict(rr.__dict__); ns.update(_open52=_open52, _bob52=_bob52)
    exec(src, ns); rr.shot_52 = ns["shot_52"]

    src = inspect.getsource(rr2.shot_72)
    a_ = src.index("    def swing(u, pose):"); b_ = src.index("    def robot(k):")
    src = src[:a_] + "    pose = _pose72(t)\n\n" + src[b_:]
    for old, new in (('        r.robot(k, x, f, SC * r.REL, "r_wait", "furious", side=-1, crack=cracked)\n', '        r.robot(k, x, f, SC * r.REL, _rpose72(t), "furious", side=-1, crack=cracked)\n'),
                     ('        b.boxer(k, HITX, F - 40, Q, pose, "hard", (0.9, 0.1), tape=True)\n',
                      '        _draw72(k, t, HITX, F - 40, lambda: b.boxer(k, HITX + 22 * ramp(t, 0.80, 0.10), F - 40, Q, pose, "hard", (0.9, 0.1), tape=True))\n')):
        assert old in src, old
        src = src.replace(old, new)
    ns = dict(rr2.__dict__); ns.update(_pose72=_pose72, _rpose72=_rpose72, _draw72=_draw72, ramp=ramp)
    exec(src, ns); rr2.shot_72 = ns["shot_72"]


_surgery()
_NEW = {"5.2": rr.shot_52, "7.2": rr2.shot_72, "6.1": quick(rr2.shot_61, dict(rr2.SHOTS)["6.1"] / 2.2)}
FILM = [(n, d, _NEW.get(n, f)) for n, d, f in FILM]

# v11: the hall is alive. The far crowd and the ringside hats bob, harder when something lands; fists go up; and on the
# hall's back wall the crowd throws tall shadows that sway and wave (the alley's lesson: a big plain shadow that moves
# is read at once; a row of still hats is wallpaper). HEAT: how worked up the hall is in a shot.
import sofia_on3 as _so3, sofia_ob as _sob
_so3.sofia = mo.alive(_so3.sofia, "SOFIA", None, tween_pose=False, blinks=False, mouth_kw=True)     # so her bubble follows her
_sob.sofia = mo.alive(_sob.sofia, "SOFIA", None, tween_pose=False, blinks=False, mouth_kw=True)
HEAT = {"5.1a": 0.7, "5.1b": 0.7, "5.2a": 0.8, "5.2": 0.8, "5.5": 1.0, "5.6": 1.0, "6.2a": 0.9, "6.2b": 1.0, "6.2c": 0.9, "6.4": 0.7, "7.1": 0.7,
        "7.2": 1.0, "7.2b": 0.8, "7.3": 0.9, "7.5": 1.0}
_hat0 = rg._hat
_DRAW_RING0 = rg.draw_ring


def _heat():
    return HEAT.get(mo.CLOCK["shot"], 0.4)


def _person(c, x, base, h, w, hat, g, T, ph, heat, col, facing=1):
    """v12: one spectator as a person: a head, a neck, a line of shoulders, a body, arms with an elbow and a fist. A
    plain silhouette in one tone. g: fist1, fist2, clap, wave, lean (a hand at the mouth, shouting), still."""
    r = 0.105 * h
    ys = -h + 2 * r + 0.04 * h                               # the shoulders
    sw = w * 0.5
    live = 0.3 if g == "still" else 1.0
    bob = -abs(math.sin(2 * math.pi * (T * (1.5 + 1.0 * ph) + ph))) * (0.015 + 0.06 * heat) * h * live     # v12b: twice the jump; it read as frozen at 8 fps
    lean = (0.17 + 0.04 * math.sin(2 * math.pi * (T * 1.1 + ph))) * facing if g == "lean" else 0.03 * math.sin(2 * math.pi * (T * 0.6 + ph)) * live
    c.save(); c.translate(x, base); c.rotate(lean); c.translate(0, bob)
    c.set_source_rgb(*col)
    c.new_path(); c.move_to(-0.40 * w, 0); c.line_to(-sw, ys + 0.16 * h); c.curve_to(-sw, ys + 0.02 * h, -sw + 0.10 * w, ys, -0.14 * w, ys)
    c.line_to(-0.10 * w, ys - 0.05 * h); c.line_to(0.10 * w, ys - 0.05 * h); c.line_to(0.14 * w, ys)
    c.curve_to(sw - 0.10 * w, ys, sw, ys + 0.02 * h, sw, ys + 0.16 * h); c.line_to(0.40 * w, 0); c.close_path(); c.fill()
    hy = -h + r
    c.save(); c.translate(0, hy); c.scale(r * 0.9, r); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
    if hat:                                                  # a fedora: a brim and a dented crown, not a box
        c.save(); c.translate(0, hy - 0.55 * r); c.scale(1.55 * r, 0.28 * r); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
        c.new_path(); c.move_to(-0.86 * r, hy - 0.55 * r); c.curve_to(-0.9 * r, hy - 1.7 * r, -0.2 * r, hy - 1.75 * r, 0, hy - 1.45 * r)
        c.curve_to(0.2 * r, hy - 1.75 * r, 0.9 * r, hy - 1.7 * r, 0.86 * r, hy - 0.55 * r); c.close_path(); c.fill()
    c.set_line_width(0.15 * w); c.set_line_cap(1); c.set_line_join(1)

    def arm(sd, ex, ey, fx, fy):
        c.new_path(); c.move_to(sd * (sw - 0.08 * w), ys + 0.07 * h); c.line_to(ex, ey); c.line_to(fx, fy); c.stroke()
        c.arc(fx, fy, 0.105 * w, 0, 2 * math.pi); c.fill()
    pump = abs(math.sin(2 * math.pi * (T * (1.9 + heat) + ph)))
    if g in ("fist1", "fist2"):
        for sd in ((1, -1) if g == "fist2" else ((1,) if ph < 0.5 else (-1,))):
            p_ = pump if sd > 0 else abs(math.sin(2 * math.pi * (T * (1.6 + heat) + ph + 0.25)))
            arm(sd, sd * (sw + 0.10 * w), ys + 0.02 * h - 0.12 * h * p_, sd * (sw + 0.02 * w), ys - 0.18 * h - 0.28 * h * p_)
    elif g == "clap":
        gap = 0.03 * w + 0.20 * w * (0.5 + 0.5 * math.sin(2 * math.pi * (T * 3.2 + ph)))
        for sd in (-1, 1):
            arm(sd, sd * (sw + 0.06 * w), ys - 0.10 * h, sd * gap, ys - 0.36 * h)
    elif g == "wave":
        sd = 1 if ph < 0.5 else -1
        arm(sd, sd * (sw + 0.08 * w), ys - 0.12 * h, sd * 0.30 * w + 0.26 * w * math.sin(2 * math.pi * (T * 1.8 + ph)), ys - 0.44 * h)
    elif g == "lean":
        arm(facing, facing * (sw + 0.02 * w), ys + 0.03 * h, facing * 0.22 * w, hy + 0.55 * r)
    c.restore()


def _gesture(i, heat):
    u, v = (i * 0.618) % 1.0, (i * 0.377) % 1.0
    g = "fist1" if u < 0.25 else "fist2" if u < 0.40 else "clap" if u < 0.53 else "wave" if u < 0.65 else "lean" if u < 0.85 else "still"
    return "still" if (g != "still" and v > heat * 1.35) else g


ROWS = (                                                     # (base above the far edge, height, width, step, tone): three tiers behind the far ropes
    (-128, 128, 46, 43, 0.33),
    (-74, 150, 56, 51, 0.23),
    (-14, 176, 68, 60, 0.14),
)


def _wall_crowd(c):
    """v12: the crowd behind the far ropes: three tiers of people, the farther the paler and smaller, overlapping, each
    in his own place in every shot and doing his own thing (fists, clapping, waving, shouting, or standing)."""
    if mo.CLOCK["shot"] is None:
        return
    T, h = mo.CLOCK["T"], _heat()
    for ri, (dy, H, W_, step, tone) in enumerate(ROWS):
        x, i = -420.0 + ri * 17, 0
        while x < rg.WW + 440:
            k_ = ri * 100 + i
            ph = (k_ * 0.2718) % 1.0
            hh = H * (0.90 + 0.22 * ((k_ * 0.531) % 1.0)); ww = W_ * (0.86 + 0.30 * ((k_ * 0.713) % 1.0))
            t_ = tone + 0.035 * ((k_ * 0.419) % 1.0 - 0.5)
            _person(c, x, rg.FAR + dy + 30, hh, ww, k_ % 3 != 1, _gesture(k_, h), T, ph, h, (t_, t_, t_ + 0.02), 1 if x < rg.LAMP[0] else -1)
            x += step * (0.82 + 0.4 * ((k_ * 0.291) % 1.0)); i += 1


def _hat_live(c, x, top, rr_, hat=True):
    """The set's own hats. Far ones (small) are out: the tiers of people stand there now. The ringside ones (big, nearest
    us) become people seen from behind, black, their heads and shoulders over the frame's bottom edge, some with a fist up."""
    if mo.CLOCK["shot"] is None:
        return _hat0(c, x, top, rr_, hat)
    if rr_ < 20:
        return
    T, h = mo.CLOCK["T"], _heat()
    i = int(x) // 7
    for dx_, dyy, sc_, tone in ((62, 26, 0.86, 0.075), (0, 0, 1.0, 0.03)):
        k_ = 900 + i * 2 + (dx_ > 0)
        H = 250 * sc_ * (0.9 + 0.2 * ((k_ * 0.531) % 1.0))
        _person(c, x + dx_, top - rr_ + H + dyy, H, 150 * sc_, k_ % 3 != 2, _gesture(k_, h), T, (k_ * 0.2718) % 1.0, h, (tone, tone, tone + 0.01), 1 if x < rg.LAMP[0] else -1)
    c.set_source_rgb(0.03, 0.03, 0.04)


rg._hat = _hat_live


def _doorway(c, lit):
    """v13: the way out reads as a doorway (it was "a slab, a speaker" dark and "an empty sign" lit): a frame, a plate over
    it (FIGHTERS), and a passage behind: its floor running back to a small far light. Lit: the passage white, the floor
    still drawn."""
    dx, dy, dw, dh = rg.DOOR
    c.set_source_rgb(0.04, 0.04, 0.05); c.rectangle(dx - 7, dy - 7, dw + 14, dh + 7); c.fill()                      # the frame
    g = cairo.LinearGradient(dx, 0, dx + dw, 0)
    if lit:
        g.add_color_stop_rgb(0, 0.80, 0.80, 0.78); g.add_color_stop_rgb(0.5, 0.99, 0.99, 0.95); g.add_color_stop_rgb(1, 0.80, 0.80, 0.78)
    else:
        g.add_color_stop_rgb(0, 0.10, 0.10, 0.12); g.add_color_stop_rgb(0.5, 0.20, 0.20, 0.23); g.add_color_stop_rgb(1, 0.10, 0.10, 0.12)
    c.set_source(g); c.rectangle(dx, dy, dw, dh); c.fill()
    mx = dx + dw / 2.0
    c.new_path(); c.move_to(dx, dy + dh); c.line_to(mx - 9, dy + dh * 0.52); c.line_to(mx + 9, dy + dh * 0.52); c.line_to(dx + dw, dy + dh); c.close_path()   # the floor, going back
    c.set_source_rgb(*((0.70, 0.70, 0.68) if lit else (0.30, 0.30, 0.33))); c.fill()
    c.set_source_rgb(*((0.55, 0.55, 0.54) if lit else (0.06, 0.06, 0.07))); c.set_line_width(1.6)
    for q in (0.25, 0.5, 0.75):                                                                                    # its boards
        c.move_to(dx + dw * q, dy + dh); c.line_to(mx + (q - 0.5) * 18, dy + dh * 0.52); c.stroke()
    if not lit:
        c.set_source_rgb(0.62, 0.62, 0.60); c.rectangle(mx - 8, dy + dh * 0.30, 16, dh * 0.22); c.fill()             # the far end, lit
    c.set_source_rgb(0.86, 0.86, 0.82); c.rectangle(dx - 10, dy - 30, dw + 20, 20); c.fill()                         # the plate
    c.set_source_rgb(0.05, 0.05, 0.06); c.set_line_width(2); c.rectangle(dx - 10, dy - 30, dw + 20, 20); c.stroke()
    c.select_font_face("Inter", 0, 1); c.set_font_size(11.5)
    e = c.text_extents("FIGHTERS"); c.move_to(mx - e.x_advance / 2, dy - 15.5); c.show_text("FIGHTERS")


def _smoke(c):
    """v13: the hall's smoke, soft: three faint layers each, wide to narrow, drifting; one hard pale stroke read as a smear."""
    T = mo.CLOCK["T"] if mo.CLOCK["shot"] is not None else 0.0
    c.set_line_cap(1)
    for j, (sx_, sy_) in enumerate(((250, 960), (440, 860), (350, 1120))):
        sx_ += 26 * math.sin(2 * math.pi * (T * 0.05 + j * 0.31))
        for wd, al in ((54, 0.022), (36, 0.03), (20, 0.035)):
            c.set_source_rgba(1, 1, 1, al); c.set_line_width(wd)
            c.move_to(sx_ - 90, sy_); c.curve_to(sx_ - 20, sy_ - 40, sx_ + 30, sy_ + 30, sx_ + 110, sy_ - 14); c.stroke()


def _ring_with_wall():
    src = inspect.getsource(_DRAW_RING0)
    old = "    dx, dy, dw, dh = DOOR                                                                  # the way out: a lit doorway\n"
    assert old in src
    d0 = src.index("    c.set_source_rgb(*((0.50, 0.50, 0.50) if door else (0.15, 0.15, 0.17)))"); d1 = src.index("    c.set_source_rgb(0.05, 0.05, 0.06)                                                     # the far crowd")
    src = src[:d0] + "    _doorway(c, door)\n" + src[d1:]
    m0 = src.index("    c.set_source_rgba(1, 1, 1, 0.10); c.set_line_width(16); c.set_line_cap(1)              # smoke"); m1 = src.index("    c.set_line_cap(0)\n", m0)
    src = src[:m0] + "    _smoke(c)\n" + src[m1:]
    ns = dict(rg.__dict__); ns.update(_wall_crowd=_wall_crowd, _doorway=_doorway, _smoke=_smoke)
    exec(src.replace(old, "    _wall_crowd(c)\n" + old).replace("_hat(c, x,", "_HAT(c, x,"), ns)
    ns["_HAT"] = _hat_live
    return ns["draw_ring"]


def _hall_people(c):
    """v13: the hall behind the robot as he sees it: the same three tiers of people (it was a black band with nine bumps)."""
    g = cairo.RadialGradient(270, 380, 40, 270, 380, 760)
    g.add_color_stop_rgba(0, 0.78, 0.78, 0.80, 1); g.add_color_stop_rgba(1, 0.12, 0.12, 0.14, 1); c.set_source(g); c.paint()
    T, h = (mo.CLOCK["T"], _heat()) if mo.CLOCK["shot"] is not None else (0.0, 0.6)
    for ri, (base, H, W_, step, tone) in enumerate(((668, 150, 54, 50, 0.40), (716, 178, 66, 59, 0.29), (774, 206, 80, 70, 0.17))):
        x, i = -30.0 + ri * 19, 0
        while x < 580:
            k_ = 300 + ri * 100 + i; ph = (k_ * 0.2718) % 1.0
            t_ = tone + 0.035 * ((k_ * 0.419) % 1.0 - 0.5)
            _person(c, x, base, H * (0.9 + 0.22 * ((k_ * 0.531) % 1.0)), W_ * (0.86 + 0.3 * ((k_ * 0.713) % 1.0)), k_ % 3 != 1, _gesture(k_, h), T, ph, h,
                    (t_, t_, t_ + 0.02), 1 if x < 270 else -1)
            x += step * (0.82 + 0.4 * ((k_ * 0.291) % 1.0)); i += 1
    c.set_source_rgb(0.05, 0.05, 0.06); c.rectangle(0, 700, 540, 80); c.fill()                                      # the barrier
    c.set_source_rgb(0.50, 0.50, 0.54)
    for y in (640, 690, 740):
        c.rectangle(0, y, 540, 5); c.fill()
    c.set_source_rgb(0.64, 0.64, 0.66); c.rectangle(0, 780, 540, 180); c.fill()


rr._hall = _hall_people
rg.draw_ring = _ring_with_wall()

TRIM = {"2.5": 0.9, "2.7": 1.3, "4.1": 1.0, "4.2": 1.3, "4.4t": 1.0, "4.4b": 0.8, "4.4c": 0.7, "6.3": 3.0, "8.1": 1.2, "8.2b": 0.7, "8.4": 1.3,
        "2.4": 1.5, "4.4": 2.1, "5.1a": 1.7, "5.2": 1.6, "5.3": 1.1, "7.1": 1.3, "7.2b": 1.3, "7.3": 2.0}      # v10: toward 80 s
FILM = [(n, TRIM.get(n, d), quick(f, d / TRIM[n]) if n in TRIM else f) for n, d, f in FILM]
LEN = {"5.2a": 1.5, "6.4": 2.6, "7.4c": 0.55}               # v10: pieces re-cut inside the shot's own function
FILM = [(n, LEN.get(n, d), f) for n, d, f in FILM]
# v10: the camera. A shot whose drawing stands still is pushed in on, slowly, from its first frame to its last (a move
# of the finished frame about a point, 3% a second, 8% at most); the clock runs on through a held drawing, so it never
# stops. Not on the first shot or the last (frame 0 is the last frame), nor on shots that have their own move.
DRIFT = {"2.0": (270, 400), "2.5": (270, 380), "2.7": (270, 420), "3.3": (300, 430), "3.3b": (270, 430), "3.4c": (270, 400), "4.1": (270, 420),
         "4.2": (270, 400), "4.3": (270, 430), "4.4a": (270, 520), "4.4b": (270, 480), "4.4c": (270, 400), "5.2a": (270, 430), "5.4": (270, 400),
         "5.4b": (270, 520), "6.3": (270, 430), "7.4": (270, 400), "7.4b": (270, 520), "7.4c": (270, 430), "8.1": (270, 430), "8.2": (270, 430),
         "8.2b": (270, 380), "8.3": (270, 480), "8.4": (270, 430)}


def _drift(fn, start, focus, rate=0.03, most=0.08):
    def f(t):
        s_ = fn(t)
        z = 1.0 + min(most, rate * max(0.0, mo.CLOCK["T"] - start))
        mo.CLOCK["zoom"] = (focus, z)
        out = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(out)
        c.translate(focus[0], focus[1]); c.scale(z, z); c.translate(-focus[0], -focus[1])
        c.set_source_surface(s_, 0, 0); c.get_source().set_filter(cairo.FILTER_BILINEAR); c.paint()
        return out
    return f


# v14: the film is lit (light_on3.auto): a pool round the tracked figures, faces lifted from above, a vignette, grain.
# Not the waking scene (in colour, plain: the dream is the dark one), not the split frame, not Don's outline in the door.
# The first shot and the last have no grain and the last fades the light in, so the last frame is still the first.
import light_on3 as lt
UNLIT = ("8.1", "8.2", "8.2b", "8.3", "8.3b", "8.4", "6.2", "6.2a")
CLOSE = ("1.1", "3.4c", "4.2", "4.4c", "5.1a2", "7.5", "8.5")
of.BACK2[0] = True                                           # his back at her desk, redrawn
mo.FROZEN.update(("1.1", "8.5"))                             # the loop's two ends: no breath, no blink (they had made the last frame differ from the first)


def _lit(fn, name):
    if name in UNLIT:
        return fn

    def f(t):
        s_ = fn(t)
        heads = [v for who, v in (mo.CLOCK.get("heads") or {}).items() if who != "ROBOT"]      # the robot's black head is not a face to lift
        k_ = ramp(t, 0.55, 0.4) if name == "8.5" else 1.0
        seed = None if name in ("1.1", "8.5") else int(round(mo.CLOCK["T"] * 15))            # grain on twos
        return lt.auto(s_, heads, k_, seed, name in CLOSE, glow=name not in ("1.1", "7.5", "8.5"), pool=name not in ("5.6",))
    return f


_T0, _F = 0.0, []
for _n, _d, _f in FILM:
    _f = _lit(mo.timed(_n, _f, _T0), _n)
    _F.append((_n, _d, _drift(_f, _T0, DRIFT[_n]) if _n in DRIFT else _f)); _T0 += _d
FILM = _F


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
