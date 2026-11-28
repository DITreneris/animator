"""Every Failure - the 10 key poses (process step 4), one per shot of the concept doc's shot list.
Built on frame0.py's set and rigs (frame 0 is locked). Writes key_01.png ... key_10.png and keys_sheet.png (432 px tiles)."""
import os, sys, math, random, cairo
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import frame0 as F
from frame0 import R, K, E, A, GL, CX0, CX1, W, H, YEL, rock, shadow, success_sign, braced_hoody, sweat, topbar, backdrop, chasm
from kit import INK, WHITE, NAVY, rr, fs, ell, hx, txt, limb
import tails as TL                                    # Perfect Trip's measured tails (on the path through frame0)

HS, HX, AX, EX = .85, 315, 122, 890                  # Hoody scale and x; MY AI x; Eva x (as frame 0)
AS = HS * 1.1
HY = GL - 300 * HS - 326 * HS                         # Hoody's head centre, standing
TEAL = hx('35d0c8')

def ear(x=HX, side=1, dy=30):                         # Hoody standing: 20 px beside the ear, mouth height
    return (x + side * (141 * HS + TL.GAP), HY + dy * HS)

# the bridge: where each failure lands in the chasm (deepest first)
BRIDGE = [('FAIL', 575, GL + 330, .95, .08), ('REJECTED', 560, GL + 140, .78, -.05), ('BUG', 470, GL - 8, .62, .06), ('404', 665, GL - 4, .62, -.07)]
def bridge(c, n=4, gone=(), dust=None):
    for i, (w, x, y, s, r) in enumerate(BRIDGE[:n]):
        if w in gone: continue
        rock(c, x, y, s, w, rot=r, ty=0)
    if dust is not None:
        x, y = dust
        for k in range(7): ell(c, x - 120 + k * 40, y - 10 - (k % 2) * 16, 30, 18); c.set_source_rgba(*hx('e9c98f'), .8); c.fill()

def particles(c, a, b, n=26, col=TEAL, seed=1):
    """Glowing bits streaming from point a to point b (data, or the sign's gold)."""
    rnd = random.Random(seed)
    for i in range(n):
        t = i / n; x = a[0] + (b[0] - a[0]) * t + rnd.uniform(-26, 26) * math.sin(t * math.pi); y = a[1] + (b[1] - a[1]) * t - 90 * math.sin(t * math.pi) + rnd.uniform(-14, 14)
        c.rectangle(x - 7, y - 7, 14, 14); c.set_source_rgba(*col, .85); c.fill()

def scene(c, f=0, sign=0.0):
    backdrop(c, f); chasm(c); rock(c, 60, GL - 34, .4, ''); rock(c, 118, GL - 26, .3, ''); success_sign(c, 845, 470, sign)

def eva(c, mode='urge', expr='evacalm'):
    shadow(c, EX, 70)
    if mode == 'urge': E.eva(c, EX, GL, HS, expr, pose='holdlow', hand_to=(EX - 230 * HS, GL - 600 * HS), leash=False)
    elif mode == 'clap':                                                            # both hands meet in front of her chest, turned to MY AI
        E.eva(c, EX, GL, HS, expr, pose='holdlow', hand_to=(EX + 70 * HS, GL - 560 * HS), leash=False, cup=False)
        for k in (-1, 1): c.move_to(EX + 20 * HS + k * 40, GL - 640 * HS); c.line_to(EX + 30 * HS + k * 60, GL - 690 * HS); c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
    else: E.eva(c, EX, GL, HS, expr, leash=False)

def visor_glow(c, x, gy, s, k=1.0):
    ell(c, x, gy - 288 * s, 110 * s, 74 * s); c.set_source_rgba(*YEL, .3 * k); c.fill()

def lean_hoody(c, expr, lean=.32, arms=('out', 'out'), x=HX):
    """Hoody bent forward over the lip (the rig cannot bend at the waist: a lean about his feet)."""
    shadow(c, x + 10, 95)
    c.save(); c.translate(x, GL); c.rotate(lean); c.translate(-x, -GL)
    R.hoody(c, x, GL, HS, expr=expr, arms=arms, legs='drag2'); c.restore()

