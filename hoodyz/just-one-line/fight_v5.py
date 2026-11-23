"""Just One Line: the fight, motion test v4 (mute test 10, "visi a"; v2 and v3 kept beside it).
  1 THE SHOVE    (0.0-1.3)  its palm on his chest; he and the chair roll a short way left; it hops onto the desk
  2 THE SCREEN   (1.3-1.9)  a close-up of the laptop: FILES CHANGED 2 -> 3, so the number means something on a phone
  3 THE FOREHEAD (1.9-3.6)  he gets up out of the chair (it stays behind him) and charges, angry, teeth set, feet sliding;
                            its arm, straight out, holds him by the forehead; his fists fall short; the counter climbs
  4 THE KICK     (3.6-5.4)  it lets go; he falls back into his chair; its leg comes off the desk and kicks the chair
                            (hit-stop, shake, push-in); the chair and he shoot to the door; he spills out, dazed
Hoody never goes behind MY AI; MY AI never looks at him and never stops typing.
Usage: python3 fight.py sheet | video"""
import os, sys, math, random, subprocess, cairo
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import kp as P
from kp import K, A, INK, WHITE, NAVY, SKIN, GREY, YEL, rr, fs, ell, limb, txt, hx, lerp, W, H, FLOOR, HS, AS, KEY, LAP, DESK_Y
cl = lambda t: max(0.0, min(1.0, t)); oe = lambda t: 1 - (1 - cl(t)) ** 3; io = lambda t: (lambda u: u * u * (3 - 2 * u))(cl(t))
K.FACES['dizzy'] = ('spiral', (None, None), 'wobble')
K.FACES['fury'] = ('open', ('angry', 'angry'), 'frown')          # angry, nothing that could read as a grin
T_CU, T_FH, T_KICK, T_END = 40, 58, 108, 162                      # story frames: the shove, the close-up, the forehead, the kick
CONTACT = T_KICK + 14
STOP = (CONTACT, 3)                                                # hit-stop on the kick's contact
NF = T_END + STOP[1]
AIX = 610                                                          # MY AI on the desk, left of the laptop
CHX = 230                                                          # the chair after the shove: behind him from here on
def story(f): return f if f < STOP[0] else (STOP[0] if f < STOP[0] + STOP[1] else f - STOP[1])
def noise(f, k): return random.Random(f * 7919 + k).uniform(-1, 1)

def counter(g):
    if g < T_CU: return int(lerp(0, 2, g / T_CU))
    if g < T_FH: return 2 if g < T_CU + 8 else 3
    if g < T_KICK: return int(lerp(3, 24, (g - T_FH) / (T_KICK - T_FH)))
    return 24 if g < CONTACT else 31

def robot_palm(c, x, y, ang, s):
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    for i in range(4): rr(c, 12, -24 + i * 13, 42 - abs(i - 1.5) * 6, 13, 6); fs(c, WHITE, 5)
    rr(c, -18, -26, 40, 52, 16); fs(c, WHITE, 6)
    c.restore()

def ai_limb(c, sh, tgt, w, L, end='palm', pref=P.DOWN):
    """A robot arm or leg, two segments, a grey joint; end: palm | foot | ball."""
    e, h = P.ik(sh, tgt, L, L, pref)
    limb(c, [sh, e, h], w, WHITE)
    ell(c, e[0], e[1], 13, 13); fs(c, GREY, 5)
    a = math.atan2(h[1] - e[1], h[0] - e[0])
    if end == 'palm': robot_palm(c, h[0], h[1], a, AS * .9)
    elif end == 'foot': c.save(); c.translate(*h); c.rotate(a); rr(c, -26, -26, 70, 52, 20); fs(c, WHITE, 7); c.restore()
    else: ell(c, h[0], h[1], 20, 20); fs(c, WHITE, 6)
    return h

