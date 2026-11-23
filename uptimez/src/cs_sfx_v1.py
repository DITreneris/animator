"""ONE STAR: small synthesized effects for the stretches with no words (scenes 4 and 5 ran 18 s silent). numpy only;
each returns mono float at 48 kHz, peak about 1 (cs_film sets the gains)."""
import numpy as np

SR = 48000
_r = np.random.RandomState(11)


def _n(dur):
    return _r.uniform(-1, 1, int(dur * SR))


def _lp(x, k):                                             # a cheap low-pass: a moving average of k samples
    return np.convolve(x, np.ones(k) / k, mode="same")


def _env(n, a=0.004, rel=None):
    t = np.arange(n) / float(SR)
    rel = rel or n / float(SR) / 4
    return np.minimum(1, t / a) * np.exp(-t / rel)


def tap(f=180.0):
    n = int(0.09 * SR); t = np.arange(n) / float(SR)
    return (np.sin(2 * np.pi * f * t) * np.exp(-t / 0.02) + 0.5 * _lp(_n(0.09), 6) * np.exp(-t / 0.006))


def key():
    n = int(0.03 * SR); t = np.arange(n) / float(SR)
    return (_n(0.03) - _lp(_n(0.03), 8)) * np.exp(-t / 0.004) + 0.3 * np.sin(2 * np.pi * 2200 * t) * np.exp(-t / 0.006)


def step():
    n = int(0.12 * SR); t = np.arange(n) / float(SR)
    return np.sin(2 * np.pi * 85 * t) * np.exp(-t / 0.03) + 0.25 * _lp(_n(0.12), 30) * np.exp(-t / 0.02)


def chime():
    n = int(0.6 * SR); t = np.arange(n) / float(SR)
    a = np.sin(2 * np.pi * 880 * t) * np.exp(-t / 0.18)
    b = np.sin(2 * np.pi * 1320 * t) * np.exp(-np.maximum(0, t - 0.09) / 0.22) * (t > 0.09)
    return 0.7 * (a + b)


def beep(f=480.0, dur=0.22):
    n = int(dur * SR); t = np.arange(n) / float(SR)
    return np.sin(2 * np.pi * f * t) * np.minimum(1, t / 0.01) * np.minimum(1, (dur - t) / 0.02)


def ring(dur=0.45):
    n = int(dur * SR); t = np.arange(n) / float(SR)
    return 0.5 * (np.sin(2 * np.pi * 440 * t) + np.sin(2 * np.pi * 480 * t)) * np.minimum(1, t / 0.02) * np.minimum(1, (dur - t) / 0.03)


def rustle(dur=0.4):
    x = _n(dur); x = x - _lp(x, 12)                         # the highs: paper
    n = len(x); e = np.abs(_lp(_r.uniform(0, 1, n), 1500)); e = e / e.max()
    return x * e * np.hanning(n)


def scratch(dur=0.5):
    x = _n(dur); x = _lp(x - _lp(x, 20), 3)
    t = np.arange(len(x)) / float(SR)
    return x * (0.55 + 0.45 * np.sin(2 * np.pi * 17 * t)) * np.hanning(len(x)) ** 0.3


def tape(dur=0.35):
    x = _n(dur); x = x - _lp(x, 6)
    t = np.arange(len(x)) / float(SR)
    return x * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * (60 + 240 * t / dur) * t))) * np.minimum(1, t / 0.01) * np.minimum(1, (dur - t) / 0.03)


def whirr(dur=2.3):
    n = int(dur * SR); t = np.arange(n) / float(SR)
    saw = 2 * ((t * 130) % 1.0) - 1
    x = 0.5 * _lp(saw, 10) + 0.35 * _lp(_n(dur), 14) * (0.6 + 0.4 * np.sin(2 * np.pi * 9 * t))
    return x * np.minimum(1, t / 0.08) * np.minimum(1, (dur - t) / 0.15)


def whoosh(dur=0.3):
    x = _lp(_n(dur), 24)
    return x * np.hanning(len(x)) ** 2 * 3
