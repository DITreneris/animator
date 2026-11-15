"""The HR robot, "Mandatory Fun", v1. The robot from the last three films (waiter_kit shell, wheel, bow tie, the big
HR badge from robot_tg v2, the v3 screen), with no costume at all: the pilgrim hat is gone.
New screen states (full-screen colour, a bold icon, the words in two lines, a glow round the screen):
"insufficient" (red, X: INSUFFICIENT / FUN), "approval" (amber, warning triangle: HUMAN APPROVAL / REQUIRED),
"approved" (green tick, small "APPROVER: PAM": shot 9, it accepts her answer), "detected" (green tick: FUN /
DETECTED). Idle and "scan" come from robot_tg. scan_beam() projects the scan: a translucent cyan fan from the screen
to a face, with a bright line sweeping down it (the same beam in shot 6 on Don and shot 12 on Pam).
New poses: POSE_CUFFS (one hand up, Don's yellow cuffs dangling: shot 8), POSE_NOD (head dips: shot 9).
robot_tg, waiter_kit and every earlier robot are untouched.
Usage: robot(k, x, feet, s, pose, state, look, side, seed, head_dx, head_rot, cuffs=False) -> points + "screen"."""
import math
import cairo
import kit
import waiter_kit as w
import santa_robot as sr
import robot_tg as rt
import props_mf as pr
from kit import INK, ellipse

RED = rt.RED
AMBER = (1.00, 0.72, 0.12)
GREEN = rt.GREEN
CYAN = sr.GLOW_V3
SRX, SRY = rt.SCREEN_RX, rt.SCREEN_RY
STATES = {"insufficient": (("INSUFFICIENT", "FUN"), RED, "x"),
          "approval": (("HUMAN APPROVAL", "REQUIRED"), AMBER, "warn"),
          "approved": (("APPROVED",), GREEN, "tick"),
          "detected": (("FUN", "DETECTED"), GREEN, "tick")}

POSE_CUFFS = (0.0, -6, 0, (-20, 0), (150, 24))     # 8: the far hand up, holding Don's cuffs like evidence
POSE_NOD = "stand"                                  # 9: drawn with head_rot / head_dx for the nod


def icon(c, kind, x, y, r, col):
    c.save(); c.translate(x, y)
    c.set_line_cap(1); c.set_line_join(1)
    if kind == "x":
        path = lambda: (c.move_to(-r, -r), c.line_to(r, r), c.move_to(r, -r), c.line_to(-r, r))
    elif kind == "tick":
        path = lambda: (c.move_to(-r, 0), c.line_to(-r * 0.3, r * 0.7), c.line_to(r, -r * 0.8))
    else:
        path = lambda: (c.move_to(0, -r), c.line_to(r * 1.05, r * 0.8), c.line_to(-r * 1.05, r * 0.8), c.close_path())
    for wd, cl in ((r * 0.9, (*col, 0.35)), (r * 0.62, (0.02, 0.04, 0.08, 1)), (r * 0.42, (*col, 1))):
        path(); c.set_source_rgba(*cl); c.set_line_width(wd); c.stroke()
    if kind == "warn":
        c.set_source_rgb(0.02, 0.04, 0.08); c.set_line_width(r * 0.22)
        c.move_to(0, -r * 0.25); c.line_to(0, r * 0.3); c.stroke()
        c.arc(0, r * 0.58, r * 0.1, 0, 2 * math.pi); c.fill()
    c.restore()


def _lines(c, lines, col, ys, size):
    sizes = size if isinstance(size, (tuple, list)) else [size] * len(lines)
    for txt, ty, size in zip(lines, ys, sizes):
        c.save()
        c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(size)
        tw = c.text_extents(txt).x_advance
        sc = min(1.0, (SRX * 2 - 12 - abs(ty) * 0.5) / tw)
        c.translate(0, ty); c.scale(sc, 1)
        c.move_to(-tw / 2, 0); c.text_path(txt)
        c.set_source_rgba(*col, 0.35); c.set_line_width(5); c.stroke_preserve()
        c.set_source_rgb(0.02, 0.04, 0.08); c.set_line_width(2.4); c.stroke_preserve()
        c.set_source_rgb(*col); c.fill()
        c.restore()


