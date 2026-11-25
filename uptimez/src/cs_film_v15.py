"""ONE STAR rough cut v15 (25 Nov): v14c plus the speech bubbles (cs_say: ten lines in frame, the repo's bubble, one
locked bubble per line and picture; the four lines on screens get none) and the reframings they need (1.4, 2.1's pan,
4.2b, 4.4). Every scene is re-rendered (5.1 and 5.4c carry lines too).
  python3 cs_film_v15.py [out_dir] [scene numbers ...]   (no numbers: all six, then the film)"""
import sys
import importlib
import cs_film_v14 as f14


def setup():
    f14.setup()
    import cs_v15b
    cs_v15b.install()
    import cs_say
    cs_say.install()
    for i in range(1, 7):
        importlib.import_module("cs_scene%d" % i).V = "v15"


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "../customer-success"
    which = [int(a) for a in sys.argv[2:]]
    setup()
    for i in which or range(1, 7):
        importlib.import_module("cs_scene%d" % i).main(out)
    if not which:
        import cs_film
        cs_film.main(out, "rough_v15")
    import cs_say
    print("bubbles placed:", len(cs_say.PLACED), "faults:", cs_say.FAULTS)
