"""Hoodyz characters for Says Here v3 (also writes the character sheet when run): Hoody's new faces, HARV's two modes, small vs full HARV,
nameplate, offer letter, the cat, the panel, the title bar; plus the dark-room TV frame at 1080x1920."""
import math, cairo, sys
sys.path.insert(0, '.')
import kit as K
from kit import INK, WHITE, NAVY, SKIN, BLUE, YEL, RED, GREY, MOUTH, TABBY, rr, fs, ell, limb, txt, shades, hx

K.ERA['young'] = dict(hair=K.HAIR_DARK, volume=1.0, beard=None, glasses=False, streak=False)
GOLD = YEL; CREAMP = hx('f5e6c5'); TEAR = hx('58c7ff')

# ---------------- Hoody's new faces ----------------
_face = K.face
def teeth_grin(c, w=40, d=100):
    c.save(); c.move_to(-w, 56); c.curve_to(-w * .7, d, w * .7, d, w, 56); c.close_path()
    c.set_source_rgb(*MOUTH); c.fill_preserve(); c.clip()
    c.rectangle(-w - 4, 50, 2 * w + 8, 18); c.set_source_rgb(*WHITE); c.fill(); c.restore()
    c.move_to(-w, 56); c.curve_to(-w * .7, d, w * .7, d, w, 56); c.close_path()
    c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
def face(c, expr, gx=0, blink=False, op=0):
    if expr == 'forced':        # eyes a little too wide, brows up, every tooth on show
        for q in (-1, 1): K.brow(c, q, 'raised'); K.eye_open(c, q, 0, big=True)
        teeth_grin(c, 44, 104)
    elif expr == 'cracked':     # the smile holds on one side and drops on the other
        K.brow(c, -1, 'raised'); K.brow(c, 1, 'worried')
        for q in (-1, 1): K.eye_open(c, q, 0)
        c.move_to(-34, 60); c.curve_to(-20, 84, 4, 84, 14, 70); c.curve_to(20, 66, 26, 74, 32, 74)
        c.set_source_rgb(*INK); c.set_line_width(7); c.stroke()
    elif expr == 'twitch':      # one eye squeezed, one wide; smile clamped flat
        K.brow(c, -1, 'angry'); K.brow(c, 1, 'raised')
        K.eye_open(c, -1, 0, lid=.62); K.eye_open(c, 1, 0, big=True)
        c.move_to(-26, 70); c.line_to(26, 66); c.set_source_rgb(*INK); c.set_line_width(7); c.stroke()
        for i, (dx, dy) in enumerate(((-86, -10), (-96, 14), (-84, 34))):   # twitch marks
            c.move_to(dx - 46, dy); c.line_to(dx - 66, dy + (i - 1) * 8); c.set_line_width(5); c.stroke()
    elif expr == 'cry':         # grateful, eyes shut, tears running, wobbly grin
        for q in (-1, 1): K.brow(c, q, 'worried'); K.eye_closed(c, q, True)
        for q in (-1, 1): limb(c, [(q * 40, 30), (q * 46, 70), (q * 52, 112)], 12, TEAR)
        K.blush(c); teeth_grin(c, 36, 96)
    elif expr == 'blown':       # the shout
        ell(c, 0, 20, 96, 80); c.set_source_rgba(*RED, .22); c.fill()
        for q in (-1, 1): K.brow(c, q, 'angry'); K.eye_open(c, q, 0, big=True)
        ell(c, 0, 78, 40, 36); fs(c, MOUTH, 6)
        c.save(); ell(c, 0, 78, 40, 36); c.clip(); c.rectangle(-44, 38, 88, 16); c.set_source_rgb(*WHITE); c.fill()
        ell(c, 0, 108, 22, 12); c.set_source_rgb(*hx('ff8fa6')); c.fill(); c.restore()
    elif expr == 'tvstare':     # dark room: lids half down, eyes up at the screen
        for q in (-1, 1):
            K.brow(c, q, 'flat')
            ell(c, q * 42, 2, 23, 25); c.set_source_rgb(*INK); c.fill()
            ell(c, q * 36, -10, 7, 7); c.set_source_rgb(*WHITE); c.fill()
            c.rectangle(q * 42 - 30, -26, 60, 22); c.set_source_rgb(*SKIN); c.fill()
            c.move_to(q * 42 - 26, -4); c.line_to(q * 42 + 26, -4); c.set_source_rgb(*INK); c.set_line_width(7); c.stroke()
        c.move_to(-18, 70); c.line_to(18, 70); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    else: _face(c, expr, gx, blink, op)
