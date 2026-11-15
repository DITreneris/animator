"""v1. The Secret Santa silent storyboard as a sheet: 20 frames from ss_sb (the 16 shots and the beats inside them),
labelled with shot, beat and time. Writes ss_sb_sheet_v1.png at 2400x1240 (drawn at 1200x620, 2x)."""
import sys
import cairo
import kit
import brand
import engine_v as ev
import ss_sb_v1 as ss_sb
from kit import INK
from charsheets import corp

W2, H2 = 1200, 620
GREY = (0.35, 0.40, 0.50)
FR = [(15, "1 ECU: the uncap"), (95, "1 out: the whisper"), (150, "2 \"mirrors\""), (232, "3 Agent Santa"),
      (285, "4 glasses off"), (375, "5 one heart"), (450, "6 \"a mirror\""), (480, "7A hurt"), (510, "7B decides"),
      (590, "8 she signs it"), (640, "9 proud"), (700, "10 detected"), (750, "11 sender"), (785, "12 recipient"),
      (840, "13 the hover"), (866, "13 THUNK."), (895, "14 the stare"), (912, "14 it lands"),
      (1010, "15 You're welcome."), (1080, "16 attempt two")]


def main(out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "SECRET SANTA · STORYBOARD", 68, 44, 26, bold=True)
    corp(c, "silent · 36.5 s · 16 shots · bubbles for the lines, no voices yet", 480, 44, 13, col=GREY)
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10)
    t = "UPTIMEZ INC. · STORYBOARD v1"
    corp(c, t, W2 - 24 - c.text_extents(t).x_advance, 30, 10, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 64); c.line_to(W2 - 24, 64); c.stroke()
    fs = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960)
    sc = 0.2
    for i, (f, lab) in enumerate(FR):
        ev.render(ss_sb, f, fs)
        x, y = 24 + (i % 10) * 116, 84 + (i // 10) * 262
        c.save(); c.translate(x, y); c.scale(sc, sc); c.set_source_surface(fs, 0, 0); c.paint(); c.restore()
        c.set_source_rgb(*INK); c.set_line_width(1.2); c.rectangle(x, y, 540 * sc, 960 * sc); c.stroke()
        corp(c, lab, x, y + 960 * sc + 13, 8.5, col=INK, bold=True)
        corp(c, "%.1f s" % (f / 30.0), x, y + 960 * sc + 25, 8, col=GREY)
    surf.write_to_png(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "ss_sb_sheet_v1.png")
