"""The Nine Laws: soundtrack v2 (chords on the cuts, melody fitted per law, lighter mix, new ending). Prophecy score (Dvorak quotes on Vangelis-style synths,
120 BPM felt as 60), SeaShell signature sounds, per-law foley, false triumph at IX,
hard cut, SeaShell voice, motif and loop click. Writes stems + mix.wav (stereo, 48 kHz)."""
import wave

import numpy as np
from scipy.signal import fftconvolve, butter, sosfilt

SR = 48000
T = 45.0
N = int(SR * T)
rng = np.random.default_rng(9)
mid = lambda m: 440.0 * 2 ** ((m - 69) / 12)
BEAT = 0.5  # 120 BPM


# ---------------------------------------------------------------- helpers
def env(n, a, d):
    t = np.arange(n) / SR
    return np.minimum(t / max(a, 1e-5), 1) * np.exp(-t / d)


def adsr(n, a, r, s=1.0):
    e = np.full(n, s)
    na, nr = min(n, int(a * SR)), min(n, int(r * SR))
    e[:na] = np.linspace(0, s, na) ** 1.5
    if nr:
        e[-nr:] *= np.linspace(1, 0, nr) ** 1.5
    return e


def bus():
    return np.zeros((N, 2))


def put(b, sig, t, g=1.0, pan=0.0):
    """Mix mono or stereo sig into stereo bus b at time t. pan -1..1 (mono only)."""
    s = int(round(t * SR))
    if s >= N:
        return
    if sig.ndim == 1:
        l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
        sig = np.stack([sig * l * 1.414, sig * r * 1.414], 1)
    a = max(0, -s)
    s = max(0, s)
    e = min(N, s + len(sig) - a)
    b[s:e] += g * sig[a : a + e - s]


def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], "band", fs=SR, output="sos"), x)


def lp(x, f, order=2):
    return sosfilt(butter(order, f, "low", fs=SR, output="sos"), x)


def hp(x, f, order=2):
    return sosfilt(butter(order, f, "high", fs=SR, output="sos"), x)


def noise(n):
    return rng.normal(0, 1, n)


def ir(dur, decay, pre=0.02, bright=6000, seed=1):
    r = np.random.default_rng(seed)
    n = int(dur * SR)
    t = np.arange(n) / SR
    out = []
    for ch in range(2):
        x = r.normal(0, 1, n) * np.exp(-t / decay)
        x = lp(x, bright)
        x[: int(pre * SR)] = 0
        x[int(pre * SR)] = 0  # predelay
        out.append(x / np.sqrt(np.sum(x**2)))
    return np.stack(out, 1)


def reverb(b, irr, wet):
    out = np.stack([fftconvolve(b[:, c], irr[:, c])[:N] for c in range(2)], 1)
    return b * (1 - wet * 0.3) + out * wet


def load(path):
    w = wave.open(path)
    x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float) / 32768
    return x


# ---------------------------------------------------------------- instruments
def brass(f, dur, swell=0.35, bright=10, detune=(0.0, -0.11, 0.13), harm=28):
    """CS-80-style brass: detuned additive saws with a brightness swell."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    b = 1.5 + (bright - 1.5) * np.minimum(t / swell, 1) ** 0.7  # brightness over time
    vib = 1 + 0.0025 * np.sin(2 * np.pi * 5.2 * t) * np.minimum(t / 0.6, 1)
    out = np.zeros((n, 2))
    for j, dt in enumerate(detune):
        ff = f * 2 ** (dt / 12) * vib
        ph = 2 * np.pi * np.cumsum(ff) / SR + rng.uniform(0, 6.28)
        s = np.zeros(n)
        for k in range(1, harm + 1):
            if f * k > 15000:
                break
            s += np.sin(k * ph) / k * np.exp(-k / b)
        pan = (-0.6, 0.6, 0.0)[j]
        out[:, 0] += s * np.cos((pan + 1) * np.pi / 4)
        out[:, 1] += s * np.sin((pan + 1) * np.pi / 4)
    return out * adsr(n, swell, min(0.6, dur * 0.4))[:, None] * 0.35


def pad(notes, dur, swell=1.2, bright=5):
    out = np.zeros((int(dur * SR), 2))
    for m in notes:
        out += brass(mid(m), dur, swell=swell, bright=bright, harm=14)
    return out / max(1, len(notes)) ** 0.6


def bowed(f, dur, bright=6):
    return brass(f, dur, swell=0.12, bright=bright, detune=(0.0, 0.07), harm=24)


def reed(f, dur):
    """Cor anglais-ish solo: odd-heavy harmonics, delayed vibrato."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    vib = 1 + 0.006 * np.sin(2 * np.pi * 5.0 * t) * np.clip((t - 0.25) / 0.4, 0, 1)
    ph = 2 * np.pi * np.cumsum(f * vib) / SR
    s = sum(np.sin(k * ph) * a for k, a in [(1, 1), (2, 0.35), (3, 0.55), (4, 0.18), (5, 0.3), (7, 0.12)])
    s = bp(s, 250, 4500)
    return s * adsr(n, 0.09, min(0.25, dur * 0.3)) * 0.5


