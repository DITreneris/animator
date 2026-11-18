"""v12, pinned: beats 06 to 08 as motion test v22 used them. on2_motion_b68.py is current.
v12 (18 Nov): the loop (Tomas: back through the window to the taxi; he chose): 8.6 ends on the toot, without the black;
8.7, she is asleep again and the camera goes into the window behind her, where a taxi pulls up in the rain, until the
window is the frame: the last drawing is the first drawing of 1.1. on2_motion_b68_v11.py is pinned.
v11 (18 Nov): from the second cold viewer's notes (Tomas chose): her face as the drawer opens (6.2r), her eyes under the
desk as she knows the shoes (7.1r), Pam sweeps her icing-sugar prints into the pan with the puff of 3.2 (8.5), and the
end is her face: a look at Pam, eyes shut, the blower half out and sagging, black (8.6; the lamp in the window is cut).
on2_motion_b68_v10.py is pinned.
v10 (18 Nov): her hands push the door shut in 6.1. on2_motion_b68_v9.py is pinned.
v9 (18 Nov): 6.1 opens on her back as she shuts the door. on2_motion_b68_v8.py is pinned.
v8 (18 Nov): 8.3 is a big close-up. on2_motion_b68_v7.py is pinned.
v7 (18 Nov): her line about the drawer starts as she comes in (6.1); 6.2, 6.7 and 7.1 shorter. on2_motion_b68_v6.py is pinned.
v6 (18 Nov): one more line of hers (6.4, 'Let him come.'); 8.2, 8.3 and 8.4 shorter. on2_motion_b68_v5.py is pinned.
v4 (18 Nov): clocks at 11:59 in the office and on the wall, midnight on the pop, 12:00 at the party; lights across the last window. on2_motion_b68_v3.py is pinned.
OFFICE NOIR 2: beats 06, 07 and 08, animated. Script v3, storyboard v7 frames 6.1 to 8.6. 17 Nov.
Used by on2_motion.py (v7), which hands itself over with use(), as on2_motion_b5.py is. Every shot takes (k, tl, dur).
06 the office and the trap: the door shut with her back, the roll in Don's drawer, the lamp, the hat at the door, one
red finger, his hand to the roll, keys, under the desk. 07 the bang: his shoes, two shadows on the wall, one pop, the
hat lifts off. 08 awake, in colour: Mom and the champagne, the paper hat coming down, the party blower, Don's thumb,
Pam's broom, the lamp in the window.
The shots in COLOUR are not put through the noir pass. Lines from the shadows on the wall are cards without tails
(nobody's mouth is drawn); Mom's and Pam's in colour have tails beside their mouths."""
import math
import cairo
import kit
import client_ob as co
import acts_ob as ac
import set_ob as st
import don_v4 as dv
from kit import INK, ellipse, rect, cut

m = None
TIP = {}                                                    # shot -> (tail tip or None, the card's left top corner)
COLOUR = {"8.1", "8.2", "8.3", "8.4", "8.5", "8.6", "8.7"}
A72 = 2.75                                                  # 7.2 is two rows of the plan, one for each line; the first is this long

# v8: 6.3 is cut; 6.4, 6.5, 6.6, 7.1, 8.2, 8.4 and 8.6 are shorter
PLAN = [("6.1", 2.0, "n5", -1.65), ("6.2", 1.0, None), ("6.2r", 9 / 12.0, None), ("6.2c", 22 / 12.0, None), ("6.4", 2.0, "n11"), ("6.5", 14 / 12.0, None), ("6.6", 20 / 12.0, None),
        ("6.7a", 1.0, None), ("6.7", 1.25, None), ("7.1", 10 / 12.0, None), ("7.1r", 9 / 12.0, None), ("7.1c", 5 / 12.0, None), ("7.2a", A72, "m1"), ("7.2b", 1.5, "c1", 0.05), ("7.3", 1.5, None),
        ("8.1", 2.5, "m2"), ("8.2", 17 / 12.0, None), ("8.3", 19 / 12.0, None), ("8.4", 1.5, None), ("8.5", 2.5, "p1"), ("8.6", 2.0, None), ("8.7", 18 / 12.0, None)]


def use(mod):
    global m
    m = mod


def d12_(tl):
    return int(round(tl * 12))


def swayed(k, x, feet, deg, draw):
    cc = k.c
    cc.save(); cc.translate(x, feet); cc.rotate(math.radians(deg)); cc.translate(-x, -feet)
    o = draw()
    cc.restore()
    return o


def say(cc, text, box, tip):
    """A spoken line on a white card, one or two rows, inside the safe area. tip: where the tail ends, beside the
    speaker's mouth, or None for a speaker whose mouth is not in the picture."""
    cc.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); cc.set_font_size(26)
    rows = [text]
    if cc.text_extents(text).x_advance > 290:
        words = text.split(); best = None
        for i in range(1, len(words)):
            a, b_ = " ".join(words[:i]), " ".join(words[i:])
            w_ = max(cc.text_extents(a).x_advance, cc.text_extents(b_).x_advance)
            if best is None or w_ < best[0]:
                best = (w_, [a, b_])
        rows = best[1]
    w = max(cc.text_extents(r_).x_advance for r_ in rows) + 36
    h, r = 26 + 32 * len(rows), 16
    x, y = box
    x = max(m.SAFE[0], min(m.SAFE[2] - w, x)); y = max(m.SAFE[1], min(m.SAFE[3] - h, y))
    for fill in (False, True):
        cc.new_path()
        cc.arc(x + r, y + r, r, math.pi, 1.5 * math.pi); cc.arc(x + w - r, y + r, r, 1.5 * math.pi, 2 * math.pi)
        cc.arc(x + w - r, y + h - r, r, 0, 0.5 * math.pi); cc.arc(x + r, y + h - r, r, 0.5 * math.pi, math.pi); cc.close_path()
        if tip is not None:                                 # the tail leaves from the edge nearest the mouth
            if tip[1] > y + h:
                bx = max(x + 26, min(x + w - 26, tip[0]))
                cc.move_to(bx - 12, y + h); cc.line_to(tip[0], tip[1]); cc.line_to(bx + 12, y + h); cc.close_path()
            else:
                bx = x if tip[0] < x else x + w
                cc.move_to(bx, y + h / 2 - 11); cc.line_to(tip[0], tip[1]); cc.line_to(bx, y + h / 2 + 11); cc.close_path()
        if fill:
            cc.set_source_rgb(1, 1, 1); cc.fill()
        else:
            cc.set_source_rgb(*INK); cc.set_line_width(7); cc.set_line_join(1); cc.stroke()
    cc.set_source_rgb(*INK)
    for j, r_ in enumerate(rows):
        cc.move_to(x + 18, y + 38 + j * 32); cc.show_text(r_)


