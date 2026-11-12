"""The Nine Laws, Part 2: "Almost Done." Soundtrack.
Same SeaShell sonic identity (motif, shell_breath, bug_click, skitter, stamp-family),
lighter/quicker/more rhythmic than Nine Laws for this episode's slapstick gags.
Reuses the Nine Laws v2 closing VO take ("Thus spoke SeaShell... Bugs are remaining.")
verbatim over the reused sign-off card. Writes stems + mix.wav (stereo, 48 kHz).
"""
import wave

import numpy as np
from scipy.signal import fftconvolve, butter, sosfilt

SR = 48000
T = 21.333333
N = int(SR * T)
rng = np.random.default_rng(9)
mid = lambda m: 440.0 * 2 ** ((m - 69) / 12)

CUTS = [1.417, 5.25, 6.375, 9.25, 10.25, 14.917, 15.042, 17.833, 18.833]


# ---------------------------------------------------------------- helpers (same palette as Nine Laws)
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
    s = int(round(t * SR))
    if s >= N:
        return
    if sig.ndim == 1:
        l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
        sig = np.stack([sig * l * 1.414, sig * r * 1.414], 1)
    a = max(0, -s)
    s = max(0, s)
    e = min(N, s + len(sig) - a)
    if e <= s:
        return
    b[s:e] += g * sig[a: a + e - s]


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
        x[int(pre * SR)] = 0
        out.append(x / np.sqrt(np.sum(x ** 2)))
    return np.stack(out, 1)


def reverb(b, irr, wet):
    out = np.stack([fftconvolve(b[:, c], irr[:, c])[:N] for c in range(2)], 1)
    return b * (1 - wet * 0.3) + out * wet


def load(path):
    w = wave.open(path)
    x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float) / 32768
    return x


def put_mono(b, s, t, g):
    i = int(t * SR)
    e = min(len(b), i + len(s))
    if e <= i:
        return
    b[i:e] += g * s[: e - i]


# ---------------------------------------------------------------- instruments
def brass(f, dur, swell=0.35, bright=10, detune=(0.0, -0.11, 0.13), harm=28):
    n = int(dur * SR)
    t = np.arange(n) / SR
    b = 1.5 + (bright - 1.5) * np.minimum(t / swell, 1) ** 0.7
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


def bell(f, d=1.6):
    n = int(d * SR)
    t = np.arange(n) / SR
    return sum(np.sin(2 * np.pi * f * r * t) * np.exp(-t / (d / (1 + i))) * a
               for i, (r, a) in enumerate([(1, 1), (2.76, 0.45), (5.4, 0.25), (8.93, 0.12)]))


def sub(f, dur, a=0.01, d=0.5):
    n = int(dur * SR)
    t = np.arange(n) / SR
    return np.sin(2 * np.pi * f * t) * env(n, a, d)


# ---------------------------------------------------------------- signature sounds (from Nine Laws)
def shell_breath(dur, rate=0.22, depth=0.8):
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
    out = np.zeros(int(0.32 * SR))
    for k, (dt, f) in enumerate([(0, 5200), (0.045, 4600), (0.085, 5800)]):
        m = int(0.012 * SR)
        c = bp(noise(m), f * 0.7, min(f * 1.4, 20000), 2) * env(m, 0.0003, 0.0025)
        put_mono(out, c, dt, 1.0)
    tk = bell(2637, 0.25) * 0.35
    put_mono(out, tk, 0.13, 1.0)
    return out


def skitter(dur, rate=38):
    out = np.zeros(int(dur * SR))
    tt = 0.0
    while tt < dur - 0.01:
        m = int(0.004 * SR)
        put_mono(out, bp(noise(m), 3000, 9000, 2) * env(m, 0.0002, 0.0012), tt, rng.uniform(0.4, 1))
        tt += rng.exponential(1 / rate)
    return out


def tink(f=2637):
    return bell(f, 0.4)


# ---------------------------------------------------------------- new, part-2-specific sounds
def chime(variant):
    """Three 'success' states: bright-but-off, hollow, and flat/deflated."""
    if variant == 1:  # FIXED. -- bright, almost convincing, one note a hair flat
        notes, det, d, bright_ = [60, 64, 67, 72], [0, 0, -0.18, 0], 0.55, 9
    elif variant == 2:  # ONE LAST FIX. -- thinner, duller, less resonant
        notes, det, d, bright_ = [58, 63, 67], [0, -0.1, 0], 0.4, 5
    else:  # dawn ONE LAST FIX. -- flat, almost not a chime
        notes, det, d, bright_ = [55, 58], [0, -0.3], 0.3, 2.5
    n = int((d + 0.4) * SR)
    out = np.zeros(n)
    for i, (m, dt) in enumerate(zip(notes, det)):
        f = mid(m + dt)
        t0 = i * 0.05
        put_mono(out, bell(f, d) * (1 - 0.15 * i), t0, 0.5)
    return bp(out, 200, 9000 if variant == 1 else (4000 if variant == 2 else 1800))


def crack_snap():
    """Glass-crack transient for the code splitting."""
    n = int(0.3 * SR)
    t = np.arange(n) / SR
    s = bp(noise(n), 1200, 8000, 3) * env(n, 0.0004, 0.025)
    sweep = np.sin(2 * np.pi * np.cumsum(np.linspace(2200, 300, n)) / SR) * env(n, 0.0003, 0.05)
    return s * 0.7 + sweep * 0.5


