"""Sound for "Mandatory Fun" animation v3 (mf_anim3.py): the cold open's effects, then the approved mix
(mf_mix_v1.wav, unchanged), then the loop tail's rewind. Writes mf_mix_v2.wav.
  python3 sound_mf_open.py"""
import numpy as np
import soundfile as sf
import mf_anim3 as M

rng = np.random.default_rng(31)


def tt(d, sr):
    return np.arange(int(d * sr)) / sr


def lp(x, n):
    k = np.ones(n) / n
    return np.convolve(x, k, "same")


def bloop(sr):                                           # the spell-check: two low beeps
    t = tt(0.16, sr)
    f = np.where(t < 0.08, 330, 262)
    return np.sin(2 * np.pi * f * t) * np.exp(-((t % 0.08) / 0.05)) * 0.18


def scan(sr):                                            # a soft rising sweep
    t = tt(0.26, sr)
    return np.sin(2 * np.pi * np.cumsum(600 + 1400 * t / 0.26) / sr) * np.sin(np.pi * t / 0.26) * 0.06


def zap(sr):                                             # electric crackle
    t = tt(0.13, sr)
    n = rng.standard_normal(len(t)) * (rng.random(len(t)) < 0.25)
    return (n - lp(n, 6)) * np.exp(-t / 0.05) * 0.35


def ding(sr):
    t = tt(0.9, sr)
    return sum(np.sin(2 * np.pi * f * t) * g for f, g in ((1568, 1.0), (3136, 0.35), (4704, 0.12))) * np.exp(-t / 0.25) * 0.12


def whistle(sr, d=0.33):                                 # the cone falling: a slide whistle down
    t = tt(d, sr)
    f = 1700 * (500 / 1700) ** (t / d)
    return np.sin(2 * np.pi * np.cumsum(f) / sr) * np.sin(np.pi * np.minimum(t / d * 1.2, 1) / 1) ** 0.5 * 0.10


def ploink(sr):
    t = tt(0.35, sr)
    f = 420 - 160 * np.minimum(t / 0.05, 1)
    return np.sin(2 * np.pi * np.cumsum(f) / sr) * np.exp(-t / 0.08) * 0.35


def toot(sr, d=0.55):                                    # a sad party horn: a buzzy saw, sagging
    t = tt(d, sr)
    f = 235 - 45 * (t / d) ** 1.5
    ph = np.cumsum(f) / sr
    saw = 2 * (ph % 1) - 1
    env = np.minimum(t / 0.03, 1) * np.where(t > d - 0.12, (d - t) / 0.12, 1)
    return lp(saw, 4) * env * 0.12


def rewind(sr, d=0.47):                                  # tape rewind: chirpy noise rising
    t = tt(d, sr)
    n = rng.standard_normal(len(t))
    f = 900 + 3200 * (t / d) ** 2
    car = np.sin(2 * np.pi * np.cumsum(f) / sr)
    return (lp(n, 3) * 0.10 + car * 0.05) * (0.6 + 0.4 * np.sin(2 * np.pi * 23 * t)) * np.sin(np.pi * t / d) ** 0.5


def add(buf, x, t0, sr):
    a = int(t0 * sr); b = min(len(buf), a + len(x))
    if x.ndim == 1 and buf.ndim == 2:
        x = np.stack([x, x], 1)
    buf[a:b] += x[:b - a]


def main(out="mf_mix_v2.wav"):
    mix, sr = sf.read("mf_mix_v1.wav")
    ch = mix.shape[1] if mix.ndim == 2 else 1
    total = int(round(M.DURATION * sr))
    shape = (total, ch) if ch > 1 else (total,)
    buf = np.zeros(shape)
    room = rng.standard_normal(total) * 0.002
    add(buf, room, 0.0, sr)
    for fn, t0 in ((bloop, 0.15), (scan, 0.30), (zap, 0.54), (ding, 0.59), (whistle, 0.62), (ploink, 0.95),
                   (toot, 1.05)):
        add(buf, fn(sr), t0, sr)
    o = int(M.OPEN * sr)
    n = min(len(mix), total - o)
    buf[o:o + n] += mix[:n]
    add(buf, rewind(sr), M.OPEN + M.D0 + 0.12, sr)
    sf.write(out, buf.astype(np.float32), sr)
    print("wrote", out, round(total / sr, 3), "s")


if __name__ == "__main__":
    main()
