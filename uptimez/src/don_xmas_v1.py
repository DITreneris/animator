"""DON, Christmas special ("Happy Compliance"): walks into the office party mid-shave.
Same head, height and face as before (kit.PEOPLE["DON"]); costume only, drawn through kit.person with
kit.BADGE_HOOK and a clip, so every earlier Don (kit, don_v4.py) is untouched:
- an open navy bathrobe with the UptimeZ mark on the chest pocket and the untied belt hanging loose;
- a white ribbed undershirt with the ketchup squiggle (always there, never mentioned) and a small
  tuft of chest hair at the neckline;
- red boxers with white hearts, hairy shins, white socks, fuzzy navy slippers;
- shaving foam on one half of his face (one stroke already shaved through it), a disposable razor;
- the staff badge, clipped to the robe lapel: he never takes it off.
Usage: p = don(k, x, feet, s, pose, face, look, seed=500, razor=True, foam=True, chin=0)"""
import math
import kit
import brand
import don_v4 as dv
from kit import INK, cut, rect, ellipse

ROBE = (0.16, 0.23, 0.38)
ROBE_LIGHT = (0.24, 0.33, 0.52)
ROBE_DARK = (0.10, 0.15, 0.27)
VEST = (0.98, 0.98, 0.96)
VEST_RIB = (0.86, 0.87, 0.89)
BOXERS = (0.85, 0.18, 0.24)
CHEST_HAIR = (0.42, 0.37, 0.33)
LEG_HAIR = (0.45, 0.40, 0.36)
SOCK = (0.97, 0.97, 0.95)
FOAM = (1.0, 1.0, 1.0)
FOAM_SHADE = (0.82, 0.88, 0.95)
RAZOR = (0.20, 0.55, 0.85)
HEM = -72                         # robe hem height (local units above the feet)

POSE_RAZOR = (-110, 234, 8, 0)    # left hand up at his foamed cheek, razor pointing in
POSE_CLUTCH = (30, 125, -30, -125)  # both hands clutching the robe shut at the chest
POSE_THUMB = dv.POSE_THUMB
POSE_HIPS = "pleased"             # hands on hips: the "Nice balls" smirk


def heart(c, x, y, s):
    c.move_to(x, y + s * 0.9)
    c.curve_to(x - s * 1.5, y - s * 0.2, x - s * 0.7, y - s * 1.2, x, y - s * 0.4)
    c.curve_to(x + s * 0.7, y - s * 1.2, x + s * 1.5, y - s * 0.2, x, y + s * 0.9)
    c.close_path()


