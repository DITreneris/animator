"""OFFICE NOIR 4: Dad's car, v2 (23 Nov): three_q (the turn) and cabin (3.4) added from refs v4-v5; sheet_v1 kept.
v1 (23 Nov), from Tomas's three photographs (office-noir-4/ref/on4_car_ref_v1..v3.jpg).
A long black modern limousine, no real make: a tall upright chrome grille with vertical bars, thin light lines for
lamps (white at the front, the series' neon red at the back), a long bonnet, coach doors with their handles side by side,
a chrome sill strip, big many-spoked chrome wheels, cream seats, and a starlit headliner seen through the glass.
Left out on purpose: the mascot on the bonnet, every monogram and badge (bonnet, plate, wheels, headrests) and the
plate's letters. The bonnet stays bare (Mom's limo, car_on3.py, has her curler there; this one is Dad's and says nothing).

  side(k, x, base, s, glass="stars")    nose left. (x, base): the middle of the car on the ground.
  front(k, x, base, s)                  head on, (x, base) the middle on the ground.
  rear(k, x, base, s, window=0.0)       from behind; window 0..1 lowers the rear window (3.4, the ringed hand).
  reflect(k, fn, base, alpha)           draws fn() and its mirror in a wet floor under base.
  glow(c, view, x, base, s, lamps)      after the grade: the lamps' light (headlights white, taillights red).
Drawn in greys and the exact NEON before the noir pass, so the accent pass keeps the taillights red."""
import math
import random
import cairo
from kit import INK

NEON = (0.93, 0.13, 0.22)
BODY = (0.06, 0.06, 0.075)
BODY_HI = (0.16, 0.16, 0.19)          # the long highlight along the flank and the bonnet's crown
CHROME = (0.86, 0.87, 0.90)
CHROME_D = (0.46, 0.48, 0.53)
GLASS = (0.10, 0.10, 0.13)
CREAM = (0.88, 0.84, 0.74)
LAMP = (0.99, 0.99, 0.97)


def _p(c, pts):
    c.new_path(); c.move_to(*pts[0])
    for q in pts[1:]:
        c.line_to(*q)
    c.close_path()


def _rr(c, x, y, w, h, r):
    r = min(r, w / 2, h / 2)
    c.new_path(); c.arc(x + r, y + r, r, math.pi, 1.5 * math.pi); c.arc(x + w - r, y + r, r, 1.5 * math.pi, 2 * math.pi)
    c.arc(x + w - r, y + h - r, r, 0, 0.5 * math.pi); c.arc(x + r, y + h - r, r, 0.5 * math.pi, math.pi); c.close_path()


def _fs(c, fill, lw=2.0):
    c.set_source_rgb(*fill); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(lw); c.stroke()


RIM = (0.42, 0.42, 0.47)


def _rim(c):
    """a thin grey edge inside the ink line, so the black body reads against a dark street (lesson 47)."""
    c.set_source_rgb(*RIM); c.set_line_width(1.0); c.stroke()


def _line(c, a, b, col, lw):
    c.set_source_rgb(*col); c.set_line_width(lw); c.new_path(); c.move_to(*a); c.line_to(*b); c.stroke()


def _stars(c, x0, y0, x1, y1, n, seed):
    """the starlit headliner: small points in the top of the glass (clip to the glass first)."""
    r = random.Random(seed)
    for _ in range(n):
        x = r.uniform(x0, x1); y = y0 + (y1 - y0) * r.random() ** 2
        c.set_source_rgb(1, 0.97, 0.88); c.new_path(); c.arc(x, y, r.uniform(0.5, 1.1), 0, 2 * math.pi); c.fill()


def _wheel(c, x, y, R):
    c.new_path(); c.arc(x, y, R, 0, 2 * math.pi); _fs(c, INK, 2.0)                       # the tyre
    c.new_path(); c.arc(x, y, R * 0.74, 0, 2 * math.pi); _fs(c, (0.20, 0.20, 0.23), 1.4)  # the rim's dish
    for i in range(16):                                                                   # many fine spokes
        a = i * math.pi / 8
        _line(c, (x + math.cos(a) * R * 0.2, y + math.sin(a) * R * 0.2),
              (x + math.cos(a + 0.12) * R * 0.70, y + math.sin(a + 0.12) * R * 0.70), CHROME, 1.6)
    c.new_path(); c.arc(x, y, R * 0.72, 0, 2 * math.pi); c.set_source_rgb(*CHROME); c.set_line_width(2.2); c.stroke()
    c.new_path(); c.arc(x, y, R * 0.2, 0, 2 * math.pi); _fs(c, (0.10, 0.10, 0.12), 1.4)  # the hub, no badge


