"""Just One Line mix: voices (lines.json), synthesized SFX on the picture's own events, a 120 bpm bed under the fight only
(it stops for the close-up, and the stamp, the takeover and the loop are dry), room tone through the loop.
Writes mix.wav (mono, 48 kHz, exactly NF frames long)."""
import os, sys, json, numpy as np, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..'))
import film as FM, fight as FI
SR = 48000; NF = FM.NF; N = NF * SR // 30
rng = np.random.default_rng(7)
vo = np.zeros(N); bed = np.zeros(N); fx = np.zeros(N)
T = lambda d: np.arange(int(d * SR)) / SR
OFF = FM.START['F']
def fr_of(story): return OFF + story + FI.held_before_story(story)
def add(buf, fr, x, g=1.0):                                            # tails wrap over the loop point
    i = int(fr / 30 * SR) % N; n = len(x); k = min(n, N - i); buf[i:i + k] += x[:k] * g
    if n > k: buf[:n - k] += x[k:n] * g
def noise(d, dec): t = T(d); return rng.standard_normal(len(t)) * np.exp(-t * dec)
hp = lambda x: np.diff(x, prepend=0)
def lowpass(x, fc):
    a = np.exp(-2 * np.pi * fc / SR); y = np.zeros_like(x); p = 0.
    for i in range(len(x)): p = (1 - a) * x[i] + a * p; y[i] = p
    return y
def sweep(a, b, d, dec=0):
    t = T(d); ph = np.cumsum(np.linspace(a, b, len(t))) / SR * 2 * np.pi; return np.sin(ph) * np.exp(-t * dec)
def P(*xs):                                                             # sum of sounds of different lengths
    n = max(len(x) for x in xs); y = np.zeros(n)
    for x in xs: y[:len(x)] += x
    return y
def kick(g=1): t = T(.22); return np.sin(2 * np.pi * (48 * t + (110 / 30) * (1 - np.exp(-30 * t)))) * np.exp(-t * 14) * g
def thud(big=1.0): return P(kick() * 1.2 * big, lowpass(noise(.12, 30), 900) * .8 * big)
def whoosh(d=.25, up=True):
    t = T(d); env = np.sin(np.pi * t / d) ** 2; x = lowpass(rng.standard_normal(len(t)), 1800) * env; return hp(x) * 2.5
def clank(): return P(sum(np.sin(2 * np.pi * f * T(.25)) * np.exp(-T(.25) * 18) for f in (620, 930, 1410)) * .4, hp(noise(.03, 200)) * .5)
def boing(f0=180): t = T(.35); return np.sin(2 * np.pi * np.cumsum(f0 * (1 + .5 * np.sin(2 * np.pi * 14 * t) * np.exp(-t * 6))) / SR) * np.exp(-t * 7)
def click(): return hp(hp(noise(.012, 500))) * .6
def blip(f=1400): t = T(.05); return np.sign(np.sin(2 * np.pi * f * t)) * np.exp(-t * 60) * .35
def ding(): return sum(np.sin(2 * np.pi * f * T(1.2)) * np.exp(-T(1.2) * 3) / (i + 1) for i, f in enumerate((1318.5, 1975.5, 2637)))
def crash(): return P(lowpass(noise(.7, 5), 3000) * 1.2, thud(1.3), sum(np.sin(2 * np.pi * f * T(.6)) * np.exp(-T(.6) * 6) for f in (210, 333)) * .3)
def squeak(): return sweep(1600, 2300, .12, 8) * .25
def roll(d): t = T(d); return lowpass(rng.standard_normal(len(t)), 220) * (1 + .5 * np.sin(2 * np.pi * 9 * t)) * np.exp(-t * 1.2) * 1.5
def zip_(): t = T(.3); return hp(rng.standard_normal(len(t)) * (np.sin(2 * np.pi * 60 * t) > 0)) * np.linspace(.3, 1, len(t)) * .5

# ---- voices
for L in json.load(open(os.path.join(HERE, 'lines.json'))):
    x, sr = sf.read(os.path.join(HERE, 'vo', L['name'] + '.wav')); assert sr == SR
    add(vo, L['start'] * 30, x / np.abs(x).max(), .62)

for L in json.load(open(os.path.join(HERE, 'reactions.json'))):           # Tomas's reactions (no words to check)
    x, sr = sf.read(os.path.join(HERE, 'vo', L['name'] + '.wav')); assert sr == SR
    add(vo, L['start'] * 30, x / np.abs(x).max(), L['gain'])

# ---- room tone, the whole loop
bed += lowpass(rng.standard_normal(N), 300) * .03

# ---- A: the snatch and the flick
add(fx, 6, hp(noise(.08, 60)), .3); add(fx, 8, whoosh(.25), .35); add(fx, 16, clank() * .5, .4)
# ---- F: the fight, on the picture's own frames
EV = [(8, 'thud', 1.0), (8, 'roll', 1), (32, 'clank', 1), (36, 'squeak', 1), (47, 'whoosh', 1), (FI.BONK, 'thud', .9), (FI.BONK, 'clank', 1),
      (FI.B3 + 8, 'boing', 1), (FI.B3 + 18, 'boing', 1.2), (FI.YANK - 4, 'zip', 1), (FI.YANK, 'whoosh', 1),
      (FI.PUSHF, 'thud', 1.0), (FI.PUSHF + 8, 'squeak', 1), (FI.PUSHF + 11, 'thud', .5), (FI.LEAP - 2, 'boing', .8), (FI.LEAP, 'whoosh', 1.3),
      (FI.CONTACT, 'thud', 1.5), (FI.CONTACT, 'roll', 1), (FI.WALL, 'crash', 1), (FI.WALL + 10, 'thud', .8), (FI.CONTACT + 10, 'clank', 1)]
