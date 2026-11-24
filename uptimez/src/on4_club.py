"""OFFICE NOIR 4: Dad's club, v6 (23 Nov). v1-v5 pinned (on4_club_v1.py .. on4_club_v5.py). v6: Dad's limousine
(on4_car.py, from Tomas's car photographs) at the kerb in front(limo=True); everything else as v5. v5: the front rebuilt on Tomas's
photograph of a lit palace entrance (ref/on4_club_ref_v3.jpg; "Proceed"): the arched passage lit from inside (the way in;
it leads to the hall), framed in bare strings of lights (the dream street's lit arch again), the marquee in the band over
the arch where the building's name was, the neon heart in the round medallion above (where the coat of arms was), the
pediment windows dark. Left out: the real name and signs, the coat of arms, the fir greenery (Christmas, not
Valentine's), the lift, the flags. The wooden gate of v1-v4 is gone.
v4 (23 Nov). v4: the 5.2 insert did not read
(Tomas: "I don't understand the shot with the Z"; the Z is no symbol in the series). His pick: the plan and the logo. The
Client's own MY GARAGES plan (cs_props.plan, "whole": ten numbered garages, the taped strips) flat on the booth table;
Dad's ringed hand, his velvet cuff, laying an UptimeZ card on it (the series' real mark and name, brand.py). Both props
the series already has: his garages, going under UptimeZ.
v3 (23 Nov). v3, from Tomas's photograph of a
game table (ref/on4_club_ref_v2.jpg): the round green felt (a grey blot after the grade) becomes a square black table
with a chequerboard top and two black dice cups (his first outline: "cards, dice"); the dealers sit in chairs whose light
bentwood arms show at their sides (the rig cannot sit; the arms say it); an empty chair, its black back to us, in front
(a foreground layer, lesson 18). The black leather backs are turned side-on, never behind a black figure (lesson 47).
v2 (23 Nov). v2: the inside rebuilt on Tomas's photograph
of a long dim hall (ref/on4_club_ref_v1.jpg; his pick: "the club's inside, rebuilt on it"): one-point perspective, the
beamed ceiling, the tall wooden panels along the left wall (where the lockers are) with the card table against them, the
alcoves in the right wall with the booth in the first, and at the end the lit double glass doors with the stage and its
spotlight in the doorway. Same beats (5.1, 6.x), more depth. FRONT and MAP as v1.
v1 (23 Nov). Stage 3 (look and set). Script v3, beats 04-06: the club is Dad's (a nightclub
owner in the canon; the booth of Daddy's Home, dh_props.booth: the velvet banquette, the neon tubes, the dark glass table).
Three drawings, all through the Office Noir 2 grade, the neon kept red (the dream's one red):
  FRONT  4.1-4.3   the club's door (the big wooden double gate of ref v2), lit cream walls, the marquee over the door: a
                   neon heart, PAM-CAT big, ONE EVENING . ONCE IN A LIFETIME small on a strip of bulbs, ONLY FOR YOU big
                   (Tomas's pick: two big lines; the ending depends on ONLY FOR YOU reading at 270 px). The sedan parked
                   at the kerb, empty: how she found the place.
  INSIDE 5.1, 6.x  one wide, laid out for the phone (faces and story props above y 720 and left of the button rail): the
                   stage up left, its curtain, the spotlight on a stand with a handle (the glove turns it in 6.4); the card
                   table in the middle, two pale-gloved shadows dealing (bare-headed, on4_street.thug); the booth right,
                   the Client (client_ob, himself, as Pam knows him from the office) and Dad, whose face is hidden by the
                   low lamp shade over the booth table (as Daddy's Home hides it under the frame); the map on the table.
  MAP    5.2       the insert: ten small boxes, an arrow, a big Z; Dad's ringed hand flat on the Z (his velvet cuff).
  python3 on4_club.py  ->  ../office-noir-4/on4_club_sheet_v1.png, on4_club_phone_v1.png"""
import math
import random
import cairo
import kit
import engine_on as eng
import on_set as ons
import on4_street as st
import dh_cast as dc
import client_ob as co
from kit import Ctx, INK, cut

NEON = st.NEON
GOLD = st.GOLD
VELVET, VELVET_D = dc.VELVET, dc.VELVET_D
FELT = (0.18, 0.36, 0.26)
HALL_LAMP = ["v6"]               # v7 (23 Nov): Dad hidden by the dark over a small lamp; "v6" the big shade
PLAN_CARD = ["v6"]               # v7: one title, every number seen, the card laid down and the hand off it; "v6" as before
MOTTO = [False]                  # v9 (24 Nov): Daddy's Home's neon motto, THE HOUSE ALWAYS COLLECTS, on the wall over the booth
ARCH_WARM = [False]              # v9: the arch's bulbs give warm light (laid after the grade, so it keeps its colour)
PASSAGE_DARK = [False]           # v9: the passage's walls charcoal, its far end lit (the POV, 4.4)
LIMO = [(150, 0.74)]              # v8 (proportion audit): (x, scale) of the limousine at the kerb; on4_scenes sets (30, 1.15)
CLIENT_DY = [0]                  # v8: the Client lower in his booth (he sat as tall as Pam stands)
FRONT_LIGHT = ["v6"]             # v7: the facade's edges dark, the marquee's light on the car's roof, the car nearer the arch
LOG = {}


def neon_text(k, txt, x, y, size, font="Lilita One"):
    """Neon letters: a soft glow, then the tube in the key red (kept red by the accent pass), a white core."""
    c = k.c
    c.select_font_face(font, 0, 0); c.set_font_size(size)
    e = c.text_extents(txt); x0 = x - e.x_advance / 2
    for wd, al in ((14, 0.10), (8, 0.22)):
        c.new_path(); c.move_to(x0, y); c.text_path(txt); c.set_source_rgba(1, 0.35, 0.42, al); c.set_line_width(wd); c.stroke()
    c.new_path(); c.move_to(x0, y); c.text_path(txt); c.set_source_rgb(*NEON); c.fill()
    c.new_path(); c.move_to(x0, y); c.text_path(txt); c.set_source_rgba(1, 0.85, 0.88, 0.9); c.set_line_width(1.2); c.stroke()


def neon_heart(c, x, y, s):
    st.heart(c, x, y, s)


def bulb_strip(k, x0, x1, y, txt, size=17):
    c = k.c
    st.poly(k, [(x0, y - 18), (x1, y - 18), (x1, y + 10), (x0, y + 10)], (0.10, 0.10, 0.11), 1.6)
    for i in range(int((x1 - x0) / 14) + 1):
        st.bulb(c, x0 + 6 + i * 14, y - 24, 2.2)
        st.bulb(c, x0 + 6 + i * 14, y + 16, 2.2)
    c.select_font_face("Lilita One", 0, 0); c.set_font_size(size)
    e = c.text_extents(txt); c.move_to((x0 + x1) / 2 - e.x_advance / 2, y + 2); c.set_source_rgb(0.98, 0.94, 0.80); c.show_text(txt)


