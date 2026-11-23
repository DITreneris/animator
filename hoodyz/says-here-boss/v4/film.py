"""Hoodyz - Says Here You Were Our Boss, v4 (21 Nov): an animated loop and a hook in the first second.
v3 (imported, untouched) ended on a held smile that matched frame 0: a still loop. v4:
- THE LOOP IS THE JOKE: after "About your experience..." HARV's antenna blinks, a NEW CHAT chip pops, and he picks the same CV
  up again. The cut lands mid-lift on frame 0, where he reads it: "Says here you used to be our boss?" He has no memory of the
  interview either. The CV's rise, the chip and the panel's breathing all run through the seam.
- THE HOOK: frame 0 is HARV in Hoody's gold shades with the CV coming up; the line starts on frame 3 (v3: a silent smile for 0.67 s).
- The desk shots are reframed close: HARV fills the frame, the desk is a strip, the nameplate sits above the app's bottom zone.
- Speech tails touch the speaker (HARV's antenna; Hoody's cheek, round his hair). "About your experience..." is now on HARV.
- Every shot moves (breathing, blinks, push-ins, typing); the one deliberate hold is the silence after the shout.
Usage: python3 film.py frames F ... | keys | video | final"""
import sys, os, math, subprocess, cairo
HERE = os.path.dirname(os.path.abspath(__file__)); V3 = os.path.join(HERE, '..', 'v3'); sys.path.insert(0, V3)
import render as V, chars as Sh, kit as K
from kit import INK, WHITE, NAVY, SKIN, BLUE, YEL, RED, GREY, rr, fs, ell, limb, txt, shades, hx, lerp, cl, ss
W, H, FPS = 1080, 1920, 30
back, oe, bg, rays = V.back, V.oe, V.bg, V.rays

SHOTS = [('a1', 60, '2027'), ('a2', 28, '2027'), ('a3', 14, '2027'), ('a4', 22, '2027'), ('a5', 14, 'REWIND'),
         ('a6', 34, '2024'), ('a7', 34, '2025'), ('a8', 28, '2026'), ('a9', 24, '2026'), ('a10', 16, '2026'),
         ('a11', 48, '2027'), ('a12', 40, '2027'), ('a13', 31, '2027'), ('a14', 56, '2027'), ('a15', 30, '2027'),
         ('a16', 16, '2027'), ('a17', 18, '2027'), ('a18', 48, '2027'), ('a19', 12, '2027'), ('a20', 24, '2027')]
START = {}; _t = 0
for _n, _d, _p in SHOTS: START[_n] = _t; _t += _d
NF = _t
LOOPF = 2 * math.pi * 45 / .45 / NF          # scales f so K.robot's breathing (.16) and antenna wobble (.45) are periodic over the loop
VO = [('h1', 'a1', 3), ('g1', 'a2', 8), ('g2', 'a13', 1), ('h2', 'a14', 2), ('g3', 'a15', 1), ('h3', 'a18', 2)]

# ---------------- speech ----------------
def bubble_at(c, lines, r, tip, cx, cy, size=66, out=None):
    """v3's bubble with the tail's tip exactly on `tip` (the speaker)."""
    V.bubble(c, lines, r, tip, cy=cy, size=size, out=out, cx=cx)

def hoody_bubble(c, lines, r, head, size=66, side=1, cy=470):
    """Hoody's bubble: the tail comes down outside his hair and bends in to his cheek beside the mouth."""
    k = back(r / 5)
    if k <= .03: return
    hx_, hy_, s = head
    tip = (hx_ + side * 92 * s, hy_ + 76 * s); turn = (hx_ + side * 196 * s, hy_ + 74 * s); o = (hx_ + side * 204 * s, hy_ - 70 * s)
    c.save(); c.select_font_face('Lilita One'); c.set_font_size(size)
    w = max(c.text_extents(l).width for l in lines) + 90; h = len(lines) * size * 1.12 + 56
    bx = min(max(o[0] - side * (w / 2 - 80), w / 2 + 30), W - w / 2 - 30)
    kk = max(k, .02); b0, b1 = (bx + side * 60 - 34 * kk, cy + (h / 2 - 8) * kk), (bx + side * 60 + 34 * kk, cy + (h / 2 - 8) * kk)
    c.move_to(*b0); c.curve_to(o[0] - side * 26, o[1], turn[0] - side * 10, turn[1] + 34, tip[0], tip[1] + 12)
    c.line_to(tip[0], tip[1] - 14)
    c.curve_to(turn[0] + side * 26, turn[1] - 34, o[0] + side * 30, o[1], *b1); c.close_path(); fs(c, WHITE, 8)
    c.translate(bx, cy); c.scale(k, k); c.translate(-bx, -cy)
    rr(c, bx - w / 2, cy - h / 2, w, h, 40); fs(c, WHITE, 8)
    c.move_to(bx + side * 60 - 30, cy + h / 2 - 12); c.line_to(bx + side * 60 + 30, cy + h / 2 - 12); c.set_source_rgb(*WHITE); c.set_line_width(14); c.stroke()
    for i, l in enumerate(lines): txt(c, l, bx, cy - h / 2 + 28 + size * .56 + i * size * 1.12, size, NAVY, lw=0)
    c.restore()

