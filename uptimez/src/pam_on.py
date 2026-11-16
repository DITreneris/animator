"""PAM, "Office Noir", v3 (pam_on_v2.py = v2, pam_on_v1.py = v1, kept). v3: the pinning reach across Don's body is
gone. POSE_PRESENT with present=True: she holds the heart up between her fingers in front of her, at chest
height, like evidence (7A); the press onto his lapel becomes a close-up of her fingertips only (fingertips()).
The blouse is a shade darker (light grey in noir) so the heart stays the strongest contrast.
v2 notes: v2 after the review: the side rolls no longer read as
headphones (curled ends low at the jaw with strands inside, and a wave across the crown to break the helmet);
three clearly different faces: "curious" (her raised-brow hopeful eyes), "knowing" (one brow up, an asymmetric
smile: her "smirk"), "delighted" (soft closed eyes, a real smile: her "happy"); thicker gold rims and three bigger
beads on the chain; heart=True puts the red heart at her pressing hand (the pinning action reads on its own).
v1 notes: the only honest thing in Don's dream. Built on pam_ss (untouched; swapped pieces are
restored after every draw):
- 1940s secretary: a cream silk pussy-bow blouse (a soft bow at the neck, a fine placket of pearl buttons), a dark
  charcoal pencil skirt to just below the knee with a waistband, seamed stockings, low pumps; no lanyard, no badge;
- her bob pinned under in a smooth 1940s roll at each side;
- her glasses gold: the half-moon frames get a gold rim and the bead chain is the episode's gold key (HOOP_GOLD,
  shared with Sofia's hoops), kept at 35 % in the noir pass;
- poses: POSE_PRESS(tx, ty) puts her screen-right hand on a point (shot 7: the heart onto Don's lapel);
- faces she uses: "curious" (shot 2: studying the heart, quietly hopeful), "knowing" (shot 7: the small knowing
  smile, eyes on Don), and everything pam_ss has.
Her light (the sheet and the light pass): soft and frontal, the only soft light in the dream.
Usage: o = pam_noir(k, x, feet, s, pose, face, look, glasses="low", mouth=None, lean=0, seed=40)"""
import math
import kit
import pam_ss as ps
import pam_mf as pm
import pam_xmas as px
import pam_tg as pt
from kit import INK, cut, rect, ellipse

HOOP_GOLD = (0.86, 0.68, 0.24)          # the episode's gold key (same as Sofia's hoops)
BLOUSE = (0.84, 0.80, 0.72)         # v3: a shade darker (v2 0.95, 0.92, 0.85)
BLOUSE_SHADE = (0.70, 0.66, 0.58)
SKIRT = (0.20, 0.20, 0.23)
STOCKING = (0.70, 0.60, 0.55)
PUMP = (0.10, 0.10, 0.11)
PEARL = (0.97, 0.96, 0.92)
HAIR = (76 / 255, 43 / 255, 23 / 255)      # her brown bob
HEM = pm.HEM
BT = pm.BT
HY = pm.HY


POSE_PRESENT = (-8, 0) + pm.ik(1, 20, BT + 34)        # v3, 7A: the heart held up in front of her, chest height


def fingertips(k, tip, s=1.0, ang=-0.55, seed=0):
    """v3, 7B: only her fingertips, coming in from off frame along ang (radians, toward the tip), with a sliver of
    blouse cuff; tip = where the index fingertip touches."""
    c = k.c
    c.save(); c.translate(*tip); c.rotate(ang); c.scale(s, s)
    for (dy, ln) in ((-9, 88), (7, 82)):                                        # index and middle finger
        c.new_path(); c.move_to(-ln, dy - 7); c.line_to(-7, dy - 7)
        c.arc(-7, dy, 7, -math.pi / 2, math.pi / 2); c.line_to(-ln, dy + 7); c.close_path()
        c.set_source_rgb(*ps.SKIN); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2); c.stroke()
        c.set_source_rgb(0.85, 0.62, 0.55); c.new_path(); c.arc(-7, dy, 3, -1.2, 1.2); c.fill()   # a nail
    cut(k, [(-150, -24), (-82, -24), (-78, 26), (-150, 26)], ps.SKIN, shadow=False, lw=2)       # the back of her hand
    cut(k, [(-230, -30), (-140, -30), (-136, 32), (-230, 32)], BLOUSE, shadow=False, lw=2)       # her cuff
    c.restore()


