"""6.1 Don's hands (phone review 25 Nov): three gestures, colour + black silhouette of Don alone, feed size."""
import sys, cairo
sys.path.insert(0, "/home/claude/animator/uptimez/src")
import ps_scenes as ps
from kit import Ctx
ps.gags_v5()
V = [("vest", ("tuck", "tuck")), ("thumbs", None), ("balance", None)]
sh = [x for x in ps.SHOTS if x["id"] == "6.1"][0] if hasattr(ps, "SHOTS") else None
def frame(v, don=True):
    ps.DON_61[0] = v
    old = ps.fg_61
    s = dict(sh)
    if not don: s["fg"] = lambda k: {"don": (0, 0, 1)}
    return ps.render(s)[0]
cols, sils = [], []
for v in V:
    a, b = frame(v), frame(v, False)
    a.flush(); b.flush(); A, B = a.get_data(), bytes(b.get_data())
    m = cairo.ImageSurface(cairo.FORMAT_RGB24, a.get_width(), a.get_height()); d = m.get_data()
    for i in range(0, len(B), 4):
        x = 0 if abs(A[i]-B[i]) + abs(A[i+1]-B[i+1]) + abs(A[i+2]-B[i+2]) > 24 else 255
        d[i] = d[i+1] = d[i+2] = x
    m.mark_dirty(); cols.append(a); sils.append(m)
for name, tiles in (("col", cols), ("sil", sils)):
    o = cairo.ImageSurface(cairo.FORMAT_RGB24, 3 * 280 + 10, 500); c = cairo.Context(o); c.set_source_rgb(.55, .55, .55); c.paint()
    for j, im in enumerate(tiles):
        c.save(); c.translate(10 + j * 280, 10); c.scale(0.5, 0.5); c.set_source_surface(im, 0, 0); c.paint(); c.restore()
        c.set_source_rgb(0, 0, 0); c.set_font_size(18); c.move_to(14 + j * 280, 496); c.show_text(str(j + 1))
    o.write_to_png(f"/tmp/d61_{name}.png")
