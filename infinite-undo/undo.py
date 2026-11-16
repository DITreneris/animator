"""ME + MY AI - Infinite Undo: the set and the pieces.
Hoody's desk at home; the glass and the water arc; the cat on the desk; MY AI's UNDO disc, its counter, the rewind marks.
The rule, written once: Hoody, the glass and the water are drawn from a story time that the button can run backwards;
MY AI and the cat are drawn from the real frame number."""
import os, sys, math, cairo
HERE = os.path.dirname(os.path.abspath(__file__)); PD = os.path.join(HERE, '..', 'perfect-date')
sys.path.insert(0, PD); sys.path.insert(0, os.path.join(PD, 'characters'))
import importlib.util                   # Perfect Date's render.py under its own name
_spec = importlib.util.spec_from_file_location('pd_render', os.path.join(PD, 'render.py')); R = importlib.util.module_from_spec(_spec)
sys.modules['pd_render'] = R; _spec.loader.exec_module(R)
import kit as K, chars as Sh, myai as A
from kit import INK, WHITE, NAVY, YEL, TABBY, TABBY_D, CREAM, rr, fs, ell, limb, txt, hx, lerp, cl
W, H = 1080, 1920

CYAN = hx('22d3ff'); WATER = hx('8fd6ff'); WATER_D = hx('4fb3ea'); GLASS = (.86, .94, 1.0)
WALL0, WALL1 = hx('f6e7cf'), hx('ecd3ad'); WOOD = hx('c98a4e'); WOOD_D = hx('a5683a'); WOOD_DD = hx('7d4a26')
DESK = 1250                              # the desk top's y

def room(c):
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, *WALL0); g.add_color_stop_rgb(1, *WALL1); c.set_source(g); c.paint()
    rr(c, 80, 430, 360, 400, 18); fs(c, WHITE, 8)                                         # the window
    g = cairo.LinearGradient(0, 440, 0, 820); g.add_color_stop_rgb(0, *hx('7cc4ff')); g.add_color_stop_rgb(1, *hx('d6eeff'))
    rr(c, 96, 446, 328, 368, 10); c.set_source(g); c.fill()
    for (x, y, r) in ((180, 560, 40), (230, 548, 52), (290, 566, 36)): ell(c, x, y, r, r * .8); c.set_source_rgb(*WHITE); c.fill()
    c.move_to(260, 446); c.line_to(260, 814); c.move_to(96, 630); c.line_to(424, 630); c.set_source_rgb(*WHITE); c.set_line_width(12); c.stroke()
    rr(c, 600, 470, 200, 150, 10); fs(c, hx('ffd46b'), 7)                                 # a picture: a small sun over hills
    ell(c, 700, 600, 90, 40); c.set_source_rgb(*hx('6cc070')); c.fill(); ell(c, 650, 520, 22, 22); c.set_source_rgb(*hx('ff9f43')); c.fill()

def desk_top(c):
    rr(c, 30, DESK, 1020, 36, 10); fs(c, WOOD, 7)

def desk_front(c):
    rr(c, 60, DESK + 30, 960, 400, 8); fs(c, WOOD_D, 7)
    for y in (DESK + 90, DESK + 230): rr(c, 640, y, 300, 110, 10); fs(c, WOOD, 5); rr(c, 760, y + 46, 60, 16, 8); fs(c, WOOD_DD, 4)
    desk_top(c)

def laptop(c, x, y, s=1.0):
    """On the desk, lid open towards Hoody: we see the back of the lid and the base's edge."""
    c.save(); c.translate(x, y); c.scale(s, s)
    rr(c, -96, -14, 192, 14, 5); fs(c, hx('8f97a6'), 5)
    c.save(); c.translate(0, -12); c.rotate(-.08); rr(c, -84, -128, 168, 128, 12); fs(c, hx('c3c9d4'), 6)
    ell(c, 0, -66, 16, 16); c.set_source_rgb(*hx('aab1be')); c.fill(); c.restore()
    c.restore()

