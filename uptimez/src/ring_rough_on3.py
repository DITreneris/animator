"""OFFICE NOIR 3: a moving rough of beat 05, whole (5.1a to 5.6), mute, for the cold test (19 Nov). v2; ring_rough_on3_v1.py
is v1 (5.1a to 5.2). v8 (ring_rough_on3_v7.py is v7; Tomas, /grill-me): first-person views and four cuts round the ring. 5.2a: at the bell,
four fast cuts (front, his view of it, its view of him, from above). 5.3 is the robot's view: his glove stopped at the
lens, the words over his face. 5.5: the jab through his eyes: the grey glove fills the frame, black; then he is down.
v7 (ring_rough_on3_v6.py is v6): the watch gag is out of 5.6; sheets(fast=...) names the shots shown at 8 a second.
v6 (ring_rough_on3_v5.py is v5): the screen is blank for three frames between the face and the words (it showed a smile).
v5 (ring_rough_on3_v4.py is v4): in 5.4 Mom sits behind her desk, in a high-backed chair (Tomas).
v4 (ring_rough_on3_v3.py is v3), four changes and no more: the gap at the stopped glove is open again (5.2, 5.5); the
stretched sleeve is held longer, with a closer cut on it (5.1c); Mom's own arm comes down on the button (5.4); the
robot's jab is three drawings (5.5).
v3 (ring_rough_on3_v2.py is v2): 5.4 is lit: a pale wall behind Mom's black coat (Tomas: too dark).
v2: a harder swing with a second shove; the robe wiped back on, not cut; and 5.3 (the screen asks),
5.4 (Mom, a stand-in office: her set is not built), 5.5 (the tick, the jab, he goes over), 5.6 (from above: the count).
v1:
Four cold tests of stills left two things a still cannot show: which way the robe is going, and a punch that stops.
This is a rough: poses change, figures slide, nobody's legs walk. 540x960, 30 fps, one encoded file per shot, joined
with the concat demuxer. In 5.2 the Referee is behind the robot again (script v15).
Usage: python3 ring_rough_on3.py [out.mp4] [sheets_dir]   (default ../office-noir-3/on3_beat05_rough_v8.mp4)"""
import os
import sys
import math
import subprocess
import cairo
import ring_on3 as rg
import ring_casts_on3 as rc
import cast_on3 as ca
import client_on3 as b
import cand_bc as cb
import robot_on3 as r
import sofia_on3 as so3
import mom_on3 as q
import client_sheet_on3 as csh
from kit import Ctx, rect, ellipse
from kit import cut

F, SC, Q = rg.F, rg.SC, rc.Q
FPS = 30
SHOTS = (("5.1a", 2.0), ("5.1b", 1.0), ("5.1c", 3.2), ("5.2a", 1.0), ("5.2", 1.9), ("5.3", 1.3), ("5.4", 2.0), ("5.5", 1.8), ("5.6", 2.0))


def lerp(a, b_, t):
    t = max(0.0, min(1.0, t))
    t = t * t * (3 - 2 * t)
    if isinstance(a, tuple):
        return tuple(x + (y - x) * t for x, y in zip(a, b_))
    return a + (b_ - a) * t


WALK, UP, SWING = b.POSES["b_walk"], (-9, 6, 150, 22), b.POSES["b_swing"]
WIND = (-9, 6, 118, 150)                                   # the elbow up and back, the glove by his ear


def shot_51a(t):
    """He is in his corner; his glove comes up toward the plan and his head goes back; Sofia walks the card across."""
    up = (t - 0.3) / 0.6

    def client(k):
        rg.shadow(k, 130, F - 30, 44)
        with rc.head_back(lerp(0.0, -0.24, up)):
            b.boxer(k, 130, F - 30, Q, lerp(WALK, UP, up), "hard", (0.7, lerp(0.0, -0.9, up)))

    def pam(k):
        rg.shadow(k, 228, F - 14, 34); ca.pam_corner(k, 228, F - 14, SC, "p_stand", "neutral", (-0.9, 0.0))

    def ref(k):
        rg.shadow(k, 336, F - 96, 36); ca.referee(k, 336, F - 96, SC * ca.REL_REF, "ref_stand", look=(-0.8, 0), waistcoat=True)

    def robot(k):
        rg.shadow(k, 408, F - 42, 40); r.robot(k, 408, F - 42, SC * r.REL, "r_wait", "furious", side=-1)

    def sofia(k):
        x = 720 - 150 * t
        so3.sofia(k, x, F + 108 - 3 * abs(math.sin(t * math.pi * 3.2)), 0.92, "r_card", "spotted", (-1, -0.2), card_="ROUND 1")
    return rg.frame("R1", [ref, robot, client, pam], [sofia], money=True)


