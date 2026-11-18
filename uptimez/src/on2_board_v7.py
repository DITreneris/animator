"""v7, pinned: builds storyboard v7 from noir2_cast_v10. on2_board.py is current.
OFFICE NOIR 2: the storyboard, v7. Script v2 (17 Nov), noir2_cast with LOOK = 9. on2_board_v6.py to _v1.py are pinned.
v7 is v6 with frame 1.1 made simpler, as Tomas chose ("only the leg and the shoe; cut the squirming"): the knee, the
gown and the shin come out of the dark doorway and the shoe is on the stones. No glove on the pillar, no leaning out.
One film frame (540 x 960) per set-up; 4.1 and 6.7 are two frames each. The dream goes through engine_on's noir pass;
light is one source per set, drawn as hard shapes; the shade on people is put on after the pass.
Writes, in ../office-noir-2: on2_board_v7.png (captioned) and on2_board_mute_v7_N.png (numbered, no captions).
  python3 on2_board.py [folder]"""
import math
import sys
import cairo
import kit
import brand
import engine_on as eng
import noir2_cast_v10 as n
import client_ob as co
import acts_ob as ac
import set_ob as st
import don_v4 as dv
import mom_on as mo
from kit import Ctx, INK, ellipse, rect, cut
from charsheets import corp

n.LOOK[0] = 9
V = "v7"
W, H = 540, 960
NIGHT = (0.13, 0.13, 0.15)
WALLN = (0.19, 0.19, 0.21)
GROUND = (0.27, 0.27, 0.30)
d = n.d


# ---------------------------------------------------------------- light and sets
def pool(cc, x, y, r, a=0.5):
    g = cairo.RadialGradient(x, y, 6, x, y, r)
    g.add_color_stop_rgba(0, 1, 1, 1, a); g.add_color_stop_rgba(1, 1, 1, 1, 0.0); cc.set_source(g); cc.paint()


def lamp(k, lx, ly, floor, w=150):
    """A street lamp: a post with a base and a curved arm, a lantern, its glow, a hard cone of light and a hard pool."""
    cc = k.c
    pool(cc, lx, ly + 4, 150, 0.50)                                                               # the glow round the lantern
    cc.set_source_rgba(1, 1, 1, 0.09); cc.new_path(); cc.move_to(lx - 12, ly + 12); cc.line_to(lx + 12, ly + 12)
    cc.line_to(lx + w, floor + 40); cc.line_to(lx - w, floor + 40); cc.close_path(); cc.fill()
    cc.set_source_rgba(1, 1, 1, 0.20); cc.save(); cc.translate(lx, floor + 46); cc.scale(w * 1.15, 34); cc.new_path()
    cc.arc(0, 0, 1, 0, 2 * math.pi); cc.restore(); cc.fill()
    px = lx + 44
    cc.set_source_rgb(0.04, 0.04, 0.05); cc.set_line_cap(1)
    cc.set_line_width(11); cc.move_to(px, ly - 6); cc.line_to(px, floor + 26); cc.stroke()             # the post
    cc.set_line_width(7); cc.new_path(); cc.move_to(px, ly - 6); cc.curve_to(px, ly - 50, lx + 4, ly - 52, lx, ly - 22); cc.stroke()
    cut(k, [(px - 15, floor + 30), (px + 15, floor + 30), (px + 9, floor - 16), (px - 9, floor - 16)], (0.05, 0.05, 0.06), shadow=False, lw=2)
    rect(k, px - 9, ly + 60, 18, 8, (0.05, 0.05, 0.06), 3, shadow=False, lw=1.5)                      # a collar on the post
    cut(k, [(lx - 20, ly - 12), (lx + 20, ly - 12), (lx + 8, ly - 26), (lx - 8, ly - 26)], (0.05, 0.05, 0.06), shadow=False, lw=2)
    cut(k, [(lx - 16, ly - 12), (lx + 16, ly - 12), (lx + 10, ly + 16), (lx - 10, ly + 16)], (1.0, 0.98, 0.86), shadow=False, lw=2.4)
    cc.set_source_rgb(0.04, 0.04, 0.05); cc.set_line_width(1.6); cc.move_to(lx, ly - 12); cc.line_to(lx, ly + 16); cc.stroke()


def street(k, floor=640, lamp_at=(400, 150), rain=True):
    """The night street: a facade with windows (one lit), a doorway with a step, a drainpipe, a hanging sign with
    nothing written on it, the pavement, the kerb, the road with puddles, a far lamp, and one lamp near."""
    cc = k.c
    cc.set_source_rgb(*NIGHT); cc.paint()
    cc.set_source_rgb(*WALLN); cc.rectangle(-60, 0, 660, floor); cc.fill()
    cc.set_source_rgba(0, 0, 0, 0.16); cc.set_line_width(1.5)                                          # brick courses
    for i in range(1, int(floor / 26) + 1):
        cc.move_to(-60, i * 26); cc.line_to(600, i * 26); cc.stroke()
    for j, (wx, wy) in enumerate(((36, 110), (156, 110), (36, 300), (156, 300))):                   # windows, with frames
        lit = j == 1
        cc.set_source_rgb(*((0.66, 0.65, 0.58) if lit else (0.09, 0.09, 0.11))); cc.rectangle(wx, wy, 78, 118); cc.fill()
        cc.set_source_rgb(0.34, 0.34, 0.37); cc.set_line_width(4); cc.rectangle(wx, wy, 78, 118); cc.stroke()
        cc.set_line_width(2.4); cc.move_to(wx + 39, wy); cc.line_to(wx + 39, wy + 118); cc.move_to(wx, wy + 54); cc.line_to(wx + 78, wy + 54); cc.stroke()
        cc.set_source_rgb(0.30, 0.30, 0.33); cc.rectangle(wx - 6, wy + 118, 90, 9); cc.fill()            # the sill
        if lit:                                                                                    # a blind, half down
            cc.set_source_rgb(0.42, 0.41, 0.37); cc.rectangle(wx + 3, wy + 3, 72, 40); cc.fill()
    if floor > 520:
        cc.set_source_rgb(0.07, 0.07, 0.08); cc.rectangle(280, floor - 190, 96, 190); cc.fill()           # a doorway, and its step
        cc.set_source_rgb(0.34, 0.34, 0.37); cc.set_line_width(4); cc.rectangle(280, floor - 190, 96, 190); cc.stroke()
        ellipse(k, 362, floor - 92, 4.5, 4.5, (0.70, 0.70, 0.72), 4, shadow=False, lw=1.4)
        cc.set_source_rgb(0.32, 0.32, 0.35); cc.rectangle(268, floor - 10, 120, 10); cc.fill()
    cc.set_source_rgb(0.08, 0.08, 0.09); cc.set_line_width(9); cc.move_to(258, 0); cc.line_to(258, floor); cc.stroke()   # a drainpipe
    cc.set_source_rgb(0.30, 0.30, 0.33); cc.set_line_width(3)
    for yy in (80, 260, 440):
        if yy < floor:
            cc.move_to(250, yy); cc.line_to(266, yy); cc.stroke()
    cc.set_source_rgb(0.08, 0.08, 0.09); cc.set_line_width(4); cc.move_to(258, 236); cc.line_to(212, 236); cc.stroke()       # a sign's bracket
    rect(k, 206, 240, 44, 30, (0.26, 0.26, 0.29), 6, shadow=False, lw=2)
    cc.set_source_rgb(0.33, 0.33, 0.36); cc.rectangle(-60, floor, 660, 30); cc.fill()                 # the pavement and its kerb
    cc.set_source_rgb(0.12, 0.12, 0.14); cc.set_line_width(4); cc.move_to(-60, floor + 30); cc.line_to(600, floor + 30); cc.stroke()
    cc.set_source_rgb(0.24, 0.24, 0.27); cc.set_line_width(2)
    for i in range(12):
        cc.move_to(-40 + i * 56, floor); cc.line_to(-40 + i * 56, floor + 30); cc.stroke()
    cc.set_source_rgb(*GROUND); cc.rectangle(-60, floor + 32, 660, H - floor + 60); cc.fill()         # the road, wet
    cc.set_source_rgb(0.20, 0.20, 0.23); cc.set_line_width(2)
    for i in range(1, 7):
        yy = floor + 32 + i * i * 8; cc.move_to(-60, yy); cc.line_to(600, yy); cc.stroke()
    for (ex, ey, rw, rh) in ((120, floor + 150, 92, 16), (430, floor + 230, 120, 20)):               # puddles
        if ey < H - 10:
            cc.set_source_rgba(1, 1, 1, 0.13); cc.save(); cc.translate(ex, ey); cc.scale(rw, rh); cc.new_path(); cc.arc(0, 0, 1, 0, 2 * math.pi)
            cc.restore(); cc.fill()
            cc.set_source_rgba(1, 1, 1, 0.30); cc.set_line_width(3); cc.move_to(ex - rw * 0.4, ey - 3); cc.line_to(ex + rw * 0.3, ey - 3); cc.stroke()
    pool(cc, 20, 70, 70, 0.45)                                                                     # a lamp far down the street
    cc.set_source_rgb(0.05, 0.05, 0.06); cc.set_line_width(4); cc.move_to(28, 76); cc.line_to(28, min(floor, 300)); cc.stroke()
    ellipse(k, 20, 70, 6, 5, (1.0, 0.98, 0.86), 7, shadow=False, lw=1.4)
    if lamp_at:
        lamp(k, lamp_at[0], lamp_at[1], floor)
    if rain:
        cc.set_source_rgba(1, 1, 1, 0.16); cc.set_line_width(1.6)
        for i in range(26):
            rx, ry = (i * 97) % 560 - 10, (i * 173) % 900
            cc.move_to(rx, ry); cc.line_to(rx - 9, ry + 34); cc.stroke()


