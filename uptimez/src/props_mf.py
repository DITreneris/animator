"""v2 (props_mf_v1.py = v1, kept): the cuff now reads as a cuff: a wide ring wrapping the wrist (front band plus the
curve of its back edge), a hinge on one end, a keyhole, and a ring loop on the other end where the chain attaches;
open=0..1 swings the jaw open (shot 10: half-closed). cuff() returns the loop point for the chain.
Mandatory Fun props shared by the character sheets, storyboard and animation: Don's bright-yellow toy handcuffs
(one cuff ring per wrist, a short chain that sags or goes taut). Sizes are in body units (s = character scale).
Usage: cuff(k, x, y, s, ang); chain(k, x0, y0, x1, y1, s, sag)"""
import math
from kit import INK

TOY_YELLOW = (1.00, 0.84, 0.08)
TOY_YELLOW_DARK = (0.86, 0.62, 0.02)


def cuff(k, x, y, s=1.0, ang=0.0, open=0.0, loop_side=-1):
    """One toy cuff around a wrist at (x, y). ang = the band's direction (radians, across the wrist).
    loop_side: which end (-1 / +1 along the band) carries the chain loop. Returns the loop centre."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    c.set_line_join(1); c.set_line_cap(1)
    # the back of the ring, seen past the wrist: a thin arc below the band
    c.set_source_rgb(*TOY_YELLOW_DARK); c.set_line_width(4)
    c.save(); c.scale(1, 0.55); c.arc(0, 6, 13, 0.1 * math.pi, 0.9 * math.pi); c.restore(); c.stroke()
    # the front band (if open, the jaw half swings away from the hinge)
    def band(x0, x1):
        c.move_to(x0, -6); c.line_to(x1, -6); c.curve_to(x1 + 4, -6, x1 + 4, 6, x1, 6); c.line_to(x0, 6)
        c.curve_to(x0 - 4, 6, x0 - 4, -6, x0, -6); c.close_path()
        c.set_source_rgba(0, 0, 0, 0.15); c.fill_preserve()
        c.set_source_rgb(*TOY_YELLOW); c.fill_preserve()
        c.set_source_rgb(*INK); c.set_line_width(2.2); c.stroke()
    hs = -loop_side                                   # the hinge sits opposite the loop
    if open > 0:
        band(min(0, hs * 14), max(0, hs * 14))
        c.save(); c.translate(0, 0); c.rotate(-hs * open * 1.0)
        band(min(0, -hs * 14), max(0, -hs * 14))
        c.restore()
    else:
        band(-14, 14)
    c.set_source_rgb(*TOY_YELLOW_DARK); c.set_line_width(1.6)               # ratchet teeth
    for i in range(3):
        xx = loop_side * (4 + i * 3.5)
        c.move_to(xx, -3.5); c.line_to(xx, 3.5); c.stroke()
    ellipse_ = lambda cx, cy, r, col: (c.arc(cx, cy, r, 0, 2 * math.pi), c.set_source_rgb(*col), c.fill_preserve(),
                                       c.set_source_rgb(*INK), c.set_line_width(1.8), c.stroke())
    ellipse_(hs * 15, 0, 3.6, TOY_YELLOW_DARK)                               # hinge
    c.set_source_rgb(*INK); c.arc(-loop_side * 4, -0.8, 1.8, 0, 2 * math.pi); c.fill()   # keyhole
    c.rectangle(-loop_side * 4 - 0.8, -0.8, 1.6, 3.6); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(5.2)                            # the chain loop
    c.arc(loop_side * 22, 0, 5, 0, 2 * math.pi); c.stroke()
    c.set_source_rgb(*TOY_YELLOW); c.set_line_width(2.8)
    c.arc(loop_side * 22, 0, 5, 0, 2 * math.pi); c.stroke()
    lx, ly = c.user_to_device(loop_side * 26, 0)
    c.restore()
    return c.device_to_user(lx, ly)


def click(k, x, y, s=1.0):
    """Three short ticks: the click."""
    c = k.c
    c.set_source_rgb(*INK); c.set_line_width(2.0 * s); c.set_line_cap(1)
    for a in (-0.9, -0.3, 0.3):
        c.move_to(x + 9 * s * math.sin(a), y - 9 * s * math.cos(a))
        c.line_to(x + 16 * s * math.sin(a), y - 16 * s * math.cos(a)); c.stroke()


def chain(k, x0, y0, x1, y1, s=1.0, sag=0.25, links=None):
    """Big plastic links from (x0, y0) to (x1, y1); sag = how far the middle droops as a share of the span
    (0 = taut and straight)."""
    c = k.c
    d = math.hypot(x1 - x0, y1 - y0)
    n = links or max(3, int(d / (11 * s)))
    pts = []
    for i in range(n + 1):
        t = i / n
        pts.append((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t + 4 * sag * d * t * (1 - t)))
    for i in range(n):
        (ax, ay), (bx, by) = pts[i], pts[i + 1]
        mx, my = (ax + bx) / 2, (ay + by) / 2
        a = math.atan2(by - ay, bx - ax)
        L = math.hypot(bx - ax, by - ay) * 0.62 + 2 * s
        c.save(); c.translate(mx, my); c.rotate(a)
        c.scale(L, (4.2 if i % 2 == 0 else 2.6) * s)
        c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        c.set_source_rgb(*TOY_YELLOW); c.fill_preserve()
        c.set_source_rgb(*INK); c.set_line_width(1.6 * s); c.stroke()
