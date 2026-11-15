"""Perfect Trip - the album, v4: Hoody loses his ROLE, not just his size.
PISA hero -> PARIS extra -> GIZA assistant -> ROME cameraman. Eva's attention moves to MY AI (bored, surprised, delighted,
holding its hand); the cat in the backpack knows first (suspicious, shocked, disapproving, resigned).
Then the reveal: the Rome photo is on the phone in Hoody's hands. python3 trip_photos.py writes trip_photos.png."""
import os, sys, math, cairo
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import photo as PH                     # shared helpers (ledge, backpack) and Perfect Date's characters through it
import places as P
from photo import R, K, Sh, E, A
from kit import INK, WHITE, NAVY, rr, fs, ell, limb, hx, txt, lerp
W, H = 1080, 1920
CAMEL, CAMEL_D = hx('c8955a'), hx('a8763f')
K.FACES['bored'] = ('half', ('flat', 'flat'), 'meh')

# ---------------- shared pieces
def frame(c, place, label='HIS TRIP'):
    P.stamp(c, place)
    c.rectangle(0, 0, W, H); c.rectangle(34, 34, W - 68, H - 68); c.set_fill_rule(cairo.FILL_RULE_EVEN_ODD); c.set_source_rgb(*WHITE); c.fill()
    c.set_fill_rule(cairo.FILL_RULE_WINDING)
    Sh.topbar(c, label)

def backpack_cat(c, x, y, s=.9, mood='suspicious'):
    """Hoody's red backpack, bottom left of every photo, the cat's head out of it. She understands before he does:
    suspicious (one eye, a lowered brow) -> shocked (both eyes round) -> disapproving (slits, brows down) -> resigned (half lids)."""
    c.save(); c.translate(x, y); c.scale(s, s)
    rr(c, -150, -10, 300, 260, 50); fs(c, hx('d9533f'), 7)
    rr(c, -150, -10, 300, 70, 30); fs(c, hx('b8412f'), 6)
    c.move_to(-150, 120); c.line_to(150, 120); c.set_source_rgb(*hx('8f2f22')); c.set_line_width(5); c.stroke()
    hs = 1.5; c.save(); c.translate(0, -40)
    if mood == 'shocked': c.translate(0, -26)                                # she sits up
    K._cat_head(c, 0, 0, hs, False, 'sleep', 0)
    c.scale(hs, hs)
    for q in (-1, 1):
        ex, ey = q * 24 + 4, -3
        ell(c, ex, ey, 15, 16); c.set_source_rgb(*K.TABBY); c.fill()         # clear the sleeping eye
        if mood == 'suspicious' and q == -1:
            c.arc(ex, ey + 1, 11, .2, math.pi - .2); c.set_source_rgb(*INK); c.set_line_width(5); c.stroke(); continue
        h = {'suspicious': 8, 'shocked': 15, 'disapproving': 4, 'resigned': 7}[mood]
        ell(c, ex, ey, 12 if mood == 'shocked' else 11, h); fs(c, hx('b8e04a'), 3)
        ell(c, ex + 1, ey, 3 if mood == 'shocked' else 4, min(h - 2, 9)); c.set_source_rgb(*INK); c.fill()
        if mood in ('resigned', 'suspicious'):                               # a heavy upper lid
            c.rectangle(ex - 14, ey - 18, 28, 14 if mood == 'resigned' else 10); c.set_source_rgb(*K.TABBY); c.fill()
            c.move_to(ex - 13, ey - 4 - (0 if mood == 'resigned' else 4)); c.line_to(ex + 13, ey - 4 - (0 if mood == 'resigned' else 4))
            c.set_source_rgb(*INK); c.set_line_width(4); c.stroke()
        if mood in ('disapproving', 'suspicious'):                           # brows down towards the middle
            c.move_to(ex - q * 14, ey - 22); c.line_to(ex + q * 10, ey - 14); c.set_source_rgb(*INK); c.set_line_width(4); c.stroke()
    c.restore()
    rr(c, -160, 20, 320, 40, 16); fs(c, hx('b8412f'), 6)
    c.restore()

