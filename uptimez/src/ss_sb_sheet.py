"""v2 (ss_sb_sheet_v1.py = v1 from ss_sb_v1), concept v5. The Secret Santa silent storyboard as a sheet: 20 frames from ss_sb (the 16 shots and the beats inside them),
labelled with shot, beat and time. Writes ss_sb_sheet_v1.png at 2400x1240 (drawn at 1200x620, 2x)."""
import sys
import cairo
import kit
import brand
import engine_v as ev
import ss_sb
from kit import INK
from charsheets import corp

W2, H2 = 1200, 620
GREY = (0.35, 0.40, 0.50)
FR = [(15, "1 ECU: the uncap"), (95, "1 out: the whisper"), (150, "2 \"mirrors\""), (210, "3 Agent Santa"),
      (290, "4 \"Licensed to gift.\""), (305, "4 Pam melts"), (370, "5 one heart, he looks past"),
      (400, "6 \"Sofía.\""), (450, "6 \"…a full-length mirror.\""), (485, "7A hurt"), (515, "7B denial"),
      (590, "8 she signs, the kiss"), (625, "9 proud"), (680, "10 detected"), (750, "12 recipient (high)"),
      (790, "13 the hover"), (812, "13 THUNK. on the kiss"), (845, "14 it lands"), (935, "15 UNCLAIMED"),
      (1005, "15 You're welcome. / APPROVED")]


def main(out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "SECRET SANTA · STORYBOARD", 68, 44, 26, bold=True)
    corp(c, "silent · 34.6 s · 16 shots (20 frames: beats inside shots) · concept v5", 480, 44, 13, col=GREY)
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10)
    t = "UPTIMEZ INC. · STORYBOARD v2"
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
    main(sys.argv[1] if len(sys.argv) > 1 else "ss_sb_sheet_v2.png")
