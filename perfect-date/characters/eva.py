import math
"""Eva, v2 (v1 + gold hoops, lash on every expression, one-brow signature, four poses, slimmer coat).
Eva, v1. Built on the neighbour from Who's a Good Boy? (yellow coat, dark curls, coffee, the red-collared dog),
moved onto the series face system so she can act. Writes eva_sheet.png."""
import sys, math, cairo
HERE = __import__('os').path.dirname(__import__('os').path.abspath(__file__))
ROOT = __import__('os').path.join(HERE, '..', '..')
sys.path.insert(0, __import__('os').path.join(HERE, '..'))
import kit as K
from kit import INK, WHITE, NAVY, YEL, RED, rr, fs, ell, limb, txt, hx

SKIN_E = hx('e8b48c'); HAIR_E = hx('3b2416'); COAT = hx('ffcf2e'); TROUS = hx('8193ad'); SHOE = hx('1f2230')   # trousers grey-blue (15 Nov): navy read as Hoody's legs
GOLD = hx('e7b84b')             # hoops: her permanent accessory
SCARF = hx('33bfff')            # matches MY AI's eyes: the one hint she likes machines
BROWN = hx('9a5b2e'); DARKB = hx('5e3416')

_mouth = K.mouth
def mouth(c, kind, op):
    if kind == 'soft' and op <= 0:
        c.set_source_rgb(*INK); c.set_line_width(7); c.move_to(-20, 64); c.curve_to(-8, 80, 8, 80, 20, 64); c.stroke(); return
    return _mouth(c, kind, op)
K.mouth = mouth
K.FACES.update({
    'evacalm':   ('open', (None, None), 'soft'),
    'charmed':   ('happy', (None, None), 'grin'),
    'amused':    ('smug', ('flat', 'up'), 'smirk'),
    'impressed': ('open', ('raised', 'raised'), 'o'),
    'laugh':     ('happy', ('raised', 'raised'), 'grin'),
    'notices':   ('open', ('raised', None), 'soft'),
})
HAPPY = {'charmed', 'laugh', 'happy'}
OPEN = {'evacalm', 'calm', 'amused', 'impressed', 'notices', 'polite', 'shock', 'hopeful'}

BACK = [(-98, -40, 54), (-62, -98, 56), (0, -120, 60), (62, -98, 56), (98, -40, 54), (-114, 18, 42), (114, 20, 42),
        (-106, 72, 34), (106, 74, 34), (150, 34, 38), (178, 68, 30), (190, 102, 22)]
FRINGE = [(-74, -64, 30), (-36, -82, 32), (8, -86, 32), (50, -72, 30), (80, -44, 24)]

def eva_head(c, x, y, s, expr='evacalm', gaze=0, tilt=0, blink=False, op=0):
    c.save(); c.translate(x, y); c.rotate(tilt); c.scale(s, s)
    for b in BACK: ell(c, *b[:2], b[2], b[2])
    c.set_source_rgb(*INK); c.set_line_width(16); c.stroke()
    for b in BACK: ell(c, *b[:2], b[2], b[2])
    c.set_source_rgb(*HAIR_E); c.fill()
    rr(c, -92, -70, 184, 176, 84); fs(c, SKIN_E)
    for b in FRINGE: ell(c, *b[:2], b[2], b[2])
    c.set_source_rgb(*HAIR_E); c.fill()
    for q in (-1, 1):                                      # gold mini hoops
        ell(c, q * 100, 92, 15, 17); c.set_source_rgb(*INK); c.set_line_width(13); c.stroke()
        ell(c, q * 100, 92, 15, 17); c.set_source_rgb(*GOLD); c.set_line_width(6); c.stroke()
    old = K.SKIN; K.SKIN = SKIN_E
    try: K.face(c, expr, gaze, blink, op)
    finally: K.SKIN = old
    for q in (-1, 1):                                      # a lash flick on every expression: open or closed eyes
        if expr in HAPPY or blink: c.move_to(q * 60, 20); c.line_to(q * 74, 12)
        else: c.move_to(q * 60, -6); c.line_to(q * 74, -16)
        c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    c.restore()

