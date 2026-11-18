"""ANIMATION v3 of "Mandatory Fun" (18 Nov): a joke by 0:01 and a true loop. Wraps animation v2 (mf_anim.py, kept and
unchanged; its renders rebuild byte for byte) with:
- a cold open (OPEN s): the slide reads MANDATROY FUN with a red squiggle; the robot scans it and zaps it right
  (MANDATORY, a ding); the jolt shakes a paper party cone loose from above and it lands on the robot's antenna,
  crooked (a ploink, a sad party-horn toot). The robot does not react. Then animation v2 plays as it was;
- the cone stays on the robot in every shot;
- a loop tail (LOOP s): back on the opening shot, the training restarts: a rewind takes the cone back up out of frame
  and the slide back to MANDATROY, and the last drawing is frame 0.
Module protocol for engine_v / engine_hd: PANELS, DURATION, RAW_T, shake."""
import math
import inspect
import cairo
import kit
from kit import Ctx, INK, clamp, ease
import mf_anim as ma
import mf_sb as sb
import mf_set as ms
import mf_set_sheet as ss
import robot_mf as rm
import waiter_kit as w

OPEN, LOOP = 1.5, 0.8
D0 = ma.DURATION
DURATION = round(OPEN + D0 + LOOP, 3)
RAW_T = 0.0
CONE_COL, STRIPE = (0.95, 0.35, 0.55), (1.0, 0.85, 0.2)
LAND = (0.0, -44.0, 0.30)                  # head-local: the cone's base centre and its tilt when it has landed
TOP = (-60.0, -520.0, -2.2)                # where it falls from (above the frame)


