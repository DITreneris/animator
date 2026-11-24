"""OFFICE NOIR 3: the cover, v3 (23 Nov). Tomas, comparing it with the house style of Office Noir and Office Noir 2
(thumb_on.py, thumb_on2.py): "palygink cover 1 cover 2 [...] kodel skiriasi" -- v1 and v2 of this cover were a raw
film frame with a flat dark gradient and three stacked cards (series, title, subtitle); the other two covers never
work that way: one small series label plus one headline card (lesson 46), and the noir light kit on top -- blinds,
a key light on the thing the shot is about, a vignette (lesson 50, "Noir is light, not grey").

v3 keeps v2's picture (shot 7.2 at the moment of contact, cropped and enlarged 20% -- both from the "what
correlates" triage) and puts the house lighting and typography on it instead of the ad hoc ones:
  - on_set.blinds across the whole frame, a key light on the punch's point of contact, on_set.vignette.
  - one small label card, "OFFICE NOIR 3", and one headline card, "THE LAST ROUND" (props_sheet_on.caption, the
    same card function and typeface the other two covers use). "HUMAN vs ROBOT" is dropped: the picture is the
    answer (lesson 46).
v1 is pinned at on3_cover.py / on3_cover_v1.png; v2 at on3_cover_v2.py / on3_cover_v2.png.
python3 on3_cover_v3.py -> ../office-noir-3/on3_cover_v3.png"""
import cairo
import film_on3 as f
import on_set as st
import props_sheet_on as psh


def build(out="../office-noir-3/on3_cover_v3.png", shot="7.2", t=0.58, y0=50, y1=850):
    D = dict((a, c_) for a, b_, c_ in f.FILM)
    fr = D[shot](t)
    pic = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960)
    c = cairo.Context(pic)
    c.save(); c.scale(960.0 / (y1 - y0), 960.0 / (y1 - y0))
    c.set_source_surface(fr, 0, -y0); c.get_source().set_filter(cairo.FILTER_BEST); c.paint(); c.restore()

    # the house noir light kit (thumb_on.py, thumb_on2.py), not the ad hoc dark gradient v1/v2 used
    st.blinds(c, -20, -20, 580, 1000, angle=-0.30, gap=30, band=11, amount=0.22)
    cx, cy = (330 - 0) * (960.0 / (y1 - y0)), (505 - y0) * (960.0 / (y1 - y0))   # the punch's point of contact
    st.key_light(c, cx, cy, 190, 0.30)
    st.vignette(c, 0.38)

    s = cairo.ImageSurface(cairo.FORMAT_RGB24, 1080, 1920); cs = cairo.Context(s)
    cs.scale(2, 2); cs.set_source_surface(pic, 0, 0); cs.get_source().set_filter(cairo.FILTER_BEST); cs.paint()
    psh.caption(cs, "OFFICE NOIR 3", 52, 108, 24)                   # the series, small (as in thumb_on2.py)
    psh.caption(cs, "THE LAST ROUND", 52, 158, 46)                  # the one headline
    s.write_to_png(out)


if __name__ == "__main__":
    build()
