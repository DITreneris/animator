"""Just One Line: the fight, v10 - a real brawl (Tomas, 23 Nov: "detaliai kadrus kuo daugiau, kad butu intensyvi kova").
Six hits in about 7 s, every one with a visible contact, a hit-stop or a shake, and the counter jumping on it.
MY AI smiles the whole time and keeps typing with one hand. Earlier versions: fight_v2..v9.py.
  1 THE SHOVE    (0.0-1.1)  both palms on his chest; he and the chair roll; it hops onto the desk
  2 THE WHIFF    (1.1-2.2)  he springs up and swings; it ducks without looking; he lunges past and faceplants the wall chart
  3 THE FOREHEAD (2.2-3.1)  he comes back; a palm on his forehead holds him off; he windmills, short
  4 THE JERSEY   (3.1-4.1)  it grabs his hoodie's hem and yanks it up over his head (hockey style); he spins, blind
  5 THE FOOT     (4.1-4.6)  a foot in his chest: he topples back into his chair
  6 THE DROPKICK (4.6-6.1)  crouch, leap, feet first into the chair; the chair shoots him into the door; it rebounds
  END            (6.1-6.9)  dazed on the floor; FILES CHANGED 32, green; a wink and a thumbs-up
Usage: python3 fight.py sheet | video"""
import os, sys, math, random, subprocess, cairo
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import kp as P
from kp import K, A, INK, WHITE, NAVY, SKIN, GREY, YEL, rr, fs, ell, limb, txt, hx, lerp, W, H, FLOOR, HS, AS, KEY, LAP, DESK_Y
cl = lambda t: max(0.0, min(1.0, t)); oe = lambda t: 1 - (1 - cl(t)) ** 3; io = lambda t: (lambda u: u * u * (3 - 2 * u))(cl(t))
K.FACES['dizzy'] = ('spiral', (None, None), 'wobble')
K.FACES['fury'] = ('open', ('angry', 'angry'), 'frown')
K.FACES['ouch'] = ('shut', ('angry', 'angry'), 'o')
B2, BONK, B3, B4, YANK, B5, PUSHF, B6, LEAP, CONTACT, WALL, BEND, T_END = 34, 56, 66, 94, 100, 122, 125, 138, 146, 156, 166, 184, 222
HOLDS = [(BONK, 2), (PUSHF, 2), (CONTACT, 4)]
NF = T_END + sum(h for _, h in HOLDS)
AIX, CHX = 540, 230
ARM = 76 * AS                                                      # MY AI's arm segments (a touch longer than standard)
WT = hx('f2f4f8')                                                  # his white tee under the hoodie

def story(f):
    s = f
    for at, h in HOLDS:
        if s < at: return s
        if s < at + h: return at
        s -= h
    return s
def held_before(f):
    s = f; n = 0
    for at, h in HOLDS:
        if s < at: break
        if s < at + h: break
        s -= h; n += h
    return n
def noise(f, k): return random.Random(f * 7919 + k).uniform(-1, 1)

def counter(g):
    if g < B2: return int(lerp(0, 3, g / B2))
    if g < BONK: return 3
    if g < B3: return 7
    if g < B4: return 7 + int(5 * cl((g - B3 - 4) / 20))
    if g < YANK + 3: return 12
    if g < B5: return 19 if g < YANK + 12 else 21
    if g < PUSHF: return 21
    if g < CONTACT: return 24
    if g < BEND + 4: return 31
    return 32

def robot_palm(c, x, y, ang, s):
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    for i in range(4): rr(c, 12, -24 + i * 13, 42 - abs(i - 1.5) * 6, 13, 6); fs(c, WHITE, 5)
    rr(c, -18, -26, 40, 52, 16); fs(c, WHITE, 6)
    c.restore()

def ai_arm(c, sh, tgt, end='fist', L=ARM):
    e, h = P.ik(sh, tgt, L, L, P.DOWN)
    limb(c, [sh, e, h], 24 * AS, WHITE); ell(c, e[0], e[1], 13, 13); fs(c, GREY, 5)
    if end == 'fist': ell(c, h[0], h[1], 22, 22); fs(c, WHITE, 6)
    else: robot_palm(c, h[0], h[1], math.atan2(h[1] - e[1], h[0] - e[0]), AS * .9)
    return h

