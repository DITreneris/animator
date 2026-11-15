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
K.FACES['spiral'] = ('spiral', ('worried', 'worried'), 'wobble')
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

# ---------------- voices: where each line sits, and the lip sync that follows it ----------------
VO = [('h_whisper', 2, .07, .7), ('ai_watch', 4, .15, .6), ('ai_turn', 6, .25, .6), ('h_oh', 12, .35, .55), ('h_whoa', 17, .25, .55)]
_ENV = {}
def env(name):
    """Per-frame loudness of a take, 0..1 (30 fps), smoothed a touch so the mouth doesn't chatter."""
    if name not in _ENV:
        import soundfile as sf, numpy as np
        x, sr = sf.read(os.path.join(HERE, 'vo', name + '.wav')); x = x if x.ndim == 1 else x[:, 0]
        n = sr // 30; m = len(x) // n
        e = 20 * np.log10(np.sqrt((x[:m * n].reshape(m, n) ** 2).mean(1)) + 1e-6)      # dB per frame
        lo, hi = np.percentile(e, 35), np.percentile(e, 97)                             # floor = the gaps between syllables
        e = np.clip((e - lo) / (hi - lo + 1e-9), 0, 1)
        e = np.convolve(e, [.2, .6, .2], 'same'); _ENV[name] = e ** 1.3
    return _ENV[name]
def talk(f, name):
    """How open the mouth is on frame f for this line (0 when it isn't being spoken)."""
    for nm, shot, off, g in VO:
        if nm == name:
            i = f - SHOTS[shot][1] - int(round(off * 30)); e = env(name)
            return float(e[i]) if 0 <= i < len(e) else 0.0
    return 0.0

def ai(c, *a, f=0, **k):
    """MY AI with its idle bob (secondary motion)."""
    k.setdefault('bob', math.sin(f * .18) * 5 * a[2] if len(a) > 2 else 0)
    A.myai(c, *a, **k)

def tuft(c, x, hy, s):
    """Messed-up hair after the landing: two loose cowlick curls sticking up off the crown, in his hair colour."""
    for dx, q, ln in ((-18, -1, 70), (22, 1, 58)):
        c.move_to(x + dx * s, hy - 120 * s); c.curve_to(x + (dx + q * 10) * s, hy - (120 + ln) * s, x + (dx + q * 44) * s, hy - (120 + ln) * s, x + (dx + q * 36) * s, hy - (120 + ln * .6) * s)
        c.set_source_rgb(*INK); c.set_line_width(20 * s); c.stroke_preserve(); c.set_source_rgb(.36, .22, .13); c.set_line_width(12 * s); c.stroke()

# ---------------- Hoody, full body ----------------
GROT = -.45; GS = .6                                     # the guitar on him: rotation and scale (times s)
def guitar_points(x, hy, s):
    """Where the guitar sits on Hoody: body centre, the fret hand on the neck, the headstock (where the balloon ties)."""
    body = (x + 20 * s, hy + 370 * s)
    at = lambda d: (body[0] + d * GS * s * math.cos(GROT), body[1] + d * GS * s * math.sin(GROT))
    return body, at(250), at(440)

def hoody(c, x, gy, s, expr='calm', pose='stand', arms=('rest', 'rest'), gaze=0, op=0, rot=0, prop=None, seat=None,
          guitar=None, f=0, legs='dangle', blink=None, hair=False, soles=False):
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
            hip = (x + q * 40 * s, waist - 10 * s); toe = 0
            if pose == 'stand':
                knee = (x + q * 44 * s, waist + 140 * s); foot = (x + q * 44 * s, gy - 14 * s)
            elif legs == 'dangle':                                       # loose, swaying, toes pointed
                sw = math.sin(f * .22 + q * 1.3) * 18 * s
                knee = (x + q * 46 * s + sw * .5, waist + 140 * s); foot = (x + q * 40 * s + sw * 1.4, gy - 14 * s); toe = q * 1.25
            elif legs == 'kick':                                         # startled: knees jerk up in turn
                up = max(0, math.sin(f * 1.1 + (q > 0) * math.pi)) * 110 * s
                knee = (x + q * 56 * s, waist + 140 * s - up); foot = (knee[0] + q * 30 * s, knee[1] + 140 * s); toe = q * .6
            elif legs == 'stiff':                                        # rigid, together, toes down
                knee = (x + q * 22 * s, waist + 140 * s); foot = (x + q * 18 * s, gy - 14 * s); toe = q * 1.45
            else:                                                        # 'pedal': running on air
                ph = f * .9 + (q > 0) * math.pi
                knee = (x + q * 40 * s + math.cos(ph) * 30 * s, waist + 110 * s + math.sin(ph) * 50 * s)
                foot = (knee[0] + math.cos(ph + .8) * 40 * s, knee[1] + 130 * s); toe = .3 * q
            limb(c, [hip, knee, foot], 40 * s, JEANS)
            c.save(); c.translate(foot[0] + q * 4 * s, foot[1] + 6 * s); c.rotate(toe)
            ell(c, 0, 0, 32 * s, 15 * s); fs(c, SHOE, max(3, 5 * s))
            if soles: ell(c, 0, 6 * s, 25 * s, 8 * s); c.set_source_rgb(*hx('8a8f9c')); c.fill()
            c.restore()
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
    if blink is None: blink = K.blinking(f, 3) and K.FACES.get(expr, ('open',))[0] != 'shut'
    K.hoodyz_head(c, x, hy, s, era='young', expr=expr, blink=blink, gaze=gaze, op=op)
    if hair: tuft(c, x, hy, s)
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

