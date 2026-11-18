"""Make It Better v5.4: rough 3. 20 shots, about 27 s, built from the gates (shot list v5.4 in the concept doc):
the want said aloud, the ladder building to Eva (banner -> cat bed -> cake), every turn an action (a synced nod and a
card; the cat paws a NO card to the dog), takes on the reactions, push-ins only on the three turns, a symmetric
union with bigger signs, and his thumbs-up popping back over the NO as the last image.
Usage: python3 rough3.py sheet | g3 | grid | video | audio"""
import os, sys, math, subprocess, cairo
import numpy as np, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import kp as S, sb as B, shots2 as N, rough as R1, rough2 as R2
from kp import R, K, Sh, A, E, P4, INK, WHITE, NAVY, YEL, SKIN, CREAM, RED, rr, fs, ell, limb, txt, hx, lerp, W, H
FPS = 30
ease, pop, dog, flipv = R2.ease, R2.pop, R2.dog, R2.flipv
SWEATER = E.COAT
def back(t, s=1.70158):                                         # overshoot ease for pops (clamped, never 0 scale)
    t = max(0., min(1., t)); t -= 1; return max(.02, t * t * ((s + 1) * t + s) + 1)

# ---------------- new and changed shots ----------------
def sh02b(c, f, r):                                             # insert: the antenna droops to the bottom and dims
    N.wall(c, garland=False)
    d = lerp(.6, 1.0, ease((r - 3) / 12))
    c.save(); c.translate(440, 1440); c.scale(5.0, 5.0); A.myai(c, 0, 280, 1.0, eye='blank', droop=d, arms=('down', 'down')); c.restore()
    if r > 12: c.rectangle(0, 0, W, H); c.set_source_rgba(0, 0, 0, .12 * ease((r - 12) / 6)); c.fill()

def sh03(c, f, r):                                              # the wide: his party for her; he says what he wants
    S.room(c, f, tv_at=(60, 1180))
    S.cabinet(c, 760, 1060, 1480); S.cat_bed(c, 900, 1455, .75)
    A.myai(c, 600, 1780, .8, eye='blank', droop=1.0, arms=('down', 'down'))
    S.banner(c, 600, 1560, 300, 96, 'v1', text='HAPPY B-DAY EVA')
    arms = ('rest', 'rest') if r < 6 else ('up', 'up')
    S.hoody(c, f, 290, 1900, s=1.0, arms=arms, thumb=False, slip=.15)
    dog(c, 470, 1910, 1.0, f=f)
    if r >= 8: R.bubble(c, ['BEST BIRTHDAY', 'EVER!'], pop(r, 8), (300, 1170), cy=560, cx=420, size=60)

def sh04(c, f, r):                                              # cat level: he squares the bed; the cat slides out onto the floor
    N.wall(c, garland=False)
    rr(c, -40, 1330, 1160, 700, 10); fs(c, hx('a8794f'), 8)
    rot = -.22 * ease((r - 10) / 6)                              # the bed tips as he squares it
    hy = lerp(400, 1150, ease(r / 10)) - (0 if r < 22 else 900 * ease((r - 22) / 10))
    c.save(); c.translate(560, 1290); c.rotate(rot); c.translate(-560, -1290)
    ell(c, 560, 1290, 380, 112); fs(c, hx('d1495b'), 7); ell(c, 560, 1270, 300, 72); fs(c, hx('f2a3ae'), 5); c.restore()
    k = ease((r - 12) / 10)                                     # the cat slides out, still asleep, over the edge
    cx_, cy_ = lerp(540, 980, k), lerp(1306, 1320, k) + 260 * ease((r - 20) / 6)
    K.cat(c, cx_, cy_, 1.6, pose='sleep')
    limb(c, [(1180, hy - 700), (1000, hy - 260), (820, hy - 10)], 130, NAVY); ell(c, 820, hy + 10, 70, 56); fs(c, SKIN, 7)
    if r >= 14: R.bubble(c, ['BETTER!'], pop(r, 14), (1060, 300), cy=560, cx=600, size=74)

