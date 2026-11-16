"""Make It Original: synthesized instruments and effects (numpy only, fixed seeds).
Everything here is our own composition and synthesis; no samples."""
import numpy as np
SR = 48000

def silence(sec):
    return np.zeros(int(round(sec * SR)))

def mtof(m):
    return 440.0 * 2 ** ((m - 69) / 12)

def onepole_lp(x, fc):
    a = np.exp(-2 * np.pi * fc / SR); y = np.empty_like(x); s = 0.0
    for i, v in enumerate(x):
        s = (1 - a) * v + a * s; y[i] = s
    return y

def place(buf, sig, t, gain=1.0):
    """Add sig into buf starting at time t (s), growing buf if needed."""
    i = int(round(t * SR))
    if i + len(sig) > len(buf):
        buf = np.concatenate([buf, np.zeros(i + len(sig) - len(buf))])
    buf[i:i + len(sig)] += sig * gain
    return buf

# ---------- guitar (Karplus-Strong, soft clip, small cabinet) ----------
def ks_pluck(freq, dur, bright=0.5, decay=0.996, seed=0, mute=0.0):
    rng = np.random.default_rng(seed)
    n = int(dur * SR); N = max(2, int(SR / freq))
    buf = rng.uniform(-1, 1, N)
    buf = onepole_lp(buf, 1500 + 6000 * bright)            # pick brightness
    out = np.empty(n); d = decay * (1 - 0.02 * mute)
    for i in range(n):
        v = buf[i % N]; nxt = buf[(i + 1) % N]
        buf[i % N] = d * 0.5 * (v + nxt)
        out[i] = v
    env = np.ones(n); r = int(0.03 * SR)
    env[-r:] = np.linspace(1, 0, r)
    if mute: env *= np.exp(-np.arange(n) / SR * (2 + 12 * mute))
    return out * env

def amp(x, drive=3.0, tone=3200):
    y = np.tanh(drive * x) / np.tanh(drive)
    return onepole_lp(y, tone)

def room(x, mix=0.18, delays=(0.031, 0.047, 0.071), fb=0.35):
    y = x.copy()
    for k, dl in enumerate(delays):
        n = int(dl * SR); e = np.zeros(len(x) + n * 6)
        e[:len(x)] = x
        for r in range(1, 6):
            e[r * n:r * n + len(x)] += x * (fb ** r) * (0.8 ** k)
        y = np.concatenate([y, np.zeros(max(0, len(e) - len(y)))])
        y[:len(e)] += mix * e[:len(y)] / len(delays)
    return y

def guitar_phrase(notes, bpm=120, detune_cents=0.0, seed=1, drive=3.0, paws=False):
    """notes: [(midi, sixteenths), ...]. paws=True: the cat's take, same notes and rhythm,
    muted thumpy plucks with a soft body thud on each contact."""
    s16 = 60 / bpm / 4
    rng = np.random.default_rng(seed)
    out = silence(0.05); t = 0.02
    for i, (m, l) in enumerate(notes):
        dur = l * s16 + (0.9 if i == len(notes) - 1 else 0.02)   # single-note lead: each note stops as the next starts
        cents = detune_cents * rng.uniform(-1, 1)
        f = mtof(m) * 2 ** (cents / 1200)
        if paws:
            p = ks_pluck(f, dur, bright=0.15, decay=0.993, seed=seed + i, mute=0.55) * 0.8
            thud = np.random.default_rng(seed + 50 + i).normal(0, 1, int(0.05 * SR))
            thud = onepole_lp(thud, 260) * np.exp(-np.arange(len(thud)) / SR * 70) * 2.2
            p[:len(thud)] += thud
        else:
            p = ks_pluck(f, dur, bright=0.55, decay=0.9965, seed=seed + i)
        out = place(out, p, t)
        t += l * s16
    y = amp(out, drive=drive if not paws else 2.0)
    return room(y), t

# ---------- the AI's tune: soft electric piano + pad ----------
def epiano(freq, dur, seed=0):
    n = int(dur * SR); tt = np.arange(n) / SR
    mod = np.sin(2 * np.pi * freq * tt) * 1.6 * np.exp(-tt * 3)       # FM bell-ish attack
    y = np.sin(2 * np.pi * freq * tt + mod) * np.exp(-tt * 2.2)
    y += 0.3 * np.sin(2 * np.pi * 2 * freq * tt) * np.exp(-tt * 4)
    a = int(0.004 * SR); y[:a] *= np.linspace(0, 1, a)
    r = int(0.05 * SR); y[-r:] *= np.linspace(1, 0, r)
    return y

