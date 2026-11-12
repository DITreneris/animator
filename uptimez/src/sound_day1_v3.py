"""v3: more sound. The opening is the joke in sound: each BREW press gets a louder click and its own
error, escalating to the full "denied" jingle, over a coffee-maker hum that restarts at the loop reset.
Added foley: Sofía's heels (settling, an impatient toe-tap, weight shifts) and Pam's typing whenever
she types at her desk (it stops dead for her look to camera). Still no music bed, no laugh track.
Lip data is not rewritten (day1_lips.json from v2 stays). Writes day1_mix_v3.wav.

v2 notes: v2 for the animated loop (day1_anim.py): same voices and stings as sound_day1.py, plus
- per-frame mouth openness for lip-sync, written to day1_lips.json;
- a loop ending: the coffee maker resets with the same "denied" beep as 9:00, and every tail wraps
  across the loop point so the join is seamless (no fade in or out).
Writes day1_mix_v2.wav.

v1 notes: Audio for the rough animatic of "How Sofía Survived Day One" (picture = storyboard v3, 25 s).
Voices: Don am_onyx, Sofía af_bella, robot = Don's take pitched up 4 semitones with light metal.
Stings only: no laugh track, no music bed. Everything except the voices is synthesized with numpy.
Usage: python3 sound_day1.py  -> day1_mix.wav"""
import os
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

