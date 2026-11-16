"""The jazz-noir cue for "Office Noir: The Secret of a Stolen Heart" (numpy only, no music licence needed).
80 BPM, A minor: Am(maj7) | Fmaj7 | Dm7 | E7(b9). A walking upright bass, brushes and a swung ride, a vibraphone
comp and a muted horn that plays only in the gaps between the lines. Sections, from the beat starts in on_timing.json:
  A  the case (0.45 s -> shot 6): the groove, horn phrases on the fake draw and over the CCTV.
  -  shot 6 (the humiliation): out, dropped right on his eyes.
  B  Pam (7A -> shot 8): vibes only, soft, one chord a bar; out on "Objection." (the dry joke plays in silence).
  C  the brag (9a, 9b): the full band builds, the horn climbs; cut dead on DONNIE!.
music(T) returns the stem (the mix ducks it under the voices)."""
import numpy as np

SR = 48000
BPM = 80
BEAT = 60.0 / BPM
rng = np.random.default_rng(80)


def hz(n):
    """Note name -> Hz ("A2", "G#4", "Bb3")."""
    names = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
    k = names[n[0]]; i = 1
    if n[i] in "#b":
        k += 1 if n[i] == "#" else -1; i += 1
    return 440.0 * 2 ** ((k + 12 * (int(n[i:]) + 1) - 69) / 12)


CHORDS = [   # bass walk (4 beats), voicing
    (["A2", "C3", "E3", "G#2"], ["A3", "C4", "E4", "G#4"]),
    (["F2", "A2", "C3", "E3"], ["A3", "C4", "E4", "F4"]),
    (["D2", "F2", "A2", "C3"], ["F3", "A3", "C4", "D4"]),
    (["E2", "G#2", "B2", "D3"], ["G#3", "D4", "F4", "B3"]),
]


def tt(d):
    return np.arange(int(d * SR)) / SR


def lp(x, n):
    return np.convolve(x, np.ones(n) / n, mode="same")


def put(buf, a, t0, g=1.0):
    i = int(t0 * SR)
    if i >= len(buf) or i + len(a) <= 0:
        return
    a = a[max(0, -i):]; i = max(0, i)
    n = min(len(a), len(buf) - i)
    buf[i:i + n] += a[:n] * g


def bass(f, d=0.7):
    t = tt(d)
    a = np.sin(2 * np.pi * f * t) + 0.45 * np.sin(4 * np.pi * f * t) + 0.12 * np.sin(6 * np.pi * f * t)
    a *= np.minimum(1, t / 0.006) * np.exp(-t / 0.38)
    a[:int(0.02 * SR)] += lp(rng.standard_normal(int(0.02 * SR)), 12) * 0.5 * np.exp(-tt(0.02) / 0.006)  # the pluck
    return a * 0.5


def brush(d=BEAT):
    t = tt(d)
    return (rng.standard_normal(len(t)) - lp(rng.standard_normal(len(t)), 4)) * np.sin(np.pi * t / d) ** 2 * 0.035


def slap():
    t = tt(0.12)
    return (rng.standard_normal(len(t)) - lp(rng.standard_normal(len(t)), 3)) * np.exp(-t / 0.03) * 0.16


def ride(g=1.0):
    t = tt(0.6)
    a = sum(np.sin(2 * np.pi * f * t + p) for f, p in ((3120, 0), (4150, 1), (5230, 2), (6870, 3), (8010, 4)))
    return a * np.exp(-t / 0.22) * 0.018 * g


def kick():
    t = tt(0.25)
    return np.sin(2 * np.pi * (55 + 60 * np.exp(-t / 0.03)) * t) * np.exp(-t / 0.12) * 0.45


def vibe(f, d=2.2):
    t = tt(d)
    a = np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * f * 4 * t) * np.exp(-t / 0.15)
    return a * np.minimum(1, t / 0.004) * np.exp(-t / 0.9) * (1 + 0.25 * np.sin(2 * np.pi * 5.5 * t)) * 0.07


def chord(names, d=2.2, g=1.0):
    return sum(vibe(hz(n), d) for n in names) * g