def sedan_side(k, x, base, s=1.0):
    """A dark sedan, side on, nose left: a long bonnet, a rounded cabin, two wheels, a red tail lamp."""
    c = k.c
    c.save(); c.translate(x, base); c.scale(s, s)
    st.poly(k, [(-150, -10), (-150, -44), (-96, -52), (-62, -92), (52, -92), (92, -54), (150, -46), (154, -10)], (0.08, 0.08, 0.09), 2.2)
    st.poly(k, [(-54, -84), (-6, -84), (-6, -56), (-82, -54)], (0.32, 0.33, 0.36), 1.4)
    st.poly(k, [(4, -84), (46, -84), (78, -56), (4, -56)], (0.32, 0.33, 0.36), 1.4)
    for wx in (-96, 98):
        c.set_source_rgb(*INK); c.new_path(); c.arc(wx, -10, 24, 0, 2 * math.pi); c.fill()
        c.set_source_rgb(0.55, 0.56, 0.58); c.new_path(); c.arc(wx, -10, 10, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(*NEON); c.rectangle(146, -40, 8, 10); c.fill()
    c.restore()


def front(k, limo=False):
    """4.1-4.3, v5 (v6: limo=True parks Dad's limousine, on4_car.side, on a wet kerb instead of the old sedan): a lit palace front; the arched passage lit from inside, framed in lights; the marquee over it."""
    c = k.c
    st.sky(k)
    FAC = (0.86, 0.85, 0.82)                                               # the facade, lit from below: pale grey
    st.poly(k, [(-10, 40), (550, 40), (550, 660), (-10, 660)], FAC, 2.2)
    for y in (40, 58, 236, 250):                                           # cornices
        st.poly(k, [(-10, y), (550, y), (550, y + 10), (-10, y + 10)], (0.94, 0.93, 0.90), 1.4)
    for (x0, x1) in ((24, 120), (420, 516)):                               # the pediment windows, dark
        st.poly(k, [(x0 - 10, 104), ((x0 + x1) / 2, 76), (x1 + 10, 104)], (0.95, 0.94, 0.91), 1.6)
        st.poly(k, [(x0 - 4, 108), (x1 + 4, 108), (x1 + 4, 116), (x0 - 4, 116)], (0.95, 0.94, 0.91), 1.4)
        st.poly(k, [(x0, 118), (x1, 118), (x1, 222), (x0, 222)], (0.06, 0.06, 0.08), 2.0)
        c.set_source_rgb(0.20, 0.20, 0.22); c.set_line_width(2); c.move_to((x0 + x1) / 2, 118); c.line_to((x0 + x1) / 2, 222); c.stroke()
        c.move_to(x0, 160); c.line_to(x1, 160); c.stroke()
    # the round medallion with the neon heart in it (where the coat of arms was)
    c.new_path(); c.arc(270, 150, 62, 0, 2 * math.pi); c.set_source_rgb(0.95, 0.94, 0.91); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(2.2); c.stroke()
    c.new_path(); c.arc(270, 150, 50, 0, 2 * math.pi); c.set_source_rgb(0.10, 0.08, 0.09); c.fill()
    neon_heart(c, 270, 154, 26)
    # the marquee in the band over the arch: the heart is above it now; PAM-CAT, the bulb strip, ONLY FOR YOU
    st.poly(k, [(40, 262), (500, 262), (500, 430), (40, 430)], (0.06, 0.06, 0.07), 2.6)
    for i in range(32):
        u = i / 31
        st.bulb(c, 48 + u * 444, 270, 2.4); st.bulb(c, 48 + u * 444, 422, 2.4)
    neon_text(k, "PAM-CAT", 270, 336, 70)
    bulb_strip(k, 70, 470, 368, "ONE EVENING · ONCE IN A LIFETIME", 17)
    neon_text(k, "ONLY FOR YOU", 270, 416, 42)
    import on4_posters as po; po.club(k)                                   # (24 Nov) her bill by the door, opt-in
    # the arched passage, lit from inside: a vault with its small lamps, the walls, the floor running in to a far opening
    ax0, ax1, at, ab = 178, 362, 478, 660
    cx = (ax0 + ax1) / 2; rr = (ax1 - ax0) / 2
    st.poly(k, [(ax0 - 60, at - 6), (ax1 + 60, at - 6), (ax1 + 60, ab), (ax0 - 60, ab)], (0.90, 0.88, 0.84), 1.8)   # the piers
    c.save(); c.new_path(); c.move_to(ax0, ab); c.line_to(ax0, at + rr); c.arc(cx, at + rr, rr, math.pi, 0); c.line_to(ax1, ab); c.close_path(); c.clip()
    c.set_source_rgb(0.98, 0.96, 0.90); c.paint()                                                 # the bright inside
    fx0, fx1, ft, fb = cx - 34, cx + 34, at + 104, ab - 52                                        # the far opening
    if PASSAGE_DARK[0]:                                                                           # v9: charcoal walls, the light only at its end
        c.set_source_rgb(0.20, 0.20, 0.21); c.paint()
        st.poly(k, [(ax0, at + rr), (fx0, ft), (fx0, fb), (ax0, ab)], (0.25, 0.25, 0.26), 1.2)
        st.poly(k, [(ax1, at + rr), (fx1, ft), (fx1, fb), (ax1, ab)], (0.21, 0.21, 0.22), 1.2)
        st.poly(k, [(ax0, ab), (fx0, fb), (fx1, fb), (ax1, ab)], (0.17, 0.17, 0.18), 1.2)
        st.poly(k, [(fx0, ft), (fx1, ft), (fx1, fb), (fx0, fb)], (1.0, 0.98, 0.92), 1.0)
        g = cairo.LinearGradient(0, fb, 0, ab)                                                    # its light on the floor, a wet shine
        g.add_color_stop_rgba(0, 1, 0.97, 0.88, 0.55); g.add_color_stop_rgba(1, 1, 0.97, 0.88, 0.0)
        c.set_source(g); c.new_path(); c.move_to(fx0 + 6, fb); c.line_to(fx1 - 6, fb); c.line_to(cx + 30, ab); c.line_to(cx - 30, ab); c.close_path(); c.fill()
        for side_ in (-1, 1):
            g = cairo.RadialGradient(cx + side_ * 34, (ft + fb) / 2, 2, cx + side_ * 34, (ft + fb) / 2, 90)
            g.add_color_stop_rgba(0, 1, 0.97, 0.88, 0.35); g.add_color_stop_rgba(1, 1, 0.97, 0.88, 0)
            c.set_source(g); c.paint()
    else:
        st.poly(k, [(ax0, at + rr), (fx0, ft), (fx0, fb), (ax0, ab)], (0.86, 0.84, 0.78), 1.2)     # its left wall
        st.poly(k, [(ax1, at + rr), (fx1, ft), (fx1, fb), (ax1, ab)], (0.80, 0.78, 0.72), 1.2)     # its right wall
        st.poly(k, [(ax0, ab), (fx0, fb), (fx1, fb), (ax1, ab)], (0.62, 0.58, 0.52), 1.2)          # its floor
    for i in range(4):                                                                            # the vault's lamps
        u = (i + 1) / 5.0; y = at + 20 + u * (ft - at - 20)
        c.set_source_rgb(1, 1, 0.92); c.new_path(); c.arc(cx, y, 4 - u * 2, 0, 2 * math.pi); c.fill()
    st.poly(k, [(fx0, ft), (fx1, ft), (fx1, fb), (fx0, fb)], (0.99, 0.98, 0.94), 1.0)              # the far end, glowing
    c.restore()
    c.new_path(); c.move_to(ax0, ab); c.line_to(ax0, at + rr); c.arc(cx, at + rr, rr, math.pi, 0); c.line_to(ax1, ab)
    c.set_source_rgb(*INK); c.set_line_width(2.6); c.stroke()
    # bare strings of lights framing the arch, on a dark band (the dark of the photograph's greenery, no fir: it is
    # Valentine's), so the bulbs read on the pale facade; three rows, down both piers
    c.new_path(); c.move_to(ax0 - 40, ab); c.line_to(ax0 - 40, at + rr); c.arc(cx, at + rr, rr + 40, math.pi, 0); c.line_to(ax1 + 40, ab)
    c.line_to(ax1 + 2, ab); c.line_to(ax1 + 2, at + rr); c.arc_negative(cx, at + rr, rr + 2, 0, math.pi); c.line_to(ax0 - 2, ab); c.close_path()
    c.set_source_rgb(0.16, 0.16, 0.17); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2); c.stroke()
    r = random.Random(17)
    for ring in (9, 21, 33):
        n = 30
        for i in range(n + 1):
            a = math.pi + math.pi * i / n
            st.bulb(c, cx + math.cos(a) * (rr + ring) + r.uniform(-2, 2), at + rr + math.sin(a) * (rr + ring) + r.uniform(-2, 2), 2.8)
        for j in range(9):
            for sx in (-1, 1):
                st.bulb(c, cx + sx * (rr + ring) + r.uniform(-2, 2), at + rr + 8 + j * 9 + r.uniform(-3, 3), 2.8)
    # the pavement, the kerb, the cobbles; the sedan parked at the kerb, empty: how she found the place
    st.poly(k, [(-10, 660), (550, 660), (550, 694), (-10, 694)], st.PAVE, 1.8)
    def road():
        c.new_path(); c.rectangle(-10, 694, 560, 270)
    road(); c.set_source_rgb(*st.ROAD); c.fill()
    st.setts(k, road, 694, 960, -10, 550, -10, 550, seed=55)
    if limo:                                                              # v6: Dad's limousine, nose left, its mirror in the wet stone
        import on4_car as car
        car.reflect(k, lambda: car.side(k, LIMO[0][0], 712, LIMO[0][1]), 712, 0.30, 60)
    else:
        sedan_side(k, 120, 716, 0.72)                                     # left, clear of the arch and above the dead zone