# ---------------- set-ups ----------------
HS = V.HS; HEAD = (540, 1020, HS)
def push(c, r, d, k=.04, cx=540, cy=1050):
    z = 1 + k * r / max(1, d); c.translate(cx, cy); c.scale(z, z); c.translate(-cx, -cy)

def hoody_close(c, f, expr, sweat_t=None, gaze=0, blink=None):
    """v3's close-up, breathing and blinking."""
    bg(c, '1a3a5c', '0d2236'); rays(c, WHITE, f, a=.05)
    br = 1 + .012 * math.sin(f * .2)
    c.save(); c.translate(540, 1700); c.scale(1, br); c.translate(-540, -1700)
    K.hoodie(c, 540, 1020 + 150 * HS, HS * 1.1); c.restore()
    hy = 1020 - 8 * math.sin(f * .2)
    bl = K.blinking(f, 3) if blink is None else blink
    K.hoodyz_head(c, 540, hy, HS, era='young', expr=expr, blink=bl, gaze=gaze)
    if sweat_t is not None: Sh.sweat(c, 540 + 112 * HS, hy + (-44 + 70 * sweat_t) * HS, HS * .9)
    return (540, hy, HS)

HX, HY, HSC = 540, 940, 1.95          # HARV at the desk, close
DESK = 1300
def harv_tip(bob=0): return (HX, HY + bob - 157 * HSC)

def chip(c, x, y, k):
    """The NEW CHAT chip by HARV's antenna."""
    if k <= .02: return
    c.save(); c.translate(x, y); c.scale(k, k)
    rr(c, -215, -56, 430, 112, 56); fs(c, hx('0f1830'), 8)
    c.set_source_rgb(*BLUE); c.set_line_width(12); c.move_to(-172, 0); c.line_to(-132, 0); c.move_to(-152, -20); c.line_to(-152, 20); c.stroke()
    txt(c, 'NEW CHAT', 34, 3, 62, WHITE, lw=0); c.restore()

def desk(c, f, bob=0, mouth='flat', arm=None, cv=0.0, cv_hand=True, cat_eye=False, panel_look=0.0, pulse=0.0, glint=None):
    """The interview room, close: HARV fills the frame; the panel behind him; the desk a strip; the nameplate above y 1700.
    cv: 0 flat on the desk .. 1 held up to read. pulse: the antenna's reset flash."""
    fl = f * LOOPF
    bg(c, '10354f', '0d2236')
    for i in range(6): c.rectangle(60 + i * 192, 560, 8, 760); c.set_source_rgba(1, 1, 1, .05); c.fill()
    for x, q, seed in ((165, 1, 0), (915, -1, 2)):
        c.save(); c.translate(x, 1120); c.rotate(.26 * q * panel_look); c.translate(-x, -1120)
        K.robot(c, x + 20 * q * panel_look, 1030, 1.02, eye=(20 * q * panel_look, -4 * panel_look), f=fl, seed=seed); c.restore()
    y = HY + bob
    if pulse > 0:
        tx, ty = HX, y - 140 * HSC
        for i in range(2):
            p = (pulse + i * .5) % 1; ell(c, tx, ty, 34 + 110 * p, 34 + 110 * p); c.set_source_rgba(.35, .8, 1, .7 * (1 - p)); c.set_line_width(9); c.stroke()
    Sh.harv(c, HX, y, HSC, mouth=mouth, arm=None)
    if arm == 'adjust':
        sh_r = (HX + 70 * HSC, y + 110 * HSC); hand = (HX + 100 * HSC, y - 14 * HSC)
        limb(c, [sh_r, (HX + 124 * HSC, y + 74 * HSC), hand], 34 * HSC * .62, WHITE); ell(c, *hand, 44, 44); fs(c, WHITE, 8)
    if glint is not None:                                                    # a glint sweeps the lenses
        c.save(); c.translate(HX, y); c.scale(HSC, HSC); c.translate(0, -12); c.scale(1.02, 1.02)
        rr(c, -92, -28, 84, 58, 22); rr(c, 8, -28, 84, 58, 22); c.clip()
        gx = lerp(-200, 200, glint); c.move_to(gx - 30, -40); c.line_to(gx + 10, -40); c.line_to(gx - 20, 40); c.line_to(gx - 60, 40); c.close_path()
        c.set_source_rgba(1, 1, 1, .55); c.fill(); c.restore()
    rr(c, -40, DESK, 1160, 64, 18); fs(c, hx('a9713f'))
    c.rectangle(-10, DESK + 60, 1100, 700); c.set_source_rgb(*hx('7c4f2a')); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(8); c.stroke()
    Sh.nameplate(c, 540, DESK + 215, .95)
    cb = 1 + .02 * math.sin(fl * .16 + 1)
    c.save(); c.translate(905, DESK + 2); c.scale(1, cb); c.translate(-905, -(DESK + 2)); Sh.cat_one_eye(c, 905, DESK + 2, .72, open_eye=cat_eye); c.restore()
    k = ss(cv)
    px, py, rot = lerp(360, 395, k), lerp(DESK - 22, DESK - 112, k), lerp(-.1, -.14, k)
    sh_l = (HX - 70 * HSC, y + 110 * HSC)
    if cv_hand: limb(c, [sh_l, (lerp(330, 320, k), lerp(DESK - 50, DESK - 40, k)), (px - 10, py + 70)], 34 * HSC * .6, WHITE)
    c.save(); c.translate(px, py); c.rotate(rot); c.scale(1, lerp(.45, 1, k))                         # flat on the desk -> upright
    rr(c, -82, -108, 164, 216, 12); fs(c, WHITE, 7); txt(c, 'CV', 0, -52, 66, INK, lw=0)
    for i in range(3): c.rectangle(-54, 0 + i * 30, 108 - (i % 2) * 34, 11); c.set_source_rgb(*hx('b9c0cc')); c.fill()
    c.restore()
    if cv_hand: ell(c, px - 10, py + 74, 30, 30); fs(c, WHITE, 7)

