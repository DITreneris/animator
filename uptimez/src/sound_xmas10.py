"""Sound for "Happy Compliance" animation v10 (xmas_anim10.py): v8's mix (xmas_mix_v8.wav, built by sound_xmas8.py)
plus the scan's soft hum under "INAPPROPRIATE BALLS DETECTED." with its tick, the bar's slap as it lands on Don, and its
whoosh as it leaves him for the door. Writes xmas_mix_v10.wav.
python3 sound_xmas10.py"""
import numpy as np
import soundfile as sf
import sound_xmas as S

PRE, BEAT, LAND = 0.8, 0.9, 0.7
D2 = 28.9
SCAN0, SCAN1, TICK = PRE + 13.85, PRE + 15.15, PRE + 15.2
SLAP = PRE + BEAT + LAND + 28.30
OFF = PRE + D2 + BEAT + LAND + 0.72


def add(st, x, at, sr):
    i = int(at * sr)
    x = x[:max(0, len(st) - i)]
    st[i:i + len(x)] += x[:, None]


def main(src="xmas_mix_v8.wav", out="xmas_mix_v10.wav"):
    st, sr = sf.read(src)
    d = SCAN1 - SCAN0
    t = np.arange(int(d * sr)) / sr
    ph = (t / d * 2) % 1.0                                     # two sweeps, as in the picture
    f = 520 + 260 * (0.5 - 0.5 * np.cos(2 * np.pi * ph))
    hum = np.sin(2 * np.pi * np.cumsum(f) / sr) * np.minimum(1, np.minimum(t, d - t) / 0.05) * 0.035
    add(st, hum, SCAN0, sr)
    add(st, S.glock(1568, 0.35) * 0.12, TICK, sr)               # the tick: one bright ping
    add(st, S.glock(2093, 0.3) * 0.08, TICK + 0.07, sr)
    add(st, S.thunk(0.12, 220) * 0.25, SLAP, sr)
    add(st, S.whoosh(0.26) * 0.3, OFF, sr)
    sf.write(out, st.astype(np.float32), sr)
    print(out, round(len(st) / sr, 3))


if __name__ == "__main__":
    main()
