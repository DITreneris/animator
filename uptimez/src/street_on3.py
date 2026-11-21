"""OFFICE NOIR 3: the street, set v3 (20 Nov; street_on3_v1.py, _v2.py are pinned). After cold test 13: the page is seen
photograph first (cv_insert(lift=0): her picture clipped over the heading: a contract), then lifted (lift=1: CV, the
lines, her number: an application); her hand stays on the folder until his gloves have it.
v2 (street_on3_v1.py is v1). After cold test 12 and Tomas: Sofia on the street
and in the photograph is the star of Office Noir 2, her dress black here (his gloves are the only red); the page is
The Onboarding's CV (portrait in the corner, CV printed whole, the number small and circled, no lipstick telephone);
the folder comes straight down out of the window to his gloves; his raised glove is answered: the glass goes back up.
v1 (Tomas, /grill-me): Outside the arena, at night: the arena's wall with
its fight posters, one street lamp with one pool of light, wet stones, and at the far right the arena door (beat 04's
door: the same place). Mom's limousine stops along the kerb; she is a ringed hand at the rear window and no more.
World: 900 wide, the pavement's front edge at G. Zones: A (0-330) where he walks in; B (330-620) the lamp's pool, where
the car stops and Sofia passes; C (620-900) the arena door.
frame(cam, mid, car, ...) -> a 540x960 surface in the dream's look. window_pov(...) is his view into the car (2.4);
cv_insert(...) is the folder open under the lamp (2.5, 2.7). Nothing here changes an earlier module."""
import math
import cairo
import kit
import client_on3 as b
import client_sheet_on3 as csh
import sofia_on3 as so3
import noir2_cast as n2
from kit import Ctx, cut, rect, ellipse, INK

WW, G = 900, 1400
LAMP_X = 470
DOOR_X = 760
NIGHT = (0.07, 0.07, 0.09)
BRICK, BRICK_D = (0.22, 0.22, 0.25), (0.14, 0.14, 0.16)
SKIN = (0.90, 0.76, 0.66)
PAPER = (0.94, 0.93, 0.88)
CAMS = {"S1": (420, 1160, 0.82),                           # the master: the whole street
        "S2": (430, 1180, 1.25),                           # the lamp's pool: him and the car
        "S3": (560, 1190, 1.35)}                           # the pool, toward the door: him and her


def view(c, cx, cy, z):
    c.translate(270, 480); c.scale(z, z); c.translate(-cx, -cy)


V5 = [False]                                               # v5 (Tomas, after the first moving rough): the poster, the car, her plain photograph


def poster2(k, x, y, s=1.0, seed=0):
    """v5: a proper fight bill: TONIGHT, HUMAN vs ROBOT, a red glove against a robot's head. Larger than v1's."""
    c = k.c
    c.save(); c.translate(x - 14, y - 34); c.scale(s * 1.3, s * 1.3)
    rect(k, 0, 0, 96, 136, PAPER, seed, shadow=False, lw=2.4)
    c.set_source_rgb(*INK); c.rectangle(4, 4, 88, 18); c.fill()
    kit.text(k, "TONIGHT", 48, 13.5, 11.5, PAPER, bold=True)
    kit.text(k, "HUMAN", 48, 36, 19, INK, bold=True)
    ellipse(k, 24, 68, 16, 15, b.KEY, seed + 2, shadow=False, lw=2)                                   # the glove
    ellipse(k, 14, 74, 6, 7, b.KEY, seed + 3, shadow=False, lw=1.6)
    rect(k, 58, 55, 28, 26, (0.20, 0.20, 0.23), seed + 4, shadow=False, lw=2)                         # the robot's head: a screen, an aerial
    c.set_source_rgb(*PAPER); c.rectangle(63, 62, 6, 4); c.fill(); c.rectangle(75, 62, 6, 4); c.fill(); c.rectangle(64, 72, 16, 3); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(2); c.move_to(72, 55); c.line_to(72, 48); c.stroke(); c.arc(72, 46, 2.4, 0, 2 * math.pi); c.fill()
    kit.text(k, "VS", 46, 69, 13, INK, bold=True)
    kit.text(k, "ROBOT", 48, 100, 19, INK, bold=True)
    c.set_source_rgb(*INK); c.set_line_width(1.6); c.move_to(10, 114); c.line_to(86, 114); c.stroke()
    kit.text(k, "LAST ROUND", 48, 124, 9.5, INK, bold=True)
    c.restore()


