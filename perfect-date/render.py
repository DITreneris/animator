"""ME + MY AI - Perfect Date. Timed rough: 20 shots, 1080x1920, 30 fps. Hoody's lines are Tomas's recordings.
Usage: python3 render.py frames 0 60 ...  |  python3 render.py video"""
import os, sys, math, random, subprocess, cairo
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, 'characters'))
import kit as K
import chars as Sh                      # Hoody's faces, the title bar, the cat's one eye, the sweat bead
import eva as E, myai as A
from kit import INK, WHITE, NAVY, SKIN, YEL, RED, TABBY, rr, fs, ell, limb, txt, hx, lerp, cl, ss
W, H = 1080, 1920
WGB = E.load_wgb()                      # Who's a Good Boy?: the park
back = lambda t: 0.02 if t <= 0 else (1 if t >= 1 else max(.02, 1 + 2.7 * (t - 1) ** 3 + 1.7 * (t - 1) ** 2))
oe = lambda t: 1 - (1 - cl(t)) ** 3
JEANS = hx('2b3a55'); SHOE = hx('1f2230'); WOOD = hx('b9783f'); WOOD_D = hx('8a5a2e'); IRON = hx('2a2d36'); COAT2 = hx('8e5bd6')

# ---------------- helpers ----------------
def bubble(c, lines, r, tail, cy=500, size=66, out=None, cx=540):
    k = back(r / 5) if out is None else back(r / 5) * cl(out / 3)
    if k <= .03: return
    c.save(); c.translate(cx, cy); c.scale(k, k)
    c.select_font_face('Lilita One'); c.set_font_size(size)
    w = max(c.text_extents(l).width for l in lines) + 90; h = len(lines) * size * 1.12 + 56
    tx, ty = (tail[0] - cx) / k, (tail[1] - cy) / k
    c.move_to(-60, h / 2 - 6); c.line_to(tx, ty); c.line_to(30, h / 2 - 6); c.close_path(); fs(c, WHITE, 8)
    rr(c, -w / 2, -h / 2, w, h, 40); fs(c, WHITE, 8)
    c.move_to(-58, h / 2 - 12); c.line_to(28, h / 2 - 12); c.set_source_rgb(*WHITE); c.set_line_width(14); c.stroke()
    for i, l in enumerate(lines): txt(c, l, 0, -h / 2 + 28 + size * .56 + i * size * 1.12, size, NAVY, lw=0)
    c.restore()

def park(c, f, zoom=1.0, cx=540, cy=1300):
    c.save(); c.translate(cx, cy); c.scale(zoom, zoom); c.translate(-cx, -cy)
    WGB.park(c, f, 0); c.restore()

def seat_front(c, x0, x1, seat):
    rr(c, x0 - 16, seat - 12, x1 - x0 + 32, 34, 12); fs(c, WOOD, 7)
def bench(c, x0, x1, seat, gy):
    for x in (x0 + 40, x1 - 40):
        c.rectangle(x - 10, seat, 20, gy - seat); c.set_source_rgb(*IRON); c.fill()
    for i in range(3): rr(c, x0, seat - 210 + i * 54, x1 - x0, 36, 10); fs(c, WOOD, 6)
    for x in (x0 + 40, x1 - 40): c.rectangle(x - 9, seat - 220, 18, 220); c.set_source_rgb(*IRON); c.fill()
    rr(c, x0 - 16, seat - 12, x1 - x0 + 32, 34, 12); fs(c, WOOD, 7)
    c.rectangle(x0 - 10, seat + 18, x1 - x0 + 20, 10); c.set_source_rgb(*WOOD_D); c.fill()

