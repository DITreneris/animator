"""OFFICE NOIR 4: the awake props, v2 (23 Nov; v1 pinned as on4_props_v1.py). v2 after the props review: Sofia's mug is
its own object (tall, black, a lipstick print on the OUTSIDE of the rim) so the eighth reads without counting; the row is
laid out from its last place back, so the eighth sits clear of the button rail; 8.2 is the set itself through a camera
that puts the lamp's head on frame 0's streetlamp (the counter, the monitor, the cups under the rota in frame);
INTERNAL MAIL bigger. v1: Stage 3, script v4 beats 7-8 (the front desk set, zone C, morning, colour).
Opt-in: nothing in fs_set4.py changes; a shot draws these through its own hooks, as Daddy's Home's props were (lesson 108).

  counter_lamp(k, x, base, s, on)   the loop's join (8.2-8.3): a small lamp on the counter built like frame 0's streetlamp
                                    (a post, the same curved bracket, the same hanging head, on4_street.lamp_head), so the cut
                                    from it to the streetlamp is a match, not a jump.
  cup(k, x, base, s, lipstick)      an empty white cup; Sofia's mug has a lipstick print on its rim (the eighth cup, the loop's
                                    change: eight where there were seven, lesson 183).
  cups(k, x0, base, s, n, step)     the row along the counter's front edge.
  envelope(k, x, y, s, ang, open_)  INTERNAL MAIL: the string-and-button envelope in the dream envelope's warm tone (the twin),
                                    its routing grid, the last line PAM in blue pen.
  rota(k, x, y, s, ang)             one sheet: COFFEE ROTA, MON to SUN, PAM on every line in big red letters (lesson 111:
                                    the thing that carries the joke reads at 270 px).
Positions on the set (world x, y): LAMP, CUPS below; the coffee machine stays at dh_props' 770, F-166."""
import math
import cairo
import kit
from kit import INK, cut
import on4_street as st

F = 800
LAMP = (668, F - 162, 1.0)                  # on the counter between Pam's monitor and the candy; its head hangs left
CUPS = (676, F - 150, 0.50, 7, 18)          # x0, base, scale, n, step: along the counter's front edge (v2: 806, the
                                            # eighth, ends at frame x ~433 in S6, clear of the rail at 470)
ENV = (0.93, 0.82, 0.58)                    # the dream envelope's warm tone (on4_cast.envelope)
ENV_D = (0.74, 0.58, 0.34)
PAPER = (0.99, 0.99, 0.97)
RED = (0.86, 0.12, 0.16)
PEN = (0.12, 0.22, 0.62)
BRASS = (0.72, 0.58, 0.30)


def _rr(c, x, y, w, h, r):
    c.new_path(); c.arc(x + r, y + r, r, math.pi, 1.5 * math.pi); c.arc(x + w - r, y + r, r, 1.5 * math.pi, 2 * math.pi)
    c.arc(x + w - r, y + h - r, r, 0, 0.5 * math.pi); c.arc(x + r, y + h - r, r, 0.5 * math.pi, math.pi); c.close_path()


def _fs(c, col, lw=2.0):
    c.set_source_rgb(*col); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(lw); c.stroke()


def counter_lamp(k, x, base, s=1.0, on=True):
    """(x, base): the middle of its foot on the counter top. The head hangs at (x - 40s, base - 90s)."""
    c = k.c
    c.save(); c.translate(x, base); c.scale(s, s)
    c.save(); c.scale(1, 0.32); c.new_path(); c.arc(0, 0, 18, 0, 2 * math.pi); c.restore(); _fs(c, INK, 1.6)   # the foot
    c.set_source_rgb(*INK); c.set_line_width(4); c.move_to(0, 0); c.line_to(0, -96); c.stroke()             # the post
    c.set_line_width(3); c.move_to(0, -96); c.curve_to(-14, -110, -32, -108, -40, -92); c.stroke()             # the bracket,
    c.restore()                                                                         # in from the right, as frame 0's
    hx, hy = x - 40 * s, base - 90 * s
    if on:
        st.lamp_head(k, hx, hy, 0.62 * s)
    else:
        st.poly(k, [(hx - 9 * s, hy - 6 * s), (hx + 9 * s, hy - 6 * s), (hx + 14 * s, hy + 4 * s), (hx - 14 * s, hy + 4 * s)], INK, 1.4)
    return hx, hy


