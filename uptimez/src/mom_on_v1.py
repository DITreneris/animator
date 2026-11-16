"""MOM, "Office Noir", v1. A new character: Don's mother, the reality check. Formidable, solid, never softens in
this episode. Built from the kit's paper-cutout primitives in the series style (square-ish head, flat cut-out
body, kit.arm arms), with no red anywhere:
- the most solid silhouette in the series: square padded shoulders, wide stance, a head taller than Pam;
- lilac foam curlers under a hairnet over short grey-brown hair;
- a quilted teal-and-mustard floral housecoat, belted tight with a mustard sash and bow, cream piping, a cream
  nightgown at the neck; fluffy lilac slippers;
- heavy black reading glasses low on the nose, on a pearl bead chain;
- the #1 MOM mug.
Faces: "stern" (default), "shout" (the DONNIE!), "unimpressed" (one brow up), "proud" (rare; later episodes).
Poses: "stand", "loom" (shot 10: leaning over the bed, finger pointing down, mug on the other hand),
"hip_mug" (hand on hip, mug up), "folded" (arms folded, the doorway).
Views: "front", "three" (three-quarter), "back".
Usage: o = mom(k, x, feet, s, pose, face, look, seed, view, mug=None, mouth=None, lean=0)  -> {"head", "hands"}"""
import math
import cairo
import kit
from kit import INK, cut, rect, ellipse

TEAL = (0.13, 0.49, 0.50)
TEAL_DARK = (0.08, 0.33, 0.35)
MUSTARD = (0.88, 0.67, 0.17)
MUSTARD_DARK = (0.66, 0.47, 0.08)
CREAM = (0.98, 0.94, 0.84)
LILAC = (0.74, 0.64, 0.90)
LILAC_DARK = (0.52, 0.42, 0.72)
HAIR = (0.52, 0.48, 0.46)
HAIR_DARK = (0.36, 0.33, 0.32)
SKIN = (0.94, 0.76, 0.64)
SKIN_SHADE = (0.80, 0.60, 0.50)
LEGS = (0.86, 0.72, 0.62)
MAUVE = (0.55, 0.36, 0.46)
PEARL = (0.96, 0.95, 0.90)
MUG = (0.99, 0.99, 0.97)

BT = -240                    # shoulders (body units above the feet)
HY = BT - 54                 # head centre
HEM = -64                    # housecoat hem, mid-calf
SASH = -160
SH_X = 52                    # shoulder joint x


def ik(side, tx, ty, ln=50):
    """Arm angles (kit convention) putting this arm's hand at body point (tx, ty), elbow outward."""
    sx, sy = side * SH_X, BT + 16
    vx, vy = tx - sx, ty - sy
    D = min(math.hypot(vx, vy), 2 * ln - 0.5)
    angD = math.degrees(math.atan2(vx, vy))
    al = math.degrees(math.acos(D / (2 * ln)))
    best = None
    for sg in (1, -1):
        a1 = angD + sg * al
        ex = sx + math.sin(math.radians(a1)) * ln
        if best is None or ex * side > best[0]:
            best = (ex * side, a1, -2 * sg * al)
    return best[1], best[2]


POSES = {
    "stand": (-10, 4, 10, -4),
    "hip_mug": ik(-1, -60, SASH + 4) + ik(1, 30, BT + 66),
    "loom": ik(-1, -98, BT + 112) + ik(1, 30, BT + 66),
    "folded": ik(-1, 34, BT + 56) + ik(1, -34, BT + 50),
}
MUG_POSES = {"hip_mug", "loom"}


def _rrect(c, x, y, w, h, r):
    c.new_path()
    c.arc(x + w - r, y + r, r, -math.pi / 2, 0); c.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    c.arc(x + r, y + h - r, r, math.pi / 2, math.pi); c.arc(x + r, y + r, r, math.pi, 1.5 * math.pi)
    c.close_path()


def _fill_stroke(c, col, lw=2.6, ink=INK):
    c.set_source_rgb(*col); c.fill_preserve(); c.set_source_rgb(*ink); c.set_line_width(lw); c.stroke()


