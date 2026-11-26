"""The hand class sheet. One PNG, three columns, one scale.

It does not paint a film frame, and it does not set kit.HAND or hands_ps.GLOVE.
Male width is the rig's 17. Female width is 15, the long sleeve. The sheet draws
both at 4x so the shapes can be judged. The nail is not on this sheet.

  python3 bp_hand_sheet.py
"""
import math
import os

import cairo

import hands_ps
import kit
import of_cast as oc

SHEET = 4.0
MALE_W = 17.0 * SHEET
FEMALE_W = 15.0 * SHEET
MALE_SKIN = kit.PEOPLE["DON"]["skin"]
FEMALE_SKIN = kit.PEOPLE["PAM"]["skin"]
METAL = (0.55, 0.58, 0.62)
EDGE = (0.55, 0.56, 0.58)
WALL = (0.93, 0.91, 0.86)
INK = kit.INK

LABEL_W = 210
COL_W = 360
ROW_H = 300
HEADER = 110
MARGIN = 16

HUMAN = (
    ("quiet", "ramybė"),
    ("point", "rodo"),
    ("point_t", "žemyn"),
    ("grab", "laiko"),
    ("clutch", "briauna"),
    ("pinch", "suspaudžia"),
    ("fist", "kumštis"),
    ("palm", "delnas"),
    ("thumb", "nykštys"),
    ("phone_grip", "telefonas"),
    ("handle_grip", "rankena"),
)
ROBOT_ROWS = (
    ("rest", "ramybė"),
    ("grip", "griebtuvas"),
)

OUT = os.path.join(
    os.path.dirname(__file__),
    "..",
    "the-blueprint",
    "rough_work",
    "pic_hands",
    "bp_hand_classes.png",
)


def _label(c, text, x, y, size, bold=False):
    c.save()
    c.select_font_face("DejaVu Sans", 0, 1 if bold else 0)
    c.set_font_size(size)
    c.set_source_rgb(*INK)
    ext = c.text_extents(text)
    c.move_to(x - ext.x_advance / 2.0, y)
    c.show_text(text)
    c.restore()


def _edge(c, x, y, w):
    """The bar sticks out past the fingers, so the clutch reads as a grip."""
    c.save()
    c.set_source_rgb(*EDGE)
    c.rectangle(x - 0.70 * w, y, 1.50 * w, 0.58 * w)
    c.fill()
    c.set_source_rgb(*INK)
    c.set_line_width(2.0)
    c.rectangle(x - 0.70 * w, y, 1.50 * w, 0.58 * w)
    c.stroke()
    c.restore()


def _handle(c, x, y, w):
    c.save()
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.set_source_rgb(*INK)
    c.set_line_width(0.28 * w + 4)
    c.move_to(x, y - 0.55 * w)
    c.line_to(x, y + 0.55 * w)
    c.stroke()
    c.set_source_rgb(*EDGE)
    c.set_line_width(0.28 * w)
    c.move_to(x, y - 0.55 * w)
    c.line_to(x, y + 0.55 * w)
    c.stroke()
    c.restore()


def _human(k, job, x, y, w, skin):
    d = (1.0, 0.0)
    if job == "clutch":
        _edge(k.c, x, y, w)
        oc.clutch(k, x, y, w, skin)
        return
    if job == "phone_grip":
        oc.phone_grip(k, x, y, w / 26.0, screen=None, skin=skin, body_x=x + 40.0)
        return
    if job == "handle_grip":
        _handle(k.c, x, y, w)
        oc.handle_grip(k, x, y, w, -math.pi / 2, skin)
        return
    hands_ps.draw(k, job, x, y, w, skin, d, 1)


def _arm(c, x, y, reach):
    c.save()
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    for col, lw in ((INK, 28), (METAL, 22)):
        c.set_source_rgb(*col)
        c.set_line_width(lw)
        c.move_to(x - reach, y)
        c.line_to(x - reach * 0.42, y)
        c.line_to(x, y)
        c.stroke()
    c.set_source_rgb(*INK)
    c.arc(x - reach * 0.42, y, 8, 0, 2 * math.pi)
    c.fill()
    c.restore()


def _robot_rest(c, x, y):
    _arm(c, x, y, 120)
    c.save()
    c.set_source_rgb(*METAL)
    c.arc(x + 16, y, 18, 0, 2 * math.pi)
    c.fill_preserve()
    c.set_source_rgb(*INK)
    c.set_line_width(2.4)
    c.stroke()
    c.restore()


