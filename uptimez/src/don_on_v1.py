"""DON, "Office Noir", v1. Two looks on his usual figure (don_ss, untouched; drawn underneath, then dressed over):
DREAM, the detective in his head (don_noir):
- a light trench coat, buttoned double-breasted, belted, the collar turned up, wide lapels; the white shirt and a
  deep navy tie in the V (TIE is an accent key colour: it stays navy at 40 % in the noir pass);
- a charcoal fedora with a black band, worn low; brim=0..1 darkens a band over his eyes inside the head
  (1 = eyes hidden while he controls the case, 0 = both eyes revealed when Pam touches his coat, shot 7);
- the plant: outline=True draws the faint sticker outline on his screen-right lapel; heart=True puts the red
  heart there instead (HEART is the episode's key red);
- the ketchup stain is under the buttoned trench (a callback nobody needs to see).
REALITY (don_pj): pale blue pyjamas with navy piping, a breast pocket, the fedora still on his head;
heart=True puts the paper heart on the pocket; lift= raises the fedora a few pixels (10B).
Faces: everything Don already has, plus "almost" (7: the almost-smile, soft lids, one corner barely up) and
"frozen" (10B: eyes wide open, mouth a short flat line). Useful existing faces: "neutral" (grave), "smug" (2),
"drop" (6: confidence dies), "indignant" (8: the objection), "deflated" (bed).
Poses: POSE_HEART_EYE (2: the heart held up to his eye), POSE_POINT (2: the smug point, screen left),
POSE_OBJECT (8: one finger up like a lawyer), POSE_LEAN (5: leaning over a desk; use lean=), "stand".
Usage: o = don_noir(k, x, feet, s, pose, face, look, brim=1, outline=True, heart=False, mouth=None, lean=0)
       o = don_pj(k, x, feet, s, pose, face, look, heart=True, lift=0, mouth=None)"""
import math
import cairo
import kit
import don_ss as ds
import don_mf as dm
import pam_mf as pm
import iwry_mouths as im
from kit import INK, cut, rect, ellipse

TRENCH = (0.78, 0.70, 0.55)
TRENCH_SHADE = (0.62, 0.54, 0.40)
TIE = (0.12, 0.17, 0.36)                  # accent key (navy, 40 % in the noir pass)
HEART = (0xD2 / 255, 0x1F / 255, 0x2B / 255)   # accent key (full red)
FEDORA = (0.24, 0.23, 0.26)
BAND = (0.08, 0.08, 0.09)
PJ = (0.66, 0.81, 0.94)
PJ_PIPE = (0.20, 0.30, 0.52)
SHIRT = (0.97, 0.97, 0.95)
SKIN = ds.SKIN
BT, HY = dm.BT, dm.HY
HEM = -72
LAPEL_HEART = (24, BT + 40)               # screen-right lapel, where the sticker sits

POSE_HEART_EYE = (-10, 4) + dm.ik(1, 18, HY + 6)
POSE_POINT = (-96, 6, 10, -4)
POSE_OBJECT = (-10, 4) + dm.ik(1, 44, BT - 12)
POSE_LEAN = (-10, 4) + dm.ik(1, 46, BT + 96)


def heart_path(c, x, y, s):
    c.move_to(x, y + 0.9 * s)
    c.curve_to(x - 1.6 * s, y - 0.1 * s, x - 0.9 * s, y - 1.1 * s, x, y - 0.45 * s)
    c.curve_to(x + 0.9 * s, y - 1.1 * s, x + 1.6 * s, y - 0.1 * s, x, y + 0.9 * s)
    c.close_path()


def heart(c, x, y, s, curl=True):
    """The paper sticker: key red, a white backing edge peeking at the curled corner."""
    heart_path(c, x, y, s)
    c.set_source_rgb(*HEART); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(max(1.2, s * 0.12)); c.stroke()
    if curl:
        cx, cy = x + 0.95 * s, y - 0.55 * s
        c.new_path(); c.move_to(cx - 0.35 * s, cy - 0.15 * s); c.line_to(cx + 0.2 * s, cy - 0.35 * s)
        c.line_to(cx + 0.05 * s, cy + 0.25 * s); c.close_path()
        c.set_source_rgb(1, 1, 1); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(max(1.0, s * 0.08))
        c.stroke()


