"""PINNED v1 (19 Nov): sheet v1 is drawn from this file. robot_on3.py is v2.
THE ROBOT, "Office Noir 3: The Last Round", v1: the other corner (Tomas, 19 Nov, /grill-me).
The same small HR robot (waiter_kit's body, the HR badge of robot_tg), in the Client's dream:
- BIG GREY GLOVES, bigger than its own screen. Grey, because the film's red is the Client's;
- an EXTRA FRAME (Tomas): a steel yoke over its shoulders that carries two piston arms, since its own thin arms
  could not lift those gloves; and an EXTRA STAND: two outriggers with small casters beside its one wheel, so a
  punch does not tip it over. The fighter has training wheels;
- a CHAMPION'S BELT under the HR badge: it has won before it starts;
- a FURIOUS screen as its face in the ring; and the screen is where the words come up: "ask" (HUMAN / APPROVAL /
  REQUIRED), "tick" (after "Approved."), "proud" (between rounds). crack=True draws the screen cracked (7.2 on).
  Nothing on it is red: the screen's ink is a cold white.
- its corner has no trainer: a charging cable and an oil can (cable(), oil_can()).
waiter_kit and robot_tg draw exactly as before.
Usage: o = robot(k, x, feet, s, pose, state, look, side, crack=False) -> {"head", "hands", "screen"}
Poses: "r_wait" (gloves hanging), "r_guard", "r_jab" (the front piston straight out), "r_oil" (oil=True: a small
service arm on the yoke tips an oil can over its elbow; with gloves on, it cannot hold the can either).
Beside the series' other figures it is drawn at 0.82 of their scale (REL): the small robot."""
import math
import cairo
import kit
import waiter_kit as w
import robot_tg as rt
import client_on3 as b
from kit import INK, cut, rect, ellipse

GLOVE_COL = (0.36, 0.37, 0.40)
GLOVE_SHADE = (0.18, 0.18, 0.20)
STEEL, STEEL_DARK = w.STEEL, w.STEEL_DARK
CHROME = (0.86, 0.87, 0.90)
INKW = (0.86, 0.95, 1.0)                                   # the screen's ink: a cold white
BELT = (0.16, 0.16, 0.19)
PLATE = (0.88, 0.72, 0.30)
PLATE_LIGHT = (1.0, 0.90, 0.60)
REL = 0.82
GS = 0.92                                                  # the gloves, against the Client's (33 units)
LN = 44
POSES = {
    "r_wait": (0.00, 0, 0, (-14, 4), (14, -4)),
    "r_guard": (0.00, -4, -2, (-52, -112), (52, 112)),
    "r_jab": (0.10, 0, 0, (-52, -112), (96, -4)),
    "r_oil": (0.00, 0, 0, (-14, 4), (30, 40)),             # the front elbow out, under the service arm's oil can
}
RX, RY = rt.SCREEN_RX, rt.SCREEN_RY


def _d(a):
    return math.sin(math.radians(a)), math.cos(math.radians(a))