def sh05(c, f, r):                                              # on the floor: one eye opens, to him
    N.wall(c, garland=False); rr(c, -40, 1400, 1160, 700, 0); fs(c, hx('c79a6a'), 8)
    c.save(); c.translate(540, 1100); c.scale(4.0, 4.0); c.translate(-520, -1290)
    K.cat(c, 510, 1298, .8, pose='sleep')
    if r >= 6:
        ex, ey = 510 - 92 * .8 + 22 * .8, 1298 - 52 * .8 - 6
        k = ease((r - 6) / 4); ell(c, ex, ey, 12, 13 * k + .5); fs(c, hx('b8e04a'), 2); ell(c, ex + 2, ey, 4, 10 * k + .3); c.set_source_rgb(*INK); c.fill()
    c.restore()

def sh06(c, f, r):                                              # medium: Eva comes in with her cake
    N.wall(c)
    rr(c, 640, 360, 420, 1700, 6); fs(c, hx('f3e2c4'), 7)                                    # the kitchen door frame
    x = lerp(1180, 600, ease(r / 14))
    S.eva_cake(c, x, 760 + 690 * 1.6, 1.6, expr='evaproud'); B.cake_heart(c, x, 760 + 690 * 1.6, 1.6)
    if r >= 14: R.bubble(c, ['TA-DA!'], pop(r, 14), (x - 60, 620), cy=430, cx=300, size=70)

def sh10(c, f, r):                                              # turn 1, a take: the smile freezes, dies; sleeves over her hands
    N.wall(c)
    expr = 'evaproud' if r < 6 else 'evafrozen' if r < 16 else 'evahurt'
    sq = 1 + (.03 if 4 <= r < 7 else 0) - (.02 if 7 <= r < 9 else 0)                     # anticipation, the accent, the settle
    c.save(); c.translate(540, 860); c.scale(1, sq); c.translate(-540, -860)
    N.eva_at(c, (540, 860), 2.6, expr=expr, gaze=0 if r < 10 else 0)
    c.restore()
    k = ease((r - 20) / 10)                                      # her hands come up to her chin, sleeves over the fingers
    for q in (-1, 1):                                           # drawn before the cake, so the cake hides the arms
        hx_, hy_ = 540 + q * 60, lerp(2150, 1300, k)
        limb(c, [(540 + q * 200, 2250), (hx_ + q * 40, hy_ + 220), (hx_, hy_)], 96, SWEATER); ell(c, hx_, hy_, 62, 54); fs(c, SWEATER, 7)
    S.cake(c, 540, 1660, 3.0, sag=ease((r - 12) / 10)); B.heart(c, 600, 1580, 3.0)

def sh12(c, f, r):                                              # turn 2: they look, nod once in sync, MY AI hands her a blank card
    N.wall(c); S.tv(c, 470, 640, w=200, h=130, f=f)
    nod = 30 * math.sin(math.pi * max(0, min(1, (r - 10) / 10)))
    k = ease((r - 24) / 12)
    c.save(); c.translate(0, nod)
    N.ai_at(c, (290, 980), 1.75, eye='open' if r >= 4 else 'blank', look=(20, -2) if r >= 4 else (0, 6), droop=.6, arms=('down', 'down'))
    c.restore()
    c.save(); c.translate(0, nod)
    N.eva_at(c, (790, 930), 2.0, expr='notices' if r < 20 else 'amused', gaze=-20)
    c.restore()
    N.sofa_fg(c, 1330)
    cx_, cy_ = lerp(380, 640, k), lerp(1300, 1210, k)           # the card, from its mitt to her hand
    S.card_back(c, cx_, cy_, 230, 150); ell(c, cx_ - 110, cy_ + 20, 40, 40); fs(c, WHITE, 7)
    if k > .9: ell(c, 760, 1230, 56, 48); fs(c, SWEATER, 7)

