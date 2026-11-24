"""PICK A SIDE (episode 14): stage 3, the set. The front desk v4 (fs_set4.py) as it is, with this episode's pieces drawn
on top, all here (nothing in fs_set4, set_ob or dh_props changes). Tomas, 23 Nov, /grill-me:
- the glass door SHUT, with blinds: white horizontal slats on a rail, a cord each side (Don's on the left, the robot's on
  the right); states up, down (u 0..1), torn (the rail hanging from one bracket, the slats gone: they are on Don), rehung;
- the tape: yellow office tape at world x 560, back wall to the camera, "DON" and an arrow in black marker on his side;
- the throne's price tag $49,999 on a string from the crown; spun (2.2), the tag shows its blank back to us;
- Pam's phone on the counter's left end: dark, or lit with INVITATION · DAD (lesson 191); a close-up for 5.7;
- the step stool (5.3-5.6); Father's booth as in 12 (client_ps.booth_room), plus the oily handprint on the velvet.
NOTE: the $49,999 tag is drawn here for the first time. Episode 12's film has no tag in its code or docs (its FOUND
locks on the phone on the throne's arm); the price came in with STORYLINE v3.4 (23 Nov).
  room(k, blind=..., u=..., tape=..., spun=..., phone=..., silhouette=...)   the whole front desk, world 960 x 960
v2 (23 Nov, Tomas: "do it as you propose, minimal words"): the robot's card. In 2.1b the robot clips a white inventory
card on the throne's BACK: OWNER: INVESTOR (technically true: the money was Father's). In 2.2 Don spins the throne to
hide the price tag, and turns the card to the room. spun=True now draws the throne from behind, the card on it.
v3 (23 Nov, set audit, Tomas "darom v3"): every state change bigger than the object: the tape 40 % wider with a dark
edge; torn: 3 crooked slats left on the broken rail and a short dangling cord; rehung: one bent slat (Pam's repair);
the price tag 1.5x, heavier numerals; the cords shorter, Don's pull white, the robot's grey; Pam's phone exactly as
episode 13's invitation (cream screen, purple INVITATION, black DAD, of_scenes 3.6); the handprint 1.5x.
  python3 ps_set.py [out_dir]  ->  ps_set_v3.png (sheet), ps_set_phone_v3.png (the pieces at 270 px)"""
import os
import sys
import math
import cairo
import kit
import set_ob as st
import fs_set4 as s4
import dh_props as dp
import pm_ps
import client_ps as cps
from kit import INK, rect, cut, ellipse

F = s4.F
LINE_X = 560
GX0, GY0, GW, GH = st.DOOR                                  # the glass: x 22-172, y 392-800
SLAT, SLAT_D, RAIL = (0.94, 0.94, 0.91), (0.60, 0.60, 0.56), (0.80, 0.80, 0.77)
CORD, PULL, PULL_R = (0.30, 0.30, 0.30), (0.97, 0.96, 0.92), (0.55, 0.57, 0.60)
TAPE, TAPE_D = (0.95, 0.78, 0.15), (0.72, 0.56, 0.08)
CORD_L, CORD_R = GX0 + 10, GX0 + GW - 8                     # Don's cord, the robot's cord
THRONE = dp.CHAIR
PHONE_AT = (640, 640)


def _shut_stage(k):
    """fs_set4.draw_set with the glass door shut (it draws it 85 % open); restored after."""
    old = st.stage
    st.stage = lambda k_, open_=0.0, **kw: old(k_, 0.0, **kw)
    return old


