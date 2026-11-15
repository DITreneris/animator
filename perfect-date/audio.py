"""Perfect Date v2 mix: park, his old riff (Make It Original), the pump, the rise, plonk, creak, pop, the fall and the landing.
No new voices: Tomas's whisper, "oh" and "whoa"; MY AI's two lines. Shot starts come from render.py. Writes mix.wav (mono, 48 kHz)."""
import os, sys, numpy as np, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE); sys.path.insert(0, HERE)
import render as R, sound as S
SR = 48000; N = R.NF * SR // 30
T0 = [a / 30 for fn, a, b in R.SHOTS]                          # shot start times, s (index 0 = shot 1)
rng = np.random.default_rng(5)
vo = np.zeros(N); mus = np.zeros(N); fx = np.zeros(N); amb = np.zeros(N)
T = lambda d: np.arange(int(d * SR)) / SR
def add(buf, t, x, g=1.0):
    i = int(t * SR); x = x[:max(0, N - i)]; buf[i:i + len(x)] += x * g
def load(p): x, sr = sf.read(p); assert sr == SR; return x / np.abs(x).max()
lp = lambda x, fc: S.onepole_lp(x, fc)
def env_seg(pts):                                               # piecewise-linear gain over the whole film: [(t, g), ...]
    t = np.arange(N) / SR; return np.interp(t, [p[0] for p in pts], [p[1] for p in pts])
midi = lambda n: 440 * 2 ** ((n - 69) / 12)

# ---- ambience: park birds on the ground, wind in the sky (shots 12-19)
park = lp(rng.standard_normal(N), 500) * .045
t = .3
while t < N / SR - .3:
    d = rng.uniform(.06, .12); f0 = rng.uniform(3200, 4600); tt = T(d)
    add(park, t, np.sin(2 * np.pi * (f0 * tt + rng.uniform(-9000, 9000) * tt ** 2)) * np.sin(np.pi * tt / d), .05); t += rng.uniform(.5, 1.6)
sky_on = T0[11]
wind = lp(lp(rng.standard_normal(N), 700), 700) * .5 * (1 + .4 * np.sin(np.arange(N) / SR * 2 * np.pi * .4))
amb = park * env_seg([(0, 1), (sky_on - .3, 1), (sky_on + .3, .15), (N / SR, .15)]) \
    + wind * env_seg([(0, 0), (sky_on - .3, 0), (sky_on + .3, 1), (N / SR, 1)])

# ---- the rose: a harp sting (shot 6)
for i, n in enumerate([72, 76, 79, 84, 88]):
    tt = T(.9); add(fx, T0[5] + .3 + i * .045, np.exp(-tt * 3.2) * np.sin(2 * np.pi * midi(n) * tt), .12)

# ---- his riff, his 1986 take, round and round from shot 8 until his eyes open (shot 13)
take, ln = S.guitar_phrase(R.K.__dict__.get('RIFF') or [(62, 3), (65, 1), (60, 2), (69, 2), (67, 2), (74, 4)], detune_cents=18, seed=11)
start, stop = T0[7] + .15, T0[12]
t = start
while t < stop: add(mus, t, take / np.abs(take).max(), .55); t += ln
mus *= env_seg([(0, 1), (T0[9], 1), (T0[9] + .5, .7), (T0[10] + .8, .45), (T0[11], .45), (T0[11] + .3, .8), (N / SR, .8)])
k = int(stop * SR); mus[k:] = 0; f = int(.02 * SR); mus[k - f:k] *= np.linspace(1, 0, f)      # cut dead: eyes open

# ---- the pump: hiss in strokes (shot 9 from frame 8, through shot 10 frame 26)
a, b = T0[8] + 8 / 30, T0[9] + 26 / 30
hiss = lp(rng.standard_normal(int((b - a) * SR)), 3500) - lp(rng.standard_normal(int((b - a) * SR)), 800) * .5
tt = np.arange(len(hiss)) / SR
add(fx, a, hiss * (.55 + .45 * np.maximum(0, np.sin(2 * np.pi * 2.2 * tt))) * np.minimum(1, tt * 20), .10)
# rubber squeaks as it swells, rising
for i, t in enumerate((T0[8] + .7, T0[8] + .95, T0[9] + .3, T0[9] + .7, T0[9] + 1.1)):
    tt = T(.14); f0 = 700 + i * 140
    add(fx, t, np.sin(2 * np.pi * (f0 * tt + 900 * tt ** 2)) * np.sin(np.pi * tt / .14) * (1 + .3 * np.sin(2 * np.pi * 60 * tt)), .06)
# the hose pops off (shot 10, frame 26)
tt = T(.08); add(fx, T0[9] + 26 / 30, np.sin(2 * np.pi * 420 * tt) * np.exp(-tt * 60), .25)

# ---- dog: a tiny whimper as it backs off (shot 4)
tt = T(.3); add(fx, T0[3] + 18 / 30, np.sin(2 * np.pi * (1300 * tt - 900 * tt ** 2)) * np.sin(np.pi * tt / .3) ** 2, .05)

# ---- plonk: one string, the wrong note (shot 15, frame 3)
pl = S.ks_pluck(midi(49) * 2 ** (-40 / 1200), 1.2, bright=.25, decay=.993, seed=4)
add(fx, T0[14] + 3 / 30, S.amp(pl, drive=1.5) * np.exp(-T(1.2) * 1.5)[:len(pl)], .5)

# ---- creak: the rubber stretching (shot 17)
tt = T(.7); cr = np.sin(2 * np.pi * (180 * tt + 60 * np.sin(2 * np.pi * 3 * tt))) * (1 + .5 * np.sign(np.sin(2 * np.pi * 37 * tt)))
add(fx, T0[16] + .2, lp(cr, 1500) * np.sin(np.pi * tt / .7), .18)

# ---- POP (shot 18), then the falling whistle (shot 19) and the landing thump on frame 0
pop = rng.standard_normal(int(.06 * SR)) * np.exp(-T(.06) * 70); tt = T(.15)
add(fx, T0[17] + .02, pop, 1.2); add(fx, T0[17] + .02, np.sin(2 * np.pi * 90 * tt) * np.exp(-tt * 30), .9)
tt = T(.6); add(fx, T0[18] - .05, np.sin(2 * np.pi * np.cumsum(np.geomspace(2200, 500, len(tt))) / SR) * np.minimum(1, tt * 15), .10)
tt = T(.25); add(fx, .0, lp(rng.standard_normal(len(tt)), 300) * np.exp(-tt * 18) * 3 + np.sin(2 * np.pi * 60 * tt) * np.exp(-tt * 14), .35)

# ---- voices
for f, t, g in (('h_whisper', T0[2] + .07, .7), ('ai_watch', T0[4] + .15, .6), ('ai_turn', T0[6] + .25, .6),
                ('h_oh', T0[12] + .35, .55), ('h_whoa', T0[17] + .25, .55)):
    add(vo, t, load(f'vo/{f}.wav'), g)

# ---- duck under the voices, then sum
w = int(.03 * SR); e = np.clip(np.convolve(np.abs(vo), np.ones(w) / w, 'same') * 10, 0, 1)
s = np.zeros(N); p = 0.; rl = np.exp(-1 / (.2 * SR))
for i in range(N): p = e[i] if e[i] > p else p * rl; s[i] = p
out = vo + mus * (1 - .55 * s) + amb * (1 - .85 * s) + fx
out = out / np.abs(out).max() * .9
sf.write('mix.wav', out, SR, subtype='PCM_16'); print('mix ok', round(len(out) / SR, 2), 's')
