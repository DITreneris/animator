"""v2 (sofia_mf_v1.py = v1, kept), after review: "done" face (relaxed shut lids, a small exhale; "For what?" is the
signature eyebrow with a side-eye at Don); a page turn that reads (the page lifts in an arc, 45-60 degrees, over the
spine); visible block heels; hoops set further from the jaw with a darker inner edge (not bigger); the walk keeps the
notebook at her chest (one continuous exit) with a longer stride and the free arm swinging; speaking mouths 20 %
smaller (she barely moves her lips).

SOFÍA, "Mandatory Fun", v1. Her office v4 look (sofia_v4.py: teal wrap blouse, black skirt, belt with a gold buckle,
staff badge, long blonde hair with the darker under-layer and face-framing locks) on the newer figure carried
forward from Christmas (soft bust, narrow belted waist, hips, shaped legs, black pumps), plus:
- big gold hoops, 1.3x the v4 hoop, dark outline, swinging with `lag` (head turns, the walk-out);
- a notebook and pen: she writes, turns a page, closes it (notebook(): open / turning / closed);
- a walk-out: `step` (0..1, one stride) shifts the legs and bobs the body for the exit in shot 11.
New poses: "write" (pen hand down to the page, the other hand on the notebook), "page" (flicking the page over),
"close" (both hands pressing the notebook shut), "carry" (notebook against her chest), "walk" (arms swinging, with step).
Faces: all of sofia_tg.face (neutral, eyebrow, closed, unimpressed, knowing, tiny ...).
sofia_v4.py, sofia_tg*.py and every earlier render are untouched.
Usage: sofia(k, x, feet, s, pose, face_kind, look, lag, step=None, notebook_state=None, mouth=None)"""
import math
import cairo
import kit
import brand
import sofia_v4 as sf
import sofia_tg as stg
from kit import INK, cut, rect, ellipse, rough_ellipse_pts, text
from sofia_v4 import SKIN, HAIR, HAIR_SHINE, HAIR_SHADE, RED, GOLD, GOLD_LIGHT, BLOUSE, BLOUSE_SHADE, BELT, H

SKIRT = sf.SKIRT
TIGHTS = sf.TIGHTS
PUMPS = (0.08, 0.08, 0.09)
HOOP_R = sf.HOOP_R * 1.3
NOTE_COVER = (0.20, 0.34, 0.62)
NOTE_PAGE = (0.99, 0.98, 0.93)
PEN = (0.12, 0.14, 0.20)

POSES = dict(stg.POSES)
POSES.update({
    "write": (-30, 120, 18, -40),      # left hand flat on the notebook, right hand down with the pen
    "page": (-30, 120, 36, -96),       # right hand up, flicking the page over
    "close": (-28, 118, 28, -118),     # both hands pressing the notebook shut
    "carry": (-34, 130, 30, -60),      # notebook held against her chest, left arm
    "walk": (-14, 0, 14, 0),           # arms swing with step (set in sofia())
})


