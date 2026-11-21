"""OFFICE NOIR 3: his garage office, awake, beat 08 (20 Nov), set v1. In colour: the only colour in the film.
The office of one of his garages at night: a low sofa, a side table with a lamp, his watch and the UptimeZ welcome
pack (a CV sticks out of it: 555 0142, circled); on the wall a hook, an empty tube and the pale rectangle where a
plan was pinned; through the window, the workshop: a car up on a lift. He is the twin of the boxer: a red dressing
gown where the robe was, bare hands, the phone on his cheek where the glove was.
frames() -> 7.5 (the dream's last drawing), 8.1, 8.2, 8.3, 8.4, 8.5 (the loop: 1.1's first drawing)."""
import math
import cairo
import kit
import client_on3 as b
import ring_rough2_on3 as rr2
from kit import Ctx, cut, rect, ellipse, INK

WALL, FLOOR = (0.80, 0.77, 0.68), (0.46, 0.45, 0.46)
SOFA, SOFA_D = (0.36, 0.42, 0.40), (0.27, 0.32, 0.31)
GREEN = (0.20, 0.72, 0.36)
CARD = (0.80, 0.68, 0.48)
PAPER = (0.96, 0.95, 0.90)
Q = 1.05 * b.REL


def phone(k, x, y, s=1.0, ang=0.0, screen="done", back=False):
    """screen: done (UptimeZ Find, PREMIUM, 100% COMPLETE, green), ring (555 0142), dark."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    rect(k, -46, -84, 92, 168, (0.10, 0.10, 0.12), 3, shadow=True, lw=3)
    if back:                                                 # its back: a lens
        ellipse(k, -24, -60, 11, 11, (0.34, 0.34, 0.38), 5, shadow=False, lw=2); ellipse(k, -24, -60, 4, 4, (0.70, 0.80, 0.90), 6, shadow=False, lw=1)
    if not back:
        col = {"done": (0.92, 0.98, 0.93), "ring": (0.96, 0.96, 0.98), "dark": (0.16, 0.16, 0.18)}[screen]
        rect(k, -39, -72, 78, 144, col, 4, shadow=False, lw=1.4)
        if screen == "done":
            kit.text(k, "UptimeZ Find", 0, -48, 11.5, INK, bold=True)
            kit.text(k, "PREMIUM", 0, -30, 10, (0.45, 0.45, 0.48), bold=True)
            c.set_source_rgb(*GREEN); c.set_line_width(7); c.arc(0, 6, 22, 0, 2 * math.pi); c.stroke()
            c.set_line_width(5); c.set_line_cap(1); c.move_to(-10, 6); c.line_to(-2, 15); c.line_to(12, -5); c.stroke(); c.set_line_cap(0)
            kit.text(k, "100%", 0, 46, 15, GREEN, bold=True)
            kit.text(k, "COMPLETE", 0, 62, 10.5, GREEN, bold=True)
        elif screen == "ring":
            kit.text(k, "INCOMING", 0, -52, 10, (0.45, 0.45, 0.48), bold=True); kit.text(k, "CALL", 0, -40, 10, (0.45, 0.45, 0.48), bold=True)
            kit.text(k, "555", 0, -12, 24, INK, bold=True); kit.text(k, "0142", 0, 16, 24, INK, bold=True)
            c.set_source_rgb(*GREEN); c.arc(-18, 50, 11, 0, 2 * math.pi); c.fill()
            c.set_source_rgb(*b.KEY); c.arc(18, 50, 11, 0, 2 * math.pi); c.fill()
    c.restore()


def buzz(k, x, y, r=70, n=3):
    c = k.c
    c.set_source_rgb(*INK); c.set_line_width(3); c.set_line_cap(1)
    for i in range(n):
        for sgn in (-1, 1):
            c.new_path(); c.arc(x, y, r + i * 14, (0 if sgn > 0 else math.pi) - 0.45, (0 if sgn > 0 else math.pi) + 0.45); c.stroke()
    c.set_line_cap(0)


def cv(k, x, y, s=1.0, ang=0.0):
    """The Onboarding's sheet: CV, lines, her number, circled in red."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    rect(k, -70, -100, 140, 200, PAPER, 5, shadow=True, lw=2.2)
    kit.text(k, "CV", 0, -62, 34, INK, bold=True)
    c.set_source_rgb(0.62, 0.62, 0.64); c.set_line_width(4); c.set_line_cap(1)
    for i, w in enumerate((100, 84, 96, 70)):
        c.move_to(-50, -30 + i * 14); c.line_to(-50 + w, -31 + i * 14); c.stroke()
    c.set_line_cap(0)
    kit.text(k, "555 0142", 0, 56, 19, INK, bold=True)
    c.set_source_rgb(*b.KEY); c.set_line_width(3.4); c.save(); c.translate(0, 55); c.scale(60, 19); c.arc(0, 0, 1, 0.3, 6.6); c.restore(); c.stroke()
    c.restore()