# ---- side, nose left ---------------------------------------------------------------------------------------------------

def side(k, x, base, s=1.0, glass="stars"):
    """nose left, 340 long at s=1, roof at -100. glass: "stars" (cream headrests under a starlit roof) or "dark"."""
    c = k.c
    c.save(); c.translate(x, base); c.scale(s, s)
    body = [(-168, -14), (-174, -40), (-172, -60), (-160, -66), (-60, -72), (-22, -100), (98, -100), (132, -74),
            (166, -68), (172, -50), (170, -20), (162, -12)]
    _p(c, body); _fs(c, BODY, 2.4); _rim(c)
    # the long highlight: bonnet crown and the shoulder line, as in the photograph's reflections
    _line(c, (-160, -64), (-64, -70), BODY_HI, 3.0)
    _line(c, (-150, -50), (164, -52), BODY_HI, 2.4)
    # the glasshouse: front door window, rear (coach) door window, a small quarter light; a chrome surround
    wins = [[(-52, -74), (-20, -96), (30, -96), (30, -74)],
            [(36, -74), (36, -96), (92, -96), (112, -78), (112, -74)]]
    for w in wins:
        _p(c, w); c.set_source_rgb(*GLASS); c.fill()
    if glass == "stars":
        for w, sx in zip(wins[:2], (6, 72)):
            c.save(); _p(c, w); c.clip()
            _stars(c, min(p[0] for p in w), -96, max(p[0] for p in w), -86, 22, 400 + sx)
            _rr(c, sx - 10, -88, 20, 16, 5); _fs(c, CREAM, 1.2)                          # a headrest
            c.restore()
    for w in wins:
        _p(c, w); c.set_source_rgb(*CHROME); c.set_line_width(2.0); c.stroke()
    _line(c, (33, -96), (33, -16), INK, 2.0)                                              # the coach doors' shut line
    _line(c, (-52, -74), (-58, -16), INK, 1.6)                                            # the front door's leading edge
    _line(c, (114, -74), (118, -26), INK, 1.6)                                            # the rear door's trailing edge
    for hx in (16, 40):                                                                   # the two handles, side by side
        _rr(c, hx - 9, -60, 18, 4, 2); _fs(c, CHROME, 1.0)
    _line(c, (-66, -20), (132, -20), CHROME, 2.6)                                         # the chrome sill strip
    _rr(c, -175, -58, 8, 14, 3); _fs(c, LAMP, 1.2)                                        # the headlight's line
    _rr(c, 165, -62, 7, 18, 3); c.set_source_rgb(*NEON); c.fill()                         # the taillight's line
    _rr(c, -64, -82, 12, 10, 3); _fs(c, BODY, 1.4)                                        # the mirror
    for wx in (-114, 104):                                                                # arches, then wheels
        c.new_path(); c.arc(wx, -28, 34, math.pi, 2 * math.pi); c.close_path(); c.set_source_rgb(0.02, 0.02, 0.03); c.fill()
        _wheel(c, wx, -28, 28)
    c.restore()


# ---- front, head on -----------------------------------------------------------------------------------------------------

