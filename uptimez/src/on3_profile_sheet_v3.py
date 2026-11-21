"""OFFICE NOIR 3: the turned walkers on one sheet, for approval before they go into the film. v3 (v1, v2 pinned): each as
it walks in the film, with what it carries there: the front drawing (a reference, not a pose of the walk), then the
whole cycle, both legs: contact, down, passing, up, and the same four on the other leg."""
import sys, math, cairo
from kit import Ctx
import client_on3 as b, client_sheet_on3 as csh, motion_on3 as mo
import sofia_ob as sob
import profile_on3_v4 as pf

W, H = 1900, 2000
POSES = (("CONTACT", 0.0), ("DOWN", 0.09), ("PASSING", 0.25), ("UP", 0.34), ("CONTACT 2", 0.5), ("DOWN 2", 0.59), ("PASSING 2", 0.75), ("UP 2", 0.84))
S_ = 0.86


def shadow(c, x, y, w):
    c.save(); c.translate(x, y); c.scale(w, w * 0.14); c.new_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
    c.set_source_rgba(0, 0, 0, 0.30); c.fill()


def her_front(k, x, F, s):
    o = sob.sofia(k, x, F, s, "low", "smile", (-0.9, 0.2), badge=False, tablet_kind=None)
    hx, hy = o["hands"][1]; c = k.c                           # her umbrella, as on the street
    c.save(); c.translate(hx, hy); c.scale(s / 0.774, s / 0.774); c.translate(-hx, -hy)
    c.set_source_rgb(0.10, 0.10, 0.12); c.set_line_width(4); c.move_to(hx, hy); c.line_to(hx - 6, hy - 250); c.stroke()
    c.new_path(); c.move_to(hx - 126, hy - 236); c.curve_to(hx - 100, hy - 330, hx + 88, hy - 330, hx + 114, hy - 236)
    for i in range(4):
        x0 = hx + 114 - 60 * i; c.curve_to(x0 - 10, hy - 250, x0 - 50, hy - 250, x0 - 60, hy - 236)
    c.close_path(); c.set_source_rgb(0.08, 0.08, 0.10); c.fill_preserve(); c.set_source_rgb(0.02, 0.02, 0.03); c.set_line_width(3); c.stroke()
    c.restore()


def rows(k):
    s = S_
    return [("THE CLIENT (2.1)", lambda x, F: b.boxer(k, x, F, s * b.REL, "b_walk", "hard", (0.8, 0), outfit="street"),
             lambda x, F: pf.client(k, x, F, s * b.REL, 1), 40 * 4 * s * b.REL, 1, 52),
            ("THE CLIENT (3.1, 3.4: the folder, the cigarette)", lambda x, F: b.boxer(k, x, F, s * b.REL, "b_walk", "hard", (0.8, 0), outfit="street", cig=True),
             lambda x, F: pf.client(k, x, F, s * b.REL, 1, cig=True, folder=True), 40 * 4 * s * b.REL, 1, 52),
            ("DON (3.4b: over his glass)", lambda x, F: mo.don(k, x, F, s, "look", "squint", (0.6, 0.9), lean=10),
             lambda x, F: pf.don(k, x, F, s, 1, bent=1.0), 26 * 4 * s, 1, 40),
            ("SOFIA (2.6)", lambda x, F: her_front(k, x, F, s * 0.86),
             lambda x, F: pf.her(k, x, F, s * 0.86, -1), 25 * 4 * s * 0.86, -1, 32)]


def sheet(path, noir=True):
    S = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(S); k = Ctx(c, 0)
    c.set_source_rgb(0.80, 0.80, 0.80); c.paint()
    for i, (name, front, side, cyc, dir_, sw) in enumerate(rows(k)):
        F = 440 + 490 * i + (40 if i == 3 else 0)
        c.set_source_rgb(0.66, 0.66, 0.66); c.rectangle(0, F, W, 30); c.fill()
        c.set_source_rgb(0.1, 0.1, 0.1); c.select_font_face("sans", 0, 1); c.set_font_size(22); c.move_to(20, F - 400 - (40 if i == 3 else 0)); c.show_text(name)
        c.set_font_size(15); c.move_to(70, F + 21); c.show_text("FRONT (reference)")
        c.set_source_rgb(0.5, 0.5, 0.5); c.rectangle(262, F - 380, 2, 410); c.fill()
        shadow(c, 130, F, sw); front(130, F)
        for j, (lab, u) in enumerate(POSES):
            xx = 380 + 196 * j
            n = math.floor(xx / cyc)
            xs = (n + u) * cyc if dir_ > 0 else (n + 1 - u) * cyc          # the place on the ground where the walk is at this pose
            c.save(); c.translate(xx - xs, 0)
            shadow(c, xs, F, sw); side(xs, F)
            c.restore()
            c.set_source_rgb(0.1, 0.1, 0.1); c.set_font_size(15); c.move_to(xx - 40, F + 21); c.show_text(lab)
    if noir:
        csh.noir(S)
    S.write_to_png(path)


if __name__ == "__main__":
    sheet(sys.argv[1] if len(sys.argv) > 1 else "../office-noir-3/on3_profile_sheet_v3.png")
