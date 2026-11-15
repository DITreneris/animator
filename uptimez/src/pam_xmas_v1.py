"""PAM, Christmas special ("Happy Compliance"): her first full-size standing figure. Same head, bob, face and
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

POSE_THERMOS = (-8, 0, 40, 120)     # right forearm up, thermos at chest height
POSE_FISTS = (-14, 8, 14, -8)       # arms stiff at her sides, fists clenched
POSE_HERO = (-50, 85, 50, -85)      # fists on hips, elbows out: the payoff stance
POSE_TAKE = (-8, 0, 70, 15)         # right arm out, hand open for the ornament


def _cape(k, bt, seed):
    """The towel, behind her: hangs from the shoulders to the knee, stripes near the hem, a fringe."""
    c = k.c
    hem = -96
    towel = [(-44, bt - 4), (44, bt - 4), (64, bt + 40), (72, hem + 30), (74, hem), (-74, hem), (-72, hem + 30),
             (-64, bt + 40)]
    cut(k, towel, TOWEL, lw=2.2)
    c.save()
    c.move_to(*towel[0])
    for q in towel[1:]:
        c.line_to(*q)
    c.close_path(); c.clip()
    for sy in (hem + 16, hem + 26):
        c.set_source_rgb(*TOWEL_STRIPE); c.rectangle(-70, sy, 140, 5); c.fill()
    c.set_source_rgb(*TOWEL_DARK); c.set_line_width(2.2)
    for fx in (-48, 48):
        c.move_to(fx, bt + 30); c.curve_to(fx * 1.05, bt + 90, fx * 1.12, bt + 150, fx * 1.2, hem + 10); c.stroke()
    c.restore()
    c.set_source_rgb(*INK); c.set_line_width(1.6)                 # fringe
    for fx in range(-60, 64, 6):
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
        c.set_source_rgb(*CARDIGAN_DARK); c.set_line_width(2.4)
        c.move_to(0, bt + 8); c.line_to(2, HEM - 6); c.stroke()
        for i, by in enumerate((30, 62, 94, 126, 158)):
            ellipse(k, 6, bt + by, 3.4, 3.4, (0.95, 0.90, 0.70), seed + 90 + i, shadow=False, lw=1.4)
            c.set_source_rgb(*INK); c.set_line_width(1.6)
            c.move_to(-7, bt + by + 16); c.line_to(-1, bt + by + 16); c.stroke()      # empty holes, one lower
        cut(k, [(-41, HEM + 10), (2, HEM + 14), (2, HEM - 10), (-41, HEM - 4)], CARDIGAN, shadow=False, lw=1.8)  # the low side
        c.set_source_rgb(*CARDIGAN_DARK); c.set_line_width(2)          # rib cuff at the hem
        c.move_to(-40, HEM - 2); c.line_to(41, HEM - 2); c.stroke()
        # reading glasses on a beaded chain
        c.set_source_rgb(*INK); c.set_line_width(1.2)
        c.move_to(-18, bt + 4); c.curve_to(-20, bt + 24, -14, bt + 38, -8, bt + 42); c.stroke()
        c.move_to(18, bt + 4); c.curve_to(20, bt + 22, 16, bt + 34, 10, bt + 40); c.stroke()
        for gx in (-11, 9):
            c.set_source_rgb(0.85, 0.93, 0.98); c.arc(gx, bt + 44, 8.5, 0, 2 * math.pi); c.fill_preserve()
            c.set_source_rgb(*INK); c.set_line_width(2.4); c.stroke()
            c.set_source_rgb(1, 1, 1); c.arc(gx - 3, bt + 41, 1.8, 0, 2 * math.pi); c.fill()
        c.set_source_rgb(*INK); c.set_line_width(2.4)
        c.move_to(-3, bt + 43); c.curve_to(-1, bt + 40, 0, bt + 40, 1, bt + 43); c.stroke()
        c.move_to(-19, bt + 42); c.line_to(-25, bt + 34); c.stroke(); c.move_to(17, bt + 42); c.line_to(23, bt + 34); c.stroke()
        # paper "P", taped on crooked
        c.save(); c.translate(-17, bt + 86); c.rotate(-0.22)
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


def _legs(k, seed):
    c = k.c
    for sx_ in (-15, 15):
        cut(k, [(sx_ - 11, HEM - 6), (sx_ + 11, HEM - 6), (sx_ + 10, -12), (sx_ - 10, -12)], TROUSERS, shadow=False, lw=1.8)
        c.set_source_rgb(*TROUSERS_DARK); c.set_line_width(1.6)
        c.move_to(sx_, HEM + 6); c.line_to(sx_, -16); c.stroke()             # pressed crease
        o = 1 if sx_ > 0 else -1
        ellipse(k, sx_ + o * 3, -6, 15, 8, TRAINER, seed + 70 + sx_, lw=2)
        c.set_source_rgb(0.55, 0.58, 0.64); c.set_line_width(1.6)
        c.move_to(sx_ + o * 3 - 12, -2); c.line_to(sx_ + o * 3 + 12, -2); c.stroke()   # sole line


def mask_strip(k, x, y, mode, seed=0):
    """Cardboard strip with two eye holes; "down" over the eyes, "up" pushed onto the forehead."""
    c = k.c
    yy = y if mode == "down" else y - 40
    rot = 0.0 if mode == "down" else -0.12
    c.save(); c.translate(x, yy); c.rotate(rot)
    c.set_source_rgb(*INK); c.set_line_width(1.6)                      # the string round her head
    c.move_to(-38, 0); c.line_to(-52, -2); c.stroke(); c.move_to(38, 0); c.line_to(52, -2); c.stroke()
    c.move_to(-40, -10); c.line_to(40, -10); c.line_to(42, 10); c.line_to(-42, 10); c.close_path()
    for ex in (-17, 17):
        c.new_sub_path(); c.save(); c.translate(ex, 0); c.scale(11.5, 8.5); c.arc_negative(0, 0, 1, 2 * math.pi, 0); c.restore()
    c.set_fill_rule(0)
    c.set_source_rgb(*CARD); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(2.2); c.stroke()
    c.set_source_rgb(*CARD_DARK); c.set_line_width(1.2)              # corrugation lines
    for cx_ in (-34, -2, 31):
        c.move_to(cx_, -8); c.line_to(cx_ + 1, 8); c.stroke()
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


def _face_hook(orig, mask):
    def face_draw(k, x, y, face, look, glasses=False, seed=0):
        orig(k, x, y, face, look, glasses=glasses, seed=seed)
        if mask and seed == FACE_SEED[0]:
            mask_strip(k, x, y, mask, seed)
    return face_draw


def pam(k, x, feet, s=1.0, pose="stand", face="neutral", look=(0, 0), mask="up", thermos_in_hand=False,
        orn=False, seed=40, badge=True, cape=True):
    c = k.c
    old_p = dict(kit.PEOPLE["PAM"])
    old_hook, old_face = kit.BADGE_HOOK, kit.face_draw
    FACE_SEED[0] = seed + 30
    kit.face_draw = _face_hook(old_face, mask)
    p = dict(old_p); p["body"] = CARDIGAN
    kit.PEOPLE["PAM"] = p
    kit.BADGE_HOOK = _costume(badge)
    bt = -300 * p["h"] + 78
    try:
        c.save(); c.translate(x, feet); c.scale(s, s)
        if cape:
            _cape(k, bt, seed)
        _legs(k, seed)
        c.restore()
        c.save()
        c.rectangle(x - 4000, feet - 8000, 8000, 8000 + HEM * s); c.clip()
        if not isinstance(pose, str):
            kit.ARM_POSES["_xmas"] = pose
            pose = "_xmas"
        out = kit.person(k, "PAM", x, feet, s, pose=pose, face=face, seed=seed, look=look, badge=True)
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
