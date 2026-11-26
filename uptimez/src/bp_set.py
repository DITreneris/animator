"""The Blueprint room. One 960x540 stage. Locked 16:9 set: the-blueprint/set-16x9.md.

fs_set4 stays the 9:16 set. This file draws the same people, the same props and the
same three zones, with the geometry the wide frame needs: a shorter counter, a floor
band, and three rows. Character scales are the home scales. Don stays 0.60.
"""
import math

import cairo

import brand
import fs_set as fs
import fs_set3 as s3
import kit
import mom_fs as mfs
import set_ob as st
import sofia_fs as sfs
from kit import INK, cut, ellipse, rect

# Wall meets floor here. 140px of floor below it is 26% of the 540 frame.
F = 400
# Three planes. X stays in the same zones. Depth is the feet line, not a new scale.
BACK = 418           # Pam and Mom, behind the desk
MID = 458            # Client, robot, Sofía
FRONT = 500          # Don
CAB = 408            # against the back wall, not standing in the room

# Home scales. Not adjusted to fit the frame.
CLIENT = (132, MID, 0.52)
ROBOT = (248, MID, 0.48)
SOFIA = (348, MID, 0.47)     # upstage of Don, and left of the stuck two-shot
DON = (476, FRONT, 0.60)
PAM = (694, BACK, 0.50)
MOM = (778, BACK, 0.50)
SHRED_AT = (556, FRONT + 4, 0.72)

# Desk sits in the mid plane, forward of the wall. Legs end in front of Pam's feet.
CX0, CX1 = 658, 846          # 42px left, so the office door has a passage
TOP_FRONT = 340          # front edge of the top. Pam's hands are 77px above her feet.
TOP_D = 28               # the slab, seen from above
LIP = 22                 # the front face, thick enough to read as a top
DESK_FEET = 448
DESK = st.DESK
DESK_DARK = st.DESK_DARK
TOP = (0.93, 0.89, 0.80)
# The front was the same sand as the wall. Darker, and a step cooler, so the top stays the light plane.
FRONT = (0.50, 0.44, 0.38)
FRONT_DARK = (0.38, 0.33, 0.29)
# CEO leaf, about 13% lighter than the last pass. The opening stays dark.
WOOD = (0.67, 0.51, 0.37)
WOOD_DARK = (0.62, 0.47, 0.34)
FRAME = (0.30, 0.24, 0.20)
BASE = (0.62, 0.52, 0.40)
# Accents only. The wall stays the series sand.
FICUS_GREEN = (0.275, 0.404, 0.306)   # #46674E
FICUS_DEEP = (0.20, 0.32, 0.24)
FICUS_LIT = (0.322, 0.482, 0.349)     # #527B59
GLASS_BLUE = (0.459, 0.584, 0.647)    # #7595A5
COOL = (0.549, 0.667, 0.725)          # #8CAAB9
WALL = (0.902, 0.851, 0.745)          # #E6D9BE
FLOOR_C = (0.725, 0.631, 0.498)       # #B9A17F
SHADE = (0.506, 0.455, 0.388)         # #817463
OCHRE = (0.769, 0.545, 0.271)         # #C48B45
TERRA = (0.608, 0.349, 0.271)         # #9B5945
# CEO door, on the back wall. Bottom flush with F. Not fs_set3's 330px door.
DOOR = (888, F - 196, 44, 196)   # 16px right of the last place, clear of the desk


def _contact(k, x, y, w):
    """Down and to the right. One brown, one weight, under every foot."""
    c = k.c
    c.save()
    c.translate(x + 8, y + 3)
    ww = max(18, w)
    c.scale(ww * 0.46, ww * 0.10)
    c.set_source_rgba(*SHADE, 0.18)
    c.arc(0, 0, 1, 0, 2 * math.pi)
    c.fill()
    c.restore()


def _fit(c, text, x, y, w, size, col):
    c.set_source_rgb(*col)
    c.select_font_face("Inter", 0, 1)
    while size > 4:
        c.set_font_size(size)
        if c.text_extents(text).x_advance <= w - 8:
            break
        size -= 0.4
    e = c.text_extents(text)
    c.move_to(x + (w - e.x_advance) / 2.0, y)
    c.show_text(text)


