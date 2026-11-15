"""ME + MY AI - Perfect Date v2: the guitar and the balloon. Timed rough: 19 shots, 1080x1920, 30 fps.
MY AI shows him how (the rose), hands him the guitar ("Your turn!"), and helps the show by pumping up his heart balloon.
He floats up playing his old riff with his eyes closed while Eva takes the robot's hand. Plonk. Pop. Back to frame 0.
Usage: python3 render.py frames 0 60 ...  |  python3 render.py video"""
import os, sys, math, subprocess, cairo
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, 'characters'))
import kit as K
import chars as Sh                      # Hoody's faces, the title bar, the cat's one eye, the sweat bead
import eva as E, myai as A
from kit import INK, WHITE, NAVY, YEL, RED, TABBY, rr, fs, ell, limb, txt, hx, lerp, cl, ss
W, H = 1080, 1920
WGB = E.load_wgb()                      # Who's a Good Boy?: the park
back = lambda t: 0.02 if t <= 0 else (1 if t >= 1 else max(.02, 1 + 2.7 * (t - 1) ** 3 + 1.7 * (t - 1) ** 2))
oe = lambda t: 1 - (1 - cl(t)) ** 3
JEANS = hx('2b3a55'); SHOE = hx('1f2230'); WOOD = hx('b9783f'); WOOD_D = hx('8a5a2e'); IRON = hx('2a2d36')
HOSE = hx('9aa3b2'); SKY0, SKY1 = hx('5fb8ff'), hx('cfeaff'); TREE = hx('3f9a4a'); TREE_D = hx('2f7a3a')
K.FACES['bliss'] = ('shut', ('raised', 'raised'), 'grin')          # eyes shut, giving it everything
K.FACES['wince'] = ('shut', ('worried', 'worried'), 'wobble')

# ---------------- helpers ----------------
def bubble(c, lines, r, tail, cy=500, size=66, cx=540):
    k = back(r / 5)
    if k <= .03: return
    c.save(); c.translate(cx, cy); c.scale(k, k)
    c.select_font_face('Lilita One'); c.set_font_size(size)
    w = max(c.text_extents(l).width for l in lines) + 90; h = len(lines) * size * 1.12 + 56
    tx, ty = (tail[0] - cx) / k, (tail[1] - cy) / k
    c.move_to(-40, h / 2 - 6); c.line_to(tx, ty); c.line_to(40, h / 2 - 6); c.close_path(); fs(c, WHITE, 8)
    rr(c, -w / 2, -h / 2, w, h, 40); fs(c, WHITE, 8)
    c.move_to(-38, h / 2 - 12); c.line_to(38, h / 2 - 12); c.set_source_rgb(*WHITE); c.set_line_width(14); c.stroke()
    for i, l in enumerate(lines): txt(c, l, 0, -h / 2 + 28 + size * .56 + i * size * 1.12, size, NAVY, lw=0)
    c.restore()

def park(c, f, zoom=1.0, cx=540, cy=1300):
    c.save(); c.translate(cx, cy); c.scale(zoom, zoom); c.translate(-cx, -cy)
    WGB.park(c, f, 0); c.restore()

def sky(c, f, trees=True, ty=1700):
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, *SKY0); g.add_color_stop_rgb(1, *SKY1); c.set_source(g); c.paint()
    for i, (x, y, r) in enumerate(((180, 380, 70), (820, 560, 90), (520, 980, 60))):    # clouds drift down: we are rising
        y = (y + f * 3) % 2100 - 100
        for dx, dy, rr_ in ((-r, 10, r * .7), (0, 0, r), (r, 12, r * .75)): ell(c, x + dx, y + dy, rr_, rr_ * .8)
        c.set_source_rgb(*WHITE); c.fill()
    if trees:
        for i in range(9):
            x = -60 + i * 150; r = 120 + (i * 37) % 50
            ell(c, x, ty + (i % 2) * 40, r, r); fs(c, TREE if i % 2 else TREE_D, 6)
        c.rectangle(0, ty + 60, W, H); c.set_source_rgb(*TREE_D); c.fill()

