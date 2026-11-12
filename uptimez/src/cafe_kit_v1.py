"""Cafeteria set, props and bubble styles for "I Will Replace You" (UptimeZ Inc.), paper-cutout kit.

World layout (540x960 units at zoom 1, same as the Day One storyboards):
  FLOOR y 880. One table in front (top at TABLE_TOP), front panel down to the floor so the seated
  characters' legs never show: Sofía and Don are drawn standing, lowered behind it (feet below the floor
  line, hidden), with orange chair backs behind them. The robot rolls up BEHIND the table, between them
  and nearer Don, so it can face Don and point at Sofía without its arm crossing anyone.
  Pam sits at a smaller table further back on the right; the serving counter is off to the right.
Props: dome tray, bolt burgers (bright silver hex bolts in warm golden buns, oil secondary), wrench, bolt.
Bubbles: speech (from the Day One storyboard), thought cloud, dotted whisper, shout."""
import math
import cairo
import kit
import pt42
from kit import INK, cut, rect, ellipse, text

WALL = (0.95, 0.90, 0.80)
WAINSCOT = (0.78, 0.62, 0.44)
FLOOR_COL = (0.80, 0.76, 0.70)
TILE_LINE = (0.70, 0.66, 0.60)
TABLE_TOP_COL = (0.92, 0.92, 0.90)
TABLE_FRONT = (0.62, 0.48, 0.34)
CHAIR = (0.95, 0.60, 0.16)
CHALK = (0.16, 0.30, 0.24)
COUNTER = (0.72, 0.75, 0.79)
BUN = (0.95, 0.68, 0.28)
BUN_DARK = (0.80, 0.50, 0.18)
SILVER = (0.86, 0.88, 0.92)
SILVER_DARK = (0.52, 0.55, 0.60)
OIL = (0.16, 0.12, 0.08)
PLATE = (1.0, 1.0, 1.0)

FLOOR = 880          # front plane: the bottom of the table's front panel
HORIZON = 700        # where the back wall meets the floor (things further back stand between this and FLOOR)
TABLE_TOP = 760
TABLE_X0, TABLE_X1 = 30, 510
SOF = (115, 880)       # (x, feet): drawn standing, clipped at the table top (seated() below)
DON = (420, 892)
ROBOT = (305, 842)     # behind the table, between them and nearer Don; the wheel is hidden by the table
PAM = (625, 770)       # back table on the floor, further back and smaller, right of the robot's path
PAM_S = 0.6


# ------------------------------------------------------------------ room
def room(k, seed=1200):
    c = k.c
    rect(k, -600, -400, 2400, HORIZON + 400, WALL, seed, shadow=False, outline=False)
    rect(k, -600, 540, 2400, HORIZON - 540, WAINSCOT, seed + 1, shadow=False, outline=False)
    rect(k, -600, 534, 2400, 12, (0.62, 0.47, 0.32), seed + 2, shadow=False, lw=2)
    rect(k, -600, HORIZON, 2400, 700, FLOOR_COL, seed + 3, shadow=False, lw=2)
    c.set_source_rgb(*TILE_LINE); c.set_line_width(1.5)
    for i in range(-16, 30):                                   # floor tiles in light perspective
        x0 = 270 + i * 60
        c.move_to(270 + (x0 - 270) * 0.6, HORIZON); c.line_to(270 + (x0 - 270) * 1.6, HORIZON + 500); c.stroke()
    for y in (HORIZON + 20, HORIZON + 48, HORIZON + 86, HORIZON + 136, HORIZON + 200):
        c.move_to(-600, y); c.line_to(1800, y); c.stroke()
    for lx in (60, 300, 540):                                  # pendant lamps fill the upper wall
        c.set_source_rgb(*INK); c.set_line_width(2); c.move_to(lx, -400); c.line_to(lx, 200); c.stroke()
        cut(k, [(lx - 46, 250), (lx - 14, 196), (lx + 14, 196), (lx + 46, 250)], (0.17, 0.42, 0.40), lw=2.2)
        c.set_source_rgba(1.0, 0.92, 0.6, 0.35)
        c.save(); c.translate(lx, 252); c.scale(40, 8); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()


