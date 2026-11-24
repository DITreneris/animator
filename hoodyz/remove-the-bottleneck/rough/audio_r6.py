"""Remove the Bottleneck rough mix: Tomas's takes (recordings 53-63), synthesized effects on the picture's events, a little march under
the carry (double time for the sprints; silent for the empty office, the drop and the loop). Writes mix.wav (mono, 48 kHz, NF frames)."""
import os, sys, json, numpy as np, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import film as FM
SR = 48000; NF = FM.NF; N = NF * SR // 30
rng = np.random.default_rng(5)
vo = np.zeros(N); bed = np.zeros(N); fx = np.zeros(N)
T = lambda d: np.arange(int(d * SR)) / SR
S = FM.START
def add(buf, fr, x, g=1.0):
    i = int(fr / 30 * SR) % N; n = len(x); k = min(n, N - i); buf[i:i + k] += x[:k] * g
    if n > k: buf[:n - k] += x[k:n] * g
def P(*xs):
    n = max(len(x) for x in xs); y = np.zeros(n)
    for x in xs: y[:len(x)] += x
    return y
def noise(d, dec): t = T(d); return rng.standard_normal(len(t)) * np.exp(-t * dec)
hp = lambda x: np.diff(x, prepend=0)
def lowpass(x, fc):
    a = np.exp(-2 * np.pi * fc / SR); y = np.zeros_like(x); p = 0.
    for i in range(len(x)): p = (1 - a) * x[i] + a * p; y[i] = p
    return y
def kick(): t = T(.22); return np.sin(2 * np.pi * (48 * t + (110 / 30) * (1 - np.exp(-30 * t)))) * np.exp(-t * 14)
def thud(b=1.0): return P(kick() * 1.2 * b, lowpass(noise(.12, 30), 900) * .8 * b)
def popsnd(): t = T(.18); return np.sin(2 * np.pi * np.cumsum(np.linspace(300, 1400, len(t))) / SR) * np.exp(-t * 18)
def tick(): t = T(.08); return np.sin(2 * np.pi * 1800 * t) * np.exp(-t * 50)
def scribble(d): t = T(d); return hp(rng.standard_normal(len(t))) * (np.sin(2 * np.pi * 7 * t) > 0) * .4
def whoosh(d=.25): t = T(d); return hp(lowpass(rng.standard_normal(len(t)), 1800) * np.sin(np.pi * t / d) ** 2) * 2.5
def zipt(d=.3): t = T(d); return hp(rng.standard_normal(len(t)) * (np.sin(2 * np.pi * 50 * t) > 0)) * .4
def slam(): return P(thud(1.4), lowpass(noise(.4, 8), 2500) * .8)
def roll(d): t = T(d); return lowpass(rng.standard_normal(len(t)), 220) * (1 + .5 * np.sin(2 * np.pi * 9 * t)) * 1.5
def ding(): return sum(np.sin(2 * np.pi * f * T(1.0)) * np.exp(-T(1.0) * 3) / (i + 1) for i, f in enumerate((1318.5, 1975.5)))
for L in json.load(open(os.path.join(HERE, 'lines.json'))):
    x, sr = sf.read(os.path.join(HERE, 'vo', L['name'] + '.wav')); add(vo, L['start'] * 30, x / np.abs(x).max(), .62)
for L in json.load(open(os.path.join(HERE, 'reactions.json'))):           # Tomas's wordless takes
    x, sr = sf.read(os.path.join(HERE, 'vo', L['name'] + '.wav')); add(vo, L['start'] * 30, x / np.abs(x).max(), L['gain'])
