import sys, cairo
import dh_anim1 as A, dh_scenes as ds
which = sys.argv[1]
if which == "v7":
    import dh_anim3 as M
    A.bubble = lambda *a, **k: None; M.A.bubble = A.bubble
    fr = M.frame
else:
    import dh_anim3_v8 as M
    M.NOBUB[0] = True; fr = M.frame
ds.ARM_PHONE[0] = True
def sheet(ts, out, cols, W=180):
    H = int(W * 16 / 9); rows = (len(ts) + cols - 1) // cols
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, cols * W, rows * (H + 18)); c = cairo.Context(s); c.set_source_rgb(1,1,1); c.paint()
    for i, tt in enumerate(ts):
        surf, _ = fr(tt, int(round(tt * 12)), 1)
        x, y = (i % cols) * W, (i // cols) * (H + 18)
        c.save(); c.translate(x, y + 18); c.scale(W / 540.0, H / 960.0); c.set_source_surface(surf, 0, 0); c.paint(); c.restore()
        c.set_source_rgb(0,0,0); c.set_font_size(12); c.move_to(x + 4, y + 13); c.show_text("%d  %.2f s" % (i + 1, tt))
    s.write_to_png(out)
T = M.TOTAL
sheet([i * 0.25 for i in range(int(T / 0.25))], "/tmp/cold/%s_4fps.png" % which, 12)
t0 = M.T0["4.2"]
sheet([t0 + i / 8.0 for i in range(8)], "/tmp/cold/%s_8fps_jump.png" % which, 8, 270)
