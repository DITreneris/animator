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
B2, BONK, B3, B4, YANK, B5, PUSHF, B6, LEAP, CONTACT, WALL, BEND, T_END = 34, 50, 66, 94, 100, 122, 125, 138, 146, 156, 166, 184, 222
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
def held_before_story(st): return sum(h for at, h in HOLDS if at < st)      # fight frame = story + this
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
    LAST['ai'] = c.user_to_device(x, gy - 280 * AS)
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
    """Hockey move. k 0..1 is how far MY AI has pulled the front hem up: belly (0) -> chest, the white tee shows (.45)
    -> over his chin and face (from below) -> over the top of his head (1). The fabric over his head keeps the round
    shape of his head; the rest of the hoodie bunches at his shoulders; his arms are dragged up to his head.
    Returns (neck, hem point for MY AI's fist)."""
    s = HS; hip = (x, gy - 300 * s)
    for q in (-1, 1):
        limb(c, [(hip[0] + q * 30 * s, hip[1]), (x + q * 38 * s, gy - 20 * s)], 58 * s, P.JEANS)
        rr(c, x + q * 38 * s - 30 * s, gy - 26 * s, 70 * s, 30 * s, 14 * s); fs(c, INK, 0)
    c.save(); c.translate(*hip); c.rotate(sway); c.translate(-hip[0], -hip[1])
    neck = (x, hip[1] - 176 * s * 1.1 + 30 * s)
    rr(c, x - 92 * 1.1 * s, neck[1] - 33 * s, 184 * 1.1 * s, 209 * s, 60 * s); fs(c, WT)     # the tee
    expr = 'shock' if k < .5 else 'fury'
    K.hoodyz_head(c, x, neck[1] - 150 * s, s, era='young', expr=expr, blink=False)
    LAST["h"] = c.user_to_device(x, neck[1] - 150 * s)
    F = lerp(neck[1] + 176 * s, neck[1] - 300 * s, k)                    # the front hem, in MY AI's fist
    hc, rx, ry = (x, neck[1] - 165 * s), 122 * s, 138 * s               # his head, as the fabric sees it
    # the hoodie body: everything from the collar down to the hem (k<.45), or bunched at the collar (k>=.45)
    rr(c, x - 105 * s, neck[1] - 33 * s, 210 * s, max(F, neck[1] + 20 * s) - (neck[1] - 33 * s) + 20 * s, 50 * s); fs(c, NAVY)
    if F < neck[1] - 20 * s:                                             # over his face: the head's shape, from the hem down
        c.save(); c.rectangle(x - 200 * s, F, 400 * s, neck[1] - F); c.clip()
        c.save(); c.translate(*hc); c.scale(rx, ry); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); fs(c, NAVY)
        c.restore()
        hw = rx * math.sqrt(max(0, 1 - ((F - hc[1]) / ry) ** 2)) if abs(F - hc[1]) < ry else 0
        if hw > 10: rr(c, x - hw, F - 8 * s, 2 * hw, 26 * s, 12 * s); fs(c, hx('2b3a66'), 5)   # the ribbed hem, rolling up
    else:
        rr(c, x - 105 * s, F - 6 * s, 210 * s, 26 * s, 12 * s); fs(c, hx('2b3a66'), 5)
    for q in (-1, 1):                                                     # his arms, dragged up in the sleeves
        sh = (x + q * 92 * s, neck[1] + 5 * s)
        hd = (x + q * lerp(125, 112, k) * s, lerp(neck[1] + 250 * s, neck[1] - 230 * s, io(k)))
        e, h = P.ik(sh, hd, 118 * s, 112 * s, P.DOWN if k < .5 else (P.LEFT if q < 0 else P.RIGHT))
        limb(c, [sh, e, h], 44 * s, NAVY); K.hand(c, h[0] + 6 * math.sin(f * .9 + q) * k, h[1], s)
    c.restore()
    return neck, (x + 70 * s, F + 10 * s)

