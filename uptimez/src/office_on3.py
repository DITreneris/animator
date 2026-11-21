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
    elif sym == "tower2":                                    # the Tower, struck: its top going over, a bolt
        c.set_source_rgb(*INK); c.rectangle(-7, -6, 13, 26); c.fill()
        c.save(); c.translate(6, -6); c.rotate(0.55); c.rectangle(-13, -12, 13, 11); c.fill()
        for dx in (-13, -8, -3):
            c.rectangle(dx, -16, 3, 5); c.fill()
        c.restore()
        c.new_path(); c.move_to(-13, -22); c.line_to(-8, -22); c.line_to(-5, -15); c.line_to(-2, -15); c.line_to(-6, -3); c.line_to(-8, -11); c.line_to(-11, -11); c.close_path(); c.fill()   # the bolt, thick enough for a phone
    elif sym == "tower3":                                    # v5: a tower you know at a glance: stone courses, windows, a door, the crown knocked off, a thick bolt
        c.set_source_rgb(*INK)
        _p = lambda pts: (c.new_path(), c.move_to(*pts[0]), [c.line_to(*q_) for q_ in pts[1:]], c.close_path(), c.fill())
        _p([(-6.5, -7), (5.5, -7), (7.5, 20), (-8.5, 20)])                                   # the shaft, wider at the foot
        _p([(-10.5, 20), (9.5, 20), (9.5, 22.5), (-10.5, 22.5)])                             # the ground
        c.set_source_rgb(*q.CARD)
        c.rectangle(-2.2, 12.5, 3.6, 7.5); c.fill(); c.arc(-0.4, 12.5, 1.8, math.pi, 0); c.fill()   # the door
        for wy in (-3.5, 4.5):
            c.rectangle(-1.6, wy, 2.4, 4); c.fill()                                          # windows
        c.set_line_width(0.5)
        for ly in (0.5, 8.5):
            c.move_to(-7, ly); c.line_to(6.5, ly); c.stroke()                                # courses
        c.set_source_rgb(*INK)
        c.save(); c.translate(5, -10); c.rotate(0.6)                                         # the crown, going over
        c.rectangle(-8, -5, 13, 5); c.fill()
        for dx in (-8, -3.2, 1.6):
            c.rectangle(dx, -8.4, 3.4, 3.6); c.fill()
        c.restore()
        _p([(-12.5, -22.5), (-7.5, -22.5), (-5.2, -16), (-2.6, -16), (-5.4, -8), (-7.4, -13), (-10.2, -13)])   # the bolt
        for (fx, fy, fa) in ((-10.5, 4, 0.5), (10.5, 9, -0.6)):                               # stones, falling
            c.save(); c.translate(fx, fy); c.rotate(fa); c.rectangle(-1.6, -1.2, 3.2, 2.4); c.fill(); c.restore()
    else:
        c.move_to(-13, -23); c.line_to(13, 23); c.move_to(13, -23); c.line_to(-13, 23); c.stroke()
    c.restore()


def deck(k, x, y, s=1.0, sq=0.5, n=4):
    """v5 (Tomas: proceed, taken as option 1): only the deck lies on her desk until he has paid."""
    for j in range(n):
        card(k, x + j * 1.5 * s, y - j * 3 * s, s, 0.2, "back", sq)


def spread(k, x, y, s=1.0, side=1, sq=0.62, faces=("star", "tower", "gear")):
    """v2 (Tomas, 20 Nov: the desk looked empty): her tarot spread. Three cards face up in a row, the gear last, and
    the deck beside them. side: +1 as she sees it (the deck at her right), -1 from the other side of the desk."""
    for i, sym in enumerate(faces):
        if sym is None:
            continue
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


BACK2 = [False]                                              # v10, opt-in: his back redrawn (Tomas: "it looks strange there")


