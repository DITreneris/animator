"""ONE STAR (episode 11): the animation pass, scene 4 "The human's blueprint" (script v16, beat 04), after layout v2
and Tomas's answers (20 Nov, /grill-me). Native 1080, 12 drawings a second, out at 30 fps.

The 7 is revealed in steps, one job a shot:
  4.1  Pam steps into his way with her roll (in her hand); one hand pushes her glasses up              (Tomas)
  4.2  top shot: she shoves her sleeves up, unrolls her taped plan over the AI's: THE PROBLEM, a gap  (Tomas)
       (a torn hole, no red 7; MY GARAGES in her pen on a strip of tape)
  4.2b THE SUSPICION: she points at the blue edge in his pocket (arm by IK from her shoulder, elbow bent)
  4.3a THE REACTION: the strip out in his fist, its blank back to us; he looks at its face and freezes  (Tomas)
  4.3c THE PROOF: close, his oily fist turns it to us: the first readable 7
  4.3b THE EXPLANATION, two beats in one shot: his hand spins the first strip (9 -> 6); he lays the 7 in the
       gap, her thumb presses the tape beside it                                                      (Tomas)
  4.4  close two-shot, the robot and Pam: its visor dims; the paddle in its hand flips: FOUND BY: HUMAN, the
       arrow on her                                                                                   (Tomas)
Framing: the series' face scale and the apps' zones, checked by cs_frame on every drawing.
  python3 cs_scene4.py [out_dir] [lo]  ->  cs_scene4_v1.mp4, _strip.png, cs_scene4_timing_v1.json"""
import json
import math
import os
import subprocess
import sys
import cairo
import numpy as np
import soundfile as sf
import kit
import fs_storyboard as sb
import pam_bc as pb
import acts_ob as ac
import cs_props as cp
import cs_anim as A
import cs_scene1 as s1
import cs_scene3 as s3
import cs_board3 as b3
from cand_bc import ik
from cs_board import S, at, base
from kit import Ctx, INK, ellipse, rect, cut

V = "v4"
DPS = 12
SR = 48000
TAKES = s1.TAKES
HI = s1.HI
ease, br, Breath = s1.ease, s1.br, s1.Breath
BLUE = (0.18, 0.42, 0.85)
OLIVE = (0.42, 0.44, 0.24)
CUFF = (0.98, 0.97, 0.94)
SKIN_CL = sb.SKIN_CL
SKIN_PAM, PURPLE = A.SKIN_PAM, A.PURPLE
PAM_S = sb.SC["pam"]
PAM_FEET = sb.F + 6
PAM_SH_R = (40.0, -300 * kit.PEOPLE["PAM"]["h"] + 78 + 14)   # her screen-right shoulder, her own (unscaled) frame
LN = 48.0
CL_SH_R = (42.64, 649.12)                                  # his screen-right shoulder: x from his x, y in the scene (measured)
CL_LN = 31.98


def lerp(a, b, t):
    return tuple(x + (y - x) * t for x, y in zip(a, b))


class Strip:
    """His pocket strip for one drawing: "edge" (only the blue edge above the pocket) or None (it is out)."""
    def __init__(self, kind="edge"):
        self.kind = kind

    def __enter__(self):
        self.op = sb.pocket_strip
        if self.kind == "edge":
            def edge(k, o, s, x=None, feet=None):
                hx, hy = o["hands"][-1]
                c = k.c
                c.save(); c.translate(hx - 4 * s, hy - 26 * s); c.rotate(-0.35); c.scale(s, s)
                rect(k, -5, -8, 10, 12, BLUE, 771, shadow=False, lw=1.4)
                c.restore()
            sb.pocket_strip = edge
        else:
            sb.pocket_strip = lambda *a, **kw: None
        return self

    def __exit__(self, *e):
        sb.pocket_strip = self.op


def pam(k, x, pose, face, look, glasses="up", lean=0.0, d=0):
    c = k.c
    c.save(); c.translate(x, PAM_FEET); c.scale(1.0, br(d, 0.5)); c.translate(-x, -PAM_FEET)
    o = pb.pam(k, x, PAM_FEET, PAM_S, pose, face, look, glasses=glasses, lean=lean)
    c.restore()
    return o