def coffee(c, x, y, s):
    rr(c, x - 22 * s, y - 50 * s, 44 * s, 62 * s, 7 * s); fs(c, WHITE, max(3, 5 * s))
    c.rectangle(x - 22 * s, y - 30 * s, 44 * s, 16 * s); c.set_source_rgb(*hx('8a5a2e')); c.fill()
    rr(c, x - 25 * s, y - 58 * s, 50 * s, 12 * s, 5 * s); fs(c, WHITE, max(3, 4 * s))

def eva(c, x, gy, s, expr='evacalm', sip=0.0, gaze=0, tilt=0, leash=True, op=0, pose='coffee', hand_to=None, walk=None, blink=False):
    """Full figure standing at ground y. sip 0 = cup at the waist, 1 = at the mouth. Returns the free hand (the leash hand).
    pose: coffee (default) | hip (free hand on the hip) | glance (sip, sideways look, one brow up) | reach (free hand out: takes a hand)"""
    if pose == 'glance': sip, gaze, tilt, expr = max(sip, .7), 16, .1, 'amused'
    for q, ph in ((-1, walk or 0), (1, (walk or 0) + math.pi)):     # legs: hip, knee, foot; a step when walking
        if walk is None: fx, lift, kx = x + q * 28 * s, 0, x + q * 28 * s
        else: fx = x + q * 26 * s + math.sin(ph) * 46 * s; lift = max(0, math.cos(ph)) * 26 * s; kx = x + q * 26 * s + math.sin(ph) * 26 * s + 10 * s
        limb(c, [(x + q * 26 * s, gy - 250 * s), (kx, gy - 130 * s - lift * .5), (fx, gy - 14 * s - lift)], 30 * s, TROUS)
        ell(c, fx + 4 * s, gy - 8 * s - lift, 28 * s, 14 * s); fs(c, SHOE, max(3, 5 * s))
    if walk is not None: gy -= abs(math.sin(walk)) * 7 * s
    hy = gy - 690 * s
    c.move_to(x - 84 * s, hy + 120 * s); c.line_to(x + 84 * s, hy + 120 * s); c.line_to(x + 110 * s, gy - 226 * s); c.line_to(x - 110 * s, gy - 226 * s)
    c.close_path(); fs(c, COAT, max(3, 7 * s))
    for i in range(3): ell(c, x, hy + 178 * s + i * 72 * s, 7 * s, 7 * s); c.set_source_rgb(*INK); c.fill()
    hxp = x + 46 * s + (1 - sip) * 44 * s; hyp = hy + K.lerp(270, 84, sip) * s
    limb(c, [(x + 76 * s, hy + 142 * s), (x + 124 * s, hy + 256 * s), (hxp, hyp)], 30 * s, COAT)
    coffee(c, hxp, hyp + 4 * s, s)
    if pose == 'hip':
        lh = (x - 96 * s, hy + 318 * s)
        limb(c, [(x - 76 * s, hy + 142 * s), (x - 168 * s, hy + 236 * s), lh], 30 * s, COAT)
    elif pose == 'holdlow':                                     # holding someone's hand at her side (hand_to: where it lands)
        sh = (x - 76 * s, hy + 142 * s); lh = hand_to or (x - 190 * s, hy + 410 * s)
        el = ((sh[0] + lh[0]) / 2 - 30 * s, (sh[1] + lh[1]) / 2 + 10 * s)
        limb(c, [sh, el, lh], 30 * s, COAT)
    elif pose == 'reach':
        lh = (x - 250 * s, hy + 236 * s)
        limb(c, [(x - 76 * s, hy + 142 * s), (x - 170 * s, hy + 214 * s), lh], 30 * s, COAT)
    else:
        lh = (x - 116 * s, hy + 344 * s)
        limb(c, [(x - 76 * s, hy + 142 * s), (x - 120 * s, hy + 262 * s), lh], 30 * s, COAT)
    ell(c, *lh, 18 * s, 18 * s); fs(c, SKIN_E, max(3, 5 * s))
    rr(c, x - 80 * s, hy + 96 * s, 160 * s, 46 * s, 22 * s); fs(c, SCARF, max(3, 6 * s))         # scarf
    rr(c, x + 24 * s, hy + 128 * s, 34 * s, 80 * s, 12 * s); fs(c, SCARF, max(3, 5 * s))
    eva_head(c, x, hy, .74 * s, expr, gaze, tilt, op=op, blink=blink)
    return lh

