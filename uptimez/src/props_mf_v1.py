"""Mandatory Fun props shared by the character sheets, storyboard and animation: Don's bright-yellow toy handcuffs
(one cuff ring per wrist, a short chain that sags or goes taut). Sizes are in body units (s = character scale).
Usage: cuff(k, x, y, s, ang); chain(k, x0, y0, x1, y1, s, sag)"""
import math
from kit import INK

TOY_YELLOW = (1.00, 0.84, 0.08)
TOY_YELLOW_DARK = (0.86, 0.62, 0.02)


def cuff(k, x, y, s=1.0, ang=0.0):
    """One toy cuff ring around a wrist at (x, y); drawn over the hand's wrist, open side hidden behind it."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    c.set_source_rgba(0, 0, 0, 0.15); c.rectangle(-11 + 2, -5 + 2, 22, 10); c.fill()
    c.set_source_rgb(*TOY_YELLOW); c.rectangle(-11, -5, 22, 10); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(2.0); c.stroke()
    c.set_source_rgb(*TOY_YELLOW_DARK); c.set_line_width(1.6)               # the moulded ratchet teeth
    for i in range(4):
        c.move_to(-7 + i * 5, -3); c.line_to(-7 + i * 5, 3); c.stroke()
    c.restore()


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
