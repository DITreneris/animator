"""Cover thumbnail for the Christmas special "Happy Compliance" (1080x1920). Key art inside the centre 1080x1440
that profile grids crop to (y 120-840 at the 540x960 drawing scale): the fully censored tree, the robot smug
with its arms out and its own line as the title, Sofía furious holding her two censored ornaments.
Drawn with the film's own kit and lighting. Usage: python3 thumb_xmas.py out.png"""
import sys
import cairo
import kit
import xmas_set as xs
import sofia_xmas as sx
import santa_robot as sr
import xmas_bubbles as xb
import xmas_anim as xa

sr.HR_FIX = True
CAM = (345, 560, 1.36)


def main(out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1080, 1920)
    c = cairo.Context(surf); c.scale(2, 2)
    k = kit.Ctx(c, 0)
    xs.lights, xs.tree = xa._lights, xa._tree
    c.save(); xs.with_cam(c, CAM)
    xs.set_dressing(k, boil=1)
    xs.tree(k, censored=tuple(range(8)))
    o = sx.sofia(k, 210, xs.FEET, 1.0, "hold2", "furious", look=(0.9, 0))
    for i, (ox, oy) in enumerate(o["orns"]):
        sr.censor_bar(k, ox, oy, 58, 19, rot=(0.06 if i else -0.06), seed=980 + i)
    sr.robot(k, 478, xs.FEET, 1.0, "present", "smug", side=-1)
    c.restore()
    xb.speech(k, "Happy compliance!", xs.to_screen(CAM, 462, xs.FEET - 238 - 118), 1.0, 0.0, size=40, at=(262, 172))
    xa.vignette(c)
    surf.write_to_png(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "xmas_thumbnail.png")