def heart(c, cx, tip, k, sx=1.0, sy=1.0, op=1.0):
    """A heart balloon, tip (where the string ties) at (cx, tip). k = 1 is the small balloon."""
    c.save(); c.translate(cx, tip); c.scale(k * 1.6 * sx, k * 1.6 * sy); c.translate(0, -40)
    c.move_to(0, 40); c.curve_to(-62, 2, -38, -50, 0, -20); c.curve_to(38, -50, 62, 2, 0, 40); c.close_path()
    c.set_source_rgba(*RED, op); c.fill_preserve(); c.set_source_rgba(*INK, op); c.set_line_width(5 / k ** .5); c.stroke()
    ell(c, -18, -14, 8, 6); c.set_source_rgba(1, 1, 1, .6 * op); c.fill()
    c.move_to(-5, 40); c.line_to(5, 40); c.line_to(0, 46); c.close_path(); c.set_source_rgba(*INK, op); c.fill()
    c.restore()

def string(c, a, b, sway=0):
    c.move_to(*a); c.curve_to(a[0] + 30 + sway, lerp(a[1], b[1], .33), b[0] - 30 - sway, lerp(a[1], b[1], .66), *b)
    c.set_source_rgb(*INK); c.set_line_width(3); c.stroke()

def notes(c, x, y, r, n=3, size=80):
    for i in range(n):
        u = ((r * .04 + i / n) % 1)
        ang = -1.5 + i * .55 + math.sin(r * .2 + i) * .1
        c.save(); c.translate(x + math.cos(ang) * (120 + u * 220), y + math.sin(ang) * (120 + u * 220))
        txt(c, '♪' if i % 2 else '♫', 0, 0, size, NAVY, lw=0); c.restore()

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
GROT = -.45; GS = .6                                     # the guitar on him: rotation and scale (times s)
def guitar_points(x, hy, s):
    """Where the guitar sits on Hoody: body centre, the fret hand on the neck, the headstock (where the balloon ties)."""
    body = (x + 20 * s, hy + 370 * s)
    at = lambda d: (body[0] + d * GS * s * math.cos(GROT), body[1] + d * GS * s * math.sin(GROT))
    return body, at(250), at(440)

def hoody(c, x, gy, s, expr='calm', pose='stand', arms=('rest', 'rest'), gaze=0, op=0, rot=0, prop=None, seat=None,
          guitar=None, f=0):
    """pose 'stand': feet on gy. 'sit': gy is the seat. 'float': gy is where the feet hang, toes down, legs swaying.
    guitar: None, or the strum offset (he is playing; arms are then set by the guitar). Returns (hands, headstock)."""
    c.save(); c.translate(x, gy); c.rotate(rot); c.translate(-x, -gy)
    waist = gy if pose == 'sit' else gy - 300 * s
    hy = waist - 326 * s; neck = hy + 150 * s
    if pose == 'sit':
        for q in (-1, 1):
            limb(c, [(x + q * 50 * s, waist + 30 * s), (x + q * 54 * s, waist + 168 * s)], 40 * s, JEANS)
            ell(c, x + q * 58 * s, waist + 176 * s, 32 * s, 15 * s); fs(c, SHOE, max(3, 5 * s))
        if seat: seat_front(c, seat[0], seat[1], gy)
        for q in (-1, 1): ell(c, x + q * 50 * s, waist + 26 * s, 36 * s, 30 * s); fs(c, JEANS, max(3, 6 * s))
    else:
        for q in (-1, 1):
            sw = math.sin(f * .25 + q) * 16 * s if pose == 'float' else 0
            foot = (x + q * 44 * s + sw, gy - 14 * s)
            limb(c, [(x + q * 40 * s, waist - 10 * s), foot], 40 * s, JEANS)
            c.save(); c.translate(foot[0] + q * 4 * s, foot[1] + 6 * s)
            if pose == 'float': c.rotate(q * 1.2)                        # toes pointing down
            ell(c, 0, 0, 32 * s, 15 * s); fs(c, SHOE, max(3, 5 * s)); c.restore()
    sl, sr_ = K.hoodie(c, x, neck, s * 1.1)
    hands = []; head = None
    if guitar is not None:
        body, fret, head = guitar_points(x, hy, s)
        K.guitar(c, body[0], body[1], GS * s, rot=GROT)
        P_l = [sl, (sl[0] - 60 * s, sl[1] + 120 * s), (body[0] - 30 * s, body[1] - 20 * s + guitar * s)]
        P_r = [sr_, (sr_[0] + 50 * s, sr_[1] + 140 * s), fret]
        K.arm(c, P_l, s); K.arm(c, P_r, s); hands = [P_l[-1], P_r[-1]]
    else:
        for q, (sh, a) in zip((-1, 1), ((sl, arms[0]), (sr_, arms[1]))):
            sx, sy = sh
            P = {'rest':    [(sx, sy), (sx + q * 30 * s, sy + 110 * s), (x + q * 70 * s, waist + 30 * s)],
                 'down':    [(sx, sy), (sx + q * 18 * s, sy + 120 * s), (sx + q * 14 * s, sy + 230 * s)],
                 'up':      [(sx, sy), (sx + q * 40 * s, sy - 110 * s), (sx + q * 50 * s, sy - 250 * s)],
                 'out':     [(sx, sy), (sx + q * 110 * s, sy + 40 * s), (sx + q * 220 * s, sy + 30 * s)],
                 'take':    [(sx, sy), (sx + q * 90 * s, sy + 80 * s), (sx + q * 190 * s, sy + 40 * s)],
                 'flail':   [(sx, sy), (sx + q * 100 * s, sy - 70 * s), (sx + q * 170 * s, sy - 150 * s)],
                 'chin':    [(sx, sy), (sx + q * 40 * s, sy + 120 * s), (x + q * 46 * s, hy + 104 * s)]}[a]
            K.arm(c, P, s); hands.append(P[-1])
            if q == 1 and prop: prop(c, *P[-1])
    K.hoodyz_head(c, x, hy, s, era='young', expr=expr, blink=False, gaze=gaze, op=op)
    c.restore()
    if head and rot:                                                      # the headstock in screen space
        dx, dy = head[0] - x, head[1] - gy
        head = (x + dx * math.cos(rot) - dy * math.sin(rot), gy + dx * math.sin(rot) + dy * math.cos(rot))
    return hands, head

