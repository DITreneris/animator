"""MY AI - Hoody's companion robot, with the arm set Perfect Date needs.
Body, head and legs are the robot from whos-a-good-boy/v3/v.py (same proportions and colours); arms, eye shapes and props are new.
All poses use fixed pivots in robot units: shoulders at (+-72, 112), elbow, hand. Writes myai_sheet.png."""
import os, sys, math, cairo
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..', '..')
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
import kit as K
from kit import INK, WHITE, NAVY, RED, rr, fs, ell, limb, txt, hx
import eva as E

EYE = hx('33bfff'); VISOR = hx('0b1020'); EARS = (.62, .65, .72); CHEST = (.82, .86, .93); PINK = hx('ff5c8a')
SHOULDER = 72, 112
ARM_W = 24
POSES = {   # per side, for q = +1 (the robot's left = screen right); x is mirrored by q
    'down':  ((96, 170), (100, 234)),
    'wave':  ((150, 60), (150, -46)),
    'offer': ((150, 150), (250, 112)),
    'up':    ((128, 20), (150, -118)),
    'hip':   ((140, 150), (88, 196)),
    'hold':  ((132, 184), (204, 226)),
    'give':  ((128, 142), (196, 70)),
    'chest': ((118, 170), (10, 150)),
    'hold2': ((140, 140), (230, 95)),
}

def eyes(c, mode, look=(0, 0)):
    gx, gy = look
    for q in (-1, 1):
        m = mode
        if mode == 'wink': m = 'happy' if q == 1 else 'open'
        x, y = q * 36 + gx, -8 + gy
        if m == 'open':  ell(c, x, y, 18, 24); c.set_source_rgb(*EYE); c.fill()
        elif m == 'wide': ell(c, x, y, 23, 31); c.set_source_rgb(*EYE); c.fill(); ell(c, x - 6, y - 10, 6, 6); c.set_source_rgb(1, 1, 1); c.fill()
        elif m == 'focus': ell(c, x, y + 4, 21, 8); c.set_source_rgb(*EYE); c.fill()
        elif m == 'happy':
            c.arc(x, y + 14, 19, math.pi + .35, 2 * math.pi - .35); c.set_source_rgb(*EYE); c.set_line_width(11); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
        elif m == 'heart':
            c.save(); c.translate(x, y + 2); c.scale(.95, .95)
            c.move_to(0, 18); c.curve_to(-30, -2, -18, -30, 0, -12); c.curve_to(18, -30, 30, -2, 0, 18); c.close_path()
            c.set_source_rgb(*PINK); c.fill(); c.restore()

def arm(c, q, pose, prop=None):
    (ex, ey), (hx_, hy) = POSES[pose]
    sx, sy = q * SHOULDER[0], SHOULDER[1]
    pts = [(sx, sy), (q * ex, ey), (q * hx_, hy)]
    limb(c, pts, ARM_W + 16, INK); limb(c, pts, ARM_W, WHITE)
    if prop: prop(c, q * hx_, hy, q)
    ell(c, q * hx_, hy, 21, 21); fs(c, WHITE, 6)
    ell(c, q * hx_ - q * 14, hy - 12, 9, 9); fs(c, WHITE, 5)                # thumb nub
    return q * hx_, hy

