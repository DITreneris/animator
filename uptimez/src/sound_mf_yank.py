"""v2 (sound_mf_yank_v1.py = v1): cues moved to the v2 timing; a plastic tap when the cap lands.
Temporary effects for the yank motion test (mf_yank.py): footsteps, the lunge whoosh, the chain twang, the
snap-back thud and chair creak, the cap's little pop and its landing tap, the glasses tick. Writes mf_yank_sfx.wav."""
import numpy as np
import soundfile as sf

SR = 48000
L = int(2.9 * SR)
rng = np.random.default_rng(5)


def tt(d):
    return np.arange(int(d * SR)) / SR


def lp(x, k):
    return np.convolve(x, np.ones(k) / k, mode="same")


def add(buf, at, x, g=1.0):
    i = int(at * SR)
    n = min(len(x), len(buf) - i)
    buf[i:i + n] += x[:n] * g


def step():
    t = tt(0.09)
    return (np.sin(2 * np.pi * 110 * t) + 0.6 * lp(rng.standard_normal(len(t)), 6)) * np.exp(-t * 45)


def whoosh(d):
    t = tt(d)
    return lp(rng.standard_normal(len(t)), 14) * np.sin(np.pi * t / d) ** 2 * 1.4


def twang():
    t = tt(0.55)
    f = 620 * (1 - 0.06 * t)
    x = sum(np.sin(2 * np.pi * f * h * t) / h for h in (1, 2.01, 3.03, 4.1))
    jingle = lp(rng.standard_normal(len(t)), 2) * np.exp(-t * 30) * 0.8
    return (x * np.exp(-t * 7) + jingle) * 0.55


def thud(f=70, d=0.5):
    t = tt(d)
    return (np.sin(2 * np.pi * f * t) + 0.5 * lp(rng.standard_normal(len(t)), 20)) * np.exp(-t * 9)


def creak(d=0.35):
    t = tt(d)
    f = 170 + 50 * np.sin(2 * np.pi * 4 * t)
    return np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.18 * np.sin(np.pi * t / d)


def pop():
    t = tt(0.12)
    return np.sin(2 * np.pi * (900 - 3000 * t) * t) * np.exp(-t * 35) * 0.5


def tick():
    t = tt(0.04)
    return np.sin(2 * np.pi * 3200 * t) * np.exp(-t * 160) * 0.4


buf = np.zeros(L)
for s in np.arange(0.05, 1.6, 0.31):
    add(buf, s, step(), 0.35)
add(buf, 0.30, whoosh(0.5), 0.35)
add(buf, 0.80, twang(), 0.9)           # taut
add(buf, 1.05, thud(90, 0.3), 0.7)     # the release snap
add(buf, 1.05, pop(), 0.6)             # the cap launches
add(buf, 1.44, creak(), 0.7)
add(buf, 1.50, thud(55, 0.4), 0.9)     # the body lands in the chair
add(buf, 1.65, thud(240, 0.12), 0.5)   # the cap lands: a plastic tap
add(buf, 2.05, tick(), 1.0)            # glasses
buf = buf / max(1e-9, np.max(np.abs(buf))) * 0.6
sf.write("mf_yank_sfx.wav", np.stack([buf, buf], 1), SR)
print("wrote mf_yank_sfx.wav")