# ---------------------------------------------------------------- beat 06: the office and the trap
def m6_1(k, tl, dur):
    n, b = m.n, m.b
    cc = k.c
    d = d12_(tl)
    b.office(k)
    m.clock(k, 470, 132, 28)                                              # v4: 11:59
    shut = d >= 4
    cc.set_source_rgb(*((0.08, 0.08, 0.09) if shut else (0.46, 0.45, 0.42))); cc.rectangle(40, 120, 250, 760); cc.fill()     # the door
    cc.set_source_rgb(0.34, 0.33, 0.31); cc.set_line_width(6); cc.rectangle(40, 120, 250, 760); cc.stroke()
    ellipse(k, 262, 520, 9, 9, n.SILVER, 9, shadow=False, lw=2)
    cc.set_source_rgb(0.24, 0.24, 0.27); cc.rectangle(-20, 880, 600, 100); cc.fill()
    if not shut:                                                          # v9: her back to us; the door swings shut in front of her
        wd = 250 * (1 - d / 4.0)
        cc.set_source_rgb(0.08, 0.08, 0.09); cc.rectangle(40 + wd, 120, 250 - wd, 760); cc.fill()
        for sx in (-1, 1):                                                # v10: her gloves, flat on the door, pushing it shut;
            hx = 170 + sx * 138 - (d * 5 if sx < 0 else 0)                # the arms go behind her hair
            n._seg(k, 170 + sx * 50, 600, hx, 500, 30, 26, n.KEY, 2.4)
            ellipse(k, hx, 494, 22, 28, n.KEY, 870 + sx, shadow=False, lw=2)
        n.star_back(k, 170, 890, 1.9, step=None, wrap=False)
        return
    look = (0.4, 0.0) if d < 10 else (1.0, -0.4) if d < 17 else (1.0, 0.5)      # the door; his photograph; Don's desk
    with m.breath(k, 170, 890, tl, rate=0.5, amt=0.012):
        n.star(k, 170, 890 + (7 if d == 4 else 0), 1.9, "g_down", "caught", look, wrap=False, bag=False)


def m6_2(k, tl, dur):
    """v9: first Don's desk from the front, and her glove pulls a drawer out of it: the roll is in the drawer. Then,
    from above as before, she unrolls a hand's width and her finger goes along the bays to the corner."""
    n = m.n
    cc = k.c
    d = d12_(tl)
    if d < 12:
        cc.set_source_rgb(0.10, 0.10, 0.11); cc.paint()
        m.b.pool(cc, 300, 300, 420, 0.22)
        rect(k, 30, 330, 480, 30, (0.46, 0.42, 0.38), 21, lw=3)                                      # the desk top, its front below
        rect(k, 50, 360, 440, 520, (0.20, 0.18, 0.17), 22, lw=3)
        rect(k, 70, 268, 132, 46, (0.80, 0.78, 0.72), 23, lw=2.4)                                    # whose desk it is
        cc.set_source_rgb(*INK); cc.select_font_face("Inter", 0, 1); cc.set_font_size(30)
        e_ = cc.text_extents("DON"); cc.move_to(136 - e_.width / 2 - e_.x_bearing, 302); cc.show_text("DON")
        rect(k, 250, 700, 200, 120, (0.26, 0.23, 0.21), 24, shadow=False, lw=3)                      # the drawer under it, shut
        ellipse(k, 350, 760, 26, 11, n.SILVER, 25, shadow=False, lw=2.4)
        g = m.ease((d - 3) / 6.0)                                         # this one comes out toward us
        fy, fw = 460 + 96 * g, 220 + 60 * g
        if g > 0:                                                         # inside it: the roll
            cut(k, [(240, 452), (460, 452), (350 + fw / 2, fy), (350 - fw / 2, fy)], (0.06, 0.06, 0.07), shadow=False, lw=3)
            cc.save(); cc.new_path(); cc.move_to(240, 452); cc.line_to(460, 452); cc.line_to(350 + fw / 2, fy); cc.line_to(350 - fw / 2, fy)
            cc.close_path(); cc.clip()
            ac.roll(k, 350, 452 + (fy - 452) * 0.62, 1.5 + 0.5 * g, math.pi / 2, ln=110)
            cc.restore()
        rect(k, 350 - fw / 2, fy, fw, 120 + 20 * g, (0.34, 0.30, 0.27), 26, lw=3)                   # its front
        hx, hy = 350, fy + 62 + 10 * g
        ellipse(k, hx, hy, 28, 12, n.SILVER, 27, shadow=False, lw=2.4)
        r_ = m.ease(d / 3.0)                                              # her glove, on the handle
        gx, gy = m.lerp(-120, hx - 6, r_), m.lerp(1010, hy + 8, r_)
        n._seg(k, gx - 170, gy + 210, gx - 10, gy + 18, 96, 84, n.KEY, 3.2)
        ellipse(k, gx, gy, 46, 40, n.KEY, 336, shadow=False, lw=3.2)
        return
    d -= 12
    cc.set_source_rgb(0.10, 0.10, 0.11); cc.paint()
    cut(k, [(30, 250), (510, 250), (540, 800), (0, 800)], (0.30, 0.25, 0.20), shadow=False, lw=4)
    cut(k, [(0, 800), (540, 800), (540, 900), (0, 900)], (0.40, 0.33, 0.26), shadow=False, lw=4)
    ellipse(k, 270, 850, 30, 14, n.SILVER, 8, shadow=False, lw=3)
    if d < 6:                                                             # the roll, whole
        ac.roll(k, 200, 520, 2.6, math.pi / 2, ln=150)
    else:                                                                 # a hand's width of it, unrolled
        f = min(1.0, 0.35 + (d - 6) * 0.22)
        cc.save(); cc.rectangle(280 - 330 * f, 200, 660 * f, 640); cc.clip()
        n.plan_open2(k, 280, 520, 3.3, -0.04)
        cc.restore()
    g = m.ease((d + 1) / 4.0)                                             # her glove
    ox = -220 * (1 - g) + (0 if d < 10 else min(150, (d - 10) * 22))      # in; then her finger goes along the bays to the corner
    tap = -10 if d in (18, 21) else 0
    n._seg(k, -60 + ox * 0.4, 760, 110 + ox, 600 + tap, 96, 84, n.KEY, 3.2)
    n.hand(k, 110 + ox, 600 + tap, 5.0, 1.2, 0.0, flip=-1)


