"""PINNED v1 (19 Nov): sheet v1 is drawn from this file. client_on3.py is v2.
THE CLIENT, "Office Noir 3: The Last Round", v1: the boxer of his own dream.
His head is The Onboarding's (client_ob v3: the same face, hair, stubble and faces), drawn by client_ob itself and
kept; everything below the jaw is this film's:
- a RED HOODED ROBE, knee length, ivory shawl collar, ivory belt and cuffs; the garages' gear on the chest in ivory
  (a symbol, never words). Hood up on the street, down in the ring. He never takes it off;
- RED BOXING GLOVES, larger than his hands, an ivory laced cuff; he never takes them off either: no fingers;
- bare shins and black lace-up boxing boots.
The robe and the gloves are the film's red: sofia_on.HEART and one darker red for folds (ACCENTS keeps both).
Options: hood=True, tape=True (Pam's strip over his brow), cig=True (a cigarette in the corner of his mouth),
note=True (a banknote clamped between his two gloves), awake=True (the twin: a red dressing gown, bare hands, his
watch; no hood, no gloves, no gear).
Usage: o = boxer(k, x, feet, s, pose, face, look, mouth=None, hood=False, tape=False, cig=False, note=False)
Returns {"head", "hands", "top"} in canvas coordinates. Poses: "b_walk", "b_fist" (one glove raised: his finger),
"b_ask" (both gloves up, nothing he can do with them), "b_pay", "b_guard", "b_swing", "b_reach" (up, for the roll).
client_ob draws exactly as before; nothing in it is changed. Beside the series' other figures he is drawn at 0.70
of their scale, as in The Onboarding (his units are larger)."""
import math
import kit
import client_ob as co
import sofia_on as son
from kit import INK, cut, rect, ellipse
from cand_bc import limb, _d

KEY = son.HEART                                            # the one red
SHADE = (0.60, 0.07, 0.11)                                 # its folds (Office Noir 2's GOWN_SHADE)
ACCENTS = [(KEY, 1.0), (SHADE, 1.0)]
IVORY = (0.95, 0.93, 0.88)
IVORY_EDGE = (0.62, 0.60, 0.56)
BOOT = (0.07, 0.07, 0.08)
SOLE = (0.86, 0.84, 0.80)
GOWN = (0.62, 0.10, 0.14)                                  # awake: towelling, a duller red
GOWN_SHADE = (0.44, 0.06, 0.10)
NOTE = (0.90, 0.93, 0.86)
PAPER = (0.98, 0.97, 0.94)
BT, HIP, HY, SH, LN1, LN2 = co.BT, co.HIP, co.HY, co.SH, co.LN1, co.LN2
GLOVE = 33                                                 # his hand is 24
HEM = -74
REL = 0.70                                                 # his scale beside the series' other figures

_ik = co._ik
POSES = {
    "b_walk": (-9, 6, 9, -6),
    "b_fist": (-9, 6, 104, 76),                            # the upper arm out, the forearm straight up
    "b_ask": _ik(-1, -36, BT + 84) + _ik(1, 36, BT + 84),
    "b_pay": _ik(-1, -36, BT + 84) + _ik(1, 36, BT + 84),  # the same hold; the note is what differs
    "b_guard": (-40, -165, 40, 165),                       # elbows out, both gloves up beside his jaw
    "b_swing": (-9, 6, 96, -4),                        # one glove out, the whole arm behind it
    "b_reach": (-9, 6, 152, 24),                           # up, as far as the arm goes
}


def _head_xf(c, face):
    """The transform client_ob draws his head in (after translate, scale and the upper body's tilt)."""
    f = co.FACES[face]
    back = {"shock": (5, -6), "dawning": (2, -3)}.get(face, (0, 0))
    c.translate(back[0], HY + 55 + back[1]); c.rotate(f["tilt"] - co.TILT * 0.6); c.scale(co.HEAD, co.HEAD)
    c.translate(0, -(HY + 55))


def _upper(c):
    c.translate(-4, HIP); c.rotate(co.TILT); c.translate(0, -HIP)