def limo2(k, x, y, s=1.0, window=0.0, beams=True):
    """v5: a long limousine that looks its price: a long bonnet, swept wings over white-walled wheels, a running board,
    a tall grille and a mascot, four side windows with blinds, light along the roof and the wings. A third larger.
    The rear glass is where v1's was, so the staging does not move."""
    c = k.c
    z = 1.34 * s
    c.save(); c.translate(x + 350 * s - 430 * z, y); c.scale(z, z)             # the rear glass (centre 430 here) stays over v1's (350)
    if beams:
        g = cairo.LinearGradient(-360, 0, -70, 0); g.add_color_stop_rgba(0, 1, 1, 1, 0); g.add_color_stop_rgba(1, 1, 1, 1, 0.6)
        c.set_source(g); c.move_to(-70, -66); c.line_to(-360, -128); c.line_to(-360, 6); c.close_path(); c.fill()
    body, gloss = (0.05, 0.05, 0.06), (0.62, 0.62, 0.66)
    cut(k, [(-78, -30), (-80, -78), (-50, -98), (150, -104), (196, -160), (236, -168), (520, -168), (566, -150), (600, -100), (640, -92), (646, -30)], body, shadow=False, lw=3)
    c.set_source_rgb(*gloss); c.set_line_width(3.4); c.set_line_cap(1)                                # light along the bonnet and the roof
    c.move_to(-46, -96); c.line_to(148, -102); c.stroke(); c.move_to(240, -166); c.line_to(516, -166); c.stroke(); c.set_line_cap(0)
    for wx in (40, 540):                                                                             # the wings, swept over the wheels
        cut(k, [(wx - 66, -30), (wx - 58, -62), (wx - 22, -82), (wx + 26, -82), (wx + 60, -60), (wx + 84, -30)], (0.08, 0.08, 0.10), shadow=False, lw=3)
        c.set_source_rgb(*gloss); c.set_line_width(2.6); c.move_to(wx - 54, -62); c.curve_to(wx - 20, -84, wx + 26, -84, wx + 58, -60); c.stroke()
        ellipse(k, wx, -22, 36, 36, (0.03, 0.03, 0.04), wx, shadow=False, lw=3)
        ellipse(k, wx, -22, 26, 26, (0.92, 0.92, 0.90), wx + 1, shadow=False, lw=2)                    # the white wall
        ellipse(k, wx, -22, 15, 15, (0.10, 0.10, 0.12), wx + 2, shadow=False, lw=2)
        ellipse(k, wx, -22, 7, 7, (0.86, 0.86, 0.88), wx + 3, shadow=False, lw=1.4)
    rect(k, 104, -34, 356, 10, (0.30, 0.30, 0.33), 7, shadow=False, lw=2.4)                            # the running board
    c.set_source_rgb(0.86, 0.86, 0.88); c.set_line_width(4); c.move_to(-76, -70); c.line_to(640, -64); c.stroke()   # the chrome line
    rect(k, -84, -92, 16, 56, (0.80, 0.80, 0.84), 8, shadow=False, lw=2.4)                             # the grille
    c.set_source_rgb(0.20, 0.20, 0.23); c.set_line_width(1.6)
    for gy in (-84, -74, -64, -54, -44):
        c.move_to(-82, gy); c.line_to(-70, gy); c.stroke()
    for i, (gx0, gw) in enumerate(((204, 74), (290, 84))):                                             # the front glasses: blinds half down
        rect(k, gx0, -156, gw, 48, (0.16, 0.17, 0.20), 9 + i, shadow=False, lw=2.2)
        c.set_source_rgb(0.42, 0.42, 0.45); c.rectangle(gx0 + 3, -153, gw - 6, 20); c.fill()
    rect(k, 386, -156, 88, 48, (0.02, 0.02, 0.03), 12, shadow=False, lw=2.6)                           # the rear glass: black
    if window > 0:
        c.set_source_rgb(0.20, 0.20, 0.23); c.rectangle(388, -154, 84, 12 * window); c.fill()
    rect(k, 486, -156, 44, 48, (0.02, 0.02, 0.03), 13, shadow=False, lw=2.2)                           # the quarter light
    for hx in (300, 392):                                                                             # door handles
        rect(k, hx, -92, 18, 5, (0.86, 0.86, 0.88), hx, shadow=False, lw=1.4)
    ellipse(k, -74, -52, 11, 15, (1, 1, 0.96), 5, shadow=False, lw=2)                                  # the lamp
    c.set_source_rgb(0.86, 0.86, 0.88); c.set_line_width(3); c.move_to(-58, -98); c.line_to(-58, -118); c.stroke()   # the mascot
    cut(k, [(-58, -118), (-36, -126), (-58, -130)], (0.86, 0.86, 0.88), shadow=False, lw=1.6)
    c.set_source_rgba(1, 1, 1, 0.16); c.rectangle(-70, 12, 700, 10); c.fill()                          # it shines in the wet road
    c.restore()