def myai(c, x, gy, s, eye='open', look=(0, 0), arms=('down', 'down'), props=(None, None), rot=0, walk=None, bob=0):
    """Standing on ground y. arms = (screen-left arm pose, screen-right arm pose). rot tips the whole robot about its feet (a bow is -.35)."""
    c.save(); c.translate(x, gy); c.rotate(rot); c.translate(0, -280 * s - bob); c.scale(s, s); c.set_line_cap(cairo.LINE_CAP_ROUND)
    a = math.sin(walk) * 26 if walk is not None else 0
    limb(c, [(-34, 205), (-34 - a, 280)], 34, WHITE); limb(c, [(34, 205), (34 + a, 280)], 34, WHITE)
    rr(c, -72, 85, 144, 135, 44); fs(c, WHITE)
    ell(c, 0, 150, 30, 30); fs(c, CHEST, 5)
    hands = [arm(c, q, p, pr) for q, p, pr in zip((-1, 1), arms, props)]
    c.move_to(0, -90); c.line_to(0, -132); c.set_source_rgb(*INK); c.set_line_width(9); c.stroke()
    ell(c, 0, -140, 17, 17); fs(c, EYE, 7)
    for q in (-1, 1): ell(c, q * 110, 0, 22, 38); fs(c, EARS, 8)
    rr(c, -108, -95, 216, 180, 78); fs(c, WHITE)
    rr(c, -82, -54, 164, 92, 40); fs(c, VISOR, 6)
    eyes(c, eye, look)
    c.restore()

# ---------------- props ----------------
def rose(c, x, y, q=1):
    limb(c, [(x, y), (x + q * 10, y - 60), (x + q * 6, y - 120)], 9, hx('2f9e4f'))
    c.save(); c.translate(x + q * 6, y - 140)
    for i in range(5): a = i * 2 * math.pi / 5; ell(c, 14 * math.cos(a), 14 * math.sin(a), 18, 18)
    c.set_source_rgb(*RED); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
    ell(c, 0, 0, 12, 12); c.set_source_rgb(*hx('b3122c')); c.fill(); c.restore()
def speaker(c, x, y, q=1):
    rr(c, x - 44, y - 40, 88, 64, 14); fs(c, hx('22252e'), 6)
    ell(c, x, y - 8, 20, 20); fs(c, hx('5b6170'), 4); ell(c, x, y - 8, 7, 7); c.set_source_rgb(*INK); c.fill()
def balloon(c, x, y, q=1):
    c.move_to(x, y); c.curve_to(x + 20, y - 80, x - 20, y - 160, x, y - 230); c.set_source_rgb(*INK); c.set_line_width(3); c.stroke()
    c.save(); c.translate(x, y - 300); c.scale(1.6, 1.6)
    c.move_to(0, 40); c.curve_to(-62, 2, -38, -50, 0, -20); c.curve_to(38, -50, 62, 2, 0, 40); c.close_path()
    fs(c, RED, 5); ell(c, -18, -14, 8, 6); c.set_source_rgba(1, 1, 1, .6); c.fill(); c.restore()

# ---------------- the sheet ----------------
def label(c, s, x, y, size=38, col=INK): txt(c, s, x, y, size, col, lw=0)
def section(c, s, y): txt(c, s, 60, y, 54, NAVY, lw=0, align='l'); c.rectangle(60, y + 32, 2040, 5); c.set_source_rgb(*NAVY); c.fill()

