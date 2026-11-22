"""Props and the second set of "Daddy's Home" (episode 12). Nothing here changes an older module: the chair and the
coffee machine go onto the front desk through the scene's own hooks (back / extra), so episodes 10 and 11 draw as before.
- ceo_chair(k, x, feet, s): the money. Black leather, deep buttons, a gold frame with a crest, gold arms, a star base
  on casters (it rolls: 2.3, 2.5). Too big for the room on purpose.
- coffee_machine(k, x, base, s, state, t): on the counter by Pam. "broken" (dark, OUT OF ORDER taped on), "rattle"
  (it shakes, the gauge in the red), "pop" (the lid jumps, the burst), "ok" (a green light, steam).
- wet_filter(k, x, y, s, ang): the filter in the air or on Don's head, coffee running from it.
- booth(k, phone=True): the club booth, a whole 540x960 frame: red neon, velvet, a bodyguard's sleeve holding the phone,
  Father's hand with the ring, his cuff and chin. Never his face.
- dad_phone(k, lit): frame 0 and the last frame, one drawing.
- star_screen(k, x, y, w, green): CUSTOMER SATISFACTION, one star, red or green.
  python3 dh_props.py sheet -> ../daddys-home/dh_props_v1.png
  python3 dh_props.py set   -> ../daddys-home/dh_set_v5_test.png (the front desk with the chair and the machine)"""
import math
import sys
import cairo
import kit
import dh_cast as dc
from kit import Ctx, INK, cut, rect, ellipse

LEATHER, LEATHER_L = (0.12, 0.10, 0.10), (0.24, 0.20, 0.19)
GOLD, GOLD_D, GOLD_L = (0.90, 0.72, 0.26), (0.62, 0.46, 0.12), (1.0, 0.90, 0.55)
STEEL, STEEL_D = (0.78, 0.80, 0.84), (0.50, 0.52, 0.57)
MACH, MACH_D = (0.72, 0.16, 0.14), (0.50, 0.09, 0.08)
COFFEE, COFFEE_D = (0.36, 0.22, 0.12), (0.22, 0.12, 0.06)
NEON = (1.0, 0.16, 0.30)
RED, GRN = (0.86, 0.14, 0.14), (0.16, 0.66, 0.30)


def _T(c, s, x, y, size, col=INK, bold=True, center=True):
    c.select_font_face("Inter", 0, 1 if bold else 0); c.set_font_size(size)
    e = c.text_extents(s); c.set_source_rgb(*col)
    c.move_to(x - (e.x_advance / 2 if center else 0), y); c.show_text(s)


