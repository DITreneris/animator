"""Sound for the Thanksgiving film "Raises for Everyone". Times below are storyboard-v3 times; they are re-timed to
the animatic (tg_timing.py: four shots held longer for the real takes, 36.6 s) when mixed. Voices (Kokoro): Don am_onyx,
Sofía af_bella, Pam bf_emma (the Christmas audition A), the robot voice B (am_echo, robotized); "OK. Signed." is the
robot muffled behind the turkey leg (low-passed, quieter). An original plucked-guitar bed (Karplus-Strong, 104 bpm,
too cheerful) stops dead on Pam's "No." and comes back on "Sign it." as if nothing happened. Synth effects only.
Usage: KOKORO_DIR=... python3 sound_tg.py mix  -> tg_mix_v1.wav, tg_lips_v1.json (per-frame loudness for lip-sync)"""
import sys
import json
import numpy as np
import soundfile as sf
import sound_iwry as si
import sound_xmas as sx

SR = si.SR
import tg_sb
import tg_timing as T


def R(t):
    return T.remap(t, tg_sb.PANELS)


DUR = round(T.duration(tg_sb.PANELS), 3)
L = int(SR * DUR)
rng = np.random.default_rng(41)
add, lp, tt = si.add, si.lp, si.tt

LINES = [   # (who, text, start, slot end, how)
    ("DON", "Raises for everyone! Sign here.", 0.12, 2.55, ("am_onyx", 1.0)),
    ("SOF", "Still hoping for a raise?", 3.95, 5.75, ("af_bella", 1.0)),
    ("PAM", "I'm expecting.", 5.9, 7.0, "pam"),
    ("DON", "Boy or girl? Ha!", 7.05, 8.8, ("am_onyx", 1.05)),
    ("ROB", "Policy violation.", 9.68, 11.2, "normal"),
    ("PAM", "A raise for saying we don't want one?", 12.3, 14.75, "pam"),
    ("DON", "Now you're getting it.", 14.8, 16.0, ("am_onyx", 1.08)),
    ("PAM", "No.", 16.15, 17.0, "pam"),
    ("DON", "You failed.", 17.65, 18.6, ("am_onyx", 1.0)),
    ("SOF", "She refused. She didn't fail.", 18.65, 20.2, ("af_bella", 1.05)),
    ("DON", "Same thing here.", 20.78, 21.7, ("am_onyx", 1.0)),
    ("PAM", "You're a walking policy violation.", 24.2, 25.9, "pam"),
    ("DON", "H.R. Back me up.", 25.95, 27.4, ("am_onyx", 1.05)),
    ("ROB", "Accurate.", 28.68, 29.5, "normal"),
    ("DON", "Sign it.", 31.58, 32.25, ("am_onyx", 1.0)),
    ("ROB", "Okay. Signed.", 32.32, 33.0, "muffled"),
]
TAKES = []


def pluck(f, d=0.9):
    """Karplus-Strong string: a noise burst in a delay line, averaged and damped each pass."""
    n = int(SR / f)
    buf = list(rng.uniform(-1, 1, n))
    out = np.zeros(int(d * SR))
    for i in range(len(out)):
        j = i % n
        out[i] = buf[j]
        buf[j] = 0.497 * (buf[j] + buf[(j + 1) % n])
    return out * np.exp(-tt(d) * 2.2)


_PL = {}


def pl(f):
    if f not in _PL:
        _PL[f] = pluck(f)
    return _PL[f]