# ---------------- Hoody, full body ----------------
def hoody(c, x, gy, s, expr='calm', pose='stand', arms=('rest', 'rest'), gaze=0, op=0, rot=0, prop=None, seat=None):
    """pose 'stand': feet on gy. pose 'sit': gy is the seat; shins hang to gy + 170 s. arms: (screen-left, screen-right).
    Returns the hands. prop(c, x, y) is drawn at the screen-right hand."""
    c.save(); c.translate(x, gy); c.rotate(rot); c.translate(-x, -gy)
    waist = gy if pose == 'sit' else gy - 300 * s
    hy = waist - 326 * s; neck = hy + 150 * s
    if pose == 'sit':                                     # front view: shins hang, the seat edge, then the knees in front of it
        for q in (-1, 1):
            limb(c, [(x + q * 50 * s, waist + 30 * s), (x + q * 54 * s, waist + 168 * s)], 40 * s, JEANS)
            ell(c, x + q * 58 * s, waist + 176 * s, 32 * s, 15 * s); fs(c, SHOE, max(3, 5 * s))
        if seat: seat_front(c, seat[0], seat[1], gy)
        for q in (-1, 1): ell(c, x + q * 50 * s, waist + 26 * s, 36 * s, 30 * s); fs(c, JEANS, max(3, 6 * s))
    else:
        for q in (-1, 1):
            kick = 70 * s if (pose == 'trip' and q == 1) else 0
            limb(c, [(x + q * 40 * s, waist - 10 * s), (x + q * 44 * s + kick, gy - 14 * s - kick * .6)], 40 * s, JEANS)
            ell(c, x + q * 48 * s + kick, gy - 8 * s - kick * .6, 32 * s, 15 * s); fs(c, SHOE, max(3, 5 * s))
    sl, sr_ = K.hoodie(c, x, neck, s * 1.1)
    hands = []
    for q, (sh, a) in zip((-1, 1), ((sl, arms[0]), (sr_, arms[1]))):
        sx, sy = sh
        P = {'rest':    [(sx, sy), (sx + q * 30 * s, sy + 110 * s), (x + q * 70 * s, waist + 30 * s)],
             'down':    [(sx, sy), (sx + q * 18 * s, sy + 120 * s), (sx + q * 14 * s, sy + 230 * s)],
             'up':      [(sx, sy), (sx + q * 40 * s, sy - 110 * s), (sx + q * 50 * s, sy - 250 * s)],
             'gesture': [(sx, sy), (sx + q * 60 * s, sy + 90 * s), (x + q * 120 * s, hy + 120 * s)],
             'forward': [(sx, sy), (sx + q * 10 * s, sy + 120 * s), (x + q * 40 * s, sy + 150 * s)],
             'out':     [(sx, sy), (sx + q * 110 * s, sy + 40 * s), (sx + q * 220 * s, sy + 30 * s)],
             'flail':   [(sx, sy), (sx + q * 100 * s, sy - 70 * s), (sx + q * 170 * s, sy - 150 * s)],
             'bench':   [(sx, sy), (sx + q * 50 * s, sy + 110 * s), (x + q * 150 * s, waist - 4 * s)],
             'chin':    [(sx, sy), (sx + q * 40 * s, sy + 120 * s), (x + q * 46 * s, hy + 104 * s)]}[a]
        K.arm(c, P, s); hands.append(P[-1])
        if q == 1 and prop: prop(c, *P[-1])
    K.hoodyz_head(c, x, hy, s, era='young', expr=expr, blink=False, gaze=gaze, op=op)
    c.restore()
    return hands

def head_close(c, f, expr, gaze=0, op=0, bgc=('8fd0ff', 'fff0c8'), s=2.4, y=1020):
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, *hx(bgc[0])); g.add_color_stop_rgb(1, *hx(bgc[1])); c.set_source(g); c.paint()
    K.hoodie(c, 540, y + 150 * s, s * 1.1)
    K.hoodyz_head(c, 540, y, s, era='young', expr=expr, blink=False, gaze=gaze, op=op)

