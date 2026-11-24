"""Remove the Bottleneck: rough 3 - the ideal loop (Tomas, 24 Nov, all a). One set (B), one camera. 434 frames, 14.47 s.
  A   0- 45  frame 0: Hoody points at the PIPELINE board (top right), coffee in his other hand: "Remove the bottleneck."
             POP POP POP behind him: MY AI is four; he backs off
  B  45-105  the list: AUTOMATE, DELEGATE, OPTIMIZE ticked; BOTTLENECK circled red; four heads turn to him
  C 105-180  the tailors (a copy holds his mug for him); the crate is pushed in behind him; "New suit?"
  D 180-255  the waist tape is yanked: he goes over backwards into the crate; his mug is tossed in after him; the lid slams
  E 255-300  four copies lift the crate; a sticker is slapped over its plate: BOTTLENECK REMOVED.
  F 300-434  HARV signs for it and leaves; his thumb comes up out of the hand slot: "Faster!" - so they sprint, out of the
             LEFT of the frame. The office is empty: the board goes green, the tasks flow. Then the board flashes red: they
             come in from the RIGHT, the sticker stamped RETURN TO SENDER, skid to the crate's own place and drop it. The
             bump throws the lid open, the sticker off and Hoody out: he lands on his feet in frame 0's pose, mug in hand;
             three copies pop away, the fourth trots to its place. The last frame IS frame 0 (no flash): he says it again.
Usage: python3 film.py sheet [step] | final | seam"""
import os, sys, math, json, random, subprocess, cairo
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..'))
import office as P, setb as B, tailors as T, kp as KP
from office import K, A, INK, WHITE, NAVY, YEL, RED, GREY, rr, fs, ell, limb, txt, hx, lerp, W, H, FLOOR, HS, AS
cl = lambda t: max(0.0, min(1.0, t)); oe = lambda t: 1 - (1 - cl(t)) ** 3; io = lambda t: (lambda u: u * u * (3 - 2 * u))(cl(t))
SHOTS = [('A', 45), ('B', 60), ('C', 75), ('D', 75), ('E', 45), ('F', 134)]
START = {}; _t = 0
for n, d in SHOTS: START[n] = _t; _t += d
NF = _t
BOARD = (606, 385, 360, 270)        # top right, the same place in every shot; clear of the carried crate and the bubbles
CX = 420                            # the crate's place: wholly in frame, its plate inside the safe zone
H0X, AI0X = 400, 170                # frame 0: where Hoody and MY AI stand
CL = 330                            # where the crate is lifted from (C-E)
SKIN = hx('ffd9b8')
BOXES = []
NOBUBBLE = False                    # the seam check draws frame 0 without its bubble (it appears as he starts to speak)
def noise(f, k): return random.Random(f * 7919 + k).uniform(-1, 1)
def pop(c, x, y, k, r=150):
    if k <= 0 or k >= 1: return
    for a in range(8):
        a_ = a * .785; c.move_to(x + r * (.6 + .4 * k) * math.cos(a_), y + r * (.6 + .4 * k) * math.sin(a_)); c.line_to(x + r * (1 + .5 * k) * math.cos(a_), y + r * (1 + .5 * k) * math.sin(a_))
    c.set_source_rgba(*YEL, 1 - k); c.set_line_width(10); c.stroke()
def bubble(c, lines, tip, cx, cy, size=66):
    if NOBUBBLE: return
    P.bubble(c, lines, size, tip, cx, cy)
    c.save(); c.select_font_face('Lilita One'); c.set_font_size(size); w = max(c.text_extents(l).width for l in lines) + 100; c.restore()
    h = len(lines) * size * 1.12 + 56; BOXES.append((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2))
def word(c, s, x, y, size=100, rot=-.1):
    c.save(); c.select_font_face('Lilita One'); c.set_font_size(size); w = c.text_extents(s).width; c.restore()
    txt(c, s, x, y, size, YEL, lw=12, st=INK, rot=rot); BOXES.append((x - w / 2 - 10, y - size * .6, x + w / 2 + 10, y + size * .6))
