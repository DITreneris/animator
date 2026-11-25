"""Office Noir 2, the raven at 0:00 (25 Nov, Tomas: "the opening is bad, the leg is drawn badly; I want it like 4,
where the cat leaps, but a raven"; he picked 1A the leg is out, 2A the raven is on the lamp in frame 0 and the last
frame, 3A the beak's axis straight at us).

The leap is built as Office Noir 4's cat (on4_motion.cat_over): one key drawing per drawing, drawn after the grade,
the camera shaken on the lens drawing and the two after it (on4_motion._shake), sizes growing evenly. Nothing in the
repo draws a bird in this style, so the raven itself is new: paper cut-out polygons with an ink outline, as kit.cut.
Noir 2 keeps one red (hers): the raven is black and grey, its eyes pale with a white glint.

Keys, at twelve drawings a second (shot 1.1 is 7 drawings under RAVEN; 1.2 starts two drawings early and holds its
first drawing, so the first shot is still fired at 1.0 s):
  d0-2 perch  on the lamp's roof, still, side on, beak to the frame's middle (about 46 px tall)
  d3   coil   its head turned to us, shoulders up, claws closed on the roof
  d4   launch off the lamp, beak first, down and to the left at us, wings shut (about 150 px)
  d5   head   the head is half the frame: two eyes, the beak's ridge pointing at the lens; wings still shut
  d6   wing   its left wing has covered the left of the frame; the right one is late
  d7   dark   both wings: the frame is feathers
  d8   sweep  (over shot 1.2) the wing tips and the tail go out over the top of the frame
  d9   gone   the street, her standing in it
"""
import math
import cairo

RAVEN = [False]

INK = (0.02, 0.02, 0.03)
BODY = (0.07, 0.07, 0.09)
WING = (0.11, 0.11, 0.13)
EDGE = (0.26, 0.27, 0.30)            # a feather's lit edge
RIM = (0.55, 0.56, 0.60)             # the lamp's light along its back
BEAK = (0.15, 0.15, 0.17)
EYE = (0.80, 0.80, 0.78)
PERCH = (440, 123)                   # the top of the lamp's roof in shot 1.1 (street(k, 668, (440, 150)))


def _poly(c, pts, fill, lw=3.0, ink=INK):
    c.new_path(); c.move_to(*pts[0])
    for p in pts[1:]:
        c.line_to(*p)
    c.close_path(); c.set_source_rgb(*fill); c.fill_preserve()
    if lw:
        c.set_source_rgb(*ink); c.set_line_width(lw); c.set_line_join(1); c.stroke()
    else:
        c.new_path()


def _line(c, a, b, col, lw):
    c.new_path(); c.move_to(*a); c.line_to(*b); c.set_source_rgb(*col); c.set_line_width(lw); c.set_line_cap(1); c.stroke()


def _eye(c, x, y, r, look=(0.0, 0.0)):
    c.new_path(); c.arc(x, y, r, 0, 2 * math.pi); c.set_source_rgb(*EYE); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(max(1.2, r * 0.16)); c.stroke()
    c.new_path(); c.arc(x + look[0] * r * 0.25, y + look[1] * r * 0.25, r * 0.55, 0, 2 * math.pi); c.set_source_rgb(*INK); c.fill()
    c.new_path(); c.arc(x - r * 0.22, y - r * 0.26, r * 0.2, 0, 2 * math.pi); c.set_source_rgb(1, 1, 1); c.fill()


def _feathers(c, x0, y0, x1, y1, n, col=EDGE, lw=2.0):
    """lit feather edges along a line, each a short stroke: the wing's rhythm"""
    for i in range(n):
        u = (i + 0.5) / n
        x, y = x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
        _line(c, (x, y), (x + (y1 - y0) * 0.06, y - (x1 - x0) * 0.06), col, lw)


