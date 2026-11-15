"""Set for "Secret Santa", v1: the Day One office at Christmas. World units as tg_set / mf_set (floor line FLOOR_Y,
a 9:16 camera (cx, cy, z[, roll]) maps the world into 540 x 960). Left to right:
- the door in the far-left wall (Don bangs it open in shot 3), plaque OFFICE;
- the robot's spot by the Secret Santa table;
- the Secret Santa table: a small table with a white cloth, Pam's present (red paper, gold ribbon, the big cream tag)
  and two plainer gifts beside it so hers stands out;
- Sofia's desk centre-right (she sits behind it), a fairy-light string swagged above it;
- on the wall: red/green paper chains along the top (one loop has come loose and sags), the hand-drawn SECRET SANTA
  sign taped crooked (marker on printer paper, a small HR-APPROVED stamp in the corner: the stamp's plant), the
  Day One wall and the UptimeZ sign. No tree.
Normal office light; the fairy lights twinkle softly (t)."""
import math
import cairo
import kit
import tg_set as ts
import mf_set as ms
from kit import INK, cut, rect, ellipse

FLOOR_Y, FEET, FEET_BACK, SEAT_DROP, TABLE_TOP = ms.FLOOR_Y, ms.FEET, ms.FEET_BACK, ms.SEAT_DROP, ms.TABLE_TOP
SEAT = FEET + SEAT_DROP
POS = {"door": 70, "robot": 250, "don": 430, "table": 430, "pam": 600, "sofia": 790}
SST = (345, 515)                     # the Secret Santa table
DESK = (660, 940)                    # Sofia's desk
RED = (0.80, 0.14, 0.16)
GREEN = (0.16, 0.55, 0.30)
GOLD = (0.93, 0.74, 0.22)
CLOTH = (0.97, 0.97, 0.95)
to_screen, with_cam = ms.to_screen, ms.with_cam
seated = ms.seated


def door(k, open_=0.0):
    ms.door(k, open_)
    if open_ < 0.5:                                         # the plaque: OFFICE, not TRAINING
        c = k.c
        x0, y0 = POS["door"] - ms.DOOR_W / 2, FLOOR_Y - ms.DOOR_H
        rect(k, x0 + 30, y0 + 58, ms.DOOR_W - 60, 26, (0.97, 0.97, 0.95), 114, shadow=False, lw=1.4)
        c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10)
        t = "OFFICE"; e = c.text_extents(t)
        c.set_source_rgb(*INK); c.move_to(x0 + ms.DOOR_W / 2 - e.x_advance / 2, y0 + 75); c.show_text(t)


def paper_chains(k, x0=150, x1=1000, y=232):
    """Red/green paper loops along the top of the wall; one stretch has come loose and sags (x 520-650)."""
    c = k.c
    n = int((x1 - x0) / 14)
    for i in range(n):
        x = x0 + i * 14
        sag = 0.0
        if 520 <= x <= 650:
            t = (x - 520) / 130
            sag = 70 * math.sin(math.pi * t) ** 1.2
        else:
            seg = ((x - x0) % 170) / 170
            sag = 18 * math.sin(math.pi * seg)
        col = RED if i % 2 == 0 else GREEN
        for wd, cl in ((5.6, INK), (3.4, col)):
            c.new_path()
            c.save(); c.translate(x, y + sag); c.rotate(0.5 if i % 2 else -0.2)
            c.scale(8, 5); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
            c.set_source_rgb(*cl); c.set_line_width(wd); c.stroke()
    for x in (x0 - 4, x0 + 170 * 4, x1):                      # the tape bits
        if 520 <= x <= 650:
            continue
        rect(k, x - 6, y - 8, 12, 10, (0.95, 0.93, 0.80), 900 + x, shadow=False, lw=0.8)


