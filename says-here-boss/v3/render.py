"""Hoodyz - Says Here You Were Our Boss, v3. 19 shots, 19.07 s, 572 frames at 30 fps, 1080x1920.
Usage: python3 render.py frames 0 30 ...  |  python3 render.py video"""
import sys, os, math, random, subprocess, cairo
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chars as Sh, kit as K
from kit import INK, WHITE, NAVY, SKIN, BLUE, YEL, RED, GREY, rr, fs, ell, limb, txt, shades, hx, lerp, cl, ss
W, H = 1080, 1920
back = lambda t: 0.02 if t <= 0 else (1 if t >= 1 else max(.02, 1 + 2.7 * (t - 1) ** 3 + 1.7 * (t - 1) ** 2))
oe = lambda t: 1 - (1 - cl(t)) ** 3

def bg(c, top, bot):
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, *hx(top)); g.add_color_stop_rgb(1, *hx(bot)); c.set_source(g); c.paint()
def rays(c, col, f, cx=540, cy=1050, a=.10):
    c.save(); c.translate(cx, cy); c.rotate(f * .012)
    for i in range(12):
        th = i / 12 * 2 * math.pi; c.move_to(0, 0); c.line_to(2400 * math.cos(th), 2400 * math.sin(th)); c.line_to(2400 * math.cos(th + .26), 2400 * math.sin(th + .26)); c.close_path()
    c.set_source_rgba(*col, a); c.fill(); c.restore()
def bubble(c, lines, r, tail, cy=500, size=66, out=None, cx=540):
    """Speech bubble under the title bar. tail: (x, y) the tail points at. Pops in on r; out: frames left -> shrink away."""
    k = back(r / 5) if out is None else back(r / 5) * cl(out / 3)
    if k <= .03: return
    c.save(); c.translate(cx, cy); c.scale(k, k)
    c.select_font_face('Lilita One'); c.set_font_size(size)
    w = max(c.text_extents(l).width for l in lines) + 90; h = len(lines) * size * 1.12 + 56
    tx, ty = (tail[0] - cx) / k, (tail[1] - cy) / k
    c.move_to(-60, h / 2 - 6); c.line_to(tx, ty); c.line_to(30, h / 2 - 6); c.close_path(); fs(c, WHITE, 8)
    rr(c, -w / 2, -h / 2, w, h, 40); fs(c, WHITE, 8)
    c.move_to(-58, h / 2 - 12); c.line_to(28, h / 2 - 12); c.set_source_rgb(*WHITE); c.set_line_width(14); c.stroke()
    for i, l in enumerate(lines): txt(c, l, 0, -h / 2 + 28 + size * .56 + i * size * 1.12, size, NAVY, lw=0)
    c.restore()
def caption(c, s, r, col=WHITE, y=470, size=96):
    txt(c, s, 540, y, size * back(r / 6), col, lw=size * .18)

# ---------------- reusable set-ups ----------------
HS = 2.4      # Hoody close-up scale
def hoody_close(c, f, expr, sweat_t=None, gaze=0, gold=False):
    bg(c, '1a3a5c', '0d2236'); rays(c, WHITE, f, a=.05)
    K.hoodie(c, 540, 1020 + 150 * HS, HS * 1.1)
    K.hoodyz_head(c, 540, 1020, HS, era='young', expr=expr, blink=False, gaze=gaze)
    if sweat_t is not None: Sh.sweat(c, 540 + 112 * HS, 1020 + (-44 + 70 * sweat_t) * HS, HS * .9)

