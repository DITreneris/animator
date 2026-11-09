"""Audio for Saved to Cloud S1v3.1 (A and B share one mix; only shot 5's page differs).
Writes s131_mix.wav and s131_sync.json (line timings + per-speaker 30 fps lip-sync envelopes).
Usage: python3 sound_s131.py s131"""
import json
import os
import sys
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

SR = 48000
L = 15 * SR
rng = np.random.default_rng(31)
which = sys.argv[1] if len(sys.argv) > 1 else "s131"
_KD = os.environ.get("KOKORO_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "models"))
K = Kokoro(os.path.join(_KD, "kokoro-v1.0.int8.onnx"), os.path.join(_KD, "voices-v1.0.bin"))
VOICE = {"PAM": ("bf_emma", 1.05), "DON": ("am_fenrir", 0.88)}


def tt(d):
    return np.arange(int(d * SR)) / SR


def lowpass(x, k):
    return np.convolve(x, np.ones(k) / k, mode="same")


def add(buf, sig, t, g=1.0):
    i = int(t * SR)
    n = min(len(sig), L - i)
    if n > 0:
        buf[i:i + n] += sig[:n] * g


def say(who, txt):
    v, sp = VOICE[who]
    a, sr = K.create(txt, voice=v, speed=sp, lang="en-us")
    a = np.asarray(a, np.float32)
    idx = np.where(np.abs(a) > 0.01)[0]
    a = a[max(0, idx[0] - 200): idx[-1] + 800]
    return np.interp(np.arange(int(len(a) * SR / sr)) * sr / SR, np.arange(len(a)), a)


def click():
    return np.sin(2 * np.pi * 1800 * tt(0.02)) * np.exp(-tt(0.02) * 250)


def whoosh(d, up=True):
    t = tt(d)
    n = lowpass(rng.standard_normal(len(t)), 14)
    env = (t / d) ** 2 if up else np.sin(np.pi * t / d)
    return n * env * 2.5


def puff(f0):
    t = tt(0.32)
    f = f0 * (1 + 0.6 * t / 0.32)
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / 0.32)
    air = lowpass(rng.standard_normal(len(t)), 20) * np.sin(np.pi * t / 0.32) * 0.8
    return tone * 0.7 + air


def inhale(d):
    t = tt(d)
    n = lowpass(rng.standard_normal(len(t)), 10) * 1.6
    tone = np.sin(2 * np.pi * np.cumsum(300 + 500 * t / d) / SR) * 0.25
    return (n + tone) * (t / d) ** 1.4 * np.minimum(1, (d - t) * 30)


def achoo():
    t1 = tt(0.12)
    ah = lowpass(rng.standard_normal(len(t1)), 8) * np.sin(np.pi * t1 / 0.12) * 0.7
    t2 = tt(0.7)
    f = 260 - 120 * t2 / 0.7
    choo = (rng.standard_normal(len(t2)) * 0.9 + np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.6) * np.exp(-t2 * 5)
    return np.concatenate([ah, choo])


def rustle(d, dens=60):
    out = np.zeros(int(d * SR))
    for _ in range(int(d * dens)):
        p = int(rng.uniform(0, d - 0.05) * SR)
        b = np.diff(rng.standard_normal(int(0.04 * SR)), prepend=0) * np.exp(-tt(0.04) * 60)
        out[p:p + len(b)] += b * rng.uniform(0.2, 0.6)
    return out


def slide():
    t = tt(0.45)
    n = lowpass(rng.standard_normal(len(t)), 4) * (1 - t / 0.45) * 0.8
    tap = np.zeros_like(t)
    tap[-int(0.06 * SR):] = np.sin(2 * np.pi * 140 * tt(0.06)) * np.exp(-tt(0.06) * 50)
    return n + tap


def gulp():
    t = tt(0.25)
    f = 420 - 270 * (t / 0.25)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / 0.25) * 0.8


def pluck(f, d=0.35):
    t = tt(d)
    return (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t)) * np.exp(-t * 9)


