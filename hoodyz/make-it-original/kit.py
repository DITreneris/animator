"""Make It Original: the episode's drawing kit.
Self-contained copy of the series helpers (from whos-a-good-boy/v3: v.py, chars.py) plus the new
characters and props. Every function draws at a world point with a scale; frame-deterministic."""
import cairo, math, random
W, H, FPS = 1080, 1920, 30
INK = (.07, .08, .13); WHITE = (1, 1, 1); NAVY = (.11, .15, .27); SKIN = (1, .87, .76)
BLUE = (.2, .75, 1); YEL = (1, .84, .15); RED = (.95, .2, .25); GREEN = (.15, .8, .42); GREY = (.62, .65, .72)
hx = lambda h: tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
cl = lambda t: max(0, min(1, t)); lerp = lambda a, b, t: a + (b - a) * t
ss = lambda t: (lambda u: u * u * (3 - 2 * u))(cl(t))
HAIR_DARK = (.25, .13, .09); HAIR_GREY = (.72, .72, .76); ROSE = (1, .55, .6)
DENIM = hx('4a78b8'); TABBY = hx('f08a2c'); TABBY_D = hx('b85a14'); CREAM = hx('fde2b8')
GUITAR = hx('1fb5a8'); MOUTH = hx('7a2230')

def rr(c, x, y, w, h, r):
    c.new_sub_path(); c.arc(x + w - r, y + r, r, -math.pi / 2, 0); c.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    c.arc(x + r, y + h - r, r, math.pi / 2, math.pi); c.arc(x + r, y + r, r, math.pi, 1.5 * math.pi); c.close_path()
def fs(c, fill, lw=8, st=INK):
    c.set_source_rgb(*fill)
    if lw: c.fill_preserve(); c.set_source_rgb(*st); c.set_line_width(lw); c.stroke()
    else: c.fill()
def ell(c, x, y, a, b):
    c.save(); c.translate(x, y); c.scale(max(a, .01), max(b, .01)); c.new_sub_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
def limb(c, pts, w, col):
    c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND)
    for lw, cc in ((w + 14, INK), (w, col)):
        c.move_to(*pts[0])
        for p in pts[1:]: c.line_to(*p)
        c.set_source_rgb(*cc); c.set_line_width(lw); c.stroke()
def txt(c, s, x, y, size, fill=WHITE, lw=None, st=INK, rot=0, align='c', alpha=1):
    c.save(); c.select_font_face('Lilita One'); c.set_font_size(size); e = c.text_extents(s)
    c.translate(x, y); c.rotate(rot)
    ox = -e.width / 2 - e.x_bearing if align == 'c' else (-e.x_bearing if align == 'l' else -e.width - e.x_bearing)
    c.move_to(ox, size * .36); c.text_path(s); c.set_line_join(cairo.LINE_JOIN_ROUND)
    lw = size * .16 if lw is None else lw
    if lw: c.set_source_rgba(*st, alpha); c.set_line_width(lw); c.stroke_preserve()
    c.set_source_rgba(*fill, alpha); c.fill(); c.restore()
def shadow(c, x, y, w):
    ell(c, x, y, w, w * .16); c.set_source_rgba(.1, .12, .18, .18); c.fill()
def blinking(f, seed):
    w = f // 84; o = random.Random(w * 31 + seed).randint(0, 76); return o <= f % 84 < o + 3
