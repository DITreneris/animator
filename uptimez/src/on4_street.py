"""OFFICE NOIR 4: the dream street, v4 (23 Nov). v3 is pinned as on4_street_v3.py. v4, Tomas's picks: A and S redrawn;
A's lane bends left with the arch half hidden round the bend; old town in paper cut-out; the shadows are Office Noir 2's
shadow rig, bare-headed, pale-gloved. B and C as in v3.
v3 (23 Nov). v1 and v2 are pinned (on4_street_v1.py, on4_street_v2.py): drawn from the
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
  python3 on4_street.py   -> ../office-noir-4/on4_street_v3_A.png .. _S.png (540x960 at 2x), on4_street_sheet_v4.png"""
import math
import random
import cairo
import kit
from kit import Ctx, cut
import engine_on as eng
import on_set as ons

NEON = (0.93, 0.13, 0.22)
C_POST = ["v4"]                   # v7 (opt-in): the double lamp's post lit
ZEBRA = ["v4"]                    # v5 (23 Nov, opt-in): the stripes flat, in the road's perspective; v6: raised above y 720
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


BLOOM = [1.0]                     # v8 (opt-in, the board review): 0.6 = the lamps' bloom 40% smaller


def lamp_glow(c, x, y, r=150, a=0.9):
    g = cairo.RadialGradient(x, y, 0, x, y, r)
    g.add_color_stop_rgba(0, 1, 1, 0.96, a); g.add_color_stop_rgba(0.10, 1, 1, 0.95, a * 0.65); g.add_color_stop_rgba(1, 1, 1, 0.9, 0)
    c.set_source(g); c.new_path(); c.arc(x, y, r, 0, 2 * math.pi); c.fill()


def lamp_head(k, x, y, s=1.0):
    c = k.c
    poly(k, [(x - 15 * s, y - 10 * s), (x + 15 * s, y - 10 * s), (x + 22 * s, y + 6 * s), (x - 22 * s, y + 6 * s)], INK, 1.6)
    lamp_glow(c, x, y + 10 * s, 150 * s * BLOOM[0])
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


# ---- A: frame 0, v4 (ref v6: the lane bends left; the arch of ref v1 half hidden round the bend) -----------------------
# Tomas's picks (23 Nov): the lane bends left out of sight; the arch with its lights shows round the bend; old town in paper
# cut-out (crooked edges, fallen plaster, a stained base, tiled roof edges, frames and sills, drainpipes).

NIGHT = [False]               # (24 Nov, review of the animation stills) the street darker, the light pooled under the lamp
A_LAMP = (396, 150)            # the loop's join: the counter lamp of 8.2 lands here
A_ARCH = (206, 560, 50, 104)   # the arch at the bend: centre x, floor y, half width, height (its left half behind the wall)
A_BEND_X = 196                 # where the left-hand wall's edge hides the lane


def plaster(k, quad_fn, seed, n=10, col=(0.74, 0.69, 0.57), sizes=(0.06, 0.16, 0.03, 0.08)):
    """Patches where the plaster has fallen, drawn on a Plane in its own (u, v)."""
    r = random.Random(seed)
    for _ in range(n):
        u, v = r.uniform(0.02, 0.85), r.uniform(0.05, 0.80)
        du, dv = r.uniform(sizes[0], sizes[1]), r.uniform(sizes[2], sizes[3])
        q = quad_fn(u, u + du, v, v + dv)
        q = [(x + r.uniform(-4, 4), y + r.uniform(-3, 3)) for x, y in q]
        poly(k, q, col, 1.0, outline=False)
        c = k.c; c.set_source_rgba(0.35, 0.30, 0.24, 0.5); c.set_line_width(1.0)
        c.move_to(*q[0])
        for pt in q[1:]:
            c.line_to(*pt)
        c.close_path(); c.stroke()


def stained_base(k, P, seed, top=0.84, col=(0.56, 0.52, 0.44)):
    """A ragged band of damp and grime along the foot of a wall."""
    r = random.Random(seed)
    pts = [P.at(0, 1.0)]
    n = 9
    for i in range(n + 1):
        u = i / n
        pts.append(P.at(u, top + r.uniform(-0.012, 0.012)))
    pts.append(P.at(1, 1.0))
    poly(k, pts, col, 1.2)


