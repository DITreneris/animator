"""v2 (18 Nov): SWEPT, opt-in: her hair swept over one shoulder in waves, the other ear showing (Customer Success).
sofia_ss_v1.py is pinned; with SWEPT off she draws exactly as before.
SOFIA, "Secret Santa", v1. Office v4 on the newer figure (sofia_mf v2: long hair, teal wrap blouse, block heels),
with this episode's touches (grill, 15 Nov):
- the earrings of the episode: original crystal teardrop drops (no logos), a small gold stud, a short link and a
  faceted teardrop about the size of her hoops, so the sparkle reads in a two-shot; they swing with `lag`, and
  sparkle=0..1 flashes a 4-point star on them (frame 0, the loop);
- a thin gold belt with a round buckle instead of the black belt;
- her classic red lips, now with a touch of gloss (next to Pam's new dusty rose);
- compact_open=0..1: her gold compact mirror held out in her screen-left hand (shot 2).
New pose: "compact". sofia_mf.py, sofia_tg.py, sofia_v4.py and every earlier Sofia are untouched.
Usage: sofia(k, x, feet, s, pose, face_kind, look, lag, seed, badge, lean, step, carry, mouth, sparkle, compact_open)"""
import math
import cairo
import kit
import brand
import sofia_v4 as sf
import sofia_tg as stg
import sofia_mf as sm
import props_ss as props
from kit import INK, cut, rect, ellipse, rough_ellipse_pts, text
from sofia_v4 import SKIN, HAIR, HAIR_SHINE, HAIR_SHADE, RED, GOLD, GOLD_LIGHT, BLOUSE, BLOUSE_SHADE, BELT, H

SKIRT, TIGHTS, PUMPS = sm.SKIRT, sm.TIGHTS, sm.PUMPS
PULLED = [False]                                           # v3, opt-in (Daddy's Home): all of it pulled back into a ponytail
                                                           # drawn by the caller: no back layer, no side locks. sofia_ss_v2.py is pinned
PENCIL = [False]                                           # v4, opt-in (Daddy's Home): a longer, narrower skirt. sofia_ss_v3.py is pinned
SWEPT = [False]                                            # v2, opt-in: all her hair swept over her right shoulder (screen-left)
                                                           # in Hollywood waves; her left ear (screen-right) shows
NOTE_COVER = sm.NOTE_COVER
CRYSTAL = (0.86, 0.94, 1.0)
CRYSTAL_DARK = (0.55, 0.70, 0.86)
DROP_H = sm.HOOP_R * 1.35            # about the size of the Mandatory Fun hoops
POSES = dict(sm.POSES)
POSES["compact"] = (-62, -48, 8, 0)  # her screen-left forearm out and up, the compact toward Pam
notebook, pen = sm.notebook, sm.pen
face = sm.face
BADGE_HOOK = None


def teardrop(k, x, y, lgx=0.0, spark=0.0, seed=0):
    """A gold stud at the lobe (x, y), a short link, a faceted crystal teardrop; swings with lgx."""
    c = k.c
    ellipse(k, x, y, 4.2, 4.2, GOLD, seed, shadow=False, lw=1.6)
    c.save(); c.translate(x, y + 3); c.rotate(-lgx * 0.035)
    c.set_source_rgb(*INK); c.set_line_width(3.2); c.move_to(0, 0); c.line_to(0, 7); c.stroke()
    c.set_source_rgb(*GOLD); c.set_line_width(1.6); c.move_to(0, 0); c.line_to(0, 7); c.stroke()
    w, h = DROP_H * 0.42, DROP_H
    c.translate(0, 7)
    c.move_to(0, 0); c.curve_to(w * 0.9, h * 0.38, w * 1.05, h * 0.78, 0, h)
    c.curve_to(-w * 1.05, h * 0.78, -w * 0.9, h * 0.38, 0, 0); c.close_path()
    c.set_source_rgba(0, 0, 0, 0.15); c.fill_preserve()
    c.set_source_rgb(*CRYSTAL); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(2.0); c.stroke()
    c.set_source_rgb(*CRYSTAL_DARK); c.set_line_width(1.1)                       # facets
    c.move_to(0, h * 0.18); c.line_to(-w * 0.55, h * 0.62); c.line_to(0, h * 0.94); c.line_to(w * 0.55, h * 0.62)
    c.close_path(); c.stroke()
    c.move_to(-w * 0.55, h * 0.62); c.line_to(w * 0.55, h * 0.62); c.stroke()
    c.set_source_rgba(1, 1, 1, 0.9); c.set_line_width(1.8); c.set_line_cap(1)
    c.move_to(-w * 0.35, h * 0.40); c.line_to(-w * 0.12, h * 0.26); c.stroke()      # the glint
    props.sparkle(c, -w * 0.5, h * 0.3, 9 + 7 * spark, spark)
    c.restore()


