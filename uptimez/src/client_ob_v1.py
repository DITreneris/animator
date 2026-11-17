"""v1, pinned (the three look options; client_ob.py is the revised look B).
THE ONBOARDING: the Client, v1 (look options). A garage owner: ten garages across the city, built them himself.
Rugged and warm, mid-forties, a head taller than Don; a clean work jacket with a gear-and-wrench patch (a symbol,
no words), a rag in the back pocket, big hands with oil in the creases, a good watch, a heavy ring of keys with his
car's fob. He smells of gas and oil, which is acted by the others and never drawn. Nobody asks his name: VISITOR.
He carries a blue roll under his arm: the blueprint of the best transmission system. It is the only blue paper
in the film, so nothing he wears is blue.

Drawn here from kit primitives with the candidates' limb code (cand_bc.limb / ik / visitor); kit, cand_bc and every
earlier character are untouched. Three looks to choose from, LOOKS["A"], ["B"], ["C"]: they differ in the head
(cap and moustache / swept grey temples and stubble / curls and a short beard) and in the jacket's colour.

Usage: o = client(k, x, feet, s, pose, face, look, mouth=None, variant="B", roll=False, badge=True)
Returns {"head", "hands", "top"} in canvas coordinates; pose is a name in POSES or (a1, a2, b1, b2) degrees
(0 = down, +90 = screen right, 180 = up). Faces: warm (the default), neutral, puzzled, relief."""
import math
import kit
import iwry_mouths as im
from kit import INK, cut, rect, ellipse
from cand_bc import limb, ik, visitor, _brow, _d

SKIN = (0.90, 0.69, 0.55)
SKIN_DARK = (0.70, 0.47, 0.35)
OIL = (0.30, 0.22, 0.18)
HAIR = (0.24, 0.17, 0.13)
GREY = (0.66, 0.65, 0.66)
TROUSERS = (0.27, 0.28, 0.32)
TROUSERS_DARK = (0.18, 0.19, 0.23)
BOOT = (0.36, 0.23, 0.14)
SOLE = (0.82, 0.74, 0.58)
TEE = (0.93, 0.90, 0.82)
RAG = (0.80, 0.22, 0.20)
STEEL = (0.80, 0.82, 0.85)
GOLD = (0.88, 0.72, 0.30)
BLUEPRINT = (0.16, 0.38, 0.78)
L, T = 178, 142
HIP = -L
BT = HIP - T
HY = BT - 60
SH = (80, BT + 26)
LN1, LN2 = 62, 58
TOP = HY - 72
HAND = 20
HEAD = 1.08                                              # the head, a little larger than drawn

LOOKS = {
    "A": dict(name="the flat cap", jacket=(0.74, 0.39, 0.20), dark=(0.52, 0.25, 0.12), collar=(0.36, 0.22, 0.14),
              head="cap", chin="moustache"),
    "B": dict(name="grey temples", jacket=(0.44, 0.49, 0.31), dark=(0.31, 0.36, 0.21), collar=(0.82, 0.72, 0.52),
              head="swept", chin="stubble"),
    "C": dict(name="the beard", jacket=(0.26, 0.26, 0.29), dark=(0.14, 0.14, 0.17), collar=(0.93, 0.88, 0.76),
              head="curls", chin="beard"),
}


def _ik(side, tx, ty):
    return ik(side * SH[0], SH[1], tx, ty, LN1, LN2, side)


POSES = {
    "stand": (-9, 4, 9, -4),
    "roll": (-11, 6, 9, -4),                                               # the blueprint upright in his fist
    "wave": (-9, 4) + _ik(1, 132, BT - 6),                                 # a small hello
    "offer": (-9, 4) + _ik(1, 150, BT + 96),                               # a hand out to shake
}


def gear(k, x, y, r, col=(0.96, 0.93, 0.84), seed=0):
    """The garages' mark: a gear with a wrench across it. A symbol, never words."""
    c = k.c
    c.save(); c.translate(x, y)
    n = 8
    pts = []
    for i in range(n * 4):
        a = 2 * math.pi * i / (n * 4)
        rr = r if i % 4 in (0, 1) else r * 0.74
        pts.append((math.cos(a - 0.2) * rr, math.sin(a - 0.2) * rr))
    c.move_to(*pts[0])
    for q in pts[1:]:
        c.line_to(*q)
    c.close_path(); c.set_source_rgb(*col); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1.2); c.stroke()
    c.arc(0, 0, r * 0.30, 0, 2 * math.pi); c.set_source_rgb(*INK); c.fill()
    c.rotate(-0.7)                                                           # the wrench
    c.set_source_rgb(*INK); c.set_line_width(r * 0.26); c.set_line_cap(1)
    c.move_to(-r * 1.15, 0); c.line_to(r * 1.15, 0); c.stroke()
    c.set_source_rgb(*col); c.set_line_width(r * 0.10)
    c.move_to(-r * 1.1, 0); c.line_to(r * 1.1, 0); c.stroke()
    c.restore()