def _baseboard(k):
    """Meets both door frames and runs past the close-up edges."""
    dx, _, dw, _ = DOOR
    # Entrance frame starts near x=10. CEO frame ends near x=940. Close-ups look past 0 and 960.
    runs = ((-80, 90), (138, dx - 8 - 138), (dx + dw + 8, 1100 - (dx + dw + 8)))
    y, h = F - 9, 9
    for i, (x, w) in enumerate(runs):
        if w < 8:
            continue
        r = k.rng(40 + i)
        def wob(px, py, rng=r):
            return (px + rng.uniform(-0.7, 0.7), py + rng.uniform(-0.55, 0.55))
        cut(k, [wob(x, y), wob(x + w, y), wob(x + w, y + h), wob(x, y + h)],
            BASE, shadow=False, lw=1.3)


def _wall_band(k):
    """A rail and a slightly darker lower wall. One seam. Not five new posters."""
    c = k.c
    c.set_source_rgba(0.42, 0.34, 0.26, 0.04)
    c.rectangle(0, F - 72, 960, 72)
    c.fill()
    c.set_source_rgba(0.35, 0.28, 0.22, 0.16)
    c.set_line_width(1.1)
    c.move_to(0, F - 72)
    c.line_to(960, F - 72)
    c.stroke()


def _span():
    """Past both edges. The counter camera looks past x=960, the shred camera past x=0."""
    return -120, 1240


def _floor(k):
    c = k.c
    x0, w = _span()
    c.set_source_rgb(*FLOOR_C)
    c.rectangle(x0, F, w, 360)
    c.fill()
    for i, a in enumerate((0.045, 0.025, 0.012)):
        c.set_source_rgba(*SHADE, a)
        c.rectangle(x0, F + i * 18, w, 18)
        c.fill()
    # Four boards, tighter at the wall, wider toward the camera.
    c.set_source_rgba(*SHADE, 0.42)
    c.set_line_width(1.15)
    c.set_line_cap(1)
    for i, xf in enumerate((150, 370, 610, 870)):
        xw = 480 + (xf - 480) * 0.58
        r = k.rng(70 + i)
        c.move_to(xw + r.uniform(-1.2, 1.2), F + 3)
        c.line_to(xf + r.uniform(-1.2, 1.2), F + 268)
        c.stroke()
    # Left is the window side. Right falls off.
    warm = cairo.LinearGradient(x0, 0, 560, 0)
    warm.add_color_stop_rgba(0, *OCHRE, 0.16)
    warm.add_color_stop_rgba(1, *OCHRE, 0.0)
    c.set_source(warm)
    c.rectangle(x0, F, 680, 360)
    c.fill()
    cool = cairo.LinearGradient(480, 0, x0 + w, 0)
    cool.add_color_stop_rgba(0, 0.20, 0.26, 0.31, 0.0)
    cool.add_color_stop_rgba(1, 0.20, 0.26, 0.31, 0.14)
    c.set_source(cool)
    c.rectangle(480, F, x0 + w - 480, 360)
    c.fill()
    c.set_source_rgb(*INK)
    c.set_line_width(2)
    c.move_to(x0, F)
    c.line_to(x0 + w, F)
    c.stroke()


def _ambience(k):
    """A window off the left. Warm there, cooler on the right, six blind bars onto the floor."""
    c = k.c
    x0, w = _span()
    warm = cairo.LinearGradient(x0, 0, 640, 0)
    warm.add_color_stop_rgba(0, *OCHRE, 0.09)
    warm.add_color_stop_rgba(1, *OCHRE, 0.0)
    c.set_source(warm)
    c.rectangle(x0, 0, 760, F)
    c.fill()
    cool = cairo.LinearGradient(500, 0, x0 + w, 0)
    cool.add_color_stop_rgba(0, *COOL, 0.0)
    cool.add_color_stop_rgba(1, *COOL, 0.07)
    c.set_source(cool)
    c.rectangle(500, 0, x0 + w - 500, F)
    c.fill()
    slope, pitch = 0.36, 48
    x1 = x0 + w
    for i in range(6):
        y0 = 24 + i * pitch
        drop = (x1 - x0) * slope
        for thick, a_l, a_r in ((16, 0.045, 0.016), (8, 0.09, 0.034)):
            pad = (16 - thick) / 2.0
            for clip_y, clip_h, scale in ((0, F, 1.0), (F, 360, 0.72)):
                c.save()
                c.rectangle(x0, clip_y, w, clip_h)
                c.clip()
                g = cairo.LinearGradient(x0, 0, x1, 0)
                g.add_color_stop_rgba(0, *SHADE, a_l * scale)
                g.add_color_stop_rgba(1, *SHADE, a_r * scale)
                c.set_source(g)
                yy = y0 + pad
                c.move_to(x0, yy)
                c.line_to(x1, yy + drop)
                c.line_to(x1, yy + thick + drop)
                c.line_to(x0, yy + thick)
                c.close_path()
                c.fill()
                c.restore()
    _baseboard(k)