def s1(c, f, r):   # frame 0: just landed back on the bench - dust settling, hair messed - hand on chin, eyes locked off right
    head_close(c, f, 'calm', gaze=26, op=.35)

    K.arm(c, [(240, 1400), (250, 1260), (330, 1180)], 2.0)
def s2(c, f, r):   # she walks in and sits at the far end with coffee and the dog
    wide(c, f, hoody_kw=dict(expr='shock', gaze=24, f=f))
    ai(c, 140, GY + 40, .95, eye='open', look=(14, 0), f=f)
    k = oe(r / 26); ex = lerp(980, 860, k)
    col = E.dog(c, ex - 135, GY + 40, .8, look=0, f=f)
    hand = E.eva(c, ex, GY + 30, .9, 'evacalm', sip=.2, walk=r * .55 if k < .97 else None, blink=K.blinking(f, 7))
    E.leash(c, hand, col, sag=50)
def s3(c, f, r):   # "Help me impress her!" - his lips follow the whisper
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, *hx('8fd0ff')); g.add_color_stop_rgb(1, *hx('fff0c8')); c.set_source(g); c.paint()
    hoody(c, 400, 1820, 1.25, expr='hopeful', pose='stand', arms=('rest', 'chin'), rot=.06, op=.15 + .6 * talk(f, 'h_whisper'), f=f)
    ai(c, 800, 1700, 1.15, eye='happy', tilt=-10, look=(-10, 0), f=f)
    bubble(c, ['HELP ME', 'IMPRESS HER!'], r - 2, (430, 860), cy=520, cx=480)
def s4(c, f, r):   # 0.8 s: the dog sniffs toward the cat; one eye; it backs off behind her
    park(c, f, zoom=1.6, cy=1500)
    rr(c, -40, 1380, 420, 50, 14); fs(c, WOOD, 7)
    Sh.cat_one_eye(c, 150 + 92 * 1.3, 1384, 1.3, open_eye=(r >= 7))
    dx = lerp(820, 660, oe(r / 8)) if r < 11 else lerp(660, 900, oe((r - 11) / 8))
    E.dog(c, dx, 1760, 1.6, look=1 if r >= 11 else 0, f=f)
    E.leash(c, (1120, 1250), (dx - 2 * 1.6, 1760 - 98 * 1.6), sag=80)
    if r >= 11: Sh.sweat(c, dx + 70, 1480, 1.1)
def s5(c, f, r):   # "Watch!" - eyes squash and the antenna glows with its voice
    park(c, f, zoom=1.3, cy=1400)
    E.eva(c, 870, 1700, .95, 'evacalm', sip=.2, blink=K.blinking(f, 7))     # she's who it's for
    ai(c, 400, 1780, 1.6, eye='focus', arms=('down', 'wait' if r < 10 else 'down'), turn=.35, talk=talk(f, 'ai_watch'), f=f)
    bubble(c, ['WATCH!'], r - 4, (400 + 14 * 1.6, 1780 - 420 * 1.6), cy=560, cx=440)
def s6(c, f, r):   # the rose; she is impressed
    park(c, f, zoom=1.2, cy=1450)
    k = oe((r - 4) / 10)
    ai(c, 330, 1720, 1.25, eye='focus', arms=('down', 'offer'), props=(None, A.rose), rot=-.12 * k, f=f)
    E.eva(c, 780, 1760, 1.0, 'impressed' if r >= 10 else 'evacalm', sip=.1, blink=K.blinking(f, 7))
def guitar_held(c, x, y, rot, s=.6):
    K.guitar(c, x, y, s, rot=rot)
    return (x + 440 * s * math.cos(rot), y + 440 * s * math.sin(rot))