def myai_at(c, f, x, gy, left='down', eye='happy', look=(18, 0), rot=0.0, typing=True, squash=1.0, legs=True):
    right = 'down'
    if typing:
        tap = 10 * math.sin(f * 2.3)
        right = P.ai_pose(1, P.ai_local(x, gy, AS, (KEY[0] + tap, KEY[1] - abs(tap))), P.DOWN)
    old = A.limb
    if not legs: A.limb = lambda c_, pts, *a: None if pts == [(-34, 205), (-34, 280)] else old(c_, pts, *a)
    c.save(); c.translate(x, gy); c.scale(1 / math.sqrt(squash), squash); c.translate(-x, -gy)
    try: A.myai(c, x, gy, AS, eye=eye, look=look, rot=rot, arms=(left, right), bob=0)
    finally: A.limb = old; c.restore()

def ai_shoulder(x, gy, q=-1, squash=1.0): return (x + q * 72 * AS / math.sqrt(squash), gy - (280 - 112) * AS * squash)

def burst(c, x, y, r, n=8, col=YEL, w=10):
    for i in range(n):
        a = i * 2 * math.pi / n + .2; c.move_to(x + r * .4 * math.cos(a), y + r * .4 * math.sin(a)); c.line_to(x + r * math.cos(a), y + r * math.sin(a))
    c.set_source_rgb(*col); c.set_line_width(w); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()

def speed(c, x0, y0, x1, y1, n=3, a=.45):
    P.lines(c, [(x0, y0), (x1, y1)], n, INK, a)

def dust(c, x, f, n=3):
    for i in range(n):
        ell(c, x - i * 28 + 6 * math.sin(f + i), FLOOR - 14 - i * 7, 16 - i * 3, 9 - i * 2); c.set_source_rgba(.6, .55, .5, .75); c.fill()

def hoody_jersey(c, x, gy, k, sway=0.0, f=0):
    """Hockey move, step by step. k 0..1 is how far the front hem has been pulled up: from his belly (0),
    past his chest (the white tee shows), over his chin and face (from below, so we see it cover him),
    to above his head (1). His arms are dragged up inside the sleeves. Returns (neck, front hem point)."""
    s = HS; hip = (x, gy - 300 * s)
    for q in (-1, 1):
        limb(c, [(hip[0] + q * 30 * s, hip[1]), (x + q * 38 * s, gy - 20 * s)], 58 * s, P.JEANS)
        rr(c, x + q * 38 * s - 30 * s, gy - 26 * s, 70 * s, 30 * s, 14 * s); fs(c, INK, 0)
    c.save(); c.translate(*hip); c.rotate(sway); c.translate(-hip[0], -hip[1])
    neck = (x, hip[1] - 176 * s * 1.1 + 30 * s)
    rr(c, x - 92 * 1.1 * s, neck[1] - 33 * s, 184 * 1.1 * s, 209 * s, 60 * s); fs(c, WT)     # the tee
    K.hoodyz_head(c, x, neck[1] - 150 * s, s, era='young', expr='shock', blink=False)        # always drawn: the fabric covers it
    F = lerp(neck[1] + 176 * s, neck[1] - 300 * s, k)                     # the front hem, in MY AI's fist
    top, bot = min(F, neck[1] - 33 * s), max(F + 40 * s, neck[1] + 10 * s + (166 * s) * (1 - cl(k / .45)))
    for q in (-1, 1):                                                     # sleeves: hanging at k=0, dragged up at k=1
        sh = (x + q * 90 * s, neck[1] + 10 * s)
        hd = (x + q * lerp(120, 70, k) * s, lerp(neck[1] + 250 * s, neck[1] - 320 * s, io(k)))
        el = (x + q * lerp(150, 140, k) * s, (sh[1] + hd[1]) / 2)
        limb(c, [sh, el, hd], 48 * s, NAVY)
        K.hand(c, hd[0] + 8 * math.sin(f * .9 + q) * k, hd[1] + (-20 if k > .5 else 20) * s, s)
    rr(c, x - 105 * s, top, 210 * s, bot - top, 60 * s); fs(c, NAVY)     # the hoodie: torso at k=0, a bag over his head at k=1
    for i in range(3):                                                    # bunched folds
        y = lerp(top, bot, .3 + .2 * i)
        c.move_to(x - 80 * s, y); c.curve_to(x - 20 * s, y + 18 * s, x + 20 * s, y + 18 * s, x + 80 * s, y)
        c.set_source_rgba(1, 1, 1, .22 if k > .1 else 0); c.set_line_width(6); c.stroke()
    c.restore()
    return neck, (x + 60 * s, F)

