"""v1, pinned: on2_cover_v1.png. thumb_on2.py is current.
Cover for "Office Noir 2: The Shadow of Fate" (1080x1920, drawn natively at 1080 with the film's own kit, in the
v25 look: the blinds on the wall, a side light, lighter faces, typewriter cards).
Inside the centre the profile grids crop to (y 120-840 at the 540x960 drawing scale): Sofía in the red gown with
the roll in her hand, knowing; behind her, screen left, the Shadow, hat and shoulders, and his lit hand coming in
from the left for the roll (the same reach as in the film); a clock at 11:59. The title is three
typewriter cards, as on the first Office Noir's cover.
Usage: python3 thumb_on2.py out.png"""
import sys
import cairo
import on2_motion as m
import on_set as ons
import props_sheet_on as psh
import client_ob as co
from kit import Ctx

b, n, eng = m.b, m.n, m.eng


def picture():
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, m.W, m.H)              # 1080x1920 under m._Hi
    c = cairo.Context(surf)
    k = Ctx(c, 0)
    b.lit_wall(k)
    m._blinds(k)
    b.black_fig(k, lambda: co.client(k, 120, 1170, 1.75, "open", "plain", look=(0, 0), roll=False, badge=False))   # his shadow,
    b.hat_at(k, 123, 1170 + (co.HY - 38) * 1.75, 2.2)                     # behind her, screen left, as in the film
    m.NOW["min"], m.NOW["sec"] = 59, None
    m.clock(k, 470, 150, 30)
    o = n.star(k, 340, 1090, 2.1, "g_down", "knowing", (-0.9, 0.25), wrap=False, bag=False, roll=True)
    rx, ry = o["hands"][0]
    b.arm_in(k, -80, 1040, rx - 40, ry - 10)                              # his hand, for the roll
    eng.TONE = "v3"
    try:
        eng.accent_pass(surf, n.ACCENTS2)
    finally:
        eng.TONE = "v2"
    c = cairo.Context(surf)
    eng.side_light(c, 0, 0, m.W, m.H, from_left=False, amount=0.40)
    hx, hy = o["head"]
    ons.key_light(c, hx, hy, 230, 0.22)
    b.vignette(c)
    g = cairo.RadialGradient(m.W / 2, m.H * 0.42, m.H * 0.30, m.W / 2, m.H * 0.42, m.H * 0.80)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.0); g.add_color_stop_rgba(1, 0, 0, 0, 0.40); c.set_source(g); c.paint()
    psh.caption(c, "OFFICE NOIR 2", 24, 150, 54)
    psh.caption(c, "The Shadow", 24, 150 + 54 * 1.9, 36)
    psh.caption(c, "of Fate", 24, 150 + 54 * 1.9 + 36 * 1.9, 36)
    return surf


O = {}


def main(out):
    orig = cairo.ImageSurface
    cairo.ImageSurface = m._Hi(orig)
    try:
        pic = picture()
    finally:
        cairo.ImageSurface = orig
    pic.write_to_png(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "../office-noir-2/on2_cover_v1.png")
