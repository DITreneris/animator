"""OFFICE NOIR 4: the dream street, v3 (23 Nov). v1 and v2 are pinned (on4_street_v1.py, on4_street_v2.py): drawn from the
first photograph alone, both came out a white, straight, symmetric corridor. v3 is one street from four camera setups,
from Tomas's seven photographs (office-noir-4/ref/on4_street_ref_v1..v7.jpg), as he agreed on 23 Nov:
  A  frame 0, 1.1-1.3   ref v6: a lane bending left between lit cream walls, someone coming down it at us, a lamp high
                        right. At its far end the arch of ref v1, with its string of lights; the florist's heart sign
                        (Valentine's, lesson 40) and the pots with lights of ref v1 along the right-hand houses.
  B  1.4, 2.1           ref v3 (and v2): further up: a tall wall on the left with a lamp on an arm, the gate pillars with
                        their pyramid caps on the right, a lit two-storey house with a little gabled porch at the end, the
                        bell tower black against the sky behind (a ball on top, no cross). The sedan waits at the end.
  C  3.1-3.6            ref v5: the wide street: the crossing (zebra stripes), a double-headed lamp, the long coping wall.
  S  the shadows        ref v4 (and v7): a bare-headed black figure thrown on a wall and folding onto the pavement at the
                        corner; the shadows of the film are drawn this way, with pale gloves as their one mark.
Left out: the graffiti of ref v6 (no readable words on the walls), the grass, the sports fence and the modern white car of
ref v5, the bicycle of ref v1, the electricity box of ref v7.
Look: the walls are lit cream, the sky near black, so after the Office Noir 2 grade (engine_on.TONE v3) the walls are light
grey and anyone in front of them is a dark shape (lesson 47). Accents kept: the neon red (heart, taillights), the bulbs'
gold at 35 %. Then the light: the lamp's pool, the far end bright, the edges dark (lesson 50).
  python3 on4_street.py   -> ../office-noir-4/on4_street_v3_A.png .. _S.png (540x960 at 2x), on4_street_sheet_v3.png"""
import math
import random
import cairo
from kit import Ctx, cut
import engine_on as eng
import on_set as ons

NEON = (0.93, 0.13, 0.22)
GOLD = (0.98, 0.80, 0.36)
INK = (0.06, 0.06, 0.07)
CREAM = (0.90, 0.85, 0.70)
CREAM_SH = (0.66, 0.61, 0.50)
CREAM_FAR = (0.95, 0.90, 0.76)
ROAD = (0.47, 0.44, 0.40)
PAVE = (0.58, 0.55, 0.50)
TILE = (0.40, 0.18, 0.14)
WIN = (0.16, 0.15, 0.15)
WIN_LIT = (0.97, 0.92, 0.75)


# ---- helpers --------------------------------------------------------------------------------------------------------

def poly(k, pts, col, lw=2.2, outline=True):
    cut(k, pts, col, shadow=False, outline=outline, lw=lw)


def lerp(a, b, u):
    return a + (b - a) * u


class Plane:
    """A wall seen in perspective: its near edge (x, top, bottom) and far edge. at(u, v): u 0 near .. 1 far (foreshortened
    by the ratio of the two heights), v 0 top .. 1 bottom."""
    def __init__(self, near, far):
        self.n, self.f = near, far
        self.r = (near[2] - near[1]) / max(1e-6, (far[2] - far[1]))

    def s(self, u):
        return u * self.r / (1 + u * (self.r - 1))

    def at(self, u, v):
        s = self.s(u)
        x = lerp(self.n[0], self.f[0], s)
        top, bot = lerp(self.n[1], self.f[1], s), lerp(self.n[2], self.f[2], s)
        return (x, lerp(top, bot, v))

    def quad(self, u0, u1, v0, v1):
        return [self.at(u0, v0), self.at(u1, v0), self.at(u1, v1), self.at(u0, v1)]

    def fill(self, k, col, lw=2.4):
        poly(k, self.quad(0, 1, 0, 1), col, lw)


