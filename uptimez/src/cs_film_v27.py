"""ONE STAR rough cut v27 (26 Nov, series hands/phones audit, Tomas: "taisom One Star"): v26 with the hand class
sheet v4 (hands_v4.enable(): grab, pinch, fist v2; phone_grip v4b). Nothing else changes.
  python3 cs_film_v27.py [out_dir] [hi] [scene numbers ...]"""
import sys
import importlib
import cs_film_v26 as f26
import hands_v4


def setup():
    f26.setup()
    for i in range(1, 7):
        importlib.import_module("cs_scene%d" % i).V = "v27"
    hands_v4.enable()


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
        cs_film.main(out, "rough_v27" if hi == 2 else "rough_v27_hi%d" % hi)
    import cs_say
    print("bubbles placed:", len(cs_say.PLACED), "faults:", cs_say.FAULTS)
    print("hand gate:", len(cs_grips.FAULTS), "faults", cs_grips.FAULTS[:6])
    ins, bands, warn, hand = f26.sweep()
    print("insert gate:", len(ins), ins[:4])
    print("flat-band gate:", len(bands), bands[:4], "| 30-40 %, look at:", warn)
    if cs_grips.FAULTS or cs_say.FAULTS or ins or bands or hand:
        raise SystemExit("a gate FAILED")