def camera(c, f, g):
    sh = 0
    for hit, amp in ((10, 10), (BONK, 22), (B3 + 6, 10), (YANK, 14), (PUSHF, 16), (CONTACT, 22), (WALL, 18)):
        hf = hit + held_before(f) if g >= hit else hit
        if g >= hit and 0 <= f - hf < 8: sh = amp * (1 - (f - hf) / 8)
    m = io((g - B2) / 6) * (1 - io((g - B6) / 8))                        # medium close for rounds 2-5
    k = lerp(1.0, 1.2, m); ax = 420; ay = lerp(1250, 1548, m)
    k += .07 * io((g - CONTACT + 4) / 4) * (1 - io((g - CONTACT - 10) / 8))
    c.translate(ax + noise(f, 1) * sh, ay + noise(f, 2) * sh); c.scale(k, k); c.translate(-ax, -ay)

def frame(f):
    S = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(S)
    g = story(f)
    c.save(); camera(c, f, g)
    ds = 10 * math.sin((g - WALL) * 2.2) * (1 - cl((g - WALL) / 10)) if g >= WALL else 0
    c.save(); c.translate(ds, 0); P.room(c); c.restore()
    P.desk(c); P.laptop(c, counter(g), tick=g >= BEND + 4)
    wob = .14 * math.sin(f * 1.7) * (1 if any(a <= g < a + 14 for a in (8, BONK, YANK, PUSHF, CONTACT)) else 0)
    c.save(); c.translate(690, DESK_Y); c.rotate(wob); P.mug(c, 0, 0, 1.0); c.restore()     # anchored on the desk, behind everyone

    if g < B2:                                                             # 1 THE SHOVE
        t = g
        cx = 270 if t < 10 else lerp(270, CHX - 20, oe((t - 10) / 14))
        tilt = -.16 * cl((t - 9) / 3) * (1 - cl((t - 22) / 8))
        P.chair(c, cx, P.SEAT_Y, rot=tilt, spin=max(0, t - 10) * .3)
        shL, shR, head = P.hoody_seated(c, cx, P.SEAT_Y, 'smug' if t < 9 else 'shock', rot=tilt)
        if t < 9:
            P.hoody_arm(c, shL, (shL[0] - 60, shL[1] + 120), HS, pref=P.LEFT, hand='palm')
            P.hoody_arm(c, shR, (shR[0] + 40, shR[1] - 190), HS, pref=P.RIGHT, hand='palm')
        else:                                                             # pushed back: both arms fly forward
            fl = 20 * math.sin(t * 1.3)
            P.hoody_arm(c, shL, (shL[0] + 120, shL[1] - 60 + fl), HS, pref=P.UP, hand='palm')
            P.hoody_arm(c, shR, (shR[0] + 150, shR[1] - 20 - fl), HS, pref=P.UP, hand='palm')
        if 10 <= t < 24: speed(c, cx + 300, P.SEAT_Y - 170, cx + 150, P.SEAT_Y - 170)
        if t < 18:
            x = lerp(P.STAND_X, 520, oe(t / 8)); gy = FLOOR
            chest = ((shL[0] + shR[0]) / 2 + 60, (shL[1] + shR[1]) / 2 + 80)
            palms = []
            def push_arm(q, dy):
                sh = (x + q * 72 * AS, gy - 280 * AS + 112 * AS)
                if t < 5: tgt = (sh[0] + 50 + 30 * io(t / 5), sh[1] + 60)                     # wind-up: palms drawn back
                elif t < 8: tgt = (lerp(sh[0] + 80, chest[0], io((t - 5) / 3)), lerp(sh[1] + 60, chest[1] + dy, io((t - 5) / 3)))
                else: tgt = (chest[0] + (0 if t < 14 else -60), chest[1] + dy)
                e, h = P.ik(sh, tgt, 130, 130, P.DOWN); limb(c, [sh, e, h], 24 * AS, WHITE); ell(c, *e, 13, 13); fs(c, GREY, 5)
                robot_palm(c, h[0], h[1], math.atan2(h[1] - e[1], h[0] - e[0]), AS * .9); palms.append(h)
            push_arm(1, 40)                                                # far arm behind the body
            A.myai(c, x, gy, AS, eye='happy', look=(18, 0), rot=(.12 if t < 5 else -.22) if t < 16 else -.06, arms=(None, None))
            push_arm(-1, -40)                                              # near arm in front
            if 8 <= t < 14:
                for h in palms: burst(c, h[0] - 20, h[1], 80, 8)
        else:
            u = io((t - 18) / 14); x = lerp(520, AIX, u); gy = lerp(FLOOR, DESK_Y, u) - math.sin(math.pi * u) * 200
            myai_at(c, f, x, gy)

    elif g < B3:                                                           # 2 THE WHIFF: swing, duck, faceplant
        t = g - B2
        P.chair(c, CHX - 20, P.SEAT_Y)
        duck = io((t - 12) / 3) * (1 - io((t - 24) / 6))
        sq = 1 - .38 * duck
        myai_at(c, f, AIX, DESK_Y, squash=sq, eye='happy')                # it ducks, still typing, still smiling
        if t < 6:                                                         # springing up out of the chair
            u = io(t / 6)
            shL, shR, head = P.hoody_seated(c, CHX - 20 + 20 * u, P.SEAT_Y - 130 * u, 'fury')
            P.hoody_arm(c, shL, (shL[0] - 60, shL[1] + 110), HS, pref=P.LEFT, hand='grip')
            P.hoody_arm(c, shR, (shR[0] + 60, shR[1] + 110), HS, pref=P.RIGHT, hand='grip')
        elif t < 22:                                                      # charge, wind-up, PUNCH... at nothing; the lunge carries on
            u = io((t - 6) / 16)
            hx_ = lerp(200, 430, u); bow = lerp(.15, .85, io((t - 12) / 8))
            shL, shR, head = P.hoody_standing(c, hx_, FLOOR, 'fury' if t < 20 else 'shock', bow=bow, gaze=18, side=1)
            wind = io((t - 8) / 4) * (1 - io((t - 12) / 2))
            fist = (shR[0] + lerp(60, 240, io((t - 12) / 3)) - 120 * wind, shR[1] - 30 - 60 * wind)
            P.hoody_arm(c, shR, fist, HS, pref=P.UP, hand='grip', ang=0)
            P.hoody_arm(c, shL, (shL[0] - 130, shL[1] - 20), HS, pref=P.LEFT, hand='palm')
            if 12 <= t < 18: speed(c, fist[0] - 40, fist[1], fist[0] - 220, fist[1], 3)
            speed(c, hx_ - 120, FLOOR - 200, hx_ - 260, FLOOR - 200, 3, .3)
            if t == 21: burst(c, head[0] + 80, head[1] - 20, 140, 10)
        else:                                                             # the faceplant, then reeling back, dazed
            u = io((t - 22) / 10)
            hx_ = lerp(430, 300, u); bow = lerp(.85, .05, u)
            shL, shR, head = P.hoody_standing(c, hx_, FLOOR, 'ouch' if t < 26 else 'dizzy', bow=bow, gaze=0, side=1)
            if t < 28: P.hoody_arm(c, shR, (head[0] + 60, head[1] + 40), HS, pref=P.DOWN, hand='palm')       # a hand to his face
            else: P.hoody_arm(c, shR, (shR[0] + 130, shR[1] + 30 - 20 * math.sin(t)), HS, pref=P.DOWN, hand='palm')
            P.hoody_arm(c, shL, (shL[0] - 120, shL[1] + 40 + 20 * math.sin(t)), HS, pref=P.LEFT, hand='palm')
            if t < 25: burst(c, 640, 790, 150, 12, YEL, 12)
            for i in range(3):
                a = f * .5 + i * 2.1; ell(c, head[0] + 70 * math.cos(a), head[1] - 190 + 14 * math.sin(a), 11, 11); c.set_source_rgb(*YEL); c.fill()

    elif g < B4:                                                           # 3 THE FOREHEAD
        t = g - B3
        P.chair(c, CHX - 20, P.SEAT_Y)
        hx_ = lerp(300, 330, oe(t / 6)) + 8 * math.sin(t * .8)
        shL, shR, head = P.hoody_standing(c, hx_, FLOOR, 'fury', bow=.42 + .06 * math.sin(t * 1.1), gaze=18, side=1)
        dust(c, hx_ - 70, f, 4)
        a_ = t * 1.1
        for q, sh, ph in ((-1, shL, 0), (1, shR, math.pi)):               # both fists windmilling at the air
            tgt = (sh[0] + 45 + 60 * math.cos(a_ + ph), sh[1] - 20 + 80 * math.sin(a_ + ph))
            P.hoody_arm(c, sh, tgt, HS, pref=P.LEFT if q < 0 else P.DOWN, hand='grip')
        for i in range(2): c.arc(shR[0] + 45, shR[1] - 20, 95 + i * 22, -.6, 1.6); c.set_source_rgba(*INK, .35); c.set_line_width(5); c.stroke()
        myai_at(c, f, AIX, DESK_Y, left=None)
        fh = (head[0] + 95, head[1] - 60)
        sh = ai_shoulder(AIX, DESK_Y)
        ai_arm(c, sh, (lerp(sh[0] - 40, fh[0], oe((t - 2) / 4)), lerp(sh[1] + 60, fh[1], oe((t - 2) / 4))), 'palm')
        if 4 <= t < 9: burst(c, fh[0], fh[1], 70, 8)
        for dx, dy in ((60, -70), (100, -30)):
            ell(c, head[0] + dx, head[1] + dy + (t % 6) * 3, 8, 13); fs(c, hx('58c7ff'), 4)

    elif g < B5:                                                           # 4 THE JERSEY (hockey style)
        t = g - B4
        P.chair(c, CHX - 20, P.SEAT_Y)
        k = io((t - 2) / 10)
        hx_ = 330 - 20 * io((t - 12) / 6) + (25 * math.sin((t - 12) * .55) if t > 12 else 0)
        sway = (.16 * math.sin((t - 12) * .7)) if t > 12 else 0
        neck, hemp = hoody_jersey(c, hx_, FLOOR - (6 * abs(math.sin(t * .9)) if t > 12 else 0), k, sway, f)
        if t > 12: dust(c, hx_ - 40, f, 2)
        myai_at(c, f, AIX, DESK_Y, left=None)
        sh = ai_shoulder(AIX, DESK_Y)
        if t < 14:
            ai_arm(c, sh, hemp, 'fist', L=ARM * 1.4)                      # the fist stays on the hem all the way up
        else: ai_arm(c, sh, (sh[0] - 50, sh[1] + 80), 'palm')
        
        if t > 12:
            for i in range(3): c.arc(hx_, neck[1] - 250 * HS, 200 + i * 24, 1.0 + .3 * i, 2.2 + .3 * i); c.set_source_rgba(*INK, .35); c.set_line_width(5); c.stroke()

    elif g < B6:                                                           # 5 THE FOOT: a kick in the chest, back into his chair
        t = g - B5
        P.chair(c, CHX, P.SEAT_Y)
        hip = (AIX - 34 * AS, DESK_Y - 75 * AS)
        if t < 3:
            neck, _ = hoody_jersey(c, 300, FLOOR, 1.0 - .4 * io(t / 3), 0, f)
            ft = (lerp(hip[0] + 20, 360, io(t / 3)), lerp(hip[1] + 60, 1070, io(t / 3)))
        elif t < 9:
            u = io((t - 3) / 6)
            shL, shR, head = P.hoody_standing(c, lerp(300, CHX + 20, u), FLOOR, 'shock', bow=.5 * u, gaze=0, side=-1)
            for q, sh in ((-1, shL), (1, shR)): P.hoody_arm(c, sh, (sh[0] + q * 130, sh[1] - 80), HS, pref=P.DOWN, hand='palm')
            ft = (lerp(360, hip[0] - 10, u), lerp(1070, hip[1] + 90, u))
        else:
            u = io((t - 9) / 5); sy = lerp(P.SEAT_Y - 140, P.SEAT_Y, u); sq = 1 + .12 * math.sin(math.pi * cl((t - 12) / 4))
            c.save(); c.translate(CHX, sy); c.scale(sq, 1 / sq); c.translate(-CHX, -sy)
            shL, shR, head = P.hoody_seated(c, CHX, sy, 'shock', rot=lerp(-.3, 0, u))
            c.restore()
            P.hoody_arm(c, shL, (shL[0] - 110, shL[1] - 80), HS, pref=P.LEFT, hand='palm')
            P.hoody_arm(c, shR, (shR[0] + 50, shR[1] - 180), HS, pref=P.RIGHT, hand='palm')
            ft = (hip[0] - 10, hip[1] + 90)
        myai_at(c, f, AIX, DESK_Y, legs=False)
        e, h = P.ik(hip, ft, 70 * AS, 70 * AS, P.UP); limb(c, [hip, e, h], 34 * AS, WHITE); ell(c, *e, 14, 14); fs(c, GREY, 5)
        c.save(); c.translate(*h); c.rotate(math.atan2(h[1] - e[1], h[0] - e[0])); rr(c, -26, -28, 74, 56, 22); fs(c, WHITE, 7); c.restore()
        if PUSHF - B5 <= t < PUSHF - B5 + 4: burst(c, 360, 1070, 120, 10)

    elif g < BEND:                                                         # 6 THE DROPKICK
        t = g - B6
        c0, w0 = CONTACT - B6, WALL - B6
        if t < c0: chx, chr_, hop = CHX, 0, 0
        elif t < w0: u = cl((t - c0) / (w0 - c0)); chx, chr_, hop = lerp(CHX, 170, u * u), -.2 * u, 40 * math.sin(math.pi * u)
        else: u = oe((t - w0 - 2) / 12); chx, chr_, hop = lerp(170, 360, u), .25 * math.sin(math.pi * u), 0
        P.chair(c, chx, P.SEAT_Y - hop, rot=chr_, spin=max(0, t - c0) * .35)
        if t < w0:
            tilt = 0 if t < c0 else -.14 * cl((t - c0) / 6)
            shL, shR, head = P.hoody_seated(c, min(chx, CHX), P.SEAT_Y - hop * 1.3, 'shock', rot=tilt)
            P.hoody_arm(c, shL, (shL[0] - 110, shL[1] - 80), HS, pref=P.LEFT, hand='palm')
            P.hoody_arm(c, shR, (shR[0] + 50, shR[1] - 180), HS, pref=P.RIGHT, hand='palm')
            if t >= c0: speed(c, chx + 330, P.SEAT_Y - 160, chx + 170, P.SEAT_Y - 160, 4)
        else:
            u = cl((t - w0) / 10)
            if t < w0 + 5: burst(c, 110, P.SEAT_Y - 230, 140, 12, WHITE, 12)
            px = lerp(170, 215, oe(u)); py = lerp(P.SEAT_Y, FLOOR - 10, u * u) - 70 * math.sin(math.pi * min(1, u * 1.4))
            c.save(); c.translate(px, py); c.rotate(-.45 * (1 - u) + .08 * math.sin(math.pi * u))
            if u < 1: P.hoody_seated(c, 0, 0, 'shock', legs=((150, -90 * (1 - u) - 10), (280, -60 * (1 - u))))
            else: P.hoody_seated(c, 0, 0, 'dizzy', legs=((170, -10), (300, 0)))
            c.restore()
            if w0 + 9 <= t < w0 + 15: dust(c, 260, f, 4)
        seat = (CHX + 95, P.SEAT_Y - 10)
        lt = LEAP - B6
        if t < lt - 6: myai_at(c, f, AIX, DESK_Y)
        elif t < lt:                                                      # crouch: anticipation
            myai_at(c, f, AIX, DESK_Y, typing=False, squash=1 - .25 * io((t - lt + 6) / 4))
        elif t < c0:                                                      # feet first, eyes still on the screen; a ghost trail
            u = (t - lt) / (c0 - lt)
            for gh in (2, 1):
                uu = max(0, u - gh * .12); gx, gy_ = lerp(AIX - 40, seat[0], uu), lerp(DESK_Y, seat[1], uu) - math.sin(math.pi * uu) * 120
                c.push_group(); myai_at(c, f, gx, gy_, typing=False, rot=lerp(.2, 1.35, io(uu * 2)), left='up'); c.pop_group_to_source(); c.paint_with_alpha(.18 * (3 - gh))
            fx, fy = lerp(AIX - 40, seat[0], u), lerp(DESK_Y, seat[1], u) - math.sin(math.pi * u) * 120
            myai_at(c, f, fx, fy, typing=False, rot=lerp(.2, 1.35, io(u * 2)), left='up')
            speed(c, fx + 260, fy - 140, fx + 120, fy - 60, 3)
        elif t < c0 + 14:
            u = io((t - c0) / 14)
            fx, fy = lerp(seat[0], AIX, u), lerp(seat[1], DESK_Y, u) - math.sin(math.pi * u) * 260
            myai_at(c, f, fx, fy, typing=False, rot=lerp(1.35, 0, io(u * 1.3)), left='up')        # one arc back up onto the desk
            if t < c0 + 5:
                ell(c, seat[0], seat[1], 75, 75); c.set_source_rgba(1, 1, 1, .85); c.fill(); burst(c, seat[0], seat[1], 150, 12, YEL, 12)
        else: myai_at(c, f, AIX, DESK_Y, squash=1 - .22 * math.sin(math.pi * cl((t - c0 - 14) / 5)))   # lands with a squash

    else:                                                                  # END: the button
        t = g - BEND
        P.chair(c, 360, P.SEAT_Y)
        c.save(); c.translate(215, FLOOR - 10)
        P.hoody_seated(c, 0, 0, 'shock' if 6 <= t < 14 else 'dizzy', legs=((170, -10), (300, 0)))
        c.restore()
        for i in range(3):
            a = f * .3 + i * 2.1; ell(c, 230 + 75 * math.cos(a), FLOOR - 540 + 18 * math.sin(a), 14, 14); c.set_source_rgb(*YEL); c.fill()
        btn = t >= 4
        thumb = (AIX - 160, DESK_Y - 340)
        pl = P.ai_pose(-1, P.ai_local(AIX, DESK_Y, AS, thumb), P.UP) if btn else 'down'
        myai_at(c, f, AIX, DESK_Y, left=pl, eye='wink' if btn else 'happy', look=(0, 0) if btn else (18, 0))
        if btn:
            tx, ty = A.hand_at(AIX, DESK_Y, AS, -1, pl); rr(c, tx - 20, ty - 100, 42, 84, 18); fs(c, WHITE, 8)
            if t < 14: burst(c, LAP['x1'] - 30, LAP['y0'] + 30, 80, 8, hx('5df08a'), 9)
    c.restore()
    P.topbar(c)
    return S