def shot_51b(t):
    """His view: the glove comes up under the plan and cannot reach; the plan sways."""
    rise = lerp(300.0, 0.0, t / 0.45) + (3 * math.sin(t * 40) if t > 0.5 else 0)       # it strains, short of the paper
    return rg.plan_pov(glove=True, swing=0.02 * math.sin(t * 5), rise=rise)


def shot_51c(t):
    """The robe is on; Pam takes the collar and pulls it down off his shoulders; one sleeve comes with her, stretches,
    and stops at the glove; she pulls twice more; she lets go; she shoves it back up over his shoulders, crooked."""
    cx, cf = rc.CL
    off = 0.35 <= t < 2.35
    if off:
        pull = lerp(0.0, 1.0, (t - 0.35) / 0.25)
        tug = 7 * math.sin((t - 0.6) * math.pi * 3.2) if 0.6 < t < 2.1 else 0
        slack = lerp(0.0, 1.0, (t - 2.1) / 0.25)
        pose = (-9, 6, lerp(20.0, 56.0, pull) + tug * 0.5, 2)
        cl = lambda k: b.boxer(k, cx, cf, Q, pose, "hard", (0.7, -0.9), strip=True)
        gx, gy = rc.probe(cl)["hands"][1]
        ln = lerp(26.0, 86.0, pull) + tug - 30 * slack
        ex, ey = gx + ln, gy + 12 + 26 * slack

        def client(k):
            rg.shadow(k, cx, cf, 44)
            with rc.head_back():
                cl(k)
            c = k.c
            cut(k, [(gx + 4, gy - 22), (ex, ey - 12), (ex + 4, ey + 12), (gx + 8, gy + 24)], b.KEY, shadow=False, lw=2.2)
            c.set_source_rgb(*b.SHADE); c.set_line_width(2.0); c.set_line_cap(1)
            for q in (0.25, 0.5, 0.75):
                x_ = gx + 8 + (ex - gx - 6) * q
                c.move_to(x_, gy - 16 + 12 * q); c.line_to(x_ + 5, gy + 18 + 2 * q); c.stroke()
            cut(k, [(ex - 3, ey - 14), (ex + 10, ey - 13), (ex + 12, ey + 14), (ex - 1, ey + 15)], b.IVORY, shadow=False, lw=1.8)

        def pam(k):
            px_, pf = rc.PAM[0] - 60 + 60 * pull, rc.PAM[1]
            lean = (lerp(-4.0, 8.0, pull) + tug * 0.4 - 6 * slack, 12)
            rg.shadow(k, px_, pf, 34)
            ca.pam_corner(k, px_, pf, SC, ca.reach(px_, pf, SC, (ex + 4, ey - 6), (ex + 12, ey + 8), stance=lean), "neutral",
                          (-0.9, 0.7), stance=lean)
        cam = (gx + 52, gy - 44, 2.3) if 0.85 <= t < 1.95 else "R3"        # v4: a closer cut on the sleeve and her hands
        return rg.frame(cam, [client, pam], [], near=False, hats=False)
    back = lerp(0.0, 1.0, (t - 2.35) / 0.3) if t >= 2.35 else 0.0
    grab = lerp(0.0, 1.0, t / 0.3) if t < 0.35 else 1.0

    def client(k):
        rg.shadow(k, cx, cf, 44)
        up = (t - 2.35) / 0.22 if t >= 2.35 else 1.0             # she drags it back up over him, from the belt
        c = k.c
        if up < 1.0:
            with rc.head_back():
                b.boxer(k, cx, cf, Q, "b_walk", "hard", (0.7, -0.9), strip=True)
            c.save(); c.rectangle(cx - 200, cf + (b.HIP - (b.HIP - b.HY + 40) * up) * Q, 400, 2000); c.clip()
        with rc.head_back():
            b.boxer(k, cx, cf - (5 * math.sin(back * math.pi) if t >= 2.35 else 0), Q, "b_walk", "hard", (0.7, -0.9))
        if up < 1.0:
            c.restore()
        if t >= 2.35:                                       # the collar, shoved up on her side: it sits crooked
            c = k.c
            sx, sy = cx + 34 * Q, cf + (b.BT - 6) * Q
            cut(k, [(sx, sy + 26 * Q), (sx + 16 * Q, sy - 40 * Q * back), (sx + 62 * Q, sy - 22 * Q * back), (sx + 74 * Q, sy + 34 * Q)],
                b.KEY, shadow=False, lw=2.2)
            c.set_source_rgb(*b.SHADE); c.set_line_width(2.0); c.set_line_cap(1)
            c.move_to(sx + 22 * Q, sy - 24 * Q * back); c.line_to(sx + 40 * Q, sy + 22 * Q); c.stroke()

    def pam(k):
        tx, ty = cx + 62 * Q, cf + (b.BT - 14) * Q
        if t >= 2.35:
            away = lerp(0.0, 1.0, (t - 2.75) / 0.3)         # she steps back, hands off
            px_, pf = cx + 118 + 40 * away, F - 14
            rg.shadow(k, px_, pf, 34)
            if away > 0.5:
                ca.pam_corner(k, px_, pf, SC, "p_stand", "neutral", (-0.9, 0.2))
            else:
                ca.pam_corner(k, px_, pf, SC, ca.reach(px_, pf, SC, (tx, ty - 10 * back), (tx + 22, ty + 26), stance="work"), "neutral",
                              (-0.9, 0.2), stance="work")
        else:
            px_, pf = cx + 170 - 52 * grab, F - 14
            rg.shadow(k, px_, pf, 34)
            ca.pam_corner(k, px_, pf, SC, ca.reach(px_, pf, SC, (tx + 40 - 40 * grab, ty + 30 - 30 * grab), (tx + 60 - 38 * grab, ty + 60 - 34 * grab),
                                                   stance="work"), "neutral", (-0.9, 0.2), stance="work")
    return rg.frame("R3", [client, pam], [], near=False, hats=False)


