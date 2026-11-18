"""Sound for "Happy Compliance" animation v7 (xmas_anim7.py): v2's mix (xmas_mix_v1.wav, unchanged) with the cold
open in front (PRE s: the bar in at his robe, a hover hum, the swerve, the THUNK), a new EXTRA s beat cut in after
"Merry Christmas, Don." (v2 26.9 s: the throw's whoosh, the whizz, a BONK on his head, the whoosh of the plank fall;
room tone under it), the bar slipping off the bauble before the alarm, and TAIL s of room tone for the loop tail.
v2's own THUD now lands as Don hits the floor in front of the robot. Writes xmas_mix_v7.wav.   python3 sound_xmas7.py"""
import numpy as np
import soundfile as sf
import sound_xmas as sx
import sound_iwry as si

PRE, TAIL, AT, EXTRA = 0.8, 0.4, 26.9, 0.9


def bonk(d=0.22):
    t = np.arange(int(d * si.SR)) / si.SR
    f = 520 * np.exp(-t * 9) + 180                                   # a hollow, falling "bonk"
    body = np.sin(2 * np.pi * np.cumsum(f) / si.SR) * np.exp(-t * 14)
    return body + sx.thunk(d, 150) * 0.6


def main(out="xmas_mix_v7.wav"):
    mix, sr = sf.read("xmas_mix_v1.wav")
    cut = int(AT * sr)
    a, b = mix[:cut], mix[cut:]
    n = int(PRE * sr) + len(a) + int(EXTRA * sr) + len(b) + int(TAIL * sr)
    fx = np.zeros(n)
    t = np.arange(int(0.15 * sr)) / sr
    si.add(fx, sx.whoosh(0.22) * 0.30, 0.08)
    si.add(fx, np.sin(2 * np.pi * 180 * t) * np.sin(np.pi * t / 0.15) * 0.06, 0.35)
    si.add(fx, sx.whoosh(0.16) * 0.22, 0.50)
    si.add(fx, sx.thunk(0.25, 120) * 0.55, 0.68)
    e0 = PRE + AT                                                     # the new beat
    si.add(fx, sx.whoosh(0.24) * 0.34, e0 + 0.02)                     # Pam throws
    si.add(fx, sx.whoosh(0.14) * 0.28, e0 + 0.26)                     # the whizz in
    si.add(fx, bonk() * 0.55, e0 + 0.40)                              # BONK
    si.add(fx, sx.whoosh(0.3) * 0.22, e0 + 0.47)                      # the plank goes over
    si.add(fx, sx.whoosh(0.12) * 0.14, PRE + EXTRA + 28.08)           # the bar slips off
    rng = np.random.default_rng(3)
    room = si.lp(rng.standard_normal(n), 160) * 0.02
    st = np.stack([fx, fx], 1)
    p0 = int(PRE * sr)
    st[p0:p0 + len(a)] += a
    p1 = p0 + len(a) + int(EXTRA * sr)
    st[p1:p1 + len(b)] += b
    quiet = np.ones(n); quiet[p0:p0 + len(a)] = 0; quiet[p1:p1 + len(b)] = 0
    st += np.stack([room * quiet] * 2, 1)
    sf.write(out, st.astype(np.float32), sr)
    print(out, round(len(st) / sr, 3))


if __name__ == "__main__":
    main()