def tape_rip(dur=0.55):
    """Sticky tape being pulled and slapped down."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    tear = bp(noise(n), 2500, 9000, 2) * (0.5 + 0.5 * np.sin(2 * np.pi * 26 * t)) ** 2
    tear *= env(n, 0.01, dur * 0.5)
    slap_n = int(0.05 * SR)
    slap = bp(noise(slap_n), 300, 2500, 2) * env(slap_n, 0.0005, 0.02)
    out = tear * 0.6
    put_mono(out, slap, dur - 0.05, 0.9)
    return out


def spawn_ding():
    """Two bugs for the price of one: a doubling, cartoon duplication ding."""
    out = np.zeros(int(0.9 * SR))
    put_mono(out, tink(1760) * 0.6, 0.0, 1.0)
    put_mono(out, tink(2217) * 0.6, 0.11, 1.0)
    return out


def reverse_fill(dur):
    """The bar's own fill-tone, played backward: progress literally undoing."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = np.linspace(900, 160, n)  # falling sweep = undoing (fill-tone reversed)
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = (np.sin(ph) + 0.4 * np.sin(2 * ph) + 0.2 * np.sin(3 * ph)) * adsr(n, 0.3, 0.8, s=0.8)
    s = bp(s, 120, 3500)
    return s


def glitch_tick():
    n = int(0.08 * SR)
    s = bp(noise(n), 2000, 12000, 3) * env(n, 0.0001, 0.01)
    return s


def tick_clock():
    n = int(0.03 * SR)
    return bp(noise(n), 1800, 6000, 2) * env(n, 0.0002, 0.006) * 0.4


# ---------------------------------------------------------------- timeline
music, fx, voice, amb = bus(), bus(), bus(), bus()

# ---- SeaShell's presence throughout: quiet breathing bed, swelling a little at cuts
put(amb, shell_breath(T + 1, rate=0.18), 0.0, 0.09)

# ---- idle bug ticks during the two "ALMOST DONE." shots (0-5.25s)
for t_ in (0.55, 2.1, 3.7):
    put(fx, bug_click(), t_, 0.25)

# ---- night clock-tick texture, sparse, 5.25 -> 17.833 (fades at dawn)
t = 5.6
while t < 17.7:
    g = 0.5 if t < 15 else 0.3
    put(fx, tick_clock(), t, g)
    t += rng.uniform(1.6, 2.6)

# ---- cut 5.25: FIXED. -- bright-but-off chime
put(music, chime(1), 5.25, 0.55)

# ---- cut 9.25: ONE LAST FIX. -- hollower chime
put(music, chime(2), 9.25, 0.5)

# ---- 10.25-14.917: the bug walks the bar backward
put(music, reverse_fill(14.917 - 10.3), 10.3, 0.5)
put(fx, skitter(0.7), 11.55, 0.6)
put(fx, skitter(1.3), 12.45, 0.55)
put(fx, bug_click(), 10.55, 0.3)
put(fx, bug_click(), 14.55, 0.3)

# ---- flash cut 14.917: hard glitch
put(fx, glitch_tick(), 14.917, 0.6)

# ---- 15.042-17.833: FIX ONE. FIND TWO. -- crack, tape, two bugs
put(fx, crack_snap(), 15.06, 0.65)
put(fx, tape_rip(0.55), 15.45, 0.7)
put(fx, skitter(0.9), 16.9, 0.5)
put(music, spawn_ding(), 17.05, 0.45)

# ---- cut 17.833: dawn ONE LAST FIX. -- flattest chime + long exhale
put(music, chime(3), 17.833, 0.45)
put(amb, shell_breath(3.0, rate=0.14), 17.9, 0.14)
put(music, sub(mid(31), 1.0, 0.05, 0.6), 17.95, 0.3)  # soft, deflated low note under the slump

# ---- 18.833-21.333: sign-off card. Motif + reused VO + one bug_click tail.
for k, m in enumerate([76, 83, 88]):  # SeaShell motif, faint glass: E-B-E'
    put(music, bell(mid(m), 1.6) * 0.4, 18.95 + 0.3 * k, 0.1, pan=(-0.3, 0.3, 0)[k])

voice_dry = load("c_bugs.wav")
voice_oct = load("c_bugs_oct.wav")
put(voice, voice_dry, 18.95, 1.0)
put(voice, voice_oct, 18.95, 0.65)
put(fx, bug_click(), 21.02, 0.4)

# ---------------------------------------------------------------- reverbs + mix
cathedral = ir(2.6, 0.9, pre=0.025, bright=5000, seed=3)
music = reverb(music, ir(1.8, 0.55, pre=0.02, bright=5200, seed=11), 0.3)
fx = reverb(fx, ir(1.1, 0.3, seed=7), 0.18)
voice = hp(reverb(voice, cathedral, 0.4).T, 90).T

room = lp(rng.normal(0, 1, (N, 2)), 2000, 1) * 0.0012
def rms(x, a, b):
    seg = x[int(a * SR):int(b * SR)]
    seg = seg[np.abs(seg).max(1) > 1e-4] if seg.ndim == 2 else seg
    return np.sqrt(np.mean(seg ** 2)) + 1e-9

bed = music * 0.85 + fx * 0.9 + amb * 0.9
ref = rms(bed, 5.25, 17.833)
voice *= (ref * 2.1) / rms(voice, 18.95, 21.1)

mix = bed + voice + room
end = int(0.04 * SR)
mix[-end:] *= np.linspace(1, 0.4, end)[:, None]


def save(p, x):
    x = x / max(1e-9, np.abs(x).max()) * 0.89
    w = wave.open(p, "w")
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((x * 32767).astype(np.int16).tobytes())
    w.close()


peak = np.abs(mix).max()
save("mix.wav", mix)
save("stem_music.wav", music * 0.85)
save("stem_fx.wav", fx * 0.9)
save("stem_voice.wav", voice)
print("ok, raw peak", round(float(peak), 3))
