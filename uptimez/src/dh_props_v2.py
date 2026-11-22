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


def ceo_chair(k, x, feet, s=1.0, seed=2000, lean=0.0, sink=0.0, puff=False):
    """v2 (after the props review): a throne. The back a quarter wider and taller, a few big buttons, ONE big crown, and
    a height lever with a red knob. sink 0..1: the gas lift lets go and the seat drops 46 units (frame 0: DAD rings, he
    jolts, PSSSH). puff: the air coming out. (x, feet): the middle of its base on the floor."""
    c = k.c
    c.save(); c.translate(x, feet); c.scale(s, s)
    for a in (-1, -0.5, 0.5, 1):                                             # the star base, gold, and its casters
        ex = a * 70
        c.set_source_rgb(*INK); c.set_line_width(10); c.set_line_cap(1); c.move_to(0, -26); c.line_to(ex, -10); c.stroke()
        c.set_source_rgb(*GOLD); c.set_line_width(6); c.move_to(0, -26); c.line_to(ex, -10); c.stroke()
        ellipse(k, ex, -6, 9, 8, (0.08, 0.08, 0.09), seed + int(a * 10), shadow=False, lw=1.8)
    drop = 46 * sink
    rect(k, -8, -78 + drop, 16, 54 - drop, GOLD_D, seed + 1, shadow=False, lw=2)             # the column, shorter as it sinks
    rect(k, -13, -34, 26, 12, STEEL_D, seed + 2, shadow=False, lw=1.8)
    c.translate(0, drop); c.rotate(lean)
    c.set_source_rgb(*INK); c.set_line_width(7); c.set_line_cap(1)           # the lever: far too big, a red knob
    c.move_to(46, -84); c.line_to(118, -70); c.stroke()
    c.set_source_rgb(*STEEL); c.set_line_width(4); c.move_to(46, -84); c.line_to(118, -70); c.stroke()
    ellipse(k, 122, -69, 11, 11, (0.86, 0.14, 0.14), seed + 3, shadow=False, lw=2)
    cut(k, [(-84, -98), (84, -98), (78, -76), (-78, -76)], LEATHER, lw=2.4)   # the seat
    cut(k, [(-84, -98), (84, -98), (80, -110), (-80, -110)], LEATHER_L, shadow=False, lw=1.8)
    back = [(-76, -104), (-92, -230), (-84, -330), (-40, -368), (0, -374), (40, -368), (84, -330), (92, -230), (76, -104)]
    cut(k, back, GOLD, lw=2.8)
    inner = [(px * 0.87, -104 + (py + 104) * 0.955) for px, py in back]
    cut(k, inner, LEATHER, shadow=False, lw=2)
    for row, yy in enumerate((-310, -240, -170)):                            # a few deep buttons
        for bx in ((-36, 36), (-54, 0, 54), (-36, 36))[row]:
            c.set_source_rgb(*LEATHER_L); c.set_line_width(2)
            for sx in (-1, 1):
                c.move_to(bx, yy); c.line_to(bx + sx * 26, yy + 34); c.stroke(); c.move_to(bx, yy); c.line_to(bx + sx * 26, yy - 34); c.stroke()
            ellipse(k, bx, yy, 5, 5, GOLD, seed + 30 + row * 5 + int(bx), shadow=False, lw=1.4)
    # one crown, big
    cut(k, [(-44, -372), (-56, -430), (-28, -402), (0, -446), (28, -402), (56, -430), (44, -372)], GOLD, lw=2.6)
    rect(k, -46, -382, 92, 14, GOLD_D, seed + 4, shadow=False, lw=2)
    for dx, dy in ((-56, -432), (0, -448), (56, -432)):
        ellipse(k, dx, dy, 7, 7, (0.62, 0.05, 0.12), seed + 20 + dx, shadow=False, lw=1.6)
    for sx in (-1, 1):                                                       # the arms
        cut(k, [(sx * 80, -110), (sx * 98, -112), (sx * 100, -168), (sx * 88, -172)], GOLD, shadow=False, lw=2.2)
        cut(k, [(sx * 72, -178), (sx * 114, -178), (sx * 116, -160), (sx * 74, -160)], LEATHER, lw=2.2)
    c.set_source_rgba(*GOLD_L, 0.9); c.set_line_width(2.8)
    c.move_to(-85, -236); c.curve_to(-80, -296, -66, -336, -36, -358); c.stroke()
    if puff:                                                                 # PSSSH: the air out both sides, in front
        c.rotate(-lean); c.translate(0, -drop)
        for sx in (-1, 1):
            for i, (y0, y1, ln) in enumerate(((-52, -66, 62), (-40, -40, 78), (-28, -14, 62))):
                c.set_source_rgb(*INK); c.set_line_width(7); c.set_line_cap(1)
                c.move_to(sx * 96, y0); c.line_to(sx * (96 + ln), y1); c.stroke()
                c.set_source_rgb(1, 1, 1); c.set_line_width(4)
                c.move_to(sx * 96, y0); c.line_to(sx * (96 + ln), y1); c.stroke()
    c.restore()
    return {"arm": (x + 94 * s, feet - (178 - drop) * s), "seat": (x, feet - (110 - drop) * s), "top": feet - (448 - drop) * s}


