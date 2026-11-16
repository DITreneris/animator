"""v1, pinned (the current file is v2). THE BEST CANDIDATE, v1: props. The small one's CV (as thick as a brick), the macho's cookie tin, Pam's pen,
Don's clipboard (with the doodle he hides) and his lanyard card: a VISITOR pass with VISITOR crossed out and
HEAD OF TALENT written on it in marker."""
import math
import kit
from kit import INK, cut, rect, ellipse

PAPER = (0.99, 0.98, 0.95)
PAPER_EDGE = (0.86, 0.84, 0.78)
TIN = (0.74, 0.16, 0.18)
TIN_DARK = (0.52, 0.09, 0.12)
COOKIE = (0.86, 0.64, 0.36)
CHIP = (0.34, 0.20, 0.12)
BOARD = (0.55, 0.38, 0.24)
CLIP = (0.62, 0.64, 0.68)
MARKER = (0.10, 0.10, 0.14)
ORANGE = (0.96, 0.56, 0.14)
LANYARD = (0.17, 0.71, 0.45)


def cv_brick(k, x, y, s=1.0, rot=0.0, seed=0, label=True):
    """A CV about 300 pages thick: a white cover, a block of page edges, coloured tabs. (x, y) = centre."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    w, h, d = 74, 92, 30
    cut(k, [(-w / 2 + d * 0.5, -h / 2 - d * 0.35), (w / 2 + d * 0.5, -h / 2 - d * 0.35), (w / 2 + d * 0.5, h / 2 - d * 0.35),
            (w / 2, h / 2), (-w / 2, h / 2), (-w / 2, -h / 2)], PAPER_EDGE, lw=2)
    c.set_source_rgb(0.62, 0.60, 0.55); c.set_line_width(1)
    for i in range(1, 9):                                                    # page edges, top and right faces
        u = i / 9.0
        c.move_to(-w / 2 + d * 0.5 * u, -h / 2 - d * 0.35 * u); c.line_to(w / 2 + d * 0.5 * u, -h / 2 - d * 0.35 * u)
        c.line_to(w / 2 + d * 0.5 * u, h / 2 - d * 0.35 * u); c.stroke()
    for i, col in enumerate(((0.95, 0.40, 0.35), (0.98, 0.78, 0.25), (0.35, 0.72, 0.50), (0.38, 0.60, 0.90))):
        rect(k, w / 2 + d * 0.5 - 2, -h / 2 + 4 + i * 19, 9, 12, col, seed + 5 + i, shadow=False, lw=1.3)   # tabs
    rect(k, -w / 2, -h / 2, w, h, PAPER, seed + 1, shadow=False, lw=2)
    if label:
        kit.text(k, "CV", 0, -18, 30, INK)
        c.set_source_rgb(0.55, 0.55, 0.58); c.set_line_width(2.4); c.set_line_cap(1)
        for i, ww in enumerate((46, 38, 44, 30)):
            c.move_to(-w / 2 + 12, 8 + i * 9); c.line_to(-w / 2 + 12 + ww, 8 + i * 9); c.stroke()
    c.restore()


def cookie(k, x, y, r, seed=0):
    ellipse(k, x, y, r, r * 0.92, COOKIE, seed, shadow=False, lw=1.6)
    c = k.c
    c.set_source_rgb(*CHIP)
    for dx, dy in ((-0.35, -0.25), (0.3, -0.3), (0.05, 0.3), (-0.4, 0.35), (0.42, 0.2)):
        c.arc(x + dx * r, y + dy * r, r * 0.15, 0, 2 * math.pi); c.fill()


def cookie_tin(k, x, y, s=1.0, seed=0, lid=True):
    """An open round tin seen from the front, cookies piled above the rim, a hand-written tag: FOR EVERYONE."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    for i, (dx, dy) in enumerate(((-22, -22), (0, -28), (22, -22), (-11, -34), (12, -35))):
        cookie(k, dx, dy, 13, seed + 10 + i)
    cut(k, [(-40, -18), (40, -18), (36, 22), (-36, 22)], TIN, lw=2.2)
    c.set_source_rgb(*TIN_DARK); c.set_line_width(2.2)
    c.move_to(-39, -9); c.line_to(39, -9); c.stroke()
    rect(k, -24, -3, 48, 19, PAPER, seed + 2, shadow=False, lw=1.4)
    kit.text(k, "FOR EVERYONE", 0, 6, 6.6, MARKER, font="Permanent Marker")
    c.restore()


