"""ME + MY AI - Untitled, rough 1: the key frames timed to the real voices (18.3 s, 549 frames, 1080x1920, 30 fps).
Moving for real: the walk-in (frame 0 -> the tableau), the kick, the walk-off into the loop. Everywhere else: breathing,
a slow push-in, lip flap on the lines, bubbles that pop. This is a timing pass, not the animation.
python3 rough.py frames F ... | video   (video writes rough_video.mp4, no sound)"""
import os, sys, math, subprocess, cairo
import numpy as np, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import keys as KK
from keys import (K, A, E, Sh, R, W, H, GY, HS, AIK, park, txt, rr, fs, ell, limb, hx, lerp, cl, INK, YEL, WHITE, RED, NAVY)
FPS = 30

# ---------------- the timeline (frames) ----------------
# rough 2: the museum runs on a 120 BPM grid (a beat = 15 frames) from the start of shot 5 to the exit; three
# "This is art." lines land on beats 0, 6 and 8, the 10/10 stamps on beats 7, 9, 10, 11 (see mix.py).
SHOTS = [('s1', 57), ('s2', 42), ('s3', 18), ('s4', 18), ('s5', 60), ('s6b', 30), ('s6c', 30), ('s6', 30), ('s7', 24), ('s8', 24),
         ('s9', 36), ('s10', 24), ('s11', 42), ('s12', 48), ('s12b', 18), ('s13', 33), ('s13b', 15), ('s14', 30), ('s15', 24), ('s16', 30)]
START = {}; t = 0
for n, d in SHOTS: START[n] = t; t += d
NF = t
VO = [('h_honest', 's1', 12), ('ai_masterpiece', 's2', 3), ('h_art', 's5', 0), ('h_art2', 's6b', 0), ('ai_art', 's6c', 0), ('ai_vandalism', 's13', 2)]   # (take, shot, frame offset)

def env(name):
    x, sr = sf.read(os.path.join(HERE, 'vo', name + '.wav')); n = sr // FPS; m = len(x) // n
    e = 20 * np.log10(np.sqrt((x[:m * n].reshape(m, n) ** 2).mean(1)) + 1e-6)
    lo, hi = np.percentile(e, 30), np.percentile(e, 97); e = np.clip((e - lo) / (hi - lo + 1e-9), 0, 1)
    return np.convolve(e, [.2, .6, .2], 'same') ** 1.3
ENV = {n: env(n) for n, _, _ in VO}
def talk(f, name):
    for n, s, off in VO:
        if n == name:
            i = f - START[s] - off; e = ENV[n]
            return float(e[i]) if 0 <= i < len(e) else 0.0
    return 0.0

# ---------------- breathing, lip flap, bubble pop: wrappers round the key-frame cast ----------------
G = dict(f=0, h=0.0, ai=0.0, r=99)
_hoody0, _myai0, _eva0, _bub0 = KK.hoody, A.myai, E.eva, KK.bubble
def _breathe(c, x, gy, k): c.translate(x, gy); c.scale(1, 1 + k); c.translate(-x, -gy)
def hoody(c, x, gy, s, *a, **k):
    if G['h'] > .02 and 'op' not in k: k['op'] = .1 + .7 * G['h']
    c.save(); _breathe(c, x, gy, .012 * math.sin(G['f'] * .21)); out = _hoody0(c, x, gy, s, *a, **k); c.restore(); return out
def myai(c, x, gy, s, *a, **k):
    if G['ai'] > .02: k['talk'] = G['ai']
    c.save(); _breathe(c, x, gy, .015 * math.sin(G['f'] * .26 + 1.3)); out = _myai0(c, x, gy, s, *a, **k); c.restore(); return out
def eva(c, x, gy, s, *a, **k):
    if k.get('hand_to') is not None: return _eva0(c, x, gy, s, *a, **k)
    c.save(); _breathe(c, x, gy, .012 * math.sin(G['f'] * .19 + 2.1)); out = _eva0(c, x, gy, s, *a, **k); c.restore(); return out
def bubble(c, lines, r, tail, **k): _bub0(c, lines, min(r, G['r']), tail, **k)
KK.hoody, A.myai, E.eva, KK.bubble = hoody, myai, eva, bubble

def push(c, r, d, k=.035, cx=540, cy=1150):
    z = 1 + k * r / max(1, d); c.translate(cx, cy); c.scale(z, z); c.translate(-cx, -cy)

# ---------------- shots ----------------
def s1(c, f, r):      # the walk-in: frame 0 = them walking in; by frame 15 the tableau; the line from frame 12
    u = KK.ss(r / 15) if hasattr(KK, 'ss') else cl(r / 15)
    walking = r < 15
    eye = 'wide' if r < 7 else 'heart'
    KK.frame0_set(c, ai_eye=eye, ai_arms=('down', 'down') if r < 10 else ('chest', 'chest'), ai_look=(20, 6) if r < 7 else (14, 6),
                  ai_tilt=6 if r >= 10 else 0, hoody_expr='calm' if r < 12 else 'critic', hoody_gaze=0 if r < 8 else 24,
                  ax=lerp(150, KK.AX, u), hx_=lerp(390, KK.HX_, u), walk=(.9 + r * .42) if walking else None,
                  hoody_arms=('rest', 'rest') if r < 13 else ('rest', 'chin'))
    KK.frame0_ground(c, card=False)                                           # no card yet: MY AI only plants it in shot 11
    if r >= 12: G['r'] = r - 12; KK.bubble(c, ['BE BRUTALLY', 'HONEST.'], 20, (520, 800), cy=560, cx=660)
    KK.topbar(c, 'ITS ART')

def held(fn, k=.035):
    def s(c, f, r, d): c.save(); push(c, r, d, k); fn(c); c.restore(); KK.topbar(c, TOP.get(fn.__name__, 'ITS ART'))
    return s
TOP = {'k05': 'HIS LESSON', 'k06': 'HIS LESSON', 'k07': 'HIS LESSON', 'k09': 'HIS LESSON', 'k10': 'HIS LESSON'}

def s3(c, f, r, d):   # CU Hoody: a slow blink, mouth flat
    c.save(); push(c, r, d, .02, cy=1000)
    R.head_close(c, f, 'deadpan', gaze=-10)
    if 6 <= r < 11: K.hoodyz_head(c, 540, 1020, 2.4, era='young', expr='deadpan', blink=True)
    c.restore(); KK.topbar(c, 'ITS ART')

def s4(c, f, r, d):   # the rewind card over shot 2, scrubbing back
    S = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); cc = cairo.Context(S); KK.k02(cc)
    c.set_source_surface(S, 0, 0); c.paint()
    c.rectangle(0, 0, W, H); c.set_source_rgba(.05, .07, .14, .8); c.fill()
    for i in range(6):
        y = (i * 330 + r * 90) % H; c.rectangle(0, y, W, 14); c.set_source_rgba(1, 1, 1, .18); c.fill()
    for q in (0, 1):                                                       # the rewind mark
        x0 = 400 + q * 120; c.move_to(x0 + 110, 760); c.line_to(x0, 840); c.line_to(x0 + 110, 920); c.close_path(); fs(c, WHITE, 8)
    txt(c, '20 MIN EARLIER', 540, 1060, 104, YEL, lw=14)
    KK.topbar(c, 'HIS LESSON')

def s8(c, f, r, d):   # out of the museum: a real facade (steps, columns, banner, glass doors). Hoody holds the door,
    # MY AI trots out first, ahead of him and fully clear of him; they head right, into the park
    KK.park_bg(c)
    c.rectangle(-20, 620, 470, 990); fs(c, hx('f4f4f2'), 8)                                       # the building
    rr(c, -30, 590, 500, 60, 10); fs(c, hx('e3e5e9'), 7)                                          # cornice
    txt(c, 'MODERN ART MUSEUM', 225, 700, KK.fit(c, 'MODERN ART MUSEUM', 44, 380), hx('8d9199'), lw=0)
    for x in (30, 400): rr(c, x, 760, 40, 840, 8); fs(c, hx('e9eaec'), 6)                          # columns
    rr(c, 300, 780, 80, 300, 6); fs(c, hx('ff5c4d'), 5); txt(c, 'NOW', 340, 840, 26, WHITE, lw=0)  # a banner
    c.rectangle(110, 1080, 260, 520); c.set_source_rgb(*hx('bfe3f7')); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(7); c.stroke()
    c.move_to(240, 1080); c.line_to(240, 1600); c.stroke()                                        # the door split
    for i in range(3): rr(c, -20 + i * 10, 1600 + i * 22, 490 - i * 20, 24, 4); fs(c, hx('d4d6db'), 5)   # steps
    u = r / d
    hoody(c, lerp(240, 470, u), GY, HS * .9, expr='calm', step=r * .45, gaze=24, blink=False)
    myai(c, lerp(600, 840, u), GY + 20, HS * .9 * AIK, eye='happy', walk=r * .5, look=(18, 0), turn=.3)
    KK.topbar(c, 'HIS LESSON')

