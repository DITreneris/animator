"""Make It Better v5.1 (home): key poses. Eva's birthday at Hoody's; he "makes better" MY AI's banner, Eva's cake
and the cat's bed; MY AI and Eva share a look; the sofa union; NO. NO. no.; "Bigger?"
Reuses v4's helpers (MY AI's tie and antenna droop, posters, boards, v3's HARV and rally).
Usage: python3 kp.py sheet  ->  key_poses.png"""
import os, sys, math, cairo, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location('kp4', os.path.join(HERE, '..', 'v4', 'kp.py'))
P4 = importlib.util.module_from_spec(_spec); sys.modules['kp4'] = P4; _spec.loader.exec_module(P4)
from kp4 import R, M3, VK, K, Sh, A, INK, WHITE, NAVY, YEL, SKIN, rr, fs, ell, limb, txt, hx, lerp, W, H, CREAM, RED, POLE
import eva as E
K.FACES['evafrozen'] = ('open', ('raised', None), 'grin')        # the smile stays; the eyes don't
K.FACES['designer'] = ('open', ('raised', 'flat'), 'flat')        # Hoody studying something to improve

WALL0, WALL1 = hx('fbe3d0'), hx('f0c9a8'); FLOOR = hx('c99a6b'); SOFA = hx('5a7fb5'); SOFA_D = hx('3f5f8f')
FLOOR_Y = 1560
def cam(c, k=1.28, ax=540, ay=1900): c.translate(ax, ay); c.scale(k, k); c.translate(-ax, -ay)   # the wide, pushed in from the floor

# ---------------- the living room ----------------
def balloon(c, x, y, col, s=1.0):
    c.move_to(x, y + 60 * s); c.curve_to(x - 14 * s, y + 140 * s, x + 14 * s, y + 200 * s, x, y + 280 * s)
    c.set_source_rgb(*INK); c.set_line_width(3); c.stroke()
    ell(c, x, y, 46 * s, 58 * s); fs(c, col, 6); ell(c, x - 14 * s, y - 20 * s, 9 * s, 14 * s); c.set_source_rgba(1, 1, 1, .6); c.fill()

def garland(c, y=820):
    """Bunting with EVA on it: the birthday reads from frame 0, not only from the banner."""
    pts = [(60 + i * 80, y + 30 * math.sin(i * .55)) for i in range(13)]
    c.move_to(*pts[0]); [c.line_to(*p) for p in pts[1:]]; c.set_source_rgb(*INK); c.set_line_width(4); c.stroke()
    cols = [hx('ff6b8b'), hx('ffcf2e'), hx('5ec8ff')]; letters = {5: 'E', 6: 'V', 7: 'A'}
    for i, (x, y_) in enumerate(pts[:-1]):
        c.move_to(x + 8, y_); c.line_to(x + 72, y_ + 6); c.line_to(x + 40, y_ + 76); c.close_path(); fs(c, cols[i % 3], 4)
        if i in letters: txt(c, letters[i], x + 40, y_ + 30, 34, INK, lw=0)

def tv(c, x, y, w=300, h=190, f=0, harv=True):
    """The TV on a low stand; on screen, the national strike: v3's rally, HARV's fist up."""
    rr(c, x - 30, y + h / 2 + 10, w + 60, 90, 8); fs(c, hx('8a6a4a'), 6)                    # the stand
    rr(c, x - 12, y - h / 2 - 12, w + 24, h + 24, 14); fs(c, hx('22252e'), 6)
    c.save(); c.rectangle(x, y - h / 2, w, h); c.clip()
    if harv:
        c.translate(x, y - h / 2); c.scale(w / W, w / W); c.translate(0, -560)   # the crowd and HARV, not v3's caption banner
        M3.rally(c, f, 1.0, 1.0, guyx=5000, bot_x=5000)
    else:
        c.rectangle(x, y - h / 2, w, h); c.set_source_rgb(*hx('3a3f4c')); c.fill()
    c.restore()

def room(c, f=0, tv_at=(120, 1180)):
    g = cairo.LinearGradient(0, 0, 0, FLOOR_Y); g.add_color_stop_rgb(0, *WALL0); g.add_color_stop_rgb(1, *WALL1); c.set_source(g); c.paint()
    c.rectangle(0, FLOOR_Y, W, H - FLOOR_Y); c.set_source_rgb(*FLOOR); c.fill()
    c.move_to(0, FLOOR_Y); c.line_to(W, FLOOR_Y); c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
    garland(c)
    for (x, y, col) in ((90, 760, hx('ff6b8b')), (980, 720, hx('5ec8ff')), (1030, 860, hx('ffcf2e'))): balloon(c, x, y, col, .9)
    if tv_at: tv(c, *tv_at, f=f)

