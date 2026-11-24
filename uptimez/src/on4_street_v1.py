"""OFFICE NOIR 4: the dream street, v1 (23 Nov). Stage 3 (look and set). From Tomas's photograph of an Old Town lane at
night (office-noir-4/ref/on4_street_ref_v1.jpg, "include this shot"): a narrow cobbled lane bending right into an arch,
a lamp hanging over the middle, a string of lights round the arch and along the flower pots at the foot of the right-hand
wall, arched windows on the right, a rough plastered wall with a recess on the left, a sign hanging on a bracket.
What it does in script v3:
  1.1-1.3  frame 0 and the 0:01 joke: Pam-Cat towards us in the foreground, Sofia coming down the lane from the arch
  1.4      the shadows run up the lane and through the arch to the taillights beyond it
  the lamp over the lane is the loop's join (8.2: the counter lamp becomes this lamp, in the same place on screen)
  the sign on the bracket is a florist's heart in red neon (Valentine's on mute, lesson 40); the flower pots are its shop's
Left out from the photograph: the bicycle (a prop with no job).
Look: drawn in colour with the kit, then the noir grade of Office Noir 2 (engine_on.TONE v3: true blacks, faces lighter),
keeping two accents: the neon red (the heart; the taillights) and the bulbs' gold at 35 % (Office Noir 1's gold).
Then the light: the lamp's pool on the cobbles, the arch lit from beyond, the left wall darker (noir is light, lesson 50).
  python3 on4_street.py   -> ../office-noir-4/on4_street_v1.png (540x960 at 2x), on4_street_sheet_v1.png"""
import math
import random
import cairo
import numpy as np
import kit
from kit import Ctx, cut
import engine_on as eng
import on_set as ons
import on2_motion as m2

VP = (300, 470)                 # where the lane runs to
ARCH = (300, 575, 92, 150)      # centre x, floor y, half width, height to the crown
LAMP = (276, 62)                # the hanging lamp: the loop's join
NEON = (0.93, 0.13, 0.22)       # the dream's one red: the heart, the taillights
GOLD = (0.98, 0.80, 0.36)       # the bulbs, kept at 35 %
PLASTER_L = (0.80, 0.74, 0.62)
PLASTER_R = (0.86, 0.70, 0.62)
STONE = (0.55, 0.50, 0.45)
COBBLE = (0.45, 0.42, 0.40)
INK = (0.06, 0.06, 0.07)


def _quad(k, pts, col, seed=0, lw=2.4):
    cut(k, pts, col, shadow=False, lw=lw)


def arch(k, glow=True, taillights=False):
    c = k.c
    cx, fy, hw, h = ARCH
    top = fy - h
    # the end wall the arch is cut through
    _quad(k, [(170, 300), (430, 300), (430, fy + 8), (170, fy + 8)], (0.70, 0.62, 0.50))
    # the passage: dark, lit at its far end
    c.new_path(); c.move_to(cx - hw, fy); c.line_to(cx - hw, top + hw); c.arc(cx, top + hw, hw, math.pi, 0); c.line_to(cx + hw, fy); c.close_path()
    g = cairo.LinearGradient(0, top, 0, fy)
    g.add_color_stop_rgb(0, 0.10, 0.09, 0.09); g.add_color_stop_rgb(1, 0.30, 0.27, 0.24)
    c.set_source(g); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(3); c.stroke()
    c.set_source_rgba(0.95, 0.90, 0.78, 0.55)                   # the far opening, light beyond
    c.new_path(); c.move_to(cx - 34, fy - 4); c.line_to(cx - 34, fy - 70); c.arc(cx, fy - 70, 34, math.pi, 0); c.line_to(cx + 34, fy - 4); c.close_path(); c.fill()
    if taillights:
        for dx in (-14, 14):
            c.set_source_rgb(*NEON); c.new_path(); c.arc(cx + dx, fy - 22, 4.5, 0, 2 * math.pi); c.fill()
    # the garland round the arch: bulbs on a wire
    n = 17
    for i in range(n):
        a = math.pi + math.pi * i / (n - 1)
        bx, by = cx + math.cos(a) * (hw + 8), top + hw + math.sin(a) * (hw + 8)
        _bulb(c, bx, by, 3.6, glow, i)
    for j in range(5):                                          # down the right-hand jamb to the pots
        _bulb(c, cx + hw + 8, top + hw + 14 + j * 16, 3.6, glow, 40 + j)


