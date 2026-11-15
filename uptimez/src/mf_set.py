"""v2 (mf_set_v1.py = v1, kept): the empty chair reads as an office chair (rounded back, lighter grey, a
stitched panel, a headrest bump); cameras take an optional 4th value, a dutch roll in radians.
Set for "Mandatory Fun": the Day One office set up as a training room. World units as tg_set.py (floor line
FLOOR_Y; a 9:16 camera (cx, cy, z) maps the world into 540 x 960). Left to right:
- a door in the far-left wall (Don bangs it open in shot 3; Sofia walks out through it in shot 11);
- the projector screen on a tripod with the MANDATORY FUN slide (navy title bar, the title huge, "AI policy
  training" small, one cheesy party-popper clip-art, "1 / 48" in the corner), the robot beside it;
- the long table centre-right, seats fixed: Sofia, an EMPTY CHAIR (Don's: where he ends up chained), Pam.
Bare, as the concept: the Day One wall and the UptimeZ sign, nothing else. The slide is the only "fun"."""
import math
import cairo
import kit
import pt42
import tg_set as ts
from kit import INK, cut, rect, ellipse

FLOOR_Y = ts.FLOOR_Y
FEET = ts.FEET
FEET_BACK = ts.FEET_BACK
SEAT_DROP = ts.SEAT_DROP
TABLE_TOP = ts.TABLE_TOP
TABLE_X0, TABLE_X1 = 470, 930
POS = {"door": 70, "screen": 270, "robot": 420, "sofia": 540, "don": 690, "pam": 840}
DOOR_W, DOOR_H = 132, 430
SCREEN = (150, 228, 250, 180)          # x, y, w, h of the slide
NAVY = (0.12, 0.17, 0.33)
DOOR = (0.74, 0.62, 0.46)
DOOR_DARK = (0.56, 0.45, 0.31)
CHAIR = (0.20, 0.22, 0.27)

CAMS = {"wide": (520, 470, 0.66), "slide": (330, 400, 1.35), "door": (95, 470, 1.25), "two": (665, 520, 1.6),
        "three": (690, 520, 1.25), "robot": (420, 420, 2.0), "approve": (600, 470, 1.2), "exit": (480, 480, 0.68)}


def wall(k):
    rect(k, -600, -400, 2400, FLOOR_Y + 400, kit.WALL, 100, shadow=False, outline=False)
    rect(k, -600, FLOOR_Y, 2400, 900, kit.FLOOR, 101, shadow=False)
    rect(k, -600, FLOOR_Y - 10, 2400, 16, (0.62, 0.5, 0.36), 102, shadow=False, lw=2)
    pt42.wall_sign(k, 700, 330, 30)


def door(k, open_=0.0):
    """open_ 0 = shut; 1 = banged wide open (the panel swings into the room, we see the dark corridor)."""
    c = k.c
    x0, y0 = POS["door"] - DOOR_W / 2, FLOOR_Y - DOOR_H
    rect(k, x0 - 10, y0 - 10, DOOR_W + 20, DOOR_H + 10, (0.93, 0.92, 0.88), 110, shadow=False, lw=2.2)   # frame
    rect(k, x0, y0, DOOR_W, DOOR_H, (0.18, 0.19, 0.24), 111, shadow=False, lw=2)                       # corridor
    c.set_source_rgba(1, 1, 1, 0.08); c.rectangle(x0, FLOOR_Y - 40, DOOR_W, 40); c.fill()
    w = DOOR_W * (1 - 0.82 * open_)                                     # the panel, foreshortened as it swings
    pts = [(x0, y0), (x0 + w, y0 - 14 * open_), (x0 + w, FLOOR_Y + 14 * open_), (x0, FLOOR_Y)]
    cut(k, pts, DOOR, lw=2.2)
    if open_ < 0.5:
        for (yy, hh) in ((y0 + 30, 160), (y0 + 220, 170)):              # two panels
            rect(k, x0 + 18, yy, w - 36, hh, DOOR_DARK, 112 + yy, shadow=False, lw=1.6)
        ellipse(k, x0 + w - 18, y0 + 222, 7, 7, (0.80, 0.70, 0.30), 113, shadow=False, lw=1.6)        # knob
        rect(k, x0 + 30, y0 + 58, w - 60, 26, (0.97, 0.97, 0.95), 114, shadow=False, lw=1.4)          # plaque
        c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10)
        t = "TRAINING"; e = c.text_extents(t)
        c.set_source_rgb(*INK); c.move_to(x0 + w / 2 - e.x_advance / 2, y0 + 75); c.show_text(t)


