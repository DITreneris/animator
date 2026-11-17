"""THE ONBOARDING: hands drawn for a purpose (v1). The kit's hand is a ball and its finger a stroke; that failed five
readings (three audits, two cold mute tests): a pinch read as a V-sign, a raised finger as an antenna, an open palm as
a box. These are small cut-out hands with a wrist, a palm and fingers, drawn over (or instead of) the kit's ball.
Each is drawn with its fingers toward -y at the origin given, then rotated by ang and scaled by s.
  pinch(k, x, y, ...)  thumb and index meet at (x, y); the other fingers fold into the palm. For one pearl.
  point(k, x, y, ...)  a closed hand at (x, y), the index finger up. For an interruption.
  palm(k, x, y, ...)   an open hand, palm up, the heel at (x, y) and the fingers toward -y. For asking to be given."""
import math
from kit import INK, cut, ellipse

RED = (0.86, 0.05, 0.12)


def _begin(k, x, y, s, ang):
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    return c


def pinch(k, x, y, s, ang, skin, nail=RED, seed=0):
    c = _begin(k, x, y, s, ang)
    c.translate(0, 22)                                      # the origin is where the two tips meet
    cut(k, [(-5, 9), (5, 9), (5.5, 24), (-5.5, 24)], skin, shadow=False, lw=1.8)                    # the wrist
    for i, (fx, fy) in enumerate(((7.2, 4.5), (8.0, -0.5), (6.6, -5.2))):                           # folded fingers
        ellipse(k, fx, fy, 3.6, 3.2, skin, seed + i, shadow=False, lw=1.5)
    cut(k, [(-7, 10), (7, 10), (8, -2), (4.5, -8), (-4, -8), (-8, -2)], skin, shadow=False, lw=1.8)  # the palm
    cut(k, [(-7.6, -2), (-3, -7.5), (-1.6, -14), (-0.6, -21), (-4.2, -21.6), (-8.6, -12)], skin, shadow=False, lw=1.7)
    cut(k, [(0.4, -7.5), (6.2, -8), (5.6, -16), (3.4, -21.6), (0.4, -21.4), (1.0, -15)], skin, shadow=False, lw=1.7)
    cut(k, [(1.0, -18.2), (4.6, -18.6), (3.6, -21.6), (0.8, -21.4)], nail, shadow=False, lw=1.0)      # one nail shows
    c.restore()


def point(k, x, y, s, ang, skin, nail=None, seed=0, wrist=True):
    c = _begin(k, x, y, s, ang)
    if wrist:
        cut(k, [(-5.5, 7), (5.5, 7), (6, 20), (-6, 20)], skin, shadow=False, lw=1.8)                   # the wrist
    cut(k, [(-1.4, -8), (5.2, -8), (4.8, -27), (2.4, -30.5), (-0.4, -27.5)], skin, shadow=False, lw=1.8)  # the index
    cut(k, [(-9, 8), (9, 8), (9.6, -4), (5.6, -9.5), (-6, -9.5), (-9.6, -3)], skin, shadow=False, lw=1.8)
    c.set_source_rgb(*INK); c.set_line_width(1.4); c.set_line_cap(1)                                   # three knuckles
    for fx in (-4.6, -1.0, 2.6):
        c.move_to(fx, -8.6); c.line_to(fx + 0.4, -3.4); c.stroke()
    ellipse(k, -5.2, 0.5, 5.4, 3.3, skin, seed, shadow=False, lw=1.5)                                  # the thumb, across
    if nail:
        cut(k, [(0.4, -25.5), (4.2, -25.2), (2.6, -29.8)], nail, shadow=False, lw=1.0)
    c.restore()


def palm(k, x, y, s, ang, skin, seed=0):
    c = _begin(k, x, y, s, ang)
    cut(k, [(-7, 4), (-10.5, -6), (-17.5, -13.5), (-14.5, -17), (-6, -11)], skin, shadow=False, lw=1.8)   # the thumb, out
    cut(k, [(-7.5, 6), (7.5, 6), (8.4, -14), (7.4, -30), (4.4, -34), (-3.6, -35), (-6.8, -31), (-7.8, -14)], skin,
        shadow=False, lw=1.9)
    c.set_source_rgb(*INK); c.set_line_width(1.3); c.set_line_cap(1)
    for fx in (-3.4, 0.6, 4.4):                                                                         # between fingers
        c.move_to(fx, -33); c.line_to(fx + 0.2, -19); c.stroke()
    c.restore()


def _fill(c, skin, lw=1.7):
    c.set_source_rgb(*skin); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(lw); c.set_line_join(1); c.set_line_cap(1); c.stroke()


def _finger(c, pts, w, skin, lw=1.7):
    """A bent finger: round-ended segments through pts, outlined as one shape."""
    for col, ww in ((INK, w + 2 * lw), (skin, w)):
        c.set_source_rgb(*col); c.set_line_width(ww); c.set_line_cap(1); c.set_line_join(1)
        c.move_to(*pts[0])
        for q in pts[1:]:
            c.line_to(*q)
        c.stroke()


def _nail(c, tip, back, nail, w=3.2, ln=4.6):
    """A long nail on the back of a fingertip: from the tip toward `back`."""
    d = math.hypot(back[0] - tip[0], back[1] - tip[1])
    ux, uy = (back[0] - tip[0]) / d, (back[1] - tip[1]) / d
    c.save(); c.translate(tip[0] + ux * (ln / 2 - 1.2), tip[1] + uy * (ln / 2 - 1.2)); c.rotate(math.atan2(uy, ux))
    c.scale(ln / 2, w / 2); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
    c.set_source_rgb(*nail); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(0.8); c.stroke()


def hold_pearl(k, x, y, s, ang, skin, nail=RED, seed=0):
    """v2 of the pinch, drawn in curves (the cut-out one still looked like two sticks): the back of a slender hand.
    (x, y) is the CENTRE of the pearl. The index finger comes up and bends in over one side of it; the thumb comes
    from lower on the other side and meets it; each has a long red nail. The other three fingers are curled: soft
    knuckles stepping down the far side. The wrist leaves toward +y. Draw the pearl first: the two fingertips overlap
    its sides, so it is held between them."""
    c = _begin(k, x, y, s, ang)
    c.move_to(-4.8, 36); c.curve_to(-5.2, 29, -8.2, 25, -7.8, 19)                    # the wrist and the back of the hand
    c.curve_to(-7.4, 14.5, -3, 12.5, 2, 12.4); c.curve_to(7, 12.3, 11.6, 13.5, 12.2, 18)
    c.curve_to(12.8, 23, 6.6, 28, 5.6, 36); c.close_path(); _fill(c, skin)
    for kx, ky, r in ((12.0, 24.0, 3.3), (12.9, 19.4, 3.6), (12.2, 14.6, 3.8)):       # three curled fingers
        c.save(); c.translate(kx, ky); c.rotate(-0.35); c.scale(r * 1.25, r)
        c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); _fill(c, skin, 1.5)
    thumb = [(-5.8, 20.0), (-7.4, 11.0), (-4.7, 3.9)]                                # their tips sit under the pearl's sides
    index = [(6.4, 17.0), (8.2, 7.5), (4.5, 2.7)]
    _finger(c, thumb, 5.0, skin)
    _finger(c, index, 4.4, skin)
    _nail(c, thumb[-1], thumb[-2], nail, w=3.2, ln=5.0)
    _nail(c, index[-1], index[-2], nail, w=2.9, ln=5.2)
    c.restore()