bed += lowpass(rng.standard_normal(N), 300) * .03
for at, _, _ in FM.POPS: add(fx, at, popsnd(), .35)
add(fx, S['B'], P(thud(.4), hp(noise(.05, 80)) * .7), .35)                                              # the list, slapped onto the wall
for at in (10, 17, 24): add(fx, S['B'] + at, tick(), .3)
add(fx, S['B'] + 31, zipt(.25), .25); add(fx, S['B'] + 15, lowpass(noise(.3, 6), 1000), .2)           # the circle; his sip
add(fx, S['C'], roll(.4), .3); add(fx, S['C'] + 4, whoosh(.2), .2); add(fx, S['C'] + 6, zipt(.3), .25)
for i in range(6): add(fx, S['C'] + 25 + 7 * i, scribble(.15), .15)
add(fx, S['D'], whoosh(.2), .4); add(fx, S['D'] + 6, whoosh(.35), .35); add(fx, S['D'] + 14, thud(.9), .5)
for i in range(5): add(fx, S['D'] + 20 + 8 * i, thud(.3), .25)
add(fx, S['D'] + 60, slam(), .55)
add(fx, S['E'] + 29, tick(), .35)                                          # the last box, ticked
add(fx, S['E'] + 4, whoosh(.4), .2); add(fx, S['E'] + 26, P(thud(.6), hp(noise(.06, 70)) * .8), .45)       # the sticker, slapped on
# ---- F: the carry, the sprint out of the left, the empty office, back in from the right, the drop, frame 0
F0 = S['F']; G = FM
def patter(a, b, g0, g1, step=2):                                        # fast little feet, getting quieter or louder
    for k, fr in enumerate(range(a, b, step)): add(fx, F0 + fr, thud(.22), lerp_(g0, g1, k / max(1, (b - a) // step - 1)))
lerp_ = lambda p, q, u: p + (q - p) * u
def buzz(): t = T(.28); return np.sign(np.sin(2 * np.pi * 220 * t)) * (np.sin(2 * np.pi * 9 * t) > 0) * np.exp(-t * 3)
def skid(d=.3): t = T(d); return hp(rng.standard_normal(len(t))) * np.linspace(1, .2, len(t)) * (1 + .5 * np.sin(2 * np.pi * 40 * t)) * .6
for i in range(2, G.T_GO - 6, 8):                                       # marching on the spot (not under "Faster!")
    if not 30 <= i < 54: add(fx, F0 + i, thud(.25), .2)
add(fx, F0 + 16, scribble(.45), .2); add(fx, F0 + 22, tick(), .25)        # HARV's pen (before "Faster!"); the thumb
add(fx, F0 + G.T_GO - 4, np.sin(2 * np.pi * np.cumsum(np.linspace(200, 500, int(.12 * SR))) / SR) * .5, .3)   # the wind-up
add(fx, F0 + G.T_GO, whoosh(.5), .5); patter(G.T_GO, G.T_OUT + 4, .3, .04)
add(fx, F0 + G.T_GO + 2, hp(whoosh(.35)), .3)                              # the list torn off the wall
#add(fx, F0 + G.T_OUT + 3, ding(), .3)                                     # the board: green, flowing

#add(fx, F0 + G.T_BACK - 1, buzz(), .28)                                   # the board: red - he is back
patter(G.T_BACK - 4, G.T_STOP - 4, .04, .3); add(fx, F0 + G.T_STOP - 9, skid(.32), .4)
for at, _ in G.POPS_F: add(fx, F0 + at, popsnd(), .28)
add(fx, F0 + G.T_DROP, whoosh(.14), .3); add(fx, F0 + G.T_HIT, slam(), .6)
add(fx, F0 + G.T_HIT + 1, whoosh(.3), .3)                                 # the lid, the sticker
patter(G.T_DROP + 1, G.T_LAND - 1, .12, .12, 3)                           # MY AI trots to its place
add(fx, F0 + G.T_LAND, thud(.5), .4)                                      # he lands on his feet
midi = lambda n: 440 * 2 ** ((n - 69) / 12)
def march(a, b, step):                                                   # a little march under the carry; double time for the sprints
    for k, fr in enumerate(range(F0 + a, F0 + b, step)):
        add(bed, fr, kick(), .3 if k % 2 == 0 else .15)
        t = T(.16); add(bed, fr, np.sign(np.sin(2 * np.pi * midi([57, 60, 64, 60][k % 4]) * t)) * np.exp(-t * 10), .05)
march(2, G.T_GO - 4, 8); march(G.T_GO, G.T_OUT, 4); march(G.T_BACK, G.T_STOP - 2, 4)
duck = np.ones(N)                                                       # effects and the march step back under the words
for L in json.load(open(os.path.join(HERE, 'lines.json'))):
    i, j = int(L['start'] * SR), int((L['start'] + L['dur']) * SR); duck[i:j] = .15
duck = np.convolve(duck, np.ones(4800) / 4800, 'same')
mix = vo + (bed + fx) * duck
sf.write(os.path.join(HERE, 'mix.wav'), mix / np.abs(mix).max() * .9, SR); print('mix.wav')
