"""PAM, "Mandatory Fun", v1. Her office look (the Day One purple) on the Thanksgiving v2 figure: the same bob,
grey lock, calm light lid, smile lines, short lanyard, keys, no ring; the cardigan is office purple and there is
no brooch. New: reading glasses worn low on her nose (half-moon lenses, eyes peeking over), on a gold bead chain.
Glasses states: "low" (default), "flash" (shot 9: the glint), "up" (shot 11: straightened), "off".
New faces for the film's beats: "peer" (shot 4, looking at Don over the glasses), "hopeful" (5), "fade" (5),
"approve" (9, the only loud one), "quiet" (10, the second cuff: calm, deliberate, not sly), "doubt" (11),
"dinner" (11, shy hope), "happy" (12, the smile the robot scans). Older faces from pam_tg still work.
New poses: POSE_FINGER, POSE_APPROVE, POSE_GLASSES, POSE_CUFF, POSE_TABLE; cuff="R"/"L" puts Don's yellow toy
cuff on that wrist (screen side) and returns the cuff point for the chain.
pam_tg.py, kit.py and every earlier Pam are untouched.
Usage: o = pam(k, x, feet, s, pose, face, look, glasses="low", cuff=None, finger=False, mouth=None)"""
import math
import cairo
import kit
import brand
import don_v4 as dv
import pam_xmas as px
import pam_tg as pt
import iwry_mouths as im
import props_mf_v1 as pr
from kit import INK, cut, rect, ellipse

PURPLE = kit.PEOPLE["PAM"]["body"]                   # the Day One office purple
PURPLE_DARK = (0.27, 0.17, 0.40)
BUTTON = pt.BUTTON
GOLD = pt.GOLD
SKIN = pt.SKIN
HEM = px.HEM
LENS = (0.86, 0.93, 0.98)
BT = -300 * kit.PEOPLE["PAM"]["h"] + 78
HY = BT - 44                                         # head centre, body units above the feet


def ik(side, tx, ty, ln=48):
    """Arm angles (kit convention: 0 = down, +90 = screen right) putting the hand of arm `side` (-1 screen left,
    +1 screen right) at body point (tx, ty), elbow kept outward."""
    sx, sy = side * 40, BT + 14
    vx, vy = tx - sx, ty - sy
    D = min(math.hypot(vx, vy), 2 * ln - 0.5)
    angD = math.degrees(math.atan2(vx, vy))
    al = math.degrees(math.acos(D / (2 * ln)))
    best = None
    for sg in (1, -1):
        a1 = angD + sg * al
        ex = sx + math.sin(math.radians(a1)) * ln
        if best is None or ex * side > best[0]:
            best = (ex * side, a1, -2 * sg * al)
    return best[1], best[2]


def _pose(left, right):
    return ik(-1, *left) + ik(1, *right)


POSE_FINGER = (-8, 0) + ik(1, 30, BT + 2)            # shot 5: one finger up at her shoulder, small and hopeful
POSE_APPROVE = (-14, 6, 168, 6)                      # shot 9: her arm shoots straight up
POSE_GLASSES = (-8, 0) + ik(1, 9, HY + 14)           # shot 11: fingertip to the bridge, straightening them
POSE_CUFF = _pose((-10, BT + 92), (8, BT + 84))      # shot 10: her own left wrist forward, right hand on the cuff
POSE_TABLE = _pose((-26, BT + 104), (24, BT + 104))  # seated: both hands flat on the table


