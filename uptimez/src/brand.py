"""UptimeZ Inc. brand marks, drawn with cairo so the same code feeds the logo files and the videos.
Mark: a navy rounded square; a green uptime pulse line whose last spike becomes a Z; a tiny 'zzz'."""
import math
import cairo

NAVY = (0x1F / 255, 0x2A / 255, 0x44 / 255)
GREEN = (0x2B / 255, 0xB6 / 255, 0x73 / 255)
PAPER = (1, 1, 1)
CORP = "Inter"
TAGLINE = "99.9% uptime. 0% findability."


def _rrect(c, x, y, w, h, r):
    c.new_sub_path()
    c.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    c.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    c.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    c.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2)
    c.close_path()


def mark(c, x, y, s, zzz=True, bg=NAVY, fg=GREEN):
    """Square mark of size s at (x, y)."""
    _rrect(c, x, y, s, s, s * 0.22)
    c.set_source_rgb(*bg)
    c.fill()
    u = s / 100.0
    # pulse: flat, small blip, big spike, then the Z (top bar, diagonal, bottom bar)
    pts = [(12, 58), (26, 58), (31, 50), (36, 64), (41, 58), (47, 58), (53, 26), (59, 72), (63, 58),
           (66, 58), (66, 40), (86, 40), (66, 70), (88, 70)]
    c.set_line_width(7.5 * u)
    c.set_line_join(cairo.LINE_JOIN_ROUND)
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.move_to(x + pts[0][0] * u, y + pts[0][1] * u)
    for px, py in pts[1:]:
        c.line_to(x + px * u, y + py * u)
    c.set_source_rgb(*fg)
    c.stroke()
    if zzz:
        c.select_font_face(CORP, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        for i, (zx, zy, zs) in enumerate([(78, 30, 9), (85, 22, 7), (90, 15, 5.5)]):
            c.set_font_size(zs * u * 1.6)
            c.move_to(x + zx * u, y + zy * u)
            c.set_source_rgba(*fg, 0.9 - i * 0.2)
            c.show_text("z")


def wordmark(c, x, y, size, ink=NAVY, z=GREEN):
    """'UPTIMEZ INC.' with the Z in green. (x, y) = left baseline. Returns width."""
    c.select_font_face(CORP, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    c.set_font_size(size)
    parts = [("UPTIME", ink), ("Z", z), (" INC.", ink)]
    cx = x
    for txt, col in parts:
        c.move_to(cx, y)
        c.set_source_rgb(*col)
        c.show_text(txt)
        cx += c.text_extents(txt).x_advance
    return cx - x


def lockup(c, x, y, h, ink=NAVY, tagline=False, tag_ink=None, mark_bg=NAVY):
    """Horizontal lockup: mark + wordmark (+ tagline under the wordmark)."""
    mark(c, x, y, h, bg=mark_bg)
    size = h * 0.42
    w = wordmark(c, x + h * 1.22, y + h * (0.56 if tagline else 0.66), size, ink=ink)
    if tagline:
        c.select_font_face(CORP, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        c.set_font_size(size * 0.42)
        c.move_to(x + h * 1.22, y + h * 0.9)
        c.set_source_rgb(*(tag_ink or ink))
        c.show_text(TAGLINE)
    return h * 1.22 + w


if __name__ == "__main__":
    import os
    import os as _os
    out = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "brand")
    os.makedirs(out, exist_ok=True)
    # mark only
    for ext in ("svg", "png"):
        S = 512
        surf = cairo.SVGSurface(f"{out}/uptimez-mark.svg", S, S) if ext == "svg" else cairo.ImageSurface(cairo.FORMAT_ARGB32, S, S)
        c = cairo.Context(surf)
        mark(c, 0, 0, S)
        if ext == "png":
            surf.write_to_png(f"{out}/uptimez-mark.png")
        surf.finish()
    # horizontal lockups: on light and on navy
    for name, bg, ink, tag in (("uptimez-lockup-light", (1, 1, 1), NAVY, False),
                               ("uptimez-lockup-dark", NAVY, (1, 1, 1), False),
                               ("uptimez-lockup-tagline", (1, 1, 1), NAVY, True)):
        Wd, Hd = 1400, 360
        for ext in ("svg", "png"):
            surf = cairo.SVGSurface(f"{out}/{name}.svg", Wd, Hd) if ext == "svg" else cairo.ImageSurface(cairo.FORMAT_ARGB32, Wd, Hd)
            c = cairo.Context(surf)
            c.set_source_rgb(*bg); c.paint()
            lockup(c, 60, 60, 240, ink=ink, tagline=tag, tag_ink=(0.35, 0.4, 0.5), mark_bg=NAVY if bg != NAVY else (0.17, 0.24, 0.38))
            if ext == "png":
                surf.write_to_png(f"{out}/{name}.png")
            surf.finish()
    print("ok", sorted(os.listdir(out)))
