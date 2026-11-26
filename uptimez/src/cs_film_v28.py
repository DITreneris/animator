"""ONE STAR rough cut v28 (26 Nov, Tomas: "the phones are not fixed, every frame carefully"): v27 with EVERY held phone
in the canon's v4c grip (hands_v4.ALL_V4C: tilted, its back to us, at the ear, the close-ups), and the phone gate
(phone_gate: a held phone drawn without the v4c grip fails the film). Nothing else changes.
  python3 cs_film_v28.py [out_dir] [hi] [scene numbers ...]"""
import sys
import importlib
import cs_film_v26 as f26
import cs_film_v27 as f27
import hands_v4
import phone_gate


def setup():
    f27.setup()
    for i in range(1, 7):
        importlib.import_module("cs_scene%d" % i).V = "v28"
    hands_v4.ALL_V4C[0] = True
    phone_gate.NOT_HELD.update({"_phone_in_claw"})          # the robot's claw holds the falling phone: not a hand
    phone_gate.install()


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
        cs_film.main(out, "rough_v28" if hi == 2 else "rough_v28_hi%d" % hi)
    import cs_say
    print("bubbles placed:", len(cs_say.PLACED), "faults:", cs_say.FAULTS)
    print("hand gate:", len(cs_grips.FAULTS), "faults", cs_grips.FAULTS[:6])
    ins, bands, warn, hand = f26.sweep()
    print("insert gate:", len(ins), ins[:4])
    print("flat-band gate:", len(bands), bands[:4], "| 30-40 %, look at:", warn)
    ok_ph = phone_gate.report()
    if cs_grips.FAULTS or cs_say.FAULTS or ins or bands or hand or not ok_ph:
        raise SystemExit("a gate FAILED")
