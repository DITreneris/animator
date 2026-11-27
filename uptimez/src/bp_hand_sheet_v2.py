"""Hand class sheet, second pass. One PNG beside the first sheet.

pinch, fist, and grab are drawn here. Calling hands_ps for them repeats the
shapes that read as claws, loose circles, and equal hooks. phone_grip and
point_t stay on the current functions: the phone shows its face, and point_t
points down. Male width is 17, female is 15 of the same shapes, no nail.

This file does not set kit.HAND or hands_ps.GLOVE, and it does not paint a
film frame.

  python3 bp_hand_sheet_v2.py
"""
import math
import os

import cairo

import bp_hand_sheet as v1
import hands_ps
import kit
import of_cast as oc

SHEET = v1.SHEET
MALE_W = v1.MALE_W
FEMALE_W = v1.FEMALE_W
MALE_SKIN = v1.MALE_SKIN
FEMALE_SKIN = v1.FEMALE_SKIN
WALL = v1.WALL
INK = v1.INK

LABEL_W = v1.LABEL_W
COL_W = v1.COL_W
HEADER = v1.HEADER
MARGIN = v1.MARGIN

# job, English word, two hands in the cell (left and right)
ROWS = (
    ("quiet", "at rest", False),
    ("point", "level", False),
    ("point_t", "down", True),
    ("grab", "holding", True),
    ("clutch", "edge", False),
    ("pinch", "pinch", True),
    ("fist", "fist", True),
    ("palm", "open", False),
    ("thumb", "thumbs-up", False),
    ("phone_grip", "phone", True),
    ("handle_grip", "handle", False),
    ("rest", "at rest", False),
    ("grip", "gripper", False),
)
MIRROR = ("point_t", "grab", "pinch", "fist", "phone_grip")
ROBOT = ("rest", "grip")

SINGLE_ANCHOR = {
    "clutch": (0.38, 0.34),
    "thumb": (0.50, 0.58),
    "handle_grip": (0.50, 0.50),
}
# One anchor for both robot rows, so the elbow mark lands on the same x.
ROBOT_ANCHOR = (0.62, 0.50)

OUT = os.path.join(
    os.path.dirname(__file__),
    "..",
    "the-blueprint",
    "rough_work",
    "pic_hands",
    "bp_hand_classes_v2.png",
)
NAIL = (0.86, 0.05, 0.12)  # sofia_v4.RED, the nail this sheet must not draw


def _row_h(job):
    if job == "phone_grip":
        return 460
    if job in MIRROR:
        return 320
    return 300


def _label(c, text, x, y, size, bold=False):
    c.save()
    c.select_font_face("DejaVu Sans", 0, 1 if bold else 0)
    c.set_font_size(size)
    c.set_source_rgb(*INK)
    ext = c.text_extents(text)
    c.move_to(x - ext.x_advance / 2.0, y)
    c.show_text(text)
    c.restore()


def _side(arm, ang=0.0):
    """Thumb side, the same rule as hands_ps.draw."""
    return -1 if (arm < 0) == (math.cos(ang) >= 0) else 1


def _pinch(c, x, y, w, skin, arm):
    """Thumb and index meet at one point. The other three fingers are one mass."""
    s_ = _side(arm)
    t = 0.26 * w
    tip = (1.02 * w, s_ * 0.02 * w)
    c.save()
    c.translate(x, y)
    hands_ps._wrist(c, w, skin)
    hands_ps._blob(c, 0.24 * w, 0, 0.40 * w, 0.36 * w, skin)
    hands_ps._blob(c, 0.46 * w, -s_ * 0.14 * w, 0.20 * w, 0.16 * w, skin)
    hands_ps._crease(c, [(0.34 * w, -s_ * 0.10 * w), (0.58 * w, -s_ * 0.10 * w)])
    hands_ps._crease(c, [(0.36 * w, -s_ * 0.20 * w), (0.56 * w, -s_ * 0.18 * w)])
    hands_ps._cap(c, [(0.42 * w, -s_ * 0.16 * w), (0.78 * w, -s_ * 0.10 * w), tip], t, skin)
    hands_ps._cap(c, [(0.16 * w, s_ * 0.34 * w), (0.62 * w, s_ * 0.26 * w), tip], t * 1.05, skin)
    c.restore()


