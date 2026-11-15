"""ANIMATION v1 of "Raises for Everyone" (540 rough of the release), 36.6 s. Built on animatic v2 (tg_animatic.py,
the approved timing, laugh and lip-sync, kept as is) with the approved mix (tg_mix_v2.wav). Adds the acting and
polish by hooking drawing functions for this render only (every module and earlier render unchanged):
- blinks: Don, Sofía and Pam (eyelids over open eyes only, never on the verdict stare or the closed/laughing faces);
- Don's laugh shakes him: little bounces on every "ha";
- Sofía's star earrings swing gently while she talks and leans;
- the verdict light spills: red glow from "POLICY VIOLATION.", green from "ACCURATE." onto whatever is near the screen;
- steam curls off the turkey;
- camera punches: a jolt on the frame-0 slap, a hit on the red verdict, a small push on "No.", a push on "ACCURATE.",
  a nudge on the bite; the stamp shake stays;
- a light warm autumn vignette."""
import math
import cairo
import kit
from kit import clamp, ease, INK
import tg_animatic as an
import tg_sb as sb
import tg_set as ts
import sofia_tg as st
import don_tg
import robot_tg as rt

DURATION = an.DURATION
RAW_T = 0.0
ACT = {"t": 0.0}
DON_BLINKS = (1.4, 6.2, 12.6, 19.2, 27.0)
SOF_BLINKS = (4.6, 9.15, 18.9, 22.15, 31.0)
PAM_BLINKS = (3.0, 13.4, 16.9, 26.2)
LAUGH = (8.05, 9.4)
GLOWS = []


def u(t, t0, d):
    return clamp((t - t0) / d)


def blinking(times, d=0.14):
    return any(0 <= ACT["t"] - b < d for b in times)


def lids(k, x, y, skin, r, seed):
    c = k.c
    for ex in (-17, 17):
        kit.ellipse(k, x + ex, y, r, r, skin, seed + ex, shadow=False, outline=False)
        c.set_source_rgb(*INK); c.set_line_width(4); c.set_line_cap(1)
        c.move_to(x + ex - r + 1.5, y + 1); c.curve_to(x + ex - 4, y + 5, x + ex + 4, y + 5, x + ex + r - 1.5, y + 1)
        c.stroke()


# ------------------------------------------------------------------ Don: blinks and the laughing bounce
_don_prev = an.sb.dt.don                  # the animatic's lip-sync proxy


def _don(*a, **kw):
    a = list(a)
    face = a[5] if len(a) > 5 else kw.get("face", "neutral")
    if LAUGH[0] <= ACT["t"] < LAUGH[1] and len(a) > 2:
        a[2] = a[2] - 5 * abs(math.sin((ACT["t"] - LAUGH[0]) * 15))
    out = _don_prev(*a, **kw)
    if a and getattr(a[0], "boil", None) is not None and face in ("neutral", "grin", "drop") and blinking(DON_BLINKS):
        hx, hy = out["head"]
        lids(a[0], hx, hy + 4, don_tg.SKIN, 12.5, 77)
    return out


# ------------------------------------------------------------------ Sofía: blinks (inside her frame) and earrings
_sface0 = st.face


def _sface(k, x, y, kind="neutral", look=(0, 0), seed=0):
    _sface0(k, x, y, kind, look, seed)
    if kind in ("neutral", "tiny") and blinking(SOF_BLINKS):
        lids(k, x, y, st.SKIN, 13, seed + 70)


_sofia_prev = an.sb.st.sofia


def _sofia(*a, **kw):
    t = ACT["t"]
    kw.setdefault("lag", (4 * math.sin(t * 6.0), 1.2 * math.sin(t * 12.0)))
    return _sofia_prev(*a, **kw)


# ------------------------------------------------------------------ Pam: blinks over her calm lid
_pam_prev = an.sb.pt.pam


def _pam(*a, **kw):
    out = _pam_prev(*a, **kw)
    face = a[5] if len(a) > 5 else kw.get("face", "neutral")
    if face == "neutral" and blinking(PAM_BLINKS) and a and getattr(a[0], "boil", None) is not None:
        hx, hy = out["head"]
        lids(a[0], hx, hy + 4, an.sb.pt.SKIN, 12.5, 88)
    return out


# ------------------------------------------------------------------ the robot: verdict light spill
_robot0 = rt.robot