def _mat(k):
    """Wider than the opening, darker, so the entrance is its own zone."""
    rect(k, 4, F + 2, 164, 46, (0.34, 0.24, 0.20), 21, shadow=False, lw=1.6)
    c = k.c
    c.set_source_rgba(*GLASS_BLUE, 0.45)
    c.set_line_width(1.3)
    c.rectangle(12, F + 8, 148, 34)
    c.stroke()


def _glass_cool(k):
    """The pane only. The open street stays the street."""
    x, y, w, h = 18, F - 214, 116, 214
    px = x - w * 0.92 * 0.85
    c = k.c
    c.save()
    c.rectangle(x, y, w, h)
    c.clip()
    c.set_source_rgba(*COOL, 0.50)
    c.rectangle(px, y, w, h)
    c.fill()
    c.set_source_rgba(*COOL, 0.70)
    c.set_line_width(5)
    c.rectangle(x + 3, y + 3, w - 6, h - 6)
    c.stroke()
    c.set_source_rgba(0.90, 0.95, 0.97, 0.55)
    c.set_line_width(7)
    c.move_to(px + 20, y + h - 16)
    c.line_to(px + 76, y + 26)
    c.stroke()
    c.restore()


def _ficus(k):
    """One plant beside the entrance. Shorter than Don. One leaf has given up."""
    x = 188
    c = k.c
    c.save()
    c.translate(x, F)
    cut(k, [(-20, -34), (20, -34), (14, 0), (-14, 0)], TERRA, shadow=False, lw=1.5)
    rect(k, -24, -40, 48, 8, OCHRE, 441, shadow=False, lw=1.2)
    c.set_source_rgb(0.34, 0.24, 0.16)
    c.set_line_width(3.4)
    c.set_line_cap(1)
    c.move_to(0, -38)
    c.curve_to(-3, -70, 5, -96, 1, -118)
    c.stroke()
    leaves = ((-20, -108, -0.7, 0), (18, -104, 0.6, 3), (-8, -124, -0.2, 1),
               (24, -122, 0.85, 0), (-28, -120, -1.0, 3), (8, -140, 0.15, 1),
               (-16, -142, -0.45, 0), (20, -146, 0.4, 3), (0, -158, 0.05, 1),
               (30, -112, 0.45, 2))
    cols = {0: FICUS_DEEP, 1: FICUS_GREEN, 2: OCHRE, 3: FICUS_LIT}
    for i, (dx, dy, rot, tone) in enumerate(leaves):
        c.save()
        c.translate(dx, dy)
        c.rotate(rot)
        if tone == 2:
            cut(k, [(0, -16), (5, -2), (3, 12), (0, 16), (-3, 10), (-6, -2)],
                (0.45, 0.30, 0.16), shadow=False, lw=1.1)
            c.set_source_rgb(0.32, 0.20, 0.10)
            c.set_line_width(0.8)
            c.move_to(0, -12)
            c.line_to(0, 12)
            c.stroke()
            c.restore()
            continue
        ellipse(k, 0, 0, 10, 16, cols[tone], 450 + i, shadow=False, lw=1.2)
        c.set_source_rgb(0.12, 0.22, 0.14)
        c.set_line_width(0.8)
        c.move_to(0, -12)
        c.line_to(0, 12)
        c.stroke()
        if tone != 2:
            c.set_source_rgba(*FICUS_LIT, 0.9 if dx < 6 else 0.45)
            c.set_line_width(1.7)
            c.arc(-3.5, -5, 7.5, math.pi * 1.1, math.pi * 1.65)
            c.stroke()
        c.restore()
    c.restore()
    _contact(k, x + 4, F, 36)