def dog(c, x, gy, s, look=0, f=0):
    """The red-collared dog from Who's a Good Boy? (sitting). Returns the collar point."""
    tw = math.sin(f * .6) * 14 * s
    c.move_to(x + 60 * s, gy - 30 * s); c.curve_to(x + 95 * s, gy - 40 * s, x + 100 * s + tw, gy - 80 * s, x + 86 * s + tw, gy - 100 * s)
    c.set_source_rgb(*INK); c.set_line_width(20 * s); c.stroke()
    c.move_to(x + 60 * s, gy - 30 * s); c.curve_to(x + 95 * s, gy - 40 * s, x + 100 * s + tw, gy - 80 * s, x + 86 * s + tw, gy - 100 * s)
    c.set_source_rgb(*BROWN); c.set_line_width(12 * s); c.stroke()
    ell(c, x + 40 * s, gy - 34 * s, 44 * s, 34 * s); fs(c, BROWN, max(3, 6 * s))
    ell(c, x + 12 * s, gy - 70 * s, 42 * s, 56 * s); fs(c, BROWN, max(3, 6 * s))
    for q in (0, 1): limb(c, [(x - 10 * s + q * 22 * s, gy - 70 * s), (x - 14 * s + q * 22 * s, gy - 6 * s)], 16 * s, BROWN)
    hx_, hy = x - 12 * s, gy - 138 * s - look * 14 * s
    c.rectangle(x - 28 * s, gy - 104 * s, 52 * s, 12 * s); c.set_source_rgb(*RED); c.fill()
    ell(c, hx_, hy, 38 * s, 32 * s); fs(c, BROWN, max(3, 6 * s))
    ell(c, hx_ - 34 * s, hy + 10 * s, 22 * s, 15 * s); fs(c, BROWN, max(3, 5 * s)); ell(c, hx_ - 52 * s, hy + 6 * s, 7 * s, 6 * s); c.set_source_rgb(*INK); c.fill()
    c.save(); c.translate(hx_ + 14 * s, hy + 4 * s); c.rotate(.3); ell(c, 0, 0, 13 * s, 28 * s); fs(c, DARKB, max(3, 4 * s)); c.restore()
    ell(c, hx_ - 14 * s, hy - 8 * s, 5 * s, 6 * s); c.set_source_rgb(*INK); c.fill()
    return (x - 2 * s, gy - 98 * s)

def leash(c, a, b, sag=110):
    c.move_to(*a); c.curve_to(a[0], a[1] + sag, b[0] + 40, b[1] - 50, *b); c.set_source_rgb(*INK); c.set_line_width(4); c.stroke()

def label(c, s, x, y, size=38, col=INK): txt(c, s, x, y, size, col, lw=0)
def section(c, s, y):
    txt(c, s, 60, y, 54, NAVY, lw=0, align='l'); c.rectangle(60, y + 32, 2040, 5); c.set_source_rgb(*NAVY); c.fill()