# ------------------------------------------------------------------ the perch (side on, beak to the left)
def perched(c, x, y, s=0.46, coil=0.0):
    """x, y: its feet on the perch. coil 0..1: it crouches, the shoulders come up and the head turns to us."""
    c.save(); c.translate(x, y); c.scale(s, s); c.translate(0, 6 * coil)
    lift = 14 * coil
    tail = [(14, -34), (40, -8), (66, 10), (70, 22), (52, 18), (30, 2)]
    _poly(c, tail, BODY, 3.4)
    body = [(-30, -58 + 4 * coil), (-8, -68 + 4 * coil), (18, -56), (30, -34), (24, -12), (6, -2), (-14, -4), (-28, -18), (-36, -38)]
    _poly(c, body, BODY, 3.4)
    wing = [(-16, -54 - lift), (12, -60 - lift), (30, -38), (44, -14), (30, -12), (22, -18), (12, -14), (2, -20), (-10, -28)]
    _poly(c, wing, WING, 3.0)
    _feathers(c, 0, -46 - lift * 0.6, 38, -16, 4, EDGE, 2.2)
    _line(c, (-12, -64 - lift * 0.3), (22, -58 - lift), RIM, 3.0)                         # the lamp's light on its back
    for fx in (-8, 4):                                                                     # legs and claws on the roof
        _line(c, (fx, -4), (fx - 2, 0), INK, 4.5)
        for dx in (-9, -2, 6):
            _line(c, (fx - 2, 0), (fx - 2 + dx * (1 - 0.4 * coil), 3 + 3 * coil), INK, 3.2)
    if coil < 0.5:                                                                         # the head, side on
        hx, hy = -34, -64
        _poly(c, [(hx - 14, hy - 4), (hx - 2, hy - 18), (hx + 14, hy - 14), (hx + 18, hy + 2), (hx + 8, hy + 12), (hx - 10, hy + 10)], BODY, 3.2)
        _poly(c, [(hx - 12, hy - 4), (hx - 42, hy + 3), (hx - 12, hy + 6)], BEAK, 3.0)
        _line(c, (hx - 12, hy - 3), (hx - 38, hy + 2), RIM, 1.6)
        _eye(c, hx - 2, hy - 4, 3.6, (-1, 0))
    else:                                                                                   # coil: its face to us
        hx, hy = -26, -70
        _poly(c, [(hx - 18, hy - 2), (hx - 10, hy - 18), (hx + 10, hy - 18), (hx + 18, hy - 2), (hx + 12, hy + 14), (hx - 12, hy + 14)], BODY, 3.2)
        _poly(c, [(hx - 7, hy + 1), (hx + 7, hy + 1), (hx, hy + 22)], BEAK, 2.8)            # the beak, end on: short
        _line(c, (hx, hy + 2), (hx, hy + 16), RIM, 1.6)
        for ex in (-9, 9):
            _eye(c, hx + ex, hy - 5, 4.6)
        _line(c, (hx - 15, hy - 14), (hx - 4, hy - 9), INK, 2.6)                              # brows down
        _line(c, (hx + 15, hy - 14), (hx + 4, hy - 9), INK, 2.6)
    c.restore()


# ------------------------------------------------------------------ the launch (3/4 front, coming down at us)
def _hackles(c, cx, cy, w, h, lw=3.0):
    """a raven's throat: shaggy pointed feathers under the beak (what makes it a raven and not a crow or an owl)"""
    n = 6
    pts = [(cx - w, cy)]
    for i in range(n):
        x0 = cx - w + (2 * w) * (i + 0.5) / n
        pts += [(x0, cy + h * (0.8 + 0.2 * ((i * 7) % 3) / 2.0)), (cx - w + (2 * w) * (i + 1) / n, cy + h * 0.35)]
    pts += [(cx + w, cy)]
    _poly(c, pts, BODY, lw)


