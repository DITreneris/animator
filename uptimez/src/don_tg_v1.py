"""DON, Thanksgiving film ("Raises for Everyone"), v1. His v4 office look (don_v4.py: open navy fleece vest,
white shirt, khakis, staff badge, the ketchup squiggle nobody mentions) plus:
- a classic, loud stars-and-stripes necktie (blue canton with white stars under the knot, red and white
  stripes to the tip), sitting in the open strip of the vest;
- a gravy drip on the tie beside the ketchup: nobody mentions that either;
- a turkey leg prop with a paper frill; `bites` 0..3 so it gets eaten across the film.
New faces: "grin" (don_v4), "laugh" (HA!), "drop" (the smile freezing), "chew" (cheek full), "deflated".
New poses (arm angles): POSE_SLAP, POSE_LAUGH, POSE_TAP, POSE_TEAR, POSE_POINT, POSE_BACKME, POSE_BLOCK.
don_v4.py, kit.py and every earlier Don are untouched (costume through kit.BADGE_HOOK, faces through a
temporary kit.face_draw wrap).
Usage: p = don(k, x, feet, s, pose, face, look, seed=500, leg=None|(bites, angle_deg, grip), gravy=True)"""
import math
import cairo
import kit
import brand
import don_v4 as dv
from kit import INK, cut, rect, ellipse

FLAG_RED = (0.80, 0.10, 0.14)
FLAG_BLUE = (0.12, 0.20, 0.50)
FLAG_WHITE = (0.99, 0.99, 0.97)
GRAVY = (0.50, 0.31, 0.14)
GRAVY_DARK = (0.34, 0.20, 0.08)
MEAT = (0.74, 0.42, 0.17)
MEAT_DARK = (0.52, 0.26, 0.09)
MEAT_IN = (0.95, 0.83, 0.68)
BONE = (0.97, 0.94, 0.84)
SKIN = kit.PEOPLE["DON"]["skin"]

POSE_SLAP = (-8, 0, 62, 28)        # shot 1: right hand down flat on the form, arm forward
POSE_LAUGH = (-35, 110, 128, 40)   # shot 4: left hand on the belly, right hand up, about to slap the table
POSE_TAP = (-8, 0, 52, 2)          # shot 6: right index finger tapping the form
POSE_TEAR = (-38, 118, 38, -118)   # shot 8: both hands at the chest, tearing the leg off
POSE_POINT = (-8, 0, 92, -8)       # shot 8: the turkey leg pointed at Pam like a gavel
POSE_BACKME = (-35, 110, 60, 95)   # shot 10: hand on hip, thumb back over his shoulder at the robot
POSE_BLOCK = (-62, 30, 128, -36)   # shot 11: leg held up over the robot's screen, left hand sliding the form


def star(c, x, y, r):
    c.move_to(x, y - r)
    for i in range(1, 10):
        a_ = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        c.line_to(x + math.cos(a_) * rr, y + math.sin(a_) * rr)
    c.close_path()


