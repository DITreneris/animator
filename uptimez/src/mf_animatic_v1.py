"""ANIMATIC v1 (pinned to storyboard mf_sb_v3) for "Mandatory Fun": storyboard v2 (mf_sb.py, untouched) re-timed to the real voice takes
(mf_timing.py, 37.35 s) with lip-sync from mf_visemes_v1.json (phoneme visemes on the 12 fps drawing grid, from the
takes in mf_mix_v1.wav). Mouths: Don iwry_mouths.don_mouth over his head; Sofia and Pam through their own mouth=
parameter. The robot speaks through its screen, no mouth. Character calls are swapped for lip-synced ones only inside
this module (the storyboard, the set sheet helpers and the yank test keep their own)."""
import json
import os
import types
import mf_sb_v3 as sb
import mf_set_sheet as ss
import mf_yank as yk
import mf_timing as T
import don_mf
import sofia_mf
import pam_mf
import iwry_mouths as im

HERE = os.path.dirname(os.path.abspath(__file__))
VIS = json.load(open(os.path.join(HERE, "mf_visemes_v1.json")))
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


def _don(k, *a, **kw):
    out = don_mf.don(k, *a, **kw)
    c = code("DON")
    if c:
        im.don_mouth(k, out["head"], c)
    return out


def _sofia(*a, **kw):
    if kw.get("mouth") is None:
        kw["mouth"] = code("SOF") or None
    return sofia_mf.sofia(*a, **kw)


def _pam(*a, **kw):
    if kw.get("mouth") is None:
        kw["mouth"] = code("PAM") or None
    return pam_mf.pam(*a, **kw)


DMX, SMX, PMX = _proxy(don_mf, don=_don), _proxy(sofia_mf, sofia=_sofia), _proxy(pam_mf, pam=_pam)
for mod in (sb, ss, yk):
    mod.dm, mod.sm, mod.pm = DMX, SMX, PMX

TIMED = T.build(sb.PANELS)
DURATION = round(T.duration(sb.PANELS), 3)


def _wrap(a0, a1, fn, t0, t1, mode):
    def g(k, t, tl):
        CUR[0] = t
        ts = t0 + (t - a0) * ((t1 - t0) / (a1 - a0) if mode == "stretch" else 1.0)
        ts = min(ts, t1 - 1e-3)
        raw = t0 + (RAW_T - a0) * ((t1 - t0) / (a1 - a0) if mode == "stretch" else 1.0)
        sb.RAW_T = min(raw, t1 - 1e-3)
        sb.PANEL_DUR[fn.__name__] = a1 - a0                # so world() undoes the engine's push over the new length
        fn(k, ts, ts - t0)
    g.__name__ = fn.__name__
    return g


PANELS = [(a0, a1, _wrap(a0, a1, fn, t0, t1, mode)) for a0, a1, fn, t0, t1, mode in TIMED]


def shake(t):
    return 0