def pam_reach(x, lean, target, side=-1):
    """Her screen-right arm's two angles for a hand at target (scene), by IK from her shoulder, fixed segments."""
    a = math.radians(-lean)
    vx, vy = target[0] - x, target[1] - PAM_FEET
    lx = (vx * math.cos(a) - vy * math.sin(a)) / PAM_S
    ly = (vx * math.sin(a) + vy * math.cos(a)) / PAM_S
    return ik(PAM_SH_R[0], PAM_SH_R[1], lx, ly, LN, LN, side)


# ---- 4.1 Pam in his way --------------------------------------------------------------------------------------------------

N41 = 24
CAM41 = (229, 665, 2.55)
ROLL_ARM = (-14, 30)                                        # her screen-left arm, the roll upright in that hand
GLASSES = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.3, 0.7, 1, 1, 1, 0.7, 0.3, 0, 0, 0, 0, 0, 0, 0]   # her other hand up and back


def s4_1(k, d):
    """24 drawings (2.0 s). He is going for the door; Pam steps in from the left, the blue roll upright in her hand;
    he stops short; her other hand goes up and pushes her glasses into her hair (d12); she holds his eye."""
    px = 96 + (175 - 96) * ease(d / 7.0)
    cx = 318 - (318 - 285) * ease(d / 6.0)
    g = GLASSES[d]
    arm = lerp((8, 0), (158, 38), ease(g))
    lean = -3.0 * ease((d - 5) / 3.0) * (1 - ease((d - 10) / 4.0))                # he rocks back as she lands
    got = {}

    def pre(k_):
        got["o"] = o = pam(k_, px, ROLL_ARM + arm, "neutral", (1, -0.2), glasses="up" if d >= 12 else "low", d=d)
        hx, hy = min(o["hands"])                                                  # her screen-left hand: the roll in it
        c = k_.c
        c.save(); c.translate(hx - 1, hy - 4); c.rotate(-0.08)
        rect(k_, -6, -44, 12, 62, BLUE, 995, lw=1.6)
        c.set_source_rgba(0.98, 0.96, 0.86, 0.9); c.rectangle(-6.5, -14, 13, 6); c.fill()
        ellipse(k_, 0, -44, 6, 2.4, (0.30, 0.52, 0.92), 996, shadow=False, lw=1.2)
        c.restore()
        ellipse(k_, hx, hy, 5.0, 5.4, SKIN_PAM, 997, shadow=False, lw=1.2)        # her fingers round it

    with Strip("edge"), s3.Client(lean=lean, edge=False), Breath(sb, "client", br(d, 0.4)):
        S(k, CAM41, auto=False, portrait=False, pre=pre,
          **base(door=0.6, rb=False, sf=False, dn=False, pm=False, mm=False,
                 cl=at("client", x=cx, face="suspicious", look=(-1, 0.25))))


# ---- 4.2 the taped plan: the problem ------------------------------------------------------------------------------------

N42 = 24                                                   # the trim (21 Nov): the push in on the gap shorter
PLAN_BOX = (20, 236, 500, 432)                              # the taped plan in the frame (x, y, w, h)
GAP_AT = (184, 568)                                         # the gap at 7, frame


def _plan_surface(state, flip=None):
    """The taped plan alone (no desk) on a clear surface, layout v2's gap and title."""
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540 * HI[0], 960 * HI[0])
    if HI[0] > 1:
        s.set_device_scale(HI[0], HI[0])
    k = Ctx(cairo.Context(s), 0)
    old = cp._bg, cp.PROPS4[0], cp.GAP_PLAIN[0], cp.TITLE_TAPE[0], cp.FLIP0[0], cp.NOTAPE7[0]
    dy = cp.TAPE7_DY[0]; cp.TAPE7_DY[0] = -9.0
    cp._bg = lambda *a, **kw: None
    cp.PROPS4[0] = cp.GAP_PLAIN[0] = cp.TITLE_TAPE[0] = True; cp.FLIP0[0] = flip
    cp.NOTAPE7[0] = state == "whole_notape"
    try:
        cp.plan(k, "whole" if state == "whole_notape" else state)
    finally:
        cp._bg, cp.PROPS4[0], cp.GAP_PLAIN[0], cp.TITLE_TAPE[0], cp.FLIP0[0], cp.NOTAPE7[0] = old
        cp.TAPE7_DY[0] = dy
    return s


