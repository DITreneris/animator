"""Make It Better v5.2: the 16-shot storyboard (one frame per shot), drawn as shots, not scenes.
The same room and characters as kp.py; each shot is a camera on it: a close-up, a point of view, a low angle.
Usage: python3 sb.py  ->  storyboard.png (+ sb_01.png ..)"""
import os, sys, math, cairo, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import kp as S
from kp import R, K, Sh, A, E, P4, INK, WHITE, NAVY, YEL, SKIN, rr, fs, ell, limb, txt, hx, W, H, RED, CREAM
K.FACES['evahurt'] = ('half', ('worried', 'worried'), 'flat')       # the smile gone, eyes down at the cake
K.FACES['evaproud'] = ('happy', ('raised', 'raised'), 'grin')

def shot(c, cx, cy, k, rot=0.0):
    """A camera on the room: (cx, cy) lands at the frame's centre, k times bigger, tilted rot (radians)."""
    c.translate(540, 1080); c.rotate(rot); c.scale(k, k); c.translate(-cx, -cy)

def heart(c, x, y, s=1.0):
    """Her crooked handmade icing heart."""
    c.save(); c.translate(x, y); c.rotate(.22); c.scale(s, s)
    c.move_to(0, 18); c.curve_to(-34, -6, -22, -34, 0, -16); c.curve_to(20, -36, 38, -4, 4, 20); c.close_path(); fs(c, hx('e8304f'), 4)
    c.restore()

def cake_heart(c, x, gy, s):
    hy = gy - 690 * s; heart(c, x + 20 * s, hy + 296 * s, 1.1 * s)

def eva_cake(c, x=600, gy=1820, s=1.0, expr='evaproud', gaze=0):
    S.eva_cake(c, x, gy, s, expr=expr, gaze=gaze); cake_heart(c, x, gy, s)

def finger(c, tip, s=1.0):
    """Hoody's huge pointing hand from the bottom-left corner, stopping at tip."""
    x, y = tip
    limb(c, [(-200 * s + x * 0, y + 900 * s), (x - 330 * s, y + 380 * s), (x - 120 * s, y + 120 * s)], 150 * s, NAVY)
    c.save(); c.translate(x, y); c.rotate(-.75); c.scale(s, s)
    rr(c, -70, 40, 150, 120, 50); fs(c, SKIN, 7)                                         # the fist
    rr(c, -18, -110, 44, 170, 22); fs(c, SKIN, 7)                                        # the finger
    c.restore()

def hoody_back(c, x, y, s=1.0):
    """Over-the-shoulder: the back of his head (hair, party hat, hood) in the foreground."""
    rr(c, x - 260 * s, y + 120 * s, 520 * s, 400 * s, 120 * s); fs(c, NAVY, 7)
    ell(c, x, y, 190 * s, 180 * s); fs(c, hx('3b2416'), 7)
    for i in range(7): ell(c, x - 150 * s + i * 50 * s, y - 150 * s + abs(i - 3) * 22 * s, 46 * s, 42 * s); fs(c, hx('3b2416'), 5)
    S.party_hat(c, (x, y + 60 * s), s * 1.4, tilt=.2, slip=.6)

ALL = []
def sb(fn): ALL.append(fn); return fn

@sb
def s01(c, f=0):   # CU MY AI: V47 up, antenna drooped, eyes flat; V1 flashes beside it
    S.room(c, f, tv_at=None)
    c.save(); shot(c, 600, 1420, 1.9)
    A.myai(c, 600, 1900, 1.0, eye='focus', arms=('up', 'up'), droop=1.0)
    S.banner(c, 600, 1330, 420, 150, 'v1', text='HAPPY B-DAY EVA'); txt(c, 'V47', 430, 1280, 30, RED, lw=0)
    c.restore()
    c.save(); c.translate(540, 520); c.rotate(.04); c.scale(.85, .85)                         # the flash: V1, identical
    S.banner(c, 0, 0, 420, 150, 'v1', text='HAPPY B-DAY EVA'); txt(c, 'V1', -170, -50, 30, RED, lw=0); c.restore()
    R.bubble(c, ['ACTUALLY, THE FIRST', 'ONE WAS BETTER.'], 10, (-60, 1900), cy=1760, cx=470, size=54)

@sb
def s02(c, f=0):   # MCU Hoody: beaming, hat, thumbs-up
    S.room(c, f)
    c.save(); shot(c, 330, 1450, 2.0); S.hoody(c, f, 300, 1900, slip=.05); c.restore()