def m6_3(k, tl, dur):
    n, b = m.n, m.b
    d = d12_(tl)
    on = d >= 10                                                          # the desk lamp
    b.office(k, lamp_on=(440, 330) if on else False, frame=False)
    face = "caught" if d < 4 else "interested" if d < 8 else "knowing"
    with m.breath(k, 250, 1270, tl, rate=1.4, amt=0.010, on=d < 8):
        n.star(k, 250, 1270 - (0 if d < 6 else 9), 3.4, "g_down", face, (0.3, 0.2) if d < 6 else (0.3, -0.3), wrap=False, bag=False,
               sparkle=1.0 if on and d % 6 < 3 else 0.0)


def m6_4(k, tl, dur):
    n, b = m.n, m.b
    cc = k.c
    d = d12_(tl)
    b.office(k, lamp_on=(330, 400), frame=False)
    m.clock(k, 470, 132, 28)
    op = d >= 8                                                           # the door opens: light behind him
    cc.set_source_rgb(*((0.50, 0.49, 0.46) if op else (0.09, 0.09, 0.10))); cc.rectangle(-20, 90, 230, 820); cc.fill()
    if not op:
        cc.set_source_rgb(0.30, 0.29, 0.28); cc.set_line_width(5); cc.rectangle(-20, 90, 230, 820); cc.stroke()
    if d >= 9:                                                            # the hat comes round the frame, tipped down at the roll
        n.shadow(k, 40 - 190 * (1 - m.ease((d - 8) / 6.0)), 1040, 1.9, "open", lit_hand=None, look_down=1.0)
    look = (-0.2, 0.7) if d < 7 else (-1.0, 0.1)
    n.star(k, 400, 800, 1.8, "g_down", "knowing", look, wrap=False, bag=False, sparkle=1.0 if d >= 20 and d % 6 < 3 else 0.0)
    cc.set_source_rgb(0.11, 0.10, 0.10); cc.rectangle(170, 650, 420, 330); cc.fill()
    cc.set_source_rgb(0.46, 0.42, 0.38); cc.rectangle(170, 650, 420, 11); cc.fill()
    if d >= 2:                                                            # she lays the roll so its end sticks out, in the light
        ac.roll(k, 236 + 110 * (1 - m.ease((d - 1) / 3.0)), 636, 1.2, math.pi / 2, ln=170)


def m6_5(k, tl, dur):
    n, b = m.n, m.b
    d = d12_(tl)
    b.office(k, lamp_on=(460, 300), frame=False)
    if d < 8:                                                             # one red finger, slowly, once
        curl = (0.0, 0.15, 0.4, 0.7, 1.0, 0.7, 0.4, 0.15)[d % 8]
        n.star(k, 230, 1180, 3.0, "g_beckon3", "knowing", (-1.0, 0.0), wrap=False, curl=curl)
    else:                                                                 # and she holds out her hand
        n.star(k, 230, 1180, 3.0, "g_offer", "knowing", (-1.0, 0.0), wrap=False)


def m6_6(k, tl, dur):
    n, b = m.n, m.b
    cc = k.c
    d = d12_(tl)
    cc.set_source_rgb(0.20, 0.20, 0.22); cc.paint()
    cc.save(); cc.rotate(-0.10)
    for i in range(9):
        cc.set_source_rgba(1, 1, 1, 0.13); cc.rectangle(-80, 80 + i * 44, 520, 18); cc.fill()
    cc.restore()
    b.pool(cc, 300, 600, 380, 0.42)
    b.pool(cc, 60, 300, 300, 0.40)
    n.shadow(k, -6, 1100, 2.3, "open", lit_hand=None, look_down=1.0)
    face, look = ("knowing", (-1.0, 0.0)) if d < 8 else ("knowing", (-1.0, 0.6)) if d < 11 else ("sideeye", (-1.0, 0.6))
    o = n.star(k, 410, 930, 2.3, "g_offer", face, look, wrap=False)
    cc.set_source_rgb(0.14, 0.13, 0.13); cc.rectangle(150, 730, 420, 260); cc.fill()
    cc.set_source_rgb(0.48, 0.44, 0.40); cc.rectangle(150, 730, 420, 12); cc.fill()
    ac.roll(k, 230, 716, 1.15, math.pi / 2, ln=170)
    lx, ly = o["hands"][0]
    n.hand(k, lx + 4, ly + 10, 3.0, -1.35, 0.0, 1)                         # her hand stays in the air
    if d >= 6:                                                            # his hand, the same watch: past hers, to the roll
        g = m.ease((d - 6) / 6.0)
        b.arm_in(k, -40 - 60 * (1 - g), 640 - 60 * (1 - g), m.lerp(-30, 118, g), m.lerp(590, 706, g), 54)