def _desk(k):
    """The desk: the AI's glossy SITE PLAN lying on it, stepped back."""
    c = k.c
    old = cp.PROPS4[0]; cp.PROPS4[0] = False
    try:
        cp.ai_site(k)
    finally:
        cp.PROPS4[0] = old
    c.set_source_rgb(0.20, 0.45, 0.85); c.rectangle(36, 126, 468, 104); c.fill()
    cp.T(c, "SITE PLAN", 270, 168, 40, col=(1, 1, 1))
    cp.T(c, "99% CONFIDENT", 270, 212, 30, col=(1, 0.9, 0.3))
    c.set_source_rgba(0.10, 0.08, 0.06, 0.38); c.paint()


def limb(k, x0, y0, x1, y1, w, sleeve, col, skin, cuff=None, seed=900, thumb=None, oil=False):
    """An arm in a top shot, from off frame (x0, y0) to its hand at (x1, y1): the sleeve over the first `sleeve`
    of it (0-1), the bare forearm after, the hand; cuff: a white cuff at the sleeve's end; thumb: +1/-1 its side."""
    c = k.c
    L = math.hypot(x1 - x0, y1 - y0); ang = math.atan2(y1 - y0, x1 - x0)
    c.save(); c.translate(x0, y0); c.rotate(ang)
    cut(k, [(L * sleeve - 4, -w * 0.42), (L - 10, -w * 0.40), (L - 10, w * 0.40), (L * sleeve - 4, w * 0.42)], skin, shadow=False, lw=2.4)
    cut(k, [(0, -w / 2), (L * sleeve, -w / 2), (L * sleeve, w / 2), (0, w / 2)], col, shadow=False, lw=2.4)
    if cuff:
        rect(k, L * sleeve - 6, -w / 2 - 2, 16, w + 4, cuff, seed + 1, shadow=False, lw=2)
    else:                                                                          # shoved up: bunched
        c.set_source_rgb(*INK); c.set_line_width(1.6)
        for i in range(3):
            xx = L * sleeve - 6 - i * 9
            if xx > 4:
                c.move_to(xx, -w / 2 + 3); c.curve_to(xx + 4, -w / 6, xx + 4, w / 6, xx, w / 2 - 3); c.stroke()
    ellipse(k, L, 0, w * 0.55, w * 0.50, skin, seed + 2, shadow=False, lw=2.4)
    if thumb:
        ellipse(k, L - 2, thumb * w * 0.50, w * 0.30, w * 0.20, skin, seed + 3, shadow=False, lw=2)
    if oil:
        c.set_source_rgba(0.15, 0.13, 0.10, 0.35); c.set_line_width(2.2)
        for dx in (-8, 4):
            c.move_to(L + dx, -w * 0.25); c.line_to(L + dx + 3, w * 0.25); c.stroke()
    c.restore()