def bulb(c, x, y, r):
    g = cairo.RadialGradient(x, y, 0, x, y, r * 4)
    g.add_color_stop_rgba(0, 1, 0.95, 0.8, 0.5); g.add_color_stop_rgba(1, 1, 0.95, 0.8, 0)
    c.set_source(g); c.new_path(); c.arc(x, y, r * 4, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(*GOLD); c.new_path(); c.arc(x, y, r, 0, 2 * math.pi); c.fill()


def lamp_glow(c, x, y, r=150, a=0.9):
    g = cairo.RadialGradient(x, y, 0, x, y, r)
    g.add_color_stop_rgba(0, 1, 1, 0.96, a); g.add_color_stop_rgba(0.10, 1, 1, 0.95, a * 0.65); g.add_color_stop_rgba(1, 1, 1, 0.9, 0)
    c.set_source(g); c.new_path(); c.arc(x, y, r, 0, 2 * math.pi); c.fill()


def lamp_head(k, x, y, s=1.0):
    c = k.c
    poly(k, [(x - 15 * s, y - 10 * s), (x + 15 * s, y - 10 * s), (x + 22 * s, y + 6 * s), (x - 22 * s, y + 6 * s)], INK, 1.6)
    lamp_glow(c, x, y + 10 * s, 150 * s)
    c.set_source_rgb(1, 1, 1); c.save(); c.translate(x, y + 9 * s); c.scale(15 * s, 7 * s); c.new_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()


def heart(c, hx, hy, s, on=True):
    for wd, al in (((20, 0.12), (11, 0.25), (5, 1.0)) if on else ((5, 1.0),)):
        c.new_path(); c.move_to(hx, hy + s * 0.9)
        c.curve_to(hx - s * 1.5, hy - s * 0.2, hx - s * 0.6, hy - s * 1.3, hx, hy - s * 0.45)
        c.curve_to(hx + s * 0.6, hy - s * 1.3, hx + s * 1.5, hy - s * 0.2, hx, hy + s * 0.9)
        c.set_line_width(wd)
        if al < 1:
            c.set_source_rgba(1, 0.4, 0.45, al)
        else:
            c.set_source_rgb(*(NEON if on else (0.35, 0.3, 0.3)))
        c.stroke()


def setts(k, clip_path, y0, y1, xl0, xr0, xl1, xr1, seed=7, dark=0.55):
    """Rows of small paving setts between y0 (far) and y1 (near), widening towards us."""
    c = k.c
    r = random.Random(seed)
    c.save(); clip_path(); c.clip()
    y, row = y0, 0
    while y < y1 + 40:
        u = (y - y0) / (y1 - y0)
        h = 3 + 22 * u ** 1.5
        xl, xr = lerp(xl0, xl1, u), lerp(xr0, xr1, u)
        w = 8 + 46 * u ** 1.3
        c.set_source_rgba(0.16, 0.15, 0.14, dark); c.set_line_width(0.5 + 1.4 * u)
        c.move_to(xl - 40, y); c.line_to(xr + 40, y); c.stroke()
        x = xl - 40 - (w * 0.5 if row % 2 else 0)
        while x < xr + 40:
            c.move_to(x, y); c.line_to(x, y + h); c.stroke()
            x += w * r.uniform(0.92, 1.08)
        y += h; row += 1
    c.restore()


def sky(k):
    c = k.c
    g = cairo.LinearGradient(0, 0, 0, 600)
    g.add_color_stop_rgb(0, 0.02, 0.02, 0.04); g.add_color_stop_rgb(1, 0.10, 0.10, 0.14)
    c.set_source(g); c.paint()


# ---- A: frame 0 (ref v6, the arch of ref v1) -------------------------------------------------------------------------

A_LAMP = (392, 150)            # the loop's join: the counter lamp of 8.2 lands here
A_ARCH = (226, 548, 44, 92)    # the far arch: centre x, floor y, half width, height


def setup_a(k, taillights=False):
    c = k.c
    sky(k)
    poly(k, [(140, 330), (170, 270), (300, 262), (330, 330)], (0.14, 0.12, 0.12))           # roofs over the far end
    poly(k, [(250, 268), (262, 240), (276, 240), (276, 266)], (0.12, 0.11, 0.11))           # a chimney
    cx, fy, hw, h = A_ARCH
    poly(k, [(150, 330), (318, 330), (318, fy + 4), (150, fy + 4)], CREAM_FAR)            # the far end, lit
    top = fy - h
    c.new_path(); c.move_to(cx - hw, fy); c.line_to(cx - hw, top + hw); c.arc(cx, top + hw, hw, math.pi, 0); c.line_to(cx + hw, fy); c.close_path()
    c.set_source_rgb(0.12, 0.11, 0.11); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.4); c.stroke()
    ox = cx + 12                                             # light round the bend beyond the arch
    c.set_source_rgba(0.97, 0.93, 0.82, 0.9)
    c.new_path(); c.move_to(ox - 16, fy - 2); c.line_to(ox - 16, fy - 40); c.arc(ox, fy - 40, 16, math.pi, 0); c.line_to(ox + 16, fy - 2); c.close_path(); c.fill()
    if taillights:
        for dx in (-8, 8):
            c.set_source_rgb(*NEON); c.new_path(); c.arc(ox + dx, fy - 12, 3.2, 0, 2 * math.pi); c.fill()
    n = 19
    for i in range(n):                                       # the string of lights round the arch
        a = math.pi + math.pi * i / (n - 1)
        bulb(c, cx + math.cos(a) * (hw + 6), top + hw + math.sin(a) * (hw + 6), 3.0)
    for j in range(6):
        bulb(c, cx + hw + 6, top + hw + 8 + j * 8, 3.0)
    # the right-hand houses: a long two-storey front receding to the far end
    R = Plane((560, 40, 905), (300, 336, 552))
    R.fill(k, CREAM_SH)
    for i in range(9):
        u = 0.05 + i * 0.105
        for v0, v1 in ((0.20, 0.40), (0.55, 0.75)):
            lit = (i, v0) in ((2, 0.20), (5, 0.55))
            poly(k, R.quad(u, u + 0.045, v0, v1), WIN_LIT if lit else WIN, 1.6)
    poly(k, R.quad(0.0, 1.0, 0.94, 1.0), (0.50, 0.47, 0.42), 1.6)                          # the plinth
    poly(k, [R.at(0, 0), R.at(1, 0), (R.at(1, 0)[0], R.at(1, 0)[1] - 10), (R.at(0, 0)[0] + 30, R.at(0, 0)[1] - 40)], (0.22, 0.12, 0.10), 1.8)
    # the left-hand wall, near and big, lit by the lamp across the lane
    L = Plane((-20, -40, 1010), (150, 328, 556))
    L.fill(k, CREAM)
    poly(k, L.quad(0.0, 0.16, 0.06, 0.42), (0.40, 0.22, 0.16), 2.4)                       # a tall window, brown frame
    poly(k, L.quad(0.015, 0.145, 0.08, 0.40), (0.82, 0.78, 0.66), 1.6)
    c.set_source_rgb(0.40, 0.22, 0.16); c.set_line_width(3)
    a0, a1 = L.at(0.08, 0.08), L.at(0.08, 0.40); c.move_to(*a0); c.line_to(*a1); c.stroke()
    for v in (0.18, 0.29):
        b0, b1 = L.at(0.015, v), L.at(0.145, v); c.move_to(*b0); c.line_to(*b1); c.stroke()
    poly(k, L.quad(0.0, 1.0, 0.86, 1.0), (0.62, 0.58, 0.50), 1.6)                          # the stained base
    for u in (0.45, 0.62, 0.78, 0.90):
        poly(k, L.quad(u, u + 0.035, 0.30, 0.48), WIN, 1.4)
    # the ground: the left pavement, the lane bending left into the arch
    def lane():
        c.new_path(); c.move_to(250, 960); c.line_to(600, 960); c.line_to(600, 905)
        c.curve_to(470, 760, 330, 620, cx + hw + 6, fy + 4); c.line_to(cx - hw, fy + 4)
        c.curve_to(190, 640, 210, 800, 250, 960); c.close_path()
    poly(k, [(-20, 1010), (150, 556), (cx - hw, fy + 4), (190, 640), (210, 800), (250, 960)], PAVE, 2.0)
    lane(); c.set_source_rgb(*ROAD); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.2); c.stroke()
    setts(k, lane, fy + 4, 960, cx - hw, cx + hw + 6, 230, 620)
    c.set_source_rgb(0.30, 0.28, 0.26); c.set_line_width(5)                                 # the kerb
    c.move_to(cx - hw, fy + 4); c.curve_to(190, 640, 210, 800, 250, 960); c.stroke()
    # pots with lights along the foot of the right-hand houses (ref v1)
    r = random.Random(11)
    spots = [(318, 562, 0.30), (350, 592, 0.42), (395, 640, 0.6), (452, 708, 0.85)]
    for x, y, s in spots:
        w, hh = 30 * s, 24 * s
        poly(k, [(x - w / 2, y - hh), (x + w / 2, y - hh), (x + w * 0.38, y), (x - w * 0.38, y)], (0.15, 0.14, 0.14), 1.4)
        for j in range(6):
            a = -math.pi / 2 + r.uniform(-1.0, 1.0); Ln = r.uniform(16, 30) * s
            c.set_source_rgb(0.24, 0.32, 0.22); c.set_line_width(3 * s)
            c.move_to(x, y - hh); c.line_to(x + math.cos(a) * Ln, y - hh + math.sin(a) * Ln); c.stroke()
            c.set_source_rgb(0.80, 0.30, 0.42); c.new_path(); c.arc(x + math.cos(a) * Ln, y - hh + math.sin(a) * Ln, 3.2 * s, 0, 2 * math.pi); c.fill()
    pts = [(cx + hw + 6, fy - 4)] + [(x, y - 8 * s) for x, y, s in spots]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        for u in (0.0, 0.34, 0.67):
            bulb(c, lerp(x0, x1, u), lerp(y0, y1, u) + 3, 2.6 + 3.0 * (lerp(y0, y1, u) - fy) / 200)
    # the florist's heart on its bracket, clear of the windows and the button rail
    bx, by = R.at(0.30, 0.03)
    c.set_source_rgb(*INK); c.set_line_width(3.5); c.move_to(bx, by + 14); c.line_to(bx - 74, by + 22); c.stroke()
    c.set_line_width(2); c.move_to(bx - 60, by + 22); c.line_to(bx - 60, by + 34); c.stroke()
    heart(c, bx - 60, by + 56, 20)
    # the lamp on its bracket off the right-hand houses: the loop's join
    lx, ly = A_LAMP
    c.set_source_rgb(*INK); c.set_line_width(4); c.move_to(560, 100); c.curve_to(480, 100, 430, 120, lx, ly - 12); c.stroke()
    lamp_head(k, lx, ly)