def front(k, x, base, s=1.0, glass="stars"):
    c = k.c
    c.save(); c.translate(x, base); c.scale(s, s)
    for sx in (-1, 1):                                                                    # the tyres under the body
        _rr(c, sx * 84 - 13, -34, 26, 34, 5); _fs(c, INK, 1.6)
    _p(c, [(-82, -104), (82, -104), (62, -150), (-62, -150)]); _fs(c, BODY, 2.2)          # the roof and pillars
    _p(c, [(-82, -104), (82, -104), (62, -150), (-62, -150)]); _rim(c)
    _p(c, [(-70, -106), (70, -106), (55, -144), (-55, -144)]); c.set_source_rgb(*GLASS); c.fill()
    if glass == "stars":
        c.save(); _p(c, [(-70, -106), (70, -106), (55, -144), (-55, -144)]); c.clip()
        _stars(c, -55, -144, 55, -132, 30, 711)
        for hx in (-32, 32):
            _rr(c, hx - 13, -124, 26, 20, 6); _fs(c, CREAM, 1.2)
        c.restore()
    _p(c, [(-70, -106), (70, -106), (55, -144), (-55, -144)]); c.set_source_rgb(*CHROME); c.set_line_width(1.6); c.stroke()
    for sx in (-1, 1):                                                                    # the mirrors
        _p(c, [(sx * 78, -114), (sx * 100, -118), (sx * 100, -104), (sx * 80, -102)]); _fs(c, BODY, 1.6)
    _p(c, [(-98, -24), (-100, -88), (-86, -104), (86, -104), (100, -88), (98, -24)]); _fs(c, BODY, 2.4)   # the body
    _p(c, [(-98, -24), (-100, -88), (-86, -104), (86, -104), (100, -88), (98, -24)]); _rim(c)
    _line(c, (-84, -100), (84, -100), BODY_HI, 2.4)                                       # the bonnet's crown
    # the grille: tall and upright, a chrome surround, vertical bars
    _rr(c, -32, -96, 64, 64, 3); _fs(c, CHROME, 2.0)
    _p(c, [(-26, -90), (26, -90), (26, -38), (-26, -38)]); c.set_source_rgb(0.08, 0.08, 0.10); c.fill()
    for i in range(11):
        bx = -24 + i * 4.8
        _line(c, (bx, -89), (bx, -39), CHROME, 2.0)
    _p(c, [(-34, -100), (34, -100), (32, -96), (-32, -96)]); _fs(c, CHROME, 1.2)          # the bonnet's chrome cap
    for sx in (-1, 1):                                                                    # the lamps: a thin bright frame
        _rr(c, min(sx * 40, sx * 86), -82, 46, 16, 7); _fs(c, (0.10, 0.10, 0.12), 1.6)
        _rr(c, min(sx * 40, sx * 86) + 1.5, -80.5, 43, 13, 6); c.set_source_rgb(*LAMP); c.set_line_width(3.0); c.stroke()
        for j in (0, 1):
            c.new_path(); c.arc(sx * (52 + j * 18), -74, 3.2, 0, 2 * math.pi); c.set_source_rgb(0.75, 0.76, 0.80); c.fill()
    _line(c, (-96, -32), (96, -32), CHROME, 2.4)                                          # the bumper's chrome lines
    _line(c, (-90, -26), (90, -26), CHROME_D, 1.6)
    for sx in (-1, 1):                                                                    # the low intakes, dark mesh
        _rr(c, min(sx * 44, sx * 88), -48, 44, 12, 3); _fs(c, (0.03, 0.03, 0.04), 1.2)
    _rr(c, -24, -30, 48, 9, 2); _fs(c, (0.04, 0.04, 0.05), 1.2)                           # a blank plate
    c.restore()


# ---- rear ----------------------------------------------------------------------------------------------------------------

