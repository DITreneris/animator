"""Just One Line: key poses (review before any animation).
One set, one camera: the desk on the right with the laptop, Hoody's rolling chair, MY AI's rolling step, the door.
Arms are two-bone and solved to their targets (lesson 172). Cast from perfect-date (kit, chars, MY AI v2).
Usage: python3 kp.py  ->  kp_<name>.png + key_poses.png"""
import os, sys, math, cairo
HERE = os.path.dirname(os.path.abspath(__file__)); PD = os.path.join(HERE, '..', 'perfect-date')
sys.path[:0] = [PD, os.path.join(PD, 'characters')]
import kit as K
from kit import INK, WHITE, NAVY, SKIN, YEL, RED, GREY, GREEN, rr, fs, ell, limb, txt, hx, lerp, W, H
import myai as A
import chars as C

FLOOR = 1560                          # feet stand here: everything readable stays above the apps' bottom zone (1600)
WALL0, WALL1 = hx('e9eef6'), hx('cfd8e6'); FLOOR_C = hx('8a7a6a'); DESK = hx('c58b54'); DESK_D = hx('8e5c31')
JEANS = hx('3b4a6b'); JEANS_FAR = hx('2e3a57'); CHAIR = hx('2b2f3a'); STEP = hx('d9573b')
HS = 1.25                             # Hoody's scale
AS = 1.08 * HS                        # MY AI: 0.6 of Hoody's standing height (the series size rule)
DESK_X0, DESK_X1, DESK_Y = 470, 1080, 1185
LAP = dict(x0=745, x1=950, y0=925, y1=1170)   # taller: the label and the number read on a phone   # the laptop screen (text inside x 60-960)

# ---------------- set ----------------
NIGHT = 0.0                           # 0 = the office by day; 1 = the nightmare: the whole background sinks into the dark
NIGHT_TO = dict(wall0=hx('2a2440'), wall1=hx('15122a'), floor=hx('1c1622'), door=hx('3a3358'), doorlit=hx('4a4370'), seam=hx('120f1c'))
def nt(col, key):
    return tuple(a + (b - a) * NIGHT for a, b in zip(col, NIGHT_TO[key]))
def wall_grad():
    g = cairo.LinearGradient(0, 0, 0, FLOOR); g.add_color_stop_rgb(0, *nt(WALL0, 'wall0')); g.add_color_stop_rgb(1, *nt(WALL1, 'wall1')); return g
def room(c, door=0.0):
    c.rectangle(0, 0, W, FLOOR); c.set_source(wall_grad()); c.fill()
    c.rectangle(0, FLOOR, W, H - FLOOR); c.set_source_rgb(*nt(FLOOR_C, 'floor')); c.fill()
    c.rectangle(0, FLOOR - 6, W, 12); c.set_source_rgb(*nt(hx('6b5d50'), 'seam')); c.fill()
    rr(c, 40, 560, 250, 1000, 6); fs(c, nt(hx('b9c4d6'), 'door'), 7)            # the door (HARV comes in here)
    if door > 0:
        c.save(); rr(c, 40, 560, 250 * (1 - .7 * door), 1000, 6); fs(c, nt(hx('dfe6f0'), 'doorlit'), 7); c.restore()
    ell(c, 260, 1060, 12, 12); fs(c, YEL, 5)
    rr(c, 640, 680, 280, 200, 10); fs(c, WHITE, 6)                                # a wall chart: arrows up and to the right
    c.move_to(670, 850); c.line_to(740, 800); c.line_to(800, 820); c.line_to(890, 720)
    c.set_source_rgb(*GREEN); c.set_line_width(10); c.stroke()

def desk(c):
    rr(c, DESK_X0, DESK_Y, DESK_X1 - DESK_X0 + 40, 34, 8); fs(c, DESK, 7)
    for x in (DESK_X0 + 30, DESK_X1 - 30):
        rr(c, x - 14, DESK_Y + 30, 28, FLOOR - DESK_Y - 30, 6); fs(c, DESK_D, 6)