CHIP = (800, 520)
# ---------------- the 20 shots ----------------
def a1(c, f, r, d):   # FRAME 0: the CV is already rising; the line from frame 3. The chip from the last shot fades in the first frames
    c.save(); push(c, r, d, .03, cy=1000)
    bob = -10 * math.sin(math.pi * cl((r - 8) / 14)) + 5 * math.sin(r * .22)
    desk(c, f, bob=bob, cv=cl(.5 + (r + 1) * .05))
    chip(c, *CHIP, 1 - cl((r - 1) / 4))        # gone before the bubble reaches it
    c.restore()
    c.save(); push(c, r, d, .03, cy=1000); tip = c.user_to_device(*harv_tip(bob)); c.restore()
    bubble_at(c, ['SAYS HERE YOU USED', 'TO BE OUR BOSS?'], r - 3, tip, 430, 470)

def a2(c, f, r, d):   # his reaction: the forced smile, the sweat, the crack: "...yes."
    hoody_close(c, f, 'forced' if r < 8 else 'cracked', sweat_t=cl(r / 20) * .6 if r < 8 else None, blink=False)

def a3(c, f, r, d):   # his eyes flick to the shades
    bg(c, '1a3a5c', '0d2236')
    c.save(); push(c, r, d, .05, cy=1000)
    K.hoodyz_head(c, 540, 1000 - 8 * 5.6, 5.6, era='young', expr='calm', blink=False, gaze=26 * oe((r - 3) / 4)); c.restore()

def a4(c, f, r, d):   # the shades, a glint and a sparkle
    c.save(); push(c, r, d, .07, cy=1000); V.s5(c, f, r); c.restore()

def a5(c, f, r, d): V.s7(c, f, r)

def trip(c, f, r, d, expr, cap, extra=None):
    cap0 = V.caption; V.caption = lambda *a, **k: None
    try:
        c.save(); push(c, r, d, .05, cy=1000); c.translate(0, 5 * math.sin(f * 1.3)); V.triptych(c, f, r, expr, cap, extra=extra); c.restore()
    finally: V.caption = cap0
    V.caption(c, cap, r)
def a6(c, f, r, d): trip(c, f, r, d, 'confident', 'PROMPT ENGINEER')
def a7(c, f, r, d):
    trip(c, f, r, d, 'sheepish', 'PROMPT MANAGER', extra=V.agents)
    for q, ph in ((1, 0), (-1, .5)): Sh.sweat(c, 540 + q * 118 * 1.6, 860 + (-40 + 90 * ((r / 18 + ph) % 1)) * 1.6, 1.2)
def a8(c, f, r, d): trip(c, f, r, d, 'happy', 'MENTOR', extra=V.mentee)
def a9(c, f, r, d): V.s11(c, f, r)
def a10(c, f, r, d): V.s12(c, f, r)

def darkroom(c, f, t, bob):
    """The dark room, recomposed: v3's TV (drawn by its own code, smaller, up top) and a big Hoody on the sofa under it,
    the JOBS laptop on his knees, the cat asleep beside him. Everything that matters sits above y 1700."""
    c.set_source_rgb(*hx('070b18')); c.paint()
    tb = Sh.topbar; Sh.topbar = lambda *a, **k: None
    try:
        c.save(); c.rectangle(0, 0, W, 975); c.clip()
        c.translate(540, 420); c.scale(.8, .8); c.translate(-540, -420); Sh.darkroom_draw(c, t=t, bob=bob); c.restore()
    finally: Sh.topbar = tb
    g = cairo.RadialGradient(540, 700, 60, 540, 900, 1100); g.add_color_stop_rgba(0, .36, .48, .9, .25); g.add_color_stop_rgba(1, .36, .48, .9, 0)
    c.rectangle(0, 975, W, H - 975); c.set_source(g); c.fill()
    rr(c, 30, 1090, 1020, 420, 80); fs(c, hx('1d3557'), 10)                       # sofa back
    rr(c, 30, 1440, 1020, 420, 70); fs(c, hx('274472'), 10)                       # seat
    cb = 1 + .02 * math.sin(f * .16)
    c.save(); c.translate(850, 1450); c.scale(1, cb); c.translate(-850, -1450); K.cat(c, 850, 1450, 1.15, pose='sleep', look=-1); c.restore()
    hx0, hy0, hs = 400, 1200 - 3 * math.sin(f * .2), 1.5
    Sh.hoody(c, hx0, hy0, hs, 'tvstare', gold=False)
    rr(c, 215, 1440, 370, 210, 16); fs(c, hx('2b2f3a'), 8)                          # the laptop, JOBS
    rr(c, 235, 1458, 330, 174, 10); c.set_source_rgb(*hx('dde7f5')); c.fill()
    txt(c, 'JOBS', 400, 1494, 50, NAVY, lw=0)
    for i in range(3):
        rr(c, 255, 1532 + i * 32, 200, 18, 9); c.set_source_rgb(*hx('9fb0c8')); c.fill()
        rr(c, 468, 1530 + i * 32, 80, 22, 11); c.set_source_rgb(*hx('22c55e')); c.fill()
    c.move_to(200, 1652); c.line_to(600, 1652); c.line_to(640, 1700); c.line_to(160, 1700); c.close_path(); fs(c, hx('3a3f4d'), 8)
    for q, hand in ((-1, (225, 1676)), (1, (575, 1676))):
        K.arm(c, [(hx0 + q * 120, 1440), (hx0 + q * 200, 1560), hand], hs)
    c.rectangle(0, 1040, W, 880); c.set_source_rgba(.1, .16, .4, .26); c.fill()     # TV light on the room