def cup(k, x, base, s=1.0, lipstick=False):
    c = k.c
    c.save(); c.translate(x, base); c.scale(s, s)
    c.save(); c.scale(1, 0.3); c.new_path(); c.arc(0, 0, 16, 0, 2 * math.pi); c.restore()
    c.set_source_rgba(0, 0, 0, 0.16); c.fill()
    c.new_path(); c.arc(13, -14, 8, -math.pi / 2, math.pi / 2); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    c.new_path(); c.arc(13, -14, 8, -math.pi / 2, math.pi / 2); c.set_source_rgb(*PAPER); c.set_line_width(3); c.stroke()
    c.new_path(); c.move_to(-13, -28); c.line_to(13, -28); c.line_to(10, 0); c.line_to(-10, 0); c.close_path(); _fs(c, PAPER, 1.8)
    c.save(); c.translate(0, -28); c.scale(13, 3.4); c.new_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
    _fs(c, (0.62, 0.48, 0.36), 1.4)                                                                          # empty: a dry ring
    if lipstick:
        c.set_source_rgb(*RED)
        for dx, w in ((-5, 5.0), (2, 5.5)):
            c.save(); c.translate(dx, -25.5); c.scale(w, 2.8); c.new_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
    c.restore()


def cups(k, x0=None, base=None, s=None, n=None, step=None, eighth=False):
    X0, B, S, N, ST = CUPS
    x0, base, s, n, step = (x0 or X0), (base or B), (s or S), (n or N), (step or ST)
    for i in range(n):
        cup(k, x0 + i * step, base + (i % 2) * 2, s)
    if eighth:
        sofia_mug(k, x0 + n * step + 4 * s / 0.5, base + 1, s)


def sofia_mug(k, x, base, s=1.0):
    """Hers, not one of the seven: taller, black, a red lipstick print on the outside of the rim, off-centre."""
    c = k.c
    c.save(); c.translate(x, base); c.scale(s, s)
    c.save(); c.scale(1, 0.3); c.new_path(); c.arc(0, 0, 17, 0, 2 * math.pi); c.restore()
    c.set_source_rgba(0, 0, 0, 0.18); c.fill()
    c.new_path(); c.arc(15, -22, 10, -math.pi / 2, math.pi / 2); c.set_source_rgb(*INK); c.set_line_width(7); c.stroke()
    c.new_path(); c.arc(15, -22, 10, -math.pi / 2, math.pi / 2); c.set_source_rgb(0.16, 0.16, 0.18); c.set_line_width(4); c.stroke()
    _rr(c, -14, -44, 28, 44, 4); _fs(c, (0.16, 0.16, 0.18), 2.0)
    c.save(); c.translate(0, -44); c.scale(14, 3.4); c.new_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
    _fs(c, (0.10, 0.10, 0.11), 1.4)
    c.save(); c.translate(-5, -37); c.rotate(-0.18); c.scale(1.15, 1.15)                    # the kiss: two lips, outside
    c.set_source_rgb(*RED)
    c.new_path(); c.move_to(-8, 0); c.curve_to(-6, -5, -2, -5, 0, -2.5); c.curve_to(2, -5, 6, -5, 8, 0)
    c.curve_to(4, 1.2, -4, 1.2, -8, 0); c.close_path(); c.fill()                                   # the upper lip
    c.new_path(); c.move_to(-7.5, 1.4); c.curve_to(-4, 2.6, 4, 2.6, 7.5, 1.4); c.curve_to(5, 6.5, -5, 6.5, -7.5, 1.4)
    c.close_path(); c.fill()                                                                       # the lower lip
    c.restore()
    c.restore()