for i in range(5): EV.append((FI.B3 + 2 + 5 * i, 'whoosh_s', 1))       # the windmill
SND = dict(thud=thud, roll=lambda: roll(.9), clank=clank, squeak=squeak, whoosh=lambda: whoosh(.22), boing=boing, zip=zip_,
           crash=crash, whoosh_s=lambda: whoosh(.14))
GAIN = dict(thud=.5, roll=.25, clank=.25, squeak=.3, whoosh=.35, boing=.35, zip=.35, crash=.45, whoosh_s=.18)
for s, k, g in EV: add(fx, fr_of(s), SND[k]() * g, GAIN[k])
prev = 0
for f in range(FI.NF):                                                  # counter ticks and typing
    g = FI.story(f); n = FI.counter(g)
    if n != prev: add(fx, OFF + f, blip(1200 + 40 * n), .25); prev = n
    flying = FI.LEAP - 6 <= g < FI.CONTACT + 12 or g < 18
    if not flying and f % (3 if g < FI.B4 else 2) == 0: add(fx, OFF + f, click(), .22)
# ---- the bed: 120 bpm (a beat = 15 frames), the fight only
a, b = OFF, FM.START['G']
midi = lambda n: 440 * 2 ** ((n - 69) / 12)
def sq(fr, d, dec=4, duty=.5): t = T(d); return np.where((t * fr) % 1 < duty, 1, -1) * np.exp(-t * dec)
ROOT = [45, 45, 43, 41]
for k, fr in enumerate(range(a, b, 15 // 2)):
    beat = k // 2
    if k % 2 == 0: add(bed, fr, kick(), .45)
    if k % 4 == 2: add(bed, fr, hp(noise(.12, 26)), .2)
    add(bed, fr, hp(hp(noise(.03, 140))), .05)
    add(bed, fr, sq(midi(ROOT[(beat // 4) % 4] + (12 if k % 8 in (3, 6) else 0)), .2, 7), .07)
# ---- G: the push-in, the rush of ticks, the DING
G = FM.START['G']
add(fx, G, whoosh(.3), .35)
prev = 32
for t in range(45):
    n = FM.g_count(t)
    if n != prev: add(fx, G + t, blip(1500 + 30 * n), .22); prev = n
    if t < 23 and t % 2 == 0: add(fx, G + t, click(), .25)
add(fx, G + 23, ding(), .35)
# ---- H: door, steps, glint, THUNK, the briefcase
Hs = FM.START['H']
add(fx, Hs + 2, P(thud(.8), clank() * .5), .45)
for t in range(5, 24, 5): add(fx, Hs + t, clank(), .2)
add(fx, Hs + 22, np.sin(2 * np.pi * 3000 * T(.3)) * np.exp(-T(.3) * 12), .12)
add(fx, Hs + 35, whoosh(.15), .25); add(fx, Hs + 40, P(thud(1.1), hp(noise(.05, 80)) * .6), .55)
add(fx, Hs + 41, whoosh(.2), .2); add(fx, Hs + 56, whoosh(.18), .2); add(fx, Hs + 66, thud(.5), .35)
# ---- J: slurps; K: the card, the twitch
J = FM.START['J']
for t in (20, 40): add(fx, J + t, lowpass(noise(.35, 6) * (1 + np.sin(2 * np.pi * 30 * T(.35))), 1200), .25)
Ks = FM.START['K']
add(fx, Ks + 4, hp(noise(.1, 50)), .2); add(fx, Ks + 30, hp(noise(.08, 60)), .2)
for t in range(40, 80):
    if (t // 3) % 3 == 0 and t % 3 == 0: add(fx, Ks + t, blip(2200), .12)

# ---- the nightmare: a low drone that grows with the dark (film.night), swells under the closing eyes, and stops dead at the cut
nt = np.interp(np.arange(N) / SR * 30, np.arange(NF), [FM.night(f) for f in range(NF)])
tt = np.arange(N) / SR
drone = (np.sin(2 * np.pi * 55 * tt) + .6 * np.sin(2 * np.pi * 82.4 * tt + np.sin(2 * np.pi * .3 * tt)) + lowpass(rng.standard_normal(N), 160) * 2) * nt ** 1.5
b0 = int((NF - FM.BLINK) / 30 * SR); sw = np.zeros(N); sw[b0:] = np.linspace(0, 1, N - b0) ** 2
bed += drone * .06 + lowpass(rng.standard_normal(N), 900) * sw * .25 + np.sin(2 * np.pi * 41 * tt) * sw * .35
duck = np.ones(N)                                                       # the bed and the effects step back under every spoken line
for L in json.load(open(os.path.join(HERE, 'lines.json'))):
    i, j = int(L['start'] * SR), int((L['start'] + L['dur']) * SR); duck[i:j] = .2
duck = np.convolve(duck, np.ones(4800) / 4800, 'same')
mix = vo + (bed + fx) * duck
sf.write(os.path.join(HERE, 'mix.wav'), mix / np.abs(mix).max() * .9, SR)
print('mix.wav', round(N / SR, 3), 's')
