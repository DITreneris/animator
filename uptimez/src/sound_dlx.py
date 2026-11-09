"""Audio for Downloads Expedition (21.5 s). One script, ENDING A or B (B adds RUSH: "Downloads." in beat 7).
Mixed relative to the measured speech level, not by ear after compression:
music bed -12 dB under speech, room tone -30 dB, effects capped at +3 dB over speech.
Writes dlx_<a|b>_mix.wav, dlx_<a|b>_sync.json (lines + 30 fps lip-sync envelopes) and prints a level report.
Usage: python3 sound_dlx.py A|B"""
import json
import os
import sys
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

ENDING = (sys.argv[1] if len(sys.argv) > 1 else "A").upper()
SR, DUR = 48000, 23.0
L, NF = int(DUR * SR), int(DUR * 30)
rng = np.random.default_rng(41)
_KD = os.environ.get("KOKORO_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "models"))
K = Kokoro(os.path.join(_KD, "kokoro-v1.0.int8.onnx"), os.path.join(_KD, "voices-v1.0.bin"))

LINES = [("PAM", "Where's the final?", 0.6, "bf_emma", 1.1),      # v10: PAM asks (deadpan, still typing)
         ("RUSH", "Hellooo?", 4.1, "am_adam", 0.95),
         ("RUSH", "Got it!", 12.7, "am_adam", 1.15),
         ("MAX", "Got the original?", 17.85, "am_michael", 1.0)]
if ENDING == "B":
    LINES.append(("RUSH", "Downloads.", 19.05, "am_adam", 0.8))


def tt(d):
    return np.arange(int(d * SR)) / SR


def lp(x, k):
    return np.convolve(x, np.ones(k) / k, mode="same")


def rms(x):
    return float(np.sqrt(np.mean(x ** 2)) + 1e-12)


def add(buf, sig, t, g=1.0):
    i = int(t * SR)
    n = min(len(sig), L - i)
    if n > 0:
        buf[i:i + n] += sig[:n] * g


def say(txt, v, sp):
    a, sr = K.create(txt, voice=v, speed=sp, lang="en-us")
    a = np.asarray(a, np.float32)
    idx = np.where(np.abs(a) > 0.01)[0]
    a = a[max(0, idx[0] - 200): idx[-1] + 800]
    return np.interp(np.arange(int(len(a) * SR / sr)) * sr / SR, np.arange(len(a)), a)


# --- effects (unit level; scaled to speech below)
def thud(f=60, d=0.5):
    t = tt(d)
    return (np.sin(2 * np.pi * f * t) + 0.5 * lp(rng.standard_normal(len(t)), 20)) * np.exp(-t * 9)


def creak(d=0.6):
    t = tt(d)
    f = 180 + 60 * np.sin(2 * np.pi * 3 * t)
    return np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.3 * np.sin(np.pi * t / d)


def echo(sig, delays=(0.18, 0.37, 0.6), g=0.45):
    out = np.concatenate([sig, np.zeros(int(0.8 * SR))])
    for i, dl in enumerate(delays):
        j = int(dl * SR)
        out[j:j + len(sig)] += sig * g ** (i + 1)
    return out


def clunk():
    t = tt(0.25)
    return (np.sin(2 * np.pi * 420 * t) * 0.6 + np.sin(2 * np.pi * 160 * t)) * np.exp(-t * 22)


def whizz(d=0.6):
    t = tt(d)
    return lp(rng.standard_normal(len(t)), 6) * np.sin(np.pi * t / d) * (0.5 + 0.5 * t / d)


def drip():
    t = tt(0.18)
    return np.sin(2 * np.pi * np.cumsum(1400 - 800 * t / 0.18) / SR) * np.exp(-t * 30)


def sting():
    t = tt(0.7)
    return sum(np.sin(2 * np.pi * f * t) for f in (311, 370, 466)) / 3 * np.exp(-t * 4)


def snap():
    t = tt(0.06)
    return rng.standard_normal(len(t)) * np.exp(-t * 80)


def rumble(d=1.0):
    t = tt(d)
    return (np.sin(2 * np.pi * 42 * t) + lp(rng.standard_normal(len(t)), 60) * 2) * np.minimum(1, t * 3) * np.exp(-np.maximum(0, t - d + 0.3) * 8)


def paper_roar(d=1.2, dens=220):
    out = np.zeros(int(d * SR))
    for _ in range(int(d * dens)):
        p = int(rng.uniform(0, d - 0.05) * SR)
        b = np.diff(rng.standard_normal(int(0.04 * SR)), prepend=0) * np.exp(-tt(0.04) * 60)
        out[p:p + len(b)] += b * rng.uniform(0.2, 0.6)
    return out * np.exp(-tt(d) * 1.5)


def tada():
    out = np.zeros(int(0.7 * SR))
    for i, f in enumerate((523, 784)):
        t = tt(0.5)
        s = int(i * 0.12 * SR)
        out[s:s + len(t)] += (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t)) * np.exp(-t * 5)
    return out