def head_close(c, f, expr, gaze=0, op=0, bgc=('8fd0ff', 'fff0c8'), s=2.4, y=1020):
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, *hx(bgc[0])); g.add_color_stop_rgb(1, *hx(bgc[1])); c.set_source(g); c.paint()
    K.hoodie(c, 540, y + 150 * s, s * 1.1)
    K.hoodyz_head(c, 540, y, s, era='young', expr=expr, blink=False, gaze=gaze, op=op)

strum = lambda f, on=True: math.sin(f * 1.9) * 10 if on else 0

# ---------------- the shots ----------------
GY = 1520; SEAT = 1390
def wide(c, f, cat=True, cat_eye=False, hoody_sit=True, hoody_kw=None):
    park(c, f)
    bench(c, 220, 780, SEAT, GY)
    if cat: Sh.cat_one_eye(c, 700, SEAT - 6, .62, open_eye=cat_eye)
    if hoody_sit: hoody(c, 420, SEAT, .82, pose='sit', seat=(220, 780), **(hoody_kw or {}))

def eva_dog(c, f, x, gy, s, expr='evacalm', pose='coffee', sip=.2, dog_dx=-150, dog_look=0, walk=None):
    """Eva with the dog on its leash, sitting at her side (screen-left of her by default)."""
    col = E.dog(c, x + dog_dx * s, gy + 10 * s, s * .9, look=dog_look, f=f)
    hand = E.eva(c, x, gy, s, expr, sip=sip, pose=pose)
    if hand and pose not in ('holdlow', 'reach'): E.leash(c, hand, col, sag=60 * s)

def s1(c, f, r):   # frame 0: on the bench, hand on chin, eyes locked off right
    head_close(c, f, 'calm', gaze=26, op=.35)
    K.arm(c, [(240, 1400), (250, 1260), (330, 1180)], 2.0)
def s2(c, f, r):   # she sits down at the far end with coffee and the dog
    wide(c, f, hoody_kw=dict(expr='shock', gaze=24))
    A.myai(c, 140, GY + 40, .95, eye='open', look=(14, 0))
    eva_dog(c, f, lerp(1150, 860, oe(r / 24)), GY + 30, .9)
def s3(c, f, r):   # "Help me impress her!"
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, *hx('8fd0ff')); g.add_color_stop_rgb(1, *hx('fff0c8')); c.set_source(g); c.paint()
    hoody(c, 400, 1820, 1.25, expr='hopeful', pose='stand', arms=('rest', 'chin'), rot=.06)
    A.myai(c, 800, 1700, 1.15, eye='happy', tilt=-10, look=(-10, 0))
    bubble(c, ['HELP ME', 'IMPRESS HER!'], r - 2, (430, 860), cy=520, cx=480)
