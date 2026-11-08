"""Audio for S1v3.6: S1v3.2's mix rebuilt with voices +3 dB and paper rustle -3 dB, spliced to the
S1v3.4+ time map (1.0 s freezes), then an office room tone under everything, a pen-scratch sting when
the doodle lands and a soft low "dun" when DON looks up.
Usage: python3 sound_s136.py s136 | s136n   (writes s136base_mix.wav, then <which>_mix.wav)"""
import os
import sys
import numpy as np
import soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
which = sys.argv[1] if len(sys.argv) > 1 else "s136"

# 1) rebuild the S1v3.2 mix with new balance (sound_s132.py itself is unchanged)
src = open(os.path.join(HERE, "sound_s132.py")).read()
src = src.replace("mix = fx + 1.25 * voice + mus * duck + room", "mix = fx + 1.25 * 2.8 * voice + 0.5 * mus * duck + room")
src = src.replace("add(fx, rustle(3.0, 150), 11.2, 0.55)", "add(fx, rustle(3.0, 150), 11.2, 0.39)")
src = src.replace("add(fx, rustle(1.8, 40), 12.2, 0.3)", "add(fx, rustle(1.8, 40), 12.2, 0.21)")
assert src.count("2.8 * voice") == 1 and "0.39)" in src and "0.21)" in src
sys.argv = ["sound_s132.py", "s136base"]
exec(compile(src, "sound_s132(s136)", "exec"), {"__name__": "__main__", "__file__": os.path.join(HERE, "sound_s132.py")})

# 2) splice to the time map (sound_s133.py logic, reading the rebuilt mix)
import s133  # noqa: E402
s133.FREEZE = 1.0
sp = open(os.path.join(HERE, "sound_s133.py")).read().replace('sf.read("s132_mix.wav")', 'sf.read("s136base_mix.wav")')
assert 's136base_mix.wav' in sp
sys.argv = ["sound_s133.py", which]
g = {"__name__": "__main__"}
exec(compile(sp, "sound_s133(s136)", "exec"), g)

# 3) room tone + stings on the spliced mix
out, SR = sf.read(f"{which}_mix.wav")
rng = np.random.default_rng(36)
L = len(out)


def tt(d):
    return np.arange(int(d * SR)) / SR


def lp(x, k):
    return np.convolve(x, np.ones(k) / k, mode="same")


def put(sig, t, gain):
    i = int(t * SR)
    n = min(len(sig), L - i)
    if n > 0:
        out[i:i + n] += sig[:n] * gain


room = lp(lp(rng.standard_normal(L), 120), 40) * 1.2 + np.sin(2 * np.pi * 60 * np.arange(L) / SR) * 0.15 * lp(rng.standard_normal(L), 4000) * 3
room *= 0.035 / (np.sqrt(np.mean(room ** 2)) + 1e-9) * 0.03
out += room


def scratch():
    o = np.zeros(int(0.55 * SR))
    for s0 in (0.0, 0.14, 0.27, 0.38):
        t = tt(0.11)
        n = np.diff(rng.standard_normal(len(t)), prepend=0) * np.sin(np.pi * t / 0.11) * 0.6
        o[int(s0 * SR):int(s0 * SR) + len(t)] += n
    return o


def dun():
    t = tt(0.9)
    return (np.sin(2 * np.pi * 73 * t) + 0.4 * np.sin(2 * np.pi * 146 * t)) * np.exp(-t * 3.5) * np.minimum(1, t * 60)


off = s133.COLD + s133.REW + s133.FREEZE * 3       # s132 time -> new time, after the last name tag
ref = np.sqrt(np.mean(out[int(3.5 * SR):int(4.3 * SR)] ** 2))      # DON's first line = speech reference
rms = lambda x: np.sqrt(np.mean(x ** 2))
sc, dn = scratch(), dun()
put(sc, 14.5 + off, 0.5 * ref / rms(sc))                          # stings sit 6 dB under the voice
put(dn, 17.2 + off, 0.5 * ref / rms(dn[:int(0.4 * SR)]))
out /= np.abs(out).max() / 0.85
sf.write(f"{which}_mix.wav", out.astype(np.float32), SR, subtype="FLOAT")
print("done", which, round(L / SR, 2))
