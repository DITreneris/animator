"""v2 (sofia_xmas_v1.py = v1, kept): a more feminine figure: hourglass dress (soft bust, narrow belted
waist, hips flaring into the skirt), shaped legs, stiletto pumps, slimmer arms. Face, hair and height unchanged.

v1 notes: SOFÍA, Christmas special ("Happy Compliance"): the v4 face, hair and hoops (sofia_v4.py, untouched) in a
glamorous nurse costume: white dress with red trim and a red belt, short sleeves, a small cap with a red
heart (not a red cross), stethoscope, white tights, red heels. Adds a "furious" face and ornament poses.
Usage: sofia(k, x, feet, s, pose, face_kind, look, lag, orn=...)  orn: None | "two" | "right" | "none"."""
import math
import kit
import brand
import sofia_v4 as sf
from kit import INK, cut, rect, ellipse, rough_ellipse_pts, text
from sofia_v4 import SKIN, HAIR, HAIR_SHINE, HAIR_SHADE, RED, RED_DARK, GOLD, GOLD_LIGHT, HOOP_R, H

WHITE = (0.99, 0.98, 0.96)
WHITE_SHADE = (0.86, 0.87, 0.90)
TIGHTS = (0.97, 0.94, 0.92)
STETH = (0.22, 0.25, 0.32)
ORN_RED = (0.84, 0.08, 0.12)
ORN_DARK = (0.55, 0.03, 0.08)

POSES = dict(sf.POSES)
POSES.update({
    "hold2": (-22, 82, 22, -82),       # both hands in front at waist height, an ornament hanging from each
    "hang": (-8, 0, 140, 25),          # right hand up to the tree
    "give": (-8, 0, 78, 12),           # right arm out: pressing an ornament into Pam's hand
    "fists": (-12, 10, 12, -10),       # arms straight down, stiff
})


