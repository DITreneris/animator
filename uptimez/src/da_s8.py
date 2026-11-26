"""THE DOUBLE AGENT (episode 15): the S8 frame, the final image 8.1 (plan: the-double-agent-s8-plan-v1.md).

Inside DON's office, looking out through the glass at the front desk floor. Frame units 540x960, drawn at 2x.
Layers (plan §2): L1 office wall, L2 the floor through the glass, L3 Don outside, L4 the glass (tint, reflections,
jambs, sill, blinds), L5 Don's chair, L6 the meeting, L7 the desk, L8 the props, L9 hands over props, L10 the light.
Mirror rule: seen from inside, Don's side (the throne) is on screen RIGHT of the tape; the counter is right outside.

  python3 da_s8.py window   ->  ../the-double-agent/da_s8_window_v1.png   step B: L1-L4, three blinds variants
"""
import math
import os
import sys
import cairo
import kit
import ps_set as pss
import fs_set4 as s4
import don_ps as dp
import da_set as ds
from kit import Ctx, INK, rect

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "the-double-agent")
W, H = 540, 960
G = (40, 104, 460, 356)                                       # the glass's opening: x 40-500, y 104-460 (v2: up, out of the captions)
JAMB = 16                                                     # the wall's thickness seen in the opening
HZ = G[1] + 150                                               # outside: the far wall meets the floor
SKIRT = (0.80, 0.74, 0.62)


def _scratch():
    return Ctx(cairo.Context(cairo.ImageSurface(cairo.FORMAT_RGB24, 4, 4)), 0)


# --- L2, L3: the floor through the glass ---------------------------------------------------------------------------------
def tape_at(t):
    """The tape's centre and half width, t 0 (near: the glass's bottom) .. 1 (far: the far wall)."""
    x0, y0, x1, y1 = 232, G[1] + G[3], 300, HZ
    return x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, 24 * (1 - t) + 5 * t


def _tape(k, gap=None):
    """The tape receding; a gap where Don peeled his strip (beside him), its torn ends ragged."""
    c = k.c
    if gap is None:                                                # v4: the line whole (the fight is across it)
        xa, ya, wa = tape_at(0.0); xb, yb, wb = tape_at(1.0)
        c.new_path(); c.move_to(xa - wa, ya); c.line_to(xa + wa, ya); c.line_to(xb + wb, yb); c.line_to(xb - wb, yb); c.close_path()
        c.set_source_rgb(*pss.TAPE); c.fill_preserve(); c.set_source_rgb(0.30, 0.22, 0.02); c.set_line_width(1.8); c.stroke()
        return
    for a, b in ((0.0, gap[0]), (gap[1], 1.0)):
        xa, ya, wa = tape_at(a); xb, yb, wb = tape_at(b)
        c.new_path(); c.move_to(xa - wa, ya); c.line_to(xa + wa, ya); c.line_to(xb + wb, yb); c.line_to(xb - wb, yb); c.close_path()
        c.set_source_rgb(*pss.TAPE); c.fill_preserve(); c.set_source_rgb(0.30, 0.22, 0.02); c.set_line_width(1.8); c.stroke()
    xa, ya, wa = tape_at(gap[0]); xb, yb, wb = tape_at(gap[1])        # the bare floor where it was: a faint glue mark
    c.new_path(); c.move_to(xa - wa, ya); c.line_to(xa + wa, ya); c.line_to(xb + wb, yb); c.line_to(xb - wb, yb); c.close_path()
    c.set_source_rgba(0.55, 0.46, 0.32, 0.35); c.fill()


def _strip(k, hx, hy, s=1.0, curl=0.35):
    """The peeled strip stuck on his palm: long (about his forearm), wide, curling, its sticky end hanging."""
    c = k.c
    w, L = 13 * s, 96 * s
    c.save(); c.translate(hx, hy)
    c.new_path()
    c.move_to(-w / 2, 0)
    c.curve_to(-w / 2 + 10 * s, L * 0.35, -w / 2 - 22 * s * curl, L * 0.7, -w / 2 + 6 * s, L)
    c.line_to(w / 2 + 6 * s, L)
    c.curve_to(w / 2 - 22 * s * curl, L * 0.7, w / 2 + 10 * s, L * 0.35, w / 2, 0)
    c.close_path()
    c.set_source_rgb(*pss.TAPE); c.fill_preserve(); c.set_source_rgb(0.30, 0.22, 0.02); c.set_line_width(1.6); c.stroke()
    c.set_source_rgba(1, 1, 1, 0.45); c.set_line_width(1.2)                       # its sheen
    c.move_to(-1, 4 * s); c.curve_to(6 * s, L * 0.35, -18 * s * curl, L * 0.7, 2 * s, L - 4 * s); c.stroke()
    c.save(); c.translate(-1 * s, L * 0.40); c.rotate(math.pi / 2 + 0.05)        # v3: the line's own marker on it,
    c.select_font_face("Permanent Marker", 0, 1); c.set_font_size(11 * s)       # "DO" of DON (cold test: "a ribbon")
    c.set_source_rgb(0.08, 0.08, 0.10); e = c.text_extents("DO"); c.move_to(-e.x_advance / 2, 4 * s); c.show_text("DO")
    c.restore()
    c.restore()


