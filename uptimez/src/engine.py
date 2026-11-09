"""Timed-slideshow engine: 15 s, 30 fps output, drawing updates at 12 fps (cutout cadence).
Usage: python3 engine.py s3            -> raw BGRA frames to stdout
       python3 engine.py s3 0 60 ...   -> PNG stills of those frames"""
import importlib
import math
import sys
import cairo
from kit import Ctx, W, H, grain

FPS, N = 30, 450


def render(mod, f, surf):
    t = math.floor(f / FPS * 12) / 12.0          # 12 fps step
    boil = int(t * 12) % 3
    c = cairo.Context(surf)
    c.set_source_rgb(1, 1, 1)
    c.paint()
    k = Ctx(c, boil)
    for (t0, t1, fn) in mod.PANELS:
        if t0 <= f / FPS < t1:
            tl = t - t0
            c.save()
            push = 1 + 0.03 * (tl / (t1 - t0))      # slow push-in so held panels breathe
            sh = mod.shake(t) if hasattr(mod, "shake") else 0
            c.translate(W / 2, H / 2 + sh)
            c.scale(push, push)
            c.translate(-W / 2, -H / 2)
            fn(k, t, tl)
            c.restore()
            if hasattr(mod, "overlay"):
                mod.overlay(k, t, tl, fn.__name__)
            break
    grain(k, 0.06)


if __name__ == "__main__":
    mod = importlib.import_module(sys.argv[1])
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    if len(sys.argv) > 2:
        for fr in sys.argv[2:]:
            render(mod, int(fr), surf)
            surf.write_to_png(f"{sys.argv[1]}_{int(fr):03d}.png")
    else:
        out = sys.stdout.buffer
        for fr in range(N):
            render(mod, fr, surf)
            surf.flush()
            out.write(bytes(surf.get_data()))
