"""PICK A SIDE: the audit's drawing faults (P1-P15, story audit v1 §3) fixed across the locked scenes, opt-in: every
switch is set only by setup() here, so the locked versions still build byte-identical from ps_film alone.

  python3 ps_film_fix.py film 1 6    (and 2 5, 4 12; scenes 5 and 6 through ps_film_end: setup() calls both)

P1  1.4   his face "hollow" (grey eyes = sunglasses) -> FACE_14
P2  roll  the hand a disc inside the roll -> don_ps.ROLL_GRIP: the ring hangs under the fist, the fist redrawn on its rim
P3  2.3   the roll over his face as it points -> BEATS_23 lower (the arm at shoulder height)
P4  2.8   the tape a short piece ending mid-frame -> sofia_ps.TAPE_LONG: edge to edge
P15 6.1b  the shock's hands piled on his chest -> the arms flung out (pose "balance")"""
import sys
import ps_film as pf
import ps_scenes as ps
import don_ps as dp

FIX = dict(face14="neutral", roll_grip=24, shock61b="balance", beats23=((0.35, 0.75, 96), (0.75, 1.15, 106), (1.15, 1.55, 116)))


def setup():
    ps.FACE_14[0] = FIX["face14"]
    dp.ROLL_GRIP[0] = FIX["roll_grip"]
    pf.BEATS_23[0] = FIX["beats23"]
    ps.sp.TAPE_LONG[0] = True
    pf.SHOT_FN["1.4"] = s14
    import ps_film_end as fe
    fe.setup()                                               # scenes 5 and 6: the new ending
    fe.SHOCK_POSE_61B[0] = FIX["shock61b"]


_s14 = pf.s14


def s14(t):
    """1.4 with the grip: the roll at his side rests ON his fist (the ring above it, out of the bottom quarter); as it
    comes up it swings under the fist"""
    u = pf.ease((t - pf.LIFT_14[0]) / (pf.LIFT_14[1] - pf.LIFT_14[0]))
    sh = _s14(t)
    inner = sh["cast"]
    def cast(k):
        was = dp.ROLL_GRIP[0]
        dp.ROLL_GRIP[0] = -22 + (FIX["roll_grip"] + 22) * u
        try:
            return inner(k)
        finally:
            dp.ROLL_GRIP[0] = was
    return dict(sh, cast=cast)


if __name__ == "__main__":
    setup()
    if len(sys.argv) > 2 and sys.argv[1] == "film":
        sys.exit(0 if pf.film(int(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else 1) else 1)
    print(__doc__)
