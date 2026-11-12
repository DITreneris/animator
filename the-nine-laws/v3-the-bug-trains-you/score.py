"""The Nine Laws, Part 3: "The Bug Trains You." Soundtrack.
David Lynch's Rabbits treatment of SeaShell's world: a continuous tide (the "rain"),
one distant foghorn (the "train whistle"), long dead silences, and a synthetic
audience laugh track that fires at the least funny moments -- never at the
two beats that actually resemble jokes. SeaShell's own voice (ElevenLabs reads of
the title cards, processed through the same dry+octave-down+reverb chain as
every other episode) narrates the cards as flat stage directions. The missing
"Act 2" gets a half-second of true silence instead of a sound. Same SeaShell
motif, same reused sign-off take as always. Writes stems + mix.wav (stereo, 48kHz).
"""
import wave

import numpy as np
from scipy.signal import fftconvolve, butter, sosfilt

SR = 48000
T = 30.041667
N = int(SR * T)
rng = np.random.default_rng(13)
mid = lambda m: 440.0 * 2 ** ((m - 69) / 12)

CUTS = [1.333, 4.333, 5.792, 8.792, 11.792, 13.292, 14.875, 17.208, 19.875, 22.542, 25.208, 27.542]


# ---------------------------------------------------------------- helpers (same palette as the series)
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