def k01(f=0):
    return F.draw(f)[0]

def k02(f=75):  # three rocks drop in rhythm: BUG overhead now, FAIL already wedged below; the antenna blinks with each
    S = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(S)
    scene(c, f); bridge(c, 1, dust=(575, GL + 250)); eva(c)
    shadow(c, AX, 70); A.myai(c, AX, GL, AS, eye='open', look=(14, -12), talk=.7)
    shadow(c, HX + 10, 95)
    c.save(); c.translate(HX, GL); c.rotate(.09); c.translate(-HX, -GL)
    rc = (HX + 10, GL - 300 * HS - 326 * HS - 200 * HS); rock(c, rc[0], rc[1], 1.25 * HS * .85, 'BUG', rot=.05, ty=-30)
    braced_hoody(c, HX, HS, f, rc, 1.25 * HS * .85, .09); sweat(c, HX + 150 * HS, HY - 20 * HS, HS); c.restore()
    TL.bubble(c, ['...BUILDS SUCCESS!'], 10, ear(), cy=1010, cx=650, size=52, bend=-.1)
    topbar(c, 'HIS SUCCESS'); return S

def k03(f=120):  # the last rock lands: the bridge is whole; he pushes it into place - "SUCCESS!"
    S = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(S)
    scene(c, f); bridge(c, 4, dust=(665, GL - 40)); eva(c, 'urge', 'charmed')
    shadow(c, AX, 70); A.myai(c, AX, GL, AS, eye='focus', look=(14, 0))
    lean_hoody(c, 'happy', .30, arms=('down', 'down'))
    TL.bubble(c, ['SUCCESS!'], 10, (HX + 250, HY - 40), cy=640, cx=560, size=60, bend=-.1)
    topbar(c, 'HIS SUCCESS'); return S

def k04(f=150):  # MY AI hops onto his bent back and springs onto the bridge
    S = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(S)
    scene(c, f); bridge(c, 4); eva(c, 'none', 'notices')                          # her eyes jump to the robot
    lean_hoody(c, 'shock', .36, arms=('down', 'down'))
    bx, by = HX + 330, GL - 300                                                     # sprung off his back: in the air over the bridge
    A.myai(c, bx, by, AS, eye='happy', arms=('up', 'up'), rot=.25)
    for k in range(3): c.move_to(bx - 40 - k * 26, by + 20 + k * 26); c.line_to(bx - 10 - k * 26, by - 10 + k * 26); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()   # speed lines from its feet, off his face
    topbar(c, 'HIS SUCCESS'); return S

def k05(f=210):  # across first: SUCCESS lights, Eva claps for it, MY AI bows; Hoody down on the far lip
    S = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(S)
    scene(c, f, sign=1.0); bridge(c, 4); eva(c, 'clap', 'laugh')
    A.myai(c, 575, GL - 40, AS, eye='happy', arms=('down', 'down'), rot=.35)
    shadow(c, HX, 95); R.hoody(c, HX, GL, HS, expr='deadpan', arms=('rest', 'rest'))
    topbar(c, 'HIS SUCCESS'); return S

def k06(f=255):  # his deadpan, close; the label pops HIS -> ITS
    S = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(S)
    R.head_close(c, f, 'deadpan', bgc=('ffd27a', 'fff3d6'), s=2.4, y=1080)
    topbar(c, 'ITS SUCCESS')
    c.save(); c.translate(540, 300); c.scale(1.2, 1.2)                              # the pop, big for half a second
    rr(c, -300, -60, 600, 120, 60); fs(c, YEL, 8); txt(c, 'ITS SUCCESS', 0, 2, 78, INK, lw=0); c.restore()
    return S