def wet_filter(k, x, y, s=1.0, ang=0.0, seed=2100, drips=False):
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


def coffee_machine(k, x, base, s=1.0, state="broken", t=0.0, seed=2200, cup=True):
    """v2 (after the props review): it has to read as a coffee machine at 270 px. A chrome espresso machine with red
    sides: a group head with a black-handled portafilter sticking out, a spout, a white cup under it, a steam wand, cups
    on top. (x, base): the middle of its foot on the counter. t: seconds, for the shake and the steam."""
    c = k.c
    dx = dy = 0.0
    if state == "rattle":
        dx, dy = math.sin(t * 61) * 3.0, math.cos(t * 47) * 2.2
    c.save(); c.translate(x + dx * s, base + dy * s); c.scale(s, s)
    rect(k, -56, -10, 112, 10, STEEL_D, seed, shadow=False, lw=2)             # the drip tray, slotted
    c.set_source_rgb(*INK); c.set_line_width(1.4)
    for xx in range(-44, 50, 12):
        c.move_to(xx, -8); c.line_to(xx, -3); c.stroke()
    cut(k, [(-58, -10), (-58, -128), (58, -128), (58, -10), (40, -10), (40, -66), (-40, -66), (-40, -10)], MACH, lw=2.6)   # red sides, an open bay
    rect(k, -40, -66, 80, 56, (0.20, 0.19, 0.21), seed + 1, shadow=False, lw=2)   # the back of the bay
    rect(k, -58, -128, 116, 40, STEEL, seed + 2, shadow=False, lw=2.4)        # the chrome front panel
    lid = -22 if state == "pop" else 0
    c.save(); c.translate(0, lid); c.rotate(-0.26 if state == "pop" else 0)
    rect(k, -62, -140, 124, 13, STEEL_D, seed + 3, shadow=False, lw=2.2)      # the top, with two cups warming on it
    if state != "pop":
        for cx_ in (-30, 4):
            cut(k, [(cx_ - 11, -140), (cx_ + 11, -140), (cx_ + 13, -160), (cx_ - 13, -160)], (0.97, 0.96, 0.92), shadow=False, lw=1.8)
    c.restore()
    rect(k, -17, -90, 34, 16, STEEL_D, seed + 4, shadow=False, lw=2)          # the group head
    cut(k, [(-13, -74), (13, -74), (10, -62), (-10, -62)], (0.12, 0.12, 0.13), shadow=False, lw=1.8)   # the portafilter
    cut(k, [(-12, -70), (-52, -58), (-56, -68), (-14, -78)], (0.08, 0.08, 0.09), shadow=False, lw=2)   # its handle, out to the left
    for sx in (-4, 4):                                                       # the twin spout
        c.set_source_rgb(*INK); c.set_line_width(3.2); c.move_to(sx, -62); c.line_to(sx, -54); c.stroke()
    c.set_source_rgb(*INK); c.set_line_width(5); c.set_line_cap(1)           # the steam wand, on the right
    c.move_to(46, -88); c.curve_to(54, -70, 50, -50, 40, -36); c.stroke()
    c.set_source_rgb(*STEEL); c.set_line_width(2.6); c.move_to(46, -88); c.curve_to(54, -70, 50, -50, 40, -36); c.stroke()
    if cup:                                                                  # the cup under the spout
        cut(k, [(-13, -34), (13, -34), (10, -11), (-10, -11)], (0.97, 0.96, 0.92), shadow=False, lw=2)
        c.set_source_rgb(*INK); c.set_line_width(2.2); c.arc(14, -24, 6, -1.2, 1.2); c.stroke()
        if state == "ok":
            c.set_source_rgb(*COFFEE); c.set_line_width(2.4)
            for sx in (-4, 4):
                c.move_to(sx, -54); c.line_to(sx, -34); c.stroke()
    ellipse(k, 36, -108, 13, 13, (0.96, 0.95, 0.90), seed + 5, shadow=False, lw=2)           # the gauge
    ga = {"broken": 2.6, "rattle": 0.25 + math.sin(t * 30) * 0.2, "pop": 0.1, "ok": 1.4}[state]
    c.set_source_rgb(0.86, 0.14, 0.14); c.set_line_width(1.6)
    c.arc(36, -108, 10, -0.9, 0.2); c.stroke()                               # its red zone
    c.set_source_rgb(*INK); c.set_line_width(2.6); c.set_line_cap(1)
    c.move_to(36, -108); c.line_to(36 + math.cos(ga) * 10, -108 - abs(math.sin(ga)) * 10); c.stroke()
    lamp = {"broken": (0.25, 0.25, 0.27), "rattle": RED, "pop": RED, "ok": GRN}[state]
    ellipse(k, -38, -108, 7, 7, lamp, seed + 6, shadow=False, lw=1.8)
    if state != "broken":
        c.set_source_rgba(*lamp, 0.35); c.arc(-38, -108, 13, 0, 2 * math.pi); c.fill()
    for i in range(3):                                                       # three buttons
        ellipse(k, -14 + i * 12, -112, 3.6, 3.6, (0.30, 0.31, 0.35), seed + 8 + i, shadow=False, lw=1.2)
    if state == "broken":                                                    # the note, taped across the bay
        c.save(); c.translate(4, -38); c.rotate(-0.07)
        rect(k, -40, -17, 80, 34, (0.99, 0.98, 0.92), seed + 12, lw=1.8)
        _T(c, "OUT OF", 0, -2, 13.5); _T(c, "ORDER", 0, 12.5, 13.5)
        c.set_source_rgba(0.85, 0.80, 0.55, 0.9); c.rectangle(-9, -21, 18, 8); c.fill()
        c.restore()
    if state == "pop":                                                       # ONE big pop: a starburst, coffee flying
        pts = []
        for i in range(18):
            a = -math.pi + i * math.pi / 17.0
            r_ = 84 if i % 2 == 0 else 50
            pts.append((math.cos(a) * r_ * 1.1, -146 + math.sin(a) * r_))
        cut(k, pts + [(60, -140), (-60, -140)], (1.0, 0.86, 0.15), lw=2.6)
        _T(c, "POP!", 0, -160, 30)
        c.set_source_rgb(*COFFEE)
        for qx, qy, r_ in ((-70, -236, 6), (46, -250, 5), (86, -204, 6.5), (-22, -262, 4.5), (10, -240, 5)):
            c.arc(qx, qy, r_, 0, 2 * math.pi); c.fill()
    if state == "ok":                                                        # steam, rising
        c.set_source_rgba(1, 1, 1, 0.85); c.set_line_width(4.5); c.set_line_cap(1)
        for i, sx_ in enumerate((-14, 4, 22)):
            ph = t * 3 + i
            c.move_to(sx_, -168); c.curve_to(sx_ + 9 * math.sin(ph), -186, sx_ - 9 * math.sin(ph), -204, sx_ + 4, -224); c.stroke()
    c.restore()


