"""Hand library v2 (hand_lib_v2.py): the test sheet. v1 kept as hand_lib_sheet_v1.py.

Hand library v1: the test sheet and the checks (sandbox, not the canon; hand_lib_v1.py says why).

  python3 hand_lib_sheet_v1.py           -> ../the-double-agent/hand_lib_v2_sheet.png  (400 %, film size, half size,
                                            left and right, with their objects; the old capsule hands beside them)
                                            ../the-double-agent/hand_lib_v2_sil.png    (the same, solid black)
  python3 hand_lib_sheet_v1.py check     -> the checks on the library's hands, then on the planted faults; exits 1 if a
                                            library hand fails or a planted fault passes

The checks read the picture (each hand and its object drawn alone, as masks):
  PIECES   the hand is one piece: no part apart from the rest (5.2 v2's fingertip stub floating at the saucer's rim)
  WRIST    the object covers no part of the wrist band (5.2 cup v1: the saucer drawn across the wrist)
  CONTACT  the object touches the hand within 2 px of its contact point (S8r v1: a grab on nothing)
  MIRROR   the right hand is the left hand mirrored (of_cast.clutch: one thumb side for both hands)
"""
import math
import os
import sys

import cairo
import numpy as np
from PIL import Image
from scipy import ndimage

import kit
from kit import Ctx, INK
import hand_lib_v2 as hl
import da_hands as dh
import hands_ps as hp
import hands_v4 as hv
import of_cast as oc

SKIN = (0.96, 0.78, 0.66)
SLEEVE = (0.97, 0.97, 0.95)
OUT = "../the-double-agent"


def forearm(k, x, y, ang, w, ln=1.5):
    """the forearm into the wrist: tapered, the wrist as wide as the hand's (0.60 w), the sleeve's cuff behind."""
    c = k.c
    ca, sa = math.cos(ang), math.sin(ang)
    nx, ny = -sa, ca
    bx, by = x - ca * ln * w, y - sa * ln * w
    pts = [(bx + nx * 0.40 * w, by + ny * 0.40 * w), (x + nx * 0.30 * w, y + ny * 0.30 * w),
           (x - nx * 0.30 * w, y - ny * 0.30 * w), (bx - nx * 0.40 * w, by - ny * 0.40 * w)]
    kit.cut(k, pts, SKIN, shadow=False, lw=hl.LW)
    cx_, cy_ = x - ca * ln * 0.75 * w, y - sa * ln * 0.75 * w            # the cuff
    cpts = [(bx + nx * 0.46 * w, by + ny * 0.46 * w), (cx_ + nx * 0.42 * w, cy_ + ny * 0.42 * w),
            (cx_ - nx * 0.42 * w, cy_ - ny * 0.42 * w), (bx - nx * 0.46 * w, by - ny * 0.46 * w)]
    kit.cut(k, cpts, SLEEVE, shadow=False, lw=hl.LW)


def cup_at(k, hx, hy, s, side, lift=0.0):
    """the cup upright, its handle's middle at (hx, hy - lift); side +1: the body to the LEFT of the handle. v2: lift
    puts the handle's middle above the fingers, so its loop shows over the fist (v1: the fist hid it)."""
    hy = hy - lift
    dh.cup(k, hx - side * (15 + 6.5) * s, hy + 12 * s, s, side)


def saucer_at(k, x, y, s):
    """the saucer lying on (x, y) (its underside's middle); 30 s half wide."""
    kit.ellipse(k, x, y - 8 * s, 30 * s, 9 * s, dh.CHINA, 7121, shadow=False, lw=2)          # v2: tipped a little to us
    kit.ellipse(k, x, y - 9.5 * s, 14 * s, 4 * s, dh.CHINA_D, 7122, shadow=False, lw=1.2)


# The poses as a film would hold them: the forearm's angle on screen, which way the hand reaches.
SETUP = {
    "RELAXED": dict(ang=math.pi / 2),                                   # hanging
    "CUP_GRIP": dict(ang=-math.pi / 2 - 0.35),                          # the forearm rising, the cup at the cheek
    "SAUCER_SUPPORT": dict(ang=0.0),
}