def m6_7a(k, tl, dur):
    """The office door from inside: the handle turns, keys swing in the lock."""
    cc = k.c
    d = d12_(tl)
    cc.set_source_rgb(0.20, 0.20, 0.22); cc.paint()
    cc.set_source_rgb(0.30, 0.29, 0.28); cc.rectangle(60, -20, 420, 1000); cc.fill()
    cc.set_source_rgb(*INK); cc.set_line_width(6); cc.rectangle(60, -20, 420, 1000); cc.stroke()
    cc.set_source_rgb(0.95, 0.94, 0.86); cc.rectangle(60, 930, 420, 40); cc.fill()
    rect(k, 330, 380, 90, 210, (0.62, 0.62, 0.66), 9, lw=3)
    cc.save(); cc.translate(376, 440); cc.rotate(0.55 * m.ease((d - 3) / 4.0))
    rect(k, -150, -16, 170, 32, (0.80, 0.80, 0.84), 10, lw=3)
    cc.restore()
    ellipse(k, 376, 440, 26, 26, (0.70, 0.70, 0.74), 11, shadow=False, lw=3)
    ellipse(k, 376, 536, 13, 18, (0.08, 0.08, 0.09), 12, shadow=False, lw=2)
    cc.set_source_rgb(0.86, 0.80, 0.50); cc.set_line_width(9); cc.set_line_cap(1); cc.move_to(376, 540); cc.line_to(318, 560); cc.stroke()
    cc.set_source_rgb(*INK); cc.set_line_width(5); cc.new_path(); cc.arc(292, 588, 34, 0, 2 * math.pi); cc.stroke()
    sw = 0.30 * math.sin(d * 1.5)
    for i, a in enumerate((1.2, 1.7, 2.3)):
        a += sw * (1 + i * 0.3)
        cc.save(); cc.translate(292 + math.cos(a) * 34, 588 + math.sin(a) * 34); cc.rotate(a - math.pi / 2)
        rect(k, -7, 0, 14, 70, (0.86, 0.80, 0.50), 13 + i, shadow=False, lw=2.4)
        ellipse(k, 0, 0, 13, 13, (0.86, 0.80, 0.50), 16 + i, shadow=False, lw=2.4)
        cc.restore()
    if d % 2 == 0:
        cc.set_source_rgb(1, 1, 1); cc.set_line_width(4)
        for (x0, y0, x1, y1) in ((210, 560, 180, 540), (206, 610, 172, 616), (228, 668, 204, 694)):
            cc.move_to(x0, y0); cc.line_to(x1, y1); cc.stroke()


def m6_7(k, tl, dur):
    n, b = m.n, m.b
    cc = k.c
    d = d12_(tl)
    b.office(k, lamp_on=(300, 330), frame=False)
    wd = 14 + 46 * m.ease((d - 6) / 6.0)                                  # the door, opening: someone has a key
    cc.set_source_rgb(0.86, 0.85, 0.80); cc.rectangle(560 - wd, 120, wd, 760); cc.fill()
    cc.set_source_rgb(0.46, 0.45, 0.43); cc.rectangle(-20, 120, 250, 520); cc.fill()
    n.shadow(k, 130 + (4 if d == 3 else 0), 900, 1.7, co.POSES["open"][:2] + co._ik(1, 104, co.BT + 80), lit_hand=1, look_down=0.6)
    under = d >= 4
    cc.set_source_rgb(0.09, 0.09, 0.10); cc.rectangle(236, 610, 250, 330); cc.fill()
    if d < 2:                                                             # v8: behind the desk, her hand still out
        n.star(k, 404, 940, 2.0, "g_offer", "sideeye", (-1.0, 0.6), wrap=False)
    elif d < 4:                                                           # she has the roll, and goes down with it
        swayed(k, 396 - 14 * (d - 2), 990 + 70 * (d - 2), 7, lambda: n.star(k, 396 - 14 * (d - 2), 990 + 70 * (d - 2), 2.0, "g_hide", "caught",
                                                                               (-1.0, 0.2), wrap=False))
    else:                                                                 # and she is under it
        cc.save(); cc.rectangle(236, 610, 250, 330); cc.clip()
        n.star(k, 360 + (1.5 if d % 2 else -1.5), 1130 - (26 if d == 4 else 0), 2.0, "g_hide", "caught", (1.0, -0.4), wrap=False)
        cc.restore()
    cc.set_source_rgb(0.11, 0.10, 0.10); cc.rectangle(212, 570, 300, 40); cc.fill()
    cc.set_source_rgb(0.46, 0.42, 0.38); cc.rectangle(212, 570, 300, 10); cc.fill()
    cc.set_source_rgb(0.11, 0.10, 0.10); cc.rectangle(212, 610, 24, 330); cc.fill(); cc.rectangle(486, 610, 24, 330); cc.fill()
    if d < 2:                                                             # the roll, under his fingers; then she has it
        ac.roll(k, 300, 556, 1.1, math.pi / 2, ln=150)


# ---------------------------------------------------------------- beat 07: the bang
def m6_2r(k, tl, dur):
    """v11: her face, close, in the lamp's light, the instant the drawer is open: tight, then the win."""
    n, b = m.n, m.b
    cc = k.c
    d = d12_(tl)
    cc.set_source_rgb(0.10, 0.10, 0.11); cc.paint()
    b.pool(cc, 270, 520, 520, 0.30)
    face, look = ("caught", (0.15, 0.95)) if d < 4 else ("knowing", (0.35, 0.75))
    n.star(k, 262 + (0 if d < 4 else 4), 560 + 272 * 3.9 + (6 if d < 4 else 0), 3.9, "g_stand", face, look, wrap=False)


def m7_1r(k, tl, dur):
    """v11: under the desk, close: her eyes over her red glove. She knows the shoes. Wide, and still."""
    n = m.n
    cc = k.c
    d = d12_(tl)
    cc.set_source_rgb(0.30, 0.30, 0.32); cc.paint()
    face = "caught" if d < 3 else "surprised"
    n.star(k, 250 + (1.5 if d % 2 else -1.5) * (d >= 3), 500 + 272 * 4.4, 4.4, "g_hide", face, (0.8, -0.6), wrap=False)
    cc.set_source_rgb(0.04, 0.04, 0.05); cc.rectangle(-20, 0, 600, 150); cc.fill()                  # the desk, above her