@sb
def s03(c, f=0):   # CU the cake: proud, one crooked heart
    S.room(c, f, tv_at=None)
    c.save(); shot(c, 610, 1260, 2.3); eva_cake(c); c.restore()

@sb
def s04(c, f=0):   # MCU Hoody: a forkful, bliss, a sincere thumbs-up
    S.room(c, f)
    c.save(); shot(c, 330, 1450, 2.0)
    hands, _ = S.hoody(c, f, 300, 1900, expr='happy', arms=('chin', 'take'), slip=.25)
    limb(c, [(hands[0][0] + 6, hands[0][1] - 4), (hands[0][0] + 40, hands[0][1] - 60)], 8, hx('c0c4cc'))      # the fork
    ell(c, hands[0][0] + 44, hands[0][1] - 66, 16, 12); fs(c, hx('f7c6d9'), 4)
    c.restore()
    R.bubble(c, ['MMM!'], 10, (560, 900), cy=640, cx=760, size=70)

@sb
def s05(c, f=0):   # Hoody's POV: his finger stops a centimetre from her heart
    S.room(c, f, tv_at=None)
    c.save(); shot(c, 610, 1300, 2.0); eva_cake(c, expr='evaproud'); finger(c, (628, 1214), .5); c.restore()
    R.bubble(c, ['COULD YOU JUST', 'MAKE IT BETTER?'], 10, (120, 1500), cy=560, cx=540, size=56)

@sb
def s06(c, f=0):   # CU Eva: the smile has died; eyes down at the cake. Silence.
    S.room(c, f, tv_at=None)
    c.save(); shot(c, 600, 1180, 3.0); eva_cake(c, expr='evahurt'); c.restore()

@sb
def s07(c, f=0):   # cat level: his hand from above adjusts the cushion; the cat slides
    S.room(c, f, tv_at=None)
    c.save(); shot(c, 760, 1400, 2.4)
    S.cabinet(c, 470, 1040, 1440); S.cat_bed(c, 770, 1410, 1.0, eye=False)
    limb(c, [(980, 700), (930, 1180), (900, 1360)], 60, NAVY); ell(c, 900, 1372, 34, 28); fs(c, SKIN, 6)
    c.restore()
    R.bubble(c, ['BETTER!'], 10, (980, 300), cy=560, cx=640, size=70)

@sb
def s08(c, f=0):   # ECU the cat: one orange eye opens
    S.room(c, f, tv_at=None)
    c.save(); shot(c, 700, 1370, 6.0); S.cabinet(c, 470, 1040, 1440); S.cat_bed(c, 770, 1410, 1.0, eye=True); c.restore()

@sb
def s09(c, f=0):   # CU MY AI: looks at V47, then away; a tired blink
    S.room(c, f, tv_at=None)
    c.save(); shot(c, 560, 1450, 2.6); A.myai(c, 560, 1900, 1.0, eye='blank', look=(-14, 6), droop=1.0, arms=('down', 'down')); c.restore()

@sb
def s10a(c, f=0):  # her eyeline, first: hat... down to his socks (one pink, one blue)... back up
    S.room(c, f)
    c.save(); shot(c, 300, 1820, 3.2); S.hoody(c, f, 300, 1900, slip=.4); c.restore()

@sb
def s10(c, f=0):   # two-shot, matching eyelines: recognition; HARV's fist on the TV behind, an easter egg
    S.room(c, f, tv_at=(430, 1260))
    c.save(); shot(c, 580, 1420, 1.55)
    A.myai(c, 340, 1900, 1.0, eye='open', look=(18, -4), droop=.6, arms=('down', 'down'))
    E.eva(c, 800, 1990, 1.0, expr='notices', gaze=-18, **S.EVA_IN)
    c.restore()

@sb
def s11(c, f=0):   # CU the cat: it looks at them - the third member
    S.room(c, f, tv_at=None)
    c.save(); shot(c, 740, 1360, 3.2); S.cabinet(c, 470, 1040, 1440); K.cat(c, 760, 1440, .8, pose='walk', phase=0, look=-1); c.restore()

def sofa(c, f, flip=False, k=1.25, cy=1450):
    c.save(); shot(c, 620, cy, k); S.union.__wrapped__(c, f, flip) if hasattr(S.union, '__wrapped__') else None; c.restore()

