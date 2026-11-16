"""Props for "Office Noir", v2 (props_on_v1.py = v1, kept). v2 after the CCTV review, all opt-in (defaults keep
every earlier sheet as it was): hook_peel() replaces the upward arc with the monitor's corner hooking the heart
(caught, stretched sideways with a white peel line, snapped onto the monitor); enhance() is the robot's digital
zoom into the footage (2x, 4x, pixelated, with a zoom label); flask(open_=True, glove=True) has his gloved hand
unscrewing the cap; bunny(menace=True) is the informant lit from below, eyes in shadow, the fedora tilted low.
v1 notes: Every noir prop has an embarrassing twin in reality:
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


def bunny(k, x, y, s=1.0, mode="pink", hat=None, seed=0, menace=False):
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
    if menace:                                       # eyes in shadow, a hard light from below on the muzzle
        c.save(); c.new_path(); c.save(); c.translate(0, -64); c.scale(26, 22); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        c.clip()
        c.set_source_rgba(0.02, 0.02, 0.03, 0.75); c.rectangle(-30, -90, 60, 25); c.fill()
        c.restore()
        for sx in (-1, 1):                           # two small glints in the dark: still watching
            c.new_path(); c.arc(sx * 10, -68, 1.4, 0, 2 * math.pi); c.set_source_rgb(1, 1, 1); c.fill()
    c.restore()
    if hat:
        d.fedora(k, x + 2 * s, y - (78 if menace else 84) * s, 0.42 * s, tilt=-0.30 if menace else -0.18, seed=seed + 3)


def flask(k, x, y, s=1.0, rot=-0.08, seed=0, open_=False, glove=False):
    """ONE DRINK: a dented steel hip flask, (x, y) its centre. open_: the cap off, hanging on its little hinge;
    glove: his black-gloved hand gripping it, thumb on the cap (the theatrical first drink)."""
    c = k.c
    if open_ or glove:
        c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
        c.restore()
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.new_path(); c.move_to(-26, -30); c.curve_to(-30, 0, -30, 20, -24, 34); c.line_to(24, 34)
    c.curve_to(30, 20, 30, 0, 26, -30); c.curve_to(10, -36, -10, -36, -26, -30); c.close_path()
    _fs(c, STEEL, 2.4)
    c.set_source_rgba(1, 1, 1, 0.55); c.new_path(); c.move_to(-18, -24); c.curve_to(-22, 0, -21, 16, -17, 28)
    c.set_line_width(4); c.stroke()                                            # the hard-light streak
    c.set_source_rgb(*STEEL_DARK); c.set_line_width(1.4)
    c.new_path(); c.move_to(10, -8); c.line_to(16, 2); c.line_to(12, 10); c.stroke()     # the dent
    if open_:
        rect(k, -6, -42, 12, 8, STEEL_DARK, seed + 4, shadow=False, lw=1.6)      # the neck, open
        c.save(); c.translate(8, -46); c.rotate(1.1)
        rect(k, -7, -14, 14, 14, STEEL_DARK, seed + 1, shadow=False, lw=2)      # the cap, flipped open on its hinge
        c.restore()
    else:
        rect(k, -7, -46, 14, 14, STEEL_DARK, seed + 1, shadow=False, lw=2)      # cap
    if glove:                                        # a black leather glove around the body, thumb up to the cap
        GL = (0.07, 0.07, 0.08)
        cut(k, [(-34, -10), (-6, -16), (14, -10), (16, 22), (-8, 30), (-36, 24)], GL, shadow=False, lw=2)
        cut(k, [(4, -14), (12, -36), (20, -38), (18, -12)], GL, shadow=False, lw=2)
        c.set_source_rgba(1, 1, 1, 0.35); c.set_line_width(2)
        c.move_to(-28, -2); c.line_to(6, -8); c.stroke()
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



# ---- v2 additions -----------------------------------------------------------------------------------------------

def hook_peel(c, lapel, corner, end, size, t):
    """The heart caught by the monitor's corner. lapel: where it sits; corner: the monitor corner that hooks its
    curled tip; end: where it ends up stuck (on the monitor, right by the corner). t: 0 on the lapel, 0.33 caught
    (the curled tip on the corner, strain marks), 0.66 stretched sideways between lapel and corner (the white back
    showing, a white peel line back to the lapel), 1 snapped onto the monitor (snap marks)."""
    import don_on as d
    if t < 0.2:
        d.heart(c, lapel[0], lapel[1], size, curl=True)
        return lapel
    if t < 0.5:                                          # caught: still on the lapel, the tip pulled to the corner
        d.heart(c, lapel[0], lapel[1], size, curl=True)
        tip = (lapel[0] + 0.95 * size, lapel[1] - 0.55 * size)
        c.set_source_rgb(1, 1, 1); c.set_line_width(max(2.0, size * 0.18)); c.set_line_cap(1)
        c.move_to(*tip); c.line_to(*corner); c.stroke()
        c.set_source_rgb(*INK); c.set_line_width(1.6)
        for i in (-1, 0, 1):
            c.move_to(corner[0] + 4, corner[1] - 6 + i * 6); c.line_to(corner[0] + 12, corner[1] - 8 + i * 8); c.stroke()
        c.set_line_cap(0)
        return lapel
    if t < 0.85:                                         # stretched sideways, the white back showing
        mx, my = (lapel[0] + corner[0]) / 2 + size * 0.3, (lapel[1] + corner[1]) / 2
        c.set_source_rgb(1, 1, 1); c.set_line_width(max(2.0, size * 0.16)); c.set_line_cap(1)
        c.move_to(lapel[0] - size * 0.3, lapel[1] + size * 0.4); c.line_to(mx, my); c.stroke()   # the peel line
        c.set_line_cap(0)
        c.save(); c.translate(mx, my); c.rotate(-0.35); c.scale(1.35, 0.72)
        c.save(); c.translate(-size * 0.25, size * 0.12)
        d.heart_path(c, 0, 0, size); c.set_source_rgb(1, 1, 1); c.fill_preserve()
        c.set_source_rgb(*INK); c.set_line_width(max(1.0, size * 0.1)); c.stroke(); c.restore()
        d.heart(c, 0, 0, size, curl=False)
        c.restore()
        return (mx, my)
    d.heart(c, end[0], end[1], size, curl=True)          # snapped onto the monitor
    c.set_source_rgb(*INK); c.set_line_width(2)
    for a in (-2.4, -1.9, -1.4):
        c.move_to(end[0] + math.cos(a) * size * 1.3, end[1] + math.sin(a) * size * 1.3)
        c.line_to(end[0] + math.cos(a) * size * 1.8, end[1] + math.sin(a) * size * 1.8); c.stroke()
    return end


ENHANCE_LOGICAL = None      # opt-in (1080 release): the frame's size in drawing units, when its pixels are 2x


def enhance(frame, centre, zoom, pixel=1, label=None):
    """The robot's digital zoom into a finished 540x960 frame: a new frame showing `zoom` times around centre,
    blocky by `pixel`; a white label (e.g. "ENHANCE x2") top-right."""
    W_, H_ = ENHANCE_LOGICAL or (frame.get_width(), frame.get_height())
    sw, sh = max(1, W_ // pixel), max(1, H_ // pixel)
    small = cairo.ImageSurface(cairo.FORMAT_ARGB32, sw, sh)
    cs = cairo.Context(small)
    cs.scale(sw / W_, sh / H_)
    cs.translate(W_ / 2, H_ / 2); cs.scale(zoom, zoom); cs.translate(-centre[0], -centre[1])
    cs.set_source_surface(frame, 0, 0); cs.get_source().set_filter(cairo.FILTER_BEST); cs.paint()
    out = cairo.ImageSurface(cairo.FORMAT_ARGB32, W_, H_)
    co = cairo.Context(out)
    co.scale(W_ / sw, H_ / sh); co.set_source_surface(small, 0, 0); co.get_source().set_filter(cairo.FILTER_NEAREST)
    co.paint()
    if label:
        co2 = cairo.Context(out)
        co2.select_font_face("DejaVu Sans Mono", 0, 1); co2.set_font_size(26)
        w = co2.text_extents(label).x_advance
        co2.set_source_rgb(0.95, 0.95, 0.95); co2.move_to(W_ - 40 - w, 112); co2.show_text(label)
        co2.set_line_width(2); co2.rectangle(W_ / 2 - 120, H_ / 2 - 120, 240, 240); co2.stroke()   # the zoom box
    return out


# ---- storyboard v2 additions: the magnifier (dream) and its toy twin (reality) -----------------------------------

TOY_PINK = (0.98, 0.62, 0.78)


def magnifier(c, x, y, r, rot=0.6, toy=False, glass=True):
    """A magnifying glass, (x, y) the lens centre, r its radius; the handle points along rot (radians, from +x).
    Dream: a black handle and a steel ring. toy=True: the reality twin, chunky pink plastic."""
    ring = TOY_PINK if toy else STEEL
    handle = TOY_PINK if toy else (0.08, 0.08, 0.09)
    hx0, hy0 = x + math.cos(rot) * r, y + math.sin(rot) * r
    hx1, hy1 = x + math.cos(rot) * r * 2.3, y + math.sin(rot) * r * 2.3
    c.set_line_cap(1)
    c.set_source_rgb(*INK); c.set_line_width(r * 0.36 + 4); c.move_to(hx0, hy0); c.line_to(hx1, hy1); c.stroke()
    c.set_source_rgb(*handle); c.set_line_width(r * 0.36); c.move_to(hx0, hy0); c.line_to(hx1, hy1); c.stroke()
    c.set_line_cap(0)
    if glass:
        c.new_path(); c.arc(x, y, r, 0, 2 * math.pi); c.set_source_rgba(0.85, 0.92, 1.0, 0.18); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(r * 0.22 + 4); c.new_path(); c.arc(x, y, r, 0, 2 * math.pi); c.stroke()
    c.set_source_rgb(*ring); c.set_line_width(r * 0.22); c.new_path(); c.arc(x, y, r, 0, 2 * math.pi); c.stroke()
    c.set_source_rgba(1, 1, 1, 0.55); c.set_line_width(r * 0.06)
    c.new_path(); c.arc(x, y, r * 0.78, math.pi * 1.1, math.pi * 1.45); c.stroke()


def lens_view(c, src, x, y, r, zoom=1.6, rot=0.6, toy=False):
    """Draw the magnifier at (x, y) over src, showing src magnified `zoom` times inside the lens."""
    c.save(); c.new_path(); c.arc(x, y, r, 0, 2 * math.pi); c.clip()
    c.translate(x, y); c.scale(zoom, zoom); c.translate(-x, -y)
    c.set_source_surface(src, 0, 0); c.get_source().set_filter(cairo.FILTER_BEST); c.paint()
    c.restore()
    magnifier(c, x, y, r, rot, toy, glass=False)