def m7_1(k, tl, dur):
    """From under the desk. Restaged from the board's frame so that what happens can be seen: she is smaller and to
    the left, the floor is lighter than his shoes, and his shadow on the wall has its hat below the desk's edge."""
    n, b = m.n, m.b
    cc = k.c
    d = d12_(tl)
    cc.set_source_rgb(0.72, 0.71, 0.68); cc.paint()
    sx_ = 430 + (14 if d >= 10 else 0)
    b.black_fig(k, lambda: co.client(k, sx_, 640, 1.3, "open", "plain", look=(0, 0), roll=False, badge=False))
    b.hat_at(k, sx_ + 3, 640 + (co.HY - 38) * 1.3, 1.65)
    cc.set_source_rgb(0.40, 0.40, 0.42); cc.rectangle(-20, 640, 600, 340); cc.fill()                 # the floor, past the desk
    step = (16 if d >= 14 else 0) + (16 if d >= 19 else 0)                # his shoes: they turn, and go toward the door
    for i, sx in enumerate((318, 410)):
        x0 = sx + step + (0 if i else (8 if d >= 14 else 0))
        if d < 8:                                                         # still toward the desk
            cut(k, [(x0 + 84, 690), (x0 + 14, 690), (x0, 730), (x0 + 84, 730)], n.BLACK, shadow=False, lw=3)
        elif d < 10:
            cut(k, [(x0 + 20, 690), (x0 + 64, 690), (x0 + 70, 730), (x0 + 14, 730)], n.BLACK, shadow=False, lw=3)
        else:
            cut(k, [(x0, 690), (x0 + 70, 690), (x0 + 84, 730), (x0, 730)], n.BLACK, shadow=False, lw=3)
    cc.set_source_rgb(0.04, 0.04, 0.05); cc.rectangle(-20, 0, 600, 96); cc.fill()                    # the desk, above her
    cc.set_source_rgb(0.04, 0.04, 0.05); cc.rectangle(-20, 0, 50, 980); cc.fill()
    n.star(k, 150 + (1.5 if d % 2 else -1.5), 1190, 2.6, "g_hide", "caught", (0.8, -0.6) if d < 10 else (1.0, -0.4), wrap=False)


def m7_2(k, tl, dur):
    """The wall. His shadow, a hand out toward the desk; hers comes on; he backs away, a palm up. They end where the
    match cut needs them: he at 96, she at 466."""
    n, b = m.n, m.b
    d = d12_(tl)
    b.lit_wall(k)
    m.clock(k, 440, 160, 34, sec=m.NOW["sec"])                            # v4: the last seconds
    back = d >= 16                                                        # she is shouting: he gives ground
    pose = (co._ik(-1, -70, co.BT - 10) + co._ik(1, 40, co.BT + 110)) if back else (co._ik(-1, -60, co.BT + 20) + co._ik(1, 30, co.BT + 110))
    swayed(k, 96, 900, (-3 if back else 0) + (1.2 if back and d % 2 else 0), lambda: n.shadow(k, 96, 900, 1.5, pose, lit_hand=None))
    if d >= 4:                                                            # small, curlers, a handbag: she marches on
        g = m.ease((d - 4) / 7.0)
        hop = 7 if d < 11 and d % 2 else 0
        shake = (2.0 if d % 2 else -2.0) if 10 <= d < 33 else 0.0         # the whole of her shouts
        b.mom_shadow(k, 466 + 200 * (1 - g) + shake, 900 - hop, 1.4, up=False)
    TIP["7.2a"] = (None, (300, 282))                                      # over her; over him
    TIP["7.2b"] = (None, (26, 112))


def m7_3(k, tl, dur):
    n, b = m.n, m.b
    cc = k.c
    d = d12_(tl)
    b.lit_wall(k)
    m.clock(k, 440, 160, 34, sec=m.NOW["sec"])                            # v4: midnight, on the pop
    pose = co._ik(-1, -70, co.BT - 10) + co._ik(1, 40, co.BT + 110)
    o = swayed(k, 96, 900, -4 if 2 <= d < 5 else -3 if d < 2 else 0,
               lambda: b.black_fig(k, lambda: co.client(k, 96, 900, 1.5, pose, "plain", look=(0, 0), roll=False, badge=False)))
    hx, hy = 96, 900 + co.HY * 1.5
    if d < 2:
        b.hat_at(k, hx + 3, hy - 38 * 1.5, 1.9)                             # still on
    else:                                                                 # off, and up
        f = min(1.0, (d - 1) / 4.0)
        b.hat_at(k, hx + 3 + 27 * f, hy - 57 - 113 * f - 5 * max(0, d - 5), 1.9, -0.1 + 0.6 * f + 0.04 * max(0, d - 5))
    b.mom_shadow(k, 466, 900, 1.4, up=d >= 1)                             # her other arm, between him and the desk
    if 2 <= d < 7:                                                        # one pop
        cc.set_source_rgb(1, 1, 1)
        cc.save(); cc.translate(190, 486); sc = (1.25, 1.0, 0.9, 0.75, 0.5)[d - 2]; cc.scale(sc, sc)
        cc.new_path()
        for i in range(16):
            r = 64 if i % 2 == 0 else 25
            a = i * math.pi / 8
            (cc.move_to if i == 0 else cc.line_to)(math.cos(a) * r, math.sin(a) * r)
        cc.close_path(); cc.fill_preserve(); cc.set_source_rgb(*INK); cc.set_line_width(4); cc.stroke()
        cc.restore()
    if d in (2, 3):                                                       # a white flash
        cc.set_source_rgba(1, 1, 1, 0.85 if d == 2 else 0.35); cc.paint()


# ---------------------------------------------------------------- beat 08: awake, in colour
FALL = ((0.16, 0.62, 0.86), (0.98, 0.84, 0.25), (0.30, 0.72, 0.45), (0.95, 0.55, 0.20))      # never red: red is hers