def s4(c, f, r):   # the dog sniffs toward the cat; one eye; the dog backs off behind her
    park(c, f, zoom=1.6, cy=1500)
    rr(c, -40, 1380, 420, 50, 14); fs(c, WOOD, 7)
    Sh.cat_one_eye(c, 150 + 92 * 1.3, 1384, 1.3, open_eye=(r >= 12))
    if r < 18: dx = lerp(820, 640, oe(r / 12))
    else: dx = lerp(640, 900, oe((r - 18) / 10))
    E.dog(c, dx, 1760, 1.6, look=1 if r >= 18 else 0, f=f)
    hand = (1120, 1250); E.leash(c, hand, (dx - 2 * 1.6, 1760 - 98 * 1.6), sag=80)
    if r >= 18: Sh.sweat(c, dx + 70, 1480, 1.1)
def s5(c, f, r):   # "Watch!"
    park(c, f, zoom=1.3, cy=1400)
    A.myai(c, 540, 1760, 1.75, eye='focus', arms=('down', 'wait' if r < 10 else 'down'))
    bubble(c, ['WATCH!'], r - 4, (546, 1000), cy=560)
def s6(c, f, r):   # the rose; she is impressed
    park(c, f, zoom=1.2, cy=1450)
    k = oe((r - 4) / 10)
    A.myai(c, 330, 1720, 1.25, eye='focus', arms=('down', 'offer'), props=(None, A.rose), rot=-.12 * k)
    E.eva(c, 780, 1760, 1.0, 'impressed' if r >= 10 else 'evacalm', sip=.1)
def s7(c, f, r):   # "Your turn!": the guitar (the small heart balloon tied to its headstock) goes into his hands
    park(c, f, zoom=1.2, cy=1450)
    k = oe((r - 6) / 14)
    rx, rs = 790, 1.15
    A.myai(c, rx, 1800, rs, eye='happy', arms=('down', 'give') if k < 1 else ('down', 'down'), turn=-.6)
    if k < 1:                                                         # in flight between them
        gx, gy_ = lerp(640, 360, k), lerp(1200, 1300, k) - math.sin(k * math.pi) * 60
        K.guitar(c, gx, gy_, .6, rot=lerp(-.2, GROT, k))
        hd = (gx + 440 * .6 * math.cos(lerp(-.2, GROT, k)), gy_ + 440 * .6 * math.sin(lerp(-.2, GROT, k)))
        hoody(c, 300, 1820, 1.0, expr='hopeful', arms=('rest', 'take'))
    else:
        _, hd = hoody(c, 300, 1820, 1.0, expr='happy', guitar=0)
    string(c, hd, (hd[0] + 40, hd[1] - 230)); heart(c, hd[0] + 40, hd[1] - 230, 1)
    bubble(c, ['YOUR TURN!'], r - 2, (rx - 24 * rs, 1800 - 420 * rs), cy=560, cx=640)
def s8(c, f, r):   # eyes closed, giving it everything
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, *hx('ffd36b')); g.add_color_stop_rgb(1, *hx('ff8fa6')); c.set_source(g); c.paint()
    _, hd = hoody(c, 470, 2350, 1.9, expr='bliss', guitar=strum(f), rot=-.06 + .05 * math.sin(r * .3), f=f)
    notes(c, 470, 900, r, size=96)