def bar_room(k, counter=None):
    """The cabaret: dark, lit from the bar's back wall. counter: the y of the bar top, or None."""
    cc = k.c
    cc.set_source_rgb(0.12, 0.12, 0.14); cc.paint()
    cc.set_source_rgb(0.34, 0.33, 0.31); cc.rectangle(-20, 150, 600, 250); cc.fill()                 # the lit back wall
    cc.set_source_rgb(0.10, 0.10, 0.12)
    for i in range(11):                                                                           # bottles against it
        bx = 20 + i * 50; bh = 60 + (i * 37) % 40
        cc.rectangle(bx, 400 - bh, 16, bh); cc.fill(); cc.rectangle(bx + 5, 400 - bh - 18, 6, 18); cc.fill()
    cc.set_source_rgb(0.08, 0.08, 0.09); cc.rectangle(-20, 396, 600, 12); cc.fill()
    if counter is not None:
        cc.set_source_rgb(0.24, 0.21, 0.18); cc.rectangle(-20, counter, 600, H - counter + 20); cc.fill()
        cc.set_source_rgb(0.60, 0.56, 0.50); cc.rectangle(-20, counter, 600, 9); cc.fill()


def office(k, lamp_on=False, desk=None, frame=True):
    """The UptimeZ office at night: light through the blinds, OUR FIRST CLIENT on the wall."""
    cc = k.c
    cc.set_source_rgb(0.15, 0.15, 0.17); cc.paint()
    cc.save(); cc.rotate(-0.10)
    for i in range(8):                                                                            # hard bars of light
        cc.set_source_rgba(1, 1, 1, 0.15); cc.rectangle(-60, 110 + i * 46, 430, 20); cc.fill()
    cc.restore()
    if frame:
        photo(k, 420, 250, 1.25)
    if desk is not None:
        cc.set_source_rgb(0.11, 0.10, 0.10); cc.rectangle(desk[0], desk[1], desk[2], H - desk[1] + 20); cc.fill()
        cc.set_source_rgb(0.46, 0.42, 0.38); cc.rectangle(desk[0], desk[1], desk[2], 11); cc.fill()
    if lamp_on:
        lx, ly = lamp_on
        cc.set_source_rgba(1, 1, 1, 0.16); cc.new_path(); cc.move_to(lx - 16, ly); cc.line_to(lx + 16, ly)
        cc.line_to(lx + 190, ly + 250); cc.line_to(lx - 190, ly + 250); cc.close_path(); cc.fill()
        cut(k, [(lx - 30, ly), (lx + 30, ly), (lx + 16, ly - 30), (lx - 16, ly - 30)], (0.30, 0.30, 0.33), shadow=False, lw=2)


def photo(k, x, y, s):
    """OUR FIRST CLIENT, with his photograph in it."""
    cc = k.c
    st.first_client(k, x, y, s)
    cc.save(); cc.rectangle(x - 32 * s, y - 42 * s, 64 * s, 84 * s); cc.clip()
    cc.set_source_rgb(0.74, 0.84, 0.94); cc.paint()
    co.client(k, x, y - 6 * s - co.HY * 0.44 * s, 0.44 * s, "open", "puzzled", look=(0, 0), roll=False, badge=False)
    cc.restore()


def party(k, floor=760):
    cc = k.c
    cc.set_source_rgb(0.93, 0.90, 0.82); cc.paint()
    cc.set_source_rgb(0.72, 0.63, 0.50); cc.rectangle(-20, floor, 600, H - floor + 20); cc.fill()
    cc.set_source_rgb(*INK); cc.set_line_width(2); cc.move_to(-20, floor); cc.line_to(560, floor); cc.stroke()
    for i, col in enumerate(((0.16, 0.62, 0.86), (0.98, 0.84, 0.25), (0.30, 0.72, 0.45), (0.95, 0.55, 0.20))):   # streamers; never red
        cc.set_source_rgb(*col); cc.set_line_width(7); cc.set_line_cap(1)
        x0 = -20 + i * 150
        cc.move_to(x0, 0); cc.curve_to(x0 + 40, 70, x0 + 110, 30, x0 + 150, 110 - (i % 2) * 50); cc.stroke()
    st.confetti(k, 10, 20, 530, floor - 40, n=26, seed=11, s=1.4)


def shade(cc, side=1, a=0.50, x0=None, x1=None):
    a *= 0.65
    """After the pass: the dark side of the frame. side=1 darkens screen right, -1 screen left."""
    x0 = (W * 0.45 if side > 0 else W * 0.55) if x0 is None else x0
    x1 = (W if side > 0 else 0) if x1 is None else x1
    g = cairo.LinearGradient(x0, 0, x1, 0)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.0); g.add_color_stop_rgba(1, 0, 0, 0, a); cc.set_source(g); cc.paint()


def vignette(cc, a=0.24):
    g = cairo.RadialGradient(W / 2, H / 2, H * 0.30, W / 2, H / 2, H * 0.72)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.0); g.add_color_stop_rgba(1, 0, 0, 0, a); cc.set_source(g); cc.paint()


def arm_in(k, x0, y0, x1, y1, w=58):
    """The Shadow's arm from off screen to his lit hand at (x1, y1): a black sleeve, a white cuff, the watch, fingers."""
    n._seg(k, x0, y0, x1, y1, w, w * 0.78, n.BLACK)
    g = math.atan2(y1 - y0, x1 - x0)
    wx, wy = x1 - math.cos(g) * 30, y1 - math.sin(g) * 30
    cx, cy = x1 - math.cos(g) * 44, y1 - math.sin(g) * 44
    n._seg(k, cx, cy, x1 - math.cos(g) * 20, y1 - math.sin(g) * 20, w * 0.84, w * 0.80, (0.97, 0.97, 0.95), 2.6)
    ellipse(k, x1, y1, 33, 29, co.SKIN, 403, shadow=False, lw=3.2)
    for i in range(3):
        fx, fy = x1 + math.cos(g) * 26 - math.sin(g) * (i - 1) * 15, y1 + math.sin(g) * 26 + math.cos(g) * (i - 1) * 15
        ellipse(k, fx, fy, 15, 7.5, co.SKIN, 406 + i, shadow=False, lw=2.4)
    px, py = -math.sin(g), math.cos(g)
    ellipse(k, wx - px * 22, wy - py * 22, 15, 15, (0.20, 0.20, 0.22), 404, shadow=False, lw=2.6)
    ellipse(k, wx - px * 22, wy - py * 22, 8, 8, (0.92, 0.92, 0.88), 405, shadow=False, lw=1.4)


def red_shoe(k, x, y, s, flip=1):
    """Her shoe and ankle from the side, the hem above it. (x, y) is the sole under the heel."""
    cc = k.c
    cc.save(); cc.translate(x, y); cc.scale(s * flip, s)
    cut(k, [(-7, -46), (6, -46), (5, -12), (-5, -12)], n.so.SKIN, shadow=False, lw=1.8)
    cut(k, [(-8, -14), (6, -14), (20, 0), (5, 0), (-1, -6), (-4, 0), (-8, 0)], n.KEY, shadow=False, lw=1.8)
    cut(k, [(-22, -84), (20, -84), (13, -40), (-13, -40)], n.KEY, shadow=False, lw=2)
    cc.restore()


