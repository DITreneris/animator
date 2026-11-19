"""OFFICE NOIR 3: a moving rough of beats 06 and 07 (6.1 to 7.5), mute, for the cold test (19 Nov). v2; ring_rough2_on3_v1.py
is v1. v2, after cold test 8 and /grill-me: 6.2's right half is Mom from the front, seated, her hand on the open cash
box, and the oil can is big; 6.4 has a closer shot for his pointing, Don's back leaving in it; in 7.3 he claps the sheet
between two gloves and it slides up and out. v1:
On the ring (ring_on3), with ring_rough_on3's helpers. A rough: poses change and figures slide. Mom's desk is the
stand-in of 5.4 (she sits); Don is Office Noir 2's detective, unchanged (Tomas, /grill-me); in 7.3 the paper slides off
the glove (Tomas).
Usage: python3 ring_rough2_on3.py [out.mp4] [sheets_dir]   (default ../office-noir-3/on3_beat0607_rough_v2.mp4)"""
import sys
import math
import cairo
import kit
import ring_on3 as rg
import ring_casts_on3 as rc
import ring_rough_on3 as rr
import cast_on3 as ca
import client_on3 as b
import robot_on3 as r
import sofia_on3 as so3
import mom_on3 as q
import noir2_cast as n2
import client_sheet_on3 as csh
from kit import Ctx, cut, rect, ellipse, INK

F, SC, Q = rg.F, rg.SC, rc.Q
lerp = rr.lerp
SHOTS = (("6.1", 3.0), ("6.2", 2.4), ("6.3", 2.2), ("6.4", 3.0), ("7.1", 1.5), ("7.2", 1.8), ("7.2b", 1.5), ("7.3", 2.4),
         ("7.4", 1.8), ("7.5", 1.3))
SEAT = 76                                                  # how much lower he is on the stool
CORNER = (205, F - 235, 2.2)                               # the corner, close: he sits, the frame cuts at his knees
SIT = (150, F + 40)


def _n2(fn, *a, **kw):
    old = n2.LOOK[0]; n2.LOOK[0] = 9
    try:
        return fn(*a, **kw)
    finally:
        n2.LOOK[0] = old


def _blank(col=(0.30, 0.30, 0.32)):
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(s); c.set_source_rgb(*col); c.paint()
    return s, c, Ctx(c, 0)


def _seated(k, tape, look=(0.6, 0.1), face="tired"):
    return b.boxer(k, SIT[0], SIT[1], Q, "b_walk", face, look, tape=tape)


def shot_61(t):
    """He is on the stool. Pam squeezes the sponge over his head, once; then she tapes his brow and presses it down."""
    head = rc.probe(lambda k: _seated(k, False))["head"]
    px_, pf = 262, F - 14

    def client(k):
        _seated(k, t >= 1.9)
        if 0.45 < t < 1.3:                                  # water, down over him
            c = k.c
            c.set_source_rgb(0.90, 0.92, 0.96); c.set_line_width(3); c.set_line_cap(1)
            for i, dx in enumerate((-16, -4, 8, 18)):
                y0 = head[1] - 70 + ((t - 0.45) * 260 + i * 23) % 90
                c.move_to(head[0] + dx, y0); c.line_to(head[0] + dx, y0 + 12); c.stroke()

    def pam(k):
        if t < 1.3:
            sq = 6 * math.sin(lerp(0.0, 1.0, (t - 0.35) / 0.3) * math.pi)
            ca.pam_corner(k, px_, pf, SC, ca.reach(px_, pf, SC, (head[0] + 4, head[1] - 86 + sq), (px_ + 26, pf - 96), stance="work"),
                          "neutral", (-0.9, 0.5), sponge_=True, stance="work")
        else:
            u = lerp(0.0, 1.0, (t - 1.3) / 0.4)
            bx, by = head[0] + 34 * Q, head[1] - 30 * Q
            press = 3 * math.sin((t - 2.2) * 9) if t > 2.2 else 0
            ca.pam_corner(k, px_, pf, SC, ca.reach(px_, pf, SC, (lerp(head[0] + 4, bx + 6, u), lerp(head[1] - 86, by + press, u)),
                                                   (lerp(px_ + 26, bx + 40, u), lerp(pf - 96, by + 16, u)), stance="work"),
                          "knowing" if t > 2.1 else "neutral", (-0.9, 0.4), tape=t < 2.0, stance="work")
    return rg.frame(CORNER, [client, pam], [], near=False, hats=False)


