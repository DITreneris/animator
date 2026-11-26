"""OFFICE NOIR 5: the alley, set v1 (25 Nov; Tomas, /grill-me on his photo IMG_20261125_192600, a Vilnius back street
at night). The opening (0:00). The hero frame: a figure under the near doorway's canopy, in its pool of light, his
long shadow across the pavement to the kerb. Colour: the photo's split, warm yellow doorway light against a cold
blue night (no grey noir pass; a new look for the series, kept to this module).
The photo is the layout guide only: the van carries no lettering (the real one has a firm's livery).
World = the screen at z=1 (540x960), drawn in the photo's perspective: the vanishing point at VP.
Zones: L the wall and the parked cars (left, one job: depth); R the facade, two doorways (the near one is the hero's
pool of light, the far one the second pool down the street); the road between, dark, for the narration at the top
and the hero's walk in from the bottom.
Reused: street_on3.view (the camera), kit (cut, rect, ellipse), noir2_cast.shadow (the hat silhouette),
on2_motion.glints (copied, not imported: importing another film's module takes it over).
frame(cam, figure=None, t=0) -> a 540x960 surface. CAMS: A1 the street as in the photo, A2 the doorway (hero)."""
import math
import random
import cairo
import kit
import noir2_cast as n2
from kit import Ctx
from street_on3 import view

VP = (300, 352)                                            # where the road ends
SKY_T, SKY_B = (0.04, 0.07, 0.15), (0.13, 0.24, 0.42)
NIGHT = (0.05, 0.06, 0.10)
WARM = (1.0, 0.80, 0.36)
WARM_HI = (1.0, 0.93, 0.66)
FACADE = (0.13, 0.12, 0.13)
DOOR_N = dict(x0=400, x1=512, top=254, foot=416)          # the near doorway: canopy at top, step at foot
DOOR_F = dict(x0=334, x1=366, top=312, foot=368)
CAMS = {"A1": (270, 480, 1.0),
        "A2": (418, 392, 1.85)}


def _poly(c, pts, rgb, a=1.0):
    c.new_path(); c.move_to(*pts[0])
    for p in pts[1:]:
        c.line_to(*p)
    c.close_path(); c.set_source_rgba(*rgb, a); c.fill()


def sky(c):
    g = cairo.LinearGradient(0, 0, 0, 360)
    g.add_color_stop_rgb(0, *SKY_T); g.add_color_stop_rgb(1, *SKY_B)
    c.set_source(g); c.rectangle(-400, -400, 1400, 800); c.fill()
    r = random.Random(5)
    for i in range(7):                                     # torn cloud, lit from below by the town
        x, y = r.uniform(120, 380), r.uniform(60, 300)
        c.save(); c.translate(x, y); c.scale(r.uniform(50, 95), r.uniform(9, 16))
        c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        c.set_source_rgba(0.30, 0.40, 0.58, 0.18); c.fill()


def far_block(c):
    """The block at the street's end: pale, a few warm windows (someone is up)."""
    _poly(c, [(176, 190), (214, 160), (290, 168), (330, 196), (330, 352), (176, 352)], (0.20, 0.23, 0.28))
    _poly(c, [(176, 190), (214, 160), (290, 168), (330, 196)], (0.10, 0.12, 0.16))
    lit = {(1, 0), (3, 0), (2, 4), (4, 3), (0, 5)}
    for row in range(6):
        for col in range(5):
            x, y = 236 + col * 17, 212 + row * 22
            on = (col, row) in lit
            c.rectangle(x, y, 9, 13)
            c.set_source_rgb(*(WARM_HI if on else (0.11, 0.13, 0.17))); c.fill()
            if on:
                g = cairo.RadialGradient(x + 4, y + 6, 2, x + 4, y + 6, 22)
                g.add_color_stop_rgba(0, *WARM, 0.25); g.add_color_stop_rgba(1, *WARM, 0)
                c.set_source(g); c.arc(x + 4, y + 6, 22, 0, 2 * math.pi); c.fill()


def _branch(c, x, y, a, ln, w, depth, r):
    if depth == 0 or ln < 4:
        return
    x2, y2 = x + math.cos(a) * ln, y + math.sin(a) * ln
    c.set_line_width(w); c.move_to(x, y); c.line_to(x2, y2); c.stroke()
    for _ in range(2 if depth > 2 else 3):
        _branch(c, x2, y2, a + r.uniform(-0.55, 0.55), ln * r.uniform(0.62, 0.78), w * 0.66, depth - 1, r)


