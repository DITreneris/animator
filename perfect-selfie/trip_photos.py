"""Perfect Trip - the three album photos before Rome, as stills for approval.
Each photo: the place, MY AI's perfect forced-perspective pose, Hoody's failed copy (smaller every time), Eva charmed by
the robot, and the cat's head out of the backpack in the same bottom-left corner. python3 trip_photos.py writes trip_photos.png."""
import os, sys, math, cairo
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import photo as PH                     # Rome photo + shared helpers (backpack_cat), and through it Perfect Date's characters
import places as P
from photo import R, K, Sh, E, A
from kit import INK, WHITE, NAVY, rr, fs, ell, limb, hx
W, H = 1080, 1920
CAMEL, CAMEL_D = hx('c8955a'), hx('a8763f')

def frame(c, place, label='HIS TRIP'):
    P.stamp(c, place)
    c.rectangle(0, 0, W, H); c.rectangle(34, 34, W - 68, H - 68); c.set_fill_rule(cairo.FILL_RULE_EVEN_ODD); c.set_source_rgb(*WHITE); c.fill()
    c.set_fill_rule(cairo.FILL_RULE_WINDING)
    Sh.topbar(c, label)

def camel(c, x, gy, s, f=0):
    """A walking camel, facing left: legs, body, one hump, a long curved neck."""
    c.save(); c.translate(x, gy); c.scale(s, s)
    for k, (lx, ph) in enumerate(((-90, 0), (-60, math.pi), (70, math.pi), (100, 0))):
        sw = math.sin(f * .3 + ph) * 18
        limb(c, [(lx, -230), (lx + sw * .5, -120), (lx + sw, 0)], 26, CAMEL_D if k % 2 else CAMEL)
    ell(c, 0, -260, 150, 70); fs(c, CAMEL, 7)
    c.move_to(-70, -300); c.curve_to(-40, -420, 60, -420, 80, -300); c.close_path(); fs(c, CAMEL, 7)           # the hump
    limb(c, [(-120, -270), (-190, -360), (-200, -470)], 46, CAMEL)                                              # the neck
    ell(c, -230, -480, 62, 34); fs(c, CAMEL, 6); ell(c, -260, -492, 7, 7); c.set_source_rgb(*INK); c.fill()      # head, eye
    c.move_to(150, -270); c.curve_to(190, -240, 180, -190, 170, -160); c.set_source_rgb(*INK); c.set_line_width(8); c.stroke()  # tail
    c.restore()

def tele_arm(c, rx, gy, rs, q, target, tip='finger'):
    """MY AI's telescopic arm (it's a robot): from its shoulder, nested white segments out to a target point.
    tip: 'finger' (one finger up: something balances on it) or 'palm' (an open palm, facing up: it holds something up)."""
    sh = (rx + q * A.SHOULDER[0] * rs, gy - 280 * rs + A.SHOULDER[1] * rs)
    dx, dy = target[0] - sh[0], target[1] - sh[1]; L = math.hypot(dx, dy); ang = math.atan2(dy, dx)
    c.save(); c.translate(*sh); c.rotate(ang)
    for k, w in enumerate((26, 21, 17)):                                    # three nested sections, each thinner
        a, b = L * k / 3 - (6 if k else 0), L * (k + 1) / 3
        rr(c, a, -w * rs / 1.2, b - a, w * rs / .6, w * rs / 1.2); fs(c, WHITE, max(4, 6 * rs / 1.4))
        if k: ell(c, a + 4, 0, 6 * rs, w * rs / 1.1); fs(c, A.CHEST, 3)      # the collar where a section slides out
    c.restore()
    if tip == 'finger':
        ell(c, target[0], target[1] + 20 * rs, 21 * rs, 19 * rs); fs(c, WHITE, 6)                       # the mitt...
        rr(c, target[0] - 7 * rs, target[1] - 4 * rs, 14 * rs, 26 * rs, 7 * rs); fs(c, WHITE, 5)        # ...one finger up
    else:
        ell(c, target[0], target[1] + 12 * rs, 30 * rs, 14 * rs); fs(c, WHITE, 6)                       # a flat palm, up
    ell(c, *sh, 20 * rs, 20 * rs); fs(c, WHITE, 6)