def launch(c, x, y, R):
    """x, y: the middle of its head; R: the head's radius. Wings shut along a heavy body that trails up and right,
    back to the lamp; the beak first, at us and down."""
    c.save(); c.translate(x, y); c.scale(R / 40.0, R / 40.0)
    _poly(c, [(40, -60), (92, -104), (104, -92), (98, -78), (60, -40)], BODY, 3.4)                     # the tail, short, behind
    _poly(c, [(-34, 0), (-20, -40), (20, -66), (60, -70), (74, -46), (56, -6), (20, 30), (-14, 34)], BODY, 3.6)   # the body
    _poly(c, [(-6, -40), (30, -62), (62, -64), (72, -46), (58, -16), (34, -6), (10, -14)], WING, 3.2)   # a shut wing on it
    _feathers(c, 20, -40, 60, -54, 4, EDGE, 2.6)
    _line(c, (-12, -44), (52, -72), RIM, 3.4)
    _hackles(c, -4, 18, 20, 14)
    _poly(c, [(-34, -4), (-30, -30), (-6, -42), (20, -36), (30, -12), (22, 16), (-4, 24), (-26, 16)], BODY, 3.6)  # the head
    _poly(c, [(-20, 0), (14, -4), (6, 14), (-12, 52), (-22, 16)], BEAK, 3.2)                       # the heavy beak, down at us
    _line(c, (-4, 0), (-11, 46), RIM, 2.4)
    for ex, ey in ((-22, -16), (14, -20)):
        _eye(c, ex, ey, 5.0, (0, 0.5))
    c.restore()


# ------------------------------------------------------------------ the head, half the frame
def head(c, x, y, R):
    """the head end on: the heavy beak points straight at the lens, a cone lit on one side and in shade on the
    other; two small eyes high on the sides of the head; the shut wings' shoulders behind, a shade lighter"""
    c.save(); c.translate(x, y); c.scale(R / 100.0, R / 100.0)
    for sx in (-1, 1):                                                                       # shoulders, wings still shut
        pts = [(sx * 70, 60), (sx * 170, 10), (sx * 236, 120), (sx * 226, 320), (sx * 70, 320)]
        _poly(c, pts, (0.15, 0.15, 0.17), 4.0)
        for i in range(4):
            _line(c, (sx * (110 + i * 28), 50 + i * 60), (sx * (170 + i * 14), 130 + i * 60), EDGE, 3.0)
    _poly(c, [(-60, 70), (-44, 120), (-26, 96), (-10, 132), (8, 100), (26, 128), (40, 96), (60, 70)], BODY, 4.0)   # the shaggy throat
    _poly(c, [(-112, 10), (-96, -60), (-50, -104), (50, -104), (96, -60), (112, 10), (80, 80), (-80, 80)], BODY, 4.5)
    c.new_path(); c.move_to(-104, 0); c.line_to(-90, -62); c.line_to(-48, -100); c.line_to(48, -100)              # the lamp's light round its crown
    c.set_source_rgb(*RIM); c.set_line_width(4.0); c.set_line_cap(1); c.stroke()
    for ax, ay in ((-70, -70), (-34, -90), (34, -90), (70, -70)):                              # feathers on the crown
        _line(c, (ax, ay), (ax * 0.7, ay + 24), EDGE, 2.6)
    tip = (0, 128)
    _poly(c, [(-34, -40), (0, -46), tip], (0.46, 0.46, 0.50), 4.0)                               # the beak: its lit side
    _poly(c, [(0, -46), (34, -40), tip], (0.20, 0.20, 0.23), 4.0)                                # and its shaded side
    _poly(c, [(-34, -40), (0, -46), (34, -40), (0, -30)], (0.10, 0.10, 0.12), 3.0)                # bristles over the nostrils
    _line(c, (0, -40), tip, (0.80, 0.80, 0.82), 3.0)                                             # the ridge
    c.new_path(); c.arc(tip[0], tip[1] - 6, 5, 0, 2 * math.pi); c.set_source_rgb(0.95, 0.95, 0.95); c.fill()   # a glint on its tip
    for sx in (-1, 1):
        _eye(c, sx * 72, -44, 13.0, (-sx * 0.5, 0.4))
        _line(c, (sx * 100, -70), (sx * 46, -58), INK, 6.0)                                      # brows down to the beak
    c.restore()