def santa_sign(k, x=330, y=318, rot=-0.06):
    """Marker on printer paper, taped crooked; a little HR-APPROVED stamp in the corner."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(rot)
    rect(k, -78, -46, 156, 96, (0.995, 0.995, 0.99), 920, lw=1.8)
    for (tx, ty, r) in ((-72, -46, -0.5), (72, -46, 0.5)):
        c.save(); c.translate(tx, ty); c.rotate(r)
        c.set_source_rgba(0.95, 0.92, 0.75, 0.9); c.rectangle(-12, -5, 24, 10); c.fill(); c.restore()
    c.select_font_face("Permanent Marker", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    for txt, ty, col, sz in (("SECRET", -10, RED, 30), ("SANTA", 24, GREEN, 30)):
        c.set_font_size(sz); e = c.text_extents(txt)
        c.move_to(-e.x_advance / 2 - 6, ty); c.text_path(txt)
        c.set_source_rgb(*col); c.fill()
    c.set_source_rgb(*RED); c.set_line_width(2.4)                 # a wobbly marker star
    c.save(); c.translate(56, -28)
    for i in range(5):
        a = -math.pi / 2 + i * 4 * math.pi / 5
        (c.move_to if i == 0 else c.line_to)(9 * math.cos(a), 9 * math.sin(a))
    c.close_path(); c.stroke(); c.restore()
    c.save(); c.translate(48, 36); c.rotate(-0.25)                 # HR-APPROVED, the stamp's plant
    c.set_source_rgb(0.10, 0.55, 0.32); c.set_line_width(1.4)
    c.rectangle(-22, -7, 44, 13); c.stroke()
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(6.2)
    c.move_to(-19, 2.5); c.show_text("HR-APPROVED")
    c.restore()
    c.restore()


def fairy_lights(k, x0=DESK[0] - 10, x1=DESK[1] + 10, y=402, t=0.0):
    c = k.c
    pts = []
    for i in range(41):
        u = i / 40
        x = x0 + (x1 - x0) * u
        sag = 26 * math.sin(math.pi * ((u * 2) % 1.0))
        pts.append((x, y + sag))
    c.set_source_rgb(0.22, 0.30, 0.20); c.set_line_width(1.6)
    c.move_to(*pts[0])
    for p in pts[1:]:
        c.line_to(*p)
    c.stroke()
    warm = [(1.0, 0.82, 0.38), (1.0, 0.55, 0.45), (0.98, 0.92, 0.60)]
    for i, (x, yy) in enumerate(pts[1:-1:3]):
        a = 0.55 + 0.45 * (0.5 + 0.5 * math.sin(t * 5 + i * 1.7))
        col = warm[i % 3]
        c.set_source_rgba(*col, 0.28 * a); c.arc(x, yy + 7, 9, 0, 2 * math.pi); c.fill()
        c.set_source_rgba(*col, 0.6 + 0.4 * a); c.save(); c.translate(x, yy + 6); c.scale(3.2, 4.4)
        c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()


SIGN_FIX = [False]   # full animation: the UptimeZ sign moved where every camera shows it whole or not at all


def wall(k, t=0.0):
    if SIGN_FIX[0]:
        import pt42
        rect(k, -600, -400, 2400, FLOOR_Y + 400, kit.WALL, 100, shadow=False, outline=False)
        rect(k, -600, FLOOR_Y, 2400, 900, kit.FLOOR, 101, shadow=False)
        rect(k, -600, FLOOR_Y - 10, 2400, 16, (0.62, 0.5, 0.36), 102, shadow=False, lw=2)
        pt42.wall_sign(k, 580, 326, 26)
    else:
        ms.wall(k)
    paper_chains(k)
    santa_sign(k)


def present(k, x, y, w, h, paper, ribbon, seed=0, stripes=None):
    """(x, y) = bottom centre."""
    c = k.c
    rect(k, x - w / 2, y - h, w, h, paper, seed, lw=2)
    if stripes:
        c.save(); c.rectangle(x - w / 2, y - h, w, h); c.clip()
        c.set_source_rgba(*stripes, 0.8); c.set_line_width(4)
        for i in range(-6, 10):
            c.move_to(x - w / 2 + i * 10, y); c.line_to(x - w / 2 + i * 10 + h, y - h); c.stroke()
        c.restore()
        c.set_source_rgb(*INK); c.set_line_width(2); c.rectangle(x - w / 2, y - h, w, h); c.stroke()
    rect(k, x - 4, y - h, 8, h, ribbon, seed + 1, shadow=False, lw=1.2)
    for sx in (-1, 1):                                           # the bow
        c.save(); c.translate(x + sx * 9, y - h - 6); c.rotate(sx * 0.4); c.scale(10, 6)
        c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        c.set_source_rgb(*ribbon); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1.6); c.stroke()
    ellipse(k, x, y - h - 4, 4, 4, ribbon, seed + 2, shadow=False, lw=1.4)


def santa_table(k, tag_bars=(), tag_blank=False, pams=True):
    """The small table with a white cloth; drawn after the characters standing behind it."""
    import pam_sheet_ss as pss
    c = k.c
    x0, x1 = SST
    t0 = TABLE_TOP + 20
    rect(k, x0 + 14, t0 + 10, 8, FEET - t0 - 10, (0.45, 0.32, 0.20), 950, lw=1.6)
    rect(k, x1 - 22, t0 + 10, 8, FEET - t0 - 10, (0.45, 0.32, 0.20), 951, lw=1.6)
    cut(k, [(x0, t0), (x1, t0), (x1 + 6, t0 + 46), (x0 - 6, t0 + 46)], CLOTH, lw=2)       # the cloth
    c.set_source_rgb(0.85, 0.85, 0.82); c.set_line_width(1.4)
    for gx in range(x0 + 20, x1, 32):
        c.move_to(gx, t0 + 6); c.line_to(gx - 2, t0 + 44); c.stroke()
    present(k, x0 + 36, t0 + 4, 40, 34, (0.20, 0.42, 0.70), (0.97, 0.97, 0.97), 960, stripes=(0.95, 0.95, 0.98))
    present(k, x1 - 34, t0 + 4, 36, 28, GREEN, (0.97, 0.97, 0.97), 963)
    if pams:
        present(k, (x0 + x1) / 2 + 4, t0 + 4, 62, 48, RED, GOLD, 966)              # Pam's, the biggest
        pss.k = k
        pss.gift_tag(c, (x0 + x1) / 2 + 30, t0 - 6, 0.62, rot=0.22, bars=tag_bars, blank=tag_blank)


def desk(k):
    """Sofia's desk, drawn after her: a top, an apron, a modesty panel."""
    c = k.c
    x0, x1 = DESK
    t0 = TABLE_TOP
    cut(k, [(x0 + 10, t0), (x1 - 10, t0), (x1, t0 + 18), (x0, t0 + 18)], ts.WOOD, lw=2.2)
    rect(k, x0, t0 + 18, x1 - x0, 12, ts.WOOD_DARK, 970, shadow=False, lw=2)
    rect(k, x0 + 12, t0 + 30, x1 - x0 - 24, FEET + 14 - (t0 + 30), ts.WOOD, 972, lw=2)


def backdrop(k, door_open=0.0, t=0.0):
    wall(k, t)
    door(k, door_open)
    fairy_lights(k, t=t)
    ms.chair_back(k, POS["sofia"], seed=130)
