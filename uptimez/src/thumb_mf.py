"""Cover for "Mandatory Fun" (1080x1920). Key art inside the centre 1080x1440 that profile grids crop to (y 120-840 at
the 540x960 drawing scale): the payoff. Don, cuffed to Pam, panics; Pam beams; the robot's green FUN DETECTED beam
lands on her smile, crossing him. The MANDATORY FUN slide is the title, tilted like a sticker. Drawn with the film's
own kit, glow and vignette (the robot is cheated a step closer so all three fit). Usage: python3 thumb_mf.py out.png"""
import sys
import math
import cairo
import kit
import mf_set as ms
import mf_set_sheet as ss
import don_mf as dm
import pam_mf as pm
import robot_mf as rm
import props_mf as pr
import mf_anim as fa

CAM = (706, 496, 1.36)
X = ms.POS
SEAT = ss.SEAT


def main(out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1080, 1920)
    c = cairo.Context(surf); c.scale(2, 2)
    k = kit.Ctx(c, 0)
    c.save(); ms.with_cam(c, CAM)
    ms.set_dressing(k)
    ms.chair_back(k, X["pam"], seed=130)
    ms.chair_back(k, X["don"], seed=130)
    d = {}
    ms.seated(k, lambda: d.update(dm.don(k, X["don"], SEAT - 20, 1.0, dm.POSE_STIFF, "panic", belt_cuffs_on=False,
                                         seed=98)))
    p_ = {}
    ms.seated(k, lambda: p_.update(pm.pam(k, X["pam"], SEAT, 1.0, ss.PAM_ARM, "happy", seed=96)))
    o = rm.robot(k, 560, ms.FEET_BACK + 6, 1.0, "stand", "detected", seed=97)
    ms.table(k)
    ss.chain_on_table(k, (X["don"] + 44, ms.TABLE_TOP - 6))
    kit.ellipse(k, X["don"] + 36, ms.TABLE_TOP - 2, 9, 9, dm.SKIN, 8, shadow=False, lw=2)
    pr.cuff(k, X["don"] + 46, ms.TABLE_TOP - 4, 1.0, math.pi / 2, loop_side=1)
    sx_, sy_ = o["screen"]
    ss.laser(k, (sx_ + 44, sy_ + 6), (p_["head"][0], p_["head"][1] + 30), rm.GREEN)
    gx, gy = c.user_to_device(sx_, sy_)
    gr = abs(c.user_to_device_distance(190, 0)[0])
    c.restore()
    c.save(); c.identity_matrix()
    fa._glow(c, gx, gy, gr, 0.22, rm.GREEN)
    c.restore()
    c.save(); c.translate(270, 222); c.rotate(-0.05)               # the title: the slide, tilted like a sticker
    c.set_source_rgba(0, 0, 0, 0.25); c.rectangle(-180 + 6, -92 + 8, 360, 184); c.fill()
    ms.slide(k, -180, -92, 360, 184)
    c.restore()
    fa.vignette(c)
    surf.write_to_png(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "mf_thumbnail.png")
