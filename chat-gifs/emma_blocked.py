"""Emma Blocked: re-time the iMessage GIF (19.9 s -> 13.2 s) and synthesize its SFX.

Writes build/emma_blocked/{frames/, list.txt, audio.wav}. build.sh does the encode.
"""
import sys

import numpy as np

from common import SR, env, put, save_wav, unpack, write_concat

OUT = sys.argv[1] if len(sys.argv) > 1 else "build/emma_blocked"
N = unpack("src/emma_blocked.gif", OUT)

# Frame roles, read from the source GIF's durations and changed regions.
kind = {}
for i in [*range(1, 13), *range(28, 33), *range(44, 62)]:
    kind[i] = "type"  # user typing into the input field
for i in [*range(17, 25), *range(37, 41)]:
    kind[i] = "dots"  # Emma's typing indicator
for i in (14, 15, 34, 35, 63, 64):
    kind[i] = "send"
for i in (25, 26, 41, 42):
    kind[i] = "recv"
# Reading holds (ms). Punchline (43) and the pause before the block (65) stay long.
hold = {0: 1300, 13: 250, 33: 250, 62: 250, 16: 700, 27: 1250, 36: 600, 43: 1000, 65: 1100, 66: 2600}
step = {"type": 65, "dots": 80}
dur = [hold.get(i, step.get(kind.get(i), 70)) for i in range(N)]
st, total = write_concat(OUT, dur)

rng = np.random.default_rng(7)
out = np.zeros(int(SR * (total + 0.5)))


def key():
    n = int(0.045 * SR)
    t = np.arange(n) / SR
    noise = np.convolve(rng.normal(0, 1, n), [1, -0.9], "same")
    body = np.sin(2 * np.pi * rng.uniform(1700, 2300) * t) * 0.4
    return (noise * 0.5 + body) * env(n, 0.0008, 0.008)


def pop(f0=880, f1=1320):
    n = int(0.22 * SR)
    t = np.arange(n) / SR
    s = np.sin(2 * np.pi * f0 * t) * env(n, 0.002, 0.06) + np.sin(2 * np.pi * f1 * t) * env(n, 0.002, 0.09) * 0.7
    k = int(0.08 * SR)
    s[k:] += np.sin(2 * np.pi * f1 * 1.5 * t[: n - k]) * env(n - k, 0.002, 0.07) * 0.6
    return s


def whoosh():
    n = int(0.35 * SR)
    noise = rng.normal(0, 1, n)
    y = np.zeros(n)
    y1 = y2 = 0.0
    for i in range(n):  # resonator sweeping 600 -> 4000 Hz
        w = 2 * np.pi * (600 + 3400 * i / n) / SR
        r = 0.97
        v = noise[i] + 2 * r * np.cos(w) * y1 - r * r * y2
        y2, y1 = y1, v
        y[i] = v
    return y / np.abs(y).max() * np.sin(np.pi * np.linspace(0, 1, n)) ** 2


def tick():
    n = int(0.03 * SR)
    return np.sin(2 * np.pi * 2600 * np.arange(n) / SR) * env(n, 0.0005, 0.006)


def thud():  # descending double "bonk" for "Emma blocked you."
    n = int(0.9 * SR)
    f = np.linspace(220, 90, n)
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = (np.sin(ph) + 0.35 * np.sin(2 * ph)) * env(n, 0.003, 0.25)
    s += rng.normal(0, 1, n) * env(n, 0.001, 0.02) * 0.4
    k = int(0.16 * SR)
    f2 = np.linspace(160, 70, n - k)
    s[k:] += np.sin(2 * np.pi * np.cumsum(f2) / SR) * env(n - k, 0.003, 0.3)
    return s


put(out, pop(), 0.25, 0.5)  # Emma's angry opener lands
for i in range(N):
    k, t = kind.get(i), st[i]
    if k == "type":
        put(out, key(), t, 0.35)
        put(out, key(), t + 0.032, 0.25)  # several characters per frame
    if i in (14, 34, 63):
        put(out, whoosh(), t, 0.45)
    if k == "dots" and i in (17, 20, 23, 37, 40):
        put(out, tick(), t, 0.25 if i in (17, 37) else 0.12)
    if i in (25, 41):
        put(out, pop(), t, 0.55)
put(out, thud(), st[66], 0.75)

save_wav(f"{OUT}/audio.wav", out, 0.85)
print(f"emma_blocked: {N} frames, {total:.2f} s")