def ceo_chair(k, x, feet, s=1.0, seed=2000, lean=0.0):
    """(x, feet): the middle of its base on the floor. About 300 units tall at s=1: a head taller than Don at his scale."""
    c = k.c
    c.save(); c.translate(x, feet); c.scale(s, s)
    for a in (-1, -0.5, 0.5, 1):                                             # the star base, gold, and its casters
        ex = a * 62
        c.set_source_rgb(*INK); c.set_line_width(9); c.set_line_cap(1); c.move_to(0, -26); c.line_to(ex, -10); c.stroke()
        c.set_source_rgb(*GOLD); c.set_line_width(5.5); c.move_to(0, -26); c.line_to(ex, -10); c.stroke()
        ellipse(k, ex, -6, 8, 7, (0.08, 0.08, 0.09), seed + int(a * 10), shadow=False, lw=1.8)
    rect(k, -7, -78, 14, 54, GOLD_D, seed + 1, shadow=False, lw=2)           # the column
    c.rotate(lean)
    cut(k, [(-70, -96), (70, -96), (64, -76), (-64, -76)], LEATHER, lw=2.4)   # the seat
    cut(k, [(-70, -96), (70, -96), (66, -106), (-66, -106)], LEATHER_L, shadow=False, lw=1.8)
    # the back: tall, winged, a gold frame
    back = [(-62, -100), (-74, -210), (-66, -290), (-30, -322), (0, -328), (30, -322), (66, -290), (74, -210), (62, -100)]
    cut(k, back, GOLD, lw=2.6)
    inner = [(px * 0.86, -100 + (py + 100) * 0.955) for px, py in back]
    cut(k, inner, LEATHER, shadow=False, lw=2)
    c.set_source_rgb(*LEATHER_L); c.set_line_width(1.6)                      # deep buttons, in diamonds
    for row, yy in enumerate(range(-290, -110, 36)):
        for col in range(-2, 3):
            bx = col * 24 + (12 if row % 2 else 0)
            if abs(bx) < 52 - (8 if yy < -270 else 0):
                c.move_to(bx - 12, yy + 18); c.line_to(bx, yy); c.line_to(bx + 12, yy + 18); c.stroke()
                c.set_source_rgb(*GOLD); c.arc(bx, yy, 2.6, 0, 2 * math.pi); c.fill(); c.set_source_rgb(*LEATHER_L)
    cut(k, [(-22, -326), (-28, -352), (-12, -340), (0, -360), (12, -340), (28, -352), (22, -326)], GOLD, shadow=False, lw=2.2)   # the crest: a crown
    for dx in (-28, 0, 28):
        ellipse(k, dx, -354 if dx else -362, 3.6, 3.6, (0.62, 0.05, 0.12), seed + 20 + dx, shadow=False, lw=1.2)
    for sx in (-1, 1):                                                       # the arms: gold, padded
        cut(k, [(sx * 66, -106), (sx * 84, -108), (sx * 86, -160), (sx * 74, -164)], GOLD, shadow=False, lw=2.2)
        cut(k, [(sx * 60, -168), (sx * 96, -168), (sx * 98, -152), (sx * 62, -152)], LEATHER, lw=2.2)
        c.set_source_rgba(*GOLD_L, 0.9); c.set_line_width(2); c.move_to(sx * 78, -114); c.line_to(sx * 80, -150); c.stroke()
    c.set_source_rgba(*GOLD_L, 0.9); c.set_line_width(2.4)                    # the frame catching the light
    c.move_to(-68, -214); c.curve_to(-64, -262, -54, -296, -28, -314); c.stroke()
    c.restore()
    return {"arm": (x + 79 * s, feet - 168 * s), "seat": (x, feet - 106 * s), "top": feet - 362 * s}


