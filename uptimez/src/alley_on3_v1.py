"""OFFICE NOIR 3: the alley, set v1 (20 Nov; Tomas, /grill-me). The gap beside the arena, off the street: the same
brick, one fight poster, a lamp at the far end that throws everything onto one long lit wall. The gunmen are never
seen: three big shadows in hats and coats on that wall (a tommy gun, a bat, a knife). One real hand comes out of a
shadow with a lighter. No weapon is fired.
World: 760 wide, the ground's front edge at G. He comes in at the left (the street), goes out at the right (the arena).
frame(cam, mid, shadows, ...) -> a 540x960 surface in the dream's look. frames() -> beat 03 staged, in order."""
import math
import cairo
import kit
import client_on3 as b
import client_sheet_on3 as csh
import noir2_cast as n2
import street_on3 as st
from kit import Ctx, cut, rect, ellipse, INK

WW, G = 760, 1400
WALL_LIT, WALL_D = (0.66, 0.66, 0.64), (0.50, 0.50, 0.50)
SHADE = (0.06, 0.06, 0.07)
SC = 0.9
Q = SC * b.REL
CAMS = {"A1": (380, 1120, 0.71),                           # the alley, end to end
        "A2": (215, 1215, 1.9),                            # him, close
        "A3": (330, 1150, 1.25)}                           # him and the nearest shadow


