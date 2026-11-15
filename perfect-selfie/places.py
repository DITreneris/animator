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
    c.save(); c.translate(640, GY - 60); c.rotate(math.radians(5))          # it leans
    w, h = 230, 960
    for i in range(7):                                                       # seven arcaded tiers, the bell chamber narrower
        y0 = -h + i * (h / 7.3); ww = w * (.86 if i == 0 else 1)
        rr(c, -ww / 2, y0 + 8, ww, h / 7.3 - 4, 8); fs(c, hx('f6f0e0'), 5)
        n = 5 if i else 4
        for j in range(n):
            ax = -ww / 2 + (j + .5) * ww / n
            c.move_to(ax - 12, y0 + h / 7.3 - 6); c.line_to(ax - 12, y0 + 40); c.arc(ax, y0 + 40, 12, math.pi, 0); c.line_to(ax + 12, y0 + h / 7.3 - 6)
            c.close_path(); c.set_source_rgb(*hx('cfc3a6')); c.fill()
    rr(c, -w * .43, -h - 70, w * .86, 80, 8); fs(c, hx('f6f0e0'), 5)
    c.restore()

# ---------------- Paris: the iron tower over the Champ de Mars (daylight only)
def paris(c, f=0):
    sky(c, '8fd0ff', 'f3f8ff'); clouds(c, f, ((180, 520, 70), (900, 380, 80)))
    ground(c, '86cf74', '74bd63')
    c.move_to(-20, GY + 300); c.line_to(420, GY - 60); c.line_to(660, GY - 60); c.line_to(1100, GY + 300); c.close_path(); c.set_source_rgb(*hx('e7d9b6')); c.fill()
    for i in range(4): tree(c, 60 + i * 70, GY - 150 - i * 6, 60 - i * 6); tree(c, 1020 - i * 70, GY - 150 - i * 6, 60 - i * 6)
    IRON, IRON_D = hx('9b7650'), hx('6f5236')
    cx, base = 540, GY - 70
    def leg(q):
        c.move_to(cx + q * 300, base); c.curve_to(cx + q * 230, base - 260, cx + q * 150, base - 420, cx + q * 110, base - 520)
        c.line_to(cx + q * 60, base - 520); c.curve_to(cx + q * 100, base - 400, cx + q * 150, base - 240, cx + q * 190, base)
        c.close_path(); fs(c, IRON, 6)
        for k in range(6):                                                    # lattice
            t = k / 6; y = base - 520 * t
            c.move_to(cx + q * (300 - 190 * t), y); c.line_to(cx + q * (190 - 130 * (t + 1 / 6)), y - 87); c.set_source_rgb(*IRON_D); c.set_line_width(3); c.stroke()
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
    for x, base_w, hgt in ((250, 380, 330), (870, 300, 250), (560, 640, 600)):   # the big one last, in front
        bx, by = x, GY - 40
        c.move_to(bx - base_w / 2, by); c.line_to(bx, by - hgt); c.line_to(bx + base_w / 2, by); c.close_path(); fs(c, hx('e8c27a'), 6)
        c.move_to(bx, by - hgt); c.line_to(bx + base_w / 2, by); c.line_to(bx + base_w * .12, by); c.close_path(); c.set_source_rgb(*hx('c99c55')); c.fill()
        c.move_to(bx - base_w / 2, by); c.line_to(bx, by - hgt); c.line_to(bx + base_w / 2, by); c.close_path(); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
        for k in range(1, 6): t = k / 6; y = by - hgt * t; c.move_to(bx - base_w / 2 * (1 - t), y); c.line_to(bx - base_w * .02 * (1 - t), y); c.set_source_rgb(*hx('d4ab66')); c.set_line_width(3); c.stroke()
    c.rectangle(0, GY - 40, W, H); c.set_source_rgb(*hx('f2d394')); c.fill()
    for i, (x, y, r) in enumerate(((150, GY + 60, 260), (820, GY + 40, 300), (500, GY + 260, 380))):   # dunes
        ell(c, x, y + r * .5, r * 1.6, r * .5); fs(c, hx('efc985') if i % 2 else hx('f6dba0'), 5)

# ---------------- Rome: the Colosseum, its broken top stepping down to one side
def rome(c, f=0):
    sky(c, '86c9ff', 'f6f1e6'); clouds(c, f, ((150, 400, 60), (920, 520, 75)))
    ST, ST_D, ST_L = hx('e2c896'), hx('b99a66'), hx('efdcb4')
    left, right, top, base = 90, 990, 760, GY - 60
    tiers = 4; th = (base - top) / tiers
    c.save()
    c.move_to(left, base); c.line_to(left, top + 40); c.line_to(560, top - 10); c.line_to(700, top + th * .9)       # the broken top: full at the left, stepping down to the right
    c.line_to(840, top + th * 1.6); c.line_to(right, top + th * 2.1); c.line_to(right, base); c.close_path(); c.clip_preserve(); fs(c, ST, 7)
    for t in range(tiers):
        y0 = top + t * th
        c.rectangle(left, y0 + th - 16, right - left, 16); c.set_source_rgb(*ST_D); c.fill()                       # cornices
        if t == 0: continue                                                                                         # the attic has small windows
        for j in range(9):
            ax = left + 40 + j * (right - left - 80) / 8.5
            c.move_to(ax - 26, y0 + th - 16); c.line_to(ax - 26, y0 + 46); c.arc(ax, y0 + 46, 26, math.pi, 0); c.line_to(ax + 26, y0 + th - 16); c.close_path()
            c.set_source_rgb(*hx('6e5638')); c.fill()
            c.rectangle(ax + 34, y0 + 14, 14, th - 32); c.set_source_rgb(*ST_L); c.fill()                         # half-columns
    for j in range(12): c.rectangle(left + 30 + j * 76, top + 30, 24, 30); c.set_source_rgb(*ST_D); c.fill()
    c.restore()
    c.move_to(left, base); c.line_to(left, top + 40); c.line_to(560, top - 10); c.line_to(700, top + th * .9); c.line_to(840, top + th * 1.6); c.line_to(right, top + th * 2.1); c.line_to(right, base)
    c.set_source_rgb(*INK); c.set_line_width(7); c.stroke()
    c.rectangle(0, base, W, H - base); c.set_source_rgb(*hx('d9cdb3')); c.fill()                                    # the cobbled square
    c.move_to(0, base); c.line_to(W, base); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    for i in range(40): rr(c, (i * 137) % 1080, base + 40 + (i * 53) % 380, 60, 26, 10); c.set_source_rgb(*hx('cbbd9f')); c.fill()

PLACES = dict(pisa=pisa, paris=paris, egypt=egypt, rome=rome)

if __name__ == '__main__':
    from PIL import Image
    ims = []
    for name, fn in PLACES.items():
        S = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(S); fn(c, 0)
        txt(c, name.upper(), 540, 1820, 64, WHITE, lw=8)
        p = os.path.join(HERE, f'_{name}.png'); S.write_to_png(p); ims.append(Image.open(p).convert('RGB').resize((540, 960))); os.remove(p)
    sheet = Image.new('RGB', (540 * 4 + 60, 960 + 40), 'white')
    for i, im in enumerate(ims): sheet.paste(im, (20 + i * 555, 20))
    sheet.save(os.path.join(HERE, 'places_sheet.png')); print('places_sheet.png')
