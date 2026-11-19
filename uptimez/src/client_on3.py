"""v2 (client_on3_v1.py = v1, kept), after the outside review of sheet v1 and Tomas's answers (19 Nov, 1A 2A 3A):
v3 (19 Nov, cast sheet v6): strip=True, the robe pulled off his shoulders and stopped at the gloves (5.1). Default
draws exactly as v2; client_on3_v2.py is v2, pinned.
- TWO OUTFITS. outfit="street": a charcoal hooded tracksuit, hood up, the garages' gear small on the chest (a symbol,
  never words), dark trainers. On the street the gloves are the only red. outfit="ring" (default): the red robe, as v1,
  from the arena on. The gloves never come off in either.
- A HARD FACE, "hard": his neutral in the dream. Heavy brows low and tipped toward the nose, eyes 15 % smaller under
  a lower lid, the mouth pressed straight with one corner down, a crease between the brows. He shows almost nothing;
  the wide eyes are kept for "shock", so the contrast is the joke. His head, jaw and hair are not changed.
- In the dream his stubble is darker (he dreams himself harder than he is). Awake it is as in episodes 9-11.
THE CLIENT, "Office Noir 3: The Last Round", v1: the boxer of his own dream.
His head is The Onboarding's (client_ob v3: the same face, hair, stubble and faces), drawn by client_ob itself and
kept; everything below the jaw is this film's:
- a RED HOODED ROBE, knee length, ivory shawl collar, ivory belt and cuffs; the garages' gear on the chest in ivory
  (a symbol, never words). Hood up on the street, down in the ring. He never takes it off;
- RED BOXING GLOVES, larger than his hands, an ivory laced cuff; he never takes them off either: no fingers;
- bare shins and black lace-up boxing boots.
The robe and the gloves are the film's red: sofia_on.HEART and one darker red for folds (ACCENTS keeps both).
Options: hood=True, tape=True (Pam's strip over his brow), cig=True (a cigarette in the corner of his mouth),
note=True (a banknote clamped between his two gloves), awake=True (the twin: a red dressing gown, bare hands, his
watch; no hood, no gloves, no gear).
Usage: o = boxer(k, x, feet, s, pose, face, look, mouth=None, hood=False, tape=False, cig=False, note=False)
Returns {"head", "hands", "top"} in canvas coordinates. Poses: "b_walk", "b_fist" (one glove raised: his finger),
"b_ask" (both gloves up, nothing he can do with them), "b_pay", "b_guard", "b_swing", "b_reach" (up, for the roll).
client_ob draws exactly as before; nothing in it is changed. Beside the series' other figures he is drawn at 0.70
of their scale, as in The Onboarding (his units are larger)."""
import math
import kit
import client_ob as co
import sofia_on as son
from kit import INK, cut, rect, ellipse
from cand_bc import limb, _d

KEY = son.HEART                                            # the one red
SHADE = (0.60, 0.07, 0.11)                                 # its folds (Office Noir 2's GOWN_SHADE)
ACCENTS = [(KEY, 1.0), (SHADE, 1.0)]
IVORY = (0.95, 0.93, 0.88)
IVORY_EDGE = (0.62, 0.60, 0.56)
BOOT = (0.07, 0.07, 0.08)
SOLE = (0.86, 0.84, 0.80)
GOWN = (0.62, 0.10, 0.14)                                  # awake: towelling, a duller red
GOWN_SHADE = (0.44, 0.06, 0.10)
NOTE = (0.90, 0.93, 0.86)
PAPER = (0.98, 0.97, 0.94)
CHAR = (0.31, 0.31, 0.35)                                  # the tracksuit: charcoal, not black, so it holds on a night street
CHAR_DARK = (0.22, 0.22, 0.25)
CHAR_LINE = (0.52, 0.52, 0.57)                             # its seams and folds, lighter than the cloth
TRAINER = (0.09, 0.09, 0.10)
co.FACES["hard"] = dict(bl=(-1, 6), br=(6, -1), lid=0.30, eye=8.6, iris=4.9, lift=(0, 0), tilt=0.0)   # a new name only
BT, HIP, HY, SH, LN1, LN2 = co.BT, co.HIP, co.HY, co.SH, co.LN1, co.LN2
GLOVE = 33                                                 # his hand is 24
HEM = -74
REL = 0.70                                                 # his scale beside the series' other figures

