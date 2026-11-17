"""v2, pinned (client_ob.py is v3).
THE ONBOARDING: the Client, v2 (client_ob_v1.py = v1, the three look options, kept). After the character design
audit of v1 ("readable, but not memorable": a mechanic, not an owner; no dominant silhouette feature; symmetrical
like a game extra; all three faces too nice), look B is the base and is revised:
  - he stands like an owner: weight on one leg, that shoulder lower, a hand in his jacket pocket, chin level;
  - the blueprint is carried under his arm, its end sticking out behind his shoulder: the silhouette's one cue;
  - a barrel chest, a thick neck, heavier hands (physical authority, not just a larger scale);
  - a lived-in face: heavier brows with a nick through one of them, a nose that was broken once, uneven stubble,
    a loose strand of hair; grey temples and the olive jacket stay;
  - the faces are far apart: "confident" (how he arrives: a half-smile, almost amused), "warm", "puzzled", "shock"
    (brows up unevenly, jaw dropped, the neck pulled back), "tired", "relief", "dawning";
  - fewer small things on the jacket: no chest pocket, one larger gear-and-wrench mark, no hem band.
Kept from the brief: ten garages, rugged and warm, a head taller than Don, a clean work jacket, a rag in the back
pocket, oil in the creases of his hands, a good watch, a ring of keys with his car's fob, VISITOR, nothing blue
but the blueprint. LOOKS still holds A, B and C (jacket and head); B is the default and the only one developed.

Usage: o = client(k, x, feet, s, pose, face, look, mouth=None, variant="B", roll=None, badge=True)
Returns {"head", "hands", "top"} in canvas coordinates. pose: a name in POSES or (a1, a2, b1, b2) degrees
(0 = down, +90 = screen right, 180 = up). roll=None draws the blueprint when the pose carries it ("arrive")."""
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
HY = BT - 52                                             # a thick neck: the head sits low between the shoulders
SH = (86, BT + 26)
LN1, LN2 = 62, 58
HAND = 24
HEAD = 1.10
TOP = HY - 70
TILT = -0.035                                            # the upper body, tipped toward the leg that carries him

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


POCKET = _ik(1, 52, BT + 122)                             # his right hand in the jacket pocket, the elbow out
CARRY = _ik(-1, -66, BT + 136)                            # his left arm clamped on the blueprint
POSES = {
    "arrive": CARRY + POCKET,                              # how he walks in
    "stand": (-10, 5) + POCKET,
    "offer": CARRY + _ik(1, 168, BT + 92),                 # a hand out to shake, the roll still under the other arm
    "open": (-10, 5, 10, -5),                              # both hands free
}
IN_POCKET = ("arrive", "stand")
CARRIES = ("arrive", "offer")


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
    c.close_path(); c.set_source_rgb(*col); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1.3); c.stroke()
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
    for yy in (-ln * 0.36, -ln * 0.05, ln * 0.30):
        c.move_to(-r + 3, yy); c.line_to(r - 3, yy + 4); c.stroke()
    for end in (-1, 1):
        ellipse(k, 0, end * ln / 2, r, r * 0.42, (0.97, 0.97, 0.99), seed + 3 + end, shadow=False, lw=1.8)
        c.set_source_rgb(*BLUEPRINT); c.set_line_width(1.4)
        c.save(); c.translate(0, end * ln / 2); c.scale(1, 0.42); c.arc(0, 0, r * 0.5, 0.4, 5.4); c.restore(); c.stroke()
    c.restore()