def light_a(c):
    g = cairo.RadialGradient(A_LAMP[0] - 40, 800, 20, A_LAMP[0] - 40, 800, 320)
    g.add_color_stop_rgba(0, 1, 1, 0.95, 0.20); g.add_color_stop_rgba(1, 1, 1, 0.95, 0)
    c.set_source(g); c.rectangle(0, 400, 540, 560); c.fill()
    gr = cairo.LinearGradient(560, 0, 300, 0)
    gr.add_color_stop_rgba(0, 0, 0, 0, 0.55); gr.add_color_stop_rgba(1, 0, 0, 0, 0.05)
    c.set_source(gr); c.rectangle(300, 0, 260, 960); c.fill()
    gb = cairo.LinearGradient(0, 960, 0, 700)
    gb.add_color_stop_rgba(0, 0, 0, 0, 0.45); gb.add_color_stop_rgba(1, 0, 0, 0, 0)
    c.set_source(gb); c.rectangle(0, 700, 540, 260); c.fill()
    ons.key_light(c, A_ARCH[0], A_ARCH[1] - 60, 120, 0.25)
    ons.vignette(c, 0.6)


# ---- B: further up (ref v3, v2) -------------------------------------------------------------------------------------

def setup_b(k, car=True):
    c = k.c
    sky(k)
    tx = 360                                                 # the bell tower, black against the sky; a ball on top
    poly(k, [(tx - 34, 520), (tx - 34, 250), (tx + 34, 250), (tx + 34, 520)], (0.10, 0.10, 0.11), 1.8)
    poly(k, [(tx - 26, 250), (tx - 26, 170), (tx + 26, 170), (tx + 26, 250)], (0.10, 0.10, 0.11), 1.8)
    poly(k, [(tx - 18, 170), (tx, 120), (tx + 18, 170)], (0.10, 0.10, 0.11), 1.8)
    c.set_source_rgb(0.10, 0.10, 0.11); c.new_path(); c.arc(tx, 112, 6, 0, 2 * math.pi); c.fill()
    for (x, y) in ((tx - 14, 200), (tx + 4, 200), (tx - 18, 290), (tx + 8, 290)):
        c.set_source_rgb(*WIN_LIT); c.new_path(); c.move_to(x, y + 34); c.line_to(x, y + 8); c.arc(x + 5, y + 8, 5, math.pi, 0); c.line_to(x + 10, y + 34); c.close_path(); c.fill()
    for i in range(5):                                       # bare trees beside it
        r = random.Random(40 + i); x0 = 420 + i * 28; c.set_source_rgba(0.12, 0.12, 0.14, 0.9); c.set_line_width(1.2)
        for j in range(14):
            c.move_to(x0, 480); c.line_to(x0 + r.uniform(-40, 40), 480 - r.uniform(80, 220)); c.stroke()
    poly(k, [(200, 430), (240, 380), (420, 380), (440, 430)], (0.20, 0.10, 0.08))           # the dark roofs at the end
    poly(k, [(205, 430), (360, 430), (360, 570), (205, 570)], CREAM_FAR)                   # the lit house
    for x in (222, 252, 330):
        for y in (450, 510):
            poly(k, [(x, y), (x + 16, y), (x + 16, y + 34), (x, y + 34)], WIN_LIT if (x, y) == (222, 510) else WIN, 1.4)
    poly(k, [(282, 478), (318, 478), (318, 570), (282, 570)], (0.88, 0.83, 0.70), 1.6)      # the little porch
    poly(k, [(276, 482), (300, 462), (324, 482)], TILE, 1.6)
    c.set_source_rgb(0.12, 0.11, 0.11); c.new_path(); c.move_to(293, 570); c.line_to(293, 512); c.arc(300, 512, 7, math.pi, 0); c.line_to(307, 570); c.close_path(); c.fill()
    L = Plane((-20, -40, 1010), (205, 300, 572))            # left: a tall plain wall, a drainpipe, a lamp on an arm
    L.fill(k, CREAM)
    for u in (0.12, 0.40, 0.62, 0.78):
        poly(k, L.quad(u, u + 0.05, 0.10, 0.30), WIN, 1.4)
        poly(k, L.quad(u, u + 0.05, 0.50, 0.70), WIN_LIT if u == 0.62 else WIN, 1.4)
    p0, p1 = L.at(0.30, 0.0), L.at(0.30, 0.94)
    c.set_source_rgb(0.45, 0.45, 0.45); c.set_line_width(7); c.move_to(*p0); c.line_to(*p1); c.stroke()
    poly(k, L.quad(0.0, 1.0, 0.88, 1.0), (0.60, 0.55, 0.46), 1.6)
    lp = L.at(0.86, 0.30)
    c.set_source_rgb(*INK); c.set_line_width(3); c.move_to(*lp); c.curve_to(lp[0] + 10, lp[1] - 20, lp[0] + 30, lp[1] - 24, lp[0] + 44, lp[1] - 20); c.stroke()
    lamp_head(k, lp[0] + 46, lp[1] - 16, 0.6)
    R = Plane((560, 330, 940), (362, 470, 574))             # right: the long wall, two gate pillars with tiled caps
    R.fill(k, CREAM_SH)
    poly(k, [R.at(0, 0), R.at(1, 0), (R.at(1, 0)[0], R.at(1, 0)[1] - 8), (R.at(0, 0)[0], R.at(0, 0)[1] - 22)], TILE, 1.6)
    for u, w in ((0.10, 0.13), (0.42, 0.10)):
        a, b = R.at(u, 0), R.at(u + w, 0)
        base = R.at(u, 1)[1]
        x0, x1 = b[0], a[0]
        poly(k, [(x0 - 6, a[1] - 40), (x1 + 6, a[1] - 40), (x1 + 6, base), (x0 - 6, base)], CREAM, 2.0)
        for j in range(1, 7):
            yy = lerp(a[1] - 40, base, j / 7.0)
            c.set_source_rgba(0.3, 0.27, 0.22, 0.8); c.set_line_width(1.6); c.move_to(x0 - 6, yy); c.line_to(x1 + 6, yy); c.stroke()
        poly(k, [(x0 - 12, a[1] - 40), (x1 + 12, a[1] - 40), ((x0 + x1) / 2, a[1] - 40 - (x1 - x0) * 0.7)], TILE, 1.8)
        poly(k, [(x0 - 6, base - 30), (x1 + 6, base - 30), (x1 + 6, base), (x0 - 6, base)], (0.55, 0.60, 0.62), 1.4)
    def lane():
        c.new_path(); c.move_to(130, 960); c.line_to(520, 960); c.line_to(355, 576); c.line_to(250, 576); c.close_path()
    poly(k, [(-20, 1010), (205, 572), (250, 576), (130, 960)], PAVE, 2.0)
    poly(k, [(355, 576), (362, 574), (600, 940), (600, 960), (520, 960)], PAVE, 1.6)
    lane(); c.set_source_rgb(*ROAD); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.2); c.stroke()
    setts(k, lane, 576, 960, 250, 355, 130, 520, seed=9)
    if car:                                                  # the sedan waiting at the end, from behind
        cx, cy, s = 300, 572, 0.55
        poly(k, [(cx - 52 * s, cy - 40 * s), (cx + 52 * s, cy - 40 * s), (cx + 58 * s, cy), (cx - 58 * s, cy)], (0.08, 0.08, 0.09), 1.6)
        poly(k, [(cx - 36 * s, cy - 40 * s), (cx - 26 * s, cy - 66 * s), (cx + 26 * s, cy - 66 * s), (cx + 36 * s, cy - 40 * s)], (0.10, 0.10, 0.11), 1.6)
        poly(k, [(cx - 28 * s, cy - 42 * s), (cx - 21 * s, cy - 60 * s), (cx + 21 * s, cy - 60 * s), (cx + 28 * s, cy - 42 * s)], (0.30, 0.30, 0.32), 1.0)
        for dx in (-44, 44):
            c.set_source_rgb(*NEON); c.rectangle(cx + dx * s - 7 * s, cy - 30 * s, 14 * s, 9 * s); c.fill()