# ------------------------------------------------------------------ the wings over the lens
def wing(c, x, y, S, side=-1, open_=1.0, rot=0.0, haze=0.0):
    """one wing from the shoulder (x, y), fanned out to side (-1 left); open_ 0..1 how far it has unfolded.
    The arm and its coverts, then six fingered primaries from the wrist, with gaps between their tips."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(side * S / 100.0, S / 100.0)
    wx, wy = 210 * math.cos(math.radians(-25 * open_)), 210 * math.sin(math.radians(-25 * open_))   # the wrist
    for i in range(6):
        a = math.radians(-60 + i * 20 * open_ + 15)
        L = 230 - i * 14
        tx, ty = wx + math.cos(a) * L, wy + math.sin(a) * L
        nx, ny = -math.sin(a) * 15, math.cos(a) * 15                                              # half a feather's width
        _poly(c, [(wx + nx, wy + ny), (tx + nx * 0.6, ty + ny * 0.6), (tx + math.cos(a) * 16, ty + math.sin(a) * 16),
                  (tx - nx * 0.6, ty - ny * 0.6), (wx - nx, wy - ny)], WING if i % 2 else BODY, 3.6)
        _line(c, (wx, wy), (tx, ty), EDGE, 2.4)                                                   # its shaft
    _poly(c, [(-20, -50), (wx - 10, wy - 46), (wx + 30, wy), (wx + 10, wy + 60), (110, 120), (20, 110), (-20, 60)], BODY, 4.0)   # the arm
    for i in range(5):                                                                            # its coverts, a row of scallops
        u = (i + 0.5) / 5
        px, py = 10 + (wx - 10) * u, 60 + (wy + 40 - 60) * u
        c.new_path(); c.arc(px, py, 22, 0.1 * math.pi, 0.9 * math.pi); c.set_source_rgb(*EDGE); c.set_line_width(2.6); c.stroke()
    c.restore()


def dark(c, late=1.0):
    """the frame is the raven: its breast and both wings; late 0..1 how far the right wing has come"""
    c.set_source_rgb(*BODY); c.paint()
    wing(c, 300, 430, 150, side=-1, open_=1.0, rot=0.3)
    wing(c, 330, 400, 130 * (0.4 + 0.4 * late), side=1, open_=late, rot=-0.2)
    _poly(c, [(220, 300), (380, 300), (420, 560), (300, 760), (180, 560)], BODY, 4.5)          # the breast between them
    for i in range(6):                                                                         # its feathers, scalloped
        y_ = 360 + i * 60
        for j in range(-2, 3):
            c.new_path(); c.arc(300 + j * 40 + (i % 2) * 20, y_, 22, 0.15 * math.pi, 0.85 * math.pi)
            c.set_source_rgb(*EDGE); c.set_line_width(2.4); c.stroke()


def sweep(c):
    """the tail and wing tips going out over the top of the frame, the street already under them"""
    for sx, x0 in ((-1, 120), (1, 420)):
        c.save(); c.translate(x0, -40); c.rotate(sx * 0.25)
        for i in range(5):
            a = math.radians(70 + sx * (i - 2) * 9)
            L = 260 - abs(i - 2) * 30
            px, py = math.cos(a) * L * sx * 0.6, math.sin(a) * L
            _poly(c, [(-18 + i * 9, 0), (px - 14, py - 10), (px, py + 6), (px + 14, py - 10), (18 + i * 9, 0)], BODY if i % 2 else WING, 4.0)
            _line(c, (i * 9, 4), (px * 0.9, py * 0.9), EDGE, 2.6)
        c.restore()
    _poly(c, [(200, -10), (340, -10), (330, 110), (300, 150), (270, 120), (240, 150), (210, 110)], BODY, 4.0)   # the tail fan
    for x_ in (240, 270, 300):
        _line(c, (x_, 0), (x_, 120), EDGE, 2.4)
    g = cairo.LinearGradient(0, 0, 0, 380)                                                      # the shadow they throw on the lens
    g.add_color_stop_rgba(0, 0, 0, 0, 0.55); g.add_color_stop_rgba(1, 0, 0, 0, 0.0)
    c.set_source(g); c.rectangle(0, 0, 540, 380); c.fill()


def lens(c, amount):
    """feathers almost on the glass: the frame's edges go soft and dark"""
    g = cairo.RadialGradient(270, 470, 160, 270, 470, 620)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.0); g.add_color_stop_rgba(1, 0.01, 0.01, 0.02, amount)
    c.set_source(g); c.paint()


