"""Hand library v4: the sheet of the five new poses and their checks (sandbox; hand_lib_v4.py says why). v3's sheet and
checks stand for its three poses (hand_lib_sheet_v3.py); this one draws all eight for the record.

  python3 hand_lib_sheet_v4.py        -> ../the-double-agent/hand_lib_v4_sheet.png, hand_lib_v4_sil.png (400 %, film
                                         size, left | right by hands_lr, each with what it holds)
  python3 hand_lib_sheet_v4.py check  -> PIECES, WRIST, CONTACT, MIRROR on every pose; the four planted faults again
"""
import math
import os
import sys

import cairo
import numpy as np
from PIL import Image

import kit
from kit import Ctx, INK
import hands_lr as lr
import hands_v4 as hv
import hand_lib_v4 as hl
import hand_lib_sheet_v3 as s3
import da_hands as dh

SKIN = s3.SKIN
OUT = "../the-double-agent"
MUSTARD = (0.86, 0.66, 0.16)
PAD = (0.12, 0.10, 0.10)
CARD = (0.99, 0.97, 0.90)

# the forearm's direction for the screen-right hand (the left mirrors it), and what the hand holds
SETUP = {
    "RELAXED": (0.0, 1.0),
    "CUP_GRIP": (math.sin(0.35), -math.cos(0.35)),
    "SAUCER_SUPPORT": (1.0, 0.0),
    "GRAB": (1.0, 0.0),
    "CLUTCH": (0.25, 1.0),                                       # the forearm coming down onto the bar
    "PINCH": (math.cos(-0.5), math.sin(-0.5)),
    "PALM": (math.sin(0.25), -math.cos(0.25)),
    "FIST": (0.0, 1.0),
}
CONTACT = {"CUP_GRIP": "handle", "SAUCER_SUPPORT": "touch", "GRAB": "object", "CLUTCH": "edge", "PINCH": "tip"}


def held_object(pose, k, x, y, ang, w, s_):
    """the object in scene coordinates, at the pose's contact (drawn before the hand, the fingers over it)."""
    c = k.c
    if pose == "GRAB":                                           # round 2: a thermos, narrower than the fist, so the
        P = hl.to_screen(pose, x, y, ang, w, s_, hl.contact(pose, "object"))   # knuckles and fingertips show past it
        kit.cut(k, [(P[0] - 0.27 * w, P[1] - 1.05 * w), (P[0] + 0.27 * w, P[1] - 1.05 * w),
                    (P[0] + 0.27 * w, P[1] + 0.95 * w), (P[0] - 0.27 * w, P[1] + 0.95 * w)], MUSTARD, shadow=False, lw=2)
        kit.ellipse(k, P[0], P[1] - 1.05 * w, 0.27 * w, 0.07 * w, (0.70, 0.52, 0.10), 7201, shadow=False, lw=1.6)
    elif pose == "CLUTCH":                                       # a bar seen from the front (the armrest's pad): its top at
        c.save(); c.translate(x, y); c.rotate(ang); c.scale(w, s_ * w)   # the knuckles, the fingers over its face
        c.rectangle(0.60, -1.10, 0.46, 2.20)
        c.restore()
        c.set_source_rgb(*PAD); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2); c.stroke()
    elif pose == "PINCH":                                        # a tag on its string, held at the string's end
        P = hl.to_screen(pose, x, y, ang, w, s_, hl.contact(pose, "tip"))
        c.set_source_rgb(0.93, 0.76, 0.28); c.set_line_width(3); c.move_to(*P); c.line_to(P[0], P[1] + 0.9 * w); c.stroke()
        kit.cut(k, [(P[0] - 0.42 * w, P[1] + 0.9 * w), (P[0] + 0.42 * w, P[1] + 0.9 * w),       # round 2: the gold cord and
                    (P[0] + 0.42 * w, P[1] + 1.5 * w), (P[0] - 0.42 * w, P[1] + 1.5 * w)], (0.80, 0.10, 0.12), shadow=False, lw=2)


