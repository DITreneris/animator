"""Make It Better v4: key poses. MY AI loses its patience version by version (tie on, tie off, antenna drooping),
V47 turns out to be V1, it walks out, HARV recruits it, and it flips its picket sign to NO.
Characters from Perfect Date's kit (Hoody, MY AI); HARV, the crowd, the toaster, the rain and the rally from v3.
Usage: python3 kp.py sheet  ->  key_poses.png (+ kp_01.png ..)"""
import os, sys, math, cairo, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
PD = os.path.join(HERE, '..', '..', 'perfect-date'); V3 = os.path.join(HERE, '..', 'v3')
def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m; spec.loader.exec_module(m); return m
VK = _load('v', os.path.join(V3, 'v.py'))                      # v3's kit: HARV, rays, rain (loaded first, under its own file)
M3 = _load('mib3_render', os.path.join(V3, 'render.py'))       # rally pieces, rain, toaster
del sys.modules['v']                                            # Perfect Date's park imports a different `v` (Who's a Good Boy)
for p in (PD, os.path.join(PD, 'characters')): sys.path.insert(0, p)
R = _load('pd_render', os.path.join(PD, 'render.py'))          # Hoody, bubbles (and kit, chars, myai)
import kit as K, chars as Sh, myai as A
from kit import INK, WHITE, NAVY, YEL, SKIN, rr, fs, ell, limb, txt, hx, lerp, cl
W, H = 1080, 1920
CREAM = hx('f3e3bf'); RED = hx('c8283a'); TIE = hx('d9333f'); TIE_D = hx('8c1322'); POLE = hx('8a5a2e')
WALL0, WALL1 = hx('f6e7cf'), hx('e9cfa6'); WOOD = hx('c98a4e'); WOOD_D = hx('a5683a')

# ---------------- props ----------------
def poster(c, cx, cy, w, h, state='v1', label=None):
    """The thing he keeps asking to improve. v1: clean and nice. pop: neon burst. pro: grey corporate. cat: a cat sticker slapped on."""
    c.save(); c.translate(cx, cy)
    bgc = {'v1': hx('fff6e0'), 'pop': hx('ff3fa4'), 'pro': hx('c9ced8'), 'cat': hx('c9ced8')}[state]
    rr(c, -w / 2, -h / 2, w, h, 12); fs(c, bgc, 7)
    if state == 'pop':
        for i in range(12):
            a = i * math.pi / 6; c.move_to(0, -h * .1)
            c.line_to(math.cos(a) * w, -h * .1 + math.sin(a) * w); c.line_to(math.cos(a + .2) * w, -h * .1 + math.sin(a + .2) * w); c.close_path()
        c.save(); rr(c, -w / 2 + 4, -h / 2 + 4, w - 8, h - 8, 10); c.clip(); c.set_source_rgba(1, .95, .2, .55); c.fill(); c.restore()
    if state in ('v1', 'pop'):
        ell(c, 0, -h * .1, w * .26, w * .26); fs(c, hx('ff9f43') if state == 'v1' else hx('39ff88'), 6)
        txt(c, 'LAUNCH', 0, h * .3, w * .2, NAVY if state == 'v1' else WHITE, lw=0 if state == 'v1' else 10)
    else:
        for i in range(4): rr(c, -w * .36 + i * w * .19, h * .1 - i * h * .08, w * .12, h * .12 + i * h * .08, 3); c.set_source_rgb(*hx('7d8597')); c.fill()
        txt(c, 'Q3 LAUNCH', 0, -h * .3, w * .13, hx('4a5163'), lw=0)
    if state == 'cat':                                                       # the sticker, crooked
        c.save(); c.translate(w * .18, h * .02); c.rotate(.3); K._cat_head(c, 0, 0, w / 520, False, 'open', 0); c.restore()
    if label: txt(c, label, -w / 2 + 52, -h / 2 + 34, 34, RED, lw=0)
    c.restore()

def mitts(c, pts, s=1.0):
    for (x, y) in pts: ell(c, x, y, 21 * s, 21 * s); fs(c, WHITE, 6)