_ik = co._ik
POSES = {
    "b_walk": (-9, 6, 9, -6),
    "b_fist": (-9, 6, 104, 76),                            # the upper arm out, the forearm straight up
    "b_ask": _ik(-1, -36, BT + 84) + _ik(1, 36, BT + 84),
    "b_pay": _ik(-1, -36, BT + 84) + _ik(1, 36, BT + 84),  # the same hold; the note is what differs
    "b_guard": (-40, -165, 40, 165),                       # elbows out, both gloves up beside his jaw
    "b_swing": (-9, 6, 96, -4),                        # one glove out, the whole arm behind it
    "b_reach": (-9, 6, 152, 24),                           # up, as far as the arm goes
}


def _head_xf(c, face):
    """The transform client_ob draws his head in (after translate, scale and the upper body's tilt)."""
    f = co.FACES[face]
    back = {"shock": (5, -6), "dawning": (2, -3)}.get(face, (0, 0))
    c.translate(back[0], HY + 55 + back[1]); c.rotate(f["tilt"] - co.TILT * 0.6); c.scale(co.HEAD, co.HEAD)
    c.translate(0, -(HY + 55))


def _upper(c):
    c.translate(-4, HIP); c.rotate(co.TILT); c.translate(0, -HIP)


def _glove(k, hx, hy, ux, uy, side, seed, col=None, shade=None):
    """A boxing glove on the end of a sleeve: the mitt, the thumb toward the body, an ivory laced cuff."""
    c = k.c
    col, shade = col or KEY, shade or SHADE
    px, py = -uy, ux
    wx, wy = hx - ux * (GLOVE - 4), hy - uy * (GLOVE - 4)
    cut(k, [(wx + px * 24 - ux * 15, wy + py * 24 - uy * 15), (wx + px * 25, wy + py * 25), (wx - px * 25, wy - py * 25),
            (wx - px * 24 - ux * 15, wy - py * 24 - uy * 15)], IVORY, shadow=False, lw=2)
    c.set_source_rgb(*IVORY_EDGE); c.set_line_width(1.5)
    for t in (-0.5, 0.0, 0.5):                             # the laces
        qx, qy = wx + px * 20 * t - ux * 12, wy + py * 20 * t - uy * 12
        c.move_to(qx, qy); c.line_to(qx + ux * 9 + px * 5, qy + uy * 9 + py * 5); c.stroke()
    ellipse(k, hx + ux * 4, hy + uy * 4, GLOVE, GLOVE * 0.94, col, seed, shadow=False, lw=2.4)
    tx, ty = hx - px * side * 21 - ux * 6, hy - py * side * 21 - uy * 6      # the thumb, on the body's side
    c.save(); c.translate(tx, ty); c.rotate(math.atan2(uy, ux))
    ellipse(k, 0, 0, 17, 11.5, col, seed + 1, shadow=False, lw=2.2)
    c.restore()
    c.set_source_rgb(*shade); c.set_line_width(2.2); c.set_line_cap(1)        # the seam across the knuckles
    c.move_to(hx + ux * 16 + px * 18, hy + uy * 16 + py * 18)
    c.curve_to(hx + ux * 26 + px * 6, hy + uy * 26 + py * 6, hx + ux * 26 - px * 6, hy + uy * 26 - py * 6,
               hx + ux * 16 - px * 18, hy + uy * 16 - py * 18); c.stroke()
    c.set_source_rgba(1, 1, 1, 0.85); c.set_line_width(3.2)                  # leather: one highlight
    c.move_to(hx - ux * 6 + px * side * 19, hy - uy * 6 + py * side * 19)
    c.line_to(hx + ux * 8 + px * side * 21, hy + uy * 8 + py * side * 21); c.stroke()