DON_POSE = ["thumbs"]                                          # v3 (Tomas 26 Nov): the salute read as a phone call 3/3
DON_AT = (330, HZ + 92)                                      # his feet, beside the gap, on his side
DON_S = 0.36


def don_outside(k, strip=True):
    """Don at his line facing the office: eyes open, the grin, the salute; the strip stuck on his saluting palm
    (drawn first, behind his hand, so the palm covers its top: stuck, not held)."""
    x, f = DON_AT
    pose = DON_POSE[0]
    o0 = dp.don(_scratch(), x, f, DON_S, pose, "grin", (-0.3, 0.2), chin=1)
    hx, hy = o0["hands"][1]
    if strip:
        _strip(k, hx + 2, hy + 4, DON_S / 0.36)
    s4.shadow(k, x, f + 2, 30)
    return dp.don(k, x, f, DON_S, pose, "grin", (-0.3, 0.2), chin=1)


def throne_from_behind(k, x, feet, s):
    """ps_set.throne_back plus its one big crown (dh_props.ceo_chair's polygon): from behind, the crown is what says
    'the throne' (v1's bare back read as a dark door)."""
    import dh_props as dhp
    pss.throne_back(k, x, feet, s, card=False)
    c = k.c
    c.save(); c.translate(x, feet); c.scale(s, s)
    kit.cut(k, [(-44, -372), (-56, -430), (-28, -402), (0, -446), (28, -402), (56, -430), (44, -372)], dhp.GOLD, lw=2.6)
    rect(k, -46, -382, 92, 14, dhp.GOLD_D, 5611, shadow=False, lw=2)
    for dx, dy in ((-56, -432), (0, -448), (56, -432)):
        kit.ellipse(k, dx, dy, 7, 7, (0.62, 0.05, 0.12), 5612 + dx, shadow=False, lw=1.6)
    c.restore()


BACKGROUND = ["fight"]                                         # v3 (Tomas 26 Nov): "Don and the robot fight for power"
FIGHT = dict(throne=(262, 0.36), don=(338, 0.36), robot=(178, 0.40))


def throne_fight(k):
    """Behind the glass: Don and the robot pull the gold throne ($49,999) across the tape line: Don toward his side
    (screen right, seen from inside), the robot toward Father's. Both lean away, arms out to the armrests."""
    import dh_props as dhp
    import robot_ps as rp
    f = DON_AT[1]
    tx, ts = FIGHT["throne"]
    old = dhp.TAG[0]; dhp.TAG[0] = True
    try:
        s4.shadow(k, tx, f + 2, 40)
        dhp.ceo_chair(k, tx, f, ts, lean=0.04)
    finally:
        dhp.TAG[0] = old
    rx, rs = FIGHT["robot"]
    s4.shadow(k, rx, f + 2, 26)
    rp.robot(k, rx, f, rs, arms=((60, 20), (88, 6)), tilt=-0.16, look=(1, 0))
    dx, dsc = FIGHT["don"]
    s4.shadow(k, dx, f + 2, 30)
    return dp.don(k, dx, f, dsc, (-92, -6, -78, 12), "confused", (-1, 0), lean=0.14)


THRONE_IN_GLASS = [False]                                     # v3: off (3/3 "a crowned door, a coffin?")


def counter_back(k):
    """The counter right outside the glass, from behind: its top edge and a plain back panel."""
    x, y, w, h = G
    rect(k, x - 6, y + h - 30, w + 12, 10, (0.86, 0.80, 0.68), 5620, shadow=False, lw=2)           # the top's edge
    rect(k, x - 6, y + h - 22, w + 12, 28, (0.78, 0.70, 0.56), 5621, shadow=False, lw=2)           # the back panel