def strike(c, beak=0.0):
    """the asymmetric strike: the head with its beak at the lens; its left wing near us, big, up and forward across
    the frame; its right wing far, small and still half shut. beak 0..1: how close the beak is to the glass"""
    wing(c, 380, 600, 45 + 10 * beak, side=1, open_=0.45, rot=0.2)                                # far wing first, behind
    c.set_source_rgba(0.55, 0.56, 0.60, 0.18); c.rectangle(300, 300, 240, 500); c.fill()         # a little air in front of it
    R = 200 + 140 * beak
    head(c, 300, 380 + 40 * beak, R)
    wing(c, 200, 640, 80 + 20 * beak, side=-1, open_=1.0, rot=0.75)                              # near wing, last, over the shoulder


def dark2(c):
    """the frame is feathers: the near wing across it on a slant, the far one's fingertips leaving at the top right"""
    c.set_source_rgb(*BODY); c.paint()
    wing(c, 470, 60, 40, side=1, open_=0.8, rot=-0.6)
    wing(c, 330, 860, 110, side=-1, open_=1.0, rot=0.9)
    lens(c, 0.9)


KEYS2 = ("dive", "turn", "head", "strike", "strike2", "dark", "dark2", "sweep", "sweep2")    # 1.1 under RAVEN2: nine drawings
END = ("perch", "coil")                                                                        # the film's last two drawings: it is on the lamp, then it springs


# ================================================================== v3 (the second review; Tomas: "proceed")
# One silhouette for a wing (no fingers fanned from one point), smaller hooded eyes with a cold glint and no brows,
# a shorter beak broad at its base with a soft sheen instead of a white line, and a silver rim from the lamp (upper
# right) on every drawing. One wing wipes the lens and uncovers her at 0.42-0.50 s.
SILVER = (0.78, 0.80, 0.86)


def _eye3(c, x, y, r, side=1):
    """a hooded eye: pale, the upper lid down over a third of it, sloping toward the beak; a small cold glint"""
    c.save()
    c.new_path(); c.save(); c.translate(x, y); c.scale(1.0, 0.8); c.arc(0, 0, r, 0, 2 * math.pi); c.restore()
    c.set_source_rgb(0.70, 0.71, 0.72); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(max(1.2, r * 0.18)); c.stroke()
    c.new_path(); c.arc(x - side * r * 0.12, y + r * 0.05, r * 0.5, 0, 2 * math.pi); c.set_source_rgb(*INK); c.fill()
    c.new_path(); c.rectangle(x - side * r * 0.42, y - r * 0.2, r * 0.22, r * 0.16); c.set_source_rgb(0.92, 0.95, 1.0); c.fill()   # the glint
    c.new_path(); c.move_to(x - r * 1.25, y - r * (0.15 if side > 0 else 0.55)); c.line_to(x + r * 1.25, y - r * (0.55 if side > 0 else 0.15))
    c.line_to(x + r * 1.25, y - r * 1.3); c.line_to(x - r * 1.25, y - r * 1.3); c.close_path()                                # the lid
    c.set_source_rgb(*BODY); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(max(1.2, r * 0.18)); c.stroke()
    c.restore()


def _rim(c, pts, lw=3.0):
    c.new_path(); c.move_to(*pts[0])
    for p_ in pts[1:]:
        c.line_to(*p_)
    c.set_source_rgb(*SILVER); c.set_line_width(lw); c.set_line_cap(1); c.set_line_join(1); c.stroke()


