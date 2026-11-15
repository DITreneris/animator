"""SOFÍA, new hire, main character of "The Human in the Loop" (UptimeZ Inc.).
Same flat paper-cutout kit and proportions as PAM (h 1.02, head r 50), plus her own parts:
long dark-brown hair (back layer + face-framing locks), gold hoops, ivory blouse with rolled sleeves,
black skirt, dark tights, ankle boots, red lips and nails, slim onboarding folder.
Hair and hoops take a `lag` offset so they can trail head turns by ~2 frames.
Usage: p = sofia(k, x, feet, s, pose="stand", face="neutral", look=(0, 0), lag=(0, 0), folder="tuck")"""
import math
import kit
import brand
from kit import INK, cut, rect, ellipse, rough_ellipse_pts, text

SKIN = (0.87, 0.67, 0.52)
HAIR = (0.24, 0.14, 0.09)
BLOUSE = (0.97, 0.94, 0.86)
SKIRT = (0.12, 0.12, 0.14)
TIGHTS = (0.20, 0.19, 0.22)
BOOTS = (0.08, 0.08, 0.09)
RED = (0.78, 0.12, 0.16)
GOLD = (0.86, 0.67, 0.22)
FOLDER = (0.55, 0.80, 0.66)
H = 1.02

POSES = {   # (left upper, left fore, right upper, right fore): kit.arm angles, 0 = down, +90 = right, 180 = up
    "stand": (-8, 0, 8, 0),
    "tuck": (-14, 40, 8, 0),          # folder tucked under the left arm
    "ask": (-14, 40, 30, 70),         # right palm open, mid-gesture
    "offer": (-40, 95, 40, -95),      # both hands forward, folder held out
    "cross": (-55, 115, 55, -115),    # arms crossed (folder hugged)
    "point_l": (-95, 0, 8, 0),
}


def _arm(k, sx, sy, a1, a2, seed, ln=48, w=17):
    """Rolled sleeves: ivory upper arm, bare forearm, red nail tip."""
    d = lambda a: (math.sin(math.radians(a)), math.cos(math.radians(a)))
    ex, ey = sx + d(a1)[0] * ln, sy + d(a1)[1] * ln
    hx, hy = ex + d(a1 + a2)[0] * ln, ey + d(a1 + a2)[1] * ln
    for (ax, ay, bx, by), col in (((sx, sy, ex, ey), BLOUSE), ((ex, ey, hx, hy), SKIN)):
        ang = math.atan2(by - ay, bx - ax)
        nx, ny = -math.sin(ang) * w / 2, math.cos(ang) * w / 2
        cut(k, [(ax + nx, ay + ny), (bx + nx, by + ny), (bx - nx, by - ny), (ax - nx, ay - ny)], col, shadow=False, lw=2)
    ang = math.atan2(ey - sy, ex - sx)                # rolled cuff at the elbow
    nx, ny = -math.sin(ang) * (w / 2 + 2), math.cos(ang) * (w / 2 + 2)
    cx, cy = ex - (ex - sx) * 0.12, ey - (ey - sy) * 0.12
    cut(k, [(cx + nx, cy + ny), (ex + nx, ey + ny), (ex - nx, ey - ny), (cx - nx, cy - ny)], BLOUSE, shadow=False, lw=2)
    ellipse(k, hx, hy, w * 0.6, w * 0.6, SKIN, seed, shadow=False, lw=2)
    fa = math.atan2(hy - ey, hx - ex)
    ellipse(k, hx + math.cos(fa) * 7, hy + math.sin(fa) * 7, 3.2, 3.2, RED, seed + 1, shadow=False, outline=False)
    return hx, hy