def _back2(k, c, glove_up):
    """His back as a back: a round hood, a neck, sloping shoulders, the hood's seam and its fold at the neck, a line of
    light down the side the window is on, and one arm that leaves his shoulder and ends in the glove. (v9 and before: a
    flat grey slab with a pointed top, and a forearm coming up from the frame's edge on its own.)"""
    gx, gy = 390, _lerp(900.0, 720.0, glove_up)
    cut(k, [(246, 640), (318, 668), (gx + 54, gy + 74), (gx - 44, gy + 92), (300, 800), (236, 760)], TRACK, shadow=False, lw=3.4)      # the arm, from his shoulder to the glove
    c.new_path(); c.move_to(-60, 980); c.line_to(-60, 610); c.curve_to(-44, 528, 6, 506, 30, 482)
    c.curve_to(-8, 440, -8, 298, 100, 284); c.curve_to(208, 298, 208, 440, 170, 482)
    c.curve_to(204, 504, 286, 528, 312, 640); c.line_to(322, 980); c.close_path()
    g = cairo.LinearGradient(-60, 0, 320, 0)
    g.add_color_stop_rgb(0, TRACK[0] * 0.95, TRACK[1] * 0.95, TRACK[2] * 0.95); g.add_color_stop_rgb(1, TRACK[0] * 1.55, TRACK[1] * 1.55, TRACK[2] * 1.55)
    c.set_source(g); c.fill_preserve(); c.set_source_rgb(0.05, 0.05, 0.06); c.set_line_width(4); c.stroke()
    c.set_source_rgb(0.12, 0.12, 0.14); c.set_line_width(3.4); c.set_line_cap(1)
    c.move_to(100, 290); c.curve_to(96, 360, 96, 420, 100, 500); c.stroke()                 # the hood's seam, crown to neck
    c.move_to(32, 484); c.curve_to(70, 520, 130, 520, 168, 484); c.stroke()                 # the hood, folded at the neck
    c.move_to(100, 520); c.line_to(104, 980); c.stroke()                                    # the back's seam
    c.set_line_width(2.4)
    for x0, y0, x1, y1 in ((-30, 600, 10, 640), (230, 600, 262, 650), (250, 700, 270, 760)):   # folds at the shoulders
        c.move_to(x0, y0); c.line_to(x1, y1); c.stroke()
    c.set_source_rgba(1, 1, 1, 0.62); c.set_line_width(7)                                   # light from the window, down his right side
    c.new_path(); c.move_to(118, 288); c.curve_to(204, 302, 204, 438, 168, 480); c.curve_to(202, 502, 282, 528, 308, 640); c.line_to(314, 760); c.stroke()
    c.set_line_cap(0)
    cut(k, [(gx - 46, gy + 60), (gx + 32, gy + 60), (gx + 36, gy + 78), (gx - 48, gy + 80)], (0.10, 0.10, 0.12), shadow=False, lw=2.6)   # the cuff


def over(glove_up=0.0, look=(0.2, 0.9), show=False, cards=False, v4=False):
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
    if cards == "deck":
        deck(k, 352, 596, 1.15)
    elif cards:                                              # cards="down": all three face down (before she turns one)
        spread(k, 372, 600, 1.15, -1, 0.5, faces=("back",) * 3 if cards == "down" else ("star", "tower", "gear"))
    if BACK2[0]:
        _back2(k, c, glove_up)
        gx, gy = 390, _lerp(900.0, 720.0, glove_up)
    else:
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
        (money if v4 else lambda *a: b.banknote(*a, 3))(k, gx - 96, gy - 64, 2.1 * (0.9 if v4 else 1), -0.16)
    csh.noir(s)
    return s


