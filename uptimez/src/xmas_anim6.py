"""ANIMATION v6 of "Happy Compliance" (18 Nov), the release: v5 (xmas_anim5.py, kept) with the last two notes of the
second pair of cold viewers (who read all five beats):
- no razor on the floor at the THUD: with Don's legs in shot it only read as "a blue limb" or "a robot leg";
- the thrown bauble spins, but its CENSORED bar stays upright and readable (it tumbled upside down).
Sound: v5's (xmas_mix_v5.wav). Module protocol for engine_v / engine_hd: PANELS, DURATION, RAW_T, shake."""
import xmas_anim5 as M5
import xmas_anim2 as A2
import sofia_xmas as sx
import santa_robot as sr

DURATION = M5.DURATION
RAW_T = 0.0
_razor5 = A2.razor_floor


def razor_floor(k, hand, s=1.0, ang=-0.9, seed=540):
    t = A2.xa.ACT.get("t", 0.0)
    if A2.SHOT11[0] <= t < A2.SHOT11[1]:
        return None                                  # not in the last shot
    return _razor5(k, hand, s, ang, seed)


A2.razor_floor = razor_floor


def bauble(k, x, y, r, rot, barred=True, seed=0):
    c = k.c
    c.save(); c.translate(x, y); c.rotate(rot)
    sx.ornament(k, 0, 0, r, seed, col=sx.ORN_RED)
    c.restore()
    if barred:                                       # the bar stays upright as the bauble spins under it
        sr.censor_bar(k, x, y, r * 3.0, r * 0.95, rot=0.08, seed=seed + 5, label=True)


M5.bauble = bauble
PANELS = M5.PANELS


def shake(t):
    return M5.shake(t)
