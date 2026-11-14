"""Says Here v3 mix: voices, a bed in the flashback only, key effects, real silence after the shout.
Writes mix.wav (mono, 48 kHz, exactly NF frames long)."""
import numpy as np, soundfile as sf, subprocess
SR = 48000; NF = 562; N = NF * SR // 30
rng = np.random.default_rng(3)
vo = np.zeros(N); bed = np.zeros(N); fx = np.zeros(N)
T = lambda d: np.arange(int(d * SR)) / SR
def add(buf, t, x, g=1.0):
    i = int(t * SR); x = x[:max(0, N - i)]; buf[i:i + len(x)] += x * g
def load(p):
    x, sr = sf.read(p); assert sr == SR, sr; return x / np.abs(x).max()
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

# ---- voices: (file, start s, gain). HARV = Kokoro bm_george 1.05 + machine treatment (locked, see voices.py).
# Hoody = Tomas, recorded 14 Nov (yes take 4, thanks take 4, shout take 1).
for f, t, g in (('h1', .10, .42), ('g1', 2.12, .45), ('g2', 12.33, .5), ('h2', 13.38, .42), ('h3', 17.15, .42)):
    add(vo, t, load(f'vo/{f}.wav'), g)
add(vo, 15.24, load('vo/g3.wav'), 1.0)                                  # THOSE ARE MINE! - the loudest thing in the film

# ---- room tone under the 2027 interview (quiet, so the silence after the shout is real)
room = lowpass(rng.standard_normal(N), 300) * .02
mask = np.ones(N); mask[int(4.00 * SR):int(9.20 * SR)] = 0; mask[int(16.20 * SR):int(17.10 * SR)] = .25
bed += room * mask * .8

# ---- bed: the flashback only, 4.47-9.20 s, 120 bpm
SEC = [(4.47, 5.67, 45, [0, 4, 7, 12]), (5.67, 6.87, 43, [0, 3, 7, 10]), (6.87, 9.20, 41, [0, 4, 7, 11])]
for a, b, root, ar in SEC:
    t = a; k = 0
    while t < b - 1e-6:
        if k % 2 == 0: add(bed, t, kick(), .55)
        if k % 4 == 2: add(bed, t, hp(noise(.14, 24)), .25)
        add(bed, t, hp(hp(noise(.04, 120))), .06)
        add(bed, t, sq(midi(root + (12 if k % 8 in (3, 6) else 0)), .23, 6), .105)
        add(bed, t, sq(midi(root + 24 + ar[k % 4]), .2, 10, .25), .06)
        t += .25; k += 1

# ---- the dark room: TV hum + HARV's podcast, muffled through the wall of the screen
add(bed, 9.20, lowpass(sq(60, 1.8, 0) * .5 + rng.standard_normal(int(1.8 * SR)) * .3, 400) * np.linspace(.3, .3, int(1.8 * SR)), .12)
pod = load('vo/pod.wav'); L = int(.12 * SR); ch = [pod[i:i + L] for i in range(0, len(pod) - L, L)]
order = np.random.default_rng(11).permutation(len(ch)); fade = np.minimum(1, np.minimum(np.arange(L), L - 1 - np.arange(L)) / 240)
pod = np.concatenate([ch[i] * fade for i in order])            # speech rhythm, no words
add(bed, 9.45, lowpass(lowpass(pod, 500), 500), .45)

# ---- effects
add(fx, 3.33, sweep(2400, 4200, .25, 6), .10)                                   # glint on the shades
add(fx, 3.55, np.sin(2 * np.pi * 3520 * T(.5)) * np.exp(-T(.5) * 9), .08)            # sparkle ting
r = sweep(1400, 90, .45, 0, 'sq'); add(fx, 4.00, r * np.linspace(.4, .9, len(r)), .14)   # rewind
add(fx, 4.00, hp(noise(.45, 2)), .15)
add(fx, 8.17, sweep(500, 2400, .16), .22); add(fx, 8.33, sweep(2400, 600, .2, 4), .18)  # yoink
add(fx, 11.27, kick(1.4), .9); add(fx, 11.27, noise(.18, 22), .3)               # 9.99 stamp
for t in (11.90, 12.03): add(fx, t, hp(hp(noise(.03, 200))), .35)               # eyelid twitch ticks
add(fx, 15.20, kick(1.8), 1.1); add(fx, 15.20, noise(.5, 7), .45)              # the shout hit
b = np.sin(2 * np.pi * 1250 * T(.11)) * np.minimum(1, (.11 - T(.11)) * 60); add(fx, 16.60, b, .10)   # one tiny beep

# ---- duck the bed under the voices, then sum
w = int(.03 * SR); e = np.convolve(np.abs(vo), np.ones(w) / w, 'same'); e = np.clip(e * 10, 0, 1)
s = np.zeros(N); p = 0.; rl = np.exp(-1 / (.18 * SR))
for i in range(N): p = e[i] if e[i] > p else p * rl; s[i] = p
out = vo + .8 * bed * (1 - .6 * s) + .8 * fx * (1 - .3 * s)
out = out / np.abs(out).max() * .9
sf.write('mix.wav', out, SR, subtype='PCM_16')
print('mix ok', len(out) / SR, 's')