def flag_tie(k, bt, gravy=True, seed=0):
    c = k.c
    shape = [(-5, bt + 12), (5, bt + 12), (10, bt + 74), (0, bt + 86), (-10, bt + 74)]
    c.save()
    c.move_to(*shape[0])
    for p in shape[1:]:
        c.line_to(*p)
    c.close_path(); c.clip()
    c.set_source_rgb(*FLAG_WHITE); c.paint()
    c.set_source_rgb(*FLAG_RED)                           # diagonal stripes, as on a real tie
    for i in range(-2, 10):
        y0 = bt + 36 + i * 9
        c.move_to(-14, y0); c.line_to(14, y0 - 8); c.line_to(14, y0 - 3.5); c.line_to(-14, y0 + 4.5); c.close_path()
    c.fill()
    c.set_source_rgb(*FLAG_BLUE); c.rectangle(-14, bt + 10, 28, 26); c.fill()
    c.set_source_rgb(*FLAG_WHITE)
    for sx_, sy_ in ((-3.5, 17), (3.5, 17), (0, 24), (-3.5, 31), (3.5, 31)):
        star(c, sx_, bt + sy_, 2.6); c.fill()
    c.restore()
    c.set_source_rgb(*INK); c.set_line_width(1.8); c.set_line_join(1)
    c.move_to(*shape[0])
    for p in shape[1:]:
        c.line_to(*p)
    c.close_path(); c.stroke()
    cut(k, [(-7, bt + 2), (7, bt + 2), (5, bt + 13), (-5, bt + 13)], FLAG_RED, shadow=False, lw=1.8)   # knot
    if gravy:                                             # a gravy splat with one short run, mid-tie
        c.save(); c.translate(-2, bt + 52)
        c.move_to(-5, -2)
        for (a_, r_) in ((0.0, 6), (0.9, 4.2), (1.7, 6.4), (2.6, 4.4), (3.4, 6), (4.3, 4.6), (5.2, 6.2)):
            c.line_to(math.cos(a_) * r_, math.sin(a_) * r_ * 0.8)
        c.close_path()
        c.move_to(-1.8, 2); c.line_to(1.8, 2); c.line_to(1.4, 10); c.arc(0, 10, 1.6, 0, math.pi); c.close_path()
        c.set_source_rgb(*GRAVY); c.fill_preserve()
        c.set_source_rgb(*GRAVY_DARK); c.set_line_width(1.4); c.stroke()
        c.set_source_rgba(1, 1, 1, 0.75); c.arc(-2, -1.5, 1.1, 0, 2 * math.pi); c.fill()
        c.set_source_rgb(*GRAVY); c.arc(6, 7, 1.3, 0, 2 * math.pi); c.fill()
        c.restore()


def _costume(stain, badge, gravy):
    base = dv._costume(stain, False)

    def hook(k, name_, p, bt, seed):
        c = k.c
        base(k, name_, p, bt, seed)                       # trousers, collar, ketchup, open vest, mark
        c.save()                                          # the tie sits in the open strip, over the shirt
        flag_tie(k, bt, gravy, seed + 90)
        c.restore()
        for sx in (-1, 1):                                # re-lay the collar points over the knot
            cut(k, [(0, bt + 2), (sx * 16, bt - 2), (sx * 12, bt + 16)], dv.SHIRT, shadow=False, lw=1.6)
        cut(k, [(-6, bt + 3), (6, bt + 3), (5, bt + 12), (-5, bt + 12)], FLAG_RED, shadow=False, lw=1.6)
        if badge:
            dv.staff_badge(k, "DON", 14, bt + 34, 29, 8)
    return hook


