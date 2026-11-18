"""ANIMATION v6 of "Secret Santa" (18 Nov): Pam kisses the camera. Wraps animation v5 (ss_anim5.py, kept and
unchanged) and replaces only the cold open (its first second of storyboard time, 1.3 s on screen):
- frame 0 as v5 (the lipstick over the fresh blank tag, the loop's join);
- 0.06-0.24: Pam swoops in to the lens, her face filling the frame (shoulders below: she leans in, nothing falls);
  0.24-0.32 her puckered lips press the glass; 0.32-0.46 she pulls back down and out of frame;
- a rose lip print stays on the glass, over the shot; 0.66: THUNK, the robot's stamp hits the glass itself and a
  black bar covers the print (the screen shakes); the bar and print stay until the cut to the wide shot;
- 0.72: she uncaps the lipstick, as before.
The sound is v5's (ss_mix_v5.wav): its whoosh, kiss, whoosh and THUNK already sit on these beats.
Module protocol for engine_v / engine_hd: PANELS, DURATION, RAW_T, shake."""
import cairo
import kit
from kit import Ctx, INK
import ss_anim5 as M5
import ss_anim4 as M4
import ss_anim3 as M3
import ss_sb as sb
import ss_motion as mo
import props_ss as props
import robot_ss as rs

DURATION = M5.DURATION
RAW_T = 0.0
T_IN, T_PRESS, T_OFF, T_GONE, T_HIT, T_UNCAP = 0.06, 0.24, 0.32, 0.46, 0.66, 0.72
KX, KY = 49, 92                                       # where her lips meet the glass (98 x 174 units)
ROSE = (0.80, 0.42, 0.48)
_PH = [None]


def _head():
    if _PH[0] is None:
        _PH[0] = sb.ps.pam(Ctx(cairo.Context(cairo.ImageSurface(cairo.FORMAT_ARGB32, 4, 4)), 0), 0, 0, 1.0,
                           "stand", "neutral", look=(0, 1))["head"]
    return _PH[0]


def pam_at_lens(k, s, mx, my, pucker):
    """Pam, whole, scaled s, with her mouth at (mx, my): her shoulders run off the bottom of the frame."""
    c = k.c
    hx, hy = _head()
    c.save(); c.translate(mx, my); c.scale(s, s); c.translate(-hx, -(hy + 32))
    kk = Ctx(c, 0)
    sb.ps.pam(kk, 0, 0, 1.0, "stand", "hopeful", look=(0, 0.2))
    if pucker:
        c.save(); c.translate(hx, hy + 32); c.scale(9, 7); c.arc(0, 0, 1, 0, 6.2832); c.restore()
        c.set_source_rgb(*ROSE); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1.6); c.stroke()
        c.set_line_width(1.0); c.move_to(hx - 5, hy + 32); c.line_to(hx + 5, hy + 32); c.stroke()
    c.restore()


def cold(k, t, tl):
    if tl < 1 / 12:
        sb.screen(Ctx(k.c, 0), tl, "s1", lambda: M3.frame0(Ctx(k.c, 0)))
        return

    def d():
        c = k.c
        dx, dy = mo.shake(tl, T_HIT, 2.2, seed=21)
        c.save(); c.translate(dx, dy)
        M3._bg(k)
        M3.tag(k, M3.TAG[0], M3.TAG[1])
        sb.sss.pam_hand(k, sb.ease((tl - T_UNCAP) / 0.3))
        if T_IN < tl < T_GONE:                         # she leans in to the lens, kisses it, and drops back
            if tl < T_PRESS:
                u = sb.ease((tl - T_IN) / (T_PRESS - T_IN))
                s, my = 0.5 + 1.6 * u, 200 - (200 - KY) * u
            elif tl < T_OFF:
                s, my = 2.1 + 0.08 * ((tl - T_PRESS) / (T_OFF - T_PRESS)), KY
            else:
                u = sb.ease((tl - T_OFF) / (T_GONE - T_OFF))
                s, my = 2.18 - 1.2 * u, KY + 160 * u
            pam_at_lens(k, s, KX, my, pucker=tl >= T_PRESS - 0.04 and tl < T_OFF + 0.04)
        c.restore()
        if tl >= T_PRESS + 0.02:                       # the print on the glass, over everything
            c.save(); c.translate(KX, KY); c.rotate(-0.08)
            props.kiss(k, 0, 0, 1.25, ang=0.0)
            c.restore()
        lift = mo.stamp_track(tl, T_HIT, 120, up_after=0.2)
        if tl >= T_HIT:                                # the bar on the glass
            c.save(); c.translate(KX, KY); c.rotate(-0.08)
            c.rectangle(-21, -10, 42, 20); c.set_source_rgb(0.08, 0.08, 0.10); c.fill_preserve()
            c.set_source_rgb(0.95, 0.93, 0.88); c.set_line_width(1.6); c.stroke()
            c.restore()
        if tl > T_HIT - 0.16 and lift < 119:          # the robot's stamp, from the top, on the glass
            rs.stamp_prop(k, KX, KY - lift + 6, 1.3, "down" if lift < 1 else "up", 0.0, 7)
            if T_HIT <= tl < T_HIT + 0.2:
                rs.impact_lines(c, KX, KY, 2, 1.0)
    sb.screen(k, tl, "s1", d)


def s1_new(k, t, tl):
    return cold(k, t, tl) if tl < 1.0 else M4.s1_rest(k, t, tl)


s1_new.__name__ = "s1"
_rows = list(M5._rows)
_a0, _a1, _f, _t0, _t1, _ks = _rows[0]
_rows[0] = (_a0, _a1, s1_new, _t0, _t1, _ks)
PANELS = [(a0, a1, M5._wrap(a0, a1, fn, t0, t1, ks)) for a0, a1, fn, t0, t1, ks in _rows]


def shake(t):
    return M5.shake(t)