def mom_box(t):
    """Mom from the front, seated in her high chair, her ringed hand flat on the open cash box; the coupe at her elbow."""
    s, c, k = _blank()
    g = cairo.RadialGradient(270, 420, 40, 270, 420, 560)
    g.add_color_stop_rgba(0, 0.86, 0.86, 0.84, 1); g.add_color_stop_rgba(1, 0.30, 0.30, 0.32, 1); c.set_source(g); c.paint()
    cut(k, [(116, 800), (124, 500), (160, 462), (380, 462), (416, 500), (424, 800)], (0.33, 0.31, 0.30), shadow=False, lw=3)
    sc = 1.55
    feet = 400 + 294 * sc + 112
    P = q._body.__globals__["POSES"]
    old = P["q_stand"]
    P["q_stand"] = old[:2] + q.mo.ik(1, 26, -136 + 2 * math.sin(t * 3))
    try:
        o = q.queen(k, 270, feet, sc, "q_stand", "bored", look=(0.2, 0.9))
    finally:
        P["q_stand"] = old
    rect(k, -20, 790, 580, 200, (0.46, 0.44, 0.42), 5, shadow=False, lw=3)
    q.cash_box(k, 300, 880, 2.6)
    q.coupe(k, 190, 850, 1.7)
    hx, hy = o["hands"][1]
    ellipse(k, hx, hy + 14, 34, 22, (0.90, 0.76, 0.66), 10, shadow=False, lw=2.6)             # her hand, flat on the lid
    for i in range(2):
        rect(k, hx - 16 + i * 18, hy + 4, 12, 20, (0.86, 0.87, 0.90), 11 + i, shadow=False, lw=1.6)
    csh.noir(s)
    return s


def shot_62(t):
    """One frame, split in two. Left: the robot in its corner, proud, an oil can tipped over its elbow. Right: Mom at
    her desk, her ringed hand flat on the open cash box."""
    def robot(k):
        x, f = 590, F - 40
        rg.shadow(k, x, f, 40)
        r.robot(k, x, f, SC * r.REL, "r_oil", "proud", side=-1, oil=True)
        r.oil_can(k, x - 58, f - 150 + 3 * math.sin(t * 5), 1.5, -0.7)                           # big, and it drips
        c = k.c; c.set_source_rgb(0.05, 0.05, 0.06)
        for i in range(3):
            y = f - 122 + ((t * 70 + i * 16) % 46)
            c.save(); c.translate(x - 84, y); c.scale(3.2, 5); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
    left = rg.frame((570, F - 150, 2.3), [robot], [], near=False, hats=False)
    s = mom_box(t)
    out = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); oc = cairo.Context(out)
    oc.save(); oc.rectangle(0, 0, 267, 960); oc.clip(); oc.set_source_surface(left, -136, 0); oc.paint(); oc.restore()
    oc.save(); oc.rectangle(273, 0, 267, 960); oc.clip(); oc.set_source_surface(s, 273 - 136, 0); oc.paint(); oc.restore()
    oc.set_source_rgb(0, 0, 0); oc.rectangle(267, 0, 6, 960); oc.fill()
    return out


def _folder(k, x, y, s=1.0, ang=0.0, stamped=False, open_=False):
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    cut(k, [(-40, -28), (40, -28), (40, 28), (-40, 28)], (0.86, 0.80, 0.62), lw=2.2)
    cut(k, [(14, -38), (38, -38), (38, -28), (14, -28)], (0.86, 0.80, 0.62), shadow=False, lw=1.8)
    if stamped:
        c.save(); c.rotate(-0.2); c.set_source_rgb(0.12, 0.12, 0.14); c.set_line_width(2.4); c.rectangle(-34, -13, 68, 26); c.stroke()
        kit.text(k, "CASE", 0, -5, 10, (0.12, 0.12, 0.14), bold=True); kit.text(k, "CLOSED", 0, 6, 10, (0.12, 0.12, 0.14), bold=True)
        c.restore()
    c.restore()


