"""ME + MY AI - Untitled: key poses of the main shots (stills for G3 review, no animation yet).
Cast and park come from Perfect Date (imported, not touched). Size rule: Hoody and Eva the same scale, MY AI 1.07 x it.
python3 keys.py            -> keys/kNN.png at 1080x1920 + keys/sheet.png"""
import os, sys, math, cairo
HERE = os.path.dirname(os.path.abspath(__file__)); PD = os.path.join(HERE, '..', 'perfect-date')
sys.path.insert(0, PD); _cwd = os.getcwd(); os.chdir(PD)
import render as R
os.chdir(_cwd)
from render import K, A, E, Sh, W, H, park, hoody, bubble, txt, rr, fs, ell, limb, hx, lerp, cl, NAVY, INK, YEL, WHITE, RED

AIK = 1.07                                   # MY AI scale = 1.07 x Hoody's / Eva's
POO, POO_D, POO_L = hx('9a6234'), hx('6e4321'), hx('c48a58')
PLW = hx('f4f4f2'); PLS = hx('d9dbe0')
K.FACES['frozen'] = ('big', ('flat', 'flat'), 'flat')
K.FACES['critic'] = ('half', ('flat', 'raised'), 'flat')
K.FACES['proud'] = ('happy', ('raised', 'raised'), 'grin')

# ---------------- props ----------------
def poop(c, x, y, s=1.0):
    """A cartoon swirl, three soft tiers and a curl on top; y = its base."""
    c.save(); c.translate(x, y); c.scale(s, s)
    for w, h, dy in ((88, 34, -30), (66, 30, -78), (44, 26, -118)):
        ell(c, 0, dy, w, h); fs(c, POO, 7)
        c.arc(-w * .2, dy - h * .1, w * .55, math.pi * 1.1, math.pi * 1.55); c.set_source_rgba(*POO_L, .9); c.set_line_width(7); c.stroke()
    c.move_to(-6, -140); c.curve_to(0, -178, 34, -170, 22, -150); fs(c, POO, 7)
    c.restore()

def plinth(c, x, top, w, h, label=True, lab_k=1.0):
    """A white gallery plinth, seen a touch from above, with a black label plate on its front."""
    d = w * .14
    c.move_to(x - w / 2, top); c.line_to(x - w / 2 + d, top - d * .7); c.line_to(x + w / 2 + d, top - d * .7); c.line_to(x + w / 2, top); c.close_path(); fs(c, WHITE, 7)
    c.move_to(x + w / 2, top); c.line_to(x + w / 2 + d, top - d * .7); c.line_to(x + w / 2 + d, top + h - d * .7); c.line_to(x + w / 2, top + h); c.close_path(); fs(c, PLS, 7)
    c.rectangle(x - w / 2, top, w, h); fs(c, PLW, 7)
    if label:
        lw, lh = w * .94 * lab_k, w * .42 * lab_k; ly = top + w * .16
        rr(c, x - lw / 2, ly, lw, lh, 10); fs(c, INK, 4)
        txt(c, 'UNTITLED', x, ly + lh * .34, lh * .36, WHITE, lw=0)
        txt(c, 'mixed media (2026)', x, ly + lh * .74, lh * .22, hx('dfe2e8'), lw=0)

def card(c, x, y, q=1):
    """MY AI's 10/10 score card on a stick, held up."""
    limb(c, [(x, y), (x, y - 90)], 10, hx('d9a86c'))
    rr(c, x - 78, y - 210, 156, 120, 14); fs(c, WHITE, 7)
    txt(c, '10/10', x, y - 150, 62, RED, lw=0)

def tongs(c, x, y, q=1):
    """Long silver tongs held out to the side, pinching at the tip (the tip is returned by tongs_tip)."""
    tx, ty = x + q * 150, y + 70
    for o in (-1, 1):
        c.move_to(x, y); c.line_to(tx, ty + o * 10); c.set_source_rgb(*INK); c.set_line_width(14); c.stroke()
        c.move_to(x, y); c.line_to(tx, ty + o * 10); c.set_source_rgb(*hx('c9ccd4')); c.set_line_width(7); c.stroke()
def tongs_tip(x, y, q=1): return x + q * 150, y + 70

def marker(c, x, y, q=1):
    c.save(); c.translate(x, y); c.rotate(q * .9); rr(c, -10, -70, 20, 80, 8); fs(c, INK, 4); rr(c, -6, -82, 12, 14, 4); fs(c, RED, 3); c.restore()

def bag(c, x, y, s=1.0, full=True):
    """A green dog bag pinched in her fingers."""
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(-14, 0); c.line_to(14, 0); c.curve_to(48, 40, 52, 110, 0, 118); c.curve_to(-52, 110, -48, 40, -14, 0); c.close_path(); fs(c, hx('5cc46a'), 6)
    if full: ell(c, 0, 82, 30, 22); c.set_source_rgba(*POO_D, .35); c.fill()
    c.restore()

def phone(c, x, y, q=1):
    rr(c, x - 26, y - 60, 52, 92, 10); fs(c, hx('22252e'), 5); rr(c, x - 19, y - 52, 38, 72, 6); c.set_source_rgb(*hx('7fd0ff')); c.fill()

def bush(c, x, gy, s=1.0):
    for dx, dy, r in ((-110, -60, 80), (-30, -120, 100), (80, -90, 90), (150, -40, 60), (-170, -20, 50)):
        ell(c, x + dx * s, gy + dy * s, r * s, r * s); c.set_source_rgb(*INK); c.set_line_width(14); c.stroke()
    for dx, dy, r in ((-110, -60, 80), (-30, -120, 100), (80, -90, 90), (150, -40, 60), (-170, -20, 50)):
        ell(c, x + dx * s, gy + dy * s, r * s, r * s); c.set_source_rgb(*hx('3f9a4a')); c.fill()
    for dx, dy, r in ((-60, -150, 26), (60, -130, 22), (-130, -80, 20)):
        ell(c, x + dx * s, gy + dy * s, r * s, r * s); c.set_source_rgb(*hx('5cb85c')); c.fill()

def puff(c, x, y, s=1.0):
    for dx, dy, r in ((-40, 0, 34), (0, -26, 42), (42, -4, 32), (8, 18, 28)):
        ell(c, x + dx * s, y + dy * s, r * s, r * s); fs(c, hx('f2efe6'), 6)

# ---------------- MY AI extras ----------------
def visor_text(c, x, gy, s, lines, col=hx('33bfff'), tilt=0, turn=0):
    """Text on MY AI's visor in place of its eyes (big shots only). Matches myai()'s head transform."""
    c.save(); c.translate(x, gy); c.translate(0, -280 * s); c.scale(s, s)
    c.translate(0, 85); c.rotate(math.radians(tilt)); c.translate(0, -85)
    vx = turn * 40
    rr(c, -82 + vx, -54, 164 - abs(turn) * 30, 92, 40); fs(c, A.VISOR, 6)
    n = len(lines); sz = 74 / n if n > 1 else 40
    for i, l in enumerate(lines): txt(c, l, vx, -8 + (i - (n - 1) / 2) * sz * 1.05, sz, col, lw=0)
    c.restore()

def ai(c, x, gy, s, **k):
    A.myai(c, x, gy, s, **k)

def ai_hand(x, gy, s, q, pose):
    return A.hand_at(x, gy, s, q, pose)

# ---------------- sets ----------------
GY = 1600                                    # ground line in the park shots (on the path)
def park_bg(c, f=0):
    park(c, f)