def hoody(c, x, expr, side=-1, bow=0.0, gaze=0, bob=0.0, rot=0.0):
    c.save(); c.translate(x, FLOOR); c.rotate(rot); c.translate(-x, -FLOOR - bob)
    r = P.hoody_standing(c, x, FLOOR, expr, bow=bow, gaze=gaze, side=side); c.restore()
    ca, sa = math.cos(rot), math.sin(rot)
    tr = lambda p: (x + (p[0] - x) * ca - (p[1] - FLOOR) * sa, FLOOR + (p[0] - x) * sa + (p[1] - FLOOR) * ca - bob)
    return [tr(p) for p in r]
def crate0(c, x0=CX, **k): return B.crate(c, x0, FLOOR, slot=True, slot_x=50, **{'lid': 1, **k})
def mug_arm(c, shL):                                                     # coffee in his screen-left hand, in every shot he holds it
    P.hoody_arm(c, shL, (shL[0] - 40, shL[1] + 180), HS, pref=P.LEFT, hand='grip'); P.mug(c, shL[0] - 46, shL[1] + 250, 1.1)

# ---------------- frame 0's pose: drawn by ONE function, at the start (A) and at the end (F) ----------------
def pose0(c, j=0.0, k=0.0):
    """j: his finger jabbing at the board; k: both of them bobbing as he talks. Both are 0 on frame 0 and on the last frames."""
    A.myai(c, AI0X, FLOOR, AS, eye='happy', look=(10 + 6 * k, -14), bob=10 * k)
    shL, shR, head = hoody(c, H0X, 'smug', side=1, bob=9 * k)
    P.hoody_arm(c, shR, (shR[0] + 150 + j, shR[1] - 260 - j), HS, pref=P.RIGHT, hand='point', ang=-.84)      # at the board
    mug_arm(c, shL)
    return head

# ---------------- A ----------------
POPS = [(15, 60, 0), (22, 285, 0), (29, 180, -40)]
def a_end():                                                             # where the four stand when A ends: (x, dy)
    return [(60, 0), (285, 0), (180, -40), (AI0X - 12, 0)]
def shot_A(c, t):
    B.room(c); B.board(c, *BOARD); crate0(c)
    if t < 15: head = pose0(c, 34 * abs(math.sin(t * .55)), abs(math.sin(t * .42)))      # talking: jabbing at the board, both bobbing
    else:
        for i, (at, x, dy) in enumerate(POPS[::-1]):                     # the back one first
            if t >= at:
                k = cl((t - at) / 4); A.myai(c, x, FLOOR + dy, AS * (1.25 - .25 * oe(k)), eye='happy', look=(14, -8), arms=('wave' if i == 1 else 'down', 'down'))
        A.myai(c, AI0X - 12, FLOOR, AS, eye='happy', look=(14, -8))
        for at, x, dy in POPS: pop(c, x, FLOOR + dy - 300, (t - at) / 6)
        back = io((t - 28) / 16)                                         # "Huh?!": he turns and backs off to the right
        hop = 8 * io((t - 15) / 3) * (1 - io((t - 20) / 6)) + (7 * abs(math.sin((t - 28) * .8)) if 28 <= t < 44 else 0)
        shL, shR, head = hoody(c, lerp(H0X, 700, back), 'shock', side=-1, gaze=-12, bob=hop)
        u = io((t - 15) / 5); P.hoody_arm(c, shR, (lerp(shR[0] + 150, shR[0] + 90, u), lerp(shR[1] - 260, shR[1] + 130, u)), HS, pref=P.RIGHT, hand='palm')
        mug_arm(c, shL)
    if 15 <= t < 40: word(c, 'POP!', 230, 780 - 6 * math.sin(t), 90 + 10 * (1 - cl((t - 15) / 4)), -.12)
    if t < 42: bubble(c, ['REMOVE THE', 'BOTTLENECK.'], (head[0] - 30, head[1] - 205), 330, 482)

