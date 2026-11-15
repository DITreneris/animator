"""MY AI v2 - Hoody's companion robot, with the arm set Perfect Date needs.
Body, head and legs are the robot from whos-a-good-boy/v3/v.py (same proportions and colours).
v2: arms are a fixed two-segment rig (upper arm 68, forearm 68, from shoulders at +-72, 112), posed by joint angles,
so arm length can't drift between shots; CONFUSED and BLANK eyes; head tilt; a WAIT pose; a three-quarter turn.
Writes myai_sheet.png."""
import os, sys, math, cairo
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..', '..')
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
import kit as K
from kit import INK, WHITE, NAVY, RED, rr, fs, ell, limb, txt, hx
import eva as E

EYE = hx('33bfff'); VISOR = hx('0b1020'); EARS = (.62, .65, .72); CHEST = (.82, .86, .93); PINK = hx('ff5c8a')
SHOULDER = (72, 112); L1 = L2 = 68; ARM_W = 24; HAND_R = 21
NECK = (0, 85)                       # the head tilts about this point
LIMITS = dict(shoulder=(0, 165), elbow=(-140, 140), tilt=(-15, 15))
# pose = (shoulder angle, elbow bend) in degrees. Shoulder: 0 = arm straight down, 90 = straight out to the side,
# 180 = straight up. Elbow: bend relative to the upper arm; + lifts the forearm outward/up, - folds it back across the body.
POSES = {
    'down':  (10, 4),     'hold':  (34, 8),     'hold2': (100, 10),
    'offer': (78, 22),    'give':  (52, 58),    'wave':  (100, 78),
    'wait':  (68, 74),    'up':    (150, 18),   'hip':   (42, -104),
    'chest': (34, -128),
}

def arm_points(q, pose):
    a1, a2 = POSES[pose] if isinstance(pose, str) else pose
    a1 = max(LIMITS['shoulder'][0], min(LIMITS['shoulder'][1], a1)); a2 = max(LIMITS['elbow'][0], min(LIMITS['elbow'][1], a2))
    t1 = math.radians(a1); t2 = math.radians(a1 + a2)
    sx, sy = q * SHOULDER[0], SHOULDER[1]
    ex, ey = sx + q * L1 * math.sin(t1), sy + L1 * math.cos(t1)
    hx_, hy = ex + q * L2 * math.sin(t2), ey + L2 * math.cos(t2)
    return (sx, sy), (ex, ey), (hx_, hy), t2

def hand_at(x, gy, s, q, pose):
    """Screen position of a hand, for lining up props and other characters (e.g. Eva's hand in his)."""
    _, _, (hx_, hy), _ = arm_points(q, pose)
    return x + hx_ * s, gy - 280 * s + hy * s

def eyes(c, mode, look=(0, 0)):
    gx, gy = look
    for q in (-1, 1):
        m = mode
        if mode == 'wink': m = 'happy' if q == 1 else 'open'
        if mode == 'confused': m = 'wide' if q == -1 else 'small'
        x, y = q * 36 + gx, -8 + gy
        if m == 'open':  ell(c, x, y, 18, 24); c.set_source_rgb(*EYE); c.fill()
        elif m == 'wide': ell(c, x, y, 23, 31); c.set_source_rgb(*EYE); c.fill(); ell(c, x - 6, y - 10, 6, 6); c.set_source_rgb(1, 1, 1); c.fill()
        elif m == 'small': ell(c, x, y + 6, 11, 11); c.set_source_rgb(*EYE); c.fill()
        elif m == 'blank': ell(c, x, y + 4, 7, 7); c.set_source_rgb(*EYE); c.fill()
        elif m == 'focus': ell(c, x, y + 4, 21, 8); c.set_source_rgb(*EYE); c.fill()
        elif m == 'happy':
            c.arc(x, y + 14, 19, math.pi + .35, 2 * math.pi - .35); c.set_source_rgb(*EYE); c.set_line_width(11); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
        elif m == 'heart':
            c.save(); c.translate(x, y + 2); c.scale(.95, .95)
            c.move_to(0, 18); c.curve_to(-30, -2, -18, -30, 0, -12); c.curve_to(18, -30, 30, -2, 0, 18); c.close_path()
            c.set_source_rgb(*PINK); c.fill(); c.restore()

