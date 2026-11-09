"""Audio for Prompt Telephone v04.3: per-word DON clips, corporate music bed, record scratch, voice punch, lip-sync envelopes. Usage: python3 sound_pt43.py pt43"""
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



import json


def sonic_logo():
    out = np.zeros(int(0.9 * SR))
    for i, f in enumerate((660, 880, 1175)):
        t = tt(0.5)
        n = (np.sin(2 * np.pi * f * t) + 0.4 * np.sin(2 * np.pi * f * 2 * t)) * np.exp(-t * 7)
        p = int(i * 0.11 * SR)
        out[p:p + len(n)] += n * 0.5
    return out


def office(d):
    out = room(d) * 0.8
    tpos = 0.3
    while tpos < d - 1.0:
        burst = typing(rng.uniform(0.4, 0.9))
        p = int(tpos * SR)
        out[p:p + len(burst)] += burst * 0.12
        tpos += rng.uniform(1.5, 3.0)
    return out


def marimba(f, d=0.45):
    t = tt(d)
    return (np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * f * 4 * t) * np.exp(-t * 30)) * np.exp(-t * 7)


def music_bed():
    """Cheesy corporate presentation loop, 120 BPM: C G Am F, one chord per second (2 beats).
    15 chords = exactly 30 beats, so it loops on the beat."""
    out = np.zeros(L)
    chords = [(261.6, 329.6, 392.0), (196.0, 246.9, 293.7), (220.0, 261.6, 329.6), (174.6, 220.0, 261.6)]
    for bar in range(15):
        r, th, fi = chords[bar % 4]
        t0 = bar * 1.0
        for i, f in enumerate((r * 2, th * 2, fi * 2, th * 2)):
            add(out, marimba(f), t0 + i * 0.25, 0.22)
        add(out, marimba(r / 2, 0.8) , t0, 0.35)          # bass
        add(out, kick(), t0, 0.35)
        add(out, clap(), t0 + 0.5, 0.25)
        for j in range(8):
            add(out, hat(), t0 + j * 0.125, 0.10)
    return out


def scratch():
    t = tt(0.4)
    f = 900 - 700 * (t / 0.4) + 120 * np.sin(t * 60)
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR)
    n = np.diff(rng.standard_normal(len(t)), prepend=0) * 0.6
    return (tone * 0.6 + n) * np.minimum(1, t * 80) * np.exp(-t * 4)


def kick():
    t = tt(0.3)
    f = 50 + 70 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 10)


def clap():
    t = tt(0.12)
    n = rng.standard_normal(len(t))
    return (n - lowpass(n, 6)) * np.exp(-t * 35) * 0.6


def hat():
    t = tt(0.04)
    return np.diff(rng.standard_normal(len(t)), prepend=0) * np.exp(-t * 90) * 0.3


def whoosh(d=0.25):
    t = tt(d)
    return lowpass(rng.standard_normal(len(t)), 10) * np.sin(np.pi * t / d) * 1.4


def punch(a):
    """Voice punch: gentle presence lift + soft-knee compression."""
    a = a + 0.35 * (a - lowpass(a, 8))
    a = a / (np.abs(a).max() + 1e-9)
    return np.tanh(2.2 * a) / np.tanh(2.2)


voice = np.zeros(L)
fx = np.zeros(L)
music = music_bed()
VOICE["DON"] = ("am_fenrir", 1.22)
VOICE["DON_SOFT"] = ("am_fenrir", 0.85)

plan = [("DON", "Make it bold!", 0.05), ("DON", "Authentic!", 0.78), ("DON", "Viral!", 1.32),
        ("PAM", "Bold and viral!", 2.05), ("RUSH", "Ew. Bold.", 3.55),
        ("DON_SOFT", "Finally.", 11.3), ("DON_SOFT", "A post about me.", 12.35)]
FPS = 30
env = {"DON": np.zeros(450), "PAM": np.zeros(450), "RUSH": np.zeros(450)}
timeline = []
prev_end = 0.0
for who, txt, t0 in plan:
    a = say(who, txt)
    if who == "DON":                      # chain DON's three shouted words back to back, no overlap
        t0 = max(t0, prev_end + 0.04)
    if who.startswith("DON"):
        a = punch(a) * (0.95 if who == "DON" else 0.8)
    add(voice, a, t0, 1.0)
    t1 = t0 + len(a) / SR
    prev_end = t1
    timeline.append({"who": who, "text": txt, "start": round(t0, 3), "end": round(t1, 3)})
    spk = "DON" if who.startswith("DON") else who
    hop = SR // FPS
    for i in range(int(len(a) / hop)):
        f = int(t0 * FPS) + i
        if f < 450:
            env[spk][f] = max(env[spk][f], np.sqrt(np.mean(a[i * hop:(i + 1) * hop] ** 2)))
for spk in env:
    m = env[spk].max()
    if m > 0:
        env[spk] = np.clip(env[spk] / (m * 0.6), 0, 1)

# flying-word cues: on the stressed word of each DON clip
cues = {"BOLD!": timeline[0]["end"] - 0.32, "AUTHENTIC!": timeline[1]["start"] + 0.05, "VIRAL!": timeline[2]["start"] + 0.05}
slam_t = timeline[2]["end"] + 0.06

add(fx, office(15.0), 0.0, 0.2)
for w, tc in cues.items():
    add(fx, whoosh(), tc - 0.05, 0.5)
add(fx, slam(), slam_t, 1.0)
add(fx, thud(), slam_t, 0.8)
add(fx, rustle(0.5, 80), slam_t, 0.4)
add(fx, squeak(0.4), 2.15, 0.5)
add(fx, clunk(), 3.2, 0.7)
add(fx, pssht(0.35), 3.65, 0.8)
add(fx, clunk(), 4.7, 0.7)
add(fx, typing(0.45), 5.0, 0.6)
add(fx, chime(), 6.5, 0.8)
add(fx, thud(), 7.6, 1.0)
add(fx, scratch(), 7.6, 0.8)
add(fx, sonic_logo(), 8.2, 0.9)
for i in range(8):
    add(fx, pop(), 8.65 + i * 0.15, 0.25)
add(fx, blip(), 14.3, 0.7)

# music: dead stop at the NO stab (7.6), back with the chime (8.2); ducked under every voice
mask = np.ones(L)
mask[int(7.6 * SR):int(8.2 * SR)] = 0
fade = int(0.04 * SR)
mask[int(8.2 * SR):int(8.2 * SR) + fade] = np.linspace(0, 1, fade)
venv = lowpass(np.abs(voice), 2400)
venv = venv / (venv.max() + 1e-9)
duck = 1 - 0.7 * np.clip(venv * 3, 0, 1)
mix = 0.55 * music * mask * duck + fx + 1.25 * voice
mix /= np.abs(mix).max() / 0.85
sf.write(f"{which}_mix.wav", mix.astype(np.float32), SR, subtype="FLOAT")
json.dump({"timeline": timeline, "cues": cues, "slam": slam_t,
           "env": {k: [round(float(x), 3) for x in v] for k, v in env.items()}}, open(f"{which}_sync.json", "w"))
print(which, timeline, {k: round(v, 2) for k, v in cues.items()}, "slam", round(slam_t, 2))
