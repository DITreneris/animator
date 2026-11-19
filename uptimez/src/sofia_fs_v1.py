"""SOFIA, "First Search" (episode 10), v1: her January look, developed on its own (the grill of 18 Nov). Every earlier
Sofia (sofia_v4, sofia_ss, sofia_bc, sofia_ob, ...) is untouched; this file draws the whole figure itself on the same
body (sofia_ss's proportions, sofia_v4's arms, face and skin) so the cast still matches.
- WINTER CHIC IN FUCHSIA: a wrap coat-dress with a soft roll collar, the wrap line running from her left shoulder to
  her right hip, the hem just above the knee; the sleeves are the coat's;
- A STATEMENT BELT: wide, black patent, a big square gold buckle, high on the waist: the silhouette;
- KNEE-HIGH BOOTS: black, a slim heel, a soft shine down the shin; dark tights in the gap under the hem;
- A SLEEK HIGH PONYTAIL: the hair pulled back smooth (no side locks), tied high at the crown with a gold cuff; the
  tail falls behind her head to one side and swings with `lag` (its tip travels most), so every turn of her head shows;
- STATEMENT EARRINGS: gold geometric drops (a stud, a hoop-ring, a long open triangle with a bead at its point); they
  swing with `lag` and catch the light;
- A PHONE IN A LUXE CASE: rose gold with a pink inlay (pose "phone"); the tablet (Sofía's, his old thumbprint on it)
  is sofia_ob's tablet in "hold" and "behind" (slid behind her back: "not me");
- no pearls in this film.
Poses: stand, hold (the tablet against her), phone (the phone in her screen-left hand, at her chest), plaster (her
screen-right hand up and out, pressing), behind (both hands behind her back, the tablet hidden), hip.
Faces: every sofia_v4/sofia_tg face (neutral, smile, knowing, flirty, unimpressed, eyebrow, closed, surprised,
curious, tiny, wink).
Usage: sofia(k, x, feet, s, pose, face_kind, look, lag, seed, badge, lean)"""
import math
import kit
import brand
import sofia_v4 as sf
import sofia_ss as ss
import sofia_ob as so
from kit import INK, cut, rect, ellipse, rough_ellipse_pts, text
from sofia_v4 import SKIN, HAIR, HAIR_SHINE, HAIR_SHADE, RED, GOLD, GOLD_LIGHT, H

FUCHSIA = (0.86, 0.18, 0.52)
FUCHSIA_DARK = (0.66, 0.10, 0.38)
FUCHSIA_LIGHT = (0.96, 0.46, 0.70)
PATENT = (0.07, 0.07, 0.09)
BOOT = (0.08, 0.08, 0.10)
TIGHTS = (0.20, 0.17, 0.21)
ROSE_GOLD = (0.90, 0.66, 0.58)
CASE_PINK = (0.98, 0.72, 0.82)
BODY_TOP = -300 * H + 78
HY = BODY_TOP - 44
SH = ((-39, BODY_TOP + 14), (39, BODY_TOP + 14))
POSES = {   # (left upper, left fore, right upper, right fore): kit arm angles, 0 = down, +90 = screen right, 180 = up
    "stand": (-8, 0, 8, 0),
    "hold": (-24, 128, 8, 0),          # the tablet against her (screen-left hand at her chest)
    "phone": (-22, 140, 8, 0),          # the phone at her chest, screen to her
    "plaster": (-8, 0, 140, -30),       # screen-right hand up and out, pressing the plaster on the glass
    "behind": (-14, -20, 14, 20),       # both hands behind her back: the tablet hidden
    "hip": (-30, 110, 8, 0),
}


