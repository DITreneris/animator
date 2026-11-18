"""ANIMATION v5 of "Secret Santa" (18 Nov), the final polish. Wraps animation v4 (ss_anim4.py, kept and unchanged):
- the cold open plays 1.3x slower (1.3 s): the kiss, the THUNK and the barred kiss each get time to read; the rest of
  the film is v4's, 0.3 s later (every voice, lip shape, blink and breath keeps v4's place: v4's clock is passed on);
- a SOFIA name plate on the front of her desk, so on mute TO: SOFIA (heart) has a face;
- shot 6: Don's palm polishing his dome reads as vanity: a big four-pointed glint on the crown as the palm passes;
- shot 13: the robot's arm is drawn sharp, in its own white with ink, a joint and a cuff (it read as "a pipe");
- the robot's PERSONAL DATA DETECTED in light text (it was red on dark red); in the tags insert the stamp and APPROVED
  land under FROM: DON, not on it;
- a light camera: slow creeps on faces (Pam's melt, her hurt, her stare, the line-up), a small punch-in on each THUNK.
Sound: ss_sound_v5.py. Module protocol for engine_v / engine_hd: PANELS, DURATION, RAW_T, shake."""
import math
import kit
from kit import Ctx, INK
import ss_anim as A
import ss_anim4 as M4
import ss_sb as sb
import ss_set as S
import ss_timing as T
import props_ss as props
import robot_ss as rs
import robot_mf as rm
import waiter_kit as w

SLOW, SHIFT = 1.3, 0.3                      # the cold open (v4: 0..1 s) becomes 0..1.3 s; later shots move by SHIFT
DURATION = round(M4.DURATION + SHIFT, 3)
RAW_T = 0.0


def v4_time(t):
    return t / SLOW if t < SLOW else t - SHIFT


# ---------------------------------------------------------------- her name on the desk
_desk0 = S.desk


def desk(k):
    _desk0(k)
    c = k.c
    x0, x1 = S.DESK
    cx, cy = (x0 + x1) / 2 + 10, S.TABLE_TOP + 62
    kit.rect(k, cx - 52, cy - 16, 104, 32, (0.16, 0.17, 0.20), 990, shadow=False, lw=2)
    c.select_font_face("Inter", 0, 1); c.set_font_size(19); e = c.text_extents("SOFÍA")
    c.set_source_rgb(0.98, 0.95, 0.85); c.move_to(cx - e.x_advance / 2, cy + 7); c.show_text("SOFÍA")


S.desk = desk

# ---------------------------------------------------------------- PERSONAL DATA DETECTED in light text
_lines0 = rm._lines


def _lines(c, lines, col, ys, size):
    if lines and lines[0] == "PERSONAL DATA":
        col = (1.0, 0.93, 0.93)
    return _lines0(c, lines, col, ys, size)


rm._lines = _lines

# ---------------------------------------------------------------- the tags insert: stamp and APPROVED under the names
_card0 = M4.card


def card(k, x, y, s, approved_lift):
    _card0(k, x, y, s, None)
    if approved_lift is not None and approved_lift < 1:
        c = k.c
        c.save(); c.translate(x + 14 * s, y + 31 * s); c.rotate(-0.16); c.scale(s, s)
        c.set_source_rgb(*rs.GREEN); c.set_line_width(2.2); c.rectangle(-30, -8, 60, 15); c.stroke()
        c.select_font_face("Inter", 0, 1); c.set_font_size(10.5); e = c.text_extents("APPROVED")
        c.move_to(-e.x_advance / 2, 4); c.show_text("APPROVED")
        c.restore()


M4.card = card
_stamp0 = rs.stamp_prop


def _tags_insert(k, t, tl):
    def stamp(k2, x, y, *a, **kw):                    # the insert's stamp, moved down onto APPROVED
        return _stamp0(k2, x + 1, y + 11, *a, **kw)
    _il0 = rs.impact_lines
    rs.stamp_prop = stamp
    rs.impact_lines = lambda c, x, y, *a: _il0(c, x + 1, y + 11, *a)
    try:
        return M4.tags_insert(k, t, tl)
    finally:
        rs.stamp_prop, rs.impact_lines = _stamp0, _il0