def a11(c, f, r, d):  # the dark room: a slow push-in, the HUMANS line falls, the TV flickers
    c.save(); push(c, r, d, .05, cy=1000); darkroom(c, f, ss((r - 4) / 24), math.sin(r * .25) * 6); c.restore()
    if r % 5 == 0: c.rectangle(0, 0, W, H); c.set_source_rgba(.6, .7, 1, .04); c.fill()
    Sh.topbar(c, '2027')

def a12(c, f, r, d): V.s14(c, f, r)

def bubble_side(c, lines, r, tip, cx, cy, size=58):
    """A bubble beside the speaker: a short tail from its near edge to `tip`."""
    k = back(r / 5)
    if k <= .03: return
    c.save(); c.select_font_face('Lilita One'); c.set_font_size(size)
    w = max(c.text_extents(l).width for l in lines) + 80; h = len(lines) * size * 1.12 + 50
    q = -1 if tip[0] < cx else 1; ty = cy - (h / 2 - 10) * k                   # the tail leaves the top corner nearest the speaker
    c.move_to(cx + q * (w / 2 - 110) * k, ty); c.line_to(*tip); c.line_to(cx + q * (w / 2 - 30) * k, ty); c.close_path(); fs(c, WHITE, 8)
    c.translate(cx, cy); c.scale(k, k); c.translate(-cx, -cy)
    rr(c, cx - w / 2, cy - h / 2, w, h, 36); fs(c, WHITE, 8)
    c.move_to(cx + q * (w / 2 - 104), cy - h / 2 + 12); c.line_to(cx + q * (w / 2 - 36), cy - h / 2 + 12); c.set_source_rgb(*WHITE); c.set_line_width(14); c.stroke()
    for i, l in enumerate(lines): txt(c, l, cx, cy - h / 2 + 25 + size * .56 + i * size * 1.12, size, NAVY, lw=0)
    c.restore()

def a13(c, f, r, d):  # "Thank you, sir." - he sits left; the bubble low beside his face, a short tail to his cheek
    bg(c, 'ff8ebf', 'e8437e'); rays(c, WHITE, f, a=.13)
    x0 = 660; hy = 1020 + math.sin(f) * 4          # he sits right: the bubble stays out of the app's button column
    K.hoodie(c, x0, 1020 + 150 * HS, HS * 1.1); K.hoodyz_head(c, x0, hy, HS, era='young', expr='cry', blink=False)
    for q in (-1, 1):
        for i in range(2):
            ph = ((r / 10 + i * .5) % 1); ell(c, x0 + q * (50 + ph * 14) * HS, 1020 + (40 + ph * 110) * HS, 14, 20); fs(c, Sh.TEAR, 5)
    bubble_side(c, ['THANK YOU,', 'SIR.'], r - 1, (x0 - 96 * HS, hy + 84 * HS), 232, 1400)

def a14(c, f, r, d):  # "I've had these for years." - his hand goes up to the shades, a glint
    c.save(); push(c, r, d, .05, cy=900)
    bob = -8 * math.sin(math.pi * cl((r - 6) / 10))
    desk(c, f, bob=bob, arm='adjust' if r >= 8 else None, cv=0, cv_hand=False, glint=cl((r - 14) / 12) if 14 <= r < 26 else None)
    tip = c.user_to_device(*harv_tip(bob)); c.restore()
    bubble_at(c, ["I'VE HAD THESE", 'FOR YEARS.'], r - 2, tip, 400, 470)

def a15(c, f, r, d): V.s18(c, f, r)

def a16(c, f, r, d):  # silence: HARV still, the panel turns to look at each other (a deliberate hold)
    desk(c, f, cv=0, cv_hand=False, panel_look=ss((r - 1) / 4))