def laptop(c, n=None, tick=False, glow=0.0):
    x0, x1, y0, y1 = LAP['x0'], LAP['x1'], LAP['y0'], LAP['y1']
    c.move_to(x0 - 10, DESK_Y); c.line_to(x1 + 40, DESK_Y); c.line_to(x1 + 20, DESK_Y - 18); c.line_to(x0 + 10, DESK_Y - 18); c.close_path(); fs(c, GREY, 6)
    rr(c, x0, y0, x1 - x0, y1 - y0, 14); fs(c, hx('1d2233'), 7)
    rr(c, x0 + 14, y0 + 14, x1 - x0 - 28, y1 - y0 - 28, 8); c.set_source_rgb(*hx('0f1424')); c.fill()
    cx = (x0 + x1) / 2
    if n is not None:
        txt(c, 'FILES', cx, y0 + 52, 40, hx('8fd6ff'), lw=0); txt(c, 'CHANGED', cx, y0 + 94, 40, hx('8fd6ff'), lw=0)
        txt(c, str(n), cx, y0 + 172, 108, WHITE if not tick else hx('5df08a'), lw=0)
        if tick:
            ell(c, x1 - 40, y0 + 40, 26, 26); c.set_source_rgb(*hx('2bbf5a')); c.fill()
            c.move_to(x1 - 52, y0 + 40); c.line_to(x1 - 43, y0 + 50); c.line_to(x1 - 26, y0 + 30); c.set_source_rgb(1, 1, 1); c.set_line_width(7); c.stroke()

def mug(c, x, y, s=1.0):
    """The #1 DEV mug (the plant): one drawing, used in every shot."""
    c.save(); c.translate(x, y); c.scale(s, s)
    c.arc(34, -30, 18, -1.3, 1.3); c.set_source_rgb(*INK); c.set_line_width(16); c.stroke()
    c.arc(34, -30, 18, -1.3, 1.3); c.set_source_rgb(*WHITE); c.set_line_width(8); c.stroke()
    rr(c, -34, -64, 68, 64, 12); fs(c, WHITE, 6)
    txt(c, '#1', 0, -44, 22, RED, lw=0); txt(c, 'DEV', 0, -20, 18, NAVY, lw=0)
    c.restore()

