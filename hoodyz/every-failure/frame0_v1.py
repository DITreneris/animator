"""Every Failure - frame 0 (the hook and the loop target) as a still for approval (process step 3).
Hoody teeters on the chasm edge under the giant FAIL rock; MY AI behind him (antenna blink); across the gap Eva cheers him on
under the unlit SUCCESS sign. Set: Perfect Trip's Giza desert, with a chasm cut into it. Writes frame0.png."""
import os, sys, math, cairo
HERE = os.path.dirname(os.path.abspath(__file__)); PT = os.path.join(HERE, '..', 'perfect-trip')
sys.path.insert(0, PT)
import places as P                                   # Giza desert (adds perfect-date to the path)
from photo import R, K, Sh, E, A                     # Perfect Date's Hoody, MY AI, Eva, series bar
from kit import INK, WHITE, NAVY, rr, fs, ell, hx, txt
W, H = 1080, 1920
GL = P.GY - 40                                        # ground line of the desert
CX0, CX1 = 420, 690                                   # the chasm's lips at the ground line
RED, YEL = hx('d63a32'), hx('ffd23f')

def chasm(c):
    c.move_to(CX0, GL); c.line_to(CX0 + 40, GL + 140); c.line_to(CX0 + 20, GL + 300); c.line_to(CX0 + 70, H + 10)
    c.line_to(CX1 - 60, H + 10); c.line_to(CX1 - 30, GL + 260); c.line_to(CX1 - 50, GL + 120); c.line_to(CX1, GL); c.close_path()
    g = cairo.LinearGradient(0, GL, 0, H); g.add_color_stop_rgb(0, *hx('7a5532')); g.add_color_stop_rgb(1, *hx('2a1c14'))
    c.set_source(g); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()

def rock(c, x, y, s, word, rot=0, ty=0):
    """A grey boulder with one red word on it, centred at x, y."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    pts = [(-150, 20), (-120, -70), (-40, -110), (70, -100), (150, -40), (160, 50), (90, 105), (-60, 110), (-140, 80)]
    c.move_to(*pts[0]); [c.line_to(*p) for p in pts[1:]]; c.close_path(); fs(c, hx('9a9a96'), 7)
    c.move_to(-110, 60); c.line_to(-40, 95); c.line_to(80, 88); c.set_source_rgb(*hx('7b7b77')); c.set_line_width(10); c.stroke()
    txt(c, word, 0, ty, 92, RED, lw=0)
    c.restore()

def success_sign(c, x, y, lit=0.0):
    w, h = 300, 104
    col = tuple((1 - lit) * a + lit * b for a, b in zip(hx('b8ad8c'), YEL))
    rr(c, x - w / 2, y - h / 2, w, h, 26); fs(c, col, 7)
    for q in (-1, 1): c.rectangle(x + q * 110 - 7, y + h / 2, 14, GL - y - h / 2); c.set_source_rgb(*INK); c.fill()
    txt(c, 'SUCCESS', x, y + 2, 60, hx('6e6650') if lit < .5 else INK, lw=0)

BAR = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, 420)
BARK = (956 - 64) / (1044 - 36)                       # the series bar scaled into the safe zone (as Perfect Trip v3)
def topbar(c, label):
    cc = cairo.Context(BAR); cc.set_operator(cairo.OPERATOR_CLEAR); cc.paint(); cc.set_operator(cairo.OPERATOR_OVER)
    Sh.topbar(cc, label)
    c.save(); c.translate(64, 222); c.scale(BARK, BARK); c.translate(-36, -222); c.set_source_surface(BAR, 0, 0); c.paint(); c.restore()

def draw(f=0, teeter=.17):
    S = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(S)
    P.egypt(c, f, s=.8, cx0=560)
    chasm(c)
    for x, y, s, w in ((150, GL - 30, .42, 'FAIL'), (60, GL - 20, .36, 'BUG')):      # the pile of new failures, his side
        rock(c, x, y, s, '')
    success_sign(c, 810, 630, 0)                                            # above her head; text inside x 60-960
    E.eva(c, 870, GL, .85, 'happy' if 'happy' in K.FACES else 'evacalm', pose='holdlow', hand_to=(870 - 150 * .85, GL - 660 * .85), leash=False)
    A.myai(c, 150, GL, .85 * 1.1, eye='happy', arms=('down', 'down'))
    hs, hx_, = .85, 365
    c.save(); c.translate(hx_, GL); c.rotate(teeter); c.translate(-hx_, -GL)        # he teeters towards the gap, about his feet
    tmp = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); hands, _ = R.hoody(cairo.Context(tmp), hx_, GL, hs, expr='shock', arms=('up', 'up'), f=f)
    mx = (hands[0][0] + hands[1][0]) / 2; my = min(hands[0][1], hands[1][1]); rs = 1.25 * hs
    rock(c, mx, my + 10 - 100 * rs, rs, 'FAIL', rot=-.06, ty=-38)                        # resting on his palms, the word clear of his hair; hands drawn over it
    print('hands', [tuple(round(v) for v in h) for h in hands], 'rock centre', round(mx), round(my + 10 - 100 * rs))
    R.hoody(c, hx_, GL, hs, expr='shock', arms=('up', 'up'), f=f)
    c.restore()
    topbar(c, 'HIS SUCCESS')
    return S

if __name__ == '__main__':
    draw().write_to_png(os.path.join(HERE, 'frame0_v1.png')); print('frame0.png')
