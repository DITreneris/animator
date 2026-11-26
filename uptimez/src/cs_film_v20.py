"""ONE STAR rough cut v20 (26 Nov): v19 plus cs_os20 (the frame-by-frame hand audit and the review's picks).
  python3 cs_film_v20.py [out_dir] [hi] [scene numbers ...]
Gates, before the render: the hand and elbow self-tests; after it, on every second drawing at 540: the hand gate, the
new insert gate (sleeve without its owner inside the frame > 200 units: rules 224/225) and the flat-band gate (a run of
one-colour rows >= 40 % of the height: v17's empty 5.2; 30-40 % listed for a look)."""
import sys
import importlib
import cs_film_v19 as f19

TAKES = f19.TAKES


def setup():
    f19.setup()
    import cs_os20
    cs_os20.install()
    for i in range(1, 7):
        importlib.import_module("cs_scene%d" % i).V = "v20"


def sweep():
    import cs_os20 as g
    import cs_scene1 as s1
    import cs_grips
    hi = s1.HI[0]; s1.HI[0] = 1
    bands, warn = [], []
    del g.INSERT_LOG[:]
    try:
        for i in range(1, 7):
            for sh, nd, fn in importlib.import_module("cs_scene%d" % i).SHOTS:
                for d in range(0, nd, 2):
                    g.CUR[:] = [sh, d]
                    fb = g.flat_bands(s1.draw(fn, d))
                    (bands if fb >= 0.40 else warn if fb >= 0.30 else []).append((sh, d, round(fb, 2)))
    finally:
        s1.HI[0] = hi
    return g.insert_faults(), bands, sorted(set(x[0] for x in warn)), list(cs_grips.FAULTS)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "../customer-success"
    hi = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    which = [int(a) for a in sys.argv[3:]]
    setup()
    import cs_scene1 as s1
    s1.HI[0] = hi
    import cs_grips
    if not (cs_grips.selftest() and cs_grips.selftest_arms()):
        raise SystemExit("the hand and elbow gates' self-tests failed")
    for i in which or range(1, 7):
        importlib.import_module("cs_scene%d" % i).main(out)
    if not which:
        import cs_film
        cs_film.main(out, "rough_v20" if hi == 2 else "rough_v20_hi%d" % hi)
    import cs_say
    print("bubbles placed:", len(cs_say.PLACED), "faults:", cs_say.FAULTS)
    print("hand gate:", len(cs_grips.FAULTS), "faults", cs_grips.FAULTS[:6])
    ins, bands, warn, hand = sweep()
    print("insert gate:", len(ins), ins[:4])
    print("flat-band gate:", len(bands), bands[:4], "| 30-40 %, look at:", warn)
    if cs_grips.FAULTS or cs_say.FAULTS or ins or bands or hand:
        raise SystemExit("a gate FAILED")
