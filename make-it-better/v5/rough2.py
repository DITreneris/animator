"""Make It Better v5.3: rough 2. 19 shots, 25 s, each composed for the 9:16 frame (faces just under the bar,
a foreground layer, eyelines that meet), with motion in every shot. Label: HER BIRTHDAY -> ITS UNION.
Usage: python3 rough2.py sheet | video | audio"""
import os, sys, math, subprocess, cairo
import numpy as np, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import kp as S, sb as B, shots2 as N, rough as R1
from kp import R, K, Sh, A, E, P4, INK, WHITE, NAVY, YEL, SKIN, CREAM, RED, rr, fs, ell, limb, txt, hx, lerp, W, H
FPS = 30
def ease(t): t = max(0., min(1., t)); return t * t * (3 - 2 * t)
def pop(r, at): return max(0, r - at)                          # bubble scale-in clock

def banner2(c, x, y, w, h, state):
    """The banner's ladder: v1 clean; pro: corporate grey 'Q3 BIRTHDAY' with a bar chart; cat: + a sticker."""
    if state == 'v1': S.banner(c, x, y, w, h, 'v1', text='HAPPY B-DAY EVA'); return
    c.save(); c.translate(x, y); rr(c, -w / 2, -h / 2, w, h, 10); fs(c, hx('c9ced8'), 7)
    txt(c, 'Q3 BIRTHDAY', -w * .12, -h * .12, h * .24, hx('4a5163'), lw=0)
    for i in range(4): rr(c, w * .2 + i * w * .06, h * .3 - i * h * .1, w * .04, h * .06 + i * h * .1, 2); c.set_source_rgb(*hx('7d8597')); c.fill()
    if state == 'cat': c.save(); c.translate(-w * .3, h * .18); c.rotate(-.3); K._cat_head(c, 0, 0, h / 300, False, 'open', 0); c.restore()
    c.restore()

def dog(c, x, gy, s, f=0, wag=True, face=-1, look=0, card=None):
    """Eva's dog (Who's a Good Boy?). face -1 looks left (as drawn), +1 right. wag False freezes the tail.
    card: a word on a little card in his mouth."""
    c.save(); c.translate(x, gy); c.scale(-face, 1); c.translate(-x, -gy)
    E.dog(c, x, gy, s, look=look, f=f if wag else 2.6)
    c.restore()
    if card:
        mx = x + face * (-58) * s * (-1); hy = gy - 138 * s - look * 14 * s
        cx_ = x - (12 + 52) * s * (1 if face < 0 else -1)
        S.card_front(c, cx_, hy + 46 * s, 120 * s, 80 * s, card, 46 * s, 'box') if card != '_' else S.card_back(c, cx_, hy + 46 * s, 120 * s, 80 * s, 'box')

# ---------------- the 19 shots: fn(c, f, r) ----------------
def sh01(c, f, r):
    N.n01(c, f)
def sh01b(c, f, r): N.n01b(c, f)
def sh02(c, f, r):                                             # the ladder flash
    N.wall(c)
    st = 0 if r < 20 else 1 if r < 40 else 2
    droop = [.3, .6, lerp(.6, 1.0, ease((r - 40) / 10))][st]
    eye = ['open', 'focus', 'blank'][st]
    gx, gy = N.ai_at(c, (540, 820), 1.7, eye=eye, droop=droop, arms=('down', 'down'))
    if st == 0: P4.tie(c, 540, gy, 1.7, ease(r / 6))
    if st == 1: P4.tie(c, 540, gy, 1.7, 1.0, dx=lerp(0, 420, ease((r - 20) / 8)), dy=lerp(0, -500, ease((r - 20) / 8)), rot=(r - 20) * .35)
    banner2(c, 540, 1350, 760, 250, ['pro', 'cat', 'v1'][st])
    for x in (170, 910): ell(c, x, 1370, 40, 40); fs(c, WHITE, 7)
    line = [['MORE PROFESSIONAL.'], ['LESS PROFESSIONAL.'], None][st]
    if line: R.bubble(c, line, pop(r, 20 * st + 2), (-40, 700), cy=520, cx=420, size=56)
