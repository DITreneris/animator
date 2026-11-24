"""ONE STAR rough cut v11 (23 Nov): v10 with one take trimmed. PAM's "Check your pocket." ended on a long released t
that the speech check heard as "pocketer" once the voices were dry; the take is cut at 1.08 s (cs_voices/film_v9).
Pictures as v9; no scene is re-rendered.
  python3 cs_film_v11.py [out_dir]"""
import sys
import importlib
import cs_film_v9 as v9

TAKES = "cs_voices/film_v9"


def setup():
    v9.setup()
    for i in range(1, 7):
        importlib.import_module("cs_scene%d" % i).TAKES = TAKES


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "../customer-success"
    setup()
    import cs_film
    cs_film.main(out, "rough_v11")
