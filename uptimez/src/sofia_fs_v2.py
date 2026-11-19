"""(pinned: sofia v2) SOFIA, "First Search" (episode 10), v2 (sofia_fs_v1.py = v1, kept), after the look-sheet audit (18 Nov): the
costume is approved; the acting was not.
- LONG SLEEVES to the wrist with a darker cuff (v1's bare forearms did not say winter);
- EIGHT FACES OF HER OWN (fs_face), built so the eyes and brows carry the feeling at 270 px, not only the lips:
    charm      lids a quarter down, brows arched high and soft, a closed smile lifted at one corner: for the Client
    fake       eyes a little too wide, straight raised brows, a wide smile with a band of teeth: the customer smile
    drop       the smile gone: eyes wide, small pupils, the inner ends of the brows up, lips parted in a small flat O
    better     happy closed arcs for eyes, relaxed brows, a small closed smirk with a dimple: after the plaster
    deadpan    half lids, pupils dead centre, one brow up, lips pressed flat: the look to camera
    sideeye    eyes open, pupils hard to one side, brows flat and low, lips pressed and pulled to that side: "not me"
    contempt   asymmetric: one lid lower, that brow pressed down, one corner of the mouth up: "We fixed the red."
    resigned   lids closed flat, brows down, a small flat mouth: Mom rescues him
  plus freeze (eyes huge, pin-point pupils, brows straight up, lips pressed) for the action. The kit faces still work;
- NEW POSES: clasp (hands together at her waist: the polite lean), freeze (arms tight at her sides), pinch (the
  plaster between finger and thumb, held up), press (her hand on the glass, flat);
- the plaster is drawn in her hand (plaster=True) and the tablet slides (slide=0..1, from her chest to behind her);
- rules for every shot: the ponytail always falls to screen right; the earrings and the ponytail lag the head; the
  buckle is always centred; freeze keeps the earrings swinging while everything else stops.
Below, the notes of v1.
SOFIA, "First Search" (episode 10), v1: her January look, developed on its own (the grill of 18 Nov). Every earlier
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
    "clasp": (-26, 96, 26, -96),        # v2: hands together at her waist
    "freeze": (-3, 0, 3, 0),            # v2: arms tight at her sides
    "pinch": (-8, 0, 150, -40),         # v2: the plaster held up between finger and thumb
    "press": (-8, 0, 128, -18),         # v2: her flat hand on the glass
}
SLEEVE_CUFF = (0.58, 0.07, 0.32)


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


# ---------------------------------------------------------------- v2: long sleeves
def arm_long(k, sx, sy, a1, a2, seed, ln=48, w=15):
    """The coat's sleeve to the wrist, a darker cuff, her hand and its red nail."""
    d = lambda a: (math.sin(math.radians(a)), math.cos(math.radians(a)))
    ex, ey = sx + d(a1)[0] * ln, sy + d(a1)[1] * ln
    hx, hy = ex + d(a1 + a2)[0] * ln, ey + d(a1 + a2)[1] * ln
    for (ax, ay, bx, by), ww in (((sx, sy, ex, ey), w), ((ex, ey, hx, hy), w * 0.92)):
        g = math.atan2(by - ay, bx - ax)
        nx, ny = -math.sin(g) * ww / 2, math.cos(g) * ww / 2
        cut(k, [(ax + nx, ay + ny), (bx + nx, by + ny), (bx - nx, by - ny), (ax - nx, ay - ny)], FUCHSIA, shadow=False, lw=2)
    g = math.atan2(hy - ey, hx - ex)
    nx, ny = -math.sin(g) * (w / 2 + 1.5), math.cos(g) * (w / 2 + 1.5)
    cx, cy = hx - math.cos(g) * 9, hy - math.sin(g) * 9
    cut(k, [(cx + nx, cy + ny), (hx - math.cos(g) * 3 + nx, hy - math.sin(g) * 3 + ny),
            (hx - math.cos(g) * 3 - nx, hy - math.sin(g) * 3 - ny), (cx - nx, cy - ny)], SLEEVE_CUFF, shadow=False, lw=1.8)
    ellipse(k, hx + math.cos(g) * 3, hy + math.sin(g) * 3, w * 0.58, w * 0.58, SKIN, seed, shadow=False, lw=2)
    ellipse(k, hx + math.cos(g) * 10, hy + math.sin(g) * 10, 3.2, 3.2, RED, seed + 1, shadow=False, outline=False)
    return hx + math.cos(g) * 3, hy + math.sin(g) * 3


# ---------------------------------------------------------------- v2: her own faces
FS_FACES = ("charm", "fake", "drop", "better", "deadpan", "sideeye", "contempt", "resigned", "freeze")


