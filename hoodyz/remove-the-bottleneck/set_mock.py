"""Remove the Bottleneck: background study. Three sets, the same frame 0 on each (Hoody points at the board,
MY AI beside him), so the backgrounds compare like for like. -> set_mock.png"""
import os, sys, math, cairo
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import office as P
from office import K, A, INK, WHITE, NAVY, YEL, RED, GREY, GREEN, rr, fs, ell, limb, txt, hx, lerp, W, H, FLOOR, HS, AS
WOOD = hx('c9955b'); PLY = hx('e3c08a'); PLY_D = hx('b98d52')

def crate(c, x, gy, w=330, h=430, lid=1.0, label=True):
    """The plant: a plywood shipping crate, open, lid up; 'AI AUTOMATION', arrows up, hazard stripes."""
    x0, y0 = x - w / 2, gy - h
    c.save(); c.translate(x0 + w, y0); c.rotate(-1.25 * lid); rr(c, -w - 10, -24, w + 20, 30, 6); fs(c, PLY_D, 6); c.restore()   # the lid, hinged at the back right
    rr(c, x0, y0, w, h, 6); fs(c, PLY, 7)
    for yy in (y0 + 30, gy - 30): c.rectangle(x0, yy - 12, w, 24); c.set_source_rgb(*PLY_D); c.fill()
    c.move_to(x0, y0 + 30); c.line_to(x0 + w, gy - 30); c.set_source_rgb(*PLY_D); c.set_line_width(18); c.stroke()
    rr(c, x0, y0, w, h, 6); c.set_source_rgb(*INK); c.set_line_width(7); c.stroke()
    if label:
        rr(c, x - 130, y0 + 120, 260, 120, 8); fs(c, WHITE, 5)
        txt(c, 'AI', x, y0 + 158, 46, INK, lw=0); txt(c, 'AUTOMATION', x, y0 + 206, 40, INK, lw=0)
        for i in range(5): c.move_to(x - 110 + i * 46, gy - 50); c.line_to(x - 80 + i * 46, gy - 80); c.set_source_rgb(*INK); c.set_line_width(14); c.stroke()
        for dx in (-30, 0): c.move_to(x0 + 50 + dx, y0 + 300); c.line_to(x0 + 50 + dx, y0 + 260); c.move_to(x0 + 40 + dx, y0 + 272); c.line_to(x0 + 50 + dx, y0 + 258); c.line_to(x0 + 60 + dx, y0 + 272)
        c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()

def board_bottleneck(c, x, y, w=420, h=300):
    """The planted diagram: TASKS pour in wide, squeeze through one narrow neck - a little Hoody, circled red - and out."""
    rr(c, x, y, w, h, 10); fs(c, WHITE, 7)
    txt(c, 'PIPELINE', x + w / 2, y + 36, 34, NAVY, lw=0)
    cx, cy = x + w / 2, y + 170
    c.move_to(x + 30, cy - 80); c.line_to(cx - 40, cy - 22); c.line_to(cx + 40, cy - 22); c.line_to(x + w - 30, cy - 80)
    c.move_to(x + 30, cy + 80); c.line_to(cx - 40, cy + 22); c.line_to(cx + 40, cy + 22); c.line_to(x + w - 30, cy + 80)
    c.set_source_rgb(*NAVY); c.set_line_width(7); c.stroke()
    for i in range(4): rr(c, x + 40 + i * 18, cy - 40 + (i % 2) * 30, 22, 16, 3); fs(c, hx('8fd6ff'), 3)
    ell(c, cx, cy, 20, 20); fs(c, hx('3a2a22'), 3); ell(c, cx, cy + 4, 13, 12); fs(c, hx('ffd9b8'), 3)   # tiny Hoody, stuck in the neck
    ell(c, cx, cy, 44, 44); c.set_source_rgb(*RED); c.set_line_width(7); c.stroke()
    txt(c, '!!', cx + 64, cy - 48, 40, RED, lw=0)

def office_v1(c):                                                      # A: Just One Line's office as it is
    P.room(c); P.desk(c); P.laptop(c); c.save(); c.translate(690, P.DESK_Y); P.mug(c, 0, 0, 1.0); c.restore()
def office_v2(c):                                                      # B: its own office: a darker wall, the board, the crate
    c.rectangle(0, 0, W, FLOOR); g = cairo.LinearGradient(0, 0, 0, FLOOR); g.add_color_stop_rgb(0, *hx('4f6f7a')); g.add_color_stop_rgb(1, *hx('3c5862')); c.set_source(g); c.fill()
    c.rectangle(0, FLOOR, W, H - FLOOR); c.set_source_rgb(*hx('8a6a4a')); c.fill()
    for i in range(0, W, 120): c.move_to(i, FLOOR); c.line_to(i - 60, H); c.set_source_rgba(0, 0, 0, .12); c.set_line_width(4); c.stroke()
    c.rectangle(0, FLOOR - 40, W, 40); c.set_source_rgb(*hx('2e4650')); c.fill()                     # skirting
    board_bottleneck(c, 560, 560)
    crate(c, 870, FLOOR, 300, 420)
def dock(c):                                                           # C: a loading bay: roller door, SHIPPING, pallets
    c.rectangle(0, 0, W, FLOOR); c.set_source_rgb(*hx('6b6f78')); c.fill()
    rr(c, 520, 520, 520, 1040, 8); fs(c, hx('9aa0aa'), 7)
    for y in range(560, 1560, 46): c.move_to(524, y); c.line_to(1036, y); c.set_source_rgb(*hx('7d838c')); c.set_line_width(6); c.stroke()
    rr(c, 640, 450, 300, 70, 8); fs(c, YEL, 6); txt(c, 'SHIPPING', 790, 486, 44, INK, lw=0)
    c.rectangle(0, FLOOR, W, H - FLOOR); c.set_source_rgb(*hx('7a7a72')); c.fill()
    for i in range(6): c.rectangle(i * 200, FLOOR + 30, 120, 18); c.set_source_rgb(*YEL); c.fill()
    crate(c, 870, FLOOR, 300, 420)

def frame0(c, bg, name):
    bg(c)
    x, gy = 360, FLOOR
    shL, shR, head = P.hoody_standing(c, x, gy, 'smug', side=1)
    P.hoody_arm(c, shR, (shR[0] + 230, shR[1] - 150), HS, pref=P.DOWN, hand='point', ang=-.5)
    P.hoody_arm(c, shL, (shL[0] - 40, shL[1] + 170), HS, pref=P.LEFT, hand='grip')
    ax = 150; A.myai(c, ax, FLOOR, AS, eye='happy', look=(14, -10))
    P.bubble(c, ['REMOVE THE', 'BOTTLENECK.'], 64, (head[0] + 60, head[1] - 200), 560, 520)
    P.topbar(c)

if __name__ == '__main__':
    sets = [(office_v1, 'A: the Just One Line office'), (office_v2, 'B: its own office: board + crate'), (dock, 'C: the loading bay')]
    sw, sh = 432, 768
    out = cairo.ImageSurface(cairo.FORMAT_RGB24, sw * 3 + 40, sh + 70); c = cairo.Context(out); c.set_source_rgb(1, 1, 1); c.paint()
    for i, (bg, name) in enumerate(sets):
        S = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); frame0(cairo.Context(S), bg, name)
        c.save(); c.translate(10 + i * (sw + 10), 60); c.scale(.4, .4); c.set_source_surface(S); c.paint(); c.restore()
        txt(c, name, 10 + i * (sw + 10) + sw / 2, 30, 24, NAVY, lw=0)
    out.write_to_png(os.path.join(HERE, 'set_mock.png')); print('ok')
