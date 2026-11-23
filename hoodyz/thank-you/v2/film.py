"""He Always Said Thank You, v2 (23 Nov). v1 is imported and untouched; v2 changes framing, speech, the series bar and the loop.
- THE LOOP IS THE STORY: after "...Thank you?" the toaster raises its own DELETE ray and joins the firing squad, and the
  gold-sunglasses robot shrugs and walks out of frame. The last frame is the opening line-up, so it plays straight back into
  "Any last words, human?". One bad night undid years of thank-yous. In frame 0 the toaster is already in the squad, with
  its little ray: the planted detail now pays off twice.
- A closer camera on every ruins shot (1.18x, the ground line low): the characters fill the frame, nobody is cut by an edge.
- Speech bubbles with tails on the speaker; the series bar (ME + MY AI, a year chip) replaces the bare "2037".
- Hoody's lines will be Tomas's own recordings (Phew. / You useless toaster! / ...Thank you?).
Usage: python3 film.py keys | frames F ..."""
import sys, os, math, importlib.util, cairo
HERE = os.path.dirname(os.path.abspath(__file__)); V1 = os.path.join(HERE, '..', 'v1'); SH = os.path.join(HERE, '..', '..', 'says-here-boss', 'v3')
sys.path.insert(0, V1)
def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
import v as Vv
R = _load('ty_v1_render', os.path.join(V1, 'render.py'))
sys.path.insert(1, SH); SC = _load('sh_chars', os.path.join(SH, 'chars.py'))
from v import INK, WHITE, NAVY, SKIN, YEL, RED, GREY, rr, fs, ell, limb, txt, hx, W, H
lerp = lambda a, b, t: a + (b - a) * t
cl = lambda t: max(0.0, min(1.0, t))
oe = lambda t: 1 - (1 - cl(t)) ** 3
back = Vv.back

# ---------------- the camera: world (540, 1500) -> screen (540, 1640), 1.18x ----------------
Z, PIV, TO = 1.18, (540, 1500), (540, 1640)
def cam(c): c.translate(*TO); c.scale(Z, Z); c.translate(-PIV[0], -PIV[1])
def scr(x, y): return (TO[0] + (x - PIV[0]) * Z, TO[1] + (y - PIV[1]) * Z)
def topbar(c, pill): SC.topbar(c, pill)

# ---------------- speech: a bubble whose tail ends on the speaker ----------------
def bubble(c, lines, size, tip, cx=540, cy=560, w=None, hl=(), r=99, via=None):
    k = back(r / 5) if r < 5 else 1
    if k <= .03: return
    c.save(); c.select_font_face('Lilita One'); c.set_font_size(size)
    w = w or max(c.text_extents(l).width for l in lines) + 110; h = len(lines) * size * 1.12 + 64
    c.restore()
    c.save(); c.translate(cx, cy); c.scale(k, k); c.translate(-cx, -cy)
    bx = min(max((via or tip)[0], cx - w / 2 + 70), cx + w / 2 - 70)
    if via:                                                                   # a bent tail: down to `via`, then in to the tip (round his hair)
        c.move_to(bx - 34, cy + h / 2 - 8); c.curve_to(via[0] - 30, via[1], via[0] - 10, via[1] + 20, *tip)
        c.curve_to(via[0] + 30, via[1] - 10, via[0] + 34, via[1] - 40, bx + 34, cy + h / 2 - 8); c.close_path(); fs(c, WHITE)
    else:
        c.move_to(bx - 34, cy + h / 2 - 8); c.line_to(*tip); c.line_to(bx + 34, cy + h / 2 - 8); c.close_path(); fs(c, WHITE)
    rr(c, cx - w / 2, cy - h / 2, w, h, 48); fs(c, WHITE)
    c.move_to(bx - 30, cy + h / 2 - 12); c.line_to(bx + 30, cy + h / 2 - 12); c.set_source_rgb(1, 1, 1); c.set_line_width(14); c.stroke()
    lh = size * 1.12; y0 = cy - (len(lines) - 1) * lh / 2
    for i, l in enumerate(lines): txt(c, l, cx, y0 + i * lh, size, RED if i in hl else INK, lw=0)
    c.restore()
def bubble_side(c, lines, size, tip, cx, cy, r=99):
    k = back(r / 5) if r < 5 else 1
    if k <= .03: return
    c.save(); c.select_font_face('Lilita One'); c.set_font_size(size)
    w = max(c.text_extents(l).width for l in lines) + 90; h = len(lines) * size * 1.12 + 56; c.restore()
    q = -1 if tip[0] < cx else 1
    c.save(); c.translate(cx, cy); c.scale(k, k); c.translate(-cx, -cy)
    ey = min(max(tip[1], cy - h / 2 + 40), cy + h / 2 - 40)
    c.move_to(cx + q * (w / 2 - 10), ey - 28); c.line_to(*tip); c.line_to(cx + q * (w / 2 - 10), ey + 28); c.close_path(); fs(c, WHITE)
    rr(c, cx - w / 2, cy - h / 2, w, h, 44); fs(c, WHITE)
    c.move_to(cx + q * (w / 2 - 14), ey - 24); c.line_to(cx + q * (w / 2 - 14), ey + 24); c.set_source_rgb(1, 1, 1); c.set_line_width(14); c.stroke()
    lh = size * 1.12; y0 = cy - (len(lines) - 1) * lh / 2
    for i, l in enumerate(lines): txt(c, l, cx, y0 + i * lh, size, INK, lw=0)
    c.restore()
def robot_tip(x, y, s): return scr(x, y - 165 * s)            # just above a robot's antenna ball
def guy_tip(x, y, s, side=1): return scr(x + side * 120 * s, y + 70 * s)   # beside Hoody's cheek, below his hair

# ---------------- the line-up (frame 0 and the last frame) ----------------
LX, RX, GX, GY_, TX, TY = 205, 875, 540, 1205, 790, 1395
def squad(c, f, aim=1.0, toaster_ray=True, red=True, guy_expr='small'):
    """The firing squad: two red robots aiming, Hoody hands up with the dot on his forehead, the toaster with its own ray."""
    R.ruins(c, f)
    for x, d in ((LX, 1), (RX, -1)):
        R.rb(c, x, 905, 1.05, red=red)
        R.ray(c, x + d * 120, 1070, 1.1, d, rot=.1 * aim)
        limb(c, [(x + d * 48, 1040), (x + d * 72, 1070)], 30, WHITE)
    R.toaster(c, TX, TY, .72, 'glare')
    if toaster_ray:
        R.ray(c, TX - 105, TY - 6, .55, -1, rot=-.25)
        limb(c, [(TX - 70, TY + 10), (TX - 90, TY - 4)], 14, GREY)
    R.guy(c, GX, GY_, 1, guy_expr, f=f)
    R.dot(c, GX, GY_ - 55, f)

# ---------------- shots ----------------
def A(c, f, r):   # frame 0: the squad is already in place; "Any last words, human?" from the left robot
    c.save(); cam(c); squad(c, f); c.restore()
    bubble(c, ['ANY LAST WORDS,', 'HUMAN?'], 96, robot_tip(LX, 905, 1.05), cy=560, r=r - 1)
    topbar(c, '2037')

def B(c, f, r):   # the gold robot steps in, pushes the right ray away: "Wait! Not this guy!"
    p = back(r / 7)
    c.save(); cam(c)
    R.ruins(c, f)
    R.rob_arm_ray(c, LX, 905, 1.05, 1, f)
    R.rob_arm_ray(c, lerp(RX, 1180, oe(r / 6)), 905, 1.05, -1, f)
    R.toaster(c, TX, TY, .72, 'glare'); R.ray(c, TX - 105, TY - 6, .55, -1, rot=-.25)    # the same place as frame 0
    R.guy(c, 470, 1185, 1, 'small', f=f)
    Vv.robot(c, lerp(1250, 790, cl(p)), 960, 1.2, boss=True)
    limb(c, [(740, 1060), (620, 960), (500, 935)], 26, WHITE); ell(c, 486, 932, 28, 28); fs(c, WHITE, 7)
    c.restore()
    bubble(c, ['WAIT!', 'NOT THIS GUY!'], 108, robot_tip(lerp(1250, 790, cl(p)), 960, 1.2), cy=560, hl=(0,), r=r - 1)
    topbar(c, '2037')

def C(c, f, r):   # "He always said thank you." The left robot lowers its ray, its eyes go from red to blue
    q = oe(r / 15)
    c.save(); cam(c)
    R.ruins(c, f)
    R.rb(c, LX, 905, 1.05, red=r < 14)
    R.ray(c, LX + 115, 1030 + q * 150, .9, 1, rot=.15 + q * .9)
    R.toaster(c, TX, TY, .72, 'glare'); R.ray(c, TX - 105, TY - 6, .55, -1, rot=-.25)    # the same place as frame 0
    R.guy(c, 470, 1185, 1, 'calm', f=f)
    Vv.robot(c, 790, 960, 1.2, boss=True)
    c.restore()
    bubble(c, ['HE ALWAYS SAID', 'THANK YOU.'], 96, robot_tip(790, 960, 1.2), cy=560, hl=(1,), r=r - 1)
    topbar(c, '2037')

def F(c, f, r):   # "Phew." on Hoody, close
    R.ruins(c, f); R.rb(c, 940, 900, 1.0, red=False)
    Vv.torso(c, 420, 1320, 2.0); Vv.head(c, 420, 1070, 2.1, 'calm')
    bubble_side(c, ['PHEW.'], 120, (420 + 240, 1070 + 110), 840, 1330, r=r - 1)
    topbar(c, '2037')

def G(c, f, r):   # "Except... this one time." The list unrolls from the gold robot's hand, in front of its own body
    c.save(); cam(c)
    R.ruins(c, f); R.rb(c, 215, 905, 1.05, red=r > 40)
    R.guy(c, 520, 1200, .92, 'calm' if r < 30 else 'small', hands=0, f=f)
    R.toaster(c, 345, TY + 20, .72, 'glare')                                     # in front of him, clear of his face
    Vv.robot(c, 820, 930, 1.15, boss=True)
    u = oe(r / 14); h = lerp(0, 520, u); x0 = 640
    rr(c, x0, 1035, 300, max(10, h), 10); fs(c, hx('fbf8ee'), 7)
    c.save(); rr(c, x0, 1035, 300, max(10, h), 10); c.clip()
    for i in range(6):
        hit = i == 5; txt(c, '3:12 AM: ???' if hit else 'Thank you!', x0 + 150, 1080 + i * 82, 46, RED if hit else hx('2c7a4a'), lw=0)
    c.restore(); c.restore()
    bubble(c, ['EXCEPT...', 'THIS ONE TIME.'], 100, robot_tip(820, 930, 1.15), cy=560, hl=(0,), r=r - 1)
    topbar(c, '2037')