def _coat_pts(k, seed):
    r = k.rng(seed)
    pts = [(-SH_X - 4, BT + 2), (-SH_X + 8, BT - 6), (SH_X - 8, BT - 6), (SH_X + 4, BT + 2),
           (SH_X + 10, SASH), (SH_X + 12, HEM), (-SH_X - 12, HEM), (-SH_X - 10, SASH)]
    return [(px + r.uniform(-1.2, 1.2), py + r.uniform(-1.2, 1.2)) for px, py in pts]


def flower(c, x, y, rr, rot=0.0):
    for i in range(5):
        a = rot + i * 2 * math.pi / 5
        c.new_path(); c.arc(x + math.cos(a) * rr * 0.75, y + math.sin(a) * rr * 0.75, rr * 0.55, 0, 2 * math.pi)
        c.set_source_rgb(*MUSTARD); c.fill_preserve(); c.set_source_rgb(*MUSTARD_DARK); c.set_line_width(1.0)
        c.stroke()
    c.new_path(); c.arc(x, y, rr * 0.38, 0, 2 * math.pi); c.set_source_rgb(*CREAM); c.fill()


def _pattern(k, pts, seed, back=False):
    """Quilting diamonds + scattered mustard flowers, clipped to the coat."""
    c = k.c
    c.save()
    c.new_path(); c.move_to(*pts[0])
    for q in pts[1:]:
        c.line_to(*q)
    c.close_path(); c.clip()
    c.set_source_rgba(*TEAL_DARK, 0.55); c.set_line_width(1.1)
    for i in range(-14, 15):
        x0 = i * 22
        c.move_to(x0 - 200, BT - 20); c.line_to(x0 + 200, BT + 380); c.stroke()
        c.move_to(x0 + 200, BT - 20); c.line_to(x0 - 200, BT + 380); c.stroke()
    r = k.rng(seed + 300)                         # same flowers every boil (seeded on seed only)
    import random
    rr = random.Random(seed * 17 + 5)
    for _ in range(26):
        fx, fy = rr.uniform(-SH_X - 10, SH_X + 10), rr.uniform(BT + 6, HEM - 6)
        flower(c, fx, fy, rr.uniform(5.0, 7.5), rr.uniform(0, 6.28))
    c.restore()


def _slipper(k, x, seed):
    c = k.c
    rr = k.rng(seed)
    c.new_path()
    n = 22
    for i in range(n + 1):
        a = math.pi + i * math.pi / n
        rad = 1 + rr.uniform(-0.08, 0.1) + (0.08 if i % 2 else 0)
        px, py = x + math.cos(a) * 24 * rad, -2 + math.sin(a) * 15 * rad
        c.line_to(px, py)
    c.line_to(x + 24, 4); c.line_to(x - 24, 4); c.close_path()
    _fill_stroke(c, LILAC, 2.2)
    c.set_source_rgba(1, 1, 1, 0.45)
    for i in range(6):
        c.new_path(); c.arc(x - 14 + i * 5.6, -12 + rr.uniform(-2, 2), 2.0, 0, 2 * math.pi); c.fill()


def _curler(c, x, y, w, rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot)
    _rrect(c, -w / 2, -8, w, 16, 7)
    _fill_stroke(c, LILAC, 2.0)
    c.set_source_rgb(*LILAC_DARK); c.set_line_width(1.0)
    for i in range(1, int(w / 6)):
        xx = -w / 2 + i * 6
        c.move_to(xx, -6); c.line_to(xx, 6); c.stroke()
    for sx in (-1, 1):
        c.new_path(); c.arc(sx * (w / 2 - 1), 0, 4.5, 0, 2 * math.pi)
        _fill_stroke(c, CREAM, 1.4)
    c.restore()