def card(c, x, y, s=1.0, rot=0.0, stamp=False):
    """The TASK card: 'TASK / Just one line.' - the same drawing at the start and the end (protect item 1)."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    rr(c, -95, -62, 190, 124, 10); fs(c, WHITE, 6)
    txt(c, 'TASK', 0, -30, 34, INK, lw=0); txt(c, 'Just one line.', 0, 14, 24, NAVY, lw=0)
    c.move_to(-60, 40); c.line_to(60, 40); c.set_source_rgb(*GREY); c.set_line_width(4); c.stroke()
    if stamp:
        c.save(); c.rotate(-.26); rr(c, -92, -26, 184, 52, 8); c.set_source_rgba(.85, .1, .15, .9); c.set_line_width(6); c.stroke()
        txt(c, 'APPROVED', 0, 0, 34, hx('d0182a'), lw=0); c.restore()
    c.restore()

def chair(c, x, seat_y, rot=0.0, spin=0.0, back_side=-1):
    """Rolling office chair. back_side -1: the back on the left (the sitter faces right)."""
    c.save(); c.translate(x, seat_y); c.rotate(rot)
    rr(c, -95, -18, 190, 36, 16); fs(c, CHAIR, 6)                                   # seat
    bx = back_side * 92
    limb(c, [(bx, 0), (bx - back_side * 6, -150)], 18, GREY)
    rr(c, bx - 30, -330, 60, 200, 24); fs(c, CHAIR, 6)                            # back
    limb(c, [(0, 18), (0, 120)], 18, GREY)                                          # gas lift
    for i, a in enumerate((-1, -.35, .35, 1)):
        a2 = a * math.cos(spin)
        limb(c, [(0, 120), (a2 * 110, 160)], 14, GREY)
        ell(c, a2 * 110, 172, 15, 15); fs(c, INK, 0)
    c.restore()

def step(c, x, rot=0.0):
    """MY AI's rolling step (C-E): a stable platform, so it reaches the keys at 0.6 of Hoody's size."""
    c.save(); c.translate(x, FLOOR); c.rotate(rot)
    rr(c, -95, -150, 190, 130, 16); fs(c, STEP, 7)
    for q in (-1, 1): ell(c, q * 60, -12, 14, 14); fs(c, INK, 0)
    c.restore()
    return FLOOR - 150

def pot(c, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(-34, -70); c.line_to(34, -70); c.line_to(46, 30); c.line_to(-46, 30); c.close_path(); fs(c, hx('c9e6ff'), 6)
    rr(c, -40, -10, 80, 40, 6); c.set_source_rgb(*hx('5a3418')); c.fill()
    rr(c, -30, -86, 60, 20, 8); fs(c, INK, 0)
    c.arc(56, -20, 26, -1.4, 1.4); c.set_source_rgb(*INK); c.set_line_width(10); c.stroke()
    c.restore()

def briefcase(c, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.arc(0, -70, 26, math.pi, 2 * math.pi); c.set_source_rgb(*INK); c.set_line_width(10); c.stroke()
    rr(c, -80, -70, 160, 110, 12); fs(c, hx('3a2a22'), 6)
    rr(c, -62, -46, 124, 36, 8); fs(c, WHITE, 4); txt(c, 'HOODY', 0, -28, 26, INK, lw=0)        # the tag reads on a phone
    c.restore()

def lines(c, pts, n=3, col=INK, a=.55, w=6):
    """Motion lines along a path of points (start -> end)."""
    for i in range(n):
        off = (i - (n - 1) / 2) * 22
        (x0, y0), (x1, y1) = pts
        dx, dy = x1 - x0, y1 - y0; L = math.hypot(dx, dy) or 1; px, py = -dy / L * off, dx / L * off
        c.move_to(x0 + px, y0 + py); c.line_to(x1 + px, y1 + py); c.set_source_rgba(*col, a); c.set_line_width(w); c.stroke()

# ---------------- two-bone arms ----------------
AMIN = math.radians(70)                # v3: no elbow folds sharper than this (the zigzag / spike elbows of v2)
def ik(sh, h, L1, L2, pref):
    dx, dy = h[0] - sh[0], h[1] - sh[1]; d0 = math.hypot(dx, dy); th = math.atan2(dy, dx)
    dmin = math.sqrt(L1 * L1 + L2 * L2 - 2 * L1 * L2 * math.cos(AMIN))
    if d0 < dmin: k = max(.45, d0 / dmin); L1 *= k; L2 *= k      # a close target: the arm shortens (sleeve / telescopic arm) instead of folding flat
    d = min(max(d0, abs(L1 - L2) + 2), L1 + L2 - .5)
    a = math.acos(max(-1, min(1, (L1 * L1 + d * d - L2 * L2) / (2 * L1 * d))))
    cands = [(sh[0] + L1 * math.cos(th + b * a), sh[1] + L1 * math.sin(th + b * a)) for b in (-1, 1)]
    e = pref(cands); return e, (sh[0] + d * math.cos(th), sh[1] + d * math.sin(th))
DOWN = lambda cs: max(cs, key=lambda p: p[1]); UP = lambda cs: min(cs, key=lambda p: p[1])
LEFT = lambda cs: min(cs, key=lambda p: p[0]); RIGHT = lambda cs: max(cs, key=lambda p: p[0])

def ai_pose(q, target_local, pref=DOWN):
    """MY AI's arm angles (perfect-date convention: shoulder 0 = down, 90 = out; elbow relative) that put the hand on a
    target in the robot's own (unscaled) coordinates."""
    sh = (q * A.SHOULDER[0], A.SHOULDER[1])
    e, h = ik(sh, target_local, A.L1, A.L2, pref)
    a1 = math.degrees(math.atan2(q * (e[0] - sh[0]), e[1] - sh[1]))
    t2 = math.degrees(math.atan2(q * (h[0] - e[0]), h[1] - e[1]))
    return (a1, t2 - a1)
