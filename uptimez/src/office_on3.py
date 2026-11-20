"""OFFICE NOIR 3: Mom's office, set v1 (20 Nov; Tomas, /grill-me). A back office over the arena: a window with blinds
that looks down on the ring's glow, which she never turns to; its light lies in stripes on the wall behind her, so her
black coat has a pale ground. She sits behind the desk in a high-backed chair in every shot and never gets up. On the
desk, two things with a job: the button (her word reaches the ring through it) and the coupe (never lifted). No cash
box, no rake, no cards: the hundred stays in her hand.
Three camera setups, each its own drawing on the same room:
  M1 front(...)     she fills the frame: 5.4, 7.4, and the right half of 6.2
  M2 over(...)      over his shoulder: his hooded back and red glove large, she is small across a deep desk: 4.3
  M3 reverse(...)   her view: him small in front of the desk, her ringed hand and the button in the foreground: 4.4
Each returns a 540x960 surface in the dream's look. Nothing here changes an earlier module."""
import math
import cairo
import kit
import mom_on3 as q
import client_on3 as b
import client_sheet_on3 as csh
from kit import Ctx, cut, rect, ellipse, INK

WALL, WALL_LIT = (0.30, 0.30, 0.32), (0.88, 0.88, 0.85)
DESK = (0.46, 0.44, 0.42)
CHAIR = (0.33, 0.31, 0.30)
SKIN = (0.90, 0.76, 0.66)
TRACK = (0.24, 0.24, 0.27)
BUTTON = (392, 806)


def _lerp(a, b_, t):
    t = max(0.0, min(1.0, t)); t = t * t * (3 - 2 * t)
    if isinstance(a, tuple):
        return tuple(x + (y - x) * t for x, y in zip(a, b_))
    return a + (b_ - a) * t


def room(c, k):
    """The wall behind her, the stripes the blinds throw on it, and the window over the arena."""
    c.set_source_rgb(*WALL); c.rectangle(0, 0, 540, 960); c.fill()
    c.save(); c.rectangle(0, 60, 540, 730); c.clip()
    c.set_source_rgb(*WALL_LIT)                              # the arena's glow, through the blinds, across the wall
    for i in range(16):
        y = 96 + i * 44
        c.move_to(-20, y + 70); c.line_to(560, y - 40); c.line_to(560, y - 16); c.line_to(-20, y + 94); c.close_path(); c.fill()
    c.restore()
    c.set_source_rgb(0.07, 0.07, 0.08); c.rectangle(372, 96, 150, 330); c.fill()          # the window: night
    g = cairo.LinearGradient(0, 300, 0, 426)                 # and the ring's glow, from below
    g.add_color_stop_rgba(0, 1, 1, 1, 0); g.add_color_stop_rgba(1, 1, 1, 1, 0.9); c.set_source(g); c.rectangle(372, 300, 150, 126); c.fill()
    c.set_source_rgb(0.96, 0.96, 0.92)
    for i in range(11):
        c.rectangle(372, 104 + i * 30, 150, 15); c.fill()
    c.set_source_rgb(0.05, 0.05, 0.06); c.set_line_width(6); c.rectangle(372, 96, 150, 330); c.stroke()
    c.set_line_width(2); c.move_to(512, 96); c.line_to(512, 460); c.stroke()               # the cord


def mom(k, note=True, down=0.0, look=(-0.9, -0.1), mouth=None, pose="q_read"):
    """Seated: lower than standing, the chair's back to her ears. down 0..1: her screen-right arm onto the button."""
    cut(k, [(96, 800), (104, 500), (140, 462), (360, 462), (396, 500), (404, 800)], CHAIR, shadow=False, lw=3)
    for bx_ in (150, 250, 350):
        ellipse(k, bx_, 520, 6, 6, (0.20, 0.19, 0.19), 20 + bx_, shadow=False, lw=1.6)
    sc = 1.55
    P = q._body.__globals__["POSES"]
    old = P[pose]
    P[pose] = old[:2] + _lerp(old[2:], q.mo.ik(1, 92, -124), down)
    try:
        return q.queen(k, 250, 400 + 294 * sc + 112, sc, pose, "bored", look=look, note=note and pose == "q_read", mouth=mouth)
    finally:
        P[pose] = old