def s7(c, f, r):   # "Your turn!": MY AI holds the guitar (balloon tied on) and passes it hand to hand
    park(c, f, zoom=1.2, cy=1450)
    rx, rs = 770, 1.15
    k = ss(cl((r - 14) / 10))                                         # the handover
    if k < 1:
        hoody(c, 360, 1820, 1.0, expr='hopeful', arms=('rest', 'take'), f=f)
        h0 = A.hand_at(rx, 1800, rs, -1, 'give')
        gp = (lerp(h0[0] - 60, 380, k), lerp(h0[1] + 20, 1300, k))     # from its hand to his chest
        ai(c, rx, 1800, rs, eye='happy', arms=('give', 'down'), turn=-.6, talk=talk(f, 'ai_turn'), f=f)
        hd = guitar_held(c, *gp, lerp(-1.0, GROT, k))
    else:
        _, hd = hoody(c, 360, 1820, 1.0, expr='happy', guitar=0, f=f)
        ai(c, rx, 1800, rs, eye='happy', arms=('down', 'down'), turn=-.6, talk=talk(f, 'ai_turn'), f=f)
    bob = math.sin(f * .15) * 8
    string(c, hd, (hd[0] + 30, hd[1] - 250 + bob)); heart(c, hd[0] + 30, hd[1] - 250 + bob, 1.7)
    ell(c, *hd, 9, 9); c.set_source_rgb(*INK); c.fill()                       # the knot on the headstock
    bubble(c, ['YOUR TURN!'], r - 2, (rx - 24 * rs, 1800 - 420 * rs), cy=560, cx=640)
def s8(c, f, r):   # eyes closed, giving it everything
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, *hx('ffd36b')); g.add_color_stop_rgb(1, *hx('ff8fa6')); c.set_source(g); c.paint()
    _, hd = hoody(c, 470, 2350, 1.9, expr='bliss', guitar=strum(f), rot=-.06 + .05 * math.sin(r * .3), f=f)
    tip = (hd[0] - 60, hd[1] - 330 + math.sin(f * .15) * 10)          # the heart balloon, still tied to the headstock
    string(c, hd, tip); heart(c, *tip, 1.9); ell(c, *hd, 12, 12); c.set_source_rgb(*INK); c.fill()
    notes(c, 470, 900, r, size=96)
def sparkles(c, x, y, r, n=6):
    for i in range(n):
        a = i * 1.05 + r * .3; d = 40 + ((r * 9 + i * 23) % 120)
        c.save(); c.translate(x + math.cos(a) * d, y - abs(math.sin(a)) * d); c.rotate(r * .2 + i); c.scale(.5, .5)
        c.move_to(0, -30)
        for j in range(1, 8): rad = 30 if j % 2 == 0 else 11; c.line_to(rad * math.sin(j * math.pi / 4), -rad * math.cos(j * math.pi / 4))
        c.close_path(); c.set_source_rgb(*(YEL if i % 2 else hx('ff6fb5'))); c.fill(); c.restore()
def s9(c, f, r):   # MY AI, the proud stage tech: a hose from its chest, confetti sparkles, a wave to the performer
    park(c, f, zoom=1.4, cy=1500)
    rs = 1.6; rx, gy = 330, 1900
    p = max(0, math.sin((r - 8) * math.pi / 6)) if r >= 8 else 0      # one pump stroke every 12 frames: it squashes down and springs up
    c.save(); c.translate(rx, gy); c.scale(1 + .06 * p, 1 - .09 * p); c.translate(-rx, -gy)
    ai(c, rx, gy, rs, eye='happy', arms=('hold', 'wave' if r >= 10 else 'down'), tilt=8, f=f)
    c.restore()
    k = cl((r - 8) / 18); bk = 1.2 + 1.1 * k + .06 * math.sin(r * 1.4) * k
    tip = (800, 1100)
    string(c, tip, (900, 1960)); heart(c, *tip, bk)
    ch = (rx, gy - 130 * rs)
    reach = oe(r / 8); end = (lerp(ch[0] + 60, tip[0], reach), lerp(ch[1], tip[1] + 10, reach))
    P = [ch, (ch[0] + 160, ch[1] + 140), (end[0] - 80, end[1] + 260), end]
    c.move_to(*P[0]); c.curve_to(*P[1], *P[2], *P[3])
    c.set_source_rgb(*INK); c.set_line_width(42); c.stroke_preserve(); c.set_source_rgb(*hx('ff8a3d')); c.set_line_width(28); c.stroke()
    if r >= 8 and p > .3:                                             # each stroke: a puff of air at the balloon, and the hose swells
        for i in range(4):
            a_ = -.5 + i * .8; ell(c, end[0] + math.cos(a_) * 60 * p, end[1] - 20 + math.sin(a_) * 40 * p, 16 * p, 16 * p); c.set_source_rgba(1, 1, 1, .9); c.fill()
        txt(c, 'PFF', end[0] + 150, end[1] + 40, 54, NAVY, lw=0)
    ell(c, *ch, 30, 30); fs(c, hx('ff8a3d'), 6)
    if r >= 8: sparkles(c, end[0], end[1] + 20, r)
