"""Cover thumbnail for "Raises for Everyone" (1080x1920). Key art inside the centre 1080x1440 that profile grids crop
to (y 120-840 at the 540x960 drawing scale): Don, grinning, holds the turkey leg over the robot's verdict (the green
glow leaking round it), Pam beside him gives him the verdict stare; Don's opening line is the title.
Drawn with the film's own kit, lighting and vignette. Usage: python3 thumb_tg.py out.png"""
import sys
import cairo
import kit
import tg_set as ts
import pam_tg as pt
import don_tg as dt
import robot_tg as rt
import xmas_bubbles as xb
import tg_anim as ta
import tg_sb as sb

dt.SMUG_FIX = True
CAM = (548, 540, 1.28)


def main(out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1080, 1920)
    c = cairo.Context(surf); c.scale(2, 2)
    k = kit.Ctx(c, 0)
    c.save(); ts.with_cam(c, CAM)
    ts.set_dressing(k, boil=1)
    scratch = kit.Ctx(cairo.Context(cairo.ImageSurface(cairo.FORMAT_ARGB32, 4, 4)), 0)
    dx_ = 515
    hx, hy = dt.don(scratch, dx_, sb.DON_FEET, 1.0, dt.POSE_BLOCK, "grin", seed=98)["hands"][1]
    sx_, sy_ = hx + 47 * 1.5, hy
    rt.robot(k, sx_, sy_ - rt.w.HEAD_Y, 1.0, "stand", "accurate", seed=97)
    gx, gy = c.user_to_device(sx_, sy_)
    gr = abs(c.user_to_device_distance(190, 0)[0])
    ts.seated(k, lambda: pt.pam(k, 392, sb.SEAT - 20, 1.0, "stand", "stare", look=(0.9, 0), seed=96))
    o = dt.don(k, dx_, sb.DON_FEET, 1.0, dt.POSE_BLOCK, "grin", look=(-0.6, 0.2), seed=98, leg=(3, 0, 1, 1.5))
    lx = o["hands"][0][0]
    ts.table(k, 1, props=True, form_at=(lx - 10, ts.TABLE_TOP + 8))
    c.restore()
    c.save(); c.identity_matrix()
    ta._glow(c, gx, gy, gr, 0.24, rt.GREEN)
    c.restore()
    head = ts.to_screen(CAM, dx_, sb.DON_FEET + sb.DON_HY - 70)
    xb.speech(k, "Raises for everyone!", head, 1.0, 0.0, size=40, at=(250, 178))
    ta.vignette(c)
    surf.write_to_png(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "tg_thumbnail.png")
