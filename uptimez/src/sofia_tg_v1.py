"""SOFÍA, Thanksgiving film ("Raises for Everyone"), v1. Her office look carried forward with the Christmas
polish (sofia_xmas.py v3 figure: soft bust, narrow belted waist, hips, shaped legs, heels), plus:
- the teal wrap blouse and black skirt of her v4 office look, reshaped to that figure;
- one side braid over her right shoulder (screen left) tied with a rust bow;
- dangling gold star earrings on short chains that swing with `lag` and sparkle with the boil;
- an autumn plaid scarf (rust, mustard, cream) knotted at the neck, tails on her left so the badge stays clear.
New faces: "tiny" (the half-second smile at the verdict: eyes open, brows relaxed, one lip corner up).
New poses: "aside" (both hands low, for the lean to Pam), "correct" (right palm open toward Don).
`lean` tilts the whole figure about the feet (degrees, + = toward screen right).
sofia_v4.py and sofia_xmas*.py are untouched.
Usage: sofia(k, x, feet, s, pose, face_kind, look, lag, lean=0, ear="star", hair="braid")"""
import math
import kit
import brand
import sofia_v4 as sf
import sofia_xmas as sx
from kit import INK, cut, rect, ellipse, rough_ellipse_pts, text
from sofia_v4 import SKIN, HAIR, HAIR_SHINE, HAIR_SHADE, RED, GOLD, GOLD_LIGHT, BLOUSE, BLOUSE_SHADE, BELT, H

SKIRT = sf.SKIRT
TIGHTS = sf.TIGHTS
PUMPS = (0.08, 0.08, 0.09)
RUST = (0.72, 0.32, 0.13)
RUST_DARK = (0.50, 0.20, 0.08)
MUSTARD = (0.90, 0.67, 0.20)
CREAM = (0.98, 0.93, 0.80)

POSES = dict(sf.POSES)
POSES.update({
    "aside": (-10, 30, 14, -34),        # hands low in front, relaxed: the quiet lean to Pam
    "correct": (-10, 20, 46, -78),      # right forearm up, palm open toward Don: "She refused."
    "fold": (-50, 110, 50, -110),       # arms folded under the scarf
})


def star(c, x, y, r, rot=0.0):
    c.move_to(x + math.cos(rot - math.pi / 2) * r, y + math.sin(rot - math.pi / 2) * r)
    for i in range(1, 10):
        a_ = rot - math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        c.line_to(x + math.cos(a_) * rr, y + math.sin(a_) * rr)
    c.close_path()


def star_earring(k, ax, ay, sw, seed, side, boil):
    """Gold five-point star on a short chain; swings by `sw`, twinkles with the boil."""
    c = k.c
    bx, by = ax + sw, ay + 24 - abs(sw) * 0.15
    c.set_source_rgb(*INK); c.set_line_width(2.2); c.set_line_cap(1)
    c.move_to(ax, ay); c.line_to(bx, by - 10); c.stroke()
    ellipse(k, ax, ay, 2.6, 2.6, GOLD, seed, shadow=False, lw=1.2)
    rot = sw * 0.03
    star(c, bx, by, 12.5, rot)
    c.set_source_rgb(*GOLD); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(2.2); c.stroke()
    star(c, bx - 1.5, by - 1.5, 6, rot)
    c.set_source_rgb(*GOLD_LIGHT); c.fill()
    c.set_source_rgb(1, 1, 1); c.arc(bx - 3.5, by - 5, 1.8, 0, 2 * math.pi); c.fill()
    sx.sparkle(c, bx + side * 14, by - 10, 7.5 if (boil + (side > 0)) % 2 else 5)


