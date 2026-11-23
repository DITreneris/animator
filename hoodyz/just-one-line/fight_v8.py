"""Just One Line: the fight, motion test v8 (tests 12-14: follow 7, intensity stuck at 5 -> the struggle is three different
attempts, each swatted a different way, with the camera in close; the hood gag; a real fall into the chair; the chair hits
the door; a button). Earlier: fight_v2..v7.py.
  1 THE SHOVE      both palms on his chest; he and the chair roll left; it hops onto the desk
  2 THE SCREEN     close-up: FILES CHANGED 2 -> 3
  3 ATTEMPT 1      he lunges for the keys: SLAP, his hand bounces off; he shakes it
    ATTEMPT 2      he climbs at the desk: a palm on his forehead holds him off, he runs in place
    ATTEMPT 3      he comes again: it pulls his hood down over his face; he gropes, blind
  4 THE FALL       the palm shoves him back; he drops into his chair (in-betweens: falling, hips in the air)
  5 THE KICK       wind-up (held), impact, the chair shoots him into the door: the door shakes, he spills out
  6 THE BUTTON     FILES CHANGED 32, green; MY AI turns to us for the first time: a wink and a thumbs-up
Usage: python3 fight.py sheet | video"""
import os, sys, math, random, subprocess, cairo
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import kp as P
from kp import K, A, INK, WHITE, NAVY, SKIN, GREY, YEL, rr, fs, ell, limb, txt, hx, lerp, W, H, FLOOR, HS, AS, KEY, LAP, DESK_Y
cl = lambda t: max(0.0, min(1.0, t)); oe = lambda t: 1 - (1 - cl(t)) ** 3; io = lambda t: (lambda u: u * u * (3 - 2 * u))(cl(t))
K.FACES['dizzy'] = ('spiral', (None, None), 'wobble')
K.FACES['fury'] = ('open', ('angry', 'angry'), 'frown')
K.FACES['ouch'] = ('shut', ('angry', 'angry'), 'o')
T_CU, T_ST = 40, 54
A2, A3 = T_ST + 22, T_ST + 44
T_FALL = T_ST + 66
T_KICK = T_FALL + 14
CONTACT = T_KICK + 12
WALL = CONTACT + 9
T_BTN = WALL + 18
T_END = T_BTN + 24
STOP = (CONTACT, 4)
NF = T_END + STOP[1]
AIX, CHX = 610, 230
SH_L = (AIX - 72 * AS, DESK_Y - 280 * AS + 112 * AS)
def story(f): return f if f < STOP[0] else (STOP[0] if f < STOP[0] + STOP[1] else f - STOP[1])
def noise(f, k): return random.Random(f * 7919 + k).uniform(-1, 1)

def counter(g):
    if g < T_CU: return int(lerp(0, 2, g / T_CU))
    if g < T_ST: return 2 if g < T_CU + 7 else 3
    if g < A2: return 3 if g < T_ST + 12 else 8                         # each swat pays the counter
    if g < A3: return 8 if g < A2 + 10 else 14
    if g < T_FALL: return 14 if g < A3 + 12 else 21
    if g < CONTACT: return 24
    if g < T_BTN: return 31
    return 32

def robot_palm(c, x, y, ang, s):
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    for i in range(4): rr(c, 12, -24 + i * 13, 42 - abs(i - 1.5) * 6, 13, 6); fs(c, WHITE, 5)
    rr(c, -18, -26, 40, 52, 16); fs(c, WHITE, 6)
    c.restore()

def ai_limb(c, sh, tgt, w, L, end='palm', pref=P.DOWN):
    e, h = P.ik(sh, tgt, L, L, pref)
    limb(c, [sh, e, h], w, WHITE)
    ell(c, e[0], e[1], 14, 14); fs(c, GREY, 5)
    a = math.atan2(h[1] - e[1], h[0] - e[0])
    if end == 'palm': robot_palm(c, h[0], h[1], a, AS * .9)
    elif end == 'foot': c.save(); c.translate(*h); c.rotate(a); rr(c, -26, -28, 74, 56, 22); fs(c, WHITE, 7); c.restore()
    elif end == 'fist': ell(c, h[0], h[1], 22, 22); fs(c, WHITE, 6)
    return h

