"""Props for "Office Noir", v1. Every noir prop has an embarrassing twin in reality:
- bunny(mode="noir"): the informant, a grey plush bunny in a tiny fedora (it never talks);
  bunny(mode="pink"): the same bunny in reality, pastel pink, one ear flopped over;
- flask(): ONE DRINK in the flashback, a dented steel hip flask;
- milk(): its twin, a carton of strawberry milk with a bendy straw (pastel pink, never red).
No red on any of these: red belongs to the heart (don_on.heart is the sticker)."""
import math
import cairo
import kit
import don_on as d
from kit import INK, cut, rect, ellipse

BUNNY_PINK = (0.97, 0.75, 0.83)
BUNNY_PINK_IN = (1.0, 0.89, 0.92)
BUNNY_GREY = (0.62, 0.61, 0.63)
BUNNY_GREY_IN = (0.80, 0.79, 0.80)
STEEL = (0.74, 0.76, 0.79)
STEEL_DARK = (0.48, 0.50, 0.54)
CARTON = (0.98, 0.97, 0.95)
CARTON_PINK = (0.98, 0.72, 0.82)


def _fs(c, col, lw=2.2):
    c.set_source_rgb(*col); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(lw); c.stroke()


def bunny(k, x, y, s=1.0, mode="pink", hat=None, seed=0):
    """(x, y) = the bottom of the sitting bunny. About 120 units tall at s=1 (ears included)."""
    c = k.c
    col, inn = (BUNNY_PINK, BUNNY_PINK_IN) if mode == "pink" else (BUNNY_GREY, BUNNY_GREY_IN)
    if hat is None:
        hat = mode == "noir"
    c.save(); c.translate(x, y); c.scale(s, s)
    # ears: the screen-left one upright, the other flopped over
    for (ex, ang, flop) in ((-12, -0.15, False), (12, 0.25, True)):
        c.save(); c.translate(ex, -78); c.rotate(ang)
        if flop:
            c.rotate(1.1)
        c.new_path(); c.save(); c.translate(0, -26); c.scale(9, 27); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        _fs(c, col)
        c.new_path(); c.save(); c.translate(0, -26); c.scale(4.5, 20); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        c.set_source_rgb(*inn); c.fill()
        c.restore()
    c.new_path(); c.save(); c.translate(0, -24); c.scale(30, 26); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
    _fs(c, col)                                                                # body
    c.new_path(); c.save(); c.translate(0, -20); c.scale(16, 15); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
    c.set_source_rgb(*inn); c.fill()                                           # tummy
    for sx in (-1, 1):                                                         # feet + paws
        c.new_path(); c.save(); c.translate(sx * 18, -4); c.scale(11, 6); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        _fs(c, col, 1.8)
        c.new_path(); c.save(); c.translate(sx * 24, -32); c.scale(7, 9); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        _fs(c, col, 1.8)
    c.new_path(); c.save(); c.translate(0, -64); c.scale(26, 22); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
    _fs(c, col)                                                                # head
    for sx in (-1, 1):                                                         # button eyes, stitched
        c.new_path(); c.arc(sx * 10, -68, 3.6, 0, 2 * math.pi); c.set_source_rgb(*INK); c.fill()
        c.new_path(); c.arc(sx * 10 - 1, -69, 1.0, 0, 2 * math.pi); c.set_source_rgb(1, 1, 1); c.fill()
    c.new_path(); c.save(); c.translate(0, -57); c.scale(9, 6); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
    c.set_source_rgb(*inn); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(1.6)                              # nose + stitched mouth
    c.new_path(); c.move_to(-3, -60); c.line_to(3, -60); c.line_to(0, -57); c.close_path(); c.fill()
    c.new_path(); c.move_to(0, -57); c.line_to(0, -53); c.move_to(-4, -51); c.line_to(0, -53); c.line_to(4, -51); c.stroke()
    c.restore()
    if hat:
        d.fedora(k, x + 2 * s, y - 84 * s, 0.42 * s, tilt=-0.18, seed=seed + 3)


