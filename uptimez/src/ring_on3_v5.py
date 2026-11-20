"""OFFICE NOIR 3: the ring, set v4 (19 Nov; ring_on3_v1.py to _v3.py are pinned). After cold test 3 and /grill-me: the
plan carries its title block, 10 GARAGES (props_on3 v2, title=True).
v3 (ring_on3_v1.py and _v2.py are pinned). After cold test 2 and /grill-me:
far_ropes=False leaves the far ropes to the cast (the Client comes through them, Pam holding two up);
side_a=False does the same for A's side ropes; plan_pov() is
the plan as he sees it from below, a shot of its own (5.1b), because a look at it was not read.
v2 (after cold test 1): After the cold test of v1's frames (2 of 5):
the doorway is dark unless door=True (Don's shots); the ringside hats sit lower, clear of Sofia's legs; side_rope() draws
one side's ropes again, over a figure who is still coming through them; R2 and R3 are re-aimed.
v1: The room of beats 05 to 07, drawn once and framed by camera setups.
World: 720 wide; the canvas' front edge is at F. Three zones, each with one job:
  A (0-250)    his corner: the post with a pale pad, the stool with the folder, the bucket. Repair and the glove gags.
  B (250-480)  centre, under the lamp and his plan on its two cords. The fight, the ask, the punch.
  C (480-720)  its corner: the post with a socket, the cable, the oil can. The machine, serviced.
Depth, back to front: the hall and the way out (a lit doorway behind C) / the far crowd / the far ropes / the canvas
and the cast / the near ropes (masters only) / the apron, Sofia's lane / the ringside hats.
draw_ring(k, mid, front, near, money, swing): mid and front are lists of callables that draw the cast, back to front.
Cameras: CAMS[name] = (cx, cy, zoom) for view(); frame(cam, mid, front, ...) returns a 540x960 surface in the dream's look.
Nothing here changes an earlier module."""
import math
import cairo
import kit
import props_on3 as pr
import cast_on3 as ca
import client_on3 as b
import robot_on3 as r
import client_sheet_on3 as csh
from kit import Ctx, INK, cut, rect, ellipse

WW, F = 720, 1400
FAR = F - 110                                              # the canvas' far edge
NEAR = F + 30                                              # and its near edge
POST_N, POST_F = (40, 680), (130, 590)                     # near and far posts, x
LAMP = (365, 730)
PLAN = (300, 1010, 1.1)                                    # props_on3.plan_hung: x, y, s; its hung end is over the gap
DOOR = (548, FAR - 250, 62, 150)                           # the way out, behind C
SC = 0.70                                                  # the scale of the series' figures on this set
ZONES = [("A", "his corner: repair, the glove gags", 0, 250, (0.80, 0.25, 0.22)),
         ("B", "centre, under the lamp and his plan: the fight", 250, 480, (0.20, 0.45, 0.85)),
         ("C", "its corner: the machine, serviced", 480, 720, (0.13, 0.55, 0.50))]
HOME = {"pam": (88, F - 16, SC), "client_stool": (152, F - 36, SC * b.REL), "client": (296, F - 42, SC * b.REL),
        "referee": (368, F - 88, SC * ca.REL_REF), "robot": (452, F - 46, SC * r.REL), "robot_corner": (600, F - 52, SC * r.REL),
        "sofia": (585, F + 108, 0.92)}
STOOL = (152, F - 36)
CAMS = {"R1": (332, 1140, 0.9),                            # the master: the ring post to post, the lamp, the plan, the lane
        "R2": (392, 1108, 1.34),                           # centre: the two of them and the plan's end over them
        "R3": (200, 1160, 1.70),                           # his corner, square on
        "R4": (578, 1178, 1.80),                           # its corner
        "R6": (340, 1050, 1.60)}                           # low, looking up at the plan (the canvas at the frame's foot)
HALL = (0.10, 0.10, 0.12)
ROPE, ROPE_FAR = (0.90, 0.90, 0.92), (0.50, 0.50, 0.54)
CANVAS, APRON = (0.64, 0.64, 0.66), (0.16, 0.16, 0.18)


def view(c, cx, cy, z):
    """World point (cx, cy) to the frame's centre, zoom z."""
    c.translate(270, 480); c.scale(z, z); c.translate(-cx, -cy)


def to_frame(cam, x, y):
    cx, cy, z = cam
    return 270 + (x - cx) * z, 480 + (y - cy) * z


def shadow(k, x, y, w):
    c = k.c
    c.save(); c.translate(x, y); c.scale(w, w * 0.16); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
    c.set_source_rgba(0, 0, 0, 0.30); c.fill()