def lift_y(r):                                                        # shot 10: how far his feet are off the ground
    return 380 * ss(cl((r - 14) / 34))
def s10(c, f, r):  # the balloon swells; he lifts off still playing. MY AI's alarm: wide eyes, reaching up. She glances: sip, brow, smile
    park(c, f)
    bench(c, 520, 1010, SEAT, GY)
    Sh.cat_one_eye(c, 640, SEAT - 6, .62, open_eye=False)
    col = E.dog(c, 880 - 135, GY + 50, .8, look=0, f=f)
    hand = E.eva(c, 880, GY + 40, .9, 'evacalm', sip=.2, pose='glance' if r >= 20 else 'coffee', blink=K.blinking(f, 7))
    E.leash(c, hand, col, sag=50)
    alarm = r >= 30
    ai(c, 100, GY + 70, .85, eye='wide' if alarm else 'happy', arms=('up', 'up') if r >= 36 else (('hold', 'up') if alarm else ('hold', 'down')),
       look=(14, -16) if alarm else (0, 0), turn=.4, f=f)
    lift = lift_y(r)
    sk = 1 - lift / 600
    ell(c, 290, GY + 60, 120 * sk, 22 * sk); c.set_source_rgba(0, 0, 0, .25 * sk); c.fill()
    k = cl(r / 30); bk = 2.3 + 1.6 * k
    hgy = GY + 30 - lift - max(0, r - 48) * 9                         # and on up, out of the top
    _, hd = hoody(c, 290, hgy, .78, expr='bliss', pose='float' if lift > 5 else 'stand', guitar=strum(f), f=f, legs='dangle')
    tip = (hd[0] + 20, hd[1] - 150 + math.sin(f * .15) * 8)
    string(c, hd, tip, sway=math.sin(r * .3) * 10); heart(c, *tip, bk)
    if r < 26:
        ch = (100, GY + 70 - 130 * .85)
        c.move_to(*ch); c.curve_to(ch[0] + 120, ch[1] - 60, tip[0] - 160, tip[1] + 120, tip[0], tip[1] + 6)
        c.set_source_rgb(*INK); c.set_line_width(18); c.stroke_preserve(); c.set_source_rgb(*HOSE); c.set_line_width(9); c.stroke()
        if r >= 4: sparkles(c, tip[0], tip[1] + 10, r, n=4)
    if 30 <= r < 40: txt(c, '!', 100, GY - 330, 110, RED, lw=8)
    notes(c, 290, hgy - 520, r, n=2, size=60)

# ---- from above: the park seen past his own shoes
def top_legs(c, f, mode, s=2.1, y=620, x=540):
    """His legs hanging into the top of a view straight down: the hoodie hem at the top edge, the shoes nearest the camera."""
    ell(c, x + 60, 1180, 90, 34); c.set_source_rgba(0, 0, 0, .22); c.fill()        # his shadow on the grass, far below
    hoody(c, x, y, s, pose='float', legs=mode, arms=('up', 'up'), f=f, blink=False, soles=True)
    c.move_to(x + 30, -10); c.line_to(x + 34, y - 300 * s); c.set_source_rgb(*INK); c.set_line_width(4); c.stroke()
def ground(c, f, z):
    """The park from above at zoom z (1 = just off the ground, smaller = higher). Returns a mapper for ground points."""
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, *hx('84cc72')); g.add_color_stop_rgb(1, *hx('5aa84f')); c.set_source(g); c.paint()
    m = lambda x, y: (540 + (x - 540) * z, 1250 + (y - 1250) * z)
    c.save(); c.translate(540, 1250); c.scale(z, z); c.translate(-540, -1250)
    for i in range(60):                                               # grass tufts
        gx, gy_ = (i * 197) % 1500 - 200, (i * 331) % 2200 - 150
        c.move_to(gx, gy_); c.line_to(gx + 8, gy_ - 22); c.line_to(gx + 16, gy_); c.set_source_rgb(*hx('4c9a43')); c.set_line_width(4); c.stroke()
    c.move_to(-300, 1700); c.curve_to(300, 1480, 700, 1560, 1500, 1300); c.set_source_rgb(*hx('e9d8b0')); c.set_line_width(240); c.stroke()
    for x, y, rad in ((-80, 520, 300), (1160, 420, 320), (1180, 2200, 300), (-120, 2250, 280)):
        ell(c, x + 30, y + 40, rad, rad); c.set_source_rgba(0, 0, 0, .18); c.fill()
        ell(c, x, y, rad, rad); fs(c, TREE_D, 8); ell(c, x - rad * .2, y - rad * .2, rad * .6, rad * .6); c.set_source_rgb(*TREE); c.fill()
    c.restore()
    return m