def flask(k, x, y, s=1.0, rot=-0.08, seed=0):
    """ONE DRINK: a dented steel hip flask, (x, y) its centre."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.new_path(); c.move_to(-26, -30); c.curve_to(-30, 0, -30, 20, -24, 34); c.line_to(24, 34)
    c.curve_to(30, 20, 30, 0, 26, -30); c.curve_to(10, -36, -10, -36, -26, -30); c.close_path()
    _fs(c, STEEL, 2.4)
    c.set_source_rgba(1, 1, 1, 0.55); c.new_path(); c.move_to(-18, -24); c.curve_to(-22, 0, -21, 16, -17, 28)
    c.set_line_width(4); c.stroke()                                            # the hard-light streak
    c.set_source_rgb(*STEEL_DARK); c.set_line_width(1.4)
    c.new_path(); c.move_to(10, -8); c.line_to(16, 2); c.line_to(12, 10); c.stroke()     # the dent
    rect(k, -7, -46, 14, 14, STEEL_DARK, seed + 1, shadow=False, lw=2)          # cap
    c.restore()


def milk(k, x, y, s=1.0, seed=0):
    """The twin: strawberry milk, a small carton with a bendy straw, (x, y) the bottom middle."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    cut(k, [(-18, 0), (18, 0), (18, -44), (-18, -44)], CARTON, shadow=False, lw=2.2)
    cut(k, [(-18, -44), (18, -44), (10, -58), (-10, -58)], CARTON_PINK, shadow=False, lw=2.0)
    rect(k, -14, -36, 28, 22, CARTON_PINK, seed + 2, shadow=False, lw=1.4)       # the label band
    kit.text(k, "MILK", 0, -25, 9, (0.55, 0.30, 0.42))
    # the bendy straw, striped pink and white
    pts = [(6, -56), (6, -78), (12, -86), (22, -88)]
    for wd, col in ((7, INK), (5, (1, 1, 1))):
        c.set_source_rgb(*col); c.set_line_width(wd); c.set_line_cap(1)
        c.new_path(); c.move_to(*pts[0]); c.line_to(*pts[1]); c.curve_to(6, -82, 8, -86, 12, -86); c.line_to(*pts[3])
        c.stroke()
    c.set_source_rgb(*CARTON_PINK); c.set_line_width(5); c.set_dash([4, 4])
    c.new_path(); c.move_to(*pts[0]); c.line_to(*pts[1]); c.curve_to(6, -82, 8, -86, 12, -86); c.line_to(*pts[3]); c.stroke()
    c.set_dash([]); c.set_line_cap(0)
    c.restore()


# ---- v1 additions (Office Noir props step): the monitor, the heart's peel, the CCTV overlay -------------------

MON_BEZEL = (0.20, 0.20, 0.22)
MON_SCREEN = (0.62, 0.66, 0.70)