K.face = face

def sweat(c, x, y, s):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(0, -26); c.curve_to(14, -4, 18, 8, 0, 18); c.curve_to(-18, 8, -14, -4, 0, -26); c.close_path()
    fs(c, TEAR, 5); c.restore()

def hoody(c, x, y, s, expr, gold=True, body=True):
    if body: K.hoodie(c, x, y + 150 * s, s * 1.1)
    K.hoodyz_head(c, x, y, s, era='young', expr=expr, blink=False)
    if gold: shades(c, x + 6 * s, y - 112 * s, .78 * s, rot=-.06)      # the gold shades, pushed up on his head

# ---------------- HARV ----------------
def harv(c, x, y, s, shade=True, mouth='flat', arm=None, eyes=(0, 0)):
    """HARV: the boss robot from says-here-boss/v2 (white face, no visor) + mouth line under the shades.
    mouth: flat | fond | smile. arm: None, 'point' (Professor gesture to the viewer's left), 'adjust' (hand at the shades)."""
    sh_l, sh_r = (x - 70 * s, y + 110 * s), (x + 70 * s, y + 110 * s)
    if arm == 'point':
        limb(c, [sh_l, (x - 170 * s, y + 70 * s), (x - 260 * s, y + 10 * s)], 34 * s, WHITE)
        limb(c, [(x - 262 * s, y + 8 * s), (x - 400 * s, y + 20 * s)], 7 * s, hx('8b5a2b'))     # lecturer's pointer
        ell(c, x - 400 * s, y + 20 * s, 7 * s, 7 * s); c.set_source_rgb(*RED); c.fill()
        ell(c, x - 262 * s, y + 6 * s, 28 * s, 28 * s); fs(c, WHITE, 7 * s)
    if arm == 'adjust':
        limb(c, [sh_r, (x + 150 * s, y + 40 * s), (x + 96 * s, y - 20 * s)], 34 * s, WHITE)
    c.save(); c.translate(x, y); c.scale(s, s); c.set_line_cap(cairo.LINE_CAP_ROUND)
    rr(c, -72, 85, 144, 135, 44); fs(c, WHITE)
    ell(c, 0, 150, 30, 30); fs(c, (.82, .86, .93), 5)
    c.move_to(0, -90); c.line_to(0, -132); c.set_source_rgb(*INK); c.set_line_width(9); c.stroke()
    ell(c, 0, -140, 17, 17); fs(c, BLUE, 7)
    for q in (-1, 1): ell(c, q * 110, 0, 22, 38); fs(c, GREY, 8)
    rr(c, -108, -95, 216, 180, 78); fs(c, WHITE)
    if shade: shades(c, 0, -12, 1.02)
    else:
        for q in (-1, 1): ell(c, q * 42 + eyes[0], -14 + eyes[1], 17, 22); c.set_source_rgb(*BLUE); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(8)
    if mouth == 'flat': c.move_to(-20, 52); c.line_to(30, 52)
    elif mouth == 'fond': c.move_to(-20, 50); c.curve_to(-6, 58, 18, 58, 30, 48)
    else: c.move_to(-26, 46); c.curve_to(-10, 66, 22, 66, 36, 44)
    c.stroke(); c.restore()
    if arm == 'adjust': ell(c, x + 96 * s, y - 24 * s, 24 * s, 24 * s); fs(c, WHITE, 7 * s)