def shot_63(t):
    """Beside him, Don's tweezers lift the folder away. Then, huge, in Don's glass: a woman's photograph."""
    if t < 1.2:
        lift = lerp(0.0, 1.0, (t - 0.45) / 0.5)
        dx_, df = 318, F - 6

        def client(k):
            _seated(k, True, look=(0.2, -0.7))

        def don(k):
            o = _n2(n2.detective, k, dx_, df, SC, "look", "squint", (-0.8, 0.6))
            hx, hy = o["hands"][0]
            fx, fy = 232 + 26 * lift, F - 96 - 58 * lift
            c = k.c
            c.set_source_rgb(0.80, 0.80, 0.84); c.set_line_width(2.4)                              # the tweezers
            c.move_to(hx, hy); c.line_to(fx + 22, fy - 16); c.move_to(hx + 5, hy + 4); c.line_to(fx + 24, fy - 12); c.stroke()
            _folder(k, fx, fy, 0.62, -0.25 + 0.3 * lift)
        return rg.frame((235, F - 215, 2.0), [client, don], [], near=False, hats=False)
    s, c, k = _blank((0.08, 0.08, 0.09))
    grow = lerp(0.86, 1.0, (t - 1.2) / 0.3)
    c.save(); c.translate(270, 440); c.scale(grow, grow); c.translate(-270, -440)
    c.set_source_rgb(0.10, 0.10, 0.11); c.set_line_width(40); c.set_line_cap(1); c.move_to(420, 640); c.line_to(540, 900); c.stroke()   # the handle
    c.save(); c.arc(270, 440, 232, 0, 2 * math.pi); c.clip()
    c.set_source_rgb(0.86, 0.80, 0.62); c.paint()                                                 # the folder's inside
    rect(k, 110, 250, 320, 400, (0.96, 0.96, 0.93), 3, shadow=False, lw=3)                        # her photograph
    c.save(); c.rectangle(112, 252, 316, 396); c.clip()
    c.set_source_rgb(0.62, 0.62, 0.64); c.paint()
    so3.sofia(k, 270, 470 + 272 * 2.3, 2.3, "r_hips", "spotted", (0, 0))
    c.restore(); c.restore()
    c.set_source_rgb(0.10, 0.10, 0.11); c.set_line_width(22); c.arc(270, 440, 236, 0, 2 * math.pi); c.stroke()
    c.set_source_rgba(1, 1, 1, 0.5); c.set_line_width(10); c.arc(270, 440, 200, 3.6, 4.5); c.stroke()
    c.restore()
    csh.noir(s)
    return s


