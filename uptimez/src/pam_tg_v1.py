"""PAM, Thanksgiving film ("Raises for Everyone"), v1. Same head, bob, flat face and height (kit.PEOPLE["PAM"]);
her sensible office clothes from the Christmas figure (pam_xmas.py: blouse collar, lanyard with badge and too many
keys, beige trousers, white trainers) without the costume, plus:
- a burnt-orange cardigan buttoned neatly all the way to the top (prim; a white collar peeks over it);
- a red enamel maple-leaf brooch with a gold rim on her left chest (she dressed up for the boss's party);
- character notes from the brief: an older single lady with a quiet soft spot for Don. So: a silver streak in
  her bob, small smile lines, no ring; a "soft" face (faint blush, eyes down, the smallest smile) and a primping
  pose (hand to her hair). The joke: she primps for him, then tells him the truth anyway.
New faces: "read", "stare", "soft". New poses: POSE_READ, POSE_PUSH, POSE_TUG, POSE_PRIMP.
pam_xmas.py, kit.py and every earlier Pam are untouched.
Usage: p = pam(k, x, feet, s, pose, face, look, seed=40, form=False, mouth=None)"""
import math
import kit
import brand
import don_v4 as dv
import pam_xmas as px
import iwry_mouths as im
from kit import INK, cut, rect, ellipse

CARDIGAN = (0.80, 0.40, 0.14)
CARDIGAN_DARK = (0.60, 0.27, 0.08)
BUTTON = (0.98, 0.90, 0.72)
LEAF = (0.84, 0.12, 0.10)
LEAF_DARK = (0.58, 0.06, 0.05)
GOLD = (0.86, 0.66, 0.20)
SILVER_HAIR = (0.80, 0.80, 0.82)
BLUSH = (0.96, 0.60, 0.58)
SKIN = kit.PEOPLE["PAM"]["skin"]
HEM = px.HEM

POSE_READ = (-27, 113, 27, -113)    # shot 7: both hands up at the chest, holding the form to read it
POSE_PUSH = (-8, 0, 50, 30)         # shot 7: right hand flat on the table, pushing the form back
POSE_TUG = (-22, 30, 22, -30)       # shot 9: standing, tugging the cardigan straight at the hem
POSE_PRIMP = (-8, 0, 109, 119)      # soft spot: right hand up, patting her bob


LEAF_R = [(0, -1.0), (0.14, -0.74), (0.32, -0.82), (0.26, -0.42), (0.5, -0.62), (0.58, -0.46), (0.9, -0.54),
          (0.8, -0.28), (0.96, -0.14), (0.56, 0.12), (0.64, 0.30), (0.22, 0.24), (0.05, 0.46)]


def maple_leaf(c, x, y, r, rot=0.0):
    """A maple leaf (three pointed lobes, two small lower ones, serrated), pointing up; stem drawn separately."""
    pts = LEAF_R + [(-px_, py_) for px_, py_ in reversed(LEAF_R[1:])]
    cs, sn = math.cos(rot), math.sin(rot)
    q = [(x + (px_ * cs - py_ * sn) * r, y + (px_ * sn + py_ * cs) * r) for px_, py_ in pts]
    c.move_to(*q[0])
    for p_ in q[1:]:
        c.line_to(*p_)
    c.close_path()


def brooch(k, x, y, s=1.0):
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    c.set_source_rgb(*INK); c.set_line_width(2.4); c.set_line_cap(1)
    c.move_to(0, 5); c.line_to(1, 13); c.stroke()
    maple_leaf(c, 0, 0, 12.5)
    c.set_source_rgb(*GOLD); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(1.6); c.stroke()
    maple_leaf(c, 0, 0.4, 9.5)
    c.set_source_rgb(*LEAF); c.fill()
    c.set_source_rgb(*LEAF_DARK); c.set_line_width(1)
    for a_ in (-math.pi / 2, -math.pi / 2 - 1.0, -math.pi / 2 + 1.0):
        c.move_to(0, 4); c.line_to(math.cos(a_) * 7.5, 4 + math.sin(a_) * 7.5); c.stroke()
    c.set_source_rgba(1, 1, 1, 0.8); c.arc(-3, -3, 1.4, 0, 2 * math.pi); c.fill()
    c.restore()