def ai_local(x, gy, s, p): return ((p[0] - x) / s, (p[1] - (gy - 280 * s)) / s)

def hoody_arm(c, sh, target, s, pref=DOWN, hand='ball', ang=None, L=(118, 112)):
    e, h = ik(sh, target, L[0] * s, L[1] * s, pref)
    limb(c, [sh, e, h], 44 * s, NAVY)
    a = math.atan2(h[1] - e[1], h[0] - e[0]) if ang is None else ang
    if hand == 'ball': K.hand(c, h[0], h[1], s)
    elif hand == 'palm': K.palm(c, h[0], h[1], s * .8, a, flick=0)
    elif hand == 'point': point(c, h[0], h[1], a, s)
    elif hand == 'grip': grip(c, h[0], h[1], a, s)
    return e, h
def point(c, x, y, ang, s):
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    rr(c, 12, -30, 52, 18, 9); fs(c, SKIN, 5); rr(c, -24, -24, 48, 48, 16); fs(c, SKIN, 6)
    c.set_source_rgb(*INK); c.set_line_width(4)
    for yy in (-6, 6): c.move_to(8, yy); c.line_to(22, yy); c.stroke()
    c.restore()
def grip(c, x, y, ang, s):
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    rr(c, -24, -24, 48, 48, 16); fs(c, SKIN, 6)
    c.set_source_rgb(*INK); c.set_line_width(4)
    for yy in (-10, 0, 10): c.move_to(10, yy); c.line_to(24, yy); c.stroke()
    c.restore()

def hoody_seated(c, x, seat_y, expr, s=HS, rot=0.0, legs=None):
    """Seated on the chair at (x, seat_y), facing right. Returns (shoulders, head) for the arms and bubbles."""
    c.save(); c.translate(x, seat_y); c.rotate(rot); c.translate(-x, -seat_y)
    hip = (x + 10 * s, seat_y - 14 * s)
    kn = legs[0] if legs else (x + 170 * s, seat_y - 4 * s); ft = legs[1] if legs else (x + 190 * s, FLOOR - 26)
    # two legs (Tomas, 23 Nov: "sometimes he has only one leg"): the far leg first, a shade darker, its knee and foot
    # set back and up a little, so it shows past the near one in every pose (seated, tumbling, on the floor)
    off = (-30 * s, -16 * s)
    fhip, fkn, fft = (hip[0] - 6 * s, hip[1] - 6 * s), (kn[0] + off[0], kn[1] + off[1]), (ft[0] + off[0] - 14 * s, ft[1] + off[1] * .5)
    if legs: fkn, fft = (kn[0] + 50 * s, kn[1] - 125 * s), (ft[0] - 40 * s, ft[1])   # on the floor / tumbling: the far knee drawn up, so both legs read
    limb(c, [fhip, fkn, fft], 56 * s, JEANS_FAR); rr(c, fft[0] - 20 * s, fft[1] - 8 * s, 70 * s, 32 * s, 14 * s); fs(c, INK, 0)
    limb(c, [hip, kn, ft], 58 * s, JEANS); rr(c, ft[0] - 20 * s, ft[1] - 8 * s, 70 * s, 32 * s, 14 * s); fs(c, INK, 0)
    neck = (x + 6 * s, seat_y - 210 * s)
    shL, shR = K.hoodie(c, neck[0], neck[1], s * 1.1)
    head = (neck[0] + 4 * s, neck[1] - 150 * s)
    K.hoodyz_head(c, head[0], head[1], s, era='young', expr=expr, blink=False, gaze=12)
    c.restore()
    def tr(p):                                                    # the same rotation, for the arms the caller draws
        dx, dy = p[0] - x, p[1] - seat_y; ca, sa = math.cos(rot), math.sin(rot)
        return (x + dx * ca - dy * sa, seat_y + dx * sa + dy * ca)
    return tr(shL), tr(shR), tr(head)