def _swept(k, hy, body_top, lgx, lgy, seed):
    """v2: the waves over her right shoulder (screen-left), in three scallops; on the other side the hair is tucked
    behind her ear, and the ear shows."""
    c = k.c
    w = lgx * 0.6
    pts = [(-30, hy - 34), (-58, hy - 22), (-64 + w, hy + 14), (-54 + w, hy + 36), (-68 + w, hy + 58), (-58 + w, hy + 80),
           (-70 + w, hy + 100), (-58 + w, hy + 120 + lgy), (-40 + w, hy + 124 + lgy), (-36 + w, hy + 104), (-30 + w, hy + 86),
           (-40 + w, hy + 66), (-34 + w, hy + 46), (-44, hy + 24), (-44, hy - 6)]
    cut(k, pts, HAIR, shadow=False, lw=2)
    c.set_source_rgb(*HAIR_SHADE); c.set_line_width(2.2); c.set_line_cap(1)             # the wave lines
    for y0 in (hy + 30, hy + 70, hy + 106):
        c.move_to(-58 + w, y0); c.curve_to(-48 + w, y0 - 8, -40 + w, y0 + 8, -32 + w, y0); c.stroke()
    c.set_source_rgb(*HAIR_SHINE); c.set_line_width(3.2)
    c.move_to(-54 + w, hy + 8); c.curve_to(-48 + w, hy + 22, -56 + w, hy + 40, -50 + w, hy + 54); c.stroke()
    ellipse(k, 50, hy + 8, 8, 12, SKIN, seed + 25, shadow=False, lw=1.8)                  # her left ear, the hair behind it
    c.set_source_rgb(*INK); c.set_line_width(1.6); c.move_to(48, hy - 18); c.curve_to(58, hy - 10, 58, hy, 54, hy + 6); c.stroke()