def keys(k, x, y, seed=0):
    """A ring of keys on a clip, with the car's fob: one ring, three keys, one fob."""
    c = k.c
    c.set_source_rgb(*INK); c.set_line_width(2.4); c.move_to(x, y - 12); c.line_to(x, y); c.stroke()
    for i, a in enumerate((-0.75, -0.25, 0.25)):
        c.save(); c.translate(x, y + 9); c.rotate(a)
        rect(k, -3, 5, 6, 25, STEEL if i % 2 else GOLD, seed + 10 + i, shadow=False, lw=1.3)
        c.restore()
    c.save(); c.translate(x, y + 9); c.rotate(0.82)                           # the fob
    rect(k, -8, 8, 16, 27, (0.14, 0.14, 0.17), seed + 30, shadow=False, lw=1.5)
    c.set_source_rgb(0.85, 0.22, 0.20); c.arc(0, 17, 3.0, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(*STEEL); c.arc(0, 27, 2.4, 0, 2 * math.pi); c.fill()
    c.restore()
    c.set_source_rgb(*STEEL); c.set_line_width(3.0); c.arc(x, y + 9, 8, 0, 2 * math.pi); c.stroke()
    c.set_source_rgb(*INK); c.set_line_width(1.1); c.arc(x, y + 9, 9.6, 0, 2 * math.pi); c.stroke()


def _head_pts(k, hy, seed):
    """Square and soft: wide at the cheekbones, a broad jaw that has rounded off."""
    r = k.rng(seed)
    pts = []
    n = 34
    for i in range(n):
        a = 2 * math.pi * i / n
        cs, sn = math.cos(a), math.sin(a)
        if sn > 0:
            px = math.copysign(abs(cs) ** 0.50, cs) * 48.5
            py = (sn ** 0.76) * 55
        else:
            px, py = cs * 46, sn * 49
        pts.append((px * (1 + r.uniform(-0.01, 0.01)), hy + py * (1 + r.uniform(-0.01, 0.01))))
    return pts


# face -> brows (left: outer dy, inner dy; right: inner dy, outer dy), upper lid, eye and iris size, which cheek
# lifts its lower lid (left, right), head tilt
FACES = {
    "confident": dict(bl=(1, 1), br=(-5, -9), lid=0.20, eye=9.8, iris=4.9, lift=(0, 1), tilt=-0.02),
    "warm": dict(bl=(1, -3), br=(-3, 1), lid=0.14, eye=9.8, iris=4.9, lift=(1, 1), tilt=0.02),
    "puzzled": dict(bl=(2, 4), br=(-9, -12), lid=0.04, eye=10.4, iris=4.6, lift=(0, 0), tilt=0.06),
    "shock": dict(bl=(-13, -9), br=(-17, -20), lid=0.0, eye=12.2, iris=3.9, lift=(0, 0), tilt=0.0),
    "tired": dict(bl=(4, 5), br=(5, 4), lid=0.44, eye=9.6, iris=4.9, lift=(0, 0), tilt=0.03),
    "relief": dict(bl=(-4, -9), br=(-9, -4), lid=0.22, eye=9.8, iris=4.9, lift=(1, 1), tilt=-0.03),
    "dawning": dict(bl=(-2, 1), br=(-12, -15), lid=0.0, eye=11.2, iris=4.2, lift=(0, 0), tilt=-0.04),
}


def _face(k, y, face, look, mouth, seed, chin):
    c = k.c
    f = FACES[face]
    lx, ly = look
    ey = y - 5
    c.set_source_rgba(0.86, 0.36, 0.26, 0.20)                                # weather on the cheeks
    for sx in (-1, 1):
        c.save(); c.translate(sx * 30, y + 14); c.scale(12, 8); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
    up = {"shock": 5, "dawning": 3, "puzzled": 2}.get(face, 0)               # the forehead, working
    c.set_source_rgba(*SKIN_DARK, 0.85); c.set_line_width(1.8 if up else 1.5); c.set_line_cap(1)
    for i, fy in enumerate((y - 36, y - 30) + ((y - 42,) if up > 3 else ())):
        c.move_to(-18 + i * 3, fy - up * 0.4); c.curve_to(-6, fy - 2 - up, 8, fy - 2 - up, 19 - i * 4, fy - up * 0.6); c.stroke()
    for n_, sx in enumerate((-17, 17)):
        R = f["eye"]
        ellipse(k, sx, ey, R, R, (1, 1, 1), seed + sx, shadow=False, lw=2)
        ellipse(k, sx + lx * 3.6, ey + ly * 3.4 + 0.6, f["iris"], f["iris"], (0.34, 0.22, 0.12), seed + sx + 1,
                shadow=False, outline=False)
        c.set_source_rgb(1, 1, 1); c.arc(sx + lx * 3.6 - 1.6, ey + ly * 3.4 - 1.2, 1.5, 0, 2 * math.pi); c.fill()
        lid = f["lid"]
        if lid:
            c.save(); c.arc(sx, ey, R + 0.8, 0, 2 * math.pi); c.clip()
            c.set_source_rgb(*SKIN); c.rectangle(sx - R - 1, ey - R - 1, 2 * R + 2, (2 * R + 1) * lid); c.fill()
            c.restore()
            yy = ey - R - 0.6 + (2 * R + 1) * lid
            _brow(c, sx - R * 0.92, yy, sx + R * 0.92, yy, 2.4)
        if f["lift"][n_]:                                                    # the cheek lifts the lower lid
            c.set_source_rgb(*SKIN); c.rectangle(sx - R - 1, ey + R * 0.66, 2 * R + 2, 6); c.fill()
            c.set_source_rgb(*INK); c.set_line_width(2.0); c.set_line_cap(1)
            c.move_to(sx - R * 0.9, ey + R * 0.74); c.curve_to(sx - 4, ey + R * 0.5, sx + 4, ey + R * 0.5, sx + R * 0.9,
                                                               ey + R * 0.74); c.stroke()
        if face == "tired":                                                  # the bag under it
            c.set_source_rgba(*SKIN_DARK, 0.9); c.set_line_width(1.6)
            c.move_to(sx - 8, ey + R + 2); c.curve_to(sx - 3, ey + R + 6, sx + 4, ey + R + 6, sx + 9, ey + R + 1); c.stroke()
        s_ = 1 if sx > 0 else -1                                             # crow's feet
        c.set_source_rgba(*SKIN_DARK, 0.9); c.set_line_width(1.6)
        for dy, dx in ((-4, 6), (1, 7), (6, 5)):
            c.move_to(sx + s_ * (R + 2.6), ey + dy * 0.6 + 2); c.line_to(sx + s_ * (R + 2.6 + dx), ey + dy + 2); c.stroke()
    by = y - 23                                                              # heavy brows
    (a1, a2), (b1, b2) = f["bl"], f["br"]
    _brow(c, -32, by + a1, -7, by + a2, 8.0); _brow(c, 7, by + b1, 32, by + b2, 8.0)
    c.set_source_rgb(*SKIN); c.set_line_width(2.6); c.set_line_cap(0)         # the nick through one of them
    mx_, my_ = 24, by + b1 + (b2 - b1) * (24 - 7) / 25.0
    c.move_to(mx_ - 2.5, my_ - 6); c.line_to(mx_ + 2.5, my_ + 6); c.stroke()
    c.set_source_rgb(*SKIN_DARK); c.set_line_width(3.0); c.set_line_cap(1); c.set_line_join(1)   # broken once, set badly
    c.move_to(-3, y - 8); c.line_to(3, y + 1); c.curve_to(-1, y + 7, -12, y + 12, -9, y + 18)
    c.curve_to(-4, y + 22, 6, y + 22, 10, y + 17); c.stroke()
    c.set_line_width(2.2); c.move_to(10, y + 17); c.curve_to(13, y + 13, 11, y + 9, 7, y + 9); c.stroke()
    my = y + 34
    c.set_source_rgba(*SKIN_DARK, 0.9); c.set_line_width(2.0)                 # the lines a smile has worn in
    for sx in (-1, 1):
        c.move_to(sx * 14, y + 17); c.curve_to(sx * 23, y + 23, sx * 26, y + 31, sx * 23, my + 3); c.stroke()
    c.set_source_rgb(*INK); c.set_line_cap(1)
    if mouth:
        im.mouth(k, 0, my, mouth, SKIN, erase=(1, 1), seed=seed + 96)
    elif face == "confident":                                                # a half-smile: one corner, almost amused
        c.set_line_width(3.8)
        c.move_to(-16, my + 1); c.curve_to(-6, my + 3, 8, my + 3, 20, my - 8); c.stroke()
        c.set_line_width(2.4); c.move_to(20, my - 8); c.curve_to(25, my - 10, 26, my - 5, 23, my - 2); c.stroke()
    elif face == "warm":
        c.move_to(-20, my - 6); c.curve_to(-10, my - 3, 10, my - 3, 21, my - 7)
        c.curve_to(15, my + 10, -14, my + 10, -20, my - 6); c.close_path()
        c.set_source_rgb(1, 1, 1); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.6); c.stroke()
    elif face == "relief":                                                   # the breath going out
        c.move_to(-15, my - 4); c.curve_to(-7, my - 2, 7, my - 2, 16, my - 5)
        c.curve_to(11, my + 9, -10, my + 9, -15, my - 4); c.close_path()
        c.set_source_rgb(0.42, 0.14, 0.14); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.6); c.stroke()
    elif face == "shock":                                                    # the jaw, dropped
        c.save(); c.translate(1, my + 5); c.scale(11, 13); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        c.set_source_rgb(0.36, 0.11, 0.12); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.8); c.stroke()
        c.set_source_rgb(1, 1, 1); c.rectangle(-6, my - 7, 14, 4); c.fill()
    elif face == "dawning":
        c.save(); c.translate(1, my + 2); c.scale(10, 5.5); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        c.set_source_rgb(0.36, 0.11, 0.12); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.6); c.stroke()
    elif face == "tired":
        c.set_line_width(3.6); c.move_to(-13, my); c.curve_to(-5, my - 2, 5, my - 2, 14, my + 2); c.stroke()
    else:                                                                    # puzzled: pulled to one side
        c.set_line_width(3.6); c.move_to(-8, my + 2); c.curve_to(0, my - 2, 8, my + 3, 17, my - 3); c.stroke()
    if chin == "moustache":
        cut(k, [(-22, my - 5), (-12, my - 13), (0, my - 11), (12, my - 13), (22, my - 5), (12, my - 3), (0, my - 5),
                (-12, my - 3)], (0.42, 0.37, 0.34), shadow=False, lw=2)


