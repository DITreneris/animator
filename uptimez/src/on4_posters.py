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


def _sheet(k, col=PAPER, tilt=0.0):
    c = k.c
    c.rotate(tilt)
    c.rectangle(0, 0, 96, 136); c.set_source_rgb(*col); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(2.4); c.stroke()


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
    c.restore()


def fight(k, x, y, s=1.0):
    """Office Noir 3's bill, as it is (street_on3.poster2 draws at 1.3 and off its corner by (-14, -34))."""
    import street_on3 as s3
    c = k.c
    c.save(); c.translate(x, y); c.scale(s / 1.3, s / 1.3); c.scale(96 / 96.0, 136 / 136.0)
    s3.poster2(k, 14 / 1.0, 34 / 1.0, 1.0, seed=31)
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


def tally(k, x, y, s=1.0):
    """Chalk on the brick: seven strokes, a gate of five and two more (her seven lives). About 74 x 42 at s=1."""
    import random
    c = k.c; r = random.Random(77)
    c.save(); c.translate(x, y); c.scale(s, s); c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.set_source_rgb(0.80, 0.79, 0.76); c.set_line_width(3.6)
    for x0 in (2, 12, 22, 32, 54, 64):
        c.move_to(x0 + r.uniform(-1.5, 1.5), r.uniform(0, 3)); c.line_to(x0 + r.uniform(-2.5, 2.5), 40 + r.uniform(-3, 2)); c.stroke()
    c.move_to(-5, 31); c.line_to(40, 8); c.stroke()
    c.restore()


def crossing(k):
    """on4_motion.c_side: the far houses' wall (y 380-568, windows y 430-500). v2 (Tomas, 24 Nov: where is it too much):
    her bill alone, right of her, clear of Don's STOP/GO sign."""
    if not ON[0]:
        return
    pam_cat(k, 382, 392, 0.74)


def lane(k):
    """2.4, the brick wall over the bin (the bin's mouth y 566, x 200-420; the camera sees x 84-456). v2: her bill, the
    chalk tally, the fight bill; the TV bill out."""
    if not ON[0]:
        return
    pam_cat(k, 204, 354, 0.76, -0.03)
    tally(k, 290, 362, 0.9)
    fight(k, 372, 352, 0.76)


def club(k):
    """v2: nothing (the marquee says it; the bill was cut by the close cameras)."""
    return
