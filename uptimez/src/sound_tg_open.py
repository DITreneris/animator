"""Sound for "Raises for Everyone" animation v3 (tg_anim3.py): v2's approved mix (tg_mix_v2.wav, unchanged) plus a
gravy-boat wobble and a plate rattle on the frame-0 slap, and the loop tail: a form dropping onto the stack.
Writes tg_mix_v3.wav.   python3 sound_tg_open.py"""
import numpy as np
import soundfile as sf
import tg_anim3 as M

rng = np.random.default_rng(11)


def tt(d, sr):
    return np.arange(int(d * sr)) / sr


def wobble(sr, d=0.6):                                   # a comic gravy wobble: a bending low tone
    t = tt(d, sr)
    f = 140 + 40 * np.sin(2 * np.pi * 9 * t) * np.exp(-t / 0.3)
    return np.sin(2 * np.pi * np.cumsum(f) / sr) * np.exp(-t / 0.22) * 0.22


def rattle(sr, d=0.25):                                  # plates and cutlery jump
    t = tt(d, sr); out = np.zeros(len(t))
    for i in range(7):
        a = int(rng.uniform(0, 0.15) * sr); f = rng.uniform(2500, 5200)
        x = np.sin(2 * np.pi * f * t[:len(t) - a]) * np.exp(-t[:len(t) - a] / 0.03) * 0.05
        out[a:] += x
    return out


def fwip(sr, d=0.28):                                    # paper through the air
    t = tt(d, sr); n = rng.standard_normal(len(t))
    k = np.ones(6) / 6
    return (n - np.convolve(n, k, "same")) * np.sin(np.pi * t / d) ** 2 * 0.06


def pat(sr, d=0.12):                                     # the form lands
    t = tt(d, sr)
    return np.sin(2 * np.pi * (180 - 400 * t) * t) * np.exp(-t / 0.02) * 0.25


def add(buf, x, t0, sr):
    a = int(t0 * sr); b = min(len(buf), a + len(x))
    if buf.ndim == 2:
        x = np.stack([x, x], 1)
    buf[a:b] += x[:b - a]


def main(out="tg_mix_v3.wav"):
    mix, sr = sf.read("tg_mix_v2.wav")
    total = int(round(M.DURATION * sr))
    shape = (total,) + mix.shape[1:]
    buf = np.zeros(shape)
    n = min(len(mix), int(M.D0 * sr))
    buf[:n] += mix[:n]
    add(buf, wobble(sr), 0.14, sr)
    add(buf, rattle(sr), 0.11, sr)
    add(buf, fwip(sr), M.D0 + 0.02, sr)
    add(buf, pat(sr), M.D0 + 0.29, sr)
    sf.write(out, buf.astype(np.float32), sr)
    print("wrote", out, round(total / sr, 3), "s, v2 mix", round(len(mix) / sr, 3), "s")


if __name__ == "__main__":
    main()