def camel(c, x, gy, s, f=0, pull=0):
    """A camel facing left; pull leans its neck away (it won't budge)."""
    c.save(); c.translate(x, gy); c.scale(s, s)
    for k, lx in enumerate((-90, -60, 70, 100)): limb(c, [(lx, -230), (lx + 4, -120), (lx + (14 if k < 2 else -6), 0)], 26, CAMEL_D if k % 2 else CAMEL)
    ell(c, 0, -260, 150, 70); fs(c, CAMEL, 7)
    c.move_to(-70, -300); c.curve_to(-40, -420, 60, -420, 80, -300); c.close_path(); fs(c, CAMEL, 7)
    limb(c, [(-120, -270), (-190 + pull, -360), (-200 + pull * 1.5, -470)], 46, CAMEL)
    ell(c, -230 + pull * 1.5, -480, 62, 34); fs(c, CAMEL, 6); ell(c, -258 + pull * 1.5, -492, 7, 7); c.set_source_rgb(*INK); c.fill()
    c.move_to(150, -270); c.curve_to(190, -240, 180, -190, 170, -160); c.set_source_rgb(*INK); c.set_line_width(8); c.stroke()
    c.restore()
    return (x + (-200 + pull * 1.5) * s, gy - 470 * s)                         # where the rope ties (its head)

def suitcase(c, x, y, w, h, col):
    rr(c, x - w / 2, y - h, w, h, 14); fs(c, hx(col), 6)
    rr(c, x - w * .2, y - h - 22, w * .4, 26, 10); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    c.move_to(x - w / 2 + 10, y - h * .5); c.line_to(x + w / 2 - 10, y - h * .5); c.set_line_width(4); c.stroke()

def tele_arm(c, rx, gy, rs, q, target, tip='finger'):
    """MY AI's telescopic arm: nested white sections from its shoulder to a target. tip: 'finger' or 'palm' (up)."""
    sh = (rx + q * A.SHOULDER[0] * rs, gy - 280 * rs + A.SHOULDER[1] * rs)
    dx, dy = target[0] - sh[0], target[1] - sh[1]; L = math.hypot(dx, dy); ang = math.atan2(dy, dx)
    c.save(); c.translate(*sh); c.rotate(ang)
    for k, w in enumerate((26, 21, 17)):
        a, b = L * k / 3 - (6 if k else 0), L * (k + 1) / 3
        rr(c, a, -w * rs / 1.2, b - a, w * rs / .6, w * rs / 1.2); fs(c, WHITE, max(4, 6 * rs / 1.4))
        if k: ell(c, a + 4, 0, 6 * rs, w * rs / 1.1); fs(c, A.CHEST, 3)
    c.restore()
    if tip == 'finger':
        ell(c, target[0], target[1] + 20 * rs, 21 * rs, 19 * rs); fs(c, WHITE, 6)
        rr(c, target[0] - 7 * rs, target[1] - 4 * rs, 14 * rs, 26 * rs, 7 * rs); fs(c, WHITE, 5)
    else:
        ell(c, target[0], target[1] + 12 * rs, 30 * rs, 14 * rs); fs(c, WHITE, 6)
    ell(c, *sh, 20 * rs, 20 * rs); fs(c, WHITE, 6)

# ---------------- the four photos
PISA_AI = (935, 1580, .8)
def pisa_overhang(lean):
    """Under the leaning side, near the top: where MY AI's palm holds it up."""
    y = 600; return (640 + math.tan(math.radians(lean)) * (P.GY - 60 - y) + 118, y)
def pisa(c, f=0, k=1.0, hoody_a=1.0, photo=True):
    """HERO. Hoody, in front, proudly does the classic pose. MY AI, behind him at the right, puts a telescopic palm under
    the overhang and the tower straightens a little: it holds it up better. Eva bored. The cat suspicious.
    k: how far the arm has gone up (the tower straightens with it); hoody_a: how far into his pose he is."""
    lean = 8 - 2 * k
    P.pisa(c, f, lean=lean)
    rx, rgy, rs = PISA_AI
    A.myai(c, rx, rgy, rs, eye='happy' if k >= 1 else 'focus', arms=(None if k > 0 else 'down', 'hip'), tilt=-8)
    if k > 0:
        sh = (rx - 72 * rs, rgy - 280 * rs + 112 * rs); tgt = pisa_overhang(lean)
        tele_arm(c, rx, rgy, rs, -1, (lerp(sh[0] - 30, tgt[0], k), lerp(sh[1] - 50, tgt[1] + 16, k)), tip='palm')
    E.eva(c, 150, 1880, .92, 'bored', sip=.5, gaze=-14)
    R.hoody(c, 720, 1830, 1.05, expr='happy', arms=('out' if hoody_a > .5 else 'rest', 'rest'), rot=-.06 * hoody_a, f=f)
    backpack_cat(c, 210, 1720, .9, 'suspicious')
    if photo: frame(c, 'pisa')

