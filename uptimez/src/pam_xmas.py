"""v2 (pam_xmas_v1.py = v1, kept), after review:
- the mask is a taller cardboard eye mask with an angled top edge, pointed outer corners, uneven holes and
  a strip of tape on the bridge; before shot 10 it hangs round her neck on its string (mode "neck"), so it
  reads as a mask she hasn't put on yet, not as goggles;
- the cardigan is visibly buttoned one hole off: a diagonal pull, an empty top hole, a loose spare button,
  one side hanging much lower;
- hero stance: feet wider (stance=1.4), elbows further out, the towel spread behind her (cape_flare),
  chin lifted slightly (chin), the same flat face.

v1 notes: PAM, Christmas special ("Happy Compliance"): her first full-size standing figure. Same head, bob, face and
height as before (kit.PEOPLE["PAM"]); drawn through kit.person with kit.BADGE_HOOK and a clip, so every
earlier Pam is untouched.
Her clothes are the most sensible outfit in the building, and the costume is plainly made in five minutes:
- a purple cardigan buttoned one hole off, a white blouse collar, reading glasses on a beaded chain,
  a lanyard with a staff badge and too many keys, beige trousers, white office trainers;
- the hero costume: a dark-blue bath towel for a cape (white stripes, safety-pinned at the neck),
  a cardboard strip mask with two eye holes (pushed up on her forehead, or down over her eyes),
  and a paper "P" taped crooked on the cardigan;
- a thermos, because of course.
Usage: p = pam(k, x, feet, s, pose, face, look, mask="up"|"down"|None, thermos=False, orn=False, seed=40)"""
import math
import kit
import brand
import don_v4 as dv
import sofia_xmas as sx
from kit import INK, cut, rect, ellipse

CARDIGAN = (0.40, 0.27, 0.58)      # her usual purple (kit body colour)
CARDIGAN_DARK = (0.30, 0.19, 0.45)
BLOUSE = (0.98, 0.97, 0.94)
TROUSERS = (0.80, 0.73, 0.60)
TROUSERS_DARK = (0.66, 0.59, 0.47)
TRAINER = (0.97, 0.97, 0.97)
TOWEL = (0.13, 0.22, 0.45)
TOWEL_DARK = (0.08, 0.15, 0.33)
TOWEL_STRIPE = (0.93, 0.94, 0.97)
CARD = (0.80, 0.64, 0.42)          # cardboard
CARD_DARK = (0.62, 0.47, 0.28)
PAPER = (1.0, 0.99, 0.95)
TAPE = (0.96, 0.92, 0.70)
SILVER = (0.74, 0.76, 0.80)
THERMOS = (0.20, 0.52, 0.42)
HEM = -112                          # cardigan hem (local units above the feet)
GLASSES = False                     # v2: reading glasses dropped (v1 had them on a chain)

POSE_THERMOS = (-8, 0, 40, 120)     # right forearm up, thermos at chest height
POSE_FISTS = (-14, 8, 14, -8)       # arms stiff at her sides, fists clenched
HERO = dict(stance=1.4, cape_flare=1.3, chin=0.6)   # v2: the payoff stance's extras
POSE_HERO = (-62, 98, 62, -98)      # v2: fists on hips, elbows well out (v1 (-50, 85, 50, -85))
POSE_TAKE = (-8, 0, 70, 15)         # right arm out, hand open for the ornament


def _cape(k, bt, seed, flare=1.0):
    """The towel, behind her: hangs from the shoulders to the knee, stripes near the hem, a fringe."""
    c = k.c
    hem = -96
    f = flare
    towel = [(-44, bt - 4), (44, bt - 4), (64 * f, bt + 40), (72 * f, hem + 30), (74 * f, hem), (-74 * f, hem),
             (-72 * f, hem + 30), (-64 * f, bt + 40)]
    cut(k, towel, TOWEL, lw=2.2)
    c.save()
    c.move_to(*towel[0])
    for q in towel[1:]:
        c.line_to(*q)
    c.close_path(); c.clip()
    for sy in (hem + 16, hem + 26):
        c.set_source_rgb(*TOWEL_STRIPE); c.rectangle(-100, sy, 200, 5); c.fill()
    c.set_source_rgb(*TOWEL_DARK); c.set_line_width(2.2)
    for fx in (-48, 48):
        c.move_to(fx, bt + 30); c.curve_to(fx * 1.05, bt + 90, fx * 1.12, bt + 150, fx * 1.2, hem + 10); c.stroke()
    c.restore()
    c.set_source_rgb(*INK); c.set_line_width(1.6)                 # fringe
    for fx in range(int(-72 * f), int(74 * f), 6):
        c.move_to(fx, hem); c.line_to(fx, hem + 5); c.stroke()