def desk_room(c, f, z=1.0, mouth='flat', arm=None, cat_eye=False, panel_look=0.0, cv=True):
    bg(c, '10354f', '0d2236')
    c.save(); c.translate(540, 1000); c.scale(z, z); c.translate(-540, -1000)
    for i in range(6): c.rectangle(90 + i * 180, 700, 8, 420); c.set_source_rgba(1, 1, 1, .05); c.fill()
    K.robot(c, 160, 880, .78, eye=(14 * panel_look, 0)); K.robot(c, 920, 880, .78, eye=(-14 * panel_look, 0))
    Sh.harv(c, 540, 830, 1.3, mouth=mouth, arm=arm)
    rr(c, -40, 1080, 1160, 60, 18); fs(c, hx('a9713f'))
    c.rectangle(30, 1140, 1020, 600); c.set_source_rgb(*hx('7c4f2a')); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(8); c.stroke()
    Sh.nameplate(c, 540, 1270, .92)
    Sh.cat_one_eye(c, 860, 1082, .62, open_eye=cat_eye)
    if cv:
        c.save(); c.translate(400, 1030); c.rotate(-.08); rr(c, -70, -48, 140, 96, 10); fs(c, WHITE, 6); txt(c, 'CV', 0, 0, 44, INK, lw=0); c.restore()
        limb(c, [(540 - 70 * 1.3, 830 + 110 * 1.3), (430, 1060)], 30, WHITE)
    c.restore()

def triptych(c, f, r, expr, cap, extra=None, gold=True):
    bg(c, 'ffd84a', 'ff9a2b') if cap == 'PROMPT ENGINEER' else (bg(c, 'b8c4d6', '5b6b85') if cap == 'PROMPT MANAGER' else bg(c, '9be3c6', '2f9e7a'))
    rays(c, WHITE, f, cy=1000, a=.12)
    if extra: extra(c, f, r)
    Sh.hoody(c, 540, 860, 1.6, expr, gold=gold)
    rr(c, 300, 1130, 480, 300, 26); fs(c, hx('8b93a3'), 9); ell(c, 540, 1280, 34, 34); c.set_source_rgb(*hx('c9ced8')); c.fill()
    for q in (-1, 1): K.arm(c, [(540 + q * 150, 1060), (540 + q * 220, 1180), (540 + q * 200, 1150)], 1.6)
    caption(c, cap, r)

# ---------------- the 20 shots ----------------
def s1(c, f, r):  hoody_close(c, f, 'forced', sweat_t=r / 20 * .5)
def s2(c, f, r):
    desk_room(c, f, z=1.0 + .03 * r / 42)
    bubble(c, ['SAYS HERE YOU USED', 'TO BE OUR BOSS?'], r - 1, (610, 670), cy=500)
def s3(c, f, r):  hoody_close(c, f, 'cracked' if r >= 3 else 'forced')
def s4(c, f, r):  # eyes insert, flick to the shades
    bg(c, '1a3a5c', '0d2236')
    K.hoodyz_head(c, 540, 1000 - 8 * 5.6, 5.6, era='young', expr='calm', blink=False, gaze=26 * oe((r - 3) / 4))
def s5(c, f, r):  # the shades, glint sweeps
    bg(c, '10354f', '0d2236')
    Sh.harv(c, 540, 1060, 4.2, mouth='flat')
    c.save(); c.translate(540, 1060); c.scale(4.2, 4.2); c.translate(0, -12); c.scale(1.02, 1.02)
    rr(c, -92, -28, 84, 58, 22); rr(c, 8, -28, 84, 58, 22); c.clip()
    gx = lerp(-200, 200, ss((r - 4) / 12)); c.move_to(gx - 30, -40); c.line_to(gx + 10, -40); c.line_to(gx - 20, 40); c.line_to(gx - 60, 40); c.close_path()
    c.set_source_rgba(1, 1, 1, .55); c.fill(); c.restore()
    k = math.sin(math.pi * cl((r - 9) / 10)); sparkle(c, 540 + 88 * 4.2, 1060 - 40 * 4.2, 90 * k)
def sparkle(c, x, y, R):
    if R < 2: return
    c.save(); c.translate(x, y); c.move_to(0, -R)
    for i in range(1, 8): a = i * math.pi / 4; rad = R if i % 2 == 0 else R * .22; c.line_to(rad * math.sin(a), -rad * math.cos(a))
    c.close_path(); c.set_source_rgb(1, 1, 1); c.fill_preserve(); c.set_source_rgb(*YEL); c.set_line_width(4); c.stroke(); c.restore()