def _costume(badge=True):
    def hook(k, name_, p, bt, seed):
        c = k.c
        for sx_ in (-1, 1):                                              # white collar over the neckline
            cut(k, [(0, bt + 2), (sx_ * 17, bt - 3), (sx_ * 15, bt + 9), (sx_ * 3, bt + 10)], px.BLOUSE,
                shadow=False, lw=1.6)
        c.set_source_rgb(*PURPLE_DARK); c.set_line_width(2.4)
        c.move_to(-4, bt + 8); c.line_to(-4, HEM - 4); c.stroke()
        c.move_to(4, bt + 8); c.line_to(4, HEM - 4); c.stroke()
        for i, by in enumerate((14, 36, 58, 80, 102, 124)):
            ellipse(k, 0, bt + by, 3.8, 3.8, BUTTON, seed + 90 + i, shadow=False, lw=1.4)
        c.set_source_rgb(*PURPLE_DARK); c.set_line_width(2)
        for yy in (HEM - 4, HEM - 9):
            c.move_to(-40, yy); c.line_to(41, yy); c.stroke()
        c.arc(0, bt - 4, 20, 0.15 * math.pi, 0.85 * math.pi); c.stroke()
        c.set_source_rgb(*brand.GREEN); c.set_line_width(3)
        c.move_to(12, bt + 6); c.line_to(22, bt + 46); c.stroke()
        c.move_to(22, bt + 4); c.line_to(30, bt + 46); c.stroke()
        if badge:
            dv.staff_badge(k, "PAM", 12, bt + 46, 28, 8)
        for i, (kx, ka) in enumerate(((22, 0.5), (27, 0.9), (17, 0.2))):
            c.save(); c.translate(kx, bt + 74); c.rotate(ka)
            rect(k, -2, 0, 4, 12, px.SILVER, seed + 97 + i, shadow=False, lw=1.2)
            c.set_source_rgb(*px.SILVER); c.arc(0, 0, 3.6, 0, 2 * math.pi); c.fill_preserve()
            c.set_source_rgb(*INK); c.set_line_width(1.2); c.stroke()
            c.restore()
    return hook


def half_moon(c, cx, top, w, h):
    c.move_to(cx - w / 2, top); c.line_to(cx + w / 2, top)
    c.curve_to(cx + w / 2, top + h * 1.2, cx - w / 2, top + h * 1.2, cx - w / 2, top); c.close_path()


def glasses_draw(k, x, y, state, seed=0):
    """Reading glasses: half-moon lenses low on the nose, the eyes peek over; a gold bead chain from the temples."""
    if state in (None, "off"):
        return
    c = k.c
    top = y - 4 if state == "up" else y + 9
    # the chain first (behind the lenses): from each temple tip down past the jaw to the shoulders
    for sx in (-1, 1):
        x0, y0 = x + sx * 41, top + 3
        c.set_source_rgb(*GOLD)
        for i in range(10):
            t = i / 9
            bx = x0 + sx * (4 * math.sin(t * math.pi * 0.9))
            by = y0 + t * 50
            c.arc(bx, by, 1.5, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(2.4); c.set_line_cap(1)
    for sx in (-1, 1):                                                   # temples, out to the hair
        c.move_to(x + sx * 29, top + 1); c.line_to(x + sx * 42, top + 2); c.stroke()
    for sx in (-17, 17):
        half_moon(c, x + sx, top, 25, 10)
        c.set_source_rgba(*LENS, 0.55); c.fill_preserve()
        c.set_source_rgb(*INK); c.set_line_width(2.6); c.stroke()
    c.move_to(x - 5, top + 1); c.curve_to(x - 2, top - 3, x + 2, top - 3, x + 5, top + 1); c.stroke()   # bridge
    if state == "flash":
        c.set_source_rgb(1, 1, 1); c.set_line_width(3.2)
        for sx in (-17, 17):
            c.move_to(x + sx - 6, top + 9); c.line_to(x + sx + 2, top + 1); c.stroke()
        c.save(); c.translate(x + 30, top - 2)                            # the sparkle
        c.move_to(0, -12); c.line_to(2.5, -2.5); c.line_to(12, 0); c.line_to(2.5, 2.5); c.line_to(0, 12)
        c.line_to(-2.5, 2.5); c.line_to(-12, 0); c.line_to(-2.5, -2.5); c.close_path()
        c.set_source_rgb(1, 1, 1); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1.4); c.stroke()
        c.restore()


def _brows(c, x, y, l, r, w=3.4):
    """l, r: ((x0, y0), (x1, y1)) offsets for the screen-left and screen-right brow."""
    c.set_source_rgb(*INK); c.set_line_width(w); c.set_line_cap(1)
    for (a, b) in (l, r):                                 # under her fringe: pulled down 6 and in 3
        ia = 3 if a[0] < 0 else -3
        ib = 3 if b[0] < 0 else -3
        c.move_to(x + a[0] + ia, y + a[1] + 6); c.line_to(x + b[0] + ib, y + b[1] + 6); c.stroke()


def _mouth_erase(k, x, y, seed):
    ellipse(k, x + 1, y + 28, 17, 9, SKIN, seed + 95, shadow=False, outline=False)
    k.c.set_source_rgb(*INK); k.c.set_line_cap(1)


