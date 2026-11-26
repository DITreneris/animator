"""ONE HAND for "Pick a Side" (episode 14) and on: one anatomy, six shapes. Tomas, 23 Nov ("Improve", after the hands
audit): the repo had six hand drawers, one per episode (a ball, sticks on balls, boxes, a claw); none had a thumbs-up or a
salute that read. This is one hand built like of_cast.cartoon_hand (episode 13's, chunky, a bold outline) with the same
palm, finger thickness, wrist and outline in every shape:
  fist    the knuckles forward, the thumb lying across them
  point   the fist, the index out along the forearm
  palm    open: four fingers together and a thumb out
  thumb   thumbs-up: the fist upright, side on, knuckles to the outside, the thumb up from its top (screen-aligned)
  salute  the flat hand, fingers together, tilted from the wrist to the temple
  relax   a loose fist hanging, the thumb along its side
  cup     a fist round a held mug (drawn again over it); two: the same, two fingers lifted off it (Pam's half salute)
  v2 (Pam & Mom audit, 23 Nov), new shapes only (the ones above draw exactly as before):
  two_s   two, the fingers 25 % smaller · relax_s  relax, the thumb pressed in · grab  an open C, the thumb apart (to
  pick something up) · tuck  nothing: the hand hidden under the other forearm (folded arms)
  v3 (One Star hand audit 2, 23 Nov), new shape only: quiet  a hand at rest: one mitten outline, the thumb's edge along
  its side, two short finger lines (relax read as a fist, "toes")
  v4 (Daddy's Home v8 review, 24 Nov), new shape only: point_s  point with the index 20 % shorter and the thumb out
  (the pinned v3 is hands_ps_v3.py)
Opt-in: kit.HAND[0] = hands_ps.hand, and GEST[0] = ("left shape", "right shape"); arms are drawn screen-left first.
Nothing else changes: with kit.HAND[0] unset every earlier sheet draws as before.
  python3 hands_ps.py [out]  ->  before/after sheet on Don at character scale"""
import math
import kit
from kit import INK

GEST = [("relax", "relax")]
_N = [0]
LATE = []                                                   # hands drawn again on top (redraw_late): over the head, round a mug
ON_TOP = ("salute", "cup", "two", "two_s")
DIRS = []                                                   # (d, arm) per hand drawn since reset(): to place a held prop
LW = 2.0


PINCH_V4 = [False]                                                   # opt-in: the clamp (the nose its own, between the fingers)
PINCH_V3 = [False]                                                   # opt-in: the C-shaped pinch (review 26 Nov)
PINCH_V2 = [False]                                                   # opt-in: the simpler pinch (index and thumb straight)

def reset(left="relax", right="relax"):
    GEST[0] = (left, right); _N[0] = 0; LATE.clear(); DIRS.clear()


def redraw_late(k):
    """The salute's fingertips touch his temple, so it is drawn again after the head."""
    c = k.c
    for m, args in LATE:
        c.save(); c.set_matrix(m); draw(k, *args); c.restore()
    LATE.clear()


def _cap(c, pts, t, skin):
    """A finger: a fat rounded stroke, outlined."""
    for col, w in ((INK, t + 2 * LW), (skin, t)):
        c.set_source_rgb(*col); c.set_line_width(w); c.set_line_cap(1); c.set_line_join(1)
        c.new_path(); c.move_to(*pts[0])
        for p in pts[1:]:
            c.line_to(*p)
        c.stroke()
    c.set_line_cap(0); c.set_line_join(0)