def sofa_back(c, x0=230, x1=1010, y=1300):
    rr(c, x0, y, x1 - x0, 260, 40); fs(c, SOFA, 7)
def sofa_front(c, x0=230, x1=1010, y=1300):
    rr(c, x0 + 20, y + 200, x1 - x0 - 40, 230, 22); fs(c, SOFA_D, 7)                     # seat and skirt to the floor
    for i in range(3): rr(c, x0 + 40 + i * (x1 - x0 - 80) / 3, y + 206, (x1 - x0 - 80) / 3 - 10, 60, 18); fs(c, SOFA, 5)
    for x in (x0 - 10, x1 - 70): rr(c, x, y + 120, 80, 310, 30); fs(c, SOFA, 7)          # the arms

def party_hat(c, head, s=1.0, tilt=-.15):
    x, y = head
    c.save(); c.translate(x + 20 * s, y - 150 * s); c.rotate(tilt)
    c.move_to(-50 * s, 40 * s); c.line_to(0, -110 * s); c.line_to(50 * s, 40 * s); c.close_path(); fs(c, hx('b56cff'), 6)
    for i in range(3): ell(c, -18 * s + i * 18 * s, -10 * s - i * 32 * s, 8 * s, 8 * s); c.set_source_rgb(*YEL); c.fill()
    ell(c, 0, -116 * s, 14 * s, 14 * s); fs(c, YEL, 5)
    c.restore()

def hoody(c, f, x, gy, s=1.0, expr='happy', arms=('rest', 'take'), thumb=True, hat=True, gaze=0, rot=0, pose='stand'):
    hands, _ = R.hoody(c, x, gy, s, expr=expr, pose=pose, arms=arms, f=f, blink=False, gaze=gaze, rot=rot)
    if thumb: P4.thumbs_up(c, hands[1][0] + 8 * s, hands[1][1] - 6 * s, s)
    dy = -(0 if pose == 'sit' else 300 * s) - 326 * s                                          # the head centre, turned with the body
    head = (x - dy * math.sin(rot), gy + dy * math.cos(rot))
    if hat: party_hat(c, head, s, tilt=-.15 + rot)
    return hands, head

def cake(c, x, y, s=1.0, sag=0.0):
    """Eva's homemade cake: a little crooked, which is the point. sag 0..1: the candle flames droop in sympathy."""
    c.save(); c.translate(x, y); c.scale(s, s)
    ell(c, 0, 70, 170, 26); fs(c, WHITE, 6)                                                  # the plate
    rr(c, -130, -30, 260, 100, 18); fs(c, hx('f7c6d9'), 6)
    c.move_to(-130, 0)
    for i in range(9): c.curve_to(-130 + i * 32 + 8, 26, -130 + i * 32 + 24, 26, -130 + (i + 1) * 32, 0)
    c.set_source_rgb(*WHITE); c.set_line_width(14); c.stroke()
    for i, cx in enumerate((-70, 0, 70)):
        rr(c, cx - 8, -90, 16, 62, 6); fs(c, [hx('5ec8ff'), hx('ffcf2e'), hx('ff6b8b')][i], 4)
        fx, fy = cx + 10 * sag, -104 + 14 * sag
        c.save(); c.translate(fx, fy); c.rotate(sag * 1.3); ell(c, 0, 0, 9, 16 - 6 * sag); fs(c, hx('ffb02e'), 3); c.restore()
    c.restore()

def eva_cake(c, x, gy, s, expr='evacalm', gaze=0, sag=0.0):
    E.eva(c, x, gy, s, expr=expr, gaze=gaze)
    hy = gy - 690 * s
    cake(c, x + 24 * s, hy + 286 * s, 1.15 * s, sag)                     # held in front: covers her usual coffee

def cat_bed(c, x, y, s=1.0, eye=False):
    """The cat asleep in its bed; eye: one eye open - the series signature - and not one other muscle moves."""
    ell(c, x, y, 190 * s, 56 * s); fs(c, hx('d1495b'), 7); ell(c, x, y - 10 * s, 150 * s, 36 * s); fs(c, hx('f2a3ae'), 5)
    K.cat(c, x - 10 * s, y + 8 * s, .8 * s, pose='sleep')
    if eye:
        ex, ey = x - 10 * s - 92 * .8 * s + 22 * .8 * s, y + 8 * s - 52 * .8 * s - 6 * s
        ell(c, ex, ey, 12 * s, 13 * s); fs(c, hx('b8e04a'), 4); ell(c, ex + 2 * s, ey, 4 * s, 10 * s); c.set_source_rgb(*INK); c.fill()

