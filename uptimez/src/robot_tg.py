"""v2 (robot_tg_v1.py = v1, kept), after review: the HR card is taller and the lettering sits inside it with a margin
(tg_badge); the verdict words are ~25 % bigger, heavier (ink outline under the colour) and condensed to fit;
the paper hat is visibly homemade: one half of the crown folded lighter, an uneven brim, two opaque tape strips.

The HR robot, Thanksgiving film ("Raises for Everyone"), v1. The waiter robot from "I Will Replace You"
(waiter_kit.py, untouched) as promoted in the Christmas special: the big HR badge (santa_robot.hr_badge, with the
lettering fix) and the larger v3 screen, but no Santa suit. Its only costume:
- a pilgrim hat folded from black paper, a gold paper buckle, sitting crooked, held on with two strips of tape.
The verdicts are the screen itself: the face goes and one big word fills it, "POLICY VIOLATION." in red,
"ACCURATE." in green, with a glow round the screen. Screen states: "eager" (idle), "scan" (eyes sweep, scan line),
"violation", "accurate", plus any waiter_kit / santa_robot face ("stern", "smug", ...).
Usage: robot(k, x, feet, s, pose, screen, look, side, head_dx, head_rot, seed=900) -> points + "screen" (centre)."""
import math
import cairo
import kit
import waiter_kit as w
import santa_robot as sr
from kit import INK, cut, rect, ellipse, text

PAPER_BLACK = (0.13, 0.13, 0.15)
PAPER_FOLD = (0.28, 0.28, 0.31)
BUCKLE = (0.95, 0.76, 0.22)
TAPE = (0.96, 0.92, 0.70)
RED = (1.00, 0.30, 0.26)
GREEN = (0.30, 0.95, 0.42)
SCREEN_RX, SCREEN_RY = 46, 38
WORDS = {"violation": (("POLICY", "VIOLATION."), RED), "accurate": (("ACCURATE.",), GREEN)}


def pilgrim_hat(k, seed=0):
    """Head-local units (screen centre 0, 0; head 50 x 44). Folded paper, crooked, taped."""
    c = k.c
    c.save(); c.translate(-4, -38); c.rotate(-0.09)
    cut(k, [(-30, 0), (30, 0), (25, -50), (-24, -52)], PAPER_BLACK, lw=2.4)
    cut(k, [(0, 0), (30, 0), (25, -50), (1, -51)], PAPER_FOLD, shadow=False, lw=1.6)   # folded-over half, lighter
    c.set_source_rgb(0.42, 0.42, 0.46); c.set_line_width(1.6)
    c.move_to(1, -51); c.line_to(14, -30); c.line_to(29, -3); c.stroke()             # a second crease
    cut(k, [(-30, -16), (29, -16), (30, -6), (-31, -6)], (0.30, 0.30, 0.33), shadow=False, lw=1.8)  # band
    c.set_source_rgb(*INK); c.rectangle(-9, -19, 18, 15); c.fill()     # paper buckle
    c.set_source_rgb(*BUCKLE); c.rectangle(-7.5, -17.5, 15, 12); c.fill()
    c.set_source_rgb(*PAPER_BLACK); c.rectangle(-3.5, -14, 7, 5); c.fill()
    cut(k, [(-50, 3), (-30, 0), (-10, 2), (12, -1), (34, 1), (50, -2), (47, 8), (20, 6), (-8, 10), (-49, 9)],
        PAPER_BLACK, lw=2.2)                                            # brim, cut unevenly
    c.restore()
    for (tx, ty, ta) in ((-44, -27, 0.9), (41, -33, -0.8)):            # opaque tape onto the head shell
        c.save(); c.translate(tx, ty); c.rotate(ta)
        rect(k, -9, -4, 18, 8, TAPE, seed + 3, shadow=False, lw=1.2)
        c.restore()


def tg_badge(k, x0, y0, seed, label="HR"):
    """v2: a taller card (58 x 40); the HR lettering sits inside it with a clear margin."""
    c = k.c
    wd, ht = 58, 40
    x0 -= 4; y0 -= 6
    rect(k, x0 + wd / 2 - 5, y0 - 5, 10, 6, (0.45, 0.47, 0.52), seed + 1, shadow=False, lw=1.2)
    rect(k, x0, y0, wd, ht, (1, 1, 1), seed, shadow=False, lw=1.8)
    c.set_source_rgb(*sr.kit_brand_green()); c.rectangle(x0 + 2, y0 + 2, wd - 4, 6); c.fill()
    c.save()
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(20)
    e = c.text_extents(label)
    c.set_source_rgb(*INK)
    c.move_to(x0 + wd / 2 - e.x_bearing - e.width / 2, y0 + 8 + (ht - 8) / 2 - e.y_bearing - e.height / 2)
    c.show_text(label)
    c.restore()