def wing3(c, x, y, S, rot=0.0, side=1, haze=0.0):
    """one wing as one shape, shoulder at (x, y), reaching out along +x (side -1: mirrored): a broad root, the
    leading edge up to the wrist and out to the tip, a trailing edge of overlapping primaries and secondaries"""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(side * S / 100.0, S / 100.0)
    lead = [(0, -40), (90, -78), (200, -92), (300, -70), (420, -30)]
    trail = [(420, -30), (392, 6), (380, -8), (350, 30), (336, 14), (300, 52), (284, 36), (246, 72), (230, 58), (180, 92),
             (150, 80), (110, 104), (80, 92), (40, 108), (0, 70)]
    _poly(c, lead + trail, BODY, 4.0)
    for k_, (f, col) in enumerate(((0.78, WING), (0.52, (0.13, 0.13, 0.15)))):          # two rows of coverts over the flight feathers
        band = [(x_ * 1.0, y_) for x_, y_ in lead[:4]] + [(300 * f + 40, -70 + 100 * f), (200 * f, -40 + 120 * f), (100 * f, -10 + 110 * f), (0, 20 + 30 * f)]
        _poly(c, band, col, 2.6)
    for i in range(7):                                                                  # the feathers' edges, overlapping, lit
        u = (i + 0.5) / 7
        bx, by = 40 + 360 * u, 60 - 70 * u
        _line(c, (bx - 30, by - 40), (bx + 4, by + 30 - 30 * u), EDGE, 3.0)
    _rim(c, lead, 5.0)                                                                   # the lamp's light along the leading edge
    if haze:
        c.new_path(); c.move_to(*lead[0])
        for p_ in lead[1:] + trail[1:]:
            c.line_to(*p_)
        c.close_path(); c.set_source_rgba(0.5, 0.5, 0.55, haze); c.fill()
    c.restore()


def beak3(c, base_w, base_y, tip_y):
    """the beak end on: broad at its base, rounded to a short tip, lit side and shade side, a soft sheen"""
    c.new_path(); c.move_to(-base_w, base_y); c.curve_to(-base_w * 0.9, base_y + (tip_y - base_y) * 0.5, -base_w * 0.3, tip_y - 10, 0, tip_y)
    c.line_to(0, base_y - 6); c.close_path(); c.set_source_rgb(0.40, 0.40, 0.44); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(4.0); c.stroke()
    c.new_path(); c.move_to(base_w, base_y); c.curve_to(base_w * 0.9, base_y + (tip_y - base_y) * 0.5, base_w * 0.3, tip_y - 10, 0, tip_y)
    c.line_to(0, base_y - 6); c.close_path(); c.set_source_rgb(0.19, 0.19, 0.22); c.fill_preserve(); c.set_source_rgb(*INK); c.stroke()
    g = cairo.LinearGradient(-base_w * 0.5, 0, base_w * 0.2, 0)                                       # the sheen, soft
    g.add_color_stop_rgba(0, 1, 1, 1, 0.0); g.add_color_stop_rgba(0.6, 0.9, 0.92, 1.0, 0.35); g.add_color_stop_rgba(1, 1, 1, 1, 0.0)
    c.new_path(); c.move_to(-base_w * 0.45, base_y + 6); c.curve_to(-base_w * 0.35, base_y + (tip_y - base_y) * 0.5, -base_w * 0.1, tip_y - 24, -2, tip_y - 14)
    c.line_to(-base_w * 0.05, base_y + 6); c.close_path(); c.set_source(g); c.fill()
    _poly(c, [(-base_w, base_y), (0, base_y - 8), (base_w, base_y), (0, base_y + 12)], (0.10, 0.10, 0.12), 3.0)   # bristles over the nostrils


def head3(c, x, y, R):
    """v3 head end on: hooded eyes, the short broad beak at us, shaggy throat, silver rim on the lamp's side"""
    c.save(); c.translate(x, y); c.scale(R / 100.0, R / 100.0)
    for sx in (-1, 1):
        _poly(c, [(sx * 70, 60), (sx * 170, 10), (sx * 236, 120), (sx * 226, 320), (sx * 70, 320)], (0.13, 0.13, 0.15), 4.0)
        for i in range(4):
            _line(c, (sx * (110 + i * 28), 50 + i * 60), (sx * (170 + i * 14), 130 + i * 60), EDGE, 3.0)
    _rim(c, [(170, 10), (236, 120), (226, 320)], 5.0)
    _poly(c, [(-60, 70), (-44, 120), (-26, 96), (-10, 132), (8, 100), (26, 128), (40, 96), (60, 70)], BODY, 4.0)
    head_pts = [(-112, 10), (-96, -60), (-50, -104), (50, -104), (96, -60), (112, 10), (80, 80), (-80, 80)]
    _poly(c, head_pts, BODY, 4.5)
    _rim(c, [(-50, -104), (50, -104), (96, -60), (112, 10)], 5.0)
    for ax, ay in ((-70, -70), (-34, -90), (34, -90), (70, -70)):
        _line(c, (ax, ay), (ax * 0.7, ay + 24), EDGE, 2.6)
    beak3(c, 44, -36, 92)
    for sx in (-1, 1):
        _eye3(c, sx * 70, -44, 11.0, side=-sx)
    c.restore()


