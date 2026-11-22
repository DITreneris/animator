"""THE OFFER (episode 13), stage 3: the garage set and its props (series/production-process.md). Set v1.

The Client's own garage, bay 7: one bay seen from inside, clean and organised (decided at stop 1). A compact car up on
four axle stands, nose to the right; out from under it, two legs in work trousers on a creeper; a caged work lamp on
the floor on its cable; a red tool cabinet in front at the left with the radio on it; a pegboard with every tool on
its painted outline; the roller door up onto a bright street at the left; on the back wall, the blue plan of the ten
garages (episode 11's drawing, cs_props.plan, "whole": the 7 taped in) under the painted sign GARAGE 7.

Set units are the series' (fs_storyboard): the floor line F = 800, the same character scales (the Client 0.52, the
bodyguards 0.56, Father 0.62), so the cast drops in. FRAME0 is the camera of frame 0 and of the last frame.

  python3 of_set.py [out_dir]   ->  of_set_v4.png         the clean set at frame 0, at 540 and at the feed's 270
                                    of_set_plan_v4.png    top-down: the bay and every garage camera of script v4
                                    of_set_props_v4.png   the new props as inserts, at 270
                                    of_blocking_s2_v4.png scene 2, The Lighter, blocked with the cast
Nothing here changes an older module."""
import math
import os
import sys
import cairo
import kit
import fs_storyboard as sb
import cs_props as cp
import cs_frame as cf
from kit import Ctx, INK, cut, rect, ellipse

W, H = 540, 960
F = sb.F                                                   # 800: the back wall meets the floor
FRAME0 = (310, 677, 1.00)                                  # frame 0: the bay from inside, the legs above y 720

WALL, WALL_D = (0.80, 0.84, 0.80), (0.56, 0.64, 0.60)      # a clean pale green, a darker dado
CEIL = (0.30, 0.32, 0.33)
FLOOR, FLOOR_L = (0.62, 0.62, 0.60), (0.78, 0.77, 0.72)    # sealed concrete; the light from the door on it
STREET, STREET_D = (1.00, 0.97, 0.86), (0.93, 0.86, 0.70)  # morning outside: bright
CAR, CAR_D, CAR_L = (0.20, 0.42, 0.62), (0.13, 0.28, 0.43), (0.40, 0.62, 0.80)   # a plain blue hatchback
GLASS = (0.72, 0.84, 0.90)
TYRE, HUB = (0.13, 0.13, 0.15), (0.70, 0.72, 0.75)
RED, RED_D = (0.80, 0.16, 0.14), (0.55, 0.10, 0.09)
NAVY_T, BOOT = (0.17, 0.22, 0.34), (0.42, 0.27, 0.14)     # his work trousers, his boots
STEEL, STEEL_D = (0.66, 0.68, 0.70), (0.40, 0.42, 0.45)
PEG = (0.86, 0.74, 0.52)
LAMP = (1.00, 0.93, 0.55)
GOLD, GOLD_D = (0.90, 0.72, 0.26), (0.62, 0.46, 0.12)
BURN = (0.46, 0.27, 0.10)
BURN_R = 30                                               # v4 (22 Nov, after the mute test): bigger, darker at the heart

SIGN = (282, 332, 570, 400)                                # GARAGE 7, set units (x0, y0, x1, y1): whole or out
PLAN = (410, 526, 1.20)                                    # v3: 50 lower, in a man's reach behind the car                                    # the plan's centre and scale (cs_props: 124 x 104 units)
CAR_X = (170, 548)                                         # the car's tail and nose
SILL, WHEEL_Y, WHEEL_R = 782, 792, 38
CAR_SQUASH = 0.80                                        # set v3 (22 Nov): the roof lower
STANDS = (236, 482)                                        # the axle stands, under the sills
CREEPER = (318, 842)                                       # where his legs come out from under the sill
LAMP_AT = (430, 892)


PROTECT = []                                               # story props drawn this frame: (name, x0, y0, x1, y1) in frame units


def protect(c, name, x0, y0, x1, y1):
    """declare a prop a beat depends on, in the current user coordinates; it must stay out of the apps' zones."""
    pts = [c.user_to_device(x, y) for x, y in ((x0, y0), (x1, y0), (x0, y1), (x1, y1))]
    PROTECT.append((name, min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts)))


def T(c, s, x, y, size, col=INK, font="Lilita One", center=True):
    c.select_font_face(font, 0, 0); c.set_font_size(size)
    e = c.text_extents(s)
    c.move_to(x - (e.x_advance / 2 if center else 0), y); c.set_source_rgb(*col); c.show_text(s)
    return e


# --- the room --------------------------------------------------------------------------------------------------------

def room(k):
    c = k.c
    c.set_source_rgb(*WALL); c.rectangle(-400, -400, 1400, F + 400); c.fill()
    c.set_source_rgb(*WALL_D); c.rectangle(-400, F - 92, 1400, 92); c.fill()                # the dado: painted, clean
    c.set_source_rgb(*INK); c.set_line_width(2.2); c.move_to(-400, F - 92); c.line_to(1000, F - 92); c.stroke()
    c.set_source_rgb(*CEIL); c.rectangle(-400, -400, 1400, 600); c.fill()                   # the ceiling and its beam
    c.set_source_rgb(*INK); c.set_line_width(2.6); c.move_to(-400, 200); c.line_to(1000, 200); c.stroke()
    rect(k, 150, 206, 240, 16, (0.96, 0.97, 0.98), 3001, lw=2)                               # the tube light
    c.set_source_rgb(*FLOOR); c.rectangle(-400, F, 1400, 800); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(2.6); c.move_to(-400, F); c.line_to(1000, F); c.stroke()
    c.set_source_rgba(0.98, 0.84, 0.20, 0.9); c.set_line_width(7)                          # the bay's yellow line
    c.move_to(-60, 1010); c.line_to(640, 1010); c.stroke()


