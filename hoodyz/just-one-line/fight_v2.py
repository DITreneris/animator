"""Just One Line: the fight, as a motion test (review round 3, "visi a").
Five seconds, four rungs, MY AI never looks away from the screen and never stops typing:
  1 the shove (0.0-0.8)        its palm on his chest; he and the chair roll away, spinning
  2 the forehead (0.8-2.0)     he charges back; its telescopic arm holds him off by the forehead; he windmills, misses
  3 the finger (2.0-2.6)       he jabs a finger up, "ONE line!"; the arm takes the finger and presses Enter with it
  4 the spin (2.6-3.5)         he drops into the chair; a flick of the arm spins him round
  5 the kick (3.5-5.0)         knee up, contact (3-frame hit-stop, shake, push-in), flight, landing; the foot hooks the chair back
Camera: locked, shake on hits, a push-in on the kick. Squash and stretch on Hoody, speed lines, papers, the mug wobbles.
Usage: python3 fight.py sheet | video"""
import os, sys, math, random, subprocess, cairo
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import kp as P
from kp import K, A, INK, WHITE, NAVY, SKIN, GREY, YEL, rr, fs, ell, limb, txt, hx, lerp, W, H, FLOOR, HS, AS, KEY, LAP, DESK_Y
cl = lambda t: max(0.0, min(1.0, t)); oe = lambda t: 1 - (1 - cl(t)) ** 3; io = lambda t: (lambda u: u * u * (3 - 2 * u))(cl(t))
K.FACES['dizzy'] = ('spiral', (None, None), 'wobble')
NF = 159
HOLD = 9                              # frames held on the Enter press (his face registers 12 -> 19)
def story(f):
    if f < 72: return f
    if f < 72 + HOLD: return 72
    s_ = f - HOLD
    return 114 if 112 <= s_ < 115 else s_
STEP_X = 560
def noise(f, k): return random.Random(f * 7919 + k).uniform(-1, 1)

def counter(f):
    if f < 24: return int(lerp(0, 3, f / 24))
    if f < 60: return int(lerp(3, 12, (f - 24) / 36))
    if f < 72: return 12
    if f < 86: return 19
    if f < 112: return int(lerp(19, 26, (f - 86) / 26))
    return 31

def tele_arm(c, sh, tgt, s, hand='open', ang=None):
    """MY AI's telescopic arm: straight, in sleeves that slide out of each other (rings at the joins)."""
    dx, dy = tgt[0] - sh[0], tgt[1] - sh[1]; L = math.hypot(dx, dy) or 1; ux, uy = dx / L, dy / L
    limb(c, [sh, tgt], 22 * s, WHITE)
    n = max(1, int(L / (60 * s)))
    for i in range(1, n):
        p = (sh[0] + ux * L * i / n, sh[1] + uy * L * i / n)
        c.save(); c.translate(*p); c.rotate(math.atan2(uy, ux)); rr(c, -6 * s, -15 * s, 12 * s, 30 * s, 5 * s); fs(c, GREY, 4); c.restore()
    a = math.atan2(uy, ux) if ang is None else ang
    if hand == 'open': K.palm(c, tgt[0], tgt[1], s * .45, a, flick=0)
    else: ell(c, tgt[0], tgt[1], 18 * s, 18 * s); fs(c, WHITE, 6)

def ai_shoulder(x, gy, q=-1): return (x + q * 72 * AS, gy - 280 * AS + 112 * AS)

def myai_at(c, f, x, gy, left=None, rot=0.0, legs=True, eye='happy'):
    """MY AI typing with its right hand, looking at the screen; the left arm is drawn by the caller (left=None) or posed."""
    tap = 10 * math.sin(f * 2.3)
    right = P.ai_pose(1, P.ai_local(x, gy, AS, (KEY[0] + tap, KEY[1] - abs(tap))), P.DOWN)
    old = A.limb
    if not legs: A.limb = lambda c_, pts, *a: None if pts == [(-34, 205), (-34, 280)] else old(c_, pts, *a)
    try: A.myai(c, x, gy, AS, eye=eye, look=(18, 0), rot=rot, arms=(left, right), bob=3 * math.sin(f * .6))
    finally: A.limb = old