# ---------------- B ----------------
def shot_B(c, t):
    B.room(c); B.board(c, *BOARD); crate0(c)
    turn = io((t - 41) / 5)                                               # all four heads to him
    sip = io((t - 15) / 4) * (1 - io((t - 30) / 4))
    shL, shR, head = hoody(c, 700, 'smug' if t < 41 else 'calm', side=-1, gaze=-10 if t < 41 else 10)
    P.hoody_arm(c, shR, (shR[0] + 60, shR[1] + 180), HS, pref=P.RIGHT, hand='grip')
    mh = (lerp(shL[0] - 40, head[0] - 70, sip), lerp(shL[1] + 180, head[1] + 110, sip))
    P.hoody_arm(c, shL, mh, HS, pref=P.LEFT, hand='grip'); P.mug(c, mh[0] - 6, mh[1] + 70, 1.1)
    g = io(t / 8)                                                         # the four shuffle from where A left them
    xs = [(lerp(a[0], b, g), lerp(a[1], 0, g)) for a, b in zip(a_end(), (110, 300, 470, 560))]
    lift = 200 * (1 - oe(t / 8))
    jig = 9 * abs(math.sin(t * .42)) * (1 - turn)                         # eager little bounces, until they all turn to him
    for i in (0, 1):
        A.myai(c, xs[i][0], FLOOR + xs[i][1], AS, eye='happy', look=(lerp(0, 18, turn), lerp(-18, -4, turn)), arms=(('up' if i == 0 else 'hold2'), ('hold2' if i == 0 else 'up')), bob=jig)
    sx, sy, sw, sh = 66, 760 + lift - jig, 330, 380
    rr(c, sx, sy, sw, sh, 10); fs(c, WHITE, 7)
    for i, (wd, done_at) in enumerate((('AUTOMATE', 10), ('DELEGATE', 17), ('OPTIMIZE', 24), ('BOTTLENECK', None))):
        y = sy + 60 + i * 82; rr(c, sx + 24, y - 24, 46, 46, 6); fs(c, WHITE, 5)
        if done_at is not None and t >= done_at:
            u = cl((t - done_at) / 3); c.move_to(sx + 32, y); c.line_to(sx + 32 + 12 * min(1, u * 2), y + 14 * min(1, u * 2))
            if u > .5: c.line_to(sx + 44 + 22 * (u - .5) * 2, y + 14 - 32 * (u - .5) * 2)
            c.set_source_rgb(*hx('2bbf5a')); c.set_line_width(8); c.stroke()
        txt(c, wd, sx + 80, y + 2, 34 if done_at else 40, INK if done_at else RED, lw=0, align='l')
        if done_at is None and t >= 31:
            c.save(); c.translate(sx + 180, y); c.scale(1.6, .55); c.arc(0, 0, 100, 0, 2 * math.pi * io((t - 31) / 8)); c.restore(); c.set_source_rgb(*RED); c.set_line_width(6); c.stroke()
    BOXES.append((sx, sy, sx + sw, sy + sh))
    for i in (2, 3):
        A.myai(c, xs[i][0], FLOOR + xs[i][1], AS, eye='open' if t >= 41 else 'happy', look=(lerp(-16, 18, turn), lerp(-14, -2, turn)), bob=9 * abs(math.sin(t * .42 + 1 + i)) * (1 - turn), rot=.05 * turn * math.sin(t * .6))