def _costume(badge=True, stain=True):
    def hook(k, name_, p, bt, seed):
        c = k.c
        waist = bt + 150
        # open front: undershirt
        cut(k, [(-23, bt + 2), (23, bt + 2), (27, waist + 2), (-27, waist + 2)], VEST, shadow=False, lw=2)
        c.set_source_rgb(*VEST_RIB); c.set_line_width(1.4)
        for rx in (-16, -8, 0, 8, 16):
            c.move_to(rx, bt + 24); c.line_to(rx * 1.12, waist - 2); c.stroke()
        c.save(); c.translate(0, bt + 2); c.scale(15, 14)                     # scoop neckline
        c.arc(0, 0, 1, 0, math.pi); c.restore()
        c.set_source_rgb(*p["skin"]); c.fill_preserve()
        c.set_source_rgb(*INK); c.set_line_width(1.8); c.stroke()
        c.set_source_rgb(*CHEST_HAIR); c.set_line_width(2.4); c.set_line_cap(1)   # a small curly tuft
        for i, (hx, hy) in enumerate(((-7, 6), (-2, 9), (3, 7), (8, 5), (-4, 3), (5, 2), (0, 12))):
            c.arc(hx, bt + hy, 3.0, (0.2 + i) % 6, (0.2 + i) % 6 + 4.2); c.stroke()
        if stain:
            dv.ketchup(k, 0, bt + 92, seed + 70)
        # boxers
        cut(k, [(-31, waist), (31, waist), (35, HEM + 2), (-35, HEM + 2)], BOXERS, shadow=False, lw=2)
        rect(k, -31, waist - 2, 62, 9, (0.97, 0.94, 0.94), seed + 63, shadow=False, lw=1.4)   # waistband
        c.set_source_rgb(*INK); c.set_line_width(1.6); c.move_to(0, waist + 8); c.line_to(0, waist + 42); c.stroke()
        for hx, hy in ((-20, 20), (12, 26), (-6, 48), (20, 58), (-22, 72), (4, 84), (-12, 100), (18, 96)):
            if waist + hy < HEM - 4:
                heart(c, hx, waist + hy, 4.2); c.set_source_rgb(1, 1, 1); c.fill()
        # robe edges (lapels), drawn over the open front
        for sx in (-1, 1):
            edge = [(sx * 12, bt - 2), (sx * 24, bt - 2), (sx * 34, waist + 4), (sx * 40, HEM + 2), (sx * 30, HEM + 2),
                    (sx * 24, waist + 4)]
            cut(k, edge, ROBE_LIGHT, shadow=False, lw=2)
            c.set_source_rgb(*ROBE_DARK); c.set_line_width(2.2)                 # terry-cloth fold
            c.move_to(sx * 38, bt + 40); c.curve_to(sx * 41, bt + 90, sx * 39, bt + 140, sx * 42, HEM + 20); c.stroke()
        # untied belt: loops at the sides, two tails hanging
        for sx in (-1, 1):
            cut(k, [(sx * 34, waist - 6), (sx * 46, waist - 6), (sx * 46, waist + 6), (sx * 34, waist + 6)], ROBE_LIGHT,
                shadow=False, lw=1.6)
        cut(k, [(-36, waist + 2), (-28, waist + 2), (-24, waist + 64), (-33, waist + 66)], ROBE_LIGHT, shadow=False, lw=1.8)
        cut(k, [(28, waist + 2), (36, waist + 2), (40, waist + 52), (31, waist + 54)], ROBE_LIGHT, shadow=False, lw=1.8)
        # chest pocket with the company mark (his left = screen right), staff badge on the other lapel
        rect(k, 26, bt + 44, 18, 18, ROBE_LIGHT, seed + 64, shadow=False, lw=1.6)
        brand.mark(c, 29, bt + 47, 12, zzz=False)
        if badge:
            dv.staff_badge(k, "DON", -31, bt + 30, 26, 7.5)
    return hook


def _legs(k, seed):
    """Hairy shins, white socks and fuzzy slippers below the robe hem (local units, feet at 0)."""
    c = k.c
    skin = kit.PEOPLE["DON"]["skin"]
    for sx in (-15, 15):
        cut(k, [(sx - 9, HEM - 6), (sx + 9, HEM - 6), (sx + 7, -26), (sx - 7, -26)], skin, shadow=False, lw=1.8)
        c.set_source_rgb(*LEG_HAIR); c.set_line_width(1.2); c.set_line_cap(1)
        for i in range(7):
            hx = sx - 6 + (i * 5) % 13
            hy = HEM - 2 + i * 6.5
            c.move_to(hx, hy); c.line_to(hx + (1.5 if i % 2 else -1.5), hy + 4); c.stroke()
        rect(k, sx - 7.5, -28, 15, 16, SOCK, seed + 80 + sx, shadow=False, lw=1.6)
        o = 1 if sx > 0 else -1
        ellipse(k, sx + o * 4, -6, 15, 8, ROBE, seed + 82 + sx, lw=2)
        ellipse(k, sx + o * 6, -9, 8, 4.5, ROBE_LIGHT, seed + 84 + sx, shadow=False, outline=False)


