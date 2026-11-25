"""OFFICE NOIR 3: the cover (thumbnail), v2 (23 Nov), from a triage of v1 ("what correlates?"):
  - the punch is shown at contact (shot 7.2, t=0.58, where the hit-stop and impact burst already land on the robot's
    shoulder) instead of t=1.0, where the glove had already pulled back clear of him.
  - the frame is cropped top and bottom (the dark window strip, the empty floor) and scaled back up 20%, so both
    figures read bigger without cutting either of them; the "HR" badge was left alone (Tomas: "nereikia to HR").
  v1 is pinned at on3_cover.py / on3_cover_v1.png.
  python3 on3_cover_v2.py -> ../office-noir-3/on3_cover_v2.png"""
import cairo
import film_on3 as f


def build(out="../office-noir-3/on3_cover_v2.png", shot="7.2", t=0.58, y0=50, y1=850):
    D = dict((a, c_) for a, b_, c_ in f.FILM)
    fr = D[shot](t)
    cropped = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960)
    cc = cairo.Context(cropped)
    cc.save(); cc.scale(960.0 / (y1 - y0), 960.0 / (y1 - y0))
    cc.set_source_surface(fr, 0, -y0); cc.get_source().set_filter(cairo.FILTER_BEST); cc.paint(); cc.restore()

    s = cairo.ImageSurface(cairo.FORMAT_RGB24, 1080, 1920); c = cairo.Context(s)
    c.save(); c.scale(2, 2); c.set_source_surface(cropped, 0, 0); c.get_source().set_filter(cairo.FILTER_BEST); c.paint(); c.restore()
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
    # v2: a third card in the same cream (not a solid black box -- Tomas, 23 Nov: "too dark"; a black slab under two
    # cream cards was new weight the cover didn't carry before). The tighter crop put "10 GARAGES" right behind it,
    # which is why it needed a card at all.
    text, size = "HUMAN vs ROBOT", 44
    c.set_font_size(size); e = c.text_extents(text); w, h = e.x_advance + 40, size * 1.32
    c.set_source_rgba(0, 0, 0, 0.5); c.rectangle(48, y + 8, w, h); c.fill()
    c.set_source_rgb(0.93, 0.90, 0.82); c.rectangle(40, y, w, h); c.fill()
    c.set_source_rgb(0.06, 0.06, 0.07); c.set_line_width(5); c.rectangle(40, y, w, h); c.stroke()
    c.move_to(60, y + size * 0.98); c.show_text(text)
    s.write_to_png(out)


if __name__ == "__main__":
    build()