if __name__ == '__main__':
    os.chdir(HERE); mode = (sys.argv[1:] or ['sheet'])[0]
    if mode == 'video':
        p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}', '-r', '30', '-i', '-',
                              '-c:v', 'libx264', '-crf', '20', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', 'fight_test.mp4'], stdin=subprocess.PIPE)
        for f in range(NF): p.stdin.write(bytes(frame(f).get_data()))
        p.stdin.close(); p.wait(); print('fight_test.mp4')
    else:
        step = int(sys.argv[2]) if len(sys.argv) > 2 else 3
        fs_ = list(range(0, NF, step)); cols = 12; tw, th = 180, 320
        out = cairo.ImageSurface(cairo.FORMAT_RGB24, cols * tw, ((len(fs_) + cols - 1) // cols) * th); c = cairo.Context(out)
        c.set_source_rgb(1, 1, 1); c.paint()
        for i, f in enumerate(fs_):
            c.save(); c.translate((i % cols) * tw, (i // cols) * th); c.scale(tw / W, th / H); c.set_source_surface(frame(f)); c.paint(); c.restore()
            txt(c, f'{f}', (i % cols) * tw + 26, (i // cols) * th + 16, 18, INK, lw=0)
        out.write_to_png('fight_sheet.png'); print('fight_sheet.png', NF / 30)