def s4_2(k, d):
    """28 drawings (2.3 s). Top shot, the AI's sheet on the desk. Her hands come in: one shoves the other's sleeve
    up, and back (d0-8); they unroll her taped plan down over the AI's (d9-17); they leave; a slow push in on the
    gap where 7 should be (d18-27): the problem."""
    c = k.c
    z = 1.0 + 0.16 * ease((d - 18) / 5.0)
    c.save(); c.translate(*GAP_AT); c.scale(z, z); c.translate(-GAP_AT[0], -GAP_AT[1])
    _desk(k)
    x0, y0, w, h = PLAN_BOX
    u = ease((d - 9) / 8.0)
    ry = y0 + h * u                                                               # the roll's place
    if d >= 9:
        c.save(); c.rectangle(0, 0, 540, ry); c.clip()
        c.set_source_surface(_plan_surface("before"), 0, 0); c.paint()
        c.restore()
    if 9 <= d <= 17 and u < 1:                                                    # the roll, still to unroll
        rect(k, x0 - 6, ry - 14, w + 12, 30, BLUE, 941, lw=2.4)
        c.set_source_rgba(1, 1, 1, 0.25); c.rectangle(x0 - 4, ry - 10, w + 8, 6); c.fill()
    # her arms, from the top
    if d < 9:
        a = ease((d - 1) / 3.0); b = ease((d - 5) / 3.0)                           # left sleeve up, then the right
        sl, sr = 0.86 - 0.42 * a, 0.86 - 0.42 * b
        lh, rh = (170, 400), (370, 400)
        if d < 5:                                                                  # the right hand on the left cuff
            cy_ = -60 + (460) * sl
            limb(k, 160, -60, lh[0], lh[1], 84, sl, PURPLE, SKIN_PAM, seed=911)
            limb(k, 470, -60, 196, cy_ + 16, 84, 0.84, PURPLE, SKIN_PAM, seed=921, thumb=-1)
        else:
            cy_ = -60 + (460) * sr
            limb(k, 380, -60, rh[0], rh[1], 84, sr, PURPLE, SKIN_PAM, seed=921)
            limb(k, 70, -60, 344, cy_ + 16, 84, sl, PURPLE, SKIN_PAM, seed=911, thumb=1)
    elif d <= 20:
        out = ease((d - 17) / 3.0)                                                 # then they leave, up
        hy = ry - 6 - out * 520
        limb(k, 80, -60 - out * 300, 96, hy, 84, 0.44, PURPLE, SKIN_PAM, seed=911, thumb=1)
        limb(k, 460, -60 - out * 300, 444, hy, 84, 0.44, PURPLE, SKIN_PAM, seed=921, thumb=-1)
    c.restore()


# ---- 4.2b the suspicion ------------------------------------------------------------------------------------------------

N42b = 14
CAM42b = (246, 690, 2.6)
PX42b, LEAN42b = 188, 4.0
POCKET = (296.0, 691.0)                                     # the blue edge above his pocket (scene)


def s4_2b(k, d):
    """14 drawings (1.2 s). Pam's eyes drop to his pocket; her arm comes up, elbow bent, her finger stopping just
    short of the blue edge sticking out of it; he looks down at it."""
    r = ease((d - 2) / 4.0)
    rest = (PX42b + 24, PAM_FEET - 64)
    sh = (PX42b + PAM_SH_R[0] * PAM_S, PAM_FEET + PAM_SH_R[1] * PAM_S)             # her hand 40 units out along the line to
    L_ = math.hypot(POCKET[0] - sh[0], POCKET[1] - sh[1])                          # the pocket, the finger pointing on at it
    aim = (sh[0] + (POCKET[0] - sh[0]) * 40 / L_, sh[1] + (POCKET[1] - sh[1]) * 40 / L_)
    tgt = lerp(rest, aim, r)
    a1, a2 = pam_reach(PX42b, LEAN42b * r, tgt)
    look_c = (1, 0) if d < 5 else (0.3, 1)
    got = {}

    def pre(k_):
        got["o"] = pam(k_, PX42b, (-8, 0, a1, a2), "neutral", (1, 0.7), glasses="up", lean=LEAN42b * r, d=d)

    def ex(k_, o):
        if r > 0.5:                                                               # her arm again, over his jacket: from
            c = k_.c                                                               # her shoulder, sleeve shoved up
            c.save(); c.translate(PX42b, PAM_FEET); c.rotate(math.radians(LEAN42b * r)); c.scale(PAM_S, PAM_S); c.set_line_cap(1)
            dd = lambda a: (math.sin(math.radians(a)), math.cos(math.radians(a)))
            sx_, sy_ = PAM_SH_R
            ex_, ey_ = sx_ + dd(a1)[0] * LN, sy_ + dd(a1)[1] * LN
            wx, wy = ex_ + dd(a1 + a2)[0] * LN, ey_ + dd(a1 + a2)[1] * LN
            for (ax, ay, bx, by), col in (((sx_, sy_, ex_, ey_), PURPLE), ((ex_, ey_, wx, wy), SKIN_PAM)):
                an = math.atan2(by - ay, bx - ax); nx, ny = -math.sin(an) * 8.5, math.cos(an) * 8.5
                cut(k_, [(ax + nx, ay + ny), (bx + nx, by + ny), (bx - nx, by - ny), (ax - nx, ay - ny)], col, shadow=False, lw=2)
            ellipse(k_, ex_, ey_, 9, 9, PURPLE, 997, shadow=False, lw=2)
            ellipse(k_, wx, wy, 10, 9, SKIN_PAM, 999, shadow=False, lw=2)
            an = math.atan2(wy - ey_, wx - ex_)                                    # her finger, on toward the pocket
            fx, fy = wx + math.cos(an) * 15, wy + math.sin(an) * 15
            c.set_source_rgb(*INK); c.set_line_width(9.5); c.move_to(wx, wy); c.line_to(fx, fy); c.stroke()
            c.set_source_rgb(*SKIN_PAM); c.set_line_width(6); c.move_to(wx, wy); c.line_to(fx, fy); c.stroke()
            c.restore()

    with Strip("edge"), s3.Client(edge=False), Breath(sb, "client", br(d, 0.4)):
        S(k, CAM42b, auto=False, portrait=False, pre=pre, extra=ex,
          **base(door=0.0, rb=False, sf=False, dn=False, pm=False, mm=False,
                 cl=at("client", x=285, face="puzzled", look=look_c)))