def s7(c, f, r):  # rewind card
    bg(c, 'c91e47', '5b0d2a')
    c.save(); c.translate(-(r * 40) % 160, 0)
    for i in range(14): c.move_to(i * 160 - 400, 0); c.line_to(i * 160 - 320, 0); c.line_to(i * 160 + 80, H); c.line_to(i * 160, H); c.close_path()
    c.set_source_rgba(1, .84, .15, .16); c.fill(); c.restore()
    for k in (0, 1):
        x = 300 + k * 120; c.move_to(x + 100, 860); c.line_to(x, 960); c.line_to(x + 100, 1060); c.close_path(); fs(c, YEL, 10)
    txt(c, 'REWIND', 540, 1200, 150 * back(r / 5), YEL, lw=26)
def agents(c, f, r):
    rnd = random.Random(7)
    for i in range(26):
        x = rnd.choice([rnd.uniform(70, 330), rnd.uniform(750, 1010), rnd.uniform(200, 880)]); y = rnd.uniform(560, 1500)
        if 330 < x < 750 and 640 < y < 1120: y = rnd.choice([rnd.uniform(560, 620), rnd.uniform(1180, 1500)])
        if r < i * .9: continue
        c.save(); c.translate(x, y + math.sin(f * .3 + i) * 6); c.rotate(rnd.uniform(-.15, .15))
        rr(c, -90, -60, 180, 120, 14); fs(c, WHITE, 6); c.rectangle(-90, -60, 180, 24); c.set_source_rgb(*hx('64748b')); c.fill()
        ell(c, -28, 14, 12, 14); ell(c, 28, 14, 12, 14); c.set_source_rgb(*BLUE); c.fill(); c.restore()
def mentee(c, f, r):
    Sh.harv(c, 830, 1010 + math.sin(f * .4) * 4, .55, shade=False, mouth='flat', eyes=(-4, -4))
def s8(c, f, r):  triptych(c, f, r, 'confident', 'PROMPT ENGINEER')
def s9(c, f, r):
    triptych(c, f, r, 'sheepish', 'PROMPT MANAGER', extra=agents)
    for q, ph in ((1, 0), (-1, .5)): Sh.sweat(c, 540 + q * 118 * 1.6, 860 + (-40 + 90 * ((r / 18 + ph) % 1)) * 1.6, 1.2)
def s10(c, f, r): triptych(c, f, r, 'happy', 'MENTOR', extra=mentee)
def s11(c, f, r):  # the theft
    bg(c, '9be3c6', '2f9e7a'); rays(c, WHITE, f, a=.12)
    hx_, hy_, hs = 400, 980, 2.0
    K.hoodie(c, hx_, hy_ + 150 * hs, hs * 1.1); K.hoodyz_head(c, hx_, hy_, hs, era='young', expr='calm', blink=False)
    k = ss((r - 3) / 10)
    bx, by, bs = 830, 1150, 1.0
    sx, sy, sc = lerp(hx_ + 6 * hs, bx, k), lerp(hy_ - 112 * hs, by - 12 * bs, k) - math.sin(k * math.pi) * 160, lerp(.78 * hs, 1.02 * bs, k)
    Sh.harv(c, bx, by, bs, shade=False, mouth='flat', eyes=(-6, -6))
    limb(c, [(bx - 70 * bs, by + 110 * bs), (lerp(bx - 200, bx - 40, k), lerp(by - 40, by + 40, k)), (sx + 40, sy + 20)], 30 * bs, WHITE)
    shades(c, sx, sy, sc, rot=-.06 * (1 - k))
    if r >= 9: txt(c, 'YOINK!', 760, 640, 110 * back((r - 9) / 5), YEL, lw=20, rot=.08)
def s12(c, f, r):  # empty forehead, the reach
    hoody_close(c, f, 'shock')
    k = ss(r / 7); hxp, hyp = lerp(120, 400, k), lerp(1500, 700, k)
    K.arm(c, [(-80, 1750), (lerp(60, 170, k), lerp(1500, 1150, k)), (hxp, hyp)], 2.0)
    ell(c, hxp, hyp, 46, 46); fs(c, SKIN, 8)