def _round_block(c, x0, y0, x1, y1, r, skin):
    c.new_path()
    c.move_to(x0 + r, y0)
    c.line_to(x1 - r, y0)
    c.arc(x1 - r, y0 + r, r, -math.pi / 2, 0)
    c.line_to(x1, y1 - r)
    c.arc(x1 - r, y1 - r, r, 0, math.pi / 2)
    c.line_to(x0 + r, y1)
    c.arc(x0 + r, y1 - r, r, math.pi / 2, math.pi)
    c.line_to(x0, y0 + r)
    c.arc(x0 + r, y0 + r, r, math.pi, 1.5 * math.pi)
    c.close_path()
    c.set_source_rgb(*skin)
    c.fill_preserve()
    c.set_source_rgb(*INK)
    c.set_line_width(hands_ps.LW)
    c.stroke()


def _fist(c, x, y, w, skin, arm):
    """One closed block. The thumb lies across the front. Not a thumbs-up."""
    s_ = _side(arm)
    c.save()
    c.translate(x, y)
    hands_ps._wrist(c, w, skin)
    x1 = 0.78 * w
    _round_block(c, 0.02 * w, -0.36 * w, x1, 0.36 * w, 0.20 * w, skin)
    hands_ps._crease(c, [(0.22 * w, -0.12 * w), (x1 - 0.06 * w, -0.12 * w)])
    hands_ps._crease(c, [(0.22 * w, 0.12 * w), (x1 - 0.06 * w, 0.12 * w)])
    hands_ps._cap(c, [(0.08 * w, s_ * 0.22 * w), (0.55 * w, s_ * 0.08 * w)], 0.28 * w, skin)
    c.set_source_rgb(*skin)
    root_y = 0.04 * w if s_ > 0 else -0.22 * w
    c.rectangle(0.04 * w, root_y, 0.26 * w, 0.18 * w)
    c.fill()
    c.restore()


def _grab(c, x, y, w, skin, arm):
    """One C. Index longest, little finger shortest. The thumb stays clear."""
    s_ = _side(arm)
    t = 0.22 * w
    c.save()
    c.translate(x, y)
    hands_ps._wrist(c, w, skin)
    hands_ps._blob(c, 0.22 * w, 0, 0.40 * w, 0.38 * w, skin)
    for reach, fy in ((0.66, 0.46), (0.80, 0.36), (0.92, 0.24), (1.02, 0.10)):
        y_root = -s_ * fy * w
        hands_ps._cap(
            c,
            [(0.36 * w, y_root), (reach * w, y_root * 0.35), (reach * 0.78 * w, s_ * 0.02 * w)],
            t,
            skin,
        )
    hands_ps._cap(
        c,
        [(0.10 * w, s_ * 0.32 * w), (0.48 * w, s_ * 0.50 * w), (0.70 * w, s_ * 0.28 * w)],
        t * 1.15,
        skin,
    )
    c.restore()


def _screen(c):
    """Three bars on the phone face. No words."""
    c.set_source_rgb(0.45, 0.50, 0.56)
    c.set_line_width(1.4)
    c.set_line_cap(1)
    for yy in (-16, 0, 16):
        c.move_to(-12, yy)
        c.line_to(12, yy)
        c.stroke()
    c.set_line_cap(0)


def _phone(k, x, y, w, skin, arm):
    body = x + 40.0 if arm < 0 else x - 40.0
    oc.phone_grip(k, x, y, w / 26.0, screen=_screen, skin=skin, body_x=body)


def _point_down(k, x, y, w, skin, arm):
    hands_ps.draw(k, "point_t", x, y, w, skin, (0.0, 1.0), arm)


def _single(k, job, x, y, w, skin):
    if job == "clutch":
        v1._edge(k.c, x, y, w)
        oc.clutch(k, x, y, w, skin)
        return
    if job == "handle_grip":
        v1._handle(k.c, x, y, w)
        oc.handle_grip(k, x, y, w, -math.pi / 2, skin)
        return
    hands_ps.draw(k, job, x, y, w, skin, (1.0, 0.0), 1)


def _place_pair(k, c, job, x0, y0, h, w, skin):
    if job == "phone_grip":
        fx, fy = (0.27, 0.73), 0.74
    elif job == "point_t":
        fx, fy = (0.30, 0.74), 0.34
    else:
        fx, fy = (0.30, 0.74), 0.56
    y = y0 + h * fy
    spots = ((fx[0], -1, "left"), (fx[1], 1, "right"))
    for frac, arm, word in spots:
        x = x0 + COL_W * frac
        _label(c, word, x, y0 + 22, 12)
        if job == "pinch":
            _pinch(c, x, y, w, skin, arm)
        elif job == "fist":
            _fist(c, x, y, w, skin, arm)
        elif job == "grab":
            _grab(c, x, y, w, skin, arm)
        elif job == "phone_grip":
            _phone(k, x, y, w, skin, arm)
        else:
            _point_down(k, x, y, w, skin, arm)


