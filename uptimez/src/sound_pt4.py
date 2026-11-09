"""Audio for Prompt Telephone v04.1. Usage: python3 sound_pt4.py pt4"""
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




def slam():
    t = tt(0.4)
    return (np.sin(2 * np.pi * 70 * t) * np.exp(-t * 14) + lowpass(rng.standard_normal(len(t)), 20) * np.exp(-t * 40) * 2)


def clunk():
    t = tt(0.35)
    s = np.sin(2 * np.pi * 240 * t) * np.exp(-t * 22) + 0.5 * np.sin(2 * np.pi * 410 * t) * np.exp(-t * 30)
    b = np.zeros(len(t)); p = int(0.12 * SR)
    b[p:] = s[:len(t) - p] * 0.35
    return s + b


def pop():
    t = tt(0.08)
    return np.sin(2 * np.pi * (600 + 900 * t / 0.08) * t) * np.exp(-t * 50)


def tick():
    t = tt(0.04)
    return np.sin(2 * np.pi * 3200 * t) * np.exp(-t * 160)


def room(d):
    return lowpass(rng.standard_normal(int(d * SR)), 200) * 0.6




def squeak(d=0.4):
    t = tt(d)
    f = 1400 + 500 * np.sin(t * 40)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-((t - d / 2) / (d / 2.2)) ** 2) * 0.5


def pssht(d=0.35):
    t = tt(d)
    n = np.diff(rng.standard_normal(len(t)), prepend=0)
    return n * np.minimum(1, t * 60) * np.exp(-t * 6) * 0.9


def chime():
    t = tt(0.6)
    return (np.sin(2 * np.pi * 880 * t) + 0.6 * np.sin(2 * np.pi * 1320 * t)) * np.exp(-t * 6) * 0.5


def thud():
    t = tt(0.3)
    return np.sin(2 * np.pi * 80 * t) * np.exp(-t * 18) + lowpass(rng.standard_normal(len(t)), 15) * np.exp(-t * 50)


def blip():
    t = tt(0.15)
    f = 500 + 700 * (t / 0.15)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 12) * 0.5


voice = np.zeros(L)
fx = np.zeros(L)
for v in ("am_fenrir", "am_onyx", "am_michael"):
    try:
        K.create("Test.", voice=v, speed=1.0, lang="en-us")
        VOICE["DON"] = (v, 1.05)
        break
    except Exception:
        continue
VOICE["DON_SOFT"] = (VOICE["DON"][0], 0.85)

plan = [("DON", "Make it bold! Authentic! Viral!", 0.08), ("PAM", "Bold and viral!", 2.05),
        ("RUSH", "Ew. Bold.", 3.55), ("DON_SOFT", "Finally.", 10.9), ("DON_SOFT", "A post about me.", 12.0)]
add(fx, room(15.0), 0.0, 0.05)
add(fx, slam(), 0.3, 0.9)
add(fx, squeak(0.4), 2.15, 0.5)
add(fx, clunk(), 3.2, 0.7)
add(fx, pssht(0.35), 3.65, 0.8)
add(fx, clunk(), 4.7, 0.7)
add(fx, typing(0.45), 5.0, 0.6)
add(fx, chime(), 6.5, 0.8)
add(fx, thud(), 7.6, 1.0)
add(fx, pop(), 8.2, 0.8)
add(fx, blip(), 14.3, 0.7)

lens = {}
for who, txt, t0 in plan:
    a = say(who, txt)
    lens[txt] = (VOICE[who][0], t0, round(t0 + len(a) / SR, 2))
    add(voice, a, t0, 1.0)

mix = fx + 1.2 * voice
mix /= np.abs(mix).max() / 0.85
sf.write(f"{which}_mix.wav", mix.astype(np.float32), SR, subtype="FLOAT")
print(which, lens)