def glass(c, x, y, tip=0.0, fill=.8):
    """Pivot at the base's right corner (x, y). tip 0 upright .. 1.2 lying. Returns the rim's lip point (where water leaves)."""
    a = tip; gw, gh = 70, 120
    c.save(); c.translate(x, y); c.rotate(a)
    c.move_to(-gw, 0); c.line_to(-gw - 8, -gh); c.line_to(8, -gh); c.line_to(0, 0); c.close_path()
    c.set_source_rgba(*GLASS, .75); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    if fill > .02:                                        # the water stays level with the world while the glass tips
        c.save(); c.move_to(-gw, 0); c.line_to(-gw - 8, -gh); c.line_to(8, -gh); c.line_to(0, 0); c.close_path(); c.clip()
        c.rotate(-a); lvl = -gh * fill * math.cos(a) * .9
        c.rectangle(-300, lvl, 600, 400); c.set_source_rgba(*WATER, .9); c.fill(); c.restore()
    c.move_to(-gw + 14, -16); c.line_to(-gw + 6, -gh + 16); c.set_source_rgba(1, 1, 1, .8); c.set_line_width(7); c.stroke()
    c.restore()
    return (x + math.cos(a) * 8 + math.sin(a) * gh, y + math.sin(a) * 8 - math.cos(a) * gh)

def arc_pts(p0, p1, peak, n=40):
    """A quadratic arc from p0 to p1 whose top is at height peak."""
    cx = (p0[0] + p1[0]) / 2; cy = 2 * peak - (p0[1] + p1[1]) / 2
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * cx + t * t * p1[0], (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * cy + t * t * p1[1]) for t in (i / n for i in range(n + 1))]

def water(c, pts, f, rewind=0.0, pulse=0.0, w=34):
    """The stream as one smooth tube, flared at the lip; bulges travel along it (pulse) and droplets fly off both ways.
    rewind 0..1 rims it in cyan."""
    def path():
        c.move_to(*pts[0])
        for p in pts[1:]: c.line_to(*p)
    c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND)
    n = len(pts) - 1
    bulges = [(pts[i], 1 + .14 * math.sin(i * .9 - f * .8) * pulse) for i in range(4, n - 1, 6)]
    layers = ([(CYAN, w + 34)] if rewind > 0 else []) + [(INK, w + 12), (WATER, w)]
    for col, lw in layers:
        path(); c.set_source_rgb(*col); c.set_line_width(lw); c.stroke()
        ell(c, pts[0][0], pts[0][1], (lw + 14) / 2, (lw + 14) / 2.6); c.set_source_rgb(*col); c.fill()          # the flare at the lip
        for (px, py), k in bulges: ell(c, px, py, lw / 2 * k, lw / 2 * k); c.set_source_rgb(*col); c.fill()
    for i in range(3, n - 3, 4):                                            # a highlight running along it
        a, b = pts[i], pts[i + 1]; c.move_to(a[0] - 5, a[1] - 7); c.line_to(b[0] - 5, b[1] - 7)
        c.set_source_rgba(1, 1, 1, .85); c.set_line_width(6); c.stroke()
    for k in range(10):                                                     # droplets, flying both ways
        t = (k * .113 + f * .02 * (1 if k % 2 else -1)) % 1; i = min(n, int(t * n)); px, py = pts[i]
        ox = math.sin(k * 2.1) * 46; oy = math.cos(k * 1.7) * 34 - 6
        ell(c, px + ox, py + oy, 7 + k % 3 * 2, 9 + k % 3 * 2); fs(c, WATER, 3)

def chevrons(c, x, y, s=1.0, n=2, op=1.0, ang=0.0):
    """Rewind marks: «« pointing back the way things came."""
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    for i in range(n):
        dx = i * 30
        c.move_to(dx + 22, -26); c.line_to(dx - 4, 0); c.line_to(dx + 22, 26)
        c.set_source_rgba(*INK, op); c.set_line_width(20); c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke_preserve()
        c.set_source_rgba(*CYAN, op); c.set_line_width(11); c.stroke()
    c.restore()

