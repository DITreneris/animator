"""OFFICE NOIR 3: the alley, set v2 (20 Nov; v1 is alley_on3_v1.py). v2 is a shadow pass after an outside review: the
three shadows are men, not signs (gangster(): a snapped brim, a turned-up collar, square shoulders, bent arms, legs),
each different, the middle one a fifth larger and hunched; one flat tone each, so limbs do not darken where they cross;
weapons short and held, none across a head; they close in between shots. frames() is v2; frames_v1() is v1.
v1: (20 Nov; Tomas, /grill-me). The gap beside the arena, off the street: the same
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


# ---- v2: the shadows as men -------------------------------------------------------------------------------------
def _poly(c, pts):
    c.new_path(); c.move_to(*pts[0])
    for p in pts[1:]:
        c.line_to(*p)
    c.close_path(); c.fill()


def _limb(c, pts, w, fist=0):
    c.set_line_width(w); c.set_line_cap(1); c.set_line_join(1)
    c.new_path(); c.move_to(*pts[0])
    for p in pts[1:]:
        c.line_to(*p)
    c.stroke()
    if fist:
        c.arc(pts[-1][0], pts[-1][1], fist, 0, 2 * math.pi); c.fill()


def _open_hand(c, x, y, r=17):
    c.arc(x, y, r, 0, 2 * math.pi); c.fill()
    c.set_line_width(8); c.set_line_cap(1)
    for a in (-1.15, -0.55, 0.0, 0.55, 1.15):
        c.move_to(x, y); c.line_to(x + math.sin(a) * r * 2.3, y - math.cos(a) * r * 2.3); c.stroke()


def _tommy(c, x, y, a):
    """A tommy gun, its rear grip at (x, y), the muzzle to the left, turned by a (positive: muzzle down)."""
    c.save(); c.translate(x, y); c.rotate(-a)
    _poly(c, [(26, -12), (-112, -12), (-112, 6), (26, 8)])                       # the body
    _poly(c, [(26, -12), (84, -2), (88, 26), (70, 26), (26, 8)])                 # the stock
    c.rectangle(-178, -7, 70, 9); c.fill()                                       # the barrel
    c.rectangle(-196, -11, 20, 17); c.fill()                                     # the compensator
    c.rectangle(-150, -15, 5, 9); c.fill()                                       # the sight
    c.arc(-52, 26, 27, 0, 2 * math.pi); c.fill()                                 # the drum
    _poly(c, [(-98, 4), (-88, 4), (-84, 36), (-98, 36)])                         # the fore grip
    _poly(c, [(-6, 6), (10, 6), (18, 40), (2, 40)])                              # the rear grip
    c.restore()


def _knife(c, x, y, a):
    c.save(); c.translate(x, y); c.rotate(a)
    _poly(c, [(-4, 4), (-9, -62), (0, -92), (10, -58), (5, 4)])                  # a blade, point up at a = 0
    c.rectangle(-15, -4, 30, 8); c.fill()                                        # the guard
    c.restore()


def _bat(c, x0, y0, x1, y1):
    a = math.atan2(y1 - y0, x1 - x0); n = math.hypot(x1 - x0, y1 - y0)
    c.save(); c.translate(x0, y0); c.rotate(a)
    _poly(c, [(-14, -7), (n * 0.45, -9), (n * 0.8, -17), (n, -15), (n + 8, 0), (n, 15), (n * 0.8, 17), (n * 0.45, 9), (-14, 7)])
    c.arc(-14, 0, 10, 0, 2 * math.pi); c.fill()                                  # the knob
    c.restore()


BUILD = {"knife": dict(sh=74, hem=64, arm=27, tilt=0.16, drop=6, lean=0.20),     # lean, wiry, bent forward
         "gun": dict(sh=98, hem=84, arm=36, tilt=0.10, drop=26, lean=0.07),       # the big one: head sunk between his shoulders
         "bat": dict(sh=84, hem=66, arm=30, tilt=-0.14, drop=0, lean=-0.03)}      # upright, his chin up


def gangster(k, x, y, s=1.0, kind="gun", state="aim", flip=False, alpha=0.86, lean=None, aim=0.30):
    """A man's shadow on the wall, feet at (x, y), facing screen left (the Client) unless flip. kind: knife, gun, bat.
    state: aim (at him), down (lowered), up (empty hands up). One flat tone: drawn into a group, then laid on the wall."""
    c = k.c; B = BUILD[kind]; sh, hem, aw = B["sh"], B["hem"], B["arm"]
    lean = B["lean"] if lean is None else lean
    if state != "aim":
        lean *= 0.35                                                            # they stand off
    c.save(); c.translate(x, y); c.scale(-s if flip else s, s)
    c.transform(cairo.Matrix(1, 0, lean, 1, 0, 0))
    c.push_group(); c.set_source_rgb(*SHADE)
    for fx, bx in ((-44, -8), (10, 46)):                                         # legs, shoes pointing at him
        _poly(c, [(fx, -80), (bx, -80), (bx - 2, 0), (fx - 20, 0), (fx - 18, -9), (fx + 2, -14)])
    up = state == "up"
    top = -300 - (10 if up else 0)
    _poly(c, [(-sh, top + 6), (-sh + 12, top - 8), (sh - 8, top - 12), (sh + 4, top + 4), (sh - 20, -178),      # the coat: square shoulders, a waist, a wide hem
              (hem + 10, -62), (-hem - 6, -62), (-sh + 22, -178)])
    c.rectangle(-sh + 20, -186, 2 * sh - 38, 12); c.fill()                       # the belt
    _poly(c, [(hem - 10, -150), (hem + 30, -66), (hem + 4, -62)])                # the coat's tail, behind
    hx, hy = -8 - (0 if up else B["drop"] * 0.5), top - 8 + (0 if up else B["drop"])
    c.save(); c.translate(hx, hy); c.rotate(0 if up else -B["tilt"])
    _poly(c, [(-34, 6), (-46, -40), (-22, -8)]); _poly(c, [(30, 4), (48, -42), (20, -10)])                      # the collar, turned up
    _poly(c, [(24, -10), (30, -52), (-22, -56), (-30, -44), (-42, -34), (-31, -28), (-33, -18), (-24, -6), (-4, 0)])   # jaw, chin, nose
    _poly(c, [(-70, -40), (-66, -50), (-18, -58), (58, -66), (62, -57), (-14, -47)])                            # the brim, snapped down in front
    _poly(c, [(-32, -54), (-38, -92), (-14, -106), (6, -95), (30, -105), (42, -62)])                            # the crown, pinched
    c.restore()
    ls, rs = (-sh + 12, top + 14), (sh - 12, top + 10)                           # shoulders: the near one is in front (screen left)
    if up:
        for sx, (ax, ay) in ((-1, ls), (1, rs)):
            _limb(c, [(ax, ay), (sx * (sh + 44), top - 30), (sx * (sh + 30), top - 118)], aw)
            _open_hand(c, sx * (sh + 30), top - 132, aw * 0.56)
    elif kind == "gun":
        if state == "aim":
            gx, gy = -sh + 4, -230
            fa = (gx - 92 * math.cos(aim), gy + 92 * math.sin(aim) + 10)         # the fore grip
            _limb(c, [rs, (sh + 14, -226), (gx + 6, gy + 14)], aw, aw * 0.5)
            _limb(c, [ls, (-sh - 40, -262), fa], aw, aw * 0.5)
            _tommy(c, gx, gy, aim)
        else:
            _limb(c, [rs, (sh + 16, -210), (sh + 2, -138)], aw, aw * 0.55)
            _limb(c, [ls, (-sh - 14, -214), (-sh - 4, -140)], aw, aw * 0.5)
            _tommy(c, -sh - 8, -146, 1.42)                                      # hanging from one hand, muzzle at the ground
    elif kind == "knife":
        _limb(c, [rs, (sh + 30, -226), (sh - 6, -172)], aw, aw * 0.6)            # a fist on his hip, the elbow out
        if state == "aim":
            _limb(c, [ls, (-sh - 8, -214), (-sh - 62, -236)], aw, aw * 0.6)
            _knife(c, -sh - 62, -240, -0.5)                                      # low, the point up at him
        else:
            _limb(c, [ls, (-sh - 12, -216), (-sh - 8, -146)], aw, aw * 0.6)
            _knife(c, -sh - 8, -138, math.pi)                                    # point down, by his leg
    else:
        if state == "aim":
            _limb(c, [ls, (-sh - 30, -228), (-sh - 26, -142)], aw, aw * 0.78)    # a big fist, low
            _limb(c, [rs, (sh + 26, -238), (sh - 34, -282)], aw, aw * 0.6)       # the bat on his shoulder, behind his head
            _bat(c, sh - 34, -286, sh + 74, -424)
        else:
            _limb(c, [rs, (sh + 14, -214), (sh + 6, -144)], aw, aw * 0.6)
            _limb(c, [ls, (-sh - 12, -214), (-sh - 10, -150)], aw, aw * 0.6)
            _bat(c, -sh - 10, -152, -sh - 26, -6)                                # its end on the ground
    c.pop_group_to_source(); c.paint_with_alpha(alpha)
    c.restore()


def draw_alley2(k, mid=(), men=(), cig=None):
    """v2. men: dicts for gangster() (x, s, kind, state, and flip, alpha, aim), drawn in the order given."""
    def gang(k2):
        c = k2.c
        c.save(); c.rectangle(-40, G - 640, WW + 80, 600); c.clip()
        for m in men:
            m = dict(m); gangster(k2, m.pop("x"), G - 40, **m)
        c.restore()
        if cig is not None:
            _cig(k2, cig)
    draw_alley(k, [gang] + list(mid), (), None)


def _cig(k, x):
    """v2: the dropped end is large enough for a phone, and it still glows."""
    c = k.c
    rect(k, x - 17, G - 22, 30, 9, (0.96, 0.96, 0.92), 8, shadow=False, lw=1.6)
    rect(k, x + 13, G - 22, 8, 9, b.KEY, 9, shadow=False, lw=1.4)
    c.set_source_rgba(1, 1, 1, 0.6); c.set_line_width(3.4); c.set_line_cap(1)
    c.move_to(x + 20, G - 24); c.curve_to(x + 38, G - 60, x + 4, G - 96, x + 28, G - 150); c.stroke(); c.set_line_cap(0)


def frame2(cam, mid=(), men=(), cig=None):
    cam = CAMS[cam] if isinstance(cam, str) else cam
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(s); k = Ctx(c, 0)
    c.save(); st.view(c, *cam); draw_alley2(k, mid, men, cig); c.restore()
    csh.noir(s)
    return s


CAMS["A2w"] = (228, 1128, 1.5)                             # him, and the shadow over him
CAMS["A3w"] = (330, 1130, 1.12)


def don_caught(x, up=0.0):
    """v3 (Tomas, /grill-me): the shadows he did not notice turn their weapons on Don. up 0: bent over his glass and the
    cigarette end. up 1: straight, both hands as high as they go; the glass and the tweezers on the ground."""
    def d(k):
        _sh(k, x, 36)
        old = n2.LOOK[0]; n2.LOOK[0] = 9
        try:
            if up < 0.5:
                o = n2.detective(k, x, G - 12, SC, "look", "squint", (0.6, 0.9), lean=10)
            else:
                dm = n2.d.dm
                o = n2.detective(k, x, G - 12, SC, dm.ik(-1, -64, n2.d.HY - 40) + dm.ik(1, 64, n2.d.HY - 40), "neutral", (0.9, -0.7), lean=-6, glass=False)
        finally:
            n2.LOOK[0] = old
        c = k.c
        if up < 0.5:
            hx, hy = o["hands"][0]
            c.set_source_rgb(0.80, 0.80, 0.84); c.set_line_width(2.4)
            c.move_to(hx, hy); c.line_to(hx + 26, G - 22); c.move_to(hx - 5, hy + 3); c.line_to(hx + 22, G - 18); c.stroke()
        else:                                                # dropped: the glass, the tweezers
            ellipse(k, x + 64, G - 14, 15, 6, (0.80, 0.84, 0.90), 3, shadow=False, lw=2.6)
            c.set_source_rgb(0.10, 0.10, 0.12); c.set_line_width(5); c.move_to(x + 78, G - 13); c.line_to(x + 100, G - 9); c.stroke()
            c.set_source_rgb(0.80, 0.80, 0.84); c.set_line_width(2.4); c.move_to(x - 50, G - 12); c.line_to(x - 22, G - 16); c.move_to(x - 50, G - 12); c.line_to(x - 24, G - 9); c.stroke()
            c.set_source_rgb(0.95, 0.95, 0.95); c.set_line_width(3); c.set_line_cap(1)               # he has had a fright
            for a in (-2.2, -1.57, -0.94):
                hx0, hy0 = o["head"]
                c.move_to(hx0 + 62 * math.cos(a), hy0 - 30 + 62 * math.sin(a)); c.line_to(hx0 + 80 * math.cos(a), hy0 - 30 + 80 * math.sin(a)); c.stroke()
            c.set_line_cap(0)
    return d


def gang(state, close=0.0, turn=False):
    """The three, back to front. close 0..1: they have come nearer him (the sides in, the big one forward and larger)."""
    kn = dict(x=250 - 14 * close, s=1.12 + 0.04 * close, kind="knife", state=state, alpha=0.72, flip=turn)
    bt = dict(x=628 - 40 * close, s=1.24, kind="bat", state=state, alpha=0.68, flip=turn)
    bg = dict(x=440 - 26 * close, s=1.50 + 0.08 * close, kind="gun", state=state, alpha=0.90, flip=turn)
    return [bt, kn, bg]


def _probe(x, pose="b_ask"):
    k = Ctx(cairo.Context(cairo.ImageSurface(cairo.FORMAT_RGB24, 8, 8)), 0)
    return b.boxer(k, x, G - 12, Q, pose, "hard", (0.9, 0), outfit="street", cig=True)


def _tip(x):
    """Where his cigarette ends (world)."""
    return x + 43 * Q, G - 12 + (b.HY + 47) * Q


def fumble(x, lit=False, stage=None, shake=0.0):
    """v2: him, two gloves and a crushed matchbox he cannot open: matches fall out of it. lit: the cigarette burns."""
    base = client(x, "b_ask", (0.9, 0.0), folder=False, matchbox=stage is None)

    def d(k):
        o = base(k); c = k.c
        (lx, ly), (rx, ry) = o["hands"]
        mx, my = (lx + rx) / 2, (ly + ry) / 2
        if stage is not None and not lit:                    # v3 (Tomas: more of the matches): 0 the box, whole; 1 crushed, they spill; 2 one match, pinched, snaps
            def match(px, py, a, ln=14.0, head=True):
                c.save(); c.translate(px, py); c.rotate(a)
                c.set_source_rgb(0.93, 0.90, 0.78); c.rectangle(-ln / 2, -1.2, ln, 2.4); c.fill()
                if head:
                    c.set_source_rgb(*b.KEY); c.arc(ln / 2, 0, 2.2, 0, 2 * math.pi); c.fill()
                c.restore()
            bx, by = mx + shake, my - 2
            if stage == 0:                                   # a matchbox: a sleeve, a striking strip, a flame on its label
                cut(k, [(bx - 13, by - 8), (bx + 13, by - 9), (bx + 14, by + 8), (bx - 12, by + 9)], (0.94, 0.92, 0.82), shadow=False, lw=1.6)
                c.set_source_rgb(0.30, 0.24, 0.20); c.rectangle(bx - 12, by + 4, 25, 4); c.fill()
                c.set_source_rgb(*b.KEY); c.new_path(); c.move_to(bx - 3, by + 1); c.curve_to(bx - 7, by - 4, bx - 1, by - 5, bx, by - 8); c.curve_to(bx + 2, by - 4, bx + 6, by - 3, bx + 3, by + 1); c.close_path(); c.fill()
            else:
                cut(k, [(bx - 11, by - 5), (bx + 8, by - 9), (bx + 12, by + 3), (bx - 5, by + 8), (bx - 13, by + 1)], (0.94, 0.92, 0.82), shadow=False, lw=1.6)
                c.set_source_rgb(0.30, 0.24, 0.20); c.set_line_width(1.6); c.move_to(bx - 9, by - 2); c.line_to(bx + 2, by + 4); c.stroke()
                fall = shake if stage == 1 else 1.0          # shake carries the fall in stage 1: 0..1
                for i, (dx, dy, a) in enumerate(((-9, 20, 0.5), (4, 34, -0.9), (15, 23, 1.3), (-2, 52, 0.2), (10, 62, -0.4))):
                    if stage == 2 or fall * 5 > i:
                        match(mx + dx, my + dy * (0.5 + 0.5 * min(1.0, fall * 5 - i) if stage == 1 else 1.3) + (40 if stage == 2 else 0), a)
            if stage == 2:                                   # the last one, between two glove tips: it bends, it breaks
                if shake < 0.6:
                    match(mx + 1, my - 20 - 4 * shake, -1.2 + 0.2 * shake, 17.0)
                else:
                    match(mx - 3, my - 18, -0.5, 9.0, head=False); match(mx + 6, my - 24, -1.9, 9.0)
                    c.set_source_rgb(0.95, 0.95, 0.95); c.set_line_width(1.6)
                    for a in (-2.4, -1.6, -0.8):
                        c.move_to(mx + 2 + 9 * math.cos(a), my - 22 + 9 * math.sin(a)); c.line_to(mx + 2 + 15 * math.cos(a), my - 22 + 15 * math.sin(a)); c.stroke()
        elif not lit:
            for i, (dx, dy, a) in enumerate(((-9, 20, 0.5), (4, 34, -0.9), (15, 23, 1.3), (-2, 52, 0.2))):   # matches, falling
                c.save(); c.translate(mx + dx, my + dy); c.rotate(a)
                c.set_source_rgb(0.93, 0.90, 0.78); c.rectangle(-7, -1.1, 14, 2.2); c.fill()
                c.set_source_rgb(*b.KEY); c.arc(7, 0, 2.0, 0, 2 * math.pi); c.fill(); c.restore()
        else:
            tx, ty = _tip(x)
            c.set_source_rgb(*b.KEY); c.arc(tx, ty, 3.4, 0, 2 * math.pi); c.fill()
            c.set_source_rgba(1, 1, 1, 0.7); c.set_line_width(2.6); c.set_line_cap(1)
            c.move_to(tx + 2, ty - 5); c.curve_to(tx + 16, ty - 26, tx - 8, ty - 44, tx + 10, ty - 72); c.stroke(); c.set_line_cap(0)
        return o
    return d


def frames_v2b():
    """v2 after cold test 16: the matches get their own shot (both viewers took the gloves for crossed arms), the
    flame reaches the cigarette and it burns (both thought he refused the light)."""
    f = []
    f.append(frame2("A1", [client(60)], gang("aim")))                                        # 3.1
    f.append(frame2("A2w", [fumble(130)], gang("aim", 1)))                                   # 3.2 they have closed in
    (lx, ly), (rx, ry) = _probe(130)["hands"]
    f.append(frame2(((lx + rx) / 2 + 6, (ly + ry) / 2 + 6, 3.6), [fumble(130)], gang("aim", 1)))   # 3.2b insert: gloves, a matchbox, matches falling
    f.append(frame2("A3w", [fumble(150)], gang("down", 1)))                                  # 3.3 the weapons go down
    tx, ty = _tip(130)
    f.append(frame2("A2", [fumble(130, lit=True), lighter_hand(tx + 13, ty + 46, 0.9)], gang("down", 1)))   # the flame at the cigarette; it burns
    f.append(frame2("A1", [client(600, "b_walk", (0.9, 0), cig=False)], gang("down", 0, True), cig=300))
    f.append(frame2("A3w", [don(346)], gang("up"), cig=300))
    return f


def frames_v2():
    f = []
    f.append(frame2("A1", [client(60)], gang("aim")))                                        # 3.1 round the corner; three men's shadows, everything on him
    f.append(frame2("A2w", [client(130, "b_ask", (0.9, 0.0), folder=False, matchbox=True)], gang("aim", 1)))   # 3.2 they have closed in; two gloves, a crushed matchbox
    f.append(frame2("A3w", [client(150, "b_ask", (0.9, 0.0), folder=False, matchbox=True)], gang("down", 1)))  # 3.3 the weapons go down
    ho = b.HY * Q
    f.append(frame2("A2", [client(130, "b_ask", (0.9, 0.0), folder=False, matchbox=True), lighter_hand(130 + 62, G - 12 + ho + 62, 0.9)], gang("down", 1)))
    f.append(frame2("A1", [client(600, "b_walk", (0.9, 0), cig=False)], gang("down", 0, True), cig=300))       # 3.4 he walks on; they watch him go
    f.append(frame2("A3w", [don(346)], gang("up"), cig=300))                                 #     Don; behind him, empty hands up
    return f


frames_v1 = frames
frames = frames_v2b


def sheet(fs, out, w=330):
    n = len(fs); h = int(w * 960 / 540)
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, n * (w + 8) + 8, h + 46); c = cairo.Context(s)
    c.set_source_rgb(0.13, 0.13, 0.15); c.paint()
    for i, f in enumerate(fs):
        c.save(); c.translate(8 + i * (w + 8), 38); c.scale(w / 540, w / 540); c.set_source_surface(f, 0, 0); c.paint(); c.restore()
        c.set_source_rgb(1, 1, 1); c.select_font_face("sans", 0, 1); c.set_font_size(20); c.move_to(12 + i * (w + 8), 26); c.show_text(str(i + 1))
    s.write_to_png(out)


if __name__ == "__main__":
    import sys
    sheet(frames(), sys.argv[1])
