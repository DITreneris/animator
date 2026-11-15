"""Perfect Selfie - shot 9, THE PHOTO, as a still for approval (production gate 1).
Eva seated on the bench, leaning her head towards MY AI (who stands on the seat, faces level, its perfect demo smile).
At the left edge: the bush, a tiny navy sleeve gripping the selfie stick, and one cat's eye. Writes photo_still.png. (v3: Rome, the end of the trip.)"""
import os, sys, math, cairo
HERE = os.path.dirname(os.path.abspath(__file__)); PD = os.path.join(HERE, '..', 'perfect-date')
sys.path.insert(0, PD); sys.path.insert(0, os.path.join(PD, 'characters'))
import importlib.util                   # Perfect Date's render.py, under its own name (this folder has a render.py too)
_spec = importlib.util.spec_from_file_location('pd_render', os.path.join(PD, 'render.py')); R = importlib.util.module_from_spec(_spec)
sys.modules['pd_render'] = R; _spec.loader.exec_module(R)
import kit as K, chars as Sh, eva as E, myai as A
import places as P
from kit import INK, WHITE, NAVY, rr, fs, ell, limb, hx
W, H = 1080, 1920
LEAF, LEAF_D = hx('3f9a4a'), hx('2c7a38')

def bush(c, x, y, s, f=0):
    for i, (dx, dy, r) in enumerate(((-40, 40, 150), (90, -60, 140), (170, 80, 130), (30, 180, 160), (-80, 260, 150), (160, 260, 140))):
        ell(c, x + dx * s, y + dy * s, r * s, r * s); fs(c, LEAF if i % 2 else LEAF_D, 7)
    for i in range(14):                                                  # leaf tips
        a = i * .9; rr_ = 150 + (i * 37) % 90
        c.save(); c.translate(x + 60 * s + math.cos(a) * rr_ * s, y + 110 * s + math.sin(a) * rr_ * s); c.rotate(a)
        ell(c, 0, 0, 26 * s, 12 * s); fs(c, LEAF, 3); c.restore()

def ledge(c, x0, x1, top, h=150):
    """A travertine ledge in the square: somewhere to sit and stand."""
    rr(c, x0, top, x1 - x0, h, 12); fs(c, hx('e9dcc0'), 7)
    c.rectangle(x0 + 6, top + 26, x1 - x0 - 12, 10); c.set_source_rgb(*hx('d4c4a0')); c.fill()
    for k in range(4): c.move_to(x0 + 60 + k * (x1 - x0 - 120) / 3, top + 44); c.line_to(x0 + 60 + k * (x1 - x0 - 120) / 3, top + h - 8); c.set_source_rgb(*hx('cdbd98')); c.set_line_width(4); c.stroke()

def backpack_cat(c, x, y, s=1.0):
    """The corner of Hoody's backpack with the cat's head poking out: both ears, one eye open."""
    c.save(); c.translate(x, y); c.scale(s, s)
    rr(c, -150, -10, 300, 260, 50); fs(c, hx('d9533f'), 7)                          # the backpack
    rr(c, -150, -10, 300, 70, 30); fs(c, hx('b8412f'), 6)                            # its open flap
    c.move_to(-150, 120); c.line_to(150, 120); c.set_source_rgb(*hx('8f2f22')); c.set_line_width(5); c.stroke()
    K._cat_head(c, 0, -40, 1.5, False, 'sleep', 0)                                   # the cat, sleepy...
    ell(c, 30 * 1.5, -46, 17 * 1.5, 14 * 1.5); c.set_source_rgb(*K.TABBY); c.fill()  # ...but one eye open
    ell(c, 30 * 1.5, -44, 11 * 1.5, 14 * 1.5); fs(c, hx('b8e04a'), 4); ell(c, 27 * 1.5, -44, 4 * 1.5, 10 * 1.5); c.set_source_rgb(*INK); c.fill()
    rr(c, -160, 20, 320, 40, 16); fs(c, hx('b8412f'), 6)                             # the rim in front of her chin
    c.restore()