def light_front(c, limo=False):
    ons.key_light(c, 270, 560, 200, 0.22)                                 # the light out of the passage
    g = cairo.LinearGradient(0, 120, 0, 450)                                 # the marquee lights the wall under it
    g.add_color_stop_rgba(0, 1, 0.9, 0.9, 0.0); g.add_color_stop_rgba(1, 1, 0.9, 0.9, 0.0)
    ons.vignette(c, 0.65)
    if FRONT_LIGHT[0] != "v6":                 # v7: the facade is lit from the arch and the marquee, not all over:
        for x0, x1 in ((0, 170), (540, 370)):       # its edges go dark; the arch's light and the marquee's red fall
            g = cairo.LinearGradient(x0, 0, x1, 0)  # on the car's roof and flank
            g.add_color_stop_rgba(0, 0, 0, 0, 0.62); g.add_color_stop_rgba(1, 0, 0, 0, 0)
            c.set_source(g); c.rectangle(min(x0, x1), 0, abs(x1 - x0), 700); c.fill()
        g = cairo.LinearGradient(0, 0, 0, 260)
        g.add_color_stop_rgba(0, 0, 0, 0, 0.55); g.add_color_stop_rgba(1, 0, 0, 0, 0)
        c.set_source(g); c.rectangle(0, 0, 540, 260); c.fill()
        g = cairo.RadialGradient(270, 600, 10, 270, 600, 230)
        g.add_color_stop_rgba(0, 1, 0.97, 0.88, 0.30); g.add_color_stop_rgba(1, 1, 0.97, 0.88, 0)
        c.set_source(g); c.rectangle(0, 380, 540, 400); c.fill()
        lx_, ls_ = LIMO[0]                                                    # v10: on the car's roof where the car is, stronger
        a_ = 0.45 if ARCH_WARM[0] else 0.30
        c.save(); c.translate(lx_ + 10 * ls_, 712 - 96 * ls_); c.scale(130 * ls_, 20 * ls_)  # the marquee's red on the car's roof
        g = cairo.RadialGradient(0, 0, 0, 0, 0, 1)
        g.add_color_stop_rgba(0, 1, 0.15, 0.22, a_); g.add_color_stop_rgba(1, 1, 0.15, 0.22, 0)
        c.set_source(g); c.arc(0, 0, 1, 0, 2 * math.pi); c.fill(); c.restore()
        if ARCH_WARM[0]:                                                        # and a red sheen on the wet stones under the marquee
            c.save(); c.translate(270, 740); c.scale(200, 26)
            g = cairo.RadialGradient(0, 0, 0, 0, 0, 1)
            g.add_color_stop_rgba(0, 1, 0.15, 0.22, 0.14); g.add_color_stop_rgba(1, 1, 0.15, 0.22, 0)
            c.set_source(g); c.arc(0, 0, 1, 0, 2 * math.pi); c.fill(); c.restore()
    if ARCH_WARM[0]:                                                       # v9: the arch's bulbs as lights: a warm ring round it
        cx_, at_, rr_ = 270, 478, 92
        for r_, a_ in ((rr_ + 34, 0.40), (rr_ + 22, 0.50)):
            c.save(); c.new_path(); c.arc(cx_, at_ + rr_, r_, math.pi, 0); c.line_to(cx_ + r_, 660); c.line_to(cx_ - r_, 660); c.close_path()
            c.set_source_rgba(GOLD[0], GOLD[1], GOLD[2], 0); c.restore()
            g = cairo.RadialGradient(cx_, at_ + rr_, rr_ - 10, cx_, at_ + rr_, r_ + 30)
            g.add_color_stop_rgba(0, GOLD[0], GOLD[1] * 0.9, GOLD[2] * 0.6, 0); g.add_color_stop_rgba(0.4, GOLD[0], GOLD[1] * 0.9, GOLD[2] * 0.6, a_)
            g.add_color_stop_rgba(1, GOLD[0], GOLD[1], GOLD[2], 0)
            c.set_source(g); c.rectangle(cx_ - r_ - 40, at_ - 40, 2 * r_ + 80, 660 - at_ + 40); c.fill()
    if limo:
        import on4_car as car
        car.glow(c, "side", LIMO[0][0], 712, LIMO[0][1])