def nameplate(c, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    rr(c, -380, -90, 760, 180, 18); fs(c, CREAMP, 8)
    txt(c, 'PROF. HARV, PhD', 0, -30, 76, INK, lw=0)
    txt(c, 'HEAD OF HUMAN RESOURCES', 0, 46, 44, hx('66707f'), lw=0)
    c.restore()

def offer(c, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s); c.rotate(-.025)
    rr(c, -330, -400, 660, 800, 26); fs(c, hx('fbf8ee'), 10)
    txt(c, 'OFFER LETTER', 0, -330, 62, INK, lw=0)
    c.rectangle(-270, -282, 540, 7); c.set_source_rgb(*INK); c.fill()
    txt(c, 'ROLE:', -270, -220, 44, hx('66707f'), lw=0, align='l')
    txt(c, 'PROMPT ENGINEER', -270, -160, 64, INK, lw=0, align='l')
    txt(c, 'PAY:', -270, -80, 44, hx('66707f'), lw=0, align='l')
    txt(c, '9.99', 0, 70, 250, RED, lw=0)
    txt(c, 'TOKENS / HOUR', 0, 230, 56, INK, lw=0)
    c.restore()

def cat_one_eye(c, x, gy, s, look=-1, open_eye=True):
    K.cat(c, x, gy, s, pose='sleep', look=look)
    if not open_eye: return
    c.save(); c.translate(x, gy); c.scale(s * look, s); c.translate(92, -52); c.scale(.95, .95)
    ell(c, 28, -2, 17, 14); c.set_source_rgb(*TABBY); c.fill()
    ell(c, 30, -4, 11, 14); fs(c, hx('b8e04a'), 4); ell(c, 27, -4, 4, 10); c.set_source_rgb(*INK); c.fill()
    c.restore()

def topbar(c, pill, y0=222):
    """ME + MY AI series bar: the Hoodyz badge (hoodie icon + HOODYZ), the title, and a pill with the story state.
    Drawn in screen space. The title shrinks only if a long pill would crowd it."""
    c.save(); c.identity_matrix()
    rr(c, 40, y0, 1000, 138, 40); fs(c, WHITE, 8)
    iy = y0 + 69
    rr(c, 58, iy - 38, 196, 76, 38); c.set_source_rgb(*NAVY); c.fill()                    # Hoodyz badge
    c.save(); c.translate(96, iy + 2); c.scale(.62, .62)
    c.move_to(-34, 34); c.line_to(-34, -4); c.curve_to(-34, -46, 34, -46, 34, -4); c.line_to(34, 34); c.close_path()
    c.set_source_rgb(*WHITE); c.fill(); ell(c, 0, -2, 20, 18); c.set_source_rgb(*SKIN); c.fill(); c.restore()
    txt(c, 'HOODYZ', 124, iy, 31, WHITE, lw=0, align='l')
    c.select_font_face('Lilita One'); c.set_font_size(58); w = max(200, c.text_extents(pill).width + 96)
    px = 1020 - w / 2
    size = 68; c.set_font_size(size); tw = c.text_extents('ME + MY AI').width; room = (px - w / 2 - 22) - 274
    if tw > room: size *= room / tw
    txt(c, 'ME + MY AI', 274, iy, size, NAVY, lw=0, align='l')
    rr(c, px - w / 2, iy - 44, w, 88, 44); fs(c, YEL, 7); txt(c, pill, px, iy, 58, INK, lw=0)
    c.restore()

def label(c, s, x, y, size=40, col=INK): txt(c, s, x, y, size, col, lw=0)
def section(c, s, y): txt(c, s, 60, y, 56, NAVY, lw=0, align='l'); c.rectangle(60, y + 34, 2040, 5); c.set_source_rgb(*NAVY); c.fill()

def sheet():
    Wd, Ht = 2160, 3000
    S = cairo.ImageSurface(cairo.FORMAT_RGB24, Wd, Ht); c = cairo.Context(S)
    c.set_source_rgb(*hx('eef1f6')); c.paint()
    txt(c, 'HOODYZ  -  SAYS HERE v3  -  CHARACTER SHEET', 1080, 60, 60, INK, lw=0)

    section(c, 'HOODY - the faces Says Here needs', 130)
    for i, (e, l1, l2) in enumerate([('forced', 'FORCED SMILE', 'grin held, sweat rolls'), ('cracked', 'CRACKED', 'one side collapses'),
                                     ('twitch', 'EYE TWITCH', 'two quick lid snaps'), ('cry', 'CRYING THANKS', 'tears run on a loop'),
                                     ('blown', 'BLOWN', 'mouth pops, holds')]):
        x = 230 + i * 425
        hoody(c, x, 420, 1.05, e, gold=(i == 0))
        if e == 'forced': sweat(c, x + 118, 380, 1.0)
        label(c, l1, x, 812); label(c, l2, x, 852, 32, hx('66707f'))

    section(c, 'HARV - one design, two faces', 920)
    cells = [('HR MODE', 'still. the desk'), ('PROFESSOR MODE', 'gesturing. the podcast'),
             ('THE ADJUST', '"I\'ve had these for years."'), ('2026 vs 2027', 'shades from the theft on. never off')]
    harv(c, 230, 1200, 1.15, mouth='flat')
    harv(c, 900, 1200, 1.0, mouth='flat', arm='point')
    harv(c, 1330, 1200, 1.0, mouth='flat', arm='adjust')
    harv(c, 1760, 1270, .55, shade=False, mouth='flat', eyes=(0, -2))
    harv(c, 1980, 1180, 1.0, mouth='flat')
    for i, (a, b) in enumerate(cells):
        x = [230, 780, 1330, 1860][i]; label(c, a, x, 1500); label(c, b, x, 1546, 32, hx('66707f'))
    label(c, 'No visor - every other robot has one. Mouth always flat - HARV never smiles.', 1080, 1600, 34, hx('9a3412'))

    section(c, 'PROPS', 1660)
    nameplate(c, 520, 1830, .95)
    label(c, 'nameplate + TV lower third', 520, 1960, 32, hx('66707f'))
    offer(c, 1240, 2250, .62)
    label(c, 'offer letter (shot 14)', 1240, 2540, 32, hx('66707f'))
    c.save(); shades(c, 1820, 1840, 1.6); c.restore()
    label(c, 'the gold shades', 1820, 1960, 32, hx('66707f'))
    cat_one_eye(c, 360, 2140, 1.15, open_eye=False); label(c, 'THE CAT - asleep', 360, 2225, 36)
    cat_one_eye(c, 360, 2430, 1.15, open_eye=True); label(c, 'one eye - shot 19', 360, 2515, 36)
    K.robot(c, 1700, 2330, .8, eye=(14, 0)); K.robot(c, 2000, 2330, .8, eye=(-14, 0))
    label(c, 'THE PANEL - the glance (shot 19)', 1850, 2560, 36)

    section(c, 'TITLE BAR', 2650)
    c.save(); c.translate(0, 2740 - 222); c.scale(1, 1)
    topbar(c, '2027'); c.translate(1080, 0); topbar(c, 'REWIND'); c.restore()
    S.write_to_png('character_sheet.png')

# ---------------- the dark-room frame ----------------
def darkroom(f=0):
    S = cairo.ImageSurface(cairo.FORMAT_RGB24, 1080, 1920); c = cairo.Context(S)
    darkroom_draw(c); S.write_to_png('darkroom.png')

def darkroom_draw(c, t=1.0, bob=0.0):
    """t: how much of the HUMANS line has been drawn (0..1); bob: HARV's pointer nod in px."""
    c.set_source_rgb(*hx('070b18')); c.paint()
    g = cairo.RadialGradient(540, 760, 60, 540, 900, 1100)
    g.add_color_stop_rgba(0, .36, .48, .9, .55); g.add_color_stop_rgba(1, .36, .48, .9, 0)
    c.set_source(g); c.paint()
    # TV
    X0, Y0, X1, Y1 = 90, 440, 990, 1010
    rr(c, X0 - 24, Y0 - 24, X1 - X0 + 48, Y1 - Y0 + 48, 30); fs(c, hx('15171f'), 10)
    c.rectangle(500, Y1 + 24, 80, 60); c.set_source_rgb(*hx('15171f')); c.fill()
    c.save(); rr(c, X0, Y0, X1 - X0, Y1 - Y0, 12); c.clip()
    gs = cairo.LinearGradient(0, Y0, 0, Y1); gs.add_color_stop_rgb(0, *hx('3b1f5c')); gs.add_color_stop_rgb(1, *hx('c2410c'))
    c.set_source(gs); c.paint()
    for i in range(7):   # studio light strips
        c.rectangle(X0 + 40 + i * 130, Y0, 14, Y1 - Y0); c.set_source_rgba(1, 1, 1, .05); c.fill()
    # graph board
    rr(c, 120, 480, 430, 340, 18); fs(c, WHITE, 7)
    c.move_to(160, 510); c.line_to(160, 780); c.line_to(520, 780); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    pts = [(170, 560), (300, 570), (360, 590), (395, 610), (420, 700), (440, 770)]
    seg = [math.dist(a, b) for a, b in zip(pts, pts[1:])]; L = sum(seg) * max(.02, min(1, t))
    c.move_to(*pts[0])
    for (a, b), d in zip(zip(pts, pts[1:]), seg):
        if L <= 0: break
        k = min(1, L / d); c.line_to(a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k); L -= d
    c.set_source_rgb(*RED); c.set_line_width(18); c.set_line_join(cairo.LINE_JOIN_ROUND); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
    if t >= 1:
        c.move_to(424, 752); c.line_to(440, 790); c.line_to(462, 756); c.set_source_rgb(*RED); c.set_line_width(14); c.stroke()
    txt(c, 'HUMANS', 270, 528, 46, RED, lw=0)
    # neon show title
    txt(c, 'THE HUMAN TOUCH', 770, 494, 46, hx('ff7ab8'), lw=6, st=hx('5b0d2a'))
    # desk, mic, HARV
    harv(c, 800, 690 + bob, .95, mouth='flat', arm='point')
    rr(c, 560, 830, 430, 200, 20); fs(c, hx('2a1d3a'), 7)
    limb(c, [(640, 830), (640, 790), (670, 760)], 10, INK); ell(c, 682, 748, 22, 30); fs(c, hx('22242e'), 6)
    # lower third
    rr(c, X0 - 20, 892, 560, 108, 0); c.set_source_rgba(.04, .06, .14, .92); c.fill()
    c.rectangle(X0 - 20, 892, 14, 108); c.set_source_rgb(*YEL); c.fill()
    txt(c, 'PROF. HARV, PhD', 130, 928, 46, WHITE, lw=0, align='l')
    txt(c, 'HEAD OF HUMAN RESOURCES', 130, 974, 30, YEL, lw=0, align='l')
    c.restore()
    # screen glare
    c.save(); rr(c, X0, Y0, X1 - X0, Y1 - Y0, 12); c.clip()
    c.move_to(X0, Y0); c.line_to(X0 + 260, Y0); c.line_to(X0, Y0 + 220); c.close_path(); c.set_source_rgba(1, 1, 1, .06); c.fill(); c.restore()
    # sofa
    rr(c, 40, 1230, 1000, 330, 70); fs(c, hx('1d3557'), 10)
    rr(c, 40, 1470, 1000, 300, 60); fs(c, hx('274472'), 10)
    # cat asleep on the sofa
    K.cat(c, 830, 1490, .9, pose='sleep', look=-1)
    # Hoody, staring up at the TV, laptop on his knees
    hoody(c, 430, 1290, 1.05, 'tvstare', gold=False)
    rr(c, 280, 1470, 310, 190, 14); fs(c, hx('2b2f3a'), 8)
    rr(c, 298, 1486, 274, 156, 8); c.set_source_rgb(*hx('dde7f5')); c.fill()
    c.move_to(270, 1662); c.line_to(600, 1662); c.line_to(640, 1712); c.line_to(230, 1712); c.close_path(); fs(c, hx('3a3f4d'), 8)
    txt(c, 'JOBS', 435, 1516, 42, NAVY, lw=0)
    for i in range(3):
        rr(c, 314, 1552 + i * 28, 170, 16, 8); c.set_source_rgb(*hx('9fb0c8')); c.fill()
        rr(c, 494, 1550 + i * 28, 66, 20, 10); c.set_source_rgb(*hx('22c55e')); c.fill()
    for q, (hx_, hy_) in ((-1, (290, 1690)), (1, (580, 1690))):
        K.arm(c, [(430 + q * 90, 1470), (430 + q * 140, 1560), (hx_, hy_)], 1.0)
    # TV light on the room
    c.rectangle(0, 1100, 1080, 820); c.set_source_rgba(.1, .16, .4, .28); c.fill()
    topbar(c, '2027')

if __name__ == '__main__':
    sheet()