def _glove(k, hx, hy, ux, uy, side, seed, col=None, shade=None):
    """A boxing glove on the end of a sleeve: the mitt, the thumb toward the body, an ivory laced cuff."""
    c = k.c
    col, shade = col or KEY, shade or SHADE
    px, py = -uy, ux
    wx, wy = hx - ux * (GLOVE - 4), hy - uy * (GLOVE - 4)
    cut(k, [(wx + px * 24 - ux * 15, wy + py * 24 - uy * 15), (wx + px * 25, wy + py * 25), (wx - px * 25, wy - py * 25),
            (wx - px * 24 - ux * 15, wy - py * 24 - uy * 15)], IVORY, shadow=False, lw=2)
    c.set_source_rgb(*IVORY_EDGE); c.set_line_width(1.5)
    for t in (-0.5, 0.0, 0.5):                             # the laces
        qx, qy = wx + px * 20 * t - ux * 12, wy + py * 20 * t - uy * 12
        c.move_to(qx, qy); c.line_to(qx + ux * 9 + px * 5, qy + uy * 9 + py * 5); c.stroke()
    ellipse(k, hx + ux * 4, hy + uy * 4, GLOVE, GLOVE * 0.94, col, seed, shadow=False, lw=2.4)
    tx, ty = hx - px * side * 21 - ux * 6, hy - py * side * 21 - uy * 6      # the thumb, on the body's side
    c.save(); c.translate(tx, ty); c.rotate(math.atan2(uy, ux))
    ellipse(k, 0, 0, 17, 11.5, col, seed + 1, shadow=False, lw=2.2)
    c.restore()
    c.set_source_rgb(*shade); c.set_line_width(2.2); c.set_line_cap(1)        # the seam across the knuckles
    c.move_to(hx + ux * 16 + px * 18, hy + uy * 16 + py * 18)
    c.curve_to(hx + ux * 26 + px * 6, hy + uy * 26 + py * 6, hx + ux * 26 - px * 6, hy + uy * 26 - py * 6,
               hx + ux * 16 - px * 18, hy + uy * 16 - py * 18); c.stroke()
    c.set_source_rgba(1, 1, 1, 0.85); c.set_line_width(3.2)                  # leather: one highlight
    c.move_to(hx - ux * 6 + px * side * 19, hy - uy * 6 + py * side * 19)
    c.line_to(hx + ux * 8 + px * side * 21, hy + uy * 8 + py * side * 21); c.stroke()


def banknote(k, x, y, s=1.0, ang=0.0, seed=0):
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    cut(k, [(-34, -17), (34, -17), (34, 17), (-34, 17)], NOTE, lw=2)
    c.set_source_rgb(*INK); c.set_line_width(1.3); c.rectangle(-29, -12, 58, 24); c.stroke()
    kit.text(k, "100", 0, 0, 20, INK)
    c.restore()