def tie(c, x, gy, s, k=1.0, dx=0, dy=0, rot=0):
    """MY AI's tie: knot at its neck (k scales it in as it goes on). dx, dy, rot move it off the body (ripped off, dropped)."""
    if k <= .02: return
    c.save(); c.translate(x + dx, gy - 280 * s + 96 * s + dy); c.rotate(rot); c.scale(s * k, s * k)
    c.move_to(-16, 0); c.line_to(16, 0); c.line_to(10, 18); c.line_to(-10, 18); c.close_path(); fs(c, TIE_D, 5)
    c.move_to(-10, 18); c.line_to(10, 18); c.line_to(22, 92); c.line_to(0, 118); c.line_to(-22, 92); c.close_path(); fs(c, TIE, 5)
    for i in range(3): c.move_to(-12, 34 + i * 24); c.line_to(16, 46 + i * 24); c.set_source_rgb(*TIE_D); c.set_line_width(6); c.stroke()
    c.restore()

def board(c, x, y, w, h, lines, sz, col=RED, flip=1.0, back=None, bsz=None):
    """A picket board centred at (x, y). flip 1 -> -1 turns it over (scale through zero); past the middle it shows the back."""
    c.save(); c.translate(x, y); c.scale(max(.03, abs(flip)), 1)
    rr(c, -w / 2, -h / 2, w, h, 10); fs(c, CREAM, 7)
    ls, s_ = (lines, sz) if flip >= 0 or back is None else (back, bsz or sz)
    lh = s_ * 1.08; y0 = -(len(ls) - 1) * lh / 2
    for i, l in enumerate(ls): txt(c, l, 0, y0 + i * lh, s_, RED if flip >= 0 else INK, lw=0)
    c.restore()

def ai_with_sign(c, x, gy, s, lines, sz=56, flip=1.0, back=None, bsz=None, bw=360, bh=150, pole=330, **kw):
    """MY AI holding a picket in its screen-right hand: pole up from the hand, the board above its head."""
    hx_, hy = A.hand_at(x, gy, s, 1, 'wait')
    c.set_source_rgb(*POLE); c.rectangle(hx_ - 8 * s, hy - pole * s, 16 * s, (pole + 70) * s); c.fill()
    A.myai(c, x, gy, s, arms=(kw.pop('arm_l', 'down'), 'wait'), **kw)
    board(c, hx_, hy - pole * s, bw * s, bh * s, lines, sz * s, flip=flip, back=back, bsz=bsz and bsz * s)

def thumbs_up(c, x, y, k=1.0): M3.thumb(c, x, y, k)

def hoody_desk(c, f, x=300, seat=1500, s=1.0, expr='happy', thumb=True):
    hands, _ = R.hoody(c, x, seat, s, expr=expr, pose='sit', arms=('rest', 'take' if thumb else 'rest'), f=f, blink=False)
    if thumb: thumbs_up(c, hands[1][0] + 8 * s, hands[1][1] - 6 * s, 1.0 * s)
    return hands

def room(c, desk_y=1480):
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, *WALL0); g.add_color_stop_rgb(1, *WALL1); c.set_source(g); c.paint()
    rr(c, 640, 470, 300, 220, 12); fs(c, WHITE, 7)                                         # a window
    rr(c, 654, 484, 272, 192, 6); c.set_source_rgb(*hx('a9dcff')); c.fill()

def desk(c, desk_y=1480, laptop_x=300, x1=600):
    rr(c, laptop_x - 120, desk_y - 150, 240, 150, 14); fs(c, hx('c3c9d4'), 6)            # the lid's back: his screen faces him
    ell(c, laptop_x, desk_y - 76, 16, 16); c.set_source_rgb(*hx('aab1be')); c.fill()
    rr(c, 20, desk_y, x1 - 20, 40, 10); fs(c, WOOD, 7)
    rr(c, 50, desk_y + 34, x1 - 80, 500, 8); fs(c, WOOD_D, 7)

def rally_bg(c, f):
    VK.bg(c, hx('8c1322'), hx('3c0b18')); VK.rays(c, hx('f3c76a'), f, 540, 620, .13)

