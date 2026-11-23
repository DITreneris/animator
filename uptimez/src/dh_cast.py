"""The new people of "Daddy's Home" (episode 12): FATHER, his BODYGUARD (one design, mirrored for the second) and the
coffee-machine REPAIRMAN. Nothing here changes an older module.
- father(): Don's own rig (kit.person: the same round head, the same skin, the same build), aged and hard. Slicked
  grey hair with a widow's peak, heavy level brows, half-closed eyes, a short level mouth, two lines by the nose.
  A burgundy velvet jacket, black shirt open at the neck, a gold chain, a gold ring. No badge. He has one face.
- guard(): the Client's rig (a big man: barrel chest, thick neck), in a black suit, white shirt, black tie, sunglasses,
  an earpiece with its coil, cropped hair. flip=True mirrors him.
- repairman(): the same rig and the same black shape at a glance (a black service jacket, zipped), so the office can
  take him for one of them. Up close: no sunglasses, a moustache, a lanyard, a coffee-cup patch, a metal case with
  the same cup on it.
  python3 dh_cast.py sheet  -> ../daddys-home/dh_cast_v1.png (the line-up with Don and the Client, canon scales)"""
import math
import sys
import cairo
import kit
import client_ob as co
import don_v4 as dv
from kit import Ctx, INK, cut, rect, ellipse
from cand_bc import limb, ik, _d

VELVET, VELVET_D, VELVET_L = (0.45, 0.07, 0.15), (0.31, 0.04, 0.10), (0.58, 0.13, 0.22)
BLACK, BLACK_L = (0.11, 0.11, 0.13), (0.20, 0.20, 0.23)
GOLD, GOLD_D = (0.90, 0.72, 0.26), (0.62, 0.46, 0.12)
GREY_HAIR, GREY_HAIR_L = (0.62, 0.62, 0.64), (0.82, 0.82, 0.84)
SKIN_F = (0.93, 0.76, 0.65)                                # Don's skin, a shade greyer
SUIT, SUIT_L = (0.10, 0.10, 0.12), (0.19, 0.19, 0.22)
STEEL, STEEL_D = (0.78, 0.80, 0.84), (0.55, 0.57, 0.62)
CUP = (0.93, 0.90, 0.82)


BROW_UP = [9]; BROW_DARK = [False]                                  # how far "brow" lifts; episode 13 raises it for one shot (default unchanged)