def _bulb(c, x, y, r, glow, i):
    if glow:
        g = cairo.RadialGradient(x, y, 0, x, y, r * 4)
        g.add_color_stop_rgba(0, 1, 0.95, 0.8, 0.5); g.add_color_stop_rgba(1, 1, 0.95, 0.8, 0)
        c.set_source(g); c.new_path(); c.arc(x, y, r * 4, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(*GOLD); c.new_path(); c.arc(x, y, r, 0, 2 * math.pi); c.fill()


def lane(k, rng=None):
    """The cobbled lane: a road bending right into the arch, a strip of large cobbles and a kerb each side."""
    c = k.c
    cx, fy, hw, h = ARCH
    road = [(-40, 960), (600, 960), (cx + hw + 4, fy), (cx - hw - 4, fy)]
    _quad(k, road, (0.52, 0.49, 0.46))
    r = random.Random(7)
    c.save(); c.new_path(); c.move_to(*road[0])
    for p in road[1:]:
        c.line_to(*p)
    c.close_path(); c.clip()
    y = fy + 6
    row = 0
    while y < 980:                                              # rows of setts, bigger as they come nearer
        u = (y - fy) / (960 - fy)
        hgt = 5 + 34 * u ** 1.6
        xl = cx - hw - 4 + ((-40) - (cx - hw - 4)) * u
        xr = cx + hw + 4 + (600 - (cx + hw + 4)) * u
        wdt = 14 + 70 * u ** 1.3
        x = xl - (wdt * 0.5 if row % 2 else 0)
        c.set_source_rgba(0.20, 0.19, 0.18, 0.55); c.set_line_width(0.6 + 1.6 * u)
        c.move_to(xl, y); c.line_to(xr, y); c.stroke()
        while x < xr:
            c.move_to(x, y); c.line_to(x + r.uniform(-1, 1) * u * 3, y + hgt); c.stroke()
            x += wdt * r.uniform(0.9, 1.1)
        y += hgt; row += 1
    c.restore()
    # big round cobbles and the kerbs along both walls
    for side in (-1, 1):
        x_far = cx + side * (hw + 4)
        x_near = -40 if side < 0 else 600
        strip = [(x_far, fy), (x_far + side * 22, fy), (x_near + side * 10 + (0 if side < 0 else 0), 960), (x_near - side * 140, 960)]
        if side < 0:
            strip = [(x_far - 22, fy), (x_far, fy), (90, 960), (-60, 960)]
        else:
            strip = [(x_far, fy), (x_far + 22, fy), (620, 960), (470, 960)]
        _quad(k, strip, (0.40, 0.37, 0.35))
        c.save(); c.new_path(); c.move_to(*strip[0])
        for p in strip[1:]:
            c.line_to(*p)
        c.close_path(); c.clip()
        for i in range(160):
            u = r.random() ** 0.7
            y = fy + (960 - fy) * u
            xa = strip[0][0] + (strip[3][0] - strip[0][0]) * u; xb = strip[1][0] + (strip[2][0] - strip[1][0]) * u
            x = r.uniform(xa, xb); rr = 2 + 12 * u
            c.save(); c.translate(x, y); c.scale(rr, rr * 0.6); c.new_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
            c.set_source_rgb(*[v + r.uniform(-0.06, 0.08) for v in STONE]); c.fill_preserve()
            c.set_source_rgba(0.1, 0.1, 0.1, 0.6); c.set_line_width(0.8); c.stroke()
        c.restore()


def walls(k):
    c = k.c
    cx, fy, hw, h = ARCH
    # left: rough plaster, a deep recess with a doorway, a window high up
    left = [(-10, -10), (190, 230), (cx - hw - 26, fy), (-10, 980)]
    left = [(-10, -10), (200, 250), (200, fy + 2), (cx - hw - 26, fy + 2), (-10, 960)]
    _quad(k, [(-10, -10), (204, 240), (204, fy + 4), (-10, 900)], PLASTER_L)
    r = random.Random(3)
    for i in range(14):                                         # patches where the plaster has fallen: stone underneath
        x, y = r.uniform(10, 180), r.uniform(80, 700)
        w, hh = r.uniform(18, 50), r.uniform(10, 34)
        cut(k, [(x, y), (x + w, y + r.uniform(-4, 4)), (x + w + r.uniform(-6, 6), y + hh), (x + r.uniform(-6, 6), y + hh)],
            (0.66, 0.60, 0.50), shadow=False, outline=False)
    _quad(k, [(40, 520), (150, 560), (150, 780), (40, 830)], (0.30, 0.28, 0.26))                      # the recess
    _quad(k, [(58, 560), (132, 586), (132, 772), (58, 806)], (0.14, 0.13, 0.13))                      # its door, dark
    _quad(k, [(30, 170), (96, 206), (96, 330), (30, 304)], (0.20, 0.22, 0.26))                        # a high window
    _quad(k, [(-10, 900), (204, fy + 4), (cx - hw - 4, fy + 4), (-10, 1000)], (0.62, 0.60, 0.57))     # the pavement
    # right: the warmer facade with arched windows, receding to the arch
    _quad(k, [(396, 250), (550, -10), (550, 960), (396, fy + 4)], PLASTER_R)
    _quad(k, [(396, 250), (430, 300), (430, fy + 8), (396, fy + 4)], (0.76, 0.62, 0.55))
    for (x0, x1, yt, yb) in ((462, 530, 330, 560), (412, 440, 400, 520)):                            # arched windows
        mid = (x0 + x1) / 2; rad = (x1 - x0) / 2
        c.new_path(); c.move_to(x0, yb); c.line_to(x0, yt + rad); c.arc(mid, yt + rad, rad, math.pi, 0); c.line_to(x1, yb); c.close_path()
        c.set_source_rgb(0.96, 0.93, 0.86); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.4); c.stroke()
        c.new_path(); c.move_to(x0 + 6, yb - 6); c.line_to(x0 + 6, yt + rad); c.arc(mid, yt + rad, rad - 6, math.pi, 0); c.line_to(x1 - 6, yb - 6); c.close_path()
        c.set_source_rgb(0.42, 0.30, 0.26); c.fill()
        c.set_source_rgb(0.95, 0.85, 0.62); c.rectangle(mid - 1.5, yt + rad * 0.4, 3, yb - yt - rad * 0.4 - 6); c.fill()
    _quad(k, [(452, 560), (540, 560), (540, 578), (452, 578)], (0.88, 0.85, 0.80))                    # the sill