# ---------------- the dog ----------------
def dog_run(c, x, gy, s, ph, look=-1):
    c.save(); c.translate(x, gy); c.scale(s * look * -1, s)            # drawn facing left (-x)
    a = math.sin(ph) * 30
    for dx, sgn in ((-50, 1), (-30, -1), (40, 1), (60, -1)):
        limb(c, [(dx, -44), (dx + sgn * a * .8, -6)], 16, E.BROWN)
    c.move_to(70, -60); c.curve_to(110, -70, 130, -90, 150, -110); c.set_source_rgb(*INK); c.set_line_width(20); c.stroke()
    c.move_to(70, -60); c.curve_to(110, -70, 130, -90, 150, -110); c.set_source_rgb(*E.BROWN); c.set_line_width(12); c.stroke()
    ell(c, 0, -62, 86, 34); fs(c, E.BROWN, 6)
    c.rectangle(-70, -84, 14, 44); c.set_source_rgb(*RED); c.fill()
    ell(c, -96, -92, 40, 32); fs(c, E.BROWN, 6); ell(c, -128, -82, 20, 14); fs(c, E.BROWN, 5); ell(c, -144, -86, 7, 6); c.set_source_rgb(*INK); c.fill()
    c.save(); c.translate(-80, -112); c.rotate(-.9 - math.sin(ph) * .2); ell(c, 24, 0, 30, 12); fs(c, E.DARKB, 4); c.restore()   # ear flying back
    ell(c, -106, -100, 6, 7); c.set_source_rgb(*INK); c.fill()
    c.restore()
    for i in range(3): c.move_to(x + 160 * s + i * 30, gy - 70 * s + i * 20); c.line_to(x + 230 * s + i * 30, gy - 70 * s + i * 20); c.set_source_rgba(1, 1, 1, .8); c.set_line_width(7); c.stroke()

# ---------------- props ----------------
def balloon_up(c, x, y): A.balloon(c, x, y + 20, 1)
def speaker_at(c, x, y): A.speaker(c, x, y + 10, 1)

# ---------------- the shots ----------------
GY = 1520; SEAT = 1390
def wide(c, f, eva_x=None, eva_pose='coffee', eva_expr='evacalm', dog=None, hoody_kw=None, ai=None, cat_eye=False, cat=True, show_hoody=True):
    park(c, f)
    bench(c, 220, 780, SEAT, GY)
    if cat: Sh.cat_one_eye(c, 700, SEAT - 6, .62, open_eye=cat_eye)
    if show_hoody: hoody(c, 420, SEAT, .82, pose='sit', seat=(220, 780), **(hoody_kw or {}))
    if ai: A.myai(c, ai.pop('x', 150), GY + 40, .95, **ai)
    if dog: dog(c)
    if eva_x is not None: E.eva(c, eva_x, GY + 30, .9, eva_expr, sip=.2, pose=eva_pose)

def s1(c, f, r):   # frozen mid-sentence, eyes off right
    head_close(c, f, 'calm', gaze=26, op=.35)
    K.arm(c, [(240, 1400), (250, 1260), (330, 1180)], 2.0)
def s2(c, f, r):   # she walks in with the dog
    ex = lerp(1220, 880, oe(r / 26))
    wide(c, f, eva_x=ex, dog=lambda c: E.dog(c, ex + 150, GY + 40, .8, look=1, f=f),
         hoody_kw=dict(expr='shock', gaze=24, arms=('rest', 'rest')), ai=dict(x=140, eye='open', look=(14, 0)))
def s3(c, f, r):   # "Help me impress her!"
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, *hx('8fd0ff')); g.add_color_stop_rgb(1, *hx('fff0c8')); c.set_source(g); c.paint()
    hoody(c, 400, 1820, 1.25, expr='hopeful', pose='stand', arms=('rest', 'chin'), rot=.06)
    A.myai(c, 800, 1700, 1.15, eye='happy', tilt=-10, look=(-10, 0))
    bubble(c, ['HELP ME', 'IMPRESS HER!'], r - 2, (460, 690), cy=520, cx=480)
