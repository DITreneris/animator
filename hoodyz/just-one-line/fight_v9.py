"""Just One Line: the fight, v9 (back to premises after v5-v8 stalled at intensity 5; "visi a").
Two big gags, in close, cut on the action; MY AI stands on the desk's edge at his eye height, so its arms and legs are
their normal length (no stretched limbs). Earlier: fight_v2..v8.py.
  S1 MS, close (0.0-1.6)   he charges the desk; MY AI hops, grabs his hood and yanks it down over his face; he gropes,
                           blind, and staggers back; it's typing again before it lands
  S2 CU (1.6-2.1)          FILES CHANGED 14 -> 24
  S3 WS (2.1-4.0)          blind, he backs into his chair and drops into it (the hood flips off); MY AI crouches on the
                           desk's edge... and DROPKICKS the chair, feet first, still looking at the screen; the chair
                           shoots him into the door (the door shakes); MY AI rebounds back onto the desk
  S4 WS (4.0-5.0)          dazed on the floor; FILES CHANGED 32, green; MY AI turns to us: a wink and a thumbs-up
Usage: python3 fight.py sheet | video"""
import os, sys, math, random, subprocess, cairo
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import kp as P
from kp import K, A, INK, WHITE, NAVY, SKIN, GREY, YEL, rr, fs, ell, limb, txt, hx, lerp, W, H, FLOOR, HS, AS, KEY, LAP, DESK_Y
cl = lambda t: max(0.0, min(1.0, t)); oe = lambda t: 1 - (1 - cl(t)) ** 3; io = lambda t: (lambda u: u * u * (3 - 2 * u))(cl(t))
K.FACES['dizzy'] = ('spiral', (None, None), 'wobble')
K.FACES['fury'] = ('open', ('angry', 'angry'), 'frown')
S2, S3, CROUCH, LEAP, CONTACT, WALL, S4, T_END = 48, 62, 76, 84, 96, 108, 122, 150
STOP = (CONTACT, 4)
NF = T_END + STOP[1]
AIX, CHX = 540, 230
ARM = 68 * AS                                                      # MY AI's arm segments, standard length
def story(f): return f if f < STOP[0] else (STOP[0] if f < STOP[0] + STOP[1] else f - STOP[1])
def noise(f, k): return random.Random(f * 7919 + k).uniform(-1, 1)

def counter(g):
    if g < 18: return 9
    if g < S2: return 14
    if g < S2 + 7: return 14
    if g < CONTACT: return 24
    if g < S4 + 4: return 31
    return 32

def robot_palm(c, x, y, ang, s):
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    for i in range(4): rr(c, 12, -24 + i * 13, 42 - abs(i - 1.5) * 6, 13, 6); fs(c, WHITE, 5)
    rr(c, -18, -26, 40, 52, 16); fs(c, WHITE, 6)
    c.restore()

def ai_arm(c, sh, tgt, end='fist'):
    e, h = P.ik(sh, tgt, ARM, ARM, P.DOWN)
    limb(c, [sh, e, h], 24 * AS, WHITE); ell(c, e[0], e[1], 13, 13); fs(c, GREY, 5)
    if end == 'fist': ell(c, h[0], h[1], 22, 22); fs(c, WHITE, 6)
    else: robot_palm(c, h[0], h[1], math.atan2(h[1] - e[1], h[0] - e[0]), AS * .9)
    return h

def myai_at(c, f, x, gy, left='down', eye='happy', look=(18, 0), rot=0.0, typing=True, turn=0.0):
    right = 'down'
    if typing:
        tap = 10 * math.sin(f * 2.3)
        right = P.ai_pose(1, P.ai_local(x, gy, AS, (KEY[0] + tap, KEY[1] - abs(tap))), P.DOWN)
    A.myai(c, x, gy, AS, eye=eye, look=look, rot=rot, turn=turn, arms=(left, right), bob=0)

def burst(c, x, y, r, n=8, col=YEL, w=10):
    for i in range(n):
        a = i * 2 * math.pi / n + .2; c.move_to(x + r * .4 * math.cos(a), y + r * .4 * math.sin(a)); c.line_to(x + r * math.cos(a), y + r * math.sin(a))
    c.set_source_rgb(*col); c.set_line_width(w); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()

