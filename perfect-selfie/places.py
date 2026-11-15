"""Perfect Trip - the four places as flat, simple backgrounds in the series style (ink outlines, flat fills).
Each draws the whole 1080x1920 frame; the landmark sits in the upper-middle so characters stand in the lower half.
Ground line is at GY. f = frame (clouds drift). python3 places.py writes places_sheet.png."""
import os, sys, math, cairo
HERE = os.path.dirname(os.path.abspath(__file__)); PD = os.path.join(HERE, '..', 'perfect-date')
sys.path.insert(0, PD)
from kit import INK, WHITE, rr, fs, ell, hx, txt
W, H = 1080, 1920
GY = 1500                                                            # where feet stand

def sky(c, top, bottom):
    g = cairo.LinearGradient(0, 0, 0, GY); g.add_color_stop_rgb(0, *hx(top)); g.add_color_stop_rgb(1, *hx(bottom)); c.set_source(g); c.paint()
def clouds(c, f, pts=((160, 430, 70), (860, 560, 90), (560, 300, 55))):
    for x, y, r in pts:
        x = (x + f * .6) % 1300 - 110
        for dx, dy, k in ((-r, 10, .7), (0, 0, 1), (r, 12, .75)): ell(c, x + dx, y + dy, r * k, r * k * .8)
        c.set_source_rgb(*WHITE); c.fill()
def ground(c, col, col2=None, y=GY - 60):
    c.rectangle(0, y, W, H - y); c.set_source_rgb(*hx(col)); c.fill()
    c.move_to(0, y); c.line_to(W, y); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    if col2:
        for i in range(9): ell(c, 60 + i * 130, y + 160 + (i % 2) * 40, 70, 16); c.set_source_rgb(*hx(col2)); c.fill()
def tree(c, x, y, r):
    c.rectangle(x - 10, y, 20, r * 1.1); c.set_source_rgb(*hx('8a5a2e')); c.fill()
    ell(c, x, y, r, r); fs(c, hx('5cbf5e'), 6)

# ---------------- Pisa: the leaning tower on the lawn
def pisa(c, f=0):
    sky(c, '7fc8ff', 'e9f6ff'); clouds(c, f)
    ground(c, '7cc66a', '6ab55a')
    rr(c, -40, 1200, 300, 240, 10); fs(c, hx('f2ead6'), 6)                    # the cathedral's corner, low at the left
    for i in range(4): c.arc(30 + i * 60, 1300, 20, math.pi, 0); c.set_source_rgb(*hx('d8ccb0')); c.fill()
    ell(c, 660, GY - 52, 200, 26); c.set_source_rgba(0, 0, 0, .22); c.fill()             # contact shadow
    c.save(); c.translate(640, GY - 60); c.rotate(math.radians(8))          # it leans, as one rigid body
    w, h = 230, 960; n = 7; th = h / n
    rr(c, -w / 2, -h, w, h, 18); fs(c, hx('f6f0e0'), 6)                       # one cylinder
    g = cairo.LinearGradient(-w / 2, 0, w / 2, 0); g.add_color_stop_rgba(0, 0, 0, 0, .0); g.add_color_stop_rgba(.7, 0, 0, 0, .0); g.add_color_stop_rgba(1, 0, 0, 0, .14)
    rr(c, -w / 2, -h, w, h, 18); c.set_source(g); c.fill()                     # round shading on one side
    for i in range(n):
        y0 = -h + i * th
        if i: c.rectangle(-w / 2 - 8, y0 - 6, w + 16, 12); fs(c, hx('e9dfc6'), 4)  # gallery ledges
        for j in range(5):
            ax = -w / 2 + (j + .5) * w / 5
            c.move_to(ax - 11, y0 + th - 14); c.line_to(ax - 11, y0 + 34); c.arc(ax, y0 + 34, 11, math.pi, 0); c.line_to(ax + 11, y0 + th - 14)
            c.close_path(); c.set_source_rgb(*hx('cfc3a6')); c.fill()
    rr(c, -w * .4, -h - 76, w * .8, 82, 10); fs(c, hx('f6f0e0'), 5)           # the bell chamber
    for j in range(4):
        ax = -w * .4 + (j + .5) * w * .8 / 4; c.arc(ax, -h - 30, 9, math.pi, 0); c.line_to(ax + 9, -h - 6); c.line_to(ax - 9, -h - 6); c.close_path(); c.set_source_rgb(*hx('cfc3a6')); c.fill()
    c.restore()