def boxer(k, x, feet, s=1.0, pose="b_walk", face="confident", look=(0, 0), seed=900, mouth=None, hood=False,
          tape=False, cig=False, note=False, awake=False):
    c = k.c
    a = POSES[pose] if isinstance(pose, str) else pose
    R, RS = (GOWN, GOWN_SHADE) if awake else (KEY, SHADE)
    c.save(); c.translate(x, feet); c.scale(s, s)
    # shins and boots (awake: slippers)
    for (x0, x1, x2, x3) in ((-46, -12, -12, -44), (20, 54, 60, 28)):
        cut(k, [(x0, HEM - 6), (x1, HEM - 6), (x2, -38), (x3, -38)], co.SKIN, shadow=False, lw=2)
    if not awake:
        for cx, rx, (x0, x1, x2, x3) in ((-28, 27, (-47, -11, -10, -46)), (46, 31, (26, 60, 64, 28))):
            ellipse(k, cx, -3, rx, 7, SOLE, seed + 1 + cx, lw=2)
            ellipse(k, cx, -9, rx, 11, BOOT, seed + 2 + cx, shadow=False, lw=2)
            cut(k, [(x0, -54), (x1, -54), (x2, -12), (x3, -12)], BOOT, shadow=False, lw=2)          # the high shaft
            c.set_source_rgb(*IVORY); c.set_line_width(1.8); c.set_line_cap(1)
            mx = (x0 + x1) / 2
            for i in range(4):                                                                        # the laces
                c.move_to(mx - 8, -48 + i * 9); c.line_to(mx + 8, -44 + i * 9); c.stroke()
    else:
        for cx, rx, (x0, x1, x2, x3) in ((-28, 25, (-44, -12, -13, -43)), (46, 28, (28, 58, 61, 31))):
            cut(k, [(x0, -40), (x1, -40), (x2, -10), (x3, -10)], co.SKIN, shadow=False, lw=2)
            ellipse(k, cx, -7, rx, 10, (0.36, 0.26, 0.20), seed + 3 + cx, lw=2)                       # a slipper
    cut(k, [(-70, HIP - 12), (70, HIP - 12), (86, HEM + 2), (44, HEM + 6), (8, HEM), (-32, HEM + 6), (-78, HEM + 2)], R, lw=2.4)
    if not awake:                                          # an ivory band above the hem
        cut(k, [(-76, HEM - 20), (-32, HEM - 16), (8, HEM - 22), (44, HEM - 16), (84, HEM - 20), (83, HEM - 9), (44, HEM - 5),
                (8, HEM - 11), (-32, HEM - 5), (-75, HEM - 9)], IVORY, shadow=False, lw=1.6)
    c.set_source_rgb(*RS); c.set_line_width(2.4); c.set_line_cap(1)                               # the skirt's folds
    for x0, x1 in ((-46, -52), (-18, -22), (40, 50), (62, 72)):
        c.move_to(x0, HIP + 22); c.line_to(x1, HEM - 2); c.stroke()
    c.set_source_rgb(*INK); c.set_line_width(2.0); c.move_to(6, HIP); c.line_to(12, HEM + 1); c.stroke()   # the front edge
    _upper(c)
    bt = BT
    if hood:                                               # the hood, behind his head
        cut(k, [(-70, HY + 58), (-74, HY - 30), (-50, HY - 84), (0, HY - 100), (50, HY - 84), (74, HY - 30), (70, HY + 58)],
            R, lw=2.4)
    else:                                                  # the hood, down: a roll behind his neck
        cut(k, [(-78, bt + 14), (-66, bt - 34), (-30, bt - 50), (30, bt - 50), (66, bt - 34), (78, bt + 14)], R, lw=2.4)
        c.set_source_rgb(*RS); c.set_line_width(2.2)
        c.move_to(-58, bt - 26); c.curve_to(-30, bt - 38, 30, bt - 38, 58, bt - 26); c.stroke()
    rect(k, -27, bt - 22, 54, 30, co.SKIN, seed + 5, shadow=False, lw=2)                          # the neck
    cut(k, [(-98, bt + 32), (-82, bt + 3), (-38, bt - 9), (38, bt - 9), (82, bt + 3), (98, bt + 32), (94, bt + 96),
            (72, HIP + 4), (-72, HIP + 4), (-94, bt + 96)], R, lw=2.4)
    cut(k, [(0, bt + 86), (-25, bt - 9), (25, bt - 9)], co.SKIN, shadow=False, lw=1.8)             # his chest, in the V
    c.set_source_rgba(*co.HAIR, 0.55); c.set_line_width(1.5); c.set_line_cap(1)
    for dx, dy in ((-7, 22), (5, 26), (-2, 38), (8, 44), (-6, 52), (2, 62)):
        c.move_to(dx, bt + dy); c.curve_to(dx + 2, bt + dy - 4, dx + 5, bt + dy - 4, dx + 6, bt + dy + 1); c.stroke()
    for sx in (-1, 1):                                                                            # the shawl collar
        cut(k, [(sx * 23, bt - 11), (sx * 46, bt - 8), (sx * 16, bt + 78), (0, bt + 98), (0, bt + 80)], IVORY,
            shadow=False, lw=2)
    c.set_source_rgb(*RS); c.set_line_width(2.4)
    c.move_to(-60, bt + 50); c.curve_to(-52, bt + 80, -50, bt + 104, -54, HIP - 16); c.stroke()
    c.move_to(60, bt + 46); c.curve_to(54, bt + 80, 52, bt + 104, 56, HIP - 16); c.stroke()
    rect(k, -73, HIP - 15, 146, 17, IVORY, seed + 46, shadow=False, lw=1.8)                       # the belt, knotted
    for dx, ln in ((-8, 44), (9, 52)):
        cut(k, [(12, HIP - 6), (22, HIP - 6), (22 + dx + 6, HIP - 6 + ln), (22 + dx - 6, HIP - 8 + ln)], IVORY,
            shadow=False, lw=1.6)
    ellipse(k, 17, HIP - 6, 9.5, 9, IVORY, seed + 47, shadow=False, lw=1.8)
    if not awake:
        co.gear(k, 56, bt + 60, 16, col=IVORY, seed=seed + 42)
        c.set_source_rgba(1, 1, 1, 0.55); c.set_line_width(3.4); c.set_line_cap(1)                # satin: one long highlight
        c.move_to(-80, bt + 40); c.curve_to(-76, bt + 70, -74, bt + 96, -70, HIP - 22); c.stroke()                                  # the garages' mark
    hands = []
    for side, (u, f_) in ((-1, (a[0], a[1])), (1, (a[2], a[3]))):
        sy_ = bt + 26 + (5 if side < 0 else 0)
        sx_ = side * SH[0]
        ex, ey = sx_ + _d(u)[0] * LN1, sy_ + _d(u)[1] * LN1
        hx, hy_ = limb(k, sx_, sy_, u, f_, LN1, LN2, 50, 43, R, R, co.SKIN if awake else R, co.HAND if awake else 4,
                       seed + 10 + side)
        ellipse(k, side * (SH[0] - 1), sy_ - 1, 24, 21, R, seed + 14 + side, shadow=False, lw=2)   # the shoulder
        c.set_source_rgb(*R); c.rectangle(min(side * 60, side * 86), sy_ - 12, 26, 32); c.fill()
        ux, uy = (hx - ex) / LN2, (hy_ - ey) / LN2
        px, py = -uy, ux
        if awake:
            wx, wy = hx - ux * (co.HAND + 1), hy_ - uy * (co.HAND + 1)                           # a towelling cuff
            cut(k, [(wx + px * 23 - ux * 12, wy + py * 23 - uy * 12), (wx + px * 23, wy + py * 23),
                    (wx - px * 23, wy - py * 23), (wx - px * 23 - ux * 12, wy - py * 23 - uy * 12)], GOWN_SHADE,
                shadow=False, lw=1.8)
            if side == 1:                                                                        # the good watch
                bx, by_ = hx - ux * (co.HAND - 8), hy_ - uy * (co.HAND - 8)
                cut(k, [(bx + px * 17 - ux * 5, by_ + py * 17 - uy * 5), (bx + px * 17 + ux * 5, by_ + py * 17 + uy * 5),
                        (bx - px * 17 + ux * 5, by_ - py * 17 + uy * 5), (bx - px * 17 - ux * 5, by_ - py * 17 - uy * 5)],
                    co.STEEL, shadow=False, lw=1.4)
                ellipse(k, bx, by_, 10, 10, co.GOLD, seed + 18, shadow=False, lw=1.6)
                ellipse(k, bx, by_, 6.4, 6.4, (0.10, 0.16, 0.14), seed + 19, shadow=False, lw=1.0)
        else:
            _glove(k, hx, hy_, ux, uy, side, seed + 60 + side)
        hands.append((hx, hy_))
    if note and not awake:                                                                        # clamped between two gloves
        (lx, ly), (rx, ry) = hands
        banknote(k, (lx + rx) / 2 + 4, (ly + ry) / 2 - 30, 1.25, -0.08, seed + 80)
    c.restore()
    # his head: client_ob's own drawing, kept whole, clipped to the head
    c.save()
    c.save(); c.translate(x, feet); c.scale(s, s); _upper(c); _head_xf(c, face)
    pts = co._head_pts(k, HY, seed + 20)
    c.new_path()
    c.move_to(pts[0][0] * 1.04, HY + (pts[0][1] - HY) * 1.04)
    for qx, qy in pts[1:]:
        c.line_to(qx * 1.04, HY + (qy - HY) * 1.04)
    c.close_path()
    c.rectangle(-62, HY - 84, 124, 86)
    for sx in (-1, 1):
        c.save(); c.translate(sx * 48, HY + 2); c.scale(10, 15); c.new_sub_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
    c.restore()
    c.clip()
    co.client(k, x, feet, s, "open", face, look=look, seed=seed, mouth=mouth, roll=False, badge=False)
    c.restore()
    c.save(); c.translate(x, feet); c.scale(s, s); _upper(c)
    if hood:                                               # the hood's rim, in front of his hair and ears
        c.new_path()
        pts_o = [(-70, HY + 58), (-74, HY - 30), (-50, HY - 84), (0, HY - 100), (50, HY - 84), (74, HY - 30), (70, HY + 58)]
        c.move_to(*pts_o[0])
        for q in pts_o[1:]:
            c.line_to(*q)
        c.close_path()
        c.save(); c.translate(0, HY + 10); c.scale(45, 56); c.new_sub_path(); c.arc_negative(0, 0, 1, 2 * math.pi, 0); c.restore()
        c.set_source_rgb(*R); c.fill()
        c.set_source_rgb(*INK); c.set_line_width(2.4)
        c.save(); c.translate(0, HY + 10); c.scale(45, 56); c.new_sub_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.stroke()
        c.move_to(*pts_o[0])
        for q in pts_o[1:]:
            c.line_to(*q)
        c.stroke()
        c.set_source_rgb(*RS); c.set_line_width(2.2); c.set_line_cap(1)
        c.move_to(-56, HY - 40); c.curve_to(-40, HY - 74, 40, HY - 74, 56, HY - 40); c.stroke()
    c.save(); _head_xf(c, face)
    if tape:                                               # Pam's strip, over the nicked brow
        cut(k, [(8, HY - 34), (38, HY - 28), (36, HY - 16), (6, HY - 22)], PAPER, shadow=False, lw=1.6)
        c.set_source_rgb(*IVORY_EDGE); c.set_line_width(1.2)
        for t in (0.3, 0.7):
            c.move_to(8 + 30 * t, HY - 34 + 6 * t); c.line_to(6 + 30 * t, HY - 22 + 6 * t); c.stroke()
    if cig:                                                # in the corner of his mouth; he cannot hold it
        c.save(); c.translate(15, HY + 39); c.rotate(0.22)
        cut(k, [(0, -3), (30, -3), (30, 3), (0, 3)], PAPER, shadow=False, lw=1.4)
        c.set_source_rgb(0.55, 0.55, 0.57); c.rectangle(26, -3, 4, 6); c.fill()
        c.restore()
    c.restore()
    c.restore()
    top = feet + (HY - (100 if hood else 70)) * s
    return {"head": (x - 4 * s, feet + HY * s), "hands": [(x + (hx - 4) * s, feet + hy_ * s) for hx, hy_ in hands],
            "top": top}