# ---- 4.3a the reaction ---------------------------------------------------------------------------------------------------

N43a = 18
CAM43a = (285, 656, 3.15)
CX = 280
HAND = [(322.6, 713.1), (322.6, 713.1), (306, 700), (300, 694), (300, 690), (300, 682), (298, 674), (296, 668)]


def s4_3a(k, d):
    """18 drawings (1.5 s). His hand goes to his pocket and comes out with the strip, up to his chest: its blank
    back to us. He looks at its face. His eyes go wide; red from the collar; he freezes (the last 8 drawings,
    breathing only)."""
    hx, hy = HAND[min(d, len(HAND) - 1)]
    a1, a2 = ik(CX + CL_SH_R[0], CL_SH_R[1], hx, hy, CL_LN, CL_LN, 1)
    out = d >= 4
    face = "plain" if d < 8 else ("dawning" if d < 10 else "shock")
    look = (0.3, 1) if d < 6 else (0.55, 0.9)

    def ex(k_, o):
        if not out:
            return
        (lx, ly), (rx, ry) = sorted(o["client"]["hands"])
        c = k_.c
        c.save(); c.translate(rx, ry - 2); c.rotate(-0.22)
        rect(k_, -6.5, -34, 13, 40, BLUE, 773, lw=1.5)                             # its back: plain blue paper
        c.set_source_rgba(1, 1, 1, 0.18); c.set_line_width(0.8)
        c.move_to(-4, -26); c.line_to(4, -24); c.stroke()
        c.restore()
        ellipse(k_, rx, ry + 1, 7.6, 7.0, SKIN_CL, 774, lw=1.5)                    # his fist round its foot
        ellipse(k_, rx - 5.5, ry - 5, 2.8, 4.4, SKIN_CL, 775, shadow=False, lw=1.2)   # the thumb across it

    with Strip(None if out else "edge"), s3.Client(edge=False), Breath(sb, "client", br(d, 0.4, 0.012)):
        S(k, CAM43a, auto=False, portrait=False, extra=ex,
          **base(door=0.0, rb=False, sf=False, dn=False, pm=False, mm=False,
                 cl=at("client", x=CX, pose=(-8, 0, a1, a2), face=face, look=look)))
    if d >= 9:
        b3.flush(k, "client", min(0.32, (d - 8) * 0.08))


# ---- 4.3c the proof ----------------------------------------------------------------------------------------------------

N43c = 14