def pisa(c, f=0):
    """Hoody full height, leaning in with his palm on the tower's low side: pushing it over. MY AI reaches its telescopic arm
    up under the overhang: holding it up. Eva laughing at the robot's perfect pose."""
    P.pisa(c, f)
    edge = lambda y, q: 640 + math.tan(math.radians(8)) * (P.GY - 60 - y) + q * 115     # the tower's side at height y
    rx, rgy, rs = 820, 1840, 1.2
    A.myai(c, rx, rgy, rs, eye='happy', arms=(None, 'hip'), tilt=-6)
    tele_arm(c, rx, rgy, rs, -1, (edge(640, 1) + 24, 640), tip='palm')
    R.hoody(c, 330, 1810, .98, expr='happy', arms=('rest', 'out'), rot=.14, f=f)          # leaning in, pushing
    E.eva(c, 170, 1860, .95, 'amused', sip=.6, gaze=18)
    PH.backpack_cat(c, 210, 1720, .9)
    frame(c, 'pisa')

def paris(c, f=0):
    """Hoody knee-high, far back by the tower, a finger up his own nose. MY AI's telescopic arm: the spire balanced on one fingertip."""
    rx, rgy, rs, hz = 780, 1880, 1.5, 1640
    tipxy = (400, 760)
    s = ((hz - 10) - tipxy[1]) / 1370
    P.paris(c, f, s=s, cx0=tipxy[0], horizon=hz)
    R.hoody(c, 560, hz + 30, .4, expr='calm', arms=('rest', 'chin'), f=f)   # far back on the path; finger to his nose
    E.eva(c, 200, 1890, .9, 'impressed', sip=.2, gaze=16)
    A.myai(c, rx, rgy, rs, eye='focus', arms=(None, 'down'), tilt=-4)
    tele_arm(c, rx, rgy, rs, -1, (tipxy[0], tipxy[1] + 26), tip='finger')
    PH.backpack_cat(c, 210, 1720, .9)
    frame(c, 'paris')

def giza(c, f=0):
    """Hoody a dot in the sand, waving; a camel walks in front of him, bigger than he is. MY AI's fingertip on the pyramid's tip."""
    rx, rgy, rs, hz = 820, 1880, 1.5, 1640
    tipxy = (420, 980)
    s = ((hz - 40 + 40 - 40) - tipxy[1]) / 620
    P.egypt(c, f, s=s, cx0=tipxy[0] - 20 * s, horizon=hz)
    R.hoody(c, 560, hz + 10, .1, expr='calm', arms=('up', 'up'), f=f)    # a dot, waving
    camel(c, 610, hz + 30, .3, f)
    E.eva(c, 200, 1890, .9, 'charmed', sip=.2, gaze=16)
    A.myai(c, rx, rgy, rs, eye='happy', arms=(None, 'down'), tilt=-4)
    tele_arm(c, rx, rgy, rs, -1, (tipxy[0], tipxy[1] + 24), tip='finger')
    PH.backpack_cat(c, 210, 1720, .9)
    frame(c, 'giza')

PHOTOS = dict(pisa=pisa, paris=paris, giza=giza, rome=lambda c, f=0: PH.photo(c, f))

if __name__ == '__main__':
    from PIL import Image
    ims = []
    for name, fn in PHOTOS.items():
        S = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(S); fn(c, 0)
        p = os.path.join(HERE, f'_{name}.png'); S.write_to_png(p); ims.append(Image.open(p).convert('RGB').resize((540, 960))); os.remove(p)
    sheet = Image.new('RGB', (540 * 4 + 60, 960 + 40), 'white')
    for i, im in enumerate(ims): sheet.paste(im, (20 + i * 555, 20))
    sheet.save(os.path.join(HERE, 'trip_photos.png')); print('trip_photos.png')