def earring(k, x, y, lgx=0.0, spark=0.0, seed=0):
    """Gold geometric drop: a stud, a small ring, a long open triangle with a bead at its point."""
    c = k.c
    ellipse(k, x, y, 4.0, 4.0, GOLD, seed, shadow=False, lw=1.5)
    c.save(); c.translate(x, y + 3); c.rotate(-lgx * 0.04)
    c.set_source_rgb(*INK); c.set_line_width(4.6); c.arc(0, 6, 5, 0, 2 * math.pi); c.stroke()
    c.set_source_rgb(*GOLD); c.set_line_width(2.4); c.arc(0, 6, 5, 0, 2 * math.pi); c.stroke()
    pts = [(-7.5, 12), (7.5, 12), (0, 29)]
    for col, lw in ((INK, 5.0), (GOLD, 2.8)):
        c.set_source_rgb(*col); c.set_line_width(lw); c.set_line_join(1)
        c.move_to(*pts[0]); c.line_to(*pts[1]); c.line_to(*pts[2]); c.close_path(); c.stroke()
    c.set_source_rgb(*GOLD_LIGHT); c.set_line_width(1.2); c.move_to(-5, 12.5); c.line_to(2, 12.5); c.stroke()
    ellipse(k, 0, 32, 3.2, 3.2, GOLD, seed + 1, shadow=False, lw=1.4)
    if spark > 0:
        c.set_source_rgba(1, 1, 1, 0.9 * spark); c.arc(-3, 16, 2.2, 0, 2 * math.pi); c.fill()
    c.restore()


def ponytail(k, hy, lgx, lgy, seed):
    """The high ponytail: tied at the back of the crown (the cuff shows at the top of her head), it lifts, arcs over
    to screen right behind her head and falls to her shoulder; the tip swings most."""
    c = k.c
    sw = lgx * 2.2
    pts = [(20, hy - 64), (46 + sw * 0.2, hy - 76), (70 + sw * 0.5, hy - 58), (78 + sw * 0.8, hy - 20),
           (74 + sw * 1.0, hy + 30 + lgy), (64 + sw * 1.3, hy + 74 + lgy),                                    # the tip
           (60 + sw * 1.0, hy + 34 + lgy), (60 + sw * 0.7, hy - 12), (52 + sw * 0.4, hy - 48), (30, hy - 52)]
    cut(k, pts, HAIR, lw=2.2)
    c.set_source_rgb(*HAIR_SHADE); c.set_line_width(2.0); c.set_line_cap(1)
    c.move_to(58 + sw * 0.4, hy - 52); c.curve_to(70 + sw * 0.7, hy - 30, 70 + sw * 0.9, hy + 10, 68 + sw * 1.2, hy + 56 + lgy)
    c.stroke()
    c.set_source_rgb(*HAIR_SHINE); c.set_line_width(3.4)
    c.move_to(44 + sw * 0.2, hy - 70); c.curve_to(62 + sw * 0.5, hy - 64, 72 + sw * 0.7, hy - 44, 74 + sw * 0.8, hy - 20)
    c.stroke()


