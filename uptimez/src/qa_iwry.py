"""QA for the "I Will Replace You" storyboard: renders frames with and without bubbles and measures how much
of each visible face (head disc, 85% radius, in screen space) the bubbles change. Any change = a bubble or
tail over a face. Usage: python3 qa_iwry.py iwry_sb [step]"""
import sys
import importlib
import numpy as np
import cairo
import engine_v
import iwry_common as ic

mod = importlib.import_module(sys.argv[1])
step = int(sys.argv[2]) if len(sys.argv) > 2 else 4
surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960)
yy, xx = np.mgrid[0:960, 0:540]
bad = []
n = int(mod.DURATION * 30)
for f in range(0, n, step):
    ic.NO_BUBBLES = False
    engine_v.render(mod, f, surf)
    a = np.frombuffer(bytes(surf.get_data()), np.uint8).reshape(960, 540, 4)[:, :, :3].astype(int)
    out, cam = ic.LAST["out"], ic.LAST["cam"]
    ic.NO_BUBBLES = True
    engine_v.render(mod, f, surf)
    b = np.frombuffer(bytes(surf.get_data()), np.uint8).reshape(960, 540, 4)[:, :, :3].astype(int)
    d = np.abs(a - b).sum(axis=2) > 40
    for who in ("sof", "don", "robot"):
        if who not in out:
            continue
        hx, hy = ic.to_screen(out[who]["head"], cam)
        r = 50 * cam[2] * 0.85 * 1.03
        mask = (xx - hx) ** 2 + (yy - hy) ** 2 < r * r
        if mask.sum() == 0:
            continue
        frac = (d & mask).sum() / mask.sum()
        if frac > 0.01:
            bad.append((round(f / 30, 2), who, round(frac * 100, 1)))
ic.NO_BUBBLES = False
print(f"checked {len(range(0, n, step))} frames; bubble-over-face hits: {len(bad)}")
for x in bad[:40]:
    print("  t=%ss %s face covered %s%%" % x)