def sh03(c, f, r):                                             # the wide: whose party, who's here
    S.room(c, f, tv_at=(60, 1180))
    S.cabinet(c, 760, 1060, 1480); S.cat_bed(c, 900, 1455, .75)
    A.myai(c, 560, 1800, .8, eye='blank', droop=1.0, arms=('down', 'down'))
    S.hoody(c, f, 230, 1900, s=.95, slip=.15)
    dog(c, 400, 1900, 1.0, f=f)
    ex = lerp(1200, 820, ease(r / 14))
    E.eva(c, ex, 1960, .95, expr='evaproud' if False else 'charmed', walk=r * .5 if r < 14 else None, **S.EVA_IN)
    S.cake(c, ex + 20, 1960 - 690 * .95 + 286 * .95, 1.0)
    if r >= 14: R.bubble(c, ['TA-DA!'], pop(r, 14), (ex - 20, 1250), cy=1020, cx=760, size=64)
def eva_cake_at(c, head, s, expr):
    x, y = head; gy = y + 690 * s; S.eva_cake(c, x, gy, s, expr=expr); B.cake_heart(c, x, gy, s)
def sh04(c, f, r):
    N.wall(c); eva_cake_at(c, (540, 700), 2.1, 'evaproud')
def sh05(c, f, r):
    N.wall(c)
    hands, _ = S.hoody(c, f, 540, 880 + 626 * 1.7, s=1.7, expr='happy', arms=('chin', 'take'), slip=lerp(.15, .3, ease(r / 20)))
    limb(c, [(hands[0][0] + 10, hands[0][1] - 6), (hands[0][0] + 70, hands[0][1] - 100)], 14, hx('c0c4cc'))
    ell(c, hands[0][0] + 78, hands[0][1] - 112, 30, 22); fs(c, hx('f7c6d9'), 5)
    R.bubble(c, ['MMM!'], pop(r, 4), (720, 760), cy=560, cx=840, size=70)
def sh06(c, f, r):
    N.wall(c); eva_cake_at(c, (540, 700), 2.1, 'evaproud')
    k = ease(r / 12); hx_, hy_ = 540 + 24 * 2.1 + 20 * 2.1, 700 + 286 * 2.1 + 10 * 2.1
    B.finger(c, (lerp(hx_ - 500, hx_, k), lerp(hy_ + 700, hy_, k)), 1.0)
    R.bubble(c, ['COULD YOU JUST', 'MAKE IT BETTER?'], pop(r, 8), (60, 1500), cy=1660, cx=640, size=54)
def sh07(c, f, r):
    N.wall(c)
    expr = 'evaproud' if r < 8 else 'evafrozen' if r < 16 else 'evahurt'
    N.eva_at(c, (540, 860), 2.6, expr=expr)
    S.cake(c, 540, 1640, 3.0, sag=ease((r - 10) / 10)); B.heart(c, 600, 1560, 3.0)
def sh08(c, f, r):                                             # cat level: the cushion, adjusted
    N.wall(c, garland=False)
    rr(c, -40, 1330, 1160, 700, 10); fs(c, hx('a8794f'), 8)                                   # the cabinet top, close
    dx = -40 * ease((r - 14) / 6)
    S.cat_bed(c, 560 + dx, 1290, 2.0)
    hy = lerp(400, 1150, ease(r / 12)) - (0 if r < 24 else 900 * ease((r - 24) / 10))
    limb(c, [(1180, hy - 700), (1000, hy - 260), (820 + dx, hy - 10)], 130, NAVY); ell(c, 820 + dx, hy + 10, 70, 56); fs(c, SKIN, 7)
    if r >= 10: R.bubble(c, ['BETTER!'], pop(r, 10), (1060, 300), cy=560, cx=640, size=74)
def sh09(c, f, r):
    N.wall(c, garland=False); rr(c, -40, 1330, 1160, 700, 10); fs(c, hx('a8794f'), 8)
    c.save(); c.translate(540, 1000); c.scale(5.5, 5.5); c.translate(-(560 - 40 - 10 - 52), -(1290 - 50)); S.cat_bed(c, 520, 1290, 1.0, eye=r >= 8); c.restore()
def sh10(c, f, r):                                             # her eyeline: the hat, down to the odd socks
    N.wall(c)
    dy = lerp(380, -560, ease(r / 18))
    c.save(); c.translate(0, dy); S.hoody(c, f, 520, 1960, s=1.5, slip=.4, thumb=True); c.restore()
    ell(c, 1010, 1820, 300, 260); fs(c, S.E.HAIR_E if hasattr(S.E, 'HAIR_E') else hx('3b2416'), 7)     # her curls, foreground right
    for i in range(6): ell(c, 820 + i * 50, 1600 + abs(i - 2.5) * 30, 50, 46); fs(c, hx('3b2416'), 5)
    rr(c, 760, 1860, 500, 200, 60); fs(c, hx('ffcf2e'), 7)