def coffee_run(k, head, s, seed=2150):
    """Coffee running down Don's head from the filter: one clear stream past his left eye to the jaw, a drop off it.
    head: the point kit.person returns."""
    c = k.c
    hx, hy = head
    c.save(); c.translate(hx, hy); c.scale(s, s)
    c.set_source_rgb(*COFFEE); c.set_line_width(7); c.set_line_cap(1)
    c.move_to(-30, -34); c.curve_to(-40, -10, -38, 12, -42, 36); c.stroke()
    c.arc(-42, 38, 5.5, 0, 2 * math.pi); c.fill()
    c.set_line_width(5); c.move_to(26, -36); c.curve_to(34, -24, 36, -14, 37, -4); c.stroke()
    c.arc(37, -2, 4.2, 0, 2 * math.pi); c.fill()
    c.arc(-40, 62, 4, 0, 2 * math.pi); c.fill()
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
    # Father: the frame cuts him under the nose. A jaw (Don's round head), a neck in its shadow, the level mouth
    cut(k, [(222, 150), (318, 150), (322, 240), (218, 240)], (0.80, 0.62, 0.52), shadow=False, lw=2.6)   # the neck, in shadow
    c.save(); c.rectangle(0, 0, 540, 200); c.clip()
    ellipse(k, 270, 10, 132, 150, dc.SKIN_F, seed + 20, shadow=False, lw=3)
    c.restore()
    c.set_source_rgba(0.45, 0.30, 0.28, 0.8); c.set_line_width(3.2); c.set_line_cap(1)
    for sx in (-1, 1):                                                                    # the lines by his mouth
        c.move_to(270 + sx * 50, 30); c.curve_to(270 + sx * 62, 56, 270 + sx * 60, 80, 270 + sx * 52, 100); c.stroke()
    c.set_source_rgb(*INK); c.set_line_width(7); c.move_to(240, 84); c.line_to(300, 84); c.stroke()
    cut(k, [(40, 300), (150, 210), (390, 210), (500, 300), (540, 700), (0, 700)], dc.VELVET, lw=3)
    cut(k, [(210, 212), (330, 212), (310, 700), (230, 700)], dc.BLACK, shadow=False, lw=2.4)
    cut(k, [(270, 330), (226, 206), (314, 206)], dc.SKIN_F, shadow=False, lw=2.2)
    for sx in (-1, 1):
        cut(k, [(270 + sx * 44, 206), (270 + sx * 96, 214), (270 + sx * 74, 300), (270 + sx * 10, 350)], dc.BLACK_L, shadow=False, lw=2.2)
        cut(k, [(270 + sx * 60, 250), (270 + sx * 150, 220), (270 + sx * 120, 480), (270 + sx * 40, 700)], dc.VELVET_D, shadow=False, lw=2.4)
    c.set_source_rgb(*GOLD_D); c.set_line_width(12); c.set_line_cap(1)
    c.move_to(236, 214); c.curve_to(246, 300, 294, 300, 304, 214); c.stroke()
    c.set_source_rgb(*GOLD); c.set_line_width(7); c.set_dash([9, 6]); c.move_to(236, 214); c.curve_to(246, 300, 294, 300, 304, 214); c.stroke(); c.set_dash([])
    rect(k, -10, 700, 560, 270, (0.13, 0.06, 0.08), seed + 1, lw=3)                       # the table: dark glass, the neon in it
    c.set_source_rgba(*NEON, 0.30); c.rectangle(0, 706, 540, 8); c.fill()
    c.set_source_rgba(*NEON, 0.10); c.rectangle(0, 760, 540, 60); c.fill()
    # the bodyguard's sleeve, from the left, holding the phone to him
    cut(k, [(-20, 560), (120, 640), (108, 742), (-20, 700)], dc.SUIT_L, lw=3)             # v2: lit from the neon, so it is seen
    c.set_source_rgba(*NEON, 0.55); c.set_line_width(4); c.move_to(-10, 566); c.line_to(118, 640); c.stroke()
    cut(k, [(106, 632), (150, 650), (138, 742), (96, 728)], (0.96, 0.96, 0.93), shadow=False, lw=2.6)
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