def a17(c, f, r, d):  # close on the cat, where she lies on this desk: she opens one eye at him - the only one who heard
    def cam():
        z = 3.6 + .15 * r / d; c.translate(540, 1350); c.scale(z, z); c.translate(-872, -(DESK - 36))   # the nameplate stays out of shot
    c.save(); cam(); desk(c, f, cv=0, cv_hand=False); c.restore()
    c.rectangle(0, 0, W, H); c.set_source_rgba(.04, .1, .18, .5); c.fill()            # the room falls away
    c.save(); cam()
    cb = 1 + .02 * math.sin(f * LOOPF * .16 + 1)
    c.translate(905, DESK + 2); c.scale(1, cb); c.translate(-905, -(DESK + 2)); Sh.cat_one_eye(c, 905, DESK + 2, .72, open_eye=(r >= 4)); c.restore()

def a18(c, f, r, d):  # HARV, flat: "About your experience..." (v3 put this bubble on Hoody)
    c.save(); push(c, r, d, .03, cy=1000)
    bob = 5 * math.sin(r * .22)
    desk(c, f, bob=bob, cv=0, cv_hand=False)
    tip = c.user_to_device(*harv_tip(bob)); c.restore()
    bubble_at(c, ['ABOUT YOUR', 'EXPERIENCE...'], r - 2, tip, 420, 470, out=d - r)

def a19(c, f, r, d):  # the forced smile comes back: he thinks it is going well
    hoody_close(c, f, 'deadpan' if r < 3 else 'forced', sweat_t=.2 if r >= 3 else None, blink=False)

def a20(c, f, r, d):  # NEW CHAT: the antenna pulses, a twitch, the chip pops - and he picks the same CV up again -> frame 0
    tw = -16 * math.sin(math.pi * cl((r - 2) / 5))
    lift = cl((r - 14) / 10) * .5                                             # reaches .5 on the last frame; frame 0 goes on from there
    desk(c, f, bob=tw, cv=lift, cv_hand=r >= 10, pulse=((r - 1) / 14) if 1 <= r < 18 else 0)
    chip(c, *CHIP, back((r - 4) / 5) if r >= 4 else 0)

FN = dict(a1=a1, a2=a2, a3=a3, a4=a4, a5=a5, a6=a6, a7=a7, a8=a8, a9=a9, a10=a10, a11=a11, a12=a12, a13=a13, a14=a14,
          a15=a15, a16=a16, a17=a17, a18=a18, a19=a19, a20=a20)

# =====================================================================================================
# polish 1 of 2 (21 Nov), from the two cold viewers' shared misreads:
# 1 the last desk shot moves (HARV leans in and taps the CV); 2 no NEW CHAT chip at frame 0 (it is gone by the last frame);
# 3 the yoink arm is thick, with a hand; 4 the reach is an arm from his shoulder, patting; 5 a glint on TV-HARV's shades;
# 6 HARV's hand slides the offer letter in; 7 the tears: greyer pink, a wobbling smile; 8 plain wall behind the cat;
# 9 the eyes insert is a slit (no mouth); 10 bigger shades on his head in 2024-26, a bigger NEW CHAT chip nearer the centre.
# =====================================================================================================
CHIP = (690, 520)
_chip0 = chip
def chip(c, x, y, k): _chip0(c, x, y, k * 1.25)

def a1(c, f, r, d):   # FRAME 0: clean - HARV, the gold shades, the CV already rising; the line from frame 3
    c.save(); push(c, r, d, .03, cy=1000)
    bob = -10 * math.sin(math.pi * cl((r - 8) / 14)) + 5 * math.sin(r * .22)
    desk(c, f, bob=bob, cv=cl(.5 + (r + 1) * .05))
    tip = c.user_to_device(*harv_tip(bob)); c.restore()
    bubble_at(c, ['SAYS HERE YOU USED', 'TO BE OUR BOSS?'], r - 3, tip, 430, 470)

def a3(c, f, r, d):   # his eyes flick to the shades: a slit, eyes only
    bg(c, '1a3a5c', '0d2236')
    c.save(); push(c, r, d, .05, cy=1000)
    K.hoodyz_head(c, 540, 1000 - 8 * 5.6, 5.6, era='young', expr='calm', blink=False, gaze=26 * oe((r - 3) / 4)); c.restore()
    for y0, y1 in ((0, 790), (1215, H)): c.rectangle(0, y0, W, y1 - y0); c.set_source_rgb(*hx('0a1626')); c.fill()
    for y in (790, 1215): c.rectangle(0, y - 5, W, 10); c.set_source_rgb(*INK); c.fill()

def trip(c, f, r, d, expr, cap, extra=None):
    cap0 = V.caption; V.caption = lambda *a, **k: None
    try:
        c.save(); push(c, r, d, .05, cy=1000); c.translate(0, 5 * math.sin(f * 1.3))
        V.triptych(c, f, r, expr, cap, extra=extra, gold=False)
        shades(c, 540 + 6 * 1.6, 860 - 120 * 1.6, 1.15 * 1.6, rot=-.06)        # his gold shades, big enough for a phone
        c.restore()
    finally: V.caption = cap0
    V.caption(c, cap, r)