def pots(k, glow=True):
    """Flower pots at the foot of the right-hand wall, with the string of lights along them."""
    c = k.c
    cx, fy, hw, h = ARCH
    r = random.Random(11)
    spots = [(415, fy + 14, 0.40), (440, fy + 40, 0.55), (468, 680, 0.75), (505, 740, 0.95), (540, 820, 1.15)]
    for i, (x, y, s) in enumerate(spots):
        w, hh = 30 * s, 26 * s
        cut(k, [(x - w / 2, y - hh), (x + w / 2, y - hh), (x + w * 0.38, y), (x - w * 0.38, y)], (0.16, 0.15, 0.15), shadow=False)
        for j in range(7):                                      # leaves and flowers above it
            a = -math.pi / 2 + r.uniform(-1.0, 1.0)
            L = r.uniform(18, 34) * s
            c.set_source_rgb(0.24, 0.32, 0.22); c.set_line_width(3 * s)
            c.move_to(x, y - hh); c.line_to(x + math.cos(a) * L, y - hh + math.sin(a) * L); c.stroke()
            c.set_source_rgb(0.80, 0.30, 0.42); c.new_path(); c.arc(x + math.cos(a) * L, y - hh + math.sin(a) * L, 3.4 * s, 0, 2 * math.pi); c.fill()
    pts = [(cx + hw + 8, fy - 6)] + [(x, y - 10 * s) for x, y, s in spots]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        for u in (0.0, 0.33, 0.66):
            _bulb(c, x0 + (x1 - x0) * u, y0 + (y1 - y0) * u + 4, 3.4 + 2.5 * (y0 - fy) / 300, glow, int(x0 + u * 10))


