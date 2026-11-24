"""Remove the Bottleneck: the office set and cast helpers, copied from just-one-line/kp.py (PR #72, two-legs fix included).
Room, desk, laptop, mug, chair, IK arms, Hoody seated/standing. Its own key poses (k0-k4) are not used here."""
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
def ik(sh, h, L1, L2, pref):
    dx, dy = h[0] - sh[0], h[1] - sh[1]; d0 = math.hypot(dx, dy); th = math.atan2(dy, dx)
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