def room(k, blind="up", u=0.0, tape=False, spun=False, phone="dark", silhouette=False, dim=True, mark=True, cords=True):
    """The whole front desk, empty (the cast goes on top). blind: up / down (u: how far, 0..1) / torn / rehung."""
    c = k.c
    old = _shut_stage(k)
    old_scr, old_conf = s4.fs.screen, s4.s3.confetti
    if NO_SCREEN[0]:
        s4.fs.screen = lambda *a, **kw: None
    if NO_DOOR_CONFETTI[0]:
        s4.s3.confetti = lambda k_, x, *a, **kw: None if x < 100 else old_conf(k_, x, *a, **kw)
    try:
        s4.draw_set(k, {})
    finally:
        st.stage = old
        s4.fs.screen, s4.s3.confetti = old_scr, old_conf
    if PLATE_BIG[0]:
        plate_big(k)
    if silhouette:
        behind_glass(k, lit=(silhouette == "phone"))
    throne(k, spun)
    if tape:
        tape_line(k, mark)
    if phone:
        pam_phone(k, *PHONE_AT, 1.0, lit=(phone == "lit"))
    blinds(k, blind, u, cords=cords)
    if dim and blind == "down" and u > 0:                    # the blinds shut out the street: the room goes dim
        c.set_source_rgba(0.05, 0.05, 0.10, 0.22 * u); c.rectangle(0, 0, 960, 960); c.fill()


def plate_big(k):
    """the status plate on DON's office door (fs_set4), at a size that reads at 270 px: DON · CEO."""
    x, y, w, h = s4.OFFICE
    c = k.c
    rect(k, x - 22, y - 62, w + 44, 52, (0.85, 0.70, 0.30), 807, lw=2)       # over the small gilt plate (y - 46 .. - 12)
    c.set_source_rgb(0.25, 0.18, 0.05); c.select_font_face("Inter", 0, 1); c.set_font_size(18)
    e = c.text_extents("DON · CEO"); c.move_to(x + w / 2 - e.x_advance / 2, y - 29); c.show_text("DON · CEO")


def behind_glass(k, x=100, lit=False):
    """Bodyguard 2 behind the glass (3.2-5.3): a big dark shape. lit (3.6, board v2): his phone up at his face, its glow
    lighting it: he is looking at something."""
    c = k.c
    c.save(); c.rectangle(GX0, GY0, GW, GH); c.clip()
    c.set_source_rgba(0.08, 0.08, 0.10, 0.72)
    c.new_path(); c.arc(x, 520, 30, 0, 2 * math.pi); c.fill()
    c.move_to(x - 60, 800); c.line_to(x - 52, 590); c.curve_to(x - 40, 560, x + 40, 560, x + 52, 590)
    c.line_to(x + 60, 800); c.close_path(); c.fill()
    if lit:
        g = cairo.RadialGradient(x + 14, 540, 2, x + 14, 540, 60)
        g.add_color_stop_rgba(0, 0.70, 0.95, 1.0, 0.85); g.add_color_stop_rgba(1, 0.70, 0.95, 1.0, 0.0)
        c.set_source(g); c.arc(x + 14, 540, 60, 0, 2 * math.pi); c.fill()
        c.set_source_rgba(0.08, 0.08, 0.10, 0.9); c.set_line_width(16); c.set_line_cap(1)      # his arm up to it
        c.move_to(x + 40, 640); c.line_to(x + 30, 570); c.stroke()
        c.set_source_rgb(0.80, 0.97, 1.0); c.rectangle(x + 6, 528, 20, 34); c.fill()
    if GUARD_CUES[0]:                                         # the guard's sunglasses (black, a glint) and earpiece coil
        for sx in (-1, 1):
            c.new_path(); c.move_to(x + sx * 3, 506); c.line_to(x + sx * 25, 505); c.line_to(x + sx * 23, 522)
            c.line_to(x + sx * 12, 525); c.line_to(x + sx * 4, 521); c.close_path()
            c.set_source_rgb(0.02, 0.02, 0.03); c.fill()
            c.set_source_rgba(1, 1, 1, 0.8); c.set_line_width(2.4); c.set_line_cap(1)
            c.move_to(x + sx * 9, 518); c.line_to(x + sx * 15, 510); c.stroke()
        c.set_source_rgb(0.02, 0.02, 0.03); c.set_line_width(3)
        c.move_to(x - 3, 507); c.line_to(x + 3, 507); c.stroke()
        c.set_source_rgb(0.92, 0.92, 0.90); c.set_line_width(2.6); c.new_path(); c.move_to(x + 29, 526)
        for i in range(6):
            yy = 532 + i * 7
            c.curve_to(x + 37, yy - 3, x + 37, yy + 3, x + 30, yy + 2)
        c.stroke(); c.set_line_cap(0)
    c.restore()


