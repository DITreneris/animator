"""A clown emoji drawn in the series' cut-paper style (not an emoji font): white face, red nose, blue tufts, red grin.
Used after "Stupid human." in the company's reply (Tomas, 23 Nov)."""
import math

INK = (0.13, 0.11, 0.12)


def clown(c, cx, cy, r, lw=None):
    lw = lw or max(1.2, r * 0.09)
    c.save()
    c.set_line_join(1)
    for sd in (-1, 1):                                               # blue tufts of hair either side
        for j, (dx, dy, rr) in enumerate(((0.95, -0.35, 0.42), (1.05, 0.15, 0.38), (0.75, -0.75, 0.34))):
            c.new_path(); c.arc(cx + sd * dx * r, cy + dy * r, rr * r, 0, 2 * math.pi)
            c.set_source_rgb(0.24, 0.52, 0.92); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(lw); c.stroke()
    c.new_path(); c.arc(cx, cy, r, 0, 2 * math.pi)                    # the face
    c.set_source_rgb(0.99, 0.97, 0.95); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(lw); c.stroke()
    for sd in (-1, 1):                                               # eyes with blue diamonds
        ex, ey = cx + sd * 0.36 * r, cy - 0.22 * r
        c.new_path(); c.move_to(ex, ey - 0.3 * r); c.line_to(ex + 0.17 * r, ey); c.line_to(ex, ey + 0.3 * r); c.line_to(ex - 0.17 * r, ey)
        c.close_path(); c.set_source_rgb(0.40, 0.70, 0.98); c.fill()
        c.new_path(); c.arc(ex, ey, 0.09 * r, 0, 2 * math.pi); c.set_source_rgb(*INK); c.fill()
    c.new_path()                                                     # the red grin
    c.arc(cx, cy + 0.18 * r, 0.52 * r, math.radians(15), math.radians(165))
    c.arc_negative(cx, cy + 0.05 * r, 0.5 * r, math.radians(160), math.radians(20))
    c.close_path(); c.set_source_rgb(0.86, 0.12, 0.16); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(lw * 0.8); c.stroke()
    c.new_path(); c.arc(cx, cy + 0.08 * r, 0.2 * r, 0, 2 * math.pi)  # the red nose, on top
    c.set_source_rgb(0.93, 0.14, 0.18); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(lw * 0.8); c.stroke()
    c.restore()