def wet_filter(k, x, y, s=1.0, ang=0.0, seed=2100, drips=True):
    """A used paper filter, open side down: a brown fluted disc, grounds, coffee running off it."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    pts = []
    for i in range(24):
        a = 2 * math.pi * i / 24
        r_ = 30 + (3.5 if i % 2 else -1.5)
        pts.append((math.cos(a) * r_, math.sin(a) * r_ * 0.42))
    cut(k, pts, (0.80, 0.68, 0.50), lw=2.2)
    ellipse(k, 0, -1, 20, 7.5, COFFEE, seed + 1, shadow=False, lw=1.6)
    c.set_source_rgb(*COFFEE_D)
    for dx, dy in ((-9, -2), (4, 1), (11, -3), (-2, 3)):
        c.arc(dx, dy - 1, 1.6, 0, 2 * math.pi); c.fill()
    if drips:
        c.set_source_rgb(*COFFEE); c.set_line_width(4.5); c.set_line_cap(1)
        for dx, ln in ((-22, 12), (16, 20), (27, 8)):
            c.move_to(dx, 8); c.line_to(dx + 1, 8 + ln); c.stroke()
            c.arc(dx + 1, 8 + ln, 3.2, 0, 2 * math.pi); c.fill()
    c.restore()


def coffee_machine(k, x, base, s=1.0, state="broken", t=0.0, seed=2200):
    """(x, base): the middle of its foot on the counter. t: seconds, for the shake and the steam."""
    c = k.c
    dx = dy = 0.0
    if state == "rattle":
        dx, dy = math.sin(t * 61) * 2.4, math.cos(t * 47) * 1.8
    c.save(); c.translate(x + dx * s, base + dy * s); c.scale(s, s)
    rect(k, -44, -8, 88, 8, STEEL_D, seed, shadow=False, lw=2)                # the drip tray
    cut(k, [(-48, -8), (48, -8), (46, -96), (-46, -96)], MACH, lw=2.4)        # the body
    rect(k, -40, -58, 80, 44, (0.16, 0.15, 0.16), seed + 1, shadow=False, lw=2)   # the bay
    rect(k, -13, -60, 26, 14, STEEL, seed + 2, shadow=False, lw=1.8)          # the group head
    rect(k, -3, -46, 6, 9, STEEL_D, seed + 3, shadow=False, lw=1.4)
    lid = -18 if state == "pop" else 0
    c.save(); c.translate(0, lid); c.rotate(-0.22 if state == "pop" else 0)
    cut(k, [(-50, -96), (50, -96), (44, -112), (-44, -112)], MACH_D, shadow=False, lw=2.2)   # the lid
    c.restore()
    ellipse(k, 28, -78, 10, 10, (0.96, 0.95, 0.90), seed + 4, shadow=False, lw=1.8)          # the gauge
    ga = {"broken": 2.6, "rattle": -0.2 + math.sin(t * 30) * 0.15, "pop": -0.4, "ok": 1.3}[state]
    c.set_source_rgb(*RED); c.set_line_width(2.2); c.set_line_cap(1)
    c.move_to(28, -78); c.line_to(28 + math.cos(ga) * 8, -78 - abs(math.sin(ga)) * 8); c.stroke()
    lamp = {"broken": (0.25, 0.25, 0.27), "rattle": RED, "pop": RED, "ok": GRN}[state]
    ellipse(k, -30, -80, 5.5, 5.5, lamp, seed + 5, shadow=False, lw=1.6)
    if state in ("ok", "rattle", "pop"):
        c.set_source_rgba(*lamp, 0.35); c.arc(-30, -80, 10, 0, 2 * math.pi); c.fill()
    if state == "broken":                                                    # the note, taped on, a little crooked
        c.save(); c.translate(0, -36); c.rotate(-0.07)
        rect(k, -34, -15, 68, 30, (0.99, 0.98, 0.92), seed + 6, lw=1.8)
        _T(c, "OUT OF", 0, -2, 11.5); _T(c, "ORDER", 0, 10.5, 11.5)
        c.set_source_rgba(0.85, 0.80, 0.55, 0.9); c.rectangle(-8, -19, 16, 7); c.fill()
        c.restore()
    if state == "pop":                                                       # the burst
        c.set_source_rgb(*INK); c.set_line_width(2.6)
        for a in (-2.6, -2.2, -1.8, -1.35, -0.95, -0.55):
            c.move_to(math.cos(a) * 26, -112 + math.sin(a) * 18); c.line_to(math.cos(a) * 48, -112 + math.sin(a) * 40); c.stroke()
        c.set_source_rgb(*COFFEE)
        for qx, qy in ((-30, -150), (22, -158), (40, -132), (-12, -168)):
            c.arc(qx, qy, 3.4, 0, 2 * math.pi); c.fill()
    if state == "ok":                                                        # steam, rising
        c.set_source_rgba(1, 1, 1, 0.8); c.set_line_width(4); c.set_line_cap(1)
        for i, sx_ in enumerate((-10, 6, 20)):
            ph = t * 3 + i
            c.move_to(sx_, -118); c.curve_to(sx_ + 8 * math.sin(ph), -134, sx_ - 8 * math.sin(ph), -150, sx_ + 4, -168); c.stroke()
    c.restore()


def star_screen(k, x, y, w, green=False, seed=2300):
    """The robot's screen, as an insert or in a shot: CUSTOMER SATISFACTION and five stars, one filled."""
    c = k.c
    h = w * 0.62
    rect(k, x - w / 2, y - h / 2, w, h, (0.07, 0.09, 0.13), seed, lw=2.4)
    _T(c, "CUSTOMER SATISFACTION", x, y - h * 0.26, w * 0.062, col=(0.80, 0.88, 0.95))
    col = GRN if green else RED
    for i in range(5):
        cx_, r_ = x + (i - 2) * w * 0.17, w * (0.105 if i == 0 else 0.062)
        c.new_path()
        for j in range(10):
            a = -math.pi / 2 + j * math.pi / 5
            rr = r_ if j % 2 == 0 else r_ * 0.45
            (c.move_to if j == 0 else c.line_to)(cx_ + math.cos(a) * rr, y + h * 0.10 + math.sin(a) * rr)
        c.close_path()
        if i == 0:
            c.set_source_rgb(*col); c.fill_preserve()
        c.set_source_rgb(*(col if i == 0 else (0.45, 0.50, 0.58))); c.set_line_width(max(1.5, w * 0.008)); c.stroke()