def door(k):
    """the roller door, up: the opening x 20-200, the drum above it; outside, the bright street, a kerb, the house
    opposite. The light lies across the floor."""
    c = k.c
    x0, x1, top = 20, 200, F - 330
    c.set_source_rgb(*STREET); c.rectangle(x0, top, x1 - x0, F - top); c.fill()
    c.set_source_rgb(0.96, 0.88, 0.72); c.rectangle(x0, F - 210, x1 - x0, 150); c.fill()     # the house opposite
    for wx in (48, 128):
        rect(k, wx, F - 186, 40, 52, (0.80, 0.90, 0.96), 3010 + wx, shadow=False, lw=1.8)
    c.set_source_rgb(*STREET_D); c.rectangle(x0, F - 60, x1 - x0, 60); c.fill()              # the pavement
    c.set_source_rgb(*INK); c.set_line_width(1.8); c.move_to(x0, F - 60); c.line_to(x1, F - 60); c.stroke()
    c.set_source_rgba(1.0, 0.98, 0.88, 0.55)                                                 # the light on the floor
    c.move_to(x0, F); c.line_to(x1, F); c.line_to(x1 + 170, F + 300); c.line_to(x0 - 60, F + 300); c.close_path(); c.fill()
    rect(k, x0 - 14, top - 4, 14, F - top + 4, (0.62, 0.64, 0.66), 3002, lw=2)               # the guides
    rect(k, x1, top - 4, 14, F - top + 4, (0.62, 0.64, 0.66), 3003, lw=2)
    rect(k, x0 - 20, top - 40, x1 - x0 + 54, 40, (0.70, 0.72, 0.74), 3004, lw=2.4)           # the drum, rolled up
    c.set_source_rgb(*INK); c.set_line_width(1.2)
    for i in range(1, 4):
        c.move_to(x0 - 16, top - 40 + i * 10); c.line_to(x1 + 30, top - 40 + i * 10); c.stroke()
    rect(k, x1 + 24, top + 120, 18, 26, (0.86, 0.86, 0.82), 3005, lw=1.6)                    # the door's switch
    c.set_source_rgb(*RED); c.arc(x1 + 33, top + 131, 4, 0, 2 * math.pi); c.fill()


def sign(k, burn=False):
    """GARAGE 7, stencilled on the wall, white on a painted green band."""
    c = k.c
    x0, y0, x1, y1 = SIGN
    rect(k, x0, y0, x1 - x0, y1 - y0, (0.18, 0.42, 0.34), 3020, shadow=False, lw=2.2)
    T(c, "GARAGE 7", (x0 + x1) / 2, y1 - 16, 50, col=(0.97, 0.97, 0.93))


def plan(k, burn=0.0):
    """episode 11's plan, whole (the 7 taped in, MY GARAGES on the tape), pinned to the wall. burn: 0 none, 0..1 the
    flame browning GARAGE 7's corner, 1 the mark that stays (1.7 on, and the last frame)."""
    c = k.c
    px, py, s = PLAN
    k0 = 3.9
    old = (cp.PROPS4[0], cp.TITLE_TAPE[0], cp._bg)
    cp.PROPS4[0], cp.TITLE_TAPE[0] = True, True
    cp._bg = lambda *a, **kw: None
    c.save(); c.translate(px, py); c.scale(s / k0, s / k0); c.translate(-270, -470)
    try:
        cp.plan(k, "whole", 740)
    finally:
        c.restore()
        cp.PROPS4[0], cp.TITLE_TAPE[0], cp._bg = old
    if burn > 0:
        bx_, by_ = bay7()
        protect(c, "the burn on 7", bx_ - 6 - BURN_R, by_ - 4 - BURN_R, bx_ - 6 + BURN_R, by_ - 4 + BURN_R)
    if burn > 0:                                   # v2: a charred patch, black at the heart, a ragged brown edge
        import random
        bx, by = bay7()
        f = min(1.0, burn)
        rnd = random.Random(7)
        rr = [1 + 0.22 * (rnd.random() - 0.5) for _ in range(18)]
        for col, rad in (((0.55, 0.33, 0.12), BURN_R * f), (BURN, BURN_R * 0.80 * f), ((0.10, 0.06, 0.03), BURN_R * 0.55 * f)):
            if rad < 1:
                continue
            c.new_path()
            for i, q in enumerate(rr):
                a_ = 2 * math.pi * i / len(rr)
                (c.move_to if i == 0 else c.line_to)(bx - 6 + math.cos(a_) * rad * q, by - 4 + math.sin(a_) * rad * q * 0.9)
            c.close_path(); c.set_source_rgb(*col); c.fill_preserve()
            if col == (0.55, 0.33, 0.12):
                c.set_source_rgb(*INK); c.set_line_width(1.4); c.stroke()
            c.new_path()
    for (dx, dy) in ((-74, -64), (74, -64), (-74, 56), (74, 56)):                         # the drawing pins
        c.set_source_rgb(*RED); c.arc(px + dx * s / 1.2, py + dy * s / 1.2, 4.2, 0, 2 * math.pi); c.fill_preserve()
        c.set_source_rgb(*INK); c.set_line_width(1.2); c.stroke()


def bay7():
    """the lower right corner of GARAGE 7 on the wall plan, in set units (where the flame goes)."""
    import acts_ob as ac
    n_, bx, by, bw, bh = [b for b in ac._bays() if b[0] == 7][0]
    px, py, s = PLAN
    return px + (bx + bw) * s, py + (by + bh) * s


def pegboard(k):
    c = k.c
    x0, y0, w, h = 244, 430, 100, 170
    rect(k, x0, y0, w, h, PEG, 3030, lw=2.2)
    c.set_source_rgba(0.45, 0.35, 0.22, 0.5)
    for i in range(6):
        for j in range(10):
            c.arc(x0 + 10 + i * 16, y0 + 10 + j * 16, 1.4, 0, 2 * math.pi); c.fill()
    tools = [(266, 458, 0.0, 44), (284, 458, 0.0, 54), (302, 458, 0.0, 64), (324, 458, 0.0, 50),   # spanners, by size
             (266, 530, 0.0, 46), (296, 530, 0.0, 46)]
    for i, (tx, ty, a, ln) in enumerate(tools):
        c.set_source_rgba(1, 1, 1, 0.55); c.set_line_width(9); c.set_line_cap(1)         # its painted outline
        c.move_to(tx, ty); c.line_to(tx, ty + ln); c.stroke()
        c.set_source_rgb(*STEEL); c.set_line_width(5.5)
        c.move_to(tx, ty); c.line_to(tx, ty + ln); c.stroke()
        c.set_source_rgb(*INK); c.set_line_width(1.4)
        c.arc(tx, ty - 1, 5.5, math.pi * 0.25, math.pi * 1.75); c.stroke()
    rect(k, 316, 524, 14, 34, RED, 3031, shadow=False, lw=1.6)                              # a screwdriver
    c.set_source_rgb(*STEEL_D); c.set_line_width(3); c.move_to(323, 558); c.line_to(323, 586); c.stroke()