def pad(freqs, dur):
    n = int(dur * SR); tt = np.arange(n) / SR; y = np.zeros(n)
    for f in freqs:
        for dt in (-0.12, 0.12):
            ph = 2 * np.pi * (f + dt) * tt
            y += (np.sin(ph) + 0.25 * np.sin(2 * ph)) / len(freqs)
    env = np.minimum(1, tt / 0.25) * np.minimum(1, (dur - tt) / 0.4)
    return onepole_lp(y * env, 1800) * 0.35

def synthlead(freq, dur):
    n = int(dur * SR); tt = np.arange(n) / SR
    saw = 2 * ((freq * tt) % 1) - 1 + 2 * ((freq * 1.004 * tt) % 1) - 1
    env = np.minimum(1, tt / 0.01) * np.exp(-tt * 1.2)
    r = int(0.06 * SR); env[-r:] *= np.linspace(1, 0, r)
    return onepole_lp(saw * env * 0.4, 1400 + 600 * np.exp(-1))

def tune(notes, chord, kind='epiano', bpm=120):
    s16 = 60 / bpm / 4; out = silence(0.05); t = 0.02
    total = sum(l for _, l in notes) * s16 + 0.9
    out = place(out, pad([mtof(m) for m in chord], total), 0.0)
    for i, (m, l) in enumerate(notes):
        dur = l * s16 + (0.8 if i == len(notes) - 1 else 0.3)
        v = epiano(mtof(m), dur) if kind == 'epiano' else synthlead(mtof(m), dur)
        out = place(out, v, t, 0.7)
        t += l * s16
    return room(out, mix=0.25), t

# ---------- effects ----------
def meow(dur=0.55, seed=3):
    n = int(dur * SR); tt = np.arange(n) / SR; u = tt / dur
    f0 = 520 + 260 * np.sin(np.pi * np.minimum(1, u * 1.3)) - 120 * u
    ph = 2 * np.pi * np.cumsum(f0) / SR
    src = sum(np.sin(k * ph) / k for k in range(1, 14))
    y = np.zeros(n)
    for fa, fb, bw in ((900, 1200, 140), (1800, 1400, 200), (3000, 2600, 300)):  # "mee-ow" formant glide
        fc = fa + (fb - fa) * u
        y += _resonate(src, fc, bw)
    env = np.minimum(1, tt / 0.04) * np.minimum(1, (dur - tt) / 0.12)
    y = y * env; return y / (np.abs(y).max() + 1e-9) * 0.5

def _resonate(x, fc, bw):
    y = np.zeros_like(x); y1 = y2 = 0.0
    for i in range(len(x)):
        r = np.exp(-np.pi * bw / SR); th = 2 * np.pi * fc[i] / SR
        v = x[i] * (1 - r) + 2 * r * np.cos(th) * y1 - r * r * y2
        y2, y1 = y1, v; y[i] = v
    return y

def tape_ff(dur=0.5, up=True, seed=5):
    n = int(dur * SR); tt = np.arange(n) / SR; u = tt / dur
    f = 250 * (14 ** (u if up else 1 - u))
    wob = 1 + 0.03 * np.sin(2 * np.pi * 9 * tt)
    sq = np.sin(2 * np.pi * np.cumsum(f * wob) / SR) * 0.25
    hiss = onepole_lp(np.random.default_rng(seed).normal(0, 0.25, n), 5000)
    env = np.minimum(1, tt / 0.03) * np.minimum(1, (dur - tt) / 0.05)
    y = (sq + hiss * 0.5) * env
    clunk = onepole_lp(np.random.default_rng(seed + 1).normal(0, 1, int(0.04 * SR)), 400)
    clunk *= np.exp(-np.arange(len(clunk)) / SR * 90) * 1.5
    y[:len(clunk)] += clunk; y[-len(clunk):] += clunk * 0.7
    return y * 0.6

def swipe(dur=0.18, seed=7):
    n = int(dur * SR); tt = np.arange(n) / SR; u = tt / dur
    x = np.random.default_rng(seed).normal(0, 1, n)
    y = onepole_lp(x, 1500) - onepole_lp(x, 300)
    return y * np.sin(np.pi * u) ** 2 * 0.5

def tick_roll(dur=1.0, seed=9):
    """Counter ticks speeding up; low-passed so AAC doesn't overshoot (lesson)."""
    out = silence(dur); t = 0.0; gap = 0.12
    while t < dur - 0.02:
        c = onepole_lp(np.random.default_rng(seed + int(t * 1000)).normal(0, 1, int(0.006 * SR)), 2500) * 0.35
        out = place(out, c, t); t += gap; gap = max(0.03, gap * 0.85)
    return out

def norm(x, peak=0.8):
    return x / (np.abs(x).max() + 1e-9) * peak