def dad_phone(k, lit=True, seed=2400, buzz=0.0):
    """Frame 0 and the last frame (540x960): the phone on the gold arm of the chair, DAD."""
    c = k.c
    c.set_source_rgb(*LEATHER); c.paint()
    cut(k, [(-20, 250), (560, 190), (560, 800), (-20, 860)], GOLD, lw=3)                  # the arm, gold
    cut(k, [(-20, 300), (560, 240), (560, 740), (-20, 800)], LEATHER_L, shadow=False, lw=2.6)   # its leather pad
    c.set_source_rgb(*GOLD)
    for i in range(6):
        c.arc(40 + i * 92, 318 - i * 9.5, 6, 0, 2 * math.pi); c.fill()
    c.save(); c.translate(270 + buzz * 5, 520 - buzz * 3); c.rotate(-0.10 + buzz * 0.02)
    rect(k, -130, -230, 260, 460, (0.06, 0.06, 0.08), seed, lw=3)
    if lit:
        c.set_source_rgb(0.10, 0.12, 0.17); c.rectangle(-118, -216, 236, 432); c.fill()
        ellipse(k, 0, -92, 56, 56, dc.VELVET, seed + 1, shadow=False, lw=2.4)              # his contact picture: the ring, no face
        dc.ring(k, 0, -90, 2.6, seed + 2)
        _T(c, "DAD", 0, 44, 86, col=(1, 1, 1))
        _T(c, "calling…", 0, 84, 26, col=(0.70, 0.76, 0.84), bold=False)
        ellipse(k, -62, 160, 30, 30, RED, seed + 4, shadow=False, lw=2.2)
        ellipse(k, 62, 160, 30, 30, GRN, seed + 5, shadow=False, lw=2.2)
    else:
        c.set_source_rgb(0.03, 0.03, 0.04); c.rectangle(-118, -216, 236, 432); c.fill()
    c.restore()
    if lit:                                                                               # buzz marks
        c.set_source_rgb(*GOLD_L); c.set_line_width(5); c.set_line_cap(1)
        for sx in (-1, 1):
            for i in range(2):
                c.arc(270, 520, 196 + i * 24, (0 if sx > 0 else math.pi) - 0.28, (0 if sx > 0 else math.pi) + 0.28); c.stroke()


