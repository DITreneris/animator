"""OFFICE NOIR 4: Dad's club, v1 (23 Nov). Stage 3 (look and set). Script v3, beats 04-06: the club is Dad's (a nightclub
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


def front(k):
    c = k.c
    st.sky(k)
    # the lit facade, a cornice, the door: a big wooden double gate with a round top (ref v2)
    st.poly(k, [(-10, 120), (550, 120), (550, 640), (-10, 640)], st.CREAM, 2.2)
    st.poly(k, [(-10, 110), (550, 110), (550, 132), (-10, 132)], (0.80, 0.75, 0.62), 1.8)
    st.plaster(k, st.Plane((-10, 430, 640), (550, 430, 640)).quad, 81, n=5)
    gx, gw, gt, gb = 300, 130, 452, 640
    c.new_path(); c.move_to(gx - gw / 2, gb); c.line_to(gx - gw / 2, gt + gw / 2); c.arc(gx, gt + gw / 2, gw / 2, math.pi, 0); c.line_to(gx + gw / 2, gb); c.close_path()
    c.set_source_rgb(0.30, 0.18, 0.14); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.6); c.stroke()
    c.set_source_rgb(0.18, 0.10, 0.08); c.set_line_width(2.4); c.move_to(gx, gt + 10); c.line_to(gx, gb); c.stroke()
    for yy in (560, 640, 720):
        c.move_to(gx - gw / 2 + 8, yy); c.line_to(gx + gw / 2 - 8, yy); c.stroke()
    for sx in (-1, 1):                                                       # the rings, brass
        c.set_source_rgb(0.75, 0.62, 0.30); c.set_line_width(3); c.new_path(); c.arc(gx + sx * 18, 620, 8, 0, 2 * math.pi); c.stroke()
    # the marquee over the door, in the top band: the heart, PAM-CAT, the bulb strip, ONLY FOR YOU
    st.poly(k, [(40, 150), (500, 150), (500, 420), (40, 420)], (0.06, 0.06, 0.07), 2.6)
    for i in range(32):                                                      # bulbs round its edge
        u = i / 31
        st.bulb(c, 48 + u * 444, 158, 2.4); st.bulb(c, 48 + u * 444, 412, 2.4)
    neon_heart(c, 270, 196, 20)
    neon_text(k, "PAM-CAT", 270, 290, 74)
    bulb_strip(k, 70, 470, 330, "ONE EVENING · ONCE IN A LIFETIME", 18)
    neon_text(k, "ONLY FOR YOU", 270, 396, 46)
    c.set_source_rgb(*st.INK); c.set_line_width(4)                           # its brackets
    for x in (90, 450):
        c.move_to(x, 420); c.line_to(x - 20, 470); c.stroke()
    # the pavement, the kerb, the cobbles; the sedan parked at the kerb, empty
    st.poly(k, [(-10, 640), (550, 640), (550, 690), (-10, 690)], st.PAVE, 1.8)
    def road():
        c.new_path(); c.rectangle(-10, 694, 560, 270)
    road(); c.set_source_rgb(*st.ROAD); c.fill()
    st.setts(k, road, 694, 960, -10, 550, -10, 550, seed=55)
    sedan_side(k, 190, 716, 0.85)                                           # above the dead zone (G3), left of the rail


def light_front(c):
    ons.key_light(c, 270, 600, 220, 0.18)
    g = cairo.LinearGradient(0, 120, 0, 450)                                 # the marquee lights the wall under it
    g.add_color_stop_rgba(0, 1, 0.9, 0.9, 0.0); g.add_color_stop_rgba(1, 1, 0.9, 0.9, 0.0)
    ons.vignette(c, 0.65)


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
    co.client(k, 316, 720, 0.42, "open", "plain", look=(0.6, 0.8), roll=False, badge=False)
    o = dc.father(k, 416, 724, 0.68, (-20, 30, 20, -30), "hard", (-0.6, 0.6))              # at the Client's size (measured)
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


def render(fn, lit, scale=2):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540 * scale, 960 * scale); s.set_device_scale(scale, scale)
    c = cairo.Context(s); fn(Ctx(c, 0))
    eng.TONE = "v3"; eng.accent_pass(s, [(NEON, 1.0), (GOLD, 0.35)])
    lit(cairo.Context(s))
    return s


def sheet(out="../office-noir-4/on4_club_sheet_v1.png", phone="../office-noir-4/on4_club_phone_v1.png"):
    panels = [(front, light_front, "FRONT 4.1-4.3: the door, the marquee, the sedan"),
              (inside, light_inside, "INSIDE 5.1 / 6.x: stage, spotlight, card table, booth"),
              (map_insert, light_inside, "MAP 5.2: ten boxes, the arrow, the Z, his hand")]
    W_, H_ = 3 * 560 + 20, 70 + 960 + 50
    sh = cairo.ImageSurface(cairo.FORMAT_RGB24, W_, H_); c = cairo.Context(sh)
    c.set_source_rgb(0.93, 0.92, 0.89); c.paint()
    c.set_source_rgb(0.1, 0.1, 0.1); c.select_font_face("Inter", 0, 1); c.set_font_size(26)
    c.move_to(20, 42); c.show_text("OFFICE NOIR 4 · Dad's club · v1 (dead zones in red on the first two)")
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