def s4_3c(k, d):
    """14 drawings (1.2 s). Close: his oily fist (one palm, the fingers round the strip, the thumb across it) turns
    the strip to us: the 7, ringed in red. Held, breathing."""
    c = k.c
    sb.bg(c, OLIVE)                                                                # his jacket behind
    c.set_source_rgba(0, 0, 0, 0.10); c.set_line_width(3)
    c.move_to(120, 0); c.curve_to(150, 300, 100, 600, 140, 960); c.stroke()        # a seam
    sway = 3.0 * math.sin(2 * math.pi * d / float(DPS) / A.BREATH)
    turn = math.cos(math.pi * ease((d - 1) / 4.0))                                 # 1 = its back, -1 = its face
    c.save(); c.translate(270, 430 + sway); c.rotate(-0.16)
    w = 150 * abs(turn)
    if w > 4:
        rect(k, -w / 2, -250, w, 430, BLUE, 774, lw=4)
        if turn < 0:
            c.save(); c.scale(abs(turn), 1.0)
            c.set_source_rgb(*cp.RED); c.set_line_width(11); c.new_path(); c.arc(0, -60, 66, 0, 6.3); c.stroke()
            cp.T(c, "7", 0, -16, 128, col=(1, 1, 1))
            c.set_source_rgb(1, 1, 1); c.set_line_width(5)                         # the bay's door under it
            c.rectangle(-36, 40, 72, 60); c.stroke()
            for yy in (55, 70, 85):
                c.move_to(-36, yy); c.line_to(36, yy); c.stroke()
            c.restore()
    else:
        c.set_source_rgb(*INK); c.set_line_width(5); c.move_to(0, -250); c.line_to(0, 180); c.stroke()
    # the fist: the sleeve and cuff, one palm, the fingers as one block with creases, the thumb across the strip
    rect(k, -92, 330, 184, 400, OLIVE, 951, lw=4)
    rect(k, -100, 300, 200, 46, CUFF, 952, shadow=False, lw=3.5)
    cut(k, [(-104, 120), (-96, 60), (96, 60), (106, 120), (100, 300), (-98, 300)], SKIN_CL, lw=4)          # the palm
    cut(k, [(-112, 150), (-100, 96), (60, 92), (80, 110), (82, 196), (60, 214), (-104, 210)], SKIN_CL, shadow=False, lw=4)   # fingers
    c.set_source_rgb(*INK); c.set_line_width(3)
    for xx in (-62, -18, 26):
        c.move_to(xx, 98); c.line_to(xx - 3, 208); c.stroke()
    cut(k, [(72, 268), (44, 204), (-14, 104), (-6, 70), (30, 64), (112, 214), (106, 276)], SKIN_CL, shadow=False, lw=4)       # the thumb, across the strip
    ellipse(k, 8, 88, 14, 11, (0.95, 0.86, 0.80), 955, shadow=False, lw=2)          # its nail
    c.set_source_rgba(0.15, 0.13, 0.10, 0.40); c.set_line_width(4)                # oil in the creases
    for (x0, y0, x1, y1) in ((-84, 232, -30, 250), (0, 240, 40, 262), (-90, 270, -60, 284)):
        c.move_to(x0, y0); c.line_to(x1, y1); c.stroke()
    c.restore()


# ---- 4.3b the explanation ------------------------------------------------------------------------------------------------

N43b = 28


def _bay7():
    n_, bx, by, bw, bh = [b for b in ac._bays() if b[0] == 7][0]
    s, x, y = 3.9, 270, 470
    return (x + (bx - 2) * s, y + (by - 3) * s, (bw + 4) * s, (bh + 16) * s)


def s4_3b(k, d):
    """28 drawings (2.3 s), two beats. One: his hand on the first strip spins it round, the 9 becomes a 6 (d0-9).
    Two: his hand brings the 7 up into the gap (d10-16); her thumb comes down and presses the tape at its end,
    beside the 7 (d17-21); the plan whole, held."""
    c = k.c
    _desk(k)
    turn = math.pi * (1 - ease((d - 2) / 6.0))
    if d < 10:
        c.set_source_surface(_plan_surface("before", flip=turn), 0, 0); c.paint()
        up = ease(d / 2.0) * (1 - ease((d - 8) / 2.0))                             # his hand in, then away
        limb(k, -40 - (1 - up) * 200, 1010 + (1 - up) * 200, 92, 600, 60, 0.58, OLIVE, SKIN_CL, cuff=CUFF, seed=931,
             thumb=-1, oil=True)
        return
    gx, gy, gw, gh = _bay7()
    taped = d >= 19
    z = 1.0 + 0.28 * ease((d - 21) / 6.0)                                          # and in on the 7, home
    c.save(); c.translate(189, 590); c.scale(z, z); c.translate(-189, -590)
    try:
        _beat2(k, d, gx, gy, gw, gh, taped)
    finally:
        c.restore()


def seven(c, ox=0.0, oy=0.0):
    """Bay 7's number, clear of the red ring's tail (the prop draws the ring over it)."""
    cp.T(c, "7", 189 + ox, 639 + oy, 29, col=(1, 1, 1))


