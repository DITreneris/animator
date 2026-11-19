"""OFFICE NOIR 3: props of the ring, v1.
  plan_hung(k, x, y, s)   the Client's plan as the prize over the ring: a roll hung level on two cords from above,
                          one end let down so the drawing shows: the ten garage bays under one roof, the L-shaped
                          one solid (Office Noir 2's drawing, noir2_cast.bays). (x, y): the middle of the roll.
                          Pale paper and dark lines, so it reads in the lamp; no words on it."""
import math
import noir2_cast as n2
from kit import INK, cut, ellipse

PAPER = (0.96, 0.96, 0.93)
PAPER_SHADE = (0.74, 0.76, 0.80)
LINE = (0.10, 0.12, 0.20)


def plan_hung(k, x, y, s=1.0, seed=0, top=None):
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    yt = -400 if top is None else (top - y) / s
    c.set_source_rgb(0.84, 0.84, 0.86); c.set_line_width(2.4)
    for sx in (-78, 78):                                   # two cords, up out of the lamp's light
        c.new_path(); c.move_to(sx, yt); c.line_to(sx, -10); c.stroke()
    sheet = [(-8, 6), (96, 6), (100, 104), (-4, 100)]      # the end that has come unrolled, hanging
    cut(k, sheet, PAPER, lw=2.2)
    c.set_source_rgb(*LINE)
    old = n2.LOOK[0]
    n2.LOOK[0] = 9
    try:
        n2.bays(c, 8, 42, 13.5, 1.9)
    finally:
        n2.LOOK[0] = old
    cut(k, [(-104, -11), (104, -11), (104, 11), (-104, 11)], PAPER, lw=2.2)   # the roll itself
    c.set_source_rgb(*PAPER_SHADE); c.set_line_width(1.6)
    c.new_path(); c.move_to(-100, 5); c.line_to(100, 5); c.stroke()
    for sx in (-1, 1):
        ellipse(k, sx * 104, 0, 5, 11, PAPER_SHADE, seed + 2 + sx, shadow=False, lw=1.8)
    c.set_source_rgb(*INK); c.set_line_width(4.6)
    for sx in (-78, 78):                                   # the cords' loops round it
        c.new_path(); c.move_to(sx, -12); c.line_to(sx, 12); c.stroke()
    c.restore()