def cyan_rim(c, draw, width=10, op=.85):
    """Draw something with a cyan outline glow: its silhouette offset in a ring, under it."""
    c.push_group(); draw(c); pat = c.pop_group()
    for k in range(12):
        a = k * math.pi / 6; c.save(); c.translate(math.cos(a) * width, math.sin(a) * width)
        c.set_source_rgba(*CYAN, op); c.mask(pat); c.restore()
    c.set_source(pat); c.paint()

def ghost(c, draw, dx, op=.3):
    """A cyan after-image of where something was, a moment ago (the rewind's trail)."""
    c.push_group(); draw(c); pat = c.pop_group()
    c.save(); c.translate(dx, 0); c.set_source_rgba(*CYAN, op); c.mask(pat); c.restore()

def undo_disc(c, x, gy, s, glow=0.0, press=0.0):
    """MY AI's chest disc as the UNDO button (drawn over its chest). glow 0..1: lit cyan; press flashes it white."""
    cx, cy = x, gy - 130 * s; r = 46 * s
    if glow > 0:
        for k in range(5): ell(c, cx, cy, r + 10 + k * 9 * glow, r + 10 + k * 9 * glow); c.set_source_rgba(*CYAN, .12 * glow); c.fill()
    ell(c, cx, cy, r, r); fs(c, (lerp(.82, CYAN[0], glow), lerp(.86, CYAN[1], glow), lerp(.93, CYAN[2], glow)), 6)
    if press > 0: ell(c, cx, cy, r * .9, r * .9); c.set_source_rgba(1, 1, 1, .8 * press); c.fill()
    c.save(); c.translate(cx, cy + 2); c.scale(s, s)
    c.move_to(-8, -14); c.line_to(-22, -2); c.line_to(-8, 10); c.set_source_rgb(*NAVY); c.set_line_width(6); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
    c.restore()
    txt(c, 'UNDO', cx, cy + 16 * s, 22 * s, NAVY, lw=0)
    return cx, cy, r

def counter(c, x, y, n, k=1.0, check=True):
    """MY AI's pride: UNDO ×n ✓ on a small chip."""
    s_ = f'UNDO ×{n}'
    c.save(); c.translate(x, y); c.scale(k, k)
    c.select_font_face('Lilita One'); c.set_font_size(40); w = c.text_extents(s_).width + (90 if check else 44)
    rr(c, -w / 2, -34, w, 68, 34); fs(c, NAVY, 6)
    txt(c, s_, -w / 2 + 22, 0, 40, CYAN, lw=0, align='l')
    if check:
        c.move_to(w / 2 - 54, 0); c.line_to(w / 2 - 42, 12); c.line_to(w / 2 - 20, -14)
        c.set_source_rgb(*hx('3ee07a')); c.set_line_width(9); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
    c.restore()