def hood(c, head, k):
    """His hood: k 0 = down behind his neck (a navy lump), 1 = pulled over his face to the chin."""
    x, y = head; s = HS
    if k < .05:
        ell(c, x + 60 * s, y + 150 * s, 70 * s, 34 * s); fs(c, NAVY, 7); return
    c.save(); c.translate(x, y)
    top = lerp(60, -180, min(1, k * 1.4)) * s; bot = lerp(140, 80, k) * s
    c.move_to(-150 * s, bot); c.curve_to(-175 * s, top, 175 * s, top, 150 * s, bot); c.curve_to(60 * s, bot + 22 * s, -60 * s, bot + 22 * s, -150 * s, bot)
    c.close_path(); fs(c, NAVY, 8)
    c.move_to(-110 * s, bot - 30 * s); c.curve_to(-40 * s, bot - 8 * s, 40 * s, bot - 8 * s, 110 * s, bot - 30 * s); c.set_source_rgba(1, 1, 1, .25); c.set_line_width(6); c.stroke()
    if k > .7:
        for q in (-1, 1): limb(c, [(q * 40 * s, bot + 6 * s), (q * 48 * s, bot + 80 * s)], 7, WHITE)
    c.restore()

def camera(c, f, g):
    sh = 0
    for hit, amp in ((14 + 0, 10), (STOP[0], 20), (WALL + STOP[1], 16)):
        if hit <= f < hit + 8: sh = amp * (1 - (f - hit) / 8)
    if g < S2: k, ax, ay = 1.3, 440, 1227                                # S1: close; his hair clears the title bar, feet at ~1660
    else: k, ax, ay = 1.0 + .06 * io((f - CONTACT + 4) / 4) * (1 - io((f - CONTACT - 10) / 8)), 400, 1250
    c.translate(ax + noise(f, 1) * sh, ay + noise(f, 2) * sh); c.scale(k, k); c.translate(-ax, -ay)

def closeup(c, g):
    t = g - S2
    P.room(c)
    c.save(); c.translate(540, 1000); s = 3.2 + .1 * io(t / 14); c.scale(s, s); c.translate(-(LAP['x0'] + LAP['x1']) / 2, -(LAP['y0'] + LAP['y1']) / 2)
    P.laptop(c, counter(g)); c.restore()
    if S2 + 7 <= g < S2 + 12:
        for i in range(3): c.arc(540, 1080, 230 + i * 30, 0, 2 * math.pi); c.set_source_rgba(*YEL, .5 - .12 * i); c.set_line_width(8); c.stroke()

