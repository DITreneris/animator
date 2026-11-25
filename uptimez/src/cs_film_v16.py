"""ONE STAR rough cut v16 (25 Nov, Tomas /grill-me "what is left to polish before the render"): v15 plus
- the voices from film_v10: Sofia's "Still one star." 3 dB up (in the mix it was lost behind Pam's line: Whisper 1/3 -> 3/3;
  six new reads, with pauses, were heard worse);
- 3.1 his point and his fist stop clear of the robot's visor (cs_grips.install_free);
- 5.2 Pam's purple sleeve from the top edge to the pen hand, the pen shorter (cs_grips.s5_2_pen);
- open palms with fingers of unequal length (hands_ps.PALM_VAR, One Star only);
- the cover v2 (cs_cover.py v2).
  python3 cs_film_v16.py [out_dir] [hi] [scene numbers ...]   (hi 2: 1080 master; hi 1: the 540 film for the PSNR check)"""
import sys
import importlib
import cs_film_v15 as f15

TAKES = "cs_voices/film_v10"


def setup():
    f15.setup()
    for i in range(1, 7):
        m = importlib.import_module("cs_scene%d" % i)
        m.V = "v16"
        m.TAKES = TAKES


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
        cs_film.main(out, "rough_v16" if hi == 2 else "rough_v16_hi%d" % hi)
    import cs_say
    print("bubbles placed:", len(cs_say.PLACED), "faults:", cs_say.FAULTS)
    print("hand gate:", len(cs_grips.FAULTS), "faults", cs_grips.FAULTS[:6])
    if cs_grips.FAULTS or cs_say.FAULTS:
        raise SystemExit("hand or bubble gate FAILED")