def reverse(pay=0.0, take=0.0, cards=False, turn=None, v4=False, eyes=None, v6=False, ticket=None, one=None):
    """M3, 4.4: her view. He is small, in his tracksuit, in front of the desk, the door behind him. pay 0..1: the note
    crosses the desk toward us. take 0..1: her ringed hand comes in from the near edge and covers it."""
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(s); k = Ctx(c, 0)
    g = cairo.RadialGradient(270, 300, 30, 270, 300, 620)
    g.add_color_stop_rgba(0, 0.62, 0.62, 0.62, 1); g.add_color_stop_rgba(1, 0.24, 0.24, 0.26, 1); c.set_source(g); c.paint()
    if v4:
        _door2(k)
    else:
        rect(k, 190, 110, 160, 400, (0.20, 0.20, 0.22), 3, shadow=False, lw=4)                 # the door he came in by
        rect(k, 206, 126, 128, 170, (0.74, 0.74, 0.72), 4, shadow=False, lw=2.4)               # its glass, lit from the stairs
        ellipse(k, 326, 330, 7, 7, (0.80, 0.80, 0.82), 5, shadow=False, lw=1.6)
    sc = 1.15 * b.REL
    c.save(); c.set_source_rgba(0, 0, 0, 0.3); c.translate(270, 560); c.scale(70, 12); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
    b.boxer(k, 270 - (40 if v4 else 0), 560, sc, "b_pay" if pay < 0.3 else "b_walk", "hard", eyes or (0, 0.5), outfit="street", note=pay < 0.3)
    cut(k, [(120, 560), (420, 560), (660, 960), (-120, 960)], DESK, shadow=False, lw=3)    # the desk, from her side
    g = cairo.LinearGradient(0, 560, 0, 960); g.add_color_stop_rgba(0, 0, 0, 0, 0.2); g.add_color_stop_rgba(1, 1, 1, 1, 0.25)
    c.set_source(g); c.rectangle(-120, 560, 780, 400); c.fill()
    if cards == "deck":
        deck(k, 400, 716, 1.7)
    elif cards and turn is None:
        spread(k, 250, 700, 1.7, 1, 0.5)
    elif cards and cards != "deck":                          # v3 (Tomas, /grill-me): three face down; she turns the last one
        spread(k, 250, 700, 1.7, 1, 0.5, faces=("back", "back", None))
    if pay >= 0.3:                                           # the hundred, on the desk, coming to her
        u = (pay - 0.3) / 0.7
        if v4 and take <= 0 and one is None:
            money(k, 270, _lerp(600.0, 800.0, u), _lerp(0.9, 2.2, u) * 0.92, 0.08)
        elif not v4:
            b.banknote(k, 270, _lerp(600.0, 800.0, u), _lerp(0.9, 2.2, u), 0.08, 3)
    q.coupe(k, 460, 880, 2.0)                                # from her side the two change places: the coupe at her right hand
    rect(k, 36, 852, 124, 30, (0.10, 0.10, 0.11), 6, shadow=False, lw=2.6)                 # the button, at her left
    ellipse(k, 98, 850, 38, 17, (0.55, 0.55, 0.56), 7, shadow=False, lw=2.8)
    if one is not None:
        _one(c, k, one, ticket if (ticket is not None and ticket < 0.62) else None)
    elif take > 0 and v4:
        _take(k, soft=cards == "deck")
    elif take > 0:                                           # her hand, rings up, over the note
        hy = _lerp(1040.0, 820.0, take)
        rect(k, 200, hy + 50, 150, 200, (0.10, 0.10, 0.11), 8, shadow=False, lw=3)
        rect(k, 190, hy + 30, 170, 36, (0.84, 0.84, 0.86), 9, shadow=False, lw=2.4)
        ellipse(k, 275, hy, 70, 54, SKIN, 10, shadow=False, lw=3)
        for i, dx in enumerate((-44, -15, 14, 43)):
            rect(k, 275 + dx - 10, hy - 92, 20, 56, SKIN, 11 + i, shadow=False, lw=2.4)
            if i in (1, 2):
                rect(k, 275 + dx - 12, hy - 62, 24, 13, (0.86, 0.87, 0.90), 15 + i, shadow=False, lw=1.6)
    if ticket is not None:                                   # v7 (Tomas: proceed): for the hundred she slides a fight ticket back across the desk to him
        fight_ticket(k, 150 - 10 * ticket, _lerp(880.0, 640.0, ticket), _lerp(2.3, 1.05, ticket), -0.10 + 0.04 * ticket)
    if cards == "deck" and turn is not None and one is None:
        _deal(c, k, turn, v6)
    elif cards and turn is not None:
        _turn(c, k, turn)
    csh.noir(s)
    return s