def blinds(k, state="up", u=1.0, seed=4900, cords=True):
    c = k.c
    top = GY0 - 10
    if state == "torn":                                       # the rail hangs from its left bracket; no slats
        c.save(); c.translate(GX0 - 6, top); c.rotate(0.55)
        for i, (dx, dy, a) in enumerate(((30, 14, 0.10), (62, 26, -0.18), (96, 16, 0.30))):   # 3 crooked slats left on it
            c.save(); c.translate(dx, dy); c.rotate(a - 0.55)
            rect(k, -26, -3, 52, 7, SLAT, seed + 20 + i, shadow=False, lw=1.4)
            c.restore()
        rect(k, 0, 0, GW + 12, 11, RAIL, seed, shadow=False, lw=2)
        c.restore()
        ellipse(k, GX0 + GW + 2, top + 4, 4, 4, (0.45, 0.45, 0.45), seed + 1, shadow=False, lw=1.4)   # the bare bracket
        _cord(c, CORD_L, top + 14, top + 150, swing=10, pull=PULL)
        return
    bent = state == "rehung"
    if state in ("up", "rehung"):
        u = 0.0
    bot = top + 14 + u * (GH - 4)
    n = 6 + int(u * 26)                                        # up: a tight stack; down: the slats spread
    stack = 34 if u == 0 else 0
    c.save(); c.rectangle(GX0 - 4, top, GW + 8, GH + 20); c.clip()
    if u > 0:
        c.set_source_rgba(*SLAT, 0.96); c.rectangle(GX0 - 2, top + 10, GW + 4, bot - top - 10); c.fill()
        c.set_source_rgb(*SLAT_D); c.set_line_width(1.2)
        step = (bot - top - 14) / max(n, 1)
        for i in range(n):
            yy = top + 14 + i * step
            c.move_to(GX0 - 2, yy); c.curve_to(GX0 + GW / 3, yy + 3, GX0 + 2 * GW / 3, yy + 3, GX0 + GW + 2, yy); c.stroke()
        c.set_source_rgb(*INK); c.set_line_width(1.8); c.rectangle(GX0 - 2, top + 10, GW + 4, bot - top - 10); c.stroke()
    else:                                                      # pulled up: the slats stacked under the rail
        for i in range(n):
            yy = top + 12 + i * (stack / n)
            rect(k, GX0 - 2, yy, GW + 4, stack / n + 1, SLAT if i % 2 else (0.88, 0.88, 0.85), seed + 10 + i, shadow=False, lw=1.2)
        bot = top + 12 + stack
    rect(k, GX0 - 4, bot - 4, GW + 8, 8, RAIL, seed + 2, shadow=False, lw=1.6)                 # the bottom bar
    c.restore()
    if bent:                                                                                   # Pam's repair: one slat bent down
        c.save(); c.translate(GX0 + GW * 0.62, bot + 2); c.rotate(0.55)
        rect(k, -4, -3, 58, 7, SLAT, seed + 30, shadow=False, lw=1.5)
        c.restore()
    rect(k, GX0 - 8, top, GW + 16, 12, RAIL, seed + 3, shadow=False, lw=2)                     # the rail
    if not cords:                                             # the motion tests draw the cords to the hands themselves
        return
    cl = max(bot + 30, top + 190)
    _cord(c, CORD_L, top + 12, cl, pull=PULL)                                                  # Don's cord, a white pull
    _cord(c, CORD_R, top + 12, cl, pull=PULL_R)                                                # the robot's, grey


