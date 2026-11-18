"""The black cat of "Office Noir" (v9 cold open, 18 Nov): it walks along the top of the monitor, stops over the
heart, arches and hisses at Don, and drops out of frame. Its twin in the bedroom sleeps curled on Don's blanket.
Paper cut-out like the rest of the kit; the eyes are drawn in their own colour after the noir pass, so they glow.

black_cat(k, x, y, s, pose, t, flip, eyes)
  (x, y): where its feet stand (for "curl", the middle of its underside); s: scale (1 = about 110 px long)
  pose: "walk" (t drives the legs), "arch" (back up, fur up, mouth open), "curl" (asleep), "fall" (legs out)
  flip: True faces left; eyes: "open", "closed", "one" (one eye opens)"""
import math
import kit
from kit import INK

FUR = (0.09, 0.09, 0.10)
FUR_HI = (0.20, 0.20, 0.22)
EYE = (0.86, 0.80, 0.26)
MOUTH = (0.55, 0.22, 0.25)


def _leg(k, x0, y0, x1, y1, w=6.0):
    dx, dy = x1 - x0, y1 - y0
    n = math.hypot(dx, dy) or 1
    px, py = -dy / n * w / 2, dx / n * w / 2
    kit.cut(k, [(x0 + px, y0 + py), (x1 + px, y1 + py), (x1 - px, y1 - py), (x0 - px, y0 - py)], FUR,
            shadow=False, lw=2.0)
    kit.ellipse(k, x1, y1, w * 0.75, w * 0.5, FUR, 901, shadow=False, lw=1.6)


def _ears(k, hx, hy, r, flat=False):
    for sx in (-1, 1):
        if flat:                                       # ears pinned back: hissing
            pts = [(hx + sx * r * 0.2 - r * 0.6, hy - r * 0.7), (hx + sx * r * 0.2 - r * 1.45, hy - r * 0.55),
                   (hx + sx * r * 0.2 - r * 0.45, hy - r * 0.25)]
        else:
            pts = [(hx + sx * r * 0.85, hy - r * 0.35), (hx + sx * r * 0.75, hy - r * 1.35),
                   (hx + sx * r * 0.15, hy - r * 0.85)]
        kit.cut(k, pts, FUR, shadow=False, lw=2.0)


def _eye(c, x, y, r, state, slit=True):
    if state == "closed":
        c.set_source_rgb(*FUR_HI); c.set_line_width(2.2)
        c.new_path(); c.arc(x, y - r * 0.4, r, 0.25 * math.pi, 0.75 * math.pi); c.stroke()
        return
    c.new_path(); c.arc(x, y, r, 0, 2 * math.pi); c.set_source_rgb(*EYE); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(1.4); c.stroke()
    if slit:
        c.new_path(); c.save(); c.translate(x, y); c.scale(0.28, 1.0)
        c.arc(0, 0, r * 0.85, 0, 2 * math.pi); c.restore(); c.set_source_rgb(0.05, 0.05, 0.05); c.fill()


def _tail(c, pts, w):
    c.set_line_cap(1); c.set_line_join(1)
    for col, lw in ((INK, w + 4), (FUR, w)):
        c.new_path(); c.move_to(*pts[0]); c.curve_to(*pts[1], *pts[2], *pts[3])
        c.set_source_rgb(*col); c.set_line_width(lw); c.stroke()


