"""Set for the Christmas special "Happy Compliance": the Day One office wall, decorated.
World units (like the cafeteria set): floor line FLOOR_Y; a 9:16 camera (cx, cy, z) maps the world into
540 x 960 as translate(270, 480) . scale(z) . translate(-cx, -cy).
- wall, floor and baseboard from Day One; the UptimeZ wall sign;
- the tree in the middle: three green tiers, gold star, gold tinsel, red and gold ornaments at fixed spots
  (ORNAMENTS, indices 0..7) so the robot can censor them one by one; a red pot, two small gifts;
- string lights along the top, a "MERRY CHRISTMAS TO ALL" bunting banner, and one wall gag:
  a "0 DAYS SINCE LAST INCIDENT" board (it was 0 before Don arrived, too);
- the door on the right, where Don and the robot come in.
Kept deliberately simple: one banner, lights, tinsel, one sign."""
import math
import kit
import pt42
import sofia_xmas as sx
import santa_robot_v2 as sr
from kit import INK, cut, rect, ellipse, text

FLOOR_Y = 660
FEET = 730                      # front-row feet
FEET_BACK = 712                 # back row (Pam)
TREE_X, TREE_BASE = 330, 732
TREE_S = 1.12                   # about Sofía's height
POS = {"sofia": 195, "pam": 478, "don_door": 700, "don": 560, "robot": 610, "door_x": 650}
GREEN = (0.16, 0.48, 0.30)
GREEN_DARK = (0.10, 0.36, 0.22)
GOLD = (0.95, 0.74, 0.18)
GOLD_DARK = (0.72, 0.52, 0.08)
POT = (0.75, 0.14, 0.16)
TRUNK = (0.45, 0.30, 0.18)
LIGHTS = [(0.95, 0.25, 0.25), (0.98, 0.80, 0.20), (0.30, 0.70, 0.95), (0.35, 0.80, 0.40)]
# ornaments: (dx, dy from the tree base, radius, colour index 0 red / 1 gold)
ORNAMENTS = [(-52, -96, 15, 0), (46, -112, 14, 1), (-16, -150, 14, 1), (34, -178, 13, 0),
             (-38, -206, 13, 0), (14, -232, 12, 1), (-8, -268, 11, 0), (58, -70, 14, 0)]

CAMS = {"wide": (420, 520, 0.88), "tree": (330, 580, 1.45), "sofia_pam": (330, 560, 1.4),
        "door": (650, 560, 1.4), "robot_don": (590, 560, 1.4), "pam": (470, 560, 1.8), "robot_cu": (610, 470, 2.6)}


def wall(k):
    c = k.c
    rect(k, -600, -400, 2200, FLOOR_Y + 400, kit.WALL, 100, shadow=False, outline=False)
    rect(k, -600, FLOOR_Y, 2200, 900, kit.FLOOR, 101, shadow=False)
    rect(k, -600, FLOOR_Y - 10, 2200, 16, (0.62, 0.5, 0.36), 102, shadow=False, lw=2)
    pt42.wall_sign(k, 410, 300, 30)


def lights(k, x0, x1, y, sag=26, n=16, boil=0):
    c = k.c
    c.set_source_rgb(*INK); c.set_line_width(2)
    pts = []
    seg = (x1 - x0) / 3
    for j in range(3):
        a, b = x0 + j * seg, x0 + (j + 1) * seg
        c.move_to(a, y); c.curve_to(a + seg * 0.3, y + sag, b - seg * 0.3, y + sag, b, y); c.stroke()
        for i in range(1, 6):
            t = i / 6
            px_ = (1 - t) ** 3 * a + 3 * (1 - t) ** 2 * t * (a + seg * 0.3) + 3 * (1 - t) * t * t * (b - seg * 0.3) + t ** 3 * b
            py_ = (1 - t) ** 3 * y + 3 * (1 - t) ** 2 * t * (y + sag) + 3 * (1 - t) * t * t * (y + sag) + t ** 3 * y
            pts.append((px_, py_))
    for i, (px_, py_) in enumerate(pts):
        col = LIGHTS[(i + boil) % 4]
        ellipse(k, px_, py_ + 8, 5, 8, col, 900 + i, shadow=False, lw=1.6)


def banner(k, x0, x1, y, words="MERRY CHRISTMAS TO ALL"):
    """Bunting: one paper flag per letter, alternating red and green, a word gap between words."""
    c = k.c
    chars = list(words)
    n = len(chars)
    step = (x1 - x0) / n
    c.set_source_rgb(*INK); c.set_line_width(2)
    c.move_to(x0 - 10, y); c.curve_to(x0 + (x1 - x0) * 0.3, y + 22, x0 + (x1 - x0) * 0.7, y + 22, x1 + 10, y); c.stroke()
    for i, ch in enumerate(chars):
        if ch == " ":
            continue
        fx = x0 + step * (i + 0.5)
        t = (fx - x0) / (x1 - x0)
        fy = y + 22 * 3 * t * (1 - t) * 0.75 * 1.33
        col = (0.80, 0.12, 0.15) if i % 2 == 0 else (0.15, 0.50, 0.30)
        cut(k, [(fx - step * 0.45, fy), (fx + step * 0.45, fy), (fx, fy + step * 1.15)], col, shadow=False, lw=1.6)
        text(k, ch, fx, fy + step * 0.52, step * 0.6, (1, 1, 1), bold=True)