def _stop_x(gap=62):
    """Where he stands so that his glove, at full reach, ends `gap` short of the robot's head (the robot at 466)."""
    reach = rc.probe(lambda k: b.boxer(k, 0, 0, Q, SWING, "hard"))["hands"][1][0] + (b.GLOVE + 4) * Q + 8
    return 466 - r.RX * SC * r.REL - gap - reach


STOP = _stop_x()
BELL, STAND = cb.POSES_MACHO["ref_bell"], cb.POSES_MACHO["ref_stand"]


def shot_52(t):
    """The Referee, behind the robot, drops his arm; Pam clicks the stopwatch; he winds up and swings with everything;
    the glove stops a hand short; the robot has not moved; he stays there, shaking with the effort."""
    def ref(k):
        rg.shadow(k, 546, F - 96, 36)
        pose = "ref_bell" if t < 0.2 else lerp(BELL, STAND, (t - 0.2) / 0.15) if t < 0.35 else "ref_stand"
        ca.referee(k, 546, F - 96, SC * ca.REL_REF, pose, look=(-0.8, 0.2), waistcoat=True)

    def robot(k):
        rg.shadow(k, 466, F - 46, 40); r.robot(k, 466, F - 46, SC * r.REL, "r_wait", "furious", side=-1)

    def client(k):
        if t < 0.35:
            pose, dx, lean = WALK, 0, 0.0
        elif t < 0.72:                                      # he winds up: back on his heels, the glove behind his ear
            u = (t - 0.35) / 0.3
            pose, dx, lean = lerp(WALK, WIND, u), -20 * lerp(0.0, 1.0, u), -0.16 * lerp(0.0, 1.0, u)
        elif t < 0.80:                                      # everything he has, in two drawings
            u = (t - 0.72) / 0.08
            pose, dx, lean = lerp(WIND, SWING, u), -20 + (STOP - 270) * lerp(0.0, 1.0, u), -0.16 + 0.22 * lerp(0.0, 1.0, u)
        else:                                               # it stops. He leans on it; he shoves again; it does not go
            shove = 7 * math.sin((t - 1.25) / 0.2 * math.pi) if 1.25 < t < 1.45 else 0
            pose, dx, lean = SWING, STOP - 290 + shove + 1.5 * math.sin(t * 70), 0.06 + shove * 0.004
        x, f = 290 + dx, F - 40
        rg.shadow(k, x, f, 44)
        c = k.c
        c.save(); c.translate(x, f); c.rotate(lean); c.translate(-x, -f)
        b.boxer(k, x, f, Q, pose, "hard", (0.9, 0))
        c.restore()

    def pam(k):
        x, f = 190, F - 6
        if 0.2 <= t < 0.5:
            ca.pam_corner(k, x, f, SC, ca.reach(x, f, SC, (240, F - 204), (210, F - 84), stance="stand"), "neutral", (0.9, 0.1),
                          watch="hand", stance="stand")
        else:
            ca.pam_corner(k, x, f, SC, "p_stand", "neutral", (0.9, 0.1))
    return rg.frame((412, 1100, 1.25), [ref, robot, pam, client], [], near=False, hats=False)    # R2, a little wider: his arm