def step_out(k, foot=(206, 716), knee=(216, 572), s=2.3, hand=1.0, rise=0.0, door=(155, 431, 150, 205)):
    """v6: she gets out of the cab drawn by n.taxi(k, 150, 716, 2.5, door=1). Screen co-ordinates. foot: the sole under
    her heel; knee: her knee, just inside the doorway. Everything above the sill is cut off by the doorway itself, so
    the leg comes out of the dark and is never in front of the car's side. hand 0..1: her glove on the pillar.
    rise 0..1: she leans out after her foot."""
    cc = k.c
    fx, fy = foot; kx, ky = knee
    dx, dy, dw, dh = door
    cc.save()
    cc.new_path(); cc.rectangle(dx, dy, dw, dh); cc.rectangle(-20, dy + dh, 600, 400); cc.clip()
    if hand > 0:                                                                # her arm, from the pillar back into the dark
        ex, ey = kx + 62, ky - 22 - 76 * rise                                   # it ends in her lap, so it never ends in mid-air
        for wdt, col in ((21, INK), (16, n.KEY)):
            cc.set_source_rgb(*col); cc.set_line_width(wdt); cc.set_line_cap(1)
            cc.move_to(dx - 2, 512); cc.curve_to(dx + 34, 498, ex - 34, ey - 34, ex, ey); cc.stroke()
    up = 96 * rise
    cut(k, [(dx + dw + 8, ky - 30 - up), (kx + 34, ky - 32 - up * 0.8), (kx + 10, ky - 32), (kx - 16, ky - 18), (kx - 20, ky + 2), (kx - 2, ky + 18),
            (fx + 22, fy - 34), (fx + 30, fy - 12), (fx + 84, fy - 2), (fx + 92, fy - 40), (kx + 78, ky + 16), (dx + dw + 8, ky + 18)],
        n.KEY, shadow=False, lw=2)                                               # the gown: over her lap, over the knee, down behind the shin
    cc.set_source_rgb(*n.GOWN_SHADE); cc.set_line_width(1.6); cc.set_line_cap(1)
    cc.move_to(kx + 22, ky + 14); cc.curve_to(kx + 30, ky + 60, fx + 44, fy - 70, fx + 50, fy - 14); cc.stroke()
    cc.move_to(kx + 56, ky + 14); cc.curve_to(kx + 62, ky + 60, fx + 70, fy - 70, fx + 72, fy - 10); cc.stroke()
    cc.move_to(kx + 4, ky - 6); cc.curve_to(kx + 30, ky + 2, kx + 60, ky + 2, dx + dw, ky - 4); cc.stroke()
    cut(k, [(kx - 15, ky + 2), (kx + 5, ky + 12), (fx + 6 * s / 2.3, fy - 12 * s), (fx - 7 * s / 2.3, fy - 12 * s)], n.so.SKIN, shadow=False, lw=1.8)   # the shin, in the slit
    cc.save(); cc.translate(fx, fy); cc.scale(-s, s)                             # the shoe, toe to screen left
    cut(k, [(-8, -14), (6, -14), (20, 0), (5, 0), (-1, -6), (-4, 0), (-8, 0)], n.KEY, shadow=False, lw=1.8)
    cc.restore()
    cc.restore()
    if hand > 0:                                                                # four fingers round the pillar, outside the doorway
        for i in range(4):
            ellipse(k, dx - 5, 500 + i * 8.5, 8.5, 4.6, n.KEY, 870 + i, shadow=False, lw=1.5)


def black_fig(k, draw):
    cc = k.c
    cc.push_group(); o = draw(); fig = cc.pop_group()
    cc.set_source_rgb(*n.BLACK); cc.mask(fig)
    return o


def hat_at(k, x, y, s, tilt=-0.1):
    n.shadow_hat(k, x, y, s, tilt, 405)


# ---------------------------------------------------------------- beat 01: the taxi
def s1_1(k):
    street(k, 668, (440, 150))
    n.taxi(k, 150, 716, 2.5, door=1.0)
    step_out(k, hand=0.0)


def s1_2(k):
    street(k, 690, (430, 150))
    n.taxi(k, 40, 730, 1.5, door=0.0)
    n.star(k, 350, 800, 1.9, "g_pose", "interested", (0.5, -0.3), sparkle=1.0)


# ---------------------------------------------------------------- beat 02: the street
def s2_1(k):
    cc = k.c
    street(k, 600, (440, 140))
    cc.set_source_rgb(*n.BLACK)                                                                    # his shadow, long, on the stones
    cc.new_path(); cc.move_to(-20, 960); cc.line_to(120, 760); cc.line_to(200, 760); cc.line_to(190, 960); cc.close_path(); cc.fill()
    cc.save(); cc.translate(160, 752); cc.scale(84, 15); cc.new_path(); cc.arc(0, 0, 1, 0, 2 * math.pi); cc.restore(); cc.fill()
    cc.new_path(); cc.move_to(118, 752); cc.line_to(128, 700); cc.line_to(152, 712); cc.line_to(170, 696); cc.line_to(196, 708); cc.line_to(204, 752)
    cc.close_path(); cc.fill()
    n.star_back(k, 340, 800, 1.9, step=0.2)


def s2_2(k):
    cc = k.c
    cc.set_source_rgb(0.11, 0.11, 0.13); cc.paint()
    pool(cc, 300, 200, 420, 0.22)
    n._seg(k, 330, 1000, 290, 760, 110, 96, n.KEY, 3.4)                                              # her glove
    n.compact2(k, 270, 470, 9.0, 0.06, hat=True)
    ellipse(k, 286, 760, 58, 52, n.KEY, 363, shadow=False, lw=3.4)


def s2_3(k):
    cc = k.c
    cc.set_source_rgb(0.13, 0.13, 0.15); cc.paint()
    pool(cc, 380, 160, 420, 0.30)
    n.star(k, 240, 1270, 3.4, "g_mirror", "real", (0.9, -0.1), wrap=False, mirror=True)


def s2_4(k):
    street(k, 720, None, rain=False)
    pool(k.c, 300, 120, 520, 0.38)
    n.shadow(k, 20, 1180, 2.5, "open", lit_hand=None, look_down=1.0)
    o = n.star(k, 340, 1060, 2.6, "g_stand", "caught", (-1.0, 0.9), wrap=False)
    lx, ly = o["hands"][0]
    arm_in(k, -40, 470, lx - 22, ly - 52)


def s2_5(k):
    cc = k.c
    cc.set_source_rgb(*GROUND); cc.paint()
    cc.set_source_rgb(0.20, 0.20, 0.23); cc.set_line_width(3)
    for i in range(7):
        cc.move_to(-20, 140 + i * 140); cc.line_to(560, 110 + i * 140); cc.stroke()
    cc.set_source_rgba(1, 1, 1, 0.16); cc.save(); cc.translate(250, 600); cc.scale(260, 200); cc.new_path(); cc.arc(0, 0, 1, 0, 2 * math.pi)
    cc.restore(); cc.fill()
    n.powder_puff(k, 220, 640, 5.0)
    red_shoe(k, 420, 560, 3.6)
    red_shoe(k, 500, 380, 3.0)
    n.footprints(k, 300, 700, 4.2, n=1, step=30)


def s2_6(k):
    street(k, 580, (440, 140))
    cc = k.c
    cc.set_source_rgba(1, 1, 1, 0.26); cc.save(); cc.translate(150, 800); cc.scale(200, 150); cc.new_path(); cc.arc(0, 0, 1, 0, 2 * math.pi)
    cc.restore(); cc.fill()
    n.footprints(k, 250, 690, 2.2, n=3, step=30)
    n.star(k, 410, 660, 1.15, "g_run3", "caught", (-0.9, 0.0), lean=7, lag=(-14, -4), wrap=False, run=True)
    arm_in(k, -40, 560, 130, 640, 60)                                                              # his hand, holding her wrap up
    cc.save(); cc.translate(150, 650); cc.scale(2.4, 2.4)
    n._cloth(cc, [("M", -5, 0), ("C", -2, -3, 2, -3, 5, 0), ("C", 20, 14, 26, 50, 20, 88), ("C", 18, 104, 12, 114, 8, 122),
                  ("C", 4, 110, 0, 100, -4, 104), ("C", -8, 110, -12, 116, -16, 124), ("C", -22, 104, -26, 50, -5, 0)])
    n._curve(cc, (4, 6, 16, 22, 20, 56, 14, 96), n.WRAP_PALE, 1.6)
    cc.restore()


