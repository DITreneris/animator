"""Office Noir 4: the town's bills and signs (24 Nov, Tomas: the houses look bare).

Opt-in: nothing is drawn unless ON[0] is True (on4_film sets it). Tomas's picks: the Pam-Cat act, Human vs Robot (Office
Noir 3's fight bill, street_on3.poster2, reused), the UptimeZ Inc. TV show, cabaret signs; her bill shows a silhouette
with ears only (nobody ever looks at her); three places (the crossing, the lane by the bin, the club's door); grey paper,
the only red the heart on her bill (exact NEON, so the grade keeps it).

Every bill is 96 x 136 at s=1, its top left at (x, y). A bill is whole in a camera or out of it (lesson 335)."""
import math
import cairo
import kit
import on4_street as st

ON = [False]
CAM = [(270, 480, 1.0)]                                      # the camera of the shot being drawn (on4_scenes.render sets it)


def whole(x, y, w, h, m=6):
    cx, cy, z = CAM[0]
    return cx - 270 / z + m <= x and x + w <= cx + 270 / z - m and cy - 480 / z + m <= y and y + h <= cy + 480 / z - m
NEON = st.NEON
INK = (0.06, 0.06, 0.07)
PAPER = (0.90, 0.89, 0.85)
PAPER_D = (0.70, 0.69, 0.66)


WALL_ST = (0.90, 0.89, 0.86)                                 # the crossing's lit wall
WALL_LN = (0.30, 0.28, 0.27)                                 # the lane's brick
WEAR = [None]                                                # v3: None = a flat sheet (v1-v2); ("fresh" | "old", wall colour)


def _sheet(k, col=PAPER, tilt=0.0):
    c = k.c
    c.translate(48, 68); c.rotate(tilt); c.translate(-48, -68)
    if WEAR[0]:
        col = (0.85, 0.85, 0.82) if WEAR[0][0] == "fresh" else (0.74, 0.74, 0.71) if col == PAPER else (0.60, 0.60, 0.58)
        c.rectangle(3, 4, 96, 136); c.set_source_rgba(0, 0, 0, 0.35); c.fill()         # the sheet's shadow on the wall
    c.rectangle(0, 0, 96, 136); c.set_source_rgb(*col); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(2.4); c.stroke()


def _wear(k, seed=1):
    """Over a finished bill (in its 96 x 136 space): a corner come away; an old one also torn at the foot, stained, the
    brick's courses showing through."""
    if not WEAR[0]:
        return
    import random
    kind, wall = WEAR[0]; c = k.c; r = random.Random(seed)
    c.new_path(); c.move_to(98, 138); c.line_to(80, 138); c.line_to(98, 120); c.close_path()         # the bottom right corner off the wall (no word there)
    c.set_source_rgb(*wall); c.fill()
    c.new_path(); c.move_to(81, 136); c.line_to(96, 121); c.line_to(83, 123); c.close_path()          # its underside, curled up
    c.set_source_rgb(0.62, 0.62, 0.60); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1.8); c.stroke()
    if kind != "old":
        return
    x0 = r.uniform(3, 6); pts = [(x0, 138)]                                                           # nicks torn out of the foot, at the left, clear of the words and the heart
    for i in range(1, 4):
        pts.append((x0 + i * 3.5, 136 - (r.uniform(5, 9) if i % 2 else r.uniform(1, 4))))
    pts.append((x0 + 14, 138))
    c.new_path(); c.move_to(*pts[0])
    for q in pts[1:]:
        c.line_to(*q)
    c.close_path(); c.set_source_rgb(*wall); c.fill()
    c.new_path(); c.move_to(*pts[0])
    for q in pts[1:]:
        c.line_to(*q)
    c.set_source_rgb(*INK); c.set_line_width(1.6); c.stroke()
    c.save(); c.rectangle(0, 0, 96, 136); c.clip()
    for _ in range(3):                                                                                # damp
        c.save(); c.translate(r.uniform(10, 86), r.uniform(20, 126)); c.scale(r.uniform(10, 20), r.uniform(8, 16))
        c.new_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.set_source_rgba(0, 0, 0, 0.10); c.fill()
    c.set_source_rgba(0, 0, 0, 0.13); c.set_line_width(1.2)                                           # the courses under the paper
    for y in range(18, 136, 40):
        c.move_to(0, y + r.uniform(-2, 2)); c.line_to(96, y + r.uniform(-2, 2)); c.stroke()
    c.restore()


