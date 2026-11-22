"""OFFICE NOIR 3 drawn at 1080x1920 (uptimez/CLAUDE.md: "Native 1080: render at 2x with set_device_scale(2,2), not an
upscale"). The film's modules make their own 540x960 surfaces in a hundred places and work on pixels in three; so,
before any of them is imported, every cairo.ImageSurface is made S times as large with a device scale of S: all drawing
stays in the same 540x960 units, and the pixel passes (the noir pass, the grain, two in film_on3) take their size from
the surface. Nothing in the 540 build changes: this file is the only place the scale is set.
  KOKORO_DIR=... python3 on3_native.py            -> ../office-noir-3/office_noir_3_release_v5_1080.mp4 and _540.mp4"""
import os
import subprocess
import sys
import cairo
import numpy as np

S = int(os.environ.get("ON3_SCALE", "2"))
_Real = cairo.ImageSurface


class _Scaled:
    def __new__(cls, fmt, w, h):
        s = _Real(fmt, int(w) * S, int(h) * S)
        s.set_device_scale(S, S)
        return s
    create_from_png = staticmethod(_Real.create_from_png)
    create_for_data = staticmethod(_Real.create_for_data)
    format_stride_for_width = staticmethod(_Real.format_stride_for_width)


if S != 1:
    cairo.ImageSurface = _Scaled
os.environ.setdefault("ON3_TP", "-2.0")
import light_on3 as li

_G = []


def _grain(surf, a=10.0, seed=0):
    """The same grain as at 540 (its four fields, each grain S pixels wide), on a surface of any size."""
    if not _G:
        rng = np.random.default_rng(3)
        _G.extend(np.repeat(np.repeat(rng.normal(0, 1, (li.H, li.W)).astype(np.float32), S, 0), S, 1) for _ in range(4))
    h, w = surf.get_height(), surf.get_width()
    buf = np.frombuffer(surf.get_data(), np.uint8).reshape(h, surf.get_stride() // 4, 4)
    n = (_G[seed % 4] * a)[:, :, None]
    lum = buf[:, :w, :3].astype(np.float32)
    red = (lum[:, :, 2:3] - lum[:, :, 1:2]) > 60
    buf[:, :w, :3] = np.clip(lum + np.where(red, 0, n), 0, 255).astype(np.uint8)
    surf.mark_dirty()


li._grain = _grain
import on3_animatic as an
import ring_rough_on3 as rr

_src = __import__("inspect").getsource(rr.render)
assert '"540x960"' in _src
exec(_src.replace('"540x960"', '"%dx%d"' % (540 * S, 960 * S)).replace('"-crf", "18"', '"-crf", "16"'), rr.__dict__)
an.V = "release_v5"
D = "../office-noir-3/"
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "frames":             # a few drawings, to compare with the 540 build
        import film_on3 as f
        F = {n: fn for n, d, fn in f.FILM}
        for n, t in (("1.1", 1.3), ("2.6", 1.5), ("3.4", 0.5), ("4.3b", 0.5), ("5.5", 1.5), ("7.2", 0.7), ("6.3", 2.6), ("8.3", 0.8)):
            s = F[n](t); print(n, s.get_width(), s.get_height()); s.write_to_png("/tmp/nat_%s_%d.png" % (n, S))
        sys.exit(0)
    out = D + "office_noir_3_release_v5_1080.mp4"
    total, held, lines = an.build(out)
    print("%.2f s" % total)
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", out, "-vf", "scale=540:960:flags=area,format=yuv420p", "-c:v", "libx264", "-crf", "27",
                           "-preset", "medium", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
                           "-movflags", "+faststart", "-c:a", "copy", D + "office_noir_3_release_v5_540.mp4"])
