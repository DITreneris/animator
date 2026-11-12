"""SOFÍA v4 (sofia.py = v2/v3 is kept): the next-film look. Same proportions and silhouette; the glow-up is
all face, hair, accessories and wardrobe:
- eyes: bolder upper liner with a small wing, two lashes, a touch larger, with a catchlight;
- hair: more volume (wider back layer and crown), a deeper side part and a light shine streak;
- lips: a stronger red, fuller shape with a cupid's bow and a white gloss highlight;
- hoops: 1.6x the diameter, thicker, with a highlight;
- outfit: a teal wrap blouse (crossover neckline, rolled sleeves) with a thin belt and gold buckle.

v2 notes: SOFÍA, new hire, main character of "The Human in the Loop" (UptimeZ Inc.).
Same flat paper-cutout kit and proportions as PAM (h 1.02, head r 50), plus her own parts:
long blonde hair (back layer + face-framing locks), gold hoops, ivory blouse with rolled sleeves,
short black skirt, dark tights, ankle boots, red lips and nails, slim onboarding folder.
Hair and hoops take a `lag` offset so they can trail head turns by ~2 frames.
Usage: p = sofia(k, x, feet, s, pose="stand", face="neutral", look=(0, 0), lag=(0, 0), folder="tuck")"""
import math
import kit
import brand
from kit import INK, cut, rect, ellipse, rough_ellipse_pts, text

SKIN = (0.87, 0.67, 0.52)
HAIR = (0.98, 0.87, 0.56)       # v2: blonde
HAIR_SHINE = (1.0, 0.96, 0.80)  # v4: light streak
HAIR_SHADE = (0.88, 0.72, 0.38)  # v4: under-layer for volume
BLOUSE = (0.15, 0.50, 0.52)     # v4: teal wrap blouse (v2 was ivory)
BLOUSE_SHADE = (0.10, 0.40, 0.42)
BELT = (0.10, 0.08, 0.08)
SKIRT = (0.12, 0.12, 0.14)
TIGHTS = (0.20, 0.19, 0.22)
BOOTS = (0.08, 0.08, 0.09)
RED = (0.86, 0.05, 0.12)        # v4: stronger red (v2 0.78, 0.12, 0.16)
RED_DARK = (0.58, 0.02, 0.08)
GOLD = (0.80, 0.55, 0.12)       # deeper than the hair so the hoops read
GOLD_LIGHT = (1.0, 0.86, 0.45)
HOOP_R = 14.4                   # v4: 1.6x the v2 hoop (9)
FOLDER = (0.55, 0.80, 0.66)
H = 1.02