def lib_hand(k, pose, x, y, w, side, parts="all"):
    """parts: "all", "hand" (the hand only, for its mask), "obj" (the object only)."""
    ang = SETUP[pose]["ang"]
    if pose == "CUP_GRIP" and side < 0:
        ang = math.pi - ang                                              # the left hand mirrors the right
    if pose == "RELAXED" and side < 0:
        ang = math.pi - ang
    s = 1.1 * w / 26.0                                                   # the cup about a hand wide; the saucer under 2 w
    obj = back = None
    if pose == "CUP_GRIP":
        H = hl.to_screen(pose, x, y, ang, w, side, hl.contact(pose, "handle"))
        Y1 = hl.to_screen(pose, x, y, ang, w, side, (hl.contact(pose, "handle")[0], hl.contact(pose, "handle")[1] + 1))
        body_left = 1 if Y1[0] < H[0] else -1                           # the cup's body on the thumb's side, the little finger away
        back = lambda k_: cup_at(k_, H[0], H[1], s, body_left, 0.22 * w)
    if pose == "SAUCER_SUPPORT":
        Sp = hl.to_screen(pose, x, y, ang, w, side, hl.contact(pose, "saucer"))
        obj = lambda k_: saucer_at(k_, Sp[0], Sp[1], 0.95 * w / 30.0)
    if parts == "obj":
        (back or obj)(k)
        return
    if parts != "hand":
        forearm(k, x, y, ang if pose != "SAUCER_SUPPORT" else (0.0 if side > 0 else math.pi) + 0.25 * side, w)
    hl.draw(k, pose, x, y, ang, w, SKIN, side,
            obj=None if parts == "hand" else obj, back_obj=None if parts == "hand" else back)


def old_hand(k, pose, x, y, w, side):
    """the same jobs with today's hands (the capsules), for the comparison column."""
    ang = SETUP[pose]["ang"]
    if pose == "RELAXED":
        hp.draw(k, "quiet", x, y, w * 1.25, SKIN, (math.cos(ang), math.sin(ang)), side)
    elif pose == "CUP_GRIP":
        a = ang if side > 0 else math.pi - ang
        dh.cup_in_pinch(k, x, y, (math.cos(a), math.sin(a)), w * 1.25, SKIN, side, (x - side * 60, y - 40), w / 17 * 1.45)
    else:
        dh.saucer_hold(k, x, y, (1, 0), w * 1.25, SKIN, side, w / 17 * 1.25)


def sheet():
    hv.enable()
    sizes = (("400 %", 68), ("film", 20), ("half", 10))
    W, H = 2200, 1500
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    c = cairo.Context(s)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    k = Ctx(c, 0)
    c.select_font_face("Inter", 0, 1)
    for col, t in ((60, "pose"), (330, "library v2, 400 %  (left | right)"), (1150, "film size, half (L R L R)"),
                   (1650, "today's capsules, 400 % and film")):
        c.set_source_rgb(*INK); c.set_font_size(22); c.move_to(col, 40); c.show_text(t)
    for row, pose in enumerate(("RELAXED", "CUP_GRIP", "SAUCER_SUPPORT")):
        y0 = 120 + row * 460
        c.set_source_rgb(*INK); c.set_font_size(22); c.move_to(40, y0 + 200); c.show_text(pose)
        dx = {"RELAXED": (0, -120), "CUP_GRIP": (0, 260), "SAUCER_SUPPORT": (-60, 60)}[pose]
        for i, side in enumerate((-1, 1)):
            lib_hand(k, pose, 470 + i * 420 + dx[0] * side, y0 + 200 + dx[1] * 0.6, 68, side)
        x = 1180
        for wv in (20, 10):
            for side in (-1, 1):
                lib_hand(k, pose, x, y0 + 200 + dx[1] * 0.12, wv, side); x += 120
        try:
            old_hand(k, pose, 1780, y0 + 200 + dx[1] * 0.6, 68, 1)
            old_hand(k, pose, 2080, y0 + 200, 20, 1)
        except Exception as e:
            c.set_source_rgb(0.7, 0, 0); c.set_font_size(16); c.move_to(1700, y0 + 300); c.show_text(str(e)[:60])
    path = os.path.join(OUT, "hand_lib_v2_sheet.png")
    s.write_to_png(path)
    im = Image.open(path).convert("RGB")
    a = np.array(im).astype(int)
    bg = np.array([247, 245, 237])
    ink = (np.abs(a - bg).sum(axis=2) > 30)
    sil = Image.fromarray(np.where(ink, 0, 255).astype(np.uint8)).convert("RGB")
    sil.save(os.path.join(OUT, "hand_lib_v2_sil.png"))
    print("wrote hand_lib_v2_sheet.png, hand_lib_v2_sil.png")


# ---- the checks -----------------------------------------------------------------------------------------------------