def hoody_standing(c, x, gy, expr, s=HS, bow=0.0, gaze=0, side=1):
    """Standing on gy; bow 0..1 bends him forward from the hips toward side (+1 right, -1 left)."""
    hip = (x, gy - 300 * s)
    for q in (-1, 1):
        limb(c, [(hip[0] + q * 30 * s, hip[1]), (x + q * 34 * s, gy - 20 * s)], 58 * s, JEANS)
        rr(c, x + q * 34 * s - 30 * s, gy - 26 * s, 70 * s, 30 * s, 14 * s); fs(c, INK, 0)
    a = .55 * bow * side
    c.save(); c.translate(*hip); c.rotate(a); c.translate(-hip[0], -hip[1])
    neck = (x, hip[1] - 176 * s * 1.1 + 30 * s)
    shL, shR = K.hoodie(c, neck[0], neck[1], s * 1.1)
    head = (x, neck[1] - 150 * s)
    K.hoodyz_head(c, head[0], head[1], s, era='young', expr=expr, blink=False, gaze=gaze)
    c.restore()
    def tr(p):
        dx, dy = p[0] - hip[0], p[1] - hip[1]; ca, sa = math.cos(a), math.sin(a)
        return (hip[0] + dx * ca - dy * sa, hip[1] + dx * sa + dy * ca)
    return tr(shL), tr(shR), tr(head)

def bubble(c, lines_, size, tip, cx, cy):
    c.save(); c.select_font_face('Lilita One'); c.set_font_size(size)
    w = max(c.text_extents(l).width for l in lines_) + 100; h = len(lines_) * size * 1.12 + 56; c.restore()
    bx = min(max(tip[0], cx - w / 2 + 60), cx + w / 2 - 60); by = cy + h / 2 - 10 if tip[1] > cy else cy - h / 2 + 10
    c.move_to(bx - 28, by); c.curve_to(bx - 10, (by + tip[1]) / 2, tip[0] - 4, tip[1] - 10, *tip); c.curve_to(tip[0] + 8, tip[1] - 30, bx + 10, (by + tip[1]) / 2, bx + 28, by)
    c.close_path(); fs(c, WHITE, 7)
    rr(c, cx - w / 2, cy - h / 2, w, h, 40); fs(c, WHITE, 7)
    c.move_to(bx - 24, by); c.line_to(bx + 24, by); c.set_source_rgb(1, 1, 1); c.set_line_width(12); c.stroke()
    lh = size * 1.12; y0 = cy - (len(lines_) - 1) * lh / 2
    for i, l in enumerate(lines_): txt(c, l, cx, y0 + i * lh, size, INK, lw=0)

def topbar(c): C.topbar(c, 'HIS FIX')

# ---------------- key poses ----------------
CHAIR_X, SEAT_Y = 270, 1330
STAND_X = 660                         # where the one who stands waits at frame 0 and in the last frame (the match cut),
                                      # left of the laptop, so the counter stays visible in the last frame
HAND_OFF = (430, 1170)                # where the TASK card changes hands at frame 0 ...
K4_OFF = (470, 1110)                  # ... and in the last frame (the seated robot's reach): nearly the same spot
KEY = (LAP['x0'] + 30, DESK_Y - 24)   # the keys MY AI types on
K.FACES['strain'] = ('open', ('angry', 'angry'), 'grin')     # Hoody pulling with everything he has
K.FACES['beaten'] = ('half', ('worried', 'worried'), 'frown')  # the intern