def banknote(k, x, y, s=1.0, ang=0.0, seed=0):
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    cut(k, [(-34, -17), (34, -17), (34, 17), (-34, 17)], NOTE, lw=2)
    c.set_source_rgb(*INK); c.set_line_width(1.3); c.rectangle(-29, -12, 58, 24); c.stroke()
    kit.text(k, "100", 0, 0, 20, INK)
    c.restore()


def _lower_ring(k, seed, R, RS, awake):
    c = k.c
    for (x0, x1, x2, x3) in ((-46, -12, -12, -44), (20, 54, 60, 28)):
        cut(k, [(x0, HEM - 6), (x1, HEM - 6), (x2, -38), (x3, -38)], co.SKIN, shadow=False, lw=2)
    if not awake:
        for cx, rx, (x0, x1, x2, x3) in ((-28, 27, (-47, -11, -10, -46)), (46, 31, (26, 60, 64, 28))):
            ellipse(k, cx, -3, rx, 7, SOLE, seed + 1 + cx, lw=2)
            ellipse(k, cx, -9, rx, 11, BOOT, seed + 2 + cx, shadow=False, lw=2)
            cut(k, [(x0, -54), (x1, -54), (x2, -12), (x3, -12)], BOOT, shadow=False, lw=2)          # the high shaft
            c.set_source_rgb(*IVORY); c.set_line_width(1.8); c.set_line_cap(1)
            mx = (x0 + x1) / 2
            for i in range(4):                                                                        # the laces
                c.move_to(mx - 8, -48 + i * 9); c.line_to(mx + 8, -44 + i * 9); c.stroke()
    else:
        for cx, rx, (x0, x1, x2, x3) in ((-28, 25, (-44, -12, -13, -43)), (46, 28, (28, 58, 61, 31))):
            cut(k, [(x0, -40), (x1, -40), (x2, -10), (x3, -10)], co.SKIN, shadow=False, lw=2)
            ellipse(k, cx, -7, rx, 10, (0.36, 0.26, 0.20), seed + 3 + cx, lw=2)                       # a slipper
    cut(k, [(-70, HIP - 12), (70, HIP - 12), (86, HEM + 2), (44, HEM + 6), (8, HEM), (-32, HEM + 6), (-78, HEM + 2)], R, lw=2.4)
    if not awake:                                          # an ivory band above the hem
        cut(k, [(-76, HEM - 20), (-32, HEM - 16), (8, HEM - 22), (44, HEM - 16), (84, HEM - 20), (83, HEM - 9), (44, HEM - 5),
                (8, HEM - 11), (-32, HEM - 5), (-75, HEM - 9)], IVORY, shadow=False, lw=1.6)
    c.set_source_rgb(*RS); c.set_line_width(2.4); c.set_line_cap(1)                               # the skirt's folds
    for x0, x1 in ((-46, -52), (-18, -22), (40, 50), (62, 72)):
        c.move_to(x0, HIP + 22); c.line_to(x1, HEM - (24 if not awake else 2)); c.stroke()
    c.set_source_rgb(*INK); c.set_line_width(2.0); c.move_to(6, HIP); c.line_to(12, HEM + 1); c.stroke()   # the front edge


def _lower_street(k, seed):
    """Tracksuit trousers, cuffed, and dark trainers with a pale sole (so his feet read on wet stones)."""
    c = k.c
    for cx, rx in ((-28, 27), (46, 31)):
        ellipse(k, cx, -3, rx, 7, SOLE, seed + 1 + cx, lw=2)
        ellipse(k, cx, -10, rx, 11, TRAINER, seed + 2 + cx, shadow=False, lw=2)
    cut(k, [(-2, HIP - 4), (-56, HIP - 4), (-48, -22), (-10, -22)], CHAR, shadow=False, lw=2.2)
    cut(k, [(2, HIP - 4), (56, HIP - 4), (64, -22), (26, -22)], CHAR, shadow=False, lw=2.2)
    for (x0, x1) in ((-49, -9), (25, 65)):                                                         # the cuffs
        cut(k, [(x0, -30), (x1, -30), (x1 - 1, -14), (x0 + 1, -14)], CHAR_DARK, shadow=False, lw=1.8)
    c.set_source_rgb(*CHAR_LINE); c.set_line_width(2.0); c.set_line_cap(1)
    c.move_to(-44, HIP + 30); c.line_to(-41, -34); c.stroke()
    c.move_to(48, HIP + 30); c.line_to(56, -34); c.stroke()