def screen(k, state, look=(0, 0), talk=0.0, side=1, seed=0, t=0.0):
    c = k.c
    if state not in STATES:
        rt.screen(k, state, look, talk, side, seed, t)
        return
    lines, col, ic = STATES[state]
    c.set_source_rgba(*col, 0.30); c.save(); c.scale(SRX + 10, SRY + 10); c.arc(0, 0, 1, 0, 2 * math.pi)
    c.restore(); c.fill()                                               # glow round the screen
    ellipse(k, 0, 0, SRX, SRY, w.SCREEN, seed, shadow=False, lw=2)
    c.save(); c.scale(SRX - 3, SRY - 3); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
    c.set_source_rgba(*col, 0.16); c.fill()                            # the whole screen tinted
    c.save(); c.scale(side, 1)
    if state == "approved":
        icon(c, "tick", 0, -8, 15, col)
        _lines(c, ("APPROVER: PAM",), col, (24,), 11)
    else:
        lay = {"insufficient": ((4, 28), (17, 25)), "approval": ((4, 27), (16, 20)), "detected": ((5, 28), (22, 18))}
        ys, sz = lay[state]
        icon(c, ic, 0, -23 if state == "detected" else -20, 8 if state == "detected" else 9, col)
        _lines(c, lines, col, ys, sz)
    c.restore()


def scan_beam(k, src, face, half, p, col=CYAN):
    """A translucent fan from the screen centre `src` to a face centred at `face` (half-height `half`), with a bright
    line at progress p (0 = top of the face, 1 = bottom)."""
    c = k.c
    sx, sy = src
    fx, fy = face
    c.save()
    c.move_to(sx, sy - 6); c.line_to(fx, fy - half); c.line_to(fx, fy + half); c.line_to(sx, sy + 6); c.close_path()
    lg = cairo.LinearGradient(sx, sy, fx, fy)
    lg.add_color_stop_rgba(0, *col, 0.45); lg.add_color_stop_rgba(1, *col, 0.12)
    c.set_source(lg); c.fill()
    ly = fy - half + 2 * half * p
    c.set_source_rgba(*col, 0.45); c.set_line_width(7); c.move_to(fx - half * 0.9, ly); c.line_to(fx + half * 0.9, ly); c.stroke()
    c.set_source_rgb(0.85, 1, 1); c.set_line_width(2.2); c.move_to(fx - half * 0.9, ly); c.line_to(fx + half * 0.9, ly); c.stroke()
    c.set_source_rgba(*col, 0.6); c.set_line_width(1.6)
    c.move_to(sx, sy); c.line_to(fx - half * 0.9, ly); c.stroke()
    c.restore()


def robot(k, x, feet, s=1.0, pose="stand", state="eager", look=(0, 0), side=1, talk=0.0, seed=900, badge=True,
          head_dx=None, head_rot=None, wobble=0.0, t=0.0, cuffs=False):
    c = k.c
    old_badge = w._badge
    w._badge = rt.tg_badge
    try:
        out = w.robot(k, x, feet, s, pose, "eager", look, wobble, side, talk, None, seed, badge, None, head_dx, head_rot)
    finally:
        w._badge = old_badge
    named = isinstance(pose, str)
    tilt = (w.POSES[pose] if named else pose)[0] + wobble
    hdx = head_dx if head_dx is not None else (w.HEAD_DX.get(pose, 0) if named else 0)
    hrot = head_rot if head_rot is not None else (w.HEAD_ROT.get(pose, 0) if named else 0)
    hx, hy = out["head"]
    c.save(); c.translate(x, feet); c.scale(s * side, s); c.rotate(tilt)
    c.translate(hdx, (hy - feet) / s); c.rotate(hrot)
    ellipse(k, 0, 0, 50, 44, w.BODY, seed + 68, shadow=False, lw=2.4)   # repaint the head over the antenna
    screen(k, state, look, talk, side, seed + 69, t)
    c.restore()
    out["screen"] = (x + hdx * s * side, hy)
    if cuffs:                                                          # Don's cuffs dangling from the raised hand
        hx_, hy_ = out["hands"][1]
        pr.chain(k, hx_, hy_ + 2 * s, hx_ + 3 * s, hy_ + 16 * s, s, sag=0.0, links=2)
        for (dx, dy) in ((-8, 26), (12, 30)):
            c.set_source_rgb(*INK); c.set_line_width(6.2 * s); c.arc(hx_ + dx * s, hy_ + dy * s, 9 * s, 0, 2 * math.pi); c.stroke()
            c.set_source_rgb(*pr.TOY_YELLOW); c.set_line_width(3.6 * s); c.arc(hx_ + dx * s, hy_ + dy * s, 9 * s, 0, 2 * math.pi); c.stroke()
        ellipse(k, hx_, hy_, 8 * s, 8 * s, w.ARM if hasattr(w, "ARM") else (0.6, 0.62, 0.66), seed + 5, shadow=False, lw=1.6 * s)
    return out