CEIL, FLOOR = 430, 1400                         # gallery: ceiling line, wall/floor line
def gallery(c, door_x=None, title_x=540, title_y=520):
    """A modern art gallery: tall white walls, a track of spotlights, polished grey concrete, big works on the walls,
    the hall's name in grey vinyl letters, a doorway into the next white room."""
    c.set_source_rgb(*hx('dfe1e5')); c.paint()                                                      # ceiling
    g = cairo.LinearGradient(0, CEIL, 0, FLOOR); g.add_color_stop_rgb(0, *hx('fdfdfc')); g.add_color_stop_rgb(1, *hx('efefed'))
    c.set_source(g); c.rectangle(0, CEIL, W, FLOOR - CEIL); c.fill()                                 # wall
    if door_x is not None:                                                                         # doorway to the next room
        c.rectangle(door_x, 900, 210, FLOOR - 900); c.set_source_rgb(*hx('e6e7ea')); c.fill()
        c.rectangle(door_x + 40, 1010, 90, 120); c.set_source_rgb(*hx('ffcf2e')); c.fill()            # a work in the next room
        c.rectangle(door_x, 900, 210, FLOOR - 900); c.set_source_rgb(*hx('c9ccd2')); c.set_line_width(6); c.stroke()
    g = cairo.LinearGradient(0, FLOOR, 0, H); g.add_color_stop_rgb(0, *hx('c3c6cc')); g.add_color_stop_rgb(1, *hx('9fa3ab'))
    c.set_source(g); c.rectangle(0, FLOOR, W, H - FLOOR); c.fill()                                  # polished concrete
    for y in (1560, 1780): c.move_to(0, y); c.line_to(W, y); c.set_source_rgba(0, 0, 0, .07); c.set_line_width(3); c.stroke()
    for x in (180, 540, 900): c.move_to(x, FLOOR); c.line_to(x + (x - 540) * .8, H); c.set_source_rgba(0, 0, 0, .06); c.set_line_width(3); c.stroke()
    c.rectangle(0, FLOOR - 8, W, 10); c.set_source_rgb(*hx('8d9199')); c.fill()                      # shadow gap
    c.rectangle(0, CEIL - 6, W, 6); c.set_source_rgb(*hx('c4c7cd')); c.fill()
    c.rectangle(0, CEIL + 34, W, 12); c.set_source_rgb(*hx('2a2d36')); c.fill()                       # light track
    txt(c, 'MODERN ART', title_x, title_y, 64, hx('a4a8b0'), lw=0)                                  # vinyl wall letters
    c.rectangle(title_x - 160, title_y + 36, 320, 4); c.set_source_rgb(*hx('c4c7cd')); c.fill()

def wall_work(c, x, y, w, h, kind):
    """A big work on the wall (generic): 'blue' monochrome, 'line' one black line on cream, 'squares' three colour blocks."""
    c.rectangle(x + 10, y + 12, w, h); c.set_source_rgba(0, 0, 0, .10); c.fill()
    c.rectangle(x, y, w, h); fs(c, {'blue': hx('2f6fd6'), 'line': hx('fbf3e0'), 'squares': WHITE}[kind], 6)
    if kind == 'line': c.move_to(x + w * .2, y + h * .8); c.curve_to(x + w * .4, y + h * .2, x + w * .6, y + h * .9, x + w * .8, y + h * .25); c.set_source_rgb(*INK); c.set_line_width(10); c.stroke()
    if kind == 'squares':
        for i, col in enumerate(('ff5c4d', 'ffcf2e', '2f6fd6')): c.rectangle(x + 18, y + 18 + i * (h - 36) / 3, w - 36, (h - 36) / 3 - 10); c.set_source_rgb(*hx(col)); c.fill()
    rr(c, x + w + 18, y + h - 50, 54, 40, 4); fs(c, WHITE, 3)                                     # its wall label

def spot(c, x, y_bot, w, y_top=CEIL + 46):
    g = cairo.LinearGradient(0, y_top, 0, y_bot); g.add_color_stop_rgba(0, 1, .98, .88, .65); g.add_color_stop_rgba(1, 1, .98, .88, 0)
    c.move_to(x - 24, y_top + 40); c.line_to(x + 24, y_top + 40); c.line_to(x + w / 2, y_bot); c.line_to(x - w / 2, y_bot); c.close_path(); c.set_source(g); c.fill()
    c.save(); c.translate(x, y_top + 10); c.rotate(.0); rr(c, -22, -10, 44, 52, 10); fs(c, hx('2a2d36'), 3); c.restore()
    ell(c, x, y_bot - 6, w * .55, 26); c.set_source_rgba(1, .98, .88, .35); c.fill()                # the pool of light on the floor

BRZ, BRZ_D, BRZ_L = hx('7a4a24'), hx('4e2c12'), hx('d29a5e')
def bronze_swirl(c, x, y, s=1.0, tiers=3):
    """The museum's star piece: a polished bronze swirl. It looks a lot like the thing in the park (that is the point)."""
    c.save(); c.translate(x, y); c.scale(s, s)
    dims = ((96, 38, -34), (74, 33, -88), (52, 29, -136), (32, 22, -176))[:tiers]
    for w, h, dy in dims:
        ell(c, 0, dy, w, h); fs(c, BRZ, 7)
        c.arc(-w * .25, dy - h * .15, w * .55, math.pi * 1.1, math.pi * 1.6); c.set_source_rgba(*BRZ_L, .95); c.set_line_width(9); c.stroke()
        ell(c, w * .45, dy + h * .2, w * .18, h * .25); c.set_source_rgba(*BRZ_D, .5); c.fill()
    ty = dims[-1][2] - dims[-1][1]
    c.move_to(-8, ty + 6); c.curve_to(0, ty - 44, 40, ty - 36, 26, ty - 12); fs(c, BRZ, 7)
    ell(c, -30, dims[0][2] - 8, 10, 6); c.set_source_rgba(1, 1, 1, .7); c.fill()                     # a glint
    c.restore()

def bronze_lumps(c, x, y, s=1.0):
    """Two bronze lumps leaning on each other."""
    c.save(); c.translate(x, y); c.scale(s, s)
    for dx, dy, a, b in ((-30, -50, 70, 52), (36, -100, 56, 60)):
        ell(c, dx, dy, a, b); fs(c, BRZ, 7); c.arc(dx - a * .2, dy - b * .1, a * .55, math.pi * 1.1, math.pi * 1.6); c.set_source_rgba(*BRZ_L, .95); c.set_line_width(9); c.stroke()
    c.restore()

def lbl(c, x, y, w):
    """A museum label on a plinth front."""
    rr(c, x - w / 2, y, w, w * .42, 8); fs(c, INK, 3); txt(c, 'UNTITLED', x, y + w * .21, w * .17, WHITE, lw=0)

def topbar(c, pill): Sh.topbar(c, pill)

# ---------------- the key shots ----------------
# frame-0 layout (park): MY AI left, Hoody centre-left, the plinth in the near foreground right of centre, room for Eva on the right
HS = 1.0; AX, HX_, PX = 175, 430, 700
def frame0_set(c, f=0, poo=True, ai_eye='heart', ai_arms=('chest', 'chest'), ai_look=(14, 6), ai_turn=0, hoody_expr='critic', hoody_gaze=20, ai_tilt=6):
    park_bg(c, f)
    ai(c, AX, GY + 20, HS * AIK, eye=ai_eye, arms=ai_arms, look=ai_look, tilt=ai_tilt, turn=ai_turn)
    hoody(c, HX_, GY, HS, expr=hoody_expr, arms=('rest', 'chin'), gaze=hoody_gaze, f=f, blink=False)

def frame0_plinth(c, poo=True):
    top = 1500; plinth(c, PX, top, 400, 520)
    if poo: poop(c, PX + 20, top - 4, 1.1)

def k01(c):   # shot 1, frame 0: "Be brutally honest."
    frame0_set(c); frame0_plinth(c)
    bubble(c, ['BE BRUTALLY', 'HONEST.'], 20, (470, 800), cy=560, cx=640)
    topbar(c, 'ITS ART')