def POSE_PRESS(tx, ty):
    return (-8, 0) + pm.ik(1, tx, ty)


def _legs(k, seed, stance=1.0):
    """Pencil skirt to just below the knee, seamed stockings, low pumps."""
    c = k.c
    for sx_ in (-11, 11):
        o = 1 if sx_ > 0 else -1
        cut(k, [(sx_ - 7, -86), (sx_ + 7, -86), (sx_ + 6, -14), (sx_ - 5, -14)], STOCKING, shadow=False, lw=1.8)
        c.set_source_rgb(*INK); c.set_line_width(1.0)
        c.move_to(sx_ + o * 1, -84); c.line_to(sx_ + o * 1, -16); c.stroke()          # the seam
        cut(k, [(sx_ - 7, -16), (sx_ + 7, -16), (sx_ + 7 + o * 8, -2), (sx_ + 7 + o * 8, 0), (sx_ - 7, 0)], PUMP,
            shadow=False, lw=1.6)
    cut(k, [(-40, HEM - 8), (40, HEM - 8), (36, -50), (-36, -50)], SKIRT, lw=2.2)        # the pencil skirt
    c.set_source_rgb(0.08, 0.08, 0.09); c.set_line_width(1.6)
    c.move_to(0, -68); c.line_to(0, -50); c.stroke()                                    # the back-vent hint


def _costume(badge=True):
    def hook(k, name_, p, bt, seed):
        c = k.c
        c.set_source_rgb(*BLOUSE_SHADE); c.set_line_width(1.6)                          # the placket
        c.move_to(0, bt + 28); c.line_to(0, HEM - 10); c.stroke()
        for i, by in enumerate((44, 64, 84, 104)):
            ellipse(k, 0, bt + by, 2.8, 2.8, PEARL, seed + 90 + i, shadow=False, lw=1.0)
        c.set_source_rgb(*BLOUSE_SHADE); c.set_line_width(1.4)                          # soft silk folds
        for sx in (-1, 1):
            c.move_to(sx * 22, bt + 30); c.curve_to(sx * 26, bt + 60, sx * 24, bt + 90, sx * 28, HEM - 12); c.stroke()
        rect(k, -40, HEM - 14, 80, 10, SKIRT, seed + 95, shadow=False, lw=1.8)            # the skirt's waistband
        for sx in (-1, 1):                                                              # the pussy bow
            c.new_path(); c.move_to(0, bt + 6); c.curve_to(sx * 10, bt - 8, sx * 26, bt - 2, sx * 22, bt + 8)
            c.curve_to(sx * 26, bt + 18, sx * 10, bt + 18, 0, bt + 6); c.close_path()
            c.set_source_rgb(*BLOUSE); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1.8); c.stroke()
            c.new_path(); c.move_to(-2 + sx * 2, bt + 10); c.curve_to(sx * 6, bt + 26, sx * 4, bt + 34, sx * 10, bt + 42)
            c.line_to(sx * 16, bt + 38); c.curve_to(sx * 10, bt + 30, sx * 8, bt + 20, 2 + sx * 2, bt + 10); c.close_path()
            c.set_source_rgb(*BLOUSE); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1.6); c.stroke()
        ellipse(k, 0, bt + 7, 5, 5, BLOUSE, seed + 96, shadow=False, lw=1.6)
    return hook


def _glasses_gold(orig):
    def draw(k, x, y, state, seed=0):
        orig(k, x, y, state, seed)
        if state in (None, "off"):
            return
        c = k.c
        top = y - 4 if state == "up" else y + 9
        for col, lw in ((INK, 4.6), (HOOP_GOLD, 2.6)):             # v2: thicker gold rims, a black edge either side
            c.set_source_rgb(*col); c.set_line_width(lw)
            for sx in (-17, 17):
                pm.half_moon(c, x + sx, top, 25, 10); c.stroke()
            for sx in (-1, 1):
                c.move_to(x + sx * 29, top + 1); c.line_to(x + sx * 42, top + 2); c.stroke()
        for sx in (-1, 1):                                          # three bigger beads on each side of the chain
            for t in (0.3, 0.6, 0.9):
                bx = x + sx * 41 + sx * (4 * math.sin(t * math.pi * 0.9))
                by = top + 3 + t * 50
                c.new_path(); c.arc(bx, by, 3.0, 0, 2 * math.pi)
                c.set_source_rgb(*HOOP_GOLD); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(0.9); c.stroke()
    return draw