def _insert_screen(state, crack=False):
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(s); k = Ctx(c, 0)
    c.set_source_rgb(0.04, 0.04, 0.05); c.paint()
    g = cairo.RadialGradient(270, 470, 60, 270, 470, 520)
    g.add_color_stop_rgba(0, 0.30, 0.34, 0.38, 1); g.add_color_stop_rgba(1, 0.04, 0.04, 0.05, 1); c.set_source(g); c.paint()
    c.save(); c.translate(270, 470); c.scale(5.0, 5.0)
    ellipse(k, 0, 0, r.RX + 7, r.RY + 7, (0.30, 0.31, 0.34), 3, shadow=False, lw=2)       # the head's rim
    if state == "off":                                     # v6: blank between the face and the words (it drew a smile)
        ellipse(k, 0, 0, r.RX, r.RY, r.w.SCREEN, 0, shadow=False, lw=2)
    else:
        r.screen(k, state, crack=crack)
    c.restore()
    csh.noir(s)
    return s


def _hall(c):
    g = cairo.RadialGradient(270, 380, 40, 270, 380, 760)
    g.add_color_stop_rgba(0, 0.78, 0.78, 0.80, 1); g.add_color_stop_rgba(1, 0.12, 0.12, 0.14, 1); c.set_source(g); c.paint()
    c.set_source_rgb(0.05, 0.05, 0.06); c.rectangle(0, 700, 540, 80); c.fill()               # the far crowd
    for i in range(9):
        c.arc(20 + i * 66, 700 - (i % 3) * 5, 16, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(0.50, 0.50, 0.54)
    for y in (640, 690, 740):
        c.rectangle(0, y, 540, 5); c.fill()
    c.set_source_rgb(0.64, 0.64, 0.66); c.rectangle(0, 780, 540, 180); c.fill()


def _hud(c, words=0, crack=False):
    """Its screen from the inside: the rim, scan lines, a frame round the target, and the rows of the ask."""
    c.set_source_rgba(0.75, 0.90, 1.0, 0.07)
    for y in range(0, 960, 8):
        c.rectangle(0, y, 540, 2); c.fill()
    c.set_source_rgb(0.02, 0.02, 0.03); c.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
    c.rectangle(0, 0, 540, 960); c.save(); c.translate(270, 480); c.scale(262, 440); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
    c.set_fill_rule(cairo.FILL_RULE_WINDING)
    c.set_source_rgb(*r.INKW); c.set_line_width(4)
    for sx, sy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):     # the corners of a target frame
        x, y = 250 + sx * 130, 560 + sy * 130
        c.move_to(x, y - sy * 36); c.line_to(x, y); c.line_to(x - sx * 36, y); c.stroke()
    if words:
        c.set_source_rgba(0.02, 0.02, 0.03, 0.72); c.rectangle(40, 200, 460, 60 * words + 26); c.fill()
        c.select_font_face("Inter", 0, 1); c.set_font_size(58); c.set_source_rgb(*r.INKW)
        for i, w_ in enumerate(("HUMAN", "APPROVAL", "REQUIRED")[:words]):
            c.move_to(270 - c.text_extents(w_).x_advance / 2, 260 + i * 60); c.show_text(w_)


def pov_robot(t=0.0, words=0, glove=True, far=False):
    """What the robot sees: him, square on, and (glove=True) his red glove stopped a hand from the lens."""
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(s); k = Ctx(c, 0)
    _hall(c)
    sc = (1.5 if far else 2.5) * b.REL
    x, f = 250, 930 + (0 if far else 250)
    b.boxer(k, x, f + 2 * math.sin(t * 60), sc, "b_walk", "hard", (0, 0.1))
    if glove:
        gx, gy = 404 + 2 * math.sin(t * 60), 812
        c.save(); c.translate(gx, gy); c.scale(3.6, 3.6); c.translate(-gx, -gy)
        cut(k, [(gx - 60, gy + 20), (gx - 20, gy + 26), (gx - 30, gy + 80), (gx - 80, gy + 70)], b.KEY, shadow=False, lw=1.2)
        b._glove(k, gx, gy, 0.5, -0.87, 1, 91)
        c.restore()
    csh.noir(s)
    _hud(c, words)
    return s