def _word(k, lines, col):
    """v2: ~25 % bigger, an ink outline under the colour, condensed to fit the screen."""
    c = k.c
    size = 19 if len(lines) == 2 else 21
    ys = (-5, 16) if len(lines) == 2 else (8,)
    for txt, ty in zip(lines, ys):
        c.save()
        c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(size)
        tw = c.text_extents(txt).x_advance
        sc = min(1.0, (SCREEN_RX * 2 - 10) / tw)
        c.translate(0, ty); c.scale(sc, 1)
        c.move_to(-tw / 2, 0); c.text_path(txt)
        c.set_source_rgba(*col, 0.35); c.set_line_width(6); c.stroke_preserve()     # glow
        c.set_source_rgb(0.02, 0.04, 0.08); c.set_line_width(2.6); c.stroke_preserve()
        c.set_source_rgb(*col); c.fill()
        c.restore()


def screen(k, state, look=(0, 0), talk=0.0, side=1, seed=0, t=0.0):
    """Draws the screen and its content in head-local units."""
    c = k.c
    if state in WORDS:
        lines, col = WORDS[state]
        c.set_source_rgba(*col, 0.28); c.save(); c.scale(SCREEN_RX + 9, SCREEN_RY + 9); c.arc(0, 0, 1, 0, 2 * math.pi)
        c.restore(); c.fill()                                           # glow round the screen
    ellipse(k, 0, 0, SCREEN_RX, SCREEN_RY, w.SCREEN, seed, shadow=False, lw=2)
    c.save(); c.scale(side, 1)
    if state in WORDS:
        _word(k, *WORDS[state])
    else:
        face = "eager" if state == "scan" else state
        c.save(); c.scale(sr.FACE_SCALE, sr.FACE_SCALE)
        old_glow, old_stern = w.GLOW, w.GLOW_STERN
        w.GLOW, w.GLOW_STERN = sr.GLOW_V3, sr.STERN_V3
        try:
            sr._screen_face_v2(w.screen_face)(k, face, look=(look[0] * side, look[1]), talk=talk, side=side)
        finally:
            w.GLOW, w.GLOW_STERN = old_glow, old_stern
        c.restore()
        if state == "scan":                                          # a scan line sweeping the screen
            sy = -SCREEN_RY + 10 + (t % 1.0) * (SCREEN_RY * 2 - 20)
            c.save(); c.scale(SCREEN_RX, SCREEN_RY); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.clip()
            c.set_source_rgba(*sr.GLOW_V3, 0.35); c.rectangle(-SCREEN_RX, sy - 3, SCREEN_RX * 2, 6); c.fill()
            c.set_source_rgb(*sr.GLOW_V3); c.rectangle(-SCREEN_RX, sy - 0.8, SCREEN_RX * 2, 1.6); c.fill()
    c.restore()


def robot(k, x, feet, s=1.0, pose="stand", state="eager", look=(0, 0), side=1, talk=0.0, seed=900, badge=True,
          head_dx=None, head_rot=None, wobble=0.0, t=0.0):
    c = k.c
    old_badge, old_fix = w._badge, sr.HR_FIX
    w._badge = tg_badge
    try:
        out = w.robot(k, x, feet, s, pose, "eager", look, wobble, side, talk, None, seed, badge, None, head_dx, head_rot)
    finally:
        w._badge, sr.HR_FIX = old_badge, old_fix
    named = isinstance(pose, str)
    tilt = (w.POSES[pose] if named else pose)[0] + wobble
    hdx = head_dx if head_dx is not None else (w.HEAD_DX.get(pose, 0) if named else 0)
    hrot = head_rot if head_rot is not None else (w.HEAD_ROT.get(pose, 0) if named else 0)
    hx, hy = out["head"]
    c.save(); c.translate(x, feet); c.scale(s * side, s); c.rotate(tilt)
    c.translate(hdx, (hy - feet) / s); c.rotate(hrot)
    ellipse(k, 0, 0, 50, 44, w.BODY, seed + 68, shadow=False, lw=2.4)   # repaint the head over the antenna
    screen(k, state, look, talk, side, seed + 69, t)
    pilgrim_hat(k, seed + 71)
    c.restore()
    out["screen"] = (x + hdx * s * side, hy)
    return out