def pop():
    t = tt(0.08)
    return np.sin(2 * np.pi * np.cumsum(500 + 900 * t / 0.08) / SR) * np.exp(-t * 30)


def steps(n, gap):
    out = np.zeros(int((n * gap + 0.2) * SR))
    for i in range(n):
        t = tt(0.06)
        b = np.sin(2 * np.pi * 110 * t) * np.exp(-t * 50)
        out[int(i * gap * SR):int(i * gap * SR) + len(b)] += b
    return out


def bones():
    out = np.zeros(int(0.5 * SR))
    for i, f in enumerate((1200, 900, 1500, 1050)):
        t = tt(0.07)
        b = np.sin(2 * np.pi * f * t) * np.exp(-t * 60)
        out[int(i * 0.08 * SR):int(i * 0.08 * SR) + len(b)] += b
    return out


def whomp():
    t = tt(0.35)
    return np.sin(2 * np.pi * np.cumsum(180 - 120 * t / 0.35) / SR) * np.exp(-t * 10)


def chime():
    out = np.zeros(int(0.9 * SR))
    for i, f in enumerate((784, 988, 1319)):
        t = tt(0.5)
        a = int(i * 0.11 * SR)
        out[a:a + len(t)] += np.sin(2 * np.pi * f * t) * np.exp(-t * 6) * 0.5
    return out


def click():
    return np.sin(2 * np.pi * 1800 * tt(0.02)) * np.exp(-tt(0.02) * 250)


def whistle(d=0.35):
    t = tt(d)
    return np.sin(2 * np.pi * np.cumsum(1800 - 1300 * t / d) / SR) * 0.5


def pluck(f, d=0.35):
    t = tt(d)
    return (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t)) * np.exp(-t * 9)