def trees(c):
    """Bare trees over the wall on the left, black against the sky: claws over the street."""
    c.set_source_rgb(0.02, 0.025, 0.04); c.set_line_cap(1)
    r = random.Random(2)
    c.move_to(-60, 330)                                    # the scrub on the bank, a ragged top
    for i in range(30):
        c.line_to(-60 + i * 11, 300 - r.uniform(0, 34) + i * 0.9)
    c.line_to(290, 345); c.line_to(-60, 345); c.close_path(); c.fill()
    for (x, y, a, ln, w, d, s) in [(150, 312, -1.22, 95, 10, 8, 3), (182, 318, -1.42, 115, 8, 8, 8),
                                   (40, 300, -1.62, 110, 9, 8, 11), (90, 306, -1.35, 90, 7, 7, 17),
                                   (226, 330, -1.05, 60, 4, 7, 13), (0, 296, -1.75, 120, 9, 8, 21)]:
        _branch(c, x, y, a, ln, w, d, random.Random(s))
    c.set_line_cap(0)


def facade(c):
    """The near building on the right, in perspective: its foot runs from the street's end to the bottom right."""
    _poly(c, [(326, -400), (900, -400), (900, 980), (540, 505), (330, 352)], FACADE)
    _poly(c, [(326, -400), (340, -400), (342, 356), (330, 352)], (0.09, 0.09, 0.10))       # its corner, in shade
    c.set_source_rgba(0, 0, 0, 0.30); c.set_line_width(1.5)
    for yy in (-300, -120, 40, 170, 250):                  # floor bands, running to the street's end
        c.move_to(900, yy + (900 - 540) * 0.2); c.line_to(342, VP[1] + (yy - VP[1]) * 0.06 + (yy - VP[1]) * 0.0); c.stroke()
    lit = {(1, 0): (0.92, 0.88, 0.76), (1, 2): (0.92, 0.88, 0.76), (2, 1): (0.55, 0.30, 0.18), (3, 0): (0.92, 0.88, 0.76)}
    for col in range(5):                                   # windows: narrower and closer together toward the end
        f = 0.18 + col * 0.17
        for row in range(3):
            y0, y1 = -230 + row * 150, -150 + row * 150
            pa, pb = (560, y0), (560, y1)
            qa, qb = _toward(pa, 1 - f), _toward(pb, 1 - f)
            ra, rb = _toward(pa, 1 - f - 0.035), _toward(pb, 1 - f - 0.035)
            if qb[1] > 236:
                continue
            _poly(c, [qa, ra, rb, qb], lit.get((col, row), (0.07, 0.07, 0.08)))
    c.set_source_rgb(0.08, 0.08, 0.09); c.set_line_width(3)                               # the drainpipe
    c.move_to(452, 280); c.line_to(452, 440); c.stroke()


def doorway(c, d, glow=1.0):
    """A doorway in the facade, its canopy and the warm light it pours on the step and the pavement."""
    x0, x1, top, foot = d["x0"], d["x1"], d["top"], d["foot"]
    w = x1 - x0
    _poly(c, [(x0 + w * 0.55, top + 8), (x1, top + 8), (x1, foot), (x0 + w * 0.55, foot - w * 0.12)], (0.86, 0.66, 0.30))
    g = cairo.LinearGradient(0, top, 0, foot)
    g.add_color_stop_rgba(0, *WARM_HI, 0.9 * glow); g.add_color_stop_rgba(1, *WARM, 0.35 * glow)
    c.set_source(g); c.rectangle(x0 + w * 0.55, top + 8, w * 0.45, foot - top - 8); c.fill()
    _poly(c, [(x0 - w * 0.05, top), (x1 + 4, top - 3), (x1 + 4, top + 9), (x0 - w * 0.05, top + 12)], (0.80, 0.76, 0.62))
    _poly(c, [(x0 - w * 0.05, top + 12), (x1 + 4, top + 9), (x1 + 4, top + 12), (x0, top + 15)], (0.30, 0.26, 0.20))


def pool(c, d, glow=1.0, r=1.0):
    """The light on the pavement under a doorway, stretched toward the kerb."""
    cx, cy = d["x0"] + (d["x1"] - d["x0"]) * 0.45, d["foot"] + (d["x1"] - d["x0"]) * 0.18
    rad = (d["x1"] - d["x0"]) * 1.25 * r
    c.save(); c.translate(cx, cy); c.rotate(-0.30); c.scale(1.0, 0.42)
    g = cairo.RadialGradient(0, 0, 4, 0, 0, rad)
    g.add_color_stop_rgba(0, *WARM, 0.62 * glow); g.add_color_stop_rgba(0.55, *WARM, 0.26 * glow); g.add_color_stop_rgba(1, *WARM, 0)
    c.set_source(g); c.arc(0, 0, rad, 0, 2 * math.pi); c.fill(); c.restore()