def falling(k, tl, floor, nn=16):
    """Confetti still coming down."""
    cc = k.c
    for i in range(nn):
        x = (i * 137 + 40) % 540
        y = ((i * 211) % 900 + tl * (90 + (i % 5) * 22)) % max(200, floor - 20)
        cc.save(); cc.translate(x + 8 * math.sin(tl * 3 + i), y); cc.rotate(i + tl * (2 + i % 3))
        cc.set_source_rgb(*FALL[i % 4]); cc.rectangle(-7, -3, 14, 6); cc.fill()
        cc.restore()


def m8_1(k, tl, dur):
    n, b = m.n, m.b
    cc = k.c
    d = d12_(tl)
    b.party(k, 900)
    m.clock(k, 330, 160, 32, 12, 0, sec=min(59, int(tl)), face=(1.0, 0.98, 0.92))       # v4: just gone twelve
    falling(k, tl, 900)
    with m.lids(co.SKIN, d in (9, 10, 19), line=True):                    # he blinks. He is fine
        o = co.client(k, 96, 900, 1.5, co._ik(-1, -70, co.BT - 10) + co._ik(1, 40, co.BT + 110), "puzzled",
                      look=(0.2, -0.8) if d < 12 else (0.8, -0.3), roll=False)
    hx, hy = o["head"]
    f = min(1.0, d / 12.0)                                                # his paper hat, coming down on him
    n.paper_hat(k, hx + 30 * (1 - f), hy - 260 + 204 * f * f, 1.9, 0.5 * (1 - f) + 0.10 * math.sin(d * 1.1) * (1 - f))
    om = n.mom_up(k, 466, 900, 1.4, False, mouth=m.said("8.1", tl, "EEMEEOOEEEMMEEOEEM"))      # v8: "Happy New Year, dear."
    (lx, ly) = om["hands"][0]
    ux, uy = math.cos(n.AIM), math.sin(n.AIM)
    mx, my = lx + ux * 64 * 1.4, ly + uy * 64 * 1.4
    for t, r in ((2, 11), (-10, 8), (12, 7)):                             # foam at the bottle's mouth
        ellipse(k, mx + t, my - 6 - abs(t) * 0.4 - (d % 3) * 2, r, r * 0.9, (1, 1, 1), 60 + t, shadow=False, lw=1.6)
    if d < 5:                                                             # the cork, on its way out of the picture
        kx, ky = hx + 84 - 34 * d, hy - 96 - 60 * d
        cc.set_source_rgb(*INK); cc.set_line_width(3); cc.set_line_cap(1)
        for dd in (-10, 0, 10):
            cc.move_to(kx + 30 + dd, ky + 46 - dd * 0.4); cc.line_to(kx + 12 + dd, ky + 22 - dd * 0.4); cc.stroke()
        cc.save(); cc.translate(kx, ky); cc.rotate(-0.6 + d * 0.5)
        rect(k, -9, -13, 18, 26, (0.80, 0.66, 0.42), 31, shadow=False, lw=2.4)
        cc.restore()
    mhx, mhy = om["head"]
    TIP["8.1"] = ((mhx - 62, mhy + 44), (210, mhy - 190))


def m8_2(k, tl, dur):
    n, b = m.n, m.b
    d = d12_(tl)
    b.party(k, 760)
    falling(k, tl + 3, 760, 10)
    if d < 6:                                                             # v9: asleep, her head on the table
        with m.breath(k, 270, 1090, tl, rate=1.0, amt=0.012):
            swayed(k, 270, 1090, 9, lambda: n.party(k, 270, 1090 + 170, 2.7, "g_blower", "breath", (0, 0)))
        b.table(k, 800)
        n.doughnut(k, 420, 790, 2.2)
        return
    d -= 6
    dy, rot = ((170, 9), (46, 3), (-14, -1), (4, 0))[d] if d < 4 else (0, 0)      # she jerks upright
    look = (0.7, 0.0) if d < 9 else (0.2, 0.9)                            # the room; then what she is holding
    with m.breath(k, 270, 1090, tl, rate=0.6, amt=0.010, on=d >= 4):
        swayed(k, 270, 1090, rot, lambda: n.party(k, 270, 1090 + dy, 2.7, "g_blower", "caught", look))
    b.table(k, 800)
    n.doughnut(k, 420, 790 - (8 if d == 2 else 0), 2.2)


def m8_3(k, tl, dur):
    n, b = m.n, m.b
    cc = k.c
    d = d12_(tl)
    cc.save(); cc.translate(255, 420); cc.scale(2.0, 2.0); cc.translate(-255, -420)   # v8: her lips and the blower, big
    b.party(k, 760)
    falling(k, tl + 5, 760, 8)
    blow = None if d < 7 else min(1.0, 0.25 + (d - 7) * 0.25) if d < 16 else max(0.55, 1.0 - (d - 15) * 0.09)
    face, look = ("caught", (0.2, 0.9)) if d < 7 else ("caught", (0.9, 0.0)) if d < 13 else ("breath", (0, 0))
    o = n.party(k, 250, 1240, 3.3, "g_blower", face, look, blow=blow)
    if 10 <= d < 15:                                                      # it toots
        (lx, ly), (rx, ry) = o["hands"]
        cc.set_source_rgb(*INK); cc.set_line_width(5); cc.set_line_cap(1)
        for a in (-0.5, -0.1, 0.3):
            x0, y0 = rx + 200 + math.cos(a) * (30 + 6 * (d % 2)), ry - 20 + math.sin(a) * (30 + 6 * (d % 2))
            cc.move_to(x0, y0); cc.line_to(x0 + math.cos(a) * 44, y0 + math.sin(a) * 44); cc.stroke()
    cc.restore()