def window(k, P, u0, u1, v0, v1, lit=False, frame=(0.36, 0.22, 0.16)):
    """A window with a frame, a sill and a cross bar, on a Plane."""
    poly(k, P.quad(u0 - 0.006, u1 + 0.006, v0 - 0.02, v1 + 0.02), (0.82, 0.78, 0.66), 1.6)      # the reveal
    poly(k, P.quad(u0, u1, v0, v1), WIN_LIT if lit else WIN, 1.4)
    c = k.c
    c.set_source_rgb(*frame); c.set_line_width(2.2)
    m0, m1 = P.at((u0 + u1) / 2, v0), P.at((u0 + u1) / 2, v1); c.move_to(*m0); c.line_to(*m1); c.stroke()
    h0, h1 = P.at(u0, v0 + (v1 - v0) * 0.38), P.at(u1, v0 + (v1 - v0) * 0.38); c.move_to(*h0); c.line_to(*h1); c.stroke()
    poly(k, P.quad(u0 - 0.012, u1 + 0.012, v1 + 0.02, v1 + 0.045), (0.86, 0.83, 0.76), 1.2)     # the sill


def tiles(k, P, seed, depth=26):
    """A tiled roof edge along the top of a Plane: a dark band with a scalloped lower edge."""
    c = k.c
    a, b = P.at(0, 0), P.at(1, 0)
    poly(k, [(a[0], a[1] - depth), (b[0], b[1] - depth * 0.35), b, a], TILE, 1.8)
    n = 22
    c.set_source_rgba(0.2, 0.08, 0.06, 0.9); c.set_line_width(1.2)
    for i in range(n):
        u = i / n
        x, y = P.at(u, 0)
        rr = 2 + 6 * (1 - P.s(u))
        c.new_path(); c.arc(x, y, rr, 0, math.pi); c.stroke()


def drainpipe(k, P, u, v0=0.0, v1=0.96):
    c = k.c
    p0, p1 = P.at(u, v0), P.at(u, v1)
    w = 3 + 5 * (1 - P.s(u))
    c.set_source_rgb(0.42, 0.42, 0.43); c.set_line_width(w); c.move_to(*p0); c.line_to(*p1); c.stroke()
    c.set_source_rgb(*INK); c.set_line_width(1.0); c.move_to(p0[0] - w / 2, p0[1]); c.line_to(p1[0] - w / 2, p1[1]); c.stroke()