def sofia(k, x, feet, s=1.0, pose="stand", face_kind="smile", look=(0, 0), lag=(0, 0), seed=7, badge=True, lean=0.0,
          sparkle=0.0, tablet_kind="auto", phone_lit=False):
    """Returns {"head", "hands"} in canvas coordinates (lean not applied to the returned points)."""
    c = k.c
    c.save(); c.translate(x, feet); c.rotate(math.radians(lean)); c.scale(s, s)
    bt, hy = BODY_TOP, HY
    lgx, lgy = lag
    ponytail(k, hy, lgx, lgy, seed + 1)                                           # behind everything
    a = POSES.get(pose) or kit.ARM_POSES[pose]
    if pose == "behind":                                                          # the tablet, hidden behind her back
        so.tablet(k, 46, bt + 92, 0.25, "back", seed + 80)
    # legs: dark tights, then the knee-high boots
    for sx_ in (-14, 14):
        o = 1 if sx_ > 0 else -1
        cut(k, [(sx_ - 8.5, -100), (sx_ + 8.5, -100), (sx_ + 6.5, -62), (sx_ - 6.5, -62)], TIGHTS, shadow=False, lw=1.8)
        cut(k, [(sx_ - 7.5, -66), (sx_ + 7.5, -66), (sx_ + 6, -12), (sx_ + 6 + o * 10, -2), (sx_ + 6 + o * 10, 0),
                (sx_ - 1 + o * 2, 0), (sx_ - 6, -8)], BOOT, shadow=False, lw=1.8)
        cut(k, [(sx_ - o * 6.0, -8), (sx_ - o * 2.8, -8), (sx_ - o * 3.6, 0), (sx_ - o * 5.6, 0)], BOOT, shadow=False, lw=1.4)  # the heel
        c.set_source_rgba(1, 1, 1, 0.45); c.set_line_width(2.0); c.set_line_cap(1)
        c.move_to(sx_ - 2.5, -58); c.line_to(sx_ - 2, -22); c.stroke()                                  # the shine
    # the coat-dress: body to the hem just above the knee
    coat = [(-37, bt), (37, bt), (41, bt + 36), (30, bt + 76), (27, bt + 98), (36, bt + 128), (52, -70), (-52, -70),
            (-36, bt + 128), (-27, bt + 98), (-30, bt + 76), (-41, bt + 36)]
    cut(k, coat, FUCHSIA, lw=2.4)
    cut(k, [(-14, bt), (14, bt), (0, bt + 26)], SKIN, shadow=False, lw=1.8)                             # the neckline
    c.set_source_rgb(*FUCHSIA_DARK); c.set_line_width(2.4); c.set_line_cap(1)
    c.move_to(-30, bt + 2); c.curve_to(-6, bt + 46, 14, bt + 80, 26, bt + 100); c.stroke()            # the wrap line
    c.move_to(26, bt + 112); c.curve_to(30, bt + 150, 36, -110, 40, -72); c.stroke()                   # its edge to the hem
    c.set_source_rgb(*FUCHSIA_LIGHT); c.set_line_width(2.0)
    c.move_to(-26, bt + 120); c.curve_to(-28, bt + 150, -32, -110, -36, -76); c.stroke()               # a soft fold
    for sx_ in (-1, 1):                                                                                # the roll collar
        cut(k, [(sx_ * 14, bt - 2), (sx_ * 38, bt - 4), (sx_ * 42, bt + 10), (sx_ * 30, bt + 22), (sx_ * 12, bt + 14)],
            FUCHSIA_DARK, shadow=False, lw=2.0)
    rect(k, -30, bt + 90, 60, 15, PATENT, seed + 45, shadow=False, lw=1.6)                              # the statement belt
    c.set_source_rgba(1, 1, 1, 0.35); c.rectangle(-28, bt + 92, 56, 2.2); c.fill()
    rect(k, -11, bt + 86, 22, 23, GOLD, seed + 46, shadow=False, lw=1.6)                                # its square buckle
    rect(k, -6, bt + 91, 12, 13, PATENT, seed + 47, shadow=False, lw=1.2)
    c.set_source_rgb(*GOLD_LIGHT); c.rectangle(-10, bt + 87, 20, 2); c.fill()
    if badge:
        rect(k, 8, bt + 46, 32, 20, (1, 1, 1), seed + 40, shadow=False, lw=1.6)
        c.set_source_rgb(*brand.GREEN); c.rectangle(11, bt + 48, 26, 3.5); c.fill()
        text(k, "SOFÍA", 24, bt + 58, 9, INK)
    # arms: the coat's sleeves
    old = sf.BLOUSE
    sf.BLOUSE = FUCHSIA
    try:
        hands = [sf._arm(k, SH[0][0], SH[0][1], a[0], a[1], seed + 9, w=15),
                 sf._arm(k, SH[1][0], SH[1][1], a[2], a[3], seed + 11, w=15)]
    finally:
        sf.BLOUSE = old
    tk = {"hold": "hold"}.get(pose) if tablet_kind == "auto" else tablet_kind
    (lx, ly), (rx, ry) = hands
    if tk == "hold":
        so.tablet(k, lx + 20, ly - 12, -0.10, "back", seed + 80)
        ellipse(k, lx, ly, 9, 9, SKIN, seed + 81, shadow=False, lw=2)
        ellipse(k, lx + 3, ly + 6, 3.0, 3.0, RED, seed + 82, shadow=False, outline=False)
    if pose == "phone":                                                                                # the luxe case
        c.save(); c.translate(lx + 12, ly - 16); c.rotate(-0.12)
        rect(k, -11, -20, 22, 40, ROSE_GOLD, seed + 85, lw=1.8)
        rect(k, -7.5, -16, 15, 32, CASE_PINK if not phone_lit else (0.95, 0.97, 1.0), seed + 86, shadow=False, lw=1.2)
        c.set_source_rgb(*ROSE_GOLD); c.arc(0, 0, 4, 0, 2 * math.pi); c.fill()                      # the gold emblem (no logo)
        c.set_source_rgb(*GOLD_LIGHT); c.set_line_width(1.2); c.arc(0, 0, 4, 0, 2 * math.pi); c.stroke()
        c.restore()
        ellipse(k, lx, ly, 9, 9, SKIN, seed + 87, shadow=False, lw=2)
        ellipse(k, lx + 3, ly + 6, 3.0, 3.0, RED, seed + 88, shadow=False, outline=False)
    if pose == "plaster":                                                                              # the nails on the strip
        ellipse(k, rx + 3, ry - 4, 3.0, 3.0, RED, seed + 89, shadow=False, outline=False)
    # head: the hair pulled back smooth, no side locks
    ellipse(k, 0, hy, 50, 50, SKIN, seed + 20)
    cap = [(math.cos(a_) * 55, hy - 8 + math.sin(a_) * 55) for a_ in [math.pi * (1.0 + i / 15.0) for i in range(16)]]
    cut(k, cap + [(53, hy - 16), (30, hy - 36), (0, hy - 40), (-30, hy - 36), (-53, hy - 16)], HAIR, shadow=False, lw=2)
    c.set_source_rgb(*HAIR_SHADE); c.set_line_width(1.6); c.set_line_cap(1)
    for dx in (-30, -12, 8, 26):                                                                       # combed back
        c.move_to(dx * 0.8, hy - 42); c.curve_to(dx * 0.9, hy - 50, dx * 0.5 + 10, hy - 56, 22, hy - 58); c.stroke()
    c.set_source_rgb(*HAIR_SHINE); c.set_line_width(4.0)
    c.move_to(-34, hy - 44); c.curve_to(-18, hy - 54, 0, hy - 56, 16, hy - 56); c.stroke()
    c.save(); c.translate(24, hy - 60); c.rotate(-0.5)
    rect(k, -7, -8, 14, 16, GOLD, seed + 25, shadow=False, lw=1.6)                                      # the gold hair cuff
    c.set_source_rgb(*GOLD_LIGHT); c.rectangle(-5, -6, 2, 12); c.fill()
    c.restore()
    for sx_ in (-1, 1):
        earring(k, sx_ * 51 + lgx * 0.6, hy + 20, lgx, sparkle if sx_ > 0 else sparkle * 0.55, seed + 30 + sx_)
    ss.face(k, 0, hy + 4, face_kind, look, seed + 60)
    if face_kind not in ("horrified", "curious", "surprised"):
        c.set_source_rgba(1, 1, 1, 0.75); c.set_line_width(2.0); c.set_line_cap(1)
        c.move_to(-4, hy + 35); c.line_to(2, hy + 35); c.stroke()
    c.restore()
    return {"head": (x, feet + hy * s), "hands": [(x + hx * s, feet + hyy * s) for hx, hyy in hands]}