def _cord(c, x, y0, y1, swing=0, pull=None):
    c.set_source_rgb(*CORD); c.set_line_width(3.0); c.new_path(); c.move_to(x, y0)
    c.curve_to(x + swing, (y0 + y1) / 2, x - swing, (y0 + y1) / 2, x + swing * 0.5, y1); c.stroke()
    c.save(); c.translate(x + swing * 0.5, y1 + 8); c.scale(5, 8); c.new_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
    c.set_source_rgb(*(pull or PULL)); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1.4); c.stroke()


NO_SCREEN = [False]                                         # opt-in (ps_scenes, board v2): the UPTIMEZ FIND screen over the
                                                            # door taken off: 3 of 3 cold viewers read "blueprint" typed into it
                                                            # as what brought the blind down
NO_DOOR_CONFETTI = [False]
GUARD_CUES = [False]                                        # opt-in (ep 14 v4, cold test 3 of 3 "who is behind the glass?"):
#                                                             the guard's canon sunglasses glint and earpiece coil (dh_cast.guard)
PLATE_BIG = [False]                                         # opt-in (ep 14 v4, 5.4: "whose side is his door on?" 2 of 3 can't
#                                                             tell): the door's DON · CEO plate drawn big enough to read                                  # opt-in (ep 14 scenes, 24 Nov): episode 10's confetti by the door
                                                            # taken off the floor: two cold viewers asked what the blue squiggles were
MARK_SMALL = [False]                                        # opt-in (ps_scenes v2): DON smaller and close beside the tape,
                                                            # so a close shot holds it whole or not at all (lesson 295)


def tape_line(k, mark=True):
    """The tape on the floor: back wall to the camera, splaying with depth; DON and an arrow in marker on his side."""
    c = k.c
    x0, x1 = LINE_X, LINE_X + 34
    c.new_path(); c.move_to(x0 - 8.5, F); c.line_to(x0 + 8.5, F); c.line_to(x1 + 20, 960); c.line_to(x1 - 20, 960); c.close_path()
    c.set_source_rgb(*TAPE); c.fill_preserve(); c.set_source_rgb(0.30, 0.22, 0.02); c.set_line_width(2.4); c.stroke()
    c.set_source_rgba(1, 1, 1, 0.35); c.set_line_width(1.5)                          # its sheen
    c.move_to(x0 - 1, F + 4); c.line_to(x1 - 6, 958); c.stroke()
    if not mark:                                                                       # 2.1: the tape just laid, no DON yet
        return
    if MARK_SMALL[0]:
        c.save(); c.translate(x0 + 100 * 28 / 160 - 40, F + 100); c.rotate(-0.04); c.scale(0.50, 0.50 * 0.55)
    else:
        c.save(); c.translate(x0 - 46, F + 110); c.rotate(-0.04); c.scale(1.0, 0.55)   # in marker, on the floor, his side
    c.select_font_face("Permanent Marker", 0, 1); c.set_font_size(52); c.set_source_rgb(0.08, 0.08, 0.10)
    e = c.text_extents("DON"); c.move_to(-e.x_advance, 0); c.show_text("DON")
    c.set_line_width(7); c.set_line_cap(1)                                             # the arrow: into his side
    c.move_to(-e.x_advance - 14, -18); c.line_to(-e.x_advance - 90, -18); c.stroke()
    c.move_to(-e.x_advance - 90, -18); c.line_to(-e.x_advance - 68, -36); c.stroke()
    c.move_to(-e.x_advance - 90, -18); c.line_to(-e.x_advance - 68, 0); c.stroke()
    c.set_line_cap(0); c.restore()


def throne(k, spun=False, card=False):
    """spun: seen from behind (2.2 on), the price tag's blank back, the robot's card on the back (card: from 2.1b)."""
    x, feet, s = THRONE
    o = dp.ceo_chair(k, x, feet, s)
    if spun:
        throne_back(k, x, feet, s)
    price_tag(k, x + 56 * s, feet - 432 * s, s * 2.4, back=spun)
    return o


