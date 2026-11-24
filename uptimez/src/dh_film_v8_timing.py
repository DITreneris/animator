"""Daddy's Home v8: every spoken line's place in the joined film (daddys_home_anim_v8.mp4), for qa_ob_speech.py.
  python3 dh_film_v8_timing.py  ->  /tmp/dh_film_v8_timing.json"""
import json, os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE); sys.path.insert(0, HERE)
import dh_voices as dv
import dh_film_v8 as fv

TEXT = {k: t for k, _, t, *_ in dv.FILM}
TEXT["3.5"] = "Green is all he sees."                          # the take since v6 (dv.FILM still has the first draft)
SR = dv.SR


def takes(n):
    """(key, at, seconds) for scene n, as its own script places them."""
    if n in (1, 2, 3):
        m = __import__({1: "dh_anim1", 2: "dh_anim2", 3: "dh_anim3_v8"}[n])
        V7 = m.V7 if n == 3 else m
        return [(key, at, len(V7.WAV[key]) / float(V7.SR)) for key, at in V7.TAKES]
    sc = __import__("dh_anim%d" % n).sc
    return [(key, at, len(sc.WAV[key]) / float(SR)) for key, at in sc.takes]


def main():
    off, shots = 0.0, []
    for n in range(1, 9):
        for key, at, d in takes(n):
            base = key.split("a")[0].split("b")[0] if key not in TEXT else key
            text = TEXT.get(key) or TEXT.get(base)
            if text:
                shots.append({"shot": "%d:%s" % (n, key), "line": {"t0": off + at, "t1": off + at + d, "text": text, "who": "", "key": "%d:%s" % (n, key)}})
        off += fv.dur("%s/dh_s%d_anim_%s.mp4" % (fv.OUT, n, fv.VERS[n]))
    shots.sort(key=lambda s: s["line"]["t0"])
    json.dump({"shots": shots}, open("/tmp/dh_film_v8_timing.json", "w"), indent=1)
    print(len(shots), "lines")


if __name__ == "__main__":
    main()