def s9(c, f, r):   # MY AI "helps the show": a hose from its chest clicks onto the balloon
    park(c, f, zoom=1.4, cy=1500)
    rs = 1.6; rx, gy = 330, 1900
    A.myai(c, rx, gy, rs, eye='happy', arms=('hold', 'down'), tilt=8)
    k = cl((r - 8) / 18); bk = 1.2 + 1.1 * k + .06 * math.sin(r * 1.4) * k
    tip = (800, 1100)
    string(c, tip, (900, 1960))
    heart(c, *tip, bk)
    ch = (rx, gy - 130 * rs)                                          # the chest disc
    reach = oe(r / 8); end = (lerp(ch[0] + 60, tip[0], reach), lerp(ch[1], tip[1] + 10, reach))
    c.move_to(*ch); c.curve_to(ch[0] + 160, ch[1] + 140, end[0] - 80, end[1] + 260, *end)
    c.set_source_rgb(*INK); c.set_line_width(26); c.stroke_preserve(); c.set_source_rgb(*HOSE); c.set_line_width(14); c.stroke()
    ell(c, *ch, 26, 26); fs(c, HOSE, 6)
    if r >= 8 and (r // 4) % 2 == 0:                                  # pump puffs
        for i in range(3): ell(c, end[0] - 40 + i * 40, end[1] + 30, 10, 10); c.set_source_rgba(1, 1, 1, .8); c.fill()
def lift_y(r):                                                        # shot 10: how far his feet are off the ground
    return 380 * ss(cl((r - 14) / 34))
def s10(c, f, r):  # the balloon swells; his feet leave the ground, still playing. She looks up: sip, brow, smile
    park(c, f)
    bench(c, 520, 1010, SEAT, GY)                                     # the bench behind her: he is out on the open path
    Sh.cat_one_eye(c, 640, SEAT - 6, .62, open_eye=False)
    eva_dog(c, f, 880, GY + 40, .9, pose='glance' if r >= 20 else 'coffee', dog_dx=-150)
    A.myai(c, 100, GY + 70, .85, eye='happy', arms=('hold', 'down'), turn=.4)
    k = cl(r / 30); bk = 2.3 + 1.6 * k
    hgy = GY + 30 - lift_y(r)
    sk = 1 - lift_y(r) / 600                                          # his shadow on the path shrinks: he is off the ground
    ell(c, 290, GY + 60, 120 * sk, 22 * sk); c.set_source_rgba(0, 0, 0, .25 * sk); c.fill()
    _, hd = hoody(c, 290, hgy, .78, expr='bliss', pose='float' if lift_y(r) > 5 else 'stand', guitar=strum(f), f=f)
    tip = (hd[0] + 20, hd[1] - 150)
    string(c, hd, tip, sway=math.sin(r * .3) * 10); heart(c, *tip, bk)
    if r < 26:                                                        # the hose, still on, then it pops off
        ch = (100, GY + 70 - 130 * .85)
        c.move_to(*ch); c.curve_to(ch[0] + 120, ch[1] - 60, tip[0] - 160, tip[1] + 120, tip[0], tip[1] + 6)
        c.set_source_rgb(*INK); c.set_line_width(18); c.stroke_preserve(); c.set_source_rgb(*HOSE); c.set_line_width(9); c.stroke()
    notes(c, 290, hgy - 520, r, n=2, size=60)
def s11(c, f, r):  # she takes its hand -> ITS DATE; they walk off, the dog giving the cat a wide berth. His feet dangle above
    if r < 24:
        park(c, f, zoom=1.25, cy=1450)
        rs = 1.3; rx = 330; hp = A.hand_at(rx, 1760, rs, 1, 'hold2')
        E.eva(c, hp[0] + 40 + 76 * .95, 1760, .95, 'charmed', sip=.1, pose='holdlow' if r >= 8 else 'coffee', hand_to=hp if r >= 8 else None)
        A.myai(c, rx, 1760, rs, eye='open' if r < 8 else 'heart', arms=('down', 'hold2'))
        notes(c, 180, 380, r, n=2, size=50)
        return
    q = r - 24; k = q / 24
    wide(c, f, hoody_sit=False)
    ax = lerp(560, 760, k); ex = ax + 175
    A.myai(c, ax, GY + 60, .95, eye='heart', arms=('down', 'hold2'), turn=-.85, walk=q * .6)
    E.eva(c, ex, GY + 60, .9, 'charmed', sip=.1)
    E.dog(c, lerp(880, 960, k), GY + 140, .7, look=0, f=f)
    for i in range(2):                                                # his feet, dangling into the top of the frame
        x = 420 + (i * 2 - 1) * 36 + math.sin(f * .25 + i) * 12
        limb(c, [(x, 360 - 200), (x + 4, 470)], 34, JEANS)
        c.save(); c.translate(x + 4, 486); c.rotate((i * 2 - 1) * 1.2); ell(c, 0, 0, 28, 13); fs(c, SHOE, 5); c.restore()
    notes(c, 420, 560, r, n=2, size=54)
def s12(c, f, r):  # over the treetops, eyes still closed, one more bar
    sky(c, f, ty=1650)
    bob = math.sin(r * .15) * 20
    _, hd = hoody(c, 480, 1480 + bob, 1.05, expr='bliss', pose='float', guitar=strum(f), f=f)
    tip = (hd[0] + 10, hd[1] - 120)
    string(c, hd, tip); heart(c, *tip, 4.2)
    notes(c, 480, 860 + bob, r, n=3, size=70)
def s13(c, f, r):  # eyes open. He looks down
    sky(c, f, trees=False)
    K.hoodie(c, 540, 1020 + 150 * 2.4, 2.4 * 1.1)
    K.guitar(c, 560, 1700, 1.3, rot=GROT)
    K.hoodyz_head(c, 540, 1020, 2.4, era='young', expr='bliss' if r < 6 else 'shock', blink=False, gaze=0, op=0, rot=.0)
def s14(c, f, r):  # his view down: the empty bench, the cat alone; two tiny figures leaving
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, *hx('7cc66a')); g.add_color_stop_rgb(1, *hx('5aa84f')); c.set_source(g); c.paint()
    z = 1 + r * .004
    c.save(); c.translate(540, 1000); c.scale(z, z); c.translate(-540, -1000)
    c.move_to(-50, 1300); c.curve_to(400, 1150, 700, 1250, 1130, 1050); c.set_source_rgb(*hx('e9d8b0')); c.set_line_width(170); c.stroke()
    for x, y, rad in ((150, 400, 150), (900, 300, 170), (980, 1600, 160), (120, 1650, 140)):
        ell(c, x, y, rad, rad); fs(c, TREE_D, 6); ell(c, x - rad * .25, y - rad * .25, rad * .55, rad * .55); c.set_source_rgb(*TREE); c.fill()
    for i in range(4): rr(c, 380, 930 + i * 34, 330, 24, 6); fs(c, WOOD, 4)    # the bench from above
    ell(c, 640, 975, 42, 34); fs(c, TABBY, 5); ell(c, 670, 958, 20, 18); fs(c, TABBY, 4)   # the cat, curled
    for i, col in enumerate((hx('ffd23f'), WHITE)): ell(c, 860 + i * 34 + r * .8, 1120 - r * .3, 13, 13); fs(c, col, 4)
    c.restore()
    for q in (-1, 1): limb(c, [(540 + q * 60, -40), (540 + q * 64, 600)], 70, JEANS); ell(c, 540 + q * 70, 620, 52, 30); fs(c, SHOE, 6)   # his own feet, top of frame