def inside(k):
    c = k.c
    c.set_source_rgb(0.08, 0.02, 0.04); c.paint()
    for yy, a in ((120, 0.9), (162, 0.55)):                                  # the neon tubes of Daddy's Home, along the wall
        for wd, al in ((22, 0.10), (12, 0.22), (5, a)):
            c.set_source_rgba(*(NEON if al == a else (1.0, 0.35, 0.42)), al if al != a else 1.0); c.set_line_width(wd); c.set_line_cap(1)
            c.move_to(20, yy); c.line_to(300, yy); c.curve_to(340, yy, 340, yy + 50, 380, yy + 50); c.line_to(520, yy + 50); c.stroke()
    # the stage, up left: its curtain in folds, the boards, the spot of light waiting on it
    st.poly(k, [(18, 196), (260, 196), (260, 430), (18, 430)], VELVET_D, 2.4)
    for i in range(8):
        x = 30 + i * 30
        c.set_source_rgb(*VELVET); c.rectangle(x, 200, 14, 226); c.fill()
    st.poly(k, [(10, 430), (272, 430), (282, 452), (0, 452)], (0.30, 0.22, 0.16), 2.0)
    c.save(); c.translate(138, 432); c.scale(70, 12)
    g = cairo.RadialGradient(0, 0, 0.1, 0, 0, 1); g.add_color_stop_rgba(0, 1, 1, 0.95, 0.85); g.add_color_stop_rgba(1, 1, 1, 0.95, 0)
    c.set_source(g); c.arc(0, 0, 1, 0, 2 * math.pi); c.fill(); c.restore()
    # the spotlight on its stand, right of the stage, its beam on the empty spot; the handle at its back
    sx, sy = 316, 330
    c.set_source_rgb(*INK); c.set_line_width(4); c.move_to(sx, sy + 20); c.line_to(sx, 470); c.stroke()
    c.move_to(sx - 24, 470); c.line_to(sx + 24, 470); c.stroke()
    c.save(); c.translate(sx, sy); c.rotate(math.radians(200))
    st.poly(k, [(-18, -16), (22, -22), (22, 22), (-18, 16)], (0.20, 0.20, 0.22), 2.0)
    c.set_source_rgb(*INK); c.set_line_width(3); c.move_to(-18, 0); c.line_to(-38, 0); c.stroke()      # the handle
    c.restore()
    g = cairo.LinearGradient(sx, sy, 138, 432)                                # the beam
    g.add_color_stop_rgba(0, 1, 1, 0.95, 0.35); g.add_color_stop_rgba(1, 1, 1, 0.95, 0.10)
    c.set_source(g); c.new_path(); c.move_to(sx - 20, sy - 6); c.line_to(sx - 16, sy + 20); c.line_to(200, 440); c.line_to(70, 430); c.close_path(); c.fill()
    # the booth, right: the velvet banquette; the Client and Dad behind its table; a lamp hanging low over it
    st.poly(k, [(262, 470), (470, 470), (470, 660), (262, 660)], VELVET_D, 2.4)
    for xx in range(282, 470, 46):
        c.set_source_rgb(*VELVET); c.rectangle(xx, 476, 30, 178); c.fill()
    co.client(k, 316, 720 + CLIENT_DY[0], 0.42, "open", "plain", look=(0.6, 0.8), roll=False, badge=False)
    o = dc.father(k, 416, 724 + CLIENT_DY[0], 0.68, (-20, 30, 20, -30), "hard", (-0.6, 0.6))              # at the Client's size (measured)
    hx, hy = o["head"]
    LOG["dad_head"] = (round(hx), round(hy))
    c.set_source_rgb(*INK); c.set_line_width(2); c.move_to(hx, 380); c.line_to(hx, hy - 32); c.stroke()  # the lamp hangs low: its
    st.poly(k, [(hx - 40, hy - 32), (hx + 40, hy - 32), (hx + 58, hy + 26), (hx - 58, hy + 26)], (0.16, 0.30, 0.20), 2.0)   # shade
    g = cairo.LinearGradient(0, hy + 26, 0, 660)                                            # hides Dad's face to the chin,
    g.add_color_stop_rgba(0, 1, 1, 0.9, 0.32); g.add_color_stop_rgba(1, 1, 1, 0.9, 0.0)     # as the frame does in Daddy's Home
    c.set_source(g); c.new_path(); c.move_to(hx - 58, hy + 26); c.line_to(hx + 58, hy + 26); c.line_to(hx + 90, 640); c.line_to(hx - 90, 640); c.close_path(); c.fill()
    st.poly(k, [(250, 636), (480, 636), (480, 660), (250, 660)], (0.12, 0.06, 0.08), 2.2)               # the table: dark glass
    st.poly(k, [(330, 622), (400, 622), (404, 638), (326, 638)], (0.95, 0.93, 0.86), 1.4)               # the map on it
    # the card table, middle left, under its own hanging lamp: a pool of light on the wall behind the two shadows dealing,
    # so their black heads read (lesson 47), and a rim on each; pale gloves
    c.save(); c.translate(144, 560); c.scale(150, 110)
    g = cairo.RadialGradient(0, 0, 0.1, 0, 0, 1); g.add_color_stop_rgba(0, 0.95, 0.85, 0.80, 0.55); g.add_color_stop_rgba(1, 0.95, 0.85, 0.80, 0)
    c.set_source(g); c.arc(0, 0, 1, 0, 2 * math.pi); c.fill(); c.restore()
    import on4_lying as ly
    import hands_ps as hp
    dealers = []
    for x in (96, 192):
        c.save(); c.rectangle(0, 0, 540, 636); c.clip()                     # the rim only above the table (not round the legs)
        ly.rim(k, x, 700, 0.36, seed=4600 + x, pose=(-40, 60, 40, -60))
        c.restore()
        dealers.append(st.thug(k, x, 700, 0.36, (-40, 60, 40, -60), seed=4600 + x, hands=("relax", "relax")))
    c.save(); c.translate(144, 640); c.scale(1, 0.32)
    c.new_path(); c.arc(0, 0, 120, 0, 2 * math.pi); c.set_source_rgb(*FELT); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
    c.restore()
    r = random.Random(4)
    for i in range(6):
        x, y = 90 + i * 20 + r.uniform(-4, 4), 634 + r.uniform(-6, 6)
        c.save(); c.translate(x, y); c.rotate(r.uniform(-0.5, 0.5))
        st.poly(k, [(-6, -9), (6, -9), (6, 9), (-6, 9)], (0.97, 0.96, 0.92), 1.0); c.restore()
    for o in dealers:                                                         # their pale gloves on the felt, dealing
        for i, (m, hx, hy, w, d, side) in enumerate(o["rec"]):
            c.save(); c.set_matrix(m); hp.draw(k, "palm" if i else "relax", hx, hy - 30, w * 1.25, st.GLOVE, d, -1 if i == 0 else 1); c.restore()
    st.poly(k, [(0, 700), (540, 700), (540, 960), (0, 960)], (0.10, 0.05, 0.06), 1.8)                   # the floor