def s13b(c, f, r, d):  # CU Eva: her eyes go from MY AI to Hoody, and one brow goes up. Silent.
    c.save(); push(c, r, d, .04, cy=1100)
    KK.park(c, 0, zoom=1.7, cy=1250)
    rr(c, 300, 1380, 480, 700, 140); fs(c, hx('ffcf2e'), 9)                                      # her coat
    rr(c, 330, 1340, 420, 100, 46); fs(c, hx('33bfff'), 8)                                       # scarf
    up = r >= 6; k = cl((r - 6) / 3)
    E.eva_head(c, 540, 1060, 2.6, 'evacalm', gaze=-18 - 10 * k, tilt=.05 * k)
    c.save(); c.translate(540, 1060); c.rotate(.05 * k); c.set_line_cap(cairo.LINE_CAP_ROUND)   # her brows, big: one goes up
    for q, lift in ((-1, 0), (1, 1)):                                          # just above her eyes; the right one climbs onto the fringe
        bx = -25 + q * 105; by = -62 - 70 * k * lift
        c.move_to(bx - 50, by + 8); c.curve_to(bx - 22, by - 8 - 30 * k * lift, bx + 22, by - 8 - 30 * k * lift, bx + 50, by + 4 + 10 * k * lift)
        c.set_source_rgb(*INK); c.set_line_width(26); c.stroke()
    c.restore()
    c.restore(); KK.topbar(c, 'ITS ART')

def s13(c, f, r, d):  # VANDALISM: a jolt on the first frames
    c.save(); j = 18 * math.exp(-r / 3) * math.sin(r * 2.4); c.translate(j, 0); KK.k13(c); c.restore()

def s15(c, f, r, d):  # the kick: wind-up, contact at frame 6, the card flies out of shot; MY AI flinches
    KK.park_bg(c)
    hit = r >= 4                                                              # the foot meets the card (same plane as him)
    myai(c, 150, GY + 20, HS * AIK, eye='wide' if hit else 'open', arms=('up', 'up') if hit else ('down', 'down'), look=(14, -6) if hit else (20, 4), tilt=-8 if hit else 0)
    k = cl(r / 6) if r < 12 else 1.0
    CX, CG = KK.CARDX, KK.FG + 12                                            # the frame-0 card, exactly where it stood
    if hit: ell(c, CX, KK.FG + 8, 50, 12); c.set_source_rgba(.45, .32, .2, .35); c.fill()            # the hole it left
    else: KK.label_card(c, CX, CG, .9)
    foot = KK.hoody_kick(c, 470, GY, HS, expr='deadpan', gaze=16, k=k)
    if hit:
        u = (r - 4) / 20; x = lerp(CX, 1300, u); y = CG - 100 - 1100 * u + 900 * u * u
        c.save(); c.translate(x, y); c.rotate(u * 6); KK.label_card(c, 0, 0, .9, rot=0); c.restore()
    KK.topbar(c, 'ITS ART')

def s16(c, f, r, d):  # the walk-off over empty grass; the cut lands on frame 0's walk-in
    KK.park_bg(c); u = r / d
    myai(c, lerp(560, 760, u), GY + 20, HS * AIK, eye='open', look=(18, 0), walk=2.4 + r * .42, turn=.3)
    hoody(c, lerp(930, 1130, u), GY, HS, expr='deadpan', gaze=20, blink=False, step=2.4 + r * .42)
    KK.topbar(c, 'ITS ART')


def s9(c, f, r, d):   # the dog trots out from behind the bush, tail going; the puff swells and fades; Eva strolls; MY AI turns
    KK.park_bg(c); u = r / d
    KK.bush(c, 720, 1500, 1.1)
    pk = cl(r / 6) * (1 - .5 * cl((r - 20) / 16)); KK.puff(c, 760, 1235 - 20 * u, 1.0 + .4 * pk)
    col = E.dog(c, lerp(640, 470, KK.ss(u) if hasattr(KK, 'ss') else u), 1600, .95, look=1, f=f * 2)
    hand = eva(c, lerp(980, 930, u), 1600, .8, 'evacalm', sip=.6, gaze=-10, walk=r * .4)
    E.leash(c, hand, col, sag=40)
    hoody(c, 300, 1640, .78, expr='calm', arms=('rest', 'take'), prop=KK.phone, gaze=14, blink=False)
    myai(c, 130, 1660, .78 * AIK, eye='open' if r < 24 else 'wide', look=(18, 4), turn=.3, tilt=-6 * cl((r - 24) / 6))
    KK.topbar(c, 'HIS LESSON')

def s11(c, f, r, d):  # in the frame-0 plane: MY AI writes, then pushes its card into the grass beside the poop; ITS ART lands
    KK.park_bg(c)
    hoody(c, 170, GY, HS, expr='calm' if r < 18 else 'shock', arms=('rest', 'down'), prop=KK.phone, gaze=0 if r < 18 else 24, blink=False)
    ell(c, KK.POOX + 6, KK.FG + 5, 150, 22); c.set_source_rgba(.2, .45, .2, .45); c.fill()
    KK.poop(c, KK.POOX, KK.FG, 1.4)                                          # the same place and size as frame 0
    x, gy, s = 450, 1680, HS * AIK
    push_k = cl((r - 14) / 10); a1 = lerp(60, 20, push_k)
    hx_, hy_ = KK.ai_hand(x, gy, s, 1, (a1, 10))
    myai(c, x, gy, s, eye='happy', arms=('chest' if r % 8 < 4 or r > 12 else 'hold', (a1, 10)), props=(KK.marker, None), look=(14, 6), turn=.2)
    KK.label_card(c, lerp(hx_ + 40, KK.CARDX, push_k), lerp(hy_ + 75, KK.FG + 12, push_k), .9, rot=.04 * (1 - push_k) - .05 * push_k)   # lands exactly on the frame-0 spot
    KK.topbar(c, 'ITS ART' if r >= 24 else 'HIS LESSON')

def s14(c, f, r, d):  # Eva walks off right with the bag and the dog, one brow up at Hoody; his dry look follows her
    KK.park_bg(c); u = r / d
    myai(c, 160, GY + 20, HS * .9 * AIK, eye='wide', arms=('up', 'up'), look=(16, -4))
    hoody(c, 430, GY - 20, HS * .9, expr='deadpan', arms=('rest', 'rest'), gaze=24, blink=False)
    ex = lerp(800, 860, u)
    col = E.dog(c, ex + 150, GY, .78, look=0, f=f * 2)
    hand = eva(c, ex, GY, HS * .9, 'notices', cup=False, gaze=-22, walk=.6 + r * .4)
    KK.bag(c, ex + 116 * .9 - 2, GY - 690 * .9 + 344 * .9 + 6, 1.1)
    E.leash(c, hand, col, sag=40)
    KK.frame0_ground(c, poo=False)                                            # the card stays where MY AI put it (nearest the camera)
    KK.topbar(c, 'ITS ART')


def s6b(c, f, r, d):  # the second "This is art." - Hoody at TWO FRIENDS; on the next beat MY AI's 10/10 goes up
    c.save(); push(c, r, d, .03)
    KK.gallery2(c, back='door', title_x=720)
    KK.visitor(c, 880, 1250, .4, hx('6f7f99'), hx('3b2416'))
    t = KK.floor_plinth(c, 690, 1500, 250, 320, 'TWO FRIENDS', score=r >= 15); KK.bronze_lumps(c, 690, t - 4, 1.05)
    hoody(c, 175, 1820, HS * 1.15, expr='confident', arms=('rest', 'out'), gaze=22, blink=False)
    up = r >= 15
    myai(c, 925, 1840, HS * 1.15 * AIK, eye='happy' if up else 'focus', look=(-16, 4), arms=('down', 'down'), bob=14 if up and r < 19 else 0)   # the stamp: a sticker slaps the label
    KK.bubble(c, ['THIS IS ART.'], 20, (200, 1010), cy=560, cx=430)
    c.restore(); KK.topbar(c, 'HIS LESSON')

def s6c(c, f, r, d):  # the third - MY AI says it now, pointing at PUDDLE (SELF-PORTRAIT); Hoody, proud; stamp on the next beat
    c.save(); push(c, r, d, .03)
    KK.gallery2(c, back='blue', right_work=False)
    t = KK.floor_plinth(c, 360, 1500, 300, 300, 'PUDDLE|(SELF-PORTRAIT)', score=r >= 15); KK.puddle(c, 360, t - 2, 1.2)
    myai(c, 640, 1860, HS * 1.15 * AIK, eye='happy', look=(-16, 0), arms=('offer', 'down'), tilt=-6, bob=14 if 15 <= r < 19 else 0)
    hoody(c, 935, 1820, HS * 1.0, expr='proud', arms=('rest', 'rest'), gaze=-20, blink=False)
    KK.bubble(c, ['THIS IS ART!'], 20, (640, 1380), cy=700, cx=600)
    c.restore(); KK.topbar(c, 'HIS LESSON')


