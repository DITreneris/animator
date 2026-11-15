"""Contact sheet for the Mandatory Fun silent storyboard (mf_sb.py): one frame per panel at a representative time,
with shot number, timecode and framing. Writes mf_storyboard_sheet_v1.png (2400x1560)."""
import sys
import cairo
import kit
import brand
import engine_v
import mf_sb_v1 as sb
from kit import INK
from charsheets import corp

W2, H2 = 1200, 780
GREY = (0.35, 0.40, 0.50)
PICK = {"s1": (0.9, "1 slide slam", "MS, punch-in"), "s2": (3.0, "2 reverse", "2-shot"),
        "s3": (4.4, "3 the door", "LOW + DUTCH"), "s4": (6.6, "4 \"under arrest\" 💗", "tight 2-shot"),
        "s4b": (10.6, "4 page turn", "INSERT"), "s5": (11.8, "5 \"I confess\"", "3-shot"),
        "s6a": (14.3, "6 the scan", "CU Don"), "s6b": (15.6, "6 red", "CU robot"),
        "s7": (17.0, "7 \"a cop!\"", "MCU, DUTCH"), "s8a": (18.6, "8 the cuffs", "INSERT"),
        "s8b": (19.6, "8 turns to Pam", "MS"), "s9a": (20.6, "9 APPROVED!", "CU, push-in"),
        "s9b": (21.4, "9 tick, DING", "CU robot"), "s10": (23.5, "10 two clicks", "INSERT"),
        "s11": (25.15, "11 the yank", "WIDE, locked"), "s12": (31.6, "12 FUN DETECTED", "2-shot, level")}


def main(out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "MANDATORY FUN · STORYBOARD v1", 68, 44, 26, bold=True)
    corp(c, "silent · 16 panels · 33.0 s · camera plan v2.2 · yank from the v2 motion test", 580, 44, 12, col=GREY)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 64); c.line_to(W2 - 24, 64); c.stroke()
    fr = cairo.ImageSurface(cairo.FORMAT_ARGB32, kit.W, kit.H)
    sc = 0.255
    for i, (t0, t1, fn) in enumerate(sb.PANELS):
        tsec, lab, kind = PICK[fn.__name__]
        engine_v.render(sb, int(round(tsec * 30)), fr)
        x, y = 24 + (i % 8) * 145, 80 + (i // 8) * 345
        c.save(); c.translate(x, y); c.scale(sc, sc); c.set_source_surface(fr, 0, 0); c.paint(); c.restore()
        c.set_source_rgb(*INK); c.set_line_width(1); c.rectangle(x, y, kit.W * sc, kit.H * sc); c.stroke()
        corp(c, lab.replace("💗", "+ heart"), x, y + kit.H * sc + 13, 9, col=INK, bold=True)
        corp(c, f"{t0:.1f}-{t1:.1f} s · {kind}", x, y + kit.H * sc + 26, 8, col=GREY)
    surf.write_to_png(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "mf_storyboard_sheet_v1.png")