def _heart(c, x, y, s):
    c.new_path(); c.move_to(x, y + s * 0.9)
    c.curve_to(x - s * 1.5, y - s * 0.2, x - s * 0.6, y - s * 1.3, x, y - s * 0.45)
    c.curve_to(x + s * 0.6, y - s * 1.3, x + s * 1.5, y - s * 0.2, x, y + s * 0.9)
    c.set_source_rgb(*NEON); c.fill()


def pam_cat(k, x, y, s=1.0, tilt=0.0):
    """TONIGHT / a cat's head in black, ears up, the mask's two slits / THE CAT / SEVEN LIVES and one red heart."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s); _sheet(k, PAPER, tilt)
    c.set_source_rgb(*INK); c.rectangle(4, 4, 88, 20); c.fill()
    kit.text(k, "TONIGHT", 48, 14.5, 13, PAPER, bold=True)
    c.set_source_rgb(*INK)
    c.new_path(); c.arc(48, 56, 20, 0, 2 * math.pi); c.fill()                       # the head
    for sg in (-1, 1):                                                              # the ears
        c.new_path(); c.move_to(48 + sg * 20, 53); c.line_to(48 + sg * 19, 27); c.line_to(48 + sg * 4, 40); c.close_path(); c.fill()
    c.set_source_rgb(*PAPER)
    for sg in (-1, 1):                                                              # the mask's slits
        c.new_path(); c.move_to(48 + sg * 3.5, 56); c.curve_to(48 + sg * 8, 49, 48 + sg * 14, 49, 48 + sg * 17, 52.5)
        c.curve_to(48 + sg * 13, 59, 48 + sg * 8, 60, 48 + sg * 3.5, 56); c.fill()
    kit.text(k, "THE CAT", 48, 90, 19, INK, bold=True)
    kit.text(k, "SEVEN LIVES", 48, 106, 10.5, INK, bold=True)
    _heart(c, 48, 122, 9)                                                           # the film's red, big enough for a phone
    _wear(k, 5)
    c.restore()


def fight(k, x, y, s=1.0, tilt=0.0):
    """Office Noir 3's bill, as it is (street_on3.poster2 draws at 1.3 and off its corner by (-14, -34))."""
    import street_on3 as s3
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    c.translate(48, 68); c.rotate(tilt); c.translate(-48, -68)
    if WEAR[0]:
        c.rectangle(3, 4, 96, 136); c.set_source_rgba(0, 0, 0, 0.35); c.fill()
    c.save(); c.scale(1 / 1.3, 1 / 1.3); s3.poster2(k, 14, 34, 1.0, seed=31); c.restore()
    if WEAR[0] and WEAR[0][0] == "old":
        c.rectangle(0, 0, 96, 136); c.set_source_rgba(0, 0, 0, 0.16); c.fill()                      # older paper
    _wear(k, 9)
    c.restore()


