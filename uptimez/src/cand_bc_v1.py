"""v1, pinned (the current file is v2). THE BEST CANDIDATE, v1: the two new candidates. Both are drawn here from kit primitives (own proportions,
legs and arms), so kit.person and every earlier character are untouched.

THE SMALL ONE (unnamed, a VISITOR sticker): about 60 % of Don's height, a big round head, round glasses, sandy
hair with a cowlick, a grey suit two sizes too big (sleeves over his hands, trousers pooling on big shoes), a
mustard tie. Perfect on paper: he hugs a CV as thick as a brick. Faces: hopeful, proud, neutral, crushed.

THE NICE MACHO (unnamed, a VISITOR sticker): taller than Don, a V-shaped torso, a sky-blue shirt with the sleeves
rolled and one button working hard, dark jeans, a square jaw with stubble, a dark quiff. Kind, never smug: he is
the one who picks up Pam's pen and brings cookies. Faces: smile, warm, listen, gracious.

Usage: o = small(k, x, feet, s, pose, face, look, mouth=None, cv=False)
       o = macho(k, x, feet, s, pose, face, look, mouth=None, glint=False)
Both return {"head", "hands", "top"} in canvas coordinates; pose is a name in POSES_* or (a1, a2, b1, b2) degrees
(0 = down, +90 = screen right, 180 = up), as in kit.ARM_POSES."""
import math
import kit
import iwry_mouths as im
import props_bc_v1 as props
from kit import INK, cut, rect, ellipse

# ------------------------------------------------------------------ shared
VIS_ORANGE = (0.96, 0.56, 0.14)
MOUTH_DARK = (0.40, 0.07, 0.08)


def _d(a):
    return math.sin(math.radians(a)), math.cos(math.radians(a))


def limb(k, sx, sy, a1, a2, ln1, ln2, w1, w2, col1, col2, skin, hand_r, seed, hand_first=False, cuff=None):
    """A two-part arm. hand_first: the hand is drawn under the sleeve end (a sleeve that is too long).
    cuff: a rolled-sleeve band at the elbow, (colour, width)."""
    ex, ey = sx + _d(a1)[0] * ln1, sy + _d(a1)[1] * ln1
    hx, hy = ex + _d(a1 + a2)[0] * ln2, ey + _d(a1 + a2)[1] * ln2
    if hand_first:
        ellipse(k, hx + _d(a1 + a2)[0] * 1, hy + _d(a1 + a2)[1] * 1, hand_r, hand_r, skin, seed, shadow=False, lw=2)
    for ax, ay, bx, by, col, w in ((ex, ey, hx, hy, col2, w2), (sx, sy, ex, ey, col1, w1)):
        ang = math.atan2(by - ay, bx - ax)
        nx, ny = -math.sin(ang) * w / 2, math.cos(ang) * w / 2
        cut(k, [(ax + nx, ay + ny), (bx + nx, by + ny), (bx - nx, by - ny), (ax - nx, ay - ny)], col, shadow=False, lw=2)
    if cuff:
        col, cw = cuff
        ang = math.atan2(ey - sy, ex - sx)
        nx, ny = -math.sin(ang) * (w1 / 2 + 2), math.cos(ang) * (w1 / 2 + 2)
        ux, uy = math.cos(ang) * cw, math.sin(ang) * cw
        cut(k, [(ex + nx - ux, ey + ny - uy), (ex + nx, ey + ny), (ex - nx, ey - ny), (ex - nx - ux, ey - ny - uy)], col,
            shadow=False, lw=1.8)
    if not hand_first:
        ellipse(k, hx, hy, hand_r, hand_r, skin, seed, shadow=False, lw=2)
    return hx, hy


def ik(sx, sy, tx, ty, ln1, ln2, side):
    """Shoulder angles (a1, a2) that put the hand at (tx, ty); the elbow bends away from the body."""
    vx, vy = tx - sx, ty - sy
    D = max(abs(ln1 - ln2) + 0.5, min(math.hypot(vx, vy), ln1 + ln2 - 0.5))
    angD = math.degrees(math.atan2(vx, vy))
    al = math.degrees(math.acos((ln1 * ln1 + D * D - ln2 * ln2) / (2 * ln1 * D)))
    be = math.degrees(math.acos((ln1 * ln1 + ln2 * ln2 - D * D) / (2 * ln1 * ln2)))
    best = None
    for sg in (1, -1):
        a1 = angD + sg * al
        ex = sx + math.sin(math.radians(a1)) * ln1
        if best is None or ex * side > best[0]:
            best = (ex * side, a1, -sg * (180 - be))
    return best[1], best[2]


