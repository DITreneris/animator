"""The Onboarding: office music, second try (17 Nov). The ceiling-speaker bossa of The Best Candidate was "a bit
annoying" under this film: too loud, never changing, and a shaker hissing on every eighth for a minute. Three
candidates in the direction the director chose, sparse vibes: no percussion at all, an eight-bar progression instead
of four, slower (24 bars over the film, about 78 bpm; whole eight-bar phrases, so the loop has no musical join).
  A  chords only: one soft rolled chord a bar and a quiet bass note; a second, softer touch every fourth bar
  B  barely there: a chord every other bar, no bass, 4 dB lower again
  C  chords and an answer: A, with a short vibes phrase in every second bar, a different one each time
bed(total, bars, kind) -> (left, right, bar length); GAIN[kind] is its level in the mix (the bossa's was 0.105)."""
import numpy as np
import sound_iwry as si

SR = si.SR
GAIN = {"A": 0.060, "B": 0.052, "C": 0.056}
PROG = [  # bass, the chord (MIDI): Cmaj9, Am7, Dm9, G13, Em7, A7, Dm7, G7sus
    (48, (64, 67, 71, 74)), (45, (60, 64, 67, 72)), (50, (60, 64, 65, 69)), (43, (59, 64, 65, 69)),
    (52, (62, 67, 71, 74)), (45, (61, 64, 67, 69)), (50, (60, 65, 69, 72)), (43, (60, 62, 65, 69)),
]
PHRASES = [  # (MIDI, beat it starts on, beats it rings); one of these in every second bar
    ((76, 2.0, 1.0), (74, 2.5, 1.0), (71, 3.0, 2.0)),
    ((72, 2.0, 1.5), (69, 3.0, 2.0)),
    ((74, 1.5, 0.8), (76, 2.0, 1.0), (79, 3.0, 2.0)),
    ((74, 2.0, 0.8), (72, 2.5, 0.8), (71, 3.0, 0.8), (67, 3.5, 2.0)),
    ((79, 2.5, 1.0), (76, 3.0, 2.0)),
    ((69, 2.0, 1.0), (72, 2.5, 1.0), (76, 3.0, 2.0)),
]


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12.0)


def vibe(m, d, soft=1.0):
    """A vibraphone bar struck with a soft mallet: the note, a bell partial that goes at once, a slow motor."""
    t = np.arange(int(d * SR)) / float(SR)
    f = hz(m)
    a = np.sin(2 * np.pi * f * t) + 0.20 * soft * np.sin(2 * np.pi * f * 4 * t) * np.exp(-t / 0.10)
    return a * np.minimum(1, t / 0.006) * np.exp(-t / 1.15) * (1 + 0.16 * np.sin(2 * np.pi * 4.6 * t))


def bed(total, bars, kind="A"):
    bar = total / float(bars); beat = bar / 4.0
    L = int(round(total * SR))
    l, r = np.zeros(L), np.zeros(L)
    for b in range(bars):
        root, notes = PROG[b % 8]
        t0 = b * bar
        if kind == "B" and b % 2:
            continue
        for i, m in enumerate(notes):                         # rolled upward, the low note first
            a = vibe(m, bar * 1.6) * (0.9 - 0.08 * i)
            pan = 0.36 + 0.09 * i
            si.add(l, a * (1 - pan), t0 + i * 0.04); si.add(r, a * pan, t0 + i * 0.04)
        if kind != "B":
            t = np.arange(int(bar * 0.9 * SR)) / float(SR)     # the bass: one round note, gone before the next bar
            a = np.sin(2 * np.pi * hz(root) * t) * np.exp(-2.4 * t) * np.minimum(1, t / 0.012) * 0.8
            si.add(l, a * 0.5, t0); si.add(r, a * 0.5, t0)
            if b % 4 == 3:                                     # every fourth bar, the top of the chord again, softer
                for i, m in enumerate(notes[2:]):
                    a = vibe(m, bar * 0.9, 0.5) * 0.45
                    si.add(l, a * 0.45, t0 + 2 * beat + i * 0.05); si.add(r, a * 0.55, t0 + 2 * beat + i * 0.05)
        if kind == "C" and b % 2 == 1:
            for m, at, ln in PHRASES[(b // 2) % len(PHRASES)]:
                a = vibe(m, ln * beat * 1.4, 0.7) * 0.62
                si.add(l, a * 0.40, t0 + at * beat); si.add(r, a * 0.60, t0 + at * beat)
    for x in (l, r):                                          # still the office's ceiling speaker, a little rounder
        x -= si.lp(x, int(SR / 200))
        x[:] = si.lp(x, 9)
    return l, r, bar