def s15(c, f, r):  # one string, the wrong note: plonk
    sky(c, f, trees=False)
    K.hoodie(c, 540, 1020 + 150 * 2.4, 2.4 * 1.1)
    K.guitar(c, 560, 1700, 1.3, rot=GROT)
    K.arm(c, [(330, 1500), (320, 1700), (470 + (30 if r < 3 else 0), 1730)], 2.4)
    K.hoodyz_head(c, 540, 1020, 2.4, era='young', expr='deadpan', blink=False, gaze=0)
    if r >= 3: txt(c, 'plonk.', 540, 500, 96, NAVY, lw=0)
def s16(c, f, r):  # the cat, close: both paws over her ears, one eye open
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, *hx('8fd0ff')); g.add_color_stop_rgb(1, *hx('fff0c8')); c.set_source(g); c.paint()
    rr(c, -40, 1500, 1160, 140, 24); fs(c, WOOD, 8)
    s = 3.2; hx_, hy_ = 540, 1180
    ell(c, 540, 1420, 300, 130); fs(c, TABBY, 8)
    K._cat_head(c, hx_, hy_, s, False, 'sleep', 0)
    c.save(); c.translate(hx_, hy_); c.scale(s, s)                 # one eye open
    ell(c, 30, -6, 17, 14); c.set_source_rgb(*TABBY); c.fill()
    ell(c, 30, -4, 11, 14); fs(c, hx('b8e04a'), 4); ell(c, 27, -4, 4, 10); c.set_source_rgb(*INK); c.fill(); c.restore()
    k = oe(r / 6)
    for q in (-1, 1):                                               # paws up over the ears
        ear = (hx_ + q * 34 * s, hy_ - 62 * s)
        base = (hx_ + q * 200, 1400)
        p = (lerp(base[0], ear[0], k), lerp(base[1] - 20, ear[1], k))
        limb(c, [base, (lerp(base[0], ear[0], .5) + q * 70, lerp(base[1], ear[1], .5)), p], 64, TABBY)
        ell(c, *p, 52, 42); fs(c, TABBY, 8)