def _father_face(k, x, y, face, look, glasses=False, seed=0):
    """v2 (21 Nov, after the design review): he does less. Half-closed lids, grey brows level (not pressed into a
    frown), a short flat mouth. face: "hard", "talk" (the mouth opens a little), "brow" (his left brow goes up: the only
    move his face makes)."""
    c = k.c
    lx, ly = look
    low = face == "low"                                     # v4: chin down: the features sit lower, the eyes come up under the brows
    if low:
        y += 6; ly = -1.0
    for sx in (-17, 17):
        ellipse(k, x + sx, y, 10, 8.5, (1, 1, 1), seed + sx, shadow=False, lw=2)
        ellipse(k, x + sx + lx * 4, y + 1.5 + ly * 3, 4.3, 4.3, INK, seed + sx + 1, shadow=False, outline=False)
        c.set_source_rgb(*SKIN_F)                           # the upper lid, half down
        c.rectangle(x + sx - 12, y - 11, 24, 9.5 if not low else 7.5); c.fill()
        c.set_source_rgb(*INK); c.set_line_width(2.8); c.set_line_cap(1)
        c.move_to(x + sx - 10.5, y - 1.5); c.line_to(x + sx + 10.5, y - 1.5); c.stroke()
        c.set_source_rgba(0.45, 0.30, 0.28, 0.5); c.set_line_width(1.8)         # a bag under each eye
        c.move_to(x + sx - 8, y + 11); c.curve_to(x + sx - 3, y + 14, x + sx + 3, y + 14, x + sx + 8, y + 11); c.stroke()
    up = BROW_UP[0] if face == "brow" else 0
    bd = 2.5 if low else 0.0                                                   # low: the brows press down over the eyes
    for sx, lift in ((-1, 0), (1, up)):                                         # brows: grey, thick, level
        c.set_source_rgb(*((0.36, 0.36, 0.38) if lift and BROW_DARK[0] else GREY_HAIR)); c.set_line_width(7); c.set_line_cap(1)
        c.move_to(x + sx * 28, y - 12 + bd * 0.4 - lift * 0.6); c.line_to(x + sx * 7, y - 12 + bd - lift); c.stroke()
        c.set_source_rgb(*INK); c.set_line_width(1.6)
        c.move_to(x + sx * 28, y - 8.5 - lift * 0.6); c.line_to(x + sx * 7, y - 8.5 - lift); c.stroke()
    c.set_source_rgba(0.45, 0.30, 0.28, 0.8); c.set_line_width(2.0)             # the lines from the nose to the mouth
    for sx in (-1, 1):
        c.move_to(x + sx * 9, y + 13); c.curve_to(x + sx * 15, y + 19, x + sx * 17, y + 25, x + sx * 16, y + 31); c.stroke()
    if up:                                                                     # the forehead, on that side only
        c.move_to(x + 6, y - 27); c.curve_to(x + 13, y - 30, x + 21, y - 30, x + 28, y - 26); c.stroke()
    c.set_source_rgb(*INK); c.set_line_width(4)
    my = y + 28
    if face == "talk":
        ellipse(k, x, my, 7, 3.6, (0.35, 0.08, 0.08), seed + 5, shadow=False, lw=2)
    else:
        c.move_to(x - 10, my); c.line_to(x + 10, my); c.stroke()


def _father_costume(k, name, p, body_top, seed):
    c = k.c
    bt = body_top
    waist = bt + 150
    cut(k, [(-45, waist), (45, waist), (47, 0), (-47, 0)], BLACK, shadow=False, lw=2)       # black trousers, a crease
    c.set_source_rgb(*BLACK_L); c.set_line_width(1.6)
    c.move_to(0, waist + 14); c.line_to(0, -4); c.stroke()
    for sx in (-1, 1):                                                                      # good shoes, shined
        ellipse(k, sx * 24, -4, 24, 8, (0.06, 0.06, 0.07), seed + 80 + sx, shadow=False, lw=2)
        c.set_source_rgba(1, 1, 1, 0.5); c.arc(sx * 30, -7, 2.4, 0, 2 * math.pi); c.fill()
    cut(k, [(-20, bt), (20, bt), (16, waist), (-16, waist)], BLACK, shadow=False, lw=1.6)   # the black shirt
    cut(k, [(0, bt + 40), (-13, bt - 2), (13, bt - 2)], SKIN_F, shadow=False, lw=1.6)       # open at the neck
    for sx in (-1, 1):
        cut(k, [(sx * 12, bt - 4), (sx * 27, bt + 2), (sx * 20, bt + 22), (sx * 3, bt + 34)], BLACK_L, shadow=False, lw=1.6)
    c.set_source_rgb(*GOLD_D); c.set_line_width(4.4); c.set_line_cap(1)                     # the chain
    c.move_to(-11, bt + 2); c.curve_to(-8, bt + 26, 8, bt + 26, 11, bt + 2); c.stroke()
    c.set_source_rgb(*GOLD); c.set_line_width(2.6); c.set_dash([3.2, 2.2])
    c.move_to(-11, bt + 2); c.curve_to(-8, bt + 26, 8, bt + 26, 11, bt + 2); c.stroke(); c.set_dash([])
    for sx in (-1, 1):                                                                      # the velvet jacket, open
        cut(k, [(sx * 13, bt + 6), (sx * 46, bt - 2), (sx * 50, waist + 8), (sx * 12, waist + 8)], VELVET, shadow=False, lw=2.2)
        cut(k, [(sx * 13, bt + 6), (sx * 34, bt - 4), (sx * 36, bt + 46), (sx * 13, bt + 96)], VELVET_D, shadow=False, lw=1.8)   # a shawl lapel
        c.set_source_rgba(*VELVET_L, 0.9); c.set_line_width(3.2); c.set_line_cap(1)         # the nap catching the light
        c.move_to(sx * 44, bt + 30); c.curve_to(sx * 46, bt + 70, sx * 44, bt + 110, sx * 46, waist - 4); c.stroke()
    ellipse(k, 9, bt + 112, 4, 4, GOLD, seed + 85, shadow=False, lw=1.4)                    # one gold button
    cut(k, [(-40, bt + 44), (-27, bt + 42), (-28, bt + 52), (-39, bt + 53)], BLACK, shadow=False, lw=1.4)   # a black pocket square


