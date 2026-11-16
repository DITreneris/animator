"""v4 (xmas_pam3_v3.py = v3 kept): shot 10 reordered after the review: she says "Human in the loop." with the
mask still UP on her head (deadpan authority), then pulls it DOWN over her readers in a visible 0.35 s move
(T_PULL 3.30, T_SNAP 3.65 in shot 10's own time, film 24.30-24.65), the hero stance after it, a 0.5 s silent hold
and a gentle push-in on her; the mask is never at her neck any more (it was, in shot 10's own code).
v3 notes: Routes the Christmas film's Pam to the v3 canon figure (pam_xmas3), for the v3 sheet and the film v2.
Inside xmas_anim's panels, px.pam is hooked (xmas_anim._pam -> _pam0); this swaps _pam0 for pam_xmas3 and swaps
the talking-mouth hook for one with her dusty-rose lips (the Secret Santa mouths at 0.8, as in pam_ss).
Per film time: the mask's neck spot becomes "up" (pushed up on her head); "glance" in the still beat of shot 5
(9.50-9.80 s, the smallest smile at Don before the horror); "over" while she says "Human in the loop.".
apply() / restore() switch it on and off."""
import kit
import xmas_anim as xa
import pam_xmas as px
import pam_xmas3 as p3
import pam_ss as ps
import iwry_mouths as mo
import math
import xmas_test_b as tb
from kit import ease, clamp
import pam_mf as pm

GLANCE = (9.50, 9.80)
OVER = (23.0, 24.25)                                    # v4: the line only (23.07-24.20)
SHOT10 = (21.5, 25.5)
T_PULL, T_SNAP = 3.30, 3.65                             # v4: after the line (shot 10 time = film time - 21.0)
_saved = {}


def face_at(t, face):
    if GLANCE[0] <= t < GLANCE[1] and face == "neutral":
        return "glance"
    if OVER[0] <= t < OVER[1] and face in ("neutral", "squint"):
        return "over"
    return face


def _pam3(k, x, feet, s=1.0, pose="stand", face="neutral", look=(0, 0), mask="neck", **kw):
    t = xa.ACT.get("t", 0.0)
    f = face_at(t, face)
    if f == "glance":
        look = (1.0, 0.1)                               # Don is screen right
    return p3.pam(k, x, feet, s, pose, f, look, mask="up" if mask == "neck" else mask, **kw)


def _pam_hook(orig, mask, chin=0.0):
    def with_mouth(k, x, y, face, look, glasses=False, seed=0):
        orig(k, x, y, face, look, glasses=glasses, seed=seed)
        if seed == px.FACE_SEED[0]:
            code = xa.vis("PAM", xa.ACT["t"])
            if code:
                c = k.c
                my = y - 7 * xa.ACT.get("pam_chin", 0) + 28
                pm._mouth_erase(k, x, my - 28, seed)                                          # clear the resting lips
                c.save(); c.translate(x, my); c.scale(0.8, 0.8)
                mo.mouth(k, 0, 0, code, ps.SKIN, lip_col=ps.ROSE, erase=(1, 1), seed=seed + 96)
                c.restore()
    return xa._pam_hook0(with_mouth, mask, chin)


def _mask(k, x, y, mode, seed=0):
    """Shot 10 draws the mask itself (outside her figure): neck -> up on her head; the pull -> a visible drop
    from the head spot down over the glasses."""
    t = xa.ACT.get("t", 0.0)
    if not (SHOT10[0] <= t < SHOT10[1]):
        return _saved["mask"](k, x, y, mode, seed)
    tt = t - 21.0
    if mode == "neck":
        return p3.mask_up(k, x, y - 4, seed)
    if T_PULL <= tt < T_SNAP:                                       # the drop, eased, a slight wobble
        p = ease(clamp((tt - T_PULL) / (T_SNAP - T_PULL)))
        c = k.c
        c.save(); c.translate(0, -44 * (1 - p)); c.rotate(0.08 * (1 - p) - 0.04 * math.sin(math.pi * p))
        try:
            return _saved["mask"](k, x, y, "down", seed)
        finally:
            c.restore()
    return _saved["mask"](k, x, y, mode, seed)


def _punch(t):
    z, dx, dy = _saved["punch"](t)
    if SHOT10[0] + T_PULL - 0.1 <= t < SHOT10[1]:                   # push in on Pam for the payoff
        e = ease(clamp((t - (21.0 + T_PULL - 0.1)) / 0.4))
        k = 0.16 * e
        z *= 1 + k; dx += -(440 - 270) * k; dy += -(300 - 480) * k
    return z, dx, dy


def apply():
    _saved.update(pam0=xa._pam0, hook=xa._pam_hook, mask=px.mask_strip, punch=xa.punch,
                  pull=tb.T_PULL, snap=tb.T_SNAP)
    xa._pam0 = _pam3
    xa._pam_hook = _pam_hook
    px.mask_strip = _mask
    xa.punch = _punch
    tb.T_PULL, tb.T_SNAP = T_PULL, T_SNAP


def restore():
    xa._pam0, xa._pam_hook, xa.punch = _saved["pam0"], _saved["hook"], _saved["punch"]
    px.mask_strip = _saved["mask"]
    tb.T_PULL, tb.T_SNAP = _saved["pull"], _saved["snap"]