def k02(c):   # shot 2: CU MY AI, heart eyes, the 10/10 card up. Hoody's shoulder in the foreground
    park(c, 0, zoom=1.7, cy=1250)
    ai(c, 470, 2050, 2.5, eye='heart', arms=('chest', 'up'), props=(None, card), tilt=-6, look=(-6, 0))
    bubble(c, ['A MASTERPIECE!', '10/10.'], 20, (470, 1010), cy=560, cx=560, size=74)
    topbar(c, 'ITS ART')

def k05(c):   # shot 5: the gallery. "See? This is art." He points at the bronze swirl on its plinth; MY AI studies it
    gallery(c, door_x=840, title_x=780, title_y=680)
    wall_work(c, 60, 640, 300, 380, 'blue')
    spot(c, 560, 1480, 420)
    plinth(c, 560, 1200, 300, 420, label=False); lbl(c, 560, 1420, 200); bronze_swirl(c, 560, 1196, 1.2)
    ai(c, 905, 1820, HS * 1.15 * AIK, eye='focus', tilt=-12, look=(-16, 6), arms=('down', 'hip'))
    hoody(c, 220, 1800, HS * 1.15, expr='confident', arms=('rest', 'out'), gaze=22, blink=False)
    bubble(c, ['SEE? THIS IS ART.'], 20, (300, 1000), cy=545, cx=540)
    topbar(c, 'HIS LESSON')

def k07(c):   # shot 7: along the hall: two more bronze pieces on plinths, each scored 10/10; the visor fills
    gallery(c, title_x=540, title_y=1010)
    wall_work(c, 420, 600, 240, 300, 'squares')
    for x in (200, 880): spot(c, x, 1420, 340)
    plinth(c, 200, 1120, 230, 300, label=False); lbl(c, 200, 1300, 160); bronze_lumps(c, 200, 1116, 1.0)
    plinth(c, 880, 1120, 230, 300, label=False); lbl(c, 880, 1300, 160); bronze_swirl(c, 880, 1116, .9, tiers=4)
    c.save(); c.translate(262, 1300); c.rotate(-.15); rr(c, -62, -32, 124, 64, 10); fs(c, WHITE, 5); txt(c, '10/10', 0, 0, 40, RED, lw=0); c.restore()   # the lumps' sticker
    hoody(c, 485, 1880, HS * .9, expr='proud', arms=('rest', 'rest'), f=0, blink=False)
    ai(c, 760, 1880, HS * .9 * AIK, eye='happy', arms=('down', 'up'), props=(None, card), look=(10, -4), turn=.2)
    visor_text(c, 760, 1880, HS * .9 * AIK, ['= ART'], turn=.2)
    topbar(c, 'HIS LESSON')

def k09(c):   # shot 9: the park, wide. Eva and the dog by the bush - a puff behind it. Hoody on his phone. MY AI sees.
    park_bg(c)
    bush(c, 700, 1500, 1.1); puff(c, 700, 1235, 1.3)
    col = E.dog(c, 560, 1590, .7, look=1)
    hand = E.eva(c, 950, 1590, .78, 'evacalm', sip=.6, gaze=-10)
    E.leash(c, hand, col, sag=40)
    hoody(c, 320, 1640, .78, expr='calm', arms=('rest', 'take'), prop=phone, gaze=14, blink=False)
    ai(c, 130, 1660, .78 * AIK, eye='open', look=(18, 4), turn=.3)
    topbar(c, 'HIS LESSON')

def k10(c):   # shot 10: CU MY AI, the rule lights up on its visor
    park(c, 0, zoom=1.7, cy=1250)
    for i in range(10):
        a = i * math.pi / 5; c.move_to(540 + math.cos(a) * 470, 1100 + math.sin(a) * 470); c.line_to(540 + math.cos(a) * 620, 1100 + math.sin(a) * 620)
        c.set_source_rgba(*YEL, .9); c.set_line_width(14); c.stroke()
    ai(c, 540, 2000, 2.8, eye='wide', arms=('down', 'down'), tilt=0)
    visor_text(c, 540, 2000, 2.8, ['PLINTH', '+ LABEL', '= ART'], col=YEL)
    topbar(c, 'HIS LESSON')

def k11(c):   # shot 11: MY AI with the tongs lifts the art onto its plinth; the marker label is already written
    park_bg(c)
    top = 1500; plinth(c, PX, top, 400, 520)
    hoody(c, 160, GY - 30, HS * .9, expr='shock', arms=('rest', 'down'), prop=phone, gaze=26, blink=False)
    x, gy, s = 430, GY + 20, HS * AIK
    hx_, hy_ = ai_hand(x, gy, s, 1, 'offer')
    ai(c, x, gy, s, eye='focus', arms=('chest', 'offer'), look=(18, 6), turn=.25)
    pb = (PX + 20, top - 30)                                              # the art, just above its place
    poop(c, *pb, 1.1); tip = (pb[0] - 30, pb[1] - 90)
    for o in (-1, 1):
        c.move_to(hx_, hy_); c.line_to(tip[0], tip[1] + o * 12); c.set_source_rgb(*INK); c.set_line_width(14); c.stroke()
        c.move_to(hx_, hy_); c.line_to(tip[0], tip[1] + o * 12); c.set_source_rgb(*hx('c9ccd4')); c.set_line_width(7); c.stroke()
    topbar(c, 'ITS ART')

def k12(c):   # shot 12: frame 0 again; Eva walks in and calmly bags it. Hoody frozen between them
    frame0_set(c, ai_eye='heart', hoody_expr='frozen', hoody_gaze=26)
    hand = E.eva(c, 870, GY, HS, 'evacalm', pose='holdlow', hand_to=(735, 1290), cup=False, gaze=-14)
    E.leash(c, (870 + 116, GY - 690 + 344), (1090, GY - 80), sag=30)      # the dog is just out of shot, right
    frame0_plinth(c, poo=False)
    bag(c, 735, 1280, 1.3)
    topbar(c, 'ITS ART')

def k13(c):   # shot 13: CU MY AI horror take: "VANDALISM!"
    park(c, 0, zoom=1.7, cy=1250)
    old = A.VISOR; A.VISOR = hx('3a0a12')
    try: ai(c, 540, 2050, 2.6, eye='wide', arms=((150, -150), (150, -150)), tilt=-8)
    finally: A.VISOR = old
    bubble(c, ['VANDALISM!'], 20, (540, 1000), cy=560, size=96)
    topbar(c, 'ITS ART')

def k14(c):   # shot 14: three-shot; Eva walks off with the bag and the dog, one brow up at Hoody. Hoody's double take
    park_bg(c)                                    # the camera follows her: the plinth is out of shot, so nothing covers her
    ai(c, 160, GY + 20, HS * .9 * AIK, eye='wide', arms=('up', 'up'), look=(16, -4))
    hoody(c, 450, GY - 20, HS * .9, expr='sheepish', arms=('rest', 'rest'), gaze=24, blink=False)
    col = E.dog(c, 990, GY, .7, look=0)
    hand = E.eva(c, 800, GY, HS * .9, 'notices', cup=False, gaze=-22, walk=.6)
    bag(c, 800 + 116 * .9 - 2, GY - 690 * .9 + 344 * .9 + 6, 1.0)
    E.leash(c, hand, col, sag=40)
    topbar(c, 'ITS ART')

def k15(c):   # shot 15, the last frame: frame-0 framing, the empty plinth; MY AI turns to eye the dog (gone off right)
    frame0_set(c, ai_eye='focus', ai_arms=('chest', 'chest'), ai_look=(30, 0), ai_turn=.4)      # Hoody exactly as frame 0
    frame0_plinth(c, poo=False)
    topbar(c, 'ITS ART')