def chime():
    out = np.zeros(int(0.9 * SR))
    for i, f in enumerate((784, 988, 1319)):
        t = tt(0.5)
        add_at = int(i * 0.11 * SR)
        out[add_at:add_at + len(t)] += np.sin(2 * np.pi * f * t) * np.exp(-t * 6) * 0.5
    return out


def music(t0, t1):
    """Light 120 BPM plucked bed (beat = 0.5 s)."""
    out = np.zeros(L)
    prog = [(262, 330, 392), (220, 262, 330), (175, 220, 262), (196, 247, 294)]
    b = 0
    tb = t0
    while tb < t1 - 0.1:
        ch = prog[(b // 4) % 4]
        add(out, pluck(ch[b % 3] * (2 if b % 2 else 1)), tb, 0.18)
        if b % 2 == 0:
            add(out, pluck(ch[0] / 2, 0.5), tb, 0.22)
        b += 1
        tb += 0.25
    return out


voice = np.zeros(L)
fx = np.zeros(L)
mus = music(0.0, 4.2) + music(6.6, 8.5)

# shot 1: BACK UP ALL
add(fx, click(), 0.12, 0.9)
for i in range(5):
    add(fx, whoosh(0.35, up=False), 0.2 + i * 0.2, 0.25)
add(fx, chime(), 1.35, 0.6)
# shot 2: the cloud swells, PAM / PRIVATE last
for i, (tp, f0) in enumerate(((2.15, 220), (2.55, 200), (2.9, 180), (3.2, 160))):
    add(fx, puff(f0), tp, 0.55 + 0.1 * i)
add(fx, whoosh(0.3), 3.05, 0.4)
# shot 3: ah... ah... ACHOO
add(fx, inhale(0.7), 4.1, 0.55)
add(fx, inhale(0.8), 4.85, 0.7)
add(fx, achoo(), 5.62, 1.1)
add(fx, rustle(2.6, 150), 5.75, 0.55)
# shot 4: pages still falling under PAM's line
add(fx, rustle(2.0, 40), 6.5, 0.3)
# shot 5: the private page slides onto DON's desk, then silence; PAM gulps
add(fx, slide(), 8.6, 0.9)
add(fx, gulp(), 11.15, 0.7)

lines = [("PAM", "All backed up!", 0.3), ("PAM", "Nice. Shared.", 6.95), ("DON", "Nice. Shared.", 12.85)]
timeline = []
env = {"PAM": np.zeros(450), "DON": np.zeros(450)}
for who, txt, t0 in lines:
    a = say(who, txt)
    add(voice, a, t0, 1.0)
    timeline.append({"who": who, "text": txt, "start": t0, "end": round(t0 + len(a) / SR, 3)})
    for f in range(450):
        s, e = int((f / 30 - t0) * SR), int(((f + 1) / 30 - t0) * SR)
        if 0 <= e and s < len(a):
            seg = a[max(0, s):max(0, min(e, len(a)))]
            if len(seg):
                env[who][f] = max(env[who][f], float(np.sqrt(np.mean(seg ** 2))))
for who in env:
    m = env[who].max()
    env[who] = np.clip(env[who] / (m * 0.6), 0, 1) if m > 0 else env[who]

# ducking: music sits under the voice
venv = lowpass(np.abs(voice), 4800)
duck = 1 - 0.6 * np.clip(venv / (venv.max() + 1e-9) * 4, 0, 1)
room = lowpass(rng.standard_normal(L), 200) * 0.02          # faint room tone, no digital silence
mix = fx + 1.25 * voice + mus * duck + room
mix /= np.abs(mix).max() / 0.85
sf.write(f"{which}_mix.wav", mix.astype(np.float32), SR, subtype="FLOAT")
json.dump({"timeline": timeline, "env": {k: [round(float(x), 3) for x in v] for k, v in env.items()}},
          open(f"{which}_sync.json", "w"))
print(which, timeline)