def setup_a(k, taillights=False):
    c = k.c
    sky(k)
    import on4_posters as _po; _po.sky(k, "A")              # (24 Nov) a crescent and seven stars, opt-in
    cx, fy, hw, h = A_ARCH
    top = fy - h
    # behind everything: roofs and a chimney over the bend
    poly(k, [(120, 312), (150, 262), (330, 250), (350, 312)], (0.16, 0.08, 0.06))
    poly(k, [(260, 256), (268, 222), (284, 222), (284, 252)], (0.12, 0.11, 0.11))
    # the house at the bend, facing us, lit, with the arch through it
    E = Plane((120, 312, 572), (340, 312, 572))
    poly(k, [(120, 312), (340, 312), (340, fy + 6), (120, fy + 6)], CREAM_FAR)
    plaster(k, E.quad, 21, n=5, col=(0.86, 0.81, 0.68))
    window(k, E, 0.62, 0.70, 0.16, 0.40, lit=True)
    window(k, E, 0.80, 0.88, 0.16, 0.40)
    c.new_path(); c.move_to(cx - hw, fy); c.line_to(cx - hw, top + hw); c.arc(cx, top + hw, hw, math.pi, 0); c.line_to(cx + hw, fy); c.close_path()
    c.set_source_rgb(0.11, 0.10, 0.10); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.4); c.stroke()
    c.set_source_rgba(0.97, 0.93, 0.82, 0.85)                 # light beyond, round the next bend to the right
    ox = cx + 18
    c.new_path(); c.move_to(ox - 18, fy - 2); c.line_to(ox - 18, fy - 44); c.arc(ox, fy - 44, 18, math.pi, 0); c.line_to(ox + 18, fy - 2); c.close_path(); c.fill()
    if taillights:
        for dx in (-8, 8):
            c.set_source_rgb(*NEON); c.new_path(); c.arc(ox + dx, fy - 12, 3.2, 0, 2 * math.pi); c.fill()
    n = 21
    for i in range(n):                                       # the string of lights round the arch, down its right jamb
        a = math.pi + math.pi * i / (n - 1)
        bulb(c, cx + math.cos(a) * (hw + 7), top + hw + math.sin(a) * (hw + 7), 3.2)
    for j in range(7):
        bulb(c, cx + hw + 7, top + hw + 8 + j * 9, 3.2)
    # the right-hand houses: one long front curving left with the lane, in three faces
    curve = [(560, 30, 905), (450, 150, 760), (385, 236, 650), (340, 300, 576)]
    faces = [Plane(curve[i], curve[i + 1]) for i in range(3)]
    shades = [CREAM_SH, (0.72, 0.67, 0.55), (0.80, 0.75, 0.62)]
    for i, (P, col) in enumerate(zip(faces, shades)):
        P.fill(k, col, 2.0)
        plaster(k, P.quad, 30 + i, n=4, col=tuple(v * 0.92 for v in col))
        stained_base(k, P, 40 + i, 0.90)
        tiles(k, P, 50 + i, 30 - i * 8)
        for u0 in (0.18, 0.60):
            window(k, P, u0, u0 + 0.20, 0.18, 0.40, lit=(i, u0) == (1, 0.60))
            window(k, P, u0, u0 + 0.20, 0.55, 0.76, lit=(i, u0) == (2, 0.18))
    drainpipe(k, faces[0], 0.02)
    drainpipe(k, faces[1], 0.98)
    # the ground: the lane bending left under the arch, the pavements
    def lane():
        c.new_path(); c.move_to(236, 960); c.line_to(600, 960); c.line_to(600, 905)
        c.curve_to(470, 780, 360, 620, cx + hw + 2, fy + 6); c.line_to(A_BEND_X, fy + 6)
        c.curve_to(206, 690, 218, 840, 236, 960); c.close_path()
    lane(); c.set_source_rgb(*ROAD); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.2); c.stroke()
    setts(k, lane, fy + 6, 960, A_BEND_X, cx + hw + 2, 236, 600)
    poly(k, [(600, 905), (560, 905), (440, 760), (370, 650), (330, 580), (340, 576), (385, 650), (450, 760), (600, 890)], PAVE, 1.4)
    # pots with lights along the foot of the right-hand houses (ref v1)
    r = random.Random(11)
    spots = [(330, 590, 0.32), (362, 626, 0.45), (408, 690, 0.62), (466, 772, 0.85)]
    for x, y, s in spots:
        w, hh = 30 * s, 24 * s
        poly(k, [(x - w / 2, y - hh), (x + w / 2, y - hh), (x + w * 0.38, y), (x - w * 0.38, y)], (0.15, 0.14, 0.14), 1.4)
        for j in range(6):
            a = -math.pi / 2 + r.uniform(-1.0, 1.0); Ln = r.uniform(16, 30) * s
            c.set_source_rgb(0.24, 0.32, 0.22); c.set_line_width(3 * s)
            c.move_to(x, y - hh); c.line_to(x + math.cos(a) * Ln, y - hh + math.sin(a) * Ln); c.stroke()
            c.set_source_rgb(0.80, 0.30, 0.42); c.new_path(); c.arc(x + math.cos(a) * Ln, y - hh + math.sin(a) * Ln, 3.2 * s, 0, 2 * math.pi); c.fill()
    pts = [(cx + hw + 7, fy - 2)] + [(x, y - 8 * s) for x, y, s in spots]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        for u in (0.0, 0.34, 0.67):
            bulb(c, lerp(x0, x1, u), lerp(y0, y1, u) + 3, 2.6 + 3.0 * (lerp(y0, y1, u) - fy) / 200)
    # the left-hand wall, near and big, curving away: drawn last of the walls, so its edge hides the arch's left half
    L = Plane((-20, -40, 1010), (A_BEND_X, 300, 566))
    L.fill(k, CREAM)
    plaster(k, L.quad, 11, n=9)
    stained_base(k, L, 12, 0.86)
    window(k, L, 0.00, 0.13, 0.06, 0.40, lit=False)
    for u in (0.48, 0.66, 0.82):
        window(k, L, u, u + 0.045, 0.28, 0.46)
    drainpipe(k, L, 0.34)
    poly(k, [(-20, 1010), (A_BEND_X, 566), (A_BEND_X, fy + 6), (206, 690), (218, 840), (236, 960)], PAVE, 1.8)
    c.set_source_rgb(0.30, 0.28, 0.26); c.set_line_width(5)                                 # the kerb
    c.move_to(A_BEND_X, fy + 6); c.curve_to(206, 690, 218, 840, 236, 960); c.stroke()
    # the lamp on its bracket off the right-hand houses: the loop's join
    lx, ly = A_LAMP
    c.set_source_rgb(*INK); c.set_line_width(4); c.move_to(560, 96); c.curve_to(490, 96, 440, 118, lx, ly - 12); c.stroke()
    lamp_head(k, lx, ly)
    # the florist's heart, drawn after the lamp (its glow would grey the neon), bigger, on a bracket off the right-hand houses, clear of the windows and the button rail
    bx, by = faces[1].at(0.05, 0.02)
    c.set_source_rgb(*INK); c.set_line_width(3.5); c.move_to(bx, by + 30); c.line_to(bx - 70, by + 36); c.stroke()
    c.move_to(bx, by + 58); c.line_to(bx - 40, by + 36); c.stroke()
    c.set_line_width(2); c.move_to(bx - 58, by + 36); c.line_to(bx - 58, by + 48); c.stroke()
    heart(c, bx - 58, by + 74, 26)


