"""ONE STAR rough cut v29 (26 Nov, Tomas's /grill-me after v28's cold test): 6.6a's phone clamped in both hands at one size
from his first drawing (v28: it grew 2.3 times in his hand when the second hand came, "the phone suddenly gets much
bigger", two cold viewers of two). Was: ONE STAR rough cut v28 (26 Nov, Tomas: "the phones are not fixed, every frame carefully"): v27 with EVERY held phone
in the canon's v4c grip (hands_v4.ALL_V4C: tilted, its back to us, at the ear, the close-ups), and the phone gate
(phone_gate: a held phone drawn without the v4c grip fails the film). Nothing else changes.
  python3 cs_film_v28.py [out_dir] [hi] [scene numbers ...]"""
import sys
import importlib
import cs_film_v26 as f26
import cs_film_v27 as f27
import cs_film_v28 as f28
import hands_v4
import phone_gate


def setup():
    f28.setup()
    for i in range(1, 7):
        importlib.import_module("cs_scene%d" % i).V = "v29"
    import cs_v14c as cv
    import cs_scene6 as s6

    def s6_6a(k, d):
        """v14c's 6.6a with the phone clamped in both hands from his first drawing (v28: one small phone in one hand,
        then a 2.3 times bigger one in two): one phone, one size, the buzz on it as before."""
        real = cv.ease
        cv.ease = lambda u: 1.0
        try:
            return cv.s6_6a(k, d)
        finally:
            cv.ease = real
    s6.SHOTS[:] = [(n, nd, s6_6a if n == "6.6a" else f) for n, nd, f in s6.SHOTS]


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "../customer-success"
    hi = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    which = [int(a) for a in sys.argv[3:]]
    import subprocess
    if b"PASS" not in subprocess.check_output([sys.executable, "phone_gate.py"]):   # its own process: it enables hands_v4
        raise SystemExit("the phone gate's self-test failed")
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
        cs_film.main(out, "rough_v29" if hi == 2 else "rough_v29_hi%d" % hi)
    import cs_say
    print("bubbles placed:", len(cs_say.PLACED), "faults:", cs_say.FAULTS)
    print("hand gate:", len(cs_grips.FAULTS), "faults", cs_grips.FAULTS[:6])
    ins, bands, warn, hand = f26.sweep()
    print("insert gate:", len(ins), ins[:4])
    print("flat-band gate:", len(bands), bands[:4], "| 30-40 %, look at:", warn)
    ok_ph = phone_gate.report()
    if cs_grips.FAULTS or cs_say.FAULTS or ins or bands or hand or not ok_ph:
        raise SystemExit("a gate FAILED")
