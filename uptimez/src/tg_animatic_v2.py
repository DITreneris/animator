"""ANIMATIC v2 (tg_animatic_v1.py = v1, kept; v2 = the new laugh, tg_mix_v2.wav / tg_visemes_v2.json) for "Raises for Everyone": storyboard v3 (tg_sb.py, untouched) re-timed to the real voice takes
(tg_timing.py, 36.6 s) with lip-sync: each speaking character's mouth follows tg_visemes.json (phoneme visemes on the
12 fps drawing grid, from the takes in tg_mix_v1.wav). Don's smug smirk is fixed here (don_tg.SMUG_FIX).
Mouths: Don iwry_mouths.don_mouth over his head, Sofía and Pam drawn in their own frames (lean included).
The robot speaks through its screen (the verdict words), so it has no mouth."""
import json
import os
import types
import tg_sb_v3 as sb
import tg_timing as T
import don_tg
import iwry_mouths as im

don_tg.SMUG_FIX = True
HERE = os.path.dirname(os.path.abspath(__file__))
VIS = json.load(open(os.path.join(HERE, "tg_visemes_v2.json")))
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


def _don(*a, **kw):
    out = don_tg.don(*a, **kw)
    c = code("DON")
    if c and a and getattr(a[0], "boil", None) is not None:
        im.don_mouth(a[0], out["head"], c)
    return out


def _sofia(*a, **kw):
    if kw.get("mouth") is None:
        kw["mouth"] = code("SOF") or None
    return _ST.sofia(*a, **kw)


def _pam(*a, **kw):
    if kw.get("mouth") is None:
        kw["mouth"] = code("PAM") or None
    return _PT.pam(*a, **kw)


_ST, _PT = sb.st, sb.pt
sb.dt = _proxy(don_tg, don=_don)
sb.st = _proxy(_ST, sofia=_sofia)
sb.pt = _proxy(_PT, pam=_pam)

TIMED = T.build(sb.PANELS)
DURATION = round(T.duration(sb.PANELS), 3)


def _wrap(t0n, t1n, fn, shift, v1):
    def g(k, t, tl):
        CUR[0] = t
        old = min(t - shift, v1 - 1e-3)
        sb.RAW_T = min(RAW_T - shift, v1 - 1e-3)
        fn(k, old, old - (t0n - shift))
    g.__name__ = fn.__name__
    return g


PANELS = [(t0, t1, _wrap(t0, t1, fn, sh, v1)) for t0, t1, fn, sh, v1 in TIMED]


def shake(t):
    for t0, t1, fn, sh, v1 in TIMED:
        if t0 <= t < t1:
            return sb.shake(min(t - sh, v1 - 1e-3))
    return 0