def rear(k, x, base, s=1.0, window=0.0, glass="stars", inside=None):
    """window: 0 shut .. 1 the rear side window down (seen as the dark gap at the left pillar). inside(k) draws what is
    in the cabin, clipped to the rear glass (the ringed hand, 3.4)."""
    c = k.c
    c.save(); c.translate(x, base); c.scale(s, s)
    for sx in (-1, 1):
        _rr(c, sx * 82 - 13, -32, 26, 32, 5); _fs(c, INK, 1.6)
    glass_pts = [(-64, -108), (64, -108), (52, -142), (-52, -142)]
    _p(c, [(-80, -104), (80, -104), (60, -150), (-60, -150)]); _fs(c, BODY, 2.2)
    _p(c, [(-80, -104), (80, -104), (60, -150), (-60, -150)]); _rim(c)
    _p(c, glass_pts); c.set_source_rgb(*GLASS); c.fill()
    c.save(); _p(c, glass_pts); c.clip()
    if glass == "stars":
        _stars(c, -52, -142, 52, -132, 26, 913)
        for hx in (-30, 30):
            _rr(c, hx - 13, -128, 26, 20, 6); _fs(c, CREAM, 1.2)
    if inside:
        inside(k)
    c.restore()
    _p(c, glass_pts); c.set_source_rgb(*CHROME); c.set_line_width(1.6); c.stroke()
    for sx in (-1, 1):
        _p(c, [(sx * 76, -114), (sx * 96, -116), (sx * 96, -104), (sx * 78, -102)]); _fs(c, BODY, 1.6)
    _p(c, [(-96, -22), (-98, -90), (-84, -104), (84, -104), (98, -90), (96, -22)]); _fs(c, BODY, 2.4)
    _p(c, [(-96, -22), (-98, -90), (-84, -104), (84, -104), (98, -90), (96, -22)]); _rim(c)
    _line(c, (-82, -100), (82, -100), BODY_HI, 2.2)
    for sx in (-1, 1):                                                                    # the taillights: tall, red lines
        x0 = min(sx * 66, sx * 88)
        _rr(c, x0, -90, 22, 36, 6); _fs(c, (0.10, 0.04, 0.05), 1.6)
        _rr(c, x0 + 2, -88, 18, 32, 5); c.set_source_rgb(*NEON); c.set_line_width(3.4); c.stroke()
    _rr(c, -44, -86, 88, 8, 3); _fs(c, CHROME, 1.4)                                       # the boot's chrome handle
    _rr(c, -34, -74, 68, 22, 3); _fs(c, (0.04, 0.04, 0.05), 1.4)                          # the plate recess, blank
    _line(c, (-90, -40), (90, -40), BODY_HI, 1.8)
    _line(c, (-86, -30), (86, -30), CHROME, 2.2)                                          # the bumper's chrome line
    for sx in (-1, 1):                                                                    # twin exhausts
        x0 = min(sx * 40, sx * 66)
        _rr(c, x0, -26, 26, 9, 3); _fs(c, (0.02, 0.02, 0.03), 1.0)
        _rr(c, x0, -26, 26, 9, 3); c.set_source_rgb(*CHROME); c.set_line_width(1.8); c.stroke()
    c.restore()


# ---- the wet floor -------------------------------------------------------------------------------------------------------

def reflect(k, fn, base, alpha=0.28, depth=90):
    """fn() draws the car; its mirror in the wet stone under base, fading over depth."""
    c = k.c
    c.push_group(); fn(); pat = c.pop_group()
    c.save()
    c.translate(0, 2 * base); c.scale(1, -1)
    c.set_source(pat)
    m = cairo.LinearGradient(0, base, 0, base - depth)
    m.add_color_stop_rgba(0, 0, 0, 0, alpha); m.add_color_stop_rgba(1, 0, 0, 0, 0)
    c.mask(m)
    c.restore()
    c.set_source(pat); c.paint()


def glow(c, view, x, base, s=1.0, lamps=1.0):
    """after the grade: the lamps' light. view: "side", "front" or "rear"."""
    def g(px, py, r, col, a):
        gr = cairo.RadialGradient(px, py, 0, px, py, r)
        gr.add_color_stop_rgba(0, col[0], col[1], col[2], a); gr.add_color_stop_rgba(1, col[0], col[1], col[2], 0)
        c.set_source(gr); c.new_path(); c.arc(px, py, r, 0, 2 * math.pi); c.fill()
    W, R = (1, 1, 0.94), (1, 0.18, 0.24)
    if view == "side":
        g(x - 171 * s, base - 51 * s, 26 * s, W, 0.5 * lamps); g(x + 168 * s, base - 53 * s, 22 * s, R, 0.45 * lamps)
    elif view == "front":
        for sx in (-1, 1):
            g(x + sx * 63 * s, base - 74 * s, 46 * s, W, 0.55 * lamps)
    elif view == "rear":
        for sx in (-1, 1):
            g(x + sx * 77 * s, base - 72 * s, 34 * s, R, 0.5 * lamps)


# ---- v2: the turn (three-quarter) and the cabin (Tomas's refs v4, v5) ------------------------------------------------------

CABIN_HAND = ["v1"]               # v2 (opt-in, the board review): the dropping hand's fingers
GOLD = (0.98, 0.80, 0.36)            # the whisky: the grade's second accent, so it stays warm
WOOD = (0.30, 0.17, 0.10)