def far_room(k, don=True):
    """L2 + L3: the far wall, its skirting, the floor, the tape with the gap, the throne's back, Don, the counter."""
    c = k.c
    x, y, w, h = G
    c.set_source_rgb(*kit.WALL); c.rectangle(x, y, w, HZ - y); c.fill()
    rect(k, x - 4, HZ - 10, w + 8, 12, SKIRT, 5601, shadow=False, lw=1.6)
    c.set_source_rgb(*kit.FLOOR); c.rectangle(x, HZ + 2, w, y + h - HZ); c.fill()
    _tape(k)
    if THRONE_IN_GLASS[0]:
        throne_from_behind(k, 452, HZ + 56, 0.34)
    if BACKGROUND[0] == "fight":
        o = throne_fight(k)
    else:
        o = don_outside(k) if don else None
    counter_back(k)
    c.set_source_rgba(0.66, 0.71, 0.75, 0.30); c.rectangle(x, y, w, h); c.fill()  # v4: cool and lower contrast (#A9B6BF):
    c.set_source_rgba(1, 1, 1, 0.08); c.rectangle(x, y, w, h); c.fill()          # the far plane, seen through glass
    return o


# --- L4: the glass -------------------------------------------------------------------------------------------------------
def blinds_tidy(k, n=8):
    """The blinds pulled up, for a wide glass: n straight parallel slats, equal gaps, the rail, two cords (opt-in
    variant of ps_set.blinds' 'up', whose wobbly stack read as wires at this width)."""
    c = k.c
    x, y, w, h = G
    top = y - 2
    def bar(x0, y0, ww, hh, col, lw):                         # straight: kit.rect's hand wobble read as wires here
        c.rectangle(x0, y0, ww, hh); c.set_source_rgb(*col); c.fill_preserve()
        c.set_source_rgb(0.42, 0.42, 0.40); c.set_line_width(lw * 0.6); c.stroke()      # v4: softer, thinner
    step = 34.0 / n
    for i in range(n):
        bar(x - 2, top + 12 + i * step, w + 4, step, pss.SLAT if i % 2 else (0.88, 0.88, 0.85), 0.9)
    bar(x - 4, top + 12 + n * step, w + 8, 7, pss.RAIL, 1.4)                                  # the bottom bar
    bar(x - 8, top, w + 16, 12, pss.RAIL, 2.0)                                                # the rail
    for cx_, pull in ((x + 12, pss.PULL), (x + w - 12, pss.PULL_R)):
        pss._cord(c, cx_, top + 14, top + 150, pull=pull)


def blinds_canon(k):
    keep = (pss.GX0, pss.GY0, pss.GW, pss.GH, pss.CORD_L, pss.CORD_R)
    x, y, w, h = G
    pss.GX0, pss.GY0, pss.GW, pss.GH, pss.CORD_L, pss.CORD_R = x, y, w, h, x + 10, x + w - 8
    try:
        pss.blinds(k, "up", 0.0, seed=5530, cords=True)
    finally:
        pss.GX0, pss.GY0, pss.GW, pss.GH, pss.CORD_L, pss.CORD_R = keep


