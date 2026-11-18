"""v3 (18 Nov): TONE = "v3", opt-in: true blacks like v2, but faces lighter (gamma 0.88). engine_on_v2.py is pinned.
Office Noir engine, v2 (engine_on_v1.py = v1, kept). v2 after the review ("a grey-coloured character, not
black-and-white film"): TONE = "v2" is a harder curve with true blacks (luma under 0.10 goes to black) and
faces pulled down toward mid-grey (gamma 1.6); TONE = "v1" keeps the old curve. side_light() darkens a frame
or a box from one side, the stand-in for the light pass until the sets have their own lights.
v1 notes: engine_v.py and engine_hd.py are untouched; only this episode uses it.
Differences from engine_v / engine_hd:
- DRAW_FPS (15 by default) sets the drawing grid: at 30 fps output every drawing is held exactly 2 frames
  (12 fps gave an uneven 2-3-2-3 cadence). DRAW_FPS = 12 reproduces the old grid.
- The panel push runs on the unquantised time, so it moves every output frame instead of stepping with the
  drawings. SMOOTH_PUSH = False restores the old stepped push.
- Optional accent pass (mod.NOIR = True): the frame is turned to greyscale with a tuned curve, and pixels whose
  colour matches one of mod.ACCENTS (exact key colours, +-KEY_TOL) are kept in colour at that accent's
  saturation. Whatever is drawn in front of an accent simply overwrites its pixels, so occlusion is free.
  The panel can opt out with mod.COLOUR_PANELS (names of panel functions drawn in full colour, e.g. reality).
- Optional mod.light(k, t, tl, name): a light pass drawn after the accent pass and before the grain, so the
  accents sit in the same light as everything else.
Usage: python3 engine_on.py MOD [--hd]           -> raw BGRA frames to stdout
       python3 engine_on.py MOD [--hd] 0 60 ...   -> PNG stills"""
import importlib
import math
import sys
import cairo
import numpy as np
from kit import Ctx, W, H, grain

FPS = 30
DRAW_FPS = 15
SMOOTH_PUSH = True
KEY_TOL = 4 / 255.0


def grid_t(f):
    """Time snapped to the drawing grid."""
    return math.floor(f / FPS * DRAW_FPS + 1e-9) / DRAW_FPS


def push_at(f, t0, t1):
    tq = (f / FPS) if SMOOTH_PUSH else grid_t(f)
    return 1 + 0.03 * ((tq - t0) / (t1 - t0))


TONE = "v2"


def grey_curve(y):
    """Noir tone curve on luma 0..1. v1: deeper blacks, faces kept light. v2: true blacks, faces mid-grey."""
    if TONE == "v3":                                       # v3, opt-in (Office Noir 2 look): true blacks, faces lighter
        y = np.clip((y - 0.09) / 0.85, 0, 1)
        return y ** 0.88
    if TONE == "v1":
        y = np.clip((y - 0.06) / 0.88, 0, 1)
        return y * y * (3 - 2 * y) * 0.92 + y * 0.08
    y = np.clip((y - 0.10) / 0.84, 0, 1)
    return y ** 1.6


def side_light(c, x, y, w, h, from_left=True, amount=0.6):
    """Hard side light: dark on the far side, a short soft edge in the middle."""
    g = cairo.LinearGradient(x, 0, x + w, 0)
    a0, a1 = (0.0, amount) if from_left else (amount, 0.0)
    g.add_color_stop_rgba(0.0, 0, 0, 0, a0); g.add_color_stop_rgba(0.42, 0, 0, 0, a0 * 0.9 + a1 * 0.1)
    g.add_color_stop_rgba(0.62, 0, 0, 0, a0 * 0.1 + a1 * 0.9); g.add_color_stop_rgba(1.0, 0, 0, 0, a1)
    c.save(); c.set_source(g); c.rectangle(x, y, w, h); c.fill(); c.restore()


def accent_pass(surf, accents):
    """accents: list of (rgb 0..1, saturation 0..1). Greyscale everywhere except the key colours."""
    surf.flush()
    h, w = surf.get_height(), surf.get_width()
    buf = np.ndarray((h, w, 4), np.uint8, surf.get_data())
    bgr = buf[..., :3].astype(np.float32) / 255.0
    r, g, b = bgr[..., 2], bgr[..., 1], bgr[..., 0]
    yv = grey_curve(0.2126 * r + 0.7152 * g + 0.0722 * b)
    out = np.stack([yv, yv, yv], -1)                      # B, G, R
    for (col, sat) in accents:
        m = (np.abs(r - col[0]) <= KEY_TOL) & (np.abs(g - col[1]) <= KEY_TOL) & (np.abs(b - col[2]) <= KEY_TOL)
        if m.any():
            orig = bgr[m]
            out[m] = yv[m][:, None] + (orig - yv[m][:, None]) * sat
    buf[..., :3] = np.clip(out * 255 + 0.5, 0, 255).astype(np.uint8)
    surf.mark_dirty()


def render(mod, f, surf, scale=1):
    t = grid_t(f)
    mod.RAW_T = f / FPS
    boil = int(t * DRAW_FPS) % 3
    c = cairo.Context(surf)
    c.set_source_rgb(1, 1, 1)
    c.paint()
    c.scale(scale, scale)
    k = Ctx(c, boil)
    for (t0, t1, fn) in mod.PANELS:
        if t0 <= f / FPS < t1:
            tl = t - t0
            c.save()
            push = push_at(f, t0, t1)
            sh = mod.shake(f / FPS) if hasattr(mod, "shake") else 0
            c.translate(W / 2, H / 2 + sh)
            c.scale(push, push)
            c.translate(-W / 2, -H / 2)
            fn(k, t, tl)
            c.restore()
            if getattr(mod, "NOIR", False) and fn.__name__ not in getattr(mod, "COLOUR_PANELS", ()):
                accent_pass(surf, getattr(mod, "ACCENTS", []))
            if hasattr(mod, "light"):
                mod.light(k, t, tl, fn.__name__)
            if hasattr(mod, "overlay"):
                mod.overlay(k, t, tl, fn.__name__)
            break
    grain(k, 0.06)


if __name__ == "__main__":
    args = sys.argv[1:]
    hd = "--hd" in args
    args = [a for a in args if a != "--hd"]
    scale = 2 if hd else 1
    mod = importlib.import_module(args[0])
    n = int(round(getattr(mod, "DURATION", 15.0) * FPS))
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W * scale, H * scale)
    if len(args) > 1:
        for fr in args[1:]:
            render(mod, int(fr), surf, scale)
            surf.write_to_png(f"{args[0]}_{int(fr):03d}.png")
    else:
        out = sys.stdout.buffer
        for fr in range(n):
            render(mod, fr, surf, scale)
            surf.flush()
            out.write(bytes(surf.get_data()))