def a9(c, f, r, d):   # the theft: a thick white arm, a hand that grips the shades, YOINK
    bg(c, '9be3c6', '2f9e7a'); rays(c, WHITE, f, a=.12)
    hx_, hy_, hs = 390, 980, 2.0
    K.hoodie(c, hx_, hy_ + 150 * hs, hs * 1.1); K.hoodyz_head(c, hx_, hy_, hs, era='young', expr='calm', blink=False)
    k = ss((r - 3) / 10)
    bx, by, bs = 850, 1180, 1.3
    sx, sy = lerp(hx_ + 6 * hs, bx, k), lerp(hy_ - 120 * hs, by - 12 * bs, k) - math.sin(k * math.pi) * 160
    sc = lerp(1.15 * 1.6, 1.02 * bs, k)
    Sh.harv(c, bx, by, bs, shade=False, mouth='flat', eyes=(-6, -6))
    hand = (sx + 110 * sc * .5, sy + 16)
    limb(c, [(bx - 70 * bs, by + 110 * bs), (lerp(bx - 230, bx - 60, k), lerp(by - 120, by + 60, k)), hand], 46, WHITE)
    shades(c, sx, sy, sc, rot=-.06 * (1 - k))
    ell(c, *hand, 34, 34); fs(c, WHITE, 8)                                     # its mitt on the frame
    if r >= 9: txt(c, 'YOINK!', 740, 620, 120 * back((r - 9) / 5), YEL, lw=20, rot=.08)

def a10(c, f, r, d):  # his hand goes up to the empty spot on his head and pats it
    head = hoody_close(c, f, 'shock', blink=False)
    k = ss(r / 6); pat = 14 * math.sin(max(0, r - 6) * 1.6)
    hand = (lerp(250, 470, k), lerp(1500, 745, k) + pat)
    K.arm(c, [(330, 1500), (lerp(190, 205, k), lerp(1560, 1180, k)), hand], 2.2)
    ell(c, *hand, 58, 58); fs(c, SKIN, 9)
    if r >= 7:
        for i in (-1, 0, 1): c.move_to(hand[0] + i * 46, hand[1] - 84); c.line_to(hand[0] + i * 62, hand[1] - 126); c.set_source_rgb(*WHITE); c.set_line_width(8); c.stroke()

def a11(c, f, r, d):  # the dark room; a glint on TV-HARV's shades ties him to the thief
    c.save(); push(c, r, d, .05, cy=1000); darkroom(c, f, ss((r - 4) / 24), math.sin(r * .25) * 6)
    V.sparkle(c, 812, 598, 46 * math.sin(math.pi * cl((r - 26) / 12))); c.restore()
    if r % 5 == 0: c.rectangle(0, 0, W, H); c.set_source_rgba(.6, .7, 1, .04); c.fill()
    Sh.topbar(c, '2027')

def a12(c, f, r, d):  # the offer: HARV's white hand slides the letter up in front of him, then lets go
    V.s14(c, f, r)
    y = lerp(1950, 1260, oe(r / 6)); away = cl((r - 12) / 6)
    hand = (880 + 260 * away, y + 330 + 200 * away)
    limb(c, [(1180, 1900), (1010 + 200 * away, y + 520 + 160 * away), hand], 70, WHITE); ell(c, *hand, 48, 48); fs(c, WHITE, 8)

def a13(c, f, r, d):  # "Thank you, sir." - greyer pink, the smile wobbling: he takes it
    bg(c, 'd9a3b8', '9c5a78'); rays(c, WHITE, f, a=.08)
    x0 = 660; hy = 1020 + math.sin(f * 1.7) * 5
    K.hoodie(c, x0, 1020 + 150 * HS, HS * 1.1); K.hoodyz_head(c, x0, hy, HS, era='young', expr='cry', blink=False, rot=.02 * math.sin(f * 1.1))
    for q in (-1, 1):
        for i in range(2):
            ph = ((r / 10 + i * .5) % 1); ell(c, x0 + q * (50 + ph * 14) * HS, 1020 + (40 + ph * 110) * HS, 14, 20); fs(c, Sh.TEAR, 5)
    bubble_side(c, ['THANK YOU,', 'SIR.'], r - 1, (x0 - 96 * HS, hy + 84 * HS), 232, 1400)

def a17(c, f, r, d):  # close on the cat on the desk, plain wall behind: she opens one eye at him
    bg(c, '10354f', '0d2236')
    z = 3.6 + .15 * r / d
    c.save(); c.translate(540, 1350); c.scale(z, z); c.translate(-872, -(DESK - 36))
    rr(c, -400, DESK, 2000, 64, 18); fs(c, hx('a9713f'))
    c.rectangle(-400, DESK + 60, 2000, 700); c.set_source_rgb(*hx('7c4f2a')); c.fill()
    cb = 1 + .02 * math.sin(f * LOOPF * .16 + 1)
    c.translate(905, DESK + 2); c.scale(1, cb); c.translate(-905, -(DESK + 2)); Sh.cat_one_eye(c, 905, DESK + 2, .72, open_eye=(r >= 4)); c.restore()