def _eye(k, x, y, o, lid=0.0, pupil=5.4, look=(0, 0), r=11.5, seed=0, closed=None):
    """One eye. o: -1 screen left, +1 screen right. lid: 0 open .. 1 shut (the skin comes down from the top).
    closed: None, "happy" (an arc up), "flat" (a line)."""
    c = k.c
    if closed == "happy":
        c.set_source_rgb(*INK); c.set_line_width(4); c.set_line_cap(1)
        c.arc(x, y + 4, 9.5, math.pi * 1.12, math.pi * 1.88); c.stroke()
        c.set_line_width(2.6); c.move_to(x + o * 9, y - 1); c.line_to(x + o * 15, y - 6); c.stroke()
        return
    if closed == "flat":
        c.set_source_rgb(*INK); c.set_line_width(4); c.set_line_cap(1)
        c.move_to(x - 11, y + 2); c.curve_to(x - 4, y + 5, x + 4, y + 5, x + 11, y + 2); c.stroke()
        c.set_line_width(2.4); c.move_to(x + o * 11, y + 2); c.line_to(x + o * 15, y - 2); c.stroke()
        return
    ellipse(k, x, y, r, r, (1, 1, 1), seed, shadow=False, lw=2)
    px_, py_ = x + look[0] * 5, y + look[1] * 4
    ellipse(k, px_, py_, pupil, pupil, INK, seed + 1, shadow=False, outline=False)
    if pupil > 3:
        c.set_source_rgb(1, 1, 1); c.arc(px_ + 1.6, py_ - 1.8, 1.5, 0, 2 * math.pi); c.fill()
    if lid > 0:
        top = y - r - 2 + (2 * r + 2) * lid
        c.save(); c.rectangle(x - r - 4, y - r - 6, 2 * r + 8, top - (y - r - 6)); c.clip()
        ellipse(k, x, y, r + 2.5, r + 2.5, SKIN, seed + 2, shadow=False, outline=False)
        c.restore()
        c.set_source_rgb(*INK); c.set_line_width(3.6); c.set_line_cap(1)
        half = math.sqrt(max(0.0, r * r - (top - y) ** 2))
        c.move_to(x - half - 0.5, top); c.line_to(x + half + 0.5, top); c.stroke()
    else:
        c.set_source_rgb(*INK); c.set_line_width(4.2); c.set_line_cap(1)
        c.arc(x, y + 1, r + 0.5, (1.08 if o > 0 else 1.05) * math.pi, (1.95 if o > 0 else 1.92) * math.pi); c.stroke()
    wy = y - r * 0.15 if lid < 0.3 else y - r + (2 * r) * lid - 1
    c.set_source_rgb(*INK); c.set_line_width(3.2)
    c.move_to(x + o * (r - 1), wy); c.line_to(x + o * (r + 7), wy - 6); c.stroke()                     # the wing


def _brow(c, x, y, o, inner, outer, arch=3.0, lw=4.2):
    """inner/outer: heights of the inner and outer end, relative to the eye line (negative is up)."""
    xi, xo = x + o * 8, x + o * 27
    c.set_source_rgb(*INK); c.set_line_width(lw); c.set_line_cap(1)
    c.move_to(xi, y + inner)
    c.curve_to(xi + o * 6, y + inner - arch, xo - o * 7, y + outer - arch, xo, y + outer); c.stroke()