def launch3(c, x, y, R, stretch=0.0):
    """v3 launch: the heavy body drawn out along its flight (stretch), hooded eyes, the short beak, rim light"""
    c.save(); c.translate(x, y)
    ang = math.atan2(-1.0, 1.4)                                                          # the flight's line, from the lamp down-left
    c.rotate(ang); c.scale(1.0 + stretch, 1.0 - stretch * 0.35); c.rotate(-ang)
    c.scale(R / 40.0, R / 40.0)
    _poly(c, [(40, -60), (92, -104), (104, -92), (98, -78), (60, -40)], BODY, 3.4)
    body = [(-34, 0), (-20, -40), (20, -66), (60, -70), (74, -46), (56, -6), (20, 30), (-14, 34)]
    _poly(c, body, BODY, 3.6)
    _poly(c, [(-6, -40), (30, -62), (62, -64), (72, -46), (58, -16), (34, -6), (10, -14)], WING, 3.2)
    _feathers(c, 20, -40, 60, -54, 4, EDGE, 2.6)
    _rim(c, [(-20, -40), (20, -66), (60, -70), (74, -46)], 3.0)
    _hackles(c, -4, 18, 20, 14)
    _poly(c, [(-34, -4), (-30, -30), (-6, -42), (20, -36), (30, -12), (22, 16), (-4, 24), (-26, 16)], BODY, 3.6)
    _rim(c, [(-6, -42), (20, -36), (30, -12)], 2.6)
    c.save(); c.translate(-5, 0); c.scale(0.36, 0.36); beak3(c, 44, -10, 100); c.restore()
    for ex, ey, sd in ((-22, -16, 1), (14, -20, -1)):
        _eye3(c, ex, ey, 4.6, side=sd)
    c.restore()


def wipe(c, u):
    """u 0..1: one wing across the lens from the left, then off to the right"""
    x = -260 + 900 * u
    wing3(c, x, 620, 210, rot=-0.55, side=1)


KEYS3 = ("dive", "turn", "head", "strike", "wipe", "wipe2", "gone")    # 0.00 .. 0.50; 1.2 is under "wipe2" and after it
BG3 = (11, 11, 11, 11, 11, 12, 12)                                  # which shot is under each: 1.1 (no leg, door shut), 1.2's first drawing


def gap(c, behind, pts):
    """v30 (cold test v29: the wing read as "a black slab", "a glitch"): a gap between its feathers, and what is behind
    the wing (1.2's first drawing: her red dress) seen through it, its feather edges lit"""
    c.save(); c.new_path(); c.move_to(*pts[0])
    for p_ in pts[1:]:
        c.line_to(*p_)
    c.close_path(); c.clip_preserve()
    c.translate(350, 650); c.scale(2.6, 2.6); c.translate(-350, -620)                 # close on her dress: red cloth, not a little woman
    c.set_source_surface(behind, 0, 0); c.paint(); c.restore()
    c.new_path(); c.move_to(*pts[0])
    for p_ in pts[1:]:
        c.line_to(*p_)
    c.close_path(); c.set_source_rgb(*INK); c.set_line_width(6); c.set_line_join(1); c.stroke_preserve()
    c.set_source_rgb(*SILVER); c.set_line_width(2.6); c.stroke()


GAP_STRIKE = [(300, 640), (360, 560), (430, 520), (470, 600), (440, 640), (480, 700), (430, 760), (470, 830), (380, 880), (320, 800)]
GAP_WIPE = [(180, 700), (300, 520), (380, 430), (420, 470), (360, 560), (400, 590), (330, 700), (360, 740), (270, 860), (220, 820)]