def k0(c):   # frame 0: Hoody seated, smug, finger up, holds out the TASK card to MY AI standing by the desk
    room(c); desk(c); laptop(c); mug(c, 560, DESK_Y, 1.1)
    chair(c, CHAIR_X, SEAT_Y)
    shL, shR, head = hoody_seated(c, CHAIR_X, SEAT_Y, 'smug')
    x, gy = STAND_X, FLOOR
    A.myai(c, x, gy, AS, eye='open', look=(-16, -6), arms=(ai_pose(-1, ai_local(x, gy, AS, (HAND_OFF[0] + 70, HAND_OFF[1] + 10)), DOWN), 'down'))
    hoody_arm(c, shR, (HAND_OFF[0] - 70, HAND_OFF[1] + 10), HS, pref=DOWN, hand='grip')
    card(c, *HAND_OFF, .9, rot=-.05)
    hoody_arm(c, shL, (shL[0] - 95, shL[1] - 190), HS, pref=LEFT, hand='point', ang=-math.pi / 2 - .15)
    bubble(c, ['JUST ONE LINE.'], 74, (head[0] + 60, head[1] - 200), 380, 500)
    topbar(c)

def k1(c):   # the shove (0.5 s): MY AI's open hand flat on Hoody's chest; he and the chair tip and roll away from it.
    # MY AI smiles at the laptop the whole time, the card held high in its other hand
    room(c); desk(c); laptop(c, 0); mug(c, 560, DESK_Y, 1.1)
    cx = CHAIR_X - 10; tilt = -.12
    lines(c, [(cx + 300, SEAT_Y - 150), (cx + 150, SEAT_Y - 150)], 3)
    chair(c, cx, SEAT_Y, rot=tilt, spin=.6)
    shL, shR, head = hoody_seated(c, cx, SEAT_Y, 'shock', rot=tilt)
    hoody_arm(c, shL, (shL[0] - 110, shL[1] - 90), HS, pref=LEFT, hand='palm')                 # arms thrown back
    hoody_arm(c, shR, (shR[0] + 30, shR[1] - 200), HS, pref=RIGHT, hand='palm')
    chest = ((shL[0] + shR[0]) / 2 + 60, (shL[1] + shR[1]) / 2 + 80)
    x, gy = 600, FLOOR; lean = -.12
    pa = ai_pose(-1, ai_local(x, gy, AS, (chest[0] + 20, chest[1])), DOWN)
    up = ai_local(x, gy, AS, (x + 60, 900))
    A.myai(c, x, gy, AS, eye='happy', look=(18, 0), rot=lean, arms=(pa, ai_pose(1, up, UP)))
    hx_, hy = A.hand_at(x, gy, AS, 1, ai_pose(1, up, UP))
    card(c, hx_ + 10, hy - 50, .8, rot=.12)
    px, py = A.hand_at(x, gy, AS, -1, pa)
    K.palm(c, px - 6, py, AS * .55, math.pi, flick=0)                                            # the flat hand on his chest
    for i in range(3): c.arc(px - 10, py, 46 + i * 24, 2.3, 4.0); c.set_source_rgba(*INK, .5); c.set_line_width(6); c.stroke()
    topbar(c)