def three_q(k, x, base, s=1.0, end="rear", lamps=True):
    """three-quarter: the end face (rear or front) near the camera at the left, the flank running away up to the right
    (ref v5, bottom right). (x, base): where the end face meets the flank, on the ground. end="front" is the car turning
    toward the camera; "rear" is it turning away."""
    c = k.c
    k1, k2, sh = 0.46 * s, 0.88 * s, 0.05
    c.save()
    c.transform(cairo.Matrix(-k1, sh * s, 0, k2, x + 170 * k1, base - 170 * sh * s))   # u=170 (the rear) at the join
    if end == "front":                                                                   # flank seen from the nose end
        c.translate(0, 0); c.scale(-1, 1)
    side(k, 0, 0, 1.0)
    c.restore()
    fs = 0.62 * s
    c.save(); c.translate(x - 98 * fs * 0.78, base); c.scale(0.78, 1)
    (rear if end == "rear" else front)(k, 0, 0, fs)
    c.restore()


def glow_three_q(c, x, base, s=1.0, end="rear"):
    fs = 0.62 * s; cx = x - 98 * fs * 0.78
    col, a, r, dy = ((1, 0.18, 0.24), 0.5, 30, 72) if end == "rear" else ((1, 1, 0.94), 0.55, 40, 74)
    for sx in (-1, 1):
        px, py = cx + sx * (77 if end == "rear" else 63) * fs * 0.78, base - dy * fs
        g = cairo.RadialGradient(px, py, 0, px, py, r * s)
        g.add_color_stop_rgba(0, col[0], col[1], col[2], a); g.add_color_stop_rgba(1, col[0], col[1], col[2], 0)
        c.set_source(g); c.new_path(); c.arc(px, py, r * s, 0, 2 * math.pi); c.fill()