def _torso_ring(k, seed, R, RS, awake, hood):
    c = k.c
    bt = BT
    if not hood:                                           # the hood, down: a roll behind his neck
        cut(k, [(-78, bt + 14), (-66, bt - 34), (-30, bt - 50), (30, bt - 50), (66, bt - 34), (78, bt + 14)], R, lw=2.4)
        c.set_source_rgb(*RS); c.set_line_width(2.2)
        c.move_to(-58, bt - 26); c.curve_to(-30, bt - 38, 30, bt - 38, 58, bt - 26); c.stroke()
    rect(k, -27, bt - 22, 54, 30, co.SKIN, seed + 5, shadow=False, lw=2)                          # the neck
    cut(k, [(-98, bt + 32), (-82, bt + 3), (-38, bt - 9), (38, bt - 9), (82, bt + 3), (98, bt + 32), (94, bt + 96),
            (72, HIP + 4), (-72, HIP + 4), (-94, bt + 96)], R, lw=2.4)
    cut(k, [(0, bt + 86), (-25, bt - 9), (25, bt - 9)], co.SKIN, shadow=False, lw=1.8)             # his chest, in the V
    c.set_source_rgba(*co.HAIR, 0.55); c.set_line_width(1.5); c.set_line_cap(1)
    for dx, dy in ((-7, 22), (5, 26), (-2, 38), (8, 44), (-6, 52), (2, 62)):
        c.move_to(dx, bt + dy); c.curve_to(dx + 2, bt + dy - 4, dx + 5, bt + dy - 4, dx + 6, bt + dy + 1); c.stroke()
    for sx in (-1, 1):                                                                            # the shawl collar
        cut(k, [(sx * 23, bt - 11), (sx * 46, bt - 8), (sx * 16, bt + 78), (0, bt + 98), (0, bt + 80)], IVORY,
            shadow=False, lw=2)
    c.set_source_rgb(*RS); c.set_line_width(2.4)
    c.move_to(-60, bt + 50); c.curve_to(-52, bt + 80, -50, bt + 104, -54, HIP - 16); c.stroke()
    c.move_to(60, bt + 46); c.curve_to(54, bt + 80, 52, bt + 104, 56, HIP - 16); c.stroke()
    rect(k, -73, HIP - 15, 146, 17, IVORY, seed + 46, shadow=False, lw=1.8)                       # the belt, knotted
    for dx, ln in ((-8, 44), (9, 52)):
        cut(k, [(12, HIP - 6), (22, HIP - 6), (22 + dx + 6, HIP - 6 + ln), (22 + dx - 6, HIP - 8 + ln)], IVORY,
            shadow=False, lw=1.6)
    ellipse(k, 17, HIP - 6, 9.5, 9, IVORY, seed + 47, shadow=False, lw=1.8)
    if not awake:
        co.gear(k, 56, bt + 60, 16, col=IVORY, seed=seed + 42)                                  # the garages' mark
        c.set_source_rgba(1, 1, 1, 0.55); c.set_line_width(3.4); c.set_line_cap(1)                # satin: one long highlight
        c.move_to(-80, bt + 40); c.curve_to(-76, bt + 70, -74, bt + 96, -70, HIP - 22); c.stroke()