def shadow_man(k, x, y, s=1.0, weapon="gun", state="aim", flip=False):
    """A man's shadow on the wall, feet at (x, y): hat, coat, one arm. state: "aim" (the weapon out at him), "down"
    (lowered), "up" (both hands up, empty). He is to screen left of them unless flip."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(-s if flip else s, s)
    c.set_source_rgba(*SHADE, 0.86)
    c.new_path()                                            # the coat
    c.move_to(-64, 0); c.line_to(-52, -250); c.line_to(-34, -300); c.line_to(34, -300); c.line_to(52, -250); c.line_to(64, 0); c.close_path(); c.fill()
    c.arc(0, -338, 36, 0, 2 * math.pi); c.fill()             # the head
    c.rectangle(-58, -366, 116, 12); c.fill()                # the brim
    c.new_path(); c.move_to(-36, -366); c.line_to(-30, -414); c.line_to(30, -414); c.line_to(36, -366); c.close_path(); c.fill()
    c.set_line_width(30); c.set_line_cap(1)
    if state == "up":
        for sx in (-1, 1):
            c.move_to(sx * 40, -280); c.line_to(sx * 86, -340); c.line_to(sx * 84, -430); c.stroke()
            c.arc(sx * 84, -446, 20, 0, 2 * math.pi); c.fill()
    else:
        a = {"knife": 0.28, "gun": 0.0, "bat": -0.85}[weapon] if state == "aim" else 1.25   # out at him, each at its own height; or down
        ex, ey = -40 - 120 * math.cos(a), -270 + 120 * math.sin(a)
        c.move_to(-40, -280); c.line_to(ex, ey); c.stroke()
        c.save(); c.translate(ex, ey); c.rotate(-a)          # the weapon, along the arm
        if weapon == "gun":
            c.rectangle(-120, -12, 120, 20); c.fill(); c.rectangle(-190, -6, 80, 9); c.fill()
            c.arc(-70, 22, 24, 0, 2 * math.pi); c.fill(); c.rectangle(-18, 0, 16, 44); c.fill()
        elif weapon == "bat":
            c.new_path(); c.move_to(0, -7); c.line_to(-210, -22); c.line_to(-216, 0); c.line_to(-210, 22); c.line_to(0, 7); c.close_path(); c.fill()
        else:
            c.new_path(); c.move_to(-10, -12); c.line_to(-150, 0); c.line_to(-10, 14); c.close_path(); c.fill(); c.rectangle(-10, -20, 12, 40); c.fill()
        c.restore()
    c.set_line_cap(0)
    c.restore()


def draw_alley(k, mid=(), shadows=(), cig=None):
    """shadows: (x, weapon, state) on the lit wall. cig: (x) a dropped cigarette end on the ground, smoking."""
    c = k.c
    c.set_source_rgb(0.05, 0.05, 0.06); c.rectangle(-600, -400, WW + 1200, G + 1400); c.fill()
    rect(k, -40, G - 640, WW + 80, 600, WALL_LIT, 3, shadow=False, lw=3)                              # the long wall
    g = cairo.LinearGradient(-40, 0, WW + 40, 0)                                                      # lit from the far (right) end
    g.add_color_stop_rgba(0, 0, 0, 0, 0.45); g.add_color_stop_rgba(0.55, 0, 0, 0, 0.0); g.add_color_stop_rgba(1, 1, 1, 1, 0.25)
    c.set_source(g); c.rectangle(-40, G - 640, WW + 80, 600); c.fill()
    c.set_source_rgb(*WALL_D); c.set_line_width(2)
    for i in range(15):
        y = G - 640 + i * 40
        c.move_to(-40, y); c.line_to(WW + 40, y); c.stroke()
        for j in range(-1, 13):
            x = j * 70 + (35 if i % 2 else 0)
            c.move_to(x, y); c.line_to(x, y + 40); c.stroke()
    st.poster(k, 18, G - 330, 1.0, 40)
    rect(k, -600, G - 700, 560, 760, (0.03, 0.03, 0.04), 4, shadow=False, lw=3)                       # the corner he comes round (the street)
    rect(k, WW + 40, G - 700, 560, 760, (0.03, 0.03, 0.04), 5, shadow=False, lw=3)                    # the far corner
    rect(k, WW - 30, G - 330, 70, 290, (0.92, 0.92, 0.88), 6, shadow=False, lw=3)                     # the way through to the arena: light
    cut(k, [(-600, G - 40), (WW + 600, G - 40), (WW + 600, G + 900), (-600, G + 900)], (0.20, 0.20, 0.23), shadow=False, lw=3)
    g = cairo.LinearGradient(0, G - 40, 0, G + 200); g.add_color_stop_rgba(0, 1, 1, 1, 0.22); g.add_color_stop_rgba(1, 1, 1, 1, 0)
    c.set_source(g); c.rectangle(-40, G - 40, WW + 80, 240); c.fill()
    c.save(); c.rectangle(-40, G - 640, WW + 80, 600); c.clip()
    for x, weapon, state in shadows:
        shadow_man(k, x, G - 40, 1.3, weapon, state)
    c.restore()
    if cig is not None:
        rect(k, cig - 9, G - 16, 18, 5, (0.96, 0.96, 0.92), 8, shadow=False, lw=1.2)
        c.set_source_rgba(1, 1, 1, 0.5); c.set_line_width(2.4); c.set_line_cap(1)
        c.move_to(cig + 9, G - 16); c.curve_to(cig + 20, G - 40, cig, G - 60, cig + 14, G - 90); c.stroke(); c.set_line_cap(0)
    for fn in mid:
        fn(k)


def frame(cam, mid=(), shadows=(), cig=None):
    cam = CAMS[cam] if isinstance(cam, str) else cam
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(s); k = Ctx(c, 0)
    c.save(); st.view(c, *cam); draw_alley(k, mid, shadows, cig); c.restore()
    csh.noir(s)
    return s


def _sh(k, x, w=44):
    c = k.c
    c.save(); c.translate(x, G - 12); c.scale(w, w * 0.16); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
    c.set_source_rgba(0, 0, 0, 0.4); c.fill()


def client(x, pose="b_walk", look=(0.8, 0), cig=True, folder=True, matchbox=False):
    def d(k):
        _sh(k, x)
        o = b.boxer(k, x, G - 12, Q, pose, "hard", look, outfit="street", cig=cig)
        if folder and pose == "b_walk":                      # the folder, under his arm
            st.folder(k, x - 44 * Q, G - 12 - 196 * Q, 0.5 * SC, 1.35)
        if matchbox:                                         # a crushed matchbox, between the two gloves
            (lx, ly), (rx, ry) = o["hands"]
            mx, my = (lx + rx) / 2, (ly + ry) / 2 - 4
            cut(k, [(mx - 10, my - 5), (mx + 9, my - 8), (mx + 11, my + 4), (mx - 6, my + 7), (mx - 12, my + 1)], (0.92, 0.90, 0.80), shadow=False, lw=1.4)
        return o
    return d


def lighter_hand(x, y, s=1.0, flame=True):
    """A real hand out of the shadow, a white cuff, a lighter; its thumb on the wheel. It reaches to screen left."""
    def d(k):
        c = k.c
        c.save(); c.translate(x, y); c.scale(s, s)
        rect(k, 30, -13, 90, 26, (0.08, 0.08, 0.09), 3, shadow=False, lw=2)                           # the sleeve, out of the dark
        rect(k, 14, -15, 22, 30, (0.97, 0.97, 0.95), 4, shadow=False, lw=1.8)                         # the cuff
        ellipse(k, 0, 0, 17, 14, (0.90, 0.76, 0.66), 5, shadow=False, lw=2)
        rect(k, -14, -34, 15, 26, (0.80, 0.80, 0.84), 6, shadow=False, lw=1.6)                        # the lighter
        if flame:
            c.new_path(); c.move_to(-7, -34); c.curve_to(-17, -48, -9, -56, -6, -66); c.curve_to(-2, -56, 5, -48, -5, -34); c.close_path()
            c.set_source_rgb(1, 1, 0.96); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1.2); c.stroke()
        c.restore()
    return d


def don(x):
    def d(k):
        _sh(k, x, 36)
        old = n2.LOOK[0]; n2.LOOK[0] = 9
        try:
            o = n2.detective(k, x, G - 12, SC, "look", "squint", (-0.6, 0.9), lean=-10)
        finally:
            n2.LOOK[0] = old
        hx, hy = o["hands"][0]
        c = k.c
        c.set_source_rgb(0.80, 0.80, 0.84); c.set_line_width(2.4)                                     # the tweezers, down to the cigarette end
        c.move_to(hx, hy); c.line_to(hx - 26, G - 22); c.move_to(hx + 5, hy + 3); c.line_to(hx - 22, G - 18); c.stroke()
    return d


AIM = [(330, "knife", "aim"), (500, "gun", "aim"), (670, "bat", "aim")]
DOWN = [(330, "knife", "down"), (500, "gun", "down"), (670, "bat", "down")]
UP = [(330, "knife", "up"), (500, "gun", "up"), (670, "bat", "up")]


def frames():
    f = []
    f.append(frame("A1", [client(60)], AIM))                                               # 3.1 he comes round the corner; everything turns on him
    f.append(frame("A2", [client(130, "b_ask", (0.9, 0.0), folder=False, matchbox=True)], AIM))   # 3.2 two gloves, a crushed matchbox, his chin forward
    f.append(frame("A3", [client(150, "b_ask", (0.9, 0.0), folder=False, matchbox=True)], DOWN))  # 3.3 the weapons go down
    ho = b.HY * Q
    f.append(frame("A2", [client(130, "b_ask", (0.9, 0.0), folder=False, matchbox=True), lighter_hand(130 + 62, G - 12 + ho + 62, 0.9)], DOWN))   # a hand, a flame
    f.append(frame("A1", [client(600, "b_walk", (0.9, 0), cig=False)], DOWN, cig=300))     # 3.4 he walks on; the cigarette is on the ground
    f.append(frame("A3", [don(346)], UP, cig=300))                                         #     Don, the tweezers; behind him, hands up
    return f