def tv_show(k, x, y, s=1.0, tilt=0.0):
    """ON TV / a set with its aerial, a robot's face on the screen / UPTIMEZ INC. / EVERY NIGHT."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s); _sheet(k, PAPER_D, tilt)
    kit.text(k, "ON TV", 48, 15, 14, INK, bold=True)
    c.set_source_rgb(*INK); c.set_line_width(2)
    c.move_to(48, 34); c.line_to(34, 22); c.stroke(); c.move_to(48, 34); c.line_to(62, 22); c.stroke()
    c.rectangle(16, 34, 64, 46); c.fill()
    c.set_source_rgb(*PAPER); c.rectangle(21, 39, 54, 36); c.fill()
    c.set_source_rgb(*INK); c.rectangle(34, 46, 28, 22); c.fill()                   # the robot on the screen
    c.set_source_rgb(*PAPER); c.rectangle(39, 52, 6, 5); c.fill(); c.rectangle(51, 52, 6, 5); c.fill(); c.rectangle(40, 61, 16, 3); c.fill()
    kit.text(k, "UPTIMEZ", 48, 96, 18, INK, bold=True)
    kit.text(k, "INC.", 48, 113, 15, INK, bold=True)
    c.set_source_rgb(*INK); c.rectangle(4, 122, 88, 11); c.fill()
    kit.text(k, "EVERY NIGHT", 48, 127.5, 8.5, PAPER, bold=True)
    c.restore()


def cabaret(k, x, y, s=1.0, right=True):
    """A hanging board, 150 x 44 at s=1, its top left at (x, y): CABARET and an arrow, a row of bulbs over and under."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    c.set_source_rgb(*INK); c.set_line_width(2.5)
    for xx in (22, 128):
        c.move_to(xx, 0); c.line_to(xx, -14); c.stroke()
    c.rectangle(0, 0, 150, 44); c.set_source_rgb(0.08, 0.08, 0.09); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.4); c.stroke()
    for i in range(13):
        for yy in (5, 39):
            c.new_path(); c.arc(9 + i * 11, yy, 2.2, 0, 2 * math.pi); c.set_source_rgb(0.95, 0.93, 0.86); c.fill()
    kit.text(k, "CABARET", 62 if right else 88, 22, 20, (0.95, 0.93, 0.86), bold=True)
    ax = 128 if right else 22; d = 1 if right else -1
    c.set_source_rgb(0.95, 0.93, 0.86)
    c.new_path(); c.move_to(ax + d * 14, 22); c.line_to(ax - d * 4, 12); c.line_to(ax - d * 4, 32); c.close_path(); c.fill()
    c.restore()


def tally(k, x, y, s=1.0, hand=False):
    """Chalk on the brick: seven strokes, a gate of five and two more (her seven lives). About 74 x 42 at s=1.
    hand=True (v3, the review): drawn by hand: each stroke of uneven weight, not straight, breaking where the chalk
    skipped over a joint."""
    import random
    c = k.c; r = random.Random(77)
    c.save(); c.translate(x, y); c.scale(s, s); c.set_line_cap(cairo.LINE_CAP_ROUND)
    if not hand:
        c.set_source_rgb(0.80, 0.79, 0.76); c.set_line_width(3.6)
        for x0 in (2, 12, 22, 32, 54, 64):
            c.move_to(x0 + r.uniform(-1.5, 1.5), r.uniform(0, 3)); c.line_to(x0 + r.uniform(-2.5, 2.5), 40 + r.uniform(-3, 2)); c.stroke()
        c.move_to(-5, 31); c.line_to(40, 8); c.stroke()
        c.restore(); return
    def stroke(xa, ya, xb, yb):
        n = 7; bow = r.uniform(-2.2, 2.2); gap = r.randrange(2, n - 1); w = r.uniform(3.0, 4.4)
        px = lambda u: (xa + (xb - xa) * u + bow * math.sin(math.pi * u), ya + (yb - ya) * u)
        for i in range(n):
            w = min(4.8, max(2.6, w + r.uniform(-0.7, 0.7)))
            u0, u1 = i / n, (i + 1) / n
            if i == gap:                                     # the chalk skipped: a short break
                u0 += 0.6 / n
            c.set_line_cap(cairo.LINE_CAP_ROUND if i in (0, n - 1) else cairo.LINE_CAP_BUTT)
            c.set_line_width(w); c.set_source_rgba(0.80, 0.79, 0.76, 0.95 if i != gap else 0.7)
            c.move_to(*px(u0)); c.line_to(*px(u1 + 0.01)); c.stroke()
    for x0 in (2, 13, 22, 33, 55, 66):
        stroke(x0 + r.uniform(-2, 2), r.uniform(-3, 4), x0 + r.uniform(-4, 4), 40 + r.uniform(-5, 4))
    stroke(-7, 33, 42, 6)
    c.restore()