def _beat2(k, d, gx, gy, gw, gh, taped):
    c = k.c
    c.set_source_surface(_plan_surface("whole" if taped else "turned"), 0, 0); c.paint()
    if taped or d >= 16:
        seven(c)
    if not taped:
        u = ease((d - 10) / 6.0)                                                   # the 7 comes up from the bottom, in his hand
        ox, oy = (1 - u) * 60, (1 - u) * 420
        whole = _plan_surface("whole_notape")
        c.save(); c.translate(ox, oy); c.rectangle(gx, gy, gw, gh); c.clip()
        c.set_source_surface(whole, 0, 0); c.paint(); c.restore()
        c.set_source_rgb(*INK); c.set_line_width(2); c.rectangle(gx + ox, gy + oy, gw, gh); c.stroke()
        if d < 16:
            seven(c, ox, oy)
        out = ease((d - 16) / 2.0)
        limb(k, 420 + ox + out * 200, 1040 + oy + out * 300, gx + gw + 14 + ox + out * 120, gy + gh * 0.72 + oy + out * 200, 60, 0.58,
             OLIVE, SKIN_CL, cuff=CUFF, seed=931, thumb=-1, oil=True)
    press = ease((d - 16) / 3.0) * (1 - ease((d - 22) / 3.0))                      # her thumb: down on the tape's end
    if press > 0:
        tx, ty = gx - 22, gy + gh * 0.30
        limb(k, 60, -60, tx - (1 - press) * 40, ty - (1 - press) * 260, 54, 0.44, PURPLE, SKIN_PAM, seed=911, thumb=-1)


# ---- 4.4 FOUND BY: HUMAN ----------------------------------------------------------------------------------------------

N44 = 34
CAM44 = (317, 717, 2.39)
PX44 = 262
LINE44 = (0.25, 0.25 + 2.18)
FLIP44 = (4, 8)                                            # drawings: the paddle turns to us