def cabin(k, x, y, s=1.0, down=1.0, hand=True, seed=5150):
    """3.4, close: the rear door from outside, its window down by `down`; inside, the cream seat with its pleats, the
    starlit roof, the wood console with a decanter and two cut glasses (the whisky in GOLD); out of the window, Dad's
    velvet cuff and ringed hand letting a fold of bills go. (x, y): the window's bottom left corner on the door."""
    import dh_cast as dc
    import kit
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    W, H = 300, 170
    _p(c, [(-30, -H - 40), (W + 60, -H - 40), (W + 60, 140), (-30, 140)]); _fs(c, BODY, 2.4)          # the door, black
    _line(c, (-30, 70), (W + 60, 70), BODY_HI, 3.0)
    _rr(c, 40, 30, 40, 8, 3); _fs(c, CHROME, 1.2)                                                       # the handle
    win = [(0, 0), (W, 0), (W, -H + 30), (W - 40, -H), (0, -H)]
    _p(c, win); c.set_source_rgb(0.05, 0.04, 0.05); c.fill()
    c.save(); _p(c, win); c.clip()
    _stars(c, 0, -H, W, -H + 50, 70, seed)                                                              # the starlit roof
    _p(c, [(90, -H + 40), (230, -H + 40), (244, 0), (76, 0)]); _fs(c, CREAM, 1.8)                     # the seat back
    for i in range(1, 6):
        xx = 90 + i * 23
        _line(c, (xx, -H + 48), (xx - 2 + (i - 3) * 2, -4), (0.70, 0.66, 0.56), 1.4)
    _rr(c, 120, -H + 4, 80, 38, 12); _fs(c, CREAM, 1.6)                                                 # the headrest
    _p(c, [(0, -44), (88, -44), (84, 0), (0, 0)]); _fs(c, WOOD, 1.6)                                  # the console, wood
    _line(c, (0, -44), (88, -44), CHROME, 2.0)
    # the decanter and two glasses on its tray
    _p(c, [(22, -92), (52, -92), (56, -56), (54, -46), (20, -46), (18, -56)]); _fs(c, (0.82, 0.84, 0.88), 1.6)
    _p(c, [(21, -70), (55, -70), (54, -48), (20, -48)]); c.set_source_rgb(*GOLD); c.fill()
    _rr(c, 31, -106, 12, 14, 3); _fs(c, (0.82, 0.84, 0.88), 1.4)                                       # its stopper
    for gx in (62, 76):
        _p(c, [(gx - 6, -66), (gx + 6, -66), (gx + 5, -46), (gx - 5, -46)]); _fs(c, (0.86, 0.88, 0.92), 1.2)
        _p(c, [(gx - 5, -56), (gx + 5, -56), (gx + 5, -47), (gx - 5, -47)]); c.set_source_rgb(*GOLD); c.fill()
    if down < 1.0:                                                                                      # the glass still up
        gy = -H * (1 - down)
        c.set_source_rgba(0.55, 0.58, 0.64, 0.45); c.rectangle(0, gy, W, H); c.fill()
    c.restore()
    _p(c, win); c.set_source_rgb(*CHROME); c.set_line_width(3.0); c.stroke()
    if hand:                                                                                             # the cuff out of the window
        import on4_lying as ly
        VEL, VEL_D = dc.VELVET, dc.VELVET_D
        _p(c, [(150, -70), (270, -96), (282, -50), (166, -20)]); _fs(c, VEL, 2.4)
        c.set_source_rgb(0.96, 0.96, 0.94); _p(c, [(140, -66), (156, -70), (170, -22), (154, -18)]); c.fill()
        kit.ellipse(k, 128, -30, 36, 28, dc.SKIN_F, 7003, shadow=False, lw=2.4)
        for i in range(4):                                                                              # fingers open, down
            a0 = (112 + i * 8, -16 + i * 2); a1 = (104 + i * 7, 18 + i * 3)
            if CABIN_HAND[0] != "v1":                                 # v2: fingers of different lengths, curling down
                L = (0.75, 1.15, 1.25, 0.95)[i]
                a1 = (a0[0] - 10 * L + i * 3, a0[1] + 34 * L); cm = (a0[0] - 12, a0[1] + 14 * L)
                for col, lw in ((INK, 14), (dc.SKIN_F, 10.5)):
                    c.set_source_rgb(*col); c.set_line_width(lw); c.set_line_cap(1)
                    c.move_to(*a0); c.curve_to(cm[0], cm[1], a1[0] - 4, a1[1] - 10, a1[0] + 4, a1[1]); c.stroke()
                continue
            c.set_source_rgb(*INK); c.set_line_width(14); c.set_line_cap(1); c.move_to(*a0); c.line_to(*a1); c.stroke()
            c.set_source_rgb(*dc.SKIN_F); c.set_line_width(10.5); c.move_to(*a0); c.line_to(*a1); c.stroke()
        c.set_line_cap(0)
        dc.ring(k, 118, -14, 1.4)
        for j, (bx, by, ba) in enumerate(((96, 70, 0.4), (122, 96, -0.5), (84, 118, 0.9))):          # the bills, falling
            ly.bill(k, bx, by, ba, 1.6, seed + j)
    c.restore()


# ---- the sheet: the turnaround, and the car in its three places -----------------------------------------------------

def _in_setup(which, draw_car, glow_car, **kw):
    import engine_on as eng
    import on4_street as st
    from kit import Ctx
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1080, 1920); s.set_device_scale(2, 2)
    c = cairo.Context(s); k = Ctx(c, 0)
    draw, lit = st.SETUPS[which]
    draw(k, **kw); draw_car(k)
    eng.TONE = "v3"; eng.accent_pass(s, [(st.NEON, 1.0), (st.GOLD, 0.35)])
    lit(cairo.Context(s)); glow_car(cairo.Context(s))           # lit() may leave its context moved
    return s


def b_end(k):
    """1.4 / 2.1: waiting at the end of the lane, from behind (replaces the old sedan of setup B)."""
    reflect(k, lambda: rear(k, 300, 574, 0.36), 574, 0.25, 20)


def c_bump(k, x=236, base=760, s=1.25):
    """3.2: head on, at walking pace, the bumper by her head."""
    reflect(k, lambda: front(k, x, base, s), base, 0.30, 60)