# ---------------------------------------------------------------- beat 03: Pam and Don
def s3_1(k):
    street(k, 600, (420, 140))
    n.footprints(k, 250, 840, 2.6, n=3, step=30)
    n.star(k, 590, 900, 2.0, "g_run3", "caught", (-0.9, 0.0), lean=7, lag=(-14, -4), wrap=False, run=True)
    n.sweeper(k, 170, 930, 2.2, "lean", "neutral", (1.0, 0.1))


def s3_2(k):
    street(k, 540, (300, 130))
    n.detective(k, 420, 700, 1.12, "look", "squint", (0.6, 0.8), wrap=True)
    n.footprints(k, 300, 900, 2.6, n=3, step=30)
    n.sweeper(k, 190, 930, 2.25, "sweep", "neutral", (1.0, -0.2))


def s3_3(k):
    cc = k.c
    cc.set_source_rgb(0.09, 0.09, 0.10); cc.paint()
    n.glass_handle(k, 250, 440, 220, 0.6)
    n.glass_view(k, 250, 440, 220, "prints")


def s3_4(k):
    street(k, 580, (270, 130))
    n.sweeper(k, 150, 930, 2.0, "lean", "neutral", (0.2, -1.0))
    n.dustpan(k, 280, 900, 2.0, full=True)
    n.detective(k, 410, 930, 1.75, "look", "squint", (-1.0, -0.1), wrap=True)


# ---------------------------------------------------------------- beat 04: the door
def bar_door(k, floor=760):
    cc = k.c
    street(k, floor, None)
    cc.set_source_rgb(0.72, 0.71, 0.66); cc.rectangle(300, 110, 300, floor - 110); cc.fill()         # the door, lit from inside
    cc.set_source_rgb(*INK); cc.set_line_width(5); cc.rectangle(300, 110, 300, floor - 110); cc.stroke()
    cc.set_source_rgba(1, 1, 1, 0.20); cc.new_path(); cc.move_to(300, floor); cc.line_to(600, floor); cc.line_to(600, 960); cc.line_to(120, 960)
    cc.close_path(); cc.fill()                                                                    # its light, hard, on the ground


def coin(k, x, y, r):
    """Her coin, big enough to be the subject: a rim, and a 1."""
    cc = k.c
    n.big_coin(k, x, y, r)
    cc.set_source_rgb(*INK); cc.select_font_face("Inter", 0, 1); cc.set_font_size(r * 1.15)
    e = cc.text_extents("1"); cc.move_to(x - e.width / 2 - e.x_bearing, y + r * 0.40); cc.show_text("1")


def s4_1a(k):
    """Closer: her glove opens over the cup, and the coin is in the air between them."""
    cc = k.c
    bar_door(k)
    o = n.rn.robot_noir(k, 340, 1020, 2.2, "stand", "eager", (-0.8, -0.3), cap=False)
    (lx, ly), (rx, ry) = o["hands"]
    hx, hy = o["head"]
    n.battery_card(k, 336, hy + 150 * 2.2, 2.0, 0.05)
    n.cup(k, lx, ly - 34, 3.6)
    ellipse(k, lx, ly, 18, 18, (0.20, 0.20, 0.22), 23, shadow=False, lw=3)
    n._seg(k, -60, 300, 110, 420, 96, 84, n.KEY, 3.2)                                                # her glove, open, above it
    ellipse(k, 118, 428, 48, 44, n.KEY, 336, shadow=False, lw=3.2)
    for i, a in enumerate((0.25, 0.65, 1.05, 1.45)):                                               # fingers, spread: she has let go
        n._seg(k, 118 + math.cos(a) * 34, 428 + math.sin(a) * 34, 118 + math.cos(a) * 78, 428 + math.sin(a) * 78, 20, 16, n.KEY, 2.6)
    coin(k, lx + 4, ly - 190, 34)
    cc.set_source_rgb(1, 1, 1); cc.set_line_width(4); cc.set_line_cap(1)
    for dx in (-22, 0, 22):
        cc.move_to(lx + 4 + dx, ly - 240); cc.line_to(lx + 4 + dx, ly - (290 if dx else 310)); cc.stroke()


def s4_1b(k):
    cc = k.c
    bar_door(k)
    n.star(k, 468, 1010, 2.2, "g_down", "appraise", (-1.0, 0.5), wrap=False, bag=False)
    o = n.coin_steps(k, 56, 800, 1.18, 2)
    bx, by = o["claw"]
    coin(k, bx + 14, by, 30)                                                                      # the same coin, back, and large
    cc.set_source_rgb(*INK); cc.set_line_width(2.4); cc.move_to(bx + 14, by + 30); cc.line_to(bx + 18, by + 52); cc.stroke()
    cc.save(); cc.translate(bx + 18, by + 52); cc.rotate(0.05); cc.scale(1.25, 1.25)
    cut(k, [(-44, 8), (-36, 0), (36, 0), (44, 8), (44, 36), (-44, 36)], (0.98, 0.95, 0.80), shadow=False, lw=1.8)
    cc.set_source_rgb(*INK); cc.select_font_face("Inter", 0, 1); cc.set_font_size(11.5)
    for i, t in enumerate(("PENDING", "APPROVAL")):
        e = cc.text_extents(t); cc.move_to(-e.width / 2 - e.x_bearing, 16 + i * 13); cc.show_text(t)
    cc.restore()


def s4_2(k):
    cc = k.c
    cc.set_source_rgb(0.12, 0.12, 0.14); cc.paint()
    pool(cc, 300, 300, 460, 0.26)
    for col, w in ((INK, 62), (n.SILVER, 44)):                                                     # the claw's arm
        cc.set_source_rgb(*col); cc.set_line_width(w); cc.set_line_cap(1); cc.move_to(-40, 330); cc.line_to(110, 330); cc.stroke()
    for sy in (-1, 1):
        cc.set_source_rgb(*INK); cc.set_line_width(26); cc.move_to(110, 330); cc.line_to(180, 330 + sy * 86); cc.stroke()
        cc.set_source_rgb(*n.SILVER); cc.set_line_width(15); cc.move_to(110, 330); cc.line_to(180, 330 + sy * 86); cc.stroke()
    coin(k, 250, 330, 92)                                                                         # the coin is the subject
    cc.save(); cc.translate(250, 424); cc.scale(3.2, 3.2)
    cc.set_source_rgb(*INK); cc.set_line_width(1.4); cc.move_to(0, 0); cc.line_to(2, 12); cc.stroke()
    cc.translate(2, 12); cc.rotate(0.05)
    cut(k, [(-44, 8), (-36, 0), (36, 0), (44, 8), (44, 36), (-44, 36)], (0.98, 0.95, 0.80), shadow=False, lw=1.2)
    cc.set_source_rgb(*INK); cc.select_font_face("Inter", 0, 1); cc.set_font_size(11.5)
    for i, t in enumerate(("PENDING", "APPROVAL")):
        e = cc.text_extents(t); cc.move_to(-e.width / 2 - e.x_bearing, 16 + i * 13); cc.show_text(t)
    cc.restore()
    n._seg(k, 600, 150, 420, 250, 100, 88, n.KEY, 3.4)                                               # her glove, a finger and thumb on the coin
    ellipse(k, 410, 256, 50, 46, n.KEY, 336, shadow=False, lw=3.2)
    for (fx, fy) in ((346, 262), (352, 312)):
        ellipse(k, fx, fy, 40, 17, n.KEY, 337 + fy, shadow=False, lw=3)


# ---------------------------------------------------------------- beat 05: the bar
def s5_1(k):
    cc = k.c
    bar_room(k)
    n.star(k, 270, 1080, 2.4, "g_stand", "interested", (0.0, -0.2), wrap=False)
    n.rich_hand(k, 110, 520, 1.9, 0.18, "money")
    n.rich_hand(k, 90, 800, 1.9, -0.12, "coupe")
    n.rich_hand(k, 440, 470, 1.9, 0.10, "coupe", flip=-1)
    n.rich_hand(k, 450, 760, 1.9, -0.16, "money", flip=-1)