def _torso_strip(k, seed, R, RS):
    """v3, strip=True (5.1): the robe pulled back off his shoulders and down to the belt. His chest is bare; the robe
    hangs behind him from his elbows, its ivory collar turned out."""
    c = k.c
    bt = BT
    cut(k, [(-124, bt + 74), (-100, bt + 56), (100, bt + 56), (124, bt + 74), (108, HIP + 4), (-108, HIP + 4)], R, lw=2.4)
    for sx in (-1, 1):
        cut(k, [(sx * 124, bt + 74), (sx * 100, bt + 56), (sx * 92, bt + 70), (sx * 114, bt + 90)], IVORY, shadow=False, lw=1.8)
    rect(k, -27, bt - 22, 54, 30, co.SKIN, seed + 5, shadow=False, lw=2)
    cut(k, [(-98, bt + 32), (-82, bt + 3), (-38, bt - 9), (38, bt - 9), (82, bt + 3), (98, bt + 32), (94, bt + 96),
            (72, HIP + 4), (-72, HIP + 4), (-94, bt + 96)], co.SKIN, lw=2.4)
    c.set_source_rgba(*co.SKIN_DARK, 0.95); c.set_line_width(2.4); c.set_line_cap(1)
    for sx in (-1, 1):                                                                            # the chest, the belly
        c.move_to(sx * 6, bt + 74); c.curve_to(sx * 26, bt + 90, sx * 62, bt + 86, sx * 76, bt + 54); c.stroke()
    c.move_to(-46, HIP - 30); c.curve_to(-20, HIP - 20, 20, HIP - 20, 46, HIP - 30); c.stroke()
    c.set_source_rgba(*co.HAIR, 0.55); c.set_line_width(1.5)
    for dx, dy in ((-7, 22), (5, 26), (-2, 38), (8, 44), (-6, 52), (2, 62), (-24, 40), (22, 38), (-34, 54), (32, 56),
                   (-18, 62), (16, 66), (-2, 84), (4, 100)):
        c.move_to(dx, bt + dy); c.curve_to(dx + 2, bt + dy - 4, dx + 5, bt + dy - 4, dx + 6, bt + dy + 1); c.stroke()
    rect(k, -73, HIP - 15, 146, 17, IVORY, seed + 46, shadow=False, lw=1.8)                       # the belt holds
    for dx, ln in ((-8, 44), (9, 52)):
        cut(k, [(12, HIP - 6), (22, HIP - 6), (22 + dx + 6, HIP - 6 + ln), (22 + dx - 6, HIP - 8 + ln)], IVORY,
            shadow=False, lw=1.6)
    ellipse(k, 17, HIP - 6, 9.5, 9, IVORY, seed + 47, shadow=False, lw=1.8)


def _torso_street(k, seed, hood):
    """A pullover hoodie: a ribbed hem, a pouch pocket, two cords, the garages' gear small on the chest."""
    c = k.c
    bt = BT
    if not hood:
        cut(k, [(-78, bt + 14), (-66, bt - 34), (-30, bt - 50), (30, bt - 50), (66, bt - 34), (78, bt + 14)], CHAR, lw=2.4)
    rect(k, -27, bt - 22, 54, 30, co.SKIN, seed + 5, shadow=False, lw=2)
    cut(k, [(-98, bt + 32), (-82, bt + 3), (-38, bt - 9), (38, bt - 9), (82, bt + 3), (98, bt + 32), (94, bt + 96),
            (76, HIP + 14), (-76, HIP + 14), (-94, bt + 96)], CHAR, lw=2.4)
    cut(k, [(-76, HIP + 2), (76, HIP + 2), (75, HIP + 18), (-75, HIP + 18)], CHAR_DARK, shadow=False, lw=1.8)   # the hem
    cut(k, [(0, bt + 22), (-22, bt - 9), (22, bt - 9)], co.SKIN, shadow=False, lw=1.8)             # the neck of it
    cut(k, [(-44, HIP - 56), (44, HIP - 56), (58, HIP - 6), (-58, HIP - 6)], CHAR, shadow=False, lw=2)          # the pouch
    c.set_source_rgb(*CHAR_LINE); c.set_line_width(2.0); c.set_line_cap(1)
    for sx in (-1, 1):
        c.move_to(sx * 44, HIP - 56); c.line_to(sx * 58, HIP - 6); c.stroke()
        c.move_to(sx * 62, bt + 50); c.curve_to(sx * 56, bt + 76, sx * 56, bt + 96, sx * 60, HIP - 62); c.stroke()
    c.set_source_rgb(*INK); c.set_line_width(4.6)                                                 # the cords
    for sx, ln in ((-1, 58), (1, 50)):
        c.move_to(sx * 13, bt + 6); c.line_to(sx * 15, bt + ln); c.stroke()
    c.set_source_rgb(*IVORY); c.set_line_width(2.6)
    for sx, ln in ((-1, 58), (1, 50)):
        c.move_to(sx * 13, bt + 6); c.line_to(sx * 15, bt + ln); c.stroke()
    co.gear(k, 58, bt + 52, 10, col=IVORY, seed=seed + 42)                                      # small, never words