def incident_board(k, x, y, w=118, h=86):
    c = k.c
    rect(k, x, y, w, h, (1, 1, 1), 910, lw=2.2)
    c.set_source_rgb(0.15, 0.50, 0.30); c.rectangle(x + 2, y + 2, w - 4, 16); c.fill()
    text(k, "SAFETY FIRST", x + w / 2, y + 14, 10, (1, 1, 1), bold=True)
    text(k, "0", x + w / 2, y + 56, 38, (0.80, 0.12, 0.15), bold=True)
    text(k, "DAYS SINCE LAST INCIDENT", x + w / 2, y + 77, 8.4, INK, bold=True)


def tree(k, x=TREE_X, base=TREE_BASE, s=TREE_S, censored=(), seed=950, boil=0):
    """Returns the canvas (world) positions of the ornaments, index-aligned with ORNAMENTS."""
    c = k.c
    c.save(); c.translate(x, base); c.scale(s, s)
    rect(k, -12, -44, 24, 30, TRUNK, seed, shadow=False, lw=2)
    cut(k, [(-34, -30), (34, -30), (26, 0), (-26, 0)], POT, lw=2.2)                     # pot
    rect(k, -37, -34, 74, 10, (0.85, 0.20, 0.22), seed + 1, shadow=False, lw=1.8)
    for i, (w_, top, bot) in enumerate(((92, -168, -40), (76, -238, -130), (58, -300, -204))):
        tier = [(0, top), (w_ * 0.25, top + (bot - top) * 0.35), (w_ * 0.55, top + (bot - top) * 0.62),
                (w_, bot), (w_ * 0.5, bot - 8), (0, bot + 4), (-w_ * 0.5, bot - 8), (-w_, bot),
                (-w_ * 0.55, top + (bot - top) * 0.62), (-w_ * 0.25, top + (bot - top) * 0.35)]
        cut(k, tier, GREEN, lw=2.4)
        c.set_source_rgb(*GREEN_DARK); c.set_line_width(2.4)
        c.move_to(-w_ * 0.4, bot - 14); c.curve_to(-w_ * 0.2, bot - 24, w_ * 0.2, bot - 24, w_ * 0.4, bot - 14); c.stroke()
    c.set_line_width(4); c.set_line_cap(1)                                               # gold tinsel, draped
    for (ax, ay, bx, by) in ((-80, -78, 84, -110), (-62, -170, 64, -196), (-44, -246, 44, -262)):
        c.set_source_rgb(*GOLD_DARK); c.set_line_width(5.4)
        c.move_to(ax, ay); c.curve_to(ax * 0.3, ay + 22, bx * 0.3, by + 22, bx, by); c.stroke()
        c.set_source_rgb(*GOLD); c.set_line_width(3)
        c.move_to(ax, ay); c.curve_to(ax * 0.3, ay + 22, bx * 0.3, by + 22, bx, by); c.stroke()
    # star
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        r = 22 if i % 2 == 0 else 9
        pts.append((math.cos(a) * r, -306 + math.sin(a) * r))
    cut(k, pts, GOLD, lw=2.2)
    out = []
    for i, (dx, dy, r, ci) in enumerate(ORNAMENTS):
        sx.ornament(k, dx, dy, r, seed + 20 + i, col=sx.ORN_RED if ci == 0 else GOLD)
        if i in censored:
            sr.censor_bar(k, dx, dy, r * 3.0, r * 0.95, rot=(-0.10 if i % 2 else 0.08), seed=seed + 40 + i,
                          label=r * 3.0 >= 34)
        out.append((x + dx * s, base + dy * s))
    c.restore()
    for gx, gw, gh, col in ((-74, 34, 26, (0.20, 0.45, 0.78)), (52, 30, 22, (0.85, 0.20, 0.22))):   # gifts
        rect(k, x + gx * s, base - gh * s, gw * s, gh * s, col, seed + 60 + gx, lw=2)
        c.set_source_rgb(*GOLD); c.set_line_width(4 * s)
        c.move_to(x + (gx + gw / 2) * s, base - gh * s); c.line_to(x + (gx + gw / 2) * s, base); c.stroke()
    return out


def door(k, x=POS["door_x"], open_amt=0.0):
    kit.door(k, x, FLOOR_Y - 250, 110, 250, 960, open_amt=open_amt, sign="PARTY")


def set_dressing(k, boil=0):
    wall(k)
    lights(k, -60, 760, 110, boil=boil)
    banner(k, 30, 560, 160)
    incident_board(k, 20, 300)


def to_screen(cam, x, y):
    cx, cy, z = cam
    return 270 + (x - cx) * z, 480 + (y - cy) * z


def with_cam(c, cam):
    cx, cy, z = cam
    c.translate(270, 480); c.scale(z, z); c.translate(-cx, -cy)