def notebook(k, x, y, s=1.0, state="open", turn=0.0, ang=-0.08, seed=0):
    """Lying on the table, seen at a shallow angle. state: open / closed; turn 0..1 flips the right page over."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s * 0.5)
    if state == "closed":
        rect(k, -30, -40, 60, 80, NOTE_COVER, seed, lw=2.4)
        c.set_source_rgb(1, 1, 1); c.rectangle(-16, -24, 32, 10); c.fill()
        c.set_source_rgb(*INK); c.set_line_width(1.5); c.rectangle(-16, -24, 32, 10); c.stroke()
    else:
        rect(k, -62, -42, 124, 84, NOTE_COVER, seed, lw=2.4)
        for sx_ in (-1, 1):
            rect(k, -58 if sx_ < 0 else 2, -38, 56, 76, NOTE_PAGE, seed + 1 + sx_, shadow=False, lw=1.6)
        c.set_source_rgb(0.62, 0.70, 0.86); c.set_line_width(1.6)
        for i in range(6):
            yy = -24 + i * 11
            c.move_to(-52, yy); c.line_to(-8, yy); c.stroke()
            c.move_to(8, yy); c.line_to(52, yy); c.stroke()
        c.set_source_rgb(*INK); c.set_line_width(2.2)             # her handwriting (unreadable on purpose)
        for i in range(3):
            yy = -26 + i * 11
            c.move_to(-50, yy)
            for j in range(9):
                c.line_to(-50 + j * 4.5, yy - 2.5 * math.sin(j * 1.9 + i))
            c.stroke()
        c.set_source_rgb(*INK); c.set_line_width(2); c.move_to(0, -42); c.line_to(0, 42); c.stroke()
    c.restore()
    if state != "closed" and turn > 0:                           # v2: the page lifts in an arc over the spine
        th = math.pi * min(turn, 1.0)
        c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
        xt, lift = 56 * math.cos(th), -52 * math.sin(th)
        c.move_to(0, -19)
        c.curve_to(xt * 0.5, -19 + lift * 0.9, xt * 0.9, -19 + lift, xt, -16 + lift)
        c.line_to(xt, 19 + lift * 0.75)
        c.curve_to(xt * 0.9, 19 + lift * 0.7, xt * 0.5, 19 + lift * 0.6, 0, 19)
        c.close_path()
        c.set_source_rgb(*NOTE_PAGE); c.fill_preserve()
        c.set_source_rgb(*INK); c.set_line_width(2); c.stroke()
        c.set_source_rgb(0.62, 0.70, 0.86); c.set_line_width(1.2)
        for i in range(3):
            c.move_to(xt * 0.15, -10 + i * 9 + lift * 0.2); c.line_to(xt * 0.85, -10 + i * 9 + lift * 0.85); c.stroke()
        c.restore()


def pen(k, hx, hy, s=1.0, ang=0.5):
    c = k.c
    c.save(); c.translate(hx, hy); c.rotate(ang)
    rect(k, -2.5 * s, -2 * s, 5 * s, 30 * s, PEN, 1400, shadow=False, lw=1.4 * s)
    c.set_source_rgb(*GOLD); c.rectangle(-2.5 * s, -2 * s, 5 * s, 4 * s); c.fill()
    c.restore()
    ellipse(k, hx, hy, 9, 9, SKIN, 1401, shadow=False, lw=2)
    ellipse(k, hx - 3, hy + 5, 3, 3, RED, 1402, shadow=False, outline=False)


def face(k, x, y, kind="neutral", look=(0, 0), seed=0):
    """sofia_tg.face plus "done": lids fully relaxed shut, a small exhale from the corner of her mouth."""
    if kind != "done":
        return stg.face(k, x, y, kind, look, seed)
    c = k.c
    stg.face(k, x, y, "closed", look, seed)
    c.set_source_rgba(*INK, 0.55); c.set_line_width(2); c.set_line_cap(1)
    for i, (dx_, dy_) in enumerate(((24, 26), (32, 21), (40, 17))):
        c.arc(x + dx_, y + dy_, 3 + i, math.pi * 1.1, math.pi * 1.9); c.stroke()


BADGE_HOOK = None


def sofia(k, x, feet, s=1.0, pose="stand", face_kind="neutral", look=(0, 0), lag=(0, 0), seed=7, badge=True,
          lean=0.0, step=None, carry=False, mouth=None):
    """Returns {"head", "hands"} in canvas coordinates (lean not applied to the returned points)."""
    c = k.c
    ph = step if step is not None else 0.0
    bob = -4 * abs(math.sin(math.pi * 2 * ph)) if step is not None else 0.0
    c.save(); c.translate(x, feet + bob); c.rotate(math.radians(lean)); c.scale(s, s)
    body_top = -300 * H + 78
    hy = body_top - 44
    lgx, lgy = lag
    # long hair, back layer, and the darker under-layer (office v4 exactly)
    back = [(-52 + lgx, hy - 30), (-72 + lgx * 1.4, body_top + 30), (-66 + lgx * 1.8, body_top + 96 + lgy),
            (-46 + lgx * 1.8, body_top + 108 + lgy), (-18 + lgx * 1.8, body_top + 102 + lgy),
            (18 + lgx * 1.8, body_top + 102 + lgy), (46 + lgx * 1.8, body_top + 108 + lgy),
            (66 + lgx * 1.8, body_top + 96 + lgy), (72 + lgx * 1.4, body_top + 30), (52 + lgx, hy - 30)]
    cut(k, back, HAIR, lw=2.2)
    cut(k, [(-40 + lgx, hy + 10), (-50 + lgx * 1.5, body_top + 80 + lgy), (-24 + lgx * 1.7, body_top + 96 + lgy),
            (24 + lgx * 1.7, body_top + 96 + lgy), (50 + lgx * 1.5, body_top + 80 + lgy), (40 + lgx, hy + 10)],
        HAIR_SHADE, shadow=False, outline=False)
    # legs: shaped, dark tights, black pumps; a stride when walking
    for i, sx_ in enumerate((-14, 14)):
        o = 1 if sx_ > 0 else -1
        sw = math.sin(math.pi * 2 * ph + (0 if i == 0 else math.pi)) if step is not None else 0.0
        dx_ = 11 * sw
        lift = 9 * max(0.0, sw) if step is not None else 0.0
        c.save(); c.translate(dx_, -lift)
        cut(k, [(sx_ - 8.5, -100 + lift), (sx_ + 8.5, -100 + lift), (sx_ + 6, -60), (sx_ + 7.5, -42), (sx_ + 4.5, -10),
                (sx_ - 4.5, -10), (sx_ - 7.5, -42), (sx_ - 6, -60)], TIGHTS, shadow=False, lw=1.8)
        cut(k, [(sx_ - o * 6.5, -8), (sx_ - o * 2.5, -8), (sx_ - o * 3.5, 0), (sx_ - o * 6.5, 0)], PUMPS,
            shadow=False, lw=1.6)                          # v2: a visible block heel
        cut(k, [(sx_ - 6, -13), (sx_ + 6, -13), (sx_ + 6 + o * 11, 0), (sx_ - 1 + o * 3, 0), (sx_ - 6, -7)], PUMPS,
            shadow=False, lw=1.8)
        c.restore()
    cut(k, [(-29, body_top + 102), (29, body_top + 102), (45, body_top + 116), (50, -92), (-50, -92),
            (-45, body_top + 116)], SKIRT)
    # the v4 teal wrap blouse on the newer figure
    top = [(-37, body_top), (37, body_top), (41, body_top + 40), (29, body_top + 102), (-29, body_top + 102),
           (-41, body_top + 40)]
    cut(k, top, BLOUSE)
    cut(k, [(-14, body_top), (14, body_top), (0, body_top + 30)], SKIN, shadow=False, lw=1.8)
    cut(k, [(14, body_top), (37, body_top), (41, body_top + 40), (29, body_top + 98), (-22, body_top + 98),
            (4, body_top + 40)], BLOUSE, shadow=False, lw=2)
    c.set_source_rgb(*BLOUSE_SHADE); c.set_line_width(2.2); c.set_line_cap(1)
    c.arc(-18, body_top + 36, 15, 0.12 * math.pi, 0.80 * math.pi); c.stroke()
    c.arc(18, body_top + 36, 15, 0.20 * math.pi, 0.88 * math.pi); c.stroke()
    c.move_to(-27, body_top + 64); c.curve_to(-22, body_top + 78, -22, body_top + 88, -24, body_top + 98); c.stroke()
    rect(k, -31, body_top + 96, 62, 10, BELT, seed + 45, shadow=False, lw=1.6)
    rect(k, -8, body_top + 94, 16, 14, GOLD, seed + 46, shadow=False, lw=1.6)
    c.set_source_rgb(*BELT); c.rectangle(-4, body_top + 98, 8, 6); c.fill()
    if badge and BADGE_HOOK is not None:
        BADGE_HOOK(k, body_top, seed)
    elif badge:
        rect(k, 8, body_top + 50, 32, 20, (1, 1, 1), seed + 40, shadow=False, lw=1.6)
        c.set_source_rgb(*brand.GREEN); c.rectangle(11, body_top + 52, 26, 3.5); c.fill()
        text(k, "SOFÍA", 24, body_top + 62, 9, INK)
    a = POSES.get(pose) or kit.ARM_POSES[pose]
    if pose == "walk" and step is not None:
        swing = 26 * math.sin(math.pi * 2 * ph)
        a = (-14 - swing, 10, 14 - swing, -10)
        if carry:                                          # v2: the notebook stays at her chest; the free arm swings
            a = (POSES["carry"][0], POSES["carry"][1], 14 - swing, -12)
    hands = [sf._arm(k, -39, body_top + 14, a[0], a[1], seed + 9, w=15),
             sf._arm(k, 39, body_top + 14, a[2], a[3], seed + 11, w=15)]
    if carry or pose == "carry":                          # the closed notebook against her chest
        hx_, hy_ = hands[0]
        c.save(); c.translate(hx_ + 22, hy_ - 18); c.rotate(-0.12)
        rect(k, -20, -30, 40, 58, NOTE_COVER, seed + 80, lw=2)
        c.set_source_rgb(1, 1, 1); c.rectangle(-11, -18, 22, 7); c.fill()
        c.restore()
        ellipse(k, hx_, hy_, 9, 9, SKIN, seed + 81, shadow=False, lw=2)
    # head, front hair (v4), locks, hoops
    ellipse(k, 0, hy, 50, 50, SKIN, seed + 20)
    cap = rough_ellipse_pts(k, 0, hy - 10, 54, 48, seed + 21)
    cap = [q for q in cap if q[1] < hy - 30] + [(53, hy - 24), (30, hy - 40), (0, hy - 44), (-30, hy - 40), (-53, hy - 22)]
    cap.sort(key=lambda q: math.atan2(q[1] - (hy - 10), q[0]))
    cut(k, cap, HAIR, shadow=False, lw=2)
    crown = [(math.cos(a_) * 58, hy - 16 + math.sin(a_) * 50) for a_ in
             [math.pi * (1.05 + 0.9 * i / 11) for i in range(12)]]
    cut(k, crown + [(54, hy - 22), (24, hy - 40), (-26, hy - 34), (-56, hy - 22)], HAIR, shadow=False, lw=2)
    c.set_source_rgb(*INK); c.set_line_width(2)
    c.move_to(-22, hy - 64); c.curve_to(-26, hy - 54, -30, hy - 44, -26, hy - 34); c.stroke()
    c.set_source_rgb(*HAIR_SHINE); c.set_line_width(4.5); c.set_line_cap(1)
    c.move_to(-34, hy - 48); c.curve_to(-18, hy - 56, 2, hy - 56, 18, hy - 50); c.stroke()
    for sx_ in (-1, 1):
        lx0 = sx_ * 50
        cut(k, [(lx0 - 8 * sx_, hy - 20), (lx0 + 12 * sx_, hy - 24), (lx0 + 17 * sx_ + lgx * 0.6, hy + 56 + lgy),
                (lx0 + 6 * sx_ + lgx * 0.6, hy + 70 + lgy), (lx0 - 6 * sx_ + lgx * 0.6, hy + 62 + lgy)],
            HAIR, shadow=False, lw=2)
    for sx_ in (-1, 1):                                   # big gold hoops (1.3x v4), swinging with lag
        hx0, hy0 = sx_ * 53 + lgx * 1.0, hy + 24 + HOOP_R + abs(lgx) * 0.25     # v2: further from the jaw
        c.set_source_rgb(*INK); c.set_line_width(9); c.arc(hx0, hy0, HOOP_R, 0, 2 * math.pi); c.stroke()
        c.set_source_rgb(*GOLD); c.set_line_width(6); c.arc(hx0, hy0, HOOP_R, 0, 2 * math.pi); c.stroke()
        c.set_source_rgb(0.45, 0.30, 0.05); c.set_line_width(1.6)               # v2: darker inner edge
        c.arc(hx0, hy0, HOOP_R - 2.8, 0, 2 * math.pi); c.stroke()
        c.set_source_rgb(*GOLD_LIGHT); c.set_line_width(2.2)
        c.arc(hx0, hy0, HOOP_R, 1.15 * math.pi, 1.55 * math.pi); c.stroke()
    face(k, 0, hy + 4, face_kind, look, seed + 60)
    if mouth:                                             # v2: 20 % smaller: she barely moves her lips
        import iwry_mouths as im
        ellipse(k, 1, hy + 4 + 28, 19, 10, SKIN, seed + 66, shadow=False, outline=False)
        c.save(); c.translate(0, hy + 4 + 29); c.scale(0.8, 0.8)
        im.mouth(k, 0, 0, mouth, SKIN, lip_col=RED, inner=(0.45, 0.06, 0.08), erase=(1, 1), seed=seed + 67)
        c.restore()
    c.restore()
    return {"head": (x, feet + bob + hy * s), "hands": [(x + hx * s, feet + bob + hyy * s) for hx, hyy in hands]}