def card(k, x, y, s=1.0, ang=0.0, sym="star", sq=0.62):
    """v2: one tarot card laid on the desk (sq: how flat we see it). Symbols only: star, tower, gear (his garages'), back."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(1, sq); c.rotate(ang); c.scale(s, s)
    cut(k, [(-17, -27), (17, -27), (17, 27), (-17, 27)], q.CARD if sym != "back" else (0.16, 0.16, 0.18), lw=2)
    c.set_source_rgb(*((0.80, 0.80, 0.78) if sym == "back" else INK)); c.set_line_width(1.2); c.rectangle(-13, -23, 26, 46); c.stroke()
    if sym == "gear":
        q.co.gear(k, 0, 0, 10, col=q.CARD, seed=5)
    elif sym == "star":
        c.new_path()
        for j in range(10):
            a = math.pi * 2 * j / 10 - math.pi / 2
            rr = 11 if j % 2 == 0 else 4.6
            (c.move_to if j == 0 else c.line_to)(rr * math.cos(a), rr * math.sin(a))
        c.close_path(); c.set_source_rgb(*INK); c.fill()
    elif sym == "tower":
        c.set_source_rgb(*INK); c.rectangle(-6, -11, 12, 26); c.fill()
        for dx in (-6, -1, 4):
            c.rectangle(dx, -16, 3, 5); c.fill()
    else:
        c.move_to(-13, -23); c.line_to(13, 23); c.move_to(13, -23); c.line_to(-13, 23); c.stroke()
    c.restore()


def spread(k, x, y, s=1.0, side=1, sq=0.62):
    """v2 (Tomas, 20 Nov: the desk looked empty): her tarot spread. Three cards face up in a row, the gear last, and
    the deck beside them. side: +1 as she sees it (the deck at her right), -1 from the other side of the desk."""
    for i, sym in enumerate(("star", "tower", "gear")):
        card(k, x + side * (i - 1) * 46 * s, y + (2 if i == 1 else 0) * s, s, side * (i - 1) * 0.10 + (math.pi if side < 0 else 0), sym, sq)
    for j in range(3):
        card(k, x + side * 118 * s + j * 2 * s, y - j * 3 * s, s, 0.2, "back", sq)


def desk(c, k, press=0.0, hand=None, lamp=True, cards=False):
    """The desk across the frame, the coupe, the button on its plate. hand: her hand's point, drawn onto the button."""
    rect(k, -20, 790, 580, 200, DESK, 5, shadow=False, lw=3)
    g = cairo.RadialGradient(BUTTON[0], 800, 10, BUTTON[0], 800, 240)
    g.add_color_stop_rgba(0, 1, 1, 1, 0.35); g.add_color_stop_rgba(1, 1, 1, 1, 0); c.set_source(g); c.rectangle(0, 790, 540, 170); c.fill()
    q.coupe(k, 86, 850, 1.7)
    if cards:
        spread(k, 214, 900, 1.25, -1, 0.5)
    bx, by = BUTTON
    rect(k, bx - 50, by - 2, 100, 26, (0.10, 0.10, 0.11), 6, shadow=False, lw=2.4)
    ellipse(k, bx, by + 5 * press, 30, 14 - 5 * press, (0.98, 0.98, 0.94) if press > 0.9 else (0.55, 0.55, 0.56), 7, shadow=False, lw=2.6)
    if hand:
        hx, hy = hand
        fy = by - 4 + 5 * press
        c.set_source_rgb(0.08, 0.08, 0.09); c.set_line_width(19); c.set_line_cap(1); c.move_to(hx, hy); c.line_to(bx, fy); c.stroke()
        c.set_source_rgb(*SKIN); c.set_line_width(14); c.move_to(hx, hy); c.line_to(bx, fy); c.stroke(); c.set_line_cap(0)
        ellipse(k, hx, hy, 17, 17, SKIN, 10, shadow=False, lw=2.4)
        rect(k, (hx + bx) / 2 - 11, (hy + fy) / 2 - 6, 22, 12, (0.86, 0.87, 0.90), 11, shadow=False, lw=1.6)


def _front(c, k, note=True, down=0.0, press=0.0, look=(-0.9, -0.1), mouth=None, cards=False):
    room(c, k)
    o = mom(k, note, down, look, mouth)
    desk(c, k, press, o["hands"][1] if down > 0.6 else None, cards=cards)


def front(note=True, down=0.0, press=0.0, look=(-0.9, -0.1), mouth=None, cards=False):
    """M1: she fills the frame."""
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(s); k = Ctx(c, 0)
    _front(c, k, note, down, press, look, mouth, cards)
    csh.noir(s)
    return s


