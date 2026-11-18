"""v3, pinned: motion test v3 (on2_motion_test_v3.mp4), from on2_board_v7 and noir2_cast_v10. on2_motion.py is current.
OFFICE NOIR 2: the motion test, v3. Beats 01 to 04 of script v2, animated. 17 Nov.
on2_motion_v2.py and _v1.py are pinned. v3, after Tomas saw v2 ("she squirms out of the car; the walk is right") and chose:
  - 1.1: only the leg and the shoe. The door opens, her foot comes down out of the dark in four drawings, the heel
    meets the puddle, hold, cut. No glove on the pillar, no leaning out;
  - the narration stays A2;
  - the run was choppy: it changed drawing eight times a second on a film of twelve, with four leg positions and two
    arm positions that swapped. Now it is one loop of eight drawings, one each twelfth of a second (noir2_cast, a
    float phase): the foot plants, travels back, swings forward; the arms swing with it; the body rises between steps;
  - beats 03 and 04 are new: she runs past the sweeper, the sweeper sees the detective and sweeps the prints into her
    pan, his glass finds a broom, he walks off the wrong way; the coin, the robot's arm, PENDING APPROVAL.
Twelve drawings a second, held; 30 frames a second. The noir pass and the light are the storyboard's.
Sound: the first film's jazz, rain, her heels, the compact, the broom, his steps, the coin, the robot.
Writes ../office-noir-2/on2_motion_test_v3.mp4 (540 x 960) and on2_motion_timing_v3.json.
  KOKORO_DIR=/tmp/kokoro python3 on2_motion.py [A2|A|B|C]"""
import json
import math
import os
import subprocess
import sys
import cairo
import numpy as np
import soundfile as sf

os.environ.setdefault("KOKORO_DIR", "/tmp/kokoro")
import on2_board_v7 as b
import on2_sound as snd
import engine_on as eng
import noir2_cast_v10 as n
import client_ob as co
from kit import Ctx, INK, ellipse, rect, cut

V = "v3"
W, H, FPS = 540, 960, 30
SAFE = (18, 96, 522, 820)
LEAD, TAIL = 0.25, 0.42
PLAN = [("1.1", 2.0, "n1"), ("1.2", 2.0, None), ("2.1", 1.5, "n2"), ("2.2", 1.0, None), ("2.3", 1.0, None), ("2.4", 1.5, None),
        ("2.5", 1.0, None), ("2.6", 2.0, "n3"),
        ("3.1", 1.75, None), ("3.2", 2.25, None), ("3.3", 1.25, None), ("3.4", 2.75, None),
        ("4.1a", 1.5, None), ("4.1b", 1.25, None), ("4.2", 1.5, None)]
TEXT = dict(snd.NARR)