def small_bench_cat(c, m, z, cat_eye=False):
    bx, by = m(500, 1360)
    c.save(); c.translate(bx, by); c.scale(.45 * z / .5, .45 * z / .5 * .8)
    ell(c, 0, 40, 330, 50); c.set_source_rgba(0, 0, 0, .2); c.fill()
    bench(c, -280, 280, 0, 90)
    Sh.cat_one_eye(c, 180, -6, .8, open_eye=cat_eye)
    c.restore()
def s11(c, f, r):  # she takes its hand (it's still looking up after him) -> ITS DATE; then from above: him leaving, them below
    if r < 30:
        park(c, f, zoom=1.25, cy=1450)
        rs = 1.3; rx = 330; hp = A.hand_at(rx, 1760, rs, 1, 'hold2')
        took = r >= 8
        E.eva(c, hp[0] + 40 + 76 * .95, 1760, .95, 'charmed', sip=.1, pose='holdlow' if took else 'reach', hand_to=hp if took else None, blink=K.blinking(f, 7))
        eye = 'wide' if r < 12 else ('open' if r < 18 else 'heart')
        look = (6, -20) if r < 12 else (14, 14) if r < 18 else (10, 0)
        ai(c, rx, 1760, rs, eye=eye, look=look, arms=('up' if r < 12 else 'down', 'hold2'), f=f)
        notes(c, 180, 420, r, n=2, size=50)
        return
    q = r - 30; k = q / 36
    z = lerp(.62, .5, k)
    m = ground(c, f, z)
    small_bench_cat(c, m, z * 1.4)
    cx_, cy_ = m(760, 1720)
    c.save(); c.translate(cx_, cy_); sc = z * 1.15
    ell(c, 0, 10, 200 * sc, 40 * sc); c.set_source_rgba(0, 0, 0, .2); c.fill()
    hp = A.hand_at(-120 * sc, 0, sc, 1, 'hold2')
    E.eva(c, hp[0] + 40 * sc + 76 * sc, 0, sc, 'charmed', sip=.1, pose='holdlow', hand_to=hp)
    A.myai(c, -120 * sc, 0, sc, eye='heart', arms=('down', 'hold2'))
    E.dog(c, 260 * sc, 30 * sc, sc * .8, look=0, f=f)
    c.restore()
    top_legs(c, f, 'dangle', y=620 - k * 60)
    notes(c, 540, 820, r, n=2, size=54)
def s12(c, f, r):  # over the treetops, eyes still closed, one more bar
    sky(c, f, ty=1860)
    bob = math.sin(r * .15) * 20
    _, hd = hoody(c, 480, 1400 + bob, 1.05, expr='bliss', pose='float', guitar=strum(f), f=f, legs='dangle')
    tip = (hd[0] + 10, hd[1] - 120)
    string(c, hd, tip); heart(c, *tip, 4.2)
    notes(c, 480, 780 + bob, r, n=3, size=70)
def s13(c, f, r):  # eyes open. "oh" - lips on the take
    sky(c, f, trees=False)
    K.hoodie(c, 540, 1020 + 150 * 2.4, 2.4 * 1.1)
    K.guitar(c, 560, 1700, 1.3, rot=GROT)
    hs = (560 + 440 * 1.3 * math.cos(GROT), 1700 + 440 * 1.3 * math.sin(GROT))   # the balloon string, up out of frame
    c.move_to(*hs); c.curve_to(hs[0] - 40, hs[1] - 400, hs[0] - 120, 600, hs[0] - 140, -10); c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
    K.hoodyz_head(c, 540, 1020, 2.4, era='young', expr='bliss' if r < 6 else 'shock', blink=False, gaze=0, op=.2 + .8 * talk(f, 'h_oh'))
def s14(c, f, r):  # the gap, wide: him a speck in the sky; below, the bench with the cat, and the couple walking off hand in hand
    park(c, f)
    bench(c, -60, 300, SEAT, GY)
    Sh.cat_one_eye(c, 200, SEAT - 6, .62, open_eye=r >= 14)
    rs = .82; rx = 420 + r * 4
    hp = A.hand_at(rx, GY + 60, rs, 1, 'hold2')
    E.dog(c, rx - 140, GY + 90, .62, look=0, f=f)
    E.eva(c, hp[0] + 40 * rs + 76 * rs * .95 / .95, GY + 60, rs * .95, 'charmed', sip=.1, pose='holdlow', hand_to=hp, walk=r * .5)
    A.myai(c, rx, GY + 60, rs, eye='heart', arms=('down', 'hold2'), walk=r * .5)
    if r >= 8:                                                        # a little heart pops over the two of them
        k = max(.05, oe((r - 8) / 6)); c.save(); c.translate(rx + 120, GY - 680 - (r - 8) * 3); c.scale(.6 * k, .6 * k)
        c.move_to(0, 18); c.curve_to(-30, -2, -18, -30, 0, -12); c.curve_to(18, -30, 30, -2, 0, 18); c.close_path(); fs(c, A.PINK, 5); c.restore()
    hy_ = 1010 + math.sin(r * .2) * 10                                 # him, small, high above the trees
    _, hd = hoody(c, 250, hy_, .42, expr='shock', pose='float', guitar=0, legs='dangle', f=f, blink=False)
    string(c, hd, (hd[0] + 10, hd[1] - 120)); heart(c, hd[0] + 10, hd[1] - 120, 1.4)
