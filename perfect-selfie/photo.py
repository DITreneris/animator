"""Perfect Selfie - shot 9, THE PHOTO, as a still for approval (production gate 1).
Eva seated on the bench, leaning her head towards MY AI (who stands on the seat, faces level, its perfect demo smile).
At the left edge: the bush, a tiny navy sleeve gripping the selfie stick, and one cat's eye. Writes photo_still.png. (v3: Rome, the end of the trip.)"""
import os, sys, math, cairo
HERE = os.path.dirname(os.path.abspath(__file__)); PD = os.path.join(HERE, '..', 'perfect-date')
sys.path.insert(0, PD); sys.path.insert(0, os.path.join(PD, 'characters'))
import render as R                      # Perfect Date: park, bench, Hoody's arm, the title bar
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

def photo(c, f=0, label='ITS TRIP', stamp_k=1.0):
    """Rome, the final photo. Reading order: the couple; Hoody's finger 'pressing' the Colosseum; the cat in the corner."""
    P.rome(c, f)
    TOP = 1500
    ledge(c, 150, 1110, TOP)
    es, ex = 1.25, 760
    c.save(); c.rectangle(0, 0, W, TOP + 6); c.clip()                     # Eva seated on the ledge: hips on the top, standing legs clipped away
    E.eva(c, ex, TOP + 250 * es, es, 'charmed', sip=0, tilt=-.24, pose='coffee'); c.restore()
    for q in (-1, 1):                                                     # knees at the edge, shins down the front
        limb(c, [(ex + q * 34 * es, TOP + 4), (ex + q * 38 * es, TOP + 200)], 32 * es, E.TROUS)
        ell(c, ex + q * 34 * es, TOP + 6, 36 * es, 26 * es); fs(c, E.TROUS, 5)
        ell(c, ex + q * 42 * es, TOP + 206, 30 * es, 14 * es); fs(c, E.SHOE, 4)
    # MY AI standing on the ledge beside her: the perfect demo smile, a clear open-palm wave, its other hand nearly touching hers
    A.myai(c, 450, TOP - 6, 1.7, eye='happy', arms=('wave', 'down'), tilt=8)
    # Hoody: only his sleeve and finger, in from the left edge, pressing the Colosseum's corner - the forced-perspective pose, at last
    c.save(); c.translate(44, 0)                                          # clear of the photo's border
    tip = (120, 748)                                                     # down onto the Colosseum's top edge
    limb(c, [(-80, 560), (40, 600), (118, 650)], 70, NAVY)                # sleeve in from the left edge, above the corner
    rr(c, 84, 612, 76, 64, 28); fs(c, K.SKIN, 6)                          # the hand
    rr(c, tip[0] - 15, 660, 30, tip[1] - 660, 14); fs(c, K.SKIN, 6)      # the finger, pressing down on the corner
    # the cat, riding on his shoulder just out of frame: an ear tip and one eye peeking in under the sleeve
    c.move_to(-6, 640); c.line_to(34, 600); c.line_to(52, 668); c.close_path(); fs(c, K.TABBY, 6)
    c.move_to(14, 630); c.line_to(32, 612); c.line_to(40, 650); c.close_path(); c.set_source_rgb(*hx('ffb3a7')); c.fill()
    ell(c, 18, 700, 64, 50); fs(c, K.TABBY, 6)
    ell(c, 44, 694, 18, 14); fs(c, hx('b8e04a'), 4); ell(c, 42, 694, 5, 11); c.set_source_rgb(*INK); c.fill()
    c.restore()
    P.stamp(c, 'rome', k=stamp_k)
    c.rectangle(0, 0, W, H); c.rectangle(34, 34, W - 68, H - 68); c.set_fill_rule(cairo.FILL_RULE_EVEN_ODD); c.set_source_rgb(*WHITE); c.fill()
    c.set_fill_rule(cairo.FILL_RULE_WINDING)
    Sh.topbar(c, label)

if __name__ == '__main__':
    S = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(S); photo(c)
    S.write_to_png(os.path.join(HERE, 'photo_still.png')); print('photo_still.png')