def light_a(c):
    if NIGHT[0]:                                           # night: everything a quarter darker, except the lamp's pool
        g_ = cairo.RadialGradient(336, 640, 95, 336, 640, 380)
        g_.add_color_stop_rgba(0, 0, 0, 0, 0.0); g_.add_color_stop_rgba(1, 0, 0, 0, 0.34)
        c.set_source(g_); c.paint()
    g = cairo.RadialGradient(A_LAMP[0] - 60, 800, 20, A_LAMP[0] - 60, 800, 320)
    g.add_color_stop_rgba(0, 1, 1, 0.95, 0.20); g.add_color_stop_rgba(1, 1, 1, 0.95, 0)
    c.set_source(g); c.rectangle(0, 400, 540, 560); c.fill()
    gr = cairo.LinearGradient(560, 0, 330, 0)
    gr.add_color_stop_rgba(0, 0, 0, 0, 0.50); gr.add_color_stop_rgba(1, 0, 0, 0, 0.05)
    c.set_source(gr); c.rectangle(330, 0, 230, 960); c.fill()
    gl = cairo.LinearGradient(0, 0, 200, 0)
    gl.add_color_stop_rgba(0, 0, 0, 0, 0.30); gl.add_color_stop_rgba(1, 0, 0, 0, 0.0)
    c.set_source(gl); c.rectangle(0, 0, 200, 960); c.fill()
    gb = cairo.LinearGradient(0, 960, 0, 700)
    gb.add_color_stop_rgba(0, 0, 0, 0, 0.45); gb.add_color_stop_rgba(1, 0, 0, 0, 0)
    c.set_source(gb); c.rectangle(0, 700, 540, 260); c.fill()
    ons.key_light(c, A_ARCH[0] + 20, A_ARCH[1] - 70, 130, 0.25)
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
    if NIGHT[0]:                                           # night: everything a quarter darker, except the lamp's pool
        g_ = cairo.RadialGradient(290, 560, 100, 290, 560, 400)
        g_.add_color_stop_rgba(0, 0, 0, 0, 0.0); g_.add_color_stop_rgba(1, 0, 0, 0, 0.30)
        c.set_source(g_); c.paint()
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
    import on4_posters as _po; _po.sky(k, "C")
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
    if C_POST[0] != "v4":                                    # v7 (Tomas, 23 Nov): the post and its arm lit against the sky,
        c.set_source_rgb(0.62, 0.62, 0.64); c.set_line_width(10)   # so the two heads hang from something (cold viewers read
        c.move_to(px, pb); c.line_to(px, pt); c.stroke()     # them as headlights, eyes, moons)
        c.set_line_width(6); c.move_to(px - 50, pt + 6); c.curve_to(px - 20, pt - 12, px + 20, pt - 12, px + 50, pt + 6); c.stroke()
    c.set_source_rgb(*INK); c.set_line_width(6); c.move_to(px, pb); c.line_to(px, pt); c.stroke()
    c.set_line_width(3); c.move_to(px - 50, pt + 6); c.curve_to(px - 20, pt - 12, px + 20, pt - 12, px + 50, pt + 6); c.stroke()
    lamp_head(k, px - 50, pt + 10, 0.6); lamp_head(k, px + 50, pt + 10, 0.6)
    def road():
        c.new_path(); c.move_to(-20, 960); c.line_to(470, 960); c.line_to(330, 606); c.line_to(150, 606); c.close_path()
    road(); c.set_source_rgb(*ROAD); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.2); c.stroke()
    setts(k, road, 606, 960, 150, 330, -20, 470, seed=12)
    poly(k, [(330, 606), (346, 606), (520, 960), (470, 960)], (0.40, 0.37, 0.35), 1.4)       # big cobbles at the edge
    poly(k, [(346, 606), (362, 604), (600, 900), (600, 960), (520, 960)], PAVE, 1.6)         # the pavement
    if ZEBRA[0] == "v4":
        for i in range(7):                                                                 # the zebra crossing
            x0 = -10 + i * 66
            poly(k, [(x0 + 4, 760), (x0 + 44, 760), (x0 + 44, 830), (x0 - 6, 830)], (0.93, 0.92, 0.88), 1.4)
    elif ZEBRA[0] == "v6":                     # v6 (Tomas's pick, 23 Nov): the crossing raised to y 646-712, above the
        def edge(y):                           # phone's caption zone; seven bands spread across the road's own width
            u = (960 - y) / 354.0
            return -20 + 170 * u, 470 - 140 * u
        c.save(); road(); c.clip()
        for i in range(7):
            pts = []
            for y, a, b in ((646, i / 7.0 + 0.02, i / 7.0 + 0.10), (712, i / 7.0 + 0.02, i / 7.0 + 0.10)):
                l, r = edge(y); pts.append((l + (r - l) * a, y)); pts.append((l + (r - l) * b, y))
            poly(k, [pts[0], pts[1], pts[3], pts[2]], (0.93, 0.92, 0.88), 1.2)
        c.restore()
    else:                                      # v5: flat bands painted on the road, in its perspective (VP 249,400),
        VP = (249, 400)                        # clipped to the road: read as paint, not as blocks standing on it
        c.save(); road(); c.clip()
        f = (750 - VP[1]) / (840 - VP[1])
        for i in range(-1, 9):
            xa, xb = -40 + i * 64, -40 + i * 64 + 40
            pts = [(VP[0] + (xa - VP[0]) * f, 750), (VP[0] + (xb - VP[0]) * f, 750), (xb, 840), (xa, 840)]
            poly(k, pts, (0.93, 0.92, 0.88), 1.2)
        c.restore()


