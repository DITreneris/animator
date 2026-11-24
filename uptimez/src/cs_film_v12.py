"""ONE STAR rough cut v12 (23 Nov): v11 plus the QA round. The opening buzz drops under the Client's first word
("Paid" was not heard in the mix since v6); 3.1's foreground is the desk corner of 1.4 (the sheet curl read as the lost
blueprint); 5.1's phone light is weak (over his sleeve it read as a glitch). Scenes 3 and 5 are re-rendered.
  python3 cs_film_v12.py [out_dir] [scene numbers ...]   (no numbers: scenes 3 and 5, then the film)"""
import sys
import importlib
import cs_film_v11 as v11

TAGS = {3: "v9", 5: "v8"}


def setup():
    v11.setup()
    import cs_v19
    import cs_scene1 as s1
    import cs_film
    cs_v19.FG19["3.1"] = [("desk", "left")]
    s1.GLOW_A["5.1"] = 0.10
    cs_film.BUZZ = cs_film.BUZZ_V12 + cs_film.BUZZ[1:]
    cs_film.FX = [(sh, d, x, g * 0.6 if (sh, d) == ("3.2a", 2) else g) for sh, d, x, g in cs_film.FX]   # the page tear was the film's peak (0 dBFS)
    for i, v in TAGS.items():
        importlib.import_module("cs_scene%d" % i).V = v


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "../customer-success"
    which = [int(a) for a in sys.argv[2:]]
    setup()
    for i in which or (3, 5):
        importlib.import_module("cs_scene%d" % i).main(out)
    if not which:
        import cs_film
        cs_film.main(out, "rough_v12")