def menu_board(k, x, y, seed=1210):
    """Chalkboard: TODAY: CHEESEBURGER, with a chalk burger doodle."""
    c = k.c
    rect(k, x - 6, y - 6, 192, 122, (0.55, 0.40, 0.26), seed, lw=2.4)
    rect(k, x, y, 180, 110, CHALK, seed + 1, shadow=False, lw=1.8)
    chalk = (0.96, 0.96, 0.90)
    text(k, "TODAY:", x + 90, y + 26, 20, chalk, font="Permanent Marker")
    text(k, "CHEESEBURGER", x + 90, y + 58, 22, (1.0, 0.86, 0.40), font="Permanent Marker")
    c.set_source_rgb(*chalk); c.set_line_width(2)
    bx, by = x + 90, y + 88
    c.arc(bx, by, 14, math.pi, 2 * math.pi); c.stroke()
    c.move_to(bx - 15, by + 4); c.line_to(bx + 15, by + 4); c.stroke()
    c.move_to(bx - 14, by + 9); c.line_to(bx + 14, by + 9); c.stroke()


def counter(k, x, w=260, base=780, seed=1220):
    """Serving counter at the back right, standing on the floor (base y), with trays and a PICK UP sign."""
    rect(k, x, base - 120, w, 120, COUNTER, seed, lw=2.4)
    rect(k, x - 6, base - 130, w + 12, 14, (0.85, 0.87, 0.90), seed + 1, shadow=False, lw=2)
    for i in range(5):
        rect(k, x + 30, base - 140 - i * 7, 90, 6, (0.62, 0.66, 0.72), seed + 2 + i, shadow=False, lw=1.4)
    rect(k, x + 140, base - 250, 100, 40, (1, 1, 1), seed + 9, lw=2)
    text(k, "PICK UP", x + 190, base - 230, 15, INK, font="Inter", bold=True)


def seated(k, draw):
    """Draws a character only above the table top, so legs and feet never show behind the table."""
    c = k.c
    c.save(); c.rectangle(-2000, -2000, 5000, 2000 + TABLE_TOP); c.clip()
    out = draw()
    c.restore()
    return out


def chair_back(k, x, top, seed):
    rect(k, x - 58, top, 116, TABLE_TOP - top + 4, CHAIR, seed, lw=2.4)
    rect(k, x - 40, top + 14, 80, 10, (1.0, 0.72, 0.30), seed + 1, shadow=False, outline=False)


def table(k, x0=TABLE_X0, x1=TABLE_X1, top=TABLE_TOP, seed=1230):
    """Front panel down to the floor (hides seated legs) and a light laminate top."""
    rect(k, x0 + 10, top + 8, x1 - x0 - 20, FLOOR - top - 4, TABLE_FRONT, seed, lw=2.4)
    rect(k, x0, top - 6, x1 - x0, 16, TABLE_TOP_COL, seed + 1, lw=2.4)


def pam_corner(k, seed=1240):
    """Pam at a smaller table further back on the right, with her thermos."""
    c = k.c
    x, feet = PAM
    c.save(); c.translate(x, feet); c.scale(PAM_S, PAM_S); c.translate(-x, -feet)
    chair_back(k, x, feet - 190, seed)
    pt42._orig_person(k, "PAM", x, feet + 40, 1.0, pose="type", face="neutral", seed=44)
    rect(k, x - 120, feet - 150, 240, 150, TABLE_FRONT, seed + 1, lw=2.4)
    rect(k, x - 130, feet - 156, 260, 14, TABLE_TOP_COL, seed + 2, lw=2.4)
    import day1_kit as dk
    dk.thermos(k, x + 70, feet - 158)
    c.restore()


# ------------------------------------------------------------------ props
def plate(k, x, y, w=70, seed=1300):
    ellipse(k, x, y, w / 2, 7, PLATE, seed, lw=2)


