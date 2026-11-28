"""v2 (mom_bc_v1.py = v1, kept), after the audit (the design stays; the action gets clear):
- "sweet" is pushed: the head tilts (tilt=, default -7 degrees for sweet), cheeks raised, tighter shut eyes;
- "lick": the tissue is at her tongue, touching it;
- "wipe": the elbow stays low so the forearm comes in under Don's pass, the tissue is squashed flat against the
  vest beside the stain, with two scrub marks; wipe_at() aims it;
- the forgotten curler is bigger and sits clear of the hat.
MOM, "The Best Candidate", v1: candidate 3, "a sweet old lady". The Office Noir character (mom_on.py: the same
head, heavy glasses on the pearl chain, the same solid square body) dressed for an interview:
- a teal wool coat with the housecoat's mustard shawl collar, three big mustard buttons, one housecoat flower as
  a brooch: her palette, so a viewer of Office Noir half-knows her before the reveal;
- a teal pillbox hat with a mustard band over set grey curls, and ONE lilac curler she forgot to take out
  (the silent clue; curler=False removes it);
- a cream handbag held in both hands, stockings, sensible mauve shoes.
New face "sweet" (the act: eyes shut in a smile, soft brows, a sugary smile, a blush). She is sweet to the panel
and never to Don: "stern", "unimpressed", "shout" and "proud" are mom_on's, unchanged.
Poses: "bag" (both hands on the handbag), "thread" (picks a thread off Don's collar: arm out to screen left),
"lick" (the tissue at her tongue), "wipe" (the tissue on his vest: pass pose=wipe_at(tx, ty) to aim it),
"hip" (hand on hip, the bag on her arm), "stand".
mom_on.py, kit and every earlier character are untouched (its hair, eye, brow and mouth functions are swapped for
the length of one call and restored).
Usage: o = mom(k, x, feet, s, pose, face, look, mouth=None, lean=0, thrust=0, bag=None, curler=True)
       -> {"head", "hands"}"""
import math
import kit
import mom_on as mo
from kit import INK, cut, rect, ellipse

TEAL, TEAL_DARK, MUSTARD, MUSTARD_DARK, CREAM = mo.TEAL, mo.TEAL_DARK, mo.MUSTARD, mo.MUSTARD_DARK, mo.CREAM
SKIN, HAIR, HAIR_DARK, MAUVE, LEGS = mo.SKIN, mo.HAIR, mo.HAIR_DARK, mo.MAUVE, mo.LEGS
BT, HY, HEM, SH_X = mo.BT, mo.HY, mo.HEM, mo.SH_X
WAIST = mo.SASH
BAG = (0.97, 0.91, 0.76)
BAG_DARK = (0.80, 0.70, 0.50)
SHOE = (0.50, 0.33, 0.44)
BLUSH = (0.93, 0.52, 0.60)
TISSUE = (1, 1, 1)


def _ik_low(side, tx, ty, ln=50):
    """Like mom_on.ik, but the elbow takes the lower of the two solutions (the forearm comes in level)."""
    sx, sy = side * SH_X, BT + 16
    vx, vy = tx - sx, ty - sy
    D = min(math.hypot(vx, vy), 2 * ln - 0.5)
    angD = math.degrees(math.atan2(vx, vy))
    al = math.degrees(math.acos(D / (2 * ln)))
    best = None
    for sg in (1, -1):
        a1 = angD + sg * al
        ey = sy + math.cos(math.radians(a1)) * ln
        if best is None or ey > best[0]:
            best = (ey, a1, -2 * sg * al)
    return best[1], best[2]


def wipe_at(tx, ty):
    """A pose that puts her screen-right hand (the tissue) at body point (tx, ty): just left of Don's stain."""
    return (-10, 4) + _ik_low(1, tx, ty)


TUPLE_NAME = ["wipe"]   # opt-in (28 Nov, ep15): what a pose given as angles is called; "wipe" (as before) draws the tissue

POSES = {
    "stand": (-10, 4, 10, -4),
    "bag": mo.ik(-1, -11, WAIST - 2) + mo.ik(1, 11, WAIST - 2),
    "thread": mo.ik(-1, -112, BT - 4) + mo.ik(1, 26, WAIST + 6),
    "lick": mo.ik(-1, -30, WAIST + 6) + mo.ik(1, 31, HY + 52),
    "wipe": wipe_at(118, BT + 78),
    "hip": mo.ik(-1, -60, WAIST + 4) + mo.ik(1, 34, WAIST - 4),
}