def cabinet(k):
    """the red roller cabinet, front left, and the radio on it (a foreground layer)."""
    c = k.c
    x0, y0, w, h = -40, 748, 132, 196
    rect(k, x0, y0, w, h, RED, 3040, lw=2.6)
    for i in range(5):
        yy = y0 + 14 + i * 34
        rect(k, x0 + 10, yy, w - 20, 28, RED_D if i % 2 else (0.72, 0.13, 0.12), 3041 + i, shadow=False, lw=1.6)
        c.set_source_rgb(*STEEL); c.rectangle(x0 + w / 2 - 18, yy + 11, 36, 5); c.fill()
    for wx in (x0 + 16, x0 + w - 16):
        ellipse(k, wx, y0 + h + 6, 9, 9, TYRE, 3048 + int(wx), shadow=False, lw=1.6)
    radio(k, 26, y0)


def radio(k, x, base):
    c = k.c
    rect(k, x - 46, base - 46, 92, 46, (0.30, 0.30, 0.28), 3050, lw=2.2)
    ellipse(k, x - 22, base - 23, 15, 15, (0.18, 0.18, 0.18), 3051, shadow=False, lw=1.6)
    c.set_source_rgb(0.98, 0.80, 0.30); c.rectangle(x + 2, base - 36, 34, 12); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(2); c.move_to(x + 30, base - 46); c.line_to(x + 52, base - 92); c.stroke()


def car(k, bonnet=0.0, tilt=0.0):
    """the hatchback, side on, nose right, on four stands; the wheels hang a little off the floor. bonnet: 0 shut,
    1 up (scene 3)."""
    c = k.c
    x0, x1 = CAR_X
    if tilt:                                     # v4: rocked on its stands (0.8), about the far stand's foot
        c.save(); c.translate(STANDS[1], SILL + 50); c.rotate(tilt); c.translate(-STANDS[1], -(SILL + 50))
    for sx in STANDS:                                                                        # the axle stands
        stand(k, sx, SILL + 8)
    body = [(x0, SILL - 6), (x0 - 4, 712), (x0 + 18, 690), (x0 + 70, 640), (x0 + 108, 616), (x0 + 236, 614),
            (x0 + 292, 676), (x1 - 18, 694), (x1 + 2, 724), (x1, SILL - 6), (x1 - 20, SILL), (x0 + 16, SILL)]
    def low(c_):                                         # v3: the body 20 % lower (the roof at a man's shoulder on stands)
        c_.save(); c_.translate(0, SILL); c_.scale(1, CAR_SQUASH); c_.translate(0, -SILL)
    low(c)
    cut(k, body, CAR, lw=2.8)
    c.restore()
    for wx in (x0 + 74, x1 - 82):                                                            # the arches
        c.set_source_rgb(*INK); c.arc(wx, WHEEL_Y - 4, WHEEL_R + 8, math.pi, 2 * math.pi); c.fill()
    for wx in (x0 + 74, x1 - 82):
        ellipse(k, wx, WHEEL_Y, WHEEL_R, WHEEL_R, TYRE, 3060 + wx, shadow=False, lw=2)
        ellipse(k, wx, WHEEL_Y, 17, 17, HUB, 3061 + wx, shadow=False, lw=1.6)
    low(c)
    cut(k, [(x0 + 80, 646), (x0 + 112, 626), (x0 + 168, 625), (x0 + 168, 668), (x0 + 80, 668)], GLASS, shadow=False, lw=2)
    cut(k, [(x0 + 180, 625), (x0 + 230, 625), (x0 + 270, 668), (x0 + 180, 668)], GLASS, shadow=False, lw=2)
    c.set_source_rgb(*CAR_D); c.set_line_width(2.4)                                          # the doors' seams
    c.move_to(x0 + 174, 622); c.line_to(x0 + 174, SILL - 8); c.stroke()
    c.move_to(x0 + 276, 676); c.line_to(x0 + 270, SILL - 8); c.stroke()
    c.set_source_rgb(*INK); c.set_line_width(2)
    c.move_to(x0 + 296, 680); c.line_to(x1 - 22, 696); c.stroke()                          # the bonnet's line
    rect(k, x0 + 150, 694, 18, 6, STEEL_D, 3062, shadow=False, lw=1.2)                       # handles
    rect(k, x0 + 246, 694, 18, 6, STEEL_D, 3063, shadow=False, lw=1.2)
    ellipse(k, x1 - 10, 712, 9, 7, (1.0, 0.95, 0.75), 3064, shadow=False, lw=1.6)            # the headlamp
    rect(k, x0 - 6, 706, 12, 14, RED, 3065, shadow=False, lw=1.4)                            # the tail lamp
    rect(k, x1 - 26, SILL - 18, 30, 12, STEEL, 3066, shadow=False, lw=1.4)                   # bumpers
    rect(k, x0 - 8, SILL - 18, 28, 12, STEEL, 3067, shadow=False, lw=1.4)
    if bonnet > 0:                                   # v2: the engine bay open, the lid up on its hinge at the screen
        hx, hy = x0 + 292, 676
        cut(k, [(hx + 2, hy + 2), (x1 - 20, 694), (x1 - 4, 712), (hx + 14, 712)], (0.12, 0.12, 0.14), shadow=False, lw=2)
        c.set_source_rgb(*STEEL_D); c.rectangle(hx + 24, 698, 30, 10); c.fill()            # the engine, a hint
        if not LID_BEHIND[0]:
            lid(k, bonnet, squashed=False)
    c.restore()
    if tilt:
        c.restore()


LID_BEHIND = [False]                                       # v6 (opt-in): the open lid drawn behind whoever works at the bay


def lid(k, bonnet, squashed=True):
    """the bonnet's lid, up on its hinge at the screen (set units; squashed=True applies the car's own squash)."""
    c = k.c
    x0, x1 = CAR_X
    hx, hy = x0 + 292, 676
    if squashed:
        c.save(); c.translate(0, SILL); c.scale(1, CAR_SQUASH); c.translate(0, -SILL)
    c.save(); c.translate(hx, hy); c.rotate(-1.45 * bonnet)
    cut(k, [(0, 0), (x1 - 16 - hx, 8), (x1 - 16 - hx, 34), (0, 24)], CAR_L, lw=2.4)          # v5: a lid you can see
    c.restore()
    if squashed:
        c.restore()