def _robot_grip(c, x, y):
    _arm(c, x, y, 120)
    c.save()
    c.rectangle(x + 14, y - 22, 36, 44)
    c.set_source_rgb(0.25, 0.27, 0.30)
    c.fill_preserve()
    c.set_source_rgb(*INK)
    c.set_line_width(2.2)
    c.stroke()
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    for y0, y1 in ((-20, -28), (20, 28)):
        c.set_source_rgb(*INK)
        c.set_line_width(12)
        c.move_to(x + 4, y + y0)
        c.line_to(x + 40, y + y1)
        c.stroke()
        c.set_source_rgb(*METAL)
        c.set_line_width(7)
        c.move_to(x + 4, y + y0)
        c.line_to(x + 40, y + y1)
        c.stroke()
    c.restore()


ANCHOR = {
    "phone_grip": (0.48, 0.78),
    "clutch": (0.38, 0.34),
    "thumb": (0.50, 0.58),
    "handle_grip": (0.50, 0.50),
}


def _cell(c, col, row, draw, job=""):
    x0 = MARGIN + LABEL_W + col * COL_W
    y0 = HEADER + row * ROW_H
    c.save()
    c.rectangle(x0 + 6, y0 + 6, COL_W - 12, ROW_H - 12)
    c.set_source_rgb(0.97, 0.96, 0.93)
    c.fill()
    c.restore()
    if draw is not None:
        ax, ay = ANCHOR.get(job, (0.42, 0.46))
        c.save()
        c.rectangle(x0 + 4, y0 + 4, COL_W - 8, ROW_H - 36)
        c.clip()
        draw(x0 + COL_W * ax, y0 + ROW_H * ay)
        c.restore()
    return x0, y0


def write(path=OUT):
    if hands_ps.GLOVE[0] is not None:
        raise RuntimeError("glove is on; the class sheet draws the bare hand")
    rows = list(HUMAN) + list(ROBOT_ROWS)
    width = MARGIN * 2 + LABEL_W + 3 * COL_W
    height = HEADER + len(rows) * ROW_H + MARGIN
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, int(width * 2), int(height * 2))
    surf.set_device_scale(2, 2)
    c = cairo.Context(surf)
    k = kit.Ctx(c, 0)
    c.set_source_rgb(*WALL)
    c.paint()
    _label(c, "Rankų klasės", MARGIN + 120, 34, 22, True)
    c.save()
    c.select_font_face("DejaVu Sans", 0, 0)
    c.set_font_size(14)
    c.set_source_rgb(*INK)
    c.move_to(MARGIN, 58)
    c.show_text("vyras 17, moteris 15, tas pats mastelis, nago nėra")
    c.restore()
    for i, name in enumerate(("Vyras", "Moteris", "Robotas")):
        _label(c, name, MARGIN + LABEL_W + i * COL_W + COL_W / 2, 96, 18, True)

    for r, (job, word) in enumerate(rows):
        _label(c, job, MARGIN + LABEL_W / 2, HEADER + r * ROW_H + ROW_H * 0.46, 16, True)
        _label(c, word, MARGIN + LABEL_W / 2, HEADER + r * ROW_H + ROW_H * 0.46 + 22, 13)
        robot_only = job in ("rest", "grip")
        for col, (w, skin) in enumerate(((MALE_W, MALE_SKIN), (FEMALE_W, FEMALE_SKIN))):
            if robot_only:
                x0, y0 = _cell(c, col, r, None)
                _label(c, "nėra", x0 + COL_W / 2, y0 + ROW_H * 0.5, 16)
            else:
                def draw(x, y, job=job, w=w, skin=skin):
                    _human(k, job, x, y, w, skin)
                _cell(c, col, r, draw, job)
        if robot_only:
            def draw(x, y, job=job):
                (_robot_rest if job == "rest" else _robot_grip)(c, x, y)
            _cell(c, 2, r, draw, job)
        else:
            x0, y0 = _cell(c, 2, r, None)
            _label(c, "nėra", x0 + COL_W / 2, y0 + ROW_H * 0.5, 16)
        x0, y0 = MARGIN + LABEL_W, HEADER + r * ROW_H
        for col in range(3):
            filled = (col < 2 and not robot_only) or (col == 2 and robot_only)
            _label(c, job if filled else "nėra", x0 + col * COL_W + COL_W / 2, y0 + ROW_H - 16, 12)

    os.makedirs(os.path.dirname(path), exist_ok=True)
    surf.write_to_png(path)
    return path


LOCKED = {
    "bp_still_s0.png": "25111ff33a2338b32e7bdea584204c28",
    "bp_still_shred.png": "da34775d2ac9821b42f149abb8261149",
    "bp_still_counter.png": "0a25fcc6b5831f360f24eb79c312fb5f",
    "bp_still_night.png": "31e044d813fe94ead453458d7b71d5fe",
}


def _md5(path):
    import hashlib
    h = hashlib.md5()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


if __name__ == "__main__":
    print(write())
    stills = os.path.join(os.path.dirname(__file__), "..", "the-blueprint", "stills")
    for name, want in LOCKED.items():
        got = _md5(os.path.join(stills, name))
        print("%s %s" % (name, "ok" if got == want else "CHANGED " + got))
