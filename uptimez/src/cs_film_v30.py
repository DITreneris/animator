"""ONE STAR rough cut v30 (28 Nov, Tomas's /grill-me after four tries on one arm: change the gesture): 6.5, Sofía holds
the phone in BOTH hands at her chest, its screen to us: her screen-left hand under it (the v4c grip), her screen-right
hand on its right edge (of_cast.clutch), both arms bent from her shoulders, as the robot's phone at 6.6a reads (2 of 2
cold viewers traced his arms). v29: one hand by her shoulder, its arm hidden by her hair, "a hand without an arm".
Was: ONE STAR rough cut v29 (26 Nov, Tomas's /grill-me after v28's cold test): 6.6a's phone clamped in both hands at one size
from his first drawing (v28: it grew 2.3 times in his hand when the second hand came, "the phone suddenly gets much
bigger", two cold viewers of two). Was: ONE STAR rough cut v28 (26 Nov, Tomas: "the phones are not fixed, every frame carefully"): v27 with EVERY held phone
in the canon's v4c grip (hands_v4.ALL_V4C: tilted, its back to us, at the ear, the close-ups), and the phone gate
(phone_gate: a held phone drawn without the v4c grip fails the film). Nothing else changes.
  python3 cs_film_v28.py [out_dir] [hi] [scene numbers ...]"""
import sys
import math
import importlib
import cs_film_v26 as f26
import cs_film_v27 as f27
import cs_film_v28 as f28
import cs_film_v29 as f29
import hands_v4
import phone_gate


L65 = (-16, 100)          # her screen-left palm, under the phone (rig units from her feet, y from BODY_TOP)
R65 = (12, 88)            # her screen-right hand, on the phone's right edge


def setup():
    f29.setup()
    for i in range(1, 7):
        importlib.import_module("cs_scene%d" % i).V = "v30"
    import cs_scene6 as s6
    import sofia_ob as so
    import of_cast as oc
    import cs_os23 as o23
    o23.SHOWX65[0], o23.SHOWY65[0] = L65                   # cs_os23 bends her screen-left arm to this

    def s6_5(k, d, _f=dict((n, f) for n, _, f in s6.SHOTS)["6.5"]):
        rest, grip = so.REST, oc.phone_grip
        so.REST = so._ik(1, R65[0], so.BODY_TOP + R65[1])  # cs_os23's "show" = left arm + REST: the right arm bent too

        def two(k_, x, y, s_, screen=None, **kw):
            if screen is not o23._screen65:
                return grip(k_, x, y, s_, screen=screen, **kw)
            (lx, ly), (rx, ry) = sorted(o23.HANDS65)
            sp = max(0.3, (rx - lx) / 22.0)                 # the phone spans from her palm to her other hand
            out = grip(k_, lx, ly, sp, screen=screen, ang=0.0, skin=kw.get("skin"), body_x=rx, back=False)
            c = k_.c
            c.save(); c.translate(lx + 23 * sp, ly - 12 * sp); c.rotate(math.pi / 2)      # her other hand on its edge, below the words
            oc.clutch(k_, 0, 0, 17 * sp, kw.get("skin"))
            c.restore()
            return out
        oc.phone_grip = two
        try:
            return _f(k, d)
        finally:
            so.REST, oc.phone_grip = rest, grip
    s6.SHOTS[:] = [(n, nd, s6_5 if n == "6.5" else f) for n, nd, f in s6.SHOTS]


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
        cs_film.main(out, "rough_v30" if hi == 2 else "rough_v30_hi%d" % hi)
    import cs_say
    print("bubbles placed:", len(cs_say.PLACED), "faults:", cs_say.FAULTS)
    print("hand gate:", len(cs_grips.FAULTS), "faults", cs_grips.FAULTS[:6])
    ins, bands, warn, hand = f26.sweep()
    print("insert gate:", len(ins), ins[:4])
    print("flat-band gate:", len(bands), bands[:4], "| 30-40 %, look at:", warn)
    ok_ph = phone_gate.report()
    if cs_grips.FAULTS or cs_say.FAULTS or ins or bands or hand or not ok_ph:
        raise SystemExit("a gate FAILED")