def shades(c, x, y, s, rot=0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    rr(c, -92, -28, 84, 58, 22); rr(c, 8, -28, 84, 58, 22); c.set_source_rgb(.04, .04, .07); c.fill_preserve()
    c.set_source_rgb(*YEL); c.set_line_width(8); c.stroke(); c.set_source_rgb(*YEL); c.set_line_width(10)
    c.move_to(-10, -14); c.line_to(10, -14); c.stroke(); c.restore()

# ---------------- faces ----------------
def eye_open(c, q, gx, big=False, lid=0, narrow=False):
    ey = 8
    if big:
        ell(c, q * 42, ey, 30, 34); fs(c, WHITE, 6); ell(c, q * 42 + gx * .6, ey, 10, 12); c.set_source_rgb(*INK); c.fill(); return
    h = 14 if narrow else 27
    ell(c, q * 42 + gx * .5, ey + (6 if narrow else 0), 23, h); c.set_source_rgb(*INK); c.fill()
    ell(c, q * 34 + gx * .5, ey - 8, 7, 7); c.set_source_rgb(1, 1, 1); c.fill()
    if lid:
        c.rectangle(q * 42 - 30, ey - 34, 60, 34 * lid + 2); c.set_source_rgb(*SKIN); c.fill()
        c.move_to(q * 42 - 26, ey - 34 + 34 * lid); c.line_to(q * 42 + 26, ey - 34 + 34 * lid)
        c.set_source_rgb(*INK); c.set_line_width(7); c.stroke()
def eye_closed(c, q, happy=True):
    if happy: c.move_to(q * 62, 22); c.curve_to(q * 50, 0, q * 20, 0, q * 12, 22)
    else: c.move_to(q * 62, 10); c.curve_to(q * 50, 18, q * 22, 18, q * 14, 10)
    c.set_source_rgb(*INK); c.set_line_width(9); c.stroke()
def brow(c, q, kind):
    if not kind: return
    if kind == 'angry': c.move_to(q * 74, -34); c.line_to(q * 18, -12)
    elif kind == 'worried': c.move_to(q * 72, -22); c.line_to(q * 20, -40)
    elif kind == 'raised': c.move_to(q * 72, -38); c.curve_to(q * 56, -56, q * 30, -56, q * 18, -42)
    elif kind == 'flat': c.move_to(q * 70, -26); c.line_to(q * 20, -26)
    elif kind == 'up': c.move_to(q * 72, -46); c.curve_to(q * 56, -66, q * 30, -66, q * 18, -50)
    c.set_source_rgb(*INK); c.set_line_width(9); c.stroke()
def mouth(c, kind, op):
    c.set_source_rgb(*INK); c.set_line_width(6)
    if op > 0:
        h = 8 + op * 26; ell(c, 0, 70, 16 + op * 6, h / 2 + 4); fs(c, MOUTH, 6); return
    if kind == 'smile': c.arc(-11, 62, 11, .2, math.pi - .1); c.new_sub_path(); c.arc(11, 62, 11, .1, math.pi - .2); c.stroke()
    elif kind == 'grin': c.move_to(-30, 60); c.curve_to(-20, 96, 20, 96, 30, 60); c.close_path(); fs(c, MOUTH, 6)
    elif kind == 'o': ell(c, 0, 72, 13, 17); fs(c, MOUTH, 5)
    elif kind == 'flat': c.move_to(-18, 68); c.line_to(18, 68); c.stroke()
    elif kind == 'frown': c.arc(0, 84, 18, math.pi + .5, 2 * math.pi - .5); c.stroke()
    elif kind == 'wobble': c.move_to(-22, 70); c.curve_to(-10, 60, -4, 80, 6, 68); c.curve_to(12, 62, 18, 74, 24, 68); c.stroke()
    elif kind == 'smirk': c.set_line_width(8); c.move_to(-20, 70); c.curve_to(0, 74, 18, 70, 30, 56); c.stroke()
    elif kind == 'meh': c.set_line_width(8); c.move_to(-20, 72); c.curve_to(-6, 66, 8, 66, 20, 74); c.stroke()
def blush(c):
    for q in (-1, 1): ell(c, q * 62, 44, 18, 10); c.set_source_rgba(*ROSE, .55); c.fill()
# expression -> (eyes, brows (left,right), mouth)
FACES = {
    'calm': ('open', (None, None), 'smile'), 'happy': ('happy', (None, None), 'grin'),
    'hopeful': ('open', ('raised', 'raised'), 'grin'), 'shock': ('big', ('raised', 'raised'), 'o'),
    'deadpan': ('half', ('flat', 'flat'), 'flat'), 'sheepish': ('open', ('worried', 'worried'), 'wobble'),
    'polite': ('half', (None, None), 'smile'),
    'smug': ('smug', ('flat', 'up'), 'smirk'),              # half-lidded, one brow up, smirk
    'dismissive': ('shut', ('raised', 'raised'), 'meh'),    # eyes closed, brows up, "meh" mouth
    'confident': ('open', ('flat', 'flat'), 'grin'),
}
def face(c, expr, gx=0, blink=False, op=0):
    e, (bl, br), m = FACES.get(expr, FACES['calm'])
    for q, b in ((-1, bl), (1, br)):
        brow(c, q, b)
        if e == 'happy': eye_closed(c, q, True)
        elif e == 'shut' or blink: eye_closed(c, q, False)
        elif e == 'big': eye_open(c, q, gx, big=True)
        elif e == 'half': eye_open(c, q, gx, lid=.5)
        elif e == 'smug': eye_open(c, q, 10, lid=.55)
        else: eye_open(c, q, gx)
    if expr in ('happy',): blush(c)
    if m: mouth(c, m, op)

# ---------------- Hoodyz (and the drummer) ----------------
ERA = {
    1986: dict(hair=HAIR_DARK, volume=1.2, beard=None, glasses=False, streak=False),
    2016: dict(hair=HAIR_DARK, volume=1.0, beard='short', glasses=False, streak=True),
    2026: dict(hair=HAIR_GREY, volume=.92, beard='full', glasses=True, streak=False),
}
BLOBS = [(-92, -58, 48), (-55, -104, 54), (5, -122, 58), (62, -100, 52), (98, -52, 44), (-108, -8, 32), (112, -6, 30), (-25, -132, 36), (40, -136, 32)]
def _hair(c, hair, vol, bob):
    bl = [(x * (1 + (vol - 1) * .55), y * vol - (vol - 1) * 30, r * (1 + (vol - 1) * .8)) for x, y, r in BLOBS]
    if vol > 1.1: bl += [(-130, 20, 38), (132, 22, 36), (-118, 60, 30), (120, 62, 28)]   # '80s volume over the ears
    return bl
def hoodyz_head(c, x, y, s, era=2026, expr='calm', f=0, rot=0, op=0, gaze=0, blink=None):
    E = ERA[era]; hair = E['hair']
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    bob = math.sin(f * .5) * 2
    bl = _hair(c, hair, E['volume'], bob)
    for b in bl: ell(c, b[0], b[1] + bob, b[2], b[2])
    c.set_source_rgb(*INK); c.set_line_width(16); c.stroke()
    for q in (-1, 1): ell(c, q * 104, 18, 18, 24); fs(c, SKIN, 7)
    rr(c, -100, -72, 200, 178, 84); fs(c, SKIN)
    bcol = hair if era != 2016 else (.36, .26, .22)
    if E['beard']:
        c.save(); rr(c, -100, -72, 200, 178, 84); c.clip()
        if E['beard'] == 'full': ell(c, 0, 116, 108, 72)
        else: ell(c, 0, 124, 100, 56)
        c.set_source_rgb(*bcol); c.fill(); ell(c, 0, 68, 40, 24); c.set_source_rgb(*SKIN); c.fill(); c.restore()
    for b in bl: ell(c, b[0], b[1] + bob, b[2], b[2])
    c.set_source_rgb(*hair); c.fill()
    for bx, by, br in [(-72, -66, 30), (-30, -80, 31), (18, -84, 30), (62, -66, 28)]:   # fringe lifted: brows sit on skin
        ell(c, bx * (1 + (E['volume'] - 1) * .4), by, br, br); c.fill()
    if E['streak']:
        for bx, by, br in [(-60, -70, 26), (-36, -96, 24), (-20, -120, 20)]:
            ell(c, bx, by + bob * .5, br, br); c.set_source_rgb(*HAIR_GREY); c.fill()
    face(c, expr, gaze, blinking(f, 3) if blink is None else blink, op)
    if E['glasses']:
        for q in (-1, 1):
            ell(c, q * 44, 10, 36, 32); c.set_source_rgb(*INK); c.set_line_width(7); c.stroke()
        c.move_to(-10, 6); c.curve_to(-4, 0, 4, 0, 10, 6); c.stroke()
        c.move_to(-80, 6); c.line_to(-100, 0); c.move_to(80, 6); c.line_to(100, 0); c.stroke()
    c.restore()

def hoodie(c, x, y, s, col=NAVY):
    """Torso anchored at the neck (x, y). Returns shoulder points (left, right) in canvas coords."""
    c.save(); c.translate(x, y); c.scale(s, s)
    rr(c, -92, -30, 184, 190, 60); fs(c, col)
    ell(c, 0, -16, 74, 34); fs(c, hx('0b1020'), 6)
    for q in (-1, 1):
        c.move_to(q * 16, 0); c.line_to(q * 18, 56); c.set_source_rgb(.95, .95, .98); c.set_line_width(7); c.stroke()
    c.restore()
    return (x - 82 * s, y + 20 * s), (x + 82 * s, y + 20 * s)

def hand(c, x, y, s):
    ell(c, x, y, 26 * s, 26 * s); fs(c, SKIN, 7)

def palm(c, x, y, s, ang, flick=1.0):
    """Open hand, fingers along ang (radians), thumb up; flick>0 adds motion arcs."""
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    for i in range(4):   # fingers
        rr(c, 10, -24 + i * 13, 54 - abs(i - 1.5) * 8, 14, 7); fs(c, SKIN, 5)
    rr(c, -20, -30, 44, 60, 20); fs(c, SKIN, 6)
    c.move_to(0, -26); c.curve_to(6, -52, 20, -58, 28, -50); c.set_source_rgb(*INK); c.set_line_width(18); c.stroke()
    c.move_to(0, -26); c.curve_to(6, -52, 20, -58, 28, -50); c.set_source_rgb(*SKIN); c.set_line_width(10); c.stroke()
    if flick > 0:
        for r in (88, 112):
            c.arc(-10, 0, r, -.9, .9); c.set_source_rgba(*INK, .55 * flick); c.set_line_width(7); c.stroke()
    c.restore()
def arm(c, pts, s, col=NAVY, flick=None):
    limb(c, pts, 44 * s, col)
    if flick is None: hand(c, pts[-1][0], pts[-1][1], s)
    else:
        (ax, ay), (bx, by) = pts[-2], pts[-1]
        palm(c, bx, by, s, math.atan2(by - ay, bx - ax) + .55, flick)

def waveoff(sh, s, k, side=1):
    """The wave-off flick for the arm at shoulder sh. k: 0 rest, .35 forearm up, .6 flick wide (hold), 1 dropped.
    side=1 flicks to the viewer's right. Returns arm points."""
    sx, sy = sh
    rest = [(sx, sy), (sx + side * 30 * s, sy + 110 * s), (sx + side * 20 * s, sy + 200 * s)]
    up = [(sx, sy), (sx + side * 70 * s, sy + 60 * s), (sx + side * 40 * s, sy - 40 * s)]          # forearm up, hand by chin
    wide = [(sx, sy), (sx + side * 110 * s, sy + 40 * s), (sx + side * 225 * s, sy - 5 * s)]       # arm out to the side, back-hand brush outward
    if k < .35: a, b, t = rest, up, k / .35
    elif k < .45: a, b, t = up, wide, (k - .35) / .1
    elif k < .8: a, b, t = wide, wide, 0
    else: a, b, t = wide, rest, (k - .8) / .2
    t = ss(t); return [(lerp(p[0], q[0], t), lerp(p[1], q[1], t)) for p, q in zip(a, b)]

def drummer_head(c, x, y, s, expr='deadpan', f=0, rot=0, op=0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    hair = hx('6b3e1e')
    # mullet: short spiky top, long back down to the shoulders
    for q in (-1, 1):   # mullet: two long locks behind the ears, down to the shoulders
        c.move_to(q * 70, -40); c.curve_to(q * 150, 10, q * 150, 140, q * 120, 200); c.line_to(q * 70, 190); c.curve_to(q * 96, 120, q * 96, 40, q * 60, 0); c.close_path()
        fs(c, hair, 8)
    for q in (-1, 1): ell(c, q * 104, 18, 18, 24); fs(c, SKIN, 7)
    rr(c, -100, -72, 200, 178, 84); fs(c, SKIN)
    for i, (bx, by, br) in enumerate([(-70, -70, 40), (-30, -96, 44), (20, -100, 44), (64, -76, 40)]):
        ell(c, bx, by, br, br * .8); c.set_source_rgb(*hair); c.fill()
    face(c, expr, 0, blinking(f, 5), op)
    shades(c, 0, -96, .82)          # pushed up on the head
    c.restore()

def vest(c, x, y, s):
    """Sleeveless denim vest over a white tee. Returns shoulders."""
    c.save(); c.translate(x, y); c.scale(s, s)
    rr(c, -92, -30, 184, 190, 60); fs(c, WHITE)
    for q in (-1, 1):
        c.move_to(q * 92, 20); c.line_to(q * 92, 150); c.curve_to(q * 92, 160, q * 80, 160, q * 30, 160); c.line_to(q * 34, -10); c.line_to(q * 70, -24); c.close_path(); fs(c, DENIM, 7)
        ell(c, q * 60, 50, 10, 10); c.set_source_rgb(*YEL); c.fill()
    c.restore()
    return (x - 82 * s, y + 20 * s), (x + 82 * s, y + 20 * s)

def drumkit(c, x, gy, s):
    c.save(); c.translate(x, gy); c.scale(s, s)
    ell(c, 0, -150, 150, 150); fs(c, hx('d23a4a')); ell(c, 0, -150, 110, 110); fs(c, hx('f5efe2'), 6)
    txt(c, 'THE LOUD', 0, -150, 44, fill=hx('d23a4a'), lw=6)
    for q, w in ((-1, 90), (1, 80)):
        ell(c, q * 200, -300, w, 26); fs(c, hx('d23a4a'), 7)
    c.move_to(260, -420); c.line_to(260, -20); c.set_source_rgb(*GREY); c.set_line_width(10); c.stroke()
    ell(c, 260, -430, 120, 18); fs(c, YEL, 6)
    c.restore()

def stick(c, hx_, hy, ang, s):
    c.save(); c.translate(hx_, hy); c.rotate(ang)
    c.move_to(0, 0); c.line_to(150 * s, 0); c.set_source_rgb(*INK); c.set_line_width(14 * s); c.stroke()
    c.move_to(0, 0); c.line_to(150 * s, 0); c.set_source_rgb(*hx('e8c99a')); c.set_line_width(8 * s); c.stroke(); c.restore()

# ---------------- props ----------------
def lightning(c, x, y, s, rot=0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.move_to(8, -46); c.line_to(-22, 4); c.line_to(0, 4); c.line_to(-10, 46); c.line_to(24, -10); c.line_to(2, -10); c.line_to(16, -46); c.close_path()
    fs(c, YEL, 5); c.restore()

def guitar(c, x, y, s, rot=0, dust=0):
    """Body centre at (x, y); neck points to the viewer's right at rot=0."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    rr(c, 90, -18, 300, 36, 10); fs(c, hx('8a5a34'), 7)                     # neck
    rr(c, 380, -30, 80, 60, 16); fs(c, hx('3a2a20'), 7)                      # headstock
    for i in range(3):
        for q in (-1, 1): ell(c, 400 + i * 22, q * 36, 7, 7); fs(c, GREY, 3)
    c.new_sub_path(); ell(c, -70, 0, 110, 100); ell(c, 40, 0, 82, 76)
    c.set_source_rgb(*INK); c.set_line_width(16); c.stroke_preserve(); c.set_source_rgb(*GUITAR); c.fill()
    ell(c, -30, 30, 60, 34); c.set_source_rgb(*WHITE); c.fill()             # pickguard
    rr(c, -110, -26, 26, 52, 6); fs(c, INK, 0)                               # bridge
    for i in range(4):
        c.move_to(-100, -12 + i * 8); c.line_to(400, -12 + i * 8); c.set_source_rgba(.92, .92, .95, .9); c.set_line_width(2.5); c.stroke()
    lightning(c, -60, -40, 1.0, -.2)
    if dust: ell(c, -20, -20, 150, 110); c.set_source_rgba(.85, .82, .76, .35 * dust); c.fill()
    c.restore()

def cassette(c, x, y, s, rot=0, label="GARAGE DEMO '86", dust=0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    rr(c, -110, -70, 220, 140, 14); fs(c, hx('2d2d3a'))
    rr(c, -92, -58, 184, 64, 8); fs(c, hx('fff6dc'), 5)
    txt(c, label, 0, -28, 21, fill=RED, lw=0)
    for q in (-1, 1): ell(c, q * 46, 30, 20, 20); fs(c, WHITE, 5)
    if dust: rr(c, -110, -70, 220, 140, 14); c.set_source_rgba(.85, .82, .76, .4 * dust); c.fill()
    c.restore()

# ---------------- the cat ----------------
def cat(c, x, gy, s, pose='walk', phase=0, old=False, f=0, look=-1, paw_down=None):
    """Orange tabby facing the viewer's left (look=-1). pose: walk (phase in steps), sit, sleep.
    paw_down: index 0-3 of the paw pressing down this frame (for timed paw contacts). Returns paw points."""
    c.save(); c.translate(x, gy); c.scale(s * look, s)   # drawn facing +x; look=-1 mirrors it to face left
    body_h = 46 if old else 40; tail_w = math.sin(f * .2) * 12
    paws = []
    if pose == 'sleep':
        ell(c, 0, -40, 120, 52); fs(c, TABBY)
        for i in range(3): c.arc(-30 + i * 34, -60, 26, math.pi * 1.15, math.pi * 1.85); c.set_source_rgb(*TABBY_D); c.set_line_width(8); c.stroke()
        c.move_to(-110, -30); c.curve_to(-140, 10, 40, 20, 100, -4); c.set_source_rgb(*INK); c.set_line_width(26); c.stroke()
        c.move_to(-110, -30); c.curve_to(-140, 10, 40, 20, 100, -4); c.set_source_rgb(*TABBY); c.set_line_width(16); c.stroke()
        hx_, hy = 92, -52
        _cat_head(c, hx_, hy, .95, old, 'sleep', f)
        c.restore(); return paws
    # legs
    lift = [0, 0, 0, 0]
    if pose == 'walk':
        for i in range(4):
            lift[i] = max(0, math.sin(phase * math.pi + i * math.pi / 2)) * 26
        if paw_down is not None: lift[paw_down] = 0
    legx = [-70, -40, 50, 80]
    for i, lx in enumerate(legx):
        top = (lx, -50); foot = (lx + (8 if lift[i] else 0), -lift[i])
        limb(c, [top, foot], 20, TABBY)
        ell(c, foot[0], foot[1], 16, 10); fs(c, CREAM if old else TABBY, 5)
        paws.append(foot)
    # tail up and curling
    c.move_to(-100, -70); c.curve_to(-150, -110, -150 + tail_w, -180, -120 + tail_w, -200)
    c.set_source_rgb(*INK); c.set_line_width(28); c.stroke_preserve(); c.set_source_rgb(*TABBY); c.set_line_width(16); c.stroke()
    ell(c, 0, -76, 108, body_h); fs(c, TABBY)
    for i in range(4):
        c.arc(-60 + i * 36, -100, 24, math.pi * 1.2, math.pi * 1.8); c.set_source_rgb(*TABBY_D); c.set_line_width(8); c.stroke()
    _cat_head(c, 104, -110, 1.0, old, 'open', f)
    c.restore()
    return [(x + look * px * s, gy + py * s) for px, py in paws]

def _cat_head(c, x, y, s, old, eyes, f):
    c.save(); c.translate(x, y); c.scale(s, s)
    for q in (-1, 1):
        c.move_to(q * 22 - 26, -30); c.line_to(q * 34, -78); c.line_to(q * 46 + 16, -24); c.close_path(); fs(c, TABBY, 7)
    ell(c, 0, 0, 62, 54); fs(c, TABBY)
    c.move_to(-14, -50); c.line_to(-8, -30); c.move_to(0, -54); c.line_to(0, -32); c.move_to(14, -50); c.line_to(8, -30)
    c.set_source_rgb(*TABBY_D); c.set_line_width(7); c.stroke()
    ell(c, 14, 22, 36, 24); c.set_source_rgb(*(hx('d8d4cc') if old else CREAM)); c.fill()      # muzzle (grey when old)
    if eyes == 'sleep' or blinking(f, 9):
        for q in (-1, 1): c.arc(q * 24 + 4, -2, 11, .2, math.pi - .2); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    else:
        for q in (-1, 1):
            ell(c, q * 24 + 6, -4, 11, 14); fs(c, hx('b8e04a'), 4); ell(c, q * 24 + 8, -4, 4, 10); c.set_source_rgb(*INK); c.fill()
    c.move_to(26, 12); c.line_to(38, 12); c.line_to(32, 20); c.close_path(); c.set_source_rgb(*hx('ff8fa6')); c.fill()
    for q in (-1, 1):
        c.move_to(40, 22 + q * 4); c.line_to(86, 16 + q * 14); c.set_source_rgb(*INK); c.set_line_width(3); c.stroke()
    if old:
        ell(c, 0, -34, 30, 10); c.set_source_rgba(.85, .85, .85, .5); c.fill()
    c.restore()

# ---------------- robot (series design) ----------------
def visor(c, emote, eye, blink, f):
    rr(c, -82, -54, 164, 92, 40); fs(c, hx('0b1020'), 6); c.set_source_rgb(*BLUE)
    if emote == 'happy':
        for q in (-1, 1): c.arc(q * 36, 4, 18, math.pi + .2, 2 * math.pi - .2); c.set_line_width(10); c.stroke()
    elif emote == 'proud':        # small closed arcs, eyes slightly up: restrained pride
        for q in (-1, 1): c.arc(q * 36, -2, 14, math.pi + .3, 2 * math.pi - .3); c.set_line_width(9); c.stroke()
        c.move_to(-14, 22); c.curve_to(-4, 28, 4, 28, 14, 22); c.set_line_width(6); c.stroke()
    elif emote == 'sideeye':      # half-lidded, looking to the viewer
        for q in (-1, 1):
            ell(c, q * 36 + 12, 0, 16, 14); c.fill()
            c.move_to(q * 36 - 18, -12); c.line_to(q * 36 + 22, -12); c.set_line_width(8); c.stroke()
    elif emote == 'nope':
        for q in (-1, 1): c.move_to(q * 36 - 16, -8); c.line_to(q * 36 + 16, -8); c.set_line_width(10); c.stroke()
    elif blink:
        for q in (-1, 1): c.move_to(q * 36 - 16, -4); c.line_to(q * 36 + 16, -4); c.set_line_width(8); c.stroke()
    else:
        for q in (-1, 1): ell(c, q * 36 + eye[0], -8 + eye[1], 18, 24); c.fill()
def robot(c, x, y, s, emote=None, eye=(0, 0), f=0, seed=0, arms=None):
    """Series robot, head centre at (x, y). arms: list of point lists (canvas coords) drawn white behind the body."""
    if arms:
        for pts in arms: limb(c, pts, 34 * s, WHITE)
    c.save(); c.translate(x, y); c.scale(s, s); c.set_line_cap(cairo.LINE_CAP_ROUND)
    br = 1 + .015 * math.sin(f * .16 + seed)
    c.save(); c.translate(0, 85); c.scale(1, br); rr(c, -72, 0, 144, 135, 44); fs(c, WHITE); ell(c, 0, 65, 30, 30); fs(c, (.82, .86, .93), 5); c.restore()
    wob = math.sin(f * .45 + seed) * 9
    c.move_to(0, -90); c.curve_to(0, -110, wob * .5, -122, wob, -132); c.set_source_rgb(*INK); c.set_line_width(9); c.stroke()
    ell(c, wob, -140, 17, 17); fs(c, BLUE, 7)
    for q in (-1, 1): ell(c, q * 110, 0, 22, 38); fs(c, GREY, 8)
    rr(c, -108, -95, 216, 180, 78); fs(c, WHITE)
    visor(c, emote, eye, emote is None and blinking(f, seed + 3), f)
    c.restore()
    return (x - 70 * s, y + 110 * s), (x + 70 * s, y + 110 * s)   # shoulder points

# ---------------- title bar ----------------
BAR_Y, BAR_H = 222, 138
def topbar(c, year, k_flip=0):
    """HOODYZ placeholder bar in screen space. k_flip 0..1 spins the year pill during a fast-forward."""
    c.save(); c.identity_matrix()
    rr(c, 40, BAR_Y, 1000, BAR_H, 40); fs(c, WHITE, 8)
    txt(c, 'HOODYZ', 90, BAR_Y + BAR_H / 2, 74, fill=NAVY, lw=0, align='l')
    px, py = 860, BAR_Y + BAR_H / 2
    rr(c, px - 110, py - 44, 220, 88, 44); fs(c, YEL, 7)
    sq = abs(math.cos(k_flip * math.pi)) if k_flip else 1
    c.save(); c.translate(px, py); c.scale(1, max(.05, sq)); txt(c, str(year), 0, 0, 58, fill=INK, lw=0); c.restore()
    c.restore()