def throne_back(k, x, feet, s, card=True):
    """The throne from behind: the gold back's rear, plain leather, no buttons; the robot's card clipped on it."""
    c = k.c
    c.save(); c.translate(x, feet); c.scale(s, s)
    back = [(-76, -104), (-92, -230), (-84, -330), (-40, -368), (0, -374), (40, -368), (84, -330), (92, -230), (76, -104)]
    cut(k, back, dp.GOLD, lw=2.8)
    cut(k, [(px * 0.87, -104 + (py + 104) * 0.955) for px, py in back], (0.20, 0.16, 0.15), shadow=False, lw=2)
    c.set_source_rgb(0.28, 0.23, 0.21); c.set_line_width(2)                   # its seams
    c.move_to(0, -350); c.line_to(0, -112); c.stroke()
    c.restore()
    if card:
        robot_card(k, x, feet - 250 * s, s * 1.5)


def robot_card(k, x, y, s=1.0, ang=-0.04):
    """The robot's inventory card, minimal words: OWNER: INVESTOR, a cyan barcode strip (its own colour), a clip."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    rect(k, -40, -26, 80, 52, (0.99, 0.99, 0.97), 4970, shadow=False, lw=1.8)
    c.set_source_rgb(0.45, 0.92, 1.0)
    for i, w in enumerate((2, 1, 3, 1, 2, 1, 1, 3, 2, 1, 2)):                 # the barcode: it was scanned in
        c.rectangle(-34 + i * 6.2, -21, w * 1.3, 9); c.fill()
    c.select_font_face("Inter", 0, 1); c.set_source_rgb(0.08, 0.10, 0.14)
    c.set_font_size(9); e = c.text_extents("OWNER:"); c.move_to(-e.x_advance / 2, 0); c.show_text("OWNER:")
    c.set_font_size(15); e = c.text_extents("INVESTOR"); c.move_to(-e.x_advance / 2, 18); c.show_text("INVESTOR")
    rect(k, -8, -32, 16, 10, (0.55, 0.58, 0.62), 4971, shadow=False, lw=1.4)    # the clip
    c.restore()


def price_tag(k, x, y, s=1.0, back=False, swing=0.18):
    """A white card tag on a string from the crown's right point: $49,999 in red; back = its blank side."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(swing); c.scale(s, s)
    c.set_source_rgb(*INK); c.set_line_width(1.4); c.move_to(0, 0); c.line_to(6, 26); c.stroke()
    c.translate(6, 26); c.rotate(-0.25)
    pts = [(-4, 0), (60, 0), (68, 10), (60, 20), (-4, 20)]
    cut(k, pts, (0.99, 0.98, 0.95), shadow=False, lw=1.6)
    ellipse(k, 60, 10, 2.4, 2.4, INK, 4950, shadow=False, lw=0.8)
    if not back:
        c.select_font_face("Inter Black", 0, 1); c.set_font_size(13); c.set_source_rgb(0.80, 0.06, 0.08)
        c.move_to(-1, 15); c.show_text("$49,999")
    c.restore()


def pam_phone(k, x, y, s=1.0, lit=False):
    """Face up on the counter: dark, or lit with INVITATION · DAD (unreadable at the set's scale: see phone_close)."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    cut(k, [(-13, -5), (13, -5), (16, 5), (-16, 5)], (0.12, 0.12, 0.14), shadow=False, lw=1.4)
    if lit:
        c.set_source_rgba(0.60, 0.90, 1.0, 0.35); c.save(); c.scale(1, 0.4); c.new_path(); c.arc(0, 0, 34, 0, 2 * math.pi); c.restore(); c.fill()
        cut(k, [(-10, -3.5), (10, -3.5), (12, 3.5), (-12, 3.5)], (0.97, 0.94, 0.86), shadow=False, lw=0.8)
    c.restore()


def phone_close(k, x, y, s=1.0, lit=True, buzz=True):
    """5.7's insert-in-shot: the phone face up, seen from above, INVITATION · DAD readable at 270 px."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    rect(k, -60, -110, 120, 220, (0.10, 0.10, 0.12), 4960, shadow=False, lw=2.2)
    rect(k, -52, -98, 104, 196, (0.97, 0.94, 0.86) if lit else (0.06, 0.06, 0.08), 4961, shadow=False, lw=1.2)
    if lit:                                                  # episode 13's invitation (of_scenes 3.6): the same card
        c.select_font_face("Lilita One"); c.set_source_rgb(0.55, 0.16, 0.46)
        c.set_font_size(18); e = c.text_extents("INVITATION"); c.move_to(-e.x_advance / 2, -16); c.show_text("INVITATION")
        c.set_source_rgb(*INK); c.set_font_size(36); e = c.text_extents("DAD"); c.move_to(-e.x_advance / 2, 26); c.show_text("DAD")
        c.set_source_rgb(0.06, 0.20, 0.40); c.set_line_width(2.4)
        for i in (1, 2, 3) if buzz else ():                                            # it buzzes
            c.new_path(); c.arc(0, 0, 60 + i * 12, -0.5, 0.5); c.stroke(); c.new_path(); c.arc(0, 0, 60 + i * 12, math.pi - 0.5, math.pi + 0.5); c.stroke()
    c.restore()


