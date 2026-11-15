"""Set for the Thanksgiving film "Raises for Everyone": the Day One office wall, a conference table pulled out for
the party. World units as xmas_set.py (floor line FLOOR_Y; a 9:16 camera (cx, cy, z) maps the world into 540 x 960).
- wall, floor, baseboard and the UptimeZ sign from Day One;
- a paper leaf garland along the top, and one printed banner: THANKFUL FOR OUR EMPLOYEES* with a tiny footnote
  in its corner (*terms and conditions apply), a quiet gag that is never pointed at;
- the long table in front: Sofía and Pam sit on the left (only their upper bodies show over it), Don stands at the
  head on the right, the robot stands behind his shoulder; Pam "stands" in shot 9 by rising SEAT_DROP;
- on the table: the roast turkey on a platter (legs=2, then 1 after Don tears one off in shot 8), two sad
  supermarket sides in plastic tubs with price stickers, the form, two small paper pumpkins at the ends.
Kept simple: one garland, one banner, the table. No desk flag: the flag is Don's tie."""
import math
import cairo
import kit
import pt42
import pam_tg as pt
import don_tg as dt
from kit import INK, cut, rect, ellipse, text

FLOOR_Y = 660
FEET = 730                   # standing feet (Don)
FEET_BACK = 712              # the robot, a step behind Don
SEAT_DROP = 74               # seated characters sink this much behind the table
TABLE_TOP = 628              # top edge of the table surface
TABLE_X0, TABLE_X1 = 70, 700
POS = {"sofia": 175, "pam": 300, "don": 560, "robot": 650, "turkey": 470, "form": 540}
LEAVES = [(0.86, 0.42, 0.12), (0.90, 0.66, 0.18), (0.70, 0.20, 0.10), (0.55, 0.30, 0.12)]
WOOD = (0.55, 0.36, 0.22)
WOOD_DARK = (0.42, 0.27, 0.16)
CLOTH = (0.97, 0.94, 0.86)
TURKEY = (0.76, 0.45, 0.18)
TURKEY_DARK = (0.55, 0.28, 0.10)
PLATTER = (0.93, 0.94, 0.96)
PUMPKIN = (0.92, 0.50, 0.14)
STICKER = (1.0, 0.86, 0.20)

CAMS = {"wide": (390, 470, 0.84), "table_cu": (505, 600, 3.0), "two_shot": (238, 520, 1.55),
        "don": (545, 480, 1.7), "robot": (640, 400, 2.2), "don_sofia": (380, 500, 1.4), "pam_cu": (300, 470, 2.1),
        "don_robot": (590, 470, 1.6)}


def wall(k):
    rect(k, -600, -400, 2200, FLOOR_Y + 400, kit.WALL, 100, shadow=False, outline=False)
    rect(k, -600, FLOOR_Y, 2200, 900, kit.FLOOR, 101, shadow=False)
    rect(k, -600, FLOOR_Y - 10, 2200, 16, (0.62, 0.5, 0.36), 102, shadow=False, lw=2)
    pt42.wall_sign(k, 410, 300, 30)


def garland(k, x0, x1, y, sag=28, boil=0):
    """A string of paper leaves in three swags."""
    c = k.c
    seg = (x1 - x0) / 3
    n = 0
    for j in range(3):
        a, b = x0 + j * seg, x0 + (j + 1) * seg
        c.set_source_rgb(*INK); c.set_line_width(2)
        c.move_to(a, y); c.curve_to(a + seg * 0.3, y + sag, b - seg * 0.3, y + sag, b, y); c.stroke()
        for i in range(1, 8):
            t = i / 8
            px_ = (1 - t) ** 3 * a + 3 * (1 - t) ** 2 * t * (a + seg * 0.3) + 3 * (1 - t) * t * t * (b - seg * 0.3) + t ** 3 * b
            py_ = (1 - t) ** 3 * y + 3 * (1 - t) ** 2 * t * (y + sag) + 3 * (1 - t) * t * t * (y + sag) + t ** 3 * y
            rot = (0.5 if n % 2 else -0.4) + 0.08 * ((n + boil) % 2)
            pt.maple_leaf(c, px_, py_ + 9, 10, math.pi + rot)
            c.set_source_rgb(*LEAVES[n % 4]); c.fill_preserve()
            c.set_source_rgb(*INK); c.set_line_width(1.4); c.stroke()
            n += 1


