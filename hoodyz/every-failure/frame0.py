"""Every Failure - frame 0 v2 (the hook and the loop target), a still for approval (process step 3).
v2 after the still audit: a deep, wide chasm with walls; the ground line raised so faces sit under the title bar; the pyramids pushed
back and hazed; contact shadows; Hoody braced under the rock (open palms under it, two-bone arms, knee bent, trailing foot slipping
to the edge, sweat); MY AI looks at the rock; Eva urges him on (arm out to him, no clapping yet); SUCCESS unlit but gold, a prize.
Set: Perfect Trip's Giza desert. Writes frame0.png (v1: frame0_v1.py)."""
import os, sys, math, cairo
HERE = os.path.dirname(os.path.abspath(__file__)); PT = os.path.join(HERE, '..', 'perfect-trip')
sys.path.insert(0, PT)
import places as P                                   # Giza desert (adds perfect-date to the path)
from photo import R, K, Sh, E, A                     # Perfect Date's Hoody, MY AI, Eva, series bar
from kit import INK, WHITE, NAVY, rr, fs, ell, hx, txt, limb
W, H = 1080, 1920
GL = 1300                                             # ground line: faces just under the title bar
CX0, CX1 = 380, 760                                   # the chasm's lips (v1: 420-690)
RED, YEL, GOLD = hx('d63a32'), hx('ffd23f'), hx('d9a520')
SAND, SAND_D = hx('f2d394'), hx('e2b874')

def shadow(c, x, w, y=GL):
    ell(c, x, y + 6, w, 14); c.set_source_rgba(0, 0, 0, .18); c.fill()

def backdrop(c, f):
    P.egypt(c, f, s=.55, cx0=880, horizon=GL - 150)                       # pyramids far off, right of centre, behind the far bank
    c.rectangle(0, GL - 150, W, 150); c.set_source_rgb(*hx('f4dca6')); c.fill()  # far desert floor, flat (no dune strokes behind the cast)
    c.rectangle(0, 0, W, GL); c.set_source_rgba(*hx('fff3d6'), .38); c.fill()  # haze: far things lighter, lower contrast
    c.rectangle(0, GL, W, H - GL); c.set_source_rgb(*SAND); c.fill()           # the ground slab, a cliff top on both sides
    c.move_to(0, GL); c.line_to(W, GL); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    # v4: no dune ovals in the foreground - they read as stray shadows (key-pose audit 2)

def chasm(c):
    lip_l = [(CX0, GL), (CX0 + 10, GL + 60), (CX0 - 6, GL + 150), (CX0 + 14, GL + 300), (CX0 + 4, H + 10)]
    lip_r = [(CX1, GL), (CX1 - 12, GL + 80), (CX1 + 6, GL + 190), (CX1 - 10, GL + 330), (CX1, H + 10)]
    c.move_to(*lip_l[0]); [c.line_to(*p) for p in lip_l[1:]]; [c.line_to(*p) for p in reversed(lip_r)]; c.close_path()
    g = cairo.LinearGradient(0, GL, 0, H); g.add_color_stop_rgb(0, *hx('4a3020')); g.add_color_stop_rgb(.45, *hx('22160f')); g.add_color_stop_rgb(1, *hx('0d0907'))
    c.set_source(g); c.fill()
    for lip, q in ((lip_l, 1), (lip_r, -1)):                                     # the two rock walls: a lit face, then the shadowed depth
        c.move_to(*lip[0]); [c.line_to(*p) for p in lip[1:]]
        for p in reversed(lip): c.line_to(p[0] + q * 46, p[1] + 30)
        c.close_path(); c.set_source_rgb(*(hx('b98a52') if q > 0 else hx('8f6338'))); c.fill()
        for k in range(1, 5):                                                    # strata
            y = GL + k * 110; c.move_to(lip[0][0] + q * 6, y); c.line_to(lip[0][0] + q * 40, y + 18); c.set_source_rgb(*hx('7a5530')); c.set_line_width(5); c.stroke()
        c.move_to(lip[0][0], lip[0][1]); c.line_to(lip[0][0] + q * 46, lip[0][1] + 30); c.line_to(lip[1][0] + q * 46, lip[1][1] + 30); c.line_to(*lip[1]); c.close_path()
        c.set_source_rgb(*hx('d8ad72')); c.fill()                                    # lit upper edge
        for k, (dy, w_) in enumerate(((210, 36), (430, 28), (620, 40))):            # loose fragments on the wall
            y = GL + dy + (q > 0) * 60; xx = lip[0][0] + q * (52 + k * 6)
            c.move_to(xx, y); c.line_to(xx + q * w_, y + 10); c.line_to(xx + q * (w_ - 8), y + 30); c.line_to(xx, y + 24); c.close_path(); fs(c, hx('6e4a2a'), 4)
        c.move_to(*lip[0]); [c.line_to(*p) for p in lip[1:]]; c.set_source_rgb(*INK); c.set_line_width(7); c.stroke()
    g = cairo.LinearGradient(CX0 + 40, 0, CX1 - 40, 0); g.add_color_stop_rgba(0, 0, 0, 0, .45); g.add_color_stop_rgba(.3, 0, 0, 0, 0); g.add_color_stop_rgba(.7, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, .45)
    c.rectangle(CX0 + 40, GL + 30, CX1 - CX0 - 80, H); c.set_source(g); c.fill()   # inner wall shadows