def shot_64(t):
    """The stamp comes down on the folder: CASE CLOSED. Don walks out under the plan; his hat sets it swinging; he does
    not look up. The Client points up after him with a glove. Close: the Referee's one eyebrow goes up."""
    if t < 0.8:
        s, c, k = _blank((0.46, 0.44, 0.42))
        down = lerp(0.0, 1.0, t / 0.3)
        _folder(k, 270, 500, 5.2, -0.06, stamped=t > 0.34)
        if t < 0.55:                                         # the stamp, and the hand on it
            y = 500 - 420 * (1 - down) - (160 * lerp(0.0, 1.0, (t - 0.38) / 0.15) if t > 0.38 else 0)
            rect(k, 190, y - 30, 160, 44, (0.20, 0.20, 0.22), 4, shadow=False, lw=3)
            rect(k, 240, y - 130, 60, 104, (0.36, 0.28, 0.20), 5, shadow=False, lw=3)
        csh.noir(s)
        return s
    if t < 2.4:
        close = t >= 1.5                                    # v2: then closer: his glove up at the plan, Don's back leaving
        u = (t - 0.8) / 1.6
        dx_ = lerp(250.0, 566.0, u); df = lerp(F - 30.0, rg.FAR + 6.0, u); ds = SC * lerp(1.0, 0.78, u)
        under = abs(dx_ - 360) < 40
        sw = 0.10 * math.sin((t - 1.45) * 9) * math.exp(-(t - 1.45) * 1.2) if t > 1.45 else 0.0

        def client(k):
            cx_ = 236 if close else 150
            rg.shadow(k, cx_, F - 30, 44)
            with rc.head_back(-0.2):
                b.boxer(k, cx_, F - 30, Q, b.POSES["b_reach"] if close else rr.WALK, "shock" if close else "hard", (0.8, -0.8), tape=True)

        def pam(k):
            px_ = 150 if close else 232
            rg.shadow(k, px_, F - 14, 34); ca.pam_corner(k, px_, F - 14, SC, "p_stand", "neutral", (0.9, 0.0))

        def ref(k):
            rg.shadow(k, 470, F - 96, 36); ca.referee(k, 470, F - 96, SC * ca.REL_REF, "ref_stand", look=(-0.6, 0), waistcoat=True)

        def robot(k):
            rg.shadow(k, 600, F - 44, 40); r.robot(k, 600, F - 44, SC * r.REL, "r_wait", "proud", side=-1)

        def don(k):
            rg.shadow(k, dx_, df, 34)
            st = math.sin(t * 11)
            _n2(n2.detective_back, k, dx_, df, ds, steps=((-14, 7 * max(st, 0)), (14, 7 * max(-st, 0))))
        order = [ref, don, robot, client, pam] if df < F - 60 else [ref, robot, client, pam, don]
        return rg.frame((360, 1105, 1.3) if close else "R1", order, [], door=True, swing=sw, near=not close, hats=not close)
    def ref(k):
        ca.referee(k, 470, F - 96, SC * ca.REL_REF, "ref_stand", look=((-0.8, 0) if t < 2.75 else (0.9, 0)), brow=2.5 <= t < 2.85,
                   waistcoat=True)
    return rg.frame((470, F - 96 - 340 * SC * ca.REL_REF, 3.6), [ref], [], near=False, hats=False)


def shot_71(t):
    """The card goes past, fast: LAST ROUND. He stands up off the stool, tape on his brow."""
    up = lerp(0.0, 1.0, (t - 0.5) / 0.4)

    def client(k):
        b.boxer(k, SIT[0] + 14 * up, SIT[1] - SEAT * up, Q, "b_walk", "hard", (0.9, 0), tape=True)
    s = rg.frame(CORNER, [client], [], near=False, hats=False)
    c = cairo.Context(s); k = Ctx(c, 0)
    x = 760 - 1500 * (t / 0.9)                                # the card, across the front
    if -260 < x < 800:
        f = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); fc = cairo.Context(f); fk = Ctx(fc, 0)
        fc.set_source_surface(s, 0, 0); fc.paint()
        so3.card(fk, x, 760, 3.0, "LAST ROUND", -0.08)
        ellipse(fk, x + 150, 770, 34, 34, (0.90, 0.76, 0.66), 3, shadow=False, lw=3)
        csh.noir(f)
        c.rectangle(0, 440, 540, 520); c.clip(); c.set_source_surface(f, 0, 0); c.paint()
    return s


LOW = (-9, 6, 62, -2)
HITX = rr.STOP + 60                                        # where he stands when the glove reaches it