def booth(k, w, h, seat_y, table_y, handprint=True):
    """Father's booth as in 12 (client_ps's front-on version), with the oily handprint on the velvet (4.3)."""
    cps.booth_room(k, w, h, seat_y, table_y)
    if handprint:
        cps.handprint(k, w * 0.30, seat_y - 120, 2.1, 0.25)
    cps.table(k, w, table_y)


def _label(c, s, x, y, size=16, bold=1, col=INK):
    c.select_font_face("Inter", 0, bold); c.set_font_size(size); c.set_source_rgb(*col)
    e = c.text_extents(s); c.move_to(x - e.x_advance / 2, y); c.show_text(s)


def sheet(out):
    W, H = 2400, 1460
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    c = cairo.Context(surf); k = kit.Ctx(c, 0)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    c.select_font_face("Inter", 0, 1); c.set_font_size(30); c.set_source_rgb(*INK); c.move_to(30, 46)
    c.show_text("PICK A SIDE · stage 3, the set · v3 · the front desk v4, door shut, with this episode's pieces")
    c.select_font_face("Inter", 0, 0); c.set_font_size(17); c.move_to(30, 76)
    c.show_text("Tomas, /grill-me: white slats with a cord each side · yellow tape, DON and an arrow in marker · the booth as in 12 + the handprint · "
                "the $49,999 tag drawn here for the first time (not in 12's film)")
    S = 0.56
    for i, (ttl, kw) in enumerate((("FRAME 0 · blinds up, no tape", dict(blind="up")),
                                   ("1.1 · Don pulls: down, the room dims", dict(blind="down", u=0.7)),
                                   ("2.2 on · the blind torn, the tape, spun: OWNER: INVESTOR", dict(blind="torn", tape=True, spun=True)),
                                   ("5.3 on · rehung, Pam's phone lit, the guard behind", dict(blind="rehung", tape=True, spun=True,
                                                                                            phone="lit", silhouette=True)))):
        x0, y0 = 30 + i * 592, 110
        c.save(); c.translate(x0, y0); c.scale(S, S); c.rectangle(0, 0, 960, 960); c.clip()
        room(k, **kw)
        c.restore()
        c.set_source_rgb(*INK); c.set_line_width(1.5); c.rectangle(x0, y0, 960 * S, 960 * S); c.stroke()
        _label(c, ttl, x0 + 480 * S, y0 + 960 * S + 26, 16)
    y0 = 720
    BS = 1.3                                                                    # the blinds, five states, the door close
    for i, (st_, u, ttl) in enumerate((("up", 0, "up"), ("down", 0.35, "a third"), ("down", 1.0, "down"),
                                       ("torn", 0, "torn (on Don)"), ("rehung", 0, "rehung (5.3 on)"))):
        x0 = 30 + i * 260
        c.save(); c.translate(x0, y0); c.scale(BS, BS); c.translate(-GX0 + 10, -GY0 + 24)
        c.rectangle(GX0 - 20, GY0 - 24, GW + 40, 440); c.clip()
        c.set_source_rgb(*kit.WALL); c.paint()
        st.door(k, 0.0)
        blinds(k, st_, u)
        c.restore()
        _label(c, ttl, x0 + 100, y0 + 600, 15)
    c.save(); c.translate(1340, 700); c.scale(0.7, 0.7); c.translate(-380, -760); c.rectangle(380, 760, 420, 200); c.clip()   # the tape, close
    c.set_source_rgb(*kit.FLOOR); c.paint(); tape_line(k); c.restore()
    _label(c, "the tape, from the camera side", 1340 + 147, 870, 15)
    c.save(); c.translate(1340, 1000); c.scale(0.6, 0.6); dp.ceo_chair(k, 140, 360, 0.60); price_tag(k, 140 + 56 * 0.6, 360 - 432 * 0.6, 1.6)
    dp.ceo_chair(k, 420, 360, 0.60); throne_back(k, 420, 360, 0.60); price_tag(k, 420 + 56 * 0.6, 360 - 432 * 0.6, 1.6, back=True); c.restore()
    _label(c, "the tag · spun: the robot's card", 1340 + 168, 1250, 15)
    c.save(); c.translate(1780, 1140); phone_close(k, 0, 0, 0.8, lit=False); phone_close(k, 150, 0, 0.8, lit=True); c.restore()
    _label(c, "Pam's phone: dark · INVITATION · DAD", 1855, 1250, 15)
    c.save(); c.translate(1960, 700); c.scale(0.42, 0.42)                       # the booth
    c.rectangle(0, 0, 960, 700); c.clip(); booth(k, 960, 700, 420, 560); c.restore()
    _label(c, "the booth as in 12 + the handprint", 2160, 1016, 15)
    c.save(); c.translate(2230, 1220); pm_ps.stool(k, 0, 0, 0.9); c.restore()
    _label(c, "the step stool", 2230, 1250, 15)
    surf.write_to_png(out); print("wrote", out)