# ---------------- C and D: the tailors, the yank, the crate ----------------
HX0 = 520
def tailors(c, t, d=-1):
    """C (t 0-75) and the start of D (d 0-14): the tailors, animated; the crate is pushed in behind him."""
    B.room(c); B.board(c, *BOARD)
    crate0(c, lerp(CX, CL, oe(t / 12)) if d < 0 else CL)
    yank = io(d / 5) if d >= 0 else 0.0
    xd, gd = 920, FLOOR + 10                                             # the spec sheet (a crate to his size), glasses on
    A.myai(c, xd, gd, AS, eye='happy', look=(-8, 10), arms=('hold', 'hold2'))
    T.glasses(c, xd, gd); T.tape_neck(c, xd, gd); T.notebook(c, xd - 10, gd - 330 + 4 * math.sin(t * 1.3), 1.15)
    x1, g1 = 175, FLOOR; x2, g2 = 175, FLOOR - (280 + 95) * AS
    ankle = (HX0 - 40, FLOOR - 40); crotch = (HX0 - 8, FLOOR - 360)
    pa = P.ai_pose(1, P.ai_local(x1, g1, AS, (ankle[0] - 60, ankle[1] - 20)), P.DOWN)
    A.myai(c, x1, g1, AS, eye='happy', look=(16, 4), arms=(P.ai_pose(-1, P.ai_local(x1, g1, AS, (x1 - 60, g2 - 20)), P.UP), pa)); T.tape_neck(c, x1, g1)
    rx = x2 + 175; rtop = lerp(FLOOR - 200, 0, oe((t - 4) / 10))
    pb = P.ai_pose(1, P.ai_local(x2, g2, AS, (rx - 6, g2 - 330)), P.UP)
    A.myai(c, x2, g2, AS, eye='happy', look=(16, -14), rot=.04 + .03 * math.sin(t * .4), arms=('down', pb)); T.tape_neck(c, x2, g2)
    mh = A.hand_at(x2, g2, AS, -1, 'down'); P.mug(c, max(mh[0], 44), mh[1] + 62, 1.1)                      # "let me hold that for you"
    rot = -1.0 * oe((d - 4) / 10) if d >= 0 else 0.0                     # over backwards
    shL, shR, head = hoody(c, HX0, 'smug' if d < 4 else 'shock', side=1, bob=4 * math.sin(t * .3), rot=rot)
    T.ruler(c, rx, max(head[1] - 250, rtop) if d < 0 else head[1] - 250, FLOOR - 10)
    hb = A.hand_at(x2, g2, AS, 1, pb); ell(c, hb[0], hb[1], 22, 22); fs(c, WHITE, 6)
    leg = cl((t - 15) / 10) if d < 0 else 1
    if leg > 0 and rot == 0: T.tape_line(c, [crotch, (lerp(crotch[0], ankle[0], leg), lerp(crotch[1], ankle[1], leg))], 14)
    ha = A.hand_at(x1, g1, AS, 1, pa); ell(c, ha[0], ha[1], 22, 22); fs(c, WHITE, 6)
    P.hoody_arm(c, shL, (shL[0] - 280, shL[1] + 10 + (60 * yank)), HS, pref=P.UP, hand='palm', ang=math.pi)
    P.hoody_arm(c, shR, (shR[0] + 200, shR[1] - 230 + 200 * yank), HS, pref=P.DOWN, hand='palm', ang=-.8)
    x3, g3 = 760, FLOOR; wy = FLOOR - 300 * HS - 40
    lean = .06 + .04 * math.sin(t * .5) + .35 * yank
    end = (HX0 + 175 + 120 * yank, wy + 30)
    if rot == 0:
        T.tape_line(c, [(HX0 - 150, wy - 4), (HX0 - 60, wy + 40), (HX0 + 60, wy + 44), (HX0 + 148, wy + 10)], 16)
        c.move_to(HX0 + 148, wy + 10); c.line_to(*end); c.set_source_rgb(*T.TAPE); c.set_line_width(16); c.stroke()
    pc = P.ai_pose(-1, P.ai_local(x3 + 40 * yank, g3, AS, end), P.DOWN)
    pr = P.ai_pose(1, P.ai_local(x3, g3, AS, (x3 + 110, g3 - 300)), P.DOWN)
    A.myai(c, x3 + 40 * yank, g3, AS, eye='happy', look=(-18, -8), rot=lean, arms=(pc, pr)); T.tape_neck(c, x3 + 40 * yank, g3); T.pincushion(c, *A.hand_at(x3 + 40 * yank, g3, AS, 1, pr))
    if d >= 4:
        for i in range(3): c.arc(HX0 - 60, FLOOR - 260, 300 + i * 26, 3.5, 4.5); c.set_source_rgba(*INK, .45); c.set_line_width(6); c.stroke()
    if d < 0 and 15 <= t < 62: bubble(c, ['NEW SUIT?'], (head[0] - 60, head[1] - 190), 420, 470, 74)
    if 0 <= d < 4: word(c, 'YANK!', 790, 900, 100, .1)