def _costume(badge=True):
    def hook(k, name_, p, bt, seed):
        c = k.c
        # white collar peeking over the closed neckline
        for sx_ in (-1, 1):
            cut(k, [(0, bt + 2), (sx_ * 17, bt - 3), (sx_ * 15, bt + 9), (sx_ * 3, bt + 10)], px.BLOUSE,
                shadow=False, lw=1.6)
        # neat placket, buttoned to the top
        c.set_source_rgb(*CARDIGAN_DARK); c.set_line_width(2.4)
        c.move_to(-4, bt + 8); c.line_to(-4, HEM - 4); c.stroke()
        c.move_to(4, bt + 8); c.line_to(4, HEM - 4); c.stroke()
        for i, by in enumerate((14, 36, 58, 80, 102, 124)):
            ellipse(k, 0, bt + by, 3.8, 3.8, BUTTON, seed + 90 + i, shadow=False, lw=1.4)
        c.set_source_rgb(*CARDIGAN_DARK); c.set_line_width(2)          # rib hem and a rib band at the neck
        for yy in (HEM - 4, HEM - 9):
            c.move_to(-40, yy); c.line_to(41, yy); c.stroke()
        c.arc(0, bt - 4, 20, 0.15 * math.pi, 0.85 * math.pi); c.stroke()
        brooch(k, -22, bt + 34, 1.0)
        # lanyard: badge plus too many keys (always)
        c.set_source_rgb(*brand.GREEN); c.set_line_width(3)
        c.move_to(10, bt + 6); c.line_to(18, bt + 84); c.stroke()
        c.move_to(22, bt + 4); c.line_to(24, bt + 84); c.stroke()
        if badge:
            dv.staff_badge(k, "PAM", 7, bt + 84, 30, 8.5)
        for i, (kx, ka) in enumerate(((30, 0.5), (34, 0.9), (26, 0.2))):
            c.save(); c.translate(kx, bt + 112); c.rotate(ka)
            rect(k, -2, 0, 4, 14, px.SILVER, seed + 97 + i, shadow=False, lw=1.2)
            c.set_source_rgb(*px.SILVER); c.arc(0, 0, 4, 0, 2 * math.pi); c.fill_preserve()
            c.set_source_rgb(*INK); c.set_line_width(1.2); c.stroke()
            c.restore()
    return hook


