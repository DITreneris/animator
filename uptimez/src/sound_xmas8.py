"""Sound for "Happy Compliance" animation v8 (xmas_anim8.py). v2's mix is rebuilt by sound_xmas.mix() with three of its
effects taken out (the off-screen THUD at 27.2 s, the bauble clink after it and the razor's slide: the razor is gone and
the THUD now lands with Don) into xmas_mix_v8base.wav; xmas_mix_v1.wav and its lip data are restored untouched. Then:
PRE s of cold open in front; the BEAT after "Merry Christmas, Don." (throw, whizz, BONK, the plank going over); the LAND
beat before "Happy compliance!" (Don drops in: a THUD and the bauble's clink); the UP beat after the alarm (a groan of a
servo-ish wobble, three slipper shuffles off); room tone for the loop tail. Writes xmas_mix_v8.wav.
python3 sound_xmas8.py"""
import inspect
import os
import shutil
import numpy as np
import soundfile as sf
import sound_xmas as S
import sound_iwry as si
import sound_xmas7 as S7

PRE, TAIL, AT, BEAT, LAND, UP = 0.8, 0.4, 26.9, 0.9, 0.7, 1.2


def base(out="xmas_mix_v8base.wav"):
    src = inspect.getsource(S.mix)
    for line in ('    add(fx, boom(), 27.2, 0.9)                                 # 11: off-screen THUD\n',
                 '    add(fx, clink(), 27.25, 0.2)                               # a bauble rolls\n',
                 '    add(fx, scrape(0.55, 40), 27.3, 0.35)                      # the razor slides in\n'):
        assert line in src, line
        src = src.replace(line, "")
    keep = {}
    for f in ("xmas_mix_v1.wav", "xmas_lips_v1.json"):
        if os.path.exists(f):
            shutil.copy(f, f + ".keep"); keep[f] = f + ".keep"
    ns = dict(S.__dict__)
    exec(compile(src, "sound_xmas_mix_v8", "exec"), ns)
    S.TAKES.clear()
    try:
        ns["mix"]()
        shutil.move("xmas_mix_v1.wav", out)
    finally:
        for f, k in keep.items():
            shutil.move(k, f)
    return out


def main(out="xmas_mix_v8.wav"):
    mix, sr = sf.read(base())
    cut = int(AT * sr)
    a, b = mix[:cut], mix[cut:]
    n = int((PRE + BEAT + LAND + UP + TAIL) * sr) + len(mix)
    fx = np.zeros(n)
    t = np.arange(int(0.15 * sr)) / sr
    si.add(fx, S.whoosh(0.22) * 0.30, 0.08)                                         # the cold open
    si.add(fx, np.sin(2 * np.pi * 180 * t) * np.sin(np.pi * t / 0.15) * 0.06, 0.35)
    si.add(fx, S.whoosh(0.16) * 0.22, 0.50)
    si.add(fx, S.thunk(0.25, 120) * 0.55, 0.68)
    e0 = PRE + AT                                                                   # BEAT
    si.add(fx, S.whoosh(0.24) * 0.34, e0 + 0.02)
    si.add(fx, S.whoosh(0.14) * 0.28, e0 + 0.26)
    si.add(fx, S7.bonk() * 0.55, e0 + 0.40)
    si.add(fx, S.whoosh(0.3) * 0.22, e0 + 0.47)
    l0 = e0 + BEAT                                                                  # LAND
    si.add(fx, S.whoosh(0.25) * 0.2, l0 + 0.05)
    si.add(fx, S.boom() * 0.9, l0 + 0.30)
    si.add(fx, S.clink() * 0.2, l0 + 0.36)
    si.add(fx, S.whoosh(0.12) * 0.14, PRE + BEAT + LAND + 28.08)                    # the bar slips off
    u0 = PRE + BEAT + LAND + len(mix) / sr                                          # UP
    tt = np.arange(int(0.5 * sr)) / sr
    si.add(fx, np.sin(2 * np.pi * np.cumsum(140 + 60 * tt / 0.5) / sr) * np.sin(np.pi * tt / 0.5) * 0.08, u0)
    for j in range(3):
        si.add(fx, S.slipper() * 0.35, u0 + 0.55 + 0.22 * j)
    rng = np.random.default_rng(3)
    room = si.lp(rng.standard_normal(n), 160) * 0.02
    st = np.stack([fx, fx], 1)
    p0 = int(PRE * sr)
    st[p0:p0 + len(a)] += a
    p1 = p0 + len(a) + int((BEAT + LAND) * sr)
    st[p1:p1 + len(b)] += b
    quiet = np.ones(n); quiet[p0:p0 + len(a)] = 0; quiet[p1:p1 + len(b)] = 0
    st += np.stack([room * quiet] * 2, 1)
    sf.write(out, st.astype(np.float32), sr)
    print(out, round(len(st) / sr, 3))


if __name__ == "__main__":
    main()
