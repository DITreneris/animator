"""Mandatory Fun, the yank motion test (shot 11, wide and locked), about 3.4 s at 540x960 for engine_v.py.
Beats at real timing: Sofia walks out left (0.0-1.6); Don lunges after her (0.35-0.85); the chain goes taut, a
held frame with a twang (0.85-1.0); he snaps back with an overshoot, a two-frame shake, the cap pops up (1.0-1.3);
he drops into his chair (1.3-1.6), the cap lands back crooked (1.75); his slump; Pam straightens her glasses
(2.3) and looks at him, shy (2.8). Silent apart from temporary effects (sound_mf_yank.py)."""
import math
import kit
from kit import INK, W, H
import mf_set as ms
import sofia_mf as sm
import don_mf as dm
import pam_mf as pm
import robot_mf as rm
import props_mf as pr

DURATION = 3.4
RAW_T = 0.0
CAM = (612, 486, 0.95)
X = ms.POS
SEAT = ms.FEET + ms.SEAT_DROP
PAM_ARM = pm.ik(-1, -34, pm.BT + 52) + (8, 0)
STAND = (-8, 0, 8, 0)
CHAIN_L = 205                       # world units of chain between the two cuffs: taut at this distance


def clamp(v, a=0.0, b=1.0):
    return max(a, min(b, v))


def ease(u):
    u = clamp(u)
    return u * u * (3 - 2 * u)


def lerp(a, b, u):
    return a + (b - a) * u


def blend(p, q, u):
    return tuple(lerp(a, b, u) for a, b in zip(p, q))


def don_state(t):
    """x, feet, lean, pose, face, cap (True or a flying offset), seated?"""
    if t < 0.35:
        return X["don"], ms.FEET, 0.0, STAND, "pout", True
    if t < 0.85:                                            # the lunge
        u = ease((t - 0.35) / 0.5)
        return lerp(X["don"], X["don"] - 70, u), ms.FEET, lerp(0, -20, u), blend(STAND, dm.POSE_LUNGE, u), "hero", True
    if t < 1.0:                                             # taut: held, the face changes
        return X["don"] - 70, ms.FEET, -20.0, dm.POSE_LUNGE, "snap", (-6, -6, -18)
    if t < 1.3:                                             # snapped back, overshoot past upright
        u = (t - 1.0) / 0.3
        e = math.sin(u * math.pi * 0.5)
        lean = lerp(-20, 12, e)
        cap = (lerp(-6, 30, u), -6 - 120 * math.sin(u * math.pi * 0.8), lerp(-18, 220, u))
        return lerp(X["don"] - 70, X["don"] + 8, e), lerp(ms.FEET, ms.FEET + 30, u), lean, \
            blend(dm.POSE_LUNGE, dm.POSE_SNAP, min(1, u * 2)), "snap", cap
    if t < 1.75:                                            # drops into the chair, cap still in the air
        u = ease((t - 1.3) / 0.3)
        v = (t - 1.3) / 0.45
        cap = (lerp(30, 10, v), lerp(-60, 0, v * v) - 10, lerp(220, 360 - 14, v))
        return lerp(X["don"] + 8, X["don"], u), lerp(ms.FEET + 30, SEAT - 20, u), lerp(12, 0, u), \
            blend(dm.POSE_SNAP, STAND, u), "snap" if t < 1.5 else "collapse", cap
    return X["don"], SEAT - 20, 0.0, STAND, "collapse", (10, -8, -14)