def glass(k, blinds="tidy8"):
    """The tint, two reflections (a soft diagonal and the frame's own), the jambs and the sill with thickness, blinds."""
    c = k.c
    x, y, w, h = G
    c.set_source_rgba(*ds.GLASS, 0.12); c.rectangle(x, y, w, h); c.fill()
    c.save(); c.rectangle(x, y, w, h); c.clip()
    g = cairo.LinearGradient(x, y, x + w, y + h)                                   # a soft sheen across the glass
    g.add_color_stop_rgba(0.00, 1, 1, 1, 0.0); g.add_color_stop_rgba(0.30, 1, 1, 1, 0.10)
    g.add_color_stop_rgba(0.38, 1, 1, 1, 0.0); g.add_color_stop_rgba(0.80, 1, 1, 1, 0.0); g.add_color_stop_rgba(0.86, 1, 1, 1, 0.07)
    g.add_color_stop_rgba(0.90, 1, 1, 1, 0.0)
    c.set_source(g); c.paint()
    c.set_source_rgba(1, 1, 1, 0.10); c.set_line_width(5)                         # the frame reflected, faint
    c.rectangle(x + 14, y + 22, w - 28, h - 40); c.stroke()
    c.restore()
    # the jambs: the wall's thickness, the inner faces as trapezoids (the left lit, the right in shade)
    cut = kit.cut
    cut(k, [(x - JAMB, y - JAMB), (x, y), (x, y + h), (x - JAMB, y + h + JAMB * 0.6)], (0.80, 0.76, 0.68), shadow=False, lw=2)
    cut(k, [(x + w, y), (x + w + JAMB, y - JAMB), (x + w + JAMB, y + h + JAMB * 0.6), (x + w, y + h)], (0.62, 0.58, 0.52), shadow=False, lw=2)
    cut(k, [(x - JAMB, y - JAMB), (x + w + JAMB, y - JAMB), (x + w, y), (x, y)], (0.70, 0.66, 0.58), shadow=False, lw=2)
    rect(k, x - JAMB - 6, y + h, w + 2 * JAMB + 12, 14, (0.88, 0.85, 0.78), 5660, lw=2)        # the sill, with its shadow
    c.set_source_rgba(0, 0, 0, 0.14); c.rectangle(x - JAMB - 6, y + h + 14, w + 2 * JAMB + 12, 7); c.fill()
    if blinds == "canon":
        blinds_canon(k)
    elif blinds.startswith("tidy"):
        blinds_tidy(k, int(blinds[4:]))


def office_wall(k):
    k.c.set_source_rgb(*ds.IN_WALL); k.c.paint()


def window_only(k, blinds="tidy8"):
    """L1-L4: the office wall, the room through the glass, Don, the glass. Returns Don's rig output."""
    office_wall(k)
    x, y, w, h = G
    k.c.save(); k.c.rectangle(x, y, w, h); k.c.clip()
    o = far_room(k)
    k.c.restore()
    glass(k, blinds)
    return o


# --- sheets --------------------------------------------------------------------------------------------------------------
def _frame(draw, scale=2):
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W * scale, H * scale)
    c = cairo.Context(surf); c.scale(scale, scale)
    draw(Ctx(c, 0))
    return surf


def sheet_window(out):
    """Step B: the window with nobody inside, three blinds variants side by side, at half size, labelled."""
    cols = (("canon", "A · canon blinds (ps_set 'up')"), ("tidy8", "B · tidy, 8 slats"), ("tidy6", "C · tidy, 6 slats"))
    sw, sh = 540, 960
    big = cairo.ImageSurface(cairo.FORMAT_RGB24, sw * 3 + 80, sh + 120)
    c = cairo.Context(big); c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    c.select_font_face("Inter", 0, 1); c.set_source_rgb(0.1, 0.1, 0.1); c.set_font_size(26)
    c.move_to(20, 40); c.show_text("THE DOUBLE AGENT · S8 step B · the window, nobody inside · v1")
    for i, (bl, label) in enumerate(cols):
        f = _frame(lambda k, bl=bl: window_only(k, bl), scale=1)
        c.save(); c.translate(20 + i * (sw + 20), 70); c.set_source_surface(f, 0, 0); c.paint(); c.restore()
        c.set_source_rgb(0.1, 0.1, 0.1); c.set_font_size(20); c.move_to(20 + i * (sw + 20), sh + 100); c.show_text(label)
    big.write_to_png(out)
    print("wrote", out)


# --- L5: Don's chair -----------------------------------------------------------------------------------------------------
LEATHER, LEATHER_L = (0.13, 0.12, 0.14), (0.30, 0.28, 0.32)
CHAIR_VARIANT = ["D"]