def myai_typing(c, f, x, gy, left='down', legs=True, eye='happy', look=(18, 0), turn=0.0):
    tap = 10 * math.sin(f * 2.3)
    right = P.ai_pose(1, P.ai_local(x, gy, AS, (KEY[0] + tap, KEY[1] - abs(tap))), P.DOWN)
    old = A.limb
    if not legs: A.limb = lambda c_, pts, *a: None if pts == [(-34, 205), (-34, 280)] else old(c_, pts, *a)
    try: A.myai(c, x, gy, AS, eye=eye, look=look, turn=turn, arms=(left, right), bob=3 * math.sin(f * .6))
    finally: A.limb = old

def burst(c, x, y, r, n=8, col=YEL, w=10):
    for i in range(n):
        a = i * 2 * math.pi / n + .2; c.move_to(x + r * .4 * math.cos(a), y + r * .4 * math.sin(a)); c.line_to(x + r * math.cos(a), y + r * math.sin(a))
    c.set_source_rgb(*col); c.set_line_width(w); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()

def dust(c, x, f, n=3):
    for i in range(n):
        ell(c, x - i * 28 + 6 * math.sin(f + i), FLOOR - 14 - i * 7, 16 - i * 3, 9 - i * 2); c.set_source_rgba(.6, .55, .5, .75); c.fill()

def hood_over(c, head, k):
    """His own hood, pulled down over his face: k 0..1 how far (0 = down on his back, 1 = over his eyes and nose)."""
    if k <= .02: return
    x, y = head; s = HS
    c.save(); c.translate(x, y)
    top = -175 * s; bot = lerp(-120 * s, 70 * s, k)
    c.move_to(-150 * s, bot); c.curve_to(-170 * s, top, 170 * s, top, 150 * s, bot); c.curve_to(60 * s, bot + 20 * s, -60 * s, bot + 20 * s, -150 * s, bot)
    c.close_path(); fs(c, NAVY, 8)
    if k > .6:
        for q in (-1, 1): limb(c, [(q * 40 * s, bot + 10 * s), (q * 46 * s, bot + 80 * s)], 7, WHITE)
    c.restore()

def camera(c, f, g):
    sh = 0
    for hit, amp in ((12, 10), (T_ST + 12 + 2, 10), (STOP[0], 18), (WALL + STOP[1], 16)):
        if hit <= f < hit + 8: sh = amp * (1 - (f - hit) / 8)
    k = 1 + .18 * io((g - T_ST) / 6) * (1 - io((g - T_FALL) / 8))         # in close for the struggle
    k += .07 * io((f - CONTACT + 5) / 5) * (1 - io((f - CONTACT - 10) / 8))
    ax, ay = 420, 1160
    c.translate(ax + noise(f, 1) * sh, ay + noise(f, 2) * sh); c.scale(k, k); c.translate(-ax, -ay)

def closeup(c, g):
    t = g - T_CU
    P.room(c)
    c.save(); c.translate(540, 1000); s = 3.2 + .1 * io(t / 14); c.scale(s, s); c.translate(-(LAP['x0'] + LAP['x1']) / 2, -(LAP['y0'] + LAP['y1']) / 2)
    P.laptop(c, counter(g)); c.restore()
    if T_CU + 7 <= g < T_CU + 12:
        for i in range(3): c.arc(540, 1080, 230 + i * 30, 0, 2 * math.pi); c.set_source_rgba(*YEL, .5 - .12 * i); c.set_line_width(8); c.stroke()

