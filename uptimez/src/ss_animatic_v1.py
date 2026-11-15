"""ANIMATIC v1 (pinned; ss_animatic.py is v2) for "Secret Santa": storyboard v2 (ss_sb.py) re-timed to the real voice takes (ss_timing.py, piecewise
warps, about 40.8 s) with lip-sync from ss_visemes_v1.json (phoneme visemes on the 12 fps grid). Pam, Sofia and Don
speak through their own mouth= parameter (the storyboard's placeholder flaps are replaced); the robot speaks through
its screen. The swaps live only inside this module: the storyboard, the set sheet and the motion test keep their
own character calls."""
import json
import os
import types
import ss_sb as sb
import ss_set_sheet as sss
import ss_timing as T
import pam_ss
import don_ss
import sofia_ss

HERE = os.path.dirname(os.path.abspath(__file__))
VIS = json.load(open(os.path.join(HERE, "ss_visemes_v1.json")))
RAW_T = 0.0
CUR = [0.0]


def code(who):
    seq = VIS[who]
    i = int(round(CUR[0] * 12))
    return seq[i] if 0 <= i < len(seq) else ""


def _proxy(mod, **over):
    p = types.ModuleType(mod.__name__ + "_lips")
    p.__dict__.update({k: v for k, v in mod.__dict__.items() if not k.startswith("__")})
    p.__dict__.update(over)
    return p


def _pam(*a, **kw):
    kw["mouth"] = code("PAM") or None
    return pam_ss.pam(*a, **kw)


def _don(*a, **kw):
    kw["mouth"] = code("DON") or None
    return don_ss.don(*a, **kw)


def _sofia(*a, **kw):
    kw["mouth"] = code("SOF") or None
    return sofia_ss.sofia(*a, **kw)


PMX, DMX, SMX = _proxy(pam_ss, pam=_pam), _proxy(don_ss, don=_don), _proxy(sofia_ss, sofia=_sofia)
for mod in (sb, sss):
    mod.ps, mod.ds, mod.so = PMX, DMX, SMX

TIMED = T.build(sb.PANELS)
DURATION = round(T.duration(sb.PANELS), 3)


def _wrap(a0, a1, fn, t0, t1, ks):
    def g(k, t, tl):
        CUR[0] = t
        sbl = min(T.sb_local(ks, t - a0), t1 - t0 - 1e-3)
        sb.PANEL_DUR[fn.__name__] = a1 - a0
        sb.PUSH_TL[0] = tl
        sb.RAW_T = t0 + sbl
        try:
            fn(k, t0 + sbl, sbl)
        finally:
            sb.PUSH_TL[0] = None
    g.__name__ = fn.__name__
    return g


PANELS = [(a0, a1, _wrap(a0, a1, fn, t0, t1, ks)) for a0, a1, fn, t0, t1, ks in TIMED]


def shake(t):
    return 0