def horn(f, d):
    """A muted horn: harmonics falling off, a breathy attack, vibrato that comes in late, a soft low-pass."""
    t = tt(d + 0.12)
    vib = 1 + 0.006 * np.sin(2 * np.pi * 5.2 * t) * np.minimum(1, t / 0.35)
    ph = 2 * np.pi * np.cumsum(f * vib) / SR
    a = sum(np.sin(k * ph) / k ** 1.3 for k in range(1, 9))
    a = lp(a, 5)
    env = np.minimum(1, t / 0.06) * np.where(t < d, 1.0, np.exp(-(t - d) / 0.05))
    breath = lp(rng.standard_normal(len(t)), 6) * 0.04 * np.exp(-t / 0.08)
    return (a * 0.12 + breath) * env


def phrase(buf, t0, notes, g=1.0):
    """notes: (name, beats) or (None, beats) for a rest."""
    t = t0
    for n, b in notes:
        if n:
            put(buf, horn(hz(n), b * BEAT * 0.94), t, g)
        t += b * BEAT


def groove(buf, t0, t1, level=1.0, drums=1.0, walk=True, comp=True, bar0=0):
    """The band from t0 to t1 on its own grid starting at t0 (each section re-phases on its first beat)."""
    t, k = t0, 0
    while t < t1 - 0.05:
        bar, beat = divmod(k, 4)
        walkn, voicing = CHORDS[(bar + bar0) % 4]
        if walk:
            put(buf, bass(hz(walkn[beat])), t, level)
        if drums:
            put(buf, brush(), t, level * drums)
            put(buf, ride(), t, level * drums)
            if beat in (1, 3):
                put(buf, slap(), t, level * drums * 0.8)
                put(buf, ride(0.6), t + BEAT * 2 / 3, level * drums)        # the swung "da"
        if comp and beat == 1:
            put(buf, chord(voicing, BEAT * 1.6), t + BEAT * 2 / 3, level * 0.9)
        t += BEAT; k += 1


def music(T):
    st = T["starts"]
    end = st[29]                                                       # DONNIE!
    buf = np.zeros(int(end * SR) + SR)
    # A: the case
    a0, a1 = 0.45, st[17]
    groove(buf, a0, a1, level=0.85)
    phrase(buf, st[5], [("E5", 1), ("D5", 0.5), ("C5", 0.5), ("B4", 2)], 0.9)                # the fake draw
    phrase(buf, st[10], [("A4", 1), ("C5", 1), ("B4", 0.5), ("G#4", 2.5)], 0.8)               # the CCTV
    # B: Pam, vibes only, one chord a bar, out on "Objection."
    t, bar = st[21], 0
    while t < st[26] - 0.3:
        put(buf, chord(CHORDS[bar % 4][1], 2.6, 1.0), t)
        put(buf, bass(hz(CHORDS[bar % 4][0][0]), 1.2), t, 0.6)
        t += BEAT * 4; bar += 1
    # C: the brag; the band builds and the horn climbs
    c0 = st[27]
    groove(buf, c0, end, level=1.0, drums=1.3)
    for i, tk in enumerate(np.arange(c0, end, BEAT)):
        put(buf, kick(), tk, 0.6 + 0.5 * i / max(1, (end - c0) / BEAT))
    phrase(buf, c0 + BEAT * 0.5, [("A4", 0.5), ("C5", 0.5), ("E5", 0.5), ("G5", 0.5), ("A5", 1.5),
                                  ("G#5", 0.5), ("B5", 1), ("C6", 4)], 1.1)
    n = len(buf); t = np.arange(n) / SR
    swell = np.where(t < c0, 1.0, 1.0 + 0.9 * np.clip((t - c0) / (end - c0), 0, 1) ** 1.5)
    buf *= swell
    # the drops: out on his eyes (a 25 ms fade), out on "Objection.", and cut dead on DONNIE!
    for x0, x1 in ((a1, st[21]), (st[26] - 0.3, c0)):
        i0, i1 = int(x0 * SR), int(x1 * SR); f = int(0.025 * SR)
        buf[i0:i0 + f] *= np.linspace(1, 0, f); buf[i0 + f:i1] = 0
    i = int(end * SR); buf[i - int(0.004 * SR):i] *= np.linspace(1, 0, int(0.004 * SR)); buf[i:] = 0
    return buf