def pack(k, x, y, s=1.0):
    """The welcome pack: a card folder, WELCOME on it, the CV sticking out of the top."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    cv(k, 14, -52, 0.62, 0.10)
    cut(k, [(-62, -40), (60, -44), (64, 44), (-60, 46)], CARD, shadow=True, lw=2.6)
    kit.text(k, "WELCOME", 0, 0, 17, INK, bold=True)
    kit.text(k, "UptimeZ Find", 0, 20, 10, (0.35, 0.33, 0.30), bold=True)
    c.restore()


def tube(k, x, y, s=1.0):
    """An empty plan tube on a hook, its cap hanging off: you can see into it."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    c.set_source_rgb(*INK); c.set_line_width(3); c.move_to(0, -150); c.line_to(0, -128); c.stroke()      # the cord, the hook
    c.arc(0, -156, 6, 0, 2 * math.pi); c.fill()
    rect(k, -17, -128, 34, 250, CARD, 7, shadow=True, lw=2.6)
    ellipse(k, 0, 122, 17, 8, (0.10, 0.09, 0.08), 8, shadow=False, lw=2.4)                               # the open end, dark: nothing in it
    c.set_source_rgb(*INK); c.set_line_width(2); c.move_to(17, 110); c.curve_to(36, 126, 30, 150, 38, 164); c.stroke()
    ellipse(k, 40, 172, 15, 8, (0.30, 0.28, 0.26), 9, shadow=False, lw=2.2)                              # its cap, hanging
    c.restore()


