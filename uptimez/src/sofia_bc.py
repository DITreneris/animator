"""v2 (sofia_bc_v1.py = v1, kept), after the audit (shock, cheerful, flirtatious, neutral is not her):
- "flustered": the round mouth is 18 % smaller: a brief involuntary crack, not panic;
- "sideeye" is rebuilt on the neutral face: eyes open and narrowed from below, both pupils hard to the side, her
  normal brows, a tiny closed mouth pulled to one side. "I saw that", not "I like what I see";
- "deadpan" (new) is her look to camera: her signature one raised eyebrow, lids a little lowered, pupils dead
  centre, lips pressed flat. Hold it 0.5 to 0.7 s;
- "paddle" keeps the paddle beside her head, so the shot needs no change of scale;
- the earrings get a soft shadow on the hair behind them, so gold separates from blonde.
SOFIA, "The Best Candidate", v1: on the interview panel. Office v4 on the newer figure (sofia_ss / sofia_mf: long
hair, teal wrap blouse, gold belt, block heels) with this episode's touches (grill, 16 Nov):
- a fitted ink-navy panel blazer worn open over the blouse, sleeves pushed to the elbow, one gold button;
- the earrings of the episode: original gold fringe drops (a stud and three fine chains of different lengths, each
  ending in a gold bead, no logos), about twice the length of her hoops; each chain swings on its own with `lag`,
  so when she loses her cool the earrings show it first;
- two new faces: "flustered" (wide eyes, a blush, a small round mouth: her one crack in the series, for the macho)
  and "sideeye" (half lids, the look thrown sideways: she clocks the curler and the thread); every sofia_tg face
  still works ("eyebrow" with look=(0, 0) is her look to camera at the reveal).
New poses: "paddle" (the YES paddle up in her screen-right hand), "chest" (screen-left hand on her chest, the other
hand up and open: the pen has just left it), "ask" (pen hand up, the standard question).
Extras: paddle="YES"/"NO" draws the vote paddle in her raised hand; pen_drop=0..1 draws her pen falling.
sofia_ss.py, sofia_mf.py, sofia_tg.py, sofia_v4.py and every earlier Sofia are untouched (the blouse colour used
for the sleeves, the earring and the face function are swapped for the length of one call and restored).
Usage: sofia(k, x, feet, s, pose, face_kind, look, lag, seed, badge, lean, mouth, sparkle, paddle, pen_drop)"""
import math
import kit
import brand
import sofia_v4 as sf
import sofia_mf as sm
import sofia_ss as ss
import props_ss
import props_bc as props
from kit import INK, cut, rect, ellipse, text
from sofia_v4 import GOLD, GOLD_LIGHT, H

BLAZER = (0.13, 0.15, 0.24)
BLAZER_EDGE = (0.30, 0.33, 0.46)
BLUSH = (0.96, 0.45, 0.50)
DROP = sm.HOOP_R * 2.1
POSES = dict(ss.POSES)
POSES.update({
    "paddle": (-12, 24, 96.6, 120),     # screen-right elbow out, forearm up: the paddle beside her head
    "chest": (-7.5, 132.6, 52, -112),   # screen-left hand flat on her chest; the other hand up and open, startled
    "ask": (-30, 120, 40, -100),        # notebook hand flat, pen hand up by her shoulder
})
BODY_TOP = -300 * H + 78
HY = BODY_TOP - 44