def _costume(badge=True):
    def hook(k, name_, p, bt, seed):
        c = k.c
        # blouse collar
        for sx_ in (-1, 1):
            cut(k, [(0, bt + 4), (sx_ * 18, bt - 2), (sx_ * 14, bt + 16)], BLOUSE, shadow=False, lw=1.6)
        # towel corners over the shoulders, pinned together under the chin
        for sx_ in (-1, 1):
            cut(k, [(sx_ * 4, bt + 10), (sx_ * 30, bt - 6), (sx_ * 46, bt + 4), (sx_ * 22, bt + 22)], TOWEL,
                shadow=False, lw=1.8)
            c.set_source_rgb(*TOWEL_STRIPE); c.set_line_width(2.4)
            c.move_to(sx_ * 26, bt - 2); c.line_to(sx_ * 40, bt + 6); c.stroke()
        # cardigan front: buttoned one hole off, so the left side hangs lower
        # v2: plainly buttoned one hole off: a crooked placket, buttons pulling diagonally, the top hole empty,
        # a spare button at the bottom and her left side hanging much lower
        c.set_source_rgb(*CARDIGAN_DARK); c.set_line_width(2.6)
        c.move_to(-2, bt + 10); c.curve_to(2, bt + 40, -6, bt + 80, 4, HEM - 6); c.stroke()
        c.set_source_rgb(*INK); c.set_line_width(2)
        c.move_to(-9, bt + 22); c.line_to(-2, bt + 22); c.stroke()                        # the empty top hole
        for i, by in enumerate((32, 54, 76)):
            c.set_source_rgb(*CARDIGAN_DARK); c.set_line_width(2.2)                        # diagonal pull
            c.move_to(-3, bt + by + 1); c.line_to(-24, bt + by + 13); c.stroke()
            c.move_to(-2, bt + by + 5); c.line_to(-16, bt + by + 15); c.stroke()
            ellipse(k, 1, bt + by, 4.4, 4.4, (0.98, 0.88, 0.45), seed + 90 + i, shadow=False, lw=1.6)
        ellipse(k, 9, HEM - 8, 4.4, 4.4, (0.98, 0.88, 0.45), seed + 94, shadow=False, lw=1.6)   # the spare button
        c.set_source_rgb(*CARDIGAN_DARK); c.set_line_width(2)          # rib cuff at the hem
        c.move_to(-40, HEM - 2); c.line_to(41, HEM - 2); c.stroke()
        if GLASSES:                                                    # v1 detail, off in v2 (clutter)
            c.set_source_rgb(*INK); c.set_line_width(1.2)
            for gx in (-11, 9):
                c.set_source_rgb(0.85, 0.93, 0.98); c.arc(gx, bt + 44, 8.5, 0, 2 * math.pi); c.fill_preserve()
                c.set_source_rgb(*INK); c.set_line_width(2.4); c.stroke()
        # paper "P", taped on crooked
        c.save(); c.translate(-20, bt + 94); c.rotate(-0.22)
        rect(k, -14, -15, 28, 30, PAPER, seed + 95, shadow=False, lw=1.6)
        kit.text(k, "P", 0, 8, 22, INK)
        for tx, ty, ta in ((-14, -15, 0.6), (14, -15, -0.6), (14, 15, 0.6)):
            c.save(); c.translate(tx, ty); c.rotate(ta)
            c.set_source_rgba(*TAPE, 0.9); c.rectangle(-6, -2.5, 12, 5); c.fill(); c.restore()
        c.restore()
        # lanyard: badge plus a bunch of keys
        c.set_source_rgb(*brand.GREEN); c.set_line_width(3)
        c.move_to(10, bt + 6); c.line_to(18, bt + 84); c.stroke()
        c.move_to(22, bt + 4); c.line_to(24, bt + 84); c.stroke()
        if badge:
            dv.staff_badge(k, "PAM", 7, bt + 84, 30, 8.5)
        for i, (kx, ka) in enumerate(((30, 0.5), (34, 0.9), (26, 0.2))):
            c.save(); c.translate(kx, bt + 112); c.rotate(ka)
            rect(k, -2, 0, 4, 14, SILVER, seed + 97 + i, shadow=False, lw=1.2)
            c.set_source_rgb(*SILVER); c.arc(0, 0, 4, 0, 2 * math.pi); c.fill_preserve()
            c.set_source_rgb(*INK); c.set_line_width(1.2); c.stroke()
            c.restore()
        # safety pin at the neck, holding the towel
        c.set_source_rgb(*INK); c.set_line_width(3.6); c.set_line_cap(1)
        c.move_to(-14, bt + 6); c.line_to(14, bt + 6); c.stroke()
        c.set_source_rgb(*SILVER); c.set_line_width(2.2)
        c.move_to(-14, bt + 6); c.line_to(14, bt + 6); c.stroke()
        c.arc(16, bt + 6, 3.4, 0, 2 * math.pi); c.stroke()
        rect(k, -20, bt + 2, 7, 8, SILVER, seed + 99, shadow=False, lw=1.2)
    return hook