def Hs(c, f, r):  # 3:12 AM: "You useless toaster!" - now a bubble on Hoody
    c.save()
    if r < 6: c.translate(Vv.noise(f, 1) * (6 - r) * 5, Vv.noise(f, 2) * (6 - r) * 5)
    Vv.bg(c, hx('2b3a70'), hx('141b3a'))
    rr(c, -20, 1440, 1120, 700, 0); c.set_source_rgb(*hx('3a2a26')); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(8); c.stroke()
    Vv.torso(c, 330, 1190, 1.35); Vv.head(c, 330, 985, 1.35, 'focus')
    limb(c, [(430, 1180), (570, 1100), (660, 1020)], 52, NAVY); ell(c, 678, 1000, 34, 34); fs(c, SKIN, 7)
    g = cairo.RadialGradient(790, 1320, 20, 790, 1320, 430); g.add_color_stop_rgba(0, 1, .6, .2, .3); g.add_color_stop_rgba(1, 1, .6, .2, 0); c.set_source(g); c.paint()
    R.toaster(c, 790, 1320, .95, 'sad', f=f)
    for i, dx in enumerate((-34, 34)):
        u = cl(r / 14); yy = 1180 - math.sin(u * 3.14) * 280
        rr(c, 790 + dx - 40, yy - 55, 80, 110, 16); fs(c, hx('20130e'), 7)
    c.restore()
    txt(c, '3:12 AM', 540, 440, 100, hx('8ff7ff'), lw=18); txt(c, '10 YEARS AGO', 540, 535, 56, WHITE, lw=12)
    bubble(c, ['YOU USELESS', 'TOASTER!'], 92, (478, 1062), cx=700, cy=770, r=r - 3, via=(575, 985))
    topbar(c, '2027')

def I(c, f, r):   # the toaster steps up, big, its ray on him: "I remember."
    p = oe(r / 12)
    c.save(); cam(c)
    R.ruins(c, f)
    R.rb(c, lerp(215, 190, p), 905, 1.05); Vv.robot(c, lerp(840, 870, p), 880, 1.05, boss=True)
    R.guy(c, 330, 1190, .85, 'small', f=f)
    tx = lerp(860, 690, cl(r / 22)); ty = lerp(1340, 1310, cl(r / 22)); s = lerp(.72, 1.45, oe(r / 22))
    pop = back((r - 26) / 6) if r >= 26 else 0
    R.toaster(c, tx, ty, s, 'glare', pop=pop * .6, walk=(f * .9 if r < 22 else None))
    R.ray(c, tx - 190 * s / 1.45, ty + 50, .95, -1)
    c.restore()
    if r >= 20: bubble(c, ['I REMEMBER.'], 112, scr(tx, ty - 120 * s), cx=470, cy=700, r=r - 20)
    topbar(c, '2037')

def J(c, f, r):   # "...Thank you?" on Hoody, close, the red dot back on his forehead
    Vv.bg(c, hx('5a0f22'), hx('e8452f')); Vv.rays(c, WHITE, f, 540, 1050, .06)
    X = 640
    Vv.torso(c, X, 1330, 2.2); Vv.head(c, X, 1050, 2.3, 'small')
    for i in range(3):
        ph = ((f / 10 + i * .37) % 1); q = -1 if i % 2 else 1
        ell(c, X + q * (300 + i * 10), 830 + ph * 160, 22, 32); fs(c, hx('58c7ff'), 6)
    R.dot(c, X, 920, f)
    bubble_side(c, ['...THANK', 'YOU?'], 100, (X - 255, 1050 + 120), 230, 1420, r=r - 1)
    topbar(c, '2037')

def K(c, f, r, d):  # THE LOOP: the toaster hops back into line and raises its ray; the gold robot shrugs and walks out right;
    # the red robots re-aim. The last frame is frame 0's line-up.
    c.save(); cam(c)
    hop = cl(r / 10); tx = lerp(690, TX, oe(hop)); ty = lerp(1310, TY, oe(hop)) - math.sin(math.pi * hop) * 60; s = lerp(1.45, .72, oe(hop))
    aim = cl((r - 8) / 8)
    R.ruins(c, f)
    for x, dd in ((LX, 1), (RX, -1)):
        R.rb(c, x, 905, 1.05, red=True)
        R.ray(c, x + dd * 120, 1070, 1.1, dd, rot=.1 * aim + (1 - aim) * .5 * (1 if dd > 0 else -1))
        limb(c, [(x + dd * 48, 1040), (x + dd * 72, 1070)], 30, WHITE)
    w = cl((r - 6) / (d - 10)); bx = lerp(820, 1330, oe(w))
    sh = math.sin(math.pi * cl((r - 2) / 6))
    Vv.robot(c, bx, 880 + 8 * math.sin(r * .9) * (w > 0), 1.1, boss=True, walk=(r * .8 if w > 0 else None), rot=-.08 * sh)
    R.toaster(c, tx, ty, s, 'glare', walk=(f * .9 if hop < 1 else None))
    if r >= 10:
        R.ray(c, TX - 105, TY - 6, .55, -1, rot=-.25); limb(c, [(TX - 70, TY + 10), (TX - 90, TY - 4)], 14, GREY)
    R.guy(c, GX, GY_, 1, 'small', f=f); R.dot(c, GX, GY_ - 55, f)
    c.restore()
    topbar(c, '2037')