# =====================================================================================================
# v2 (19 Nov): the rule is the SHAPE (MATCH 99% = ART); no plinth in the park, a handwritten card in the grass;
# a real gallery in one-point perspective with titled works, visitors and a guard; more lesson beats.
# =====================================================================================================
VP = (540, 1120); BW = (200, 880, 600, 1220)          # vanishing point; back wall x0, x1, top, bottom
def _side(x_s, v, left=True):
    """A point on a side wall: x_s = screen x (0..200 left wall, 880..1080 right), v = 0 floor .. 1 ceiling line."""
    u = x_s / BW[0] if left else (W - x_s) / (W - BW[1])
    top = 294 + (BW[2] - 294) * u; bot = 1279 + (BW[3] - 1279) * u
    return (x_s, bot + (top - bot) * v)

def gallery2(c, back='door', left_work=True, right_work=True, title_x=540):
    c.set_source_rgb(*hx('e3e5e9')); c.paint()                                                      # ceiling
    for i in range(3):                                                                               # skylights, receding
        k = .25 + i * .25; y0 = 30 + i * 170; y1 = y0 + 100
        xl, xr = lerp(-200, BW[0], k), lerp(W + 200, BW[1], k)
        c.move_to(xl + 120, y0); c.line_to(xr - 120, y0); c.line_to(xr - 150, y1); c.line_to(xl + 150, y1); c.close_path()
        c.set_source_rgb(*hx('f6fbff')); c.fill_preserve(); c.set_source_rgb(*hx('c4c8cf')); c.set_line_width(5); c.stroke()
    for left in (True, False):                                                                       # side walls
        xs = (0, BW[0]) if left else (W, BW[1])
        p = [_side(xs[0], 1, left), _side(xs[1], 1, left), _side(xs[1], 0, left), _side(xs[0], 0, left)]
        c.move_to(*p[0]); [c.line_to(*q) for q in p[1:]]; c.close_path(); c.set_source_rgb(*hx('ecedeb')); c.fill()
    c.rectangle(BW[0], BW[2], BW[1] - BW[0], BW[3] - BW[2]); c.set_source_rgb(*hx('fbfbf9')); c.fill()  # back wall
    g = cairo.LinearGradient(0, BW[3], 0, H); g.add_color_stop_rgb(0, *hx('c8cbd0')); g.add_color_stop_rgb(1, *hx('9da1a9'))
    c.move_to(0, 1279); c.line_to(BW[0], BW[3]); c.line_to(BW[1], BW[3]); c.line_to(W, 1279); c.line_to(W, H); c.line_to(0, H); c.close_path(); c.set_source(g); c.fill()
    for i in range(-4, 5):                                                                          # floor seams to the VP
        c.move_to(VP[0] + i * 85, BW[3]); c.line_to(VP[0] + i * 85 * 6.5, H); c.set_source_rgba(0, 0, 0, .06); c.set_line_width(3); c.stroke()
    for y in (1330, 1480, 1700): c.move_to(0, y); c.line_to(W, y); c.set_source_rgba(0, 0, 0, .05); c.set_line_width(3); c.stroke()
    for a, b in ((( 0, 1279), (BW[0], BW[3])), ((BW[0], BW[3]), (BW[1], BW[3])), ((BW[1], BW[3]), (W, 1279))):   # shadow gaps
        c.move_to(*a); c.line_to(*b); c.set_source_rgb(*hx('8d9199')); c.set_line_width(6); c.stroke()
    for x in (BW[0], BW[1]): c.move_to(x, BW[2]); c.line_to(x, BW[3]); c.set_source_rgba(0, 0, 0, .12); c.set_line_width(3); c.stroke()
    c.move_to(0, 294); c.line_to(BW[0], BW[2]); c.line_to(BW[1], BW[2]); c.line_to(W, 294); c.set_source_rgb(*hx('c4c7cd')); c.set_line_width(5); c.stroke()
    for x in (330, 540, 750): ell(c, x, BW[2] + 12, 16, 10); c.set_source_rgb(*hx('2a2d36')); c.fill()   # spot heads on the back track
    txt(c, 'MODERN ART', title_x, BW[2] + 74, 46, hx('a4a8b0'), lw=0)
    if back == 'door':                                                                              # next room through the door
        c.rectangle(470, 900, 140, BW[3] - 900); c.set_source_rgb(*hx('eceef1')); c.fill()
        c.rectangle(505, 960, 70, 90); c.set_source_rgb(*hx('ff5c4d')); c.fill()
        c.rectangle(470, 900, 140, BW[3] - 900); c.set_source_rgb(*hx('c9ccd2')); c.set_line_width(5); c.stroke()
    elif back == 'blue':
        wall_title(c, 'BLUE, MOSTLY', 400, 760, 280, 320, hx('2f6fd6'))
    if left_work: side_work(c, 40, 160, .32, .74, hx('fbf3e0'), True, kind='line')
    if right_work: side_work(c, 920, 1040, .32, .74, hx('ffcf2e'), False, kind='block')

def side_work(c, x0, x1, v0, v1, col, left, kind='line'):
    p = [_side(x0, v1, left), _side(x1, v1, left), _side(x1, v0, left), _side(x0, v0, left)]
    c.move_to(*p[0]); [c.line_to(*q) for q in p[1:]]; c.close_path(); fs(c, col, 5)
    if kind == 'line':
        a, b = lerp(p[3][0], p[2][0], .2), lerp(p[3][1], p[2][1], .2) - 30
        c.move_to(a, b); c.curve_to(a + 30, b - 120, a + 60, b + 40, lerp(p[0][0], p[1][0], .8), lerp(p[0][1], p[1][1], .8) + 40); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    else:
        q = [_side(x0 + 20, lerp(v0, v1, .3), left), _side(x1 - 20, lerp(v0, v1, .3), left)]
        c.move_to(*q[0]); c.line_to(*q[1]); c.set_source_rgb(*hx('ff5c4d')); c.set_line_width(26); c.stroke()

def wall_title(c, title, x, y, w, h, col):
    c.rectangle(x + 8, y + 10, w, h); c.set_source_rgba(0, 0, 0, .1); c.fill()
    c.rectangle(x, y, w, h); fs(c, col, 5)
    rr(c, x + w + 14, y + h - 56, 120, 50, 4); fs(c, WHITE, 3); txt(c, title, x + w + 74, y + h - 31, 15, INK, lw=0)

def visitor(c, x, gy, s, coat, hair, bag=False):
    """A gallery visitor seen from behind (no face): legs, coat, head, hair."""
    for q in (-1, 1): limb(c, [(x + q * 22 * s, gy - 250 * s), (x + q * 24 * s, gy - 12 * s)], 30 * s, hx('3b3f4a'))
    rr(c, x - 90 * s, gy - 610 * s, 180 * s, 380 * s, 60 * s); fs(c, coat, max(3, 6 * s))
    ell(c, x, gy - 680 * s, 70 * s, 76 * s); fs(c, hair, max(3, 6 * s))
    if bag: limb(c, [(x + 70 * s, gy - 560 * s), (x + 100 * s, gy - 360 * s)], 10 * s, INK); rr(c, x + 70 * s, gy - 380 * s, 70 * s, 60 * s, 10 * s); fs(c, hx('c96f3b'), max(3, 5 * s))