def legs_in(c, d):
    """D from 14: legs up out of the crate; a copy on the rim pushes his knees in; his mug is tossed in after him; the lid slams."""
    B.room(c); B.board(c, *BOARD)
    x0 = CL; top = FLOOR - 330
    lid = 1 - io((d - 60) / 4)
    sink = io((d - 40) / 18)
    rock = .012 * math.sin(d * 1.1) * (1 - sink)                           # he kicks: the crate rocks
    crate0(c, x0, lid=max(lid, 0), rot=rock)
    c.save(); c.rectangle(0, 0, W, top - 4); c.clip()                     # what shows above the rim
    if sink < 1:
        for col, dx, ph in ((P.JEANS_FAR, 50, 1.2), (P.JEANS, 0, 0)):
            kick = 30 * math.sin(d * .8 + ph) * (1 - sink)
            hip = (x0 + 330 + dx, top + 60 + 420 * sink); kn = (x0 + 300 + dx * 1.4, top - 250 + 420 * sink); ft = (x0 + 390 + dx * 2 + kick, top - 470 + 420 * sink)
            limb(c, [hip, kn, ft], 70, col); c.save(); c.translate(*ft); c.rotate(-.6); rr(c, -30, -26, 100, 48, 18); fs(c, INK, 0); c.restore()
    c.restore()
    kn = (x0 + 330, top - 230 + 420 * sink)
    xr, gr = x0 + 150, top + 8
    pa = P.ai_pose(1, P.ai_local(xr, gr, AS, (kn[0] - 30, max(kn[1] + 20, top - 260))), P.DOWN)
    A.myai(c, 150, FLOOR, AS, eye='happy', look=(16, -10), arms=('hold2', 'up'), bob=8 * abs(math.sin(d * .45)))
    if d < 64: A.myai(c, xr, gr, AS, eye='happy', look=(18, 4), rot=.2 + .07 * math.sin(d * .8), bob=6 * abs(math.sin(d * .8)), arms=(P.ai_pose(-1, P.ai_local(xr, gr, AS, (xr - 40, gr - 300)), P.UP), pa))
    else: A.myai(c, xr - 40, gr, AS, eye='happy', look=(10, 0), arms=('up', 'up'), bob=6 * math.sin(d))   # standing on the shut lid
    hand = A.hand_at(150, FLOOR, AS, 1, 'up'); mu = cl((d - 46) / 10)     # his mug: held up for him, then lobbed in after him
    if mu < 1:
        mx, my = lerp(hand[0] + 10, x0 + 250, mu), lerp(hand[1] - 10, top + 60, mu) - 260 * math.sin(math.pi * mu)
        c.save()
        if mu > .7: c.rectangle(0, 0, W, top - 4); c.clip()
        c.translate(mx, my); c.rotate(5 * mu); P.mug(c, 0, 32, 1.1); c.restore()
    if 60 <= d < 66:
        for i in range(6): ell(c, x0 + 60 + i * 110, top - 10, 40, 16); c.set_source_rgba(.85, .8, .7, .8); c.fill()
        word(c, 'SLAM!', 780, 1000, 100, -.08)

# ---------------- E and F: the lift, the sticker, the carry, the sprint round the world, the drop ----------------
HT = FLOOR - 280 * AS - 95 * AS - 10                                     # the crate's underside, on their heads
DX = (80, 240, 400, 560)
def carriers(c, x0, walk=None, look=(-16, -4), rot=0.0, gone=(), bob=0.0):
    for i, dx in enumerate(DX):
        x = x0 + dx
        if i not in gone and -200 < x < W + 200:
            A.myai(c, x, FLOOR, AS, eye='happy' if i % 2 == 0 else 'open', look=look, rot=rot, bob=bob, walk=walk + i * 1.6 if walk is not None else None, arms=('up', 'up'))