def light_c(c):
    for x in (322, 422):
        g = cairo.RadialGradient(x, 700, 20, x, 700, 240)
        g.add_color_stop_rgba(0, 1, 1, 0.95, 0.16); g.add_color_stop_rgba(1, 1, 1, 0.95, 0)
        c.set_source(g); c.rectangle(0, 400, 540, 560); c.fill()
    gb = cairo.LinearGradient(0, 960, 0, 820)
    gb.add_color_stop_rgba(0, 0, 0, 0, 0.45); gb.add_color_stop_rgba(1, 0, 0, 0, 0)
    c.set_source(gb); c.rectangle(0, 820, 540, 140); c.fill()
    ons.vignette(c, 0.6)


# ---- S: the shadows, v4 (Tomas's pick, 23 Nov: Office Noir 2's shadow rig, bare-headed) --------------------------
# noir2_cast.shadow is the Client's rig masked black with a top hat, his collar and his watch: here the same body is masked
# black with NO hat, no collar, no pin, no watch (those are the Client's), and a pale glove on each of its own hands.
# On a lit wall it also throws its cast shadow (ref v4), skewed onto the wall and folded at the corner.
GLOVE = (0.93, 0.92, 0.88)


def thug(k, x, feet, s=0.5, pose="open", seed=4100, hands=None, lean=0.0):
    """One of the shadows: a black figure, bare-headed, pale gloves. Returns the rig's points.
    hands (opt-in, on4_lying v2): a (left, right) pair of hands_ps shapes; the gloves are then the series' one hand in
    the pale glove colour (wrist, thumb), not ellipses. lean: radians about the feet (bent forward to reach)."""
    import client_ob as co
    c = k.c
    rec = []
    if lean:
        c.save(); c.translate(x, feet); c.rotate(lean); c.translate(-x, -feet)
    if hands:
        import hands_ps as hp
        old = kit.HAND[0]
        def _rec(k_, hx, hy, w, skin, seed_, d, side):
            rec.append((k_.c.get_matrix(), hx, hy, w, d, side))
        kit.HAND[0] = _rec
    try:
        c.push_group()
        o = co.client(k, x, feet, s, pose, "plain", look=(0, 0), roll=False, badge=False, seed=seed)
        body = c.pop_group()
    finally:
        if hands:
            kit.HAND[0] = old
    c.set_source_rgb(0.05, 0.05, 0.06); c.mask(body)
    if hands:
        for i, (m, hx, hy, w, d, side) in enumerate(rec[:2]):
            c.save(); c.set_matrix(m); hp.draw(k, hands[i], hx, hy, w * 1.25, GLOVE, d, -1 if i == 0 else 1); c.restore()
    else:
        for i, (hx, hy) in enumerate(o["hands"]):
            kit.ellipse(k, hx, hy, 13 * s * 2, 11 * s * 2, GLOVE, seed + 7 + i, shadow=False, lw=1.6)
    if lean:
        c.restore()
    if hands:
        o["rec"] = rec[:2]                       # to draw a glove again over what is in front of him (on4_lying v2)
    return o


