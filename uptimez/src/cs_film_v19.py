"""ONE STAR rough cut v19 (26 Nov): v18 plus cs_os19 (1.2 the reactions count going viral).

  python3 cs_film_v19.py [out_dir] [hi] [scene numbers ...]"""
import sys
import importlib
import cs_film_v18 as f18

TAKES = f18.TAKES


def setup():
    f18.setup()
    import cs_os19
    cs_os19.install()
    for i in range(1, 7):
        importlib.import_module("cs_scene%d" % i).V = "v19"


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
        cs_film.main(out, "rough_v19" if hi == 2 else "rough_v19_hi%d" % hi)
    import cs_say
    print("bubbles placed:", len(cs_say.PLACED), "faults:", cs_say.FAULTS)
    print("hand gate:", len(cs_grips.FAULTS), "faults", cs_grips.FAULTS[:6])
    if cs_grips.FAULTS or cs_say.FAULTS:
        raise SystemExit("hand or bubble gate FAILED")