def shot_72(t):
    """His glove lands: a dent in its chest. Again: its screen cracks. It rocks back onto one outrigger."""
    h1, h2 = 0.3, 0.9
    cracked, dented = t >= h2, t >= h1
    rock = 0.28 * lerp(0.0, 1.0, (t - h2) / 0.25) if t >= h2 else 0.05 * math.sin((t - h1) * 30) * math.exp(-(t - h1) * 6) if t >= h1 else 0

    def swing(u, pose):                                     # u: 0 wound up .. 1 landed
        return lerp(rr.WIND, pose, u)
    if t < h1:
        pose = swing((t - h1 + 0.1) / 0.1, LOW)
    elif t < h2 - 0.1:
        pose = swing(1 - (t - h1 - 0.1) / 0.25, LOW)
    elif t < h2 + 0.3:
        pose = swing((t - h2 + 0.1) / 0.1, rr.SWING)
    else:
        pose = rr.SWING

    def robot(k):
        c = k.c
        x, f = 466 + 60 * rock, F - 46
        rg.shadow(k, x, f, 40)
        c.save(); c.translate(x + 30, f); c.rotate(rock); c.translate(-x - 30, -f)
        r.robot(k, x, f, SC * r.REL, "r_wait", "furious", side=-1, crack=cracked)
        if dented:                                          # the dent, in its belt plate
            ellipse(k, x - 16, f - 86, 13, 10, (0.10, 0.10, 0.12), 3, shadow=False, lw=2)
        c.restore()

    def client(k):
        rg.shadow(k, HITX, F - 40, 44)
        b.boxer(k, HITX, F - 40, Q, pose, "hard", (0.9, 0.1), tape=True)
        for h, (sx, sy) in ((h1, (438, F - 132)), (h2, (436, F - 196))):
            if h <= t < h + 0.12:
                c = k.c; c.set_source_rgb(1, 1, 1); c.set_line_width(4); c.set_line_cap(1)
                for i in range(8):
                    an = i * math.pi / 4
                    c.move_to(sx + 12 * math.cos(an), sy + 12 * math.sin(an)); c.line_to(sx + 30 * math.cos(an), sy + 30 * math.sin(an)); c.stroke()
    cam = (430, F - 160, 2.3) if t < h2 + 0.3 else (412, 1100, 1.25)
    return rg.frame(cam, [robot, client], [], near=False, hats=False)


def shot_72b(t):
    """The Referee steps between them, a bare palm toward the Client. He stops at once, steps back, lets his gloves
    hang. The robot rights itself."""
    inn = lerp(0.0, 1.0, t / 0.3)
    back = lerp(0.0, 1.0, (t - 0.45) / 0.4)

    def ref(k):
        x = lerp(546.0, 396.0, inn)
        rg.shadow(k, x, F - 60, 36); ca.referee(k, x, F - 60, SC * ca.REL_REF, "ref_break", look=(-0.9, 0), waistcoat=True)

    def robot(k):
        rock = 0.28 * (1 - lerp(0.0, 1.0, (t - 0.6) / 0.4))
        c = k.c; x, f = 466 + 60 * rock, F - 46
        rg.shadow(k, x, f, 40)
        c.save(); c.translate(x + 30, f); c.rotate(rock); c.translate(-x - 30, -f)
        r.robot(k, x, f, SC * r.REL, "r_wait", "furious", side=-1, crack=True)
        ellipse(k, x - 16, f - 86, 13, 10, (0.10, 0.10, 0.12), 3, shadow=False, lw=2)
        c.restore()

    def client(k):
        x = HITX - 80 * back
        rg.shadow(k, x, F - 40, 44)
        b.boxer(k, x, F - 40, Q, lerp(rr.SWING, rr.WALK, (t - 0.3) / 0.25), "hard", (0.9, 0), tape=True)
    return rg.frame((400, 1100, 1.25), [robot, client, ref], [], near=False, hats=False)


def shot_73(t):
    """Low, looking up: under the plan, he reaches. Then his view: the glove gets against the hung end; the paper
    slides over the leather and swings away; the glove closes on nothing."""
    if t < 0.9:
        def client(k):
            rg.shadow(k, 322, F - 40, 44)
            with rc.head_back(-0.26):
                b.boxer(k, 322, F - 40, Q, lerp(rr.WALK, b.POSES["b_reach"], t / 0.5), "dawning", (0.3, -1), tape=True)
        return rg.frame((335, 1130, 1.5), [client], [], near=False, hats=False, swing=0.03 * math.sin(t * 6))
    u = t - 0.9
    if u < 0.35:                                             # both gloves up, and onto the hung end
        return rg.plan_pov(two=True, rise=lerp(300.0, -170.0, u / 0.3))
    if u < 0.85:                                             # he has it, between them: it shakes
        return rg.plan_pov(two=True, rise=-170 + 2 * math.sin(u * 60), squeeze=46)
    v = u - 0.85                                             # it slides up and out; the gloves meet on nothing; down
    up = lerp(0.0, 1.0, v / 0.3)
    return rg.plan_pov(two=True, rise=-170 + (360 * lerp(0.0, 1.0, (v - 0.35) / 0.3) if v > 0.35 else 0), squeeze=46 + 44 * up,
                       lift=150 * up, swing=-0.16 * math.sin(v * 7) * math.exp(-v * 1.5))