SR, DUR = 48000, 25.0
L = int(SR * DUR)
rng = np.random.default_rng(11)
KD = os.environ.get("KOKORO_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "models"))
K = Kokoro(os.path.join(KD, "kokoro-v1.0.int8.onnx"), os.path.join(KD, "voices-v1.0.bin"))
DON, SOF = ("am_onyx", 1.0), ("af_bella", 1.0)


def tt(d):
    return np.arange(int(d * SR)) / SR


def add(buf, a, t0, g=1.0):
    i = int(t0 * SR)
    idx = (i + np.arange(len(a))) % L                    # tails wrap across the loop point
    np.add.at(buf, idx, a * g)


def lp(x, n):
    return np.convolve(x, np.ones(n) / n, mode="same")


def noise(d):
    return rng.standard_normal(int(d * SR))


def env(d, a=0.005, r=None):
    t = tt(d)
    r = d if r is None else r
    return np.minimum(1, t / a) * np.exp(-t / r * 4)


# ---------------------------------------------------------------- voices
def say(txt, voice, speed):
    a, sr = K.create(txt, voice=voice, speed=speed, lang="en-us")
    a = np.asarray(a, dtype=np.float64)
    if sr != SR:
        a = np.interp(np.linspace(0, len(a) - 1, int(len(a) * SR / sr)), np.arange(len(a)), a)
    idx = np.where(np.abs(a) > 0.01)[0]
    a = a[max(0, idx[0] - 600):idx[-1] + 2400]
    return a / np.sqrt(np.mean(a ** 2)) * 0.11          # equal RMS per line


def robotize(a, semis=4, ring=0.18, comb=0.35):
    f = 2 ** (semis / 12)
    b = np.interp(np.arange(0, len(a) - 1, f), np.arange(len(a)), a)
    b = b * (1 - ring) + b * np.sin(2 * np.pi * 62 * tt(len(b) / SR)[:len(b)]) * ring * 1.6
    d = int(0.0045 * SR)
    c = b.copy()
    c[d:] += b[:-d] * comb
    c[2 * d:] += b[:-2 * d] * comb * 0.5
    return c / np.sqrt(np.mean(c ** 2)) * 0.10


LINES = [  # (who, text, start, slot end = when its bubble leaves)
    ("DON", "I approve everything.", 3.35, 5.5),
    ("DON", "Trained it myself.", 5.75, 7.4),
    ("DON", "Pam?", 8.05, 9.0),
    ("SOF", "Can you help me?", 12.55, 14.3),
    ("ROB", "Pam?", 15.0, 16.2),
    ("DON", "Perfect.", 16.95, 17.8),
    ("ROB", "Can you help me?", 20.9, 21.8),
    ("SOF", "Pam?", 22.05, 22.8),
]
import json
voice = np.zeros(L)
ends = {}
NF = int(DUR * 30)
lips = {"DON": [0.0] * NF, "SOF": [0.0] * NF, "ROB": [0.0] * NF}
for who, txt, t0, slot in LINES:
    a = say(txt, *(SOF if who == "SOF" else DON))
    if who == "ROB":
        a = robotize(a)
    add(voice, a, t0)
    hop = SR // 30
    e = np.array([np.sqrt(np.mean(a[j:j + hop] ** 2)) for j in range(0, len(a), hop)])
    e = e / e.max()
    for j, v in enumerate(e):
        f = int(round(t0 * 30)) + j
        if f < NF:
            lips[who][f] = round(float(v), 3)
    ends[(who, txt, t0)] = t0 + len(a) / SR
    print(f"{who:4s} {txt:24s} {t0:5.2f} -> {t0 + len(a) / SR:5.2f}  (bubble leaves {slot})", "OK" if t0 + len(a) / SR <= slot + 0.15 else "LATE")


# ---------------------------------------------------------------- effects
def stamp(low=False):
    f = 70 if low else 95
    d = 0.5 if low else 0.32
    t = tt(d)
    a = np.sin(2 * np.pi * f * t * (1 + 0.5 * np.exp(-t * 40))) * np.exp(-t * (9 if low else 16))
    a[:int(0.02 * SR)] += lp(noise(0.02), 6) * 0.5 * np.linspace(1, 0, int(0.02 * SR))
    return a


def tick(f=2400):
    t = tt(0.03)
    return np.sin(2 * np.pi * f * t) * np.exp(-t * 220)


def click():
    t = tt(0.04)
    return (np.sin(2 * np.pi * 1500 * t) * np.exp(-t * 160) + lp(noise(0.04), 4) * np.exp(-t * 260) * 0.6)


def beep(f, d):
    t = tt(d)
    return np.sign(np.sin(2 * np.pi * f * t)) * 0.4 * np.minimum(1, np.minimum(t, d - t) / 0.008)


def swish(d=0.28, f0=900, f1=2600):
    n = noise(d)
    t = tt(d)
    car = np.sin(2 * np.pi * np.cumsum(np.linspace(f0, f1, len(t))) / SR)
    return lp(n, 10) * car * np.sin(np.pi * t / d) ** 2 * 3


def servo(d=0.4, f0=300, f1=520):
    t = tt(d)
    ph = 2 * np.pi * np.cumsum(np.linspace(f0, f1, len(t))) / SR
    return (np.sin(ph) + 0.4 * np.sign(np.sin(ph * 2))) * 0.4 * np.minimum(1, np.minimum(t, d - t) / 0.03)


def pluck(f, d=0.5):
    t = tt(d)
    return (np.sin(2 * np.pi * f * t) + 0.45 * np.sin(4 * np.pi * f * t) * np.exp(-t * 9) +
            0.2 * np.sin(6 * np.pi * f * t) * np.exp(-t * 16)) * np.minimum(1, t / 0.004) * np.exp(-t * 6.5)


def pam_motif(step, resolve=False):
    """Two-note rising bass pluck that asks a question; a step higher each time; the third one resolves."""
    f = 98 * 2 ** (step * 2 / 12)                        # G2, A2, B2
    out = np.zeros(int(1.2 * SR))
    for i, (ff, at) in enumerate(((f, 0.0), (f * 2 ** (5 / 12), 0.17))):
        p = pluck(ff)
        out[int(at * SR):int(at * SR) + len(p)] += p
    if resolve:
        p = pluck(f * 2, 0.7)
        out[int(0.42 * SR):int(0.42 * SR) + len(p)] += p * 0.9
    return out


def woodblock():
    t = tt(0.12)
    return (np.sin(2 * np.pi * 880 * t) + 0.5 * np.sin(2 * np.pi * 2140 * t)) * np.exp(-t * 55)


def bell(f=1560, d=1.3):
    t = tt(d)
    return sum(g * np.sin(2 * np.pi * f * r * t) * np.exp(-t * k) for r, g, k in
               ((1, 1, 4), (2.76, 0.5, 6), (5.4, 0.25, 9), (8.9, 0.12, 14))) * np.minimum(1, t / 0.002)


def triangle():
    t = tt(0.9)
    return sum(np.sin(2 * np.pi * f * t) for f in (3520, 5210, 6880)) / 3 * np.exp(-t * 5) * np.minimum(1, t / 0.002)


def vibra(f=392, d=1.6):
    t = tt(d)
    return (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * f * 4 * t) * np.exp(-t * 8)) * \
        (1 + 0.25 * np.sin(2 * np.pi * 5 * t)) * np.exp(-t * 2.6) * np.minimum(1, t / 0.004)