def s5_2(k):
    cc = k.c
    bar_room(k)
    # Don, across the room, a hand over his eyes, searching the wrong way
    o = n.detective(k, 400, 760, 1.5, d.dm.ik(-1, -34, d.HY - 6) + d.dm.ik(1, 62, d.BT + 40), "squint", (1.0, -0.1))
    # she is low, behind two fans of money: one eye out, on him
    o = n.star(k, 170, 1250, 2.7, "g_fan", "caught", (1.0, -0.3), wrap=False, bag=False)
    hx, hy = o["head"]
    n.money(k, hx - 70, hy + 150, 4.4, -0.35, 5, 711)                                               # a stranger's fan, over half her face
    n.rich_hand(k, hx - 96, hy + 170, 2.1, 0.5, "money")
    n.rich_hand(k, 520, 930, 1.9, -0.2, "coupe", flip=-1)


def s5_3(k):
    bar_room(k)
    n.bartender(k, 390, 700, 1.55, brow=True, look=(-0.8, 0.2))
    cc = k.c
    cc.set_source_rgb(0.24, 0.21, 0.18); cc.rectangle(-20, 640, 600, 340); cc.fill()
    cc.set_source_rgb(0.60, 0.56, 0.50); cc.rectangle(-20, 640, 600, 9); cc.fill()
    n.coupe(k, 280, 640, 2.0)
    n.star(k, 130, 1060, 2.2, "g_down", "interested", (0.8, -0.1), wrap=False, bag=False)


def bar_top(k):
    cc = k.c
    cc.set_source_rgb(0.22, 0.19, 0.16); cc.paint()
    cc.set_source_rgb(0.28, 0.25, 0.21); cc.set_line_width(3)
    for i in range(6):
        cc.move_to(-20, 90 + i * 170); cc.line_to(560, 70 + i * 170); cc.stroke()
    pool(cc, 300, 400, 420, 0.22)


def s5_4(k):
    bar_top(k)
    n.napkin2(k, 320, 500, 3.0, ang=-0.05)
    arm_in(k, -40, 200, 150, 400, 90)
    n.coupe(k, 440, 900, 2.4)


def s5_5(k):
    cc = k.c
    bar_room(k)
    n.star(k, 280, 1010, 3.0, "g_down", "sideeye", (-1.0, 0.1), wrap=False, bag=False)
    cc.set_source_rgb(0.22, 0.19, 0.16); cc.rectangle(-20, 560, 600, 420); cc.fill()
    cc.set_source_rgb(0.60, 0.56, 0.50); cc.rectangle(-20, 560, 600, 9); cc.fill()
    n.napkin2(k, 230, 740, 2.5, ang=-0.05)
    n._seg(k, 600, 1000, 420, 850, 92, 80, n.KEY, 3.2)
    n.hand(k, 420, 850, 5.0, -1.02, 0.0)


def s5_6(k):
    cc = k.c
    bar_top(k)
    n.napkin2(k, 250, 480, 3.3, back=True, ang=0.04)
    n._seg(k, 600, 900, 440, 720, 96, 84, n.KEY, 3.2)
    ellipse(k, 436, 716, 50, 46, n.KEY, 336, shadow=False, lw=3.2)
    cc.save(); cc.translate(404, 680); cc.rotate(-0.75); cc.scale(4.6, 4.6)                         # her lipstick
    rect(k, -3.4, -2, 6.8, 15, (0.12, 0.12, 0.14), 331, shadow=False, lw=1.0)
    cut(k, [(-2.6, -2), (-2.6, -9), (2.6, -12), (2.6, -2)], n.KEY, shadow=False, lw=0.9)
    cc.restore()


def s5_7(k):
    """From above: her answer alone on the bar. Nobody takes it. Her glove waits; the stool across from her is empty."""
    cc = k.c
    bar_top(k)
    cc.set_source_rgb(0.10, 0.10, 0.11); cc.rectangle(-20, -20, 600, 190); cc.fill()                 # the floor beyond the bar
    cc.set_source_rgb(0.60, 0.56, 0.50); cc.rectangle(-20, 166, 600, 9); cc.fill()                  # the bar's far edge
    ellipse(k, 150, 70, 88, 60, (0.34, 0.30, 0.27), 51, lw=3.4)                                     # an empty stool
    ellipse(k, 150, 62, 70, 44, (0.44, 0.39, 0.35), 52, shadow=False, lw=2.4)
    n.napkin2(k, 270, 520, 3.0, back=True, ang=0.04)
    n._seg(k, 620, 960, 500, 850, 96, 84, n.KEY, 3.2)                                                # her glove, drawn back, waiting
    ellipse(k, 496, 846, 50, 46, n.KEY, 336, shadow=False, lw=3.2)
    n.coupe(k, 90, 900, 2.4)


def s5_8(k):
    cc = k.c
    bar_room(k)
    cc.set_source_rgb(0.05, 0.05, 0.06); cc.rectangle(-20, 60, 250, 920); cc.fill()                 # the door, open on the night
    cc.set_source_rgb(0.40, 0.38, 0.34); cc.set_line_width(8); cc.rectangle(-20, 60, 250, 920); cc.stroke()
    n.star(k, 200, 1090, 2.6, "g_down", "sideeye", (1.0, 0.0), wrap=False, bag=False)


def s5_9(k):
    cc = k.c
    bar_room(k)
    n.bartender(k, 496, 560, 0.80, brow=True, look=(-0.8, 0.3))
    cc.set_source_rgb(0.24, 0.21, 0.18); cc.rectangle(250, 500, 330, 480); cc.fill()
    cc.set_source_rgb(0.60, 0.56, 0.50); cc.rectangle(250, 500, 330, 9); cc.fill()
    o = n.detective(k, 372, 640, 1.0, "up", "squint", (-0.9, 0.1), napkin_in_band=True)
    hx, hy = o["head"]
    n.glass_handle(k, hx - 30, hy + 20, 92, 0.5)
    n.glass_view(k, hx - 30, hy + 20, 92, "eye")
    n.star(k, 120, 1150, 2.6, "g_stand", "caught", (1.0, 0.0), wrap=False, bag=False)


def s5_10(k):
    cc = k.c
    bar_room(k)
    n.bartender(k, 440, 690, 1.3, brow=True, look=(-0.9, 0.2))
    cc.set_source_rgb(0.24, 0.21, 0.18); cc.rectangle(-20, 640, 600, 340); cc.fill()
    cc.set_source_rgb(0.60, 0.56, 0.50); cc.rectangle(-20, 640, 600, 9); cc.fill()
    o = n.detective(k, 210, 1010, 2.1, "proud", "almost", (0.3, -0.2), napkin_in_band=True)
    lx, ly = o["hands"][0]
    n.coupe(k, lx - 4, ly + 10, 1.9)
    ellipse(k, lx, ly - 30, 20, 20, d.SKIN, 478, shadow=False, lw=3)


# ---------------------------------------------------------------- beat 06: the office and the trap
def s6_1(k):
    cc = k.c
    office(k)
    cc.set_source_rgb(0.08, 0.08, 0.09); cc.rectangle(40, 120, 250, 760); cc.fill()                 # the door she shut
    cc.set_source_rgb(0.34, 0.33, 0.31); cc.set_line_width(6); cc.rectangle(40, 120, 250, 760); cc.stroke()
    ellipse(k, 262, 520, 9, 9, n.SILVER, 9, shadow=False, lw=2)
    cc.set_source_rgb(0.24, 0.24, 0.27); cc.rectangle(-20, 880, 600, 100); cc.fill()
    n.star(k, 170, 890, 1.9, "g_down", "caught", (1.0, -0.4), wrap=False, bag=False)


def s6_2(k):
    cc = k.c
    cc.set_source_rgb(0.10, 0.10, 0.11); cc.paint()
    cut(k, [(30, 250), (510, 250), (540, 800), (0, 800)], (0.30, 0.25, 0.20), shadow=False, lw=4)      # the drawer, open
    cut(k, [(0, 800), (540, 800), (540, 900), (0, 900)], (0.40, 0.33, 0.26), shadow=False, lw=4)
    ellipse(k, 270, 850, 30, 14, n.SILVER, 8, shadow=False, lw=3)
    n.plan_open2(k, 280, 520, 3.3, -0.04)
    n._seg(k, -60, 760, 110, 600, 96, 84, n.KEY, 3.2)
    n.hand(k, 110, 600, 5.0, 1.2, 0.0, flip=-1)