def s12(c, f, r, d):  # Eva walks in, leans down and bags it - the viewer sees it go - then stands with the full bag
    KK.frame0_set(c, ai_eye='heart', hoody_expr='calm' if r < 12 else 'frozen', hoody_gaze=26)
    KK.frame0_ground(c, poo=False)
    gone = r >= 20
    if not gone:
        k = 1 - cl((r - 16) / 4)                                              # the art shrinks into the bag
        KK.poop(c, KK.POOX, KK.FG - 40 * (1 - k), 1.4 * max(.05, k))
    ex = lerp(1120, 935, cl(r / 10))
    lean = cl((r - 8) / 6) * (1 - cl((r - 24) / 8))                           # 0 upright .. 1 bent to the grass
    if lean > .02:
        tgt = (KK.POOX + 10, KK.FG - 110 + 40 * (1 - lean))
        hand = eva(c, ex, 1660, 1.0, 'evacalm', pose='holdlow', hand_to=(lerp(ex - 200, tgt[0], lean), lerp(1240, tgt[1], lean)), cup=False, gaze=-10, tilt=-.18 * lean)
        KK.bag(c, hand[0], hand[1] - 6, 1.4, full=r >= 18)
    else:
        hand = eva(c, ex, 1660, 1.0, 'evacalm', pose='reach' if r >= 24 else 'coffee', cup=False, gaze=-14, walk=(r * .45) if r < 10 else None)
        KK.bag(c, hand[0], hand[1] - 6, 1.4, full=r >= 18)
    E.leash(c, (ex + 116, 1660 - 690 + 344), (1090, 1560), sag=30)
    KK.topbar(c, 'ITS ART')

def s12b(c, f, r, d):  # the pause: CU MY AI, heart eyes still on... they flicker, then go blank. Silence.
    c.save(); push(c, r, d, .05, cy=1300)
    KK.park(c, 0, zoom=1.7, cy=1250)
    eye = 'heart' if r < 6 else ('blank' if r % 2 or r >= 11 else 'heart')
    myai(c, 540, 2050, 2.6, eye=eye, arms=('chest', 'chest'), tilt=0 if r < 11 else -4)
    c.restore(); KK.topbar(c, 'ITS ART')

MAP = {'s1': None, 's2': held(KK.k02), 's3': s3, 's4': s4, 's5': held(KK.k05), 's6': held(KK.k06), 's6b': s6b, 's6c': s6c, 's7': held(KK.k07), 's8': s8,
       's9': s9, 's10': held(KK.k10, .06), 's11': s11, 's12': s12, 's12b': s12b, 's13': s13, 's13b': s13b, 's14': s14,
       's15': s15, 's16': s16}
LINE_SHOT = {s: off for n, s, off in VO}
SPEAKER = {'h_honest': 'h', 'h_art': 'h', 'h_art2': 'h', 'ai_masterpiece': 'ai', 'ai_vandalism': 'ai', 'ai_art': 'ai'}

def draw(f):
    S = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(S)
    G['f'] = f; G['h'] = G['ai'] = 0.0
    for n, s, off in VO: G[SPEAKER[n]] = max(G[SPEAKER[n]], talk(f, n))
    for n, d in SHOTS:
        a = START[n]
        if a <= f < a + d:
            r = f - a; G['r'] = r - LINE_SHOT[n] if n in LINE_SHOT else 99
            if n == 's1': s1(c, f, r)
            else: MAP[n](c, f, r, d)
            break
    return S

# =====================================================================================================
# rough 6 (12:46, Tomas: "all"): 1 the park camera 1.2x closer (anchored at the ground line, so the art stays above the
# phone's controls); 2 MY AI bounces and nods on the museum beat; 3 VANDALISM: red X eyes, a red siren on the antenna, a red flash;
# 4 the park sound holes filled (mix.py); 5 the dog shot closer; 6 shot 3 on the park, not a plain gradient.
# =====================================================================================================
Z, ZC = 1.2, (522, 1700)
def cam(c, z=Z, zc=ZC): c.translate(*zc); c.scale(z, z); c.translate(-zc[0], -zc[1])
def scr(p, z=Z, zc=ZC): return (zc[0] + (p[0] - zc[0]) * z, zc[1] + (p[1] - zc[1]) * z)
KK.AX, KK.HX_ = 230, 455                                                     # a tighter layout, so the closer camera fits everyone
KK.POOX, KK.CARDX = 840, 620
_fg0 = KK.frame0_ground
def _fg(c, poo=True, card=True):                                              # the card a touch smaller, clear of Hoody's legs
    ell(c, KK.POOX + 6, KK.FG + 5, 150, 22); c.set_source_rgba(.2, .45, .2, .45); c.fill()
    if card: KK.label_card(c, KK.CARDX, KK.FG + 12, .8)
    if poo: KK.poop(c, KK.POOX, KK.FG, 1.4)
KK.frame0_ground = _fg

def _myai_beat(c, x, gy, s, *a, **k):                                        # the museum groove: a hop on every beat, a nod side to side
    b = G.get('beat')
    if b is not None:
        ph, n = b; e = math.exp(-ph / 3)
        k['bob'] = k.get('bob', 0) + 22 * s * e; k['tilt'] = k.get('tilt', 0) + (5 if n % 2 else -5) * e
    return myai(c, x, gy, s, *a, **k)
A.myai = _myai_beat

def s1(c, f, r):      # the walk-in, closer: frame 0 = them walking in, the poop waiting; by frame 15 the tableau; the line from frame 12
    u = cl(r / 15); walking = r < 15
    c.save(); cam(c)
    KK.frame0_set(c, ai_eye='wide' if r < 7 else 'heart', ai_arms=('down', 'down') if r < 10 else ('chest', 'chest'),
                  ai_look=(20, 6) if r < 7 else (14, 6), ai_tilt=6 if r >= 10 else 0, hoody_expr='calm' if r < 12 else 'critic',
                  hoody_gaze=0 if r < 8 else 24, ax=lerp(130, KK.AX, u), hx_=lerp(380, KK.HX_, u),
                  walk=(.9 + r * .42) if walking else None, hoody_arms=('rest', 'rest') if r < 13 else ('rest', 'chin'))
    KK.frame0_ground(c, card=False)
    c.restore()
    if r >= 12: G['r'] = r - 12; KK.bubble(c, ['BE BRUTALLY', 'HONEST.'], 20, scr((470, 830)), cy=470, cx=640)
    KK.topbar(c, 'ITS ART')

def s3(c, f, r, d):   # CU Hoody on the park: a slow blink, mouth flat
    c.save(); push(c, r, d, .02, cy=1000)
    KK.park(c, 0, zoom=1.7, cy=1250)
    K.hoodie(c, 540, 1020 + 150 * 2.4, 2.4 * 1.1)
    K.hoodyz_head(c, 540, 1020, 2.4, era='young', expr='deadpan', blink=6 <= r < 11, gaze=-10)
    c.restore(); KK.topbar(c, 'ITS ART')

def s9(c, f, r, d):   # closer on the cause: the dog trots out from behind the bush, the puff; Eva; Hoody on his phone; MY AI's head snaps round
    u = r / d; z9, c9 = 1.22, (580, 1600)
    c.save(); cam(c, z9, c9)
    KK.park_bg(c)
    KK.bush(c, 710, 1500, 1.1)
    pk = cl(r / 6) * (1 - .5 * cl((r - 20) / 16)); KK.puff(c, 700, 1235 - 20 * u, 1.0 + .4 * pk)
    col = E.dog(c, lerp(600, 520, u), 1600, .95, look=1, f=f * 2)
    hand = eva(c, lerp(900, 870, u), 1600, .8, 'evacalm', sip=.6, gaze=-10, walk=r * .4)
    E.leash(c, hand, col, sag=40)
    hoody(c, 380, 1640, .78, expr='calm', arms=('rest', 'down'), prop=KK.phone, gaze=14, blink=False)
    snap = cl((r - 22) / 3)
    myai(c, 250, 1660, .78 * AIK, eye='open' if r < 22 else 'wide', look=(18 + 6 * snap, 4), turn=.3 + .3 * snap, tilt=-8 * snap)
    if 22 <= r < 30: KK.txt(c, '!', 250 + 60, 1660 - 470 * .83, 90, YEL, lw=12)
    c.restore(); KK.topbar(c, 'HIS LESSON')