def rumble(d):
    t = tt(d)
    return lp(noise(d), 160) * 9 * np.sin(np.pi * t / d) ** 0.5 * (1 + 0.5 * np.sin(2 * np.pi * 19 * t))


def chuff(d, rate=7):
    t = tt(d)
    gate = (np.sin(2 * np.pi * rate * t) > 0.2) * np.exp(-((t * rate) % 1) * 5)
    return lp(noise(d), 14) * gate * 2.2


def whistle(d=0.28):
    t = tt(d)
    return (np.sin(2 * np.pi * 1320 * t) + np.sin(2 * np.pi * 1580 * t)) * 0.35 * np.minimum(1, np.minimum(t, d - t) / 0.03)


def pour(d):
    t = tt(d)
    n = lp(noise(d), 22)
    bub = np.sin(2 * np.pi * (240 + 120 * np.sin(2 * np.pi * 9 * t) + 160 * t / d) * t)
    return (n * 4 + bub * 0.25 * (lp(np.abs(noise(d)), 900) * 6)) * np.minimum(1, np.minimum(t, d - t) / 0.06)


def drip():
    t = tt(0.09)
    return np.sin(2 * np.pi * (500 + 2600 * t) * t) * np.exp(-t * 45)


def rustle(d=0.25):
    t = tt(d)
    n = noise(d)
    return (n - lp(n, 6)) * (lp(np.abs(noise(d)), 500) * 5) * np.sin(np.pi * t / d)


def chime():
    out = np.zeros(int(1.1 * SR))
    for i, f in enumerate((523, 659, 784)):
        t = tt(0.7)
        p = np.sin(2 * np.pi * f * t) * np.exp(-t * 5) * np.minimum(1, t / 0.004)
        out[int(i * 0.09 * SR):int(i * 0.09 * SR) + len(p)] += p
    return out


fx = np.zeros(L)
for t0, low in ((0.0, False), (3.0, False), (12.2, False), (20.2, True)):          # clock stamps
    add(fx, stamp(low), t0 + 0.02, 0.55)
    add(fx, tick(1700 if low else 2400), t0 + 0.2, 0.25)
def bzz(f, d):
    """Annoyed error buzz: square wave with a fast wobble."""
    t = tt(d)
    w = np.sign(np.sin(2 * np.pi * f * t + 0.6 * np.sin(2 * np.pi * 31 * t)))
    return w * 0.45 * np.minimum(1, np.minimum(t, d - t) / 0.006)


def hum(d):
    """Coffee maker idling: mains hum, a motor whine and a slow gurgle."""
    t = tt(d)
    g = lp(noise(d), 60) * 6 * (0.5 + 0.5 * np.sin(2 * np.pi * 1.3 * t) ** 8)
    return 0.5 * np.sin(2 * np.pi * 60 * t) + 0.3 * np.sin(2 * np.pi * 120 * t) + 0.06 * np.sin(2 * np.pi * 410 * t) + g * 0.25


def heel(bright=1.0):
    t = tt(0.07)
    n = noise(0.07)
    return (np.sin(2 * np.pi * 2900 * t) * 0.6 * bright + (n - lp(n, 3)) * 1.2 + np.sin(2 * np.pi * 180 * t) * 1.2) * np.exp(-t * 90)


def key(space=False):
    d = 0.05
    t = tt(d)
    n = noise(d)
    if space:
        return (lp(n, 5) * 1.5 + np.sin(2 * np.pi * 220 * t)) * np.exp(-t * 70)
    return ((n - lp(n, 4)) * 1.3 + np.sin(2 * np.pi * rng.uniform(1800, 2600) * t) * 0.4) * np.exp(-t * 140)


# 9:00 opening: three presses, each denial angrier than the last
add(fx, hum(3.5), 24.5, 0.07)                                                      # wraps: 24.5 -> 3.0
for t0, g in ((0.33, 0.55), (1.23, 0.7), (2.03, 0.85)):                            # BREW clicks, firmer each time
    add(fx, click(), t0, g)
add(fx, bzz(150, 0.16), 0.48, 0.16)                                                # 1: one short buzz
add(fx, bzz(175, 0.11), 1.36, 0.19); add(fx, bzz(175, 0.11), 1.52, 0.19)           # 2: two, higher
add(fx, beep(196, 0.11), 2.18, 0.24); add(fx, beep(156, 0.24), 2.33, 0.24)         # 3: the full "denied" jingle
add(fx, bzz(120, 0.3), 2.33, 0.08)                                                 #    with a low raspberry under it