def father(k, x, feet, s=1.0, pose="stand", face="hard", look=(0, 0), seed=1500):
    """Returns {"head", "hands"} in canvas coordinates. pose: a kit.ARM_POSES name or four angles. face: "hard", "talk"."""
    old_hook, old_face = kit.BADGE_HOOK, kit.face_draw
    kit.PEOPLE["FATHER"] = dict(skin=SKIN_F, body=VELVET, hair=SKIN_F, bald=True, h=1.12)
    kit.BADGE_HOOK = _father_costume
    kit.face_draw = _father_face
    tmp = None
    if not isinstance(pose, str):
        tmp = "_dh"; kit.ARM_POSES[tmp] = pose
    try:
        o = kit.person(k, "FATHER", x, feet, s, pose=tmp or pose, face=face, seed=seed, look=look, badge=True)
    finally:
        kit.BADGE_HOOK, kit.face_draw = old_hook, old_face
        del kit.PEOPLE["FATHER"]
        if tmp:
            del kit.ARM_POSES[tmp]
    c = k.c
    hx, hy = o["head"]
    c.save(); c.translate(hx, hy); c.scale(s, s)
    # v3: Don's side tufts are drawn in skin (see PEOPLE below): they are his ears, and the hair comes down to them
    top = [(55 * math.cos(math.radians(a_)), -8 - 49 * math.sin(math.radians(a_))) for a_ in range(0, 181, 15)]
    cut(k, [(45, 2)] + top + [(-45, 2), (-41, -10), (-40, -24), (-24, -34), (0, -25), (24, -34), (40, -24), (41, -10)],
        GREY_HAIR, shadow=False, lw=2)                                                       # one piece: slicked back, the temples run into it
    c.set_source_rgba(*GREY_HAIR_L, 0.95); c.set_line_width(2.2); c.set_line_cap(1)           # the comb's lines, wet
    for dx in (-30, -15, 0, 15, 30):
        c.move_to(dx * 0.95, -33 + (5 if dx == 0 else 0)); c.curve_to(dx, -40, dx * 0.9, -46, dx * 0.8, -49); c.stroke()
    for sx in (-1, 1):                                                                       # sideburns
        pass
    c.restore()
    for i, (qx, qy) in enumerate(o["hands"]):                                                # the ring, on his right hand
        if i == 1:
            c.save(); c.translate(qx, qy); c.scale(s, s)
            rect(k, -3.5, 5, 7, 13, SKIN_F, seed + 94, shadow=False, lw=1.5)                 # v3: one finger, and the ring on it
            rect(k, -5.5, 9, 11, 4, GOLD, seed + 95, shadow=False, lw=1.2)
            rect(k, -4, 6.5, 8, 7, (0.62, 0.05, 0.12), seed + 96, shadow=False, lw=1.2)
            c.restore()
    return o