def _legs(k, seed, stance=1.0):
    c = k.c
    for sx_ in (-15 * stance, 15 * stance):
        top = sx_ / stance                                   # hips stay put; the feet move apart
        cut(k, [(top - 11, HEM - 6), (top + 11, HEM - 6), (sx_ + 10, -12), (sx_ - 10, -12)], TROUSERS, shadow=False, lw=1.8)
        c.set_source_rgb(*TROUSERS_DARK); c.set_line_width(1.6)
        c.move_to(top, HEM + 6); c.line_to(sx_, -16); c.stroke()             # pressed crease
        o = 1 if sx_ > 0 else -1
        ellipse(k, sx_ + o * 3, -6, 15, 8, TRAINER, seed + 70 + sx_, lw=2)
        c.set_source_rgb(0.55, 0.58, 0.64); c.set_line_width(1.6)
        c.move_to(sx_ + o * 3 - 12, -2); c.line_to(sx_ + o * 3 + 12, -2); c.stroke()   # sole line


def mask_strip(k, x, y, mode, seed=0):
    """v2 cardboard eye mask: angled top edge, pointed outer corners, uneven holes, tape on the bridge.
    mode "down" = over her eyes; "neck" = hanging under her chin on its string; "up" = the v1 forehead spot."""
    c = k.c
    if mode == "neck":
        c.set_source_rgb(*INK); c.set_line_width(1.6)                 # string up behind her ears
        c.move_to(x - 40, y + 62); c.curve_to(x - 50, y + 40, x - 50, y + 20, x - 46, y + 8); c.stroke()
        c.move_to(x + 42, y + 60); c.curve_to(x + 52, y + 40, x + 52, y + 20, x + 46, y + 8); c.stroke()
        yy, rot, sc = y + 66, 0.10, 0.9
    elif mode == "up":
        yy, rot, sc = y - 40, -0.12, 1.0
    else:
        yy, rot, sc = y, -0.04, 1.0                                   # a little crooked on her face
    c.save(); c.translate(x, yy); c.rotate(rot); c.scale(sc, sc)
    if mode != "neck":
        c.set_source_rgb(*INK); c.set_line_width(1.6)                 # the string round her head
        c.move_to(-44, 0); c.line_to(-54, -1); c.stroke(); c.move_to(45, -2); c.line_to(54, -3); c.stroke()
    outline = [(-50, -17), (-31, -14), (-11, -12), (0, -6), (11, -12), (31, -15), (51, -19), (44, 1), (33, 12),
               (13, 12), (0, 6), (-13, 12), (-32, 12), (-43, 1)]
    c.move_to(*outline[0])
    for q in outline[1:]:
        c.line_to(*q)
    c.close_path()
    for ex, ey, rx, ry in ((-18, 0, 10.5, 7.5), (19, -1, 12, 8.5)):  # uneven holes, cut by hand
        c.new_sub_path(); c.save(); c.translate(ex, ey); c.scale(rx, ry); c.arc_negative(0, 0, 1, 2 * math.pi, 0); c.restore()
    c.set_fill_rule(0)
    c.set_source_rgb(*CARD); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(2.4); c.stroke()
    c.set_source_rgb(*CARD_DARK); c.set_line_width(1.2)              # corrugation lines
    for cx_ in (-40, 34):
        c.move_to(cx_, -12); c.line_to(cx_ + 1, 6); c.stroke()
    c.save(); c.rotate(0.15)                                          # tape on the bridge
    c.set_source_rgba(*TAPE, 0.92); c.rectangle(-5, -12, 10, 16); c.fill()
    c.restore()
    c.restore()