def _cast(k, x, y, w, h, depth):
    """Down and to the right. A sheet sits close. A thicker object throws more."""
    c = k.c
    c.set_source_rgba(*SHADE, 0.05 + 0.035 * depth)
    c.rectangle(x + 1.2 + depth, y + 1.6 + depth, w, h)
    c.fill()


def _logo(k):
    """The company, high on the empty wall between the screen and the portrait."""
    brand.lockup(k.c, 330, 18, 40)


def _poster(k, x, y):
    """The company line. The zero is files found."""
    _cast(k, x, y, 100, 118, 2)
    rect(k, x, y, 100, 118, (0.20, 0.24, 0.32), 31, shadow=False, lw=2)
    rect(k, x + 5, y + 5, 90, 108, (0.93, 0.90, 0.82), 32, shadow=False, lw=1.2)
    c = k.c
    c.set_source_rgb(*brand.NAVY)
    c.select_font_face("Inter", 0, 1)
    c.set_font_size(10)
    c.move_to(x + 16, y + 24)
    c.show_text("NOTHING")
    c.move_to(x + 18, y + 38)
    c.show_text("GETS LOST")
    c.set_source_rgb(0.20, 0.62, 0.34)
    c.arc(x + 50, y + 68, 16, 0, 2 * math.pi)
    c.fill()
    c.set_source_rgb(1, 1, 1)
    c.set_font_size(18)
    e = c.text_extents("0")
    c.move_to(x + 50 - e.x_advance / 2, y + 74)
    c.show_text("0")
    c.set_source_rgb(*brand.NAVY)
    c.set_font_size(8)
    e = c.text_extents("FOUND")
    c.move_to(x + 50 - e.x_advance / 2, y + 102)
    c.show_text("FOUND")


def _clock(k, x, y):
    c = k.c
    c.set_source_rgba(*SHADE, 0.10)
    c.arc(x + 3, y + 4, 22, 0, 2 * math.pi)
    c.fill()
    c.set_source_rgb(*INK)
    c.set_line_width(3)
    c.arc(x, y, 23, 0, 2 * math.pi)
    c.stroke()
    c.set_source_rgb(0.97, 0.96, 0.92)
    c.arc(x, y, 20, 0, 2 * math.pi)
    c.fill()
    c.set_source_rgb(*INK)
    c.set_line_width(1.8)
    c.move_to(x, y)
    c.line_to(x + 11, y - 5)
    c.move_to(x, y)
    c.line_to(x - 2, y - 14)
    c.stroke()


def _cctv(k, x, y):
    """A head on a short arm. The arm meets a plate on the wall."""
    _cast(k, x + 8, y - 8, 14, 8, 1)
    rect(k, x + 8, y - 10, 14, 7, (0.34, 0.36, 0.40), 90, shadow=False, lw=1.1)
    rect(k, x + 12, y - 4, 5, 8, (0.28, 0.30, 0.34), 91, shadow=False, lw=1.0)
    rect(k, x, y, 30, 14, (0.22, 0.24, 0.28), 92, shadow=False, lw=1.4)
    ellipse(k, x + 22, y + 7, 4.2, 4.2, (0.45, 0.62, 0.78), 93, shadow=False, lw=1.1)


def _board(k, x, y):
    """A static board, about a fifth larger. The papers do not change in this pilot."""
    _cast(k, x, y, 82, 60, 3)
    rect(k, x, y, 82, 60, (0.62, 0.54, 0.44), 94, shadow=False, lw=1.2)
    rect(k, x + 4, y + 4, 74, 52, (0.84, 0.76, 0.60), 95, shadow=False, lw=0.9)
    rect(k, x + 10, y + 10, 26, 18, (0.96, 0.95, 0.91), 96, shadow=False, lw=1)
    rect(k, x + 42, y + 26, 28, 20, (0.90, 0.94, 0.97), 97, shadow=False, lw=1)
    ellipse(k, x + 22, y + 10, 2.2, 2.2, (0.70, 0.16, 0.16), 98, shadow=False, lw=0.8)
    ellipse(k, x + 54, y + 26, 2.2, 2.2, (0.70, 0.16, 0.16), 99, shadow=False, lw=0.8)


