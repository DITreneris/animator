"""Hand class sheet v4: one table picks which drawing each row uses.

ACCEPTED is the rollback. grab and pinch are back on v2, the phone stays on
v3. A row changes only when Tomas picks a new drawing on bp_hand_compare.py;
then its entry here changes and the old drawing stays in DRAWERS.

Every row of the v4 PNG must match, pixel for pixel, the same row of the
sheet its version came from. Otherwise the file is not written.

  python3 bp_hand_sheet_v4.py
"""
import math
import os

import cairo
from PIL import Image, ImageChops

import bp_hand_sheet_v2 as v2
import bp_hand_sheet_v3 as v3
import hands_ps
import kit
import of_cast as oc

PICS = os.path.join(os.path.dirname(__file__), "..", "the-blueprint", "rough_work", "pic_hands")
OUT = os.path.join(PICS, "bp_hand_classes_v4.png")
SHEETS = {
    "v1": os.path.join(PICS, "bp_hand_classes.png"),
    "v2": os.path.join(PICS, "bp_hand_classes_v2.png"),
    "v3": os.path.join(PICS, "bp_hand_classes_v3.png"),
}


def _phone_a(k, x, y, w, skin, arm):
    """Phone, attempt a. A forearm from below, a palm narrower than the phone,
    fingertips wrapping the far edge, a straight thumb low on the near edge."""
    s = w / 26.0
    body = x + 40.0 if arm < 0 else x - 40.0
    thumb = oc.inner_thumb(x, body, False)
    far = -thumb
    c = k.c
    c.new_path()
    c.save()
    c.translate(x, y + 0.50 * w)
    c.rotate(-math.pi / 2)
    hands_ps._cap(c, [(-1.00 * w, 0), (0, 0)], 0.60 * w, skin)
    c.restore()
    hands_ps._blob(c, x, y + 0.44 * w, 0.62 * w, 0.42 * w, skin)
    oc.phone(k, x, y - 22.0 * s, s, v2._screen)
    t = 0.27 * w
    edge = 22.0 * s
    for fy in (-30.0, -17.0, -4.0):
        hands_ps._cap(
            c,
            [(x + far * (edge + 3.0 * s), y + fy * s), (x + far * (edge - 7.0 * s), y + fy * s)],
            t,
            skin,
        )
    hands_ps._cap(
        c,
        [(x + thumb * 0.40 * w, y + 0.62 * w), (x + thumb * (edge - 9.0 * s), y + 6.0 * s)],
        0.30 * w,
        skin,
    )


def _phone_b(k, x, y, w, skin, arm):
    """Phone, attempt b, the last one. Forearm, palm, the side of the hand and the
    thumb are one silhouette with one outline. Three fingers of unequal length
    wrap the far edge, tips bent toward the palm; the fourth is behind the phone."""
    s = w / 26.0
    body = x + 40.0 if arm < 0 else x - 40.0
    thumb = oc.inner_thumb(x, body, False)
    far = -thumb
    c = k.c
    c.new_path()
    py = y - 22.0 * s
    oc.phone(k, x, py, s, v2._screen)
    edge = 22.0 * s
    lw = hands_ps.LW
    bend = math.radians(12.0)

    def outside_phone():
        pts = kit.rough_rect_pts(k, -22, -38, 44, 76, 3501)
        c.new_path()
        c.rectangle(x - 10 * w, y - 10 * w, 20 * w, 20 * w)
        c.move_to(x + pts[0][0] * s, py + pts[0][1] * s)
        for px_, py_ in pts[1:]:
            c.line_to(x + px_ * s, py + py_ * s)
        c.close_path()
        c.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
        c.clip()
        c.set_fill_rule(cairo.FILL_RULE_WINDING)

    def stroke(pts, t, col):
        c.set_source_rgb(*col)
        c.set_line_width(t)
        c.set_line_cap(cairo.LINE_CAP_ROUND)
        c.set_line_join(cairo.LINE_JOIN_ROUND)
        c.new_path()
        c.move_to(*pts[0])
        for p in pts[1:]:
            c.line_to(*p)
        c.stroke()

    def oval(cx, cy, rx, ry, col):
        c.save()
        c.translate(cx, cy)
        c.scale(rx, ry)
        c.new_path()
        c.arc(0, 0, 1, 0, 2 * math.pi)
        c.restore()
        c.set_source_rgb(*col)
        c.fill()

    fingers = []
    for fy, ln in ((-34.0, 9.0), (-23.0, 10.5), (-12.0, 8.0)):
        root = (x + far * (edge + 4.0 * s), y + fy * s - 1.5 * s)
        knuckle = (x + far * (edge - 1.0 * s), y + fy * s)
        tip = (
            knuckle[0] - far * ln * s * math.cos(bend),
            knuckle[1] + ln * s * math.sin(bend),
        )
        fingers.append([root, knuckle, tip])
    thumb_pts = [
        (x + thumb * 0.40 * w, y + 0.62 * w),
        (x + thumb * (edge - 4.0 * s), y + 12.0 * s),
        (x + thumb * (edge - 10.0 * s), y + 5.0 * s),
    ]
    arm_pts = [(x, y + 1.55 * w), (x, y + 0.40 * w)]
    side_pts = [
        (x + far * 0.40 * w, y + 0.66 * w),
        (x + far * (edge + 1.5 * s), y + 0.22 * w),
        (x + far * (edge + 1.5 * s), y - 34.0 * s),
    ]
    tf = 0.27 * w
    tt = 0.30 * w
    for ink in (True, False):
        col = hands_ps.INK if ink else skin
        grow = 2 * lw if ink else 0.0
        c.save()
        outside_phone()
        stroke(arm_pts, 0.60 * w + grow, col)
        oval(x, y + 0.44 * w, 0.62 * w + grow / 2, 0.42 * w + grow / 2, col)
        stroke(side_pts, 8.0 * s + grow, col)
        c.restore()
        for pts in fingers:
            stroke(pts, tf + grow, col)
        stroke(thumb_pts, tt + grow, col)
    c.set_line_cap(cairo.LINE_CAP_BUTT)
    c.set_line_join(cairo.LINE_JOIN_MITER)