def _plaid(k, pts, seed):
    """Fill a cutout with the autumn plaid: rust ground, mustard bands, thin cream lines."""
    c = k.c
    cut(k, pts, RUST, shadow=False, lw=2)
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    c.save()
    c.move_to(*pts[0])
    for p in pts[1:]:
        c.line_to(*p)
    c.close_path(); c.clip()
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    c.set_source_rgba(*MUSTARD, 0.85)
    for gx in range(int(x0) - 40, int(x1) + 40, 16):
        c.rectangle(gx, y0 - 2, 5, y1 - y0 + 4)
    for gy in range(int(y0) - 4, int(y1) + 4, 16):
        c.rectangle(x0 - 2, gy, x1 - x0 + 4, 5)
    c.fill()
    c.set_source_rgb(*CREAM); c.set_line_width(1.2)
    for gx in range(int(x0) - 32, int(x1) + 40, 16):
        c.move_to(gx, y0 - 2); c.line_to(gx, y1 + 2)
    for gy in range(int(y0) + 4, int(y1) + 4, 16):
        c.move_to(x0 - 2, gy); c.line_to(x1 + 2, gy)
    c.stroke()
    c.restore()
    c.set_source_rgb(*INK); c.set_line_width(2)          # re-ink the edge over the pattern
    c.move_to(*pts[0])
    for p in pts[1:]:
        c.line_to(*p)
    c.close_path(); c.stroke()


def scarf(k, body_top, lag, seed):
    lgx, lgy = lag
    # tails first (behind the knot), on her left = screen right? No: braid is screen left, badge screen right;
    # tails hang just left of centre, between the two.
    _plaid(k, [(-24, body_top + 8), (-8, body_top + 10), (-10 + lgx * 0.5, body_top + 74 + lgy),
               (-26 + lgx * 0.5, body_top + 76 + lgy)], seed)
    _plaid(k, [(-12, body_top + 10), (4, body_top + 8), (4 + lgx * 0.7, body_top + 62 + lgy),
               (-10 + lgx * 0.7, body_top + 66 + lgy)], seed + 1)
    c = k.c
    c.set_source_rgb(*CREAM); c.set_line_width(2)          # fringe
    for (fx, fy) in ((-25 + lgx * 0.5, body_top + 76 + lgy), (-9 + lgx * 0.7, body_top + 65 + lgy)):
        for i in range(5):
            c.move_to(fx + i * 3.6, fy); c.line_to(fx + i * 3.6, fy + 6)
    c.stroke()
    # wrap round the neck
    _plaid(k, [(-34, body_top - 8), (34, body_top - 8), (38, body_top + 6), (20, body_top + 16), (-20, body_top + 16),
               (-38, body_top + 6)], seed + 2)
    # knot
    _plaid(k, [(-14, body_top + 4), (6, body_top + 2), (10, body_top + 18), (-10, body_top + 22)], seed + 3)


def face(k, x, y, kind="neutral", look=(0, 0), seed=0):
    """sofia_xmas.face plus "tiny": a half-second smile she can't hold back. Eyes open, brows relaxed,
    closed lips with only her left corner (screen right) lifted, a small dimple."""
    if kind != "tiny":
        return sx.face(k, x, y, kind, look, seed)
    c = k.c
    sf.face(k, x, y, "neutral", look, seed)
    my = y + 29
    ellipse(k, x, my, 17, 10, SKIN, seed + 9, shadow=False, outline=False)       # erase the level lips
    c.save(); c.translate(x - 12, my + 1); c.rotate(-0.16)
    sf.lips(k, 12, 0)
    c.restore()
    c.set_source_rgb(*INK); c.set_line_width(1.8); c.set_line_cap(1)
    c.arc(x + 16, my - 5, 3.2, -0.3 * math.pi, 0.25 * math.pi); c.stroke()       # dimple


BADGE_HOOK = None


