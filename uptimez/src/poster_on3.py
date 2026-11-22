"""OFFICE NOIR 3: the fight bill, as a prop of its own (22 Nov; Tomas: "the glove climbs onto the letters of VS; make
the poster separately, as a prop"). The same sheet as street_on3.poster2 (96 x 136 at scale 1.3, same corner), so the
staging does not move. What is new: the middle row is three things that do not touch: the red glove, VS, the robot's
head, each in its own third with air between; the glove has a cuff and a shine, the head an aerial and a jaw.
  bill(k, x, y, s=1.0, seed=0)      sheet() -> ../office-noir-3/on3_poster_prop_v1.png"""
import math
import cairo
import kit
from kit import Ctx, rect, ellipse, cut
import client_on3 as b
import street_on3 as st

PAPER, INK = st.PAPER, st.INK
W, H = 96, 136
GLOVE_X, VS_X, HEAD_X, ROW_Y = 20, 48, 76, 68               # the three thirds of the middle row


def bill(k, x, y, s=1.0, seed=0):
    c = k.c
    c.save(); c.translate(x - 14, y - 34); c.scale(s * 1.3, s * 1.3)
    rect(k, 0, 0, W, H, PAPER, seed, shadow=False, lw=2.4)
    c.set_source_rgb(*INK); c.rectangle(4, 4, 88, 18); c.fill()
    kit.text(k, "TONIGHT", 48, 13.5, 11.5, PAPER, bold=True)
    kit.text(k, "HUMAN", 48, 37, 19, INK, bold=True)
    # the glove: fist, thumb, cuff; all left of x = 35
    rect(k, GLOVE_X - 9, ROW_Y + 9, 16, 8, PAPER, seed + 1, shadow=False, lw=1.6)
    ellipse(k, GLOVE_X, ROW_Y - 1, 12.5, 12, b.KEY, seed + 2, shadow=False, lw=2)
    ellipse(k, GLOVE_X + 9, ROW_Y + 3, 4.5, 6, b.KEY, seed + 3, shadow=False, lw=1.6)
    c.set_source_rgba(1, 1, 1, 0.75); c.set_line_width(1.8); c.set_line_cap(1); c.move_to(GLOVE_X - 6, ROW_Y - 7); c.line_to(GLOVE_X - 1, ROW_Y - 9); c.stroke(); c.set_line_cap(0)
    kit.text(k, "VS", VS_X, ROW_Y + 1, 12, INK, bold=True)                                             # 39..57: clear of both
    # the robot's head: all right of x = 62
    rect(k, HEAD_X - 13, ROW_Y - 12, 26, 24, (0.20, 0.20, 0.23), seed + 4, shadow=False, lw=2)
    c.set_source_rgb(*PAPER); c.rectangle(HEAD_X - 8, ROW_Y - 6, 5.5, 4); c.fill(); c.rectangle(HEAD_X + 2.5, ROW_Y - 6, 5.5, 4); c.fill()
    for i in range(4):
        c.rectangle(HEAD_X - 8 + i * 4.3, ROW_Y + 4, 3, 3.4); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(2); c.move_to(HEAD_X, ROW_Y - 12); c.line_to(HEAD_X, ROW_Y - 19); c.stroke(); c.arc(HEAD_X, ROW_Y - 21, 2.4, 0, 2 * math.pi); c.fill()
    kit.text(k, "ROBOT", 48, 100, 19, INK, bold=True)
    c.set_source_rgb(*INK); c.set_line_width(1.6); c.move_to(10, 114); c.line_to(86, 114); c.stroke()
    kit.text(k, "LAST ROUND", 48, 124, 9.5, INK, bold=True)
    c.restore()


def sheet(path="../office-noir-3/on3_poster_prop_v1.png"):
    import client_sheet_on3 as csh
    S = cairo.ImageSurface(cairo.FORMAT_RGB24, 1500, 900); c = cairo.Context(S); c.set_source_rgb(0.86, 0.86, 0.86); c.paint()
    for i, (lab, fn, noir) in enumerate((("was (street_on3.poster2)", st.poster2, False), ("now (poster_on3.bill)", bill, False), ("now, in the dream's look", bill, True))):
        t = cairo.ImageSurface(cairo.FORMAT_RGB24, 460, 660); tc = cairo.Context(t); tc.set_source_rgb(0.30, 0.30, 0.33); tc.paint()
        fn(Ctx(tc, 0), 40 + 14 * 3.0, 40 + 34 * 3.0, 3.0, 20)
        if noir:
            csh.noir(t)
        c.set_source_surface(t, 30 + i * 490, 60); c.paint()
        c.set_source_rgb(0.1, 0.1, 0.1); c.select_font_face("DejaVu Sans", 0, 1); c.set_font_size(24); c.move_to(30 + i * 490, 44); c.show_text(lab)
    for i, sc in enumerate((1.0, 0.7)):                                                                 # at the sizes the film shows it
        t = cairo.ImageSurface(cairo.FORMAT_RGB24, 200, 200); tc = cairo.Context(t); tc.set_source_rgb(0.30, 0.30, 0.33); tc.paint()
        bill(Ctx(tc, 0), 30 + 14, 10 + 34, sc, 20); csh.noir(t)
        c.set_source_surface(t, 30 + i * 220, 740 - 40); c.rectangle(30 + i * 220, 700, 200, 190); c.fill()
    c.set_source_rgb(0.1, 0.1, 0.1); c.set_font_size(20); c.move_to(480, 800); c.show_text("at the street's size (1.0) and smaller (0.7): the three stay apart")
    S.write_to_png(path)


if __name__ == "__main__":
    sheet()