def turnaround(k):
    c = k.c
    c.set_source_rgb(0.13, 0.13, 0.14); c.paint()
    c.set_source_rgb(0.22, 0.22, 0.23); c.rectangle(0, 0, 540, 960); c.fill()
    for y0 in (260, 560, 860):
        c.set_source_rgb(0.30, 0.29, 0.28); c.rectangle(0, y0, 540, 90); c.fill()
    reflect(k, lambda: side(k, 270, 260, 1.4), 260, 0.28, 60)
    reflect(k, lambda: front(k, 270, 560, 1.6), 560, 0.28, 60)
    reflect(k, lambda: rear(k, 270, 860, 1.6), 860, 0.28, 60)


def sheet_v1(out="../office-noir-4/on4_car_sheet_v1.png", phone="../office-noir-4/on4_car_phone_v1.png"):
    import engine_on as eng
    import on4_street as st
    import on4_club as cl
    from kit import Ctx
    from PIL import Image

    def turn():
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1080, 1920); s.set_device_scale(2, 2)
        k = Ctx(cairo.Context(s), 0); turnaround(k)
        eng.TONE = "v3"; eng.accent_pass(s, [(st.NEON, 1.0), (st.GOLD, 0.35)])
        c = cairo.Context(s); glow(c, "side", 270, 260, 1.4); glow(c, "front", 270, 560, 1.6); glow(c, "rear", 270, 860, 1.6)
        return s
    panels = [(turn(), "Dad's car: side, front, rear (no make, no badge)"),
              (_in_setup("B", b_end, lambda c: glow(c, "rear", 300, 574, 0.36), car=False), "B 1.4 / 2.1: waiting at the end"),
              (_in_setup("C", c_bump, lambda c: glow(c, "front", 236, 760, 1.25)), "C 3.2: the headlights, the bump"),
              (cl.render(lambda k: cl.front(k, True), lambda c: cl.light_front(c, True)), "4.1: parked at the club, empty")]
    W_, H_ = 4 * 560 + 20, 70 + 960 + 40 + 230 + 30
    sh = cairo.ImageSurface(cairo.FORMAT_RGB24, W_, H_); c = cairo.Context(sh)
    c.set_source_rgb(0.93, 0.92, 0.89); c.paint()
    c.set_source_rgb(0.1, 0.1, 0.1); c.select_font_face("Inter", 0, 1); c.set_font_size(26)
    c.move_to(20, 42); c.show_text("Office Noir 4: Dad's car, v1 (from Tomas's three photographs; dead zones in red)")
    for i, (s, lab) in enumerate(panels):
        x = 20 + i * 560
        c.set_source_surface(s, x, 70); c.paint()
        if i:
            c.save(); c.translate(x, 70); st.overlay(c); c.restore()
        c.set_source_rgb(0.1, 0.1, 0.1); c.select_font_face("Inter", 0, 1); c.set_font_size(18)
        c.move_to(x, 70 + 960 + 28); c.show_text(lab)
    rx = 20
    for i in (1, 2, 3):
        im = Image.open("../office-noir-4/ref/on4_car_ref_v%d.jpg" % i).convert("RGB")
        w0, h0 = im.size; sc = 230 / h0
        im = im.resize((int(w0 * sc), 230)); im.save("/tmp/_r.png")
        ri = cairo.ImageSurface.create_from_png("/tmp/_r.png")
        c.set_source_surface(ri, rx, 70 + 960 + 44); c.paint(); rx += ri.get_width() + 10
    sh.write_to_png(out)
    ph = cairo.ImageSurface(cairo.FORMAT_RGB24, 4 * 280 - 10, 480); c = cairo.Context(ph); c.set_source_rgb(1, 1, 1); c.paint()
    for i, (s, _) in enumerate(panels):
        c.save(); c.translate(i * 280, 0); c.scale(0.5, 0.5); c.set_source_surface(s, 0, 0); c.paint(); c.restore()
    ph.write_to_png(phone)
    return out


def c_turn(k):
    """3.1: at the junction the car swings round toward the crossing: the three-quarter, nose to the camera."""
    reflect(k, lambda: three_q(k, 250, 640, 0.62, "front"), 640, 0.25, 30)


def c_cabin(k):
    """3.4, medium: the rear window down, the starlit cabin, the decanter; the ringed hand lets the bills go."""
    c = k.c
    c.set_source_rgba(0, 0, 0, 0.55); c.paint()
    cabin(k, 40, 500, 1.45, 1.0, True)