def m8_4(k, tl, dur):
    n, b = m.n, m.b
    cc = k.c
    d = d12_(tl)
    b.party(k, 800)
    falling(k, tl + 7, 800, 10)
    st.robot(k, 462, 800 - (4 if d in (6, 7) else 0), 1.15, "idle", look=(-1, 0), side=-1)
    with m.lids(co.SKIN, d in (15, 16), line=True):
        o = co.client(k, 110, 800, 1.45, co.POSES["open"][:2] + co._ik(1, 40, co.BT + 40), "warm", look=(0.6, 0.2), roll=False)
    rx, ry = o["hands"][1]
    ellipse(k, rx + 6, ry - 24, 13, 16, (0.80, 0.66, 0.42), 31, shadow=False, lw=2.4)                # the cork
    up = d >= 11                                                          # Don, in a paper crown: the thumb
    Hh = kit.PEOPLE["DON"]["h"]; sy = -300 * Hh + 92
    kit.ARM_POSES["_on2"] = ac._pose(Hh, left=(-58, sy + 50), right=(74, sy - 34) if up else (50, sy + 98))
    try:
        with ac.arms():
            o = dv.don(k, 300, 800 - (7 if d == 11 else 0), 1.7, "_on2", "happy", look=(0, 0.3))
    finally:
        del kit.ARM_POSES["_on2"]
    hx, hy = o["head"]
    cut(k, [(hx - 46, hy - 60), (hx - 46, hy - 104), (hx - 22, hy - 80), (hx, hy - 110), (hx + 22, hy - 80), (hx + 46, hy - 104),
            (hx + 46, hy - 60)], (0.98, 0.84, 0.25), shadow=False, lw=3)
    tx, ty = o["hands"][1]
    skin = kit.PEOPLE["DON"]["skin"]
    if up:                                                                # v9: a thumb: short, fat, leaning back from the fist
        cc.save(); cc.translate(tx - 12, ty - 14); cc.rotate(-0.34)
        rect(k, -16, -40, 32, 46, skin, 36, shadow=False, lw=3.4)
        ellipse(k, 0, -40, 16, 15, skin, 37, shadow=False, lw=3.4)
        cc.set_source_rgb(*skin); cc.rectangle(-13.5, -40, 27, 14); cc.fill()
        cc.set_source_rgb(*INK); cc.set_line_width(2.2); cc.new_path(); cc.arc(0, -42, 9, math.pi * 1.1, math.pi * 1.9); cc.stroke()   # its nail
        cc.restore()
    ellipse(k, tx + 2, ty + 2, 36, 30, skin, 33, shadow=False, lw=3.4)     # the fist, seen from the side: four fingers folded
    cc.set_source_rgb(*INK); cc.set_line_width(2.6); cc.set_line_cap(1)
    for i in range(3):
        cc.move_to(tx + 4, ty - 10 + i * 12); cc.line_to(tx + 34, ty - 8 + i * 12); cc.stroke()
    qx, qy = o["hands"][0]
    n.coupe(k, qx - 2, qy + 12, 1.9)                                       # the coupe he took at the bar
    ellipse(k, qx, qy - 30, 22, 20, skin, 34, shadow=False, lw=3)