def party_popper(c, x, y, s):
    """Cheesy clip-art: a striped cone, a burst of confetti."""
    c.save(); c.translate(x, y); c.scale(s, s); c.rotate(-0.5)
    c.move_to(0, 0); c.line_to(-9, 30); c.line_to(9, 30); c.close_path()
    c.set_source_rgb(0.95, 0.35, 0.55); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1.4); c.stroke()
    c.set_source_rgb(1.0, 0.85, 0.2)
    for i in range(3):
        c.move_to(-3 - i * 2, 9 + i * 7); c.line_to(3 + i * 2, 9 + i * 7); c.set_line_width(2); c.stroke()
    cols = [(0.2, 0.6, 1.0), (1.0, 0.75, 0.1), (0.3, 0.85, 0.4), (0.95, 0.3, 0.3), (0.7, 0.4, 0.9)]
    for i in range(14):
        a = -math.pi / 2 + (i - 6.5) * 0.17
        r = 14 + (i * 7) % 16
        c.set_source_rgb(*cols[i % 5])
        c.save(); c.translate(math.cos(a) * r, -4 + math.sin(a) * r); c.rotate(i)
        c.rectangle(-2, -1, 4, 2.2); c.fill(); c.restore()
    c.restore()


def slide(k, x, y, w, h, alpha=1.0):
    """The MANDATORY FUN slide (also the title card at frame 0)."""
    c = k.c
    c.save()
    c.rectangle(x, y, w, h); c.clip()
    c.set_source_rgb(0.99, 0.99, 0.98); c.paint_with_alpha(alpha)
    c.set_source_rgba(*NAVY, alpha); c.rectangle(x, y, w, h * 0.16); c.fill()
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    c.set_font_size(h * 0.07); t = "UptimeZ  ·  HR"
    c.set_source_rgba(1, 1, 1, alpha); c.move_to(x + w * 0.04, y + h * 0.105); c.show_text(t)
    c.select_font_face("Lilita One", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    for txt, ty, size in (("MANDATORY", 0.46, 0.25), ("FUN", 0.74, 0.31)):
        c.set_font_size(h * size); e = c.text_extents(txt)
        sc = min(1.0, w * 0.84 / e.x_advance)
        c.save(); c.translate(x + w / 2, y + h * ty); c.scale(sc, 1)
        c.move_to(-e.x_advance / 2, 0); c.set_source_rgba(*NAVY, alpha); c.show_text(txt); c.restore()
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL); c.set_font_size(h * 0.065)
    t = "AI policy training"; e = c.text_extents(t)
    c.set_source_rgba(0.40, 0.44, 0.52, alpha); c.move_to(x + w / 2 - e.x_advance / 2, y + h * 0.88); c.show_text(t)
    c.set_font_size(h * 0.045); t = "1 / 48"; e = c.text_extents(t)
    c.move_to(x + w - e.x_advance - w * 0.03, y + h * 0.96); c.show_text(t)
    party_popper(c, x + w * 0.12, y + h * 0.80, h / 200)
    c.restore()
    c.set_source_rgb(*INK); c.set_line_width(2); c.rectangle(x, y, w, h); c.stroke()


def projector_screen(k, on=True):
    c = k.c
    x, y, w, h = SCREEN
    cx = x + w / 2
    c.set_source_rgb(*INK); c.set_line_width(4); c.set_line_cap(1)               # tripod
    for dx in (-60, 0, 60):
        c.move_to(cx, y + h + 10); c.line_to(cx + dx, FLOOR_Y + 30); c.stroke()
    c.move_to(cx, y - 14); c.line_to(cx, y + h + 10); c.stroke()
    rect(k, x - 14, y - 22, w + 28, 12, (0.30, 0.31, 0.36), 120, shadow=False, lw=2)  # roller case
    rect(k, x - 6, y - 10, w + 12, h + 16, (0.96, 0.96, 0.94), 121, lw=2)             # screen cloth
    if on:
        slide(k, x, y, w, h)
    rect(k, x - 4, y + h + 6, w + 8, 6, (0.30, 0.31, 0.36), 122, shadow=False, lw=1.6)  # bottom bar


