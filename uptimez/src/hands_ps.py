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


def draw(k, g, hx, hy, w, skin, d, arm):
    """arm: -1 his left arm as we see it (screen-left), 1 screen-right. w: the hand's width."""
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
    _blob(c, 0.22 * w, 0, 0.46 * w, 0.44 * w, skin)                   # fist, point, relax: the palm
    for fy in (-0.27, 0.0, 0.27):                                     # three curled knuckles
        _blob(c, 0.60 * w, fy * w, 0.18 * w, 0.17 * w, skin)
    if g == "two":                                                    # two fingers up off a held cup (Pam's half salute)
        for fy in (-0.22, 0.02):
            _cap(c, [(0.50 * w, -s_ * fy * w - s_ * 0.0), (1.20 * w, -s_ * fy * w)], t, skin)
    if g == "point":
        _cap(c, [(0.50 * w, -s_ * 0.20 * w), (1.35 * w, -s_ * 0.20 * w)], t, skin)  # the index, out
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