def monitor(k, x, y, s=1.0, seed=0):
    """Pam's office monitor, front three-quarter, (x, y) = the bottom middle of the stand. Returns its rects."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    rect(k, -34, -10, 68, 10, MON_BEZEL, seed, shadow=False, lw=2)                     # foot
    rect(k, -8, -40, 16, 32, MON_BEZEL, seed + 1, shadow=False, lw=2)                   # neck
    rect(k, -88, -150, 176, 114, MON_BEZEL, seed + 2, lw=2.4)                           # bezel
    rect(k, -80, -142, 160, 92, MON_SCREEN, seed + 3, shadow=False, lw=1.6)              # screen
    c.set_source_rgba(1, 1, 1, 0.35); c.set_line_width(3)
    for i in range(4):
        c.move_to(-68, -126 + i * 18); c.line_to(-68 + (110 - i * 22), -126 + i * 18); c.stroke()
    c.restore()
    return {"bezel": (x - 88 * s, y - 150 * s, 176 * s, 114 * s), "left_edge": (x - 88 * s, y - 120 * s)}


def _ease(t):
    return t * t * (3 - 2 * t)


def heart_peel(c, start, end, size, t):
    """The paper heart moving from start (on the lapel) to end (on the monitor), t = 0..1.
    0: flat on the lapel; ~0.33: the curled corner caught on the monitor edge, lifting; ~0.66: peeled, stretched
    between the two, the white back showing; 1: stuck flat on the monitor."""
    import don_on as d
    u = _ease(max(0.0, min(1.0, (t - 0.15) / 0.75)))
    x = start[0] + (end[0] - start[0]) * u
    y = start[1] + (end[1] - start[1]) * u - 18 * math.sin(math.pi * u) * size / 13
    rot = -0.55 * math.sin(math.pi * u) + (0.10 * u)
    squash = 1 - 0.35 * math.sin(math.pi * u)
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(squash, 1)
    if 0.05 < u < 0.95:                                   # the white paper back, peeking out as it peels
        c.save(); c.translate(size * 0.25, -size * 0.1)
        d.heart_path(c, 0, 0, size); c.set_source_rgb(1, 1, 1); c.fill_preserve()
        c.set_source_rgb(*INK); c.set_line_width(max(1.0, size * 0.1)); c.stroke(); c.restore()
    d.heart(c, 0, 0, size, curl=True)
    c.restore()
    if 0.2 < t < 0.5:                                     # the corner catching: a tiny strain mark at the edge
        c.set_source_rgb(*INK); c.set_line_width(1.6)
        for i in (-1, 0, 1):
            c.move_to(x + size * 1.2, y - size * 0.6 + i * 5); c.line_to(x + size * 1.6, y - size * 0.7 + i * 7); c.stroke()
    return (x, y)


def cctv_overlay(c, w, h, stamp="MON 08:59:14", cam="CAM 3", rec_on=True, seed=3):
    """Security-cam look over a finished frame: scanlines, a soft vignette, corner brackets, a timestamp, the camera
    name and a blinking WHITE REC (red is the heart's)."""
    import random
    r = random.Random(seed)
    c.save()
    c.set_source_rgba(0, 0, 0, 0.13)
    for yy in range(0, int(h), 4):
        c.rectangle(0, yy, w, 1.6)
    c.fill()
    g = cairo.RadialGradient(w / 2, h / 2, min(w, h) * 0.3, w / 2, h / 2, max(w, h) * 0.72)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, 0.55)
    c.set_source(g); c.rectangle(0, 0, w, h); c.fill()
    c.set_source_rgba(1, 1, 1, 0.05)                                                   # tape noise streak
    yy = r.uniform(0.2, 0.8) * h
    c.rectangle(0, yy, w, 6); c.fill()
    c.set_source_rgb(0.95, 0.95, 0.95); c.set_line_width(3)
    m, L = 22, 34
    for (x0, y0, dx, dy) in ((m, m, 1, 1), (w - m, m, -1, 1), (m, h - m, 1, -1), (w - m, h - m, -1, -1)):
        c.move_to(x0, y0 + dy * L); c.line_to(x0, y0); c.line_to(x0 + dx * L, y0); c.stroke()
    c.select_font_face("DejaVu Sans Mono", 0, 1); c.set_font_size(h * 0.03)
    c.set_source_rgb(0.95, 0.95, 0.95)
    c.move_to(m + 12, h - m - 14); c.show_text(stamp)
    c.move_to(m + 12, m + 14 + h * 0.03); c.show_text(cam)
    if rec_on:
        c.arc(w - m - 120, m + 14 + h * 0.022, h * 0.011, 0, 2 * math.pi); c.fill()
        c.move_to(w - m - 104, m + 14 + h * 0.03); c.show_text("REC")
    c.restore()