def face(k, x, y, kind="neutral", look=(0, 0), seed=0):
    """Her expressions. The signature is "eyebrow": one brow up, the other flat, mouth level."""
    c = k.c
    lx, ly = look
    big = kind == "surprised"
    for sx in (-17, 17):
        r = 13 if big else 10.5
        ellipse(k, x + sx, y, r, r, (1, 1, 1), seed + sx, shadow=False, lw=2)
        ellipse(k, x + sx + lx * 4, y + ly * 4, 4.6, 4.6, INK, seed + sx + 1, shadow=False, outline=False)
        if kind == "knowing":                         # half-lidded
            c.save(); c.rectangle(x + sx - 14, y - 15, 28, 14); c.clip()
            ellipse(k, x + sx, y, r + 1, r + 1, SKIN, seed + sx + 2, shadow=False, outline=False)
            c.restore()
            c.set_source_rgb(*INK); c.set_line_width(3.5)
            c.move_to(x + sx - 11, y - 1); c.line_to(x + sx + 11, y - 1); c.stroke()
        c.set_source_rgb(*INK); c.set_line_width(2.6)    # one lash at the outer corner
        o = -1 if sx < 0 else 1
        c.move_to(x + sx + o * 8, y - 7); c.line_to(x + sx + o * 15, y - 13); c.stroke()
    c.set_source_rgb(*INK); c.set_line_width(4); c.set_line_cap(1)
    brows = {   # (left start y, left end y, right start y, right end y), relative to the eye line
        "neutral": (-18, -21, -21, -18), "curious": (-24, -27, -27, -24), "eyebrow": (-15, -15, -36, -28),
        "smile": (-19, -22, -22, -19), "surprised": (-28, -31, -31, -28), "knowing": (-16, -18, -18, -16),
    }[kind]
    c.move_to(x - 27, y + brows[0]); c.curve_to(x - 20, y + brows[1] - 3, x - 14, y + brows[1] - 3, x - 8, y + brows[1]); c.stroke()
    c.move_to(x + 8, y + brows[2]); c.curve_to(x + 14, y + brows[2] - 3, x + 20, y + brows[3] - 3, x + 27, y + brows[3]); c.stroke()
    my = y + 29
    if kind in ("curious", "surprised"):
        ellipse(k, x, my, 6 if kind == "curious" else 8, 7 if kind == "curious" else 10, (0.45, 0.06, 0.08), seed + 5,
                shadow=False, lw=2)
        c.set_source_rgb(*RED); c.set_line_width(3.2)
        c.arc(x, my, (6 if kind == "curious" else 8) + 1.5, 0, 2 * math.pi); c.stroke()
    elif kind == "smile":
        c.set_source_rgb(*RED); c.set_line_width(5)
        c.arc(x, my - 9, 12, 0.22 * math.pi, 0.78 * math.pi); c.stroke()
    elif kind == "knowing":
        c.set_source_rgb(*RED); c.set_line_width(5)
        c.move_to(x - 10, my + 1); c.curve_to(x - 2, my + 4, x + 6, my + 2, x + 12, my - 4); c.stroke()
    else:                                             # closed red lips, level (eyebrow: a touch to one side)
        dx = 3 if kind == "eyebrow" else 0
        ellipse(k, x + dx, my, 10, 3.6, RED, seed + 6, shadow=False, outline=False)
        c.set_source_rgb(*INK); c.set_line_width(1.6)
        c.move_to(x + dx - 9, my); c.line_to(x + dx + 9, my); c.stroke()