def outline_mark(c, x, y, s):
    """The faint sticker outline: a slightly darker heart shape on the lapel, where the sticker used to sit."""
    heart_path(c, x, y, s)
    c.set_source_rgba(0, 0, 0, 0.12); c.fill_preserve()
    c.set_source_rgba(0, 0, 0, 0.35); c.set_line_width(1.0); c.set_dash([2.5, 2.0]); c.stroke(); c.set_dash([])


def fedora(k, x, y, s=1.0, tilt=-0.06, seed=0):
    """(x, y) = the middle of the brim line."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(tilt); c.scale(s, s)
    cut(k, [(-40, 2), (-35, -34), (-12, -40), (0, -33), (12, -40), (35, -34), (40, 2)], FEDORA, shadow=False, lw=2.4)
    c.set_source_rgba(1, 1, 1, 0.10); c.move_to(-7, -35); c.line_to(-4, 0); c.line_to(6, 0); c.line_to(2, -35)
    c.close_path(); c.fill()                                                       # the pinch
    rect(k, -40, -12, 80, 12, BAND, seed + 1, shadow=False, lw=2)
    c.new_path(); c.save(); c.scale(64, 9); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
    c.set_source_rgb(*FEDORA); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.4); c.stroke()
    c.restore()


def _faces(orig):
    def face_draw(k, x, y, face, look, glasses=False, seed=0):
        c = k.c
        my = y + 28
        if face == "almost":                       # 7: soft lids, the corner of the mouth barely up
            orig(k, x, y, "neutral", look, glasses=glasses, seed=seed)
            for sx in (-17, 17):
                c.save(); c.new_path(); c.arc(x + sx, y, 11, 0, 2 * math.pi); c.clip()
                c.set_source_rgb(*SKIN); c.rectangle(x + sx - 12, y - 12, 24, 9); c.fill(); c.restore()
                c.set_source_rgb(*INK); c.set_line_width(2.4)
                c.new_path(); c.move_to(x + sx - 10, y - 3); c.line_to(x + sx + 10, y - 3); c.stroke()
            ellipse(k, x, my, 16, 7, SKIN, seed + 91, shadow=False, outline=False)
            c.set_source_rgb(*INK); c.set_line_width(4); c.set_line_cap(1)
            c.new_path(); c.move_to(x - 11, my + 1); c.line_to(x + 5, my + 1); c.curve_to(x + 9, my + 1, x + 12, my - 1, x + 13, my - 4)
            c.stroke(); c.set_line_cap(0)
        elif face == "frozen":                     # 10B: wide open, small pupils, a short flat mouth
            orig(k, x, y, "shock", (0, 0.3), glasses=glasses, seed=seed)
            ellipse(k, x, my, 16, 14, SKIN, seed + 92, shadow=False, outline=False)
            c.set_source_rgb(*INK); c.set_line_width(4); c.set_line_cap(1)
            c.new_path(); c.move_to(x - 7, my); c.line_to(x + 7, my); c.stroke(); c.set_line_cap(0)
        else:
            orig(k, x, y, face, look, glasses=glasses, seed=seed)
    return face_draw


def _base(k, x, feet, s, pose, face, look, seed, mouth):
    old, old_ear = kit.face_draw, ds.earpiece
    kit.face_draw = _faces(old)
    ds.earpiece = lambda *a, **kw: None                     # no agent earpiece in this episode
    try:
        out = ds.don(k, x, feet, s, pose=pose, face=face, look=look, seed=seed, shades=None, card=None, badge=False)
    finally:
        kit.face_draw, ds.earpiece = old, old_ear
    if mouth:
        im.don_mouth(k, out["head"], mouth, seed=seed + 30)
    return out


def _pose_tuple(pose):
    return pose if not isinstance(pose, str) else kit.ARM_POSES[pose]


def _arms(k, pose, col, seed, cuff=None):
    a = _pose_tuple(pose)
    hands = []
    for side, (u, f) in ((-1, (a[0], a[1])), (1, (a[2], a[3]))):
        hands.append(kit.arm(k, side * 40, BT + 14, u, f, col, SKIN, seed + 10 + side))
    return hands


def _hand_extras(k, pose, hands, s, seed):
    c = k.c
    if pose == POSE_OBJECT:
        pm.finger_up(k, hands[1][0], hands[1][1], 1.0, seed)
    if pose == POSE_POINT:                                  # index finger out to screen left
        hx, hy = hands[0]
        c.set_source_rgb(*INK); c.set_line_width(8); c.set_line_cap(1)
        c.new_path(); c.move_to(hx, hy); c.line_to(hx - 20, hy - 1); c.stroke()
        c.set_source_rgb(*SKIN); c.set_line_width(5)
        c.new_path(); c.move_to(hx, hy); c.line_to(hx - 20, hy - 1); c.stroke(); c.set_line_cap(0)
        ellipse(k, hx, hy, 10, 10, SKIN, seed + 3, shadow=False, lw=2)


def _brim_shadow(c, amount):
    if amount <= 0:
        return
    c.save()
    c.new_path(); c.arc(0, HY, 50, 0, 2 * math.pi); c.clip()
    y1 = HY + 14 * amount
    g = cairo.LinearGradient(0, y1 - 14, 0, y1)                 # soft lower edge, not a visor
    g.add_color_stop_rgba(0, 0.05, 0.05, 0.08, 0.62 * amount)
    g.add_color_stop_rgba(1, 0.05, 0.05, 0.08, 0.0)
    c.set_source_rgba(0.05, 0.05, 0.08, 0.62 * amount)
    c.rectangle(-60, HY - 60, 120, 60 + 14 * amount - 14); c.fill()
    c.set_source(g); c.rectangle(-60, y1 - 14, 120, 14); c.fill()
    c.restore()


def _wrap_lean(fn, k, x, feet, lean, *args):
    c = k.c
    c.save(); c.translate(x, feet); c.rotate(math.radians(lean)); c.translate(-x, -feet)
    try:
        out = fn(k, x, feet, *args)
        dev = {"head": c.user_to_device(*out["head"]), "hands": [c.user_to_device(*q) for q in out["hands"]]}
    finally:
        c.restore()
    return {"head": c.device_to_user(*dev["head"]), "hands": [c.device_to_user(*q) for q in dev["hands"]]}


def don_noir(k, x, feet, s=1.0, pose="stand", face="neutral", look=(0, 0), brim=1.0, outline=True, heart_on=False,
             mouth=None, lean=0.0, seed=500, hat=True, held_heart=None):
    if lean:
        return _wrap_lean(lambda k_, x_, f_: don_noir(k_, x_, f_, s, pose, face, look, brim, outline, heart_on, mouth, 0.0,
                                                      seed, hat, held_heart), k, x, feet, lean)
    c = k.c
    out = _base(k, x, feet, s, pose, face, look, seed, mouth)
    c.save(); c.translate(x, feet); c.scale(s, s)
    # the trench: torso to the knee, collar up, wide lapels, double-breasted, belted
    cut(k, [(-46, BT - 2), (46, BT - 2), (56, HEM), (-56, HEM)], TRENCH)
    c.new_path(); c.move_to(-12, BT - 2); c.line_to(0, BT + 66); c.line_to(12, BT - 2); c.close_path()
    c.set_source_rgb(*SHIRT); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1.6); c.stroke()
    cut(k, [(0, BT + 2), (-7, BT + 10), (-4, BT + 58), (0, BT + 66), (4, BT + 58), (7, BT + 10)], TIE, shadow=False, lw=1.6)
    for sx in (-1, 1):
        cut(k, [(sx * 10, BT - 4), (sx * 36, BT - 6), (sx * 40, BT + 22), (sx * 26, BT + 30), (sx * 4, BT + 70)],
            TRENCH_SHADE, shadow=False, lw=2)                                          # lapel
        cut(k, [(sx * 14, BT - 6), (sx * 34, BT - 28), (sx * 44, BT - 6)], TRENCH, shadow=False, lw=2)   # collar up
        for i in range(3):
            ellipse(k, sx * 18, BT + 86 + i * 30, 3.6, 3.6, (0.30, 0.25, 0.18), seed + 40 + i + sx, shadow=False, lw=1.2)
    rect(k, -56, BT + 120, 112, 14, TRENCH_SHADE, seed + 50, shadow=False, lw=2)          # the belt
    rect(k, -9, BT + 118, 18, 18, TRENCH, seed + 51, shadow=False, lw=1.8)
    c.set_source_rgb(*TRENCH_SHADE); c.set_line_width(1.6)
    c.new_path(); c.move_to(2, BT + 70); c.line_to(6, HEM); c.stroke()
    if heart_on:
        heart(c, LAPEL_HEART[0], LAPEL_HEART[1], 13)
    elif outline:
        outline_mark(c, LAPEL_HEART[0], LAPEL_HEART[1], 13)
    _brim_shadow(c, brim)
    c.restore()
    c.save(); c.translate(x, feet); c.scale(s, s)
    hands = _arms(k, pose, TRENCH, seed)
    _hand_extras(k, pose, hands, s, seed)
    c.restore()
    if hat:
        fedora(k, x + 2 * s, feet + (HY - 26) * s, 1.0 * s, seed=seed + 5)
    hands = [(x + hx * s, feet + hy * s) for hx, hy in hands]
    if held_heart is not None or pose == POSE_HEART_EYE:              # the heart held up between his fingers
        hx, hy = hands[1]
        heart(c, hx - 4 * s, hy - 14 * s, (held_heart or 15) * s)
        ellipse(k, hx + 2 * s, hy, 10 * s, 10 * s, SKIN, seed + 6, shadow=False, lw=2 * s)
    out["hands"] = hands
    return out


def don_pj(k, x, feet, s=1.0, pose="stand", face="deflated", look=(0, 0), heart_on=True, lift=0.0, mouth=None,
           seed=500, hat=True):
    c = k.c
    out = _base(k, x, feet, s, pose, face, look, seed, mouth)
    c.save(); c.translate(x, feet); c.scale(s, s)
    cut(k, [(-46, BT - 2), (46, BT - 2), (48, 0), (-48, 0)], PJ)                      # pyjama top + trousers
    c.set_source_rgb(*PJ_PIPE); c.set_line_width(2.4)
    c.new_path(); c.move_to(0, BT + 4); c.line_to(0, BT + 140); c.stroke()
    c.new_path(); c.move_to(-46, BT + 146); c.line_to(46, BT + 146); c.stroke()
    c.new_path(); c.move_to(0, BT + 160); c.line_to(0, -2); c.stroke()
    for i in range(4):
        ellipse(k, -6, BT + 22 + i * 32, 3.2, 3.2, (0.98, 0.97, 0.94), seed + 60 + i, shadow=False, lw=1.2)
    for sx in (-1, 1):                                                              # collar with piping
        cut(k, [(0, BT + 2), (sx * 22, BT - 6), (sx * 26, BT + 14), (sx * 4, BT + 22)], PJ, shadow=False, lw=1.8)
    rect(k, 8, BT + 30, 34, 34, PJ, seed + 70, shadow=False, lw=1.8)                  # breast pocket
    c.set_source_rgb(*PJ_PIPE); c.set_line_width(2.4)
    c.new_path(); c.move_to(9, BT + 33); c.line_to(41, BT + 33); c.stroke()
    if heart_on:
        heart(c, 25, BT + 48, 13)
    c.restore()
    c.save(); c.translate(x, feet); c.scale(s, s)
    hands = _arms(k, pose, PJ, seed)
    c.restore()
    if hat:
        fedora(k, x + 2 * s, feet + (HY - 26 - lift) * s, 1.0 * s, seed=seed + 5)
    out["hands"] = [(x + hx * s, feet + hy * s) for hx, hy in hands]
    return out