def stand(k, x, top):
    c = k.c
    c.set_source_rgb(*RED); c.set_line_width(5); c.set_line_cap(1)
    for dx in (-16, 16):
        c.move_to(x, top + 8); c.line_to(x + dx, top + 46); c.stroke()
    c.set_source_rgb(*INK); c.set_line_width(1.6)
    for dx in (-16, 16):
        c.move_to(x - 2.5, top + 8); c.line_to(x + dx - 2.5, top + 46); c.stroke()
    rect(k, x - 6, top - 4, 12, 16, STEEL, 3070 + x, shadow=False, lw=1.4)


def legs(k, out=0.0):
    """his legs on the creeper, from under the sill toward us, knees a little up; out: the creeper rolled out
    (scene 2, 1.3), in set units."""
    c = k.c
    lx, ly = CREEPER
    ly += out
    rect(k, lx - 34, ly - 14, 68, 20, (0.24, 0.24, 0.26), 3080, lw=2)                       # the creeper's board
    for wx in (lx - 26, lx + 26):
        ellipse(k, wx, ly + 9, 6, 6, (0.45, 0.45, 0.48), 3081 + wx, shadow=False, lw=1.4)
    c.set_line_cap(1); c.set_line_join(1)
    for side, (kx, ky, fx, fy) in ((-1, (lx - 34, ly + 22, lx - 46, ly + 62)), (1, (lx + 16, ly + 30, lx + 30, ly + 66))):
        sx = lx + side * 11
        for col, lw in ((INK, 27), (NAVY_T, 22)):
            c.set_source_rgb(*col); c.set_line_width(lw)
            c.move_to(sx, ly - 6); c.line_to(kx, ky); c.line_to(fx, fy); c.stroke()
        c.save(); c.translate(fx, fy + 6); c.rotate(-0.15 * side)
        cut(k, [(-13, -10), (12, -10), (15, 8), (-15, 10)], BOOT, shadow=False, lw=2)       # the boot, sole to us
        c.set_source_rgb(*INK); c.rectangle(-15, 7, 30, 5); c.fill()
        c.restore()
    c.set_source_rgba(0, 0, 0, 0.18); c.rectangle(CAR_X[0] + 20, SILL + 4, CAR_X[1] - CAR_X[0] - 40, 46); c.fill()   # under the car


def lamp(k, x=None, y=None, ang=-0.5, lit=True):
    """the caged work lamp on its cable (lying on the floor in frame 0)."""
    c = k.c
    x = LAMP_AT[0] if x is None else x
    y = LAMP_AT[1] if y is None else y
    c.set_source_rgb(*INK); c.set_line_width(3); c.set_line_cap(1)                          # the cable, to the wall
    c.move_to(x + 24, y + 6); c.curve_to(x + 80, y + 30, 560, y - 40, 600, F - 30); c.stroke()
    if lit:
        g = cairo.RadialGradient(x, y, 4, x, y, 90)
        g.add_color_stop_rgba(0, 1.0, 0.95, 0.70, 0.55); g.add_color_stop_rgba(1, 1.0, 0.95, 0.70, 0.0)
        c.set_source(g); c.arc(x, y, 90, 0, 2 * math.pi); c.fill()
    c.save(); c.translate(x, y); c.rotate(ang)
    rect(k, 8, -7, 34, 14, (0.15, 0.15, 0.16), 3090, lw=1.8)                                  # the handle
    ellipse(k, -6, 0, 20, 15, LAMP if lit else (0.85, 0.85, 0.80), 3091, lw=2)
    c.set_source_rgb(*INK); c.set_line_width(1.6)
    for dy in (-10, 0, 10):
        c.move_to(-24, dy); c.line_to(10, dy * 0.6); c.stroke()
    c.restore()


def garage(k, burn=0.0, legs_out=None, bonnet=0.0, lamp_on_floor=True, behind=None, front=None, tilt=0.0):
    """the whole set in set units; frame 0 and the last frame: garage(k) and garage(k, burn=1). behind: people in
    the walkway between the wall and the car (drawn before the car); front: people in front of it."""
    room(k); door(k); sign(k); plan(k, burn); pegboard(k)
    c = k.c
    if LID_BEHIND[0] and bonnet > 0:
        lid(k, bonnet)
    if behind:
        behind(k)
    rect(k, 560, F - 40, 18, 22, (0.90, 0.90, 0.86), 3095, shadow=False, lw=1.4)             # the socket
    car(k, bonnet, tilt)
    if legs_out is not None:
        legs(k, legs_out)
    if lamp_on_floor:
        lamp(k)
    if front:
        front(k)
    cabinet(k)


def frame(k, cam=FRAME0, draw=garage, **kw):
    """one 540 x 960 frame through a camera (fx, fy, z): set (fx, fy) at the frame's (270, 480)."""
    c = k.c
    fx, fy, z = cam
    c.save(); c.translate(270, 480); c.scale(z, z); c.translate(-fx, -fy)
    try:
        draw(k, **kw)
    finally:
        c.restore()


def to_frame(cam, x, y):
    fx, fy, z = cam
    return ((x - fx) * z + 270, (y - fy) * z + 480)


# --- the sheets ------------------------------------------------------------------------------------------------------

def _render(fn, scale=2):
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W * scale, H * scale)
    s.set_device_scale(scale, scale)
    c = cairo.Context(s); c.set_source_rgb(1, 1, 1); c.paint()
    fn(Ctx(c, 0))
    return s


def _label(c, s, x, y, size=22, col=INK, center=False, font="Inter"):
    c.select_font_face(font, 0, 1); c.set_font_size(size); c.set_source_rgb(*col)
    e = c.text_extents(s)
    c.move_to(x - (e.x_advance / 2 if center else 0), y); c.show_text(s)


def _guides(c, cam=None):
    """the apps' zones: the top bar, the bottom quarter, the right-hand buttons."""
    c.set_source_rgba(0.1, 0.1, 0.1, 0.22); c.rectangle(0, 0, W, 96); c.fill()
    c.set_source_rgba(0.85, 0.1, 0.1, 0.16); c.rectangle(0, cf.BOTTOM, W, H - cf.BOTTOM); c.fill()
    c.set_source_rgba(0.85, 0.1, 0.1, 0.16); c.rectangle(cf.RAIL[0], cf.RAIL[1], W - cf.RAIL[0], min(cf.RAIL[2], cf.BOTTOM) - cf.RAIL[1]); c.fill()
    c.set_source_rgb(0.85, 0.1, 0.1); c.set_line_width(1.5); c.set_dash([6, 4])
    c.move_to(0, cf.BOTTOM); c.line_to(W, cf.BOTTOM); c.stroke()
    c.rectangle(cf.RAIL[0], cf.RAIL[1], W - cf.RAIL[0], cf.RAIL[2] - cf.RAIL[1]); c.stroke(); c.set_dash([])


