"""Says Here v4 mix. v3's voices and sounds on the v4 timeline (film.START), plus the loop: the room tone, the NEW CHAT chime
and the paper rustle of the CV all run through the cut (tails wrap from the end onto the start), so the seam has no jump.
Writes mix.wav (mono, 48 kHz, exactly NF frames long)."""
import os, sys, numpy as np, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from film import START, SHOTS, NF, VO
SR = 48000; N = NF * SR // 30
rng = np.random.default_rng(3)
vo = np.zeros(N); bed = np.zeros(N); fx = np.zeros(N)
T = lambda d: np.arange(int(d * SR)) / SR
t0 = lambda s, fr=0: (START[s] + fr) / 30
DUR = {n: d for n, d, _ in SHOTS}
def add(buf, t, x, g=1.0):                                           # tails wrap over the loop point
    i = int(t * SR) % N; n = len(x); k = min(n, N - i); buf[i:i + k] += x[:k] * g
    if n > k: buf[:n - k] += x[k:n] * g
def load(p):
    x, sr = sf.read(os.path.join(HERE, '..', 'v3', 'vo', p)); assert sr == SR, sr; return x / np.abs(x).max()
def kick(g=1): t = T(.22); return np.sin(2 * np.pi * (48 * t + (110 / 30) * (1 - np.exp(-30 * t)))) * np.exp(-t * 14) * g
def noise(d, dec): t = T(d); return rng.standard_normal(len(t)) * np.exp(-t * dec)
hp = lambda x: np.diff(x, prepend=0)
midi = lambda n: 440 * 2 ** ((n - 69) / 12)
def sq(fr, d, dec=4, duty=.5): t = T(d); return np.where((t * fr) % 1 < duty, 1, -1) * np.exp(-t * dec)
def sweep(a, b, d, dec=0, kind='sine'):
    t = T(d); ph = np.cumsum(np.linspace(a, b, len(t))) / SR * 2 * np.pi
    return (np.sign(np.sin(ph)) if kind == 'sq' else np.sin(ph)) * np.exp(-t * dec)
def lowpass(x, fc):
    a = np.exp(-2 * np.pi * fc / SR); y = np.zeros_like(x); p = 0.
    for i in range(len(x)): p = (1 - a) * x[i] + a * p; y[i] = p
    return y

# ---- voices (v3's takes: HARV = Kokoro bm_george, locked; Hoody = Tomas, 14 Nov)
GAIN = dict(h1=.62, g1=.62, g2=.62, h2=.58, g3=.62, h3=.58)
for n, s, off in VO: add(vo, t0(s, off), load(n + '.wav'), GAIN[n])

# ---- room tone under every 2027 desk and close-up shot; it is the same at the end and at the start, so the loop has no step
room = lowpass(rng.standard_normal(N), 300) * .035
mask = np.ones(N)
a, b = int(t0('a5') * SR), int(t0('a11') * SR); mask[a:b] = 0                       # the flashback has its own bed
a, b = int(t0('a16') * SR), int(t0('a18') * SR); mask[a:b] = .3                     # the silence after the shout stays quiet
bed += room * mask

# ---- bed: the flashback only (a6-a10), 120 bpm
SEC = [(t0('a6'), t0('a7'), 45, [0, 4, 7, 12]), (t0('a7'), t0('a8'), 43, [0, 3, 7, 10]), (t0('a8'), t0('a11'), 41, [0, 4, 7, 11])]
for a, b, root, ar in SEC:
    t = a; k = 0
    while t < b - 1e-6:
        if k % 2 == 0: add(bed, t, kick(), .55)
        if k % 4 == 2: add(bed, t, hp(noise(.14, 24)), .25)
        add(bed, t, hp(hp(noise(.04, 120))), .06)
        add(bed, t, sq(midi(root + (12 if k % 8 in (3, 6) else 0)), .23, 6), .105)
        add(bed, t, sq(midi(root + 24 + ar[k % 4]), .2, 10, .25), .06)
        t += .25; k += 1