# ---------------------------------------------------------------- the cone, in the robot's head frame
def cone(c, x, y, rot, s=1.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.new_path(); c.move_to(-23, 2); c.line_to(23, 2); c.line_to(4, -66); c.close_path()
    c.set_source_rgb(*CONE_COL); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(2.4); c.set_line_join(1); c.stroke()
    c.set_source_rgb(*STRIPE); c.set_line_width(5)
    for f in (0.28, 0.58):                                   # two stripes across the cone
        y0 = 2 - 68 * f; half = 23 * (1 - f)
        c.new_path(); c.move_to(-half + 2 + 4 * f, y0); c.line_to(half - 2 + 4 * f, y0); c.stroke()
    kit_dot = (1.0, 0.85, 0.2)
    c.new_path(); c.arc(4, -68, 7, 0, 2 * math.pi); c.set_source_rgb(*kit_dot); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(1.8); c.stroke()
    c.restore()


_SIG = inspect.signature(rm.robot)


def head_frame(c, args, kwargs, out):
    """Apply robot_mf.robot's head transform for this call (as robot_mf draws the head)."""
    b = _SIG.bind(*args, **kwargs); b.apply_defaults(); a = b.arguments
    x, feet, s, pose, side, wob = a["x"], a["feet"], a["s"], a["pose"], a["side"], a["wobble"]
    named = isinstance(pose, str)
    tilt = (w.POSES[pose] if named else pose)[0] + wob
    hdx = a["head_dx"] if a["head_dx"] is not None else (w.HEAD_DX.get(pose, 0) if named else 0)
    hrot = a["head_rot"] if a["head_rot"] is not None else (w.HEAD_ROT.get(pose, 0) if named else 0)
    hy = out["head"][1]
    c.translate(x, feet); c.scale(s * side, s); c.rotate(tilt)
    c.translate(hdx, (hy - feet) / s); c.rotate(hrot)


_robot_v2 = ma._robot0                                       # robot_mf.robot as animation v2 calls it
_rm_robot = rm.robot                                         # the module's own, restored after every panel


def robot_cone(k, *a, **kw):
    out = _robot_v2(k, *a, **kw)
    c = k.c
    c.save(); head_frame(c, (k,) + a, kw, out); cone(c, *LAND); c.restore()
    return out


# ---------------------------------------------------------------- the slide, with the typo
_slide0 = ms.slide
WORD = {"text": "MANDATORY", "squiggle": 0.0, "fixed": 0.0, "jolt": 0.0}


def slide3(k, x, y, wd, h, alpha=1.0):
    c = k.c
    c.save()
    if WORD["jolt"]:
        c.translate(x + wd / 2, y); c.rotate(WORD["jolt"]); c.translate(-(x + wd / 2), -y)
    _slide0(k, x, y, wd, h, alpha)
    if WORD["text"] != "MANDATORY" or WORD["fixed"]:          # repaint the title word
        c.save(); c.rectangle(x + 2, y + h * 0.27, wd - 4, h * 0.24); c.clip()
        c.set_source_rgb(0.99, 0.99, 0.98); c.paint()
        c.select_font_face("Lilita One", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        txt = WORD["text"]; c.set_font_size(h * 0.25)
        ref = c.text_extents("MANDATORY"); e = c.text_extents(txt)
        sc = min(1.0, wd * 0.84 / ref.x_advance)
        c.save(); c.translate(x + wd / 2, y + h * 0.46); c.scale(sc, 1)
        c.move_to(-e.x_advance / 2, 0); c.set_source_rgb(*ms.NAVY); c.show_text(txt)
        if WORD["squiggle"] > 0:                              # the spell-check squiggle, drawn left to right
            x0, x1 = -e.x_advance / 2, -e.x_advance / 2 + e.x_advance * WORD["squiggle"]
            c.set_source_rgb(0.88, 0.12, 0.12); c.set_line_width(3)
            c.new_path(); xx = x0
            c.move_to(xx, 8)
            while xx < x1:
                xx += 6; c.line_to(min(xx, x1), 8 + (5 if int((xx - x0) / 6) % 2 else 0))
            c.stroke()
        c.restore()
        if WORD["fixed"] > 0:                                  # a green flash on the corrected word
            c.set_source_rgba(0.25, 0.80, 0.35, 0.35 * WORD["fixed"]); c.paint()
        c.restore()
    c.restore()


# ---------------------------------------------------------------- the opening shot (cold open and loop tail)
def opening(k, tl, dur, cone_at=None, scan=False, zap=0.0, overlay=None):
    """The settled first shot of animation v2 (CAM1), robot beside the slide. cone_at: (x, y, rot) head-local,
    or None; zap: 0..1, a spark from the antenna to the slide."""
    c = k.c
    push = 1 + 0.03 * (tl / dur)
    c.save()
    c.translate(270, 480); c.scale(1 / push, 1 / push); c.translate(-270, -480)   # no engine push on this shot
    ms.with_cam(c, sb.CAM1)
    ms.slide = slide3
    try:
        ss.base(k)
    finally:
        ms.slide = _slide0
    out = rm.robot(k, sb.X["robot"], ms.FEET_BACK, 1.0, "stand", "scan" if scan else "eager",
                   look=(-0.9, -0.3) if scan else (0, 0), t=tl, seed=97)
    if zap > 0:
        _spark(k, out, zap)
    if cone_at is not None:
        c.save(); head_frame(c, (k, sb.X["robot"], ms.FEET_BACK, 1.0, "stand"), {}, out); cone(c, *cone_at); c.restore()
    c.restore()
    ma.vignette(c)


def _slide_pt():
    x, y, wd, h = ms.SCREEN
    return (x + wd * 0.8, y + h * 0.42)


def _spark(k, out, zap):
    """A zig-zag from the antenna ball to the slide's title word."""
    c = k.c
    c.save(); head_frame(c, (k, sb.X["robot"], ms.FEET_BACK, 1.0, "stand"), {}, out)
    p0 = c.user_to_device(0, -62); c.restore()
    p1 = c.user_to_device(*_slide_pt())
    c.save(); c.identity_matrix()
    n = 7; pts = []
    for i in range(n + 1):
        f = i / n
        px = p0[0] + (p1[0] - p0[0]) * f; py = p0[1] + (p1[1] - p0[1]) * f
        if 0 < i < n:
            px += (10 if i % 2 else -10); py += (8 if i % 2 else -8)
        pts.append((px, py))
    for col, lw in (((0.55, 0.95, 1.0), 9 * zap), ((1, 1, 1), 3.5 * zap)):
        c.new_path(); c.move_to(*pts[0])
        for q in pts[1:]:
            c.line_to(*q)
        c.set_source_rgba(*col, zap); c.set_line_width(lw); c.set_line_join(1); c.stroke()
    c.restore()


def fall_path(u):
    """u 0..1: from above the frame to the antenna, spinning, with a small bounce at the end."""
    e = u * u
    x = TOP[0] + (LAND[0] - TOP[0]) * e
    y = TOP[1] + (LAND[1] - TOP[1]) * e
    r = TOP[2] + (LAND[2] - TOP[2]) * ease(u)
    return (x, y, r)


def cold(k, t, tl):
    WORD.update(text="MANDATROY", squiggle=0.0, fixed=0.0, jolt=0.0)
    scan, zap, cone_at = False, 0.0, None
    if tl >= 0.15:
        WORD["squiggle"] = clamp((tl - 0.15) / 0.2)
    if 0.30 <= tl < 0.58:
        scan = True
    if 0.52 <= tl < 0.66:
        zap = 1.0 - abs(tl - 0.58) / 0.08
    if tl >= 0.58:
        WORD.update(text="MANDATORY", squiggle=0.0, fixed=clamp(1 - (tl - 0.58) / 0.35))
        WORD["jolt"] = 0.05 * math.exp(-(tl - 0.58) / 0.12) * math.cos((tl - 0.58) * 40)
    if 0.62 <= tl < 0.95:
        cone_at = fall_path((tl - 0.62) / 0.33)
    elif tl >= 0.95:                                          # the landing squash, then still
        b = max(0.0, 1 - (tl - 0.95) / 0.12)
        cone_at = (LAND[0], LAND[1] + 4 * b, LAND[2] + 0.12 * b * math.sin((tl - 0.95) * 50))
    try:
        opening(k, tl, OPEN, cone_at, scan, max(zap, 0.0))
    finally:
        WORD.update(text="MANDATORY", squiggle=0.0, fixed=0.0, jolt=0.0)


def rewind(k, t, tl):
    """The training restarts: a fast rewind, ending on frame 0 exactly."""
    if tl >= 0.62:                                            # frame 0, on the unboiled paper, without the engine push
        c = k.c; pe = 1 + 0.03 * (tl / LOOP)
        c.save(); c.translate(270, 480); c.scale(1 / pe, 1 / pe); c.translate(-270, -480)
        try:
            return cold(Ctx(c, 0), 0.0, 0.0)
        finally:
            c.restore()
    u = clamp((tl - 0.12) / 0.45)
    if u <= 0:
        WORD.update(text="MANDATORY"); cone_at = LAND
    else:
        cone_at = fall_path(1 - u)
        if u > 0.6:
            WORD.update(text="MANDATROY", squiggle=clamp((1 - u) / 0.4))
    try:
        opening(k, tl, LOOP, cone_at if cone_at[1] > -500 else None)
    finally:
        WORD.update(text="MANDATORY", squiggle=0.0)
    if u > 0:                                                 # rewind streaks
        c = k.c; c.save(); c.identity_matrix()
        r = (int(t * 30) * 7919) % 1000
        for i in range(6):
            yy = (r * (i + 3) * 37) % 1920 / 1920 * 960
            c.set_source_rgba(1, 1, 1, 0.20); c.rectangle(0, yy, 540, 3 + i % 3); c.fill()
        c.select_font_face("DejaVu Sans Mono", 0, 1); c.set_font_size(22)
        c.set_source_rgba(1, 1, 1, 0.85); c.move_to(30, 900); c.show_text("◀◀ RESTART TRAINING")
        c.restore()


def shifted(fn):
    def panel(k, t, tl):
        ma.RAW_T = RAW_T - OPEN
        ma._robot0 = robot_cone
        try:
            fn(k, t - OPEN, tl)
        finally:
            ma._robot0 = _robot_v2
            rm.robot = _rm_robot                              # mf_anim.wrap restores robot_mf.robot to _robot0
    panel.__name__ = getattr(fn, "__name__", "panel")
    return panel


def shake(t):
    return ma.shake(t - OPEN) if OPEN <= t < OPEN + D0 else 0


PANELS = ([(0.0, OPEN, cold)] + [(t0 + OPEN, t1 + OPEN, shifted(fn)) for t0, t1, fn in ma.PANELS] +
          [(OPEN + D0, DURATION, rewind)])