def union_only(c, f, flip):
    """kp.union without its topbar and camera: the room, the sofa, the three and their signs."""
    S.room(c, f, tv_at=(60, 1150))
    E.eva(c, 790, 1760, .95, expr='evacalm' if not flip else 'amused', **S.EVA_IN)
    S.sofa_back(c); S.sofa_front(c)
    A.myai(c, 560, 1520, .85, eye='focus', droop=0.0, arms=('offer', 'offer'))
    K.cat(c, 975, 1440, .5, pose='walk', phase=0, look=-1)
    signs = [((560, 1405, 270, 120, 'banner'), 'NO.', 70), ((790, 1330, 220, 140, 'box'), 'NO.', 72), ((905, 1450, 86, 58, 'box'), 'no.', 30)]
    for (x, y, w, h, kind), word, size in signs:
        (S.card_front(c, x, y, w, h, word, size, kind) if flip else S.card_back(c, x, y, w, h, kind))

@sb
def s12(c, f=0):   # Hoody's POV: the sofa, blank backs, surprisingly organised
    c.save(); shot(c, 640, 1400, 1.45); union_only(c, f, False); c.restore()

@sb
def s13(c, f=0):   # over Hoody's shoulder: "Love the energy! Make it better?"
    c.save(); shot(c, 660, 1380, 1.3); union_only(c, f, False); c.restore()
    hoody_back(c, 170, 1720, 2.0)
    R.bubble(c, ['LOVE THE ENERGY!', 'MAKE IT BETTER?'], 10, (240, 1380), cy=640, cx=480, size=56)

@sb
def s14(c, f=0):   # low angle, straight on: NO. NO. ... no.
    c.save(); shot(c, 660, 1430, 1.55); union_only(c, f, True); c.restore()

@sb
def s15(c, f=0):   # CU Hoody, the Dutch angle (once): the smile held too long, then "Bigger?"
    S.room(c, f)
    c.save(); shot(c, 330, 1420, 2.3, rot=.18); S.hoody(c, f, 300, 1900, expr='happy', thumb=True, slip=1.0); c.restore()
    R.bubble(c, ['BIGGER?'], 10, (560, 1380), cy=1700, cx=640, size=80)

@sb
def s16(c, f=0):   # extreme foreground: MY AI shoves its NO into the lens; the cat's tiny no. beneath
    c.save(); shot(c, 660, 1430, 1.55); union_only(c, f, True); c.restore()
    c.rectangle(0, 0, W, H); c.set_source_rgba(0, 0, 0, .25); c.fill()
    c.save(); c.translate(540, 1060); c.rotate(-.06)
    rr(c, -520, -330, 1040, 600, 20); fs(c, CREAM, 12); txt(c, 'NO.', 0, -20, 330, RED, lw=0)
    c.restore()
    for x in (90, 990): ell(c, x, 1300, 80, 70); fs(c, WHITE, 8)                         # MY AI's mitts on the edges
    S.card_front(c, 760, 1560, 200, 130, 'no.', 70, 'box')

NAMES = ['CU MY AI: V47 = V1', 'Hoody beams', 'the cake, her heart', 'bliss, thumbs-up', 'his finger (POV)', 'her smile dies',
         'cat level: cushion', 'one eye', 'MY AI: tired', 'her eyeline: his socks', 'the look', 'the cat looks', 'his POV: the sofa', 'over his shoulder',
         'NO. NO. no.', 'Dutch: "Bigger?"', 'NO. into the lens']
PILL = ['HIS PARTY'] * 14 + ['ITS UNION'] * 3
if __name__ == '__main__':
    surfs = []
    for i, fn in enumerate(ALL):
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s); fn(c, 0); Sh.topbar(c, PILL[i])
        s.write_to_png(os.path.join(HERE, f'sb_{i + 1:02d}.png')); surfs.append(s)
    cols, k = 9, .25; sw, sh = int(W * k), int(H * k)
    out = cairo.ImageSurface(cairo.FORMAT_ARGB32, cols * (sw + 8) + 8, 2 * (sh + 56) + 10); c = cairo.Context(out); c.set_source_rgb(1, 1, 1); c.paint()
    for i, s in enumerate(surfs):
        x, y = 8 + (i % cols) * (sw + 8), 48 + (i // cols) * (sh + 56)
        c.save(); c.translate(x, y); c.scale(k, k); c.set_source_surface(s); c.paint(); c.restore()
        txt(c, f'{i + 1:02d} {NAMES[i]}', x + sw / 2, y - 20, 20, NAVY, lw=0)
    out.write_to_png(os.path.join(HERE, 'storyboard.png')); print('ok', len(surfs))
