"""Choose Your Career: unpack the four-panel GIF and synthesize its sound effects.

Each panel's sounds are cued from the GIF's own frame start times, so sound and
picture share one clock. Usage: python3 sfx.py <out_dir>
Writes <out_dir>/frames/NNN.png, <out_dir>/list.txt (concat list),
<out_dir>/audio.wav (48 kHz stereo) and <out_dir>/events.json (cue times).
"""
import json
import os
import sys
import wave

import numpy as np
from PIL import Image
from scipy.signal import lfilter

SR = 48000
GIF = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src", "choose_career_reveal.gif")
PAN = [-0.35, -0.12, 0.12, 0.35]  # the four amounts sit left-to-right on screen

out = sys.argv[1] if len(sys.argv) > 1 else "build"
os.makedirs(f"{out}/frames", exist_ok=True)

# ---- frames and timing (panels appear at 0, 1.7, 3.7 and 6.0 s; 10.2 s total)
im = Image.open(GIF)
dur = []
for i in range(im.n_frames):
    im.seek(i)
    im.convert("RGB").save(f"{out}/frames/{i:03d}.png")
    dur.append(im.info["duration"] / 1000)
PANELS = list(np.cumsum([0] + dur[:-1]))
DUR = sum(dur)
with open(f"{out}/list.txt", "w") as f:
    for i, d in enumerate(dur):
        f.write(f"file 'frames/{i:03d}.png'\nduration {d}\n")
    f.write(f"file 'frames/{len(dur) - 1:03d}.png'\n")

# ---- synthesis helpers
rng = np.random.default_rng(7)
buf = np.zeros((int(round(DUR * SR)), 2))


def env(n, a=0.002, d=0.1):
    t = np.arange(n) / SR
    return np.minimum(t / max(a, 1e-5), 1) * np.exp(-t / d)


def add(t, x, g=1.0, pan=0.0):
    """Mix x into the stereo buffer at t seconds with constant-power panning."""
    i = int(t * SR)
    x = x[: len(buf) - i] * g
    th = (pan + 1) * np.pi / 4
    buf[i:i + len(x), 0] += x * np.cos(th) * 1.414
    buf[i:i + len(x), 1] += x * np.sin(th) * 1.414


def lp(x, fc):
    """One-pole low-pass."""
    a = 1 - np.exp(-2 * np.pi * fc / SR)
    return lfilter([a], [1, -(1 - a)], x)


def slam():  # panel lands: low thud plus a short crack
    n = int(0.45 * SR); t = np.arange(n) / SR
    f = 48 + 90 * np.exp(-t / 0.035)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.001, 0.13)
    crack = lp(rng.standard_normal(n), 2500) * env(n, 0.0005, 0.022) * 1.6
    return boom + crack


def stamp(seed=1):  # office rubber stamp, identical every time
    n = int(0.14 * SR); t = np.arange(n) / SR
    noise = np.random.default_rng(seed).standard_normal(n)
    return ((np.sin(2 * np.pi * 185 * t) + 0.4 * np.sin(2 * np.pi * 370 * t)) * env(n, 0.001, 0.028)
            + lp(noise, 1800) * env(n, 0.0005, 0.008))


def coin(f):  # inharmonic bell partials
    n = int(0.55 * SR); t = np.arange(n) / SR; x = np.zeros(n)
    for r, g, d in [(1, 1, 0.16), (1.51, 0.5, 0.11), (2.76, 0.45, 0.07), (4.1, 0.22, 0.04)]:
        x += g * np.sin(2 * np.pi * f * r * t) * env(n, 0.0008, d)
    return x


def knock(f):  # hollow knock on an empty box
    n = int(0.2 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * f * t * (1 - 0.15 * t)) * env(n, 0.001, 0.045)


def register():  # two-note cash-register ding
    x = np.zeros(int(0.8 * SR))
    for off, f, g in [(0, 2093, 1), (0.085, 2637, 1.1)]:
        c = coin(f) * g; i = int(off * SR); x[i:i + len(c)] += c[: len(x) - i]
    return x