def _certificate(k, x, y):
    """The absurd one, beside the CEO door."""
    _cast(k, x, y, 56, 42, 1)
    rect(k, x, y, 56, 42, (0.85, 0.70, 0.30), 100, shadow=False, lw=1.6)
    rect(k, x + 4, y + 4, 48, 34, (0.97, 0.96, 0.92), 101, shadow=False, lw=1)
    c = k.c
    _fit(c, "BEST", x, y + 16, 56, 7, brand.NAVY)
    _fit(c, "BOSS", x, y + 28, 56, 8, (0.70, 0.16, 0.16))
    ellipse(k, x + 44, y + 32, 5, 5, (0.85, 0.70, 0.30), 102, shadow=False, lw=1)


def _ceo_door(k):
    """One leaf, ajar, hinged on the right. The old 330px door hung a panel below the floor."""
    x, y, w, h = DOOR
    c = k.c
    rect(k, x - 8, y - 8, w + 16, h + 8, FRAME, 801, shadow=False, lw=2)
    rect(k, x, y, w, h, (0.20, 0.18, 0.16), 802, shadow=False, lw=1.4)
    rect(k, x, y, 3, h, (0.48, 0.38, 0.30), 807, shadow=False, lw=0.8)
    gap = 14
    leaf_r = x + w - 3
    cut(k, [(x + gap + 6, y + 5), (leaf_r, y + 3), (leaf_r, y + h - 2), (x + gap, y + h - 2)],
        WOOD, shadow=False, lw=2)
    cut(k, [(x + gap + 10, y + 36), (leaf_r - 6, y + 34), (leaf_r - 6, y + h - 22), (x + gap + 6, y + h - 20)],
        WOOD_DARK, shadow=False, lw=1.3)
    for i, hy in enumerate((y + 42, y + h - 48)):
        rect(k, x + w - 5, hy, 7, 5, (0.74, 0.72, 0.64), 810 + i, shadow=False, lw=1.0)
    kx, ky = x + gap + 8, y + int(h * 0.56)
    ellipse(k, kx, ky, 3.2, 3.2, (0.85, 0.72, 0.38), 812, shadow=False, lw=1)
    c.set_source_rgba(1, 0.96, 0.84, 0.85)
    c.arc(kx - 1.1, ky - 1.1, 1.15, 0, 2 * math.pi)
    c.fill()
    _contact(k, x + w / 2, y + h, 30)
    px, py, pw, ph = x - 10, y - 40, w + 20, 32
    rect(k, px, py, pw, ph, (0.85, 0.70, 0.30), 806, lw=1.6)
    _fit(c, "DON · CEO", px, py + 13, pw, 7, (0.25, 0.18, 0.05))
    _fit(c, "VISIONARY", px, py + 26, pw, 6.5, (0.25, 0.18, 0.05))


def _cabinet(k, x, floor):
    """A front, a narrow side, label holders. FILES sits in the top holder."""
    w, h, d = 48, 98, 9
    y = floor - h
    cut(k, [(x + w, y + 4), (x + w + d, y + 10), (x + w + d, floor - 2), (x + w, floor)],
        (0.32, 0.34, 0.40), lw=1.6)
    rect(k, x, y, w, h, (0.42, 0.45, 0.50), 41, lw=2)
    c = k.c
    for i, dy in enumerate((8, 52)):
        rect(k, x + 4, y + dy, w - 8, 36, (0.50, 0.53, 0.58), 42 + i, shadow=False, lw=1.2)
        rect(k, x + 6, y + dy + 5, 36, 10, (0.93, 0.90, 0.82), 44 + i, shadow=False, lw=0.8)
        c.set_source_rgb(0.72, 0.74, 0.78)
        c.rectangle(x + 16, y + dy + 20, 16, 3)
        c.fill()
    _fit(c, "FILES", x + 6, y + 18, 36, 5.5, INK)
    _fit(c, "LOST FILES", x + 6, y + 62, 36, 4.6, INK)
    _contact(k, x + w / 2, floor, 36)


def _chair(k, x, floor):
    """A chair back, the seat hidden by the counter."""
    rect(k, x - 14, floor - 148, 28, 52, (0.28, 0.32, 0.38), 51, lw=1.6)
    rect(k, x - 16, floor - 98, 32, 8, (0.22, 0.24, 0.30), 52, shadow=False, lw=1.2)