def sofia(k, x, feet, s=1.0, pose="stand", face_kind="neutral", look=(0, 0), lag=(0, 0), seed=7, badge=True,
          lean=0.0, ear="star", hair="braid", folder=None):
    """Returns {"head", "hands"} in canvas coordinates (lean not applied to the returned points)."""
    c = k.c
    c.save(); c.translate(x, feet); c.rotate(math.radians(lean)); c.scale(s, s)
    body_top = -300 * H + 78
    hy = body_top - 44
    lgx, lgy = lag
    if hair == "braid":
        back = [(-52, hy - 30), (-60, hy + 40), (-40, body_top + 14), (40, body_top + 14), (60, hy + 40), (52, hy - 30)]
    else:
        back = [(-52 + lgx, hy - 30), (-72 + lgx * 1.4, body_top + 30), (-66 + lgx * 1.8, body_top + 96 + lgy),
                (-46 + lgx * 1.8, body_top + 108 + lgy), (46 + lgx * 1.8, body_top + 108 + lgy),
                (66 + lgx * 1.8, body_top + 96 + lgy), (72 + lgx * 1.4, body_top + 30), (52 + lgx, hy - 30)]
    cut(k, back, HAIR, lw=2.2)
    # legs: shaped, dark tights, black pumps (Christmas figure)
    for sx_ in (-14, 14):
        o = 1 if sx_ > 0 else -1
        cut(k, [(sx_ - 8.5, -100), (sx_ + 8.5, -100), (sx_ + 6, -60), (sx_ + 7.5, -42), (sx_ + 4.5, -10), (sx_ - 4.5, -10),
                (sx_ - 7.5, -42), (sx_ - 6, -60)], TIGHTS, shadow=False, lw=1.8)
        c.set_source_rgb(*INK); c.set_line_width(3.2); c.set_line_cap(1)
        c.move_to(sx_ - o * 4, -9); c.line_to(sx_ - o * 5, 0); c.stroke()
        cut(k, [(sx_ - 6, -13), (sx_ + 6, -13), (sx_ + 6 + o * 11, 0), (sx_ - 1 + o * 3, 0), (sx_ - 6, -7)], PUMPS,
            shadow=False, lw=1.8)
    # skirt: black, from the narrow waist over the hips, above the knee
    cut(k, [(-29, body_top + 102), (29, body_top + 102), (45, body_top + 116), (50, -92), (-50, -92),
            (-45, body_top + 116)], SKIRT)
    # wrap blouse on the hourglass top
    top = [(-37, body_top), (37, body_top), (41, body_top + 40), (29, body_top + 102), (-29, body_top + 102),
           (-41, body_top + 40)]
    cut(k, top, BLOUSE)
    cut(k, [(14, body_top), (37, body_top), (41, body_top + 40), (29, body_top + 98), (-22, body_top + 98),
            (4, body_top + 40)], BLOUSE, shadow=False, lw=2)                # right panel crossing over
    c.set_source_rgb(*BLOUSE_SHADE); c.set_line_width(2.2); c.set_line_cap(1)
    c.arc(-18, body_top + 36, 15, 0.12 * math.pi, 0.80 * math.pi); c.stroke()
    c.arc(18, body_top + 36, 15, 0.20 * math.pi, 0.88 * math.pi); c.stroke()
    c.move_to(-27, body_top + 64); c.curve_to(-22, body_top + 78, -22, body_top + 88, -24, body_top + 98); c.stroke()
    rect(k, -31, body_top + 96, 62, 10, BELT, seed + 45, shadow=False, lw=1.6)
    rect(k, -8, body_top + 94, 16, 14, GOLD, seed + 46, shadow=False, lw=1.6)
    c.set_source_rgb(*BELT); c.rectangle(-4, body_top + 98, 8, 6); c.fill()
    if badge and BADGE_HOOK is not None:
        BADGE_HOOK(k, body_top, seed)
    elif badge:
        rect(k, 8, body_top + 50, 32, 20, (1, 1, 1), seed + 40, shadow=False, lw=1.6)
        c.set_source_rgb(*brand.GREEN); c.rectangle(11, body_top + 52, 26, 3.5); c.fill()
        text(k, "SOFÍA", 24, body_top + 62, 9, INK)
    scarf(k, body_top, lag, seed + 120)
    a = POSES.get(pose) or kit.ARM_POSES[pose]
    hands = [sf._arm(k, -39, body_top + 14, a[0], a[1], seed + 9, w=15),
             sf._arm(k, 39, body_top + 14, a[2], a[3], seed + 11, w=15)]
    if pose == "correct":                                 # open palm: fingers fanned
        hx2, hy2 = hands[1]
        for i, ang in enumerate((-0.9, -0.45, 0.0, 0.45)):
            fx, fy = hx2 + math.sin(ang) * 11, hy2 - math.cos(ang) * 11
            c.set_source_rgb(*INK); c.set_line_width(7); c.set_line_cap(1)
            c.move_to(hx2, hy2); c.line_to(fx, fy); c.stroke()
            c.set_source_rgb(*SKIN); c.set_line_width(4.2); c.move_to(hx2, hy2); c.line_to(fx, fy); c.stroke()
        ellipse(k, hx2, hy2, 8.5, 8.5, SKIN, seed + 56, shadow=False, lw=2)
    # head, front hair
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
    c.move_to(-34, hy - 48); c.curve_to(-18, hy - 56, 2, hy - 56, 18, hy - 50); c.stroke()
    for sgn in (-1, 1):
        lx0 = sgn * 50
        if hair == "braid":
            cut(k, [(lx0 - 8 * sgn, hy - 20), (lx0 + 12 * sgn, hy - 24), (lx0 + 13 * sgn, hy + 18), (lx0 + 2 * sgn, hy + 30),
                    (lx0 - 6 * sgn, hy + 22)], HAIR, shadow=False, lw=2)
        else:
            cut(k, [(lx0 - 8 * sgn, hy - 20), (lx0 + 12 * sgn, hy - 24), (lx0 + 17 * sgn + lgx * 0.6, hy + 56 + lgy),
                    (lx0 + 6 * sgn + lgx * 0.6, hy + 70 + lgy), (lx0 - 6 * sgn + lgx * 0.6, hy + 62 + lgy)],
                HAIR, shadow=False, lw=2)
    if hair == "braid":                                   # one thick braid over her right shoulder, rust bow
        n = 6                                             # one tapered rope, plaits drawn as chevrons
        pts = [(-50 + 10 * (i / n) + lgx * (0.3 + i / n), hy + 26 + i * 19 + lgy * (i / n)) for i in range(n + 1)]
        L = [(px - (15 - 4 * i / n), py) for i, (px, py) in enumerate(pts)]
        R = [(px + (15 - 4 * i / n), py) for i, (px, py) in enumerate(pts)]
        cut(k, L + R[::-1], HAIR, shadow=False, lw=2.2)
        for i, (px, py) in enumerate(pts[:-1]):
            w_ = 15 - 4 * i / n
            c.set_source_rgb(*HAIR_SHADE); c.set_line_width(2.4); c.set_line_cap(1)
            c.move_to(px - w_ + 2, py + 2); c.curve_to(px - 3, py + 8, px, py + 12, px + 2, py + 17); c.stroke()
            c.move_to(px + w_ - 2, py + 10); c.curve_to(px + 3, py + 13, px + 1, py + 16, px - 1, py + 20); c.stroke()
            c.set_source_rgb(*HAIR_SHINE); c.set_line_width(2.6)
            c.move_to(px - w_ + 5, py + 6); c.line_to(px - w_ + 8, py + 11); c.stroke()
        ex_, ey_ = -40 + lgx * 1.3, hy + 34 + n * 19 - 4 + lgy
        cut(k, [(ex_ - 7, ey_), (ex_ + 7, ey_), (ex_ + 10, ey_ + 20), (ex_, ey_ + 26), (ex_ - 10, ey_ + 20)], HAIR,
            shadow=False, lw=2)
        cut(k, [(ex_ - 14, ey_ - 8), (ex_, ey_ - 2), (ex_ + 14, ey_ - 8), (ex_ + 14, ey_ + 6), (ex_, ey_), (ex_ - 14, ey_ + 6)],
            RUST, shadow=False, lw=1.8)
        ellipse(k, ex_, ey_ - 1, 3.4, 3.4, RUST_DARK, seed + 130, shadow=False, lw=1.4)
    for sgn in (-1, 1):
        if ear == "star":
            star_earring(k, sgn * 48, hy + 24, lgx * 1.3, seed + 70 + sgn, sgn, k.boil)
        else:
            hx0, hy0 = sgn * 48 + lgx * 0.8, hy + 26 + sf.HOOP_R + abs(lgx) * 0.2
            c.set_source_rgb(*INK); c.set_line_width(8.2); c.arc(hx0, hy0, sf.HOOP_R, 0, 2 * math.pi); c.stroke()
            c.set_source_rgb(*GOLD); c.set_line_width(5.4); c.arc(hx0, hy0, sf.HOOP_R, 0, 2 * math.pi); c.stroke()
    face(k, 0, hy + 4, face_kind, look, seed + 60)
    c.restore()
    return {"head": (x, feet + hy * s), "hands": [(x + hx * s, feet + hyy * s) for hx, hyy in hands]}