def frame(f):
    S = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(S)
    g = story(f)
    if S2 <= g < S3:
        closeup(c, g); P.topbar(c); return S
    c.save(); camera(c, f, g)
    ds = 10 * math.sin((g - WALL) * 2.2) * (1 - cl((g - WALL) / 10)) if g >= WALL else 0
    c.save(); c.translate(ds, 0); P.room(c); c.restore()
    P.desk(c); P.laptop(c, counter(g), tick=g >= S4 + 4)

    if g < S2:                                                             # S1: THE HOOD
        t = g
        P.chair(c, CHX - 40, P.SEAT_Y)
        hx_ = lerp(150, 330, oe(t / 8)) if t < 22 else lerp(330, 280, io((t - 22) / 20)) + 10 * math.sin(t * .7)
        blind = t >= 18
        shL, shR, head = P.hoody_standing(c, hx_, FLOOR, 'fury', bow=.12 if not blind else .05, gaze=18, side=1)
        k = io((t - 12) / 7)
        hood(c, head, k)
        if not blind:                                                     # charging: fists up
            P.hoody_arm(c, shL, (shL[0] + 40, shL[1] - 60), HS, pref=P.DOWN, hand='grip')
            P.hoody_arm(c, shR, (shR[0] + 90, shR[1] - 40), HS, pref=P.DOWN, hand='grip', ang=0)
        else:                                                             # groping, arms out wide, blind
            for q, sh in ((-1, shL), (1, shR)):
                P.hoody_arm(c, sh, (sh[0] + q * 130 + 30 * math.sin(t * .8 + q), sh[1] + 30 + 30 * math.cos(t * .9)), HS, pref=P.DOWN, hand='palm')
            for i in range(3):
                c.move_to(head[0] - 150 - i * 20, head[1] - 60 + i * 50); c.line_to(head[0] - 200 - i * 20, head[1] - 60 + i * 50)
            c.set_source_rgba(*INK, .35); c.set_line_width(5); c.stroke()
        hop = 150 * math.sin(math.pi * cl((t - 8) / 14))                  # MY AI hops up to reach his hood, then lands typing
        gy = DESK_Y - hop
        sh = (AIX - 72 * AS, gy - 280 * AS + 112 * AS)
        if 8 <= t < 22:
            grab = (head[0] + 70, lerp(head[1] + 140 * HS, head[1] - 150 * HS, k))
            myai_at(c, f, AIX, gy, left=None, typing=False)
            ai_arm(c, sh, grab, 'fist')
            if 12 <= t < 18: burst(c, head[0] + 40, head[1] - 120, 120, 10)
        else:
            myai_at(c, f, AIX, gy)

    elif g < S4:                                                           # S3: THE CHAIR AND THE DROPKICK
        t = g - S3
        c0, w0 = CONTACT - S3, WALL - S3
        if t < c0: chx, chr_, hop = CHX, 0, 0
        elif t < w0: u = cl((t - c0) / (w0 - c0)); chx, chr_, hop = lerp(CHX, 170, u * u), -.2 * u, 40 * math.sin(math.pi * u)
        else: u = oe((t - w0) / 12); chx, chr_, hop = lerp(170, 360, u), .15 * math.sin(math.pi * u), 0
        P.chair(c, chx, P.SEAT_Y - hop, rot=chr_, spin=max(0, t - c0) * .35)
        if t < 10:                                                        # blind, backing into the chair; he drops into it
            u = io(t / 10)
            if t < 6:
                shL, shR, head = P.hoody_standing(c, lerp(280, CHX + 20, u), FLOOR, 'fury', bow=.3 * u, gaze=0, side=-1)
                hood(c, head, 1)
                for q, sh in ((-1, shL), (1, shR)): P.hoody_arm(c, sh, (sh[0] + q * 130, sh[1] - 40), HS, pref=P.DOWN, hand='palm')
            else:
                sy = lerp(P.SEAT_Y - 140, P.SEAT_Y, io((t - 6) / 4)); sq = 1 + .12 * math.sin(math.pi * cl((t - 8) / 4))
                c.save(); c.translate(CHX, sy); c.scale(sq, 1 / sq); c.translate(-CHX, -sy)
                shL, shR, head = P.hoody_seated(c, CHX, sy, 'shock', rot=lerp(-.3, 0, io((t - 6) / 4)))
                c.restore()
                hood(c, head, 1 - io((t - 8) / 2))                       # flips off on the plop
        elif t < w0:                                                      # in the chair; then shot to the door
            tilt = 0 if t < c0 else -.14 * cl((t - c0) / 6)
            shL, shR, head = P.hoody_seated(c, min(chx, CHX), P.SEAT_Y - hop * 1.3, 'shock', rot=tilt)
            P.hoody_arm(c, shL, (shL[0] - 110, shL[1] - 80), HS, pref=P.LEFT, hand='palm')
            P.hoody_arm(c, shR, (shR[0] + 50, shR[1] - 180), HS, pref=P.RIGHT, hand='palm')
            if t >= c0: P.lines(c, [(chx + 330, P.SEAT_Y - 160), (chx + 170, P.SEAT_Y - 160)], 4)
        else:                                                             # into the door, out onto the floor
            u = io((t - w0) / 4)
            if t < w0 + 5: burst(c, 110, P.SEAT_Y - 230, 130, 10, WHITE, 12)
            c.save(); c.translate(lerp(175, 215, u), lerp(P.SEAT_Y, FLOOR - 10, u)); c.rotate(lerp(-.14, -.12, u))
            P.hoody_seated(c, 0, 0, 'shock' if u < 1 else 'dizzy', legs=((170, -10), (300, 0)))
            c.restore()
        # MY AI: typing; crouch (anticipation); the dropkick, feet first, eyes still on the screen; the rebound to the desk
        seat = (CHX + 95, P.SEAT_Y - 10)
        if t < CROUCH - S3: myai_at(c, f, AIX, DESK_Y)
        elif t < LEAP - S3:
            u = io((t - CROUCH + S3) / 6)
            c.save(); c.translate(AIX, DESK_Y); c.scale(1 + .12 * u, 1 - .18 * u); c.translate(-AIX, -DESK_Y)
            myai_at(c, f, AIX, DESK_Y, typing=False, left='down'); c.restore()
        elif t < c0:                                                      # in the air, feet first, toward the chair
            u = (t - (LEAP - S3)) / (c0 - (LEAP - S3))
            fx, fy = lerp(AIX - 40, seat[0], u), lerp(DESK_Y, seat[1], u) - math.sin(math.pi * u) * 120
            myai_at(c, f, fx, fy, typing=False, rot=lerp(.2, 1.35, io(u * 2)), left='up', look=(18, 0))
            P.lines(c, [(fx + 260, fy - 140), (fx + 120, fy - 60)], 3)
        elif t < c0 + 14:                                                 # contact, then the rebound up onto the desk
            u = io((t - c0) / 14)
            fx, fy = lerp(seat[0], AIX, u), lerp(seat[1], DESK_Y, u) - math.sin(math.pi * u) * 160
            myai_at(c, f, fx, fy, typing=False, rot=lerp(1.35, 0, u), left='up')
            if t < c0 + 5:
                ell(c, seat[0], seat[1], 70, 70); c.set_source_rgba(1, 1, 1, .85); c.fill(); burst(c, seat[0], seat[1], 140, 10, YEL, 12)
        else: myai_at(c, f, AIX, DESK_Y)

    else:                                                                  # S4: THE BUTTON
        t = g - S4
        P.chair(c, 360, P.SEAT_Y)
        c.save(); c.translate(215, FLOOR - 10); c.rotate(-.12)
        P.hoody_seated(c, 0, 0, 'shock' if 6 <= t < 14 else 'dizzy', legs=((170, -10), (300, 0)))
        c.restore()
        for i in range(3):
            a = f * .3 + i * 2.1; ell(c, 230 + 75 * math.cos(a), FLOOR - 540 + 18 * math.sin(a), 13, 13); c.set_source_rgb(*YEL); c.fill()
        btn = t >= 4
        thumb = (AIX - 150, DESK_Y - 330)
        pl = P.ai_pose(-1, P.ai_local(AIX, DESK_Y, AS, thumb), P.UP) if btn else 'down'
        myai_at(c, f, AIX, DESK_Y, left=pl, eye='wink' if btn else 'happy', look=(0, 0) if btn else (18, 0))
        if btn:
            tx, ty = A.hand_at(AIX, DESK_Y, AS, -1, pl); rr(c, tx - 17, ty - 86, 36, 70, 16); fs(c, WHITE, 8)
            if t < 14: burst(c, LAP['x1'] - 30, LAP['y0'] + 30, 70, 8, hx('5df08a'), 8)
    c.save(); c.translate(470, DESK_Y); P.mug(c, 0, 0, 1.1); c.restore()
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
        fs_ = list(range(0, NF, 4)); cols = 13; tw, th = 166, 295
        out = cairo.ImageSurface(cairo.FORMAT_RGB24, cols * tw, ((len(fs_) + cols - 1) // cols) * th); c = cairo.Context(out)
        c.set_source_rgb(1, 1, 1); c.paint()
        for i, f in enumerate(fs_):
            c.save(); c.translate((i % cols) * tw, (i // cols) * th); c.scale(tw / W, th / H); c.set_source_surface(frame(f)); c.paint(); c.restore()
            txt(c, f'{f / 30:.2f}', (i % cols) * tw + 34, (i // cols) * th + 16, 18, INK, lw=0)
        out.write_to_png('fight_sheet.png'); print('fight_sheet.png', NF / 30)
