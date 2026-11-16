"""Make It Better v5.2: the rough (an animatic with the key motions) - 21 s, 630 frames, placeholder voices.
Timing follows the shot list in the concept doc. Usage: python3 rough.py  ->  rough.mp4 (video) ; python3 rough.py audio"""
import os, sys, math, subprocess, cairo
import numpy as np, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sb as B, kp as S
from kp import R, K, Sh, A, E, P4, INK, WHITE, NAVY, CREAM, RED, rr, fs, ell, txt, hx, lerp, W, H
FPS = 30
def ease(t): t = max(0., min(1., t)); return t * t * (3 - 2 * t)

def union_flip(c, f, fl, look_eva='evacalm'):
    """The sofa with each sign's turn: fl = (eva, my ai, cat), 1 = blank back to us, -1 = NO facing us."""
    S.room(c, f, tv_at=(60, 1150))
    E.eva(c, 790, 1760, .95, expr=look_eva, **S.EVA_IN)
    S.sofa_back(c); S.sofa_front(c)
    A.myai(c, 560, 1520, .85, eye='focus', arms=('offer', 'offer'))
    K.cat(c, 975, 1440, .5, pose='walk', phase=0, look=-1)
    signs = [((790, 1330, 220, 140, 'box'), 'NO.', 72), ((560, 1405, 270, 120, 'banner'), 'NO.', 70), ((905, 1450, 86, 58, 'box'), 'no.', 30)]
    for ((x, y, w, h, kind), word, size), v in zip(signs, fl):
        c.save(); c.translate(x, y); c.scale(max(.04, abs(v)), 1); c.translate(-x, -y)
        (S.card_back(c, x, y, w, h, kind) if v > 0 else S.card_front(c, x, y, w, h, word, size, kind)); c.restore()

def flipv(r, at, d=6): return 1 - 2 * ease((r - at) / d)

# each shot: (frames, draw(c, f, r), pill)
def st(fn): return lambda c, f, r: fn(c, f)
def s05(c, f, r):
    S.room(c, f, tv_at=None)
    c.save(); B.shot(c, 610, 1300, 2.0); B.eva_cake(c, expr='evaproud')
    k = ease(r / 12); B.finger(c, (lerp(330, 628, k), lerp(1714, 1214, k)), .5); c.restore()
    if r >= 6: R.bubble(c, ['COULD YOU JUST', 'MAKE IT BETTER?'], r - 6, (150, 1960), cy=1700, cx=600, size=56)
def s06(c, f, r):
    S.room(c, f, tv_at=None)
    expr = 'evaproud' if r < 8 else 'evafrozen' if r < 16 else 'evahurt'
    c.save(); B.shot(c, 600, 1180, 3.0); B.eva_cake(c, expr=expr); c.restore()
def s07(c, f, r):
    S.room(c, f, tv_at=None)
    c.save(); B.shot(c, 760, 1400, 2.4); S.cabinet(c, 470, 1040, 1440)
    dx = -14 * ease((r - 14) / 6); S.cat_bed(c, 770 + dx, 1410, 1.0)
    hy = lerp(1000, 1372, ease(r / 12)) - (0 if r < 22 else 300 * ease((r - 22) / 10))
    S.limb(c, [(980, 700), (930, hy - 190), (900 + dx, hy - 12)], 60, NAVY); ell(c, 900 + dx, hy, 34, 28); fs(c, S.SKIN, 6)
    c.restore()
    if r >= 10: R.bubble(c, ['BETTER!'], r - 10, (980, 300), cy=560, cx=640, size=70)
def s08(c, f, r):
    S.room(c, f, tv_at=None)
    c.save(); B.shot(c, 700, 1370, 6.0); S.cabinet(c, 470, 1040, 1440); S.cat_bed(c, 770 - 14, 1410, 1.0, eye=r >= 8); c.restore()
def s14(c, f, r):
    c.save(); B.shot(c, 660, 1430, 1.55)
    union_flip(c, f, (flipv(r, 10), flipv(r, 17, 4), flipv(r, 36, 8)), 'amused' if r >= 10 else 'evacalm'); c.restore()
def s15(c, f, r):
    S.room(c, f)
    c.save(); B.shot(c, 330, 1420, 2.3, rot=.18 * ease(r / 8))
    S.hoody(c, f, 300, 1900, expr='happy', thumb=True, slip=.8 if r < 30 else lerp(.8, 1.0, ease((r - 30) / 4))); c.restore()
    if r >= 30: R.bubble(c, ['BIGGER?'], r - 30, (560, 1380), cy=1700, cx=640, size=80)