def sign_state(cam):
    x0, y0 = to_frame(cam, SIGN[0], SIGN[1]); x1, y1 = to_frame(cam, SIGN[2], SIGN[3])
    if x1 < 0 or x0 > W or y1 < 0 or y0 > H:
        return "out"
    if x0 >= 0 and x1 <= W and y0 >= 96 and y1 <= cf.BOTTOM:
        return "whole"
    return "CUT"                                   # partly in the picture, or under the top bar: never


def sheet_set(out):
    """the clean set at frame 0 (540 with the apps' zones; the same frame at the feed's 270) and the last frame."""
    f0 = _render(lambda k: frame(k, FRAME0, legs_out=0.0))
    f1 = _render(lambda k: frame(k, FRAME0, burn=1.0, legs_out=0.0))
    g = _render(lambda k: (frame(k, FRAME0, legs_out=0.0), _guides(k.c)))
    SW, SH = 540 * 2 + 270 + 120 + 270, 960 + 200
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, SW * 2, SH * 2); s.set_device_scale(2, 2)
    c = cairo.Context(s); c.set_source_rgb(0.96, 0.95, 0.92); c.paint()
    _label(c, "THE OFFER · the garage · set v4 · frame 0 (camera %s, %s, %.2f)" % FRAME0, 30, 46, 26)
    _label(c, "clean, organised: every tool on its outline. GARAGE 7: %s in frame 0. Legs end at y %d (bottom line 720)."
           % (sign_state(FRAME0), to_frame(FRAME0, CREEPER[0], CREEPER[1] + 72)[1]), 30, 80, 17, col=(0.3, 0.3, 0.3))
    y = 120
    for i, (img, cap) in enumerate(((f0, "frame 0"), (g, "frame 0, the apps' zones"))):
        c.save(); c.translate(30 + i * 570, y); c.scale(1.0, 1.0); c.set_source_surface(img, 0, 0); c.paint(); c.restore()
        _label(c, cap, 30 + i * 570, y + 960 + 30, 18)
    x = 30 + 2 * 570
    for j, (img, cap) in enumerate(((f0, "frame 0 at 270 (the feed)"), (f1, "the last frame at 270: the burn on 7"))):
        c.save(); c.translate(x, y + j * 520); c.scale(0.5, 0.5); c.set_source_surface(img, 0, 0); c.paint(); c.restore()
        _label(c, cap, x, y + j * 520 + 480 + 22, 16)
    x2 = x + 300
    for j, b in enumerate((0.0, 1.0)):                                       # the plan, close, before and after
        def close(k, b=b):
            bx, by = bay7()
            frame(k, (PLAN[0], PLAN[1], 3.4), burn=b, legs_out=0.0)
        img = _render(close)
        c.save(); c.translate(x2, y + j * 520); c.scale(0.5, 0.5); c.set_source_surface(img, 0, 0); c.paint(); c.restore()
        _label(c, ("the plan (ep 11's, whole)" if j == 0 else "after 1.7: the brown mark"), x2, y + j * 520 + 480 + 22, 16)
    s.write_to_png(out)


BLOCK_TOP = [("Father", 96, 380), ("bodyguard 1 (obeys)", 240, 360), ("bodyguard 2 (loyal, lighter)", 456, 50),
             ("Client, sat up on the creeper", 318, 330)]

# the cameras of every garage shot in script v4 (top-down plan): shot -> (x, depth, aim x, aim depth, label)
# depth: 0 = the back wall, + toward us; the frame-0 camera stands at the bay's front.
TOP = dict(wall=0, car=(170, 548, 40, 110), creeper=(318, 110, 190), door=(20, 200), cabinet=(-40, 92, 150, 250),
           plan=(300, 420), lamp=(430, 180))
CAMS = [
    ("0.1/0.2/1.3/4.2", 270, 560, 270, 60, "frame 0: WIDE, the bay"),
    ("0.3", 250, 300, 110, 80, "LOW, floor level by the creeper, to the door"),
    ("0.4", 130, 360, 318, 300, "HIGH over Father's shoulder, down at the legs"),
    ("0.5/0.9", 330, 230, 330, 150, "UNDER THE CAR, close on his face"),
    ("0.6/1.6/2.3b/2.4/2.6", 360, 360, 120, 230, "CLOSE, Father (at the door end)"),
    ("0.8/0.10", 270, 440, 300, 80, "MEDIUM, the hand on the roof"),
    ("1.1/1.2/1.5/1.7", 300, 70, 410, 0, "TWO-SHOT at the plan"),
    ("1.4/2.5/2.8b", 160, 400, 380, 190, "CLOSE, the Client"),
        ("2.1/2.3/2.8c", 270, 520, 300, 140, "TWO-SHOT, Father and the Client, car between"),
    ("2.2/2.8d/2.8f", 500, 380, 470, 120, "the bonnet end: the Client, the lamp"),
    ("2.7/2.8/2.8e", 230, 300, 300, 180, "MEDIUM / INSERTS: phone, key"),
    ("2.9", 120, 420, 120, 230, "MEDIUM, Father and the loyal one"),
    ("4.1", 110, 120, 110, -60, "INSERT, the doorway, his hand"),
]