def hoody_back(c, x, seat_y, s=HS):
    """Hoody from behind: the same head and hair silhouette as the front, the face painted over with hair."""
    K.hoodie(c, x + 6 * s, seat_y - 210 * s, s * 1.1)
    hx_, hy = x + 10 * s, seat_y - 210 * s - 150 * s
    K.hoodyz_head(c, hx_, hy, s, era='young', expr='calm', blink=False)
    c.save(); c.translate(hx_, hy); c.scale(s, s); rr(c, -100, -72, 200, 178, 84); c.set_source_rgb(*K.HAIR_DARK); c.fill()
    c.move_to(-60, 60); c.curve_to(-20, 90, 20, 90, 60, 60); c.set_source_rgba(0, 0, 0, .25); c.set_line_width(6); c.stroke(); c.restore()

def hoody_spin(c, x, seat_y, th, f, expr):
    """One continuous turn: front while he faces us, back while he faces away; never squashed (the head keeps its shape)."""
    if math.cos(th) > 0: P.hoody_seated(c, x, seat_y, expr)
    else: hoody_back(c, x, seat_y)
    for i in range(3):
        c.arc(x, seat_y - 250, 190 + i * 24, -2.4, -1.0); c.set_source_rgba(*INK, .4); c.set_line_width(6); c.stroke()

def papers(c, f):
    if f < 112: return
    r = random.Random(3)
    for i in range(4):
        t = (f - 112) / 30; vx = r.uniform(-9, -4); vy = r.uniform(-14, -8); sp = r.uniform(-.3, .3)
        x = 600 + vx * (f - 112) * 1.6; y = 1170 + vy * (f - 112) * 1.6 + .5 * 1.1 * (f - 112) ** 2
        if y > FLOOR - 10: y = FLOOR - 10; sp = 0
        c.save(); c.translate(x, y); c.rotate(sp * (f - 112) + i); rr(c, -40, -28, 80, 56, 4); fs(c, WHITE, 5)
        for j in range(3): c.move_to(-28, -14 + j * 12); c.line_to(24, -14 + j * 12)
        c.set_source_rgba(*GREY, 1); c.set_line_width(3); c.stroke(); c.restore()

def camera(c, f):
    """Shake on the hits, a push-in on the kick; hit-stop handled in frame mapping."""
    sh = 0
    for hit, amp in ((6, 14), (112 + HOLD, 26), (129 + HOLD, 16)):
        if hit <= f < hit + 8: sh = amp * (1 - (f - hit) / 8)
    k = 1 + .12 * io((f - 104 - HOLD) / 6) * (1 - io((f - 116 - HOLD) / 8))
    ax, ay = 460, 1250
    c.translate(ax + noise(f, 1) * sh, ay + noise(f, 2) * sh); c.scale(k, k); c.translate(-ax, -ay)