def s11(c, f, r, d):  # closer, in the frame-0 plane: MY AI pushes its card into the grass beside the poop; ITS ART lands
    c.save(); cam(c)
    KK.park_bg(c)
    hoody(c, 230, GY, HS, expr='calm' if r < 18 else 'shock', arms=('rest', 'down'), prop=KK.phone, gaze=0 if r < 18 else 24, blink=False)
    ell(c, KK.POOX + 6, KK.FG + 5, 150, 22); c.set_source_rgba(.2, .45, .2, .45); c.fill()
    KK.poop(c, KK.POOX, KK.FG, 1.4)
    x, gy, s = 470, 1680, HS * AIK
    push_k = cl((r - 14) / 10); a1 = lerp(60, 20, push_k)
    hx_, hy_ = KK.ai_hand(x, gy, s, 1, (a1, 10))
    myai(c, x, gy, s, eye='happy', arms=('chest' if r % 8 < 4 or r > 12 else 'hold', (a1, 10)), props=(KK.marker, None), look=(14, 6), turn=.2)
    KK.label_card(c, lerp(hx_ + 40, KK.CARDX, push_k), lerp(hy_ + 75, KK.FG + 12, push_k), .8, rot=.04 * (1 - push_k) - .05 * push_k)
    c.restore(); KK.topbar(c, 'ITS ART' if r >= 24 else 'HIS LESSON')

def s12(c, f, r, d):  # closer: Eva walks in, leans down and bags it; the art (nearest the camera) shrinks into the bag
    c.save(); cam(c)
    KK.frame0_set(c, ai_eye='heart', hoody_expr='calm' if r < 12 else 'frozen', hoody_gaze=26)
    KK.frame0_ground(c, poo=False)
    ex = lerp(1120, 860, cl(r / 10))
    lean = cl((r - 8) / 6) * (1 - cl((r - 24) / 8))
    if lean > .02:
        tgt = (KK.POOX + 10, KK.FG - 110 + 40 * (1 - lean))
        hand = eva(c, ex, 1660, 1.0, 'evacalm', pose='holdlow', hand_to=(lerp(ex - 200, tgt[0], lean), lerp(1240, tgt[1], lean)), cup=False, gaze=-10, tilt=-.18 * lean)
    else:
        hand = eva(c, ex, 1660, 1.0, 'evacalm', pose='reach' if r >= 24 else 'coffee', cup=False, gaze=-14, walk=(r * .45) if r < 10 else None)
    if r < 20:
        k = 1 - cl((r - 16) / 4)
        KK.poop(c, KK.POOX, KK.FG - 40 * (1 - k), 1.4 * max(.05, k))
    KK.bag(c, hand[0], hand[1] - 6, 1.4, full=r >= 18)
    E.leash(c, (ex + 116, 1660 - 690 + 344), (1200, 1560), sag=30)
    c.restore(); KK.topbar(c, 'ITS ART')