def sheet_plan(out):
    SW, SH = 1100, 1250
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, SW * 2, SH * 2); s.set_device_scale(2, 2)
    c = cairo.Context(s); c.set_source_rgb(0.96, 0.95, 0.92); c.paint()
    k = Ctx(c, 0)
    _label(c, "THE OFFER · the garage from above · every garage camera of script v4", 30, 46, 26)
    _label(c, "set x across (as in the set's frames); depth down the page from the back wall. Shot numbers as in the script.",
           30, 78, 16, col=(0.3, 0.3, 0.3))
    ox, oy, sc = 140, 170, 1.05                                              # set x -> page, depth -> page
    P = lambda x, d: (ox + (x + 60) * sc, oy + d * sc)
    c.set_source_rgb(0.86, 0.86, 0.83); x0_, y0_ = P(-60, 0); x1_, y1_ = P(640, 620)
    c.rectangle(x0_, y0_, x1_ - x0_, y1_ - y0_); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(6); c.move_to(*P(-60, 0)); c.line_to(*P(20, 0)); c.stroke()
    c.move_to(*P(200, 0)); c.line_to(*P(640, 0)); c.stroke()
    c.set_source_rgb(*STREET); a, b = P(20, -70); a2, b2 = P(200, 0); c.rectangle(a, b, a2 - a, b2 - b); c.fill()
    _label(c, "ROLLER DOOR, up: the street", P(20, -80)[0], P(20, -80)[1], 14)
    for (nm, x_, d_, w_, h_, col) in (("GARAGE 7 sign + the plan (wall)", 282, -10, 288, 10, (0.18, 0.42, 0.34)),
                                      ("pegboard", 214, -10, 100, 10, PEG)):
        a, b = P(x_, d_); c.set_source_rgb(*col); c.rectangle(a, b, w_ * sc, h_ * sc); c.fill()
        _label(c, nm, a, b - 6, 12)
    a, b = P(170, 110); c.set_source_rgb(*CAR); c.rectangle(a, b, 378 * sc, 150 * sc); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(2); c.rectangle(a, b, 378 * sc, 150 * sc); c.stroke()
    _label(c, "CAR on 4 stands (nose right)", a + 100, b + 80, 15, col=(1, 1, 1))
    _label(c, "walkway behind the car: the second bodyguard reaches the plan", P(200, 60)[0], P(200, 60)[1], 13)
    for nm, x_, d_ in BLOCK_TOP:                                              # where they stand in scene 2
        a, b = P(x_, d_); c.set_source_rgb(0.25, 0.25, 0.30); c.arc(a, b, 9, 0, 2 * math.pi); c.fill()
        _label(c, nm, a + 12, b + 5, 13, col=(0.25, 0.25, 0.30))
    a, b = P(300, 200); c.set_source_rgb(0.24, 0.24, 0.26); c.rectangle(a, b, 36 * sc, 130 * sc); c.fill()
    _label(c, "creeper + legs", a + 44, b + 130, 13)
    a, b = P(-40, 260); c.set_source_rgb(*RED); c.rectangle(a, b, 132 * sc, 70 * sc); c.fill()
    _label(c, "cabinet + radio", a, b + 92, 13)
    a, b = P(430, 220); c.set_source_rgb(*LAMP); c.arc(a, b, 10, 0, 2 * math.pi); c.fill()
    _label(c, "lamp", a + 14, b + 5, 13)
    for i, (shot, x, d, ax, ad, cap) in enumerate(CAMS):
        p = P(x, d); q = P(ax, ad)
        ang = math.atan2(q[1] - p[1], q[0] - p[0])
        c.save(); c.translate(*p); c.rotate(ang)
        c.set_source_rgba(0.95, 0.55, 0.10, 0.25); c.move_to(0, 0); c.line_to(60, -24); c.line_to(60, 24); c.close_path(); c.fill()
        c.set_source_rgb(*INK); c.rectangle(-12, -8, 18, 16); c.fill()
        c.restore()
        c.set_source_rgb(0.6, 0.25, 0.0); c.arc(p[0], p[1], 11, 0, 2 * math.pi); c.fill()
        _label(c, str(i + 1), p[0], p[1] + 5, 13, col=(1, 1, 1), center=True)
        _label(c, "%d  %s  %s" % (i + 1, shot, cap), 40, 870 + i * 25, 15)
    s.write_to_png(out)


# --- the props -------------------------------------------------------------------------------------------------------

def lighter(k, x, y, s=1.0, flame=1.0, hand=True, lid=1.0):
    """the gold lighter (v2): a square case, its lid flipped open on the hinge, the chimney with its holes, the
    wheel; flame 0..1; hand: his fist round the case from below, the black sleeve and white cuff going off right.
    (x, y) is the flame's foot."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    if hand:
        for col, lw in ((INK, 46), ((0.11, 0.11, 0.13), 40)):                  # the sleeve, from his side
            c.set_source_rgb(*col); c.set_line_width(lw); c.set_line_cap(1)
            c.move_to(16, 74); c.line_to(80, 140); c.stroke()
        c.save(); c.translate(34, 94); c.rotate(0.8)
        rect(k, -10, -24, 22, 48, (0.97, 0.97, 0.95), 3105, shadow=False, lw=1.8)  # the white cuff
        c.restore()
    rect(k, -26, 0, 52, 74, GOLD, 3101, lw=2.6)                                   # the case
    c.set_source_rgb(*GOLD_D); c.set_line_width(2); c.move_to(-26, 22); c.line_to(26, 22); c.stroke()
    c.save(); c.translate(26, 0); c.rotate(-1.9 * lid)                           # the lid, open on its hinge
    cut(k, [(0, 0), (0, -2), (-52, -2), (-52, 30), (0, 30)], GOLD, lw=2.4)
    c.restore()
    rect(k, -16, -26, 28, 26, (0.86, 0.86, 0.84), 3102, shadow=False, lw=2)       # the chimney
    c.set_source_rgb(*INK)
    for i in range(3):
        for j in range(2):
            c.arc(-10 + i * 8, -18 + j * 10, 2, 0, 2 * math.pi); c.fill()
    ellipse(k, 18, -10, 7, 9, (0.40, 0.40, 0.42), 3103, shadow=False, lw=1.6)    # the wheel
    if flame > 0:
        f = flame
        g = cairo.RadialGradient(-2, -50, 2, -2, -50, 46)
        g.add_color_stop_rgba(0, 1.0, 0.95, 0.6, 0.85 * f); g.add_color_stop_rgba(1, 1.0, 0.6, 0.1, 0.0)
        c.set_source(g); c.arc(-2, -50, 46, 0, 2 * math.pi); c.fill()
        cut(k, [(-2, -30 - 50 * f), (12, -42), (8, -28), (-12, -28), (-16, -42)], (1.0, 0.62, 0.12), shadow=False, lw=1.8)
        cut(k, [(-2, -34 - 26 * f), (5, -34), (-9, -34)], (1.0, 0.95, 0.65), shadow=False, outline=False)
    if hand:                                                                    # the fist round the case, thumb on the wheel
        ellipse(k, 2, 60, 34, 26, (0.92, 0.74, 0.60), 3104, lw=2.4)
        c.set_source_rgb(*INK); c.set_line_width(2)
        for q in range(3):
            c.new_path(); c.move_to(-18 + q * 14, 44); c.line_to(-20 + q * 14, 62); c.stroke()
        ellipse(k, 22, 2, 9, 14, (0.92, 0.74, 0.60), 3106, shadow=False, lw=2)
    c.restore()


def insert_lighter(k):
    c = k.c
    c.set_source_rgb(*WALL); c.paint()
    old = PLAN
    globals()["PLAN"] = (270, 360, 3.4)
    try:
        plan(k, 0.6)
    finally:
        globals()["PLAN"] = old
    bx, by = 270 + (bay7()[0] - PLAN[0]) * 3.4 / PLAN[2], 360 + (bay7()[1] - PLAN[1]) * 3.4 / PLAN[2]
    lighter(k, bx - 4, by + 4 + 80 * 1.3, 1.3, 1.0)
    for i, ln in enumerate(("THE LIGHTER (1.2)", "flame at GARAGE 7's corner")):
        _label(c, ln, 270, 880 + i * 36, 26 if i == 0 else 20, center=True)


def insert_delete(k):
    """0.4: the one-star post on the bodyguard's phone, DELETE POST under it, his thumb over the button."""
    cp.phone(k, "review", 940)
    c = k.c
    x0, y0, w = 58, 70, 424
    rect(k, x0 + 40, y0 + 640, w - 80, 110, RED, 3110, shadow=False, lw=2.4)
    T(c, "DELETE POST", x0 + w / 2, y0 + 712, 46, col=(1, 1, 1))
    c.save(); c.translate(x0 + w / 2 + 90, y0 + 820)                                         # the thumb, hovering
    cut(k, [(-40, 140), (-46, 20), (-30, -30), (0, -44), (30, -30), (44, 20), (40, 140)], (0.86, 0.68, 0.56), lw=2.4)
    ellipse(k, 0, -24, 22, 14, (0.96, 0.86, 0.80), 3111, shadow=False, lw=1.6)
    c.restore()


