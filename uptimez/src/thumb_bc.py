"""Cover for "The Best Candidate" (animation v4.1), 1080x1920, drawn natively at 1080 with the film's own renderer
(bc_anim4 over bc_anim). The picture is the film's own drawing at 78.6 s, the moment both cold viewers said they would
screenshot: Mom scrubbing the stain on Don's vest, his VISITOR badge re-lettered HEAD OF TALENT, under WE HIRE ON
MERIT. Added for the cover: her line as a bubble on the bare wall to the right of the poster (tail to her crown) and
the title as a banner under the scrubbing hand. Everything that must be read sits inside the centre the profile grids crop to (y 120-840 at the 540x960
drawing scale).
Usage: python3 thumb_bc.py [out.png]"""
import sys
import cairo
import kit
import brand
from kit import INK
import bc_anim4 as V

A = V.A
W, H = 540, 960
T_KEY = 78.6


def bubble(c, text, x, y, tip, size=38):
    c.select_font_face(kit.FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL); c.set_font_size(size)
    rows = text.split("\n")
    w = max(c.text_extents(r).x_advance for r in rows) + 44
    h = len(rows) * size * 1.14 + 26
    for fill in (False, True):
        c.new_path(); r = 18
        c.arc(x + r, y + r, r, 3.1416, 4.712); c.arc(x + w - r, y + r, r, 4.712, 6.283)
        c.arc(x + w - r, y + h - r, r, 0, 1.571); c.arc(x + r, y + h - r, r, 1.571, 3.1416); c.close_path()
        if tip[0] < x:                                     # the speaker is to the left: the tail leaves the left edge
            ty = y + h * 0.62
            c.move_to(x + 2, ty - 13); c.line_to(*tip); c.line_to(x + 2, ty + 13); c.close_path()
        else:
            bx = min(max(tip[0], x + 40), x + w - 40)
            c.move_to(bx - 14, y + h - 2); c.line_to(*tip); c.line_to(bx + 14, y + h - 2); c.close_path()
        if fill:
            c.set_source_rgb(1, 1, 1); c.fill()
        else:
            c.set_source_rgb(*INK); c.set_line_width(7); c.set_line_join(1); c.stroke()
    c.set_source_rgb(*INK)
    for i, r_ in enumerate(rows):
        e = c.text_extents(r_)
        c.move_to(x + (w - e.x_advance) / 2, y + 13 + size * 0.86 + i * size * 1.14); c.show_text(r_)


def banner(c, text, y):
    c.save(); c.translate(270, y); c.rotate(-0.025)
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(44)
    e = c.text_extents(text); w = e.x_advance + 44
    c.set_source_rgba(0, 0, 0, 0.25); c.rectangle(-w / 2 + 6, -42 + 6, w, 84); c.fill()
    c.set_source_rgb(*brand.NAVY); c.rectangle(-w / 2, -42, w, 84); c.fill()
    c.set_source_rgb(*brand.GREEN); c.rectangle(-w / 2, 30, w, 12); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(4); c.rectangle(-w / 2, -42, w, 84); c.stroke()
    c.set_source_rgb(1, 1, 1); c.move_to(-e.x_advance / 2, 12); c.show_text(text)
    c.restore()


VARIANTS = {            # name: (film time, the title's y, an added bubble or None)
    "a_shout": (76.8, 792, None),                       # she shouts it, a hand on her hip; he sweats (the film's bubble)
    "b_lick": (75.6, 176, None),                        # the lick, close: what is she about to do?
    "c_scrub": (78.0, 812, None),                       # the scrub, close: her hand on the stain, his badge, his face
}


def variant(name, out):
    t, by, bub = VARIANTS[name]
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 2 * W, 2 * H)
    c = cairo.Context(surf)
    A.draw(c, t, w=2 * W, last=True)
    if name == "a_shout":                                  # 28 px lower, so the grid crop keeps WE HIRE whole (the
        c.identity_matrix(); c.reset_clip()                # strip left at the top is the first drawing's bare wall)
        A.draw(c, t, w=2 * W, y=56, last=True)
    c.identity_matrix(); c.reset_clip(); c.scale(2, 2)
    if bub:
        bubble(c, *bub)
    banner(c, "THE BEST CANDIDATE", by)
    surf.write_to_png(out)
    print("wrote", out)


def main(out):
    A.load_pushes()
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 2 * W, 2 * H)
    c = cairo.Context(surf)
    A.draw(c, T_KEY, w=2 * W, last=True)
    c.identity_matrix(); c.reset_clip(); c.scale(2, 2)
    bubble(c, "DONNIE!\nYour vest!", 322, 300, (236, 412), size=32)
    banner(c, "THE BEST CANDIDATE", 786)
    surf.write_to_png(out)
    print("wrote", out)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "v2":          # the director's pick: A, the shout
        A.load_pushes()
        variant("a_shout", sys.argv[2] if len(sys.argv) > 2 else "../the-best-candidate/bc_cover_v2.png")
        sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] == "variants":
        A.load_pushes()
        for n_ in VARIANTS:
            variant(n_, "%s/bc_cover_v2_%s.png" % (sys.argv[2], n_))
        sys.exit(0)
    main(sys.argv[1] if len(sys.argv) > 1 else "../the-best-candidate/bc_cover_v1.png")
