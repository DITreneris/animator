"""OFFICE NOIR 3: the side drawings beside the front ones, on one sheet, for approval before they go into the film."""
import sys, math, cairo
from kit import Ctx
import client_on3 as b, client_sheet_on3 as csh, street_casts_on3 as stc, alley_on3 as al, noir2_cast as n2, motion_on3 as mo
import sofia_ob as sob
import profile_on3 as pf

W, H = 1620, 960


def sheet(path, noir=True, xs=(0.0, 0.25)):
    S = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(S); k = Ctx(c, 0)
    c.set_source_rgb(0.80, 0.80, 0.80); c.paint()
    F = 820; s = 1.55
    cols = [("THE CLIENT", lambda x: b.boxer(k, x, F, s * b.REL, "b_walk", "hard", (0.8, 0), outfit="street"),
             lambda x, ph: pf.client(k, x + ph, F, s * b.REL, 1), 46 * 4 * s * b.REL),
            ("DON", lambda x: mo.don(k, x, F, s, "look", "squint", (0.6, 0.3)),
             lambda x, ph: pf.don(k, x + ph, F, s, 1), 34 * 4 * s),
            ("SOFIA", lambda x: sob.sofia(k, x, F, s * 0.86, "low", "smile", (-0.9, 0.2), badge=False, tablet_kind=None),
             lambda x, ph: pf.her(k, x + ph, F, s * 0.86, -1), 30 * 4 * s * 0.86)]
    for i, (name, front, side, cyc) in enumerate(cols):
        x0 = 540 * i
        c.set_source_rgb(0.1, 0.1, 0.1); c.select_font_face("sans", 0, 1); c.set_font_size(26); c.move_to(x0 + 20, 40); c.show_text(name + ": front, side")
        front(x0 + 120)
        for j, u in enumerate(xs):
            # the side drawing takes its step from x: shift the canvas so that phase u stands at the same place
            ph = u * cyc
            xx = x0 + 300 + 150 * j
            base = math.floor(xx / cyc) * cyc
            c.save(); c.translate(xx - (base + ph), 0); side(base, ph); c.restore()
    if noir:
        csh.noir(S)
    S.write_to_png(path)


if __name__ == "__main__":
    sheet(sys.argv[1] if len(sys.argv) > 1 else "../office-noir-3/on3_profile_sheet_v1.png")
