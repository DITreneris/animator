"""Audio for S1v3.3: splices s132_mix.wav to s133's time map and adds the cold-open slap,
a tape rewind and a freeze sting per name card. Run sound_s132.py first.
Usage: python3 sound_s133.py s133 | s133n"""
import sys
import numpy as np
import soundfile as sf
import s133

which = sys.argv[1] if len(sys.argv) > 1 else "s133"
end = 20.5 if which.endswith("n") else 21.5
src, SR = sf.read("s132_mix.wav")
rng = np.random.default_rng(33)
L = int(s133.duration(end) * SR)
out = np.zeros(L)


def tt(d):
    return np.arange(int(d * SR)) / SR


def lowpass(x, k):
    return np.convolve(x, np.ones(k) / k, mode="same")


def put(sig, t, g=1.0):
    i = int(t * SR)
    n = min(len(sig), L - i)
    if n > 0:
        out[i:i + n] += sig[:n] * g


def seg(a, b):
    return src[int(a * SR):int(b * SR)].copy()


def slap():
    t = tt(0.25)
    return (rng.standard_normal(len(t)) * 0.8 + np.sin(2 * np.pi * 110 * t)) * np.exp(-t * 25)


def freeze_sting():
    t = tt(0.35)
    shutter = np.diff(rng.standard_normal(int(0.03 * SR)), prepend=0) * 0.8
    tone = np.sin(2 * np.pi * np.cumsum(880 - 500 * t / 0.35) / SR) * np.exp(-t * 8) * 0.5
    s = tone.copy()
    s[:len(shutter)] += shutter
    return s


# cold open: the mix from the sneeze on, slap on the lens
put(seg(11.1 - 0.03, 11.1 + s133.COLD), 0.0)
put(slap(), 0.7, 0.9)
# rewind: 11.6 s of mix reversed and squeezed into 0.4 s, plus tape whir
r = seg(0.0, 11.6)[::-1]
n = int(s133.REW * SR)
rew = np.interp(np.linspace(0, len(r) - 1, n), np.arange(len(r)), r)
whir = np.sin(2 * np.pi * np.cumsum(np.linspace(300, 1200, n)) / SR) * 0.25
put((rew * 0.5 + whir) * np.sin(np.pi * np.arange(n) / n) ** 0.3, s133.COLD)
# the film, with a gap + sting at each freeze
T = s133.COLD + s133.REW
prev = 0.0
for (ft, *_r) in s133.CARDS:
    put(seg(prev, ft), T)
    T += ft - prev
    put(freeze_sting(), T, 0.8)
    put(lowpass(rng.standard_normal(int(s133.FREEZE * SR)), 200) * 0.02, T)
    T += s133.FREEZE
    prev = ft
put(seg(prev, end), T)
fade = int(0.05 * SR)
out[-fade:] *= np.linspace(1, 0, fade)
out /= np.abs(out).max() / 0.85
sf.write(f"{which}_mix.wav", out.astype(np.float32), SR, subtype="FLOAT")
print(which, round(L / SR, 2))
