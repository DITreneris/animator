"""Just One Line: the fight, motion test v3 (mute test 9: the middle read as a windmill; "visi a").
Three rungs, one clear action each, about 1.5 s each; Hoody never goes behind MY AI (a visible gap all the way);
MY AI never looks at him and never stops typing. (v2 kept as fight_v2.py.)
  1 THE SHOVE    (0.0-1.3)  its palm flat on his chest, held; he and the chair roll left; it hops up onto the desk
  2 THE FOREHEAD (1.3-3.0)  he gets up and charges; its arm, straight out, holds him off by the forehead; he punches
                            the air, short every time; the counter climbs
  3 THE KICK     (3.0-4.7)  it lets go, he stumbles forward, its foot meets his chest (hit-stop, shake, push-in),
                            he flies back to the door and sits there, dazed; a thumbs-up over its shoulder
Usage: python3 fight.py sheet | video"""
import os, sys, math, random, subprocess, cairo
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import kp as P
from kp import K, A, INK, WHITE, NAVY, SKIN, GREY, YEL, rr, fs, ell, limb, txt, hx, lerp, W, H, FLOOR, HS, AS, KEY, LAP, DESK_Y
cl = lambda t: max(0.0, min(1.0, t)); oe = lambda t: 1 - (1 - cl(t)) ** 3; io = lambda t: (lambda u: u * u * (3 - 2 * u))(cl(t))
K.FACES['dizzy'] = ('spiral', (None, None), 'wobble')
STOP = (100, 3)                       # hit-stop: story frame 100 (the kick's contact) held for 3 frames
NF = 141 + STOP[1]
AIX = 610                             # MY AI on the desk, left of the laptop
def story(f): return f if f < STOP[0] else (STOP[0] if f < STOP[0] + STOP[1] else f - STOP[1])
def noise(f, k): return random.Random(f * 7919 + k).uniform(-1, 1)

def counter(g):
    if g < 40: return int(lerp(0, 3, g / 40))
    if g < 90: return int(lerp(3, 24, (g - 40) / 50))
    if g < 100: return 24
    return 31

def robot_palm(c, x, y, ang, s):
    """MY AI's open hand, white like the robot (not a human hand)."""
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    for i in range(4): rr(c, 12, -24 + i * 13, 42 - abs(i - 1.5) * 6, 13, 6); fs(c, WHITE, 5)
    rr(c, -18, -26, 40, 52, 16); fs(c, WHITE, 6)
    c.restore()

def ai_arm(c, sh, tgt, hand='palm', L=150):
    """A robot arm, two segments a little longer than its standard ones, a grey elbow joint."""
    e, h = P.ik(sh, tgt, L, L, P.DOWN)
    limb(c, [sh, e, h], 24 * AS, WHITE)
    ell(c, e[0], e[1], 13, 13); fs(c, GREY, 5)
    a = math.atan2(h[1] - e[1], h[0] - e[0])
    if hand == 'palm': robot_palm(c, h[0], h[1], a, AS * .9)
    else: ell(c, h[0], h[1], 20, 20); fs(c, WHITE, 6)
    return h

def myai_typing(c, f, x, gy, left='down', rot=0.0):
    tap = 10 * math.sin(f * 2.3)
    right = P.ai_pose(1, P.ai_local(x, gy, AS, (KEY[0] + tap, KEY[1] - abs(tap))), P.DOWN)
    A.myai(c, x, gy, AS, eye='happy', look=(18, 0), rot=rot, arms=(left, right), bob=3 * math.sin(f * .6))

def camera(c, f):
    sh = 0
    for hit, amp in ((10, 12), (STOP[0], 26), (118 + STOP[1], 16)):
        if hit <= f < hit + 8: sh = amp * (1 - (f - hit) / 8)
    k = 1 + .06 * io((f - 94) / 6) * (1 - io((f - 108) / 8))
    ax, ay = 400, 1150
    c.translate(ax + noise(f, 1) * sh, ay + noise(f, 2) * sh); c.scale(k, k); c.translate(-ax, -ay)