def myai_typing(c, f, x, gy, left='down', legs=True):
    tap = 10 * math.sin(f * 2.3)
    right = P.ai_pose(1, P.ai_local(x, gy, AS, (KEY[0] + tap, KEY[1] - abs(tap))), P.DOWN)
    old = A.limb
    if not legs: A.limb = lambda c_, pts, *a: None if pts == [(-34, 205), (-34, 280)] else old(c_, pts, *a)
    try: A.myai(c, x, gy, AS, eye='happy', look=(18, 0), arms=(left, right), bob=3 * math.sin(f * .6))
    finally: A.limb = old

def camera(c, f):
    sh = 0
    for hit, amp in ((10, 10), (STOP[0], 16), (CONTACT + 16 + STOP[1], 8)):
        if hit <= f < hit + 8: sh = amp * (1 - (f - hit) / 8)
    k = 1 + .07 * io((f - CONTACT + 5) / 5) * (1 - io((f - CONTACT - 10) / 8))
    ax, ay = 400, 1250
    c.translate(ax + noise(f, 1) * sh, ay + noise(f, 2) * sh); c.scale(k, k); c.translate(-ax, -ay)

def closeup(c, g):
    """The laptop, full frame: what the number is."""
    t = g - T_CU
    P.room(c)
    c.save(); c.translate(540, 1000); s = 3.2 + .1 * io(t / 18); c.scale(s, s); c.translate(-(LAP['x0'] + LAP['x1']) / 2, -(LAP['y0'] + LAP['y1']) / 2)
    P.laptop(c, counter(g))
    c.restore()
    if T_CU + 8 <= g < T_CU + 14:                                       # the tick: a pop on the number
        for i in range(3): c.arc(540, 1080, 230 + i * 30, 0, 2 * math.pi); c.set_source_rgba(*YEL, .5 - .12 * i); c.set_line_width(8); c.stroke()