def frame(k, t, tl):
    c = k.c
    T = RAW_T
    c.save()
    push = 1 + 0.03 * (tl / DURATION)                       # undo the engine's slow push: this shot is locked
    c.translate(W / 2, H / 2); c.scale(1 / push, 1 / push); c.translate(-W / 2, -H / 2)
    sh = 0.0
    if 1.0 <= T < 1.07:
        sh = 9 if int(T * 30) % 2 == 0 else -9
    c.translate(0, sh)
    ms.with_cam(c, CAM)
    ms.set_dressing(k, door_open=0.6)
    for key in ("sofia", "pam"):
        ms.chair_back(k, X[key], seed=130)
    if t < 0.2:
        ms.chair_back(k, X["don"], seed=130)
    # Sofia: up and out, notebook at her chest
    sx = lerp(X["sofia"] - 20, X["door"] + 40, ease(t / 1.6))
    if t < 1.75:
        sm.sofia(k, sx, ms.FEET, 1.0, "walk", "neutral", look=(-0.9, 0), step=(t * 1.6) % 1.0, carry=True, seed=99)
    # Pam: anchored in her seat; her arm jerks at the taut frame; then the glasses, then the look
    jerk = 6 if 0.85 <= t < 1.05 else 0
    if t < 2.3:
        pf, pose, kw = "neutral", PAM_ARM, dict(look=(-1, 0))
    elif t < 2.75:
        pf, pose, kw = "avert", PAM_ARM[:2] + pm.POSE_GLASSES[2:], dict(glasses="up", finger="bridge")
    else:
        pf, pose, kw = "dinner", PAM_ARM, dict(glasses="up")
    o_p = {}
    ms.seated(k, lambda: o_p.update(pm.pam(k, X["pam"] - jerk, SEAT, 1.0, pose, pf, seed=96, **kw)))
    rm.robot(k, X["robot"], ms.FEET_BACK, 1.0, "stand", "eager", seed=97)
    # Don
    dx, dfeet, lean, pose, face, cap = don_state(t)
    if t >= 0.2 and dfeet < ms.FEET + 31:
        ms.chair_back(k, X["don"], seed=130)
    head_cap = cap if (cap is True or abs(cap[1]) < 20) else False
    c.save(); c.rectangle(-4000, -4000, 9000, 4000 + ms.FEET + 14); c.clip()   # nothing below the table's foot
    d = dm.don(k, dx, dfeet, 1.0, pose, face, lean=lean, look=(-1, 0) if t < 1.0 else (0, 0.4), cuff="R",
               belt_cuffs_on=False, cap=head_cap, seed=98)
    c.restore()
    if cap is not True and head_cap is False:              # the cap in flight, in the head's frame
        hx, hy = d["head"]
        dm.police_cap(k, hx + cap[0], hy - 70 + cap[1], 1.0, cap[2], seed=5)
    if 1.75 <= t:                                          # it landed crooked: drawn by don() via cap tuple
        pass
    ms.table(k)
    # Pam's cuffed wrist on the table and the chain to Don's cuff
    px_, py_ = X["pam"] - 52 - jerk, ms.TABLE_TOP - 2
    kit.ellipse(k, px_ - 8, py_, 9, 9, pm.SKIN, 7, shadow=False, lw=2)
    pc = pr.cuff(k, px_ + 6, py_ - 1, 1.0, math.pi / 2, loop_side=1)
    dc = d["cuff"]
    dist = math.hypot(pc[0] - dc[0], pc[1] - dc[1])
    sag = clamp((CHAIN_L - dist) / CHAIN_L, 0, 1) * 0.55
    pr.chain(k, dc[0], dc[1], pc[0], pc[1], 1.0, sag=sag)
    if 0.85 <= t < 1.05:                                   # the twang
        mx, my = (dc[0] + pc[0]) / 2, (dc[1] + pc[1]) / 2
        c.set_source_rgb(*INK); c.set_line_width(3); c.set_line_cap(1)
        for j in range(3):
            c.move_to(mx - 20 + j * 18, my - 22); c.line_to(mx - 12 + j * 18, my - 34); c.stroke()
    if 0.35 <= t < 0.8:                                    # lunge speed lines behind him
        c.set_source_rgba(0.35, 0.40, 0.50, 0.8); c.set_line_width(3)
        for j in range(3):
            c.move_to(dx + 60, 420 + j * 40); c.line_to(dx + 110, 420 + j * 40); c.stroke()
    c.restore()


def shake(t):
    return 0


PANELS = [(0.0, DURATION, frame)]
