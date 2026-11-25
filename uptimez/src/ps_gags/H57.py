"""5.7 Pam's hand on her phone and 6.1 Pam's reach (review 25 Nov): three variants each, colour + black silhouette."""
import sys, cairo
sys.path.insert(0, "/home/claude/animator/uptimez/src")
import ps_scenes as ps
from kit import Ctx
ps.gags_v5()
W, H = ps.W, ps.H
def surf(fn):
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); fn(Ctx(cairo.Context(s), 0)); s.flush(); return s
def mask(a, b):
    A, B = a.get_data(), bytes(b.get_data())
    m = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); d = m.get_data()
    for i in range(0, len(B), 4):
        x = 0 if abs(A[i]-B[i]) + abs(A[i+1]-B[i+1]) + abs(A[i+2]-B[i+2]) > 24 else 255
        d[i] = d[i+1] = d[i+2] = x
    m.mark_dirty(); return m
def sheet(tiles, path):
    o = cairo.ImageSurface(cairo.FORMAT_RGB24, 3 * 280 + 10, 500); c = cairo.Context(o); c.set_source_rgb(.55, .55, .55); c.paint()
    for j, im in enumerate(tiles):
        c.save(); c.translate(10 + j * 280, 10); c.scale(0.5, 0.5); c.set_source_surface(im, 0, 0); c.paint(); c.restore()
        c.set_source_rgb(0, 0, 0); c.set_font_size(18); c.move_to(14 + j * 280, 496); c.show_text(str(j + 1))
    o.write_to_png(path)
# 5.7: the insert; the silhouette is hand + sleeve + phone over the bare table
bare = surf(lambda k: (k.c.set_source_rgb(0.55, 0.48, 0.40), k.c.paint()))
cols, sils = [], []
for v in ("grab", "held", "fist"):
    ps.H57[0] = v; a = surf(ps.ins_phone_57); cols.append(a); sils.append(mask(a, bare))
sheet(cols, "/tmp/h57_col.png"); sheet(sils, "/tmp/h57_sil.png")
# 6.1: Pam alone against the frame without her
sh = [x for x in ps.SHOTS if x["id"] == "6.1"][0]
cols, sils = [], []
for v in ("reach", "reach_up", "reach_pt"):
    ps.PAM_61[0] = v; a = ps.render(sh)[0]
    pam = ps.pam
    ps.pam = lambda k, *a_, **kw: ({"hands": [(0, 0), (0, 0)], "head": (0, 0)}, (0, 0, 1))
    b = ps.render(sh)[0]; ps.pam = pam
    a.flush(); b.flush(); cols.append(a); sils.append(mask(a, b))
sheet(cols, "/tmp/p61_col.png"); sheet(sils, "/tmp/p61_sil.png")