def _harden(k, c, face, mouth, seed, awake):
    """In the head's transform: the darker stubble of the dream, and the hard face's own mouth and crease."""
    if awake:
        return
    hy = HY
    y = hy + 4
    my = y + 34
    pts = co._head_pts(k, hy, seed + 20)
    if face == "hard" and not mouth:                       # the mouth client_ob drew for an unknown face, taken off
        sk = tuple(a * 0.83 + b_ * 0.17 for a, b_ in zip(co.SKIN, (0.20, 0.15, 0.13)))
        ellipse(k, 4, my, 22, 8.5, sk, seed + 97, shadow=False, outline=False)
    c.save()
    c.new_path(); c.move_to(*pts[0])
    for q in pts[1:]:
        c.line_to(*q)
    c.close_path(); c.clip()
    c.set_source_rgba(0.14, 0.10, 0.09, 0.20)
    c.move_to(-56, hy + 12); c.curve_to(-36, hy + 22, -28, hy + 24, -24, hy + 39)
    c.curve_to(-10, hy + 25, 10, hy + 25, 24, hy + 39); c.curve_to(28, hy + 24, 36, hy + 20, 56, hy + 8)
    c.line_to(56, hy + 72); c.line_to(-56, hy + 72); c.close_path(); c.fill()
    c.restore()
    if face == "hard":
        c.set_source_rgb(*INK); c.set_line_cap(1)
        if not mouth:                                      # pressed straight, one corner down
            c.set_line_width(4.0); c.move_to(-15, my + 0.5); c.line_to(14, my); c.stroke()
            c.set_line_width(2.6); c.move_to(14, my); c.curve_to(18, my + 1, 20, my + 4, 20, my + 7); c.stroke()
        c.set_source_rgba(*co.SKIN_DARK, 0.95); c.set_line_width(2.2)                              # between the brows
        c.move_to(-2, y - 22); c.line_to(-1, y - 13); c.stroke()
        c.move_to(4, y - 21); c.line_to(3, y - 14); c.stroke()
        c.set_line_width(1.8)                                                                      # under the eyes
        for sx in (-17, 17):
            c.move_to(sx - 8, y + 6); c.curve_to(sx - 3, y + 10, sx + 4, y + 10, sx + 9, y + 6); c.stroke()