def ease(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def lerp(a, c, x):
    return a + (c - a) * min(1.0, max(0.0, x))


def rain(k, t, floor=None):
    """Streaks that fall: each one drops the height of the frame in about two thirds of a second."""
    cc = k.c
    cc.set_source_rgba(1, 1, 1, 0.20); cc.set_line_width(1.6); cc.set_line_cap(1)
    for i in range(30):
        x0 = (i * 97) % 580 - 20
        y = ((i * 173) % 1000 + t * 1500) % 1040 - 60
        cc.move_to(x0 - y * 0.26 + 120, y); cc.line_to(x0 - y * 0.26 + 111, y + 34); cc.stroke()


def splash(k, x, y, a):
    """Rings where something met the wet stones. a: 0..1 through its life."""
    if a <= 0 or a >= 1:
        return
    cc = k.c
    cc.set_source_rgba(1, 1, 1, 0.7 * (1 - a)); cc.set_line_width(2.4)
    for r in (16 + 40 * a, 8 + 22 * a):
        cc.save(); cc.translate(x, y); cc.scale(r, r * 0.3); cc.new_path(); cc.arc(0, 0, 1, 0, 2 * math.pi); cc.restore(); cc.stroke()


# ---------------------------------------------------------------- the shots
def m1_1(k, tl):
    b.street(k, 668, (440, 150), rain=False)
    door = ease((tl - 0.25) / 0.34)
    n.taxi(k, 150, 716, 2.5, door=door)
    d12 = int(round(tl * 12))
    if d12 >= 8:                                                                # her foot comes out of the dark and down, in four drawings
        foot, knee = (((186, 636), (219, 563)), ((192, 664), (218, 566)), ((199, 696), (217, 569)), ((206, 716), (216, 572)))[min(3, d12 - 8)]
        b.step_out(k, foot, knee, hand=0.0)
    splash(k, 176, 722, (tl - 11 / 12.0) / 0.5)
    rain(k, tl)


def m1_2(k, tl):
    b.street(k, 690, (430, 150), rain=False)
    x = 40 - 640 * ease((tl - 0.5) / 1.1) ** 1.6
    n.taxi(k, x, 730, 1.5, door=0.0)
    rise = 12 if tl < 1 / 12.0 else 5 if tl < 2 / 12.0 else 0
    look = (0.1, -0.2) if tl < 1.25 else (-0.7, 0.0)
    n.star(k, 350, 800 + rise, 1.9, "g_pose", "interested", look, sparkle=1.0 if int(tl * 12) % 6 < 3 else 0.2)
    rain(k, tl + 2)


def m2_1(k, tl, dur=2.75):
    cc = k.c
    b.street(k, 600, (440, 140), rain=False)
    p = tl / dur
    dy = 300 * (1 - ease(tl / 1.4))                                      # his shadow slides onto the stones after her
    cc.save(); cc.translate(0, dy)
    cc.set_source_rgb(*n.BLACK)
    cc.new_path(); cc.move_to(-20, 960); cc.line_to(120, 760); cc.line_to(200, 760); cc.line_to(190, 960); cc.close_path(); cc.fill()
    cc.save(); cc.translate(160, 752); cc.scale(84, 15); cc.new_path(); cc.arc(0, 0, 1, 0, 2 * math.pi); cc.restore(); cc.fill()
    cc.new_path(); cc.move_to(118, 752); cc.line_to(128, 700); cc.line_to(152, 712); cc.line_to(170, 696); cc.line_to(196, 708); cc.line_to(204, 752)
    cc.close_path(); cc.fill()
    cc.restore()
    n.star_back(k, 340, lerp(806, 772, p), lerp(1.92, 1.76, p), step=tl * 1.6)
    rain(k, tl + 4)


def m2_2(k, tl):
    cc = k.c
    cc.set_source_rgb(0.11, 0.11, 0.13); cc.paint()
    b.pool(cc, 300, 200, 420, 0.22)
    ang = 0.16 if tl < 1 / 12.0 else 0.10 if tl < 2 / 12.0 else 0.06
    n._seg(k, 330, 1000, 290, 760, 110, 96, n.KEY, 3.4)
    n.compact2(k, 270, 470, 9.0, ang, hat=tl >= 4 / 12.0)
    ellipse(k, 286, 760, 58, 52, n.KEY, 363, shadow=False, lw=3.4)


def m2_3(k, tl):
    cc = k.c
    cc.set_source_rgb(0.13, 0.13, 0.15); cc.paint()
    b.pool(cc, 380, 160, 420, 0.30)
    face = "interested" if tl < 4 / 12.0 else "real"
    n.star(k, 240, 1270 - (0 if tl < 4 / 12.0 else 6), 3.4, "g_mirror", face, (0.9, -0.1), wrap=False, mirror=True,
           sparkle=1.0 if tl >= 6 / 12.0 else 0.0)


def m2_4(k, tl):
    b.street(k, 720, None, rain=False)
    b.pool(k.c, 300, 120, 520, 0.38)
    slide = -40 * (1 - ease(tl / 0.25))
    n.shadow(k, 20 + slide, 1180, 2.5, "open", lit_hand=None, look_down=1.0)
    reach = ease((tl - 0.25) / 0.5)
    face = "real" if tl < 0.5 else "caught"
    look = (0.9, -0.1) if tl < 0.5 else (-0.6, 0.5) if tl < 0.75 else (-1.0, 0.9)
    o = n.star(k, 340, 1060, 2.6, "g_stand", face, look, wrap=False)
    lx, ly = o["hands"][0]
    ex, ey = lerp(-200, lx - 22, reach), lerp(380, ly - 52, reach)
    if tl >= 0.25:
        b.arm_in(k, ex - 320, ey - 110, ex, ey)


def m2_5(k, tl):
    cc = k.c
    cc.set_source_rgb(*b.GROUND); cc.paint()
    cc.set_source_rgb(0.20, 0.20, 0.23); cc.set_line_width(3)
    for i in range(7):
        cc.move_to(-20, 140 + i * 140); cc.line_to(560, 110 + i * 140); cc.stroke()
    cc.set_source_rgba(1, 1, 1, 0.16); cc.save(); cc.translate(250, 600); cc.scale(260, 200); cc.new_path(); cc.arc(0, 0, 1, 0, 2 * math.pi)
    cc.restore(); cc.fill()
    if tl < 2 / 12.0:                                                   # the compact, falling
        n.compact2(k, 230, 330 + 1500 * tl, 3.6, 0.9 + tl * 6)
    else:
        g = ease((tl - 2 / 12.0) / 0.34)
        cc.save(); cc.translate(220, 640); cc.scale(0.35 + 0.65 * g, 0.35 + 0.65 * g); cc.translate(-220, -640)
        n.powder_puff(k, 220, 640, 5.0)
        cc.restore()
    if 4 / 12.0 <= tl < 6 / 12.0:
        b.red_shoe(k, 330, 610, 3.6)
    elif 6 / 12.0 <= tl < 8 / 12.0:
        b.red_shoe(k, 460, 470, 3.2)
        n.footprints(k, 300, 700, 4.2, n=1, step=30)
    elif tl >= 8 / 12.0:
        n.footprints(k, 300, 700, 4.2, n=1, step=30)
        n.footprints(k, 420, 560, 3.6, n=1, step=30)


def cloth(k, x, y, s, ang):
    cc = k.c
    cc.save(); cc.translate(x, y); cc.rotate(ang); cc.scale(s, s)
    n._cloth(cc, [("M", -5, 0), ("C", -2, -3, 2, -3, 5, 0), ("C", 20, 14, 26, 50, 20, 88), ("C", 18, 104, 12, 114, 8, 122),
                  ("C", 4, 110, 0, 100, -4, 104), ("C", -8, 110, -12, 116, -16, 124), ("C", -22, 104, -26, 50, -5, 0)])
    n._curve(cc, (4, 6, 16, 22, 20, 56, 14, 96), n.WRAP_PALE, 1.6)
    cc.restore()


def runner(k, x, y, s, tl, face="caught", look=(-0.9, 0.0)):
    """Her run: a loop of eight drawings, two thirds of a second. She is highest between her steps."""
    u = (tl * 1.5) % 1.0
    up = 6 * (0.5 + 0.5 * math.cos(4 * math.pi * (u + 0.03)))
    w = math.sin(4 * math.pi * u)
    return n.star(k, x, y - up * s, s, "g_run3", face, look, lean=7 + w, lag=(-14 + 3 * w, -4), wrap=False, run=True, phase=float(u))


def m2_6(k, tl, dur=3.5):
    cc = k.c
    b.street(k, 580, (440, 140), rain=False)
    cc.set_source_rgba(1, 1, 1, 0.26); cc.save(); cc.translate(150, 690); cc.scale(190, 96); cc.new_path(); cc.arc(0, 0, 1, 0, 2 * math.pi)
    cc.restore(); cc.fill()
    p = tl / dur
    x, y, s = lerp(250, 470, p), lerp(720, 640, p), lerp(1.42, 1.0, p)
    for i in range(int(tl * 1.5 + 1e-6) + 1):                           # her prints: one where her near foot lands
        q = (i / 1.5) / dur
        n.footprints(k, lerp(250, 470, q) - 46, lerp(720, 640, q) + 6 + (7 if i % 2 else -7), lerp(2.2, 1.5, q), n=1, step=30)
    runner(k, x, y, s, tl)
    # the wrap: off her shoulders, down to the stones; his hand lifts it, shakes it, lets it go
    if tl < 0.75:                                                       # all of this stays above the narration's line
        f = tl / 0.75
        n.wrap_flying(k, lerp(250, 124, f), lerp(470, 716, f * f), 1.5, lerp(0.5, 0.05, f))
    elif tl < 1.25 or tl >= 3.0:
        n.wrap_flying(k, 124, 722, 1.5, 0.05)
    if 1.0 <= tl < 3.25:
        if tl < 1.25:
            hx, hy = lerp(-60, 124, (tl - 1.0) / 0.25), lerp(620, 712, (tl - 1.0) / 0.25)
        elif tl < 1.67:
            hx, hy = 130, lerp(712, 500, ease((tl - 1.25) / 0.42))
        elif tl < 3.0:
            hx, hy = 130, 500
        else:
            hx, hy = lerp(130, -80, (tl - 3.0) / 0.25), lerp(500, 470, (tl - 3.0) / 0.25)
        b.arm_in(k, hx - 180, hy - 80, hx, hy, 60)
        if 1.25 <= tl < 3.0:
            shake = (0.16 if int(tl * 12) % 2 else -0.16) if 1.67 <= tl < 2.5 else 0.0
            if tl < 2.75:
                cloth(k, hx + 20, hy + 10, 1.75, shake)
            else:                                                       # let go: it falls
                cloth(k, 150, lerp(520, 640, (tl - 2.75) / 0.25), 1.75, 0.5)
    rain(k, tl + 7)


# ---------------------------------------------------------------- beat 03: the sweeper and the detective
def prints(k, x, y, s, step, which):
    """Her prints, each one separately, so that they can be swept away one at a time."""
    for i in which:
        n.footprints(k, x + i * step * s, y - (14 * s if i % 2 else 0), s, n=1, step=step)


def m3_1(k, tl):
    b.street(k, 600, (420, 140), rain=False)
    xs = -130 + 800 * max(0.0, tl - 2 / 12.0)                            # the red dress, through the frame
    prints(k, 250, 840, 2.6, 30, [i for i in range(3) if xs > 300 + i * 78])
    if tl >= 2 / 12.0 and xs < 700:
        runner(k, xs, 900, 2.0, tl)
    if xs < 700:
        look = (max(-1.0, min(1.0, (xs - 170) / 260.0)), 0.1)             # her head goes with it
    else:
        look = (1.0, 0.1) if tl < 17 / 12.0 else (0.6, 0.9)               # then down, to what it left
    n.sweeper(k, 170, 930, 2.2, "lean", "neutral", look)
    rain(k, tl + 11)


SWEEP = {12: (520, 902), 13: (432, 904), 14: (352, 906), 15: (300, 908)}     # the broom's head, drawing by drawing


def m3_2(k, tl, dur=2.25):
    b.street(k, 540, (300, 130), rain=False)
    p = tl / dur
    d12 = int(round(tl * 12))
    n.detective(k, lerp(476, 420, p), lerp(688, 704, p) + (3 if d12 % 5 < 2 else 0), lerp(0.98, 1.16, p), "look", "squint", (0.6, 0.8), wrap=True)
    left = 3 if d12 < 13 else 2 if d12 < 14 else 1 if d12 < 15 else 0
    prints(k, 300, 900, 2.6, 30, range(left))
    n.dustpan(k, 262, 922, 2.0, full=d12 >= 15)
    if d12 in SWEEP:
        n.sweeper(k, 190, 930, 2.25, "sweep", "neutral", (0.7, 0.9), head=SWEEP[d12])
    else:
        look = (0.6, 0.9) if d12 < 5 else (1.0, -0.2) if d12 < 12 else (0.7, 0.9) if d12 < 18 else (1.0, -0.2)
        n.sweeper(k, 190, 930, 2.25, "lean", "neutral", look)
    rain(k, tl + 13)


def glass_prints(k, x, y, r, off):
    """What his glass shows, as noir2_cast.glass_view draws it, but the stones slide under the glass: off is how far the
    trail still has to come (in pixels). A print, a print, then the bristles."""
    c = k.c
    g = r / 42.0
    c.save(); c.new_path(); c.arc(x, y, r, 0, 2 * math.pi); c.clip()
    c.set_source_rgb(0.46, 0.46, 0.49); c.paint()
    c.set_source_rgb(0.38, 0.38, 0.41); c.set_line_width(1.2 * g)
    for i in range(-3, 4):
        c.move_to(x - r, y + i * 15 * g); c.line_to(x + r, y + i * 15 * g); c.stroke()
    x0 = x + off
    for i, (px, py) in enumerate(((-30, 9), (-13, -8), (4, 9))):
        c.save(); c.translate(x0 + px * g, y + py * g); c.rotate(-0.12); c.scale(g, g)
        c.set_source_rgb(1, 1, 1)
        c.new_path(); c.move_to(-2, -5.5); c.curve_to(8, -8, 15, -3, 15, 0); c.curve_to(15, 3, 8, 8, -2, 5.5); c.close_path(); c.fill()
        c.new_path(); c.arc(-8.5, 0, 3.0, 0, 2 * math.pi); c.fill()
        c.restore()
    c.set_source_rgba(1, 1, 1, 0.55); c.set_line_width(5 * g); c.set_line_cap(1)
    c.move_to(x0 + 10 * g, y + 4 * g); c.line_to(x0 + 19 * g, y - 3 * g); c.stroke()
    c.save(); c.translate(x0 + 27 * g, y + 2 * g); c.rotate(0.22); c.scale(g, g)
    c.set_source_rgb(*INK); c.set_line_width(8); c.move_to(4, -12); c.line_to(22, -60); c.stroke()
    c.set_source_rgb(0.72, 0.56, 0.36); c.set_line_width(4.6); c.move_to(4, -12); c.line_to(22, -60); c.stroke()
    rect(k, -9, -22, 13, 44, (0.50, 0.36, 0.22), 720, shadow=False, lw=1.8)
    cut(k, [(-9, -22), (-9, 22), (-27, 27), (-27, -27)], (0.86, 0.74, 0.46), shadow=False, lw=1.8)
    c.set_source_rgb(0.50, 0.40, 0.20); c.set_line_width(1.3)
    for i in range(-3, 4):
        c.move_to(-10, i * 6); c.line_to(-26, i * 7.4); c.stroke()
    c.restore()
    c.restore()
    c.set_source_rgb(*INK); c.set_line_width(max(5.0, r * 0.11)); c.new_path(); c.arc(x, y, r, 0, 2 * math.pi); c.stroke()
    c.set_source_rgb(*n.SILVER); c.set_line_width(max(2.2, r * 0.045)); c.new_path(); c.arc(x, y, r, 0, 2 * math.pi); c.stroke()
    c.set_source_rgba(1, 1, 1, 0.85); c.set_line_width(max(2.0, r * 0.05)); c.set_line_cap(1)
    c.new_path(); c.arc(x, y, r - r * 0.16, math.pi * 1.10, math.pi * 1.36); c.stroke()


def m3_3(k, tl):
    cc = k.c
    cc.set_source_rgb(0.09, 0.09, 0.10); cc.paint()
    f = ease(tl / 0.58)
    gx = lerp(214, 250, f)                                               # the glass itself moves a little along the trail
    n.glass_handle(k, gx, 440, 220, 0.6)
    glass_prints(k, gx, 440, 220, lerp(300, 0, f))


def m3_4(k, tl):
    b.street(k, 580, (270, 130), rain=False)
    d12 = int(round(tl * 12))
    walk = max(0.0, tl - 1.5)
    xd = 410 - 560 * walk
    if d12 < 5:
        dlook, dlean = (-0.3, 0.9), -7                                   # bent over the pan
    elif d12 < 12:
        dlook, dlean = (-0.8, -0.3), 0                                   # he straightens up and looks at her
    elif d12 < 15:
        dlook, dlean = (-1.0, 0.3), 0                                    # left
    elif d12 < 18:
        dlook, dlean = (1.0, 0.1), 0                                     # right
    else:
        dlook, dlean = (-1.0, 0.1), -3                                   # and off, the wrong way
    plook = (1.0, 0.0) if d12 < 7 else (0.2, -1.0) if d12 < 19 else (max(-1.0, min(1.0, (xd - 150) / 200.0)), 0.0)

    def don():
        n.detective(k, xd, 930 - (5 if walk > 0 and d12 % 4 < 2 else 0), 1.75, "look", "squint", dlook, lean=dlean, wrap=True)
    if walk > 0:                                                         # he passes behind her
        don()
    n.sweeper(k, 150, 930, 2.0, "lean", "neutral", plook)
    n.dustpan(k, 280, 900, 2.0, full=True)
    if walk <= 0:
        don()
    rain(k, tl + 17)


# ---------------------------------------------------------------- beat 04: the door
def door_set(k, floor=760):
    """on2_board.bar_door, with the rain left to fall."""
    cc = k.c
    b.street(k, floor, None, rain=False)
    cc.set_source_rgb(0.72, 0.71, 0.66); cc.rectangle(300, 110, 300, floor - 110); cc.fill()
    cc.set_source_rgb(*INK); cc.set_line_width(5); cc.rectangle(300, 110, 300, floor - 110); cc.stroke()
    cc.set_source_rgba(1, 1, 1, 0.20); cc.new_path(); cc.move_to(300, floor); cc.line_to(600, floor); cc.line_to(600, 960); cc.line_to(120, 960)
    cc.close_path(); cc.fill()


def tag(k, x, y, s, ang):
    cc = k.c
    cc.save(); cc.translate(x, y); cc.rotate(ang); cc.scale(s, s)
    cut(k, [(-44, 8), (-36, 0), (36, 0), (44, 8), (44, 36), (-44, 36)], (0.98, 0.95, 0.80), shadow=False, lw=1.8 / max(1.0, s / 1.25))
    cc.set_source_rgb(*INK); cc.select_font_face("Inter", 0, 1); cc.set_font_size(11.5)
    for i, t in enumerate(("PENDING", "APPROVAL")):
        e = cc.text_extents(t); cc.move_to(-e.width / 2 - e.x_bearing, 16 + i * 13); cc.show_text(t)
    cc.restore()


def m4_1a(k, tl):
    cc = k.c
    door_set(k)
    d12 = int(round(tl * 12))
    rlook = (-0.8, -0.3) if d12 < 6 else (-0.6, 0.8) if d12 < 13 else (0.9, 0.0)      # the glove, the cup, then after her
    turn = {} if d12 < 6 else dict(head_rot=0.10, head_dx=-4) if d12 < 13 else dict(head_rot=-0.12, head_dx=6)
    o = n.rn.robot_noir(k, 340, 1020, 2.2, "stand", "eager", rlook, cap=False, **turn)
    (lx, ly), (rx, ry) = o["hands"]
    hx, hy = o["head"]
    n.battery_card(k, 336, hy + 150 * 2.2, 2.0, 0.05)
    if d12 == 10:                                                            # the coin goes into the cup: drawn behind its rim
        b.coin(k, lx + 4, ly - 100, 34)
    n.cup(k, lx, ly - 34 + (6 if d12 == 11 else 0), 3.6)
    ellipse(k, lx, ly, 18, 18, (0.20, 0.20, 0.22), 23, shadow=False, lw=3)
    if d12 < 2 or d12 >= 13:
        g = None
    elif d12 < 10:
        g = 1 - ease((d12 - 1) / 3.0)                                        # in, from the left
    else:
        g = ease((d12 - 9) / 3.0)                                            # and gone again: she has not slowed
    if g is not None:
        ox, oy = -230 * g, -150 * g
        n._seg(k, -60 + ox, 300 + oy, 110 + ox, 420 + oy, 96, 84, n.KEY, 3.2)
        ellipse(k, 118 + ox, 428 + oy, 48, 44, n.KEY, 336, shadow=False, lw=3.2)
        opened = d12 >= 6
        for i, a in enumerate((0.25, 0.65, 1.05, 1.45) if opened else (0.95, 1.12, 1.29, 1.46)):
            ln = 78 if opened else 64
            n._seg(k, 118 + ox + math.cos(a) * 34, 428 + oy + math.sin(a) * 34, 118 + ox + math.cos(a) * ln, 428 + oy + math.sin(a) * ln, 20, 16, n.KEY, 2.6)
        if not opened:                                                       # the coin, still in her fingers
            b.coin(k, 142 + ox, 500 + oy, 34)
    if 6 <= d12 < 10:                                                        # it falls
        f = (d12 - 6) / 4.0
        cx, cy = lerp(142, lx + 4, f), lerp(500, ly - 100, f * f)
        b.coin(k, cx, cy, 34)
        cc.set_source_rgb(1, 1, 1); cc.set_line_width(4); cc.set_line_cap(1)
        for dx in (-22, 0, 22):
            cc.move_to(cx + dx, cy - 50); cc.line_to(cx + dx, cy - (100 if dx else 120)); cc.stroke()
    rain(k, tl + 19)


def m4_1b(k, tl):
    cc = k.c
    door_set(k)
    d12 = int(round(tl * 12))
    if d12 < 2:                                                              # she is still walking
        n.star(k, 400 + d12 * 34, 1010 - (6 if d12 % 2 else 0), 2.2, "g_down", "interested", (0.6, 0.0), wrap=False, bag=False)
        o = n.rn.robot_noir(k, 56, 800, 1.18, "stand", "eager", (0.9, 0.0), cap=False)
        (lx, ly), _ = o["hands"]
        n.battery_card(k, 56 - 2 * 1.18, o["head"][1] + 150 * 1.18, 1.18 * 0.9, 0.05, 920)
        n.cup(k, lx, ly - 16 * 1.18, 1.18 * 1.5, 921)
        ellipse(k, lx, ly, 8 * 1.18, 8 * 1.18, (0.20, 0.20, 0.22), 923, shadow=False, lw=1.6 * 1.18)
    else:
        n.star(k, 468, 1010, 2.2, "g_down", "appraise", (-1.0, 0.5), lean=-3 if d12 < 4 else 0, wrap=False, bag=False)
        o = n.coin_steps(k, 56, 800, 1.18, 2, lines=d12 < 4)                 # the arm is out, across her path
        if d12 >= 5:                                                         # her coin, back, and the tag swinging under it
            bx, by = o["claw"]
            b.coin(k, bx + 14, by, 30)
            sw = 0.22 * math.cos((d12 - 5) * 1.6) * math.exp(-(d12 - 5) / 3.5)
            cc.set_source_rgb(*INK); cc.set_line_width(2.4); cc.move_to(bx + 14, by + 30); cc.line_to(bx + 18 - sw * 22, by + 52); cc.stroke()
            tag(k, bx + 18 - sw * 22, by + 52, 1.25, 0.05 + sw)
    rain(k, tl + 21)


def m4_2(k, tl):
    cc = k.c
    cc.set_source_rgb(0.12, 0.12, 0.14); cc.paint()
    b.pool(cc, 300, 300, 460, 0.26)
    d12 = int(round(tl * 12))
    taken = d12 >= 10
    spread = 86 if not taken else 40                                         # the claw, and it closes on nothing
    for col, w in ((INK, 62), (n.SILVER, 44)):
        cc.set_source_rgb(*col); cc.set_line_width(w); cc.set_line_cap(1); cc.move_to(-40, 330); cc.line_to(110, 330); cc.stroke()
    for sy in (-1, 1):
        cc.set_source_rgb(*INK); cc.set_line_width(26); cc.move_to(110, 330); cc.line_to(180, 330 + sy * spread); cc.stroke()
        cc.set_source_rgb(*n.SILVER); cc.set_line_width(15); cc.move_to(110, 330); cc.line_to(180, 330 + sy * spread); cc.stroke()
    if d12 < 6:
        gx, gy = (240, -150) if d12 < 5 else (110, -70)                      # her glove comes in from the door's side
        show = d12 >= 5
    elif d12 < 10:
        gx, gy, show = 0, 0, True                                            # a finger and thumb on the coin
    else:
        f = (d12 - 9) / 2.0
        gx, gy, show = 330 * f, -210 * f, d12 < 12                           # and it is gone, sharply
    ox, oy = (gx, gy) if taken else (0, 0)
    if not taken or show:
        b.coin(k, 250 + ox, 330 + oy, 92)
        sw = 0.10 * math.cos(d12 * 1.5) * math.exp(-d12 / 4.0) + (0.5 if taken else 0.0)
        cc.set_source_rgb(*INK); cc.set_line_width(4.5); cc.move_to(250 + ox, 424 + oy); cc.line_to(256 + ox - sw * 40, 462 + oy); cc.stroke()
        tag(k, 256 + ox - sw * 40, 462 + oy, 3.2, 0.05 + sw)
    if show:
        n._seg(k, 600 + gx, 150 + gy, 420 + gx, 250 + gy, 100, 88, n.KEY, 3.4)
        ellipse(k, 410 + gx, 256 + gy, 50, 46, n.KEY, 336, shadow=False, lw=3.2)
        for (fx, fy) in ((346, 262), (352, 312)):
            ellipse(k, fx + gx, fy + gy, 40, 17, n.KEY, 337 + fy, shadow=False, lw=3)
    if taken and d12 < 12:                                                   # how fast
        cc.set_source_rgb(1, 1, 1); cc.set_line_width(5); cc.set_line_cap(1)
        for dy in (-40, 0, 44):
            cc.move_to(250, 330 + dy); cc.line_to(250 + gx * 0.7, 330 + dy + gy * 0.7); cc.stroke()


SHOTS = {"1.1": (m1_1, 0, lambda cc: b.shade(cc, -1, 0.45)), "1.2": (m1_2, 0, lambda cc: b.shade(cc, -1, 0.50)), "2.1": (m2_1, 0, None),
         "2.2": (m2_2, 0, None), "2.3": (m2_3, 0, lambda cc: b.shade(cc, -1, 0.55)), "2.4": (m2_4, -0.07, None), "2.5": (m2_5, 0, None),
         "2.6": (m2_6, 0, lambda cc: b.shade(cc, -1, 0.35)),
         "3.1": (m3_1, 0, lambda cc: b.shade(cc, 1, 0.40)), "3.2": (m3_2, 0, lambda cc: b.shade(cc, -1, 0.30)), "3.3": (m3_3, 0, None),
         "3.4": (m3_4, 0, None), "4.1a": (m4_1a, 0, lambda cc: b.shade(cc, -1, 0.40)), "4.1b": (m4_1b, 0, lambda cc: b.shade(cc, -1, 0.40)),
         "4.2": (m4_2, 0, None)}


def timing(kind):
    meta = json.load(open(snd.TAKES + "/takes.json"))
    rows, t = [], 0.0
    for shot, planned, key in PLAN:
        need = (LEAD + meta["%s_%s" % (key, kind)]["len"] + TAIL) if key else 0.0
        d = math.ceil(max(planned, need) * 12 - 1e-6) / 12.0
        row = {"shot": shot, "start": round(t, 4), "len": round(d, 4)}
        if key:
            row["line"] = {"who": "N", "text": TEXT[key], "t0": round(t + LEAD, 3), "t1": round(t + LEAD + meta["%s_%s" % (key, kind)]["len"], 3)}
        rows.append(row); t += d
    return rows, t


def caption(cc, text):
    cc.select_font_face("Inter", cairo.FONT_SLANT_ITALIC, cairo.FONT_WEIGHT_BOLD); cc.set_font_size(23)
    rows, line = [], ""
    for wd in text.split():
        trial = (line + " " + wd).strip()
        if cc.text_extents(trial).x_advance > SAFE[2] - SAFE[0] - 36 and line:
            rows.append(line); line = wd
        else:
            line = trial
    rows.append(line)
    hh = len(rows) * 30 + 22; y0 = SAFE[3] - hh
    cc.set_source_rgba(0.04, 0.04, 0.06, 0.82); cc.rectangle(SAFE[0], y0, SAFE[2] - SAFE[0], hh); cc.fill()
    cc.set_source_rgb(1, 1, 1)
    for j, ln in enumerate(rows):
        e = cc.text_extents(ln); cc.move_to((W - e.x_advance) / 2, y0 + 33 + j * 30); cc.show_text(ln)


def frame(row, tl, t):
    fn, tilt, post = SHOTS[row["shot"]]
    sf_ = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    cc = cairo.Context(sf_); cc.set_source_rgb(*b.NIGHT); cc.paint()
    if tilt:
        cc.translate(W / 2, H / 2); cc.rotate(tilt); cc.scale(1.10, 1.10); cc.translate(-W / 2, -H / 2)
    k = Ctx(cc, int(round(t * 12)) % 3)
    if row["shot"] in ("2.1", "2.6", "3.2"):
        fn(k, tl, row["len"])
    else:
        fn(k, tl)
    eng.accent_pass(sf_, n.ACCENTS2)
    cc = cairo.Context(sf_)
    if post:
        post(cc)
    b.vignette(cc)
    ln = row.get("line")
    if ln and ln["t0"] - 0.05 <= t <= ln["t1"] + 0.30:
        caption(cc, ln["text"])
    return sf_


def main(kind="A2", folder="../office-noir-2"):
    rows, total = timing(kind)
    json.dump({"kind": kind, "total": total, "shots": rows}, open("on2_motion_timing_%s.json" % V, "w"), indent=1)
    tmp = "/tmp/on2/motion"; os.makedirs(tmp, exist_ok=True)
    nfr = int(round(total * FPS))
    enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", "%dx%d" % (W, H), "-r", str(FPS),
                            "-i", "-", "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p", "-colorspace", "bt709",
                            "-color_primaries", "bt709", "-color_trc", "bt709", tmp + "/video.part.mp4"], stdin=subprocess.PIPE)
    last, buf = None, None
    for f in range(nfr):
        t = f / float(FPS)
        d12 = math.floor(t * 12 + 1e-6)                                  # which drawing: twelve a second, held
        row = [r for r in rows if r["start"] <= d12 / 12.0 + 1e-6][-1]
        if d12 != last:
            tl = d12 / 12.0 - row["start"]
            buf = bytes(frame(row, max(0.0, tl), d12 / 12.0).get_data()); last = d12
        enc.stdin.write(buf)
    enc.stdin.close(); enc.wait()
    os.replace(tmp + "/video.part.mp4", tmp + "/video.mp4")
    wav, spans = snd.motion_mix3([(r["shot"], r["start"], r["len"]) for r in rows], total, kind, tmp + "/mix.wav")
    out = "%s/on2_motion_test_%s.mp4" % (folder, V)
    # one constant gain to about -14.5 LUFS, then the final file is measured
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", wav, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True)
    cur = float([x for x in r.stderr.split("\n") if "I:" in x][-1].split("I:")[1].split("LUFS")[0])
    gain = -13.5 - cur
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp + "/video.mp4", "-i", wav, "-map", "0:v", "-map", "1:a", "-af",
                    "volume=%.2fdB,alimiter=limit=0.60:attack=2:release=40:level=disabled" % gain, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                    "-shortest", tmp + "/out.part.mp4"], check=True)
    os.replace(tmp + "/out.part.mp4", out)
    return out, rows, total, nfr


if __name__ == "__main__":
    out, rows, total, nfr = main(sys.argv[1] if len(sys.argv) > 1 else "A2")
    print("wrote", out, "%.2f s" % total, nfr, "frames")
