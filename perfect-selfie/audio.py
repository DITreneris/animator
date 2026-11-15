"""Perfect Trip mix: per-place ambience, MY AI's telescoping clicks, the shutter and the stamp thunk on every photo,
Hoody's shuffle back, the camel's rope, a flourish on Rome, the voices from render.VO. Writes mix.wav (mono 48 kHz, exactly NF frames)."""
import os, sys, numpy as np, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE); sys.path.insert(0, HERE)
import render as R
SR = 48000; N = R.NF * SR // 30
T0 = [a / 30 for fn, a, b in R.SHOTS]
rng = np.random.default_rng(7)
vo = np.zeros(N); fx = np.zeros(N); amb = np.zeros(N)
T = lambda d: np.arange(int(d * SR)) / SR
def add(buf, t, x, g=1.0):
    i = int(t * SR); x = x[:max(0, N - i)]; buf[i:i + len(x)] += x * g
def lp(x, fc):
    a = np.exp(-2 * np.pi * fc / SR); y = np.zeros_like(x); p = 0.
    for i in range(len(x)): p = (1 - a) * x[i] + a * p; y[i] = p
    return y
def load(p): x, sr = sf.read(p); assert sr == SR; return x / np.abs(x).max()
midi = lambda n: 440 * 2 ** ((n - 69) / 12)

# ---- ambience per place: birds (Pisa, Paris), desert wind (Giza), a city square (Rome)
place_of = ['park', 'pisa', 'pisa', 'pisa', 'paris', 'paris', 'giza', 'giza', 'rome', 'rome', 'park', 'park']
noise = lp(rng.standard_normal(N), 600)
for i, (fn, a, b) in enumerate(R.SHOTS):
    t0, t1 = a / 30, b / 30; seg = slice(int(t0 * SR), int(t1 * SR)); pl = place_of[i]
    amb[seg] += noise[seg] * (.05 if pl == 'giza' else .02)
    if pl in ('pisa', 'paris', 'park'):
        t = t0 + .2
        while t < t1 - .2:
            d = rng.uniform(.06, .12); tt = T(d); f0 = rng.uniform(3200, 4600)
            add(amb, t, np.sin(2 * np.pi * (f0 * tt + rng.uniform(-9000, 9000) * tt ** 2)) * np.sin(np.pi * tt / d), .03); t += rng.uniform(.4, 1.2)
    if pl == 'rome':
        amb[seg] += lp(rng.standard_normal(seg.stop - seg.start), 900) * .03                # murmur

# ---- MY AI's arm telescoping out: a click per section (Pisa shot 1 from frame 16, Paris shot 3 from frame 36)
def clicks(t, n=3, gap=.16):
    for k in range(n):
        tt = T(.05); add(fx, t + k * gap, np.sin(2 * np.pi * (2400 - 300 * k) * tt) * np.exp(-tt * 90) + rng.standard_normal(len(tt)) * np.exp(-tt * 120) * .4, .25)
clicks(T0[2] + 16 / 30); clicks(T0[4] + 50 / 30, gap=.12)

# ---- every photo: the shutter (click + whirr), then the stamp's thunk
def shutter(t):
    tt = T(.04); add(fx, t, rng.standard_normal(len(tt)) * np.exp(-tt * 140), .45)
    tt = T(.12); add(fx, t + .05, np.sin(2 * np.pi * 900 * tt) * np.exp(-tt * 40) * .5 + lp(rng.standard_normal(len(tt)), 2000) * .4, .25)
def thunk(t):
    tt = T(.18); add(fx, t, np.sin(2 * np.pi * 110 * tt) * np.exp(-tt * 30) + lp(rng.standard_normal(len(tt)), 400) * np.exp(-tt * 40), .5)
for i in (3, 5, 7, 9):
    shutter(T0[i]); thunk(T0[i] + 6 / 30)

# ---- Hoody shuffling back (Paris), the rope creaking (Giza)
for k in range(8): tt = T(.06); add(fx, T0[4] + (14 + k * 5) / 30, lp(rng.standard_normal(len(tt)), 700) * np.exp(-tt * 50), .25)
tt = T(.5); add(fx, T0[6] + 24 / 30, np.sin(2 * np.pi * (150 * tt + 30 * np.sin(2 * np.pi * 5 * tt))) * np.sin(np.pi * tt / .5) * (1 + .4 * np.sign(np.sin(2 * np.pi * 33 * tt))), .12)

# ---- Rome: a short flourish as the label switches; the reveal is near silence
for k, n in enumerate([72, 76, 79, 84]):
    tt = T(.9); add(fx, T0[9] + 14 / 30 + k * .06, np.exp(-tt * 3) * np.sin(2 * np.pi * midi(n) * tt), .12)

# ---- MY AI pops up from behind the bench (a springy boing); her phone turns (a soft swish)
tt = T(.3); add(fx, T0[0] + 76 / 30, np.sin(2 * np.pi * (300 * tt + 500 * tt ** 2)) * np.exp(-tt * 9), .18)
tt = T(.2); add(fx, T0[10] + 62 / 30, lp(rng.standard_normal(len(tt)), 3000) * np.sin(np.pi * tt / .2), .12)

# ---- voices
for f, shot, off, g in R.VO: add(vo, T0[shot] + round(off * 30) / 30, load(f'vo/{f}.wav'), g)

w = int(.03 * SR); e = np.clip(np.convolve(np.abs(vo), np.ones(w) / w, 'same') * 10, 0, 1)
s = np.zeros(N); p = 0.; rl = np.exp(-1 / (.2 * SR))
for i in range(N): p = e[i] if e[i] > p else p * rl; s[i] = p
out = vo + amb * (1 - .8 * s) + fx
out = out / np.abs(out).max() * .9
sf.write('mix.wav', out, SR, subtype='PCM_16'); print('mix ok', round(len(out) / SR, 2), 's')