def k07(f=315):  # the gold flows into its screen; it hops back and eats the bridge behind it - "Thanks for the training data!"
    S = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(S)
    scene(c, f, sign=.35); bridge(c, 4, gone=('404', 'REJECTED'))
    particles(c, (665, GL - 20), (560, GL - 470), col=TEAL, seed=2); particles(c, (590, GL + 160), (560, GL - 470), n=18, col=TEAL, seed=3)
    particles(c, (845, 470), (560, GL - 330), n=20, col=YEL, seed=4)
    eva(c, 'none', 'amused')
    shadow(c, HX, 95); R.hoody(c, HX, GL, HS, expr='deadpan', arms=('rest', 'rest'))
    A.myai(c, 560, GL - 120, AS, eye='happy', arms=('up', 'down'), talk=.8); visor_glow(c, 560, GL - 120, AS)
    TL.bubble(c, ['THANKS FOR THE', 'TRAINING DATA!'], 10, TL.robot_top(560, GL - 120, AS, 1, dx=40), cy=640, cx=560, size=54, bend=.1)
    topbar(c, 'ITS SUCCESS'); return S

def k08(f=390):  # close on the feet: the last rock dissolves under his raised foot
    big = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(big)
    scene(c, f); bridge(c, 3, gone=('REJECTED', 'FAIL'))
    rock(c, 430, GL + 6, .55, 'BUG', rot=.06, ty=0)
    particles(c, (430, GL), (400, GL - 700), n=14, col=TEAL, seed=5)
    hx2 = 430 - 40 * HS; shadow(c, hx2 - 30, 60); R.hoody(c, hx2, GL - 40, HS, expr='shock', arms=('rest', 'rest'), step=math.pi)   # right foot lifted over the rock
    S = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); cc = cairo.Context(S)
    z = 2.2; cc.translate(540, 1100); cc.scale(z, z); cc.translate(-420, -GL + 120); cc.set_source_surface(big, 0, 0); cc.paint()
    cc.identity_matrix(); topbar(cc, 'ITS SUCCESS'); return S

def k09(f=450):  # innocent: it hands him a new FAIL - "More?"; Eva urges him on again
    S = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(S)
    scene(c, f); eva(c)
    shadow(c, HX, 95); R.hoody(c, HX, GL, HS, expr='deadpan', arms=('rest', 'rest'))
    ax = AX; shadow(c, ax, 70)
    A.myai(c, ax, GL, AS, eye='happy', arms=('down', 'out') if False else ('down', 'down'), talk=.6)
    rock(c, ax + 150, GL - 330, .7, 'FAIL', rot=-.06, ty=-20)                     # offered up to his chest
    TL.bubble(c, ['MORE?'], 10, TL.robot_side(ax, GL, AS, 1), cy=1080, cx=560, size=60, bend=.1)
    topbar(c, 'ITS SUCCESS'); return S

def k10(f=539):
    return F.draw(f)[0]

KEYS = [k01, k02, k03, k04, k05, k06, k07, k08, k09, k10]
TIMES = ['0,0 s', '2,5 s', '4,0 s', '5,2 s', '7,0 s', '8,5 s', '10,5 s', '13,0 s', '15,0 s', '17,9 s']

if __name__ == '__main__':
    from PIL import Image, ImageDraw
    tiles = []
    for i, fn in enumerate(KEYS):
        p = os.path.join(HERE, f'key_{i + 1:02d}.png'); fn().write_to_png(p); tiles.append(p)
    tw, th = 432, 768
    sheet = Image.new('RGB', (tw * 5, (th + 30) * 2), (25, 25, 25)); d = ImageDraw.Draw(sheet)
    for i, p in enumerate(tiles):
        x, y = (i % 5) * tw, (i // 5) * (th + 30)
        sheet.paste(Image.open(p).convert('RGB').resize((tw, th)), (x, y + 30)); d.text((x + 6, y + 8), f'{i + 1}  {TIMES[i]}', fill=(255, 255, 0))
    sheet.save(os.path.join(HERE, 'keys_sheet.png')); print('keys_sheet.png')