def screen(k, state, look=(0, 0), crack=False, seed=0):
    """Head-local units: the screen and what is on it."""
    c = k.c
    ellipse(k, 0, 0, RX, RY, w.SCREEN, seed, shadow=False, lw=2)
    c.set_source_rgb(*INKW); c.set_line_cap(1)
    lx, ly = look[0] * 5, look[1] * 3
    if state == "furious":                                 # brows slammed down to the middle, slit eyes, bared teeth
        c.set_line_width(7.5)
        for sx in (-1, 1):
            c.new_path(); c.move_to(sx * 31, -18); c.line_to(sx * 6, -5); c.stroke()
        for sx in (-1, 1):
            c.new_path(); c.save(); c.translate(sx * 16 + lx, 3 + ly); c.scale(9, 4.5); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
        c.set_line_width(2.6); c.new_path(); c.rectangle(-17, 15, 34, 11); c.stroke()
        for i in range(1, 5):
            c.new_path(); c.move_to(-17 + i * 6.8, 15); c.line_to(-17 + i * 6.8, 26); c.stroke()
    elif state == "ask":
        for txt, ty, size in (("HUMAN", -11, 17), ("APPROVAL", 6, 17), ("REQUIRED", 23, 17)):
            c.save(); c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(size)
            tw = c.text_extents(txt).x_advance
            wd = (RX * 2 - 12) * (0.80 if ty != 6 else 1.0)
            sc = min(1.0, wd / tw)
            c.translate(0, ty); c.scale(sc, 1); c.move_to(-tw / 2, 0); c.text_path(txt)
            c.set_source_rgb(0.02, 0.04, 0.08); c.set_line_width(2.4); c.stroke_preserve(); c.set_source_rgb(*INKW); c.fill()
            c.restore()
    elif state == "tick":
        c.set_line_width(11); c.set_line_join(1)
        c.new_path(); c.move_to(-24, 2); c.line_to(-7, 19); c.line_to(26, -19); c.stroke()
    elif state == "proud":                                 # shut, pleased eyes and a small smile
        c.set_line_width(5)
        for sx in (-1, 1):
            c.new_path(); c.arc(sx * 16, 0, 9, math.pi * 1.12, math.pi * 1.88); c.stroke()
        c.new_path(); c.arc(0, 8, 13, math.pi * 0.2, math.pi * 0.8); c.stroke()
    else:                                                  # "eager": two round eyes and a smile, as it is at work
        for sx in (-1, 1):
            c.new_path(); c.arc(sx * 15 + lx, -4 + ly, 8, 0, 2 * math.pi); c.fill()
        c.set_line_width(4); c.new_path(); c.arc(0, 8, 12, math.pi * 0.2, math.pi * 0.8); c.stroke()
    c.set_line_cap(0)
    if crack:                                              # the glass, cracked across
        c.save(); c.new_path(); c.save(); c.scale(RX, RY); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.clip()
        for col, lw in (((0.02, 0.04, 0.08), 4.2), ((1, 1, 1), 1.8)):
            c.set_source_rgb(*col); c.set_line_width(lw)
            c.new_path(); c.move_to(-RX, -8); c.line_to(-14, -2); c.line_to(-4, -16); c.line_to(12, 6); c.line_to(RX, -2); c.stroke()
            c.new_path(); c.move_to(-14, -2); c.line_to(-22, 22); c.stroke()
            c.new_path(); c.move_to(12, 6); c.line_to(20, RY); c.stroke()
        c.restore()


def belt(k, body_y, seed=0):
    """The champion's belt, low on the shell under the HR badge."""
    c = k.c
    cut(k, [(-51, body_y + 14), (51, body_y + 14), (47, body_y + 34), (-47, body_y + 34)], BELT, shadow=False, lw=2)
    ellipse(k, 0, body_y + 24, 21, 15, PLATE, seed, shadow=False, lw=2)
    ellipse(k, 0, body_y + 24, 14, 9.5, PLATE_LIGHT, seed + 1, shadow=False, lw=1.2)
    c.new_path()
    for j in range(10):
        a = math.pi * 2 * j / 10 - math.pi / 2
        rr = 7.5 if j % 2 == 0 else 3.2
        (c.move_to if j == 0 else c.line_to)(rr * math.cos(a), body_y + 24 + rr * math.sin(a))
    c.close_path(); c.set_source_rgb(*INK); c.fill()
    for sx in (-1, 1):
        rect(k, sx * 33 - 6, body_y + 17, 12, 14, PLATE, seed + 3 + sx, shadow=False, lw=1.4)


