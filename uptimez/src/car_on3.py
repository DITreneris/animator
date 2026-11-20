"""OFFICE NOIR 3: Mom's car, v1. A long black 1940s limousine, no real make: a tall chrome grille with vertical bars, a
long bonnet with a centre ridge, separate round lamps on swelling wings, a chrome bumper with over-riders, and on the
grille a chrome curler with wings (her mark, where a mascot would be). No number plate.
  limo_front(k, cx, y0, s, inside)   head on. (cx, y0): the middle of the windscreen's bottom edge. inside: a callable
                                     that draws the driver; it is clipped to the glass.
  limo_side(k, x0, y0, s, inside)    the driver's door from outside. (x0, y0): the window sill's left end. inside is
                                     clipped to the window. Returns the sill's outside point for an arm.
Both are drawn in greys, before the noir pass; the lamps' glare is modest so the driver's face leads the frame."""
import math
import cairo
from kit import INK, cut, ellipse

BODY = (0.07, 0.07, 0.09)
BODY_UP = (0.13, 0.13, 0.16)
CHROME = (0.84, 0.85, 0.88)
CHROME_DARK = (0.50, 0.52, 0.58)
EDGE = (0.44, 0.44, 0.50)


def _path(c, pts):
    c.new_path(); c.move_to(*pts[0])
    for q in pts[1:]:
        c.line_to(*q)
    c.close_path()


def _rr(c, x, y, w, h, r):
    c.new_path(); c.arc(x + r, y + r, r, math.pi, 1.5 * math.pi); c.arc(x + w - r, y + r, r, 1.5 * math.pi, 2 * math.pi)
    c.arc(x + w - r, y + h - r, r, 0, 0.5 * math.pi); c.arc(x + r, y + h - r, r, 0.5 * math.pi, math.pi); c.close_path()


def _fs(c, fill, lw=2.2, ink=INK):
    c.set_source_rgb(*fill); c.fill_preserve(); c.set_source_rgb(*ink); c.set_line_width(lw); c.stroke()


def curler_mascot(c, x, y, s=1.0):
    """A chrome curler with two swept wings, on a short stem."""
    c.save(); c.translate(x, y); c.scale(s, s)
    c.new_path(); c.rectangle(-3, 0, 6, 12); _fs(c, CHROME_DARK, 1.4)
    for sx in (-1, 1):
        _path(c, [(sx * 10, -4), (sx * 44, -22), (sx * 36, -8), (sx * 46, -6), (sx * 34, 2), (sx * 12, 6)]); _fs(c, CHROME, 1.6)
        c.set_source_rgb(*CHROME_DARK); c.set_line_width(1.2)
        c.new_path(); c.move_to(sx * 14, 0); c.line_to(sx * 36, -12); c.stroke()
    _rr(c, -17, -9, 34, 15, 7); _fs(c, CHROME, 1.8)
    c.set_source_rgb(*CHROME_DARK); c.set_line_width(1.0)
    for i in range(1, 6):
        c.new_path(); c.move_to(-17 + i * 5.6, -7); c.line_to(-17 + i * 5.6, 4); c.stroke()
    for sx in (-1, 1):
        c.new_path(); c.arc(sx * 17, -1.5, 5.5, 0, 2 * math.pi); _fs(c, (0.96, 0.96, 0.98), 1.4)
    c.restore()