def _hat(c, x, top, rr, hat=True):
    c.arc(x, top, rr, 0, 2 * math.pi); c.fill()
    if hat:
        c.rectangle(x - rr * 1.5, top - rr * 0.7, rr * 3, rr * 0.3); c.fill()
        c.rectangle(x - rr * 0.9, top - rr * 1.6, rr * 1.8, rr); c.fill()


def stool(k, x, y, folder=True, seed=0):
    c = k.c
    c.set_source_rgb(*INK); c.set_line_width(5)
    for dx in (-22, 22):
        c.move_to(x + dx * 0.7, y - 44); c.line_to(x + dx, y); c.stroke()
    cut(k, [(x - 30, y - 52), (x + 30, y - 52), (x + 28, y - 42), (x - 28, y - 42)], (0.42, 0.42, 0.45), shadow=False, lw=2)
    if folder:                                             # the folder, on the seat, its tab up
        cut(k, [(x - 24, y - 60), (x + 22, y - 62), (x + 24, y - 53), (x - 22, y - 51)], (0.86, 0.80, 0.62), shadow=False, lw=1.8)
        cut(k, [(x + 6, y - 66), (x + 20, y - 67), (x + 20, y - 61), (x + 6, y - 60)], (0.86, 0.80, 0.62), shadow=False, lw=1.4)


def _post(k, x, top, base, w, pad=None, socket=False):
    c = k.c
    rect(k, x - w / 2, top, w, base - top, (0.34, 0.34, 0.37), 0, shadow=False, lw=2)
    ellipse(k, x, top, w * 0.62, w * 0.3, (0.52, 0.52, 0.55), 1, shadow=False, lw=1.8)
    if pad:
        rect(k, x - w * 0.8, top + 16, w * 1.6, 74, pad, 2, shadow=False, lw=2)
    if socket:
        rect(k, x - 9, top + 40, 18, 24, (0.80, 0.80, 0.82), 3, shadow=False, lw=1.6)
        c.set_source_rgb(*INK)
        for dy in (48, 56):
            c.rectangle(x - 4, top + dy, 8, 2.4); c.fill()


def side_rope(k, side=0):
    """One side's three ropes (0: A's side, 1: C's), far post to near post. A mid callable can draw them again over a
    figure who is coming through them."""
    c = k.c
    fx, nx = POST_F[side], POST_N[side]
    c.set_source_rgb(*ROPE_FAR)
    for t in (92, 62, 32):
        c.set_line_width(5); c.move_to(fx, FAR - t); c.line_to(nx, NEAR - t * 1.25); c.stroke()