def s4_4(k, d):
    """34 drawings (2.8 s). The robot and Pam, close. A beat of defeat: its visor dims. Then the paddle in its hand
    flips to us: FOUND BY: HUMAN, its arrow on Pam. She looks at the arrow, then down and away, almost pleased."""
    t = d / float(DPS)
    f = ease((d - FLIP44[0]) / float(FLIP44[1] - FLIP44[0]))
    speaking = LINE44[0] <= t <= LINE44[1]
    look_p = (1, 0.2) if d < 13 else ((1, -0.1) if d < 24 else (-0.4, 0.8))
    face_p = "neutral" if d < 16 else "pleased"

    def pre(k_):
        pam(k_, PX44, "stand", face_p, look_p, glasses="up", d=d)

    def ex(k_, o):
        c = k_.c
        sx, sy = o["robot"]["screen"]
        r = 50 * sb.SC["robot"]
        dim = 0.6 * (1 - f)
        if speaking and (d // 2) % 3 == 0:
            dim = min(0.75, dim + 0.2)
        if dim > 0:                                                                # defeat: the visor dims
            c.set_source_rgba(0.02, 0.03, 0.06, dim); c.new_path(); c.arc(sx, sy, 0.78 * r, 0, 6.3); c.fill()
        hx, hy = min(o["robot"]["hands"])                                          # its raised hand
        c.set_source_rgb(*INK); c.set_line_width(4.2); c.set_line_cap(1)           # the paddle's handle, in its hand
        c.move_to(hx, hy + 3); c.line_to(hx - 6, hy - 26); c.stroke()
        c.set_source_rgb(0.70, 0.55, 0.35); c.set_line_width(2.4); c.move_to(hx, hy + 3); c.line_to(hx - 6, hy - 26); c.stroke()
        ellipse(k_, hx, hy, 4.2, 4.2, (0.62, 0.64, 0.68), 983, shadow=False, lw=1.2)   # its grip over the handle
        turn = math.cos(math.pi * f)                                               # 1 = its back, -1 = its face
        c.save(); c.translate(hx - 7, hy - 44); c.rotate(-0.04); c.scale(max(0.06, abs(turn)), 1.0)
        rect(k_, -33, -20, 66, 40, (1, 1, 1) if turn < 0 else (0.80, 0.82, 0.86), 982, lw=2)
        if turn < 0:                                                               # cold test: FOUND BY too small, HUMAN clipped
            cp.T(c, "FOUND BY:", 0, -5, 10.5, col=INK)
            cp.T(c, "HUMAN", 0, 13, 15, col=cp.GRN)
            c.set_source_rgb(*cp.GRN); c.set_line_width(3.4); c.set_line_cap(1); c.set_line_join(1)   # the arrow, at her
            c.move_to(-36, 0); c.line_to(-52, 0); c.stroke()
            c.move_to(-45, -6); c.line_to(-53, 0); c.line_to(-45, 6); c.stroke()
        c.restore()

    with Breath(sb, "robot", br(d, 0.5, 0.006)):
        S(k, CAM44, auto=False, portrait=False, pre=pre, extra=ex,
          **base(cl=False, sf=False, dn=False, mm=False, pm=False, door=0.0, rb=at("robot", arm="paddle")))


SHOTS = [("4.1", N41, s4_1), ("4.2", N42, s4_2), ("4.2b", N42b, s4_2b), ("4.3a", N43a, s4_3a), ("4.3c", N43c, s4_3c),
         ("4.3b", N43b, s4_3b), ("4.4", N44, s4_4)]


def schedule():
    n = sum(nd for sh, nd, _ in SHOTS[:-1])
    return [("4.4", n / float(DPS) + LINE44[0])]


def draw(fn, d):
    return s1.draw(fn, d)


def main(out_dir):
    tmp = "/tmp/cs_s4"; os.makedirs(tmp, exist_ok=True)
    lst, n, tiles = open(tmp + "/list.txt", "w"), 0, []
    for shot, nd, fn in SHOTS:
        for d in range(nd):
            f = draw(fn, d)
            p = "%s/d%03d.png" % (tmp, n); f.write_to_png(p)
            lst.write("file '%s'\nduration %.6f\n" % (p, 1.0 / DPS))
            tiles.append(("#%d %s %.2f s" % (n + 1, shot, n / float(DPS)), f)); n += 1
    lst.write("file '%s'\n" % p); lst.close()
    total = n / float(DPS)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", tmp + "/list.txt",
                    "-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                    "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", tmp + "/v.mp4"], check=True)
    meta = json.load(open(TAKES + "/takes.json"))
    a = np.zeros(int((total + 0.3) * SR))
    for key, t0 in schedule():
        x, _ = sf.read("%s/%s.wav" % (TAKES, key))
        p_ = int(t0 * SR); a[p_:p_ + len(x)] += x[:len(a) - p_]
    sf.write(tmp + "/a.wav", (a / max(1e-9, np.abs(a).max()) * 0.7).astype(np.float32), SR)
    r_ = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", tmp + "/a.wav", "-af", "ebur128", "-f", "null", "-"],
                        capture_output=True, text=True)
    cur = float([x for x in r_.stderr.split("\n") if "I:" in x][-1].split("I:")[1].split("LUFS")[0])
    out = os.path.join(out_dir, "cs_scene4_%s.mp4" % V)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp + "/v.mp4", "-i", tmp + "/a.wav", "-map", "0:v", "-map", "1:a",
                    "-af", "volume=%.2fdB,alimiter=limit=0.60:attack=2:release=40:level=disabled" % (-11.5 - cur),
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", tmp + "/o.part.mp4"], check=True)
    os.replace(tmp + "/o.part.mp4", out)
    json.dump({"shots": [{"shot": k, "line": {"key": k, "who": meta[k]["who"], "text": meta[k]["text"], "t0": round(t0, 3),
                                                "t1": round(t0 + meta[k]["len"], 3)}} for k, t0 in schedule()]},
              open("cs_scene4_timing_%s.json" % V, "w"), indent=1)
    A.strip(tiles[::2], os.path.join(out_dir, "cs_scene4_%s_strip.png" % V), 160, 10)
    print("wrote", out, "%d drawings, %.2f s" % (n, total))


if __name__ == "__main__":
    if "lo" in sys.argv[1:]:
        HI[0] = 1
    args = [a for a in sys.argv[1:] if a != "lo"]
    main(args[0] if args else "../customer-success")
