"""Just One Line: the fight, motion test v6 (mute test 12: follow 6/6, intensity 4/4 -> the struggle has to move).
  1 THE SHOVE    both robot palms on his chest, held; he and the chair roll left
  2 THE SCREEN   a close-up: FILES CHANGED 2 -> 3
  3 THE STRUGGLE he springs up (on screen) and drives forward, feet slipping, one hand clawing for the keyboard;
                 its arm on his forehead stretches under the load but it never moves; every time he gains an inch
                 the counter jumps
  4 THE PUSH     the palm walks him back, three stumbling steps, and sits him in his chair (on screen)
  5 THE KICK     wind-up, a big impact on the seat, hit-stop; the chair shoots him to the door, he tips out onto the
                 floor (on screen) and the chair rolls back out on its own; dazed
  6 THE BUTTON   the counter ticks 31 -> 32; MY AI, still not looking, a thumbs-up and a happy wiggle
Hoody never goes behind MY AI; MY AI never looks at him. Earlier versions: fight_v2/v3/v5.py.
Usage: python3 fight.py sheet | video"""
import os, sys, math, random, subprocess, cairo
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import kp as P
from kp import K, A, INK, WHITE, NAVY, SKIN, GREY, YEL, rr, fs, ell, limb, txt, hx, lerp, W, H, FLOOR, HS, AS, KEY, LAP, DESK_Y
cl = lambda t: max(0.0, min(1.0, t)); oe = lambda t: 1 - (1 - cl(t)) ** 3; io = lambda t: (lambda u: u * u * (3 - 2 * u))(cl(t))
K.FACES['dizzy'] = ('spiral', (None, None), 'wobble')
K.FACES['fury'] = ('open', ('angry', 'angry'), 'frown')
T_CU, T_ST, T_PUSH, T_KICK, T_BTN, T_END = 40, 54, 108, 128, 168, 190
CONTACT = T_KICK + 8
STOP = (CONTACT, 4)
NF = T_END + STOP[1]
AIX = 610
CHX = 230
NEAR = [None]
def story(f): return f if f < STOP[0] else (STOP[0] if f < STOP[0] + STOP[1] else f - STOP[1])
def noise(f, k): return random.Random(f * 7919 + k).uniform(-1, 1)
SH_L = (AIX - 72 * AS, DESK_Y - 280 * AS + 112 * AS)                # MY AI's left shoulder on the desk

# the struggle: he gains ground in three surges; each surge pays the counter
SURGES = [(8, 16), (22, 30), (36, 44)]                              # (start, end) in struggle frames
def gain(t):
    g = 0.0
    for a, b in SURGES: g += 34 * io((t - a) / (b - a))
    return g

def counter(g):
    if g < T_CU: return int(lerp(0, 2, g / T_CU))
    if g < T_ST: return 2 if g < T_CU + 7 else 3
    if g < T_PUSH:
        t = g - T_ST; n = 3 + int(3 * t / 54)
        for a, b in SURGES: n += int(5 * io((t - a) / (b - a)))
        return n
    if g < CONTACT: return 24
    if g < T_BTN + 6: return 31
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
    return h

def myai_typing(c, f, x, gy, left='down', legs=True, eye='happy', bob=None):
    tap = 10 * math.sin(f * 2.3)
    right = P.ai_pose(1, P.ai_local(x, gy, AS, (KEY[0] + tap, KEY[1] - abs(tap))), P.DOWN)
    old = A.limb
    if not legs: A.limb = lambda c_, pts, *a: None if pts == [(-34, 205), (-34, 280)] else old(c_, pts, *a)
    try: A.myai(c, x, gy, AS, eye=eye, look=(18, 0), arms=(left, right), bob=3 * math.sin(f * .6) if bob is None else bob)
    finally: A.limb = old

def burst(c, x, y, r, n=8, col=YEL, w=10):
    for i in range(n):
        a = i * 2 * math.pi / n + .2; c.move_to(x + r * .4 * math.cos(a), y + r * .4 * math.sin(a)); c.line_to(x + r * math.cos(a), y + r * math.sin(a))
    c.set_source_rgb(*col); c.set_line_width(w); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()