def thumb_up(c, sl, k):
    """His fist out of the hand slot, thumb up (a fist on its side, the thumb off the top of it: never one lone finger)."""
    if k <= 0 or not sl: return
    c.save(); c.rectangle(0, 0, W, sl[1]); c.clip(); c.translate(sl[0], sl[1] + 60 * (1 - k) - 6)
    rr(c, -24, -40, 48, 50, 12); fs(c, NAVY, 6)
    c.save(); c.rotate(-.12); rr(c, -52, -158, 34, 84, 16); fs(c, SKIN, 7); c.restore()
    rr(c, -40, -100, 88, 70, 24); fs(c, SKIN, 7)
    for i in range(3): c.move_to(48, -86 + i * 18); c.line_to(24, -86 + i * 18)
    c.set_source_rgb(*INK); c.set_line_width(5); c.stroke(); c.restore()
def shot_E(c, t):
    B.room(c); B.board(c, *BOARD)
    up = io((t - 4) / 14)
    y = lerp(FLOOR, HT, up) - (6 * math.sin(t * .9) if up >= 1 else 0)    # marching on the spot under it
    if up > 0: carriers(c, CL, None)
    else: carriers(c, CL - 400, None, look=(16, -4))                      # (walking in to lift it)
    B.crate(c, CL, y, lid=0, stamp=io((t - 26) / 4) if t >= 26 else 0, rot=-.02 * up, slot=True, slot_x=50)        # the sticker, slapped on
    if 26 <= t < 32: c.save(); c.translate(CL + 350, y - 185); c.set_source_rgba(1, 1, 1, .5 * (1 - (t - 26) / 6)); ell(c, 0, 0, 300, 140); c.fill(); c.restore()