def booth(k, seed=2500, tap=0.0, face_down=False):
    """The club booth (0.3, 0.5, 0.7), 540x960. Faces stay out: the frame cuts Father at the chin."""
    c = k.c
    g = cairo.LinearGradient(0, 0, 0, 960); g.add_color_stop_rgb(0, 0.10, 0.02, 0.05); g.add_color_stop_rgb(1, 0.03, 0.01, 0.03)
    c.set_source(g); c.paint()
    for yy, a in ((150, 0.9), (196, 0.55)):                                               # neon, two tubes and their glow
        for wd, al in ((26, 0.10), (14, 0.22), (5, a)):
            c.set_source_rgba(*NEON, al); c.set_line_width(wd); c.set_line_cap(1)
            c.move_to(30, yy); c.line_to(300, yy); c.curve_to(350, yy, 350, yy + 70, 400, yy + 70); c.line_to(520, yy + 70); c.stroke()
    cut(k, [(-10, 330), (550, 330), (550, 640), (-10, 640)], (0.36, 0.05, 0.11), lw=3)    # the banquette's back, velvet
    c.set_source_rgba(0.20, 0.02, 0.06, 1); c.set_line_width(3)
    for xx in range(40, 540, 90):
        c.move_to(xx, 336); c.line_to(xx, 634); c.stroke()
        c.set_source_rgb(*GOLD_D); c.arc(xx, 420, 5, 0, 2 * math.pi); c.fill(); c.arc(xx, 540, 5, 0, 2 * math.pi); c.fill()
        c.set_source_rgba(0.20, 0.02, 0.06, 1)
    # Father: the frame cuts him at the chin. Velvet shoulders, the black shirt, the chain
    cut(k, [(170, 120), (370, 120), (372, 250), (168, 250)], dc.SKIN_F, shadow=False, lw=0, outline=False)
    c.set_source_rgb(*dc.SKIN_F); c.new_path(); c.arc(270, 40, 118, 0.25, math.pi - 0.25); c.fill()   # the chin, coming into frame
    c.set_source_rgb(*INK); c.set_line_width(3); c.new_path(); c.arc(270, 40, 118, 0.45, math.pi - 0.45); c.stroke()
    c.set_line_width(4); c.move_to(238, 96); c.line_to(302, 96); c.stroke()               # the mouth: level
    cut(k, [(40, 300), (150, 210), (390, 210), (500, 300), (540, 700), (0, 700)], dc.VELVET, lw=3)
    cut(k, [(210, 212), (330, 212), (310, 700), (230, 700)], dc.BLACK, shadow=False, lw=2.4)
    cut(k, [(270, 330), (226, 206), (314, 206)], dc.SKIN_F, shadow=False, lw=2.2)
    for sx in (-1, 1):
        cut(k, [(270 + sx * 44, 206), (270 + sx * 96, 214), (270 + sx * 74, 300), (270 + sx * 10, 350)], dc.BLACK_L, shadow=False, lw=2.2)
        cut(k, [(270 + sx * 60, 250), (270 + sx * 150, 220), (270 + sx * 120, 480), (270 + sx * 40, 700)], dc.VELVET_D, shadow=False, lw=2.4)
    c.set_source_rgb(*GOLD_D); c.set_line_width(12); c.set_line_cap(1)
    c.move_to(236, 214); c.curve_to(246, 300, 294, 300, 304, 214); c.stroke()
    c.set_source_rgb(*GOLD); c.set_line_width(7); c.set_dash([9, 6]); c.move_to(236, 214); c.curve_to(246, 300, 294, 300, 304, 214); c.stroke(); c.set_dash([])
    rect(k, -10, 700, 560, 270, (0.07, 0.04, 0.05), seed + 1, lw=3)                       # the table: black glass
    c.set_source_rgba(*NEON, 0.16); c.rectangle(0, 706, 540, 10); c.fill()
    # the bodyguard's sleeve, from the left, holding the phone to him
    cut(k, [(-20, 600), (150, 640), (140, 730), (-20, 720)], dc.SUIT, lw=3)
    cut(k, [(140, 642), (172, 650), (164, 728), (132, 722)], (0.96, 0.96, 0.93), shadow=False, lw=2.2)
    c.save(); c.translate(262, 560 if not face_down else 668); c.rotate(0.08 if not face_down else 0.0); c.scale(1.7, 1.7)
    if face_down:
        rect(k, -66, -30, 132, 60, (0.10, 0.10, 0.12), seed + 3, lw=2.6)
    else:
        rect(k, -66, -112, 132, 224, (0.06, 0.06, 0.08), seed + 3, lw=2.6)
        c.set_source_rgb(0.97, 0.97, 0.95); c.rectangle(-58, -100, 116, 200); c.fill()
        _T(c, "10 GARAGES", -50, -78, 13, center=False)
        for i in range(5):                                                                # one star
            cx_ = -42 + i * 21
            c.new_path()
            for j in range(10):
                a = -math.pi / 2 + j * math.pi / 5
                rr = 10 if j % 2 == 0 else 4.5
                (c.move_to if j == 0 else c.line_to)(cx_ + math.cos(a) * rr, -52 + math.sin(a) * rr)
            c.close_path()
            if i == 0:
                c.set_source_rgb(*RED); c.fill_preserve()
            c.set_source_rgb(*(RED if i == 0 else (0.6, 0.6, 0.62))); c.set_line_width(1.6); c.stroke()
        _T(c, "They lost my", -50, -22, 12.5, center=False, bold=False); _T(c, "blueprint.", -50, -6, 12.5, center=False, bold=False)
        c.set_source_rgb(0.90, 0.93, 0.97); c.rectangle(-52, 12, 104, 60); c.fill()
        _T(c, "UptimeZ:", -46, 30, 11, center=False)
        _T(c, "Shut off!", -46, 48, 16, col=RED, center=False); _T(c, "Our AI does not lose files!", -46, 63, 7.6, center=False)
    c.restore()
    ellipse(k, 150, 690, 40, 34, (0.90, 0.69, 0.55), seed + 4, shadow=False, lw=2.6)       # the guard's hand
    # Father's hand: on the table, the ring; one finger taps the post
    hx, hy = 410, 700
    cut(k, [(560, 640), (470, 650), (462, 742), (560, 760)], dc.VELVET, lw=3)
    cut(k, [(472, 652), (444, 656), (438, 738), (464, 742)], (0.96, 0.96, 0.93), shadow=False, lw=2.2)
    ellipse(k, hx, hy, 46, 38, dc.SKIN_F, seed + 6, shadow=False, lw=2.6)
    for i, ln in enumerate((50, 58, 54, 44)):
        up = (14 * tap if i == 0 else 0)
        c.save(); c.translate(hx - 28, hy - 26 + i * 17); c.rotate(-0.10 * tap if i == 0 else 0)
        rect(k, -ln, -8 - up, ln, 16, dc.SKIN_F, seed + 7 + i, shadow=False, lw=2.2)
        c.restore()
    c.save(); c.translate(hx - 46, hy + 9); c.rotate(math.pi / 2)
    dc.ring(k, 0, 0, 2.3, seed + 12)
    c.restore()