def light_b(c):
    gl = cairo.LinearGradient(0, 0, 220, 0)
    gl.add_color_stop_rgba(0, 0, 0, 0, 0.35); gl.add_color_stop_rgba(1, 0, 0, 0, 0)
    c.set_source(gl); c.rectangle(0, 0, 220, 960); c.fill()
    gb = cairo.LinearGradient(0, 960, 0, 650)
    gb.add_color_stop_rgba(0, 0, 0, 0, 0.5); gb.add_color_stop_rgba(1, 0, 0, 0, 0)
    c.set_source(gb); c.rectangle(0, 650, 540, 310); c.fill()
    for dx in (-24, 24):                                     # the taillights' glow, after the grade
        g = cairo.RadialGradient(300 + dx, 556, 0, 300 + dx, 556, 16)
        g.add_color_stop_rgba(0, 1, 0.2, 0.25, 0.45); g.add_color_stop_rgba(1, 1, 0.2, 0.25, 0)
        c.set_source(g); c.new_path(); c.arc(300 + dx, 556, 16, 0, 2 * math.pi); c.fill()
    ons.key_light(c, 290, 520, 160, 0.22)
    ons.vignette(c, 0.6)


# ---- C: the crossing (ref v5) ---------------------------------------------------------------------------------------

def setup_c(k):
    c = k.c
    sky(k)
    poly(k, [(150, 470), (330, 470), (330, 600), (150, 600)], CREAM_FAR)                    # the far lit house
    poly(k, [(140, 470), (180, 430), (320, 430), (340, 470)], (0.24, 0.12, 0.10))
    for x in (172, 220, 286):
        poly(k, [(x, 500), (x + 18, 500), (x + 18, 534), (x, 534)], WIN, 1.4)
    L = Plane((-20, 380, 760), (160, 470, 604))             # left: low houses with tiled roofs
    L.fill(k, CREAM)
    poly(k, [L.at(0, 0), L.at(1, 0), (L.at(1, 0)[0] + 10, L.at(1, 0)[1] - 30), (L.at(0, 0)[0], L.at(0, 0)[1] - 120)], (0.26, 0.13, 0.10), 1.8)
    for u in (0.10, 0.40, 0.62):
        poly(k, L.quad(u, u + 0.08, 0.30, 0.60), WIN, 1.4)
    poly(k, L.quad(0.18, 0.30, 0.38, 1.0), (0.30, 0.22, 0.18), 1.6)                       # a big wooden door
    R = Plane((560, 420, 830), (340, 540, 604))             # right: the long wall with its tiled coping
    R.fill(k, CREAM_SH)
    poly(k, [R.at(0, 0), R.at(1, 0), (R.at(1, 0)[0], R.at(1, 0)[1] - 6), (R.at(0, 0)[0], R.at(0, 0)[1] - 22)], TILE, 1.6)
    poly(k, R.quad(0.0, 1.0, 0.85, 1.0), (0.55, 0.52, 0.46), 1.4)
    px, pb, pt = 372, 700, 300                               # the double-headed lamp
    c.set_source_rgb(*INK); c.set_line_width(6); c.move_to(px, pb); c.line_to(px, pt); c.stroke()
    c.set_line_width(3); c.move_to(px - 50, pt + 6); c.curve_to(px - 20, pt - 12, px + 20, pt - 12, px + 50, pt + 6); c.stroke()
    lamp_head(k, px - 50, pt + 10, 0.6); lamp_head(k, px + 50, pt + 10, 0.6)
    def road():
        c.new_path(); c.move_to(-20, 960); c.line_to(470, 960); c.line_to(330, 606); c.line_to(150, 606); c.close_path()
    road(); c.set_source_rgb(*ROAD); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.2); c.stroke()
    setts(k, road, 606, 960, 150, 330, -20, 470, seed=12)
    poly(k, [(330, 606), (346, 606), (520, 960), (470, 960)], (0.40, 0.37, 0.35), 1.4)       # big cobbles at the edge
    poly(k, [(346, 606), (362, 604), (600, 900), (600, 960), (520, 960)], PAVE, 1.6)         # the pavement
    for i in range(7):                                                                     # the zebra crossing
        x0 = -10 + i * 66
        poly(k, [(x0 + 4, 760), (x0 + 44, 760), (x0 + 44, 830), (x0 - 6, 830)], (0.93, 0.92, 0.88), 1.4)