def insert_card(k):
    """2.8: one contact card, nothing else: PAM — finds things."""
    c = k.c
    x0, y0, w = cp._phone(k, 950)
    cx = x0 + w / 2
    if hasattr(cp, "pam_photo"):
        cp.pam_photo(k, cx, y0 + 250, 120, 951)
    T(c, "PAM", cx, y0 + 520, 96)
    T(c, "finds things", cx, y0 + 600, 52, col=(0.42, 0.44, 0.50), font="Inter")
    protect(c, "PAM finds things", x0 + 60, y0 + 120, x0 + w - 60, y0 + 620)


def insert_visor(k):
    """3.2: the robot's calendar card, one line: WITHOUT HIM."""
    c = k.c
    c.set_source_rgb(0.10, 0.12, 0.18); c.paint()
    rect(k, 50, 260, 440, 440, (0.12, 0.16, 0.26), 3120, lw=3)
    rect(k, 80, 300, 380, 80, (0.30, 0.85, 0.95), 3121, shadow=False, lw=2)
    T(c, "NEW MEETING", 270, 356, 44, col=(0.10, 0.12, 0.18))
    T(c, "WITHOUT", 270, 500, 92, col=(0.35, 0.85, 0.95))
    T(c, "HIM", 270, 610, 110, col=(0.35, 0.85, 0.95))


def insert_invite(k):
    """3.6: Pam's phone: INVITATION."""
    c = k.c
    x0, y0, w = cp._phone(k, 960)
    cx = x0 + w / 2
    rect(k, x0 + 30, y0 + 220, w - 60, 330, (0.97, 0.94, 0.86), 3130, lw=2.4)
    T(c, "INVITATION", cx, y0 + 330, 58, col=(0.55, 0.16, 0.46))
    T(c, "from", cx, y0 + 410, 30, col=(0.42, 0.44, 0.50), font="Inter")
    T(c, "FATHER", cx, y0 + 470, 52)
    rect(k, x0 + 70, y0 + 556, w - 140, 76, cp.GRN, 3131, shadow=False, lw=2)          # v2: clear of the captions
    T(c, "ACCEPT", cx, y0 + 608, 38, col=(1, 1, 1))
    protect(c, "INVITATION from FATHER", x0 + 60, y0 + 220, x0 + w - 60, y0 + 634)


def sheet_props(out):
    items = [("0.4 DELETE POST", insert_delete), ("1.2 the gold lighter", insert_lighter),
             ("2.8 PAM — finds things", insert_card), ("3.2 WITHOUT HIM", insert_visor), ("3.6 INVITATION", insert_invite)]
    tw, th = 270, 480
    SW, SH = 40 + len(items) * (tw + 30), 120 + th + 60
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, SW * 2, SH * 2); s.set_device_scale(2, 2)
    c = cairo.Context(s); c.set_source_rgb(0.96, 0.95, 0.92); c.paint()
    _label(c, "THE OFFER · the new props · every insert at 270 px (the feed): each must read at this size", 30, 46, 24)
    _label(c, "The plan and its burn mark are on the set sheet. The DONNIE call (4.1) is episode 12's dad_phone screen.",
           30, 78, 16, col=(0.3, 0.3, 0.3))
    for i, (cap, fn) in enumerate(items):
        img = _render(fn)
        x = 30 + i * (tw + 30)
        c.save(); c.translate(x, 110); c.scale(0.5, 0.5); c.set_source_surface(img, 0, 0); c.paint(); c.restore()
        _label(c, cap, x, 110 + th + 30, 16)
    s.write_to_png(out)


# --- scene 2, The Lighter: blocking with the cast -----------------------------------------------------------------------

FS, GS, CS = 0.62, 0.56, 0.52                              # Father, the bodyguards, the Client (the series' scales)
POS = dict(father=(96, 880), g1=(240, 872), g2=(456, F + 18), client=(318, 916))   # the Client: his hips, sat up
LEGS_OUT = 48


def _head(o, s, r0=55):
    h = o.get("head") if isinstance(o, dict) else None
    return (h[0], h[1], r0 * s) if h else None


