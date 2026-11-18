"""Sound for "Happy Compliance" animation v5 (xmas_anim5.py): v2's mix (xmas_mix_v1.wav, unchanged) PRE s later,
with the cold open retimed (the bar in at his robe, a hover hum, the swerve, the THUNK at 0.68 s), a whoosh as Pam
throws the bauble (v2 24.95 s), a whizz as it comes in at Don (26.62 s), and a soft slide as the bar slips off the
bauble before the alarm (28.08 s). Writes xmas_mix_v5.wav.   python3 sound_xmas5.py"""
import numpy as np
import soundfile as sf
import sound_xmas as sx
import sound_iwry as si

PRE, TAIL = 0.8, 0.4


def main(out="xmas_mix_v5.wav"):
    mix, sr = sf.read("xmas_mix_v1.wav")
    n = int(PRE * sr) + len(mix) + int(TAIL * sr)
    fx = np.zeros(n)
    t = np.arange(int(0.15 * sr)) / sr
    hum = np.sin(2 * np.pi * 180 * t) * np.sin(np.pi * t / 0.15) * 0.06              # the bar hovers, "looking"
    si.add(fx, sx.whoosh(0.22) * 0.30, 0.08)
    si.add(fx, hum, 0.35)
    si.add(fx, sx.whoosh(0.16) * 0.22, 0.50)
    si.add(fx, sx.thunk(0.25, 120) * 0.55, 0.68)
    si.add(fx, sx.whoosh(0.30) * 0.32, PRE + 24.95)                                 # Pam throws
    si.add(fx, sx.whoosh(0.22) * 0.30, PRE + 26.62)                                 # it comes in at Don
    si.add(fx, sx.whoosh(0.12) * 0.14, PRE + 28.08)                                 # the bar slips off
    rng = np.random.default_rng(3)
    room = si.lp(rng.standard_normal(n), 160) * 0.02
    a0 = int(PRE * sr)
    room[a0:a0 + len(mix)] = 0.0
    st = np.stack([fx + room, fx + room], 1)
    st[a0:a0 + len(mix)] += mix
    sf.write(out, st.astype(np.float32), sr)
    print(out, round(len(st) / sr, 3))


if __name__ == "__main__":
    main()