def finger(c, x0, y, length, thick, bend=0):
    """One finger lying sideways: a rounded capsule with a fingernail at the tip and a knuckle crease."""
    c.save(); c.translate(x0, y); c.rotate(bend)
    rr(c, 0, -thick / 2, length, thick, thick / 2); fs(c, K.SKIN, 6)
    rr(c, length - thick * .95, -thick * .32, thick * .72, thick * .64, thick * .3); c.set_source_rgb(*hx('ffe9df')); c.fill_preserve()
    c.set_source_rgb(*hx('e3b9a4')); c.set_line_width(3); c.stroke()                                  # the nail
    for k in (.38, .66): c.move_to(length * k, -thick * .3); c.curve_to(length * k + 6, -thick * .1, length * k + 6, thick * .1, length * k, thick * .3)
    c.set_source_rgb(*hx('e3b9a4')); c.set_line_width(3); c.stroke()                                   # knuckle creases
    c.restore()

def pinch_hand(c, x0, y_top, y_bot, reach):
    """Hoody's hand near the camera, from the left edge, in the tourist pinch: the index finger over the top, the thumb under the base."""
    my = (y_top + y_bot) / 2; t = 64
    limb(c, [(-90, my + 230), (x0 - 70, my + 70)], 130, NAVY)                             # the sleeve
    c.move_to(x0 - 120, my + 110); c.curve_to(x0 - 150, my - 40, x0 - 60, y_top + 10, x0 + 30, y_top + 20)
    c.line_to(x0 + 40, y_bot - 30); c.curve_to(x0 - 20, y_bot, x0 - 100, my + 150, x0 - 120, my + 110); c.close_path(); fs(c, K.SKIN, 7)   # the palm side
    for k in range(3): finger(c, x0 - 70, my - 40 + k * 46, 120, 46, .15)                 # three curled fingers, tucked
    finger(c, x0 - 10, y_top + 4, reach, t, -.05)                                          # the index, reaching over the top
    finger(c, x0 - 10, y_bot - 4, reach * .78, t * 1.08, .06)                              # the thumb, under the base

def photo(c, f=0, label='ITS TRIP', stamp_k=1.0):
    """Rome, the final photo. Reading order: the couple; Hoody's big hand pinching the (far, small) Colosseum; the cat in his backpack."""
    CS, CX, HZ = .62, 300, 1230                                          # the Colosseum, far off at the left, on a raised horizon: big, but pinchable
    P.rome(c, f, s=CS, cx=CX, horizon=HZ)
    TOP = 1520
    ledge(c, 480, 1110, TOP)
    es, ex = 1.05, 850
    c.save(); c.rectangle(0, 0, W, TOP + 6); c.clip()
    rx, rs = 590, 1.32
    hp = A.hand_at(rx, TOP - 6, rs, 1, 'hold')                           # where its hand is: she takes it
    E.eva(c, ex, TOP + 250 * es, es, 'charmed', sip=.1, tilt=-.22, pose='holdlow', hand_to=hp); c.restore()
    for q in (-1, 1):
        limb(c, [(ex + q * 34 * es, TOP + 4), (ex + q * 38 * es, TOP + 200)], 32 * es, E.TROUS)
        ell(c, ex + q * 34 * es, TOP + 6, 36 * es, 26 * es); fs(c, E.TROUS, 5)
        ell(c, ex + q * 42 * es, TOP + 206, 30 * es, 14 * es); fs(c, E.SHOE, 4)
    A.myai(c, rx, TOP - 6, rs, eye='happy', arms=('wave', 'hold'), tilt=8)
    ell(c, *hp, 20 * es, 18 * es); fs(c, E.SKIN_E, 4)                       # her hand on top of its hand: they're holding hands
    base = HZ; top = HZ - (P.GY - 60 - 700) * CS                         # the Colosseum's top and base on screen
    pinch_hand(c, 120, top - 10, base + 12, CX - 30)
    backpack_cat(c, 190, 1660, 1.0)
    P.stamp(c, 'rome', k=stamp_k)
    c.rectangle(0, 0, W, H); c.rectangle(34, 34, W - 68, H - 68); c.set_fill_rule(cairo.FILL_RULE_EVEN_ODD); c.set_source_rgb(*WHITE); c.fill()
    c.set_fill_rule(cairo.FILL_RULE_WINDING)
    Sh.topbar(c, label)

if __name__ == '__main__':
    S = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(S); photo(c)
    S.write_to_png(os.path.join(HERE, 'photo_still.png')); print('photo_still.png')