def _cell_back(c, x0, y0, h):
    c.save()
    c.rectangle(x0 + 6, y0 + 6, COL_W - 12, h - 12)
    c.set_source_rgb(0.97, 0.96, 0.93)
    c.fill()
    c.restore()


def _clip(c, x0, y0, h):
    c.rectangle(x0 + 4, y0 + 4, COL_W - 8, h - 28)
    c.clip()


def _nail_red(surf):
    """Pixels near Sofia's nail red. Skin and ink are not in this range."""
    data = surf.get_data()
    stride = surf.get_stride()
    width = surf.get_width()
    height = surf.get_height()
    count = 0
    for y in range(height):
        row = data[y * stride:y * stride + width * 4]
        for i in range(0, width * 4, 4):
            b, g, r = row[i], row[i + 1], row[i + 2]
            if r > 180 and g < 60 and b < 80:
                count += 1
    return count


def _md5(path):
    import hashlib
    h = hashlib.md5()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def write(path=OUT):
    if hands_ps.GLOVE[0] is not None:
        raise RuntimeError("glove is on; the class sheet draws the bare hand")
    if os.path.basename(path) == "bp_hand_classes.png":
        raise RuntimeError("v2 must not overwrite the first class sheet")
    heights = [_row_h(job) for job, _word, _mirror in ROWS]
    width = MARGIN * 2 + LABEL_W + 3 * COL_W
    height = HEADER + sum(heights) + MARGIN
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, int(width * 2), int(height * 2))
    surf.set_device_scale(2, 2)
    c = cairo.Context(surf)
    k = kit.Ctx(c, 0)
    c.set_source_rgb(*WALL)
    c.paint()
    _label(c, "Hand classes", MARGIN + 140, 34, 22, True)
    c.save()
    c.select_font_face("DejaVu Sans", 0, 0)
    c.set_font_size(14)
    c.set_source_rgb(*INK)
    c.move_to(MARGIN, 58)
    c.show_text("male 17, female 15, same shapes, no nail")
    c.restore()
    for i, name in enumerate(("Male", "Female", "Robot")):
        _label(c, name, MARGIN + LABEL_W + i * COL_W + COL_W / 2, 96, 18, True)

    y = HEADER
    for (job, word, mirror), h in zip(ROWS, heights):
        _label(c, job, MARGIN + LABEL_W / 2, y + h * 0.46, 16, True)
        _label(c, word, MARGIN + LABEL_W / 2, y + h * 0.46 + 22, 13)
        robot = job in ROBOT
        for col, (hw, skin) in enumerate(((MALE_W, MALE_SKIN), (FEMALE_W, FEMALE_SKIN))):
            x0 = MARGIN + LABEL_W + col * COL_W
            _cell_back(c, x0, y, h)
            if robot:
                _label(c, "none", x0 + COL_W / 2, y + h * 0.5, 16)
            else:
                c.save()
                _clip(c, x0, y, h)
                if mirror:
                    _place_pair(k, c, job, x0, y, h, hw, skin)
                else:
                    ax, ay = SINGLE_ANCHOR.get(job, (0.42, 0.50))
                    _single(k, job, x0 + COL_W * ax, y + h * ay, hw, skin)
                c.restore()
            _label(c, job if not robot else "none", x0 + COL_W / 2, y + h - 16, 12)
        x0 = MARGIN + LABEL_W + 2 * COL_W
        _cell_back(c, x0, y, h)
        if robot:
            c.save()
            _clip(c, x0, y, h)
            ax, ay = ROBOT_ANCHOR
            (v1._robot_rest if job == "rest" else v1._robot_grip)(c, x0 + COL_W * ax, y + h * ay)
            c.restore()
            _label(c, job, x0 + COL_W / 2, y + h - 16, 12)
        else:
            _label(c, "none", x0 + COL_W / 2, y + h * 0.5, 16)
            _label(c, "none", x0 + COL_W / 2, y + h - 16, 12)
        y += h

    red = _nail_red(surf)
    if red:
        raise RuntimeError("nail red pixels: %d (near %s)" % (red, NAIL))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    surf.write_to_png(path)
    return path


if __name__ == "__main__":
    print(write())
    print("red 0")
    stills = os.path.join(os.path.dirname(__file__), "..", "the-blueprint", "stills")
    for name, want in v1.LOCKED.items():
        got = _md5(os.path.join(stills, name))
        print("%s %s" % (name, "ok" if got == want else "CHANGED " + got))
