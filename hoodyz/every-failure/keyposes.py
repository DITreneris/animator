"""Every Failure - the 10 key poses (process step 4), one per shot of the concept doc's shot list.
Built on frame0.py's set and rigs (frame 0 is locked). Writes key_01.png ... key_10.png and keys_sheet.png (432 px tiles)."""
import os, sys, math, random, cairo
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import frame0 as F
from frame0 import R, K, E, A, GL, CX0, CX1, W, H, YEL, rock, shadow, success_sign, braced_hoody, sweat, topbar, backdrop, chasm
from kit import INK, WHITE, NAVY, rr, fs, ell, hx, txt, limb
JEANS = R.JEANS
import tails as TL                                    # Perfect Trip's measured tails (on the path through frame0)

HS, HX, AX, EX = .85, 315, 122, 890                  # Hoody scale and x; MY AI x; Eva x (as frame 0)
AS = HS * 1.1
HY = GL - 300 * HS - 326 * HS                         # Hoody's head centre, standing
TEAL = hx('35d0c8')

def ear(x=HX, side=1, dy=30):                         # Hoody standing: 20 px beside the ear, mouth height
    return (x + side * (141 * HS + TL.GAP), HY + dy * HS)

# the bridge: where each failure lands in the chasm (deepest first)
BRIDGE = [('FAIL', 570, GL + 262, 1.15, .82, .04), ('REJECTED', 570, GL + 128, 1.12, .7, -.03),   # v2: every word above y 1600 (dead zone)
          ('BUG', 478, GL + 26, .66, .48, 0), ('404', 665, GL + 26, .66, .48, 0)]       # word, x, y, sx, sy (flat slabs on top), rot
DECK = GL - 6                                                                          # the deck's walking surface: the slabs' tops, lip to lip
def slab(c, x, y, sx, sy, word, rot=0):
    """A rock squashed into a slab (the polygon only; the word stays round): flat-topped deck stones."""
    c.save(); c.translate(x, y); c.rotate(rot)
    c.save(); c.scale(sx, sy)
    pts = [(-150, -60), (-90, -100), (60, -102), (150, -70), (158, 40), (90, 100), (-70, 104), (-150, 60)]
    c.move_to(*pts[0]); [c.line_to(*p) for p in pts[1:]]; c.close_path(); c.restore()
    c.set_source_rgb(*hx('8c8c88')); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(7); c.stroke()
    c.move_to(-120 * sx, 60 * sy); c.line_to(100 * sx, 66 * sy); c.set_source_rgb(*hx('6f6f6b')); c.set_line_width(8); c.stroke()
    txt(c, word, 0, 4, min(70, 64 * sx * 1.4), hx('e03a30'), lw=0); c.restore()
def bridge(c, n=4, gone=(), dust=None):
    for i, (w, x, y, sx, sy, r) in enumerate(BRIDGE[:n]):
        if w in gone: continue
        slab(c, x, y, sx, sy, w, r)
    if n >= 2 and 'REJECTED' not in gone:                                              # rubble jammed between stones and walls: what holds them
        for x, y, r in ((CX0 + 34, GL + 300, 26), (CX1 - 30, GL + 290, 24), (CX0 + 40, GL + 92, 22), (CX1 - 38, GL + 96, 22), (572, GL + 86, 20), (CX0 + 30, GL + 500, 28), (CX1 - 26, GL + 520, 26)):
            ell(c, x, y, r, r * .8); fs(c, hx('8c8c88'), 5)
    if dust is not None:
        x, y = dust
        for k in range(7): ell(c, x - 120 + k * 40, y - 10 - (k % 2) * 16, 30, 18); c.set_source_rgba(*hx('e9c98f'), .8); c.fill()

def particles(c, a, b, n=34, col=TEAL, seed=1):
    """Glowing bits streaming from point a to point b (data, or the sign's gold)."""
    rnd = random.Random(seed)
    for i in range(n):
        t = i / n; x = a[0] + (b[0] - a[0]) * t + rnd.uniform(-26, 26) * math.sin(t * math.pi); y = a[1] + (b[1] - a[1]) * t - 90 * math.sin(t * math.pi) + rnd.uniform(-14, 14)
        z = 22 - 12 * t
        c.rectangle(x - z / 2, y - z / 2, z, z); c.set_source_rgba(*col, .92); c.fill_preserve(); c.set_source_rgba(*INK, .5); c.set_line_width(2); c.stroke()

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