VP = (250, 452)
END = (176, 330, 324, 560)        # the end wall: x0, top, x1, floor


def hall(k):
    """5.1 / 6.x: the club's hall, after the photograph: one long room seen down its length."""
    c = k.c
    ex0, et, ex1, ef = END
    c.set_source_rgb(0.02, 0.02, 0.03); c.paint()
    # the ceiling and its beams, closing toward the end
    st.poly(k, [(-20, -20), (560, -20), (ex1, et), (ex0, et)], (0.16, 0.15, 0.15), 2.0)
    L = st.Plane((-20, -20, 1000), (ex0, et, ef)); R = st.Plane((560, -20, 1000), (ex1, et, ef))
    for i in range(1, 12):
        u = i / 12.0
        a, b = L.at(u, 0), R.at(u, 0)
        th = 3 + 16 * (1 - L.s(u))
        st.poly(k, [a, b, (b[0], b[1] + th), (a[0], a[1] + th)], (0.30, 0.29, 0.28), 1.2)
    # the end wall, lit, and the double glass doors: the stage in the doorway, waiting in its light
    st.poly(k, [(ex0, et), (ex1, et), (ex1, ef), (ex0, ef)], (0.94, 0.93, 0.90), 1.8)
    for (x0, x1) in ((194, 222), (278, 306)):                                  # the side lights, small panes
        st.poly(k, [(x0, 400), (x1, 400), (x1, 556), (x0, 556)], (0.97, 0.97, 0.95), 1.4)
        for yy in range(412, 556, 26):
            c.set_source_rgb(*INK); c.set_line_width(1); c.move_to(x0, yy); c.line_to(x1, yy); c.stroke()
        c.move_to((x0 + x1) / 2, 400); c.line_to((x0 + x1) / 2, 556); c.stroke()
    st.poly(k, [(194, 360), (306, 360), (306, 396), (194, 396)], (0.97, 0.97, 0.95), 1.4)        # the transom
    for xx in range(208, 306, 22):
        c.set_source_rgb(*INK); c.set_line_width(1); c.move_to(xx, 360); c.line_to(xx, 396); c.stroke()
    st.poly(k, [(226, 400), (274, 400), (274, 558), (226, 558)], (0.40, 0.08, 0.14), 1.6)         # the doorway: the stage curtain
    for xx in range(230, 274, 9):
        c.set_source_rgb(0.55, 0.12, 0.20); c.rectangle(xx, 402, 4, 154); c.fill()
    st.poly(k, [(222, 548), (278, 548), (282, 560), (218, 560)], (0.30, 0.22, 0.16), 1.4)         # the stage's edge
    c.save(); c.translate(250, 548); c.scale(26, 5)                                               # the spot on it
    g = cairo.RadialGradient(0, 0, 0.1, 0, 0, 1); g.add_color_stop_rgba(0, 1, 1, 0.95, 0.95); g.add_color_stop_rgba(1, 1, 1, 0.95, 0)
    c.set_source(g); c.arc(0, 0, 1, 0, 2 * math.pi); c.fill(); c.restore()
    sx, sy = 312, 452                                                                             # the spotlight on its stand,
    c.set_source_rgb(*INK); c.set_line_width(3); c.move_to(sx, sy + 8); c.line_to(sx, 572); c.stroke()   # by the doorway; its
    c.move_to(sx - 12, 572); c.line_to(sx + 12, 572); c.stroke()                                  # handle at the back (above the dealers)
    c.save(); c.translate(sx, sy); c.rotate(math.radians(195))
    st.poly(k, [(-9, -8), (11, -11), (11, 11), (-9, 8)], (0.20, 0.20, 0.22), 1.6)
    c.set_source_rgb(*INK); c.set_line_width(2.4); c.move_to(-9, 0); c.line_to(-22, 0); c.stroke()
    c.restore()
    g = cairo.LinearGradient(sx, sy, 250, 548)
    g.add_color_stop_rgba(0, 1, 1, 0.95, 0.40); g.add_color_stop_rgba(1, 1, 1, 0.95, 0.10)
    c.set_source(g); c.new_path(); c.move_to(sx - 10, sy - 4); c.line_to(sx - 8, sy + 8); c.line_to(276, 552); c.line_to(228, 548); c.close_path(); c.fill()
    # the left wall: plaster above, the tall wooden panels below (the lockers of the photograph); a neon tube along it
    L.fill(k, (0.74, 0.74, 0.72), 2.2)
    for i in range(14):
        u0, u1 = i / 14.0, (i + 0.94) / 14.0
        st.poly(k, L.quad(u0, u1, 0.50, 0.97), (0.62, 0.46, 0.30), 1.2)
    for wd, al in ((18, 0.10), (10, 0.22), (4, 1.0)):
        c.set_source_rgba(*((1.0, 0.35, 0.42) if al < 1 else NEON), al); c.set_line_width(wd); c.set_line_cap(1)
        a, b = L.at(0.02, 0.44), L.at(0.98, 0.44); c.move_to(*a); c.line_to(*b); c.stroke()
    # the right wall and its alcoves (the photograph's), empty
    R.fill(k, (0.70, 0.70, 0.68), 2.2)
    st.stained_base(k, R, 91, 0.94, (0.55, 0.55, 0.53))
    for (u0, u1) in ((0.48, 0.70), (0.80, 0.90)):
        st.poly(k, R.quad(u0, u1, 0.30, 1.0), (0.22, 0.20, 0.20), 1.8)
    # the floor: boards running to the end, the end's light on them
    st.poly(k, [(-20, 1000), (560, 1000), (ex1, ef), (ex0, ef)], (0.30, 0.20, 0.14), 2.0)
    c.save(); c.new_path(); c.move_to(-20, 1000); c.line_to(560, 1000); c.line_to(ex1, ef); c.line_to(ex0, ef); c.close_path(); c.clip()
    c.set_source_rgba(0.08, 0.05, 0.04, 0.35 if MOTTO[0] else 0.8); c.set_line_width(1.4)   # v9: the boards' joints quieter (they read as a drawing)
    for i in range(-14, 15):
        xb = 250 + i * 48
        c.move_to(VP[0] + (xb - VP[0]) * 0.17, ef); c.line_to(xb, 1000); c.stroke()
    c.restore()
    g = cairo.LinearGradient(0, ef, 0, 900)
    g.add_color_stop_rgba(0, 1, 1, 0.95, 0.35); g.add_color_stop_rgba(1, 1, 1, 0.95, 0.0)
    c.set_source(g); c.new_path(); c.move_to(ex0 + 20, ef); c.line_to(ex1 - 20, ef); c.line_to(330, 900); c.line_to(170, 900); c.close_path(); c.fill()
    # the booth on the left, free-standing, its high velvet back to the panels: the Client and Dad, the lamp over Dad's face
    st.poly(k, [(24, 470), (236, 470), (236, 656), (24, 656)], VELVET_D, 2.2)
    for xx in range(34, 230, 26):
        c.set_source_rgb(*VELVET); c.rectangle(xx, 476, 15, 172); c.fill()
    co.client(k, 84, 712 + CLIENT_DY[0], 0.42, "open", "plain", look=(0.7, 0.8), roll=False, badge=False)
    o = dc.father(k, 180, 716 + CLIENT_DY[0], 0.68, (-20, 30, 20, -30), "hard", (-0.6, 0.6))
    hx, hy = o["head"]
    LOG["dad_head"] = (round(hx), round(hy))
    if HALL_LAMP[0] == "v6":
        c.set_source_rgb(*INK); c.set_line_width(2); c.move_to(hx, 330); c.line_to(hx, hy - 32); c.stroke()
        st.poly(k, [(hx - 40, hy - 32), (hx + 40, hy - 32), (hx + 58, hy + 26), (hx - 58, hy + 26)], (0.16, 0.30, 0.20), 2.0)
        g = cairo.LinearGradient(0, hy + 26, 0, 650)
        g.add_color_stop_rgba(0, 1, 1, 0.9, 0.32); g.add_color_stop_rgba(1, 1, 1, 0.9, 0.0)
        c.set_source(g); c.new_path(); c.move_to(hx - 58, hy + 26); c.line_to(hx + 58, hy + 26); c.line_to(hx + 90, 640); c.line_to(hx - 90, 640); c.close_path(); c.fill()
    else:
        # v7: the dark hides him, not the shade. Above the lamp everything is black (his head a shape against the velvet,
        # to the chin, as the frame cuts him in Daddy's Home); a small shade hangs on its cord under his chin; its cone of
        # light falls on the table, his cuffs and the ring.
        cy = hy + 34                                                                          # the chin line
        g = cairo.LinearGradient(0, cy - 6, 0, cy + 8)
        g.add_color_stop_rgba(0, 0.02, 0.02, 0.03, 0.93); g.add_color_stop_rgba(1, 0.02, 0.02, 0.03, 0.0)
        c.set_source(g); c.rectangle(128, cy - 6, 110, 14); c.fill()
        c.set_source_rgba(0.02, 0.02, 0.03, 0.93); c.rectangle(128, 470, 110, cy - 476); c.fill()
        c.set_source_rgb(0.55, 0.55, 0.57); c.set_line_width(1.4); c.move_to(hx + 6, 330); c.line_to(hx + 6, cy + 14); c.stroke()   # the cord
        st.poly(k, [(hx - 8, cy + 14), (hx + 20, cy + 14), (hx + 32, cy + 34), (hx - 20, cy + 34)], (0.16, 0.30, 0.20), 1.8)   # the shade
        c.set_source_rgb(1, 0.98, 0.88); c.new_path(); c.arc(hx + 6, cy + 35, 5, 0, math.pi); c.fill()                         # the bulb
        g = cairo.LinearGradient(0, cy + 34, 0, 650)
        g.add_color_stop_rgba(0, 1, 1, 0.9, 0.40); g.add_color_stop_rgba(1, 1, 1, 0.9, 0.04)
        c.set_source(g); c.new_path(); c.move_to(hx - 20, cy + 34); c.line_to(hx + 32, cy + 34); c.line_to(hx + 76, 640); c.line_to(hx - 64, 640); c.close_path(); c.fill()
    st.poly(k, [(14, 636), (246, 636), (246, 660), (14, 660)], (0.12, 0.06, 0.08), 2.2)              # its table: dark glass
    st.poly(k, [(96, 622), (166, 622), (170, 638), (92, 638)], (0.95, 0.93, 0.86), 1.4)               # the map on it
    # the card table on the floor, right of centre, two shadows dealing against the lit right wall
    import on4_lying as ly
    import hands_ps as hp
    dealers = []
    for x in (300, 392):
        c.save(); c.rectangle(0, 0, 540, 632); c.clip()
        ly.rim(k, x, 700, 0.36, seed=4600 + x, pose=(-40, 60, 40, -60))
        c.restore()
        dealers.append(st.thug(k, x, 700, 0.36, (-40, 60, 40, -60), seed=4600 + x, hands=("relax", "relax")))
    WOOD = (0.72, 0.45, 0.22)
    for x in (300, 392):                                                  # their chairs: the bentwood arms at their sides
        for sx in (-1, 1):
            ax = x + sx * 50
            c.set_source_rgb(*INK); c.set_line_width(9); c.set_line_cap(1)
            c.move_to(ax - sx * 22, 604); c.line_to(ax, 604); c.curve_to(ax + sx * 12, 604, ax + sx * 12, 630, ax + sx * 4, 700); c.stroke()
            c.set_source_rgb(*WOOD); c.set_line_width(6)
            c.move_to(ax - sx * 22, 604); c.line_to(ax, 604); c.curve_to(ax + sx * 12, 604, ax + sx * 12, 630, ax + sx * 4, 700); c.stroke()
            c.set_line_cap(0)
    # the game table: square, black, a chequerboard top, two dice cups, dice, the cards
    st.poly(k, [(262, 634), (430, 634), (448, 664), (244, 664)], (0.07, 0.07, 0.08), 2.4)
    for leg in (252, 440):
        c.set_source_rgb(0.07, 0.07, 0.08); c.set_line_width(6); c.move_to(leg, 664); c.line_to(leg, 704); c.stroke()
    n_, m_ = 8, 3
    for i in range(n_):
        for j in range(m_):
            u0, u1, v0, v1 = i / n_, (i + 1) / n_, j / m_, (j + 1) / m_
            def P(u, v):
                yv = 638 + v * 22; xl = 290 - v * 8; xr = 404 + v * 8
                return (xl + (xr - xl) * u, yv)
            col = (0.88, 0.62, 0.70) if (i + j) % 2 else (0.20, 0.12, 0.16)
            st.poly(k, [P(u0, v0), P(u1, v0), P(u1, v1), P(u0, v1)], col, 0.6, outline=False)
    for (x, y) in ((276, 640), (420, 638)):                               # the dice cups
        st.poly(k, [(x - 9, y - 22), (x + 9, y - 22), (x + 10, y), (x - 10, y)], (0.06, 0.06, 0.07), 1.6)
        c.save(); c.translate(x, y - 22); c.scale(9, 3); c.new_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        c.set_source_rgb(0.35, 0.35, 0.37); c.fill()
    for (x, y, a) in ((300, 652, 0.2), (312, 656, -0.3)):                 # two dice
        c.save(); c.translate(x, y); c.rotate(a)
        st.poly(k, [(-5, -5), (5, -5), (5, 5), (-5, 5)], (0.97, 0.96, 0.92), 1.0)
        c.set_source_rgb(*INK); c.new_path(); c.arc(0, 0, 1.4, 0, 2 * math.pi); c.fill(); c.restore()
    r = random.Random(4)
    for i in range(4):
        x, y = 330 + i * 18 + r.uniform(-4, 4), 648 + r.uniform(-4, 4)
        c.save(); c.translate(x, y); c.rotate(r.uniform(-0.5, 0.5))
        st.poly(k, [(-6, -9), (6, -9), (6, 9), (-6, 9)], (0.97, 0.96, 0.92), 1.0); c.restore()
    for o in dealers:
        for i, (m, hx_, hy_, w, d, side) in enumerate(o["rec"]):
            c.save(); c.set_matrix(m); hp.draw(k, "palm" if i else "relax", hx_, hy_ - 28, w * 1.25, st.GLOVE, d, -1 if i == 0 else 1); c.restore()
    # the empty chair in front, its black back to us, the bentwood arms and runners (a foreground layer)
    fx, fy = 452, 720
    st.poly(k, [(fx - 36, fy - 76), (fx + 36, fy - 76), (fx + 40, fy + 6), (fx - 40, fy + 6)], (0.05, 0.05, 0.06), 2.4)
    c.set_source_rgba(1, 1, 1, 0.18); c.set_line_width(2); c.move_to(fx - 30, fy - 70); c.curve_to(fx - 10, fy - 76, fx + 10, fy - 76, fx + 30, fy - 70); c.stroke()
    for sx in (-1, 1):
        ax = fx + sx * 44
        c.set_source_rgb(*INK); c.set_line_width(9); c.set_line_cap(1)
        c.move_to(ax, fy - 36); c.curve_to(ax + sx * 12, fy - 36, ax + sx * 12, fy, ax + sx * 6, fy + 60); c.line_to(ax - sx * 30, fy + 60); c.stroke()
        c.set_source_rgb(*WOOD); c.set_line_width(6)
        c.move_to(ax, fy - 36); c.curve_to(ax + sx * 12, fy - 36, ax + sx * 12, fy, ax + sx * 6, fy + 60); c.line_to(ax - sx * 30, fy + 60); c.stroke()
        c.set_line_cap(0)