def limo_front(k, cx, y0, s=1.0, inside=None):
    c = k.c
    c.save(); c.translate(cx, y0); c.scale(s, s)
    _rr(c, -206, -262, 412, 300, 56); _fs(c, BODY, 2.6)                    # the roof and the pillars
    c.set_source_rgb(*EDGE); c.set_line_width(2.4); c.new_path(); c.arc(-150, -206, 50, math.pi, 1.5 * math.pi); c.stroke()
    glass = [(-178, -222), (178, -222), (192, -10), (-192, -10)]
    g = cairo.LinearGradient(0, -222, 0, -10)
    g.add_color_stop_rgba(0, 0.26, 0.26, 0.30, 1); g.add_color_stop_rgba(1, 0.66, 0.66, 0.70, 1)
    _path(c, glass); c.set_source(g); c.fill()
    if inside is not None:
        c.save(); _path(c, glass); c.clip()
        c.save(); c.scale(1 / s, 1 / s); c.translate(-cx, -y0)             # the driver is drawn in the frame's own units
        inside()
        c.restore(); c.restore()
    _path(c, glass); c.set_source_rgb(*CHROME); c.set_line_width(5); c.stroke()
    for sx in (-1, 1):                                                                             # the wipers
        c.set_source_rgb(*INK); c.set_line_width(4); c.set_line_cap(1)
        c.new_path(); c.move_to(sx * 150, -12); c.line_to(sx * 104, -40); c.stroke(); c.set_line_cap(0)
    _path(c, [(-200, -6), (200, -6), (238, 360), (-238, 360)]); _fs(c, BODY, 2.6)                 # the car's front, below the glass
    _path(c, [(-150, -6), (150, -6), (118, 150), (-118, 150)]); _fs(c, BODY_UP, 2.2)              # the long bonnet, coming at us
    c.set_source_rgb(*EDGE); c.set_line_width(2.6); c.new_path(); c.move_to(0, -4); c.line_to(0, 40); c.stroke()   # its ridge
    c.set_line_width(1.8)
    for sx in (-1, 1):
        for i in range(4):
            c.new_path(); c.move_to(sx * (96 - i * 2), 30 + i * 16); c.line_to(sx * (132 - i * 5), 30 + i * 16); c.stroke()   # louvres
    for sx in (-1, 1):                                                                             # the wings
        c.new_path(); c.save(); c.translate(sx * 176, 236); c.scale(86, 128); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        _fs(c, BODY, 2.6)
        c.set_source_rgb(*EDGE); c.set_line_width(2.6)
        c.new_path(); c.save(); c.translate(sx * 176, 236); c.scale(72, 114); c.arc(0, 0, 1, 1.15 * math.pi, 1.85 * math.pi); c.restore(); c.stroke()
    for sx in (-1, 1):                                                                             # the tyres, under the wings
        c.new_path(); c.rectangle(sx * 196 - 30, 300, 60, 110); _fs(c, (0.04, 0.04, 0.05), 2.2)
        c.set_source_rgb(*EDGE); c.set_line_width(1.6)
        for i in range(1, 5):
            c.new_path(); c.move_to(sx * 196 - 30 + i * 12, 304); c.line_to(sx * 196 - 30 + i * 12, 408); c.stroke()
    c.new_path(); c.move_to(-66, 330); c.line_to(-66, 92); c.curve_to(-66, 36, 66, 36, 66, 92); c.line_to(66, 330); c.close_path()
    c.set_source_rgb(0.12, 0.12, 0.14); c.fill_preserve()                                         # the grille
    c.set_source_rgb(*INK); c.set_line_width(11); c.stroke_preserve(); c.set_source_rgb(*CHROME); c.set_line_width(7); c.stroke()
    c.save(); c.new_path(); c.move_to(-62, 330); c.line_to(-62, 92); c.curve_to(-62, 42, 62, 42, 62, 92); c.line_to(62, 330); c.close_path(); c.clip()
    c.set_source_rgb(*CHROME); c.set_line_width(3.2)
    for i in range(-5, 6):
        c.new_path(); c.move_to(i * 11, 40); c.line_to(i * 11, 332); c.stroke()
    c.set_source_rgb(*INK); c.set_line_width(4); c.new_path(); c.move_to(0, 40); c.line_to(0, 332); c.stroke()
    c.set_source_rgb(*CHROME); c.set_line_width(2); c.new_path(); c.move_to(0, 40); c.line_to(0, 332); c.stroke()
    c.restore()
    for sx in (-1, 1):                                                                             # the lamps, and a modest glare
        gx, gy = sx * 150, 176
        gl = cairo.RadialGradient(gx, gy, 20, gx, gy, 96)
        gl.add_color_stop_rgba(0, 1, 1, 1, 0.55); gl.add_color_stop_rgba(1, 1, 1, 1, 0)
        c.set_source(gl); c.new_path(); c.arc(gx, gy, 96, 0, 2 * math.pi); c.fill()
        c.new_path(); c.arc(gx, gy, 40, 0, 2 * math.pi); _fs(c, CHROME, 2.4)
        c.new_path(); c.arc(gx, gy, 31, 0, 2 * math.pi); _fs(c, (0.99, 0.99, 0.97), 1.8)
        c.set_source_rgb(*CHROME_DARK); c.set_line_width(1.4)
        for i in range(-2, 3):
            c.new_path(); c.move_to(gx + i * 10, gy - 28); c.line_to(gx + i * 10, gy + 28); c.stroke()
    _rr(c, -246, 338, 492, 26, 13); _fs(c, CHROME, 2.4)                                           # the bumper
    c.set_source_rgb(1, 1, 1); c.set_line_width(2.4); c.new_path(); c.move_to(-230, 345); c.line_to(230, 345); c.stroke()
    for sx in (-1, 1):
        _rr(c, sx * 92 - 9, 322, 18, 56, 8); _fs(c, CHROME, 2.0)
    curler_mascot(c, 0, 28, 1.6)
    c.restore()