def sofia(k, x, feet, s=1.0, pose="stand", face_kind="neutral", look=(0, 0), lag=(0, 0), seed=7, badge=True,
          lean=0.0, step=None, carry=False, mouth=None, sparkle=0.0, compact_open=None):
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
    if SWEPT[0]:                                           # v2: the mass goes to one side, behind her right shoulder
        back = [(-52 + lgx, hy - 30), (-80 + lgx * 1.4, body_top + 20), (-84 + lgx * 1.8, body_top + 120 + lgy),
                (-58 + lgx * 1.8, body_top + 142 + lgy), (-30 + lgx * 1.8, body_top + 110 + lgy), (20 + lgx, body_top + 10),
                (50 + lgx, hy + 6), (54 + lgx, hy - 30)]
    if not PULLED[0]:
        cut(k, back, HAIR, lw=2.2)
    if not SWEPT[0] and not PULLED[0]:
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
    if PENCIL[0]:
        cut(k, [(-29, body_top + 102), (29, body_top + 102), (41, body_top + 120), (35, -66), (-35, -66),
                (-41, body_top + 120)], SKIRT)
    else:
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
    rect(k, -31, body_top + 98, 62, 6, GOLD, seed + 45, shadow=False, lw=1.4)      # the thin gold belt
    c.set_source_rgb(*GOLD_LIGHT); c.rectangle(-30, body_top + 99, 60, 1.6); c.fill()
    ellipse(k, 0, body_top + 101, 5, 5, GOLD, seed + 46, shadow=False, lw=1.4)        # its round buckle
    ellipse(k, 0, body_top + 101, 2.2, 2.2, GOLD_LIGHT, seed + 47, shadow=False, outline=False)
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
    if compact_open is not None:                          # the compact held out in her screen-left hand
        hx_, hy_ = hands[0]
        props.compact(k, hx_ - 4, hy_ - 14, 1.0, -0.1, compact_open, seed + 85)
        ellipse(k, hx_, hy_, 9, 9, SKIN, seed + 86, shadow=False, lw=2)
    if carry or pose == "carry":                          # the closed notebook against her chest
        hx_, hy_ = hands[0]
        c.save(); c.translate(hx_ + 22, hy_ - 18); c.rotate(-0.12)
        rect(k, -20, -30, 40, 58, NOTE_COVER, seed + 80, lw=2)
        c.set_source_rgb(1, 1, 1); c.rectangle(-11, -18, 22, 7); c.fill()
        c.restore()
        ellipse(k, hx_, hy_, 9, 9, SKIN, seed + 81, shadow=False, lw=2)
    # head, front hair (v4), locks, hoops
    ellipse(k, 0, hy, 50, 50, SKIN, seed + 20)
    cap = rough_ellipse_pts(k, 0, hy - 10, 54, 48 if not PULLED[0] else 44, seed + 21)
    cap = [q for q in cap if q[1] < hy - 30] + [(53, hy - 24), (30, hy - 40), (0, hy - 44), (-30, hy - 40), (-53, hy - 22)]
    cap.sort(key=lambda q: math.atan2(q[1] - (hy - 10), q[0]))
    cut(k, cap, HAIR, shadow=False, lw=2)
    if PULLED[0]:                                          # v4: no fringe, no parting: combed straight back, close to the head
        crown = [(math.cos(a_) * 54, hy - 12 + math.sin(a_) * 44) for a_ in
                 [math.pi * (1.03 + 0.94 * i / 11) for i in range(12)]]
        cut(k, crown + [(52, hy - 26), (28, hy - 42), (0, hy - 47), (-28, hy - 42), (-52, hy - 26)], HAIR, shadow=False, lw=2)
        c.set_source_rgb(*HAIR_SHINE); c.set_line_width(3.2); c.set_line_cap(1)
        for x0 in (-30, -8, 14):
            c.move_to(x0, hy - 44); c.curve_to(x0 + 6, hy - 52, x0 + 14, hy - 56, x0 + 22, hy - 55); c.stroke()
    else:
        crown = [(math.cos(a_) * 58, hy - 16 + math.sin(a_) * 50) for a_ in
                 [math.pi * (1.05 + 0.9 * i / 11) for i in range(12)]]
        cut(k, crown + [(54, hy - 22), (24, hy - 40), (-26, hy - 34), (-56, hy - 22)], HAIR, shadow=False, lw=2)
        c.set_source_rgb(*INK); c.set_line_width(2)
        c.move_to(-22, hy - 64); c.curve_to(-26, hy - 54, -30, hy - 44, -26, hy - 34); c.stroke()
        c.set_source_rgb(*HAIR_SHINE); c.set_line_width(4.5); c.set_line_cap(1)
        c.move_to(-34, hy - 48); c.curve_to(-18, hy - 56, 2, hy - 56, 18, hy - 50); c.stroke()
    if SWEPT[0]:
        _swept(k, hy, body_top, lgx, lgy, seed)
    elif not PULLED[0]:
        for sx_ in (-1, 1):
            lx0 = sx_ * 50
            cut(k, [(lx0 - 8 * sx_, hy - 20), (lx0 + 12 * sx_, hy - 24), (lx0 + 17 * sx_ + lgx * 0.6, hy + 56 + lgy),
                    (lx0 + 6 * sx_ + lgx * 0.6, hy + 70 + lgy), (lx0 - 6 * sx_ + lgx * 0.6, hy + 62 + lgy)],
                HAIR, shadow=False, lw=2)
    for sx_ in (-1, 1):                                   # the crystal teardrops, swinging with lag
        teardrop(k, sx_ * 53 + lgx * 0.6, hy + 22, lgx, sparkle if sx_ > 0 else sparkle * 0.55, seed + 30 + sx_)
    face(k, 0, hy + 4, face_kind, look, seed + 60)
    if not mouth and face_kind not in ("horrified", "curious", "surprised"):   # the classic red, a touch of gloss
        c.set_source_rgba(1, 1, 1, 0.75); c.set_line_width(2.0); c.set_line_cap(1)
        c.move_to(-4, hy + 4 + 31); c.line_to(2, hy + 4 + 31); c.stroke()
    if mouth:                                             # v2: 20 % smaller: she barely moves her lips
        import iwry_mouths as im
        ellipse(k, 1, hy + 4 + 28, 19, 10, SKIN, seed + 66, shadow=False, outline=False)
        c.save(); c.translate(0, hy + 4 + 29); c.scale(0.8, 0.8)
        im.mouth(k, 0, 0, mouth, SKIN, lip_col=RED, inner=(0.45, 0.06, 0.08), erase=(1, 1), seed=seed + 67)
        c.restore()
    c.restore()
    return {"head": (x, feet + bob + hy * s), "hands": [(x + hx * s, feet + bob + hyy * s) for hx, hyy in hands]}
