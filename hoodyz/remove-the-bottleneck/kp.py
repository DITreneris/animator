"""Remove the Bottleneck: key poses on set B. k0 frame 0 | k1 the split (0.5 s) | k2 the list | k3 the tailors |
k4 into the crate | k5 THE CARRY (iconic). Usage: python3 kp.py -> kp_<name>.png + key_poses.png"""
import os, sys, math, cairo
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import office as P, setb as B, tailors as T
from office import K, A, INK, WHITE, NAVY, YEL, RED, GREY, rr, fs, ell, limb, txt, hx, lerp, W, H, FLOOR, HS, AS
LABEL = 'HIS TEAM'                                                      # Tomas, 23 Nov
def bar(c): P.C.topbar(c, LABEL)
BOARD = (110, 540); CRATE_X = 600
def harv(c, x, gy, s=AS, mouth='flat', clip=True):
    """HARV as the series draws him (Says Here, Make It Better): MY AI's body and size, his gold-rimmed shades.
    (Just One Line gave him long legs; this is the series' size.) A clipboard: he signs for the crate."""
    for q in (-1, 1): limb(c, [(x + q * 34 * s, gy - 75 * s), (x + q * 34 * s, gy)], 34 * s, WHITE)
    if clip:
        bx, by = x + 95 * s, gy - 150 * s
        limb(c, [(x + 72 * s, gy - 168 * s), (x + 120 * s, gy - 120 * s), (bx, by)], 24 * s, WHITE)
        c.save(); c.translate(bx + 10, by - 40); c.rotate(.15); rr(c, -46, -60, 92, 120, 8); fs(c, hx('b98d52'), 5); rr(c, -36, -46, 72, 96, 4); fs(c, WHITE, 3)
        for i in range(3): c.move_to(-26, -26 + i * 22); c.line_to(22, -26 + i * 22); c.set_source_rgb(*GREY); c.set_line_width(3); c.stroke()
        c.move_to(-24, 34); c.curve_to(-10, 20, 0, 44, 22, 26); c.set_source_rgb(*NAVY); c.set_line_width(4); c.stroke(); c.restore()   # his signature
    P.C.harv(c, x, gy - 280 * s, s, shade=True, mouth=mouth)

def k0(c):   # frame 0: Hoody, coffee in hand, points at the board: "Remove the bottleneck." MY AI at his side. The crate waits.
    B.room(c); B.board(c, *BOARD); B.crate(c, CRATE_X, FLOOR, lid=1)
    x = 470; shL, shR, head = P.hoody_standing(c, x, FLOOR, 'smug', side=-1)
    P.hoody_arm(c, shL, (shL[0] - 150, shL[1] - 260), HS, pref=P.LEFT, hand='point', ang=-2.3)
    P.hoody_arm(c, shR, (shR[0] + 40, shR[1] + 180), HS, pref=P.RIGHT, hand='grip'); P.mug(c, shR[0] + 46, shR[1] + 250, 1.1)
    A.myai(c, 220, FLOOR, AS, eye='happy', look=(10, -14))
    P.bubble(c, ['REMOVE THE', 'BOTTLENECK.'], 66, (head[0] + 40, head[1] - 205), 650, 470)
    bar(c)

def k1(c):   # 0.5 s: POP POP POP - MY AI splits into four (DELEGATE); the new ones pop out sideways in a little cloud
    B.room(c); B.board(c, *BOARD); B.crate(c, CRATE_X, FLOOR, lid=1)
    for i, (x, dy, r) in enumerate(((290, -60, .05), (110, -40, -.08), (200, 0, 0), (380, 10, .1))):
        A.myai(c, x, FLOOR + dy, AS, eye='happy', look=(14, -6), rot=r, arms=('wave' if i % 2 else 'down', 'down'))
        if i in (1, 3):
            cx_, cy_ = x, FLOOR + dy - 300
            for a_ in range(8): c.move_to(cx_ + 150 * math.cos(a_ * .785), cy_ + 150 * math.sin(a_ * .785)); c.line_to(cx_ + 210 * math.cos(a_ * .785), cy_ + 210 * math.sin(a_ * .785))
            c.set_source_rgb(*YEL); c.set_line_width(10); c.stroke()
    shL, shR, head = P.hoody_standing(c, 640, FLOOR, 'shock', side=-1)
    P.hoody_arm(c, shL, (shL[0] - 120, shL[1] + 120), HS, pref=P.LEFT, hand='palm')
    P.hoody_arm(c, shR, (shR[0] + 40, shR[1] + 180), HS, pref=P.RIGHT, hand='grip'); P.mug(c, shR[0] + 46, shR[1] + 250, 1.1)
    txt(c, 'POP!', 200, 820, 90, YEL, lw=12, st=INK, rot=-.12)
    bar(c)