# ---------------- Paris: the iron tower over the Champ de Mars (daylight only)
def paris(c, f=0):
    sky(c, '8fd0ff', 'f3f8ff'); clouds(c, f, ((180, 520, 70), (900, 380, 80)))
    ground(c, '86cf74', '74bd63')
    c.move_to(-20, GY + 300); c.line_to(420, GY - 60); c.line_to(660, GY - 60); c.line_to(1100, GY + 300); c.close_path(); c.set_source_rgb(*hx('e7d9b6')); c.fill()
    for i, r in enumerate((66, 52, 60, 44)): tree(c, 60 + i * 72, GY - 150 - i * 6, r); tree(c, 1020 - i * 72, GY - 150 - i * 6, (48, 64, 46, 56)[i])
    IRON, IRON_D = hx('9b7650'), hx('6f5236')
    cx, base = 540, GY - 70
    def leg(q):
        c.move_to(cx + q * 300, base); c.curve_to(cx + q * 230, base - 260, cx + q * 150, base - 420, cx + q * 110, base - 520)
        c.line_to(cx + q * 60, base - 520); c.curve_to(cx + q * 100, base - 400, cx + q * 150, base - 240, cx + q * 190, base)
        c.close_path(); fs(c, IRON, 6)
        for k in range(4):                                                    # a few X-braces, so the legs read as iron lattice
            t0, t1 = k / 4, (k + 1) / 4
            ox = lambda t: cx + q * (300 - 190 * t); ix = lambda t: cx + q * (190 - 130 * t); yy = lambda t: base - 520 * t
            for a_, b_ in (((ox(t0), yy(t0)), (ix(t1), yy(t1))), ((ix(t0), yy(t0)), (ox(t1), yy(t1)))):
                c.move_to(*a_); c.line_to(*b_); c.set_source_rgb(*IRON_D); c.set_line_width(5); c.stroke()
            c.move_to(ox(t1), yy(t1)); c.line_to(ix(t1), yy(t1)); c.stroke()
    leg(-1); leg(1)
    c.move_to(cx - 190, base); c.curve_to(cx - 120, base - 210, cx + 120, base - 210, cx + 190, base); c.set_source_rgb(*IRON_D); c.set_line_width(14); c.stroke()   # the arch
    rr(c, cx - 150, base - 540, 300, 34, 6); fs(c, IRON, 5)                    # first platform
    c.move_to(cx - 110, base - 506); c.line_to(cx - 50, base - 900); c.line_to(cx + 50, base - 900); c.line_to(cx + 110, base - 506); c.close_path(); fs(c, IRON, 6)
    for k in range(5): y = base - 540 - k * 75; c.move_to(cx - 100 + k * 11, y); c.line_to(cx + 100 - k * 11, y - 75); c.set_source_rgb(*IRON_D); c.set_line_width(3); c.stroke()
    rr(c, cx - 80, base - 920, 160, 26, 5); fs(c, IRON, 5)                     # second platform
    c.move_to(cx - 44, base - 896); c.line_to(cx - 8, base - 1290); c.line_to(cx + 8, base - 1290); c.line_to(cx + 44, base - 896); c.close_path(); fs(c, IRON, 5)
    rr(c, cx - 22, base - 1310, 44, 24, 5); fs(c, IRON, 4)
    c.move_to(cx, base - 1310); c.line_to(cx, base - 1370); c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()

# ---------------- Egypt: three pyramids in the dunes
def egypt(c, f=0):
    sky(c, 'ffd27a', 'fff3d6')
    ell(c, 840, 520, 90, 90); c.set_source_rgb(*hx('fff7c2')); c.fill()
    for x, base_w, hgt in ((230, 330, 280), (880, 260, 210), (560, 660, 620)):   # the big one last, in front; the side ones smaller
        bx, by = x, GY - 40
        side = base_w < 600
        c.move_to(bx - base_w / 2, by); c.line_to(bx, by - hgt); c.line_to(bx + base_w / 2, by); c.close_path(); fs(c, hx('f0d49a') if side else hx('e8c27a'), 6)
        c.move_to(bx, by - hgt); c.line_to(bx + base_w / 2, by); c.line_to(bx + base_w * .12, by); c.close_path(); c.set_source_rgb(*hx('c99c55')); c.fill()
        c.move_to(bx - base_w / 2, by); c.line_to(bx, by - hgt); c.line_to(bx + base_w / 2, by); c.close_path(); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
        for k in range(1, 6): t = k / 6; y = by - hgt * t; c.move_to(bx - base_w / 2 * (1 - t), y); c.line_to(bx - base_w * .02 * (1 - t), y); c.set_source_rgb(*hx('d4ab66')); c.set_line_width(3); c.stroke()
    c.rectangle(0, GY - 40, W, H); c.set_source_rgb(*hx('f2d394')); c.fill()
    for i, (x, y, r) in enumerate(((150, GY + 60, 260), (820, GY + 40, 300), (500, GY + 260, 380))):   # dunes
        ell(c, x, y + r * .5, r * 1.6, r * .5); fs(c, hx('efc985') if i % 2 else hx('f6dba0'), 5)