def _leg(k, x, lip_b):
    """A leg clear of the people standing behind it, with a foot and its own shadow."""
    h = DESK_FEET - lip_b
    rect(k, x, lip_b, 8, h - 5, FRONT, 61, shadow=False, lw=1.4)
    rect(k, x - 3, DESK_FEET - 5, 14, 5, FRONT_DARK, 63, shadow=False, lw=1.1)
    _contact(k, x + 4, DESK_FEET, 16)


def _counter(k):
    """One top, one front, two legs clear of the people, a rail under the top."""
    top = TOP_FRONT
    back = top - TOP_D
    lip_b = top + LIP
    cut(k, [(CX0 + 10, top), (CX1 - 2, top), (CX1 - 8, back), (CX0 + 18, back)],
        TOP, shadow=False, lw=1.7)
    rect(k, CX0 + 8, top, CX1 - CX0 - 10, LIP, FRONT, 60, shadow=False, lw=1.6)
    rect(k, CX0 + 8, top + LIP - 5, CX1 - CX0 - 10, 5, FRONT_DARK, 65, shadow=False, lw=1.0)
    rect(k, CX0 + 22, lip_b, CX1 - CX0 - 48, 4, FRONT_DARK, 64, shadow=False, lw=1.0)
    c = k.c
    c.set_source_rgba(*SHADE, 0.20)
    c.rectangle(CX0 + 16, lip_b + 2, CX1 - CX0 - 36, 11)
    c.fill()
    _leg(k, CX0 + 4, lip_b)
    _leg(k, CX1 - 24, lip_b)


def _nameplate(k, x, y):
    """Both lines inside the plate. The stock plate's second line fell out the bottom."""
    fs.baby_photo(k, x, y - 8, 0.42)
    rect(k, x + 12, y - 24, 58, 22, (0.15, 0.17, 0.22), 730, shadow=False, lw=1.2)
    c = k.c
    _fit(c, "ASSISTANT", x + 12, y - 14, 58, 6, (1, 1, 1))
    _fit(c, "TO DON", x + 12, y - 5, 58, 6, (1, 1, 1))


def _desk_things(k, hide_plan):
    """Monitor, the plan, the plate, the mug. The tiny extras were noise."""
    top = TOP_FRONT
    surface = top - 10
    s3.monitor(k, 676, surface, 0.38)
    c = k.c
    c.save()
    c.translate(676, surface)
    c.scale(0.38, 0.38)
    c.set_source_rgba(0.86, 0.93, 0.96, 0.75)
    c.set_line_width(6)
    c.move_to(-20, -41)
    c.line_to(2, -24)
    c.stroke()
    c.restore()
    if not hide_plan:
        c.save()
        c.translate(708, surface - 2)
        c.rotate(-0.02)
        fs.PLAN_V2[0] = True
        try:
            fs.plan_taped(k, 0, 0, 0.15)
        finally:
            fs.PLAN_V2[0] = False
        c.restore()
    _nameplate(k, 752, surface + 6)
    mfs.mug(k, 832, surface - 2, 0.20)


def _shredder(k):
    """The body is the show's shredder. The top, the strips and ARCHIVE are this room only."""
    import acts_ob as ac
    x, floor, s = SHRED_AT
    ac.shredder(k, x, floor, s, fill=0.0)
    c = k.c
    c.save()
    c.translate(x, floor)
    c.scale(s, s)
    cut(k, [(34, -108), (46, -100), (46, -8), (34, 0)], (0.24, 0.26, 0.32), shadow=False, lw=1.5)
    cut(k, [(-28, -112), (34, -112), (44, -126), (-20, -128)], (0.28, 0.30, 0.36), shadow=False, lw=1.5)
    rect(k, -10, -123, 34, 8, (0.08, 0.08, 0.10), 21, shadow=False, lw=1.3)
    c.save()
    c.rectangle(-26, -58, 52, 42)
    c.clip()
    for i, col in enumerate(((0.95, 0.95, 0.93), (0.55, 0.57, 0.60), (0.90, 0.91, 0.92),
                             (0.70, 0.72, 0.74), (0.97, 0.97, 0.95))):
        c.save()
        c.translate(-18 + i * 9, -46 + (i % 2) * 10)
        c.rotate(-0.5 + i * 0.28)
        c.set_source_rgb(*col)
        c.rectangle(-8, -1.6, 16, 3.2)
        c.fill()
        c.restore()
    c.restore()
    rect(k, -22, -96, 44, 12, (0.18, 0.20, 0.24), 22, shadow=False, lw=1.1)
    _fit(c, "ARCHIVE", -22, -87, 44, 7, (0.95, 0.95, 0.93))
    c.restore()
    _contact(k, x + 6, floor, 56)


