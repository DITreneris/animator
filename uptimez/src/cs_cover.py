"""ONE STAR (episode 11): the cover, 1080 x 1920, from the master's own drawing (cs_film_v13 setup, HI=2).
The title at the top, under the apps' bar, clear of the bottom quarter and the right rail.
  python3 cs_cover.py [shot drawing] [out]   e.g.  python3 cs_cover.py 4.4 30 ../customer-success/one_star_cover_v1.png"""
import sys
import importlib
import cairo
import cs_film_v13 as v
import cs_scene1 as s1
import cs_props as cp


INSET = {"1.4b": (0.84, 560)}                              # (scale, top): the post whole below the title
CROP = {"1.4b": (40, 22, 500, 938)}                         # the phone body in the 540 frame


def frame(shot, d):
    for i in range(1, 7):
        m = importlib.import_module("cs_scene%d" % i)
        for n, nd, f in m.SHOTS:
            if n == shot:
                m.draw(f, 0)
                return m.draw(f, min(d, nd - 1))
    raise KeyError(shot)


def build(shot, d, out):
    v.setup(); s1.HI[0] = 2
    fr = frame(shot, d)
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, 1080, 1920); c = cairo.Context(s)
    if INSET.get(shot):                                                     # the picture smaller and lower, under the title
        sc, top = INSET[shot]
        c.set_source_rgb(0.10, 0.10, 0.12); c.paint()
        x0, y0, x1, y1 = CROP.get(shot, (0, 0, 540, 960))                  # only the phone, not the room's edge
        c.save(); c.translate((1080 - (x1 - x0) * 2 * sc) / 2, top); c.scale(2 * sc, 2 * sc)
        c.rectangle(0, 0, x1 - x0, y1 - y0); c.clip()
        c.set_source_surface(fr, -x0, -y0); c.paint(); c.restore()
    else:
        c.save(); c.scale(2, 2); c.set_source_surface(fr, 0, 0); c.paint(); c.restore()   # (its device scale is 2: lesson 162)
    g = cairo.LinearGradient(0, 0, 0, 640)
    g.add_color_stop_rgba(0, 0.05, 0.06, 0.08, 0.80); g.add_color_stop_rgba(0.7, 0.05, 0.06, 0.08, 0.30)
    g.add_color_stop_rgba(1, 0.05, 0.06, 0.08, 0.0)
    c.set_source(g); c.rectangle(0, 0, 1080, 640); c.fill()
    c.select_font_face("Inter", 0, 1)
    c.set_font_size(150); e = c.text_extents("ONE STAR")
    x = (1080 - e.x_advance) / 2; y = 300
    c.set_source_rgba(0, 0, 0, 0.55); c.move_to(x + 6, y + 6); c.show_text("ONE STAR")
    c.set_source_rgb(1, 1, 1); c.move_to(x, y); c.show_text("ONE STAR")
    for i in range(5):                                                    # the rating: one gold star, four empty
        cx, cy, r = 540 + (i - 2) * 112, 410, 44
        c.new_path()
        import math
        for j in range(10):
            a = -math.pi / 2 + j * math.pi / 5; rr = r if j % 2 == 0 else r * 0.45
            c.line_to(cx + rr * math.cos(a), cy + rr * math.sin(a))
        c.close_path()
        if i == 0:
            c.set_source_rgb(0.98, 0.78, 0.18); c.fill_preserve()
        c.set_source_rgb(1, 1, 1); c.set_line_width(5); c.stroke()
    c.set_font_size(40); t = "UptimeZ Inc. · episode 11"; e = c.text_extents(t)
    c.set_source_rgb(0.85, 0.88, 0.92); c.move_to((1080 - e.x_advance) / 2, 505); c.show_text(t)
    s.write_to_png(out)


if __name__ == "__main__":
    a = sys.argv[1:]
    build(a[0] if a else "4.4", int(a[1]) if len(a) > 1 else 30, a[2] if len(a) > 2 else "../customer-success/one_star_cover_v1.png")
