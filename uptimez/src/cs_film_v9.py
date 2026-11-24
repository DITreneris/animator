"""ONE STAR rough cut v9 (23 Nov): v8 plus the cold-test round (4.1 air between Pam's palm and his back, 4.2 held
2.7 s, 5.2 her purple sleeve in frame) and the voices DRY: no room reflections or tail (Tomas: "the sound is like
from a well"; cs_film.WET = 0, the room tone stays). Scenes 1, 2, 3, 6 are v8's files.
  python3 cs_film_v9.py [out_dir] [scene numbers ...]   (no numbers: scenes 4 and 5, then the film)"""
import sys
import importlib
import cs_film_v8 as v8

TAGS = {1: "v12", 2: "v7", 3: "v8", 4: "v7", 5: "v7", 6: "v6"}


def setup():
    v8.setup()
    for i, v in TAGS.items():
        importlib.import_module("cs_scene%d" % i).V = v
    import cs_film
    cs_film.WET = 0.0


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "../customer-success"
    which = [int(a) for a in sys.argv[2:]]
    setup()
    for i in which or (4, 5):
        importlib.import_module("cs_scene%d" % i).main(out)
    if not which:
        import cs_film
        cs_film.main(out, "rough_v9")
