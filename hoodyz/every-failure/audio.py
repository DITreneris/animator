"""Every Failure mix (rough, placeholder voices): desert wind; a stone thud per landing (heavier each time), a lift grunt-less
scrape; WHOOSH on the robot's hop; a DING + claps on SUCCESS; a sudden music-less silence on the deadpan; a digital suck
while the stones dissolve; a slip on the void; a cheerful blip on "More?". Loops: the tails wrap across the seam.
Writes mix.wav (mono 48 kHz, exactly NF frames)."""
import os, sys, numpy as np, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE); sys.path.insert(0, HERE)
import animatic as AN
SR = 48000; N = AN.NF * SR // 30
rng = np.random.default_rng(11)
vo = np.zeros(N); fx = np.zeros(N); amb = np.zeros(N)
T = lambda d: np.arange(int(d * SR)) / SR
def add(buf, t, x, g=1.0):                                            # wraps across the loop point
    i = int(t * SR) % N; n = len(x); end = min(N, i + n); buf[i:end] += x[:end - i] * g
    if i + n > N: buf[:i + n - N] += x[end - i:] * g
def lp(x, fc):
    a = np.exp(-2 * np.pi * fc / SR); y = np.zeros_like(x); p = 0.
    for k in range(len(x)): p = (1 - a) * x[k] + a * p; y[k] = p
    return y
def load(p): x, sr = sf.read(p); x = x if x.ndim == 1 else x[:, 0]; assert sr == SR; return x / np.abs(x).max()
fr = lambda f: f / 30
fo = lambda o: AN.new_of(o) / 30                                  # a cue placed on the v3 timeline -> the v4 timeline

amb += lp(rng.standard_normal(N), 400) * .035                         # desert wind
def thud(w):
    t = T(.45); return (np.sin(2 * np.pi * (55 + 30 * w) * t * (1 - .5 * t)) * np.exp(-t * 9) + lp(rng.standard_normal(len(t)), 900) * np.exp(-t * 22) * .6) * (.5 + .5 * w)
for name, lift, t0, land, kind in AN.MTH:                         # the montage: heavy, a fast patter, then one pebble - TIK
    if kind == 'peb': add(fx, fr(land), np.sin(2 * np.pi * 2400 * T(.06)) * np.exp(-T(.06) * 90) + lp(rng.standard_normal(len(T(.06))), 6000) * np.exp(-T(.06) * 120) * .5, .5)
    else: add(fx, fr(land), thud(1.0 if kind == 'big' else .45), .9 if kind == 'big' else .55)   # the montage: heavy, then a fast patter
def whoosh(d=.35, up=True):
    t = T(d); n = lp(rng.standard_normal(len(t)), 2500) * np.sin(np.pi * t / d) ** 2; return n * 1.4
add(fx, fo(139), whoosh(.3)); add(fx, fo(149), whoosh(.35)); add(fx, fo(345), whoosh(.45))
for k in (159, 168, 176): add(fx, fo(k), np.sin(2 * np.pi * 900 * T(.05)) * np.exp(-T(.05) * 60), .25)   # little robot steps
t = T(1.2); ding = sum(np.sin(2 * np.pi * f0 * t) * np.exp(-t * 2.5) / (j + 1) for j, f0 in enumerate((1318, 1975, 2637)))
add(fx, fo(182), ding, .35)
for k in range(118, 245, 6):
    if 205 <= k < 225: continue                                          # her claps (from his step on)
    c = lp(rng.standard_normal(int(.04 * SR)), 5000) * np.exp(-T(.04) * 80); add(fx, fo(k), c, .5)
t = T(1.6); suck = np.sin(2 * np.pi * (300 + 900 * t / 1.6) * t) * .25 * np.sin(np.pi * t / 1.6) + lp(rng.standard_normal(len(t)), 3000) * .15
add(fx, fo(312), suck); add(fx, fo(372), suck[:int(.4 * SR)])
t = T(.5); slip = np.sin(2 * np.pi * (700 - 500 * t) * t) * np.exp(-t * 4) * .4; add(fx, fo(381), slip)
t = T(.25); blip = np.sin(2 * np.pi * 880 * t) * np.exp(-t * 10) * .3 + np.sin(2 * np.pi * 1320 * t) * np.exp(-t * 14) * .2; add(fx, fo(438), blip)
t = T(.35); sag = np.sin(2 * np.pi * 70 * t) * np.exp(-t * 10) * .6; add(fx, fo(495), sag)

VO = [('h_every', fr(2)), ('h_success_v2', fo(116)), ('ai_thanks', fo(286)), ('ai_more', fo(441))]
for name, t0 in VO: add(vo, t0, load(f'vo/{name}.wav'), .9)
duck = np.convolve(np.abs(vo) > .02, np.ones(int(.15 * SR)) / int(.15 * SR), 'same')
mix = vo + fx * .7 * (1 - .8 * np.clip(duck, 0, 1)) + amb * (1 - .5 * np.clip(duck, 0, 1))   # effects duck under every line (claps masked 'Success!')
s0, s1 = int(fo(240) * SR), int(fo(270) * SR); mix[s0:s1] *= np.linspace(1, .15, s1 - s0) ** 0 * .15 + .0   # the deadpan: near silence
mix = mix / np.abs(mix).max() * .9
fd = int(.02 * SR); r = np.linspace(0, 1, fd); mix[:fd] *= r; mix[-fd:] *= r[::-1]
sf.write('mix.wav', mix, SR); print('mix ok', len(mix) / SR, 's')