def s6_3(k):
    office(k, lamp_on=(440, 330), frame=False)
    n.star(k, 250, 1270, 3.4, "g_down", "knowing", (0.3, -0.3), wrap=False, bag=False)


def s6_4(k):
    cc = k.c
    office(k, lamp_on=(330, 400), frame=False)
    cc.set_source_rgb(0.50, 0.49, 0.46); cc.rectangle(-20, 90, 230, 820); cc.fill()                 # the doorway, lit behind him
    n.shadow(k, 40, 1040, 1.9, "open", lit_hand=None, look_down=1.0)
    n.star(k, 400, 800, 1.8, "g_down", "knowing", (-1.0, 0.1), wrap=False, bag=False)
    cc.set_source_rgb(0.11, 0.10, 0.10); cc.rectangle(170, 650, 420, 330); cc.fill()                # the desk; she sits on its corner
    cc.set_source_rgb(0.46, 0.42, 0.38); cc.rectangle(170, 650, 420, 11); cc.fill()
    ac.roll(k, 236, 636, 1.2, math.pi / 2, ln=170)


def s6_5(k):
    office(k, lamp_on=(460, 300), frame=False)
    n.star(k, 230, 1180, 3.0, "g_beckon3", "knowing", (-1.0, 0.0), wrap=False, curl=0.7)


def s6_6(k):
    cc = k.c
    cc.set_source_rgb(0.20, 0.20, 0.22); cc.paint()
    cc.save(); cc.rotate(-0.10)
    for i in range(9):
        cc.set_source_rgba(1, 1, 1, 0.13); cc.rectangle(-80, 80 + i * 44, 520, 18); cc.fill()
    cc.restore()
    pool(cc, 300, 600, 380, 0.42)
    pool(cc, 60, 300, 300, 0.40)
    n.shadow(k, -6, 1100, 2.3, "open", lit_hand=None, look_down=1.0)
    o = n.star(k, 410, 930, 2.3, "g_offer", "sideeye", (-1.0, 0.6), wrap=False)
    cc.set_source_rgb(0.14, 0.13, 0.13); cc.rectangle(150, 730, 420, 260); cc.fill()
    cc.set_source_rgb(0.48, 0.44, 0.40); cc.rectangle(150, 730, 420, 12); cc.fill()
    ac.roll(k, 230, 716, 1.15, math.pi / 2, ln=170)
    lx, ly = o["hands"][0]
    n.hand(k, lx + 4, ly + 10, 3.0, -1.35, 0.0, 1)
    arm_in(k, -40, 640, 118, 706, 54)


def s6_7a(k):
    """An insert: the office door from inside. The handle turns; keys swing in the lock; light under the door."""
    cc = k.c
    cc.set_source_rgb(0.20, 0.20, 0.22); cc.paint()
    cc.set_source_rgb(0.30, 0.29, 0.28); cc.rectangle(60, -20, 420, 1000); cc.fill()                 # the door
    cc.set_source_rgb(*INK); cc.set_line_width(6); cc.rectangle(60, -20, 420, 1000); cc.stroke()
    cc.set_source_rgb(0.95, 0.94, 0.86); cc.rectangle(60, 930, 420, 40); cc.fill()                   # light under it
    rect(k, 330, 380, 90, 210, (0.62, 0.62, 0.66), 9, lw=3)                                          # the lock plate
    cc.save(); cc.translate(376, 440); cc.rotate(0.55)                                              # the handle, turning
    rect(k, -150, -16, 170, 32, (0.80, 0.80, 0.84), 10, lw=3)
    cc.restore()
    ellipse(k, 376, 440, 26, 26, (0.70, 0.70, 0.74), 11, shadow=False, lw=3)
    ellipse(k, 376, 536, 13, 18, (0.08, 0.08, 0.09), 12, shadow=False, lw=2)                          # the keyhole
    cc.set_source_rgb(0.86, 0.80, 0.50); cc.set_line_width(9); cc.set_line_cap(1); cc.move_to(376, 540); cc.line_to(318, 560); cc.stroke()
    cc.set_source_rgb(*INK); cc.set_line_width(5); cc.new_path(); cc.arc(292, 588, 34, 0, 2 * math.pi); cc.stroke()     # the ring
    for i, a in enumerate((1.2, 1.7, 2.3)):                                                        # the other keys, swinging
        cc.save(); cc.translate(292 + math.cos(a) * 34, 588 + math.sin(a) * 34); cc.rotate(a - math.pi / 2)
        rect(k, -7, 0, 14, 70, (0.86, 0.80, 0.50), 13 + i, shadow=False, lw=2.4)
        ellipse(k, 0, 0, 13, 13, (0.86, 0.80, 0.50), 16 + i, shadow=False, lw=2.4)
        cc.restore()
    cc.set_source_rgb(1, 1, 1); cc.set_line_width(4)
    for (x0, y0, x1, y1) in ((210, 560, 180, 540), (206, 610, 172, 616), (228, 668, 204, 694)):   # they jingle
        cc.move_to(x0, y0); cc.line_to(x1, y1); cc.stroke()


def s6_7(k):
    cc = k.c
    office(k, lamp_on=(300, 330), frame=False)
    cc.set_source_rgb(0.86, 0.85, 0.80); cc.rectangle(500, 120, 60, 760); cc.fill()                 # the door, opening: someone has a key
    cc.set_source_rgb(0.46, 0.45, 0.43); cc.rectangle(-20, 120, 250, 520); cc.fill()                # the wall behind him, in the lamp's light
    n.shadow(k, 130, 900, 1.7, co.POSES["open"][:2] + co._ik(1, 104, co.BT + 80), lit_hand=1, look_down=0.6)
    cc.save(); cc.rectangle(236, 610, 250, 330); cc.clip()                                         # under the desk
    cc.set_source_rgb(0.09, 0.09, 0.10); cc.paint()
    n.star(k, 360, 1130, 2.0, "g_hide", "caught", (1.0, -0.4), wrap=False)
    cc.restore()
    cc.set_source_rgb(0.11, 0.10, 0.10); cc.rectangle(212, 570, 300, 40); cc.fill()                 # the desk top, two legs
    cc.set_source_rgb(0.46, 0.42, 0.38); cc.rectangle(212, 570, 300, 10); cc.fill()
    cc.set_source_rgb(0.11, 0.10, 0.10); cc.rectangle(212, 610, 24, 330); cc.fill(); cc.rectangle(486, 610, 24, 330); cc.fill()


# ---------------------------------------------------------------- beat 07: the bang
def lit_wall(k):
    cc = k.c
    cc.set_source_rgb(0.72, 0.71, 0.68); cc.paint()
    cc.set_source_rgba(0, 0, 0, 0.30)                                                              # the lamp's hard edge on the wall
    cc.new_path(); cc.move_to(0, 0); cc.line_to(540, 0); cc.line_to(540, 150); cc.line_to(0, 60); cc.close_path(); cc.fill()
    cc.new_path(); cc.move_to(0, 960); cc.line_to(540, 960); cc.line_to(540, 860); cc.line_to(0, 900); cc.close_path(); cc.fill()
    pool(cc, 270, 430, 460, 0.40)


def mom_shadow(k, x, feet, s, up=True):
    """Mom's shadow, without the strands that hang beside her face (they made her the sweeper)."""
    cc = k.c
    cc.push_group()
    if up:
        o = n.mom_up(k, x, feet, s, True)
    else:
        poses = dict(mo.POSES); poses["_up"] = mo.ik(-1, -44, mo.BT + 110) + mo.ik(1, 46, mo.SASH + 6)
        with n._swap((mo, "POSES", poses), (n, "AIM", math.atan2(110, -10))):
            o = n.mom_up(k, x, feet, s, True)
    hx, hy = o["head"]
    cc.save(); cc.set_operator(cairo.OPERATOR_CLEAR)
    for sx in (-1, 1):
        cc.rectangle(hx + sx * 49 * s - (0 if sx > 0 else 26 * s), hy - 6 * s, 26 * s, 72 * s); cc.fill()
    cc.restore()
    fig = cc.pop_group()
    cc.set_source(fig); cc.paint()
    return o