def pov_client(t=0.0, state="furious", jab=0.0):
    """What he sees: the robot, square on, small under the lamp. jab 0..1: its grey glove comes at the lens."""
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(s); k = Ctx(c, 0)
    _hall(c)
    r.robot(k, 270, 900, 2.3 * r.REL, "r_guard" if jab == 0 and state == "tick" else "r_wait", state, side=-1)
    if jab > 0:
        b.robot_glove(k, 270, 560, 1.2 + 9.0 * jab * jab, ang=-math.pi / 2)
    csh.noir(s)
    return s


def top_view():
    """The ring from straight above, at the bell: the two of them, the Referee, Pam at the ropes, the plan's bar."""
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(s); k = Ctx(c, 0)
    c.set_source_rgb(0.10, 0.10, 0.12); c.paint()
    rect(k, 50, 230, 440, 500, (0.66, 0.66, 0.68), 3, shadow=False, lw=3)
    g = cairo.RadialGradient(270, 480, 20, 270, 480, 300)
    g.add_color_stop_rgba(0, 1, 1, 1, 0.5); g.add_color_stop_rgba(1, 1, 1, 1, 0); c.set_source(g); c.rectangle(50, 230, 440, 500); c.fill()
    c.set_source_rgb(0.90, 0.90, 0.92); c.set_line_width(5)
    for d in (0, 14, 28):
        c.rectangle(50 - d, 230 - d, 440 + 2 * d, 500 + 2 * d); c.stroke()
    for px_, py_ in ((22, 202), (518, 202), (22, 758), (518, 758)):
        ellipse(k, px_, py_, 16, 16, (0.34, 0.34, 0.37), 5, shadow=False, lw=2.4)
    ellipse(k, 190, 500, 50, 40, b.KEY, 6, shadow=False, lw=3); ellipse(k, 190, 500, 24, 22, (0.24, 0.18, 0.15), 7, shadow=False, lw=2)   # him
    ellipse(k, 250, 470, 20, 20, b.KEY, 8, shadow=False, lw=2.4); ellipse(k, 240, 540, 20, 20, b.KEY, 9, shadow=False, lw=2.4)
    ellipse(k, 350, 500, 34, 34, (0.10, 0.10, 0.12), 10, shadow=False, lw=3)                                                              # it
    ellipse(k, 320, 452, 20, 20, (0.30, 0.30, 0.33), 11, shadow=False, lw=2.4); ellipse(k, 320, 548, 20, 20, (0.30, 0.30, 0.33), 12, shadow=False, lw=2.4)
    ellipse(k, 420, 360, 36, 26, (0.09, 0.09, 0.10), 13, shadow=False, lw=3); ellipse(k, 420, 360, 17, 16, (0.05, 0.05, 0.06), 14, shadow=False, lw=2)  # the Referee
    ellipse(k, 84, 690, 28, 22, (0.40, 0.40, 0.44), 15, shadow=False, lw=3)                                                               # Pam's cap
    rect(k, 150, 410, 240, 20, (0.96, 0.96, 0.93), 16, shadow=True, lw=2.4)                                                               # the plan's roll
    rect(k, 300, 430, 86, 70, (0.96, 0.96, 0.93), 17, shadow=True, lw=2.2)
    csh.noir(s)
    return s


def shot_52a(t):
    """The bell: four cuts round the ring, a quarter of a second each: from the front, his view of it, its view of
    him, from above."""
    i = min(int(t / 0.25), 3)
    if i == 0:
        return shot_52(0.0)
    if i == 1:
        return pov_client(t)
    if i == 2:
        return pov_robot(t, glove=False, far=True)
    return top_view()


def shot_53(t):
    """The robot's view: his glove, stopped a hand from the lens, shaking; over his face the three rows come up."""
    return pov_robot(t, words=0 if t < 0.3 else 1 if t < 0.45 else 2 if t < 0.6 else 3)