def bed(d):
    """An invented, slightly too cheerful folk strum: I-V-vi-IV in G, 104 bpm, eighth-note picking."""
    out = np.zeros(int(d * SR) + SR)
    beat = 60 / 104
    chords = [(196, 247, 294, 392), (147, 220, 294, 370), (165, 247, 330, 392), (131, 196, 262, 330)]
    n = int(d / (beat / 2)) + 1
    for i in range(n):
        ch = chords[(i // 8) % 4]
        f = ch[[0, 2, 1, 3, 2, 1, 3, 2][i % 8]]
        add(out, pl(f), i * beat / 2, 0.5 if i % 2 == 0 else 0.32)
    out = out[:int(d * SR)]
    fade = int(0.03 * SR)
    out[-fade:] *= np.linspace(1, 0, fade)
    return out


def pop():
    t = tt(0.09)
    return np.sin(2 * np.pi * (520 + 900 * t / 0.09) * t) * np.exp(-t * 45)


def ding():
    t = tt(0.7)
    return (np.sin(2 * np.pi * 1320 * t) + 0.4 * np.sin(2 * np.pi * 2640 * t)) * np.exp(-t * 5)


def buzz(d=0.45):
    t = tt(d)
    return np.sign(np.sin(2 * np.pi * 110 * t)) * 0.5 * np.minimum(1, (d - t) * 20)


def rip(d=0.35):
    return lp(rng.standard_normal(int(d * SR)), 3) * np.exp(-tt(d) * 6) * np.minimum(1, tt(d) * 40)


def crunch():
    out = np.zeros(int(0.3 * SR))
    for i in range(6):
        add(out, lp(rng.standard_normal(int(0.03 * SR)), 2) * np.exp(-tt(0.03) * 60), i * 0.04, 1 - i * 0.12)
    return out


def scratch(d):
    t = tt(d)
    return lp(rng.standard_normal(len(t)), 2) * (0.5 + 0.5 * np.sin(2 * np.pi * 9 * t)) * 0.4


def sweep(d=0.8):
    t = tt(d)
    return np.sin(2 * np.pi * np.cumsum(600 + 500 * np.sin(np.pi * t / d)) / SR) * 0.35 * np.sin(np.pi * t / d)


def muffle(a):
    b = lp(lp(a, 14), 10)
    return b / np.sqrt(np.mean(b ** 2)) * 0.06


def make_line(who, txt, how):
    if how == "pam":
        return sx.pam_line(txt, "A")
    if who == "ROB":
        return muffle(si.robot_line(txt, "B", "normal")) if how == "muffled" else si.robot_line(txt, "B", how)
    v, sp = how
    return sx.best_take(txt, v, sp, "en-us")


def mix():
    voice = np.zeros(L)
    late = 0
    for who, txt, t0, slot, how in LINES:
        t0, slot = R(t0), T.remap_end(slot, tg_sb.PANELS)
        a = make_line(who, txt, how)
        add(voice, a, t0)
        TAKES.append((who, txt, t0, a))
        end = t0 + len(a) / SR
        ok = end <= slot + 0.1
        late += not ok
        print(f"{who} {txt:38s} {t0:5.2f}-{end:5.2f} slot {slot:5.2f}", "OK" if ok else "LATE")
    fx = np.zeros(L)

    def addf(buf, a, t, g=1.0):
        add(buf, a, R(t), g)
    addf(fx, sx.thunk(0.25, 90), 0.1, 0.8)                         # 1: the form slapped down
    addf(fx, sx.rustle(0.3), 2.65, 0.25)                           # 2: paper
    addf(fx, sx.thunk(0.2, 110), 8.05, 0.6)                        # 4: Don slaps the table
    addf(fx, pop(), 8.9, 0.35)                                     # 4b: 🙄 pop
    addf(fx, buzz(), 9.62, 0.22)                                   # 5: red verdict
    for tp in (11.3, 11.55, 11.8, 12.05):                         # 6: the tap
        addf(fx, si.tick(1500), tp, 0.25)
    addf(fx, sx.scrape(0.5, 30), 16.05, 0.25)                      # 7: the form pushed back
    addf(fx, rip(), 17.05, 0.45)                                   # 8a: the leg torn off
    addf(fx, crunch(), 20.48, 0.5)                                 # 8c: the bite
    addf(fx, pop(), 21.8, 0.35)                                    # 8d: 😮‍💨 pop
    addf(fx, sx.rustle(0.4), 22.7, 0.3)                            # 9: she rises
    addf(fx, pop(), 23.45, 0.3)                                    # 9: 💗 pop
    addf(fx, sweep(), 27.4, 0.3)                                   # 10b: the scan
    addf(fx, ding(), 28.65, 0.3)                                   # 10b: green verdict
    addf(fx, sx.whoosh(0.2), 30.6, 0.3)                            # 11: the leg goes up
    addf(fx, sx.scrape(0.5, 30), 30.9, 0.25)                       # 11: the form slides to the robot
    addf(fx, scratch(0.7), 33.15, 0.5)                             # 11b: the robot signs
    addf(fx, sx.thunk(0.3, 70), 34.0, 1.0)                         # 11b: the stamp
    music = np.zeros(L)
    add(music, bed(R(16.15)), 0.0, 1.0)                           # stops dead on "No."
    add(music, bed(DUR - R(31.55)), R(31.55), 1.0)                      # back on "Sign it." as if nothing happened
    room = lp(rng.standard_normal(L), 160) * 0.05
    venv = lp(np.abs(voice), 4800)
    duck = 1 - 0.55 * np.clip(venv / 0.05, 0, 1)
    out = voice + fx * duck + music * 0.14 * duck + room * duck
    out = np.tanh(out * 1.6) / 1.6
    out /= max(1.0, np.max(np.abs(out)) / 0.85)
    sf.write("tg_mix_v1.wav", np.stack([out, out], 1), SR)
    nf = int(DUR * 30)
    lips = {"DON": [0.0] * nf, "SOF": [0.0] * nf, "PAM": [0.0] * nf, "ROB": [0.0] * nf, "lines": []}
    hop = SR // 30
    for who, txt, t0, a in TAKES:
        e = np.array([np.sqrt(np.mean(a[j:j + hop] ** 2)) for j in range(0, len(a), hop)])
        e = e / e.max()
        f0 = int(round(t0 * 30))
        for j, v in enumerate(e):
            if f0 + j < nf:
                lips[who][f0 + j] = round(float(v), 3)
        lips["lines"].append([who, txt, round(t0, 3), round(t0 + len(a) / SR, 3)])
    json.dump(lips, open("tg_lips_v1.json", "w"))
    print("peak", round(float(np.max(np.abs(out))), 3), "late", late)


if __name__ == "__main__" and sys.argv[1:] == ["mix"]:
    mix()
