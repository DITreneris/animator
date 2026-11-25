import sys, cairo
sys.path.insert(0, "/home/claude/animator/uptimez/src")
import ps_scenes as ps
ps.FIX_V4[0] = True; ps.pss.NO_DOOR_CONFETTI[0] = ps.rp.SUN_UP[0] = True
ps.sp.CV_WORD[0] = "HR?"; ps.GAGS_V5[0] = True
by = {s["id"]: s for s in ps.SHOTS}
tiles = []
for sid in ("5.2", "5.5", "5.6", "6.1"):
    surf, msgs = ps.render(by[sid]); tiles.append(surf); print(sid, [x[:80] for x in msgs]); surf.write_to_png("/tmp/gags/A_%s.png" % sid)
out = cairo.ImageSurface(cairo.FORMAT_RGB24, len(tiles) * 280 + 10, 500); c = cairo.Context(out); c.set_source_rgb(.15, .15, .16); c.paint()
for j, im in enumerate(tiles):
    c.save(); c.translate(10 + j * 280, 10); c.scale(0.5, 0.5); c.set_source_surface(im, 0, 0); c.paint(); c.restore()
out.write_to_png("/tmp/gags/A.png")