def a18(c, f, r, d):  # HARV leans in and taps the CV twice: "About your experience..."
    c.save(); push(c, r, d, .07, cy=1000)
    lean = ss(r / 8); tap = max(0, math.sin((r - 10) * .5)) if 10 <= r < 36 else 0
    bob = 22 * lean + 5 * math.sin(r * .22)
    desk(c, f, bob=bob, cv=.1 * tap, cv_hand=r >= 6)
    tip = c.user_to_device(*harv_tip(bob)); c.restore()
    bubble_at(c, ['ABOUT YOUR', 'EXPERIENCE...'], r - 2, tip, 420, 470, out=d - r)

def a20(c, f, r, d):  # NEW CHAT: pulse, twitch, the chip pops and is gone again before the cut; he lifts the same CV -> frame 0
    tw = -16 * math.sin(math.pi * cl((r - 2) / 5))
    lift = cl((r - 14) / 10) * .5
    desk(c, f, bob=tw, cv=lift, cv_hand=r >= 10, pulse=((r - 1) / 14) if 1 <= r < 16 else 0)
    chip(c, *CHIP, (back((r - 3) / 5) if r >= 3 else 0) * (1 - cl((r - 19) / 4)))

FN.update(a1=a1, a3=a3, a6=a6, a7=a7, a8=a8, a9=a9, a10=a10, a11=a11, a12=a12, a13=a13, a17=a17, a18=a18, a20=a20)

def draw(f):
    S = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(S)
    for n, d, pill in SHOTS:
        a = START[n]
        if a <= f < a + d:
            c.save(); FN[n](c, f, f - a, d); c.restore(); c.identity_matrix()
            if n != 'a11': Sh.topbar(c, pill)
            break
    return S

def _mid(n, k=.6): return START[n] + int(dict((x[0], x[1]) for x in SHOTS)[n] * k)
KEYS = [(0, '0  frame 0'), (_mid('a1', .4), 'a1  the line'), (_mid('a2', .2), 'a2  forced smile'), (_mid('a2', .8), 'a2  ...yes'),
        (_mid('a3'), 'a3  eyes'), (_mid('a4'), 'a4  the shades'), (_mid('a5'), 'a5  rewind'), (_mid('a6'), 'a6  2024'),
        (_mid('a7'), 'a7  2025'), (_mid('a8'), 'a8  2026'), (_mid('a9', .8), 'a9  yoink'), (_mid('a10', .9), 'a10  reach'),
        (_mid('a11', .8), 'a11  dark room'), (_mid('a12', .7), 'a12  offer'), (_mid('a13'), 'a13  thank you'),
        (_mid('a14'), 'a14  had these'), (_mid('a15'), 'a15  MINE'), (_mid('a16', .8), 'a16  silence'), (_mid('a17', .8), 'a17  cat'),
        (_mid('a18'), 'a18  about your...'), (_mid('a19', .7), 'a19  hope'), (_mid('a20', .4), 'a20  NEW CHAT'),
        (NF - 1, 'last frame'), (0, 'frame 0 again')]

# =====================================================================================================
# polish 2 of 2 (21 Nov): the animation pass.
# - HARV visibly speaks: his antenna glows with his voice and his head tilts on each phrase (his mouth stays flat: he never smiles);
#   the panel robots turn to him while he talks.
# - Hoody's mouth moves on "...yes."; a cut "pop" (a 5-frame settle) on his shots; the forced smile snaps back with a squash.
# - NEW CHAT holds 0.7 s (the last shot is 30 frames, was 24), still gone before the cut.
# =====================================================================================================
import numpy as _np, soundfile as _sf
SHOTS[-1] = ('a20', 30, '2027')
START.clear(); _t = 0
for _n, _d, _p in SHOTS: START[_n] = _t; _t += _d
NF = _t
LOOPF = 2 * math.pi * 45 / .45 / NF
def _env(name):
    x, sr = _sf.read(os.path.join(V3, 'vo', name + '.wav')); n = sr // FPS; m = len(x) // n
    e = _np.sqrt((x[:m * n].reshape(m, n) ** 2).mean(1)); e = e / (e.max() + 1e-9)
    return _np.convolve(_np.clip(e * 1.8, 0, 1), [.25, .5, .25], 'same')
ENV = {n: _env(n) for n, _, _ in VO}
def voice(f, names):
    v = 0.0
    for n, s, off in VO:
        if n in names:
            i = f - START[s] - off
            if 0 <= i < len(ENV[n]): v = max(v, float(ENV[n][i]))
    return v
G = dict(sp=0.0, tilt=0.0)
_harv0 = Sh.harv
def _harv(c, x, y, s, **k):
    if s != HSC: return _harv0(c, x, y, s, **k)
    c.save(); c.translate(x, y + 200 * s); c.rotate(G['tilt']); c.translate(-x, -(y + 200 * s))
    if G['sp'] > .03:
        for i in range(3): ell(c, x, y - 140 * s, (26 + i * 16) * s * .6 + 30 * G['sp'], (26 + i * 16) * s * .6 + 30 * G['sp']); c.set_source_rgba(.35, .8, 1, .28 * G['sp']); c.fill()
    _harv0(c, x, y, s, **k); c.restore()