def sh11(c, f, r):
    N.wall(c); S.tv(c, 470, 640, w=200, h=130, f=f)
    look_ai = (20, -2) if r >= 6 else (0, 6)
    N.ai_at(c, (290, 980), 1.75, eye='open' if r >= 6 else 'blank', look=look_ai, droop=.6, arms=('down', 'down'))
    N.eva_at(c, (790, 930), 2.0, expr='notices', gaze=-20 if r >= 2 else 0)
    N.sofa_fg(c, 1330)
def sh12(c, f, r):                                             # the echo: the cat recruits the dog with one eye
    N.wall(c, garland=False)
    rr(c, 600, 1060, 600, 1100, 10); fs(c, hx('a8794f'), 8)                                   # the cabinet, the cat on top, eye level with the dog
    S.cat_bed(c, 880, 1030, 2.0, eye=True)
    dog(c, 300, 1900, 4.2, f=f, wag=r < 18, face=1, look=1 if r < 18 else 0)
def four(c, f, fl, eva='evacalm', card_dog='NO.'):
    """The union, composed: MY AI, Eva, the dog and the cat behind the sofa back, signs in front."""
    N.wall(c)
    N.ai_at(c, (190, 880), 1.15, eye='focus', arms=('down', 'down'))
    N.eva_at(c, (470, 760), 1.35, expr=eva)
    N.sofa_fg(c, 1230)
    dog(c, 760, 1240, 1.6, f=0, wag=False)
    K.cat(c, 965, 1236, .8, pose='walk', phase=0, look=-1)
    signs = [((470, 1080, 300, 190, 'box'), 'NO.', 104), ((190, 1200, 300, 170, 'banner'), 'NO.', 96),
             ((700, 1150, 180, 116, 'box'), 'NO.', 70), ((950, 1330, 170, 104, 'box'), 'no.', 62)]
    for ((x, y, w, h, kind), word, size), v in zip(signs, fl):
        c.save(); c.translate(x, y); c.scale(max(.04, abs(v)), 1); c.translate(-x, -y)
        (S.card_back(c, x, y, w, h, kind) if v > 0 else S.card_front(c, x, y, w, h, word, size, kind)); c.restore()
def sh13(c, f, r): four(c, f, (1, 1, 1, 1))
def sh14(c, f, r):
    c.save(); c.translate(540, 1000); c.scale(.9, .9); c.translate(-540, -1000); four(c, f, (1, 1, 1, 1)); c.restore()
    B.hoody_back(c, 170, 1720, 2.0)
    R.bubble(c, ['LOVE THE ENERGY!', 'MAKE IT BETTER?'], pop(r, 4), (240, 1380), cy=560, cx=480, size=56)
def flipv(r, at, d=6): return 1 - 2 * ease((r - at) / d)
def sh15(c, f, r): four(c, f, (flipv(r, 16, 4), flipv(r, 10), flipv(r, 22, 4), flipv(r, 44, 8)), eva='amused' if r >= 10 else 'evacalm')
def sh16(c, f, r):
    N.wall(c)
    c.save(); c.translate(540, 1080); c.rotate(.17 * ease(r / 8)); c.translate(-540, -1080)
    expr = 'happy' if r < 14 else 'calm' if r < 30 else 'designer'
    S.hoody(c, f, 540, 900 + 626 * 1.9, s=1.9, expr=expr, thumb=r < 30, slip=.8 if r < 30 else lerp(.8, 1.0, ease((r - 30) / 4)))
    c.restore()
    if r >= 32: R.bubble(c, ['BIGGER?'], pop(r, 32), (520, 1240), cy=1640, cx=600, size=84)
def sh17(c, f, r):                                             # the dog's tail twitches up; the cat's paw lands on it
    N.wall(c, garland=False); rr(c, -40, 1500, 1160, 600, 0); fs(c, S.SOFA, 8)
    twitch = r >= 4 and r < 12
    dog(c, 300, 1560, 3.6, f=8 if twitch else 2.6, wag=True)
    k = ease((r - 10) / 6); px, py = lerp(1240, 700, k), lerp(900, 1290, k)
    limb(c, [(1300, py - 60), (px + 90, py - 20), (px, py)], 70, hx('f2a03c'))                     # the cat's paw, from the right
    ell(c, px, py, 52, 40); fs(c, hx('f2a03c'), 6)
    for k_ in (-1, 0, 1): ell(c, px - 30, py + k_ * 16, 7, 7); c.set_source_rgb(*hx('d9733a')); c.fill()