def boxer(k, x, feet, s=1.0, pose="b_walk", face="confident", look=(0, 0), seed=900, mouth=None, hood=None,
          tape=False, cig=False, note=False, awake=False, outfit="ring", strip=False):
    c = k.c
    a = POSES[pose] if isinstance(pose, str) else pose
    street = outfit == "street" and not awake
    strip = strip and not street and not awake              # v3: the robe half off, in the ring only
    if strip:
        hood = False
    if hood is None:
        hood = street                                      # up on the street, down in the ring
    R, RS = (GOWN, GOWN_SHADE) if awake else (CHAR, CHAR_LINE) if street else (KEY, SHADE)
    c.save(); c.translate(x, feet); c.scale(s, s)
    if street:
        _lower_street(k, seed)
    else:
        _lower_ring(k, seed, R, RS, awake)
    _upper(c)
    bt = BT
    HOOD = [(-70, HY + 58), (-74, HY - 30), (-50, HY - 84), (0, HY - 100), (50, HY - 84), (74, HY - 30), (70, HY + 58)]
    if hood:                                               # the hood, behind his head
        cut(k, HOOD, R, lw=2.4)
    if street:
        _torso_street(k, seed, hood)
    elif strip:
        _torso_strip(k, seed, R, RS)
    else:
        _torso_ring(k, seed, R, RS, awake, hood)
    hands = []
    for side, (u, f_) in ((-1, (a[0], a[1])), (1, (a[2], a[3]))):
        sy_ = bt + 26 + (5 if side < 0 else 0)
        sx_ = side * SH[0]
        ex, ey = sx_ + _d(u)[0] * LN1, sy_ + _d(u)[1] * LN1
        UP = co.SKIN if strip else R                         # v3: bare to the elbow when the robe is half off
        hx, hy_ = limb(k, sx_, sy_, u, f_, LN1, LN2, 50, 43, UP, R, co.SKIN if awake else R, co.HAND if awake else 4,
                       seed + 10 + side)
        ellipse(k, side * (SH[0] - 1), sy_ - 1, 24, 21, UP, seed + 14 + side, shadow=False, lw=2)   # the shoulder
        c.set_source_rgb(*UP); c.rectangle(min(side * 60, side * 86), sy_ - 12, 26, 32); c.fill()
        if strip:                                            # the sleeve, bunched at the elbow: it stops at the glove
            ellipse(k, ex, ey, 34, 27, R, seed + 16 + side, shadow=False, lw=2.2)
            c.set_source_rgb(*RS); c.set_line_width(2.2); c.set_line_cap(1)
            for d_ in (-12, 0, 12):
                c.move_to(ex + d_ - 5, ey - 15); c.curve_to(ex + d_ + 3, ey - 5, ex + d_ - 7, ey + 5, ex + d_ + 2, ey + 16); c.stroke()
        ux, uy = (hx - ex) / LN2, (hy_ - ey) / LN2
        px, py = -uy, ux
        if awake:
            wx, wy = hx - ux * (co.HAND + 1), hy_ - uy * (co.HAND + 1)                           # a towelling cuff
            cut(k, [(wx + px * 23 - ux * 12, wy + py * 23 - uy * 12), (wx + px * 23, wy + py * 23),
                    (wx - px * 23, wy - py * 23), (wx - px * 23 - ux * 12, wy - py * 23 - uy * 12)], GOWN_SHADE,
                shadow=False, lw=1.8)
            if side == 1:                                                                        # the good watch
                bx, by_ = hx - ux * (co.HAND - 8), hy_ - uy * (co.HAND - 8)
                cut(k, [(bx + px * 17 - ux * 5, by_ + py * 17 - uy * 5), (bx + px * 17 + ux * 5, by_ + py * 17 + uy * 5),
                        (bx - px * 17 + ux * 5, by_ - py * 17 + uy * 5), (bx - px * 17 - ux * 5, by_ - py * 17 - uy * 5)],
                    co.STEEL, shadow=False, lw=1.4)
                ellipse(k, bx, by_, 10, 10, co.GOLD, seed + 18, shadow=False, lw=1.6)
                ellipse(k, bx, by_, 6.4, 6.4, (0.10, 0.16, 0.14), seed + 19, shadow=False, lw=1.0)
        else:
            _glove(k, hx, hy_, ux, uy, side, seed + 60 + side)
        hands.append((hx, hy_))
    if note and not awake:                                                                        # clamped between two gloves
        (lx, ly), (rx, ry) = hands
        banknote(k, (lx + rx) / 2 + 4, (ly + ry) / 2 - 30, 1.25, -0.08, seed + 80)
    c.restore()
    # his head: client_ob's own drawing, kept whole, clipped to the head
    c.save()
    c.save(); c.translate(x, feet); c.scale(s, s); _upper(c); _head_xf(c, face)
    pts = co._head_pts(k, HY, seed + 20)
    c.new_path()
    c.move_to(pts[0][0] * 1.04, HY + (pts[0][1] - HY) * 1.04)
    for qx, qy in pts[1:]:
        c.line_to(qx * 1.04, HY + (qy - HY) * 1.04)
    c.close_path()
    c.rectangle(-62, HY - 84, 124, 86)
    for sx in (-1, 1):
        c.save(); c.translate(sx * 48, HY + 2); c.scale(10, 15); c.new_sub_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
    c.restore()
    c.clip()
    co.client(k, x, feet, s, "open", face, look=look, seed=seed, mouth=mouth, roll=False, badge=False)
    c.restore()
    c.save(); c.translate(x, feet); c.scale(s, s); _upper(c)
    c.save(); _head_xf(c, face); _harden(k, c, face, mouth, seed, awake); c.restore()
    if hood:                                               # the hood's rim, in front of his hair and ears
        c.new_path()
        c.move_to(*HOOD[0])
        for q in HOOD[1:]:
            c.line_to(*q)
        c.close_path()
        c.save(); c.translate(0, HY + 10); c.scale(45, 56); c.new_sub_path(); c.arc_negative(0, 0, 1, 2 * math.pi, 0); c.restore()
        c.set_source_rgb(*R); c.fill()
        c.set_source_rgb(*INK); c.set_line_width(2.4)
        c.save(); c.translate(0, HY + 10); c.scale(45, 56); c.new_sub_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.stroke()
        c.move_to(*HOOD[0])
        for q in HOOD[1:]:
            c.line_to(*q)
        c.stroke()
        c.set_source_rgb(*RS); c.set_line_width(2.2); c.set_line_cap(1)
        c.move_to(-56, HY - 40); c.curve_to(-40, HY - 74, 40, HY - 74, 56, HY - 40); c.stroke()
        if street:                                         # a pale edge where the lamp catches the hood
            c.set_source_rgba(0.86, 0.86, 0.90, 0.9); c.set_line_width(2.6)
            c.move_to(-69, HY - 28); c.line_to(-47, HY - 80); c.line_to(-2, HY - 95); c.stroke()
    c.save(); _head_xf(c, face)
    if tape:                                               # Pam's strip, over the nicked brow
        cut(k, [(8, HY - 34), (38, HY - 28), (36, HY - 16), (6, HY - 22)], PAPER, shadow=False, lw=1.6)
        c.set_source_rgb(*IVORY_EDGE); c.set_line_width(1.2)
        for t in (0.3, 0.7):
            c.move_to(8 + 30 * t, HY - 34 + 6 * t); c.line_to(6 + 30 * t, HY - 22 + 6 * t); c.stroke()
    if cig:                                                # in the corner of his mouth; he cannot hold it
        c.save(); c.translate(15, HY + 39); c.rotate(0.22)
        cut(k, [(0, -3), (30, -3), (30, 3), (0, 3)], PAPER, shadow=False, lw=1.4)
        c.set_source_rgb(0.55, 0.55, 0.57); c.rectangle(26, -3, 4, 6); c.fill()
        c.restore()
    c.restore()
    c.restore()
    top = feet + (HY - (100 if hood else 70)) * s
    return {"head": (x - 4 * s, feet + HY * s), "hands": [(x + (hx - 4) * s, feet + hy_ * s) for hx, hy_ in hands],
            "top": top}


