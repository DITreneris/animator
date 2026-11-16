"""Shots composed for the frame, not cropped from a wide set.
Rules: faces in the upper-middle band (y 760-1000, below the bar, above the caption), heads big in close-ups,
a foreground layer for depth (sofa back, cake edge, his hand), eyelines pointing at each other, the background
simplified behind the faces. -> shots2.png (before / after for four shots)"""
import os, sys, math, cairo
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import kp as S, sb as B
from kp import R, K, Sh, A, E, P4, INK, WHITE, NAVY, YEL, SKIN, CREAM, RED, rr, fs, ell, limb, txt, hx, lerp, W, H

def wall(c, dim=0.0, garland=True):
    """The room behind a close-up: wall, a soft garland, nothing that competes with a face."""
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, *S.WALL0); g.add_color_stop_rgb(1, *S.WALL1); c.set_source(g); c.paint()
    if garland:
        c.save(); c.translate(0, -300); c.scale(1.0, 1.0); S.garland(c, 760); c.restore()
        c.rectangle(0, 0, W, H); c.set_source_rgba(*S.WALL0, .45); c.fill()                     # pushed back: soft, out of focus
    if dim: c.rectangle(0, 0, W, H); c.set_source_rgba(0, 0, 0, dim); c.fill()

def sofa_fg(c, y, x0=-40, x1=1120):
    """The sofa back as a foreground layer: it hides the bodies' lower halves and gives depth."""
    rr(c, x0, y, x1 - x0, H - y + 60, 46); fs(c, S.SOFA, 8)
    rr(c, x0 + 30, y + 26, x1 - x0 - 60, 24, 12); c.set_source_rgba(1, 1, 1, .15); c.fill()

def eva_at(c, head, s, **kw):
    """Eva with her head centre at screen point head (her body runs off the bottom)."""
    x, y = head; E.eva(c, x, y + 690 * s, s, **{**S.EVA_IN, **kw})
def ai_at(c, head, s, **kw):
    x, y = head; A.myai(c, x, y + 280 * s, s, **kw); return (x, y + 280 * s)

def n01(c, f=0):   # CU MY AI holding V47; Hoody just off-frame left (his thumb, his hat edge), so the line is his
    wall(c)
    ai_at(c, (600, 860), 2.0, eye='focus', look=(-14, 4), droop=1.0, arms=('down', 'down'))
    S.banner(c, 600, 1400, 760, 250, 'v1', text='HAPPY B-DAY EVA'); txt(c, 'V47', 290, 1310, 44, RED, lw=0)
    for x in (230, 970): ell(c, x, 1420, 40, 40); fs(c, WHITE, 7)                                   # its mitts on the banner
    limb(c, [(-120, 1180), (0, 1110), (70, 1060)], 100, NAVY); P4.thumbs_up(c, 90, 1020, 1.8)        # his thumb from the left
    S.party_hat(c, (-60, 860), 1.4, tilt=.6)
    R.bubble(c, ['ACTUALLY, THE FIRST', 'ONE WAS BETTER.'], 10, (40, 900), cy=560, cx=420, size=50)

def n01b(c, f=0):  # the cut-in: V1 and V47 side by side, identical
    wall(c, garland=False)
    for y, lab in ((800, 'V1'), (1260, 'V47')):
        S.banner(c, 540, y, 860, 300, 'v1', text='HAPPY B-DAY EVA'); txt(c, lab, 160, y - 110, 56, RED, lw=0)
    txt(c, '=', 540, 1030, 120, NAVY, lw=0)

def n06(c, f=0):   # CU Eva: the smile gone, eyes down; the cake's edge in the foreground
    wall(c)
    eva_at(c, (540, 860), 2.6, expr='evahurt')
    S.cake(c, 540, 1640, 3.0, sag=1.0); B.heart(c, 600, 1560, 3.0)

def n10(c, f=0):   # the look: two heads at one height, eyelines meeting, the sofa in front, the TV small behind
    wall(c)
    S.tv(c, 470, 640, w=200, h=130)
    ai_at(c, (290, 980), 1.75, eye='open', look=(20, -2), droop=.6, arms=('down', 'down'))
    eva_at(c, (790, 930), 2.0, expr='notices', gaze=-20)
    sofa_fg(c, 1330)

def n14(c, f=0, fl=(-1, -1, -1)):   # the flips, low and frontal: three in a row, each sign readable, the cat given room
    wall(c)
    ai_at(c, (230, 900), 1.3, eye='focus', arms=('down', 'down'))
    eva_at(c, (560, 790), 1.45, expr='amused')
    sofa_fg(c, 1240)
    K.cat(c, 880, 1270, 1.0, pose='walk', phase=0, look=-1)
    signs = [((560, 1110, 330, 210, 'box'), 'NO.', 116), ((230, 1220, 330, 180, 'banner'), 'NO.', 104), ((860, 1380, 230, 140, 'box'), 'no.', 80)]
    for ((x, y, w, h, kind), word, size), v in zip(signs, fl):
        c.save(); c.translate(x, y); c.scale(max(.04, abs(v)), 1); c.translate(-x, -y)
        (S.card_back(c, x, y, w, h, kind) if v > 0 else S.card_front(c, x, y, w, h, word, size, kind)); c.restore()

PAIRS = [('01 MY AI, V47', B.s01, n01), ('01b V1 = V47', None, n01b), ('06 her smile dies', B.s06, n06), ('10 the look', B.s10, n10), ('14 NO. NO. no.', B.s14, n14)]
if __name__ == '__main__':
    k = .26; sw, sh = int(W * k), int(H * k)
    out = cairo.ImageSurface(cairo.FORMAT_ARGB32, len(PAIRS) * (sw + 12) + 12, 2 * (sh + 50) + 20); c = cairo.Context(out); c.set_source_rgb(1, 1, 1); c.paint()
    for i, (name, old, new) in enumerate(PAIRS):
        for j, fn in enumerate((old, new)):
            x, y = 12 + i * (sw + 12), 44 + j * (sh + 50)
            txt(c, ('BEFORE  ' if j == 0 else 'AFTER  ') + name, x + sw / 2, y - 20, 19, NAVY, lw=0)
            if fn is None: continue
            s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); cc = cairo.Context(s); fn(cc, 0)
            Sh.topbar(cc, 'ITS UNION' if '14' in name else 'HER BIRTHDAY')
            if j == 1: s.write_to_png(os.path.join(HERE, f'n_{name[:3].strip()}.png'))
            c.save(); c.translate(x, y); c.scale(k, k); c.set_source_surface(s); c.paint(); c.restore()
    out.write_to_png(os.path.join(HERE, 'shots2.png')); print('ok')