def s16(c, f, r):
    c.save(); B.shot(c, 660, 1430, 1.55); union_flip(c, f, (-1, -1, -1), 'amused'); c.restore()
    k = ease(r / 6); sh = (1 - k) * 0 + (math.sin(r * 2.3) * 10 * max(0, 1 - (r - 6) / 8) if r >= 6 else 0)
    c.rectangle(0, 0, W, H); c.set_source_rgba(0, 0, 0, .25 * k); c.fill()
    c.save(); c.translate(540 + sh, 1060); c.rotate(-.06); c.scale(lerp(.35, 1, k), lerp(.35, 1, k))
    rr(c, -520, -330, 1040, 600, 20); fs(c, CREAM, 12); txt(c, 'NO.', 0, -20, 330, RED, lw=0); c.restore()
    if k > .9:
        for x in (90, 990): ell(c, x + sh, 1300, 80, 70); fs(c, WHITE, 8)
        S.card_front(c, 760, 1560, 200, 130, 'no.', 70, 'box')

SHOTS = [(54, st(B.s01), 'HIS PARTY'), (24, st(B.s02), 'HIS PARTY'), (36, st(B.s03), 'HIS PARTY'), (24, st(B.s04), 'HIS PARTY'),
         (36, s05, 'HIS PARTY'), (36, s06, 'HIS PARTY'), (36, s07, 'HIS PARTY'), (21, s08, 'HIS PARTY'), (24, st(B.s09), 'HIS PARTY'),
         (24, st(B.s10a), 'HIS PARTY'), (24, st(B.s10), 'HIS PARTY'), (21, st(B.s11), 'HIS PARTY'), (48, st(B.s12), 'HIS PARTY'),
         (51, st(B.s13), 'HIS PARTY'), (60, s14, None), (60, s15, 'ITS UNION'), (51, s16, 'ITS UNION')]
T0 = np.cumsum([0] + [d for d, _, _ in SHOTS]); NF = int(T0[-1])

def frame(f):
    i = int(np.searchsorted(T0, f, side='right') - 1); d, fn, pill = SHOTS[i]; r = f - T0[i]
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    c.save(); k = 1 + .035 * r / d; c.translate(540, 1060); c.scale(k, k); c.translate(-540, -1060)   # a slow push on every shot
    fn(c, f, r); c.restore()
    Sh.topbar(c, pill or ('ITS UNION' if r >= 10 else 'HIS PARTY'))                                 # the label flips with Eva's sign
    return s

# ---------------- sound ----------------
SR = 48000
def load(n):
    a, sr = sf.read(os.path.join(HERE, 'vo', n + '.wav'), dtype='float32')
    if a.ndim > 1: a = a.mean(1)
    if sr != SR: a = np.interp(np.arange(int(len(a) * SR / sr)) * sr / SR, np.arange(len(a)), a).astype(np.float32)
    return a / (np.abs(a).max() + 1e-9) * .7
def tone(f0, d, dec=8, f1=None):
    t = np.arange(int(d * SR)) / SR; fr = f0 if f1 is None else np.linspace(f0, f1, len(t))
    return (np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * dec)).astype(np.float32)
def noise(d, dec, lp=.3):
    rng = np.random.default_rng(int(d * 1000)); x = rng.standard_normal(int(d * SR)).astype(np.float32)
    for _ in range(3): x = np.convolve(x, np.ones(int(1 / lp)) / int(1 / lp), 'same')
    return x * np.exp(-np.arange(len(x)) / SR * dec)
def at(shot, sec=0.0): return T0[shot] / FPS + sec
def audio(out='rough.wav'):
    n = int(NF / FPS * SR); mix = np.zeros(n, np.float32)
    def add(x, t, g=1.0):
        i = int(t * SR); j = min(n, i + len(x)); mix[i:j] += x[:j - i] * g
    VO = [('h_first', at(0, .15)), ('e_tada', at(2, .2)), ('h_mmm', at(3, .05)), ('h_ask', at(4, .2)), ('h_better', at(6, .35)),
          ('h_energy', at(13, .2)), ('h_bigger', at(15, 1.0))]
    for nm, t in VO: add(load(nm), t)
    add(tone(1200, .12, 30, 2200), at(1, .05), .35)                                      # the pop of his approval
    add(noise(.25, 14, .2) * 1.5, at(6, .45), .5)                                       # the cushion squeak
    for t, g in ((at(14, 10 / 30), .9), (at(14, 17 / 30), .9), (at(14, 36 / 30), .45)): add(noise(.12, 30, .5) * 3, t, g)   # cardboard flips
    add(noise(.35, 9, .15) * 3 + tone(70, .35, 9), at(16, .2), .9)                      # the sign impact
    room = np.random.default_rng(3).standard_normal(n).astype(np.float32)
    for _ in range(4): room = np.convolve(room, np.ones(40) / 40, 'same')
    mix += room * .02
    sf.write(os.path.join(HERE, out), np.stack([mix, mix], 1), SR)

if __name__ == '__main__':
    if sys.argv[1:] == ['audio']: audio(); print('audio', NF / FPS); sys.exit()
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', os.path.join(HERE, 'video.mp4')], stdin=subprocess.PIPE)
    for f in range(NF): p.stdin.write(bytes(frame(f).get_data()))
    p.stdin.close(); assert p.wait() == 0; print('video', NF)