def ring(k, x, y, s=1.0, seed=1595):
    """v2: big enough to know him by in the booth, where it is all we see of him. A gold band and a square red stone."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    rect(k, -12, -2, 24, 9, GOLD, seed, shadow=False, lw=1.6)
    rect(k, -7.5, -8, 15, 14, (0.62, 0.05, 0.12), seed + 1, shadow=False, lw=1.5)
    c.set_source_rgba(1, 1, 1, 0.75); c.rectangle(-5, -6, 4, 3); c.fill()
    c.restore()


def cup_logo(c, x, y, r, col=CUP):
    """A plain cup with steam: nobody's brand."""
    c.save(); c.translate(x, y); c.scale(r / 10.0, r / 10.0)
    c.set_source_rgb(*col); c.set_line_width(2.2); c.set_line_cap(1)
    c.move_to(-7, -2); c.line_to(-5.5, 8); c.line_to(5.5, 8); c.line_to(7, -2); c.close_path(); c.fill()
    c.arc(8.5, 2.5, 3.4, -1.3, 1.5); c.stroke()
    for dx in (-3, 2):
        c.move_to(dx, -5); c.curve_to(dx + 3, -8, dx - 2, -10, dx + 1, -13); c.stroke()
    c.restore()


def tool_case(k, x, y, s=1.0, seed=1700, open_=False):
    """The metal case, by its handle at (x, y): ribbed aluminium, two latches, the cup on its side."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    c.set_source_rgb(*INK); c.set_line_width(5); c.set_line_cap(1)
    c.move_to(-16, 14); c.curve_to(-16, -4, 16, -4, 16, 14); c.stroke()
    rect(k, -52, 12, 104, 66, STEEL, seed, lw=2.4)
    c.set_source_rgb(*STEEL_D); c.set_line_width(2)
    for yy in (26, 40, 54, 66):
        for x0, x1 in ((-48, -28), (28, 48)):
            c.move_to(x0, yy); c.line_to(x1, yy); c.stroke()
    for sx in (-1, 1):
        rect(k, sx * 34 - 6, 8, 12, 12, (0.30, 0.31, 0.35), seed + 2 + sx, shadow=False, lw=1.5)
    ellipse(k, 0, 45, 25, 25, (0.16, 0.16, 0.19), seed + 5, shadow=False, lw=1.8)             # v3: half as big again
    cup_logo(c, -1.5, 46, 13.5)
    c.restore()


PATCH = [False]                                            # v2: the cup is on the case only, where Pam alone sees it


def brush(k, x, y, s=1.0, ang=0.0, seed=1760):
    """The descaling brush: a twist of wire, a tuft, an orange grip. Five centimetres of it."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    c.set_source_rgb(*STEEL_D); c.set_line_width(2.4); c.set_line_cap(1)
    c.move_to(-4, 0); c.line_to(14, 0); c.stroke()
    rect(k, -20, -3.5, 17, 7, (0.95, 0.52, 0.12), seed, shadow=False, lw=1.4)
    c.set_source_rgb(*INK); c.set_line_width(1.2)
    for i in range(7):
        xx = 13 + i * 2.2
        c.move_to(xx, -5.5); c.line_to(xx, 5.5); c.stroke()
    c.restore()


def case_open(k, x, y, s=1.0, seed=1740, lid=1.0, brush_in=True):
    """The case on the counter, open towards us: the lid up behind, grey foam, and one small brush in a cut-out made for
    something far bigger. (x, y) is the middle of its front edge. lid 0..1 raises the lid."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    h = 70 * lid
    cut(k, [(-56, -38), (56, -38), (52, -38 - h), (-52, -38 - h)], STEEL, lw=2.4)             # the lid, standing
    c.set_source_rgb(*STEEL_D); c.set_line_width(2)
    for i in range(1, 5):
        yy = -38 - h * i / 5.0
        c.move_to(-50, yy); c.line_to(50, yy); c.stroke()
    cut(k, [(-60, 0), (60, 0), (56, -38), (-56, -38)], (0.90, 0.89, 0.84), lw=2.4)            # v3: pale foam, quite empty
    if brush_in:
        brush(k, 2, -19, 1.25, 0.0, seed + 3)
    rect(k, -60, 0, 120, 16, STEEL, seed + 1, shadow=False, lw=2.2)                          # the front wall
    for sx in (-1, 1):
        rect(k, sx * 36 - 6, 2, 12, 9, (0.30, 0.31, 0.35), seed + 5 + sx, shadow=False, lw=1.4)
    ellipse(k, 0, 8, 7.5, 7.5, (0.16, 0.16, 0.19), seed + 8, shadow=False, lw=1.2)
    cup_logo(c, -0.5, 8, 4.2)
    c.restore()


def pass_card(k, x, y, s=1.0, seed=1780):
    """His pass as Pam's insert shows it (5.4): the cup, COFFEE SERVICE. On the figure it is too small to read."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    c.set_source_rgb(0.20, 0.52, 0.80); c.set_line_width(5); c.set_line_cap(1)
    c.move_to(-16, -70); c.line_to(0, -30); c.line_to(16, -70); c.stroke()
    rect(k, -40, -32, 80, 104, (0.97, 0.97, 0.94), seed, lw=2.2)
    ellipse(k, 0, 0, 20, 20, (0.16, 0.16, 0.19), seed + 1, shadow=False, lw=1.6)
    cup_logo(c, -1, 1, 11)
    kit.text(k, "COFFEE", 0, 38, 17, INK); kit.text(k, "SERVICE", 0, 57, 17, INK)
    c.restore()