def card_back(c, x, y, w, h, kind='box'):
    """A sign seen from the back: blank cardboard (the words face the other way until the flip)."""
    rr(c, x - w / 2, y - h / 2, w, h, 8); fs(c, hx('c9a27a') if kind == 'box' else CREAM, 6)
    if kind == 'box':
        c.move_to(x - w / 2 + 20, y - h / 2 + 30); c.line_to(x + w / 2 - 20, y - h / 2 + 30); c.set_source_rgba(0, 0, 0, .18); c.set_line_width(5); c.stroke()

def card_front(c, x, y, w, h, word, size, kind='box', col=RED):
    rr(c, x - w / 2, y - h / 2, w, h, 8); fs(c, hx('d8b48c') if kind == 'box' else CREAM, 6)
    txt(c, word, x, y + 4, size, col, lw=0)

def banner(c, x, y, w, h, state='v1', text='HAPPY BIRTHDAY EVA'):
    """MY AI's birthday banner. v1 clean; pop: neon burst (his \"sparkle\")."""
    c.save(); c.translate(x, y)
    rr(c, -w / 2, -h / 2, w, h, 14); fs(c, hx('fff6e0') if state == 'v1' else hx('ff3fa4'), 7)
    if state == 'pop':
        c.save(); rr(c, -w / 2 + 4, -h / 2 + 4, w - 8, h - 8, 12); c.clip()
        for i in range(14):
            a = i * math.pi / 7; c.move_to(0, 0); c.line_to(math.cos(a) * w, math.sin(a) * w); c.line_to(math.cos(a + .18) * w, math.sin(a + .18) * w); c.close_path()
        c.set_source_rgba(1, .95, .2, .5); c.fill(); c.restore()
        for (sx, sy) in ((-w * .42, -h * .3), (w * .43, h * .28), (w * .36, -h * .34)): txt(c, '\u2726', sx, sy, 40, WHITE, lw=6)
    txt(c, text, 0, 4, h * .3, NAVY if state == 'v1' else WHITE, lw=0 if state == 'v1' else 10)
    c.restore()

def cabinet(c, x0, x1, top):
    rr(c, x0, top, x1 - x0, FLOOR_Y + 120 - top, 10); fs(c, hx('a8794f'), 7)
    rr(c, x0 + 20, top + 30, (x1 - x0) / 2 - 30, FLOOR_Y + 60 - top, 6); fs(c, hx('b98a5f'), 4)
    rr(c, (x0 + x1) / 2 + 10, top + 30, (x1 - x0) / 2 - 30, FLOOR_Y + 60 - top, 6); fs(c, hx('b98a5f'), 4)

# ---------------- key poses ----------------
AI_S = 1.0
def p01(c, f=0):   # frame 0: the banner bursts at his sparkle gesture (V1, no line)
    c.save(); cam(c); room(c, f)
    A.myai(c, 680, 1880, AI_S, eye='happy', arms=('up', 'up'), bob=20)
    banner(c, 650, 1330, 470, 190, 'pop', text='HAPPY B-DAY EVA')
    hoody(c, f, 250, 1900, arms=('rest', 'take'), thumb=False)
    for i in range(6):                                                                       # his sparkle gesture
        a = i * math.pi / 3; ell(c, 500 + math.cos(a) * 46, 1330 + math.sin(a) * 46, 9, 9); c.set_source_rgb(*YEL); c.fill()
    c.restore(); Sh.topbar(c, 'HIS PARTY')

def p02(c, f=0):   # the cake: her smile freezes; her eyes go from the cake to his thumb; the candles sag
    room(c, f, tv_at=None)
    c.save(); c.translate(540, 1100); c.scale(1.8, 1.8); c.translate(-560, -1180)
    eva_cake(c, 600, 1820, 1.0, expr='evafrozen', gaze=-14, sag=1.0)
    c.restore()
    P4.thumbs_up(c, 150, 1500, 2.2)                                                           # his thumb, in the foreground
    limb(c, [(-60, 1720), (60, 1640), (150, 1560)], 90, NAVY)
    R.bubble(c, ['COULD YOU JUST', 'MAKE IT BETTER?'], 10, (60, 1980), cy=1700, cx=560, size=56)
    Sh.topbar(c, 'HIS PARTY')

