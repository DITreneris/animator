"""ONE STAR rough cut v8 (23 Nov): v7 plus shot list v19 (cs_v19: five close-ups, two over-the-shoulder shots, the
foreground layer with parallax, the 7 insert 4.3s, Pam's STOP palm with in-betweens, the Client sheepish in 4.3a).
  python3 cs_film_v8.py [out_dir] [scene numbers ...]   (no numbers: all six, then the film)"""
import sys
import importlib
import cs_film_v7 as v7
import cs_v19

TAGS = {1: "v12", 2: "v7", 3: "v8", 4: "v6", 5: "v6", 6: "v6"}


def setup():
    v7.setup()
    cs_v19.install()
    for i, v in TAGS.items():
        importlib.import_module("cs_scene%d" % i).V = v


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "../customer-success"
    which = [int(a) for a in sys.argv[2:]]
    setup()
    for i in which:
        importlib.import_module("cs_scene%d" % i).main(out)
    if not which:
        for i in range(1, 7):
            importlib.import_module("cs_scene%d" % i).main(out)
        import cs_film
        cs_film.main(out, "rough_v8")