def client(k, x, feet, s=1.0, pose="arrive", face="confident", look=(0, 0), seed=900, mouth=None, variant="B",
           roll=None, badge=True):
    c = k.c
    v = LOOKS[variant]
    J, JD, COL = v["jacket"], v["dark"], v["collar"]
    a = POSES[pose] if isinstance(pose, str) else pose
    pocket = pose in IN_POCKET
    if roll is None:
        roll = pose in CARRIES
    c.save(); c.translate(x, feet); c.scale(s, s)
    # the leg that carries him (screen left) is straight; the other is set out to the side, the foot turned
    ellipse(k, -28, -4, 27, 9, SOLE, seed + 1, lw=2); ellipse(k, -28, -9, 27, 11, BOOT, seed + 2, shadow=False, lw=2)
    ellipse(k, 46, -4, 31, 9, SOLE, seed + 3, lw=2); ellipse(k, 46, -9, 31, 11, BOOT, seed + 4, shadow=False, lw=2)
    cut(k, [(-2, HIP - 4), (-54, HIP - 4), (-46, -12), (-10, -12)], TROUSERS, shadow=False, lw=2)
    cut(k, [(2, HIP - 4), (54, HIP - 4), (62, -12), (26, -12)], TROUSERS, shadow=False, lw=2)
    c.set_source_rgb(*TROUSERS_DARK); c.set_line_width(1.8)
    c.move_to(-42, HIP + 30); c.line_to(-39, -16); c.stroke()
    c.move_to(46, HIP + 30); c.line_to(54, -16); c.stroke()
    cut(k, [(58, HIP + 12), (78, HIP + 18), (80, HIP + 48), (67, HIP + 58), (59, HIP + 42)], RAG, shadow=False, lw=1.8)  # the rag
    c.set_source_rgba(*OIL, 0.8)
    for dx, dy in ((66, 30), (72, 42), (63, 46)):
        c.arc(dx, HIP + dy, 2.2, 0, 2 * math.pi); c.fill()
    keys(k, -22, HIP + 16, seed + 60)
    c.translate(-4, HIP); c.rotate(TILT); c.translate(0, -HIP)                # the upper body, over the straight leg
    bt = BT
    rect(k, -27, bt - 22, 54, 30, SKIN, seed + 5, shadow=False, lw=2)         # the neck: as wide as his jaw
    cut(k, [(-98, bt + 32), (-82, bt + 3), (-32, bt - 10), (32, bt - 10), (82, bt + 3), (98, bt + 32), (94, bt + 96),
            (76, HIP + 14), (-76, HIP + 14), (-94, bt + 96)], J, lw=2.4)      # a barrel, widest at the chest
    cut(k, [(0, bt + 50), (-24, bt - 9), (24, bt - 9)], TEE, shadow=False, lw=1.6)
    for sx in (-1, 1):                                                       # the collar
        cut(k, [(sx * 24, bt - 9), (sx * 50, bt - 16), (sx * 42, bt + 22), (sx * 5, bt + 48)], COL, shadow=False, lw=1.8)
    c.set_source_rgb(*JD); c.set_line_width(2.4); c.set_line_cap(1)
    c.move_to(0, bt + 50); c.line_to(0, HIP + 12); c.stroke()                 # the zip
    c.move_to(-80, bt + 84); c.curve_to(-40, bt + 100, 40, bt + 100, 80, bt + 84); c.stroke()   # the chest, carried forward
    gear(k, -47, bt + 58, 13, seed=seed + 42)
    if badge:
        visitor(k, 46, bt + 54, 32, -0.06, seed + 50)
    if roll:                                                                 # under the arm: the end sticks out behind
        blueprint_roll(k, -99, bt + 90, -0.42, 214, 11.5, seed + 70)
    hands = []
    for side, (u, f_) in ((-1, (a[0], a[1])), (1, (a[2], a[3]))):
        sy_ = bt + 26 + (5 if side < 0 else 0)
        sx_ = side * SH[0]
        ex, ey = sx_ + _d(u)[0] * LN1, sy_ + _d(u)[1] * LN1
        hx, hy_ = limb(k, sx_, sy_, u, f_, LN1, LN2, 47, 39, J, J, SKIN, HAND, seed + 10 + side)
        ellipse(k, side * (SH[0] - 1), sy_ - 1, 23, 20, J, seed + 14 + side, shadow=False, lw=2)   # the shoulder
        c.set_source_rgb(*J); c.rectangle(min(side * 58, side * 86), sy_ - 12, 28, 32); c.fill()
        ux, uy = (hx - ex) / LN2, (hy_ - ey) / LN2
        px, py = -uy, ux
        wx, wy = hx - ux * (HAND + 2), hy_ - uy * (HAND + 2)                   # the knit cuff
        cut(k, [(wx + px * 21 - ux * 9, wy + py * 21 - uy * 9), (wx + px * 20, wy + py * 20), (wx - px * 20, wy - py * 20),
                (wx - px * 21 - ux * 9, wy - py * 21 - uy * 9)], COL, shadow=False, lw=1.8)
        if side == 1:                                                        # the good watch, below the cuff
            bx, by_ = hx - ux * (HAND - 7), hy_ - uy * (HAND - 7)
            cut(k, [(bx + px * 17 - ux * 5, by_ + py * 17 - uy * 5), (bx + px * 17 + ux * 5, by_ + py * 17 + uy * 5),
                    (bx - px * 17 + ux * 5, by_ - py * 17 + uy * 5), (bx - px * 17 - ux * 5, by_ - py * 17 - uy * 5)],
                (0.20, 0.14, 0.10), shadow=False, lw=1.4)
            ellipse(k, bx, by_, 9.5, 9.5, GOLD, seed + 18, shadow=False, lw=1.6)
            ellipse(k, bx, by_, 6.2, 6.2, (0.97, 0.97, 0.95), seed + 19, shadow=False, lw=1.0)
        if side == 1 and pocket:                                             # the hand is in the jacket pocket:
            c.set_source_rgb(*J)                                             # only the wrist and the watch show
            c.move_to(hx - 32, hy_ - 16); c.line_to(hx + 27, hy_ - 5); c.line_to(hx + 25, hy_ + 27)
            c.line_to(hx - 32, hy_ + 27); c.close_path(); c.fill()
            c.set_source_rgb(*INK); c.set_line_width(5.2); c.set_line_cap(1)
            c.move_to(hx - 30, hy_ - 16); c.line_to(hx + 25, hy_ - 5); c.stroke()
            c.set_source_rgb(*JD); c.set_line_width(2.6)
            c.move_to(hx - 30, hy_ - 16); c.line_to(hx + 25, hy_ - 5); c.stroke()
        else:
            c.set_source_rgba(*OIL, 0.75); c.set_line_width(1.8); c.set_line_cap(1)        # oil in the creases
            for t in (-0.45, 0.0, 0.45):
                qx, qy = hx + ux * 7 + px * t * HAND, hy_ + uy * 7 + py * t * HAND
                c.move_to(qx, qy); c.line_to(qx + ux * 10, qy + uy * 10); c.stroke()
        hands.append((hx, hy_))
    # the head
    f = FACES[face]
    hy = HY
    back = {"shock": (5, -6), "dawning": (2, -3)}.get(face, (0, 0))            # the neck, pulled back
    c.save(); c.translate(back[0], hy + 55 + back[1]); c.rotate(f["tilt"] - TILT * 0.6); c.scale(HEAD, HEAD)
    c.translate(0, -(hy + 55))
    pts = _head_pts(k, hy, seed + 20)
    for sx in (-1, 1):
        ellipse(k, sx * 48, hy + 2, 7.5, 12, SKIN, seed + 26 + sx, shadow=False, lw=2)
    cut(k, pts, SKIN)

    def inside():
        c.move_to(*pts[0])
        for q in pts[1:]:
            c.line_to(*q)
        c.close_path(); c.clip()
    if v["chin"] in ("stubble", "moustache"):                                # two days' shadow, and not even
        c.save(); inside()
        c.set_source_rgba(0.20, 0.15, 0.13, 0.26 if v["chin"] == "stubble" else 0.10)
        c.move_to(-56, hy + 12); c.curve_to(-36, hy + 22, -28, hy + 24, -24, hy + 39)
        c.curve_to(-10, hy + 25, 10, hy + 25, 24, hy + 39); c.curve_to(28, hy + 24, 36, hy + 20, 56, hy + 8)
        c.line_to(56, hy + 72); c.line_to(-56, hy + 72); c.close_path(); c.fill()
        r = k.rng(seed + 27)
        c.set_source_rgba(0.16, 0.11, 0.10, 0.55); c.set_line_width(1.3); c.set_line_cap(1)
        for _ in range(46):
            qx = r.uniform(-42, 42); qy = hy + r.uniform(26, 58)
            if abs(qx) < 21 and qy < hy + 44:
                continue                                                     # not across the lips
            c.move_to(qx, qy); c.line_to(qx + r.uniform(-1, 1), qy + 2.6); c.stroke()
        c.restore()
    if v["chin"] == "beard":
        c.save(); inside()
        c.move_to(-54, hy + 2); c.curve_to(-40, hy + 12, -30, hy + 20, -25, hy + 26)
        c.curve_to(-12, hy + 20, 12, hy + 20, 25, hy + 26); c.curve_to(30, hy + 20, 40, hy + 12, 54, hy + 2)
        c.line_to(54, hy + 72); c.line_to(-54, hy + 72); c.close_path()
        c.set_source_rgb(0.30, 0.23, 0.19); c.fill()
        c.restore()
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
        cut(k, [(4, hy - 40), (18, hy - 42), (27, hy - 31), (23, hy - 24), (17, hy - 33)], HAIR, shadow=False, lw=1.6)   # a strand that will not stay back
    elif v["head"] == "curls":
        for sx in (-1, 1):
            cut(k, [(sx * 46, hy + 2), (sx * 48, hy - 20), (sx * 40, hy - 22), (sx * 39, hy - 8)], GREY, shadow=False, lw=1.6)
        spots = [(-42, -28), (-36, -44), (-22, -55), (-6, -60), (11, -60), (27, -54), (38, -43), (43, -28), (-26, -38),
                 (-9, -44), (9, -44), (26, -38)]
        for i, (dx, dy) in enumerate(spots):
            ellipse(k, dx, hy + dy, 11.5, 10.5, HAIR, seed + 34 + i, shadow=False, lw=1.8)
    else:                                                                    # a flat cap; grey at the sides
        for sx in (-1, 1):
            cut(k, [(sx * 47, hy + 2), (sx * 49, hy - 22), (sx * 41, hy - 24), (sx * 40, hy - 8)], GREY, shadow=False, lw=1.6)
        cap, cap_d = (0.46, 0.42, 0.36), (0.34, 0.30, 0.25)
        cut(k, [(-52, hy - 24), (-50, hy - 44), (-30, hy - 60), (0, hy - 66), (32, hy - 62), (52, hy - 46), (56, hy - 24)],
            cap, shadow=False, lw=2)
        ellipse(k, 6, hy - 24, 56, 8.5, cap_d, seed + 39, shadow=False, lw=2)
    if face in ("shock", "dawning"):                                         # the chin, tucked: a second line under it
        c.set_source_rgba(*SKIN_DARK, 0.95); c.set_line_width(2.2); c.set_line_cap(1)
        c.move_to(-24, hy + 52); c.curve_to(-10, hy + 59, 10, hy + 59, 24, hy + 52); c.stroke()
    _face(k, hy + 4, face, look, mouth, seed + 30, v["chin"])
    c.restore()
    c.restore()
    return {"head": (x - 4 * s, feet + hy * s), "hands": [(x + (hx - 4) * s, feet + hy_ * s) for hx, hy_ in hands],
            "top": feet + TOP * s}