T_GO, T_OUT, T_BACK, T_STOP, T_DROP, T_HIT, T_LAND, T_SET = 56, 72, 88, 102, 110, 114, 124, 130
POPS_F = [(107, 3), (108, 2), (109, 1)]                                   # (frame, which carrier) pops away
def shot_F(c, t):
    sh = 14 * (1 - (t - T_HIT) / 6) if T_HIT <= t < T_HIT + 6 else 0      # the drop shakes the room (0 again long before the end)
    c.save(); c.translate(noise(t, 1) * sh, noise(t, 2) * sh)
    B.room(c)
    flow = io((t - T_OUT) / 3) * (1 - io((t - T_BACK + 1) / 2))           # green while they are out of the frame
    alarm = (1 - cl((t - T_BACK) / 12)) if t >= T_BACK else 0             # red as they come back
    B.board(c, *BOARD, flow=flow, f=t, alarm=alarm)
    if t >= T_SET:                                                        # ---- frame 0 again, exactly
        crate0(c); pose0(c, 0.0); c.restore(); return
    # where the crate is
    if t < T_GO: x0 = CL
    elif t < T_OUT: x0 = CL - 1100 * ((t - T_GO) / (T_OUT - T_GO)) ** 2   # accelerating out to the left
    elif t < T_BACK: x0 = None                                            # round the world
    else: x0 = lerp(1160, CX, oe((t - T_BACK) / (T_STOP - T_BACK)))       # in from the right, skidding to its place
    fall = cl((t - T_DROP) / (T_HIT - T_DROP)) ** 2
    y = lerp(HT, FLOOR, fall) if t >= T_DROP else HT - (5 * math.sin(t * .9) if t < T_GO - 4 else 0)
    if x0 is not None:
        if t < T_GO - 4: carriers(c, x0, t * .45)                         # marching on the spot
        elif t < T_GO: carriers(c, x0, None, rot=.14 * io((t - T_GO + 4) / 3), bob=-10)        # the wind-up
        elif t < T_OUT: carriers(c, x0, t * 1.3, rot=-.26)                # sprint
        elif t < T_STOP: carriers(c, x0, t * 1.3 if t < T_STOP - 6 else None, rot=lerp(-.26, .2, oe((t - T_BACK) / (T_STOP - T_BACK))))    # braking
        elif t < T_DROP:
            carriers(c, x0, None, gone=[i for at, i in POPS_F if t >= at], bob=5 * math.sin(t * 1.4))
        if T_GO <= t < T_OUT:                                             # speed lines behind them
            for i in range(5): yy = HT - 260 + i * 130; c.move_to(x0 + 700 + 40 * i, yy); c.line_to(x0 + 900 + 90 * i, yy); c.set_source_rgba(1, 1, 1, .45); c.set_line_width(7); c.stroke()
        if T_BACK + 4 <= t < T_STOP + 2:                                  # skid dust ahead of their feet
            for i in range(5): ell(c, x0 - 20 - i * 46 + 10 * math.sin(t + i), FLOOR - 14 - i * 5, 30 - i * 4, 14 - i * 2); c.set_source_rgba(.85, .8, .7, .7); c.fill()
        # the crate; the hit throws its lid open and its sticker off
        hit = t >= T_HIT
        sl = B.crate(c, x0, y, lid=oe((t - T_HIT) / 4) if hit else 0, stamp=0 if hit else 1.0, rts=1.0 if t >= T_BACK else 0, slot=True, slot_x=50,
                     rot=(.02 if t < T_GO else (-.05 if t < T_OUT else lerp(-.05, .04, oe((t - T_BACK) / 14)))) * (1 - fall) if not hit else 0)
        thumb_up(c, sl, io((t - 22) / 5) * (1 - io((t - T_DROP + 3) / 3)))
        if 32 <= t < T_GO and sl: bubble(c, ['FASTER!'], (sl[0] - 6, sl[1] - 150), 330, 470, 70)
        for at, i in POPS_F: pop(c, x0 + DX[i], FLOOR - 300, (t - at) / 6)
        if T_DROP <= t:                                                   # the one that is left trots to its place
            u = io((t - T_DROP) / (T_LAND - T_DROP)); ax = lerp(CX + DX[0], AI0X, u)
            if u < 1: A.myai(c, ax, FLOOR, AS, eye='happy', look=(lerp(-16, 10, u), lerp(-4, -14, u)), walk=t * 1.2)
            else: A.myai(c, AI0X, FLOOR, AS, eye='happy', look=(10, -14))
        if hit:
            if t < T_LAND:                                                # thrown out: one somersault, the mug never leaves his hand
                u = (t - T_HIT) / (T_LAND - T_HIT); x = lerp(CX + 260, H0X, u); hgt = 4 * 420 * u * (1 - u)
                c.save()
                if u < .35: c.rectangle(-50, -50, W + 100, FLOOR - 330 - 4 + 50); c.clip()      # still inside: only what is above the rim
                c.translate(x, FLOOR - hgt - 470); c.rotate(-2 * math.pi * io(u)); c.translate(-x, -(FLOOR - 470))
                shL, shR, head = P.hoody_standing(c, x, FLOOR, 'shock', bow=0, gaze=0, side=1)
                P.hoody_arm(c, shR, (shR[0] + 130, shR[1] - 200), HS, pref=P.RIGHT, hand='palm'); mug_arm(c, shL)
                c.restore()
            else:                                                         # lands on his feet; the finger comes up
                u = io((t - T_LAND) / (T_SET - T_LAND))
                shL, shR, head = hoody(c, H0X, 'shock' if t < T_LAND + 2 else 'smug', side=1, bow=.3 * (1 - u))
                P.hoody_arm(c, shR, (shR[0] + lerp(130, 150, u), shR[1] - lerp(200, 260, u)), HS, pref=P.RIGHT, hand='palm' if u < .5 else 'point', ang=-.84)
                mug_arm(c, shL)
                if t < T_LAND + 4:
                    for i in range(4): ell(c, H0X - 90 + i * 60, FLOOR - 10, 30, 12); c.set_source_rgba(.85, .8, .7, .7 * (1 - (t - T_LAND) / 4)); c.fill()
            u = (t - T_HIT) / 10                                          # the sticker, blown off, out of the top right
            if u < 1.3: B.sticker(c, CX + 350 + 520 * u, FLOOR - 185 - 900 * u + 300 * u * u, 1.0, rot=-.06 + 5 * u, rts=1.0)
            if t < T_HIT + 5:
                for i in range(7): ell(c, CX + 20 + i * 100, FLOOR - 8, 44, 16); c.set_source_rgba(.85, .8, .7, .8 * (1 - (t - T_HIT) / 5)); c.fill()
    # HARV: walks in, signs for it, leaves before the sprint
    hv = lerp(-200, 165, io(t / 10)) if t < 40 else lerp(165, -220, io((t - 40) / 14))
    if hv > -190 and t < 56:
        KP.harv(c, hv, FLOOR + 10, mouth='fond' if 14 <= t < 40 else 'flat')
        if 16 <= t < 38: c.move_to(hv + 120, FLOOR - 230); c.curve_to(hv + 140, FLOOR - 250 + 8 * math.sin(t * 2), hv + 150, FLOOR - 220, hv + 170, FLOOR - 240); c.set_source_rgb(*NAVY); c.set_line_width(4); c.stroke()
    c.restore()

