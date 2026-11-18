"""Cover for "The First Client" (The Onboarding, animation v18), 1080x1920, drawn natively at 1080 with the film's own
kit (ob_anim). Inside the centre the profile grids crop to (y 120-840 at the 540x960 drawing scale): the Client,
close, wearing OUR FIRST CLIENT round his neck where it fell on him, a ficus leaf on his head, not amused, saying his
line; behind him the office wall with the UptimeZ mark and the edge of the glass door. The title is a banner over him.
Usage: python3 thumb_ob.py out.png"""
import sys
import cairo
import kit
import brand
import ob_anim as a
import client_ob as co
from kit import Ctx, INK

W, H = 540, 960


def bubble(c, text, x, y, tip, size=34):
    c.select_font_face(kit.FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL); c.set_font_size(size)
    rows = text.split("\n")
    w = max(c.text_extents(r).x_advance for r in rows) + 44
    h = len(rows) * size * 1.14 + 26
    for fill in (False, True):
        c.new_path(); r = 18
        c.arc(x + r, y + r, r, 3.1416, 4.712); c.arc(x + w - r, y + r, r, 4.712, 6.283)
        c.arc(x + w - r, y + h - r, r, 0, 1.571); c.arc(x + r, y + h - r, r, 1.571, 3.1416); c.close_path()
        bx = min(max(tip[0], x + 40), x + w - 40)
        c.move_to(bx - 14, y + h); c.line_to(*tip); c.line_to(bx + 14, y + h); c.close_path()
        if fill:
            c.set_source_rgb(1, 1, 1); c.fill()
        else:
            c.set_source_rgb(*INK); c.set_line_width(7); c.set_line_join(1); c.stroke()
    c.set_source_rgb(*INK)
    for i, r_ in enumerate(rows):
        c.move_to(x + 22, y + 13 + size * 0.86 + i * size * 1.14); c.show_text(r_)


def bubble_r(c, text, x, y, tip, size=32):
    """A bubble to the right of his face, its tail coming in from its left edge to his cheek beside the mouth."""
    c.select_font_face(kit.FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL); c.set_font_size(size)
    rows = text.split("\n")
    w = max(c.text_extents(r).x_advance for r in rows) + 40
    h = len(rows) * size * 1.14 + 24
    for fill in (False, True):
        c.new_path(); r = 18
        c.arc(x + r, y + r, r, 3.1416, 4.712); c.arc(x + w - r, y + r, r, 4.712, 6.283)
        c.arc(x + w - r, y + h - r, r, 0, 1.571); c.arc(x + r, y + h - r, r, 1.571, 3.1416); c.close_path()
        ty = min(max(tip[1], y + 16), y + h - 16)
        c.move_to(x + 2, ty - 12); c.line_to(*tip); c.line_to(x + 2, ty + 12); c.close_path()
        if fill:
            c.set_source_rgb(1, 1, 1); c.fill()
        else:
            c.set_source_rgb(*INK); c.set_line_width(7); c.set_line_join(1); c.stroke()
    c.set_source_rgb(*INK)
    for i, r_ in enumerate(rows):
        c.move_to(x + 20, y + 12 + size * 0.86 + i * size * 1.14); c.show_text(r_)


def banner(c, text):
    c.save(); c.translate(270, 150); c.rotate(-0.025)
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(50)
    e = c.text_extents(text); w = e.x_advance + 60
    c.set_source_rgba(0, 0, 0, 0.25); c.rectangle(-w / 2 + 6, -42 + 6, w, 84); c.fill()
    c.set_source_rgb(*brand.NAVY); c.rectangle(-w / 2, -42, w, 84); c.fill()
    c.set_source_rgb(*brand.GREEN); c.rectangle(-w / 2, 30, w, 12); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(4); c.rectangle(-w / 2, -42, w, 84); c.stroke()
    c.set_source_rgb(1, 1, 1); c.move_to(-e.x_advance / 2, 14); c.show_text(text)
    c.restore()


def main(out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 2 * W, 2 * H)
    c = cairo.Context(surf)
    c.scale(2, 2)
    m = c.get_matrix(); m.invert(); a.BASE[0] = m; a.PX[0] = 2.0
    a.CUR.update(t=4.0, tl=0.6, d=1.9, u=0.3, shot="1.3", n=48)
    k = Ctx(c, 0)
    a.wall(k)
    g = cairo.RadialGradient(300, 420, 40, 300, 420, 520)                # the office's light, behind him
    g.add_color_stop_rgba(0, 1, 0.97, 0.88, 0.35); g.add_color_stop_rgba(1, 1, 0.97, 0.88, 0)
    c.set_source(g); c.paint()
    c.set_source_rgb(0.62, 0.64, 0.66); c.rectangle(-10, 0, 46, H); c.fill()                # the glass door's edge
    c.set_source_rgb(*INK); c.set_line_width(3); c.move_to(36, 0); c.line_to(36, H); c.stroke()
    brand.mark(c, 418, 236, 92, zzz=False)
    hx, hy, s = 236, 430, 1.8
    pose = co.POSES["arrive"][:2] + co.POSES["open"][2:]
    a.client(k, hx, hy, s, pose, "plain", (0.7, 0.05), roll=False, mouth="E")
    sc = s / 0.66
    a.hung(k, hx + 4 * s + 1, hy + 52 * s, 0.7 * sc, 0.03)                  # OUR FIRST CLIENT, round his neck
    a.leaf(k, hx + 6, hy - 56 * s, 1.6 * sc, 0.4)                           # and the leaf
    bubble_r(c, "Hi. I'd like\nto sign up.", 352, 436, (hx + 48.6, hy + 54))
    banner(c, "THE FIRST CLIENT")
    surf.write_to_png(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "../the-onboarding/ob_cover_v1.png")