def envelope(k, x, y, s=1.0, ang=0.0, open_=False, sheet=0.0):
    """(x, y): its middle. 160 x 220 at s=1, portrait. sheet: 0..1, the rota pulled up out of it."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    if sheet > 0:
        rota(k, 0, -sheet * 150, 0.62, 0.0)
    cut(k, [(-80, -110), (80, -110), (80, 110), (-80, 110)], ENV, shadow=False, lw=2.2)
    if open_ or sheet > 0:
        c.set_source_rgb(*ENV_D); c.rectangle(-80, -110, 160, 8); c.fill()
    c.set_source_rgb(*ENV_D); c.set_line_width(1.4)                                                         # the flap
    c.move_to(-80, -76); c.line_to(80, -76); c.stroke()
    kit.text(k, "INTERNAL MAIL", 0, -90, 21, (0.42, 0.28, 0.14), bold=True)
    c.new_path(); c.arc(0, -66, 6, 0, 2 * math.pi); _fs(c, ENV_D, 1.2)                                       # button,
    c.new_path(); c.arc(0, -46, 6, 0, 2 * math.pi); _fs(c, ENV_D, 1.2)                                       # button
    c.set_source_rgb(0.30, 0.22, 0.14); c.set_line_width(1.2)                                                # the string
    c.move_to(0, -66); c.curve_to(12, -60, 12, -50, 0, -46); c.curve_to(-10, -42, -6, -36, 6, -34); c.stroke()
    for i in range(7):                                                                                       # the routing grid
        yy = -30 + i * 19
        c.set_source_rgb(*ENV_D); c.set_line_width(1.0); c.move_to(-70, yy); c.line_to(70, yy); c.stroke()
        if i < 5:                                                                                            # old names, crossed
            c.set_source_rgba(0.25, 0.25, 0.30, 0.55); c.set_line_width(1.6)
            c.move_to(-60, yy + 12); c.curve_to(-40, yy + 6, -20, yy + 16, 10 + (i * 7) % 20, yy + 10); c.stroke()
            c.set_source_rgba(0.25, 0.25, 0.30, 0.7); c.set_line_width(1.2); c.move_to(-64, yy + 10); c.line_to(32, yy + 10); c.stroke()
    c.set_line_width(1.0); c.set_source_rgb(*ENV_D); c.move_to(-14, -30); c.line_to(-14, 104); c.stroke()
    kit.text(k, "PAM", -40, 94, 24, PEN, font="Comic Neue", bold=True)
    c.restore()


def rota(k, x, y, s=1.0, ang=0.0):
    """(x, y): its middle; 220 x 300 at s=1."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    cut(k, [(-110, -150), (110, -150), (110, 150), (-110, 150)], PAPER, shadow=False, lw=2.2)
    kit.text(k, "COFFEE ROTA", 0, -120, 30, INK, bold=True)
    c.set_source_rgb(*INK); c.set_line_width(2); c.move_to(-96, -102); c.line_to(96, -102); c.stroke()
    for i, d in enumerate(("MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN")):
        yy = -84 + i * 34
        kit.text(k, d, -62, yy + 12, 22, (0.20, 0.20, 0.24), bold=True)
        kit.text(k, "PAM", 46, yy + 13, 28, RED, bold=True)
        c.set_source_rgb(0.78, 0.78, 0.80); c.set_line_width(1); c.move_to(-96, yy + 24); c.line_to(96, yy + 24); c.stroke()
    c.restore()


# ---- the sheet ------------------------------------------------------------------------------------------------------------

def _frame(fn, bg=None):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1080, 1920); s.set_device_scale(2, 2)
    c = cairo.Context(s); k = kit.Ctx(c, 0)
    c.set_source_rgb(*(bg or kit.WALL)); c.paint()
    fn(k)
    return s


def s6(k, eighth=False):
    """7.1 / 8.1 at setup S6, zone C: the set, the machine (ok), the lamp on, the seven cups (eight at the end)."""
    import fs_set4 as fs4
    import fs_storyboard_v17 as sb
    import dh_props as dp
    c = k.c
    c.save(); sb.view(c, 720, 600, 1.6)
    def props(k):
        dp.coffee_machine(k, 770, F - 166, 0.62, "ok")
        counter_lamp(k, *LAMP)
        cups(k, eighth=eighth)
    fs4.draw_set(k, {"mom_front": props})
    c.restore()


def lamp_match(k):
    """8.2's end: the camera has pushed in from S6 (8.1, the counter, the cups under the rota) until the lamp's head hangs
    where frame 0's streetlamp hangs (on4_street.A_LAMP); the room goes dark round it as the rain starts, so the cut to
    the night street (8.3 = frame 0) keeps only the lamp. The push carries the context: it is the desk lamp."""
    import fs_set4 as fs4
    import dh_props as dp
    c = k.c
    z = 2.4
    hx, hy = LAMP[0] - 40, LAMP[1] - 90
    ax, ay = st.A_LAMP
    c.save(); c.translate(ax, ay); c.scale(z, z); c.translate(-hx, -hy)
    fs4.draw_set(k, {"mom_front": lambda k: (cups(k, eighth=True), counter_lamp(k, *LAMP))})
    c.restore()
    g = cairo.RadialGradient(ax, ay + 20, 90, ax, ay + 20, 470)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.0); g.add_color_stop_rgba(0.40, 0.02, 0.02, 0.04, 0.85); g.add_color_stop_rgba(1, 0.02, 0.02, 0.04, 0.97)
    c.set_source(g); c.paint()
    st.lamp_head(k, ax, ay, 0.62 * z)                                   # the head over the dark, as in frame 0


