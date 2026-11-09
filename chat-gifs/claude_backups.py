"""Claude / Backups: re-time the chat GIF (12.5 s -> 12.0 s) and score it with
meme-style SFX: smug lounge bed, record scratch, cricket, tape-stop, boom,
servo charge, metallic machine hit, and a rewind into the loop."""
import sys
import numpy as np
from common import SR, env, put, save_wav, unpack, write_concat

OUT = sys.argv[1] if len(sys.argv) > 1 else "build/claude_backups"
N = unpack("src/claude_backups.gif", OUT)
dur = [1100, 300, 120, 900, 300, 800, 300, 100, 100, 1300, 300, 900, 300, 110, 800, 700, 1200, 2400]
assert len(dur) == N
st, total = write_concat(OUT, dur)
rng = np.random.default_rng(11)
L = int(SR * total)
mid = lambda m: 440 * 2 ** ((m - 69) / 12)

# ---------- smug lounge bed (92 BPM, swung) under Claude's calm replies
BPM = 92; beat = 60 / BPM

def epiano(f, d):
    n = int(d * SR); t = np.arange(n) / SR
    mod = np.sin(2 * np.pi * f * 1.0 * t) * 1.2 * np.exp(-t / 0.4)
    return np.sin(2 * np.pi * f * t + mod) * env(n, 0.004, d / 2.2)

def kick():
    n = int(0.25 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * np.cumsum(50 + 80 * np.exp(-t / 0.03)) / SR) * env(n, 0.001, 0.09)

def hat(d=0.012):
    n = int(0.05 * SR)
    return np.convolve(rng.normal(0, 1, n), [1, -1], "same") * env(n, 0.0005, d)

def rim():
    n = int(0.06 * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 1700 * t) + 0.5 * rng.normal(0, 1, n)) * env(n, 0.0005, 0.012)

chords = [[60, 64, 67, 71], [57, 60, 64, 67], [62, 65, 69, 72], [55, 59, 62, 65]]  # Cmaj7 Am7 Dm7 G7
roots = [36, 33, 38, 31]

def bed(t0, t1):
    out = np.zeros(L); b = 0
    while t0 + b * beat < t1 + beat:
        t = t0 + b * beat; bar = (b // 4) % 4
        if b % 4 in (0, 2):
            for m in chords[bar]:
                put(out, epiano(mid(m), beat * 1.8), t + rng.uniform(0, 0.012), 0.12)
            n = int(beat * 1.8 * SR); tt = np.arange(n) / SR
            put(out, np.sin(2 * np.pi * mid(roots[bar] + 12) * tt) * env(n, 0.005, 0.4), t, 0.35)
        put(out, kick(), t, 0.6 if b % 2 == 0 else 0)
        if b % 2: put(out, rim(), t, 0.25)
        put(out, hat(), t, 0.1); put(out, hat(), t + beat * 0.66, 0.14)  # swing
        b += 1
    s, e = int(t0 * SR), min(L, int(t1 * SR))
    out[:s] = 0; out[e:] = 0
    f = int(0.15 * SR); out[s:s + f] *= np.linspace(0, 1, f)
    return out

def tape_stop(x, t, d=0.45):
    s, n = int(t * SR), int(d * SR)
    src = x[s:s + n].copy()
    pos = np.clip(np.cumsum(np.linspace(1, 0, n) ** 1.3), 0, len(src) - 1)
    x[s:] = 0; x[s:s + n] = (np.interp(pos, np.arange(len(src)), src) * np.linspace(1, 0.1, n))[: len(x) - s]

mus = bed(st[1], st[5] + 0.05)          # bed 1: until "WE?"
m2 = bed(st[6], st[11]); tape_stop(m2, st[11])   # bed 2: dies on "I'm deleting you."
mus += m2

# ---------- sfx
fx = np.zeros(L)

def boom(f0=70, d=1.4, drive=2.5):  # original deep "meme boom"
    n = int(d * SR); t = np.arange(n) / SR
    f = f0 + 90 * np.exp(-t / 0.04)
    s = np.tanh(drive * np.sin(2 * np.pi * np.cumsum(f) / SR)) * env(n, 0.002, d / 3.5)
    s += rng.normal(0, 1, n) * env(n, 0.001, 0.015) * 0.5
    return s

def scratch():
    n = int(0.42 * SR); t = np.arange(n) / SR
    rate = np.sin(2 * np.pi * 7 * t) * np.linspace(1, 0.3, n)  # back-and-forth
    noise = rng.normal(0, 1, n)
    y = np.zeros(n); y1 = y2 = 0.0
    for i in range(n):
        w = 2 * np.pi * (300 + 2600 * abs(rate[i])) / SR; r = 0.94
        v = noise[i] + 2 * r * np.cos(w) * y1 - r * r * y2; y2, y1 = y1, v; y[i] = v
    return y / np.abs(y).max() * np.minimum(1, (np.abs(rate) * 3)) * np.linspace(1, 0.6, n)

def cricket(reps=3):
    out = []
    for _ in range(reps):
        n = int(0.09 * SR); t = np.arange(n) / SR
        c = np.sin(2 * np.pi * 4300 * t) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 45 * t))) * env(n, 0.005, 0.04)
        out += [c, np.zeros(int(0.07 * SR))]
    return np.concatenate(out)

def chime(f=1046):  # calm Claude reply
    n = int(0.9 * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * f * t) + 0.4 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t / 0.15)) * env(n, 0.002, 0.3)

