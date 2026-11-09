"""Audio for the ending variants. Usage: python3 sound2.py s3b|s3c|s1v2 (sound.py is unchanged)"""
import sys
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

SR = 48000
L = 15 * SR
rng = np.random.default_rng(11)
which = sys.argv[1]
import os as _os
_KD = _os.environ.get("KOKORO_DIR", _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "models"))
K = Kokoro(_os.path.join(_KD, "kokoro-v1.0.int8.onnx"), _os.path.join(_KD, "voices-v1.0.bin"))
VOICE = {"RUSH": ("am_adam", 1.15), "PAM": ("bf_emma", 1.0), "MAX": ("am_michael", 1.0)}


def tt(d):
    return np.arange(int(d * SR)) / SR


def lowpass(x, k):
    return np.convolve(x, np.ones(k) / k, mode="same")


def add(buf, sig, t, g=1.0):
    i = int(t * SR)
    n = min(len(sig), L - i)
    if n > 0:
        buf[i:i + n] += sig[:n] * g


def say(who, text):
    v, sp = VOICE[who]
    a, sr = K.create(text, voice=v, speed=sp, lang="en-us")
    a = np.asarray(a, np.float32)
    idx = np.where(np.abs(a) > 0.01)[0]
    a = a[max(0, idx[0] - 200): idx[-1] + 800]
    return np.interp(np.arange(int(len(a) * SR / sr)) * sr / SR, np.arange(len(a)), a)


def creak(d=0.9):
    t = tt(d)
    f = 180 + 120 * np.sin(t * 7) + 60 * np.sin(t * 23)
    ph = 2 * np.pi * np.cumsum(f) / SR
    saw = (ph / (2 * np.pi)) % 1 * 2 - 1
    pulses = (np.sin(2 * np.pi * 38 * t) > 0.6).astype(float)
    return lowpass(saw * pulses, 6) * np.minimum(1, t * 10) * np.minimum(1, (d - t) * 6)


def rustle(d, dens=60):
    out = np.zeros(int(d * SR))
    for _ in range(int(d * dens)):
        p = int(rng.uniform(0, d - 0.05) * SR)
        b = np.diff(rng.standard_normal(int(0.04 * SR)), prepend=0) * np.exp(-tt(0.04) * 60)
        out[p:p + len(b)] += b * rng.uniform(0.2, 0.6)
    return out


def rumble(d):
    t = tt(d)
    n = lowpass(lowpass(rng.standard_normal(len(t)), 60), 60) * 6
    return n * np.sin(np.pi * np.clip(t / d, 0, 1)) ** 0.5


def thunk():
    t = tt(0.9)
    f = 34 + 50 * np.exp(-t * 12)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 4.5)
    imp = lowpass(rng.standard_normal(len(t)), 40) * np.exp(-t * 30) * 3
    return body + imp


def whoosh(d):
    t = tt(d)
    n = lowpass(rng.standard_normal(len(t)), 18)
    return n * (t / d) ** 2 * 3


def typing(d):
    out = np.zeros(int(d * SR))
    tpos = 0.0
    while tpos < d - 0.05:
        b = np.sin(2 * np.pi * 2800 * tt(0.012)) * np.exp(-tt(0.012) * 300)
        b += np.diff(rng.standard_normal(len(b)), prepend=0) * 0.3
        p = int(tpos * SR)
        out[p:p + len(b)] += b * rng.uniform(0.3, 0.6)
        tpos += rng.uniform(0.07, 0.16)
    return out


def click():
    return np.sin(2 * np.pi * 1800 * tt(0.02)) * np.exp(-tt(0.02) * 250)


def cough():
    out = np.zeros(int(0.6 * SR))
    for s0 in (0.0, 0.22, 0.4):
        t = tt(0.16)
        n = lowpass(rng.standard_normal(len(t)), 5) * np.exp(-t * 22)
        tone = np.sin(2 * np.pi * 160 * t) * np.exp(-t * 18) * 0.6
        p = int(s0 * SR)
        out[p:p + len(t)] += (n + tone) * 0.8
    return out


def inhale(d):
    t = tt(d)
    n = lowpass(rng.standard_normal(len(t)), 12) * 1.5
    return n * (t / d) ** 1.5 * np.minimum(1, (d - t) * 30)