def bolt(k, x, y, s=1.0, rot=0.0, seed=1310):
    """A big hex bolt seen from the side: hex head (bright face, dark flats) and a threaded shank."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    rect(k, -4, -2, 30, 12, SILVER_DARK, seed, shadow=False, lw=1.6)             # shank
    c.set_source_rgb(*INK); c.set_line_width(1.2)
    for i in range(5):
        c.move_to(2 + i * 5, -2); c.line_to(5 + i * 5, 10); c.stroke()             # threads
    hexp = [(-22, -10), (-12, -14), (-2, -10), (-2, 18), (-12, 22), (-22, 18)]
    cut(k, hexp, SILVER, shadow=False, lw=2)
    c.set_source_rgb(*SILVER_DARK); c.rectangle(-22, -10, 4, 28); c.fill()
    c.set_source_rgb(1, 1, 1); c.set_line_width(2.4)                              # bright edge
    c.move_to(-12, -10); c.line_to(-12, 18); c.stroke()
    c.restore()


def wrench(k, x, y, s=1.0, rot=0.0, seed=1320, oily=True):
    c = k.c
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    rect(k, -6, 0, 12, 70, SILVER, seed, shadow=False, lw=2)                       # handle
    c.set_source_rgb(1, 1, 1); c.set_line_width(2); c.move_to(-2, 6); c.line_to(-2, 64); c.stroke()
    head = [(-16, -24), (-6, -24), (-6, -10), (6, -10), (6, -24), (16, -24), (14, 4), (-14, 4)]
    cut(k, head, SILVER, shadow=False, lw=2)
    if oily:
        c.set_source_rgb(*OIL)
        c.move_to(-6, 30); c.curve_to(-8, 44, -2, 50, -4, 60); c.set_line_width(4); c.stroke()
        c.arc(-4, 62, 3, 0, 2 * math.pi); c.fill()
    c.restore()


def bolt_burger(k, x, y, s=1.0, seed=1330, wrench_out=True, oil=1.0):
    """Burger on a plate whose top surface is at y: golden buns full of oversized silver hex bolts."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    plate(k, 0, 0, 96, seed)
    if oil > 0:                                                    # a little oil, under the buns only
        c.set_source_rgba(*OIL, 0.9)
        c.save(); c.translate(6, -2); c.scale(26 * oil, 4); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
    cut(k, [(-34, -4), (34, -4), (30, -16), (-30, -16)], BUN, shadow=False, lw=2)        # bottom bun
    if wrench_out:
        wrench(k, 24, -34, 0.55, 0.9, seed + 1, oily=False)
    bolt(k, -14, -26, 0.8, -0.15, seed + 2)
    bolt(k, 14, -24, 0.8, 0.25, seed + 3)
    bolt(k, 0, -34, 0.75, 0.05, seed + 4)
    top = [(-38, -36), (-32, -54), (-14, -62), (14, -62), (32, -54), (38, -36)]
    cut(k, top, BUN, shadow=False, lw=2.2)                                               # top bun
    c.set_source_rgb(*BUN_DARK); c.set_line_width(3)
    c.arc(0, -36, 30, math.pi * 1.15, math.pi * 1.35); c.stroke()
    c.set_source_rgb(1.0, 0.95, 0.80)
    for sx, sy in ((-14, -52), (-2, -56), (10, -53), (20, -48), (-24, -46)):            # sesame
        c.save(); c.translate(sx, sy); c.scale(2.6, 1.4); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
    if oil > 0:                                                    # one drip off the bun edge
        c.set_source_rgb(*OIL); c.set_line_width(3.2)
        c.move_to(-30, -18); c.curve_to(-32, -12, -29, -8, -31, -4); c.stroke()
    c.restore()


# ------------------------------------------------------------------ bubbles (screen space)
def _text_box(c, s, size):
    lines = s.split("\n")
    c.select_font_face(kit.FONT); c.set_font_size(size)
    tw = max(c.text_extents(l).x_advance for l in lines)
    return lines, tw, size * 1.12