def draw_ring(k, mid=(), front=(), near=True, money=False, swing=0.0, folder=True, hats=True, door=False, side_a=True, far_ropes=True):
    """The whole set in world coordinates. mid: the cast on the canvas, back to front. front: on the apron (Sofia).
    near: the three near ropes and their posts (the masters; a camera inside the ropes leaves them out).
    money: cuffs waving notes in the far crowd (5.1). swing: the plan's swing, radians (6.4, 7.3)."""
    c = k.c
    c.set_source_rgb(*HALL); c.rectangle(-400, -200, WW + 800, F + 800); c.fill()
    g = cairo.RadialGradient(LAMP[0], F - 260, 30, LAMP[0], F - 260, 760)                  # the haze the lamp lights
    g.add_color_stop_rgba(0, 0.70, 0.70, 0.72, 1); g.add_color_stop_rgba(0.5, 0.36, 0.36, 0.39, 1)
    g.add_color_stop_rgba(1, *HALL, 1)
    c.set_source(g); c.rectangle(-400, -200, WW + 800, FAR + 200); c.fill()
    dx, dy, dw, dh = DOOR                                                                  # the way out: a lit doorway
    c.set_source_rgb(*((0.50, 0.50, 0.50) if door else (0.15, 0.15, 0.17))); c.rectangle(dx, dy, dw, dh); c.fill()
    c.set_source_rgb(*HALL); c.set_line_width(5); c.rectangle(dx, dy, dw, dh); c.stroke()
    c.set_source_rgb(0.05, 0.05, 0.06)                                                     # the far crowd: one dark mass
    c.rectangle(-400, FAR - 62, WW + 800, 66); c.fill()
    x, i = -380.0, 0
    while x < WW + 400:
        rr = (12, 16, 10, 14, 17, 11)[i % 6]; top = FAR - 62 - (3, 11, 0, 8, 4, 13)[i % 6]
        if not (dx - 14 < x < dx + dw + 14):                                               # the aisle to the door stays clear
            _hat(c, x, top, rr, i % 3 != 1)
            if money and i % 4 == 1 and 60 < x < WW - 60:                                  # a cuff, a note
                c.set_source_rgb(0.86, 0.86, 0.84); c.rectangle(x + rr, top - 46, 9, 30); c.fill()
                c.save(); c.translate(x + rr + 4, top - 50); c.rotate(-0.3); c.rectangle(-13, -8, 26, 14); c.fill(); c.restore()
                c.set_source_rgb(0.05, 0.05, 0.06)
        x += (44, 62, 38, 70, 50, 56)[i % 6]; i += 1
    c.set_source_rgb(0.05, 0.05, 0.06); c.rectangle(dx - 10, FAR - 100, dw + 20, 104); c.fill()
    c.set_source_rgb(0.30, 0.30, 0.32); c.rectangle(dx + 6, dy + dh, dw - 12, FAR + 4 - dy - dh); c.fill()   # the aisle's floor
    for px_ in POST_F:                                                                     # the far posts and ropes
        _post(k, px_, FAR - 104, FAR + 4, 14)
    c.set_source_rgb(*ROPE_FAR)
    for ry in (FAR - 92, FAR - 62, FAR - 32) if far_ropes else ():       # far_ropes=False: the cast draws them (5.1a)
        c.rectangle(POST_F[0], ry, POST_F[1] - POST_F[0], 3.5); c.fill()
    cut(k, [(POST_F[0] - 26, FAR), (POST_F[1] + 26, FAR), (POST_N[1] + 34, NEAR), (POST_N[0] - 34, NEAR)], CANVAS, shadow=False, lw=2.4)
    g = cairo.RadialGradient(LAMP[0], F - 40, 20, LAMP[0], F - 40, 330)                    # the lamp's pool on the canvas
    g.add_color_stop_rgba(0, 1, 1, 1, 0.42); g.add_color_stop_rgba(1, 1, 1, 1, 0)
    c.save(); c.rectangle(-400, FAR, WW + 800, NEAR - FAR); c.clip(); c.set_source(g); c.paint(); c.restore()
    lx, ly = LAMP                                                                          # the cone: the smoke shows it
    c.new_path(); c.move_to(lx - 60, ly + 10); c.line_to(lx + 60, ly + 10); c.line_to(POST_F[1] + 40, FAR + 40)
    c.line_to(POST_F[0] - 40, FAR + 40); c.close_path()
    g = cairo.LinearGradient(0, ly, 0, FAR)
    g.add_color_stop_rgba(0, 1, 1, 1, 0.20); g.add_color_stop_rgba(1, 1, 1, 1, 0.04)
    c.set_source(g); c.fill()
    c.set_source_rgba(1, 1, 1, 0.10); c.set_line_width(16); c.set_line_cap(1)              # smoke
    for sx_, sy_ in ((250, 960), (440, 860), (350, 1120)):
        c.move_to(sx_ - 70, sy_); c.curve_to(sx_ - 20, sy_ - 40, sx_ + 30, sy_ + 30, sx_ + 90, sy_ - 14); c.stroke()
    c.set_line_cap(0)
    cut(k, [(lx - 74, ly + 12), (lx - 34, ly - 34), (lx + 34, ly - 34), (lx + 74, ly + 12)], (0.22, 0.22, 0.25), shadow=False, lw=2.4)
    c.set_source_rgb(0.98, 0.98, 0.96); c.save(); c.translate(lx, ly + 12); c.scale(58, 9); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
    c.set_source_rgb(0.22, 0.22, 0.25); c.set_line_width(3); c.move_to(lx, ly - 34); c.line_to(lx, ly - 900); c.stroke()
    px_, py_, ps_ = PLAN                                                                   # his plan, on its two cords
    c.save(); c.translate(px_ + 46 * ps_, ly); c.rotate(swing); c.translate(-(px_ + 46 * ps_), -ly)
    pr.plan_hung(k, px_, py_, ps_, top=ly - 40, title=True)
    c.restore()
    c.set_source_rgb(*ROPE_FAR)                                                            # the side ropes, far post to near
    for (fx, nx) in ((POST_F[0], POST_N[0]), (POST_F[1], POST_N[1]))[0 if side_a else 1:]:
        for t in (92, 62, 32):
            c.set_line_width(3.5 + 1.5); c.move_to(fx, FAR - t); c.line_to(nx, NEAR - t * 1.25); c.stroke()
    _post(k, POST_N[0], NEAR - 128, NEAR + 6, 22, pad=(0.82, 0.82, 0.80))                  # his post: a pale pad
    _post(k, POST_N[1], NEAR - 128, NEAR + 6, 22, socket=True)                             # its post: a socket
    stool(k, *STOOL, folder=folder)
    ca.bucket(k, POST_N[0] + 44, NEAR - 6, 0.5)
    r.oil_can(k, POST_N[1] - 40, NEAR - 12, 0.5)
    for fn in mid:
        fn(k)
    if near:                                                                               # the near ropes, in front of them
        for i, t in enumerate((40, 78, 115)):
            c.set_source_rgb(*ROPE); c.rectangle(POST_N[0], NEAR - t, POST_N[1] - POST_N[0], 6); c.fill()
            c.set_source_rgba(0, 0, 0, 0.35); c.rectangle(POST_N[0], NEAR - t + 6, POST_N[1] - POST_N[0], 2); c.fill()
    c.set_source_rgb(*APRON); c.rectangle(-400, NEAR, WW + 800, 500); c.fill()             # the apron: Sofia's lane
    c.set_source_rgb(0.74, 0.74, 0.76); c.rectangle(POST_N[0] - 34, NEAR, POST_N[1] - POST_N[0] + 68, 7); c.fill()
    c.set_source_rgb(0.24, 0.24, 0.27); c.rectangle(-400, NEAR + 66, WW + 800, 60); c.fill()   # the floor she walks on
    for fn in front:
        fn(k)
    if hats:                                                                               # ringside: big, dark, nearest us
        c.set_source_rgb(0.03, 0.03, 0.04)
        c.rectangle(-400, F + 236, WW + 800, 400); c.fill()
        x, i = -30.0, 0
        while x < WW + 60:
            rr = (30, 38, 26, 34)[i % 4]
            _hat(c, x, F + 232 - (0, 12, 5, 16)[i % 4], rr * 0.8, i % 3 != 2)
            x += (120, 150, 104, 136)[i % 4]; i += 1