def paris(c, f=0):
    """EXTRA. MY AI in front with the spire on its fingertip; Eva turned to it, surprised. Hoody small at the left, whole and annoyed."""
    rx, rgy, rs, hz = 900, 1760, 1.25, 1640
    tipxy = (500, 760)
    s = ((hz - 10) - tipxy[1]) / 1370
    P.paris(c, f, s=s, cx0=tipxy[0], horizon=hz)
    R.hoody(c, 200, hz + 40, .5, expr='bored', arms=('rest', 'rest'), gaze=24, f=f)   # an extra in his own trip, glaring at the robot
    E.eva(c, 400, 1900, .9, 'impressed', sip=.2, gaze=18)
    A.myai(c, rx, rgy, rs, eye='focus', arms=(None, 'down'), tilt=-4)
    tele_arm(c, rx, rgy, rs, -1, (tipxy[0], tipxy[1] + 26), tip='finger')
    backpack_cat(c, 210, 1720, .9, 'shocked')
    frame(c, 'paris')

def giza(c, f=0):
    """ASSISTANT. MY AI and Eva pose together, delighted. Behind them Hoody drags the luggage and the camel won't budge."""
    P.egypt(c, f, s=.72, cx0=600, horizon=1460)
    rope_to = camel(c, 150, 1500, .42, f, pull=20)
    for (x, y, w, h, col, a) in ((250, 1530, 110, 80, '3f7fd6', 0), (262, 1450, 84, 62, 'e8b23a', .25), (330, 1530, 70, 110, '5aa84f', 0)):
        c.save(); c.translate(x, y); c.rotate(a); suitcase(c, 0, 0, w, h, col); c.restore()      # the luggage, stacked, the top one sliding
    hands, _ = R.hoody(c, 400, 1530, .52, expr='wince', arms=('out', 'down'), rot=.3, f=f)     # leaning far back: the camel won't come
    Sh.sweat(c, 450, 1260, .7)
    c.move_to(*hands[0]); c.line_to(*rope_to); c.set_source_rgb(*hx('8a5a2e')); c.set_line_width(5); c.stroke()
    A.myai(c, 700, 1860, 1.3, eye='happy', arms=('wave', 'hold'), tilt=10)
    hp = A.hand_at(700, 1860, 1.3, 1, 'hold')
    E.eva(c, 900, 1880, 1.0, 'laugh', sip=.1, tilt=-.2, pose='holdlow', hand_to=hp)
    backpack_cat(c, 210, 1720, .9, 'disapproving')
    frame(c, 'giza')

def rome(c, f=0, label='ITS TRIP', stamp=True):
    """CAMERAMAN, part 1: the couple photo. Eva holding MY AI's hand on the ledge before the Colosseum. No Hoody at all."""
    P.rome(c, f, s=.62, cx=540, horizon=1230)
    TOP = 1520
    PH.ledge(c, 200, 1000, TOP)
    es, ex = 1.05, 650
    rx, rs = 450, 1.32
    hp = A.hand_at(rx, TOP - 6, rs, 1, 'hold')
    c.save(); c.rectangle(0, 0, W, TOP + 6); c.clip()
    E.eva(c, ex, TOP + 250 * es, es, 'charmed', sip=.1, tilt=-.34, pose='holdlow', hand_to=hp); c.restore()
    for q in (-1, 1):
        limb(c, [(ex + q * 34 * es, TOP + 4), (ex + q * 38 * es, TOP + 200)], 32 * es, E.TROUS)
        ell(c, ex + q * 34 * es, TOP + 6, 36 * es, 26 * es); fs(c, E.TROUS, 5)
        ell(c, ex + q * 42 * es, TOP + 206, 30 * es, 14 * es); fs(c, E.SHOE, 4)
    A.myai(c, rx, TOP - 6, rs, eye='happy', arms=('wave', 'hold'), tilt=8)
    ell(c, *hp, 20 * es, 18 * es); fs(c, E.SKIN_E, 4)
    backpack_cat(c, 210, 1720, .9, 'resigned')
    if stamp: P.stamp(c, 'rome')
    c.rectangle(0, 0, W, H); c.rectangle(34, 34, W - 68, H - 68); c.set_fill_rule(cairo.FILL_RULE_EVEN_ODD); c.set_source_rgb(*WHITE); c.fill()
    c.set_fill_rule(cairo.FILL_RULE_WINDING)
    Sh.topbar(c, label)