def s15(c, f, r):  # an insert: one finger, one string, the wrong note - then his face: plonk
    if r < 12:
        g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, *SKY0); g.add_color_stop_rgb(1, *SKY1); c.set_source(g); c.paint()
        c.save(); c.translate(540, 1100); c.rotate(-.5)
        rr(c, -900, -130, 1800, 260, 30); fs(c, hx('7a4a25'), 10)       # the neck, close
        for i in range(-3, 4): c.rectangle(i * 240 - 8, -130, 16, 260); c.set_source_rgb(*hx('d9d9d9')); c.fill()
        for j in range(6):
            yy = -100 + j * 40
            if j == 3:                                                  # the plucked string wobbles
                amp = (20 if r >= 4 else 0) * math.exp(-(r - 4) * .25) if r >= 4 else -26 * r / 4
                c.move_to(-900, yy)
                for xx in range(-900, 901, 30): c.line_to(xx, yy + amp * math.sin((xx + 900) / 1800 * math.pi) * (math.cos(r * 2.4) if r >= 4 else 1))
            else: c.move_to(-900, yy); c.line_to(900, yy)
            c.set_source_rgb(*hx('f2f2f2')); c.set_line_width(7 if j < 3 else 5); c.stroke()
        c.restore()
        fx_, fy_ = (600, 1050 - (26 if r < 4 else -30)) if r < 4 else (640, 1150)
        limb(c, [(820, 1500), (700, 1300), (fx_, fy_)], 90, K.SKIN); ell(c, fx_, fy_, 50, 44); fs(c, K.SKIN, 8)
        if r >= 4: txt(c, 'plonk.', 540, 640, 110, NAVY, lw=0)
        return
    sky(c, f, trees=False)
    K.hoodie(c, 540, 1020 + 150 * 2.4, 2.4 * 1.1)
    K.guitar(c, 560, 1700, 1.3, rot=GROT)
    hs = (560 + 440 * 1.3 * math.cos(GROT), 1700 + 440 * 1.3 * math.sin(GROT))   # the balloon string, up out of frame
    c.move_to(*hs); c.curve_to(hs[0] - 40, hs[1] - 400, hs[0] - 120, 600, hs[0] - 140, -10); c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
    K.hoodyz_head(c, 540, 1020, 2.4, era='young', expr='deadpan', blink=False, gaze=0)
def s16(c, f, r):  # the cat, close: both paws over her ears, one eye open
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, *hx('8fd0ff')); g.add_color_stop_rgb(1, *hx('fff0c8')); c.set_source(g); c.paint()
    rr(c, -40, 1500, 1160, 140, 24); fs(c, WOOD, 8)
    s = 3.2; hx_, hy_ = 540, 1180
    ell(c, 540, 1420, 300, 130); fs(c, TABBY, 8)
    K._cat_head(c, hx_, hy_, s, False, 'sleep', 0)
    c.save(); c.translate(hx_, hy_); c.scale(s, s)
    ell(c, 30, -6, 17, 14); c.set_source_rgb(*TABBY); c.fill()
    ell(c, 30, -4, 11, 14); fs(c, hx('b8e04a'), 4); ell(c, 27, -4, 4, 10); c.set_source_rgb(*INK); c.fill(); c.restore()
    k = oe(r / 6)
    for q in (-1, 1):
        ear = (hx_ + q * 34 * s, hy_ - 62 * s); base = (hx_ + q * 200, 1400)
        p = (lerp(base[0], ear[0], k), lerp(base[1] - 20, ear[1], k))
        limb(c, [base, (lerp(base[0], ear[0], .5) + q * 70, lerp(base[1], ear[1], .5)), p], 64, TABBY)
        if k > .8:                                                    # ears pressed flat, tips sticking out sideways
            c.move_to(p[0] + q * 30, p[1] - 22); c.line_to(p[0] + q * 110, p[1] - 4); c.line_to(p[0] + q * 34, p[1] + 16); c.close_path(); fs(c, TABBY, 7)
            c.move_to(p[0] + q * 44, p[1] - 10); c.line_to(p[0] + q * 88, p[1] - 3); c.line_to(p[0] + q * 46, p[1] + 6); c.close_path(); c.set_source_rgb(*hx('ffb3a7')); c.fill()
        ell(c, *p, 52, 42); fs(c, TABBY, 8)