def her(k, x, feet, s=1.0, look=(0.6, 0.0)):
    """Her picture. v1 to v4: Office Noir 2's star in black (feet as star() takes them). v5: The Onboarding's Sofia as
    on an identity photograph: her everyday jacket, looking straight out, nothing in her hands."""
    if not V5[0]:
        return star(k, x, feet, s, "g_stand", "interested", look)
    import sofia_ob as sob
    yc = feet - 272 * s
    return sob.sofia(k, x, yc + 40 * s + 243 * s * 1.1, s * 1.1, "low", "smile", (0, 0), badge=False, tablet_kind=None)


def poster(k, x, y, s=1.0, seed=0):
    """A fight poster: a red glove against a round dark head, TONIGHT. No names."""
    if V5[0]:
        return poster2(k, x, y, s, seed)
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    rect(k, 0, 0, 96, 132, PAPER, seed, shadow=False, lw=2.2)
    ellipse(k, 64, 46, 20, 20, (0.10, 0.10, 0.12), seed + 1, shadow=False, lw=2)
    ellipse(k, 34, 50, 18, 16, b.KEY, seed + 2, shadow=False, lw=2)
    kit.text(k, "TONIGHT", 48, 100, 17, INK, bold=True)
    c.restore()


def limo(k, x, y, s=1.0, window=0.0, beams=True):
    """The limousine, side on, its nose to screen left, along the kerb. (x, y): under the front wheel.
    window 0..1: the rear glass down a hand's width."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    if beams:
        g = cairo.LinearGradient(-330, 0, -60, 0); g.add_color_stop_rgba(0, 1, 1, 1, 0); g.add_color_stop_rgba(1, 1, 1, 1, 0.55)
        c.set_source(g); c.move_to(-60, -74); c.line_to(-330, -130); c.line_to(-330, 6); c.close_path(); c.fill()
    body = (0.05, 0.05, 0.06)
    cut(k, [(-70, -40), (-66, -84), (20, -96), (150, -100), (190, -150), (420, -152), (470, -98), (560, -92), (566, -36)], body, shadow=False, lw=3)
    c.set_source_rgb(0.86, 0.86, 0.88); c.set_line_width(4)   # the chrome line, nose to tail
    c.move_to(-64, -70); c.line_to(560, -66); c.stroke()
    for wx in (30, 470):                                       # the wheels
        ellipse(k, wx, -22, 34, 34, (0.03, 0.03, 0.04), wx, shadow=False, lw=3)
        ellipse(k, wx, -22, 15, 15, (0.80, 0.80, 0.82), wx + 1, shadow=False, lw=2)
    rect(k, 200, -140, 80, 40, (0.16, 0.17, 0.20), 3, shadow=False, lw=2)                          # the front side glass
    rect(k, 300, -140, 100, 40, (0.02, 0.02, 0.03), 4, shadow=False, lw=2.4)                       # the rear glass: black
    if window > 0:
        c.set_source_rgb(0.20, 0.20, 0.23); c.rectangle(302, -138, 96, 12 * window); c.fill()      # down a hand's width
    ellipse(k, -62, -74, 9, 13, (1, 1, 0.96), 5, shadow=False, lw=2)                               # the lamp
    c.set_source_rgb(0.86, 0.86, 0.88); c.set_line_width(3); c.move_to(-40, -96); c.line_to(-40, -116); c.stroke()   # the mascot
    ellipse(k, -40, -120, 8, 5, (0.86, 0.86, 0.88), 6, shadow=False, lw=1.6)
    c.restore()


def draw_street(k, mid=(), car=None, rain=0, door_open=False):
    """mid: the cast on the pavement, back to front. car: (x, window) or None: the limousine along the kerb, in front."""
    c = k.c
    c.set_source_rgb(*NIGHT); c.rectangle(-600, -400, WW + 1200, G + 1400); c.fill()
    rect(k, -600, G - 620, WW + 1200, 560, BRICK, 3, shadow=False, lw=3)                           # the arena's wall
    c.set_source_rgb(*BRICK_D); c.set_line_width(2)
    for i in range(14):
        y = G - 600 + i * 40
        c.move_to(-600, y); c.line_to(WW + 600, y); c.stroke()
        for j in range(-8, 22):
            x = j * 70 + (35 if i % 2 else 0)
            c.move_to(x, y); c.line_to(x, y + 40); c.stroke()
    rect(k, DOOR_X - 60, G - 330, 120, 270, (0.90, 0.90, 0.86) if door_open else (0.12, 0.12, 0.14), 5, shadow=False, lw=4)   # the arena door
    rect(k, DOOR_X - 74, G - 392, 148, 44, (0.06, 0.06, 0.07), 6, shadow=False, lw=3)
    kit.text(k, "ARENA", DOOR_X, G - 370, 26, (0.96, 0.96, 0.92), bold=True)
    for i, px_ in enumerate((60, 190, 600)):
        poster(k, px_, G - 300 + (i % 2) * 14, 1.0, 20 + i * 5)
    cut(k, [(-600, G - 60), (WW + 600, G - 60), (WW + 600, G + 16), (-600, G + 16)], (0.34, 0.34, 0.37), shadow=False, lw=3)   # the pavement
    c.set_source_rgb(0.10, 0.10, 0.12); c.rectangle(-600, G + 16, WW + 1200, 800); c.fill()        # the wet road
    g = cairo.RadialGradient(LAMP_X, G - 30, 10, LAMP_X, G - 30, 250)                              # the lamp's pool
    g.add_color_stop_rgba(0, 1, 1, 1, 0.75); g.add_color_stop_rgba(1, 1, 1, 1, 0)
    c.save(); c.rectangle(-600, G - 60, WW + 1200, 600); c.clip(); c.translate(0, G - 30); c.scale(1, 0.34); c.translate(0, -(G - 30))
    c.set_source(g); c.paint(); c.restore()
    c.new_path(); c.move_to(LAMP_X - 26, G - 520); c.line_to(LAMP_X + 26, G - 520); c.line_to(LAMP_X + 190, G - 40); c.line_to(LAMP_X - 190, G - 40); c.close_path()
    g = cairo.LinearGradient(0, G - 520, 0, G - 40); g.add_color_stop_rgba(0, 1, 1, 1, 0.34); g.add_color_stop_rgba(1, 1, 1, 1, 0.06)
    c.set_source(g); c.fill()
    c.set_source_rgb(0.05, 0.05, 0.06); c.set_line_width(9); c.move_to(LAMP_X + 150, G - 56); c.line_to(LAMP_X + 150, G - 560)
    c.line_to(LAMP_X + 10, G - 560); c.stroke()                                                    # the lamp post, its arm
    cut(k, [(LAMP_X - 34, G - 520), (LAMP_X - 16, G - 556), (LAMP_X + 16, G - 556), (LAMP_X + 34, G - 520)], (0.05, 0.05, 0.06), shadow=False, lw=2.4)
    ellipse(k, LAMP_X, G - 520, 26, 7, (1, 1, 0.96), 7, shadow=False, lw=1.6)
    for fn in mid:
        fn(k)
    if car:
        (limo2 if V5[0] else limo)(k, car[0], G + 96, 1.0, car[1])
        c.set_source_rgba(1, 1, 1, 0.10)                     # its shine on the wet road
        c.rectangle(car[0] - 60, G + 104, 620, 60); c.fill()
    if rain:
        c.set_source_rgba(1, 1, 1, 0.22); c.set_line_width(2)
        for i in range(90):
            x = (i * 137 + rain * 60) % (WW + 600) - 300; y = (i * 251 + rain * 190) % 1400 + G - 1100
            c.move_to(x, y); c.line_to(x - 8, y + 34); c.stroke()


def frame(cam, mid=(), car=None, **kw):
    cam = CAMS[cam] if isinstance(cam, str) else cam
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(s); k = Ctx(c, 0)
    c.save(); view(c, *cam); draw_street(k, mid, car, **kw); c.restore()
    csh.noir(s)
    return s


def star(k, x, feet, s=1.0, pose="g_stand", face="interested", look=(-0.8, 0.0), **kw):
    """Office Noir 2's star, as he dreams her: the same gown, wrap and earrings, the gown black."""
    old = n2.LOOK[0]; n2.LOOK[0] = 9
    try:
        with n2._swap((n2, "KEY", (0.07, 0.07, 0.08))):
            return n2.star(k, x, feet, s, pose, face, look, **kw)
    finally:
        n2.LOOK[0] = old