def _people(k):
    import fs_storyboard_v17 as sb
    _chair(k, PAM[0] - 36, BACK)
    _chair(k, MOM[0] + 30, BACK)
    _contact(k, PAM[0], PAM[1], 28)
    sb.pam_taping(k, *PAM)
    _contact(k, MOM[0], MOM[1], 28)
    mfs.mom(k, *MOM, "fists", "unimpressed", look=(-0.9, 0.3), chin=True)
    _counter(k)
    _desk_things(k, _people.hide_plan)
    _cabinet(k, 540, CAB)
    if not SKIP_CLIENT[0]:
        _contact(k, CLIENT[0], CLIENT[1], 36)
        sb.client(k, *CLIENT, "stand", "confident", (0.9, 0))
    _contact(k, ROBOT[0], ROBOT[1], 24)
    fs.robot_finger(k, *ROBOT)
    _contact(k, SOFIA[0], SOFIA[1], 26)
    sfs.sofia(k, *SOFIA, "hold", "charm", look=(0.6, -0.2))
    _shredder(k)
    _contact(k, DON[0], DON[1], 34)
    sb.DON_STATE[0] = ("up", "up")
    try:
        sb.don(k, *DON, "stand", "neutral", (-1, 0))
    finally:
        sb.DON_STATE[0] = None


_people.hide_plan = False
# Walk frames set this. Off, the home Client is drawn and the locked stills do not change.
SKIP_CLIENT = [False]


def draw(k, hide_plan=False):
    """The whole room, already framed for 960x540. Call it under bp_frame.view."""
    _people.hide_plan = hide_plan
    saved_door = st.DOOR
    st.DOOR = (18, F - 214, 116, 214)
    try:
        x0, w = _span()
        k.c.set_source_rgb(*WALL)
        k.c.rectangle(x0, -40, w, F + 40)
        k.c.fill()
        _wall_band(k)
        _floor(k)
        _ambience(k)
        st.door(k, 0.85)
        _glass_cool(k)
        _mat(k)
        _ficus(k)
        fs.screen(k, "query", 148, 48, 136, 72)
        _logo(k)
        _poster(k, 300, 78)
        fs.portrait(k, 508, 128, 0.72)
        _clock(k, 612, 118)
        _board(k, 668, 88)
        _cctv(k, 756, 100)
        _certificate(k, 796, 96)
        _ceo_door(k)
        _people(k)
    finally:
        st.DOOR = saved_door


def ground_plan(path):
    """Top view. Three rows, the same zones. Not a render of the room."""
    W, H = 980, 420
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    c = cairo.Context(surf)
    c.set_source_rgb(0.96, 0.94, 0.90)
    c.paint()
    rows = (("back  Pam, Mom, counter", 70, (0.75, 0.82, 0.78)),
            ("mid  Client, robot, Sofia", 160, (0.95, 0.90, 0.78)),
            ("front  Don, shredder", 250, (0.90, 0.82, 0.78)))
    for name, y, col in rows:
        c.set_source_rgb(*col)
        c.rectangle(40, y, 900, 70)
        c.fill()
        c.set_source_rgb(*INK)
        c.select_font_face("Inter", 0, 1)
        c.set_font_size(16)
        c.move_to(52, y + 28)
        c.show_text(name)
    c.set_source_rgb(*INK)
    c.set_font_size(13)
    c.move_to(40, 36)
    c.show_text("A  0-280          B  280-570          C  570-960")
    c.move_to(40, 360)
    c.show_text("Floor band on the wide frame is y 400-540, 26 percent. Scales stay the home scales.")
    for label, x, y in (("Client", 132, 195), ("robot", 248, 195), ("Sofia", 348, 195),
                        ("Don", 476, 285), ("shredder", 556, 285),
                        ("cabinet", 562, 100), ("Pam", 694, 115), ("Mom", 778, 115)):
        c.arc(x, y, 8, 0, 2 * math.pi)
        c.fill()
        c.move_to(x + 12, y + 4)
        c.show_text(label)
    surf.write_to_png(path)
    return path
