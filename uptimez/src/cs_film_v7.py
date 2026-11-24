"""ONE STAR rough cut v7 (23 Nov): everything Tomas approved today, opt-in flags on, the earlier scene files kept.
  phones: every line inside the screen (cs_props.FIT2, on in cs_scene1.draw) · scene 4 v5: layout B, Pam's line
  "Check your pocket." · scene 6 v5: Pam says "Some post. Others find." · hands: the series' one hand (hands_ps
  "quiet"), phones and the 7 held (cs_scene1.GRIP), Pam's point and STOP palm, the robot's own grippers (cs_hands).
  python3 cs_film_v7.py [out_dir] [scene numbers ...]   (no numbers: all six, then the film)"""
import sys
import importlib
import cs_scene1 as s1
import cs_hands as ch

TAGS = {1: "v11", 2: "v6", 3: "v7", 4: "v5", 5: "v5", 6: "v5"}


def setup():
    s1.GRIP[0] = True
    ch.install()
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
        cs_film.main(out, "rough_v7")