def k2(c):   # the wrestle: on a diagonal. MY AI leans in to the keys, smiling, typing on; Hoody leans back with all his
    # weight on its left arm, both fists on it, heels dug in; the arm stretched between them
    room(c); desk(c); laptop(c, 12); mug(c, 560, DESK_Y, 1.1)
    chair(c, 40, SEAT_Y, spin=1.2)
    x = 560; gy = step(c, x)
    pull = (x - 175, 1170)
    pl = ai_pose(-1, ai_local(x, gy, AS, pull), DOWN)
    shL, shR, head = hoody_standing(c, 265, FLOOR, 'strain', bow=.5, gaze=14, side=-1)
    A.myai(c, x, gy, AS, eye='happy', look=(18, 0), rot=.14, arms=(pl, ai_pose(1, ai_local(x, gy, AS, KEY), DOWN)))
    hx_, hy = A.hand_at(x, gy, AS, -1, pl)
    hoody_arm(c, shR, (hx_ - 14, hy - 18), HS, pref=DOWN, hand='grip', ang=0)
    hoody_arm(c, shL, (hx_ - 58, hy + 10), HS, pref=DOWN, hand='grip', ang=0)
    for i in range(3): c.arc(KEY[0] + 20, KEY[1] - 30, 30 + i * 18, -1.6, -.2); c.set_source_rgba(*INK, .5); c.set_line_width(5); c.stroke()
    for dx, dy in ((60, -40), (90, 0)):                                                       # effort
        ell(c, head[0] + dx, head[1] + dy, 9, 14); fs(c, hx('58c7ff'), 4)
    topbar(c)

def k3(c):   # THE KICK (iconic): Hoody airborne, tumbling back-left, clear of the chair; MY AI types on, its left leg
    # kicked out behind it (the other leg on the step), a thumbs-up over its shoulder, its face never leaves the screen
    room(c); desk(c); laptop(c, 31); mug(c, 560, DESK_Y, 1.1)
    chair(c, 175, SEAT_Y - 10, rot=.45, spin=2.0)                                    # the chair, tipping away on its own
    x = 520; gy = step(c, x); r = .06
    def w(lx, ly):                                                                     # robot-local -> world (with its lean)
        X, Y = lx * AS, ly * AS - 280 * AS; ca, sa = math.cos(r), math.sin(r)
        return (x + X * ca - Y * sa, gy + X * sa + Y * ca)
    hip, kn, ft = w(-34, 205), w(-120, 236), w(-215, 212)
    limb(c, [hip, kn, ft], 34 * AS, WHITE)                                            # the kicking leg, straight out behind
    c.save(); c.translate(*ft); c.rotate(math.pi + .1); rr(c, -26, -24, 64, 48, 20); fs(c, WHITE, 7); c.restore()
    for i in range(3): c.arc(ft[0] + 10, ft[1], 40 + i * 22, 2.2, 4.1); c.set_source_rgba(*INK, .5); c.set_line_width(6); c.stroke()   # contact
    old = A.limb                                                                       # draw MY AI without its left leg
    A.limb = lambda c_, pts, *a: None if pts == [(-34, 205), (-34, 280)] else old(c_, pts, *a)
    thumb = (x - 150, 1075)
    pl = ai_pose(-1, ai_local(x, gy, AS, thumb), UP)
    try: A.myai(c, x, gy, AS, eye='happy', look=(18, 0), rot=r, arms=(pl, ai_pose(1, ai_local(x, gy, AS, KEY), DOWN)))
    finally: A.limb = old
    tx, ty = A.hand_at(x, gy, AS, -1, pl)
    rr(c, tx - 12, ty - 66, 26, 50, 12); fs(c, WHITE, 7)                             # the thumb, up, over its shoulder
    # Hoody: thrown back-left, chair gone from under him, arms flailing, legs up
    c.save(); c.translate(370, 780); c.rotate(-.42)
    sh = hoody_seated(c, 0, 0, 'shock', s=HS * .7, legs=((120, -30), (200, -150)))
    c.restore()
    shL, shR, head = sh
    def rot(p, a=-.42, o=(370, 780)): return (o[0] + p[0] * math.cos(a) - p[1] * math.sin(a), o[1] + p[0] * math.sin(a) + p[1] * math.cos(a))
    L, Rr = rot(shL), rot(shR)
    hoody_arm(c, L, (L[0] - 110, L[1] - 120), HS * .74, pref=LEFT, hand='palm')
    hoody_arm(c, Rr, (Rr[0] + 50, Rr[1] - 190), HS * .74, pref=RIGHT, hand='palm')
    for i in range(3): c.arc(420, 1000, 220 + i * 26, 2.2, 3.4); c.set_source_rgba(*INK, .45); c.set_line_width(6); c.stroke()   # his arc
    topbar(c)