def robot_glove(k, x, y, s=1.0, ang=math.pi, seed=950):
    """The other corner's glove, grey, on a steel piston: for frame 0. (x, y) is the middle of the mitt; ang is the
    way it travels (pi = from screen right to left)."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    ux, uy = math.cos(ang), math.sin(ang)
    px, py = -uy, ux
    bx, by = -ux * (GLOVE + 6), -uy * (GLOVE + 6)
    cut(k, [(bx + px * 11, by + py * 11), (bx - ux * 170 + px * 11, by - uy * 170 + py * 11),
            (bx - ux * 170 - px * 11, by - uy * 170 - py * 11), (bx - px * 11, by - py * 11)], (0.78, 0.80, 0.84), shadow=False, lw=2)
    cut(k, [(bx - ux * 40 + px * 17, by - uy * 40 + py * 17), (bx - ux * 170 + px * 17, by - uy * 170 + py * 17),
            (bx - ux * 170 - px * 17, by - uy * 170 - py * 17), (bx - ux * 40 - px * 17, by - uy * 40 - py * 17)],
        (0.52, 0.54, 0.60), shadow=False, lw=2)
    _glove(k, 0, 0, ux, uy, 1, seed, col=(0.36, 0.37, 0.40), shade=(0.18, 0.18, 0.20))
    c.restore()