def frame(f):
    S = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(S)
    g = story(f)                                                              # holds: the Enter press, the kick's contact
    c.save(); camera(c, f)
    P.room(c); P.desk(c); P.laptop(c, counter(g))
    wob = .12 * math.sin(f * 1.7) * (1 if (4 <= f < 20 or 112 + HOLD <= f < 135 + HOLD) else 0)
    c.save(); c.translate(560, DESK_Y); c.rotate(wob); P.mug(c, 0, 0, 1.1); c.restore()
    papers(c, g)
    P.step(c, STEP_X)
    top = FLOOR - 150

    if g < 24:                                                             # 1 THE SHOVE
        t = g
        cx = lerp(260, 130, oe((t - 5) / 18)) if t >= 5 else 260; spin = t * .5
        tilt = -.12 * cl((t - 4) / 3)
        P.chair(c, cx, P.SEAT_Y, rot=tilt, spin=spin)
        sq = 1 + .12 * math.sin(math.pi * cl((t - 4) / 6))                     # squash on contact
        c.save(); c.translate(cx, P.SEAT_Y); c.scale(sq, 1 / sq); c.translate(-cx, -P.SEAT_Y)
        shL, shR, head = P.hoody_seated(c, cx, P.SEAT_Y, 'shock' if t >= 4 else 'smug', rot=tilt)
        c.restore()
        P.hoody_arm(c, shL, (shL[0] - 110, shL[1] - 90), HS, pref=P.LEFT, hand='palm')
        P.hoody_arm(c, shR, (shR[0] + 30, shR[1] - 200), HS, pref=P.RIGHT, hand='palm')
        if t < 14:                                                        # standing, the push
            x = lerp(P.STAND_X, 590, oe(t / 4)); gy = FLOOR
            chest = ((shL[0] + shR[0]) / 2 + 60, (shL[1] + shR[1]) / 2 + 80)
            reach = chest if t < 9 else (x - 120, 1250)
            pa = P.ai_pose(-1, P.ai_local(x, gy, AS, reach), P.DOWN)
            A.myai(c, x, gy, AS, eye='happy', look=(18, 0), rot=-.12, arms=(pa, 'down'))
            if 4 <= t < 9:
                for i in range(3): c.arc(reach[0] - 10, reach[1], 46 + i * 24, 2.3, 4.0); c.set_source_rgba(*INK, .5); c.set_line_width(6); c.stroke()
        else:                                                             # the hop onto the step
            u = io((t - 14) / 10); x = lerp(590, STEP_X, u); gy = lerp(FLOOR, top, u) - math.sin(math.pi * u) * 80
            myai_at(c, f, x, gy, left='down')
        if t >= 5: P.lines(c, [(cx + 300, P.SEAT_Y - 150), (cx + 150, P.SEAT_Y - 150)], 3)

    elif g < 60:                                                           # 2 THE FOREHEAD
        t = g - 24
        P.chair(c, 130, P.SEAT_Y, spin=2.5)
        hx_ = lerp(90, 150, oe(t / 10)); bow = .2
        stretch = 1 + .1 * math.sin(math.pi * cl(t / 8))
        c.save(); c.translate(hx_, FLOOR); c.scale(1 / stretch, stretch); c.translate(-hx_, -FLOOR)
        shL, shR, head = P.hoody_standing(c, hx_, FLOOR, 'strain', bow=bow, gaze=14, side=1)
        c.restore()
        for q, sh in ((-1, shL), (1, shR)):                              # windmill punches that never land
            ph = t * .9 + (0 if q < 0 else math.pi)
            tgt = (sh[0] + 60 + 150 * math.cos(ph), sh[1] - 40 + 150 * math.sin(ph))
            P.hoody_arm(c, sh, tgt, HS, pref=P.UP if math.sin(ph) < 0 else P.DOWN, hand='grip')
        for i in range(2):
            c.arc(head[0] + 40, head[1] + 60, 200 + i * 30, -1.0, .2); c.set_source_rgba(*INK, .35); c.set_line_width(6); c.stroke()
        myai_at(c, f, STEP_X, top, left=None)
        sh = ai_shoulder(STEP_X, top)
        ext = oe((t - 4) / 5)
        fh = (head[0] + 75, head[1] - 70)
        tele_arm(c, sh, (lerp(sh[0], fh[0], ext), lerp(sh[1], fh[1], ext)), AS, hand='open', ang=math.pi)

    elif g < 78:                                                           # 3 THE FINGER: "ONE line!" -> Enter
        t = g - 60
        P.chair(c, 130, P.SEAT_Y, spin=2.5)
        yank = io((t - 5) / 6) * (1 - io((t - 12) / 6))
        hx_ = lerp(340, 400, yank)
        shL, shR, head = P.hoody_standing(c, hx_, FLOOR, 'strain' if t < 5 else 'shock', bow=lerp(.45, .75, yank), gaze=14, side=1)
        P.hoody_arm(c, shL, (shL[0] - 60, shL[1] + 120), HS, pref=P.LEFT, hand='palm')
        up = (shR[0] + 20, shR[1] - 230)
        tip = (lerp(up[0], KEY[0] + 40, yank), lerp(up[1], KEY[1] - 10, yank))
        limb(c, [shR, tip], 44 * HS * (1 - .3 * yank), NAVY)                 # his arm, stretched by the robot
        P.point(c, tip[0], tip[1], math.atan2(tip[1] - shR[1], tip[0] - shR[0]), HS)
        myai_at(c, f, STEP_X, top, left=None)
        sh = ai_shoulder(STEP_X, top)
        tele_arm(c, sh, (tip[0] - 10, tip[1] + 10), AS, hand='fist')
        if 11 <= t < 15:
            for i in range(3): c.arc(KEY[0] + 40, KEY[1] - 10, 30 + i * 22, 0, 2 * math.pi); c.set_source_rgba(*YEL, .8); c.set_line_width(6); c.stroke()

    elif g < 105:                                                          # 4 THE SPIN: he falls back, the chair rolls under him,
        t = g - 78                                                         #   he plops in; one flick, one full turn
        chx = lerp(130, 300, oe(t / 6))
        if t < 8:
            P.chair(c, chx, P.SEAT_Y)
            hx_ = lerp(400, 310, io(t / 8))
            shL, shR, head = P.hoody_standing(c, hx_, FLOOR, 'shock', bow=.35 * io(t / 8), gaze=-10, side=-1)   # tipping back
            P.hoody_arm(c, shL, (shL[0] - 120, shL[1] - 40), HS, pref=P.LEFT, hand='palm')
            P.hoody_arm(c, shR, (shR[0] + 110, shR[1] - 60), HS, pref=P.RIGHT, hand='palm')
        else:
            th = 2 * math.pi * io((t - 9) / 16)
            P.chair(c, 300, P.SEAT_Y, spin=th)
            sq = 1 + .07 * math.sin(math.pi * cl((t - 8) / 3))
            c.save(); c.translate(300, P.SEAT_Y); c.scale(1, 1 / sq); c.translate(-300, -P.SEAT_Y)
            hoody_spin(c, 300, P.SEAT_Y, th, f, 'shock')
            c.restore()
        myai_at(c, f, STEP_X, top, left=None)
        sh = ai_shoulder(STEP_X, top)
        flick = io((t - 6) / 3) * (1 - io((t - 11) / 4))
        tele_arm(c, sh, (lerp(sh[0] - 70, 420, flick), lerp(sh[1] + 70, P.SEAT_Y - 230, flick)), AS, hand='open', ang=math.pi)

    else:                                                                  # 5 THE KICK
        t = g - 105
        r = .06
        def w(lx, ly, x=STEP_X, gy=top):
            X, Y = lx * AS, ly * AS - 280 * AS; ca, sa = math.cos(r), math.sin(r)
            return (x + X * ca - Y * sa, gy + X * sa + Y * ca)
        hip = w(-34, 205)
        if t < 7:   u = io(t / 6); kn, ft = w(lerp(-34, -10, u), lerp(250, 175, u)), w(lerp(-34, -40, u), lerp(280, 215, u))   # knee up
        elif t < 24:                                                       # out, low: the foot on the chair's column, under his thighs
            dx = 0 if t < 9 else (300 - (300 - 70 * min(1, (t - 7) / 7) ** 2)) * .4
            kn, ft = (440 - dx, 1385), (345 - dx, 1415)
        else:
            u = io((t - 24) / 6); k0, f0 = (412, 1385), (317, 1415)
            kn, ft = (lerp(k0[0], w(-34, 245)[0], u), lerp(k0[1], w(-34, 245)[1], u)), (lerp(f0[0], w(-34, 280)[0], u), lerp(f0[1], w(-34, 280)[1], u))
        # the chair: still until the contact (t 7), then slides with him, accelerating; at t 14 it shoots away without him;
        # from t 30 the arm drags it back to the desk
        if t < 7: chx, chr_ = 300, 0
        elif t < 14: u = (t - 7) / 7; chx, chr_ = 300 - 70 * u * u, -.1 * u
        elif t < 30: u = oe((t - 14) / 10); chx, chr_ = lerp(230, 105, u), lerp(-.1, .6, u)
        else: u = io((t - 32) / 12); chx, chr_ = lerp(105, 300, u), lerp(.6, 0, u)
        P.chair(c, chx, P.SEAT_Y, rot=chr_, spin=t * .25)
        if t < 14:                                                        # in the chair: a look down, then tipping back
            tilt = 0 if t < 7 else -.35 * (t - 7) / 7
            shL, shR, head = P.hoody_seated(c, chx, P.SEAT_Y, 'shock', rot=tilt)
            P.hoody_arm(c, shL, (shL[0] - 120, shL[1] - 60), HS, pref=P.LEFT, hand='palm')
            P.hoody_arm(c, shR, (shR[0] + 60, shR[1] - 170), HS, pref=P.RIGHT, hand='palm')
            if t >= 7: P.lines(c, [(chx + 260, P.SEAT_Y - 120), (chx + 140, P.SEAT_Y - 120)], 3)
        elif t < 24:                                                      # off the chair, backward, a short arc to the floor
            u = (t - 14) / 10
            px = lerp(230, 235, u); py = lerp(P.SEAT_Y, FLOOR - 10, u * u) - math.sin(math.pi * u) * 90; a = lerp(-.35, -.9, u)
            c.save(); c.translate(px, py); c.rotate(a)
            P.hoody_seated(c, 0, 0, 'shock', legs=((150, -40), (250, -150)))
            c.restore()
        else:                                                             # down: a small squash of the body, dazed, against the door
            sq = 1 + .08 * math.sin(math.pi * cl((t - 24) / 4))
            c.save(); c.translate(235, FLOOR - 10); c.scale(sq, 1 / sq); c.rotate(-.12)
            P.hoody_seated(c, 0, 0, 'dizzy', legs=((170, -10), (300, 0)))
            c.restore()
            for i in range(3):
                a = f * .3 + i * 2.1; ell(c, 250 + 75 * math.cos(a), FLOOR - 540 + 18 * math.sin(a), 11, 11); c.set_source_rgb(*YEL); c.fill()
        limb(c, [hip, kn, ft], 34 * AS, WHITE)
        c.save(); c.translate(*ft); c.rotate(math.atan2(ft[1] - kn[1], ft[0] - kn[0])); rr(c, -26, -24, 64, 48, 20); fs(c, WHITE, 7); c.restore()
        if 7 <= t < 12:
            for i in range(3): c.arc(ft[0] - 10, ft[1], 40 + i * 22, 2.2, 4.1); c.set_source_rgba(*INK, .6); c.set_line_width(7); c.stroke()
        if t < 30:                                                        # the thumb, up, over its shoulder - never a look back
            thumb = (STEP_X - 150, 1075)
            pl = P.ai_pose(-1, P.ai_local(STEP_X, top, AS, thumb), P.UP) if t >= 7 else 'down'
            myai_at(c, f, STEP_X, top, left=pl, rot=r, legs=False)
            if t >= 7: tx, ty = A.hand_at(STEP_X, top, AS, -1, pl); rr(c, tx - 12, ty - 66, 26, 50, 12); fs(c, WHITE, 7)
        else:                                                             # the arm fetches the chair back
            myai_at(c, f, STEP_X, top, left=None, rot=r, legs=False)
            sh = ai_shoulder(STEP_X, top)
            grab = (chx + 90, P.SEAT_Y - 10)
            ext = io((t - 30) / 3)
            tele_arm(c, sh, (lerp(sh[0] - 60, grab[0], ext), lerp(sh[1] + 60, grab[1], ext)), AS, hand='fist')
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
        fs_ = list(range(0, NF, 6)); cols = 10; tw, th = 216, 384
        out = cairo.ImageSurface(cairo.FORMAT_RGB24, cols * tw, ((len(fs_) + cols - 1) // cols) * th); c = cairo.Context(out)
        for i, f in enumerate(fs_):
            c.save(); c.translate((i % cols) * tw, (i // cols) * th); c.scale(tw / W, th / H); c.set_source_surface(frame(f)); c.paint(); c.restore()
            txt(c, f'{f / 30:.1f}s', (i % cols) * tw + 40, (i // cols) * th + 20, 22, INK, lw=0)
        out.write_to_png('fight_sheet.png'); print('fight_sheet.png')