def pen(k, x, y, s=1.0, ang=0.0):
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    c.set_source_rgb(*INK); c.set_line_width(7); c.set_line_cap(1); c.move_to(-17, 0); c.line_to(17, 0); c.stroke()
    c.set_source_rgb(0.45, 0.29, 0.62); c.set_line_width(4.2); c.move_to(-17, 0); c.line_to(12, 0); c.stroke()
    c.set_source_rgb(0.85, 0.85, 0.88); c.set_line_width(4.2); c.move_to(12, 0); c.line_to(17, 0); c.stroke()
    c.restore()


def doodle(c, x, y, s=1.0):
    """Don's interview notes: a stick figure of himself with a crown, and a heart."""
    c.save(); c.translate(x, y); c.scale(s, s)
    c.set_source_rgb(*MARKER); c.set_line_width(2); c.set_line_cap(1); c.set_line_join(1)
    c.arc(0, -8, 7, 0, 2 * math.pi); c.stroke()
    c.move_to(-7, -15); c.line_to(-6, -22); c.line_to(-2.5, -17); c.line_to(0, -23); c.line_to(2.5, -17)
    c.line_to(6, -22); c.line_to(7, -15); c.stroke()
    c.move_to(0, -1); c.line_to(0, 14); c.move_to(-8, 5); c.line_to(8, 5)
    c.move_to(0, 14); c.line_to(-6, 24); c.move_to(0, 14); c.line_to(6, 24); c.stroke()
    c.set_source_rgb(0.82, 0.16, 0.20)
    c.move_to(18, 2); c.curve_to(12, -6, 22, -8, 18, -1); c.curve_to(14, -8, 24, -6, 18, 2); c.stroke()
    c.restore()


def clipboard(k, x, y, s=1.0, rot=0.0, seed=0, side="front"):
    """(x, y) = centre. side "front": the paper with the doodle; "back": the bare board (hidden from Mom)."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    rect(k, -30, -40, 60, 80, BOARD, seed + 1, lw=2)
    if side == "front":
        rect(k, -25, -30, 50, 66, PAPER, seed + 2, shadow=False, lw=1.5)
        kit.text(k, "CANDIDATES", 0, -20, 6.4, INK, font="Inter", bold=True)
        c.set_source_rgb(0.60, 0.60, 0.63); c.set_line_width(1.6)
        for i in range(3):
            c.move_to(-20, -10 + i * 6); c.line_to(-4 - i * 3, -10 + i * 6); c.stroke()
        doodle(c, 4, 16, 0.78)
    rect(k, -13, -47, 26, 12, CLIP, seed + 3, shadow=False, lw=1.6)
    c.restore()


def talent_card(k, x, y, s=1.0, rot=0.0, seed=0):
    """Don's lanyard card: a VISITOR pass, VISITOR struck through, HEAD OF TALENT in marker. (x, y) = centre."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    rect(k, -5, -22, 10, 7, CLIP, seed + 1, shadow=False, lw=1.3)
    rect(k, -24, -17, 48, 34, (1, 1, 1), seed + 2, shadow=False, lw=1.8)
    c.set_source_rgb(*ORANGE); c.rectangle(-22.5, -15.5, 45, 9); c.fill()
    kit.text(k, "VISITOR", 0, -10.6, 6.2, INK, font="Inter", bold=True)
    c.set_source_rgb(*MARKER); c.set_line_width(1.8); c.set_line_cap(1)
    c.move_to(-17, -10); c.line_to(17, -11.5); c.stroke()
    kit.text(k, "HEAD OF", 0, -0.5, 7.6, MARKER, font="Permanent Marker")
    kit.text(k, "TALENT", 0, 9.5, 10.5, MARKER, font="Permanent Marker")
    c.restore()
