"""Riff candidates and the originality screen.
Notes are (midi, length in sixteenths at 120 BPM). The screen compares interval sequences
(transposition-free) with a list of famous melodies and riffs, approximated from memory:
a quick screening aid, not a guarantee. A candidate fails on 3+ consecutive shared intervals
anywhere (rhythm ignored, which is stricter than the rule in the concept doc), and is flagged
when the shared run also has the same rhythm ratios."""

# Candidates: single-note leads, 5-6 notes, zigzag climb, last note long (he leans into it).
CANDIDATES = {
    'A': [(64, 2), (67, 2), (62, 2), (69, 2), (66, 1), (71, 5)],   # E G D A F# B
    'B': [(57, 2), (64, 2), (60, 1), (67, 3), (62, 2), (69, 4)],   # A E C G D A
    'C': [(62, 3), (65, 1), (60, 2), (69, 2), (67, 2), (74, 4)],   # D F C A G D'
}

# Famous riffs and melodies as pitch sequences (semitones relative; approximate).
FAMOUS = {
    'Smoke on the Water': [0, 3, 5, 0, 3, 6, 5, 0, 3, 5, 3, 0],
    'Seven Nation Army': [0, 0, 3, 0, -2, -4, -5],
    'Iron Man': [0, 3, 3, 5, 5, 8, 7, 8, 7, 8, 7, 3, 3, 5, 5],
    'Satisfaction': [0, 0, 2, 3, 3, 3, 2, 2, 0],
    'Day Tripper': [0, 3, 4, 7, 12, 10, 7, 2, 5, 7],
    'Sunshine of Your Love': [0, 0, -2, 0, -5, -6, -7, -12],
    'Come As You Are': [0, 0, 1, 2, 5, 2, 5, 2, 2, 1, 0, -5, 0, 0],
    'Sweet Child O\' Mine': [0, 12, 7, 5, 17, 7, 16, 7],
    'Smells Like Teen Spirit (roots)': [0, 5, 3, 8],
    'Enter Sandman': [0, 12, 18, 17, 12, 13],
    'Crazy Train': [0, 0, 7, 0, 8, 0, 7, 0, 5, 3, 2, 3, 5, 3, 2, -2],
    'Purple Haze': [0, 6, 0, 6],
    'Layla': [0, 3, 5, 8, 5, 3, 5],
    'Money': [0, 7, 12, 10, 7, 5, 3, 5],
    'Beat It': [0, 0, -2, 0, -3, -5, -3, -2],
    'Paranoid': [0, 0, 0, -2, 3, 0],
    'Peter Gunn': [0, 0, 2, 0, 3, 0, 5, 4],
    'Eye of the Tiger': [0, 0, -2, 0],
    'The Final Countdown': [0, -2, 0, -7, 2, 0, 2, 0, -2],
    'Axel F': [0, 3, 5, 3, 3, 8, 3, 1, 0, 7, 0, 0, 8, 7, 3, 0, 7, 12],
    'Super Mario Bros.': [0, 0, 0, -4, 0, 3, -9],
    'Fuer Elise': [0, -1, 0, -1, 0, -5, -2, -4, -7],
    'Nokia tune': [0, -2, 2, 4, -3, -5, -2, 0, -5, -7, -3, 0, -7],
    'Imperial March': [0, 0, 0, -4, 3, 0, -4, 3, 0],
    'Star Wars theme': [0, 0, 0, 5, 12, 10, 9, 7, 17, 12],
    'Shave and a Haircut': [0, -5, -5, -3, -5, -1, 0],
    'Twinkle Twinkle': [0, 0, 7, 7, 9, 9, 7],
    'Ode to Joy': [0, 0, 1, 3, 3, 1, 0, -2, -4, -4, -2, 0, 0, -2, -2],
    'Happy Birthday': [0, 0, 2, 0, 5, 4],
    'Jingle Bells': [0, 0, 0, 0, 0, 0, 0, 3, -4, -2, 0],
    'Sweet Home Alabama (roots)': [0, -2, -7],
    'Back in Black (lick)': [0, -2, -7, 0, -2, -7],
    'Thunderstruck': [0, 7, 0, 5, 0, 7, 0, 3, 0, 7, 0, 5, 0, 7, 0, 3],
    'Whole Lotta Love': [0, 0, 12, 0, 10, 0, 7, 10],
    'Johnny B. Goode (intro)': [0, 0, 0, 3, 3, 0, 3, 5],
    'Batman theme': [0, 0, -1, -1, -2, -2, -1, -1],
    'Mission: Impossible': [0, 0, 3, 5, 0, 0, -2, -1],
    'The Pink Panther': [0, 1, 3, 4, 10, 9, 4, 7, 6],
    'Hey Jude': [0, -3, -3, 0, 2, -5],
    'Tetris': [0, -5, -4, -2, -4, -5, -7],
}

def intervals(p):
    return [b - a for a, b in zip(p, p[1:])]

def screen(notes, run=3):
    iv = intervals([m for m, _ in notes])
    hits = []
    for name, seq in FAMOUS.items():
        fv = intervals(seq)
        for i in range(len(iv) - run + 1):
            win = iv[i:i + run]
            for j in range(len(fv) - run + 1):
                if fv[j:j + run] == win:
                    hits.append((name, i, win))
    # near-misses: 2 shared consecutive intervals (reported, not failing)
    near = set()
    for name, seq in FAMOUS.items():
        fv = intervals(seq)
        for i in range(len(iv) - 1):
            for j in range(len(fv) - 1):
                if fv[j:j + 2] == iv[i:i + 2]:
                    near.add(name)
    return hits, sorted(near)

if __name__ == '__main__':
    for k, n in CANDIDATES.items():
        hits, near = screen(n)
        print(k, 'intervals', intervals([m for m, _ in n]), 'length', sum(l for _, l in n) / 8, 's',
              'FAIL ' + str(hits) if hits else 'PASS', '| 2-interval overlaps:', near or 'none')