def sheet(out="../daddys-home/dh_props_v2.png"):
    import don_v4 as dv
    Wd, Hd = 1900, 1440
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, Wd, Hd); c = cairo.Context(surf)
    c.set_source_rgb(*kit.WALL); c.paint()
    k = Ctx(c, 0)
    kit.text(k, "DADDY'S HOME · PROPS AND THE BOOTH · v2", Wd / 2, 44, 34, INK)

    def frame(fn, x, y, sc, title):
        c.save(); c.translate(x, y); c.scale(sc, sc); c.rectangle(0, 0, 540, 960); c.clip(); fn(Ctx(c, 0)); c.restore()
        c.set_source_rgb(*INK); c.set_line_width(3); c.rectangle(x, y, 540 * sc, 960 * sc); c.stroke()
        kit.text(k, title, x + 270 * sc, y + 960 * sc + 24, 17, INK, font=kit.MONO)
    frame(lambda q: dad_phone(q), 40, 90, 0.5, "0.1 = 11.7: DAD (frame 0)")
    frame(lambda q: booth(q), 350, 90, 0.5, "0.3: the booth. Never his face")
    frame(lambda q: booth(q, face_down=True), 660, 90, 0.5, "0.7: Today. (face down)")
    Z = 0.60 * 1.45
    c.set_source_rgb(*kit.FLOOR); c.rectangle(980, 560, 900, 60); c.fill()
    dv.don(k, 1050, 582, Z, "stand", "neutral", look=(1, 0))
    ceo_chair(k, 1250, 582, Z)
    ceo_chair(k, 1500, 582, Z, sink=1.0, puff=True)
    kit.text(k, "the throne, at Don's scale", 1150, 644, 17, INK, font=kit.MONO)
    kit.text(k, "0.2: DAD rings. PSSSH.", 1500, 644, 17, INK, font=kit.MONO)
    star_screen(k, 1745, 250, 250, green=False); star_screen(k, 1745, 440, 250, green=True)
    kit.text(k, "3.1 to 3.3: it turns green", 1745, 540, 16, INK, font=kit.MONO)
    rect(k, 40, 1310, 1480, 26, (0.55, 0.38, 0.24), 2900, lw=2.4)
    for i, (st_, lab) in enumerate((("broken", "broken"), ("rattle", "7.2: it rattles"), ("pop", "7.2: one big POP"), ("ok", "fixed, and pouring"))):
        coffee_machine(k, 220 + i * 370, 1310, 2.3, st_, t=0.4)
        kit.text(k, lab, 220 + i * 370, 1372, 17, INK, font=kit.MONO)
    o = dv.don(k, 1720, 1340, 0.60 * 1.9, "stand", "neutral", look=(0, 0))
    coffee_run(k, o["head"], 0.60 * 1.9)
    wet_filter(k, o["head"][0], o["head"][1] - 48 * 0.60 * 1.9, 1.5, -0.12)
    kit.text(k, "7.3 to 8.2: on his head", 1720, 1372, 17, INK, font=kit.MONO)
    surf.write_to_png(out); print("wrote", out)


def set_test(out="../daddys-home/dh_set_v5_test_v2.png"):
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
MACHINE = (770, 800 - 166, 0.72)                           # on the counter top, at Pam's elbow


if __name__ == "__main__":
    {"sheet": sheet, "set": set_test}[sys.argv[1] if len(sys.argv) > 1 else "sheet"]()