def foam_patch(k, x, y, seed=0):
    """Shaving foam over his right cheek and half his chin (screen left), with one clean stroke shaved
    through it; stays clear of the mouth (x - 12 .. x + 12 at y + 28) so the lip-sync is never covered."""
    c = k.c
    blobs = [(-41, 18, 9), (-44, 30, 10), (-35, 40, 11), (-24, 47, 10), (-13, 50, 8), (-33, 24, 8), (-23, 37, 8),
             (-45, 41, 7), (-30, 32, 8)]
    c.set_source_rgb(*INK)
    for bx, by, r in blobs:
        c.arc(x + bx, y + by, r + 1.8, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(*FOAM)
    for bx, by, r in blobs:
        c.arc(x + bx, y + by, r, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(*FOAM_SHADE)
    for bx, by, r in blobs[::2]:
        c.arc(x + bx + r * 0.3, y + by + r * 0.35, r * 0.45, 0, 2 * math.pi); c.fill()
    c.save()                                               # one stroke already shaved: a clean skin track
    for bx, by, r in blobs:
        c.arc(x + bx, y + by, r, 0, 2 * math.pi); c.new_sub_path()
    c.clip()
    c.set_source_rgb(*kit.PEOPLE["DON"]["skin"]); c.set_line_width(7); c.set_line_cap(1)
    c.move_to(x - 50, y + 20); c.line_to(x - 33, y + 46); c.stroke()
    c.restore()
    c.set_source_rgb(1, 1, 1)                              # a couple of loose flecks
    for fx, fy, r in ((-56, 46, 2.6), (-8, 58, 2.2)):
        c.arc(x + fx, y + fy, r, 0, 2 * math.pi); c.fill()
        c.set_source_rgb(*INK); c.set_line_width(1); c.arc(x + fx, y + fy, r, 0, 2 * math.pi); c.stroke()
        c.set_source_rgb(1, 1, 1)


def razor(k, hand, s=1.0, ang=-0.9, seed=540):
    """A disposable razor in the hand point; ang tilts it (0 = head up)."""
    c = k.c
    hx, hy = hand
    c.save(); c.translate(hx, hy); c.scale(s, s); c.rotate(ang)
    rect(k, -3.5, -30, 7, 34, RAZOR, seed, shadow=False, lw=1.6)
    rect(k, -9, -38, 18, 8, (0.88, 0.90, 0.93), seed + 1, shadow=False, lw=1.6)
    c.set_source_rgb(*INK); c.set_line_width(1); c.move_to(-7, -34); c.line_to(7, -34); c.stroke()
    c.set_source_rgb(1, 1, 1); c.arc(4, -40, 3, 0, 2 * math.pi); c.fill()      # a bit of foam on the blade
    c.restore()
    ellipse(k, hx, hy, 10, 10, kit.PEOPLE["DON"]["skin"], seed + 2, shadow=False, lw=2)   # fingers over the handle


def _face_hook(orig, foam):
    def face_draw(k, x, y, face, look, glasses=False, seed=0):
        orig(k, x, y, face, look, glasses=glasses, seed=seed)
        if foam and seed == FACE_SEED[0]:
            foam_patch(k, x, y, seed)
    return face_draw


FACE_SEED = [530]


def don(k, x, feet, s=1.0, pose="stand", face="neutral", look=(0, 0), seed=500, badge=True, stain=True, chin=0,
        razor_in_hand=True, foam=True):
    c = k.c
    old_p = dict(kit.PEOPLE["DON"])
    old_hook, old_face = kit.BADGE_HOOK, kit.face_draw
    FACE_SEED[0] = seed + 30
    face_fn = dv._face_wrap(old_face, chin) if (face == "grin" or chin) else old_face
    kit.face_draw = _face_hook(face_fn, foam)
    p = dict(old_p); p["body"] = ROBE; p.pop("tie", None)
    kit.PEOPLE["DON"] = p
    kit.BADGE_HOOK = _costume(badge, stain)
    try:
        c.save(); c.translate(x, feet); c.scale(s, s); _legs(k, seed); c.restore()
        c.save()                                            # the robe stops at the hem; legs show below it
        c.rectangle(x - 4000, feet - 8000, 8000, 8000 + HEM * s); c.clip()
        razor_up = pose == POSE_RAZOR
        if not isinstance(pose, str):
            kit.ARM_POSES["_xmas"] = pose
            pose = "_xmas"
        out = kit.person(k, "DON", x, feet, s, pose=pose, face=face, seed=seed, look=look, badge=True)
        c.restore()
    finally:
        kit.ARM_POSES.pop("_xmas", None)
        kit.PEOPLE["DON"] = old_p
        kit.BADGE_HOOK, kit.face_draw = old_hook, old_face
    if razor_in_hand:
        hand = out["hands"][0]
        razor(k, hand, s, ang=0.5 if razor_up else -0.3, seed=seed + 40)
    return out
