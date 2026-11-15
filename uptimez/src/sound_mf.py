"""Sound for "Mandatory Fun", animatic v1. Lines and effects are written in storyboard-v2 time (mf_sb.py) and placed
through mf_timing.remap (37.25 s). Voices (Kokoro, same cast): Don am_onyx, Sofia af_bella, Pam bf_emma (the
Christmas audition A), the robot voice B (am_echo, robotized, flat). Pam's "Approved!" is her one loud line: her take
pitched up a touch (and so a little faster), driven harder and louder, with a tiny room slap. An original,
relentlessly upbeat corporate-training jingle (marimba plucks, bass, a soft hat, 120 bpm, C-Am-F-G) runs under it all,
dropped low under the confession, the approval and the ending. Synth effects only.
Usage: KOKORO_DIR=... python3 sound_mf.py mix -> mf_mix_v1.wav, mf_lips_v1.json (per-frame loudness for lip-sync)"""
import sys
import json
import numpy as np
import soundfile as sf
import sound_iwry as si
import sound_xmas as sx
import mf_sb
import mf_timing as T

SR = si.SR
P = mf_sb.PANELS
DUR = round(T.duration(P), 3)
L = int(SR * DUR)
rng = np.random.default_rng(57)
add, lp, tt = si.add, si.lp, si.tt


def R(t):
    return T.remap(t, P)


def shot_end(t):
    for a0, a1, fn, t0, t1, mode in T.build(P):
        if t0 <= t < t1:
            return a1
    return DUR


LINES = [   # (who, text, storyboard start, how)
    ("ROB", "Attendance is mandatory. So is fun.", 0.45, "robot"),
    ("DON", "A.I. Police! Who's going to jail?", 3.65, ("am_onyx", 1.0)),
    ("DON", "Sofia, you're under arrest.", 5.65, ("am_onyx", 1.0)),
    ("SOF", "For what?", 7.6, ("af_bella", 1.0)),
    ("DON", "Stealing my attention.", 8.5, ("am_onyx", 1.0)),
    ("PAM", "Officer? I confess.", 11.0, "pam"),
    ("ROB", "Failure to enjoy training. Detention required.", 14.8, "robot"),
    ("DON", "You can't arrest a cop!", 16.4, ("am_onyx", 1.0)),
    ("ROB", "Human approval required.", 18.95, "robot"),
    ("PAM", "Approved!", 20.22, "approved"),
    ("PAM", "So... dinner?", 27.6, "pam"),
    ("ROB", "Mandatory fun. Successful.", 30.9, "robot"),
]
TAKES = []


def approved():
    """Pam's one loud line: pitched up ~6 % (resampled, so also shorter), driven, louder, a small room slap."""
    a = sx.pam_line("Approved!", "A")
    b = np.interp(np.arange(0, len(a) - 1, 1.06), np.arange(len(a)), a)
    b = np.tanh(b * 9) / 9 * 2.1
    out = np.concatenate([b, np.zeros(int(0.12 * SR))])
    for d, g in ((0.023, 0.33), (0.041, 0.2), (0.067, 0.1)):
        add(out, b, d, g)
    return out / np.sqrt(np.mean(out ** 2)) * 0.17


def make_line(who, txt, how):
    if how == "approved":
        return approved()
    if how == "pam":
        return sx.pam_line(txt, "A")
    if how == "robot":
        return si.robot_line(txt, "B", "normal")
    v, sp = how
    return sx.best_take(txt, v, sp, "en-us")


# ---------------------------------------------------------------- the jingle
def mallet(f, d=0.45):
    t = tt(d)
    return (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 4 * f * t) * np.exp(-t * 30)) * np.exp(-t * 9)