def handbag(k, x, y, s=1.0, seed=0):
    """(x, y) = the top of the handle, where her hands are."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    c.new_path(); c.arc(0, 20, 20, math.pi, 2 * math.pi)
    c.set_source_rgb(*INK); c.set_line_width(8); c.stroke_preserve()
    c.set_source_rgb(*BAG_DARK); c.set_line_width(4.4); c.stroke()
    cut(k, [(-30, 22), (30, 22), (35, 66), (-35, 66)], BAG, lw=2.2)
    cut(k, [(-30, 22), (30, 22), (26, 40), (0, 45), (-26, 40)], BAG, shadow=False, lw=2)
    ellipse(k, 0, 44, 5.5, 5.5, MUSTARD, seed + 3, shadow=False, lw=1.8)
    c.restore()


def _hair_hat(curler):
    def draw(k, seed, back=False):
        c = k.c
        top = HY - 58
        for sx in (-1, 1):                                              # the set hair at the sides (mom_on's)
            c.new_path()
            c.move_to(sx * 50, HY - 28); c.curve_to(sx * 66, HY - 16, sx * 64, HY + 10, sx * 54, HY + 18)
            c.line_to(sx * 46, HY + 6); c.line_to(sx * 46, HY - 26); c.close_path()
            mo._fill_stroke(c, HAIR, 2.2)
        c.new_path()
        c.move_to(-56, HY - 22); c.curve_to(-62, top - 8, 62, top - 8, 56, HY - 22)
        c.curve_to(30, HY - 34, -30, HY - 34, -56, HY - 22); c.close_path()
        mo._fill_stroke(c, HAIR, 2.4)
        if curler:                                                      # the one she missed
            mo._curler(c, -60, HY - 34, 42, -1.0, big=True)
        for i in range(7):                                              # the curls the others left behind
            u = i / 6.0
            cx = -45 + 90 * u
            cy = HY - 27 - 9 * math.sin(math.pi * u)
            c.new_path(); c.arc(cx, cy, 9.5, 0, 2 * math.pi); mo._fill_stroke(c, HAIR, 2.0)
            c.set_source_rgb(*HAIR_DARK); c.set_line_width(1.4)
            c.new_path(); c.arc(cx, cy, 4.5, 0.2 * math.pi, 1.5 * math.pi); c.stroke()
        c.save(); c.translate(4, top + 6); c.rotate(0.07)                # the pillbox hat, slightly off
        mo._rrect(c, -38, -22, 76, 34, 9); mo._fill_stroke(c, TEAL, 2.4)
        c.new_path(); c.rectangle(-38, 2, 76, 9); mo._fill_stroke(c, MUSTARD, 1.8)
        mo.flower(c, 24, 2, 9.5, 0.3)
        c.restore()
    return draw


def _sweet(inner_eyes, inner_brows, inner_mouth):
    def eyes(c, face, look, turn=0.0):
        if face != "sweet":
            inner_eyes(c, face, look, turn)
            return
        c.set_source_rgb(*INK); c.set_line_width(3.8); c.set_line_cap(1)   # squeezed shut in a smile, low in the lens
        for sx in (-1, 1):
            c.new_path(); c.arc(sx * 20 + turn, HY + 9, 7.0, math.pi * 1.08, math.pi * 1.92); c.stroke()
        c.set_line_cap(0)

    def brows(c, face, turn=0.0):
        inner_brows(c, "proud" if face == "sweet" else face, turn)

    def mouth(c, face, m, turn=0.0):
        if face != "sweet":
            inner_mouth(c, face, m, turn)
            return
        for sx in (-1, 1):
            c.save(); c.translate(turn + sx * 36, HY + 17); c.scale(11, 7.5); c.new_path(); c.arc(0, 0, 1, 0, 2 * math.pi)
            c.restore(); c.set_source_rgba(*BLUSH, 0.6); c.fill()
            c.set_source_rgb(*mo.SKIN_SHADE); c.set_line_width(2.0)       # cheeks pushed up under the glasses
            c.new_path(); c.arc(turn + sx * 34, HY + 20, 12, math.pi * 1.15, math.pi * 1.85); c.stroke()
        if m:
            inner_mouth(c, "proud", m, turn)
            return
        inner_mouth(c, "none", "M", turn)                               # nose and jaw lines only
        my = HY + 30
        c.set_source_rgb(*SKIN); c.rectangle(turn - 16, my - 6, 32, 13); c.fill()
        c.set_source_rgb(*MAUVE); c.set_line_width(4.6); c.set_line_cap(1)
        c.new_path(); c.move_to(turn - 17, my - 5); c.curve_to(turn - 8, my + 9, turn + 8, my + 9, turn + 17, my - 5)
        c.stroke()
        c.set_source_rgb(*INK); c.set_line_width(1.6)
        for sx in (-1, 1):
            c.new_path(); c.move_to(turn + sx * 17, my - 9); c.line_to(turn + sx * 20, my - 4); c.stroke()
        c.set_line_cap(0)
    return eyes, brows, mouth


def _hand(k, x, y, seed):
    ellipse(k, x, y, 11, 11, SKIN, seed, shadow=False, lw=2)


def _tissue(k, x, y, seed, s=1.0):
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    cut(k, [(-11, -6), (-3, -13), (6, -9), (13, -2), (8, 9), (-2, 12), (-10, 6)], TISSUE, shadow=False, lw=1.8)
    c.set_source_rgb(0.75, 0.78, 0.84); c.set_line_width(1.2)
    c.new_path(); c.move_to(-4, -6); c.line_to(1, 2); c.line_to(7, -1); c.stroke()
    c.restore()


def mom(k, x, feet, s=1.0, pose="bag", face="sweet", look=(0, 0), seed=70, mouth=None, lean=0.0, thrust=0.0, bag=None,
        curler=True, tilt=None):
    c = k.c
    if lean:
        c.save(); c.translate(x, feet); c.rotate(math.radians(lean)); c.translate(-x, -feet)
        try:
            out = mom(k, x, feet, s, pose, face, look, seed, mouth, 0.0, thrust, bag, curler, tilt)
            dev = {"head": c.user_to_device(*out["head"]), "hands": [c.user_to_device(*q) for q in out["hands"]]}
        finally:
            c.restore()
        return {"head": c.device_to_user(*dev["head"]), "hands": [c.device_to_user(*q) for q in dev["hands"]]}
    name = pose if isinstance(pose, str) else TUPLE_NAME[0]
    if tilt is None:
        tilt = -7.0 if face == "sweet" else 0.0
    a = POSES[pose] if isinstance(pose, str) else pose
    if bag is None:
        bag = name in ("bag", "hip", "thread")
    c.save(); c.translate(x, feet); c.scale(s, s)
    for sx in (-1, 1):                                                  # stockings, sensible shoes
        rect(k, sx * 20 - 9, HEM - 4, 18, -HEM - 8, LEGS, seed + 2 + sx, shadow=False, lw=2)
        ellipse(k, sx * 23, -7, 19, 9, SHOE, seed + 5 + sx, lw=2)
        rect(k, sx * 23 - 9, -18, 18, 6, SHOE, seed + 7 + sx, shadow=False, lw=1.6)
    pts = mo._coat_pts(k, seed)
    cut(k, pts, TEAL)
    c.set_source_rgb(*TEAL_DARK); c.set_line_width(2.2)
    c.new_path(); c.move_to(-SH_X - 10, HEM - 7); c.line_to(SH_X + 10, HEM - 7); c.stroke()      # the hem
    c.new_path(); c.move_to(-16, BT - 4); c.line_to(0, BT + 46); c.line_to(16, BT - 4); c.close_path()
    mo._fill_stroke(c, CREAM, 1.8)                                      # a cream blouse, buttoned to the top
    for sx in (-1, 1):                                                  # the shawl collar: the housecoat's mustard
        c.new_path(); c.move_to(sx * 18, BT - 6); c.line_to(sx * 36, BT - 4); c.line_to(sx * 3, BT + 64)
        c.line_to(sx * 0, BT + 48); c.close_path()
        mo._fill_stroke(c, MUSTARD, 2.0)
    c.set_source_rgb(*INK); c.set_line_width(1.8)
    c.new_path(); c.move_to(3, BT + 64); c.line_to(9, HEM); c.stroke()   # the front edge
    for i, by in enumerate((BT + 84, BT + 116, BT + 148)):
        ellipse(k, -7, by, 6.5, 6.5, MUSTARD, seed + 30 + i, shadow=False, lw=1.8)
        c.set_source_rgb(*MUSTARD_DARK)
        for dx in (-2, 2):
            c.new_path(); c.arc(-7 + dx, by, 1.1, 0, 2 * math.pi); c.fill()
    for sx in (-1, 1):                                                  # pocket flaps
        rect(k, sx * 38 - 15, WAIST + 26, 30, 9, TEAL, seed + 36 + sx, shadow=False, lw=1.8)
    mo.flower(c, 33, BT + 34, 11, 0.2)                                   # the brooch: one flower off the housecoat
    tdx, tdy, tsc = -10 * thrust, 10 * thrust, 1 + 0.08 * thrust
    rect(k, -14 + tdx * 0.5, BT - 14 - 4 * thrust, 28, 18 + 4 * thrust, mo.SKIN_SHADE, seed + 50, shadow=False, lw=2)
    old = (mo._hair_and_curlers, mo._eyes, mo._brows, mo._mouth)
    mo._hair_and_curlers = _hair_hat(curler)
    mo._eyes, mo._brows, mo._mouth = _sweet(old[1], old[2], old[3])
    try:
        c.save(); c.translate(tdx, tdy); c.translate(0, BT); c.scale(tsc, tsc); c.rotate(math.radians(tilt))
        c.translate(0, -BT)
        mo._head(k, face, look, mouth, seed, "front")
        c.restore()
    finally:
        mo._hair_and_curlers, mo._eyes, mo._brows, mo._mouth = old
    hands = []
    if bag and name == "bag":
        handbag(k, 0, WAIST - 4, 1.0, seed + 80)
    for side, (u, f) in ((-1, (a[0], a[1])), (1, (a[2], a[3]))):
        hands.append(kit.arm(k, side * SH_X, BT + 16, u, f, TEAL, SKIN, seed + 10 + side, ln=50, w=22))
    if bag and name in ("hip", "thread"):                               # the bag on her other arm
        handbag(k, hands[1][0] + 2, hands[1][1] - 6, 0.9, seed + 80)
    for i, (hx, hy) in enumerate(hands):
        _hand(k, hx, hy, seed + 60 + i)
    if name == "lick":                                                  # the tissue held up to her tongue, touching
        hx, hy = hands[1]
        _tissue(k, hx - 4, hy - 13, seed + 90, 1.1)
        _hand(k, hx + 5, hy + 3, seed + 61)
        if not mouth:
            c.save(); c.translate(11, HY + 37); c.rotate(0.25); c.scale(10, 5); c.new_path(); c.arc(0, 0, 1, 0, 2 * math.pi)
            c.restore(); mo._fill_stroke(c, (0.90, 0.48, 0.55), 1.8)
            c.set_source_rgb(0.72, 0.30, 0.40); c.set_line_width(1.2)
            c.new_path(); c.move_to(6, HY + 36); c.line_to(16, HY + 38.5); c.stroke()
    elif name == "wipe":                                                # squashed flat on the vest, scrubbing
        hx, hy = hands[1]
        cut(k, [(hx + 2, hy - 13), (hx + 15, hy - 10), (hx + 19, hy + 1), (hx + 14, hy + 12), (hx + 1, hy + 13)], TISSUE,
            shadow=False, lw=1.8)
        _hand(k, hx - 3, hy, seed + 61)
        c.set_source_rgb(*INK); c.set_line_width(2.4); c.set_line_cap(1)
        for d in (0, 9):                                                # two scrub marks
            c.new_path(); c.arc(hx - 2, hy - 2, 24 + d, -1.35, -0.75); c.stroke()
            c.new_path(); c.arc(hx - 2, hy + 2, 24 + d, 0.75, 1.35); c.stroke()
        c.set_line_cap(0)
    elif name == "thread":                                              # a thread between finger and thumb
        hx, hy = hands[0]
        c.set_source_rgb(*INK); c.set_line_width(1.6)
        c.new_path(); c.move_to(hx - 8, hy - 6); c.curve_to(hx - 16, hy - 16, hx - 8, hy - 22, hx - 18, hy - 30); c.stroke()
    c.restore()
    return {"head": (x, feet + HY * s), "hands": [(x + hx * s, feet + hy * s) for hx, hy in hands]}