def light_c(c):
    for x in (322, 422):
        g = cairo.RadialGradient(x, 700, 20, x, 700, 240)
        g.add_color_stop_rgba(0, 1, 1, 0.95, 0.16); g.add_color_stop_rgba(1, 1, 1, 0.95, 0)
        c.set_source(g); c.rectangle(0, 400, 540, 560); c.fill()
    gb = cairo.LinearGradient(0, 960, 0, 820)
    gb.add_color_stop_rgba(0, 0, 0, 0, 0.45); gb.add_color_stop_rgba(1, 0, 0, 0, 0)
    c.set_source(gb); c.rectangle(0, 820, 540, 140); c.fill()
    ons.vignette(c, 0.6)


# ---- S: a shadow (ref v4) -------------------------------------------------------------------------------------------

def setup_s(k):
    """A bare-headed figure thrown on a lit wall, folding at the corner onto the pavement; two pale gloves."""
    c = k.c
    poly(k, [(-20, -20), (560, -20), (560, 300), (-20, 760)], CREAM, 2)
    poly(k, [(-20, 760), (560, 300), (560, 360), (-20, 840)], (0.55, 0.50, 0.42), 1.6)
    poly(k, [(-20, 840), (560, 360), (560, 980), (-20, 980)], PAVE, 2)
    c.set_source_rgba(0.25, 0.23, 0.2, 0.7); c.set_line_width(2)
    for i in range(8):
        c.move_to(-20 + i * 90, 980); c.line_to(150 + i * 90, 760 - i * 60); c.stroke()
    sh = [(250, 380), (230, 410), (232, 450), (210, 480), (150, 520), (140, 560), (160, 590), (210, 590), (238, 600),
          (250, 650), (260, 760), (240, 900), (250, 990), (330, 990), (330, 880), (350, 990), (430, 990), (400, 820),
          (390, 700), (420, 640), (440, 590), (410, 540), (360, 500), (330, 470), (320, 430), (300, 390), (275, 372)]
    c.new_path(); c.move_to(*sh[0])
    for p in sh[1:]:
        c.line_to(*p)
    c.close_path(); c.set_source_rgba(0.05, 0.04, 0.04, 0.92); c.fill()
    for (x, y) in ((150, 575), (432, 610)):                                              # the pale gloves: the one mark
        c.save(); c.translate(x, y); c.scale(16, 12); c.new_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        c.set_source_rgb(0.93, 0.92, 0.88); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2); c.stroke()