def hand(c, x, y, t2, q, open_=False):
    """Round mitt; the thumb nub sits off the forearm's line, so it turns with the wrist."""
    if open_: ell(c, x, y, HAND_R + 3, HAND_R + 7)
    else: ell(c, x, y, HAND_R, HAND_R)
    fs(c, WHITE, 6)
    tx, ty = x + q * math.cos(t2) * 18 - q * math.sin(t2) * 6, y - math.sin(t2) * 18 * q * q - math.cos(t2) * 6
    ell(c, tx, ty, 9, 9); fs(c, WHITE, 5)

def arm(c, q, pose, prop=None):
    s_, e_, h_, t2 = arm_points(q, pose)
    limb(c, [s_, e_, h_], ARM_W + 16, INK); limb(c, [s_, e_, h_], ARM_W, WHITE)
    if prop: prop(c, h_[0], h_[1], q)
    hand(c, *h_, t2, q, open_=(pose == 'wait'))
    return h_

def myai(c, x, gy, s, eye='happy', look=(0, 0), arms=('down', 'down'), props=(None, None), rot=0, walk=None, bob=0, tilt=0, turn=0, talk=0.0):
    """Standing on ground y. arms = (screen-left pose, screen-right pose). rot tips the whole robot about its feet (bow: -.35).
    tilt: head tilt in degrees (limit +-15). turn: -1..1, a three-quarter turn (visor and antenna slide, far ear hides)."""
    tilt = max(LIMITS['tilt'][0], min(LIMITS['tilt'][1], tilt))
    c.save(); c.translate(x, gy); c.rotate(rot); c.translate(0, -280 * s - bob - (abs(math.sin(walk)) * 8 * s if walk is not None else 0)); c.scale(s, s); c.set_line_cap(cairo.LINE_CAP_ROUND)
    if walk is None:
        limb(c, [(-34, 205), (-34, 280)], 34, WHITE); limb(c, [(34, 205), (34, 280)], 34, WHITE)
    else:                                                             # a step: the swinging leg lifts, the knee bends
        for q, ph in ((-1, walk), (1, walk + math.pi)):
            fx = q * 34 + math.sin(ph) * 30; lift = max(0, math.cos(ph)) * 22
            limb(c, [(q * 34, 205), (q * 34 + math.sin(ph) * 12 + 8, 244 - lift * .5), (fx, 280 - lift)], 34, WHITE)
    rr(c, -72, 85, 144, 135, 44); fs(c, WHITE)
    ell(c, turn * 22, 150, 30 - abs(turn) * 6, 30); fs(c, CHEST, 5)
    for q, p, pr in zip((-1, 1), arms, props): arm(c, q, p, pr)
    c.save(); c.translate(*NECK); c.rotate(math.radians(tilt)); c.translate(-NECK[0], -NECK[1])
    ax = turn * 40
    c.move_to(ax, -90); c.line_to(ax, -132); c.set_source_rgb(*INK); c.set_line_width(9); c.stroke()
    if talk > .05:                                                    # speaking: the antenna glows with the voice
        ell(c, ax, -140, 17 + 22 * talk, 17 + 22 * talk); c.set_source_rgba(*EYE, .35 * talk); c.fill()
    ell(c, ax, -140, 17, 17); fs(c, EYE, 7)
    for q in (-1, 1):
        if turn * q < -.5: continue                                  # far ear hidden in a three-quarter view
        ell(c, q * 110 - turn * 10, 0, 22 - abs(turn) * 4 * (q == (1 if turn > 0 else -1)), 38); fs(c, EARS, 8)
    rr(c, -108, -95, 216, 180, 78); fs(c, WHITE)
    vx = turn * 40
    rr(c, -82 + vx, -54, 164 - abs(turn) * 30, 92, 40); fs(c, VISOR, 6)
    if talk > .05:                                                    # ...and the eyes squash on each syllable
        c.save(); c.translate(vx, -8); c.scale(1 + .08 * talk, 1 - .38 * talk); c.translate(-vx, 8)
        eyes(c, eye, (look[0] + turn * 34, look[1])); c.restore()
    else: eyes(c, eye, (look[0] + turn * 34, look[1]))
    c.restore(); c.restore()