def k2(c):   # the list: two copies hold up one big sheet; three boxes ticked, the fourth empty; all four heads turn to him
    B.room(c); B.board(c, *BOARD); B.crate(c, CRATE_X, FLOOR, lid=1)
    shL, shR, head = P.hoody_standing(c, 700, FLOOR, 'smug', side=-1)
    P.hoody_arm(c, shL, (shL[0] - 60, shL[1] + 180), HS, pref=P.LEFT, hand='grip'); P.hoody_arm(c, shR, (shR[0] + 40, shR[1] + 180), HS, pref=P.RIGHT, hand='grip')
    P.mug(c, shR[0] + 46, shR[1] + 250, 1.1)
    xs = (110, 300)
    for x in xs: A.myai(c, x, FLOOR, AS, eye='happy', look=(18, -4), arms=(('up' if x == 110 else 'hold2'), ('hold2' if x == 110 else 'up')))
    sx, sy, sw, sh = 50, 760, 330, 380
    rr(c, sx, sy, sw, sh, 10); fs(c, WHITE, 7)
    for i, (t, done) in enumerate((('AUTOMATE', 1), ('DELEGATE', 1), ('OPTIMIZE', 1), ('BOTTLENECK', 0))):
        y = sy + 60 + i * 82; rr(c, sx + 24, y - 24, 46, 46, 6); fs(c, WHITE, 5)
        if done: c.move_to(sx + 32, y); c.line_to(sx + 44, y + 14); c.line_to(sx + 66, y - 18); c.set_source_rgb(*hx('2bbf5a')); c.set_line_width(8); c.stroke()
        txt(c, t, sx + 80, y + 2, 34 if done else 40, INK if done else RED, lw=0, align='l')
        if not done:                                                     # the one left: circled red, an arrow to him
            c.save(); c.translate(sx + 180, y); c.scale(1.6, .55); c.arc(0, 0, 100, 0, 2 * math.pi); c.restore(); c.set_source_rgb(*RED); c.set_line_width(6); c.stroke()
    for x in (470, 560):
        A.myai(c, x, FLOOR, AS * .96, eye='open', look=(18, -2))
    bar(c)

def k3(c):   # the tailors (tailors.py), on set B
    T.P.room, old = (lambda c_: (B.room(c_), B.board(c_, 600, 520, 420, 280), B.crate(c_, 300, FLOOR, L=470, h=300, lid=1))), P.room
    old_desk, old_lap, old_mug = P.desk, P.laptop, P.mug
    P.desk = lambda c_: None; P.laptop = lambda c_, *a, **k: None
    try:
        T.P.topbar = bar; T.kp(c)
    finally: P.room, P.desk, P.laptop = old, old_desk, old_lap

def k4(c):   # into the crate: tipped in head first - only his legs and sneakers stick up out of it; two copies push
    # the last of him in, one holds the lid, one keeps the list (the last box ticked)
    B.room(c); B.board(c, *BOARD)
    x0 = 330; top = FLOOR - 330
    B.crate(c, x0, FLOOR, L=640, lid=1)
    c.save(); c.rectangle(0, 0, W, top - 4); c.clip()                    # his legs, up out of the opening (in front of the lid)
    for col, dx in ((P.JEANS_FAR, 50), (P.JEANS, 0)):
        hip = (x0 + 330 + dx, top + 60); kn = (x0 + 300 + dx * 1.4, top - 250); ft = (x0 + 390 + dx * 2, top - 470)
        limb(c, [hip, kn, ft], 70, col); c.save(); c.translate(*ft); c.rotate(-.6); rr(c, -30, -26, 100, 48, 18); fs(c, INK, 0); c.restore()
    c.restore()
    for i in range(3): c.arc(x0 + 330, top - 120, 220 + i * 26, 3.4, 4.4); c.set_source_rgba(*INK, .45); c.set_line_width(6); c.stroke()   # his arc, backwards
    kn = (x0 + 330, top - 230)
    xr, gr = x0 + 150, top + 8                                            # a copy on the rim, left of his legs (never in front of them)
    pa = P.ai_pose(1, P.ai_local(xr, gr, AS, (kn[0] - 30, kn[1] + 20)), P.DOWN)
    A.myai(c, 150, FLOOR, AS, eye='happy', look=(16, -10), arms=('hold2', 'up'))
    A.myai(c, xr, gr, AS, eye='happy', look=(18, 4), rot=.2, arms=(P.ai_pose(-1, P.ai_local(xr, gr, AS, (xr - 40, gr - 300)), P.UP), pa))
    c.move_to(30, FLOOR - 560); c.curve_to(200, FLOOR - 700, 300, FLOOR - 520, x0 + 300, top + 20); c.set_source_rgb(*T.TAPE); c.set_line_width(14); c.stroke()   # the tape that pulled him over
    bar(c)