def sub(f, dur, a=0.01, d=0.5):
    n = int(dur * SR)
    t = np.arange(n) / SR
    return np.sin(2 * np.pi * f * t) * env(n, a, d)


def timp(f, g=1.0):
    n = int(1.8 * SR)
    t = np.arange(n) / SR
    fr = f * (1 + 0.08 * np.exp(-t / 0.05))
    ph = 2 * np.pi * np.cumsum(fr) / SR
    s = (np.sin(ph) + 0.5 * np.sin(1.5 * ph) * np.exp(-t / 0.3) + 0.25 * np.sin(1.99 * ph)) * env(n, 0.002, 0.55)
    s += lp(noise(n), 900) * env(n, 0.001, 0.03) * 0.6
    return s * g


def bell(f, d=1.6):
    n = int(d * SR)
    t = np.arange(n) / SR
    return sum(np.sin(2 * np.pi * f * r * t) * np.exp(-t / (d / (1 + i))) * a
               for i, (r, a) in enumerate([(1, 1), (2.76, 0.45), (5.4, 0.25), (8.93, 0.12)]))


# ---------------------------------------------------------------- signature sounds
def shell_breath(dur, rate=0.22, depth=0.8):
    """The sea in a shell: noise through cavity resonances, breathing slowly. Stereo."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    out = np.zeros((n, 2))
    for c in range(2):
        x = noise(n)
        s = sum(bp(x, f * 0.92, f * 1.08, 2) * a for f, a in [(380, 1), (870, 0.8), (1650, 0.5), (2900, 0.3)])
        s += lp(x, 300) * 0.6
        lfo = 1 - depth * 0.5 * (1 + np.cos(2 * np.pi * rate * t + c * 0.4))
        out[:, c] = s * lfo
    return out / np.abs(out).max()


def bug_click():
    """Three dry insect clicks and a small green tink."""
    out = np.zeros(int(0.32 * SR))
    for k, (dt, f) in enumerate([(0, 5200), (0.045, 4600), (0.085, 5800)]):
        m = int(0.012 * SR)
        c = bp(noise(m), f * 0.7, min(f * 1.4, 20000), 2) * env(m, 0.0003, 0.0025)
        put_mono(out, c, dt, 1.0)
    tk = bell(2637, 0.25) * 0.35
    put_mono(out, tk, 0.13, 1.0)
    return out


def put_mono(b, s, t, g):
    i = int(t * SR)
    e = min(len(b), i + len(s))
    b[i:e] += g * s[: e - i]


def skitter(dur, rate=38):
    out = np.zeros(int(dur * SR))
    tt = 0.0
    while tt < dur - 0.01:
        m = int(0.004 * SR)
        put_mono(out, bp(noise(m), 3000, 9000, 2) * env(m, 0.0002, 0.0012), tt, rng.uniform(0.4, 1))
        tt += rng.exponential(1 / rate)
    return out


def stamp(f0, ring=1.0):
    """Stone-tablet impact: thud, grit, gong partials."""
    n = int(2.6 * SR)
    t = np.arange(n) / SR
    fr = f0 * (1 + 0.6 * np.exp(-t / 0.025))
    s = np.tanh(1.6 * np.sin(2 * np.pi * np.cumsum(fr) / SR)) * env(n, 0.001, 0.35)
    s += lp(noise(n), 1800) * env(n, 0.0005, 0.04) * 0.9
    g = sum(np.sin(2 * np.pi * f0 * 2 * r * t) * np.exp(-t / dcy) * a
            for r, dcy, a in [(1, 1.4 * ring, 0.35), (1.47, 1.0 * ring, 0.22), (2.09, 0.7 * ring, 0.16), (2.76, 0.5 * ring, 0.1), (3.98, 0.3 * ring, 0.06)])
    return s + g


def rev_swell(d=0.45):
    n = int(d * SR)
    x = hp(noise(n), 3000) * np.linspace(0, 1, n) ** 3
    return x


def tink(f=2637):
    return bell(f, 0.4)


# ---------------------------------------------------------------- timeline
CUTS = [3.5, 7.5, 11.0, 15.0, 19.0, 23.0, 27.5, 32.29, 36.5]
music, fx, voice, amb = bus(), bus(), bus(), bus()

# ---- 0-3.5 opening: breath, click, faint motif, low E drone
put(amb, shell_breath(4.0, rate=0.3), 0.0, 0.10)
put(music, sub(mid(28), 3.6, a=1.5, d=3.0) * 0.6, 0.0, 0.5)
for k, m in enumerate([76, 83, 88]):  # SeaShell motif, faint glass: E-B-E'
    put(music, bell(mid(m), 2.0) * 0.5, 2.2 + 0.33 * k, 0.12, pan=(-0.3, 0.3, 0)[k])

# ---- Dvorak 4th-movement intro: semitone figure E-F, accelerating, 1.5 -> 7.5
t, step = 1.6, 1.0
while t < 7.45:
    for m, pn in ((40, -0.2), (41, 0.2)):
        if t >= 7.45:
            break
        d = min(step * 0.95, 0.9)
        put(music, bowed(mid(m), d, bright=4 + 6 * (t - 1.6) / 6), t, 0.45 + 0.4 * (t - 1.6) / 6)
        put(music, bowed(mid(m - 12), d, bright=3), t, 0.35)
        t += step
    step = max(0.25, step * 0.82)

# ---- low pulse from Law I: E1 eighths with a heartbeat envelope
def pulse(t0, t1, g=0.4, note=28):
    t = t0
    while t < t1 - 0.01:
        put(music, (sub(mid(note), 0.24, 0.004, 0.08) + 0.3 * sub(mid(note + 12), 0.24, 0.004, 0.05)), t, g)
        t += 0.25


pulse(3.5, 7.5, 0.35)  # Law I: E, under the Dvorak semitone figure

# ---- pads: one chord per law, starting exactly on the card cut (VII: two chords, still on the cut)
Em, C_, Am, B_ = [40, 47, 52, 55, 59], [36, 43, 48, 52, 55], [33, 45, 48, 52, 57], [35, 47, 51, 54, 59]
LAW_PADS = [(7.5, 11.0, [Em]), (11.0, 15.0, [C_]), (15.0, 19.0, [Am]), (19.0, 23.0, [B_]),
            (23.0, 27.5, [Em]), (27.5, 31.79, [C_, B_])]
for a, b, chords in LAW_PADS:
    part = (b - a) / len(chords)
    for j, ch in enumerate(chords):
        t0 = a + j * part
        root = 28 + (ch[0] - 28) % 12                                 # bass follows the chord, kept in E1..D#2
        pulse(t0, t0 + part, 0.45 if t0 < 27.5 else 0.5, note=root)
        put(music, brass(mid(root + 12), 0.5, swell=0.03, bright=6), t0, 0.35)   # clear downbeat on the cut
        put(music, pad(ch, part + 0.3, swell=0.45, bright=4 + (t0 - 7.5) / 6), t0, 0.30 + 0.2 * (t0 - 7.5) / 24)

# ---- Dvorak main theme (approximate), synth brass: Law VI then answer in VII
theme = [(52, 1.0), (54, 0.5), (55, 0.5), (54, 0.5), (52, 0.5), (47, 1.0), (52, 0.5), (54, 0.5), (55, 0.5), (57, 0.5)]
def play(seq, t0, g, inst=brass, oct_=0):
    t = t0
    for m, d in seq:
        put(music, inst(mid(m + oct_), d * 1.05), t, g)
        t += d
    return t


mel = lambda f, d: brass(f, d, swell=0.06, bright=11)  # fast attack: notes land on the beat
phrase_vi = [(52, 1.0), (54, 0.5), (55, 0.5), (54, 0.5), (52, 0.5), (47, 1.0)]               # 4.0 s, ends 27.0
phrase_vii = [(52, 0.5), (54, 0.5), (55, 0.5), (57, 0.5), (59, 1.0), (57, 0.5), (55, 0.5)]   # 4.0 s, ends 31.5
play(phrase_vi, 23.0, 0.55, inst=mel)
play(phrase_vii, 27.5, 0.6, inst=mel)
play([(m - 12, d) for m, d in phrase_vii], 27.5, 0.25, inst=mel)  # quiet low double, same line
for k in range(4):  # timpani on VII's first four downbeats
    put(music, timp(mid(28)), 27.5 + k * 1.0, 0.4 + 0.05 * k)

# ---- VIII: Largo ("Goin' home") solo reed in E major over soft strings
put(music, pad([40, 52, 56, 59], 4.4, swell=0.3, bright=3), 32.29, 0.35)
put(music, brass(mid(40), 0.6, swell=0.03, bright=5), 32.29, 0.35)  # soft defined onset for VIII
largo = [(68, 0.75), (71, 0.25), (71, 1.0), (68, 0.75), (66, 0.25), (64, 1.0)]  # G# B B G# F# E
play(largo, 32.45, 0.55, inst=reed)

# ---- IX: dark drone, then FALSE TRIUMPH from ENTER (38.6) to the hard cut (41.25)
put(music, pad([28, 40, 47], 2.2, swell=0.2, bright=2), 36.5, 0.4)
put(music, brass(mid(40), 0.6, swell=0.03, bright=4), 36.5, 0.4)  # IX onset
tri = [(38.6, [40, 52, 56, 59, 64], 0.6), (39.25, [45, 52, 57, 61, 64], 0.5),
       (39.75, [47, 54, 59, 63, 66], 0.5), (40.25, [40, 52, 56, 59, 64, 68], 1.0)]
for t0, ch, d in tri:
    put(music, pad(ch, d + 0.5, swell=0.15, bright=12), t0, 0.75)
play([(64, 0.65), (68, 0.5), (71, 0.5), (76, 1.0)], 38.6, 0.5)  # rising fanfare line
t = 39.4
while t < 41.2:  # timpani roll crescendo
    put(music, timp(mid(28)), t, 0.15 + 0.5 * (t - 39.4) / 1.8)
    t += 0.07
CUT_AT = 41.25

# ---- 42.5 finale: deep hit, then SeaShell motif low and soft UNDER the voice (E-B-E), Em held
put(music, stamp(41.2) * 1.0, 42.5, 0.9)
put(music, sub(mid(16), 2.4, 0.005, 1.0), 42.5, 0.8)
put(music, timp(mid(28)), 42.5, 0.6)
for k, m in enumerate([40, 47, 52]):
    put(music, brass(mid(m), 2.4 - 0.35 * k, swell=0.3, bright=4), 42.5 + 0.35 * k, 0.4)
put(music, pad([28, 40, 47, 52, 55], 1.8, swell=0.4, bright=3), 43.2, 0.35)

# ---------------------------------------------------------------- SFX
# law stamps, descending by semitone, each with a reverse swell into it
for k, c in enumerate(CUTS):
    put(fx, rev_swell(0.25), c - 0.25, 0.14)
    put(fx, stamp(mid(40 - k), ring=0.55), c, 0.7)

# bug: signature clicks wherever it shows up, plus leg skitter while it moves
for t in (0.08, 4.6, 16.7, 24.9, 29.75, 44.82):
    put(fx, bug_click(), t, 0.5, pan=rng.uniform(-0.3, 0.3))
for a, b_ in ((4.8, 5.9), (6.83, 7.45), (24.95, 26.7)):
    put(fx, skitter(b_ - a), a, 0.35, pan=0.15)

# I: mouse clicks
for t in (4.15, 6.2):
    m = int(0.02 * SR)
    put(fx, bp(noise(m), 1500, 6000) * env(m, 0.0003, 0.003), t, 0.5)

# II: build progress beeps that climb and never finish
t, f, gap = 7.62, 520, 0.25
while t < 10.92:
    m = int(0.06 * SR)
    put(fx, np.sin(2 * np.pi * f * np.arange(m) / SR) * env(m, 0.002, 0.02), t, 0.22)
    t += gap
    f *= 1.045
    gap = max(0.09, gap * 0.95)
put(fx, sub(mid(28), 1.2, 0.002, 0.3) * 0.8, 8.5, 0.6)  # "BUGS ARE ETERNAL." accent

# III: paper rustle as the README unrolls (ticks every 3 frames)
t = 11.12
while t < 14.45:
    m = int(0.05 * SR)
    put(fx, bp(noise(m), 1200, 7000) * env(m, 0.004, 0.015), t, 0.12, pan=rng.uniform(-0.4, 0.4))
    t += 0.125

# IV: crab claws click against the shell, shell resonance swells
for k in range(9):
    m = int(0.03 * SR)
    c = bp(noise(m), 1800, 3200, 4) * env(m, 0.0004, 0.006) + 0.4 * sub(900 + 120 * (k % 3), 0.03, 0.0005, 0.008)
    put(fx, c, 15.25 + k * 0.14 + rng.uniform(0, 0.03), 0.45, pan=0.2)
put(amb, shell_breath(2.5, rate=0.4), 15.0, 0.12)

# V: lamp click, then something big creaking in the shadow
m = int(0.03 * SR)
put(fx, bp(noise(m), 2000, 8000) * env(m, 0.0003, 0.004) + 0.3 * sub(3000, 0.03, 0.0003, 0.005), 19.08, 0.55)
n = int(1.1 * SR)
tt = np.arange(n) / SR
creak = bp(np.sign(np.sin(2 * np.pi * np.cumsum(55 + 25 * np.sin(2 * np.pi * 1.3 * tt)) / SR)) * (0.5 + 0.5 * noise(n) * 0.3), 300, 2500)
put(fx, creak * np.sin(np.pi * np.linspace(0, 1, n)), 20.33, 0.12)

# VI: success chime, then it goes sour as the bug climbs on
def chime(det=0.0):
    out = np.zeros(int(1.6 * SR))
    for k, m in enumerate([76, 80, 83, 88]):
        put_mono(out, bell(mid(m) * 2 ** (det * (k % 2) / 12), 1.2), k * 0.07, 0.4)
    return out


put(fx, chime(), 23.05, 0.4)
put(fx, chime(det=-0.6), 25.6, 0.4)  # detuned: trust no green

# VII: tape rip, slap, two bugs pop out
n = int(0.38 * SR)
rip = bp(noise(n), 800, 9000) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 60 * np.arange(n) / SR + noise(n) * 0.5))) * env(n, 0.005, 0.15)
put(fx, rip, 28.42, 0.45)
put(fx, lp(noise(int(0.08 * SR)), 1500) * env(int(0.08 * SR), 0.0005, 0.02), 28.85, 0.7)
for t, pn in ((30.0, -0.35), (30.45, 0.35)):
    put(fx, sub(500, 0.12, 0.001, 0.03) * np.linspace(1.6, 0.6, int(0.12 * SR)), t, 0.4, pan=pn)
    put(fx, bug_click(), t + 0.05, 0.35, pan=pn)

# VIII: heartbeat slowing to a stop, bones, dust
for t, g in ((32.55, 0.7), (33.25, 0.55), (34.1, 0.35)):
    put(fx, sub(52, 0.25, 0.004, 0.08), t, g)
    put(fx, sub(48, 0.25, 0.004, 0.08), t + 0.17, g * 0.7)
for k in range(6):
    m = int(0.02 * SR)
    put(fx, bp(noise(m), 1500, 5000, 4) * env(m, 0.0003, 0.004), 33.9 + k * 0.08 + rng.uniform(0, 0.03), 0.35)
n = int(0.95 * SR)
grains = np.zeros(n)
for _ in range(220):
    m = int(0.006 * SR)
    put_mono(grains, hp(noise(m), 2500) * env(m, 0.0003, 0.002), rng.uniform(0, 0.9), rng.uniform(0.2, 1))
put(fx, grains * np.linspace(1, 0.3, n), 35.0, 0.35)

# IX: bony hand, ENTER clack, cheerful push-success chime (starts the false triumph)
for k in range(5):
    m = int(0.02 * SR)
    put(fx, bp(noise(m), 1500, 5000, 4) * env(m, 0.0003, 0.004), 37.75 + k * 0.1, 0.35)
m = int(0.06 * SR)
put(fx, bp(noise(m), 600, 4000) * env(m, 0.0005, 0.012) + 0.4 * sub(180, 0.06, 0.0005, 0.02), 38.58, 0.8)
put(fx, chime(), 38.66, 0.35)

put(amb, shell_breath(3.9, rate=0.25), 41.1, 0.16)

# ---------------------------------------------------------------- VOICE
def vline(name, t, g_dry, g_oct, pan=0.0):
    put(voice, load(f"{name}.wav"), t, g_dry, pan)
    put(voice, load(f"{name}_oct.wav"), t, g_oct, pan)


vline("w_they", 0.31, 1.0, 0.35)
vline("w_already", 0.81, 1.0, 0.35)
vline("w_foundyou", 1.31, 1.0, 0.35)
vline("c_line", 41.27, 1.0, 0.7)
vline("c_bugs", 42.72, 1.0, 0.7)  # SeaShell echoes the law in its own words
echo = lp(load("c_bugs.wav")[int(1.30 * SR):], 2500)  # "...remaining" once more, darker, off to the side
put(voice, echo, 42.72 + 1.30 + 0.42, 0.32, pan=0.35)

# ---------------------------------------------------------------- reverbs + mix
cathedral = ir(3.6, 1.1, pre=0.03, bright=5500, seed=3)
shellroom = ir(1.2, 0.18, pre=0.006, bright=3500, seed=5)
music = reverb(music, ir(2.6, 0.75, pre=0.025, bright=5500, seed=11), 0.35)
fx = reverb(fx, ir(2.2, 0.5, seed=7), 0.25)
amb = reverb(amb, cathedral, 0.4)
# HARD CUT at 41.25 (after reverb, so nothing rings into the silence)
c, f = int(CUT_AT * SR), int(0.004 * SR)
for b_ in (music, fx):
    b_[c - f : c] *= np.linspace(1, 0, f)[:, None]
    b_[c : int(42.495 * SR)] = 0

vo_open = voice.copy(); vo_open[int(5 * SR):] = 0
vo_close = voice - vo_open
vo_open = hp(reverb(vo_open, shellroom, 0.35).T, 90).T
vo_close = hp(reverb(reverb(vo_close, shellroom, 0.3), cathedral, 0.45).T, 70).T

# duck music under the opening whisper
duck = np.ones(N)
a, b_ = int(0.25 * SR), int(2.4 * SR)
duck[a:b_] = 0.5
duck[int(42.62 * SR):int(44.9 * SR)] = 0.55
duck = np.convolve(duck, np.ones(2400) / 2400, "same")
music *= duck[:, None]

room = lp(rng.normal(0, 1, (N, 2)), 2000, 1) * 0.0015  # never digital silence
def rms(x, a, b):
    seg = x[int(a * SR):int(b * SR)]
    seg = seg[np.abs(seg).max(1) > 1e-4] if seg.ndim == 2 else seg
    return np.sqrt(np.mean(seg ** 2)) + 1e-9

bed = music * 0.8 + fx * 0.9 + amb * 0.9
ref = rms(bed, 3.5, 32.29)                                   # body of the score
vo_open *= (ref * 1.15) / rms(vo_open, 0.3, 2.3)            # intimate, just over the ducked bed
vo_close *= (ref * 2.0) / rms(vo_close, 41.27, 44.84)       # the oracle: loudest thing in the film
mix = bed + vo_open + vo_close + room
end = int(0.05 * SR)
mix[-end:] *= np.linspace(1, 0.4, end)[:, None]

def save(p, x):
    x = x / max(1e-9, np.abs(x).max()) * 0.89
    w = wave.open(p, "w"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((x * 32767).astype(np.int16).tobytes()); w.close()


peak = np.abs(mix).max()
save("mix_v2.wav", mix)
for nm, s in (("v2_music.wav", music * 0.8), ("v2_fx.wav", fx * 0.9), ("v2_voice.wav", vo_open + vo_close)):
    save(nm, s / peak * np.abs(s).max() / max(1e-9, np.abs(s).max()) if False else s)
print("ok, raw peak", round(float(peak), 3))