def sh18(c, f, r):
    four(c, f, (-1, -1, -1, -1), eva='amused')
    k = ease(r / 6); shk = math.sin(r * 2.3) * 10 * max(0, 1 - (r - 6) / 8) if r >= 6 else 0
    c.rectangle(0, 0, W, H); c.set_source_rgba(0, 0, 0, .25 * k); c.fill()
    c.save(); c.translate(540 + shk, 1000); c.rotate(-.06); c.scale(lerp(.35, 1, k), lerp(.35, 1, k))
    rr(c, -520, -330, 1040, 600, 20); fs(c, CREAM, 12); txt(c, 'NO.', 0, -20, 330, RED, lw=0); c.restore()
    if k > .9:
        for x in (90, 990): ell(c, x + shk, 1240, 80, 70); fs(c, WHITE, 8)

SHOTS = [(48, sh01), (18, sh01b), (60, sh02), (36, sh03), (30, sh04), (24, sh05), (36, sh06), (36, sh07), (36, sh08), (21, sh09),
         (24, sh10), (48, sh11), (36, sh12), (45, sh13), (51, sh14), (66, sh15), (63, sh16), (24, sh17), (48, sh18)]
T0 = np.cumsum([0] + [d for d, _ in SHOTS]); NF = int(T0[-1])
def frame(f):
    i = int(np.searchsorted(T0, f, side='right') - 1); d, fn = SHOTS[i]; r = f - T0[i]
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    c.save(); k = 1 + .025 * r / d; c.translate(540, 1000); c.scale(k, k); c.translate(-540, -1000); fn(c, f, r); c.restore()
    flipped = i > 15 or (i == 15 and r >= 10)
    Sh.topbar(c, 'ITS UNION' if flipped else 'HER BIRTHDAY')
    return s

# ---------------- sound ----------------
SR = 48000
def audio(out='rough2.wav'):
    n = int(NF / FPS * SR); mix = np.zeros(n, np.float32)
    def add(x, t, g=1.0):
        i = int(t * SR); j = min(n, i + len(x)); mix[i:j] += x[:j - i] * g
    at = lambda i, sec=0.: T0[i] / FPS + sec
    vo = R1.load
    for nm, t in (('h_first', at(0, .1)), ('h_more', at(2, .1)), ('h_less', at(2, .77)), ('e_tada', at(3, .5)), ('h_mmm', at(5, .05)),
                  ('h_ask', at(6, .3)), ('h_better', at(8, .35)), ('h_energy', at(14, .15)), ('h_bigger', at(16, 1.07))):
        add(vo(nm), t)
    for t in (at(2, .05), at(2, .72)): add(R1.tone(1700, .15, 18), t, .25)              # the version dings
    add(R1.tone(1200, .12, 30, 2200), at(3, .45), .3)
    add(R1.noise(.25, 14, .2) * 1.5, at(8, .45), .5)
    for k in range(8): add(R1.noise(.06, 40, .3) * 2, at(12, .1 + k * .07), .3 * (1 - k / 8))   # the wag's thumps, slowing out
    for t, g in ((at(15, 10 / 30), .9), (at(15, 16 / 30), .9), (at(15, 22 / 30), .7), (at(15, 44 / 30), .45)): add(R1.noise(.12, 30, .5) * 3, t, g)
    add(R1.noise(.08, 30, .4) * 2, at(17, .4), .4)
    add(R1.noise(.35, 9, .15) * 3 + R1.tone(70, .35, 9), at(18, .2), .9)
    room = np.random.default_rng(3).standard_normal(n).astype(np.float32)
    for _ in range(4): room = np.convolve(room, np.ones(40) / 40, 'same')
    mix += room * .02
    sf.write(os.path.join(HERE, out), np.stack([mix, mix], 1), SR)

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'sheet'
    if mode == 'audio': audio(); print('audio', NF / FPS)
    elif mode == 'sheet':
        k = .22; sw, sh = int(W * k), int(H * k); cols = 10
        out = cairo.ImageSurface(cairo.FORMAT_ARGB32, cols * sw, 2 * sh); c = cairo.Context(out)
        for i in range(len(SHOTS)):
            s = frame(int(T0[i] + SHOTS[i][0] * .7)); c.save(); c.translate((i % cols) * sw, (i // cols) * sh); c.scale(k, k); c.set_source_surface(s); c.paint(); c.restore()
        out.write_to_png(os.path.join(HERE, 'rough2_sheet.png')); print('sheet', NF)
    else:
        p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                              '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', os.path.join(HERE, 'video.mp4')], stdin=subprocess.PIPE)
        for f in range(NF): p.stdin.write(bytes(frame(f).get_data()))
        p.stdin.close(); assert p.wait() == 0; print('video', NF)
