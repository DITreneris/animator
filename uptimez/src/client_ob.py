"""THE ONBOARDING: the Client, v3 (client_ob_v2.py = v2, client_ob_v1.py = the three look options, both kept).
v2 read as a worker, not as the man who owns ten garages: the jacket was a uniform (knit cuffs, zipped up, a
company patch), the bunch of keys and the rag were a mechanic's, the face was weary. Same man, same olive, now
dressed and carried as the owner:
  - a good olive field jacket with a brown cord collar, worn OPEN over a white open-necked shirt, a leather belt,
    white shirt cuffs under the sleeves; no knit cuffs, no zip, no sewn patch;
  - the garages' gear is a small pin on his collar (still a symbol, never words); the rag and the bunch of keys
    are gone; one car fob hangs at his belt;
  - he stands with a hand in his trouser pocket, the jacket pushed back by it, the watch at the pocket's edge;
  - the hands still have oil in the creases: he owns the garages and still opens a bonnet;
  - the face at rest is at ease, not tired: lighter lids and lines, attentive eyes, one corner of the mouth up;
    "warm" is a crooked closed smile with a tilt of the head (for Sofia), not teeth; "suspicious" is new (the
    confidence starting to crack); "shock" keeps his uneven brows, the pupils offset, the jaw dropped to one side;
  - "offer" is an open hand, not a fist.
Below, the notes of v2, which hold except where the list above replaces them.
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
SHIRT = (0.98, 0.97, 0.94)
SHIRT_DARK = (0.80, 0.80, 0.80)
BELT = (0.36, 0.22, 0.13)
CORD = (0.44, 0.29, 0.17)
RAG = (0.80, 0.22, 0.20)
STEEL = (0.80, 0.82, 0.85)
GOLD = (0.88, 0.72, 0.30)
BLUEPRINT = (0.16, 0.38, 0.78)
L, T = 178, 142
HIP = -L
BT = HIP - T
HY = BT - 52                                             # a thick neck: the head sits low between the shoulders
SH = (86, BT + 26)
LN1, LN2 = 63, 60
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


NO_FOB = [False]                                           # fs v32: the 0:48 shot leaves the car fob off


def _ik(side, tx, ty):
    return ik(side * SH[0], SH[1], tx, ty, LN1, LN2, side)


POCKET = _ik(1, 38, HIP + 6)                              # his right hand in his trouser pocket, the jacket pushed back
CARRY = _ik(-1, -66, BT + 136)                            # his left arm clamped on the blueprint
POSES = {
    "arrive": CARRY + POCKET,                              # how he walks in
    "stand": (-10, 5) + POCKET,
    "offer": CARRY + _ik(1, 176, BT + 100),                # an open hand out to shake, the roll under the other arm
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
# lifts its lower lid (left, right), head tilt, and how far each pupil sits off the look (left, right)
FACES = {
    "confident": dict(bl=(0, 0), br=(-3, -7), lid=0.12, eye=10.0, iris=5.3, lift=(0, 1), tilt=-0.02),
    "warm": dict(bl=(0, -4), br=(-4, 0), lid=0.16, eye=10.0, iris=5.4, lift=(1, 1), tilt=0.07),
    "puzzled": dict(bl=(2, 4), br=(-9, -12), lid=0.04, eye=10.4, iris=4.8, lift=(0, 0), tilt=0.06),
    "suspicious": dict(bl=(4, 7), br=(-6, -9), lid=0.34, eye=10.0, iris=5.0, lift=(0, 0), tilt=-0.05),
    "shock": dict(bl=(-6, -3), br=(-15, -20), lid=0.0, eye=11.2, iris=4.3, lift=(0, 0), tilt=0.03,
                  skew=((-1.6, 0.6), (1.8, -1.0))),
    "exhausted": dict(bl=(4, 5), br=(5, 4), lid=0.44, eye=9.8, iris=5.0, lift=(0, 0), tilt=0.03),
    "relief": dict(bl=(-4, -9), br=(-9, -4), lid=0.22, eye=10.0, iris=5.2, lift=(1, 1), tilt=-0.03),
    "dawning": dict(bl=(-2, 1), br=(-12, -15), lid=0.0, eye=11.0, iris=4.4, lift=(0, 0), tilt=-0.04),
}
FACES["tired"] = FACES["exhausted"]
# opt-in, after the mute test of storyboard v2 (his half-smile read as smirking back at Sofia): a face with nothing in
# it. Level brows, open eyes, a short level mouth: a man answering a question about his postcode.
FACES["plain"] = dict(bl=(0, 0), br=(0, 0), lid=0.06, eye=10.2, iris=5.2, lift=(0, 0), tilt=0.0)


def _face(k, y, face, look, mouth, seed, chin):
    c = k.c
    f = FACES[face]
    lx, ly = look
    ey = y - 5
    c.set_source_rgba(0.86, 0.36, 0.26, 0.11)                                # a little weather on the cheeks
    for sx in (-1, 1):
        c.save(); c.translate(sx * 30, y + 14); c.scale(12, 8); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
    up = {"shock": 5, "dawning": 3, "puzzled": 2}.get(face, 0)               # the forehead, working
    c.set_source_rgba(*SKIN_DARK, 0.85 if up else 0.5); c.set_line_width(1.8 if up else 1.4); c.set_line_cap(1)
    for i, fy in enumerate((y - 36, y - 30) + ((y - 42,) if up > 3 else ())):
        c.move_to(-18 + i * 3, fy - up * 0.4); c.curve_to(-6, fy - 2 - up, 8, fy - 2 - up, 19 - i * 4, fy - up * 0.6); c.stroke()
    for n_, sx in enumerate((-17, 17)):
        R = f["eye"]
        kx, ky = f.get("skew", ((0, 0), (0, 0)))[n_]
        ix, iy = sx + lx * 3.6 + kx, ey + ly * 3.4 + 0.4 + ky
        ellipse(k, sx, ey, R, R, (1, 1, 1), seed + sx, shadow=False, lw=2)
        ellipse(k, ix, iy, f["iris"], f["iris"], (0.36, 0.23, 0.12), seed + sx + 1, shadow=False, outline=False)
        c.set_source_rgb(0.10, 0.07, 0.05); c.arc(ix, iy, f["iris"] * 0.46, 0, 2 * math.pi); c.fill()
        c.set_source_rgb(1, 1, 1); c.arc(ix - 1.8, iy - 1.6, 1.7, 0, 2 * math.pi); c.fill()
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
        if face in ("tired", "exhausted"):                                   # the bag under it
            c.set_source_rgba(*SKIN_DARK, 0.9); c.set_line_width(1.6)
            c.move_to(sx - 8, ey + R + 2); c.curve_to(sx - 3, ey + R + 6, sx + 4, ey + R + 6, sx + 9, ey + R + 1); c.stroke()
        s_ = 1 if sx > 0 else -1                                             # crow's feet
        c.set_source_rgba(*SKIN_DARK, 0.75); c.set_line_width(1.5)
        for dy, dx in ((-3, 5), (3, 5.5)):
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
    elif face == "confident":                                                # at ease: one corner up, almost amused
        c.set_line_width(3.8)
        c.move_to(-16, my - 1); c.curve_to(-6, my + 4, 8, my + 3, 20, my - 7); c.stroke()
        c.set_line_width(2.4); c.move_to(20, my - 7); c.curve_to(25, my - 9, 26, my - 4, 23, my - 1); c.stroke()
    elif face == "warm":                                                     # for Sofia: closed, crooked, real
        c.set_line_width(4.0)
        c.move_to(-20, my - 6); c.curve_to(-10, my + 9, 10, my + 8, 23, my - 10); c.stroke()
        c.set_line_width(2.4)
        c.move_to(23, my - 10); c.curve_to(28, my - 12, 29, my - 6, 26, my - 3); c.stroke()
        c.move_to(-20, my - 6); c.curve_to(-24, my - 7, -24, my - 3, -22, my - 1); c.stroke()
        c.set_source_rgba(*SKIN_DARK, 0.9); c.set_line_width(2.0)             # the lower lip
        c.move_to(-7, my + 10); c.curve_to(-2, my + 12, 5, my + 12, 10, my + 9); c.stroke()
    elif face == "suspicious":                                               # pressed, and pulled to one side
        c.set_line_width(3.8)
        c.move_to(-14, my - 4); c.curve_to(-4, my - 1, 6, my + 1, 16, my + 1); c.stroke()
        c.set_line_width(2.4); c.move_to(-14, my - 4); c.curve_to(-18, my - 6, -19, my - 1, -17, my + 1); c.stroke()
    elif face == "relief":                                                   # the breath going out
        c.move_to(-15, my - 4); c.curve_to(-7, my - 2, 7, my - 2, 16, my - 5)
        c.curve_to(11, my + 9, -10, my + 9, -15, my - 4); c.close_path()
        c.set_source_rgb(0.42, 0.14, 0.14); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.6); c.stroke()
    elif face == "shock":                                                    # the jaw, dropped, and to one side
        c.save(); c.translate(5, my + 4); c.rotate(0.30); c.scale(9.5, 12); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        c.set_source_rgb(0.36, 0.11, 0.12); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.8); c.stroke()
        c.save(); c.translate(5, my + 4); c.rotate(0.30)
        c.set_source_rgb(1, 1, 1); c.rectangle(-6, -10.5, 12, 4); c.fill(); c.restore()
    elif face == "dawning":
        c.save(); c.translate(1, my + 2); c.scale(10, 5.5); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        c.set_source_rgb(0.36, 0.11, 0.12); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.6); c.stroke()
    elif face in ("tired", "exhausted"):
        c.set_line_width(3.6); c.move_to(-13, my); c.curve_to(-5, my - 2, 5, my - 2, 14, my + 2); c.stroke()
    elif face == "plain":                                                    # level, short, closed
        c.set_line_width(3.6); c.move_to(-11, my); c.curve_to(-4, my + 1.5, 5, my + 1.5, 12, my); c.stroke()
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
    ellipse(k, -28, -4, 27, 8, (0.18, 0.12, 0.09), seed + 1, lw=2); ellipse(k, -28, -9, 27, 11, BOOT, seed + 2, shadow=False, lw=2)
    ellipse(k, 46, -4, 31, 8, (0.18, 0.12, 0.09), seed + 3, lw=2); ellipse(k, 46, -9, 31, 11, BOOT, seed + 4, shadow=False, lw=2)
    cut(k, [(-2, HIP - 4), (-54, HIP - 4), (-46, -12), (-10, -12)], TROUSERS, shadow=False, lw=2)
    cut(k, [(2, HIP - 4), (54, HIP - 4), (62, -12), (26, -12)], TROUSERS, shadow=False, lw=2)
    c.set_source_rgb(*TROUSERS_DARK); c.set_line_width(1.8)
    c.move_to(-42, HIP + 30); c.line_to(-39, -16); c.stroke()
    c.move_to(46, HIP + 30); c.line_to(54, -16); c.stroke()
    if not NO_FOB[0]:                                                          # (fs v32: off for one shot)
     c.save(); c.translate(-30, HIP + 8); c.rotate(0.10)                       # his car's fob, at his belt
     c.set_source_rgb(*INK); c.set_line_width(2.2); c.move_to(0, -8); c.line_to(0, 6); c.stroke()
     c.set_source_rgb(*STEEL); c.set_line_width(2.6); c.arc(0, 9, 5.5, 0, 2 * math.pi); c.stroke()
     rect(k, -8, 13, 16, 26, (0.14, 0.14, 0.17), seed + 30, shadow=False, lw=1.5)
     c.set_source_rgb(*STEEL); c.arc(0, 21, 3.4, 0, 2 * math.pi); c.fill()
     c.set_source_rgb(0.85, 0.22, 0.20); c.arc(0, 31, 2.4, 0, 2 * math.pi); c.fill()
     c.restore()
    c.translate(-4, HIP); c.rotate(TILT); c.translate(0, -HIP)                # the upper body, over the straight leg
    bt = BT
    rect(k, -27, bt - 22, 54, 30, SKIN, seed + 5, shadow=False, lw=2)         # the neck: as wide as his jaw
    cut(k, [(-66, bt + 6), (-30, bt - 10), (30, bt - 10), (66, bt + 6), (74, bt + 70), (64, HIP + 4), (-64, HIP + 4),
            (-74, bt + 70)], SHIRT, lw=2.2)                                    # a white shirt, open at the neck
    cut(k, [(0, bt + 34), (-20, bt - 9), (20, bt - 9)], SKIN, shadow=False, lw=1.6)
    for sx in (-1, 1):                                                       # its collar
        cut(k, [(sx * 20, bt - 10), (sx * 40, bt - 6), (sx * 31, bt + 20), (sx * 3, bt + 30)], SHIRT, shadow=False, lw=1.8)
    c.set_source_rgb(*SHIRT_DARK); c.set_line_width(1.8); c.set_line_cap(1)
    c.move_to(0, bt + 34); c.line_to(0, HIP - 8); c.stroke()
    for i, yy in enumerate((bt + 56, bt + 86, bt + 116)):
        ellipse(k, 0, yy, 3.2, 3.2, (0.90, 0.90, 0.88), seed + 44 + i, shadow=False, lw=1.2)
    rect(k, -64, HIP - 8, 128, 13, BELT, seed + 46, shadow=False, lw=1.6)      # a good belt
    rect(k, -9, HIP - 10, 18, 17, STEEL, seed + 47, shadow=False, lw=1.5)
    # the field jacket, open: two fronts; the one over his pocketed hand is pushed back
    cut(k, [(-98, bt + 32), (-82, bt + 3), (-38, bt - 9), (-27, bt + 16), (-25, HIP + 30), (-80, HIP + 30), (-94, bt + 96)],
        J, lw=2.4)
    if pocket:                                                               # swept back behind the hip
        cut(k, [(98, bt + 32), (82, bt + 3), (38, bt - 9), (27, bt + 16), (36, bt + 74), (59, HIP - 8), (62, HIP + 30),
                (84, HIP + 30), (94, bt + 96)], J, lw=2.4)
    else:
        cut(k, [(98, bt + 32), (82, bt + 3), (38, bt - 9), (27, bt + 16), (25, HIP + 30), (80, HIP + 30), (94, bt + 96)],
            J, lw=2.4)
    for sx in (-1, 1):                                                       # the cord collar, and a pocket flap
        cut(k, [(sx * 27, bt + 16), (sx * 32, bt - 12), (sx * 56, bt - 17), (sx * 54, bt + 14), (sx * 31, bt + 44)], CORD,
            shadow=False, lw=1.8)
        if not (pocket and sx > 0):
            cut(k, [(sx * 40, bt + 112), (sx * 84, bt + 112), (sx * 83, bt + 124), (sx * 41, bt + 124)], J, shadow=False,
                lw=1.6)
    gear(k, -44, bt + 20, 7.5, col=GOLD, seed=seed + 42)                        # the garages' mark: a pin on his collar
    if badge:
        visitor(k, 62, bt + 62, 30, -0.06, seed + 50)
    if roll:                                                                 # under the arm: the end sticks out behind
        blueprint_roll(k, -99, bt + 90, -0.42, 214, 11.5, seed + 70)
    hands = []
    for side, (u, f_) in ((-1, (a[0], a[1])), (1, (a[2], a[3]))):
        sy_ = bt + 26 + (5 if side < 0 else 0)
        sx_ = side * SH[0]
        ex, ey = sx_ + _d(u)[0] * LN1, sy_ + _d(u)[1] * LN1
        hr = 17 if (side == 1 and pocket) else HAND                           # in the pocket only the heel of it shows
        hx, hy_ = limb(k, sx_, sy_, u, f_, LN1, LN2, 47, 39, J, J, SKIN, hr, seed + 10 + side)
        ellipse(k, side * (SH[0] - 1), sy_ - 1, 23, 20, J, seed + 14 + side, shadow=False, lw=2)   # the shoulder
        c.set_source_rgb(*J); c.rectangle(min(side * 60, side * 86), sy_ - 12, 26, 32); c.fill()
        ux, uy = (hx - ex) / LN2, (hy_ - ey) / LN2
        px, py = -uy, ux
        wx, wy = hx - ux * (hr + 1), hy_ - uy * (hr + 1)                   # a white shirt cuff under the sleeve
        cut(k, [(wx + px * 19 - ux * 7, wy + py * 19 - uy * 7), (wx + px * 18, wy + py * 18), (wx - px * 18, wy - py * 18),
                (wx - px * 19 - ux * 7, wy - py * 19 - uy * 7)], SHIRT, shadow=False, lw=1.8)
        if side == 1:                                                        # the good watch, below the cuff
            bx, by_ = hx - ux * (hr - 8), hy_ - uy * (hr - 8)
            cut(k, [(bx + px * 17 - ux * 5, by_ + py * 17 - uy * 5), (bx + px * 17 + ux * 5, by_ + py * 17 + uy * 5),
                    (bx - px * 17 + ux * 5, by_ - py * 17 + uy * 5), (bx - px * 17 - ux * 5, by_ - py * 17 - uy * 5)],
                STEEL, shadow=False, lw=1.4)
            ellipse(k, bx, by_, 10, 10, GOLD, seed + 18, shadow=False, lw=1.6)
            ellipse(k, bx, by_, 6.4, 6.4, (0.10, 0.16, 0.14), seed + 19, shadow=False, lw=1.0)
        if side == 1 and pocket:                                             # the hand is in his trouser pocket
            c.set_source_rgb(*TROUSERS)
            c.move_to(hx - 24, hy_ + 4); c.line_to(hx + 18, hy_ - 6); c.line_to(hx + 20, hy_ + 30)
            c.line_to(hx - 24, hy_ + 30); c.close_path(); c.fill()
            c.set_source_rgb(*INK); c.set_line_width(2.4); c.set_line_cap(1)
            c.move_to(hx - 24, hy_ + 4); c.line_to(hx + 18, hy_ - 6); c.stroke()
            c.set_line_width(2.0); c.move_to(hx + 19, hy_ - 5); c.line_to(hx + 21, hy_ + 30); c.stroke()
        elif side == 1 and pose == "offer":                                  # an open hand: the edge of the palm, the thumb up
            c.save(); c.translate(hx, hy_); c.rotate(math.atan2(uy, ux))
            cut(k, [(-14, -17), (24, -19), (44, -12), (47, 6), (40, 17), (-14, 19)], SKIN, shadow=False, lw=2)
            ellipse(k, 4, -24, 9, 15, SKIN, seed + 17, shadow=False, lw=2)
            c.set_source_rgb(*SKIN); c.rectangle(-4, -18, 16, 8); c.fill()
            c.set_source_rgba(*OIL, 0.7); c.set_line_width(1.6); c.set_line_cap(1)
            for yy in (-6, 3, 11):
                c.move_to(24, yy); c.line_to(42, yy + 1); c.stroke()
            c.restore()
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
        c.set_source_rgba(0.20, 0.15, 0.13, 0.17 if v["chin"] == "stubble" else 0.10)
        c.move_to(-56, hy + 12); c.curve_to(-36, hy + 22, -28, hy + 24, -24, hy + 39)
        c.curve_to(-10, hy + 25, 10, hy + 25, 24, hy + 39); c.curve_to(28, hy + 24, 36, hy + 20, 56, hy + 8)
        c.line_to(56, hy + 72); c.line_to(-56, hy + 72); c.close_path(); c.fill()
        r = k.rng(seed + 27)
        c.set_source_rgba(0.16, 0.11, 0.10, 0.42); c.set_line_width(1.3); c.set_line_cap(1)
        for _ in range(26):
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