def shot_54(t):
    """Mom, in her office (a stand-in set): she reads the hundred beside her eyes; her eyes go to the desk; one ringed
    finger comes down on the button; her mouth opens a crack."""
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(s); k = Ctx(c, 0)
    c.set_source_rgb(0.30, 0.30, 0.32); c.paint()            # v3: a lit wall behind her: a black coat needs a pale ground
    g = cairo.RadialGradient(230, 420, 40, 230, 420, 560)   # the desk lamp throws up onto the wall
    g.add_color_stop_rgba(0, 0.86, 0.86, 0.84, 1); g.add_color_stop_rgba(0.6, 0.58, 0.58, 0.58, 1); g.add_color_stop_rgba(1, 0.30, 0.30, 0.32, 1)
    c.set_source(g); c.paint()
    c.set_source_rgb(0.16, 0.16, 0.18); c.rectangle(296, 100, 228, 396); c.fill()          # the window: night outside
    c.set_source_rgb(0.96, 0.96, 0.92)                       # the blinds behind her, lit from the ring she does not watch
    for i in range(13):
        c.rectangle(300, 110 + i * 30, 220, 17); c.fill()
    c.set_source_rgb(0.06, 0.06, 0.07); c.set_line_width(5); c.rectangle(296, 100, 228, 396); c.stroke()
    press = lerp(0.0, 1.0, (t - 1.15) / 0.12)
    sc = 1.55
    feet = 400 + 294 * sc + 112                              # v5: she sits: lower, the desk across her, a high chair behind
    cut(k, [(96, 800), (104, 500), (140, 462), (360, 462), (396, 500), (404, 800)], (0.33, 0.31, 0.30), shadow=False, lw=3)   # the chair's back, wide, to her ears
    for bx_ in (150, 250, 350):                              # its buttons
        ellipse(k, bx_, 520, 6, 6, (0.20, 0.19, 0.19), 20 + bx_, shadow=False, lw=1.6)
    down = lerp(0.0, 1.0, (t - 0.9) / 0.25)                  # v4: her own screen-right arm comes down onto the button
    P = q._body.__globals__["POSES"]
    old = P["q_read"]
    P["q_read"] = old[:2] + lerp(old[2:], q.mo.ik(1, 92, -124), down)
    try:
        o = q.queen(k, 250, feet, sc, "q_read", "bored", look=((-0.9, -0.1) if t < 0.9 else (0.8, 0.9)), note=True,
                    mouth=("dry" if 1.3 <= t < 1.75 else None))
    finally:
        P["q_read"] = old
    hx, hy = o["hands"][1]
    rect(k, -20, 790, 580, 200, (0.46, 0.44, 0.42), 5, shadow=False, lw=3)                 # her desk
    g = cairo.RadialGradient(400, 800, 10, 400, 800, 240)
    g.add_color_stop_rgba(0, 1, 1, 1, 0.35); g.add_color_stop_rgba(1, 1, 1, 1, 0); c.set_source(g); c.rectangle(0, 790, 540, 170); c.fill()
    bx, by = 250 + 92 * sc, 806
    rect(k, bx - 50, by - 2, 100, 26, (0.10, 0.10, 0.11), 6, shadow=False, lw=2.4)         # the button's plate
    lit = press > 0.9
    ellipse(k, bx, by + 5 * press, 30, 14 - 5 * press, (0.98, 0.98, 0.94) if lit else (0.55, 0.55, 0.56), 7, shadow=False, lw=2.6)
    if down > 0.6:                                            # one ringed finger, from her hand, on it
        fy = by - 4 + 5 * press
        c.set_source_rgb(0.08, 0.08, 0.09); c.set_line_width(19); c.set_line_cap(1); c.move_to(hx, hy); c.line_to(bx, fy); c.stroke()
        c.set_source_rgb(0.90, 0.76, 0.66); c.set_line_width(14); c.move_to(hx, hy); c.line_to(bx, fy); c.stroke(); c.set_line_cap(0)
        ellipse(k, hx, hy, 17, 17, (0.90, 0.76, 0.66), 10, shadow=False, lw=2.4)
        rect(k, (hx + bx) / 2 - 11, (hy + fy) / 2 - 6, 22, 12, (0.86, 0.87, 0.90), 11, shadow=False, lw=1.6)   # her ring
    csh.noir(s)
    return s