def _hair_and_curlers(k, seed, back=False):
    c = k.c
    top = HY - 58
    # short set hair at the sides and nape
    for sx in (-1, 1):
        c.new_path()
        c.move_to(sx * 50, HY - 28); c.curve_to(sx * 66, HY - 16, sx * 64, HY + 10, sx * 54, HY + 18)
        c.line_to(sx * 46, HY + 6); c.line_to(sx * 46, HY - 26); c.close_path()
        _fill_stroke(c, HAIR, 2.2)
    # the curler cap: a dome of hair under the net
    c.new_path()
    c.move_to(-56, HY - 22); c.curve_to(-62, top - 8, 62, top - 8, 56, HY - 22)
    c.curve_to(30, HY - 34 if not back else HY - 10, -30, HY - 34 if not back else HY - 10, -56, HY - 22)
    c.close_path()
    _fill_stroke(c, HAIR, 2.4)
    rows = [(-30, top + 10, 30, -0.10), (2, top + 4, 32, 0.02), (32, top + 12, 28, 0.14),
            (-44, top + 30, 24, -0.5), (44, top + 30, 24, 0.5), (-14, top + 26, 28, 0.0), (16, top + 26, 28, 0.04)]
    if back:
        rows += [(-20, top + 44, 30, 0.0), (18, top + 46, 30, 0.0)]
    for (cx, cy, w, rot) in rows:
        _curler(c, cx, cy, w, rot)
    # the hairnet: a thin diagonal mesh over the dome and a band at the hairline
    c.save()
    c.new_path(); c.move_to(-60, HY - 18); c.curve_to(-66, top - 16, 66, top - 16, 60, HY - 18); c.close_path()
    c.clip()
    c.set_source_rgba(*HAIR_DARK, 0.55); c.set_line_width(0.8)
    for i in range(-12, 13):
        c.move_to(i * 9 - 60, top - 20); c.line_to(i * 9 + 60, HY); c.stroke()
        c.move_to(i * 9 + 60, top - 20); c.line_to(i * 9 - 60, HY); c.stroke()
    c.restore()
    c.set_source_rgb(*HAIR_DARK); c.set_line_width(2.4)
    c.new_path(); c.move_to(-57, HY - 20)
    c.curve_to(-30, HY - 32 if not back else HY - 8, 30, HY - 32 if not back else HY - 8, 57, HY - 20); c.stroke()


def _eyes(c, face, look, turn=0.0):
    lx, ly = look
    ey = HY - 4
    for sx in (-1, 1):
        x = sx * 20 + turn
        if face == "proud":
            c.set_source_rgb(*INK); c.set_line_width(3.4)
            c.new_path(); c.arc(x, ey + 3, 8, math.pi * 1.15, math.pi * 1.85); c.stroke()
            continue
        big = face == "shout"
        rx, ry = (10.5, 10.5) if big else (9.0, 8.0)
        c.new_path(); c.save(); c.translate(x, ey); c.scale(rx, ry); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        _fill_stroke(c, (1, 1, 1), 2.0)
        pr = 3.2 if big else 4.2
        c.new_path(); c.arc(x + lx * 3.5, ey + ly * 3 + (1 if not big else 0), pr, 0, 2 * math.pi)
        c.set_source_rgb(*INK); c.fill()
        lid = {"stern": -2.0, "unimpressed": 0.5 if sx > 0 else -1.0, "shout": -11}.get(face, -3)
        if lid > -10:                                       # heavy upper lid: skin over the top of the eye
            c.save(); c.new_path(); c.save(); c.translate(x, ey); c.scale(rx + 1, ry + 1)
            c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.clip()
            c.new_path(); c.rectangle(x - 14, ey - 14, 28, 14 + lid)
            c.set_source_rgb(*SKIN_SHADE); c.fill(); c.restore()
            c.set_source_rgb(*INK); c.set_line_width(2.6)
            c.new_path(); c.move_to(x - rx - 1, ey + lid); c.line_to(x + rx + 1, ey + lid); c.stroke()
        # crow's feet + bags
        c.set_source_rgb(*SKIN_SHADE); c.set_line_width(1.4)
        c.new_path(); c.move_to(x + sx * 12, ey - 2); c.line_to(x + sx * 17, ey - 5); c.stroke()
        c.new_path(); c.move_to(x + sx * 12, ey + 2); c.line_to(x + sx * 17, ey + 3); c.stroke()
        c.new_path(); c.arc(x, ey + 6, 8, 0.25 * math.pi, 0.75 * math.pi); c.stroke()


def _brows(c, face, turn=0.0):
    by = HY - 20
    c.set_source_rgb(*HAIR_DARK); c.set_line_width(5.2); c.set_line_cap(1)
    for sx in (-1, 1):
        x = sx * 20 + turn
        if face == "shout":
            inner, outer = by + 8, by - 6
        elif face == "stern":
            inner, outer = by + 5, by - 2
        elif face == "unimpressed":
            inner, outer = (by + 2, by + 1) if sx < 0 else (by - 10, by - 6)
        else:                                               # proud: soft, lifted
            inner, outer = by - 4, by - 2
        c.new_path()
        if face == "unimpressed" and sx > 0:
            c.move_to(x - 10, inner); c.curve_to(x - 2, by - 16, x + 6, by - 14, x + 12, outer)
        else:
            c.move_to(x - sx * 10, inner); c.line_to(x + sx * 12, outer)
        c.stroke()
    c.set_line_cap(0)