def ground(c):
    """The road and the pavement; the kerb a long diagonal from the street's end down to the bottom."""
    _poly(c, [(VP[0] - 4, VP[1]), (336, VP[1]), (470, 980), (-200, 980), (-200, 400)], (0.09, 0.09, 0.11))
    _poly(c, [(318, VP[1]), (336, VP[1]), (900, 980), (470, 980)], (0.18, 0.16, 0.15))      # the pavement
    _poly(c, [(316, VP[1]), (320, VP[1]), (474, 980), (458, 980)], (0.03, 0.03, 0.04))      # the kerb's dark face
    c.set_source_rgba(0, 0, 0, 0.35); c.set_line_width(1)
    for i in range(1, 16):                                 # pavement slabs, closer together far away
        f = (i / 16.0) ** 1.8
        y = VP[1] + (980 - VP[1]) * f
        xa = 320 + (474 - 320) * f; xb = 336 + (900 - 336) * f
        c.move_to(xa, y); c.line_to(xb, y); c.stroke()
    g = cairo.LinearGradient(0, 640, 0, 960)               # the near road falls into darkness: room for the title
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, 0.8)
    c.set_source(g); c.rectangle(-400, 640, 1400, 400); c.fill()


def wall(c):
    """The retaining wall on the left, under the trees."""
    _poly(c, [(-200, 312), (VP[0] - 6, 342), (VP[0] - 6, 356), (-200, 420)], (0.17, 0.18, 0.16))
    _poly(c, [(-200, 306), (VP[0] - 6, 340), (VP[0] - 6, 343), (-200, 314)], (0.27, 0.28, 0.24))


def _toward(p, f):
    return (p[0] + (VP[0] - p[0]) * f, p[1] + (VP[1] - p[1]) * f)


def car(c, x, foot, h, body=(0.10, 0.10, 0.12), van=False, f_len=0.22):
    """A parked car along the left kerb, its face to us, its right side running to the street's end; h = its height
    at the near end (px). The side's top and bottom edges go to VP."""
    w = h * (1.25 if van else 1.45)
    b0 = (x, foot); t0 = (x, foot - h)
    b1 = _toward(b0, f_len); t1 = _toward(t0, f_len)
    roof = 0.0 if van else 0.30                            # a car's roof sits back from its face
    _poly(c, [b0, b1, t1, (t0[0], t0[1])], tuple(v * 0.82 for v in body))                   # its side
    if not van:                                            # the bonnet, then the windscreen up to the roof
        tb = _toward((x, foot - h * 0.55), f_len * roof)
        _poly(c, [(x - w, foot - h * 0.55), (x, foot - h * 0.55), tb, (tb[0] - w * 0.9, tb[1])], body)
        _poly(c, [(tb[0] - w * 0.86, tb[1]), (tb[0] - w * 0.04, tb[1]), _toward((x - w * 0.10, foot - h), f_len * roof * 1.6),
                  (_toward((x - w * 0.10, foot - h), f_len * roof * 1.6)[0] - w * 0.62, _toward((x - w * 0.10, foot - h), f_len * roof * 1.6)[1])], (0.04, 0.05, 0.08))
    _poly(c, [(x - w, foot - h * 0.08), (x, foot - h * 0.08), (x, foot - h * (1.0 if van else 0.55)), (x - w, foot - h * (1.0 if van else 0.55))], body)
    if van:                                                # its windscreen
        _poly(c, [(x - w * 0.92, foot - h * 0.92), (x - w * 0.08, foot - h * 0.92), (x - w * 0.08, foot - h * 0.62), (x - w * 0.92, foot - h * 0.62)], (0.06, 0.07, 0.10))
        sw0, sw1 = _toward((x, foot - h * 0.92), 0.02), _toward((x, foot - h * 0.62), 0.05)
        _poly(c, [sw0, _toward((x, foot - h * 0.92), 0.06), _toward((x, foot - h * 0.62), 0.06), sw1], (0.06, 0.07, 0.10))
    for side in (-0.84, -0.16):                            # the headlights, off: they catch the doorway's light
        c.save(); c.translate(x + w * side, foot - h * 0.36); c.scale(w * 0.10, h * 0.06); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        c.set_source_rgba(0.95, 0.90, 0.78, 0.75); c.fill()
    c.set_source_rgba(0.80, 0.86, 1.0, 0.30); c.set_line_width(max(1.0, h * 0.025))           # the sky along its top
    c.move_to(*_toward((x, foot - h), 0.0 if van else f_len * 0.45)); c.line_to(*t1); c.stroke()
    for f in (0.12, 0.80):                                 # the near-side wheels
        wx, wy = _toward((x, foot - h * 0.02), f_len * f)
        r = h * (0.13 if van else 0.22) * (1 - f_len * f)
        c.save(); c.translate(wx, wy - r * 0.6); c.scale(r * 0.55, r); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        c.set_source_rgb(0.02, 0.02, 0.02); c.fill()
    c.set_source_rgb(0.02, 0.02, 0.03); c.rectangle(x - w, foot - h * 0.08, w, h * 0.08); c.fill()


