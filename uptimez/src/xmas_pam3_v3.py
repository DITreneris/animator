"""Routes the Christmas film's Pam to the v3 canon figure (pam_xmas3), for the v3 sheet and the film v2.
Inside xmas_anim's panels, px.pam is hooked (xmas_anim._pam -> _pam0); this swaps _pam0 for pam_xmas3 and swaps
the talking-mouth hook for one with her dusty-rose lips (the Secret Santa mouths at 0.8, as in pam_ss).
Per film time: the mask's neck spot becomes "up" (pushed up on her head); "glance" in the still beat of shot 5
(9.50-9.80 s, the smallest smile at Don before the horror); "over" while she says "Human in the loop.".
apply() / restore() switch it on and off."""
import kit
import xmas_anim as xa
import pam_xmas as px
import pam_xmas3_v3 as p3
import pam_ss as ps
import iwry_mouths as mo
import pam_mf as pm

GLANCE = (9.50, 9.80)
OVER = (23.0, 24.7)
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


def apply():
    _saved.update(pam0=xa._pam0, hook=xa._pam_hook)
    xa._pam0 = _pam3
    xa._pam_hook = _pam_hook


def restore():
    xa._pam0, xa._pam_hook = _saved["pam0"], _saved["hook"]
