"""THE DOUBLE AGENT (episode 15): the Don x robot money runner (28 Nov; Tomas /grill-me: the film had 19 s without a
line and Don and the robot never spoke; "Robot and Don should talk about money ... people love money"; HR deadpan).

Four short exchanges over pictures that already read mute (no gag leans on them). The robot is technically true every
time, and the money shrinks: he pays it -> he is worth the chair's price tag -> his compensation is already deducted -> it
moves a $49,999 chair for a four-cent clip.

The robot's voice: the series' own (sound_day1.robotize: Don's take pitched up 4 semitones, light metal), dry.
Takes are written to da_voices/takes/r<n>_<who>.wav; each scene's mix adds its own from CUES below.

  python3 da_runner.py   -> the takes, each checked by ear (Whisper), and da_runner_takes.json
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TAKES = os.path.join(HERE, "da_voices", "takes")
SR = 48000
# (id, who, the line, what the voice is given, speed, gain)
LINES = [
    ("r1a", "DON", "I pay you!", "I pay you!", 1.02, 1.0),
    ("r1b", "ROBOT", "He pays you.", "He pays you.", 0.96, 0.9),
    ("r2a", "DON", "I'm worth millions.", "I'm worth millions.", 0.96, 0.9),
    ("r2b", "ROBOT", "Forty-nine thousand. The chair.", "Forty nine thousand. The chair.", 0.96, 0.9),
    ("r3a", "ROBOT", "Incident logged.", "Incident logged.", 0.96, 0.9),
    ("r3b", "DON", "Compensation?", "Compensation?", 0.96, 0.85),
    ("r3c", "ROBOT", "Already deducted.", "Already deducted.", 0.90, 0.9),   # ("Deducted." alone: Whisper heard "the nothing")
    ("r4a", "ROBOT", "One clip. Four cents.", "One clip. Four cents.", 0.90, 1.35),   # (in the mix under the casters it was heard as "one threat": slower, louder)
]
# scene module -> [(shot, seconds into the shot, take id)]
CUES = {
    "s1": [("1.3", 0.40, "r1a"), ("1.3c", 0.15, "r1b")],
    "s4": [("4.2", 1.30, "r2a"), ("4.2", 2.45, "r2b")],
    "s5": [("5.3", 1.10, "r3a"), ("5.3b", 0.10, "r3b"), ("5.4", 0.80, "r3c")],
    "s7": [("7.4", 0.10, "r4a")],
}


def _trim(a):
    a = np.asarray(a, dtype=np.float64)
    i = np.where(np.abs(a) > 0.02 * np.abs(a).max())[0]
    b = a[max(0, i[0] - 240):i[-1] + 1200].copy()
    f = 480; b[-f:] *= np.linspace(1, 0, f)
    return b / (np.max(np.abs(b)) + 1e-9)


def make():
    import soundfile as sf
    import sound_bc as bc
    import sound_day1_v4 as d1
    import da_voices as dv
    r = dv.recognizer()
    out = {}
    prev = None
    for lid, who, line, say, sp, gain in LINES:
        best = None
        for k in (sp, sp * 0.94, sp * 1.06):                           # three takes; the first Whisper hears right is kept
            a = np.asarray(bc.don(say, k), dtype=np.float64)
            if who == "ROBOT":
                a = d1.robotize(a, semis=4, ring=0.18, comb=0.35)
            a = _trim(a)
            good, heard = dv.score(r, a, line, prev)
            if best is None or good > best[0]:
                best = (good, heard, a, k)
            if good >= 2:
                break
        good, heard, a, k = best
        sf.write(os.path.join(TAKES, "%s_%s.wav" % (lid, who)), a, SR)
        out[lid] = dict(who=who, line=line, speed=round(k, 3), heard=heard, good=int(good), sec=round(len(a) / SR, 2), gain=gain)
        print("%-4s %-5s %-34s %.2f s  heard %d/3  %s" % (lid, who, line, len(a) / SR, good, heard))
        prev = (a, line)
    json.dump(out, open(os.path.join(TAKES, "da_runner_takes.json"), "w"), indent=1)


def add(m, scene, starts, sr=SR):
    """mix this scene's runner lines into the float mix m (in place); returns [(start s, take id, seconds)]."""
    import soundfile as sf
    info = json.load(open(os.path.join(TAKES, "da_runner_takes.json")))
    done = []
    for shot, at, lid in CUES.get(scene, ()):
        a, _ = sf.read(os.path.join(TAKES, "%s_%s.wav" % (lid, info[lid]["who"])))
        i = int((starts[shot] + at) * sr)
        n = max(0, min(len(a), len(m) - i))
        m[i:i + n] += 0.6 * info[lid]["gain"] * a[:n]
        done.append((starts[shot] + at, lid, len(a) / sr))
    return done


def window(scene, shot, lid):
    """(start, end) of a take inside its shot, for a mouth."""
    info = json.load(open(os.path.join(TAKES, "da_runner_takes.json")))
    for sh, at, l_ in CUES.get(scene, ()):
        if sh == shot and l_ == lid:
            return at, at + info[lid]["sec"]
    return None


if __name__ == "__main__":
    sys.path.insert(0, HERE)
    make()
