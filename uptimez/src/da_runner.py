"""THE DOUBLE AGENT (episode 15): the Don x robot money lines, v2 (28 Nov).

Tomas: the film had long stretches without a line and Don and the robot never spoke; "they should talk about money";
"they need to speak when they are in the room". v1 (reverted, 3cad530) put lines where the film was silent, with the
robot off screen for three of five: nobody could tell who spoke. v2: only the three shots where BOTH are in the frame,
the wording Tomas picked from three options each:

  1.3  DON: "I pay you!"     ROBOT: "He pays you."      (the robot has just let go of the throne)
  5.4  DON: "I'll sue."      ROBOT: "Yourself."         (he has just slipped; he is the company)
  7.4  ROBOT: "One clip. Four cents."   then Don's "NOT THE CHAIR!" as before

The robot's voice: the series' own (sound_day1.robotize: Don's take pitched up 4 semitones, light metal), dry.
No gag leans on these: each picture reads mute.

  python3 da_runner.py   -> da_voices/takes/r<n>_<who>.wav, each checked by Whisper, and da_runner_takes.json
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
    ("r1b", "ROBOT", "He pays you.", "He pays you.", 0.96, 1.0),
    ("r2a", "DON", "I'll sue.", "I'll sue.", 0.96, 0.9),
    ("r2b", "ROBOT", "Yourself.", "Yourself.", 0.90, 1.0),
    ("r3a", "ROBOT", "One clip. Four cents.", "One clip. Four cents.", 0.90, 1.35),   # louder: the casters run under it
]
# scene -> [(shot, seconds into the shot, take id)]
CUES = {
    "s1": [("1.3", 0.33, "r1a"), ("1.3", 1.25, "r1b")],
    "s5": [("5.4", 0.90, "r2a"), ("5.4", 1.75, "r2b")],
    "s7": [("7.4", 0.10, "r3a")],
}


def _trim(a):
    a = np.asarray(a, dtype=np.float64)
    i = np.where(np.abs(a) > 0.02 * np.abs(a).max())[0]
    b = a[max(0, i[0] - 240):i[-1] + 1200].copy()
    f = 480; b[-f:] *= np.linspace(1, 0, f)
    return b / (np.max(np.abs(b)) + 1e-9)


def make():
    import contextlib
    import io
    import soundfile as sf
    with contextlib.redirect_stdout(io.StringIO()):                    # (sound_day1_v4 prints its own timing on import)
        import sound_bc as bc
        import sound_day1_v4 as d1
        import da_voices as dv
    r = dv.recognizer()
    out = {}
    for lid, who, line, say, sp, gain in LINES:
        best = None
        for k in (sp, sp * 0.94, sp * 1.06, sp * 0.88):                # the first take Whisper hears right is kept
            a = np.asarray(bc.don(say, k), dtype=np.float64)
            if who == "ROBOT":
                a = d1.robotize(a, semis=4, ring=0.18, comb=0.35)
            a = _trim(a)
            heard = [dv._hear(r, w) for w in (dv._to16(a), np.concatenate([np.zeros(4800), dv._to16(a)]))]
            best = best or (heard, a, k)
            if any(_same(h, line) for h in heard):
                best = (heard, a, k); break
        heard, a, k = best
        sf.write(os.path.join(TAKES, "%s_%s.wav" % (lid, who)), a, SR)
        out[lid] = dict(who=who, line=line, speed=round(k, 3), heard=heard, sec=round(len(a) / SR, 2), gain=gain)
        print("%-4s %-5s %-24s %.2f s  heard %s" % (lid, who, line, len(a) / SR, heard))
    json.dump(out, open(os.path.join(TAKES, "da_runner_takes.json"), "w"), indent=1)


def _same(heard, line):
    n = lambda s_: "".join(ch for ch in s_.lower().replace("one", "1").replace("four", "4") if ch.isalnum())
    return n(heard) == n(line)


def _info():
    return json.load(open(os.path.join(TAKES, "da_runner_takes.json")))


def add(m, scene, starts, sr=SR):
    """mix this scene's lines into the float mix m (in place)."""
    import soundfile as sf
    info = _info()
    for shot, at, lid in CUES.get(scene, ()):
        a, _ = sf.read(os.path.join(TAKES, "%s_%s.wav" % (lid, info[lid]["who"])))
        i = int((starts[shot] + at) * sr)
        n = max(0, min(len(a), len(m) - i))
        m[i:i + n] += 0.6 * info[lid]["gain"] * a[:n]


def on(scene, shot, lid, td):
    """is this take sounding at td (seconds into its shot)? for a mouth or a head tilt."""
    info = _info()
    for sh, at, l_ in CUES.get(scene, ()):
        if sh == shot and l_ == lid:
            return at <= td < at + info[lid]["sec"] - 0.12
    return False


if __name__ == "__main__":
    sys.path.insert(0, HERE)
    make()