# ---------------- Rome: the Colosseum, its broken top stepping down to one side
def rome(c, f=0, s=1.0, cx=540):
    """s, cx: the Colosseum's size and centre on the horizon (s < 1: further away, e.g. small enough to pinch)."""
    sky(c, '86c9ff', 'd6eeff'); clouds(c, f, ((150, 400, 60), (920, 520, 75)))
    ST, ST_D, ST_L = hx('e2c896'), hx('b99a66'), hx('efdcb4')
    left, right, top, base = 70, 1010, 760, GY - 60
    tiers = 4; th = (base - top) / tiers
    bow = 70                                                                  # the facade curves away: edges higher in the middle
    cy = lambda x: -bow * (1 - ((x - 540) / 470) ** 2)                       # 0 at the ends, -bow in the middle
    edge = [(70, 0), (300, -14), (520, -6), (600, 70), (640, 50), (720, 170), (800, 210), (860, 300), (930, 320), (1010, 430)]   # the broken top
    def outline():
        c.move_to(left, base); c.line_to(left, top + 40 + cy(left))
        for x, dy in edge: c.line_to(x, top + 40 + cy(x) + dy)
        c.line_to(right, base + 0); c.close_path()
    c.save(); c.translate(cx, base); c.scale(s, s); c.translate(-540, -base)          # the Colosseum's own frame
    c.save(); outline(); c.clip_preserve(); fs(c, ST, 7 / s)
    for t in range(tiers):
        y0 = top + t * th
        c.move_to(left, y0 + th - 16 + cy(left))
        for x in range(left, right + 1, 20): c.line_to(x, y0 + th - 16 + cy(x) * (1 - t / tiers))
        c.set_source_rgb(*ST_D); c.set_line_width(16); c.stroke()            # curved cornices
        if t == 0: continue
        for j in range(10):
            ax = left + 40 + j * (right - left - 80) / 9.5; yo = cy(ax) * (1 - t / tiers)
            w_ = 24 * (1 - .35 * abs(ax - 540) / 470)                         # arches narrow towards the ends: the curve
            c.move_to(ax - w_, y0 + th - 16 + yo); c.line_to(ax - w_, y0 + 46 + yo); c.arc(ax, y0 + 46 + yo, w_, math.pi, 0); c.line_to(ax + w_, y0 + th - 16 + yo); c.close_path()
            c.set_source_rgb(*hx('6e5638')); c.fill()
    c.restore()
    outline(); c.set_source_rgb(*INK); c.set_line_width(7 / s); c.stroke(); c.restore()
    c.rectangle(0, base, W, H - base); c.set_source_rgb(*hx('d9cdb3')); c.fill()
    c.move_to(0, base); c.line_to(W, base); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    for i in range(40): rr(c, (i * 137) % 1080, base + 40 + (i * 53) % 380, 60, 26, 10); c.set_source_rgb(*hx('cbbd9f')); c.fill()

PLACES = dict(pisa=pisa, paris=paris, giza=egypt, rome=rome)
STAMP = dict(pisa=('PISA', 'c8323c', -.18, 220), paris=('PARIS', '2f5fb3', .14, 870), giza=('GIZA', 'b5651d', -.1, 240), rome=('ROMA', '7b3fa0', .2, 870))   # name, ink, tilt, x (kept off the landmark)

def stamp(c, place, x=None, y=500, k=1.0, op=.85):
    """A small passport stamp naming the place, in the photo's top-right corner (clear of the title bar and the app's buttons).
    k animates it in (0..1: it thumps down from a bit bigger)."""
    if k <= 0: return
    name, col, rot, x0 = STAMP[place]; col = hx(col); x = x0 if x is None else x
    sc = 1 + .5 * (1 - k)
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(sc, sc)
    c.set_source_rgba(*col, op * k)
    rr(c, -130, -62, 260, 124, 26); c.set_line_width(9); c.stroke()
    rr(c, -114, -46, 228, 92, 18); c.set_line_width(3); c.stroke()
    for q in (-1, 1):                                                        # the little stars of a stamp
        cx = q * 92; c.move_to(cx, -14)
        for j in range(1, 10): rd = 12 if j % 2 == 0 else 5; c.line_to(cx + rd * math.sin(j * math.pi / 5), -14 + rd * -math.cos(j * math.pi / 5) + 14 - 14)
        c.close_path(); c.fill()
    c.select_font_face('Lilita One'); c.set_font_size(58); e = c.text_extents(name)
    c.move_to(-e.width / 2 - e.x_bearing, 20); c.show_text(name)
    c.restore()

if __name__ == '__main__':
    from PIL import Image
    ims = []
    for name, fn in PLACES.items():
        S = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(S); fn(c, 0)
        stamp(c, name)
        p = os.path.join(HERE, f'_{name}.png'); S.write_to_png(p); ims.append(Image.open(p).convert('RGB').resize((540, 960))); os.remove(p)
    sheet = Image.new('RGB', (540 * 4 + 60, 960 + 40), 'white')
    for i, im in enumerate(ims): sheet.paste(im, (20 + i * 555, 20))
    sheet.save(os.path.join(HERE, 'places_sheet.png')); print('places_sheet.png')