def chair_back(k, x, seat_y=None, seed=0):
    """v2: an office chair back above the table at a seat (drawn before the sitter): rounded top, a headrest bump,
    a stitched panel, so the empty one reads as a chair, not a cabinet."""
    c = k.c
    yb = TABLE_TOP - 150
    col, dark, light = (0.36, 0.39, 0.46), (0.24, 0.26, 0.31), (0.48, 0.51, 0.58)
    c.save()

    def back(ox, oy):
        c.move_to(x - 44 + ox, TABLE_TOP + 6 + oy); c.line_to(x - 46 + ox, yb + 34 + oy)
        c.curve_to(x - 46 + ox, yb + 4 + oy, x - 30 + ox, yb - 2 + oy, x - 18 + ox, yb - 2 + oy)
        c.curve_to(x - 14 + ox, yb - 22 + oy, x + 14 + ox, yb - 22 + oy, x + 18 + ox, yb - 2 + oy)   # headrest bump
        c.curve_to(x + 30 + ox, yb - 2 + oy, x + 46 + ox, yb + 4 + oy, x + 46 + ox, yb + 34 + oy)
        c.line_to(x + 44 + ox, TABLE_TOP + 6 + oy); c.close_path()
    back(4, 5); c.set_source_rgba(0, 0, 0, 0.18); c.fill()
    back(0, 0)
    c.set_source_rgb(*col); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.2); c.stroke()
    c.move_to(x - 32, TABLE_TOP); c.line_to(x - 34, yb + 32); c.curve_to(x - 34, yb + 14, x - 22, yb + 10, x, yb + 10)
    c.curve_to(x + 22, yb + 10, x + 34, yb + 14, x + 34, yb + 32); c.line_to(x + 32, TABLE_TOP)
    c.set_source_rgb(*light); c.set_line_width(2); c.set_dash([5, 4]); c.stroke(); c.set_dash([])   # stitching
    c.set_source_rgba(1, 1, 1, 0.22); c.set_line_width(5); c.set_line_cap(1)
    c.move_to(x - 30, yb + 20); c.curve_to(x - 24, yb + 12, x - 14, yb + 10, x - 6, yb + 10); c.stroke()  # sheen
    c.restore()


def set_dressing(k, door_open=0.0, slide_on=True):
    wall(k)
    door(k, door_open)
    projector_screen(k, slide_on)


def table(k):
    """Drawn after the characters: the table top, the apron and the modesty panel. Nothing on it but the notebook,
    which sofia_mf draws in her hands."""
    c = k.c
    t0 = TABLE_TOP
    cut(k, [(TABLE_X0 + 10, t0), (TABLE_X1 - 10, t0), (TABLE_X1, t0 + 18), (TABLE_X0, t0 + 18)], ts.WOOD, lw=2.2)
    rect(k, TABLE_X0, t0 + 18, TABLE_X1 - TABLE_X0, 12, ts.WOOD_DARK, 970, shadow=False, lw=2)
    rect(k, TABLE_X0 + 12, t0 + 30, TABLE_X1 - TABLE_X0 - 24, FEET + 14 - (t0 + 30), ts.WOOD, 972, lw=2)
    c.set_source_rgb(*ts.WOOD_DARK); c.set_line_width(2)
    for gx in range(TABLE_X0 + 80, TABLE_X1 - 40, 120):
        c.move_to(gx, t0 + 32); c.line_to(gx, FEET + 12); c.stroke()


seated = ts.seated


def to_screen(cam, x, y):
    cx, cy, z = cam[:3]
    r = cam[3] if len(cam) > 3 else 0.0
    dx, dy = (x - cx) * z, (y - cy) * z
    return 270 + dx * math.cos(r) - dy * math.sin(r), 480 + dx * math.sin(r) + dy * math.cos(r)


def with_cam(c, cam):
    """(cx, cy, z[, roll]): roll in radians for a dutch angle."""
    cx, cy, z = cam[:3]
    c.translate(270, 480)
    if len(cam) > 3:
        c.rotate(cam[3])
    c.scale(z, z); c.translate(-cx, -cy)