def chair(k, x, top, s=1.0, variant=None):
    """Don's executive chair from the front: black leather, a lighter edge, buttons, a headrest. Its bottom is hidden
    by the sitter and the desk. A: rounded tufted back; B: high back with a separate headrest; C: mid back, wider."""
    c = k.c
    v = variant or CHAIR_VARIANT[0]
    c.save(); c.translate(x, top); c.scale(s, s)
    if v == "A":
        pts = [(-58, 260), (-64, 90), (-56, 30), (-34, 4), (0, -2), (34, 4), (56, 30), (64, 90), (58, 260)]
        kit.cut(k, pts, LEATHER, lw=2.6)
        kit.cut(k, [(px * 0.86, 8 + py * 0.95) for px, py in pts], LEATHER_L, shadow=False, lw=1.6)
        kit.cut(k, [(px * 0.80, 12 + py * 0.92) for px, py in pts], LEATHER, shadow=False, lw=0)
        for bx, by in ((-24, 56), (24, 56), (0, 90), (-24, 124), (24, 124), (0, 158)):
            kit.ellipse(k, bx, by, 3.2, 3.2, LEATHER_L, 5700 + bx + by, shadow=False, lw=0.8)
    elif v == "B":
        kit.cut(k, [(-34, 2), (34, 2), (38, 46), (-38, 46)], LEATHER, lw=2.4)                   # the headrest
        kit.cut(k, [(-58, 260), (-62, 70), (-50, 54), (50, 54), (62, 70), (58, 260)], LEATHER, lw=2.6)
        c.set_source_rgb(*LEATHER_L); c.set_line_width(2)
        for yy in (100, 150, 200):
            c.move_to(-50, yy); c.line_to(50, yy); c.stroke()
    elif v == "C":
        kit.cut(k, [(-74, 260), (-78, 120), (-60, 70), (60, 70), (78, 120), (74, 260)], LEATHER, lw=2.6)
        c.set_source_rgb(*LEATHER_L); c.set_line_width(2.2)
        c.move_to(-58, 84); c.curve_to(-20, 74, 20, 74, 58, 84); c.stroke()
    else:                                                     # D: brown leather, wide rounded back, channels, armrests
        BR, BR_L, BR_D = (0.22, 0.16, 0.13), (0.40, 0.29, 0.22), (0.13, 0.09, 0.07)   # v4: #382820, darker than his coat
        c.new_path(); r = 34
        c.move_to(-66 + r, 0); c.line_to(66 - r, 0); c.curve_to(66, 0, 72, 10, 72, r)
        c.line_to(70, 250); c.line_to(-70, 250); c.line_to(-72, r); c.curve_to(-72, 10, -66, 0, -66 + r, 0); c.close_path()
        c.set_source_rgb(*BR); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.6); c.stroke()
        c.set_source_rgb(*BR_L); c.set_line_width(3)                      # the lit rim
        c.move_to(-60, 40); c.curve_to(-60, 12, -50, 8, -30, 8); c.line_to(30, 8); c.stroke()
        c.set_source_rgb(*BR_D); c.set_line_width(2)                      # vertical channels, the headrest seam
        for xx in (-36, -12, 12, 36):
            c.move_to(xx, 56); c.line_to(xx, 240); c.stroke()
        c.move_to(-62, 52); c.curve_to(-20, 60, 20, 60, 62, 52); c.stroke()
        for sx in (-1, 1):                                                # armrests, either side of the sitter
            kit.cut(k, [(sx * 66, 196), (sx * 104, 196), (sx * 108, 214), (sx * 70, 216)], BR_D, lw=2.2)
            rect(k, sx * 86 - 6, 214, 12, 40, (0.20, 0.20, 0.22), 5760 + sx, shadow=False, lw=1.6)
    c.restore()


# --- L7, L8: the desk and its props --------------------------------------------------------------------------------------
DESK_TOP_Y, DESK_NEAR_Y, DESK_FRONT_Y = 652, 712, 712   # v2: the plan out of the bottom quarter (y > 720)       # far edge, near edge (the top plane), the front panel's top
DESK_TOP = (0.76, 0.58, 0.40)                                # the top plane, lighter than the front (lit from above)


def desk(k):
    """Don's desk across the frame: a visible top plane (far edge to near edge), a shorter front panel (v1 was a brown
    wall: review), the near edge's lip; a soft shadow under the lip."""
    c = k.c
    kit.cut(k, [(-20, DESK_TOP_Y), (560, DESK_TOP_Y), (580, DESK_NEAR_Y), (-40, DESK_NEAR_Y)], DESK_TOP, shadow=False, lw=2.4)
    c.set_source_rgb(*ds.IN_FLOOR); c.rectangle(-20, DESK_FRONT_Y, 600, 300); c.fill()      # v4: the office floor under it
    rect(k, -20, DESK_FRONT_Y, 580, 150, (0.40, 0.26, 0.17), 5720, shadow=False, lw=2.4)      # the front, 25 % shorter (#65432F)
    c.set_source_rgba(0, 0, 0, 0.20); c.rectangle(-20, DESK_FRONT_Y + 150, 600, 14); c.fill()  # its shadow on the floor
    for dx in (40, 300):                                                                     # two drawers with a bevel
        rect(k, dx, DESK_FRONT_Y + 26, 200, 70, ds.DESK, 5722 + dx, shadow=False, lw=1.8)
        c.set_source_rgba(1, 1, 1, 0.18); c.set_line_width(2.5); c.move_to(dx + 4, DESK_FRONT_Y + 30); c.line_to(dx + 196, DESK_FRONT_Y + 30); c.stroke()
        c.set_source_rgba(0, 0, 0, 0.25); c.move_to(dx + 4, DESK_FRONT_Y + 93); c.line_to(dx + 196, DESK_FRONT_Y + 93); c.stroke()
        rect(k, dx + 84, DESK_FRONT_Y + 56, 32, 8, (0.80, 0.66, 0.30), 5723 + dx, shadow=False, lw=1.2)
    rect(k, -30, DESK_NEAR_Y - 4, 600, 10, ds.DESK, 5721, shadow=False, lw=2)                   # the lip
    c.set_source_rgba(0, 0, 0, 0.18); c.rectangle(-30, DESK_NEAR_Y + 6, 600, 8); c.fill()