def floor_tube(k, x, y, s=1.0):
    """The plan's tube on the floor, its cap off beside it: PLAN on it, and nothing in it."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    rect(k, -120, -20, 230, 40, CARD, 7, shadow=True, lw=2.8)
    kit.text(k, "PLAN", -20, 0, 22, INK, bold=True)
    ellipse(k, 110, 0, 12, 20, (0.08, 0.07, 0.06), 8, shadow=False, lw=2.8)
    ellipse(k, 158, 14, 20, 9, (0.30, 0.28, 0.26), 9, shadow=True, lw=2.4)
    c.restore()


def gone(k, x, y, w, h):
    """Where the plan was pinned: a paler rectangle, four pin holes, one pin left with a torn corner."""
    c = k.c
    c.set_source_rgb(0.88, 0.86, 0.79); c.rectangle(x, y, w, h); c.fill()
    c.set_source_rgba(0, 0, 0, 0.18); c.set_line_width(2); c.set_dash([8, 6]); c.rectangle(x, y, w, h); c.stroke(); c.set_dash([])
    for i, (px, py, sx, sy) in enumerate(((x, y, 1, 1), (x + w, y, -1, 1), (x, y + h, 1, -1), (x + w, y + h, -1, -1))):
        cut(k, [(px + sx * 2, py + sy * 2), (px + sx * 40, py + sy * 5), (px + sx * 22, py + sy * 16), (px + sx * 9, py + sy * 34)], (0.80, 0.88, 0.96), shadow=False, lw=1.8)
        c.set_source_rgb(0.25, 0.40, 0.62); c.set_line_width(1.6)
        c.move_to(px + sx * 8, py + sy * 8); c.line_to(px + sx * 28, py + sy * 8); c.move_to(px + sx * 8, py + sy * 8); c.line_to(px + sx * 8, py + sy * 24); c.stroke()
        c.set_source_rgb(*b.KEY); c.arc(px + sx * 10, py + sy * 10, 4.4, 0, 2 * math.pi); c.fill()


def window(k, x, y, w, h):
    """The workshop through the glass: strip light, a car up on a two-post lift."""
    c = k.c
    rect(k, x - 8, y - 8, w + 16, h + 16, (0.30, 0.29, 0.28), 3, shadow=False, lw=3)
    c.save(); c.rectangle(x, y, w, h); c.clip()
    c.set_source_rgb(0.62, 0.74, 0.80); c.paint()
    c.set_source_rgb(0.90, 0.96, 0.98); c.rectangle(x + 10, y + 12, w - 20, 9); c.fill()                 # the strip light
    c.set_source_rgb(0.38, 0.46, 0.52); c.rectangle(x, y + h - 34, w, 34); c.fill()                      # the workshop floor
    c.set_source_rgb(0.20, 0.24, 0.28)
    for px in (x + 34, x + w - 46):
        c.rectangle(px, y + 52, 12, h - 86); c.fill()                                                    # the posts
    c.rectangle(x + 34, y + 128, w - 68, 8); c.fill()                                                    # the arms
    c.new_path(); cx = x + w / 2; cy = y + 126                                                           # the car, side on, up in the air
    c.move_to(cx - 84, cy); c.line_to(cx - 80, cy - 26); c.line_to(cx - 44, cy - 30); c.line_to(cx - 24, cy - 56); c.line_to(cx + 34, cy - 56)
    c.line_to(cx + 56, cy - 30); c.line_to(cx + 84, cy - 24); c.line_to(cx + 86, cy); c.close_path()
    c.set_source_rgb(0.72, 0.20, 0.18); c.fill()
    c.set_source_rgb(0.12, 0.13, 0.15)
    for wx in (cx - 50, cx + 52):
        c.arc(wx, cy + 2, 17, 0, 2 * math.pi); c.fill()
    c.restore()
    c.set_source_rgb(0.30, 0.29, 0.28); c.set_line_width(5); c.move_to(x + w / 2, y); c.line_to(x + w / 2, y + h); c.stroke()


def lamp(k, x, y):
    c = k.c
    c.set_source_rgb(*INK); c.set_line_width(5); c.move_to(x, y); c.line_to(x - 6, y - 70); c.line_to(x - 40, y - 96); c.stroke()
    ellipse(k, x, y, 22, 6, (0.20, 0.20, 0.22), 3, shadow=False, lw=2)
    cut(k, [(x - 66, y - 82), (x - 34, y - 112), (x - 20, y - 92), (x - 56, y - 64)], (0.20, 0.34, 0.30), shadow=False, lw=2.6)


def sleeper(k, x, y, face="exhausted", look=(0, 0.4), cover=0.0):
    """Him on the sofa, on his back, his head to screen right at (x, y) on the arm. cover 0..1: the gown over his head."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(math.pi / 2); c.translate(0, -b.HY * Q)       # the head stays where it is
    o = b.boxer(k, 0, 0, Q, "b_walk", face, look, awake=True)
    c.restore()
    if cover > 0:                                           # the gown, pulled up over his face
        cut(k, [(x - 70, y - 62), (x - 20, y - 78), (x + 52, y - 60), (x + 70, y - 6), (x + 56, y + 58), (x - 10, y + 70), (x - 76, y + 56)], b.GOWN, shadow=False, lw=3.4)
        c.set_source_rgb(*b.GOWN_SHADE); c.set_line_width(3); c.set_line_cap(1)
        for dx in (-30, 6, 36):
            c.move_to(x + dx, y - 50); c.curve_to(x + dx + 10, y - 10, x + dx - 8, y + 20, x + dx + 6, y + 50); c.stroke()
        c.set_line_cap(0)
    return o