_ROME = None
def rome_reveal(c, f=0):
    """CAMERAMAN, part 2: pull back - on the phone in Hoody's hands, a tight couple portrait; over it, his flat, exhausted
    stare. MY AI, at the right, thanks him."""
    global _ROME
    if _ROME is None:                                                      # the couple alone: no bar, no stamp, no cat, no border
        _ROME = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); cc = cairo.Context(_ROME)
        P.rome(cc, 0, s=.62, cx=540, horizon=1230)
        TOP = 1520; PH.ledge(cc, 200, 1000, TOP); es, ex = 1.05, 650; rx, rs = 450, 1.32
        hp = A.hand_at(rx, TOP - 6, rs, 1, 'hold')
        cc.save(); cc.rectangle(0, 0, W, TOP + 6); cc.clip()
        E.eva(cc, ex, TOP + 250 * es, es, 'charmed', sip=.1, tilt=-.34, pose='holdlow', hand_to=hp); cc.restore()
        A.myai(cc, rx, TOP - 6, rs, eye='happy', arms=('wave', 'hold'), tilt=8); ell(cc, *hp, 20 * es, 18 * es); fs(cc, E.SKIN_E, 4)
    P.rome(c, f, s=.62, cx=540, horizon=1230)
    K.hoodie(c, 400, 1020 + 150 * 2.1, 2.1 * 1.1)
    K.hoodyz_head(c, 400, 1020, 2.1, era='young', expr='bored', blink=False, gaze=0)
    px, py, pw, ph = 150, 1080, 500, 800                                   # the phone
    rr(c, px - 18, py - 18, pw + 36, ph + 36, 60); fs(c, hx('1d2130'), 8)
    c.save(); rr(c, px, py, pw, ph, 44); c.clip()
    cx0, cy0, cw = 210, 820, 720                                           # crop: the couple, close
    k = pw / cw; c.translate(px, py); c.scale(k, k); c.translate(-cx0, -cy0); c.set_source_surface(_ROME, 0, 0); c.paint(); c.restore()
    for q, hy_ in ((-1, 1620), (1, 1560)):
        hx_ = px - 8 if q < 0 else px + pw + 8
        limb(c, [(hx_ + q * 120, 1960), (hx_ + q * 40, hy_ + 80), (hx_, hy_)], 70, NAVY)
        ell(c, hx_, hy_, 44, 52); fs(c, K.SKIN, 6)
    rx, rgy, rs = 900, 1640, 1.05
    A.myai(c, rx, rgy, rs, eye='happy', arms=('down', 'wave'), tilt=-8)
    PH.R.bubble(c, ['THANKS FOR', 'THE PHOTOS!'], 10, (rx, rgy - 420 * rs), cy=780, cx=820, size=56)
    Sh.topbar(c, 'ITS TRIP')

PHOTOS = dict(pisa=pisa, paris=paris, giza=giza, rome=rome, reveal=rome_reveal)

if __name__ == '__main__':
    from PIL import Image
    ims = []
    for name, fn in PHOTOS.items():
        S = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(S); fn(c, 0)
        p = os.path.join(HERE, f'_{name}.png'); S.write_to_png(p); ims.append(Image.open(p).convert('RGB').resize((432, 768))); os.remove(p)
    sheet = Image.new('RGB', (432 * 5 + 72, 768 + 40), 'white')
    for i, im in enumerate(ims): sheet.paste(im, (12 + i * 444, 20))
    sheet.save(os.path.join(HERE, 'trip_photos.png')); print('trip_photos.png')