def _mf_faces(inner, gstate, mouth):
    base_of = {"peer": "neutral", "hopeful": "neutral", "fade": "neutral", "approve": "neutral",
               "quiet": "read", "doubt": "neutral", "dinner": "neutral", "happy": "happy"}

    def face_draw(k, x, y, face, look, glasses=False, seed=0):
        c = k.c
        b = base_of.get(face, face)
        if face in ("peer", "hopeful", "fade", "approve", "doubt", "dinner"):
            b = "wide"                                    # pam_tg "wide": open eyes, no lid
        lk = {"peer": (0.8, -0.6), "quiet": (-0.4, 1.0), "dinner": (0.8, 0.2), "doubt": (0.6, 0.6)}.get(face, look)
        inner(k, x, y, b, lk, glasses=False, seed=seed)
        if face == "peer":                                # over the glasses at Don: brows up, a tiny private smile
            _brows(c, x, y, ((-26, -21), (-9, -24)), ((9, -24), (26, -21)))
            _mouth_erase(k, x, y, seed)
            c.set_line_width(3.2); c.move_to(x - 7, y + 27); c.curve_to(x - 2, y + 30, x + 3, y + 30, x + 8, y + 26); c.stroke()
        elif face == "hopeful":                           # brows lift in the middle, a small closed smile
            _brows(c, x, y, ((-26, -19), (-9, -25)), ((9, -25), (26, -19)))
            _mouth_erase(k, x, y, seed)
            c.set_line_width(3.2); c.move_to(x - 8, y + 26); c.curve_to(x - 3, y + 31, x + 3, y + 31, x + 8, y + 26); c.stroke()
        elif face == "fade":                              # the smile goes; mouth flat, a little down at one end
            _brows(c, x, y, ((-26, -17), (-9, -21)), ((9, -21), (26, -17)))
            _mouth_erase(k, x, y, seed)
            c.set_line_width(3.4); c.move_to(x - 9, y + 28); c.line_to(x + 5, y + 28); c.line_to(x + 9, y + 30); c.stroke()
        elif face == "approve":                           # eyes wide, brows high, mouth wide open: the only loud one
            for sx in (-17, 17):
                ellipse(k, x + sx, y, 13, 13, (1, 1, 1), seed + sx, shadow=False, lw=2.2)
                ellipse(k, x + sx + 2, y - 1, 5, 5, INK, seed + sx + 1, shadow=False, outline=False)
            _brows(c, x, y, ((-28, -24), (-9, -30)), ((9, -30), (28, -24)), w=4)
            _mouth_erase(k, x, y, seed)
            ellipse(k, x + 1, y + 30, 11, 9, (0.35, 0.08, 0.08), seed + 5, shadow=False, lw=2.2)
            c.set_source_rgb(0.92, 0.45, 0.45); c.arc(x + 1, y + 34, 5, 0, math.pi); c.fill()
        elif face == "quiet":                             # eyes down to the wrist, calm, the corner of a smile
            _mouth_erase(k, x, y, seed)
            c.set_line_width(3.2); c.move_to(x - 6, y + 28); c.line_to(x + 4, y + 28)
            c.curve_to(x + 6, y + 28, x + 8, y + 27, x + 9, y + 25); c.stroke()
        elif face == "doubt":                             # the moment of doubt: worried brows, a wobbly line
            _brows(c, x, y, ((-26, -17), (-9, -24)), ((9, -24), (26, -17)))
            _mouth_erase(k, x, y, seed)
            c.set_line_width(3.0); c.move_to(x - 8, y + 28)
            c.curve_to(x - 4, y + 25, x - 1, y + 31, x + 2, y + 28); c.curve_to(x + 5, y + 25, x + 7, y + 30, x + 9, y + 28); c.stroke()
        elif face == "dinner":                            # shy hope: blush, brows up, small round "So..."
            c.set_source_rgba(*pt.BLUSH, 0.75)
            for sx in (-26, 26):
                c.save(); c.translate(x + sx, y + 14); c.scale(8, 4.5); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
            _brows(c, x, y, ((-26, -19), (-9, -25)), ((9, -25), (26, -19)))
            if not mouth:
                _mouth_erase(k, x, y, seed)
                c.set_line_width(3.0); c.move_to(x - 6, y + 27); c.curve_to(x - 2, y + 30, x + 2, y + 30, x + 6, y + 27); c.stroke()
        elif face == "happy":                             # what the robot scans: closed happy eyes, a real smile
            c.set_source_rgba(*pt.BLUSH, 0.85)
            for sx in (-26, 26):
                c.save(); c.translate(x + sx, y + 14); c.scale(9, 5); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
            _mouth_erase(k, x, y, seed)
            c.save(); c.move_to(x - 13, y + 23); c.curve_to(x - 6, y + 37, x + 7, y + 37, x + 14, y + 23); c.close_path()
            c.set_source_rgb(0.35, 0.08, 0.08); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.6); c.stroke()
            c.restore()
        if mouth and face == "approve":
            pass
        elif mouth and face in base_of:                   # speaking on an MF face: her small mouths
            _mouth_erase(k, x, y, seed)
            c.save(); c.translate(x, y + 28); c.scale(0.8, 0.8)
            im.mouth(k, 0, 0, mouth, SKIN, erase=(1, 1), seed=seed + 96)
            c.restore()
        glasses_draw(k, x, y, gstate, seed)
    return face_draw