def chart_swing(c, g):
    """The wall chart after his fist hits it: it swings on its nail."""
    if not (BONK <= g < B4): return
    a = .3 * math.sin((g - BONK) * .8) * math.exp(-(g - BONK) / 14)
    c.rectangle(628, 668, 304, 224); c.set_source(P.wall_grad()); c.fill()
    c.save(); c.translate(780, 676); c.rotate(a); c.translate(-780, -676)
    rr(c, 640, 680, 280, 200, 10); fs(c, WHITE, 6)
    c.move_to(670, 850); c.line_to(740, 800); c.line_to(800, 820); c.line_to(890, 720); c.set_source_rgb(*P.GREEN); c.set_line_width(10); c.stroke()
    c.move_to(700, 760); c.line_to(660, 790); c.move_to(690, 800); c.line_to(650, 770); c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()  # a dent
    c.restore(); ell(c, 780, 674, 8, 8); fs(c, GREY, 4)

def camera(c, f, g):
    sh = 0
    for hit, amp in ((10, 10), (BONK, 22), (B3 + 6, 10), (YANK, 14), (PUSHF, 16), (CONTACT, 22), (WALL, 18)):
        hf = hit + held_before(f) if g >= hit else hit
        if g >= hit and 0 <= f - hf < 8: sh = amp * (1 - (f - hf) / 8)
    m = io((g - B2) / 6) * (1 - io((g - B6) / 8))                        # medium close for rounds 2-5
    k = lerp(1.0, 1.2, m); ax = 420; ay = lerp(1250, 1548, m)
    k += .07 * io((g - CONTACT + 4) / 4) * (1 - io((g - CONTACT - 10) / 8))
    c.translate(ax + noise(f, 1) * sh, ay + noise(f, 2) * sh); c.scale(k, k); c.translate(-ax, -ay)

LAST = {}                                                                  # where each one's head is on screen (for the film's bubbles)
_hs, _hst = P.hoody_seated, P.hoody_standing
def _rec_seated(c, *a, **k):
    r = _hs(c, *a, **k); LAST['h'] = c.user_to_device(*r[2]); return r
def _rec_standing(c, *a, **k):
    r = _hst(c, *a, **k); LAST['h'] = c.user_to_device(*r[2]); return r
P.hoody_seated, P.hoody_standing = _rec_seated, _rec_standing