def sneeze():
    t1 = tt(0.15)
    ah = lowpass(rng.standard_normal(len(t1)), 10) * np.sin(np.pi * t1 / 0.15) * 0.8
    t2 = tt(0.5)
    choo = (rng.standard_normal(len(t2)) * 0.9 + np.sin(2 * np.pi * 220 * t2) * 0.5) * np.exp(-t2 * 7)
    return np.concatenate([ah, choo])




def whistle(d):
    t = tt(d)
    f = 1700 - 1100 * (t / d)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.minimum(1, t * 8) * 0.6


def steps(n=3, gap=0.18):
    out = np.zeros(int((n * gap + 0.2) * SR))
    for i in range(n):
        t = tt(0.08)
        b = np.sin(2 * np.pi * 90 * t) * np.exp(-t * 40)
        p = int(i * gap * SR)
        out[p:p + len(b)] += b
    return out


def rip():
    t = tt(0.3)
    n = np.diff(rng.standard_normal(len(t)), prepend=0)
    return n * (0.5 + 0.5 * (rng.random(len(t)) > 0.6)) * np.exp(-t * 6) * 0.8


def gulp():
    t = tt(0.25)
    f = 420 - 270 * (t / 0.25)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / 0.25) * 0.8


voice = np.zeros(L)
fx = np.zeros(L)
VOICE["RUSH_FLAT"] = ("am_adam", 1.0)
VOICE["MAX_FAST"] = ("am_michael", 1.12)

if which in ("s3b", "s3c"):
    plan = [("RUSH", "Where's the final?!", 0.05), ("PAM", "Downloads.", 1.2), ("RUSH", "Got it!", 8.4)]
    add(fx, typing(2.0), 0.0, 0.25)
    add(fx, creak(0.9), 2.1, 0.35)
    add(fx, rumble(2.6), 5.0, 0.5)
    add(fx, rustle(2.8, 90), 5.0, 0.35)
    add(fx, rustle(0.4, 40), 8.0, 0.3)
    add(fx, click(), 10.82, 0.9)
    add(fx, whoosh(0.35), 11.2, 0.5)
    add(fx, thunk(), 11.55, 1.0)
    add(fx, rustle(0.5, 80), 11.55, 0.4)
    add(fx, rustle(0.6, 30), 12.5, 0.3)
    if which == "s3b":
        add(fx, click(), 13.32, 0.9)
        add(fx, whistle(1.2), 13.5, 0.35)
        add(fx, thunk(), 14.7, 1.0)
    else:
        add(fx, steps(), 13.2, 0.5)
        plan += [("MAX_FAST", "Where's the final?", 13.25), ("RUSH_FLAT", "Downloads. ", 14.2)]
else:
    plan = [("MAX", "Where's the file?", 0.1), ("PAM", "Cloud.", 1.25),
            ("MAX", "Who's this?", 3.0), ("PAM", "Nice. Shared.", 10.6)]
    add(fx, click(), 0.05, 0.6)
    add(fx, creak(0.5), 2.05, 0.25)
    add(fx, cough(), 4.9, 0.7)
    add(fx, cough(), 5.9, 0.8)
    add(fx, rustle(1.8, 50), 4.9, 0.3)
    add(fx, inhale(1.4), 7.05, 0.6)
    add(fx, sneeze(), 8.45, 1.0)
    add(fx, rustle(1.8, 140), 8.6, 0.55)
    add(fx, rip(), 11.85, 0.7)
    tc = 13.62
    while tc < 14.3:
        add(fx, click(), tc, 0.9)
        tc += 1 / 6
    add(fx, gulp(), 14.45, 0.8)

lens = {}
for who, txt, t0 in plan:
    a = say(who, txt)
    lens[txt] = (t0, round(len(a) / SR, 2), round(t0 + len(a) / SR, 2))
    add(voice, a, t0, 1.0)

mix = fx + 1.2 * voice
mix /= np.abs(mix).max() / 0.85
sf.write(f"{which}_mix.wav", mix.astype(np.float32), SR, subtype="FLOAT")
print(which, lens)