def _blob(c, x, y, rx, ry, skin, rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(rx, ry); c.new_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
    c.set_source_rgb(*skin); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(LW); c.stroke()


def _crease(c, pts, lw=1.4):
    c.set_source_rgb(*INK); c.set_line_width(lw); c.set_line_cap(1); c.new_path(); c.move_to(*pts[0])
    for p in pts[1:]:
        c.line_to(*p)
    c.stroke(); c.set_line_cap(0)


def _wrist(c, w, skin):
    _cap(c, [(-0.55 * w, 0), (0.05 * w, 0)], 0.60 * w, skin)


def hand(k, hx, hy, w, skin, seed, d, side):
    """kit.HAND hook. The forearm runs along d into (hx, hy); arms arrive screen-left first."""
    g = GEST[0][_N[0] % 2]; arm = -1 if _N[0] % 2 == 0 else 1; _N[0] += 1
    DIRS.append((d, arm))
    draw(k, g, hx, hy, w * 1.25, skin, d, arm)
    if g in ON_TOP:
        LATE.append((k.c.get_matrix(), (g, hx, hy, w * 1.25, skin, d, arm)))


GLOVE = [None]                                              # v5 (25 Nov, Office Noir 2 v34, the hand sheet's review: "rubber robot gloves"), opt-in:
#   {"shade": (r, g, b), "shine": bool}. The same anchor, shapes and thumb side, drawn as a lady's glove: one silhouette (no
#   line across the wrist), fingers about 12 % longer and thinner, tapered, of four lengths, creases where it bends.
#   Unset, every shape draws exactly as before.
GLOVE_SHAPES = ("quiet", "point", "point_s", "grab", "fist", "palm", "relax", "beckon")


def _glove(k, g, hx, hy, w, skin, d, arm):
    c = k.c
    cfg = GLOVE[0]
    a = math.atan2(d[1], d[0])
    s_ = -1 if (arm < 0) == (math.cos(a) >= 0) else 1                 # the thumb's side, as in draw()
    T0, T1 = 0.235 * w, 0.165 * w                                     # a finger at its root and at its tip
    parts = [("cap", [(-0.60, 0.0), (0.18, 0.0)], 0.60 * w, 0.60 * w),            # the wrist, as wide as the forearm it ends
             ("blob", (0.30, 0.0), 0.40, 0.37)]                                   # the palm
    lines = []                                                        # creases, in the shade colour
    Y = (-0.27, -0.09, 0.09, 0.27)                                    # index (thumb side) .. little finger, across the hand
    fy = lambda i: s_ * (-Y[i])                                       # index nearest the thumb

    def finger(i, pts, k0=1.0, k1=1.0):
        parts.append(("cap", pts, T0 * k0, T1 * k1))
    if g == "palm":
        for i, ln in enumerate((0.66, 0.76, 0.70, 0.52)):
            y = fy(i); fan = y * 0.22
            finger(i, [(0.52, y), (0.52 + ln * 0.55, y + fan * 0.6), (0.52 + ln, y + fan)], 1.0 if i < 3 else 0.9, 1.0 if i < 3 else 0.9)
        parts.insert(0, ("cap", [(0.16, s_ * 0.28), (0.44, s_ * 0.58), (0.62, s_ * 0.70)], T0 * 1.05, T1 * 1.1))
        lines += [[(0.40, s_ * 0.16), (0.52, s_ * 0.02), (0.50, -s_ * 0.20)]]
    elif g == "grab":                                                 # an open hand closing: fingers curved in, the thumb apart
        for i, ln in enumerate((0.58, 0.66, 0.60, 0.46)):
            y = fy(i)
            finger(i, [(0.52, y), (0.52 + ln * 0.62, y + s_ * 0.03), (0.52 + ln * 0.95, y + s_ * 0.24)], 1.0 if i < 3 else 0.9, 1.0 if i < 3 else 0.9)
        parts.insert(0, ("cap", [(0.16, s_ * 0.28), (0.50, s_ * 0.60), (0.86, s_ * 0.58)], T0 * 1.05, T1 * 1.1))
    elif g in ("quiet", "relax"):                                     # at rest: the fingers together, gently curved, the thumb lying along them
        for i, ln in enumerate((0.50, 0.58, 0.54, 0.42)):
            y = fy(i) * 0.80
            finger(i, [(0.50, y), (0.50 + ln * 0.6, y + s_ * 0.02), (0.50 + ln, y + s_ * 0.12)], 1.0, 1.0)
        parts.insert(0, ("cap", [(0.14, s_ * 0.26), (0.46, s_ * 0.40), (0.72, s_ * 0.38)], T0, T1 * 1.05))
    else:                                                             # fist, point: the fingers folded into the palm
        parts.append(("blob", (0.62, -s_ * 0.02), 0.20, 0.36))
        for i in ((1, 2, 3) if (g.startswith("point") or g == "beckon") else (0, 1, 2, 3)):
            parts.append(("blob", (0.76, fy(i) * 0.92), 0.105, 0.10))               # a knuckle each, small
        if g == "beckon":                                   # v6 (glove mode only): the index up and curling back toward the palm
            finger(0, [(0.56, fy(0)), (0.98, fy(0) - s_ * 0.04), (1.18, fy(0) + s_ * 0.16), (1.10, fy(0) + s_ * 0.34)], 1.0, 0.9)
            parts.append(("cap", [(0.20, s_ * 0.30), (0.52, s_ * 0.36), (0.70, s_ * 0.20)], T0 * 0.95, T1))
        elif g.startswith("point"):
            ln = 0.84 if g == "point" else 0.70                        # the index: out, a little bent at its middle joint
            finger(0, [(0.56, fy(0)), (0.56 + ln * 0.5, fy(0) - s_ * 0.045), (0.56 + ln, fy(0) + s_ * 0.02)], 1.0, 0.95)
            parts.append(("cap", [(0.20, s_ * 0.30), (0.52, s_ * 0.36), (0.70, s_ * 0.20)], T0 * 0.95, T1))   # the thumb folded over the others
        else:
            parts.append(("cap", [(0.22, s_ * 0.34), (0.56, s_ * 0.34), (0.78, s_ * 0.14)], T0, T1 * 1.05))   # the thumb across them
        lines += [[(0.60, -s_ * 0.30), (0.66, -s_ * 0.02), (0.60, s_ * 0.22)]]
    lines += [[(-0.16, -0.22), (-0.10, 0.0), (-0.16, 0.22)], [(-0.02, -0.20), (0.03, 0.0), (-0.02, 0.20)]]   # the glove's folds at the wrist

    def lay(grow, col):
        c.set_source_rgb(*col); c.set_line_cap(1); c.set_line_join(1)
        for p in parts:
            if p[0] == "blob":
                (bx, by), rx, ry = p[1], p[2], p[3]
                c.save(); c.translate(bx * w, by * w); c.scale(rx * w + grow, ry * w + grow); c.new_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
            else:
                pts, t0, t1 = p[1], p[2], p[3]
                n_ = len(pts) - 1
                for j in range(n_):                                   # tapered: each piece a little thinner than the one before
                    tt = t0 + (t1 - t0) * (j + 0.5) / n_
                    c.set_line_width(tt + 2 * grow); c.new_path(); c.move_to(pts[j][0] * w, pts[j][1] * w); c.line_to(pts[j + 1][0] * w, pts[j + 1][1] * w); c.stroke()
    c.save(); c.translate(hx, hy); c.rotate(a)
    lay(LW, INK)                                                      # one outline round all of it,
    c.set_source_rgb(*skin); c.set_line_cap(0); c.set_line_width(0.60 * w); c.new_path(); c.move_to(-0.95 * w, 0); c.line_to(-0.3 * w, 0); c.stroke()   # open toward the forearm
    lay(0.0, skin)                                                    # then the glove itself: no lines inside it but the ones below
    c.set_line_cap(1)
    if g in ("palm", "grab", "quiet", "relax"):                       # where one finger lies against the next
        for p in parts:
            if p[0] == "cap" and len(p[1]) == 3 and p[1][0][0] >= 0.5:
                pts = p[1]; off = p[2] * 0.5
                c.set_source_rgb(*INK); c.set_line_width(1.1)
                c.new_path(); c.move_to(pts[0][0] * w + 0.06 * w, pts[0][1] * w + s_ * off * 0.0 + off * (1 if pts[0][1] * 1 > -9 else 1)); c.line_to(pts[1][0] * w, pts[1][1] * w + off)
                c.stroke()
    shade = cfg.get("shade") if cfg else None
    if shade:
        c.set_source_rgb(*shade); c.set_line_width(max(1.2, 0.035 * w))
        for ln_ in lines:
            c.new_path(); c.move_to(ln_[0][0] * w, ln_[0][1] * w); c.curve_to(ln_[1][0] * w, ln_[1][1] * w, ln_[1][0] * w, ln_[1][1] * w, ln_[2][0] * w, ln_[2][1] * w); c.stroke()
        c.set_line_width(max(2.0, 0.07 * w))                          # the palm's shaded side, away from the thumb
        c.new_path(); c.move_to(0.02 * w, -s_ * 0.27 * w); c.curve_to(0.20 * w, -s_ * 0.33 * w, 0.40 * w, -s_ * 0.33 * w, 0.52 * w, -s_ * 0.29 * w); c.stroke()
    if cfg and cfg.get("shine"):                                      # satin: one thin white line along the back of the hand
        c.set_source_rgb(1, 1, 1); c.set_line_width(max(1.0, 0.028 * w))
        c.new_path(); c.move_to(0.16 * w, s_ * 0.10 * w); c.curve_to(0.26 * w, s_ * 0.14 * w, 0.38 * w, s_ * 0.13 * w, 0.46 * w, s_ * 0.08 * w); c.stroke()
    c.set_line_cap(0); c.set_line_join(0)
    c.restore()


def draw(k, g, hx, hy, w, skin, d, arm):
    """arm: -1 his left arm as we see it (screen-left), 1 screen-right. w: the hand's width."""
    if GLOVE[0] is not None and g in GLOVE_SHAPES:
        return _glove(k, g, hx, hy, w, skin, d, arm)
    c = k.c
    a = math.atan2(d[1], d[0])
    t = 0.30 * w                                                      # one finger thickness for every shape
    c.save(); c.translate(hx, hy)
    if g == "two_s":                                                  # screen-aligned: the fist on the mug's rim, two fingers
        c.translate(d[0] * 0.25 * w, d[1] * 0.25 * w); c.scale(-arm, 1)       # up and leaning in toward her brow
        _cap(c, [(0, 0.55 * w), (0, 0.15 * w)], 0.60 * w, skin)
        for i, fx in enumerate((0.02, 0.24)):
            _cap(c, [(fx * w, -0.20 * w), (fx * w + 0.30 * w, -0.86 * w + i * 0.06 * w)], t * 0.75, skin)
        _blob(c, 0.02 * w, 0.02 * w, 0.44 * w, 0.40 * w, skin)
        for yy in (-0.10, 0.12):
            _crease(c, [(-0.20 * w, yy * w), (0.20 * w, yy * w)])
        _cap(c, [(-0.40 * w, -0.06 * w), (-0.30 * w, 0.24 * w)], t * 0.85, skin)        # the thumb on the far side
        c.restore(); return
    if g == "thumb":                                                  # screen-aligned: the fist upright, side on
        c.translate(d[0] * 0.25 * w, d[1] * 0.25 * w); c.scale(-arm, 1)       # the thumb toward the body's outside
        _cap(c, [(0, 0.55 * w), (0, 0.15 * w)], 0.60 * w, skin)       # the wrist under it
        c.new_path()                                                  # the fist: a rounded block, knuckles outward (+x)
        r = 0.22 * w
        x0, x1, y0, y1 = -0.42 * w, 0.46 * w, -0.40 * w, 0.40 * w
        c.move_to(x0 + r, y0); c.line_to(x1 - r, y0); c.arc(x1 - r, y0 + r, r, -math.pi / 2, 0); c.line_to(x1, y1 - r)
        c.arc(x1 - r, y1 - r, r, 0, math.pi / 2); c.line_to(x0 + r, y1); c.arc(x0 + r, y1 - r, r, math.pi / 2, math.pi)
        c.line_to(x0, y0 + r); c.arc(x0 + r, y0 + r, r, math.pi, 1.5 * math.pi); c.close_path()
        c.set_source_rgb(*skin); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(LW); c.stroke()
        for yy in (-0.13, 0.13):                                      # the curled fingers, two creases
            _crease(c, [(0.10 * w, yy * w), (x1 - 0.02 * w, yy * w)])
        _cap(c, [(-0.22 * w, -0.30 * w), (-0.20 * w, -0.88 * w)], 0.34 * w, skin)    # the thumb, up from the top corner
        c.set_source_rgb(*skin); c.new_path(); c.rectangle(-0.37 * w, -0.40 * w, 0.32 * w, 0.14 * w); c.fill()  # its root, merged
        _crease(c, [(-0.37 * w, -0.40 * w), (-0.37 * w, -0.30 * w)], LW)
        _crease(c, [(-0.05 * w, -0.40 * w), (-0.05 * w, -0.30 * w)], LW)
        c.restore(); return
    c.rotate(a)                                                       # the rest: along the forearm (+x forward)
    s_ = -1 if (arm < 0) == (math.cos(a) >= 0) else 1                 # the thumb's side, mirrored per arm
    if g == "salute":
        c.rotate(-arm * 0.0)
        _wrist(c, w, skin)
        c.rotate(0.35 * s_)                                           # bent at the wrist toward the temple
        _cap(c, [(0.05 * w, 0), (0.95 * w, 0)], 0.62 * w, skin)       # the flat hand, fingers together
        _crease(c, [(0.45 * w, -0.08 * w), (1.15 * w, -0.08 * w)]); _crease(c, [(0.45 * w, 0.10 * w), (1.15 * w, 0.10 * w)])
        _cap(c, [(0.05 * w, s_ * 0.22 * w), (0.40 * w, s_ * 0.30 * w)], t, skin)     # the thumb tucked along it
        c.restore(); return
    if g == "tuck":
        c.restore(); return
    _wrist(c, w, skin)
    if g == "grab":                                                   # an open C: the thumb apart from four curled fingers
        _blob(c, 0.20 * w, 0, 0.42 * w, 0.40 * w, skin)
        _cap(c, [(0.15 * w, s_ * 0.32 * w), (0.55 * w, s_ * 0.52 * w), (0.78 * w, s_ * 0.40 * w)], t, skin)
        for fy in (-0.26, -0.09, 0.08):
            _cap(c, [(0.42 * w, -s_ * fy * w), (0.86 * w, -s_ * fy * w), (1.02 * w, -s_ * (fy - 0.16) * w)], t * 0.9, skin)
        c.restore(); return
    if g == "palm":
        _cap(c, [(0.10 * w, s_ * 0.30 * w), (0.42 * w, s_ * 0.62 * w)], t, skin)     # the thumb out
        _blob(c, 0.20 * w, 0, 0.42 * w, 0.40 * w, skin)
        for fy in (-0.24, -0.08, 0.08, 0.24):
            _cap(c, [(0.40 * w, fy * w), (1.02 * w - abs(fy) * 0.5 * w, fy * w * 1.15)], t * 0.9, skin)
        c.restore(); return
    if g == "quiet":                                                  # v3 (One Star audit 2, 23 Nov): a hand at rest. One
        _cap(c, [(0.12 * w, s_ * 0.26 * w), (0.56 * w, s_ * 0.34 * w)], t * 0.95, skin)   # outline; the thumb first, so the
        c.save(); c.translate(0.40 * w, 0); c.scale(0.56 * w, 0.40 * w)                   # mitten covers its root and only
        c.new_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()                          # its outer edge shows along the side
        c.set_source_rgb(*skin); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(LW); c.stroke()
        for fy in (-0.12, 0.10):                                      # two short finger lines at the tips
            _crease(c, [(0.68 * w, -s_ * fy * w), (0.90 * w, -s_ * fy * w)], 1.3)
        c.restore(); return
    if g == "pinch" and PINCH_V4[0]:                                  # v10 (review 26 Nov): a clamp. The index straight up one side
        _blob(c, 0.18 * w, 0, 0.40 * w, 0.40 * w, skin)               # of the (narrowed) nose, the thumb up the other, the nose its
        c.new_path(); c.save(); c.translate(0.38 * w, 0); c.scale(0.20 * w, 0.17 * w)   # own, seen between them; the three
        c.arc(0, 0, 1, -math.pi / 2, math.pi / 2); c.line_to(-0.8, 1); c.line_to(-0.8, -1); c.close_path(); c.restore()   # curled: one
        c.set_source_rgb(*skin); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(LW); c.stroke()              # block,
        _crease(c, [(0.38 * w, 0), (0.54 * w, 0)], 1.0)                                                                  # one line
        _cap(c, [(0.36 * w, -s_ * 0.36 * w), (0.74 * w, -s_ * 0.36 * w), (0.98 * w, -s_ * 0.30 * w)], t * 0.68, skin)   # index
        _cap(c, [(0.10 * w, s_ * 0.38 * w), (0.66 * w, s_ * 0.38 * w), (0.90 * w, s_ * 0.32 * w)], t * 0.82, skin)      # thumb
        c.restore(); return
    if g == "pinch" and PINCH_V3[0]:                                  # v9 (review 26 Nov): a C: the index round one side of the
        pass                                                          # nose, the thumb (a pad) round the other, a gap between the
        c.set_source_rgba(0.45, 0.22, 0.14, 0.28)                     # tips; the three curled into one block, two lines. A contact
        c.save(); c.translate(0.80 * w, 0.02 * w); c.scale(0.52 * w, 0.50 * w); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
        _blob(c, 0.20 * w, 0, 0.42 * w, 0.40 * w, skin)               # shadow on the face under them
        c.new_path(); c.save(); c.translate(0.36 * w, s_ * 0.03 * w); c.scale(0.17 * w, 0.21 * w)   # the curled three
        c.arc(0, 0, 1, -math.pi / 2, math.pi / 2); c.line_to(-0.7, 1); c.line_to(-0.7, -1); c.close_path(); c.restore()
        c.set_source_rgb(*skin); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(LW); c.stroke()
        for yy in (-0.06, 0.09):
            _crease(c, [(0.34 * w, s_ * yy * w), (0.50 * w, s_ * yy * w)], 1.0)
        _cap(c, [(0.40 * w, -s_ * 0.27 * w), (0.76 * w, -s_ * 0.34 * w), (0.96 * w, -s_ * 0.24 * w)], t * 0.80, skin)   # index
        _cap(c, [(0.12 * w, s_ * 0.34 * w), (0.56 * w, s_ * 0.40 * w)], t * 0.95, skin)                                 # thumb
        _blob(c, 0.80 * w, s_ * 0.30 * w, 0.20 * w, 0.14 * w, skin, s_ * -0.7)                                           # its pad
        nose = (min(1.0, skin[0] + 0.03), skin[1] * 0.80, skin[2] * 0.80)                    # the nose's tip between them, squeezed
        _blob(c, 0.98 * w, s_ * 0.04 * w, 0.21 * w, 0.17 * w, nose)                          # red, drawn over their tips
        c.restore(); return
    if g == "pinch" and PINCH_V2[0]:                                  # v7 (review 26 Nov: "too many fingers at the nose"): the palm
        _blob(c, 0.22 * w, 0.06 * s_ * w, 0.46 * w, 0.44 * w, skin)    # with the three curled into it (one shape, one crease), the
        _crease(c, [(0.30 * w, s_ * 0.08 * w), (0.58 * w, s_ * 0.12 * w)])   # index and thumb straight, their tips together
        _cap(c, [(0.50 * w, -s_ * 0.20 * w), (1.08 * w, -s_ * 0.10 * w)], t, skin)
        _cap(c, [(0.36 * w, s_ * 0.36 * w), (1.02 * w, s_ * 0.10 * w)], t * 1.05, skin)
        c.restore(); return
    if g == "pinch":                                                  # v6 (Pick a Side 4.3b, Tomas 26 Nov, a new shape): the
        _blob(c, 0.22 * w, 0, 0.44 * w, 0.42 * w, skin)               # thumb and the index meet at the tips (a nose between),
        for fy in (0.02, 0.24):                                       # the other three curled back into the palm
            _blob(c, 0.56 * w, s_ * fy * w, 0.16 * w, 0.15 * w, skin)
        _cap(c, [(0.46 * w, -s_ * 0.22 * w), (0.92 * w, -s_ * 0.24 * w), (1.10 * w, -s_ * 0.08 * w)], t, skin)   # the index,
        _cap(c, [(0.18 * w, s_ * 0.38 * w), (0.74 * w, s_ * 0.40 * w), (1.04 * w, s_ * 0.14 * w)], t * 1.05, skin)  # the thumb
        c.restore(); return
    _blob(c, 0.22 * w, 0, 0.46 * w, 0.44 * w, skin)                   # fist, point, relax: the palm
    for fy in (-0.27, 0.0, 0.27):                                     # three curled knuckles
        _blob(c, 0.60 * w, fy * w, 0.18 * w, 0.17 * w, skin)
    if g == "two":                                                    # two fingers up off a held cup (Pam's half salute)
        for fy in (-0.22, 0.02):
            _cap(c, [(0.50 * w, -s_ * fy * w - s_ * 0.0), (1.20 * w, -s_ * fy * w)], t, skin)
    if g == "point":
        _cap(c, [(0.50 * w, -s_ * 0.20 * w), (1.35 * w, -s_ * 0.20 * w)], t, skin)  # the index, out
    if g == "point_t":                                                # v5 (Daddy's Home v8 review 2, 24 Nov, opt-in): the index
        _cap(c, [(0.50 * w, -s_ * 0.20 * w), (1.35 * w, -s_ * 0.20 * w)], t, skin)  # out, no thumb
        c.restore(); return                                           # (big, "point"'s thumb across the knuckles read as a
                                                                      # second, bent finger; pressed along the side, too): the
                                                                      # thumb is behind the hand, seen from its back
    if g == "point_s":                                                # v4 (Daddy's Home v8 review, 24 Nov): the index 20 %
        _cap(c, [(0.50 * w, -s_ * 0.20 * w), (1.18 * w, -s_ * 0.20 * w)], t, skin)  # shorter, the thumb standing clear
        _cap(c, [(0.12 * w, s_ * 0.30 * w), (0.40 * w, s_ * 0.58 * w)], t, skin)
        c.restore(); return
    if g == "relax":
        _cap(c, [(0.05 * w, s_ * 0.36 * w), (0.40 * w, s_ * 0.42 * w)], t, skin)    # the thumb along the side
    elif g == "relax_s":
        _cap(c, [(0.12 * w, s_ * 0.24 * w), (0.40 * w, s_ * 0.28 * w)], t * 0.85, skin)  # the thumb pressed in
    else:
        _cap(c, [(0.20 * w, s_ * 0.38 * w), (0.58 * w, s_ * 0.05 * w)], t, skin)    # the thumb across the knuckles
    c.restore()


def sheet(out):
    import cairo
    import of_cast as oc
    import don_ps as dp
    W, H = 2200, 1350
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W * 2, H * 2); surf.set_device_scale(2, 2)
    c = cairo.Context(surf); k = kit.Ctx(c, 0)
    c.set_source_rgb(*kit.WALL); c.paint()

    def lab(t_, x, y, sz=16, b=1):
        c.select_font_face("Inter", 0, b); c.set_font_size(sz); c.set_source_rgb(*INK)
        e = c.text_extents(t_); c.move_to(x - e.x_advance / 2, y); c.show_text(t_)
    lab("ONE HAND · hands_ps v1 · six shapes, one anatomy · before / after on Don at sheet scale", W / 2, 44, 26)
    skin = (0.96, 0.80, 0.68)
    for i, g in enumerate(("fist", "point", "palm", "thumb", "salute", "relax")):
        x = 190 + i * 360
        for j, (arm, d) in enumerate(((-1, (0.0, 1.0)), (1, (0.0, 1.0)))):
            dd = {"point": (1.0, 0.0), "palm": (0.0, -1.0), "salute": (0.4, -0.9), "fist": (0.0, -1.0)}.get(g, d)
            if arm < 0 and g in ("point", "salute"):
                dd = (-dd[0], dd[1])
            draw(k, g, x - 70 + j * 140, 200, 46, skin, dd, arm)
        lab(g, x, 300, 18); lab("screen-left · screen-right arm", x, 322, 12, 0)
    F = 760; S = 0.9
    rows = (("BEFORE: kit ball (Don v1)", None), ("BEFORE: cartoon_hand (ep 13)", "cartoon"), ("AFTER: hands_ps", "new"))
    poses = (("thumbs", ("thumb", "thumb"), "3.1 thumbs-up"), ("salute", ("relax", "salute"), "2.5 salute"),
             ("point_roll", ("relax", "point"), "2.3 point"), ("vest", ("fist", "fist"), "6.1 vest"),
             ("push", ("palm", "palm"), "2.11 palms"))
    for r, (name, mode) in enumerate(rows):
        for i, (p, gs, n) in enumerate(poses):
            x = 120 + r * 720 + i * 128
            if mode == "new":
                dp.don(k, x, F + r * 0, S * 0.8, p, "pleased", (0, 0), hands=gs)
            else:
                kit.HAND[0] = oc.cartoon_hand if mode == "cartoon" else None
                try:
                    dp.don(k, x, F, S * 0.8, p, "pleased", (0, 0), hands=False)
                finally:
                    kit.HAND[0] = None
            if r == 0:
                pass
            lab(n, x, F + 40, 12, 0)
        lab(name, 120 + r * 720 + 256, F + 74, 17)
    surf.write_to_png(out); print("wrote", out)


if __name__ == "__main__":
    import sys
    sheet(sys.argv[1] if len(sys.argv) > 1 else "../pick-a-side/ps_hands_v1.png")