def duck(b, t0, t1, depth=0.45, fade=0.05):
    """Sidechain-style gain dip over b in [t0, t1], so another element (voice,
    laugh, foghorn) can cut through the bed instead of fighting it."""
    s0, s1 = int(t0 * SR), int(t1 * SR)
    s0, s1 = max(0, s0), min(N, s1)
    if s1 <= s0:
        return
    fs = min(int(fade * SR), (s1 - s0) // 2)
    core = np.full(s1 - s0, 1 - depth)
    if fs > 0:
        core[:fs] = np.linspace(1, 1 - depth, fs)
        core[-fs:] = np.linspace(1 - depth, 1, fs)
    b[s0:s1] *= core[:, None]


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


def bell(f, d=1.6):
    n = int(d * SR)
    t = np.arange(n) / SR
    return sum(np.sin(2 * np.pi * f * r * t) * np.exp(-t / (d / (1 + i))) * a
               for i, (r, a) in enumerate([(1, 1), (2.76, 0.45), (5.4, 0.25), (8.93, 0.12)]))


def sub(f, dur, a=0.01, d=0.5):
    n = int(dur * SR)
    t = np.arange(n) / SR
    return np.sin(2 * np.pi * f * t) * env(n, a, d)


# ---------------------------------------------------------------- signature sounds (from the series)
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


# ---------------------------------------------------------------- Part-3-specific sounds
def tide(dur, rate=0.08):
    """The ocean, standing in for Rabbits' endless rain: a continuous, barely-there swell."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    out = np.zeros((n, 2))
    for c in range(2):
        x = noise(n)
        s = lp(x, 900) + 0.5 * bp(x, 150, 500, 2)
        lfo = 0.55 + 0.45 * (1 + np.sin(2 * np.pi * rate * t + c * 1.1)) / 2
        out[:, c] = s * lfo
    return out / np.abs(out).max()


def foghorn(dur=2.2, f0=88):
    """Low enough to sit under the tide, but with a second harmonic poked up
    and brightened so it still reads as an event on small speakers, not just
    extra rumble."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    vib = 1 + 0.004 * np.sin(2 * np.pi * 3.1 * t)
    fund = np.sin(2 * np.pi * f0 * vib * t)
    second = np.sin(2 * np.pi * f0 * 2 * vib * t) * 0.55
    third = np.sin(2 * np.pi * f0 * 3 * vib * t) * 0.22
    s = (fund + second + third) * adsr(n, 0.3, 1.0, s=0.9)
    s = lp(s, 650)
    return s * 1.3


def laugh(dur=1.3, voices=3, seed=0):
    """Synthetic, deliberately artificial audience laughter -- not a real recording
    (none used, none licensed), built as a row of voiced "ha" syllables: two
    stacked vowel-formant resonances per burst with a quick pitch-sag, not just
    banded noise. Its artificiality is the point -- an obviously fake laugh
    track is more unsettling than a real one would be, but it has to actually
    read as laughing, not as static."""
    r = np.random.default_rng(seed)
    n = int(dur * SR)
    out = np.zeros((n, 2))
    for v in range(voices):
        rate = r.uniform(3.6, 4.6)          # distinct "ha" pulses, not a buzz
        f0 = r.uniform(170, 260)            # voiced pitch, not hiss
        pan = r.uniform(-0.6, 0.6)
        delay = r.uniform(0, 0.12)
        tt = delay
        ch = np.zeros(n)
        while tt < dur - 0.02:
            m = int(r.uniform(0.11, 0.16) * SR)
            tb = np.arange(m) / SR
            sag = f0 * (1.0 - 0.3 * tb / (m / SR))  # pitch drops through each "ha"
            buzz = np.sign(np.sin(2 * np.pi * np.cumsum(sag) / SR))  # raspy voiced source
            burst = bp(buzz, 400, 1100, 2) * 0.8 + bp(buzz, 1800, 3200, 2) * 0.35
            burst *= env(m, 0.01, 0.065)
            put_mono(ch, burst, tt, r.uniform(0.75, 1.0))
            tt += 1 / rate * r.uniform(0.85, 1.15)
        amp_shape = adsr(n, 0.06, dur * 0.6, s=1.0)
        l, rr = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
        out[:, 0] += ch * amp_shape * l
        out[:, 1] += ch * amp_shape * rr
    return out / np.abs(out).max() * 0.85


def ui_blip(f=1800, up=True):
    n = int(0.09 * SR)
    t = np.arange(n) / SR
    sweep = np.linspace(f, f * (1.6 if up else 0.6), n)
    s = np.sin(2 * np.pi * np.cumsum(sweep) / SR) * env(n, 0.001, 0.03)
    return s


def autocomplete_tick(dur, rate=14):
    out = np.zeros(int(dur * SR))
    tt = 0.0
    while tt < dur - 0.01:
        m = int(0.006 * SR)
        f = rng.uniform(2800, 4200)
        put_mono(out, bp(noise(m), f * 0.8, f * 1.3, 2) * env(m, 0.0003, 0.003), tt, rng.uniform(0.3, 0.7))
        tt += 1 / rate * rng.uniform(0.7, 1.3)
    return out


def heartbeat_beep(f=1100):
    n = int(0.12 * SR)
    t = np.arange(n) / SR
    return np.sin(2 * np.pi * f * t) * env(n, 0.001, 0.045) * 0.6


def flatline_tone(dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    return np.sin(2 * np.pi * 900 * t) * adsr(n, 0.02, dur * 0.3, s=0.55)


def power_down(dur=0.9):
    n = int(dur * SR)
    f = np.linspace(400, 60, n)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * env(n, 0.005, dur * 0.4) * 0.6


def splash(dur=0.5):
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = bp(noise(n), 200, 3500, 2) * env(n, 0.002, 0.12)
    s += lp(noise(n), 400) * env(n, 0.005, 0.25) * 0.5
    return s


def press_thunk():
    n = int(0.12 * SR)
    s = bp(noise(n), 150, 1200, 2) * env(n, 0.0005, 0.03)
    s += sub(140, 0.12, 0.001, 0.05) * 0.6
    return s


VOICE_DUR = {  # trimmed-clip durations, for ducking the bed under each line
    "reward": 0.65, "good_developer": 0.839, "still_on_call": 0.992,
    "permission_to_rest": 1.417, "who_trained_whom": 1.130, "thus_spoke": 2.706,
}


def vline(bus_, name, t, g_dry=1.0, g_oct=0.6, pan=0.0):
    put(bus_, load(f"{name}_trim.wav"), t, g_dry, pan)
    put(bus_, load(f"{name}_oct.wav"), t, g_oct, pan)
    for b_ in (music, fx, amb):
        duck(b_, t - 0.05, t + VOICE_DUR.get(name, 1.0) + 0.15, depth=0.55, fade=0.08)


# ---------------------------------------------------------------- timeline
music, fx, voice, amb = bus(), bus(), bus(), bus()

# ---- the tide: continuous, under everything
put(amb, tide(T + 1), 0.0, 0.11)

# ===================== ACT 1: REWARD. (0 - 5.792) =====================
# idle desk ambience, bug sits by the button
for t_ in (0.4, 1.0):
    put(fx, bug_click(), t_, 0.22)
# the press (insert, 1.333-4.333): X -> check
put(fx, ui_blip(1600, up=True), 1.85, 0.55)
put(music, tink(2093) * 0.4, 1.95, 0.4)
# cut back to wide (4.333): the sip -- SeaShell states the card as the reward lands
vline(voice, "reward", 4.48, 1.1, 0.32)
put(music, bell(mid(76), 1.2) * 0.3, 4.5, 0.12)
# laugh #1: right after the sip, bleeding across the hard cut into the law-card
for b_ in (music, amb):
    duck(b_, 5.5, 7.05, depth=0.65, fade=0.1)
put(fx, laugh(1.7, voices=4, seed=1), 5.55, 1.35)

# ===================== interstitial: TRUST NO GREEN. (5.792 - 8.792) =====================
put(amb, shell_breath(3.2, rate=0.2), 5.9, 0.12)
put(music, bell(mid(43), 2.2) * 0.5, 6.9, 0.18)
put(music, bell(mid(50), 1.8) * 0.4, 7.15, 0.14)

# ---- the missing Act 2: a true half-second of silence right on the cut
GAP = 8.792
gs, ge = int((GAP - 0.05) * SR), int((GAP + 0.35) * SR)
for b_ in (music, fx, amb):
    b_[gs:ge] *= 0.0

# ===================== ACT 3: GOOD DEVELOPER. (8.792 - 14.875) =====================
vline(voice, "good_developer", 8.95, 1.1, 0.32)
for t_ in (9.6, 10.4, 10.9):
    put(fx, bug_click(), t_, 0.18)
# insert (11.792-13.292): bug hops off, cursor creeps in -- no reward chime this time
put(fx, ui_blip(900, up=False), 12.05, 0.4)
put(fx, skitter(0.5), 11.85, 0.4)
# wide (13.292-14.875): reaching for the keyboard, mug untouched -- flat, denied
put(music, sub(mid(28), 0.8, 0.02, 0.4), 13.4, 0.2)

# ===================== STILL ON CALL. triptych (14.875 - 22.542) =====================
vline(voice, "still_on_call", 15.0, 1.1, 0.32)
# ambulance #1 (14.875-17.208): steady monitor beep, distant wheels/radio murmur
t = 15.3
while t < 17.1:
    put(fx, heartbeat_beep(1100), t, 0.3)
    t += 0.85
put(amb, lp(noise(int(2.3 * SR)), 1200) * 0.03, 14.9, 1, pan=-0.3)

# ONE LAST FIX / autocomplete / FIX press (17.208-19.875)
put(fx, autocomplete_tick(1.6), 18.1, 0.45)
put(fx, skitter(0.6), 18.2, 0.35)
put(fx, press_thunk(), 19.55, 0.7)
put(music, bp(noise(int(0.3 * SR)), 300, 2200, 2) * env(int(0.3 * SR), 0.001, 0.08), 19.56, 0.35)

# the claw / gray X (19.875-22.542)
put(fx, splash(0.6), 20.7, 0.5)
put(fx, power_down(), 20.85, 0.6)
put(amb, shell_breath(2.6, rate=0.16), 19.95, 0.18)
duck(amb, 20.1, 21.6, depth=0.45, fade=0.12)
put(fx, foghorn(1.3, f0=88), 20.1, 0.6, pan=-0.3)
put(music, sub(mid(21), 2.0, 0.3, 1.2), 20.9, 0.3)
# laugh #2: right after the claw breaks the surface
duck(music, 21.5, 23.2, depth=0.65, fade=0.1)
duck(amb, 21.5, 23.2, depth=0.65, fade=0.1)
put(fx, laugh(1.6, voices=4, seed=2), 21.55, 1.35)

# ===================== PERMISSION TO REST. (22.542 - 25.208) =====================
vline(voice, "permission_to_rest", 22.68, 1.1, 0.32)
put(amb, shell_breath(2.6, rate=0.12), 22.6, 0.2)
for k, m in enumerate([76, 83, 88]):  # the motif, arriving early and soft -- foreshadowing the sign-off
    put(music, bell(mid(m), 1.8) * 0.3, 23.9 + 0.3 * k, 0.07, pan=(-0.2, 0.2, 0)[k])

# ===================== WHO TRAINED WHOM? (25.208 - 27.542) =====================
# ambulance #2: same scoring as #1 at first, then the flatline
t = 25.4
while t < 26.3:
    put(fx, heartbeat_beep(1100), t, 0.3)
    t += 0.85
vline(voice, "who_trained_whom", 25.35, 1.1, 0.35)
put(fx, flatline_tone(1.1), 26.35, 0.42)
# laugh #3: right after the question lands, bleeding into the cut to the sign-off
duck(music, 26.5, 28.3, depth=0.65, fade=0.1)
duck(amb, 26.5, 28.3, depth=0.65, fade=0.1)
put(fx, laugh(1.8, voices=4, seed=3), 26.55, 1.35)

# ===================== sign-off (27.542 - 30.042) =====================
for k, m in enumerate([76, 83, 88]):
    put(music, bell(mid(m), 1.5) * 0.4, 27.68 + 0.28 * k, 0.1, pan=(-0.3, 0.3, 0)[k])
vline(voice, "thus_spoke", 27.75, 1.1, 0.38)
# no closing bug-click here -- this episode ends on SeaShell's line and the tide, not a bug sound

# ---------------------------------------------------------------- reverbs + mix
cathedral = ir(2.0, 0.7, pre=0.02, bright=6000, seed=3)
music = reverb(music, ir(1.8, 0.55, pre=0.02, bright=5200, seed=11), 0.25)
fx = reverb(fx, ir(1.1, 0.3, seed=7), 0.14)
voice = hp(reverb(voice, cathedral, 0.22).T, 110).T

room = lp(rng.normal(0, 1, (N, 2)), 2000, 1) * 0.0012
def rms(x, a, b):
    seg = x[int(a * SR):int(b * SR)]
    seg = seg[np.abs(seg).max(1) > 1e-4] if seg.ndim == 2 else seg
    return np.sqrt(np.mean(seg ** 2)) + 1e-9

bed = music * 0.65 + fx * 0.8 + amb * 0.7
ref = rms(bed, 8.9, 14.8)
voice *= (ref * 3.0) / rms(voice, 4.48, 29.0)

mix = bed + voice + room
# re-apply the Act-2 silence gap after reverb too, so nothing rings across it
for b_ in (mix,):
    gfade = int(0.02 * SR)
    b_[gs - gfade:gs] *= np.linspace(1, 0, gfade)[:, None]
    b_[gs:ge] *= 0.0
    b_[ge:ge + gfade] *= np.linspace(0, 1, gfade)[:, None]
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