def _mouth(c, face, mouth, turn=0.0):
    my = HY + 30
    x = turn
    c.set_source_rgb(*SKIN_SHADE); c.set_line_width(1.6)          # nasolabial lines, a firm jaw
    for sx in (-1, 1):
        c.new_path(); c.move_to(x + sx * 12, HY + 12); c.curve_to(x + sx * 18, HY + 22, x + sx * 18, my, x + sx * 16, my + 6)
        c.stroke()
    c.set_source_rgb(*INK); c.set_line_width(2.4)                   # nose
    c.new_path(); c.move_to(x - 2, HY + 4); c.curve_to(x - 7, HY + 16, x + 6, HY + 18, x + 5, HY + 14); c.stroke()
    m = mouth or {"shout": "A"}.get(face)
    if m in ("A", "O", "E"):
        w, h = {"A": (16, 15), "O": (9, 11), "E": (14, 7)}[m]
        c.new_path(); c.save(); c.translate(x, my + 2); c.scale(w, h); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        _fill_stroke(c, (0.22, 0.13, 0.15), 2.4, MAUVE)
        c.save(); c.new_path(); c.save(); c.translate(x, my + 2); c.scale(w, h); c.arc(0, 0, 1, 0, 2 * math.pi)
        c.restore(); c.clip()
        c.set_source_rgb(1, 1, 1); c.rectangle(x - w, my + 2 - h, 2 * w, h * 0.4); c.fill()
        c.restore()
        c.set_source_rgb(*INK); c.set_line_width(1.6)
        c.new_path(); c.save(); c.translate(x, my + 2); c.scale(w + 1, h + 1); c.arc(0, 0, 1, 0, 2 * math.pi)
        c.restore(); c.stroke()
        return
    c.set_line_cap(1)
    if face == "proud":
        c.set_source_rgb(*MAUVE); c.set_line_width(4.2)
        c.new_path(); c.move_to(x - 9, my); c.curve_to(x - 3, my + 4, x + 3, my + 4, x + 9, my); c.stroke()
    elif face == "unimpressed":
        c.set_source_rgb(*MAUVE); c.set_line_width(4.2)
        c.new_path(); c.move_to(x - 8, my + 2); c.line_to(x + 12, my - 2); c.stroke()
        c.set_source_rgb(*INK); c.set_line_width(1.6)
        c.new_path(); c.move_to(x + 12, my - 4); c.line_to(x + 15, my - 2); c.stroke()
    else:                                                    # stern: a flat line, corners down
        c.set_source_rgb(*MAUVE); c.set_line_width(4.4)
        c.new_path(); c.move_to(x - 13, my + 4); c.line_to(x - 9, my); c.line_to(x + 9, my); c.line_to(x + 13, my + 4)
        c.stroke()
    c.set_line_cap(0)


def _glasses(c, turn=0.0, with_chain=True):
    gy = HY + 2
    c.set_source_rgb(*INK); c.set_line_width(4.2)
    for sx in (-1, 1):
        x = sx * 20 + turn
        _rrect(c, x - 13, gy - 8, 26, 16, 3)
        c.set_source_rgba(0.88, 0.93, 0.97, 0.35); c.fill_preserve()
        c.set_source_rgb(*INK); c.stroke()
    c.new_path(); c.move_to(turn - 7, gy - 2); c.line_to(turn + 7, gy - 2); c.stroke()
    if with_chain:                                            # pearl bead chain from the temples down behind the neck
        for sx in (-1, 1):
            x0 = sx * 34 + turn
            for i in range(9):
                u = i / 8
                bx = x0 + sx * (8 * math.sin(u * math.pi * 0.9))
                by = gy + 4 + u * 62
                c.new_path(); c.arc(bx, by, 2.4, 0, 2 * math.pi)
                c.set_source_rgb(*PEARL); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(0.9); c.stroke()