def _ring_hand(k, x, y, s=1.0):
    """Her small hand from the dark, palm down, two rings, a fur cuff behind it."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    rect(k, 30, -26, 90, 52, (0.86, 0.86, 0.88), 3, shadow=False, lw=2.4)
    for i in range(4):
        ellipse(k, 44 + i * 22, -26, 14, 10, (0.86, 0.86, 0.88), 4 + i, shadow=False, lw=1.6)
        ellipse(k, 44 + i * 22, 26, 14, 10, (0.86, 0.86, 0.88), 8 + i, shadow=False, lw=1.6)
    ellipse(k, 0, 0, 40, 30, SKIN, 12, shadow=False, lw=2.6)
    for i, dy in enumerate((-20, -7, 7, 20)):
        rect(k, -74, dy - 6, 46, 12, SKIN, 13 + i, shadow=False, lw=2)
        if i in (1, 2):
            rect(k, -58, dy - 8, 11, 16, (0.86, 0.87, 0.90), 17 + i, shadow=False, lw=1.4)
    c.restore()


def folder(k, x, y, s=1.0, ang=0.0):
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    cut(k, [(-40, -28), (40, -28), (40, 28), (-40, 28)], (0.86, 0.80, 0.62), lw=2.2)
    cut(k, [(14, -38), (38, -38), (38, -28), (14, -28)], (0.86, 0.80, 0.62), shadow=False, lw=1.8)
    c.restore()


def window_pov(down=1.0, out=0.0, take=0.0, fist=0.0, door=False):
    """His view of the car's rear door, black. down 0..1: the glass down a hand's width. fist 0..1: one red glove of
    his raised at the glass (2.3: the glass answers by going back up). out 0..1: from the dark her ringed hand comes
    down out of the gap with the folder hanging from it, straight at him. take 0..1: his two gloves come up from the
    frame's foot and have it between them; her hand goes back in."""
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(s); k = Ctx(c, 0)
    c.set_source_rgb(0.05, 0.05, 0.06); c.paint()
    c.set_source_rgb(0.86, 0.86, 0.88); c.set_line_width(7); c.move_to(-10, 700); c.line_to(550, 690); c.stroke()         # the chrome line
    if door:                                                 # v4, opt-in: it is a car (two viewers took the window for a monitor): the roof's line, the door's seams, a wheel arch, rain on the paint
        c.set_source_rgb(0.11, 0.11, 0.13); c.new_path(); c.move_to(-10, 960); c.line_to(-10, 96); c.curve_to(120, 44, 420, 40, 550, 84); c.line_to(550, 960); c.close_path(); c.fill()
        c.set_source_rgb(0.86, 0.86, 0.88); c.set_line_width(6); c.move_to(-10, 96); c.curve_to(120, 44, 420, 40, 550, 84); c.stroke()      # the roof's chrome
        c.set_source_rgb(0.02, 0.02, 0.03); c.set_line_width(4)
        for x0, x1 in ((34, 26), (508, 520)):
            c.move_to(x0, 80); c.line_to(x1, 960); c.stroke()                                                            # the door's seams
        c.set_source_rgb(0.02, 0.02, 0.03); c.arc(600, 1010, 250, 0, 2 * math.pi); c.fill()                              # the rear wheel's arch
        c.set_source_rgb(0.30, 0.30, 0.33); c.set_line_width(5); c.arc(600, 1010, 250, math.pi, 1.5 * math.pi); c.stroke()
        c.set_source_rgba(1, 1, 1, 0.30); c.set_line_width(2.4); c.set_line_cap(1)
        for i in range(16):
            x = 30 + (i * 197) % 480; y = 470 + (i * 131) % 380
            c.move_to(x, y); c.line_to(x - 3, y + 16 + (i % 3) * 8); c.stroke()                                          # rain, running down the door
        c.set_line_cap(0)
    rect(k, 60, 110, 420, 330, (0.02, 0.02, 0.03), 3, shadow=False, lw=6)                                               # the window: nothing inside
    gap = 80 * down
    c.set_source_rgb(0.30, 0.31, 0.35); c.rectangle(64, 114 + gap, 412, 322 - gap); c.fill()                           # the glass goes DOWN: the gap is at the top
    c.set_source_rgba(1, 1, 1, 0.20); c.set_line_width(10); c.move_to(110, 410); c.line_to(250, 170 + gap); c.stroke()  # the lamp, in the glass
    c.set_source_rgb(0.80, 0.80, 0.84); c.set_line_width(3); c.move_to(64, 114 + gap); c.line_to(476, 114 + gap); c.stroke()
    ellipse(k, 440, 560, 26, 12, (0.86, 0.86, 0.88), 4, shadow=False, lw=2.4)                                           # the door's handle
    if door:
        cut(k, [(476, 106), (486, 106), (486, 446), (476, 446), (392, 106)], (0.11, 0.11, 0.13), shadow=False, lw=0)     # the rear pillar: the window slopes
        c.set_source_rgb(0.02, 0.02, 0.03); c.set_line_width(6); c.move_to(392, 108); c.line_to(478, 444); c.stroke()
    if out > 0:
        hy = 114 + gap * 0.5 + 150 * out + 60 * min(take, 0.8)   # her hand, over the glass's edge, fingers down; it follows him down
        fy = 114 + gap * 0.5 + 150 * out + 150 + 150 * take                           # the folder, hanging from it; then in his gloves
        folder(k, 270, fy, 3.2, -0.05)
        if take < 0.8:
            c.save(); c.translate(270, hy); c.rotate(-math.pi / 2); _ring_hand(k, 0, 0, 1.25); c.restore()
            c.set_source_rgb(0.02, 0.02, 0.03); c.rectangle(64, 108, 412, max(hy - 150, 4)); c.fill()                   # the dark she comes out of
    for side, gx in ((-1, 150), (1, 390)):                   # his gloves, from the frame's foot
        gy = 1040 - 250 * take
        c.save(); c.translate(gx, gy); c.scale(3.6, 3.6); c.translate(-gx, -gy)
        cut(k, [(gx - 22, gy + 26), (gx + 22, gy + 26), (gx + 26, gy + 120), (gx - 26, gy + 120)], (0.24, 0.24, 0.27), shadow=False, lw=1.2)
        b._glove(k, gx, gy, -side * 0.25, -0.97, side, 61 + side)
        c.restore()
    if fist > 0:                                             # one glove, raised at the glass, and held
        gx, gy = 330, 1080 - 520 * fist
        c.save(); c.translate(gx, gy); c.scale(4.4, 4.4); c.translate(-gx, -gy)
        cut(k, [(gx - 22, gy + 26), (gx + 22, gy + 26), (gx + 30, gy + 160), (gx - 30, gy + 160)], (0.24, 0.24, 0.27), shadow=False, lw=1.2)
        b._glove(k, gx, gy, 0.05, -1.0, 1, 66)
        c.restore()
    csh.noir(s)
    return s


