"""Sound for "Happy Compliance" animation v3 (xmas_anim3.py): v2's mix (xmas_mix_v1.wav from `sound_xmas.py mix`,
unchanged) PRE s later, with the cold open in front (a whoosh as the CENSORED bar flies in at his robe, a second as it
swerves, a THUNK as it slaps onto the bauble) and TAIL s of quiet room tone after it for the loop tail.
Writes xmas_mix_v3.wav.   python3 sound_xmas3.py"""
import numpy as np
import soundfile as sf
import sound_xmas as sx
import sound_iwry as si

PRE, TAIL = 0.8, 0.4


def main(out="xmas_mix_v3.wav"):
    mix, sr = sf.read("xmas_mix_v1.wav")
    pre = np.zeros(int(PRE * sr)); tail = np.zeros(int(TAIL * sr))
    mono = np.concatenate([pre, np.zeros(len(mix)), tail])
    fx = np.zeros_like(mono)
    si.add(fx, sx.whoosh(0.22) * 0.30, 0.10)
    si.add(fx, sx.whoosh(0.16) * 0.22, 0.34)
    si.add(fx, sx.thunk(0.25, 120) * 0.55, 0.55)
    rng = np.random.default_rng(3)
    room = si.lp(rng.standard_normal(len(mono)), 160) * 0.02
    room[int(PRE * sr):int(PRE * sr) + len(mix)] = 0.0
    st = np.stack([fx + room, fx + room], 1)
    st[int(PRE * sr):int(PRE * sr) + len(mix)] += mix
    sf.write(out, st.astype(np.float32), sr)
    print(out, round(len(st) / sr, 3))


if __name__ == "__main__":
    main()