def frame(f):
    S = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(S)
    g = story(f)
    if T_CU <= g < T_FH:
        closeup(c, g); P.topbar(c); return S
    c.save(); camera(c, f)
    P.room(c); P.desk(c); P.laptop(c, counter(g))
    wob = .12 * math.sin(f * 1.7) * (1 if (8 <= g < 24 or CONTACT <= g < CONTACT + 20) else 0)
    c.save(); c.translate(560, DESK_Y); c.rotate(wob); P.mug(c, 0, 0, 1.1); c.restore()

    if g < T_CU:                                                           # 1 THE SHOVE
        t = g
        cx = 270 if t < 10 else lerp(270, CHX, oe((t - 10) / 14))
        tilt = -.12 * cl((t - 9) / 3) * (1 - cl((t - 26) / 8))
        P.chair(c, cx, P.SEAT_Y, rot=tilt, spin=max(0, t - 10) * .3)
        shL, shR, head = P.hoody_seated(c, cx, P.SEAT_Y, 'smug' if t < 9 else 'shock', rot=tilt)
        P.hoody_arm(c, shL, (shL[0] - 110, shL[1] - 90), HS, pref=P.LEFT, hand='palm')
        P.hoody_arm(c, shR, (shR[0] + 40, shR[1] - 190), HS, pref=P.RIGHT, hand='palm')
        if 10 <= t < 26: P.lines(c, [(cx + 300, P.SEAT_Y - 150), (cx + 150, P.SEAT_Y - 150)], 3)
        if t < 22:
            x = lerp(P.STAND_X, 560, oe(t / 8)); gy = FLOOR
            chest = ((shL[0] + shR[0]) / 2 + 70, (shL[1] + shR[1]) / 2 + 90)
            reach = chest if t < 18 else (x - 110, 1240)
            A.myai(c, x, gy, AS, eye='happy', look=(18, 0), rot=-.18 if 6 <= t < 18 else -.08, arms=(None, 'down'))
            ai_limb(c, (x - 72 * AS, gy - 280 * AS + 112 * AS), reach, 24 * AS, 140)
            if 8 <= t < 14:
                for i in range(3): c.arc(reach[0] - 10, reach[1], 46 + i * 24, 2.3, 4.0); c.set_source_rgba(*INK, .55); c.set_line_width(6); c.stroke()
        else:
            u = io((t - 22) / 12); x = lerp(560, AIX, u); gy = lerp(FLOOR, DESK_Y, u) - math.sin(math.pi * u) * 120
            myai_typing(c, f, x, gy)

    elif g < T_KICK:                                                       # 3 THE FOREHEAD
        t = g - T_FH
        P.chair(c, CHX, P.SEAT_Y)
        hx_ = lerp(CHX, CHX + 30, oe(t / 8))
        shL, shR, head = P.hoody_standing(c, hx_, FLOOR, 'fury', bow=.18, gaze=16, side=1)
        for q, sh, ph in ((1, shR, 0), (-1, shL, math.pi)):               # jabs at the air, alternating, always short
            k = .5 + .5 * math.sin(t * .8 + ph)
            tgt = (sh[0] + lerp(30, 150, k), sh[1] + (10 if q > 0 else 60))
            P.hoody_arm(c, sh, tgt, HS, pref=P.DOWN, hand='grip', ang=0)
        for i in range(3):                                                # feet sliding: dust behind his heels
            ell(c, hx_ - 80 - i * 26 + 6 * math.sin(f + i), FLOOR - 14 - i * 6, 14 - i * 3, 8 - i * 2); c.set_source_rgba(.6, .55, .5, .7); c.fill()
        for dx, dy in ((70, -60), (100, -20)):
            ell(c, head[0] + dx, head[1] + dy, 9, 14); fs(c, hx('58c7ff'), 4)
        myai_typing(c, f, AIX, DESK_Y, left=None)
        sh = (AIX - 72 * AS, DESK_Y - 280 * AS + 112 * AS)
        fh = (head[0] + 95, head[1] - 60)
        ext = oe((t - 4) / 5)
        ai_limb(c, sh, (lerp(sh[0] - 40, fh[0], ext), lerp(sh[1] + 60, fh[1], ext)), 24 * AS, 150)

    else:                                                                  # 4 THE KICK
        t = g - T_KICK
        hip = (AIX - 34 * AS, DESK_Y - 75 * AS)
        # the chair: still; at contact it shoots to the door with him in it; he spills out against the door
        c0 = CONTACT - T_KICK
        if t < c0: chx, chr_ = CHX, 0
        else: u = cl((t - c0) / 12); chx, chr_ = lerp(CHX, 190, 1 - (1 - u) ** 2), -.25 * math.sin(math.pi * u)
        P.chair(c, chx, P.SEAT_Y, rot=chr_, spin=max(0, t - c0) * .35)
        if t < 8:                                                         # the palm on his forehead pushes him back down into his chair
            u = io(t / 8)
            shL, shR, head = P.hoody_standing(c, lerp(CHX + 30, CHX, u), FLOOR - 0 * u, 'shock', bow=.35 * u, gaze=10, side=-1)
            P.hoody_arm(c, shL, (shL[0] - 120, shL[1] - 40), HS, pref=P.LEFT, hand='palm')
            P.hoody_arm(c, shR, (shR[0] + 100, shR[1] - 80), HS, pref=P.RIGHT, hand='palm')
            sh = (AIX - 72 * AS, DESK_Y - 280 * AS + 112 * AS)
            ai_limb(c, sh, (head[0] + 95, head[1] - 60), 24 * AS, 170)
            for i in range(2): c.arc(head[0] + 95, head[1] - 60, 40 + i * 22, -.6, 1.0); c.set_source_rgba(*INK, .5); c.set_line_width(6); c.stroke()
        elif t < c0 + 12:                                                 # sitting; then shot to the door, tipping back
            sq = 1 + .07 * math.sin(math.pi * cl((t - 8) / 3))
            tilt = 0 if t < c0 else -.14 * cl((t - c0) / 6)
            c.save(); c.translate(chx, P.SEAT_Y); c.scale(1, 1 / sq); c.translate(-chx, -P.SEAT_Y)
            shL, shR, head = P.hoody_seated(c, chx, P.SEAT_Y, 'shock', rot=tilt)
            c.restore()
            P.hoody_arm(c, shL, (shL[0] - 110, shL[1] - 80), HS, pref=P.LEFT, hand='palm')
            P.hoody_arm(c, shR, (shR[0] + 50, shR[1] - 180), HS, pref=P.RIGHT, hand='palm')
            if t >= c0: P.lines(c, [(chx + 330, P.SEAT_Y - 160), (chx + 170, P.SEAT_Y - 160)], 4)
        else:                                                             # spilled out against the door, dazed
            sq = 1 + .08 * math.sin(math.pi * cl((t - c0 - 12) / 4))
            c.save(); c.translate(215, FLOOR - 10); c.scale(sq, 1 / sq); c.rotate(-.12)
            P.hoody_seated(c, 0, 0, 'dizzy', legs=((170, -10), (300, 0)))
            c.restore()
            for i in range(3):
                a = f * .3 + i * 2.1; ell(c, 230 + 75 * math.cos(a), FLOOR - 540 + 18 * math.sin(a), 11, 11); c.set_source_rgb(*YEL); c.fill()
        # its leg: rest, knee up, the kick to the chair's seat, held, back
        seat = (CHX + 100, P.SEAT_Y - 4)
        if t < c0 - 5: ft = (hip[0] - 10, hip[1] + 90)
        elif t < c0: u = io((t - c0 + 5) / 5); ft = (lerp(hip[0] - 10, hip[0] + 20, u), lerp(hip[1] + 90, hip[1] + 20, u))   # wind-up
        elif t < c0 + 10: ft = (seat[0] if t < c0 + 2 else lerp(seat[0], seat[0] - 40, (t - c0 - 2) / 8), seat[1])
        else: u = io((t - c0 - 10) / 8); ft = (lerp(seat[0] - 40, hip[0] - 10, u), lerp(seat[1], hip[1] + 90, u))
        ai_limb(c, hip, ft, 44 * AS, 180, end='foot', pref=P.UP)
        if c0 <= t < c0 + 6:                                              # the impact, on the seat's edge
            for i in range(4):
                a = i * math.pi / 2 + .4; c.move_to(seat[0] + 30 * math.cos(a), seat[1] + 30 * math.sin(a)); c.line_to(seat[0] + 80 * math.cos(a), seat[1] + 80 * math.sin(a))
            c.set_source_rgb(*YEL); c.set_line_width(10); c.stroke()
            for i in range(3): c.arc(seat[0], seat[1], 50 + i * 22, 2.0, 4.3); c.set_source_rgba(*INK, .6); c.set_line_width(7); c.stroke()
        thumb = (AIX - 150, DESK_Y - 330)
        pl = P.ai_pose(-1, P.ai_local(AIX, DESK_Y, AS, thumb), P.UP) if t >= c0 else (None if t < 8 else 'down')
        myai_typing(c, f, AIX, DESK_Y, left=pl, legs=False)
        if t >= c0:
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
        fs_ = list(range(0, NF, 6)); cols = 10; tw, th = 216, 384
        out = cairo.ImageSurface(cairo.FORMAT_RGB24, cols * tw, ((len(fs_) + cols - 1) // cols) * th); c = cairo.Context(out)
        c.set_source_rgb(1, 1, 1); c.paint()
        for i, f in enumerate(fs_):
            c.save(); c.translate((i % cols) * tw, (i // cols) * th); c.scale(tw / W, th / H); c.set_source_surface(frame(f)); c.paint(); c.restore()
            txt(c, f'{f / 30:.1f}s', (i % cols) * tw + 40, (i // cols) * th + 20, 22, INK, lw=0)
        out.write_to_png('fight_sheet.png'); print('fight_sheet.png')