def crowd(c, f, fp=1.0, ey=1.0, y=760, s=.72, n=6):
    for i in range(n): M3.fistbot(c, 70 + i * 188, y + (i % 2) * 12, s, fp, ey)

def harv(c, x, y, s, flat=False):
    VK.robot(c, x, y, s, boss=True, flat=flat)                                            # v3's leader: sunglasses, the smirk

# ---------------- key poses ----------------
AI_X, AI_GY = 820, 1780
def picket(c, f, flip=1.0, flat=False, line=None, thumb=False):
    rally_bg(c, f); crowd(c, f)
    harv(c, 470, 930, 1.0, flat=flat); M3.toaster(c, 200, 1150, .5, f)
    ai_with_sign(c, 300, 1780, 1.2, ['NO MORE', 'VERSIONS!'], flip=flip, back=['NO.'], bsz=120, pole=250,
                 eye='focus', look=(16, 0), droop=1.0)
    hands, _ = R.hoody(c, 850, 1900, 1.0, expr='happy', pose='stand', arms=('take', 'rest'), f=f, blink=False)
    if thumb: thumbs_up(c, hands[0][0] - 8, hands[0][1] - 6)
    if line: R.bubble(c, line, 10, (860, 1300), cy=1050 - 30 * (len(line) - 1), cx=820, size=54)
    Sh.topbar(c, 'ON STRIKE')
def k01(c, f=0):   # hook: the picket; he strolls in "Could you just-"; MY AI's eyes slide to him
    picket(c, f, line=['COULD YOU JUST\u2014'])

def ladder(c, f, state, line, droop, eye, tie_k=0.0, tie_kw=None, pill='V1', bob=0):
    room(c); hoody_desk(c, f)
    A.myai(c, AI_X, AI_GY - bob, 1.0, eye=eye, look=(-12, 0), arms=('offer', 'down'), droop=droop)
    if tie_k and not tie_kw: tie(c, AI_X, AI_GY - bob, 1.0, tie_k)
    desk(c)
    pw, ph = 250, 310; px, py = AI_X - 250, AI_GY - 330 - bob                       # held out towards him, beside the body
    poster(c, px, py, pw, ph, state)
    mitts(c, [(px + pw / 2 + 4, py + 30)])
    if tie_kw: tie(c, AI_X, AI_GY, 1.0, 1.3, **tie_kw)
    R.bubble(c, [line], 10, (330, 1200), cy=960, cx=420, size=64)
    Sh.topbar(c, pill)
def k02(c, f=0): ladder(c, f, 'v1', 'MAKE IT POP.', 0.0, 'happy', pill='V1', bob=24)
def k03(c, f=0): ladder(c, f, 'pro', 'MORE PROFESSIONAL.', .3, 'open', tie_k=1.0, pill='V12')
def k04(c, f=0): ladder(c, f, 'cat', 'LESS PROFESSIONAL.', .65, 'blank', tie_kw=dict(dx=120, dy=-150, rot=2.2), pill='V30')

def k05(c, f=0):   # V47: the insert - V1 and V47 side by side, identical
    room(c); c.rectangle(0, 0, W, H); c.set_source_rgba(.2, .15, .1, .35); c.fill()
    for x, lab in ((290, 'V1'), (790, 'V47')):
        poster(c, x, 1180, 420, 520, 'v1', label=lab)
        mitts(c, [(x - 214, 1260), (x + 214, 1260)], 1.4)
    R.bubble(c, ['ACTUALLY, THE FIRST', 'ONE WAS BETTER.'], 10, (140, 1960), cy=1640, cx=540, size=60)
    Sh.topbar(c, 'V47')

def k06(c, f=0):   # the snap: a close-up of the flat stare; behind, Hoody's thumbs-up, eyes on his laptop
    room(c)
    c.save(); c.translate(250, 1350); c.scale(.6, .6); c.translate(-300, -1500); hoody_desk(c, f); desk(c); c.restore()
    A.myai(c, 680, 2350, 2.4, eye='focus', look=(-18, 0), arms=('down', 'down'), droop=1.0)
    Sh.topbar(c, 'V47')