POSES = {   # (left upper, left fore, right upper, right fore): kit.arm angles, 0 = down, +90 = right, 180 = up
    "stand": (-8, 0, 8, 0),
    "tuck": (-14, 40, 8, 0),          # folder tucked under the left arm
    "ask": (-14, 40, 30, 70),         # right palm open, mid-gesture
    "offer": (-40, 95, 40, -95),      # both hands forward, folder held out
    "cross": (-55, 115, 55, -115),    # arms crossed (folder hugged)
    "point_l": (-95, 0, 8, 0),
    "twirl": (-14, 40, 115, 89),      # right hand up at the lock beside her face (forearm 40)
    "hip": (-30, 110, 8, 0),          # left hand on hip
    "wave": (-14, 40, 112, -42),      # Don's lazy wave toward Pam (17:00)
    "press": (-100, 20, 8, 0),        # left hand out to the coffee maker's BREW button
    "mug": (-14, 40, 30, -120),       # right hand holding a mug at chest height
    "finger": (-14, 40, 158, 14),     # "I Will Replace You": right hand up, one finger raised to order
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
    big = kind in ("surprised", "horrified")
    for sx in (-17, 17):
        if kind == "closed":                              # resigned blink: both lids down, lashes along the line
            c.set_source_rgb(*INK); c.set_line_width(4); c.set_line_cap(1)
            c.move_to(x + sx - 11, y + 1); c.curve_to(x + sx - 4, y + 5, x + sx + 4, y + 5, x + sx + 11, y + 1)
            c.stroke()
            continue
        if kind == "wink" and sx > 0:                 # closed, happy eye
            c.set_source_rgb(*INK); c.set_line_width(4)
            c.arc(x + sx, y + 3, 9, math.pi * 1.15, math.pi * 1.85); c.stroke()
            c.set_line_width(2.6); c.move_to(x + sx + 8, y - 4); c.line_to(x + sx + 15, y - 10); c.stroke()
            continue
        r = 14 if big else 11.5
        ellipse(k, x + sx, y, r, r, (1, 1, 1), seed + sx, shadow=False, lw=2)
        px_, py_ = x + sx + lx * 4, y + ly * 4
        pr = 3.6 if kind == "horrified" else 5.4         # horrified: shrunken pupils
        ellipse(k, px_, py_, pr, pr, INK, seed + sx + 1, shadow=False, outline=False)
        c.set_source_rgb(1, 1, 1); c.arc(px_ + 1.8, py_ - 2, 1.6, 0, 2 * math.pi); c.fill()    # catchlight
        if kind in ("knowing", "flirty", "unimpressed"):  # half-lidded
            c.save(); c.rectangle(x + sx - 16, y - 17, 32, 16); c.clip()
            ellipse(k, x + sx, y, r + 3, r + 3, SKIN, seed + sx + 2, shadow=False, outline=False)
            c.restore()
            c.set_source_rgb(*INK); c.set_line_width(3.5)
            c.move_to(x + sx - 11, y - 1); c.line_to(x + sx + 11, y - 1); c.stroke()
        o = -1 if sx < 0 else 1
        if kind not in ("knowing", "flirty", "unimpressed"):  # bold upper liner over the top of the eye
            c.set_source_rgb(*INK); c.set_line_width(4.2); c.set_line_cap(1)
            a0, a1 = (1.08 * math.pi, 1.95 * math.pi) if o > 0 else (1.05 * math.pi, 1.92 * math.pi)
            c.arc(x + sx, y + 1, r + 0.5, a0, a1); c.stroke()
        c.set_source_rgb(*INK); c.set_line_width(3.4)    # winged liner at the outer corner
        lid = kind in ("knowing", "flirty", "unimpressed")
        wy = y - 1 if lid else y - 3
        c.move_to(x + sx + o * (r - 1), wy); c.line_to(x + sx + o * (r + 7), wy - 6); c.stroke()
        c.set_line_width(2.4)                            # two short lashes along the lid
        for ax, ln in ((5, 3.5), (9, 3.5)):
            ay = (y - 1) if lid else (y - math.sqrt(max(0, r * r - ax * ax)))
            c.move_to(x + sx + o * ax, ay); c.line_to(x + sx + o * (ax + 2.5), ay - ln); c.stroke()
    c.set_source_rgb(*INK); c.set_line_width(4); c.set_line_cap(1)
    brows = {   # (left start y, left end y, right start y, right end y), relative to the eye line
        "neutral": (-18, -21, -21, -18), "curious": (-24, -27, -27, -24), "eyebrow": (-15, -15, -36, -28),
        "smile": (-19, -22, -22, -19), "surprised": (-28, -31, -31, -28), "knowing": (-16, -18, -18, -16),
        "wink": (-21, -24, -18, -16), "flirty": (-22, -26, -26, -22),
        "horrified": (-24, -42, -42, -24),   # inner ends up: alarm
        "unimpressed": (-16, -16, -34, -27),  # lowered lids + one brow up + flat closed mouth (before horrified)
        "closed": (-17, -17, -24, -20),       # the resigned blink: brow drops back down
    }[kind]
    c.move_to(x - 27, y + brows[0]); c.curve_to(x - 20, y + brows[1] - 3, x - 14, y + brows[1] - 3, x - 8, y + brows[1]); c.stroke()
    c.move_to(x + 8, y + brows[2]); c.curve_to(x + 14, y + brows[2] - 3, x + 20, y + brows[3] - 3, x + 27, y + brows[3]); c.stroke()
    my = y + 29
    if kind == "horrified":                               # open grimace: teeth showing, red lips
        c.save(); c.translate(x, my + 2)                 # wide, flat grimace: clenched teeth
        c.move_to(-16, -6); c.line_to(16, -6); c.curve_to(18, -6, 18, 7, 14, 7); c.line_to(-14, 7)
        c.curve_to(-18, 7, -18, -6, -16, -6); c.close_path()
        c.set_source_rgb(1, 1, 1); c.fill_preserve()
        c.set_source_rgb(*RED); c.set_line_width(4.2); c.stroke()
        c.set_source_rgb(*INK); c.set_line_width(1.4)
        c.move_to(-15, 0.5); c.line_to(15, 0.5); c.stroke()
        for tx in (-8, 0, 8):
            c.move_to(tx, -6); c.line_to(tx, 7); c.stroke()
        c.restore()
    elif kind in ("curious", "surprised"):
        ellipse(k, x, my, 6 if kind == "curious" else 8, 7 if kind == "curious" else 10, (0.45, 0.06, 0.08), seed + 5,
                shadow=False, lw=2)
        c.set_source_rgb(*RED); c.set_line_width(3.2)
        c.arc(x, my, (6 if kind == "curious" else 8) + 1.5, 0, 2 * math.pi); c.stroke()
    elif kind in ("smile", "wink", "flirty"):
        c.set_source_rgb(*RED); c.set_line_width(7)
        c.arc(x, my - 9, 12.5, 0.22 * math.pi, 0.78 * math.pi); c.stroke()
        c.set_source_rgb(1, 1, 1); c.arc(x - 3, my + 2, 1.4, 0, 2 * math.pi); c.fill()            # gloss
    elif kind == "knowing":
        c.set_source_rgb(*RED); c.set_line_width(7)
        c.move_to(x - 11, my + 1); c.curve_to(x - 2, my + 4, x + 6, my + 2, x + 13, my - 4); c.stroke()
        c.set_source_rgb(1, 1, 1); c.arc(x - 2, my + 1, 1.4, 0, 2 * math.pi); c.fill()
    else:                                             # closed red lips, level (eyebrow: a touch to one side)
        dx = 3 if kind in ("eyebrow", "unimpressed") else 0
        lips(k, x + dx, my)


def lips(k, x, my, w=13):
    """Fuller closed lips: upper lip with a cupid's bow, rounder lower lip, a dark parting line, gloss."""
    c = k.c
    c.move_to(x - w, my)
    c.curve_to(x - w * 0.6, my - 6, x - w * 0.25, my - 7, x, my - 4)         # cupid's bow
    c.curve_to(x + w * 0.25, my - 7, x + w * 0.6, my - 6, x + w, my)
    c.curve_to(x + w * 0.55, my + 8, x - w * 0.55, my + 8, x - w, my)
    c.close_path()
    c.set_source_rgb(*RED); c.fill_preserve()
    c.set_source_rgb(*RED_DARK); c.set_line_width(1.4); c.stroke()
    c.set_source_rgb(*RED_DARK); c.set_line_width(1.8)
    c.move_to(x - w + 1, my); c.curve_to(x - 4, my + 1.5, x + 4, my + 1.5, x + w - 1, my); c.stroke()
    c.set_source_rgb(1, 1, 1)
    c.save(); c.translate(x - 3, my + 3.6); c.scale(3, 1.2); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()


BADGE_HOOK = None   # callable(k, body_top, seed); None = the v2 sheet badge


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
    back = [(-52 + lgx, hy - 30), (-72 + lgx * 1.4, body_top + 30), (-66 + lgx * 1.8, body_top + 96 + lgy),
            (-46 + lgx * 1.8, body_top + 108 + lgy), (-18 + lgx * 1.8, body_top + 102 + lgy),
            (18 + lgx * 1.8, body_top + 102 + lgy), (46 + lgx * 1.8, body_top + 108 + lgy),
            (66 + lgx * 1.8, body_top + 96 + lgy), (72 + lgx * 1.4, body_top + 30), (52 + lgx, hy - 30)]
    cut(k, back, HAIR, lw=2.2)
    cut(k, [(-40 + lgx, hy + 10), (-50 + lgx * 1.5, body_top + 80 + lgy), (-24 + lgx * 1.7, body_top + 96 + lgy),
            (24 + lgx * 1.7, body_top + 96 + lgy), (50 + lgx * 1.5, body_top + 80 + lgy), (40 + lgx, hy + 10)],
        HAIR_SHADE, shadow=False, outline=False)          # darker under-layer: depth and volume
    # legs, boots, skirt, blouse
    for sx in (-15, 15):
        rect(k, sx - 7, -100, 14, 90, TIGHTS, seed + 30 + sx, shadow=False, lw=1.8)
        rect(k, sx - 11 + (sx > 0) * 4, -16, 22, 16, BOOTS, seed + 32 + sx, shadow=False, lw=1.8)
    skirt = [(-40, body_top + 106), (40, body_top + 106), (46, -96), (-46, -96)]   # v2: above the knee
    cut(k, skirt, SKIRT)
    blouse = [(-39, body_top), (39, body_top), (42, body_top + 112), (-42, body_top + 112)]
    cut(k, blouse, BLOUSE)
    # wrap blouse: crossover neckline (a modest V of skin), the right panel over the left, a soft shade fold
    cut(k, [(-14, body_top), (14, body_top), (0, body_top + 30)], SKIN, shadow=False, lw=1.8)
    cut(k, [(14, body_top), (39, body_top), (42, body_top + 98), (-20, body_top + 98), (6, body_top + 40)],
        BLOUSE, shadow=False, lw=2)
    c.set_source_rgb(*BLOUSE_SHADE); c.set_line_width(2.4)
    c.move_to(-30, body_top + 40); c.curve_to(-26, body_top + 62, -28, body_top + 80, -24, body_top + 96); c.stroke()
    # thin belt with a gold buckle at the waist
    rect(k, -42, body_top + 98, 84, 10, BELT, seed + 45, shadow=False, lw=1.6)
    rect(k, -8, body_top + 96, 16, 14, GOLD, seed + 46, shadow=False, lw=1.6)
    c.set_source_rgb(*BELT); c.rectangle(-4, body_top + 100, 8, 6); c.fill()
    if badge and BADGE_HOOK is not None:                 # optional custom badge (set by a film module)
        BADGE_HOOK(k, body_top, seed)
    elif badge:
        rect(k, 4, body_top + 34, 38, 22, (1, 1, 1), seed + 40, shadow=False, lw=1.6)
        c.set_source_rgb(*brand.GREEN); c.rectangle(7, body_top + 36, 32, 3.5); c.fill()
        text(k, "SOFÍA", 23, body_top + 47, 10.5, INK)
    a = POSES.get(pose) or kit.ARM_POSES[pose]
    if folder == "tuck":                                 # under the left arm, against the body
        rect(k, -58, body_top + 26, 16, 82, FOLDER, seed + 50, shadow=False, lw=1.8)
    hands = [_arm(k, -40, body_top + 14, a[0], a[1], seed + 9), _arm(k, 40, body_top + 14, a[2], a[3], seed + 11, ln=40 if pose == "twirl" else 48)]
    if pose == "finger":                                 # the raised index finger
        fx, fy = hands[1]
        c.set_line_cap(1)
        c.set_source_rgb(*INK); c.set_line_width(8.5); c.move_to(fx + 1, fy - 4); c.line_to(fx + 3, fy - 21); c.stroke()
        c.set_source_rgb(*SKIN); c.set_line_width(5.5); c.move_to(fx + 1, fy - 4); c.line_to(fx + 3, fy - 21); c.stroke()
        c.set_source_rgb(*RED); c.arc(fx + 3, fy - 22, 2.2, 0, 2 * math.pi); c.fill()
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
    crown = [(math.cos(a) * 58, hy - 16 + math.sin(a) * 50) for a in
             [math.pi * (1.05 + 0.9 * i / 11) for i in range(12)]]                 # rounded, fuller crown
    cut(k, crown + [(54, hy - 22), (24, hy - 40), (-26, hy - 34), (-56, hy - 22)], HAIR, shadow=False, lw=2)
    c.set_source_rgb(*INK); c.set_line_width(2)                                  # deep side part on her left
    c.move_to(-22, hy - 64); c.curve_to(-26, hy - 54, -30, hy - 44, -26, hy - 34); c.stroke()
    c.set_source_rgb(*HAIR_SHINE); c.set_line_width(4.5); c.set_line_cap(1)  # shine streak
    c.move_to(-34, hy - 48); c.curve_to(-18, hy - 56, 2, hy - 56, 18, hy - 50); c.stroke()
    for sx in (-1, 1):                                   # face-framing locks down to the shoulders
        lx0 = sx * 50
        cut(k, [(lx0 - 8 * sx, hy - 20), (lx0 + 12 * sx, hy - 24), (lx0 + 17 * sx + lgx * 0.6, hy + 56 + lgy),
                (lx0 + 6 * sx + lgx * 0.6, hy + 70 + lgy), (lx0 - 6 * sx + lgx * 0.6, hy + 62 + lgy)],
            HAIR, shadow=False, lw=2)                    # fuller locks with a curled end
    for sx in (-1, 1):                                   # gold hoops below the locks, swinging with lag
        hx0, hy0 = sx * 48 + lgx * 0.8, hy + 26 + HOOP_R + abs(lgx) * 0.2
        c.set_source_rgb(*INK); c.set_line_width(8.2); c.arc(hx0, hy0, HOOP_R, 0, 2 * math.pi); c.stroke()
        c.set_source_rgb(*GOLD); c.set_line_width(5.4); c.arc(hx0, hy0, HOOP_R, 0, 2 * math.pi); c.stroke()
        c.set_source_rgb(*GOLD_LIGHT); c.set_line_width(2)
        c.arc(hx0, hy0, HOOP_R, 1.15 * math.pi, 1.55 * math.pi); c.stroke()
    face(k, 0, hy + 4, face_kind, look, seed + 60)
    if pose == "twirl":                                 # the twirling hand sits in front of her hair
        hx2, hy2 = hands[1]
        c.set_source_rgb(*INK); c.set_line_width(2.4)
        c.arc(hx2 - 4, hy2 + 12, 7, 0.2, 5.2); c.stroke()
        ellipse(k, hx2, hy2, 10, 10, SKIN, seed + 54, shadow=False, lw=2)
        ellipse(k, hx2 - 5, hy2 + 5, 3.2, 3.2, RED, seed + 55, shadow=False, outline=False)
    c.restore()
    return {"head": (x, feet + hy * s), "hands": [(x + hx * s, feet + hyy * s) for hx, hyy in hands], "folder": fbox}