def guard(c, x, gy, s):
    """The gallery guard on a chair by the wall: dark uniform, cap, arms folded, half asleep."""
    rr(c, x - 70 * s, gy - 300 * s, 140 * s, 24 * s, 6 * s); fs(c, hx('2a2d36'), max(3, 5 * s))           # seat
    for q in (-1, 1): limb(c, [(x + q * 55 * s, gy - 280 * s), (x + q * 55 * s, gy)], 12 * s, hx('2a2d36'))
    for q in (-1, 1): limb(c, [(x + q * 30 * s, gy - 300 * s), (x + q * 40 * s, gy - 300 * s), (x + q * 40 * s, gy - 20 * s)], 34 * s, hx('3a4152'))
    rr(c, x - 80 * s, gy - 600 * s, 160 * s, 320 * s, 50 * s); fs(c, hx('3a4152'), max(3, 6 * s))
    rr(c, x - 70 * s, gy - 470 * s, 140 * s, 50 * s, 25 * s); fs(c, hx('3a4152'), max(3, 5 * s))           # folded arms
    ell(c, x, gy - 670 * s, 62 * s, 66 * s); fs(c, SKIN_G, max(3, 6 * s))
    for q in (-1, 1): c.move_to(x + q * 30 * s - 10 * s, gy - 670 * s); c.line_to(x + q * 30 * s + 10 * s, gy - 668 * s); c.set_source_rgb(*INK); c.set_line_width(5 * s); c.stroke()
    rr(c, x - 68 * s, gy - 742 * s, 136 * s, 44 * s, 14 * s); fs(c, hx('1f2230'), max(3, 5 * s))          # cap
    rr(c, x - 20 * s, gy - 712 * s, 100 * s, 16 * s, 8 * s); fs(c, hx('1f2230'), max(3, 4 * s))
SKIN_G = hx('d9a77e')

def stanchions(c, x0, x1, gy, h=150):
    for x in (x0, x1):
        ell(c, x, gy, 30, 10); fs(c, hx('b8bcc4'), 4); rr(c, x - 7, gy - h, 14, h, 6); fs(c, hx('d9dce2'), 4); ell(c, x, gy - h, 13, 13); fs(c, hx('d9dce2'), 4)
    c.move_to(x0, gy - h + 10); c.curve_to(x0 + (x1 - x0) * .3, gy - h + 70, x0 + (x1 - x0) * .7, gy - h + 70, x1, gy - h + 10)
    c.set_source_rgb(*INK); c.set_line_width(16); c.stroke_preserve(); c.set_source_rgb(*hx('b0222f')); c.set_line_width(10); c.stroke()

def title_lbl(c, x, y, w, title, sub='bronze, 2019', score=False):
    """A museum label on the plinth front: title + medium; score=True slaps MY AI's 10/10 sticker on its corner."""
    h = w * .46
    rr(c, x - w / 2, y, w, h, 8); fs(c, INK, 3)
    lines = title.split('|')
    if len(lines) == 1:
        size = min(w * .16, w * 1.6 / max(6, len(title))); txt(c, title, x, y + h * .38, size, WHITE, lw=0)
    else:
        for i, l in enumerate(lines): txt(c, l, x, y + h * (.26 + .28 * i), min(w * .14, w * 1.5 / max(6, len(l))), WHITE, lw=0)
    txt(c, sub, x, y + h * (.74 if len(lines) == 1 else .86), w * .1, hx('c9ccd4'), lw=0)
    if score:
        c.save(); c.translate(x + w * .42, y - 4); c.rotate(-.18); rr(c, -54, -26, 108, 52, 10); fs(c, WHITE, 5); txt(c, '10/10', 0, 0, 34, RED, lw=0); c.restore()

def reflect(c, x, gy, w, h):
    g = cairo.LinearGradient(0, gy, 0, gy + h); g.add_color_stop_rgba(0, 1, 1, 1, .35); g.add_color_stop_rgba(1, 1, 1, 1, 0)
    c.rectangle(x - w / 2, gy, w, h); c.set_source(g); c.fill()

def floor_plinth(c, x, gy, w, h, title, sub='bronze, 2019', score=False):
    """A plinth standing on the gallery floor at gy, with its reflection and its label. Returns its top y."""
    reflect(c, x, gy, w, h * .5)
    plinth(c, x, gy - h, w, h, label=False)
    title_lbl(c, x, gy - h * .55, w * .78, title, sub, score)
    return gy - h

def puddle(c, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(-110, -6); c.curve_to(-120, -40, -40, -30, -20, -44); c.curve_to(20, -58, 120, -40, 112, -12); c.curve_to(106, 6, -100, 10, -110, -6); fs(c, BRZ, 7)
    c.arc(-30, -30, 50, math.pi * 1.1, math.pi * 1.6); c.set_source_rgba(*BRZ_L, .9); c.set_line_width(8); c.stroke(); c.restore()

def bronze_ball(c, x, y, s=1.0):
    ell(c, x, y - 70 * s, 72 * s, 70 * s); fs(c, BRZ, 7)
    c.arc(x - 18 * s, y - 84 * s, 46 * s, math.pi * 1.05, math.pi * 1.6); c.set_source_rgba(*BRZ_L, .95); c.set_line_width(9); c.stroke()

def holo(c, x, y, w, h, draw):
    """MY AI's projected memory panel: a cyan frame, a soft glow, contents drawn by draw(c, x, y, w, h)."""
    rr(c, x - w / 2 - 10, y - h / 2 - 10, w + 20, h + 20, 30); c.set_source_rgba(.2, .75, 1, .18); c.fill()
    rr(c, x - w / 2, y - h / 2, w, h, 24); c.set_source_rgba(.04, .07, .14, .9); c.fill_preserve(); c.set_source_rgb(*hx('33bfff')); c.set_line_width(7); c.stroke()
    draw(c, x, y, w, h)

def beam(c, a, b, w0=20, w1=180):
    """A scan beam from MY AI's visor (a) to its target (b)."""
    dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy); nx, ny = -dy / L, dx / L
    c.move_to(a[0] + nx * w0 / 2, a[1] + ny * w0 / 2); c.line_to(b[0] + nx * w1 / 2, b[1] + ny * w1 / 2)
    c.line_to(b[0] - nx * w1 / 2, b[1] - ny * w1 / 2); c.line_to(a[0] - nx * w0 / 2, a[1] - ny * w0 / 2); c.close_path()
    c.set_source_rgba(.2, .75, 1, .22); c.fill()

def marker_txt(c, s, x, y, size, col=INK, rot=0):
    c.save(); c.translate(x, y); c.rotate(rot); c.select_font_face('Permanent Marker'); c.set_font_size(size)
    e = c.text_extents(s); c.move_to(-e.width / 2 - e.x_bearing, -e.height / 2 - e.y_bearing); c.set_source_rgb(*col); c.show_text(s); c.restore()

def label_card(c, x, ground, s=1.0, rot=-.05):
    """MY AI's card on a stick, pushed into the grass: UNTITLED (2026) in marker. x = stick, ground = where it goes in."""
    c.save(); c.translate(x, ground); c.rotate(rot); c.scale(s, s)
    rr(c, -9, -120, 18, 130, 6); fs(c, hx('d9a86c'), 5)
    rr(c, -150, -280, 300, 170, 10); fs(c, WHITE, 7)
    marker_txt(c, 'UNTITLED', 0, -218, 58); marker_txt(c, '(2026)', 0, -150, 40)
    c.restore()

# ---- park frame 0: no plinth. The poop on the grass and its card, both in the near foreground ----
POOX, CARDX, FG = 760, 400, 1880
def frame0_ground(c, poo=True):
    ell(c, POOX + 10, FG + 6, 190, 30); c.set_source_rgba(.2, .45, .2, .45); c.fill()
    label_card(c, CARDX, FG + 20, 1.0)
    if poo: poop(c, POOX, FG, 1.7)

def k01(c):   # shot 1, frame 0: "Be brutally honest."
    frame0_set(c, hoody_gaze=24); frame0_ground(c)
    bubble(c, ['BE BRUTALLY', 'HONEST.'], 20, (470, 800), cy=560, cx=640)
    topbar(c, 'ITS ART')