def black_cat(k, x, y, s=1.0, pose="walk", t=0.0, flip=True, eyes="open"):
    c = k.c
    c.save(); c.translate(x, y); c.scale(-s if flip else s, s)
    if pose == "curl":
        _tail(c, [(-46, -6), (-40, 14), (20, 16), (40, 4)], 9)
        kit.ellipse(k, 0, -22, 52, 26, FUR, 905, shadow=False, lw=2.4)
        c.set_source_rgb(*FUR_HI); c.set_line_width(2); c.new_path(); c.arc(-6, -24, 30, 3.6, 5.2); c.stroke()
        hx, hy, r = 38, -30, 17
        _ears(k, hx, hy, r)
        kit.ellipse(k, hx, hy, r, r * 0.9, FUR, 906, shadow=False, lw=2.2)
        c.restore()
        c.save(); c.translate(x, y); c.scale(-s if flip else s, s)
        e1 = "closed" if eyes == "closed" else "closed"
        e2 = "open" if eyes in ("open", "one") else "closed"
        _eye(c, hx - 7, hy - 2, 3.6, e1, slit=False)
        _eye(c, hx + 7, hy - 2, 3.6, e2)
        c.restore()
        return
    if pose == "arch":                                    # the Halloween cat: back up, tail up and bristled
        _tail(c, [(-40, -62), (-58, -90), (-50, -128), (-60, -150)], 13)
        for i in range(7):                                # bristles on the tail
            a = -1.9 + 0.35 * i
            c.set_source_rgb(*FUR); c.set_line_width(3)
            c.new_path(); c.move_to(-56 + 2 * math.cos(a), -110 + 30 * (i / 6) - 20); c.rel_line_to(9 * math.cos(a), 6 * math.sin(a)); c.stroke()
        for lx in (-34, -22, 26, 38):
            _leg(k, lx, -50, lx + (2 if lx > 0 else -2), 0, 7)
        kit.cut(k, [(-48, -48), (-40, -78), (-18, -96), (8, -98), (30, -86), (46, -60), (40, -44), (14, -56),
                    (-14, -56), (-36, -42)], FUR, shadow=False, lw=2.4)
        for i in range(9):                                # fur up along the arch
            a = math.pi * (1.05 + 0.9 * i / 8)
            px, py = 0 + 44 * math.cos(a), -60 + 40 * math.sin(a)
            c.set_source_rgb(*FUR); c.set_line_width(3)
            c.new_path(); c.move_to(px, py); c.rel_line_to(6 * math.cos(a), 6 * math.sin(a)); c.stroke()
        hx, hy, r = 58, -58, 19
        _ears(k, hx, hy, r, flat=True)
        kit.ellipse(k, hx, hy, r, r * 0.92, FUR, 907, shadow=False, lw=2.4)
        c.new_path(); c.save(); c.translate(hx + 9, hy + 9); c.scale(1.0, 0.8)
        c.arc(0, 0, 7, 0, 2 * math.pi); c.restore(); c.set_source_rgb(*MOUTH); c.fill_preserve()
        c.set_source_rgb(*INK); c.set_line_width(1.6); c.stroke()
        c.set_source_rgb(0.95, 0.95, 0.92)                # two fangs
        for fx in (-3, 3):
            c.new_path(); c.move_to(hx + 9 + fx - 1.6, hy + 4); c.line_to(hx + 9 + fx + 1.6, hy + 4)
            c.line_to(hx + 9 + fx, hy + 9); c.close_path(); c.fill()
        c.set_source_rgb(0.75, 0.75, 0.72); c.set_line_width(1.0)    # whiskers, pushed forward
        for wy in (-1, 3):
            c.new_path(); c.move_to(hx + 12, hy + 3 + wy); c.rel_line_to(18, wy * 1.5 - 2); c.stroke()
        _eye(c, hx + 4, hy - 5, 5.2, eyes)
        c.restore()
        return
    # walk / fall: a long body, head forward
    ph = 2 * math.pi * t * 3.2
    if pose == "fall":
        legs = [(-34, -26, -46, 4), (-22, -26, -26, 8), (26, -26, 30, 8), (38, -26, 52, 2)]
    else:
        sw = 10 * math.sin(ph)
        legs = [(-36, -24, -36 + sw, 0), (-24, -24, -24 - sw, 0), (24, -24, 24 - sw, 0), (36, -24, 36 + sw, 0)]
    _tail(c, [(-46, -34), (-70, -40), (-74, -78), (-60 - 6 * math.sin(ph * 0.5), -96)], 9)
    for x0, y0, x1, y1 in legs:
        _leg(k, x0, y0, x1, y1, 6.5)
    kit.ellipse(k, 0, -34, 52, 17, FUR, 908, shadow=False, lw=2.4)
    hx, hy, r = 56, -46, 17
    _ears(k, hx, hy, r)
    kit.ellipse(k, hx, hy, r, r * 0.9, FUR, 909, shadow=False, lw=2.2)
    _eye(c, hx + 6, hy - 3, 4.6, eyes)
    c.restore()