def blueprint_roll(k, x, y, ang, ln=150, r=11, seed=0):
    """The roll: blue paper, white on the inside. (x, y) is its middle; ang in radians from the vertical."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang)
    rect(k, -r, -ln / 2, 2 * r, ln, BLUEPRINT, seed + 1, shadow=False, lw=2)
    c.set_source_rgba(1, 1, 1, 0.75); c.set_line_width(1.3)
    for yy in (-ln * 0.28, -ln * 0.05, ln * 0.2):
        c.move_to(-r + 3, yy); c.line_to(r - 3, yy + 4); c.stroke()
    for end in (-1, 1):
        ellipse(k, 0, end * ln / 2, r, r * 0.42, (0.97, 0.97, 0.99), seed + 3 + end, shadow=False, lw=1.8)
        c.set_source_rgb(*BLUEPRINT); c.set_line_width(1.4)
        c.save(); c.translate(0, end * ln / 2); c.scale(1, 0.42); c.arc(0, 0, r * 0.5, 0.4, 5.4); c.restore(); c.stroke()
    c.restore()


def keys(k, x, y, seed=0):
    """A heavy ring of keys on a clip, with the car's fob."""
    c = k.c
    c.set_source_rgb(*INK); c.set_line_width(2.2); c.move_to(x, y - 12); c.line_to(x, y); c.stroke()
    r = k.rng(seed)
    for i, a in enumerate((-0.9, -0.55, -0.2, 0.15, 0.5, 0.85)):
        c.save(); c.translate(x, y + 8); c.rotate(a + r.uniform(-0.06, 0.06))
        col = STEEL if i % 2 else GOLD
        rect(k, -2.4, 4, 4.8, 22, col, seed + 10 + i, shadow=False, lw=1.2)
        c.restore()
    c.save(); c.translate(x, y + 8); c.rotate(0.34)                           # the fob
    rect(k, -7, 8, 14, 24, (0.14, 0.14, 0.17), seed + 30, shadow=False, lw=1.4)
    c.set_source_rgb(0.85, 0.22, 0.20); c.arc(0, 16, 2.6, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(*STEEL); c.arc(0, 25, 2.2, 0, 2 * math.pi); c.fill()
    c.restore()
    c.set_source_rgb(*STEEL); c.set_line_width(2.6); c.arc(x, y + 8, 7, 0, 2 * math.pi); c.stroke()
    c.set_source_rgb(*INK); c.set_line_width(1.0); c.arc(x, y + 8, 8.4, 0, 2 * math.pi); c.stroke()


def _head_pts(k, hy, seed):
    """Square and soft: wide at the cheekbones, a strong jaw that has rounded off."""
    r = k.rng(seed)
    pts = []
    n = 34
    for i in range(n):
        a = 2 * math.pi * i / n
        cs, sn = math.cos(a), math.sin(a)
        if sn > 0:
            px = math.copysign(abs(cs) ** 0.56, cs) * 47
            py = (sn ** 0.78) * 55
        else:
            px, py = cs * 46, sn * 49
        pts.append((px * (1 + r.uniform(-0.01, 0.01)), hy + py * (1 + r.uniform(-0.01, 0.01))))
    return pts


def _face(k, y, face, look, mouth, seed, chin):
    c = k.c
    lx, ly = look
    ey = y - 5
    warm = face in ("warm", "relief")
    c.set_source_rgba(0.86, 0.36, 0.26, 0.20)                                # weather on the cheeks
    for sx in (-1, 1):
        c.save(); c.translate(sx * 29, y + 14); c.scale(12, 8); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
    c.set_source_rgba(*SKIN_DARK, 0.7); c.set_line_width(1.6); c.set_line_cap(1)   # two lines on the forehead
    for i, fy in enumerate((y - 33, y - 27)):
        c.move_to(-17 + i * 3, fy); c.curve_to(-6, fy - 2, 8, fy - 2, 18 - i * 4, fy); c.stroke()
    for sx in (-17, 17):
        ellipse(k, sx, ey, 9.8, 9.8, (1, 1, 1), seed + sx, shadow=False, lw=2)
        ellipse(k, sx + lx * 3.6, ey + ly * 3.4 + 0.6, 4.9, 4.9, (0.34, 0.22, 0.12), seed + sx + 1, shadow=False,
                outline=False)
        c.set_source_rgb(1, 1, 1); c.arc(sx + lx * 3.6 - 1.6, ey + ly * 3.4 - 1.2, 1.5, 0, 2 * math.pi); c.fill()
        lid = 0.14 if warm else (0.10 if face == "neutral" else 0.0)        # easy lids
        if lid:
            c.save(); c.arc(sx, ey, 10.6, 0, 2 * math.pi); c.clip()
            c.set_source_rgb(*SKIN); c.rectangle(sx - 11, ey - 11, 22, 21 * lid); c.fill()
            c.restore()
            _brow(c, sx - 9.0, ey - 10.6 + 21 * lid, sx + 9.0, ey - 10.6 + 21 * lid, 2.4)
        if warm:                                                             # the cheek lifts the lower lid
            c.set_source_rgb(*SKIN); c.rectangle(sx - 11, ey + 6.5, 22, 6); c.fill()
            c.set_source_rgb(*INK); c.set_line_width(2.0); c.set_line_cap(1)
            c.move_to(sx - 9, ey + 7.2); c.curve_to(sx - 4, ey + 5.0, sx + 4, ey + 5.0, sx + 9, ey + 7.2); c.stroke()
        s_ = 1 if sx > 0 else -1                                             # crow's feet
        c.set_source_rgba(*SKIN_DARK, 0.9); c.set_line_width(1.5)
        for dy, dx in ((-3, 5), (2, 6)):
            c.move_to(sx + s_ * 12.5, ey + dy * 0.6 + 2); c.line_to(sx + s_ * (12.5 + dx), ey + dy + 2); c.stroke()
    by = y - 22
    if face == "puzzled":
        _brow(c, -30, by - 3, -8, by + 1, 6.4); _brow(c, 8, by - 6, 30, by - 8, 6.4)
    elif face == "relief":
        _brow(c, -30, by - 1, -8, by - 6, 6.4); _brow(c, 8, by - 6, 30, by - 1, 6.4)
    elif face == "neutral":
        _brow(c, -30, by, -8, by, 6.4); _brow(c, 8, by, 30, by, 6.4)
    else:                                                                    # warm: the inner ends a little up
        _brow(c, -31, by + 1, -8, by - 2, 6.4); _brow(c, 8, by - 2, 31, by + 1, 6.4)
    c.set_source_rgb(*SKIN_DARK); c.set_line_width(2.8); c.set_line_cap(1); c.set_line_join(1)   # a nose with history
    c.move_to(-3, y - 4); c.curve_to(-5, y + 6, -11, y + 12, -8, y + 17)
    c.curve_to(-3, y + 21, 5, y + 21, 9, y + 16); c.stroke()
    c.set_line_width(2.0); c.move_to(9, y + 16); c.curve_to(12, y + 12, 10, y + 8, 6, y + 8); c.stroke()
    my = y + 33
    if chin == "beard":
        pass                                                                 # drawn by the caller, under the mouth
    c.set_source_rgba(*SKIN_DARK, 0.9); c.set_line_width(2.0)                 # the lines a smile has worn in
    for sx in (-1, 1):
        c.move_to(sx * 13, y + 16); c.curve_to(sx * 22, y + 22, sx * 25, y + 30, sx * 22, my + 3); c.stroke()
    if chin == "beard":                                                      # the lips, clear of the beard
        ellipse(k, 1, my, 19, 8.5, (0.84, 0.60, 0.50), seed + 95, shadow=False, outline=False)
    if mouth:
        im.mouth(k, 0, my, mouth, SKIN, erase=(1, 1), seed=seed + 96)
    elif warm:                                                               # a closed, lopsided, real smile
        c.set_source_rgb(*INK); c.set_line_width(3.6); c.set_line_cap(1)
        c.move_to(-19, my - 4); c.curve_to(-9, my + 8, 9, my + 8, 21, my - 7); c.stroke()
        c.set_line_width(2.2); c.move_to(21, my - 7); c.line_to(24, my - 10); c.stroke()
    elif face == "puzzled":
        c.set_source_rgb(*INK); c.set_line_width(3.4); c.set_line_cap(1)
        c.move_to(-10, my + 1); c.curve_to(-3, my - 2, 4, my + 2, 12, my - 1); c.stroke()
    else:
        c.set_source_rgb(*INK); c.set_line_width(3.4); c.set_line_cap(1)
        c.move_to(-11, my); c.curve_to(-4, my + 2, 4, my + 2, 12, my - 1); c.stroke()
    if chin == "moustache":                                                  # salt and pepper, over the lip
        cut(k, [(-22, my - 5), (-12, my - 13), (0, my - 11), (12, my - 13), (22, my - 5), (12, my - 3), (0, my - 5),
                (-12, my - 3)], (0.42, 0.37, 0.34), shadow=False, lw=2)
        c.set_source_rgba(1, 1, 1, 0.5); c.set_line_width(1.2)
        for dx in (-14, -7, 7, 14):
            c.move_to(dx, my - 10); c.line_to(dx * 1.1, my - 5); c.stroke()


def client(k, x, feet, s=1.0, pose="stand", face="warm", look=(0, 0), seed=900, mouth=None, variant="B", roll=False,
           badge=True):
    c = k.c
    v = LOOKS[variant]
    J, JD, COL = v["jacket"], v["dark"], v["collar"]
    a = POSES[pose] if isinstance(pose, str) else pose
    c.save(); c.translate(x, feet); c.scale(s, s)
    for sx in (-1, 1):                                                       # boots and work trousers
        ellipse(k, sx * 27, -4, 27, 9, SOLE, seed + 2 + sx, lw=2)
        ellipse(k, sx * 27, -9, 27, 11, BOOT, seed + 3 + sx, shadow=False, lw=2)
        cut(k, [(sx * 1, HIP - 4), (sx * 50, HIP - 4), (sx * 44, -12), (sx * 8, -12)], TROUSERS, shadow=False, lw=2)
        c.set_source_rgb(*TROUSERS_DARK); c.set_line_width(1.8)
        c.move_to(sx * 40, HIP + 30); c.line_to(sx * 37, -16); c.stroke()
    cut(k, [(46, HIP + 12), (66, HIP + 16), (70, HIP + 46), (57, HIP + 58), (48, HIP + 42)], RAG, shadow=False, lw=1.8)  # the rag
    c.set_source_rgba(*OIL, 0.8)
    for dx, dy in ((55, 28), (61, 40), (52, 44)):
        c.arc(dx, HIP + dy, 2.2, 0, 2 * math.pi); c.fill()
    keys(k, -40, HIP + 18, seed + 60)
    bt = BT
    rect(k, -19, bt - 26, 38, 32, SKIN, seed + 5, shadow=False, lw=2)         # the neck
    cut(k, [(-90, bt + 30), (-75, bt + 5), (-26, bt - 9), (26, bt - 9), (75, bt + 5), (90, bt + 30), (84, bt + 100),
            (72, HIP + 14), (-72, HIP + 14), (-84, bt + 100)], J, lw=2.4)      # the work jacket: a barrel, not a V
    cut(k, [(0, bt + 46), (-19, bt - 8), (19, bt - 8)], TEE, shadow=False, lw=1.6)
    for sx in (-1, 1):                                                       # the collar
        cut(k, [(sx * 19, bt - 8), (sx * 44, bt - 15), (sx * 38, bt + 20), (sx * 5, bt + 44)], COL, shadow=False, lw=1.8)
    c.set_source_rgb(*JD); c.set_line_width(2.4); c.set_line_cap(1)
    c.move_to(0, bt + 46); c.line_to(0, HIP + 12); c.stroke()                 # the zip
    c.move_to(-73, HIP + 2); c.line_to(73, HIP + 2); c.stroke()               # the hem band
    rect(k, -62, bt + 54, 40, 36, J, seed + 41, shadow=False, lw=1.6)         # the chest pocket and its patch
    c.set_source_rgb(*JD); c.set_line_width(1.6); c.move_to(-62, bt + 62); c.line_to(-22, bt + 62); c.stroke()
    gear(k, -42, bt + 75, 10.5, seed=seed + 42)
    if badge:
        visitor(k, 46, bt + 62, 30, -0.06, seed + 50)
    if roll:                                                                 # upright in his fist, at his side
        h0 = (-SH[0] + _d(a[0])[0] * LN1 + _d(a[0] + a[1])[0] * LN2, bt + 26 + _d(a[0])[1] * LN1 + _d(a[0] + a[1])[1] * LN2)
        blueprint_roll(k, h0[0] - 13, h0[1] - 58, -0.06, 176, 11, seed + 70)
    hands = []
    for side, (u, f) in ((-1, (a[0], a[1])), (1, (a[2], a[3]))):
        sx_, sy_ = side * SH[0], bt + 26
        ex, ey = sx_ + _d(u)[0] * LN1, sy_ + _d(u)[1] * LN1
        hx, hy_ = limb(k, sx_, sy_, u, f, LN1, LN2, 44, 35, J, J, SKIN, HAND, seed + 10 + side)
        ellipse(k, side * (SH[0] - 1), bt + 25, 22, 19, J, seed + 14 + side, shadow=False, lw=2)   # the shoulder
        c.set_source_rgb(*J); c.rectangle(min(side * 56, side * 82), bt + 14, 26, 32); c.fill()
        ux, uy = (hx - ex) / LN2, (hy_ - ey) / LN2
        px, py = -uy, ux
        wx, wy = hx - ux * (HAND + 3), hy_ - uy * (HAND + 3)                   # the wrist: a knit cuff
        cut(k, [(wx + px * 19 - ux * 9, wy + py * 19 - uy * 9), (wx + px * 18, wy + py * 18), (wx - px * 18, wy - py * 18),
                (wx - px * 19 - ux * 9, wy - py * 19 - uy * 9)], COL, shadow=False, lw=1.8)
        if side == 1:                                                        # the good watch, below the cuff
            bx, by_ = hx - ux * (HAND - 6), hy_ - uy * (HAND - 6)
            cut(k, [(bx + px * 15 - ux * 5, by_ + py * 15 - uy * 5), (bx + px * 15 + ux * 5, by_ + py * 15 + uy * 5),
                    (bx - px * 15 + ux * 5, by_ - py * 15 + uy * 5), (bx - px * 15 - ux * 5, by_ - py * 15 - uy * 5)],
                (0.20, 0.14, 0.10), shadow=False, lw=1.4)
            ellipse(k, bx, by_, 8.5, 8.5, GOLD, seed + 18, shadow=False, lw=1.6)
            ellipse(k, bx, by_, 5.6, 5.6, (0.97, 0.97, 0.95), seed + 19, shadow=False, lw=1.0)
        c.set_source_rgba(*OIL, 0.75); c.set_line_width(1.6); c.set_line_cap(1)   # oil in the creases
        for t in (-0.45, 0.0, 0.45):
            qx, qy = hx + ux * 6 + px * t * HAND, hy_ + uy * 6 + py * t * HAND
            c.move_to(qx, qy); c.line_to(qx + ux * 8, qy + uy * 8); c.stroke()
        hands.append((hx, hy_))
    hy = HY
    c.save(); c.translate(0, hy + 55); c.scale(HEAD, HEAD); c.translate(0, -(hy + 55))   # about the chin
    pts = _head_pts(k, hy, seed + 20)
    for sx in (-1, 1):
        ellipse(k, sx * 47, hy + 2, 7, 11, SKIN, seed + 26 + sx, shadow=False, lw=2)
    cut(k, pts, SKIN)

    def inside():
        c.move_to(*pts[0])
        for q in pts[1:]:
            c.line_to(*q)
        c.close_path(); c.clip()
    if v["chin"] in ("stubble", "moustache"):                                # a day's shadow on the jaw
        c.save(); inside()
        c.set_source_rgba(0.20, 0.15, 0.13, 0.22 if v["chin"] == "stubble" else 0.10)
        c.move_to(-54, hy + 14); c.curve_to(-34, hy + 22, -27, hy + 24, -23, hy + 38)
        c.curve_to(-10, hy + 24, 10, hy + 24, 23, hy + 38); c.curve_to(27, hy + 24, 34, hy + 22, 54, hy + 14)
        c.line_to(54, hy + 70); c.line_to(-54, hy + 70); c.close_path(); c.fill()
        c.restore()
    if v["chin"] == "beard":                                                 # short, kept, going grey at the chin
        c.save(); inside()
        c.move_to(-54, hy + 2); c.curve_to(-40, hy + 12, -30, hy + 20, -25, hy + 26)
        c.curve_to(-12, hy + 20, 12, hy + 20, 25, hy + 26); c.curve_to(30, hy + 20, 40, hy + 12, 54, hy + 2)
        c.line_to(54, hy + 70); c.line_to(-54, hy + 70); c.close_path()
        c.set_source_rgb(0.30, 0.23, 0.19); c.fill()
        c.set_source_rgba(*GREY, 0.85)
        c.move_to(-16, hy + 44); c.curve_to(-6, hy + 40, 6, hy + 40, 16, hy + 44); c.line_to(12, hy + 62)
        c.line_to(-12, hy + 62); c.close_path(); c.fill()
        c.restore()
        c.set_source_rgb(*INK); c.set_line_width(2.0)
        c.move_to(-47, hy + 6); c.curve_to(-38, hy + 13, -30, hy + 20, -25, hy + 26)
        c.curve_to(-12, hy + 20, 12, hy + 20, 25, hy + 26); c.curve_to(30, hy + 20, 38, hy + 13, 47, hy + 6); c.stroke()
    if v["head"] == "swept":                                                 # swept back, grey at the temples
        cut(k, [(-47, hy - 2), (-50, hy - 30), (-40, hy - 54), (-10, hy - 66), (24, hy - 64), (46, hy - 46), (50, hy - 24),
                (47, hy - 2), (42, hy - 20), (28, hy - 36), (2, hy - 40), (-24, hy - 36), (-40, hy - 20)], HAIR,
            shadow=False, lw=2)
        for sx in (-1, 1):
            cut(k, [(sx * 47, hy - 2), (sx * 49, hy - 26), (sx * 41, hy - 30), (sx * 39, hy - 14)], GREY, shadow=False,
                lw=1.6)
        c.set_source_rgba(1, 1, 1, 0.20); c.set_line_width(2.6); c.set_line_cap(1)
        for dy in (0, 9):
            c.move_to(-26, hy - 50 + dy); c.curve_to(-6, hy - 60 + dy, 14, hy - 58 + dy, 32, hy - 46 + dy); c.stroke()
    elif v["head"] == "curls":                                               # short dark curls, some grey in them
        r = k.rng(seed + 33)
        for sx in (-1, 1):
            cut(k, [(sx * 46, hy + 2), (sx * 48, hy - 20), (sx * 40, hy - 22), (sx * 39, hy - 8)], GREY, shadow=False, lw=1.6)
        spots = [(-42, -28), (-36, -44), (-22, -55), (-6, -60), (11, -60), (27, -54), (38, -43), (43, -28), (-26, -38),
                 (-9, -44), (9, -44), (26, -38)]
        for i, (dx, dy) in enumerate(spots):
            ellipse(k, dx, hy + dy, 11.5, 10.5, HAIR, seed + 34 + i, shadow=False, lw=1.8)
        c.set_source_rgba(1, 1, 1, 0.16); c.set_line_width(2.0)
        for dx, dy in spots[1:7]:
            c.arc(dx + r.uniform(-1, 1), hy + dy, 6, 3.6, 5.2); c.stroke()
    else:                                                                    # a flat cap; grey at the sides
        for sx in (-1, 1):
            cut(k, [(sx * 47, hy + 2), (sx * 49, hy - 22), (sx * 41, hy - 24), (sx * 40, hy - 8)], GREY, shadow=False, lw=1.6)
        cap, cap_d = (0.46, 0.42, 0.36), (0.34, 0.30, 0.25)
        cut(k, [(-52, hy - 24), (-50, hy - 44), (-30, hy - 60), (0, hy - 66), (32, hy - 62), (52, hy - 46), (56, hy - 24)],
            cap, shadow=False, lw=2)
        c.set_source_rgb(*cap_d); c.set_line_width(1.6)
        for dx in (-28, -6, 18, 40):
            c.move_to(dx, hy - 26); c.curve_to(dx + 2, hy - 44, dx + 6, hy - 54, dx + 12, hy - 60); c.stroke()
        ellipse(k, 6, hy - 24, 56, 8.5, cap_d, seed + 39, shadow=False, lw=2)   # the brim
    _face(k, hy + 4, face, look, mouth, seed + 30, v["chin"])
    c.restore()
    c.restore()
    return {"head": (x, feet + hy * s), "hands": [(x + hx * s, feet + hy_ * s) for hx, hy_ in hands],
            "top": feet + TOP * s}