def buzz(f):  # "card declined" error buzz
    n = int(0.24 * SR); t = np.arange(n) / SR
    saw = 2 * ((f * t) % 1) - 1
    sq = np.sign(np.sin(2 * np.pi * f * 1.01 * t))
    e = np.minimum(t / 0.004, 1) * np.minimum((t[-1] - t) / 0.03, 1)
    return lp(0.6 * saw + 0.4 * sq, 1700) * e


def horn(dur, f0, f1, bright=2600):  # party horn; a falling sweep makes the deflate
    n = int(dur * SR); t = np.arange(n) / SR
    f = f0 + (f1 - f0) * (t / dur) ** 0.6 + 9 * np.sin(2 * np.pi * 23 * t)
    ph = np.cumsum(f) / SR
    x = 2 * (ph % 1) - 1 + 0.5 * (2 * ((ph * 1.006) % 1) - 1)
    e = np.minimum(t / 0.03, 1) * np.minimum((t[-1] - t) / 0.05, 1)
    return lp(x, bright) * e


# ---- cue sheet
ev = []
for t in PANELS:
    add(t, slam(), 0.55); ev.append(("slam", t))

# EMPLOYEE: four identical stamps, metronome-even
s = stamp()
for k, o in enumerate([0.42, 0.70, 0.98, 1.26]):
    add(PANELS[0] + o, s, 0.5, PAN[k]); ev.append(("stamp", PANELS[0] + o))

# FREELANCER: uneven timing; coin pitch and size follow the amount ($900 $1.5k $500 $2k)
for k, (o, f, g) in enumerate([(0.42, 1320, 0.3), (0.66, 1760, 0.42), (1.14, 1046, 0.2), (1.36, 2093, 0.5)]):
    add(PANELS[1] + o, coin(f), g, PAN[k]); ev.append(("coin", PANELS[1] + o))

# FOUNDER: three hollow knocks for $0, then the $600k payout
for k, o in enumerate([0.42, 0.72, 1.02]):
    add(PANELS[2] + o, knock(150), 0.55, PAN[k]); ev.append(("knock", PANELS[2] + o))
pay = PANELS[2] + 1.4
add(pay, slam(), 0.75, PAN[3]); add(pay, register(), 0.55, PAN[3]); ev.append(("payout", pay))
for _ in range(16):  # coin shower
    tc = pay + 0.1 + 0.5 * rng.random()
    add(tc, coin(rng.uniform(2400, 4200)), 0.1 * (1 - (tc - pay) / 0.7), rng.uniform(-0.1, 0.7))

# VIBE CODER: four falling error buzzes for -$200, party horn, then it deflates
for k, (o, f) in enumerate(zip([0.42, 0.74, 1.06, 1.38], [330, 294, 262, 220])):
    add(PANELS[3] + o, buzz(f), 0.3, PAN[k]); ev.append(("charge", PANELS[3] + o))
hornt = PANELS[3] + 2.0
add(hornt, horn(0.42, 520, 900), 0.3); ev.append(("horn", hornt))
add(hornt + 0.5, horn(0.28, 620, 1040), 0.32); ev.append(("horn2", hornt + 0.5))
add(hornt + 0.95, horn(0.95, 720, 130, 1400), 0.22); ev.append(("deflate", hornt + 0.95))

# ---- master: soft-clip for density, then leave 3 dB headroom before AAC
buf /= np.abs(buf).max()
buf = np.tanh(buf * 4.5)
buf /= np.abs(buf).max()
buf *= 10 ** (-3.0 / 20)
with wave.open(f"{out}/audio.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((buf * 32767).astype(np.int16).tobytes())
with open(f"{out}/events.json", "w") as f:
    json.dump([(e, round(float(t), 3)) for e, t in ev], f, indent=0)
print(f"{len(ev)} cues, {DUR:.1f} s -> {out}/audio.wav")