def motto(k):
    """v9: Daddy's Home's motto over the booth (dh_props.booth's), in exact NEON so the accent pass keeps it red; drawn by
    on4_scenes after the hall's dark (which would grey it)."""
    c = k.c
    for i, (txt, sz) in enumerate((("THE HOUSE", 15), ("ALWAYS", 21), ("COLLECTS", 21))):
        yy = 384 + i * 27
        c.set_source_rgba(0.10, 0.01, 0.03, 0.85); c.rectangle(46, yy - 22, 168, 28); c.fill()
        kit.text(k, txt, 130, yy, sz, NEON)


def light_hall(c):
    ons.vignette(c, 0.6)


def light_inside(c):
    ons.vignette(c, 0.55)


def map_insert(k):
    """5.2: ten small boxes in two rows, an arrow, a big Z; Dad's ringed hand flat on the Z; the velvet cuff."""
    c = k.c
    c.set_source_rgb(0.12, 0.06, 0.08); c.paint()
    st.poly(k, [(40, 150), (500, 140), (510, 640), (30, 650)], (0.95, 0.93, 0.86), 2.4)
    for i in range(10):
        x, y = 80 + (i % 5) * 52, 230 + (i // 5) * 70
        st.poly(k, [(x, y), (x + 40, y), (x + 40, y + 44), (x, y + 44)], (0.95, 0.93, 0.86), 2.2)
        c.set_source_rgb(*INK); c.set_line_width(2); c.move_to(x + 6, y + 18); c.line_to(x + 34, y + 18); c.stroke()
    c.set_source_rgb(*INK); c.set_line_width(7); c.set_line_cap(1)
    c.move_to(200, 400); c.curve_to(230, 460, 280, 470, 320, 470); c.stroke()
    c.move_to(320, 470); c.line_to(296, 450); c.stroke(); c.move_to(320, 470); c.line_to(298, 492); c.stroke()
    c.select_font_face("Lilita One", 0, 0); c.set_font_size(170); c.move_to(330, 590); c.set_source_rgb(*INK); c.show_text("Z")
    # Dad's hand flat on the Z: the velvet cuff from the right, the gold ring
    st.poly(k, [(560, 560), (490, 590), (496, 650), (560, 650)], VELVET, 2.4)               # the cuff, below the Z
    kit.ellipse(k, 468, 616, 40, 30, dc.SKIN_F, 7001, shadow=False, lw=2.4)
    for i in range(4):                                                                     # four fingers flat, the first on
        c.set_source_rgb(*dc.SKIN_F); c.set_line_width(13); c.set_line_cap(1)               # the Z's bottom corner
        c.move_to(450 - i * 2, 600 + i * 12); c.line_to(420 - i * 4, 594 + i * 14); c.stroke()
    dc.ring(k, 444, 604, 1.4)


def uptimez_card(k, x, y, s=1.0, ang=0.0):
    """A white business card: the series' mark and UPTIMEZ big (brand.py), readable on a phone in black and white."""
    import brand
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    st.poly(k, [(-110, -62), (110, -62), (110, 62), (-110, 62)], (0.98, 0.98, 0.96), 2.6)
    brand.mark(c, -100, -36, 72, zzz=False)
    c.select_font_face(brand.CORP, 0, 1); c.set_font_size(25); c.set_source_rgb(*brand.NAVY)
    c.move_to(-20, 8); c.show_text("UPTIME")
    c.set_source_rgb(*brand.GREEN); c.move_to(-20 + c.text_extents("UPTIME").x_advance, 8); c.show_text("Z")
    c.set_font_size(14); c.set_source_rgb(*brand.NAVY); c.move_to(-18, 32); c.show_text("INC.")
    c.restore()


def _plan_card_v7(k):
    """5.2's held end: the card lies flat across the middle, on the tape between the two rows (over all ten, covering no
    number); his hand has let go and lifts away to the right, fingers open, the ring still in frame (whose hand)."""
    c = k.c
    CX, CY, CS, CA = 262, 392, 0.62, -0.04
    c.save(); c.translate(CX + 6, CY + 8); c.rotate(CA); c.scale(86, 50)                    # its shadow: tight, it is down
    g = cairo.RadialGradient(0, 0, 0.3, 0, 0, 1); g.add_color_stop_rgba(0, 0, 0, 0, 0.55); g.add_color_stop_rgba(1, 0, 0, 0, 0)
    c.set_source(g); c.arc(0, 0, 1, 0, 2 * math.pi); c.fill(); c.restore()
    uptimez_card(k, CX, CY, CS, CA)
    HX, HY = 418, 470                                                                     # the hand, lifted off, open
    c.save(); c.translate(HX, HY); c.rotate(-0.25)
    c.set_source_rgba(0, 0, 0, 0.35); c.new_path(); c.arc(-6, 26, 30, 0, 2 * math.pi); c.fill()   # its shadow, apart from it
    st.poly(k, [(150, -30), (40, -16), (44, 44), (150, 52)], VELVET, 2.4)                 # the velvet cuff
    c.set_source_rgb(0.96, 0.96, 0.94); c.rectangle(30, -14, 14, 58); c.fill()
    kit.ellipse(k, 0, 12, 40, 30, dc.SKIN_F, 7002, shadow=False, lw=2.4)
    for i in range(4):                                                                    # fingers open, lifted
        a0 = (-20 + i * 10, -4 + i * 10); a1 = (-56 + i * 2, -26 + i * 18)
        c.set_source_rgb(*INK); c.set_line_width(15); c.set_line_cap(1); c.move_to(*a0); c.line_to(*a1); c.stroke()
        c.set_source_rgb(*dc.SKIN_F); c.set_line_width(11.5); c.move_to(*a0); c.line_to(*a1); c.stroke()
    c.set_line_cap(0)
    dc.ring(k, -24, 14, 1.5)
    c.restore()


def plan_insert(k):
    """5.2: his plan flat on the dark glass table; Dad's hand from the right lays the UptimeZ card on it."""
    import cs_props as cp
    c = k.c
    c.set_source_rgb(0.12, 0.06, 0.08); c.paint()
    old = (cp.PROPS4[0], cp.TITLE_TAPE[0], cp._bg)
    cp.PROPS4[0], cp.TITLE_TAPE[0] = True, True
    v7 = PLAN_CARD[0] != "v6"
    if v7:                                     # v7: one title (her pen label); the painted title under the seams is left out,
        class _Off(list):                      # and the tape over the 7 sits higher so its number reads
            def __setitem__(self, i, v): pass
        old7 = (cp.ac.TITLE, cp.TAPE7_DY[0])
        cp.ac.TITLE = _Off([False]); cp.TAPE7_DY[0] = -15
    cp._bg = lambda *a, **kw: None
    c.save(); c.translate(250, 400); c.rotate(-0.06); c.scale(1.15, 1.15); c.translate(-270, -470)
    try:
        cp.plan(k, "whole", 740)
        if v7:                                 # v7: the bottom row's numbers again, whole (the strips' clip cut the 7)
            c.save(); c.translate(270, 470); c.scale(3.9, 3.9)
            c.select_font_face("Inter", 0, 1); c.set_font_size(8.5)
            for n, bx, by, bw, bh in cp.ac._bays():
                if by >= 0:
                    t = str(n); e = c.text_extents(t)
                    c.set_source_rgb(0.20, 0.20, 0.22); c.rectangle(bx + bw / 2 - e.x_advance / 2 - 2, by + bh - 0.5, e.x_advance + 4, 11.5); c.fill()
                    c.set_source_rgb(1, 1, 1); c.move_to(bx + bw / 2 - e.x_advance / 2, by + bh + 9); c.show_text(t)
            c.restore()
    finally:
        c.restore()
        cp.PROPS4[0], cp.TITLE_TAPE[0], cp._bg = old
        if v7:
            cp.ac.TITLE, cp.TAPE7_DY[0] = old7
    if PLAN_CARD[0] != "v6":
        _plan_card_v7(k)
        return
    # the card going down onto the middle of the plan, a soft shadow under it, Dad's hand on it
    c.save(); c.translate(282, 556); c.rotate(0.12); c.scale(130, 74)
    g = cairo.RadialGradient(0, 0, 0.2, 0, 0, 1); g.add_color_stop_rgba(0, 0, 0, 0, 0.45); g.add_color_stop_rgba(1, 0, 0, 0, 0)
    c.set_source(g); c.arc(0, 0, 1, 0, 2 * math.pi); c.fill(); c.restore()
    uptimez_card(k, 270, 540, 1.0, 0.10)
    HX, HY = 0, -14                                                                        # his hand on the card's corner
    st.poly(k, [(560, 600 + HY), (450, 622 + HY), (456, 690 + HY), (560, 690 + HY)], VELVET, 2.4)    # the velvet cuff
    c.set_source_rgb(0.96, 0.96, 0.94); c.rectangle(440, 616 + HY, 16, 70); c.fill()       # the shirt cuff
    kit.ellipse(k, 410, 640 + HY, 44, 32, dc.SKIN_F, 7001, shadow=False, lw=2.4)          # the back of his hand,
    for i in range(4):                                                                     # four fingers flat on the card
        c.set_source_rgb(*INK); c.set_line_width(16); c.set_line_cap(1)
        c.move_to(388 - i * 2, 622 + HY + i * 12); c.line_to(350 - i * 4, 612 + HY + i * 14); c.stroke()
        c.set_source_rgb(*dc.SKIN_F); c.set_line_width(12.5)
        c.move_to(388 - i * 2, 622 + HY + i * 12); c.line_to(350 - i * 4, 612 + HY + i * 14); c.stroke()
    c.set_line_cap(0)
    dc.ring(k, 380, 626 + HY, 1.5)


def render(fn, lit, scale=2):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540 * scale, 960 * scale); s.set_device_scale(scale, scale)
    c = cairo.Context(s); fn(Ctx(c, 0))
    eng.TONE = "v3"; eng.accent_pass(s, [(NEON, 1.0), (GOLD, 0.35)])
    lit(cairo.Context(s))
    return s


