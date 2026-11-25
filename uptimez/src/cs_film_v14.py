"""ONE STAR rough cut v14 (25 Nov): v13 plus the physical beats (cs_v14): the opening gag, the antenna, the sheet
faster than his hand and the roll at the door, the ball and PLOK. And the hands round (cs_v14_hands: 2.1, 4.1, 6.3). Scenes 1, 2, 3, 4, 6 re-rendered; 5 as v13.
  python3 cs_film_v14.py [out_dir] [scene numbers ...]   (no numbers: scenes 1, 2, 3, 4, 6, then the film)"""
import sys
import importlib
import cs_film_v13 as f13


def setup():
    f13.setup()
    import cs_v14
    cs_v14.install()
    import cs_v14_hands
    cs_v14_hands.install()
    import cs_v14c
    cs_v14c.install()


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "../customer-success"
    which = [int(a) for a in sys.argv[2:]]
    setup()
    for i in which or (1, 2, 3, 4, 6):
        importlib.import_module("cs_scene%d" % i).main(out)
    if not which:
        import cs_film
        cs_film.main(out, "rough_v14")