def _heavy(k, x, feet, s, kind, pose, look, seed, flip, mouth, case):
    c = k.c
    BT, HIP, HY, SH, LN1, LN2 = co.BT, co.HIP, co.HY, co.SH, co.LN1, co.LN2
    a = pose
    J = SUIT
    c.save(); c.translate(x, feet); c.scale(-s if flip else s, s)
    for sx, w in ((-30, 28), (34, 29)):                                                     # black shoes, feet apart
        ellipse(k, sx, -5, w, 9.5, (0.05, 0.05, 0.06), seed + 1 + sx, lw=2)
    cut(k, [(-2, HIP - 4), (-56, HIP - 4), (-52, -10), (-10, -10)], SUIT, shadow=False, lw=2)
    cut(k, [(2, HIP - 4), (56, HIP - 4), (56, -10), (14, -10)], SUIT, shadow=False, lw=2)
    c.set_source_rgb(*SUIT_L); c.set_line_width(1.6)
    c.move_to(-32, HIP + 24); c.line_to(-31, -14); c.stroke(); c.move_to(34, HIP + 24); c.line_to(35, -14); c.stroke()
    bt = BT
    rect(k, -27, bt - 22, 54, 30, co.SKIN, seed + 5, shadow=False, lw=2)                    # the neck
    if kind == "guard":
        cut(k, [(-68, bt + 6), (-30, bt - 10), (30, bt - 10), (68, bt + 6), (76, bt + 70), (66, HIP + 26), (-66, HIP + 26),
                (-76, bt + 70)], J, lw=2.4)                                                  # the suit, buttoned
        cut(k, [(0, bt + 92), (-22, bt - 9), (22, bt - 9)], co.SHIRT, shadow=False, lw=1.6)  # a white V
        cut(k, [(0, bt - 2), (-6, bt + 8), (-4, bt + 84), (0, bt + 92), (4, bt + 84), (6, bt + 8)], (0.04, 0.04, 0.05),
            shadow=False, lw=1.4)                                                            # the black tie
        for sx in (-1, 1):
            cut(k, [(sx * 22, bt - 10), (sx * 40, bt - 8), (sx * 30, bt + 48), (sx * 2, bt + 92)], SUIT_L, shadow=False, lw=1.8)
        ellipse(k, 0, bt + 108, 3.4, 3.4, (0.30, 0.30, 0.33), seed + 44, shadow=False, lw=1.2)
    else:
        cut(k, [(-68, bt + 6), (-30, bt - 10), (30, bt - 10), (68, bt + 6), (76, bt + 70), (68, HIP + 18), (-68, HIP + 18),
                (-76, bt + 70)], J, lw=2.4)                                                  # the service jacket, zipped
        for sx in (-1, 1):                                                                   # a stand collar
            cut(k, [(sx * 2, bt + 6), (sx * 4, bt - 14), (sx * 30, bt - 16), (sx * 33, bt + 2)], SUIT_L, shadow=False, lw=1.8)
        c.set_source_rgb(0.60, 0.62, 0.66); c.set_line_width(3); c.set_line_cap(1)
        c.move_to(0, bt - 6); c.line_to(0, HIP + 16); c.stroke()
        rect(k, -66, HIP + 8, 132, 11, SUIT_L, seed + 46, shadow=False, lw=1.6)              # the knitted hem
        if PATCH[0]:                                                                         # v1 only: the chest patch
            rect(k, 22, bt + 34, 34, 26, (0.16, 0.16, 0.19), seed + 47, shadow=False, lw=1.6)
            cup_logo(c, 38, bt + 48, 8)
        c.set_source_rgb(0.20, 0.52, 0.80); c.set_line_width(3.2)                            # a lanyard and his pass
        c.move_to(-21, bt - 8); c.line_to(-12, bt + 70); c.line_to(-3, bt - 8); c.stroke()
        rect(k, -24, bt + 68, 24, 31, (0.97, 0.97, 0.94), seed + 48, shadow=False, lw=1.6)
        c.set_source_rgb(*INK); c.set_line_width(1.5)
        for yy in (bt + 84, bt + 90):
            c.move_to(-20, yy); c.line_to(-4, yy); c.stroke()
        ellipse(k, -12, bt + 77, 4, 4, co.SKIN, seed + 49, shadow=False, lw=1.2)
    hands = []
    for side, (u, f_) in ((-1, (a[0], a[1])), (1, (a[2], a[3]))):
        sy_ = bt + 26; sx_ = side * SH[0]
        hx, hy_ = limb(k, sx_, sy_, u, f_, LN1, LN2, 47, 39, J, J, co.SKIN, co.HAND, seed + 10 + side)
        ellipse(k, side * (SH[0] - 1), sy_ - 1, 23, 20, J, seed + 14 + side, shadow=False, lw=2)
        c.set_source_rgb(*J); c.rectangle(min(side * 60, side * 86), sy_ - 12, 26, 32); c.fill()
        if kind == "guard":                                                                  # a white cuff
            ex, ey = sx_ + _d(u)[0] * LN1, sy_ + _d(u)[1] * LN1
            ux, uy = (hx - ex) / LN2, (hy_ - ey) / LN2; px, py = -uy, ux
            wx, wy = hx - ux * (co.HAND + 1), hy_ - uy * (co.HAND + 1)
            cut(k, [(wx + px * 19 - ux * 6, wy + py * 19 - uy * 6), (wx + px * 18, wy + py * 18), (wx - px * 18, wy - py * 18),
                    (wx - px * 19 - ux * 6, wy - py * 19 - uy * 6)], co.SHIRT, shadow=False, lw=1.8)
        if kind == "guard" and side == 1:                                                    # v3: the gripping hand has fingers
            c.set_source_rgb(*INK); c.set_line_width(1.8); c.set_line_cap(1)
            for i in (-1, 0, 1):
                c.move_to(hx - 16, hy_ + i * 8 + 1); c.line_to(hx + 2, hy_ + i * 8 + 3); c.stroke()
        hands.append((hx, hy_))
    if case:
        tool_case(k, hands[0][0], hands[0][1] + 4, 1.0, seed + 60)
    hy = HY
    c.save(); c.translate(0, hy + 55); c.scale(co.HEAD, co.HEAD); c.translate(0, -(hy + 55))
    pts = co._head_pts(k, hy, seed + 20)
    for sx in (-1, 1):
        ellipse(k, sx * 48, hy + 2, 7.5, 12, co.SKIN, seed + 26 + sx, shadow=False, lw=2)
    cut(k, pts, co.SKIN)
    hair = (0.13, 0.11, 0.10) if kind == "guard" else (0.36, 0.27, 0.20)
    cut(k, [(-47, hy - 4), (-49, hy - 30), (-38, hy - 52), (-10, hy - 62), (22, hy - 60), (44, hy - 46), (49, hy - 26),
            (47, hy - 4), (42, hy - 24), (26, hy - 38), (0, hy - 41), (-26, hy - 38), (-42, hy - 24)], hair, shadow=False, lw=2)
    if kind == "guard":
        co._face(k, hy + 4, "plain", (0, 0), mouth, seed + 30, "none")
        for sx in (-1, 1):                                                                   # the sunglasses
            cut(k, [(sx * 4, hy - 12), (sx * 38, hy - 13), (sx * 36, hy + 8), (sx * 20, hy + 13), (sx * 6, hy + 8)],
                (0.03, 0.03, 0.04), shadow=False, lw=2)
            c.set_source_rgba(1, 1, 1, 0.42); c.set_line_width(3); c.set_line_cap(1)
            c.move_to(sx * 12 + 6, hy - 8); c.line_to(sx * 12 + 16, hy - 8); c.stroke()
        c.set_source_rgb(0.03, 0.03, 0.04); c.set_line_width(4)
        c.move_to(-6, hy - 9); c.line_to(6, hy - 9); c.stroke()
        c.move_to(-37, hy - 9); c.line_to(-49, hy - 6); c.stroke(); c.move_to(37, hy - 9); c.line_to(49, hy - 6); c.stroke()
        c.set_source_rgb(0.92, 0.92, 0.90); c.set_line_width(2.4)                            # the earpiece: a coil down the neck
        c.move_to(51, hy + 4)
        for i in range(7):
            yy = hy + 10 + i * 8
            c.curve_to(58, yy, 44, yy + 4, 51, yy + 8)
        c.stroke()
        ellipse(k, 50, hy + 2, 4.5, 5.5, (0.92, 0.92, 0.90), seed + 33, shadow=False, lw=1.4)
    else:
        co._face(k, hy + 4, "plain", look, mouth, seed + 30, "none")
        cut(k, [(-24, hy + 22), (-12, hy + 17), (0, hy + 20), (12, hy + 17), (24, hy + 22), (22, hy + 30), (8, hy + 26),
                (0, hy + 28), (-8, hy + 26), (-22, hy + 30)], hair, shadow=False, lw=1.6)   # a moustache
    c.restore()
    c.restore()
    m = -1 if flip else 1
    return {"head": (x, feet + hy * s), "hands": [(x + m * hx * s, feet + hy_ * s) for hx, hy_ in hands],
            "top": feet + co.TOP * s}


