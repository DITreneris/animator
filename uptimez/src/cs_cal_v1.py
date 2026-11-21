"""ONE STAR: the tear-off wall calendar by the door, redrawn (Tomas, 20 Nov: "the FRI calendar looks lame, like a stupid
stick, not a calendar"). Same place and footprint as cs_board.calendar_on (that one stays, for the boards):
a nail and its string, the binding with two rings, a red NOV header, the big red FRI and the date, the stack of
pages under it seen at the edge, a torn stub of yesterday's page at the top.
  calendar2(k, x=296, y=470, s=0.20)   # drawn in the set's coordinates, like calendar_on"""
import math
import cs_props as cp
from kit import INK, rect, ellipse

CAL_AT = (296, 470)          # by the door, where calendar_on put it. Tried (330, 600), to share a close with Don at the
                             # series' face scale: it was then cut in every Don/robot shot. 2.1 pans to him from it instead
PAPER = (0.99, 0.98, 0.95)
EDGE = (0.86, 0.84, 0.78)
RED = cp.RED


def calendar2(k, x=296, y=470, s=0.20, day="20", tear=0.0):
    """tear (0-1): today's page lifting off at its bottom corner (for a later gag); 0 = flat."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s); c.translate(-270, -380)
    c.set_line_cap(1); c.set_line_join(1)
    # the nail and the string
    c.set_source_rgb(*INK); c.set_line_width(5)
    c.move_to(150, 196); c.line_to(270, 120); c.line_to(390, 196); c.stroke()
    ellipse(k, 270, 118, 13, 13, (0.55, 0.55, 0.58), 961, shadow=False, lw=4)
    # the stack of pages, seen at the right and bottom edges
    for i, off in enumerate((18, 12, 6)):
        rect(k, 120 + off, 190 + off, 300, 380, EDGE if i == 0 else PAPER, 962 + i, shadow=(i == 0), lw=5)
    # today's page
    rect(k, 120, 190, 300, 380, PAPER, 965, lw=7)
    c.set_source_rgb(*RED); c.rectangle(124, 194, 292, 96); c.fill()
    cp.T(c, "NOV", 270, 262, 62, col=(1, 1, 1))
    # the binding: a dark bar and two rings through it
    c.set_source_rgb(0.18, 0.18, 0.20); c.rectangle(118, 186, 304, 18); c.fill()
    for rx in (190, 350):
        c.set_source_rgb(0.75, 0.75, 0.78); c.set_line_width(9); c.new_path(); c.arc(rx, 192, 16, math.pi * 1.05, math.pi * 1.95); c.stroke()
        c.set_source_rgb(*INK); c.set_line_width(3); c.new_path(); c.arc(rx, 192, 20, math.pi * 1.05, math.pi * 1.95); c.stroke()
    # the day: big FRI, the date under it
    cp.T(c, "FRI", 270, 410, 128, col=RED)
    cp.T(c, day, 270, 520, 86, col=INK)
    # yesterday's torn stub under the binding
    c.set_source_rgb(*PAPER)
    c.move_to(124, 204)
    for i in range(13):
        c.line_to(124 + i * 24, 214 + (8 if i % 2 else 0))
    c.line_to(416, 204); c.close_path(); c.fill()
    if tear > 0:
        c.set_source_rgb(*EDGE)
        c.move_to(420, 570); c.line_to(420 - 90 * tear, 570); c.line_to(420, 570 - 90 * tear); c.close_path(); c.fill()
    c.restore()