def heart_sign(k, on=True):
    """The florist's sign on its bracket over the pots: a heart in red neon (the wreath in the photograph)."""
    c = k.c
    c.set_source_rgb(*INK); c.set_line_width(4)
    c.move_to(540, 300); c.line_to(430, 300); c.stroke()
    c.move_to(540, 340); c.line_to(470, 300); c.stroke()
    hx, hy, s = 468, 352, 30
    for wd, al in ((22, 0.10), (12, 0.22), (5, 1.0)) if on else ((5, 1.0),):
        c.new_path(); c.move_to(hx, hy + s * 0.9)
        c.curve_to(hx - s * 1.5, hy - s * 0.2, hx - s * 0.6, hy - s * 1.3, hx, hy - s * 0.45)
        c.curve_to(hx + s * 0.6, hy - s * 1.3, hx + s * 1.5, hy - s * 0.2, hx, hy + s * 0.9)
        c.set_line_width(wd)
        if al < 1:
            c.set_source_rgba(1, 0.4, 0.45, al)
        else:
            c.set_source_rgb(*(NEON if on else (0.35, 0.30, 0.30)))
        c.stroke()
    c.set_source_rgb(*INK); c.set_line_width(2); c.move_to(450, 300); c.line_to(452, 318); c.stroke(); c.move_to(486, 300); c.line_to(484, 318); c.stroke()


def lamp(k, on=True):
    """The lamp on a wire over the lane: the loop's join."""
    c = k.c
    x, y = LAMP
    c.set_source_rgb(*INK); c.set_line_width(2)
    c.move_to(-10, 20); c.line_to(x, y - 14); c.line_to(550, 6); c.stroke()
    cut(k, [(x - 16, y - 14), (x + 16, y - 14), (x + 26, y + 10), (x - 26, y + 10)], (0.08, 0.08, 0.09), shadow=False)
    if on:
        g = cairo.RadialGradient(x, y + 16, 0, x, y + 16, 140)
        g.add_color_stop_rgba(0, 1, 1, 0.96, 0.9); g.add_color_stop_rgba(0.12, 1, 1, 0.95, 0.6); g.add_color_stop_rgba(1, 1, 1, 0.9, 0)
        c.set_source(g); c.new_path(); c.arc(x, y + 16, 140, 0, 2 * math.pi); c.fill()
        c.set_source_rgb(1, 1, 1); c.new_path(); c.save(); c.translate(x, y + 16); c.scale(18, 10); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()


def light(c):
    """After the grade: noir is light. The lamp's pool on the cobbles, the arch's glow, the left wall in shadow, a vignette."""
    g = cairo.RadialGradient(LAMP[0], 760, 30, LAMP[0], 760, 330)
    g.add_color_stop_rgba(0, 1, 1, 0.95, 0.22); g.add_color_stop_rgba(1, 1, 1, 0.95, 0)
    c.set_source(g); c.rectangle(0, 470, 540, 490); c.fill()
    eng.side_light(c, 0, 0, 250, 960, from_left=False, amount=0.0)
    gl = cairo.LinearGradient(0, 0, 230, 0)
    gl.add_color_stop_rgba(0, 0, 0, 0, 0.55); gl.add_color_stop_rgba(1, 0, 0, 0, 0.0)
    c.set_source(gl); c.rectangle(0, 0, 230, 960); c.fill()
    ons.key_light(c, ARCH[0], ARCH[1] - 60, 150, 0.18)
    ons.vignette(c, 0.55)


def street(k, glow=True, taillights=False):
    """The whole set in colour (before the grade)."""
    c = k.c
    c.set_source_rgb(0.05, 0.05, 0.08); c.paint()              # the night sky between the roofs
    arch(k, glow, taillights)
    walls(k)
    lane(k)
    pots(k, glow)
    heart_sign(k)
    lamp(k)


def render(scale=2, grade=True, taillights=False, marks=False):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540 * scale, 960 * scale)
    s.set_device_scale(scale, scale)
    c = cairo.Context(s)
    street(Ctx(c, 0), True, taillights)
    if grade:
        eng.TONE = "v3"
        eng.accent_pass(s, [(NEON, 1.0), (GOLD, 0.35)])
        c = cairo.Context(s); c.scale(1, 1)
        light(c)
    if marks:
        _marks(c)
    return s