def sh13(c, f, r):                                              # the echo: the cat paws a NO card to the dog; the dog takes it
    N.wall(c, garland=False); rr(c, -40, 1500, 1160, 600, 0); fs(c, hx('c79a6a'), 8)
    K.cat(c, 860, 1560, 1.4, pose='walk', phase=0, look=-1)
    k = ease((r - 6) / 14)
    held = r >= 24
    if not held:
        px, py = lerp(700, 470, k), 1520                          # the card slides across the floor under its paw
        S.card_front(c, px, py, 200, 130, 'NO.', 84)
        ell(c, px + 90, py - 40, 34, 28); fs(c, hx('f2a03c'), 6)
    dog(c, 260, 1560, 3.0, f=f, wag=r < 24, face=1, look=1 if not held else 0, card='NO.' if held else None)

def four3(c, f, fl, eva='evacalm'):
    """The union, symmetric: Eva in the middle, MY AI left, the dog right, the cat front and centre; bigger signs."""
    N.wall(c)
    N.ai_at(c, (200, 880), 1.15, eye='focus', arms=('down', 'down'))
    N.eva_at(c, (540, 760), 1.35, expr=eva)
    N.sofa_fg(c, 1230)
    dog(c, 900, 1240, 1.6, f=0, wag=False, face=-1)
    K.cat(c, 560, 1520, .9, pose='walk', phase=0, look=-1)
    signs = [((540, 1080, 320, 200, 'box'), 'NO.', 116), ((200, 1200, 300, 180, 'banner'), 'NO.', 104),
             ((880, 1180, 260, 160, 'box'), 'NO.', 100), ((560, 1650, 240, 140, 'box'), 'no.', 90)]
    for ((x, y, w, h, kind), word, size), v in zip(signs, fl):
        c.save(); c.translate(x, y); c.scale(max(.04, abs(v)), 1); c.translate(-x, -y)
        (S.card_back(c, x, y, w, h, kind) if v > 0 else S.card_front(c, x, y, w, h, word, size, kind)); c.restore()

def sh14(c, f, r): four3(c, f, (1, 1, 1, 1))
def sh15(c, f, r):
    c.save(); c.translate(540, 1000); c.scale(.9, .9); c.translate(-540, -1000); four3(c, f, (1, 1, 1, 1)); c.restore()
    B.hoody_back(c, 170, 1720, 2.0)
    R.bubble(c, ['LOVE THE ENERGY!', 'MAKE IT BETTER?'], pop(r, 4), (240, 1380), cy=560, cx=480, size=56)
def sh16(c, f, r):                                              # order: Eva, MY AI, the dog, a beat, the cat
    four3(c, f, (flipv(r, 16, 4), flipv(r, 10), flipv(r, 22, 4), flipv(r, 44, 8)), eva='amused' if r >= 10 else 'evacalm')

def sh17(c, f, r):                                              # the sting, a take with a double take, then "Bigger?"
    N.wall(c)
    c.save(); c.translate(540, 1080); c.rotate(.17 * ease(r / 8)); c.translate(-540, -1080)
    if r < 10: expr, gaze = 'happy', 0
    elif r < 13: expr, gaze = 'shock', 0                         # accent
    elif r < 20: expr, gaze = 'calm', 24                         # eyes to the signs
    elif r < 26: expr, gaze = 'happy', 0                         # back: it's fine
    elif r < 30: expr, gaze = 'shock', 30                        # the double take
    else: expr, gaze = 'designer', 24                            # studying them: how to improve a NO
    jolt = -26 if 26 <= r < 29 else 0
    sq = 1.04 if 10 <= r < 12 else .97 if r == 9 else 1.0
    c.translate(0, jolt); c.translate(540, 1500); c.scale(1, sq); c.translate(-540, -1500)
    S.hoody(c, f, 540, 900 + 626 * 1.9, s=1.9, expr=expr, gaze=gaze, thumb=r < 10, slip=.8 if r < 30 else lerp(.8, 1.0, ease((r - 30) / 4)))
    c.restore()
    if r >= 44: R.bubble(c, ['BIGGER?'], pop(r, 44), (520, 1240), cy=1640, cx=600, size=84)