def _faces(orig):
    def face_draw(k, x, y, face, look, glasses=False, seed=0):
        c = k.c
        my = y + 28
        if face == "grin":
            orig(k, x, y, "neutral", look, glasses=glasses, seed=seed)
            ellipse(k, x + 1, my - 2, 19, 9, SKIN, seed + 90, shadow=False, outline=False)
            c.set_source_rgb(*INK); c.set_line_width(4); c.set_line_cap(1)
            c.arc(x, my - 14, 15, 0.2 * math.pi, 0.8 * math.pi); c.stroke()
            c.move_to(x - 26, y - 22); c.line_to(x - 9, y - 25); c.stroke()      # brows up: the showman
            c.move_to(x + 9, y - 25); c.line_to(x + 26, y - 22); c.stroke()
        elif face == "laugh":
            orig(k, x, y, "happy", look, glasses=glasses, seed=seed)
            ellipse(k, x + 1, my - 3, 19, 10, SKIN, seed + 90, shadow=False, outline=False)
            c.move_to(x - 16, my - 6); c.line_to(x + 16, my - 6)                 # big open D
            c.curve_to(x + 16, my + 12, x - 16, my + 12, x - 16, my - 6); c.close_path()
            c.set_source_rgb(0.35, 0.08, 0.08); c.fill_preserve()
            c.set_source_rgb(*INK); c.set_line_width(3); c.stroke()
            c.save(); c.translate(x, my + 4); c.scale(8, 3.5); c.arc(0, 0, 1, math.pi, 2 * math.pi); c.restore()
            c.set_source_rgb(0.85, 0.40, 0.40); c.fill()
            c.set_source_rgb(1, 1, 1); c.rectangle(x - 13, my - 5, 26, 4); c.fill()
            c.set_source_rgb(*INK); c.set_line_width(4); c.set_line_cap(1)
            c.move_to(x - 26, y - 20); c.line_to(x - 9, y - 24); c.stroke()
            c.move_to(x + 9, y - 24); c.line_to(x + 26, y - 20); c.stroke()
        elif face == "drop":                              # the smile freezing: eyes wide, a stiff thin smile
            orig(k, x, y, "neutral", look, glasses=glasses, seed=seed)
            ellipse(k, x + 1, my - 1, 19, 9, SKIN, seed + 90, shadow=False, outline=False)
            c.set_source_rgb(*INK); c.set_line_width(3.4); c.set_line_cap(1)
            c.move_to(x - 13, my - 3); c.curve_to(x - 6, my + 1, x + 6, my + 1, x + 13, my - 3); c.stroke()
            c.set_line_width(3)
            c.move_to(x - 25, y - 21); c.line_to(x - 9, y - 21); c.stroke()
            c.move_to(x + 9, y - 21); c.line_to(x + 25, y - 21); c.stroke()
        elif face == "chew":                              # eyes shut with pleasure, one cheek full
            orig(k, x, y, "pleased", look, glasses=glasses, seed=seed)
            ellipse(k, x + 1, my - 1, 19, 9, SKIN, seed + 90, shadow=False, outline=False)
            ellipse(k, x + 26, y + 20, 15, 13, SKIN, seed + 91, shadow=False, lw=2)
            c.save(); c.arc(x + 26, y + 20, 16, 0, 2 * math.pi); c.clip()
            c.set_source_rgb(*SKIN); c.rectangle(x + 4, y + 2, 14, 40); c.fill()
            c.restore()
            c.set_source_rgb(*INK); c.set_line_width(3.4); c.set_line_cap(1)
            c.move_to(x - 10, my - 1); c.curve_to(x - 4, my + 3, x + 2, my - 4, x + 9, my); c.stroke()
            c.set_source_rgb(*MEAT); c.arc(x + 12, my + 4, 2, 0, 2 * math.pi); c.fill()   # a crumb
        elif face == "deflated":                          # the collapse: heavy lids, a flat frown
            orig(k, x, y, "neutral", (look[0], 0.6), glasses=glasses, seed=seed)
            c.set_source_rgb(*SKIN)
            for sx in (-17, 17):
                c.rectangle(x + sx - 12, y - 12, 24, 10); c.fill()
            c.set_source_rgb(*INK); c.set_line_width(4); c.set_line_cap(1)
            for sx in (-17, 17):
                c.move_to(x + sx - 11, y - 2); c.line_to(x + sx + 11, y - 2); c.stroke()
            ellipse(k, x + 1, my - 1, 19, 9, SKIN, seed + 90, shadow=False, outline=False)
            c.move_to(x - 11, my + 3); c.curve_to(x - 4, my - 3, x + 4, my - 3, x + 11, my + 3); c.stroke()
        else:
            orig(k, x, y, face, look, glasses=glasses, seed=seed)
    return face_draw