def prop_shadow(k, x, y, w):
    s4.shadow(k, x, y, w)


def blueprint(k, x, y, s=1.0, ang=-0.06):
    """The Client's blueprint as what it is: MY GARAGES, ten garages, bay 7 ringed (acts_ob v6/v7, opt-in flags set and
    restored), lying on the desk's top plane (foreshortened)."""
    import acts_ob as ac
    old = (ac.GARAGES[0], ac.TITLE[0])
    ac.GARAGES[0], ac.TITLE[0] = True, True
    try:
        prop_shadow(k, x + 4, y + 26 * s * 0.42, 66 * s)
        c = k.c
        c.save(); c.translate(x, y); c.rotate(ang); c.scale(1.0, 0.42)
        ac.plan_open(k, 0, 0, s)
        c.restore()
    finally:
        ac.GARAGES[0], ac.TITLE[0] = old


def props(k):
    """L8 alone, at their places (the sheet; the frame calls the same)."""
    blueprint(k, *PLAN_AT)
    prop_shadow(k, 384, 702, 18); ds.pam_mug(k, 378, 702, 1.15)


def sheet_furniture(out):
    """Step C: three chairs (colour and silhouette at 270 px), the desk with its props."""
    big = cairo.ImageSurface(cairo.FORMAT_RGB24, 1700, 1100)
    c = cairo.Context(big); c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    k = Ctx(c, 0)
    c.select_font_face("Inter", 0, 1); c.set_source_rgb(0.1, 0.1, 0.1); c.set_font_size(26)
    c.move_to(20, 40); c.show_text("THE DOUBLE AGENT · S8 step C · Don's chair, the desk, the props · v1")
    for i, v in enumerate("ABD"):
        x = 130 + i * 260
        c.set_source_rgb(*ds.IN_WALL); c.rectangle(x - 110, 70, 220, 380); c.fill()
        chair(k, x, 110, 1.2, v)
        sil = cairo.ImageSurface(cairo.FORMAT_ARGB32, 220, 380)          # the same at 270-px feed size, as a silhouette
        cc = cairo.Context(sil); kk = Ctx(cc, 0); chair(kk, 110, 40, 1.2, v)
        cc.set_operator(cairo.OPERATOR_IN); cc.set_source_rgb(0, 0, 0); cc.paint()
        c.save(); c.translate(x - 55, 470); c.scale(0.5, 0.5); c.set_source_surface(sil, 0, 0); c.paint(); c.restore()
        c.set_source_rgb(0.1, 0.1, 0.1); c.set_font_size(20); c.move_to(x - 100, 690); c.show_text("%s · %s" % (v, (
            "rounded, tufted", "high back + headrest", "brown leather, armrests")[i]))
    c.save(); c.translate(820, 60); c.scale(1.0, 1.0)
    c.set_source_rgb(*ds.IN_WALL); c.rectangle(0, 0, 540, 1000 - 60); c.fill()
    c.translate(0, -700); desk(k); props(k)
    c.restore()
    c.set_source_rgb(0.1, 0.1, 0.1); c.set_font_size(20); c.move_to(820, 1080)
    c.show_text("the desk: top plane + a shorter front; the blueprint (MY GARAGES), Pam's mustard mug, Don's white mug")
    big.write_to_png(out)
    print("wrote", out)