def shot_74(t):
    """The cracked screen asks again. Her desk: a card, his gear, turned face down; her finger on the button. The tick."""
    if t < 0.5:
        return rr._insert_screen("ask", crack=True)
    if t >= 1.45:
        return rr._insert_screen("tick", crack=True)
    u = t - 0.5
    s = rr.shot_54(0.6 + u * 1.0)                            # she sits; her arm comes down on the button
    c = cairo.Context(s); k = Ctx(c, 0)
    f = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); fc = cairo.Context(f); fk = Ctx(fc, 0)
    fc.set_source_surface(s, 0, 0); fc.paint()
    flip = lerp(0.0, 1.0, (u - 0.15) / 0.25)                 # the card on the desk: his gear, then its back
    w = 74 * abs(math.cos(flip * math.pi))
    rect(fk, 120 - w / 2, 812, max(w, 4), 104, (0.96, 0.96, 0.93) if flip < 0.5 else (0.20, 0.20, 0.24), 3, shadow=False, lw=2.6)
    if flip < 0.5 and w > 30:
        b.co.gear(fk, 120, 864, 22, col=(0.12, 0.12, 0.14), seed=4)
    elif flip >= 0.5 and w > 30:
        fc.set_source_rgb(0.80, 0.80, 0.84); fc.set_line_width(2); fc.rectangle(120 - w / 2 + 8, 822, w - 16, 84); fc.stroke()
    csh.noir(f)
    c.rectangle(60, 800, 130, 130); c.clip(); c.set_source_surface(f, 0, 0); c.paint()
    return s


def shot_75(t):
    """Close: his face, hard again, the grey glove an inch away, the piston behind it. It lands. White."""
    s, c, k = _blank((0.20, 0.20, 0.22))
    g = cairo.RadialGradient(230, 300, 40, 230, 300, 760)
    g.add_color_stop_rgba(0, 0.80, 0.80, 0.82, 1); g.add_color_stop_rgba(1, 0.14, 0.14, 0.16, 1); c.set_source(g); c.paint()
    hit = 0.75
    sc = 3.3 * b.REL
    b.boxer(k, 210, 520 - b.HY * sc + 20, sc, "b_walk", "hard" if t < hit else "shock", (0.9, 0.0), tape=True)
    gx = lerp(560.0, 392.0, t / 0.45) if t < 0.45 else 392 if t < hit - 0.06 else lerp(392.0, 300.0, (t - hit + 0.06) / 0.06)
    b.robot_glove(k, gx, 500, 3.0)
    csh.noir(s)
    if t >= hit:
        w = lerp(0.0, 1.0, (t - hit) / 0.2)
        c.set_source_rgba(1, 1, 1, w); c.paint()
    return s


FN = {"6.1": shot_61, "6.2": shot_62, "6.3": shot_63, "6.4": shot_64, "7.1": shot_71, "7.2": shot_72, "7.2b": shot_72b,
      "7.3": shot_73, "7.4": shot_74, "7.5": shot_75}


def _use():
    rr.SHOTS, rr.FN = SHOTS, FN


if __name__ == "__main__":
    _use()
    if len(sys.argv) > 2:
        rr.sheets(sys.argv[2], fast=("7.2", "7.5"))
    else:
        rr.render(sys.argv[1] if len(sys.argv) > 1 else "../office-noir-3/on3_beat0607_rough_v2.mp4")