def k05(c):   # shot 5: the gallery. "See? This is art." He points at UNTITLED, the bronze swirl behind a rope; MY AI studies it
    gallery2(c, back='door', title_x=740)
    visitor(c, 300, 1250, .42, hx('c9b28f'), hx('3b2416'), bag=True); visitor(c, 760, 1250, .4, hx('6f7f99'), hx('9aa0aa'))
    guard(c, 960, 1300, .5)
    top = floor_plinth(c, 560, 1520, 280, 360, 'UNTITLED')
    bronze_swirl(c, 560, top - 2, 1.25)
    stanchions(c, 380, 740, 1600)
    ai(c, 905, 1840, HS * 1.15 * AIK, eye='focus', tilt=-12, look=(-16, 6), arms=('down', 'hip'))
    hoody(c, 200, 1820, HS * 1.15, expr='confident', arms=('rest', 'flail'), gaze=22, blink=False)
    bubble(c, ['SEE? THIS IS ART.'], 20, (230, 1000), cy=545, cx=470)
    topbar(c, 'HIS LESSON')

def k06(c):   # shot 6: CU MY AI scans the swirl; its memory panel saves the shape: SAVED: ART
    gallery2(c, back='door', left_work=False, title_x=330)
    top = floor_plinth(c, 250, 1330, 220, 280, 'UNTITLED'); bronze_swirl(c, 250, top - 2, 1.0)
    x, gy, s = 690, 2080, 2.3
    ai(c, x, gy, s, eye='focus', tilt=-6, look=(-20, 4), arms=('down', 'down'), turn=-.25)
    beam(c, (x - 60 * s, gy - 280 * s - 8 * s), (250, top - 90))
    def mem(c, X, Y, w, h):
        bronze_swirl(c, X, Y + 50, .75); txt(c, 'SAVED: ART', X, Y + h / 2 - 50, 50, hx('33bfff'), lw=0)
    holo(c, 690, 860, 380, 380, mem)
    topbar(c, 'HIS LESSON')

def k07(c):   # shot 7: the fast round: TWO FRIENDS, HEAVY THOUGHTS, PUDDLE (SELF-PORTRAIT), BLUE, MOSTLY - each 10/10
    gallery2(c, back='blue', right_work=False)
    visitor(c, 400, 1250, .4, hx('6f7f99'), hx('3b2416'))
    t = floor_plinth(c, 640, 1330, 170, 210, 'HEAVY|THOUGHTS', score=True); bronze_ball(c, 640, t - 2, .9)
    t = floor_plinth(c, 145, 1500, 240, 300, 'TWO FRIENDS', score=True); bronze_lumps(c, 145, t - 4, .95)
    t = floor_plinth(c, 900, 1500, 260, 280, 'PUDDLE|(SELF-PORTRAIT)', score=True); puddle(c, 900, t - 2, 1.0)
    c.save(); c.translate(625, 1050); c.rotate(-.15); rr(c, -54, -26, 108, 52, 10); fs(c, WHITE, 5); txt(c, '10/10', 0, 0, 34, RED, lw=0); c.restore()   # on BLUE, MOSTLY
    hoody(c, 420, 1890, HS * .9, expr='proud', arms=('rest', 'rest'), blink=False)
    ai(c, 690, 1900, HS * .9 * AIK, eye='happy', arms=('up', 'down'), props=(card, None), look=(14, -4), turn=.2)
    topbar(c, 'HIS LESSON')

def k10(c):   # shot 10: CU MY AI, the match: the museum swirl beside the poop, MATCH 99% = ART
    park(c, 0, zoom=1.7, cy=1250)
    for i in range(10):
        a = i * math.pi / 5; c.move_to(540 + math.cos(a) * 470, 1300 + math.sin(a) * 470); c.line_to(540 + math.cos(a) * 620, 1300 + math.sin(a) * 620)
        c.set_source_rgba(*YEL, .9); c.set_line_width(14); c.stroke()
    ai(c, 540, 2200, 2.6, eye='wide', arms=('down', 'down'))
    def mem(c, X, Y, w, h):
        bronze_swirl(c, X - 200, Y + 40, .85); txt(c, '=', X, Y - 20, 110, hx('33bfff'), lw=0); poop(c, X + 200, Y + 40, .95)
        txt(c, 'MATCH 99%', X - 100, Y + h / 2 - 50, 52, hx('33bfff'), lw=0); txt(c, '= ART', X + 190, Y + h / 2 - 50, 52, YEL, lw=0)
    holo(c, 540, 700, 860, 420, mem)
    topbar(c, 'HIS LESSON')

def k11(c):   # shot 11: MY AI pushes its card into the grass beside the poop (marker in the other mitt). Hoody looks up
    park_bg(c)
    hoody(c, 770, 1560, .8, expr='shock', arms=('rest', 'down'), prop=phone, gaze=-26, blink=False)
    poop(c, POOX, FG, 1.4)
    x, gy, s = 330, 1890, 1.3 * AIK
    hx_, hy_ = ai_hand(x, gy, s, 1, (60, 10))
    label_card(c, hx_ + 4, hy_ + 50, .85, rot=.04)                         # the stick in its mitt, its tip in the grass
    ai(c, x, gy, s, eye='happy', arms=('chest', (60, 10)), props=(marker, None), look=(14, 6), turn=.2)
    topbar(c, 'ITS ART')

def k12(c):   # shot 12: frame 0 again; Eva has stepped into the foreground and bagged it, holding the bag up. Hoody frozen
    frame0_set(c, ai_eye='heart', hoody_expr='frozen', hoody_gaze=26)
    frame0_ground(c, poo=False)
    hand = E.eva(c, 860, 1900, 1.08, 'evacalm', pose='reach', cup=False, gaze=-14)
    E.leash(c, (860 + 116 * 1.08, 1900 - 690 * 1.08 + 344 * 1.08), (1090, 1700), sag=30)       # the dog just out of shot, right
    bag(c, hand[0], hand[1] - 6, 1.3)
    topbar(c, 'ITS ART')

def k15(c):   # shot 15, the last frame: frame 0 minus the poop (the card stays); MY AI's eyes slide off right after the dog
    frame0_set(c, ai_eye='focus', ai_arms=('chest', 'chest'), ai_look=(30, 0), ai_turn=.4, hoody_gaze=24)
    frame0_ground(c, poo=False)
    topbar(c, 'ITS ART')

KEYS = [('k01', k01, '1  frame 0'), ('k02', k02, '2  10/10'), ('k05', k05, '5  museum'), ('k06', k06, '6  saved'),
        ('k07', k07, '7  10/10 round'), ('k09', k09, '9  the dog'), ('k10', k10, '10  MATCH 99%'), ('k11', k11, '11  the card'),
        ('k12', k12, '12  bagged'), ('k13', k13, '13  VANDALISM'), ('k14', k14, '14  eyebrow'), ('k15', k15, '15  last frame')]

# =====================================================================================================
# v3 (19 Nov, 12:06): frame 0 is a walk-in (they stop, hearts, tableau by 0.5 s); the end: Hoody kicks the card away,
# MY AI flinches, they walk off right over empty grass -> frame 0's walk-in. Plus the review fixes Tomas agreed:
# a bigger dog, brown inside a see-through bag, a pointing hand clear of the art, three 10/10s, Hoody's dry look.
# =====================================================================================================
AX, HX_ = 200, 480                                    # the tableau places (reached 0.5 s into the walk-in)
POOX, CARDX = 720, 440                  # (rough 3: further left, so Eva can step in beside the art fully in frame)

def bag(c, x, y, s=1.0, full=True):
    """A see-through green dog bag pinched in her fingers; the brown art clearly inside."""
    c.save(); c.translate(x, y); c.scale(s, s)
    if full:
        for w, h, dy in ((34, 16, 92), (26, 13, 72), (17, 11, 55)): ell(c, 0, dy, w, h); c.set_source_rgb(*POO); c.fill()
    c.move_to(-14, 0); c.line_to(14, 0); c.curve_to(48, 40, 52, 110, 0, 118); c.curve_to(-52, 110, -48, 40, -14, 0); c.close_path()
    c.set_source_rgba(.36, .77, .42, .45); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    c.move_to(-20, 30); c.curve_to(-30, 60, -26, 90, -14, 104); c.set_source_rgba(1, 1, 1, .6); c.set_line_width(5); c.stroke()
    c.restore()

