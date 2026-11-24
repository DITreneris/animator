"""ONE STAR rough cut v13 (23 Nov): v12's pictures; the opening sound again. Tomas: the buzz still covered the first
word. Now the buzz is short and alone (0.05-0.40 s), then a beat of quiet, and the Client's post starts at 0.58 s
(was 0.30) with nothing under it. Sound only.
  python3 cs_film_v13.py [out_dir]"""
import sys
import cs_film_v12 as v12

LINE12 = 0.58
BUZZ13 = [("1.1", 0.05, 0.35, 0.7)]


def setup():
    v12.setup()
    import cs_scene1 as s1
    import cs_film
    old = s1.schedule
    s1.schedule = lambda: [(k, LINE12 if k == "1.2" else t) for k, t in old()]
    cs_film.BUZZ = BUZZ13 + [b for b in cs_film.BUZZ if b[0] != "1.1"]


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "../customer-success"
    setup()
    import cs_film
    cs_film.main(out, "rough_v13")