def _marks(c):
    """The frame-0 plan: Pam-Cat's mark, Sofia's path, the shadows' way out, the lamp, the dead zones."""
    def lab(t, x, y, sz=15):
        c.select_font_face("Inter", 0, 1); c.set_font_size(sz)
        e = c.text_extents(t); c.set_source_rgba(0, 0, 0, 0.7); c.rectangle(x - 4, y - sz, e.x_advance + 8, sz + 6); c.fill()
        c.set_source_rgb(1, 0.85, 0.2); c.move_to(x, y); c.show_text(t)
    c.set_source_rgba(1, 0.85, 0.2, 0.9); c.set_line_width(3); c.set_dash([10, 6])
    c.new_path(); c.save(); c.translate(250, 880); c.scale(70, 14); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.stroke()
    lab("PAM-CAT (feet, faces us)", 150, 925)
    c.move_to(305, 585); c.curve_to(300, 700, 380, 760, 400, 900); c.stroke()
    lab("SOFIA: from the arch, past Pam, out", 300, 640, 13)
    c.set_source_rgba(0.4, 0.9, 1, 0.9)
    c.move_to(200, 840); c.curve_to(240, 700, 290, 640, 300, 585); c.stroke()
    lab("1.4 the shadows run to the arch", 20, 760, 13)
    c.set_dash([])
    lab("the lamp: the loop's join", 300, 40, 13)
    lab("the heart: Valentine's", 380, 410, 13)
    c.set_source_rgba(1, 0.2, 0.2, 0.25); c.rectangle(0, 720, 540, 240); c.fill()
    c.rectangle(470, 380, 70, 340); c.fill()
    lab("dead zone", 10, 950, 12)


def sheet(out="../office-noir-4/on4_street_sheet_v1.png", ref="../office-noir-4/ref/on4_street_ref_v1.jpg"):
    """The photograph, the set, the set with the frame-0 plan, and the set at phone size (270 px)."""
    W_, H_ = 540 * 3 + 80 + 290, 960 + 150
    sh = cairo.ImageSurface(cairo.FORMAT_RGB24, W_, H_); c = cairo.Context(sh)
    c.set_source_rgb(0.93, 0.92, 0.89); c.paint()
    c.set_source_rgb(0.1, 0.1, 0.1); c.select_font_face("Inter", 0, 1); c.set_font_size(26)
    c.move_to(20, 40); c.show_text("Office Noir 4: the dream street, v1 (from Tomas's photograph, 23 Nov)")
    c.set_font_size(16); c.select_font_face("Inter", 0, 0)
    try:
        from PIL import Image
        im = Image.open(ref).convert("RGB")
        w0, h0 = im.size; scale = min(540 / w0, 960 / h0)
        im = im.resize((int(w0 * scale), int(h0 * scale)))
        im.save("/tmp/_ref.png")
        ri = cairo.ImageSurface.create_from_png("/tmp/_ref.png")
        c.set_source_surface(ri, 20 + (540 - ri.get_width()) / 2, 70); c.paint()
    except Exception as e:
        c.move_to(30, 300); c.show_text("reference not found: %s" % e)
    panels = [(render(1, True), "the set, graded (frame 0's framing)"), (render(1, True, False, True), "frame 0's plan, dead zones in red")]
    x = 20 + 540 + 20
    c.move_to(20, 1060); c.show_text("the photograph")
    for s, lab in panels:
        c.set_source_surface(s, x, 70); c.paint()
        c.set_source_rgb(0.1, 0.1, 0.1); c.move_to(x, 1060); c.show_text(lab)
        x += 540 + 20
    small = render(1, True)
    c.save(); c.translate(x, 70); c.scale(0.5, 0.5); c.set_source_surface(small, 0, 0); c.paint(); c.restore()
    c.set_source_rgb(0.1, 0.1, 0.1); c.move_to(x, 70 + 500); c.show_text("at phone size (270 px)")
    tl = render(1, True, True)
    c.save(); c.translate(x, 600); c.scale(0.3, 0.3); c.set_source_surface(tl, 0, 0); c.paint(); c.restore()
    c.move_to(x, 600 + 300); c.show_text("1.4: taillights in the arch")
    sh.write_to_png(out)
    return out


if __name__ == "__main__":
    render(2).write_to_png("../office-noir-4/on4_street_v1.png")
    print(sheet())