def sh18(c, f, r):                                              # the NO into the lens; a beat; his thumbs-up pops back over it
    R2.sh18(c, f, r)
    if r >= 20:
        k = back((r - 20) / 8)
        y = lerp(2300, 1240, min(1, (r - 20) / 8))
        limb(c, [(880, 2300), (840, y + 260), (820, y + 60)], 130, NAVY)
        c.save(); c.translate(820, y); c.scale(k, k); P4.thumbs_up(c, 0, 0, 3.2); c.restore()

SHOTS = [(48, R2.sh01), (18, R2.sh01b), (60, R2.sh02), (21, sh02b), (48, sh03), (45, sh04), (21, sh05), (36, sh06),
         (24, R2.sh04), (36, R2.sh05), (36, R2.sh06), (45, sh10), (21, R2.sh10), (51, sh12), (45, sh13),
         (30, sh14), (45, sh15), (66, sh16), (69, sh17), (54, sh18)]
NAMES = ['01', '01b', '02', '02b', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18']
PUSH = {11: 1.15, 13: 1.12, 17: 1.10}                           # push-ins only on the turns: her face, the nod, the flips
FLIP = 17
T0 = np.cumsum([0] + [d for d, _ in SHOTS]); NF = int(T0[-1])
def shot_of(f): i = int(np.searchsorted(T0, f, side='right') - 1); return i, f - T0[i]
def frame(f):
    i, r = shot_of(f); d, fn = SHOTS[i]
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    k = 1 + (PUSH.get(i, 1) - 1) * ease(r / (d * .6))
    c.save(); c.translate(540, 1000); c.scale(k, k); c.translate(-540, -1000); fn(c, f, r); c.restore()
    flipped = i > FLIP or (i == FLIP and r >= 10)
    if i == FLIP and 10 <= r < 26:                               # the label switch pops big, then settles
        Sh.topbar(c, 'ITS UNION'); kk = back((r - 10) / 6) * (1.6 - .6 * ease((r - 18) / 8))
        c.save(); c.translate(540, 1000); c.scale(kk, kk); rr(c, -330, -70, 660, 140, 30); fs(c, NAVY, 8)
        txt(c, 'ITS UNION', 0, 6, 92, YEL, lw=0); c.restore()
    else: Sh.topbar(c, 'ITS UNION' if flipped else 'HER BIRTHDAY')
    return s

# ---------------- sound ----------------
SR = 48000
def audio(out='rough3.wav'):
    n = int(NF / FPS * SR); mix = np.zeros(n, np.float32)
    def add(x, t, g=1.0):
        i = int(t * SR); j = min(n, i + len(x)); mix[i:j] += x[:j - i] * g
    at = lambda i, sec=0.: T0[i] / FPS + sec
    vo = R1.load
    for nm, t in (('h_first', at(0, .1)), ('h_more', at(2, .1)), ('h_less', at(2, .77)), ('h_best', at(4, .27)), ('h_better', at(5, .47)),
                  ('e_tada', at(7, .47)), ('h_mmm', at(9, .05)), ('h_ask', at(10, .3)), ('h_energy', at(16, .15)), ('h_bigger', at(18, 1.47))):
        add(vo(nm), t)
    for t in (at(2, .05), at(2, .72)): add(R1.tone(1700, .15, 18), t, .25)                 # the version dings
    add(R1.tone(520, .6, 4, 180), at(3, .1), .35)                                          # the antenna's descending boop
    add(R1.noise(.25, 14, .2) * 1.5, at(5, .33), .5)                                       # the cushion squeak
    add(R1.noise(.2, 18, .12) * 2 + R1.tone(90, .2, 18), at(5, .85), .5)                   # the soft thud on the floor
    add(R1.noise(.3, 10, .5) * 1.2, at(13, .8), .3)                                        # the card's swish
    add(R1.noise(.4, 8, .5) * 1.0, at(14, .2), .25)                                        # the card sliding across the floor
    for k in range(8): add(R1.noise(.06, 40, .3) * 2, at(14, .1 + k * .1), .3 * (1 - k / 8))   # the wag's thumps, stopping
    for t, g in ((at(17, 10 / 30), .9), (at(17, 16 / 30), .9), (at(17, 22 / 30), .7), (at(17, 44 / 30), .45)): add(R1.noise(.12, 30, .5) * 3, t, g)
    add(R1.noise(.35, 9, .15) * 3 + R1.tone(70, .35, 9), at(19, .2), .9)                   # the NO impact
    add(R1.tone(900, .1, 30, 1800), at(19, 20 / 30), .3)                                   # the thumbs-up pop
    room = np.random.default_rng(3).standard_normal(n).astype(np.float32)
    for _ in range(4): room = np.convolve(room, np.ones(40) / 40, 'same')
    mix += room * .02
    sf.write(os.path.join(HERE, out), mix, SR)                  # mono; master.sh pans and limits

def sheet(path, frames, k=.22, cols=10, label=True):
    sw, sh = int(W * k), int(H * k); rows = (len(frames) + cols - 1) // cols
    out = cairo.ImageSurface(cairo.FORMAT_ARGB32, cols * sw, rows * (sh + (24 if label else 0))); c = cairo.Context(out); c.set_source_rgb(1, 1, 1); c.paint()
    for j, (f, lab) in enumerate(frames):
        x, y = (j % cols) * sw, (j // cols) * (sh + (24 if label else 0))
        s = frame(f); c.save(); c.translate(x, y + (24 if label else 0)); c.scale(k, k); c.set_source_surface(s); c.paint(); c.restore()
        if label: txt(c, lab, x + sw / 2, y + 14, 16, NAVY, lw=0)
    out.write_to_png(path)

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'sheet'
    if mode == 'audio': audio(); print('audio', NF / FPS)
    elif mode == 'sheet':
        sheet(os.path.join(HERE, 'rough3_sheet.png'), [(int(T0[i] + SHOTS[i][0] * .75), NAMES[i]) for i in range(len(SHOTS))]); print('sheet', NF, NF / FPS)
    elif mode == 'g3':                                          # composition check at feed size: 270 px wide
        sheet(os.path.join(HERE, 'rough3_g3_270.png'), [(int(T0[i] + SHOTS[i][0] * .75), NAMES[i]) for i in range(len(SHOTS))], k=.25, cols=5); print('g3')
    elif mode == 'grid':                                        # cold-viewer grids: 4 fps and 8 fps, no captions are stubbed here
        fps = int(sys.argv[2]); step = FPS // fps; os.makedirs(os.path.join(HERE, 'chk'), exist_ok=True)
        fr = list(range(0, NF, step)); per = 60
        for p in range(0, len(fr), per):
            sheet(os.path.join(HERE, 'chk', f'grid{fps}_{p // per:02d}.png'), [(f, f'{f / FPS:.2f}s') for f in fr[p:p + per]], k=.12, cols=10)
        print('grid', fps, len(fr))
    else:
        p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                              '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-color_primaries', 'bt709',
                              '-color_trc', 'bt709', '-colorspace', 'bt709', os.path.join(HERE, 'video3.mp4')], stdin=subprocess.PIPE)
        for f in range(NF): p.stdin.write(bytes(frame(f).get_data()))
        p.stdin.close(); assert p.wait() == 0; print('video', NF)
