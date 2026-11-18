"""v3 (thumb_on2_v2.py = v2, kept), after the second review: her eyes on him, the same smirk ("I know you're there");
the headline smaller; a thin light on his hat brim and collar, and his lit hand with the watch coming for her shoulder
(the Shadow never has a face: his signs are the brim, the collar, the watch and one lit hand).
v2 (thumb_on2_v1.py = v1, kept): Cover for "Office Noir 2: The Shadow of Fate", 1080x1920, drawn natively at 1080
with the film's own kit in the v25 look. Rebuilt after an outside review (concept A/C: "who's behind her? / she
knows"): her face close and large, looking at us with her smirk; the Shadow's fedora and shoulders big and sharp on
a lit wall right behind her shoulder, his shadow falling across one side of her face; one headline card, "The Shadow
of Fate", and OFFICE NOIR 2 as a small label; the blinds fainter; no clock.
Usage: python3 thumb_on2.py out.png"""
import sys
import math
import cairo
import on2_motion as m
import on_set as ons
import props_sheet_on as psh
import client_ob as co
from kit import Ctx

b, n, eng = m.b, m.n, m.eng
SX, SFEET, SS = 318, 1450, 3.1                                           # her: centre, feet, scale (her head is large)


def picture():
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, m.W, m.H)             # 1080x1920 under m._Hi
    c = cairo.Context(surf)
    k = Ctx(c, 0)
    c.set_source_rgb(0.30, 0.30, 0.31); c.paint()
    g = cairo.RadialGradient(150, 420, 40, 150, 420, 420)                 # the lamp on the wall behind them
    g.add_color_stop_rgba(0, 0.95, 0.94, 0.90, 1.0); g.add_color_stop_rgba(1, 0.95, 0.94, 0.90, 0.0)
    c.set_source(g); c.paint()
    ons.blinds(c, -40, -40, m.W + 80, m.H + 80, -0.32, 34, 10, 0.16)
    b.black_fig(k, lambda: co.client(k, 150, 1240, 2.15, "open", "plain", look=(0, 0), roll=False, badge=False))    # the Shadow
    b.hat_at(k, 153, 1240 + (co.HY - 38) * 2.15, 2.7)
    o = n.star(k, SX, SFEET, SS, "g_down", "knowing", (-1.0, 0.05), wrap=False, bag=False)
    hx, hy = o["head"]
    c.set_source_rgb(0.78, 0.78, 0.80); c.set_line_width(2.6); c.set_line_cap(1)   # the lamp on his brim and his collar
    c.move_to(18, 362); c.curve_to(90, 352, 200, 352, 300, 344); c.stroke()
    c.move_to(30, 420); c.curve_to(70, 440, 110, 470, 140, 520); c.stroke()     # his collar, clear of her hair
    b.arm_in(k, -70, 900, hx - 150, hy + 245)                            # his lit hand, the watch, coming for her shoulder
    c.save()                                                             # his shadow across the near side of her face
    c.translate(hx - 150, hy - 120); c.rotate(0.18)
    c.set_source_rgba(0, 0, 0, 0.42)
    c.move_to(0, 0); c.curve_to(60, 30, 120, 70, 128, 160); c.curve_to(110, 260, 70, 330, 20, 380); c.line_to(-120, 380)
    c.line_to(-120, 0); c.close_path(); c.fill()
    c.restore()
    eng.TONE = "v3"
    try:
        eng.accent_pass(surf, n.ACCENTS2)
    finally:
        eng.TONE = "v2"
    c = cairo.Context(surf)
    eng.side_light(c, 0, 0, m.W, m.H, from_left=True, amount=0.38)       # the dark side is away from him
    ons.key_light(c, hx + 30, hy, 220, 0.18)
    g = cairo.RadialGradient(m.W / 2, m.H * 0.42, m.H * 0.32, m.W / 2, m.H * 0.42, m.H * 0.80)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.0); g.add_color_stop_rgba(1, 0, 0, 0, 0.45); c.set_source(g); c.paint()
    psh.caption(c, "OFFICE NOIR 2", 24, 104, 22)                         # the series, small
    psh.caption(c, "The Shadow of Fate", 24, 150, 34)                    # the headline, over the lit wall, above them
    return surf


def main(out):
    orig = cairo.ImageSurface
    cairo.ImageSurface = m._Hi(orig)
    try:
        pic = picture()
    finally:
        cairo.ImageSurface = orig
    pic.write_to_png(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "../office-noir-2/on2_cover_v3.png")