def money(k, x, y, s=1.0, ang=0.0):
    """v4, opt-in: the hundred drawn as money: a frame, a head in an oval, 100, a mark in each corner."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    cut(k, [(-40, -19), (40, -19), (40, 19), (-40, 19)], b.NOTE, lw=2)
    c.set_source_rgb(*INK); c.set_line_width(1.3); c.rectangle(-35, -14, 70, 28); c.stroke()
    c.save(); c.translate(-18, 0); c.scale(9, 11); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.stroke()
    c.arc(-18, -3, 3.4, 0, 2 * math.pi); c.fill(); c.rectangle(-23, 2, 10, 7); c.fill()
    kit.text(k, "100", 12, 0, 17, INK, bold=True)
    for sx in (-1, 1):
        for sy in (-1, 1):
            kit.text(k, "$", sx * 30 + (12 if sx < 0 else 0) * 0, sy * 9, 6.5, INK, bold=True)
    c.restore()


def _take(k, x=270, y=838, soft=False):
    """v4, opt-in: her hand has the note: fingers bent over its far edge, the thumb at its side, and it has come toward her."""
    c = k.c
    c.set_source_rgb(0.10, 0.10, 0.11); c.set_line_width(4); c.set_line_cap(1)                  # two marks where it was: it has moved
    for dx in (-50, 46):
        c.move_to(x + dx, y - 104); c.line_to(x + dx + 2, y - 76); c.stroke()
    c.set_line_cap(0)
    money(k, x, y - 8, 2.5, 0.05)
    rect(k, x - 70, y + 62, 150, 200, (0.10, 0.10, 0.11), 8, shadow=False, lw=3)                # her sleeve, her cuff
    rect(k, x - 80, y + 44, 170, 34, (0.84, 0.84, 0.86), 9, shadow=False, lw=2.4)
    ellipse(k, x + 4, y + 18, 66, 44, SKIN, 10, shadow=False, lw=3)                             # the back of her hand
    if soft:                                                 # v5: round fingers, closed over the note's far edge; no knuckle lines (they read as a robot's)
        for i, dx in enumerate((-42, -14, 14, 42)):
            ellipse(k, x + 4 + dx, y - 30, 13, 26 - (4 if i in (0, 3) else 0), SKIN, 11 + i, shadow=False, lw=2.6)
            if i in (1, 2):
                rect(k, x + 4 + dx - 14, y - 26, 28, 11, (0.86, 0.87, 0.90), 15 + i, shadow=False, lw=1.6)
        cut(k, [(x - 58, y + 10), (x - 96, y - 14), (x - 104, y + 6), (x - 66, y + 36)], SKIN, shadow=False, lw=2.6)
        return
    for i, dx in enumerate((-42, -14, 14, 42)):                                                 # fingers, bent: short, a knuckle, the tip gone over the edge
        rect(k, x + 4 + dx - 11, y - 54, 22, 44, SKIN, 11 + i, shadow=False, lw=2.4)
        c.set_source_rgb(*INK); c.set_line_width(2); c.move_to(x + 4 + dx - 9, y - 38); c.line_to(x + 4 + dx + 9, y - 38); c.stroke()
        if i in (1, 2):
            rect(k, x + 4 + dx - 13, y - 30, 26, 12, (0.86, 0.87, 0.90), 15 + i, shadow=False, lw=1.6)
    cut(k, [(x - 58, y + 10), (x - 96, y - 14), (x - 104, y + 6), (x - 66, y + 36)], SKIN, shadow=False, lw=2.6)   # the thumb, on the note's side


def _door2(k):
    """v4, opt-in: the door he came in by, to one side of him and ajar: a frame, the stairs' light in the gap and on the floor."""
    c = k.c
    rect(k, 330, 96, 150, 420, (0.14, 0.14, 0.16), 3, shadow=False, lw=4)                       # the frame
    rect(k, 342, 108, 126, 408, (0.90, 0.90, 0.86), 4, shadow=False, lw=2)                      # the stairs' light
    cut(k, [(380, 108), (474, 96), (478, 528), (380, 516)], (0.30, 0.30, 0.33), shadow=False, lw=3.4)   # the door, ajar
    ellipse(k, 394, 320, 7, 7, (0.80, 0.80, 0.82), 5, shadow=False, lw=1.6)
    c.set_source_rgba(1, 1, 1, 0.22); c.new_path(); c.move_to(342, 516); c.line_to(380, 516); c.line_to(330, 566); c.line_to(250, 566); c.close_path(); c.fill()