def rock(c, x, y, s, word, rot=0, ty=0):
    """A grey boulder with one red word on it, centred at x, y."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    pts = [(-150, 20), (-120, -70), (-40, -110), (70, -100), (150, -40), (160, 50), (90, 105), (-60, 110), (-140, 80)]
    c.move_to(*pts[0]); [c.line_to(*p) for p in pts[1:]]; c.close_path(); fs(c, hx('9a9a96'), 7)
    c.move_to(-110, 60); c.line_to(-40, 95); c.line_to(80, 88); c.set_source_rgb(*hx('7b7b77')); c.set_line_width(10); c.stroke()
    size = 92
    if word:                                                                     # fit the word to the stone (REJECTED is long), measured
        c.select_font_face('Lilita One'); c.set_font_size(92); wd = c.text_extents(word).width
        size = min(92, 92 * 250 / max(1, wd))
    txt(c, word, 0, ty, size, RED, lw=0)
    c.restore()

def success_sign(c, x, y, lit=0.0, word=True):
    """A marquee sign: gold frame and bulbs. Unlit = a prize waiting (gold, dim bulbs); lit = bulbs and plate glow."""
    w, h = 300, 104
    for q in (-1, 1): c.rectangle(x + q * 70 - 7, y + h / 2, 14, GL - y - h / 2); c.set_source_rgb(*INK); c.fill()
    plate = tuple((1 - lit) * a + lit * b for a, b in zip(hx('f6e7bd'), hx('fff3a8')))
    if lit > 0: pass
    rr(c, x - w / 2 - 14, y - h / 2 - 14, w + 28, h + 28, 34); fs(c, GOLD, 7)
    rr(c, x - w / 2, y - h / 2, w, h, 24); fs(c, plate, 5)
    if lit > 0:                                                                  # lit: a glow around the frame
        rr(c, x - w / 2 - 30, y - h / 2 - 30, w + 60, h + 60, 46); c.set_source_rgba(*YEL, .45 * lit); c.fill()
    if word: txt(c, 'SUCCESS', x, y + 2, 60, hx('b07d12') if lit < .5 else INK, lw=0)

def ik2(s, t, a, b, bend):
    """Two bones of fixed length a, b from s towards t; bend = +1/-1 picks the elbow side. Out of reach: straight, short of t."""
    dx, dy = t[0] - s[0], t[1] - s[1]; d = min(math.hypot(dx, dy), a + b - 1e-3)
    ang = math.atan2(dy, dx); cos_a = max(-1, min(1, (a * a + d * d - b * b) / (2 * a * d)))
    e = (s[0] + a * math.cos(ang + bend * math.acos(cos_a)), s[1] + a * math.sin(ang + bend * math.acos(cos_a)))
    return e, (s[0] + d * math.cos(ang), s[1] + d * math.sin(ang))

def braced_hoody(c, x, s, f, rock_c, rock_s, teeter):
    """Hoody under the rock: the series rig with its 'up' arms swapped for two-bone arms ending in open palms under the rock."""
    hands = []
    orig = K.arm
    def arm(cc, pts, ss, col=NAVY, flick=None):
        sh = pts[0]; q = 1 if sh[0] > x else -1
        tgt = (rock_c[0] + q * 118 * rock_s, rock_c[1] + 92 * rock_s)          # the rock's lower corners
        e, h = ik2(sh, tgt, 118 * ss, 140 * ss, q)                             # elbows out
        limb(cc, [sh, e, h], 44 * ss, col)
        cf = lambda t: (e[0] + (h[0] - e[0]) * t, e[1] + (h[1] - e[1]) * t)
        limb(cc, [cf(.74), cf(.9)], 52 * ss, hx('15203a'))                          # the cuff: sleeve into wrist
        cc.save(); cc.translate(*h); cc.scale(q, 1)                                  # one palm, mirrored per side: thumbs alike
        K.palm(cc, 0, 0, ss * 1.25, -math.pi / 2 - .5, 0); cc.restore()
        hands.append(h)
    K.arm = arm
    try: R.hoody(c, x, GL, s, expr='shock', arms=('up', 'up'), legs='drag2', f=f)
    finally: K.arm = orig
    return hands

def sweat(c, x, y, s):
    for dx, dy, k in ((0, 0, 1), (34, 40, .7)):
        c.move_to(x + dx, y + dy - 22 * k * s); c.curve_to(x + dx + 14 * k * s, y + dy, x + dx + 10 * k * s, y + dy + 14 * k * s, x + dx, y + dy + 14 * k * s)
        c.curve_to(x + dx - 10 * k * s, y + dy + 14 * k * s, x + dx - 14 * k * s, y + dy, x + dx, y + dy - 22 * k * s); fs(c, hx('9fdcff'), 4)

BAR = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, 420)
BARK = (956 - 64) / (1044 - 36)                       # the series bar scaled into the safe zone (as Perfect Trip v3)
def topbar(c, label):
    cc = cairo.Context(BAR); cc.set_operator(cairo.OPERATOR_CLEAR); cc.paint(); cc.set_operator(cairo.OPERATOR_OVER)
    Sh.topbar(cc, label)
    c.save(); c.translate(64, 222); c.scale(BARK, BARK); c.translate(-36, -222); c.set_source_surface(BAR, 0, 0); c.paint(); c.restore()

def draw(f=0, teeter=.09):
    S = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(S)
    backdrop(c, f); chasm(c)
    rock(c, 60, GL - 34, .4, ''); rock(c, 118, GL - 26, .3, '')                    # the pile of new failures, his side (left edge)
    hs, hx_ = .85, 315
    ex = 890
    success_sign(c, 845, 470, 0)                                                     # poles at 775 and 915: both on the right bank (lip 760)
    shadow(c, ex, 70); E.eva(c, ex, GL, .85, 'evacalm', pose='holdlow', hand_to=(ex - 230 * .85, GL - 600 * .85), leash=False)   # she urges him on: arm out to him across the gap
    shadow(c, 122, 70); A.myai(c, 122, GL, .85 * 1.1, eye='open', look=(14, -12), arms=('down', 'down'))
    shadow(c, hx_ + 10, 95)
    c.save(); c.translate(hx_, GL); c.rotate(teeter); c.translate(-hx_, -GL)        # the weight tips him towards the gap, about his feet
    rs = 1.25 * hs; rc = (hx_ + 10, GL - 300 * hs - 326 * hs - 200 * hs)   # bottom edge at the palms' full reach (two fixed bones): no floating rock           # rock centre above his head (rig: waist, head, reach)
    rock(c, rc[0], rc[1], rs, 'FAIL', rot=-.06, ty=-34)                             # the rock first, his palms over it
    hands = braced_hoody(c, hx_, hs, f, rc, rs, teeter)
    ell(c, rc[0], rc[1] + 92 * rs + 6, 120 * rs, 20 * rs); c.set_source_rgba(0, 0, 0, .16); c.fill()   # the rock's shadow on his hair
    sweat(c, hx_ + 150 * hs, GL - 300 * hs - 326 * hs - 20 * hs, hs)
    c.restore()
    topbar(c, 'HIS SUCCESS')
    return S, hands, rc

if __name__ == '__main__':
    S, hands, rc = draw(); S.write_to_png(os.path.join(HERE, 'frame0.png'))
    print('palms', [tuple(round(v) for v in h) for h in hands], 'rock centre', tuple(round(v) for v in rc))