def hand(k, pose, x, y, w, arm, parts="all", skin=SKIN):
    """one hand at its wrist, screen-right (arm +1) or the mirror (-1), with its forearm and its object."""
    dx, dy = SETUP[pose]
    d = (arm * dx, dy)
    ang = math.atan2(d[1], d[0])
    s_ = lr.side(arm, d) if pose != "SAUCER_SUPPORT" else arm
    if parts in ("all", "obj"):
        if pose in ("GRAB", "CLUTCH", "PINCH"):
            held_object(pose, k, x, y, ang, w, s_)
        elif pose == "CUP_GRIP":
            H = hl.to_screen(pose, x, y, ang, w, s_, hl.contact(pose, "handle"))
            Y1 = hl.to_screen(pose, x, y, ang, w, s_, (1.10, 1.06))
            s3.big_cup(k, H[0], H[1], 1.1 * w / 26.0, 1 if Y1[0] < H[0] else -1, w)
        if parts == "obj":
            if pose == "SAUCER_SUPPORT":
                Sp = hl.to_screen(pose, x, y, 0, w, arm, hl.contact(pose, "saucer"))
                s3.saucer_at(k, Sp[0], Sp[1], 0.95 * w / 30.0)
            return
    if parts == "all":
        s3.forearm(k, x, y, ang if pose != "SAUCER_SUPPORT" else (0.0 if arm > 0 else math.pi) - 0.45 * arm, w, skin=skin)
    obj = None
    if pose == "SAUCER_SUPPORT" and parts == "all":
        Sp = hl.to_screen(pose, x, y, 0, w, arm, hl.contact(pose, "saucer"))
        obj = lambda k_: s3.saucer_at(k_, Sp[0], Sp[1], 0.95 * w / 30.0)
    hl.draw_lr(k, pose, x, y, d, w, skin, arm, obj=obj, reach=arm)


def sheet():
    lr.setup(); hv.enable()
    poses = list(SETUP)
    W, H = 2400, 280 * len(poses) + 80
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    c = cairo.Context(s); c.set_source_rgb(0.97, 0.96, 0.93); c.paint(); k = Ctx(c, 0)
    c.select_font_face("Inter", 0, 1)
    for col, t in ((40, "pose"), (420, "400 %: left | right"), (1500, "film size (Don, 0.60): L R")):
        c.set_source_rgb(*INK); c.set_font_size(22); c.move_to(col, 40); c.show_text(t)
    lr.reset_log()
    for i, pose in enumerate(poses):
        y0 = 120 + i * 280
        lr.frame(cut=True)
        c.set_source_rgb(*INK); c.set_font_size(22); c.move_to(40, y0 + 60); c.show_text(pose + ("  (new, v4)" if i >= 3 else ""))
        for j, arm in enumerate((-1, 1)):
            hand(k, pose, 700 + j * 520 - arm * 60, y0 + 70, 68, arm)
        for j, arm in enumerate((-1, 1)):
            hand(k, pose, 1640 + j * 160, y0 + 70, 24.4 * 0.60 * 2.5, arm)   # the rig's hand at Don's scale, MC camera 2.5
    p = os.path.join(OUT, "hand_lib_v4_sheet.png")
    s.write_to_png(p)
    a = np.array(Image.open(p).convert("RGB")).astype(int)
    ink = (np.abs(a - np.array([247, 245, 237])).sum(axis=2) > 30)
    Image.fromarray(np.where(ink, 0, 255).astype(np.uint8)).convert("RGB").save(os.path.join(OUT, "hand_lib_v4_sil.png"))
    print("wrote hand_lib_v4_sheet.png, hand_lib_v4_sil.png; hands_lr:", "clean" if not lr.check() else lr.check())


def run_checks():
    lr.setup(); hv.enable()
    W, X, Y, w = 420, 150, 230, 68
    bad = 0
    for pose in SETUP:
        cp = None
        if pose in CONTACT:
            dx, dy = SETUP[pose]
            ang = math.atan2(dy, dx)
            s_ = lr.side(1, (dx, dy)) if pose != "SAUCER_SUPPORT" else 1
            cp = hl.to_screen(pose, X, Y, 0 if pose == "SAUCER_SUPPORT" else ang, w, s_, hl.contact(pose, CONTACT[pose]))
        obj = (lambda k, p=pose: hand(k, p, X, Y, w, 1, "obj")) if pose in CONTACT else None
        f = s3.check_one(pose, lambda k, p=pose: hand(k, p, X, Y, w, 1, "hand"), obj, cp,
                         (X, Y, 0.0 if pose == "SAUCER_SUPPORT" else math.atan2(SETUP[pose][1], SETUP[pose][0]), w),
                         mirror=lambda k, p=pose: hand(k, p, W - X, Y, w, -1, "hand"))
        print("%-16s %s" % (pose, "PASS" if not f else "FAIL"))
        for m in f:
            print("     ", m)
        bad += bool(f)
    print("(the planted faults: python3 hand_lib_sheet_v3.py check, the same check_one)")
    print("hand_lib v4 checks", "ok" if not bad else "FAIL")
    return 0 if not bad else 1


if __name__ == "__main__":
    if sys.argv[1:2] == ["check"]:
        sys.exit(run_checks())
    sheet()