def sheet(out="../office-noir-4/on4_club_sheet_v7.png", phone="../office-noir-4/on4_club_phone_v7.png"):
    HALL_LAMP[0] = PLAN_CARD[0] = FRONT_LIGHT[0] = "v7"
    panels = [(lambda k: front(k, True), lambda c: light_front(c, True), "FRONT 4.1-4.3: the lit passage, the marquee, the heart, Dad's limousine"),
              (hall, light_hall, "INSIDE 5.1 / 6.x: the hall, the booth, the game table, the stage at the end"),
              (plan_insert, light_inside, "5.2: his MY GARAGES plan; Dad lays the UptimeZ card on it")]
    W_, H_ = 3 * 560 + 20, 70 + 960 + 50
    sh = cairo.ImageSurface(cairo.FORMAT_RGB24, W_, H_); c = cairo.Context(sh)
    c.set_source_rgb(0.93, 0.92, 0.89); c.paint()
    c.set_source_rgb(0.1, 0.1, 0.1); c.select_font_face("Inter", 0, 1); c.set_font_size(26)
    c.move_to(20, 42); c.show_text("OFFICE NOIR 4 · Dad's club · v7 (Dad in the dark, the card laid down, the front lit from the arch; dead zones in red)")
    x = 20
    smalls = []
    for i, (fn, lit, lab) in enumerate(panels):
        s = render(fn, lit, 2)
        c.set_source_surface(s, x, 70); c.paint()
        if i < 2:
            c.save(); c.translate(x, 70); st.overlay(c); c.restore()
        c.set_source_rgb(0.1, 0.1, 0.1); c.select_font_face("Inter", 0, 1); c.set_font_size(17)
        c.move_to(x, 70 + 960 + 30); c.show_text(lab)
        smalls.append(s)
        x += 560
    sh.write_to_png(out)
    ph = cairo.ImageSurface(cairo.FORMAT_RGB24, 2 * 270 + 10, 480); c = cairo.Context(ph); c.set_source_rgb(1, 1, 1); c.paint()
    for i in range(2):
        c.save(); c.translate(i * 280, 0); c.scale(0.5, 0.5); c.set_source_surface(smalls[i], 0, 0); c.paint(); c.restore()
    ph.write_to_png(phone)
    return out


if __name__ == "__main__":
    print(sheet(), LOG)