def cars(c):
    for (x, foot, h, body) in [(272, 364, 7, (0.30, 0.30, 0.32)), (262, 368, 10, (0.14, 0.14, 0.16)),
                               (246, 376, 15, (0.42, 0.40, 0.40)), (220, 390, 22, (0.24, 0.24, 0.26)),
                               (176, 414, 34, (0.58, 0.60, 0.64)), (110, 452, 52, (0.06, 0.06, 0.08))]:
        car(c, x, foot, h, body)
    car(c, 70, 600, 190, (0.82, 0.82, 0.80), van=True, f_len=0.30)   # the near van, white, no lettering


def glints(c, x0, x1, y0, y1, n_, t, seed=1, a=0.55, rgb=(1, 1, 0.97)):
    """on2_motion.glints (itself on4_weather's), copied, with a colour"""
    d = int(t * 6)
    c.set_line_cap(1)
    for i in range(n_):
        r = random.Random(seed * 131 + i * 17 + (d + i) // 5)
        x = r.uniform(x0, x1); y = r.uniform(y0, y1); g = 0.5 + (y - y0) / max(1.0, y1 - y0)
        c.set_source_rgba(*rgb, a * r.uniform(0.4, 1.0)); c.set_line_width(2.0 * g)
        w = r.uniform(5, 14) * g; c.move_to(x - w, y); c.line_to(x + w, y); c.stroke()
    c.set_line_cap(0)


def figure(k, x, foot, s=0.27, shadow_len=2.4):
    """A man in a hat under the canopy, black against the light behind him; his shadow laid on the pavement toward the
    kerb (lower left), long and thin. noir2_cast.shadow is the series' hat silhouette."""
    c = k.c
    c.save()                                               # the cast shadow: the same silhouette, flattened and skewed
    c.translate(x, foot); c.transform(cairo.Matrix(1, 0, 1.55, -0.38 * shadow_len / 2.4, 0, 0)); c.translate(-x, -foot)
    c.push_group(); n2.shadow(k, x, foot, s, pose="open", lit_hand=None); m = c.pop_group()
    c.set_source_rgba(0.02, 0.02, 0.03, 0.70); c.mask(m); c.restore()
    c.push_group(); n2.shadow(k, x, foot, s, pose="open", lit_hand=None); m = c.pop_group()
    c.save(); c.translate(1.6, 0); c.set_source_rgba(*WARM_HI, 0.9); c.mask(m); c.restore()   # rim light, door side
    c.set_source_rgb(0.015, 0.015, 0.02); c.mask(m)                                          # all black: no lapels


def draw(k, fig=None, t=0.0):
    c = k.c
    c.set_source_rgb(*NIGHT); c.rectangle(-400, -400, 1400, 1800); c.fill()
    sky(c); far_block(c); trees(c); wall(c); facade(c); ground(c)
    doorway(c, DOOR_F, 0.8); doorway(c, DOOR_N, 1.0)
    pool(c, DOOR_F, 0.7, 1.4); pool(c, DOOR_N, 1.0, 1.5)
    glints(c, 360, 540, 430, 640, 10, t, 7, 0.22, WARM_HI)
    cars(c)
    if fig:
        figure(k, *fig)


def frame(cam="A1", fig=None, t=0.0, scale=1):
    cam = CAMS[cam] if isinstance(cam, str) else cam
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, 540 * scale, 960 * scale); c = cairo.Context(s); k = Ctx(c, 0)
    c.scale(scale, scale); c.save(); view(c, *cam); draw(k, fig, t); c.restore()
    return s


if __name__ == "__main__":
    import sys
    for name, cam, fig in [("A1", "A1", None), ("A2", "A2", (446, 424))]:
        frame(cam, fig).write_to_png("/tmp/on5_%s.png" % name)
    print("ok")