def s13(c, f, r):
    Sh.darkroom_draw(c, t=ss((r - 6) / 26), bob=math.sin(r * .25) * 6)
def s14(c, f, r):  # offer letter, his face above it
    bg(c, '10354f', '0d2236')
    K.hoodie(c, 540, 700 + 150 * 1.6, 1.6 * 1.1); K.hoodyz_head(c, 540, 700, 1.6, era='young', expr='hopeful' if r < 10 else 'deadpan', blink=False)
    y = lerp(1950, 1260, oe(r / 6)); z = 1 + .06 * ss((r - 10) / 30)
    c.save(); c.translate(540, y); c.rotate(-.025); c.scale(z, z)
    rr(c, -400, -420, 800, 840, 26); fs(c, hx('fbf8ee'), 10)
    txt(c, 'OFFER LETTER', 0, -350, 66, INK, lw=0); c.rectangle(-330, -300, 660, 7); c.set_source_rgb(*INK); c.fill()
    txt(c, 'ROLE:', -330, -240, 46, hx('66707f'), lw=0, align='l'); txt(c, 'PROMPT ENGINEER', -330, -180, 70, INK, lw=0, align='l')
    txt(c, 'PAY:', -330, -100, 46, hx('66707f'), lw=0, align='l')
    if r >= 8: txt(c, '9.99', 0, 50, 260 * back((r - 8) / 5), RED, lw=0)
    if r >= 8: txt(c, 'TOKENS / HOUR', 0, 225, 78, INK, lw=0)
    c.restore()
def s16(c, f, r):
    bg(c, 'ff8ebf', 'e8437e'); rays(c, WHITE, f, a=.13)
    K.hoodie(c, 540, 1020 + 150 * HS, HS * 1.1); K.hoodyz_head(c, 540, 1020 + K.math.sin(f) * 4, HS, era='young', expr='cry', blink=False)
    for q in (-1, 1):
        for i in range(2):
            ph = ((r / 10 + i * .5) % 1); ell(c, 540 + q * (50 + ph * 14) * HS, 1020 + (40 + ph * 110) * HS, 14, 20); fs(c, Sh.TEAR, 5)
    bubble(c, ['THANK YOU, SIR.'], r - 1, (560, 660), cy=470)
def s17(c, f, r):  # "I've had these for years."
    desk_room(c, f, z=1.22 + .02 * r / 56, mouth='flat', arm='adjust', cv=False)
    bubble(c, ["I'VE HAD THESE", 'FOR YEARS.'], r - 2, (520, 640), cy=500, cx=360)
def s18(c, f, r):  # THOSE ARE MINE! - the one wide of his face
    if r < 8: c.translate(K.math.sin(f * 7) * (8 - r) * 4, K.math.cos(f * 9) * (8 - r) * 4)
    bg(c, 'c91e47', '5b0d2a'); rays(c, YEL, f, a=.10)
    hs = 1.5
    K.arm(c, [(690, 1290), (840, 1150), (870, 900)], hs); ell(c, 870, 890, 46, 46); fs(c, SKIN, 8)       # fist up
    K.arm(c, [(390, 1290), (360, 1230), (380, 1190)], hs)                                                  # arm out at the shades
    K.hoodie(c, 540, 1000 + 150 * hs, hs * 1.1); K.hoodyz_head(c, 540, 1000, hs, era='young', expr='blown', blink=False)
    limb(c, [(372, 1192), (300, 1200)], 26, SKIN); ell(c, 372, 1194, 40, 40); fs(c, SKIN, 8)             # pointing hand
    Sh.harv(c, 40, 1300, 2.2, mouth='flat')                                                                # foreground: HARV in Hoody's shades
    txt(c, 'THOSE ARE', 540, 470, 120 * back(r / 3), YEL, lw=22); txt(c, 'MINE!', 540, 610, 170 * back((r - 1) / 3), YEL, lw=28)