def draw3(s, key, behind=None):
    import on4_motion as m4
    c = cairo.Context(s)
    if key == "perch":
        perched(c, *PERCH)
    elif key == "coil":
        perched(c, *PERCH, coil=1.0)
    elif key == "dive":
        launch3(c, 370, 270, 62, stretch=0.35)
        for i in range(4):
            _line(c, (420 + i * 14, 180 - i * 4), (480 + i * 14, 100 - i * 4), (0.32, 0.32, 0.35), 2.0)
    elif key == "turn":
        launch3(c, 320, 360, 96, stretch=0.15)
    elif key == "head":
        head3(c, 300, 410, 175)
        lens(c, 0.45)
    elif key == "strike":                                       # the beak at the glass; the wing comes in from the left
        c.save(); c.rectangle(0, 0, 540, 960); c.clip()
        head3(c, 300, 420, 300)
        wing3(c, -300, 640, 210, rot=-0.55, side=1)
        c.restore(); lens(c, 0.7)
        if behind is not None:
            gap(c, behind, GAP_STRIKE)
        return m4._shake(s, 0.0, amp=6.0)
    elif key == "wipe":                                         # the wing over the whole lens
        c.save(); c.rectangle(0, 0, 540, 960); c.clip(); wing3(c, -140, 720, 300, rot=-0.62, side=1); c.restore(); lens(c, 0.6)
        if behind is not None:
            gap(c, behind, GAP_WIPE)
        return m4._shake(s, 0.33, amp=6.0)
    elif key == "wipe2":                                        # its trailing edge going off to the right: she is there
        c.save(); c.rectangle(0, 0, 540, 960); c.clip(); wing3(c, 260, 760, 300, rot=-0.62, side=1); c.restore()
        return m4._shake(s, 0.66, amp=6.0)
    return s


KEYS = ("perch", "perch", "perch", "coil", "launch", "head", "wing", "dark", "sweep", "gone")


def draw(s, key):
    """draw the raven's drawing `key` on the graded surface s; returns the surface to use (shaken or not)"""
    import on4_motion as m4
    c = cairo.Context(s)
    if key == "perch":
        perched(c, *PERCH)
    elif key == "coil":
        perched(c, *PERCH, coil=1.0)
    elif key == "launch":
        launch(c, 360, 300, 52)
    elif key == "dive":                                      # frame 0: already off the lamp, mid-dive
        launch(c, 380, 250, 46)
        for i in range(4):                                   # the air it leaves behind it
            _line(c, (412 + i * 14, 182 - i * 4), (470 + i * 14, 110 - i * 4), (0.30, 0.30, 0.33), 2.0)
    elif key == "turn":                                      # the head snaps round to us
        launch(c, 330, 360, 84)
    elif key == "head":
        head(c, 300, 410, 175)
        lens(c, 0.5)
    elif key == "wing":
        c.save(); c.rectangle(0, 0, 540, 960); c.clip()
        wing(c, 300, 470, 120, side=-1, open_=1.0)
        head(c, 330, 250, 150)
        wing(c, 360, 470, 80, side=1, open_=0.3)
        c.restore(); lens(c, 0.7)
        return m4._shake(s, 0.0, amp=6.0)
    elif key == "dark":
        dark(c, 0.55); lens(c, 0.85)
        return m4._shake(s, 0.4, amp=6.0)
    elif key == "strike":
        c.save(); c.rectangle(0, 0, 540, 960); c.clip(); strike(c, 0.0); c.restore(); lens(c, 0.6)
        return m4._shake(s, 0.0, amp=6.0)
    elif key == "strike2":
        c.save(); c.rectangle(0, 0, 540, 960); c.clip(); strike(c, 1.0); c.restore(); lens(c, 0.8)
        return m4._shake(s, 0.25, amp=6.0)
    elif key == "dark2":
        dark2(c)
        return m4._shake(s, 0.5, amp=6.0)
    elif key == "sweep":
        sweep(c)
        return m4._shake(s, 0.67, amp=6.0)
    elif key == "sweep2":
        c.save(); c.translate(0, -120); sweep(c); c.restore()
        return m4._shake(s, 0.85, amp=6.0)
    return s