def dust(c, x, f, n=3):
    for i in range(n):
        ell(c, x - i * 28 + 6 * math.sin(f + i), FLOOR - 14 - i * 7, 16 - i * 3, 9 - i * 2); c.set_source_rgba(.6, .55, .5, .75); c.fill()

def camera(c, f):
    sh = 0
    for hit, amp in ((12, 10), (STOP[0], 18), (STOP[0] + STOP[1] + 14, 8)):
        if hit <= f < hit + 8: sh = amp * (1 - (f - hit) / 8)
    k = 1 + .07 * io((f - CONTACT + 5) / 5) * (1 - io((f - CONTACT - 10) / 8))
    ax, ay = 400, 1250
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
    c.save(); camera(c, f)
    P.room(c); P.desk(c); P.laptop(c, counter(g), tick=g >= T_BTN + 6)
    wob = .12 * math.sin(f * 1.7) * (1 if (8 <= g < 24 or CONTACT <= g < CONTACT + 20) else 0)
    mug_at = (520, DESK_Y)

    if g < T_CU:                                                           # 1 THE SHOVE: both palms on his chest
        t = g
        cx = 270 if t < 12 else lerp(270, CHX - 20, oe((t - 12) / 14))
        if t >= 26: cx = lerp(CHX - 20, CHX, io((t - 26) / 8))            # a small roll back: it settles
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
            for q, dy in ((-1, -30), (1, 30)):                            # both arms, both palms
                sh = (x + q * 72 * AS, gy - 280 * AS + 112 * AS)
                tgt = (chest[0] + (0 if t < 18 else -60), chest[1] + dy) if t >= 6 else (sh[0] - 40, sh[1] + 90)
                ai_limb(c, sh, tgt, 24 * AS, 130)
            if 10 <= t < 16: burst(c, chest[0] - 10, chest[1], 90)
        else:
            u = io((t - 22) / 16); x = lerp(520, AIX, u); gy = lerp(FLOOR, DESK_Y, u) - math.sin(math.pi * u) * 200
            for i in range(2): c.arc(x, gy - 40, 60 + i * 30, 1.2, 2.0); c.set_source_rgba(*INK, .4); c.set_line_width(5); c.stroke()
            myai_typing(c, f, x, gy)

    elif g < T_PUSH:                                                       # 3 THE STRUGGLE
        t = g - T_ST
        P.chair(c, CHX, P.SEAT_Y)
        if t < 6:                                                         # springing up out of the chair, on screen
            u = io(t / 6)
            shL, shR, head = P.hoody_seated(c, CHX + 20 * u, P.SEAT_Y - 120 * u, 'fury')
            P.hoody_arm(c, shL, (shL[0] - 60, shL[1] + 120), HS, pref=P.LEFT, hand='grip')
            P.hoody_arm(c, shR, (shR[0] + 60, shR[1] + 120), HS, pref=P.RIGHT, hand='grip')
            fh = (head[0] + 95, head[1] - 60)
        else:                                                             # running in place against the palm, arms whirling behind
            gn = gain(t); push = any(a <= t < b for a, b in SURGES)
            hx_ = CHX - 50 + gn
            bow = .42 + .08 * math.sin(t * 1.1) + (.06 if push else 0)
            shL, shR, head = P.hoody_standing(c, hx_, FLOOR, 'fury', bow=bow, gaze=18, side=1)
            dust(c, hx_ - 70, f, 4)
            for i in range(3): c.move_to(hx_ - 140 - i * 22, FLOOR - 40 - i * 34); c.line_to(hx_ - 210 - i * 22, FLOOR - 40 - i * 34)
            c.set_source_rgba(*INK, .35); c.set_line_width(5); c.stroke()
            a_ = t * .9                                                   # the outer arm whirls on his left, outside his body;
            P.hoody_arm(c, shL, (shL[0] - 70 + 80 * math.cos(a_), shL[1] - 60 + 90 * math.sin(a_)), HS, pref=P.LEFT, hand='grip')
            for i in range(2): c.arc(shL[0] - 70, shL[1] - 60, 120 + i * 22, 1.6, 4.4); c.set_source_rgba(*INK, .35); c.set_line_width(5); c.stroke()
            pump = math.sin(t * 1.4)                                      # the near arm pumps like a runner's, below its arm
            late = io((t - 38) / 6)                                       # ...until the last surge: a grab at the keys, short
            NEAR[0] = (shR, (lerp(shR[0] + 60 + 50 * pump, KEY[0] - 70, late), lerp(shR[1] + 150 - 30 * pump, KEY[1] - 20, late)), late)
            fh = (head[0] + 95, head[1] - 60)
            for dx, dy in ((60, -70), (100, -30), (-80, -40)):
                ell(c, head[0] + dx, head[1] + dy + (t % 6) * 3, 8, 13); fs(c, hx('58c7ff'), 4)
        myai_typing(c, f, AIX, DESK_Y, left=None)
        if t >= 6 and NEAR[0]:
            sh_, tg_, late = NEAR[0]; P.hoody_arm(c, sh_, tg_, HS, pref=P.DOWN, hand='palm' if late > .5 else 'grip', ang=0)
            if late > .5:
                for i in range(2): c.arc(tg_[0] + 40, tg_[1], 24 + i * 16, -1.3, 1.3); c.set_source_rgba(*INK, .5); c.set_line_width(5); c.stroke()
        ext = oe((t - 2) / 4)
        ai_limb(c, SH_L, (lerp(SH_L[0] - 40, fh[0], ext), lerp(SH_L[1] + 60, fh[1], ext)), 24 * AS, 170)
        if 2 <= t < 6: burst(c, fh[0], fh[1], 60, 6)

    elif g < T_KICK:                                                       # 4 THE PUSH: walked back and sat down
        t = g - T_PUSH
        P.chair(c, CHX, P.SEAT_Y)
        gn = gain(99); u = io(t / 15)
        if t < 15:
            hx_ = lerp(CHX - 50 + gn, CHX + 10, u)
            shL, shR, head = P.hoody_standing(c, hx_, FLOOR, 'shock', bow=lerp(.3, .35, u), gaze=10, side=-1 if t > 2 else 1)
            step_ = abs(math.sin(t * 1.4)) * 18                            # stumbling steps
            P.hoody_arm(c, shL, (shL[0] - 120, shL[1] - 30 - step_), HS, pref=P.LEFT, hand='palm')
            P.hoody_arm(c, shR, (shR[0] + 110, shR[1] - 70), HS, pref=P.RIGHT, hand='palm')
            fh = (head[0] + 95, head[1] - 60)
            ai_limb(c, SH_L, fh, 24 * AS, 170)
            for i in range(2): c.arc(fh[0] + 10, fh[1], 40 + i * 22, -.6, 1.0); c.set_source_rgba(*INK, .5); c.set_line_width(6); c.stroke()
        else:                                                             # plop
            sq = 1 + .1 * math.sin(math.pi * cl((t - 15) / 3))
            c.save(); c.translate(CHX, P.SEAT_Y); c.scale(sq, 1 / sq); c.translate(-CHX, -P.SEAT_Y)
            shL, shR, head = P.hoody_seated(c, CHX, P.SEAT_Y, 'shock')
            c.restore()
            P.hoody_arm(c, shL, (shL[0] - 110, shL[1] - 80), HS, pref=P.LEFT, hand='palm')
            P.hoody_arm(c, shR, (shR[0] + 50, shR[1] - 180), HS, pref=P.RIGHT, hand='palm')
            ai_limb(c, SH_L, (SH_L[0] - 60, SH_L[1] + 80), 24 * AS, 120)
        myai_typing(c, f, AIX, DESK_Y, left=None)

    else:                                                                  # 5 THE KICK + 6 THE BUTTON
        t = g - T_KICK; c0 = CONTACT - T_KICK
        hip = (AIX - 34 * AS, DESK_Y - 75 * AS)
        # the chair: shot to the door with him; it hits the door, he tips out, and it rolls back out on its own
        if t < c0: chx, chr_ = CHX, 0
        elif t < c0 + 10: u = cl((t - c0) / 10); chx, chr_ = lerp(CHX, 175, 1 - (1 - u) ** 2), -.2 * math.sin(math.pi * u)
        else: u = oe((t - c0 - 10) / 14); chx, chr_ = lerp(175, 400, u), .15 * math.sin(math.pi * u)
        hop = 50 * math.sin(math.pi * cl((t - c0) / 10)) if c0 <= t < c0 + 10 else 0
        P.chair(c, chx, P.SEAT_Y - hop, rot=chr_, spin=max(0, t - c0) * .35)
        if t < c0 + 10:
            tilt = 0 if t < c0 else -.14 * cl((t - c0) / 6)
            shL, shR, head = P.hoody_seated(c, min(chx, CHX), P.SEAT_Y - hop * 1.3, 'shock', rot=tilt)
            P.hoody_arm(c, shL, (shL[0] - 110, shL[1] - 80), HS, pref=P.LEFT, hand='palm')
            P.hoody_arm(c, shR, (shR[0] + 50, shR[1] - 180), HS, pref=P.RIGHT, hand='palm')
            if t >= c0: P.lines(c, [(chx + 330, P.SEAT_Y - 160), (chx + 170, P.SEAT_Y - 160)], 4)
        elif t < c0 + 14:                                                 # tipping out of the chair onto the floor
            u = io((t - c0 - 10) / 4)
            c.save(); c.translate(lerp(175, 215, u), lerp(P.SEAT_Y, FLOOR - 10, u)); c.rotate(lerp(-.14, -.4, u))
            P.hoody_seated(c, 0, 0, 'shock', legs=((150, -20), (260, -40)))
            c.restore()
        else:
            sq = 1 + .1 * math.sin(math.pi * cl((t - c0 - 14) / 4))
            c.save(); c.translate(215, FLOOR - 10); c.scale(sq, 1 / sq); c.rotate(-.12)
            look_up = T_BTN + 6 <= g < T_BTN + 16
            P.hoody_seated(c, 0, 0, 'shock' if look_up else 'dizzy', legs=((170, -10), (300, 0)))
            c.restore()
            for i in range(3):
                a = f * .3 + i * 2.1; ell(c, 230 + 75 * math.cos(a), FLOOR - 540 + 18 * math.sin(a), 13, 13); c.set_source_rgb(*YEL); c.fill()
        seat = (CHX + 100, P.SEAT_Y - 4)
        if t < c0 - 6: ft = (hip[0] - 10, hip[1] + 90)
        elif t < c0: u = io((t - c0 + 6) / 6); ft = (lerp(hip[0] - 10, hip[0] + 60, u), lerp(hip[1] + 90, hip[1] - 40, u))   # wind-up: leg cocked high
        elif t < c0 + 3: ft = seat
        else: u = io((t - c0 - 3) / 6); ft = (lerp(seat[0], hip[0] - 10, u), lerp(seat[1], hip[1] + 90, u))
        ai_limb(c, hip, ft, 44 * AS, 180, end='foot', pref=P.UP)
        if c0 - 6 <= t < c0:
            for i in range(2): c.arc(hip[0] + 40, hip[1], 120 + i * 24, -2.2, -1.0); c.set_source_rgba(*INK, .45); c.set_line_width(6); c.stroke()
        if c0 <= t < c0 + 6:                                              # the impact
            ell(c, seat[0], seat[1], 70, 70); c.set_source_rgba(1, 1, 1, .85); c.fill()
            burst(c, seat[0], seat[1], 130, 10, YEL, 12)
        btn = g >= T_BTN
        wig = math.sin((g - T_BTN) * .9) * 6 if btn else 0
        thumb = (AIX - 150, DESK_Y - 330 + wig)
        pl = P.ai_pose(-1, P.ai_local(AIX, DESK_Y, AS, thumb), P.UP) if t >= c0 else 'down'
        myai_typing(c, f, AIX, DESK_Y, left=pl, legs=False, bob=(abs(wig) if btn else None))
        if t >= c0:
            tx, ty = A.hand_at(AIX, DESK_Y, AS, -1, pl); rr(c, tx - 17, ty - 86, 36, 70, 16); fs(c, WHITE, 8)
        if btn and g < T_BTN + 12:
            burst(c, LAP['x1'] - 30, LAP['y0'] + 30, 60, 8, hx('5df08a'), 8)
    c.save(); c.translate(*mug_at); c.rotate(wob); P.mug(c, 0, 0, 1.1); c.restore()   # the mug, always on top: never "on the leg"
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
        out.write_to_png('fight_sheet.png'); print('fight_sheet.png')