def s17(c, f, r):  # the balloon stretches... creak
    sky(c, f, trees=False)
    _, hd = hoody(c, 540, 1950, 1.25, expr='shock', pose='float', guitar=0, gaze=0, f=f)
    tip = (hd[0] - 60, hd[1] - 640)
    st = .08 * math.sin(r * 1.3) * cl(r / 8)
    string(c, hd, tip); heart(c, *tip, 3.4, sx=1 + st, sy=1 - st)
    for q in (-1, 1):                                               # strain marks either side
        for i in range(3):
            if r >= 6: c.move_to(tip[0] + q * (300 + i * 14), tip[1] - 300 + i * 50); c.line_to(tip[0] + q * (350 + i * 14), tip[1] - 320 + i * 50); c.set_source_rgb(*INK); c.set_line_width(7); c.stroke()
def s18(c, f, r):  # POP. A cartoon hold in the air
    sky(c, f, trees=False)
    hoody(c, 540, 1950, 1.25, expr='shock', pose='float', guitar=0, gaze=0, f=0)
    cx, cy = 560, 780; k = oe(r / 4)
    if r < 12:
        c.save(); c.translate(cx, cy); c.scale(.4 + .9 * k, .4 + .9 * k)
        c.move_to(0, -260)
        for i in range(1, 25):
            a = i * math.pi / 12; rad = 260 if i % 2 == 0 else 130
            c.line_to(rad * math.sin(a), -rad * math.cos(a))
        c.close_path(); fs(c, YEL, 10); c.restore()
        txt(c, 'POP!', cx, cy + 10, 130 * (.5 + .5 * k), RED, lw=10)
    for i in range(7):                                              # red shreds flying out
        a = i * 0.9 + .3; d = 120 + r * 26
        c.save(); c.translate(cx + math.cos(a) * d, cy + math.sin(a) * d + r * r * .6); c.rotate(r * .4 + i)
        rr(c, -26, -12, 52, 24, 10); fs(c, RED, 5); c.restore()
def s19(c, f, r):  # he drops out of the bottom of the frame
    sky(c, f, trees=False)
    y = 1950 + (r / 16) ** 2 * 1500
    for i in range(6):
        x = 300 + i * 90; c.move_to(x, y - 1300 - i * 30); c.line_to(x, y - 1700 - i * 30); c.set_source_rgba(1, 1, 1, .9); c.set_line_width(10); c.stroke()
    hoody(c, 540, y, 1.25, expr='shock', pose='float', arms=('flail', 'flail'), f=0)

DUR = [24, 36, 45, 36, 27, 36, 45, 42, 30, 48, 48, 42, 30, 24, 18, 30, 24, 24, 18]
FNS = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19]
SHOTS = []; _t = 0
for fn, d in zip(FNS, DUR): SHOTS.append((fn, _t, _t + d)); _t += d
NF = _t
def pill(f): return 'ITS DATE' if f >= SHOTS[10][1] + 8 else 'HIS DATE'

def draw(f):
    S = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(S)
    for fn, a, b in SHOTS:
        if a <= f < b:
            c.save(); fn(c, f, f - a); c.restore(); c.identity_matrix(); Sh.topbar(c, pill(f)); break
    return S

if __name__ == '__main__':
    if sys.argv[1:2] == ['frames']:
        for f in map(int, sys.argv[2:]): draw(f).write_to_png(os.path.join(HERE, f'chk_{f:03d}.png'))
    else:
        p = subprocess.Popen(f'ffmpeg -y -v error -f rawvideo -pix_fmt bgra -s {W}x{H} -r 30 -i - -vf format=yuv420p -c:v libx264 -crf 18 -preset veryfast -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709 {os.path.join(HERE, "tmp_video.mp4")}'.split(), stdin=subprocess.PIPE)
        for f in range(NF): p.stdin.write(bytes(draw(f).get_data()))
        p.stdin.close(); assert p.wait() == 0; os.rename(os.path.join(HERE, 'tmp_video.mp4'), os.path.join(HERE, 'video.mp4')); print('video ok', NF)