def light_s(c):
    ons.vignette(c, 0.55)


# ---- render ---------------------------------------------------------------------------------------------------------

SETUPS = {"A": (setup_a, light_a), "B": (setup_b, light_b), "C": (setup_c, light_c), "S": (setup_s, light_s)}


def render(which="A", scale=2, grade=True, **kw):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540 * scale, 960 * scale)
    s.set_device_scale(scale, scale)
    c = cairo.Context(s)
    draw, lit = SETUPS[which]
    draw(Ctx(c, 0), **kw)
    if grade:
        eng.TONE = "v3"
        eng.accent_pass(s, [(NEON, 1.0), (GOLD, 0.35)])
        c = cairo.Context(s)
        lit(c)
    return s


def overlay(c):
    """The phone's dead zones (bottom quarter, button rail), on the sheet only."""
    c.set_source_rgba(1, 0.2, 0.2, 0.22); c.rectangle(0, 720, 540, 240); c.fill(); c.rectangle(470, 380, 70, 340); c.fill()


def sheet(out="../office-noir-4/on4_street_sheet_v3.png"):
    from PIL import Image
    refs = {"A": ["v6", "v1"], "B": ["v3", "v2"], "C": ["v5"], "S": ["v4"]}
    labels = {"A": "A  frame 0, 1.1-1.3", "B": "B  1.4, 2.1 (the car at the end)", "C": "C  the crossing, 3.1-3.6", "S": "S  how a shadow looks"}
    W_, H_ = 4 * 560 + 20, 70 + 960 + 40 + 300 + 30
    sh = cairo.ImageSurface(cairo.FORMAT_RGB24, W_, H_); c = cairo.Context(sh)
    c.set_source_rgb(0.93, 0.92, 0.89); c.paint()
    c.set_source_rgb(0.1, 0.1, 0.1); c.select_font_face("Inter", 0, 1); c.set_font_size(26)
    c.move_to(20, 42); c.show_text("Office Noir 4: the dream street, v3 (one street, four setups, from Tomas's seven photographs; dead zones in red)")
    x = 20
    for key in "ABCS":
        s = render(key, 1, True)
        c.set_source_surface(s, x, 70); c.paint()
        if key in "ABC":
            c.save(); c.translate(x, 70); overlay(c); c.restore()
        c.set_source_rgb(0.1, 0.1, 0.1); c.select_font_face("Inter", 0, 1); c.set_font_size(18)
        c.move_to(x, 70 + 960 + 28); c.show_text(labels[key])
        rx = x
        for rv in refs[key]:
            im = Image.open("../office-noir-4/ref/on4_street_ref_%s.jpg" % rv).convert("RGB")
            w0, h0 = im.size; sc = 290 / h0
            im = im.resize((int(w0 * sc), 290)); im.save("/tmp/_r.png")
            ri = cairo.ImageSurface.create_from_png("/tmp/_r.png")
            c.set_source_surface(ri, rx, 70 + 960 + 44); c.paint(); rx += ri.get_width() + 10
        x += 560
    sh.write_to_png(out)
    return out


if __name__ == "__main__":
    for key in "ABCS":
        render(key, 2).write_to_png("../office-noir-4/on4_street_v3_%s.png" % key)
    print(sheet())