def thought(k, s, anchor, cx, cy, size=30):
    """Thought cloud centred at (cx, cy) with three shrinking dots leading down to anchor (her head)."""
    c = k.c
    lines, tw, lh = _text_box(c, s, size)
    rw, rh = tw / 2 + 34, lh * len(lines) / 2 + 26
    puffs = []
    n = 12
    for i in range(n):
        a = 2 * math.pi * i / n
        puffs.append((cx + math.cos(a) * rw * 0.92, cy + math.sin(a) * rh * 0.88, 0.32 * min(rw, rh) + 8))
    for px, py, r in puffs:                                        # outline pass
        c.arc(px, py, r + 1.6, 0, 2 * math.pi); c.set_source_rgb(*INK); c.fill()
    c.save(); c.translate(cx, cy); c.scale(rw + 1.6, rh + 1.6); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
    c.fill()
    c.set_source_rgb(1, 1, 1)
    for px, py, r in puffs:
        c.arc(px, py, r, 0, 2 * math.pi); c.fill()
    c.save(); c.translate(cx, cy); c.scale(rw, rh); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
    ax, ay = anchor                                                # three dots to the head
    for i, r in enumerate((10, 7, 4.5)):
        u = (i + 1) / 4
        dx, dy = cx + (ax - cx) * (0.55 + u * 0.4), (cy + rh) + (ay - cy - rh) * (0.25 + u * 0.7)
        c.arc(dx, dy, r + 1.8, 0, 2 * math.pi); c.set_source_rgb(*INK); c.fill()
        c.arc(dx, dy, r, 0, 2 * math.pi); c.set_source_rgb(1, 1, 1); c.fill()
    c.set_source_rgb(*INK)
    for i, l in enumerate(lines):
        e = c.text_extents(l)
        c.move_to(cx - e.x_advance / 2, cy - lh * len(lines) / 2 + lh * i + size * 0.86); c.show_text(l)


def whisper(k, s, anchor, cx, cy, size=30):
    """Whisper: normal-size text in a dotted bubble with a dotted tail to the speaker."""
    c = k.c
    lines, tw, lh = _text_box(c, s, size)
    bw, bh = tw + 44, lh * len(lines) + 30
    bx, by = cx - bw / 2, cy - bh / 2
    c.set_source_rgb(1, 1, 1)
    kit._poly(c, kit.rough_rect_pts(k, bx, by, bw, bh, 1401, j=1.0)); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(3); c.set_dash([4, 7]); c.set_line_cap(1)
    kit._poly(c, kit.rough_rect_pts(k, bx, by, bw, bh, 1401, j=1.0)); c.stroke()
    ax, ay = anchor
    ex = min(max(ax, bx + 20), bx + bw - 20)
    ey = by + bh if ay > by + bh else by
    c.move_to(ex, ey); c.line_to(ax, ay); c.stroke()
    c.set_dash([])
    for i, l in enumerate(lines):
        e = c.text_extents(l)
        c.move_to(cx - e.x_advance / 2, by + 15 + lh * i + size * 0.86); c.show_text(l)


def shout(k, s, anchor, cx, cy, size=44):
    """Shout: the biggest, boldest box in the film, spiky edge, tail to the speaker."""
    c = k.c
    c.select_font_face(kit.FONT); c.set_font_size(size)
    lines = s.split("\n")
    tw = max(c.text_extents(l).x_advance for l in lines)
    lh = size * 1.08
    rw, rh = tw / 2 + 40, lh * len(lines) / 2 + 30
    pts = []
    n = 22
    for i in range(n):
        a = 2 * math.pi * i / n
        r = 1.0 if i % 2 == 0 else 0.84
        pts.append((cx + math.cos(a) * rw * r * 1.08, cy + math.sin(a) * rh * r * 1.12))
    ax, ay = anchor
    cut(k, [(cx + (ax - cx) * 0.35 - 14, cy + (ay - cy) * 0.35), (ax, ay), (cx + (ax - cx) * 0.35 + 14, cy + (ay - cy) * 0.35 + 8)],
        (1.0, 0.95, 0.55), shadow=False, lw=3)
    cut(k, pts, (1.0, 0.95, 0.55), lw=3)
    c.set_source_rgb(*INK)
    for i, l in enumerate(lines):
        e = c.text_extents(l)
        c.move_to(cx - e.x_advance / 2, cy - lh * len(lines) / 2 + lh * i + size * 0.88); c.show_text(l)