def thermos(k, hand, s=1.0, seed=60):
    c = k.c
    hx, hy = hand
    c.save(); c.translate(hx, hy); c.scale(s, s)
    rect(k, -9, -30, 18, 44, THERMOS, seed, shadow=False, lw=1.8)
    rect(k, -10, -38, 20, 9, SILVER, seed + 1, shadow=False, lw=1.6)
    c.set_source_rgb(1, 1, 1); c.rectangle(-5, -24, 3, 30); c.fill()
    c.restore()
    ellipse(k, hx, hy, 9.5, 9.5, kit.PEOPLE["PAM"]["skin"], seed + 2, shadow=False, lw=2)


FACE_SEED = [70]


def _face_hook(orig, mask, chin=0.0):
    def face_draw(k, x, y, face, look, glasses=False, seed=0):
        orig(k, x, y, face, look, glasses=glasses, seed=seed)
        if mask and seed == FACE_SEED[0]:
            mask_strip(k, x, y - (7 * chin if mask == "down" else 0), mask, seed)
    return face_draw


def pam(k, x, feet, s=1.0, pose="stand", face="neutral", look=(0, 0), mask="neck", thermos_in_hand=False,
        orn=False, seed=40, badge=True, cape=True, stance=1.0, cape_flare=1.0, chin=0.0):
    c = k.c
    old_p = dict(kit.PEOPLE["PAM"])
    old_hook, old_face = kit.BADGE_HOOK, kit.face_draw
    FACE_SEED[0] = seed + 30
    base_face = dv._face_wrap(old_face, chin) if chin else old_face
    kit.face_draw = _face_hook(base_face, mask, chin)
    p = dict(old_p); p["body"] = CARDIGAN
    kit.PEOPLE["PAM"] = p
    kit.BADGE_HOOK = _costume(badge)
    bt = -300 * p["h"] + 78
    try:
        c.save(); c.translate(x, feet); c.scale(s, s)
        if cape:
            _cape(k, bt, seed, cape_flare)
        _legs(k, seed, stance)
        c.restore()
        c.save()
        c.rectangle(x - 4000, feet - 8000, 8000, 8000 + HEM * s); c.clip()
        if not isinstance(pose, str):
            kit.ARM_POSES["_xmas"] = pose
            pose = "_xmas"
        out = kit.person(k, "PAM", x, feet, s, pose=pose, face=face, seed=seed, look=look, badge=True)
        c.restore()
        c.save(); c.translate(x, feet); c.scale(s, s)               # v2: her left side hangs a button lower
        cut(k, [(-41, HEM - 2), (2, HEM - 2), (2, HEM + 16), (-41, HEM + 11)], CARDIGAN, shadow=False, lw=1.8)
        c.set_source_rgb(*CARDIGAN_DARK); c.set_line_width(2); c.move_to(-39, HEM + 7); c.line_to(0, HEM + 11); c.stroke()
        c.restore()
    finally:
        kit.ARM_POSES.pop("_xmas", None)
        kit.PEOPLE["PAM"] = old_p
        kit.BADGE_HOOK, kit.face_draw = old_hook, old_face
    if thermos_in_hand:
        thermos(k, out["hands"][1], s, seed + 60)
    if orn:
        hx, hy = out["hands"][1]
        sx.ornament(k, hx + 2 * s, hy + 22 * s, 17 * s, seed + 80)
        ellipse(k, hx, hy, 9.5 * s, 9.5 * s, kit.PEOPLE["PAM"]["skin"], seed + 81, shadow=False, lw=2)
    return out