def robot_glove(k, x, y, s=1.0, ang=math.pi, seed=950):
    """The other corner's glove, grey, on a steel piston: for frame 0. (x, y) is the middle of the mitt; ang is the
    way it travels (pi = from screen right to left)."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    ux, uy = math.cos(ang), math.sin(ang)
    px, py = -uy, ux
    bx, by = -ux * (GLOVE + 6), -uy * (GLOVE + 6)
    cut(k, [(bx + px * 11, by + py * 11), (bx - ux * 170 + px * 11, by - uy * 170 + py * 11),
            (bx - ux * 170 - px * 11, by - uy * 170 - py * 11), (bx - px * 11, by - py * 11)], (0.78, 0.80, 0.84), shadow=False, lw=2)
    cut(k, [(bx - ux * 40 + px * 17, by - uy * 40 + py * 17), (bx - ux * 170 + px * 17, by - uy * 170 + py * 17),
            (bx - ux * 170 - px * 17, by - uy * 170 - py * 17), (bx - ux * 40 - px * 17, by - uy * 40 - py * 17)],
        (0.52, 0.54, 0.60), shadow=False, lw=2)
    _glove(k, 0, 0, ux, uy, 1, seed, col=(0.36, 0.37, 0.40), shade=(0.18, 0.18, 0.20))
    c.restore()