def draw(fr, bar=True):
    BOXES.clear()
    S = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(S)
    n, t = next((n, fr - START[n]) for n, d in SHOTS if fr < START[n] + d)
    if n == 'A': shot_A(c, t)
    elif n == 'B': shot_B(c, t)
    elif n == 'C': tailors(c, t)
    elif n == 'D': tailors(c, 75, t) if t < 14 else legs_in(c, t)
    elif n == 'E': shot_E(c, t)
    else: shot_F(c, t)
    if bar: KP.bar(c)
    return S

def seam():
    """The loop gate: the last frame against frame 0 drawn without its bubble (which appears as he starts to speak).
    They are built from the same calls, so the difference must be exactly zero."""
    global NOBUBBLE
    import numpy as np
    g = lambda f: np.frombuffer(draw(f).get_data(), np.uint8).astype(float)
    a = g(NF - 1); NOBUBBLE = True
    try: b = g(0)
    finally: NOBUBBLE = False
    d = np.abs(a - b); return float(d.mean()), float(d.max())

if __name__ == '__main__':
    os.chdir(HERE); mode = (sys.argv[1:] or ['sheet'])[0]
    if mode == 'seam':
        mean, mx = seam(); print(f'seam: last frame vs frame 0 (without its bubble): mean diff {mean:.3f}/255, max {mx:.0f}'); sys.exit(0 if mx == 0 else 1)
    if mode == 'final':
        p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}', '-r', '30', '-i', '-',
                              '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', '-pix_fmt', 'yuv420p',
                              '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', 'video.mp4'], stdin=subprocess.PIPE)
        bad = []
        for f in range(NF):
            p.stdin.write(bytes(draw(f).get_data())); bad += [(f, b) for b in BOXES if b[0] < 60 or b[2] > 960 or b[1] < 375 or b[3] > 1600]
        p.stdin.close(); p.wait(); print('video.mp4', NF, 'outside', len(bad), bad[:4])
        if bad: sys.exit(1)
    else:
        step = int(sys.argv[2]) if len(sys.argv) > 2 else 6
        f0 = int(sys.argv[3]) if len(sys.argv) > 3 else 0
        fs_ = list(range(f0, NF, step)); cols = 12; tw, th = 180, 320
        out = cairo.ImageSurface(cairo.FORMAT_RGB24, cols * tw, ((len(fs_) + cols - 1) // cols) * th); c = cairo.Context(out)
        for i, f in enumerate(fs_):
            c.save(); c.translate((i % cols) * tw, (i // cols) * th); c.scale(tw / W, th / H); c.set_source_surface(draw(f)); c.paint(); c.restore()
            txt(c, f'{f}', (i % cols) * tw + 26, (i // cols) * th + 16, 18, WHITE, lw=0)
        out.write_to_png('rough_sheet.png'); print('rough_sheet.png', NF / 30)