def s4(c, f, r):   # the dog charges
    park(c, f, zoom=1.6, cy=1500)
    rr(c, -40, 1380, 360, 50, 14); fs(c, WOOD, 7)                       # the bench end, the cat asleep on it
    Sh.cat_one_eye(c, 130 + 92 * 1.2, 1384, 1.2, open_eye=False)
    dog_run(c, lerp(1300, 520, r / 15), 1700, 2.1, r * 1.4)
def s5(c, f, r):   # the cat opens one eye
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, *hx('8fd0ff')); g.add_color_stop_rgb(1, *hx('fff0c8')); c.set_source(g); c.paint()
    rr(c, -40, 1250, 1160, 90, 20); fs(c, WOOD, 8)
    Sh.cat_one_eye(c, 540 + 92 * 2.6, 1250, 2.6, open_eye=(r >= 3))
def s6(c, f, r):   # the dog hides behind her legs; her glance
    park(c, f)
    sh = math.sin(r * 2.6) * 5                                        # trembling
    E.dog(c, 520 + sh, GY + 120, 1.05, look=0, f=0)
    E.eva(c, 470, GY + 140, 1.15, 'amused', sip=.6, pose='glance')
    c.save(); c.translate(600 + sh, 1500); c.scale(1.05, 1.05)        # head peeking round her legs, ears flat, worried eye
    ell(c, 0, 0, 40, 34); fs(c, E.BROWN, 6); ell(c, -32, 12, 22, 15); fs(c, E.BROWN, 5); ell(c, -50, 8, 7, 6); c.set_source_rgb(*INK); c.fill()
    c.save(); c.translate(18, 8); c.rotate(.9); ell(c, 0, 0, 12, 30); fs(c, E.DARKB, 4); c.restore()
    ell(c, -10, -6, 9, 10); fs(c, WHITE, 3); ell(c, -12, -4, 4, 5); c.set_source_rgb(*INK); c.fill(); c.restore()
    Sh.sweat(c, 650, 1440, .9)
    for i in range(3):
        c.move_to(668 + i * 16, 1470 + i * 12); c.line_to(696 + i * 16, 1460 + i * 12); c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
def s7(c, f, r):   # "Watch."
    park(c, f, zoom=1.3, cy=1400)
    A.myai(c, 540, 1760, 1.75, eye='focus', arms=('down', 'wait' if r < 10 else 'down'))
    bubble(c, ['WATCH.'], r - 4, (600, 760), cy=520)
def s8(c, f, r):   # the rose
    park(c, f, zoom=1.2, cy=1450)
    k = oe((r - 4) / 10)
    A.myai(c, 330, 1720, 1.25, eye='focus', arms=('down', 'offer'), props=(None, A.rose), rot=-.12 * k)
    E.eva(c, 800, 1760, 1.0, 'impressed' if r >= 10 else 'evacalm', sip=.1)
def s9(c, f, r):   # Hoody copies the bow, empty-handed, facing us
    park(c, f, zoom=1.2, cy=1450)
    A.myai(c, 300, 1380, .62, eye='focus', arms=('down', 'offer'), props=(None, A.rose), rot=-.12)
    E.eva(c, 700, 1400, .6, 'impressed', sip=.1)
    hoody(c, 540, 1900, 1.2, expr='sheepish', pose='stand', arms=('down', 'out'), rot=-.18 * oe(r / 8))
def s10(c, f, r):  # the speaker into his hands; play
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, *hx('fff0c8')); g.add_color_stop_rgb(1, *hx('8fd16b')); c.set_source(g); c.paint()
    k = oe(r / 8)
    K.arm(c, [(-40, 1500), (220, 1420), (420, 1330)], 2.4)
    c.save(); c.translate(lerp(900, 560, k), lerp(900, 1240, k)); c.scale(3.0, 3.0); A.speaker(c, 0, 0); c.restore()
    c.save(); c.translate(lerp(1000, 760, k), lerp(820, 1180, k)); c.scale(2.6, 2.6)
    ell(c, 0, 0, A.HAND_R, A.HAND_R); fs(c, WHITE, 6); c.restore()
    if r >= 6:
        for i in range(3):
            ang = -1.2 + i * .5; txt(c, '♪', 560 + math.cos(ang) * (190 + (r - 6) * 12), 1150 + math.sin(ang) * (190 + (r - 6) * 12), 80, NAVY, lw=0)