def cv_insert(lift=0.0):
    """2.5 / 2.7, from above, under the lamp: the folder open on his gloves. lift 0: her photograph, large, clipped
    over the top of the page; nothing else to read: a contract. lift 1: one glove has pushed the photograph up on its
    clip; under it, The Onboarding's sheet: CV, lines, and her number, circled."""
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(s); k = Ctx(c, 0)
    c.set_source_rgb(0.30, 0.30, 0.33); c.paint()
    g = cairo.RadialGradient(270, 420, 40, 270, 420, 620); g.add_color_stop_rgba(0, 1, 1, 1, 0.5); g.add_color_stop_rgba(1, 0, 0, 0, 0.4)
    c.set_source(g); c.paint()
    cut(k, [(40, 170), (500, 150), (512, 800), (52, 820)], (0.86, 0.80, 0.62), lw=3)                # the folder, open
    cut(k, [(80, 200), (470, 186), (478, 770), (88, 784)], PAPER, shadow=False, lw=2.4)             # the page
    kit.text(k, "CV", 270, 300, 110, INK, bold=True)
    c.set_source_rgb(0.55, 0.55, 0.58); c.set_line_width(7); c.set_line_cap(1)
    for y, x0, x1 in ((400, 120, 430), (440, 120, 390), (480, 120, 420), (520, 120, 350)):
        c.move_to(x0, y); c.line_to(x1, y - 3); c.stroke()
    c.set_line_cap(0)
    kit.text(k, "555 0142", 270, 650, 50, INK, bold=True)
    c.set_source_rgb(*b.KEY); c.set_line_width(6); c.save(); c.translate(270, 647); c.scale(158, 48); c.arc(0, 0, 1, 0.3, 6.6); c.restore(); c.stroke()
    if lift < 0.5:                                           # her photograph, over all of it
        rect(k, 104, 214, 340, 500, (0.98, 0.98, 0.96), 3, shadow=True, lw=3)
        c.save(); c.rectangle(114, 224, 320, 480); c.clip(); c.set_source_rgb(0.62, 0.62, 0.64); c.paint()
        her(k, 274, 420 + 272 * 2.2, 2.2, (0.6, 0.0)); c.restore()
    else:                                                    # pushed up on its clip: its back, above the page
        cut(k, [(110, 216), (440, 204), (452, 40), (122, 52)], (0.80, 0.80, 0.80), shadow=True, lw=3)
    rect(k, 250, 196, 44, 30, (0.70, 0.70, 0.74), 9, shadow=False, lw=2)                             # the clip
    for side, gx, gy in (((-1, 60, 850), (1, 480, 850)) if lift < 0.5 else ((-1, 60, 850), (1, 450, 130))):
        c.save(); c.translate(gx, gy); c.scale(3.4, 3.4); c.translate(-gx, -gy)
        b._glove(k, gx, gy, -side * 0.3, -0.95 if gy > 400 else 0.95, side, 71 + side)
        c.restore()
    csh.noir(s)
    return s