def frame0_set(c, f=0, poo=True, ai_eye='heart', ai_arms=('chest', 'chest'), ai_look=(14, 6), ai_turn=0, hoody_expr='critic', hoody_gaze=20, ai_tilt=6,
               ax=None, hx_=None, walk=None, hoody_arms=('rest', 'chin')):
    park_bg(c, f)
    ai(c, ax or AX, GY + 20, HS * AIK, eye=ai_eye, arms=ai_arms, look=ai_look, tilt=ai_tilt, turn=ai_turn, walk=walk)
    hoody(c, hx_ or HX_, GY, HS, expr=hoody_expr, arms=hoody_arms, gaze=hoody_gaze, f=f, blink=False, step=walk)

def k00(c):   # frame 0: they walk in from the left; the poop and its card are waiting in the foreground; MY AI's eyes start to change
    frame0_set(c, ai_eye='wide', ai_arms=('down', 'down'), ai_look=(20, 6), ai_tilt=0, hoody_expr='calm', hoody_gaze=0,
               ax=150, hx_=400, walk=.9, hoody_arms=('rest', 'rest'))
    frame0_ground(c)
    topbar(c, 'ITS ART')

def k01(c):   # 0.5 s: the tableau. "Be brutally honest."
    frame0_set(c, hoody_gaze=24); frame0_ground(c)
    bubble(c, ['BE BRUTALLY', 'HONEST.'], 20, (520, 800), cy=560, cx=660)
    topbar(c, 'ITS ART')

def k05(c):   # shot 5: the gallery. "See? This is art." He points at UNTITLED (a clear gap between his finger and the art)
    gallery2(c, back='door', title_x=740)
    visitor(c, 300, 1250, .42, hx('c9b28f'), hx('3b2416'), bag=True); visitor(c, 760, 1250, .4, hx('6f7f99'), hx('9aa0aa'))
    guard(c, 960, 1300, .5)
    top = floor_plinth(c, 680, 1520, 240, 360, 'UNTITLED')
    bronze_swirl(c, 680, top - 2, 1.15)
    stanchions(c, 530, 840, 1600)
    ai(c, 935, 1840, HS * 1.15 * AIK, eye='focus', tilt=-12, look=(-16, 6), arms=('down', 'down'))
    hoody(c, 165, 1820, HS * 1.15, expr='confident', arms=('rest', 'out'), gaze=22, blink=False)
    bubble(c, ['SEE? THIS IS ART.'], 20, (200, 1000), cy=545, cx=450)
    topbar(c, 'HIS LESSON')

def k07(c):   # shot 7: the fast round - three clear 10/10s: the card at PUDDLE, stickers on TWO FRIENDS and BLUE, MOSTLY
    gallery2(c, back='blue', right_work=False)
    visitor(c, 370, 1250, .4, hx('6f7f99'), hx('3b2416'))
    t = floor_plinth(c, 640, 1420, 170, 210, 'HEAVY|THOUGHTS'); bronze_ball(c, 640, t - 2, .9)
    t = floor_plinth(c, 145, 1500, 240, 300, 'TWO FRIENDS', score=True); bronze_lumps(c, 145, t - 4, .95)
    t = floor_plinth(c, 900, 1500, 260, 280, 'PUDDLE|(SELF-PORTRAIT)'); puddle(c, 900, t - 2, 1.0)
    c.save(); c.translate(470, 800); c.rotate(-.15); rr(c, -54, -26, 108, 52, 10); fs(c, WHITE, 5); txt(c, '10/10', 0, 0, 34, RED, lw=0); c.restore()
    hoody(c, 420, 1890, HS * .9, expr='proud', arms=('rest', 'rest'), blink=False)
    ai(c, 760, 1900, HS * .9 * AIK, eye='happy', arms=('up', 'down'), props=(card, None), look=(14, -4), turn=.2)
    topbar(c, 'HIS LESSON')

def k09(c):   # shot 9: the park. The dog trots out from behind the bush, tail up; a puff behind it. Hoody on his phone. MY AI sees.
    park_bg(c)
    bush(c, 720, 1500, 1.1); puff(c, 760, 1235, 1.3)
    col = E.dog(c, 520, 1600, .95, look=1)
    hand = E.eva(c, 950, 1600, .8, 'evacalm', sip=.6, gaze=-10)
    E.leash(c, hand, col, sag=40)
    hoody(c, 300, 1640, .78, expr='calm', arms=('rest', 'take'), prop=phone, gaze=14, blink=False)
    ai(c, 130, 1660, .78 * AIK, eye='open', look=(18, 4), turn=.3)
    topbar(c, 'HIS LESSON')

def k12(c):   # shot 12: frame 0's framing; Eva has stepped into the foreground and bagged it (brown inside). Hoody frozen
    frame0_set(c, ai_eye='heart', hoody_expr='frozen', hoody_gaze=26)
    frame0_ground(c, poo=False)
    hand = E.eva(c, 870, 1900, 1.08, 'evacalm', pose='reach', cup=False, gaze=-14)
    E.leash(c, (870 + 116 * 1.08, 1900 - 690 * 1.08 + 344 * 1.08), (1090, 1700), sag=30)
    bag(c, hand[0], hand[1] - 6, 1.4)
    topbar(c, 'ITS ART')

def k14(c):   # shot 14: three-shot; Eva walks off with the bag and the dog, one brow up at Hoody. His dry "are you serious?"
    park_bg(c)
    ai(c, 160, GY + 20, HS * .9 * AIK, eye='wide', arms=('up', 'up'), look=(16, -4))
    hoody(c, 450, GY - 20, HS * .9, expr='deadpan', arms=('rest', 'rest'), gaze=24, blink=False)
    col = E.dog(c, 985, GY, .78, look=0)
    hand = E.eva(c, 790, GY, HS * .9, 'notices', cup=False, gaze=-22, walk=.6)
    bag(c, 790 + 116 * .9 - 2, GY - 690 * .9 + 344 * .9 + 6, 1.1)
    E.leash(c, hand, col, sag=40)
    topbar(c, 'ITS ART')

def hoody_kick(c, x, gy, s, expr='deadpan', gaze=0, k=1.0):
    """Hoody on his left leg, his right foot swinging forward-up (k = 0 planted .. 1 full kick). Same build as render.hoody."""
    waist = gy - 300 * s; hy = waist - 326 * s; neck = hy + 150 * s
    lean = -.08 * k
    c.save(); c.translate(x, gy); c.rotate(lean); c.translate(-x, -gy)
    hip = (x - 40 * s, waist - 10 * s); limb(c, [hip, (x - 44 * s, waist + 140 * s), (x - 44 * s, gy - 14 * s)], 40 * s, R.JEANS)
    ell(c, x - 40 * s, gy - 8 * s, 32 * s, 15 * s); fs(c, R.SHOE, max(3, 5 * s))
    hip = (x + 40 * s, waist - 10 * s); knee = (x + (44 + 90 * k) * s, waist + (140 - 70 * k) * s); foot = (x + (44 + 230 * k) * s, gy - (14 + 150 * k) * s)
    limb(c, [hip, knee, foot], 40 * s, R.JEANS)
    c.save(); c.translate(*foot); c.rotate(-.5 * k); ell(c, 10 * s, 0, 34 * s, 15 * s); fs(c, R.SHOE, max(3, 5 * s)); c.restore()
    sl, sr_ = K.hoodie(c, x, neck, s * 1.1)
    sx, sy = sl; K.arm(c, [(sx, sy), (sx - 40 * s, sy + 120 * s), (sx - 60 * s, sy + 230 * s)], s)      # near arm down
    sx, sy = sr_; K.arm(c, [(sx, sy), (sx + 100 * s, sy + 60 * s), (sx + 170 * s, sy + 20 * s)], s)     # far arm out for balance
    K.hoodyz_head(c, x, hy, s, era='young', expr=expr, blink=False, gaze=gaze)
    c.restore()
    return foot