def load_wgb():
    import importlib.util
    wgb = __import__('os').path.join(ROOT, 'whos-a-good-boy', 'v3'); sys.path.insert(0, wgb)
    spec = importlib.util.spec_from_file_location('v9', __import__('os').path.join(wgb, 'v9.py'))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def sheet(out='eva_sheet.png'):
    v9 = load_wgb()
    W, H = 2160, 3560
    S = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(S)
    c.set_source_rgb(*hx('eef1f6')); c.paint()
    txt(c, 'ME + MY AI  -  EVA  -  CHARACTER SHEET v2', 1080, 60, 58, INK, lw=0)

    section(c, 'EVA - who she is', 130)
    lh = eva(c, 330, 1090, 1.12, 'evacalm', sip=.15)
    dc = dog(c, 620, 1090, 1.0, look=1); leash(c, lh, dc)
    label(c, 'yellow coat, curls + side bun,', 400, 1150, 32, hx('66707f')); label(c, 'coffee, the dog on a lead', 400, 1192, 32, hx('66707f'))
    # where she came from
    c.save(); c.translate(1000, 300); c.scale(.55, .55)
    l2 = v9.neighbor(c, 200, 1300, 1.0, 0, sip=1.0); d2 = v9.dog(c, 420, 1300, 1.0, 'sit', look=1)
    c.move_to(*l2); c.curve_to(l2[0], l2[1] + 120, d2[0] + 40, d2[1] - 60, *d2); c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
    c.restore()
    label(c, 'FIRST SEEN', 1150, 1060, 36); label(c, "Who's a Good Boy? (the park)", 1150, 1100, 30, hx('66707f'))
    # with MY AI, for scale
    v9.bot(c, 1920, 1090, 1.38, walk=0, eye=(0, -6), glow=.55)         # MY AI: the companion from Who's a Good Boy?, human height
    eva(c, 1540, 1090, .9, 'charmed', sip=0, leash=False)
    label(c, 'EVA + MY AI', 1760, 1150, 36); label(c, 'scarf = the colour of its eyes', 1760, 1192, 30, hx('66707f'))

    section(c, 'EXPRESSIONS', 1270)
    E = [('evacalm', 'CALM', 'coffee, park, her day'), ('impressed', 'IMPRESSED', 'competence - the rose'),
         ('charmed', 'CHARMED', 'the dance'), ('laugh', 'LAUGH', 'the music'),
         ('amused', 'AMUSED', 'sharp - sees everything'), ('notices', 'NOTICES HOODY', 'the long game')]
    for i, (e, a, b) in enumerate(E):
        x = 190 + i * 356
        eva_head(c, x, 1520, 1.0, e, gaze=(14 if e == 'notices' else 0), tilt=(.12 if e == 'notices' else 0), op=(.9 if e == 'laugh' else 0))
        label(c, a, x, 1730, 36); label(c, b, x, 1772, 28, hx('66707f'))

    section(c, 'POSES', 1860)
    P = [('coffee', 'COFFEE', 'her default'), ('hip', 'HAND ON HIP', 'confident, waiting'),
         ('glance', 'THE GLANCE', 'sip + one brow: I see you'), ('reach', 'REACH', 'takes the hand (Perfect Date)')]
    for i, (p_, a, b) in enumerate(P):
        x = 300 + i * 520
        if p_ == 'reach': v9.bot(c, 1680, 2600, 1.15, walk=0, eye=(12, -6), glow=.55)    # MY AI, human height, her hand on his
        eva(c, 2010 if p_ == 'reach' else x, 2600, .78, 'charmed' if p_ == 'reach' else 'evacalm', sip=.1, pose=p_)
        label(c, a, x, 2660, 36); label(c, b, x, 2702, 28, hx('66707f'))

    section(c, 'PALETTE + PROPS', 2780)
    for i, (col, n) in enumerate([(COAT, 'COAT ffcf2e'), (HAIR_E, 'HAIR 3b2416'), (SKIN_E, 'SKIN e8b48c'), (SCARF, 'SCARF 33bfff'), (GOLD, 'HOOPS e7b84b'), (TROUS, 'TROUSERS 30364a'), (BROWN, 'DOG 9a5b2e')]):
        x = 150 + i * 310; rr(c, x - 105, 2860, 210, 110, 20); fs(c, col, 6); label(c, n, x, 3010, 26)
    coffee(c, 360, 3330, 2.0); label(c, 'the coffee', 360, 3420, 32, hx('66707f'))
    dog(c, 860, 3400, 1.3, look=1); label(c, 'her dog (red collar)', 880, 3450, 32, hx('66707f'))
    eva_head(c, 1560, 3250, 1.25, 'amused'); label(c, 'SIGNATURE: one brow up + hoops', 1560, 3480, 32)
    S.write_to_png(out)

if __name__ == '__main__':
    sheet()
