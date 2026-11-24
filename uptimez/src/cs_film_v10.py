"""ONE STAR rough cut v10 (23 Nov): v9's pictures, one voice changed. 0:10 "Stupid human." is Don's, in his clean
voice (Tomas: the robot's effect on it read as "Don in a pipe"; he has just approved the reply, so he reads it out
proudly). The takes are cs_voices/film_v8 (film_v7 with 1.4b re-recorded). No scene is re-rendered.
  python3 cs_film_v10.py [out_dir]"""
import sys
import importlib
import cs_film_v9 as v9

TAKES = "cs_voices/film_v8"


def setup():
    v9.setup()
    for i in range(1, 7):
        importlib.import_module("cs_scene%d" % i).TAKES = TAKES


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "../customer-success"
    setup()
    import cs_film
    cs_film.main(out, "rough_v10")