Sh.harv = _harv
def harv_tip(bob=0):
    px, py = HX, HY + bob + 200 * HSC; dx, dy = 0, -357 * HSC; a = G['tilt']
    return (px + dx * math.cos(a) - dy * math.sin(a), py + dx * math.sin(a) + dy * math.cos(a))
_desk0 = desk
def desk(c, f, **k):
    k['panel_look'] = max(k.get('panel_look', 0), .5 * G['sp_s']); return _desk0(c, f, **k)

def a2(c, f, r, d):   # the forced smile, the sweat sliding, one blink - then it cracks and he says it: "...yes."
    bg(c, '1a3a5c', '0d2236'); rays(c, WHITE, f, a=.05)
    crack = r >= 8; sink = 10 * ss((r - 8) / 5)
    K.hoodie(c, 540, 1020 + 150 * HS + sink * .4, HS * 1.1)
    hy = 1020 + sink - 6 * math.sin(f * .2)
    K.hoodyz_head(c, 540, hy, HS, era='young', expr='cracked' if crack else 'forced', blink=(3 <= r < 6), op=voice(f, ('g1',)) * .9 if crack else 0)
    if not crack: Sh.sweat(c, 540 + 112 * HS, hy + (-44 + 70 * cl(r / 8) * .7) * HS, HS * .9)

def a19(c, f, r, d):  # the forced smile snaps back on, with a squash: he thinks it is going well
    k = cl((r - 3) / 4); sq = 1 - .06 * math.sin(math.pi * k)
    c.save(); c.translate(540, 1700); c.scale(2 - sq, sq); c.translate(-540, -1700)
    hoody_close(c, f, 'deadpan' if r < 3 else 'forced', sweat_t=.2 if r >= 3 else None, blink=False); c.restore()

def a20(c, f, r, d):  # NEW CHAT: pulse, twitch, the chip holds 0.7 s and is gone before the cut; he lifts the same CV -> frame 0
    tw = -16 * math.sin(math.pi * cl((r - 2) / 5))
    desk(c, f, bob=tw, cv=cl((r - 19) / 10) * .5, cv_hand=r >= 14, pulse=((r - 1) / 14) if 1 <= r < 20 else 0)
    chip(c, *CHIP, (back((r - 3) / 5) if r >= 3 else 0) * (1 - cl((r - 24) / 4)))

FN.update(a2=a2, a19=a19, a20=a20)
POP = {'a2', 'a3', 'a4', 'a6', 'a7', 'a8', 'a9', 'a10', 'a12', 'a13', 'a15', 'a19'}
HARV_LINES = ('h1', 'h2', 'h3')
def draw(f):
    S = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(S)
    sp = voice(f, HARV_LINES); G['sp'] = sp
    G['sp_s'] = max(voice(f - k, HARV_LINES) for k in range(0, 9))               # held after each syllable; nothing anticipates, so frame 0 matches the last frame
    G['tilt'] = .045 * G['sp_s'] * math.sin(f * .33)
    for n, d, pill in SHOTS:
        a = START[n]
        if a <= f < a + d:
            r = f - a
            c.save()
            if n in POP and r < 5:
                z = 1 + .05 * (1 - oe(r / 5)); c.translate(540, 1000); c.scale(z, z); c.translate(-540, -1000)
            FN[n](c, f, r, d); c.restore(); c.identity_matrix()
            if n != 'a11': Sh.topbar(c, pill)
            break
    return S
KEYS = [(0, '0')]

if __name__ == '__main__':
    os.chdir(HERE); a = sys.argv[1:]
    if a[:1] == ['frames']:
        for f in map(int, a[1:]): draw(f).write_to_png(f'chk_{f:03d}.png')
    elif a[:1] == ['keys']:
        from PIL import Image, ImageDraw, ImageFont
        tw, th = 270, 480; cols = 6; rows = (len(KEYS) + cols - 1) // cols
        sheet = Image.new('RGB', (cols * (tw + 12) + 12, rows * (th + 50) + 12), 'white'); dr = ImageDraw.Draw(sheet)
        font = ImageFont.truetype(os.path.expanduser('~/.fonts/LilitaOne-Regular.ttf'), 28)
        for i, (f, lab) in enumerate(KEYS):
            draw(f).write_to_png('_k.png'); x = 12 + (i % cols) * (tw + 12); y = 12 + (i // cols) * (th + 50)
            sheet.paste(Image.open('_k.png').resize((tw, th)), (x, y)); dr.text((x, y + th + 8), lab, fill='#1b2030', font=font)
        os.remove('_k.png'); sheet.save('keys.png'); print('keys ok', NF, NF / 30)
    else:
        final = a[:1] == ['final']
        p = subprocess.Popen(f'ffmpeg -y -v error -f rawvideo -pix_fmt bgra -s {W}x{H} -r 30 -i - -vf format=yuv420p -c:v libx264 -crf {14 if final else 18} -preset {"slow" if final else "veryfast"} -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709 tmp_video.mp4'.split(), stdin=subprocess.PIPE)
        for f in range(NF): p.stdin.write(bytes(draw(f).get_data()))
        p.stdin.close(); assert p.wait() == 0; os.rename('tmp_video.mp4', 'video.mp4'); print('video ok', NF)