def fs_face(k, x, y, kind, look=(0, 0), seed=0):
    c = k.c
    lx = look[0]
    E = {   # (lid L, lid R, pupil, (brow L inner, outer, arch), (brow R inner, outer, arch), closed)
        "charm":    (0.25, 0.25, 5.4, (-23, -22, 6), (-23, -22, 6), None),
        "fake":     (0.0, 0.0, 4.8, (-27, -27, 1), (-27, -27, 1), None),
        "drop":     (0.0, 0.0, 3.4, (-30, -22, 2), (-30, -22, 2), None),
        "better":   (0, 0, 0, (-19, -21, 3), (-19, -21, 3), "happy"),
        "deadpan":  (0.45, 0.45, 5.0, (-16, -16, 1), (-30, -26, 4), None),
        "sideeye":  (0.15, 0.15, 5.0, (-15, -17, 1), (-15, -17, 1), None),
        "contempt": (0.20, 0.50, 5.0, (-20, -23, 3), (-12, -16, 1), None),
        "resigned": (0, 0, 0, (-14, -16, 1), (-14, -16, 1), "flat"),
        "freeze":   (0.0, 0.0, 2.4, (-31, -31, 0), (-31, -31, 0), None),
    }[kind]
    lidL, lidR, pupil, bL, bR, closed = E
    lk = {"sideeye": (1.6 if lx >= 0 else -1.6, 0.1), "deadpan": (0, 0.1), "freeze": (0, 0)}.get(kind, look)
    big = kind in ("fake", "drop", "freeze")
    for o, lid, b in ((-1, lidL, bL), (1, lidR, bR)):
        _eye(k, x + o * 17, y, o, lid, pupil, lk, 13.0 if big else 11.5, seed + o, closed)
        _brow(c, x + o * 0, y, o, b[0], b[1], b[2])
    my = y + 29
    c.set_source_rgb(*RED)
    if kind == "charm":                                    # closed smile, one corner up
        c.set_line_width(6.5); c.set_line_cap(1)
        c.move_to(x - 11, my - 2); c.curve_to(x - 4, my + 4, x + 6, my + 3, x + 13, my - 5); c.stroke()
    elif kind == "fake":                                   # wide, a band of teeth
        c.save(); c.translate(x, my - 2)
        c.move_to(-16, -3); c.curve_to(-8, 10, 8, 10, 16, -3); c.curve_to(8, 1, -8, 1, -16, -3); c.close_path()
        c.set_source_rgb(1, 1, 1); c.fill_preserve(); c.set_source_rgb(*RED); c.set_line_width(4.6); c.stroke()
        c.set_source_rgb(*INK); c.set_line_width(1.0); c.move_to(-12, 1.5); c.line_to(12, 1.5); c.stroke()
        c.restore()
    elif kind == "drop":                                   # lips parted, a small flat O
        ellipse(k, x, my, 6.5, 4.0, (0.45, 0.06, 0.08), seed + 5, shadow=False, lw=1.6)
        c.set_source_rgb(*RED); c.set_line_width(3.4); c.save(); c.translate(x, my); c.scale(1.0, 0.62)
        c.arc(0, 0, 8, 0, 2 * math.pi); c.restore(); c.stroke()
    elif kind == "better":                                 # small closed smirk, a dimple
        c.set_line_width(6.0); c.set_line_cap(1)
        c.move_to(x - 8, my); c.curve_to(x - 2, my + 3, x + 5, my + 2, x + 10, my - 4); c.stroke()
        c.set_source_rgb(*INK); c.set_line_width(1.8); c.arc(x + 16, my - 5, 3.0, -0.3 * math.pi, 0.25 * math.pi); c.stroke()
    elif kind in ("deadpan", "freeze", "resigned"):        # pressed flat
        c.set_line_width(5.4); c.set_line_cap(1)
        w_ = 8 if kind == "resigned" else 11
        c.move_to(x - w_, my); c.line_to(x + w_, my); c.stroke()
    elif kind == "sideeye":                                # pressed, pulled to the side she looks
        o = 1 if lk[0] > 0 else -1
        c.set_line_width(5.4); c.set_line_cap(1)
        c.move_to(x - 7 + o * 5, my + 1); c.line_to(x + 7 + o * 5, my - 1); c.stroke()
    elif kind == "contempt":                               # one corner up
        c.set_line_width(5.4); c.set_line_cap(1)
        c.move_to(x - 10, my + 1); c.line_to(x + 4, my + 1); c.curve_to(x + 8, my + 1, x + 11, my - 2, x + 13, my - 6); c.stroke()


_sofia_v1 = sofia


def sofia(k, x, feet, s=1.0, pose="stand", face_kind="smile", look=(0, 0), lag=(0, 0), seed=7, badge=True, lean=0.0,
          sparkle=0.0, tablet_kind="auto", phone_lit=False, plaster=None, slide=None):
    """v2: long sleeves; her own faces (FS_FACES) or any kit face; plaster="held"/None; slide 0..1 (the tablet, from
    her chest to behind her back)."""
    old = sf._arm, ss.face
    sf._arm = arm_long
    if face_kind in FS_FACES:
        ss.face = lambda k_, x_, y_, kind, look_, seed_: fs_face(k_, x_, y_, face_kind, look, seed_)
    tk = tablet_kind
    if slide is not None:
        tk = None if slide >= 0.999 else None
    try:
        base = face_kind
        if face_kind in FS_FACES:                           # no lip gloss over a flat or open mouth
            base = "neutral" if face_kind in ("charm", "fake", "better") else "surprised"
        out = _sofia_v1(k, x, feet, s, pose, base, look, lag, seed, badge,
                        lean, sparkle, tk if slide is None else None, phone_lit)
    finally:
        sf._arm, ss.face = old
    c = k.c
    (lx, ly), (rx, ry) = out["hands"]
    if slide is not None:                                   # the tablet, on its way down and behind her
        import sofia_ob as so_
        u = max(0.0, min(1.0, slide))
        tx = lx + 10 + (x + 46 * s - (lx + 10)) * u
        ty = ly - 8 * s + (feet - 116 * s - (ly - 8 * s)) * u
        if u < 0.999:
            so_.tablet(k, tx, ty, -0.10 + 0.4 * u, "back", seed + 80) if s == 1.0 else _tablet_scaled(k, tx, ty, s, u, seed)
        else:
            c.save(); c.translate(x, feet); c.scale(s, s); c.restore()
    if pose == "pinch" and plaster:                         # the plaster, between finger and thumb
        import fs_set as fs_
        fs_.plaster(c, rx + 6 * s, ry - 14 * s, 0.9 * s, ang=-0.9)
        ellipse(k, rx, ry, 8.5 * s, 8.5 * s, SKIN, seed + 99, shadow=False, lw=2 * s)
    return out


def _tablet_scaled(k, tx, ty, s, u, seed):
    import sofia_ob as so_
    c = k.c
    c.save(); c.translate(tx, ty); c.scale(s, s)
    so_.tablet(k, 0, 0, -0.10 + 0.4 * u, "back", seed + 80)
    c.restore()
