"""FIRST SEARCH: a theme of its own (19 Nov: the director asked for a new one, not The Onboarding's vibes nor the
bossa he found annoying). Three candidates, synthesized (no licence), each starting on the bonk and ducked under the
voices by the film's mix:
  A  "Thrilled to announce": a bright plucked motif over clean claps and a bouncy bass, 112 bpm: the corporate-success
     jingle, played straight, so the zero being green is ironic.
  B  "Cover-up": sneaky pizzicato and a walking bass on the off-beats, 104 bpm, a woodblock: the shredder, the plaster.
  C  "Open plan": a muted-trumpet-ish lead over a lounge comp and brushes, 96 bpm: a sitcom office.
bed(kind, total, start) -> mono array at SR (silence before `start`)."""
import numpy as np
import sound_iwry as si

SR = si.SR
rng = np.random.default_rng(1010)


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12.0)


def tt(d):
    return np.arange(int(d * SR)) / float(SR)


def pluck(m, d, bright=1.0):
    t = tt(d); f = hz(m)
    a = sum(np.sin(2 * np.pi * f * h * t) * np.exp(-t * (6 + 5 * h)) * (bright / h) for h in (1, 2, 3, 4))
    return a * np.minimum(1, t / 0.003)


def pizz(m, d):
    t = tt(d); f = hz(m)
    a = (np.sin(2 * np.pi * f * t) + 0.4 * np.sin(2 * np.pi * 2 * f * t)) * np.exp(-t * 14)
    return a * np.minimum(1, t / 0.002)


def bass(m, d, decay=5.0):
    t = tt(d); f = hz(m)
    return (np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * 2 * f * t)) * np.exp(-t * decay) * np.minimum(1, t / 0.006)


def clap(d=0.12):
    n = rng.standard_normal(int(d * SR)); t = tt(d)
    return (n - si.lp(n, 3)) * np.exp(-t * 40) * 0.6


def wood(d=0.08):
    t = tt(d)
    return np.sin(2 * np.pi * 1300 * t) * np.exp(-t * 70) + 0.4 * np.sin(2 * np.pi * 2100 * t) * np.exp(-t * 90)


def brush(d=0.18):
    n = rng.standard_normal(int(d * SR)); t = tt(d)
    return (n - si.lp(n, 6)) * np.exp(-t * 18) * 0.25


def horn(m, d):
    t = tt(d); f = hz(m) * (1 + 0.004 * np.sin(2 * np.pi * 5 * t))
    ph = 2 * np.pi * np.cumsum(f) / SR
    a = sum(np.sin(ph * h) / h ** 1.3 for h in range(1, 7))
    env = np.minimum(1, t / 0.04) * np.exp(-t * 1.2) * np.minimum(1, (d - t) / 0.05)
    return si.lp(a, 3) * env


def chord(ms, d, f=pluck, g=0.5):
    out = np.zeros(int(d * SR))
    for m in ms:
        x = f(m, d); out[:len(x)] += x * g
    return out


def _put(out, a, t, g=1.0):
    i = int(t * SR)
    if i >= len(out):
        return
    a = a[:len(out) - i]
    out[i:i + len(a)] += a * g


def bed(kind, total, start=0.0):
    out = np.zeros(int(total * SR))
    if kind == "A":
        bpm = 112.0; beat = 60 / bpm
        prog = [(48, (60, 64, 67)), (45, (60, 64, 69)), (41, (60, 65, 69)), (43, (59, 62, 67))]   # C Am F G
        motif = [72, 76, 79, 76, 77, 76, 74, 72]
        t = start; b = 0
        while t < total:
            root, ch = prog[(b // 4) % 4]
            _put(out, bass(root, beat * 0.9), t, 0.55)
            if b % 2 == 1:
                _put(out, clap(), t, 0.35)
            _put(out, chord(ch, beat * 0.8), t + beat * 0.5, 0.18)
            _put(out, pluck(motif[b % 8], beat * 0.9, 1.2), t, 0.22 if (b // 8) % 2 == 0 else 0.0)
            t += beat; b += 1
    elif kind == "B":
        bpm = 104.0; beat = 60 / bpm
        line = [45, 48, 50, 51, 52, 50, 48, 47]
        melody = [69, None, 72, 71, None, 69, 67, None, 64, None, 67, 69, None, 72, 71, None]
        t = start; b = 0
        while t < total:
            _put(out, bass(line[b % 8], beat * 0.45, 9), t, 0.5)
            _put(out, wood(), t + beat * 0.5, 0.22)
            m = melody[(2 * b) % 16]
            if m:
                _put(out, pizz(m, beat * 0.4), t, 0.30)
            m = melody[(2 * b + 1) % 16]
            if m:
                _put(out, pizz(m, beat * 0.4), t + beat * 0.5, 0.26)
            t += beat; b += 1
    else:
        bpm = 96.0; beat = 60 / bpm
        prog = [(50, (65, 69, 72, 76)), (43, (65, 69, 71, 74)), (48, (64, 67, 71, 74)), (45, (64, 67, 69, 73))]
        tune = [(76, 1.5), (74, 0.5), (72, 1.0), (69, 1.0), (71, 2.0), (None, 2.0), (72, 1.0), (74, 1.0), (76, 2.0)]
        t = start; b = 0
        while t < total:
            root, ch = prog[(b // 4) % 4]
            _put(out, bass(root if b % 2 == 0 else root + 7, beat * 0.9, 4), t, 0.45)
            _put(out, brush(), t, 0.5); _put(out, brush(0.1), t + beat * 0.66, 0.3)
            if b % 4 in (1, 3):
                _put(out, chord(ch, beat * 1.2, pluck, 0.3), t + beat * 0.5, 0.16)
            t += beat; b += 1
        t = start + beat * 4; i = 0
        while t < total:
            m, d = tune[i % len(tune)]
            if m:
                _put(out, horn(m, d * beat * 0.95), t, 0.16)
            t += d * beat; i += 1
    out -= si.lp(out, int(SR / 200))
    out /= max(1e-6, np.abs(out).max())
    fade = int(0.3 * SR); i0 = int(start * SR)
    out[i0:i0 + fade] *= np.linspace(0, 1, len(out[i0:i0 + fade]))
    return out
