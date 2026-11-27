"""Hand class sheet, third pass. grab, pinch, and the phone only.

v2 left those three unreadable: grab's four fingers met at one point, pinch
read as a beak, and the phone's fingertips were separate ovals. This file
draws those three. Every other row stays on bp_hand_sheet_v2. hands_ps and
of_cast are not edited. The phone's dark frame stays.

  python3 bp_hand_sheet_v3.py
"""
import os

import bp_hand_sheet_v2 as v2
import hands_ps
import of_cast as oc

OUT = os.path.join(
    os.path.dirname(__file__),
    "..",
    "the-blueprint",
    "rough_work",
    "pic_hands",
    "bp_hand_classes_v3.png",
)
V1_PNG = os.path.join(os.path.dirname(OUT), "bp_hand_classes.png")
V2_PNG = os.path.join(os.path.dirname(OUT), "bp_hand_classes_v2.png")


def _pinch(c, x, y, w, skin, arm):
    """Thumb and index meet. The other three fingers stay short, on the far side."""
    s_ = v2._side(arm)
    c.save()
    c.translate(x, y)
    hands_ps._wrist(c, w, skin)
    hands_ps._blob(c, 0.22 * w, 0, 0.36 * w, 0.34 * w, skin)
    for reach, root, tip in ((0.36, 0.44, 0.36), (0.42, 0.28, 0.22), (0.48, 0.12, 0.08)):
        y0 = -s_ * root * w
        y1 = -s_ * tip * w
        hands_ps._cap(
            c,
            [(0.20 * w, y0), (reach * w, (y0 + y1) * 0.5), (reach * 0.70 * w, y1)],
            0.08 * w,
            skin,
        )
    hands_ps._cap(
        c,
        [(0.32 * w, -s_ * 0.14 * w), (0.54 * w, -s_ * 0.02 * w), (0.72 * w, s_ * 0.04 * w)],
        0.13 * w,
        skin,
    )
    hands_ps._cap(
        c,
        [(0.08 * w, s_ * 0.32 * w), (0.42 * w, s_ * 0.22 * w), (0.76 * w, s_ * 0.05 * w)],
        0.20 * w,
        skin,
    )
    c.restore()


def _grab(c, x, y, w, skin, arm):
    """Four fingers, each with its own tip. The thumb stays clear of them."""
    s_ = v2._side(arm)
    t = 0.08 * w
    c.save()
    c.translate(x, y)
    hands_ps._wrist(c, w, skin)
    hands_ps._blob(c, 0.20 * w, 0, 0.38 * w, 0.48 * w, skin)
    for reach, root, tip in (
        (0.78, 0.58, 0.56),
        (0.90, 0.40, 0.38),
        (1.00, 0.22, 0.20),
        (1.08, 0.08, 0.06),
    ):
        y0 = -s_ * root * w
        y1 = -s_ * tip * w
        hands_ps._cap(
            c,
            [(0.26 * w, y0), (reach * w, (y0 + y1) * 0.5), (reach * 0.62 * w, y1)],
            t,
            skin,
        )
    hands_ps._cap(
        c,
        [(0.02 * w, s_ * 0.16 * w), (0.36 * w, s_ * 0.40 * w), (0.64 * w, s_ * 0.26 * w)],
        t * 1.5,
        skin,
    )
    c.restore()


def _at(x, y, s, p):
    return (x + p[0] * s, y + p[1] * s)


def _phone(k, x, y, w, skin, arm):
    """Palm and phone from the current grip. Fingers are drawn here, joined to the palm."""
    s = w / 26.0
    body = x + 40.0 if arm < 0 else x - 40.0
    thumb = oc.inner_thumb(x, body, False)
    far = -thumb
    # The label leaves a current point. phone_grip's arc would stroke a line from that word.
    k.c.new_path()
    oc.phone_grip(k, x, y, s, skin=skin, body_x=body, part="back")
    oc.phone(k, x, y - 22.0 * s, s, v2._screen)
    c = k.c
    t = 6.0 * s
    for root, mid, tip in (
        ((far * 18, -30), (far * 21, -38), (far * 20, -46)),
        ((far * 16, -6), (far * 21, -10), (far * 20, -16)),
        ((far * 14, 10), (far * 21, 6), (far * 20, 2)),
    ):
        hands_ps._cap(c, [_at(x, y, s, root), _at(x, y, s, mid), _at(x, y, s, tip)], t, skin)
    hands_ps._cap(
        c,
        [
            _at(x, y, s, (thumb * 12, 14)),
            _at(x, y, s, (thumb * 20, 4)),
            _at(x, y, s, (thumb * 18, -6)),
        ],
        t * 1.15,
        skin,
    )


def write(path=OUT):
    if os.path.basename(path) in ("bp_hand_classes.png", "bp_hand_classes_v2.png"):
        raise RuntimeError("v3 must not overwrite an earlier class sheet")
    before = {name: v2._md5(p) for name, p in (("v1", V1_PNG), ("v2", V2_PNG)) if os.path.exists(p)}
    v2._pinch = _pinch
    v2._grab = _grab
    v2._phone = _phone
    out = v2.write(path)
    after = {name: v2._md5(p) for name, p in (("v1", V1_PNG), ("v2", V2_PNG))}
    for name in before:
        if after[name] != before[name]:
            raise RuntimeError("%s class sheet changed" % name)
    return out


if __name__ == "__main__":
    print(write())
    print("red 0")
    stills = os.path.join(os.path.dirname(__file__), "..", "the-blueprint", "stills")
    for name, want in v2.v1.LOCKED.items():
        got = v2._md5(os.path.join(stills, name))
        print("%s %s" % (name, "ok" if got == want else "CHANGED " + got))
