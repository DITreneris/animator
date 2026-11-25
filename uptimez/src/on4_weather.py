"""OFFICE NOIR 4: the weather and the film's grain (24 Nov, Tomas's picks, after Office Noir 2 and 3).
  rain    on every street shot: on2_motion.rain's slanted streaks (Office Noir 2), rings on the ground (its drops' drawing)
  wet     the cobbles and the road shine: the lit wall's light down the lane, glints on the stones (drawn under the cast)
  grain   in the dream only, light, changing on twos, the key red left clean (light_on3._grain, Office Noir 3)
All of it off unless ON[0]; nothing here draws when it is off."""
import math
import random
import cairo
import on4_scenes as sc
import on2_motion as o2
import light_on3 as l3

ON = [False]
T = [0.0]                                                    # the film's time for the drawing being made (on4_text sets it)
RAMP = [1.0]                                                 # 0 on frame 0 (the last drawing has none): comes in over the first 0.6 s
STREET = ("1.1", "1.2", "1.3", "1.4", "2.1", "2.2", "2.3", "2.4", "3.1", "3.2", "3.3", "3.3b", "3.4", "3.5", "3.6", "4.1")
GROUND = {"1.1": (100, 420, 640, 940), "1.2": (100, 420, 640, 940), "1.3": (60, 480, 720, 940), "1.4": (100, 420, 640, 940),
          "2.1": (170, 420, 600, 940), "3.1": (0, 540, 500, 700), "3.2": (0, 540, 500, 700), "3.3": (0, 540, 500, 700),
          "3.3b": (0, 540, 500, 700), "3.4": (0, 540, 500, 700), "3.5": (0, 540, 500, 700), "4.1": (0, 540, 720, 940)}
GRAIN_A = 6.0


def glints(c, x0, x1, y0, y1, n, t, seed=1, a=0.55):
    """wet stones: short level dashes of light, each on for a few drawings"""
    d = int(t * 6)
    c.set_line_cap(1)
    for i in range(n):
        r = random.Random(seed * 131 + i * 17 + (d + i) // 5)
        x = r.uniform(x0, x1); y = r.uniform(y0, y1); g = 0.5 + (y - y0) / max(1.0, y1 - y0)
        c.set_source_rgba(1, 1, 0.97, a * r.uniform(0.4, 1.0)); c.set_line_width(2.0 * g)
        w = r.uniform(5, 14) * g; c.move_to(x - w, y); c.line_to(x + w, y); c.stroke()
    c.set_line_cap(0)


def wet(k, name):
    """under the cast, in the location's own units"""
    c = k.c; t = T[0]
    if name in ("A", "A_tail"):                              # the lit wall at the lane's end, down the wet cobbles
        g = cairo.LinearGradient(0, 548, 0, 900)
        g.add_color_stop_rgba(0, 1, 1, 0.96, 0.36); g.add_color_stop_rgba(1, 1, 1, 0.96, 0.0)
        c.new_path(); c.move_to(205, 548); c.line_to(320, 548); c.line_to(400, 900); c.line_to(150, 900); c.close_path(); c.set_source(g); c.fill()
        glints(c, 150, 420, 570, 930, 30, t, 3)
    elif name in ("B_high", "B_escape", "above"):
        glints(c, 180, 420, 600, 930, 20, t, 5)
    elif name.startswith("C"):
        glints(c, -200, 900, 610, 730, 40, t, 7, 0.5)
    elif name == "front":
        glints(c, 0, 540, 720, 930, 24, t, 9)


def rings(c, shot, t):
    if shot not in GROUND:
        return
    x0, x1, y0, y1 = GROUND[shot]
    d = int(round(t * 12))
    for i in range(12):
        per = 7 + (i * 5) % 6
        cyc, age = divmod(d + i * 3, per)
        if age > 3:
            continue
        a = age / 4.0
        x = x0 + (i * 131 + cyc * 197) % max(1, int(x1 - x0)); y = y0 + (i * 71 + cyc * 113) % max(1, int(y1 - y0))
        g = 0.6 + 0.8 * (y - y0) / float(y1 - y0)
        c.set_source_rgba(1, 1, 1, 0.50 * (1 - a) * RAMP[0]); c.set_line_width(1.5 * g)
        c.save(); c.translate(x, y); c.scale((5 + 16 * a) * g, (5 + 16 * a) * g * 0.3); c.new_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.stroke()


STRENGTH = [0.75]                                            # light_on3.auto at full strength left this film at 0.22 mean (Office Noir 1: 0.26, 2: 0.28)
LIGHT = [False]                                              # the repo's solved light (light_on3.auto, Office Noir 3 after Tomas asked why 1 and 2 looked better): a pool round the measured heads, the rest sinks, faces lifted from above, its vignette and grain


def post(s, shot, t, heads=()):
    """over the finished drawing, under the words"""
    if LIGHT[0] and not shot.startswith(("7.", "8.")) and RAMP[0] > 0:
        hs = [(h[0], h[1], h[2] / 50.0) for h in heads]
        import numpy as np
        s.flush(); src = np.frombuffer(bytes(s.get_data()), np.uint8).reshape(960, s.get_stride() // 4, 4)[:, :540].copy()
        lit = l3.auto(s, hs, RAMP[0] * STRENGTH[0], int(t * 12), max([h[2] for h in heads] or [0]) > 110, glow=True, pool=True)
        c0 = cairo.Context(s); c0.set_source_surface(lit, 0, 0); c0.paint(); s.flush()
        buf = np.frombuffer(s.get_data(), np.uint8).reshape(960, s.get_stride() // 4, 4)
        red = (src[:, :, 2].astype(np.int16) - src[:, :, 1]) > 60                         # the key red (the heart, the neon, the fire) keeps its own light: the pool does not dim it
        buf[:, :540][red] = src[red]; s.mark_dirty()
    if not ON[0]:
        return s
    if shot in STREET and RAMP[0] > 0:
        c = cairo.Context(s)
        rings(c, shot, t)
        for dt_, dx_ in ((0.0, 0), (0.37, 61), (0.71, -47)):      # three layers of Office Noir 2's streaks: one was too thin on this film's light walls
            c.push_group(); c.translate(dx_, 0); o2.rain(sc.Ctx(c, 0), t + dt_); c.translate(-dx_, 0); c.pop_group_to_source(); c.paint_with_alpha(RAMP[0])
    if not shot.startswith(("7.", "8.")) and RAMP[0] > 0 and not LIGHT[0]:   # with LIGHT the grain is light_on3's own
        l3._grain(s, GRAIN_A * RAMP[0], int(t * 12))
    return s


_done = [False]


def install():
    if _done[0]:
        return
    _done[0] = True
    loc0 = sc._loc
    def _loc(k, name):
        out = loc0(k, name)
        if ON[0] and isinstance(name, str):
            wet(k, name)
        return out
    sc._loc = _loc