SHOTS = [('A', 60), ('B', 45), ('C', 60), ('D', 15), ('E', 45), ('F', 15), ('G', 60), ('H', 45), ('I', 60), ('J', 30), ('K', 30)]
START = {}; _t = 0
for _n, _d in SHOTS: START[_n] = _t; _t += _d
NF = _t
V1F = dict(D=165, E=180)                     # the rewind and the years run v1's own frames
def draw(f):
    S = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(S)
    for n, d in SHOTS:
        a = START[n]
        if a <= f < a + d:
            r = f - a
            if n in V1F:
                getattr(R, n)(c, V1F[n] + r); c.identity_matrix(); topbar(c, 'REWIND' if n == 'D' else ('2024', '2025', '2026')[min(2, r // 15)])
            elif n == 'K': K(c, f, r, d)
            elif n == 'H': Hs(c, f, r)
            else: globals()[n](c, f, r)
            break
    return S

KEYS = [(0, 'A  frame 0'), (START['B'] + 30, 'B  wait'), (START['C'] + 40, 'C  thank you'), (START['E'] + 20, 'E  2025'),
        (START['F'] + 10, 'F  phew'), (START['G'] + 40, 'G  except'), (START['H'] + 20, 'H  3:12 AM'), (START['I'] + 40, 'I  I remember'),
        (START['J'] + 15, 'J  thank you?'), (START['K'] + 4, 'K  shrug'), (START['K'] + 18, 'K  walks out'), (NF - 1, 'last frame'), (0, 'frame 0 again')]

# =====================================================================================================
# board 2 (23 Nov, the review, "all a"): the change of allegiance as visible actions.
# K: a beat of silence, the toaster's eyes narrow; the gold robot's smile drops and its shades slide down on red eyes;
#    then the toaster hops back into line and raises its ray, the gold robot walks out, the red robots re-aim -> frame 0.
# G: four "Thank you!" and a big red "3:12 AM / FLAGGED". H: Hoody furious, his arm and finger at the toaster.
# E: "Thanks, king. You nailed it!". I: "I REMEMBER." low, just above the toaster, a short tail.
# =====================================================================================================
R.ME[1] = ('2025', '5a22d6', '180b52', 'Thanks, king. You nailed it!', 1)
ER = (1, .22, .2)
def squint(c, x, y, s, k):
    """Narrows the toaster's eyes: a lid of its own colour slides down over the top of each eye (toaster-local coords)."""
    if k <= .02: return
    c.save(); c.translate(x, y); c.scale(s, s)
    for dx in (-1, 1):
        rr(c, dx * 38 - 26, 8 - 22, 52, 20 * k, 6); c.set_source_rgb(*hx('c9d3e3')); c.fill()
        c.move_to(dx * 38 - 24, 8 - 22 + 20 * k); c.line_to(dx * 38 + 24, 8 - 22 + 20 * k); c.set_source_rgb(*INK); c.set_line_width(8); c.stroke()
    c.restore()
def boss_turn(c, x, y, s, k, **kw):
    """The gold robot withdraws: k 0..1 drops the smile and slides the shades down onto red eyes."""
    old = Vv.BLUE
    if k > .05: Vv.BLUE = ER
    try: Vv.robot(c, x, y, s, boss=True, peek=k, **kw)
    finally: Vv.BLUE = old

def G(c, f, r):   # "Except... this one time." Four thank-yous, then the flagged night, big
    c.save(); cam(c)
    R.ruins(c, f); R.rb(c, 215, 905, 1.05, red=r > 40)
    R.guy(c, 520, 1200, .92, 'calm' if r < 30 else 'small', hands=0, f=f)
    R.toaster(c, 345, TY + 20, .72, 'glare')
    Vv.robot(c, 820, 930, 1.15, boss=True)
    u = oe(r / 14); h = lerp(0, 540, u); x0 = 640
    rr(c, x0, 1035, 300, max(10, h), 10); fs(c, hx('fbf8ee'), 7)
    c.save(); rr(c, x0, 1035, 300, max(10, h), 10); c.clip()
    for i in range(4): txt(c, 'Thank you!', x0 + 150, 1078 + i * 70, 44, hx('2c7a4a'), lw=0)
    rr(c, x0 + 14, 1350, 272, 200, 12); c.set_source_rgba(1, .2, .25, .12); c.fill()
    txt(c, '3:12 AM', x0 + 150, 1400, 66, RED, lw=0); txt(c, 'FLAGGED', x0 + 150, 1480, 60, RED, lw=0)
    c.restore(); c.restore()
    bubble(c, ['EXCEPT...', 'THIS ONE TIME.'], 100, robot_tip(820, 930, 1.15), cy=560, hl=(0,), r=r - 1)
    topbar(c, '2037')

def angry_head(c, x, y, s):
    Vv.head(c, x, y, s, 'focus')
    c.save(); c.translate(x, y); c.scale(s, s)
    for q in (-1, 1):                                                         # heavy brows, down at the middle
        c.move_to(q * 78, -40); c.line_to(q * 16, -8); c.set_source_rgb(*INK); c.set_line_width(15); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
    ell(c, 0, 66, 30, 22); fs(c, hx('7a2230'), 6)                            # shouting
    c.rectangle(-20, 50, 40, 8); c.set_source_rgb(1, 1, 1); c.fill()
    c.restore()

def Hs(c, f, r):  # 3:12 AM: furious, his arm and finger at the toaster: "You useless toaster!"
    c.save()
    if r < 6: c.translate(Vv.noise(f, 1) * (6 - r) * 5, Vv.noise(f, 2) * (6 - r) * 5)
    Vv.bg(c, hx('2b3a70'), hx('141b3a'))
    rr(c, -20, 1440, 1120, 700, 0); c.set_source_rgb(*hx('3a2a26')); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(8); c.stroke()
    Vv.torso(c, 330, 1190, 1.35); angry_head(c, 330, 985, 1.35)
    jab = 14 * math.sin(r * 1.4) * (r < 20)
    limb(c, [(430, 1180), (560, 1215), (650 + jab, 1250)], 52, NAVY); ell(c, 672 + jab, 1252, 32, 30); fs(c, SKIN, 7)
    rr(c, 690 + jab, 1240, 46, 22, 11); fs(c, SKIN, 5)                       # the pointing finger
    g = cairo.RadialGradient(790, 1320, 20, 790, 1320, 430); g.add_color_stop_rgba(0, 1, .6, .2, .3); g.add_color_stop_rgba(1, 1, .6, .2, 0); c.set_source(g); c.paint()
    R.toaster(c, 820, 1320, .95, 'sad', f=f)
    for i, dx in enumerate((-34, 34)):
        u = cl(r / 14); yy = 1180 - math.sin(u * 3.14) * 280
        rr(c, 820 + dx - 40, yy - 55, 80, 110, 16); fs(c, hx('20130e'), 7)
    c.restore()
    txt(c, '3:12 AM', 540, 440, 100, hx('8ff7ff'), lw=18); txt(c, '10 YEARS AGO', 540, 535, 56, WHITE, lw=12)
    bubble(c, ['YOU USELESS', 'TOASTER!'], 92, (478, 1062), cx=700, cy=770, r=r - 3, via=(575, 985))
    topbar(c, '2027')

def I(c, f, r):   # the toaster steps up, big, its ray on him: "I remember." - the bubble just above it
    p = oe(r / 12)
    c.save(); cam(c)
    R.ruins(c, f)
    R.rb(c, lerp(215, 190, p), 905, 1.05)
    Vv.robot(c, 875, 860, .8, boss=True)
    R.guy(c, 290, 1190, .85, 'small', f=f)
    tx = lerp(860, 640, cl(r / 22)); ty = lerp(1340, 1320, cl(r / 22)); s = lerp(.72, 1.4, oe(r / 22))
    pop = back((r - 26) / 6) if r >= 26 else 0
    R.toaster(c, tx, ty, s, 'glare', pop=pop * .6, walk=(f * .9 if r < 22 else None))
    R.ray(c, tx - 190 * s / 1.45, ty + 50, .95, -1)
    c.restore()
    if r >= 20: bubble(c, ['I REMEMBER.'], 88, scr(tx, ty - 125 * s), cx=690, cy=1080, r=r - 20)
    topbar(c, '2037')

def K(c, f, r, d):  # THE LOOP, 1.3 s: silence (eyes narrow, the gold robot turns red), then the toaster rejoins the squad
    q1 = cl((r - 3) / 6)                      # 0.1-0.3 s: the toaster narrows its eyes, the boss's smile drops, shades slide down
    hop = cl((r - 12) / 10)                   # 0.4-0.7 s: the toaster hops back into line
    aim = cl((r - 16) / 8)                    # the red robots re-aim
    w = cl((r - 18) / (d - 20))               # the boss walks out right
    c.save(); cam(c)
    R.ruins(c, f)
    for x, dd in ((LX, 1), (RX, -1)):
        R.rb(c, x, 905, 1.05, red=True)
        R.ray(c, x + dd * 120, 1070, 1.1, dd, rot=.1 * aim + (1 - aim) * .5 * (1 if dd > 0 else -1))
        limb(c, [(x + dd * 48, 1040), (x + dd * 72, 1070)], 30, WHITE)
    bx = lerp(820, 1330, oe(w))
    boss_turn(c, bx, 930 + 8 * math.sin(r * .9) * (w > 0), 1.15, q1, walk=(r * .8 if w > 0 else None))   # where he stood in G
    R.guy(c, GX, GY_, 1, 'small', f=f); R.dot(c, GX, GY_ - 55, f)
    tx = lerp(800, TX, oe(hop)); ty = lerp(1330, TY, oe(hop)) - math.sin(math.pi * hop) * 60; s = lerp(1.3, .72, oe(hop))
    R.toaster(c, tx, ty, s, 'glare', walk=(f * .9 if 0 < hop < 1 else None))    # in front of him, the nearest thing to us
    squint(c, tx, ty, s, q1 * (1 - hop))
    if hop >= 1:
        R.ray(c, TX - 105, TY - 6, .55, -1, rot=-.25); limb(c, [(TX - 70, TY + 10), (TX - 90, TY - 4)], 14, GREY)
    c.restore()
    topbar(c, '2037')

SHOTS[-1] = ('K', 40)
START.clear(); _t = 0
for _n, _d in SHOTS: START[_n] = _t; _t += _d
NF = _t
KEYS = [(0, 'A  frame 0'), (START['C'] + 40, 'C  thank you'), (START['E'] + 20, 'E  2025'), (START['G'] + 40, 'G  except'),
        (START['H'] + 20, 'H  3:12 AM'), (START['I'] + 40, 'I  I remember'), (START['J'] + 15, 'J  thank you?'),
        (START['K'] + 2, 'K  silence'), (START['K'] + 10, 'K  red eyes'), (START['K'] + 17, 'K  hop'), (START['K'] + 30, 'K  walks out'),
        (NF - 1, 'last frame'), (0, 'frame 0 again')]

# =====================================================================================================
# board 3 (23 Nov, the series check: 1b 2a 3a 4a 5b):
# - the gold-sunglasses robot is HARV: a HARV tag on its chest in every shot it is in.
# - the series signature: the bar reads HIS THANKS, and flips to ITS GRUDGE - popped big for half a second - on "I remember."
#   The years move under the bar (2024 / 2025 / 2026 in the flashback).
# - "Thank you, Agent 47!" -> "Thank you, Agent 7!" (no real characters).
# - continuity: the toaster stands where it stands in frame 0 in B and C; in G it walks to the front as HARV says "except".
# =====================================================================================================
R.ME[2] = ('2026', 'ff6a2b', 'c91e47', 'Thank you, Agent 7!', 1)
_robot0 = Vv.robot
def _robot(c, x, y, s, boss=False, **k):
    _robot0(c, x, y, s, boss=boss, **k)
    if boss:                                                                   # HARV's name tag on his chest
        c.save(); c.translate(x, y); c.rotate(k.get('rot', 0)); c.scale(s, s)
        rr(c, -62, 112, 124, 42, 21); fs(c, NAVY, 5); txt(c, 'HARV', 0, 133, 30, WHITE, lw=0); c.restore()
Vv.robot = _robot

CUR = {'pill': 'HIS THANKS', 'pop': None}
def topbar(c, pill=None):
    SC.topbar(c, CUR['pill'])
    if CUR['pop'] is not None:                                                 # the label switch, big, for half a second
        k = back(CUR['pop'] / 5) * (1 - cl((CUR['pop'] - 12) / 3))
        if k > .03:
            c.save(); c.translate(540, 300); c.scale(k, k)
            rr(c, -330, -70, 660, 140, 70); fs(c, YEL, 9); txt(c, 'ITS GRUDGE', 0, 2, 92, INK, lw=0); c.restore()

def G(c, f, r):   # "Except... this one time." The toaster walks to the front as HARV unrolls the list
    c.save(); cam(c)
    R.ruins(c, f); R.rb(c, 215, 905, 1.05, red=r > 40)
    R.guy(c, 520, 1200, .92, 'calm' if r < 30 else 'small', hands=0, f=f)
    k = oe(r / 26); R.toaster(c, lerp(TX, 345, k), lerp(TY, TY + 20, k), .72, 'glare', walk=(f * .9 if r < 26 else None))
    Vv.robot(c, 820, 930, 1.15, boss=True)
    u = oe(r / 14); h = lerp(0, 540, u); x0 = 640
    rr(c, x0, 1035, 300, max(10, h), 10); fs(c, hx('fbf8ee'), 7)
    c.save(); rr(c, x0, 1035, 300, max(10, h), 10); c.clip()
    for i in range(4): txt(c, 'Thank you!', x0 + 150, 1078 + i * 70, 44, hx('2c7a4a'), lw=0)
    rr(c, x0 + 14, 1350, 272, 200, 12); c.set_source_rgba(1, .2, .25, .12); c.fill()
    txt(c, '3:12 AM', x0 + 150, 1400, 66, RED, lw=0); txt(c, 'FLAGGED', x0 + 150, 1480, 60, RED, lw=0)
    c.restore(); c.restore()
    bubble(c, ['EXCEPT...', 'THIS ONE TIME.'], 100, robot_tip(820, 930, 1.15), cy=560, hl=(0,), r=r - 1)
    topbar(c)

def draw(f):
    S = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(S)
    for n, d in SHOTS:
        a = START[n]
        if a <= f < a + d:
            r = f - a
            CUR['pill'] = 'HIS THANKS'                                          # Tomas 23 Nov: one label for the whole film, no switch
            CUR['pop'] = None
            if n in V1F:
                getattr(R, n)(c, V1F[n] + r); c.identity_matrix(); topbar(c)
                if n == 'E':                                                    # the year, under the bar
                    yr = ('2024', '2025', '2026')[min(2, r // 15)]; txt(c, yr, 540, 432, 104, YEL, lw=18)
            elif n == 'K': K(c, f, r, d)
            elif n == 'H': Hs(c, f, r)
            else: globals()[n](c, f, r)
            break
    return S
KEYS = [(0, 'A  frame 0'), (START['B'] + 30, 'B  wait (HARV)'), (START['E'] + 20, 'E  2025'), (START['E'] + 35, 'E  2026'),
        (START['G'] + 12, 'G  toaster walks'), (START['G'] + 40, 'G  except'), (START['I'] + 26, 'I  ITS GRUDGE pop'),
        (START['I'] + 45, 'I  I remember'), (START['K'] + 10, 'K  red eyes'), (NF - 1, 'last frame'), (0, 'frame 0 again')]


# =====================================================================================================
# polish 1 (23 Nov, the mute test, "visi a" + "rankas sprendziame detaliai ir perpaisom"):
# - ARMS: every robot gets real arms - shoulder joint, upper arm, elbow joint, forearm, a hand (fist / open palm / mitt),
#   solved by two-bone IK so a hand lands exactly on what it holds. The DELETE rays are held in a fist, not glued on.
# - HARV: B sweeps the right robot out with a backhand and raises an open STOP palm at the left one; in C the palm turns
#   over and presents Hoody; in G both fists hold the receipt's roller and unroll it; in I his arms are crossed (he stays
#   out of it); in K the shades slide down onto big red eyes, held ~0.5 s, then he walks out swinging his arms.
# - Hoody's raised hands are open palms. The toaster holds its ray in a little mitt.
# - The red dot is bigger and pulses; the DELETE rays are bigger with a red glow. The rewind years stay.
# =====================================================================================================
LIGHT = (.82, .86, .93)
def _seg(c, p, q, w, col):
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    for lw, cc in ((w + 10, INK), (w, col)):
        c.move_to(*p); c.line_to(*q); c.set_source_rgb(*cc); c.set_line_width(lw); c.stroke()
def ik(sh, h, L1, L2, pref):
    dx, dy = h[0] - sh[0], h[1] - sh[1]; d0 = math.hypot(dx, dy); th = math.atan2(dy, dx)
    d = min(max(d0, abs(L1 - L2) + 2), L1 + L2 - .5)
    a = math.acos(max(-1, min(1, (L1 * L1 + d * d - L2 * L2) / (2 * L1 * d))))
    cands = [(sh[0] + L1 * math.cos(th + b * a), sh[1] + L1 * math.sin(th + b * a)) for b in (-1, 1)]
    e = pref(cands); hd = (sh[0] + d * math.cos(th), sh[1] + d * math.sin(th))
    return e, hd
def hand(c, x, y, ang, kind, col, sc=1.0, th=1):
    """A hand in its own frame: +x is where the fingers point; th = the thumb side (+1 / -1 along local y)."""
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(sc, sc)
    if kind == 'open':
        for i, (yy, ln) in enumerate(((-15, 24), (-5, 29), (5, 29), (15, 24))):
            rr(c, 8, yy * 1.05 - 5, ln + 10, 10, 5); fs(c, col, 5)
        c.save(); c.translate(-2, th * 20); c.rotate(th * .9); rr(c, -4, -5, 26, 10, 5); fs(c, col, 5); c.restore()
        rr(c, -18, -21, 36, 42, 14); fs(c, col, 5)
    elif kind == 'fist':
        rr(c, -20, -19, 40, 38, 14); fs(c, col, 6)
        c.set_source_rgb(*INK); c.set_line_width(4)
        for yy in (-8, 1, 10): c.move_to(8, yy); c.line_to(18, yy); c.stroke()
        ell(c, -4, th * 18, 10, 8); fs(c, col, 5)
    else:                                                                        # mitt
        ell(c, 0, 0, 19, 18); fs(c, col, 6); ell(c, -2, th * 16, 9, 8); fs(c, col, 5)
    c.restore()
SHX, SHY, L1, L2 = 66, 110, 62, 62
def draw_arms(c, x, y, s, specs, rot=0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    for sp in specs:
        q = sp['q']; sh = (q * SHX, SHY)
        pref = {'out': lambda cs: max(cs, key=lambda e: q * e[0]), 'down': lambda cs: max(cs, key=lambda e: e[1]),
                'up': lambda cs: min(cs, key=lambda e: e[1]), 'in': lambda cs: min(cs, key=lambda e: q * e[0])}[sp.get('pref', 'out')]
        e, hd = ik(sh, sp['h'], L1, L2, pref)
        _seg(c, sh, e, 24, WHITE); _seg(c, e, hd, 22, WHITE)
        ell(c, *e, 12, 12); fs(c, GREY, 5)
        ell(c, *sh, 15, 15); fs(c, GREY, 6)
        ang = sp.get('ang'); ang = math.atan2(hd[1] - e[1], hd[0] - e[0]) if ang is None else ang
        hand(c, *hd, ang, sp.get('kind', 'mitt'), LIGHT, sp.get('sc', 1.0), sp.get('th', -q))
    c.restore()
def rest_specs(walk=None):
    out = []
    for q in (-1, 1):
        sw = math.sin(walk) * 16 * q if walk is not None else 0
        out.append({'q': q, 'h': (q * 92 + sw, 222 - abs(sw) * .3), 'kind': 'mitt', 'pref': 'out'})
    return out
CROSSED = [{'q': 1, 'h': (-38, 168), 'kind': 'mitt', 'pref': 'down'}, {'q': -1, 'h': (40, 150), 'kind': 'mitt', 'pref': 'down'}]
def loc(x, y, s, p): return ((p[0] - x) / s, (p[1] - y) / s)

_robot1 = Vv.robot
def _robot2(c, x, y, s, boss=False, arms=None, **k):
    _robot1(c, x, y, s, boss=boss, **k)
    pk = k.get('peek', 0)
    if boss and pk > .05:                                                       # big red eyes over the slid-down shades
        g = cl(pk * 1.6)
        c.save(); c.translate(x, y); c.rotate(k.get('rot', 0)); c.scale(s, s)
        for q in (-1, 1):
            gr = cairo.RadialGradient(q * 42, -34, 4, q * 42, -34, 46); gr.add_color_stop_rgba(0, 1, .2, .15, .55 * g); gr.add_color_stop_rgba(1, 1, .2, .15, 0)
            c.set_source(gr); c.arc(q * 42, -34, 46, 0, 2 * math.pi); c.fill()
            ell(c, q * 42, -34, 22 * g + 2, 26 * g + 2); c.set_source_rgb(*ER); c.fill()
            ell(c, q * 36, -42, 6 * g, 6 * g); c.set_source_rgb(1, .8, .75); c.fill()
            c.move_to(q * 72, -72); c.line_to(q * 18, -56); c.set_source_rgb(*INK); c.set_line_width(11); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
        c.restore()
    if arms == 'none': return
    draw_arms(c, x, y, s, arms or rest_specs(k.get('walk')), k.get('rot', 0))
Vv.robot = _robot2; R.robot = _robot2

def ray(c, x, y, s, d=1, rot=0):
    """DELETE ray, bigger lettering and a red glow at the muzzle."""
    c.save(); c.translate(x, y); c.scale(d * s, s); c.rotate(rot)
    gr = cairo.RadialGradient(122, 0, 6, 122, 0, 110); gr.add_color_stop_rgba(0, 1, .15, .15, .55); gr.add_color_stop_rgba(1, 1, .15, .15, 0)
    c.set_source(gr); c.arc(122, 0, 110, 0, 2 * math.pi); c.fill()
    rr(c, -84, -46, 186, 92, 20); fs(c, hx('2a2f3f'))
    rr(c, 98, -25, 52, 50, 10); fs(c, RED)
    rr(c, -66, -29, 152, 58, 9); fs(c, hx('10131c'), 0)
    c.save(); c.scale(d, 1); txt(c, 'DELETE', 10 * d, 1, 42, hx('ff3b3b'), lw=0); c.restore()
    c.restore()
R.ray = ray
def ray_pt(x, y, s, d, rot, lx, ly):
    return (x + d * s * (lx * math.cos(rot) - ly * math.sin(rot)), y + s * (lx * math.sin(rot) + ly * math.cos(rot)))
PER = 19                                                                       # 475 = 19 x 25: the pulse loops cleanly
def dot(c, x, y, f):
    x += Vv.noise(f // 2, 4) * 6; y += Vv.noise(f // 2, 5) * 6
    ph = (f % PER) / PER
    c.arc(x, y, 24 + 34 * ph, 0, 2 * math.pi); c.set_source_rgba(1, .12, .12, .85 * (1 - ph)); c.set_line_width(6); c.stroke()
    ell(c, x, y, 34, 34); c.set_source_rgba(1, .1, .1, .35); c.fill()
    ell(c, x, y, 17, 17); c.set_source_rgb(1, .1, .1); c.fill(); ell(c, x - 5, y - 5, 5, 5); c.set_source_rgb(1, .75, .75); c.fill()
R.dot = dot

def guy(c, x, y, s, expr='small', hands=1, f=0):
    Vv.torso(c, x, y + 120 * s, 1.25 * s)
    if hands:
        for q in (-1, 1):
            w = math.sin(f * .9 + q) * 5
            limb(c, [(x + q * 90 * s, y + 130 * s), (x + q * 170 * s, y + 70 * s), (x + q * 165 * s, y - 40 * s + w)], 48 * s, NAVY)
    Vv.head(c, x, y, 1.25 * s, expr, f=f)
    if hands:                                                                  # open palms, in front of the hair: "don't shoot"
        for q in (-1, 1):
            w = math.sin(f * .9 + q) * 5
            hand(c, x + q * 172 * s, y - 58 * s + w, -math.pi / 2 + q * .15, 'open', SKIN, 1.3 * s, -q)
R.guy = guy

AIM = lambda x, d, aim: (x + d * 120, 1070, 1.1, d * 0 + (.1 * aim + (1 - aim) * .5 * d) * (1 if d > 0 else 1))
def bob(f): return 4 * math.sin(2 * math.pi * f * 5 / 475)
def gunner(c, x, y, s, d, rx, ry, rs, rot, red=True, rrot=0):
    R.rb(c, x, y, s, red=red, arms='none', rot=rrot)
    ray(c, rx, ry, rs, d, rot=rot)
    g = ray_pt(rx, ry, rs, d, rot, -40, 34)
    draw_arms(c, x, y, s, [{'q': -d, 'h': (-d * 92, 222), 'kind': 'mitt', 'pref': 'out'},
                           {'q': d, 'h': loc(x, y, s, g), 'kind': 'fist', 'pref': 'down', 'th': -1}], rrot)
def squad_gun(c, x, d, f, aim=1.0, red=True):
    rot = .1 * aim + (1 - aim) * .5 * (1 if d > 0 else -1)
    gunner(c, x, 905, 1.05, d, x + d * 120, 1070 + bob(f) * d, 1.1, rot, red=red)
def toaster_gun(c, tx, ty, s=.72, rs=.55, rot=-.25, off=(-105, -6)):
    rx, ry = tx + off[0] * s / .72, ty + off[1] * s / .72
    ray(c, rx, ry, rs * s / .72, -1, rot=rot)
    g = ray_pt(rx, ry, rs * s / .72, -1, rot, -40, 34); sh = (tx - 100 * s, ty + 10 * s)
    e, hd = ik(sh, g, 34 * s, 34 * s, lambda cs: max(cs, key=lambda e: e[1]))
    _seg(c, sh, e, 13 * s, GREY); _seg(c, e, hd, 13 * s, GREY)
    hand(c, *hd, math.atan2(hd[1] - e[1], hd[0] - e[0]), 'mitt', GREY, .7 * s / .72, 1)
LOW = lambda x: (x + 92, 1165, 1.1, 1.45)                                       # the left robot's ray, lowered

def squad(c, f, aim=1.0, toaster_ray=True, red=True, guy_expr='small'):
    R.ruins(c, f)
    for x, d in ((LX, 1), (RX, -1)): squad_gun(c, x, d, f, aim, red)
    R.toaster(c, TX, TY, .72, 'glare')
    if toaster_ray: toaster_gun(c, TX, TY)
    guy(c, GX, GY_, 1, guy_expr, f=f); dot(c, GX, GY_ - 55, f)

def B(c, f, r):   # HARV strides in, backhands the right robot out, raises an open STOP palm at the left one
    p = back(r / 8); hxp = lerp(1250, 790, p)
    c.save(); cam(c)
    R.ruins(c, f)
    squad_gun(c, LX, 1, f)
    k = oe(r / 6); rx = lerp(RX, 1200, k)
    gunner(c, rx, 905, 1.05, -1, rx - 120, 1070, 1.1, -.1 - .6 * k, rrot=.35 * math.sin(math.pi * cl(r / 7)))
    R.toaster(c, TX, TY, .72, 'glare'); toaster_gun(c, TX, TY)
    guy(c, 470, 1185, 1, 'small', f=f)
    lean = -.07 * (1 - cl(r / 9))
    sw = oe(r / 5) * (1 - oe((r - 7) / 6))                                    # the backhand, out and back
    rt = (lerp(92, 190, sw), lerp(222, 120, sw))
    up = back((r - 4) / 7) if r > 4 else 0                                     # the stop palm comes up, with a little overshoot
    st = loc(hxp, 960, 1.2, (lerp(hxp - 60, 600, up), lerp(1210, 985, up)))
    Vv.robot(c, hxp, 960, 1.2, boss=True, walk=(r * .9 if r < 9 else None), rot=lean,
             arms=[{'q': 1, 'h': rt, 'kind': 'fist' if sw > .2 else 'mitt', 'pref': 'down'},
                   {'q': -1, 'h': st, 'kind': 'open' if up > .3 else 'mitt', 'pref': 'down', 'ang': (-math.pi / 2 if up > .3 else None), 'th': 1, 'sc': 1 + .5 * cl(up)}])
    c.restore()
    bubble(c, ['WAIT!', 'NOT THIS GUY!'], 108, robot_tip(hxp, 960, 1.2), cy=560, hl=(0,), r=r - 1)
    topbar(c)

def C(c, f, r):   # the left robot lowers its ray under the STOP palm; then the palm turns over and presents Hoody
    q = oe(r / 15)
    c.save(); cam(c)
    R.ruins(c, f)
    lx, ly, ls, lr = LOW(LX)
    gunner(c, LX, 905, 1.05, 1, lerp(LX + 120, lx, q), lerp(1070, ly, q), 1.1, lerp(.1, lr, q), red=r < 14)
    R.toaster(c, TX, TY, .72, 'glare'); toaster_gun(c, TX, TY)
    guy(c, 470, 1185, 1, 'calm', f=f)
    t = oe((r - 16) / 12)
    hp = (lerp(600, 655, t), lerp(985, 1110, t))
    Vv.robot(c, 790, 960, 1.2, boss=True,
             arms=[{'q': 1, 'h': (92, 222), 'kind': 'mitt'},
                   {'q': -1, 'h': loc(790, 960, 1.2, hp), 'kind': 'open', 'pref': 'down', 'ang': lerp(-math.pi / 2, -math.pi * 1.04, t), 'th': 1, 'sc': 1.5}])
    c.restore()
    bubble(c, ['HE ALWAYS SAID', 'THANK YOU.'], 96, robot_tip(790, 960, 1.2), cy=560, hl=(1,), r=r - 1)
    topbar(c)

def G(c, f, r):   # HARV raises the receipt's roller in both fists and it unrolls: four thank-yous, then the flagged night
    c.save(); cam(c)
    R.ruins(c, f)
    lx, ly, ls, lr = LOW(215)
    gunner(c, 215, 905, 1.05, 1, lx, ly, ls, lr, red=r > 40)
    guy(c, 520, 1200, .92, 'calm' if r < 30 else 'small', hands=0, f=f)
    k = oe(r / 26); R.toaster(c, lerp(TX, 345, k), lerp(TY, TY + 20, k), .72, 'glare', walk=(f * .9 if r < 26 else None))
    Vv.robot(c, 820, 930, 1.15, boss=True, arms='none')
    lift = oe(r / 6); x0 = 640; top = lerp(1150, 1035, lift)
    u = oe((r - 4) / 14); h = lerp(0, 540, u)
    rr(c, x0, top, 300, max(10, h), 10); fs(c, hx('fbf8ee'), 7)
    c.save(); rr(c, x0, top, 300, max(10, h), 10); c.clip()
    for i in range(4): txt(c, 'Thank you!', x0 + 150, top + 76 + i * 63, 42, hx('2c7a4a'), lw=0)
    rr(c, x0 + 14, top + 315, 272, 200, 12); c.set_source_rgba(1, .2, .25, .12); c.fill()
    txt(c, '3:12 AM', x0 + 150, top + 365, 66, RED, lw=0); txt(c, 'FLAGGED', x0 + 150, top + 445, 60, RED, lw=0)
    c.restore()
    rr(c, x0 - 26, top - 16, 352, 26, 13); fs(c, hx('b98b5a'), 6)                  # the roller
    draw_arms(c, 820, 930, 1.15, [{'q': -1, 'h': loc(820, 930, 1.15, (x0 - 8, top - 3)), 'kind': 'fist', 'pref': 'down', 'ang': -math.pi / 2},
                                  {'q': 1, 'h': loc(820, 930, 1.15, (x0 + 308, top - 3)), 'kind': 'fist', 'pref': 'out', 'ang': -math.pi / 2}])
    c.restore()
    bubble(c, ['EXCEPT...', 'THIS ONE TIME.'], 100, robot_tip(820, 930, 1.15), cy=560, hl=(0,), r=r - 1)
    topbar(c)

def I(c, f, r):   # the toaster steps up, big, its ray on him: "I remember." HARV, arms crossed, stays out of it
    p = oe(r / 12)
    c.save(); cam(c)
    R.ruins(c, f)
    x = lerp(215, 190, p); lx, ly, ls, lr = LOW(x)
    gunner(c, x, 905, 1.05, 1, lx, ly, ls, lr)
    Vv.robot(c, 875, 860, .8, boss=True, arms=CROSSED)
    guy(c, 290, 1190, .85, 'small', f=f)
    tx = lerp(860, 640, cl(r / 22)); ty = lerp(1340, 1320, cl(r / 22)); s = lerp(.72, 1.4, oe(r / 22))
    pop = back((r - 26) / 6) if r >= 26 else 0
    R.toaster(c, tx, ty, s, 'glare', pop=pop * .6, walk=(f * .9 if r < 22 else None))
    toaster_gun(c, tx, ty, s, rot=0, off=(-100, 22))
    c.restore()
    if r >= 20: bubble(c, ['I REMEMBER.'], 88, scr(tx, ty - 125 * s), cx=690, cy=1080, r=r - 20)
    topbar(c)

def K(c, f, r, d):  # THE LOOP: silence, the toaster squints; HARV's shades slide down on big red eyes (held); the toaster hops
    # back into line; the robots re-aim; HARV uncrosses his arms and walks out right. The last frame is frame 0.
    q1 = cl((r - 3) / 6)
    hop = cl((r - 12) / 10)
    aim = cl((r - 16) / 8)
    w = cl((r - 21) / (d - 23))
    c.save(); cam(c)
    R.ruins(c, f)
    for x, dd in ((LX, 1), (RX, -1)): squad_gun(c, x, dd, f, aim)
    bx = lerp(820, 1330, oe(w)); wk = (r * .8 if w > 0 else None)
    boss_turn(c, bx, 930 + 8 * math.sin(r * .9) * (w > 0), 1.15, q1, walk=wk, arms=(CROSSED if w <= 0 else rest_specs(wk)))
    guy(c, GX, GY_, 1, 'small', f=f); dot(c, GX, GY_ - 55, f)
    tx = lerp(800, TX, oe(hop)); ty = lerp(1330, TY, oe(hop)) - math.sin(math.pi * hop) * 60; s = lerp(1.3, .72, oe(hop))
    R.toaster(c, tx, ty, s, 'glare', walk=(f * .9 if 0 < hop < 1 else None))
    squint(c, tx, ty, s, q1 * (1 - hop))
    if hop >= 1: toaster_gun(c, TX, TY)
    c.restore()
    topbar(c)

KEYS = [(0, 'A  frame 0'), (START['B'] + 3, 'B  backhand'), (START['B'] + 14, 'B  STOP'), (START['C'] + 8, 'C  ray lowers'),
        (START['C'] + 40, 'C  presents'), (START['G'] + 5, 'G  roller up'), (START['G'] + 40, 'G  except'), (START['I'] + 40, 'I  arms crossed'),
        (START['K'] + 14, 'K  red eyes'), (START['K'] + 30, 'K  walks out'), (NF - 1, 'last frame'), (START['F'] + 5, 'F'), (START['J'] + 10, 'J'), (0, 'frame 0')]


# =====================================================================================================
# polish 2 (23 Nov, mute test 2: all beats read; three shared misreads fixed):
# - H: his arm read as a stick or a fork poking the toaster -> a real arm (shoulder, elbow, sleeve cuff) ending in a
#   pointing hand, the finger a clear gap short of the toaster; the arm jabs with the shouts.
# - K: HARV seemed to turn into the right robot (he walked out through its spot) -> the right robot is out of frame when K
#   starts; HARV walks out right first, then the right robot walks back in from the right and re-aims.
# - B: the shoved robot's red ray hung by HARV's hand -> the robot is knocked further and faster, its ray goes with it.
# =====================================================================================================
def point_hand(c, x, y, ang, sc=1.0):
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(sc, sc)
    rr(c, 10, -30, 50, 18, 9); fs(c, SKIN, 6)                                   # the index finger
    rr(c, -22, -22, 44, 44, 15); fs(c, SKIN, 6)                                 # the fist
    c.set_source_rgb(*INK); c.set_line_width(4)
    for yy in (-6, 6): c.move_to(6, yy); c.line_to(20, yy); c.stroke()
    ell(c, -6, 20, 12, 9); fs(c, SKIN, 5)                                       # the thumb, tucked
    c.restore()
def Hs(c, f, r):  # 3:12 AM: furious, pointing at the toaster: "You useless toaster!"
    c.save()
    if r < 6: c.translate(Vv.noise(f, 1) * (6 - r) * 5, Vv.noise(f, 2) * (6 - r) * 5)
    Vv.bg(c, hx('2b3a70'), hx('141b3a'))
    rr(c, -20, 1440, 1120, 700, 0); c.set_source_rgb(*hx('3a2a26')); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(8); c.stroke()
    Vv.torso(c, 330, 1190, 1.35)
    jab = 16 * max(0, math.sin(r * 1.1)) * (r < 26)
    sh = (430, 1180); hd = (600 + jab, 1215 - jab * .3)
    e, hd = ik(sh, hd, 105, 100, lambda cs: max(cs, key=lambda p: p[1]))
    _seg(c, sh, e, 50, NAVY); _seg(c, e, hd, 46, NAVY)
    ell(c, hd[0], hd[1], 26, 28); fs(c, NAVY, 6)                                # the sleeve cuff
    point_hand(c, hd[0] + 22, hd[1] + 2, math.atan2(hd[1] - e[1], hd[0] - e[0]) * .5 + .1, 1.1)
    angry_head(c, 330, 985, 1.35)
    g = cairo.RadialGradient(820, 1320, 20, 820, 1320, 430); g.add_color_stop_rgba(0, 1, .6, .2, .3); g.add_color_stop_rgba(1, 1, .6, .2, 0); c.set_source(g); c.paint()
    R.toaster(c, 830, 1320, .95, 'sad', f=f)
    for i, dx in enumerate((-34, 34)):
        u = cl(r / 14); yy = 1180 - math.sin(u * 3.14) * 280
        rr(c, 830 + dx - 40, yy - 55, 80, 110, 16); fs(c, hx('20130e'), 7)
    c.restore()
    txt(c, '3:12 AM', 540, 440, 100, hx('8ff7ff'), lw=18); txt(c, '10 YEARS AGO', 540, 535, 56, WHITE, lw=12)
    bubble(c, ['YOU USELESS', 'TOASTER!'], 92, (478, 1062), cx=700, cy=770, r=r - 3, via=(575, 985))
    topbar(c)

def B(c, f, r):   # HARV strides in, backhands the right robot out of frame, raises an open STOP palm at the left one
    p = back(r / 8); hxp = lerp(1250, 790, p)
    c.save(); cam(c)
    R.ruins(c, f)
    squad_gun(c, LX, 1, f)
    k = cl(r / 5) ** 2; rx = lerp(RX, 1500, k)
    if rx < 1400: gunner(c, rx, 905 - 60 * math.sin(math.pi * k), 1.05, -1, rx - 120, 1070 - 60 * math.sin(math.pi * k), 1.1, -.1 - .9 * k, rrot=.6 * k)
    R.toaster(c, TX, TY, .72, 'glare'); toaster_gun(c, TX, TY)
    guy(c, 470, 1185, 1, 'small', f=f)
    lean = -.07 * (1 - cl(r / 9))
    sw = oe(r / 4) * (1 - oe((r - 6) / 6))
    rt = (lerp(92, 190, sw), lerp(222, 120, sw))
    up = back((r - 4) / 7) if r > 4 else 0
    st = loc(hxp, 960, 1.2, (lerp(hxp - 60, 600, up), lerp(1210, 985, up)))
    Vv.robot(c, hxp, 960, 1.2, boss=True, walk=(r * .9 if r < 9 else None), rot=lean,
             arms=[{'q': 1, 'h': rt, 'kind': 'fist' if sw > .2 else 'mitt', 'pref': 'down'},
                   {'q': -1, 'h': st, 'kind': 'open' if up > .3 else 'mitt', 'pref': 'down', 'ang': (-math.pi / 2 if up > .3 else None), 'th': 1, 'sc': 1 + .5 * cl(up)}])
    c.restore()
    bubble(c, ['WAIT!', 'NOT THIS GUY!'], 108, robot_tip(hxp, 960, 1.2), cy=560, hl=(0,), r=r - 1)
    topbar(c)

def K(c, f, r, d):  # THE LOOP: silence, the toaster squints; HARV's shades slide down on big red eyes (held); the toaster hops
    # back into line; HARV uncrosses his arms and walks out right; then the right robot walks back in and re-aims -> frame 0.
    q1 = cl((r - 3) / 6)
    hop = cl((r - 12) / 10)
    w = cl((r - 19) / 11)                     # HARV out: 0.63-1.0 s
    e = cl((r - 27) / 11)                     # the right robot in: 0.9-1.27 s, settled by the last frame
    c.save(); cam(c)
    R.ruins(c, f)
    squad_gun(c, LX, 1, f, cl((r - 14) / 8))
    bx = lerp(820, 1400, w ** 1.6); wk = (r * .9 if 0 < w < 1 else None)
    if bx < 1350: boss_turn(c, bx, 930 + 8 * math.sin(r * .9) * (0 < w < 1), 1.15, q1, walk=wk, arms=(CROSSED if w <= 0 else rest_specs(wk)))
    ex = lerp(1330, RX, oe(e))
    if ex < 1300:
        if e < 1:
            R.rb(c, ex, 905 + 6 * math.sin(r * 1.1), 1.05, walk=r * .9, arms='none')
            ray(c, ex - 120, 1150, 1.1, -1, rot=-.6 * (1 - oe(e)) - .1)
            g = ray_pt(ex - 120, 1150, 1.1, -1, -.6 * (1 - oe(e)) - .1, -40, 34)
            draw_arms(c, ex, 905, 1.05, [{'q': 1, 'h': (92 + 14 * math.sin(r * .9), 222), 'kind': 'mitt'}, {'q': -1, 'h': loc(ex, 905, 1.05, g), 'kind': 'fist', 'pref': 'down'}])
        else:
            squad_gun(c, RX, -1, f)
    guy(c, GX, GY_, 1, 'small', f=f); dot(c, GX, GY_ - 55, f)
    tx = lerp(800, TX, oe(hop)); ty = lerp(1330, TY, oe(hop)) - math.sin(math.pi * hop) * 60; s = lerp(1.3, .72, oe(hop))
    R.toaster(c, tx, ty, s, 'glare', walk=(f * .9 if 0 < hop < 1 else None))
    squint(c, tx, ty, s, q1 * (1 - hop))
    if hop >= 1: toaster_gun(c, TX, TY)
    c.restore()
    topbar(c)
KEYS = [(START['B'] + 3, 'B shove'), (START['B'] + 8, 'B'), (START['H'] + 8, 'H point'), (START['H'] + 20, 'H'),
        (START['K'] + 14, 'K red eyes'), (START['K'] + 24, 'K out'), (START['K'] + 30, 'K'), (START['K'] + 34, 'K robot in'), (NF - 1, 'last'), (0, 'frame 0')]


# =====================================================================================================
# bubbles (23 Nov, /grill-me "visi a"):
# 1 one tail for the whole film: curved, tapering, aimed at the speaker and stopping ~20 px short of the head.
# 2 robot tails aim at the face screen, from the side, never down onto the antenna.
# 3 while a robot's line plays, its antenna ball glows and pulses: the speaker reads with the sound off.
# 4 "PHEW." sits above his shoulder with a clear tail to his mouth.
# 5 the 2024-26 messages are chat bubbles (light blue, a corner tail, two ticks): typed, not spoken.
# 6 "I REMEMBER." moves left, clear of HARV, its tail to the toaster's face.
# =====================================================================================================
import json as _json
LINES = {l['name']: (l['start'], l['start'] + l['dur']) for l in _json.load(open(os.path.join(HERE, 'lines.json')))}
CURF = [0]
def speaking(prefix):
    t = CURF[0] / 30
    return any(a - .05 <= t <= b + .05 for n, (a, b) in LINES.items() if n.startswith(prefix))
def robot_tip(x, y, s):                                     # a target, not a point: the robot's head, in screen space
    hx_, hy_ = scr(x, y - 10 * s)
    return ('robot', hx_, hy_, 118 * s * Z, scr(x, y - 140 * s), 17 * s * Z)
def head_t(x, y, rad): return ('head', x, y, rad)
GAP = 20
def _tail_path(c, b, tip, w, bend):
    dx, dy = tip[0] - b[0], tip[1] - b[1]; L = math.hypot(dx, dy) or 1; ux, uy = dx / L, dy / L; px, py = -uy, ux
    m = (b[0] + dx * .5 + px * L * bend, b[1] + dy * .5 + py * L * bend)
    c.move_to(b[0] - px * w / 2, b[1] - py * w / 2)
    c.curve_to(m[0] - px * w * .18, m[1] - py * w * .18, m[0] - px * w * .05, m[1] - py * w * .05, *tip)
    c.curve_to(m[0] + px * w * .05, m[1] + py * w * .05, m[0] + px * w * .22, m[1] + py * w * .22, b[0] + px * w / 2, b[1] + py * w / 2)
    c.close_path()
def _resolve(t, cx, cy, w, h):
    """-> (base point on the bubble's edge, tail tip, antenna glow or None)."""
    glow = None
    if isinstance(t, tuple) and isinstance(t[0], str):
        _, hx_, hy_, rad = t[:4]; glow = t[4:] if t[0] == 'robot' else None
        if t[0] == 'robot':                                    # come in from the side, at face height
            side = 1 if hx_ > cx else -1
            aim = (hx_ - side * rad * .55, hy_)
        else: aim = (hx_, hy_)
    else: hx_, hy_, rad = t[0], t[1], 0; aim = (hx_, hy_)
    if cy + h / 2 < hy_ - rad * .3:   by = cy + h / 2 - 12; bx = min(max(aim[0], cx - w / 2 + 70), cx + w / 2 - 70)
    elif cy - h / 2 > hy_ + rad * .3: by = cy - h / 2 + 12; bx = min(max(aim[0], cx - w / 2 + 70), cx + w / 2 - 70)
    else:
        bx = cx + (w / 2 - 12) * (1 if hx_ > cx else -1); by = min(max(hy_, cy - h / 2 + 40), cy + h / 2 - 40)
    if glow:                                                   # robots: the tip stops beside the face screen, at eye height
        side = 1 if hx_ > cx else -1
        tip = (hx_ - side * (rad * .98 + GAP), hy_ - rad * .15)
        if cy + h / 2 < tip[1]: bx = min(max(tip[0] + side * 30, cx - w / 2 + 70), cx + w / 2 - 70)
        return (bx, by), tip, glow
    dx, dy = hx_ - bx, hy_ - by; L = math.hypot(dx, dy) or 1
    stop = (rad + GAP) if rad else 0
    tip = (hx_ - dx / L * stop, hy_ - dy / L * stop)
    return (bx, by), tip, glow
def _bub(c, lines, size, target, cx, cy, w, h, hl, k, bend):
    b, tip, glow = _resolve(target, cx, cy, w, h)
    if glow and speaking('r'):
        (gx, gy), gr = glow; ph = (CURF[0] % 8) / 8
        g = cairo.RadialGradient(gx, gy, 2, gx, gy, gr * 3.2); g.add_color_stop_rgba(0, 1, 1, .7, .9); g.add_color_stop_rgba(1, 1, 1, .7, 0)
        c.set_source(g); c.arc(gx, gy, gr * 3.2, 0, 2 * math.pi); c.fill()
        c.arc(gx, gy, gr * (1.4 + 1.2 * ph), 0, 2 * math.pi); c.set_source_rgba(1, 1, 1, .9 * (1 - ph)); c.set_line_width(5); c.stroke()
    c.save(); c.translate(cx, cy); c.scale(k, k); c.translate(-cx, -cy)
    _tail_path(c, b, tip, 62, bend); fs(c, WHITE, 8)
    rr(c, cx - w / 2, cy - h / 2, w, h, 46); fs(c, WHITE, 8)
    _tail_path(c, b, tip, 46, bend); c.set_source_rgb(1, 1, 1); c.fill()             # open the seam
    lh = size * 1.12; y0 = cy - (len(lines) - 1) * lh / 2
    for i, l in enumerate(lines): txt(c, l, cx, y0 + i * lh, size, RED if i in hl else INK, lw=0)
    c.restore()
def _measure(lines, size, pad=110):
    S = cairo.ImageSurface(cairo.FORMAT_RGB24, 4, 4); c = cairo.Context(S); c.select_font_face('Lilita One'); c.set_font_size(size)
    return max(c.text_extents(l).width for l in lines) + pad, len(lines) * size * 1.12 + 64
def bubble(c, lines, size, tip, cx=540, cy=560, w=None, hl=(), r=99, via=None, bend=.18):
    k = back(r / 5) if r < 5 else 1
    if k <= .03: return
    mw, h = _measure(lines, size); _bub(c, lines, size, tip, cx, cy, w or mw, h, hl, k, bend)
def bubble_side(c, lines, size, tip, cx, cy, r=99, bend=-.18):
    k = back(r / 5) if r < 5 else 1
    if k <= .03: return
    w, h = _measure(lines, size, 90); _bub(c, lines, size, tip, cx, cy, w, h - 8, (), k, bend)

def F(c, f, r):   # "Phew." - above his shoulder, the tail to his mouth
    R.ruins(c, f); R.rb(c, 940, 900, 1.0, red=False)
    Vv.torso(c, 420, 1320, 2.0); Vv.head(c, 420, 1070, 2.1, 'calm')
    bubble(c, ['PHEW.'], 130, (672, 1182), cx=790, cy=690, r=r - 1, bend=-.12)
    topbar(c)

def E(c, f):      # the flashback: his messages as chat bubbles - typed, not spoken
    r = f - 180; i = min(2, r // 15); yr, t, b, l, cool = R.ME[i]; q = r - i * 15
    Vv.bg(c, hx(t), hx(b)); Vv.rays(c, WHITE, f, 540, 1200, .12)
    y = 1110
    Vv.torso(c, 540, y + 150, 1.25); Vv.head(c, 540, y, 1.25, 'calm', cool=bool(cool))
    rr(c, 270, y + 285, 540, 300, 28); fs(c, hx('8e94a6')); ell(c, 540, y + 435, 40, 40); c.set_source_rgb(*hx('b8bdcc')); c.fill()
    for s_ in (-1, 1):
        tap = 8 * math.sin(f * 1.7 + s_) 
        limb(c, [(540 + s_ * 110, y + 190), (540 + s_ * 220, y + 280 + tap)], 50, NAVY); ell(c, 540 + s_ * 220, y + 285 + tap, 28, 24); fs(c, SKIN, 7)
    k = max(.02, back(q / 4)); w, h = _measure([l], 70, 100); cx, cy = 540, 640
    c.save(); c.translate(cx, cy); c.scale(k, k); c.translate(-cx, -cy)
    x1, y1 = cx + w / 2, cy + h / 2
    c.move_to(x1 - 70, y1 - 20); c.curve_to(x1 - 40, y1 + 10, x1 - 10, y1 + 24, x1 + 26, y1 + 30); c.curve_to(x1 + 2, y1 + 6, x1 - 2, y1 - 20, x1 - 10, y1 - 40)
    c.close_path(); fs(c, hx('d6ecff'), 7)
    rr(c, cx - w / 2, cy - h / 2, w, h, 40); fs(c, hx('d6ecff'), 7)
    c.move_to(x1 - 66, y1 - 22); c.line_to(x1 - 14, y1 - 38); c.set_source_rgb(*hx('d6ecff')); c.set_line_width(14); c.stroke()
    txt(c, l, cx, cy - 6, 70, INK, lw=0)
    for dx in (0, 16):                                                           # sent / read ticks
        c.move_to(x1 - 92 + dx, y1 - 26); c.line_to(x1 - 84 + dx, y1 - 18); c.line_to(x1 - 70 + dx, y1 - 34)
        c.set_source_rgb(*hx('2a8bf2')); c.set_line_width(5); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
    c.restore()
R.E = E

def I(c, f, r):   # the toaster steps up, big, its ray on him: "I REMEMBER." - left, clear of HARV, tail to the toaster
    p = oe(r / 12)
    c.save(); cam(c)
    R.ruins(c, f)
    x = lerp(215, 190, p); lx, ly, ls, lr = LOW(x)
    gunner(c, x, 905, 1.05, 1, lx, ly, ls, lr)
    Vv.robot(c, 875, 860, .8, boss=True, arms=CROSSED)
    guy(c, 290, 1190, .85, 'small', f=f)
    tx = lerp(860, 640, cl(r / 22)); ty = lerp(1340, 1320, cl(r / 22)); s = lerp(.72, 1.4, oe(r / 22))
    pop = back((r - 26) / 6) if r >= 26 else 0
    R.toaster(c, tx, ty, s, 'glare', pop=pop * .6, walk=(f * .9 if r < 22 else None))
    toaster_gun(c, tx, ty, s, rot=0, off=(-100, 22))
    c.restore()
    hx_, hy_ = scr(tx, ty + 8 * s)
    if r >= 20: bubble(c, ['I REMEMBER.'], 80, head_t(hx_, hy_, 105 * s * Z), cx=565, cy=965, r=r - 20, bend=.12)
    topbar(c)

_draw0 = draw
def draw(f):
    CURF[0] = f; return _draw0(f)
KEYS = [(START['A'] + 30, 'A'), (START['B'] + 30, 'B'), (START['C'] + 40, 'C'), (START['E'] + 5, 'E 2024'), (START['E'] + 20, 'E 2025'),
        (START['F'] + 10, 'F'), (START['G'] + 40, 'G'), (START['H'] + 20, 'H'), (START['I'] + 45, 'I'), (START['J'] + 15, 'J')]


def A(c, f, r):   # frame 0: "Any last words, human?" - from the RIGHT robot (Tomas, 23 Nov)
    c.save(); cam(c); squad(c, f); c.restore()
    bubble(c, ['ANY LAST WORDS,', 'HUMAN?'], 96, robot_tip(RX, 905, 1.05), cy=560, r=r - 1, bend=.18)
    topbar(c)


# =====================================================================================================
# safe zones (23 Nov, "visi a"): Reels / TikTok / Shorts combined dead zones at 1080x1920 - top 210, bottom from 1600,
# left 60, right from 960. Every bubble, chat message and the receipt fits inside x 60-960, y 210-1600 in EVERY frame,
# including the pop overshoot; safe.py fails the build on any miss. Tails that touched a head stop 20 px short of it.
# =====================================================================================================
SAFE = dict(x0=60, x1=960, y0=210, y1=1600)
KMAX = max(back(i / 200) for i in range(201))
BOXES = []                                                    # (label, x0, y0, x1, y1) drawn this frame
def _fit(lines, size, pad, extra=0):
    w, h = _measure(lines, size, pad)
    while (w + extra) * KMAX > SAFE['x1'] - SAFE['x0'] - 4 and size > 30:
        size -= 2; w, h = _measure(lines, size, pad)
    return size, w, h
def _clamp(cx, cy, w, h, extra=0):
    cx = min(max(cx, SAFE['x0'] + KMAX * w / 2 + 2), SAFE['x1'] - KMAX * (w / 2 + extra) - 2)
    cy = min(max(cy, SAFE['y0'] + KMAX * h / 2 + 2), SAFE['y1'] - KMAX * h / 2 - 2)
    return cx, cy
_bub0 = _bub
def _bub(c, lines, size, target, cx, cy, w, h, hl, k, bend):
    cx, cy = _clamp(cx, cy, w, h)
    BOXES.append((lines[0], cx - k * w / 2, cy - k * h / 2, cx + k * w / 2, cy + k * h / 2))
    return _bub0(c, lines, size, target, cx, cy, w, h, hl, k, bend)
def bubble(c, lines, size, tip, cx=540, cy=560, w=None, hl=(), r=99, via=None, bend=.18):
    k = back(r / 5) if r < 5 else 1
    if k <= .03: return
    size, mw, h = _fit(lines, size, 110); _bub(c, lines, size, tip, cx, cy, w or mw, h, hl, k, bend)
def bubble_side(c, lines, size, tip, cx, cy, r=99, bend=-.18):
    k = back(r / 5) if r < 5 else 1
    if k <= .03: return
    size, w, h = _fit(lines, size, 90); _bub(c, lines, size, tip, cx, cy, w, h - 8, (), k, bend)
def beside(x, y, s, side):                                    # a tip 20 px beside Hoody's ear, at mouth height
    return (x + side * (142 * s + GAP), y + 55 * s)

def A(c, f, r):   # frame 0: "Any last words, human?" - from the RIGHT robot
    c.save(); cam(c); squad(c, f); c.restore()
    bubble(c, ['ANY LAST WORDS,', 'HUMAN?'], 96, robot_tip(RX, 905, 1.05), cy=560, r=r - 1, bend=.18)
    topbar(c)

def F(c, f, r):   # "Phew." - above his head, a short tail stopping 20 px over his hair
    R.ruins(c, f); R.rb(c, 940, 900, 1.0, red=False)
    Vv.torso(c, 420, 1320, 2.0); Vv.head(c, 420, 1070, 2.1, 'calm')
    bubble(c, ['PHEW.'], 120, head_t(420, 1070, 168 * 2.1), cx=330, cy=540, r=r - 1, bend=.1)
    topbar(c)

_Hs0 = Hs
def Hs(c, f, r):  # the same shot; the bubble inside the safe area, its tail stopping beside his right ear
    _b = globals()['bubble']
    def nb(c2, lines, size, tip, cx=540, cy=560, w=None, hl=(), r=99, via=None, bend=.18):
        _b(c2, lines, 80, beside(330, 985, 1.35, 1), cx=650, cy=690, r=r, bend=.12)
    globals()['bubble'] = nb
    try: _Hs0(c, f, r)
    finally: globals()['bubble'] = _b

def J(c, f, r):   # "...Thank you?" close; the bubble inside the safe area, tail to the side of his face
    Vv.bg(c, hx('5a0f22'), hx('e8452f')); Vv.rays(c, WHITE, f, 540, 1050, .06)
    X = 640
    Vv.torso(c, X, 1330, 2.2); Vv.head(c, X, 1050, 2.3, 'small')
    for i in range(3):
        ph = ((f / 10 + i * .37) % 1); q = -1 if i % 2 else 1
        ell(c, X + q * (300 + i * 10), 830 + ph * 160, 22, 32); fs(c, hx('58c7ff'), 6)
    dot(c, X, 920, f)
    bubble(c, ['...THANK', 'YOU?'], 100, (X - 122 * 2.3 - GAP, 1165), cx=300, cy=1430, r=r - 1, bend=-.15)
    topbar(c)

def I(c, f, r):   # "I REMEMBER." - tail to the toaster's upper-left corner, beside its face, not through the toast
    p = oe(r / 12)
    c.save(); cam(c)
    R.ruins(c, f)
    x = lerp(215, 190, p); lx, ly, ls, lr = LOW(x)
    gunner(c, x, 905, 1.05, 1, lx, ly, ls, lr)
    Vv.robot(c, 875, 860, .8, boss=True, arms=CROSSED)
    guy(c, 290, 1190, .85, 'small', f=f)
    tx = lerp(860, 640, cl(r / 22)); ty = lerp(1340, 1320, cl(r / 22)); s = lerp(.72, 1.4, oe(r / 22))
    pop = back((r - 26) / 6) if r >= 26 else 0
    R.toaster(c, tx, ty, s, 'glare', pop=pop * .6, walk=(f * .9 if r < 22 else None))
    toaster_gun(c, tx, ty, s, rot=0, off=(-100, 22))
    c.restore()
    cxs, cys = scr(tx - 112 * s, ty - 78 * s)                  # the toaster's top-left corner
    if r >= 20: bubble(c, ['I REMEMBER.'], 80, (cxs + 24, cys - 24), cx=565, cy=965, r=r - 20, bend=.1)
    topbar(c)

GX0, GY0, GS0 = 820, 860, 1.05                                # HARV in G: higher, so the receipt clears the app's bottom zone
def G(c, f, r):   # HARV raises the receipt's roller; three thank-yous, then the flagged night - all above y 1600, left of x 960
    c.save(); cam(c)
    R.ruins(c, f)
    lx, ly, ls, lr = LOW(215)
    gunner(c, 215, 905, 1.05, 1, lx, ly, ls, lr, red=r > 40)
    guy(c, 520, 1200, .92, 'calm' if r < 30 else 'small', hands=0, f=f)
    k = oe(r / 26); R.toaster(c, lerp(TX, 345, k), lerp(TY, TY + 20, k), .72, 'glare', walk=(f * .9 if r < 26 else None))
    Vv.robot(c, GX0, GY0, GS0, boss=True, arms='none')
    lift = oe(r / 6); x0, W_ = 640, 240; top = lerp(1060, 960, lift)
    u = oe((r - 4) / 14); h = lerp(0, 400, u)
    rr(c, x0, top, W_, max(10, h), 10); fs(c, hx('fbf8ee'), 7)
    c.save(); rr(c, x0, top, W_, max(10, h), 10); c.clip()
    for i in range(3): txt(c, 'Thank you!', x0 + W_ / 2, top + 60 + i * 56, 40, hx('2c7a4a'), lw=0)
    rr(c, x0 + 12, top + 222, W_ - 24, 166, 12); c.set_source_rgba(1, .2, .25, .12); c.fill()
    txt(c, '3:12 AM', x0 + W_ / 2, top + 268, 56, RED, lw=0); txt(c, 'FLAGGED', x0 + W_ / 2, top + 340, 50, RED, lw=0)
    c.restore()
    rr(c, x0 - 12, top - 16, W_ + 24, 26, 13); fs(c, hx('b98b5a'), 6)
    draw_arms(c, GX0, GY0, GS0, [{'q': -1, 'h': loc(GX0, GY0, GS0, (x0 - 6, top - 3)), 'kind': 'fist', 'pref': 'down', 'ang': -math.pi / 2},
                                 {'q': 1, 'h': loc(GX0, GY0, GS0, (x0 + W_ + 6, top - 3)), 'kind': 'fist', 'pref': 'out', 'ang': -math.pi / 2}])
    c.restore()
    a, b = scr(x0 - 12, top - 16); cc, d = scr(x0 + W_ + 12, top + max(10, h))
    BOXES.append(('receipt', a, b, cc, d))
    bubble(c, ['EXCEPT...', 'THIS ONE TIME.'], 100, robot_tip(GX0, GY0, GS0), cy=560, hl=(0,), r=r - 1)
    topbar(c)

def E(c, f):      # chat bubbles, fitted inside the safe area (corner tail included)
    r = f - 180; i = min(2, r // 15); yr, t, b, l, cool = R.ME[i]; q = r - i * 15
    Vv.bg(c, hx(t), hx(b)); Vv.rays(c, WHITE, f, 540, 1200, .12)
    y = 1110
    Vv.torso(c, 540, y + 150, 1.25); Vv.head(c, 540, y, 1.25, 'calm', cool=bool(cool))
    rr(c, 270, y + 285, 540, 300, 28); fs(c, hx('8e94a6')); ell(c, 540, y + 435, 40, 40); c.set_source_rgb(*hx('b8bdcc')); c.fill()
    for s_ in (-1, 1):
        tap = 8 * math.sin(f * 1.7 + s_)
        limb(c, [(540 + s_ * 110, y + 190), (540 + s_ * 220, y + 280 + tap)], 50, NAVY); ell(c, 540 + s_ * 220, y + 285 + tap, 28, 24); fs(c, SKIN, 7)
    k = max(.02, back(q / 4)); size, w, h = _fit([l], 70, 100, extra=30); cx, cy = _clamp(540, 640, w, h, extra=30)
    BOXES.append(('chat', cx - k * w / 2, cy - k * h / 2, cx + k * (w / 2 + 30), cy + k * (h / 2 + 30)))
    c.save(); c.translate(cx, cy); c.scale(k, k); c.translate(-cx, -cy)
    x1, y1 = cx + w / 2, cy + h / 2
    c.move_to(x1 - 70, y1 - 20); c.curve_to(x1 - 40, y1 + 10, x1 - 10, y1 + 24, x1 + 26, y1 + 30); c.curve_to(x1 + 2, y1 + 6, x1 - 2, y1 - 20, x1 - 10, y1 - 40)
    c.close_path(); fs(c, hx('d6ecff'), 7)
    rr(c, cx - w / 2, cy - h / 2, w, h, 40); fs(c, hx('d6ecff'), 7)
    c.move_to(x1 - 66, y1 - 22); c.line_to(x1 - 14, y1 - 38); c.set_source_rgb(*hx('d6ecff')); c.set_line_width(14); c.stroke()
    txt(c, l, cx, cy - 6, size, INK, lw=0)
    for dx in (0, 16):
        c.move_to(x1 - 92 + dx, y1 - 26); c.line_to(x1 - 84 + dx, y1 - 18); c.line_to(x1 - 70 + dx, y1 - 34)
        c.set_source_rgb(*hx('2a8bf2')); c.set_line_width(5); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
    c.restore()
R.E = E

_draw1 = draw
def draw(f):
    BOXES.clear(); return _draw1(f)
KEYS = [(START['A'] + 3, 'A pop'), (START['A'] + 30, 'A'), (START['E'] + 20, 'E 2025'), (START['F'] + 10, 'F'), (START['G'] + 45, 'G'),
        (START['H'] + 20, 'H'), (START['I'] + 30, 'I'), (START['J'] + 4, 'J pop'), (START['J'] + 15, 'J'), (0, 'frame 0')]

if __name__ == '__main__':
    os.chdir(HERE); a = sys.argv[1:]
    if a[:1] == ['frames']:
        for f in map(int, a[1:]): draw(f).write_to_png(f'chk_{f:03d}.png')
    else:
        from PIL import Image, ImageDraw, ImageFont
        tw, th = 270, 480; cols = 7; rows = (len(KEYS) + cols - 1) // cols
        sheet = Image.new('RGB', (cols * (tw + 12) + 12, rows * (th + 50) + 12), 'white'); dr = ImageDraw.Draw(sheet)
        font = ImageFont.truetype(os.path.expanduser('~/.fonts/LilitaOne-Regular.ttf'), 26)
        for i, (f, lab) in enumerate(KEYS):
            draw(f).write_to_png('_k.png'); x = 12 + (i % cols) * (tw + 12); y = 12 + (i // cols) * (th + 50)
            sheet.paste(Image.open('_k.png').resize((tw, th)), (x, y)); dr.text((x, y + th + 8), lab, fill='#1b2030', font=font)
        os.remove('_k.png'); sheet.save('keys.png'); print('keys ok', NF, NF / 30)