def s7_1(k):
    cc = k.c
    cc.set_source_rgb(0.72, 0.71, 0.68); cc.paint()                                                # the wall, in the lamp's light
    black_fig(k, lambda: co.client(k, 440, 560, 1.5, "open", "plain", look=(0, 0), roll=False, badge=False))
    hat_at(k, 443, 560 + (co.HY - 38) * 1.5, 1.9)
    cc.set_source_rgb(0.20, 0.20, 0.22); cc.rectangle(-20, 600, 600, 380); cc.fill()                 # the floor, past the desk
    for sx in (300, 400):                                                                         # his shoes, turning to the door
        cut(k, [(sx, 640), (sx + 80, 640), (sx + 96, 676), (sx, 676)], n.BLACK, shadow=False, lw=3)
    cc.set_source_rgb(0.04, 0.04, 0.05); cc.rectangle(-20, 0, 600, 150); cc.fill()                   # the desk, above her
    cc.set_source_rgb(0.04, 0.04, 0.05); cc.rectangle(-20, 0, 60, 980); cc.fill()
    n.star(k, 210, 1190, 3.0, "g_hide", "caught", (0.8, -0.6), wrap=False)


def s7_2(k):
    lit_wall(k)
    n.shadow(k, 96, 900, 1.5, co._ik(-1, -60, co.BT + 20) + co._ik(1, 30, co.BT + 110), lit_hand=None)
    mom_shadow(k, 466, 900, 1.4, up=False)


def s7_3(k):
    cc = k.c
    lit_wall(k)
    pose = co._ik(-1, -70, co.BT - 10) + co._ik(1, 40, co.BT + 110)
    o = black_fig(k, lambda: co.client(k, 96, 900, 1.5, pose, "plain", look=(0, 0), roll=False, badge=False))
    hx, hy = o["head"]
    hat_at(k, hx + 30, hy - 170, 1.9, 0.5)                                                         # his hat, off
    mom_shadow(k, 466, 900, 1.4, up=True)
    cc.set_source_rgb(1, 1, 1)                                                                     # the pop
    cc.save(); cc.translate(190, 486)
    cc.new_path()
    for i in range(16):
        r = 64 if i % 2 == 0 else 25
        a = i * math.pi / 8
        (cc.move_to if i == 0 else cc.line_to)(math.cos(a) * r, math.sin(a) * r)
    cc.close_path(); cc.fill_preserve(); cc.set_source_rgb(*INK); cc.set_line_width(4); cc.stroke()
    cc.restore()


# ---------------------------------------------------------------- beat 08: awake
def s8_1(k):
    party(k, 900)
    o = co.client(k, 96, 900, 1.5, co._ik(-1, -70, co.BT - 10) + co._ik(1, 40, co.BT + 110), "puzzled", look=(0.8, -0.3), roll=False)
    hx, hy = o["head"]
    n.paper_hat(k, hx + 30, hy - 150, 1.9, 0.5)
    om = n.mom_up(k, 466, 900, 1.4, False)
    cc = k.c
    (lx, ly) = om["hands"][0]
    ux, uy = math.cos(n.AIM), math.sin(n.AIM)                                                      # along the bottle, toward him
    mx, my = lx + ux * 64 * 1.4, ly + uy * 64 * 1.4                                                 # its mouth
    for t, r in ((2, 11), (-10, 8), (12, 7)):                                                     # foam at the mouth, not over the bottle
        ellipse(k, mx + t, my - 6 - abs(t) * 0.4, r, r * 0.9, (1, 1, 1), 60 + t, shadow=False, lw=1.6)
    kx, ky = hx + 84, hy - 96                                                                     # the cork, on its way to his hat
    cc.set_source_rgb(*INK); cc.set_line_width(3); cc.set_line_cap(1)
    for dd in (-10, 0, 10):
        cc.move_to(kx + 30 + dd, ky + 46 - dd * 0.4); cc.line_to(kx + 12 + dd, ky + 22 - dd * 0.4); cc.stroke()
    cc.save(); cc.translate(kx, ky); cc.rotate(-0.6)
    rect(k, -9, -13, 18, 26, (0.80, 0.66, 0.42), 31, shadow=False, lw=2.4)
    cc.restore()


def table(k, y):
    cc = k.c
    rect(k, -20, y, 600, 34, (0.70, 0.56, 0.40), 5, lw=3)
    cc.set_source_rgb(0.62, 0.49, 0.34); cc.rectangle(-20, y + 34, 600, H); cc.fill()


def s8_2(k):
    party(k, 760)
    n.party(k, 270, 1090, 2.7, "g_blower", "caught", (0.7, 0.0))
    table(k, 800)
    n.doughnut(k, 420, 790, 2.2)


def s8_3(k):
    cc = k.c
    party(k, 760)
    o = n.party(k, 250, 1240, 3.3, "g_blower", "caught", (0.9, 0.0), blow=1.0)
    (lx, ly), (rx, ry) = o["hands"]
    cc.set_source_rgb(*INK); cc.set_line_width(5); cc.set_line_cap(1)                               # it toots
    for a in (-0.5, -0.1, 0.3):
        x0, y0 = rx + 200 + math.cos(a) * 30, ry - 20 + math.sin(a) * 30
        cc.move_to(x0, y0); cc.line_to(x0 + math.cos(a) * 44, y0 + math.sin(a) * 44); cc.stroke()


def s8_4(k):
    cc = k.c
    party(k, 800)
    st.robot(k, 462, 800, 1.15, "idle", look=(-1, 0), side=-1)
    o = co.client(k, 110, 800, 1.45, co.POSES["open"][:2] + co._ik(1, 40, co.BT + 40), "warm", look=(0.6, 0.2), roll=False)
    rx, ry = o["hands"][1]
    ellipse(k, rx + 6, ry - 24, 13, 16, (0.80, 0.66, 0.42), 31, shadow=False, lw=2.4)                # the cork
    Hh = kit.PEOPLE["DON"]["h"]; sy = -300 * Hh + 92
    kit.ARM_POSES["_on2"] = ac._pose(Hh, left=(-58, sy + 50), right=(74, sy - 34))
    try:
        with ac.arms():
            o = dv.don(k, 300, 800, 1.7, "_on2", "happy", look=(0, 0.3))
    finally:
        del kit.ARM_POSES["_on2"]
    hx, hy = o["head"]
    cut(k, [(hx - 46, hy - 60), (hx - 46, hy - 104), (hx - 22, hy - 80), (hx, hy - 110), (hx + 22, hy - 80), (hx + 46, hy - 104),
            (hx + 46, hy - 60)], (0.98, 0.84, 0.25), shadow=False, lw=3)                            # a paper crown
    tx, ty = o["hands"][1]
    ellipse(k, tx, ty, 34, 30, kit.PEOPLE["DON"]["skin"], 33, shadow=False, lw=3.4)                 # his fist, the thumb up, large
    cut(k, [(tx - 14, ty - 20), (tx - 13, ty - 82), (tx + 11, ty - 86), (tx + 15, ty - 20)], kit.PEOPLE["DON"]["skin"], shadow=False, lw=3.4)
    for i in range(3):
        cc.set_source_rgb(*INK); cc.set_line_width(2.6); cc.move_to(tx - 26, ty - 6 + i * 11); cc.line_to(tx + 8, ty - 6 + i * 11); cc.stroke()
    qx, qy = o["hands"][0]
    n.coupe(k, qx - 2, qy + 12, 1.9)                                                               # the coupe he took at the bar
    ellipse(k, qx, qy - 30, 22, 20, kit.PEOPLE["DON"]["skin"], 34, shadow=False, lw=3)


def s8_5(k):
    cc = k.c
    party(k, 780)
    n.party(k, 420, 850, 1.7, "g_blower", "caught", (-1.0, 0.3))
    table(k, 660 + 40)
    st.confetti(k, 20, 800, 380, 930, n=18, seed=5, s=2.0)
    o = ac.pam(k, 170, 940, 2.2, "stand", (0.2, 0.9))
    (lx, ly), (rx, ry) = o["hands"]
    n.broom(k, rx + 10, ry - 150, 330, 930, 2.0)
    ellipse(k, rx + 6, ry - 30, 18, 18, kit.PEOPLE["PAM"]["skin"], 35, shadow=False, lw=3)