def scrap(k, x, y, s=1.0):
    """What is left of an older bill: a torn piece of grey paper, no words, two runs of old paste. About 46 x 34."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s); c.rotate(0.12)
    pts = [(0, 3), (9, 0), (17, 5), (27, 1), (38, 4), (46, 2), (44, 14), (47, 24), (39, 33), (30, 28), (22, 34), (12, 29), (3, 31), (5, 19)]
    c.new_path(); c.move_to(*pts[0])
    for q in pts[1:]:
        c.line_to(*q)
    c.close_path(); c.set_source_rgb(0.56, 0.56, 0.54); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1.6); c.stroke()
    c.set_source_rgba(0, 0, 0, 0.22); c.set_line_width(2)
    c.move_to(8, 10); c.line_to(36, 9); c.stroke(); c.move_to(10, 20); c.line_to(30, 22); c.stroke()
    c.restore()


def crossing(k):
    """on4_motion.c_side: the far houses' wall (y 380-568, windows y 430-500). v2 (Tomas, 24 Nov: where is it too much):
    her bill alone, right of her, clear of Don's STOP/GO sign. v3 (the review, Tomas's picks): a fresh bill: turned a
    little, its shadow, one corner come away."""
    if not ON[0]:
        return
    WEAR[0] = ("fresh", WALL_ST)
    try:
        pam_cat(k, 382, 392, 0.74, 0.045)
    finally:
        WEAR[0] = None


def lane(k):
    """2.4, the brick wall over the bin (the bin's mouth y 566, x 200-420; the camera sees x 84-456). v2: her bill, the
    chalk tally, the fight bill; the TV bill out. v3: old bills (darker paper, torn, damp, the courses showing), the
    tally by hand on the brick (the window above now ends behind the platform), a scrap of an older bill."""
    if not ON[0]:
        return
    WEAR[0] = ("old", WALL_LN)
    try:
        pam_cat(k, 204, 356, 0.76, -0.05)
        fight(k, 358, 354, 0.76, 0.04)
    finally:
        WEAR[0] = None
    tally(k, 290, 364, 0.82, hand=True)
    scrap(k, 298, 420, 0.85)


def club(k):
    """v2: nothing (the marquee says it; the bill was cut by the close cameras)."""
    return


# ---- the sky (24 Nov, Tomas's picks): a young thin crescent, seven stars in the Plough's shape (her seven lives, like the
# chalk), still; over the first street (A) and the crossing (C from the road, C_side from the kerb). Opt-in with ON.
PLOUGH = [(0.0, 0.0), (0.02, 0.30), (0.33, 0.36), (0.38, 0.10), (0.60, 0.02), (0.80, -0.08), (1.0, 0.08)]
SKY = {"A": ((322, 66, 25), (88, 36, 170)),                  # the moon (x, y, r); the Plough (x, y, width)
       "C": ((118, 328, 17), (30, 214, 140)),
       "side": ((266, 322, 16), (122, 294, 112))}


def moon(k, x, y, r, turn=-0.5):
    c = k.c
    c.save(); c.translate(x, y); c.rotate(turn)
    c.new_path(); c.arc(0, 0, r, -math.pi / 2, math.pi / 2)                  # the lit limb, then back along the terminator
    c.save(); c.scale(0.62, 1.0); c.arc_negative(0, 0, r, math.pi / 2, -math.pi / 2); c.restore()
    c.close_path(); c.set_source_rgb(0.95, 0.94, 0.90); c.fill()
    c.restore()


def star(c, x, y, r):
    c.set_source_rgb(0.93, 0.92, 0.88)
    c.new_path(); c.arc(x, y, r, 0, 2 * math.pi); c.fill()
    c.set_line_width(r * 0.5)
    c.move_to(x - r * 2.1, y); c.line_to(x + r * 2.1, y); c.stroke(); c.move_to(x, y - r * 2.1); c.line_to(x, y + r * 2.1); c.stroke()


def sky(k, where):
    if not ON[0]:
        return
    (mx, my, mr), (px, py, pw) = SKY[where]
    for i, (u, v) in enumerate(PLOUGH):
        star(k.c, px + u * pw, py + v * pw, (3.0 if i in (0, 4, 6) else 2.4) * (0.75 + 0.25 * pw / 140.0))
    moon(k, mx, my, mr)