def visitor(k, x, y, w=30, rot=-0.06, seed=0):
    """The paper VISITOR sticker both candidates wear (no name: nobody asked)."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(rot)
    rect(k, -w / 2, -9, w, 18, (1, 1, 1), seed + 1, shadow=False, lw=1.5)
    c.set_source_rgb(*VIS_ORANGE); c.rectangle(-w / 2 + 1.2, -7.8, w - 2.4, 6.2); c.fill()
    kit.text(k, "VISITOR", 0, 3.6, w * 0.2, INK, font="Inter", bold=True)
    c.restore()


def _brow(c, x1, y1, x2, y2, w):
    c.set_source_rgb(*INK); c.set_line_width(w); c.set_line_cap(1)
    c.move_to(x1, y1); c.line_to(x2, y2); c.stroke()


# ------------------------------------------------------------------ the small one
S_SKIN = (0.99, 0.85, 0.73)
S_HAIR = (0.80, 0.50, 0.22)
S_SUIT = (0.55, 0.58, 0.64)
S_SUIT_DARK = (0.40, 0.43, 0.50)
S_SHIRT = (0.98, 0.98, 0.96)
S_TIE = (0.93, 0.72, 0.18)
S_SHOE = (0.36, 0.22, 0.13)
S_L, S_T = 44, 78
S_HIP = -S_L
S_BT = S_HIP - S_T
S_HY = S_BT - 40
S_SH = (38, S_BT + 16)
S_LN = 30
S_TOP = S_HY - 52


def _s_ik(side, tx, ty):
    return ik(side * S_SH[0], S_SH[1], tx, ty, S_LN, S_LN, side)


POSES_SMALL = {
    "stand": (-10, 4, 10, -4),
    "hug": _s_ik(-1, -8, S_BT + 52) + _s_ik(1, 12, S_BT + 40),            # both arms round the CV
    "offer": (-10, 4) + _s_ik(1, 62, S_BT + 4),                            # the CV held out to the panel, on tiptoe
    "finger": (-10, 4) + _s_ik(1, 44, S_BT - 16),                         # "Three degrees.": one finger up
    "sag": (-4, 2, 4, -2),                                                # crushed: arms hang
    "sit": _s_ik(-1, -22, S_BT + 62) + _s_ik(1, 22, S_BT + 62),           # hands on his knees
}


def _small_face(k, y, face, look, mouth, seed, slip=0.0):
    c = k.c
    lx, ly = look
    gy = y + 4 + slip * 9                                                  # the glasses slide down when he's crushed
    for sx in (-19, 19):
        c.set_source_rgb(1, 1, 1); c.arc(sx, gy, 16.5, 0, 2 * math.pi); c.fill()
    ey = y + 4
    lid = {"hopeful": 0.0, "proud": 0.0, "neutral": 0.0, "crushed": 0.45}.get(face, 0.0)
    if face == "proud":                                                    # eyes shut in a happy arc
        c.set_source_rgb(*INK); c.set_line_width(3.6); c.set_line_cap(1)
        for sx in (-19, 19):
            c.arc(sx, ey + 4, 8, math.pi * 1.15, math.pi * 1.85); c.stroke()
    else:
        dy = 3 if face == "crushed" else 0
        for sx in (-19, 19):
            ellipse(k, sx + lx * 4.5, ey + ly * 4.5 + dy, 5.2, 5.2, INK, seed + sx + 1, shadow=False, outline=False)
            c.set_source_rgb(1, 1, 1); c.arc(sx + lx * 4.5 - 1.6, ey + ly * 4.5 + dy - 1.8, 1.5, 0, 2 * math.pi); c.fill()
        if lid:
            for sx in (-19, 19):
                c.save(); c.arc(sx, gy, 15.5, 0, 2 * math.pi); c.clip()
                c.set_source_rgb(*S_SKIN); c.rectangle(sx - 17, gy - 17, 34, 17 * 2 * lid + 2); c.fill()
                c.restore()
                _brow(c, sx - 13, gy - 17 + 34 * lid + 1, sx + 13, gy - 17 + 34 * lid + 1, 2.6)
    c.set_source_rgb(*INK); c.set_line_width(3.2)
    for sx in (-19, 19):
        c.arc(sx, gy, 16.5, 0, 2 * math.pi); c.stroke()
    c.move_to(-3, gy - 2); c.curve_to(-1, gy - 5, 1, gy - 5, 3, gy - 2); c.stroke()
    c.set_source_rgba(1, 1, 1, 0.75); c.set_line_width(2.2)                 # lens shine
    for sx in (-19, 19):
        c.arc(sx, gy, 12, math.pi * 1.1, math.pi * 1.4); c.stroke()
    by = y - 20
    if face == "hopeful":
        _brow(c, -30, by + 1, -12, by - 5, 3.4); _brow(c, 12, by - 5, 30, by + 1, 3.4)
    elif face == "proud":
        _brow(c, -30, by - 2, -12, by - 4, 3.4); _brow(c, 12, by - 4, 30, by - 2, 3.4)
    elif face == "crushed":
        _brow(c, -30, by + 5, -12, by - 4, 3.4); _brow(c, 12, by - 4, 30, by + 5, 3.4)
    else:
        _brow(c, -29, by, -12, by, 3.4); _brow(c, 12, by, 29, by, 3.4)
    c.set_source_rgba(0.75, 0.42, 0.25, 0.7)                                # freckles
    for fx, fy in ((-33, 24), (-27, 28), (-36, 30), (33, 24), (27, 28), (36, 30)):
        c.arc(fx, y + fy, 1.5, 0, 2 * math.pi); c.fill()
    my = y + 31
    if mouth:
        im.mouth(k, 0, my, mouth, S_SKIN, erase=(1, 1), seed=seed + 96)
        return
    c.set_source_rgb(*INK); c.set_line_width(3.4); c.set_line_cap(1)
    if face == "hopeful":
        c.arc(0, my - 7, 11, 0.2 * math.pi, 0.8 * math.pi); c.stroke()
    elif face == "proud":
        c.move_to(-12, my - 3); c.curve_to(-6, my + 9, 6, my + 9, 12, my - 3); c.close_path()
        c.set_source_rgb(1, 1, 1); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.6); c.stroke()
    elif face == "crushed":
        c.move_to(-10, my + 3); c.curve_to(-5, my - 4, 0, my + 4, 4, my - 1); c.curve_to(6, my - 3, 9, my + 1, 11, my + 3)
        c.stroke()
    else:
        c.move_to(-8, my); c.line_to(8, my); c.stroke()


def small(k, x, feet, s=1.0, pose="stand", face="hopeful", look=(0, 0), seed=600, mouth=None, badge=True, cv=False,
          tiptoe=0.0, seated=False):
    """cv: True draws the CV brick in his hands (poses "hug" and "offer"). tiptoe: 0..1 lifts his heels.
    seated: legs dangle straight down from a chair seat at `feet` (his shoes hang below it)."""
    c = k.c
    a = POSES_SMALL[pose] if isinstance(pose, str) else pose
    slump = 5 if face == "crushed" else 0
    c.save(); c.translate(x, feet - tiptoe * 7 * s); c.scale(s, s)
    if seated:
        c.translate(0, S_L - 6)                                             # the seat is at his hips; legs hang
    # legs: trousers too long, pooling on big shoes
    for sx in (-1, 1):
        ellipse(k, sx * 19, -4 + tiptoe * 4, 19, 8.5, S_SHOE, seed + 3 + sx, shadow=not seated, lw=2)
        cut(k, [(sx * 4, S_HIP - 2), (sx * 31, S_HIP - 2), (sx * 33, -7), (sx * 3, -7)], S_SUIT, shadow=False, lw=2)
        c.set_source_rgb(*S_SUIT_DARK); c.set_line_width(1.8)
        for yy in (-12, -18):
            c.move_to(sx * 6, yy); c.curve_to(sx * 14, yy + 3, sx * 22, yy - 3, sx * 30, yy + 1); c.stroke()
    bt = S_BT + slump
    # jacket: wide, long, shoulders past his own
    cut(k, [(-41, bt + 6), (-30, bt - 2), (30, bt - 2), (41, bt + 6), (45, S_HIP + 12), (-45, S_HIP + 12)], S_SUIT, lw=2.4)
    cut(k, [(0, bt + 44), (-13, bt - 1), (13, bt - 1)], S_SHIRT, shadow=False, lw=1.6)
    cut(k, [(0, bt + 5), (-5.5, bt + 12), (0, bt + 44), (5.5, bt + 12)], S_TIE, shadow=False, lw=1.5)
    cut(k, [(-4, bt + 1), (4, bt + 1), (5, bt + 8), (-5, bt + 8)], S_TIE, shadow=False, lw=1.5)
    for sx in (-1, 1):                                                      # lapels
        cut(k, [(sx * 13, bt - 1), (sx * 26, bt + 2), (sx * 20, bt + 30), (0, bt + 46)], S_SUIT, shadow=False, lw=1.8)
    c.set_source_rgb(*S_SUIT_DARK); c.set_line_width(2)
    c.move_to(0, bt + 46); c.line_to(1, S_HIP + 12); c.stroke()
    for i, by in enumerate((58, 72)):
        ellipse(k, 5, bt + by, 3, 3, S_SUIT_DARK, seed + 40 + i, shadow=False, lw=1.2)
    c.set_source_rgb(*S_SUIT_DARK); c.set_line_width(1.8)
    c.move_to(-36, bt + 64); c.line_to(-20, bt + 64); c.stroke()             # pocket
    if badge:
        visitor(k, 17, bt + 42, 23, -0.08, seed + 50)
    hands = []
    held = cv and pose in ("hug", "offer")
    if held and pose == "hug":
        props.cv_brick(k, 2, bt + 46, 0.62, -0.08, seed + 60)
    for side, (u, f) in ((-1, (a[0], a[1])), (1, (a[2], a[3]))):
        hands.append(limb(k, side * S_SH[0], bt + 16, u, f, S_LN, S_LN, 18, 19, S_SUIT, S_SUIT, S_SKIN, 8, seed + 10 + side,
                          hand_first=True))
    # head
    hy = S_HY + slump * 1.6
    for sx in (-1, 1):
        ellipse(k, sx * 46, hy + 6, 8, 11, S_SKIN, seed + 20 + sx, shadow=False, lw=2)
    ellipse(k, 0, hy, 46, 45, S_SKIN, seed + 22)
    cut(k, [(-46, hy - 8), (-48, hy - 28), (-36, hy - 46), (-12, hy - 54), (16, hy - 53), (36, hy - 43), (47, hy - 26),
            (46, hy - 8), (39, hy - 20), (22, hy - 29), (-4, hy - 25), (-14, hy - 31), (-31, hy - 21)], S_HAIR,
        shadow=False, lw=2)
    c.set_source_rgb(*INK); c.set_line_width(6.4); c.set_line_cap(1)                                              # cowlick
    c.move_to(18, hy - 51); c.curve_to(18, hy - 66, 30, hy - 70, 34, hy - 60); c.stroke()
    c.set_source_rgb(*S_HAIR); c.set_line_width(3.4)
    c.move_to(18, hy - 50); c.curve_to(18, hy - 66, 30, hy - 70, 34, hy - 60); c.stroke()
    c.set_source_rgb(0.60, 0.34, 0.12); c.set_line_width(1.8)
    c.move_to(-12, hy - 22); c.curve_to(-16, hy - 34, -14, hy - 44, -8, hy - 50); c.stroke()                         # the parting
    _small_face(k, hy, face, look, mouth, seed + 30, slip=1.0 if face == "crushed" else 0.0)
    if held and pose == "offer":
        hx_, hy_ = hands[1]
        props.cv_brick(k, hx_ + 20, hy_ - 26, 0.6, 0.10, seed + 60)
        ellipse(k, hx_ + 2, hy_ + 2, 8, 8, S_SKIN, seed + 70, shadow=False, lw=2)
    off = (S_L - 6) if seated else 0
    c.restore()
    fy = feet - tiptoe * 7 * s
    return {"head": (x, fy + (hy + off) * s), "hands": [(x + hx * s, fy + (hy_ + off) * s) for hx, hy_ in hands],
            "top": fy + (S_TOP + off) * s}


# ------------------------------------------------------------------ the nice macho
M_SKIN = (0.87, 0.66, 0.50)
M_SKIN_DARK = (0.72, 0.50, 0.36)
M_HAIR = (0.19, 0.12, 0.08)
M_SHIRT = (0.66, 0.82, 0.95)
M_SHIRT_DARK = (0.44, 0.62, 0.80)
M_JEANS = (0.17, 0.24, 0.40)
M_JEANS_DARK = (0.11, 0.16, 0.29)
M_BELT = (0.42, 0.26, 0.14)
M_BOOT = (0.50, 0.32, 0.18)
M_L, M_T = 146, 140
M_HIP = -M_L
M_BT = M_HIP - M_T
M_HY = M_BT - 50
M_SH = (57, M_BT + 20)
M_LN1, M_LN2 = 52, 50
M_TOP = M_HY - 60


def _m_ik(side, tx, ty):
    return ik(side * M_SH[0], M_SH[1], tx, ty, M_LN1, M_LN2, side)


POSES_MACHO = {
    "stand": (-7, 2, 7, -2),
    "pen": (-7, 2) + _m_ik(1, 88, M_BT + 70),                              # hands Pam her pen, palm up
    "tin": _m_ik(-1, -26, M_BT + 96) + _m_ik(1, 26, M_BT + 96),            # the cookie tin in both hands
    "wave": (-7, 2) + _m_ik(1, 96, M_BT - 34),                             # a small open-hand hello
    "shrug": _m_ik(-1, -98, M_BT + 62) + _m_ik(1, 98, M_BT + 62),          # gracious: palms out, no hard feelings
    "sit": _m_ik(-1, -30, M_BT + 118) + _m_ik(1, 30, M_BT + 118),
}


def _head_pts(k, hy, seed):
    """A square-jawed head: round on top, a wide flat chin."""
    r = k.rng(seed)
    pts = []
    n = 30
    for i in range(n):
        a = 2 * math.pi * i / n
        cs, sn = math.cos(a), math.sin(a)
        if sn > 0:                                                          # lower half: a superellipse (the jaw)
            px = math.copysign(abs(cs) ** 0.55, cs) * 43
            py = (sn ** 0.72) * 50
        else:
            px, py = cs * 45, sn * 46
        pts.append((px * (1 + r.uniform(-0.012, 0.012)), hy + py * (1 + r.uniform(-0.012, 0.012))))
    return pts


def _macho_face(k, y, face, look, mouth, seed, glint):
    c = k.c
    lx, ly = look
    ey = y - 2
    smile = face in ("smile", "warm", "gracious")
    for sx in (-18, 18):
        ellipse(k, sx, ey, 9.5, 9.5, (1, 1, 1), seed + sx, shadow=False, lw=2)
        ellipse(k, sx + lx * 3.6, ey + ly * 3.6, 4.6, 4.6, (0.24, 0.15, 0.08), seed + sx + 1, shadow=False, outline=False)
        c.set_source_rgb(1, 1, 1); c.arc(sx + lx * 3.6 - 1.5, ey + ly * 3.6 - 1.6, 1.4, 0, 2 * math.pi); c.fill()
        if smile:                                                           # the cheek pushes the lower lid up
            c.set_source_rgb(*M_SKIN); c.rectangle(sx - 11, ey + 5, 22, 7); c.fill()
            c.set_source_rgb(*INK); c.set_line_width(2.2); c.set_line_cap(1)
            c.move_to(sx - 9, ey + 6); c.curve_to(sx - 4, ey + 3.5, sx + 4, ey + 3.5, sx + 9, ey + 6); c.stroke()
    by = y - 17
    if face == "gracious":                                                  # brows up in the middle: "no worries"
        _brow(c, -30, by + 1, -9, by - 5, 5.2); _brow(c, 9, by - 5, 30, by + 1, 5.2)
    elif face == "listen":
        _brow(c, -30, by - 1, -9, by + 1, 5.2); _brow(c, 9, by - 3, 30, by - 4, 5.2)
    else:
        _brow(c, -30, by, -9, by - 2, 5.2); _brow(c, 9, by - 2, 30, by, 5.2)
    c.set_source_rgb(*M_SKIN_DARK); c.set_line_width(2.6); c.set_line_cap(1)  # nose
    c.move_to(1, y + 4); c.line_to(5, y + 15); c.line_to(-2, y + 16); c.stroke()
    my = y + 31
    if mouth:
        im.mouth(k, 0, my, mouth, M_SKIN, erase=(1, 1), seed=seed + 96)
    elif face == "smile":
        c.move_to(-17, my - 6); c.curve_to(-9, my - 3, 9, my - 3, 17, my - 6)
        c.curve_to(12, my + 9, -12, my + 9, -17, my - 6); c.close_path()
        c.set_source_rgb(1, 1, 1); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.6); c.stroke()
    elif face in ("warm", "gracious"):
        c.set_source_rgb(*INK); c.set_line_width(3.6); c.set_line_cap(1)
        c.move_to(-14, my - 4); c.curve_to(-6, my + 5, 6, my + 5, 14, my - 4); c.stroke()
    else:
        c.set_source_rgb(*INK); c.set_line_width(3.6); c.set_line_cap(1)
        c.move_to(-10, my); c.curve_to(-4, my + 2, 4, my + 2, 11, my - 1); c.stroke()
    if smile:                                                               # dimples
        c.set_source_rgb(*M_SKIN_DARK); c.set_line_width(2.2)
        for sx in (-1, 1):
            c.move_to(sx * 22, my - 9); c.curve_to(sx * 26, my - 5, sx * 26, my, sx * 22, my + 3); c.stroke()
    if glint and face == "smile":
        c.save(); c.translate(15, my - 5); c.scale(0.7, 0.7)
        c.move_to(0, -8); c.line_to(1.8, -1.8); c.line_to(8, 0); c.line_to(1.8, 1.8); c.line_to(0, 8)
        c.line_to(-1.8, 1.8); c.line_to(-8, 0); c.line_to(-1.8, -1.8); c.close_path()
        c.set_source_rgb(1, 1, 1); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1.2); c.stroke()
        c.restore()


def macho(k, x, feet, s=1.0, pose="stand", face="smile", look=(0, 0), seed=700, mouth=None, badge=True, glint=False,
          tin=False, pen=False, seated=False):
    """tin: the cookie tin in his hands (pose "tin"). pen: Pam's pen on his open palm (pose "pen").
    seated: thighs forward (drawn short), for the interview chair; `feet` is still the floor."""
    c = k.c
    a = POSES_MACHO[pose] if isinstance(pose, str) else pose
    c.save(); c.translate(x, feet); c.scale(s, s)
    drop = 0
    if seated:
        drop = 62                                                           # the hips come down to the seat
        for sx in (-1, 1):
            ellipse(k, sx * 24, -5, 21, 9, M_BOOT, seed + 3 + sx, lw=2)
            cut(k, [(sx * 12, M_HIP + drop + 30), (sx * 36, M_HIP + drop + 30), (sx * 35, -8), (sx * 13, -8)], M_JEANS,
                shadow=False, lw=2)
            cut(k, [(sx * 3, M_HIP + drop - 6), (sx * 40, M_HIP + drop - 6), (sx * 40, M_HIP + drop + 34),
                    (sx * 8, M_HIP + drop + 34)], M_JEANS, shadow=False, lw=2)
    else:
        for sx in (-1, 1):
            ellipse(k, sx * 20, -5, 21, 9, M_BOOT, seed + 3 + sx, lw=2)
            cut(k, [(sx * 1, M_HIP - 4), (sx * 39, M_HIP - 4), (sx * 31, -8), (sx * 7, -8)], M_JEANS, shadow=False, lw=2)
            c.set_source_rgb(*M_JEANS_DARK); c.set_line_width(1.8)
            c.move_to(sx * 33, M_HIP + 14); c.line_to(sx * 27, -12); c.stroke()
    c.translate(0, drop)
    bt = M_BT
    rect(k, -15, bt - 18, 30, 24, M_SKIN, seed + 5, shadow=False, lw=2)       # neck
    cut(k, [(-64, bt + 12), (-48, bt), (48, bt), (64, bt + 12), (40, M_HIP - 6), (-40, M_HIP - 6)], M_SHIRT, lw=2.4)
    cut(k, [(0, bt + 36), (-15, bt + 1), (15, bt + 1)], M_SKIN, shadow=False, lw=1.6)          # open collar
    for sx in (-1, 1):
        cut(k, [(sx * 15, bt + 1), (sx * 31, bt - 7), (sx * 24, bt + 20), (sx * 4, bt + 34)], M_SHIRT, shadow=False, lw=1.8)
    c.set_source_rgb(*M_SHIRT_DARK); c.set_line_width(2); c.set_line_cap(1)
    c.move_to(0, bt + 36); c.line_to(0, M_HIP - 8); c.stroke()                # placket
    for sx in (-1, 1):                                                       # the chest, two soft curves
        c.move_to(sx * 6, bt + 62); c.curve_to(sx * 18, bt + 72, sx * 40, bt + 68, sx * 50, bt + 50); c.stroke()
    for i, by in enumerate((48, 84, 108)):
        ellipse(k, 0, bt + by, 3, 3, (1, 1, 1), seed + 40 + i, shadow=False, lw=1.3)
    c.save(); c.translate(0, bt + 62); c.scale(2.6, 6.5); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()   # the button gap
    c.set_source_rgb(*M_SKIN); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1.3); c.stroke()
    ellipse(k, 0, bt + 62, 3, 3, (1, 1, 1), seed + 45, shadow=False, lw=1.3)                              # holding on
    c.set_source_rgb(*M_SHIRT_DARK); c.set_line_width(1.4)
    for sx in (-1, 1):
        c.move_to(sx * 5, bt + 60); c.line_to(sx * 14, bt + 56); c.stroke()
        c.move_to(sx * 5, bt + 64); c.line_to(sx * 14, bt + 68); c.stroke()
    rect(k, -40, M_HIP - 10, 80, 11, M_BELT, seed + 61, shadow=False, lw=1.6)
    rect(k, -7, M_HIP - 12, 14, 15, (0.80, 0.70, 0.36), seed + 62, shadow=False, lw=1.4)
    if badge:
        visitor(k, 27, bt + 40, 28, -0.06, seed + 50)
    hands = []
    for side, (u, f) in ((-1, (a[0], a[1])), (1, (a[2], a[3]))):
        hands.append(limb(k, side * M_SH[0], bt + 20, u, f, M_LN1, M_LN2, 27, 22, M_SHIRT, M_SKIN, M_SKIN, 13,
                          seed + 10 + side, cuff=((0.80, 0.90, 0.98), 9)))
    # head
    hy = M_HY
    cut(k, _head_pts(k, hy, seed + 20), M_SKIN)
    c.save()                                                                 # stubble: a shadow on the jaw
    pts = _head_pts(k, hy, seed + 20)
    c.move_to(*pts[0])
    for q in pts[1:]:
        c.line_to(*q)
    c.close_path(); c.clip()
    c.set_source_rgba(0.16, 0.10, 0.07, 0.20)
    c.move_to(-50, hy + 14); c.curve_to(-30, hy + 20, -24, hy + 22, -20, hy + 34)
    c.curve_to(-10, hy + 22, 10, hy + 22, 20, hy + 34); c.curve_to(24, hy + 22, 30, hy + 20, 50, hy + 14)
    c.line_to(50, hy + 60); c.line_to(-50, hy + 60); c.close_path(); c.fill()
    c.restore()
    for sx in (-1, 1):                                                       # ears
        ellipse(k, sx * 45, hy + 4, 6, 10, M_SKIN, seed + 26 + sx, shadow=False, lw=2)
    # hair: short sides, a swept quiff
    cut(k, [(-47, hy - 4), (-48, hy - 30), (-36, hy - 50), (-8, hy - 62), (22, hy - 64), (42, hy - 50), (49, hy - 28),
            (47, hy - 4), (40, hy - 18), (30, hy - 30), (4, hy - 26), (-22, hy - 32), (-38, hy - 22)], M_HAIR,
        shadow=False, lw=2)
    c.set_source_rgba(1, 1, 1, 0.22); c.set_line_width(3); c.set_line_cap(1)
    c.move_to(-20, hy - 50); c.curve_to(-4, hy - 58, 16, hy - 56, 30, hy - 44); c.stroke()
    _macho_face(k, hy + 4, face, look, mouth, seed + 30, glint)
    if tin and pose == "tin":
        mx = (hands[0][0] + hands[1][0]) / 2
        props.cookie_tin(k, mx, hands[0][1] - 6, 0.9, seed + 80)
        for hx_, hy_ in hands:
            ellipse(k, hx_, hy_ + 4, 12, 11, M_SKIN, seed + 82, shadow=False, lw=2)
    if pen and pose == "pen":
        hx_, hy_ = hands[1]
        props.pen(k, hx_ + 2, hy_ - 12, 1.0, 0.15)
    c.restore()
    return {"head": (x, feet + (hy + drop) * s), "hands": [(x + hx * s, feet + (hy_ + drop) * s) for hx, hy_ in hands],
            "top": feet + (M_TOP + drop) * s}
