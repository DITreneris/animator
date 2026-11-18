"""v9 (18 Nov), for ss_anim10.py: v8 with a new take of Don's "Sofia." (ss_takes/08_v9.npy: Kokoro am_onyx,
"So-fee-ah." at 0.9, the house best-of-three; Whisper heard the old one as "Soviet"). Writes ss_mix_v9.wav.
v8 (18 Nov), for ss_anim8.py: v5 without the cap pop (the lipstick is open from frame 0). Writes ss_mix_v8.wav.
v5 (18 Nov), for ss_anim5.py: the cold open 1.3x slower (0..1 s -> 0..1.3 s), everything after it 0.3 s later.
Writes ss_mix_v5.wav. v4 (18 Nov), for ss_anim4.py: the cold open retimed (her head comes down 0.06 s, the kiss 0.24 s, back up 0.34 s,
THUNK 0.66 s, the cap 0.86 s). Writes ss_mix_v4.wav. v3 (18 Nov), a copy of ss_sound.py (kept) for ss_anim3.py: the cold open's tag whoosh, the kiss, the THUNK on the
kiss, and the cap pop moved to the later uncap. Writes ss_mix_v3.wav (the lip data is v1's, unchanged: ss_lips_v3.json).

Sound for "Secret Santa", animatic v1. The takes (ss_takes/, ss_takes_v1.json) are placed by ss_timing.remap; the
effects are written in storyboard-v2 time (ss_sb.py) and placed the same way. An original soft jingle-bell bed (glock
melody, sleigh-bell shakes, a low bass, about 110 bpm, G-Em-C-D) ducks under the lines, goes low under Pam's hurt and
her tag (7-9) and drops out entirely with the kiss stamp (13): Pam's stare and the robot's lines play in the quiet.
Don's entrance gets a tiny heroic brass sting, cut dead by the robot's THUNK. The three stamps grow: THUNK, THUNK!,
THUNK. (take A). Synth effects only.
Usage: python3 ss_sound.py -> ss_mix_v1.wav, ss_lips_v1.json (per-frame loudness for lip-sync)"""
import json
import numpy as np
import soundfile as sf
import sound_iwry as si
import sound_xmas as sx
import ss_sb
import ss_timing as T

SR = si.SR
P = ss_sb.PANELS
DUR = round(T.duration(P) + 0.8 + 0.3, 3)
L = int(SR * DUR)
rng = np.random.default_rng(61)
add, lp, tt = si.add, si.lp, si.tt
TAKES = json.load(open("ss_takes_v1.json"))
START = {fn.__name__: t0 for t0, t1, fn in P}


EXTRA, HOLD_AT = 0.8, 38.951                       # v4.1: the film is 0.8 s longer after the tags insert (ss_anim4)


def R(t):
    a = T.remap(t, P)
    a = a + EXTRA if a > HOLD_AT else a
    return a * 1.3 if a <= 1.0 else a + 0.3                     # v5


# ---------------------------------------------------------------- effects
def pop(f0=520, d=0.09):
    t = tt(d)
    return np.sin(2 * np.pi * (f0 + 900 * t / d) * t) * np.exp(-t * 45)


def click(f=3000, g=1.0):
    t = tt(0.05)
    return (np.sign(np.sin(2 * np.pi * f * t)) * 0.4 + lp(rng.standard_normal(len(t)), 1)) * np.exp(-t * 110) * g


def ding(f=1320, d=0.8):
    t = tt(d)
    return (np.sin(2 * np.pi * f * t) + 0.4 * np.sin(2 * np.pi * 2 * f * t)) * np.exp(-t * 5)


def buzz(d=0.45):
    t = tt(d)
    return np.sign(np.sin(2 * np.pi * 110 * t)) * 0.45 * np.minimum(1, (d - t) * 20)


def thud(f=70, d=0.5):
    t = tt(d)
    return (np.sin(2 * np.pi * f * t) + 0.5 * lp(rng.standard_normal(len(t)), 20)) * np.exp(-t * 9)