def sheet(out='myai_sheet.png'):
    W, H = 2160, 3300
    S = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(S)
    c.set_source_rgb(*hx('eef1f6')); c.paint()
    txt(c, 'ME + MY AI  -  MY AI  -  CHARACTER SHEET (arm set)', 1080, 60, 58, INK, lw=0)
    v9 = E.load_wgb(); import v as WV

    section(c, 'MY AI - who it is', 130)
    myai(c, 330, 1060, 1.45, eye='happy')
    label(c, 'helpful, eager, never sees it is the problem', 330, 1120, 30, hx('66707f'))
    rs = 1.3; rx = 960; hand = (rx + 230 * rs, 1060 - 280 * rs + 95 * rs)            # hand in hand: her hand lands on his
    E.eva(c, hand[0] + 190 * .9, 1060, .9, 'charmed', sip=.1, pose='holdlow')
    myai(c, rx, 1060, rs, eye='happy', arms=('down', 'hold2'))
    label(c, 'WITH EVA', 1130, 1120, 36); label(c, 'her scarf = its eyes', 1130, 1160, 30, hx('66707f'))
    myai(c, 1700, 1060, 1.05); WV.robot(c, 1980, 1060 - 280 * 1.05, 1.05, boss=True)
    my = 1060 - 280 * 1.05 + 52 * 1.05                                               # HARV never smiles: flat mouth
    rr(c, 1980 - 26 * 1.05, my - 16 * 1.05, 70 * 1.05, 30 * 1.05, 8); c.set_source_rgb(*WHITE); c.fill()
    c.move_to(1980 - 20 * 1.05, my); c.line_to(1980 + 30 * 1.05, my); c.set_source_rgb(*INK); c.set_line_width(8); c.stroke()
    limb(c, [(1980 - 34 * 1.05, 1060 - 75 * 1.05), (1980 - 34 * 1.05, 1060)], 34 * 1.05, WHITE); limb(c, [(1980 + 34 * 1.05, 1060 - 75 * 1.05), (1980 + 34 * 1.05, 1060)], 34 * 1.05, WHITE)
    label(c, 'MY AI  vs  HARV', 1840, 1120, 36); label(c, 'visor + eyes / shades, no visor', 1840, 1160, 30, hx('66707f'))

    section(c, 'EYES', 1240)
    for i, (m, a) in enumerate([('open', 'OPEN'), ('happy', 'HAPPY'), ('heart', 'HEART'), ('wide', 'WIDE'), ('focus', 'FOCUS'), ('wink', 'WINK')]):
        x = 190 + i * 356
        c.save(); c.translate(x, 1460); c.scale(1.05, 1.05)
        for q in (-1, 1): ell(c, q * 110, 0, 22, 38); fs(c, EARS, 8)
        rr(c, -108, -95, 216, 180, 78); fs(c, WHITE); rr(c, -82, -54, 164, 92, 40); fs(c, VISOR, 6); eyes(c, m); c.restore()
        label(c, a, x, 1640, 36)

    section(c, 'ARMS - pivots and poses', 1730)
    P = [(('down', 'down'), 'open', (None, None), 0, 'REST', 'pivots marked'),
         (('down', 'wave'), 'happy', (None, None), 0, 'WAVE', '"Your turn!"'),
         (('down', 'offer'), 'focus', (None, rose), 0, 'OFFER', '"Watch." - the rose'),
         (('up', 'hip'), 'happy', (None, None), .12, 'DANCE', 'one smooth move'),
         (('chest', 'down'), 'happy', (None, None), -.35, 'BOW', 'tips at the feet'),
         (('give', 'down'), 'open', (balloon, None), 0, 'GIVE', 'the balloon to Hoody')]
    for i, (arms, e, pr, rot, a, b) in enumerate(P):
        x = 200 + i * 352
        myai(c, x, 2560, .82, eye=e, arms=arms, props=pr, rot=rot)
        if i == 0:
            for (px, py) in ((-72, 112), (72, 112), (-96, 170), (96, 170), (-100, 234), (100, 234)):
                ell(c, x + px * .82, 2560 - 280 * .82 + py * .82, 9, 9); c.set_source_rgb(*RED); c.fill()
        label(c, a, x, 2630, 36); label(c, b, x, 2672, 28, hx('66707f'))

    section(c, 'PROPS + PALETTE', 2760)
    rose(c, 260, 3160); label(c, 'rose', 260, 3220, 30, hx('66707f'))
    speaker(c, 560, 3080); label(c, 'speaker', 560, 3220, 30, hx('66707f'))
    balloon(c, 860, 3170); label(c, 'heart balloon', 860, 3220, 30, hx('66707f'))
    for i, (col, n) in enumerate([(WHITE, 'BODY ffffff'), (VISOR, 'VISOR 0b1020'), (EYE, 'EYES 33bfff'), (EARS, 'EARS 9ea6b8'), (PINK, 'HEART ff5c8a')]):
        x = 1180 + i * 205; rr(c, x - 90, 2900, 180, 110, 20); fs(c, col, 6); label(c, n, x, 3050, 24)
    S.write_to_png(os.path.join(HERE, out))

if __name__ == '__main__':
    sheet()