def s11(c, f, r):  # one impossibly smooth dance move; she laughs
    park(c, f, zoom=1.2, cy=1450)
    A.myai(c, 360, 1720, 1.25, eye='happy', arms=('up', 'hip'), rot=.14 * math.sin(r * .35))
    E.eva(c, 800, 1760, 1.0, 'laugh', sip=.1, op=.9)
def s12(c, f, r):  # he copies, trips; the robot steadies the speaker without looking
    park(c, f, zoom=1.2, cy=1450)
    k = ss((r - 4) / 16)
    hoody(c, 470, 1820, 1.05, expr='shock' if r >= 6 else 'hopeful', pose='trip' if r >= 6 else 'stand',
          arms=('flail', 'flail') if r >= 6 else ('up', 'hip' if False else 'rest'), rot=.32 * k)
    sx, sy = lerp(560, 880, k), lerp(1100, 980, k) - math.sin(k * math.pi) * 220
    c.save(); c.translate(sx, sy); c.rotate(k * 2.2); c.scale(1.7, 1.7); A.speaker(c, 0, 0); c.restore()
    if r >= 18:
        A.myai(c, 1010, 1800, 1.15, eye='happy', arms=('give', 'down'), turn=-.85)
def s13(c, f, r):  # the balloon: "Ooh!"
    head_close(c, f, 'happy' if r >= 5 else 'hopeful', gaze=18)
    k = oe(r / 7)
    A.balloon(c, lerp(1100, 860, k), lerp(1500, 1200, k), 1)
def s14(c, f, r):  # the tableau: he is the backdrop
    park(c, f)
    hoody(c, 540, 1350, .58, expr='polite', pose='stand', arms=('rest', 'up'), prop=balloon_up)
    A.myai(c, 360, GY + 110, 1.15, eye='heart', arms=('down', 'hold'), turn=.7)
    E.eva(c, 750, GY + 130, 1.02, 'charmed', sip=.1)
    for i, (hx_, hy_) in enumerate(((560, 1180), (530, 1080), (575, 990))):
        if r >= 6 + i * 6:
            c.save(); c.translate(hx_, hy_ - (r - 6 - i * 6) * 2); c.scale(.5, .5)
            c.move_to(0, 18); c.curve_to(-30, -2, -18, -30, 0, -12); c.curve_to(18, -30, 30, -2, 0, 18); c.close_path(); fs(c, A.PINK, 5); c.restore()
def s15(c, f, r):  # he looks up at his own arm. "...oh."
    head_close(c, f, 'happy' if r < 8 else 'deadpan', gaze=0)
    K.arm(c, [(820, 1500), (880, 1120), (900, 700)], 2.0)
    A.balloon(c, 900, 700, 1)
def s16(c, f, r):  # she takes its hand. Hold.
    park(c, f, zoom=1.25, cy=1450)
    rs = 1.3; rx = 330; hp = A.hand_at(rx, 1760, rs, 1, 'hold2')
    E.eva(c, hp[0] + 40 + 76 * .95, 1760, .95, 'charmed', sip=.1, pose='holdlow' if r >= 6 else 'coffee', hand_to=hp if r >= 6 else None)
    A.myai(c, rx, 1760, rs, eye='open' if r < 6 else 'blank', arms=('down', 'hold2'))
def s17(c, f, r):  # it looks at the hand, at Hoody, at her
    park(c, f, zoom=1.6, cy=1300)
    if r < 9: e, lk, tl = 'open', (0, 14), 0
    elif r < 18: e, lk, tl = 'confused', (-20, 0), -10
    else: e, lk, tl = 'happy', (16, 0), 8
    A.myai(c, 540, 1960, 2.4, eye=e, look=lk, tilt=tl)