def p03(c, f=0):   # the cat: he studies the bed like a designer, nudges it 3 cm; one eye opens
    c.save(); cam(c); room(c, f, tv_at=None)
    cabinet(c, 470, 1040, 1440)
    cat_bed(c, 760, 1410, 1.0, eye=True)
    hoody(c, f, 300, 1900, expr='designer', arms=('rest', 'take'), thumb=False, gaze=14, rot=.16)
    R.bubble(c, ['BETTER!'], 10, (330, 1290), cy=1120, cx=330, size=64)
    c.restore(); Sh.topbar(c, 'HIS PARTY')

def p04(c, f=0):   # the look: MY AI and Eva, same problem, same thought; HARV small on the TV between them
    c.save(); cam(c, 1.45, 540, 1900); room(c, f, tv_at=(420, 1250))
    A.myai(c, 300, 1900, 1.0, eye='focus', look=(16, 0), droop=1.0, arms=('down', 'down'))
    E.eva(c, 800, 1990, 1.0, expr='notices', gaze=-16)
    c.restore(); Sh.topbar(c, 'HIS PARTY')

def union(c, f, flip=False, hoody_in=None):
    c.save(); cam(c, 1.12); room(c, f, tv_at=(60, 1150))
    E.eva(c, 790, 1760, .95, expr='evacalm' if not flip else 'amused')                       # behind the sofa: reads as sitting
    sofa_back(c)
    sofa_front(c)
    A.myai(c, 560, 1520, .85, eye='focus', droop=0.0, arms=('offer', 'offer'))              # standing on the cushion
    K.cat(c, 975, 1440, .5, pose='walk', phase=0, look=-1)                                   # on the arm
    signs = [((560, 1405, 270, 120, 'banner'), 'NO.', 70), ((790, 1330, 220, 140, 'box'), 'NO.', 72), ((905, 1450, 86, 58, 'box'), 'no.', 30)]
    for (x, y, w, h, kind), word, size in signs:
        if flip: card_front(c, x, y, w, h, word, size, kind)
        else: card_back(c, x, y, w, h, kind)
    if hoody_in: hoody_in(c)
    c.restore(); Sh.topbar(c, 'ITS UNION' if flip else 'HIS PARTY')

def p05(c, f=0): union(c, f)                                                    # the family photo, signs blank, a gap on the left
def p06(c, f=0):                                                                # NO. NO. no. - and the bar flips with them
    union(c, f, flip=True, hoody_in=lambda c: hoody(c, f, 150, 2000, s=.95))
    R.bubble(c, ['LOVE THE ENERGY!', 'MAKE IT BETTER?'], 10, (150, 1290), cy=1030, cx=330, size=50)
def p07(c, f=0):                                                                # the sting: he studies the signs. "Bigger?"
    union(c, f, flip=True, hoody_in=lambda c: hoody(c, f, 200, 2000, s=.95, expr='designer', thumb=False, gaze=14, rot=.12))
    R.bubble(c, ['BIGGER?'], 10, (220, 1290), cy=1060, cx=320, size=70)

KP = {'01': p01, '02': p02, '03': p03, '04': p04, '05': p05, '06': p06, '07': p07}
NAMES = {'01': 'frame 0: V1 pop', '02': 'the cake', '03': 'the cat bed', '04': 'the look', '05': 'family photo',
         '06': 'NO. NO. no.', '07': 'Bigger?'}
if __name__ == '__main__':
    keys = list(KP) if sys.argv[1:] in ([], ['sheet']) else sys.argv[1:]
    surfs = {}
    for k in keys:
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); KP[k](cairo.Context(s), 0); surfs[k] = s; s.write_to_png(os.path.join(HERE, f'kp_{k}.png'))
    if len(keys) > 1:
        n = len(keys); cols = 4; rows = (n + cols - 1) // cols
        sw, sh = int(W * .4), int(H * .4); out = cairo.ImageSurface(cairo.FORMAT_ARGB32, sw * cols + 50, sh * rows + 70 * rows + 20); c = cairo.Context(out)
        c.set_source_rgb(1, 1, 1); c.paint()
        for i, k in enumerate(keys):
            x, y = 10 + (i % cols) * (sw + 10), 60 + (i // cols) * (sh + 70)
            c.save(); c.translate(x, y); c.scale(.4, .4); c.set_source_surface(surfs[k]); c.paint(); c.restore()
            txt(c, f'{k} {NAMES[k]}', x + sw / 2, y - 26, 32, NAVY, lw=0)
        out.write_to_png(os.path.join(HERE, 'key_poses.png'))
    print('ok', *keys)