def s19(c, f, r):  # nothing happens: HARV still, the panel looks at each other, the cat opens one eye
    look = ss((r - 1) / 4)
    bg(c, '10354f', '0d2236')
    for i in range(6): c.rectangle(90 + i * 180, 640, 8, 500); c.set_source_rgba(1, 1, 1, .05); c.fill()
    for x, q in ((190, 1), (890, -1)):
        c.save(); c.translate(x, 1000); c.rotate(.32 * q * look); c.translate(-x, -1000)
        K.robot(c, x + 24 * q * look, 900, 1.0, eye=(22 * q * look, -4 * look)); c.restore()
    Sh.harv(c, 540, 840, 1.3, mouth='flat')
    rr(c, -40, 1130, 1160, 60, 18); fs(c, hx('a9713f'))
    c.rectangle(30, 1190, 1020, 600); c.set_source_rgb(*hx('7c4f2a')); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(8); c.stroke()
    Sh.nameplate(c, 540, 1330, .92)                     # same room as shot 2: the nameplate stays
    Sh.cat_one_eye(c, 560, 1135, 1.1, open_eye=False)
def s19b(c, f, r):  # close on the cat: the only one in the room who heard him
    bg(c, '10354f', '0d2236')
    c.save(); c.translate(540, 520); c.scale(2.2, 2.2); c.translate(-540, -520)
    Sh.harv(c, 540, 575, 1.3, mouth='flat'); c.restore()                       # HARV's body, out of focus behind
    c.rectangle(0, 0, W, H); c.set_source_rgba(.04, .1, .18, .55); c.fill()
    rr(c, -40, 1140, 1160, 70, 20); fs(c, hx('a9713f'))
    c.rectangle(0, 1210, W, 710); c.set_source_rgb(*hx('7c4f2a')); c.fill()
    Sh.cat_one_eye(c, 540 + 92 * 2.8, 1146, 2.8, open_eye=(r >= 4))
def s20(c, f, r):  # back to frame 0
    if r < 5: hoody_close(c, f, 'deadpan')
    else: hoody_close(c, f, 'forced', sweat_t=0)
    bubble(c, ['ABOUT YOUR', 'EXPERIENCE...'], r - 2, (860, 650), cy=500, cx=660, out=45 - r)

# fix 1: the jaw-tight shot (old 6) is cut - a fresh viewer couldn't read it. Retimed for the recorded lines.
SHOTS = [(s1, 0, 20, '2027'), (s2, 20, 62, '2027'), (s3, 62, 81, '2027'), (s4, 81, 96, '2027'), (s5, 96, 120, '2027'),
         (s7, 120, 134, 'REWIND'), (s8, 134, 170, '2024'), (s9, 170, 206, '2025'), (s10, 206, 236, '2026'),
         (s11, 236, 260, '2026'), (s12, 260, 276, '2026'), (s13, 276, 330, '2027'), (s14, 330, 372, '2027'),
         (s16, 372, 403, '2027'), (s17, 403, 459, '2027'), (s18, 459, 489, '2027'), (s19, 489, 505, '2027'), (s19b, 505, 523, '2027'),
         (s20, 523, 572, '2027')]
NF = 572   # 15 Nov review: twitch shot cut, 9.99 held ~1.1 s

def draw(f):
    S = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(S)
    for fn, a, b, pill in SHOTS:
        if a <= f < b:
            c.save(); fn(c, f, f - a); c.restore(); c.identity_matrix()
            if fn is not s13: Sh.topbar(c, pill)
            break
    return S

if __name__ == '__main__':
    if sys.argv[1] == 'frames':
        for f in map(int, sys.argv[2:]): draw(f).write_to_png(f'chk_{f:03d}.png')
    else:
        p = subprocess.Popen(f'ffmpeg -y -v error -f rawvideo -pix_fmt bgra -s {W}x{H} -r 30 -i - -vf format=yuv420p -c:v libx264 -crf 18 -preset veryfast -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709 tmp_video.mp4'.split(), stdin=subprocess.PIPE)
        for f in range(NF): p.stdin.write(bytes(draw(f).get_data()))
        p.stdin.close(); assert p.wait() == 0; os.rename('tmp_video.mp4', 'video.mp4'); print('video ok')