def shot_55(t):
    """The screen: a tick. Then, wider than 5.2: one jab, straight, like a piston; he goes over backwards."""
    if t < 0.4:
        return _insert_screen("tick")
    if t < 0.75:                                             # v8: through his eyes: the grey glove, at the lens
        return pov_client(t, "tick", jab=(t - 0.4) / 0.35)
    if t < 0.9:
        s = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); cairo.Context(s).paint()
        return s
    u = t - 0.9 + 0.34                                       # then, from outside, he is already going over
    hit = 0.34

    def ref(k):
        rg.shadow(k, 546, F - 96, 36); ca.referee(k, 546, F - 96, SC * ca.REL_REF, "ref_stand", look=(-0.8, 0.2), waistcoat=True)

    def robot(k):
        if u < hit - 0.2:
            pose, dx = "r_wait", 0
        elif u < hit - 0.07:                                # one: both gloves come up
            pose, dx = "r_guard", 0
        elif u < hit + 0.3:                                 # two, three: it rolls in and the piston goes out, and holds
            pose, dx = "r_jab", -34 * lerp(0.0, 1.0, (u - (hit - 0.07)) / 0.07)
        else:
            pose, dx = "r_wait", -34 + 34 * lerp(0.0, 1.0, (u - hit - 0.3) / 0.2)
        rg.shadow(k, 466 + dx, F - 46, 40)
        r.robot(k, 466 + dx, F - 46, SC * r.REL, pose, "tick", side=-1)

    def client(k):
        c = k.c
        if u < hit:
            x, f, a, face, pose = STOP, F - 40, 0.06, "hard", SWING
        else:
            v = lerp(0.0, 1.0, (u - hit) / 0.3)
            x, f, a, face, pose = STOP - 44 * v, F - 40 + 6 * v, 0.06 - 1.58 * v, "shock", lerp(SWING, (-70, -20, 70, 20), v)
        rg.shadow(k, x - 60 * (0.06 - a), F - 36, 44 + 30 * (0.06 - a))
        c.save(); c.translate(x, f); c.rotate(a); c.translate(-x, -f)
        b.boxer(k, x, f, Q, pose, face, (0.9, 0))
        c.restore()
        if hit <= u < hit + 0.1:                             # where it landed
            c.set_source_rgb(1, 1, 1); c.set_line_width(5); c.set_line_cap(1)
            for i in range(8):
                an = i * math.pi / 4
                c.move_to(STOP + 30 + 16 * math.cos(an), F - 226 + 16 * math.sin(an)); c.line_to(STOP + 30 + 40 * math.cos(an), F - 226 + 40 * math.sin(an)); c.stroke()
    return rg.frame((318, 1130, 1.0), [ref, robot, client], [], near=False, hats=False)


def shot_56(t):
    """From above: he lies flat on the canvas, arms out, the plan's shadow across his chest. A bare hand counts over
    him: one finger, two, three. He lifts his wrist to see the time: a glove. It drops. A stopwatch is held in to him."""
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(s); k = Ctx(c, 0)
    c.set_source_rgb(0.70, 0.70, 0.72); c.paint()
    g = cairo.RadialGradient(270, 470, 40, 270, 470, 560)
    g.add_color_stop_rgba(0, 1, 1, 1, 0.5); g.add_color_stop_rgba(1, 0, 0, 0, 0.35); c.set_source(g); c.paint()
    c.set_source_rgb(0.90, 0.90, 0.92)                       # the ropes, seen from over them, at the frame's edges
    for d in (22, 40, 58):
        c.rectangle(d, 0, 6, 960); c.fill(); c.rectangle(540 - d - 6, 0, 6, 960); c.fill()
    lift = 0.0                                               # v7: the watch gag is cut (unread in three tests; Tomas)
    pose = (-84, -4, lerp(84.0, 150.0, lift), lerp(4.0, 148.0, lift))
    x, f, sc = 262, 800, 1.5 * b.REL
    c.set_source_rgba(0, 0, 0, 0.28)                         # he is on the floor: a shadow all round him
    c.save(); c.translate(x, f - 230); c.scale(185, 300); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
    c.save(); c.translate(x, f); c.rotate(-0.10); c.translate(-x, -f)
    b.boxer(k, x, f, sc, pose, "exhausted", (0.0, -0.3))
    c.restore()
    c.set_source_rgba(0, 0, 0, 0.34)                         # the shadow of the plan: the roll, the hung end
    c.save(); c.translate(250, 470); c.rotate(-0.16); c.rectangle(-260, -16, 520, 32); c.fill(); c.rectangle(30, 16, 130, 120); c.fill(); c.restore()
    n = 1 if t < 0.6 else 2 if t < 1.2 else 3
    bob = 10 * abs(math.sin(t / 0.6 * math.pi))
    ca._open_hand(k, 420, 150 + bob, 3.2, math.pi / 2 + 0.25, n, 51)                        # the Referee's hand, counting
    rect(k, 420, -60, 90, 150 + bob, (0.96, 0.96, 0.94), 12, shadow=False, lw=2.6)        # his sleeve, from the top edge
    wx, wy = 74, 640                                          # Pam's stopwatch, held in from the ropes
    rect(k, -20, wy - 18, 70, 36, (0.86, 0.72, 0.62), 13, shadow=False, lw=2.4)
    ellipse(k, wx, wy, 44, 44, ca.CHROME, 14, shadow=False, lw=3)
    ellipse(k, wx, wy, 32, 32, (0.98, 0.98, 0.96), 15, shadow=False, lw=2)
    c.set_source_rgb(0.10, 0.10, 0.12); c.set_line_width(4); c.set_line_cap(1)
    an = -math.pi / 2 + t * 2.4
    c.move_to(wx, wy); c.line_to(wx + 26 * math.cos(an), wy + 26 * math.sin(an)); c.stroke()
    csh.noir(s)
    return s