# ---- the dark room: TV hum + HARV's podcast, wordless and muffled
d11 = DUR['a11'] / 30
add(bed, t0('a11'), lowpass(sq(60, d11, 0) * .5 + rng.standard_normal(int(d11 * SR)) * .3, 400) * .3, .12)
pod = load('pod.wav'); L = int(.12 * SR); ch = [pod[i:i + L] for i in range(0, len(pod) - L, L)]
order = np.random.default_rng(11).permutation(len(ch)); fade = np.minimum(1, np.minimum(np.arange(L), L - 1 - np.arange(L)) / 240)
pod = np.concatenate([ch[i] * fade for i in order])[:int((d11 - .3) * SR)]
add(bed, t0('a11') + .2, lowpass(lowpass(pod, 500), 500), .45)

# ---- effects
add(fx, t0('a3', 3), sweep(900, 1500, .09), .07)                                         # his eyes flick
add(fx, t0('a4', 4), sweep(2400, 4200, .25, 6), .10)                                     # glint on the shades
add(fx, t0('a4', 10), np.sin(2 * np.pi * 3520 * T(.5)) * np.exp(-T(.5) * 9), .08)        # sparkle ting
r = sweep(1400, 90, DUR['a5'] / 30, 0, 'sq'); add(fx, t0('a5'), r * np.linspace(.4, .9, len(r)), .14)   # rewind
add(fx, t0('a5'), hp(noise(.45, 2)), .15)
add(fx, t0('a9', 9), sweep(500, 2400, .16), .22); add(fx, t0('a9', 14), sweep(2400, 600, .2, 4), .18)   # yoink
add(fx, t0('a12', 8), kick(1.4), .9); add(fx, t0('a12', 8), noise(.18, 22), .3)          # 9.99 stamp
add(fx, t0('a14', 8), sweep(700, 1100, .08), .06)                                        # his hand to the shades
add(fx, t0('a15'), kick(1.8), 1.1); add(fx, t0('a15'), noise(.5, 7), .45)                # the shout hit
b = np.sin(2 * np.pi * 1250 * T(.11)) * np.minimum(1, (.11 - T(.11)) * 60); add(fx, t0('a16', 8), b, .10)   # one tiny beep
tt = T(.25); add(fx, t0('a17', 4), np.sin(2 * np.pi * (520 + 300 * tt) * tt) * np.sin(np.pi * tt / .25) ** 2, .035)   # the cat's eye: a tiny "mrr"
for fr in (12, 25): add(fx, t0('a18', fr), noise(.05, 90) * .6 + np.sin(2 * np.pi * 180 * T(.05)) * np.exp(-T(.05) * 60), .10)   # HARV taps the CV
add(fx, t0('a12', 2), lowpass(noise(.3, 8), 3000), .05)                                   # the letter slides in
# ---- the loop: NEW CHAT. Two soft descending boops, then a rising two-note chime whose tail rings over the cut;
# the CV's paper rustle starts before the cut and ends after it.
for j, (fr, n) in enumerate(((1, 79), (5, 74))):
    tt = T(.12); add(fx, t0('a20', fr), np.sin(2 * np.pi * midi(n) * tt) * np.sin(np.pi * tt / .12), .12)
for j, n in enumerate((76, 83)):
    tt = T(1.1); add(fx, t0('a20', 8 + j * 4), (np.sin(2 * np.pi * midi(n) * tt) + .3 * np.sin(2 * np.pi * midi(n + 12) * tt)) * np.exp(-tt * 3.2) * np.minimum(1, tt * 200), .16)
tt = T(.7); rus = (rng.standard_normal(len(tt)) - lowpass(rng.standard_normal(len(tt)), 1800)) * np.sin(np.pi * tt / .7) ** 2 * (.6 + .4 * np.sin(2 * np.pi * 9 * tt))
add(fx, t0('a20', 13), lowpass(rus, 5000), .06)

# ---- duck the bed under the voices, then sum
w = int(.03 * SR); e = np.convolve(np.abs(vo), np.ones(w) / w, 'same'); e = np.clip(e * 10, 0, 1)
s = np.zeros(N); p = 0.; rl = np.exp(-1 / (.18 * SR))
for i in range(N): p = e[i] if e[i] > p else p * rl; s[i] = p
out = vo + .8 * bed * (1 - .6 * s) + .8 * fx * (1 - .3 * s)
out = out / np.abs(out).max() * .9
sf.write(os.path.join(HERE, 'mix.wav'), out, SR, subtype='PCM_16'); print('mix ok', len(out) / SR, 's')