def room(k, phone_at="floor", cover=0.0, face="exhausted", ringing=False):
    """8.2 / 8.4, the wide."""
    c = k.c
    c.set_source_rgb(*WALL); c.paint()
    c.set_source_rgb(*FLOOR); c.rectangle(-200, 742, 940, 600); c.fill()
    g = cairo.RadialGradient(430, 560, 30, 430, 560, 620)                                                # the desk lamp's pool
    g.add_color_stop_rgba(0, 1, 0.95, 0.75, 0.45); g.add_color_stop_rgba(1, 0.05, 0.05, 0.12, 0.42); c.set_source(g); c.paint()
    cut(k, [(-20, 742), (560, 742), (560, 980), (-20, 980)], FLOOR, shadow=False, lw=3)
    window(k, 296, 170, 210, 250)
    gone(k, 74, 250, 170, 130)
    c.set_source_rgb(*INK); c.set_line_width(3.4); c.arc(262, 236, 9, 0.2, math.pi + 0.6); c.stroke(); c.arc(262, 222, 4, 0, 2 * math.pi); c.fill()   # the hook, bare
    rect(k, 14, 600, 400, 150, SOFA_D, 5, shadow=False, lw=3.4)                                           # the sofa: back, arm, seat
    rect(k, 8, 664, 410, 96, SOFA, 6, shadow=False, lw=3.4)
    rect(k, 364, 618, 60, 142, SOFA, 7, shadow=False, lw=3.4)
    rect(k, 318, 632, 64, 44, (0.84, 0.80, 0.66), 8, shadow=False, lw=2.6)                                # a cushion, under his head
    o = sleeper(k, 344, 648, face, cover=cover)
    rect(k, 434, 668, 100, 12, (0.42, 0.30, 0.20), 9, shadow=False, lw=3)                                 # the side table
    rect(k, 444, 680, 10, 70, (0.36, 0.26, 0.18), 10, shadow=False, lw=2.4); rect(k, 514, 680, 10, 70, (0.36, 0.26, 0.18), 11, shadow=False, lw=2.4)
    lamp(k, 512, 668)
    pack(k, 474, 640, 0.52)
    floor_tube(k, 150, 818)
    if phone_at == "floor":                                 # it has buzzed itself off the edge
        phone(k, 440, 800, 0.42, 1.2, "done")
        buzz(k, 440, 800, 34, 2)
    elif phone_at == "pack":                                # face down on the CV
        cut(k, [(372, 636), (452, 606), (458, 624), (378, 660)], b.GOWN, shadow=False, lw=3)        # his arm, out from under the gown
        phone(k, 478, 612, 0.40, 1.45, back=True)
        ellipse(k, 462, 614, 13, 11, (0.90, 0.76, 0.66), 14, shadow=False, lw=2.4)
        if ringing:
            buzz(k, 482, 606, 32, 2)
    return o


def _surf():
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(s)
    return s, c, Ctx(c, 0)


def _zoom(c, z=1.22, cx=292, cy=540):
    c.translate(270, 480); c.scale(z, z); c.translate(-cx, -cy)


def f81(eye=True):
    """8.1: the framing of 7.5, in colour. A sofa cushion where the ring was; the phone on his cheek where the glove was."""
    s, c, k = _surf()
    c.set_source_rgb(0.84, 0.80, 0.66); c.paint()
    c.set_source_rgba(0, 0, 0, 0.10); c.set_line_width(3)
    for i in range(-4, 12):
        c.move_to(i * 90, 0); c.line_to(i * 90 + 300, 960); c.stroke()
    g = cairo.RadialGradient(380, 500, 40, 380, 500, 700); g.add_color_stop_rgba(0, 0.6, 1, 0.7, 0.20); g.add_color_stop_rgba(1, 0, 0, 0, 0.30); c.set_source(g); c.paint()
    sc = 3.3 * b.REL
    b.boxer(k, 210, 520 - b.HY * sc + 20, sc, "b_walk", "suspicious" if eye else "exhausted", (0.9, 0.2), awake=True)
    phone(k, 372, 506, 1.5, 0.30, "done")
    return s


def f82():
    s, c, k = _surf(); _zoom(c); room(k); return s


def f83():
    """8.3: the phone rings in his hand: 555 0142. Beside it, on the table, the CV: 555 0142, circled."""
    s, c, k = _surf()
    c.set_source_rgb(0.42, 0.30, 0.20); c.paint()
    g = cairo.RadialGradient(300, 300, 40, 300, 300, 800); g.add_color_stop_rgba(0, 1, 0.95, 0.75, 0.35); g.add_color_stop_rgba(1, 0, 0, 0, 0.35); c.set_source(g); c.paint()
    cut(k, [(250, 470), (560, 440), (560, 900), (270, 930)], CARD, shadow=True, lw=3)
    kit.text(k, "WELCOME", 420, 800, 36, INK, bold=True)
    cv(k, 392, 380, 1.9, 0.07)
    cut(k, [(-40, 980), (-40, 700), (60, 640), (150, 700), (190, 980)], b.GOWN, shadow=False, lw=4)       # his sleeve
    ellipse(k, 124, 640, 62, 50, (0.90, 0.76, 0.66), 12, shadow=False, lw=3)                              # his hand
    phone(k, 138, 520, 1.55, -0.10, "ring")
    buzz(k, 138, 430, 96, 2)
    return s


def f84():
    s, c, k = _surf(); _zoom(c); room(k, phone_at="pack", cover=1.0, ringing=True); return s


def f85():
    """The loop: the dream's first drawing again (1.1 = 7.5 before it lands)."""
    return rr2.shot_75(0.6)


def frames():
    return [rr2.shot_75(0.74), f81(), f82(), f83(), f84(), f85()]