def banner(k, x, y, w=420, h=50):
    """Printed office banner; the footnote is tiny on purpose."""
    c = k.c
    rect(k, x, y, w, h, (1, 1, 1), 905, lw=2.2)
    c.set_source_rgb(*LEAVES[0]); c.rectangle(x + 2, y + 2, w - 4, 6); c.fill()
    c.rectangle(x + 2, y + h - 8, w - 4, 6); c.fill()
    c.save()
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(23)
    t = "THANKFUL FOR OUR EMPLOYEES*"
    tw = c.text_extents(t).x_advance
    c.set_source_rgb(0.45, 0.18, 0.06); c.move_to(x + (w - tw) / 2, y + 33); c.show_text(t)
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL); c.set_font_size(5.5)
    f = "*terms and conditions apply"
    c.set_source_rgb(0.3, 0.3, 0.3); c.move_to(x + w - 8 - c.text_extents(f).x_advance, y + h - 10); c.show_text(f)
    c.restore()
    for tx in (x + 10, x + w - 10):                        # tape at the corners
        c.save(); c.translate(tx, y + 2); c.rotate(0.6 if tx < x + w / 2 else -0.6)
        c.set_source_rgba(0.96, 0.92, 0.70, 0.9); c.rectangle(-8, -3, 16, 6); c.fill(); c.restore()


def set_dressing(k, boil=0):
    wall(k)
    garland(k, -60, 760, 100, boil=boil)
    banner(k, 200, 160)


def pumpkin(k, x, y, s=1.0, seed=0):
    c = k.c
    for dx_, rx in ((-9, 11), (9, 11), (0, 12)):
        ellipse(k, x + dx_ * s, y - 12 * s, rx * s, 12 * s, PUMPKIN, seed + int(dx_), shadow=False, lw=1.8)
    rect(k, x - 2.5 * s, y - 29 * s, 5 * s, 7 * s, (0.35, 0.45, 0.20), seed + 5, shadow=False, lw=1.4)


def tub(k, x, y, label, fill, seed=0):
    """A plastic supermarket tub with a clear lid and a yellow price sticker."""
    c = k.c
    cut(k, [(x - 20, y - 26), (x + 20, y - 26), (x + 16, y), (x - 16, y)], (0.95, 0.96, 0.97), shadow=False, lw=1.8)
    c.save(); c.rectangle(x - 19, y - 22, 38, 22); c.clip()
    c.set_source_rgb(*fill); c.rectangle(x - 19, y - 16, 38, 18); c.fill()
    c.restore()
    rect(k, x - 22, y - 30, 44, 5, (0.88, 0.92, 0.96), seed + 1, shadow=False, lw=1.4)       # lid
    rect(k, x - 14, y - 22, 28, 10, (1, 1, 1), seed + 2, shadow=False, lw=1.1)
    text(k, label, x, y - 14.5, 6, INK, bold=True)
    ellipse(k, x + 10, y - 6, 8, 6, STICKER, seed + 3, shadow=False, lw=1.1)
    text(k, "$1.99", x + 10, y - 4.2, 4.6, INK, bold=True)