def fight_ticket(k, x, y, s=1.0, ang=0.0):
    """v7: what the hundred buys: a ticket, notched at both ends, a stub torn off. FIGHT, TONIGHT, No 1."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(1, 0.62); c.rotate(ang); c.scale(s, s)
    cut(k, [(-44, -20), (44, -20), (44, -7), (39, 0), (44, 7), (44, 20), (-44, 20), (-44, 7), (-39, 0), (-44, -7)], (0.97, 0.96, 0.90), lw=2)
    c.set_source_rgb(*INK); c.set_line_width(1.2); c.set_dash([3, 3]); c.move_to(22, -20); c.line_to(22, 20); c.stroke(); c.set_dash([])
    kit.text(k, "FIGHT", -10, -5, 15, INK, bold=True)
    kit.text(k, "TONIGHT", -10, 10, 7.5, INK, bold=True)
    kit.text(k, "1", 32, 0, 15, INK, bold=True)
    c.restore()


def ticket_insert(t=1.0):
    """4.4a, insert (v7): the ticket stops against his two gloves at the far edge of her desk. He cannot pick it up."""
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(s); k = Ctx(c, 0)
    c.set_source_rgb(*DESK); c.paint()
    g = cairo.RadialGradient(270, 420, 60, 270, 420, 760); g.add_color_stop_rgba(0, 1, 1, 1, 0.34); g.add_color_stop_rgba(1, 0, 0, 0, 0.42); c.set_source(g); c.paint()
    c.set_source_rgb(0.05, 0.05, 0.06); c.rectangle(0, 0, 540, 150); c.fill()                         # the desk's far edge; beyond it, him
    ty = _lerp(820.0, 400.0, t)
    c.save(); c.translate(270, ty); c.scale(1, 1 / 0.62); c.translate(-270, -ty)
    fight_ticket(k, 270, ty, 5.4, 0.04)
    c.restore()
    for side, gx in ((-1, 130), (1, 410)):                                                           # his gloves, down onto the desk's edge, either side of it
        gy = 170
        c.save(); c.translate(gx, gy); c.scale(3.4, 3.4); c.translate(-gx, -gy)
        b._glove(k, gx, gy, -side * 0.15, 0.98, side, 81 + side)
        c.restore()
    csh.noir(s)
    return s


def _her_hand(k, x, y, grip=False):
    """v8: her one hand, up from her edge of the desk to (x, y): the sleeve, the wide cuff, the back of the hand, round
    fingers, two rings."""
    c = k.c
    ax, ay = 300 + (x - 270) * 0.35, 1000
    d = math.hypot(x - ax, y - ay); ux, uy = (x - ax) / d, (y - ay) / d
    c.set_source_rgb(0.10, 0.10, 0.11); c.set_line_width(128); c.set_line_cap(0); c.move_to(ax, ay); c.line_to(x - ux * 92, y - uy * 92); c.stroke()
    c.set_source_rgb(0.84, 0.84, 0.86); c.set_line_width(142); c.move_to(x - ux * 94, y - uy * 94); c.line_to(x - ux * 60, y - uy * 60); c.stroke()
    ellipse(k, x - ux * 6, y - uy * 6, 62, 46, SKIN, 22, shadow=False, lw=3)
    for i, off in enumerate((-40, -13, 13, 40)):
        fx, fy = x + ux * (30 if grip else 44) - uy * off, y + uy * (30 if grip else 44) + ux * off
        c.save(); c.translate(fx, fy); c.rotate(math.atan2(uy, ux)); ellipse(k, 0, 0, 17 if grip else 25, 12, SKIN, 23 + i, shadow=False, lw=2.6)
        if i in (1, 2):
            rect(k, -15, -13, 12, 26, (0.86, 0.87, 0.90), 28 + i, shadow=False, lw=1.6)
        c.restore()


def _one(c, k, u, push=None):
    """v8 (Tomas, /grill-me): one hand does all of it, so nobody asks whose the second is. u 0..1: it comes down on the
    hundred. 1..2: it pushes the hundred under the foot of her coupe and lets go. 2..3: to the deck; the top card to the
    middle of the desk, face down. 3..4: it turns the card: the Tower; the hand lies beside it."""
    N0, N1 = (270, 800), (438, 906)                          # the note: where he left it; under the coupe
    D, M = (400, 716), (250, 716)                            # the deck; the middle of the desk
    f = lambda a, b_, t: (_lerp(float(a[0]), float(b_[0]), t), _lerp(float(a[1]), float(b_[1]), t))
    if u < 2:
        t = max(0.0, u - 1)
        nx, ny = f(N0, N1, t)
        money(k, nx, ny, _lerp(2.02, 1.5, t), 0.08 + 0.3 * t)
    else:
        money(k, N1[0], N1[1], 1.5, 0.38)
    if u >= 1.6:                                             # the coupe stands on it
        q.coupe(k, 460, 880, 2.0)
    if u < 1:
        hx, hy = f((300, 1010), (N0[0] + 6, N0[1] + 52), u); grip = False
    elif u < 2:
        hx, hy = f((N0[0] + 6, N0[1] + 52), (N1[0] - 30, N1[1] + 30), u - 1); grip = True
    elif u < 3:
        t = u - 2
        if t < 0.4:
            hx, hy = f((N1[0] - 30, N1[1] + 30), (D[0] + 20, D[1] + 60), t / 0.4)
        else:
            hx, hy = f((D[0] + 20, D[1] + 60), (M[0] + 30, M[1] + 62), (t - 0.4) / 0.6)
            card(k, hx - 30, hy - 62, 1.7, 0.15, "back", 0.5)
        grip = True
    else:
        t = u - 3
        if t < 0.5:
            card(k, M[0], M[1] - 10 * t, 1.7, 0.10, "back", 0.5 * (1 - 1.6 * t))
        else:
            v = (t - 0.5) / 0.5
            card(k, M[0], M[1], 1.9 + 0.5 * math.sin(math.pi * v), 0.04, "tower3", 0.5 * (0.25 + 0.75 * v))
        hx, hy = f((M[0] + 30, M[1] + 62), (M[0] + 120, M[1] + 110), max(0.0, t - 0.6) / 0.4); grip = False
    if push is not None:                                     # v9: the same hand pushes the ticket out to him, and comes back
        hx, hy, grip = 150 - 10 * push + 34, _lerp(880.0, 640.0, push) + 78, True
    _her_hand(k, hx, hy, grip)


def _deal(c, k, t, hers=False):
    """v5: the hundred is hers; now her other hand takes the top card off the deck, lays it in the middle of the desk
    (t 0..0.5, face down) and turns it (0.5..1): the Tower."""
    cx, cy = 250, 716
    if t <= 0:
        return
    u = min(t / 0.5, 1.0)
    px, py = _lerp(400.0, cx, u), cy - 26 * math.sin(math.pi * u)
    if t < 0.5:
        card(k, px, py, 1.7, 0.2 * (1 - u), "back", 0.5)
    else:
        v = (t - 0.5) / 0.5
        card(k, cx, cy, 1.9 + 0.5 * math.sin(math.pi * v), 0.04, "tower3", 0.5 * (0.25 + 0.75 * v))
    hx, hy = (px + 70, py) if t < 0.5 else (cx + 76 + 40 * max(0.0, t - 0.75) / 0.25, cy - 2)
    if hers:                                                 # v6: plainly her other hand: up from her edge of the desk, the same wide cuff, the same rings
        ax, ay = 470, 990
        d = math.hypot(hx - ax, hy - ay); ux, uy = (hx - ax) / d, (hy - ay) / d
        c.set_source_rgb(0.10, 0.10, 0.11); c.set_line_width(120); c.set_line_cap(0); c.move_to(ax, ay); c.line_to(hx - ux * 96, hy - uy * 96); c.stroke()
        c.set_source_rgb(0.84, 0.84, 0.86); c.set_line_width(134); c.move_to(hx - ux * 98, hy - uy * 98); c.line_to(hx - ux * 62, hy - uy * 62); c.stroke()
        c.set_source_rgb(*INK); c.set_line_width(2.4)
        ellipse(k, hx - ux * 8, hy - uy * 8, 58, 44, SKIN, 22, shadow=False, lw=3)
        for i, off in enumerate((-36, -12, 12, 36)):
            fx, fy = hx + ux * 40 - uy * off, hy + uy * 40 + ux * off
            c.save(); c.translate(fx, fy); c.rotate(math.atan2(uy, ux)); ellipse(k, 0, 0, 24, 11, SKIN, 23 + i, shadow=False, lw=2.6)
            if i in (1, 2):
                rect(k, -16, -12, 12, 24, (0.86, 0.87, 0.90), 28 + i, shadow=False, lw=1.6)
            c.restore()
        return
    c.set_source_rgb(0.10, 0.10, 0.11); c.set_line_width(46); c.set_line_cap(0); c.move_to(640, hy + 70); c.line_to(hx + 60, hy + 8); c.stroke()
    rect(k, hx + 30, hy - 16, 34, 44, (0.84, 0.84, 0.86), 21, shadow=False, lw=2.4)
    ellipse(k, hx, hy + 4, 34, 24, SKIN, 22, shadow=False, lw=3)
    for i, dy in enumerate((-12, 2, 16)):
        ellipse(k, hx - 40, hy + dy, 20, 7.5, SKIN, 23 + i, shadow=False, lw=2.2)
    rect(k, hx - 30, hy - 4, 12, 17, (0.86, 0.87, 0.90), 27, shadow=False, lw=1.6)


def _turn(c, k, t):
    """4.4, its end: her other hand comes in from the right and turns the last card: the Tower. She does not look up
    (this is her view). t 0: face down. 0..0.5: the hand comes, the card's edge lifts. 0.5..1: it goes over, larger
    for a moment, and lies face up; the hand rests beside it."""
    cx, cy = 250 + 46 * 1.7, 700
    if t <= 0:
        card(k, cx, cy, 1.7, 0.10, "back", 0.5)
    elif t < 0.5:
        u = t / 0.5
        card(k, cx, cy - 10 * u, 1.7, 0.10, "back", 0.5 * (1 - 0.8 * u))      # seen thinner and thinner: its edge comes up
    else:
        u = (t - 0.5) / 0.5
        card(k, cx, cy - 10 * (1 - u), 1.7 + 0.9 * math.sin(math.pi * min(u, 1.0)) * 0.4 + 0.5, 0.06, "tower2", 0.5 * (0.2 + 0.8 * u))
    if t > 0:
        u = min(t / 0.5, 1.0)
        hx, hy = _lerp(620.0, cx + 74, u) + (30 * max(0.0, t - 0.75) / 0.25), cy - 4
        c.set_source_rgb(0.10, 0.10, 0.11); c.set_line_width(46); c.set_line_cap(0); c.move_to(640, hy + 60); c.line_to(hx + 60, hy + 8); c.stroke()   # her sleeve, from the right
        rect(k, hx + 30, hy - 16, 34, 44, (0.84, 0.84, 0.86), 21, shadow=False, lw=2.4)
        ellipse(k, hx, hy + 4, 34, 24, SKIN, 22, shadow=False, lw=3)
        for i, dy in enumerate((-12, 2, 16)):
            rect(k, hx - 58, hy + dy - 6, 34, 13, SKIN, 23 + i, shadow=False, lw=2.2)
        rect(k, hx - 30, hy - 4, 12, 17, (0.86, 0.87, 0.90), 27, shadow=False, lw=1.6)


def tower_insert(t=1.0, v5=False, one=False):
    """4.4b, insert (v3): the turned card, close, from above her hands. The Tower, struck. t < 1: her fingers still on
    its edge. Below it, the corner of the hundred under her other hand."""
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(s); k = Ctx(c, 0)
    c.set_source_rgb(*DESK); c.paint()
    g = cairo.RadialGradient(270, 380, 60, 270, 380, 760); g.add_color_stop_rgba(0, 1, 1, 1, 0.34); g.add_color_stop_rgba(1, 0, 0, 0, 0.42); c.set_source(g); c.paint()
    if v5:                                                   # one card, alone on the desk
        card(k, 262, 400, 10.4, 0.04, "tower3", 1.0)
    else:
        card(k, 96, 150, 5.2, -0.12, "back", 1.0); card(k, -40, 420, 5.2, 0.08, "back", 1.0)       # the two still face down
        card(k, 286, 400, 9.4, 0.05, "tower2", 1.0)
    if one:                                                  # v8: the hundred under the foot of her coupe; her one hand beside the card
        money(k, 120, 870, 3.6, 0.3)
        ellipse(k, 150, 838, 84, 20, (0.92, 0.92, 0.94), 30, shadow=True, lw=3)
        c.set_source_rgb(*INK); c.set_line_width(7); c.move_to(150, 838); c.line_to(150, 700); c.stroke()
    else:
        money(k, 150, 880, 3.8, 0.10)                                                        # the hundred, under her hand
        rect(k, 250, 880, 330, 150, (0.10, 0.10, 0.11), 30, shadow=False, lw=3)
        rect(k, 214, 868, 60, 120, (0.84, 0.84, 0.86), 31, shadow=False, lw=2.6)
        ellipse(k, 150, 930, 96, 66, SKIN, 32, shadow=False, lw=3.4)
    hx = _lerp(452.0, 520.0, t)                                                              # her other hand, leaving the card
    rect(k, hx + 54, 470, 120, 110, (0.10, 0.10, 0.11), 33, shadow=False, lw=3)
    rect(k, hx + 30, 462, 44, 124, (0.84, 0.84, 0.86), 34, shadow=False, lw=2.6)
    ellipse(k, hx, 524, 62, 50, SKIN, 35, shadow=False, lw=3.4)
    for i, dy in enumerate((-30, -4, 22)):
        rect(k, hx - 104, 524 + dy - 11, 62, 24, SKIN, 36 + i, shadow=False, lw=2.6)
    rect(k, hx - 60, 510, 20, 30, (0.86, 0.87, 0.90), 40, shadow=False, lw=2)
    csh.noir(s)
    return s


def button_insert(press=0.0):
    """5.4b / 7.4b, insert (v6): the button, close. Her ringed finger comes down on it; pressed, it lights and the
    light jumps outward. The cause of the tick, large enough for a phone."""
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(s); k = Ctx(c, 0)
    c.set_source_rgb(*DESK); c.paint()
    g = cairo.RadialGradient(270, 520, 40, 270, 520, 700); g.add_color_stop_rgba(0, 1, 1, 1, 0.20 + 0.5 * press); g.add_color_stop_rgba(1, 0, 0, 0, 0.5); c.set_source(g); c.paint()
    rect(k, 90, 520, 360, 110, (0.10, 0.10, 0.11), 3, shadow=True, lw=4)                             # the plate
    lit = press > 0.9
    ellipse(k, 270, 520 + 26 * press, 130, 58 - 20 * press, (0.98, 0.98, 0.94) if lit else (0.55, 0.55, 0.56), 4, shadow=False, lw=4)
    if lit:
        c.set_source_rgb(0.98, 0.98, 0.94); c.set_line_width(9); c.set_line_cap(1)
        for i in range(9):
            a = math.pi + math.pi * (i + 0.5) / 9
            c.move_to(270 + 170 * math.cos(a), 540 + 110 * math.sin(a)); c.line_to(270 + 240 * math.cos(a), 540 + 170 * math.sin(a)); c.stroke()
        c.set_line_cap(0)
    fy = _lerp(250.0, 500.0, min(press / 0.9, 1.0))                                                  # her finger, from above, a ring on it
    rect(k, 196, -40, 150, fy - 250 + 60, (0.10, 0.10, 0.11), 5, shadow=False, lw=3)
    rect(k, 184, fy - 250, 174, 40, (0.84, 0.84, 0.86), 6, shadow=False, lw=2.6)
    ellipse(k, 270, fy - 150, 80, 70, SKIN, 7, shadow=False, lw=3.4)
    rect(k, 246, fy - 110, 48, 118, SKIN, 8, shadow=False, lw=3)
    ellipse(k, 270, fy + 6, 24, 16, SKIN, 9, shadow=False, lw=3)
    rect(k, 242, fy - 70, 56, 22, (0.86, 0.87, 0.90), 10, shadow=False, lw=2)
    csh.noir(s)
    return s
