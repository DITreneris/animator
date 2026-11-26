"""ONE STAR v21 (26 Nov, the review of v20: 8.7/10, "three last corrections only", then QA and publish):
- P0 5.2 the pen in a real tripod: the index finger along its top to near the tip (a nail on it), the thumb on its
  lower side, the middle finger under it; the tip ON the last stroke written (v20: a fist round the pen);
- P1 5.3 SAVE blue and active before the tap (grey read "disabled"), green SAVED after;
- P1 4.2/4.3w the other bays a further 25 % down, a soft light rim round bay 7.
Nothing else changes. Opt-in through install()."""
import cairo
import cs_os20 as g20
import cs_scene4 as s4
import cs_scene5 as s5
import cs_grips as g


def plan_surface(state, flip=None):
    sf = g20._OLD_PLAN[0](state, flip)
    c = cairo.Context(sf)
    c.set_operator(cairo.OPERATOR_ATOP)
    c.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
    c.rectangle(0, 0, 540, 960)
    for x, y, w, h in (g20.BAY7, g20.TITLE):
        c.rectangle(x, y, w, h)
    c.set_source_rgba(0.16, 0.32, 0.72, 0.38); c.fill_preserve()                  # v20's tone toward the plan's blue
    c.set_source_rgba(0.04, 0.06, 0.14, 0.25); c.fill()                            # v21: and 25 % down
    c.set_operator(cairo.OPERATOR_OVER)                                            # a soft light rim round bay 7
    x, y, w, h = g20.BAY7
    for i, a in ((10, 0.10), (6, 0.18), (3, 0.30)):
        c.set_source_rgba(1, 0.97, 0.80, a); c.set_line_width(i); c.rectangle(x - 2, y - 2, w + 4, h + 4); c.stroke()
    return sf


def install():
    g20.TRIPOD[0] = True
    g.TIP52[0] = True
    s5.SAVE_BLUE[0] = True
    s4._plan_surface = plan_surface