def sheet(out="../office-noir-4/on4_car_sheet_v2.png", phone="../office-noir-4/on4_car_phone_v2.png"):
    """v2: the turn and the cabin added (Tomas, 23 Nov: "Posukis ir vidus"); the crossing's stripes flat (on4_street v5)."""
    import engine_on as eng
    import on4_street as st
    import on4_club as cl
    from kit import Ctx
    st.ZEBRA[0] = "v5"
    cl.HALL_LAMP[0] = cl.PLAN_CARD[0] = cl.FRONT_LIGHT[0] = "v7"

    def turn():
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1080, 1920); s.set_device_scale(2, 2)
        k = Ctx(cairo.Context(s), 0); c = k.c
        c.set_source_rgb(0.22, 0.22, 0.23); c.paint()
        for y0 in (200, 420, 640, 860):
            c.set_source_rgb(0.30, 0.29, 0.28); c.rectangle(0, y0, 540, 70); c.fill()
        reflect(k, lambda: side(k, 270, 200, 1.2), 200, 0.28, 40)
        reflect(k, lambda: front(k, 150, 420, 1.1), 420, 0.28, 40)
        reflect(k, lambda: rear(k, 400, 420, 1.1), 420, 0.28, 40)
        reflect(k, lambda: three_q(k, 230, 640, 1.0, "rear"), 640, 0.28, 40)
        reflect(k, lambda: three_q(k, 230, 860, 1.0, "front"), 860, 0.28, 40)
        eng.TONE = "v3"; eng.accent_pass(s, [(st.NEON, 1.0), (st.GOLD, 0.35)])
        c = cairo.Context(s)
        glow(c, "side", 270, 200, 1.2); glow(c, "front", 150, 420, 1.1); glow(c, "rear", 400, 420, 1.1)
        glow_three_q(c, 230, 640, 1.0, "rear"); glow_three_q(c, 230, 860, 1.0, "front")
        return s
    panels = [(turn(), "Turnaround: side, front, rear, turning away, turning to us"),
              (_in_setup("B", b_end, lambda c: glow(c, "rear", 300, 574, 0.36), car=False), "B 1.4 / 2.1: waiting at the end"),
              (_in_setup("C", c_turn, lambda c: glow_three_q(c, 250, 640, 0.62, "front")), "C 3.1: it swings round at the junction"),
              (_in_setup("C", c_bump, lambda c: glow(c, "front", 236, 760, 1.25)), "C 3.2: the headlights, the bump"),
              (_in_setup("C", c_cabin, lambda c: None), "3.4: the window down, the bills"),
              (cl.render(lambda k: cl.front(k, True), lambda c: cl.light_front(c, True)), "4.1: parked at the club, empty")]
    cols = 3
    W_, H_ = cols * 560 + 20, 70 + 2 * (960 + 50)
    sh = cairo.ImageSurface(cairo.FORMAT_RGB24, W_, H_); c = cairo.Context(sh)
    c.set_source_rgb(0.93, 0.92, 0.89); c.paint()
    c.set_source_rgb(0.1, 0.1, 0.1); c.select_font_face("Inter", 0, 1); c.set_font_size(26)
    c.move_to(20, 42); c.show_text("Office Noir 4: Dad's car, v2 (the turn and the cabin; dead zones in red)")
    for i, (s, lab) in enumerate(panels):
        x = 20 + (i % cols) * 560; y = 70 + (i // cols) * 1010
        c.set_source_surface(s, x, y); c.paint()
        if i:
            c.save(); c.translate(x, y); st.overlay(c); c.restore()
        c.set_source_rgb(0.1, 0.1, 0.1); c.select_font_face("Inter", 0, 1); c.set_font_size(18)
        c.move_to(x, y + 960 + 28); c.show_text(lab)
    sh.write_to_png(out)
    ph = cairo.ImageSurface(cairo.FORMAT_RGB24, 6 * 280 - 10, 480); c = cairo.Context(ph); c.set_source_rgb(1, 1, 1); c.paint()
    for i, (s, _) in enumerate(panels):
        c.save(); c.translate(i * 280, 0); c.scale(0.5, 0.5); c.set_source_surface(s, 0, 0); c.paint(); c.restore()
    ph.write_to_png(phone)
    return out


if __name__ == "__main__":
    print(sheet())