def step_hoody(c, expr, x=HX, foot=(150, -130), gy=GL, lean=None, arms=('rest', 'rest')):
    """Hoody lifting his right foot to step (foot = offset from his hip-side ground point). Leg drawn first, the rig over it with its own right leg clipped away.
    v2: his weight goes onto the standing (left) foot - the whole figure leans back about that foot as the leg rises (lean defaults to the lift)."""
    s = HS
    k = min(1.0, math.hypot(*foot) / 200)
    lean = -.07 * k if lean is None else lean
    pv = (x - 44 * s, gy)                                                             # the standing foot: the pivot
    shadow(c, x - 30, 60, gy)
    c.save(); c.translate(*pv); c.rotate(lean); c.translate(-pv[0], -pv[1])
    waist = gy - 300 * s; hip = (x + 40 * s, waist - 10 * s)
    fx, fy = x + 40 * s + foot[0] * s, gy - 14 * s + foot[1] * s
    knee = ((hip[0] + fx) / 2 + 40 * s, (hip[1] + fy) / 2 - 30 * s)
    limb(c, [hip, knee, (fx, fy)], 40 * s, JEANS)
    c.save(); c.translate(fx + 4 * s, fy + 6 * s); c.rotate(.25); ell(c, 0, 0, 32 * s, 15 * s); fs(c, R._shoe(1), 5); c.restore()
    c.save(); c.rectangle(0, 0, W, H); c.rectangle(x + 4 * s, waist + 30 * s, 400, 600); c.set_fill_rule(cairo.FILL_RULE_EVEN_ODD); c.clip(); c.set_fill_rule(cairo.FILL_RULE_WINDING)   # the clip only; the rig fills as usual
    R.hoody(c, x, gy, s, expr=expr, arms=arms); c.restore()
    c.restore()

def lean_hoody(c, expr, lean=.32, arms=('out', 'out'), x=HX):
    """Hoody bent forward over the lip (the rig cannot bend at the waist: a lean about his feet)."""
    shadow(c, x + 10, 95)
    c.save(); c.translate(x, GL); c.rotate(lean); c.translate(-x, -GL)
    R.hoody(c, x, GL, HS, expr=expr, arms=arms, legs='drag2'); c.restore()

def capsule_pop(c, label, k):
    """The series bar as frame 0 draws it, with only its label capsule swelling (k), from its right end (Perfect Trip v3)."""
    cc = cairo.Context(F.BAR); cc.set_operator(cairo.OPERATOR_CLEAR); cc.paint(); cc.set_operator(cairo.OPERATOR_OVER)
    F.Sh.topbar(cc, label)
    cc.select_font_face('Lilita One'); cc.set_font_size(58); w = max(200, cc.text_extents(label).width + 96); iy = 291
    cc.set_font_size(68); k = 1 if k <= 1 else 1 + (k - 1) * min(1, ((1020 - 274 - cc.text_extents('ME + MY AI').width - 14) / w - 1) / (k - 1))   # never over ME + MY AI (measured)
    cc.save(); cc.translate(1020, iy + 40 * (k - 1)); cc.scale(k, k); rr(cc, -w, -44, w, 88, 44); fs(cc, YEL, 7); txt(cc, label, -w / 2, 0, 58, INK, lw=0); cc.restore()
    c.save(); c.translate(64, 222); c.scale(F.BARK, F.BARK); c.translate(-36, -222); c.set_source_surface(F.BAR, 0, 0); c.paint(); c.restore()

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
    step_hoody(c, 'happy')
    TL.bubble(c, ['SUCCESS!'], 10, ear(), cy=640, cx=600, size=60, bend=-.1)
    topbar(c, 'HIS SUCCESS'); return S

def k04(f=150):  # MY AI hops onto his bent back and springs onto the bridge
    S = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(S)
    scene(c, f); bridge(c, 4); eva(c, 'none', 'notices')                          # her eyes jump to the robot
    step_hoody(c, 'shock')
    bx = 565; shadow(c, bx, 50, DECK)                                                # on the deck, clear of his raised foot
    A.myai(c, bx, DECK, AS, eye='happy', arms=('up', 'down'), walk=.9)               # on Hoody's bridge: first stride onto BUG
    for k in range(3): c.move_to(HX + 60 - k * 10, HY + 120 + k * 34); c.line_to(bx - 120, DECK - 200 + k * 34); c.set_source_rgba(*INK, .7); c.set_line_width(5); c.stroke()   # its path: off his back, down onto the deck
    topbar(c, 'HIS SUCCESS'); return S