# (row, version) -> the drawing. Old drawings stay here after a row moves on.
DRAWERS = {
    ("grab", "v2"): v2._grab,
    ("grab", "v3"): v3._grab,
    ("pinch", "v2"): v2._pinch,
    ("pinch", "v3"): v3._pinch,
    ("phone_grip", "v2"): v2._phone,
    ("phone_grip", "v3"): v3._phone,
    ("phone_grip", "v4a"): _phone_a,
    ("phone_grip", "v4b"): _phone_b,
}

ACCEPTED = {
    "grab": "v2",
    "pinch": "v2",
    "phone_grip": "v4b",
}

# Attempts waiting for Tomas's pick on the comparison sheet: row -> version.
CANDIDATES = {}


def _row_bands():
    y = v2.HEADER
    for job, _word, _mirror in v2.ROWS:
        h = v2._row_h(job)
        yield job, y, y + h
        y += h


def _same(a, b, box):
    return ImageChops.difference(a.crop(box), b.crop(box)).getbbox() is None


def check(path):
    """Each row equals the same row of its source sheet; the header equals v2."""
    new = Image.open(path).convert("RGB")
    src = {name: Image.open(p).convert("RGB") for name, p in SHEETS.items() if name != "v1"}
    width = new.size[0]
    bad = []
    if not _same(new, src["v2"], (0, 0, width, v2.HEADER * 2)):
        bad.append("header")
    for job, y0, y1 in _row_bands():
        ver = ACCEPTED.get(job, "v2")
        if ver not in src:
            continue
        if not _same(new, src[ver], (0, y0 * 2, width, y1 * 2)):
            bad.append("%s (%s)" % (job, ver))
    return bad


def write(path=OUT):
    if os.path.abspath(path) in {os.path.abspath(p) for p in SHEETS.values()}:
        raise RuntimeError("v4 must not overwrite an earlier class sheet")
    before = {name: v2._md5(p) for name, p in SHEETS.items()}
    saved = (v2._grab, v2._pinch, v2._phone)
    v2._grab = DRAWERS[("grab", ACCEPTED["grab"])]
    v2._pinch = DRAWERS[("pinch", ACCEPTED["pinch"])]
    v2._phone = DRAWERS[("phone_grip", ACCEPTED["phone_grip"])]
    tmp = path + ".tmp.png"
    try:
        v2.write(tmp)
    finally:
        v2._grab, v2._pinch, v2._phone = saved
    bad = check(tmp)
    if bad:
        os.remove(tmp)
        raise RuntimeError("rows differ from their source sheet: " + ", ".join(bad))
    os.replace(tmp, path)
    for name, p in SHEETS.items():
        if v2._md5(p) != before[name]:
            raise RuntimeError("%s class sheet changed" % name)
    return path


if __name__ == "__main__":
    print(write())
    print("red 0")
    print("rows match their source sheets")
    for job, ver in ACCEPTED.items():
        print("%s %s" % (job, ver))
    stills = os.path.join(os.path.dirname(__file__), "..", "the-blueprint", "stills")
    for name, want in v2.v1.LOCKED.items():
        got = v2._md5(os.path.join(stills, name))
        print("%s %s" % (name, "ok" if got == want else "CHANGED " + got))