def cat(c, x, y, s, f=0, face=-1, look_back=False, head_up=0.0, lap=0.0, eyes='content', lids=.55, look=0,
        paw_to=None, tail_to=None, ears_up=False):
    """The cat on the desk. face -1: body towards the glass (left), +1: towards MY AI (right). look_back turns the head
    over the shoulder. eyes: content (half lids), track (alert, pupils shifted by look), wide (ears-up surprise).
    paw_to / tail_to: screen points the front paw or the tail tip rests on (the button). lap 0..1: the tongue.
    Returns the tongue tip (or mouth) in screen coordinates."""
    c.save(); c.translate(x, y); c.scale(face * s, s)                        # drawn facing +x
    loc = lambda p: ((p[0] - x) / (face * s), (p[1] - y) / s)
    if tail_to is not None:
        tx, ty = loc(tail_to); c.move_to(-100, -70); c.curve_to(-170, -90, tx - 30, ty + 70, tx, ty)
    else:
        tw = math.sin(f * .15) * 10; c.move_to(-100, -70); c.curve_to(-150, -110, -150 + tw, -180, -120 + tw, -200)
    c.set_source_rgb(*INK); c.set_line_width(28); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke_preserve(); c.set_source_rgb(*TABBY); c.set_line_width(16); c.stroke()
    for lx in ((-70, -40, 50) if paw_to is not None else (-70, -40, 50, 80)):
        limb(c, [(lx, -50), (lx, 0)], 20, TABBY); ell(c, lx, 0, 16, 10); fs(c, TABBY, 5)
    ell(c, 0, -76, 108, 40); fs(c, TABBY)
    for i in range(4): c.arc(-60 + i * 36, -100, 24, math.pi * 1.2, math.pi * 1.8); c.set_source_rgb(*TABBY_D); c.set_line_width(8); c.stroke()
    if paw_to is not None:
        px, py = loc(paw_to)
        limb(c, [(80, -60), ((80 + px) / 2 + 8, (py - 60) / 2 - 16), (px - 8, py)], 20, TABBY)
        ell(c, px - 4, py, 17, 13); fs(c, TABBY, 5)
    hx_, hy = (70, -150) if look_back else (110, -116)
    c.save(); c.translate(hx_, hy)
    if look_back: c.scale(-1, 1)                                               # the head turned over the shoulder
    c.rotate(-head_up)
    if ears_up: c.translate(0, -8)
    K._cat_head(c, 0, 0, 1.0, False, 'sleep', 0)
    for q in (-1, 1):
        ex, ey = q * 24 + 6, -4
        ell(c, ex, ey, 14, 16); c.set_source_rgb(*TABBY); c.fill()
        big = eyes == 'wide'
        ell(c, ex, ey + 1, 12 if big else 10, 14 if big else 11); fs(c, hx('b8e04a'), 3)
        ell(c, ex + 2 + look, ey + 1, 3 if big else 3.5, 9); c.set_source_rgb(*INK); c.fill()
        lid = {'content': lids, 'track': .18, 'wide': 0}[eyes]
        if lid > 0:
            c.rectangle(ex - 14, ey - 16, 28, 16 * lid + 4); c.set_source_rgb(*TABBY); c.fill()
            c.move_to(ex - 12, ey - 12 + 16 * lid); c.line_to(ex + 12, ey - 12 + 16 * lid); c.set_source_rgb(*INK); c.set_line_width(4); c.stroke()
    mx, my = 44, 30
    if lap > 0:
        c.move_to(mx - 8, my - 6); c.curve_to(mx + 14 * lap, my - 6 - 20 * lap, mx + 36 * lap, my - 28 * lap, mx + 42 * lap, my - 42 * lap)
        c.set_source_rgb(*INK); c.set_line_width(17); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke_preserve()
        c.set_source_rgb(*hx('ff8fa6')); c.set_line_width(10); c.stroke()
    c.restore(); c.restore()
    hd = -1 if look_back else 1
    ca, sa = math.cos(-head_up), math.sin(-head_up)
    tx_, ty_ = mx + 42 * lap, my - 42 * lap
    lx, ly = hx_ + hd * (ca * tx_ - sa * ty_), hy + sa * tx_ + ca * ty_
    return (x + face * s * lx, y + s * ly)

def cat_drink(c, x, y, s, f, lap=0.0, tail_to=None, head_up=.45, lids=.55):
    return cat(c, x, y, s, f, face=-1, head_up=head_up, lap=lap, lids=lids, tail_to=tail_to)

def phone(c, x, y, s=1.0, rot=0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    rr(c, -24, -44, 48, 88, 10); fs(c, hx('2a2f3d'), 5); rr(c, -17, -34, 34, 62, 5); c.set_source_rgb(*hx('7fd0ff')); c.fill()
    c.restore()

def thumb_up(c, x, gy, s):
    """MY AI's screen-left arm raised in a thumbs-up (myai drawn with that arm None)."""
    c.save(); c.translate(x, gy - 280 * s); c.scale(s, s)
    hx_, hy = A.arm(c, -1, (70, 100))
    rr(c, hx_ - 8, hy - 50, 16, 34, 8); fs(c, WHITE, 5)
    c.restore()