STEPS = (0, 9, 18)                                                    # the balloon swells in three visible steps (a creak each)
def s17(c, f, r):  # the balloon stretches... creak, creak, creak
    sky(c, f, trees=False)
    _, hd = hoody(c, 540, 1950, 1.25, expr='shock', pose='float', guitar=0, gaze=0, f=f, legs='stiff')
    n = sum(r >= t for t in STEPS); kk = 3.2 + .45 * (n - 1) + .25 * oe(cl((r - STEPS[n - 1]) / 4)) - .25
    st = .07 * math.sin((r - STEPS[n - 1]) * 1.6) * math.exp(-(r - STEPS[n - 1]) * .3)
    tip = (hd[0] - 60, hd[1] - 640)
    string(c, hd, tip); heart(c, *tip, kk, sx=1 + st, sy=1 - st)
    j = .015 * n * math.sin(r * 3.1)                                  # the skin shivers harder with each step
    heart(c, tip[0] + 6 * n * math.sin(r * 2.3), tip[1], kk * (1.03 + .01 * n), sx=1 + st + j, sy=1 - st - j, op=.25)
def s18(c, f, r):  # POP. A cartoon hold in the air. "whoa" - lips on the take
    sky(c, f, trees=False)
    hoody(c, 540, 1950, 1.25, expr='shock', pose='float', guitar=0, gaze=0, f=f, legs='stiff', op=.3 + .7 * talk(f, 'h_whoa'))
    cx, cy = 560, 780; k = oe(r / 4)
    if r < 12:
        c.save(); c.translate(cx, cy); c.scale(.4 + .9 * k, .4 + .9 * k)
        c.move_to(0, -260)
        for i in range(1, 25):
            a = i * math.pi / 12; rad = 260 if i % 2 == 0 else 130
            c.line_to(rad * math.sin(a), -rad * math.cos(a))
        c.close_path(); fs(c, YEL, 10); c.restore()
        txt(c, 'POP!', cx, cy + 10, 130 * (.5 + .5 * k), RED, lw=10)
    for i in range(7):
        a = i * 0.9 + .3; d = 120 + r * 26
        c.save(); c.translate(cx + math.cos(a) * d, cy + math.sin(a) * d + r * r * .6); c.rotate(r * .4 + i)
        rr(c, -26, -12, 52, 24, 10); fs(c, RED, 5); c.restore()
def s19(c, f, r):  # he drops out of the bottom of the frame - legs pedalling, the guitar tumbling after him
    sky(c, f, trees=False)
    y = 1950 + (r / 10) ** 2 * 1500
    for i in range(6):
        x = 300 + i * 90; c.move_to(x, y - 1300 - i * 30); c.line_to(x, y - 1700 - i * 30); c.set_source_rgba(1, 1, 1, .9); c.set_line_width(10); c.stroke()
    hoody(c, 540, y, 1.25, expr='shock', pose='float', arms=('flail', 'flail'), f=f, legs='pedal', op=.6)
    gy_ = 1300 + (r / 10) ** 2 * 1300
    K.guitar(c, 860, gy_, .7, rot=r * .5)