def frame(f, cnt=None, tick=None, cam=None, extra=None, overlay=None, bar=True):
    """The fight at frame f. The film passes: cnt/tick (the counter), cam (its own camera), extra(c) (props on the desk,
    drawn behind the fighters), overlay(c, g) (drawn last, in the camera), bar=False (the film draws the title bar)."""
    S = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(S)
    g = story(f); LAST.clear()
    c.save(); (cam(c) if cam else camera(c, f, g))
    ds = 10 * math.sin((g - WALL) * 2.2) * (1 - cl((g - WALL) / 10)) if g >= WALL else 0
    c.save(); c.translate(ds, 0); P.room(c); c.restore()
    chart_swing(c, g)
    P.desk(c); P.laptop(c, counter(g) if cnt is None else cnt, tick=(g >= BEND + 4) if tick is None else tick)
    wob = .14 * math.sin(f * 1.7) * (1 if any(a <= g < a + 14 for a in (8, BONK, YANK, PUSHF, CONTACT)) else 0)
    c.save(); c.translate(690, DESK_Y); c.rotate(wob); P.mug(c, 0, 0, 1.0); c.restore()     # anchored on the desk, behind everyone
    if extra: extra(c)

    if g < B2:                                                             # 1 THE SHOVE
        t = g
        cx = 270 if t < 10 else lerp(270, CHX - 20, oe((t - 10) / 14))
        tilt = -.16 * cl((t - 9) / 3) * (1 - cl((t - 22) / 8))
        P.chair(c, cx, P.SEAT_Y, rot=tilt, spin=max(0, t - 10) * .3)
        shL, shR, head = P.hoody_seated(c, cx, P.SEAT_Y, 'smug' if t < 9 else 'shock', rot=tilt)
        if t < 9:                                                         # frame 0's pose: the hand that held the card out, the finger up
            P.hoody_arm(c, shR, (P.HAND_OFF[0] - 70, P.HAND_OFF[1] + 10), HS, pref=P.DOWN, hand='grip')
            P.hoody_arm(c, shL, (shL[0] - 95, shL[1] - 190), HS, pref=P.LEFT, hand='point', ang=-math.pi / 2 - .15)
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
            LAST['ai'] = c.user_to_device(x, gy - 280 * AS)
            A.myai(c, x, gy, AS, eye='happy', look=(18, 0), rot=(.12 if t < 5 else -.22) if t < 16 else -.06, arms=(None, None))
            push_arm(-1, -40)                                              # near arm in front
            if 8 <= t < 11:
                for h in palms: burst(c, h[0] - 20, h[1], 80, 8)
        else:
            u = io((t - 18) / 14); x = lerp(520, AIX, u); gy = lerp(FLOOR, DESK_Y, u) - math.sin(math.pi * u) * 200
            myai_at(c, f, x, gy)

    elif g < B3:                                                           # 2 THE WHIFF: he swings, it ducks, his fist hits the wall chart
        t = g - B2; tb = BONK - B2
        P.chair(c, CHX - 20, P.SEAT_Y)
        duck = io((t - 11) / 3) * (1 - io((t - 22) / 6))
        myai_at(c, f, AIX, DESK_Y, squash=1 - .42 * duck)                 # it ducks under the punch, still typing, still smiling
        if t < 6:                                                         # springing up out of the chair
            u = io(t / 6)
            shL, shR, head = P.hoody_seated(c, CHX - 20 + 20 * u, P.SEAT_Y - 130 * u, 'fury')
            P.hoody_arm(c, shL, (shL[0] - 60, shL[1] + 110), HS, pref=P.LEFT, hand='grip')
            P.hoody_arm(c, shR, (shR[0] + 60, shR[1] + 110), HS, pref=P.RIGHT, hand='grip')
        else:
            hx_ = lerp(200, 360, io((t - 6) / 8))
            expr = 'fury' if t < tb else ('ouch' if t < tb + 9 else 'fury')
            shL, shR, head = P.hoody_standing(c, hx_, FLOOR, expr, bow=.1 if t < tb + 2 else .03, gaze=18, side=1)
            CH = (668, 790)
            if t < 9: fist = (shR[0] + 50, shR[1] + 40)                  # fists up, charging in
            elif t < 13: u = io((t - 9) / 4); fist = (lerp(shR[0] + 50, shR[0] - 70, u), lerp(shR[1] + 40, shR[1] - 50, u))   # cocked back by his ear
            elif t < tb: u = ((t - 13) / (tb - 13)) ** 2; fist = (lerp(shR[0] - 70, CH[0], u), lerp(shR[1] - 50, CH[1], u))     # accelerating
            elif t < tb + 3: fist = CH                                    # contact: the chart, where its head just was
            else: fist = (shR[0] + 150 + 26 * math.sin(t * 2.6), shR[1] + 10 + 30 * math.cos(t * 2.6))                    # shaking the hurt hand, out to the side
            P.hoody_arm(c, shR, fist, HS, pref=P.DOWN, hand='grip' if t < tb + 3 else 'palm')
            if t < tb: P.hoody_arm(c, shL, (shL[0] + 70, shL[1] - 30), HS, pref=P.DOWN, hand='grip')                     # guard up
            else: P.hoody_arm(c, shL, (shR[0] + 40, shR[1] + 70), HS, pref=P.DOWN, hand='palm')                           # holding his arm
            if 13 <= t < tb: speed(c, fist[0] - 30, fist[1] + 10, fist[0] - 200, fist[1] + 60, 3)
            if tb <= t < tb + 3: burst(c, CH[0], CH[1], 70, 8)
            if t >= tb + 3:
                for i in range(3):
                    a_ = -1.2 + i * .6; c.move_to(fist[0] + 50 * math.cos(a_), fist[1] + 50 * math.sin(a_)); c.line_to(fist[0] + 80 * math.cos(a_), fist[1] + 80 * math.sin(a_))
                c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()

    elif g < B4:                                                           # 3 THE FOREHEAD: a palm holds him off; two shoves back
        t = g - B3
        P.chair(c, CHX - 20, P.SEAT_Y)
        p = max([1 - (t - q) / 5 for q in (8, 18) if 0 <= t - q < 5] + [0])
        hx_ = lerp(300, 250, oe(t / 6)) - 35 * p
        shL, shR, head = P.hoody_standing(c, hx_, FLOOR, 'fury' if p < .5 else 'ouch', bow=.36 - .25 * p + .04 * math.sin(t * 1.1), gaze=18, side=1)
        dust(c, hx_ - 70, f, 4)
        a_ = t * 1.1
        for q, sh, ph in ((-1, shL, 0), (1, shR, math.pi)):               # both fists windmilling, short of the robot
            tgt = (sh[0] + 40 + 55 * math.cos(a_ + ph), sh[1] - 10 + 75 * math.sin(a_ + ph))
            P.hoody_arm(c, sh, tgt, HS, pref=P.LEFT if q < 0 else P.DOWN, hand='grip')
        for i in range(2): c.arc(shR[0] + 40, shR[1] - 10, 90 + i * 22, -.6, 1.6); c.set_source_rgba(*INK, .35); c.set_line_width(5); c.stroke()
        myai_at(c, f, AIX, DESK_Y, left=None)
        fh = (head[0] + 85, head[1] - 10)
        sh = ai_shoulder(AIX, DESK_Y)
        u = oe(t / 4)
        ai_arm(c, sh, (lerp(sh[0] - 30, fh[0], u), lerp(sh[1] + 60, fh[1], u)), 'palm')
        if p > .6: burst(c, fh[0] - 10, fh[1], 60, 8)
        for dx, dy in ((60, -70), (100, -30)):
            ell(c, head[0] + dx, head[1] + dy + (t % 6) * 3, 8, 13); fs(c, hx('58c7ff'), 4)

    elif g < B5:                                                           # 4 THE JERSEY (hockey style)
        t = g - B4
        P.chair(c, CHX - 20, P.SEAT_Y)
        k = io((t - 2) / 10) * (1 - io((t - 22) / 6))
        blind = 12 <= t < 22
        hx_ = 310 - (22 * math.sin((t - 12) * .55) if blind else 0)
        sway = .14 * math.sin((t - 12) * .7) if blind else 0
        neck, hemp = hoody_jersey(c, hx_, FLOOR - (6 * abs(math.sin(t * .9)) if blind else 0), k, sway, f)
        if blind:
            dust(c, hx_ - 40, f, 2)
            for i in range(3): c.arc(hx_, neck[1] - 170 * HS, 190 + i * 24, 1.0 + .3 * i, 2.2 + .3 * i); c.set_source_rgba(*INK, .35); c.set_line_width(5); c.stroke()
        myai_at(c, f, AIX, DESK_Y, left=None)
        sh = ai_shoulder(AIX, DESK_Y)
        if t < 2: ai_arm(c, sh, (lerp(sh[0] - 30, hemp[0], io(t / 2)), lerp(sh[1] + 60, hemp[1], io(t / 2))), 'fist')
        elif t < 14: ai_arm(c, sh, hemp, 'fist', L=ARM * 1.55)            # the fist stays on the hem all the way up
        else: ai_arm(c, sh, (sh[0] - 50, sh[1] + 80), 'palm')

    elif g < B6:                                                           # 5 THE FOOT: a kick in the chest, back into his chair
        t = g - B5; tc = PUSHF - B5
        P.chair(c, CHX, P.SEAT_Y)
        hip = (AIX - 34 * AS, DESK_Y - 75 * AS)
        if t < 9:
            lean = -.32 * io((t - tc) / 2) * (1 - .3 * io((t - tc - 3) / 3)) if t >= tc else .05
            hx_ = 360 if t < tc else lerp(360, CHX + 30, io((t - tc) / 6))
            c.save(); c.translate(hx_, FLOOR); c.rotate(lean); c.translate(-hx_, -FLOOR)
            shL, shR, head = P.hoody_standing(c, hx_, FLOOR, 'fury' if t < tc else 'shock', bow=.12 if t < tc else 0, gaze=18 if t < tc else 0, side=1)
            chest = ((shL[0] + shR[0]) / 2 + 30, (shL[1] + shR[1]) / 2 + 70)
            if t < tc: tg = ((sh_[0] + 60, sh_[1] - 60) for sh_ in (shL, shR))
            elif t < tc + 3: tg = ((chest[0] - 10, chest[1] - 10), (chest[0] + 10, chest[1] + 10))    # hands to the hit
            else: tg = ((shL[0] + 140, shL[1] - 90), (shR[0] + 150, shR[1] - 40))                       # arms fly forward
            for sh_, tt in zip((shL, shR), tg): P.hoody_arm(c, sh_, tt, HS, pref=P.DOWN, hand='grip' if t < tc else 'palm')
            ca, sa = math.cos(lean), math.sin(lean)
            wc = (hx_ + (chest[0] - hx_) * ca - (chest[1] - FLOOR) * sa, FLOOR + (chest[0] - hx_) * sa + (chest[1] - FLOOR) * ca)
            c.restore()
            if t < tc: ft = (lerp(hip[0] + 20, wc[0], io(t / tc)), lerp(hip[1] + 60, wc[1], io(t / tc)))
            elif t < tc + 3: ft = wc
            else: ft = (lerp(wc[0], hip[0] - 10, io((t - tc - 3) / 3)), lerp(wc[1], hip[1] + 90, io((t - tc - 3) / 3)))
            if tc <= t < tc + 3: burst(c, wc[0], wc[1], 90, 8)
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

    elif g < BEND:                                                         # 6 THE DROPKICK
        t = g - B6
        c0, w0 = CONTACT - B6, WALL - B6
        if t < c0: chx, chr_, hop = CHX, 0, 0
        elif t < w0: u = cl((t - c0) / (w0 - c0)); chx, chr_, hop = lerp(CHX, 170, oe(u)), -.2 * u, 40 * math.sin(math.pi * u)
        else: u = oe((t - w0 - 2) / 12); chx, chr_, hop = lerp(170, 360, u), .25 * math.sin(math.pi * u), 0
        P.chair(c, chx, P.SEAT_Y - hop, rot=chr_, spin=max(0, t - c0) * .35)
        if t < w0:
            tilt = 0 if t < c0 else -.3 * oe((t - c0) / 3)
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
            myai_at(c, f, AIX, DESK_Y, typing=False, squash=1 - .38 * io((t - lt + 6) / 4))
        elif t < c0:                                                      # feet first, eyes still on the screen; a ghost trail
            u = (t - lt) / (c0 - lt)
            for gh in (2, 1):
                uu = max(0, u - gh * .12); gx, gy_ = lerp(AIX - 40, seat[0], uu), lerp(DESK_Y, seat[1], uu) - math.sin(math.pi * uu) * 120
                c.push_group(); myai_at(c, f, gx, gy_, typing=False, rot=lerp(.2, 1.35, io(uu * 2)), left='up'); c.pop_group_to_source(); c.paint_with_alpha(.18 * (3 - gh))
            fx, fy = lerp(AIX - 40, seat[0], u), lerp(DESK_Y, seat[1], u) - math.sin(math.pi * u) * 120
            myai_at(c, f, fx, fy, typing=False, rot=lerp(.2, 1.35, io(u * 2)), left='up')
            speed(c, fx + 260, fy - 140, fx + 120, fy - 60, 3)
        elif t < c0 + 10:
            u = io((t - c0) / 10)
            fx, fy = lerp(seat[0], AIX, u), lerp(seat[1], DESK_Y, u) - math.sin(math.pi * u) * 160
            myai_at(c, f, fx, fy, typing=False, rot=lerp(1.35, 0, io(u * 1.3)), left='up')        # one arc back up onto the desk
            if t < c0 + 3:
                ell(c, seat[0], seat[1], 75, 75); c.set_source_rgba(1, 1, 1, .85); c.fill(); burst(c, seat[0], seat[1], 150, 12, YEL, 12)
        else: myai_at(c, f, AIX, DESK_Y, squash=1 - .22 * math.sin(math.pi * cl((t - c0 - 10) / 5)))   # lands with a squash

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
    if overlay: overlay(c, g)
    c.restore()
    if bar: P.topbar(c)
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