def over(glove_up=0.0, look=(0.2, 0.9), show=False, cards=False):
    """M2, 4.3: over his shoulder. His hood and back fill the near left; one red glove, lower right, comes up with the
    note in it (glove_up 0..1). Across a deep desk she is small, and does not look up."""
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(s); k = Ctx(c, 0)
    c.set_source_rgb(*WALL); c.paint()
    c.save(); c.translate(226, 40); c.scale(0.56, 0.56)      # the far end of the room: M1, small
    c.rectangle(0, 0, 540, 800); c.clip()
    room(c, k); mom(k, False, 0.0, look, None, pose="q_stand")
    c.restore()
    c.set_source_rgb(0.05, 0.05, 0.06); c.set_line_width(5); c.rectangle(226, 40, 302, 448); c.stroke()
    cut(k, [(190, 482), (560, 482), (700, 900), (-60, 900)], DESK, shadow=False, lw=3)     # the desk, deep, toward us
    g = cairo.LinearGradient(0, 482, 0, 900); g.add_color_stop_rgba(0, 1, 1, 1, 0.30); g.add_color_stop_rgba(1, 0, 0, 0, 0.25)
    c.set_source(g); c.rectangle(-100, 482, 740, 418); c.fill()
    rect(k, 430, 498, 62, 16, (0.10, 0.10, 0.11), 6, shadow=False, lw=2)                   # the button, by her
    ellipse(k, 461, 498, 18, 9, (0.55, 0.55, 0.56), 7, shadow=False, lw=2)
    q.coupe(k, 286, 520, 0.95)
    if cards:
        spread(k, 372, 600, 1.15, -1, 0.5)
    cut(k, [(-60, 980), (-60, 560), (-10, 380), (90, 300), (190, 380), (240, 580), (256, 980)], TRACK, shadow=False, lw=4)   # his back, hood up
    c.set_source_rgb(0.14, 0.14, 0.16); c.set_line_width(4); c.set_line_cap(1)
    c.move_to(10, 430); c.curve_to(60, 350, 130, 350, 172, 430); c.stroke()               # the hood's seam
    c.move_to(92, 470); c.line_to(92, 960); c.stroke()
    gx, gy = 390, _lerp(900.0, 720.0, glove_up)              # his glove, the note pinched against it
    cut(k, [(gx - 60, 980), (gx - 44, gy + 60), (gx + 30, gy + 60), (gx + 50, 980)], TRACK, shadow=False, lw=3.4)
    c.save(); c.translate(gx, gy); c.scale(3.0, 3.0); c.translate(-gx, -gy)
    b.banknote(k, gx + 6, gy - 22, 0.55, -0.3, 3)
    b._glove(k, gx, gy, 0.1, -1.0, 1, 71)
    c.restore()
    if show:                                                 # v2, opt-in: the hundred, whole, held out past the glove (v1 hid it behind the glove)
        b.banknote(k, gx - 96, gy - 64, 2.1, -0.16, 3)
    csh.noir(s)
    return s


def reverse(pay=0.0, take=0.0, cards=False):
    """M3, 4.4: her view. He is small, in his tracksuit, in front of the desk, the door behind him. pay 0..1: the note
    crosses the desk toward us. take 0..1: her ringed hand comes in from the near edge and covers it."""
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(s); k = Ctx(c, 0)
    g = cairo.RadialGradient(270, 300, 30, 270, 300, 620)
    g.add_color_stop_rgba(0, 0.62, 0.62, 0.62, 1); g.add_color_stop_rgba(1, 0.24, 0.24, 0.26, 1); c.set_source(g); c.paint()
    rect(k, 190, 110, 160, 400, (0.20, 0.20, 0.22), 3, shadow=False, lw=4)                 # the door he came in by
    rect(k, 206, 126, 128, 170, (0.74, 0.74, 0.72), 4, shadow=False, lw=2.4)               # its glass, lit from the stairs
    ellipse(k, 326, 330, 7, 7, (0.80, 0.80, 0.82), 5, shadow=False, lw=1.6)
    sc = 1.15 * b.REL
    c.save(); c.set_source_rgba(0, 0, 0, 0.3); c.translate(270, 560); c.scale(70, 12); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
    b.boxer(k, 270, 560, sc, "b_pay" if pay < 0.3 else "b_walk", "hard", (0, 0.5), outfit="street", note=pay < 0.3)
    cut(k, [(120, 560), (420, 560), (660, 960), (-120, 960)], DESK, shadow=False, lw=3)    # the desk, from her side
    g = cairo.LinearGradient(0, 560, 0, 960); g.add_color_stop_rgba(0, 0, 0, 0, 0.2); g.add_color_stop_rgba(1, 1, 1, 1, 0.25)
    c.set_source(g); c.rectangle(-120, 560, 780, 400); c.fill()
    if cards:
        spread(k, 250, 700, 1.7, 1, 0.5)
    if pay >= 0.3:                                           # the hundred, on the desk, coming to her
        u = (pay - 0.3) / 0.7
        b.banknote(k, 270, _lerp(600.0, 800.0, u), _lerp(0.9, 2.2, u), 0.08, 3)
    q.coupe(k, 460, 880, 2.0)                                # from her side the two change places: the coupe at her right hand
    rect(k, 36, 852, 124, 30, (0.10, 0.10, 0.11), 6, shadow=False, lw=2.6)                 # the button, at her left
    ellipse(k, 98, 850, 38, 17, (0.55, 0.55, 0.56), 7, shadow=False, lw=2.8)
    if take > 0:                                             # her hand, rings up, over the note
        hy = _lerp(1040.0, 820.0, take)
        rect(k, 200, hy + 50, 150, 200, (0.10, 0.10, 0.11), 8, shadow=False, lw=3)
        rect(k, 190, hy + 30, 170, 36, (0.84, 0.84, 0.86), 9, shadow=False, lw=2.4)
        ellipse(k, 275, hy, 70, 54, SKIN, 10, shadow=False, lw=3)
        for i, dx in enumerate((-44, -15, 14, 43)):
            rect(k, 275 + dx - 10, hy - 92, 20, 56, SKIN, 11 + i, shadow=False, lw=2.4)
            if i in (1, 2):
                rect(k, 275 + dx - 12, hy - 62, 24, 13, (0.86, 0.87, 0.90), 15 + i, shadow=False, lw=1.6)
    csh.noir(s)
    return s