def frame(f):
    S = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(S)
    g = story(f)
    c.save(); camera(c, f)
    P.room(c); P.desk(c); P.laptop(c, counter(g))
    wob = .12 * math.sin(f * 1.7) * (1 if (8 <= g < 24 or 100 <= g < 120) else 0)
    c.save(); c.translate(560, DESK_Y); c.rotate(wob); P.mug(c, 0, 0, 1.1); c.restore()

    if g < 40:                                                             # 1 THE SHOVE
        t = g
        cx = 270 if t < 10 else lerp(270, 120, oe((t - 10) / 18))
        tilt = -.12 * cl((t - 9) / 3) * (1 - cl((t - 30) / 8))
        P.chair(c, cx, P.SEAT_Y, rot=tilt, spin=max(0, t - 10) * .4)
        shL, shR, head = P.hoody_seated(c, cx, P.SEAT_Y, 'smug' if t < 9 else 'shock', rot=tilt)
        P.hoody_arm(c, shL, (shL[0] - 110, shL[1] - 90), HS, pref=P.LEFT, hand='palm')
        P.hoody_arm(c, shR, (shR[0] + 40, shR[1] - 190), HS, pref=P.RIGHT, hand='palm')
        if t >= 10: P.lines(c, [(cx + 300, P.SEAT_Y - 150), (cx + 150, P.SEAT_Y - 150)], 3)
        if t < 22:                                                        # standing at the desk's edge: the push, held
            x = lerp(P.STAND_X, 560, oe(t / 8)); gy = FLOOR
            chest = ((shL[0] + shR[0]) / 2 + 70, (shL[1] + shR[1]) / 2 + 90)
            reach = chest if t < 18 else (x - 110, 1240)
            A.myai(c, x, gy, AS, eye='happy', look=(18, 0), rot=-.1, arms=(None, 'down'))
            ai_arm(c, (x - 72 * AS, gy - 280 * AS + 112 * AS), reach, L=110)
            if 8 <= t < 14:
                for i in range(3): c.arc(reach[0] - 10, reach[1], 46 + i * 24, 2.3, 4.0); c.set_source_rgba(*INK, .55); c.set_line_width(6); c.stroke()
        else:                                                             # the hop up onto the desk
            u = io((t - 22) / 12); x = lerp(560, AIX, u); gy = lerp(FLOOR, DESK_Y, u) - math.sin(math.pi * u) * 120
            myai_typing(c, f, x, gy)

    elif g < 90:                                                           # 2 THE FOREHEAD
        t = g - 40
        P.chair(c, 120, P.SEAT_Y, spin=4)
        if t < 8:                                                         # up out of the chair
            shL, shR, head = P.hoody_seated(c, 120 + 10 * t, P.SEAT_Y - 30 * t / 8, 'strain')
        else:
            hx_ = lerp(130, 175, oe((t - 8) / 8))
            shL, shR, head = P.hoody_standing(c, hx_, FLOOR, 'strain', bow=.12, gaze=16, side=1)
            for q, sh, ph in ((1, shR, 0), (-1, shL, math.pi)):           # punches at the air, alternating, always short
                k = .5 + .5 * math.sin(t * .8 + ph)
                tgt = (sh[0] + lerp(40, 210 if q > 0 else 230, k), sh[1] + (-40 if q > 0 else 30))
                P.hoody_arm(c, sh, tgt, HS, pref=P.DOWN, hand='grip', ang=0)
                if k > .8:
                    for i in range(2): c.move_to(tgt[0] + 30 + i * 14, tgt[1] - 30); c.line_to(tgt[0] + 30 + i * 14, tgt[1] + 30)
                    c.set_source_rgba(*INK, .5); c.set_line_width(5); c.stroke()
        myai_typing(c, f, AIX, DESK_Y, left=None)
        sh = (AIX - 72 * AS, DESK_Y - 280 * AS + 112 * AS)
        fh = (head[0] + 95, head[1] - 60)
        ext = oe((t - 12) / 5)
        ai_arm(c, sh, (lerp(sh[0] - 40, fh[0], ext), lerp(sh[1] + 60, fh[1], ext)))

    else:                                                                  # 3 THE KICK
        t = g - 90
        P.chair(c, 120, P.SEAT_Y, spin=4)
        foot_hip = (AIX - 34 * AS, DESK_Y - 75 * AS)
        if t < 10:                                                        # it lets go; he stumbles forward, arms out
            u = io(t / 10); hx_ = lerp(175, 290, u)
            shL, shR, head = P.hoody_standing(c, hx_, FLOOR, 'shock', bow=lerp(.12, .45, u), gaze=16, side=1)
            P.hoody_arm(c, shL, (shL[0] + 160, shL[1] + 40), HS, pref=P.DOWN, hand='palm')
            P.hoody_arm(c, shR, (shR[0] + 160, shR[1] - 40), HS, pref=P.DOWN, hand='palm')
            kn = (foot_hip[0] - 40 * u, foot_hip[1] - 60 * u); ft = (foot_hip[0] - 30 * u, foot_hip[1] + 40 - 30 * u)   # knee comes up
        elif t < 28:                                                      # contact, then the flight back to the door
            u = cl((t - 10) / 18)
            px = lerp(285, 215, u); py = lerp(1250, FLOOR - 10, u * u) - math.sin(math.pi * u) * 120; a = lerp(-.25, -.8, u)
            c.save(); c.translate(px, py); c.rotate(a)
            P.hoody_seated(c, 0, 0, 'shock', legs=((150, -40), (250, -150)))
            c.restore()
            P.lines(c, [(px + 280, py - 140), (px + 140, py - 120)], 3)
            kn, ft = (foot_hip[0] - 110, foot_hip[1] - 10), (440, 1090)     # the leg out, held
        else:                                                             # against the door, dazed
            u = io((t - 28) / 6)
            sq = 1 + .08 * math.sin(math.pi * cl((t - 28) / 4))
            c.save(); c.translate(215, FLOOR - 10); c.scale(sq, 1 / sq); c.rotate(-.12)
            P.hoody_seated(c, 0, 0, 'dizzy', legs=((170, -10), (300, 0)))
            c.restore()
            for i in range(3):
                a = f * .3 + i * 2.1; ell(c, 230 + 75 * math.cos(a), FLOOR - 540 + 18 * math.sin(a), 11, 11); c.set_source_rgb(*YEL); c.fill()
            kn = (lerp(foot_hip[0] - 110, foot_hip[0] - 20, u), lerp(foot_hip[1] - 10, foot_hip[1] + 40, u))
            ft = (lerp(440, foot_hip[0] - 10, u), lerp(1090, DESK_Y - 4, u))
        limb(c, [foot_hip, kn, ft], 34 * AS, WHITE)
        c.save(); c.translate(*ft); c.rotate(math.atan2(ft[1] - kn[1], ft[0] - kn[0])); rr(c, -26, -24, 64, 48, 20); fs(c, WHITE, 7); c.restore()
        if 10 <= t < 15:
            for i in range(3): c.arc(ft[0] - 10, ft[1], 40 + i * 22, 2.2, 4.1); c.set_source_rgba(*INK, .6); c.set_line_width(7); c.stroke()
        thumb = (AIX - 150, DESK_Y - 330)
        pl = P.ai_pose(-1, P.ai_local(AIX, DESK_Y, AS, thumb), P.UP) if t >= 10 else 'down'
        old = A.limb
        A.limb = lambda c_, pts, *a: None if pts == [(-34, 205), (-34, 280)] else old(c_, pts, *a)
        try: myai_typing(c, f, AIX, DESK_Y, left=pl)
        finally: A.limb = old
        if t >= 10:
            tx, ty = A.hand_at(AIX, DESK_Y, AS, -1, pl); rr(c, tx - 12, ty - 66, 26, 50, 12); fs(c, WHITE, 7)
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
        fs_ = list(range(0, NF, 6)); cols = 9; tw, th = 240, 427
        out = cairo.ImageSurface(cairo.FORMAT_RGB24, cols * tw, ((len(fs_) + cols - 1) // cols) * th); c = cairo.Context(out)
        c.set_source_rgb(1, 1, 1); c.paint()
        for i, f in enumerate(fs_):
            c.save(); c.translate((i % cols) * tw, (i // cols) * th); c.scale(tw / W, th / H); c.set_source_surface(frame(f)); c.paint(); c.restore()
            txt(c, f'{f / 30:.1f}s', (i % cols) * tw + 40, (i // cols) * th + 20, 22, INK, lw=0)
        out.write_to_png('fight_sheet.png'); print('fight_sheet.png')