def s8_6(k):
    cc = k.c
    party(k, 900)
    cc.set_source_rgb(0.08, 0.08, 0.11); cc.rectangle(300, 120, 260, 420); cc.fill()                 # the window, the night outside
    cc.set_source_rgb(*INK); cc.set_line_width(6); cc.rectangle(300, 120, 260, 420); cc.stroke()
    cc.move_to(430, 120); cc.line_to(430, 540); cc.stroke()
    cc.save(); cc.rectangle(303, 123, 254, 414); cc.clip()
    g = cairo.RadialGradient(470, 240, 4, 470, 240, 150)
    g.add_color_stop_rgba(0, 1, 0.97, 0.80, 0.95); g.add_color_stop_rgba(1, 1, 0.97, 0.80, 0.0); cc.set_source(g); cc.paint()
    cc.set_source_rgb(0.02, 0.02, 0.03); cc.set_line_width(6); cc.move_to(488, 232); cc.line_to(488, 560); cc.stroke()
    ellipse(k, 470, 240, 13, 9, (1.0, 0.98, 0.86), 2, shadow=False, lw=2)
    cc.set_source_rgba(1, 1, 1, 0.35); cc.set_line_width(1.6)
    for i in range(22):
        rx, ry = 300 + (i * 53) % 250, 120 + (i * 89) % 400
        cc.move_to(rx, ry); cc.line_to(rx - 8, ry + 30); cc.stroke()
    cc.restore()
    n.party(k, 190, 1230, 3.1, "g_blower", "breath", (0, 0))


# id, seconds from the start (the script's estimate), the frame, tilt, colour, what is said, the light put on after the pass
FRAMES = [
    ("1.1", 0.0, s1_1, 0, False, 'N: "New Year\'s Eve."', lambda cc: shade(cc, -1, 0.45)),
    ("1.2", 2.0, s1_2, 0, False, "", lambda cc: shade(cc, -1, 0.50)),
    ("2.1", 4.0, s2_1, 0, False, 'N: "A woman like me doesn\'t walk alone."', None),
    ("2.2", 5.5, s2_2, 0, False, "", None),
    ("2.3", 6.5, s2_3, 0, False, "", lambda cc: shade(cc, -1, 0.55)),
    ("2.4", 7.5, s2_4, -0.07, False, "", None),
    ("2.5", 9.0, s2_5, 0, False, "", None),
    ("2.6", 10.0, s2_6, 0, False, 'N: "I don\'t run. I give them something to chase."', lambda cc: shade(cc, -1, 0.35)),
    ("3.1", 12.0, s3_1, 0, False, "", lambda cc: shade(cc, 1, 0.40)),
    ("3.2", 13.5, s3_2, 0, False, "", lambda cc: shade(cc, -1, 0.30)),
    ("3.3", 15.0, s3_3, 0, False, "", None),
    ("3.4", 16.0, s3_4, 0, False, "", None),
    ("4.1", 18.0, s4_1a, 0, False, "", lambda cc: shade(cc, -1, 0.40)),
    ("4.1", 19.5, s4_1b, 0, False, "", lambda cc: shade(cc, -1, 0.40)),
    ("4.2", 20.5, s4_2, 0, False, "", None),
    ("5.1", 22.0, s5_1, 0, False, "", None),
    ("5.2", 24.5, s5_2, 0, False, "", None),
    ("5.3", 27.0, s5_3, 0, False, 'SOFÍA: "The usual."', lambda cc: shade(cc, -1, 0.35)),
    ("5.4", 29.5, s5_4, 0, False, 'N: "He sent a note. They always send a note."', None),
    ("5.5", 32.0, s5_5, 0, False, "", None),
    ("5.6", 34.0, s5_6, 0, False, "", None),
    ("5.7", 36.0, s5_7, 0, False, "", None),
    ("5.8", 38.0, s5_8, 0, False, "", lambda cc: shade(cc, 1, 0.30)),
    ("5.9", 39.0, s5_9, 0, False, "", None),
    ("5.10", 41.0, s5_10, 0, False, "", None),
    ("6.1", 43.0, s6_1, 0, False, "", lambda cc: shade(cc, 1, 0.30)),
    ("6.2", 45.0, s6_2, 0, False, 'N: "Everybody had lost it. I found it in one drawer."', None),
    ("6.3", 47.5, s6_3, 0, False, "", lambda cc: shade(cc, -1, 0.55)),
    ("6.4", 49.0, s6_4, 0, False, "", None),
    ("6.5", 51.0, s6_5, 0, False, "", lambda cc: shade(cc, -1, 0.50)),
    ("6.6", 52.5, s6_6, -0.07, False, "", None),
    ("6.7", 54.0, s6_7a, 0, False, "(keys, off)", None),
    ("6.7", 55.0, s6_7, 0, False, "", None),
    ("7.1", 56.0, s7_1, 0, False, "", None),
    ("7.2", 58.5, s7_2, 0, False, 'MOM: "You! Not near Donnie\'s desk!"  THE SHADOW: "I only want my—"', None),
    ("7.3", 62.5, s7_3, 0, False, "(one pop)", None),
    ("8.1", 64.0, s8_1, 0, True, 'MOM: "Happy New Year, dear."', None),
    ("8.2", 66.0, s8_2, 0, True, "", None),
    ("8.3", 67.5, s8_3, 0, True, "", None),
    ("8.4", 69.5, s8_4, 0, True, "", None),
    ("8.5", 71.5, s8_5, 0, True, 'PAM: "Some dream. Others sweep."', None),
    ("8.6", 73.5, s8_6, 0, True, "", None),
]


def render(i):
    sid, t, fn, tilt, colour, said, post = FRAMES[i]
    sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    cc = cairo.Context(sf)
    cc.set_source_rgb(*NIGHT); cc.paint()
    if tilt:
        cc.translate(W / 2, H / 2); cc.rotate(tilt); cc.scale(1.10, 1.10); cc.translate(-W / 2, -H / 2)
    fn(Ctx(cc, 0))
    if not colour:
        eng.accent_pass(sf, n.ACCENTS2)
        cc = cairo.Context(sf)
        if post:
            post(cc)
        vignette(cc)
    return sf


def sheet(out, idx, tiles, cols, tw, captions, title=None):
    """A contact sheet of the frames in idx. captions: shot numbers and lines; otherwise the order number and a time."""
    th = tw * 16 // 9
    rows = (len(idx) + cols - 1) // cols
    lab = 44 if captions else 26
    top = 54 if title else 12
    Wp, Hp = cols * (tw + 12) + 12, top + rows * (th + lab) + 8
    sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, Wp, Hp)
    c = cairo.Context(sf); c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    if title:
        corp(c, title, 14, 34, 20, bold=True)
    for j, i in enumerate(idx):
        x, y = 12 + (j % cols) * (tw + 12), top + (j // cols) * (th + lab)
        c.save(); c.translate(x, y); c.scale(tw / float(W), tw / float(W)); c.set_source_surface(tiles[i], 0, 0)
        c.get_source().set_filter(cairo.FILTER_BEST); c.paint(); c.restore()
        c.set_source_rgb(0.10, 0.12, 0.20); c.set_line_width(1.2); c.rectangle(x, y, tw, th); c.stroke()
        sid, t, fn, tilt, colour, said, post = FRAMES[i]
        if captions:
            corp(c, sid, x, y + th + 15, 12, bold=True)
            if said:
                c.select_font_face("Inter", 0, 0); c.set_font_size(9.0)
                words, line, yy = said.split(), "", y + th + 28
                for w_ in words:
                    trial = (line + " " + w_).strip()
                    if c.text_extents(trial).x_advance > tw - 30 and line:
                        c.set_source_rgb(0.25, 0.28, 0.36); c.move_to(x + 30, yy - 13); c.show_text(line); line = w_; yy += 11
                    else:
                        line = trial
                c.set_source_rgb(0.25, 0.28, 0.36); c.move_to(x + 30, yy - 13); c.show_text(line)
        else:
            corp(c, "%d" % (i + 1), x, y + th + 18, 15, bold=True)
            corp(c, "%d:%02d" % (int(t) // 60, int(t) % 60), x + tw - 34, y + th + 18, 12, col=(0.35, 0.40, 0.50))
    sf.write_to_png(out)


def main(folder):
    tiles = [render(i) for i in range(len(FRAMES))]
    nfr = len(FRAMES)
    sheet("%s/on2_board_%s.png" % (folder, V), list(range(nfr)), tiles, 7, 216, True,
          "OFFICE NOIR 2 · The Shadow of Fate · storyboard " + V + " · script v2 · %d frames" % nfr)
    per = 14
    for s_ in range((nfr + per - 1) // per):
        sheet("%s/on2_board_mute_%s_%d.png" % (folder, V, s_ + 1), list(range(s_ * per, min(nfr, (s_ + 1) * per))), tiles, 7, 270, False)
    return tiles


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "../office-noir-2")
    print("wrote", len(FRAMES), "frames")