def _robot(k, *a, **kw):
    out = _robot0(k, *a, **kw)
    state = a[4] if len(a) > 4 else kw.get("state", "eager")
    if state in ("violation", "accurate") and getattr(k, "boil", None) is not None:
        sx_, sy_ = out["screen"]
        dx, dy = k.c.user_to_device(sx_, sy_)
        r = k.c.user_to_device_distance(170, 0)[0]
        GLOWS.append((dx, dy, abs(r), rt.RED if state == "violation" else rt.GREEN))
    return out


def _glow(c, x, y, r, a, col):
    g = cairo.RadialGradient(x, y, 0, x, y, r)
    g.add_color_stop_rgba(0, *col, a); g.add_color_stop_rgba(1, *col, 0)
    c.set_source(g); c.arc(x, y, r, 0, 2 * math.pi); c.fill()


# ------------------------------------------------------------------ the turkey steams
_turkey0 = ts.turkey


def _turkey(k, x, y, legs=2, s=1.0, seed=0):
    _turkey0(k, x, y, legs, s, seed)
    c = k.c
    t = ACT["t"]
    c.set_line_cap(1)
    for i, ox in enumerate((-16, 4, 22)):
        ph = (t * 0.7 + i * 0.33) % 1.0
        a = math.sin(math.pi * ph) * 0.55
        c.set_source_rgba(1, 1, 1, a); c.set_line_width(3.2 * s)
        bx, by = x + ox * s, y - 54 * s - ph * 46 * s
        c.move_to(bx, by + 18 * s)
        c.curve_to(bx - 7 * s, by + 10 * s, bx + 7 * s, by + 5 * s, bx, by - 4 * s)
        c.stroke()


def vignette(c):
    g = cairo.RadialGradient(270, 470, 270, 270, 470, 650)
    g.add_color_stop_rgba(0, 0.38, 0.20, 0.06, 0.0)
    g.add_color_stop_rgba(1, 0.38, 0.20, 0.06, 0.24)
    c.set_source(g); c.paint()


# ------------------------------------------------------------------ camera punches (animatic times)
def punch(t):
    z, dx_, dy_ = 1.0, 0.0, 0.0
    if 0.10 <= t < 0.30:                                    # the frame-0 slap
        f = int((t - 0.10) * 30)
        dx_ += (4, -3, 2, -1, 0, 0)[f % 6]; dy_ += (5, -4, 3, -1, 0, 0)[f % 6]
    if 9.6 <= t < 10.3:                                     # the red verdict hits
        z = 1 + 0.06 * (1 - ease(u(t, 9.6, 0.7)))
    if 16.15 <= t < 17.0:                                   # "No.": a small push
        z = 1 + 0.035 * ease(u(t, 16.15, 0.25))
    if 29.6 <= t < 30.45:                                   # "ACCURATE.": a push
        z = 1 + 0.05 * ease(u(t, 29.6, 0.2))
    if 21.0 <= t < 21.12:                                   # the bite
        dx_ += 2; dy_ += 3
    return z, dx_, dy_


def shake(t):
    return an.shake(t)


def wrap(fn):
    def panel(k, t, tl):
        c = k.c
        raw = RAW_T if abs(RAW_T - t) < 0.2 else t
        ACT["t"] = t
        an.RAW_T = RAW_T
        GLOWS.clear()
        z, ox, oy = punch(raw)
        c.save()
        c.translate(270 + ox, 480 + oy); c.scale(z, z); c.translate(-270, -480)
        an.sb.dt.don, an.sb.st.sofia, an.sb.pt.pam = _don, _sofia, _pam
        st.face, sb.rt.robot, ts.turkey = _sface, _robot, _turkey
        try:
            fn(k, t, tl)
        finally:
            an.sb.dt.don, an.sb.st.sofia, an.sb.pt.pam = _don_prev, _sofia_prev, _pam_prev
            st.face, sb.rt.robot, ts.turkey = _sface0, _robot0, _turkey0
        c.restore()
        c.save(); c.identity_matrix()
        for gx, gy, r, col in GLOWS:
            _glow(c, gx, gy, r, 0.20, col)
        vignette(c)
        c.restore()
    return panel


PANELS = [(t0, t1, wrap(fn)) for t0, t1, fn in an.PANELS]