def ornament(k, x, y, r=16, seed=0, col=ORN_RED):
    """A big glossy bauble with a gold cap and loop: the planted prop."""
    c = k.c
    ellipse(k, x, y, r, r, col, seed + 300, shadow=False, lw=2.4)
    c.save(); c.arc(x, y, r - 1.5, 0, 2 * math.pi); c.clip()
    c.set_source_rgb(*ORN_DARK); c.arc(x + r * 0.55, y + r * 0.6, r * 0.9, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(*col); c.arc(x - r * 0.15, y - r * 0.15, r * 0.95, 0, 2 * math.pi); c.fill()
    c.restore()
    c.set_source_rgb(1, 1, 1)
    c.save(); c.translate(x - r * 0.38, y - r * 0.42); c.rotate(-0.6); c.scale(r * 0.26, r * 0.14)
    c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
    rect(k, x - r * 0.28, y - r - r * 0.3, r * 0.56, r * 0.36, GOLD, seed + 301, shadow=False, lw=1.6)
    c.set_source_rgb(*INK); c.set_line_width(1.8); c.arc(x, y - r - r * 0.42, r * 0.17, 0, 2 * math.pi); c.stroke()


def _arm(k, sx, sy, a1, a2, seed, ln=48, w=17):
    """Bare arm with a short white sleeve and a red cuff; red nail tip."""
    d = lambda a: (math.sin(math.radians(a)), math.cos(math.radians(a)))
    ex, ey = sx + d(a1)[0] * ln, sy + d(a1)[1] * ln
    hx, hy = ex + d(a1 + a2)[0] * ln, ey + d(a1 + a2)[1] * ln
    for (ax, ay, bx, by) in ((sx, sy, ex, ey), (ex, ey, hx, hy)):
        ang = math.atan2(by - ay, bx - ax)
        nx, ny = -math.sin(ang) * w / 2, math.cos(ang) * w / 2
        cut(k, [(ax + nx, ay + ny), (bx + nx, by + ny), (bx - nx, by - ny), (ax - nx, ay - ny)], SKIN, shadow=False, lw=2)
    ang = math.atan2(ey - sy, ex - sx)
    ux, uy = math.cos(ang), math.sin(ang)
    nx, ny = -uy * (w / 2 + 2.5), ux * (w / 2 + 2.5)
    q = lambda t: (sx + ux * ln * t, sy + uy * ln * t)
    (p0x, p0y), (p1x, p1y), (p2x, p2y) = q(-0.08), q(0.42), q(0.52)
    cut(k, [(p0x + nx, p0y + ny), (p1x + nx, p1y + ny), (p1x - nx, p1y - ny), (p0x - nx, p0y - ny)], WHITE, shadow=False, lw=2)
    cut(k, [(p1x + nx, p1y + ny), (p2x + nx, p2y + ny), (p2x - nx, p2y - ny), (p1x - nx, p1y - ny)], RED, shadow=False, lw=1.8)
    ellipse(k, hx, hy, w * 0.6, w * 0.6, SKIN, seed, shadow=False, lw=2)
    fa = math.atan2(hy - ey, hx - ex)
    ellipse(k, hx + math.cos(fa) * 7, hy + math.sin(fa) * 7, 3.2, 3.2, RED, seed + 1, shadow=False, outline=False)
    return hx, hy


def face(k, x, y, kind="neutral", look=(0, 0), seed=0):
    """sofia_v4.face plus "furious": narrowed eyes under brows driven hard down to the middle, tight down-turned lips."""
    if kind != "furious":
        return sf.face(k, x, y, kind, look, seed)
    c = k.c
    lx, ly = look
    r = 11.5
    for sx in (-17, 17):
        o = -1 if sx < 0 else 1
        ellipse(k, x + sx, y, r, r, (1, 1, 1), seed + sx, shadow=False, lw=2)
        px_, py_ = x + sx + lx * 4, y + 1.5 + ly * 3
        ellipse(k, px_, py_, 4.6, 4.6, INK, seed + sx + 1, shadow=False, outline=False)
        c.set_source_rgb(1, 1, 1); c.arc(px_ + 1.6, py_ - 1.6, 1.3, 0, 2 * math.pi); c.fill()
        c.save(); c.arc(x + sx, y, r + 1.5, 0, 2 * math.pi); c.clip()      # angry lid: a skin wedge, low at the nose side
        c.move_to(x + sx - o * 16, y - 16); c.line_to(x + sx + o * 16, y - 16)
        c.line_to(x + sx + o * 16, y - 7); c.line_to(x + sx - o * 16, y + 1); c.close_path()
        c.set_source_rgb(*SKIN); c.fill()
        c.restore()
        c.set_source_rgb(*INK); c.set_line_width(4); c.set_line_cap(1)
        c.move_to(x + sx - o * 11, y); c.line_to(x + sx + o * 11.5, y - 6); c.stroke()
        c.set_line_width(3.4); c.move_to(x + sx + o * 11, y - 6); c.line_to(x + sx + o * 18, y - 12); c.stroke()   # wing
        c.set_line_width(2.4)
        for ax in (4, 8):
            ay = y - 3 - ax * 0.3
            c.move_to(x + sx + o * ax, ay); c.line_to(x + sx + o * (ax + 2.5), ay - 3.5); c.stroke()
    c.set_source_rgb(*INK); c.set_line_width(5); c.set_line_cap(1)        # brows: outer ends high, inner ends slammed down
    c.move_to(x - 29, y - 27); c.curve_to(x - 22, y - 26, x - 14, y - 20, x - 6, y - 12); c.stroke()
    c.move_to(x + 29, y - 27); c.curve_to(x + 22, y - 26, x + 14, y - 20, x + 6, y - 12); c.stroke()
    c.set_line_width(1.8)                                               # crease between the brows
    c.move_to(x - 2, y - 17); c.line_to(x - 1, y - 11); c.stroke()
    c.move_to(x + 2, y - 17); c.line_to(x + 1, y - 11); c.stroke()
    my = y + 30                                                          # pressed lips, corners down
    c.move_to(x - 13, my + 4); c.curve_to(x - 7, my - 6, x + 7, my - 6, x + 13, my + 4)
    c.curve_to(x + 6, my + 3, x - 6, my + 3, x - 13, my + 4); c.close_path()
    c.set_source_rgb(*RED); c.fill_preserve(); c.set_source_rgb(*RED_DARK); c.set_line_width(1.6); c.stroke()
    c.set_source_rgb(*RED_DARK); c.set_line_width(1.8)
    c.move_to(x - 11, my + 2.5); c.curve_to(x - 5, my - 2.5, x + 5, my - 2.5, x + 11, my + 2.5); c.stroke()
    c.set_source_rgb(1, 1, 1); c.arc(x - 3, my - 1.5, 1.3, 0, 2 * math.pi); c.fill()


def heart(c, x, y, s):
    c.move_to(x, y + s * 0.9)
    c.curve_to(x - s * 1.5, y - s * 0.2, x - s * 0.7, y - s * 1.2, x, y - s * 0.4)
    c.curve_to(x + s * 0.7, y - s * 1.2, x + s * 1.5, y - s * 0.2, x, y + s * 0.9)
    c.close_path()


BADGE_HOOK = None


def sofia(k, x, feet, s=1.0, pose="stand", face_kind="neutral", look=(0, 0), lag=(0, 0), seed=7, badge=True,
          orn=None, folder=None):
    """Returns {"head", "hands", "orns": [(x, y), ...]} in canvas coordinates. folder is accepted and ignored."""
    c = k.c
    c.save(); c.translate(x, feet); c.scale(s, s)
    body_top = -300 * H + 78
    hy = body_top - 44
    lgx, lgy = lag
    orn = orn if orn is not None else ("two" if pose == "hold2" else ("right" if pose in ("hang", "give") else "none"))
    back = [(-52 + lgx, hy - 30), (-72 + lgx * 1.4, body_top + 30), (-66 + lgx * 1.8, body_top + 96 + lgy),
            (-46 + lgx * 1.8, body_top + 108 + lgy), (-18 + lgx * 1.8, body_top + 102 + lgy),
            (18 + lgx * 1.8, body_top + 102 + lgy), (46 + lgx * 1.8, body_top + 108 + lgy),
            (66 + lgx * 1.8, body_top + 96 + lgy), (72 + lgx * 1.4, body_top + 30), (52 + lgx, hy - 30)]
    cut(k, back, HAIR, lw=2.2)
    cut(k, [(-40 + lgx, hy + 10), (-50 + lgx * 1.5, body_top + 80 + lgy), (-24 + lgx * 1.7, body_top + 96 + lgy),
            (24 + lgx * 1.7, body_top + 96 + lgy), (50 + lgx * 1.5, body_top + 80 + lgy), (40 + lgx, hy + 10)],
        HAIR_SHADE, shadow=False, outline=False)
    # legs: white tights, red heels
    for sx in (-14, 14):                                  # v2: shaped legs (thigh, knee, calf, ankle) and stiletto pumps
        o = 1 if sx > 0 else -1
        cut(k, [(sx - 8.5, -100), (sx + 8.5, -100), (sx + 6, -60), (sx + 7.5, -42), (sx + 4.5, -10), (sx - 4.5, -10),
                (sx - 7.5, -42), (sx - 6, -60)], TIGHTS, shadow=False, lw=1.8)
        c.set_source_rgb(*INK); c.set_line_width(3.2); c.set_line_cap(1)
        c.move_to(sx - o * 4, -9); c.line_to(sx - o * 5, 0); c.stroke()               # heel
        cut(k, [(sx - 6, -13), (sx + 6, -13), (sx + 6 + o * 11, 0), (sx - 1 + o * 3, 0), (sx - 6, -7)], RED,
            shadow=False, lw=1.8)
    # dress: fitted top, belt, flared skirt above the knee, red hem
    # v2: an hourglass line: shoulders, a soft bust, a narrow belted waist, hips flaring into the skirt
    skirt = [(-29, body_top + 102), (29, body_top + 102), (45, body_top + 116), (54, -90), (-54, -90),
             (-45, body_top + 116)]
    cut(k, skirt, WHITE)
    cut(k, [(-52, -102), (52, -102), (54, -90), (-54, -90)], RED, shadow=False, lw=1.8)
    top = [(-37, body_top), (37, body_top), (41, body_top + 40), (29, body_top + 102), (-29, body_top + 102),
           (-41, body_top + 40)]
    cut(k, top, WHITE)
    c.set_source_rgb(*WHITE_SHADE); c.set_line_width(2.2); c.set_line_cap(1)
    c.arc(-18, body_top + 36, 15, 0.12 * math.pi, 0.80 * math.pi); c.stroke()      # soft shaping under the bust
    c.arc(18, body_top + 36, 15, 0.20 * math.pi, 0.88 * math.pi); c.stroke()
    c.move_to(-27, body_top + 64); c.curve_to(-22, body_top + 78, -22, body_top + 88, -24, body_top + 98); c.stroke()
    c.move_to(27, body_top + 64); c.curve_to(22, body_top + 78, 22, body_top + 88, 24, body_top + 98); c.stroke()
    # collar: a modest V with red lapels
    cut(k, [(-13, body_top), (13, body_top), (0, body_top + 26)], SKIN, shadow=False, lw=1.8)
    cut(k, [(-13, body_top), (0, body_top + 26), (-8, body_top + 34), (-27, body_top + 2)], RED, shadow=False, lw=1.8)
    cut(k, [(13, body_top), (0, body_top + 26), (8, body_top + 34), (27, body_top + 2)], RED, shadow=False, lw=1.8)
    for by in (50, 66, 82):                                           # buttons down the front
        ellipse(k, 0, body_top + by, 2.6, 2.6, RED, seed + 43 + by, shadow=False, lw=1.2)
    rect(k, -31, body_top + 96, 62, 11, RED, seed + 45, shadow=False, lw=1.6)
    rect(k, -8, body_top + 94, 16, 15, GOLD, seed + 46, shadow=False, lw=1.6)
    c.set_source_rgb(*RED_DARK); c.rectangle(-4, body_top + 98, 8, 7); c.fill()
    # stethoscope: round the neck, chest piece on her right
    c.set_line_cap(1)
    for col, lw in ((INK, 6.5), (STETH, 3.6)):
        c.set_source_rgb(*col); c.set_line_width(lw)
        c.move_to(-22, body_top + 1); c.curve_to(-26, body_top + 30, -22, body_top + 52, -18, body_top + 60); c.stroke()
        c.move_to(22, body_top + 1); c.curve_to(26, body_top + 26, 24, body_top + 40, 21, body_top + 48); c.stroke()
    ellipse(k, -18, body_top + 64, 6.5, 6.5, (0.80, 0.82, 0.86), seed + 47, shadow=False, lw=1.8)
    if badge and BADGE_HOOK is not None:
        BADGE_HOOK(k, body_top, seed)
    elif badge:
        rect(k, 5, body_top + 52, 34, 20, (1, 1, 1), seed + 40, shadow=False, lw=1.8)
        c.set_source_rgb(*brand.GREEN); c.rectangle(8, body_top + 54, 28, 3.5); c.fill()
        text(k, "SOFÍA", 22, body_top + 64, 9.5, INK)
    a = POSES.get(pose) or kit.ARM_POSES[pose]
    hands = [_arm(k, -39, body_top + 14, a[0], a[1], seed + 9, w=15), _arm(k, 39, body_top + 14, a[2], a[3], seed + 11, w=15)]
    orns = []
    if orn == "two":
        orns = [(hands[0][0] - 9, hands[0][1] + 25), (hands[1][0] + 9, hands[1][1] + 25)]    # dangling by their loops, at hip level
    elif orn == "right":
        hx_, hy_ = hands[1]
        orns = [(hx_ + 4, hy_ + (22 if pose == "hang" else -18))]
    for i, (ox, oy) in enumerate(orns):
        ornament(k, ox, oy, 17, seed + 80 + i)
    if orns:                                                       # fingers over the bauble / on the loop
        for hx_, hy_ in (hands if orn == "two" else hands[1:]):
            ellipse(k, hx_, hy_, 9.5, 9.5, SKIN, seed + 52, shadow=False, lw=2)
            ellipse(k, hx_, hy_ - 6, 3.2, 3.2, RED, seed + 53, shadow=False, outline=False)
    # head, front hair, locks
    ellipse(k, 0, hy, 50, 50, SKIN, seed + 20)
    cap = rough_ellipse_pts(k, 0, hy - 10, 54, 48, seed + 21)
    cap = [q for q in cap if q[1] < hy - 30] + [(53, hy - 24), (30, hy - 40), (0, hy - 44), (-30, hy - 40), (-53, hy - 22)]
    cap.sort(key=lambda q: math.atan2(q[1] - (hy - 10), q[0]))
    cut(k, cap, HAIR, shadow=False, lw=2)
    crown = [(math.cos(a_) * 58, hy - 16 + math.sin(a_) * 50) for a_ in
             [math.pi * (1.05 + 0.9 * i / 11) for i in range(12)]]
    cut(k, crown + [(54, hy - 22), (24, hy - 40), (-26, hy - 34), (-56, hy - 22)], HAIR, shadow=False, lw=2)
    c.set_source_rgb(*INK); c.set_line_width(2)
    c.move_to(-22, hy - 64); c.curve_to(-26, hy - 54, -30, hy - 44, -26, hy - 34); c.stroke()
    c.set_source_rgb(*HAIR_SHINE); c.set_line_width(4.5); c.set_line_cap(1)
    c.move_to(-34, hy - 46); c.curve_to(-18, hy - 53, 2, hy - 53, 18, hy - 47); c.stroke()
    # nurse cap with a red heart, sitting on the crown, tilted a little
    c.save(); c.translate(4, hy - 60); c.rotate(0.06)
    cut(k, [(-30, 6), (-24, -22), (24, -22), (30, 6), (20, 10), (-20, 10)], WHITE, shadow=False, lw=2.2)
    cut(k, [(-30, 6), (30, 6), (20, 12), (-20, 12)], RED, shadow=False, lw=1.6)
    heart(c, 0, -9, 7.5); c.set_source_rgb(*RED); c.fill_preserve()
    c.set_source_rgb(*RED_DARK); c.set_line_width(1.2); c.stroke()
    c.restore()
    for sx in (-1, 1):
        lx0 = sx * 50
        cut(k, [(lx0 - 8 * sx, hy - 20), (lx0 + 12 * sx, hy - 24), (lx0 + 17 * sx + lgx * 0.6, hy + 56 + lgy),
                (lx0 + 6 * sx + lgx * 0.6, hy + 70 + lgy), (lx0 - 6 * sx + lgx * 0.6, hy + 62 + lgy)],
            HAIR, shadow=False, lw=2)
    for sx in (-1, 1):
        hx0, hy0 = sx * 48 + lgx * 0.8, hy + 26 + HOOP_R + abs(lgx) * 0.2
        c.set_source_rgb(*INK); c.set_line_width(8.2); c.arc(hx0, hy0, HOOP_R, 0, 2 * math.pi); c.stroke()
        c.set_source_rgb(*GOLD); c.set_line_width(5.4); c.arc(hx0, hy0, HOOP_R, 0, 2 * math.pi); c.stroke()
        c.set_source_rgb(*GOLD_LIGHT); c.set_line_width(2)
        c.arc(hx0, hy0, HOOP_R, 1.15 * math.pi, 1.55 * math.pi); c.stroke()
    face(k, 0, hy + 4, face_kind, look, seed + 60)
    c.restore()
    return {"head": (x, feet + hy * s), "hands": [(x + hx * s, feet + hyy * s) for hx, hyy in hands],
            "orns": [(x + ox * s, feet + oy * s) for ox, oy in orns]}