def phone_check(out):
    """Three 540x960 frames of the pieces that must read at 270 px: the cords (frame 0), the tape with DON, the phone."""
    frames = []
    for name in ("cords", "tape", "card", "phone"):
        f = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(f); k = kit.Ctx(c, 0)
        c.set_source_rgb(*kit.WALL); c.paint()
        if name == "cords":                                  # S2, knees up: the door, the blind, the two cords
            c.save(); c.scale(2.6, 2.6); c.translate(-6, -340); room(k, blind="up"); c.restore()
        elif name == "card":                                  # 2.2: the spun throne, the robot's card to the room
            c.save(); c.scale(2.4, 2.4); c.translate(-340, -440); room(k, blind="torn", tape=True, spun=True); c.restore()
        elif name == "tape":                                  # S4 low: the tape across the floor
            c.save(); c.scale(1.6, 1.6); c.translate(-250, -360); room(k, blind="torn", tape=True, spun=True); c.restore()
        else:
            c.set_source_rgb(0.55, 0.48, 0.40); c.paint(); phone_close(k, 270, 480, 1.6)
        frames.append((name, f))
    W = 4 * 270 + 5 * 20
    s_ = cairo.ImageSurface(cairo.FORMAT_RGB24, W, 540); c = cairo.Context(s_); c.set_source_rgb(0.15, 0.15, 0.16); c.paint()
    for i, (name, f) in enumerate(frames):
        c.save(); c.translate(20 + i * 290, 20); c.scale(0.5, 0.5); c.set_source_surface(f, 0, 0); c.paint(); c.restore()
        c.select_font_face("Inter", 0, 1); c.set_font_size(15); c.set_source_rgb(1, 1, 1)
        c.move_to(20 + i * 290, 522); c.show_text(name.upper() + " · at 270 px")
    s_.write_to_png(out); print("wrote", out)


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else "../pick-a-side"
    os.makedirs(d, exist_ok=True)
    sheet(os.path.join(d, "ps_set_v3.png"))
    phone_check(os.path.join(d, "ps_set_phone_v3.png"))