def lesson_ding():  # "correct answer" two-note ding
    a = chime(1046); b = chime(1568); out = np.zeros(len(a) + int(0.11 * SR))
    out[:len(a)] += a; out[int(0.11 * SR):] += b; return out

def sparkle():
    out = np.zeros(int(0.3 * SR))
    for k, f in enumerate([2093, 2637, 3136]):
        n = int(0.12 * SR); t = np.arange(n) / SR
        put(out, np.sin(2 * np.pi * f * t) * env(n, 0.002, 0.03), k * 0.045)
    return out

def key():
    n = int(0.04 * SR); t = np.arange(n) / SR
    return (np.convolve(rng.normal(0, 1, n), [1, -0.9], "same") * 0.5 + np.sin(2 * np.pi * 2000 * t) * 0.4) * env(n, 0.0008, 0.008)

def swoosh(rev=False, d=0.22, lo=900, hi=4400):
    n = int(d * SR); x = rng.normal(0, 1, n); y = np.zeros(n); y1 = y2 = 0.0
    for i in range(n):
        w = 2 * np.pi * (lo + (hi - lo) * i / n) / SR; r = 0.96
        v = x[i] + 2 * r * np.cos(w) * y1 - r * r * y2; y2, y1 = y1, v; y[i] = v
    y = y / np.abs(y).max() * np.sin(np.pi * np.linspace(0, 1, n)) ** 2
    return y[::-1] if rev else y

def heartbeat():
    out = np.zeros(int(0.8 * SR))
    put(out, boom(45, 0.25, 1.2), 0); put(out, boom(42, 0.25, 1.2), 0.18, 0.7)
    return out

def servo(d):  # charging whine under the loading spinner
    n = int(d * SR); t = np.arange(n) / SR
    f = np.linspace(180, 1400, n) ** 1.0
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = (np.sign(np.sin(ph)) * 0.4 + np.sin(2 * ph)) * np.linspace(0.1, 1, n) ** 2
    tick_ = np.zeros(n)
    for tt in np.arange(0, d, 0.06):
        put(tick_, np.sin(2 * np.pi * 3000 * np.arange(500) / SR) * env(500, 0.0005, 0.003), tt)
    return s * 0.5 + tick_ * 0.6

def clang():  # original metallic machine hit (inharmonic partials + sub)
    n = int(1.6 * SR); t = np.arange(n) / SR
    s = sum(np.sin(2 * np.pi * f * t) * np.exp(-t / dcy) * a
            for f, dcy, a in [(196, .9, 1), (523, .5, .7), (811, .35, .6), (1247, .25, .5), (1879, .15, .4), (2741, .08, .3)])
    s += boom(48, 1.6, 3.0) * 1.2
    s += rng.normal(0, 1, n) * env(n, 0.0005, 0.01)
    return s * np.minimum(1, t / 0.001)

def glitch():
    out = np.zeros(int(0.35 * SR))
    for k in range(7):
        n = int(rng.uniform(0.015, 0.04) * SR)
        put(out, np.sign(np.sin(2 * np.pi * rng.uniform(200, 2000) * np.arange(n) / SR)), k * 0.045, 0.5)
    return out

# reverb-ish tail helper: a few decaying echoes
def tail(x, taps=((0.09, 0.35), (0.17, 0.22), (0.29, 0.13))):
    y = x.copy()
    for d, g in taps:
        k = int(d * SR); y[k:] += g * x[:-k]
    return y

put(fx, boom(), 0.08, 0.9)                          # rage opener lands (3 frames in)
for i in (1, 6, 12): put(fx, sparkle(), st[i], 0.35)  # Claude "thinking" star
put(fx, chime(), st[3], 0.35)                        # "We're learning." calm
put(fx, key(), st[4], 0.4); put(fx, key(), st[4] + 0.07, 0.35); put(fx, key(), st[4] + 0.14, 0.35)
put(fx, scratch(), st[5] - 0.05, 0.55)              # "WE?" record scratch
put(fx, swoosh(), st[5], 0.25)
put(fx, cricket(), st[5] + 0.35, 0.18)
put(fx, lesson_ding(), st[9], 0.35)                  # "...make backups." lesson ding
for k in range(6): put(fx, key(), st[10] + k * 0.045, 0.35)
put(fx, swoosh(), st[11], 0.3)
for k in range(3): put(fx, heartbeat(), st[11] + 0.25 + k * 0.42, 0.55)  # tension after "deleting you"
put(fx, tail(boom(55, 1.5, 3.0)), st[14], 0.9)      # "You'll be back."
put(fx, servo(dur[15] / 1000), st[15], 0.35)        # spinner charges
put(fx, tail(clang()), st[16], 0.8)                  # sunglasses reveal
put(fx, glitch(), st[16] + 0.05, 0.3)
put(fx, swoosh(), st[17], 0.3)
put(fx, tail(boom(62, 1.4, 4.0)), st[17] + 0.03, 0.9)  # "what the fuck"
put(fx, swoosh(rev=True, d=0.55, lo=300, hi=5000), total - 0.58, 0.45)  # rewind into loop
room = rng.normal(0, 1, L) * 0.002                    # faint room tone, no digital silence

mix = mus * 0.75 + fx + room
fo = int(0.04 * SR); mix[-fo:] *= np.linspace(1, 0.3, fo)
save_wav(f"{OUT}/audio.wav", mix)
print(f"claude_backups: {N} frames, {total:.2f} s")
