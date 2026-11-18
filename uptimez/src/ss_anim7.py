"""ANIMATION v7 of "Secret Santa" (18 Nov), the final: v6 (ss_anim6.py, kept) with Sofia taken out of the cold open's
close-up. Her big, barely soft face behind Pam's hand was the largest face in frame 0, looked into the lens and
competed with Pam's kiss to the camera ("whose hand is it?"). Now the close-up's background is the office wall with the
fairy lights soft and warm behind; the only face in the first second is Pam's. The end shot uses the same background,
so the last frame is still frame 0. Everything else is v6's (and the sound is v5's).
Module protocol for engine_v / engine_hd: PANELS, DURATION, RAW_T, shake."""
import math
import kit
import ss_anim3 as M3
import ss_anim6 as M6
import props_ss as props

DURATION = M6.DURATION
RAW_T = 0.0
WARM = [(1.0, 0.82, 0.38), (1.0, 0.55, 0.45), (0.98, 0.92, 0.60), (0.55, 0.85, 0.55)]
BOKEH = [(12, 22, 7), (34, 14, 9), (58, 26, 6), (82, 12, 8), (93, 40, 6), (6, 58, 8), (70, 52, 5), (44, 44, 4),
         (22, 84, 6), (88, 76, 7)]


def _bg(k):
    """The wall behind the close-up: warm paper, a hint of the paper chain, the fairy lights out of focus."""
    c = k.c
    c.set_source_rgb(*kit.WALL); c.rectangle(-5, -5, 108, 184); c.fill()
    g = __import__("cairo").LinearGradient(0, 0, 0, 174)
    g.add_color_stop_rgba(0, 0.0, 0.0, 0.0, 0.0); g.add_color_stop_rgba(1, 0.35, 0.22, 0.10, 0.18)
    c.set_source(g); c.rectangle(-5, -5, 108, 184); c.fill()

    def lights(lc):
        for i, (x, y, r) in enumerate(BOKEH):
            col = WARM[i % len(WARM)]
            lc.set_source_rgba(*col, 0.30); lc.arc(x, y, r * 1.8, 0, 2 * math.pi); lc.fill()
            lc.set_source_rgba(*col, 0.85); lc.arc(x, y, r, 0, 2 * math.pi); lc.fill()
        lc.set_source_rgba(0.80, 0.14, 0.16, 0.35); lc.set_line_width(4)      # the paper chain, soft, high up
        lc.move_to(-5, 4); lc.curve_to(30, 16, 64, 16, 103, 2); lc.stroke()
    props.soft(c, lights, 2.6)


M3._bg = _bg                                       # frame 0, the cold open and the end shot share it
PANELS = M6.PANELS


def shake(t):
    return M6.shake(t)
