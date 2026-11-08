"""Audio for Saved to Cloud S1v3.2 (21.5 s, version B extended). Writes s132_mix.wav and s132_sync.json.
The tag (cloud sniff at 20.5 s) is in the mix; the no-tag cut is trimmed at 20.5 s by the build.
Usage: python3 sound_s132.py s132"""
import json
import os
import sys
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

SR = 48000
DUR = 21.5
L = int(DUR * SR)
NF = int(DUR * 30)
rng = np.random.default_rng(32)
which = sys.argv[1] if len(sys.argv) > 1 else "s132"
_KD = os.environ.get("KOKORO_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "models"))
K = Kokoro(os.path.join(_KD, "kokoro-v1.0.int8.onnx"), os.path.join(_KD, "voices-v1.0.bin"))
VOICE = {"PAM": ("bf_emma", 1.05), "DON": ("am_fenrir", 0.88), "DON_Q": ("am_fenrir", 1.0)}


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


def steps(n, gap):
    out = np.zeros(int((n * gap + 0.2) * SR))
    for i in range(n):
        t = tt(0.08)
        b = np.sin(2 * np.pi * 90 * t) * np.exp(-t * 40)
        out[int(i * gap * SR):int(i * gap * SR) + len(b)] += b
    return out


def hic():
    t = tt(0.16)
    f = 500 + 900 * t / 0.16
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / 0.16)


def wobble(d):
    t = tt(d)
    return np.sin(2 * np.pi * 70 * t) * (0.5 + 0.5 * np.sin(2 * np.pi * 9 * t)) * np.sin(np.pi * t / d) * 0.8


def sniff():
    out = np.zeros(int(0.5 * SR))
    for s0 in (0.0, 0.18):
        t = tt(0.12)
        n = lowpass(rng.standard_normal(len(t)), 6) * np.sin(np.pi * t / 0.12)
        out[int(s0 * SR):int(s0 * SR) + len(t)] += n
    return out


def ding(f=1568):
    t = tt(0.4)
    return np.sin(2 * np.pi * f * t) * np.exp(-t * 10)


voice = np.zeros(L)
fx = np.zeros(L)
mus = music(0.0, 11.0)

# 1: DON walks in
add(fx, steps(5, 0.24), 0.0, 0.5)
# 2: slam BACK UP ALL, files fly out, chime
add(fx, click(), 2.6, 1.0)
for i in range(5):
    add(fx, whoosh(0.35, up=False), 2.7 + i * 0.17, 0.25)
add(fx, chime(), 3.85, 0.55)
# 3: the cloud gulps each file
for i, tp in enumerate((4.75, 5.15, 5.55, 5.95)):
    add(fx, puff(220 - 15 * i), tp, 0.55 + 0.08 * i)
add(fx, ding(1175), 6.05, 0.35)
# 4: holding it in, hic, PAM shoves it back and saves again
add(fx, wobble(0.8), 6.55, 0.6)
add(fx, hic(), 7.4, 0.8)
add(fx, rustle(0.3, 60), 7.9, 0.4)
add(fx, whoosh(0.3), 8.25, 0.4)
add(fx, puff(150), 8.55, 0.8)
add(fx, click(), 9.0, 1.0)
add(fx, whoosh(0.25, up=False), 9.05, 0.35)
add(fx, puff(130), 9.25, 0.9)
# 5: ah... ah... ACHOO
add(fx, inhale(0.7), 9.7, 0.55)
add(fx, inhale(0.65), 10.4, 0.75)
add(fx, achoo(), 11.08, 1.15)
add(fx, rustle(3.0, 150), 11.2, 0.55)
# 6: pages still falling
add(fx, rustle(1.8, 40), 12.2, 0.3)
# 7: page slides onto DON's desk, silence, PAM gulps
add(fx, slide(), 14.1, 0.9)
add(fx, gulp(), 16.3, 0.7)
# 8: DON holds the page out, eyebrow
add(fx, rustle(0.3, 50), 17.5, 0.35)
add(fx, ding(2093), 19.6, 0.25)
# 9: tag
add(fx, sniff(), 20.7, 0.8)

lines = [("DON_Q", "Everything backed up?", 1.2), ("PAM", "All backed up!", 2.75),
         ("PAM", "Nice. Shared.", 12.3), ("DON", "Nice. Shared.", 18.5)]
timeline = []
env = {"PAM": np.zeros(NF), "DON": np.zeros(NF)}
for who, txt, t0 in lines:
    a = say(who, txt)
    add(voice, a, t0, 1.0)
    spk = who.split("_")[0]
    timeline.append({"who": spk, "text": txt, "start": t0, "end": round(t0 + len(a) / SR, 3)})
    for f in range(NF):
        s, e = int((f / 30 - t0) * SR), int(((f + 1) / 30 - t0) * SR)
        if e > 0 and s < len(a):
            seg = a[max(0, s):min(e, len(a))]
            if len(seg):
                env[spk][f] = max(env[spk][f], float(np.sqrt(np.mean(seg ** 2))))
for spk in env:
    m = env[spk].max()
    env[spk] = np.clip(env[spk] / (m * 0.6), 0, 1) if m > 0 else env[spk]

venv = lowpass(np.abs(voice), 4800)
duck = 1 - 0.6 * np.clip(venv / (venv.max() + 1e-9) * 4, 0, 1)
room = lowpass(rng.standard_normal(L), 200) * 0.02
mix = fx + 1.25 * voice + mus * duck + room
mix /= np.abs(mix).max() / 0.85
sf.write(f"{which}_mix.wav", mix.astype(np.float32), SR, subtype="FLOAT")
json.dump({"timeline": timeline, "env": {k: [round(float(x), 3) for x in v] for k, v in env.items()}},
          open(f"{which}_sync.json", "w"))
print(which, timeline)