# ---------------- props ----------------
def rose(c, x, y, q=1):
    """A decorative long-stemmed rose: layered petals, two leaves, a satin bow on the stem, a glint."""
    GRN, GRN_D, R1, R2, R3 = hx('2f9e4f'), hx('1f7a3a'), hx('b3122c'), hx('e0243e'), hx('ff5a6e')
    limb(c, [(x, y + 20), (x + q * 8, y - 60), (x + q * 4, y - 150)], 9, GRN)
    for side, yy, rot in ((1, -50, .5), (-1, -95, -.6)):                # leaves
        c.save(); c.translate(x + q * 6 + side * 6, y + yy); c.rotate(rot * side); ell(c, side * 26, 0, 28, 12); fs(c, GRN, 4)
        c.move_to(0, 0); c.line_to(side * 46, 0); c.set_source_rgb(*GRN_D); c.set_line_width(3); c.stroke(); c.restore()
    c.save(); c.translate(x + q * 6, y - 20)                           # the satin bow
    for side in (-1, 1):
        c.move_to(0, 0); c.curve_to(side * 30, -26, side * 46, 6, 0, 0); fs(c, hx('ff8fc7'), 4)
        c.move_to(0, 2); c.line_to(side * 18, 40); c.line_to(side * 8, 42); c.close_path(); fs(c, hx('ff8fc7'), 3)
    ell(c, 0, 0, 8, 7); fs(c, hx('ff8fc7'), 3); c.restore()
    c.save(); c.translate(x + q * 4, y - 182); c.scale(1.5, 1.5)      # the bloom: sepals, outer, middle, inner, spiral heart
    for i in range(3): a = -2.3 + i * .8; c.move_to(0, 18); c.line_to(22 * math.cos(a) * -1, 30 + 6 * i); c.line_to(6, 22); c.close_path(); fs(c, GRN, 3)
    for i in range(6): a = i * math.pi / 3; ell(c, 20 * math.cos(a), 4 + 14 * math.sin(a), 20, 18); fs(c, R1, 4)
    for i in range(5): a = i * 2 * math.pi / 5 + .3; ell(c, 11 * math.cos(a), 11 * math.sin(a) - 2, 15, 14); fs(c, R2, 3)
    ell(c, 0, -6, 12, 11); fs(c, R3, 3)
    c.move_to(0, -6)
    for i in range(1, 22): a = i * .5; rd = i * .5; c.line_to(rd * math.cos(a), -6 + rd * math.sin(a))
    c.set_source_rgb(*R1); c.set_line_width(2.5); c.stroke()
    ell(c, -12, -16, 4, 6); c.set_source_rgba(1, 1, 1, .8); c.fill()     # glint
    c.restore()
def speaker(c, x, y, q=1):
    """A small boombox: handle, two speakers - reads as music at a glance."""
    c.move_to(x - 34, y - 40); c.line_to(x - 34, y - 62); c.line_to(x + 34, y - 62); c.line_to(x + 34, y - 40)
    c.set_source_rgb(*INK); c.set_line_width(9); c.stroke()
    rr(c, x - 64, y - 42, 128, 72, 14); fs(c, hx('e8504f'), 6)
    for q_ in (-1, 1): ell(c, x + q_ * 34, y - 6, 22, 22); fs(c, hx('22252e'), 5); ell(c, x + q_ * 34, y - 6, 8, 8); c.set_source_rgb(*hx('5b6170')); c.fill()
    rr(c, x - 10, y - 34, 20, 12, 4); c.set_source_rgb(*hx('ffd23f')); c.fill()