def stamp(weight):
    """1: an ordinary office THUNK; 2: THUNK!, heavier, a wood crack; 3: THUNK., the biggest, a low boom under it."""
    a = np.zeros(int(0.35 * SR))
    add(a, sx.thunk(0.25, 120), 0.0, 0.7); add(a, thud(90, 0.3), 0.0, 0.5)
    if weight >= 2:
        a = np.concatenate([a, np.zeros(SR)])[:int(0.6 * SR)]
        add(a, thud(65, 0.5), 0.0, 0.8)
        add(a, lp(rng.standard_normal(int(0.05 * SR)), 1) * np.exp(-tt(0.05) * 60), 0.0, 0.5)
    if weight >= 3:
        a = np.concatenate([a, np.zeros(SR)])
        add(a, sx.boom(), 0.0, 0.9)
    return a * (0.8, 1.0, 1.15)[weight - 1]


def sting(cut=0.42):
    """A tiny heroic brass sting (saw-ish triad, a rising fifth), cut dead after `cut` seconds."""
    t = tt(cut)
    out = np.zeros(len(t))
    for f in (196, 247, 294, 392):
        ph = 2 * np.pi * f * t * (1 + 0.003 * np.sin(2 * np.pi * 5 * t))
        out += sum(np.sin(h * ph) / h for h in range(1, 7))
    out *= np.minimum(1, t / 0.02)
    return out / np.max(np.abs(out)) * 0.6


def squeak(d=0.22):
    t = tt(d)
    f = 2400 + 500 * np.sin(2 * np.pi * 9 * t)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / d) * 0.35


def scratch(d):
    n = rng.standard_normal(int(d * SR))
    t = tt(d)
    g = 0.5 + 0.5 * np.abs(np.sin(2 * np.pi * 7 * t))
    return (n - lp(n, 3)) * g * np.sin(np.pi * t / d) * 0.12


def mwah():
    t = tt(0.16)
    smack = lp(rng.standard_normal(len(t)), 2) * np.exp(-t * 60) * 0.6
    tone = np.sin(2 * np.pi * (300 - 120 * t / 0.16) * t) * np.exp(-t * 18) * 0.4
    return smack + tone


# ---------------------------------------------------------------- the bed
def bells(d=0.18):
    out = np.zeros(int(d * SR))
    for i in range(6):
        add(out, np.sin(2 * np.pi * (5200 + 900 * rng.random()) * tt(0.04)) * np.exp(-tt(0.04) * 110), i * 0.022, 0.35)
    return out