FN = {"5.2a": shot_52a, "5.1a": shot_51a, "5.1b": shot_51b, "5.1c": shot_51c, "5.2": shot_52, "5.3": shot_53, "5.4": shot_54, "5.5": shot_55, "5.6": shot_56}


def frames():
    """Every frame in order: (shot, time in the film, surface)."""
    t0 = 0.0
    for name, dur in SHOTS:
        for i in range(round(dur * FPS)):
            yield name, t0 + i / FPS, FN[name](i / FPS)
        t0 += dur


def render(out):
    d = os.path.dirname(os.path.abspath(out))
    parts = []
    for name, dur in SHOTS:
        tmp, fin = os.path.join(d, "_on3_%s.tmp.mp4" % name), os.path.join(d, "_on3_%s.mp4" % name)
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", "540x960", "-r", str(FPS),
                              "-i", "-", "-vf", "format=yuv420p", "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p",
                              "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", tmp], stdin=subprocess.PIPE)
        for i in range(round(dur * FPS)):
            p.stdin.write(bytes(FN[name](i / FPS).get_data()))
        p.stdin.close()
        assert p.wait() == 0, name
        os.replace(tmp, fin); parts.append(fin)
    lst = os.path.join(d, "_on3_list.txt")
    open(lst, "w").write("".join("file '%s'\n" % p_ for p_ in parts))
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", out])
    for p_ in parts + [lst]:
        os.remove(p_)


def sheets(d, prefix="sheet", fast=("5.2", "5.5")):
    """Contact sheets for the cold test: every 4th of a second, numbered and timed; the punch at 8 a second; and the
    4-a-second sheet again at phone size."""
    os.makedirs(d, exist_ok=True)
    fr = list(frames())

    def grid(pick, cols, w, name, start=0):
        z = w / 540
        rows = (len(pick) + cols - 1) // cols
        s = cairo.ImageSurface(cairo.FORMAT_RGB24, cols * (w + 8) + 8, rows * (int(960 * z) + 30) + 8)
        c = cairo.Context(s); c.set_source_rgb(0.15, 0.15, 0.16); c.paint()
        for n, (_, t, f) in enumerate(pick):
            x, y = 8 + (n % cols) * (w + 8), 8 + (n // cols) * (int(960 * z) + 30)
            c.save(); c.translate(x, y + 24); c.scale(z, z); c.set_source_surface(f, 0, 0); c.paint(); c.restore()
            c.set_source_rgb(1, 1, 1); c.select_font_face("Inter", 0, 1); c.set_font_size(16)
            c.move_to(x + 2, y + 17); c.show_text("%d   %.2f s" % (start + n + 1, t))
        s.write_to_png(os.path.join(d, name))
    four = [fr[i] for i in range(0, len(fr), 7)]              # about 4 a second
    third = (len(four) + 2) // 3
    for j, tag in enumerate("abc"):
        grid(four[j * third:(j + 1) * third], 5, 400, prefix + "_4fps_%s.png" % tag, start=j * third)
    grid([x for x in fr if x[0] in fast][::4], 7, 280, prefix + "_8fps_punches.png")
    grid(four, 10, 200, prefix + "_phone.png")


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "../office-noir-3/on3_beat05_rough_v8.mp4"
    if len(sys.argv) > 2:
        sheets(sys.argv[2])
    else:
        render(out)