def _head(k, face, look, mouth, seed, view):
    c = k.c
    turn = {"three": -14.0}.get(view, 0.0)
    if view == "back":
        for sx in (-1, 1):
            c.new_path(); c.save(); c.translate(sx * 55, HY + 4); c.scale(8, 12); c.arc(0, 0, 1, 0, 2 * math.pi)
            c.restore(); _fill_stroke(c, SKIN, 2.0)
        _rrect(c, -54, HY - 52, 108, 100, 30); _fill_stroke(c, HAIR)          # the back of the head: all hair
        c.set_source_rgb(*HAIR_DARK); c.set_line_width(1.4)
        for i in range(-3, 4):
            c.new_path(); c.move_to(i * 12, HY + 6); c.line_to(i * 13, HY + 44); c.stroke()
        _hair_and_curlers(k, seed, back=True)
        return
    for sx in (-1, 1):                                        # ears (one hidden in three-quarter)
        if view == "three" and sx < 0:
            continue
        c.new_path(); c.save(); c.translate(sx * 55, HY + 4); c.scale(8, 12); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        _fill_stroke(c, SKIN, 2.0)
    c.new_path()                                              # the head: square-ish, a wide firm jaw
    c.move_to(-52, HY - 40); c.curve_to(-54, HY - 56, 54, HY - 56, 52, HY - 40)
    c.curve_to(56, HY + 20, 50, HY + 46, 30, HY + 50); c.line_to(-30, HY + 50)
    c.curve_to(-50, HY + 46, -56, HY + 20, -52, HY - 40); c.close_path()
    _fill_stroke(c, SKIN)
    c.set_source_rgb(*SKIN_SHADE); c.set_line_width(1.6)      # jowls
    for sx in (-1, 1):
        c.new_path(); c.arc(turn + sx * 30, HY + 40, 10, (0.2 if sx > 0 else 0.55) * math.pi, (0.45 if sx > 0 else 0.8) * math.pi)
        c.stroke()
    _hair_and_curlers(k, seed)
    _eyes(c, face, look, turn)
    _brows(c, face, turn)
    _glasses(c, turn)
    _mouth(c, face, mouth, turn)


def _mug(k, x, y, s=1.0, seed=0):
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    c.new_path(); c.arc(17, 0, 9, -math.pi / 2, math.pi / 2); c.set_source_rgb(*INK); c.set_line_width(7.5); c.stroke()
    c.new_path(); c.arc(17, 0, 9, -math.pi / 2, math.pi / 2); c.set_source_rgb(*MUG); c.set_line_width(4); c.stroke()
    _rrect(c, -15, -18, 32, 36, 4); _fill_stroke(c, MUG, 2.2)
    c.new_path(); c.save(); c.translate(1, -18); c.scale(16, 4); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
    _fill_stroke(c, (0.42, 0.27, 0.16), 1.6)
    kit.text(k, "#1", 1, -4, 11, TEAL_DARK)
    kit.text(k, "MOM", 1, 8, 10, TEAL_DARK)
    c.restore()


def _hand(k, x, y, seed, point=False):
    c = k.c
    ellipse(k, x, y, 11, 11, SKIN, seed, shadow=False, lw=2)
    if point:
        c.set_source_rgb(*INK); c.set_line_width(8); c.set_line_cap(1)
        c.new_path(); c.move_to(x, y + 4); c.line_to(x - 6, y + 22); c.stroke()
        c.set_source_rgb(*SKIN); c.set_line_width(5)
        c.new_path(); c.move_to(x, y + 4); c.line_to(x - 6, y + 22); c.stroke()
        c.set_line_cap(0)