def finger_up(k, hx, hy, s, seed=0):
    """One index finger raised from the fist (shot 5)."""
    c = k.c
    c.save(); c.translate(hx + 2 * s, hy - 6 * s); c.scale(s, s)
    c.move_to(-3, 2); c.line_to(-3, -12); c.arc(0, -12, 3, math.pi, 0); c.line_to(3, 2); c.close_path()
    c.set_source_rgb(*SKIN); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2); c.stroke()
    c.restore()


def pam(k, x, feet, s=1.0, pose="stand", face="neutral", look=(0, 0), seed=40, badge=True, glasses="low",
        cuff=None, finger=False, mouth=None):
    c = k.c
    old_p = dict(kit.PEOPLE["PAM"])
    old_hook, old_face = kit.BADGE_HOOK, kit.face_draw
    tg_face = pt._faces(old_face, mouth if face not in ("peer", "hopeful", "fade", "approve", "quiet", "doubt",
                                                         "dinner", "happy") else None)
    kit.face_draw = _mf_faces(tg_face, glasses, mouth)
    p = dict(old_p); p["body"] = PURPLE
    kit.PEOPLE["PAM"] = p
    kit.BADGE_HOOK = _costume(badge)
    try:
        c.save(); c.translate(x, feet); c.scale(s, s)
        px._legs(k, seed, 1.0)
        c.restore()
        bt = BT
        c.save()                                            # the Thanksgiving v2 waist: hem clip minus two wedges
        c.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
        c.rectangle(x - 4000, feet - 8000, 8000, 8000 + HEM * s)
        for o in (-1, 1):
            w = [(o * 40, bt + 30), (o * 33.5, bt + 84), (o * 42.5, bt + 118), (o * 70, bt + 118), (o * 70, bt + 30)]
            c.move_to(x + w[0][0] * s, feet + w[0][1] * s)
            for q in w[1:]:
                c.line_to(x + q[0] * s, feet + q[1] * s)
            c.close_path()
        c.clip(); c.set_fill_rule(cairo.FILL_RULE_WINDING)
        if not isinstance(pose, str):
            kit.ARM_POSES["_mf"] = pose
            pose = "_mf"
        out = kit.person(k, "PAM", x, feet, s, pose=pose, face=face, seed=seed, look=look, badge=True)
        c.restore()
        c.save(); c.translate(x, feet); c.scale(s, s)
        c.set_source_rgb(*INK); c.set_line_width(2.2); c.set_line_join(1)
        for o in (-1, 1):
            c.move_to(o * 40, bt + 30); c.line_to(o * 33.5, bt + 84); c.line_to(o * 42.5, bt + 118); c.stroke()
        a = kit.ARM_POSES[pose]
        hands = []
        for side, (u, f) in ((-1, (a[0], a[1])), (1, (a[2], a[3]))):
            hands.append(kit.arm(k, side * 40, bt + 14, u, f, PURPLE, SKIN, seed + 10 + side))
        c.restore()
    finally:
        kit.ARM_POSES.pop("_mf", None)
        kit.PEOPLE["PAM"] = old_p
        kit.BADGE_HOOK, kit.face_draw = old_hook, old_face
    hands = [(x + hx * s, feet + hy * s) for hx, hy in hands]
    out["hands"] = hands
    if finger:
        finger_up(k, hands[1][0], hands[1][1], s, seed)
    if cuff:
        hx, hy = hands[0] if cuff == "L" else hands[1]
        pr.cuff(k, hx, hy - 9 * s, s, 0.0)
        out["cuff"] = (hx + (-11 if cuff == "L" else 11) * s, hy - 9 * s)
    out["head"] = (x, feet + HY * s)
    return out
