"""FULL ANIMATION v1 (pinned; ss_anim.py is v2) for "Secret Santa": animatic v3 (same takes, mix, timing and lip-sync, 40.8 s) plus the polish
and the frame-check fixes:
- blinks: Pam and Sofia blink for two drawings every few seconds (own rhythms); Don's shades hide his, the robot has
  its screen;
- a subtle idle sway: every character breathes (about 1-2 px, a slow vertical swell about the feet), Sofia's crystal
  earrings swing gently when nothing else moves them;
- Don's vest card sits clear of his arm (reads TOP SECRET / SANTA whole); the UptimeZ sign hangs where every camera
  shows it whole or not at all; Sofia's tail in 2 lands on her head; Don's tail in 6 points up to his mouth.
Render: engine_v (540) and engine_hd (1080), tagged BT.709 at encode."""
import json
import math
import os
import types
import ss_sb as sb
import ss_set as S
import ss_set_sheet as sss
import ss_timing as T
import pam_ss
import don_ss
import sofia_ss
import pam_mf
from kit import INK, ellipse

HERE = os.path.dirname(os.path.abspath(__file__))
VIS = json.load(open(os.path.join(HERE, "ss_visemes_v1.json")))
RAW_T = 0.0
CUR = [0.0]


def code(who):
    seq = VIS[who]
    i = int(round(CUR[0] * 12))
    return seq[i] if 0 <= i < len(seq) else ""


def blinking(period, phase):
    """Two drawings (1/6 s) closed in every `period` seconds."""
    x = (CUR[0] + phase) % period
    return x < 2 / 12.0


def sway(k, x, feet, s, phase, fn):
    c = k.c
    a = 0.006 * math.sin(2 * math.pi * CUR[0] / 3.1 + phase)
    c.save(); c.translate(x, feet); c.scale(1, 1 + a); c.translate(-x, -feet)
    try:
        return fn()
    finally:
        c.restore()


def _proxy(mod, **over):
    p = types.ModuleType(mod.__name__ + "_anim")
    p.__dict__.update({k: v for k, v in mod.__dict__.items() if not k.startswith("__")})
    p.__dict__.update(over)
    return p


def _pam(k, x, feet, s=1.0, *a, **kw):
    kw["mouth"] = code("PAM") or None
    out = sway(k, x, feet, s, 0.0, lambda: pam_ss.pam(k, x, feet, s, *a, **kw))
    if blinking(3.4, 0.9) and "head" in out:                 # her lids down over both eyes (above the lenses)
        hx, hy = out["head"]
        c = k.c
        c.save(); c.rectangle(hx - 60 * s, hy - 30 * s, 120 * s, 38 * s); c.clip()
        for sx in (-17, 17):
            ellipse(k, hx + sx * s, hy - 1 * s, 13.5 * s, 13.5 * s, pam_mf.SKIN, 5, shadow=False, outline=False)
        c.restore()
        c.set_source_rgb(*INK); c.set_line_width(3.6 * s); c.set_line_cap(1)
        for sx in (-17, 17):
            ex = hx + sx * s
            c.move_to(ex - 11 * s, hy + 1 * s); c.curve_to(ex - 4 * s, hy + 5 * s, ex + 4 * s, hy + 5 * s, ex + 11 * s, hy + 1 * s)
            c.stroke()
    return out


def _don(k, x, feet, s=1.0, *a, **kw):
    kw["mouth"] = code("DON") or None
    return sway(k, x, feet, s, 1.7, lambda: don_ss.don(k, x, feet, s, *a, **kw))


def _sofia(k, x, feet, s=1.0, pose="stand", face_kind="neutral", *a, **kw):
    kw["mouth"] = code("SOF") or None
    if blinking(3.9, 2.1) and not kw["mouth"]:
        face_kind = "closed"
    if tuple(kw.get("lag", (0, 0))) == (0, 0):            # the earrings swing gently
        kw["lag"] = (1.6 * math.sin(2 * math.pi * CUR[0] / 1.5), 0)
    return sway(k, x, feet, s, 3.1, lambda: sofia_ss.sofia(k, x, feet, s, pose, face_kind, *a, **kw))


PMX, DMX, SMX = _proxy(pam_ss, pam=_pam), _proxy(don_ss, don=_don), _proxy(sofia_ss, sofia=_sofia)
for mod in (sb, sss):
    mod.ps, mod.ds, mod.so = PMX, DMX, SMX

don_ss.CLEAN = True
don_ss.CARD_FIX = True
sb.S4_FIX[0] = True
sb.TAG_FIX[0] = True
sb.TAIL_FIX[0] = True
S.SIGN_FIX[0] = True
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