def oil_can(k, x, y, s=1.0, ang=0.0, seed=0):
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    cut(k, [(-13, 0), (13, 0), (10, -22), (-10, -22)], CHROME, lw=2)
    cut(k, [(-5, -22), (5, -22), (2, -30), (-2, -30)], STEEL, shadow=False, lw=1.6)
    c.set_source_rgb(*INK); c.set_line_width(4.6); c.set_line_cap(1)
    c.new_path(); c.move_to(0, -30); c.curve_to(2, -44, 16, -48, 30, -44); c.stroke()
    c.set_source_rgb(*STEEL); c.set_line_width(2.4); c.new_path(); c.move_to(0, -30); c.curve_to(2, -44, 16, -48, 30, -44); c.stroke()
    c.set_line_cap(0)
    c.set_source_rgb(0.10, 0.10, 0.12); c.new_path(); c.arc(31, -39, 2.6, 0, 2 * math.pi); c.fill()   # a drop
    c.restore()


def cable(k, x0, y0, x1, y1, seed=0):
    """A charging cable from its back (x0, y0) to a plug in the corner post's socket at (x1, y1)."""
    c = k.c
    mx = (x0 + x1) / 2
    for col, lw in ((INK, 7.5), ((0.20, 0.20, 0.23), 4.5)):
        c.set_source_rgb(*col); c.set_line_width(lw); c.set_line_cap(1)
        c.new_path(); c.move_to(x0, y0); c.curve_to(mx, y0 + 70, mx, y1 + 70, x1, y1); c.stroke()
    c.set_line_cap(0)
    rect(k, x1 - 9, y1 - 11, 18, 22, CHROME, seed, shadow=False, lw=1.8)
    rect(k, x1 + 9, y1 - 6, 8, 4, STEEL_DARK, seed + 1, shadow=False, lw=1.0)
    rect(k, x1 + 9, y1 + 2, 8, 4, STEEL_DARK, seed + 2, shadow=False, lw=1.0)