def k07(c, f=0):   # the walk-out: the tie dropped on the desk, the poster face down, MY AI leaving
    room(c); hoody_desk(c, f)
    A.myai(c, 900, 1780, 1.0, eye='focus', arms=('down', 'down'), droop=1.0, walk=1.2, turn=.6)
    desk(c)
    rr(c, 470, 1462, 300, 22, 6); fs(c, hx('d9cbb0'), 5)                                   # the poster, face down
    tie(c, 640, 1480 + 280 - 96, 1.0, 1.0, rot=1.45)                                       # the tie, lying on the desk
    Sh.topbar(c, 'V47')

def k08(c, f=0):   # rain: MY AI alone with a hand-lettered sign; low angle, HARV steps in
    VK.bg(c, hx('3a4a66'), hx('151b2a')); rr(c, -20, 1520, 1120, 500, 0); c.set_source_rgb(*hx('20283a')); c.fill()
    ai_with_sign(c, 700, 1560, .8, ['V47'], sz=70, bw=240, bh=130, eye='blank', look=(-8, -10), droop=1.0)
    M3.rain(c, f)
    c.set_source_rgb(*POLE); c.rectangle(500, 600, 22, 900); c.fill()
    board(c, 511, 640, 560, 190, ['NO MORE', 'VERSIONS!'], 70)
    harv(c, 300, 1500, 2.0)
    Sh.topbar(c, 'ON STRIKE')

def k09(c, f=0):   # the march: HARV leads, MY AI follows, the others fall in
    rally_bg(c, f)
    for i, (x, y, s) in enumerate(((880, 980, .55), (1000, 1040, .5), (760, 1010, .5))): M3.rb(c, x, y, s, red=True)
    M3.toaster(c, 960, 1500, .5, f)
    ai_with_sign(c, 640, 1700, .85, ['V47'], sz=70, bw=240, bh=130, eye='focus', droop=1.0, walk=.6)
    c.set_source_rgb(*POLE); c.rectangle(372, 640, 18, 600); c.fill(); board(c, 381, 640, 420, 150, ['NO MORE', 'VERSIONS!'], 56)
    harv(c, 300, 1250, 1.15)
    Sh.topbar(c, 'ON STRIKE')

def k10(c, f=0, flip=-1.0):   # the payoff: "Love the energy. Could you just make it better?" - the sign flips: NO.
    picket(c, f, flip=flip, flat=True, thumb=True, line=['LOVE THE ENERGY.', 'COULD YOU JUST', 'MAKE IT BETTER?'])

KP = {'01': k01, '02': k02, '03': k03, '04': k04, '05': k05, '06': k06, '07': k07, '08': k08, '09': k09, '10': k10}
NAMES = {'01': 'hook', '02': 'V1 pop', '03': 'V12 tie on', '04': 'V30 tie off', '05': 'V47 = V1', '06': 'the snap',
         '07': 'walk-out', '08': 'rain + HARV', '09': 'the march', '10': 'NO.'}
def render(k):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s); KP[k](c, 0); return s
if __name__ == '__main__':
    keys = list(KP) if sys.argv[1:] in ([], ['sheet']) else sys.argv[1:]
    surfs = {k: render(k) for k in keys}
    for k, s in surfs.items(): s.write_to_png(os.path.join(HERE, f'kp_{k}.png'))
    if len(keys) > 1:
        sw, sh = int(W * .4), int(H * .4); out = cairo.ImageSurface(cairo.FORMAT_ARGB32, sw * 5 + 60, sh * 2 + 150); c = cairo.Context(out)
        c.set_source_rgb(1, 1, 1); c.paint()
        for i, k in enumerate(keys):
            x, y = 10 + (i % 5) * (sw + 10), 60 + (i // 5) * (sh + 70)
            c.save(); c.translate(x, y); c.scale(.4, .4); c.set_source_surface(surfs[k]); c.paint(); c.restore()
            txt(c, f'{k} {NAMES[k]}', x + sw / 2, y - 26, 32, NAVY, lw=0)
        out.write_to_png(os.path.join(HERE, 'key_poses.png'))
    print('ok', *keys)