def hair_roll(k, x, y, s=1.0, seed=0):
    """v2: the bob's ends curled under, low at the jaw (not at the ears), strands drawn inside; a wave across the
    crown breaks the helmet."""
    c = k.c
    for sx in (-1, 1):
        c.save(); c.translate(x + sx * 44 * s, y + 38 * s); c.scale(s, s)
        c.new_path()                                        # a C-shaped curl turning in under the bob
        c.move_to(sx * -4, -16); c.curve_to(sx * 12, -18, sx * 16, -2, sx * 10, 8)
        c.curve_to(sx * 4, 14, sx * -8, 12, sx * -10, 4); c.curve_to(sx * -6, 6, sx * 2, 4, sx * 2, -4)
        c.curve_to(sx * 2, -10, sx * -2, -12, sx * -4, -16); c.close_path()
        c.set_source_rgb(*HAIR); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1.8); c.stroke()
        c.set_source_rgba(1, 1, 1, 0.35); c.set_line_width(1.4)
        for r_ in (9, 5):
            c.new_path(); c.arc(sx * 3, 0, r_, (0.0 if sx > 0 else 0.5) * math.pi - 0.6, (0.5 if sx > 0 else 1.0) * math.pi + 0.2)
            c.stroke()
        c.restore()
    c.set_source_rgba(1, 1, 1, 0.30); c.set_line_width(2.0 * s); c.set_line_cap(1)      # the crown wave
    c.new_path(); c.move_to(x - 30 * s, y - 40 * s); c.curve_to(x - 10 * s, y - 52 * s, x + 6 * s, y - 34 * s, x + 26 * s, y - 46 * s)
    c.stroke()
    c.set_source_rgb(*INK); c.set_line_width(1.4 * s)
    c.new_path(); c.move_to(x - 34 * s, y - 34 * s); c.curve_to(x - 14 * s, y - 46 * s, x + 2 * s, y - 28 * s, x + 22 * s, y - 40 * s)
    c.stroke(); c.set_line_cap(0)


def pam_noir(k, x, feet, s=1.0, pose="stand", face="neutral", look=(0, 0), glasses="low", mouth=None, lean=0.0,
             seed=40, roll=True, heart=False, heart_size=13, present=False):
    saved = [(pm, "PURPLE", pm.PURPLE), (pm, "PURPLE_DARK", pm.PURPLE_DARK), (pm, "GOLD", pm.GOLD),
             (pm, "_costume", pm._costume), (px, "_legs", px._legs), (pm, "glasses_draw", pm.glasses_draw)]
    fk, lk = face, look
    if face == "curious":
        fk, lk = "hopeful", (0.3, 0.6)
    elif face == "knowing":
        fk, lk = "smirk", look if look != (0, 0) else (1.0, -0.1)
    elif face == "delighted":
        fk = "happy"
    try:
        pm.PURPLE, pm.PURPLE_DARK, pm.GOLD = BLOUSE, BLOUSE_SHADE, HOOP_GOLD
        pm._costume, px._legs = _costume, _legs
        pm.glasses_draw = _glasses_gold(saved[5][2])
        out = ps.pam(k, x, feet, s, pose=pose, face=fk, look=lk, seed=seed, badge=False, glasses=glasses,
                     mouth=mouth, lean=lean)
    finally:
        for m, n, v in saved:
            setattr(m, n, v)
    if roll and not lean:
        hx, hy = out["head"]
        hair_roll(k, hx, hy, s, seed)
    if present:                                           # v3: the heart held up between her fingers
        import don_on as d
        hx, hy = out["hands"][1]
        d.heart(k.c, hx + 4 * s, hy - 20 * s, heart_size * s)
        for i, dx in enumerate((-5, 5)):
            ellipse(k, hx + dx * s, hy - 6 * s, 4.5 * s, 7 * s, ps.SKIN, seed + 62 + i, shadow=False, lw=1.5 * s)
    if heart:                                             # the heart under her pressing fingertips
        import don_on as d
        hx, hy = out["hands"][1]
        d.heart(k.c, hx + 16 * s, hy - 2 * s, heart_size * s)
        ellipse(k, hx + 3 * s, hy + 2 * s, 5 * s, 7 * s, ps.SKIN, seed + 61, shadow=False, lw=1.6 * s)
    return out