def sofia(k, x, feet, s=1.0, pose="tuck", face_kind="neutral", look=(0, 0), lag=(0, 0), seed=7, badge=True,
          folder=None):
    """Returns {"head": (x, y), "hands": [...], "folder": box or None} in canvas coordinates."""
    c = k.c
    c.save(); c.translate(x, feet); c.scale(s, s)
    body_top = -300 * H + 78
    hy = body_top - 44
    lgx, lgy = lag
    folder = folder if folder is not None else ("tuck" if pose in ("tuck", "ask") else
                                                 ("offer" if pose == "offer" else ("hug" if pose == "cross" else None)))
    # long hair, back layer (behind the body), trails head turns
    back = [(-56 + lgx, hy - 30), (-62 + lgx * 1.4, body_top + 40), (-52 + lgx * 1.8, body_top + 92 + lgy),
            (-20 + lgx * 1.8, body_top + 100 + lgy), (20 + lgx * 1.8, body_top + 100 + lgy),
            (52 + lgx * 1.8, body_top + 92 + lgy), (62 + lgx * 1.4, body_top + 40), (56 + lgx, hy - 30)]
    cut(k, back, HAIR, lw=2.2)
    # legs, boots, skirt, blouse
    for sx in (-15, 15):
        rect(k, sx - 7, -64, 14, 54, TIGHTS, seed + 30 + sx, shadow=False, lw=1.8)
        rect(k, sx - 11 + (sx > 0) * 4, -16, 22, 16, BOOTS, seed + 32 + sx, shadow=False, lw=1.8)
    skirt = [(-40, body_top + 106), (40, body_top + 106), (48, -60), (-48, -60)]
    cut(k, skirt, SKIRT)
    blouse = [(-39, body_top), (39, body_top), (42, body_top + 112), (-42, body_top + 112)]
    cut(k, blouse, BLOUSE)
    c.set_source_rgb(*INK); c.set_line_width(2)          # collar notch and a tuck line
    c.move_to(-12, body_top + 2); c.line_to(0, body_top + 20); c.line_to(12, body_top + 2); c.stroke()
    c.move_to(-40, body_top + 108); c.line_to(40, body_top + 108); c.stroke()
    if badge:
        rect(k, 4, body_top + 34, 38, 22, (1, 1, 1), seed + 40, shadow=False, lw=1.6)
        c.set_source_rgb(*brand.GREEN); c.rectangle(7, body_top + 36, 32, 3.5); c.fill()
        text(k, "SOFÍA", 23, body_top + 47, 10.5, INK)
    a = POSES.get(pose) or kit.ARM_POSES[pose]
    if folder == "tuck":                                 # under the left arm, against the body
        rect(k, -58, body_top + 26, 16, 82, FOLDER, seed + 50, shadow=False, lw=1.8)
    hands = [_arm(k, -40, body_top + 14, a[0], a[1], seed + 9), _arm(k, 40, body_top + 14, a[2], a[3], seed + 11)]
    fbox = None
    if folder in ("offer", "hug"):                       # held in front, between the hands
        (ax, ay), (bx, by) = hands
        fx, fy = (ax + bx) / 2, (ay + by) / 2 - (6 if folder == "offer" else -4)
        rect(k, fx - 34, fy - 26, 68, 50, FOLDER, seed + 51, lw=2)
        c.set_source_rgb(1, 1, 1); c.rectangle(fx - 22, fy - 16, 30, 7); c.fill()
        for hxx, hyy in hands:                          # fingers over the folder edge
            ellipse(k, hxx, hyy, 9.5, 9.5, SKIN, seed + 52, shadow=False, lw=2)
            ellipse(k, hxx, hyy - 6, 3.2, 3.2, RED, seed + 53, shadow=False, outline=False)
        fbox = (x + (fx - 34) * s, feet + (fy - 26) * s, x + (fx + 34) * s, feet + (fy + 24) * s)
    # head, front hair, locks, hoops
    ellipse(k, 0, hy, 50, 50, SKIN, seed + 20)
    cap = rough_ellipse_pts(k, 0, hy - 10, 54, 48, seed + 21)
    cap = [q for q in cap if q[1] < hy - 30] + [(53, hy - 24), (30, hy - 40), (0, hy - 44), (-30, hy - 40), (-53, hy - 22)]
    cap.sort(key=lambda q: math.atan2(q[1] - (hy - 10), q[0]))
    cut(k, cap, HAIR, shadow=False, lw=2)               # hairline high enough to leave the brows readable
    cut(k, [(-50, hy - 28), (-10, hy - 52), (34, hy - 48), (53, hy - 26), (22, hy - 40), (-22, hy - 38)],
        HAIR, shadow=False, lw=2)                        # side-swept fringe, parted on her left
    for sx in (-1, 1):                                   # face-framing locks down to the shoulders
        lx0 = sx * 50
        cut(k, [(lx0 - 8 * sx, hy - 18), (lx0 + 8 * sx, hy - 22), (lx0 + 12 * sx + lgx * 0.6, hy + 58 + lgy),
                (lx0 - 2 * sx + lgx * 0.6, hy + 64 + lgy)], HAIR, shadow=False, lw=2)
    for sx in (-1, 1):                                   # gold hoops below the locks, swinging with lag
        hx0, hy0 = sx * 47 + lgx * 0.8, hy + 32 + abs(lgx) * 0.2
        c.set_source_rgb(*INK); c.set_line_width(5.6); c.arc(hx0, hy0, 9, 0, 2 * math.pi); c.stroke()
        c.set_source_rgb(*GOLD); c.set_line_width(3.4); c.arc(hx0, hy0, 9, 0, 2 * math.pi); c.stroke()
    face(k, 0, hy + 4, face_kind, look, seed + 60)
    c.restore()
    return {"head": (x, feet + hy * s), "hands": [(x + hx * s, feet + hyy * s) for hx, hyy in hands], "folder": fbox}
