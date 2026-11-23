"""OFFICE NOIR 4: the awake props, v1 (23 Nov). Stage 3, script v4 beats 7-8 (the front desk set, zone C, morning, colour).
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
CUPS = (690, F - 150, 0.50, 7, 22)          # x0, base, scale, n, step: along the counter's front edge
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
        cup(k, x0 + n * step + 4, base + 1, s * 1.05, lipstick=True)


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
    kit.text(k, "INTERNAL MAIL", 0, -92, 16, (0.42, 0.28, 0.14), bold=True)
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
    """8.2 -> 8.3: the counter lamp close, its head where frame 0's streetlamp hangs (on4_street.A_LAMP)."""
    c = k.c
    c.set_source_rgb(0.72, 0.66, 0.56); c.paint()
    ax, ay = st.A_LAMP
    s = 2.4
    counter_lamp(k, ax + 40 * s, ay + 90 * s, s)
    c.set_source_rgb(0.60, 0.48, 0.34); c.rectangle(0, ay + 90 * s, 540, 960); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(2); c.move_to(0, ay + 90 * s); c.line_to(540, ay + 90 * s); c.stroke()


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
    cups(k, 40, 560, 1.4, 7, 58, eighth=True)


def sheet(out="../office-noir-4/on4_props_sheet_v1.png", phone="../office-noir-4/on4_props_phone_v1.png"):
    panels = [(_frame(lambda k: s6(k, False)), "7.1 S6: the lamp, seven cups, the machine"),
              (_frame(lambda k: s6(k, True)), "8.1 S6: eight cups (Sofia's mug)"),
              (_frame(lamp_match), "8.2: the counter lamp, close"),
              (st.render("A", 2, True), "8.3 = frame 0: the streetlamp"),
              (_frame(insert74), "7.4: INTERNAL MAIL, the COFFEE ROTA"),
              (_frame(cups_close), "the cups, close: the eighth has lipstick")]
    cols = 3
    W_, H_ = cols * 560 + 20, 70 + 2 * (960 + 50)
    sh = cairo.ImageSurface(cairo.FORMAT_RGB24, W_, H_); c = cairo.Context(sh)
    c.set_source_rgb(0.93, 0.92, 0.89); c.paint()
    c.set_source_rgb(0.1, 0.1, 0.1); c.select_font_face("Inter", 0, 1); c.set_font_size(26)
    c.move_to(20, 42); c.show_text("Office Noir 4: the awake props, v1 (zone C; dead zones in red)")
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
