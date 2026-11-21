"""OFFICE NOIR 3: the turned walkers beside the front drawings, on one sheet, for approval before they go into the film.
v2 (v1 pinned): each figure's front drawing, then its four walk poses (contact, down, passing, up) on a floor line with
its contact shadow."""
import sys, math, cairo
from kit import Ctx
import client_on3 as b, client_sheet_on3 as csh, motion_on3 as mo
import sofia_ob as sob
import profile_on3 as pf

W, H = 1620, 1830
POSES = (("CONTACT", 0.0), ("DOWN", 0.09), ("PASSING", 0.25), ("UP", 0.34))


def shadow(c, x, y, w):
    c.save(); c.translate(x, y); c.scale(w, w * 0.14); c.new_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
    c.set_source_rgba(0, 0, 0, 0.30); c.fill()


def sheet(path, noir=True):
    S = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(S); k = Ctx(c, 0)
    c.set_source_rgb(0.80, 0.80, 0.80); c.paint()
    s = 1.12
    rows = [("THE CLIENT", lambda x, F: b.boxer(k, x, F, s * b.REL, "b_walk", "hard", (0.8, 0), outfit="street"),
             lambda x, F: pf.client(k, x, F, s * b.REL, 1), 40 * 4 * s * b.REL, 1, 66),
            ("DON", lambda x, F: mo.don(k, x, F, s, "look", "squint", (0.6, 0.3)),
             lambda x, F: pf.don(k, x, F, s, 1), 38 * 4 * s, 1, 50),
            ("SOFIA", lambda x, F: sob.sofia(k, x, F, s * 0.86, "low", "smile", (-0.9, 0.2), badge=False, tablet_kind=None),
             lambda x, F: pf.her(k, x, F, s * 0.86, -1), 24 * 4 * s * 0.86, -1, 40)]
    for i, (name, front, side, cyc, dir_, sw) in enumerate(rows):
        F = 560 + 610 * i
        c.set_source_rgb(0.66, 0.66, 0.66); c.rectangle(0, F, W, 34); c.fill()
        c.set_source_rgb(0.1, 0.1, 0.1); c.select_font_face("sans", 0, 1); c.set_font_size(26); c.move_to(24, F - 500); c.show_text(name)
        c.set_font_size(18); c.move_to(110, F + 24); c.show_text("FRONT")
        shadow(c, 150, F, sw); front(150, F)
        for j, (lab, u) in enumerate(POSES):
            xx = 480 + 290 * j
            n = math.floor(xx / cyc)
            xs = (n + u * dir_) * cyc if dir_ > 0 else (n + 1 + u * dir_) * cyc      # the place on the ground where the walk is at this pose
            c.save(); c.translate(xx - xs, 0)
            shadow(c, xs, F, sw); side(xs, F)
            c.restore()
            c.set_source_rgb(0.1, 0.1, 0.1); c.set_font_size(18); c.move_to(xx - 40, F + 24); c.show_text(lab)
    if noir:
        csh.noir(S)
    S.write_to_png(path)


if __name__ == "__main__":
    sheet(sys.argv[1] if len(sys.argv) > 1 else "../office-noir-3/on3_profile_sheet_v2.png")