def s6_rota(k):
    """8.1 / 8.2's start: S6, eight (Sofia's mug at the end), the rota laid over the cups."""
    import fs_set4 as fs4
    import fs_storyboard_v17 as sb
    import dh_props as dp
    c = k.c
    c.save(); sb.view(c, 720, 600, 1.6)
    def props(k):
        dp.coffee_machine(k, 770, F - 166, 0.62, "ok")
        counter_lamp(k, *LAMP)
        cups(k, eighth=True)
        rota(k, 734, F - 168, 0.30, 0.12)
    fs4.draw_set(k, {"mom_front": props})
    c.restore()


def frame0(k):
    import engine_on as eng
    s = st.render("A", 2, True)
    k.c.set_source_surface(s, 0, 0); k.c.paint()


def insert74(k):
    c = k.c
    c.set_source_rgb(0.60, 0.48, 0.34); c.paint()
    rota(k, 270, 300, 1.1, -0.02)                       # pulled right out: every PAM reads (lesson 111)
    envelope(k, 282, 600, 0.92, 0.05, open_=True)       # under it, the envelope it came in


def cups_close(k):
    c = k.c
    c.set_source_rgb(*kit.WALL); c.paint()
    c.set_source_rgb(0.93, 0.89, 0.80); c.rectangle(0, 470, 540, 120); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(2); c.move_to(0, 590); c.line_to(540, 590); c.stroke()
    c.set_source_rgb(0.86, 0.80, 0.68); c.rectangle(0, 590, 540, 370); c.fill()
    cups(k, 52, 560, 1.15, 7, 44, eighth=True)            # the eighth ends by x 440, clear of the rail


def sheet(out="../office-noir-4/on4_props_sheet_v2.png", phone="../office-noir-4/on4_props_phone_v2.png"):
    panels = [(_frame(lambda k: s6(k, False)), "7.1 S6: the lamp, seven cups, the machine"),
              (_frame(s6_rota), "8.1 / 8.2 start: Sofia's mug, the rota over the cups"),
              (_frame(lamp_match), "8.2 end: pushed in to the lamp, the room goes dark"),
              (st.render("A", 2, True), "8.3 = frame 0: the streetlamp"),
              (_frame(insert74), "7.4: INTERNAL MAIL, the COFFEE ROTA"),
              (_frame(cups_close), "the cups, close: the eighth is hers")]
    cols = 3
    W_, H_ = cols * 560 + 20, 70 + 2 * (960 + 50)
    sh = cairo.ImageSurface(cairo.FORMAT_RGB24, W_, H_); c = cairo.Context(sh)
    c.set_source_rgb(0.93, 0.92, 0.89); c.paint()
    c.set_source_rgb(0.1, 0.1, 0.1); c.select_font_face("Inter", 0, 1); c.set_font_size(26)
    c.move_to(20, 42); c.show_text("Office Noir 4: the awake props, v2 (Sofia's own mug; the eighth clear of the rail; dead zones in red)")
    for i, (s, lab) in enumerate(panels):
        x = 20 + (i % cols) * 560; y = 70 + (i // cols) * 1010
        c.set_source_surface(s, x, y); c.paint()
        c.save(); c.translate(x, y); st.overlay(c); c.restore()
        c.set_source_rgb(0.1, 0.1, 0.1); c.select_font_face("Inter", 0, 1); c.set_font_size(18)
        c.move_to(x, y + 960 + 28); c.show_text(lab)
    sh.write_to_png(out)
    ph = cairo.ImageSurface(cairo.FORMAT_RGB24, 6 * 280 - 10, 480); c = cairo.Context(ph); c.set_source_rgb(1, 1, 1); c.paint()
    for i, (s, _) in enumerate(panels):
        c.save(); c.translate(i * 280, 0); c.scale(0.5, 0.5); c.set_source_surface(s, 0, 0); c.paint(); c.restore()
    ph.write_to_png(phone)
    return out


if __name__ == "__main__":
    print(sheet())