# --- L6, the meeting, and the whole frame ---------------------------------------------------------------------------------
FATHER_FOLDED = (-20, 140, 20, -140)                          # arms folded, hands together at the chest (sheet D/E)
V6 = [False]   # opt-in (26 Nov, Tomas: "to the canon"): V5 plus Pam in her office canon (dusty-rose lips, no brooch; pm_ps's
               # berry lips and flower are episode 8's touches)
V5 = [False]   # opt-in (26 Nov, after the cast analysis and the Father sheet's cold test): Sofía in her episode 15 outfit
               # (sofia_da, the job interview, charcoal); Father leaning back, the ring hand on the chair's armrest, the other
               # on his belly (the fold misread 3 times: "checking a watch"). False draws the locked v4 exactly.
PLAN_AT = (226, 682, 1.40)


def seated(k, draw):
    """cafe_kit.seated: only what is above the desk's far edge is drawn (legs never show behind the desk)."""
    c = k.c
    c.save(); c.rectangle(-2000, -2000, 5000, 2000 + DESK_TOP_Y + 2); c.clip()
    out = draw()
    c.restore()
    return out


def meeting(k):
    """The four at Don's desk, working on the plan, nobody looking at the camera (cold test v1: 'a judging panel')."""
    import client_ps as cps
    import dh_cast as dc
    import sofia_ps as sp
    import pm_ps as pm
    heads = {}
    px, py, _ = PLAN_AT
    chair(k, 336, 378, 1.0, "D")
    c = k.c                                                    # v4: a soft side light on the chair behind Father (separation)
    g = cairo.RadialGradient(300, 470, 10, 300, 470, 120)
    g.add_color_stop_rgba(0, 0.95, 0.85, 0.70, 0.22); g.add_color_stop_rgba(1, 0.95, 0.85, 0.70, 0.0)
    c.save(); c.rectangle(264, 378, 144, 280); c.clip(); c.set_source(g); c.paint(); c.restore()
    if V5[0]:
        import hands_ps as hp
        import hands_v4 as hv
        import kit as kit_
        import sofia_da as sd
        hv.enable(); kit_.HAND[0] = hp.hand                    # the canon hand for both (rules-hands: one hand for the cast)
        try:
            hp.reset("quiet", "quiet")
            heads["father"] = seated(k, lambda: _father_rest(k))
            heads["sofia"] = seated(k, lambda: sd.with_board(k, 444, 748, 0.66, "binder", face_kind="interested",
                                                              look=(-1.0, 0.9), lift=62)["head"])    # reading: board_two
        finally:
            hv.disable(); kit_.HAND[0] = None
    else:
        heads["father"] = seated(k, lambda: dc.father(k, 336, 706, 0.78, FATHER_FOLDED, "hard", (-0.6, 0.9))["head"])
        heads["sofia"] = seated(k, lambda: sp.sofia(k, 444, 748, 0.66, "hold", "smile", look=(-1.0, 0.9))["head"])
    heads["pam"] = seated(k, lambda: pam_taking(k)["head"])
    return heads


def _father_rest(k, x=336, feet=706, s=0.78):
    import dh_cast as dc
    """V5: leaning back in Don's chair, the ring hand (screen right) on the armrest, the other flat on his belly; his
    sleeves in the dark velvet so the arms read on the jacket (the Father sheet v4's 8.1)."""
    import kit as kit_
    from cand_bc import ik
    c = k.c
    bt = -300 * 1.12 + 78
    rest = ik(-40, bt + 14, 4, bt + 112, 48, 48, -1) + ik(40, bt + 14, 80, bt + 146, 48, 48, 1)
    seat = feet + (bt + 150) * s
    orig = kit_.arm
    kit_.arm = lambda k_, sx, sy, a1, a2, col, *a, **kw: orig(k_, sx, sy, a1, a2, dc.VELVET_D if col == dc.VELVET else col, *a, **kw)
    try:
        for p_ in (0, 1):                                      # pass 0 finds the ring hand; the armrest goes under it; pass 1 draws
            if p_ == 0:
                c.push_group()
            c.save(); c.translate(x, seat); c.rotate(-0.05); c.translate(-x, -seat)
            o = dc.father(k, x, feet, s, rest, "hard", (-0.6, 0.9))
            c.restore()
            if p_ == 0:
                c.pop_group()
                hx, hy = o["hands"][1]
                kit_.rect(k, hx - 24 * s, hy + 7 * s, 50 * s, 13 * s, (0.30, 0.22, 0.17), 5100, lw=2)   # the armrest, under the hand
    finally:
        kit_.arm = orig
    return o["head"]


