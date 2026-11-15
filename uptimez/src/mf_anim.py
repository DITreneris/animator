"""ANIMATION v2 (mf_anim_v1.py = v1, kept): shot 12 framed wider (storyboard v5) and a gentler final push, so
Pam's and Don's faces stay whole in the payoff.
ANIMATION v1 of "Mandatory Fun" (540 rough of the release), 37.35 s. Built on animatic v2 (mf_animatic.py: the
approved timing and lip-sync, kept as is) with the approved mix (mf_mix_v1.wav). Adds the acting and polish by
hooking drawing functions for this render only (every module and earlier render unchanged):
- blinks: Don, Sofia and Pam (only on open-eyed faces, never on the verdict stare, the wink or closed eyes);
- Sofia's gold hoops swing gently (she writes, turns, walks);
- the verdict light spills: red from INSUFFICIENT FUN, amber from HUMAN APPROVAL REQUIRED, green from the tick and
  FUN DETECTED, onto whatever is near the screen;
- the robot's idle face breathes (a slow glow pulse);
- camera punches: a hit on the door bang, a hit on the red verdict, a jolt on "APPROVED!", a small push on the
  DING, two tiny jolts on the clicks (hers bigger), a slow push on FUN DETECTED; the yank shake stays;
- a light cool office vignette."""
import math
import cairo
import kit
from kit import clamp, ease, INK
import mf_animatic as an
import sofia_mf
import robot_mf
import don_mf

DURATION = an.DURATION
RAW_T = 0.0
ACT = {"t": 0.0}
DON_BLINKS = (4.9, 12.7, 14.9)
SOF_BLINKS = (3.25, 6.6, 10.2, 13.2, 22.6)
PAM_BLINKS = (3.45, 22.9, 29.6)
GLOWS = []
VERDICT = {"insufficient": robot_mf.RED, "approval": robot_mf.AMBER, "approved": robot_mf.GREEN,
           "detected": robot_mf.GREEN}


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


def _face_of(a, kw, i):
    return a[i] if len(a) > i else kw.get("face", kw.get("face_kind", "neutral"))


# ------------------------------------------------------------------ Don
_don_prev = an.DMX.don


def _don(*a, **kw):
    out = _don_prev(*a, **kw)
    face = _face_of(a, kw, 5)
    if face in ("hero", "neutral") and not kw.get("lean") and blinking(DON_BLINKS) and not an.code("DON"):
        hx, hy = out["head"]
        lids(a[0], hx, hy + 4, don_mf.SKIN, 12.5, 77)
    return out


# ------------------------------------------------------------------ Sofia: blinks inside her frame, the hoops swing
_sface0 = sofia_mf.face


def _sface(k, x, y, kind="neutral", look=(0, 0), seed=0):
    _sface0(k, x, y, kind, look, seed)
    if kind == "neutral" and blinking(SOF_BLINKS):
        lids(k, x, y, sofia_mf.SKIN, 13, seed + 70)


_sofia_prev = an.SMX.sofia


def _sofia(*a, **kw):
    t = ACT["t"]
    kw.setdefault("lag", (4 * math.sin(t * 5.0), 1.2 * math.sin(t * 10.0)))
    return _sofia_prev(*a, **kw)


# ------------------------------------------------------------------ Pam: blinks over her calm lid
_pam_prev = an.PMX.pam


def _pam(*a, **kw):
    out = _pam_prev(*a, **kw)
    face = _face_of(a, kw, 5)
    if face in ("neutral", "read") and blinking(PAM_BLINKS) and not an.code("PAM"):
        hx, hy = out["head"]
        lids(a[0], hx, hy + 4, an.PMX.SKIN, 12.5, 88)
    return out


# ------------------------------------------------------------------ the robot: verdict light, idle pulse
_robot0 = robot_mf.robot


def _robot(k, *a, **kw):
    out = _robot0(k, *a, **kw)
    state = a[4] if len(a) > 4 else kw.get("state", "eager")
    sx_, sy_ = out["screen"]
    dx, dy = k.c.user_to_device(sx_, sy_)
    if state in VERDICT:
        r = k.c.user_to_device_distance(170, 0)[0]
        GLOWS.append((dx, dy, abs(r), VERDICT[state], 0.20))
    elif state == "eager":
        r = k.c.user_to_device_distance(80, 0)[0]
        GLOWS.append((dx, dy, abs(r), robot_mf.CYAN, 0.05 + 0.04 * math.sin(ACT["t"] * 2.6)))
    return out


def _glow(c, x, y, r, a, col):
    g = cairo.RadialGradient(x, y, 0, x, y, r)
    g.add_color_stop_rgba(0, *col, a); g.add_color_stop_rgba(1, *col, 0)
    c.set_source(g); c.arc(x, y, r, 0, 2 * math.pi); c.fill()


def vignette(c):
    g = cairo.RadialGradient(270, 470, 280, 270, 470, 660)
    g.add_color_stop_rgba(0, 0.10, 0.14, 0.24, 0.0)
    g.add_color_stop_rgba(1, 0.10, 0.14, 0.24, 0.20)
    c.set_source(g); c.paint()


# ------------------------------------------------------------------ camera punches (animatic times)
def punch(t):
    z, dx_, dy_ = 1.0, 0.0, 0.0
    if 16.25 <= t < 16.95:                                  # the red verdict hits
        z = 1 + 0.06 * (1 - ease(u(t, 16.25, 0.7)))
    if 24.12 <= t < 24.32:                                  # "APPROVED!" jolts the frame
        f = int((t - 24.12) * 30)
        dx_ += (5, -4, 3, -2, 1, 0)[f % 6]; dy_ += (-4, 4, -2, 2, -1, 0)[f % 6]
    if 25.07 <= t < 25.85:                                  # the DING: a small push
        z = 1 + 0.035 * ease(u(t, 25.07, 0.25))
    if 26.45 <= t < 26.52:                                  # the robot's click
        dy_ += 2
    if 27.25 <= t < 27.36:                                  # hers: bigger
        dx_ += 3; dy_ += 4
    if t >= 34.45:                                          # FUN DETECTED: a slow push while the contrast holds
        z = 1 + 0.03 * ease(u(t, 34.45, 2.6))
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
        an.DMX.don, an.SMX.sofia, an.PMX.pam = _don, _sofia, _pam
        sofia_mf.face, robot_mf.robot = _sface, _robot
        try:
            fn(k, t, tl)
        finally:
            an.DMX.don, an.SMX.sofia, an.PMX.pam = _don_prev, _sofia_prev, _pam_prev
            sofia_mf.face, robot_mf.robot = _sface0, _robot0
        c.restore()
        c.save(); c.identity_matrix()
        for gx, gy, r, col, a in GLOWS:
            _glow(c, gx, gy, r, a, col)
        c.restore()
        vignette(c)
    return panel


PANELS = [(t0, t1, wrap(fn)) for t0, t1, fn in an.PANELS]