def limo_side(k, x0, y0, s=1.0, inside=None):
    """The driver's door, from outside, the car's nose to screen left."""
    c = k.c
    c.save(); c.translate(x0, y0); c.scale(s, s)
    c.set_source_rgb(*BODY); c.rectangle(-400, -420, 1200, 1000); c.fill()                          # the car fills the frame
    c.set_source_rgb(*EDGE); c.set_line_width(3)                                                   # the roof line, above
    c.new_path(); c.move_to(-400, -340); c.curve_to(-100, -372, 300, -372, 800, -330); c.stroke()
    win = lambda: (c.new_path(), c.move_to(0, 0), c.line_to(0, -238), c.curve_to(0, -292, 40, -300, 70, -300),
                   c.line_to(292, -300), c.curve_to(322, -300, 330, -280, 330, -250), c.line_to(330, 0), c.close_path())
    g = cairo.LinearGradient(0, -300, 0, 0)
    g.add_color_stop_rgba(0, 0.28, 0.28, 0.32, 1); g.add_color_stop_rgba(1, 0.66, 0.66, 0.70, 1)
    win(); c.set_source(g); c.fill()
    if inside is not None:
        c.save(); win(); c.clip()
        c.save(); c.scale(1 / s, 1 / s); c.translate(-x0, -y0)
        inside()
        c.restore(); c.restore()
    win(); c.set_source_rgb(*INK); c.set_line_width(12); c.stroke()
    win(); c.set_source_rgb(*CHROME); c.set_line_width(7); c.stroke()
    c.new_path(); c.move_to(366, -300); c.line_to(366, 0); c.line_to(520, 0); c.line_to(520, -210)   # the rear quarter light
    c.curve_to(520, -270, 480, -300, 440, -300); c.close_path()
    c.set_source_rgb(0.80, 0.80, 0.82); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(10); c.stroke_preserve()
    c.set_source_rgb(*CHROME); c.set_line_width(5); c.stroke()
    c.set_source_rgb(*CHROME_DARK); c.set_line_width(2.4)                                           # its curtain
    for i in range(1, 8):
        c.new_path(); c.move_to(366 + i * 19, -292 + (8 if i > 5 else 0)); c.line_to(366 + i * 19 - 4, -6); c.stroke()
    c.set_source_rgb(*EDGE); c.set_line_width(2.6)                                                 # the door's seams
    c.new_path(); c.move_to(-26, -300); c.line_to(-26, 420); c.stroke()
    c.new_path(); c.move_to(348, -300); c.line_to(348, 420); c.stroke()
    _rr(c, -400, 44, 1200, 12, 6); _fs(c, CHROME, 1.8)                                              # a chrome strip, nose to tail
    _rr(c, 252, 84, 66, 14, 7); _fs(c, CHROME, 1.8)                                                 # the handle
    c.new_path(); c.arc(306, 91, 12, 0, 2 * math.pi); _fs(c, CHROME, 1.8)
    c.new_path(); c.arc(-170, 430, 190, 0, 2 * math.pi); _fs(c, (0.04, 0.04, 0.05), 2.6)           # the front wheel, a white wall
    c.new_path(); c.arc(-170, 430, 150, 0, 2 * math.pi); _fs(c, (0.96, 0.96, 0.94), 2.0)
    c.new_path(); c.arc(-170, 430, 104, 0, 2 * math.pi); _fs(c, (0.06, 0.06, 0.07), 2.0)
    c.new_path(); c.arc(-170, 430, 60, 0, 2 * math.pi); _fs(c, CHROME, 2.0)
    c.new_path(); c.move_to(-400, 232); c.curve_to(-300, 196, -60, 190, 30, 300); c.line_to(60, 420); c.line_to(-400, 420)
    c.close_path(); c.set_source_rgb(*BODY); c.fill()                                               # the wing over it
    c.set_source_rgb(*EDGE); c.set_line_width(2.6)
    c.new_path(); c.move_to(-400, 232); c.curve_to(-300, 196, -60, 190, 30, 300); c.stroke()
    _rr(c, 20, 330, 760, 16, 6); _fs(c, CHROME_DARK, 1.8)                                           # the running board
    c.restore()
    return x0 + 14 * s, y0 - 6 * s