PAM_AT = (212, 762, 0.66)


def _pam_pose():
    """v3: both of Pam's hands on the plan's near edge, pulling it to her (cold test v2: 'handed to the boss' 2/3).
    pam_mf.ik targets in her body units (feet origin, y up negative), from the plan's place in the frame."""
    import pm_ps as pm
    x, feet, s = PAM_AT
    px, py, sc = PLAN_AT
    ty = (py - 14 - feet) / s                                  # the far edge, at its two corners, clear of the title
    pose = pm.pm.ik(-1, (px - 84 - x) / s, ty) + pm.pm.ik(1, (px + 98 - x) / s, ty + 6)
    pm.P_HANDS[pose] = ("palm", "palm")
    return pose


def pam_taking(k):
    import pm_ps as pm
    x, feet, s = PAM_AT
    kw = dict(lips="rose", brooch=False) if V6[0] else {}
    return pm.pam(k, x, feet, s, _pam_pose(), "neutral", (0.1, 1.0), mug=False, **kw)


def pam_hands_over(k):
    """Her forearms and hands drawn again over the desk and the plan: the same drawing, clipped to a strip round each
    hand (lesson 224: the hand drawn again over the object)."""
    import pm_ps as pm
    x, feet, s = PAM_AT
    o = pm.pam(_scratch(), x, feet, s, _pam_pose(), "neutral", (0.1, 1.0), mug=False)
    c = k.c
    c.save(); c.new_path()
    for hx, hy in o["hands"]:
        c.rectangle(hx - 16, DESK_TOP_Y - 6, 32, hy - DESK_TOP_Y + 20)
    c.clip()
    pam_taking(k)
    c.restore()


def client_over_desk(k):
    """The Client leaning over the desk, drawn after it (14's booth: clip_hip, the hip on the desk's top plane), his oily
    finger on the plan's near-left bay (cause and effect in one frame, lesson 132)."""
    import client_ps as cps
    import client_on3 as co
    px, py, _ = PLAN_AT
    s = 0.70
    o = cps.cast_client(k, 62, 712 - co.HIP * s, s, look=(1.0, 1.0), targets=[(px - 190, py + 14), (px - 74, py + 20)],
                        clip_hip=True, hands={1: "point"}, aim=(px - 50, py + 18))
    return {"client": o["head"]}


def frame(k):
    """The S8 frame v2: L1-L4 (the window), L5-L6 (the chair, the meeting), L7-L8 (the desk, the props), L10 light."""
    o = window_only(k, "tidy8")
    heads = {"don": o["head"]}
    heads.update(meeting(k))
    desk(k); props(k)
    pam_hands_over(k)
    heads.update(client_over_desk(k))
    light(k)
    return heads


def light(k):
    """of_scenes.grade's idea, local (opt-in there): the office darker at the top and the corners and toward the near
    desk; the glass stays the brightest area."""
    c = k.c
    c.save()
    g = cairo.LinearGradient(0, 0, 0, 110)                      # v4 (review): only a light top; the brown vignette is gone
    g.add_color_stop_rgba(0, 0.05, 0.05, 0.08, 0.08); g.add_color_stop_rgba(1, 0.05, 0.05, 0.08, 0.0)
    c.set_source(g); c.rectangle(0, 0, W, 110); c.fill()
    c.restore()


def still(out):
    surf = _frame(frame, scale=2)
    surf.write_to_png(out)
    print("wrote", out)


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "window"
    out = sys.argv[2] if len(sys.argv) > 2 else OUT
    os.makedirs(out, exist_ok=True)
    if what == "window":
        sheet_window(os.path.join(out, "da_s8_window_v1.png"))
    elif what == "frame":
        still(os.path.join(out, "da_s8_final_v4.png"))
    elif sys.argv[1] == "frame7":
        import da_arms
        da_arms.setup()                                        # v7: the thumbs mirrored per arm (no two left hands)
        V5[0] = True; V6[0] = True
        still(os.path.join(out, "da_s8_final_v7.png"))
    elif sys.argv[1] == "frame6":
        V5[0] = True; V6[0] = True
        still(os.path.join(out, "da_s8_final_v6.png"))
    elif sys.argv[1] == "frame5":
        V5[0] = True
        still(os.path.join(out, "da_s8_final_v5.png"))
    elif what == "furniture":
        sheet_furniture(os.path.join(out, "da_s8_furniture_v1.png"))