def k5(c):   # THE CARRY (iconic): four copies march the shut crate out on their heads, BOTTLENECK REMOVED. on its side,
    # his thumb up out of the hand slot. "Faster!" (muffled)
    B.room(c); B.board(c, *BOARD)
    xs = (400, 570, 740, 910); top = FLOOR - 280 * AS - 95 * AS - 10
    for i, x in enumerate(xs):
        ph = i * 1.6
        A.myai(c, x, FLOOR, AS, eye='happy' if i % 2 == 0 else 'open', look=(16, -4), walk=ph, arms=('up', 'up'))
    sl = B.crate(c, 300, top, L=760, h=300, lid=0, stamp=1.0, slot=True, rot=-.025)
    for x in xs:                                                         # hands flat on its underside: it weighs something
        for q in (-1, 1): ell(c, x + q * 40, top - 8 + (x - 300) * -.025 * .0, 22, 18); fs(c, WHITE, 6)
    tx, ty = sl[0], sl[1]
    c.save(); c.translate(tx, ty - 6)                                    # his fist out of the slot, thumb up (big: the iconic detail)
    rr(c, -24, -40, 48, 50, 12); fs(c, NAVY, 6)                          # sleeve cuff
    c.save(); c.rotate(-.12); rr(c, -52, -158, 34, 84, 16); fs(c, hx('ffd9b8'), 7); c.restore()   # the thumb, on the side of the fist
    rr(c, -40, -100, 88, 70, 24); fs(c, hx('ffd9b8'), 7)                                  # the fist, knuckles to the right
    for i in range(3): c.move_to(48, -86 + i * 18); c.line_to(24, -86 + i * 18)
    c.set_source_rgb(*INK); c.set_line_width(5); c.stroke(); c.restore()
    for a in (-2.4, -1.6, -.8): c.move_to(tx + 3 + 110 * math.cos(a), ty - 150 + 110 * math.sin(a)); c.line_to(tx + 3 + 150 * math.cos(a), ty - 150 + 150 * math.sin(a))
    c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    harv(c, 165, FLOOR + 10, mouth='fond')                               # the witness, in front: HARV signs for the crate
    P.bubble(c, ['FASTER!'], 70, (tx - 10, ty - 24), 640, 470)          # the tail into the slot: him, inside
    bar(c)

KP = dict(k0=k0, k1=k1, k2=k2, k3=k3, k4=k4, k5=k5)
NAMES = dict(k0='frame 0', k1='the split', k2='the list', k3='the tailors', k4='into the crate', k5='THE CARRY')
if __name__ == '__main__':
    keys = sys.argv[1:] or list(KP); surfs = {}
    for k in keys:
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); KP[k](cairo.Context(s)); surfs[k] = s; s.write_to_png(os.path.join(HERE, f'kp_{k}.png'))
    n = len(keys); sw, sh = int(W * .4), int(H * .4)
    out = cairo.ImageSurface(cairo.FORMAT_ARGB32, sw * n + 10 * (n + 1), sh + 80); c = cairo.Context(out); c.set_source_rgb(1, 1, 1); c.paint()
    for i, k in enumerate(keys):
        x = 10 + i * (sw + 10); c.save(); c.translate(x, 70); c.scale(.4, .4); c.set_source_surface(surfs[k]); c.paint(); c.restore()
        txt(c, f'{k}  {NAMES[k]}', x + sw / 2, 36, 30, NAVY, lw=0)
    out.write_to_png(os.path.join(HERE, 'key_poses.png')); print('ok', *keys)