# Sofía's heels: settling at the machine, impatient toe-tap on her eyebrow, weight shifts
for t0, g in ((0.08, 0.30), (0.22, 0.26), (2.55, 0.22), (2.68, 0.22), (2.81, 0.25), (6.45, 0.22), (11.05, 0.24),
              (12.3, 0.26), (12.42, 0.24), (14.45, 0.22), (19.35, 0.22), (20.35, 0.26), (20.48, 0.24), (21.95, 0.26)):
    add(fx, heel(), t0, g)

# Pam's typing: whenever she types at her desk; louder in her own shots, dead stop at her look to camera
krng = np.random.default_rng(5)
for a, b in ((0.0, 8.6), (9.6, 17.8), (20.2, 25.0)):
    t0, n = a, 0
    while t0 < b - 0.05:
        loud = 1.6 if (9.0 <= t0 < 9.6 or 17.0 <= t0 < 17.8) else 1.0
        add(fx, key(space=(n % 7 == 6)), t0, 0.075 * loud * krng.uniform(0.7, 1.1))
        t0 += krng.uniform(0.07, 0.16) + (0.35 if krng.random() < 0.08 else 0)    # bursts with short pauses
        n += 1
add(fx, swish(), 5.82, 0.22)                                                       # Don's tie tug
add(fx, servo(), 6.22, 0.13)                                                       # robot copies it
add(fx, swish(0.35, 600, 1500), 7.8, 0.16)                                         # Don's lazy wave
add(fx, pam_motif(0), ends[("DON", "Pam?", 8.05)] + 0.05, 0.42)
add(fx, rumble(0.42), 9.6, 0.5); add(fx, click(), 10.0, 0.5)                       # partition slides, stops
add(fx, chuff(0.62), 9.9, 0.22); add(fx, whistle(), 10.22, 0.10)                   # the approval train
add(fx, bell(), 10.6, 0.30)
add(fx, woodblock(), 11.65, 0.22)                                                  # Sofía's eyebrow
add(fx, servo(0.3), 14.9, 0.11)                                                    # robot's wave
add(fx, pam_motif(1), ends[("ROB", "Pam?", 15.0)] + 0.05, 0.42)
add(fx, triangle(), ends[("DON", "Perfect.", 16.95)] + 0.02, 0.10)
add(fx, woodblock(), 18.15, 0.3)                                                   # Pam looks at us
add(fx, pour(0.5), 18.95, 0.16)                                                    # thermos
add(fx, vibra(), 19.5, 0.20)
add(fx, servo(0.6, 180, 260), 20.3, 0.10)                                          # robot rolls up
add(fx, rustle(), 20.8, 0.3)
add(fx, pam_motif(2, resolve=True), ends[("SOF", "Pam?", 22.05)] + 0.05, 0.45)
add(fx, chuff(0.3, 9), 22.82, 0.16)
add(fx, bell(), 23.2, 0.30)
add(fx, chime(), 23.3, 0.16)
add(fx, pour(0.85), 23.7, 0.20)
for t0 in (24.2, 24.38):
    add(fx, drip(), t0, 0.2)
add(fx, beep(196, 0.11), 24.5, 0.16); add(fx, beep(156, 0.2), 24.65, 0.16)         # screen resets: denied again, loop

# room tone: office hum, lower in the evening, silent under Pam's look
t = np.arange(L) / SR
room = lp(rng.standard_normal(L), 240) * 0.9 + 0.012 * np.sin(2 * np.pi * 100 * t)
gain = 0.85 - 0.15 * np.clip(np.minimum((t - 20.2) / 0.2, (DUR - t) / 0.2), 0, 1) * (t >= 20.2)   # evening, eased back at the loop
gate = 1 - np.clip(np.minimum(t - 17.8, 18.8 - t) / 0.08, 0, 1)                    # 17.8-18.8 dead air
fade = 1.0                                              # seamless loop: no fade
room = room * gain * gate * fade * 0.05

venv = lp(np.abs(voice), 4800)
duck = 1 - 0.45 * np.clip(venv / 0.05, 0, 1)
mix = voice + fx * duck * 0.7 + room            # effects sit about 3 dB under the first mix
mix = np.tanh(mix * 1.6) / 1.6
mix /= max(1.0, np.max(np.abs(mix)) / 0.85)
sf.write("day1_mix_v3.wav", np.stack([mix, mix], 1), SR)
print("peak", round(float(np.max(np.abs(mix))), 3))