def k15(c):   # shot 15: Hoody glances round and kicks the card away; MY AI flinches
    park_bg(c)
    ai(c, 150, GY + 20, HS * AIK, eye='wide', arms=('up', 'up'), look=(14, -6), tilt=-8)
    foot = hoody_kick(c, 470, GY, HS, expr='deadpan', gaze=16, k=1.0)
    for i in range(3):                                                        # speed lines behind the card, below its stick
        c.move_to(foot[0] - 10 + i * 40, foot[1] - 20 - i * 10); c.line_to(foot[0] + 30 + i * 40, foot[1] - 120 - i * 10)
        c.set_source_rgb(*INK); c.set_line_width(7); c.stroke()
    c.save(); c.translate(foot[0] + 70, foot[1] - 230); c.rotate(.6)         # the card, flying off right (inside the frame)
    label_card(c, 0, 0, .75, rot=0); c.restore()
    ell(c, CARDX, FG + 6, 70, 16); c.set_source_rgba(.45, .32, .2, .35); c.fill()                # the hole it left
    topbar(c, 'ITS ART')

def k16(c):   # the last frame: empty grass; they walk off right (the cut lands on frame 0's walk-in from the left)
    park_bg(c)
    ai(c, 560, GY + 20, HS * AIK, eye='open', arms=('down', 'down'), look=(18, 0), walk=2.4, turn=.3)
    hoody(c, 930, GY, HS, expr='deadpan', arms=('rest', 'rest'), gaze=20, blink=False, step=2.4)
    topbar(c, 'ITS ART')

KEYS = [('k00', k00, '0  frame 0: walk-in'), ('k01', k01, '1  0.5 s tableau'), ('k02', k02, '2  10/10'), ('k05', k05, '5  museum'),
        ('k06', k06, '6  saved'), ('k07', k07, '7  10/10 round'), ('k09', k09, '9  the dog'), ('k10', k10, '10  MATCH 99%'),
        ('k11', k11, '11  the card'), ('k12', k12, '12  bagged'), ('k13', k13, '13  VANDALISM'), ('k14', k14, '14  eyebrow'),
        ('k15', k15, '15  the kick'), ('k16', k16, '15  last frame')]

# ---- v4 (12:12): every label's text is measured and fitted inside its card or plate (it used to spill over the edges) ----
def fit(c, s, size, maxw, font='Lilita One'):
    c.save(); c.select_font_face(font); c.set_font_size(size); w = c.text_extents(s).width; c.restore()
    return size if w <= maxw else size * maxw / w

def marker_txt(c, s, x, y, size, col=INK, rot=0, maxw=None):
    if maxw: size = fit(c, s, size, maxw, 'Permanent Marker')
    c.save(); c.translate(x, y); c.rotate(rot); c.select_font_face('Permanent Marker'); c.set_font_size(size)
    e = c.text_extents(s); c.move_to(-e.width / 2 - e.x_bearing, -e.height / 2 - e.y_bearing); c.set_source_rgb(*col); c.show_text(s); c.restore()

def label_card(c, x, ground, s=1.0, rot=-.05):
    """MY AI's card on a stick: UNTITLED (2026) in marker, fitted inside the card with a 30 px margin each side."""
    c.save(); c.translate(x, ground); c.rotate(rot); c.scale(s, s)
    rr(c, -9, -120, 18, 130, 6); fs(c, hx('d9a86c'), 5)
    rr(c, -150, -280, 300, 170, 10); fs(c, WHITE, 7)
    marker_txt(c, 'UNTITLED', 0, -222, 54, maxw=240); marker_txt(c, '(2026)', 0, -152, 42, maxw=200)
    c.restore()

def title_lbl(c, x, y, w, title, sub='bronze, 2019', score=False):
    """A museum label on the plinth front: title (one or two lines) + medium, each fitted inside the plate."""
    h = w * .46; m = w * .84
    rr(c, x - w / 2, y, w, h, 8); fs(c, INK, 3)
    lines = title.split('|')
    if len(lines) == 1: txt(c, title, x, y + h * .38, fit(c, title, w * .16, m), WHITE, lw=0)
    else:
        for i, l in enumerate(lines): txt(c, l, x, y + h * (.26 + .28 * i), fit(c, l, w * .14, m), WHITE, lw=0)
    txt(c, sub, x, y + h * (.74 if len(lines) == 1 else .86), fit(c, sub, w * .1, m), hx('c9ccd4'), lw=0)
    if score:
        c.save(); c.translate(x + w * .4, y - 40); c.rotate(-.18); rr(c, -54, -26, 108, 52, 10); fs(c, WHITE, 5); txt(c, '10/10', 0, 0, 34, RED, lw=0); c.restore()

def wall_title(c, title, x, y, w, h, col):
    c.rectangle(x + 8, y + 10, w, h); c.set_source_rgba(0, 0, 0, .1); c.fill()
    c.rectangle(x, y, w, h); fs(c, col, 5)
    rr(c, x + w + 14, y + h - 56, 120, 50, 4); fs(c, WHITE, 3); txt(c, title, x + w + 74, y + h - 31, fit(c, title, 18, 100), INK, lw=0)

def card(c, x, y, q=1):
    """MY AI's 10/10 score card on a stick, held up (text fitted)."""
    limb(c, [(x, y), (x, y - 90)], 10, hx('d9a86c'))
    rr(c, x - 78, y - 210, 156, 120, 14); fs(c, WHITE, 7)
    txt(c, '10/10', x, y - 150, fit(c, '10/10', 62, 124), RED, lw=0)

# ---- v5 (12:30): the art and its card come up to the path, in the characters' plane: everything sits above y 1660,
# clear of the platforms' bottom controls (caption, likes, buttons cover roughly the bottom 250 px on a phone).
AX, HX_ = 180, 430
POOX, CARDX, FG = 860, 612, 1700
def frame0_ground(c, poo=True, card=True):
    ell(c, POOX + 6, FG + 5, 150, 22); c.set_source_rgba(.2, .45, .2, .45); c.fill()
    if card: label_card(c, CARDX, FG + 12, .9)
    if poo: poop(c, POOX, FG, 1.4)

if __name__ == '__main__':
    os.makedirs(os.path.join(HERE, 'keys'), exist_ok=True)
    want = sys.argv[1:]
    for name, fn, _ in KEYS:
        if want and name not in want: continue
        S = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(S); fn(c); S.write_to_png(os.path.join(HERE, 'keys', name + '.png'))
    if not want:
        from PIL import Image, ImageDraw, ImageFont
        tw, th = 300, 533; cols = 5; rows = math.ceil(len(KEYS) / cols)
        sheet = Image.new('RGB', (cols * tw + (cols + 1) * 16, rows * (th + 56) + 16), 'white'); d = ImageDraw.Draw(sheet)
        font = ImageFont.truetype(os.path.expanduser('~/.fonts/LilitaOne-Regular.ttf'), 30)
        for i, (name, _, lab) in enumerate(KEYS):
            x = 16 + (i % cols) * (tw + 16); y = 16 + (i // cols) * (th + 56)
            sheet.paste(Image.open(os.path.join(HERE, 'keys', name + '.png')).resize((tw, th)), (x, y)); d.text((x, y + th + 8), lab, fill='#1b2030', font=font)
        sheet.save(os.path.join(HERE, 'keys', 'sheet.png'))
    print('keys ok')