def turkey_leg(k, x, y, s=1.0, ang=0.0, bites=0, seed=0):
    """Drumstick held at the bone end (x, y); points along `ang` (degrees, 0 = screen right)."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(math.radians(ang)); c.scale(s, s)
    cut(k, [(-6, -4), (26, -5), (26, 5), (-6, 4)], BONE, shadow=False, lw=2)             # bone
    ellipse(k, -8, -4, 5, 5, BONE, seed, shadow=False, lw=1.8)
    ellipse(k, -8, 4, 5, 5, BONE, seed + 1, shadow=False, lw=1.8)
    pts = [(22, -9), (34, -18), (52, -21), (66, -15), (72, 0), (66, 15), (52, 21), (34, 18), (22, 9)]
    holes = [(71, -9, 9), (67, 13, 8.5), (55, -21, 8.5)][:bites]

    def poly():
        c.move_to(*pts[0])
        for q in pts[1:]:
            c.line_to(*q)
        c.close_path()

    def outside_holes():                                  # clip to everything except the bites
        c.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
        c.rectangle(-200, -200, 400, 400)
        for (bx, by, r) in holes:
            c.new_sub_path(); c.arc(bx, by, r, 0, 2 * math.pi)
        c.clip()
        c.set_fill_rule(cairo.FILL_RULE_WINDING)

    c.save(); poly(); c.clip(); outside_holes()
    c.set_source_rgb(*MEAT); c.paint()
    c.set_source_rgb(*MEAT_DARK)
    for (bx, by, r) in ((40, -8, 3), (55, 6, 2.6), (47, 12, 2), (60, -9, 2.2)):
        c.arc(bx, by, r, 0, 2 * math.pi); c.fill()
    c.set_source_rgba(1, 0.92, 0.75, 0.7)
    c.save(); c.translate(44, -12); c.rotate(-0.15); c.scale(12, 3.5); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
    c.set_source_rgb(*MEAT_IN); c.set_line_width(7)       # pale flesh along each bite edge
    for (bx, by, r) in holes:
        c.arc(bx, by, r, 0, 2 * math.pi); c.stroke()
    c.restore()
    c.set_source_rgb(*INK); c.set_line_width(2.2); c.set_line_join(1)
    c.save(); outside_holes(); poly(); c.stroke(); c.restore()
    c.save(); poly(); c.clip()
    for (bx, by, r) in holes:
        c.arc(bx, by, r, 0, 2 * math.pi); c.set_line_width(2); c.stroke()
    c.restore()
    # paper frill on the bone end
    c.set_source_rgb(1, 1, 1)
    c.move_to(-2, -9)
    for i in range(7):
        c.line_to(-2 + (i % 2) * 7, -9 + i * 3)
    c.line_to(8, 9); c.line_to(8, -9); c.close_path(); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(1.6); c.stroke()
    c.restore()


def don(k, x, feet, s=1.0, pose="stand", face="neutral", look=(0, 0), seed=500, badge=True, stain=True,
        gravy=True, leg=None):
    """leg: None, or (bites, angle_deg, hand[, scale]) with hand 0 = left, 1 = right. Returns kit.person's dict."""
    c = k.c
    old_p = dict(kit.PEOPLE["DON"])
    old_hook, old_face = kit.BADGE_HOOK, kit.face_draw
    kit.face_draw = _faces(old_face)
    p = dict(old_p); p["body"] = dv.SHIRT; p.pop("tie", None)
    kit.PEOPLE["DON"] = p
    kit.BADGE_HOOK = _costume(stain, badge, gravy)
    try:
        if not isinstance(pose, str):
            kit.ARM_POSES["_tg"] = pose
            pose = "_tg"
        out = kit.person(k, "DON", x, feet, s, pose=pose, face=face, seed=seed, look=look, badge=True)
    finally:
        kit.ARM_POSES.pop("_tg", None)
        kit.PEOPLE["DON"] = old_p
        kit.BADGE_HOOK, kit.face_draw = old_hook, old_face
    if leg is not None:
        bites, ang, hand = leg[:3]
        ls = leg[3] if len(leg) > 3 else 1.0              # finale: the leg is cheated bigger to cover the word
        hx, hy = out["hands"][hand]
        turkey_leg(k, hx, hy, s * ls, ang, bites, seed + 40)
        ellipse(k, hx, hy, 10.5 * s, 10.5 * s, SKIN, seed + 41, shadow=False, lw=2 * s)    # fist over the bone
        c.set_source_rgb(*INK); c.set_line_width(1.4 * s)
        for d in (-3, 3):
            c.move_to(hx - 6 * s, hy + d * s); c.line_to(hx + 2 * s, hy + d * s); c.stroke()
    return out


def tapping_finger(k, hand, s=1.0, ang=0.4, seed=560):
    """Index finger out from the hand point, toward the form."""
    c = k.c
    hx, hy = hand
    fx, fy = hx + math.sin(ang) * 18 * s, hy + math.cos(ang) * 18 * s
    c.set_line_cap(1)
    c.set_source_rgb(*INK); c.set_line_width(9 * s); c.move_to(hx, hy); c.line_to(fx, fy); c.stroke()
    c.set_source_rgb(*SKIN); c.set_line_width(5.6 * s); c.move_to(hx, hy); c.line_to(fx, fy); c.stroke()