def balloon(c, x, y, q=1):
    c.move_to(x, y); c.curve_to(x + 20, y - 80, x - 20, y - 160, x, y - 230); c.set_source_rgb(*INK); c.set_line_width(3); c.stroke()
    c.save(); c.translate(x, y - 300); c.scale(1.6, 1.6)
    c.move_to(0, 40); c.curve_to(-62, 2, -38, -50, 0, -20); c.curve_to(38, -50, 62, 2, 0, 40); c.close_path()
    fs(c, RED, 5); ell(c, -18, -14, 8, 6); c.set_source_rgba(1, 1, 1, .6); c.fill(); c.restore()

# ---------------- the sheet ----------------
GREYT = hx('4b5563')
def label(c, s, x, y, size=40, col=INK): txt(c, s, x, y, size, col, lw=0)
def sub(c, s, x, y): txt(c, s, x, y, 32, GREYT, lw=0)
def section(c, s, y): txt(c, s, 60, y, 56, NAVY, lw=0, align='l'); c.rectangle(60, y + 32, 2040, 5); c.set_source_rgb(*NAVY); c.fill()

def sheet(out='myai_sheet.png'):
    W, H = 2160, 4080
    S = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(S)
    c.set_source_rgb(*hx('eef1f6')); c.paint()
    txt(c, 'ME + MY AI  -  MY AI  -  CHARACTER SHEET v2', 1080, 60, 60, INK, lw=0)
    v9 = E.load_wgb(); import v as WV

    section(c, 'MY AI - who it is', 130)
    myai(c, 300, 1060, 1.4, eye='happy')
    label(c, 'DEFAULT: HAPPY', 300, 1120); sub(c, 'its optimism is the joke', 300, 1162)
    rs = 1.3; rx = 860; hp = hand_at(rx, 1060, rs, 1, 'hold2')                        # hand in hand: hers lands on his
    E.eva(c, hp[0] + 40 + 76 * .9, 1060, .9, 'charmed', sip=.1, pose='holdlow', hand_to=hp)
    myai(c, rx, 1060, rs, eye='happy', arms=('down', 'hold2'), tilt=8)
    label(c, 'WITH EVA', 1050, 1120); sub(c, 'her scarf = its eyes', 1050, 1162)
    myai(c, 1700, 1060, 1.05); WV.robot(c, 1980, 1060 - 280 * 1.05, 1.05, boss=True)
    limb(c, [(1980 - 34 * 1.05, 1060 - 75 * 1.05), (1980 - 34 * 1.05, 1060)], 34 * 1.05, WHITE); limb(c, [(1980 + 34 * 1.05, 1060 - 75 * 1.05), (1980 + 34 * 1.05, 1060)], 34 * 1.05, WHITE)
    my = 1060 - 280 * 1.05 + 52 * 1.05
    rr(c, 1980 - 26 * 1.05, my - 16 * 1.05, 70 * 1.05, 30 * 1.05, 8); c.set_source_rgb(*WHITE); c.fill()
    c.move_to(1980 - 20 * 1.05, my); c.line_to(1980 + 30 * 1.05, my); c.set_source_rgb(*INK); c.set_line_width(8); c.stroke()
    label(c, 'MY AI  vs  HARV', 1840, 1120); sub(c, 'visor + eyes / shades, no visor', 1840, 1162)

    section(c, 'EYES', 1240)
    for i, (m, a) in enumerate([('happy', 'HAPPY'), ('open', 'OPEN'), ('confused', 'CONFUSED'), ('blank', 'BLANK'),
                                ('heart', 'HEART'), ('wide', 'WIDE'), ('focus', 'FOCUS'), ('wink', 'WINK')]):
        x = 150 + i * 266
        c.save(); c.translate(x, 1440); c.scale(.92, .92)
        for q in (-1, 1): ell(c, q * 110, 0, 22, 38); fs(c, EARS, 8)
        rr(c, -108, -95, 216, 180, 78); fs(c, WHITE); rr(c, -82, -54, 164, 92, 40); fs(c, VISOR, 6); eyes(c, m); c.restore()
        label(c, a, x, 1610, 36)
    sub(c, 'CONFUSED = it misread the request.  BLANK = processing, or nothing to say.', 1080, 1666)

    section(c, 'POSES - one rig, joint angles only', 1740)
    P = [(('down', 'down'), 'happy', (None, None), 0, 0, 'REST', 'default stance'),
         (('down', 'wave'), 'happy', (None, None), 0, 0, 'WAVE', '"Your turn!"'),
         (('down', 'offer'), 'focus', (None, rose), 0, 0, 'OFFER', '"Watch." - the rose'),
         (('up', 'hip'), 'happy', (None, None), .12, 0, 'DANCE', 'one smooth move'),
         (('chest', 'down'), 'happy', (None, None), -.35, 0, 'BOW', 'tips at the feet'),
         (('give', 'down'), 'open', (balloon, None), 0, 0, 'GIVE', 'the balloon'),
         (('down', 'wait'), 'open', (None, None), 0, 0, 'WAIT', 'freeze 0.3-0.5 s'),
         (('down', 'down'), 'confused', (None, None), 0, 15, 'HEAD TILT', '+-15 deg, then a pause')]
    for i, (arms, e, pr, rot, tl, a, b) in enumerate(P):
        col, row = i % 4, i // 4
        x = 300 + col * 520; gy = 2330 + row * 700
        myai(c, x, gy, .9, eye=e, arms=arms, props=pr, rot=rot, tilt=tl)
        label(c, a, x, gy + 64); sub(c, b, x, gy + 104)

    section(c, 'RIG REFERENCE', 3200)
    s = 1.2; x0, gy = 300, 3960
    myai(c, x0, gy, s, eye='open', arms=('down', 'offer'))
    (sx, sy), (ex, ey), (hx_, hy), _ = arm_points(1, 'offer')
    oy = gy - 280 * s
    for (px, py), n in (((sx, sy), 'SHOULDER'), ((ex, ey), 'ELBOW'), ((hx_, hy), 'WRIST')):
        ell(c, x0 + px * s, oy + py * s, 11, 11); c.set_source_rgb(*RED); c.fill()
        pass
    for (px, py), n, ly in (((hx_, hy), 'WRIST', 3720), ((ex, ey), 'ELBOW', 3930), ((sx, sy), 'SHOULDER', 3990)):
        X, Y = x0 + px * s, oy + py * s                     # labels in a column to the right, leader lines to the joints
        c.move_to(X, Y); c.line_to(600, ly); c.set_source_rgb(*RED); c.set_line_width(3); c.stroke()
        txt(c, n, 612, ly, 30, RED, lw=0, align='l')
    for i, t in enumerate(['upper arm 68, forearm 68 (robot units)', 'shoulder 0-165 deg: 0 down, 90 out, 180 up',
                           'elbow -140..+140 deg: + lifts, - folds across', 'head tilt +-15 deg about the neck',
                           'hand: round mitt, thumb turns with the wrist']):
        txt(c, t, 760, 3300 + i * 52, 34, INK, lw=0, align='l')
    for i, (tn, n) in enumerate([(0, 'FRONT'), (.85, 'THREE-QUARTER'), (-.85, 'THREE-QUARTER (L)')]):
        x = 880 + i * 360
        myai(c, x, 3960, .62, eye='happy', turn=tn, arms=('down', 'down'))
        sub(c, n, x, 4010)
    gx = 1980; myai(c, gx - 50, 3960, .62, eye='focus', arms=('down', 'offer'), props=(None, rose))
    sub(c, 'GRIP', gx, 4010)
    S.write_to_png(os.path.join(HERE, out))

if __name__ == '__main__':
    sheet()