def k4(c):   # the takeover = the last frame: MY AI SITS in Hoody's chair, sipping from his #1 DEV mug, the briefcase at
    # its feet, and holds out the TASK card; Hoody, head down, shoulders in, the coffee pot in his other hand, takes it.
    # 47 ✓ on the laptop. The same framing as frame 0: the chair in its place, the one who stands at the desk's edge.
    room(c); desk(c); laptop(c, 47, tick=True)
    chair(c, CHAIR_X, SEAT_Y)
    x = CHAIR_X + 10; gy = SEAT_Y - 18 + 60 * AS
    mugp = (x - 105, 1040)
    old = A.limb                                                                               # seated: its own legs drawn below
    A.limb = lambda c_, pts, *a: None if pts in ([(-34, 205), (-34, 280)], [(34, 205), (34, 280)]) else old(c_, pts, *a)
    try:
        A.myai(c, x, gy, AS, eye='happy', look=(16, -4), tilt=-6,
               arms=(ai_pose(-1, ai_local(x, gy, AS, mugp), UP), ai_pose(1, ai_local(x, gy, AS, (K4_OFF[0] - 70, K4_OFF[1] + 10)), DOWN)))
    finally: A.limb = old
    for q in (-1, 1):                                                                          # legs dangling over the seat's edge
        hip = (x + q * 34 * AS, gy - 75 * AS); kn = (x + q * 40 * AS, gy - 30 * AS); ft = (x + q * 46 * AS + 10, gy + 50 * AS)
        limb(c, [hip, kn, ft], 34 * AS, WHITE)
    mug(c, mugp[0] + 6, mugp[1] + 36, 1.1)
    briefcase(c, x + 170, FLOOR - 6, 1.25)
    shL, shR, head = hoody_standing(c, STAND_X, FLOOR, 'beaten', bow=.6, gaze=-16, side=-1)
    hoody_arm(c, shL, (K4_OFF[0] + 70, K4_OFF[1] + 10), HS, pref=DOWN, hand='grip')
    card(c, *K4_OFF, .9, rot=-.05)
    hoody_arm(c, shR, (shR[0] - 50, shR[1] + 215), HS, pref=RIGHT, hand='grip')
    pot(c, shR[0] - 50, shR[1] + 305, 1.1)
    bubble(c, ['JUST ONE LINE.'], 74, (x - 160, gy - 380), 420, 500)
    topbar(c)

KP = dict(k0=k0, k1=k1, k2=k2, k3=k3, k4=k4)
NAMES = dict(k0='frame 0', k1='the shove', k2='the wrestle', k3='THE KICK', k4='takeover = last frame')

if __name__ == '__main__':
    keys = sys.argv[1:] or list(KP)
    surfs = {}
    for k in keys:
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); KP[k](cairo.Context(s)); surfs[k] = s; s.write_to_png(os.path.join(HERE, f'kp_{k}.png'))
    n = len(keys); sw, sh = int(W * .4), int(H * .4)
    out = cairo.ImageSurface(cairo.FORMAT_ARGB32, sw * n + 10 * (n + 1), sh + 80); c = cairo.Context(out); c.set_source_rgb(1, 1, 1); c.paint()
    for i, k in enumerate(keys):
        x = 10 + i * (sw + 10)
        c.save(); c.translate(x, 70); c.scale(.4, .4); c.set_source_surface(surfs[k]); c.paint(); c.restore()
        txt(c, f'{k}  {NAMES[k]}', x + sw / 2, 36, 30, NAVY, lw=0)
    out.write_to_png(os.path.join(HERE, 'key_poses.png')); print('ok', *keys)