def jingle(d):
    out = np.zeros(int(d * SR) + SR)
    beat = 0.5
    chords = [(262, 330, 392), (220, 262, 330), (175, 220, 262), (196, 247, 294)]
    bass = (131, 110, 87, 98)
    melody = [523, 587, 659, 523, 440, 523, 587, 0, 440, 523, 587, 659, 587, 523, 494, 0]
    n = int(d / (beat / 2)) + 1
    for i in range(n):
        bar = (i // 8) % 4
        ch = chords[bar]
        if i % 2 == 0:
            add(out, mallet(ch[(i // 2) % 3], 0.4), i * beat / 2, 0.45)
        m = melody[i % 16]
        if m and i % 2 == 0:
            add(out, mallet(m, 0.35), i * beat / 2, 0.4)
        if i % 4 == 0:
            t = tt(0.4)
            add(out, np.sin(2 * np.pi * bass[bar] * t) * np.exp(-t * 6), i * beat / 2, 0.7)
        add(out, lp(rng.standard_normal(int(0.03 * SR)), 1) * np.exp(-tt(0.03) * 120), i * beat / 2, 0.08)
    return out[:int(d * SR)]


# ---------------------------------------------------------------- effects
def sweep(d=0.6):
    t = tt(d)
    return np.sin(2 * np.pi * np.cumsum(500 + 700 * t / d) / SR) * 0.35 * np.sin(np.pi * t / d)


def buzz(d=0.45):
    t = tt(d)
    return np.sign(np.sin(2 * np.pi * 110 * t)) * 0.5 * np.minimum(1, (d - t) * 20)


def ding():
    t = tt(0.8)
    return (np.sin(2 * np.pi * 1320 * t) + 0.4 * np.sin(2 * np.pi * 2640 * t)) * np.exp(-t * 5)


def glitch(d=0.3):
    t = tt(d)
    x = np.sign(np.sin(2 * np.pi * (300 + 900 * (np.floor(t * 40) % 3)) * t)) * 0.3
    return x * (np.floor(t * 60) % 2)


def pop():
    t = tt(0.09)
    return np.sin(2 * np.pi * (520 + 900 * t / 0.09) * t) * np.exp(-t * 45)


def jingle_chain(d=0.35):
    out = np.zeros(int(d * SR))
    for i in range(7):
        add(out, np.sin(2 * np.pi * (2500 + 400 * rng.random()) * tt(0.03)) * np.exp(-tt(0.03) * 120), i * 0.045, 0.5)
    return out


def click(f=2400, g=1.0):
    t = tt(0.06)
    return (np.sign(np.sin(2 * np.pi * f * t)) * 0.5 + lp(rng.standard_normal(len(t)), 1)) * np.exp(-t * 90) * g


def step():
    t = tt(0.09)
    return (np.sin(2 * np.pi * 110 * t) + 0.6 * lp(rng.standard_normal(len(t)), 6)) * np.exp(-t * 45)


def twang():
    t = tt(0.55)
    x = sum(np.sin(2 * np.pi * 620 * (1 - 0.06 * t) * h * t) / h for h in (1, 2.01, 3.03, 4.1))
    return (x * np.exp(-t * 7) + lp(rng.standard_normal(len(t)), 2) * np.exp(-t * 30) * 0.8) * 0.55


def thud(f=70, d=0.5):
    t = tt(d)
    return (np.sin(2 * np.pi * f * t) + 0.5 * lp(rng.standard_normal(len(t)), 20)) * np.exp(-t * 9)


def creak(d=0.35):
    t = tt(d)
    f = 170 + 50 * np.sin(2 * np.pi * 4 * t)
    return np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.18 * np.sin(np.pi * t / d)


def tick():
    t = tt(0.04)
    return np.sin(2 * np.pi * 3200 * t) * np.exp(-t * 160) * 0.4


def mix():
    voice = np.zeros(L)
    late = 0
    for who, txt, t0, how in LINES:
        a0, end_ok = R(t0), shot_end(t0)
        a = make_line(who, txt, how)
        add(voice, a, a0)
        TAKES.append((who, txt, a0, a))
        end = a0 + len(a) / SR
        ok = end <= end_ok + 0.05
        late += not ok
        print(f"{who} {txt:48s} {a0:5.2f}-{end:5.2f} shot ends {end_ok:5.2f}", "OK" if ok else "LATE")
    fx = np.zeros(L)

    def addf(a, t, g=1.0):
        add(fx, a, R(t), g)
    addf(thud(80, 0.35), 0.0, 0.9); addf(sx.whoosh(0.15), 0.0, 0.4)          # 1: the slide slams on
    addf(thud(65, 0.5), 3.4, 1.0); addf(sx.thunk(0.2, 140), 3.42, 0.6)       # 3: the door bangs
    addf(pop(), 6.98, 0.4)                                                   # 4b: 💗
    addf(sx.rustle(0.3), 10.15, 0.45)                                        # 4: the page turn
    addf(sweep(0.6), 13.9, 0.5)                                              # 6a: the scan
    addf(buzz(), 14.62, 0.3)                                                 # 6b: red
    addf(jingle_chain(), 18.1, 0.5)                                          # 8a: the cuffs lifted
    addf(glitch(), 18.6, 0.25)                                               # 8a: the freeze
    addf(ding(), 21.02, 0.35)                                                # 9b: accepted
    addf(click(2200, 0.6), 22.4, 0.7)                                        # 10: the robot's click
    addf(click(1800, 1.0), 23.2, 1.0)                                        # 10: hers, louder
    for s in np.arange(24.25, 25.8, 0.31):                                   # 11: Sofia walks out
        addf(step(), s, 0.3)
    addf(sx.whoosh(0.4), 24.5, 0.4)                                          # 11: the lunge
    addf(twang(), 25.0, 0.8)                                                 # 11: taut
    addf(thud(90, 0.3), 25.25, 0.7); addf(pop(), 25.25, 0.4)                 # 11: the release, the cap pops
    addf(creak(), 25.64, 0.6); addf(thud(55, 0.4), 25.7, 0.8)                # 11: into the chair
    addf(thud(240, 0.12), 25.85, 0.4)                                        # 11: the cap lands
    addf(tick(), 26.25, 0.9)                                                 # 11: the glasses
    addf(sweep(0.7), 29.6, 0.5)                                              # 12: the scan crosses Don
    addf(ding(), 30.42, 0.4)                                                 # 12: green
    music = np.zeros(L)
    add(music, jingle(DUR), 0.0, 1.0)
    level = np.ones(L)
    for s0, s1 in ((10.9, 12.5), (19.9, 21.8), (29.4, 33.0)):                # dropped low under these
        i0, i1 = int(R(s0) * SR), int(min(DUR, R(s1 - 1e-3)) * SR)
        level[i0:i1] = 0.35
    level = lp(level, 4800)
    room = lp(rng.standard_normal(L), 160) * 0.05
    venv = lp(np.abs(voice), 4800)
    duck = 1 - 0.55 * np.clip(venv / 0.05, 0, 1)
    out = voice + fx * duck + music * 0.11 * level * duck + room * duck
    out = np.tanh(out * 1.6) / 1.6
    out /= max(1.0, np.max(np.abs(out)) / 0.85)
    sf.write("mf_mix_v1.wav", np.stack([out, out], 1), SR)
    nf = int(DUR * 30) + 1
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
    json.dump(lips, open("mf_lips_v1.json", "w"))
    print("peak", round(float(np.max(np.abs(out))), 3), "late", late, "dur", DUR)


if __name__ == "__main__" and sys.argv[1:] == ["mix"]:
    mix()
