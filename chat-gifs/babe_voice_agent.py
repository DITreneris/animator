"""Babe / Voice Agent: re-time the Messenger GIF (19.9 s -> 14.85 s) and compose a
catchy music bed with chat SFX, a tape-stop at the punchline and an ending sting.

Writes build/babe_voice_agent/{frames/, list.txt, audio.wav}. build.sh does the encode.
"""
import sys

import numpy as np

from common import SR, env, put, save_wav, unpack, write_concat

OUT = sys.argv[1] if len(sys.argv) > 1 else "build/babe_voice_agent"
N = unpack("src/babe_voice_agent.gif", OUT)

dots = {*range(1, 7), *range(13, 19), *range(25, 31)}  # her typing indicator
enddots = set(range(37, 55))  # endless typing after the punchline
# Reading holds (ms): long message (21) longest; punchline (36) holds 1.5 s;
# last frame long enough for the dun-dun-DUN tail.
hold = {0: 250, 9: 900, 12: 1000, 21: 1800, 24: 1500, 33: 1300, 36: 1500, 55: 1800}
dur = [hold.get(i, 100 if i in dots else 120 if i in enddots else 70) for i in range(N)]
st, total = write_concat(OUT, dur)

rng = np.random.default_rng(3)
L = int(SR * total)  # exactly the video length, so the fade-out lands
mid = lambda m: 440 * 2 ** ((m - 69) / 12)

# ---------- music bed: 116 BPM, C-Am-F-G, plucked hook
BPM = 116
beat = 60 / BPM
t_stop = st[34]  # "Already training my voice agent." appears
mus = np.zeros(L)


def pluck(f, d=0.35):  # Karplus-Strong
    n, p = int(d * SR), int(SR / f)
    buf = rng.uniform(-1, 1, p)
    out = np.zeros(n)
    for i in range(n):
        out[i] = buf[i % p]
        buf[i % p] = 0.5 * (buf[i % p] + buf[(i + 1) % p]) * 0.996
    return out * env(n, 0.001, d / 2.5)


def kick():
    n = int(0.25 * SR)
    t = np.arange(n) / SR
    f = 50 + 90 * np.exp(-t / 0.03)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.001, 0.09)


def snap():
    n = int(0.12 * SR)
    x = np.convolve(rng.normal(0, 1, n), [1, -1], "same")
    return (x * 0.6 + np.sin(2 * np.pi * 1800 * np.arange(n) / SR) * 0.3) * env(n, 0.001, 0.035)


def hat():
    n = int(0.05 * SR)
    return np.convolve(rng.normal(0, 1, n), [1, -1], "same") * env(n, 0.0005, 0.012)


def bass(f, d):
    n = int(d * SR)
    t = np.arange(n) / SR
    return (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t)) * env(n, 0.005, d / 2)


hook = [(0, 72), (0.5, 76), (1, 79), (1.5, 76), (2, 81), (2.75, 79), (3, 76), (3.5, 74),
        (4, 72), (4.5, 76), (5, 79), (5.5, 84), (6, 83), (6.5, 79), (7, 76), (7.5, 74)]
bassline = [(0, 48), (2, 45), (4, 41), (6, 43)]
cache = {}
nb = int(t_stop / beat) + 2
for b in range(0, nb, 8):
    for off, m in hook:
        cache.setdefault(m, pluck(mid(m)))
        put(mus, cache[m], (b + off) * beat, 0.35)
    for off, m in bassline:
        put(mus, bass(mid(m), beat * 2), (b + off) * beat, 0.35)
K, S, H = kick(), snap(), hat()
for b in range(nb):
    t = b * beat
    put(mus, K if b % 2 == 0 else S, t, 0.9 if b % 2 == 0 else 0.45)
    put(mus, H, t + beat / 2, 0.18)
    put(mus, H, t, 0.1)
fi = int(0.4 * SR)
mus[:fi] *= np.linspace(0, 1, fi)

# tape-stop at the punchline: playback rate ramps 1 -> 0 over 0.55 s
s, n = int(t_stop * SR), int(0.55 * SR)
src = mus[s : s + n].copy()
pos = np.clip(np.cumsum(np.linspace(1, 0, n) ** 1.3), 0, len(src) - 1)
stopped = np.interp(pos, np.arange(len(src)), src) * np.linspace(1, 0.2, n)
mus[s:] = 0
mus[s : s + n] = stopped[: len(mus) - s]

# ---------- sfx
fx = np.zeros(L)


def pop(f):
    n = int(0.15 * SR)
    t = np.arange(n) / SR
    fr = f * (1 + 0.6 * np.exp(-t / 0.01))
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * env(n, 0.001, 0.035)


def swoosh():
    n = int(0.22 * SR)
    x = rng.normal(0, 1, n)
    y = np.zeros(n)
    y1 = y2 = 0.0
    for i in range(n):
        w = 2 * np.pi * (900 + 3500 * i / n) / SR
        r = 0.96
        v = x[i] + 2 * r * np.cos(w) * y1 - r * r * y2
        y2, y1 = y1, v
        y[i] = v
    return y / np.abs(y).max() * np.sin(np.pi * np.linspace(0, 1, n)) ** 2


def tick(f):
    n = int(0.025 * SR)
    return np.sin(2 * np.pi * f * np.arange(n) / SR) * env(n, 0.0005, 0.005)


def blip():  # "voice agent" robot chirp
    out = np.zeros(int(0.5 * SR))
    for a, f in [(0, 660), (0.09, 990), (0.18, 523), (0.27, 1320)]:
        m = int(0.08 * SR)
        sq = np.sign(np.sin(2 * np.pi * f * np.arange(m) / SR)) * env(m, 0.002, 0.04)
        out[int(a * SR) : int(a * SR) + m] += sq
    return out * 0.5


def brass(f, d):
    n = int(d * SR)
    ph = 2 * np.pi * f * np.arange(n) / SR
    return sum(np.sin(k * ph) / k for k in range(1, 12)) * env(n, 0.01, d / 1.8)


for i in (7, 19, 31):  # her messages arrive
    put(fx, pop(700), st[i], 0.6)
for i in (10, 22, 34):  # his messages go out
    put(fx, swoosh(), st[i], 0.35)
    put(fx, pop(1050), st[i] + 0.05, 0.4)
put(fx, blip(), st[34] + 0.5, 0.35)
for i in sorted(enddots):
    put(fx, tick(2400 if i % 2 else 1800), st[i], 0.25)
a, b = st[37], st[55] + 0.2  # riser under the endless typing
n = int((b - a) * SR)
ph = 2 * np.pi * np.cumsum(np.linspace(110, 220, n)) / SR
put(fx, (np.sin(ph) + 0.5 * np.sin(2.02 * ph)) * np.linspace(0, 1, n) ** 2, a, 0.25)
z = st[55]  # dun-dun-DUN
put(fx, brass(mid(43), 0.25), z, 0.35)
put(fx, brass(mid(42), 0.25), z + 0.25, 0.35)
put(fx, brass(mid(38), 1.1), z + 0.5, 0.45)
put(fx, kick(), z + 0.5, 0.8)

mix = mus * 0.7 + fx
fo = int(0.25 * SR)
mix[-fo:] *= np.linspace(1, 0, fo)
save_wav(f"{OUT}/audio.wav", mix)
print(f"babe_voice_agent: {N} frames, {total:.2f} s")