def bed(d):
    out = np.zeros(int(d * SR) + SR)
    beat = 60 / 110
    roots = (196, 165, 131, 147)                                     # G, Em, C, D
    melody = [784, 740, 659, 587, 659, 740, 784, 0, 659, 587, 523, 494, 523, 587, 659, 0]
    n = int(d / (beat / 2)) + 1
    for i in range(n):
        bar = (i // 8) % 4
        m = melody[i % 16]
        if m and i % 2 == 0:
            add(out, sx.glock(m, 0.5), i * beat / 2, 0.30)
        if i % 4 == 0:
            t = tt(0.5)
            add(out, np.sin(2 * np.pi * roots[bar] / 2 * t) * np.exp(-t * 5), i * beat / 2, 0.55)
        add(out, bells(), i * beat / 2, 0.22 if i % 2 == 0 else 0.12)
    return out[:int(d * SR)]


def mix():
    voice = np.zeros(L)
    lines = []
    for l in TAKES:
        a = np.load("ss_takes/08_v9.npy" if l["id"] == 8 else "ss_takes/%02d.npy" % l["id"])   # v9: "Sofia." again
        a0 = R(START[l["panel"]] + l["at"])
        add(voice, a, a0)
        lines.append((l["who"], l["text"], a0, a))
        print(f'{l["who"]} {l["text"]:46s} {a0:6.2f}-{a0 + len(a) / SR:6.2f}')
    fx = np.zeros(L)

    def addf(a, t, g=1.0):
        add(fx, a, R(t), g)
    S = START
    addf(sx.whoosh(0.15), S["s1"] + 0.06, 0.25)                              # v4: her head comes down
    addf(mwah(), S["s1"] + 0.22, 0.7)                                        # v4: the kiss
    addf(sx.whoosh(0.12), S["s1"] + 0.34, 0.18)                              # v4: and back up
    addf(stamp(1), S["s1"] + 0.66, 1.0)                                      # v4: THUNK on the kiss
    addf(sx.whoosh(0.25), S["s1"] + 1.0, 0.25)                               # 1: the pull-out
    addf(click(3400, 0.5), S["s2b"] + 0.05, 0.5)                             # 2: the compact
    addf(thud(65, 0.5), S["s3b"], 1.0); addf(sx.thunk(0.2, 140), S["s3b"] + 0.02, 0.6)   # 3: the door bangs
    cut = R(S["s3b"] + 1.3) - R(S["s3b"] + 0.05)                             # the sting, cut dead by the THUNK
    addf(sting(cut), S["s3b"] + 0.05, 0.35)
    addf(stamp(1), S["s3b"] + 1.3, 0.8); addf(ding(1568, 0.5), S["s3b"] + 1.35, 0.15)
    addf(click(2600, 0.6), S["s4b"] + 0.55, 0.6)                             # 4: the glasses fold
    addf(pop(), S["s4b"] + 2.05, 0.4)                                        # 4: her heart
    addf(squeak(), S["s6b"] + 0.8, 0.5); addf(ding(2640, 0.4), S["s6b"] + 0.95, 0.12)   # 6: the dome, the glint
    addf(scratch(0.75), S["s8b"] + 0.25, 1.0); addf(scratch(0.65), S["s8b"] + 1.15, 1.0)  # 8: the pen
    addf(mwah(), S["s8b"] + 1.95, 0.7)                                       # 8: the kiss
    addf(buzz(), S["s10b"] + 0.25, 0.3)                                      # 10: red
    addf(stamp(1), S["s11b"] + 0.33, 1.0)                                    # 11: THUNK
    addf(stamp(2), S["s12b"] + 0.4, 1.0)                                     # 12: THUNK!
    addf(stamp(3), S["s13b"] + 0.95, 1.0)                                    # 13: THUNK.
    addf(thud(110, 0.25), S["s15b"] + 1.1, 0.5)                              # 15: Don sets his gift down
    addf(sx.rustle(0.5), S["s15b"] + 1.8, 0.5)                               # 15: her present slides to UNCLAIMED
    addf(ding(), S["s15b"] + 3.3, 0.35); addf(stamp(1), S["s15b"] + 3.3, 0.35)   # 15: the tick, APPROVED
    addf(sx.rustle(0.35), S["s16b"] + 0.05, 0.4)                             # 16: a fresh tag
    music = bed(DUR)
    level = np.ones(L)
    i0, i1 = int(R(S["s7b"]) * SR), int(R(S["s10b"]) * SR)
    level[i0:i1] = 0.45                                                      # low under the hurt and the tag
    i0 = int(R(S["s13b"] + 1.0) * SR)
    level[i0:] = 0.0                                                         # out with the kiss stamp
    level = lp(level, 2400)
    room = lp(rng.standard_normal(L), 160) * 0.04
    venv = lp(np.abs(voice), 4800)
    duck = 1 - 0.55 * np.clip(venv / 0.05, 0, 1)
    out = voice + fx * duck + music * 0.12 * level * duck + room
    out = np.tanh(out * 1.6) / 1.6
    out /= max(1.0, np.max(np.abs(out)) / 0.85)
    sf.write("ss_mix_v9.wav", np.stack([out, out], 1), SR)
    nf = int(DUR * 30) + 1
    lips = {"DON": [0.0] * nf, "SOF": [0.0] * nf, "PAM": [0.0] * nf, "ROB": [0.0] * nf, "lines": []}
    hop = SR // 30
    for who, txt, t0, a in lines:
        e = np.array([np.sqrt(np.mean(a[j:j + hop] ** 2)) for j in range(0, len(a), hop)])
        e = e / e.max()
        f0 = int(round(t0 * 30))
        for j, v in enumerate(e):
            if f0 + j < nf:
                lips[who][f0 + j] = round(float(v), 3)
        lips["lines"].append([who, txt, round(t0, 3), round(t0 + len(a) / SR, 3)])
    json.dump(lips, open("ss_lips_v9.json", "w"))
    print("peak", round(float(np.max(np.abs(out))), 3), "dur", DUR)


if __name__ == "__main__":
    mix()
