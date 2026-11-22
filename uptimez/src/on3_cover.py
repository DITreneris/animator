"""OFFICE NOIR 3: the cover (thumbnail), v1 (21 Nov). 1080 x 1920. The last round's punch as it lands (7.2), lit as the
film is; the title on the film's own cream typewriter cards, at the top under the bar and clear of the apps' controls.
A draft: the picture is the 540 film frame scaled up twice (the film itself is not yet rendered at 1080).
  python3 on3_cover.py -> ../office-noir-3/on3_cover_v1.png"""
import cairo
import film_on3 as f


def build(out="../office-noir-3/on3_cover_v1.png", shot="7.2", t=1.0):
    D = dict((a, c_) for a, b_, c_ in f.FILM)
    fr = D[shot](t)
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, 1080, 1920); c = cairo.Context(s)
    c.save(); c.scale(2, 2); c.set_source_surface(fr, 0, 0); c.get_source().set_filter(cairo.FILTER_BEST); c.paint(); c.restore()
    g = cairo.LinearGradient(0, 0, 0, 760)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.82); g.add_color_stop_rgba(0.6, 0, 0, 0, 0.35); g.add_color_stop_rgba(1, 0, 0, 0, 0.0)
    c.set_source(g); c.rectangle(0, 0, 1080, 760); c.fill()
    c.select_font_face("Special Elite", 0, 0)
    y = 210
    for text, size in (("OFFICE NOIR 3", 104), ("THE LAST ROUND", 78)):
        c.set_font_size(size); e = c.text_extents(text); w, h = e.x_advance + 56, size * 1.32
        c.set_source_rgba(0, 0, 0, 0.5); c.rectangle(48, y + 8, w, h); c.fill()
        c.set_source_rgb(0.93, 0.90, 0.82); c.rectangle(40, y, w, h); c.fill()
        c.set_source_rgb(0.06, 0.06, 0.07); c.set_line_width(6); c.rectangle(40, y, w, h); c.stroke()
        c.move_to(68, y + size * 0.98); c.show_text(text); y += h + 18
    c.set_font_size(44); c.set_source_rgb(0.93, 0.90, 0.82); c.move_to(44, y + 46); c.show_text("HUMAN vs ROBOT")
    s.write_to_png(out)


if __name__ == "__main__":
    build()