GUARD_POSE_V2 = ik(-co.SH[0], co.BT + 26, 4, co.HIP + 6, co.LN1, co.LN2, -1) + ik(co.SH[0], co.BT + 26, -4, co.HIP + 22, co.LN1, co.LN2, 1)
# v3: the left fist hangs low in the middle; the right hand lies across its wrist, higher and to the side
GUARD_POSE = ik(-co.SH[0], co.BT + 26, 14, co.HIP + 34, co.LN1, co.LN2, -1) + ik(co.SH[0], co.BT + 26, -16, co.HIP + 2, co.LN1, co.LN2, 1)
WORK_POSE = (-6, 3, 8, -4)


def guard(k, x, feet, s=1.0, pose=None, flip=False, seed=1600, mouth=None):
    """Hands folded in front, feet apart. flip=True is the second one."""
    return _heavy(k, x, feet, s, "guard", pose or GUARD_POSE, (0, 0), seed, flip, mouth, False)


def repairman(k, x, feet, s=1.0, pose=None, look=(0, 0), seed=1650, mouth=None, case=True, flip=False):
    return _heavy(k, x, feet, s, "repair", pose or WORK_POSE, look, seed, flip, mouth, case)


def sheet(out="../daddys-home/dh_cast_v3.png"):
    Wd, Hd, Z = 1760, 1180, 2.0
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, Wd, Hd); c = cairo.Context(surf)
    c.set_source_rgb(*kit.WALL); c.paint()
    c.set_source_rgb(*kit.FLOOR); c.rectangle(0, 1060, Wd, 120); c.fill()
    k = Ctx(c, 0)
    F = 1080
    kit.text(k, "DADDY'S HOME · THE NEW PEOPLE · v3", Wd / 2, 44, 34, INK)
    kit.text(k, "canon scales, on one floor · the entrance: the two part, and he is between them", Wd / 2, 80, 19, INK, font=kit.MONO)
    dv.don(k, 150, F, 0.60 * Z, "stand", "neutral", look=(1, 0))
    guard(k, 500, F, 0.56 * Z)
    father(k, 760, F, 0.62 * Z, look=(-1, 0))
    guard(k, 1020, F, 0.56 * Z, flip=True)
    repairman(k, 1420, F, 0.56 * Z)
    for name, note, x in (("DON", "0.60 · unchanged", 150), ("BODYGUARD", "one hand on the other wrist", 500),
                          ("FATHER", "0.62 · temples run into the hair", 760), ("BODYGUARD (mirrored)", "a beat late", 1020),
                          ("REPAIRMAN", "the cup, bigger, on the case", 1420)):
        kit.text(k, name, x, 1120, 24, INK); kit.text(k, note, x, 1148, 15, INK, font=kit.MONO)

    def panel(x, y, w, h, title):
        rect(k, x, y, w, h, (0.97, 0.94, 0.86), 1900 + int(x), lw=2.2)
        kit.text(k, title, x + w / 2, y + h + 22, 16, INK, font=kit.MONO)
    panel(40, 120, 240, 250, "his face: \"hard\"")
    c.save(); c.rectangle(44, 124, 232, 242); c.clip(); father(k, 160, 820, 1.9, look=(0, 0)); c.restore()
    panel(310, 120, 240, 250, "\"brow\": his only move")
    c.save(); c.rectangle(314, 124, 232, 242); c.clip(); father(k, 430, 820, 1.9, face="brow", look=(0, 0)); c.restore()
    panel(580, 120, 240, 250, "the ring, on one finger")
    c.save(); c.rectangle(584, 124, 232, 242); c.clip()
    c.set_source_rgb(0.20, 0.04, 0.07); c.paint()
    cut(k, [(584, 250), (680, 216), (690, 300), (584, 330)], VELVET, shadow=False, lw=2.4)
    cut(k, [(668, 222), (702, 212), (712, 290), (678, 302)], (0.96, 0.96, 0.93), shadow=False, lw=2.2)
    ellipse(k, 738, 250, 40, 36, SKIN_F, 1930, shadow=False, lw=2.4)
    for i, ln in enumerate((40, 46, 44, 36)):                                                # four fingers, pointing down
        rect(k, 708 + i * 17, 268, 15, ln, SKIN_F, 1931 + i, shadow=False, lw=2)
    rect(k, 739, 286, 21, 9, GOLD, 1940, shadow=False, lw=1.6)                               # the band, round the third
    rect(k, 739.5, 277, 20, 17, (0.62, 0.05, 0.12), 1941, shadow=False, lw=1.6)
    c.set_source_rgba(1, 1, 1, 0.75); c.rectangle(743, 280, 5, 4); c.fill()
    c.restore()
    panel(850, 120, 300, 250, "7.1b: the case. One brush")
    case_open(k, 1000, 335, 1.75)
    panel(1180, 120, 250, 250, "7.1c: in two fingers")
    ellipse(k, 1275, 262, 48, 42, co.SKIN, 1950, shadow=False, lw=2.4)
    brush(k, 1344, 232, 3.0, -0.5, 1955)
    ellipse(k, 1312, 228, 16, 12, co.SKIN, 1951, shadow=False, lw=2.2); ellipse(k, 1320, 249, 16, 12, co.SKIN, 1952, shadow=False, lw=2.2)
    panel(1460, 120, 260, 250, "5.4: what Pam sees")
    c.save(); c.rectangle(1464, 124, 252, 242); c.clip()
    c.set_source_rgb(*SUIT); c.paint()
    pass_card(k, 1530, 240, 1.25)
    tool_case(k, 1670, 250, 1.5)
    c.restore()
    surf.write_to_png(out); print("wrote", out)


if __name__ == "__main__":
    sheet()