def m8_5(k, tl, dur):
    n, b = m.n, m.b
    d = d12_(tl)
    b.party(k, 780)
    look = (-1.0, 0.3) if d < 20 else (-0.4, 0.8)
    n.party(k, 420, 850, 1.7, "g_blower", "caught", look)
    b.table(k, 660 + 40)
    ph = (d % 10) / 10.0                                                  # two strokes of the broom
    stroke = 0.5 - 0.5 * math.cos(2 * math.pi * ph)
    done = (d // 10) + stroke if d < 20 else 2.0
    st.confetti(k, 20 - 34 * done, 800, 380 - 34 * done, 930, n=18, seed=5, s=2.0)
    left = 4 if d < 5 else 3 if d < 7 else 2 if d < 15 else 1 if d < 17 else 0      # v11: her prints in icing sugar, swept up
    m.prints(k, 300, 905, 2.3, 26, range(4 - left, 4))
    n.dustpan(k, 262 - (3 if d == 19 else 0), 935, 2.6, full=d >= 17)
    if 17 <= d < 22:                                                      # the puff out of the pan, as in 3.2
        q = (d - 17) / 5.0
        for i, (dx, r) in enumerate(((-14, 13), (6, 16), (22, 11))):
            k.c.set_source_rgba(1, 1, 1, 0.75 * (1 - q)); k.c.new_path()
            k.c.arc(262 + 1.5 * dx, 890 - 70 * q - i * 9, 1.6 * r * (0.8 + 0.9 * q), 0, 2 * math.pi); k.c.fill()
    with m.talking(kit.PEOPLE["PAM"]["skin"], m.said("8.5", tl, "EAMEEEMMMAFEEUUEEM"), (0.66, 0.20, 0.42)):     # v8: "Some dream. Others sweep."
        o = swayed(k, 170, 940, 1.6 * (stroke - 0.5) if d < 20 else 0.0, lambda: ac.pam(k, 170, 940, 2.2, "stand", (0.2, 0.9)))
    (lx, ly), (rx, ry) = o["hands"]
    n.broom(k, rx + 10, ry - 150, 330 - (70 * stroke if d < 20 else 0), 930, 2.0)
    ellipse(k, rx + 6, ry - 30, 18, 18, kit.PEOPLE["PAM"]["skin"], 35, shadow=False, lw=3)
    hx, hy = o["head"]
    TIP["8.5"] = ((hx - 122, hy + 56), (22, hy - 250))                     # down the outside of her head, to beside her mouth


def m8_6(k, tl, dur):
    """v11: close on her. She looks at Pam (Pam does not look back), looks ahead, shuts her eyes and blows: the blower
    gets half out, and sags. Black."""
    n, b = m.n, m.b
    cc = k.c
    d = d12_(tl)
    if d >= 24:
        cc.set_source_rgb(0, 0, 0); cc.paint(); return
    cc.save(); cc.translate(255, 420); cc.scale(1.45, 1.45); cc.translate(-255, -420)
    b.party(k, 760)
    falling(k, tl + 9, 760, 6)
    if d < 9:
        face, look, blow = "caught", (-1.0, 0.15), None
    elif d < 12:
        face, look, blow = "caught", (0.0, 0.2), None
    else:
        face, look = "breath", (0, 0)
        blow = (None, None, 0.15, 0.32, 0.46, 0.55, 0.55, 0.48, 0.36, 0.24, 0.14, 0.08)[d - 12]
    n.party(k, 255, 1240, 3.3, "g_blower", face, look, blow=blow)
    cc.restore()


WIN = (352, 26, 162, 288)                                 # v12: the window behind her in 8.7, 9:16 like the film


def m8_7(k, tl, dur):
    """v12: the loop. She is asleep again, her head on the table; behind her, the window: the noir street in the rain,
    and a taxi pulling up. The camera goes into the window until the window is the frame: the last drawing is the first
    drawing of 1.1, so the film starts again where it ends."""
    n, b = m.n, m.b
    cc = k.c
    d = d12_(tl)
    last = int(round(dur * 12)) - 1
    g = m.ease(max(0.0, (d - 3) / float(last - 3)))                      # held, then in
    wx, wy, ww, wh = WIN
    x1, y1, w1 = m.lerp(wx, 0, g), m.lerp(wy, 0, g), m.lerp(ww, m.W, g)
    z = w1 / ww
    row = [r for r in m.timing.rows if r["shot"] == "1.1"][0]
    m.TAXI_DX[0] = -440 * (1 - m.ease(min(1.0, d / float(last)))) ** 2   # it comes in from the left and stops in its place
    try:
        street = m.frame(row, (d - last) / 12.0, 0.0)
    finally:
        m.TAXI_DX[0] = 0.0
    if d == last:
        cc.set_source_surface(street, 0, 0); cc.paint(); return
    cc.save(); cc.translate(x1, y1); cc.scale(z, z); cc.translate(-wx, -wy)
    b.party(k, 760)
    falling(k, tl + 11, 760, 6)
    cc.save(); cc.translate(wx, wy); cc.scale(ww / m.W, ww / m.W); cc.set_source_surface(street, 0, 0); cc.paint(); cc.restore()
    a = 1.0 - max(0.0, (d - last + 4) / 4.0)                              # the window's frame goes as it fills the picture
    cc.set_source_rgba(0.98, 0.97, 0.94, a); cc.set_line_width(10); cc.rectangle(wx - 5, wy - 5, ww + 10, wh + 10); cc.stroke()
    with m.breath(k, 270, 1090, tl, rate=1.0, amt=0.012):                  # asleep, as in 8.2
        swayed(k, 270, 1090, 9, lambda: n.party(k, 270, 1090 + 170, 2.7, "g_blower", "breath", (0, 0)))
    b.table(k, 800)
    n.doughnut(k, 420, 790, 2.2)
    cc.restore()


def m8_6_old(k, tl, dur):
    n, b = m.n, m.b
    cc = k.c
    d = d12_(tl)
    z = 1.0 + 2.0 * m.ease((d - 8) / 20.0)                                # the camera goes to the lamp in the window
    cc.save(); cc.translate(470, 240); cc.scale(z, z); cc.translate(-470, -240)
    b.party(k, 900)
    cc.set_source_rgb(0.08, 0.08, 0.11); cc.rectangle(300, 120, 260, 420); cc.fill()
    cc.set_source_rgb(*INK); cc.set_line_width(6); cc.rectangle(300, 120, 260, 420); cc.stroke()
    cc.move_to(430, 120); cc.line_to(430, 540); cc.stroke()
    m.bulbs(k, 300, 128, 560, 128, 30, 9, tl, 1.1, 2)                     # v4: the lights across the window
    cc.save(); cc.rectangle(303, 123, 254, 414); cc.clip()
    g = cairo.RadialGradient(470, 240, 4, 470, 240, 150)
    g.add_color_stop_rgba(0, 1, 0.97, 0.80, 0.95); g.add_color_stop_rgba(1, 1, 0.97, 0.80, 0.0); cc.set_source(g); cc.paint()
    cc.set_source_rgb(0.02, 0.02, 0.03); cc.set_line_width(6); cc.move_to(488, 232); cc.line_to(488, 560); cc.stroke()
    ellipse(k, 470, 240, 13, 9, (1.0, 0.98, 0.86), 2, shadow=False, lw=2)
    cc.set_source_rgba(1, 1, 1, 0.35); cc.set_line_width(1.6)
    for i in range(22):                                                   # rain, falling
        rx, ry = 300 + (i * 53) % 250, 120 + ((i * 89) % 400 + tl * 520) % 420
        cc.move_to(rx, ry); cc.line_to(rx - 8, ry + 30); cc.stroke()
    cc.restore()
    n.party(k, 190, 1230, 3.1, "g_blower", "caught" if d < 6 else "breath", (0.6, 0.2) if d < 6 else (0, 0))     # she shuts her eyes
    cc.restore()


SHOTS = {"6.1": (m6_1, 0, lambda cc: m.b.shade(cc, 1, 0.30)), "6.2": (m6_2, 0, None), "6.2r": (m6_2r, 0, lambda cc: m.b.shade(cc, 1, 0.35)),
         "6.2c": (lambda k, tl, dur: m6_2(k, tl + 1.0, dur), 0, None), "6.4": (m6_4, 0, None), "6.5": (m6_5, 0, lambda cc: m.b.shade(cc, -1, 0.50)), "6.6": (m6_6, -0.07, None), "6.7a": (m6_7a, 0, None),
         "6.7": (m6_7, 0, None), "7.1": (m7_1, 0, None), "7.1r": (m7_1r, 0, None),
         "7.1c": (lambda k, tl, dur: m7_1(k, tl + 10 / 12.0, dur), 0, None), "7.2a": (m7_2, 0, None), "7.2b": (lambda k, tl, dur: m7_2(k, tl + A72, dur), 0, None),
         "7.3": (m7_3, 0, None), "8.1": (m8_1, 0, None), "8.2": (m8_2, 0, None), "8.3": (m8_3, 0, None), "8.4": (m8_4, 0, None),
         "8.5": (m8_5, 0, None), "8.6": (m8_6, 0, None), "8.7": (m8_7, 0, None)}