def s18(c, f, r):  # leaving: "Your turn!"
    k = r / 36
    wide(c, f, cat=True, show_hoody=True, hoody_kw=dict(expr='deadpan', arms=('rest', 'up'), prop=balloon_up))
    ax = lerp(600, 780, k); ex = ax + 175
    A.myai(c, ax, GY + 60, .95, eye='happy', arms=('down', 'wave'), turn=-.85, walk=r * .6)
    E.eva(c, ex, GY + 60, .9, 'charmed', sip=.1)
    E.dog(c, lerp(900, 1060, k), GY + 70, .8, look=1, f=f)
    bubble(c, ['YOUR TURN!'], r - 6, (ax - 30, 1180), cy=820, cx=560)
def s19(c, f, r):  # alone; the cat's paw on his hand
    park(c, f, zoom=1.7, cy=1350)
    bench(c, -60, 1140, 1500, 1920)
    hands = hoody(c, 560, 1500, 1.25, expr='deadpan' if r < 26 else 'calm', pose='sit', arms=('bench', 'up'), prop=balloon_up, seat=(-60, 1140))
    hx_, hy_ = hands[0]
    Sh.cat_one_eye(c, hx_ - 175, 1494, 1.25, look=1, open_eye=(r >= 8))
    if r >= 12:                                                       # one paw, a short reach, onto his hand
        k = oe((r - 12) / 8); px, py = lerp(hx_ - 60, hx_ - 4, k), lerp(1470, hy_ - 6, k)
        limb(c, [(hx_ - 80, 1470), (px, py)], 26, TABBY); ell(c, px, py, 22, 17); fs(c, TABBY, 5)
def s20(c, f, r):  # someone else walks in -> frame 0
    if r >= 22: s1(c, f, 0); return
    wide(c, f, hoody_kw=dict(expr='shock' if r > 10 else 'calm', gaze=24, arms=('rest', 'up'), prop=balloon_up), ai=None)
    x = lerp(1240, 900, oe(r / 16))
    keep = (E.COAT, E.HAIR_E, E.SCARF, E.GOLD)
    E.COAT, E.HAIR_E, E.SCARF, E.GOLD = COAT2, hx('d9a441'), hx('f4f4f4'), hx('d9d9d9')   # someone else: purple coat, fair hair
    E.eva(c, x, GY + 30, .9, 'evacalm', sip=.2)
    E.COAT, E.HAIR_E, E.SCARF, E.GOLD = keep

DUR = [24, 36, 45, 15, 12, 18, 27, 30, 24, 21, 30, 39, 21, 36, 27, 30, 27, 36, 42, 30]
FNS = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19, s20]
SHOTS = []; _t = 0
for fn, d in zip(FNS, DUR): SHOTS.append((fn, _t, _t + d)); _t += d
NF = _t
def pill(f): return 'ITS DATE' if f >= SHOTS[15][1] else 'HIS DATE'

def draw(f):
    S = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(S)
    for fn, a, b in SHOTS:
        if a <= f < b:
            c.save(); fn(c, f, f - a); c.restore(); c.identity_matrix(); Sh.topbar(c, pill(f if fn is not s20 or f - a < 22 else 0)); break
    return S

if __name__ == '__main__':
    if sys.argv[1] == 'frames':
        for f in map(int, sys.argv[2:]): draw(f).write_to_png(os.path.join(HERE, f'chk_{f:03d}.png'))
    else:
        p = subprocess.Popen(f'ffmpeg -y -v error -f rawvideo -pix_fmt bgra -s {W}x{H} -r 30 -i - -vf format=yuv420p -c:v libx264 -crf 18 -preset veryfast -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709 {os.path.join(HERE, "tmp_video.mp4")}'.split(), stdin=subprocess.PIPE)
        for f in range(NF): p.stdin.write(bytes(draw(f).get_data()))
        p.stdin.close(); assert p.wait() == 0; os.rename(os.path.join(HERE, 'tmp_video.mp4'), os.path.join(HERE, 'video.mp4')); print('video ok', NF)