def frame(f):
    S = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(S)
    g = story(f)
    if T_CU <= g < T_ST:
        closeup(c, g); P.topbar(c); return S
    c.save(); camera(c, f, g)
    door_shake = 10 * math.sin((g - WALL) * 2.2) * (1 - cl((g - WALL) / 10)) if g >= WALL else 0
    c.save(); c.translate(door_shake, 0); P.room(c); c.restore()
    P.desk(c); P.laptop(c, counter(g), tick=g >= T_BTN)
    wob = .12 * math.sin(f * 1.7) * (1 if (8 <= g < 24 or CONTACT <= g < CONTACT + 20) else 0)
    late_arm = None

    if g < T_CU:                                                           # 1 THE SHOVE
        t = g
        cx = 270 if t < 12 else lerp(270, CHX - 20, oe((t - 12) / 14))
        if t >= 26: cx = lerp(CHX - 20, CHX, io((t - 26) / 8))
        tilt = -.16 * cl((t - 11) / 3) * (1 - cl((t - 24) / 8))
        P.chair(c, cx, P.SEAT_Y, rot=tilt, spin=max(0, t - 12) * .3)
        shL, shR, head = P.hoody_seated(c, cx, P.SEAT_Y, 'smug' if t < 11 else 'shock', rot=tilt)
        P.hoody_arm(c, shL, (shL[0] - 110, shL[1] - 90), HS, pref=P.LEFT, hand='palm')
        P.hoody_arm(c, shR, (shR[0] + 40, shR[1] - 190), HS, pref=P.RIGHT, hand='palm')
        if 12 <= t < 26: P.lines(c, [(cx + 300, P.SEAT_Y - 170), (cx + 150, P.SEAT_Y - 170)], 3)
        if t < 22:
            x = lerp(P.STAND_X, 520, oe(t / 10)); gy = FLOOR
            chest = ((shL[0] + shR[0]) / 2 + 60, (shL[1] + shR[1]) / 2 + 80)
            A.myai(c, x, gy, AS, eye='happy', look=(18, 0), rot=-.2 if 8 <= t < 20 else -.06, arms=(None, None))
            for q, dy in ((-1, -30), (1, 30)):
                sh = (x + q * 72 * AS, gy - 280 * AS + 112 * AS)
                tgt = (chest[0] + (0 if t < 18 else -60), chest[1] + dy) if t >= 6 else (sh[0] - 40, sh[1] + 90)
                ai_limb(c, sh, tgt, 24 * AS, 130)
            if 10 <= t < 17: burst(c, chest[0] - 10, chest[1], 110, 10)
        else:
            u = io((t - 22) / 16); x = lerp(520, AIX, u); gy = lerp(FLOOR, DESK_Y, u) - math.sin(math.pi * u) * 200
            myai_typing(c, f, x, gy)

    elif g < T_FALL:                                                       # 3 THE THREE ATTEMPTS
        t = g - T_ST
        P.chair(c, CHX - 40, P.SEAT_Y)
        left = None
        if g < A2:                                                        # ATTEMPT 1: the lunge for the keys, SLAP
            u = io(t / 8); hx_ = lerp(CHX - 20, 255, u)
            slap = t >= 12
            shL, shR, head = P.hoody_standing(c, hx_, FLOOR, 'fury' if not slap else 'ouch', bow=lerp(.1, .35, u), gaze=18, side=1)
            reach = (lerp(shR[0] + 80, 560, u), lerp(shR[1] + 120, DESK_Y - 30, u))
            if slap: reach = (reach[0] - 90 * oe((t - 12) / 4), reach[1] - 70 * oe((t - 12) / 4) + 10 * math.sin(t * 3))   # bounced off, shaken
            late_arm = (shR, reach, 'palm')
            P.hoody_arm(c, shL, (shL[0] - 100, shL[1] + 60), HS, pref=P.LEFT, hand='grip')
            sl = (reach[0] + 30, reach[1] - 40) if 9 <= t < 14 else (SH_L[0] - 50, SH_L[1] + 70)
            left_arm = (SH_L, sl, 'palm', 130)
            if 12 <= t < 17: burst(c, reach[0] + 10, reach[1] - 10, 90, 10)
        elif g < A3:                                                      # ATTEMPT 2: at the desk, held off by the forehead, running in place
            t2 = g - A2
            hx_ = 265 + 12 * math.sin(t2 * .8)
            shL, shR, head = P.hoody_standing(c, hx_, FLOOR, 'fury', bow=.42 + .06 * math.sin(t2 * 1.1), gaze=18, side=1)
            dust(c, hx_ - 70, f, 4)
            a_ = t2 * .9
            P.hoody_arm(c, shL, (shL[0] - 70 + 80 * math.cos(a_), shL[1] - 60 + 90 * math.sin(a_)), HS, pref=P.LEFT, hand='grip')
            for i in range(2): c.arc(shL[0] - 70, shL[1] - 60, 120 + i * 22, 1.6, 4.4); c.set_source_rgba(*INK, .35); c.set_line_width(5); c.stroke()
            pump = math.sin(t2 * 1.4)
            P.hoody_arm(c, shR, (shR[0] + 60 + 50 * pump, shR[1] + 150 - 30 * pump), HS, pref=P.DOWN, hand='grip', ang=0)
            fh = (head[0] + 95, head[1] - 60)
            left_arm = (SH_L, (lerp(SH_L[0] - 40, fh[0], oe(t2 / 4)), lerp(SH_L[1] + 60, fh[1], oe(t2 / 4))), 'palm', 170)
            if t2 < 4: burst(c, fh[0], fh[1], 60, 6)
        else:                                                             # ATTEMPT 3: the hood, pulled down over his face; he gropes, blind
            t3 = g - A3
            hx_ = 270 - 30 * io((t3 - 10) / 12) + 8 * math.sin(t3 * .9)
            shL, shR, head = P.hoody_standing(c, hx_, FLOOR, 'fury', bow=.25 - .15 * io((t3 - 10) / 10), gaze=10, side=1)
            k = io((t3 - 4) / 6)
            hood_over(c, head, k)
            for q, sh in ((-1, shL), (1, shR)):                            # groping, arms out, blind
                P.hoody_arm(c, sh, (sh[0] + q * 120 + 30 * math.sin(t3 * .7 + q), sh[1] + 40 + 30 * math.cos(t3 * .8)), HS, pref=P.DOWN, hand='palm')
            grab = (head[0] + 40, head[1] - 160 * HS + 170 * HS * k)
            left_arm = (SH_L, grab if t3 < 12 else (SH_L[0] - 40, SH_L[1] + 70), 'fist' if t3 < 12 else 'palm', 190)
            if t3 >= 10:
                for i in range(3): c.move_to(head[0] - 120 - i * 20, head[1] - 100 + i * 50); c.line_to(head[0] - 170 - i * 20, head[1] - 100 + i * 50)
                c.set_source_rgba(*INK, .35); c.set_line_width(5); c.stroke()
        myai_typing(c, f, AIX, DESK_Y, left=None)
        ai_limb(c, left_arm[0], left_arm[1], 24 * AS, left_arm[3], end=left_arm[2])
        if late_arm: P.hoody_arm(c, late_arm[0], late_arm[1], HS, pref=P.DOWN, hand=late_arm[2], ang=0)

    elif g < T_KICK:                                                       # 4 THE FALL into the chair (with in-betweens)
        t = g - T_FALL
        P.chair(c, CHX, P.SEAT_Y)
        if t < 5:                                                         # shoved: tipping back, hood flipping off
            u = io(t / 5)
            shL, shR, head = P.hoody_standing(c, lerp(270, CHX + 20, u), FLOOR, 'shock', bow=.5 * u, gaze=10, side=-1)
            hood_over(c, head, 1 - u)
            P.hoody_arm(c, shL, (shL[0] - 130, shL[1] - 60), HS, pref=P.LEFT, hand='palm')
            P.hoody_arm(c, shR, (shR[0] + 120, shR[1] - 90), HS, pref=P.RIGHT, hand='palm')
            fh = (head[0] + 95, head[1] - 60)
            myai_typing(c, f, AIX, DESK_Y, left=None); ai_limb(c, SH_L, fh, 24 * AS, 190)
        else:                                                             # falling: hips above the seat, then the plop
            u = io((t - 5) / 5)
            sy = lerp(P.SEAT_Y - 150, P.SEAT_Y, u); tilt = lerp(-.35, 0, u)
            sq = 1 + .12 * math.sin(math.pi * cl((t - 9) / 4))
            c.save(); c.translate(CHX, sy); c.scale(sq, 1 / sq); c.translate(-CHX, -sy)
            shL, shR, head = P.hoody_seated(c, CHX, sy, 'shock', rot=tilt)
            c.restore()
            P.hoody_arm(c, shL, (shL[0] - 110, shL[1] - 80), HS, pref=P.LEFT, hand='palm')
            P.hoody_arm(c, shR, (shR[0] + 50, shR[1] - 180), HS, pref=P.RIGHT, hand='palm')
            myai_typing(c, f, AIX, DESK_Y, left='down')

    else:                                                                  # 5 THE KICK + 6 THE BUTTON
        t = g - T_KICK; c0 = CONTACT - T_KICK; wl = WALL - T_KICK
        hip = (AIX - 34 * AS, DESK_Y - 75 * AS)
        if t < c0: chx, chr_, hop = CHX, 0, 0
        elif t < wl: u = cl((t - c0) / (wl - c0)); chx, chr_, hop = lerp(CHX, 175, u * u), -.2 * u, 40 * math.sin(math.pi * u)
        else: u = oe((t - wl) / 14); chx, chr_, hop = lerp(175, 400, u), .15 * math.sin(math.pi * u), 0
        P.chair(c, chx, P.SEAT_Y - hop, rot=chr_, spin=max(0, t - c0) * .35)
        if t < wl:
            tilt = 0 if t < c0 else -.14 * cl((t - c0) / 6)
            shL, shR, head = P.hoody_seated(c, min(chx, CHX), P.SEAT_Y - hop * 1.3, 'shock' if t >= c0 - 4 else 'dizzy', rot=tilt)
            P.hoody_arm(c, shL, (shL[0] - 110, shL[1] - 80), HS, pref=P.LEFT, hand='palm')
            P.hoody_arm(c, shR, (shR[0] + 50, shR[1] - 180), HS, pref=P.RIGHT, hand='palm')
            if t >= c0: P.lines(c, [(chx + 330, P.SEAT_Y - 160), (chx + 170, P.SEAT_Y - 160)], 4)
        elif t < wl + 4:                                                  # into the door, spilling out
            u = io((t - wl) / 4)
            burst(c, 120, P.SEAT_Y - 220, 120, 10, WHITE, 12)
            c.save(); c.translate(lerp(175, 215, u), lerp(P.SEAT_Y, FLOOR - 10, u)); c.rotate(lerp(-.14, -.4, u))
            P.hoody_seated(c, 0, 0, 'shock', legs=((150, -20), (260, -40)))
            c.restore()
        else:
            sq = 1 + .1 * math.sin(math.pi * cl((t - wl - 4) / 4))
            look_up = g >= T_BTN
            c.save(); c.translate(215, FLOOR - 10); c.scale(sq, 1 / sq); c.rotate(-.12)
            P.hoody_seated(c, 0, 0, 'shock' if T_BTN + 2 <= g < T_BTN + 12 else 'dizzy', legs=((170, -10), (300, 0)))
            c.restore()
            for i in range(3):
                a = f * .3 + i * 2.1; ell(c, 230 + 75 * math.cos(a), FLOOR - 540 + 18 * math.sin(a), 13, 13); c.set_source_rgb(*YEL); c.fill()
        seat = (CHX + 100, P.SEAT_Y - 4)
        if t < c0 - 8: u = io(t / 4); ft = (lerp(hip[0] - 10, hip[0] + 70, u), lerp(hip[1] + 90, hip[1] - 60, u))   # wind-up, cocked high
        elif t < c0: ft = (hip[0] + 70 + 4 * math.sin(t * 3), hip[1] - 60)                                          # held: the cocked leg trembles
        elif t < c0 + 3: ft = seat
        else: u = io((t - c0 - 3) / 6); ft = (lerp(seat[0], hip[0] - 10, u), lerp(seat[1], hip[1] + 90, u))
        ai_limb(c, hip, ft, 44 * AS, 180, end='foot', pref=P.UP)
        if t < c0:
            for i in range(2): c.arc(hip[0] + 60, hip[1] - 20, 130 + i * 24, -2.4, -1.2); c.set_source_rgba(*INK, .45); c.set_line_width(6); c.stroke()
        if c0 <= t < c0 + 6:
            ell(c, seat[0], seat[1], 70, 70); c.set_source_rgba(1, 1, 1, .85); c.fill(); burst(c, seat[0], seat[1], 130, 10, YEL, 12)
        btn = g >= T_BTN
        thumb = (AIX - 150, DESK_Y - 330)
        pl = P.ai_pose(-1, P.ai_local(AIX, DESK_Y, AS, thumb), P.UP) if btn else 'down'
        if btn: myai_typing(c, f, AIX, DESK_Y, left=pl, legs=False, eye='wink', look=(0, 0), turn=-.0)   # it turns to us: a wink
        else: myai_typing(c, f, AIX, DESK_Y, left=pl, legs=False)
        if btn:
            tx, ty = A.hand_at(AIX, DESK_Y, AS, -1, pl); rr(c, tx - 17, ty - 86, 36, 70, 16); fs(c, WHITE, 8)
            if g < T_BTN + 10: burst(c, LAP['x1'] - 30, LAP['y0'] + 30, 70, 8, hx('5df08a'), 8)
    c.save(); c.translate(520, DESK_Y); c.rotate(wob); P.mug(c, 0, 0, 1.1); c.restore()
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
        fs_ = list(range(0, NF, 6)); cols = 11; tw, th = 196, 348
        out = cairo.ImageSurface(cairo.FORMAT_RGB24, cols * tw, ((len(fs_) + cols - 1) // cols) * th); c = cairo.Context(out)
        c.set_source_rgb(1, 1, 1); c.paint()
        for i, f in enumerate(fs_):
            c.save(); c.translate((i % cols) * tw, (i // cols) * th); c.scale(tw / W, th / H); c.set_source_surface(frame(f)); c.paint(); c.restore()
            txt(c, f'{f / 30:.1f}s', (i % cols) * tw + 36, (i // cols) * th + 18, 20, INK, lw=0)
        out.write_to_png('fight_sheet.png'); print('fight_sheet.png', NF / 30)