def _faces(orig, mouth=None):
    def face_draw(k, x, y, face, look, glasses=False, seed=0):
        c = k.c
        hy = y - 4
        # silver streak: one lighter lock in her fringe, from the parting sweeping to her left (screen left)
        c.save()
        c.move_to(x - 4, hy - 47); c.curve_to(x - 16, hy - 44, x - 30, hy - 34, x - 38, hy - 20)
        c.line_to(x - 30, hy - 18); c.curve_to(x - 24, hy - 30, x - 14, hy - 38, x + 4, hy - 44); c.close_path()
        c.set_source_rgb(*SILVER_HAIR); c.fill_preserve()
        c.set_source_rgb(*INK); c.set_line_width(1.3); c.stroke()
        c.restore()
        base = {"read": "neutral", "stare": "neutral", "soft": "neutral"}.get(face, face)
        lk = {"read": (0, 1.0), "soft": (0.8, 0.8)}.get(face, look)
        orig(k, x, y, base, lk, glasses=glasses, seed=seed)
        if face in ("read", "stare", "soft"):                 # lids: half (read, soft), a third (stare)
            drop = {"read": 9, "stare": 6, "soft": 8}[face]
            c.set_source_rgb(*SKIN)
            for sx in (-17, 17):
                c.rectangle(x + sx - 12, y - 13, 24, 13 - (10 - drop)); c.fill()
            c.set_source_rgb(*INK); c.set_line_width(3.6); c.set_line_cap(1)
            for sx in (-17, 17):
                c.move_to(x + sx - 11, y - 10 + drop); c.line_to(x + sx + 11, y - 10 + drop); c.stroke()
            if face == "stare":                                 # level brows, pressed low
                c.set_line_width(4)
                c.move_to(x - 26, y - 15); c.line_to(x - 9, y - 15); c.stroke()
                c.move_to(x + 9, y - 15); c.line_to(x + 26, y - 15); c.stroke()
        if face == "soft":                                      # faint blush, the smallest smile
            c.set_source_rgba(*BLUSH, 0.75)
            for sx in (-26, 26):
                c.save(); c.translate(x + sx, y + 14); c.scale(9, 5); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
            ellipse(k, x + 1, y + 28, 15, 6, SKIN, seed + 95, shadow=False, outline=False)
            c.set_source_rgb(*INK); c.set_line_width(3.4); c.set_line_cap(1)
            c.move_to(x - 8, y + 28); c.curve_to(x - 3, y + 31, x + 3, y + 31, x + 8, y + 27); c.stroke()
        c.set_source_rgb(*INK); c.set_line_width(1.4); c.set_line_cap(1)   # smile lines: an older face
        for sx in (-1, 1):
            c.move_to(x + sx * 31, y + 2); c.line_to(x + sx * 35, y - 1); c.stroke()
            c.move_to(x + sx * 31, y + 6); c.line_to(x + sx * 35, y + 6); c.stroke()
        if mouth:
            im.mouth(k, x, y + 28, mouth, SKIN, erase=(16, 8), seed=seed + 96)
    return face_draw


def form_held(k, hands, s, seed=0):
    """The satisfaction form, upright between her hands (we see its front)."""
    c = k.c
    (ax, ay), (bx, by) = hands
    fx, fy = (ax + bx) / 2, (ay + by) / 2 - 8 * s
    w, h = 44 * s, 56 * s
    c.set_source_rgb(1, 1, 1); c.rectangle(fx - w / 2, fy - h / 2, w, h); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(1.6 * s); c.stroke()
    c.set_source_rgb(*brand.GREEN); c.rectangle(fx - w / 2 + 2 * s, fy - h / 2 + 2 * s, w - 4 * s, 6 * s); c.fill()
    c.set_source_rgb(*INK); c.rectangle(fx - w * 0.38, fy - h * 0.15, w * 0.76, 5 * s); c.fill()
    c.set_source_rgb(0.6, 0.6, 0.6)
    for i in range(3):
        c.rectangle(fx - w * 0.38, fy + i * 6 * s, w * 0.6, 2 * s); c.fill()
    for hx, hy in hands:
        ellipse(k, hx, hy, 9.5 * s, 9.5 * s, SKIN, seed, shadow=False, lw=2 * s)


def pam(k, x, feet, s=1.0, pose="stand", face="neutral", look=(0, 0), seed=40, badge=True, form=False, mouth=None):
    c = k.c
    old_p = dict(kit.PEOPLE["PAM"])
    old_hook, old_face = kit.BADGE_HOOK, kit.face_draw
    kit.face_draw = _faces(old_face, mouth)
    p = dict(old_p); p["body"] = CARDIGAN
    kit.PEOPLE["PAM"] = p
    kit.BADGE_HOOK = _costume(badge)
    try:
        c.save(); c.translate(x, feet); c.scale(s, s)
        px._legs(k, seed, 1.0)
        c.restore()
        c.save()
        c.rectangle(x - 4000, feet - 8000, 8000, 8000 + HEM * s); c.clip()
        if not isinstance(pose, str):
            kit.ARM_POSES["_tg"] = pose
            pose = "_tg"
        out = kit.person(k, "PAM", x, feet, s, pose=pose, face=face, seed=seed, look=look, badge=True)
        c.restore()
    finally:
        kit.ARM_POSES.pop("_tg", None)
        kit.PEOPLE["PAM"] = old_p
        kit.BADGE_HOOK, kit.face_draw = old_hook, old_face
    if form:
        form_held(k, out["hands"], s, seed + 60)
    return out