def music(t0, t1):
    out = np.zeros(L)
    prog = [(262, 330, 392), (220, 262, 330), (175, 220, 262), (196, 247, 294)]
    b, tb = 0, t0
    while tb < t1 - 0.1:
        ch = prog[(b // 4) % 4]
        add(out, pluck(ch[b % 3] * (2 if b % 2 else 1)), tb, 0.5)
        if b % 2 == 0:
            add(out, pluck(ch[0] / 2, 0.5), tb, 0.6)
        b += 1
        tb += 0.25
    return out


def drone(t0, t1):
    out = np.zeros(L)
    n = int((t1 - t0) * SR)
    t = np.arange(n) / SR
    d = (np.sin(2 * np.pi * 55 * t) + 0.5 * np.sin(2 * np.pi * 82.5 * t)) * 0.3 + lp(rng.standard_normal(n), 300) * 2
    d *= np.minimum(1, t * 2) * np.minimum(1, (n / SR - t) * 4)
    out[int(t0 * SR):int(t0 * SR) + n] = d
    return out


# --- voices first: these set the reference level
voice = np.zeros(L)
timeline, env = [], {"RUSH": np.zeros(NF), "MAX": np.zeros(NF), "PAM": np.zeros(NF)}
for who, txt, t0, v, sp in LINES:
    a = say(txt, v, sp)
    if who == "MAX":
        a = a * 1.5          # MAX's voice model is quieter; match RUSH
    if txt == "Downloads.":
        a = a * 0.9
    dry = a                                        # lip-sync follows the dry voice, not the echo
    if txt == "Hellooo?":
        a = echo(a * 0.9, delays=(0.22, 0.45, 0.7), g=0.5)     # the cave answers
    add(voice, a, t0)
    timeline.append({"who": who, "text": txt, "start": t0, "end": round(t0 + len(a) / SR, 3)})
    line_env = np.zeros(NF)                       # each line normalised on its own, so adding a line
    for f in range(NF):                            # (ending B) never changes another line's mouth
        s, e = int((f / 30 - t0) * SR), int(((f + 1) / 30 - t0) * SR)
        if e > 0 and s < len(dry):
            seg = dry[max(0, s):min(e, len(dry))]
            if len(seg):
                line_env[f] = rms(seg)
    env[who] = np.maximum(env[who], np.clip(line_env / (line_env.max() * 0.6), 0, 1))
speech = rms(np.concatenate([voice[int(l["start"] * SR):int(l["end"] * SR)] for l in timeline]))

fx = np.zeros(L)
FX = [  # (signal, time, dB relative to speech RMS)
    (thud(55, 0.6), 0.0, -10), (whizz(0.45), 0.0, -6), (pop(), 0.12, -14), (pop(), 1.6, -14),
    (creak(0.2), 2.2, -10), (echo(drip()), 2.9, -8),
    (clunk(), 3.1, -2), (whizz(0.6), 3.5, -8), (whizz(0.25), 3.9, -8), (echo(drip()), 4.6, -12),
    (whizz(0.6), 5.0, -12), (sting(), 5.6, -4), (pop(), 5.85, -14), (snap(), 7.05, -8), (drip(), 8.3, -10),
    (whizz(0.2), 9.0, -6), (whizz(0.2), 9.6, -16), (whizz(0.2), 9.8, -16), (rumble(1.0), 9.8, 0), (paper_roar(1.4), 10.45, 0), (thud(70, 0.4), 10.98, 0),
    (tada(), 12.5, -4), (click(), 14.2, -2), (whistle(0.35), 14.6, -6), (thud(45, 0.7), 14.95, +3),
    (paper_roar(0.6, 60), 15.0, -10), (whizz(0.3), 15.0, -14), (steps(5, 0.14), 16.2, -12), (click(), 16.6, -8), (click(), 19.05, -14),
    (drip(), 19.45, -12), (click(), 20.0, -16), (click(), 20.1, -16), (pop(), 20.2, -8), (whizz(0.3), 19.9, -12), (clunk(), 20.55, -10), (steps(4, 0.17), 20.8, -12), (creak(0.15), 21.55, -10), (thud(55, 0.6), 21.7, -2),
    # v4: footsteps on the sprint, rope creak, bones, impact whomps, kinetic pops, the tower
    (steps(4, 0.1), 0.0, -8), (creak(0.9), 4.0, -16), (bones(), 5.6, -6), (whomp(), 5.6, -4), (pop(), 8.6, -12),
    (pop(), 13.55, -12), (whomp(), 14.95, -2), (whizz(0.35), 21.9, -6), (chime(), 22.0, -8),
    (rumble(0.45), 22.3, -2), (pop(), 22.5, -6), (whizz(0.5), 22.5, -8),
]
for sig, t0, db in FX:
    add(fx, sig / rms(sig[:int(0.3 * SR)]) * speech * 10 ** (db / 20), t0)
bed = music(0.0, 2.9) + music(10.9, 13.4)
bed = bed / rms(bed[bed != 0]) * speech * 10 ** (-16 / 20)
cave = drone(2.9, 10.5)
cave = cave / rms(cave[int(3.5 * SR):int(10 * SR)]) * speech * 10 ** (-24 / 20)
room = lp(lp(rng.standard_normal(L), 120), 40)
room = room / rms(room) * speech * 10 ** (-30 / 20)
venv = lp(np.abs(voice), 4800)
duck = 1 - 0.5 * np.clip(venv / (venv.max() + 1e-9) * 4, 0, 1)
mix = voice + fx + (bed + cave) * duck + room
mix = mix / np.abs(mix).max() * 0.89
tag = ENDING.lower()
# film-time cuts (same as dlx.CUTS): 0.6 s at the pile start, 0.6 s of the wide hold; sync json stays in film time
CUTS = [(8.0, 0.6), (15.5, 0.6)]
xf = int(0.02 * SR)
cut_mix = mix
for at, d in reversed(CUTS):                         # from the end, so earlier sample positions stay valid
    a, b = int(at * SR), int((at + d) * SR)
    cut_mix = np.concatenate([cut_mix[:a], cut_mix[b:]])
    cut_mix[a - xf:a + xf] *= np.concatenate([np.linspace(1, 0.6, xf), np.linspace(0.6, 1, xf)])
sf.write(f"dlx_{tag}_mix.wav", cut_mix.astype(np.float32), SR, subtype="FLOAT")
json.dump({"timeline": timeline, "env": {k: [round(float(x), 3) for x in v] for k, v in env.items()}},
          open(f"dlx_{tag}_sync.json", "w"))
ref = rms(mix[int(0.6 * SR):int(1.4 * SR)])
for name, a, b in (("speech RUSH", 0.6, 1.4), ("cave drone", 4.0, 5.0), ("after salute", 7.6, 8.2),
                   ("avalanche", 10.5, 11.3), ("wide hold", 16.7, 17.8), ("speech MAX", 17.85, 18.9), ("tower", 22.0, 22.9)):
    print(f"{name:22s} {20 * np.log10(rms(mix[int(a * SR):int(b * SR)]) / ref):+6.1f} dB vs speech")
print(ENDING, timeline)
