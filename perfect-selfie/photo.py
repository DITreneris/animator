"""Perfect Selfie - shot 9, THE PHOTO, as a still for approval (production gate 1).
Eva seated on the bench, leaning her head towards MY AI (who stands on the seat, faces level, its perfect demo smile).
At the left edge: the bush, a tiny navy sleeve gripping the selfie stick, and one cat's eye. Writes photo_still.png."""
import os, sys, math, cairo
HERE = os.path.dirname(os.path.abspath(__file__)); PD = os.path.join(HERE, '..', 'perfect-date')
sys.path.insert(0, PD); sys.path.insert(0, os.path.join(PD, 'characters'))
import render as R                      # Perfect Date: park, bench, Hoody's arm, the title bar
import kit as K, chars as Sh, eva as E, myai as A
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

def photo(c, f=0, label='ITS SELFIE'):
    R.park(c, f, zoom=1.35, cy=1350)
    c.save(); c.translate(560, 1880); c.scale(1.22, 1.22); c.translate(-560, -1880)   # a selfie is framed close
    SEAT = 1560
    R.bench(c, 120, 1180, SEAT, 1800)
    # Eva, seated (her lap on the seat), her head leaning towards MY AI
    es, ex = 1.05, 760
    c.save(); c.rectangle(0, 0, W, SEAT + 6); c.clip()                    # seated: hips on the seat, the standing legs clipped away
    E.eva(c, ex, SEAT + 250 * es, es, 'charmed', sip=0, tilt=-.24, pose='coffee'); c.restore()
    for q in (-1, 1):                                                     # knees at the seat's edge, shins down to the path
        limb(c, [(ex + q * 34 * es, SEAT + 4), (ex + q * 38 * es, 1786)], 32 * es, E.TROUS)
        ell(c, ex + q * 34 * es, SEAT + 6, 36 * es, 26 * es); fs(c, E.TROUS, 5)
        ell(c, ex + q * 42 * es, 1790, 30 * es, 14 * es); fs(c, E.SHOE, 4)
    # MY AI standing on the seat beside her, faces level, the perfect demo smile and a photo wave
    A.myai(c, 460, SEAT - 10, 1.45, eye='happy', arms=('wave', 'down'), tilt=8)
    c.restore()
    # the bush at the left edge (in front, nearer the camera): his sleeve and hand grip the stick; one cat's eye beside it
    bush(c, -70, 1080, 1.05)
    hand = (205, 1290)
    c.move_to(hand[0] + 10, hand[1] + 6); c.line_to(-40, 1960)                            # the stick, running back towards the camera
    c.set_source_rgb(*INK); c.set_line_width(26); c.stroke_preserve(); c.set_source_rgb(*hx('8a8f9c')); c.set_line_width(16); c.stroke()
    limb(c, [(60, 1250), hand], 34, NAVY)                                                  # a navy sleeve out of the leaves
    ell(c, hand[0], hand[1], 20, 18); fs(c, K.SKIN, 4)
    ell(c, 120, 1150, 26, 20); fs(c, hx('b8e04a'), 5); ell(c, 117, 1150, 6, 15); c.set_source_rgb(*INK); c.fill()   # the cat's one eye
    # the photo's thin border
    c.rectangle(0, 0, W, H); c.rectangle(34, 34, W - 68, H - 68); c.set_fill_rule(cairo.FILL_RULE_EVEN_ODD); c.set_source_rgb(*WHITE); c.fill()
    c.set_fill_rule(cairo.FILL_RULE_WINDING)
    Sh.topbar(c, label)

if __name__ == '__main__':
    S = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(S); photo(c)
    S.write_to_png(os.path.join(HERE, 'photo_still.png')); print('photo_still.png')