def fringe(k, x, y, lgx=0.0, spark=0.0, seed=0):
    """A gold stud at the lobe (x, y) and three fine chains with a bead each; every chain swings a little differently."""
    c = k.c
    c.save(); c.translate(x, y + 2); c.rotate(-lgx * 0.045)             # a soft shadow on the hair behind the chains
    c.set_source_rgba(0.62, 0.42, 0.10, 0.42); c.rectangle(-9.5, 0, 19, DROP + 8); c.fill()
    c.restore()
    for i, (dx, ln, kf) in enumerate(((-4.6, DROP * 0.74, 0.8), (0.0, DROP, 1.0), (4.6, DROP * 0.86, 1.25))):
        c.save(); c.translate(x + dx, y + 2); c.rotate(-lgx * 0.045 * kf)
        c.set_source_rgb(*INK); c.set_line_width(3.8); c.set_line_cap(0); c.move_to(0, 0); c.line_to(0, ln); c.stroke()
        c.set_source_rgb(*GOLD); c.set_line_width(2.0); c.move_to(0, 0); c.line_to(0, ln); c.stroke()
        ellipse(k, 0, ln + 3, 4.4, 4.8, GOLD, seed + 3 + i, shadow=False, lw=1.6)
        c.set_source_rgba(1, 1, 1, 0.9); c.arc(-1.2, ln + 1.6, 1.3, 0, 2 * math.pi); c.fill()
        c.restore()
    ellipse(k, x, y, 5.6, 5.6, GOLD, seed, shadow=False, lw=1.8)
    props_ss.sparkle(c, x - 5, y + DROP * 0.55, 9 + 7 * spark, spark)


def _blazer(k, body_top, seed):
    c = k.c
    for sx in (-1, 1):
        cut(k, [(sx * 38, body_top - 1), (sx * 15, body_top - 1), (sx * 9, body_top + 46), (sx * 13, body_top + 116),
                (sx * 34, body_top + 114), (sx * 43, body_top + 40)], BLAZER, shadow=False, lw=2.2)
        cut(k, [(sx * 15, body_top - 1), (sx * 30, body_top - 3), (sx * 25, body_top + 30), (sx * 9, body_top + 50)],
            BLAZER, shadow=False, lw=1.8)                               # a sharp lapel
        c.set_source_rgb(*BLAZER_EDGE); c.set_line_width(1.4)
        c.move_to(sx * 16, body_top + 2); c.line_to(sx * 11, body_top + 46); c.stroke()
        c.move_to(sx * 20, body_top + 92); c.line_to(sx * 33, body_top + 92); c.stroke()
    ellipse(k, 12, body_top + 66, 3.6, 3.6, GOLD, seed + 48, shadow=False, lw=1.4)


def _hook(badge):
    def hook(k, body_top, seed):
        _blazer(k, body_top, seed)
        if badge:
            c = k.c
            rect(k, 15, body_top + 34, 26, 16, (1, 1, 1), seed + 40, shadow=False, lw=1.5)
            c.set_source_rgb(*brand.GREEN); c.rectangle(17, body_top + 36, 22, 3); c.fill()
            text(k, "SOFÍA", 28, body_top + 44, 7.2, INK)
    return hook


def _face(inner, blush, special=None):
    def face(k, x, y, kind="neutral", look=(0, 0), seed=0):
        c = k.c
        inner(k, x, y, kind, look, seed)
        my = y + 29
        if special == "flustered":                                      # the round mouth, 18 % smaller
            ellipse(k, x, my, 13, 14, sf.SKIN, seed + 70, shadow=False, outline=False)
            ellipse(k, x, my, 6.6, 8.2, (0.45, 0.06, 0.08), seed + 71, shadow=False, lw=2)
            c.set_source_rgb(*sf.RED); c.set_line_width(3.0); c.save(); c.translate(x, my); c.scale(7.9, 9.5)
            c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.stroke()
        elif special == "sideeye":                                      # narrowed from below, a mouth pulled aside
            for sx in (-17, 17):
                c.save(); c.arc(x + sx, y, 12.6, 0, 2 * math.pi); c.clip()
                c.set_source_rgb(*sf.SKIN); c.rectangle(x + sx - 14, y + 5.5, 28, 9); c.fill()
                c.restore()
                c.set_source_rgb(*INK); c.set_line_width(2.6); c.set_line_cap(1)
                c.move_to(x + sx - 10.5, y + 5.5); c.line_to(x + sx + 10.5, y + 5.5); c.stroke()
            ellipse(k, x, my, 18, 11, sf.SKIN, seed + 72, shadow=False, outline=False)
            c.set_source_rgb(*INK); c.set_line_width(7.6); c.set_line_cap(1)      # a short closed line, pulled to one side
            c.move_to(x - 5, my + 2.5); c.line_to(x + 9, my - 1); c.stroke()
            c.set_source_rgb(*sf.RED); c.set_line_width(5.0)
            c.move_to(x - 5, my + 2.5); c.line_to(x + 9, my - 1); c.stroke()
            c.set_source_rgb(*INK); c.set_line_width(1.8)
            c.move_to(x + 11, my - 4.5); c.line_to(x + 13.5, my - 0.5); c.stroke()   # the corner, tucked in
        elif special == "deadpan":                                      # lids a little down, lips pressed flat
            for sx in (-17, 17):
                c.set_source_rgb(*sf.SKIN); c.rectangle(x + sx - 14.5, y - 12.6, 29, 7.2); c.fill()
                c.set_source_rgb(*INK); c.set_line_width(4.0); c.set_line_cap(1)
                c.move_to(x + sx - 11, y - 5.5); c.line_to(x + sx + 11, y - 5.5); c.stroke()
            ellipse(k, x, my, 19, 11, sf.SKIN, seed + 73, shadow=False, outline=False)
            c.set_source_rgb(*INK); c.set_line_width(8.2); c.set_line_cap(1)
            c.move_to(x - 10, my); c.line_to(x + 10, my); c.stroke()
            c.set_source_rgb(*sf.RED); c.set_line_width(5.6)
            c.move_to(x - 10, my); c.line_to(x + 10, my); c.stroke()
            c.set_source_rgb(*INK); c.set_line_width(1.2)
            c.move_to(x - 9, my); c.line_to(x + 9, my); c.stroke()
        if blush:
            for sx in (-1, 1):
                c.save(); c.translate(x + sx * 31, y + 14); c.scale(10, 6); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
                c.set_source_rgba(*BLUSH, 0.55 * blush); c.fill()
    return face