def cast(k, x, feet, s=0.5, pose="open", skew=-0.55, squash=0.85, alpha=0.75, seed=4100):
    """The thug's shadow thrown on the wall behind: the same body, sheared and darkened, no gloves."""
    import client_ob as co
    c = k.c
    c.push_group()
    c.save(); c.translate(x, feet); c.transform(cairo.Matrix(1, 0, skew, squash, 0, 0)); c.translate(-x, -feet)
    co.client(k, x, feet, s, pose, "plain", look=(0, 0), roll=False, badge=False, seed=seed)
    c.restore()
    body = c.pop_group()
    c.set_source_rgba(0.04, 0.03, 0.03, alpha); c.mask(body)


def setup_s(k):
    """The shadows beside the Client at the series' size: a bare-headed thug, one reaching, one with its cast shadow on a lit
    wall; the Client in colour at the right, so the two can be told apart."""
    import client_ob as co
    c = k.c
    poly(k, [(-20, -20), (560, -20), (560, 760), (-20, 760)], CREAM, 2)                    # a lit wall
    plaster(k, Plane((-20, -20, 760), (560, -20, 760)).quad, 70, n=8)
    poly(k, [(-20, 760), (560, 760), (560, 980), (-20, 980)], PAVE, 2)
    s = 0.62
    cast(k, 120, 760, s, "open", -0.45, 0.9)                                               # its shadow on the wall
    thug(k, 96, 880, s, "open")
    thug(k, 270, 880, s, (-10, 5) + co._ik(1, 150, co.BT + 60))                            # reaching (for a bill, a coat, a lamp)
    co.client(k, 440, 880, s, "stand", "plain", look=(-0.5, 0), roll=False, badge=False)   # the Client, for comparison
    c.select_font_face("Inter", 0, 1); c.set_font_size(15); c.set_source_rgb(0.1, 0.1, 0.1)
    for x, t in ((40, "a shadow, its cast shadow"), (220, "reaching"), (390, "the Client (compare)")):
        c.move_to(x, 940); c.show_text(t)


def light_s(c):
    ons.vignette(c, 0.4)


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


def sheet(out="../office-noir-4/on4_street_sheet_v4.png"):
    from PIL import Image
    refs = {"A": ["v6", "v1"], "B": ["v3", "v2"], "C": ["v5"], "S": ["v4", "v7"]}
    labels = {"A": "A  frame 0, 1.1-1.3", "B": "B  1.4, 2.1 (the car at the end)", "C": "C  the crossing, 3.1-3.6", "S": "S  the shadows (bare-headed, pale gloves)"}
    W_, H_ = 4 * 560 + 20, 70 + 960 + 40 + 300 + 30
    sh = cairo.ImageSurface(cairo.FORMAT_RGB24, W_, H_); c = cairo.Context(sh)
    c.set_source_rgb(0.93, 0.92, 0.89); c.paint()
    c.set_source_rgb(0.1, 0.1, 0.1); c.select_font_face("Inter", 0, 1); c.set_font_size(26)
    c.move_to(20, 42); c.show_text("Office Noir 4: the dream street, v4 (A and S redrawn; one street, four setups, from Tomas's seven photographs; dead zones in red)")
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
        render(key, 2).write_to_png("../office-noir-4/on4_street_v4_%s.png" % key)
    print(sheet())