def robot(k, x, feet, s=1.0, pose="r_wait", state="furious", look=(0, 0), side=1, seed=900, crack=False, rig=True,
          wobble=0.0, oil=False):
    """side=1: it faces screen right. rig=False draws it without the yoke, pistons and outriggers (the work robot)."""
    c = k.c
    tilt, crouch, drop, near, far = POSES[pose] if isinstance(pose, str) else pose
    old, old_tie = w._badge, w.TIE
    w._badge = rt.tg_badge
    if rig:
        w.TIE = (0.13, 0.13, 0.15)                         # a black tie in the ring: nothing on it is red
    try:
        out = w.robot(k, x, feet, s, (tilt, crouch, drop, near, far), "eager", look, wobble, side, 0.0, None, seed, True, False, 0, 0)
    finally:
        w._badge, w.TIE = old, old_tie
    c.save(); c.translate(x, feet); c.scale(s * side, s); c.rotate(tilt + wobble)
    body_y = -118 + crouch
    sh_y = w.SHOULDER_Y + crouch
    hands = []
    if rig:
        for sx in (-1, 1):                                 # the stand: an outrigger and a caster each side of its wheel
            c.set_source_rgb(*INK); c.set_line_width(8); c.set_line_cap(1)
            c.new_path(); c.move_to(sx * 10, -34); c.line_to(sx * 52, -12); c.stroke()
            c.set_source_rgb(*STEEL); c.set_line_width(4.6); c.new_path(); c.move_to(sx * 10, -34); c.line_to(sx * 52, -12); c.stroke()
            c.set_line_cap(0)
            ellipse(k, sx * 54, -8, 8.5, 8.5, (0.10, 0.10, 0.12), seed + 80 + sx, shadow=False, lw=2)
            ellipse(k, sx * 54, -8, 3, 3, STEEL, seed + 82 + sx, shadow=False, outline=False)
        belt(k, body_y, seed + 84)
        c.save(); c.scale(side, 1)                         # the badge again, over the belt's top edge if they meet
        c.restore()
        for col, lw in ((INK, 15), (STEEL_DARK, 10.5)):    # the frame: a yoke over both shoulders
            c.set_source_rgb(*col); c.set_line_width(lw); c.set_line_cap(1)
            c.new_path(); c.move_to(-50, sh_y + 20); c.curve_to(-64, sh_y - 30, 64, sh_y - 30, 50, sh_y + 20); c.stroke()
        c.set_source_rgb(*CHROME); c.set_line_width(2.0)
        c.new_path(); c.move_to(-50, sh_y + 6); c.curve_to(-58, sh_y - 22, 58, sh_y - 22, 50, sh_y + 6); c.stroke()
        c.set_line_cap(0)
        for sgn, (a1, a2) in ((-1, near), (1, far)):       # the piston arms, over its own thin ones
            sx_, sy_ = sgn * 46, sh_y
            ex, ey = sx_ + _d(a1)[0] * LN, sy_ + _d(a1)[1] * LN
            hx, hy = ex + _d(a1 + a2)[0] * LN, ey + _d(a1 + a2)[1] * LN
            for col, lw in ((INK, 22), (STEEL_DARK, 17)):  # the cylinder
                c.set_source_rgb(*col); c.set_line_width(lw); c.set_line_cap(0)
                c.new_path(); c.move_to(sx_, sy_); c.line_to(ex, ey); c.stroke()
            for col, lw in ((INK, 11), (CHROME, 6.5)):     # the rod
                c.set_source_rgb(*col); c.set_line_width(lw); c.set_line_cap(1)
                c.new_path(); c.move_to(ex, ey); c.line_to(hx, hy); c.stroke()
            c.set_line_cap(0)
            ellipse(k, sx_, sy_, 13, 13, STEEL, seed + 86 + sgn, shadow=False, lw=2)
            ellipse(k, ex, ey, 9, 9, STEEL, seed + 88 + sgn, shadow=False, lw=2)
            ux, uy = (hx - ex) / LN, (hy - ey) / LN
            c.save(); c.translate(hx + ux * 12, hy + uy * 12); c.scale(GS, GS)
            b._glove(k, 0, 0, ux, uy, sgn, seed + 90 + sgn, col=GLOVE_COL, shade=GLOVE_SHADE)
            c.restore()
            hands.append((hx + ux * 12, hy + uy * 12))
            if oil and sgn > 0:                            # the service arm, and the can over that elbow
                ax, ay = 34, sh_y - 22
                bx, by = ex + 26, ey - 62
                for col, lw in ((INK, 7.5), (STEEL, 4.5)):
                    c.set_source_rgb(*col); c.set_line_width(lw); c.set_line_cap(1); c.set_line_join(1)
                    c.new_path(); c.move_to(ax, ay); c.line_to(ax + 40, ay - 26); c.line_to(bx, by); c.stroke()
                c.set_line_cap(0)
                ellipse(k, ax + 40, ay - 26, 5.5, 5.5, STEEL_DARK, seed + 95, shadow=False, lw=1.6)
                oil_can(k, bx + 2, by + 14, 1.0, 2.2, seed + 96)
    hy0 = w.HEAD_Y + drop + crouch
    c.save(); c.translate(0, hy0)
    ellipse(k, 0, 0, 50, 44, w.BODY, seed + 68, shadow=False, lw=2.4)
    c.save(); c.scale(side, 1); screen(k, state, (look[0] * side, look[1]), crack, seed + 69); c.restore()
    c.set_source_rgb(*INK); c.set_line_width(2.4); c.new_path(); c.move_to(0, -44); c.line_to(0, -58); c.stroke()
    ellipse(k, 0, -62, 6.5, 6.5, (1, 1, 1) if state in ("furious", "ask") else (0.80, 0.82, 0.86), seed + 70, shadow=False, lw=1.5)
    if state == "furious":                                 # the antenna, flashing
        c.set_source_rgb(*INK); c.set_line_width(2.2); c.set_line_cap(1)
        for a in (-2.4, -1.57, -0.74):
            c.new_path(); c.move_to(11 * math.cos(a), -62 + 11 * math.sin(a)); c.line_to(18 * math.cos(a), -62 + 18 * math.sin(a)); c.stroke()
        c.set_line_cap(0)
    c.restore()
    c.restore()
    P = lambda px, py: (x + px * s * side, feet + py * s)
    if rig:
        out["hands"] = [P(*h) for h in hands]
    out["screen"] = P(0, hy0)
    return out