IMPACT = 3                                                            # shot 20: the frame he hits the bench
def s20(c, f, r):  # BOOM: he slams onto the bench, the camera shakes, the cat doesn't care; dizzy; snap back to frame 0
    if r >= 16: s1(c, f, 0); return                                   # the last frames are frame 0: a seamless loop
    if r < 9:                                                         # wide: the impact
        sh = 26 * math.exp(-(r - IMPACT) * .45) if r >= IMPACT else 0
        c.translate(sh * math.sin(r * 7.3), sh * math.cos(r * 5.1))
        park(c, f)
        sag = 16 * math.exp(-(r - IMPACT) * .6) if r >= IMPACT else 0
        c.save(); c.translate(0, sag); bench(c, 220, 780, SEAT, GY); c.restore()
        Sh.cat_one_eye(c, 700, SEAT - 6 + sag, .62, open_eye=(5 <= r < 8))   # one eye: unbothered
        if r < IMPACT:                                                # the streak coming down
            y1 = SEAT - 120 + (r - IMPACT) * 500
            rr(c, 360, y1 - 900, 120, 900, 60); c.set_source_rgba(*NAVY, .85); c.fill()
            for i in range(4): c.move_to(330 + i * 60, y1 - 1000); c.line_to(330 + i * 60, y1 - 1400); c.set_source_rgba(1, 1, 1, .9); c.set_line_width(8); c.stroke()
            return
        if r <= IMPACT + 1:                                           # the impact frame: an ink starburst behind him
            c.save(); c.translate(420, SEAT - 200); c.move_to(0, -420)
            for i in range(1, 33): rad = 420 if i % 2 == 0 else 200; c.line_to(rad * math.sin(i * math.pi / 16), -rad * math.cos(i * math.pi / 16))
            c.close_path(); fs(c, YEL, 12); c.restore()
        q = r - IMPACT; sq = .35 * math.exp(-q * .7) * math.cos(q * 1.6)
        c.save(); c.translate(420, SEAT + sag); c.scale(1 + sq, 1 - sq); c.translate(-420, -SEAT - sag)
        hoody(c, 420, SEAT + sag, .82, expr='spiral' if r > IMPACT + 1 else 'shock', pose='sit', seat=(220, 780), arms=('flail', 'flail'), f=f, blink=False)
        c.restore()
        for i in range(9):                                            # the dust bursts out sideways
            a = math.pi + i * math.pi / 8; d = 120 + q * 70
            ell(c, 420 + math.cos(a) * d * 1.6, GY - 10 + math.sin(a) * d * .35, 70 + q * 8, 44 + q * 5)
            c.set_source_rgba(.88, .80, .64, max(0, .85 - q * .12)); c.fill()
        return
    q = r - 9                                                         # close-up: two bounces, dizzy, then the snap
    y = 1020 - 70 * abs(math.cos(q * 1.1)) * math.exp(-q * .45)
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, *hx('8fd0ff')); g.add_color_stop_rgb(1, *hx('fff0c8')); c.set_source(g); c.paint()
    K.hoodie(c, 540, y + 150 * 2.4, 2.4 * 1.1)
    K.hoodyz_head(c, 540, y, 2.4, era='young', expr='spiral', blink=False)

    for i in range(3):                                                # stars circling his head
        a = q * .7 + i * 2.1
        c.save(); c.translate(540 + math.cos(a) * 300, y - 300 + math.sin(a) * 60); c.scale(.8, .8); c.move_to(0, -30)
        for j in range(1, 10): rad = 30 if j % 2 == 0 else 12; c.line_to(rad * math.sin(j * math.pi / 5), -rad * math.cos(j * math.pi / 5))
        c.close_path(); fs(c, YEL, 4); c.restore()

DUR = [24, 36, 45, 24, 27, 36, 45, 39, 30, 63, 66, 36, 30, 30, 30, 30, 27, 24, 12, 22]
FNS = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19, s20]
SHOTS = []; _t = 0
for fn, d in zip(FNS, DUR): SHOTS.append((fn, _t, _t + d)); _t += d
NF = _t
def pill(f): return 'ITS DATE' if SHOTS[10][1] + 8 <= f < SHOTS[19][1] + 16 else 'HIS DATE'      # resets with the snap
def pulse(c, f):
    """The moment the label flips to ITS DATE, the pill pops big and settles: the punchline can't be missed."""
    t = f - (SHOTS[10][1] + 8)
    if not 0 <= t < 16: return
    k = 1 + .75 * (1 - t / 16) ** 2 * (1 if t > 1 else t / 1)
    c.select_font_face('Lilita One'); c.set_font_size(58); w = max(200, c.text_extents('ITS DATE').width + 96)
    px, iy = 1020 - w / 2, 222 + 69
    c.save(); c.translate(px - 40 * (k - 1), iy + 60 * (k - 1)); c.scale(k, k)
    rr(c, -w / 2, -44, w, 88, 44); fs(c, YEL, 7); txt(c, 'ITS DATE', 0, 0, 58, INK, lw=0); c.restore()

def draw(f):
    S = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(S)
    for fn, a, b in SHOTS:
        if a <= f < b:
            c.save(); fn(c, f, f - a); c.restore(); c.identity_matrix(); Sh.topbar(c, pill(f)); pulse(c, f); break
    return S

if __name__ == '__main__':
    if sys.argv[1:2] == ['frames']:
        for f in map(int, sys.argv[2:]): draw(f).write_to_png(os.path.join(HERE, f'chk_{f:03d}.png'))
    else:
        p = subprocess.Popen(f'ffmpeg -y -v error -f rawvideo -pix_fmt bgra -s {W}x{H} -r 30 -i - -vf format=yuv420p -c:v libx264 -crf 18 -preset veryfast -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709 {os.path.join(HERE, "tmp_video.mp4")}'.split(), stdin=subprocess.PIPE)
        for f in range(NF): p.stdin.write(bytes(draw(f).get_data()))
        p.stdin.close(); assert p.wait() == 0; os.rename(os.path.join(HERE, 'tmp_video.mp4'), os.path.join(HERE, 'video.mp4')); print('video ok', NF)