def mom(k, x, feet, s=1.0, pose="stand", face="stern", look=(0, 0), seed=70, view="front", mug=None, mouth=None,
        lean=0.0):
    c = k.c
    if lean:
        c.save(); c.translate(x, feet); c.rotate(math.radians(lean)); c.translate(-x, -feet)
        try:
            out = mom(k, x, feet, s, pose, face, look, seed, view, mug, mouth, 0.0)
            dev = {"head": c.user_to_device(*out["head"]), "hands": [c.user_to_device(*q) for q in out["hands"]]}
        finally:
            c.restore()
        return {"head": c.device_to_user(*dev["head"]), "hands": [c.device_to_user(*q) for q in dev["hands"]]}
    if mug is None:
        mug = pose in MUG_POSES
    c.save(); c.translate(x, feet)
    if view == "three":
        c.scale(s * 0.88, s)
    else:
        c.scale(s, s)
    # legs + slippers
    for sx in (-1, 1):
        rect(k, sx * 20 - 9, HEM - 4, 18, -HEM - 10, LEGS, seed + 2 + sx, shadow=False, lw=2)
        _slipper(k, sx * 22, seed + 5 + sx)
    pts = _coat_pts(k, seed)
    cut(k, pts, TEAL)
    _pattern(k, pts, seed, back=view == "back")
    c.set_source_rgb(*CREAM); c.set_line_width(4)                       # cream piping at the hem
    c.new_path(); c.move_to(-SH_X - 12, HEM + 4); c.line_to(SH_X + 12, HEM + 4); c.stroke()
    if view != "back":
        c.new_path(); c.move_to(-16, BT - 4); c.line_to(0, BT + 46); c.line_to(16, BT - 4); c.close_path()   # nightgown V
        _fill_stroke(c, CREAM, 1.8)
        for sx in (-1, 1):                                              # the shawl collar, mustard with piping
            c.new_path(); c.move_to(sx * 18, BT - 6); c.line_to(sx * 34, BT - 4); c.line_to(sx * 2, BT + 60)
            c.line_to(sx * 0, BT + 48); c.close_path()
            _fill_stroke(c, MUSTARD, 2.0)
        c.set_source_rgb(*INK); c.set_line_width(1.8)                   # the wrap overlap down to the hem
        c.new_path(); c.move_to(2, BT + 60); c.line_to(10, HEM); c.stroke()
        for sx in (-1, 1):                                              # patch pockets
            rect(k, sx * 38 - 14, SASH + 30, 28, 26, TEAL, seed + 30 + sx, shadow=False, lw=1.8)
            c.set_source_rgb(*CREAM); c.set_line_width(2.4)
            c.new_path(); c.move_to(sx * 38 - 13, SASH + 33); c.line_to(sx * 38 + 13, SASH + 33); c.stroke()
    rect(k, -SH_X - 11, SASH - 7, 2 * SH_X + 22, 14, MUSTARD, seed + 40, shadow=False, lw=2)   # the sash
    if view != "back":                                                  # the bow, tied tight, slightly off-centre
        bx = 10
        for sx in (-1, 1):
            c.new_path(); c.move_to(bx, SASH); c.curve_to(bx + sx * 10, SASH - 16, bx + sx * 24, SASH - 10, bx + sx * 20, SASH)
            c.curve_to(bx + sx * 24, SASH + 10, bx + sx * 10, SASH + 14, bx, SASH); c.close_path()
            _fill_stroke(c, MUSTARD, 2.0)
            c.new_path(); c.move_to(bx - 3 + sx * 2, SASH + 4); c.line_to(bx + sx * 9, SASH + 40)
            c.line_to(bx + sx * 15, SASH + 36); c.line_to(bx + 3 + sx * 2, SASH + 4); c.close_path()
            _fill_stroke(c, MUSTARD, 2.0)
        c.new_path(); c.arc(bx, SASH, 5, 0, 2 * math.pi); _fill_stroke(c, MUSTARD_DARK, 1.8)
    # neck + head
    rect(k, -14, BT - 14, 28, 18, SKIN_SHADE, seed + 50, shadow=False, lw=2)
    _head(k, face, look, mouth, seed, view)
    # arms (sleeves teal, cuffs cream)
    if view == "back":
        a = POSES["stand"]
    else:
        a = POSES[pose]
    hands = []
    for side, (u, f) in ((-1, (a[0], a[1])), (1, (a[2], a[3]))):
        hx, hy = kit.arm(k, side * SH_X, BT + 16, u, f, TEAL, SKIN, seed + 10 + side, ln=50, w=22)
        hands.append((hx, hy))
    for i, (hx, hy) in enumerate(hands):
        point = (pose == "loom" and i == 0 and view != "back")
        _hand(k, hx, hy, seed + 60 + i, point=point)
    if mug and view != "back":
        hx, hy = hands[1]
        _mug(k, hx + 6, hy - 6, 1.0, seed)
        _hand(k, hx - 6, hy + 2, seed + 70)
    c.restore()
    sx_ = s * (0.88 if view == "three" else 1.0)
    return {"head": (x, feet + HY * s), "hands": [(x + hx * sx_, feet + hy * s) for hx, hy in hands]}