def turkey(k, x, y, legs=2, s=1.0, seed=0):
    """Roast turkey on an oval platter; legs=1 after shot 8 (a bare stump where the leg was)."""
    c = k.c
    ellipse(k, x, y - 4 * s, 62 * s, 12 * s, PLATTER, seed, lw=2)
    ellipse(k, x, y - 26 * s, 44 * s, 26 * s, TURKEY, seed + 1, lw=2.2)
    c.set_source_rgba(1, 0.92, 0.75, 0.55)
    c.save(); c.translate(x - 12 * s, y - 38 * s); c.scale(16 * s, 6 * s); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
    c.set_source_rgb(*TURKEY_DARK); c.set_line_width(2 * s)
    c.arc(x + 6 * s, y - 22 * s, 18 * s, 0.9 * math.pi, 1.5 * math.pi); c.stroke()
    for side, present in ((-1, True), (1, legs >= 2)):
        if present:
            dt.turkey_leg(k, x + side * 46 * s, y - 34 * s, 0.55 * s, 160 if side < 0 else 20, 0, seed + 5 + side)
        else:
            ellipse(k, x + side * 36 * s, y - 22 * s, 8 * s, 7 * s, (0.95, 0.83, 0.68), seed + 9, shadow=False, lw=1.6)


def form_flat(k, x, y, s=1.0, ang=-0.1):
    """The form lying on the table (seen at a shallow angle)."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s * 0.42)
    c.set_source_rgb(1, 1, 1); c.rectangle(-26, -34, 52, 68); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(2.6); c.stroke()
    import brand
    c.set_source_rgb(*brand.GREEN); c.rectangle(-24, -32, 48, 8); c.fill()
    c.set_source_rgb(*INK); c.rectangle(-18, -14, 36, 6); c.fill()
    c.set_source_rgb(0.6, 0.6, 0.6)
    for i in range(3):
        c.rectangle(-18, 0 + i * 7, 28, 2.5); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(1.6); c.move_to(-14, 26); c.line_to(14, 26); c.stroke()
    c.restore()


def table(k, legs=2, form_at=None, props=True):
    """Drawn after the characters: the table top, the cloth, the apron and its legs, then the props."""
    c = k.c
    t0 = TABLE_TOP
    cut(k, [(TABLE_X0 + 10, t0), (TABLE_X1 - 10, t0), (TABLE_X1, t0 + 18), (TABLE_X0, t0 + 18)], WOOD, lw=2.2)
    rect(k, TABLE_X0, t0 + 18, TABLE_X1 - TABLE_X0, 12, WOOD_DARK, 970, shadow=False, lw=2)
    rect(k, TABLE_X0 + 12, t0 + 30, TABLE_X1 - TABLE_X0 - 24, FEET + 14 - (t0 + 30), WOOD, 972, lw=2)   # modesty panel
    c.set_source_rgb(*WOOD_DARK); c.set_line_width(2)
    for gx in range(TABLE_X0 + 80, TABLE_X1 - 40, 120):               # panel seams
        c.move_to(gx, t0 + 32); c.line_to(gx, FEET + 12); c.stroke()
    cut(k, [(TABLE_X0 + 30, t0 + 30), (TABLE_X1 - 30, t0 + 30), (TABLE_X1 - 36, t0 + 70), (TABLE_X0 + 36, t0 + 70)],
        CLOTH, shadow=False, lw=1.8)                                 # a runner hanging over the front
    if props:
        pumpkin(k, TABLE_X0 + 40, t0 + 8, 1.0, 980)
        pumpkin(k, TABLE_X1 - 40, t0 + 8, 0.85, 981)
        tub(k, 250, t0 + 10, "MASH", (0.96, 0.92, 0.78), 982)
        tub(k, 330, t0 + 10, "STUFFING", (0.70, 0.52, 0.32), 983)
        turkey(k, POS["turkey"], t0 + 12, legs, 1.0, 984)
    if form_at:
        form_flat(k, form_at[0], form_at[1] if len(form_at) > 1 else t0 + 8)


def seated(k, draw):
    """Draw a seated character: everything below the table top is hidden (their legs never show)."""
    c = k.c
    c.save(); c.rectangle(-2000, -2000, 5000, 2000 + TABLE_TOP + 30); c.clip()
    draw()
    c.restore()


def to_screen(cam, x, y):
    cx, cy, z = cam
    return 270 + (x - cx) * z, 480 + (y - cy) * z


def with_cam(c, cam):
    cx, cy, z = cam
    c.translate(270, 480); c.scale(z, z); c.translate(-cx, -cy)
