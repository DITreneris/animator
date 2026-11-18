"""THE BEST CANDIDATE, animation v4 (18 Nov): the joke at 0:01 and a loop that says who is at the door.
Wraps animation v3 (bc_anim.py, unchanged; it still builds v3 bit for bit):
  - the cold open is re-cut. The door (frame 0, the loop's join) is held for 4 drawings (1/3 s) in place of 12, and
    the CLIENT · 47 MISSED CALLS insert comes before "First candidate.", not after it. The phone buzzes from 0.33 s,
    and Don's hand turns it face down without a look at about 1.0 s: the first gag, readable on mute;
  - Don's shot is held 2/3 s longer, for the second buzz he ignores; from the small one on, the film is v3's,
    drawing for drawing (v4: 92.5 s). v4.1 trims silent holds (see HOLD below).
The sound is sound_bc_mix4.py (the v3 mix with one buzz after "First candidate.", ignored, and the car parking under
the last door shot, so the loop says that Father is the next candidate).
  python3 bc_anim4.py timing            -> bc_timing_v4.json
  python3 bc_anim4.py stills OUT t ...  -> OUT/bc_anim_<t>.png
  python3 bc_anim4.py qa [all]          -> the bubble rules of qa_bc.py
  python3 bc_anim4.py render OUT [1080] -> OUT silent video"""
import json
import os
import sys
import bc_sb as B

_names = [s[4].__name__ for s in B.SHOTS]
_i, _j = _names.index("s_first"), _names.index("s_phone47")
assert _j == _i + 1
B.SHOTS[_i], B.SHOTS[_j] = B.SHOTS[_j], B.SHOTS[_i]          # the phone before "First candidate."

import bc_anim as A                                          # noqa: E402  (builds its timing from the new order)

_V3 = {x["name"]: x["t0"] for x in A.T["shots"]}               # v3's shot starts (A.T is still v3's timing here,
                                                              # in the new order: only the first three shots differ)
_V3.update({"s_door": 0.0, "s_first": 1.0, "s_phone47": 2.6667})
A.HOLD["s_door"] = 1 / 3
A.LINES["s_first"] = ("first", 0.2, 0.92)                   # he ignores the second buzz: v3's length, every later
                                                             # shot at v3's time, so every later drawing is v3's
# v4.1, the final trim: about 3 s off silent holds (an action's motion is timed in seconds from its shot's start, so
# only the stillness after it goes). Every line, the two-second pause, the scrub and the door shots are kept.
A.HOLD.update({"s_small_low": 0.75, "s_small_out": 0.67, "s_loom": 0.75, "s_legs": 0.75, "s_chain": 1.0,
               "s_eyes_jealous": 0.58, "s_push_cu": 0.75, "s_eyes_afraid": 0.5, "s_upright": 0.67, "s_mom_sits": 0.67,
               "s_leaves": 0.67, "s_lick": 0.67, "s_stain": 0.58, "s_witnesses": 0.58, "s_lapel": 1.08})
A.T = A.build()
A.SHOT.clear(); A.SHOT.update({s["name"]: s for s in A.T["shots"]})
A.DURATION = A.T["total"]
T, DURATION = A.T, A.DURATION
OFF = {x["name"]: _V3[x["name"]] - x["t0"] for x in T["shots"]}


def _t3():
    """The time v3 had at this point of the shot: breaths and blinks run on it, so a trimmed film breathes and
    blinks where v3 did, shot by shot (the bubble checks were passed on v3's poses)."""
    return A.CUR["t"] + OFF.get(A.CUR["name"], 0.0)


def _blinking(period, phase):
    if A.CUR["name"] in ("s_eyes_jealous", "s_eyes_afraid", "s_tilt", "s_stain", "s_push_cu") or \
            (A.CUR["name"] == "s_pause" and A.CUR["u"] < 0.6):
        return False
    return (_t3() + phase) % period < 2 / 12.0


def _sway(k, x, feet, phase, fn):
    c = k.c
    a = 0.006 * A.math.sin(2 * A.math.pi * _t3() / 3.1 + phase)
    c.save(); c.translate(x, feet); c.scale(1, 1 + a); c.translate(-x, -feet)
    try:
        return fn()
    finally:
        c.restore()


A.blinking, A.sway = _blinking, _sway

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "timing"
    if cmd == "timing":
        json.dump(T, open(os.path.join(A.HERE, "bc_timing_v4.json"), "w"), indent=1)
        for s in T["shots"][:6]:
            print("%s %-16s %6.2f  %.2f" % (s["id"], s["name"], s["t0"], s["d"]))
        print("total %.2f s, %d lines" % (T["total"], len(T["lines"])))
    else:
        A.load_pushes()
        if cmd == "stills":
            for a in sys.argv[3:]:
                A.still(float(a)).write_to_png(os.path.join(sys.argv[2], "bc_anim_%07.2f.png" % float(a)))
        elif cmd == "qa":
            sys.exit(1 if A.qa(1 if "all" in sys.argv else 4) else 0)
        elif cmd == "render":
            A.render(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 540)