def sheet(out="../daddys-home/dh_props_v1.png"):
    Wd, Hd = 1900, 1120
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, Wd, Hd); c = cairo.Context(surf)
    c.set_source_rgb(*kit.WALL); c.paint()
    k = Ctx(c, 0)
    kit.text(k, "DADDY'S HOME · PROPS AND THE BOOTH · v1", Wd / 2, 44, 34, INK)

    def frame(fn, x, y, sc, title):
        c.save(); c.translate(x, y); c.scale(sc, sc); c.rectangle(0, 0, 540, 960); c.clip(); fn(Ctx(c, 0)); c.restore()
        c.set_source_rgb(*INK); c.set_line_width(3); c.rectangle(x, y, 540 * sc, 960 * sc); c.stroke()
        kit.text(k, title, x + 270 * sc, y + 960 * sc + 24, 17, INK, font=kit.MONO)
    frame(lambda q: dad_phone(q), 40, 90, 0.5, "0.1 = 11.7: DAD (frame 0)")
    frame(lambda q: booth(q), 350, 90, 0.5, "0.3: the booth. Never his face")
    frame(lambda q: booth(q, face_down=True), 660, 90, 0.5, "0.7: Today. (face down)")
    import don_v4 as dv
    c.set_source_rgb(*kit.FLOOR); c.rectangle(980, 520, 900, 60); c.fill()
    dv.don(k, 1060, 540, 0.60 * 1.5, "stand", "neutral", look=(1, 0))
    ceo_chair(k, 1250, 540, 0.60 * 1.5)
    kit.text(k, "the CEO chair, at Don's scale", 1160, 604, 17, INK, font=kit.MONO)
    star_screen(k, 1500, 200, 300, green=False); star_screen(k, 1500, 420, 300, green=True)
    kit.text(k, "3.1 → 3.3: it turns green", 1500, 548, 17, INK, font=kit.MONO)
    wet_filter(k, 1770, 250, 2.0); kit.text(k, "the wet filter", 1770, 380, 17, INK, font=kit.MONO)
    rect(k, 60, 990, 1500, 26, (0.55, 0.38, 0.24), 2900, lw=2.4)
    for i, (st_, lab) in enumerate((("broken", "broken"), ("rattle", "7.2: it rattles"), ("pop", "POP"), ("ok", "fixed"))):
        coffee_machine(k, 260 + i * 380, 990, 2.3, st_, t=0.4)
        kit.text(k, lab, 260 + i * 380, 1050, 17, INK, font=kit.MONO)
    dv.don(k, 1730, 1010, 0.60 * 1.7, "stand", "neutral", look=(0, 0))
    wet_filter(k, 1730, 1010 - 0.60 * 1.7 * (336 - 78 + 44 + 46), 1.25, -0.12)
    kit.text(k, "7.3 → 8.2: on his head", 1730, 1050, 17, INK, font=kit.MONO)
    surf.write_to_png(out); print("wrote", out)


def set_test(out="../daddys-home/dh_set_v5_test.png"):
    """The front desk with the chair in zone B and the machine on the counter in zone C, through the scene's hooks."""
    import cs_board as cb
    import cs_scene1 as s1
    import fs_storyboard as sb
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1080, 1920); c = cairo.Context(surf); c.scale(2, 2)
    k = Ctx(c, 0)

    def back(k_):
        import cs_cal
        cs_cal.wall(k_, cs_cal.FRI)
        ceo_chair(k_, CHAIR[0], CHAIR[1], CHAIR[2])

    def extra(k_, o):
        coffee_machine(k_, MACHINE[0], MACHINE[1], MACHINE[2], "broken")
    cb.S(k, (590, 575, 1.0), auto=False, back=back, extra=extra, portrait="hang",
         **cb.base(cl=False, sf=False, dn=cb.at("don", face="neutral", look=(1, 0))))
    surf.write_to_png(out); print("wrote", out)


CHAIR = (452, 800 + 8, 0.60)                               # zone B, on Don's mark under the portrait: he sits in it, or stands before it
MACHINE = (770, 800 - 166, 0.62)                           # on the counter top, at Pam's elbow


if __name__ == "__main__":
    {"sheet": sheet, "set": set_test}[sys.argv[1] if len(sys.argv) > 1 else "sheet"]()