def s15_new(k, t, tl):
    return _tags_insert(k, t, tl) if M4.I0 <= tl < M4.I1 else M4.s15_wide(k, t, tl)


# ---------------------------------------------------------------- shot 6: the glint on the dome
def s6_new(k, t, tl):
    sb.s6b(k, t, tl)
    if 0.75 < tl < 1.75:                              # the palm passes; the crown flashes behind it
        a = 1.0 - abs(((tl - 0.75) % 0.5) - 0.25) * 2.4
        def d():
            props.sparkle(k.c, 52, 322 + sb.ds.HY * 0.85 - 30, 13 * max(0.35, a), max(0.0, a))
        sb.screen(k, tl, "s6b", d)


# ---------------------------------------------------------------- shot 13: the robot's arm, sharp
def s13_new(k, t, tl):
    _soft0 = props.soft

    def soft(c, fn, r):                              # only this shot's foreground (the arm) is drawn sharp
        if getattr(fn, "__name__", "") == "fg":
            fn2 = fn
            c.save()
            fn2(c)
            c.restore()
            return
        return _soft0(c, fn, r)
    props.soft = soft
    try:
        sb.s13b(k, t, tl)
    finally:
        props.soft = _soft0
    # a cuff and an elbow joint over the sharp arm, in the robot's white
    def d():
        c = k.c
        kit.ellipse(Ctx(c, 0), 14, 34, 7, 7, w.BODY, 44, shadow=False, lw=2)
    sb.screen(k, tl, "s13b", d)


# ---------------------------------------------------------------- a light camera
HITS = {"s11b": 0.33, "s12b": 0.4, "s13b": 0.95}


def move(name, tl, d):
    """(cx, cy, z) in 540 x 960 screen space."""
    e = sb.ease(min(1.0, tl / max(d, 1e-6)))
    if name in HITS and tl >= HITS[name]:
        return 270, 520, 1 + 0.05 * (1 - sb.ease(min(1.0, (tl - HITS[name]) / 0.3)))
    return {"s4b": (300, 420, 1 + 0.04 * e) if not (M4.G0 <= tl < M4.G1) else (270, 480, 1.0),
            "s5b": (270, 420, 1 + 0.03 * e),
            "s7b": (220, 420, 1 + 0.06 * e),
            "s14b": (270, 400, 1 + 0.06 * e),
            "s15b": (270, 480, 1 + 0.03 * e) if not (M4.I0 <= tl < M4.I1) else (270, 480, 1.0)}.get(name, (270, 480, 1.0))


def cam(name, fn):
    def g(k, t, tl):
        cx, cy, z = move(name, tl, sb.PANEL_DUR.get(name, 1.0))
        if z == 1.0:
            return fn(k, t, tl)
        c = k.c
        c.save(); c.translate(cx, cy); c.scale(z, z); c.translate(-cx, -cy)
        try:
            return fn(k, t, tl)
        finally:
            c.restore()
    g.__name__ = name
    return g


# ---------------------------------------------------------------- the panels: v4's, retimed, with the new shots
_NEW = {"s6b": s6_new, "s13b": s13_new, "s15b": s15_new}
_rows = []
for i, (a0, a1, fn, t0, t1, ks) in enumerate(M4._rows):
    name = fn.__name__
    if name in _NEW:
        fn = _NEW[name]
    fn = cam(name, fn) if name not in ("s1", "s16b") else fn
    if i == 0:                                        # the cold open slowed, the pull-out and the rest moved
        ks = [(0.0, 0.0), (1.0, 1.0 * SLOW)] + [(x, y + SHIFT) for x, y in ks if x > 1.0]
        a1 = a1 + SHIFT
    else:
        a0, a1 = a0 + SHIFT, a1 + SHIFT
    _rows.append((a0, a1, fn, t0, t1, ks))


def _wrap(a0, a1, fn, t0, t1, ks):
    """ss_anim._wrap, but the clock that lips, blinks, breaths and timed bubbles read is v4's."""
    def g(k, t, tl):
        A.CUR[0] = v4_time(t)
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


PANELS = [(a0, a1, _wrap(a0, a1, fn, t0, t1, ks)) for a0, a1, fn, t0, t1, ks in _rows]


def shake(t):
    return A.shake(t)
