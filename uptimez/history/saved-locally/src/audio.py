"""Synthesize the full soundtrack for variant A or B. Everything is wrapped on a
15 s loop so tails cross the seam. Usage: python3 audio.py A"""
import sys
import numpy as np
import soundfile as sf
from timing import VARIANTS, SHARED, FPS, N

SR = 48000
L = N * SR // FPS  # 720000 samples = 15 s
rng = np.random.default_rng(7)
v = sys.argv[1]
T = VARIANTS[v]


def add(buf, sig, t, gain=1.0):
    i0 = int(round(t * SR))
    idx = (i0 + np.arange(len(sig))) % L
    np.add.at(buf, idx, sig * gain)


def tt(d):
    return np.arange(int(d * SR)) / SR


def lowpass(x, k):
    ker = np.ones(k) / k
    return np.convolve(x, ker, mode="same")


# ---------- instruments ----------
def kick():
    t = tt(0.35)
    f = 50 + 70 * np.exp(-t * 30)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t * 9)


def clap():
    t = tt(0.15)
    n = rng.standard_normal(len(t))
    n = n - lowpass(n, 6)
    return n * np.exp(-t * 35) * 0.5


def hat():
    t = tt(0.05)
    n = rng.standard_normal(len(t))
    n = np.diff(n, prepend=0)
    return n * np.exp(-t * 90) * 0.25


def bass(freq):
    t = tt(0.45)
    s = np.sin(2 * np.pi * freq * t) + 0.3 * np.sin(2 * np.pi * freq * 2 * t)
    return s * np.minimum(1, t * 80) * np.exp(-t * 5)


def ding():
    t = tt(1.0)
    s = np.sin(2 * np.pi * 1568 * t) + 0.6 * np.sin(2 * np.pi * 2093 * t)
    return s * np.exp(-t * 4) * np.minimum(1, t * 400)


def pop():
    t = tt(0.06)
    return (np.sin(2 * np.pi * 900 * t) * 0.8 + rng.standard_normal(len(t)) * 0.4) * np.exp(-t * 70)


def click():
    t = tt(0.03)
    return np.sin(2 * np.pi * 2400 * t) * np.exp(-t * 200)


def thunk():
    t = tt(0.9)
    f = 34 + 50 * np.exp(-t * 12)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 4.5)
    imp = lowpass(rng.standard_normal(len(t)), 40) * np.exp(-t * 30) * 3
    rattle = np.zeros(len(t))
    for _ in range(18):
        p = int(rng.uniform(0.04, 0.4) * SR)
        c = click()[: len(t) - p] * rng.uniform(0.05, 0.15)
        rattle[p:p + len(c)] += c
    return body * 1.0 + imp + rattle


def hum(d):
    t = tt(d)
    f = 180 + 220 * (t / d) ** 1.5
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) + 0.35 * np.sin(3 * ph)
    return s * np.minimum(1, t / (d * 0.6)) * np.minimum(1, (d - t) * 20)


def whoosh(d):
    t = tt(d)
    n = lowpass(rng.standard_normal(len(t)), 25)
    env = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 2
    return n * env * 2.5


def scuffle(d):
    out = np.zeros(int(d * SR))
    for _ in range(int(d * 9)):
        p = int(rng.uniform(0, d - 0.1) * SR)
        b = lowpass(rng.standard_normal(int(0.07 * SR)), 8) * np.exp(-tt(0.07) * 40)
        out[p:p + len(b)] += b * rng.uniform(0.4, 1.0)
    return out


# ---------- build ----------
music = np.zeros(L)
sfx = np.zeros(L)
voice = np.zeros(L)


def music_on(t):
    return t < 8.0 or t >= T["music_back"]


for s in range(15):  # 1-second (2-beat) groove: loops cleanly in 15 repeats
    for off, kind in [(0.0, "k"), (0.25, "h"), (0.5, "c"), (0.75, "h"), (0.75, "k2")]:
        t = s + off
        if not music_on(t):
            continue
        if kind == "k":
            add(music, kick(), t, 0.9)
            add(music, bass(55 if s % 2 == 0 else 65.4), t, 0.35)
        elif kind == "k2":
            add(music, kick(), t, 0.45)
        elif kind == "c":
            add(music, clap(), t, 0.6)
        else:
            add(music, hat(), t, 1.0)

for k in ("ding1", "ding2", "ding3"):
    add(sfx, ding(), SHARED[k] / FPS, 0.28)

g0, h0 = T["glow"] / FPS, T["hatch"] / FPS
add(sfx, hum(h0 - g0), g0, 0.12)
add(sfx, pop(), h0, 0.6)
add(sfx, thunk(), T["thunk"] / FPS, 0.95)
p0 = T["pounce"] / FPS
pd = 15.0 - p0
add(sfx, whoosh(min(0.8, pd)), p0, 0.35)
add(sfx, whoosh(0.9), 14.55, 0.25)  # swell straddling the seam
add(sfx, scuffle(pd + 0.7), p0 + 0.05, 0.5)  # tail runs across the seam into the cold open
add(sfx, click(), p0 + pd * 0.72, 0.7)  # hatch clicks shut as the cube zips back

for key in ("L1", "L2", "L3", "L4", "L5", "L6"):
    a, sr = sf.read(f"{key}.wav")
    a = np.interp(np.arange(int(len(a) * SR / sr)) * sr / SR, np.arange(len(a)), a)
    start = SHARED[key] if key != "L6" else T["L6"]
    add(voice, a, start, 1.0)

# duck music under voice
env = lowpass(np.abs(voice), 2400)
env = env / (env.max() + 1e-9)
music *= 1 - 0.65 * np.clip(env * 3, 0, 1)

mix = 0.55 * music + sfx + 1.1 * voice
mix /= np.abs(mix).max() / 0.8
sf.write(f"mix_{v}.wav", mix.astype(np.float32), SR, subtype="FLOAT")
print("ok", v, round(len(mix) / SR, 3), "s")