def _cast(heads, sit=True, g2_pose=None):
    import dh_cast as dc
    import client_ob as co

    def behind(k):
        x, f = POS["g2"]
        heads["g2"] = _head(dc.guard(k, x, f, GS, pose=g2_pose, flip=True), GS) or (x, f - 372 * GS, 55 * GS)

    def front(k):
        c = k.c
        x, f = POS["father"]
        heads["father"] = _head(dc.father(k, x, f, FS, look=(1, 0)), FS, 50) or (x, f - 338 * FS, 50 * FS)
        x, f = POS["g1"]
        heads["g1"] = _head(dc.guard(k, x, f, GS), GS) or (x, f - 372 * GS, 55 * GS)
        if sit:                                                 # sat up on the creeper: his top half over his legs
            x, hip = POS["client"]
            feet = hip - co.HIP * CS
            c.save(); c.rectangle(x - 200, hip - 400, 400, 400 + 6); c.clip()
            o = co.client(k, x, feet, CS, "open", "plain", look=(-1, -0.2), badge=False)
            c.restore()
            heads["client"] = _head(o, CS) or (x, feet - 372 * CS, 55 * CS)
            rect(k, x - 62, hip - 4, 124, 16, (0.24, 0.24, 0.26), 3082, lw=2.2)       # the creeper under him
            for wx in (x - 50, x + 50):
                ellipse(k, wx, hip + 16, 8, 8, (0.45, 0.45, 0.48), 3083 + wx, shadow=False, lw=1.6)
    return behind, front


def _flame_at():
    return bay7()


S2 = [   # shot, camera ("wide" | heads to frame), what the set shows, note
    ("1.1", (426, 520, 1.75), dict(burn=0.0), "TWO-SHOT: GARAGE 7 painted, the plan, the loyal one behind the car"),
    ("1.2", (426, 520, 1.75), dict(burn=0.4, flame=True), "SAME FRAME: the lighter's flame under 7's corner"),
    ("1.3", "wide", dict(burn=0.7, flame=True), "WIDE, frame 0's frame: the creeper out, the Client sat up"),
    ("1.4", ["client"], dict(burn=0.7, flame=True), "CLOSE, the Client to Father (Father off left)"),
    ("1.5", (426, 520, 1.75), dict(burn=0.8, flame=True), "1.1's FRAME (v2): his head turns to Father, the flame held"),
    ("1.6", ["father"], dict(burn=0.8), "CLOSE, Father alone (bodyguard 1 out): the eyebrow, a small no"),
    ("1.7", (426, 520, 1.75), dict(burn=1.0), "SAME FRAME as 1.2: the lighter shut, the mark stays"),
]


def blocking_frame(k, shot, heads_out):
    name, cam, st, note = shot
    heads = {}
    behind, front = _cast(heads, sit=name != "1.1" and name != "1.2" and name != "1.7")
    flame = st.get("flame")

    def draw(k):
        garage(k, burn=st.get("burn", 0.0), legs_out=LEGS_OUT if name not in ("1.1", "1.2") else 0.0, behind=behind,
               front=lambda k: (front(k), flame and lighter(k, _flame_at()[0] + 2, _flame_at()[1] + 46, 0.5, 1.0)))
    # pass 1: find the heads (drawn off-surface), pass 2: through the camera
    tmp = cairo.ImageSurface(cairo.FORMAT_RGB24, 8, 8)
    draw(Ctx(cairo.Context(tmp), 0))
    if cam == "wide":
        cm = FRAME0
    elif isinstance(cam, tuple):                       # a camera set by hand (the sign must be whole)
        cm = cam
    else:
        hs = [heads[h] if h != "plan" else (PLAN[0], PLAN[1] + 30, 40) for h in cam]
        cm = cf.face_cam(hs)
    frame(k, cm, draw=draw)
    heads_out.update(dict(cam=cm, heads={n: to_frame(cm, h[0], h[1]) + (h[2] * cm[2],) for n, h in heads.items()}))


def sheet_blocking(out):
    tw, th = 270, 480
    SW, SH = 40 + 4 * (tw + 30), 130 + 2 * (th + 150)
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, SW * 2, SH * 2); s.set_device_scale(2, 2)
    c = cairo.Context(s); c.set_source_rgb(0.96, 0.95, 0.92); c.paint()
    _label(c, "THE OFFER · scene 2, The Lighter · blocking v4 · the cast on the garage set, every camera by the series' rule", 30, 46, 22)
    _label(c, "cs_frame.face_cam: biggest face r 78 at y 400. Red: the apps' zones. Each frame lists its biggest face, what is in"
           " the zones, and GARAGE 7.", 30, 76, 15, col=(0.3, 0.3, 0.3))
    report = []
    for i, shot in enumerate(S2):
        info = {}
        img = _render(lambda k: (blocking_frame(k, shot, info), _guides(k.c)))
        x = 30 + (i % 4) * (tw + 30); y = 110 + (i // 4) * (th + 150)
        c.save(); c.translate(x, y); c.scale(0.5, 0.5); c.set_source_surface(img, 0, 0); c.paint(); c.restore()
        hs = info["heads"]
        big = max(hs.items(), key=lambda kv: kv[1][2] if 0 <= kv[1][0] <= W and 0 <= kv[1][1] <= H else -1)
        bad = [n for n, (hx, hy, r) in hs.items() if 0 <= hx <= W and 0 <= hy <= H and
               (hy > cf.BOTTOM or (hx > cf.RAIL[0] and cf.RAIL[1] <= hy <= cf.RAIL[2]))]
        sg = sign_state(info["cam"])
        import textwrap
        for j, ln in enumerate(textwrap.wrap("%s  %s" % (shot[0], shot[3]), 40)[:2]):
            _label(c, ln, x, y + th + 22 + j * 18, 13)
        _label(c, "biggest face: %s r %d" % (big[0], big[1][2]), x, y + th + 62, 13, col=(0.25, 0.25, 0.25))
        _label(c, "in the zones: %s · GARAGE 7: %s" % (", ".join(bad) or "nothing", sg), x, y + th + 80, 13,
               col=(0.75, 0.1, 0.1) if bad or sg == "CUT" else (0.1, 0.45, 0.2))
        report.append((shot[0], info["cam"], big[0], round(big[1][2]), bad, sg))
    s.write_to_png(out)
    return report


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else "../the-offer"
    os.makedirs(d, exist_ok=True)
    sheet_set(os.path.join(d, "of_set_v4.png"))
    sheet_plan(os.path.join(d, "of_set_plan_v4.png"))
    sheet_props(os.path.join(d, "of_set_props_v4.png"))
    for r in sheet_blocking(os.path.join(d, "of_blocking_s2_v4.png")):
        print(r)
    print("wrote", d)