def s13(c, f, r, d):  # VANDALISM: the jolt, a red flash, red X eyes, the antenna a red siren
    c.save(); j = 18 * math.exp(-r / 3) * math.sin(r * 2.4); c.translate(j, 0); KK.k13(c)
    c.translate(540, 2050); c.translate(0, -280 * 2.6); c.scale(2.6, 2.6)
    c.translate(0, 85); c.rotate(math.radians(-8)); c.translate(0, -85)
    rr(c, -82, -54, 164, 92, 40); fs(c, hx('3a0a12'), 6)                       # wipe the eyes
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    for q in (-1, 1):
        for a, b in (((-16, -24), (16, 8)), ((16, -24), (-16, 8))):
            c.move_to(q * 36 + a[0], a[1]); c.line_to(q * 36 + b[0], b[1]); c.set_source_rgb(*hx('ff3348')); c.set_line_width(13); c.stroke()
    on = (r // 3) % 2 == 0
    if on:
        for i in range(8):                                                     # siren rays
            a = i * math.pi / 4 + r * .4; c.move_to(math.cos(a) * 26, -140 + math.sin(a) * 26); c.line_to(math.cos(a) * 62, -140 + math.sin(a) * 62)
            c.set_source_rgba(1, .2, .28, .8); c.set_line_width(7); c.stroke()
    ell(c, 0, -140, 19, 19); fs(c, hx('ff3348') if on else hx('8a1020'), 6)
    c.restore()
    if r < 3: c.rectangle(0, 0, W, H); c.set_source_rgba(1, .1, .15, .22 * (1 - r / 3)); c.fill(); KK.topbar(c, 'ITS ART')

def s15(c, f, r, d):  # closer: the kick; MY AI flinches
    c.save(); cam(c)
    KK.park_bg(c)
    hit = r >= 4
    myai(c, 230, GY + 20, HS * AIK, eye='wide' if hit else 'open', arms=('up', 'up') if hit else ('down', 'down'), look=(14, -6) if hit else (20, 4), tilt=-8 if hit else 0)
    k = cl(r / 6) if r < 12 else 1.0
    CX, CG = KK.CARDX, KK.FG + 12
    if hit: ell(c, CX, KK.FG + 8, 50, 12); c.set_source_rgba(.45, .32, .2, .35); c.fill()
    else: KK.label_card(c, CX, CG, .8)
    foot = KK.hoody_kick(c, 500, GY, HS, expr='deadpan', gaze=16, k=k)
    if hit:
        u = (r - 4) / 20; x = lerp(CX, 1300, u); y = CG - 100 - 1100 * u + 900 * u * u
        c.save(); c.translate(x, y); c.rotate(u * 6); KK.label_card(c, 0, 0, .8, rot=0); c.restore()
    c.restore(); KK.topbar(c, 'ITS ART')

def s16(c, f, r, d):  # closer: the walk-off over empty grass; the cut lands on frame 0's walk-in
    u = r / d; c.save(); cam(c)
    KK.park_bg(c)
    myai(c, lerp(560, 760, u), GY + 20, HS * AIK, eye='open', look=(18, 0), walk=2.4 + r * .42, turn=.3)
    hoody(c, lerp(880, 1080, u), GY, HS, expr='deadpan', gaze=20, blink=False, step=2.4 + r * .42)
    c.restore(); KK.topbar(c, 'ITS ART')

MAP.update({'s3': s3, 's9': s9, 's11': s11, 's12': s12, 's13': s13, 's15': s15, 's16': s16})
_draw0 = draw
def draw(f):
    b0, b1 = START['s5'], START['s8']
    G['beat'] = ((f - b0) % 15, (f - b0) // 15) if b0 <= f < b1 else None
    if START['s1'] <= f < START['s1'] + dict(SHOTS)['s1']:
        S = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(S)
        G['f'] = f; G['h'] = G['ai'] = 0.0
        for n, s, off in VO: G[SPEAKER[n]] = max(G[SPEAKER[n]], talk(f, n))
        G['r'] = 99; s1(c, f, f); return S
    return _draw0(f)

# =====================================================================================================
# rough 7 (iteration 1 of 2, the animation pass): everyone blinks; glances between the lines; Eva really crouches (bent knees,
# a lean) to bag it; MY AI lifts the card high and slams it into the grass (wobble, dust), then turns proud.
# =====================================================================================================
_h1, _m1, _e1 = hoody, myai, eva
def hoody(c, x, gy, s, *a, **k):
    if k.get('blink') is False and K.FACES.get(k.get('expr', 'calm'), ('open',))[0] in ('open', 'half', 'big'):
        k['blink'] = K.blinking(G['f'], 3)
    return _h1(c, x, gy, s, *a, **k)
def myai(c, x, gy, s, *a, **k):
    if k.get('eye') == 'open' and K.blinking(G['f'], 5): k['eye'] = 'focus'
    return _m1(c, x, gy, s, *a, **k)
def eva(c, x, gy, s, *a, **k):
    if 'blink' not in k: k['blink'] = K.blinking(G['f'], 7)
    return _e1(c, x, gy, s, *a, **k)
KK.hoody, E.eva = hoody, eva

def eva_crouch(c, x, gy, s, k, target, **kw):
    """Eva squatting (k 0..1): feet planted, knees bent toward us, the body lowered and leaning; her hand goes to `target`."""
    dy = 170 * s * k; rot = -.3 * k
    L = 118 * s
    for q in (-1, 1):
        hip = (x + q * 26 * s, gy - 250 * s + dy); foot = (x + q * 28 * s, gy - 14 * s)
        d = math.hypot(hip[0] - foot[0], hip[1] - foot[1]); off = math.sqrt(max(0, L * L - (d / 2) ** 2))
        knee = ((hip[0] + foot[0]) / 2 + q * off * .55 - off * .45, (hip[1] + foot[1]) / 2)
        limb(c, [hip, knee, foot], 30 * s, E.TROUS); ell(c, foot[0] + 4 * s, gy - 8 * s, 28 * s, 14 * s); fs(c, E.SHOE, max(3, 5 * s))
    dev = c.user_to_device(*target)
    c.save(); c.translate(0, dy); c.translate(x, gy - 250 * s); c.rotate(rot); c.translate(-x, -(gy - 250 * s))
    lt = c.device_to_user(*dev)
    n = {'limb': 0, 'ell': 0}; l0, e0 = E.limb, E.ell                          # skip her own straight legs and shoes (the first two of each)
    def limb_(*a):
        n['limb'] += 1
        if n['limb'] > 2: l0(*a)
    def ell_(cc, *a):
        n['ell'] += 1
        if n['ell'] > 2: e0(cc, *a)
        else: cc.new_path()
    E.limb, E.ell = limb_, ell_
    try: hand = _eva0(c, x, gy, s, 'evacalm', pose='holdlow', hand_to=lt, cup=False, blink=K.blinking(G['f'], 7), **kw)
    finally: E.limb, E.ell = l0, e0
    hd = c.user_to_device(*hand); c.restore()
    return c.device_to_user(*hd)

def s1(c, f, r):      # as rough 6, plus: at the end of his line MY AI's eyes go up to him - it is about to answer
    u = cl(r / 15); walking = r < 15
    c.save(); cam(c)
    KK.frame0_set(c, ai_eye='wide' if r < 7 else 'heart', ai_arms=('down', 'down') if r < 10 else ('chest', 'chest'),
                  ai_look=(20, 6) if r < 7 else ((14, 6) if r < 46 else (18, -8)), ai_tilt=6 if r >= 10 else 0,
                  hoody_expr='calm' if r < 12 else 'critic', hoody_gaze=0 if r < 8 else (24 if r < 48 else -14),
                  ax=lerp(130, KK.AX, u), hx_=lerp(380, KK.HX_, u),
                  walk=(.9 + r * .42) if walking else None, hoody_arms=('rest', 'rest') if r < 13 else ('rest', 'chin'))
    KK.frame0_ground(c, card=False)
    c.restore()
    if r >= 12: G['r'] = r - 12; KK.bubble(c, ['BE BRUTALLY', 'HONEST.'], 20, scr((470, 830)), cy=470, cx=640)
    KK.topbar(c, 'ITS ART')

def s11(c, f, r, d):  # MY AI scribbles on the card, lifts it high, slams it into the grass (wobble, dust), then turns proud. ITS ART on the slam
    c.save(); cam(c)
    KK.park_bg(c)
    hoody(c, 230, GY, HS, expr='calm' if r < 18 else 'shock', arms=('rest', 'down'), prop=KK.phone, gaze=-6 if r < 18 else 24, blink=False)
    ell(c, KK.POOX + 6, KK.FG + 5, 150, 22); c.set_source_rgba(.2, .45, .2, .45); c.fill()
    KK.poop(c, KK.POOX, KK.FG, 1.4)
    x, gy, s = 470, 1680, HS * AIK
    lift = cl((r - 8) / 6); slam = cl((r - 14) / 4)
    a1 = lerp(lerp(60, 140, lift), 25, slam)
    hx_, hy_ = KK.ai_hand(x, gy, s, 1, (a1, 10))
    proud = r >= 26
    left = 'chest' if proud else (('chest' if r % 4 < 2 else 'hold') if r < 8 else 'down')
    myai(c, x, gy, s, eye='heart' if proud else ('focus' if r < 14 else 'happy'), arms=(left, 'chest' if proud else (a1, 10)),
         props=(None if r >= 8 else KK.marker, None), look=(14, 6), turn=.2 * (1 - slam), rot=.1 * math.sin(math.pi * cl((r - 14) / 6)))
    wob = .28 * math.exp(-(r - 18) / 4) * math.sin((r - 18) * 1.3) if r >= 18 else 0
    cx_, cg = lerp(hx_ + 40, KK.CARDX, slam), lerp(hy_ + 75, KK.FG + 12, slam)
    KK.label_card(c, cx_, cg, .8, rot=lerp(.04, -.05, slam) + wob)
    if 18 <= r < 27: KK.puff(c, KK.CARDX, KK.FG + 4, .5 * (1 - (r - 18) / 9) + .15)
    c.restore(); KK.topbar(c, 'ITS ART' if r >= 18 else 'HIS LESSON')

def s12(c, f, r, d):  # Eva walks in, squats (knees bent, a lean), the bag goes over the art, she stands with the full bag. Hoody freezes
    c.save(); cam(c)
    KK.frame0_set(c, ai_eye='heart', hoody_expr='calm' if r < 12 else 'frozen', hoody_gaze=26 if r < 30 else 14)
    KK.frame0_ground(c, poo=False)
    ex = lerp(1120, 880, cl(r / 10))
    k = cl((r - 8) / 7) * (1 - cl((r - 24) / 7))                              # 0 standing .. 1 squatting
    if k > .02:
        tgt = (KK.POOX + 6, KK.FG - 120 + 50 * (1 - k))
        hand = eva_crouch(c, ex, 1660, 1.0, k, tgt, gaze=-12)
    else:
        hand = eva(c, ex, 1660, 1.0, 'evacalm', pose='reach' if r >= 24 else 'coffee', cup=False, gaze=-14, walk=(r * .45) if r < 10 else None)
    if r < 20:
        q = 1 - cl((r - 16) / 4)
        KK.poop(c, KK.POOX, KK.FG - 40 * (1 - q), 1.4 * max(.05, q))
    KK.bag(c, hand[0], hand[1] - 6, 1.4, full=r >= 18)
    E.leash(c, (ex + 116, 1660 - 690 + 344 + 170 * k), (1200, 1560), sag=30)
    c.restore(); KK.topbar(c, 'ITS ART')

def s14(c, f, r, d):  # Eva walks off right with the bag and the dog; Hoody's dry look follows her, then MY AI's arms sink and it looks up at him
    KK.park_bg(c); u = r / d
    down = r >= 16
    myai(c, 160, GY + 20, HS * .9 * AIK, eye='wide' if not down else 'open', arms=('up', 'up') if not down else ('down', 'down'),
         look=(16, -4) if not down else (16, -10), tilt=0 if not down else 8)
    hoody(c, 430, GY - 20, HS * .9, expr='deadpan', arms=('rest', 'rest'), gaze=lerp(10, 28, cl(r / 14)) if r < 20 else -18, blink=False)
    ex = lerp(800, 860, u)
    col = E.dog(c, ex + 150, GY, .78, look=0, f=f * 2)
    hand = eva(c, ex, GY, HS * .9, 'notices', cup=False, gaze=-22 if r < 10 else 14, walk=.6 + r * .4)
    KK.bag(c, ex + 116 * .9 - 2, GY - 690 * .9 + 344 * .9 + 6, 1.1)
    E.leash(c, hand, col, sag=40)
    KK.frame0_ground(c, poo=False)
    KK.topbar(c, 'ITS ART')

MAP.update({'s11': s11, 's12': s12, 's14': s14})

# =====================================================================================================
# final (iteration 2 of 2): the eight staging faults both cold viewers shared.
# 1 the dog visibly squats and leaves a poop; 2 a bigger phone; 3 small brown dust, not a white puff; 4 Eva squats deeper, leans less;
# 5 Hoody's face holds while Eva arrives; 6 frame 0: they are still entering from the left edge; 7 thicker card text, bigger
# SAVED / MATCH text; 8 the red X eyes flicker back to blue before the next shot.
# =====================================================================================================
def phone_big(c, x, y, q=1):
    c.save(); c.translate(x, y - 10); c.scale(1.5, 1.5); c.translate(-x, -y); KK.phone(c, x, y); c.restore()

def marker_bold(c, s, x, y, size, maxw):
    size = KK.fit(c, s, size, maxw, 'Permanent Marker')
    c.save(); c.translate(x, y); c.select_font_face('Permanent Marker'); c.set_font_size(size)
    e = c.text_extents(s); c.move_to(-e.width / 2 - e.x_bearing, -e.height / 2 - e.y_bearing); c.text_path(s)
    c.set_source_rgb(*INK); c.set_line_width(size * .07); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke_preserve(); c.fill(); c.restore()
def label_card(c, x, ground, s=1.0, rot=-.05):
    c.save(); c.translate(x, ground); c.rotate(rot); c.scale(s, s)
    rr(c, -9, -120, 18, 130, 6); fs(c, hx('d9a86c'), 5)
    rr(c, -160, -290, 320, 180, 10); fs(c, WHITE, 7)
    marker_bold(c, 'UNTITLED', 0, -228, 66, 270); marker_bold(c, '(2026)', 0, -154, 50, 220)
    c.restore()
KK.label_card = label_card

def k06(c):   # the scan, with SAVED: ART big enough for a phone
    KK.gallery2(c, back='door', left_work=False, title_x=330)
    top = KK.floor_plinth(c, 250, 1330, 220, 280, 'UNTITLED'); KK.bronze_swirl(c, 250, top - 2, 1.0)
    x, gy, s = 690, 2080, 2.3
    KK.ai(c, x, gy, s, eye='focus', tilt=-6, look=(-20, 4), arms=('down', 'down'), turn=-.25)
    KK.beam(c, (x - 60 * s, gy - 280 * s - 8 * s), (250, top - 90))
    def mem(c, X, Y, w, h):
        KK.bronze_swirl(c, X, Y + 20, .7); txt(c, 'SAVED: ART', X, Y + h / 2 - 62, KK.fit(c, 'SAVED: ART', 86, w - 50), hx('33bfff'), lw=0)
    KK.holo(c, 700, 850, 440, 400, mem)
def k10(c):   # the match, one big line: MATCH 99% = ART
    KK.park(c, 0, zoom=1.7, cy=1250)
    for i in range(10):
        a = i * math.pi / 5; c.move_to(540 + math.cos(a) * 470, 1300 + math.sin(a) * 470); c.line_to(540 + math.cos(a) * 620, 1300 + math.sin(a) * 620)
        c.set_source_rgba(*YEL, .9); c.set_line_width(14); c.stroke()
    KK.ai(c, 540, 2200, 2.6, eye='wide', arms=('down', 'down'))
    def mem(c, X, Y, w, h):
        KK.bronze_swirl(c, X - 210, Y - 10, .85); txt(c, '=', X, Y - 80, 120, hx('33bfff'), lw=0); KK.poop(c, X + 210, Y - 10, .95)
        txt(c, 'MATCH 99%', X - 150, Y + h / 2 - 70, 88, hx('33bfff'), lw=0); txt(c, '= ART', X + 265, Y + h / 2 - 70, 88, YEL, lw=0)
    KK.holo(c, 540, 720, 920, 480, mem)

def s1(c, f, r):      # frame 0: they are still coming in from the left edge (the last frame has them leaving right)
    u = cl(r / 15); walking = r < 15
    c.save(); cam(c)
    KK.frame0_set(c, ai_eye='wide' if r < 7 else 'heart', ai_arms=('down', 'down') if r < 10 else ('chest', 'chest'),
                  ai_look=(20, 6) if r < 7 else ((14, 6) if r < 46 else (18, -8)), ai_tilt=6 if r >= 10 else 0,
                  hoody_expr='calm' if r < 12 else 'critic', hoody_gaze=0 if r < 8 else (24 if r < 48 else -14),
                  ax=lerp(40, KK.AX, u), hx_=lerp(250, KK.HX_, u),
                  walk=(.9 + r * .42) if walking else None, hoody_arms=('rest', 'rest') if r < 13 else ('rest', 'chin'))
    KK.frame0_ground(c, card=False)
    c.restore()
    if r >= 12: G['r'] = r - 12; KK.bubble(c, ['BE BRUTALLY', 'HONEST.'], 20, scr((470, 830)), cy=470, cx=640)
    KK.topbar(c, 'ITS ART')

def s9(c, f, r, d):   # the cause, in the open: the dog squats (a strain wiggle, a little puff), trots on to Eva - and a poop is left on the grass
    u = r / d; z9, c9 = 1.22, (580, 1600)
    c.save(); cam(c, z9, c9)
    KK.park_bg(c)
    KK.bush(c, 930, 1470, .9)
    squat = r < 14; go = cl((r - 14) / 12)
    evx = lerp(880, 900, u)
    if r >= 10:                                                               # what it left
        k = min(1, (r - 10) / 4); ell(c, 632, 1604, 60 * k, 9 * k); c.set_source_rgba(.2, .45, .2, .45); c.fill()
        KK.poop(c, 630, 1600, .6 * max(.05, k))
    dx = 590 + (math.sin(r * 2.2) * 3 if squat else 0) + 150 * go; dyy = -abs(math.sin(r * .9)) * 14 * (go > 0) * (go < 1)
    if 6 <= r < 14: KK.puff(c, 660, 1570, .28)
    col = E.dog(c, dx, 1600 + dyy, .95, look=0 if squat else 1, f=f * 2)
    hand = eva(c, evx, 1600, .8, 'evacalm', sip=.6, gaze=-10)
    E.leash(c, hand, col, sag=40)
    hoody(c, 400, 1640, .78, expr='calm', arms=('rest', 'take'), prop=phone_big, gaze=10, blink=False)
    snap = cl((r - 20) / 3)
    myai(c, 225, 1660, .78 * AIK, eye='open' if r < 20 else 'wide', look=(18 + 6 * snap, 6), turn=.3 + .3 * snap, tilt=-8 * snap)
    if 20 <= r < 32: txt(c, '!', 225, 1660 - 560 * .83, 150, YEL, lw=16)
    c.restore(); KK.topbar(c, 'HIS LESSON')

def s11(c, f, r, d):  # as rough 7; the phone is bigger, the dust is a few small brown specks
    c.save(); cam(c)
    KK.park_bg(c)
    hoody(c, 230, GY, HS, expr='calm' if r < 18 else 'shock', arms=('rest', 'down'), prop=phone_big, gaze=-6 if r < 18 else 24, blink=False)
    ell(c, KK.POOX + 6, KK.FG + 5, 150, 22); c.set_source_rgba(.2, .45, .2, .45); c.fill()
    KK.poop(c, KK.POOX, KK.FG, 1.4)
    x, gy, s = 470, 1680, HS * AIK
    lift = cl((r - 8) / 6); slam = cl((r - 14) / 4)
    a1 = lerp(lerp(60, 140, lift), 25, slam)
    hx_, hy_ = KK.ai_hand(x, gy, s, 1, (a1, 10))
    proud = r >= 26
    left = 'chest' if proud else (('chest' if r % 4 < 2 else 'hold') if r < 8 else 'down')
    myai(c, x, gy, s, eye='heart' if proud else ('focus' if r < 14 else 'happy'), arms=(left, 'chest' if proud else (a1, 10)),
         props=(None if r >= 8 else KK.marker, None), look=(14, 6), turn=.2 * (1 - slam), rot=.1 * math.sin(math.pi * cl((r - 14) / 6)))
    wob = .28 * math.exp(-(r - 18) / 4) * math.sin((r - 18) * 1.3) if r >= 18 else 0
    cx_, cg = lerp(hx_ + 40, KK.CARDX, slam), lerp(hy_ + 75, KK.FG + 12, slam)
    KK.label_card(c, cx_, cg, .8, rot=lerp(.04, -.05, slam) + wob)
    if 18 <= r < 24:
        q = (r - 18) / 6
        for sx in (-1, 1): ell(c, KK.CARDX + sx * (16 + 40 * q), KK.FG + 6 - 26 * q + 30 * q * q, 9 * (1 - q) + 2, 7 * (1 - q) + 2); c.set_source_rgba(.48, .34, .2, .8 * (1 - q)); c.fill()
    c.restore(); KK.topbar(c, 'ITS ART' if r >= 18 else 'HIS LESSON')

def eva_squat(c, x, gy, s, k, target, **kw):
    """Deeper and more upright than rough 7 (a viewer read the lean as a fall): knees wide, the body straight down, a small lean."""
    dy = 215 * s * k; rot = -.1 * k; L = 118 * s
    for q in (-1, 1):
        hip = (x + q * 26 * s, gy - 250 * s + dy); foot = (x + q * 34 * s, gy - 14 * s)
        dd = math.hypot(hip[0] - foot[0], hip[1] - foot[1]); off = math.sqrt(max(0, L * L - (dd / 2) ** 2))
        knee = ((hip[0] + foot[0]) / 2 + q * off, (hip[1] + foot[1]) / 2 - 10 * s * k)
        limb(c, [hip, knee, foot], 30 * s, E.TROUS); ell(c, foot[0] + q * 6 * s, gy - 8 * s, 28 * s, 14 * s); fs(c, E.SHOE, max(3, 5 * s))
    dev = c.user_to_device(*target)
    c.save(); c.translate(0, dy); c.translate(x, gy - 250 * s); c.rotate(rot); c.translate(-x, -(gy - 250 * s))
    lt = c.device_to_user(*dev)
    n = {'limb': 0, 'ell': 0}; l0, e0 = E.limb, E.ell
    def limb_(*a):
        n['limb'] += 1
        if n['limb'] > 2: l0(*a)
    def ell_(cc, *a):
        n['ell'] += 1
        if n['ell'] > 2: e0(cc, *a)
        else: cc.new_path()
    E.limb, E.ell = limb_, ell_
    try: hand = _eva0(c, x, gy, s, 'evacalm', pose='holdlow', hand_to=lt, cup=False, blink=False, **kw)
    finally: E.limb, E.ell = l0, e0
    hd = c.user_to_device(*hand); c.restore()
    return c.device_to_user(*hd)

def s12(c, f, r, d):  # Hoody's face holds (frozen from the cut, no blink); Eva squats straight down, bags it, stands with the full bag
    c.save(); cam(c)
    G['noblink'] = True
    KK.frame0_set(c, ai_eye='heart', hoody_expr='frozen', hoody_gaze=26 if r < 30 else 14)
    G['noblink'] = False
    KK.frame0_ground(c, poo=False)
    ex = lerp(1120, 895, cl(r / 10))
    k = cl((r - 8) / 7) * (1 - cl((r - 24) / 7))
    if k > .02:
        hand = eva_squat(c, ex, 1660, 1.0, k, (KK.POOX + 6, KK.FG - 120 + 50 * (1 - k)), gaze=-12)
    else:
        hand = eva(c, ex, 1660, 1.0, 'evacalm', pose='reach' if r >= 24 else 'coffee', cup=False, gaze=-14, walk=(r * .45) if r < 10 else None, blink=False)
    if r < 20:
        q = 1 - cl((r - 16) / 4); KK.poop(c, KK.POOX, KK.FG - 40 * (1 - q), 1.4 * max(.05, q))
    KK.bag(c, hand[0], hand[1] - 6, 1.4, full=r >= 18)
    E.leash(c, (ex + 116, 1660 - 690 + 344 + 215 * k), (1200, 1560), sag=30)
    c.restore(); KK.topbar(c, 'ITS ART')
_h2 = hoody
def hoody(c, x, gy, s, *a, **k):
    if G.get('noblink'): k['blink'] = None; return _h1.__wrapped__(c, x, gy, s, *a, **k) if hasattr(_h1, '__wrapped__') else _nb(c, x, gy, s, *a, **k)
    return _h2(c, x, gy, s, *a, **k)
def _nb(c, x, gy, s, *a, **k):                                               # the breathing wrapper, with the eyes held open
    k['blink'] = False; return _h1(c, x, gy, s, *a, **k)
KK.hoody = hoody

_s13 = s13
def s13(c, f, r, d):  # the X eyes hold for the word, then flicker back to blue in the last frames: it is shaken, not broken
    if r < d - 7 or (r < d - 2 and r % 2 == 0): return _s13(c, f, r, d)
    c.save(); KK.k13(c); c.restore()

MAP.update({'s6': held(k06), 's10': held(k10, .06), 's9': s9, 's11': s11, 's12': s12, 's13': s13})

# =====================================================================================================
# 20 Nov: speech tails land on the speaker, computed every frame from where the speaker is actually drawn.
# Hoody: the tip sits just outside his cheek beside the mouth (head-local (+-92, 64)); the bubble goes to that side, so the
# tail never crosses his hair. MY AI: the tip touches the top of its antenna ball (it moves with walk, beat hops, tilt, shake).
# =====================================================================================================
ANCH = {}
_hh0 = K.hoodyz_head
def _hh_rec(c, x, y, s, *a, **k):
    rot = k.get('rot', a[2] if len(a) > 2 else 0)
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    ANCH['h'] = dict(c=c.user_to_device(0, 0), side={q: c.user_to_device(q * 92, 64) for q in (-1, 1)},
                     hair=[c.user_to_device(px, py) for px, py in ((-150, -40), (150, -40), (0, -190), (0, 120))])
    c.restore()
    return _hh0(c, x, y, s, *a, **k)
K.hoodyz_head = _hh_rec

_myai_draw = _myai0
def _myai_rec(c, x, gy, s, eye='happy', look=(0, 0), arms=('down', 'down'), props=(None, None), rot=0, walk=None, bob=0, tilt=0, turn=0, talk=0.0, droop=0.0, **kw):
    t = max(A.LIMITS['tilt'][0], min(A.LIMITS['tilt'][1], tilt))
    c.save(); c.translate(x, gy); c.rotate(rot); c.translate(0, -280 * s - bob - (abs(math.sin(walk)) * 8 * s if walk is not None else 0)); c.scale(s, s)
    c.translate(*A.NECK); c.rotate(math.radians(t)); c.translate(-A.NECK[0], -A.NECK[1])
    ax = turn * 40; bx, by = ax + 70 * droop, -140 + 30 * droop
    ANCH['ai'] = dict(tip=c.user_to_device(bx, by - 19), c=c.user_to_device(0, 0))
    c.restore()
    return _myai_draw(c, x, gy, s, eye=eye, look=look, arms=arms, props=props, rot=rot, walk=walk, bob=bob, tilt=tilt, turn=turn, talk=talk, droop=droop, **kw)
_myai0 = _myai_rec                                                           # the breathing wrapper calls _myai0 by name

LINE_OF = {s: n for n, s, off in VO}
def speech(c, lines, r, tail, cy=500, size=66, cx=540):
    """Ignores the hand-set tail/position: places the bubble from the speaker drawn in this frame, in screen space."""
    shot = G.get('shot'); who = SPEAKER.get(LINE_OF.get(shot, ''), None)
    a = ANCH.get(who)
    if a is None: return _bub0(c, lines, min(r, G['r']), tail, cy=cy, size=size, cx=cx)
    c.save(); c.select_font_face('Lilita One'); c.set_font_size(size)
    w = max(c.text_extents(l).width for l in lines) + 90; h = len(lines) * size * 1.12 + 56; c.restore()
    top_min, m = 380 + h / 2, 34
    if who == 'h':
        side = 1 if a['c'][0] < 540 else -1
        tip = a['side'][side]; sh = abs(a['hair'][1][0] - a['c'][0]) / 150          # his head's scale on screen
        bx = a['c'][0] + side * 310 * sh; by = tip[1] - h / 2 - 300 * sh                # far enough out that the tail clears his hair
    else:
        tip = a['tip']; bx = tip[0]; by = tip[1] - h / 2 - 240                         # high enough to clear what it points at
    bx = min(max(bx, w / 2 + m), W - w / 2 - m); by = max(by, top_min)
    G.setdefault('tails', []).append((who, (bx, by + h / 2 - 6), tip, a))
    c.save(); c.identity_matrix(); _bub0(c, lines, min(r, G['r']), tip, cy=by, size=size, cx=bx); c.restore()
KK.bubble = speech

_draw_prev = draw
def draw(f):
    ANCH.clear(); G['tails'] = []
    for n, d in SHOTS:
        if START[n] <= f < START[n] + d: G['shot'] = n
    return _draw_prev(f)

# ---- a curved tail for Hoody: down outside his hair, then in under the side curls to his cheek at mouth height ----
_hh1 = K.hoodyz_head
def _hh_rec2(c, x, y, s, *a, **k):
    rot = k.get('rot', a[2] if len(a) > 2 else 0)
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    ANCH['h2'] = {q: dict(tip=c.user_to_device(q * 90, 76), turn=c.user_to_device(q * 205, 70), out=c.user_to_device(q * 215, -60)) for q in (-1, 1)}
    c.restore()
    return _hh1(c, x, y, s, *a, **k)
K.hoodyz_head = _hh_rec2

def bubble_curved(c, lines, r, base_x, by, size, p):
    """render.bubble's look, with a bent tail: bubble bottom -> outside the hair (p['out']) -> round the turn -> p['tip']."""
    k = R.back(r / 5) if hasattr(R, 'back') else min(1, r / 5)
    if k <= .03: return
    c.save(); c.identity_matrix(); c.select_font_face('Lilita One'); c.set_font_size(size)
    w = max(c.text_extents(l).width for l in lines) + 90; h = len(lines) * size * 1.12 + 56
    bx, cy = base_x, by
    kk = max(k, .02); b0, b1 = (bx - 34 * kk, cy + (h / 2 - 8) * kk), (bx + 34 * kk, cy + (h / 2 - 8) * kk)   # the tail stays on his face while the bubble pops
    o, t, tp = p['out'], p['turn'], p['tip']
    side = 1 if t[0] > tp[0] else -1
    c.move_to(*b0); c.curve_to(o[0] - side * 24, o[1], t[0] - side * 10, t[1] + 30, tp[0], tp[1] + 10)
    c.line_to(tp[0], tp[1] - 12)
    c.curve_to(t[0] + side * 26, t[1] - 30, o[0] + side * 30, o[1], *b1); c.close_path(); fs(c, WHITE, 8)
    c.translate(bx, cy); c.scale(k, k); c.translate(-bx, -cy)
    rr(c, bx - w / 2, cy - h / 2, w, h, 40); fs(c, WHITE, 8)
    c.move_to(bx - 32, cy + h / 2 - 12); c.line_to(bx + 32, cy + h / 2 - 12); c.set_source_rgb(*WHITE); c.set_line_width(14); c.stroke()
    for i, l in enumerate(lines): txt(c, l, bx, cy - h / 2 + 28 + size * .56 + i * size * 1.12, size, NAVY, lw=0)
    c.restore()

_speech1 = speech
def speech(c, lines, r, tail, cy=500, size=66, cx=540):
    shot = G.get('shot'); who = SPEAKER.get(LINE_OF.get(shot, ''), None)
    if who != 'h' or 'h2' not in ANCH: return _speech1(c, lines, r, tail, cy=cy, size=size, cx=cx)
    a = ANCH['h']; side = 1 if a['c'][0] < 540 else -1; p = ANCH['h2'][side]
    c.save(); c.select_font_face('Lilita One'); c.set_font_size(size)
    w = max(c.text_extents(l).width for l in lines) + 90; h = len(lines) * size * 1.12 + 56; c.restore()
    bx = min(max(p['out'][0] + side * (w / 2 - 70), w / 2 + 34), W - w / 2 - 34)
    by = max(p['out'][1] - h / 2 - 150, 380 + h / 2)
    G.setdefault('tails', []).append(('h', (bx, by + h / 2), p['tip'], a))
    bubble_curved(c, lines, min(r, G['r']), bx, by, size, p)
KK.bubble = speech

# =====================================================================================================
# 20 Nov, museum v3 (Tomas: "too much poop, it didn't hook"): ONE poop-like piece in the whole museum, the bronze UNTITLED.
# The lesson is now three different things: Hoody at BLUE, MOSTLY (a big blue canvas), Hoody at NOTHING (an empty plinth),
# then MY AI itself at the bronze swirl - "THIS IS ART!" - and only then the scan: SAVED: ART. The shape match stays.
# Order: s5, s6b, s6c, s6 (scan), s7; lines on beats 0, 4, 6; stickers on beats 5, 7; the round on 10, 11 (mix.py).
# =====================================================================================================
def chair(c, x, y, s=1.0):
    """A plain wooden chair, three-quarter view; y = the floor under it (the plinth top)."""
    W_ = hx('c98a4b')
    for dx in (-52, 44): rr(c, x + dx * s, y - 96 * s, 14 * s, 96 * s, 4 * s); fs(c, W_, max(3, 5 * s))
    rr(c, x - 60 * s, y - 112 * s, 126 * s, 22 * s, 6 * s); fs(c, W_, max(3, 5 * s))
    for dx in (-52, 44): rr(c, x + dx * s, y - 250 * s, 14 * s, 140 * s, 4 * s); fs(c, W_, max(3, 5 * s))
    rr(c, x - 54 * s, y - 250 * s, 114 * s, 54 * s, 8 * s); fs(c, W_, max(3, 5 * s))

def cubes(c, x, y, s=1.0):
    """Three painted cubes stacked off-axis."""
    for i, (dx, col) in enumerate(((-8, 'ff5c4d'), (14, 'ffcf2e'), (-4, '2f6fd6'))):
        c.save(); c.translate(x + dx * s, y - (i * 78 + 40) * s); c.rotate((-.08, .1, -.05)[i]); rr(c, -42 * s, -40 * s, 84 * s, 80 * s, 6 * s); fs(c, hx(col), max(3, 6 * s)); c.restore()

def k05(c):   # lesson 1: Hoody at BLUE, MOSTLY - a big blue canvas on the back wall, a rope in front. "See? This is art."
    KK.gallery2(c, back='none', title_x=540)
    c.rectangle(472, 872, 390, 320); c.set_source_rgba(0, 0, 0, .1); c.fill()
    c.rectangle(460, 860, 390, 320); fs(c, hx('2f6fd6'), 7)                    # low on the wall, clear of his bubble
    rr(c, 648, 1300, 14, 150, 4); fs(c, hx('d9dce2'), 4)                      # its label on a floor stand
    KK.title_lbl(c, 655, 1215, 250, 'BLUE, MOSTLY', 'paint, 2019')
    KK.stanchions(c, 470, 850, 1500)
    KK.ai(c, 935, 1840, HS * 1.15 * AIK, eye='focus', tilt=-12, look=(-16, -6), arms=('down', 'down'))
    KK.hoody(c, 165, 1820, HS * 1.15, expr='confident', arms=('rest', 'out'), gaze=22, blink=False)
    KK.bubble(c, ['SEE? THIS IS ART.'], 20, (200, 1000), cy=545, cx=450)

def s6b(c, f, r, d):  # lesson 2: Hoody at NOTHING - an empty plinth in a pool of light. "This is art." A 10/10 lands on the next beat
    c.save(); push(c, r, d, .03)
    KK.gallery2(c, back='door', title_x=720)
    KK.visitor(c, 880, 1250, .4, hx('6f7f99'), hx('3b2416'))
    g = cairo.LinearGradient(0, 700, 0, 1190); g.add_color_stop_rgba(0, 1, .98, .85, .5); g.add_color_stop_rgba(1, 1, .98, .85, .05)
    c.move_to(660, 620); c.line_to(720, 620); c.line_to(830, 1190); c.line_to(550, 1190); c.close_path(); c.set_source(g); c.fill()
    KK.floor_plinth(c, 690, 1500, 250, 320, 'NOTHING', 'air, 2019', score=r >= 15)
    hoody(c, 175, 1820, HS * 1.15, expr='confident', arms=('rest', 'out'), gaze=22, blink=False)
    up = r >= 15
    myai(c, 925, 1840, HS * 1.15 * AIK, eye='happy' if up else 'focus', look=(-16, 4), arms=('down', 'down'), bob=14 if up and r < 19 else 0)
    KK.bubble(c, ['THIS IS ART.'], 20, (200, 1010), cy=560, cx=430)
    c.restore(); KK.topbar(c, 'HIS LESSON')

def s6c(c, f, r, d):  # lesson 3: MY AI says it itself, at the one bronze piece: UNTITLED. Hoody, proud. A 10/10 on the next beat
    c.save(); push(c, r, d, .03)
    KK.gallery2(c, back='door', title_x=330, left_work=False)
    t = KK.floor_plinth(c, 330, 1500, 280, 330, 'UNTITLED', score=r >= 15); KK.bronze_swirl(c, 330, t - 2, 1.2)
    myai(c, 650, 1860, HS * 1.15 * AIK, eye='happy', look=(-16, 0), arms=('offer', 'down'), tilt=-6, bob=14 if 15 <= r < 19 else 0)
    hoody(c, 935, 1820, HS * 1.0, expr='proud', arms=('rest', 'rest'), gaze=-20, blink=False)
    KK.bubble(c, ['THIS IS ART!'], 20, (640, 1380), cy=700, cx=600)
    c.restore(); KK.topbar(c, 'HIS LESSON')

def k07(c):   # the fast round: three more, none of them brown - THE WAIT (a chair), THREE MOODS (cubes), a yellow canvas; 10/10 each
    KK.gallery2(c, back='none', right_work=False)
    c.rectangle(452, 760, 220, 280); c.set_source_rgba(0, 0, 0, .1); c.fill()
    c.rectangle(440, 748, 220, 280); fs(c, hx('ffcf2e'), 6)
    c.save(); c.translate(690, 1010); c.rotate(-.15); rr(c, -54, -26, 108, 52, 10); fs(c, WHITE, 5); txt(c, '10/10', 0, 0, 34, RED, lw=0); c.restore()
    t = KK.floor_plinth(c, 150, 1500, 240, 300, 'THE WAIT', 'wood, 2019', score=True); chair(c, 150, t - 2, .9)
    t = KK.floor_plinth(c, 905, 1500, 240, 280, 'THREE MOODS', 'paint, 2019'); cubes(c, 905, t - 2, .9)
    KK.hoody(c, 420, 1890, HS * .9, expr='proud', arms=('rest', 'rest'), blink=False)
    KK.ai(c, 690, 1900, HS * .9 * AIK, eye='happy', arms=('down', 'up'), props=(None, KK.card), look=(14, -4), turn=.2)
k05.__name__, k07.__name__ = 'k05', 'k07'

MAP.update({'s5': held(k05), 's6b': s6b, 's6c': s6c, 's7': held(k07)})

if __name__ == '__main__':
    os.chdir(HERE)
    if sys.argv[1:2] == ['frames']:
        for f in map(int, sys.argv[2:]): draw(f).write_to_png(f'chk_{f:03d}.png')
    else:
        p = subprocess.Popen(f'ffmpeg -y -v error -f rawvideo -pix_fmt bgra -s {W}x{H} -r 30 -i - -vf format=yuv420p -c:v libx264 -crf {14 if sys.argv[1:2] == ["final"] else 18} -preset {"slow" if sys.argv[1:2] == ["final"] else "veryfast"} -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709 tmp_video.mp4'.split(), stdin=subprocess.PIPE)
        for f in range(NF): p.stdin.write(bytes(draw(f).get_data()))
        p.stdin.close(); assert p.wait() == 0; os.rename('tmp_video.mp4', 'rough_video.mp4'); print('video ok', NF)
