"""ANIMATION v3 of "Secret Santa" (18 Nov): the joke at 0:01 and a true loop. Wraps animation v2 (ss_anim.py, kept
and unchanged) and replaces only the first second of shot 1 and the last drawings of shot 16:
- frame 0 is the ECU of the film's end: Pam's hand with the capped lipstick, Sofia soft behind, and the fresh blank
  tag she has just slid in (v2 ended on it, but v2's frame 0 had no tag, so the loop jumped);
- 0.08 s: the tag lifts out of the top of the frame (to her lips); 0.30 s: it drops back with her kiss on it;
  0.55 s: THUNK, the robot's stamp comes down from the top and bars the kiss. The episode's own mechanism, readable
  on mute, before a word is said; and the loop now says "again";
- 0.62-0.95 s she uncaps the lipstick, as v2 did, and the film goes on as v2 (the pull-out at 1.0 s, the whisper);
- shot 16: the fresh tag slides in and settles where frame 0 has it; the last drawings are unboiled, so the last
  frame is frame 0.
Sound: ss_sound_v3.py (v2's mix with the lift whoosh, the kiss, the THUNK, and the cap pop moved to the uncap).
Module protocol for engine_v / engine_hd: PANELS, DURATION, RAW_T, shake."""
import kit
from kit import Ctx
import ss_anim as A
import ss_sb as sb
import ss_motion as mo
import pam_sheet_ss as pss
import props_ss as props
import robot_ss as rs
import sofia_ss

DURATION = A.DURATION
RAW_T = 0.0
TAG = (54, 122, 1.0, 0.06)                 # where the fresh tag rests (v2 ended at x 62: kiss and bar cut by the edge)
T_UP, T_DOWN, T_HIT, T_UNCAP = 0.08, 0.30, 0.55, 0.62


def _bg(k):
    c = k.c
    c.set_source_rgb(*kit.WALL); c.rectangle(0, 0, 98, 174); c.fill()

    def bg(lc):
        sofia_ss.sofia(Ctx(lc, 0),                          # unproxied: no breath or blink, the same every loop
                       98 * 0.40, 174 * 0.34 - sb.SHY, 1.0, "stand", "neutral", look=(-0.6, 0.1),
                    lag=(3, 0), badge=False, sparkle=0.0)
    props.soft(c, bg, 1.5)


def tag(k, x, y, kissed=False, barred=False):
    s, rot = TAG[2], TAG[3]
    sb.tag2(k, x, y, s, blank=True, rot=rot)
    if kissed and not barred:
        props.kiss(k, x + 23 * s, y + 10.5 * s, 0.26 * sb.KISS * s, ang=-0.12 + rot)
    if barred:                                   # the kiss bar of the climax (storyboard v2's bigger kiss)
        c = k.c
        c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
        c.rectangle(13.5, 3.5, 19, 14); c.set_source_rgb(0.08, 0.08, 0.10); c.fill_preserve()
        c.set_source_rgb(*pss.CREAM); c.set_line_width(1.4); c.stroke()
        c.restore()


def frame0(k):
    _bg(k)
    tag(k, TAG[0], TAG[1])
    sb.sss.pam_hand(k, 0.0)


def cold(k, t, tl):
    """0..1 s of shot 1: the kiss, barred."""
    if tl < 1 / 12:                              # frame 0, unboiled
        sb.screen(Ctx(k.c, 0), tl, "s1", lambda: frame0(Ctx(k.c, 0)))
        return

    def d():
        c = k.c
        _bg(k)
        dx, dy = mo.shake(tl, T_HIT, 1.4, seed=21)
        c.save(); c.translate(dx, dy)
        x, y = TAG[0], TAG[1]
        if tl < T_DOWN:                          # up and out of the top: to her lips
            y = TAG[1] - 200 * sb.ease(min(1.0, (tl - T_UP) / 0.16)) if tl > T_UP else TAG[1]
        elif tl < T_DOWN + 0.14:                 # and back down, kissed
            y = TAG[1] - 200 * (1 - sb.ease((tl - T_DOWN) / 0.14))
        tag(k, x, y, kissed=tl >= T_DOWN, barred=tl >= T_HIT)
        lift = mo.stamp_track(tl, T_HIT, 70, up_after=0.2)
        if tl > T_HIT - 0.25 and lift < 69:     # the robot's stamp, from the top
            bx, by = x + 23 * TAG[2], y + 10.5 * TAG[2]
            rs.stamp_prop(k, bx, by - lift - 3, 0.6, "down" if lift < 1 else "up", 0.0, 7)
            if T_HIT <= tl < T_HIT + 0.18:
                rs.impact_lines(c, bx, by, 1, 0.6)
        c.restore()
        sb.sss.pam_hand(k, sb.ease((tl - T_UNCAP) / 0.33))
    sb.screen(k, tl, "s1", d)


def end(k, t, tl):
    """Shot 16 as v2, but the tag settles exactly where frame 0 has it, and the last drawings are unboiled."""
    d_ = sb.PANEL_DUR.get("s16b", 1.0)
    kk = Ctx(k.c, 0) if tl > 0.55 else k

    def d():
        _bg(kk)
        tag(kk, sb.lerp(130, TAG[0], sb.ease(min(1.0, tl / 0.5))), TAG[1])
        sb.sss.pam_hand(kk, 0.0)
    sb.screen(kk, tl, "s16b", d)


def _with(fn_v2, new, cond):
    def g(k, t, tl):
        return new(k, t, tl) if cond(tl) else fn_v2(k, t, tl)
    g.__name__ = fn_v2.__name__
    return g


_rows = list(A.TIMED)
_a0, _a1, _f, _t0, _t1, _ks = _rows[0]
_rows[0] = (_a0, _a1, _with(_f, cold, lambda tl: tl < 1.0), _t0, _t1, _ks)
_a0, _a1, _f, _t0, _t1, _ks = _rows[-1]
_rows[-1] = (_a0, _a1, _with(_f, end, lambda tl: True), _t0, _t1, _ks)
PANELS = [(a0, a1, A._wrap(a0, a1, fn, t0, t1, ks)) for a0, a1, fn, t0, t1, ks in _rows]


def shake(t):
    return A.shake(t)