def _mask(draw, W=420, H=420):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    c = cairo.Context(s)
    draw(Ctx(c, 0))
    s.flush()
    a = np.frombuffer(s.get_data(), np.uint8).reshape(H, s.get_stride() // 4, 4)[:, :W, 3]
    return a > 40


def check_one(name, hand, obj, contact_pt, wrist, mirror=None):
    out = []
    hm = _mask(hand)
    lab, n = ndimage.label(hm)
    sizes = ndimage.sum(hm, lab, range(1, n + 1))
    if n > 1 and sorted(sizes)[-2] > 12:
        out.append("PIECES %s: %d pieces (the second %d px)" % (name, n, sorted(sizes)[-2]))
    if obj is not None:
        om = _mask(obj)
        x, y, ang, w = wrist
        yy, xx = np.mgrid[0:om.shape[0], 0:om.shape[1]]
        u = (xx - x) * math.cos(ang) + (yy - y) * math.sin(ang)
        v = -(xx - x) * math.sin(ang) + (yy - y) * math.cos(ang)
        band = (u > -0.6 * w) & (u < 0.12 * w) & (np.abs(v) < 0.34 * w)
        if (om & band).sum() > 6:
            out.append("WRIST %s: the object covers %d px of the wrist" % (name, (om & band).sum()))
        cx, cy = contact_pt
        near = ((xx - cx) ** 2 + (yy - cy) ** 2) < 3.0 ** 2
        dil = ndimage.binary_dilation(hm, iterations=2)
        if not (om & dil & ndimage.binary_dilation(near, iterations=4)).any():
            out.append("CONTACT %s: the object does not touch the hand at its contact point" % name)
    if mirror is not None:
        mm = _mask(mirror)[:, ::-1]
        inter, union = (hm & mm).sum(), (hm | mm).sum()
        if union and inter / float(union) < 0.95:
            out.append("MIRROR %s: the right hand is not the left mirrored (IoU %.2f)" % (name, inter / float(union)))
    return out


def run_checks():
    hv.enable()
    W = 420
    res = {}
    w = 68
    X, Y = 210, 210
    for pose in ("RELAXED", "CUP_GRIP", "SAUCER_SUPPORT"):
        ang = SETUP[pose]["ang"]
        f = []
        hand = lambda k, s_=1, p=pose: lib_hand(k, p, X if s_ > 0 else W - X, Y, w, s_, "hand")
        obj = None if pose == "RELAXED" else (lambda k, p=pose: lib_hand(k, p, X, Y, w, 1, "obj"))
        cp = None
        if pose != "RELAXED":
            nm = "handle" if pose == "CUP_GRIP" else "saucer"
            cp = hl.to_screen(pose, X, Y, ang, w, 1, hl.contact(pose, nm))
        f += check_one(pose, lambda k: hand(k, 1), obj, cp, (X, Y, ang if pose != "SAUCER_SUPPORT" else 0.0, w),
                       mirror=lambda k: hand(k, -1))
        res["library " + pose] = f
    # the planted faults
    plants = {}
    plants["PIECES: a fingertip apart (5.2 v2 saucer)"] = check_one(
        "plant", lambda k: (lib_hand(k, "RELAXED", X, Y, w, 1, "hand"), kit.ellipse(k, X + 160, Y - 80, 8, 6, SKIN, 1, shadow=False)),
        None, None, None)
    plants["WRIST: the saucer across the wrist (5.2 cup v1)"] = check_one(
        "plant", lambda k: lib_hand(k, "SAUCER_SUPPORT", X, Y, w, 1, "hand"),
        lambda k: saucer_at(k, X, Y + 4, 0.95 * w / 30.0), (X + 1.12 * w, Y - 0.30 * w), (X, Y, 0.0, w))
    plants["CONTACT: the cup off the hand (a grab on nothing)"] = check_one(
        "plant", lambda k: lib_hand(k, "CUP_GRIP", X, Y, w, 1, "hand"),
        lambda k: cup_at(k, X - 120, Y - 140, 1.1 * w / 26.0, 1),
        hl.to_screen("CUP_GRIP", X, Y, SETUP["CUP_GRIP"]["ang"], w, 1, hl.contact("CUP_GRIP", "handle")),
        (X, Y, SETUP["CUP_GRIP"]["ang"], w))
    plants["MIRROR: of_cast.clutch for both hands"] = check_one(
        "plant", lambda k: oc.clutch(k, X, Y, w, SKIN), None, None, None,
        mirror=lambda k: oc.clutch(k, W - X, Y, w, SKIN))
    bad = 0
    for n_, f in res.items():
        print("%-34s %s" % (n_, "PASS" if not f else "FAIL"))
        for m in f:
            print("     ", m)
        bad += bool(f)
    for n_, f in plants.items():
        print("plant %-52s %s" % (n_, "caught" if f else "MISSED"))
        for m in f:
            print("     ", m)
        bad += not f
    print("hand_lib checks", "ok" if not bad else "FAIL")
    return 0 if not bad else 1


if __name__ == "__main__":
    if sys.argv[1:2] == ["check"]:
        sys.exit(run_checks())
    sheet()