def k05(f=210):  # across first: SUCCESS lights, Eva claps for it, MY AI bows; Hoody down on the far lip
    S = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(S)
    global EX
    scene(c, f, sign=1.0); bridge(c, 4)
    ex0 = EX; EX = 975; eva(c, 'clap', 'laugh'); EX = ex0                              # she steps aside for it
    shadow(c, 820, 70); A.myai(c, 820, GL, AS, eye='happy', arms=('down', 'down'), rot=.22)
    shadow(c, HX, 95); R.hoody(c, HX, GL, HS, expr='deadpan', arms=('rest', 'rest'))
    topbar(c, 'HIS SUCCESS'); return S

def k06(f=255):  # his deadpan, close; the label pops HIS -> ITS
    S = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(S)
    R.head_close(c, f, 'deadpan', bgc=('ffd27a', 'fff3d6'), s=2.4, y=1080)
    capsule_pop(c, 'ITS SUCCESS', 1.22)
    return S

def k07(f=315):  # the gold flows into its screen; it hops back and eats the bridge behind it - "Thanks for the training data!"
    S = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(S)
    scene(c, f, sign=.35); bridge(c, 4, gone=('404', 'REJECTED'))
    rx, rgy = 500, DECK; ant = (rx, rgy - 430 * AS)
    particles(c, (665, GL + 20), ant, col=TEAL, seed=2); particles(c, (570, GL + 200), ant, n=24, col=TEAL, seed=3)
    particles(c, (845, 470), (rx, rgy - 288 * AS), n=20, col=YEL, seed=4)
    eva(c, 'none', 'amused')
    shadow(c, HX, 95); R.hoody(c, HX, GL, HS, expr='deadpan', arms=('rest', 'rest'))
    shadow(c, rx, 60, DECK); A.myai(c, rx, rgy, AS, eye='happy', arms=('down', 'down'), talk=.8, walk=2.2, turn=-.5); visor_glow(c, rx, rgy, AS)
    TL.bubble(c, ['THANKS FOR THE', 'TRAINING DATA!'], 10, TL.robot_top(rx, rgy, AS, 1, dx=40), cy=640, cx=600, size=54, bend=.1)
    topbar(c, 'ITS SUCCESS'); return S

def k08(f=390):  # close on the feet: the last rock dissolves under his raised foot
    big = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(big)
    scene(c, f); bridge(c, 3, gone=('REJECTED', 'FAIL'))
    slab(c, 478, GL + 26, .66, .48, 'BUG')
    c.save(); c.rectangle(478, GL - 200, 300, 400); c.clip(); backdrop(c, f); chasm(c); c.restore()   # its right half already gone
    particles(c, (520, GL), (900, GL - 700), n=16, col=TEAL, seed=5)
    step_hoody(c, 'shock', x=330, foot=(150, -40))                                   # his foot over where the stone was
    S = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); cc = cairo.Context(S)
    z = 1.55; cc.translate(540, 1000); cc.scale(z, z); cc.translate(-440, -(GL - 380)); cc.set_source_surface(big, 0, 0); cc.paint()   # legs, foot and stone only
    cc.identity_matrix(); topbar(cc, 'ITS SUCCESS'); return S

def k09(f=450):  # innocent: it hands him a new FAIL - "More?"; Eva urges him on again
    S = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(S)
    scene(c, f); eva(c)
    shadow(c, HX, 95); R.hoody(c, HX, GL, HS, expr='deadpan', arms=('rest', 'rest'))
    ax = AX; shadow(c, ax, 70)
    A.myai(c, ax, GL, AS, eye='happy', arms=('down', 'out') if False else ('down', 'down'), talk=.6)
    rock(c, ax + 70, GL - 190, .55, 'FAIL', rot=-.06, ty=-10)                     # held up at its chest, offered
    TL.bubble(c, ['MORE?'], 10, TL.robot_top(ax, GL, AS, -1, dx=40), cy=560, cx=190, size=60, bend=.05)
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