def frame(cam, mid=(), front=(), noir=True, **kw):
    """A 540x960 camera frame of the set. cam: a name in CAMS or (cx, cy, zoom)."""
    cam = CAMS[cam] if isinstance(cam, str) else cam
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(s); k = Ctx(c, 0)
    c.save(); view(c, *cam)
    draw_ring(k, mid, front, **kw)
    c.restore()
    if noir:
        csh.noir(s)
    return s


def plan_pov(glove=True, swing=0.0, rise=0.0):
    """5.1b, his view: the plan from below, the lamp behind it, and one red glove coming up into the frame toward it.
    Its own drawing (not a framing of the set). Returns a 540x960 surface in the dream's look."""
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(s); k = Ctx(c, 0)
    c.set_source_rgb(*HALL); c.paint()
    g = cairo.RadialGradient(270, 170, 20, 270, 170, 620)                                 # the lamp, straight overhead
    g.add_color_stop_rgba(0, 1, 1, 1, 1); g.add_color_stop_rgba(0.12, 0.86, 0.86, 0.88, 1)
    g.add_color_stop_rgba(0.5, 0.40, 0.40, 0.43, 1); g.add_color_stop_rgba(1, *HALL, 1)
    c.set_source(g); c.paint()
    c.set_source_rgb(0.20, 0.20, 0.23); c.set_line_width(22)                              # the shade's rim, seen from under it
    c.save(); c.translate(270, 170); c.scale(1, 0.62); c.arc(0, 0, 150, 0, 2 * math.pi); c.restore(); c.stroke()
    c.set_source_rgba(1, 1, 1, 0.10); c.set_line_width(26); c.set_line_cap(1)
    for sx_, sy_ in ((150, 330), (380, 620)):
        c.move_to(sx_ - 110, sy_); c.curve_to(sx_ - 30, sy_ - 50, sx_ + 50, sy_ + 40, sx_ + 150, sy_ - 20); c.stroke()
    c.set_line_cap(0)
    c.save(); c.translate(270, 170); c.rotate(swing); c.translate(-270, -170)
    pr.plan_hung(k, 150, 420, 3.0, top=170, title=True)                                               # big: the ten bays can be counted
    c.restore()
    if glove:                                                                             # his glove, up toward it, short of it
        ang = -1.36
        ux, uy = math.cos(ang), math.sin(ang)
        hx, hy = 372, 820 + rise                             # rise > 0: the glove is still on its way up (the rough)
        c.save(); c.translate(hx, hy); c.scale(2.3, 2.3); c.translate(-hx, -hy)
        px_, py_ = -uy, ux
        cut(k, [(hx - ux * 30 + px_ * 22, hy - uy * 30 + py_ * 22), (hx - ux * 30 - px_ * 22, hy - uy * 30 - py_ * 22),
                (hx - ux * 160 - px_ * 26, hy - uy * 160 - py_ * 26), (hx - ux * 160 + px_ * 26, hy - uy * 160 + py_ * 26)], b.KEY, shadow=False, lw=2.4)
        b._glove(k, hx, hy, ux, uy, 1, 77)
        c.restore()
    csh.noir(s)
    return s