def sofia(k, x, feet, s=1.0, pose="stand", face_kind="neutral", look=(0, 0), lag=(0, 0), seed=7, badge=True, lean=0.0,
          mouth=None, sparkle=0.0, paddle=None, pen_drop=None, blush=None):
    """Returns {"head", "hands"} in canvas coordinates (lean not applied to the returned points)."""
    kind, special = face_kind, None
    if face_kind == "flustered":
        kind, special, blush = "surprised", "flustered", (1.0 if blush is None else blush)
        if look == (0, 0):
            look = (0.5, -0.2)
    elif face_kind == "sideeye":
        kind, special = "neutral", "sideeye"
        if look == (0, 0):
            look = (1.0, 0.1)
        look = (look[0] * 1.6, look[1])                                  # pupils hard into the corners
    elif face_kind == "deadpan":
        kind, special, look = "eyebrow", "deadpan", (0, 0.35)
    old = (ss.POSES, ss.teardrop, ss.face, ss.BADGE_HOOK, sf.BLOUSE)
    ss.POSES = POSES
    ss.teardrop = fringe
    ss.face = _face(old[2], blush or 0.0, special)
    ss.BADGE_HOOK = _hook(badge)
    sf.BLOUSE = BLAZER                                                  # the sleeves are the blazer's
    try:
        out = ss.sofia(k, x, feet, s, pose, kind, look, lag, seed, True, lean, None, False, mouth, sparkle, None)
    finally:
        ss.POSES, ss.teardrop, ss.face, ss.BADGE_HOOK, sf.BLOUSE = old
    c = k.c
    if paddle:
        hx, hy = out["hands"][1]
        props.paddle(k, hx + 1 * s, hy - 2 * s, 0.9 * s, 0.12, paddle, seed + 90)
        ellipse(k, hx, hy, 10 * s, 10 * s, sf.SKIN, seed + 91, shadow=False, lw=2 * s)
    if pen_drop is not None:                                            # the pen, on its way to the floor
        hx, hy = out["hands"][1]
        px, py = hx + 10 * s, hy + (16 + 46 * pen_drop) * s
        props.pen(k, px, py, 0.9 * s, 0.9 + 2.2 * pen_drop)
        c.set_source_rgb(*INK); c.set_line_width(1.8 * s); c.set_line_cap(1)
        for dx in (-9, 9):
            c.move_to(px + dx * s, py - 16 * s); c.line_to(px + dx * s, py - 28 * s); c.stroke()
    return out
