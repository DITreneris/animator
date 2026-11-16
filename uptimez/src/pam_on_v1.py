"""PAM, "Office Noir", v1: the only honest thing in Don's dream. Built on pam_ss (untouched; swapped pieces are
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
BLOUSE = (0.95, 0.92, 0.85)
BLOUSE_SHADE = (0.80, 0.76, 0.68)
SKIRT = (0.20, 0.20, 0.23)
STOCKING = (0.70, 0.60, 0.55)
PUMP = (0.10, 0.10, 0.11)
PEARL = (0.97, 0.96, 0.92)
HAIR = (76 / 255, 43 / 255, 23 / 255)      # her brown bob
HEM = pm.HEM
BT = pm.BT
HY = pm.HY


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
        c.set_source_rgb(*HOOP_GOLD); c.set_line_width(1.5)
        for sx in (-17, 17):
            pm.half_moon(c, x + sx, top, 25, 10); c.stroke()
        for sx in (-1, 1):
            c.move_to(x + sx * 29, top + 1); c.line_to(x + sx * 42, top + 2); c.stroke()
    return draw


def hair_roll(k, x, y, s=1.0, seed=0):
    """The low 1940s roll along the bottom of her bob (head centre x, y)."""
    c = k.c
    for sx in (-1, 1):                                      # one smooth roll each side, under the bob's ends
        rx, ry = x + sx * 46 * s, y + 18 * s
        c.new_path(); c.save(); c.translate(rx, ry); c.rotate(sx * 0.35); c.scale(10 * s, 15 * s)
        c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        c.set_source_rgb(*HAIR); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1.8 * s); c.stroke()
        c.set_source_rgba(1, 1, 1, 0.30); c.set_line_width(1.6 * s)
        c.new_path(); c.arc(rx, ry, 6 * s, math.pi * 1.1, math.pi * 1.7); c.stroke()


def pam_noir(k, x, feet, s=1.0, pose="stand", face="neutral", look=(0, 0), glasses="low", mouth=None, lean=0.0,
             seed=40, roll=True):
    saved = [(pm, "PURPLE", pm.PURPLE), (pm, "PURPLE_DARK", pm.PURPLE_DARK), (pm, "GOLD", pm.GOLD),
             (pm, "_costume", pm._costume), (px, "_legs", px._legs), (pm, "glasses_draw", pm.glasses_draw)]
    fk, lk = face, look
    if face == "curious":
        fk, lk = "neutral", (0.3, 0.6)
    elif face == "knowing":
        fk, lk = "rest", look if look != (0, 0) else (1.0, -0.1)
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
    if face == "knowing" and not mouth:                   # the small knowing smile: corners lifted, closed
        hx, hy = out["head"]
        c = k.c
        c.set_source_rgb(*ps.ROSE_LINE); c.set_line_width(2.0 * s); c.set_line_cap(1)
        for sx in (-1, 1):
            c.new_path(); c.move_to(hx + sx * 9 * s, hy + 31 * s); c.line_to(hx + sx * 13 * s, hy + 28 * s); c.stroke()
        c.set_line_cap(0)
    return out
